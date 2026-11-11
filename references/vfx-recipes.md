# VFX recipes: 22 effects, layer by layer

What this is: build sheets for the effects almost every Roblox game needs. Each recipe lists its layers in order with starting property values, timing in milliseconds, hex colours, the textures it uses, a phone budget, a cheap version, a showpiece version and the usual mistakes. Open it when you are about to build a specific effect. The reasons behind the numbers (principles, instance traps, timing table, hit-stop, replication, pooling, budgets, comfort) are in `vfx-and-juice.md` and are not repeated; reference images for most recipes are in `visual-library/vfx.md`.

**Status of the numbers.** Values tagged `[official]` come from Roblox's own tutorials; `[lihfolk]` and `[community]` come from the sources named in `vfx-and-juice.md`. Everything else is a `[house]` starting point, **untested in engine**: build it, capture it on a phone, compare with a reference frame by frame, then tune. No Luau here except names from the `HitFeel` module (`game-craft.md` §1.3); the play path is `FxPool.play` and animation markers from `vfx-and-juice.md` §6, §10 and §11.

**Fast route for one effect** (about 150 lines): this header, Conventions (curves, palette, kit with tonight stand-ins), then your recipe. A heavy hit on a standing target is recipe 3; a slam on the ground is recipe 4. Routes for other tasks: `vfx-and-juice.md` Fast routes.

## Contents

Start here by level · Conventions: curves, palette, kit, build it tonight · 1. Hit spark · 2. Melee slash · 3. Heavy melee hit · 4. Heavy impact (ground slam) · 5. Projectile · 6. Charge-up · 7. AoE telegraph and detonation · 8. Explosion · 9. Shockwave · 10. Aura or buff · 11. Heal · 12. Shield · 13. Dash · 14. Teleport · 15. Level-up · 16. Coin or reward burst · 17. Hatch or open reveal · 18. Footstep and landing dust · 19. Fire · 20. Lightning · 21. Water splash · 22. Environmental ambience · Review gate · Sources

## Start here by level

| Level | Do | Skip for now |
|---|---|---|
| Beginner | Build the **cheap version** of recipes 1, 16 and 18 with the first four kit textures (tonight stand-ins are fine). Block each in white, then colour | Meshes, flipbooks, showpiece versions |
| Intermediate | Build the full layer tables for your core verb (usually 2, 3, 4, 5 or 7). Model the five kit meshes in Blender once and reuse them everywhere | Showpiece versions except for the rarest moments |
| Expert | Add showpiece versions for the top one or two tiers only; write the importance sheet first (`vfx-and-juice.md` §1); score with the §16 rubric on a phone | — |

New game: build recipes in the order your loop needs them, cheap versions first, and upgrade only what the importance sheet rates 7 or more. Live game: capture your current effect, score it with the rubric, then change the lowest-scoring line using the matching recipe row.

## Conventions: curves, palette, kit, build it tonight

- Shorthand: `Life` = `Lifetime` in seconds; `Spd` = `Speed` in studs/s; `Acc` = `Acceleration`; `LE` = `LightEmission`; `Br` = `Brightness`; `Emit n` = burst with `Enabled = false`; `Rate n` = stream; a beam's `Width` = `Width0` and `Width1`. Every emitter sets `LightInfluence` explicitly (0 unless a row says otherwise) and `Rotation` 0–360 unless a row says otherwise. Sizes assume a 5-stud character and a third-person camera 15–25 studs away. Windows are milliseconds from the trigger (animation marker or contact = 0); negative means before it.
- Sequences: `a → b` = keypoints (0, a) (1, b); `a → b → c` = (0, a) (0.5, b) (1, c); explicit keys are written `(time, value)`. Colour sequences use the same notation with hex. Mesh changes such as "scale 0.2 → 1 in 150 ms" are client tweens with `Quad`, `Out` unless stated.
- Named curves. Size: `POP(S)` = (0, 0.2·S) (0.15, 0.8·S) (1, S), fast in, eased out; `SHRINK(S)` = (0, S) (1, 0). Transparency: `FADE` = (0, 0) (0.6, 0.3) (1, 1); `HOLD` = (0, 0) (0.6, 0) (1, 1); `INOUT` = (0, 1) (0.15, 0) (0.7, 0.4) (1, 1); `FLICKER` = (0, 0) (0.15, 0.6) (0.3, 0.1) (0.45, 0.7) (0.6, 0.2) (0.8, 0.6) (1, 1). Colour: `RAMP` = (0, hot) (0.35, body) (1, dark). Squash: `STREAK` = −1 constant with `VelocityParallel` (the docs' rain uses ±3 and flips the sign for `VelocityParallel` `[official]`; check the direction with an arrow texture).
- Budget line: particles alive at peak for your own cast at full detail (the low tier multiplies bursts by 0.4), pooled meshes, lights. Others' casts run at half and lose decoration layers.

**Palette** (example values, the same as sheet 12; roles from the ramp table in `vfx-and-juice.md` §1). Greyscale value bands: core 95–100%, hot 80–95%, body 50–80%, dark 10–25%; if your swap breaks a band, the effect loses its value structure.

| Row (use for) | core | hot | body | dark | spark | debris |
|---|---|---|---|---|---|---|
| Steel (weapon hits, no element) | `#FFFFFF` | `#E6F6FF` | `#6FB7FF` | `#141A33` | `#FFB347` | `#5A6478` |
| Fire | `#FFF6DD` | `#FFC83D` | `#FF6A1A` | `#6B1220` | `#FFD98A` | `#3A2420` |
| Ice | `#FFFFFF` | `#BFEFFF` | `#55B8F0` | `#12305E` | `#E6FAFF` | `#7FA6C4` |
| Lightning | `#FFFFFF` | `#FFF29A` | `#8FD0FF` | `#1B1F5C` | `#FFF9D1` | `#3A3F6B` |
| Nature, heal | `#F4FFD6` | `#C6F26B` | `#4FB83A` | `#0F3D2A` | `#E3FF9C` | `#5A4630` |
| Water | `#FFFFFF` | `#B8F0FF` | `#2F9BE0` | `#0C2A5A` | `#DDF7FF` | `#6F93B5` |
| Arcane, teleport | `#FFFFFF` | `#E7C6FF` | `#A05BF0` | `#2A0F52` | `#F3E1FF` | `#4A3A66` |
| Gold (coins, level-up, holy) | `#FFFDF2` | `#FFE58A` | `#F2B632` | `#5A3A0A` | `#FFF3B0` | `#8A6A2A` |
| Earth (slams, rock) | `#FFF4DC` | `#E8C98A` | `#A8743A` | `#3A2414` | `#FFE0A0` | `#6B4A2E` |

Allegiance (primary layer only): ally `#2F8CFF`, enemy `#E5333B`; both sit near 50% value, so they differ by hue alone and must also differ by shape (`vfx-and-juice.md` §1). Floor-tinted layers (dust, footsteps): the floor's colour × 0.8.

| Kit texture (greyscale, painted for the game) | Size | Used by | Tonight stand-in |
|---|---|---|---|
| `soft_dot` radial glow | 128² | Cores, glows, motes | Engine `rbxasset://textures/particles/explosion01_implosion_main.dds` (soft white dot), or tutorial `rbxassetid://3845808160` |
| `hard_dot` hard-edged disc | 128² | Flat sparks, coins, bubbles | A hard circle from the Kenney Particle Pack |
| `spark_streak` soft elongated oval, painted horizontal | 128² | Sparks, embers, rain, speed lines with `VelocityParallel` and `STREAK` | Tutorial embers `rbxassetid://17581858560` or spark `rbxassetid://6101261905` |
| `star4` four-point flash | 256² | Hit frames, muzzle flashes, glints | Engine `rbxasset://textures/particles/sparkles_main.dds` (the emitter's default eight-point sparkle) |
| `ring_drawn` irregular hand-drawn shock ring | 512² | Impacts, explosions, level-up | A ring from the Kenney pack; else the engine ring below |
| `ring_thin` clean thin ring | 512² | Telegraph rims, auras, shields | Engine `rbxasset://textures/particles/explosion01_shockwave_main.dds` (soft ring) |
| `slash_streak` hand-painted streak, tips fading | 512×256 | Crescents, trails, beams | A slash from the Kenney pack |
| `puff_set` four flat smoke puffs with an inner shadow shape (2×2) | 512² | Dust, smoke, fire body | Engine `rbxasset://textures/particles/smoke_main.dds` (one puff: set `Rotation` 0–360, no flipbook) or tutorial smoke `rbxassetid://16830673704` |
| `splash_set` four splash shapes (2×2) | 512² | Water, liquid hits | Tutorial splashes `rbxassetid://17363668312`, `rbxassetid://17363669906`; droplets `rbxassetid://17082061238` |
| `crack_decal` radial ground cracks | 512² | Impact and explosion residue | None: skip residue tonight |
| `noise_tile` tiling streaky noise | 256² | Shields, beams, scrolling layers | None: use the rim and hit flash only |
| `glow_gradient` soft vertical gradient strip | 256² | Pillars, rays, light shafts | A flare from the Kenney pack, or skip the pillar |

Kit meshes (Blender, `vfx-and-juice.md` §5): crescent band, flat ring, disc with sector variants, dome shell, pillar, crossed ribbons, shard set. Twelve textures and seven meshes build every recipe below; until the meshes exist, use each recipe's cheap version (flat cards and beams).

**Build it tonight** (no textures or sounds of your own yet). Three legitimate texture sources, in this order:
1. **Engine textures** (`rbxasset://textures/particles/…`): files inside every Roblox client, so they need no upload or moderation and load at once. The docs name only the default "white sparkle"; the other file names come from a community mirror of the client files (Roblox-Client-Tracker, 2026-11-10) and were viewed for this table `[VS]`. They are Roblox's own engine content, used inside Roblox as the engine itself uses them; never export them.
2. **Roblox tutorial textures** (`rbxassetid://…`): image assets that the official VFX tutorials tell you to paste into `Texture` (IDs as printed in the docs; not loaded here). Images are Open Use by default, meaning any creator or game may use them `[official]`.
3. **Kenney Particle Pack**: 80 sprites, CC0 (no credit, commercial use; page read 2026-11-11, `visual-library/vfx-learning.md` row 48). Upload the sprites you use under the game's owner.

Make stock look designed: tint every texture from one palette row (they are white or grey); put a dark copy (same texture, the row's dark, LE 0, ZOffset −0.5, 1.3× size) behind every bright layer; use `POP`, `SHRINK` and `STREAK` instead of constant sizes; build the cheap version first. Stock shapes are still the first generic tell (`vfx-and-juice.md` §14): **replace first** `star4` and `slash_streak` (they are the silhouette of every hit), then `puff_set` (stock smoke is the most recognisable), then `ring_drawn`; soft dots and glows can stay longest. Sounds tonight: Roblox-published Creator Store audio found by creator name (steps in `audio-sfx-music.md` §3), or Kenney's CC0 Impact Sounds and RPG Audio packs; replace your core verb's impact transient first.

## 1. Hit spark (light hit, several per second)

Read: "that connected, in that direction". No hit-stop, no shake at this tier.

| Layer | Build | Window |
|---|---|---|
| Flash card (primary) | `star4`, Emit 1, Life 0.05–0.07, Size `SHRINK(2.5–3)` (about 0.6× the target's width), Color `#FFFFFF`, LE 1, Br 4, ZOffset +1 | 16–70 |
| Directional sparks | `spark_streak`, `VelocityParallel`, Emit 6–10, Life 0.15–0.3, Spd 25–40, Drag 8–10 (official spark burst uses Spd 20–40, Drag 10, Life 0.2–0.6 `[official]`), SpreadAngle 25,25 around the swing direction, Size `SHRINK(0.4)`, Squash `STREAK`, Transparency `HOLD`, Color `#FFE7A8 → #FF8A2E`, LE 1, Br 6 | 0–300 |
| Dark puff | `puff_set` (Grid2x2, `FlipbookMode` Random, framerate 0), Emit 1–2, Life 0.25–0.35, Size `POP(2)`, LE 0, Color `#141A33`, Transparency 0.4 → 1, ZOffset −0.5 | 0–350 |
| Target response | Persistent Highlight: FillColor `#FFFFFF`, FillTransparency 1 → 0.5 → 1 over 80–120 ms; sound with pitch variation | 0–120 |

- Colour (Steel row; swap the row for an element): white flash, warm accent sparks, blue-black puff. Kid-friendly: no red spray.
- Budget: about 12 alive, no meshes, no light. Cheap: flash plus 4 sparks. Showpiece (crit): add `ring_drawn` on a flat card growing 0 → 4 studs in 120 ms and a number popup.
- Mistakes: radial sparks; flash larger than the target; anything living past 400 ms on an effect that fires three times a second; hit-stop on light hits.

## 2. Melee slash

Read: the arc is the hit area; the leading edge is where it is now.

| Layer | Build | Window |
|---|---|---|
| Anticipation glint | `star4` on the blade tip, Emit 1, Life 0.06–0.08, Size `SHRINK(1)`, Color hot, LE 1, Br 4 | −120 to −40 |
| Crescent body (primary) | Crescent band mesh with `slash_streak` tinted body, appears at the `TrailOn` marker, scale 0.85 → 1.05 in 120 ms (ease out), Transparency 0 → 1 between 120 and 220 ms, texture slid toward the tip. Angle and radius equal the hit test | 0–220 |
| Hot edge | Smaller copy (85% width) at the leading edge, tinted core with the emissive mask on (`SurfaceAppearance`, `vfx-and-juice.md` §5), Transparency 0 → 1 over 80–100 ms | 0–100 |
| Dark trailing edge | Same mesh tinted dark, no emissive, appears at +30, Transparency 0.2 → 1 by 260 ms | 30–260 |
| Blade trail (arcs under 120°) | `Trail` between two blade attachments, Lifetime 0.12–0.18, `WidthScale` 1 → 0, Color body → dark, Transparency 0.2 → 1, LE 0.6, `Clear()` then enable for the cut window only | 0–180 |
| Sparks | `spark_streak`, `VelocityParallel`, Squash `STREAK`, Emit 4–8 along the swing tangent, Life 0.2–0.35, Spd 15–25, Drag 6, Size `SHRINK(0.35)`, Transparency `HOLD`, Color spark, LE 1, Br 6 | 0–350 |

- Colour (Fire row, as drawn on sheet 11): core `#FFF6DD`, hot `#FFC83D`, body `#FF6A1A`, dark trailing shape `#6B1220` that outlives the light, sparks `#FFD98A`. The crescent body is `#FF6A1A`; flat colours read better than gradients at phone size.
- Budget: 2–3 pooled meshes, under 10 particles. Cheap: trail plus flash. Showpiece: one thin straight speed line across the arc for 2 frames, a dust line on the ground under the arc, embers lingering 400–600 ms.
- Mistakes: trail wrapping the character; ribbon of uniform width and brightness; crescent pivot left at the bounding-box centre; arc drawn wider than the hitbox; body visible beyond 250 ms; additive only.

## 3. Heavy melee hit (sword, axe or hammer on a standing target)

Read: "that blow landed hard, on that target, from that way". Assumes a third-person camera, a 5-stud character and a heavy attack whose `Hit` marker lands 0.5–0.7 s after input (markers on sheet 21). Heavy tier from `vfx-and-juice.md` §7; Steel row (swap the row for an element). Emitters sit on attachments of one invisible anchored host part (`vfx-and-juice.md` §3). Bright for about 100 ms of 1,350: that ratio is the weight.

| Layer, in firing order | Build | Window |
|---|---|---|
| Wind-up sound | `windup` cue (table below), started at −450 so its swell peaks about −40 (start = beat − peak) | −450 to −40 |
| Glint | `star4` on the blade-tip attachment, Emit 1 at two `Glint` markers (−300 and −120), Life 0.07, Size `SHRINK(1.2)`, Color `#E6F6FF`, LE 1, Br 4, ZOffset 0.5 | −300 to −50 |
| Trail | `Trail` between two blade attachments, Lifetime 0.15, `WidthScale` 1 → 0, Color `#6FB7FF`, Transparency 0.2 → 1, LE 0.6; `Clear()` then enable at `TrailOn`, disable at `TrailOff` and on the track's `Stopped` | −100 to +80 |
| Crescent (primary) | Tonight a `Beam`: `FaceCamera`, `slash_streak`, `TextureMode` Stretch, `TextureSpeed` 0, Width0 0.2, Width1 2.4, Segments 40, Color `#6FB7FF → #E6F6FF` (bright at the leading end), Transparency (0, 1) (0.3, 0.1) (1, 0.1), LE 0.7; both attachments' +X along the swing; a 100° arc of radius 5 needs `CurveSize0 = CurveSize1 = 4/3 × tan 25° × 5 = 3.1`. Arc and radius equal the hit test. Tween `LocalTransparencyModifier` 0 → 1 from +120 to +220 | −100 to +220 |
| Impact sound | `impact_transient`, `impact_body` and `impact_tail` together on the contact frame, as the stop begins; never paused by it | 0 |
| Hit-stop | `HitFeel.stop(track, 0.066, 1)`: the attacker's track at 0.12× for 66 ms, then 1.88× for 66 ms. Attacker's client only | 0–132 |
| Contact flash | `star4`, Emit 1, Life 0.05, Size `SHRINK(4)`, Color `#FFFFFF`, LE 1, Br 5, ZOffset 1 | 16–66 |
| Dark star | `star4`, Emit 1, Life 0.07, Size `SHRINK(2)`, Color `#141A33`, LE 0, Br 1, ZOffset 1.5: the dark shape inside the white is the punch (`visual-library/vfx.md` row 25) | 16–86 |
| Light | `PointLight` on the contact attachment, Color `#E6F6FF`, Range 12, `Shadows` false, Brightness 3 → 0 in 100 ms | 0–100 |
| Sparks | `spark_streak`, `VelocityParallel`, Squash `STREAK`, Emit 20, Life 0.2–0.45, Spd 30–45, SpreadAngle 25,25, Drag 9, Acc (0, −20, 0), Size `SHRINK(0.5)`, Transparency `HOLD`, Color `#FFE7A8 → #FFB347 → #FF6A1F`, LE 1, Br 6. `EmissionDirection` Top with the attachment's +Y along the blade's travel at contact: never radial | 0–450 |
| Dark puff | `puff_set` (Grid2x2, `FlipbookMode` Random, framerate 0, `FlipbookStartRandom`), Emit 3, Life 0.3–0.4, Spd 2–4, SpreadAngle 40,40, Drag 3, Size (0, 0.6) (0.15, 2.4) (1, 3), Transparency 0.4 → 1, Color `#141A33`, LE 0, ZOffset −0.5 | 0–400 |
| Target flash | The target's one persistent `Highlight`: FillColor `#FFFFFF`, OutlineTransparency 1, DepthMode Occluded; FillTransparency set to 0.35 at contact, tweened back to 1 over 120 ms | 0–120 |
| Dust skirt | `puff_set` on a flat 4 × 0.2 × 4 host part at the target's feet: Shape Disc, `ShapeStyle` Surface, `ShapeInOut` Outward, `ShapePartial` 0.9; Emit 6 at +30, Life 0.4–0.7, Spd 12–18, Drag 3, Size `POP(5)`, Transparency (0, 0.3) (0.5, 0.5) (1, 1), Color floor × 0.8, LE 0, LightInfluence 0.3 | 30–700 |
| Kick | When the stop releases: `HitFeel.kick(swingDirection, 0.5)`: 0.4° at FOV 70, eased back over 150 ms | 66–216 |
| Shake | Same moment: `HitFeel.addTrauma(0.75)`: peak 1.1° (up to 5 px on `Phone-S`), pitch and yaw only, back to exactly 0 at about +366 | 66–366 |
| Embers | `spark_streak`, `VelocityParallel`, Emit 4 at +200, Life 0.5–0.7, Spd 4–8, SpreadAngle 60,60, Drag 2, Acc (0, −12, 0), Size `SHRINK(0.25)`, Transparency `FLICKER`, Color `#FF6A1F`, LE 1, Br 4 | 200–900 |
| Impact frame (optional) | One `ColorCorrectionEffect` on the camera, Saturation −1, Contrast 0.35, Brightness 0.12, on for 45 ms from contact; attacker only, through the flash gate (2 per second), off with flashes off or reduced motion | 0–45 |

| Sound cue | Content | Length | Volume | Variation |
|---|---|---|---|---|
| `windup` | Low air whoosh with a 30–60 ms swell; never trimmed to its loudest sample | 350–450 ms | 0.5 | Pitch ±3% |
| `impact_transient` | Sharp metal crack layered with a low thud | 5–60 ms | 1.0 | 3 takes in a shuffle bag, pitch ±4% |
| `impact_body` | Metallic ring or heavy swish | 100–300 ms | 0.7 | The transient's pitch |
| `impact_tail` | Lower, quieter whoosh, trimmed at −60 dB so the hit ends under 0.6 s | 300–500 ms | 0.4 | None |

- Sound rules (`audio-sfx-music.md` §5–6): files normalised alike (−18 LUFS momentary maximum, −1 dBTP), transient within 5 ms of file start (or `TimePosition` set to the onset), loaded on equip; music ducked 4 dB for 400 ms. A phone speaker plays little below 300 Hz, so the crack carries the hit on phones and the thud on headphones. Predict only the neutral contact; kill, crit and block sounds wait for the server.
- Others' screens (one small server event, skipping the attacker): flash, sparks, dark puff and a quieter 3D impact (min 6, max 100 studs); no stop, no kick, no impact frame; trauma × 0.3 with the §7 falloff.
- Budget: about 34 alive at peak, 1 beam, 1 trail, 1 light, 1 Highlight. Phone (low tier): bursts × 0.4 (sparks 8, puff 1); drop dark star, dust, embers, light and impact frame; keep the flash, sparks, crescent, target flash, all the sound and the camera. Showpiece (finisher tier: 75 ms, trauma 0.85): the crescent as a Blender band mesh (120°, under 100 triangles, UVs straight along the arc) in three copies (hot edge `#FFFFFF` 0–100, body `#6FB7FF` 0–220, dark `#141A33` 30–260), one straight speed line across the arc for 2 frames, `crack_decal` under the target.
- Tonight: every texture has a stand-in in the kit table; the crescent beam takes a Kenney slash, the flash and dark star the engine sparkle.
- Mistakes: trail on for the whole swing; radial sparks; a ground ring under a standing target (that is recipe 4); shake or kick during the stop; the old trauma 0.25 (0.125°: invisible on a phone); all layers additive with no dark star or puff; a Highlight created per hit; 20–80 ms of silence at the start of the impact file; stop, kick or impact frame on the victim's or onlookers' screens.

## 4. Heavy impact (ground slam)

Read: big, here, now; the ring edge is the damage radius.

| Layer | Build | Window |
|---|---|---|
| Anticipation | Weapon glow or recipe 6 at low strength | −300 to 0 |
| Hit frame | `star4` or `soft_dot`, Emit 1, Life 0.05, Size `SHRINK(4–5)`, Color core, LE 1, Br 5; optional `PointLight`, Color hot, Brightness 3 → 0 in 100 ms, Range 12, shadows off | 16–66 |
| Hit-stop, then shake | Heavy tier (`vfx-and-juice.md` §7): `HitFeel.stop` 66 ms; when it releases, `HitFeel.addTrauma(0.75, true)` (the ground moved: rotation plus offset) and a 0.5% kick straight down | 0–66, then 66–366 |
| Ring (primary) | Flat ring mesh with `ring_drawn`, Color hot, scale 0.2 → 1 (the damage radius) in 150 ms, Transparency 0 → 1 from 120 to 320 ms | 0–320 |
| Dust ring | `puff_set`, Shape Disc with `ShapePartial` 0.9, outward, Emit 10–14, Life 0.4–0.7, Spd 12–18, Drag 3, Size `POP(4–6)`, LE 0, LightInfluence 0.3, Color floor × 0.8, Transparency 0.3 → 1 | 30–700 |
| Debris | `hard_dot` or shard sprites, Emit 6–10, Spd 20–30, SpreadAngle 60,60 upward, Acc (0, −60, 0), Life 0.5–0.8, Size 0.3–0.6 (constant), Color debris, LE 0, LightInfluence 0.5, RotSpeed ±180 | 0–800 |
| Residue | Disc mesh with `crack_decal`, Color dark, Transparency 0.2 → 1 over 1.2–2 s | 50–2,000 |

- Colour (Earth row): core `#FFF4DC`, ring `#E8C98A`, debris `#6B4A2E`, residue `#3A2414`; dust from the floor.
- Budget: about 30 alive, 2 meshes, 0–1 light. Cheap: hit frame, one flat ring card (`VelocityPerpendicular`, Spd 0.01) and 6 dust puffs. Showpiece: Blender rock chunks rising in a ring then sinking, a second ring at +80 ms and 70% size, glowing cracks that cool to dark.
- Mistakes: perfectly even ring; debris in a full sphere instead of a hemisphere; residue brighter than the hit; shake during the stop; ring drawn larger than the server radius.

## 5. Projectile (cast, travel, hit)

Read: where it is, where it came from, how wide it is. The hot point is the hit volume.

| Layer | Build | Window |
|---|---|---|
| Cast | `star4` 1–2 studs ahead of the hand, Emit 1, Life 0.05, Color core, LE 1; two `ring_thin` cards (`VelocityPerpendicular`) moving along the shot direction, Spd 8, Life 0.15, Size `POP(1.5)`, Transparency `FADE`, Color hot | 0–150 |
| Hot point (primary) | `hard_dot` or a small core mesh, diameter = server hit diameter, Color hot (a core-coloured centre painted in or a second smaller dot), LE 1; `LockedToPart`, Rate 20, Life 0.1, Transparency 0 | Travel |
| Glow and shadow | `soft_dot` in the body colour (LE 1) over a larger dark `soft_dot` (LE 0, ZOffset −0.5): the dark buys the glow | Travel |
| Trail | `Trail`, Lifetime = (12 to 30 studs) ÷ speed, `WidthScale` 1 → 0, Color body → dark, Transparency 0.1 → 1, LE 0.5 | Travel |
| Shed motes (secondary) | `soft_dot`, Rate 12–15, Life 0.3–0.5, Spd 0–1, Size `SHRINK(0.3)`, Transparency `FADE`, Color spark, LE 1, Br 2: they outlast the trail | Travel +500 |
| Hit | Recipe 1 scaled up: hit frame about 100 ms, sparks continuing the direction of travel, ring perpendicular to it, motes last | 0–600 |

- Colour (Water row): hot point `#B8F0FF`, glow `#2F9BE0` over dark `#0C2A5A`, trail `#2F9BE0 → #0C2A5A`, motes `#DDF7FF`. In PvP the hot point's rim takes the allegiance colour.
- Budget: at most 15 alive per projectile in flight; cap live projectiles through the pool. Cheap: core, trail, flash. Showpiece: a unique silhouette (teardrop core mesh, a motif in the trail), a spiralling second trail.
- Mistakes: hot point offset from the server position; trail too long (laser) or too short (dot); muzzle flash on the hand hiding the character; visuals moved by the server; identical ally and enemy projectiles in PvP.

## 6. Charge-up

Read: power is gathering; a clear "ready" beat.

| Layer | Build | Window |
|---|---|---|
| Inward specks | Host part 8–10 studs wide, Shape Sphere, `ShapeStyle` Surface, `ShapeInOut` Inward, `spark_streak`, `VelocityParallel`, Rate 15–20, Life 0.35–0.5, Spd = radius ÷ Life (about 12 for a 5-stud radius) so they die at the centre, Size `SHRINK(0.3)`, Squash `STREAK`, Transparency `INOUT`, Color hot, LE 1, Br 3 | Hold |
| Core | `soft_dot`, `LockedToPart`, 1 alive (Rate 4, Life 0.25), Size set from the charge (0.5 at start, 2 when full), Color core, LE 1, over a dark `soft_dot` 1.5× its size (Color dark, LE 0, ZOffset −0.5) | Hold |
| Imploding ring | `ring_thin` card (`VelocityPerpendicular`, Spd 0.01), Life 0.3, Size `SHRINK(6)`, Color body, LE 1, once per charge tier | Tier steps |
| Ready glint | `star4`, Emit 1, Life 0.08, Size `SHRINK(2)`, Color core, LE 1; specks switch from hot to core; `HitFeel.kick` 0.25% | Full charge |

- Colour (Arcane row): specks `#E7C6FF` (then `#FFFFFF` when ready), core `#FFFFFF` over `#2A0F52`, ring `#A05BF0`.
- Timing: if the charge also hides a server round trip, the loop holds at least 300–600 ms `[lihfolk]`. Replicate as a character attribute so others see it at reduced detail.
- Budget: about 10 alive. Cheap: core plus specks at Rate 8. Showpiece: three audible and visible tiers, FOV −3° eased in, small arcs between the hands.
- Mistakes: outward particles (reads as a leak); charge longer than the move deserves; glow covering the character; no release payoff.

## 7. AoE telegraph and detonation

Read: exactly where, and exactly when. Never culled, never simplified below outline, fill and pop.

| Layer | Build | Window |
|---|---|---|
| Dark outline | Two semicircle `Beam`s (`CurveSize0` and `CurveSize1` = 1.333 × r), Width 0.6, LE 0, Color dark, Segments 40 | 0 → T |
| Base fill | Disc mesh, Color allegiance, Transparency 0.78 | 0 → T |
| Progress fill (primary) | Second disc scaling 0 → 1 over T with `Quad`, `In`, Color allegiance, Transparency 0.55, a `ring_thin` card in the rim colour on its leading edge | 0 → T |
| Bright rim | Ring beams, Width 0.4, Color rim, LE 1, centred on the exact server radius, `ZOffset` above the outline. Both widths keep the line at about 6 px or more at a 20-stud phone camera (`vfx-and-juice.md` §1); widen for a higher camera | 0 → T |
| Pop | Both fills switch to `#FFFFFF` at Transparency 0.2 on the damage frame, then Transparency → 1 in about 220 ms `[lihfolk]` | T → T+220 |
| Detonation | Recipe 8 or 9 scaled to r | T → |

- T = 250 ms reaction + escape distance ÷ 16 studs/s (+100–200 ms for touch): r = 10 gives 0.9 s minimum, 1.1–1.4 s comfortable `[lihfolk]`. One shape table feeds both this drawing and the server hit test.
- Colour and value: outline for bright floors, rim for dark floors, both always. Enemy: outline `#2A0A0E`, fills `#E5333B`, rim `#FFB3B8`, hard or dashed. Ally: outline `#0A1A33`, fills `#2F8CFF`, rim `#BFE0FF`, smooth (heal zones: recipe 11).
- Budget: 4 beams and 2 meshes; cap concurrent telegraphs per client by simplifying to outline, fill and pop, never by skipping. Cheap: outline ring, fill disc, pop. Showpiece: a motif inside the disc (cracks, runes), motes rising at the rim, a sky warning line as in recipe 20.
- Mistakes: linear fill (the last 200 ms cannot be judged); drawn radius differs from the server's; additive fill on a bright floor; fill so opaque it hides other hazards; hidden on low settings.

## 8. Explosion (stylised)

Read: one bright beat, then smoke. The fireball is a quarter of the timeline.

| Layer | Build | Window |
|---|---|---|
| Hit frame | `soft_dot`, Emit 1, Life 0.05, Size `SHRINK(0.6 × body)`, Color `#FFFFFF`, LE 1, Br 6; `PointLight`, Color hot, Brightness 4 → 0 in 100 ms, Range 16, shadows off | 16–66 |
| Fire body (primary) | `puff_set`, Emit 5–8, Life 0.3–0.45, Size `POP(5–7)`, Spd 6–10, Drag 4, Color `RAMP`, Transparency `FADE`, LE 0.6, ZOffset +0.5 | 0–450 |
| Streak lines | `spark_streak`, `VelocityParallel`, Squash `STREAK`, Emit 10–14 at uneven angles, Spd 40–60, Drag 10, Life 0.15–0.25, Size `SHRINK(0.6)`, Transparency `HOLD`, Color spark, LE 1, Br 6 | 0–250 |
| Ring | Flat ring mesh with `ring_drawn` tinted hot, scale 0.2 → 1.3 × body radius in 180 ms, Transparency 0 → 1 from 150 to 300 ms | 0–300 |
| Smoke | `puff_set`, Emit 4–6, Life 0.8–1.2, Size `POP(6–8)`, Acc (0, 3, 0), LE 0, Color debris → dark, Transparency 0.2 → 1, ZOffset −1 | 80–1,200 |
| Embers | `spark_streak`, Emit 8–12, Life 0.6–1.2, Spd 8–14, Acc (0, −15, 0), Drag 0.8, Size `SHRINK(0.3)`, Squash `STREAK`, Transparency `FLICKER`, Color spark → body, LE 1, Br 6 (official ember set-up: `VelocityParallel` with Squash, Drag 0.8 `[official]`) | 0–1,200 |

- Colour (Fire row): hit frame `#FFFFFF`; body `RAMP` = (0, `#FFC83D`) (0.35, `#FF6A1A`) (1, `#6B1220`); streaks `#FFD98A`; ring `#FFC83D`; smoke `#3A2420 → #6B1220`; embers `#FFD98A → #FF6A1A`. Smoke darker than the fire, never the same colour.
- Hit-stop and shake by tier from the hit's strength value (`vfx-and-juice.md` §7); a ground blast passes `moved = true`.
- Budget: about 45 alive, 1 mesh, 1 light. Cheap: hit frame, 4 puffs, 6 streaks. Showpiece: a 4×4 OneShot flipbook as the body (Life 0.4), second delayed ring, Blender debris, `crack_decal` scorch for 2 s.
- Mistakes: everything additive; smoke the same colour as the fire; evenly spaced radial streaks; total over 1.4 s; a unique 1024² flipbook per explosion type.

## 9. Shockwave

Read: a force front passing a radius.

| Layer | Build | Window |
|---|---|---|
| Ring (primary) | Flat ring mesh with `ring_drawn` tinted hot, scale 0.2 → 1 over 200–300 ms, band thinning as it grows (scale the mesh's height to 0.4 as it widens), Transparency 0 → 1 over the last 60% | 0–300 |
| Leading edge | `ring_thin` card, Color core, LE 1, 3% ahead of the ring, same curve, Transparency 0 → 1 by 200 ms | 0–200 |
| Ground dust | `puff_set`, Disc with `ShapePartial` 0.95, Emit 8–12, Spd 20, Drag 6, Life 0.3, Size `POP(2.5)`, Transparency `FADE`, Color floor × 0.8, LE 0, LightInfluence 0.3 | 20–350 |
| Dome (3D blast only) | Dome shell mesh tinted body, scale 0.3 → 1 in 200 ms, Transparency 0.6 → 1 | 0–250 |

- Colour: the source's row (Earth for a stomp: ring `#E8C98A`, edge `#FFF4DC`, dome `#A8743A`).
- Budget: 1–2 meshes, about 12 alive. Cheap: one flat card particle (`VelocityPerpendicular`, Spd 0.01, Life 0.25, Size 0 → 2r). Showpiece: a second ring at +80 ms and 70% size, short radial streak cards. Screen-space distortion is not available on Roblox; do not fake it with stacked transparent layers.
- Mistakes: constant band thickness; linear growth; opaque band over players; visual radius beyond the real one.

## 10. Aura or buff (state)

Read: this character has a status, and which kind. Driven by a character attribute, so late joiners see it.

| Layer | Build | Window |
|---|---|---|
| Start burst | `ring_thin` card (`VelocityPerpendicular`, Spd 0.01), Life 0.3, Size `POP(5)`, Transparency `FADE`, Color hot, LE 1; plus 6 motes | 0–300 |
| Ground ring (primary) | `ring_thin` on a flat ring mesh or two beams under the feet, slow rotation or `TextureSpeed` 0.1, Color body, Transparency 0.6 | Loop |
| Motes | `soft_dot` or the element's secondary shape, host Cylinder Surface sized to the character, Rate 6–10, Life 0.8–1.2, Spd 2–3 upward, Size `SHRINK(0.25)`, Transparency `INOUT`, Color spark, LE 0.6, Br 2 | Loop |
| End puff | 4 motes outward, ring fades in 200 ms | End |

- Buff versus debuff must differ by more than hue: buffs rise, are smooth and light (Gold or Nature row: ring `#F2B632`, motes `#FFF3B0`); debuffs fall or drip, are jagged and dark (Arcane row darkened: ring `#2A0F52` at Transparency 0.4, motes `#A05BF0`, Acc (0, −3, 0)).
- Budget: at most 12 alive per aura; others' auras at half rate; sleep beyond 160 studs. Parent to a helper part outside the character model, welded to it, or it disappears in first person `[official]`. Cheap: ground ring plus 4 motes a second. Showpiece: orbiting element shapes on a ring beam, a pulse synced to the remaining duration.
- Mistakes: covering the character's silhouette; constant bright additive glow; sent as a one-time event; never ends; every buff identical.

## 11. Heal

Read: friendly and soft. No sharp shapes, no flame; green by convention `[community]` (Riot).

| Layer | Build | Window |
|---|---|---|
| Ground ring | `ring_thin` on a flat ring mesh, Color `#4FB83A`, scale 0 → r in 250 ms, hold, Transparency 0 → 1 over the last 400 ms | 0–900 |
| Light column | Pillar mesh or vertical beam with `glow_gradient`, Color `#C6F26B`, Transparency 0.7 → 1 | 100–700 |
| Rising motes or petals (secondary) | `soft_dot` or a leaf shape, Emit 8–12 (or Rate 12 for 0.5 s), Life 0.8–1.2, Spd 3–5, Acc (0, 2, 0), Size 0.3–0.5 with Transparency `INOUT`, RotSpeed ±40, Color `#E3FF9C → #F4FFD6`, LE 0.5 | 100–1,300 |
| Target response | Highlight FillColor `#E3FF9C`, FillTransparency 1 → 0.6 → 1 over 150 ms; "+N" popup in `#4FB83A` with a dark outline | 150–400 |

- Timing is slow and low-contrast on purpose: 250 ms in, 600–900 ms total.
- Budget: about 14 alive, 1–2 meshes. Cheap: ring, 6 motes, popup. Showpiece: a growth motif (vines or flowers blooming along the ring), a small rising tick on every ally healed.
- Mistakes: star or spike shapes; red or orange; a pillar bright enough to hide the target; symbols with unwanted meanings (a pentagram reads as hostile).

## 12. Shield (state, hit response, break)

Read: protected; that hit was absorbed; now it is gone.

| Layer | Build | Window |
|---|---|---|
| Appear | Sphere shell mesh a little larger than the character, scale 0.8 → 1.05 → 1 in 180 ms (`Back`, `Out`) | 0–180 |
| Shell (primary) | `noise_tile` on a `Texture`, lines panning downward (`OffsetStudsV` tween), Color body, Transparency 0.8; non-colliding, `CanQuery = false` | Loop |
| Rim | `ring_thin`, `LockedToPart`, 1 alive (Rate 2, Life 0.5), Size = shell diameter, Transparency `INOUT`, Color hot, LE 1 | Loop |
| Hit response | `soft_dot` flash (Color core, Size `SHRINK(2)`, Life 0.08) and a `ring_thin` ripple (Size `POP(3)`, `FADE`, Color hot) at the hit point; shell Transparency 0.8 → 0.5 → 0.8 in 150 ms | 0–200 |
| Break | Blender shard set bursting outward 300 ms, `star4` hit frame, glass-like sound | 0–400 |

- Colour (Ice or Water row): shell `#55B8F0`, rim `#BFEFFF`, flash `#FFFFFF`, shards `#BFEFFF` with a `#12305E` copy behind.
- Budget: 1–2 meshes per shielded character, about 3 alive; fade the shell for its owner in first person (`LocalTransparencyModifier`). Cheap: rim ring plus hit flash. Showpiece: hex pattern texture, a directional ripple travelling from the hit point, shards that catch the allegiance colour.
- Mistakes: an opaque bubble hiding the character; looks like recipe 10; no hit response, so nobody knows it absorbed; a shell that blocks raycasts.

## 13. Dash

Read: where from, which way; gone in under half a second.

| Layer | Build | Window |
|---|---|---|
| Origin puff | `puff_set`, Emit 3–4 pushed opposite to the dash, Life 0.3, Size `POP(2)`, Transparency 0.3 → 1, LE 0, LightInfluence 0.3, Color floor × 0.8 | 0–300 |
| Body trails | 1–2 `Trail`s on torso attachments, Lifetime 0.15–0.2, `WidthScale` 1 → 0, Color hot → body, Transparency 0.3 → 1, LE 0.5, `Clear()` before enabling | Dash (150–250) |
| Speed lines | `spark_streak`, `VelocityParallel`, Squash `STREAK`, Emit 6–8 along the path, Life 0.15, Size `SHRINK(0.5)`, Transparency `HOLD`, Color core, LE 1 | 0–200 |
| Camera | FOV +9° in 60 ms, out over 250 ms `[lihfolk]`; half under reduced motion | 0–310 |
| Arrival | 2 small dust puffs, pose squash | End |

- Colour: the character's ability row (Steel default: trail `#E6F6FF → #6FB7FF`, lines `#FFFFFF`).
- Budget: about 12 alive. Cheap: one trail plus the origin puff. Showpiece: an element-coloured afterimage card at the origin for 120 ms, a ground streak decal fading in 400 ms.
- Mistakes: trail not cleared (a line from the last position); two scripts writing `FieldOfView`; trail longer than the dash; trails parented in the character, so they vanish in first person.

## 14. Teleport (out and in)

Read: left from here; arriving there. In PvP the arrival point is shown before the player is.

| Layer | Build | Window |
|---|---|---|
| Out: anticipation | Recipe 6 specks at Rate 8, Highlight FillColor `#FFFFFF`, FillTransparency 1 → 0.3 | −200 to 0 |
| Out: vanish | Pillar mesh with `glow_gradient` tinted hot, width 1 → 0 in 80 ms (`Quad`, `In`); `ring_thin` card on the ground, Size `POP(3)`, `FADE`; 6 `soft_dot` motes rising (Spd 4, Life 0.4, `INOUT`, Color spark) | 0–400 |
| In: arrival tell | `ring_thin` card on the ground at the destination, Size 3, Transparency 1 → 0.3, Color allegiance in PvP, else body | −150 to 0 |
| In: appear | Pillar flash 60 ms, outward ring, 6 motes, landing dust | 0–300 |

- Colour (Arcane row): pillar `#E7C6FF`, rings `#A05BF0`, motes `#F3E1FF`, dark `#2A0F52` under the pillar's base.
- Keep a handle and cancel the visuals if the server rejects the move (`vfx-and-juice.md` §10).
- Budget: about 12 alive and 2 meshes per end. Cheap: ring plus flash at each end. Showpiece: the character dissolving into motes that stream toward the destination along a beam.
- Mistakes: no arrival tell in PvP; identical timing at both ends (arrival should be snappier); camera snapping without a cut or ease; effect implying success before the server agrees.

## 15. Level-up

Read: a milestone, without taking control away.

| Layer | Build | Window |
|---|---|---|
| Hit frame | `star4` at the chest, Emit 1, Life 0.08, Size `SHRINK(3)`, Color `#FFFDF2`, LE 1, Br 5 | 0–80 |
| Ground ring | `ring_drawn` on a flat ring mesh tinted `#F2B632`, 0 → 8 studs in 250 ms, Transparency 0 → 1 from 250 to 400 ms | 0–400 |
| Pillar | Pillar mesh with `glow_gradient` tinted `#FFE58A`, Transparency 0.6 → 1; at least 0.75 transparent on the camera line | 50–550 |
| Rising motes | `soft_dot`, 12–16 over 0.6 s, Life 0.8, Spd 4–6, Size `SHRINK(0.3)`, Transparency `INOUT`, Color `#FFF3B0`, LE 1, Br 2 | 100–1,200 |
| UI and sound | Banner pop, counter count-up, stinger; FOV +4° kick | 0–800 |

- Others see ring and pillar at half detail. Total at most 1.2 s.
- Budget: about 16 alive, 2 meshes. Cheap: ring, star, sound, UI pop. Showpiece (milestone levels only): a second ring, element motes falling for 1.5 s, a brief world dim on the high tier.
- Mistakes: blocking the view mid-combat; every level identical; a full-screen flash.

## 16. Coin or reward burst

Read: got it, and it went there. The reward sequence is in `game-craft.md` §1; its UI timings are in `ui-motion-and-feedback.md` §5.

| Layer | Build | Window |
|---|---|---|
| Pickup pop | Coin mesh squash 15–30% then hide; `star4`, Emit 1, Life 0.06, Size `SHRINK(1.5)`, Color `#FFFDF2`, LE 1 | 0–80 |
| Sparks | `hard_dot`, Color `#FFE58A`, Emit 0–4 (small tier), Spd 10–15, Acc (0, −30, 0), Life 0.3–0.4, Size `SHRINK(0.3)`, LE 0.5 | 0–400 |
| Fly to counter | A few UI icons on a curved path, never one per coin; count and timing in `ui-motion-and-feedback.md` §5 | 50–550 |
| Counter | Pop and count-up (`ui-motion-and-feedback.md` §5); pitch rises on chains | 350–700 |
| Big reward fountain | Coin sprite (4×4 spin flipbook, Loop), Emit 8–12, Spd 18–25, SpreadAngle 30,30, Acc (0, −50, 0), Life 0.6–0.8, Size 0.6 (constant), Transparency `HOLD`, Color `#FFFFFF` (the sprite carries its own gold), LE 0, LightInfluence 0 | 0–800 |

- Budget: 0–4 particles for a normal pickup (the small tier in `game-craft.md`), up to 12 for a fountain. Cheap: pop plus sound. Showpiece: rarity-coloured ring and a short ray card behind the icon in the counter.
- Mistakes: one flying icon per coin; popups stacking; coins tweened on the server; showing a valuable reward before the server confirms it.

## 17. Hatch or open reveal (egg, chest, crate)

Read: something is coming, how good it is, and here it is. House rules: the server decides the result before any animation; every tell derives from the real result; the reveal shows only reachable items; no fake near-miss; skippable after the first view.

| Layer | Build | Window (rare tier) |
|---|---|---|
| Wobble | Three accelerating wobbles of the container (300, 220, 150 ms), ±6° about its up axis, `Sine`, `InOut` | 0–670 |
| Tell | Cracks or seams glowing in the rarity colour (`ui-design-figma.md` rarity ramp, e.g. Rare `#4A98E8`) through an emissive mask or thin beams; inward specks from recipe 6 in the same colour | 300–670 |
| Burst | Hit frame 50 ms (`star4`, `#FFFFFF`), Blender shell shards outward, `ring_drawn` card tinted the rarity colour, Size `POP(6)`, `FADE` | 670–900 |
| Reveal (primary) | Item scale 0 → 1.1 → 1 in 200 ms (`Back`, `Out`); two `glow_gradient` ray cards tinted the rarity colour at Transparency 0.5, rotating ±30°/s in opposite directions behind it; motes in `#FFFFFF` | 700–1,400 |
| Banner | Name and rarity, sound stinger | 900–1,500 |

- Time by tier `[lihfolk]` (full ladder in `ui-motion-and-feedback.md` §5): common 0.3–0.5 s (flash and pop only), rare 1–1.5 s (adds ring and rays), top tiers 5–6 s (add a ground piece, pillar, camera push, world dim). Each tier adds a layer; it does not just get louder. Auto-open modes get a compact reveal.
- Budget: about 20 alive, 2–3 meshes, in front of a calm background. Cheap: flash, pop, banner. Showpiece: top tier only.
- Mistakes: long animation for commons; rays on everything; unskippable; result rolled on the client; strobing.

## 18. Footstep and landing dust

Read: weight and surface. Own character and near neighbours only.

| Layer | Build | Window |
|---|---|---|
| Footstep puff | `puff_set`, Emit 1–2 at the foot marker, Life 0.3–0.45, Size `POP(1.2–1.6)`, Spd 1–2, `VelocityInheritance` 0.2, LE 0, LightInfluence 0.3, Transparency 0.5 → 1, Color from a `Humanoid.FloorMaterial` table: the floor colour × 0.8 (sand `#A8946E`, grass `#55703C`, concrete `#707070`; snow `#AAB6C4`, darker than the snow so it reads) | 0–450 |
| Landing ring | `puff_set`, Disc outward, Emit 6–10 scaled by fall speed, Spd 8–12, Drag 5, Life 0.4–0.6, Size `POP(2)`, Transparency 0.4 → 1, same colour table, LE 0, LightInfluence 0.3 | 0–600 |
| Heavy landing | Add a `ring_drawn` card (Size `POP(5)`, `FADE`, same colour) and medium-tier shake as ground movement: `HitFeel.addTrauma(0.5, true)` | 0–300 |

- Budget: 2–4 alive while running; only when running, within about 40 studs, every other step on the low tier. Cheap: landing ring only. Showpiece: surface-specific shapes (splash on water, sparks on metal, leaves on grass).
- Mistakes: the same dust on water and metal; dust at walking speed; emitted from the server; opaque puffs; puffs glowing in the dark (set LightInfluence above 0 for matter, and check caves).

## 19. Fire (torch, campfire, burning state)

Read: hot at the base, rising, then smoke. Break the reference into components first `[official]`.

| Layer | Build | Window |
|---|---|---|
| Flame body (primary) | Flame-shaped sprites or a 4×4 loop, Rate 8–12, Life 0.5–0.8, Spd 2–4, Acc (0, 4, 0), Size 1.5 → 0.3, Transparency `INOUT`, Color (0, `#FFF6DD`) (0.2, `#FFC83D`) (0.5, `#FF6A1A`) (1, `#6B1220`), LE 0.8, Br 3, Rotation −15 to 15 only | Loop |
| Core glow | `soft_dot`, `LockedToPart`, 1 alive (Rate 2, Life 0.5), Size 2, Transparency `INOUT`, Color `#FFC83D`, LE 1, Br 2 | Loop |
| Embers | `spark_streak`, `VelocityParallel` with Squash, Rate 2–4, Life 0.8–1.5, Spd 5–8, Acc (0, 10, 0), Drag 0.8, Size `SHRINK(0.2)`, Squash `STREAK`, Transparency `FLICKER`, Color `#FFD98A → #FF6A1A`, LE 1 (Spd, Acc and Drag `[official]`; the tutorial's Life 1–5 and Br 20 suit a volcano, start at Br 6–10) | Loop |
| Smoke | `puff_set`, Rate 1–2, Life 2–3, Acc (0, 2, 0), LE 0–0.1, LightInfluence 0.1–0.3, Size `POP(4)`, Color `#3A2420 → #6A5F5A`, Transparency `INOUT` (fading in while the flame fades out), ZOffset −1 | Loop |
| Light | `PointLight`, Color `#FFB060`, Brightness 1.5–2.5 flickering at 8–12 Hz, Range 12–16, shadows off | Loop |

- Budget: at most 25 alive per fire; sleep by distance; counts against the ambient budget in `performance.md`. Cheap: flame at Rate 6 plus the light. Showpiece: three nested Blender flame shells with a scrolling `Texture`, sparks reacting to wind (`WindAffectsDrag`).
- Mistakes: Rotation 0–360 on flames (fire has an up); additive smoke; a hard cut from fire to smoke; too many embers; a shadow-casting light.

## 20. Lightning strike

Read: warning line, bolt, burst, residue: five beats in under 1.5 s `[community]` (greyscale storyboard in the library).

| Layer | Build | Window |
|---|---|---|
| Warning line | Vertical `Beam`, `FaceCamera`, Width 0.8, Color `#8FD0FF`, Transparency 0.7 → 0.3 (scripted over the 300 ms), LE 1 | −300 to 0 |
| Bolt (primary) | Crossed-ribbon mesh in 3 jagged variants shown 2 frames each, or 2–3 beams with fresh random curves per step; Width 1.2 → 0; core `#FFFFFF`, edge `#8FD0FF`, a `#1B1F5C` copy 1.5× wide behind it for value | 0–100 |
| Flash | `star4` at the ground (Size `SHRINK(6)`, `#FFFFFF`, LE 1), `PointLight` Color `#BFE6FF`, Brightness 6, Range 30, 60 ms; no full-screen flash by default | 0–60 |
| Ground burst | `ring_drawn` card (Size `POP(5)`, `FADE`, `#FFF29A`), forking `spark_streak` sparks (`VelocityParallel`, `STREAK`, Emit 8, Spd 30, Drag 10, Life 0.2, `HOLD`, `#FFF9D1`, LE 1) | 16–300 |
| Residue | Dark spiky `puff_set` (`#3A3F6B`, LE 0, 0.4 → 1), `crack_decal` (`#1B1F5C`), 2–3 small embers (`#8FD0FF`, `FLICKER`) | 100–1,000 |

- Budget: about 14 alive, 1–3 meshes, 1 light. Cheap: one bolt mesh for 100 ms, flash, sound. Showpiece: branch bolts, a second weaker re-strike at +120 ms, the telegraph from recipe 7.
- Mistakes: a smooth wavy bolt; bolt visible beyond 150 ms; strobing more than 3 flashes a second; blue only, with no white core or dark; lines under 0.8 studs wide that vanish at phone size.

## 21. Water splash

Read: liquid is matter: it has weight, an outline and a ring on the surface. Never additive.

| Layer | Build | Window |
|---|---|---|
| Crown | `splash_set`, `FacingCameraWorldUp`, Emit 2–3, Life 0.3–0.4, Size `POP(3–4)`, Squash 0.8 → 0.2 (positive is taller `[official]`), Transparency `FADE`, Color `#B8F0FF`, LE 0.4 | 0–400 |
| Droplets | `hard_dot`, Emit 8–12, Life 0.25–0.35, Spd 20–35, SpreadAngle 50,50, Acc (0, −40, 0), Size `SHRINK(0.25)`, Color `#DDF7FF`, LE 0.5, LightInfluence 0.1 `[official]` | 0–350 |
| Surface foam ring | `ring_drawn` or foam sprite, `VelocityPerpendicular`, Spd 0.01, Life 0.5–0.7, RotSpeed ±15, LE 0.25 `[official]`, Size 2 → 5, Transparency 0.3 → 1, Color `#FFFFFF` | 30–700 |
| Mist (large splashes) | `soft_dot`, Life 0.5–1, Spd 35–50 upward, Drag 1.5 `[official]`, Size `POP(4)`, Transparency 0.8 → 1, Color `#DDF7FF`, LE 0 | 0–1,000 |

- Colour and value (Water row): blue body `#2F9BE0` turning `#FFFFFF` at the top; darker `#0C2A5A` inner shapes painted into `splash_set` so it reads against sky.
- Budget: about 16 alive. Cheap: droplets plus foam ring. Showpiece: a 4×4 OneShot splash flipbook, a secondary ring at +150 ms.
- Mistakes: glowing water; droplets without gravity; no ring on the surface; the same splash for a pebble and a boss.

## 22. Environmental ambience

Read: the place is alive, quietly. Ambience is never brighter or sharper than gameplay effects. Budget: 6–10 ambient emitters in view at Rate ≤ 20 (`performance.md`).

| Element | Build |
|---|---|
| Dust motes in light | `soft_dot`, Rate 3–5, Life 6–10, Spd 0.3–0.6, Size 0.08–0.15, LE 0.5, `INOUT`, Color the light's colour (warm sun `#FFF6DD`) |
| Fireflies | `soft_dot`, Rate 1–2, Life 4–6, Size 0.2, Color `#E3FF9C`, LE 1, Br 4, Transparency (0, 1) (0.1, 0) (0.2, 1) (0.45, 1) (0.55, 0) (0.65, 1) (1, 1) |
| Leaves or petals | Leaf shape tinted from the foliage, Rate 2–4, Life 6–8, Spd 2–3 downward, `INOUT`, LightInfluence 1, RotSpeed ±60, Drag 0.5 with `WindAffectsDrag` so `GlobalWind` carries them `[official]` |
| Rain | One emitter box that follows the camera, `spark_streak`, `VelocityParallel`, Squash −3 `[official]`, Rate up to the mobile cap of 100, Life 0.6–0.8, Spd 60–80, Color `#9FB4C8`, LightInfluence 0.6 (the docs: darken the colour, raise LightInfluence); a second emitter for ground splashes at Rate 10 |
| Ground mist | Large `soft_dot` cards, at most 4 alive, Transparency 0.85 or more (large transparent sprites are the overdraw cost), Color `#DDE6EE`, LightInfluence 0.5 |
| Waterfall or lava | Stacked `Beam`s. Waterfall: Width0 60 → Width1 20, `TextureSpeed` 0.4, `TextureLength` 64, Wrap. Lava: base beam plus two crust beams at `TextureSpeed` 0.01 and −0.008 `[official]` |

- Rules: emitters live in zones or follow the camera, never the whole map; sleep when the zone is out of view; long lifetimes multiply the alive count (`Rate × Lifetime`).
- Mistakes: map-wide emitters; ambience brighter than combat effects; rates above the mobile cap; rain that falls indoors.

## Review gate

- [ ] The effect was blocked in white first and matches its "Read" line in a half-second glance at phone size.
- [ ] Every layer in the table has a role, a window in milliseconds and an end; the bright phase is a quarter of the total or less.
- [ ] The primary layer is drawn at the exact hit volume and carries allegiance where teams exist.
- [ ] Untested `[house]` values were tuned against a frame-by-frame capture; nothing is shipped at recipe defaults unseen.
- [ ] Colours come from one palette row and keep its value bands in a greyscale screenshot; every sequence is written out, none left at the default constant.
- [ ] Textures come from the shared kit (or a justified addition); any tonight stand-in still in use is on a replace list, `star4` and `slash_streak` first; meshes are Blender kit pieces, pooled and non-colliding.
- [ ] The cheap version is the low tier; the showpiece version is reserved for importance 8–10.
- [ ] Scored with the rubric in `vfx-and-juice.md` §16.

## Sources

Accessed 2026-11-11; every `[official]` value re-checked against the tutorials the same day. Detail and links for each are in `vfx-and-juice.md` Sources and the two `visual-library/vfx*.md` files.

- Roblox/creator-docs at commit 7cbffff (read): `tutorials/use-case-tutorials/vfx/use-particles-for-explosions.md` (spark burst values, spark texture id), `create-volcanoes.md` (embers, ripples, lava splash, lava flow beams, smoke plume, texture ids), `create-waterfalls.md` (cascade beams, splashes, white water, foam, mist), `custom-particle-effects.md` (soft circle id); `effects/particle-emitters.md` (shapes, drag, flipbooks, wind, default sparkle, squash sign for rain); `projects/assets/privacy.md` (images are Open Use by default).
- Engine particle textures: file list and files from Roblox-Client-Tracker (community mirror of the client, commit d39c04f, 2026-11-10), five viewed; not documented by Roblox.
- LihFolk Vault V2 (CC BY 4.0) (read): timing table, telegraph formula, hit-stop tiers, dash FOV, reveal time by tier.
- realtimevfx.com and 80.lv (read, images viewed): Riot missile anatomy and heal conventions (McDonald), three-stage timing and element table (Jevremović), projectile hot point and shadow (Leroy), lightning storyboard (jqarlsson), slash, explosion, shockwave and heal references listed in `visual-library/vfx.md`.
- DevForum (read): first-person hiding of avatar effects (staff), inward emission, crescent slash mesh, fire-to-smoke critique.
- No source gives full Roblox property sets for most of these effects: the layer structures follow the references, and the unsourced numbers are house estimates awaiting an in-engine pass.
