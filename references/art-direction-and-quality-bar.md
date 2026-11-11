# Art direction and the quality bar: a cohesive game that does not look generic

What this is: the cross-discipline guide to the owner's bar ("very high-quality, cohesive, put-together, avoids the generic AI slop look"). It names what gives a Roblox game away as generic or AI-made in every discipline, gives the method that produces one distinct look across models, world, light, UI, effects, motion, sound and words, sets the bar per release tier, and gives a review procedure and an ordered rescue plan for a live game. Open it before the first asset of a new game, at every milestone review, when feedback says "looks like every other game" or "looks AI", and before commissioning art. It owns direction and review; depth stays with the discipline files and is linked, not repeated: `blender-modeling-craft.md` (asset numbers and the per-asset rubric), `art-pipeline-blender.md` (the style-bible template, export), `lighting-and-atmosphere.md`, `level-design-worldbuilding.md`, `ui-design-figma.md`, `vfx-and-juice.md`, `animation-and-rigs.md`, `audio-sfx-music.md`, `growth-and-marketing.md` (icon and thumbnail rules). Reference images: `visual-library/environments-and-maps.md`, `visual-library/models-props-characters.md`, `visual-library/lighting-and-mood.md`. Tags: `[official]` Roblox, `[community]` forum or named practitioner, `[lihfolk]`, `[VS]` version-sensitive, `[house]` house rule or estimate.

Contents: 1 What generic means · 2 Slop tells by discipline · 3 Pillars to art direction · 4 A style a small team can sustain · 5 Reference board · 6 Style bible: measurable rules and tie-ins · 7 Quality bar by tier · 8 Art review procedure · 9 AI tools without slop · 10 Raising a live game in ordered passes · 11 Level-up table · Review gate · Sources

## Start here by level

| Level | Do these first | Ignore for now |
|---|---|---|
| Beginner | Run the defaults sweep (§2 last block, §10 pass 1). Write the three-decisions line (§3). Pick the cheapest style in §4. Build a 20-image board with a label on every image (§5). Make one golden sample before anything else | Rubric scoring, tie-in tables, tiers |
| Intermediate | Fill the measurable rules and tie-ins (§6) into the bible template. Build a beauty corner (§3). Run the four tests on 12 captures at each milestone (§8). Hold contractors to the bible and the rubric | Blind scoring panels |
| Expert | Blind one-screenshot tests with strangers; weakest-link scoring per discipline with caps; a motif audit across icon, UI, world and effects; bible versioning with family-by-family migration (§10) | Nothing |

Terms: **generic** = could be swapped into another game unnoticed; **slop** = output nobody made a decision about, whatever tool produced it; **pillar** = one of the three promises the game makes; **golden sample** = the finished asset every new asset is held beside; **beauty corner** = a small area finished to final quality in every discipline; **motif** = a small shape or pattern repeated across disciplines; **value** = lightness independent of hue; **tie-in** = a rule that makes one discipline inherit from another.

## 1. What "generic" means, and what it costs

Three causes produce the same look `[house]`: **defaults left in** (every other game has them too), **a template copied from one source** (the cube pet, the 2020 simulator lobby), and **averaged output** (generators and mixed asset packs, where nobody chose a rule). Working test: an asset or screen is generic when you cannot name three decisions that make it this game's.

| Evidence | Detail |
|---|---|
| Similar or mismatched games lose discovery `[official]` | Since December 2024, experiences whose thumbnails, title, description or place files closely resemble existing ones are not prioritised in Home and Charts and rank lower in search; metadata that does not match the content is not recommended |
| Default thumbnails lose Home `[official]` | From 2026-10-19 only games with a custom thumbnail receive homepage recommendation impressions. The most-liked replies ask for AI thumbnails to be excluded as well `[community]` |
| Developers read the tells within a minute `[community]` | A "why does nobody play my well-made game" thread (143 likes): top replies list an AI thumbnail and description, `print` output left in the console, assets from a premade kit, stiff animation, overlapping UI and a rushed lobby |
| Players say they skip `[community: search summary]` | Reddit threads and a petition report players avoiding games with AI icons; dissent exists and a meme-led hit shows players forgive it when the game is fun. Treat it as a trust cost, not a law |
| AI meshes fail technically `[community: Liz Edwards via Game Developer]` | Baked-in lighting, a texture projected from one 2D image with its artefacts, dense automatic topology, jumbled auto-unwrapped UVs, about 50,000 triangles for a crate that needs about 500, asymmetry, limbs fused into blobs that cannot be posed. No single trait proves origin |
| Hand-made work can be slop too `[community: search summary]` | A player reply makes the point that work with no AI in it can be slop as well: the bar is decisions, not tools |

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
| Lighting | Noon sun, default sky, no grade | The most recognisable default on the platform | Genre preset plus white-cube balance (`lighting-and-atmosphere.md` §2, §12) |
| Lighting | Blown whites, haze of bloom, sun rays always on | "Effects on" mistaken for quality | Safe ranges (its §6) |
| Lighting | One tint over everything (the all-blue city); black "horror" | Hue replaces value structure; darkness hides the game | Value bands first; night by hue, not darkness |
| UI | Default-looking frames and fonts, mixed icon packs, a hit game's skin, rainbow gradients | Defaults, several sources, or one source | Tokens tied to the bible (§6); full list in `ui-design-figma.md` |
| UI | Generated panels and buttons: wobbly bevels, stroke weight changing along one edge, garbled glyphs | Cannot be 9-sliced or restated as tokens; no two elements match | Design in Figma from tokens |
| Icons | Rendered-plastic grinning avatar, extra fingers, lettering that melts, a style absent from the game | The current generator look; mismatch with the first minute | Compose from the game's own Blender assets and a Figma layout |
| Icons | Item icons from several packs or emoji | Mixed line weight and perspective | Viewport renders of the real meshes, one camera and light rig for all |
| Thumbnails | Default or auto image | Not eligible for Home recommendations `[official]` | Captures from real zones |
| Thumbnails | Off-model art; a clone of a hit's layout, pose and colours; "FREE" text walls | Mismatch and similarity both reduce exposure `[official]` | Real captures from review cameras; rules in `growth-and-marketing.md` |
| VFX | Default particle texture; legacy `Fire`, `Smoke`, `Sparkles`, `Explosion` | Engine defaults | Authored textures and Blender effect meshes (`vfx-and-juice.md`) |
| VFX | A different colour logic per effect; white additive blobs | No effect language; bloom soup | Effect palette and shapes from the bible (§6) |
| Animation | Default idle and walk on custom NPCs; sliding NPCs; linear tweens | "Clumsy and stiff" is named in reviews `[community]` | Authored idle, anticipation and overshoot; easing tokens (`animation-and-rigs.md`) |
| Animation | Mocap-like clips beside snappy cartoon clips | Two sources | One timing family per game |
| Audio | Default death, footstep and jump sounds; silent UI; one library click | Engine and library defaults | A UI sound set from one material family; replace character sounds (`audio-sfx-music.md`) |
| Audio | Over-used library tracks; loops with no structure; unmixed levels | Heard in many games; no mix decision | A music brief per zone; buses and loudness targets |
| Writing, naming | Title as tag soup with emoji; chatbot description ("embark on an epic journey", feature bullets that are not in the game) | Clone naming; mismatch | Title is the name; description says what you do in the first minute |
| Writing, naming | "Zone 1", "Epic Sword", "Dummy"; placeholder and "coming soon" boards; mixed capitalisation | No voice | A 30-word lexicon from the fantasy; two voice rules; one string table, proofread |
| Code-visible | Default player list, backpack bar, health bar, loading screen, proximity prompt, chat styling, cursor | The engine's own UI beside yours | Decide each: restyle, replace or hide (block below) |
| Code-visible | `print` spam in the client console; visible SpawnLocation decal; ForceField sparkle; NPC name and health bars; ragdoll-less default death | Seen by players and by every developer who presses F9 | Sweep before each release |

Defaults to decide on purpose `[official, VS]`: `StarterGui:SetCoreGuiEnabled` per `CoreGuiType` (PlayerList, Health, Backpack, EmotesMenu); `ReplicatedFirst:RemoveDefaultLoadingScreen()` after your own screen is up; `ProximityPrompt.Style = Custom` with `ProximityPromptService.PromptShown`; `TextChatService` window, input-bar and bubble configuration objects; `UserInputService.MouseIcon`; `Humanoid.DisplayDistanceType` and `HealthDisplayType` on NPCs; `SpawnLocation.Duration` (0 removes the ForceField) and an invisible SpawnLocation inside a Blender pad; the character sound script in `StarterPlayerScripts` (replace it with your own of the same name `[community]`). Hiding a default without replacing its function (no player list, no way to see friends) is worse than the default.

```lua
--!strict
-- unexecuted sketch, Studio command bar in Edit mode, read-only: counts engine defaults a player can see or hear
local ScriptEditorService = game:GetService("ScriptEditorService")
local DEFAULT_PARTICLE = "rbxasset://textures/particles/sparkles_main.dds" -- [VS] read it off a fresh ParticleEmitter
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
		elseif inst:IsA("BasePart") and inst.Transparency < 1 and inst.Material == Enum.Material.Plastic then
			note("default Plastic material")
		elseif inst:IsA("GuiObject") and inst.BackgroundTransparency < 1 and inst.BackgroundColor3 == DEFAULT_GREY then
			note("default grey GUI background")
		elseif inst:IsA("LuaSourceContainer") and string.find(ScriptEditorService:GetEditorSource(inst), "print(", 1, true) then
			note("script that prints")
		end
		if (inst:IsA("TextLabel") or inst:IsA("TextButton")) and string.find(inst.FontFace.Family, "SourceSansPro", 1, true) then
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
2. **The three-decisions line.** "This is the game with ___ shapes, a ___ palette and the ___ motif." If a competitor could sign it, rewrite it.
3. **One motif, repeated across disciplines.** A knot carved on a pauldron that returns on the belt, the bracer and the anvil is what makes a character read as one design (`visual-library/models-props-characters.md`). Put yours on a model trim, a UI corner, the icon and one effect shape.
4. **Rules can carry meaning.** Team Fortress 2 gave one team warm colours, natural materials and angular geometry and the other cool colours, industrial materials and orthogonal forms, kept characters identifiable as pure silhouettes, and omitted high-frequency detail where possible `[community: Valve, NPAR 2007]`. Use the same device for factions, zones or rarity.
5. **Find the style by making, then freeze it.** Practitioners describe the same loop: a small prop test before the kit; one or two objects pushed to final to lead everything else; about twenty objects, a critique of the whole, one or two iterations, then hold `[community: Gonçalves, Lucas, Özben on 80.lv]`. Write the bible from that golden sample, not from intentions.
6. **Build a beauty corner before production.** About 30 × 30 studs at final quality in every discipline: kit pieces, lighting preset, one interactable with its prompt, the HUD over it, one effect, one sound. It is the capture for the one-screenshot test (§8) and the brief for everyone who joins later.

## 4. A style a small team can sustain

A style is what the team can make two hundred times at the same quality. Sable's flat-shaded desert was chosen because the team could not build a detailed open world: the look had to be quick to produce, quick to iterate, consistent and still stand out, and readability was then recovered with layered lighting, distance fog and line work `[community: Kythreotis, GDC 2022]`.

| Style | Cost per asset | Low-end phone (no shadows) | Cohesion risk | Generic risk | Choose when |
|---|---|---|---|---|---|
| Flat colour, chunky bevels, palette atlas | Lowest | Strong: the look lives in shape and colour | Low | High unless shapes and palette are distinctive | Solo or two people; many assets |
| Faceted low-poly | Low | Needs an angled sun or per-face value jitter | Low | High: the 2019 "low poly" look | Rocks, crystals, terrain inside another style |
| Gradient atlas or simple hand-painted | Medium | Strong | Medium: painting skill varies between people | Low | One consistent painter on the team |
| Stylised PBR with trim sheets | High | Weak: depends on Realistic lighting | Medium | Low | Interiors, horror, a dedicated artist |
| Voxel | Low | Strong | Lowest: the grid enforces it | Medium | Building or mining games; strict grid discipline |
| Realistic PBR | Highest | Weakest | High | Low | Not with a small team |

- **Capacity check** `[house]`: assets needed × hours per asset at rubric score 8 ≤ art hours before launch. If not, cut asset count or drop a style tier; never drop the score.
- **Limitation as style.** Pick two or three hard limits and enforce them everywhere (a 12-colour zone palette, no textures, one bevel width, no outlines, one material idea such as "everything is folded paper" `[community: Lucas]`). Constraints kept everywhere beat detail.
- **Less detail, better read.** At gameplay distance small detail reads as noise `[community: Koepp]`; areas of low detail are what make the detailed focal point draw the eye `[community: Barrett]`.
- **Do not raise the detail level mid-production.** A team that used extra time to add painted folds, edge highlights and AO to new assets found them clashing with the earlier flat ones `[community: Fishing Cactus via Game Developer]`. Version the bible; migrate whole families or not at all (§10).
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

The one-page template is in `art-pipeline-blender.md` ("Style bible in one page"). A rule belongs in it only if a reviewer can check it with a number or a side-by-side. What each line must say:

| Rule | Measurable form | Source of the number | Check |
|---|---|---|---|
| Palette | Hex list per role, with HSV value range and saturation cap per role (ground V 35–60, structures one band away, interactables lightest or a saturation spike); at most 3 hue families per zone plus neutrals; 2 accents | Value-band table in `blender-modeling-craft.md` | Greyscale capture shows three or more bands |
| Shape language | Dominant primitive (round, square or triangular) and its accent; big:medium:small about 60:30:10; taper and lean rules ("posts lean 2–4°") | §3 pillars | Silhouette sheet; roster test |
| Edge and bevel | One width per viewing band, 1 or 2 segments, weighted normals | Bevel table in the craft file | Bevels read at 15 and 40 studs on the phone |
| Texel density | One px-per-stud figure for textured classes (start at 32–64 `[house]`); "none" for palette-atlas art | Texture budget in the pipeline file | Neighbouring assets equally sharp |
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

1. **Capture, do not remember.** Twelve captures on the phone at automatic quality: first frame after spawn; the hub from its gate view; three review cameras per zone for two zones; the shop open; the inventory open; the core verb mid-action with effects; the darkest preset; the icon at 64 px and at tile size beside five competitors; the first thumbnail beside the first frame.
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

Write the bible after pass 2 from the best fifth of what exists, then hold passes 4–9 to it. Do not start pass 8 before passes 1–3: new kit under default lighting and a rainbow palette still reads as generic.

## 11. Level-up: symptoms in a live game → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| "Looks like every other simulator" | Template from one source | Three-decisions line; change primary shapes and palette before adding anything |
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

- [ ] Three-decisions line written; no competitor could sign it.
- [ ] Style chosen with the capacity check; two or three hard limits written as bans.
- [ ] Reference board: 20–40 labelled images, at most a third from one title, at least 40% real world, no generated targets; anti-board exists.
- [ ] Bible lines are numbers or side-by-sides; tie-ins written for UI, icons, thumbnails, VFX, animation, audio and writing; the motif appears in each.
- [ ] Golden sample and beauty corner exist and are current.
- [ ] Defaults scan shows only deliberate rows; house-rule scan clean.
- [ ] Twelve captures taken on the phone; four tests run; every discipline scored by someone other than its author; no caps triggered for the target tier.
- [ ] Nothing generated ships: meshes, textures, UI art, icons, thumbnails, unedited copy.
- [ ] For a live game: passes run in order, each re-captured from the same cameras and shipped through the safe-change steps.

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
- https://github.com/Roblox/creator-docs (read, commit ccc2b01): `tutorials/curriculums/environmental-art/develop-polished-assets.md` (art style as "main source of truth", mood board), `resources/the-mystery-of-duvall-drive/construct-the-house.md`; class references for the APIs named in §2
- https://www.gamedeveloper.com/art/how-devs-can-spot-ai-generated-3d-models (read; Bryant Francis reporting Liz Edwards, 2024-11-05)
- https://www.gamedeveloper.com/gdc2022/how-shedworks-refined-the-art-of-sable-in-pursuit-of-readability (read; 2022-03-25)
- https://www.gamedeveloper.com/design/when-extra-budget-increases-your-visual-quality (read; Fishing Cactus on Epistory, 2016-03-07)
- https://www.gamedeveloper.com/art/deep-dive-cultivating-the-soft-art-of-shumi-come-home (read; 2022-07-28)
- Mitchell, Francke, Eng, "Illustrative Rendering in Team Fortress 2", NPAR 2007, https://steamcdn-a.akamaihd.net/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf (read: sections 3–4)
- 80.lv breakdowns (read; images viewed, listed in the three library files): Stanley Barrett, Emek Can Özben, Rodrigo Gonçalves, Benjamin Lucas, Tobias Koepp, Ivan Blinov, Georg Klein, Sasha Bernert, Angelo Tsiflas, Vitaliy Novart
- Reddit and petition sentiment on AI thumbnails (search summary only; reddit.com is not reachable from here)
- Not verified: the default `ParticleEmitter.Texture` path and the Luau scan (unexecuted); the 32–64 px-per-stud starting range, board sizes, capacity check and rubric caps are house estimates. No measured data was found linking AI art to retention or click-through; vendor "high CTR" claims were not used.
