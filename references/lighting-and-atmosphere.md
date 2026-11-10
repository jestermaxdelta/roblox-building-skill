# Lighting and atmosphere: mood, readability and phone-safe light

What this is: how Roblox lighting works after the unified-lighting change, how to build a mood from key, fill, colour, air and post-processing, how to budget local lights, how to switch looks per zone on the client, and how to keep the look alive on a phone with shadows off. Open it when choosing a look for a new game, lighting an interior or a night, adding zones or a day cycle, or when a live game looks flat, glows too much or is unreadable on phones (jump to §13 and §14). It extends the "Lighting" section of `art-pipeline-blender.md` (decision rule, property starting points, five house presets) and "Shadows and lights" in `performance.md`; it does not repeat them. Map layout is in `level-design-worldbuilding.md`. Tags: `[official]` Roblox docs, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (rules of thumb unless marked measured), `[VS]` version-sensitive, `[house]` house estimate. No preset in this file was run in the engine here: every number is a starting point to tune on a phone and a PC.

## Contents

1 How lighting works today · 2 Key, fill and rim · 3 Colour script and palettes · 4 Mood by time of day · 5 Atmosphere, Sky, Clouds · 6 Post-processing safe ranges · 7 Local lights: budgets and shadow cost · 8 Interior lighting · 9 Emissive materials and fake light · 10 Per-zone transitions (client-side) · 11 Quality-level fallbacks · 12 Presets by genre · 13 Common mistakes · 14 Level-up table · Review gate · Sources

## Start here by level

| Level | Do these | Ignore for now |
|---|---|---|
| Beginner | Choose `LightingStyle` and `PrioritizeLightingQuality` on purpose in Studio (§1). Paste one genre preset (§12). Add one `ColorCorrectionEffect` and one `BloomEffect` inside the safe ranges (§6). Run the no-shadow and greyscale tests (§11). Put real lights only at focal points, `Shadows` off. | Day cycles, zone blending, grade stacks |
| Intermediate | Balance key against fill on a white cube (§2). Plan a colour strip across zones (§3). Tune Atmosphere in order (§5). Light interiors with their own profile (§8). Budget lights and cull to the nearest few (§7). Client-side zone profiles (§10). A low-detail mode (§11). | Luminance maths, clocks |
| Expert | Mood keyframes on a server-published clock (§4). A priority stack for personal screen effects (§6). GPU cost measured in the MicroProfiler (`ShadowMapSystem`, `LightGridCPU`). Contrast ratios checked numerically (§3). Snapshot and restore around Edit previews; one owner per property (§10). | Nothing; measure on the 3 GB phone |

Terms: *key* = the main directional light (sun or moon); *fill* = light in the shadows (ambient and sky); *rim* = whatever separates a shape from its background; *post-processing* = full-screen filters applied after the scene is drawn; *emissive* = a surface that shows its own colour regardless of light; *quality level* = the device's graphics setting, 1–10, automatic for most players.

## 1. How Roblox lighting works today `[VS]`

What reaches a pixel, in order: direct sun or moon light (`Brightness`, tinted by `ColorShift_Top`, blocked where `GlobalShadows` casts shadow); ambient (`OutdoorAmbient` under open sky, `Ambient` where the sky is occluded, `ColorShift_Bottom` on faces turned away from the sun); sky-derived light (`EnvironmentDiffuseScale`, `EnvironmentSpecularScale`); local lights; emissive surfaces; then `Atmosphere` haze by distance; then post-processing.

| Fact | Detail |
|---|---|
| Two properties replaced `Technology` | `LightingStyle` (Realistic or Soft) is the artistic intent; `PrioritizeLightingQuality` chooses what scales down first on weak devices: `true` keeps shadows and shaders near the camera, `false` keeps view distance `[official]` |
| Old mapping | Future → Realistic + on; ShadowMap → Soft + on; Voxel → Soft + off `[official announcement, via search summary]`. The docs confirm one case: Soft with the priority on "uses shadow maps rather than voxel lighting" `[official]` |
| `Technology` | Deprecated and locked to Roblox scripts; a script that sets it errors `[official]` |
| Shading paths | Voxel path: light and shadow on a 4×4×4-stud grid, so thin walls leak and small props cast no believable shadow. Shadow-map path: crisp sun shadows from any geometry. Realistic: per-pixel local lights, local-light shadows, visible specular `[official, lihfolk]` |
| Quality level | Shadow quality degrades as the level drops and shadows are disabled below level 4 `[official]`. Forum reports: Realistic-style shading needs level 4 or higher and is dropped when a device cannot hold 30 FPS; low settings fall back to the voxel path; lights look brighter there `[community]` |
| Ambient split | Needs `GlobalShadows` on. With it off, `Ambient` applies everywhere and `OutdoorAmbient` is ignored. If any `Ambient` channel exceeds the same `OutdoorAmbient` channel, it starts to apply outdoors too `[official]` |
| `Brightness` | Scales the sun or moon only. It raises contrast, not visibility in shadow; ambient lifts shadows `[lihfolk]` |
| `EnvironmentDiffuseScale` | Sky-coloured ambient that changes with sky and time. When raising it, lower `Ambient` and `OutdoorAmbient` or the scene washes out `[official]` |
| `ExposureCompensation` | −5 to 5; +1 doubles exposure, −1 halves it, applied before tone mapping `[official]`. Use it to lift a dim set without changing ratios |
| `ShadowSoftness` | 0 hard to 1 soft; Realistic only `[official]` |
| Fog | `FogColor`, `FogStart`, `FogEnd` are hidden and ignored while `Lighting` contains an `Atmosphere` `[official]` |
| Replication | Server writes to `Lighting` replicate to everyone; client writes stay local. `ClockTime` is tagged NotReplicated and never advances by itself `[official]` |
| Dead ends | `ShadowColor` does nothing; light `Range` is clamped to 120 studs and `Brightness` does not extend it `[official]` |

- Conflict: default style. The docs tutorials say "Studio begins every game with Soft"; LihFolk reads Realistic from the API dump. Both can be true (class default versus place template). Read your own place and set both properties explicitly.
- Conflict: can scripts set `LightingStyle`? The class reference lists no script restriction; the light-sources guide says it is "modifiable only in the Properties window", and forum threads report `PrioritizeLightingQuality` unreachable from scripts and the style reverting in the live client `[community]`. Treat both as edit-time choices and never plan a runtime switch.
- Conflict: `ShadowSoftness` default is 0.2 on the reference page and 0.5 in the API dump `[lihfolk]`. Set it explicitly (0.15–0.3 per `art-pipeline-blender.md`).
- Decision rule (from `art-pipeline-blender.md`, restated in one line): Realistic for interiors, local lights, PBR metals and night; Soft for bright flat cartoon art; priority on for small dense worlds, off for large open maps. Ship Realistic only if the low-end capture still holds 30 FPS (`performance.md`).

## 2. Key, fill and rim

Film terms map onto a handful of properties. Get this balance right before touching post-processing.

| Role | Roblox lever | Target | Trap |
|---|---|---|---|
| Key | Sun or moon: `ClockTime` and `GeographicLatitude` set the angle, `Brightness` the strength, `ColorShift_Top` the tint | Sun 30–50° above the horizon, a quarter turn off the main direction of travel, so every object shows a lit side, a shadow side and a readable top `[lihfolk]` | Overhead noon sun lights all tops equally and flattens every wall: the "flat noon" look |
| Fill | `OutdoorAmbient`, `Ambient`, `EnvironmentDiffuseScale` 0.2–0.5 | Lit faces about 1.5–2.5× the brightness of shadow faces on a white cube; fill cooler than the key `[lihfolk]` | Fill too bright: flat cut-outs. Fill near black: shadow sides become holes on a phone in daylight |
| Rim and separation | `ColorShift_Bottom` (bounce colour), value contrast between character and ground, Atmosphere depth bands, a `Highlight` outline as fallback | Characters, enemies and pickups sit at a value nothing around them uses | Relying on shadows for separation: they are off below level 4 |
| Local key | One hero light per room or node | A pool roughly the size of the play space around the feature `[lihfolk]` | A bright lamp in a dead end pulls players into it |

- Warm key with cool fill is the dependable default: a warm `ColorShift_Top` and a slightly blue ambient give every flat-coloured object a hue shift for free `[lihfolk]`.
- Value before hue: if the scene does not read in greyscale, colour will not save it.
- Lay out the map so the main play direction looks across the light, not into it (everything back-lit and muddy) or away from it (everything front-lit and flat) `[lihfolk]`.
- Colour does the work shadows would do. Shadows vanish below quality level 4, so the lit-side and shadow-side difference must come from `ColorShift_Top`, ambient tint, bevels and baked vertex-colour AO, with shadows as a bonus.
- Build a look-dev corner in a `_Dev` folder (never published): white cube, white sphere, mid-grey cube, the palette chips, the R15 dummy and the golden sample. Check every new asset there under each preset the game uses `[lihfolk]`.

## 3. Colour script and palettes

A colour script is the plan for how colour and value change across the game. For a zone chain it is one strip.

- Put each zone's ground, mid (props), accent and sky colour side by side in one image and read across it. The strip exposes neighbours that are too close (forest green into jungle green), value cliffs three zones running, and an accent used by four zones `[lihfolk]`.
- Rules that hold `[lihfolk]`: each zone owns one accent hue no other zone uses; alternate warm and cool along the chain; widen the value range with progression (deeper darks and brighter emissives read as "higher level"); the ground carries the zone's base colour flatly and calmly.
- Saturation is a budget: spend it on the hero landmark, interactables and rewards, never on the ground. Pickups use one game-wide colour no zone uses as decoration.
- Value structure from the style bible: ground mid-dark, walls mid, interactables brightest. Decide per zone whether enemies are lighter or darker than the floor and enforce it.
- Check contrast numerically where it matters. Relative luminance `L = 0.2126 R + 0.7152 G + 0.0722 B` on linearised channels; contrast ratio `(L_light + 0.05) / (L_dark + 0.05)`. Aim for 3 or more between a gameplay object and its usual background before lighting `[lihfolk]`; a critical signal also needs a non-colour cue (shape, motion, outline).
- Sample colours under the game's lighting, not in a colour picker. Near-black surface colours (luminance under about 0.06) swallow texture detail entirely `[lihfolk, measured]`.
- Three reads identify a zone: silhouette (screenshot as black on white), colour (blurred screenshot), light (props hidden). Two of three is the minimum. Light is the cheapest to change: minutes of tuning alter every pixel `[lihfolk]`.
- Light colour is a language too: one colour for safe, the hazard colour only on hazards, one for interactables. Never light a harmless area in the hazard colour.

## 4. Mood by time of day

Most games should pick one hour and tune it. Add a cycle only when night changes play (roleplay, survival, horror).

Keyframes for a cycle (`[house]`, blended from the LihFolk recipes and the `art-pipeline-blender.md` presets). Interpolate every field, not only `ClockTime`, or midnight looks like a dim noon.

| Moment | ClockTime | Brightness | OutdoorAmbient | Ambient | ColorShift_Top | Atmosphere Color / Haze | Grade saturation |
|---|---|---|---|---|---|---|---|
| Dawn | 6.3 | 1.5 | (120,110,125) | (75,70,85) | (255,200,170) | (235,200,190) / 1.5 | 0 |
| Day | 14 | 2.5 | (140,140,150) | (90,90,100) | (255,240,215) | (200,225,255) / 0.5 | +0.1 |
| Golden hour | 17.6 | 2.2 | (130,100,90) | (90,70,70) | (255,190,120) | (255,200,160) / 1.5 | +0.1 |
| Dusk | 18.6 | 1.0 | (100,90,125) | (65,60,90) | (230,150,150) | (160,130,170) / 1.5 | 0 |
| Night | 0 | 0.6 | (80,95,140) | (60,70,110) | (150,170,255) | (60,75,120) / 0.5 | −0.1 |

- Night is shown by hue (blue-violet), lower saturation and lit windows, not by darkness. Keep night ambient around 15–25% brightness and tinted, so silhouettes read at 50 studs; moonlight is a weak, cool, clearly angled key `[lihfolk]`. Test on a phone at low screen brightness.
- Gameplay objects get their own readability at night (outline, emissive accent, a small light). Do not brighten the whole world to rescue three objects.
- The clock: the server publishes the cycle once as attributes; each client derives the hour from `workspace:GetServerTimeNow()`, so there is no per-frame traffic and late joiners are correct at once. Give day more than half the cycle (one production game used a 360 s cycle with 62% day) `[lihfolk]`. Apply the mood at 10–20 Hz.
- Golden hour collapses to "orange" when shadows are off; the colour shift has to carry it. Long shadows across the playfield also hurt gameplay readability: lovely for a hub, risky for an arena `[lihfolk]`.
- QA needs a developer-only override (an attribute such as `ForceClock`) to pin the hour.

```lua
--!strict
-- Unexecuted sketch. Client. The server sets Workspace attributes DayEpoch (server time of a 06:00) and DayLength (seconds) once.
local DAY_SHARE = 0.62 -- fraction of the cycle between 06:00 and 18:00

local function clockTime(): number
	local length = workspace:GetAttribute("DayLength") :: number
	local t = ((workspace:GetServerTimeNow() - (workspace:GetAttribute("DayEpoch") :: number)) % length) / length
	if t < DAY_SHARE then
		return 6 + 12 * t / DAY_SHARE
	end
	return (18 + 12 * (t - DAY_SHARE) / (1 - DAY_SHARE)) % 24
end
return clockTime
```

## 5. Atmosphere, Sky and Clouds

| `Atmosphere` property | Does `[official]` | Working range `[lihfolk]` |
|---|---|---|
| `Density` | Amount of air between camera and object; obscures objects and terrain, not the skybox directly | 0.25–0.35 clear day, 0.4–0.55 hazy, 0.6+ fog and storms |
| `Offset` | How light transmits between camera and sky: higher silhouettes the horizon, lower blends distant objects into the sky | 0–0.25 for endless open worlds, 0.25–0.5 for a crisp horizon |
| `Haze` | Haziness above the horizon and into the distance | 0–3; most moods 1–2 |
| `Color` | Hue of the air; needs `Haze` to show | Tint toward the zone palette |
| `Glare` | Glow around the sun; needs `Haze` above 0 | 0–0.5 for most scenes |
| `Decay` | Hue away from the sun; needs `Haze` and `Glare` above 0 | Cooler than `Color` at sunset |

- Tuning order `[lihfolk]`: `Density` until distant geometry fades where the "edge of interest" should be; `Offset` until the horizon silhouette is right and nothing ghosts; `Haze` and `Color` for mood; `Glare` and `Decay` last, looking toward the sun.
- Ghosting: a low `Offset` with a high `Density` lets the skybox show through distant objects `[official]`. Raise `Offset`.
- Density hides distance, it does not cull: hidden geometry still renders. Pair dense air with a smaller `StreamingTargetRadius` (`performance.md`) if the goal is performance.
- Reference values `[official]`: the indoor tutorial uses `Density` 0.5 so sun shafts catch haze; the environmental-art curriculum uses 0.285 (preset in `art-pipeline-blender.md`).
- Sky: six images that must be seamless at every shared edge `[official]`. The sky also feeds environment diffuse and specular light, so choose or paint one whose horizon colours match the palette. Author skies yourself (rendered from Blender or painted); keep faces at 1024² or less `[house]`. `SunAngularSize` defaults to 21° and clamps to 0–60; 0 hides the sun alone; `CelestialBodiesShown = false` hides sun, moon and stars `[official]`.
- `SkyboxOrientation` rotates the six faces only (not the sun, moon, stars or clouds); wrap the angle with `% 360` `[official]`. A slow client-side spin (1–5° per second) makes a night or alien sky feel alive `[lihfolk]`.
- Clouds render only when the `Clouds` object is parented under `Workspace.Terrain` `[official]`. That uses the Terrain container, not terrain voxels, so it does not touch the Terrain house rule. `Cover` 0–1, `Density` (thin and wispy to dark and stormy), `Color` (heavily influenced by Lighting and Atmosphere). Motion comes from `Workspace.GlobalWind`; changing the wind wakes physics assemblies, so do not animate it every frame.
- Weather reads well when cloud `Cover` and `Density` move together with `Atmosphere.Density` and `Haze` over 5–20 s `[lihfolk]`. Rain and snow emitters follow the camera; they are not spread over the map.

## 6. Post-processing: safe value ranges

Effects in `Lighting` show to every player; effects in the `Camera` show to that player only `[official]`. Each one is a full-screen pass: keep 2–3 always on (`art-pipeline-blender.md`). Some effects do not render at a low Editor Quality Level, so author at the highest and test at the lowest `[official]`.

| Effect | Engine default `[lihfolk: API dump]` | Safe range for world mood | Never |
|---|---|---|---|
| `ColorCorrectionEffect` | Brightness, Contrast, Saturation 0; TintColor white | Contrast 0 to +0.15; Saturation −0.2 to +0.2 (horror down to −0.45); Brightness within ±0.05; TintColor no darker than about (215,215,215) on any channel | Contrast above about 0.25: crushed blacks on a phone screen. Using Brightness to fix exposure (use `ExposureCompensation`). A strong tint as the permanent grade (it multiplies channels and removes colours) |
| `BloomEffect` | Intensity 0.4, Size 24, Threshold 0.95 | Day scenes: Intensity 0.2–0.5, Threshold 1.1–2 so only emissive and effects glow. Night, neon, caves: Intensity 0.6–1.2, Threshold 0.9–1, Size 24–40 | Threshold under about 0.9 with white or pale surfaces in view: walls and snow glow. Gameplay information carried by glow alone: bloom is missing at low graphics `[community]` |
| `SunRaysEffect` | Intensity 0.25, Spread 1 | Intensity 0.02–0.15 (the indoor tutorial uses 0.023, Spread 0.266 `[official]`); only when the sun is in the composition | Spread outside 0–1 (undefined `[official]`); leaving it on when the sun is never on screen |
| `DepthOfFieldEffect` | FarIntensity 0.75, FocusDistance 0.05, InFocusRadius 10, NearIntensity 0.75 | Shop previews, photo mode, cutscenes: FocusDistance = camera-to-subject distance, InFocusRadius 3–10, FarIntensity 0.3–0.6, NearIntensity 0 | On during third-person gameplay: the character and the enemy are at different distances |
| `BlurEffect` | Size 24 | Behind modal menus: tween Size 0 → 12–20, in the Camera | A blur whose lifetime is not tied to the menu's cleanup ("my screen is stuck blurry"); ignoring a reduce-motion setting |
| `ColorGradingEffect` | TonemapperPreset Default | Default, or Retro for the pre-2019 look with all light Brightness at 1.0 or less | More than one: it must sit in `Lighting` and only the most recently parented applies `[official]` |

- Conflict: the earlier house cap on `BloomEffect.Intensity` was 0.1–0.5 `[house]`; LihFolk's night and neon recipes use up to 1.2 `[lihfolk]`. Both hold: 0.5 is the day-scene cap with a threshold near 1; higher intensity is acceptable only with a threshold of 1.5 or more, or in dark scenes where emissive surfaces are the lighting.
- Tune bloom and effect brightness together `[lihfolk]`: particles, beams and trails can be far brighter than 1, so a combat game sets Threshold around 1.5–2 and lets effect brightness cross it, while a stylised game that wants signs to glow sets Threshold near 1 and keeps white surfaces off-white.
- Colour correction is reported to run after tone mapping while bloom and sun rays work on the HDR image `[community]`, which is why a contrast boost can rescue a "washy" bloom but cannot recover clipped highlights.
- Ownership: the zone grade and bloom are named instances in `Lighting` with one writer (§10). Personal effects (low-health tint, hit flash, menu blur, ultimate grade) live in the Camera behind a small priority stack (zone base 0, low health 10, status 20, cutscene or ultimate 100): systems push and pop requests, and one function applies the winner. Without it, the last writer wins every frame `[lihfolk]`.

## 7. Local lights: budgets and shadow cost

| Class | Shape | Use `[official]` | Note |
|---|---|---|---|
| `PointLight` | Sphere | Bulbs, torches, pickups | Costs more than the others on low-end devices because it projects in every direction `[official]` |
| `SpotLight` | Cone from a face (`Angle` up to 180) | Street lamps, torches, headlights | On an Attachment it aims along the attachment |
| `SurfaceLight` | Whole face of a part | Screens, signs, panels, window "sun" | Needs a BasePart face |

- Budget: Roblox publishes no per-scene light limit. Working numbers for a mid-range phone: at most 8–12 local lights affecting the screen `[lihfolk]` and 2–4 with `Shadows` on (`performance.md`). The MicroProfiler decides, not the table.
- The official cost list: many shadow-casting lights, many small parts receiving shadows, large `Range` and `Angle`, moving shadow casters. Mitigations in the docs' own order: `CastShadow` off on small parts, shadows off on moving objects, `Light.Shadows` off where not needed, smaller range and angle, fewer lights, lights disabled by distance or room `[official]`.
- Fixture pattern: the light sits on a `Light_Att` attachment exported with the Blender fixture, just outside the shade, with `Shadows = false`. A light inside a shade with shadows on is shadowed by its own lamp: move the attachment or set `CastShadow = false` on the shade `[lihfolk]`.
- A light that "does not reach" needs more `Range`, not more `Brightness` (which only burns out the centre). Turn on Show Light Guides in Studio settings while placing `[official]`.
- Shadows only on the hero lights that shape a room (a ceiling lamp, a window spot). One production lobby read as cosy on seven unshadowed PointLights `[lihfolk, measured]`.
- Thin for performance by tagging and disabling, not deleting, so lights can return on higher tiers `[lihfolk]`.
- Effect lights expire with their effect (parent under the effect root or pool them); cap them (two per ability cast, four alive in total, was one project's rule) `[lihfolk]`.
- Reference values `[official tutorials]`: candle cluster PointLight Brightness 0.7, Color (255,202,156); desk lamp SpotLight Angle 140, Brightness 4, Range 12; radio screen SurfaceLight Brightness 2, Range 4; campfire PointLight Brightness 2, Color (255,179,73).

```lua
--!strict
-- Unexecuted sketch. Client. Fixture lights carry the tag "DecorLight"; only the nearest few stay on.
local CollectionService = game:GetService("CollectionService")
local MAX_ON, MAX_DISTANCE = 8, 120 -- low-detail mode drops MAX_ON to 4

local function refresh()
	local camera = workspace.CurrentCamera
	if not camera then return end
	local origin = camera.CFrame.Position
	local near: { { light: Light, distance: number } } = {}
	for _, inst in CollectionService:GetTagged("DecorLight") do
		local parent = inst.Parent
		local position: Vector3? = if parent and parent:IsA("Attachment") then parent.WorldPosition
			elseif parent and parent:IsA("BasePart") then parent.Position else nil
		if inst:IsA("Light") and position then
			local distance = (position - origin).Magnitude
			if distance <= MAX_DISTANCE then
				table.insert(near, { light = inst, distance = distance })
			else
				inst.Enabled = false -- client-side change: does not replicate
			end
		end
	end
	table.sort(near, function(a, b) return a.distance < b.distance end)
	for index, entry in near do entry.light.Enabled = index <= MAX_ON end
end

task.spawn(function()
	while true do
		refresh()
		task.wait(0.25) -- lights on streamed-out fixtures simply leave the tag list
	end
end)
```

## 8. Interior lighting

- "Indoors" means occluded from the sky: `Ambient` applies there and `OutdoorAmbient` does not, but only with `GlobalShadows` on `[official]`. If an interior is as bright as outside, shadows are off, an `Ambient` channel exceeds `OutdoorAmbient`, or the shell leaks.
- Shell thickness: under Realistic, enclose interiors with geometry at least 1 stud thick (the official sample uses 2.5) `[official]`. On the voxel path the light grid is 4 studs, so walls thinner than a cell leak `[lihfolk]`, and low quality levels can fall back to that path `[community]`. So Blender walls are ≥ 1 stud thick, roofs and floors are sealed, and an interior that must stay dark on phones gets an invisible blocker shell about 4 studs thick outside the visual wall. That blocker is the one helper that keeps `CastShadow = true` (parts cast shadows regardless of transparency, `performance.md`) `[house: verify on the low-end phone]`.
- Give interiors their own profile and switch to it at the door in 0.5–1 s (§10). Official sample values for a warm cabin `[official]`: `Ambient` (83,70,57), `ClockTime` 15.6 so sun enters the window at an angle, `EnvironmentDiffuseScale` and `EnvironmentSpecularScale` 1 for PBR metal, `Atmosphere.Density` 0.5, sun rays 0.023 / 0.266, colour correction Contrast 0.05 and Saturation 0.1.
- Lift a dim interior with `ExposureCompensation`, not `Brightness`: exposure keeps the light ratios; brightness only strengthens the sun `[official]`.
- Light is the interior's wayfinding. The official sample pulls the eye fireplace → window → exit; make the exit the last and clearest pool `[official]`.
- One shadowed hero light per room, unshadowed fills, and emissive window panes with a `SurfaceLight` on the pane's inner face to fake daylight.
- Under Soft, local lights do not cast shadows the way the sun does and material detail flattens `[official]`: an interior-heavy game is the main reason to choose Realistic.
- Ceilings of 10–15 studs keep the third-person camera out of the roof (`level-design-worldbuilding.md` §2).

## 9. Emissive materials and fake light

| Feature | Lights the surroundings? | What it is for |
|---|---|---|
| `Light` instance | Yes, within `Range` | The few real pools of light |
| Emissive mask on a `SurfaceAppearance` (`EmissiveMaskContent`, `EmissiveStrength`, `EmissiveTint`) `[official, VS]` | No | Windows, screens, runes, lamp glass painted in Blender; too high a strength clamps to white `[official]` |
| `Material = Neon` on a Blender mesh | No | Whole-mesh glow with no texture; reads the same day and night; loses its bloom at low graphics `[community]` |
| `LightEmission` on particles, beams, trails | No (additive blending only) `[lihfolk]` | Effects |

- A glowing object is up to three layers: an emissive surface, a bright trail or particles, and one small `PointLight` (Range 6–14) so the floor picks up the colour. When the budget is tight, drop the light first; the other two still read as glowing `[lihfolk]`.
- Keep glow rare: emissive only on interactables, landmarks and light fixtures (style bible). Glow covering more than about a sixth of an object, or of the frame, dissolves shapes in bloom on high settings and looks flat on low ones `[lihfolk, measured]`.
- Fake light that costs no lighting: a warmer palette swatch or vertex-colour tint baked around a fixture; a soft "light pool" disc mesh under a lamp (few of them: partial transparency is overdraw); `ColorShift_Bottom` in the lava colour so every underside glows without one local light `[lihfolk]`.
- Bake what shadows would have given: vertex-colour AO and a darker contact band at the base of props (`bake_ao_to_vertex_colour` in `art-pipeline-blender.md`) keep objects seated when shadows are off.
- Test the brightest and the darkest effect in the brightest and the darkest zone. One project's effect set, designed in daylight, vanished in dark zones and had to be re-authored brighter with a small coloured light per large piece `[lihfolk]`.

## 10. Per-zone lighting transitions (client-side)

There is one `Lighting`, one `Atmosphere` and one `Sky` at a time. Per-zone looks are each client swapping profiles as its own player moves; client writes do not replicate, which is the point.

- The server sets the initial look and then publishes facts only (clock epoch, weather state) as attributes. If the server also writes `Lighting`, it overwrites every client's blend `[lihfolk]`.
- Exactly one client system writes each property. A cutscene or ultimate sets a flag, the mood controller stands aside, and on release the controller blends back over 1–2 s. Two tweens on `Ambient` at once produce a flicker that is very hard to trace `[lihfolk]`.
- Profiles are data (one table per look); zones are boxes stored in a module, exported from the zone volumes at edit time, so streaming cannot remove them.
- Between zones keep the previous profile; overlap neighbouring boxes by a few studs so a player on the border does not flicker.
- Durations `[lihfolk]`: 1.5–3 s walking between zones; 0 during a teleport's fade cover; 0.5–1 s through a door; 5–20 s for weather. For long open borders, blend by position across a band instead of by trigger.
- Skies cannot blend. Swap the `Sky` inside a tunnel or arch, or under dense air, and preload its six textures first or the default sky flashes.
- Do not tween `ClockTime` per zone (the sun slides across the sky as players walk); fake a different hour with ambient, colour shift and grade, or change it inside a tunnel.
- Forum reports: tweening Atmosphere colours looks choppy while `Density` is smooth, and a recent thread reports choppy rendering when tweening several lighting properties at once `[community]`. Keep the tweened set small, cancel running tweens before starting new ones, and step colour changes at the threshold if a blend stutters on the phone.
- Edit-mode previews leak: snapshot every `Lighting`, `Atmosphere` and effect value before a preview and restore it after. A controller that reads the place's Atmosphere as its base at Play start bakes in whatever a preview left behind `[lihfolk, measured]`.

```lua
--!strict
-- Unexecuted sketch. Client (StarterPlayerScripts). The only writer of Lighting, Atmosphere, ZoneGrade and ZoneBloom.
local Lighting = game:GetService("Lighting")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

type Goals = { [string]: any }
type Profile = { Lighting: Goals, Atmosphere: Goals, Grade: Goals, Bloom: Goals }
type Box = { profile: string, cframe: CFrame, size: Vector3 }
local Zones = require(ReplicatedStorage.Shared.Config.LightingZones) :: { profiles: { [string]: Profile }, boxes: { Box } }

local atmosphere = Lighting:WaitForChild("Atmosphere") :: Atmosphere
local grade = Lighting:WaitForChild("ZoneGrade") :: ColorCorrectionEffect
local bloom = Lighting:WaitForChild("ZoneBloom") :: BloomEffect
local player = Players.LocalPlayer
local current: string? = nil
local running: { Tween } = {}

local function apply(name: string, seconds: number)
	for _, tween in running do tween:Cancel() end
	table.clear(running)
	local profile = Zones.profiles[name]
	local targets: { [Instance]: Goals } =
		{ [Lighting] = profile.Lighting, [atmosphere] = profile.Atmosphere, [grade] = profile.Grade, [bloom] = profile.Bloom }
	for instance, goals in targets do
		if seconds <= 0 then
			for property, value in goals do (instance :: any)[property] = value end
		else
			local info = TweenInfo.new(seconds, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
			local tween = TweenService:Create(instance, info, goals)
			table.insert(running, tween)
			tween:Play()
		end
	end
	current = name
end

local function zoneAt(position: Vector3): string?
	for _, box in Zones.boxes do
		local p = box.cframe:PointToObjectSpace(position)
		if math.abs(p.X) <= box.size.X / 2 and math.abs(p.Y) <= box.size.Y / 2 and math.abs(p.Z) <= box.size.Z / 2 then
			return box.profile
		end
	end
	return nil -- between zones: keep the previous profile
end

task.spawn(function()
	while true do
		task.wait(0.25)
		local character = player.Character
		if character and not player:GetAttribute("LightingLocked") then -- cutscenes set this flag and take over
			local name = zoneAt(character:GetPivot().Position)
			if name and name ~= current then
				apply(name, if current then 2 else 0) -- first apply and teleports are instant; walking blends
			end
		end
	end
end)
```

## 11. Quality-level fallbacks for low-end phones

Most phones run on automatic quality and many sit below level 4, where there are no shadows at all `[official]`. Design for that picture first and let higher levels add richness.

- No-shadow test: set Studio's Editor Quality Level to 1–3 (or turn `GlobalShadows` off for a moment). If the scene goes flat and unreadable, move contrast into `ColorShift_Top`, ambient tint, material value and baked AO `[lihfolk]`.
- Greyscale test: `ColorCorrectionEffect.Saturation = -1`. Player, enemies, pickups and the path must each sit at their own value.
- Never encode gameplay in shadows, bloom or fine local-light shading: a dark doorway that means danger, or a glow that marks the objective, also needs shape, colour or motion.
- `PrioritizeLightingQuality`: `false` for open maps keeps view distance (and far landmarks) as quality drops; `true` for interiors and dense small maps keeps the light.
- Local lights can read brighter on the voxel fallback `[community]`: look at each lit interior at level 1 before shipping and trim brightness if it blows out.
- Low-detail mode `[house]`, chosen by a settings toggle and automatically from measured frame time with hysteresis (`performance.md`), turns things off in this order: (1) SunRays and any DepthOfField; (2) shadows on local lights, then all but the nearest four decorative lights; (3) bloom to half, then off; (4) ambient particle emitters; (5) a slightly denser Atmosphere to hide the shorter view. It never changes anything that carries gameplay information.
- Detection: `UserSettings():GetService("UserGameSettings").SavedQualityLevel` returns `Automatic` or `QualityLevel1`–`QualityLevel10` `[official]`. `Automatic` (the usual phone case) says nothing about the real level, so measured frame time is the signal that matters.
- Test matrix: Editor Quality Level 1, 4 and maximum; the 3 GB Android phone; the same phone at low screen brightness for night presets.

## 12. Presets by genre

Starting points `[house]`, adapted from the LihFolk recipes and earlier house presets (`art-pipeline-blender.md` keeps only an overcast and an interior-shop preset and defers to this file for everything else). Colours are RGB 0–255; `Ambient` never exceeds `OutdoorAmbient` on any channel. Atmosphere is Density / Offset / Haze / Glare then Color; Bloom is Intensity / Size / Threshold; Grade is the zone `ColorCorrectionEffect`. Apply, then run the §11 tests on the phone.

| Genre look | Style, priority | ClockTime | Brightness | Ambient / OutdoorAmbient | ColorShift Top / Bottom | Env diffuse / specular | Atmosphere | Bloom | Grade |
|---|---|---|---|---|---|---|---|---|---|
| Simulator or pet hub (bright cartoon) | Soft, off | 14 | 2.5 | (100,100,115) / (145,145,155) | (255,240,215) / none | 0.3 / 0 | 0.25 / 0.1 / 0.5 / 0, (200,225,255) | 0.4 / 24 / 1.2 | Contrast 0.08, Saturation 0.15 |
| Tycoon or cozy town (golden hour) | Realistic, on | 17.6, latitude 30 | 2.2 | (90,70,70) / (130,100,90) | (255,190,120) / (60,40,80) | 0.4 / 0.3 | 0.35 / 0.2 / 1.5 / 0.4, (255,200,160) | 0.5 / 32 / 1.1 | Contrast 0.1, Saturation 0.1, tint (255,245,235); SunRays 0.06 |
| Obby or platformer (clear and angled) | Soft, off | 10 | 2.5 | (95,100,115) / (140,145,160) | (255,245,225) / none | 0.3 / 0 | 0.2 / 0.25 / 0 / 0, (210,230,255) | 0.3 / 24 / 1.5 | Contrast 0.1, Saturation 0.1 |
| PvP arena or battlegrounds (calm world, loud effects) | Soft or Realistic, on | 16 | 2 | (70,70,85) / (100,100,115) | (255,225,190) / none | 0.2 / 0.1 | 0.3 / 0.15 / 1 / 0, (180,190,210) | 0.8 / 32 / 1.6 | Contrast 0.12, Saturation −0.05 |
| Horror (fog) | Realistic, on | 20.5 | 0.5 | (35,35,40) / (55,55,60) | none | 0.1 / 0.2 | 0.55 / 0 / 2.5 / 0, (120,125,130) | 0.3 / 20 / 1.5 | Contrast 0.05, Saturation −0.4, tint (235,245,240) |
| Dungeon or cave interior | Realistic, on | any | 0.3 | (50,45,70) / (60,55,85) | none | 0.1 / 0.5 | 0.45 / 0 / 1 / 0, (90,80,120) | 0.8 / 30 / 1.0 | Contrast 0.12, Saturation 0.1; ExposureCompensation +0.3 |
| Roleplay town at night (readable) | Realistic, on | 0 | 0.6 | (60,70,110) / (80,95,140) | (150,170,255) / none | 0.2 / 0.4 | 0.3 / 0 / 0.5 / 0, (60,75,120) | 0.6 / 30 / 0.95 | Contrast 0.1, Saturation −0.1, tint (220,230,255); ExposureCompensation +0.2 |
| Neon city or night racing | Realistic, on | 22 | 0.4 | (40,30,60) / (60,45,90) | none | 0.2 / 0.6 | 0.4 / 0 / 2 / 0, (90,50,120) | 1.0 / 36 / 0.9 | Contrast 0.15, Saturation 0.2 |

- Conflict: the simulator row uses a brighter ambient than the earlier house "Bright stylized day" preset ((70,70,80) / (120,120,130)) `[house]`. The darker pair gives bevelled palette art more form; the brighter pair is the "nothing is ever dark" simulator look. Decide with the white-cube test: lit faces 1.5–2.5× shadow faces.
- Obby: no haze (the next stages must read), no sun rays, no depth of field; the kill colour is the only saturated emissive on the course. PvP: environment saturation slightly below zero leaves saturation for effects and team colours; light the fighting floor more than its surroundings. Horror: one warm light the player carries or follows; darkness hides the threat, never the counter. Bright cartoon cannot be made scary by darkening it: switch preset `[lihfolk]`.
- Special zones `[lihfolk]`: lava uses `ColorShift_Bottom` (255,80,30) with warm haze; frost keeps Bloom Threshold near 1.4 so snow does not glow and uses cool ambient for blue shadows; underwater is `Density` 0.6 with a teal tint and red removed, built as a lighting mood rather than a volume of water; void zones are near-black with emissive rims on everything that matters.

## 13. Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Everything glows, white walls included (over-bloom) | Bloom Threshold below about 1 with pale surfaces; high Intensity | Threshold 1.1–2; Intensity ≤ 0.5 by day; off-white instead of pure white |
| Crushed blacks, detail lost in shadow on phones | Contrast pushed past about 0.25; near-black ambient; stacked grade and tint | Contrast ≤ 0.15; tinted ambient; lift with `ExposureCompensation` |
| Flat, shapeless scene at noon | Overhead sun; ambient close to sun strength | Sun at 30–50°, a quarter turn off the travel direction; lower ambient or raise Brightness |
| Night is black or unplayable | Ambient near zero | Blue-violet ambient at 15–25%; outlines and emissive accents on gameplay objects |
| Washed out after raising environment diffuse | Ambient not lowered | Lower `Ambient` and `OutdoorAmbient` together with it |
| Fog settings do nothing | An `Atmosphere` exists | Use `Density` and `Haze`, or remove the Atmosphere |
| Glare or Decay does nothing | `Haze` is 0 (and `Glare` 0 for Decay) | Raise Haze first |
| Skybox visible through distant hills | `Offset` too low for the `Density` | Raise `Offset` |
| Indoors as bright as outdoors | `GlobalShadows` off, `Ambient` above `OutdoorAmbient`, or a leaking shell | Shadows on; Ambient ≤ OutdoorAmbient; thicker or sealed shell |
| Metal looks like grey plastic | `EnvironmentSpecularScale` 0 | Raise toward 1 where PBR metal matters |
| Lamp throws a black shadow of itself | Light inside the shade with Shadows on | Move the attachment out or `CastShadow` off on the shade |
| Lighting flickers at borders or after cutscenes | Two systems writing the same properties | One owner; flag hand-off; blend back |
| "It looked different yesterday" | An Edit preview left values changed | Snapshot and restore |
| Clouds missing or frozen | Not under `Workspace.Terrain`; `GlobalWind` zero | Re-parent; set a wind vector |
| Soft focus on the enemy or the avatar | DepthOfField left on in gameplay | Contextual only |
| Sky pops on zone change | Sky swapped in view or not preloaded | Swap in a threshold; preload |

## 14. Level-up: symptoms in a live game → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| "Looks cheap" or flat in feedback and thumbnails | Default lighting, no key-to-fill contrast, no grade | Preset from §12; white-cube balance; one ColorCorrection |
| Looks great on PC, grey on phones | Look depends on shadows, bloom or Realistic shading | §11 tests; move contrast into colour shifts, ambient tint and baked AO |
| Phone players cannot see at night or in caves | Black ambient; low screen brightness | Tinted ambient; exposure +0.2 to +0.3; emissive and outlines on gameplay objects |
| Frame rate dips near lantern rows or markets | Many overlapping lights, some shadowed; `ShadowMapSystem` high | Shadows off on decoration; nearest-K culling; fewer, larger lights |
| Zones feel the same | One global look | Client profiles per zone; one accent hue each; colour strip review |
| Players miss the exit or objective indoors | Brightest light is decoration | Light the exit; dim the rest |
| Enemies or pickups blend into the floor | No value plan per zone | Per-zone lighter-or-darker rule; contrast ratio ≥ 3; outline fallback |
| Effects invisible in one zone | Effect palette matches the zone (fire in lava, white in snow) | White-hot core and dark rim; test in darkest and brightest zones |
| Interiors glow with daylight on phones | Thin shells leaking on the voxel fallback | Sealed shell; invisible 4-stud blocker |
| Screen stays tinted or blurry | Personal effects with no owner or cleanup | Camera effects behind a priority stack; tie blur to menu lifetime |
| Stutter when crossing zones | Many lighting tweens at once; Atmosphere colour tweens | Smaller tween set; step colour in the threshold |
| The whole server changes look when one player enters a cave | Zone lighting written by the server | Move it to the client controller |

## Review gate

- [ ] `LightingStyle` and `PrioritizeLightingQuality` chosen in Studio and written in the style bible; nothing depends on `Technology` or on switching style at runtime.
- [ ] `Ambient` ≤ `OutdoorAmbient` on every channel; `GlobalShadows` on unless the style deliberately has none.
- [ ] White-cube check: lit faces about 1.5–2.5× shadow faces; sun angled, not overhead.
- [ ] Greyscale and no-shadow tests pass in every preset the game uses; night readable on a dim phone.
- [ ] Atmosphere or fog, not both; no ghosting at the horizon; far landmarks still visible in every preset.
- [ ] At most 2–3 always-on post effects, all inside the safe ranges; DepthOfField and Blur contextual only.
- [ ] Local lights within budget in the worst view; shadows only on hero lights; decorative lights culled by distance.
- [ ] Interiors sealed, ≥ 1 stud thick, with their own profile; checked for leaks at quality level 1.
- [ ] Emissive only on interactables, landmarks and fixtures; nothing important is signalled by glow alone.
- [ ] One client owner for `Lighting`, `Atmosphere` and the zone grade; the server writes no lighting after setup; cutscenes hand off by flag.
- [ ] Low-detail mode exists and never removes gameplay information; captured on the 3 GB Android phone.

## Sources

Accessed 2026-11-10.

- https://github.com/Roblox/creator-docs (read, commit ccc2b01 of 2026-11-07), under `content/en-us/`: `environment/{lighting,atmosphere,skybox,clouds,post-processing-effects}.md`, `effects/light-sources.md`, `tutorials/use-case-tutorials/lighting/{enhance-indoor-environments,enhance-outdoor-environments,light-with-props}.md`, `performance-optimization/improve.md`, `reference/engine/classes/{Lighting,Atmosphere,Sky,Clouds,Light,BloomEffect,ColorCorrectionEffect,SunRaysEffect,DepthOfFieldEffect,BlurEffect,ColorGradingEffect,SurfaceAppearance,UserGameSettings,Workspace}.yaml`, `reference/engine/enums/{LightingStyle,SavedQualitySetting}.yaml`
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/07 Lighting VFX and Audio/{Lighting Technologies and Settings,Light Sources and Shadows,Lighting Mood and Time of Day,Stylized Lighting Recipes,Atmosphere Sky Clouds and Post-Processing}.md`; `54 Untextured Stylised Modelling/Lighting Untextured Art in Roblox.md`; `06 World Building and Art/Zone and Biome Art Direction.md`; `skills/lihfolk-worldbuilding/{SKILL.md,references/budgets.md}` (read)
- https://devforum.roblox.com/t/let-there-be-unified-light-unified-lighting-is-fully-live/3401512 (search summary: Technology-to-style mapping)
- https://devforum.roblox.com/t/prioritizelightingquality-not-accessible-in-scripts/3826475, https://devforum.roblox.com/t/lightingstyle-property-keeps-changing-to-soft-only-in-game/3437295, https://devforum.roblox.com/t/lightningstyle-gets-changed-to-soft-on-roblox-player/3590527 (search summary)
- https://devforum.roblox.com/t/roblox-lighting-modes-what-do-i-use-for-my-game/1687174, https://devforum.roblox.com/t/future-is-bright-on-android-is-fully-rolled-out-client-beta/3235808, https://devforum.roblox.com/t/future-lighting-looks-fine-on-pc-but-way-too-bright-on-mobile/1087420 (search summary: quality-level fallbacks, staff reply on level 4 and 30 FPS)
- https://devforum.roblox.com/t/in-mobile-neon-part-doesnt-glow/2333429, https://devforum.roblox.com/t/bloom-vs-color-correction/494805, https://devforum.roblox.com/t/why-is-the-bloom-on-my-game-so-bright/518435 (search summary)
- https://devforum.roblox.com/t/changing-lighting-on-the-client-side-when-stepping-into-different-zones/3597161, https://devforum.roblox.com/t/tweens-on-atmospheredensity-are-not-smooth/3216997, https://devforum.roblox.com/t/atmosphere-bugs-out-when-transitioning-using-tweens/2841565, https://devforum.roblox.com/t/choppy-rendering-when-tweening-properties-of-lighting-and-other-lighting-instances/4525441 (search summary)
- https://devforum.roblox.com/t/compatibility-lighting-becomes-retro-tone-mapping-sunset-migration/3128560, https://devforum.roblox.com/t/ambient-occlusion-settings/4044364 (search summary)
- https://devforum.roblox.com/t/improve-lighting-step-by-step/1387033, https://devforum.roblox.com/t/guide-to-lighting/2764787 (search summary)
- No evidence found: an official per-quality-level feature list; an official 2026 lighting feature announcement beyond unified lighting; community-agreed post-processing values (third-party "preset" pages were SEO mirrors and were ignored); a documented default for `LightingStyle` on the class page.
