# Blender-to-Roblox art pipeline and lighting

The house art pipeline: style bible, Blender authoring, headless GLB export, upload, Studio fix-up, lighting. Open it before modelling anything, when writing export or import tooling, and when auditing a live game's look, collisions or draw calls (jump to "Level-up"). House rules 1 and 2: every visible object is a Blender model, nothing visible is a primitive Part or a marketplace asset, and everything visible is solid. Distilled from knowledge-base 5.7, 5.8 and 4.10.4, re-verified against `Roblox/creator-docs` (commit of 2026-11-07). Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

## Pipeline overview

1. **Style bible and kit plan first**: fill in the one-page template below before the first mesh.
2. **Author in Blender through the Blender Lab MCP bridge** (`tools/blender_exec.py` in the game repo sends Python to the running Blender). Use it for modelling, validation and layout, never for export.
3. **Validate in Blender**: `check()` from the export script (transforms, UVs, one material, budgets, collision plan).
4. **Export GLB in a separate headless process**: `blender -b --factory-startup assets/blender/<kit>.blend -P tools/export_kit.py -- build/<kit>`. Never export from the MCP-driven session.
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
| Texture size | Up to 4096² is supported; texture streaming (automatic) loads a baseline first and raises quality to the device's memory budget. Doc guidance: 256² per 5×5 studs, 512² per 10×10, 1024² per 20×20. |
| Texture formats | png, jpg, tga, bmp. Open Cloud images must be under 8000×8000. Albedo and normal 24-bit RGB (normal: OpenGL tangent space); roughness, metalness, emissive mask 8-bit grey. |
| Import formats | `.fbx`, `.gltf`/`.glb`, `.obj`. FBX and glTF carry hierarchies, PBR textures, cages, rigs, animation data and vertex colours. Asset Manager bulk import does not take rigs, skins or animation. |
| glTF hierarchy | Each node becomes a Model holding one MeshPart per primitive of its mesh (FBX: MeshParts sit directly in the top Model). If a node and its mesh share a name, one of them gets `_Node`. |
| Naming hooks | `_Att` → Attachment; `_OuterCage` → WrapTarget; `_InnerCage` + `_OuterCage` → WrapLayer. No collision-mesh naming hook exists. |
| Skinned meshes | Bones scale 1, rotation 0; root at origin; ≤ 4 influences per vertex; none on the root; one animation track per FBX. |
| `RenderFidelity` | Automatic: full detail under 250 studs, medium 250–500, lowest beyond 500. Performance and Precise are the manual options. No import path for hand-made LOD chains. |
| `CollisionFidelity` | Box, Hull, Default, PreciseConvexDecomposition, Tunable (adds `CollisionPrecision`). Collision data is stored even with `CanCollide = false`. |
| Open Cloud upload | One asset per call, ≤ 20 MB. Model accepts `model/fbx`, `model/gltf+json`, `model/gltf-binary`, arrives as a package of MeshParts. Create Asset is marked beta. Content update (PATCH) works for `.fbx` only. |
| Rate limits | No per-endpoint number is published for the Assets API in the mirrored spec; undocumented limits may apply and are counted per key owner. Read `x-ratelimit-*` headers and back off on HTTP 429. |
| Upload cost | No fee is documented for model or image uploads in the pages read. Audio and video have quotas. Send `creationContext.expectedPrice: 0` so an unexpected fee fails the call. |
| Moderation | Human and automated; "generally within a few hours". An asset still in the queue is invisible to players in a published game. Operation states: `Reviewing`, `Approved`, `Rejected`. |
| Asset privacy | Images, Decals and Meshes are Open Use by default; with Asset Privacy enabled they are created Restricted and each game needs a grant. Open Use cannot be undone; game grants are permanent. |
| Misc | Light `Range` is clamped to 120 studs. Shadows switch off below graphics quality level 4. SLIM needs streaming, a published place and Team Create, and static models without a Humanoid. |

Conflict: the texture spec page says both "supports up to 4096×4096" and, under UV mapping, "supports up to 1024×1024 pixel spaces". House cap stays 1024², mostly ≤ 512², because the target is a 3 GB phone and a mobile bug report describes SurfaceAppearance maps stuck at low mips `[community]`. Community guides that quote 10,000 or 21,000 triangles are wrong or stale.

## Units, scale, orientation, transforms

- 1 stud = 0.28 m (1 m ≈ 3.57 studs). Gravity 196.2 studs/s².
- Convention: **1 Blender unit = 1 stud** (Studio importer Scale Unit = Stud). Blender Scene > Units > Unit System = None (or Metric with Unit Scale 1), Rotation = Degrees. Do not mix with metric-scale assets (importer Scale Unit = Meter multiplies by about 3.57). The web API exposes no import settings `[community]`, so the file itself must already be in studs.
- Keep an R15 dummy exported from Studio in a hidden Blender collection; Roblox avatars are chunky, so size doors, counters, steps and seats against it.
- Orientation: glTF exports +Y up; model assets facing −Y in Blender; Studio importer World Forward = Front, World Up = Top; confirm once with an asset that has an obvious front.
- Apply all transforms (rotation 0, scale 1) and modifiers before export. Unapplied scale, an unapplied Mirror modifier and flipped normals are the usual causes of inside-out or dark shading after import `[community]`.

## Grid and pivots

- One grid per project, written in the style bible: 5-stud grid (environmental-art curriculum), 16-stud for large architecture (Beyond the Dark), 4- or 8-stud sub-grid for props in town games.
- Modular kit pivots at the front-lower corner so pieces snap edge to edge in 90° steps. Prop pivots where the prop attaches: bottom-centre for floor props, back-centre for wall props, top-centre for hanging props.
- The export script moves each asset's origin to world (0,0,0) so Use Imported Pivot, Set Pivot to Scene Origin and Insert Using Scene Position agree.

## Mesh specifications and budgets

One material per mesh (each extra slot becomes another MeshPart, draw call and collision shape); consistent normals; Make Double Sided only for foliage cards.

| Asset class | Triangles |
|---|---|
| Clutter (hand-sized) | 50–300 |
| Small prop (bins, signs, chairs) | 200–1,500 |
| Medium prop (street lamps, vending machines) | 1,500–5,000 |
| Vehicle | 5,000–15,000, split into ≤ 4 meshes |
| Modular building piece | 200–3,000 |
| Hero landmark | up to 20,000 per mesh, several meshes |
| NPC character | 4,000–10,000 |
| Collision proxy `_COL` | 12–200 |

Spend triangles on silhouette and edge bevels. A 0.05–0.15 stud chamfer with weighted normals is the single biggest cure for the "cheap AI asset" look. Count triangles after modifiers; the bevel is part of the budget.

## Texturing strategy

| Method | Use for | Cost | Rule |
|---|---|---|---|
| Palette atlas ("palette UV") | Flat-colour stylised props, vehicles, NPCs | One 256² ColorMap for the whole game | UV islands collapsed onto swatch cells; no normal or roughness maps |
| Trim sheets | Architecture and hard surface that needs PBR detail | 4–8 sets at ≤ 1024² | Follow Active Quads onto the bands; no recognisable stains |
| Tileable MaterialVariant | Ground, long walls | Engine-shared | Set as Override, Organic tiling |
| Unique bake | Hero landmark, hero NPC | ≤ 1024² each | Cap the count in the style bible |
| Vertex colour | Baked AO, height gradients, tint variation | No texture memory | Export with `export_vertex_color="ACTIVE"` |

Pick one primary method per game and write it in the style bible; mixing a flat palette kit with PBR trim props is the most common cohesion failure `[house]`.

Palette atlas method:
1. Paint one atlas: a 16×16 grid of flat swatches from the style-bible palette, plus a few vertical gradient strips. Cells ≥ 16 px.
2. Every mesh uses the single material `M_Palette`. Run `palette_uv()` (below) to snap each face to its swatch centre. For a gradient, keep U on the strip and map V to height.
3. In Studio every MeshPart shares one `Palette_SA` (ColorMap only) or one `TextureID`. `SurfaceAppearance.ResampleMode = Pixelated` stops neighbouring swatches blurring together `[official, VS]`. Keep UVs ≥ 2 px inside a cell and never rely on sub-cell detail: phones may show a lower mip `[community]`.
4. Form comes from bevels, vertex-colour AO and lighting, not from the texture.
5. A re-skin (season, event, night palette) is one texture swap. For per-instance tint, `SurfaceAppearance.Color` tints the ColorMap (author those swatches near-white), or leave swatch alpha at 0 under Overlay so `MeshPart.Color` shows through.
6. A shared texture cuts texture memory, not draw calls: instancing needs the same MeshId as well.

PBR details (trim and unique routes): ColorMap sRGB, near-white if tinted; NormalMap OpenGL tangent space, never DirectX; RoughnessMap +0.1 to offset Roblox's Fresnel; MetalnessMap 0 or 1; emissive through `EmissiveMaskContent`, `EmissiveStrength`, `EmissiveTint` `[VS]`. `AlphaMode`: Overlay (default), Transparency (cutout at part Transparency 0), TintMask, Opaque (beta `[VS]`). Most SurfaceAppearance properties cannot change at runtime, so variants are separate instances; on publish the engine bakes the maps into one texture pack. One SurfaceAppearance per material named `<Name>_SA`, published as a package material library; the post-import script swaps Blender placeholder materials (`M_Trim_Metal`) for the matching `_SA`. Texel density: about 50 px per stud for architecture, up to 100 px per stud for arm's-length props, constant across the kit.

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

Under glTF the mesh datablock name reaches Studio as well as the object name (hence the `_Node` rule), and Reimport matches on mesh path and name. Blender's defaults (`Cube.014`) are neither unique nor stable, so the export script renames every datablock to `<Object>_Mesh`; which name lands on the MeshPart is not documented, so check one test import `[VS]`. Split multi-part assets into named children (`Door`, `Frame`, `Handle_Att`) so moving parts can animate and each piece gets the right collision. `_Att` empties are the hand-off between art and code: scripts find attachments by name instead of hard-coding offsets.

## Collision authoring

- Decide per asset: fidelity on the visual mesh (custom property `Fidelity` = `Box` or `Hull` on the root) or a `_COL` child. The export script refuses an asset with neither.
- `_COL` proxies are convex (or a few convex pieces), have no material, 12–200 triangles, sit flush on walkable surfaces. Doorways use three boxes (two jambs and a lintel); stairs use a single ramp. `make_col()` builds a hull for convex props; concave assets need hand-made pieces.
- Tunable fidelity with `CollisionPrecision` is the newer middle ground for one-off concave shapes `[VS]`; view the result with Visualization Options > Collision fidelity.
- Flags after import are in performance.md ("Making everything solid").

## Blender automation

Tested on Blender 5.2.3 LTS (standalone `bpy`, headless, 2026-11-10): exported, re-read the GLB, checked names, triangle counts and `COLOR_0`. Not run through a Studio import. Pin the Blender version in the repo and re-check `bpy.ops.export_scene.gltf` options on upgrade. Add `--python-exit-code 1` so a script error fails CI.

```python
# tools/export_kit.py: validate, then export every root (or --only names) to its own GLB at the origin.
# blender -b --factory-startup assets/blender/street_kit.blend -P tools/export_kit.py -- build/street_kit [--only SM_Street_Lamp_A]
import bpy, hashlib, json, sys
from pathlib import Path

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir = Path(argv[0]); out_dir.mkdir(parents=True, exist_ok=True)
only = set(argv[argv.index("--only") + 1:]) if "--only" in argv else None
MAX_TRIS, PREFIXES = 20000, ("SM_", "KIT_", "SK_")

def tri_count(obj):  # counted after modifiers (bevels), which is what ships
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh(); n = sum(len(p.vertices) - 2 for p in me.polygons); ev.to_mesh_clear()
    return n

def check(root):
    family = [o for o in (root, *root.children_recursive) if o.type == "MESH"]
    bad = []
    for o in family:
        col = o.name.endswith("_COL")
        o.data.name = o.name + "_Mesh"   # glTF mesh name becomes the MeshPart name; keep it unique and stable for Reimport
        if any(abs(s - 1) > 1e-4 for s in o.scale) or any(abs(r) > 1e-4 for r in o.rotation_euler):
            bad.append(f"{o.name}: unapplied rotation/scale")
        if not col and len(o.data.uv_layers) != 1: bad.append(f"{o.name}: {len(o.data.uv_layers)} UV maps (need 1)")
        if len([s for s in o.material_slots if s.material]) > (0 if col else 1): bad.append(f"{o.name}: material slots")
        if tri_count(o) > (200 if col else MAX_TRIS): bad.append(f"{o.name}: {tri_count(o)} tris over budget")
    if not any(o.name.endswith("_COL") for o in family) and "Fidelity" not in root:
        bad.append(f"{root.name}: no _COL child and no 'Fidelity' custom property (Box/Hull)")
    return family, bad

manifest, failed = {}, []
for root in [o for o in bpy.data.objects if o.parent is None and o.name.startswith(PREFIXES)]:
    if only and root.name not in only: continue
    family, bad = check(root)
    if bad: failed += bad; continue
    saved = root.matrix_world.copy(); root.location = (0, 0, 0)   # pivot = Blender origin at world zero
    bpy.ops.object.select_all(action="DESELECT")
    for o in (root, *root.children_recursive): o.hide_set(False); o.select_set(True)
    path = out_dir / f"{root.name}.glb"
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", use_selection=True,
        export_apply=True, export_yup=True, export_animations=False,
        export_vertex_color="ACTIVE", export_all_vertex_colors=False)  # default MATERIAL writes a fake COLOR_0
    root.matrix_world = saved
    manifest[root.name] = {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "tris": {o.name: tri_count(o) for o in family}, "fidelity": root.get("Fidelity")}
(out_dir / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True))
print("\n".join(failed) or f"OK {len(manifest)} assets")
sys.exit(1 if failed else 0)
```

Helpers to run through the MCP bridge (same test run):

```python
import bpy, bmesh

def make_col(obj, angle=0.09):
    """Convex-hull proxy named <obj>_COL, parented to obj, no materials. Studio side: CollisionFidelity = Hull."""
    bm = bmesh.new(); bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    bmesh.ops.delete(bm, geom=bm.faces[:], context="FACES_ONLY")
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bmesh.ops.dissolve_limit(bm, angle_limit=angle, verts=bm.verts[:], edges=bm.edges[:])  # merge near-coplanar faces
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(obj.name + "_COL"); bm.to_mesh(me); bm.free()
    col = bpy.data.objects.new(obj.name + "_COL", me); obj.users_collection[0].objects.link(col)
    col.parent = obj; col.display_type = "WIRE"
    return col

def palette_uv(obj, swatch, grid=16, material="M_Palette"):
    """swatch = {"M_Red": (col, row)}, cells counted from the atlas top-left. Collapses the mesh to one material."""
    uv = obj.data.uv_layers.active.data
    for poly in obj.data.polygons:
        c, r = swatch[obj.material_slots[poly.material_index].material.name]
        for li in poly.loop_indices: uv[li].uv = ((c + 0.5) / grid, 1 - (r + 0.5) / grid)
        poly.material_index = 0
    obj.data.materials.clear(); obj.data.materials.append(bpy.data.materials[material])
```

- **AO to vertex colour**: add a `BYTE_COLOR` corner attribute, make it the active colour, set the render engine to Cycles (CPU works headless) and call `bpy.ops.object.bake(type="AO", target="VERTEX_COLORS")` with the object active (tested).
- **Geometry Nodes for kits**: use node groups to generate variants (fence runs, pipe bends, window arrays), then apply and export each variant as its own asset. The glTF exporter skips Geometry Nodes instances by default (`export_gn_mesh` is off) and Realize Instances can drop UVs `[community]`, so test one export. For layouts do not realise at all: export transforms and place package copies in Studio, which keeps instancing. `[{"asset": i.object.data.name.removesuffix("_Mesh"), "matrix": [list(r) for r in i.matrix_world]} for i in bpy.context.evaluated_depsgraph_get().object_instances if i.is_instance]` returns one row per instance (tested); convert axes with the exporter's mapping (X, Z, −Y) and confirm with one asymmetric asset.
- **Decimate** is for `_COL` sources, far backdrops and over-built agent output (`ratio = budget / triangles`), never a substitute for modelling to budget. The engine builds its own RenderFidelity levels.
- **Atlas baking**: bake several unique props onto one shared 1024² set (Cycles bake, selected to active or a joined copy) only when the palette and trim routes cannot carry the look.
- **FBX** (animations and the FBX-only update endpoint): Path Mode = Copy with Embed Textures, Apply Scalings = FBX Unit Scale, Add Leaf Bones off, Bake Animation off for static meshes.

## Upload routes `[VS]`

| Route | Use when | Notes |
|---|---|---|
| Open Cloud key (`POST https://apis.roblox.com/assets/v1/assets`) | CI and batch uploads | A Lune or Python script reads `manifest.json`, skips unchanged hashes, polls `GET /assets/v1/operations/{id}`, writes ids. |
| Studio MCP `open_cloud_invoke` | Interactive agent sessions | No API key. Enable `asset:read` and `asset:write` for the game and approve the export folder; the client cannot copy files into an approved folder. Studio's built-in `rbx-import-asset` skill checks triangle limits, uploads, waits for moderation and fixes scale, rotation, textures and anchoring. |
| Official Roblox Blender add-on | Artist-driven iteration | OAuth login; uploads selected objects as packages; a re-upload publishes a new version of the same package (tracked in a `Roblox Package ID` custom property). |
| Studio Importer + Reimport | Manual imports, one-off fixes | Reimport (Alt+Shift+R) updates MeshParts and SurfaceAppearances in place by mesh path and name and keeps CollisionFidelity, RenderFidelity and other properties. Auto-Reimport is a Studio beta `[community]`. |

```bash
curl -s -X POST "https://apis.roblox.com/assets/v1/assets" -H "x-api-key: $ROBLOX_API_KEY" \
  -F 'request={"assetType":"Model","displayName":"SM_Street_Lamp_A","description":"Street lamp, kit v3","creationContext":{"creator":{"groupId":"1234567"},"expectedPrice":0}}' \
  -F 'fileContent=@build/street_kit/SM_Street_Lamp_A.glb;type=model/gltf-binary'
```

- The key needs the assets scope with Read and Write (OAuth `asset:read`, `asset:write`). Upload under the group that owns the game or the place may not load the asset. Never commit the key; scope it to one group and the assets API.
- Check `moderationResult.moderationState` before publishing a build that depends on the asset. Uploads are permanent assets of the owner; remove them in the Creator Dashboard.
- Conflict: the earlier rule "every GLB re-upload creates a new asset id" is true for raw `POST` uploads only. Package versions (Blender add-on, Studio publish) keep the package id, and Reimport keeps the instances, although a DevForum beta post reports new mesh and texture ids on each reimport with asset versioning still in progress `[community]`. So: reference kit pieces by package, let a script own `assets/asset-ids.json` (name → package id, MeshIds, file hash) and regenerate `Shared/Config/Assets.luau`; never hand-edit or hard-code MeshIds.
- Audio quota: 100 a month verified, 10 unverified on the Open Cloud page (the audio page says 2,000 / 100; plan around the stricter numbers).

## Studio 3D Importer preset (manual imports)

Import Only As Model on; Upload to Roblox on; Creator = the group that owns the game; Import as Package on for kit pieces and props; Add to Workspace on (it also grants the game permission to use a restricted asset); Insert Using Scene Position on for layouts, off for single assets; Set Pivot to Scene Origin on; Use Imported Pivot on; Anchored on for static assets; Scale Unit = Studs; World Forward/Up = Front/Top; Merge Meshes off; Make Double Sided off; Invert Negative Faces off; Ignore Vertex Colors off. Save it as an import preset and apply it to the whole import queue. The importer de-duplicates only within a session (known asset cache): import each kit piece once, then place package copies.

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
		if not d:IsA("MeshPart") then continue end
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
```

`CollisionFidelity` is not settable from a running game script; this runs at edit time only. Confirm the `_COL` naming once on a test import `[VS]`.

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

## Style bible in one page (template)

```markdown
# <Game> style bible v<N> (<date>, owner)
Fantasy in one line:            | Mood words (3):
Golden sample: <asset name>, the piece every new asset is held next to in Studio
Palette (hex): base 8–12 ...    | accents 2 ... (accents only on things players can use)
Value rule: ground mid-dark, walls mid, interactables brightest and most saturated
Shape language: chunky-rounded / crisp-bevelled; primary:secondary:detail = 60:30:10
Proportions vs R15 dummy: door __ studs, counter __, step rise __, handle thickness ≥ __
Bevel standard: props __ studs, architecture __ studs, weighted normals always
Grid: architecture __ studs, props __ studs; pivot rule per class
Texturing method: palette atlas / trim sheets / mixed (state which classes use which)
Texel density: __ px per stud; max texture __; unique bakes allowed: __ assets
Material response: roughness range per family; metalness 0 or 1; emissive only on __
Wear and story: edge wear yes/no; grime direction; what never gets dirty
Lighting preset: LightingStyle __, ClockTime __, Atmosphere D/O/H/G __, post effects __
Smallest readable detail: __ studs (anything smaller is deleted or enlarged)
Banned: unlisted colours, unbevelled boxes, baked text, one-off textures, neon as decoration
Sign-off: every asset passes the acceptance checklist under this lighting on a phone
```

Rules behind the template:
- Constraints applied everywhere beat detail. Write the bible from a finished golden sample, not from intentions.
- Community builders name the same tells for an amateur map: inconsistent art across the map, no contrast or focal point, flat ground and uniform heights, props scattered evenly instead of clustered, default lighting `[community]`. Consistency plus lighting and post-processing is the most cited fix `[community]`.
- Phone readability `[house]`: screenshot at 360 px wide and squint. Each interactable must read by silhouette; details under about 0.5 stud disappear at third-person distance; exaggerate handles, rails and frames for the chunky avatar; reserve the accent colours for things that can be used.
- Anti-patterns: mixed texel densities, noisy procedural textures, saturated rainbow palettes, everything glowing, unbevelled boxes, one-off textures per prop, marketplace-looking proportions, text baked into textures (use SurfaceGui or decals for localisable signage).

## Lighting `[VS]`

`Lighting.Technology` is superseded by `Lighting.LightingStyle` (Realistic or Soft; new places start on Soft) and `Lighting.PrioritizeLightingQuality` (true keeps shadows and shaders close up; false keeps view distance). Voxel, ShadowMap and Future remain in the old enum; Legacy, Compatibility and Unified are deprecated (Retro look: Voxel plus `ColorGradingEffect.TonemapperPreset = Retro`).

Decision rule: Realistic for interiors, local lights, PBR metals or a night mode (most Blender-art games); Soft for bright flat cartoon styles. `PrioritizeLightingQuality = true` for small dense worlds, false for large open maps.

Starting points: `Ambient` dark and slightly tinted, e.g. (26,34,36); `OutdoorAmbient` warm by day, cool blue at night; `Brightness` 2–3 day, 0.5–1 night; `ExposureCompensation` 0, ±0.5 for mood; `EnvironmentDiffuseScale` 0.5–1; `EnvironmentSpecularScale` 0.7–1 with PBR metals; `ShadowSoftness` 0.15–0.3 (Realistic only); `ClockTime` and `GeographicLatitude` scripted and tuned for long shadows.

Curriculum preset (exact doc values): Ambient and OutdoorAmbient (26,34,36), LightingStyle Realistic, ShadowSoftness 0.15, GeographicLatitude −18; Atmosphere Density 0.285, Offset 0.65, Decay (254,254,254), Glare 0.3, Haze 2.

House starting presets (tune in-engine):

| Preset | Style | ClockTime | Brightness | Ambient / OutdoorAmbient | Atmosphere D/O/H/G | Post |
|---|---|---|---|---|---|---|
| Bright stylized day | Soft or Realistic | 14 | 2.5 | (70,70,80) / (120,120,130) | 0.25 / 0.25 / 0.5 / 0 | Bloom low, Saturation +0.1 |
| Golden hour town | Realistic | 17.6 | 2 | (40,35,45) / (110,90,80) | 0.3 / 0.3 / 1.5 / 0.4 | SunRays low, Bloom low |
| Night city (neon) | Realistic | 0 | 0.5 | (15,15,25) / (40,45,70) | 0.35 / 0.2 / 1 / 0 | Bloom for signs |
| Overcast | Realistic | 12 | 1.2 | (50,55,60) / (90,95,100) | 0.4 / 0.1 / 2.5 / 0 | Contrast +0.1 |
| Interior shop | Realistic | any | 1.5 | (30,30,35) / (60,60,70) | 0.2 / 0.5 / 0 / 0 | SurfaceLights in Blender fixtures |

Stylised finish `[community]`: one `ColorCorrectionEffect` with Contrast and Saturation around +0.1 to +0.2 does most of the work for flat-colour art; keep `BloomEffect.Intensity` low (0.1–0.5) and raise `Threshold` so only emissive and neon bloom. There is no agreed preset; tune against the golden sample.

Atmosphere `Density` hides streaming pop-in and lets you lower `StreamingTargetRadius`. Glare needs Haze > 0; Decay needs Haze and Glare > 0. Changing `Workspace.GlobalWind` wakes physics assemblies. Post-processing effects each cost full-screen GPU time: keep at most 2–3 always on; toggle Blur and DepthOfField contextually.

Lighting performance: lights go on `_Att` attachments inside Blender fixture models with `Shadows = false` by default; bake mood into textures, emissive and vertex colour; interiors need walls ≥ 1 stud thick (extra blockers are invisible helpers); test at graphics levels 1–3 where shadows are off.

## Asset acceptance checklist (per asset, pass or fail)

- [ ] Named to convention; root at origin; pivot where the asset attaches; rotation 0, scale 1.
- [ ] Triangles within class budget after modifiers; no n-gons; normals out; bevels and weighted normals to the bible standard.
- [ ] One material, one UV set in 0–1; texturing method and texel density match the bible; no new texture unless the bible allows it.
- [ ] Colours only from the palette; vertex colour present if the kit uses it (`COLOR_0` in the GLB).
- [ ] Collision plan explicit: `Fidelity` property or `_COL` child; walk and jump on it in Studio with collision visualisation on.
- [ ] `_Att` points present for every light, prompt, seat and VFX socket the design calls for.
- [ ] `export_kit.py` exits 0; manifest row written; upload operation `Approved`; uploaded under the owning group.
- [ ] Wrapped as a package; placed copies share one MeshId; no duplicate upload of the same piece.
- [ ] Held next to the golden sample under final lighting, at graphics level 1–3 and on a phone: reads by silhouette, nothing glows that should not, no z-fighting, no light leaks.
- [ ] CastShadow off if small; RenderFidelity Automatic (Performance for clutter); streaming mode set (Atomic for interactive props).

## Level-up: art symptoms → cause → fix

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| Mismatched styles (flat props beside PBR props, sharp beside blurry) | Assets from several sources, no bible, mixed texel density | Write the bible from the best 20% of assets; re-texture the rest onto the palette or trim library; replace marketplace models with kit pieces |
| Primitive leftovers (visible Parts, unions, greybox) | Blockout never replaced | Run the house-rule scan in checklists.md, sort by count, model the top offenders as kit pieces first; invisible helpers may stay |
| Walk-through props, or invisible walls around props | `CanCollide` off on imports, missing `_COL`, Box fidelity on a concave shape | Collision scan; add `Fidelity` or `_COL`; doorway = three boxes; walk test with collision visualisation |
| Heavy draw calls in one view | Duplicate MeshIds from whole-map imports, a texture per prop, multi-material meshes, many decals | Duplicate-MeshId audit (performance.md); re-point copies to one package; shared `_SA`; merge unique clutter; replace decals with trim or palette detail |
| Texture memory high, blurry textures on phones | Unique 1024² sets per prop | Move props to the palette atlas or trim library; cap unique bakes; ≤ 512² default |
| Looks flat or "plastic" | No bevels, no AO, default lighting | Bevel and weighted-normal pass; vertex-colour AO; pick a lighting preset and one ColorCorrection |
| Dark, inside-out or faceted shading | Flipped normals, unapplied Mirror or scale, modifiers not applied at export | Recalculate normals, apply transforms, export with `export_apply=True` |
| Doors, stairs or furniture feel the wrong size | Modelled in metres or without the R15 dummy | Rescale against the dummy; lock the grid and proportions in the bible |
| Characters snag, hover or stutter on stairs and trims | Default or Precise fidelity on detailed meshes, per-step collision | `_COL` ramp and simple hulls; Box on trims; reserve Precise for approved cases |
| Grey or missing meshes for players, fine in Studio | Asset still in moderation, uploaded under the wrong creator, Restricted asset not granted to the game | Check the operation's moderation state; upload under the owning group; grant the game in the asset's permissions |
| Every art tweak breaks references | Raw re-uploads mint new ids | Package versioning (Blender add-on or Reimport) and the generated ids manifest |
| Washed-out, glowing scenes | Neon used as decoration, Bloom threshold too low, several stacked post effects | Emissive only on interactables; raise Bloom `Threshold`; keep 2–3 effects |

## Review gate

- [ ] Style bible filled in and versioned; a golden sample exists in Studio; every asset passed the acceptance checklist.
- [ ] Every mesh came from the Blender pipeline; the manifest maps every asset name to an id; no marketplace or free models; no visible primitive Parts; Terrain only with the owner's explicit per-game approval.
- [ ] Each kit piece uploaded once and placed as a package; duplicate-MeshId audit clean.
- [ ] Triangle budgets met; ≤ 20k per mesh; one material and one UV set per mesh.
- [ ] Textures ≤ 1024², mostly ≤ 512², from the shared palette or trim library; `_SA` SurfaceAppearances shared.
- [ ] Every visible object collides (fidelity or `_COL`); house-rule scan in checklists.md passes; walk-through test passes.
- [ ] RenderFidelity Automatic (Performance for clutter); SLIM on large static models where available.
- [ ] All uploaded assets `Approved` and owned by the game's group before the build is published.
- [ ] LightingStyle and PrioritizeLightingQuality chosen; no interior light leaks; CastShadow off on small, moving and invisible parts.

Grep `references/knowledge-base.md` for `## 5.7`, `## 5.8` and `### 4.10.4`. Tool and skill options for this pipeline: `references/ai-toolchain-skills.md`.

## Sources

Accessed 2026-11-10.

- https://github.com/Roblox/creator-docs (read, commit ccc2b01 of 2026-11-07), under `content/en-us/`: `art/modeling/specifications.md`, `art/modeling/texture-specifications.md`, `art/modeling/export-requirements.md`, `art/modeling/reimport.md`, `art/modeling/roblox-blender-plugin.md`, `art/blender.md`, `studio/importer.md`, `studio/mcp-open-cloud.md`, `parts/meshes.md`, `parts/textures-decals.md`, `cloud/guides/usage-assets.md`, `cloud/reference/rate-limits.md`, `reference/cloud/assets/v1.json`, `projects/assets/index.md`, `projects/assets/privacy.md`, `performance-optimization/improve.md`, `workspace/streaming/slim.md`, `reference/engine/classes/{MeshPart,TriangleMeshPart,SurfaceAppearance,Lighting,BloomEffect,ColorCorrectionEffect}.yaml`, `reference/engine/enums/CollisionFidelity.yaml`
- https://github.com/Roblox/roblox-blender-plugin (read: README, package versioning)
- https://github.com/jackTabsCode/asphalt (read: README note that the web API exposes no import settings)
- Blender 5.2.3 LTS `bpy` wheel from PyPI (ran the scripts above; read `export_scene.gltf` option defaults)
- https://devforum.roblox.com/t/studio-beta-auto-reimport-automatically-reimport-external-files-on-changes/4859863 (search summary)
- https://devforum.roblox.com/t/full-release-reimport/4622567 (search summary)
- https://devforum.roblox.com/t/4k-texture-rendering/4316229 and https://devforum.roblox.com/t/introducing-texture-streaming/4144855 (search summary)
- https://devforum.roblox.com/t/surface-appearance-loads-inconsistently-on-mobile-and-often-displays-at-very-low-quality-even-if-the-phone-allows-it/4530853 (search summary)
- https://devforum.roblox.com/t/does-roblox-use-mesh-instancing/399564 and https://devforum.roblox.com/t/part-instancing-pre-release-announcement/130333 (search summary)
- https://devforum.roblox.com/t/first-person-shooter-map-design-in-roblox-picture-heavy/25475, https://devforum.roblox.com/t/few-questions-from-professional-builders/2891675, https://devforum.roblox.com/t/low-poly-lighting/1015398, https://devforum.roblox.com/t/improve-lighting-step-by-step/1387033 (search summary)
- https://gamedevreport.beehiiv.com/p/the-one-trick-to-making-good-looking-games (search summary)
- https://devforum.roblox.com/t/weird-shading-on-meshes-imported-from-blender/2964265 (search summary)
- https://projects.blender.org/blender/blender-addons/issues/96517 and https://blenderartists.org/t/geo-nodes-instances-to-real-instances/1409710 (search summary)
- Searched without usable evidence: r/robloxgamedev and r/ROBLOXStudio threads on art cohesion (no results returned), an RDC talk on mobile art readability (none found), a 2026 triangle-limit increase (none found).
