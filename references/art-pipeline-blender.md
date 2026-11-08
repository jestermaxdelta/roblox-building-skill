# Blender-to-Roblox art pipeline and lighting

Distilled from knowledge-base sections 5.7, 5.8 and 4.10.4. House rules 1 and 2: every visible object is a Blender model, nothing visible is a primitive Part or a marketplace asset, and everything visible is solid. `[VS]` marks version-sensitive facts; exporter and importer parameter names change between releases.

## Pipeline overview

1. **Style bible and kit plan first**: palette, texel density, bevel standard, trim-sheet set and grid (see "Cohesive art style").
2. **Author in Blender through the Blender Lab MCP bridge** (`tools/blender_exec.py` in the game repo sends Python to the running Blender). Use it for modelling, validation and layout, never for export.
3. **Validate in Blender**: triangle counts, applied transforms, one material per mesh, one UV map, naming, `_COL` proxies present.
4. **Export GLB in a separate headless process**: `blender -b assets/blender/<file>.blend --python tools/export_glb.py -- <RootObject> build/<Asset>.glb`. Never export from the MCP-driven session.
5. **Upload through Open Cloud** (`POST https://apis.roblox.com/assets/v1/assets`, `model/gltf-binary`), poll the operation, record the asset id in a manifest.
6. **Insert into Studio** (Studio MCP, Toolbox "My Models" or Asset Manager) and run the post-import fix-up script (anchoring, collision flags, `_COL` handling, CastShadow, RenderFidelity, shared SurfaceAppearances).
7. **Wrap each kit piece or prop as a package** (PackageLink, AutoUpdate on). Place package copies, never fresh imports.
8. **QA under final lighting** at a low graphics level and on a real phone.

Blockout rule (knowledge-base resolution): no primitive greybox ships. Prototype with a Blender blockout kit (a handful of boxy GLB modules) or in a throwaway place that is never published.

## Units, scale, orientation, transforms

- 1 stud = 0.28 m (1 m ≈ 3.57 studs). Gravity 196.2 studs/s².
- Convention: **1 Blender unit = 1 stud** (Studio importer Scale Unit = Stud). Blender Scene > Units > Unit System = None (or Metric with Unit Scale 1), Rotation = Degrees. Do not mix with metric-scale assets (importer Scale Unit = Meter multiplies by about 3.57).
- Keep an R15 dummy exported from Studio in a hidden Blender collection; Roblox avatars are chunky, so size doors, counters, steps and seats against it.
- Orientation: glTF exports +Y up; model assets facing −Y in Blender; Studio importer World Forward = Front, World Up = Top; confirm once with an asset that has an obvious front.
- Apply all transforms (rotation 0, scale 1) before export. Skinned meshes: bones scale 1 and rotation 0, root at origin, at most 4 influences per vertex, no influence on the root bone.

## Grid and pivots

- One grid per project, written in the style bible: 5-stud grid (environmental-art curriculum), 16-stud for large architecture (Beyond the Dark), 4- or 8-stud sub-grid for props in town games.
- Modular kit pivots at the front-lower corner so pieces snap edge to edge in 90° steps. Prop pivots where the prop attaches: bottom-centre for floor props, back-centre for wall props, top-centre for hanging props.
- Place each asset's origin at world (0,0,0) in Blender before export so Use Imported Pivot, Set Pivot to Scene Origin and Insert Using Scene Position agree.

## Mesh specifications and budgets

Doc limits: ≤ 20,000 triangles per mesh (import limit); watertight; no n-gons; one material per mesh (each extra material slot becomes another MeshPart, draw call and collision shape); one UV set in 0–1 space (overlaps allowed); consistent normals; Make Double Sided only for foliage cards.

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

Spend triangles on silhouette and edge bevels. A 0.05–0.15 stud chamfer with weighted normals is the single biggest cure for the "cheap AI asset" look.

## Textures, texel density and materials

- Treat 1024² as the practical maximum (4096² is a technical upload limit). Most textures ≤ 512², minor ≤ 256². Images are transcoded, so file-size tricks do not save memory.
- Texel density: about 50 px per stud for environment and architecture, up to about 100 px per stud for arm's-length props; keep it consistent across the kit. (The docs give 256² per 5×5 studs, about 51 px/stud, and a PBR page gives about 128 px/stud; the house value is the lower one.)
- PBR maps: ColorMap sRGB, authored near-white if you tint; NormalMap OpenGL tangent space (Blender's default; never DirectX); RoughnessMap 8-bit, add about +0.1 to compensate for Roblox's Fresnel; MetalnessMap 0 or 1; emissive via `EmissiveMaskContent`, `EmissiveStrength`, `EmissiveTint` `[VS]`.
- `SurfaceAppearance.AlphaMode`: Overlay (default, alpha reveals `MeshPart.Color`), Transparency (cutout at part Transparency 0; blending from 0.02), TintMask, Opaque (beta `[VS]`). SurfaceAppearance overrides MaterialVariant maps and most of its properties cannot change at runtime, so make variants as separate instances.
- Material architecture: 4–8 shared 1024² trim sheets (metal, wood, concrete, painted panels, signage, fabric) plus a few tileables; upload each map once; one SurfaceAppearance per material named `<Name>_SA`, published as a package material library; tileables as MaterialVariants with Set as Override and Organic tiling; each Blender material is a placeholder name (`M_Trim_Metal`) that the post-import script swaps for the matching `_SA`. Beyond the Dark built 90% of its architecture from a handful of trim sheets. Avoid recognisable stains on trims.
- Vertex colour adds variation without textures; keep importer Ignore Vertex Colors off if you rely on it.

## Naming and hierarchy

| Convention | Meaning |
|---|---|
| `SM_<Category>_<Name>_<Variant>` | Static mesh, e.g. `SM_Street_Lamp_A` |
| `SK_<Name>` | Skinned mesh |
| `KIT_<Set>_<Piece>_<WxH>_<Variant>` | Modular piece, e.g. `KIT_Shop_Wall_16x12_A` |
| `<Asset>_COL` | Invisible collision proxy (house convention; Roblox has no UCX_ auto-collision) |
| `<Name>_Att` | Imported as an Attachment: `Prompt_Att`, `Light_Att`, `VFX_Steam_Att`, `Seat_Att` |
| `_OuterCage` / `_InnerCage` | Layered clothing cages |
| `<Name>_SA` | SurfaceAppearance |
| `M_<Library>_<Name>` | Blender placeholder material |

glTF imports as a nested Model with one MeshPart per primitive; name collisions get `_Node`. Split multi-part assets into named children (`Door`, `Frame`, `Handle_Att`) so moving parts can animate and each piece gets the right collision. `_Att` empties are the hand-off between art and code: scripts find attachments by name instead of hard-coding offsets.

## Collision authoring

- Decide per asset in the style bible: fidelity on the visual mesh (Box or Hull) or a `_COL` proxy.
- `_COL` proxies are convex (or a few convex pieces), have no material, 12–200 triangles, sit flush on walkable surfaces. Doorways use three boxes (two jambs and a lintel); stairs use a single ramp.
- Export `_COL` objects in the same GLB as the visual mesh.
- Flags after import are in performance.md ("Making everything solid").

## Headless export script

```python
# tools/export_glb.py
# usage: blender -b assets/street_props.blend --python tools/export_glb.py -- SM_Street_Lamp_A build/SM_Street_Lamp_A.glb
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
root_name, out_path = argv[0], argv[1]

bpy.ops.object.select_all(action="DESELECT")
root = bpy.data.objects[root_name]
for obj in [root, *root.children_recursive]:
    obj.hide_set(False)
    obj.select_set(True)
bpy.context.view_layer.objects.active = root

bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format="GLB",
    use_selection=True,
    export_apply=True,        # apply modifiers (bevels, weighted normals)
    export_yup=True,
    export_texcoords=True,
    export_normals=True,
    export_materials="EXPORT",
    export_animations=False,
)
```

Pin the Blender version in the repo and re-check `bpy.ops.export_scene.gltf` options on upgrade. FBX (animations, and the FBX-only update endpoint): Path Mode = Copy with Embed Textures, Apply Scalings = FBX Unit Scale, Add Leaf Bones off, Bake Animation off for static meshes; one animation track per file.

Pre-export validation (run through the MCP bridge):

```python
import bpy, bmesh
MAX_TRIS = 20000
problems = []
for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    if any(abs(s - 1) > 1e-4 for s in obj.scale):
        problems.append(f"{obj.name}: unapplied scale {tuple(obj.scale)}")
    if len(obj.data.uv_layers) != 1 and not obj.name.endswith("_COL"):
        problems.append(f"{obj.name}: {len(obj.data.uv_layers)} UV maps (need 1)")
    if len([m for m in obj.material_slots if m.material]) > 1:
        problems.append(f"{obj.name}: more than one material")
    bm = bmesh.new(); bm.from_mesh(obj.data)
    tris = sum(len(f.verts) - 2 for f in bm.faces)
    ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
    bm.free()
    if tris > MAX_TRIS: problems.append(f"{obj.name}: {tris} tris > {MAX_TRIS}")
    if ngons: problems.append(f"{obj.name}: {ngons} n-gons")
print("\n".join(problems) or "OK")
```

## Open Cloud upload `[VS]`

```bash
curl -s -X POST "https://apis.roblox.com/assets/v1/assets" \
  -H "x-api-key: $ROBLOX_API_KEY" \
  -F 'request={"assetType":"Model","displayName":"SM_Street_Lamp_A","description":"Street lamp, kit v3","creationContext":{"creator":{"groupId":"1234567"}}}' \
  -F 'fileContent=@build/SM_Street_Lamp_A.glb;type=model/gltf-binary'
curl -s -H "x-api-key: $ROBLOX_API_KEY" "https://apis.roblox.com/assets/v1/operations/$OPERATION_ID"
```

- Content types: `model/gltf-binary`, `model/gltf+json`, `model/fbx`. At most 20 MB per file. Images under 8000×8000. Audio up to 7 minutes; quota 100 a month verified / 10 unverified on the Open Cloud page (the audio page says 2,000 / 100; plan around the stricter numbers).
- The key needs the assets scope with Read and Write (OAuth `asset:read`, `asset:write`). Upload under the group that owns the game or the place may not load the asset.
- Uploaded models arrive as a Model of MeshParts, as a package. Reference by `rbxassetid://<id>` or `Content.fromAssetId(id)`.
- Content updates (PATCH) are supported for `.fbx` only and are beta. **Every GLB re-upload creates a new asset id**, so a Lune or Python script owns `assets/asset-ids.json` (name → id, file hash, version) and regenerates `Shared/Config/Assets.luau`; update placements by editing the package and publishing so AutoUpdate propagates. Never hand-edit ids.
- Never commit the API key; scope it to one group and the assets API.

## Studio 3D Importer preset (manual imports)

Import Only As Model on; Upload to Roblox on; Creator = the group that owns the game; Import as Package on for kit pieces and props; Add to Workspace on; Insert Using Scene Position on for layouts, off for single assets; Set Pivot to Scene Origin on; Use Imported Pivot on; Anchored on for static assets; Scale Unit = Studs; World Forward/Up = Front/Top; Merge Meshes off; Make Double Sided off; Invert Negative Faces off; Ignore Vertex Colors off if used. The importer does not de-duplicate meshes: import each kit piece once, then place package copies.

## Post-import fix-up (edit time, via Studio MCP `execute_luau` or the command bar)

```lua
local function fixup(model: Model)
	for _, d in model:GetDescendants() do
		if d:IsA("MeshPart") then
			d.Anchored = true
			if d.Name:match("_COL$") then
				d.Transparency = 1
				d.CanCollide, d.CanQuery, d.CanTouch = true, true, false
				d.CastShadow = false
				d.CollisionFidelity = Enum.CollisionFidelity.Hull
			elseif model:FindFirstChild(d.Name .. "_COL", true) or model:GetAttribute("HasCOL") then
				d.CanCollide, d.CanTouch = false, false
				d.CollisionFidelity = Enum.CollisionFidelity.Box
			else
				d.CanCollide, d.CanTouch = true, false
				local fid = model:GetAttribute("Fidelity") or "Hull"
				d.CollisionFidelity = Enum.CollisionFidelity[fid]
			end
			if d.Size.Magnitude < 3 then d.CastShadow = false end
		end
	end
end
```

`CollisionFidelity` is not settable from a running game script; this runs at edit time only.

## Modular kits and packages

Keep the kit small and versatile (Beyond the Dark placed over 1,000 instances of a few wall panels). Each piece is a package with AutoUpdate on, so one Blender fix propagates everywhere and keeps the asset id. Snap on the kit grid, rotate in 90° steps, hide seams with trims (cornices, corner posts, skirting), and prefer variant SurfaceAppearances over new meshes.

## Cohesive art style (avoiding the generic look)

Write a one-page style bible and check every asset against it:

1. Palette: 8–12 base colours plus 2 accents, applied through `SurfaceAppearance.Color`, `MeshPart.Color` or vertex colour; unlisted colours banned.
2. Shape language: either soft-rounded and chunky or crisp with small bevels; exaggerate proportions slightly for the chunky avatar (thicker frames, larger handles).
3. Bevel standard: one chamfer width per size class (for example 0.05 studs props, 0.15 architecture), always weighted normals.
4. One texel density and one shared trim library.
5. Roughness range per material family (painted metal 0.4–0.6, raw concrete 0.8–0.95); metalness 0 or 1.
6. Consistent wear and grime direction (gravity-driven), not random noise.
7. Review in-engine under the final Lighting and Atmosphere at a low graphics level and on a phone.

Anti-patterns: mixed texel densities, noisy procedural textures, saturated rainbow palettes, everything glowing, unbevelled boxes, one-off textures per prop, marketplace-looking proportions, text baked into textures (use SurfaceGui or decals for localisable signage).

## Lighting `[VS]`

`Lighting.Technology` is superseded by `Lighting.LightingStyle` (Realistic or Soft; new places start on Soft) and `Lighting.PrioritizeLightingQuality` (true keeps shadows and shaders close up; false keeps view distance). Voxel, ShadowMap and Future remain in the old enum; Legacy, Compatibility and Unified are deprecated (Retro look: Voxel plus `ColorGradingEffect.TonemapperPreset = Retro`).

Decision rule: Realistic for interiors, local lights, PBR metals or a night mode (most Blender-art games); Soft for bright flat cartoon styles. `PrioritizeLightingQuality = true` for small dense worlds, false for large open maps.

| Property | Starting point |
|---|---|
| `Ambient` | Dark, slightly tinted, e.g. (26,34,36) |
| `OutdoorAmbient` | Warm by day, cool blue at night |
| `Brightness` | 2–3 day, 0.5–1 night |
| `ExposureCompensation` | 0, ±0.5 for mood |
| `EnvironmentDiffuseScale` | 0.5–1 |
| `EnvironmentSpecularScale` | 0.7–1 with PBR metals |
| `ShadowSoftness` | 0.15–0.3 (Realistic only) |
| `ClockTime` / `GeographicLatitude` | Scripted cycle; tune for long shadows |

Curriculum preset (exact doc values): Ambient and OutdoorAmbient (26,34,36), LightingStyle Realistic, ShadowSoftness 0.15, GeographicLatitude −18; Atmosphere Density 0.285, Offset 0.65, Decay (254,254,254), Glare 0.3, Haze 2.

House starting presets (tune in-engine):

| Preset | Style | ClockTime | Brightness | Ambient / OutdoorAmbient | Atmosphere D/O/H/G | Post |
|---|---|---|---|---|---|---|
| Bright stylized day | Soft or Realistic | 14 | 2.5 | (70,70,80) / (120,120,130) | 0.25 / 0.25 / 0.5 / 0 | Bloom low, Saturation +0.1 |
| Golden hour town | Realistic | 17.6 | 2 | (40,35,45) / (110,90,80) | 0.3 / 0.3 / 1.5 / 0.4 | SunRays low, Bloom low |
| Night city (neon) | Realistic | 0 | 0.5 | (15,15,25) / (40,45,70) | 0.35 / 0.2 / 1 / 0 | Bloom for signs |
| Overcast | Realistic | 12 | 1.2 | (50,55,60) / (90,95,100) | 0.4 / 0.1 / 2.5 / 0 | Contrast +0.1 |
| Interior shop | Realistic | any | 1.5 | (30,30,35) / (60,60,70) | 0.2 / 0.5 / 0 / 0 | SurfaceLights in Blender fixtures |

Atmosphere `Density` hides streaming pop-in and lets you lower `StreamingTargetRadius`. Glare needs Haze > 0; Decay needs Haze and Glare > 0. Changing `Workspace.GlobalWind` wakes physics assemblies. Post-processing effects each cost full-screen GPU time: keep at most 2–3 always on; toggle Blur and DepthOfField contextually.

Lighting performance: lights go on `_Att` attachments inside Blender fixture models with `Shadows = false` by default; bake mood into textures, emissive and vertex colour; interiors need walls ≥ 1 stud thick (extra blockers are invisible helpers); test at graphics levels 1–3 where shadows are off.

## Art review gate

- [ ] Every mesh came from the Blender pipeline; the manifest maps every asset name to an id; no marketplace or free models; no visible primitive Parts; Terrain only with the owner's explicit per-game approval.
- [ ] Each kit piece uploaded once and placed as a package; duplicate-MeshId audit clean.
- [ ] Triangle budgets met; ≤ 20k per mesh; one material and one UV set per mesh.
- [ ] Textures ≤ 1024², mostly ≤ 512², from the shared trim library; `_SA` SurfaceAppearances shared.
- [ ] Every visible object collides (fidelity or `_COL`); house-rule scan in checklists.md passes; walk-through test passes.
- [ ] RenderFidelity Automatic (Performance for clutter); SLIM on large static models where available.
- [ ] Style bible check under final lighting at a low graphics level.
- [ ] LightingStyle and PrioritizeLightingQuality chosen; no interior light leaks; CastShadow off on small, moving and invisible parts.

Grep `references/knowledge-base.md` for `## 5.7`, `## 5.8` and `### 4.10.4`.
