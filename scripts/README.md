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

## Studio (`scripts/studio/`)

| Script | What it does | Run |
|---|---|---|
| `house_rule_scan.luau` | Read-only scan of a place for house-rule debt: visible primitive Parts, meshes uploaded by someone other than the game's owner, world geometry players can walk through. Groups findings by area and caps its output. Unexecuted sketch: reviewed by reading, never run in Studio | Edit mode only: paste into the command bar, or send through the Studio MCP's `execute_luau` with `datamodel_type = "Edit"`. How to read the result: `references/checklists.md`, Gate 4 |

## UI (`scripts/ui/`)

| Script | What it does | Run |
|---|---|---|
| `ui_device_check.luau` | Switches Studio's Device Simulator through six presets (Galaxy A06, iPhone 17 Pro, Fire HD 10, iPad 10th generation, Average Windows, HD 1080), reads the live UI's `AbsolutePosition`/`AbsoluteSize` and reports per device: safe frame, HUD coverage and centre-box share, buttons in the jump, thumbstick, hotbar, chat or player-list zones, taps under 44 px, text under 14 px (12 for bold stroked or plated text), off-frame elements, short backdrops and overlaps between ScreenGuis. By JoCoding-Inc, MIT (`LICENSE-JoCoding.txt`), unchanged below an added header. Reviewed by reading, not run here. Adds three probe ScreenGuis and changes the simulated device, then removes and restores them | Studio MCP `execute_luau` in Play with the Client datamodel (Edit checks `StarterGui` only, with a frame 58 px too tall). How to read it: `references/ui-input-crossplatform.md` §Mobile layout and thumb zones |

## Vault (`scripts/vault/`)

Python 3, standard library only.

| Script | What it does | Run |
|---|---|---|
| `build_vault.py` | Turns this repository into an Obsidian vault for humans and agents: about 200 notes in numbered topic folders, YAML front matter (title, aliases, tags, summary, source), wikilinks in place of repo paths (heading links where a § points to a numbered section), the knowledge base split by section, a gallery of the reference sheets, a vault map, a path map and `vault-index.json`. Ends with a link check. Deletes and rewrites only `<out>/Roblox Game Dev Playbook/`. | `python scripts/vault/build_vault.py . "<vault folder>"`; add `--kit "<folder>"` (repeatable) to copy a private UI kit or a downloaded icon pack into `21 Private Kits/` with an index note, without it ever entering this repo |
| `search_vault.py` | Copied into the vault's `99 Meta/`: ranks notes for a query by title, aliases, skill trigger phrases, tags, headings, summary and full text. | `python "99 Meta/search_vault.py" "my game is laggy" -n 10` |

`AGENTS.md`, `CLAUDE.md` and `Start Here.md` in the same folder are the vault's entry pages; the builder copies them in.

## What was tested, and what was not

- Tested on 2026-11-10 with the standalone `bpy` 5.2.3 LTS Python module, driving each script the way `blender -b file.blend -P script.py -- args` does: a five-piece test file, every flag above, and the exported GLBs re-read to confirm names, triangle counts, sizes and vertex colour.
- `scripts/ui/ui_device_check.luau`: read line by line on 2026-11-27; not run in this repository. Its author reports testing in Studio 0.747 on 2026-11-12.
- Not tested: the Blender desktop binary itself, any Blender version other than 5.2.3, skinned meshes (`SK_`), very large files, and what Roblox Studio does with the exported GLBs. Do one test import of a piece with an obvious front, a `_COL` child and an `_Att` marker before trusting a whole kit. In particular, the scripts treat `_Att` markers as Blender empties, while the Roblox docs describe the `_Att` conversion for mesh objects: if an empty does not arrive as an Attachment, see "Naming and hierarchy" in `references/art-pipeline-blender.md`.
- Not shipped: a Blender-to-Studio upload script and the owner's live-Blender bridge (`tools/blender_exec.py` in the owner's game repos). Upload with the Studio MCP `open_cloud_invoke` tool, the official Roblox Blender add-on, or the 3D Importer by hand; drive a live Blender with the official Blender MCP server, or skip live control and run these scripts headless. Details: "Upload routes" in `references/art-pipeline-blender.md`.
