"""Acceptance report for Roblox kit pieces in a .blend. Reads only; exports nothing.

Usage:

    blender -b --factory-startup kit.blend -P scripts/blender/check_asset.py --
    blender -b --factory-startup kit.blend -P scripts/blender/check_asset.py -- --only SM_Prop_Crate_A
    blender -b --factory-startup kit.blend -P scripts/blender/check_asset.py -- --out build/kit --symmetric SM_Shield_A

For every asset (a parentless object named SM_*, KIT_* or SK_*) it prints:
  - the errors and warnings export_kit.py would raise (names, transforms, UVs, materials,
    triangle limits, collision plan, origin)
  - triangles per mesh, and against a class budget if the root has a custom property `Class`
    (tiny, small, medium, rock, tree, weapon, module, building, vehicle, creature, hero)
  - share of triangle area facing up / down / sideways (bottoms of grounded props should be deleted)
  - open (non-manifold) edges, and a count of thin triangles (aspect above 8:1; bevel strips are
    counted too, so read it as a hint after decimation, not as a failure)
  - X-mirror symmetry error for roots listed after --symmetric
With --out it also writes <out>/check_report.json. Exit code 1 if any asset has an error.

These are the mechanical lines of the acceptance checklist and rubric in
references/art-pipeline-blender.md and references/blender-modeling-craft.md. Silhouette,
proportion, colour and in-game read still need eyes.

Safety: no network access; imports only bpy, the standard library and the two sibling files
(export_kit.py, modeling_helpers.py); writes one JSON file, and only when --out is given.

Tested 2026-11-10 with the standalone `bpy` 5.2.3 LTS module driving it as
`blender -b file.blend -P check_asset.py -- ...` would, on a five-asset test file
(clean crate, lamp with _COL and _Att, badly named and scaled object, scaled parent, open barrel).
Not tested: the Blender desktop binary, other Blender versions, skinned meshes.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_kit  # noqa: E402
import modeling_helpers as mh  # noqa: E402

# target, ceiling (triangles after modifiers). House defaults; tune per game in the style bible.
BUDGETS = {
    "tiny": (150, 300), "small": (600, 1500), "medium": (2000, 5000), "rock": (400, 1000),
    "tree": (2000, 5000), "weapon": (2500, 5000), "module": (800, 3000), "building": (6000, 10000),
    "vehicle": (8000, 15000), "creature": (5000, 10000), "hero": (10000, 20000),
}


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(prog="check_asset.py", description="Acceptance report for kit pieces.")
    p.add_argument("--only", nargs="*", default=None)
    p.add_argument("--prefixes", default="SM_,KIT_,SK_")
    p.add_argument("--symmetric", nargs="*", default=[], help="roots that must be X-mirror symmetric")
    p.add_argument("--out", default=None, help="directory for check_report.json (optional)")
    return p.parse_args(argv)


def report_for(root, symmetric):
    errors, warnings = export_kit.check(root)
    visual = [o for o in export_kit.meshes_of(root) if not export_kit.is_col(o)]
    tris = {o.name: export_kit.tri_count(o) for o in export_kit.meshes_of(root)}
    total = sum(n for name, n in tris.items() if not name.endswith("_COL"))
    cls = root.get("Class")
    if cls in BUDGETS:
        target, ceiling = BUDGETS[cls]
        if total > ceiling:
            errors.append(f"{root.name}: {total} triangles, over the {cls} ceiling of {ceiling}")
        elif total > target:
            warnings.append(f"{root.name}: {total} triangles, over the {cls} target of {target} (write down why)")
    elif cls is not None:
        warnings.append(f"{root.name}: unknown Class '{cls}'")
    spend, open_count, thin = {}, 0, 0
    for o in visual:
        _, spend[o.name] = mh.spend_report(o)
        open_count += mh.open_edges(o)
        thin += mh.thin_triangles(o)
    info = export_kit.describe(root)
    grounded = info["origin_in_bounds"] is not None and info["origin_in_bounds"][2] < 0.05
    if grounded and any(s["down"] >= 10 for s in spend.values()):
        warnings.append(f"{root.name}: origin is at the bottom but 10 % or more of the area faces down (delete hidden bottoms)")
    if open_count:
        warnings.append(f"{root.name}: {open_count} open edges (fine for deleted bottoms; check for holes)")
    sym = None
    if root.name in symmetric:
        sym = max(round(mh.symmetry_error(o), 4) for o in visual) if visual else None
        if sym is not None and sym > 0.01:
            errors.append(f"{root.name}: symmetry error {sym} (limit 0.01); build half and mirror")
    return {"errors": errors, "warnings": warnings, "tris": tris, "total_tris": total, "class": cls,
            "area_facing": spend, "open_edges": open_count, "thin_triangles": thin, "symmetry_error": sym, **info}


def main(argv=None):
    args = parse_args(argv)
    roots = export_kit.find_roots([p for p in args.prefixes.split(",") if p], args.only)
    if not roots:
        print("check_asset: no assets found")
        return 1
    report = {root.name: report_for(root, set(args.symmetric)) for root in roots}
    bad = 0
    for name, r in report.items():
        status = "FAIL" if r["errors"] else "PASS"
        bad += bool(r["errors"])
        print(f"{status} {name}: {r['total_tris']} tris, size {r['size']}, origin {r['origin_in_bounds']}, facing {r['area_facing']}")
        for line in r["errors"]:
            print("  ERROR " + line)
        for line in r["warnings"]:
            print("  WARNING " + line)
    if args.out:
        out_dir = Path(args.out).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "check_report.json").write_text(json.dumps(report, indent=1, sort_keys=True))
    print(f"check_asset: {len(roots)} assets, {bad} failing")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
