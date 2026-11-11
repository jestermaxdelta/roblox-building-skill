# Lighting and mood reference library

What this is: 25 checked references for lighting and mood in day, dusk, night, interior, cozy and horror scenes, with before-and-after pairs where they exist. The values and safe ranges that turn these looks into Roblox settings live in `references/lighting-and-atmosphere.md` (key and fill in §2, time of day in §4, presets in §12); the review tests are in `references/art-direction-and-quality-bar.md` §8.

How to use this file:
- Choose the mood, open two rows for it and one pair row, and write three things before touching `Lighting`: where the key comes from, what colour the shadows are, and which one or two things are allowed to be warm (or bright). Then view the reference in greyscale and at 320 px wide: if the mood survives, value carries it and it will survive a phone with shadows off.
- Evidence: `viewed` = the image was downloaded and looked at; `read` = the page or thread was read; `oembed` = video verified, not watched; `search` = seen in search results only, not opened.
- These are references to study, not assets to copy: every image stays its owner's. Most were rendered in engines with features Roblox lacks (baked bounce light, volumetric shafts, many shadowed lights), so take the plan (key, fill, accents, value), not the technique.

Image host prefixes: `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads/original`, `LV` = `https://cdn.80.lv/api/upload/content`, `DOCS` = `https://prod.docsiteassets.roblox.com/assets`. Rows named "env" or "models" point at `environments-and-maps.md` and `models-props-characters.md`.

## A. Day

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Enhance outdoor environments](https://create.roblox.com/docs/tutorials/use-case-tutorials/lighting/enhance-outdoor-environments), Roblox · `DOCS/tutorials/enhancing-outdoor-environments/Intro-Before.png` | image | Weak on purpose: the starting state. High sun, blue sky, every green equally lit; the campfire is warm but changes nothing around it | viewed |
| 2 | Same page · `DOCS/tutorials/enhancing-outdoor-environments/Intro-After.png` | image | The same camp with a low sun behind the trees, haze and a warm grade: the path becomes the light shape, trunks become dark frames, the fire now belongs | viewed |
| 3 | Same page · `DOCS/tutorials/enhancing-outdoor-environments/Bad-Skybox.png` and `…/Good-Skybox.png` | image | A chrome ball under two skies: the sky is the reflection and the ambient colour of everything, so a teal sky tints the whole scene | viewed |
| 4 | env row 6 (Medieval Market) and env row 28 (beach) | image | Bright day done well: cream walls in the light, cool shadows, nothing black; distance fades to pale flat bands | viewed |
| 5 | env row 20 (resort pool) | image | Weak: bloom as "quality". Sky and floor burn out and the two-hue palette is lost | viewed |

## B. Dusk and golden hour

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 6 | [Map Design and Scene Building](https://devforum.roblox.com/t/709866), Ahlvie, 2020 · `DF/4X/b/1/7/b17e510f03d0a8ddaa0a6d5f8d26b6c16c9cf9f1.png` | image | One house at flat noon and at dusk: warm windows and lanterns against a cooler sky make it read as lived in. No geometry changed | viewed |
| 7 | [Japanese Countryside](https://devforum.roblox.com/t/4727106), FrostFareswof, 2026 · `DF/5X/5/e/c/5/5ec553e9c4f67e57767ce55d320f2aa5c25442a1.jpeg` | image | A dusk street: paper-screen windows and two orange lanterns are the only warm areas in a green-grey scene; the road is a dark leading shape with white kerb lines. Realistic style | viewed |
| 8 | Same thread · `DF/5X/5/4/4/4/5444e5e456cd12010a8ae0a05ca42eb1c620772a.jpeg` | image | From under an eave: a dark foreground frame and the lit house across the road as the destination | viewed |
| 9 | env row 30 (Athonite) | image | A dark mass against an orange sky with fog at its base: at dusk the silhouette is the picture | viewed |

## C. Night

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 10 | [Day & Night in Stylized Scenes](https://80.lv/articles/day-night-in-stylized-scenes), Anouk Debruyne, 2017 · `LV/51/5d2cab186c97e.jpg` | breakdown | Night shown by hue, not darkness: a purple-grey sky with every surface readable; a string of lanterns repeats the warm accent across the frame. She dimmed sun and sky light until they barely mattered and lit with props | viewed |
| 11 | Same article · `LV/e3/5d2cab1a85194.jpg` | image | Fire pit and two chairs as the focal group; fog over the lake separates the tree line; many small glows instead of one big light | viewed |
| 12 | Same article · `LV/8d/5d2cab1cb4833.jpg` | image | Pines stay green at night; the glow at the outhouse door shows how little light a waymarker needs | viewed |
| 13 | [Nordic Village](https://80.lv/articles/building-a-game-ready-nordic-village-scene-with-day-night-lighting-setups), Danylo Kyslenko, 2026 · `LV/53/6ada780ce57e4.jpeg` | breakdown | Windows as the only sources, spilling onto fence and plants; a sky lighter than the roofs keeps the roofline. Pair with env row 10, the same village by day | viewed |
| 14 | [Cozy Modern Bedroom](https://sketchfab.com/models/ea25adc53f514eaba9dd043f5eac9c77), dylanheyes, 2023, CC BY | image | Mixed: one cyan hue for the whole room with emissive wall shapes. Strong mood, weak readability: only value separates the bed from the floor | viewed |
| 15 | env row 58 (city at night board) | image | Night mood references kept apart from structure references | viewed |

## D. Interiors and cozy

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 16 | [Enhance indoor environments](https://create.roblox.com/docs/tutorials/use-case-tutorials/lighting/enhance-indoor-environments), Roblox · `DOCS/tutorials/enhancing-indoor-environments/Sample-Start.jpg` and `…/Sample-Complete.jpg` | image | One shelf under the starting look (dim, blue, the wood unreadable) and after tuning (sun through the window at an angle, warm ambient, candle pools): materials appear only once the light is set | viewed |
| 17 | [The Mystery of Duvall Drive](https://create.roblox.com/docs/resources/the-mystery-of-duvall-drive/construct-the-house), Roblox · `DOCS/resources/mystery-of-duvall-drive/constructing-the-house/overview.png` | image | A dark library made of pools: fireplace, table lamps, three ceiling spots; a cool ambient keeps the walls visible; the bust in the foreground catches a rim | viewed |
| 18 | [Making a Cozy Stylized Room](https://80.lv/articles/making-a-cozy-stylized-room-in-blender-and-photoshop), Margarita Posledovich, 2022 · `LV/59/6213c37d17de4.jpg` | breakdown | Cozy by palette and density: peach and pink only, the window as a soft blown key with a faint purple fill from the opposite corner, clutter concentrated on desk and shelves, a clear floor, dark plants as a foreground frame | viewed |
| 19 | [Modular Approach to Stylized Environments](https://80.lv/articles/001agt-002mrs-crafting-a-low-poly-model-kit), Rodrigo Gonçalves, 2019 · `LV/78/5d28761268e42.jpg` | image | The cabin of env row 39 in the editor: about fifteen small point lights, one per lamp, plus area fills. Light sources are props, and each pool marks a place to be | viewed |
| 20 | [Creating a Stylized Witch Hut Interior](https://80.lv/articles/creating-a-stylized-witch-hut-interior-in-ue4), Angelo Tsiflas, 2020 · `LV/84/5f96a1a027614.jpg` | image | The rig from outside the room: one directional light through the window and a few boxed fills; nothing else | viewed |
| 21 | env rows 41 and 43 (café, restaurant) | image | Window light as two floor patches in an otherwise calm room; glowing windows as fill behind warm wood | viewed |

## E. Horror

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 22 | [Designing a Scene With Horror Vibes](https://80.lv/articles/designing-a-scene-with-horror-vibes-in-unreal-engine-5), Justin Hien, 2022 · `LV/9f/6359105880b54.jpg` | breakdown | One red porch light as the focal point of a near-black house; a small warm shed light as the second read; the sky is dark blue with stars, not black, so the roofline holds | viewed |
| 23 | Same article · `LV/bb/6359107528cea.jpg` | image | A low camera through grass; red on the left and amber on the right split the house; foreground blades as a dark frame | viewed |
| 24 | env row 45 (Duvall Drive early version) | image | A single green shaft behind a dark roofline: one unnatural colour is enough to say "wrong" | viewed |

## F. Shading style and technique

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 25 | [How Shedworks refined the art of Sable](https://www.gamedeveloper.com/gdc2022/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability), Game Developer, 2022 | breakdown | Flat shading loses depth; it was recovered in layers: lighting, distance fog, then line work, with characters casting shadows wherever possible so they sit on the ground | read |
| 26 | [Cel shade using a normal map](https://devforum.roblox.com/t/4880290), yamashio, 2026 · `DF/5X/9/2/4/a/924a5309dc3c12008f4ecb1c7764fc7ed9df155b.png` | tutorial | A two-tone toon terminator on a character from a hand-drawn normal map under stock Studio lighting `[VS]`: shading style as an authored choice, not a post effect | viewed |
| 27 | [Solid Coloring Cookbook](https://devforum.roblox.com/t/2031219), SuperSpaceMan230, 2022, and [Stylized Flat-Color Art](https://devforum.roblox.com/t/1510773), Flumzee, 2021 | tutorial | The unlit flat-colour look by lighting values (ambient near white, brightness 0, shadows off). Both lean on the retired `Technology` setting `[VS]`: read for the idea that removing light makes shape and value carry everything | read |
| 28 | models row 32 (Team Fortress 2 paper) | breakdown | Shadows go cool, not black; saturation rises at the edge between light and shade; rim light instead of outlines | read |
| 29 | [The Complete Guide to Lighting in Roblox Studio](https://devforum.roblox.com/t/1876371), smartycar23, 2022 | tutorial | A video-led walkthrough of lighting properties (54 likes); predates the unified-lighting change `[VS]` | search |
| 30 | [Setting Up Lighting for a Cozy Forest Scene](https://80.lv/articles/setting-up-lighting-for-a-cozy-forest-scene-in-unreal-engine-5-1) and [Horror lighting study](https://80.lv/articles/artist-shows-a-ue5-horror-lighting-study-featuring-hinako-from-silent-hill-f), 80 Level | breakdown | Further cozy and horror lighting write-ups found in search | search |

## Patterns seen

- **Mood came from a plan of three things**: key direction, shadow colour, and one or two permitted warm (or bright) accents. Dusk street (7), night cabin (10), horror house (22) and library (17) can each be described that way in one sentence.
- **Night was a hue.** Purple-grey or blue with every surface readable (10–13); the sky stayed lighter than the roofs so silhouettes held. Nothing good was black.
- **Light sources were props, and they were small and many**: lanterns on a string (10), a dozen lamp lights (19), windows (13), candles (16). Each pool marked a place to stand or go.
- **Warm against cool did the separating**: orange windows in green-grey (7), red porch in blue-black (22), fire against purple (11).
- **Before-and-after pairs changed no geometry** (1–2, 6, 16): sun angle, ambient colour, haze and a mild grade did the work.
- **Foreground frames** (dark eave, grass, plants) appear in most composed shots (8, 18, 23).
- **The sky is a light source** (3): choose or author it with the palette.

## What the weak examples had in common

- **Noon sun and a default blue sky**: every surface equally lit, so nothing leads (1).
- **Effects standing in for a plan**: bloom until the sky burns out (5).
- **One hue over everything**: mood without readability (14; env row 13 is the outdoor version).
- **Warm sources that light nothing**: a fire or lamp that does not change its surroundings looks pasted on (1).
- **Lighting shown on an empty baseplate**: several forum "better lighting" posts present settings with nothing in the scene, which teaches values but not mood; they were left out.

## Sources and licences

Accessed 2026-11-11. All images are third-party and are linked, not stored.

- Roblox Creator Docs images (`Roblox/creator-docs`, commit ccc2b01; documentation CC BY 4.0): outdoor and indoor lighting tutorials, The Mystery of Duvall Drive.
- DevForum threads (Discourse JSON API): 709866, 4727106, 4880290 (images viewed); 2031219, 1510773 (read); 1876371 (opening only, listed as `search`).
- 80.lv articles and images: copyright the named artists and 80 Level. Two rows are search results only.
- Game Developer article on Sable: read as text.
- Sketchfab model: CC BY as stated; listed to look at only.
- Rejected after viewing: baseplate screenshots of lighting panels, colour-grading panel screenshots, a material graph, a sculpt close-up, an editor capture that duplicated row 22, and one mood board whose images could not be told from generated ones.
