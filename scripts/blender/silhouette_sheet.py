"""Render black-on-white silhouettes of kit pieces from the four views that matter on Roblox.

Usage:

    blender -b --factory-startup kit.blend -P scripts/blender/silhouette_sheet.py -- --out build/silhouettes
    blender -b --factory-startup kit.blend -P scripts/blender/silhouette_sheet.py -- --out build/silhouettes --px 64 --only SM_Pet_Dragon_A
    blender -b --factory-startup kit.blend -P scripts/blender/silhouette_sheet.py -- --out build/silhouettes --roster

For each asset (a parentless object named SM_*, KIT_* or SK_*) it writes
<Asset>_side.png, <Asset>_front34.png, <Asset>_high34.png and <Asset>_top.png at --px pixels
square (default 96, close to in-game size on a phone). With --roster it also renders all
assets at one shared scale, in name order, joined left to right as Roster_<view>.png, so their
outlines and relative sizes can be compared side by side.
`_COL` collision proxies are hidden. Read the result with the four-view test in
references/blender-modeling-craft.md.

Uses Cycles on the CPU with one sample, so it runs on machines and CI runners without a GPU.
Safety: no network access, nothing beyond bpy and the standard library, writes PNG files only
inside --out, never saves the .blend (render settings are changed in memory only).

Tested 2026-11-10 with the standalone `bpy` 5.2.3 LTS module driving it as
`blender -b file.blend -P silhouette_sheet.py -- ...` would, with and without --roster; the PNGs
were opened and showed solid black shapes on white. Not tested: the Blender desktop binary, other Blender versions.
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

VIEWS = (("side", 90, 0), ("front34", 45, 0), ("high34", 45, 35), ("top", 0, 85))


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(prog="silhouette_sheet.py", description="Silhouette renders for kit pieces.")
    p.add_argument("--out", required=True)
    p.add_argument("--only", nargs="*", default=None)
    p.add_argument("--prefixes", default="SM_,KIT_,SK_")
    p.add_argument("--px", type=int, default=96)
    p.add_argument("--roster", action="store_true")
    return p.parse_args(argv)


def setup_scene(px):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 1
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = sc.render.resolution_y = px
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    world = sc.world or bpy.data.worlds.new("SilhouetteWorld")
    sc.world = world
    if world.node_tree is None:  # Blender 5 creates node trees by default; older versions need the switch
        world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    black = bpy.data.materials.new("SilhouetteBlack")
    if black.node_tree is None:
        black.use_nodes = True
    black.node_tree.nodes.clear()
    out = black.node_tree.nodes.new("ShaderNodeOutputMaterial")
    emission = black.node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs[0].default_value = (0, 0, 0, 1)
    black.node_tree.links.new(emission.outputs[0], out.inputs[0])
    bpy.context.view_layer.material_override = black
    camera = bpy.data.objects.new("SilhouetteCam", bpy.data.cameras.new("SilhouetteCam"))
    sc.collection.objects.link(camera)
    sc.camera = camera
    camera.data.type = "ORTHO"
    return sc, camera


def frame(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    centre = sum(pts, Vector()) / len(pts)
    return centre, max((p - centre).length for p in pts) or 1.0


def render_views(sc, camera, objs, stem, radius=None):
    """Render the four views of objs. Pass a shared radius to keep several assets at one scale."""
    centre, own_radius = frame(objs)
    radius = radius or own_radius
    camera.data.ortho_scale = 2.2 * radius
    paths = []
    for name, yaw, pitch in VIEWS:
        y, p = math.radians(yaw), math.radians(pitch)
        camera.location = centre + 4 * radius * Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))
        camera.rotation_euler = (centre - camera.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = f"{stem}_{name}.png"
        bpy.ops.render.render(write_still=True)
        paths.append(Path(sc.render.filepath))
    return paths


def stitch(tile_paths, out_path, px):
    """Join square tiles left to right into one PNG, then delete the tiles."""
    import numpy as np  # ships with Blender
    tiles = []
    for path in tile_paths:
        image = bpy.data.images.load(str(path))
        buffer = np.empty(px * px * 4, dtype=np.float32)
        image.pixels.foreach_get(buffer)
        tiles.append(buffer.reshape(px, px, 4))
        bpy.data.images.remove(image)
        path.unlink()
    sheet = np.concatenate(tiles, axis=1)
    out = bpy.data.images.new("RosterSheet", width=px * len(tiles), height=px)
    out.pixels.foreach_set(sheet.ravel())
    out.filepath_raw = str(out_path)
    out.file_format = "PNG"
    out.save()
    bpy.data.images.remove(out)


def main(argv=None):
    args = parse_args(argv)
    out_dir = Path(args.out).resolve()
    prefixes = tuple(p for p in args.prefixes.split(",") if p)
    roots = sorted((o for o in bpy.data.objects if o.parent is None and o.name.startswith(prefixes)
                    and (not args.only or o.name in set(args.only))), key=lambda o: o.name)
    if not roots:
        print("silhouette_sheet: no assets found")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    sc, camera = setup_scene(args.px)
    everything = [o for o in bpy.data.objects if o.type == "MESH"]
    families = {}
    for root in roots:
        visible = [o for o in (root, *root.children_recursive) if o.type == "MESH" and not o.name.endswith("_COL")]
        if visible:
            families[root.name] = visible
    written = 0
    for name, visible in families.items():
        for o in everything:
            o.hide_render = o not in visible
        written += len(render_views(sc, camera, visible, str(out_dir / name)))
    if args.roster and families:
        shared = max(frame(visible)[1] for visible in families.values())
        tiles = {view: [] for view, _, _ in VIEWS}
        for name, visible in families.items():
            for o in everything:
                o.hide_render = o not in visible
            for (view, _, _), path in zip(VIEWS, render_views(sc, camera, visible, str(out_dir / f"_tile_{name}"), shared)):
                tiles[view].append(path)
        for view, paths in tiles.items():
            stitch(paths, out_dir / f"Roster_{view}.png", args.px)
            written += 1
    print(f"silhouette_sheet: wrote {written} images to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
