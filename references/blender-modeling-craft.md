# Blender modelling craft for Roblox

How to make a model that looks designed at phone size: the numbers behind readability, shape, proportion, edges, triangle spending and colour, then recipes, a concept-to-model workflow, a 0–10 quality rubric and a first-kit walkthrough. Open it before modelling, when reviewing an asset, or when a live game "looks cheap" and nobody can say why. Getting the finished model into Roblox (export, upload, collision flags, lighting, style-bible template) is `references/art-pipeline-blender.md`; rigs and animation are `references/animation-and-rigs.md`. House rule 1 applies throughout: every asset is authored in Blender, by hand or by script. Tags: `[official]`, `[community]`, `[lihfolk]` (adapted from LihFolk Vault V2, CC BY 4.0), `[house]`, `[VS]`.

## Start here by level

| Level | Do these first | Ignore for now |
|---|---|---|
| Beginner | Follow "First kit walkthrough". Keep the two avatar proxies in every file. Judge every model as a black silhouette at about 64 px before adding detail. One bevel width, one palette | Sculpting, normal-map baking, custom normals, voxel meshing |
| Intermediate | Size features from the pixel table, exaggerate in pairs, choose bevel widths by viewing distance, plan value bands before hue, review at blockout, score every asset on the rubric | Scripted generation, mechanical gates |
| Expert | Segment counts from the sagitta rule, GPU vertex splits, triangle spend by direction, normal transfer for canopies, symmetry and seating gates on scripted assets, colour scripts per zone, roster tests across the whole cast | Nothing |

Terms: a **stud** is Roblox's length unit (0.28 m); the **silhouette** is the filled outline of a model; a **bevel** replaces a sharp edge with a narrow strip (a one-strip bevel is a **chamfer**); **normals** are the per-vertex directions that decide shading; **weighted normals** bias those directions toward large faces so flat faces stay flat; **value** is how light or dark a colour is, independent of hue; a **texel** is one texture pixel.

Contents: The numbers · Shape and silhouette · Proportion and exaggeration · Edges and shading · Spending triangles · Colour and value · Faceted and voxel styles · Recipes and budgets · Concept to model · Quality rubric · First kit walkthrough · Level-up · Review gate · Sources

## The numbers that drive every decision

On-screen size, with the default 70° vertical field of view `[official]`: `pixels = size × screenHeight / (1.40 × distance)`. Use 720 px as the phone render height `[lihfolk]` (phones often render below native resolution; exact scaling is undocumented).

| Distance (studs) | What lives there | 1 px on a 720 px phone | Smallest feature that reads (about 3 px) | Pixels per stud |
|---|---|---|---|---|
| 8 | Held tool, shop counter, pet | 0.016 studs | 0.05 | 64 |
| 15 | Own character, nearby props | 0.03 | 0.09 | 34 |
| 40 | Enemies at range, buildings | 0.08 | 0.25 | 13 |
| 100 | Landmarks across a zone | 0.19 | 0.6 | 5 |
| 300 | Skyline | 0.58 | 1.75 | 2 |

Rules that fall out of it:
- One phone pixel covers about `d / 520` studs. Under 2 px a feature flickers or vanishes, so the floor is `d / 260`; aim for `d / 170` on anything that matters `[lihfolk]`.
- A 0.1-stud window bar at 40 studs is 1.3 px: invisible however well it is modelled. A 40-stud tower at 300 studs and an 8-stud enemy at 60 studs both land near 69 px, which is why landmarks can be simple.
- Text on a model needs letter height of at least `d / 25` studs; an icon shape reads further than letters `[lihfolk]`.
- Aspect changes the view: horizontal field of view is about 86° at 4:3, 102° at 16:9 and 113° on a 19.5:9 phone. A facade that ends just off-screen on a monitor shows its unfinished side on a phone `[lihfolk]`.
- The follow camera starts about 12.5 studs behind the character and looks down 10–40° `[lihfolk]`. Tops of things are on screen more than fronts.

Player scale `[lihfolk]`, in avatar heights (classic avatar about 5 studs; taller body types about 6.5; default jump 7.2 studs and walk speed 16 studs/s `[official]`):

| Element | Avatar heights | Studs (5-stud avatar) |
|---|---|---|
| Door height / width | 1.5–1.6 / 1.0–1.2 | 7.5–8 / 5–6 (gameplay doors at least 5 wide; 3.6–4 only for decorative or single-occupant doors, per level-design-worldbuilding.md) |
| Corridor width | 1.6–2.4 | 8–12 (room for the camera) |
| Indoor ceiling | 2–3 | 10–15 (real-world ceilings push the camera into the roof) |
| Table or counter top | 0.5–0.6 | 2.5–3 |
| Step rise / tread | 0.2–0.3 | 1–1.5 rise, 2–3 tread |
| See-over wall | under 0.6 | under 3 |

Size openings for the largest avatar the game allows, not the classic one.

Blender setup that matches the game `[lihfolk]`: a `Scale_Ref` collection (excluded from export) with a 5-stud and a 6.5-stud proxy; a camera with Lens Unit = Field of View, Sensor Fit = Vertical, 70°; output 1560×720 for the phone check and 1920×1080 for PC; camera 12.5 units behind and 3–4 above the proxy's head, pitched down 15–20°; extra camera positions at 25, 40 and 80 units. Judge models through that camera, never in a close-up viewport.

Measure the real thing in Studio (fly the camera to a player position, select a model):

```lua
--!strict
-- unexecuted sketch, command bar: on-screen height of the selected model, here and on a 720 px phone
local camera = workspace.CurrentCamera
local target = game:GetService("Selection"):Get()[1]
if camera and target and target:IsA("Model") then
	local cf, size = target:GetBoundingBox()
	local minY, maxY = math.huge, -math.huge
	for _, sx in { -0.5, 0.5 } do
		for _, sy in { -0.5, 0.5 } do
			for _, sz in { -0.5, 0.5 } do
				local p = camera:WorldToViewportPoint(cf * Vector3.new(size.X * sx, size.Y * sy, size.Z * sz))
				minY, maxY = math.min(minY, p.Y), math.max(maxY, p.Y)
			end
		end
	end
	local here = maxY - minY
	print(string.format("%s: %.0f px here, about %.0f px on a 720 px phone, %.0f studs away", target.Name, here,
		here * 720 / camera.ViewportSize.Y, (camera.CFrame.Position - cf.Position).Magnitude))
end
```

## Shape language and silhouette

Shape carries more on Roblox than in most engines: screens are small, lighting quality differs per player, and every player's avatar clashes with your palette `[lihfolk]`. Detail does not survive those three; outline and value do.

- **Hierarchy**: one primary mass that says what the thing is, two to four secondary shapes that break the outline, tertiary detail only inside the hand band. Make each level clearly smaller than the last; three similar-sized lumps read as noise.
- **Vocabulary**: round reads friendly, square reads sturdy, triangles and spikes read hostile. Pick a dominant shape per asset and add one contrasting accent. Set straights against curves, vary spacing (even repetition reads as manufactured), and give living things a lean or line of action.
- **Negative space and tangents**: gaps (between arm and body, under an arch) are part of the outline; close them and the model becomes a lump. Edges that only just touch flatten the read: overlap clearly or separate clearly.
- **Taper says grown, uniform width says made** `[lihfolk]`. Support must look able to carry the load (a huge head on a thread-thin stem reads as an error). Anything near a face becomes a facial feature. Models look assembled at the joints, so give every junction a collar, cuff or socket.

Four-view silhouette test `[lihfolk]`, rendered as flat black at game pixel height (about 64 px for props, 96 px for characters):

| View | Why | Pass when |
|---|---|---|
| Side | Enemies crossing the screen | Identifiable as a filled shape |
| Front three-quarter | Approaching NPCs and enemies | At least one secondary breaks the outline |
| High three-quarter (35° down) | The default follow camera | Top surfaces carry a distinct shape |
| Top | Pets, pickups, ground props | Not a featureless blob: a crest, rim, ears or cap survives |

Then the roster test: put every enemy, pet or pickup of a set in one row and confirm no two share a primary shape (colour is the second cue, never the first), and that a rarer version changes the outline, not just the trim. Flip the sheet horizontally to expose lopsided shapes. Test characters in their idle pose.

```python
# Tested on Blender 5.2.3 (bpy, headless, Cycles on CPU). Writes <path>_side/_front34/_high34/_top.png, black on white.
import bpy, math
from mathutils import Vector

def silhouette_sheet(objs, path, px_high=96):
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.samples = 1; sc.view_settings.view_transform = "Standard"
    world = sc.world or bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    black = bpy.data.materials.new("SIL"); black.use_nodes = True; black.node_tree.nodes.clear()
    out = black.node_tree.nodes.new("ShaderNodeOutputMaterial"); em = black.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (0, 0, 0, 1); black.node_tree.links.new(em.outputs[0], out.inputs[0])
    bpy.context.view_layer.material_override = black
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    centre = sum(pts, Vector()) / len(pts); radius = max((p - centre).length for p in pts)
    cam = bpy.data.objects.new("SilCam", bpy.data.cameras.new("SilCam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 2.2 * radius
    sc.render.resolution_x = sc.render.resolution_y = px_high
    for name, yaw, pitch in (("side", 90, 0), ("front34", 45, 0), ("high34", 45, 35), ("top", 0, 85)):
        y, p = math.radians(yaw), math.radians(pitch)
        cam.location = centre + 4 * radius * Vector((math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), math.sin(p)))
        cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = f"{path}_{name}.png"; bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.material_override = None
```

## Proportion and exaggeration

Exaggeration is a function of viewing distance, not taste `[lihfolk]`. Decide the band first: hand (0–10 studs), character (10–25), engagement (25–80), landmark (80–400), skyline (beyond). Most exaggeration pays off in the engagement band.

| Feature | Multiply real proportion by | Why |
|---|---|---|
| Head | 1.3–2 (chibi 2.5–3) | Identity reads further |
| Hands, feet | 1.3–1.6 | Gestures read; weapons look gripped |
| Eyes | 1.5–3 | Facing and mood read at 20–40 studs |
| Signature item or weapon | 1.3–2 | Role reads instantly |
| Waist, neck, wrists | 0.7–0.9 | The thin part is what makes the big part look big |
| Window frames, rims, trims | 2–4 | Survive the pixel table |
| Handles, knobs, lamps | 1.5–2.5 | Interactables must look usable |
| Roof overhang | 1.5–2 | Strong shadow line from the high camera |
| Fence posts and rails | posts 0.4–0.8 studs thick, gaps ≥ 0.6 | Thin rails alias and vanish |

- **Exaggerate in pairs**: everything scaled up just looks fat. Big hands need thin wrists.
- **Small props carry the most**: a real lantern is a fifth of a person's height; a stylised one is often half an avatar and looks right. Use 3–5 props at 1.5–2.5× grouped into one secondary shape, not 15 at true size.
- **Flat-colour art needs about 1.5× thicker trims** than textured art at the same distance, because the pattern has to live in geometry `[lihfolk]`.
- **Where it breaks gameplay**: keep collision tight to the gameplay shape when the visual is oversized; keep decorative props near paths under about 1.5 avatar heights or the follow camera pumps in and out; never derive a weapon hitbox from its exaggerated mesh. Write the multipliers into the style bible so two artists do not build two worlds.

## Edges and shading

A razor-sharp edge catches no light, so the form reads as a flat cut-out. A bevel gives the edge a strip that faces the light. It only works if the strip is wide enough on screen.

| Viewing distance | Minimum readable bevel | Typical stylised choice `[lihfolk]` |
|---|---|---|
| 5–10 studs | 0.02–0.04 studs | 0.03–0.06 |
| 15 | about 0.06 | 0.06–0.12 |
| 40 | about 0.15 | 0.15–0.3 |
| 100 | about 0.4 | 0.4–0.8 |

Conflict: the knowledge base and earlier versions of the pipeline file gave one bevel width per size class (0.05 studs for props, 0.15 for architecture); LihFolk sizes by viewing distance and the pixel table agrees. Trust distance: a 0.05-stud bevel on a prop seen from 40 studs is under 1 px and only costs triangles. As a sanity band, 1–2% of the object's size reads crisp and manufactured, 3–6% soft and toy-like, over 8% pillow-like, under 0.5% invisible `[lihfolk]`.

| Type | Segments | Cost on a box (measured, Blender 5.2.3) | Use |
|---|---|---|---|
| Chamfer | 1 | 12 → 44 triangles | Faceted styles, architecture, anything far or repeated |
| Soft bevel | 2 | 12 → 108 | Stylised props and characters near the camera |
| Round bevel | 3 | 12 → 188 | Hero pieces whose curve shows in the outline |

- Bevel modifier settings to set explicitly (the defaults are not game defaults): Width type Absolute, Limit Method Angle 30°, Clamp Overlap on, Harden Normals on, then a Weighted Normal modifier (Face Area, weight 50, Keep Sharp on), Shade Smooth, and Triangulate last. Apply scale before bevelling or widths come out uneven.
- Bevel outer corners; leave inner corners sharp. One width per size band, written in the bible.
- Flat faces that darken toward their edges (an "inflated" look) mean smooth shading is averaging across the bevel: Harden Normals or Weighted Normal fixes it. Check with a matcap; they exaggerate normal errors.
- Clean geometry first, edit normals last: Merge by Distance after a normal edit destroys it `[lihfolk]`.
- Lumpy "popcorn" tree canopies: each blob shades as its own sphere. Add a Data Transfer modifier copying custom normals from a single enclosing proxy sphere so the canopy shades as one volume `[lihfolk]`.
- Edge highlight without geometry: brighten edges in vertex colour (keep the range 0.75–1.0 or it turns into streaks), a separate lighter trim piece, or a lit-edge strip in the palette. Inverted-hull outlines double the triangle count; avoid them in game meshes `[lihfolk]`.
- Bevels vanish under flat ambient light. If they read in Blender and not in game, check the lighting before widening them.

## Spending triangles where the camera looks

Triangles are worth only what they change on screen: the outline first, shading across curves second, separate colour regions third `[lihfolk]`.

Segments for a round cross-section so the outline is within one phone pixel of a true circle (sagitta rule: `n ≥ π / acos(1 − d / (520 r))`):

| Radius | Seen from 8 studs | 15 | 40 | 100 |
|---|---|---|---|---|
| 0.25 studs (handle) | 9 | 7 | 4 | 3 |
| 1 stud (barrel, limb) | 18 | 13 | 8 | 5 |
| 3 studs (tower, crown) | 31 | 23 | 14 | 9 |
| 10 studs (dome) | 57 | 42 | 26 | 16 |

Only the silhouette needs that count; interior loops can be half. Practical bands: rivets 4–6 sides, grips 6–8, barrels and posts 8–12, large visible curves 12–24. A deliberate hexagon with chamfers often scores better than a "round" prop stuck at 16 uneven steps `[lihfolk]`: make the polygon a decision.

Delete: bottom faces and the bottom bevel ring of grounded props (up to a fifth of a small prop), faces buried in other meshes, interior faces (Select All by Trait > Interior Faces), backs against map edges the camera cannot reach, and anything under 1 px at its closest normal distance. Add: the top silhouette and one focal feature.

```python
# Tested on Blender 5.2.3. A bevelled cube returns (44, {'up': 19, 'down': 19, 'side': 62}); a grounded prop should show ~0 down.
import bpy, bmesh
from mathutils import Vector, kdtree

def spend_report(obj):
    bm = bmesh.new(); bm.from_object(obj, bpy.context.evaluated_depsgraph_get()); bmesh.ops.triangulate(bm, faces=bm.faces[:])
    area = {"up": 0.0, "down": 0.0, "side": 0.0}
    for f in bm.faces: area["up" if f.normal.z > 0.5 else "down" if f.normal.z < -0.5 else "side"] += f.calc_area()
    total, tris = sum(area.values()) or 1.0, len(bm.faces); bm.free()
    return tris, {k: round(100 * v / total) for k, v in area.items()}

def symmetry_error(obj):  # worst X-mirror mismatch as a fraction of the largest dimension; 0.0 on a mirrored build
    vs = [v.co.copy() for v in obj.data.vertices]; kd = kdtree.KDTree(len(vs))
    for i, co in enumerate(vs): kd.insert(co, i)
    kd.balance()
    return max(kd.find(Vector((-co.x, co.y, co.z)))[2] for co in vs) / max(obj.dimensions)
```

- **GPU vertices, not just triangles** `[lihfolk]`: every sharp edge and UV seam splits vertices. Fully flat shading costs about three vertices per triangle; put sharp edges where the UV seams already are so the split happens once. A dense faceted forest can cost more memory than a smooth one.
- **Topology matters only where it bends**: static props need clean shading and no long thin triangles (keep aspect under about 8:1); skinned meshes need three or more loops at hinges, five at shoulders and hips, and poles kept on rigid areas (details in animation-and-rigs.md).
- **Scene share** `[lihfolk]`, rule of thumb per zone: hero landmarks 15–25% of triangles, path-side props within 25 studs 30–40%, interactables 15–20%, background 15–25%, skyline 5–10%.

## Colour and value

Value first, hue second: a zone where every colour sits at mid value looks muddy however pretty each swatch is.

| Role | Value (HSV 0–100, under game lighting) | Saturation |
|---|---|---|
| Ground and floors | 35–60: avatars in black or white must both separate from it | Low to medium |
| Walls and big structures | One band away from the ground | Medium |
| Props | Inside the structure band, varied by hue | Medium |
| Interactables | The lightest band or a saturation spike that nothing else shares | High |
| Enemies and NPCs | At least one band (about 20 points) from the ground | High |
| Glow | Above everything, small area | High |

- **Budget per prop**: 2–3 dominant colours plus one accent on the focal feature; more than four reads as busy at Roblox distances. Per zone 8–16 colours on a shared base of 12–20 neutrals, trims and metals; whole game 60–120 `[lihfolk]`. Do not give interactables colours that avatars commonly wear.
- **Ramps**: never mix shadows toward black or highlights toward white. Shadow step: hue 10–25° toward blue-violet, saturation up slightly, value down 20–30. Lit step: hue 10–20° toward yellow, saturation down a little, value up 10–20. Halve the shift under a strongly blue ambient or shadows turn purple `[lihfolk]`.
- **Colour script** `[lihfolk]`: one 200×120 px thumbnail per zone in play order (sky band, ground band, one structure, one focal glow), each with a key-light colour, shadow hue, dominant hue, accent and value key. Neighbouring zones must differ in at least two of hue, value key and saturation.
- **Check in greyscale**: add a temporary `ColorCorrectionEffect` with `Saturation = -1` in Studio and screenshot from the gameplay camera; remove it before publishing. Pick colours under the game's lighting, never in a neutral picker.

Choosing how colour reaches the mesh (the pipeline file's "Texturing strategy" covers the texture side):

| | Flat colour per part | Palette or gradient atlas | Vertex colour |
|---|---|---|---|
| MeshParts for a 3-colour prop | 3 | 1 | 1 |
| Recolour a whole zone | Script over instances | Swap one image | Re-export, or multiply `Color` |
| Gradients | No | Along a strip | Between vertices |
| Survives decimation | Yes | Mostly | Poorly: colours smear |
| Main risk | Instance count | Swatch bleed at distance | Locked-in noise you cannot fix in Studio |

For 300 scattered props averaging 2.5 colour regions, flat colour means about 750 MeshParts against 300 `[lihfolk]`: use flat colour for large one-colour architecture and Neon glows, an atlas for multi-colour props, and vertex colour for grey ambient occlusion only (range 0.7–1.0, never tinted).

Gradient strips `[lihfolk]`: each palette column is a vertical ramp, bottom 15% contact shadow, middle 70% body across about three value steps, top 15% highlight. Keep the whole ramp under 40 value points or meshes look striped. Unwrap by Project from View (front), scale the island to zero width, and slide it onto the strip so height on the model picks the shade. Strips 8 px wide for close props, 16 px for anything seen far away; UVs 2 px inside the strip; neighbours ordered by similarity; PNG never JPG; material SmoothPlastic so no built-in pattern smears over collapsed UVs. Freeze the layout and version it: moving one strip breaks every mesh that uses it.

## Untextured, faceted and voxel styles

**Faceted or smooth** `[lihfolk]`: facet rocks, cliffs, crystals and canopies; keep characters, pets, pickups and cloth smooth (skinned flat faces flicker). Size facets in pixels: for a rock seen from 25 studs (about 21 px per stud) facets of 0.5–0.8 studs read; the same facets on a mountain become static. Rock recipe: icosphere with 2 subdivisions (1 is only 20 faces), scaled wider than tall, three or four vertices pulled by hand to make a top plane and a heavy side, Decimate Collapse to 60–120 triangles then Planar at 5–10°, base flattened and sunk 0.2 studs, Shade Flat, one-segment chamfer on the big edges. Make 4–6 variants by changing the pulled planes, not the noise seed; scatter at random yaw and 0.8–1.3 scale. Faceting disappears under flat ambient light: keep the sun 30–50° up or jitter value per face.

**Voxel style** `[lihfolk]`:
- Cell sizes are binary fractions of a stud (1, 0.5, 0.25, 0.125) and every grain divides the largest, or tiles crack and pets hover. Typical: 0.5 for buildings and tiles, 0.25 for avatar-scale characters and props.
- A cell needs about 3 px: at 40 studs a 0.25-stud cell is 3 px and a 0.125 cell is 1.6 px, which shimmers.
- Never ship per-cell cubes: a solid 32³ block is 393,216 triangles as cubes, 12,288 with hidden faces removed and 12 after merging coplanar same-colour faces (greedy meshing). Merged rectangles can leave T-junctions that sparkle at grazing angles; split long edges or cap rectangle size.
- Shade Flat and export normals, or cubes come out rounded and dark. Bevel geometry on cells triples triangles for nothing; paint the top-edge cells one palette step lighter instead.
- Tiles: 4-stud modules with even cell counts, decoration kept one cell inside the footprint, 1-stud height steps (characters climb those smoothly).
- Characters: chibi 2–2.5 heads tall, toy 3–4, heroic 5–6; faces at least 6 cells across and limbs 2 cells thick; rigid parts with cap or sleeve joints, never smooth skin weights.
- Conflict: LihFolk authors voxels in MagicaVoxel, Goxel or Blockbench. House rule 1 keeps Blender as the authoring tool. Blender-native route, tested on 5.2.3: Remesh modifier in Blocks mode (a radius-2 sphere at octree depth 4 gave cells of about 0.25 studs and 2,316 triangles), then a planar Limited Dissolve delimited by material (1,312 triangles), then Triangulate and Shade Flat. Set object size and octree depth so the cell lands exactly on the grid.

## Recipes and budgets

Budgets are target / ceiling per asset, counted after modifiers. Going over target needs a written reason `[lihfolk]`; the hard limit is 20,000 per mesh `[official]`.

| Class | Target / ceiling | Recipe notes |
|---|---|---|
| Clutter (hand-sized) | 150 / 300 | Often better deleted or enlarged; group several into one mesh |
| Small repeated prop (crate, barrel, lamp) | 600 / 1,500 | The budget that matters most: it is multiplied by every copy in view. Bottoms deleted, 8–12 sides |
| Medium prop (stall, cart, statue) | 2,000 / 5,000 | One focal feature (awning, sign). Join the planks; do not ship 110 parts |
| Rock | 400 / 1,000 | Faceted recipe above |
| Tree | 2,000 / 5,000 | Trunk and canopy as two meshes (trunk solid, canopy `NonSolid`); canopy from 3–8 blobs, never alpha cards |
| Held weapon | 2,500 / 5,000 | Below |
| Kit module (wall, floor, roof) | 800 / 3,000 | Below |
| Building (sum of modules) | 6,000 / 10,000 | Split into modules sharing one bottom-centre origin |
| Vehicle | 8,000 / 15,000 | Body, wheels, glass, interior: at most 4 meshes; wheels separate so they spin; segments from the sagitta table |
| Creature or NPC | 5,000 / 10,000 | Below |
| Boss | 10,000–30,000 total | Several meshes, each under 20,000 |
| Hero landmark | 10,000 / 20,000 per mesh | Seen from everywhere: spend on the skyline shape |

- **Weapon** `[lihfolk]`: origin at the grip centre, blade or shaft along +Z, cutting edge toward −Y, scale applied; split by role (Handle, Guard, Blade, Glow) and by motion. Stylised proportions: haft radius 0.18–0.23 studs, head about a third of total length, shorter haft tapering toward the head. Build the blade from a cross-section loop with a flat rounded edge (a one-point edge renders as a razor ribbon) and let the point come from the profile curve, not a taper. Guards and pommels are extruded, bevelled silhouettes, not tubes and balls. Give small round parts their own, higher lathe resolution than the grip. A glowing edge is a few pixels wide in third person: the read is colour and outline. Reserve flames and ornate guards for the top tier so rarity stays readable.
- **Modular building** `[lihfolk]`: pick the grid first (4 studs suits most buildings for default avatars; 8 for scaled-up characters). A minimal kit: straight walls 4 and 8 wide by 12 tall by 1 thick, inner and outer corners, door wall, window wall, end cap, floors, stairs, pillar, top and base trims, roof pieces. Pillars and trims hide seams. Cut real openings so interiors work later. Roofs sag slightly, posts lean 2–4°, plank widths vary 15–30%, but parts that touch stay within a degree of each other or gaps open. Run a floating-shell check on the whole building: one hovering plank spoils it.
- **Creature** `[lihfolk]`: decide skinned (organic bending) or rigid segments (toy, robot, armour) before modelling, and model in an A-pose facing −Y. Scripted route that works: loft cross-sections traced from a side view, add limbs as tubes, fuse with a voxel remesh, decimate to budget with symmetry on, then triangulate, dissolve at 5° and triangulate again for facets. Grow appendages out of the main mass by extrusion; do not float primitives beside it. Wings as two or three layered plates, not individual feathers. One exaggerated feature. Fins and other thin parts need a half-thickness of at least 0.6 of the quad edge or they fold.
- **Cute pet (chibi)** `[lihfolk]`: smooth, round, no neck, bottom-heavy; eyes below the middle of the head, large, with iris depth and two catchlights; nothing pointing up unless you want horns. Express rarity with accessories and effects, not a spikier style. Judge from behind and above, where pets are actually seen.
- **Character**: build on an R15 proxy with joint geometry centred on the R15 pivots; proportions, skinning, cages and the three routes (avatar body, R15-compatible, custom rig) are in `references/animation-and-rigs.md`.

Mechanical gates for scripted or generated-by-script assets `[lihfolk]`, run after modifiers are applied and before anyone reviews: symmetric-by-design shapes are built as half plus mirror and measure ≤ 1% symmetry error; emblems, gems and guards are centred by bounding-box or centroid maths within 2%, never by eye, and seated on their surface; accents are built from the parent's own vertices; no self-intersections; concave caps (stars, gears) are ear-clipped, not beauty-filled; no floating shells. A gate failure caps the rubric at 5. Directional light makes symmetric shapes look lopsided: trust the number.

## Concept to model

1. **Brief** (five lines): role and gameplay job, viewing band, size in studs with the origin position, class budget, style words plus the one exaggerated feature.
2. **Reference board**: three images marked on target, too realistic and too blocky `[lihfolk]`, plus the golden sample from the style bible. Use references for shape and mood; never trace or lift another game's asset.
3. **Concept sheet**: orthographic front, side and back at one scale so proportions can be measured, one three-quarter view for feel, the size in studs written on it, part names exactly as they will appear in Studio, one flat colour per part. Remember the sheet shows eye level; the game shows the model from above and behind.
4. **Blockout** in Blender at final scale beside the proxies, big then medium then small shapes, grey. Export it and look at it in the place before any detail: a silhouette fix costs minutes here and hours later.
5. **Mid pass**: final shapes and rough colour, no bevels. **Final**: bevels, detail, technical cleanup.

| Checkpoint | Review only | Typical time before review `[lihfolk]` |
|---|---|---|
| Blockout | Purpose, silhouette, proportion | 15–60 min |
| Mid | Value, colour, shape grammar | 1–4 h |
| Final | Edges, detail placement, technical | Remainder |

Critique in a fixed order and stop at the first level that fails `[lihfolk]`: purpose, silhouette, proportion, value, colour, edges, detail, technical. Feedback names what, where, why and how much, with a paintover (line, shape-fill, value or colour; 2–30 minutes) drawn slightly stronger than needed because fixes get applied at half strength. Review in-game screenshots from the follow camera at 15 and 40 studs on a 19.5:9 frame, beside neighbouring assets, never Blender renders alone. When a note names one spot, fix the principle across the whole model. If a reviewer liked a version, lock it before trying a recomposition.

## Quality rubric (0–10 per asset)

Score each line 0, 0.5 or 1 from in-game screenshots and the silhouette sheet. Ship at 8 or more with no zero; hero and store-front assets need 9. Any failed mechanical gate or acceptance-checklist item caps the score at 5 `[house]`, structure adapted from `[lihfolk]`.

| # | Criterion | 1 point when |
|---|---|---|
| 1 | Role | A new player can say what it is and whether it can be used, at its normal distance |
| 2 | Silhouette | Passes all four views at game pixel height and the roster test |
| 3 | Hierarchy | Clear big, medium, small; one focal feature |
| 4 | Proportion | Confident exaggeration in pairs; correct against both avatar proxies |
| 5 | Value and colour | On palette, 2–3 colours plus accent, separates from its background in greyscale |
| 6 | Edges | Bible bevel widths, readable at distance, no gradients on flat faces |
| 7 | Shading and surface | No artefacts, flipped faces, z-fighting or stray vertex colour |
| 8 | Triangle economy | Within class target; nothing under 1 px; no hidden faces; wireframe is not a solid mass |
| 9 | Kit fit | Indistinguishable in style from the golden sample beside it |
| 10 | In-game read | Holds up under final lighting at graphics level 1–3 on a phone |

Kits: score one representative piece per family plus every hero piece. Have someone who did not build it score it from the screenshots alone `[lihfolk]`.

## First kit walkthrough (beginner)

Goal: a crate, barrel, lamp post and fence section that look like one family and import cleanly.

1. **Scene**: Scene Properties > Units > Unit System None. Add the two avatar proxies (boxes 5 and 6.5 tall) in a `Scale_Ref` collection. Add the 70° camera described above.
2. **Palette**: pick six colours (two woods, a metal, a dark, a light, one accent). Write the hex values down. Nothing else is allowed.
3. **Crate** (2.5 studs): add a cube, size 2.5. Tab into Edit Mode, select the four side faces, `I` to inset 0.3, `E` to extrude inward 0.1. Tab out, `Ctrl+A` > Scale. Add a Bevel modifier (Width 0.08, Segments 1, Limit Method Angle 30°, Harden Normals on), a Weighted Normal modifier and a Triangulate modifier; right-click > Shade Smooth. Delete the bottom face.
4. **Barrel** (3 tall, radius 1): add a cylinder with 12 vertices. `Ctrl+R` two loop cuts, scale the middle loops out 10% for a bulge. Select two edge rings and bevel them into raised hoops 0.15 wide, extruded out 0.05. Same three modifiers. Delete the bottom cap.
5. **Lamp post** (9 tall): a 0.6-stud square post that tapers, a chunky lantern about 2.5 studs tall (half an avatar is correct), a cap wider than the lantern. Add an Empty named `Light_Att` at the bulb; it imports as an Attachment for the PointLight.
6. **Fence section** (4 long): posts 0.6 thick, two rails 0.4 thick, gaps of at least 0.6. Origin at one bottom end so sections snap.
7. **Colour**: assign palette colours by material while modelling, then collapse to one material with the palette method in art-pipeline-blender.md.
8. **Origins and names**: bottom-centre for crate, barrel and lamp post (`SM_Prop_Crate_A` and so on). Add a custom property `Fidelity` = `Box` (crate, fence) or `Hull` (barrel, lamp post).
9. **Check**: render the silhouette sheet. Can you tell the four apart at 64 px from the top view? If the barrel and crate blur together, exaggerate the hoops and the crate's frame.
10. **Export and import** with `tools/export_kit.py` and the importer preset in art-pipeline-blender.md. Set `MeshPart.Color` to white if you used vertex colour. Walk into each piece, jump on it, then view all four from 15 and 40 studs in the phone emulator.
11. **Score** each on the rubric. Fix the lowest line on every piece before making a fifth asset.

Common first-kit mistakes: bevelling before applying scale, 32-segment default cylinders, real-world thin rails, a different bevel width on each piece, colours picked by eye, judging in the Blender viewport instead of in game.

## Level-up: craft symptoms → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Looks good in Blender, tiny or mushy in game | Judged close up with a wide lens | Matched 70° camera at real distances; Studio pixel script |
| Players confuse two enemy types | Same primary shape, different colour only | Change one primary or large secondary shape; roster test |
| Rare and common items look alike | Upgrade adds trim or colour only | Add an outline-changing element (crest, floating piece) |
| Trims and rails flicker or vanish | Real-world thickness | Size from the pixel table, at least `d / 170` |
| Model looks "fat", not stylised | Everything scaled up | Exaggerate in pairs |
| Budget met but the model looks plain | Triangles spread evenly | Move them to the top silhouette and one focal feature |
| Heavy cylinders and wheels | Default 32 segments | Sagitta table; delete hidden caps |
| Zone looks muddy | No value structure | Value bands; greyscale check |
| Players cannot find the chest or exit | Interactables share a value band with scenery | Reserve the lightest band or a saturation spike |
| Dead grey shadows, chalky highlights | Ramps mixed toward black and white | Hue-shifted ramps |
| Rocks look like noise blobs | Facets too small and all one size | Size facets in pixels; big planes plus a few small edge facets |
| Library drifts over months | Rules are adjectives; no golden assets | Numbers in the bible, 3–5 golden assets, side-by-side review |
| The same notes come back every round | Detail critiqued before silhouette | Fixed critique order; stop at the first failing level |
| Scripted assets subtly lopsided or with floating bits | Placement by eye | Half-plus-mirror, centring by maths, seating and floating-shell gates |

## Review gate

- [ ] Brief, reference board and (for characters and hero pieces) a concept sheet exist before modelling.
- [ ] Blockout reviewed in the place at final scale beside both avatar proxies.
- [ ] Four-view silhouette sheet and roster test passed at game pixel height.
- [ ] Feature sizes, bevel widths and segment counts taken from the distance tables, and written in the style bible.
- [ ] Value bands planned; greyscale check done under game lighting; palette respected.
- [ ] Within class target, or the reason is written down; bottoms and hidden faces removed.
- [ ] Mechanical gates passed for scripted assets.
- [ ] Rubric score 8 or more with no zero, given by someone other than the author, from in-game screenshots.
- [ ] Asset then passes the acceptance checklist in `references/art-pipeline-blender.md` (collision plan, naming, export, upload).

## Sources

Accessed 2026-11-10.

- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `55 Modelling Nuance and Readability/` (Modelling to the Roblox Camera and Player Scale; Proportion Exaggeration and Gameplay Distance; Shape Language and Silhouette Testing; Spending Triangles Where the Camera Looks; Bevels Chamfers and Edge Highlights Without Textures; Style Bibles for Consistent Models; Critiquing a Model - Paintovers and Iteration; Art-Direction Nitpicks - The Principles Behind Them), `54 Untextured Stylised Modelling/` (Flat Colour vs Gradient Atlas vs Vertex Colour; The Gradient Palette Texture Workflow; Colour Scripts and Value Structure for Untextured Art; Faceted Low-Poly - Flat Normals and Facet Size; Clean Stylised Shading - Weighted and Custom Normals), `53 Voxel Modelling Deep Dive/` (scale grids, palettes, shading, meshing, characters, props and tiles), `14 3D Modeling/` (Modeling Fundamentals for Games; Low-Poly and Stylized Modeling; Topology and Edge Flow; Hard-Surface Modeling; Modeling Weapons and Props; Organic and Creature Modeling; Mesh Optimization for Mobile; Modular Environment Kits; Procedural Model Kits - Lessons; Mesh Gates for Generated Models), `45 Procedural Blender Assets/` (worked-example notes only; no `.blend`, `.fbx`, `.glb` or renders used), `19 Concept Sheets/Concept Sheets.md`, `skills/roblox-blender-modeling/SKILL.md` and `references/quality-research.md` (read; tables and headings skimmed, wording rewritten)
- https://github.com/Roblox/creator-docs (read, commit of 2026-11-07): `reference/engine/classes/Camera.yaml` (FieldOfView default 70, vertical), `Humanoid.yaml` (jump height 7.2, walk speed 16), `art/modeling/specifications.md` (20,000 triangles)
- Blender 5.2.3 LTS `bpy` (ran: bevel triangle costs, `silhouette_sheet`, `spend_report`, `symmetry_error`, Remesh Blocks plus planar dissolve). The pixel, field-of-view and sagitta tables were recomputed from the formulas, and match LihFolk's to rounding.
- Not verified in Studio: the Luau measuring snippet, LihFolk's follow-camera distance and pitch figures, and its 720 px phone render height (all rules of thumb there too).
- Rejected from LihFolk: anything relying on its Asset Pack or bundled rigs, voxel authoring outside Blender, Part-based blockouts in the shipping place, and non-colliding decoration as a default (see the conflict notes in art-pipeline-blender.md).
