# UI design: hierarchy, design system, construction, critique, Figma hand-off

How to design Roblox UI that looks authored by this game's art team and reads on a small phone: what the player sees first, the grid, colour, type and icon systems, how panels and buttons are built from native instances, how to score and redesign an existing UI, and how to run the work through Figma (and the Figma MCP) into Studio. Open it when designing UI for a new game, re-skinning a live one, or when a review says "looks default", "looks AI" or "too much on screen". Siblings: `ui-screen-recipes.md` (sizes, screen recipes, HUD layouts by genre), `ui-motion-and-feedback.md` (motion tokens, button feedback, reward sequences), `ui-input-crossplatform.md` (engine rules, safe areas, thumb zones, gamepad focus, performance), `accessibility-and-player-qol.md` (colour-blind checks, text size, settings). Examples to study before drawing: `visual-library/ui-hud.md` (HUDs), `visual-library/ui-screens.md` (windows), `visual-library/ui-components-and-style.md` (kits, icons, native styling, tools); bundled sheets 05–07 and 09 (`visual-library/reference-sheets.md`).

Tags: `[official]` Roblox docs and staff announcements, `[community]` DevForum, GitHub and third-party craft writing (source named inline), `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0, rewritten), `[VS]` version-sensitive, `[house]` house rule or estimate. The file gives a method for building a game's own look, never a look to copy.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Write the three reads for the HUD (§1). (2) Derive the tokens from four inputs taken from the game (§3): 6 colour roles, 2 fonts, 1 radius, 1 outline; never ship the §15 placeholder. (3) Grey-box the HUD and one window at `Phone-S` over a real screenshot. (4) Build button, panel and currency readout from the recipes in §6. (5) Score with the rubric (§9) and fix every row under 1. | StyleSheets, converters, springs, virtualised lists |
| Intermediate | Theme module with no raw value outside it; full state matrix per component; icon family; the tells table as a pre-ship check; Figma variables mirrored to the theme; hand-off checklist; six test viewports | Automating the Figma round trip |
| Expert | Regenerate builders from Figma; automated audit plus rubric score per screen in every milestone review; A/B HUD and shop layouts with Experiments `[official]`; style stress test before any re-skin; measured budgets in `ui-input-crossplatform.md` §UI performance | Nothing: re-verify every `[VS]` |

Terms: a **token** is a named design value stored once. A **read** is one pass of the eye over the screen. **9-slice** stretches an image's edges and centre while keeping its corners. **Optical** alignment centres what the eye sees (the glyph, the icon's mass), not the bounding box.

## Fast routes

The six commonest UI tasks, each read in 250–360 lines instead of the four guides end to end. "figma" is this file; "recipes", "input" and "motion" are `ui-screen-recipes.md`, `ui-input-crossplatform.md` and `ui-motion-and-feedback.md`. Sheets are `assets/reference/NN-*.png`; library rows are in `visual-library/`. Each listed section defines its tokens or sits beside the section that does.

| Task | Read exactly | Look at |
|---|---|---|
| Redesign one screen (shop, inventory, rewards) | figma §3, §4, §6, §9, §10 · recipes §1, §3 and the screen's own section (§5 shop, §6 inventory, §9 rewards) · input §UI architecture from the `DisplayOrder` band plan to the note under the presenter · motion §2, §8 (about 350 lines) | Sheets 03 or 04, 05, 09 · `ui-screens.md` the screen's section, its "Start here" rows (shops #1, #4, #10) · `ui-components-and-style.md` §1 #1–#3 against #8 |
| Build a new HUD | figma §1, §2, §3, §4, §6 · recipes §1, §2, §4 · input §Containers, insets and sizing, §Mobile layout and thumb zones · motion §2 (about 330) | Sheets 01, 02, 19 · `ui-hud.md` §1–§3 (#1–#28), "Start here" rows first |
| Fix the phone layout of a live UI | figma §2, §4, §11 · input §Containers, insets and sizing, §Text, numbers and localisation, §Mobile layout and thumb zones, Level-up table, UI audit scan · recipes §1, §4 (about 270) | Sheets 01, 19, 06 · `ui-hud.md` #4, #18, #20, #36 |
| Add motion and feedback to an existing UI | figma §3 "States" bullet · motion §1–5, §7, §8, Level-up table · input the presenter sketch and its note in §UI architecture (about 270) | Sheets 05, 08 · `ui-components-and-style.md` §5 #33, #38, #39 · `ui-screens.md` §7 #67, #68, #72 |
| Figma to Roblox | figma §3, §4, §7, §9, §11, §12, §13, §14, §15 · input §Containers, insets and sizing (about 310) | Sheets 06, 05 · `ui-components-and-style.md` §4 #27–#31, §7 #47, #51 |
| Critique a UI (score, list fixes) | figma §1, §3, §4, §8, §9, Level-up table · input the pass criteria at the end of §Mobile layout, Level-up table · recipes and motion Level-up tables (about 250) | Sheets 02, 09, 07 · "What the weak examples had in common" in each `visual-library/ui-*.md` |

## Contents

Fast routes · 1 Visual hierarchy: the three reads · 2 Grid and spacing · 3 Colour system · 4 Type system · 5 Icons · 6 Construction recipes (native-first) · 7 From brief to design system · 8 Generic and AI-look tells · 9 Critique rubric · 10 Redesign procedure · 11 Frames and scale · 12 Figma and the Figma MCP · 13 Export, upload, converters · 14 Hand-off checklist · 15 Theme module · Level-up table · Review gate · Sources

## 1. Visual hierarchy: the three reads

A player in motion reads the HUD in the corner of the eye. Design it like a poster: one thing readable from across the street, a few things on a second look, the small print on request. Zach Gage's GDC 2018 talk calls this "the three reads" and uses a concert poster as the model `[community]`; the Roblox docs ask the same questions under "hierarchy of information" (what is the player doing now, what must they know, what choices, how often) `[official]`.

| Read | Budget | What belongs | Treatment |
|---|---|---|---|
| 1: within 1 s, peripheral vision | At most 3 elements | The primary verb, the one vital that can end or stall play (health, carry bar, round timer), the number the loop is about | Largest size tier, full saturation, own screen region, may move on change |
| 2: a 3 s glance | 4–6 elements in at most 4 groups (HUD total: 7 groups; one menu column is one group) | Next goal, second currency, cooldowns, boost timers, the menu buttons | Middle size tier, neutral ink, colour only as a small key |
| 3: on demand | Everything else | Inventory, stats breakdown, settings, codes, social | Behind one tap; never on the HUD |

Tools of emphasis, strongest first `[official]`: size, colour (bright against muted), space around the element, proximity (grouping), motion. Every tool is a shared budget: each element that shouts makes the others quieter, so a screen gets one saturated filled action, and motion is reserved for change.

Method:

1. List every element the screen could show; star the three the loop cannot work without (the Burrito Bison designer does this before any mockup `[community]`). If more than three are starred, the loop is unclear, not the UI.
2. Assign each element a read. Anything in read 3 leaves the HUD. Anything that matters only sometimes becomes contextual: shown by state (ball possession swaps Sprint/Tackle for Deke/Pass in the docs' example `[official]`), by proximity (a prompt), or on change (a counter that appears for 3 s).
3. Give each read one size tier with a ratio of at least 1.25 between tiers (20 → 16 → 14 px text; 64 → 48 → 36 px buttons). Two elements of nearly equal size read as equal.
4. Group by proximity: gap between groups at least 2× the gap inside a group (§2).
5. Test (10 minutes, from a Kongregate designer's "UI litmus test" `[community]`): write the intended top three; screenshot at phone size over busy gameplay; make one copy with a 4 px blur and one in greyscale; circle what stands out in each; the circles must match the list. Colour-only emphasis fails the greyscale copy.

Worked example: backpack simulator HUD at `Phone-S` (800×360), numbers `[house]`.

| Read | Element | Place | Size | Treatment |
|---|---|---|---|---|
| 1 | Sell button (the verb that completes the loop) | Left of the jump button, placed from the live `JumpButton` | 60 px round | Accent fill, icon only, lip; pulses once when the backpack fills |
| 1 | Backpack bar | Bottom centre, 12 px above the safe edge | 200×16 | Neutral track; fill turns accent at 100% with the word `FULL` |
| 1 | Coins | Top-left, under the top bar | Icon 30, number 20 | Outlined number, no plate; counts up |
| 2 | Next-goal chip | Top centre | Height 32 | Dark plate at 0.25 transparency, progress `340/500`, white ink |
| 2 | Gems | Under coins | Icon 22, number 16 | Same construction, one tier smaller |
| 2 | Menu: Shop, Pets, Gifts, More (Rebirth behind More or a world prompt) | Right edge, above the jump zone, 2 × 2 | 56 px tiles, gap 8 | Neutral tiles, icon 24 plus a 14 px caption of one short word; badge only when claimable |
| 2 | Boost pills | Under the goal chip | Height 32 | Only while a boost runs; honest timer |
| 3 | Everything else | Behind `More` or a world prompt | n/a | Not on the HUD |

The result uses one accent (Sell), one colour per currency icon and white ink for everything else. Zone rules behind the placements: `ui-input-crossplatform.md` §Mobile layout.

Diegetic or not `[community]` (Fagerholt and Lorentzon's four types, summarised by Stonehouse): **non-diegetic** HUD (fastest to read: use for read 1), **spatial** (in the world, outside the fiction: prices and timers on a `BillboardGui`, objective trails; use for anything that belongs to one object), **meta** (screen-space effects standing for a state: damage vignette), **diegetic** (inside the fiction: a `SurfaceGui` on a Blender-modelled board). Move read-2 information into the world when it belongs to an object, and the HUD shrinks without losing information (HP over heads, prices over items: `visual-library/ui-hud.md` #9, #21, #22, #26).

## 2. Grid and spacing

Numbers are px at `Phone-S`; all `[house]` unless tagged. Critique threads return to spacing more than to any other fault ("padding is bad", "borders do not line up", "slots unevenly sized", "do the maths on paper first") `[community]`.

| Rule | Value |
|---|---|
| Base unit | 4. Every gap, padding and size is a multiple of 4 |
| Spacing scale | 4 (icon to its number), 8 (between controls), 12 (inside cards), 16 (panel padding, screen margin), 24 (between groups), 32 (between sections) |
| Screen margin | 16 from the safe-area edge on phones, 24 on tablets, 5% on TV |
| Proximity | Gap between groups ≥ 2× the gap inside a group |
| Row heights | One set per game: 32 (chips), 44–48 (controls), 56–64 (HUD buttons), 72 (list rows with two lines) |
| Button padding | Horizontal padding 0.5–0.75× the button height; icon 55–65% of the button height |
| Columns | Window content width = columns × cell + (columns − 1) × 8; compute cells from width, never hand-place |
| Nested radius | Inner radius = outer radius − padding (16 outer, 12 padding → 4 inner; never the same radius twice in a nest) |
| Alignment lines | At most 3 vertical alignment lines per window (left edge, content column, right edge); every element sits on one |
| Optical centring | Centre the visible mass: shift a play triangle 5–8% right, lift descender-heavy captions 1 px, centre the art inside the image file itself |
| Empty space | Leave one free cell or 15% free width in every window: features arrive later and a full window forces a redesign `[community]` |

- Use `UIListLayout` + `UIPadding` (auto layout in Figma) so spacing is a property, not a position; `UIFlexItem` for the one child that should take the remaining width `[official]`.
- Borders cost separation, not add it: prefer spacing and a surface step to a 1 px line around every element `[community]`.

## 3. Colour system built from the game's art direction

**Derive the theme from the game before drawing anything.** The values in §15 and on the bundled sheets are placeholders: shipped unchanged, they make every game look like the sheets, which is the generic result this skill exists to prevent. Take four inputs from the game, preferably from its style bible (`art-direction-and-quality-bar.md` §6, whose UI tie-in row these steps apply), and turn them into tokens `[house]`:

| Input | Read it from | Becomes |
|---|---|---|
| 1. Dominant world hue and value band | The brightest and the darkest gameplay screenshot: the hue covering most pixels, and the HSV value range | `Surface` hue (a neutral tinted 5–15% saturation toward it). `Surface` lightness outside the world's band: a bright world takes dark panels (lightness 15–25%) or light panels with a dark outline; a dark world takes light ink on dark plates at 75–85% opacity. `Outline` = the world's darkest neutral. Official guidance for HUD over 3D: neutral black and white for almost everything, colour only for key information `[official]` |
| 2. One accent | The bible's interactable accent (the colour of things players use) | `Primary`, the one action per screen. `Premium` and `Danger` at least 40° of hue from it and from each other; a world with a treasure colour (gold coin, gem) lends it to `Premium` |
| 3. Material motif | One object only this game has (a basket, a collar tag, an enamel sign) | Radius family (soft bevels → 16/12/8; crisp chamfers → 4/2 or cut corners), outline weight, the header or frame treatment, the close button's shape. Icon shapes stay distinct from world props so UI never reads as scenery `[official]` |
| 4. Tone and age band | The brief | Display family (§4), lip or flat buttons (§6), enter easing (Back Out playful, Quint Out tense), saturation cap |

Then measure every text-on-fill pair (contrast bullets below) and fix failures by moving lightness, not hue. **No access to the game:** ask for two screenshots (brightest and darkest zone) and one object that is unmistakably theirs; until they arrive, write the four assumed inputs in one line above the theme, keep `Placeholder = true` (§15) and say so in the hand-off. **Line-up check:** place the HUD beside captures of the three nearest competitors; if it shares a palette family and radius with any of them, change the accent or the motif. Two derivations, ratios measured with the WCAG formula `[house]`:

| | A: pet-farm simulator | B: hospital escape (horror) |
|---|---|---|
| Inputs | Grass H 105°, V 55–85%; sunflower-yellow interactables; woven-basket motif; playful, ages 8–12 | Teal-grey H 190°, V 8–45%; sodium-amber lamps; enamel name tags; tense, 13+ |
| `Surface`, `SurfaceAlt` | Cream `#FFF4DC`, straw `#F2DDB0`: light panels, separated from the bright world by the outline | `#12181A` at transparency 0.2, `#1E2629`: dark plates under light ink |
| `Ink`, `InkMuted`, `Outline` | `#3A2414`, `#6E513C`; outline = ink (the basket's shadow brown), 3 px | Paper `#E8E2D0`, `#A8A28F`; outline `#0A0D0E`, 2 px |
| `Primary` (label) | `#FFC234` (dark ink, 9.0:1) | `#E8A33D` (ink `#12181A`, 8.3:1) |
| `Premium`, `Danger` (label) | Teal `#0F766D` (white 5.5:1), red `#C8343A` (white 5.2:1) | Enamel green `#6FB8AC` (ink `#12181A`, 7.8:1), red `#A33241` (paper 5.3:1) |
| Shape | Radius 16/12/8, lip 5, a basket-weave header strip (9-sliced image) | Radius 2/0, flat buttons, the header is an enamel tag with two rivets |
| Type, motion | `LuckiestGuy` + `BuilderSans`; enter Back Out 0.22 s | `SpecialElite` + `BuilderSans`; enter Quint Out 0.18 s, no overshoot, no idle loops |
| Ink on surface | 13.3:1, muted 6.6:1 | 9.9:1, muted 5.0:1 on the plate composited over the brightest zone (`#8FA3A6`) |

**Assign roles, not colours.** 60% of any screen is neutral surface, about 30% structure (headers, tabs, plates), at most 10% accent.

| Role | Use | Derived values per role |
|---|---|---|
| `Surface`, `SurfaceAlt` | Window body; raised or inset areas | A visible step of 4–10% lightness between them; never pure black or white on large areas (dark base near `#121212`–`#232323` `[community]`) |
| `Ink`, `InkMuted`, `OnAccent` | Text and glyph icons | `InkMuted` = ink at 70–80% opacity, read-3 text only. `OnAccent` is chosen per accent by measurement (below), never assumed white |
| `Outline` | Every border and text stroke | One near-black, tinted toward the world's shadow hue |
| `Primary` | The one confirm action per screen; soft-currency buy | `light` +8–10% lightness (gradient top; less where `OnAccent` would drop under 4.5:1 on it), `dark` −18–25% lightness shifted 5–10° toward blue (lip only: no text sits on it), `OnAccent` = white or the `Outline` ink, whichever measures ≥ 4.5:1 on `light`, the base and the pressed fill |
| `Premium` | Robux actions only | Same ramp; used nowhere else, so players learn it |
| `Danger` | Close, destructive, cannot afford | Same ramp. Red as text on a surface is a lighter tint measured on that surface, never the fill colour; never red text on a `Primary` fill (1.6:1 on a mid green, and red/green is the first pair colour-blind players lose) |
| `Info`, `Warning` | Links, timers running out | Small areas only |
| `Focus` | Gamepad ring | Reserved: appears nowhere else |
| Rarity ramp | Frames, plates, name bars; never filled action buttons | Below |

- **States** are computed, not picked: hover +6–8% lightness; pressed −10–12% and the face sinks; selected adds an outline and a tint; disabled drops the fill's saturation under 15% and its opacity to 50–60%, keeps the label at full opacity (dimming both lands under 3:1) and states the reason ("Need 50 coins"). An unaffordable price uses this disabled state with the shortfall as its label. Grey means unusable and a lock means not yet earned: conventions the docs name `[official]`.
- **Rarity ramp: one ramp, three cues.** (1) Hue in the order players already read `[community]`: grey, green, blue, purple, gold, then pink. (2) Lightness rising at every tier, so the ladder survives colour-blindness and greyscale. (3) A name and a pip count (or frame shape) on every card (`accessibility-and-player-qol.md` §3). Example values with OKLab lightness `[house]`: Common `#6A7382` (0.55) → Uncommon `#2F9E55` (0.62) → Rare `#4A98E8` (0.67) → Epic `#B48BF5` (0.72) → Legendary `#F0B63A` (0.81) → Mythic `#FFC0D9` (0.87). The conventional light-grey Common and deep-purple Epic break cue 2: darken the grey, lighten the purple. Adjacent tiers differ by at least 40° of hue and 0.04 OKLab lightness; a label on the tier colour is white on Common and `Outline` ink on the rest (each ≥ 4.5:1); the top tier earns a treatment (animated gradient sweep), not just another hue. 5–6 tiers; sheets 04 and 07 draw this ramp.
- **Contrast targets** (WCAG 2 relative luminance): text 4.5:1; large text (≥ 24 px, or ≥ 19 px bold) and icons 3:1; disabled text not under 3:1; HUD text must hold 4.5:1 against both the brightest and the darkest screenshot, which in practice means outline or plate. Adjacent surfaces differ by a visible lightness step or carry an outline. Measure every pairing in the token table with a checker (`visual-library/ui-components-and-style.md` #53); do not judge by eye.
- **Mid-tone accents fail white.** Measured on the placeholder tokens of §15: white on `Primary` `#35B25D` is 2.7:1 and on its `light` 2.2:1, so a bare label there uses the `Outline` ink (6.0:1 base, 7.5:1 light, 4.6:1 pressed). The cartoon look (white label on bright green) passes only because of its outline: white on a 2 px `Outline` stroke is 16.5:1 and the stroke on the fill 6.0:1. `Premium` gold takes dark ink (9.0:1). `Danger` `#CF2E3E` takes white (5.1:1; 4.6:1 on its `light`), which is why its `light` is only 3% lighter. Red price text on `Surface` needs a tint near `#FFA3A3` (6.7:1; 4.7:1 on `SurfaceAlt`). `InkMuted` `#C8D2E3` holds 8.4:1 and 5.8:1 on the two surfaces.
- **"Harsh" palettes** `[community]` (the most common colour critique): several fully saturated hues touching. Fix: one fully saturated hue per screen plus the rarity ramp; other hues at 70% saturation or less; neutrals between coloured areas. "Bland" is the opposite fault: only greys, no role colour on the primary action.
- **Colour is function.** Health is the same green in the bar, the icon and the text; each destination keeps one colour everywhere (Shop, Rewards, Quests) `[official][community]`. A category button in an off-theme colour is read as a mistake.
- Young audiences: bright is fine, but separate brights with neutrals; children aged 6–8 and 9–12 are different audiences and each rejects what looks made for the younger band `[community]` (NN/g studies, 125 children). Playtest with the real age band.

## 4. Type system

| Decision | Rule |
|---|---|
| Families | One display, one body. Roblox-native display: `FredokaOne`, `LuckiestGuy`, `Bangers` (playful), `Oswald` (condensed, sports), `Michroma`, `Jura`, `Sarpanch` (sci-fi), `Creepster`, `SpecialElite` (horror). Body: `BuilderSans*`, `Nunito`, `Roboto`, `TitilliumWeb`, `Ubuntu` (all `Enum.Font`), Montserrat (family only: `Font.fromName("Montserrat")`) `[official]` |
| Loading | `Enum.Font` or a Creator Store family through `Font.fromName` / `Font.fromId`; no arbitrary font upload was found in the docs `[VS]`. `Gotham*` enum values were removed and map to Montserrat `[official]`: name the family that really renders. Pick the Roblox family first, then its Figma twin |
| Scale (`Phone-S` px) | Caption 14, Body 16, HUD number 20, Title 24, Display 30 (ratio about 1.25). At most 4 sizes per screen. Epic's mobile guidance puts the reading floor near 18 pt on phones `[community]`: keep 14 for captions only |
| Weights | Two: regular or medium for reading, bold or extra-bold for emphasis. Build hierarchy with weight and ink colour before reaching for a new size |
| Stylised display font | Titles and alerts only `[official]`; never body, prices or numbers the player compares |
| Case | Capitals for labels of one or two words; sentences in sentence case |
| Text over the world | Stroke or plate `[official]`. Stroke at most about 7% of rendered size on rounded heavy fonts (2 px at 30 px), 8–12% on open geometric ones `[lihfolk]`; add `UIShadow` with `Mode = Enum.ApplyShadowMode.Text`, `Offset` `(0, 2)` px, `BlurRadius` 0, for the hard cartoon drop (`Spread`, `Inset` and `ShowBehindParent` do nothing in text mode) `[official][VS]` |
| Size mismatch | Labels in one group share one size; a size difference must mean importance. Mixed sizes from `TextScaled` are the most repeated text critique `[community]` |

- A glyph stroke grows inward and closes the holes of 0, 6, 8, 9, a, e; `UIScale` scales the stroke with the text, so enlarging does not help `[lihfolk]`. Test string: `10 20 60 80 88 00 Fast` at the smallest phone size over the real background.
- Numbers `[lihfolk]`: 3 significant figures when abbreviated (`4.62K`), separators below the first tier (`9,840`); strip trailing zeros only after a decimal point; re-check the tier after rounding (999,950 must not print `1000K`); fixed-width, right-aligned labels for ticking counters.
- Engine behaviour (`TextScaled`, `PreferredTextSize`, RichText, localisation): `ui-input-crossplatform.md` §Text.

## 5. Icons

- **One family.** Same grid (24 or 32 units with a 2-unit margin), same stroke weight (8–10% of the icon size) or all filled, same corner radius as the UI, one light direction (top-left), one perspective (flat front, or one fixed three-quarter view). Mixed packs and mixed fidelity (a crisp button beside a pixelated close icon, shaded icons in a flat UI) are named in nearly every critique thread `[community]`.
- **Two kinds, two pipelines.** Glyph icons (navigation, stats, states) are drawn in Figma in white with the outline baked in, then tinted with `ImageColor3`. Item icons are renders of the real Blender asset on a transparent background with one fixed camera and light rig, so the icon is the item (house rule 1; no AI-generated icons).
- **Optical size.** Limit detail: an icon must read at the size it ships `[official]`. Under 24 px draw a simpler version (fewer interior lines, thicker stroke) instead of scaling the large one down.
- **Metaphors children already know** `[official][community]`: lean on genre symbols (sword = strength) and on conventions seen everywhere (home, back arrow, X to close, play, lock). Safe set: backpack (inventory), basket or stall (shop), paw (pets), gear (settings), gift box (rewards), scroll or checklist (quests), two arrows (trade), lightning or potion (boost), ticket (codes). Avoid adult-software metaphors (floppy disk, hamburger without a label) and anything needing reading.
- **Captions.** Icon plus one word on menu buttons until analytics show the buttons are found; never text-only buttons for young players (Google's kids guidance `[community]`). Icons survive translation; labels cost +30% width `[official]`.
- **Naming test** `[house]`: show each icon alone at 32 px to five people outside the team; under 4 of 5 correct means redraw or add a caption.
- Wireframes may use Roblox's built-in `BuilderIcons` font through a RichText `<font family>` tag `[community][VS]`; the path is undocumented, so do not ship on it. Open icon sets for studying construction and testing metaphors, with the licence each was read under: `visual-library/ui-components-and-style.md` §6; a hand-painted set on a live hit and a nine-icon grid drawn as one family: #6, #7 there.

## 6. Construction recipes: native first

**Structure, layout, text and most styling are native instances; artwork is images.** The 2025–2026 modifier releases moved a lot from "export a PNG" to "set a property" `[official][VS]`:

| Now native (fully released) | Since | Still an image |
|---|---|---|
| Several border strokes per object, inner / centre / outer position, `BorderOffset`, thickness scaled to the parent (`StrokeSizingMode.ScaledSize`) | Dec 2025 | Dashed or textured borders |
| Drop shadow (`UIShadow`: `BlurRadius`, `Offset`, `Spread`, `Color`, `Transparency`, `ZIndex`); per-corner radii on `UICorner` (`TopLeftRadius`, `TopRightRadius`, `BottomLeftRadius`, `BottomRightRadius`) | Jun 2026 | Non-rectangular silhouettes: ribbons, shields, stars, speech tails, slanted tabs |
| Radial, conical and elliptical `UIGradient`, tile modes, `Scale` | Oct 2026 (dark gradients may band: known issue) | Textured panels (wood, paper, studs), illustrations, logos |
| Text shadow (`Mode = Text`), inset shadow (`Inset`), knockout shadow (`ShowBehindParent = false`), a child `UIGradient` on a shadow | Nov 2026 | Background blur (no released UI blur), blend modes, masks |

Budgets from the announcements `[official]`: under 300 `UIStroke`s and at most 100 `UIShadow`s on screen (low-end devices); `UIShadow` is faster than a 9-sliced shadow image; strokes do not affect layout, so leave room for them. One contextual (text) stroke per label; set a distinct `ZIndex` on stacked border strokes and stacked shadows. `UIStroke` follows the box or the glyphs, never an image's alpha: bake icon outlines into the PNG. `UIShadow` takes no texture and does not work on `Path2D`. Each announcement's example image: `visual-library/ui-components-and-style.md` #27–#31.

Recipes (px at `Phone-S`; colours are role names from §3; unexecuted property sketches):

| Component | Instances and properties |
|---|---|
| Chunky button (toy, simulator) | Root `TextButton` 160×48, transparent, `AutoButtonColor = false`. `Lip` Frame full size, `Primary.dark`, `UICorner` 12, `UIStroke` Outer 3 `Outline`. `Face` Frame `Size = UDim2.new(1, 0, 1, -5)`, white background, `UICorner` 12, `UIGradient` `Rotation = 90` from `Primary.light` to `Primary`; second `UIStroke` on `Face`: `BorderStrokePosition = Inner`, thickness 2, white, transparency 0.65, with its own `UIGradient` fading it out below mid-height (top highlight only). Label: bold 20 (display family for words, body family for prices, §4), white with a contextual stroke 2 `Outline` (the stroke is what makes white legible on a mid-tone fill, §3), `UIShadow` `Mode = Text`, offset `(0, 2)`, `Primary.dark`. Pressed: `Face.Position` +4 px so it sinks into the lip |
| Flat button (competitive, tools) | One Frame, `Primary`, `UICorner` 8, no stroke, no gradient. Hover +6% lightness, pressed −10% and inner `UIScale` 0.97. Label medium weight 16 in `OnAccent`, no stroke. Depth, if any: `UIShadow` blur 8, offset `(0, 2)`, transparency 0.75 |
| Window | Three layers, so the fade cannot clip what leaves the window's box: `Face` (`CanvasGroup`, transparent, static size = window + 20 px on every side; the presenter fades its `GroupTransparency`) → `Window` Frame at 20 px inset (`Surface`, `UICorner` 16, `UIStroke` Outer 3 `Outline`, one `UIShadow` blur 16, offset `(0, 4)`, transparency 0.65, the pop `UIScale`) → header, close, content. Close overhang (≤ 8), stroke (3) and shadow (16 + 4) all fit in the 20 px margin; at `Phone-S` a 736×308 window makes a 776×348 group. Header strip in the destination colour (deep enough for a white title at 3:1 or better) with per-corner radii (top 16, bottom 0) so nothing pokes past the rounding. Content areas `SurfaceAlt`, radius 4 (16 − 12 padding). Body gradient at most 4% lightness, vertical, or none |
| Card / slot | Plate = rarity colour mixed 25% into `Surface`; `UICorner` 8; one `UIStroke` 2 in the rarity colour; icon 70% of the cell; count bottom-right in outlined text; no shadow per cell (the 100-shadow budget goes in one screen of cards) |
| HUD number | Icon + `TextLabel`, no plate; stroke per §4; optional text `UIShadow` |
| Progress bar | Track `SurfaceAlt` darkened, radius = height / 2, `UIShadow` `Inset = true`, blur 4, offset `(0, 2)`, black at 0.6 (reads as a groove). Fill is a child with its own `UICorner`, vertical gradient `light` → base, minimum visible sliver 6 px |
| Badge | `Danger` circle ≥ 22 px, white 2 px stroke, bold 14 px white number (needs a `Danger` on which white measures 4.5:1), overlapping the button's top-right corner by a third |

- A gradient multiplies the background: put `UIGradient` on a white `BackgroundColor3` `[community]`. Keep gradients to 2–3 stops (the docs advise no more than 6) and never put one on text that also has a legacy text stroke `[official]`.
- `ClipsDescendants` clips to the rectangle, not the `UICorner`: round the child too (per-corner radii), inset it, or use one `CanvasGroup` `[official]`.
- A `CanvasGroup` always clips its descendants to its bounds `[official]`, and a `UIStroke` or `UIShadow` parented directly to the group draws outside its texture and ignores `GroupTransparency` (as designed, per a staff reply) `[community]`: keep stroke and shadow on the inner `Window`, never on the group. The docs' reduced-motion sample fades a full-screen transparent group; the 20 px margin is the same idea for less texture memory. A window that does not fade needs no group.
- A chunky button is about ten instances: right for 5 HUD buttons, wrong for 300 list cells. For dense lists use a 9-sliced body image or the flat recipe.
- Reach for an image when the recipe exceeds about 10 instances per repeated element, when the silhouette is not a rounded rectangle, or when the surface has texture.

When an effect earns its place, and when it reads as a template:

| Effect | Helps | Reads as template or generated |
|---|---|---|
| Gradient | One hue, vertical, light on top, ≤ 10% lightness change: a lit surface | Two unrelated hues on every panel; 45° sweeps; gradients on body text; a gradient on one of two sibling buttons `[community]` |
| Stroke | One weight and one near-black colour separating UI from an unpredictable world | Thin 1 px saturated strokes on dark translucent panels (called out as the "AI look" `[community]`); a different weight per element; a border around everything |
| Shadow | Elevation: a window above the HUD, a raised button; small offset on sober styles `[community]` | A soft black blur under every element; a shadow on a number that already has a stroke; coloured glow on every button |
| Lip / bevel | Toy and simulator styles: a clear "press me" for children; the docs note highlights and shadows make buttons look tactile `[official]` | Mixed with flat elements; lip on non-interactive plates |
| Inner highlight | Top edge only, matching the light direction | All four edges (reads as glow) |
| Translucent panels | HUD plates at 0.2–0.35 transparency under text | Windows the player must read: body under 85% opaque loses contrast over gameplay `[community]` |
| Corner radius | One family; rounder for friendly, sharper for realistic, horror and military `[community]` | Round and square corners mixed; pill buttons in a sharp-cornered sci-fi shooter |
| Tilt and skew | Headers, title tabs and one hero panel as the signature | A tilted body the player must read or tap precisely (`visual-library/ui-components-and-style.md` #1, #3, #5) |

## 7. From brief to design system

1. **Brief with pictures, not adjectives** `[lihfolk]`. One style direction in a phrase, 3–5 reference screenshots, what to take (palette logic, shape language, hierarchy) and what to leave (logos, characters, exact art). Never trace or ship reference art. The UI should let a player name the genre from a screenshot.
2. **Pick the direction from the game, not from fashion.** Vocabulary for briefs `[lihfolk]`, each a bundle of colour, shape and one signature detail: chunky simulator (deep neutral canvas, bevelled slabs, rays behind featured items), toy brick (one primary per menu on white, dark outline, stud dots), pastel cute (low-saturation pills, hairline strokes), storybook (paper, framed panels, small radius), neon tech (near-black, clipped corners, two electric accents), battle (slanted shapes, speed lines), dread (desaturated, sharp, one sickly accent), flat pro (greys, one action colour, spacing does the work), scoreboard (team colours, big numerals). Examples: `visual-library/ui-components-and-style.md` §1 (kits and style directions, with template kits marked for comparison). A kit reads as one family when four numbers never change (outline weight, lip depth, highlight angle, corner radius) and it carries one motif from the game's world that could not be moved to another game unchanged (#1–#4 there, against #8–#10).
3. **Turn the direction into tokens** (§2–5), then into components (§6). Nothing else may hold a raw value.
4. **Stress-test before committing** `[lihfolk]`: mock five screens in the candidate style: HUD over a busy scene, shop card with a price, a 30-item inventory, a reward moment, settings rows. A style chosen on one screen fails on the dense list.
5. **Design the most complex screen first** (usually shop or inventory): it forces most of the component set, after which other screens are assembly `[community]`.
6. **Components own every number** `[lihfolk]`: screens call builders such as `Components.header(panel, title)`; a one-off look is an explicit attribute that every re-skin pass checks.
7. **Make mass edits reversible** `[lihfolk]`: before a sweep, store the old value in an attribute (`Pre_Font`, `Pre_Color`); `UDim2`, `Color3` and `Font` are valid attribute types `[official]`.

State matrix: draw and build every state before shipping a component; most visual bugs are missing states `[lihfolk]`.

| Component | States |
|---|---|
| Button | default, hover, pressed, gamepad-focused, disabled (with reason), pending (request in flight) |
| Claim / buy | available, pending, done (kept visible with a tick), locked (with the requirement) |
| Tab | idle, active, has-badge, focused. Active ("this page is open") and focused ("the cursor is here") must differ |
| Card / slot | default, selected, equipped, locked, new, empty |
| Toggle, slider, segmented | each value, disabled, focused; a toggle moves the knob and changes a word or icon, not only colour |
| Text field | empty with a label outside the field (not placeholder only), focused, filled, error. It must look typeable `[community]` |
| Progress bar | empty (minimum sliver), filling, full, completed |

One shared close button `[lihfolk]`: a square about 1.1× the header height (`SizeConstraint = RelativeYY`), anchored at the header's top-right, `Danger` colour, white X: the convention the docs describe `[official]`. Keep `ClipsDescendants` off the header and panel, and keep the overhang inside the fade group's margin (§6 Window).

## 8. Generic and AI-look tells, with the fix

In 2026 feedback threads, reviewers dismiss a game at the first screenshot when the UI "looks AI", and they name the cues `[community]`. Rows marked A come from those threads; D are default-Studio tells; C are recurring critique corrections; L come from the captures rejected while building the visual library (each `visual-library/ui-*.md` ends with "What the weak examples had in common"; row numbers cite its entries); H are house observations.

| | Tell | Fix |
|---|---|---|
| A | Too much information on the first screen: stats, subtitles and cards nobody asked for | Three reads (§1). "Remove things, do not add more." Numbers the player compares become meters or icons |
| A | Thin saturated strokes on dark, slightly transparent rounded panels; bright pastel accents | One outline weight in one near-black; opaque surfaces from the world's palette (§3) |
| A | A panel behind every HUD number (ammo box, coin box) | Icon + outlined number straight on the world, as the HUDs that read best when shrunk do (`ui-hud.md` #1, #6, #24 against the commissioned kits #10–#12) |
| A | Rounded "friendly dashboard" shapes in a genre that wants edges; the same look for a horror game and a pet game | Shape language from the brief (§7): the UI must name the genre |
| H | Purple-to-blue or cyan-to-magenta gradients; glow on every button; emoji used as icons | One-hue gradients ≤ 10% (§6); one authored icon family (§5) |
| H | Perfectly even emphasis: every card the same size, every button filled | Size tiers with ratio ≥ 1.25; one filled action per screen |
| L | Variety by recolour: one bevel in ten hues, or five buttons in five unrelated saturated colours with no rule for which colour means what (`ui-components-and-style.md` #8, #9; `ui-screens.md` #3 against #2) | Colour by function (§3): one colour per destination, kept everywhere |
| L | No motif from the game's world: the kit could be pasted into any game, and players read it that way (`ui-components-and-style.md` #8–#10 against #1–#4; `ui-screens.md` #1, #4, #7) | One signature detail taken from the world's materials or shapes (§7) |
| L | A kit shown only at rest: no pressed, disabled or selected variant; placeholder strings ("000 Robux", "(CLICK TO PURCHASE)") | State matrix (§7); mock with the longest real strings and largest numbers (`ui-screens.md` #11, #56) |
| L | Text standing in for icons (hotbar slots as words, `Cash:` captions) and text a few px tall once the capture is shrunk to 800×360 (`ui-hud.md` #2, #6) | Icon + number; check every screen shrunk to `Phone-S` before judging it |
| L | Decoration standing in for content: glow, sunbursts and shards round empty cards; chrome and neon gradients; a concept shown over a blurred backdrop, so contrast was never tested | Effects table in §6; design over real gameplay screenshots |
| H | AI-generated item icons or thumbnails: styles differ from icon to icon, details melt | Render icons from the Blender assets with one rig (house rule) |
| D | Default grey frames, `SourceSans`, square corners, 1 px borders | Theme module; one display font; one radius family; 2–3 px outline |
| D | Stretched icons, squashed round buttons on wide phones | `UIAspectRatioConstraint` on every button, icon and image; 9-slice panels |
| D | Blurry art; dark fringes around transparent PNG edges | Export 2× (≤ 1024); alpha-bleed exports before upload (§13) |
| C | Mixed fidelity: crisp buttons beside a pixelated or differently drawn icon | One icon family; redraw or drop the odd one out |
| C | Uneven padding, borders that do not line up, off-centre icons and captions | 4 px scale, layouts instead of hand placement, optical centring (§2) |
| C | Different text size per label in one group | Fixed type scale; `TextScaled` only for short numerals with `UITextSizeConstraint` |
| C | Two fonts fighting (logo font on one button, body font on the next); a decorative display face on text that must be read | Two families with fixed jobs (§4) |
| C | Round and square corners in one UI; close button in a different place or colour per window | One radius family; one shared close component, top-right |
| C | A pattern applied on one window and missing on the next (plate behind text here, bare text there; one page without the open animation) | Components and motion tokens; review screens side by side |
| C | Empty windows with tiny content, or controls crammed to the edge | Size the window to its content; 16 px padding |
| C | Buttons on two or more edges, including the thumb zones | One home edge outside the reserved zones (`ui-input-crossplatform.md` §Mobile layout) |
| C | The whole UI baked into one image | Native structure and text; images only for art |
| C | Black text on a deep saturated button; white on a mid-tone one; captions in a darker shade of their own button hue; yellow on white; red on red or on black | `OnAccent` by measured contrast (§3) |
| H | Copy of a hit game's skin, or a bought template pack (the same tilted purple panel, green 3D button and seven identical day cards in every game that bought it: `ui-screens.md` #43) | Copy the layout convention, never the art, logo or palette |

## 9. Critique rubric (0–10, observable)

Score each row 1 (passes), 0.5 (one exception) or 0. Run it on phone-size screenshots over busy gameplay, per screen, by someone who did not build the screen. Under 6: rebuild from tokens. 6–7.5: fix the failing rows. 8 or more: polish and ship.

| # | Criterion | Observable test |
|---|---|---|
| 1 | One-second read | Blur and greyscale copies (§1): the three elements that stand out are the intended three |
| 2 | Tiers | At most 3 size tiers on the screen; exactly one saturated filled action |
| 3 | Spacing | Every gap and padding is on the 4 px scale; group gaps ≥ 2× inner gaps; no two rows of one list differ in height |
| 4 | Alignment | Every element sits on a shared edge or centre line; captions and icons within 1 px of optical centre |
| 5 | Colour | No colour outside the theme; one fully saturated hue plus rarity; text passes contrast on the brightest and darkest screenshot; states readable in greyscale |
| 6 | Type | At most 2 families and 4 sizes; nothing drawn under 12 px (design floor 14); the stroke test string reads |
| 7 | Icons | One family; 4 of 5 outsiders name each icon at 32 px; no baked text |
| 8 | Consistency and states | One close, one radius family, one outline weight; every component has its full state matrix including pending, disabled with reason and focus |
| 9 | Touch and zones | Targets ≥ 44 px (48 on the HUD), gaps ≥ 8; nothing interactive in the stick or jump zones; passes at 667×375 with chat open |
| 10 | Identity | With the logo hidden, the screenshot belongs to this game (palette from the world, shape language, one signature detail); zero rows of §8 apply; no third-party or generated art |

## 10. Redesigning an existing ugly UI

1. **Freeze behaviour.** Tag every scripted hook (`UiHook` attribute), capture each screen at 667×375, 844×390 and 1920×1080, and note the baselines the redesign must not hurt: shop opens per session, tutorial step completion by device, purchase conversion.
2. **Inventory and cut.** Dump the tree (audit scan in `ui-input-crossplatform.md`), list every element, mark what players use. Remove or demote until removing more would hurt play.
3. **Score** every screen with §9 so the worst screens are known and the result is measurable.
4. **Rank** each screen's elements into the three reads.
5. **Grey-box** the new layout in rectangles over real screenshots, in greyscale, with reserved zones drawn and the chat and player list open `[official]`. Fix layout here, where it costs minutes.
6. **Derive tokens** from the world (§3–4). Keep existing art that fits and re-purpose it on the new layout; a redesign is not a redraw (Sonic Racing's Apple Arcade rework kept most assets `[community]`).
7. **Rebuild the components once** (§6), starting from the most complex screen.
8. **Ship screen by screen behind a Config flag**, HUD and the highest-traffic window first; compare the baselines, and use Experiments where a layout touches conversion `[official]`.
9. **Re-score, delete the old assets, re-run the audit.** Record before and after screenshots and scores in the milestone review.

## 11. Frames and scale

| Figma frame | Size | Purpose |
|---|---|---|
| `Phone-S` (design here first) | 800×360 `[house]` | Smallest landscape phone; everything must work here |
| `Phone-Narrow` | 667×375 | Every HUD overlap shows here first `[lihfolk]` |
| `Phone-Notch` | 844×390 (also 932×430) | Notch on either side |
| `Tablet` | 1024×768 | Thumb reach differs: a button 40% from the top is reachable on a phone, not on a tablet `[official]` |
| `Desktop/TV` | 1920×1080 | Same components; `UISizeConstraint` max so panels do not balloon `[official]` |

- A phone's viewport is not its physical resolution: print `workspace.CurrentCamera.ViewportSize` on the target phone and add that frame `[house][VS]`.
- Every frame carries locked overlay layers (prefix `skip_`): thumbstick zone, jump button, top-bar strip, with the numbers from `ui-input-crossplatform.md` §Mobile layout.
- Size from the short side: element height by scale, shape locked with `UIAspectRatioConstraint` or `SizeConstraint = RelativeYY`; offsets for margins, padding and strokes.
- **Conflict:** LihFolk designs at 1920×1080 and adds a phone arrangement for any screen that would draw text under 12 px. This skill designs the phone frame first (house rule) and widens it. Both end with a real phone layout rather than a shrunken desktop one.

## 12. Figma and the Figma MCP

What to give the designer (human or agent) before any frame is drawn: the style direction and references with take/leave notes; the audience age band and platform split; the three reads per screen; the token table; the screen list with every state; the reserved-zone overlays; two gameplay screenshots per zone of the game.

Tool names are those of the official Figma MCP as connected to this skill's operator `[VS]`. Tools that read from Figma are rate-limited by plan and seat `[community]` (Figma's developer docs, read 2026-11-11): View or Collab seat, 20 calls a month on every plan; Full or Dev seat, 200 a day on Professional (10 a minute) and Organization (15 a minute), 600 a day on Enterprise (20 a minute); the Starter plan has no higher tier. Some tools are exempt, including those that write to files (the docs name `create_new_file`, `generate_figma_design`, `add_code_connect_map` and `whoami`). Batch reads and avoid repeat screenshots.

1. **Load the server's skills first**: `/figma-use` before `use_figma`, `/figma-design-to-code` before `get_design_context`, `/figma-generate-design` for full screens (fallback: `get_figma_skill`).
2. **File and session.** `whoami` → `create_new_file` → `create_session` once; pass `sessionId` to every later call. For an existing file parse `fileKey` and `node-id` from the URL (`1-2` → `1:2`).
3. **Tokens before pixels.** `use_figma`: variable collections `Color`, `Space`, `Radius`, `Stroke`, and text styles for the type scale, named exactly as the theme keys (`Color/Primary`).
4. **Components before screens.** Button (role × state), Panel, Card, CurrencyReadout, Tab, Badge, Toast, Slot, Close. Frames with auto layout, never Groups. Layer name = Roblox instance name. Prefixes: `Img_` rasterise as one PNG, `Btn_` button, `Scroll_` ScrollingFrame, `Txt_` runtime text (placeholder = longest expected string +30%), `skip_` guides.
5. **Compose at `Phone-S`** over gameplay screenshots (`upload_assets` places them) and the zone overlays; then reuse the same components in the other frames. Never scale a desktop design down.
6. **Self-critique.** `get_screenshot` (raise `maxDimension` above the 1024 default for detail), then score with §9 and check §8. Fix in Figma, where iteration is cheap.
7. **Extract.** `get_metadata` (tree and geometry) → `get_design_context` per screen → `get_variable_defs` → `download_assets` per `Img_` node (png, scale 2–3; URLs expire). The reference code is React + Tailwind: a spec to read, never to transliterate. `get_motion_context` returns keyframes and easing for prototyped motion: map them onto the tokens in `ui-motion-and-feedback.md`.
8. **Build and verify** in Studio per §14.

- `generate_image` spends Figma AI credits per image and produces AI art: throwaway ideation only, never a shipped pixel (house rules: no AI-generated art ships). `generate_figma_design` captures web pages; it is not for Roblox.
- Level-up mode: dump the live ScreenGui tree with Studio MCP `execute_luau`, `screen_capture` each screen, rebuild it in Figma as the baseline frame, redesign beside it (§10), ship the diff screen by screen.
- Never hand-edit a generated builder: fix the Figma file or the generator and regenerate; keep states and motion in a separate controller `[lihfolk]`.

### px → Roblox

For a node `(x, y, w, h)` inside parent `(pw, ph)`, coordinates relative to the direct parent (Figma metadata is absolute), anchor `(ax, ay)` `[community]`:

```
Size      = UDim2.fromScale(w / pw, h / ph)
Position  = UDim2.fromScale((x + w * ax) / pw, (y + h * ay) / ph)
Corner    = UDim.new(math.min(0.5, r / math.min(w, h)), 0)   -- scale is relative to the shorter side [official]
Aspect    = UIAspectRatioConstraint.AspectRatio = w / h      -- root panels, buttons, icons, exported images
Gap / pad = px offsets for small fixed spacing; scale only when the container itself scales
```

- Anchor by intent: edge-pinned HUD on its edge; fill bars `(0, 0.5)`; anything that scale-tweens, and centred panels, `(0.5, 0.5)`.
- Alternative `[lihfolk]`: keep every size in Offset exactly as drawn and put one fit `UIScale` on the screen root (`ui-input-crossplatform.md` §Containers, "Sizing strategies"); pixels then map 1:1, which is what generated builders should emit.
- **Conflicts with import skills:** they set `TextScaled = true` everywhere, and one bans `UIScale`. House rules and the reasons: `ui-input-crossplatform.md` §Text (fixed `TextSize`, `TextScaled` only for short numerals) and its `UIStroke` note under §Containers (keep the root `UIScale`; never combine it with `TextScaled` text that carries a scaled stroke).

Mapping traps `[lihfolk]` (compare a Studio capture with the Figma screenshot after each):

| Figma | Roblox | Trap |
|---|---|---|
| Linear gradient handles | `UIGradient.Rotation` in degrees, white background | Handles are normalised to the box: convert to pixels first. Roblox spreads stops edge to edge, Figma pins them to the handles: rescale the stops |
| Radial / angular gradient | `UIGradient.Type` Radial, Elliptical or Conical `[VS]` | Check banding on dark gradients on a device |
| Stroke align Inside / Center / Outside | `BorderStrokePosition` Inner / Center / Outer | Outside strokes add to the box and ignore layout: reserve the space |
| Drop shadow, inner shadow | `UIShadow`, `Inset = true` for inner | Roblox blur was retuned toward CSS during beta `[official]`: match by eye against the blur ladder in `visual-library/ui-components-and-style.md` #27, not by number |
| Mixed corner radii | `UICorner.TopLeftRadius` and its three siblings | `CornerRadius` now sets all four and reads the top-left: do not set both, above all in style rules `[official]` |
| Rotated node | `Rotation` + the node's own size | The bounding box of a rotated node is not its size |
| Hug contents | `AutomaticSize` | A fixed size makes translated text overflow |
| Image fill Fill / Fit / Tile | `ScaleType` Crop / Fit / Tile | Crop the PNG yourself rather than rely on a transform |
| Letter spacing | none | Roblox text has no tracking: design with 0 |
| Layer blur, background blur, blend modes, masks | none | Bake into the PNG, or redesign |
| Font size 12 in a 1080p frame | about 4 px on a 667×375 phone (scale 0.347) | Design text at `Phone-S` (≥ 14 px there); a 1080p frame would need about 35 px text to draw 12 on that phone, so phones get their own arrangement (§11) |

## 13. Export, upload, converters

| Topic | Rule | Tag |
|---|---|---|
| Format | PNG with alpha, cropped to visible bounds plus 2 px transparent padding | `[community]` |
| Edge fringe | Transparent pixels still carry RGB; texture filtering samples it and draws a dark or light fringe on scaled images. Alpha-bleed every export (PixelFix-style tools extend edge colour into transparent pixels) | `[community]` |
| Resolution | Longest side ≤ 1024 px: export 2× the largest on-screen size (3× for small icons). 4K texture streaming (Jan 2026) lists MeshPart, SurfaceAppearance, Texture, Decal and MaterialVariant; GUI images are not on the list | `[official][VS]` |
| Memory | Cost follows pixel count, not file size: 1024² costs 4× a 512² | `[official]` |
| Text | Hide text layers before export; rebuild as TextLabel. Baked text cannot be localised, resized or read by a screen reader | `[community]` |
| Colour variants | One white or grey base tinted with `ImageColor3`; one slot image serves every rarity | `[community]` |
| 9-slice | Stretchable textured panels, bars, buttons: export small (128–256 px, about `2 × inset + 8` per side), `ScaleType = Slice`, `SliceCenter`, tune `SliceScale`. `UICorner` on a sliced image rounds each slice separately, and a fix listed as live in the v722 release notes was reported as not working (bug reports of Jul and Aug 2026): bake the corners | `[official][community][VS]` |
| Sprite sheets | Many small icons → one ≤ 1024² sheet, `ImageRectOffset`/`ImageRectSize`, 2 px gutter | `[official]` gutter `[house]` |
| Tiling | Stud and noise textures: `ScaleType = Tile` + `TileSize`; never stretch a texture | `[official]` |
| Upload | Studio MCP `upload_image` (batch), Open Cloud Assets (`.png .jpeg .bmp .tga`, ≤ 20 MB), or Asset Manager bulk import. Every image is moderated and blank until approved | `[official][VS]` |
| Third-party art | Kits and packs are references unless the licence clearly allows shipping; Studio MCP `generate_*` and `insert_asset` stay off-limits for shipped content | `[house]` |

Converters and agent skills (GitHub metadata checked 2026-11-10; DevForum threads read 2026-11-11). Low star counts everywhere: treat converters as accelerators and audit their output. Community cost of hand import: about 30 minutes per frame, or more than $10 a frame when outsourced `[community]`. `lopi-py/figblox` and `EgoMoose/figma-to-roblox-ui` are stale or archived (2023–2024): do not start there.

| Tool | Status | What it does |
|---|---|---|
| `NoTwistedHere/Figma-to-Roblox` | 32★, 2026-08, MPL-2.0 | Figma plugin → `.rbxmx`, name-driven, Open Cloud upload |
| `xtrair/figma-to-roblox-ui` | 7★, 2026-09, MIT | Agent skill: Figma MCP + Studio MCP, validator. Its Scale-only and `TextScaled` rules conflict with §12 |
| `grim-technologies-arch/ui-figma-roblox` | 22★, 2026-10, MIT text | Agent skill for stud-style UI with a verified Studio port; bundled art has no clear licence |
| `lihfolk-cy/v2-vault` (`skills/lihfolk-figma`) | CC BY 4.0 text | Property-mapping contract and a Figma-JSON → Luau builder (Offset + fit `UIScale`). Read for method |
| `MarkRuiz00/RbxUiStudio`, `RaRdq/FigmaRobloxForge`, `astrorehan/figlo`, `MiaGobble/Figma-Import-Assistant` | 1–18★, 2026 | Teardown notes and editor; rasterise-everything exporter (many uploads, more texture memory); relay plugin (alpha); manual-import assistant |
| `cameronpcampbell/supercorner` | 16★, MIT | Squircle corners as generated 9-slice images |
| RoImport (free), UILint v2, GuiForge (free, browser editor), Bloxporter (paid, about $20 a month) | DevForum, 2025–2026 | Tag-driven Figma → Studio importers; UILint also lints overlap, overflow and scaling |

## 14. Hand-off checklist: Figma to Studio

- [ ] Variables and text styles carry the theme key names; no detached styles, no raw hex on any layer.
- [ ] Every component has its state matrix as variants; every screen exists at `Phone-S` and `Desktop/TV`, with empty, locked, error and longest-string cases.
- [ ] Each layer is classified: native (default), `Img_` (art), `Txt_` (runtime text), `skip_` (guides). No text inside any `Img_` export.
- [ ] Manifest committed: layer name → asset id, export scale, slice insets, tint role.
- [ ] Exports are alpha-bled, ≤ 1024 px, white where tintable; icons share one sheet where practical.
- [ ] Build order: ScreenGui (`ResetOnSpawn = false`, `ZIndexBehavior = Sibling`, `ScreenInsets = CoreUISafeInsets`) → containers and layouts → native visuals → images → text; one builder script per screen (Studio MCP `execute_luau` in the Edit datamodel, or Rojo-owned code).
- [ ] Motion spec attached per screen as token names (`enter`, `press`, …), not durations.
- [ ] Studio `screen_capture` at phone, tablet and desktop matches the Figma frame (overlay at 50% to compare); UI audit scan clean; rubric ≥ 8; then the real 3 GB Android phone.

## 15. Theme module (unexecuted sketch)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Theme.luau. Generated from Figma variables; edit in Figma, then regenerate.
-- PLACEHOLDER palette, the one the bundled sheets are drawn in. It must not ship: derive every colour, font,
-- radius and stroke from the game (section 3), then set Placeholder = false. The boot script warns while it is true:
--   if Theme.Placeholder then warn("UI theme is the placeholder: derive it (ui-design-figma.md section 3)") end
-- Label ink is measured, not assumed: On passes 4.5:1 on Base and Light (ratios in section 3).
local function ramp(hex: string, light: string, dark: string, on: string)
	return table.freeze({
		Base = Color3.fromHex(hex), Light = Color3.fromHex(light),
		Dark = Color3.fromHex(dark), On = Color3.fromHex(on),
	})
end
return table.freeze({
	Placeholder = true,
	Color = table.freeze({
		Surface = Color3.fromHex("#26324A"), SurfaceAlt = Color3.fromHex("#3A4A6B"),
		Ink = Color3.fromHex("#FFFFFF"), InkMuted = Color3.fromHex("#C8D2E3"),
		Outline = Color3.fromHex("#1A1F2B"), DangerInk = Color3.fromHex("#FFA3A3"),
		Focus = Color3.fromHex("#FFFFFF"),
	}),
	Role = table.freeze({
		Primary = ramp("#35B25D", "#3FC76C", "#1F7A3D", "#1A1F2B"), -- white only with an Outline stroke
		Premium = ramp("#F0B63A", "#F6C95C", "#B07A10", "#1A1F2B"),
		Danger = ramp("#CF2E3E", "#D93446", "#9E2233", "#FFFFFF"),
	}),
	-- Hue in the familiar order, OKLab lightness rising 0.55 -> 0.87; cards also carry a name and pips.
	Rarity = table.freeze({
		Common = Color3.fromHex("#6A7382"), Uncommon = Color3.fromHex("#2F9E55"),
		Rare = Color3.fromHex("#4A98E8"), Epic = Color3.fromHex("#B48BF5"),
		Legendary = Color3.fromHex("#F0B63A"), Mythic = Color3.fromHex("#FFC0D9"),
	}),
	Font = table.freeze({
		Display = Font.fromEnum(Enum.Font.FredokaOne),
		Body = Font.fromEnum(Enum.Font.BuilderSansBold),
	}),
	TextSize = table.freeze({ Caption = 14, Body = 16, Hud = 20, Title = 24, Display = 30 }),
	Space = table.freeze({ XS = 4, S = 8, M = 12, L = 16, XL = 24, XXL = 32 }),
	Radius = table.freeze({ S = UDim.new(0, 8), M = UDim.new(0, 12), L = UDim.new(0, 16), Pill = UDim.new(0.5, 0) }),
	Stroke = table.freeze({ Regular = 3, Thin = 2, TextRatio = 0.07 }),
})
```

Studio-authored screens can mirror the same tokens as `StyleSheet` attributes and drive buttons by tag selectors; styling, `StyleQuery` and transitions are fully released `[official]` (status and limits in `ui-input-crossplatform.md`). The Motion module is in `ui-motion-and-feedback.md`; the window presenter in `ui-input-crossplatform.md` §UI architecture.

## Level-up: UI look symptoms → cause → fix

Engine symptoms (safe areas, input, performance) are in `ui-input-crossplatform.md`; motion symptoms in `ui-motion-and-feedback.md`.

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| "Looks like a free model" or "looks AI" in comments; low thumbnail-to-play trust | No design system; rows of §8 apply | Score with §9; redesign procedure §10, HUD and shop first |
| New players miss the main loop button | No read-1 tier; many equal buttons | Three reads; one filled action; badge only on the next useful action |
| "Too much on screen" | Read-3 content on the HUD; a panel behind every number | Cut to the budget in §1; move object data into the world |
| "Colours hurt" or "it's bland" | Several saturated hues touching, or no role colour at all | Roles and the 60/30/10 split (§3) |
| Shop conversion low although traffic is fine | Buy button not the brightest element; price baked in art, unreadable under a thick stroke, or bare white on a mid-tone fill | One `Primary` button per card, native price text, stroke ≤ 7%, label ink by measured contrast (§3); `monetization-and-policy.md` |
| Players do not understand an icon | Abstract or adult metaphor; no caption | Naming test (§5); caption until found |
| UI and world look like two games, or like the bundled sheets | Theme chosen apart from the art bible, or the §15 placeholder shipped | Derive the theme from four inputs (§3); shape language from the brief (§7) |
| Soft or fringed art; client memory up after a UI update | 1× exports without alpha bleed; dozens of 1024² uploads, one image per colour | Re-export 2–3× (≤ 1024) and alpha-bleed (§13); native recipes, tinted bases, sprite sheets, 9-slice |
| Re-skin takes weeks | Colours and sizes hard-coded per instance | Theme module or `StyleSheet` tokens; components own numbers |

## Review gate

- [ ] Three reads written for the HUD and each window; blur and greyscale test passed at phone size over busy gameplay.
- [ ] Tokens exist in Figma and in `Theme.luau`; no raw colour, font, size or spacing elsewhere; the four inputs of §3 are written above the theme, `Placeholder = false`, and the line-up check against three competitors passed.
- [ ] Every text-on-fill pairing in the token table has a measured ratio written beside it: 4.5:1 text, 3:1 large text and icons, 3:1 disabled; rarity ramp rises in lightness and each tier carries a name or pips.
- [ ] One icon family; item icons rendered from the Blender assets; naming test passed; no generated or third-party art shipped.
- [ ] Components built from §6 with full state matrices; effects within the 300-stroke and 100-shadow budgets; nothing depends on an unreleased or beta-only property.
- [ ] Zero rows of the tells table (§8) apply; rubric (§9) ≥ 8 on every screen, scored by someone who did not build it.
- [ ] Designed at `Phone-S` first with zone overlays; checked at 667×375, notch phone, tablet and 1080p.
- [ ] Hand-off checklist (§14) complete; Studio captures match the Figma frames; verified on a real 3 GB Android phone.
- [ ] No timer, discount or scarcity element that is not literally true (house rule 3).
- [ ] `ui-screen-recipes.md`, `ui-motion-and-feedback.md` and `ui-input-crossplatform.md` gates passed for the screens in use.

## Sources

Accessed 2026-11-11 unless noted. "(read)" = opened and read at source; "(viewed)" = image looked at; "(oembed)" = video verified to exist, not watched; "(search summary)" = not opened.

- `Roblox/creator-docs` mirror, commit `7cbffff` (read): `production/game-design/ui-ux-design.md`; `tutorials/curriculums/user-interface-design/choose-an-art-style.md`, `wireframe-your-layouts.md`; `ui/position-and-size.md`, `ui/appearance-modifiers.md`, `ui/9-slice.md`, `ui/styling/index.md`, `ui/styling/editor.md`; `art/modeling/texture-specifications.md`; class reference `UIStroke`, `UICorner`, `UIShadow`, `UIGradient`, `UIFlexItem`, `TextLabel`, `GuiService`, `CanvasGroup` (always clips its descendants); `includes/ui/clipping.md`; `production/publishing/accessibility.md` (the reduced-motion sample's full-screen fade group); `cloud/guides/usage-assets.md` (upload formats, 20 MB); enums `Font`, `GradientType`, `GradientTileMode`, `ApplyShadowMode`, `BorderStrokePosition`, `GuiState`: https://github.com/Roblox/creator-docs. Note: the mirror still shows beta alerts for gradients and shadows that the announcements below supersede.
- Roblox staff announcements on DevForum (read): UIStroke improvements, full release Dec 2025 https://devforum.roblox.com/t/3958036 · shadows and individual corners, full release Jun 2026 https://devforum.roblox.com/t/4636263 · upgraded UIShadow, full release Nov 2026 https://devforum.roblox.com/t/4934553 · upgraded UI gradients, full release Oct 2026 https://devforum.roblox.com/t/4846594 · UI styling https://devforum.roblox.com/t/4275082 · StyleQuery https://devforum.roblox.com/t/4566519 · styling transitions https://devforum.roblox.com/t/4646870 · 4K texture rendering https://devforum.roblox.com/t/4316229 · scaled-stroke bug report with staff reply https://devforum.roblox.com/t/4238464. Release dates, the 300-stroke and 100-shadow guidance and the shadow and corner property names re-read on 2026-11-11.
- DevForum bug reports (read): a `UIStroke` parented directly to a `CanvasGroup` ignores `GroupTransparency`, staff reply "as-designed" (2024) https://devforum.roblox.com/t/2880215 · `UICorner` on 9-slice images https://devforum.roblox.com/t/4713370 (Jul 2026), https://devforum.roblox.com/t/4779785 (Aug 2026)
- DevForum tutorials (read): UI Design Starter Guide (2017, 1,112 likes on the thread) https://devforum.roblox.com/t/53461 · The Ultimate UI Design Guide (2021) https://devforum.roblox.com/t/1236916 · A Guide to User Interface Design (2017) https://devforum.roblox.com/t/47526 · How to make extremely Clean UI while keeping good UX (2023) https://devforum.roblox.com/t/2438099 · UI Design and the Fundamentals (2021) https://devforum.roblox.com/t/1455805 · Professional UI Designer Raising Guides 101 (2020) https://devforum.roblox.com/t/476101 · 5 Tricks to improve your UIs (2021) https://devforum.roblox.com/t/1416491 · Customize your GUIs with builder icons (2025) https://devforum.roblox.com/t/3968755 · Automated PixelFix for UI (2026) https://devforum.roblox.com/t/4812286. Mostly mechanics; the craft rules here come from the critique threads and outside sources.
- DevForum critique threads, replies read (source of the C rows and §2–5 corrections): https://devforum.roblox.com/t/4859702, /t/4809265, /t/4823740, /t/4738500, /t/3098753, /t/764512, /t/756188, /t/317837, /t/4110542, /t/3166846, /t/4775592, /t/4706951, /t/2893476, /t/453803, /t/819976, /t/807561, /t/1170877, /t/4860297, /t/3676758
- DevForum threads on the "AI look" (read; source of the A rows): https://devforum.roblox.com/t/4960156, /t/4943365, /t/4526615, /t/3780811
- DevForum converter threads (read): https://devforum.roblox.com/t/3381689, /t/4731967, /t/4765869, /t/4834077, /t/4891173, /t/3501193
- Outside craft writing (read): Zach Gage, "Building Games That Can Be Understood at a Glance" (GDC 2018) via the GIGAZINE summary https://gigazine.net/gsc_news/en/20180501-game-design-subway-legibility and https://mgmarlow.pages.dev/words/2023-01-15-case-study-zach-gage (talk video, oembed: https://www.youtube.com/watch?v=YISKcRDcDJg) · "A simple 10-minute UI litmus test" https://www.gamedeveloper.com/design/a-simple-10-minute-ui-litmus-test · Anthony Stonehouse, "User interface design in video games" (2014) https://www.gamedeveloper.com/design/user-interface-design-in-video-games · Yowan Langlais, "Burrito Bison: Launcha Libre – UI Design Process" https://interfaceingame.com/articles/burrito-bison-launcha-libre-ui-design-process/ · Raffaele Lattanzio, "The UI & UX of Sonic Racing" https://interfaceingame.com/articles/the-ui-ux-of-sonic-racing/ · Epic, "Designing for Mobile in Fortnite" https://dev.epicgames.com/documentation/fortnite/designing-for-mobile-in-fortnite · NN/g, "Children's UX" https://www.nngroup.com/articles/childrens-websites-usability-issues/ · Google, "Designing engaging apps" (kids) https://developers.google.com/building-for-kids/designing-engaging-apps · Figma MCP rate limits and exempt tools (re-read 2026-11-11) https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ · Roblox Creators, "UI/UX Essentials" (oembed) https://www.youtube.com/watch?v=lOOvOIJoMi4
- GitHub READMEs and skills read on 2026-11-10: `xtrair/figma-to-roblox-ui`, `grim-technologies-arch/ui-figma-roblox`, `MarkRuiz00/RbxUiStudio`, `NoTwistedHere/Figma-to-Roblox`, `RaRdq/FigmaRobloxForge`, `astrorehan/figlo`, `MiaGobble/Figma-Import-Assistant`, `cameronpcampbell/supercorner`; star and push dates from the GitHub API that day (not refreshed: the API was closed to this session on 2026-11-11).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault) (read): `05 UI and UX/` UI Design Systems; UI Style Directions - A Visual Vocabulary for Briefs; Text Fonts and Rich Text; Figma Property Mapping for Roblox UI; Figma to Roblox UI - Pipeline and Handoff; Designing Roblox UI in Figma - Frames, Safe Areas and Tokens; `56 Field Notes/` Shared Close Buttons and Headers, UIStroke on Text; `skills/lihfolk-figma/SKILL.md`. Method adopted; its palette, kit and icon style were not.
- Figma MCP tool names as listed by the server in this session (names checked 2026-11-11, with the schemas of `get_screenshot`, `download_assets` and `get_motion_context` read; no tool was called): `whoami`, `create_session`, `create_new_file`, `use_figma`, `get_metadata`, `get_design_context`, `get_variable_defs`, `get_screenshot`, `download_assets`, `upload_assets`, `get_motion_context`, `generate_image`, `get_figma_skill`; `generate_figma_design` is named in the server's instructions and Figma's docs
- Contrast ratios in §3 (including both worked derivations) and §15: computed for this guide with the WCAG 2 relative-luminance formula; OKLab lightness after Björn Ottosson
- Not reachable: reddit.com, medium.com-hosted articles, GitHub API, gameuidatabase.com (the docs recommend it for icon research: browse it yourself, not opened).
