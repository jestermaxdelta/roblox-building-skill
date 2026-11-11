# Scripts shipped with the skill

Small, readable tools the references point to. Copy the folder into a game repo or run the scripts in place. None of them needs network access, installs anything, or saves the `.blend` it reads.

## Blender (`scripts/blender/`)

Requires Blender 5.x on the PATH. Run headless: `-b` means no window, `--factory-startup` ignores personal add-ons and preferences so results repeat on any machine, and everything after `--` goes to the script.

| Script | What it does | Run |
|---|---|---|
| `export_kit.py` | Validates every kit piece (names, applied transforms, one UV map, one material, triangle limits, collision plan, origin), then writes one GLB per piece at the origin plus `manifest.json` (file hash, triangles, size in studs, where the origin sits inside the bounds, the names of `_Att` markers, collision plan). Exits 1 if any piece fails | `blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit` |
| `check_asset.py` | The same checks without exporting, plus class budgets (custom property `Class`), where the triangles face, open edges and optional mirror-symmetry error. Prints PASS or FAIL per piece; `--out` adds `check_report.json` | `blender -b --factory-startup kit.blend -P scripts/blender/check_asset.py --` |
| `silhouette_sheet.py` | Black-on-white renders from side, front three-quarter, high three-quarter and top at in-game pixel size; `--roster` joins all pieces into one comparison strip per view. Cycles on CPU, so no GPU is needed | `blender -b --factory-startup kit.blend -P scripts/blender/silhouette_sheet.py -- --out build/silhouettes --roster` |
| `modeling_helpers.py` | Importable functions: `make_col` (convex collision proxy), `palette_uv` (collapse materials onto a palette atlas), `tri_count`, `spend_report`, `symmetry_error`, `thin_triangles`, `open_edges` | `import sys; sys.path.append(".../scripts/blender"); import modeling_helpers as mh` |

Useful flags: `--only NAME [NAME ...]` and `--prefixes SM_,KIT_,SK_` (which root names count as assets) on all three command-line scripts; `--check-only`, `--apply-transforms`, `--max-tris` and `--max-col-tris` on `export_kit.py`; `--px 64` on `silhouette_sheet.py` (default 96); `--symmetric NAME` on `check_asset.py`. Put `--python-exit-code 1` before `-P` so CI fails on a non-zero exit. Each file's docstring lists every option.

Class budgets used by `check_asset.py` are the target and ceiling table in `references/blender-modeling-craft.md` ("Recipes and budgets").

Conventions the scripts assume (from `references/art-pipeline-blender.md`): 1 Blender unit = 1 stud; an asset is a parentless object named `SM_…`, `KIT_…` or `SK_…`; collision proxies are children named `<Asset>_COL`; attachment points are empties named `<Name>_Att`; an asset without a `_COL` child carries a custom property `Fidelity` set to `Box` or `Hull`.

## Images (`scripts/images/`)

| Script | What it does | Run |
|---|---|---|
| `tile_test.py` | Shows an icon and thumbnails the way the Roblox Home grid does: icon at 150, 64 and 32 px on dark and light, each thumbnail at 320×180 and 160×90, greyscale, blurred and with the bottom 20% hidden. Writes `tile_test.png` in the current folder. Needs Pillow. Pass marks: `references/icons-thumbnails-and-store-page.md` §5. Run on 2026-11-11 | `python3 scripts/images/tile_test.py icon.png thumb1.png thumb2.png` |

## What was tested, and what was not

- Tested on 2026-11-10 with the standalone `bpy` 5.2.3 LTS Python module, driving each script the way `blender -b file.blend -P script.py -- args` does: a five-piece test file, every flag above, and the exported GLBs re-read to confirm names, triangle counts, sizes and vertex colour.
- Not tested: the Blender desktop binary itself, any Blender version other than 5.2.3, skinned meshes (`SK_`), very large files, and what Roblox Studio does with the exported GLBs. Do one test import of a piece with an obvious front, a `_COL` child and an `_Att` marker before trusting a whole kit. In particular, the scripts treat `_Att` markers as Blender empties, while the Roblox docs describe the `_Att` conversion for mesh objects: if an empty does not arrive as an Attachment, see "Naming and hierarchy" in `references/art-pipeline-blender.md`.
- Not shipped: a Blender-to-Studio upload script and the owner's live-Blender bridge (`tools/blender_exec.py` in the owner's game repos). Upload with the Studio MCP `open_cloud_invoke` tool, the official Roblox Blender add-on, or the 3D Importer by hand; drive a live Blender with the official Blender MCP server, or skip live control and run these scripts headless. Details: "Upload routes" in `references/art-pipeline-blender.md`.
