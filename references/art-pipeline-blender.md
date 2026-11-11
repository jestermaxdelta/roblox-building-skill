# Blender-to-Roblox art pipeline

The house art pipeline from a finished Blender model to a placed, colliding, instanced Roblox asset: units, naming, texturing method, collision plan, headless GLB export, upload, Studio fix-up, packages. Open it when setting up a kit file, writing export or import tooling, or auditing a live game's collisions, draw calls, texture memory or broken imports (jump to "Level-up"). It does not own the look: the style bible and the generic-look tells are `references/art-direction-and-quality-bar.md` (§6, §2), modelling rules are `references/blender-modeling-craft.md`, lighting is `references/lighting-and-atmosphere.md`. House rules 1 and 2: every visible object is a Blender model, nothing visible is a primitive Part or a marketplace asset, and everything visible is solid. Platform facts re-verified against `Roblox/creator-docs` (commit 7cbffff of 2026-11-10) and the DevForum announcements listed under Sources. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

## Start here by level

| Level | Do these first | Leave for later |
|---|---|---|
| Beginner | Work at 1 Blender unit = 1 stud beside an R15 dummy. Apply transforms, one material, origin where the asset attaches. Export by hand (File > Export > glTF 2.0, selected objects, Apply Modifiers) or with the shipped `scripts/blender/export_kit.py`, import with the preset below, then walk on the asset. Build the first kit in `references/blender-modeling-craft.md` | PBR maps, trim sheets, Open Cloud keys, Geometry Nodes, SLIM |
| Intermediate | Fill in the style bible (`art-direction-and-quality-bar.md` §6). Pick one texturing method. Give every asset a collision plan (`Fidelity` or `_COL`). Wrap pieces as packages, choose one upload route and keep the ids manifest. Run the acceptance checklist on every asset | Custom CI, layout export |
| Expert | Hash-skipping uploads in CI, duplicate-MeshId and instancing audits, merge-or-modular decisions measured in Shift+F2, Reimport and package versioning, layout transforms from Geometry Nodes, the mesh-streaming rollout, phone measurements under final lighting | Nothing: read "Platform limits" and "Import traps" in full |

Terms used below: a **MeshPart** is the Roblox instance one imported mesh becomes; a **draw call** is one batch of geometry sent to the GPU; **instancing** is the engine drawing copies of the same mesh in one draw call; a **SurfaceAppearance** is the child object holding a MeshPart's PBR texture maps; a **package** is a versioned, auto-updating asset wrapper. Rigs and animation are in `references/animation-and-rigs.md`.

Contents: Pipeline overview · Platform limits · Units and transforms · Grid and pivots · Mesh specifications · Texturing strategy · Naming · Collision · Blender automation · Upload routes · Importer preset · Post-import fix-up · Import traps · Kits, instancing, merging · Style bible and lighting (pointers) · Acceptance checklist · Level-up · Review gate · Sources

## Pipeline overview

1. **Style bible and kit plan first**: fill in the one-page template in `art-direction-and-quality-bar.md` §6 before the first mesh.
2. **Author in Blender**, by hand or by driving a running Blender through a Blender MCP server (the official Blender Lab MCP; see `references/ai-toolchain-skills.md`). The owner's game repos also carry an optional bridge script, `tools/blender_exec.py`, that posts Python to that server; it is not shipped with this skill and nothing here needs it. Without any live connection, write a build script and run it headless with `blender -b -P`. Use a live session for modelling, validation and layout, never for export.
3. **Validate in Blender**: `blender -b --factory-startup <kit>.blend -P scripts/blender/check_asset.py --` (names, transforms, UVs, one material, budgets, collision plan, origin).
4. **Export GLB in a separate headless process**: `blender -b --factory-startup assets/blender/<kit>.blend -P scripts/blender/export_kit.py -- --out build/<kit>` (script shipped with this skill). Never export from the MCP-driven session.
5. **Upload**: Open Cloud key in CI, or the Studio MCP `open_cloud_invoke` route for interactive agent work (see "Upload routes"). Record ids in a manifest.
6. **Insert into Studio** and run the post-import fix-up (anchoring, collision flags, `_COL` handling, CastShadow, shared SurfaceAppearances).
7. **Wrap each kit piece or prop as a package** (PackageLink, AutoUpdate on). Place package copies, never fresh imports.
8. **QA under final lighting** at a low graphics level and on a real phone, then run the asset acceptance checklist.

Blockout rule: no primitive greybox ships. Prototype with a Blender blockout kit (a handful of boxy GLB modules) or in a throwaway place that is never published.

## Platform limits and behaviours `[VS]`

| Item | Limit or behaviour `[official]` |
|---|---|
| Triangles | ≤ 20,000 per mesh. Watertight, no n-gons, no zero-thickness geometry. No 2026 increase found. |
| Materials, UVs | One material per mesh. One UV set, inside 0–1, overlaps allowed. |
| Texture size | Up to 4096² renders on MeshPart textures, SurfaceAppearance maps, Texture, Decal and MaterialVariant, through texture streaming (automatic: a baseline loads first, quality rises to the device's memory budget; live since 2026-01-30). Devices under about 3.5 GB of memory have 4K disabled `[official: staff posts]`. UI images, SurfaceGui content, Terrain and Sky faces are not on texture streaming yet (listed as work in progress, 2026-03), and a 2026-10 bug report shows UI images above 1024² being downscaled `[community]`. Uploads up to 8K are stored and transcoded down. Doc guidance: 256² per 5×5 studs, 512² per 10×10, 1024² per 20×20 (about 51 px per stud). |
| Texture formats | png, jpg, tga, bmp. Open Cloud images must be under 8000×8000. Albedo and normal 24-bit RGB (normal: OpenGL tangent space); roughness, metalness, emissive mask 8-bit grey. |
| Import formats | `.fbx`, `.gltf`/`.glb`, `.obj`. FBX and glTF carry hierarchies, PBR textures, cages, rigs, animation data and vertex colours. Asset Manager bulk import does not take rigs, skins or animation. |
| glTF hierarchy | Each node becomes a Model holding one MeshPart per primitive of its mesh (FBX: MeshParts sit directly in the top Model). If a node and its mesh share a name, one of them gets `_Node`. |
| Naming hooks | Objects named `…_Att` → Attachment; `_OuterCage` → WrapTarget; `_InnerCage` + `_OuterCage` → WrapLayer. The docs word the `_Att` rule as "mesh objects", and the character-body page says it applies when importing meshes with cage data; whether a Blender empty in a prop GLB arrives as an Attachment is not documented (see "Naming and hierarchy"). No collision-mesh naming hook is documented. |
| Skinned meshes | Bones scale 1, rotation 0; root at origin; ≤ 4 influences per vertex; none on the root; one animation track per FBX. |
| `RenderFidelity` | Automatic: full detail under 250 studs, medium 250–500, lowest beyond 500. Performance and Precise are the manual options. No import path for hand-made LOD chains. Being replaced: with `Workspace.MeshStreamingAndImprovedLods = Enabled` (opt-in since 2026-04-27) the property is ignored and the engine picks cloud-generated LODs by screen importance and memory; Roblox plans to make that the default and then remove both properties `[official: staff post]`. |
| `CollisionFidelity` | Box, Hull, Default, PreciseConvexDecomposition, Tunable (adds `CollisionPrecision`). Collision data is stored even with `CanCollide = false`. |
| Open Cloud upload | One asset per call, ≤ 20 MB. Model accepts `model/fbx`, `model/gltf+json`, `model/gltf-binary`, arrives as a package of MeshParts. Create Asset is marked beta. Content update (PATCH) works for `.fbx` only. |
| Rate limits | No per-endpoint number is published for the Assets API in the mirrored spec; undocumented limits may apply and are counted per key owner. Read `x-ratelimit-*` headers and back off on HTTP 429. |
| Upload cost | No fee is documented for model or image uploads in the pages read. Audio and video have quotas. Send `creationContext.expectedPrice: 0` so an unexpected fee fails the call. |
| Moderation | Human and automated; "generally within a few hours". An asset still in the queue is invisible to players in a published game. Operation states: `Reviewing`, `Approved`, `Rejected`. |
| Asset privacy | Images, Decals and Meshes are Open Use by default; with Asset Privacy enabled they are created Restricted and each game needs a grant. Open Use cannot be undone; game grants are permanent. |
| Misc | Light `Range` is clamped to 120 studs. Shadows switch off below graphics quality level 4. Draw distance is at least 500 studs at the lowest quality level (since 2026-11-05). SLIM needs streaming, a published place and Team Create, and static models without a Humanoid. |

The texture spec page still says both "supports up to 4096×4096" and, under UV mapping, "up to 1024×1024 pixel spaces"; the staff posts above settle it (4K on streamed 3D surfaces, 1024² elsewhere). House cap stays 1024², mostly ≤ 512²: the target 3 GB phone is below the 4K memory line, and a staff reply confirms 4K and full texture streaming are off on a 3 GB iPad `[community: staff reply]`. Community guides that quote 10,000 or 21,000 triangles are wrong or stale.

## Units, scale, orientation, transforms

- 1 stud = 0.28 m (1 m ≈ 3.57 studs). Gravity 196.2 studs/s².
- Convention: **1 Blender unit = 1 stud** (Studio importer Scale Unit = Stud). Blender Scene > Units > Unit System = None (or Metric with Unit Scale 1), Rotation = Degrees. Do not mix with metric-scale assets (importer Scale Unit = Meter multiplies by about 3.57). The web API exposes no import settings `[community]`, so the file itself must already be in studs.
- Keep an R15 dummy exported from Studio in a hidden Blender collection; Roblox avatars are chunky, so size doors, counters, steps and seats against it.
- Orientation: glTF exports +Y up; model assets facing −Y in Blender; Studio importer World Forward = Front, World Up = Top; confirm once with an asset that has an obvious front.
- Apply all transforms (rotation 0, scale 1) and modifiers before export. Unapplied scale, an unapplied Mirror modifier and flipped normals are the usual causes of inside-out or dark shading after import `[house]`.

## Grid and pivots

- One grid per project, written in the style bible. Architecture on 5, 8 or 16 studs (5 in the environmental-art curriculum, 16 in Beyond the Dark `[official]`; a 4-stud module cannot hold the 5-stud gameplay door); props and trims on a sub-grid of it (4 or 2).
- Modular kit pivots at the front-lower corner so pieces snap edge to edge in 90° steps. Prop pivots where the prop attaches: bottom-centre for floor props, back-centre for wall props, top-centre for hanging props.
- The export script moves each asset's origin to world (0,0,0) so Use Imported Pivot, Set Pivot to Scene Origin and Insert Using Scene Position agree.

## Mesh specifications

One material per mesh (each extra slot becomes another MeshPart, draw call and collision shape); consistent normals; Make Double Sided only where a single-sided surface is unavoidable (canopies are solid blobs here, not cards). Triangles are counted after modifiers, so the bevel is part of the budget (a one-segment bevel turns a 12-triangle box into 44, two segments into 108).

Class budgets (target and ceiling per class, from clutter at 150 / 300 to hero landmarks at 10,000 / 20,000 per mesh) are the table in `references/blender-modeling-craft.md` ("Recipes and budgets"); `check_asset.py` enforces the same numbers through the `Class` custom property. The only budget set here: collision proxies (`_COL`) 12–200 triangles. Bevel widths come from the viewing-distance table in the same file.

## Texturing strategy

| Method | Use for | Cost | Rule |
|---|---|---|---|
| Palette atlas ("palette UV") | Flat-colour stylised props, vehicles, NPCs | One 256² ColorMap for the whole game | UV islands collapsed onto swatch cells; no normal or roughness maps |
| Trim sheets | Architecture and hard surface that needs PBR detail | 4–8 sets at ≤ 1024² | Follow Active Quads onto the bands; no recognisable stains |
| Tileable MaterialVariant | Ground, long walls | Engine-shared | Set as Override, Organic tiling |
| Unique bake | Hero landmark, hero NPC | ≤ 1024² each | Cap the count in the style bible |
| Vertex colour | Baked AO, height gradients, tint variation | No texture memory | Export with `export_vertex_color="ACTIVE"` |

Pick one primary method per game and write it in the style bible; two methods meeting in one view is a cohesion failure (`art-direction-and-quality-bar.md` §2).

Palette atlas method:
1. Paint one atlas: a 16×16 grid of flat swatches from the style-bible palette, plus a few vertical gradient strips. Cells ≥ 16 px.
2. Every mesh uses the single material `M_Palette`. Run `palette_uv()` from `scripts/blender/modeling_helpers.py` to snap each face to its swatch centre. For a gradient, keep U on the strip and map V to height.
3. In Studio every MeshPart shares one `Palette_SA` (ColorMap only) or one `TextureID`. `SurfaceAppearance.ResampleMode = Pixelated` stops neighbouring swatches blurring together `[official, VS]`. Keep UVs ≥ 2 px inside a cell and never rely on sub-cell detail: phones may show a lower mip `[community]`.
4. Form comes from bevels, vertex-colour AO and lighting, not from the texture.
5. A re-skin (season, event, night palette) is one texture swap. For per-instance tint, `SurfaceAppearance.Color` tints the ColorMap (author those swatches near-white), or leave swatch alpha at 0 under Overlay so `MeshPart.Color` shows through.
6. A shared texture cuts texture memory, not draw calls: instancing needs the same MeshId as well.

PBR details (trim and unique routes): ColorMap sRGB, near-white if tinted; NormalMap OpenGL tangent space, never DirectX; RoughnessMap +0.1 to offset Roblox's Fresnel; MetalnessMap 0 or 1; emissive through `EmissiveMaskContent`, `EmissiveStrength`, `EmissiveTint` `[VS]`. `AlphaMode`: Overlay (default), Transparency (cutout at part Transparency 0), TintMask, Opaque (beta `[VS]`). Most SurfaceAppearance properties cannot change at runtime, so variants are separate instances; on publish the engine bakes the maps into one texture pack. One SurfaceAppearance per material named `<Name>_SA`, published as a package material library; the post-import script swaps Blender placeholder materials (`M_Trim_Metal`) for the matching `_SA`. Texel density: one figure, constant across the kit. Start at about 50 px per stud (the docs' guidance works out to 51; a 1024² map then covers a 20-stud wall). More than 64 is invisible on a 720 px phone even at 8 studs; up to 100 pays off only on arm's-length props on a 1080p screen.

## Naming and hierarchy

| Convention | Meaning |
|---|---|
| `SM_<Category>_<Name>_<Variant>` | Static mesh, e.g. `SM_Street_Lamp_A` |
| `SK_<Name>` | Skinned mesh |
| `KIT_<Set>_<Piece>_<WxH>_<Variant>` | Modular piece, e.g. `KIT_Shop_Wall_16x12_A` |
| `<Asset>_COL` | Invisible collision proxy (house convention; Roblox has no UCX_ auto-collision) |
| `<Name>_Att` | Imported as an Attachment: `Prompt_Att`, `Light_Att`, `VFX_Steam_Att`, `Seat_Att` |
| `<Object>_Mesh` | Mesh datablock name, set by the export script |
| `<Name>_SA` / `M_<Library>_<Name>` | SurfaceAppearance / Blender placeholder material |

Under glTF the mesh datablock name reaches Studio as well as the object name (hence the `_Node` rule), and Reimport matches on mesh path and name. Blender's defaults (`Cube.014`) are neither unique nor stable, so the export script renames every datablock to `<Object>_Mesh`; which name lands on the MeshPart is not documented, so check one test import `[VS]`. Split multi-part assets into named children (`Door`, `Frame`, `Handle_Att`) so moving parts can animate and each piece gets the right collision. `_Att` markers are the hand-off between art and code: scripts find attachments by name instead of hard-coding offsets. Unverified `[VS]`: the scripts and the walkthrough use Blender empties, the docs describe `_Att` **mesh objects**, and an older forum answer says FBX empties are dropped. On the first test import, check that every `_Att` arrived as an Attachment at the right place. If not, make each marker a one-triangle mesh object named `…_Att`, or add the Attachments in the fix-up script.

## Collision authoring

- Decide per asset: fidelity on the visual mesh (custom property `Fidelity` = `Box` or `Hull` on the root) or a `_COL` child. The export script refuses an asset with neither.
- `_COL` proxies are convex (or a few convex pieces), have no material, 12–200 triangles, sit flush on walkable surfaces. Doorways use three boxes (two jambs and a lintel); stairs use a single ramp. `make_col()` in `scripts/blender/modeling_helpers.py` builds a hull for convex props; concave assets need hand-made pieces.
- Tunable fidelity with `CollisionPrecision` is the newer middle ground for one-off concave shapes `[VS]`; view the result with Visualization Options > Collision fidelity.
- Flags after import are in performance.md ("Making everything solid").

## Blender automation

The skill ships its Blender tools in `scripts/blender/` (usage and test notes in `scripts/README.md`); copy the folder into the game repo. All run headless, need nothing beyond Blender, write only inside the output folder and never save the `.blend`.

| Script | Use | Command |
|---|---|---|
| `export_kit.py` | Validate, then write one GLB per kit piece at the origin plus `manifest.json` (hash, triangles, size, pivot position, attachments, collision plan). `--only`, `--check-only`, `--apply-transforms` | `blender -b --factory-startup kit.blend -P scripts/blender/export_kit.py -- --out build/kit` |
| `check_asset.py` | The same checks without exporting, plus class budgets (`Class` custom property), triangle area by direction, open edges, optional symmetry error | `blender -b --factory-startup kit.blend -P scripts/blender/check_asset.py --` |
| `silhouette_sheet.py` | Four-view black silhouettes at game pixel size, optional roster strip | `blender -b --factory-startup kit.blend -P scripts/blender/silhouette_sheet.py -- --out build/silhouettes --roster` |
| `modeling_helpers.py` | Import in a Blender console or MCP call: `make_col(obj)` builds a convex `<obj>_COL` proxy, `palette_uv(obj, swatches)` snaps faces to palette cells and collapses to one material, plus `tri_count`, `spend_report`, `symmetry_error` | `import modeling_helpers as mh` after adding the folder to `sys.path` |

What `export_kit.py` enforces and why:
- Names limited to `A-Z a-z 0-9 _`; rotation 0 and scale 1 (or `--apply-transforms`); exactly one UV map and at most one material per visual mesh; ≤ 20,000 triangles after modifiers; `_COL` children without material and ≤ 200 triangles; a collision plan on every asset (`_COL` child or `Fidelity` = `Box`/`Hull`). Any failure skips that asset and exits 1.
- Mesh datablocks are renamed `<Object>_Mesh` in memory so Reimport has stable names; a Triangulate modifier is appended if missing; the root moves to the world origin so the Blender origin becomes the pivot.
- Export options: `export_apply=True` (the default drops bevels and weighted normals), `export_yup=True`, no animation, `export_vertex_color="ACTIVE"` (the default writes a placeholder `COLOR_0` when the material does not use the colour).
- The same input gives byte-identical GLBs on one Blender version, so the manifest hash is a safe "unchanged" test. The exporter version is embedded in the file: pin Blender in the repo, and re-check `bpy.ops.export_scene.gltf` options on upgrade.

Tested on 2026-11-10 with the standalone `bpy` 5.2.3 LTS module driving the scripts as `blender -b` does; the GLBs were re-read for names, triangle counts, sizes and `COLOR_0`. Not run with the desktop binary and not imported into Studio. Add `--python-exit-code 1` before `-P` so a script error fails CI.

- **AO to vertex colour**: add a `BYTE_COLOR` corner attribute, make it the active colour, set the render engine to Cycles (CPU works headless) and call `bpy.ops.object.bake(type="AO", target="VERTEX_COLORS")` with the object active (tested).
- **Geometry Nodes for kits**: use node groups to generate variants (fence runs, pipe bends, window arrays), then apply and export each variant as its own asset. The glTF exporter skips Geometry Nodes instances by default (`export_gn_mesh` is off) and Realize Instances can drop UVs `[community]`, so test one export. For layouts do not realise at all: export transforms and place package copies in Studio, which keeps instancing. `[{"asset": i.object.data.name.removesuffix("_Mesh"), "matrix": [list(r) for r in i.matrix_world]} for i in bpy.context.evaluated_depsgraph_get().object_instances if i.is_instance]` returns one row per instance (tested); convert axes with the exporter's mapping (X, Z, −Y) and confirm with one asymmetric asset.
- **Decimate** is for `_COL` sources, far backdrops and over-built agent output (`ratio = budget / triangles`), never a substitute for modelling to budget. The engine builds its own RenderFidelity levels.
- **Atlas baking**: bake several unique props onto one shared 1024² set (Cycles bake, selected to active or a joined copy) only when the palette and trim routes cannot carry the look.
- **FBX** (animations and the FBX-only update endpoint): Path Mode = Copy with Embed Textures, Apply Scalings = FBX Unit Scale, Add Leaf Bones off, Bake Animation off for static meshes.

## Upload routes `[VS]`

| Route | Use when | Notes |
|---|---|---|
| Open Cloud key (`POST https://apis.roblox.com/assets/v1/assets`) | CI and batch uploads | A Lune or Python script you write for the game repo (none is shipped; the `curl` call below is the whole request) reads `manifest.json`, skips unchanged hashes, polls `GET /assets/v1/operations/{id}`, writes ids. |
| Studio MCP `open_cloud_invoke` | Interactive agent sessions | No API key. Enable `asset:read` and `asset:write` for the game and approve the export folder; the client cannot copy files into an approved folder. Studio's built-in `rbx-import-asset` skill checks triangle limits, uploads, waits for moderation and fixes scale, rotation, textures and anchoring. |
| Official Roblox Blender add-on | Artist-driven iteration | OAuth login; uploads selected objects as packages; a re-upload publishes a new version of the same package (tracked in a `Roblox Package ID` custom property). |
| Studio Importer + Reimport | Manual imports, one-off fixes | Reimport (Alt+Shift+R) updates MeshParts and SurfaceAppearances in place by mesh path and name and keeps CollisionFidelity, RenderFidelity and other properties. Auto-Reimport (reimports when the source file changes) is a Studio beta since 2026-09-08 `[official: staff post]`. |

```bash
curl -s -X POST "https://apis.roblox.com/assets/v1/assets" -H "x-api-key: $ROBLOX_API_KEY" \
  -F 'request={"assetType":"Model","displayName":"SM_Street_Lamp_A","description":"Street lamp, kit v3","creationContext":{"creator":{"groupId":"1234567"},"expectedPrice":0}}' \
  -F 'fileContent=@build/street_kit/SM_Street_Lamp_A.glb;type=model/gltf-binary'
```

- The key needs the assets scope with Read and Write (OAuth `asset:read`, `asset:write`). Upload under the group that owns the game or the place may not load the asset. Never commit the key; scope it to one group and the assets API.
- Check `moderationResult.moderationState` before publishing a build that depends on the asset. Uploads are permanent assets of the owner; remove them in the Creator Dashboard.
- Conflict: the earlier rule "every GLB re-upload creates a new asset id" is true for raw `POST` uploads only. Package versions (Blender add-on, Studio publish) keep the package id, and Reimport keeps the instances and their properties but "does not version assets": every reimport uploads new meshes and textures with new asset ids, with mesh and image versioning announced as in progress `[official: staff post, 2026-09-08]`. So: reference kit pieces by package, let a script own `assets/asset-ids.json` (name → package id, MeshIds, file hash) and regenerate `Shared/Config/Assets.luau`; never hand-edit or hard-code MeshIds.
- Audio uploads have quotas and their own rules: `audio-sfx-music.md` §4.

## Studio 3D Importer preset (manual imports)

Name set to the asset name (a GLB otherwise arrives as a Model called `Scene` `[lihfolk]`); Import Only As Model on; Upload to Roblox off while iterating and on for the final import, so test passes do not litter the inventory `[lihfolk]`; Creator = the group that owns the game; Import as Package on for kit pieces and props; Add to Workspace on (it also grants the game permission to use a restricted asset); Insert Using Scene Position on for layouts, off for single assets; Set Pivot to Scene Origin on; Use Imported Pivot on; Anchored on for static assets; Scale Unit = Studs; World Forward/Up = Front/Top; Merge Meshes off; Make Double Sided off; Invert Negative Faces off; Ignore Vertex Colors off. Save it as an import preset and apply it to the whole import queue. The importer de-duplicates only within a session (known asset cache): import each kit piece once, then place package copies.

## Post-import fix-up (edit time, via Studio MCP `execute_luau` or the command bar)

```lua
--!strict
-- unexecuted sketch. `fidelity` comes from manifest.json ("Box" or "Hull"); nil when the asset ships a _COL child.
local function isCol(d: Instance): boolean
	local parent = d.Parent -- under glTF the node is a Model and the MeshPart carries the mesh name, so test both
	return d.Name:find("_COL", 1, true) ~= nil or (parent ~= nil and parent.Name:find("_COL", 1, true) ~= nil)
end

local function fixup(model: Model, fidelity: string?)
	local hasCol = false
	for _, d in model:GetDescendants() do
		if d:IsA("MeshPart") and isCol(d) then hasCol = true break end
	end
	for _, d in model:GetDescendants() do
		if d:IsA("MeshPart") then
			d.Anchored = true
			d.CanTouch = false
			if isCol(d) then
				d.Transparency = 1
				d.CanCollide, d.CanQuery, d.CastShadow = true, true, false
				d.CollisionFidelity = Enum.CollisionFidelity.Hull
			elseif hasCol then
				d.CanCollide = false
				d.CollisionFidelity = Enum.CollisionFidelity.Box
			else
				d.CanCollide = true
				d.CollisionFidelity = if fidelity == "Box" then Enum.CollisionFidelity.Box else Enum.CollisionFidelity.Hull
			end
			if d.Size.Magnitude < 3 then d.CastShadow = false end
		end
	end
end
```

`CollisionFidelity` is not settable from a running game script; this runs at edit time only. Confirm the `_COL` naming once on a test import `[VS]`.

## Import traps and failure modes

Each row was hit in practice by this file's tests or by the LihFolk vault's Blender 5.2 builds `[lihfolk]`; all are `[VS]`.

| Symptom | Cause | Fix |
|---|---|---|
| Bevels, mirrors or weighted normals missing in Studio | glTF `export_apply` defaults to off (confirmed on 5.2.3) | Always pass `export_apply=True`; compare evaluated and base triangle counts |
| Asset 100 times too big from FBX | FBX written with scale option None `[lihfolk]` | Apply Scalings = FBX Unit Scale (`apply_scale_options="FBX_SCALE_UNITS"`), or use GLB. Never repair units by scaling in Studio: texel density and pivots stay wrong |
| Vertex-coloured mesh looks dark or tinted | Vertex colour multiplies `MeshPart.Color` `[lihfolk]` | Set `Color` to white on import |
| Mesh is plain grey although it was painted | Exporter left the attribute out | `export_vertex_color="ACTIVE"`; check for `COLOR_0` in the GLB |
| Patchy streaks no `Color` or `Material` change removes | A stray or noisy colour attribute; Blender 5.2 writes extra colour layers (seen as `COLOR_1` in the test) | Keep exactly one colour attribute, or tick Ignore Vertex Colors |
| N-gon failures after bevelling fan caps | Bevel turns pole fans into n-gons `[lihfolk]` | Triangulate modifier after the bevel |
| Rotated or offset pivot after an add-on upload | A leftover `PivotOffset` `[lihfolk]` | Reset `PivotOffset = CFrame.new()` per part. With a `PrimaryPart`, set its `PivotOffset`: `WorldPivot` is ignored then `[official]` |
| Mirrored copy needed | A CFrame cannot hold a reflection, so `PivotTo` never mirrors | Mirror in Blender and export it as its own piece |
| Names changed on upload, installer cannot find parts | Dots or spaces in object names `[lihfolk]` | `[A-Za-z0-9_]` only; the export script rejects anything else |
| Roughness or metalness ignored | Packed ORM or ARM texture | Separate 8-bit greyscale maps `[official]`; bake AO into the colour map or vertex colour |
| AO bake comes out black | Other objects occlude the target `[lihfolk]` | Hide everything else from render before baking |
| Lantern glows in Blender, is dark in game | Blender emission lights nothing in Roblox | PointLight on a `Light_Att`; emissive mask or Neon for the glow itself |
| Headless script fails with a poll or context error | Operator needs a UI area under `-b` (for example `uv.sphere_project`) `[lihfolk]` | Use `bmesh.ops` and data APIs; compute UVs from positions |
| Rebuilt kit differs from last week's | Unseeded or shared random stream | Seed per asset (hash of its name) |
| Long batch runs out of memory | Orphan meshes, materials and images pile up | One Blender process per asset, or purge orphans between assets |
| Preview renders fail on CI | Eevee and Workbench need a GPU | Cycles on CPU for automated previews |
| Artist's open scene wiped | `read_factory_settings` sent over the live MCP connection `[lihfolk]` | Never reset or delete through the bridge; build headless and append |

Conflicts with LihFolk guidance, house position in each case:
- Conflict (collision default): LihFolk switches `CanCollide`, `CanTouch` and `CanQuery` off on anything it calls decoration and prefers non-colliding visuals with invisible Part colliders. House rule 2 is the reverse default: every visible world mesh is solid unless it carries the `NonSolid` tag for the narrow cases in performance.md (foliage canopies, cables; held tools, viewmodels and transient effect meshes never collide). Invisible collider helpers are fine in both. Trust the house rule; it exists so nothing is walk-through.
- Conflict (blockout): LihFolk blocks out with grey Parts in the working place. Here Part blockouts live only in a throwaway place; the shipping place gets the Blender blockout kit.
- LOD (resolved at source): the staff announcement of 2026-04-27 confirms LihFolk's report. Mesh Streaming and Improved Cloud LoDs is opt-in through `Workspace.MeshStreamingAndImprovedLods`; when enabled, `RenderFidelity` is ignored; the stated plan is opt-out by default (first targeted for July 2026; no notice of that phase was found by 2026-11-11), then removal of both properties. The docs still describe `RenderFidelity` and do not mention the new property, and bug reports describe meshes stuck at a low LOD or stuttering on moving assemblies with it enabled `[community]`. Practice either way: never hand-author LOD chains, build one mesh whose silhouette survives simplification, check hero pieces at 250 and 500 studs with the property both ways, and do not build systems on `RenderFidelity`.
- Units: LihFolk uses Unit System Metric with Unit Scale 1, this file uses None; both end at 1 unit = 1 stud.

## Modular kits, instancing and when to merge

Keep the kit small and versatile (Beyond the Dark placed over 1,000 instances of a few wall panels). Each piece is a package with AutoUpdate on. Snap on the kit grid, rotate in 90° steps, hide seams with trims (cornices, corner posts, skirting), and prefer variant SurfaceAppearances over new meshes.

Instancing rule `[official]`: MeshParts share a draw call only when they have the same MeshContent and identical SurfaceAppearances (or identical TextureContent, or identical materials when neither exists). Importing a whole map at once gives identical meshes separate ids. `MeshPart.Color` is reported not to break instancing `[community]`; measure in your build.

| Situation | Do |
|---|---|
| Repeated piece (walls, lamps, trees, fences) | Keep modular: one upload, package copies |
| Many small one-off meshes that always sit together (a stall's clutter) | Merge in Blender into one mesh per material, ≤ 20k triangles, after layout is final |
| Part that moves, animates or is interacted with on its own | Keep as a separate named child |
| Prop with several materials | Collapse to one (palette or trim) or split deliberately; never ship accidental slots |
| Merged mesh larger than about 64 studs | Split: big meshes defeat culling, streaming and SLIM |
| Skyline, mountains, unreachable backdrop | One dedicated low-poly backdrop mesh |

## Style bible and lighting (pointers)

- **Style bible**: the one-page template, the measurable form of each line, the tie-ins to UI, VFX, audio and writing, and the generic-look tells and anti-patterns are in `references/art-direction-and-quality-bar.md` (§6 and §2). This file needs four of its lines filled in before export: grid and pivots, texturing method, texel density and bevel widths.
- **Lighting**: `references/lighting-and-atmosphere.md` owns `LightingStyle`, property ranges (§6), presets (§12), the official curriculum sample values (§5) and the low-end tests (§11). What the pipeline contributes: every fixture model carries a `Light_Att` marker just outside its shade, lights are added with `Shadows = false` by default, interior shells are at least 1 stud thick and sealed, vertex-colour AO is baked for the levels where shadows are off, and every asset is reviewed under the game's preset, never under default lighting.

## Asset acceptance checklist (per asset, pass or fail)

- [ ] Named to convention; root at origin; pivot where the asset attaches; rotation 0, scale 1.
- [ ] Triangles within class budget after modifiers; no n-gons; normals out; bevels and weighted normals to the bible standard.
- [ ] One material, one UV set in 0–1; texturing method and texel density match the bible; no new texture unless the bible allows it.
- [ ] Colours only from the palette; vertex colour present if the kit uses it (`COLOR_0` in the GLB).
- [ ] Collision plan explicit: `Fidelity` property or `_COL` child; walk and jump on it in Studio with collision visualisation on.
- [ ] `_Att` points present for every light, prompt, seat and VFX socket the design calls for.
- [ ] `scripts/blender/export_kit.py` (or `check_asset.py`) exits 0; manifest row written; upload operation `Approved`; uploaded under the owning group.
- [ ] Wrapped as a package; placed copies share one MeshId; no duplicate upload of the same piece.
- [ ] Held next to the golden sample under final lighting, at graphics level 1–3 and on a phone: reads by silhouette, nothing glows that should not, no z-fighting, no light leaks.
- [ ] CastShadow off if small; RenderFidelity Automatic (Performance for clutter); streaming mode set (Atomic for interactive props).

## Level-up: art symptoms → cause → fix

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| Mismatched styles (flat props beside PBR props, sharp beside blurry) | Assets from several sources, no bible, mixed texel density | Ordered rescue passes in `art-direction-and-quality-bar.md` §10; pipeline part: re-texture onto the palette or trim library, replace marketplace models with kit pieces |
| Primitive leftovers (visible Parts, unions, greybox) | Blockout never replaced | Run the house-rule scan in checklists.md, sort by count, model the top offenders as kit pieces first; invisible helpers may stay |
| Walk-through props, or invisible walls around props | `CanCollide` off on imports, missing `_COL`, Box fidelity on a concave shape | Collision scan; add `Fidelity` or `_COL`; doorway = three boxes; walk test with collision visualisation |
| Heavy draw calls in one view | Duplicate MeshIds from whole-map imports, a texture per prop, multi-material meshes, many decals | Duplicate-MeshId audit (performance.md); re-point copies to one package; shared `_SA`; merge unique clutter; replace decals with trim or palette detail |
| Texture memory high, blurry textures on phones | Unique 1024² sets per prop | Move props to the palette atlas or trim library; cap unique bakes; ≤ 512² default |
| Looks flat or "plastic" | No bevels, no AO, default lighting | Bevel and weighted-normal pass; vertex-colour AO; a preset from `lighting-and-atmosphere.md` §12 |
| Dark, inside-out or faceted shading | Flipped normals, unapplied Mirror or scale, modifiers not applied at export | Recalculate normals, apply transforms, export with `export_apply=True` |
| Doors, stairs or furniture feel the wrong size | Modelled in metres or without the R15 dummy | Rescale against the dummy; lock the grid and proportions in the bible |
| Characters snag, hover or stutter on stairs and trims | Default or Precise fidelity on detailed meshes, per-step collision | `_COL` ramp and simple hulls; Box on trims; reserve Precise for approved cases |
| Meshes missing or failing to load for players | Asset still in moderation, uploaded under the wrong creator, Restricted asset not granted to the game | Check the operation's moderation state; upload under the owning group; grant the game in the asset's permissions |
| Every art tweak breaks references | Raw re-uploads mint new ids | Package versioning (Blender add-on or Reimport) and the generated ids manifest |
| Attachments missing after import (no light, prompt or seat points) | `_Att` markers not converted | Check the test import; one-triangle `_Att` mesh markers or Attachments added by the fix-up script |
| Distant meshes look crushed or pop | Automatic LOD on a mesh whose silhouette does not survive simplification; mesh streaming enabled | Thicken thin parts; compare with `MeshStreamingAndImprovedLods` both ways; Precise only on approved hero pieces |

## Review gate

- [ ] Style bible (`art-direction-and-quality-bar.md` §6) filled in and versioned; a golden sample exists in Studio; every asset passed the acceptance checklist.
- [ ] Every mesh came from the Blender pipeline; the manifest maps every asset name to an id; no marketplace or free models; no visible primitive Parts; Terrain only with the owner's explicit per-game approval.
- [ ] Each kit piece uploaded once and placed as a package; duplicate-MeshId audit clean.
- [ ] Triangle budgets met; ≤ 20k per mesh; one material and one UV set per mesh.
- [ ] Textures ≤ 1024², mostly ≤ 512², from the shared palette or trim library; `_SA` SurfaceAppearances shared.
- [ ] Every visible world object collides (fidelity or `_COL`; skinned meshes through a `_COL` proxy; `NonSolid` only on canopies, cables, held tools, viewmodels and transient effect meshes); house-rule scan in checklists.md passes; walk-through test passes.
- [ ] RenderFidelity Automatic (Performance for clutter); hero pieces checked at 250 and 500 studs; SLIM on large static models where available.
- [ ] One test import confirmed pivots, names, `_COL` handling and that every `_Att` marker arrived as an Attachment.
- [ ] All uploaded assets `Approved` and owned by the game's group before the build is published.
- [ ] Assets reviewed under the game's lighting preset (`lighting-and-atmosphere.md`); no interior light leaks; CastShadow off on small, moving and invisible parts.

Grep `references/knowledge-base.md` for `## 5.7`, `## 5.8` and `### 4.10.4`. Tool and skill options for this pipeline: `references/ai-toolchain-skills.md`.

## Sources

Accessed 2026-11-10; platform facts re-checked and DevForum posts read on 2026-11-11.

- https://github.com/Roblox/creator-docs (read; re-checked at commit 7cbffff of 2026-11-10), under `content/en-us/`: `art/modeling/specifications.md`, `art/modeling/texture-specifications.md`, `art/modeling/export-requirements.md`, `art/modeling/reimport.md`, `art/modeling/roblox-blender-plugin.md`, `art/modeling/index.md`, `art/blender.md`, `studio/importer.md`, `studio/mcp-open-cloud.md`, `parts/meshes.md`, `parts/textures-decals.md`, `avatar/character-bodies/specifications.md` (the `_Att` conversion note), `cloud/guides/usage-assets.md`, `cloud/reference/rate-limits.md`, `reference/cloud/assets/v1.json`, `projects/assets/index.md`, `projects/assets/privacy.md`, `performance-optimization/{improve,design}.md`, `workspace/streaming/{slim,techniques}.md`, `reference/engine/classes/{MeshPart,TriangleMeshPart,SurfaceAppearance}.yaml`, `reference/engine/enums/{CollisionFidelity,RenderFidelity,AlphaMode}.yaml`
- Roblox staff posts on the DevForum (read): 4K texture rendering, 2026-01-30, https://devforum.roblox.com/t/4k-texture-rendering/4316229 · texture streaming and its platform and instance support list, 2025-12-12 with updates to 2026-03-23, https://devforum.roblox.com/t/introducing-texture-streaming/4144855 · staff reply on 4K below 3.5 GB of memory, 2026-07-10, https://devforum.roblox.com/t/4526736 · Mesh Streaming and Improved Cloud LoDs, 2026-04-27, https://devforum.roblox.com/t/4601232 · Reimport full release, 2026-05-06, https://devforum.roblox.com/t/full-release-reimport/4622567 · Auto-Reimport beta, 2026-09-08, https://devforum.roblox.com/t/studio-beta-auto-reimport-automatically-reimport-external-files-on-changes/4859863 · draw distance and quality levels, 2026-11-05, https://devforum.roblox.com/t/4977292
- Engine API dump, version 0.747 (https://github.com/MaximumADHD/Roblox-Client-Tracker, read 2026-11-11): `Workspace.MeshStreamingAndImprovedLods` exists (not scriptable); enum items and SurfaceAppearance members as named above
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-asset-import/SKILL.md`, `skills/roblox-blender-modeling/SKILL.md` and `references/quality-research.md`, `Skill - Roblox Asset Import.md`, `14 3D Modeling/Exporting and Validating Models for Roblox.md`, `14 3D Modeling/Mesh Gates for Generated Models - Symmetry, Seating and Caps.md`, `17 Pipelines/Art Pipeline - Concept to In-Game Asset.md`, `45 Procedural Blender Assets/Blender 5 Python Gotchas for Headless Builds.md`, `54 Untextured Stylised Modelling/Flat Colour vs Gradient Atlas vs Vertex Colour.md` (read)
- https://github.com/Roblox/roblox-blender-plugin (read: README, package versioning)
- https://github.com/jackTabsCode/asphalt (read: README note that the web API exposes no import settings)
- Blender 5.2.3 LTS `bpy` wheel from PyPI (ran the scripts above; read `export_scene.gltf` option defaults)
- Community threads (read): https://devforum.roblox.com/t/does-roblox-use-mesh-instancing/399564 (2019 answer that `MeshPart.Color` does not affect instancing) · https://devforum.roblox.com/t/1893887 (2022: empties dropped by the FBX importer) · https://devforum.roblox.com/t/4933005 (2026-10: UI images above 1024² downscaled) · https://devforum.roblox.com/t/meshstreamingandimprovedlods-persistently-stuck-at-lowest-lod-level-for-all-meshes/4835534 and https://devforum.roblox.com/t/4742906 (bug reports with mesh streaming enabled; titles and opening posts)
- Search summaries only, not re-read: https://devforum.roblox.com/t/surface-appearance-loads-inconsistently-on-mobile-and-often-displays-at-very-low-quality-even-if-the-phone-allows-it/4530853 · https://projects.blender.org/blender/blender-addons/issues/96517 and https://blenderartists.org/t/geo-nodes-instances-to-real-instances/1409710 (Geometry Nodes instances and UVs on export)
- Not verified: nothing here was imported into Studio. Open questions to settle on the first test import: whether `_Att` empties become Attachments, which glTF name lands on the MeshPart, and the `_COL` naming under the glTF node hierarchy. No 2026 triangle-limit increase was found.
