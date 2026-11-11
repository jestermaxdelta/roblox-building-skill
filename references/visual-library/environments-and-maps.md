# Environments and maps reference library

What this is: 81 checked references for stylised and low-poly environments that suit Roblox: towns, lobbies and hubs, biomes, interiors, obby and arena layouts, the boards, thumbnails and kits behind them, and captures of the top genres (tycoon, simulator, obby, horror, roleplay, fishing, survival) with their default looks marked. The rules they support live in `references/art-direction-and-quality-bar.md` (slop tells, reference boards, review tests) and `references/level-design-worldbuilding.md` (layout, composition, kits).

How to use this file:
- Pick the kind of space you are building, open three rows (include one marked Weak or Mixed), and write down one decision from each (focal point, palette, value split, kit size) before blocking out. Shrink each image to 320 px wide first: what survives is the lesson.
- Evidence: `viewed` = the image was downloaded and looked at; `read` = the page or thread was read; `oembed` = the video exists with that title and creator and was not watched; `search` = seen in search results only, not opened.
- These are references to study, not assets to copy: every third-party image and model stays its owner's, and house rule 1 means everything shipped is our own Blender work. Open-licence rows give the licence so a kit can be opened and measured, never imported.

Image host prefixes: `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads/original`, `LV` = `https://cdn.80.lv/api/upload/content`, `DOCS` = `https://prod.docsiteassets.roblox.com/assets`. `t/<id>` = `https://devforum.roblox.com/t/<id>`. `RBX <id>` = a Roblox image asset (official game thumbnail): request `https://thumbnails.roblox.com/v1/assets?assetIds=<id>&size=768x432&format=Png` and open the `imageUrl` it returns (that URL expires; the id does not, but developers replace thumbnails). Sketchfab rows link the model page; its preview is at `https://api.sketchfab.com/v3/models/<uid>` under `thumbnails`.

## A. Towns, villages and streets

Start here: 1, 6, 11.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Map Design and Scene Building: before and after](https://devforum.roblox.com/t/709866), Ahlvie, 2020 · `DF/4X/e/6/8/e68db8b0e88fe9346c996bf879a7138a758ad9d5.png` (PNG, 3.2 MB) | image | One town twice. Left: flat ground, houses dropped on a plane, even light. Right: stepped heights, a framed street, foliage masses, warm lamps. The buildings barely changed; the composition did | viewed |
| 2 | Same thread, gatehouse · `DF/4X/a/6/e/a6e1a39cc674364c0026a1d214d6764bb78b079a.jpeg` (JPEG, 1.2 MB) | image | A threshold: dark gate frame, bright town through the arch, cart and pines as secondary shapes at the edges, path leading in | viewed |
| 3 | Same thread, lantern path · `DF/4X/c/9/e/c9eb37436e6604c3f1b46d6e937ddca925a6b7d9.jpeg` (JPEG, 1.1 MB) | image | Lantern posts repeat along the path as a leading line to the lit house; ground haze turns the far posts into clean dark shapes | viewed |
| 4 | Same thread, prop group · `DF/4X/f/6/f/f6fa4cd43b1e65a73c63c763009d10685ea58498.jpeg` | image | One story group against a wall: two crates, a lantern on top, a rock, a fern; one tall, two medium, several small, with grass hiding the seam | viewed |
| 5 | Same thread, text | tutorial | Order of work: stylisation, layout, sculpting, scene building, lighting, details. Placeholder blocks at true scale before any asset; a small unified palette with rare vivid accents. It uses Roblox Terrain, which needs the owner's approval here | read |
| 6 | [Medieval Market](https://80.lv/articles/medieval-market-a-detailed-guide-on-stylized-environment-art-in-unreal-engine), Kristina Nakić, 2025 · `LV/d0/6851556c5af06.jpg` | breakdown | One hero (the church tower) on the centre axis; bunting and both roof rows converge on it; stalls dress the edges and the middle stays clear; warm roofs against one blue sky | viewed |
| 7 | Same article, timber kit · `LV/e1/6851561f7f266.jpg` | image | Beams, braces, posts and two doors laid out before assembly: a timber-frame town is about ten pieces | viewed |
| 8 | [Modular Lowpoly Medieval Environment](https://sketchfab.com/models/5bf0a1562b7e401e9e6d7758ec54d09c), Satendra Saraswat, 2022, CC BY | image | A street from one kit: two roof colours alternate, timber frames are thick enough to read small, a tower closes the view. 560k faces as posted: study layout, not budget | viewed |
| 9 | [Lisbon Streets](https://80.lv/articles/lisbon-streets-creating-a-futuristic-scene-in-the-overwatch-style), Georg Klein, 2020 · `LV/fa/5f98043aa2f18.jpg` | breakdown | The reference board: photos of the real city (trams, facades, hills) beside shots in the target style, so the scene translates a place instead of copying a game | viewed |
| 10 | [Nordic Village](https://80.lv/articles/building-a-game-ready-nordic-village-scene-with-day-night-lighting-setups), Danylo Kyslenko, 2026 · `LV/28/6ada70d14aa77.jpeg` | breakdown | V-shaped composition: two house rows frame a bright gap of sea and mist; one red building is the accent against greys; turf roofs repeat one material idea. Realistic PBR: take layout and palette only | viewed |
| 11 | [Starter Kit City Builder](https://github.com/KenneyNL/Starter-Kit-City-Builder), Kenney, 2026 commit; code MIT, models CC0 · `https://raw.githubusercontent.com/KenneyNL/Starter-Kit-City-Builder/main/screenshots/screenshot.png` | repo | Palette discipline on a tiny kit: every building shares one roof grey and one base grey and takes exactly one saturated band; roads are the darkest value, grass the lightest | viewed |
| 12 | [KayKit Medieval Hexagon Pack](https://github.com/KayKit-Game-Assets/KayKit-Medieval-Hexagon-Pack-1.0), Kay Lousberg, 2024 commit, CC0 · contents image linked in its README | repo | Three value bands (lime ground, mid-grey rock, dark pines), blue roofs as the only cool accent, the same soft bevel on every piece including rocks | viewed |
| 13 | [Feedback on my game's map](https://devforum.roblox.com/t/3788097), ineedfundsformygame, 2025 · `DF/5X/f/9/4/0/f940fa3e57040922554664ec230bf1fe4b4f4ba6.jpeg` | image | Weak: one blue tint over everything and the same building repeated in visible rows; the top replies ask for variety. Compare rows 8 and 11 | viewed |

## B. Lobbies and hubs

Start here: 14, 23, 24.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 14 | [New Lobby Graphics (PROPHECY)](https://devforum.roblox.com/t/3682295), nowflybird, 2025 · `DF/5X/3/1/2/d/312d0fa904ef48fcdd64e2338fb1bec8beb6cb15.jpeg` | image | A lobby with its own look: two hues only (blue rock, gold blocks), nested triangular portal as the focal point, cyan lights as waymarkers, ropes as leading lines. PBR rock: a small team takes the composition | viewed |
| 15 | [Feedback on simulator map](https://devforum.roblox.com/t/3643516), oFinallyyy, 2025 · `DF/5X/5/a/c/8/5ac89970a78d93a042d46d8fb18f61861cf0f5f4.jpeg` | image | Mixed: a tidy hub ring (fountain centre, shop and sell on the rim, cliffs closing the view) in the look of many simulators. Nothing says which game it is | viewed |
| 16 | [Low poly-styled simulator lobby](https://devforum.roblox.com/t/683143), Official_Darcloud, 2020 · `DF/4X/3/3/6/3363c552d197842c4ba6d7005fa433246b6f39a2.png` | image | Weak: the 2020 template in one frame: orange cliffs with green caps, checker ground, floating extruded text. Built "in the style of" one studio, which is why it resembles a hundred others | viewed |
| 17 | [I need some feedback on this lobby map](https://devforum.roblox.com/t/4068529), CaydenIs3D, 2025 · `DF/5X/9/2/f/b/92fbbc95bf7087822f60ec0cb93f46ad1338fee4.jpeg` | image | Weak: a slab floating in the default sky, pixel-font signs, grey spikes as backdrop. Sign, shop and ground share no rule; reviewers call it small and dull | viewed |
| 18 | [Feedback on my game's lobby](https://devforum.roblox.com/t/3644614), LumoseerGaming, 2025 · `DF/5X/1/1/a/2/11a26e692dee29762d97fb4e342e2ed08d08f162.jpeg` | image | Weak: cube trees and flat grey ground beside one detailed timber house: two detail levels in one view | viewed |
| 19 | [How would you rate my Simulator Lobby](https://devforum.roblox.com/t/1891111), TweetyBuilds, 2022 · `DF/4X/4/a/4/4a45f9bc6fa247eac1f0946e2bdef181d45ad39f.jpeg` | image | Weak: pure cyan, blue and yellow at full saturation; reviewers say the "random colors" do not fit. A phone capture, which is how players see it | viewed |
| 20 | [Luxurious Resort on Tropical Island](https://devforum.roblox.com/t/293803), nineteen85, 2019 · `DF/5X/2/2/f/4/22f49c4c148b92b946c9c0b2922f06700a606cd9.png` (PNG, 1.4 MB) | image | Mixed: a two-hue world (sand, cyan) with palms and umbrellas as the only accents and arches repeating around the pool. Bloom is far past safe range: sky and floor burn out | viewed |
| 21 | Same thread, aerial · `DF/5X/f/c/3/3/fc33bcdb110ddd84ba4bb8c1f91d5a8ab8bf0d9b.png` (PNG, 2.2 MB) | image | Dome repetition and a symmetric plan make a large hub readable from above; hedge maze and pools mark districts | viewed |
| 22 | Same thread, palm path · `DF/5X/3/a/6/5/3a655b898debe43f00c635e4562d977dfb7f23ec.jpeg` (JPEG, 1.7 MB) | image | Trunks as a foreground frame, one saturated umbrella at the end of the path as the pull | viewed |
| 23 | [Beyond the Dark: building architecture](https://create.roblox.com/docs/resources/beyond-the-dark/building-architecture), Roblox · `DOCS/resources/beyond-the-dark/building-architecture/Architecture-Overview.jpeg` | image | A dark hub lit by its content: a black-hole landmark through the roof, teal, magenta and amber signs marking districts, a white centrepiece below | viewed |
| 24 | Same page, greybox · `DOCS/resources/beyond-the-dark/building-architecture/Architecture_Example_1.jpeg` | image | Greybox with emissive colour blocks standing in for districts: the lighting and wayfinding plan is tested before any art exists | viewed |

## C. Biomes, nature and landmarks

Start here: 25, 28, 29.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 25 | [Creating Visual Interest in Low Poly Artworks](https://80.lv/articles/creating-visual-interest-in-low-poly-artworks), Stanley Barrett, 2019 · `LV/a7/5d6407c54431e.jpg` | breakdown | A low-poly island arena: cool shadow tint over most of the scene, one warm sunlit patch on the floor pattern pulls the eye; tilted pillars break the grid | viewed |
| 26 | Same article, wireframe · `LV/e1/5d6407cdc7cc6.jpg` | image | Where the triangles went: big planes for floor and pillars, density only in the tree and the spiral; flagstones are separate tilted slabs | viewed |
| 27 | Same article, trees · `LV/56/5d6407d27dd84.jpg` | image | Two canopy trees at 1,658 and 1,874 triangles from clustered blobs: inside this skill's tree budget | viewed |
| 28 | [Stylized Production: Tips and Tricks](https://80.lv/articles/stylized-production-tips-and-tricks), Benjamin Lucas, 2017 · `LV/2b/5d2c957d5e158.jpg` | breakdown | A beach: saturated, detailed foreground corner; everything else fades into two flat bands through haze. Depth from value, not geometry | viewed |
| 29 | Same article, kit · `LV/54/5d2c957867cb4.jpg` | image | A whole island town from three trees, three rocks and six buildings, rotated and recoloured (three days of work, per the text) | viewed |
| 30 | [Simple Stylized Environment: Scale and Mood](https://80.lv/articles/simple-stylized-environment-scale-and-mood), Sebastian Vomvas, 2018 · `LV/a1/5d2c51c4cd073.jpg` | breakdown | Scale sold by repetition (rows of balconies count the floors), a dark mass against a bright sky, fog at the base | viewed |
| 31 | [Breakdown: Simple Stylized Scene in Unity](https://80.lv/articles/breakdown-simple-stylized-scene-in-unity), 80 Level, 2019 · `LV/0e/5daeb0a77e8e2.jpg` | breakdown | The silhouette test applied to a scene: lighthouse, two umbrella pines and rocks as one white shape; the hero is the only vertical | viewed |
| 32 | [Small Low poly Showcase Map](https://devforum.roblox.com/t/1046975), SolarThresh, 2021 · `DF/4X/f/1/5/f1566e025f4ae7eb2580a85d41764473d45fd559.png` | image | Mixed: consistent facets and a held warm palette, but ground, rocks and trees share one value, so in greyscale it is a single band; two cacti are the only relief | viewed |
| 33 | [Low-Polying Tutorial for Beginners](https://devforum.roblox.com/t/235354), Pyrotenics, 2019 · `DF/5X/d/2/5/4/d25401b8bfdec68336f7988b49c504cf7aa3794d.png` | image | Weak: the stock low-poly look: blob canopies with one facet size, lime ground at full saturation, no value plan. Use it as the "too generic" marker on a board | viewed |
| 34 | [Halloween Low-Poly Map](https://devforum.roblox.com/t/1497479), Bloxquility, 2021 · `DF/4X/e/2/4/e24941f238b54a2b4056c5d395c9a997631bd717.jpeg` | image | Mixed: a strict three-hue palette (purple, orange, green) gives identity; everything is glossy, saturated and glowing at once, so nothing leads | viewed |
| 35 | [Ultimate Guide to Stylized Trees](https://devforum.roblox.com/t/1124673), Tradesmark, 2021 · `DF/4X/0/e/a/0ea39faba968de13f934416ff9e53bdca7388675.png` | tutorial | Branch skeleton first, canopy second; one tree in three colourways. The canopies are alpha leaf cards, which this skill's tree recipe avoids: study the branch structure | viewed |
| 36 | [Ancient Ruins](https://sketchfab.com/models/105c85f4668245208fe71cac4861cf8c), Maksim Batyrev, 2021, CC BY | image | A ruin kit as a sheet: three rune stones in a size ladder, one tall sword pillar, arch fragments, grass tufts; 2,090 faces for the lot | viewed |
| 37 | [Lowpoly Environment Design Tricks](https://80.lv/articles/emek-can-ozben-low-poly-environment), Emek Can Özben, 2016 | breakdown | Method: about twenty objects, then a critique of the whole, one or two iterations, then hold the style; focus points made by contrast against similarity | read |
| 38 | [Simple Stylized Approach to Environments](https://80.lv/articles/simple-stylized-approach-to-environments), Tobias Koepp, 2017 | breakdown | Sculpt only large forms: at camera distance small detail reads as noise; accent colours (blue paint, green plants) separate architecture from same-coloured sand | read |

## D. Interiors

Start here: 39, 41, 44.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 39 | [Modular Approach to Stylized Environments](https://80.lv/articles/001agt-002mrs-crafting-a-low-poly-model-kit), Rodrigo Gonçalves, 2019 · `LV/a1/5d28760750e79.jpg` | breakdown | A two-room cutaway from the front, three-quarter and top: a warm lamp pool marks each seating group, red armchairs and a green fridge are the only saturated objects, the floor material changes at the room boundary | viewed |
| 40 | Same article, atlas · `LV/ca/5d28760a1407c.jpg` | image | The whole interior kit on one texture sheet: one atlas, one material | viewed |
| 41 | [Wes Anderson-Inspired Internet Café](https://80.lv/articles/creating-wes-anderson-inspired-internet-caf-game-environment), Elisa Passera, 2025 · `LV/ad/68414f7b9286e.jpg` | breakdown | One-point symmetry; a teal and orange pair held across walls, floor, furniture and lights; window light lands as two patches and leaves the rest calm | viewed |
| 42 | [Working on Stylized Interior](https://80.lv/articles/working-on-stylized-interior-silhouettes-materials-lighting), Alex Engelmann, 2020 · `LV/29/5e6760e896e57.jpg` | breakdown | A blockout kit with every proxy named (`SM_proxy_…`) before art: the list is the asset plan | viewed |
| 43 | [Resto ni Teo](https://sketchfab.com/models/2c587738161e43708b4d99210c57c9cc), LowPolyBoy, 2023, CC BY | image | Restaurant: wood as the base, magenta seats as the accent, hanging menu boards as the overhead landmark, glowing windows as fill. 151k faces as posted | viewed |
| 44 | [The Mystery of Duvall Drive: construct the house](https://create.roblox.com/docs/resources/the-mystery-of-duvall-drive/construct-the-house), Roblox · `DOCS/resources/mystery-of-duvall-drive/constructing-the-house/gray-boxed-versions.jpeg` and `…/final-content-versions.jpeg` | image | One furniture family lined up as greybox and again as final art in an "asset zoo": review a family together, never piece by piece | viewed |
| 45 | Same page, early version · `DOCS/resources/mystery-of-duvall-drive/constructing-the-house/earliest-version-toolbox-house.png` | image | Roblox's own team blocked out with a Toolbox house and then replaced it: placeholders belong to throwaway stages only | viewed |
| 46 | [Ruski's Tutorial #2: how to design a simple house](https://devforum.roblox.com/t/330237), Trustmeimrussian, 2019 · `DF/4X/8/e/6/8e606879921da8cae8ff3a0b33f047a9bad1a809.png` | tutorial | Floor plan, walls, roof, porch: the order is right. Built from Parts with stock materials, so the result is plain: keep the sequence, model in Blender | viewed |
| 47 | [Creating a Stylized Witch Hut Interior](https://80.lv/articles/creating-a-stylized-witch-hut-interior-in-ue4), Angelo Tsiflas, 2020 · `LV/9a/5f96a26df28cd.jpg` | breakdown | A per-asset board: the concept in the middle and a labelled row of real photos for every prop and surface (ceiling, floorboard, pump, garlic) | viewed |

## E. Obby, arena and track layouts

Start here: 48, 52, 53.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 48 | [Starter Kit 3D Platformer](https://github.com/KenneyNL/Starter-Kit-3D-Platformer), Kenney, 2026 commit; code MIT, models CC0 · `https://raw.githubusercontent.com/KenneyNL/Starter-Kit-3D-Platformer/main/screenshots/screenshot.png` | repo | Obby readability: each platform has a dark top and a thick bright rim, so the landing edge is the highest-contrast line on screen; the pastel sky stays below the platforms in saturation | viewed |
| 49 | [Starter Kit Racing](https://github.com/KenneyNL/Starter-Kit-Racing), Kenney, 2026 commit; code MIT, models CC0 · `https://raw.githubusercontent.com/KenneyNL/Starter-Kit-Racing/main/screenshots/screenshot.png` | repo | Track edges as red and white kerbs, a bright arch as the gate landmark, a yellow tent as the pit marker; layered cone pines are one mesh idea repeated | viewed |
| 50 | [Level Design Workshop: Blockmesh and Lighting Tips](https://www.youtube.com/watch?v=09r1B9cVEQY), GDC | video | Not watched here. A talk on what a blockout must already prove and on steering players with light; watch it beside `level-design-worldbuilding.md` §5 and §8 and note where the two disagree | oembed |
| 51 | [Ruski's Tutorial #1: how to design a map layout](https://devforum.roblox.com/t/277853), Trustmeimrussian, 2019 | tutorial | The questions answered before opening Studio: genre, theme, server size, detail level and the map's overall shape (a horseshoe shows the objective but makes players go round; a circle returns them to the start). Then a small worked map | read |
| 52 | [Ruski's Tutorial #3: how to design a PvP map](https://devforum.roblox.com/t/2746055), Trustmeimrussian, 2023 | tutorial | Seven steps in order: a labelled 2D layout on a 400 × 400 plate with three 32-stud lanes and cross alleys, greybox, risk-versus-reward spots, cover props, perimeter, lighting, finish. Rooms get several entrances so nobody can camp. Built from Parts: keep the order, build the kit in Blender | read |
| 53 | [Mad Studio map layout design guidebook](https://devforum.roblox.com/t/1246963), loleris (Mad Studio), 2021 | tutorial | A studio's layout cycle: theme and one map quirk, a flat top-down sketch with spawns and objectives placed exactly, then a minimal 3D sketch. Layout is approved before visuals so two people can do the two jobs | read |

## F. Process: boards, thumbnails and kits

Start here: 54, 56, 57.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 54 | [Develop polished assets](https://create.roblox.com/docs/tutorials/curriculums/environmental-art/develop-polished-assets), Roblox · `DOCS/tutorials/environmental-art-curriculum/Section2/Art-Style.png` (PNG, 3.6 MB) | image | The whole art-style board for a sci-fi arena is five real-world photos (stepped concrete, basalt columns, perforated metal, moss, ferns): shapes and materials taken from the world, not from other games | viewed |
| 55 | Same page, kit · `DOCS/tutorials/environmental-art-curriculum/Section2/DesigningModularKits-ModularKit.jpg` | image | The laser-tag kit: wall, corner, door, ramp-top and trim pieces in two colours (white trim, yellow field) | viewed |
| 56 | [The Drunk Lake Inn](https://80.lv/articles/the-drunk-lake-inn-stylized-environment-breakdown), Ivan Blinov, 2020 · `LV/69/5efc6629e35d7.png` | breakdown | A board in sections (Scene, Props, Light, "Reference with colours palette") with notes written over the concept; the palette was read by pixelating the concept | viewed |
| 57 | [Working on Lighting and Composition for a Night Scene](https://80.lv/articles/working-on-lighting-and-composition-for-a-night-scene), Stephen A. Falk, 2020 · `LV/b2/5e959e735df3d.jpg` | breakdown | Eight pencil thumbnails of one scene before any blockout: composition is chosen on paper | viewed |
| 58 | [Melancholic City at Night](https://80.lv/articles/how-to-build-a-melancholic-environment-of-a-city-at-night-with-blender), Vitaliy Novart, 2026 · `LV/8d/696534f2a9b24.jpg` | breakdown | Mood references (night illustrations, lit alleys) kept apart from structure references (brick tenements, fire escapes) | viewed |
| 59 | [As a builder, how do you plan your builds?](https://devforum.roblox.com/t/187515), AbandonedRick and replies, 2018 | tutorial | 706 likes. Greybox the world first (most-liked reply); always work from reference; subdivide until a piece is small enough to finish well | read |
| 60 | [Environmental Art Design](https://www.youtube.com/watch?v=nwShvDmFHWc) and [Developing Polished Assets](https://www.youtube.com/watch?v=JiXnyF0fbrU), Roblox Documentation | video | Not watched here. The videos embedded in the curriculum behind rows 54 and 55: the same board and kit shown being built | oembed |
| 61 | [The Art of Firewatch (GDC 2015)](https://www.youtube.com/watch?v=ZYnS3kKTcGg), Campo Santo Productions | video | Not watched here. Listed for one question: how a landscape is carried by a few flat colour bands per time of day instead of surface detail | oembed |
| 62 | [Crafting a Tiny Open World: A Short Hike Postmortem](https://www.youtube.com/watch?v=ZW8gWgpptI8), GDC | video | Not watched here. Listed for scope: what one developer chose to build, and to leave out, in a small stylised open world | oembed |

## G. Genre captures: tycoon, simulator, obby, horror, roleplay

Start here: 66, 73, 79; for one genre, open its default marker first (tycoon 63, simulator 70, obby 72, horror 76, roleplay 75), then the rows that broke from it.

The top genres in `market-scan-2026-11.md`, viewed 2026-11-11. Official thumbnails (`RBX`) are promotional renders built from the game's own assets: take palette, assets and lighting from them, not composition. "Default marker" rows show what the genre converges on; `art-direction-and-quality-bar.md` §4 builds its default rows from them, and hex values quoted here were sampled from the images.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 63 | [Creator Spotlight: Ultraw's tycoons](https://devforum.roblox.com/t/3840933), Roblox, 2025 · `DF/5X/6/b/b/c/6bbcf85bfd172e81a9ebdccc71d6604bb89654d4.png` (PNG, 2.6 MB) | image | Default marker, four tycoon generations in one image: a walled flat slab with path strips and Part machines; a dome on bare orange ground; identical lots in a row along a road; real-world brick and white render at noon. The plot-as-slab and the lot row are the tycoon default | viewed |
| 64 | [Restaurant Tycoon 3](https://www.roblox.com/games/119048529960596), Ultraw, official thumbnail · `RBX 107621000669324` | image | Default marker for build-your-own tycoons: a brick-and-timber bistro at dusk, four warm lamps, pines, picket fence. Photo materials at real scale under a golden key, which is what the genre's tiles already show | viewed |
| 65 | [Retail Tycoon 2](https://www.roblox.com/games/5865858426), official in-game screenshot · `RBX 7105520921` | image | A tycoon interior from the build camera: dark floor as the lowest value, white walls, orange shelving as the one structure colour, produce as the saturated layer, a green placement highlight | viewed |
| 66 | [Run A Farm!](https://www.roblox.com/games/79496881832552), official thumbnail · `RBX 93209235075406` | image | Both plot states in one frame: a lone red coop on bare dirt, then the finished farm (crop rows, barn, stalls, fenced paths). What the empty plot must promise; chunky low-poly, red accents on tan and sage | viewed |
| 67 | [LINE UP! Metro Tycoon](https://www.roblox.com/games/76792629643884), official thumbnail · `RBX 131098589865928` | image | Management as a toy diagram: a transit map in five line colours on white, stations as dots. A flat graphic direction carrying a cozy-management hit | viewed |
| 68 | Same post as 63, garden · `DF/5X/5/4/9/7/5497cde9fe1c61b0d05cd09202c83a539477a3b3.jpeg` | image | A pastel garden inside the tycoon map: faceted grey rocks, round peach and lilac canopies, fairy lights, a cyan pond. A non-realistic corner beside row 64's realism | viewed |
| 69 | [Creator Spotlight: HDFrisk and The Gang](https://devforum.roblox.com/t/3419750), Roblox, 2025 · `DF/5X/b/4/2/a/b42a8dce07da5b2469e129c1d0ef49727c0bd676.jpeg` | image | Simulator default, in game: a training room with a deep red floor, faceted slate rocks, a volcano centrepiece, saturated pets in front, a floating counter | viewed |
| 70 | [Steal a Brainrot](https://www.roblox.com/games/109983668079237), official thumbnail · `RBX 126549264012376` | image | Default marker for steal-a: a stacked red box base with a name board, flat green grass, pale sky, voxel collectables; red #D85846, green #3BD776, sky #CFF7E4, all above value 80 | viewed |
| 71 | [Grow a Garden](https://www.roblox.com/games/126884695634066), official thumbnail · `RBX 140220498115065` | image | A plot as rows on a studded surface: brown strips, chunky fence posts, voxel fruit, green #71F96A at value 98. Retro studs as a choice, now a default of its own | viewed |
| 72 | [Tower of Hell](https://www.roblox.com/games/1962086868), official thumbnail · `RBX 133636978559560` | image | Default marker for obby: looking up the tower, each section one saturated hue family (orange, green, pink) on grey, so players know where they are | viewed |
| 73 | [Creator Spotlight: xJa_ys on Bayside High](https://devforum.roblox.com/t/3579254), Roblox, 2025 · `DF/5X/7/8/3/4/78345a226c687420911895e0e48a68945ceaebdd.jpeg` | image | Roleplay made on purpose: real school architecture made friendlier, white and lavender-grey with blue trims, chunky palms, the school sign as landmark; the text explains blending recognisable architecture with colour | viewed |
| 74 | Same post, rival school · `DF/5X/5/9/c/e/59ce0073cb8bae0d8835e2e1808e0167f59a6a76.jpeg` | image | The same kit recoloured red and white: a family reused by palette swap; parking lines and plaza kept as negative space | viewed |
| 75 | [Brookhaven RP](https://www.roblox.com/games/4924922222), official thumbnail · `RBX 85300103585150` | image | Default marker for roleplay: white suburban mansion (#D8D8D8), grey asphalt, lawn #869B7C, palms, noon | viewed |
| 76 | [DOORS](https://www.roblox.com/games/6516141723), official thumbnail · `RBX 136890620187326` | image | Default marker for horror, done well: a hotel lounge in warm dark wood (value 9–55, saturation 45–68: brown, not black), fireplace and chandelier as the only sources | viewed |
| 77 | [DONT SPLASH](https://www.roblox.com/games/119958473240233), official thumbnail · `RBX 105851805811061` | image | Bright liminal horror: cream tile walls at value 93, saturated cyan water, fluorescent tubes, stepping tiles as the path. The threat lives in a well-lit room | viewed |
| 78 | [Creator Spotlight: Qwelver on Dandy's World](https://devforum.roblox.com/t/3639226), Roblox, 2025 · `DF/5X/a/c/0/4/ac048acdfb7af3e8c0f1e723bc8132e774ee01c4.jpeg` | image | Toon cast in a dark building: a museum hall near black (value 3–35), three floor spots on a skeleton as the focal point, cool ceiling strips; the post's character sheets are saturated flat toons | viewed |
| 79 | [Creator Spotlight: The Inn](https://devforum.roblox.com/t/3659603), Roblox, 2025 · `DF/5X/b/7/1/1/b711ca481e5b9874314ab9ddaaedc593e98076ec.jpeg` | image | One-hue horror: a symmetric inn corridor all in deep reds (value 7–76), floor lanterns and one ceiling lamp, the far door as the destination | viewed |
| 80 | [Creator Spotlight: 99 Nights in the Forest](https://devforum.roblox.com/t/4036940), Roblox, 2025 · `DF/5X/9/a/6/9/9a69c85ac3dc64c96c415cd7c14ed5ea551d592d.jpeg` and `DF/5X/4/b/2/8/4b28d0a217ee0d8f56d646619ecb2d5ca3a7f491.jpeg` | image | Survival-horror default: a grey manor in grey-green fog with blocky trees and graves (saturation under 50); then night, one warm window and pumpkins on dark ground | viewed |
| 81 | [Creator Spotlight: WoozyNate on Fisch](https://devforum.roblox.com/t/3269481), Roblox, 2024 · `DF/5X/5/8/1/5/58153a27b43fc07b5f453693849a16487209bc2d.jpeg` | image | A fishing island as one zone: faceted red and green trees, a lighthouse landmark, piers as the ways out, blue-grey sea haze as the boundary | viewed |

## Patterns seen

- **Composition, not asset quality, separated the strong scenes.** Row 1 is the clearest case: the same buildings read as amateur on a flat plane and as finished once heights step, a street is framed and light picks a focal point.
- **One hero per view on an axis, with lines aimed at it**: church tower and bunting (6), portal and ropes (14), tower at the street end (8), lit house and lantern posts (3).
- **Two or three hues, one accent.** Sand and cyan (20), blue and gold (14), teal and orange (41), grey with one red house (10). Strong scenes could be described in one palette sentence.
- **Shared neutrals make variety safe.** Kenney's buildings share roof and base greys and vary one band (11); the timber town varies two roof colours (8).
- **Value does the depth.** Foreground saturated and dark, distance flat and pale (28, 30, 3); landing edges as the highest contrast (48).
- **Kits are small.** Three trees, three rocks and six buildings made a town (29); about ten timber pieces made a market (7); one atlas held an interior (40).
- **Good boards mix the real world with the target style and are labelled** (9, 47, 54, 56, 58).
- **Process artefacts recur in good work**: paper thumbnails (57), named proxy kits (42), greybox with colour blocks (24), family line-ups (44).
- **Each genre has a visible default** (§G): tycoon lots on a road or a walled slab (63), simulator primaries above value 80 (70), obby one hue per section (72), horror brown-dark or grey fog (76, 80), roleplay white suburb at noon (75). The rows that stand out moved shape, material or light, not only palette (67, 77, 78, 79).

## What the weak examples had in common

- **A template from one source**: the simulator lobby (16), cube trees and stock cliffs (15, 18), the blob-canopy "low poly" look (33). Each could be swapped into another game unnoticed.
- **No focal point and no value plan**: one flat band in greyscale (32), one tint over everything (13), every colour at full saturation (19, 34).
- **Two detail levels in one view** (18) and **stock materials on Part-built geometry** (46).
- **Undesigned edges**: a slab in the default sky (17), a map that "just ends".
- **Effects used as quality**: bloom that burns the sky out (20), gloss and glow on everything (34).
- **Repetition left visible**: one building or one tree copied in rows at one scale and yaw (13, 33).

## Sources and licences

Accessed 2026-11-11. All images are third-party and are linked, not stored.

- Official Creator Spotlight posts (Discourse JSON API; images resolved from short URLs to the upload host): 3840933, 3419750, 3579254, 3639226, 3659603, 4036940, 3269481 (images viewed, post text read, 2026-11-11).
- Official game thumbnails: listed with Roblox's omni-search API, fetched through `thumbnails.roblox.com` (games multiget, then assets by id) and viewed 2026-11-11, for rows 64–67, 70–72 and 75–77.
- DevForum threads (Discourse JSON API; images from the forum's upload host): 709866, 3788097, 3682295, 3643516, 683143, 4068529, 3644614, 1891111, 293803, 1046975, 235354, 1497479, 1124673, 330237, 187515 (viewed or read as marked); 277853, 2746055, 1246963 (opening posts read on 2026-11-11). Posts remain their authors' under the forum's terms.
- Roblox Creator Docs images (`Roblox/creator-docs`): environmental-art curriculum, Beyond the Dark, The Mystery of Duvall Drive. © Roblox; the repository's CC BY 4.0 statement names prose, not images (`assets/reference/ATTRIBUTION.md`), so they are linked only.
- 80.lv articles and their images: copyright the named artists and 80 Level; study only.
- Sketchfab models: licences as stated per row (CC BY). They are listed to look at, and must not be downloaded into a game (house rule 1).
- GitHub kits: KenneyNL starter kits (code MIT, models CC0, README checked), KayKit packs (CC0, `LICENSE.txt` checked). Study only. One KayKit image host request was refused (403), so only one contents image was viewed.
- YouTube rows verified by oEmbed (title and channel); the videos were not watched.
- Link check, 2026-11-11: every URL and image path in the tables answered (sizes above 1 MB are marked; none is animated) (DevForum through the JSON API, GitHub through `git ls-remote`, Sketchfab through its model API, YouTube through oEmbed). A section of ArtStation portfolios and gallery feeds was removed: ArtStation is not reachable from here and none of it had been opened.
- Rejected after viewing: tutorial screenshots of Studio and Blender panels, a meme logo, material-graph screenshots, a realistic character render and one reference board whose sources could not be told from generated images.
