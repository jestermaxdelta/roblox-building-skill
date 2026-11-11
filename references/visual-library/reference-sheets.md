# Bundled reference sheets

22 original annotated diagrams that ship with the skill (`assets/reference/*.png`), plus 30 official Roblox documentation images listed as external references. Use them when a rule is easier to see than to read, when working offline, or to show the developer what "right" looks like before building.

How to use this file:
- Open a sheet with the Read tool on its path relative to the plugin root, for example `assets/reference/01-phone-hud-anatomy.png`. Every sheet is 1600 px wide (2×), under 250 KB, and names the guide sections it supports in its top-right box.
- The guide wins. Sheets are drawn from the guides as read on 2026-11-11 (sheets 16–18 re-rendered that day after the review); if a number on a sheet differs from its guide, follow the guide and rebuild the sheet (`node assets/reference/src/render.js`, sources in `assets/reference/src/`).
- The art on the sheets is illustrative, drawn in a system font and a neutral palette: copy the measurements and the method, never the look. The skill ships no house style.

## 1. UI, HUD and screens

| # | Sheet | Shows | Open it when | Supports |
|---|---|---|---|---|
| 01 | `assets/reference/01-phone-hud-anatomy.png` | Phone-S (800×360) HUD with 12 numbered zones: top bar, safe area, currency, menu block, objective, toast lane, tracker, thumbstick touch area, jump button, primary action, centre third, capacity bar; sizes in px and as H/W fractions | Placing any HUD element; reviewing a phone screenshot for zone violations | `ui-screen-recipes.md` §1, §4; `ui-input-crossplatform.md` §Mobile layout and thumb zones; `ui-design-figma.md` §1 |
| 02 | `assets/reference/02-hud-three-densities.png` | One HUD drawn cluttered, generic and well ordered, five numbered faults or fixes each | Explaining why a HUD "looks free-model" or overloaded; before a HUD redesign | `ui-design-figma.md` §1, §8; `ui-screen-recipes.md` §2, §4 |
| 03 | `assets/reference/03-shop-anatomy.png` | Phone shop window that fits a 360 px tall screen (side category rail, one scrolling card row, fade group) with 11 callouts, desktop arrangement, the buy/claim state machine, house rule 3 on this screen | Building or auditing a shop or any card window | `ui-screen-recipes.md` §1, §3, §5; `monetization-and-policy.md` |
| 04 | `assets/reference/04-inventory-grid-anatomy.png` | Grid with detail pane, eight cell states, rarity ramp in colour and greyscale with Oklab lightness, data rules | Building an inventory, collection or pet grid; choosing rarity colours | `ui-screen-recipes.md` §6; `ui-design-figma.md` §3, §6 |
| 05 | `assets/reference/05-button-anatomy-states.png` | Native chunky-button anatomy and instance tree, the eight states, press and release curve on a ms axis, perception bands | Building the first button component; reviewing missing states | `ui-design-figma.md` §3, §6, §7; `ui-motion-and-feedback.md` §2, §4, §7 |
| 06 | `assets/reference/06-type-scale-spacing.png` | Type scale drawn 1:1, floors by screen, stroke that closes digit holes (pass and fail), spacing scale, radius family, nested radius | Setting up the theme module; text looks tiny, clipped or blobby | `ui-design-figma.md` §2, §4, §15; `accessibility-and-player-qol.md` §4 |
| 07 | `assets/reference/07-colour-roles-contrast.png` | Colour roles, rarity ladder under protan, deutan and tritan simulation, computed contrast pass and fail, blue-versus-orange team pair with and without a lightness gap | Choosing a palette; any colour-blindness or contrast question | `ui-design-figma.md` §3; `accessibility-and-player-qol.md` §3 |
| 08 | `assets/reference/08-reward-sequence-storyboard.png` | Six frames (trigger, anticipation, reveal, count-up, goal bar, settle) with timings, an example rare-tier timeline, the tier ladder | Building a chest, hatch, claim or pickup reward; rewards feel flat or too long | `ui-motion-and-feedback.md` §5, §2; `game-craft.md` §1 |
| 09 | `assets/reference/09-template-vs-designed.png` | One daily-rewards panel built with default properties and with theme tokens, compared property by property | Showing a developer what separates a template look from a designed one | `ui-design-figma.md` §8, §6, §2; `ui-screen-recipes.md` §9 |
| 19 | `assets/reference/19-thumb-reach-phone-tablet.png` | Phone and tablet at the same physical scale with the thumbstick touch area, jump button and right thumb arc; one button at "40% from the top" on both | Someone positions touch buttons by screen percentage; planning a tablet check | `ui-input-crossplatform.md` §Mobile layout and thumb zones; `ui-design-figma.md` §11 |
| 20 | `assets/reference/20-icon-readability-sizes.png` | Two game icons at 150, 64 and 32 px in colour and greyscale; one UI icon scaled versus redrawn per size | Reviewing a game icon, item icons or HUD glyphs | `icons-thumbnails-and-store-page.md` §5; `ui-design-figma.md` §5 |

## 2. VFX, combat feel and animation

| # | Sheet | Shows | Open it when | Supports |
|---|---|---|---|---|
| 10 | `assets/reference/10-vfx-timing-chart.png` | A heavy hit as a to-scale timeline on a ms axis, light and medium hits and an enemy telegraph for comparison, the shake curve per tier (peak degrees and pixels on a phone), the strength table | Timing any hit, ability or telegraph; an effect feels late, long or weightless | `vfx-and-juice.md` §1, §6, §7; `game-craft.md` §1 |
| 11 | `assets/reference/11-vfx-layer-anatomy.png` | A melee slash and an explosion as composites and as separate layers in depth order (primary, secondary, tertiary, light, camera) with instance and lifetime, a greyscale check, and what the low tier keeps | Planning an effect as a layer table before building; cutting an effect for the low tier | `vfx-and-juice.md` §1, §2, §5, §6, §7; `vfx-recipes.md` |
| 12 | `assets/reference/12-vfx-shape-value-language.png` | Readable versus noise pairs (silhouette, direction, value stack), named palette roles with value bands for the elements in colour and greyscale, the dark-zone and bright-zone test | An effect reads as a blob; choosing element colours; an effect vanishes on a bright floor | `vfx-and-juice.md` §1, §5 |
| 21 | `assets/reference/21-attack-frame-data.png` | Light, heavy and enemy attacks as 30 fps frame strips with TrailOn, Hit, TrailOff and CancelOpen markers; ranges per phase | Authoring or retiming an attack clip; combat feels sluggish or unfair | `animation-and-rigs.md` §4, §6; `game-craft.md` §1.2 |

## 3. Cameras, onboarding, world and art direction

| # | Sheet | Shows | Open it when | Supports |
|---|---|---|---|---|
| 13 | `assets/reference/13-camera-shot-vocabulary.png` | Five shot sizes on a 5-stud avatar with frame height and camera distance at FOV 70 and 40, horizontal FOV by screen shape, lead room, the 180-degree line, cutscene rules | Writing a shot list; a cutscene feels flat, cramped or confusing | `cutscenes-and-cinematics.md` §4, §5, §8; `level-design-worldbuilding.md` §2 (screen maths) |
| 14 | `assets/reference/14-camera-path-easing.png` | Position and speed curves for Linear, Sine, Quad and Quint InOut; chained tweens versus linear segments versus one spline with one ease; spline parameter versus distance | A scripted camera looks robotic or stop-and-go | `cutscenes-and-cinematics.md` §5; `game-craft.md` §3; `accessibility-and-player-qol.md` §5 |
| 15 | `assets/reference/15-tutorial-guidance-devices.png` | Eight guidance devices in one scene (objective line, marker, beam, highlight, prompt, screen-edge pointer, button pulse, tracker) with use-when and avoid-when | Choosing how to point at the next action; players miss the first verb | `tutorial-and-onboarding.md` §5, §3, §7; `level-design-worldbuilding.md` §5 |
| 22 | `assets/reference/22-first-ten-minutes-timeline.png` | Eight beats from spawn to the first meso goal with what the game does, what to log and the failure for each | Scripting or auditing the first session | `tutorial-and-onboarding.md` §2 (the beat script, its funnel steps and fail conditions), §3, §9; `core-loop-tuning.md` §2 keeps only the timing targets |
| 16 | `assets/reference/16-lighting-key-fill-rim.png` | Key, fill, rim and local key on a look-dev scene mapped to Lighting properties; the white-cube test with computed ratios; a five-keyframe day cycle as swatches | Setting up Lighting; a scene looks flat, muddy or too dark; planning a day cycle | `lighting-and-atmosphere.md` §2, §3, §4 (values untested in engine, as in the guide) |
| 17 | `assets/reference/17-level-design-spawn-metrics.png` | A first-frame composition with six callouts; door (5 × 7.5–8), stair (rise ≤ 1, tread ≥ 2), cover, counter and window metrics drawn to scale; jump reach at five landing heights for JumpHeight 7.2 | Laying out a spawn or lobby; sizing doors, stairs, gaps and cover | `level-design-worldbuilding.md` §2, §4, §5, §6; `game-craft.md` §2 |
| 18 | `assets/reference/18-style-bible-one-pager.png` | The style-bible template filled in for an example game: three-decisions line, golden sample, palette, value rule, shape language, proportions, bevel width by viewing band, grid, texturing, lighting preset, banned list | Starting art direction; two assets do not look like one game | `art-direction-and-quality-bar.md` §6; `blender-modeling-craft.md` (shape, edges, colour); `lighting-and-atmosphere.md` §12 |

## 4. Official Roblox documentation images (external, not bundled)

These are from the Roblox Creator Docs repository. They are **not copied into the skill** because its licence statement covers prose and code samples, not clearly the images (evidence in `assets/reference/ATTRIBUTION.md`), and several are screenshots of other studios' games. Each was downloaded to a scratch folder and viewed on 2026-11-11. To look at one: download it to a scratch directory, then Read it.

```bash
curl -sS -o "$SCRATCH/img" "https://media.githubusercontent.com/media/Roblox/creator-docs/main/content/en-us/assets/<path>"
```

The same path also resolves under `https://prod.docsiteassets.roblox.com/assets/<path>`. These are references to study, not assets to copy.

| # | Path | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | `tutorials/user-interface-design/Section2/VisualHierarchy.png` | image | The docs' own zone diagram: objective information top centre, player state at the sides, the tool bottom centre | viewed |
| 2 | `tutorials/user-interface-design/Section2/MobileBlockIn.png` | image | A phone wireframe as black blocks over a greyscale screenshot, with the mobile-controls block reserved before anything is styled | viewed |
| 3 | `tutorials/user-interface-design/Section2/PCBlockIn.png` | image | The same block-in on desktop: compare what moves when the touch controls go | viewed |
| 4 | `game-design/ui-ux-design/ui-ux-design-1.png` | image | A minimal third-person HUD: two bars top-right, small ability keys at the edges, an empty centre | viewed |
| 5 | `game-design/ui-ux-design/ui-ux-design-8.png` | image | A season-pass window: numbered track, exclusives row, two actions. Study the layout only; its countdown label is the kind house rule 3 limits | viewed |
| 6 | `game-design/ui-ux-design/ui-ux-design-12.png` | image | Tabbed inventory with a four-column grid, rarity plates, a detail pane and a capacity counter in the footer | viewed |
| 7 | `game-design/onboarding-techniques/visual-elements-1.png` | image | An objective line that colour-matches the world trail it tells the player to follow | viewed |
| 8 | `game-design/onboarding-techniques/visual-elements-4.png` | image | Footprints on the ground as a route hint that suggests without ordering | viewed |
| 9 | `game-design/onboarding-techniques/timed-hints-1.png` | image | A timed hint panel: three short lines and one large button, shown only after a stall | viewed |
| 10 | `lighting-and-effects/particle-emitter/Color-Examples.jpg` | image | Three emitters differing only in `Color` over a dark scene: hue against a dark ground | viewed |
| 11 | `lighting-and-effects/particle-emitter/8x8-Explosion.png` | image | An 8×8 flipbook sheet: flash, fireball, then smoke, with spacing around every cell | viewed |
| 12 | `lighting-and-effects/beam/Curves-Applied.png` | image | A Beam bent by `CurveSize0` and `CurveSize1` between two attachments, with a colour sequence along it | viewed |
| 13 | `lighting-and-effects/beam/Width-Adjusted.png` | image | `Width0` to `Width1` taper on the same beam: the comet and crescent shape | viewed |
| 14 | `tutorials/custom-particle-effects/sizeSequenceParticles.jpg` | image | A smoke plume before colour: size sequence alone gives the billow | viewed |
| 15 | `tutorials/custom-particle-effects/colorSequenceParticles.jpg` | image | The same plume with a colour sequence, hot at the vent and grey above | viewed |
| 16–17 | `lighting-and-effects/lighting-properties/LightingStyle-Realistic.jpg`, `…/LightingStyle-Soft.jpg` | image pair | The same interior under both styles: local-light shadows and specular on one, flatter fill on the other | viewed |
| 18–19 | `lighting-and-effects/lighting-properties/GlobalShadows-True.jpg`, `…/GlobalShadows-False.jpg` | image pair | What a scene loses without cast shadows: the picture most phones below quality level 4 get | viewed |
| 20–21 | `lighting-and-effects/atmosphere/Density-A.jpg`, `…/Density-B.jpg` | image pair | Distant rock formations crisp versus faded into the air: depth bands from `Density` | viewed |
| 22–23 | `lighting-and-effects/atmosphere/Haze-A.jpg`, `…/Haze-B.jpg` | image pair | Clear versus hazy horizon and sky with the same geometry | viewed |
| 24–25 | `lighting-and-effects/post-processing/BloomEffect-With.jpg`, `…/BloomEffect-Without.jpg` | image pair | Bloom on emissive lamps in a night scene: how little is needed | viewed |
| 26 | `tutorials/environmental-art-curriculum/Section1/ThreeLaneLayout-PrimaryLanes.jpg` | image | A three-lane map plan as a top-down diagram: spawn zones and primary lanes before any geometry | viewed |
| 27 | `tutorials/environmental-art-curriculum/Section2/DesigningModularKits-ModularKit.jpg` | image | A modular kit laid out as pieces: walls, trims, corners, doorway, all on one grid | viewed |
| 28–29 | `tutorials/block-out-a-playable-area/Add-Platforms-Greybox.jpg`, `…/Add-Platforms-Final.jpg` | image pair | The same space as a greybox and dressed: the blockout already holds the silhouette | viewed |
| 30 | `animation/curve-editor/Euler-Angle-Curve-Tangents.png` | image | Curve-editor tangent handles on a rotation channel: where ease in and ease out live | viewed |

Also viewed and left out: `Section2/UserFlowChart.jpg` (text too small to read as an image), `PlayerInfoPreview.png` (too small), `ui-ux-design-4`, `-15` and `contextual-tutorial-1` (third-party game screenshots that add nothing the bundled sheets lack), `Shape-Disc.jpg`, `Texture-Applied.png`, `TimeOfDay-*`, `ColorShift-Top-255-60-0.jpg`, `EnvironmentDiffuseScale-*`, `Offset-A.jpg`, `ColorCorrectionEffect-With.jpg`, `Trimsheet.png`, `ThreeLaneLayout-SpawnZones.jpg`, `Pivot-Points-Aligned-Diagram.jpg`, `Overview-Asset-Kit.png`, `curve-editor/UI-Overview.png`, `IK-Move-Attachment.png`.

## Sources and licences

- Bundled sheets: original work made for this skill with HTML, SVG and a headless browser; no third-party artwork. Details, method credits and the rebuild command: `assets/reference/ATTRIBUTION.md`.
- External images: © Roblox Corporation and, for game screenshots, their respective studios; from `Roblox/creator-docs` at commit `7cbffff7` (2026-11-10). All 30 paths answered on the docs asset host in a link check on 2026-11-11. Licence evidence and the decision not to bundle: `assets/reference/ATTRIBUTION.md`.
