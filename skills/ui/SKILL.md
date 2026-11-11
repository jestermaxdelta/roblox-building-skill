---
name: ui
description: "Design, build and fix Roblox UI and UX. Use when the user says \"my UI looks bad / cheap / generic / like AI made it\", \"the menu is broken on phone\", \"make a HUD / shop / inventory / settings screen\", \"the buttons are too small\", \"turn this Figma design into Roblox UI\", or asks about ScreenGui layout, scaling, safe areas, UI animation, controller or mobile input, accessibility or settings."
argument-hint: "[the screen or problem]"
---

# UI, UX and Figma

Make the interface look designed rather than default.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

**Start from references, not from memory.** Before designing anything here, open the library rows listed below, pick three to five references that fit this game's genre and tone, and look at them: bundled sheets open with the Read tool; for a linked image, download it to a temporary folder and Read it, or work from its "Look at it for" note if it cannot be fetched. Write down what to take from each (layout, hierarchy, palette, timing, shape) before building, borrow principles from several sources and never reproduce one. Work built from defaults is what makes a game look generic.

## Fast routes

Pick the row that matches the task and read only those sections, in that order, instead of whole guides. Guides are in `${CLAUDE_PLUGIN_ROOT}/references/` (`figma` = `ui-design-figma.md`, `recipes` = `ui-screen-recipes.md`, `input` = `ui-input-crossplatform.md`, `motion` = `ui-motion-and-feedback.md`); library files are in `${CLAUDE_PLUGIN_ROOT}/references/visual-library/`; sheets are `${CLAUDE_PLUGIN_ROOT}/assets/reference/NN-*.png`. §N is the section numbered N. For anything else, use the table under "What to read".

| Task | Read exactly | Look at | Lines |
|---|---|---|---|
| Redesign one screen | figma §Fast routes, §3, §4, §6, §9, §10 · recipes §1, §3, the screen's own section · input §UI architecture (from the `DisplayOrder` band plan to the presenter note) · motion §2, §8 | Sheets 03/04, 05, 09 · `ui-screens.md`, that screen's section (shops #1, #4, #10) · `ui-components-and-style.md` §1 #1–3 against #8 | ~350 |
| New HUD | figma §1–4, §6 · recipes §1, §2, §4 · input §Containers, §Mobile layout · motion §2 | Sheets 01, 02, 19 · `ui-hud.md` #1–28, "Start here" rows first | ~330 |
| Fix phone layout | figma §2, §4, §11 · input §Containers, §Text, §Mobile layout, §Level-up, the audit scan · recipes §1, §4 | Sheets 01, 19, 06 · `ui-hud.md` #4, #18, #20, #36 | ~270 |
| Motion and feedback | figma §3 "States" · motion §1–5, §7, §8, §Level-up · input, the presenter and its note | Sheets 05, 08 · `ui-components-and-style.md` #33, #38, #39 · `ui-screens.md` #67, #68, #72 | ~270 |
| Figma to Roblox | figma §3, §4, §7, §9, §11–15 · input §Containers | Sheets 06, 05 · `ui-components-and-style.md` #27–31, #47, #51 | ~310 |
| Critique a UI | figma §1, §3, §4, §8, §9, §Level-up · input, the pass criteria and §Level-up · recipes and motion §Level-up | Sheets 02, 09, 07 · the "weak examples" section of each `ui-*` library file | ~250 |

## What to read

| When | Open |
|---|---|
| Visual hierarchy, layout grid, colour and type systems, panels and buttons that look designed, Figma workflow, generic-UI tells, critique rubric, redesign procedure | `${CLAUDE_PLUGIN_ROOT}/references/ui-design-figma.md` |
| Build recipes per screen: HUD, shop, inventory, settings, codes, daily rewards, rebirth, notifications, loading | `${CLAUDE_PLUGIN_ROOT}/references/ui-screen-recipes.md` |
| Motion tokens, button feedback, reward sequences | `${CLAUDE_PLUGIN_ROOT}/references/ui-motion-and-feedback.md` |
| Implementation: scaling, safe areas, thumb zones, input mapping, gamepad focus, console and VR, UI performance, symptom table | `${CLAUDE_PLUGIN_ROOT}/references/ui-input-crossplatform.md` |
| Colour-blind safety, text size, reduced motion, settings menu, quality-of-life features | `${CLAUDE_PLUGIN_ROOT}/references/accessibility-and-player-qol.md` |
| Reference images: HUDs by genre | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/ui-hud.md` |
| Reference images: shop, inventory, menus, rewards and other screens | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/ui-screens.md` |
| Reference images and tools: buttons, icons, type, colour, panels, motion, kits | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/ui-components-and-style.md` |
| Bundled sheets: HUD anatomy, densities, shop, inventory, buttons, type, colour, rewards, template vs designed, thumb reach, icon sizes (01–09, 19, 20) | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Design at the small-phone frame first and scale up; never shrink a desktop layout.
- Native first: build buttons, panels, cards and bars from `UICorner`, `UIStroke`, `UIGradient` and `UIShadow` (recipes: `ui-design-figma.md` §6). Use an image only for texture, a silhouette that is not a rounded rectangle, or a repeated element needing more than about 10 instances. Images carry no text and are at most 1024 px on the longest side. Stay under 300 strokes and 100 shadows on screen.
- No colour, font, size or timing outside the theme module.
- Never hard-code the top-bar height or the jump-button position: read the insets.
- Pass lines, measured on the drawn result: text at least 12 px (design at HUD 18, body 16, captions 14), taps at least 44 px (48 on the HUD), gaps at least 8 px, no overlapping targets, at most 7 HUD groups, no signal carried by colour alone.
- Build the game's own look. Do not copy another game's style or a stock kit.
- With the Figma MCP: its output is a spec to translate, not code to paste.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the shop needs a product and pricing plan, not just a screen: use the `monetization` skill.
- If the UI is slow because the whole game is slow: use the `performance` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
