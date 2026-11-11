# VFX and juice: principles, particles, beams, meshes, timing, shake, replication, budgets, safety

What this is: the build-level reference for visual effects and game feel on Roblox: what makes a stylised effect readable, every effect instance and its traps, texture and mesh authoring, timing in milliseconds, hit-stop and camera work, the client-only replication pattern, pooling, budgets for a 3 GB Android phone, and motion and flash safety. Open it when building an effect or auditing why a game feels flat, laggy, unreadable or generic. Effect-by-effect builds are in `vfx-recipes.md`; viewed reference images and tutorials are in `visual-library/vfx.md` and `visual-library/vfx-learning.md`. It extends `game-craft.md` §1 (feedback tiers; §1.3 holds the shake module) and `core-loop-tuning.md` §8 (juice ordered by build cost); neither is repeated here. UI pops and reward sequences are in `ui-motion-and-feedback.md`; sound in `audio-sfx-music.md`; comfort settings in `accessibility-and-player-qol.md`; frame budgets in `performance.md`; animation markers in `animation-and-rigs.md` §6.

Tags: `[official]` Roblox docs (mirror commit 7cbffff, 2026-11-10; re-checked 2026-11-11) and staff posts, `[community]` practice from named artists on realtimevfx.com, 80.lv and the DevForum (named in Sources), `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its numbers come from one production combat game and are starting points, not laws), `[VS]` version-sensitive, `[house]` house estimate. Terms: *VFX* = visual effects; *juice* = small non-gameplay responses that confirm an action; *emitter* = `ParticleEmitter`; *additive* = colours add to what is behind (glow); *value* = how light or dark a colour is, ignoring hue; *overdraw* = the same pixel drawn several times by stacked transparent layers; *telegraph* = a warning drawn before an attack lands; *block-in* = a first version built from plain white shapes.

## Contents

Start here by level · Fast routes · 1. Principles of readable stylised effects · 2. Instances and ParticleEmitter · 3. Beam, Trail, Attachment · 4. Highlight · 5. Meshes and textures (Blender) · 6. Timing and ability anatomy · 7. Hit-stop, shake, FOV · 8. Screen effects and number popups · 9. Tween or spring · 10. Replication · 11. Pooling, budgets, quality scaling · 12. Reduced motion and flash safety · 13. Juice ladder by frame cost · 14. Generic tells and fixes · 15. Level-up table · 16. Critique rubric · Review gate · Sources

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Every effect runs in a LocalScript; the server only sends "what happened". (2) Emitters stay `Enabled = false`; fire them with `:Emit(n)`. (3) Set `LightInfluence = 0` on every emitter. (4) Build the effect in white first: one flash, one shape, a few sparks, a sound; add colour last (§1). (5) Add a shake slider and honour Reduce Motion before shipping any shake | Flipbooks, mesh VFX, governors, hit-stop budgets |
| Intermediate | Write each effect as a layer table (§6) with primary, secondary and tertiary roles (§1). Paint your own greyscale textures (§5). Pool effect roots. One dark layer under every bright stack. Play the caster's effect on input and skip the echo. Tie effects to animation markers, not timers | Per-client particle governors, catch-up hit-stop |
| Expert | Keep a style guide and a 0–10 importance sheet per ability and per viewer (§1). Budget per cast, per caster window and per client; never cull gameplay information. Catch-up hit-stop, FOV-normalised shake. Score every effect with §16 on a hot phone with 8 casters at one spot | — |

## Fast routes

For the commonest tasks read only these sections, in this order (§N = the section numbered N in that file; "top" = the lines above its first numbered section). Sheets are `assets/reference/NN-*.png`, opened with the Read tool; library rows are in `visual-library/`.

| Task | Read exactly | Look at |
|---|---|---|
| Make one effect from a recipe | `vfx-recipes.md` top, Conventions, your recipe, Review gate; this file §2 (and §3 if it uses a beam or trail), §6, §10, §16 (about 250 lines) | Sheets 11, 12; `vfx.md`: the "Start here" rows of the section for your effect |
| Make a hit feel heavier | This file §6, §7; `game-craft.md` §1, §1.3; `vfx-recipes.md` top, Conventions, recipe 3 (recipe 4 for a ground slam); `audio-sfx-music.md` §5 up to its code block (about 330 lines) | Sheets 10, 21; `vfx.md` rows 25, 30, 16 |
| Fix effects that look cheap | This file §1, §5, §6, §14, §15, §16; `vfx-recipes.md` Conventions and the recipe for the effect (about 250 lines) | Sheets 12, 11; `vfx.md` rows 1, 8–9, 16 and 52–55; `vfx-learning.md` row 5 |
| Add sound to an action | `audio-sfx-music.md` top, §2 (skip if the bus graph exists), §3, §5, §6, §13 (about 235 lines, 175 without §2) | Sheet 10 (sound on the heavy-hit timeline); `audio-and-sound.md` rows 1, 13, 17, 32–33 |
| Build a UI or reward sound set | `audio-sfx-music.md` top, §9, §5 "Variation", §6, §14, §3, §11, §2 (skip if the bus graph exists); `ui-motion-and-feedback.md` §5; `vfx-recipes.md` recipe 16 (about 255 lines, 200 without §2) | Sheet 08; `audio-and-sound.md` rows 30, 33, 44 |
| Cut effect cost on phones | This file §11, §13, §2, §4, §8; `performance.md` "Frame budgets and device targets", "VFX, animation and audio budgets"; `audio-sfx-music.md` §10; the Budget line of each recipe you use (about 260 lines) | Sheet 11 (low-tier pictures); `vfx.md` row 51; `vfx-learning.md` rows 18, 26 |

## 1. Principles of readable stylised effects

An effect has three jobs **in this order**: communicate gameplay without clutter, carry the theme, delight. When they conflict, the earlier one wins `[community]` (Riot's ordered goals). A stylised effect is a few designed shapes on a short timeline, not many particles.

| Tool | Rule | How to check |
|---|---|---|
| Shape and silhouette | Block the effect in with plain white and grey shapes: no colour, flipbook or glow. If the block-in has no punch, polish will not add it; if it has, the finished effect keeps it `[community]` (Keyser). Sharp, spiky shapes read as threat; round, soft shapes read as friendly: a heal has no sharp shapes `[community]` (Riot). Draw irregular: spokes at uneven angles and lengths, no even scallops | Greyscale screenshot at phone size: can you name the effect from the outline? |
| Value before hue | The area of focus holds the lightest **and** darkest values side by side, the highest saturation and the sharpest edges; everything else is lower in value, saturation and sharpness `[community]` (McDonald). A glow needs a shadow: brightness is clamped at 1, so over a mid-grey floor (0.5) a glow has 0.5 of headroom; darken behind it to 0.2 and it has 0.8 `[community]` (Leroy) | Desaturate and squint: exactly one bright spot, with dark next to it |
| Primary, secondary, tertiary | Primary = the part that carries gameplay (projectile head, blade arc, AoE rim) and matches the hit volume exactly. Secondary = theme (trail, motif, element body). Tertiary = sparks, dust, linger. Ask of every layer: is it primary; how much attention should it take; how does it appear and leave; does it add noise `[community]` (Jevremović). If everything is important, nothing is | Hide the secondary and tertiary layers: gameplay must still read |
| Timing | Three stages. **Anticipation**: length set by game design, low contrast. **Climax**: all layers at once, highest contrast and saturation, very short (a hit frame of about 100 ms). **Dissipation**: low contrast, low opacity, gone quickly `[community]` (Jevremović, Leroy). Curves are never linear: size reaches most of its final value in about 4 frames then eases; brightness peaks for 1–3 frames then drops `[community]`. In the references viewed, the bright phase is 15–25% of the total and the rest is quiet dissipation `[house]` | Step a capture frame by frame (`,` and `.` on YouTube); compare with a reference |
| Importance | Rate each ability 0–10 for three viewers (caster, enemies, allies) and scale size, brightness, sharpness and timing to the number. 0 means that viewer does not see it: a range ring matters to caster and target, not to allies `[community]` (Riot hierarchy sheet) | The rarest, most dangerous move is the loudest; basic attacks are the quietest |
| Identity and language | Each ability gets 2–3 unique identifiers (a shape, a motif, a motion) that survive a recolour. Shared mechanics share a look across the game: roots = ring plus cage, shields = lines panning downward, knock-ups = strong verticals, heals = green and soft `[community]` (Riot) | A skin or rarity recolour is still recognised in a glance |

- **Retime, do not rebuild.** The same layers played slowly with low contrast read as a friendly spell; played fast with darks pressed against whites they read as damage `[community]` (Keyser).
- **Less is more** is a budget: one ground piece, one body, one core, one accent hue (numbers in §6). Add a layer only if removing it would lose information or the theme.

**Colour script by element.** Ramp runs dark → body → hot; white is only ever the thin core (example hex per row: `vfx-recipes.md` Conventions). Secondary elements and motion carry the element as much as hue does `[community]` (Jevremović's element table) `[lihfolk]`.

| Element | Ramp (dark → body → hot) | Secondary elements | Motion |
|---|---|---|---|
| Fire | Deep red-brown → orange → yellow-white | Smoke, sparks, embers | Chaotic, rising |
| Water | Navy → cyan-blue → white foam | Waves, foam, droplets | Wave, arcing and falling |
| Ice | Deep blue → pale cyan → white | Shards, mist, sparkles | Snap, then still |
| Lightning | Blue-black → electric blue or yellow → white | Sparks, small blast | Forking, 1–3 frame steps |
| Earth | Dark brown → ochre → dusty cream | Rocks, dust | Snap up, heavy fall |
| Nature, heal | Deep green → leaf green → yellow-white | Leaves, petals, soft motes | Growth, slow rise |
| Arcane | Indigo → magenta or violet → pink-white | Runes, rings, sparkles | Orbiting, converging |
| Dark, poison | Black-purple or black-green → saturated purple or acid green → pale tint | Liquid, fumes, bubbles | Dripping, creeping |
| Light, holy | Warm brown-gold → gold → white | Rays, sparkles | Radiating, descending |

- **Friend or foe.** In team modes the side must read before the element. Reserve one hue pair for allegiance (for example blue = ally, red = enemy, as Brawl Stars does `[community]`) and apply it to the primary layer only: ground ring, projectile rim, telegraph fill. The element lives in the secondary layers. Never rely on red versus green alone: pair hue with shape (enemy telegraphs spiky or dashed, friendly zones smooth) and value (`accessibility-and-player-qol.md`) `[house]`.
- **Busy or changing backgrounds.** Additive layers vanish on snow, sand and sky and wash out on bright floors. An opaque or alpha-blended flat body with a darker inner shape reads on any ground; that is how Supercell handles desert, snow and mine maps with plain quads `[community]` (Woo). Test on the lightest and darkest floor in the game.
- **Phone size.** Thin or small detail turns into shimmering noise `[community]` (Woo, on electricity). At the game camera on a small phone, any feature under about 6 px is gone: thicken lines, drop tiny sparks, enlarge the primary shape `[house]`.

## 2. Instances and ParticleEmitter

| Need | Use | Why |
|---|---|---|
| Sparks, smoke, flashes, dust, rain, pickup pops | `ParticleEmitter` | Camera-facing or velocity-aligned quads; cheapest to author |
| A line or ribbon between two points: laser, tether, guide arrow, flowing surface, ring outline of constant width | `Beam` | Cubic Bézier ribbon with a scrolling texture (§3) |
| The path something just travelled: blade, dash, projectile | `Trail` | Records two attachments each frame |
| "This object matters": interactable, target, ally through walls, hit flash | `Highlight` | Outline and fill on a whole model; strict rules in §4 |
| A designed silhouette: crescent, shock ring, dome, pillar, shards, telegraph disc | Blender mesh (`MeshPart`) tweened on the client (§5) | House rule 1: authored in Blender |
| Light on the scene from the effect | `PointLight` in an Attachment, `Shadows = false`, one per effect | Particles never light the world, even at `LightEmission = 1` `[official]` |
| Whole-screen response | GUI overlay or a post effect on the Camera (§8) | Post effects on `Workspace.CurrentCamera` show for that player only `[official]` |
| Runtime-generated images or meshes | Avoid: bake offline and upload | Loading an existing asset into `EditableImage`/`EditableMesh` needs asset permission, and clients have strict memory budgets for them `[official]` `[VS]` |

**ParticleEmitter.** Parent to a `BasePart` (particles spawn in its box or `Shape`) or to an `Attachment` (spawn at a point; rotate the attachment rather than using `EmissionDirection`). With the default camera scripts, emitters, beams and trails (also `Fire`, `Smoke`, `Sparkles`, `Explosion`) parented inside a character are hidden for that player in first person (since September 2024). To keep one visible, put it on a helper part parented **outside** the character model and welded to it (`WeldConstraint`, `Massless`, `CanCollide`/`CanQuery` false) `[official]` `[VS]`.

| Property | What it does | Trap or tip |
|---|---|---|
| `Texture` | Sprite. Transparent PNG, or greyscale on black with `LightEmission = 1` `[official]` | Author white and grey; tint with `Color` so one texture serves every element (§5) |
| `Color`, `Transparency`, `Size` | Sequences over each particle's life (at most 20 keypoints `[VS]`); a number-sequence keypoint envelope randomises `Size` or `Transparency` per particle `[official]` | `Color` multiplies the whole sprite: it cannot recolour light and dark areas separately. Punchy growth reaches about 80% of final size by 35% of life `[lihfolk]` |
| `Squash` | Above 0 thinner and taller, below 0 wider and shorter `[official]` | With `VelocityParallel`: embers, rain streaks, speed lines. The docs' rain recipe uses a **negative** value there to stretch along the direction of travel `[official]`; confirm with an arrow texture |
| `LightEmission` | 0 normal blend, 1 additive; with additive, darker colours look more transparent `[official]` | Additive layers sum to white. Dense matter (water, smoke, debris) stays at 0 |
| `LightInfluence` | 0 ignores scene light, 1 lit like a part. Defaults to 1 when inserted in Studio but 0 from `Instance.new` `[official]` | Set 0 explicitly or the effect goes black in caves and grey in shade |
| `Brightness` | Scales emitted light when `LightInfluence = 0` `[official]` | Bigger sprite on screen = lower brightness; tiny specks need several times more `[lihfolk]`. Official volcano values: embers 20, ripples 15 |
| `Orientation` | `FacingCamera`, `FacingCameraWorldUp`, `VelocityParallel`, `VelocityPerpendicular` `[official]` | Flat card in any plane: `VelocityPerpendicular`, `Speed` 0.01, `SpreadAngle` 0 `[official]` (volcano ripples, waterfall foam) |
| `ZOffset` | Moves the sprite toward (+) or away from the camera in studs without resizing `[official]` | Sort layers: flash in front (+), dark layer behind (−) |
| `Shape`, `ShapeStyle`, `ShapeInOut`, `ShapePartial` | Box, Sphere, Cylinder or Disc of the parent's size; volume or surface; outward, inward or both. `ShapePartial`: cylinder top radius (0 = cone), disc inner radius (1 = rim only), sphere hemisphere angle `[official]` | Charge-up = Sphere, Surface, Inward. Ring burst = Disc with `ShapePartial` near 1. Sphere and Cylinder do not display correctly on an Attachment `[official]` |
| `Rate`, `Enabled` | Continuous emission. Cap 400/s per emitter, 100/s on mobile `[official]` | Scaled down at low quality levels `[official]`; one developer's workaround assumes `Rate × level / 10` `[community]`. Staff say this scaling will be made less aggressive (2026-11-05) `[VS]` |
| `:Emit(n)` | Instant burst; works with `Enabled = false` | Forum replies and one production measurement say bursts are not thinned by quality level (one reply disagrees; no official statement) `[community]` `[lihfolk]`: scale `n` yourself (§11) |
| `Lifetime` | Per-particle age range; values above 20 s are capped (the official volcano tutorial's 50–60 s smoke plume is clamped to 20); 0 emits nothing `[official]` | Alive particles ≈ `Rate × Lifetime.Max`: this is the cost |
| `Speed`, `SpreadAngle`, `Acceleration`, `Drag` | Launch speed and cone; `Acceleration` is world space; `Drag` decays speed exponentially, higher is stronger (official examples: 0.8 for drifting embers, 10 for sparks that stop almost at once) `[official]` | High speed with strong drag = a streak that stops at a fixed distance (official spark burst: Speed 20–40, Drag 10, Lifetime 0.2–0.6) |
| `LockedToPart`, `VelocityInheritance` | Particles glued to the emitter, or given the parent's velocity at birth | Locked for auras on a moving body; inherited for dust shed by a foot |
| `Rotation`, `RotSpeed` | Start angle and spin per particle | `[0, 360]` rotation hides texture repetition |
| `TimeScale` | 0–1 playback speed `[official]` | 0.2–0.4 to review in slow motion; 0 for a still capture |
| `LocalTransparencyModifier` | Client-only transparency multiplier; also on Beam and Trail `[official]` | Fade a whole effect for one viewer without touching its sequences |
| `:Clear()` | Removes live particles | Call before reusing a pooled emitter for an unrelated hit |

**Flipbooks** animate the sprite from a grid: `FlipbookLayout` Grid2x2, Grid4x4, Grid8x8 or Custom (`FlipbookSizeX`/`FlipbookSizeY`, 1–64 each); `FlipbookMode` Loop, OneShot, PingPong, Random; `FlipbookFramerate` at most 30; `FlipbookBlendFrames` cross-fades frames; `FlipbookStartRandom` with framerate 0 turns one sheet into random static sprites `[official]`.
- OneShot spreads the frames across the particle's lifetime and ignores the framerate `[official]`: use it for slashes and explosions with a 0.2–0.5 s lifetime.
- Texture sizes `[official]` `[VS]`: square powers of two from 8² to 1024² since the 2022 release; since the custom-layout beta (October 2025) non-square sheets work, for example 512×256 with a 4×4 grid, so frames can keep their real aspect ratio. Check that `FlipbookIncompatible` is empty. This replaces the older "must be 1024²" advice.
- Clients switch flipbooks off automatically when memory is low, which is likely on old phones `[official]`: frame 1 must read acceptably as a still, and no effect may consist only of a flipbook.
- Leave transparent spacing around every cell; mip filtering bleeds neighbours `[official]`.

**Bursts versus streams.** Moments (hit, pickup, cast) are bursts: `Enabled = false`, `:Emit(n)` with n = 1 for a flash card, 5–30 for sparks. States (fire, aura, rain) are streams with `Rate ≤ 20` on mobile `[house]`. Writing emitter properties every frame is costly `[official]`: set once, emit, leave alone. Streams do not run in Edit mode; judge them in Play `[lihfolk]`. Review at both ends of Studio Settings → Rendering → Editor Quality Level `[official]`.

**Value rules for a layer stack** `[lihfolk]` (principles in §1): a thin white-hot core, the element colour as the body, and one saturated dark layer (blue-black, deep red; never grey) behind every bright stack; at most one accent hue; sparks follow the swing direction, not a radial sphere; later repeats of a layer are shorter and different. Kid-friendly default: hit colours that do not read as blood, no persistent marks.

## 3. Beam, Trail, Attachment

**Attachment** rules: an Attachment must be parented to a `BasePart`; author VFX sockets in Blender as `<Name>_Att` empties (`art-pipeline-blender.md`); for world-space effects use one invisible anchored host part (`Transparency = 1`, `CanCollide/CanTouch/CanQuery = false`, `CastShadow = false`) carrying several attachments.

**Beam** `[official]`: a cubic Bézier from `Attachment0` to `Attachment1`. Control point 1 lies `CurveSize0` studs along Attachment0's +X axis; control point 2 lies `CurveSize1` studs along Attachment1's −X axis, so rotating an attachment bends the beam.

| Property | Tip |
|---|---|
| `Segments` (default 10) | Straight pieces. A sequence with n keypoints needs at least n − 1 segments; 40–80 for a smooth arc `[lihfolk]`. Since November 2026 low quality levels no longer aggressively cut the segment count `[official]` `[VS]`; still check a curved beam at Editor Quality Level 1 |
| `Texture`, `TextureMode`, `TextureLength`, `TextureSpeed` | `TextureSpeed` is texture cycles per second from Attachment0 to Attachment1 (negative reverses). Unset, invalid or **not yet loaded** textures draw as a solid ribbon `[official]`: preload when the owner equips, or hold `Transparency` at 1 until loaded |
| `:SetTextureOffset(0..1)` | Sets where the texture cycle is `[official]`. With `TextureSpeed = 0`, stepping the offset from a script plays one controlled wipe along the beam. Raising the offset moves the texture the opposite way to a positive `TextureSpeed` (toward Attachment0) `[official]` |
| `Width0`, `Width1` | Linear taper. Wide to 0 gives a crescent or comet |
| `FaceCamera` | True for slash arcs and lasers; false when the ribbon must lie on a surface (waterfall, ground line) |
| `ZOffset`, `LightEmission`, `LightInfluence`, `Brightness` | As for emitters, except that beam and trail `Brightness` (0–10,000) applies whenever `LightInfluence` is below 1; `ZOffset` separates stacked beams on the same attachments `[official]` |

- Depth from layers: stack two or three beams on one path with different textures, lengths and speeds (official lava flow: base colour, crust at `TextureSpeed` 0.01, second crust reversed at −0.008). The same idea, one texture over itself at a different speed, is how League trails get their shimmer `[community]` (McSheehan).
- Exact arc: a cubic approximates a circular arc of angle θ with handle length `4/3 × tan(θ/4) × r`; a semicircle is `1.333 × r`. Two semicircle beams sharing end attachments make a ring whose line width stays constant at any radius: the right tool for telegraph outlines `[lihfolk]`.
- Sequences cannot be tweened: rebuild the `NumberSequence` from a driver value each step. Freshly uploaded images can fail to load for about 20–60 s `[lihfolk]`.

**Trail** `[official]`: while `Enabled` it records both attachments every frame and fills between them. `Lifetime` 0.01–20 s (default 2); `WidthScale` (0–1 of the attachment distance) tapers over life; `MinLength` and `MaxLength` bound segments.
- Teleport streak: enabling a trail after the blade moved draws a line from the old position. Call `:Clear()` immediately before `Enabled = true`.
- Wrap-around sheet: a trail left on through wind-up and follow-through wraps the character. Open it only for the cut (`TrailOn`/`TrailOff` markers). Trails suit arcs under about 120°; wider sweeps need a drawn crescent (§5) `[lihfolk]`.
- Projectile streak length = speed × `Lifetime`; 12–30 studs reads as a shot, shorter as a dot, longer as a laser `[lihfolk]`.

## 4. Highlight

Limits `[official]`: at most 255 Highlights display per client and extras are silently ignored; a disabled Highlight still holds a slot. Adding or removing one can trigger a geometry rebuild, while changing properties is lightweight. The first Highlight on screen costs up to 1 ms of GPU on mobile and the cost grows with screen coverage. Older code budgets against 31 `[VS]`.

- Set all of `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode` in code; the defaults (red fill, visible through walls) are almost never wanted.
- Flash by animating the transparency of a persistent Highlight; never create and destroy per hit. One Highlight per object. When hit flash, target marker and interact outline all want the same model, route them through one client arbiter (requests with priorities, highest wins). Leftover or competing Highlights are the usual "outline stopped showing" bug `[lihfolk]`.
- A uniform outline for a whole class (all enemies, all pickups) is one Highlight whose `Adornee` is their container: one slot. Keep highlighted objects out of each other's hierarchies; nested ones draw wrongly `[lihfolk]`.
- Budget `[house]`: 2 live on the low tier, 5 mid, 8 high; one interact outline at a time. Occluded depth mode for anything decorative.

## 5. Meshes and textures (authored in Blender)

Particles alone look thin; the silhouette of a strong effect is usually a mesh with a painted alpha texture that scales and fades for 0.2–0.5 s `[lihfolk]` `[community]`. A mobile studio's rule: use particles only when you must and fake the rest with textures moving over meshes, because overdraw is the cost `[community]` (Jevremović). Under house rule 1 every such mesh is a Blender model. Conflict: LihFolk and most DevForum tutorials build bolts, cores, shields and rock rings from Neon primitive Parts, `ForceField` balls or Toolbox meshes; do not import that.

| Kit piece (Blender) | Use | Notes |
|---|---|---|
| Crescent or washer-shaped band | Slash arcs | A flat ring or squashed-sphere band, 120–200° used; UVs straightened so U runs along the arc and V across (the "soulercoaster" layout `[community]`), so a horizontally painted streak follows the swing |
| Flat ring, disc, 60°/90° sector, quad | Shockwaves, ground bursts, telegraph fills | Ring texture must tile horizontally or a seam shows |
| Dome, sphere shell, cone, pillar | Shields, explosions, thrusts, light shafts | Shell slightly larger than the body for a rim |
| Crossed ribbons (two perpendicular strips) | Lightning bolts, light shafts | Reads as a glowing line from any angle without a tube look |
| Shards, chunks, nested shells, spiral ribbon | Debris, crystals, fire bodies, tornadoes | 3–4 nested shells give depth for few triangles. Modifier stacks (mask by noise, smooth, simple deform) make broken wind rings procedurally `[community]` |

- Triangle budget `[house]`: 20–300 per piece, a full effect under about 1,500. Import each layer as its own mesh so layers fade and scale separately; reuse one MeshId per piece (`performance.md`).
- Instance settings: `Anchored = true`, `CanCollide/CanTouch/CanQuery = false`, `CastShadow = false`, `CollisionFidelity = Box`, `DoubleSided = true` for cards and ribbons. Roblox positions a mesh by its bounding-box centre, which for a crescent is not the centre of its circle: set `PivotOffset` once and check one swing `[community]` `[VS]`.
- House rule 2: transient VFX meshes must not collide (a slash that blocks players or trips hit queries is a bug); treat them as `NonSolid` like foliage in `performance.md` and keep them short-lived. Anything that persists and looks solid (ice wall, summoned rock) gets real collision.
- Stacked semi-transparent meshes sort per object and can flicker: offset layers slightly, keep overlaps few, and drive all layers from one shared loop `[lihfolk]`. Every effect ships a low version with 2–3 layers.

**Moving a texture on a mesh.** Roblox has no material shader, so each engine trick maps to one of these:

| Need | Method on Roblox | Limits |
|---|---|---|
| Texture flows along a path | `Beam` (`TextureSpeed`, `:SetTextureOffset`) | Flat ribbon only; lay it along the mesh's centre line |
| Texture slides across a surface | A `Texture` instance parented to the mesh part, tweening `OffsetStudsU`/`OffsetStudsV` (the documented way to animate a surface) `[official]`; keep the mesh's own colour transparent and stack two Textures for depth `[community]` (crescent tutorial) | How a Texture maps onto a custom mesh is not documented and one developer reports it cannot be controlled `[community]`: check with an arrow texture first `[VS]` |
| Frame-by-frame animation ("mesh flipbook") | A script swaps the texture among preloaded frames, or swaps between pre-made meshes `[community]` | Every frame is a unique texture: at most 8–12 frames at 256² `[house]`; preload or the first play flickers |
| Dissolve or erosion | No threshold shader exists: cross-fade two or three baked erosion stages, or put the erosion in a OneShot flipbook particle | Fade with `Transparency`; accept a softer edge |
| Glow and soft edges | `SurfaceAppearance`: `ColorMap` alpha with `AlphaMode = Transparency` (set `MeshPart.Transparency` to at least 0.02 for smooth gradients), `Color` tint, emissive mask, strength and tint `[official]` `[VS]` | Emissive clamps to white when over-driven `[official]`; check on a low quality level |
| Edge fade by vertex alpha (common in other engines) | Not available: vertex colours import, but no doc states that vertex alpha drives transparency `[VS]` | Paint the fade into the texture alpha along the UV edge |

**Texture authoring.**
- Paint in white and grey with alpha; colour comes from the emitter, beam or part at runtime through palette roles, so one template serves every element `[lihfolk]` `[community]`. Role names across the skill: dark, body, hot, core, spark, debris; example hex per element in the palette table of `vfx-recipes.md` Conventions and on sheet 12. Other engines recolour one greyscale texture through a gradient map (dark, body and hot from one image); Roblox only multiplies by one colour, so build the ramp from layers: a dark non-additive copy behind, the body colour, and a smaller additive core `[house]`.
- Hand-painted streak or trail, in order `[community]` (McSheehan): draw the overall shape with motion in it; carve sections that follow the flow and delete those that fight it; decide primary and secondary shapes; narrow the value range so depth reads; add motion blur along the direction of travel; soften and darken what belongs in the background; colour last.
- Paint by hand: slash streaks, shockwave rings, impact stars, stylised smoke puffs and splashes, anything whose outline is the effect. For a shockwave ring: guide lines from the centre at uneven angles and lengths, an outer line with varied curvature, an inner line, fill, then cut shapes with the eraser `[community]` (McDonald). Generate: soft glows, gradients, tiling noise, and fluid sims for realistic smoke and fire (Blender, EmberGen). Krita's wrap-around mode makes tiling textures easy `[community]`.
- Polar trick for swirls: paint horizontal lines of varied thickness and opacity, erase the ends, apply a polar-coordinates filter (GIMP: Filters → Distorts → Polar Coordinates) `[community]`.
- Fade edges to transparent white, never transparent black, or sprites get a dark halo `[lihfolk]`. Check orientation with an asymmetric arrow texture before painting the real one.
- Flipbook layout: 2×2 for four random variants (framerate 0); 4×4 (16 frames) for one-shots of 0.2–0.5 s; 8×8 (64 frames) only for 1–2 s smoke or fire that must hold up close; custom strips such as 8×2 for wide slash frames. Use only as many frames as the layer's duration needs and let `FlipbookBlendFrames` smooth the rest `[community]` `[house]`. In the official 8×8 explosion sheet the fireball takes about a quarter of the frames and smoke the rest: budget frames for dissipation.
- Sizes: sprites 256² (specks 128²), strips and rings 512². Cell margins about 16/12/8 px for 512/256/128 px cells `[lihfolk]`. Memory is unique pixel count (`performance.md`); share ring, strip and glow textures. House budget: at most 8–12 VFX textures per kit, 3–4 flipbook sheets in memory on the low tier.
- Bloom is scene-wide: get glow from the texture and brightness first, keep `BloomEffect` moderate, and remember post effects weaken or vanish at low quality levels `[official]`. No textures of your own yet: the kit table in `vfx-recipes.md` Conventions names a built-in, Roblox-tutorial or CC0 stand-in for each kit texture, with its status and what to replace first. The shapes that define your game's effects are painted for it, and no AI-generated textures ship.

## 6. Timing in milliseconds and ability anatomy

Design the effect as a table (role, class, texture, size curve, life, brightness, ZOffset) before building. Study a reference frame by frame: each phase is shorter than expected, and when an effect feels long, cut it hard `[lihfolk]`.

| Beat | Target | Source |
|---|---|---|
| Input read → first visible or audible response | Same frame; within 1–2 frames (under about 35 ms at 60 FPS). Never wait for the server | `[lihfolk]` |
| Player wind-up (anticipation) on a light attack | 2–6 frames at 30 FPS (about 65–200 ms); every frame is input delay, so let a glint or rising sound anticipate while the body already moves | `[lihfolk]` |
| Input → hit frame of a light attack | About 200 ms feels responsive if motion starts at once | `[lihfolk]` |
| Enemy or boss telegraph | 250 ms reaction + escape distance ÷ 16 studs/s (default walk speed); add 100–200 ms for touch. Circle r = 10: at least 0.9 s, comfortable 1.1–1.4 s. A shipped mobile game tunes its area warning between 0.5 and 2 s | `[lihfolk]` `[community]` |
| Hot flash, or hit frame | 1–3 frames at 60 FPS (16–50 ms) for a flash card at about 0.6× the body size; up to about 100 ms for the whole hit frame | `[lihfolk]` `[community]` |
| Hit-stop | None on light hits; 50–90 ms medium to ultimate (§7) | `[lihfolk]` |
| Body (the shape that reads) | 200–400 ms | `[lihfolk]` |
| Secondary (sparks, shards, debris) and ground (rings, cracks, dust) | 300–800 ms; they outlast the glow and the trail | `[lihfolk]` `[community]` |
| Tail or linger (haze, embers, scorch) | 600–2,000 ms at very low brightness; cap whole effects near 1.4 s, ground pieces 2.2 s | `[lihfolk]` |
| Shake start | When the hit-stop releases, not during it | `[lihfolk]` |
| UI pop on a counter or icon | `emphasis` token, Back Out: `ui-motion-and-feedback.md` §2 | owner guide |
| Sound against picture | 0–30 ms late fuses; 20 ms early is noticed; 80+ ms late reads as lag (`audio-sfx-music.md` §5) | `[lihfolk]` |
| Server round trip to hide | 80–250 ms typical: cover it with an anticipation loop of 0.3–0.6 s minimum that holds until the reply | `[lihfolk]` |

**Ability anatomy.** Five stages; each has a job and a failure mode. Builds for each are in `vfx-recipes.md`.

| Stage | Job | Typical content | Failure |
|---|---|---|---|
| Telegraph | Tell targets where and when (enemy and boss attacks, big player ultimates) | Ground shape with four layers: dark outline, translucent base fill, progress fill with a hot leading edge, bright rim; fill eases in and pops white on the damage frame, fading in about 220 ms | Rim-only shapes vanish on bright floors, outline-only on dark floors. Shape numbers differ from the server's hit test, so players "dodged but got hit" |
| Cast | Confirm the input instantly; show commitment and direction | Converging specks, rings moving along the shot direction, weapon glint, riser sound; starts on the input frame on the caster's client | Waiting for the server echo; wind-up longer than the move deserves |
| Travel | Show path and speed | A hot point exactly where the hit volume is, tapered trail, dark wake; muzzle flash 1–2 studs ahead of the hand | Reads as a dot or a laser (trail length); hot point offset from the server's hit position, so dodging is guesswork `[community]` (Leroy) |
| Hit | The payoff: the cluster from `game-craft.md` §1 | Flash, body, directional sparks, ground ring, sound, hit-stop, shake | All additive (white blob); radial sparks on a directional hit; three systems drawing the same explosion |
| Linger | Aftermath and persistent state | Scorch, embers, haze; states (burning, shielded) as looping low-rate emitters driven by a character attribute | Effects that outlive their cause; a state sent as a one-time event that late joiners never see |

- One shape table shared by the telegraph drawing and the server hit test. For long warnings send `Workspace:GetServerTimeNow()` so late receivers draw only the remainder `[lihfolk]`.
- Fire effects from animation markers (`GetMarkerReachedSignal`), the same data that times damage; when the clip is retimed everything moves together `[lihfolk]`. A common Roblox workflow welds one invisible VFX part to the root with a `Motor6D` and animates it like a limb, so emitters follow hand-authored motion `[community]`.
- Tie layer count to importance with a written ladder (base kit; rare adds a shockwave; epic adds a ground piece; top tier adds a pillar) and audit effects against it. When several systems can draw one beat (kit effect, rarity layer, ultimate climax), each claims the beat for its duration and the others skip it `[lihfolk]`. A modular kit (flash, eruption, ring, residue as shared components with colour, scale and duration parameters) scales to hundreds of variants `[community]`.
- Grandeur comes from escalating a few layers and cutting others, with at most one growing environmental element; re-check the character's silhouette at game distance after each addition. Readability budget per cast `[lihfolk]`: one ground piece at a time, at most 3 large pieces, at most 35% of the screen (55% for an ultimate), anything on the line between camera and the player's head at least 0.75 transparent.

## 7. Hit-stop, camera shake and FOV kicks

This section owns the hit-stop, shake and kick numbers for the whole skill; `game-craft.md` §1.3 holds the one module (`HitFeel`: shake, kick, catch-up hit-stop) that applies them. Give every hit **one strength value** (about 0.3–1.3) and derive every layer from it, so designers move one number per move `[lihfolk]`. Pixels are on `Phone-S` (800×360, `ui-design-figma.md`) at FOV 70.

| Tier | Strength | Hit-stop | Trauma added | Peak shake (trauma² × 2°) | On `Phone-S` | Shake back to 0 after | Kick: % of height (°, px) |
|---|---|---|---|---|---|---|---|
| Light | 0.30 | none | 0 | none | 0 | — | none |
| Medium | 0.45 | 50 ms | 0.50 | 0.5° | 2.2 px: just visible | 0.20 s | 0.25% (0.2°, 0.9 px) |
| Heavy | 0.80 | 66 ms | 0.75 | 1.1° | 5 px: clear | 0.30 s | 0.5% (0.4°, 1.8 px) |
| Finisher | 1.00 | 75 ms | 0.85 | 1.45° | 6.5 px | 0.34 s | 0.8% (0.64°, 2.9 px) |
| Ultimate | 1.30 | 89 ms | 1.00 | 2.0° (the comfort cap) | 9 px: strong | 0.40 s | 1.2% (0.96°, 4.3 px) |

Arithmetic (heavy): 0.75² × 2° = 1.125°; tan 1.125° ÷ (2 × tan 35°) = 1.4% of screen height × 360 px = 5 px (15 physical px on a 1,080-px panel). Smooth noise rarely sits at its extreme: sampling Luau's own `math.noise` code, the largest swing of one hit is typically 0.6–0.75 of the peak, so read the pixel column as "up to". Visibility bands `[house]`, to confirm on a real phone: under 1 px nothing, about 2 px just visible, 4–5 px clear, 8–9 px strong. Stop = `0.03 + 0.045 × strength` seconds `[lihfolk]`; trauma, kick and the bands are `[house]`.

Conflict: LihFolk's ladder adds 0.12 / 0.25 / 0.35 / 0.60 trauma and keeps single medium and heavy hits nearly shakeless on purpose, letting flurries build it up; under the house 2° cap its heavy hit is 0.125° (0.56 px on `Phone-S`): invisible on a phone. Ruling: the trauma column above, which also sits inside the knowledge-base tier ranges (medium 0.30–0.50, large 0.70–1.00). The knowledge base's longer stops (0.04–0.06 s medium, 0.10–0.15 s large) remain only a ceiling for isolated, spaced moments (a launch, a rare drop, a boss slam).

- **Frame maths.** A 50 ms stop is 3 frames at 60 FPS but 1 or 2 at 30 FPS, so it reads as inconsistency on phones. A stop that must be felt needs at least 66 ms; cap any stop at 200 ms `[lihfolk]`.
- **Budgets** `[lihfolk]`: at most 140 ms of hit-stop per rolling 0.6 s; under 15% of a move's duration; reserve room for the finisher; one stop per swing however many targets it hits; trauma grows with `1 + 0.35 × log2(targets)` up to the cap of 1; visible shake under about 10% of combat time.
- **Catch-up hit-stop** (`HitFeel.stop`): slow the track to 0.12× for `d`, then play at 1.88× for `d`; after `2d` the animation is back on the wall clock, so effects scheduled at cast time still line up `[lihfolk]`.
- **Shake by FOV, not resolution.** Screen movement for a rotation `a` is `tan(a) / (2 × tan(FOV/2))` of screen height: 1° is 1.25% at FOV 70 and 2.4% at FOV 40. The module multiplies rotation by `min(1, tan(FOV/2) / tan 35°)`, so zooming in does not double the shake and widening never exceeds 2°. Use rotation (pitch and yaw) for impacts and translation only for "the ground moved" (0.5 studs moves a subject 15 studs away by 2.4% of the screen, as much as 2° of rotation). Cap noise frequency at 0.4 × smoothed FPS (12 Hz at 30 FPS) or smooth noise turns into jitter `[lihfolk]`.
- **Directional kick** (`HitFeel.kick`): one rotation away from the impact, set in one frame, eased back over 100–180 ms; it carries direction and is the comfortable substitute for shake. Others' hits: no hit-stop or kick on your screen; trauma × 0.3 with smoothstep falloff from 30 to 150 studs `[lihfolk]` (a heavy hit next to you adds 0.225: 0.1°, nothing visible).
- **Shake amplitude and roll.** Shake plus kick stays within 2° of pitch and yaw per axis and 0.5 studs of offset (`accessibility-and-player-qol.md` §5). **No roll in gameplay**: roll is the strongest nausea trigger. Conflict: LihFolk's camera module clamps roll at 4° and rolls 2.5° on a dash, while its comfort note says "no gameplay roll"; the comfort note wins. A static tilted frame belongs to cutscenes (`cutscenes-and-cinematics.md` §5).
- **FOV and offsets.** Every effect is a finite envelope that ends at exactly 0 (exponential decays leave residue). Sum envelopes per channel and clamp: FOV ±12°, offset 1.6 studs. One module owns `Camera.FieldOfView`; two systems tweening it fight every frame. Reference dash: +9° in 60 ms, out over 250 ms `[lihfolk]`. First person: FOV only.
- **Impact frames**: one high-contrast full-screen frame (the anime version inverts the scene to black and white with radial streaks). Conflict: LihFolk counts rendered frames (remove after 2 `PreRender` callbacks); at 240 FPS that is 8 ms and invisible. Time flashes on the real clock: about 33–50 ms and at least one rendered frame `[house]`. Flash limits in §12.

## 8. Screen effects and number popups

- `ColorCorrectionEffect`, `BlurEffect` and `BloomEffect` parented to `Workspace.CurrentCamera` affect only that player; post effects never affect GUI and may work differently or not at all at low quality levels `[official]`. So no gameplay information may live only in a post effect. There is no vignette post effect: use a full-screen `ImageLabel` with a radial-gradient texture `[lihfolk]`. Full-screen overlays and post passes are the most expensive juice on phones (fill rate): off on the low tier (§11).
- One client module owns every screen-effect instance and composes requests each frame; several scripts tweening the same effect leave it stuck on. Hits are pulses (instant attack, 150–350 ms decay); low health is a level (below about 30%, fades over 1 s on heal). Clamp summed pulse strength so ten pellets do not white out the screen. No blur while aiming `[lihfolk]`.
- Incoming-damage effects wait for the server-confirmed event and carry the attacker's position for a directional arc; outgoing hit feedback may be predicted `[lihfolk]`.

**Number popups** (damage, +coins).
- Motion: the floating-number row of `ui-motion-and-feedback.md` §5 (rise 24–40 px, fade over 0.6–1.2 s) with the `emphasis` pop. Combat additions `[house]`: random sideways drift so stacked hits separate; crits by size and colour, never by flashing.
- Clutter `[lihfolk]`: merge hits on one target within 150 ms into one number; cap about 12 on screen and drop the oldest; default to "mine only" in multiplayer; abbreviate (12.4K).
- Cost: staff confirm that neither text nor billboard rendering is cheap (one report: 20 visible BillboardGuis took a desktop from 240 to 130 FPS) `[community]`; the MicroProfiler tag is `Prepare/Pass3dAdorn`, fixed by fewer visible adorned objects `[official]`. Pool them, set `Enabled = false` when idle, or draw labels in one ScreenGui placed with `Camera:WorldToViewportPoint`; measure both on a phone `[house]`. The server sends the damage fact; the client draws the number.

## 9. Tween or spring

| Tool | Behaviour | Use for | Avoid for |
|---|---|---|---|
| `TweenService:Create` | Fixed duration and easing curve; client only | One-shot moves with a known end: UI pops, mesh scale and fade, FOV envelopes | Targets that change mid-flight (it restarts and looks stiff); world objects on the server |
| `TweenService:GetValue(alpha, style, direction)` | Easing as a pure function | Driving many layers or a `NumberSequence` from one loop | `Enum.EasingStyle.Spring` and `Bezier`: it and `TweenInfo.new` raise an error for them `[official]` `[VS]` |
| `TweenService:SmoothDamp(current, target, velocity, smoothTime, maxSpeed?, dt?)` | Critically damped spring: no overshoot; returns new value and velocity (feed the velocity back in); number, Vector2, Vector3 or CFrame `[official]` `[VS]` | Followers and retargeting: camera offsets, health bars, counters chasing a value, magnet pull | Bouncy pops (it never overshoots) |
| Spring (stiffness or frequency, damping) | Overshoot, interruptible, keeps velocity. Hand-rolled, or an MIT library such as spr or Ripple (`ui-motion-and-feedback.md` §6) | Squash and stretch, button presses, hits landing on an object that is still settling | Timed sequences that must end on a beat |
| `1 − exp(−rate × dt)` lerp | Cheapest smoothing, frame-rate independent | Camera follow (`game-craft.md` §3) | Anything needing overshoot |

- Squash and stretch `[lihfolk]`: preserve area or volume (height 0.8 → width 1.25 in 2D); set the extreme pose instantly and spring back (tweening into it adds 50–100 ms of mush); damping ratio 0.4–0.6 gives one visible overshoot; squash the art layer, never the text; sub-step stiff springs to about 120 Hz so 30 FPS phones stay stable. Depth: 3–5% sober UI, 8–15% cartoon UI, 15–30% collectibles. Rigid R15 parts cannot squash, so use pose; single-mesh props can through `MeshPart.Size` `[lihfolk]`. Easing tokens and UI motion rules: `ui-motion-and-feedback.md` §2–3.

## 10. Replication: the server says what happened, each client draws it

The server does no rendering; a server-built effect replicates every instance and property change to everyone and arrives late `[official]`. Pattern `[lihfolk]` `[community]`:

| Step | Caster's client | Server | Other clients |
|---|---|---|---|
| Input | Plays the effect now; sends `(presetId, aim)` | — | — |
| Decide | — | Validates, applies gameplay | — |
| Tell | — | One payload to players near the cast, skipping the caster (loop `Players:GetPlayers()`, `FireClient` within the radius) | — |
| Draw | Already drawn | Nothing | Build from pooled templates |

- Payload = ids and numbers only: `(caster, presetId, cframe, seed, aux?)`. Preset lists are append-only (reordering makes old servers and new clients disagree). Tuning (sizes, colours, durations) lives in a shared client table; the client never sends size, colour or CFrame for the server to trust.
- Server checks, in order: argument types; preset is client-castable (telegraphs and rewards are server-only); finite values; character alive; clamp aim to range rather than reject (the prediction stays roughly right); per-preset cooldown with about 50 ms grace; per-player token bucket (for example burst 6, refill 3/s). Details in `networking-and-security.md`.
- Recipients: players within about 250 studs, a little beyond the client cull; `FireAllClients` for local effects wastes bandwidth. Channel: `UnreliableRemoteEvent` for frequent cosmetic events (payload limit 1,000 bytes `[official]` `[VS]`); reliable for anything players react to.
- Seed: emitters randomise inside the engine, so a seed only reproduces your own scripted choices (debris directions, bolt shapes); draw them from `Random.new(seed)`.
- Moments travel as events; **states travel as attributes** on the character (aura on, shield up, burning), so late joiners and streamed-in characters show them.
- A rejected cast leaves a harmless cosmetic; for effects that imply an outcome (teleport), keep a handle and cancel on rejection. Never pass Instances the client may not have yet `[community]`.

## 11. Pooling, budgets and quality scaling

**Where cost goes** `[lihfolk]` `[official]`: fill rate and overdraw (screen area × layers; one 40-stud smoke puff at the camera can cost more than 300 sparks across the room), particles alive (`Rate × Lifetime` plus bursts), draw calls (emitters, beams, trails and textures batch poorly), instance churn (clone and destroy per hit shows up as a hitch seconds later), property churn, lights (shadows off, always), per-effect frame loops (use one shared stepper).

**Pooling rules**: clone each template once per client; reposition; `:Clear()`; emit; release after the longest `Lifetime.Max` plus any emit delay. Destroying an emitter destroys its live particles. Cap the pool (peak concurrency plus about 25%) and skip decoration when it is full. The `EmitCount`/`EmitDelay` attribute convention below is also what community VFX plugins write, so plugin-authored templates drop in `[community]`.

```lua
--!strict
-- Unexecuted sketch. Client module. Emitters in templates are Enabled = false and carry attributes:
-- EmitCount (number), EmitDelay (seconds), MinDetail (0..1; decoration layers set it above 0).
local FxPool = { detail = 1 } -- 0..1, written by the governor below
local MAX_LIVE = 12
local free: { [BasePart]: { BasePart } } = {}
local live: { [BasePart]: number } = {}
local function num(d: Instance, name: string, default: number): number
	local v = d:GetAttribute(name)
	return if type(v) == "number" then v else default
end
function FxPool.play(template: BasePart, cf: CFrame, gameplay: boolean?)
	local bucket = free[template] or {}
	free[template] = bucket
	local count = live[template] or 0
	local pooled = table.remove(bucket)
	if not pooled and count >= MAX_LIVE and not gameplay then return end -- decoration is droppable, information is not
	local root: BasePart = pooled or template:Clone()
	root.Parent = workspace
	live[template] = count + 1
	root.CFrame = cf
	local longest = 0
	for _, d in root:GetDescendants() do
		if not d:IsA("ParticleEmitter") then continue end
		d:Clear()
		if not gameplay and FxPool.detail < num(d, "MinDetail", 0) then continue end
		local n = math.max(1, math.round(num(d, "EmitCount", 1) * FxPool.detail))
		local delay = num(d, "EmitDelay", 0)
		longest = math.max(longest, d.Lifetime.Max + delay)
		task.delay(delay, d.Emit, d, n)
	end
	task.delay(longest + 0.1, function()
		live[template] -= 1
		table.insert(bucket, root)
	end)
end
return FxPool
```

**Budgets for the 3 GB Android phone.** `performance.md` holds the doc limits and house ambient budget. Add:

| Budget | Low tier | Mid | High | Source |
|---|---|---|---|---|
| Particles alive from effects, per client | about 360 | 900 | 3,000 | `[lihfolk]` module caps and rule of thumb |
| Burst count scale | 0.4 | 0.7 | 1 | `[lihfolk]` |
| New effect instances or pool takes per frame | 3 | 8 | 20 | `[lihfolk]` |
| Live Highlight flashes | 2 | 5 | 8 | `[lihfolk]` |
| Full-screen post effects and glows | off | off | on | `[lihfolk]` |
| Lights per effect | 0–1, no shadows | 1 | 1–2 | `[lihfolk]` |
| Others' effects | Half detail; decoration dropped beyond about 160 studs; nothing small beyond 220; skipped off-screen | same | same | `[lihfolk]` |

- Three budgets are needed together: per cast, per caster over a window, and per client. Worked check `[lihfolk]`: 8 players swinging twice a second at about 62 particles alive per swing is about 560 alive for you (own full, others half): fine. Eight simultaneous ultimates at 5,600 each for the caster and half for onlookers is 25,200: not fine on any phone, so the per-client cap must exist. Budget per effect by rarity, duration on screen, how many units it can hit and how often it can be cast `[community]` (Jevremović).
- **Never cull gameplay information** (telegraphs, hazards, objectives, your own hit confirmation): simplify, never skip. Degrade others' decoration to zero first.
- Decide once when the effect starts (owner, gameplay flag, distance, in view, current load, detail); re-evaluating each frame causes popping. Long-lived effects (auras, waterfalls) sleep by distance with two thresholds so they do not flicker. Degradation is authored: artists mark decoration layers with `MinDetail`; code never guesses which layers matter `[lihfolk]`.

**Quality scaling.** The engine's effective quality level is not readable from game scripts, and Roblox now asks developers **not** to change effects based on `UserGameSettings.SavedQualityLevel`: it works against automatic scaling and the API is planned for deprecation `[official]` `[VS]` (staff post, 2026-11-05; this reverses the earlier advice in this guide). So: offer your own Effects setting (Low, Medium, High) as the ceiling, then let measured frame time move a detail value with hysteresis, and keep it running all session because phones throttle after 10–15 minutes `[lihfolk]`. The sketch raises detail when the frame time is holding the target, not beating it by 20% as the LihFolk governor does, because a 60 Hz-capped phone can never beat a 60 FPS target `[house]`.

```lua
--!strict
-- Unexecuted sketch. Client. Quick to fall, slow to rise, never above the player's own Effects setting.
local RunService = game:GetService("RunService")
local FxPool = require(script.Parent.FxPool)
local CEILING = { Low = 0.4, Medium = 0.7, High = 1 }
local ceiling = CEILING.High -- set from your settings module when the player changes "Effects"
local TARGET = 1 / 60 -- use 1 / 30 where the device or your own frame cap holds 30 FPS, or detail sits at the floor
local average, overFor, okFor = TARGET, 0, 0
FxPool.detail = math.min(ceiling, 0.7)
RunService.PreRender:Connect(function(dt: number)
	if dt > 0.25 then return end -- a hitch, not a trend
	average += (dt - average) * math.min(1, dt * 2)
	if average > TARGET * 1.15 then overFor += dt; okFor = 0
	elseif average < TARGET * 1.05 then okFor += dt; overFor = 0
	else overFor = 0; okFor = 0 end
	if overFor > 2 then FxPool.detail = math.max(0.4, FxPool.detail - 0.15); overFor = 0
	elseif okFor > 10 then FxPool.detail = math.min(ceiling, FxPool.detail + 0.1); okFor = 0 end
end)
```

**Measure** `[lihfolk]`: draw calls with Shift+F2 on a quiet frame versus a full-party ultimate; `debug.profilebegin("FxStep")` around the stepper; a debug counter of particles alive; stress protocol with one phone, one tablet and one PC in a server while 4–8 players cast at one spot, then at the phone's camera, then 200 studs away. Target: the phone stays under 33 ms per frame in the worst repeatable fight. Cut order: onlooker share, others' decoration, big transparent pieces, stream lifetimes, then your own effects.

## 12. Reduced motion and photosensitivity

- `GuiService.ReducedMotionEnabled` mirrors the player's Reduce Motion toggle; the docs frame it around UI tweens (snap or fade instead of slide) `[official]`. Extend it to camera and screen effects, add your own setting with three states (Follow Roblox, On, Off), and listen for changes at runtime. One comfort module answers every effect; effects that each read settings themselves drift apart `[lihfolk]`.

| System | Under reduced motion |
|---|---|
| Camera shake and offsets | Off; keep a 0.25× directional kick if any confirmation is wanted (about 1 px from the finisher tier up, nothing below: the flash, target flash and sound carry the hit) |
| FOV changes | 0.5× |
| Hit-stop | Off or shortened; keep the sound and spark |
| Impact frames, blur, full-screen flashes | Off; replace with a steady edge vignette and a directional indicator |
| UI motion | Snap or fade (`ui-motion-and-feedback.md` §7) |

- Settings to ship with any shake, flash or FOV juice (tier 2 in `core-loop-tuning.md` §8): shake slider 0–100% (schema and default in `accessibility-and-player-qol.md` §10; tune the values in §7 so that 100% is comfortable), screen-effects intensity slider (0 removes tint, blur and vignette), flashes toggle, hit-stop toggle, damage numbers (All, Mine, Off).
- Flash safety: nothing flashes more than three times in any one second (WCAG 2.3.1); Xbox Accessibility Guideline 118 counts a flash as a luminance change of 10% or more over about 20% or more of the screen and has a separate, stricter test for saturated red. So: no saturated red full-screen flashes; rapid hits merge into one sustained tint; reduce contrast, frequency and area instead of adding a warning screen. Every large flash from every player's effects passes one limiter (the flash gate in `accessibility-and-player-qol.md` §5, set to 2 per second). No Roblox-specific rule was found, so this is the developer's job. Comfort: unrequested camera rotation, especially roll, is the strongest nausea trigger; keep camera motion player-driven and decoration optional `[lihfolk]`. Keep the information, remove the motion: with everything off the player must still know they hit, were hit and from where.

## 13. Juice ladder ordered by frame cost

`core-loop-tuning.md` §8 orders juice by build time. This orders it by what it costs a phone at runtime `[lihfolk]`; climb only while the frame holds.

| Rung | Juice | Runtime cost | Risk |
|---|---|---|---|
| 1–2 | Sound one-shot with pitch variation; `UIScale` pop, position slide, `UIGradient` sweep | Low | Voice cap |
| 3 | Camera kick, shake, FOV punch | Negligible CPU | Comfort, not performance |
| 4 | Counter count-up, number popup | Low to medium | Text reshaping every change: cap update rate |
| 5 | Small particle burst (5–30) | Medium | Size on screen matters more than count |
| 6 | Highlight flash | Medium | Slot and rebuild rules (§4) |
| 7 | Beams and trails | Medium | Segments and overdraw |
| 8 | Mesh VFX layers | Medium | Instances and tweens per swing: pool |
| 9 | `CanvasGroup` fades | Medium to high | Off-screen render target and memory |
| 10 | Full-screen glows, overlays, blur and bloom pulses | High on phones | Fill rate over every pixel. Hidden cost at any rung: creating instances per event (the hitch lands seconds later) |

## 14. Generic Roblox VFX tells and their fixes

What makes an effect look like every other Roblox game `[house]`, from the DevForum work viewed for this guide set against the professional references (`visual-library/vfx.md`).

| Tell | Why it reads as generic | Fix |
|---|---|---|
| Clusters of same-size soft round puffs or sparkles | Default or pack textures; no silhouette | One hand-drawn shape with a hard edge carries the effect; soft glow is a single supporting layer |
| Everything additive, white or neon | No value structure; white blob on bright floors, invisible on snow | Dark layer, element body, thin core (§2); the shadow buys the glow |
| Perfect radial burst, equal spokes, all layers start and end together | Reads as a default emitter | Uneven spacing and lengths; follow the action's direction; stagger layers by 0–60 ms; fast in, eased out |
| No anticipation and no dissipation: pops in, pops out | Nothing to read before or after the hit | Three stages (§1); most of the duration is quiet dissipation |
| Rainbow or several saturated hues | No element identity | One ramp plus one accent (§1 table) |
| Neon primitive rings, balls, cylinders and Toolbox rocks | The stock Roblox look; also breaks house rule 1 | Blender kit pieces with painted alpha textures (§5) |
| Pack mash-up: realistic fire flipbook beside a flat cartoon slash | Mixed edge treatment, detail level and palette | One style guide: edge hardness, outline or none, detail level, palette; repaint or drop what does not fit |
| Effect ignores the world: no ground dust, no contact, same on every floor | Floats on top of the scene | A ground layer where it touches; tint dust to the surface; a short dark residue |
| Ribbons or rings of uniform width and brightness | Reads as flat geometry, not energy | Taper widths; a hot leading edge; a dark trailing edge; break the shape up |
| Every move equally big and bright | No hierarchy; fights are unreadable | 0–10 importance sheet (§1); basic attacks are quiet |
| Glow comes from Bloom | Disappears on low quality levels and differs per device | Glow painted into the texture, plus `Brightness` |
| Friend and foe effects identical | Team fights cannot be parsed | Allegiance hue and shape on the primary layer (§1) |

**Engineering mistakes that sink good art:** effects built or tweened on the server, or a caster waiting for the echo · `LightInfluence` left at the Studio default · clone and destroy per hit, or destroying an emitter right after `Emit` · a Highlight created per flash · a trail left on through the whole swing or enabled without `Clear()` · trusting the engine to thin bursts, or reading `SavedQualityLevel` · tuning on a desktop, close up, in daylight, alone · a telegraph drawn from different numbers than the server hit test, or culled on low settings · a state replicated as a one-time event · per-frame random shake, camera roll, exponential FOV decay, two writers of `FieldOfView` · a flipbook as the whole effect · a unique 1024² texture per effect · no shake slider, flash toggle or reduced-motion path.

## 15. Level-up: symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Effect is a white blob, or muddy and flat | All additive with no dark layer and oversized bright sprites; or grey darks and one hue | Saturated dark layer, element body, thin white core, one accent; brightness by screen area |
| Effect dark in caves, grey in shade | `LightInfluence` 1 | Set 0 on every emitter, beam and trail |
| Feels slow or floaty | Phases too long; linear curves; sound peak late; feedback waits for the server | Cut every phase; flash under 50 ms; fast-in curves; predict locally; align sound peak (`audio-sfx-music.md`) |
| Solid coloured slab instead of a slash | Beam texture not loaded | Preload on equip; hold transparent until loaded; wait out fresh uploads |
| Streak across the body, or a sheet around the character | Trail not cleared; trail window too wide | `Clear()` before enabling; marker window; crescent for sweeps over 120° |
| Outline stopped showing | Slot limit or a leftover Highlight on the model | Destroy unused; one arbiter per object |
| Own aura or trail missing in first person | Effects parented inside the character are hidden there | Parent to a welded helper part outside the character model |
| Fine alone, lags in a full server | No onlooker share or per-client cap | Others at half or less; global particle cap; distance and view culling for strangers |
| Hitch a few seconds after big moments | Instance churn | Pools with a cap |
| Phones lag only when the effect is near the camera | Large see-through pieces causing overdraw | Make them smaller, stack fewer layers, raise transparency along the camera line |
| Low graphics does not help | Bursts are not thinned by the engine | Own detail value on `EmitCount`; `MinDetail` layers |
| Old phones show a single flipbook frame | Memory pressure switched flipbooks off | Fewer sheets; first frame reads as a still |
| Caster sees effects late or twice | Caster waits for the echo, or the echo is not skipped | Play on input; server skips the caster |
| Aura or shield missing for some players | State sent as an event | Character attribute; each client starts its own visual |
| "Dodged but got hit" | Telegraph pop and damage on different frames or shapes; projectile hot point offset from the hit volume | One shared shape table; damage at the pop; primary layer drawn at the hit volume |
| Light hits feel inconsistent on phones | 50 ms stops are 1–2 frames at 30 FPS | 66 ms or more where it matters; otherwise rely on sound and spark |
| Fast weapons feel sticky | Hit-stop adds up in flurries | Rolling 140 ms per 0.6 s budget; reserve for finishers |
| Shake reads as jitter or is violent when zoomed; FOV drifts over a session | Noise above half the frame rate; no FOV scaling; exponential decays and several FOV writers | Cap at 0.4 × FPS; scale by `tan(FOV/2)`; finite envelopes ending at 0; one owner |
| Motion sickness or flash complaints | No comfort settings; roll; strobing | §12 table; three-flash limit; replacement feedback |
| Fights unreadable | No readability budget; no hierarchy; everyone's effects at full strength | One ground piece, 3 large pieces, 35% screen; importance sheet; onlookers reduced |

## 16. Critique rubric

Score each line 0 (fails), 1 (partly), 2 (holds) from a phone capture at the game camera, at full speed and then frame by frame. Ship at 16 or more out of 20 with no 0 in lines 1–4 `[house]`; the lines come from §1 and the sources behind it.

| # | Line | Holds when |
|---|---|---|
| 1 | Gameplay read | In half a second a new viewer can say what it is, where it hits, when, and whose it is |
| 2 | Silhouette | The greyscale block-in reads; shapes are designed and irregular; the primary shape matches the hit volume |
| 3 | Value | One area of focus with dark beside light; survives the lightest and darkest floor |
| 4 | Timing | Anticipation fits the design; climax is short; dissipation is quiet; no linear ramps |
| 5 | Hierarchy | Primary, secondary and tertiary are distinct; loudness matches the 0–10 importance |
| 6 | Colour | One ramp and one accent; allegiance clear without relying on red versus green |
| 7 | Cohesion | Same edge treatment, detail level and palette family as the rest of the game; no generic tell from §14 |
| 8 | Feel | Sound, hit-stop and camera land on the same beat (§6, §7); nothing outlives its cause |
| 9 | Cost | Inside the §11 budgets with 8 casters; a 2–3 layer low version exists |
| 10 | Comfort | Flash, shake and motion pass §12 with settings off and on |

Asking for critique `[community]`: give the context (game, camera, device, the reference you aimed at) and ask pointed questions ("does the hit frame read at phone size?"), not "is it good?". When giving it, name what works first; a paint-over of one still frame says more than a paragraph.

## Review gate

- [ ] Every effect is built on clients from one small validated payload; the caster predicts and the server skips the echo; states replicate as attributes.
- [ ] Each effect was blocked in greyscale first and has a written layer table: primary matching the hit volume, secondary, tertiary, and a dark layer under every bright stack.
- [ ] Anticipation, climax and dissipation exist and are timed against §6; curves are non-linear; effects fire from animation markers; telegraph drawing and server hit test share one shape table.
- [ ] An importance sheet (0–10 per ability and viewer) and an element and allegiance colour script exist; friend and foe differ by more than hue.
- [ ] `LightInfluence` set explicitly; emitters fire with `Emit`; streams at mobile rates; no per-frame emitter property writes; nothing reads `SavedQualityLevel`.
- [ ] Beam and trail textures preloaded; trails cleared and windowed; arcs over 120° drawn as crescents; Highlights persistent with one owner per object; VFX meshes are Blender kit pieces, non-colliding, pooled, with a 2–3 layer low version; textures greyscale, painted or CC0, shared and counted.
- [ ] Hit-stop is client-only, budgeted, one per swing; shake starts after the stop and never rolls the camera; FOV has one owner and returns to exactly 0.
- [ ] Pools capped; per-cast, per-caster and per-client budgets written; gameplay information never culled; detail scales from the player's Effects setting and measured frame time.
- [ ] Shake slider, screen-effects intensity, flash toggle, hit-stop toggle and reduced-motion path exist; large flashes pass one gate (at most 2 per second, under the three-per-second limit).
- [ ] Scored 16+ on §16 from a hot 3 GB Android phone, in slow motion, at game distance, on the brightest and darkest floor, with 8 casters at one spot.

## Sources

Accessed 2026-11-10 and 2026-11-11. "(read)" = opened; "(viewed)" = images looked at. Nothing here rests on search summaries any more. Full annotated list with image links: `visual-library/vfx.md`, `visual-library/vfx-learning.md`.

- Roblox/creator-docs at commit 7cbffff (read): `effects/particle-emitters.md`, `effects/beams.md`, `effects/trails.md`, `effects/highlighting.md`, `parts/textures-decals.md`, `art/modeling/surface-appearance.md`, `performance-optimization/design.md`, `tutorials/use-case-tutorials/vfx/` (explosions, volcanoes, waterfalls); reference classes `ParticleEmitter`, `Beam`, `Trail`, `Texture`, `SurfaceAppearance`, `MeshPart`, `Highlight`, `TweenService`, `UserGameSettings`, `GuiService`, `UnreliableRemoteEvent`. https://github.com/Roblox/creator-docs
- Roblox staff posts (read): custom flipbook layouts, 2025-10-13 https://devforum.roblox.com/t/4005128 · flipbook release and texture sizes, 2022-10-21 https://devforum.roblox.com/t/2029388 · quality levels, beam segments and `SavedQualityLevel`, 2026-11-05 https://devforum.roblox.com/t/4977292 · procedural emitter shapes, 2021-10-20 https://devforum.roblox.com/t/1517642 · hiding avatar effects in first person, 2024-08-27 https://devforum.roblox.com/t/3136706
- Oli "Beardilocks" McDonald (Riot), Anatomy of a League of Legends missile, part 1 https://realtimevfx.com/t/11614 and part 2 https://realtimevfx.com/t/13062 (read, viewed); shockwave drawing advice https://realtimevfx.com/t/25874 (read, viewed)
- Jason Keyser, Block-ins and Timing, 2025 https://realtimevfx.com/t/29830 (read, viewed) and Artistic Principles of VFX https://realtimevfx.com/t/4081 (read; videos verified by oEmbed, not watched) · Shannon McSheehan (Riot), texture-painting tutorial in post 6 of https://realtimevfx.com/t/1133 (read, viewed) · Woo (Supercell), Very Cartoonic VFX for Brawl Stars https://realtimevfx.com/t/11032 (read, viewed)
- Stefan Jevremović (Nordeus), VFX Staples: Shape, Color, and Motion https://80.lv/articles/vfx-staples-shape-color-and-motion/ (read, viewed); Kevin Leroy, Constructing VFX Worthy of League of Legends https://80.lv/articles/constructing-vfx-worthy-of-league-of-legends/ (read)
- Mesh and timing threads (read, viewed): Mesh Soulercoasters https://realtimevfx.com/t/1987 · How do I make my timing better https://realtimevfx.com/t/17547 · Modular Approach to AOE VFX https://realtimevfx.com/t/31540 · On Asking for Feedback https://realtimevfx.com/t/7159 (read)
- DevForum community (read, viewed): Crecent Sword Slash Effect https://devforum.roblox.com/t/1113871 · VFX Tutorial (Blender modifiers) https://devforum.roblox.com/t/872437 · Scrollable textures for MeshParts https://devforum.roblox.com/t/2820890 · What are Mesh Flipbooks https://devforum.roblox.com/t/2656999 · Stoic Bomb workflow overview https://devforum.roblox.com/t/3608056 · Client Replication 101 https://devforum.roblox.com/t/1789487 · critique threads https://devforum.roblox.com/t/2898977, https://devforum.roblox.com/t/4824974, https://devforum.roblox.com/t/3114938
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault, commit 43ba05d) (read): `07 Lighting VFX and Audio/` (particle emitters, beams and trails, highlights, VFX design playbook, budgets and culling, replication, telegraphs, projectiles, screen damage, textures and flipbooks, readability and value, escalation, kid-friendly hit feedback), `47 Game Feel and Juice/`, `08 Animation/05 Systems/`, `45 Procedural Blender Assets/Mesh VFX Packs Built in Blender`, `58 Player QoL and Game Tweaks/Comfort Toggles`, `42 Accessibility and Inclusive Design/Motion Sensitivity and Camera Comfort`.
- Read 2026-11-11: `Rate` and `Emit` versus quality level https://devforum.roblox.com/t/474762, https://devforum.roblox.com/t/2657543 (developer replies, no staff answer) · BillboardGui cost, with staff replies https://devforum.roblox.com/t/3542255 · https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118 · https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html · `performance-optimization/microprofiler/tag-table.md`, `production/publishing/accessibility.md`, `environment/post-processing-effects.md` in the docs mirror
- Not reachable or not found: the Riot VFX style guide PDF (the 2017 nexus.leagueoflegends.com links now redirect to the home page); vfxapprentice.com (403); an official statement on whether `Emit` bursts are thinned by graphics level; a documented rule for how `Texture` maps onto custom meshes; an official flash-rate rule.
