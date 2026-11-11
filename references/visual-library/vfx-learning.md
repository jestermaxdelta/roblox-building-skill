# VFX learning library: tutorials, courses, tools and texture sources

What this is: 49 checked references for learning to make stylised effects and for tooling a Roblox VFX pipeline: principle courses and talks, texture techniques, official Roblox pages and staff posts, community tutorials and workflows, plugins and libraries with the licence that was read, and texture sources. The rules they support live in `references/vfx-and-juice.md`; builds are in `references/vfx-recipes.md`; reference images are in `vfx.md`.

How to use this file:
- Beginners: rows 1–3, then 20–23. Intermediate: rows 4–8 and 12–15, then build a recipe. Experts: rows 9–10 and the staff posts 26–29 before changing a pipeline.
- Evidence: `read` = the page, thread, README or licence file was read; `oembed` = the video exists with that title and creator, it was not watched, and the note comes from its title or the page that led to it; `search` = not opened. `[VS]` = depends on an API or feature that can change.
- These are references to study, not assets to copy. Tool rows state the licence that was read, or say "licence not verified". House rule 1 applies to anything a pack or plugin library contains: effect **meshes** that ship are modelled in Blender for the game; textures from a pack need a licence you have read; nothing AI-generated ships. Accessed 2026-11-11.

Thread links are `https://realtimevfx.com/t/<id>` and `https://devforum.roblox.com/t/<id>`.

## 1. Principles, courses and breakdowns

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Artistic Principles of VFX](https://www.youtube.com/playlist?list=PLQD_sA-R5qVKVYw3EVuRT7fSJsVukLEhD) (5 videos), Jason Keyser / VFX Apprentice, 2018; [thread](https://realtimevfx.com/t/4081) (21k views) | video | Gameplay, shape, value, colour and timing through League of Legends; made from the GDC 2017 talk with Hadidjah Chamberlain and built to be re-watched. Replies single out the timing video | oembed; read |
| 2 | [So You Wanna Make Games?? Episode 7: Game VFX](https://www.youtube.com/watch?v=3QKK2o5rWSQ), Riot Games; [page](https://www.riotgames.com/en/artedu/visual-effects) | video | Riot's framing: VFX artists "carry the heavy burden of restraint" so players can tell what is happening. The page recommends row 11 and the forum in row 3 | oembed; read |
| 3 | [Getting Started in Real Time VFX? Start Here!](https://realtimevfx.com/t/3415), Travis, 2018 (209 likes, 154k views) | tutorial | The community's own curriculum: tools of the trade, a learning order, and where the stylised (League-like) resources are | read |
| 4 | [Constructing VFX Worthy of League of Legends](https://80.lv/articles/constructing-vfx-worthy-of-league-of-legends/), Kevin Leroy, 2017 | breakdown | A projectile is cast + projectile + hit. The hot point must sit on the collision box; a shadow behind a glow gives it room (background 0.5 → 0.2 leaves 0.8 of glow); the hit frame is about 0.1 s; textures stay black and white so colour is set per particle | read |
| 5 | [Official VFX Sketch #22: Grayscale](https://realtimevfx.com/t/8473), Niels, 2019 | tutorial | An exercise to copy: pick one common effect (muzzle flash, portal, slash, hit impact…), make seven rough greyscale variations as different as possible, finish one | read |
| 6 | [On Asking for Feedback](https://realtimevfx.com/t/7159), Chris, 2019 | tutorial | Vague questions get vague answers: give context (platform, reference, limits), ask pointed questions, make no excuses | read |
| 7 | [GDC 2023 VFX Roundtable Discussion Notes](https://realtimevfx.com/t/23367), Keith, 2023 | breakdown | Art direction notes: a style guide as the source of truth, paint-overs to turn words into shapes, start every effect coarse and take it into the game before adding detail; a list of free 2D animation tools (Krita, OpenToonz, Aseprite) | read |
| 8 | [Particle Gradient Mapping](https://realtimevfx.com/t/1952), Tobias Noller, 2017 (26k views); [article](https://tobiasnoller.com/articles/ue4-gradient-mapping-vfx/) | breakdown | One greyscale texture recoloured through a gradient: more colour variation, less memory. Roblox has no equivalent, which is why `vfx-and-juice.md` §5 builds the ramp from layers | read |
| 9 | [What is your Alpha/Opacity Mask/Clip/Erode workflow?](https://realtimevfx.com/t/7705), boorch and replies, 2019 (258 topic likes) | breakdown | How dissolves work elsewhere: a threshold moved through a painted greyscale ramp, remapped like Photoshop Levels; ramps painted without pure white or black to leave headroom. On Roblox: bake the stages | read |
| 10 | [Stylized VFX in RiME](https://simonschreibt.de/gat/stylized-vfx-in-rime/), Simon Trümpler | breakdown | Talk page (video not watched) with written updates: the fire material graph, how to sharpen a linear fade, and a note on lit smoke that erodes instead of fading | read |
| 11 | *Elemental Magic* (book), Joseph Gilland | tutorial | Hand-drawn effects animation: how fire, water and smoke move as shapes. Recommended by Riot's VFX team on the page in row 2 | search |
| 12 | [VFX noob: texture creation techniques](https://realtimevfx.com/t/18906), 2022, reply by Simon Trümpler; with [How do you make textures?](https://realtimevfx.com/t/11732), 2020 | tutorial | Five ways to get a texture (packs, painting, photo bashing, procedural tools, simulation): start with the first three. Krita's wrap-around mode (W) makes a tiling smoke texture in minutes | read |
| 13 | [Technical Artist Bootcamp: The VFX of Diablo](https://www.youtube.com/watch?v=YPy2hytwDLM), GDC | video | The talk Trümpler's page says to "watch now", and the one the smoke thread cites at 24:30 for smoke built in the shader | oembed |
| 14 | [VFX Academy: Principles of Color](https://www.youtube.com/watch?v=cB1SlvVyqNE), Plebarae, 2025; [DevForum post](https://devforum.roblox.com/t/3894223) | video | A Roblox VFX artist's colour lesson; the channel teaches Studio, After Effects and Photoshop for Roblox effects | oembed; read |

## 2. Game feel talks

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 15 | [Juice it or lose it](https://www.youtube.com/watch?v=Fy0aCDmgnxg), Martin Jonasson and Petri Purho | video | The classic demonstration of adding feedback layer by layer to a plain game; pair it with the cost ladder in `vfx-and-juice.md` §13 | oembed |
| 16 | [The art of screenshake](https://www.youtube.com/watch?v=AJdEqssNZ-U), Jan Willem Nijman (Vlambeer), 2013 | video | Many small feel changes to one shooter; use the comfort rules in `vfx-and-juice.md` §12 as the counterweight | oembed |
| 17 | [Secrets of Game Feel and Juice](https://www.youtube.com/watch?v=216_5nu4aVQ), Game Maker's Toolkit | video | A short overview to share with non-artists on the team | oembed |

Camera-shake modules and "Juicing Your Cameras With Math" are in `cutscenes-and-cameras.md` (rows 31, 32, 57); the 12 principles of animation are in `animation.md`; spring libraries (spr, Ripple) are in `references/ui-motion-and-feedback.md` §6.

## 3. Roblox: official pages and staff posts

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 18 | [Particle emitters](https://create.roblox.com/docs/effects/particle-emitters), Roblox docs | tutorial | Every property with images: shape, squash, orientation, flipbooks; the mobile rate cap (100/s), the 20 s lifetime cap, the flipbook memory warning | read |
| 19 | [Beams](https://create.roblox.com/docs/effects/beams) and [Trails](https://create.roblox.com/docs/effects/trails), Roblox docs | tutorial | Curve control points, texture modes, segments; the advice to check both ends of Editor Quality Level | read |
| 20 | [Create explosions with VFX](https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/use-particles-for-explosions), Roblox docs | tutorial | A burst with numbers: Drag 10, Lifetime 0.2–0.6, Speed 20–40, SpreadAngle 180, emitter disabled and fired with `Emit` | read |
| 21 | [Create volcanoes](https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/create-volcanoes), Roblox docs | tutorial | Full property lists for ripples, embers, flipbook lava splashes, a three-beam lava flow and a smoke plume, plus the lighting and bloom around them | read |
| 22 | [Create waterfalls](https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/create-waterfalls), Roblox docs | tutorial | Beams for the cascade (`TextureSpeed`, `TextureLength`, Wrap) and five particle layers: splashes, white water, foam, mist | read |
| 23 | [Create laser beams with VFX](https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/laser-traps-with-beams), Roblox docs | tutorial | A beam between two attachments with an invisible collision box for the hit. It starts from a Creator Store blaster model: use your own Blender model instead | read |
| 24 | [Textures and decals: animate textures](https://create.roblox.com/docs/parts/textures-decals), Roblox docs | tutorial | The documented scrolling method: tween `OffsetStudsU`/`OffsetStudsV` and `StudsPerTile` on `Texture` instances; the sample layers two fog textures | read |
| 25 | [SurfaceAppearance](https://create.roblox.com/docs/art/modeling/surface-appearance), Roblox docs | tutorial | Alpha modes (Overlay, Transparency, Tint mask), colour tint and the emissive mask, strength and tint for glowing meshes `[VS]` | read |
| 26 | [Particles' Flipbook Release](https://devforum.roblox.com/t/2029388), Roblox staff, 2022 (357 likes) | tutorial | Flipbook texture sizes from 8² to 1024², the enum rename to `Grid2x2/4x4/8x8`, border clipping fix | read |
| 27 | [New Procedural Particle Emitter Shapes](https://devforum.roblox.com/t/1517642), JaapSuter (Roblox), 2021 (405 likes) | tutorial | `Shape`, `ShapeStyle`, `ShapeInOut`, `ShapePartial` explained by the engineer: cones from cylinders, rings from discs, inward emission | read |
| 28 | [Hiding Avatar Particle Effects in First-Person](https://devforum.roblox.com/t/3136706), TheGamer101 (Roblox), 2024 (183 likes) | tutorial | Emitters, beams and trails parented in a character are hidden in first person; the post shows the welded helper-part workaround `[VS]` | read |
| 29 | [Scrollable textures for MeshParts](https://devforum.roblox.com/t/2820890) (feature request), Zomebody, 2024 | breakdown | Every current workaround and its limit in one post: SurfaceGui, Beam, texture swapping, `Texture` offsets, `EditableMesh:SetUV` | read |

Staff posts on custom flipbook layouts and on quality levels are rows 46 and 51 of `vfx.md`.

## 4. Roblox: community tutorials and workflows

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 30 | [Full Beginner's Guide on scripting Anime/Fighting VFX, part 1](https://devforum.roblox.com/t/1610853), SushiScripter, 2022 (380 likes, 82k views) | tutorial | The most-liked VFX scripting tutorial: input, remote, debounce, damage, then spawning. It shows a server-sided version as "easy, but not recommended"; build the client-replicated one | read (opening) |
| 31 | [Client Replication 101](https://devforum.roblox.com/t/1789487), j_adsa, 2022 (107 likes) | tutorial | Why server-side effects raise ping, with diagrams. It uses `FireAllClients`; `vfx-and-juice.md` §10 narrows that to nearby players and skips the caster | read |
| 32 | [VFX Tutorial: create your own VFX through Blender](https://devforum.roblox.com/t/872437), Drakoliann, 2020 (273 likes, 70k views) | tutorial | A broken wind-ring mesh from a cylinder and a modifier stack: vertex weights masked by a clouds texture, Mask, Smooth, Simple Deform 360° | read |
| 33 | [Stoic Bomb VFX Recreation and Personal Workflow Overview](https://devforum.roblox.com/t/3608056), pewpewagent, 2025 | breakdown | A working Roblox VFX artist's pipeline: one VFX part welded to the root with a `Motor6D` and animated like a limb, an `EmitCount` attribute per emitter, animation events calling functions from a table | read |
| 34 | [Physics-based VFX: Creation Overview Part 2](https://devforum.roblox.com/t/3617845), pewpewagent, 2025 | breakdown | Orbiting debris from sine and cosine with a phase per piece; attributes as the tuning surface so one ability scales from a small attack to a tornado | read |
| 35 | [RUNUP: VFX breakdown part 4](https://devforum.roblox.com/t/3669430), pewpewagent, 2025 | breakdown | Two rigs animated together and exported as a pair; camera keyframes exported and stepped at a fixed 1/60 s with an accumulator so the cutscene is frame-rate independent | read |
| 36 | [How to make inward pulling particles](https://devforum.roblox.com/t/4970318), leoprad2006, 2026 | tutorial | The charge-up emitter in two steps: a sphere part and `ShapeInOut = Inward` | read |
| 37 | [What are Mesh Flipbooks?](https://devforum.roblox.com/t/2656999), 2023 | tutorial | The answer in one line: a script cycling a mesh's textures or mesh ids; there is no engine feature | read |

## 5. Tools, plugins and libraries

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 38 | [VFX Editor](https://github.com/VirtualButFake/vfx-editor), VirtualButFake, 2024; MIT; [thread](https://devforum.roblox.com/t/3103467) (123 likes) | tool | A properties-window replacement for effects: number-sequence editor with easing styles and Béziers, colour-sequence editor, texture store with flipbook support, undo | read |
| 39 | [Effect Designer Suite](https://github.com/MiaGobble/Effect-Design-Suite), iGottic, 2026; GPL-3.0 (plugin code); [thread](https://devforum.roblox.com/t/4754553) | tool | Emit count, delay and duration as attributes shared with other plugins; colour sequences interpolated in Oklab; a curve editor. Its library of about 7,000 preset textures is of mixed origin: check each before shipping | read |
| 40 | [Arc: a VFX animation plugin](https://devforum.roblox.com/t/4903133), sevenIIl, 2026; free on the Creator Store; licence not verified | tool | A timeline for effects: keyframes on parts, attachments and emitters, emit keyframes that scrub, named events, export to one ModuleScript with `Start()` and `Cancel()` | read |
| 41 | [Beziers: modular VFX plugin](https://devforum.roblox.com/t/4180222), coroutine_yieId, 2025 (123 likes); licence not verified | tool | `EmitRepeat` attributes, enable and disable with tween-in for held abilities, add-ons for impact frames, shake and mesh VFX. Its 10,000-asset library includes meshes: study only | read |
| 42 | [VFX Forge](https://devforum.roblox.com/t/3867553), zilibobi, 2025 (114 likes); [docs](https://docs.zilibobi.dev/vfx-forge); licence not verified | tool | Mesh VFX and beam flipbooks, path preview for Béziers and lightning, retime and recolour, texture preloading to stop first-play flicker | read |
| 43 | [Lumina](https://github.com/Mqxsyy/Lumina), Mqxsyy; MIT | repo | A node-based custom particle system; its README says not to use it in production. Read it to see what scripted particles involve before choosing engine emitters | read |
| 44 | [Open-Source Mesh Flipbook Pack](https://devforum.roblox.com/t/3635032), pewpewagent, 2025; no licence text | repo | A small module that loops separate textures on a mesh, with shockwave and dissolve examples. Study the module; the meshes are third-party | read |
| 45 | [Easing Functions Cheat Sheet](https://easings.net/) | tool | Every easing curve drawn; pick the curve by shape before typing a style name | read |
| 46 | [EmberGen](https://jangafx.com/software/embergen/), JangaFX; commercial | tool | Real-time fluid simulation exported as flipbooks; the tool three forum threads name for realistic smoke and fire | read (site) |
| 47 | [EffectTextureMaker](https://mebiusbox.github.io/contents/EffectTextureMaker/), mebiusbox; licence not stated on the page | tool | A browser generator for flares, rings, noise and sparks, useful for block-in textures; verify terms before shipping its output | read (page) |

## 6. Texture sources with licences

| # | Reference | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 48 | [Particle Pack](https://kenney.nl/assets/particle-pack), Kenney, 2018; CC0 (stated on the page) | gallery | 80 sprites at 512²: flares, smoke, sparks, slashes, magic circles. A legitimate block-in kit | read |
| 49 | [Textures for Particles, Visual Effects, Lights and Lensflares](https://github.com/RPicster/Godot-particle-and-vfx-textures), RPicster; CC0 (LICENSE file) | repo | Textures at 1024², 256² and 64² in black-and-white and alpha versions, with the Blender files that rendered them: a worked example of generating soft textures in Blender | read |

## Sources and licences

- Licences read on 2026-11-11: MIT for rows 38 and 43 (LICENSE files); GPL-3.0 for row 39; CC0 for rows 48 and 49. Rows marked "licence not verified" had no licence text on the page read. A licence on a plugin covers its code, not every asset in its library.
- Roblox documentation is CC BY 4.0 (https://github.com/Roblox/creator-docs, commit 7cbffff). Forum posts belong to their authors.
- Videos were verified through YouTube oEmbed (title and channel) and were not watched; notes on them come from the linking page.
- Not reachable: vfxapprentice.com (403: its blog summaries of the Riot style guide and its courses were seen only in search results), the Riot VFX style guide PDF (2017 links redirect to the League home page), artstation.com, reddit.com.
- Thin spots: no Reddit thread with concrete Roblox VFX numbers was found; DevForum critique threads on effects are short, so the critique method in `vfx-and-juice.md` §16 leans on realtimevfx.com.
