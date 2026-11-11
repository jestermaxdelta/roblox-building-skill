# VFX recipes: 21 effects, layer by layer

What this is: build sheets for the effects almost every Roblox game needs. Each recipe lists its layers in order with starting property values, timing in milliseconds, colour and value notes, the textures it uses, a phone budget, a cheap version, a showpiece version and the usual mistakes. Open it when you are about to build a specific effect. The reasons behind the numbers (principles, instance traps, timing table, hit-stop, replication, pooling, budgets, comfort) are in `vfx-and-juice.md` and are not repeated; reference images for most recipes are in `visual-library/vfx.md`.

**Status of the numbers.** Values tagged `[official]` come from Roblox's own tutorials; `[lihfolk]` and `[community]` come from the sources named in `vfx-and-juice.md`. Everything else is a `[house]` starting point, **untested in engine**: build it, capture it on a phone, compare with a reference frame by frame, then tune. No Luau here; the play path is `FxPool.play` and animation markers from `vfx-and-juice.md` §6, §10 and §11.

## Contents

Start here by level · Conventions and shared kit · 1. Hit spark · 2. Melee slash · 3. Heavy impact · 4. Projectile · 5. Charge-up · 6. AoE telegraph and detonation · 7. Explosion · 8. Shockwave · 9. Aura or buff · 10. Heal · 11. Shield · 12. Dash · 13. Teleport · 14. Level-up · 15. Coin or reward burst · 16. Hatch or open reveal · 17. Footstep and landing dust · 18. Fire · 19. Lightning · 20. Water splash · 21. Environmental ambience · Review gate · Sources

## Start here by level

| Level | Do | Skip for now |
|---|---|---|
| Beginner | Build the **cheap version** of recipes 1, 15 and 17 with the first four kit textures. Block each in white, then colour | Meshes, flipbooks, showpiece versions |
| Intermediate | Build the full layer tables for your core verb (usually 2, 3, 4 or 6). Model the five kit meshes in Blender once and reuse them everywhere | Showpiece versions except for the rarest moments |
| Expert | Add showpiece versions for the top one or two tiers only; write the importance sheet first (`vfx-and-juice.md` §1); score with the §16 rubric on a phone | — |

New game: build recipes in the order your loop needs them, cheap versions first, and upgrade only what the importance sheet rates 7 or more. Live game: capture your current effect, score it with the rubric, then change the lowest-scoring line using the matching recipe row.

## Conventions and shared kit

- Shorthand: `Life` = `Lifetime` in seconds; `Spd` = `Speed` in studs/s; `Acc` = `Acceleration`; `LE` = `LightEmission`; `Br` = `Brightness`; `Emit n` = burst with `Enabled = false`; `Rate n` = stream. Every emitter sets `LightInfluence` explicitly (0 unless a row says otherwise). Sizes assume a 5-stud character and a third-person camera 15–25 studs away. Windows are milliseconds from the trigger (animation marker or contact = 0); negative means before it.
- Curves: `POP(S)` = Size keys (0, 0.2·S) (0.15, 0.8·S) (1, S): fast in, eased out. `SHRINK(S)` = (0, S) (1, 0). `FADE` = Transparency (0, 0) (0.6, 0.3) (1, 1). `INOUT` = Transparency (0, 1) (0.15, 0) (0.7, 0.4) (1, 1).
- Colour roles per element come from the ramp table in `vfx-and-juice.md` §1: **dark**, **body**, **hot**, plus white for the thin core. "Allegiance" means the team hue on the primary layer.
- Budget line: particles alive at peak for your own cast at full detail (the low tier multiplies bursts by 0.4), pooled meshes, lights. Others' casts run at half and lose decoration layers.

| Kit texture (greyscale, painted for the game) | Size | Used by |
|---|---|---|
| `soft_dot` radial glow | 128² | Cores, glows, motes |
| `hard_dot` hard-edged disc | 128² | Flat sparks, coins, bubbles |
| `spark_streak` soft elongated oval | 128² | Sparks, embers, rain, speed lines (with `VelocityParallel`) |
| `star4` four-point flash | 256² | Hit frames, muzzle flashes, glints |
| `ring_drawn` irregular hand-drawn shock ring | 512² | Impacts, explosions, level-up |
| `ring_thin` clean thin ring | 512² | Telegraph rims, auras, shields |
| `slash_streak` hand-painted streak, tips fading | 512×256 | Crescents, trails, beams |
| `puff_set` four flat smoke puffs with an inner shadow shape (2×2) | 512² | Dust, smoke, fire body |
| `splash_set` four splash shapes (2×2) | 512² | Water, liquid hits |
| `crack_decal` radial ground cracks | 512² | Impact and explosion residue |
| `noise_tile` tiling streaky noise | 256² | Shields, beams, scrolling layers |
| `glow_gradient` soft vertical gradient strip | 256² | Pillars, rays, light shafts |

Kit meshes (Blender, `vfx-and-juice.md` §5): crescent band, flat ring, disc with sector variants, dome shell, pillar, crossed ribbons, shard set. Twelve textures and seven meshes build every recipe below.

## 1. Hit spark (light hit, several per second)

Read: "that connected, in that direction". No hit-stop, no shake at this tier.

| Layer | Build | Window |
|---|---|---|
| Flash card (primary) | `star4`, Emit 1, Life 0.05–0.07, Size `SHRINK(2.5–3)` (about 0.6× the target's width), LE 1, Br 4, ZOffset +1, random Rotation | 16–70 |
| Directional sparks | `spark_streak`, `VelocityParallel`, Emit 6–10, Life 0.15–0.3, Spd 25–40, Drag 8–10 (official spark burst uses Spd 20–40, Drag 10, Life 0.2–0.6 `[official]`), SpreadAngle 25,25 around the swing direction, Size `SHRINK(0.4)`, LE 1, Br 6 | 0–300 |
| Dark puff | `puff_set` (random frame, framerate 0), Emit 1–2, Life 0.25–0.35, Size `POP(2)`, LE 0, dark colour, Transparency 0.4 → 1, ZOffset −0.5 | 0–350 |
| Target response | Persistent Highlight fill pulse 80–120 ms, sound with pitch variation | 0–120 |

- Colour and value: white flash, hot sparks, saturated dark puff. Kid-friendly: no red spray.
- Budget: about 12 alive, no meshes, no light. Cheap: flash plus 4 sparks. Showpiece (crit): add `ring_drawn` on a flat card growing 0 → 4 studs in 120 ms and a number popup.
- Mistakes: radial sparks; flash larger than the target; anything living past 400 ms on an effect that fires three times a second; hit-stop on light hits.

## 2. Melee slash

Read: the arc is the hit area; the leading edge is where it is now.

| Layer | Build | Window |
|---|---|---|
| Anticipation glint | `star4` on the blade tip, Emit 1, Life 0.06–0.08, Size `SHRINK(1)`, LE 1 | −120 to −40 |
| Crescent body (primary) | Crescent band mesh with `slash_streak`, appears at the `TrailOn` marker, scale 0.85 → 1.05 in 120 ms (ease out), Transparency 0 → 1 between 120 and 220 ms, texture slid toward the tip. Angle and radius equal the hit test | 0–220 |
| Hot edge | Smaller additive copy at the leading edge, hot colour, 80–100 ms | 0–100 |
| Dark trailing edge | Same mesh, dark colour, not additive, delayed 30 ms, gone by 260 ms | 30–260 |
| Blade trail (arcs under 120°) | `Trail` between two blade attachments, Lifetime 0.12–0.18, `WidthScale` 1 → 0, `Clear()` then enable for the cut window only | 0–180 |
| Sparks | `spark_streak`, Emit 4–8 along the swing tangent, Life 0.2–0.35, Spd 15–25 | 0–350 |

- Colour and value: hot leading edge, body in the element colour, dark trailing shape that outlives the light; flat colours read better than gradients at phone size.
- Budget: 2–3 pooled meshes, under 10 particles. Cheap: trail plus flash. Showpiece: one thin straight speed line across the arc for 2 frames, a dust line on the ground under the arc, embers lingering 400–600 ms.
- Mistakes: trail wrapping the character; ribbon of uniform width and brightness; crescent pivot left at the bounding-box centre; arc drawn wider than the hitbox; body visible beyond 250 ms; additive only.

## 3. Heavy impact (ground slam)

Read: big, here, now; the ring edge is the damage radius.

| Layer | Build | Window |
|---|---|---|
| Anticipation | Weapon glow or recipe 5 at low strength | −300 to 0 |
| Hit frame | `star4` or `soft_dot`, Emit 1, Life 0.05, Size 4–5, LE 1, Br 5; optional `PointLight` Brightness 3, Range 12, shadows off, 100 ms | 16–66 |
| Hit-stop, then shake | Heavy tier: 66 ms stop, trauma 0.25, kick 0.5% `[lihfolk]`; shake starts when the stop releases | 0–66, then 66–400 |
| Ring (primary) | Flat ring mesh with `ring_drawn`, scale 0.2 → 1 (the damage radius) in 150 ms ease out, Transparency 0 → 1 from 120 to 320 ms | 0–320 |
| Dust ring | `puff_set`, Shape Disc with `ShapePartial` 0.9, outward, Emit 10–14, Life 0.4–0.7, Spd 12–18, Drag 3, Size `POP(4–6)`, LE 0, LightInfluence 0.3, floor-tinted, Transparency 0.3 → 1 | 30–700 |
| Debris | `hard_dot` or shard sprites, Emit 6–10, Spd 20–30, SpreadAngle 60,60 upward, Acc (0, −60, 0), Life 0.5–0.8 | 0–800 |
| Residue | Disc mesh with `crack_decal`, dark colour, Transparency 0.2 → 1 over 1.2–2 s | 50–2,000 |

- Budget: about 30 alive, 2 meshes, 0–1 light. Cheap: hit frame, one flat ring card (`VelocityPerpendicular`, Spd 0.01) and 6 dust puffs. Showpiece: Blender rock chunks rising in a ring then sinking, a second ring at +80 ms and 70% size, glowing cracks that cool to dark.
- Mistakes: perfectly even ring; debris in a full sphere instead of a hemisphere; residue brighter than the hit; shake during the stop; ring drawn larger than the server radius.

## 4. Projectile (cast, travel, hit)

Read: where it is, where it came from, how wide it is. The hot point is the hit volume.

| Layer | Build | Window |
|---|---|---|
| Cast | `star4` 1–2 studs ahead of the hand, Emit 1, Life 0.05; two `ring_thin` cards (`VelocityPerpendicular`) moving along the shot direction, Spd 8, Life 0.15, Size `POP(1.5)` | 0–150 |
| Hot point (primary) | `hard_dot` or a small core mesh, diameter = server hit diameter, hot colour with a white centre; `LockedToPart`, Rate 20, Life 0.1 | Travel |
| Glow and shadow | `soft_dot` in the body colour (LE 1) over a larger dark `soft_dot` (LE 0, ZOffset −0.5): the dark buys the glow | Travel |
| Trail | `Trail`, Lifetime = (12 to 30 studs) ÷ speed, `WidthScale` 1 → 0, colour body → dark | Travel |
| Shed motes (secondary) | `soft_dot`, Rate 12–15, Life 0.3–0.5, Spd 0–1, Size `SHRINK(0.3)`: they outlast the trail | Travel +500 |
| Hit | Recipe 1 scaled up: hit frame about 100 ms, sparks continuing the direction of travel, ring perpendicular to it, motes last | 0–600 |

- Budget: at most 15 alive per projectile in flight; cap live projectiles through the pool. Cheap: core, trail, flash. Showpiece: a unique silhouette (teardrop core mesh, a motif in the trail), a spiralling second trail.
- Mistakes: hot point offset from the server position; trail too long (laser) or too short (dot); muzzle flash on the hand hiding the character; visuals moved by the server; identical ally and enemy projectiles in PvP.

## 5. Charge-up

Read: power is gathering; a clear "ready" beat.

| Layer | Build | Window |
|---|---|---|
| Inward specks | Host part 8–10 studs wide, Shape Sphere, `ShapeStyle` Surface, `ShapeInOut` Inward, `spark_streak`, `VelocityParallel`, Rate 15–20, Life 0.35–0.5, Spd = radius ÷ Life (about 12 for a 5-stud radius) so they die at the centre, Size `SHRINK(0.3)` | Hold |
| Core | `soft_dot`, `LockedToPart`, 1 alive (Rate 4, Life 0.25), Size driven 0.5 → 2 by charge, hot colour over a dark `soft_dot` | Hold |
| Imploding ring | `ring_thin` card, Size 6 → 0 in 300 ms, once per charge tier | Tier steps |
| Ready glint | `star4`, Emit 1, Life 0.08, plus colour shift body → hot and a 0.25% kick | Full charge |

- Timing: if the charge also hides a server round trip, the loop holds at least 300–600 ms `[lihfolk]`. Replicate as a character attribute so others see it at reduced detail.
- Budget: about 10 alive. Cheap: core plus specks at Rate 8. Showpiece: three audible and visible tiers, FOV −3° eased in, small arcs between the hands.
- Mistakes: outward particles (reads as a leak); charge longer than the move deserves; glow covering the character; no release payoff.

## 6. AoE telegraph and detonation

Read: exactly where, and exactly when. Never culled, never simplified below outline, fill and pop.

| Layer | Build | Window |
|---|---|---|
| Dark outline | Two semicircle `Beam`s (handle 1.333 × r), Width 0.3, LE 0, dark colour, Segments 40 | 0 → T |
| Base fill | Disc mesh, allegiance colour, Transparency 0.75–0.8 | 0 → T |
| Progress fill (primary) | Second disc scaling 0 → 1 with an ease-in curve, Transparency 0.55, a hot `ring_thin` on its leading edge | 0 → T |
| Bright rim | Ring beams, Width 0.15, LE 1, at the exact server radius | 0 → T |
| Pop | Fill flashes white on the damage frame and fades in about 220 ms `[lihfolk]` | T → T+220 |
| Detonation | Recipe 7 or 8 scaled to r | T → |

- T = 250 ms reaction + escape distance ÷ 16 studs/s (+100–200 ms for touch): r = 10 gives 0.9 s minimum, 1.1–1.4 s comfortable `[lihfolk]`. One shape table feeds both this drawing and the server hit test.
- Colour and value: outline for bright floors, rim for dark floors, both always. Enemy zones in the enemy hue with a hard or dashed rim; friendly zones (recipe 10) smooth.
- Budget: 4 beams and 2 meshes; cap concurrent telegraphs per client by simplifying to outline, fill and pop, never by skipping. Cheap: outline ring, fill disc, pop. Showpiece: a motif inside the disc (cracks, runes), motes rising at the rim, a sky warning line as in recipe 19.
- Mistakes: linear fill (the last 200 ms cannot be judged); drawn radius differs from the server's; additive fill on a bright floor; fill so opaque it hides other hazards; hidden on low settings.

## 7. Explosion (stylised)

Read: one bright beat, then smoke. The fireball is a quarter of the timeline.

| Layer | Build | Window |
|---|---|---|
| Hit frame | `soft_dot`, Emit 1, Life 0.05, Size 0.6 × body, white, LE 1, Br 6; `PointLight` 100 ms | 16–66 |
| Fire body (primary) | `puff_set`, Emit 5–8, Life 0.3–0.45, Size `POP(5–7)`, Spd 6–10, Drag 4, Color hot → body → dark, LE 0.6, ZOffset +0.5 | 0–450 |
| Streak lines | `spark_streak`, `VelocityParallel`, Emit 10–14 at uneven angles, Spd 40–60, Drag 10, Life 0.15–0.25, LE 1 | 0–250 |
| Ring | Flat ring mesh with `ring_drawn`, 0.2 → 1.3 × body radius in 180 ms, gone by 300 ms | 0–300 |
| Smoke | `puff_set`, Emit 4–6, Life 0.8–1.2, Size `POP(6–8)`, Acc (0, 3, 0), LE 0, warm dark colour, Transparency 0.2 → 1, ZOffset −1 | 80–1,200 |
| Embers | `spark_streak`, Emit 8–12, Life 0.6–1.2, Spd 8–14, Acc (0, −15, 0), Drag 0.8, flickering Transparency, LE 1 (official ember set-up: `VelocityParallel` with Squash, Drag 0.8 `[official]`) | 0–1,200 |

- Hit-stop and shake by tier from the hit's strength value (`vfx-and-juice.md` §7).
- Budget: about 45 alive, 1 mesh, 1 light. Cheap: hit frame, 4 puffs, 6 streaks. Showpiece: a 4×4 OneShot flipbook as the body (Life 0.4), second delayed ring, Blender debris, `crack_decal` scorch for 2 s.
- Mistakes: everything additive; smoke the same colour as the fire; evenly spaced radial streaks; total over 1.4 s; a unique 1024² flipbook per explosion type.

## 8. Shockwave

Read: a force front passing a radius.

| Layer | Build | Window |
|---|---|---|
| Ring (primary) | Flat ring mesh with `ring_drawn`, scale 0.2 → 1 over 200–300 ms ease out, band thinning as it grows, Transparency 0 → 1 over the last 60% | 0–300 |
| Leading edge | `ring_thin`, additive, 3% ahead of the ring, same curve, gone by 200 ms | 0–200 |
| Ground dust | `puff_set`, Disc with `ShapePartial` 0.95, Emit 8–12, Spd 20, Drag 6, Life 0.3, Size `POP(2.5)`, LE 0 | 20–350 |
| Dome (3D blast only) | Dome shell mesh, scale 0.3 → 1 in 200 ms, Transparency 0.6 → 1 | 0–250 |

- Budget: 1–2 meshes, about 12 alive. Cheap: one flat card particle (`VelocityPerpendicular`, Spd 0.01, Life 0.25, Size 0 → 2r). Showpiece: a second ring at +80 ms and 70% size, short radial streak cards. Screen-space distortion is not available on Roblox; do not fake it with stacked transparent layers.
- Mistakes: constant band thickness; linear growth; opaque band over players; visual radius beyond the real one.

## 9. Aura or buff (state)

Read: this character has a status, and which kind. Driven by a character attribute, so late joiners see it.

| Layer | Build | Window |
|---|---|---|
| Start burst | `ring_thin` card 0 → 5 studs in 200 ms plus 6 motes | 0–300 |
| Ground ring (primary) | `ring_thin` on a flat ring mesh or two beams under the feet, slow rotation or `TextureSpeed` 0.1, Transparency 0.6 | Loop |
| Motes | `soft_dot` or the element's secondary shape, host Cylinder Surface sized to the character, Rate 6–10, Life 0.8–1.2, Spd 2–3 upward, Size `SHRINK(0.25)`, LE 0.6, Br 2 | Loop |
| End puff | 4 motes outward, ring fades in 200 ms | End |

- Buff versus debuff must differ by more than hue: buffs rise, are smooth and light; debuffs fall or drip, are jagged and dark.
- Budget: at most 12 alive per aura; others' auras at half rate; sleep beyond 160 studs. Parent to a welded helper part or it disappears in first person `[official]`. Cheap: ground ring plus 4 motes a second. Showpiece: orbiting element shapes on a ring beam, a pulse synced to the remaining duration.
- Mistakes: covering the character's silhouette; constant bright additive glow; sent as a one-time event; never ends; every buff identical.

## 10. Heal

Read: friendly and soft. No sharp shapes, no flame; green by convention `[community]` (Riot).

| Layer | Build | Window |
|---|---|---|
| Ground ring | `ring_thin`, 0 → r in 250 ms ease out, hold, fade 400 ms, body green | 0–900 |
| Light column | Pillar mesh or vertical beam with `glow_gradient`, Transparency 0.7 → 1 | 100–700 |
| Rising motes or petals (secondary) | `soft_dot` or a leaf shape, Emit 8–12 (or Rate 12 for 0.5 s), Life 0.8–1.2, Spd 3–5, Acc (0, 2, 0), Size 0.3–0.5, RotSpeed ±40, pale green to yellow-white | 100–1,300 |
| Target response | Highlight fill pulse green-white 150 ms; "+N" popup in green | 150–400 |

- Timing is slow and low-contrast on purpose: 250 ms in, 600–900 ms total.
- Budget: about 14 alive, 1–2 meshes. Cheap: ring, 6 motes, popup. Showpiece: a growth motif (vines or flowers blooming along the ring), a small rising tick on every ally healed.
- Mistakes: star or spike shapes; red or orange; a pillar bright enough to hide the target; symbols with unwanted meanings (a pentagram reads as hostile).

## 11. Shield (state, hit response, break)

Read: protected; that hit was absorbed; now it is gone.

| Layer | Build | Window |
|---|---|---|
| Appear | Sphere shell mesh a little larger than the character, scale 0.8 → 1.05 → 1 in 180 ms | 0–180 |
| Shell (primary) | `noise_tile` on a `Texture`, lines panning downward (`OffsetStudsV` tween), Transparency 0.75–0.85; non-colliding, `CanQuery = false` | Loop |
| Rim | `ring_thin`, `LockedToPart`, 1 alive (Rate 2, Life 0.5), Size = shell diameter, LE 1 | Loop |
| Hit response | `soft_dot` flash and a `ring_thin` ripple at the hit point, shell Transparency 0.8 → 0.5 → 0.8 in 150 ms | 0–200 |
| Break | Blender shard set bursting outward 300 ms, `star4` hit frame, glass-like sound | 0–400 |

- Budget: 1–2 meshes per shielded character, about 3 alive; fade the shell for its owner in first person (`LocalTransparencyModifier`). Cheap: rim ring plus hit flash. Showpiece: hex pattern texture, a directional ripple travelling from the hit point, shards that catch the allegiance colour.
- Mistakes: an opaque bubble hiding the character; looks like recipe 9; no hit response, so nobody knows it absorbed; a shell that blocks raycasts.

## 12. Dash

Read: where from, which way; gone in under half a second.

| Layer | Build | Window |
|---|---|---|
| Origin puff | `puff_set`, Emit 3–4 pushed opposite to the dash, Life 0.3, Size `POP(2)`, LE 0, floor-tinted | 0–300 |
| Body trails | 1–2 `Trail`s on torso attachments, Lifetime 0.15–0.2, `WidthScale` 1 → 0, Transparency 0.3 → 1, `Clear()` before enabling | Dash (150–250) |
| Speed lines | `spark_streak`, `VelocityParallel`, Emit 6–8 along the path, Life 0.15, LE 1 | 0–200 |
| Camera | FOV +9° in 60 ms, out over 250 ms `[lihfolk]`; half under reduced motion | 0–310 |
| Arrival | 2 small dust puffs, pose squash | End |

- Budget: about 12 alive. Cheap: one trail plus the origin puff. Showpiece: an element-coloured afterimage card at the origin for 120 ms, a ground streak decal fading in 400 ms.
- Mistakes: trail not cleared (a line from the last position); two scripts writing `FieldOfView`; trail longer than the dash; trails parented in the character, so they vanish in first person.

## 13. Teleport (out and in)

Read: left from here; arriving there. In PvP the arrival point is shown before the player is.

| Layer | Build | Window |
|---|---|---|
| Out: anticipation | Recipe 5 specks at low rate, Highlight fill toward white | −200 to 0 |
| Out: vanish | Pillar mesh with `glow_gradient` collapsing in width to 0 in 80 ms, `ring_thin` on the ground 0 → 3 studs, 6 motes rising for 400 ms | 0–400 |
| In: arrival tell | `ring_thin` on the ground at the destination | −150 to 0 |
| In: appear | Pillar flash 60 ms, outward ring, 6 motes, landing dust | 0–300 |

- Keep a handle and cancel the visuals if the server rejects the move (`vfx-and-juice.md` §10).
- Budget: about 12 alive and 2 meshes per end. Cheap: ring plus flash at each end. Showpiece: the character dissolving into motes that stream toward the destination along a beam.
- Mistakes: no arrival tell in PvP; identical timing at both ends (arrival should be snappier); camera snapping without a cut or ease; effect implying success before the server agrees.

## 14. Level-up

Read: a milestone, without taking control away.

| Layer | Build | Window |
|---|---|---|
| Hit frame | `star4` at the chest, Emit 1, Life 0.08 | 0–80 |
| Ground ring | `ring_drawn` on a flat ring mesh, 0 → 8 studs in 250 ms | 0–400 |
| Pillar | Pillar mesh with `glow_gradient`, Transparency 0.6 → 1; at least 0.75 transparent on the camera line | 50–550 |
| Rising motes | `soft_dot`, 12–16 over 0.6 s, Life 0.8, Spd 4–6 | 100–1,200 |
| UI and sound | Banner pop, counter count-up, stinger; FOV +4° kick | 0–800 |

- Others see ring and pillar at half detail. Total at most 1.2 s.
- Budget: about 16 alive, 2 meshes. Cheap: ring, star, sound, UI pop. Showpiece (milestone levels only): a second ring, element motes falling for 1.5 s, a brief world dim on the high tier.
- Mistakes: blocking the view mid-combat; every level identical; a full-screen flash.

## 15. Coin or reward burst

Read: got it, and it went there. The reward sequence itself is in `game-craft.md` §1.

| Layer | Build | Window |
|---|---|---|
| Pickup pop | Coin mesh squash 15–30% then hide; `star4`, Emit 1, Life 0.06 | 0–80 |
| Sparks | `hard_dot` in the coin colour, Emit 0–4 (small tier), Spd 10–15, Acc (0, −30, 0), Life 0.3–0.4 | 0–400 |
| Fly to counter | 1–5 UI icons on a curved path, 300–500 ms, however large the amount | 50–550 |
| Counter | Pop and count-up; pitch rises on chains | 350–700 |
| Big reward fountain | Coin sprite (4×4 spin flipbook), Emit 8–12, Spd 18–25, SpreadAngle 30,30, Acc (0, −50, 0), Life 0.6–0.8 | 0–800 |

- Budget: 0–4 particles for a normal pickup (the small tier in `game-craft.md`), up to 12 for a fountain. Cheap: pop plus sound. Showpiece: rarity-coloured ring and a short ray card behind the icon in the counter.
- Mistakes: one flying icon per coin; popups stacking; coins tweened on the server; showing a valuable reward before the server confirms it.

## 16. Hatch or open reveal (egg, chest, crate)

Read: something is coming, how good it is, and here it is. House rules: the server decides the result before any animation; every tell derives from the real result; the reveal shows only reachable items; no fake near-miss; skippable after the first view.

| Layer | Build | Window (rare tier) |
|---|---|---|
| Wobble | Three accelerating wobbles of the container (300, 220, 150 ms) | 0–670 |
| Tell | Cracks or seams glowing in the rarity colour (emissive mask or thin beams), inward specks from recipe 5 | 300–670 |
| Burst | Hit frame 50 ms, Blender shell shards outward, `ring_drawn` | 670–900 |
| Reveal (primary) | Item scale 0 → 1.1 → 1 in 200 ms; two `glow_gradient` ray cards rotating in opposite directions behind it; motes | 700–1,400 |
| Banner | Name and rarity, sound stinger | 900–1,500 |

- Time by tier `[lihfolk]` (`game-craft.md`): common 0.3–0.5 s (flash and pop only), rare 1–1.5 s (adds ring and rays), top tiers 5–6 s (add a ground piece, pillar, camera push, world dim). Each tier adds a layer; it does not just get louder. Auto-open modes get a compact reveal.
- Budget: about 20 alive, 2–3 meshes, in front of a calm background. Cheap: flash, pop, banner. Showpiece: top tier only.
- Mistakes: long animation for commons; rays on everything; unskippable; result rolled on the client; strobing.

## 17. Footstep and landing dust

Read: weight and surface. Own character and near neighbours only.

| Layer | Build | Window |
|---|---|---|
| Footstep puff | `puff_set`, Emit 1–2 at the foot marker, Life 0.3–0.45, Size `POP(1.2–1.6)`, Spd 1–2, `VelocityInheritance` 0.2, LE 0, LightInfluence 0.3, Transparency 0.5 → 1, colour from a `Humanoid.FloorMaterial` table | 0–450 |
| Landing ring | `puff_set`, Disc outward, Emit 6–10 scaled by fall speed, Spd 8–12, Drag 5, Life 0.4–0.6 | 0–600 |
| Heavy landing | Add a `ring_drawn` card and medium trauma (0.12) | 0–300 |

- Budget: 2–4 alive while running; only when running, within about 40 studs, every other step on the low tier. Cheap: landing ring only. Showpiece: surface-specific shapes (splash on water, sparks on metal, leaves on grass).
- Mistakes: the same dust on water and metal; dust at walking speed; emitted from the server; opaque puffs; puffs glowing in the dark (set LightInfluence above 0 for matter, and check caves).

## 18. Fire (torch, campfire, burning state)

Read: hot at the base, rising, then smoke. Break the reference into components first `[official]`.

| Layer | Build | Window |
|---|---|---|
| Flame body (primary) | Flame-shaped sprites or a 4×4 loop, Rate 8–12, Life 0.5–0.8, Spd 2–4, Acc (0, 4, 0), Size 1.5 → 0.3, Color hot → body → dark, LE 0.8, Br 3, Rotation ±15 only | Loop |
| Core glow | `soft_dot`, `LockedToPart`, 1 alive, hot colour | Loop |
| Embers | `spark_streak`, `VelocityParallel` with Squash, Rate 2–4, Life 0.8–1.5, Spd 5–8, Acc (0, 10, 0), Drag 0.8, flickering Transparency, LE 1 (motion values `[official]`; the tutorial's Br 20 suits a volcano, start at 6–10) | Loop |
| Smoke | `puff_set`, Rate 1–2, Life 2–3, Acc (0, 2, 0), LE 0–0.1, LightInfluence 0.1–0.3, dark → grey, ZOffset −1, fading in while the flame fades out | Loop |
| Light | `PointLight`, Brightness 1.5–2.5 flickering at 8–12 Hz, Range 12–16, shadows off | Loop |

- Budget: at most 25 alive per fire; sleep by distance; counts against the ambient budget in `performance.md`. Cheap: flame at Rate 6 plus the light. Showpiece: three nested Blender flame shells with a scrolling `Texture`, sparks reacting to wind (`WindAffectsDrag`).
- Mistakes: Rotation 0–360 on flames (fire has an up); additive smoke; a hard cut from fire to smoke; too many embers; a shadow-casting light.

## 19. Lightning strike

Read: warning line, bolt, burst, residue: five beats in under 1.5 s `[community]` (greyscale storyboard in the library).

| Layer | Build | Window |
|---|---|---|
| Warning line | Vertical `Beam`, Width 0.3, Transparency 0.7 → 0.3, LE 1 | −300 to 0 |
| Bolt (primary) | Crossed-ribbon mesh in 3 jagged variants shown 2 frames each, or 2–3 beams with fresh random curves per step; Width 1.2 → 0; white core, body colour edge | 0–100 |
| Flash | `star4` at the ground, `PointLight` Brightness 6, Range 30, 60 ms; no full-screen flash by default | 0–60 |
| Ground burst | `ring_drawn`, forking `spark_streak` sparks (Emit 8, Spd 30, Drag 10, Life 0.2) | 16–300 |
| Residue | Dark spiky `puff_set`, `crack_decal`, 2–3 small embers | 100–1,000 |

- Budget: about 14 alive, 1–3 meshes, 1 light. Cheap: one bolt mesh for 100 ms, flash, sound. Showpiece: branch bolts, a second weaker re-strike at +120 ms, the telegraph from recipe 6.
- Mistakes: a smooth wavy bolt; bolt visible beyond 150 ms; strobing more than 3 flashes a second; blue only, with no white core or dark; lines under 0.8 studs wide that vanish at phone size.

## 20. Water splash

Read: liquid is matter: it has weight, an outline and a ring on the surface. Never additive.

| Layer | Build | Window |
|---|---|---|
| Crown | `splash_set`, `FacingCameraWorldUp`, Emit 2–3, Life 0.3–0.4, Size `POP(3–4)`, Squash stretching upward, LE 0.4 | 0–400 |
| Droplets | Emit 8–12, Life 0.25–0.35, Spd 20–35, SpreadAngle 50,50, Acc (0, −40, 0), LE 0.5, LightInfluence 0.1 `[official]` | 0–350 |
| Surface foam ring | `ring_drawn` or foam sprite, `VelocityPerpendicular`, Spd 0.01, Life 0.5–0.7, RotSpeed ±15, LE 0.25 `[official]`, Size 2 → 5 | 30–700 |
| Mist (large splashes) | `soft_dot`, Life 0.5–1, Spd 35–50 upward, Drag 1.5 `[official]`, Transparency 0.8 → 1 | 0–1,000 |

- Colour and value: blue body turning white at the top; add darker blue inner shapes so it reads against sky.
- Budget: about 16 alive. Cheap: droplets plus foam ring. Showpiece: a 4×4 OneShot splash flipbook, a secondary ring at +150 ms.
- Mistakes: glowing water; droplets without gravity; no ring on the surface; the same splash for a pebble and a boss.

## 21. Environmental ambience

Read: the place is alive, quietly. Ambience is never brighter or sharper than gameplay effects. Budget: 6–10 ambient emitters in view at Rate ≤ 20 (`performance.md`).

| Element | Build |
|---|---|
| Dust motes in light | `soft_dot`, Rate 3–5, Life 6–10, Spd 0.3–0.6, Size 0.08–0.15, LE 0.5, `INOUT` |
| Fireflies | `soft_dot`, Rate 1–2, Life 4–6, Size 0.2, Br 4, Transparency keys blinking 2–3 times |
| Leaves or petals | Leaf shape, Rate 2–4, Life 6–8, Spd 2–3 downward, RotSpeed ±60, Drag 0.5 with `WindAffectsDrag` so `GlobalWind` carries them `[official]` |
| Rain | One emitter box that follows the camera, `spark_streak`, `VelocityParallel` with Squash, Rate up to the mobile cap of 100, Life 0.6–0.8, Spd 60–80; a second emitter for ground splashes at Rate 10 |
| Ground mist | Large `soft_dot` cards, at most 4 alive, Transparency 0.85 or more (large transparent sprites are the overdraw cost) |
| Waterfall or lava | Stacked `Beam`s. Waterfall: Width0 60 → Width1 20, `TextureSpeed` 0.4, `TextureLength` 64, Wrap. Lava: base beam plus two crust beams at `TextureSpeed` 0.01 and −0.008 `[official]` |

- Rules: emitters live in zones or follow the camera, never the whole map; sleep when the zone is out of view; long lifetimes multiply the alive count (`Rate × Lifetime`).
- Mistakes: map-wide emitters; ambience brighter than combat effects; rates above the mobile cap; rain that falls indoors.

## Review gate

- [ ] The effect was blocked in white first and matches its "Read" line in a half-second glance at phone size.
- [ ] Every layer in the table has a role, a window in milliseconds and an end; the bright phase is a quarter of the total or less.
- [ ] The primary layer is drawn at the exact hit volume and carries allegiance where teams exist.
- [ ] Untested `[house]` values were tuned against a frame-by-frame capture; nothing is shipped at recipe defaults unseen.
- [ ] Textures come from the shared kit (or a justified addition); meshes are Blender kit pieces, pooled and non-colliding.
- [ ] The cheap version is the low tier; the showpiece version is reserved for importance 8–10.
- [ ] Scored with the rubric in `vfx-and-juice.md` §16.

## Sources

Accessed 2026-11-11. Detail and links for each are in `vfx-and-juice.md` Sources and the two `visual-library/vfx*.md` files.

- Roblox/creator-docs at commit 7cbffff (read): `tutorials/use-case-tutorials/vfx/use-particles-for-explosions.md` (spark burst values), `create-volcanoes.md` (embers, ripples, lava splash, lava flow beams, smoke plume), `create-waterfalls.md` (cascade beams, splashes, white water, foam, mist); `effects/particle-emitters.md` (shapes, drag, flipbooks, wind).
- LihFolk Vault V2 (CC BY 4.0) (read): timing table, telegraph formula, hit-stop tiers, dash FOV, reveal time by tier.
- realtimevfx.com and 80.lv (read, images viewed): Riot missile anatomy and heal conventions (McDonald), three-stage timing and element table (Jevremović), projectile hot point and shadow (Leroy), lightning storyboard (jqarlsson), slash, explosion, shockwave and heal references listed in `visual-library/vfx.md`.
- DevForum (read): first-person hiding of avatar effects (staff), inward emission, crescent slash mesh, fire-to-smoke critique.
- No source gives full Roblox property sets for most of these effects: the layer structures follow the references, and the unsourced numbers are house estimates awaiting an in-engine pass.
