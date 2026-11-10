# VFX and juice: particles, beams, meshes, timing, shake, replication, budgets, safety

What this is: the build-level reference for visual effects and game feel on Roblox: every effect instance and its traps, effect anatomy and timing in milliseconds, hit-stop and camera work, the client-only replication pattern, pooling, budgets for a 3 GB Android phone, and motion and flash safety. Open it when building an effect or auditing why a game feels flat, laggy or unreadable. It extends `game-craft.md` §1 (tier table, trauma-shake module, reward pop sketch) and `core-loop-tuning.md` §7 (juice ordered by build cost); neither is repeated here. Sound is in `audio-sfx-music.md`; frame budgets in `performance.md`.

Tags: `[official]` Roblox docs (mirror commit ccc2b01), `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its numbers come from one production combat game and are starting points, not laws), `[VS]` version-sensitive, `[house]` house estimate. Terms: *VFX* = visual effects; *juice* = small non-gameplay responses that confirm an action; *emitter* = `ParticleEmitter`; *additive* = colours add to what is behind (glow); *overdraw* = the same pixel drawn several times by stacked transparent layers; *telegraph* = a warning drawn before an attack lands.

## Contents

1. Start here by level · 2. Pick the right instance · 3. ParticleEmitter · 4. Beam, Trail, Attachment · 5. Highlight · 6. Meshes and textures (Blender) · 7. Timing and ability anatomy · 8. Hit-stop, shake, FOV · 9. Screen effects and number popups · 10. Tween or spring · 11. Replication · 12. Pooling, budgets, quality scaling · 13. Reduced motion and flash safety · 14. Juice ladder by frame cost · 15. Common mistakes · 16. Level-up table · Review gate · Sources

## 1. Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Every effect runs in a LocalScript; the server only sends "what happened". (2) Emitters stay `Enabled = false`; fire them with `:Emit(n)`. (3) Set `LightInfluence = 0` on every emitter. (4) One flash, one shape, a few sparks, a sound: stop there. (5) Add a shake slider and honour Reduce Motion before shipping any shake | Flipbooks, mesh VFX, governors, hit-stop budgets |
| Intermediate | Design each effect as a layer table (§7) before opening Studio. Pool effect roots. Give every bright stack one dark layer. Play the caster's effect on input and skip the echo. Scale burst counts yourself on weak devices. Tie effects to animation markers, not timers | Per-client particle governors, catch-up hit-stop |
| Expert | Budget per cast, per caster window and per client; never cull gameplay information. Count cost from templates with a script. Catch-up hit-stop, FOV-normalised shake, noise frequency capped by frame rate. Measure on a hot phone with 8 casters at one spot | — |

## 2. Pick the right instance

| Need | Use | Why |
|---|---|---|
| Sparks, smoke, flashes, dust, rain, pickup pops | `ParticleEmitter` | Camera-facing or velocity-aligned quads; cheapest to author |
| A line or ribbon between two points: laser, tether, guide arrow, slash arc, ring outline of constant width | `Beam` | Cubic Bézier ribbon; texture can scroll (`TextureSpeed`) |
| The path something just travelled: blade, dash, projectile | `Trail` | Records two attachments each frame |
| "This object matters": interactable, target, ally through walls, hit flash | `Highlight` | Outline and fill on a whole model; strict rules in §5 |
| A shape with volume or a silhouette particles cannot give: shock ring, crescent, dome, pillar, shards, telegraph disc | Blender mesh (`MeshPart`) tweened on the client | House rule 1: authored in Blender |
| Light on the scene from the effect | `PointLight` in an Attachment, `Shadows = false`, one per effect | Particles never light the world, even at `LightEmission = 1` `[official]` |
| Whole-screen response | GUI overlay or a post effect on the Camera (§9) | Post effects on `Workspace.CurrentCamera` show for that player only `[official]` |

Runtime `EditableImage`/`EditableMesh` are not a VFX tool: they need an experience permission and have tight memory budgets; bake offline and upload `[lihfolk]` `[VS]`.

## 3. ParticleEmitter

Parent to a `BasePart` (particles spawn in its box or `Shape`) or to an `Attachment` (spawn at a point; rotate the attachment rather than using `EmissionDirection`). `Sphere` and `Cylinder` shapes do not display correctly on an Attachment `[official]`.

| Property | What it does | Trap or tip |
|---|---|---|
| `Texture` | Sprite. Transparent PNG, or greyscale on black with `LightEmission = 1` `[official]` | Author white/grey and tint with `Color`, so one texture serves every element |
| `Color`, `Transparency`, `Size` | Sequences over each particle's life (at most 20 keypoints `[VS]`) | Linear between keys. Punchy growth reaches about 80% of final size by 35% of life `[lihfolk]`; fade in and out or particles pop |
| `Squash` | Non-uniform scale: above 0 thinner and taller, below 0 wider and shorter `[official]` | Rain streaks, speed lines, anamorphic flares |
| `LightEmission` | 0 normal blend, 1 additive `[official]` | Additive layers sum to white. Dense matter (water, smoke, debris) stays at 0 |
| `LightInfluence` | 0 ignores scene light, 1 lit like a part. Defaults to 1 when inserted in Studio but 0 from `Instance.new` `[official]` | Set 0 explicitly or the effect goes black in caves and grey in shade |
| `Brightness` | Scales emitted light when `LightInfluence = 0` `[official]` | Bigger sprite on screen = lower brightness; tiny specks need several times more `[lihfolk]` |
| `Orientation` | `FacingCamera`, `FacingCameraWorldUp`, `VelocityParallel`, `VelocityPerpendicular` `[official]` | Flat card in any plane: `VelocityPerpendicular`, `Speed` 0.001, `SpreadAngle` 0, attachment pointing along the card's normal `[lihfolk]` |
| `ZOffset` | Moves the sprite toward (+) or away from the camera in studs without resizing; fractional values work `[official]` | Sort layers: flash in front (+), dark layer behind (−) |
| `Rate`, `Enabled` | Continuous emission. Cap 400/s per emitter, 100/s on mobile `[official]` | Scaled down by graphics level; one forum test measured `Rate × level / 10` `[community]` |
| `:Emit(n)` | Instant burst; works with `Enabled = false` | Forum reports and one production measurement say bursts are not thinned by graphics level (one report disagrees) `[community]` `[lihfolk]`: scale `n` yourself (§12) |
| `Lifetime` | Per-particle age range; values above 20 s are capped; 0 emits nothing `[official]` | Alive particles ≈ `Rate × Lifetime.Max`: this is the cost |
| `Speed`, `SpreadAngle`, `Acceleration`, `Drag` | Launch speed and cone; `Acceleration` is world space; `Drag` is exponential decay of speed `[official]` | High speed + high drag = a streak that stops at a fixed distance. Gravity on a rotated rig must be computed in world space |
| `LockedToPart`, `VelocityInheritance` | Particles glued to the emitter, or given the parent's velocity at birth | Locked for auras on a moving body; inherited for dust shed by a foot |
| `Rotation`, `RotSpeed` | Start angle and spin per particle | `[0, 360]` rotation hides texture repetition |
| `TimeScale` | 0–1 playback speed `[official]` | 0.2–0.4 to review in slow motion; 0 for a still capture |
| `:Clear()` | Removes live particles | Call before reusing a pooled emitter for an unrelated hit |

**Flipbooks** animate the sprite from a grid: `FlipbookLayout` 2×2, 4×4, 8×8 or Custom; `FlipbookMode` Loop, OneShot, PingPong, Random; `FlipbookFramerate` at most 30; `FlipbookStartRandom` plus framerate 0 turns one sheet into a set of random static sprites `[official]`.
- OneShot spreads the frames across the particle's lifetime and ignores the framerate property `[official]`; use it for slashes and explosions with a 0.2–0.5 s lifetime.
- Clients switch flipbooks off automatically when memory is low, which is likely on old phones `[official]`: frame 1 must read acceptably as a still, and no effect may consist only of a flipbook.
- Leave transparent spacing around every cell; mip filtering bleeds neighbours `[official]`.
- Conflict: the docs say the texture size must be an exact multiple of the layout and recommend smaller textures to save memory; LihFolk reports the Studio error text demands 1024×1024 `[lihfolk]`. Trust the docs, then check: author 1024² for 8×8 (128 px cells), try 512² for 4×4 and 2×2, and confirm the emitter's `FlipbookIncompatible` message is empty.

**Bursts versus streams.** Moments (hit, pickup, cast) are bursts: `Enabled = false`, `:Emit(n)` with n = 1 for a flash card, 5–30 for sparks. States (fire, aura, rain) are streams with `Rate ≤ 20` on mobile `[house]`. Writing emitter properties every frame is costly `[official]`: set once, emit, leave alone. Streams do not run in Edit mode; judge them in Play `[lihfolk]`.

**Value rules that separate amateur from professional effects** `[lihfolk]`: a thin white-hot core, the element colour as the body, and one saturated dark layer (blue-black, deep red; never grey) behind every bright stack so it keeps a shape; at most one accent hue; white only as a thin core; sparks follow the swing direction, not a radial sphere; later repeats of a layer are shorter and different, never identical copies. Test in the darkest and brightest zone of the map: an effect tuned at noon vanishes in a cave. Kid-friendly default: hit colours that do not read as blood, no persistent marks `[lihfolk]`.

## 4. Beam, Trail, Attachment

**Attachment** rules: an Attachment must be parented to a `BasePart`; author VFX sockets in Blender as `<Name>_Att` empties (`art-pipeline-blender.md`); for world-space effects use one invisible anchored host part (`Transparency = 1`, `CanCollide/CanTouch/CanQuery = false`, `CastShadow = false`) carrying several attachments.

**Beam** `[official]`: a cubic Bézier from `Attachment0` to `Attachment1`. Control point 1 lies `CurveSize0` studs along Attachment0's +X axis; control point 2 lies `CurveSize1` studs along Attachment1's −X axis, so rotating an attachment bends the beam.

| Property | Tip |
|---|---|
| `Segments` (default 10) | Straight pieces. A colour or transparency sequence with n keypoints needs at least n − 1 segments; 40–80 for a smooth arc `[lihfolk]` |
| `Texture`, `TextureMode`, `TextureLength`, `TextureSpeed` | The only built-in scrolling texture on Roblox. Unset, invalid or **not yet loaded** textures draw as a solid ribbon `[official]`: preload when the owner equips, or hold `Transparency` at 1 until loaded |
| `Width0`, `Width1` | Linear taper. Wide to 0 gives a crescent or comet |
| `FaceCamera` | True for slash arcs and lasers; false when the ribbon must lie on a surface (waterfall, ground line) |
| `ZOffset`, `LightEmission`, `LightInfluence`, `Brightness` | As for emitters; set `Transparency` explicitly |

- Exact arc: a cubic approximates a circular arc of angle θ with handle length `4/3 × tan(θ/4) × r`; a semicircle is `1.333 × r`. Two semicircle beams sharing end attachments make a ring whose line width stays constant at any radius: the right tool for telegraph outlines `[lihfolk]`.
- Sequences cannot be tweened: rebuild the `NumberSequence` from a driver value each step.
- Freshly uploaded images can fail to load for about 20–60 s `[lihfolk]`; never judge or ship a texture uploaded seconds ago.

**Trail** `[official]`: while `Enabled` it records both attachments every frame and fills between them. `Lifetime` 0.01–20 s (default 2); `WidthScale` tapers over life; `MinLength` and `MaxLength` bound segments; changing attachments wipes the trail.
- Teleport streak: enabling a trail after the blade moved draws a line from the old position. Call `:Clear()` immediately before `Enabled = true`.
- Wrap-around sheet: a trail left on through wind-up and follow-through wraps the character. Open it only for the cut (`TrailOn`/`TrailOff` animation markers). Trails suit arcs under about 120°; wider sweeps need a drawn crescent (beam or mesh) `[lihfolk]`.
- Projectile streak length = speed × `Lifetime`; 12–30 studs reads as a shot, shorter reads as a dot, longer as a laser `[lihfolk]`.

## 5. Highlight

Limits `[official]`: at most 255 Highlights display per client and extras are silently ignored; a disabled Highlight still holds a slot, so destroy the ones you will not reuse. Adding or removing one can trigger a geometry rebuild (spike plus draw calls), while changing properties is lightweight. The first Highlight on screen costs up to 1 ms of GPU on mobile; on mobile the cost also grows with screen coverage. Low-end devices draw them more pixelated. Limit history: older code budgets against 31 `[VS]`.

Rules:
- Set all of `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode` in code; the defaults (red fill, visible through walls) are almost never wanted.
- Flash by animating the transparency of a persistent Highlight; never create and destroy per hit.
- One Highlight per object. When hit flash, target marker and interact outline all want the same model, route them through one client arbiter (requests with priorities, highest wins). Leftover or competing Highlights on one model are the usual "outline stopped showing" bug `[lihfolk]`.
- A uniform outline for a whole class (all enemies, all pickups) is one Highlight whose `Adornee` is their container: one slot `[lihfolk]`.
- Keep highlighted objects out of each other's hierarchies; nested ones draw wrongly `[lihfolk]`.
- Budget `[house]`: 2 live on the low tier, 5 mid, 8 high; one interact outline at a time. Occluded depth mode for anything decorative.

## 6. Meshes and textures (authored in Blender)

Particles alone look thin; the silhouette of a strong effect is usually a mesh with a painted alpha texture that scales and fades for 0.2–0.5 s `[lihfolk]` `[community]`. Under house rule 1 every such mesh is a Blender model. Conflict: LihFolk builds bolts, projectile cores, shields and telegraphs from Neon primitive Parts, `ForceField` balls, `SpecialMesh` and `HandleAdornment`s; do not import that. Use the kit below.

| Kit piece (Blender) | Use | Notes |
|---|---|---|
| Crescent ribbon | Slash arcs | U along the arc, V across; 120–200° long; width swells at the head, tapers at both tips |
| Flat ring, disc, 60°/90° sector, quad | Shockwaves, ground bursts, telegraph fills | Ring texture must tile horizontally or a seam shows |
| Dome, sphere shell, cone, pillar | Shields, explosions, thrusts, beams of light | Shell slightly larger than the body for a rim |
| Crossed ribbons (two perpendicular strips) | Lightning bolts, light shafts | Reads as a glowing line from any angle without a tube look |
| Shards, chunks, nested flame shells | Debris, crystals, fire bodies | 3–4 nested shells give depth for few triangles |

- Triangle budget `[house]`: 20–300 per piece; a full effect under about 1,500.
- Import each layer as its own mesh (merge off) so layers fade and scale separately; reuse one MeshId per piece (instancing rules in `performance.md`).
- Instance settings: `Anchored = true`, `CanCollide/CanTouch/CanQuery = false`, `CastShadow = false`, `CollisionFidelity = Box`, `DoubleSided = true` for cards and ribbons.
- House rule 2 interpretation: transient VFX meshes are the one visible class that must not collide (a slash that blocks players or trips hit queries is a bug). Treat them as `NonSolid` (same class as foliage in `performance.md`) and keep them short-lived; anything that persists and looks solid (ice wall, summoned rock, lingering crystal) gets real collision.
- Roblox positions a mesh by its bounding-box centre, which for a crescent is not the centre of its circle: set `PivotOffset` once per mesh and check one swing `[community]` `[VS]`.
- A MeshPart's texture cannot be UV-scrolled `[community]`. Animate `Size`, `CFrame` and `Transparency`; for dissolve, cross-fade two or three baked erosion stages; where the texture must flow, use a Beam.
- Stacked semi-transparent meshes sort per object and can flicker: offset layers slightly and keep overlaps few. Drive all layers of an effect from one shared loop, not thirty tweens `[lihfolk]`.
- Every effect ships a low version with 2–3 layers.

**Texture authoring.**
- Paint in white and grey with alpha; colour comes from the emitter, beam or part at runtime through palette roles (main, hot, dark, glow, spark, debris) so one template serves every element `[lihfolk]`.
- Fade edges to transparent white, never transparent black, or sprites get a dark halo `[lihfolk]`.
- Sizes: sprites 256² (specks 128²), strips and rings 512², flipbooks per §3. Cell margins about 16/12/8 px for 512/256/128 px cells `[lihfolk]`. Memory is unique pixel count (`performance.md`); share ring, strip and glow textures across effects. House budget: at most 8–12 VFX textures per kit, 3–4 flipbook sheets in memory on the low tier.
- Sources of frames: paint them (Krita, Photoshop, Figma); render a Blender simulation or animated noise to 16 or 64 orthographic frames and pack the grid; fluid tools such as EmberGen and After Effects are common in the community `[community]`.
- Check orientation with an asymmetric arrow texture before painting the real one.
- Bloom is scene-wide: get glow from the texture and brightness first, keep `BloomEffect` moderate, and remember post effects weaken or vanish at low quality levels `[official]`.

## 7. Timing in milliseconds and ability anatomy

Design the effect as a table (role, class, texture, size curve, life, brightness, ZOffset) before building. Study a reference frame by frame: each phase is shorter than expected, and when an effect feels long, cut it hard `[lihfolk]`.

| Beat | Target | Source |
|---|---|---|
| Input read → first visible or audible response | Same frame; within 1–2 frames (under about 35 ms at 60 FPS). Never wait for the server | `[lihfolk]` |
| Player wind-up (anticipation) on a light attack | 2–6 frames at 30 FPS (about 65–200 ms); every frame is input delay, so let a glint or rising sound anticipate while the body already moves | `[lihfolk]` |
| Input → hit frame of a light attack | About 200 ms feels responsive if motion starts at once | `[lihfolk]` |
| Enemy or boss telegraph | 250 ms reaction + escape distance ÷ 16 studs/s (default walk speed); add 100–200 ms for touch. Circle r = 10: at least 0.9 s, comfortable 1.1–1.4 s | `[lihfolk]` |
| Hot flash | 1–3 frames at 60 FPS (16–50 ms), about 0.6× the body size, at the contact point, one frame after contact | `[lihfolk]` |
| Hit-stop | None on light hits; 50–90 ms medium to ultimate (§8) | `[lihfolk]` |
| Body (the shape that reads) | 200–400 ms | `[lihfolk]` |
| Secondary (sparks, shards, debris) | 300–800 ms | `[lihfolk]` |
| Ground (rings, cracks, dust) | 300–700 ms | `[lihfolk]` |
| Tail or linger (haze, embers, scorch) | 600–2,000 ms at very low brightness; cap whole effects near 1.4 s, ground pieces 2.2 s | `[lihfolk]` |
| Shake start | When the hit-stop releases, not during it | `[lihfolk]` |
| UI pop return | 120–180 ms Back Out (`game-craft.md`) | `[house]` |
| Sound against picture | 0–30 ms late fuses; 20 ms early is noticed; 80+ ms late reads as lag (`audio-sfx-music.md` §5) | `[lihfolk]` |
| Server round trip to hide | 80–250 ms typical: cover it with an anticipation loop of 0.3–0.6 s minimum that holds until the reply | `[lihfolk]` |

**Ability anatomy.** Five stages; each has a job and a failure mode.

| Stage | Job | Typical content | Failure |
|---|---|---|---|
| Telegraph | Tell targets where and when (enemy and boss attacks, big player ultimates) | Ground shape with four layers: dark outline, translucent base fill, progress fill with a hot leading edge, bright rim; fill eases in and pops white on the damage frame, fading in about 220 ms | Rim-only shapes vanish on bright floors, outline-only on dark floors. Shape numbers differ from the server's hit test, so players "dodged but got hit" |
| Cast | Confirm the input instantly; show commitment | Converging specks, imploding ring, weapon glint, charge glow, riser sound; starts on the input frame on the caster's client | Waiting for the server echo; wind-up longer than the move deserves |
| Travel | Show path and speed | Core with a hot centre, tapered trail, dark wake; muzzle flash 1–2 studs ahead of the hand | Reads as a dot or a laser (trail length); travel visual and server hit position disagree |
| Hit | The payoff: the cluster from `game-craft.md` §1 | Flash, body, directional sparks, ground ring, sound, hit-stop, shake | All additive (white blob); radial sparks on a directional hit; three systems drawing the same explosion |
| Linger | Aftermath and persistent state | Scorch, embers, haze; states (burning, shielded) as looping low-rate emitters driven by a character attribute | Effects that outlive their cause; a state sent as a one-time event that late joiners never see |

- One shape table shared by the telegraph drawing and the server hit test. For long warnings send `Workspace:GetServerTimeNow()` so late receivers draw only the remainder `[lihfolk]`.
- Fire effects from animation markers (`GetMarkerReachedSignal`), the same data that times damage; when the clip is retimed everything moves together `[lihfolk]`.
- Tie layer count to importance with a written ladder (base kit; rare adds a shockwave; epic adds a ground piece; top tier adds a pillar) and audit effects against it `[lihfolk]`.
- When several systems can draw one beat (kit effect, rarity layer, ultimate climax), each claims the beat for its duration and the others skip it `[lihfolk]`.
- Grandeur comes from escalating a few layers and cutting others, with at most one growing environmental element; re-check the character's silhouette at game distance after each addition `[lihfolk]`.
- Readability budget per cast `[lihfolk]`: one ground piece at a time, at most 3 large pieces, at most 35% of the screen (55% for an ultimate), anything on the line between camera and the player's head at least 0.75 transparent.

## 8. Hit-stop, camera shake and FOV kicks

Base values and the shake module are in `game-craft.md` §1. Net-new rules:

- **One strength value per hit** (about 0.3–1.3) drives every layer, so designers move one number per move `[lihfolk]`.

| Tier | Strength | Hit-stop | Trauma added | Directional kick (% of screen height) |
|---|---|---|---|---|
| Light | 0.30 | none | 0 | none |
| Medium | 0.45 | 50 ms | 0.12 | 0.25 |
| Heavy | 0.80 | 66 ms | 0.25 | 0.5 |
| Finisher | 1.00 | 75 ms | 0.35 | 0.8 |
| Ultimate | 1.30 | 89 ms | 0.60 | 1.2 |

  Stop = `0.03 + 0.045 × strength` seconds `[lihfolk]`. These trauma values are lower than the `game-craft.md` table; start there for solo games and here for crowded combat, where hits stack.
- **Frame maths.** A 50 ms stop is 3 frames at 60 FPS but 1 or 2 at 30 FPS, so it reads as inconsistency on phones. A stop that must be felt needs at least 66 ms; cap any stop at 200 ms `[lihfolk]`. This qualifies the 40–60 ms medium stop in `game-craft.md`: treat it as seasoning.
- **Budgets** `[lihfolk]`: at most 140 ms of hit-stop per rolling 0.6 s; under 15% of a move's duration; reserve room for the finisher; one stop per swing however many targets it hits; trauma grows with `1 + 0.35 × log2(targets)`; visible shake under about 10% of combat time.
- **Catch-up hit-stop**: slow the track to 0.12× for `d`, then play at 1.88× for `d`; after `2d` the animation is back on the wall clock, so effects scheduled at cast time still line up `[lihfolk]`.
- **Shake by FOV, not resolution.** Screen movement for a rotation `a` is `tan(a) / (2 × tan(FOV/2))` of screen height: 1° is 1.25% at FOV 70 and 2.4% at FOV 40. Multiply rotational shake by `tan(FOV/2) / tan(35°)` when zoomed. Use rotation for impacts and translation only for "the ground moved" `[lihfolk]`.
- **Aliasing on phones**: cap noise frequency at 0.4 × smoothed FPS (12 Hz at 30 FPS) or smooth noise turns into jitter `[lihfolk]`.
- **Directional kick**: one rotation away from the impact, set in one frame, eased back over 100–180 ms; it carries direction and is the comfortable substitute for shake `[lihfolk]`.
- **FOV and offsets.** Every effect is a finite envelope that ends at exactly 0 (exponential decays leave residue). Sum envelopes per channel and clamp: FOV +12°, offset 1.6 studs, roll 4°. One module owns `Camera.FieldOfView`; two systems tweening it fight every frame. Reference dash: +9° in 60 ms, out over 250 ms `[lihfolk]`. First person: FOV only.
- **Others' hits**: no hit-stop or kick on your screen; trauma × 0.3 with smoothstep falloff from 30 to 150 studs `[lihfolk]`.
- **Impact frames**: one high-contrast full-screen frame. Conflict: LihFolk counts rendered frames (remove after 2 `PreRender` callbacks); at 240 FPS that is 8 ms and invisible. Hold flashes for `max(2 frames, 33 ms)` and never beyond 50 ms `[house]`.

```lua
--!strict
-- Unexecuted sketch. Client only. Catch-up hit-stop; the newest stop owns the restore.
local token = 0
local function hitStop(track: AnimationTrack, seconds: number, baseSpeed: number)
	token += 1
	local mine = token
	track:AdjustSpeed(baseSpeed * 0.12)
	task.delay(seconds, function()
		if token ~= mine then return end
		track:AdjustSpeed(baseSpeed * 1.88) -- replay the lost time
		task.delay(seconds, function()
			if token == mine then track:AdjustSpeed(baseSpeed) end
		end)
	end)
end
return hitStop
```

## 9. Screen effects and number popups

- Instances: `ColorCorrectionEffect`, `BlurEffect` and `BloomEffect` parented to `Workspace.CurrentCamera` affect only that player; post effects never affect GUI and may work differently or not at all at low quality levels `[official]`. So no gameplay information may live only in a post effect. There is no vignette post effect: use a full-screen `ImageLabel` with a radial-gradient texture `[lihfolk]`.
- One client module owns every screen-effect instance and composes requests each frame; several scripts tweening the same effect leave it stuck on `[lihfolk]`.
- Hits are pulses (instant attack, 150–350 ms decay); low health is a level (below about 30%, fades over 1 s on heal). Clamp summed pulse strength so ten pellets do not white out the screen. No blur while aiming `[lihfolk]`.
- Incoming-damage effects wait for the server-confirmed event and carry the attacker's position for a directional arc; outgoing hit feedback may be predicted `[lihfolk]`.
- Full-screen overlays and post passes are the most expensive juice on phones (fill rate): off on the low tier (§12).

**Number popups** (damage, +coins).
- Motion `[house]`: pop 1.3 → 1 in 120 ms, rise 40–60 px over 600–800 ms, fade during the last 30%, random sideways drift; crits by size and colour, never by flashing.
- Clutter `[lihfolk]`: merge hits on one target within 150 ms into one number; cap about 12 on screen and drop the oldest; default to "mine only" in multiplayer; abbreviate (12.4K).
- Cost: BillboardGuis carry real overhead and hidden or fully transparent ones still cost `[community]` (`Pass3dAdorn` in `performance.md`). Pool them, set `Enabled = false` when idle, or draw labels in one ScreenGui placed with `Camera:WorldToViewportPoint`; measure both on a phone `[house]`.
- The server sends the damage fact; the client draws the number.

## 10. Tween or spring

| Tool | Behaviour | Use for | Avoid for |
|---|---|---|---|
| `TweenService:Create` | Fixed duration and easing curve; client only | One-shot moves with a known end: UI pops, mesh scale and fade, FOV envelopes | Targets that change mid-flight (it restarts from the current value and looks stiff); world objects on the server |
| `TweenService:GetValue(alpha, style, direction)` | Easing as a pure function | Driving many layers or a `NumberSequence` from one loop | — |
| `TweenService:SmoothDamp(current, target, velocity, smoothTime, maxSpeed?, dt?)` | Critically damped spring: no overshoot; returns new value and velocity; number, Vector2, Vector3, CFrame `[official]` `[VS]` | Followers and retargeting: camera offsets, health bars, counters chasing a value, magnet pull | Bouncy pops (it never overshoots) |
| Hand-rolled spring (stiffness, damping) | Overshoot, interruptible, keeps velocity | Squash and stretch, button presses, hits landing on an object that is still settling | Timed sequences that must end on a beat |
| `1 − exp(−rate × dt)` lerp | Cheapest smoothing, frame-rate independent | Camera follow (`game-craft.md` §3) | Anything needing overshoot |

- Squash and stretch `[lihfolk]`: preserve area or volume (height 0.8 → width 1.25 in 2D); set the extreme pose instantly and spring back (tweening into it adds 50–100 ms of mush); damping ratio 0.4–0.6 gives one visible overshoot; squash the art layer, never the text; sub-step stiff springs to about 120 Hz so 30 FPS phones stay stable. Depth: 3–5% sober UI, 8–15% cartoon UI, 15–30% collectibles.
- Rigid R15 parts cannot squash; use pose. Single-mesh props can by `MeshPart.Size` `[lihfolk]`.
- Easing choices are in `game-craft.md` §1; UI motion rules in `ui-input-crossplatform.md`.

## 11. Replication: the server says what happened, each client draws it

The server does no rendering; a server-built effect replicates every instance and property change to everyone and arrives late `[official]`. Pattern `[lihfolk]` `[community]`:

| Step | Caster's client | Server | Other clients |
|---|---|---|---|
| Input | Plays the effect now; sends `(presetId, aim)` | — | — |
| Decide | — | Validates, applies gameplay | — |
| Tell | — | One payload to players near the cast, skipping the caster | — |
| Draw | Already drawn | Nothing | Build from pooled templates |

- Payload = ids and numbers only: `(caster, presetId, cframe, seed, aux?)`. Preset lists are append-only (reordering makes old servers and new clients disagree). Tuning (sizes, colours, durations) lives in a shared client table; the client never sends size, colour or CFrame for the server to trust.
- Server checks, in order: argument types; preset is client-castable (telegraphs and rewards are server-only); finite values; character alive; clamp aim to range rather than reject (the prediction stays roughly right); per-preset cooldown with about 50 ms grace; per-player token bucket (for example burst 6, refill 3/s). Details in `networking-and-security.md`.
- Recipients: players within about 250 studs, a little beyond the client cull. `FireAllClients` for local effects wastes bandwidth.
- Channel: `UnreliableRemoteEvent` for frequent cosmetic events (payload limit 1,000 bytes `[official]` `[VS]`); reliable for anything players react to.
- Seed: emitters randomise inside the engine, so a seed only reproduces your own scripted choices (debris directions, bolt shapes); draw them from `Random.new(seed)`.
- Moments travel as events; **states travel as attributes** on the character (aura on, shield up, burning), so late joiners and streamed-in characters show them.
- A rejected cast leaves a harmless cosmetic; for effects that imply an outcome (teleport), keep a handle and cancel on rejection. Never pass Instances the client may not have yet `[community]`.

```lua
--!strict
-- Unexecuted sketch. Server: after validating a cast and applying gameplay, tell nearby clients once.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local playFx = ReplicatedStorage:WaitForChild("PlayFx") :: RemoteEvent
local RADIUS = 250
local rng = Random.new()

local function broadcast(caster: Player?, presetId: number, cf: CFrame, aux: Vector3?)
	local seed = rng:NextInteger(1, 2147483646)
	for _, player in Players:GetPlayers() do
		if player == caster then continue end -- the caster drew it on input
		local character = player.Character
		local root = character and character.PrimaryPart
		if root and (root.Position - cf.Position).Magnitude <= RADIUS then
			playFx:FireClient(player, caster, presetId, cf, seed, aux)
		end
	end
end
return broadcast
```

## 12. Pooling, budgets and quality scaling

**Where cost goes** `[lihfolk]` `[official]`: fill rate and overdraw (screen area × layers; one 40-stud smoke puff at the camera can cost more than 300 sparks across the room), particles alive (`Rate × Lifetime` plus bursts), draw calls (emitters, beams, trails and textures batch poorly), instance churn (clone and destroy per hit shows up as a hitch seconds later), property churn, lights (shadows off, always), per-effect frame loops (use one shared stepper).

**Pooling rules**: clone each template once per client; reposition; `:Clear()`; emit; release after the longest `Lifetime.Max` plus any emit delay. Destroying an emitter destroys its live particles. Cap the pool (peak concurrency plus about 25%) and skip decoration when it is full.

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
	local root = table.remove(bucket)
	if not root then
		if count >= MAX_LIVE and not gameplay then return end -- decoration is droppable, information is not
		root = template:Clone()
		root.Parent = workspace
	end
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

- Three budgets are needed together: per cast, per caster over a window, and per client. Worked check `[lihfolk]`: 8 players swinging twice a second at about 62 particles alive per swing is about 560 alive for you (own full, others half): fine. Eight simultaneous ultimates at 5,600 each for the caster and half for onlookers is 25,200: not fine on any phone, so the per-client cap must exist.
- **Never cull gameplay information** (telegraphs, hazards, objectives, your own hit confirmation): simplify, never skip. Degrade others' decoration to zero first.
- Decide once when the effect starts (owner, gameplay flag, distance, in view, current load, detail); re-evaluating each frame causes popping. Long-lived effects (auras, waterfalls) sleep by distance with two thresholds so they do not flicker `[lihfolk]`.
- Authored degradation: artists mark decoration layers with `MinDetail`; code never guesses which layers matter `[lihfolk]`.

**Quality scaling by device and by the player's graphics level.** `UserGameSettings.SavedQualityLevel` is readable but is `Automatic` for most players; the engine's effective level (`GraphicsQualityLevel`) is not readable from game scripts `[official]`. So: treat a manual level as a ceiling, then let measured frame time move a detail value with hysteresis, and keep it running all session because phones throttle after 10–15 minutes `[lihfolk]`. Also offer an explicit Effects setting (Low, Medium, High) that overrides it.

```lua
--!strict
-- Unexecuted sketch. Client. Quick to fall, slow to rise, never above the player's own setting.
local RunService = game:GetService("RunService")
local FxPool = require(script.Parent.FxPool)
local saved = UserSettings():GetService("UserGameSettings").SavedQualityLevel
local ceiling = if saved == Enum.SavedQualitySetting.Automatic then 1 else math.clamp(saved.Value / 7, 0.4, 1)
local TARGET = 1 / 60
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

The rise test is "holding the target", not "beating it by 20%" as in the LihFolk governor, because a 60 Hz-capped phone can never beat a 60 FPS target `[house]`.

**Measure** `[lihfolk]`: draw calls with Shift+F2 on a quiet frame versus a full-party ultimate; `debug.profilebegin("FxStep")` around the stepper; a debug counter of particles alive; stress protocol with one phone, one tablet and one PC in a server while 4–8 players cast at one spot, then at the phone's camera, then 200 studs away, at lowest and highest graphics. Target: the phone stays under 33 ms per frame in the worst repeatable fight. Cut order: onlooker share, others' decoration, big transparent pieces, stream lifetimes, then your own effects.

## 13. Reduced motion and photosensitivity

- `GuiService.ReducedMotionEnabled` mirrors the player's Reduce Motion toggle; the docs frame it around UI tweens (snap or fade instead of slide) `[official]`. Extend it to camera and screen effects, add your own setting with three states (Follow Roblox, On, Off), and listen for changes at runtime `[lihfolk]`.
- One comfort module answers every effect; effects that each read settings themselves drift apart `[lihfolk]`.

| System | Under reduced motion |
|---|---|
| Camera shake, roll, offsets | Off; keep a 0.25× directional kick if any confirmation is wanted |
| FOV changes | 0.5× |
| Hit-stop | Off or shortened; keep the sound and spark |
| Impact frames, blur, full-screen flashes | Off; replace with a steady edge vignette and a directional indicator |
| UI motion | Snap or fade (`ui-input-crossplatform.md`) |

- Settings to ship with any tier-2 juice: shake slider (default 60–80%), screen-effects intensity slider (0 removes tint, blur and vignette), flashes toggle, hit-stop toggle, damage numbers (All, Mine, Off).
- Flash safety: no more than 3 full-screen flashes in any second (WCAG 2.3.1); avoid saturated red full-screen flashes; rapid hits merge into one sustained tint; prefer reducing contrast, frequency and area over a warning screen (Xbox Accessibility Guideline 118). No Roblox-specific rule was found, so this is the developer's job.
- Comfort: unrequested camera rotation, especially roll, is the strongest nausea trigger; keep camera motion player-driven and decoration optional `[lihfolk]`.
- Keep the information, remove the motion: with everything off the player must still know they hit, were hit and from where.

## 14. Juice ladder ordered by frame cost

`core-loop-tuning.md` §7 orders juice by build time. This orders it by what it costs a phone at runtime `[lihfolk]`; climb only while the frame holds.

| Rung | Juice | Runtime cost | Risk |
|---|---|---|---|
| 1 | Sound one-shot with pitch variation | Low | Voice cap |
| 2 | `UIScale` pop, position slide, `UIGradient` sweep | Low | — |
| 3 | Camera kick, shake, FOV punch | Negligible CPU | Comfort, not performance |
| 4 | Counter count-up, number popup | Low to medium | Text reshaping every change: cap update rate |
| 5 | Small particle burst (5–30) | Medium | Size on screen matters more than count |
| 6 | Highlight flash | Medium | Slot and rebuild rules (§5) |
| 7 | Beams and trails | Medium | Segments and overdraw |
| 8 | Mesh VFX layers | Medium | Instances and tweens per swing: pool |
| 9 | `CanvasGroup` fades | Medium to high | Off-screen render target and memory |
| 10 | Full-screen glows, overlays, blur and bloom pulses | High on phones | Fill rate over every pixel |
| — | Creating instances per event | Hidden | The hitch lands seconds later |

## 15. Common mistakes

1. Building effects on the server, or tweening world objects there.
2. Waiting for the server before showing the caster anything.
3. `LightInfluence` left at the Studio default; effect dark indoors.
4. Everything additive and white; no dark layer; big sprites at full brightness.
5. Radial sparks on a directional hit; identical layers repeated per beat.
6. Clone and destroy per hit; destroying an emitter right after `Emit`.
7. Trail left enabled through the whole swing; no `Clear()` before enabling.
8. Creating and destroying Highlights per flash; several systems highlighting one model.
9. Relying on the engine to thin bursts on low graphics.
10. Tuning on a desktop, close up, in daylight, alone.
11. Telegraph drawn from different numbers than the server's hit test, or culled on low settings.
12. Per-frame random shake; exponential FOV decay that never returns to 0; two writers of `FieldOfView`.
13. Effects that outlive their cause; a state replicated as a one-time event.
14. A flipbook as the whole effect; unique 1024² textures per effect.
15. No shake slider, flash toggle or reduced-motion path.

## 16. Level-up: symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Effect is a white blob | All additive, no dark layer, large sprites too bright | Saturated dark layer; brightness by screen area; white only as a thin core |
| Effect looks muddy or flat | Grey darks, one hue, one value | Deep saturated ink, element body, hot core, one accent |
| Effect dark in caves, grey in shade | `LightInfluence` 1 | Set 0 on every emitter, beam and trail |
| Feels slow or floaty | Phases too long; sound peak late; feedback waits for the server | Cut every phase; flash under 50 ms; predict locally; align sound peak (`audio-sfx-music.md`) |
| Solid coloured slab instead of a slash | Beam texture not loaded | Preload on equip; hold transparent until loaded; wait out fresh uploads |
| Streak across the body, or a sheet around the character | Trail not cleared; trail window too wide | `Clear()` before enabling; marker window; crescent for sweeps over 120° |
| Outline stopped showing | Slot limit or a leftover Highlight on the model | Destroy unused; one arbiter per object |
| Fine alone, lags in a full server | No onlooker share or per-client cap | Others at half or less; global particle cap; distance and view culling for strangers |
| Hitch a few seconds after big moments | Instance churn | Pools with a cap |
| Phones lag only when the effect is near the camera | Overdraw from large transparent pieces | Shrink, raise transparency on the camera line, fewer stacked layers |
| Low graphics does not help | Bursts are not thinned by the engine | Own detail value on `EmitCount`; `MinDetail` layers |
| Flipbook shows one frame on old phones | Flipbooks disabled under memory pressure | Fewer sheets; first frame reads as a still |
| Caster sees effects late or twice | Caster waits for the echo, or the echo is not skipped | Play on input; server skips the caster |
| Aura or shield missing for some players | State sent as an event | Character attribute; each client starts its own visual |
| "Dodged but got hit" | Telegraph pop and damage on different frames or shapes | One shared shape table; damage at the pop |
| Light hits feel inconsistent on phones | 50 ms stops are 1–2 frames at 30 FPS | 66 ms or more where it matters; otherwise rely on sound and spark |
| Fast weapons feel sticky | Hit-stop adds up in flurries | Rolling 140 ms per 0.6 s budget; reserve for finishers |
| Shake reads as jitter, or is violent when zoomed | Noise above half the frame rate; no FOV scaling | Cap at 0.4 × FPS; scale by `tan(FOV/2)` |
| FOV drifts after long sessions | Exponential decays, several writers | Finite envelopes ending at 0; one owner |
| Motion sickness or flash complaints | No comfort settings; roll; strobing | §13 table; three-flash limit; replacement feedback |
| Fights unreadable | No readability budget; everyone's effects at full strength | One ground piece, 3 large pieces, 35% screen; onlookers reduced |

## Review gate

- [ ] Every effect is built on clients from one small validated payload; the caster predicts and the server skips the echo; states replicate as attributes.
- [ ] Each effect has a written layer table with flash, body, secondary, ground and tail, and a dark layer under every bright stack.
- [ ] `LightInfluence` set explicitly; emitters fire with `Emit`; streams at mobile rates; no per-frame emitter property writes.
- [ ] Beam and trail textures preloaded with their owner; trails cleared and windowed; arcs over 120° drawn as crescents.
- [ ] Highlights persistent, one owner per object, counted against a budget.
- [ ] VFX meshes are Blender kit pieces, non-colliding, pooled, with a 2–3 layer low version; textures greyscale, shared and counted.
- [ ] Timing checked against §7; effects fire from animation markers; telegraph drawing and server hit test share one shape table.
- [ ] Hit-stop is client-only, budgeted, one per swing; shake starts after the stop; FOV has one owner and returns to exactly 0.
- [ ] Pools capped; per-cast, per-caster and per-client budgets written; gameplay information never culled.
- [ ] Detail scales from the player's setting and measured frame time; verified on a hot 3 GB Android phone with 8 casters at one spot.
- [ ] Shake slider, screen-effects intensity, flash toggle, hit-stop toggle and reduced-motion path exist; at most 3 full-screen flashes per second.
- [ ] Reviewed in slow motion, at game camera distance, on a phone, in the darkest and brightest zones.

## Sources

Accessed 2026-11-10. "(read)" = opened; "(search summary)" = seen only through web search result text.

- Roblox/creator-docs at commit ccc2b01 (read): `content/en-us/effects/particle-emitters.md`, `effects/beams.md`, `effects/trails.md`, `effects/highlighting.md`, `environment/post-processing-effects.md`, `performance-optimization/improve.md`, `production/publishing/accessibility.md`; `reference/engine/classes/` `ParticleEmitter.yaml`, `Beam.yaml`, `Trail.yaml`, `Highlight.yaml`, `PostEffect.yaml`, `TweenService.yaml`, `UserGameSettings.yaml`, `GuiService.yaml`, `UnreliableRemoteEvent.yaml`, `MeshPart.yaml`, `HapticEffect.yaml`; `reference/engine/enums/SavedQualitySetting.yaml`. https://github.com/Roblox/creator-docs
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault, commit 43ba05d) (read): `07 Lighting VFX and Audio/` Particle Emitters In Depth; Beams and Trails; Highlights and Selection Effects; VFX Design Playbook; VFX Performance Budgets and Culling; Replicating VFX - Server Validates, Clients Render; AoE Telegraphs; Projectile VFX; Screen Damage Effects; Designing VFX Textures and Flipbooks in Figma; VFX Readability and Value; Escalation and Grandeur Without Clutter; Gore Policy and Kid-Friendly Hit Feedback (summaries of the last five). `47 Game Feel and Juice/` Hit-Stop and Screen Shake Tuning by Numbers; Feedback Timing; Juice on a Budget; Squash Stretch and Anticipation; Reward Moments; Input Responsiveness. `08 Animation/05 Systems/` VFX Timing with Animation; Camera Shake and Camera FX. `45 Procedural Blender Assets/Mesh VFX Packs Built in Blender`. `58 Player QoL and Game Tweaks/Comfort Toggles`. `42 Accessibility and Inclusive Design/Motion Sensitivity and Camera Comfort`. `skills/lihfolk-vfx/SKILL.md`.
- https://devforum.roblox.com/t/a-way-to-make-particleemitter-rate-ignore-graphics-quality/474762 and https://devforum.roblox.com/t/graphics-quality-affects-particle-emitters/2657543 (search summary; Emit and Rate versus graphics level)
- https://devforum.roblox.com/t/how-should-i-prevent-exploiters-spamming-my-remoteevent-for-vfx-replication/4749010, https://devforum.roblox.com/t/client-replication-101-the-guide-to-replicating-effects-to-clients/1789487, https://devforum.roblox.com/t/best-way-to-replicate-vfxanimations-for-a-battlegrounds-game-tsbjjs-style-architecture/4814813 (search summary; replication practice)
- https://devforum.roblox.com/t/animated-particles-with-the-particle-flipbooks-beta/1718023 and https://devforum.roblox.com/t/how-do-you-make-flipbook-particles-from-scratch/2645538 (search summary; flipbook sizes and tools)
- https://devforum.roblox.com/t/scrollable-textures-for-meshparts/2820890 (search summary; no UV scroll on MeshParts)
- https://devforum.roblox.com/t/damage-numbers-best-approach/3889210 and https://devforum.roblox.com/t/billboard-gui-causing-fps-lag/3542255 (search summary; BillboardGui overhead)
- https://devforum.roblox.com/t/springservice-drop-in-replacement-for-tweenservice-using-smoothdamp/3621210 (search summary; led to the `SmoothDamp` check in the docs)
- https://learn.microsoft.com/en-ie/gaming/accessibility/xbox-accessibility-guidelines/118 (search summary; photosensitivity) and https://www.w3.org/WAI/WCAG21/Understanding/three-flashes-or-below-threshold.html (cited through LihFolk; not opened)
- No evidence found: Reddit threads with concrete VFX numbers; an official Roblox statement on whether `Emit` bursts are thinned by graphics level; an official flash-rate rule.
