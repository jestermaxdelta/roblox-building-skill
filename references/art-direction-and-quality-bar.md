# Art direction and the quality bar: a cohesive game that does not look generic

What this is: the cross-discipline guide to the owner's bar ("very high-quality, cohesive, put-together, avoids the generic AI slop look"). It names what gives a Roblox game away as generic or AI-made in every discipline, gives the method that produces one distinct look across models, world, light, UI, effects, motion, sound and words (genre defaults and named directions in §4, a several-artists system in §8), sets the bar per release tier, and gives a review procedure and an ordered six-week rescue plan for a live game. Open it before the first asset of a new game, at every milestone review, when feedback says "looks like every other game" or "looks AI", and before commissioning art. It owns direction, the style bible (template in §6) and review; depth stays with the discipline files and is linked, not repeated: `blender-modeling-craft.md` (asset numbers and the per-asset rubric), `art-pipeline-blender.md` (export, import, collision), `lighting-and-atmosphere.md`, `level-design-worldbuilding.md`, `ui-design-figma.md`, `vfx-and-juice.md`, `animation-and-rigs.md`, `audio-sfx-music.md`, `icons-thumbnails-and-store-page.md` (icon, thumbnail and store-page recipes, tells and rubric), `growth-and-marketing.md` (ads and channels). Reference images: `visual-library/environments-and-maps.md`, `visual-library/models-props-characters.md`, `visual-library/lighting-and-mood.md`. Tags: `[official]` Roblox, `[community]` forum or named practitioner, `[lihfolk]`, `[VS]` version-sensitive, `[house]` house rule or estimate.

Contents: Fast routes · 1 What generic means · 2 Slop tells by discipline · 3 Pillars to art direction · 4 Choosing the direction (intake, genre defaults and directions, style tiers, capacity) · 5 Reference board · 6 Style bible: template, measurable rules, tie-ins, palette scan · 7 Quality bar by tier · 8 Art review procedure, several artists on one look · 9 AI tools without slop · 10 Raising a live game: ordered passes and a six-week plan · 11 Level-up table · Review gate · Sources

## Fast routes

Read only these for the commonest tasks (about 200–340 lines each). AD = this file, LA = `lighting-and-atmosphere.md`, LD = `level-design-worldbuilding.md`, BM = `blender-modeling-craft.md`, AP = `art-pipeline-blender.md`; library files are in `visual-library/` (env, models, light); sheets are `assets/reference/NN-*.png`.

| Task | Read exactly (file §section, …) | Look at (sheet numbers, library file and row ranges) |
|---|---|---|
| Give a new game its look | AD Fast routes, §1, §3, §4, §5, §6, §8 steps 1–2; LA §2, §12 | Sheets 18, 16; env §G rows of the genre (63–81) plus 1 and 54; light: the "start here" rows of the chosen mood |
| Make a generic-looking live game distinct | AD §1, §2, §4, §8, §10, §11; LA §12, §14 | Sheets 18, 16; env §G default rows (63, 70, 72, 75, 76) beside 1, 13, 16; light 1–2, 6 |
| Keep a team of artists consistent | AD §3, §4 "Style tiers", §6, §8 (with "Several artists, one look"), §10 six-week table; BM "Edges and shading", "Colour and value", "Concept to model", "Quality rubric"; AP "Texturing strategy", "Naming and hierarchy", "Asset acceptance checklist" | Sheet 18; models 1, 8, 10–11; env 44 |
| Fix an empty or confusing map | LD Start here, §1, §4, §5, §6, §7, §8, §16, §17, polish checklist; LA §2, §3 | Sheet 17; env 1–4, 6, 13–19, 23–24 and the genre's §G rows |
| Fix flat lighting | LA Start here, §1, §2, §3, §4, §5, §6, §8, §9, §11, §12, §13, §14 | Sheet 16; light 1–3, 6, 10, 16; env 28 |
| Model one prop to the bar | BM "The numbers", "Shape language", "Proportion", "Edges and shading", "Spending triangles", "Colour and value", "Recipes and budgets", "Concept to model", "Quality rubric"; AP "Asset acceptance checklist" | Sheet 18 (bevel and value panels); models 1–3, 8, then 16 and 25 (weak) and 17 (too realistic) |
| Build a first kit | BM "The numbers" (first table), "Edges and shading", "Recipes and budgets", "Quality rubric", "First kit walkthrough"; LD §8, §9; AP "Naming and hierarchy", "Modular kits", "Asset acceptance checklist" | Sheet 17 (avatar metrics); env 7, 11, 29, 44, 55; models 1, 8, 10–11 |

## Start here by level

| Level | Do these first | Ignore for now |
|---|---|---|
| Beginner | In order: run the defaults scan (§2, the code block) and fix what it prints. Fill the §4 intake, read your genre's default row, take one direction from the table as a starting point and run its two-day test. Write the three-decisions line (§3). Build a 20-image board with a label on every image (§5). Make one golden sample before any other asset | Rubric scoring, tie-in tables, tiers |
| Intermediate | Run §4 in full: default row from three competitors, two directions tested as hero assets, the line-up. Fill in the bible template with measurable rules and tie-ins (§6); run the palette scan. Build a beauty corner (§3). Run the four tests on 12 captures at each milestone (§8). Hold contractors to the bible and the rubric | Blind scoring panels |
| Expert | Blind one-screenshot tests with strangers; weakest-link scoring per discipline with caps; a motif audit across icon, UI, world and effects; the several-artists system (§8); bible versioning with family-by-family migration and the six-week plan (§10) | Nothing |

Terms: **generic** = could be swapped into another game unnoticed; **slop** = output nobody made a decision about, whatever tool produced it; **pillar** = one of the three promises the game makes; **golden sample** = the finished asset every new asset is held beside; **beauty corner** = a small area finished to final quality in every discipline; **motif** = a small shape or pattern repeated across disciplines; **value** = lightness independent of hue; **tie-in** = a rule that makes one discipline inherit from another.

## 1. What "generic" means, and what it costs

Three causes produce the same look `[house]`: **defaults left in** (every other game has them too), **a template copied from one source** (the cube pet, the 2020 simulator lobby), and **averaged output** (generators and mixed asset packs, where nobody chose a rule). Working test: an asset or screen is generic when you cannot name three decisions that make it this game's. Hand-made work fails it as easily as generated work: the bar is decisions, not tools.

| Evidence | Detail |
|---|---|
| Similar or mismatched games lose discovery `[official]` | Since December 2024, experiences whose thumbnails, title, description or place files closely resemble existing ones are not prioritised in Home and Charts and rank lower in search; metadata that does not match the content is not recommended |
| Default thumbnails lose Home `[official]` | From 2026-10-19 only games with a custom thumbnail receive homepage recommendation impressions. The most-liked replies ask for AI thumbnails to be excluded as well `[community]` |
| Developers read the tells within a minute `[community]` | A "why does nobody play my well-made game" thread (143 likes): top replies list an AI thumbnail and description, `print` output left in the console, assets from a premade kit, stiff animation, overlapping UI and a rushed lobby |
| Players say they skip `[community: search summary, not re-checked]` | Search results for Reddit threads and a petition report players avoiding games with AI icons, with dissent. Reddit is not readable from here, so treat it as a likely trust cost, not a measured one |
| AI meshes fail technically `[community: Liz Edwards via Game Developer]` | Baked-in lighting, a texture projected from one 2D image with its artefacts, dense automatic topology, jumbled auto-unwrapped UVs, about 50,000 triangles for a crate that needs about 500, asymmetry, limbs fused into blobs that cannot be posed. No single trait proves origin |

## 2. Slop tells by discipline

Each row: the tell, why it reads as generic, the fix and where the fix is specified.

| Discipline | Tell | Why it reads as generic | Fix |
|---|---|---|---|
| Models | Unbevelled boxes, default 32-segment cylinders | Every first mesh has them; razor edges catch no light | One bevel width per viewing band, segments from the sagitta table (`blender-modeling-craft.md`) |
| Models | Cube pet with a face decal | Traced from one hit; forum replies to such pets joke about the originator's lawyers `[community]` | Change the primary mass and proportions, not the decal; roster test |
| Models | Lumpy, slightly asymmetrical forms, fused limbs, even dense triangles | The generator look: no silhouette decision, cannot be rigged | Authored in Blender; half-plus-mirror; triangle-spend and symmetry gates |
| Models | Real-world proportions (thin rails, small wheels, narrow car) | Vanish or look weak at phone size; the standard forum note on low-poly cars `[community]` | Exaggerate in pairs from the proportion table |
| Models | One PBR hero beside a flat-colour kit; equal detail everywhere | Two sources or two authors; no hierarchy | One texturing method; 60:30:10; one focal feature per asset |
| Textures, materials | Built-in materials at default scale on visible surfaces; `Plastic` everywhere | Recognisable from thousands of places | Palette atlas or trim sheets; `SmoothPlastic` only as the flat-colour carrier |
| Textures, materials | Photo or generated textures with baked highlights, noise, mixed sharpness | Baked light fights scene light; texel density jumps between neighbours | One texel density; no baked lighting; closed material list |
| Textures, materials | Pure primaries and a rainbow of them; gloss or Neon on everything | Colour-picker defaults; "everything glows" | Palette with value and saturation ranges (§6); emissive only on listed classes |
| Environments | Flat ground, equal heights, props sprinkled evenly, one tree at one scale | No composition; the first thing forum reviewers name `[community]` | Focal hierarchy, stepped heights, clumps, 3–5 variants (`level-design-worldbuilding.md` §6) |
| Environments | The simulator-lobby template: orange cliffs with green caps, checker ground, floating SHOP text | One 2020 template repeated | Start from the map brief and the three decisions; landmark and palette of your own |
| Environments | Floating slab that "just ends", default sky behind it | Boundary and backdrop never designed | Diegetic edge, backdrop mesh, authored sky, atmosphere |
| Environments | Pack trees beside a detailed house; one building repeated in a visible row | Style seam; reviewers call out repetition `[community]` | One kit from one bible; reuse by rotation, roofline and palette swap |
| Lighting | Noon sun, default sky, no grade; or the genre preset pasted unchanged | The most recognisable defaults on the platform | The §12 row your direction names, its deviation step and white-cube balance (`lighting-and-atmosphere.md` §2, §12) |
| Lighting | Blown whites, haze of bloom, sun rays always on | "Effects on" mistaken for quality | Safe ranges (its §6) |
| Lighting | One tint over everything (the all-blue city); black "horror" | Hue replaces value structure; darkness hides the game | Value bands first; night by hue, not darkness |
| UI | Default-looking frames and fonts, mixed icon packs, a hit game's skin, rainbow gradients | Defaults, several sources, or one source | Tokens tied to the bible (§6); full list in `ui-design-figma.md` |
| UI | Generated panels and buttons: wobbly bevels, stroke weight changing along one edge, garbled glyphs | Cannot be 9-sliced or restated as tokens; no two elements match | Design in Figma from tokens |
| Icons | Rendered-plastic grinning avatar, extra fingers, lettering that melts, a style absent from the game | The current generator look; mismatch with the first minute | Compose from the game's own Blender assets and a Figma layout |
| Icons | Item icons from several packs or emoji | Mixed line weight and perspective | Viewport renders of the real meshes, one camera and light rig for all |
| Thumbnails | Default or auto image | Not eligible for Home recommendations `[official]` | Captures from real zones |
| Thumbnails | Off-model art; a clone of a hit's layout, pose and colours; "FREE" text walls | Mismatch and similarity both reduce exposure `[official]` | Real captures from review cameras; recipes and the full tell list in `icons-thumbnails-and-store-page.md` |
| VFX | Default particle texture; legacy `Fire`, `Smoke`, `Sparkles`, `Explosion` | Engine defaults | Authored textures and Blender effect meshes (`vfx-and-juice.md`) |
| VFX | A different colour logic per effect; white additive blobs | No effect language; bloom soup | Effect palette and shapes from the bible (§6) |
| Animation | Default idle and walk on custom NPCs; sliding NPCs; linear tweens | "Clumsy and stiff" is named in reviews `[community]` | Authored idle, anticipation and overshoot; easing tokens (`animation-and-rigs.md`) |
| Animation | Mocap-like clips beside snappy cartoon clips | Two sources | One timing family per game |
| Audio | Default death, footstep and jump sounds; silent UI; one library click | Engine and library defaults | A UI sound set from one material family; replace character sounds (`audio-sfx-music.md`) |
| Audio | Over-used library tracks; loops with no structure; unmixed levels | Heard in many games; no mix decision | A music brief per zone; buses and loudness targets |
| Writing, naming | Title as tag soup with emoji; chatbot description ("embark on an epic journey", feature bullets that are not in the game) | Clone naming; mismatch | Title is the name; description says what you do in the first minute |
| Writing, naming | "Zone 1", "Epic Sword", "Dummy"; placeholder and "coming soon" boards; mixed capitalisation | No voice | A 30-word lexicon from the fantasy; two voice rules; one string table, proofread |
| Code-visible | Default player list, backpack bar, health bar, loading screen, proximity prompt, chat styling, cursor | The engine's own UI beside yours | Decide each: restyle, replace or hide (block below) |
| Code-visible | `print` spam in the client console; visible SpawnLocation decal; ForceField sparkle; NPC name and health bars; the default fall-apart death | Seen by players and by every developer who presses F9 | Sweep before each release |

Defaults to decide on purpose `[official, VS]`: `StarterGui:SetCoreGuiEnabled` per `CoreGuiType` (PlayerList, Health, Backpack, EmotesMenu); `ReplicatedFirst:RemoveDefaultLoadingScreen()` after your own screen is up; `ProximityPrompt.Style = Custom` with `ProximityPromptService.PromptShown`; `TextChatService` window, input-bar and bubble configuration objects; `UserInputService.MouseIcon`; `Humanoid.DisplayDistanceType` and `HealthDisplayType` on NPCs; `SpawnLocation.Duration` (0 removes the ForceField) and an invisible SpawnLocation inside a Blender pad; the character sound script in `StarterPlayerScripts` (replace it with your own of the same name `[community]`). Hiding a default without replacing its function (no player list, no way to see friends) is worse than the default.

```lua
--!strict
-- unexecuted sketch, Studio command bar in Edit mode, read-only: counts engine defaults a player can see or hear
local ScriptEditorService = game:GetService("ScriptEditorService")
local DEFAULT_PARTICLE = "rbxasset://textures/particles/sparkles_main.dds" -- class default in the engine API dump, 2026-11 [VS]
local DEFAULT_GREY = Color3.fromRGB(163, 162, 165)
local found: { [string]: number } = {}
local function note(kind: string)
	found[kind] = (found[kind] or 0) + 1
end

for _, service in { workspace, game:GetService("ReplicatedStorage"), game:GetService("StarterGui"), game:GetService("StarterPlayer"), game:GetService("ServerScriptService") } do
	for _, inst in service:GetDescendants() do
		if inst:IsA("Fire") or inst:IsA("Smoke") or inst:IsA("Sparkles") then
			note("legacy effect instance")
		elseif inst:IsA("ParticleEmitter") and inst.Texture == DEFAULT_PARTICLE then
			note("default particle texture")
		elseif inst:IsA("SpawnLocation") and (inst.Transparency < 1 or inst:FindFirstChildOfClass("Decal") ~= nil) then
			note("visible SpawnLocation")
		elseif inst:IsA("Humanoid") and inst.DisplayDistanceType ~= Enum.HumanoidDisplayDistanceType.None then
			note("NPC with default name or health display")
		elseif inst:IsA("BasePart") and inst.Transparency < 1 and inst.Material == Enum.Material.Plastic
			and not inst:FindFirstChildOfClass("SurfaceAppearance") then
			note("default Plastic material")
		elseif inst:IsA("GuiObject") and inst.BackgroundTransparency < 1 and inst.BackgroundColor3 == DEFAULT_GREY then
			note("default grey GUI background")
		elseif inst:IsA("LuaSourceContainer") and string.find(ScriptEditorService:GetEditorSource(inst), "print(", 1, true) then
			note("script that prints")
		end
		if (inst:IsA("TextLabel") or inst:IsA("TextButton") or inst:IsA("TextBox")) and string.find(inst.FontFace.Family, "SourceSansPro", 1, true) then
			note("default font")
		end
		if inst:IsA("Model") and (inst.Name == "Dummy" or inst.Name == "Rig" or inst.Name == "Model") then
			note("default-named model")
		end
	end
end
local lighting = game:GetService("Lighting")
if not lighting:FindFirstChildOfClass("Sky") then note("default sky") end
if not lighting:FindFirstChildOfClass("ColorCorrectionEffect") then note("no grade") end
for kind, count in found do
	print(string.format("%4d  %s", count, kind))
end
```

The house-rule scan in `checklists.md` (primitive Parts, marketplace and generated assets, collision) is separate and comes first.

## 3. From pillars to art direction

1. **Three pillars, three visual consequences.** Take the pillars from the one-pager and write what each forces on the look. Example: "cosy" → rounded primary shapes, warm key, nothing darker than value 20; "collect everything" → every collectable identifiable at 64 px by outline; "show off" → the avatar and the pet are the most saturated things on screen, so the world stays under saturation 45.
2. **The three-decisions line.** "This is the game with ___ shapes, a ___ palette and the ___ motif." If a competitor could sign it, rewrite it. Weak: "chunky low-poly shapes, a bright palette and a star motif" (every simulator). Strong: "everything is sewn felt with no straight edge longer than 2 studs, nine dusk colours with one mustard accent, and a cross-stitch on seams, UI corners and hit effects".
   **Line-up test before production**: the genre default row, the two-axis rule and the two-day test are §4 steps 2–4. If the line fails them, change shape, edge, material or light first, palette last.
3. **One motif, repeated across disciplines.** A knot carved on a pauldron that returns on the belt, the bracer and the anvil is what makes a character read as one design (`visual-library/models-props-characters.md`). Put yours on a model trim, a UI corner, the icon and one effect shape.
4. **Rules can carry meaning.** Team Fortress 2 gave one team warm colours, natural materials and angular geometry and the other cool colours, industrial materials and orthogonal forms, kept characters identifiable as pure silhouettes, and omitted high-frequency detail where possible `[community: Valve, NPAR 2007]`. Use the same device for factions, zones or rarity.
5. **Find the style by making, then freeze it.** Practitioners describe the same loop: a small prop test before the kit; one or two objects pushed to final to lead everything else; about twenty objects, a critique of the whole, one or two iterations, then hold `[community: Gonçalves, Lucas, Özben on 80.lv]`. Write the bible from that golden sample, not from intentions. Make the golden sample a set of three (one small prop, one kit module, one character, creature or interactable) so every scale has a reference to stand beside. The same rule holds per family `[house]`: finish and approve one hero piece of a kit, pet line or enemy set (rubric 8+, in the place, under the preset) before producing its siblings, so a wrong bevel or palette is fixed once, not twenty times.
6. **Build a beauty corner before production.** About 30 × 30 studs at final quality in every discipline: kit pieces, lighting preset, one interactable with its prompt, the HUD over it, one effect, one sound. It is the capture for the one-screenshot test (§8) and the brief for everyone who joins later.

## 4. Choosing the direction: intake, the genre default, a style the team can sustain

A process without a decision ships the genre's average: the §12 lighting preset, sheet 18's examples and a safe palette, which is what every other agent and template produces too. This section ends in one named direction with numbers. Method `[house]`; defaults read from the captures in `visual-library/environments-and-maps.md` §G and the market scan.

1. **Intake** (written, ten minutes). Fantasy and tone in three words; audience (age band, phone share, session length); the three competitors the game is mistaken for (beside it on Home, in search, or named by players); what the team can sustain (people × art hours a week, and the style tier below they can hold for 200 assets); what cannot change on a live game (footprints, pad positions, avatar scale).
2. **Write the genre default.** Capture the first frame of those three competitors (no access: their official thumbnails through `thumbnails.roblox.com`, plus the §G rows) and fill one row on the seven axes of the table below (palette, value key, shape, edge, material, light, motif). That row is what "generic" means for this game.
3. **Pick a direction that differs from the default on at least two named axes**, one of them shape, edge, material or light. Palette alone never counts: it is the cheapest thing for the next clone to copy. Each genre below has a default row and three or four directions with the trade-off; any other genre gets the same treatment from its three competitors.
4. **Test it in two days, before the bible.** One hero asset (the most-seen interactable: the dropper, the pet, the checkpoint) and one 20 × 20-stud vignette in the direction, under its light, captured on the phone. Line-up: the capture beside the three competitors' first frames at 320 px, shown for 3 s to two people outside the team; pass when both pick yours afterwards and name what differs, and greyscale shows three value bands. If two directions pass, take the one the team can sustain, not the prettier.

No access to the game: ask for two captures (first frame, core action) and the three competitor names, derive the default row from the competitors' thumbnails, and present two directions with trade-offs. Never fill the blanks with a table row or a sheet example: the owner chooses (taste is theirs).

| Genre · direction | Palette: value key and hex anchors (HSV V) | Shape and edge | Materials | Light (start row in `lighting-and-atmosphere.md`, then the change) | Motif | Trade-off · who sustains it |
|---|---|---|---|---|---|---|
| **Tycoon · default** (env 63–66) | Grass V55–75, brick #845B50, concrete #C7C4BF; player colour on everything | Lots in a row on a road or a walled flat slab; default boxes | Photo brick, wood, glass at real scale, or built-in materials | Noon in play; warm dusk with lamps in promo art (the §12 golden-hour row) | None | What the line-up already shows |
| Tycoon · Tin-toy workshop | High key: felt ground #3F6E5A (43), tin cream #EFE6D2 (94), red #C8473A, cobalt #2F5D8C; brass #C9A04A only on buyables; #22303F only in gaps | Pressed tin: rounded rectangles, rolled rims, rivets; round bevel 4–6% of size, 2 segments | Painted tin (roughness 0.4), brass (metal), felt | §12 simulator row at Brightness 1.8, sun 45°, fill raised to key:fill 1.5: a soft studio | Wind-up key on machines, UI corners, the buy effect | Reads young; flat colour and one atlas, 1–2 generalists |
| Tycoon · Overcast works | Greys V35–60: steel #4A535C, floor #6B6E70, concrete #8A8D8F; safety orange #F28C28 (95) only on buyables | Square, heavy; crisp one-segment chamfers 1–2% | Concrete, painted steel, rubber belt, glass on one trim sheet | §12 overcast row plus 6–8 warm practicals (255,170,90) on machines | Hazard chevron on trims, belts, UI stroke | Drab if the practicals are cut; needs Realistic and a light budget; one lighting-literate artist |
| Tycoon · Lantern night market | Low key V25–45: indigo #1E2A44, teal ground #2F5E66, wood #6B4A36; lacquer red #A8322D; paper #F6E7C1 glowing on buyables | Tall narrow stalls, canvas awnings, sagging strings; soft bevel 0.1–0.2 | Canvas, lacquered wood, paper, rope | §12 roleplay-night row at ClockTime 20, ExposureCompensation +0.3; one shadowed light per stall | Paper lantern | Dim phones need the value floor held; stands out among noon tiles; 2–3 artists with one lighting owner |
| Tycoon · Cut-paper diorama | Sage ground #7E9A7A (60), paper #F3EBDD (95), kraft #D9B98C; coral #E8735A on buyables; ink #2B2B3A edges | Extruded flat silhouettes 0.4 thick, layered like a pop-up book; no bevel | Matte paper only, no textures | §12 overcast row with both ambients lifted 40 per channel | Torn edge | Depth only from layering and value; cheapest per asset; solo |
| **Simulator · default** (env 69–71) | Saturated primaries at high value: red #D85846, green #3BD776, sky #CFF7E4 (V80–97, saturation 65–75) | Stacked box bases, lanes, voxel or faceted props, cube pets, floating text | Flat plastic, studs | Noon, high fill, bloom | The currency number | — |
| Simulator · Gouache storybook | Saturation capped at 50 except interactables: ground #7F9470 (58), slate #4E5A6B, terracotta #B9654A, ochre #D7A24A, cream #F2E6C9; teal #2FB5A8 on interactables | Organic, tapered, leaning 2–4°; soft bevel 3–6% | One painted gradient atlas | §12 golden-hour row moved to ClockTime 9 with a cooler fill | Brush swirl in clouds, trails, UI | One painter must own the atlas; medium cost |
| Simulator · Night arcade | Low key V15–40: #141826, #262C44, floor #3A4566; cyan #3FF0FF and magenta #FF4FD8 only on interactables and rewards | Geometric, sharp chamfers; light strips as trims | Matte dark plastic, glass, emissive strips | §12 neon-city row | Pixel grid | Glow must live in emissive shape, not bloom (bloom drops at low quality); small team |
| Simulator · Matte clay | Low saturation (15–25): ground #8A7F99 (60), mint #BFD8C5, lilac #C9C3E6, peach #F2C9B6, shadow #4A4458; one saturation spike on interactables | Pillowy: round bevel over 8%, no straight edge over 2 studs | Matte clay (roughness 1), no specular | §12 overcast row at Brightness 1.6, ClockTime 11 | Thumbprint dimple | Hierarchy without saturation is hard; cheapest; solo |
| Simulator · One hue per world | Each world one hue plus near-black and off-white: ground #2E3F8A (54), hue #1E3FE0, #0B0E1A, #F4F4F0; the next world red | Hard graphic shapes, crisp chamfers | Flat colour, one emissive | §12 PvP row, `ColorShift_Top` tinted to the world hue | The world's sigil | Strong thumbnails; monotony inside a world, so keep worlds short; 1–2 people |
| **Obby · default** (env 72) | One saturated hue per section, neon kill bricks, grey shell; V60–90 | Floating slabs over the default sky | SmoothPlastic, Neon | Noon | None | — |
| Obby · Brutalist with one signal | Concrete V37–72: #5E5C58, #8C8984, #B8B5AE; landing tops #FFD23F; #FF3B30 only on hazards | Monoliths, big flat landing faces, crisp chamfers | Board-marked concrete trim, painted metal | §12 obby row at ClockTime 8.5; tops lighter than sides by value so it holds without shadows | Stencilled stage numbers | Austere; a 12–15-piece kit; solo |
| Obby · Craft table | Dark kraft ground #8E6A45 (56), kraft #C49A6C, tape #EADFBF, marker blue #2E5AAC; marker red #D2423A on hazards | Boxes 2–4° off square, tape strips as trims | Corrugated card, masking tape, felt | §8 interior: one warm desk-lamp SpotLight key, cool window fill | Masking-tape strip | Needs giant props to sell scale; 2 people |
| Obby · Backlit silhouettes | Sides #141019 (10), tops #5A4A6E (43) with a glowing rim #FFE3A3; sky #F49A5B to #6A4C93 | Irregular organic slabs; no bevel (the outline is the read) | Matte plus one emissive edge | §12 backlit-dusk row | Glowing rim | Depth is hard: blob shadows mandatory; cheapest geometry; solo |
| **Horror · default** (env 76, 80) | Warm dark wood V5–55 (saturation 45–68), or grey-green fog V20–70 under saturation 50 | Realistic rooms and forests | PBR textures | Night or fog; a flashlight | The monster's face | — |
| Horror · Bright liminal (env 77) | High key walls #EDE4CF (93); floor tiles #958E7E (58); water #0E8A94, deep #124D50 | 2-stud tile grid, long sightlines, repetition | Tile, still water, fluorescent tubes | §12 fluorescent-liminal row | Tile grid | Fear must come from sound, emptiness and repetition; cheap kit; solo |
| Horror · One hue, lanterns (env 79) | Red family V7–76: #130503, floor #6A2418 (42), #7A2D21, highlight #C2715F; lanterns (255,170,110) | Traditional architecture, symmetry, one-point corridors | Lacquered wood, paper screens | §12 horror row with ambient and colour shift tinted red; lanterns as practicals | Paper lantern | Hue fatigue: change hue per chapter; 2+ artists |
| Horror · Toon cast in a dark building (env 78) | World V5–35: #0E0D0B, #2B281C, floor #5A4D38; characters and pickups V100: #FFD23F, #FF5FA2, #3FC5FF | Round flat-shaded characters; plain institutional boxes | Flat-shaded cast, plain materials | §12 dungeon row with cool fluorescent pools | The cast | Needs a strong character designer; the world is cheap |
| **Roleplay · default** (env 73–75) | White render #D8D8D8, grey asphalt, lawn #869B7C, blue-grey glass, palms | Modern suburb at real proportions, chunky trees | Real-world materials | Noon | None | — |
| Roleplay · Mediterranean morning | Whitewash #F2EEE6, plaster shade #D9CBB5, terracotta #C0643C, cobble ground #8E8170 (56), cypress #3E5B3A; cobalt #2E6DB4 shutters mark districts | Rounded plaster masses, arches, stepped hill heights; bevel 3–5% | Plaster, terracotta tile, painted wood, stone | §4 day keyframe at ClockTime 9.5 | The arch | Hills need solid Blender ground; 2–3 people |
| Roleplay · Rainy blue hour | Cool V35–50: asphalt #474F5E (37), brick #5C3F3A, concrete #6E747E; sign accents #FF6B4A, #4AD9FF | Tall narrow facades, awnings | Wet asphalt (roughness 0.2), brick, glass, neon tube | §4 dusk keyframe at ClockTime 19, Realistic, `EnvironmentSpecularScale` 1 | Neon lettering | Wetness is specular, lost on low end: paint reflections as value strips; a lighting owner |
| Roleplay · Retro-future pastel | Terrazzo ground #8F8A84 (56), mint #9ED9C8, salmon #F2A28C, cream #F5EBD7, chrome #B8C0C8, charcoal #3A3F47; #FFC93C accent | Boomerangs, capsules, large radii | Enamel, chrome, terrazzo | §12 simulator row at Brightness 2, ClockTime 11 | Starburst | Theme-locked (modern items clash); flat colour, 1–2 people |

Every row is a starting point to push, not a skin to apply: two games that both pick "Tin-toy workshop" converge as surely as two on noon. Grounds sit at value 35–60 so black and white avatars both separate (`blender-modeling-craft.md` "Colour and value"). Fill the bible (§6) from the tested hero asset, with your own hexes measured from it.

### Style tiers: what the team can sustain

A style is what the team can make two hundred times at the same quality. Sable's flat-shaded desert was chosen because the team could not build a detailed open world: the look had to be quick to produce, quick to iterate, consistent and still stand out, and readability was then recovered with layered lighting, distance fog and line work `[community: Kythreotis, GDC 2022]`.

| Style | Cost per asset | Low-end phone (no shadows) | Cohesion risk | Generic risk | Choose when |
|---|---|---|---|---|---|
| Flat colour, chunky bevels, palette atlas | Lowest | Strong: the look lives in shape and colour | Low | High unless shapes and palette are distinctive | Solo or two people; many assets |
| Faceted low-poly | Low | Needs an angled sun or per-face value jitter | Low | High: the 2019 "low poly" look | Rocks, crystals, terrain inside another style |
| Gradient atlas or simple hand-painted | Medium | Strong | Medium: painting skill varies between people | Low | One consistent painter on the team |
| Stylised PBR with trim sheets | High | Weak: depends on Realistic lighting | Medium | Low | Interiors, horror, a dedicated artist |
| Voxel | Low | Strong | Lowest: the grid enforces it | Medium | Building or mining games; strict grid discipline |
| Realistic PBR | Highest | Weakest | High | Low | Not with a small team |

- **Capacity check** `[house]`: assets needed × hours per asset at rubric score 8 ≤ art hours before launch. If not, cut asset count or drop a style tier; never drop the score. Modelling-only times from one production vault: rock 20–45 min, crate or barrel 20–40 min, stylised weapon 1–3 h `[lihfolk]`; one artist built a 12-piece island kit in three days `[community: Lucas]`. Starting figures at score 8, including bevels, palette, export, the in-game check and one fix round, flat colour or atlas `[house]`: small prop 1–2 h, kit module 2–4 h, medium prop or machine with a moving part 4–8 h, tree 2–4 h, pet or creature without rig 6–12 h, hero landmark 12–24 h; double them for stylised PBR. Replace them with the measured time of your own golden samples in week 1.
- **Limitation as style.** Pick two or three hard limits and enforce them everywhere (a 12-colour zone palette, no textures, one bevel width, no outlines, one material idea such as "everything is folded paper" `[community: Lucas]`). Constraints kept everywhere beat detail.
- **Less detail, better read.** At gameplay distance small detail reads as noise `[community: Koepp]`; areas of low detail are what make the detailed focal point draw the eye `[community: Barrett]`.
- **Do not raise the detail level mid-production.** A team that used extra time to add painted folds, edge highlights and AO to new assets found them clashing with the earlier flat ones `[community: Epistory team via Game Developer]`. Version the bible: a change ships as a new version signed by one named owner, with the old and new golden sample side by side and the list of families to migrate. Migrate whole families or not at all (§10).
- **Free distinctiveness**: a proportion rule, a palette, a motif, a lighting key, one material idea. None costs triangles.

## 5. Reference board

| Question | Rule | Basis |
|---|---|---|
| How many | 20–40 images for the game, 3–9 per asset, 3–5 "not this" images | `[house]`; per asset keep the on-target, too-realistic and too-blocky triple `[lihfolk]` |
| From where | At least 40% real world (materials, architecture, plants, places); shipped games from three or more titles; film or illustration for light and colour; your own sketches | Boards in published breakdowns mix city photos with target-style game shots, and keep mood references apart from structure references `[community: Klein, Novart]`; Roblox's curriculum board is five real-world photos `[official]` |
| How organised | Sections: Scene, Props, Light, Palette; or by purpose (design, mechanism, wood, metal); per-asset photo rows for an interior | `[community: Blinov, Bernert, Tsiflas]` |
| What to extract | One label per image (SHAPE, PALETTE, LIGHT, MATERIAL, LAYOUT or MOTIF) and one sentence saying what is taken. No label, no place on the board | `[house]`; the curriculum names the elements it takes: lush foliage, rounded frames, rectangular concrete forms `[official]` |
| Palette | Pixelate the concept or key reference to read its real palette, then write values | `[community: Blinov]` |
| Avoiding one source | No more than a third of the board from one title; never take shape, palette and motif from the same image; put the reference beside the blockout and change the primary shape if a stranger names the source | `[house]`; similarity is demoted `[official]` |
| Never on the board | A single hit game as the target; generated images as targets (they average styles and carry artefacts); marketplace previews | `[house]` |

The top-liked forum answer to "how are simulator pets made" starts by exporting another game's pets as the reference `[community]`. That is how the cube-pet look spreads, and it copies protected work: study proportion and construction, then change the primary shape. Tools: PureRef, Miro or a FigJam board. Third-party images stay out of the repository; keep a link list.

## 6. Style bible: measurable rules and tie-ins

The bible is one page, so it fits beside the viewport and two artists (or two agents) build one world. Fill it in from the golden sample. Sheet `assets/reference/18-style-bible-one-pager.png` shows the blank page and two opposite fillings of one brief: examples of the range, never values to ship.

```markdown
# <Game> style bible v<N> (<date>, owner)
Fantasy in one line:            | Mood words (3):
Three decisions: ___ shapes, a ___ palette, the ___ motif (passes the line-up test)
Golden samples: <prop>, <kit module>, <character or interactable>; every new asset is held beside one in Studio
Palette (hex): base 8–12 ...    | accents 2 ... (accents only on things players can use)
Value rule: ground V __–__, structures one band away, interactables lightest or a saturation spike
Shape language: dominant ___, accent ___; big:medium:small = 60:30:10; taper and lean rules
Proportions vs both avatar proxies: door __ studs, counter __, step rise __, handle thickness ≥ __
Bevel width by viewing band: hand __, character __, engagement __ studs; segments __; weighted normals always
Grid: architecture __ studs, props __ studs; pivot rule per class
Texturing method: palette atlas / trim sheets / mixed (state which classes use which)
Texel density: __ px per stud (or "none"); max texture __; unique bakes allowed: __ assets
Materials (closed list, 6–10): name and roughness range each; metalness 0 or 1; emissive only on __
Outline: yes / no; if yes, where it comes from and its colour
Wear and story: edge wear yes/no; grime direction; what never gets dirty
Lighting key: LightingStyle __, sun elevation __, key:fill __, one preset name per zone
Smallest readable detail: __ studs (anything smaller is deleted or enlarged)
Tie-ins: UI __ | icons __ | thumbnails __ | VFX __ | motion __ | audio __ | writing __
Banned (named things): unlisted colours, pure primaries, unbevelled boxes, baked text, one-off textures, Neon as decoration
Sign-off: asset rubric 8+ from a non-author, acceptance checklist passed, seen under this lighting on a phone
```

A rule belongs in the bible only if a reviewer can check it with a number or a side-by-side. What each line must say:

| Rule | Measurable form | Source of the number | Check |
|---|---|---|---|
| Palette | Hex list per role, with HSV value range and saturation cap per role (ground V 35–60, structures one band away, interactables lightest or a saturation spike); at most 3 hue families per zone plus neutrals; 2 accents | Value-band table in `blender-modeling-craft.md` | Greyscale capture shows three or more bands |
| Shape language | Dominant primitive (round, square or triangular) and its accent; big:medium:small about 60:30:10; taper and lean rules ("posts lean 2–4°") | §3 pillars | Silhouette sheet; roster test |
| Edge and bevel | One width per viewing band, 1 or 2 segments, weighted normals | Bevel table in the craft file | Bevels read at 15 and 40 studs on the phone |
| Texel density | One px-per-stud figure for textured classes; "none" for palette-atlas art. Start at about 50: the docs' 256² per 5 × 5 studs is 51 `[official]`, and a 720 px phone shows at most 64 px per stud at 8 studs | "Texturing strategy" in the pipeline file | Neighbouring assets equally sharp |
| Material list | A closed list of 6–10 named materials with a roughness range each; metalness 0 or 1 | Golden sample | Nothing in the place uses an unlisted material |
| Outline | Yes or no, once. If yes: where it comes from and its colour (the darkest palette neutral) | Inverted-hull outlines double triangles (craft file) | UI outline matches |
| Lighting key | `LightingStyle`, sun elevation, key-to-fill ratio 1.5–2.5, grade values, one preset per zone | `lighting-and-atmosphere.md` | White-cube capture |
| Smallest detail | A size in studs below which detail is deleted or enlarged | Pixel table in the craft file | Phone-size test |
| Banned | Named things, not adjectives: unlisted colours, pure primaries, Neon as decoration, baked text, one-off textures | §2 | Defaults scan and review |

Tie-ins make the other disciplines inherit from the model rules instead of being designed apart:

| Discipline | Inherits | Example line in the bible |
|---|---|---|
| UI | Corner radius family from the bevel character (soft toy bevels → large radii; crisp chamfers → small radii or cut corners); outline colour = darkest palette neutral; action colour = the interactable accent; panel surfaces from the neutral ramp; font chosen for the shape language | "Radius 16/24/32 px at 1080; 3 px outline #1F2430; accent #FFC53D only on things you can press" |
| Icons | Renders of the real meshes under the bible's light, one camera angle, one background family; never a second drawing style | "Item icons: 35° down, 30° yaw, key from top-left, flat rarity disc behind" |
| Thumbnails | Captured in-game from review cameras, composed with the same focal rules as a zone | "Hero landmark plus one avatar action; no text over 6 words" |
| VFX | Effect hues = the accents plus a white-hot core, at most two colours plus white per effect; shapes follow the shape language (round world: puffs and rings; angular world: shards and slashes); one timing family | "Hit: 2 shards + ring, accent and white, 0.25 s" |
| Animation | One timing family and overshoot amount shared by characters and UI | "Snappy: 0.12 s anticipation, 8% overshoot" |
| Audio | A material family for UI and world sounds that matches the material list (wood and felt for a cosy wooden world; glass and synth for a neon one); an instrument family per zone | "UI: soft wood taps; rewards: marimba" |
| Writing | A lexicon and two voice rules; naming patterns for zones, items and rarities | "Zones are places a child could draw; no numerals in names" |

The motif from §3 appears at least once in every row.

Check the palette line mechanically (flat-colour and atlas styles; textured parts are skipped):

```lua
--!strict
-- unexecuted sketch, Studio command bar in Edit mode, read-only: part colours that are not in the bible palette
local PALETTE = { "#2F4858", "#3E6F7A", "#F2B63C" } -- paste the bible's hex list
local allowed: { [string]: boolean } = {}
for _, hex in PALETTE do
	allowed[Color3.fromHex(hex):ToHex()] = true
end
local offenders: { [string]: number } = {}
for _, inst in workspace:GetDescendants() do
	if inst:IsA("BasePart") and inst.Transparency < 1 and not inst:FindFirstChildOfClass("SurfaceAppearance")
		and not (inst:IsA("MeshPart") and inst.TextureID ~= "") then
		local hex = inst.Color:ToHex()
		if not allowed[hex] then
			offenders[hex] = (offenders[hex] or 0) + 1
		end
	end
end
for hex, count in offenders do
	print(string.format("%5d  #%s", count, hex))
end
```

Zero rows is the pass for the "unlisted colours" ban; a long tail of near-duplicates (#3E6F7A beside #3F707B) means colours were picked by eye, not from the list.

## 7. Quality bar by tier

Observable criteria. "Rubric" is the 0–10 scale in §8; the asset rubric is the per-asset one in `blender-modeling-craft.md`.

| Criterion | Jam (days) | Soft launch | Competitive |
|---|---|---|---|
| House rules | Scan clean in everything published | Scan clean | Scan clean |
| Defaults (§2 scan) | Lighting and sky replaced; no `print` spam | Zero rows except deliberate ones written in the bible | Zero; the engine's UI is restyled or replaced where it shows |
| Bible | Three-decisions line, palette, one bevel width | Full template with numbers and tie-ins; golden sample | Versioned; beauty corner kept current; every contractor works from it |
| Assets | One golden sample at asset rubric 8; the rest 6+ | Every hero and store-front asset 8+; kit pieces 7+ | Heroes 9; everything else 8+; roster tests on all sets |
| Palette | One palette, no pure primaries | Value bands hold in greyscale in every zone | Colour script across zones; each zone owns one accent |
| Lighting | One tuned preset | Preset per zone; no-shadow test passes | Client zone profiles; night readable on a dim phone |
| UI | Tokens for colour, radius and font; no default frames | Every screen from the token set; icons from one family | Motion tokens; nothing a reviewer can call default |
| Icon and thumbnails | Custom capture | Captures that match the first minute; icon reads at 64 px | A tested set, refreshed with major updates |
| VFX, animation, audio | No engine-default effects or sounds on the core verb | Effect palette, authored idle, a UI sound set | A language for each, with the motif present |
| Writing | No placeholder text | Lexicon applied; description matches the first minute | Proofread string table; localisation-ready |
| Devices | Looks right in the phone emulator | Checked on the 3 GB Android phone | Checked at graphics level 1, 4 and maximum |
| Review score (§8) | No discipline under 5 | No discipline under 6, no caps | No discipline under 8; one-screenshot test passed with strangers |

## 8. Art review procedure

Asset-level review (the fixed critique order and paintovers) and zone-level tests live in the craft and level-design files. This is the whole-game review, run at each milestone and before any paid traffic.

1. **Capture, do not remember.** Judge at three distances `[house]`, because each answers a different question and a pass at one hides a fail at another: far (100 studs or more, or thumbnail size) for silhouette and zone identity; gameplay distance (15–40 studs) for value, colour and what can be used; close (about 8 studs) for edges, materials and seams. The pixel sizes behind those bands are in `blender-modeling-craft.md`. Twelve captures on the phone at automatic quality: first frame after spawn; the hub from its gate view; three review cameras per zone for two zones; the shop open; the inventory open; the core verb mid-action with effects; the darkest preset; the icon at 64 px and at tile size beside five competitors; the first thumbnail beside the first frame.
2. **Run the four tests on every capture.**

| Test | How | Pass when |
|---|---|---|
| Squint | Squint, or blur about 8 px at 720 p | You can still point at the focal object, the path and the primary button |
| Phone-size | View at about 320 px wide, or on the phone at arm's length | Every interactable, HUD number and the icon subject is identifiable |
| Greyscale | `ColorCorrectionEffect.Saturation = -1` | Three or more value bands; player, enemies and pickups each separate from the ground |
| One-screenshot | Show one unlabelled gameplay capture among five from the genre for 3 s; then show the world with UI hidden and the UI over a blank world | A stranger picks yours out afterwards and says what you do in it; both halves are recognisably the same game |

3. **Score each discipline 0–10 from the captures.** Anchors: 0–2 defaults, placeholders or a house-rule breach; 3–4 authored but inconsistent; 5–6 consistent and forgettable; 7–8 consistent, distinctive and passes all four tests; 9–10 identifiable from a cropped fragment, with nothing left to remove.

| Discipline | Look at | 5 means | 8 means | Capped at |
|---|---|---|---|---|
| Models | Silhouette sheet, asset rubric scores | On palette and bevelled; shapes are stock | Shape language visible in every family; rosters pass | 2 on any house-rule breach; 5 on a failed mechanical gate |
| Materials | Close-ups at 8 studs | One method, even density | Closed material list; nothing glows without a reason | 4 if two texturing methods meet in one view |
| Environment | Review cameras, blur test | Tidy, grounded, evenly dressed | One focal point per view; zones nameable from a blurred capture | 4 if the first frame shows no objective |
| Lighting | White-cube and no-shadow captures | A preset inside safe ranges | A mood per zone that survives graphics level 1 | 3 on default lighting or sky |
| UI | HUD over gameplay, shop, inventory | Token-consistent | Tied to the bible; recognisable with the world hidden | 3 if any default-looking frame ships |
| Icons, thumbnails | Tile-size line-up | Custom and accurate | Readable at 64 px; unmistakably this game | 0 if generated, off-model or default |
| VFX | Core verb capture, darkest zone | One palette | Shapes and timing follow the bible; never hides the action | 4 on any engine-default effect |
| Animation | Idle, core verb, a UI open | No sliding, no linear pops | One timing family; anticipation and follow-through on the core verb | 4 on default clips on custom rigs |
| Audio | 60 s of play, eyes closed | Every action has a sound; mixed | A recognisable sound family; the reward sound is the game's signature | 4 on default character sounds |
| Writing | Title, description, ten item names, three signs | Clean and accurate | A voice; names could not belong to another game | 3 on generated or mismatched copy |
| Cohesion | World-only and UI-only halves; motif count | Nothing clashes | The motif appears in four or more disciplines | Equal to the lowest discipline score + 2 |

4. **Rules.** The scorer is not the author. The game's art score is its lowest discipline, because cohesion is weakest-link. Write findings as what, where, why and how much, ranked by how many players see it over the hours to fix. Re-capture from the same cameras after the fix.

### Several artists, one look `[house]`

Three artists drift into three games through small choices nobody reviews. Make the cheap rules mechanical and review the rest weekly against fixed samples.

| Piece | Rule |
|---|---|
| Bible | §6 lines as numbers; one named owner signs each version; changes only at the weekly line-up |
| Golden samples | The three from §3 in `golden.blend` and in the place's `_Dev/Golden` folder (unpublished); every review places the new asset beside one |
| Shared sources | One `palette_vN.png` atlas and the trim sheets, versioned, in a shared folder; one `kit_base.blend` holding the `Scale_Ref` proxies, bevel and Weighted Normal presets and the `M_` placeholder materials. Artists append from it; nobody types a hex by eye |
| Ownership and names | Each artist owns whole families (all plot walls, all machines), never half of one; names per `art-pipeline-blender.md` "Naming and hierarchy"; one `.blend` per family (`kit_plot.blend`) so the roster renders it whole |
| Author check (before review) | `blender -b --factory-startup kit_plot.blend -P scripts/blender/check_asset.py -- --out build/check` exits 0 (names, transforms, UVs, class budgets, open edges; add `--symmetric <name>` for mirrored pieces); the same call with `silhouette_sheet.py -- --out build/sil --px 64 --roster` shows the new piece beside its family; the palette scan (§6) prints nothing for it in the test place |
| Reviewer check | A non-author, rotating so each artist reviews the other two; the bible owner breaks ties. Rubric in `blender-modeling-craft.md` beside the golden sample at 8, 15–40 and 100 studs under the zone preset on the phone, plus the acceptance checklist in `art-pipeline-blender.md`. Pass at 8 with no zero; a fail is written as what, where, why and how much |
| Weekly line-up (Friday, 30 min) | The twelve fixed captures and the four tests; every family's roster sheet; all of the week's new assets in one row beside the golden samples. Output: the fix list and any bible change |
| Drift alarms | Palette-scan rows; a `check_report.json` budget outlier; an outline that breaks its roster; two reviewers 2+ points apart on one asset (re-calibrate both on a golden sample) |

## 9. AI tools without shipping slop

The line `[house]`: generative tools may feed thinking; nothing they output ships. Everything a player sees or hears as art is authored: meshes in Blender (house rule 1), UI art, icons and thumbnails designed in Figma or by hand.

| Use | Allowed | Note |
|---|---|---|
| Mood exploration, layout thumbnails, naming brainstorms, critique of your own capture | Yes, throwaway | Keep the words (palette values, shape notes), not the pixels; then find real references for them |
| An agent writing Blender Python, export scripts, Luau | Yes | Scripted modelling is Blender authoring; it still has to pass the mechanical gates and the rubric |
| Generated meshes, textures, characters, scenes (including Studio's generators) | Never in a published place | Roblox presents Scene Generation as a way to "prototype and test ideas" `[official]`; use it only in a throwaway place |
| Generated UI art, icons, thumbnails, ad creatives | Never shipped | §1 evidence; accuracy rule in `growth-and-marketing.md` |
| Generated description or item text, unedited | Never shipped | Rewrite in the game's voice and check every claim against the build |
| Generated audio | See `audio-sfx-music.md` §3 for the licence risk | The cohesion argument below applies equally |

Why the line sits there:
- **Cohesion.** A generator cannot obey your bevel width, palette values, texel density or motif; each output is an average of other people's styles, so ten outputs are ten styles.
- **Technical.** Generated meshes arrive heavy, unsymmetrical, with baked lighting and unusable UVs (§1), which is the opposite of a mobile-first kit.
- **Discovery and trust.** Similar and mismatched metadata is demoted `[official]`; developers and many players call AI art low effort on sight `[community]`. Forum opinion is split on whether the tool or the user is to blame; the house bar does not depend on settling that.
- **Rights.** `team-business-legal.md` covers what a generator's terms and copyright notices mean for shipped content.

Scripted and agent-made work has its own tells: detail spread evenly, parts placed by eye, primitives floating beside the main mass, every asset the same complexity. The gates in `blender-modeling-craft.md` and the review in §8 apply to it without exception.

## 10. Raising a live generic-looking game: ordered passes

Order by visual gain per hour, then by how many players see the surface. Ship each pass through the safe-change steps in `audit-existing-game.md` §9, and re-capture the same twelve views after each.

| Pass | What changes | Typical effort | Why here |
|---|---|---|---|
| 0 | Baseline: twelve captures, §8 scores, defaults scan, house-rule scan | 2 h | Nothing else can be judged without it |
| 1 | Defaults sweep: lighting preset and grade, authored sky, default GUIs decided, default sounds replaced, `print` removed, SpawnLocation decals, NPC display, default names | Hours | Largest change per hour; touches every frame |
| 2 | Palette pass: recolour existing meshes and UI to one palette with value bands; remove pure primaries and stray Neon. No remodelling | Hours to a day | Fixes "muddy" and "rainbow" at once and sets the base for every later asset |
| 3 | Writing pass: title, description, names, signs | Hours | Cheap; removes the mismatch and chatbot tells |
| 4 | Spawn view: first-frame composition, one hero landmark, clutter removed, the worst assets in view replaced | Days | Every new player and every capture sees it (debt order 1 in the audit file) |
| 5 | UI skin: move every screen onto tokens tied to the bible | Days | On screen 100% of the time |
| 6 | Icon and thumbnails captured from the improved game | A day | Only now do they match the first minute |
| 7 | Effect and sound language on the core verb and the reward moment | Days | The most repeated moments |
| 8 | Kit replacement, one family at a time, by traffic: shop, main path, zones | Weeks | The house-rule debt track; whole families only, so old and new never sit side by side |
| 9 | Animation: authored idles, core-verb timing, UI motion tokens | Days | Last because it depends on final meshes and UI |

Choose the direction (§4) before pass 2, so the palette pass recolours toward it rather than tidying the old look; write bible v1 from the tested hero asset and hold passes 4–9 to it. Do not start pass 8 before passes 1–3: new kit under default lighting and a rainbow palette still reads as generic.

**Six weeks, biggest visual win per hour first** `[house]`. Passes run in parallel lanes; the order that matters is 1–3 before 8, and 4 before 6. Before week 1, export 14 days of the numbers this should move: Home click-through, play-through past the first minute, D1, average session (`analytics-and-discovery.md`). Each pass ships behind a Config flag whose default is the old look; at a few thousand CCU, run the first-frame and kit passes as Experiments.

| Week | Three artists (A, B, C) | Solo (about 20 art hours a week) | Measure at the end of the week |
|---|---|---|---|
| 1 Direction | Day 1 all: pass 0, §4 intake and default row. Days 2–3: each builds the hero asset in a different candidate direction. Day 4: line-up test, choose. Day 5: golden samples frozen, bible v1, passes 1–3 behind a flag | Pass 0, intake, two candidate hero assets (a day each), line-up test, bible v1, pass 1 | Twelve captures scored; line-up passed; hours per golden sample timed (capacity check, §4) |
| 2 Light and first frame | A: pass 4 (first frame, hero landmark, plot edge and backdrop). B: lighting from the §12 row plus the deviation, white-cube and no-shadow tests. C: hero piece of family 1 (the most-seen, such as plot structure) to 8+ | Passes 2–3, then pass 4 | First-frame capture passes the four tests; flag on for 50% of servers |
| 3 Families | A: hero piece of family 3 (hub or zone). B: hero piece and siblings of family 2 (machines). C: family 1 siblings. First weekly line-up | Hero piece and three siblings of the most-seen family | Every new piece 8+; rosters clean; memory and draw calls on the 3 GB phone not worse |
| 4 Families and UI | A: family 3 siblings. B: family 2 done. C: pass 5 (UI skin on tokens) | Pass 5 | World-only and UI-only halves read as one game; first-minute play-through vs baseline |
| 5 Verbs | A: rest of family 1 by traffic. B: pass 7 (effects and sounds on the core verb and reward). C: item icons rendered from the meshes | Pass 7 on the core verb only | Motif in four disciplines; cohesion score |
| 6 Show it | Fixes from the line-up; pass 6 (icon and thumbnails captured in-game); final twelve captures | Pass 6; final captures | No discipline under 8 (team) or 7 (solo); a stranger picks your capture from six in 3 s; Home click-through, play-through and D1 not worse on any pass and better on the first-frame pass; thumbnails left 7 days before judging |

Families go live whole or not at all, so old and new never share a plot. Keep every pad id, purchase key and footprint: a wall 0.5 studs wider than the old one moves saved buttons.

## 11. Level-up: symptoms in a live game → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| "Looks like every other simulator" | Template from one source, or a default (preset, sheet example, safe palette) left unchanged | §4: default row, a direction two axes away, hero asset and line-up test; change primary shapes before adding anything |
| Comments or reviews say "AI game" | Generated icon, thumbnail or description; defaults everywhere | Real captures, rewritten copy, defaults sweep |
| Each zone is fine; the game feels stitched together | Assets from several sources or eras | One bible; replace by family (§10 pass 8) |
| New assets make old ones look worse | Detail level rose mid-production | Freeze the bible version; migrate the family or hold the new work back |
| UI looks like it belongs to another game | No tie-in | §6 tie-in table; sample from the bible |
| Effects look pasted on | Effect palette and shapes chosen per effect | VFX tie-in; two colours plus white |
| Good click-through, poor play-through or ratings | Tile promises a look the game lacks | Capture the tile in-game after pass 4 |
| The team argues about taste | Rules are adjectives | Numbers, a golden sample and side-by-side review |
| Polished but forgettable (scores of 5–6) | No motif, safe palette, stock shapes | One bold constraint from §4; a motif across four disciplines |
| "More detail" made it worse | Detail added where structure was missing | Remove; restore one focal point per view |
| Looks like a different game on low-end phones | The look depends on shadows, bloom or PBR | Move it into shape and colour (`lighting-and-atmosphere.md` §11) |
| Contractor work does not match | Brief had no bible or golden sample | Send bible, golden sample and rubric; accept at 8 only |

## Review gate

- [ ] §4 intake written; the genre default row filled from three named competitors; the chosen direction differs from it on at least two axes, one of them shape, edge, material or light; hero asset and line-up test passed before the bible.
- [ ] Three-decisions line written; no competitor could sign it.
- [ ] Style tier chosen with the capacity check (timed golden samples); two or three hard limits written as bans.
- [ ] Reference board: 20–40 labelled images, at most a third from one title, at least 40% real world, no generated targets; anti-board exists.
- [ ] Bible lines are numbers or side-by-sides; tie-ins written for UI, icons, thumbnails, VFX, animation, audio and writing; the motif appears in each; palette scan prints zero rows.
- [ ] Golden samples (prop, kit module, character or interactable) and the beauty corner exist and match the current bible version.
- [ ] Defaults scan shows only deliberate rows; house-rule scan clean.
- [ ] Twelve captures taken on the phone; four tests run; every discipline scored by someone other than its author; no caps triggered for the target tier.
- [ ] Nothing generated ships: meshes, textures, UI art, icons, thumbnails, unedited copy.
- [ ] Several artists: each owns whole families; `check_asset.py` and the roster sheet run before every review; a non-author signs off at 8+ beside a golden sample; weekly line-up held.
- [ ] For a live game: passes run in order (1–3 before 8, 4 before 6), each re-captured from the same cameras, behind a flag, measured against the 14-day baseline.

## Sources

Accessed 2026-11-11. DevForum threads read through the Discourse JSON API.

- https://devforum.roblox.com/t/improving-user-experience-by-reducing-exposure-of-low-quality-content/3299107 (read; official, 2024-12-09, 1,253 likes)
- https://devforum.roblox.com/t/homepage-recommendation-eligibility-now-requires-a-custom-thumbnail/4945086 (read; official, 2026-10-19; top replies read)
- https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042 (read; official, 2026-08-06: Home weighs retention and monetisation)
- https://devforum.roblox.com/t/3874516 ("Why isn’t anyone playing my Roblox game despite it being well-made?") (read; 2025-08-11, replies with 9–17 likes)
- https://devforum.roblox.com/t/introducing-scene-generation-prototype-scenes-faster/4966611, https://devforum.roblox.com/t/beta-introducing-quality-mode-for-texture-generation/4938282, https://devforum.roblox.com/t/studio-beta-generate-game-characters-with-prompt-to-avatar/4964945 (read; official posts and most-liked replies, 2026-10)
- https://devforum.roblox.com/t/rovisuals-high-ctr-roblox-gfx-thumbnails-game-icons-more-using-ai/4346638, https://devforum.roblox.com/t/vizzbees-ai-thumbnails-icons-assets-that-actually-get-clicks/4723872, https://devforum.roblox.com/t/rblxai-from-idea-to-asset-in-under-a-minute/2974290, https://devforum.roblox.com/t/ai-generated-thumbnails/2667653 (read: developer replies to AI art tools; vendor claims ignored)
- https://devforum.roblox.com/t/how-are-modern-simulator-pets-made/2882620, https://devforum.roblox.com/t/low-poly-car-feedback/1367537, https://devforum.roblox.com/t/feedback-on-my-games-map/3788097, https://devforum.roblox.com/t/how-would-you-rate-my-simulator-lobby-so-far/1891111, https://devforum.roblox.com/t/how-to-stay-consistent-with-modeling/3274662, https://devforum.roblox.com/t/as-a-builder-how-do-you-plan-your-builds/187515 (read: critique threads)
- https://devforum.roblox.com/t/creator-spotlight-how-unroot-designs-ui-for-marbles-mermaids-and-more/3077233 (read: visual cohesion across map, lighting, UI and sound)
- https://github.com/Roblox/creator-docs (read, commit ccc2b01): `tutorials/curriculums/environmental-art/develop-polished-assets.md` (art style as "main source of truth", mood board), `resources/the-mystery-of-duvall-drive/construct-the-house.md`
- https://www.gamedeveloper.com/art/how-devs-can-spot-ai-generated-3d-models (read; Bryant Francis reporting Liz Edwards, 2024-11-05)
- https://www.gamedeveloper.com/gdc2022/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability (read; 2022-03-25)
- https://www.gamedeveloper.com/design/when-extra-budget-increases-your-visual-quality (read; Urbain Bruno on Epistory, 2016-03-07)
- https://www.gamedeveloper.com/art/deep-dive-cultivating-the-soft-art-of-shumi-come-home (read; 2022-07-28)
- Mitchell, Francke, Eng, "Illustrative Rendering in Team Fortress 2", NPAR 2007, https://steamcdn-a.akamaihd.net/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf (read: sections 3–4)
- 80.lv breakdowns (read; images viewed, listed in the three library files): Stanley Barrett, Emek Can Özben, Rodrigo Gonçalves, Benjamin Lucas, Tobias Koepp, Ivan Blinov, Georg Klein, Sasha Bernert, Angelo Tsiflas, Vitaliy Novart
- Reddit and petition sentiment on AI thumbnails (search summary only; reddit.com is not reachable from here)
- Engine API dump, version 0.747 (https://github.com/MaximumADHD/Roblox-Client-Tracker, read 2026-11-11): every class, member and enum item named in §2 exists with that spelling, and `ParticleEmitter.Texture` defaults to the path in the scan.
- Genre defaults (§4) read from captures viewed on 2026-11-11 and listed in `visual-library/environments-and-maps.md` §G: official Creator Spotlight posts (https://devforum.roblox.com/t/3840933, /3419750, /3579254, /3639226, /3659603, /4036940, /3269481) and official game thumbnails fetched through `https://thumbnails.roblox.com/v1/games/multiget/thumbnails` (Restaurant Tycoon 3, Retail Tycoon 2, Run A Farm!, LINE UP! Metro Tycoon, Steal a Brainrot, Grow a Garden, Tower of Hell, Brookhaven RP, DOORS, DONT SPLASH); hex values in the default rows were sampled from those images (median-cut, six colours). The directions are house proposals, not measured.
- LihFolk Vault V2, `15 AI Tools/AI 3D Model Generation Outside Roblox.md` §4 (modelling times) and `55 Modelling Nuance and Readability/Critiquing a Model - Paintovers and Iteration.md` (read, 2026-11-11)
- Not verified: both Luau scans are unexecuted; the reference hours per asset class and the six-week plan are house estimates; the default font family and grey GUI colour in the defaults scan are from memory `[VS]`; board sizes, the line-up test, capacity check and rubric caps are house estimates. No measured data was found linking AI art to retention or click-through; vendor "high CTR" claims were not used.
