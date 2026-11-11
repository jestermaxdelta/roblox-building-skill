# VFX reference library: images, breakdowns and showcases

What this is: 62 checked references for stylised game effects: annotated stills from shipped games, frame sequences of slashes, impacts, explosions, lightning, heals and shields, texture and mesh breakdowns, Roblox diagrams, critique cases and reels. The rules they support live in `references/vfx-and-juice.md` (§1 principles, §5 authoring, §14 generic tells, §16 rubric) and the builds in `references/vfx-recipes.md`. Tutorials, courses, tools and texture sources are in `vfx-learning.md`.

How to use this file:
- Pick the effect you are building, open two or three rows, and write down what you will copy as a number or a shape (frames of brightness, number of layers, where the dark sits) before opening Studio.
- Evidence: `viewed` = the image was downloaded and looked at; for a GIF, six evenly spaced still frames were looked at, not the motion; `read` = the page or thread was read; `oembed` = the video exists with that title and creator, it was not watched, and the note comes from its title or the thread that led to it; `search` = not opened.
- These are references to study, not assets to copy: every third-party image, clip, texture and mesh stays its owner's. Most are from Unity or Unreal; the shapes, values and timing transfer, the shaders do not (`vfx-and-juice.md` §5 maps each trick to Roblox). Accessed 2026-11-11; every page and image link re-checked the same day (all respond).

Image host prefixes: `RT` = `https://realtimevfx.com/uploads/default`, `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads`, `DOCS` = `https://prod.docsiteassets.roblox.com/assets`, `LV` = `https://cdn.80.lv/api/upload/content`. Thread links are `https://realtimevfx.com/t/<id>` and `https://devforum.roblox.com/t/<id>`.

## 1. Readability, value and hierarchy

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Anatomy of a League of Legends missile, part 1](https://realtimevfx.com/t/11614), Oli "Beardilocks" McDonald (Riot), 2020: annotated Veigar Q `RT/optimized/2X/c/cfef348efa33e9dfef4e470839d5c31e73b2b133_2_619x500.jpeg` | image | The missile head is the brightest, most saturated, sharpest shape and shows the hitbox width; trail and cast effect are darker and softer. A value ramp at the left runs white → magenta → near-black purple | viewed |
| 2 | Same thread: focus versus rest `RT/original/2X/0/06a9c6c6766f9aa875fca5777ab5770c0490d720.jpeg` | image | Two labels to copy as a checklist: "highest value, most contrast, highest saturation, sharpest shapes" at the head; "lower value, less contrast, lower saturation, softer shapes" on the trail | viewed |
| 3 | [Anatomy of a League of Legends missile, part 2](https://realtimevfx.com/t/13062), McDonald, 2020: Morgana Dark Binding `RT/original/3X/1/4/144d19815d6803ca6a93989a7abee614b651121f.jpeg` | image | Four identifiers on one projectile: teardrop shape, chain-link motif, long trail, a solid object inside a glowing shockwave. Identity that survives a recolour | viewed |
| 4 | Same thread: visual hierarchy sheet `RT/original/3X/d/e/de2193134e2434cbb8f5a064bfbd76c8e65217d8.png` | image | A spreadsheet rating each ability 0–10 for self, enemies and allies with a notes column and a key of example abilities; the range circle is 0 for allies, so they never see it | viewed |
| 5 | Same thread: heals `RT/optimized/3X/a/9/a983a92d6758d8e1f591187c289d79b1c1fcf52a_2_690x348.jpeg` | image | Four heals from different characters, all green, all round; the caption on the missile: "should not feel threatening (no sharp shapes)" | viewed |
| 6 | Same thread: roots `RT/original/3X/4/a/4ae30b48c1594681382eab44a7994b84697dca82.jpeg` | image | Six skins in six palettes, one mechanic: every root is a ring on the floor plus a cage or cylinder around the target | viewed |
| 7 | Same thread: team fight `RT/optimized/3X/f/3/f3a6d478444c6dbeb48ad8ccf0255f727bf84af5_2_665x500.jpeg` | image | Ten players' effects on one screen. Count how many shapes you can still name: the case for quiet basic attacks and importance ratings | viewed |
| 8 | [Block-ins and Timing](https://realtimevfx.com/t/29830), Jason Keyser, 2025: finished effect `RT/original/3X/3/a/3aca77cd3e6d5f27f0a3d94a349cb9f0323d8c04.gif` | image | Yellow pillar as anticipation, a magenta burst, then a dark cracked crater. Of six evenly spaced stills two are bright (pillar, burst); the rest is empty ground or residue fading | viewed |
| 9 | Same thread: block-in version `RT/original/3X/8/b/8b3f66bf34297af7f290182f0368a001153c9dc0.gif` | image | The same beat built from a white dome, a ring and a four-point star, greyscale only. If this reads, the polish is safe | viewed |
| 10 | [Very Cartoonic VFX for Brawl Stars made with Flash](https://realtimevfx.com/t/11032), Woo (Supercell), 2019: explosion source shapes `RT/original/2X/7/7559d269960c624369bf31cd5a6de4f708765ca8.png` | image | The whole explosion kit is about 14 flat white shapes: teardrops, a dot, a soft dot, quarter arcs from thick to hairline. Constraints stated in the post: no custom shaders, plain quads, many ground colours, team side must be obvious | viewed |
| 11 | Same thread: explosion frames `RT/original/2X/f/f8f374267907103fddb8f19abf9cdef720732bca.gif` | image | Flat red blobs with a darker red shape inside each for volume; no gradients, no glow; ground part and air part animated separately with random cloud variants | viewed |
| 12 | Same thread: in-game shot `RT/original/2X/e/ef7e2aed37fc1e9296afb60cfeef4f2e8c13907e.gif` | image | One-frame white star at the muzzle, a chunky cyan projectile, an impact puff, a damage number; green ring under the ally and red under the enemy. Opaque shapes read on a purple floor | viewed |
| 13 | [VFX Staples: Shape, Color, and Motion](https://80.lv/articles/vfx-staples-shape-color-and-motion/), Stefan Jevremović (Nordeus, mobile), 2018: element table `LV/c7/images/5d2c6ca037af8/widen_920x0.png` | image | Twelve elements (fire to lightning), each with a 4–6 step colour ramp, its secondary elements (fire: smoke, sparks, embers) and which of shape, colour or motion defines it (lightning: forking motion) | viewed |
| 14 | Same article: three stages `LV/c7/images/5d2c6ca0f313c/widen_920x0.png` | image | A meteor split into anticipation (ground ring and falling ball), climax (white-yellow core, purple rim as the complement, debris, dark smoke) and dissipation (a dark crack decal and nothing else) | viewed |
| 15 | Same article: paladin attack `LV/84/5d2c6c9b91619.gif` | image | Top-down mobile camera on a mossy stone floor: gold flash on the caster, a warm cone, a white-gold flash on the target. Three beats, each readable at small size | viewed |
| 16 | [How do I make my timing better?](https://realtimevfx.com/t/17547), reply by Limeslushie, 2021: curves `RT/optimized/3X/d/1/d177d426189a61e236185d7da104fa68b456842f_2_611x500.png` | image | Two hand-drawn curves: "flash" spikes then decays in a long tail; "explosion" scale jumps to most of its size at once then creeps. The reply steps a real explosion through four frames | viewed |
| 17 | [Spyro: Sketch #22](https://realtimevfx.com/t/8642) (greyscale challenge), Spyro, 2019: tornado `RT/original/2X/6/6b980af2947f59a2c034102840639712e0844ec7.gif` | image | A tornado in white ribbons over a black core, capped and grounded by rings. Fully readable with no colour at all | viewed |
| 18 | [Lush: Sketch #22](https://realtimevfx.com/t/8474), Lush, 2019: grenade concept `RT/optimized/2X/6/673eecd118d595eb40d578bf45c1fd87362ece13_2_690x388.jpeg` | image | A greyscale concept painting with a top-down range diagram in the corner: the concept states the gameplay radius before any effect exists | viewed |

## 2. Slashes and trails

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 19 | [Siberi4: Slash VFX](https://realtimevfx.com/t/11020), Romel Heidi, 2019 `RT/original/2X/f/f92ca58b599bec76db02cc56d79eb9cf7dd5bed4.gif` | image | Thick orange crescent, white-yellow leading edge, one thin straight streak cutting across it, sparks trailing along the swing. The body is gone within a few frames; embers stay | viewed |
| 20 | [Fire Swoosh 2D VFX](https://realtimevfx.com/t/15426), PBJayz, 2020 `RT/original/3X/4/2/422b330d8374009e7d664354b8472910ba24dbbf.gif` | image | Hand-drawn frames: white-yellow tip, orange-red body, then a near-black smoke shape takes over the same arc and breaks into blobs. Bright for under a third of its 30 frames; flat colours only | viewed |
| 21 | [Venom Slash (breakdown included)](https://realtimevfx.com/t/18903), Geri, 2022: mesh and mask `RT/original/3X/4/0/404c1427f6100827fb5f732065bad8b73f491647.jpeg` | image | The slash is a static tilted ring (washer) mesh; a soft vertical capsule mask hides all but the swing segment | viewed |
| 22 | Same thread: noise layers `RT/optimized/3X/7/e/7ef9a18a1fb91622f809e1494293fd70d1da8f37_2_690x274.jpeg` | image | Two noise textures multiplied; one scrolls while the mesh stays still, which makes the streaks travel | viewed |
| 23 | [Crecent Sword Slash Effect](https://devforum.roblox.com/t/1113871), ImaginePowerq, 2021 (151 likes): result `DF/original/5X/a/3/0/e/a30e1b7bb83abbfa614fffb574ed6eb2f4620587.png`, mesh `DF/optimized/5X/b/6/f/4/b6f4fdc8669d8d1297c4ef8d3808576fa69c9f1e_2_517x282.jpeg` | image | The Roblox version: a squashed sphere modelled in Blender, UV-mapped per side, with two `Texture` objects on a transparent mesh | viewed |
| 24 | Same thread: texture steps `DF/optimized/5X/e/1/0/9/e109e392ae9a4fe7ddca9ee6d3384699b68d051d_2_517x305.png`, `DF/optimized/5X/2/b/a/4/2ba488afee1c374b9b448da43c24271a8e74dd3e_2_517x315.png` | image | Horizontal lines of varied thickness and opacity, then GIMP's Polar Coordinates filter turns them into a swirl | viewed |
| 25 | [Rubfish/Rafles VFX stuff](https://realtimevfx.com/t/8465), Sr. Rubfish, 2019 (94 likes): anime impact `RT/original/2X/1/1f4a1334e361f0f74070318667779c14e8b60a05.gif` | image | Cyan crescent with a white core and a warm rim glow at the contact point, thin speed lines back to the source; one bright still out of six | viewed |

## 3. Impacts, explosions and shockwaves

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 26 | [Stylized Frag Launcher Explosion](https://realtimevfx.com/t/1894), Atif, 2017 `RT/original/2X/3/30d2b1828d0525cb20281186f4167f7bff536f02.gif` | image | White core, radial streaks of uneven length, a thick orange ring with a wavy inner edge that breaks into arcs; then only sparks on brown haze. The post counts 18 short-lived layers; the last 60% of the clip is nearly empty | viewed |
| 27 | [Seeking advice to create shockwave textures](https://realtimevfx.com/t/25874), reply by McDonald, 2024 `RT/original/3X/3/e/3e2590725e8139493b7e2d2956b8677958035ebe.jpeg` | image | Four panels with ticks and crosses: guide lines at uneven angles and lengths (right) versus equal spacing (wrong); an outer line with varied curvature; an inner cut-out; the filled white ring | viewed |
| 28 | Same thread: the target effect `RT/optimized/3X/6/f/6f6f7a66439018e49d3a18e74bd674667c7d3c40_2_534x500.jpeg` | image | A radial burst: white centre, long uneven spikes, slight colour fringing at the edges, dark silhouettes in front | viewed |
| 29 | [Rolling rock shockwave breakdown, Rhei'a (Seekers of Skyveil)](https://realtimevfx.com/t/28613), McDonald, 2025 `RT/original/3X/d/4/d48ba44f97191ac91874b1fff2ca5f26d3e4db4b.gif` | image | Thin ring and crack lines as the warning, an orange crescent sweep with rocks rising, a rock wall with glowing cracks, then a dark cracked ring. Orange on green ground; the rim marks the exact radius | viewed |
| 30 | [Easy Impact Frames](https://realtimevfx.com/t/30252), Lush (Vefects), 2026 `RT/optimized/3X/6/7/679a1a8a899cf459c3ba22dc9dfb8ef5c6931b9e_2_690x388.jpeg` | image | The anime impact frame: scene reduced to black and white, the character as a silhouette, radial streaks from the hit. One frame, not a strobe | viewed |
| 31 | [Particle emitters: flipbooks](https://create.roblox.com/docs/effects/particle-emitters#flipbooks), Roblox docs: sample sheet `DOCS/lighting-and-effects/particle-emitter/8x8-Explosion.png` | image | An 8×8 explosion on black: a growing dot in row 1, the fireball for about 16 frames, darkening smoke for the second half. Spacing around every cell | viewed |
| 32 | Rubfish thread (row 25): fire shot `RT/original/2X/c/c347c3ee481e07b8c5e1ac09f02256a57147fe4b.gif` | image | An orange streak with a dark smoke wake behind it; after the hit only a few sparks and a grey smear remain | viewed |
| 33 | [Modular Approach to AOE VFX Breakdown](https://realtimevfx.com/t/31540), Jonathan Price, 2026 `RT/optimized/3X/f/3/f39c38aecb8011e5e70471ff72cf5200b418395e_2_690x389.jpeg` | image | An ice pool: a rune ring marks the exact radius and is brighter than the fill; shards stand inside. The post explains building AoEs from shared components driven by a data table | viewed |

## 4. Projectiles, beams and lightning

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 34 | [Lightning VFX WIP](https://realtimevfx.com/t/3936), jqarlsson, 2018 (137 topic likes): storyboard `RT/original/2X/a/a17526922b115e81462b12504bff314af72dc7a4.jpg` | image | Five greyscale beats on one strip: faint line, brighter line, jagged bolt, white spiky ground burst, black spiky debris on a ground disc. A whole effect planned before any engine work | viewed |
| 35 | Same thread: first iteration `RT/original/2X/7/73114ab9e578c3e15ab3f22d97d95f27f945b2fa.gif` | image | A thin warning line, then dark spiky smoke with a small blue ember on the ground that lingers | viewed |
| 36 | [Breakdown: Stylized Energy Beam](https://realtimevfx.com/t/21866), Fabrício Duarte, 2022 `RT/original/3X/8/0/804a3bdefad0e904129e81728ca9859d965672a0.gif` | image | One magenta hue plus a white core carries the whole effect: converging burst, four-point star, expanding rings, beam, collapse to a dot. The post lists each phase; the beam is a Blender mesh with a scrolling texture | viewed |
| 37 | Rubfish thread (row 25): charged laser `RT/original/2X/6/61a75b90a8101dfc5bed30bdf52fff5728616e58.gif` | image | Glow gathering at the source, a thin blue beam, dark debris smoke at the impact; nothing left in the last still | viewed |

## 5. Heal, shield and area effects

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 38 | Rubfish thread (row 25): flower heal `RT/original/2X/f/f48ab08ebb3179d4b7cf90870f346604a3712487.gif` | image | A green ring on the ground marks the area, a pale column of light, small pink and white petals rising. Nothing sharp, nothing fast | viewed |
| 39 | Rubfish thread (row 25): water shield `RT/original/2X/5/53207fabf2e9ce74db72560f009e11f02905dd18.gif` | image | An icon above the unit as anticipation, then a flattened disc of swirling pale-blue streaks with a bright centre and soft edges | viewed |
| 40 | [Healing spell concept art](https://realtimevfx.com/t/21022), Ryukai, 2022 `RT/optimized/3X/f/2/f25fe07710d72350a7c00af7d78bffc4b8465bd3_2_690x487.jpeg` | image | A four-frame storyboard of a heal and the critique it received: too many components, a pentagram and a flame both read as hostile; later versions switch to vines and petals | viewed; read |

## 6. Texture and mesh authoring

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 41 | [Shannon McSheehan: LoL FX + Knowledge Share](https://realtimevfx.com/t/1133) (221k views), post 6 "Trails with Shannon", 2016 `RT/original/2X/3/302f8478e20ea916ff8274c8adee44c00831413f.jpg` | breakdown | Seven painted steps for a trail texture: overall shape, carve the flow, primary and secondary shapes, narrow the values, motion blur along travel, soften the background, colour by gradient map (navy → blue → cyan; dark red → orange → yellow) | viewed |
| 42 | [VFX Basics: Mesh Soulercoasters](https://realtimevfx.com/t/1987), Augie, 2017 (142 likes) `RT/optimized/2X/1/12c52df6caaaef60b79115105b1a5a5be41c8f94_2_690x326.jpg` | breakdown | A spiral ribbon mesh beside its UVs: a plain straight rectangle, with an arrow for the scroll direction. Straight UVs are what make a texture travel along any path | viewed |
| 43 | [Smoke sprite sheet](https://realtimevfx.com/t/10838), reply by LudeosShaft, 2019 `RT/optimized/2X/f/fc2d1fe397331cb5590495833cd896028534fad8_2_500x500.png` | image | A smoke puff made from a clouds-noise filter and paint: the noise pattern is still visible. The reply lists four ways to get smoke textures (simulation, photo work, hand painting, shader) | viewed; read |
| 44 | [Create volcanoes](https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/create-volcanoes), Roblox docs: splash sheet `DOCS/tutorials/creating-volcanoes/WebbySplash-Texture.jpg` | image | An official 8×8 flipbook in white on dark: a dot stretching into a stringy splash, with margins | viewed |
| 45 | Same tutorial: ember sprite `DOCS/tutorials/creating-volcanoes/Embers-Texture.jpg` | image | A soft elongated oval crossed with a shorter one: the shape that `VelocityParallel` plus `Squash` turns into an ember streak | viewed |
| 46 | [Custom flipbook layouts](https://devforum.roblox.com/t/4005128), Roblox staff, 2025: example B `DF/original/5X/d/2/0/b/d20bdec079b6122599a42c580e72027b02940935.png` | image | The same 512² texture laid out 4×8 instead of 4×4: twice the frames, each frame wider than tall, matching the motion | viewed |
| 47 | [How can I recreate this VFX effect?](https://devforum.roblox.com/t/4886877), reply by eatabler0ck, 2026 `DF/optimized/5X/f/a/8/0/fa809588c6405d37ff7e8d3371616d5dde15171f_2_276x189.jpeg` | image | A lens-shaped disc mesh that carries a sprite sheet on its top and bottom faces, advanced by a script: the "mesh flipbook" used for sword arcs on Roblox | viewed; read |

## 7. Roblox diagrams and official samples

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 48 | [Beams](https://create.roblox.com/docs/effects/beams), Roblox docs `DOCS/engine-api/classes/Beam/Curvature-Diagram.png` | image | P0 to P3 of the Bézier: `CurveSize0` and `CurveSize1` push the control points along each attachment's axis, so rotating an attachment bends the beam | viewed |
| 49 | [Particle emitters: shape](https://create.roblox.com/docs/effects/particle-emitters#shape), Roblox docs `DOCS/lighting-and-effects/particle-emitter/Disc-ShapePartial-0.5.jpg` | image | A disc emitter with `ShapePartial` 0.5 drawn as a red ring: emission from an annulus, the basis of ground rings | viewed |
| 50 | Create volcanoes (row 44): `DOCS/tutorials/creating-volcanoes/Sample-Components.jpg` | image | The sample labelled as five components (embers, smoke plume, lava splashes, surface ripples, lava flow): the official method is to break a reference into parts and assign one instance type to each | viewed |
| 51 | [Auto-quality level improvements](https://devforum.roblox.com/t/4977292), Roblox staff, 2026-11-05 `DF/optimized/5X/0/e/6/1/0e61d4422db53634360af9ca0401799b55d16580_2_690x495.png` | image | Where to preview low quality: Studio Settings → Rendering → Editor Quality Level set to Level 01 | viewed; read |

## 8. Critique cases from the DevForum

Posts by developers who asked for feedback. Study what the replies suggested and what `vfx-and-juice.md` §14 would add.

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 52 | [How can I make VFX look more dynamic and better?](https://devforum.roblox.com/t/2898977), 2024 `DF/optimized/5X/9/d/c/2/9dc2cb460b5b50ff798c3176669d082c57eebd3e_2_388x500.jpeg` | image | A fire tornado of orange and dark spiral ribbons. Replies: add dust that reacts to the ground material; add white highlights. Also missing: tapering, a hot core, anything at ground contact. Compare with row 17 | viewed; read |
| 53 | [Feedback on VFX](https://devforum.roblox.com/t/4824974), 2026 `DF/optimized/5X/8/1/2/9/8129be99782878f4553f134393e769cbec93ee4c_2_460x500.jpeg` | image | A heal zone: pillar, plus sign and concentric ground rings, all pale and soft. The idea is clear; value contrast is not. Compare with row 38 | viewed; read |
| 54 | [What should I do about my explosion visuals?](https://devforum.roblox.com/t/3114938), 2024 `DF/original/5X/5/8/b/1/58b1c3d3e12adc0332a4ebef5ffcbbb7e011b96b.jpeg` | image | Explosion variants built from clusters of same-size soft blobs in several hues: the default-emitter look. Compare with rows 11 and 26 | viewed; read |
| 55 | [Out of place fire VFX compared to my smoke](https://devforum.roblox.com/t/4850341), 2026 | breakdown | Replies converge on one fix: overlap the two layers, fading the flame out while the smoke fades in, and vary colour | read |

## 9. Reels and showcases (video)

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 56 | [Shannon Berke VFX Demo reel 2016](https://www.youtube.com/watch?v=drTrkPoJ3O4), Shannon McSheehan | video | Shipped League of Legends champion effects; her post says gameplay comes first, so nothing is too flashy | oembed |
| 57 | [Fan-Made League VFX](https://www.youtube.com/playlist?list=PLXily77ZuhLEC3vb5cq0uTEj20S0t5KY2) (playlist), Sirhaian (Kevin Leroy); [project thread](https://realtimevfx.com/t/1435), 2017 (151 likes) | video | About 50 spells for 14 fan skins; the thread shares the Unity project for study only (Riot characters; do not reuse) | oembed; read |
| 58 | Sr. Rubfish channel: [Anime Impact](https://www.youtube.com/watch?v=HfIKJ6a9gUY), [Healing area](https://www.youtube.com/watch?v=WOK2kU5j39k), [Water Projectile](https://www.youtube.com/watch?v=K5xOLbIkkqk), [Laser](https://www.youtube.com/watch?v=8UNWDsZ8cNo) | video | Full-speed versions of rows 25 and 37–39; the thread describes them as studies in "progression and visibility" | oembed |
| 59 | [Rock Shockwave Effect Breakdown for Rhei'a](https://www.youtube.com/watch?v=YRCC3VXBYZk), Oli McDonald, 2025 | video | The mesh method behind row 29 | oembed |
| 60 | [Meteor Strike Breakdown](https://vimeo.com/238504185), Stefan Jevremović, 2017; [thread](https://realtimevfx.com/t/3299) | video | Layer-by-layer build of the mobile meteor in row 14 | oembed |
| 61 | Roblox: [Shanks & Mihawk VFX](https://www.youtube.com/watch?v=YDrrHwNNBy0) and [Sword Combat 2](https://www.youtube.com/watch?v=TzhIKHlpWvM), hazu; [KJ's Stoic Bomb](https://www.youtube.com/watch?v=0oaQSZo_wSg), Pew | video | Roblox anime-style combat effects that DevForum threads ask how to recreate (mesh flipbooks, synced two-character animation). Study timing and layering; any mesh you want from them is rebuilt in Blender (house rule 1) | oembed |
| 62 | [Zelda: Breath of the Wild, fire and explosions compilation](https://www.youtube.com/watch?v=kZV7ld4gIKE) | video | The reference one artist used for cartoon cooking smoke, fire and debris explosions in [this thread](https://realtimevfx.com/t/1490) | oembed |

## Places to browse (not checked row by row)

- [Sakugabooru, effects tag](https://www.sakugabooru.com/post?tags=effects): hand-drawn anime effects clips, recommended by artists in [this thread](https://realtimevfx.com/t/625) for shape and timing study (site opened; clips not viewed).
- [Realtime VFX sketchbooks](https://realtimevfx.com/search?q=sketch%20order%3Alikes): Hovl, Niels, Simon Trümpler and Alex Fedorov have the most-liked threads (search results read; threads not opened).
- Behance "Brawl Stars VFX" by Woo and ArtStation breakdowns linked from rows 29 and 33 (not opened: those sites do not load here).

## Sources and licences

- realtimevfx.com: posts and images belong to their authors; read through the public forum JSON. League of Legends images are Riot Games' property, Brawl Stars images Supercell's, shown by their own artists.
- 80.lv interview images belong to the interviewed artists. Roblox Creator Docs text is CC BY 4.0 (`Roblox/creator-docs`); that licence statement names the prose, not the images, so docs images are © Roblox and are linked here for study, not redistributed. DevForum uploads belong to their posters.
- GIF rows were judged from six still frames each; motion and exact timing were not seen. Counts such as "8 of 30 frames" come from the frame indices of those stills.
- Not reachable: artstation.com, behance.net, vfxapprentice.com (403), the Riot VFX style guide PDF (old links redirect).
