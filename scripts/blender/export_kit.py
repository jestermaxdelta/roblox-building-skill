"""Batch-export Roblox kit pieces from a .blend: one GLB per asset plus manifest.json.

Usage (run from the game repo; nothing is installed and the .blend is never saved):

    blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit
    blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit --only SM_Prop_Crate_A
    blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit --check-only
    blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit --apply-transforms

Add `--python-exit-code 1` before `-P` in CI so a failed check fails the job.

What is an asset: every object without a parent whose name starts with SM_, KIT_ or SK_
(change with --prefixes). Its children are exported with it, so `<Asset>_COL` collision
proxies and `<Name>_Att` empties travel in the same GLB.

Checks (any error skips that asset and makes the script exit 1):
  - names use only A-Z a-z 0-9 _ (dots and spaces get mangled on upload)
  - rotation 0 and scale 1 on every mesh (or pass --apply-transforms)
  - exactly one UV map and at most one material on visual meshes
  - triangle count after modifiers <= --max-tris (20000, the Roblox per-mesh limit)
  - `_COL` children: no material, <= --max-col-tris (200)
  - a collision plan: a `_COL` child, or a custom property `Fidelity` ("Box" or "Hull") on the root
Warnings (exported anyway): n-gons before triangulation, more than one colour attribute,
origin outside the asset's bounding box.

What it does to each asset before export, in memory only: renames mesh datablocks to
`<Object>_Mesh` (stable names for Studio Reimport), appends a Triangulate modifier if there is
none, moves the root to the world origin (the Blender origin becomes the Roblox pivot), then
exports with modifiers applied, +Y up, no animation, and the ACTIVE vertex colour attribute
(the exporter default writes a placeholder COLOR_0 when the material does not use the colour).

Safety: no network access, no imports beyond bpy and the standard library, writes only inside
--out, never saves the .blend.

Tested 2026-11-10 with the standalone `bpy` 5.2.3 LTS module driving it exactly as
`blender -b file.blend -P export_kit.py -- ...` would (file opened, argv after `--`):
export, --only, --check-only and --apply-transforms on a five-asset test file, then the GLBs
were re-read to confirm node names, mesh names, triangle counts and COLOR_0.
Not tested: the Blender desktop binary itself, Blender versions other than 5.2.3, skinned
meshes (SK_), and the import of the results into Roblox Studio.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector

NAME_RE = re.compile(r"[A-Za-z0-9_]+")


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(prog="export_kit.py", description="Export Roblox kit pieces as GLB.")
    p.add_argument("--out", required=True, help="output directory (created if missing)")
    p.add_argument("--only", nargs="*", default=None, help="export only these root object names")
    p.add_argument("--prefixes", default="SM_,KIT_,SK_", help="comma-separated root name prefixes")
    p.add_argument("--max-tris", type=int, default=20000)
    p.add_argument("--max-col-tris", type=int, default=200)
    p.add_argument("--apply-transforms", action="store_true", help="apply rotation and scale in memory first")
    p.add_argument("--check-only", action="store_true", help="validate and print, write nothing")
    return p.parse_args(argv)


def is_col(obj):
    return obj.name.endswith("_COL")


def family_of(root):
    return [root, *root.children_recursive]


def meshes_of(root):
    return [o for o in family_of(root) if o.type == "MESH"]


def tri_count(obj):
    """Triangles after modifiers, which is what ships."""
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    n = sum(len(p.vertices) - 2 for p in me.polygons)
    ev.to_mesh_clear()
    return n


def ngon_count(obj):
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    n = sum(1 for p in me.polygons if len(p.vertices) > 4)
    ev.to_mesh_clear()
    return n


def find_roots(prefixes, only=None):
    roots = [o for o in bpy.data.objects if o.parent is None and o.name.startswith(tuple(prefixes))]
    if only:
        roots = [o for o in roots if o.name in set(only)]
    return sorted(roots, key=lambda o: o.name)


def apply_transforms(root):
    """Apply rotation and scale on the whole family (in memory). Returns an error string or None."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in family_of(root):
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = root
    try:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    except RuntimeError as exc:
        return f"{root.name}: could not apply transforms ({str(exc).strip()})"
    return None


def bounds(root):
    """World-space bounding box (min, max) of the visual meshes, after modifiers."""
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in meshes_of(root):
        if is_col(o):
            continue
        ev = o.evaluated_get(dg)
        pts += [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    if not pts:
        return None
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def check(root, max_tris=20000, max_col_tris=200):
    """Return (errors, warnings) for one asset. Changes nothing."""
    errors, warnings = [], []
    members = family_of(root)
    meshes = meshes_of(root)
    for o in members:
        if not NAME_RE.fullmatch(o.name):
            errors.append(f"{o.name}: use only A-Z a-z 0-9 _ in names")
    if not any(not is_col(o) for o in meshes):
        errors.append(f"{root.name}: no visual mesh")
    for o in meshes:
        col = is_col(o)
        if any(abs(s - 1) > 1e-4 for s in o.scale) or any(abs(r) > 1e-4 for r in o.rotation_euler):
            errors.append(f"{o.name}: unapplied rotation or scale (Ctrl+A, or pass --apply-transforms)")
        slots = len([s for s in o.material_slots if s.material])
        tris = tri_count(o)
        if tris == 0:
            errors.append(f"{o.name}: mesh has no triangles")
        if col:
            if slots:
                errors.append(f"{o.name}: collision proxies carry no material")
            if tris > max_col_tris:
                errors.append(f"{o.name}: {tris} triangles, collision proxy limit is {max_col_tris}")
        else:
            if len(o.data.uv_layers) != 1:
                errors.append(f"{o.name}: {len(o.data.uv_layers)} UV maps (need exactly 1)")
            if slots > 1:
                errors.append(f"{o.name}: {slots} materials (one per mesh; each extra becomes another MeshPart)")
            if tris > max_tris:
                errors.append(f"{o.name}: {tris} triangles, limit is {max_tris}")
            if ngon_count(o):
                warnings.append(f"{o.name}: {ngon_count(o)} n-gons before triangulation (the export triangulates them; add a Triangulate modifier after Bevel to control how)")
            if len(o.data.color_attributes) > 1:
                warnings.append(f"{o.name}: {len(o.data.color_attributes)} colour attributes (keep one; extra layers get exported)")
    fidelity = root.get("Fidelity")
    has_col = any(is_col(o) for o in meshes)
    if not has_col and fidelity not in ("Box", "Hull"):
        errors.append(f"{root.name}: no collision plan (add a {root.name}_COL child or a custom property Fidelity = Box or Hull)")
    box = bounds(root)
    if box:
        lo, hi = box
        pad = 0.05 * max((hi - lo).length, 1e-6)
        origin = root.matrix_world.translation
        if any(origin[i] < lo[i] - pad or origin[i] > hi[i] + pad for i in range(3)):
            warnings.append(f"{root.name}: origin lies outside the mesh bounds (the origin becomes the Roblox pivot)")
    return errors, warnings


def describe(root):
    """Facts for the manifest: size in studs, where the origin sits inside the bounds, attachments."""
    info = {"size": None, "origin_in_bounds": None}
    box = bounds(root)
    if box:
        lo, hi = box
        size = hi - lo
        origin = root.matrix_world.translation
        info["size"] = [round(v, 3) for v in size]
        info["origin_in_bounds"] = [round((origin[i] - lo[i]) / size[i], 3) if size[i] > 1e-9 else 0.5 for i in range(3)]
    info["attachments"] = sorted(o.name for o in family_of(root) if o.type == "EMPTY" and o.name.endswith("_Att"))
    return info


def prepare(root):
    """In-memory export preparation: stable datablock names and a final Triangulate modifier."""
    for o in meshes_of(root):
        o.data.name = o.name + "_Mesh"
        if not any(m.type == "TRIANGULATE" for m in o.modifiers):
            o.modifiers.new("ExportTriangulate", "TRIANGULATE")


def export_glb(root, path):
    saved = root.matrix_world.copy()
    root.location = (0.0, 0.0, 0.0)
    bpy.ops.object.select_all(action="DESELECT")
    for o in family_of(root):
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = root
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(path), export_format="GLB", use_selection=True,
            export_apply=True, export_yup=True, export_animations=False,
            export_vertex_color="ACTIVE", export_all_vertex_colors=False,
        )
    finally:
        root.matrix_world = saved


def main(argv=None):
    args = parse_args(argv)
    out_dir = Path(args.out).resolve()
    prefixes = [p for p in args.prefixes.split(",") if p]
    roots = find_roots(prefixes, args.only)
    if not roots:
        print(f"export_kit: no root objects starting with {prefixes} (or matching --only)")
        return 1
    if not args.check_only:
        out_dir.mkdir(parents=True, exist_ok=True)
    assets, failed, warned, passed = {}, [], [], 0
    for root in roots:
        if args.apply_transforms:
            problem = apply_transforms(root)
            if problem:
                failed.append(problem)
                continue
        errors, warnings = check(root, args.max_tris, args.max_col_tris)
        warned += warnings
        if errors:
            failed += errors
            continue
        passed += 1
        if args.check_only:
            continue
        info = describe(root)
        prepare(root)
        path = out_dir / f"{root.name}.glb"
        export_glb(root, path)
        meshes = meshes_of(root)
        assets[root.name] = {
            "file": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "tris": {o.name: tri_count(o) for o in meshes},
            "fidelity": root.get("Fidelity"),
            "has_col": any(is_col(o) for o in meshes),
            "vertex_colour": any(len(o.data.color_attributes) > 0 for o in meshes if not is_col(o)),
            **info,
            "warnings": [w for w in warnings],
        }
    if not args.check_only:
        manifest = {"blender": bpy.app.version_string, "unit": "1 Blender unit = 1 stud", "assets": assets}
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True))
    for line in warned:
        print("WARNING " + line)
    for line in failed:
        print("ERROR " + line)
    done = "passed the checks" if args.check_only else "exported"
    print(f"export_kit: {len(roots)} assets found, {passed} {done}, {len(failed)} errors, {len(warned)} warnings")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
