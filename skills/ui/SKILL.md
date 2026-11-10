---
name: ui
description: "Design, build and fix Roblox UI and UX. Use when the user says \"my UI looks bad / cheap / generic\", \"the menu is broken on phone\", \"make a HUD / shop / inventory / settings screen\", \"the buttons are too small\", \"turn this Figma design into Roblox UI\", or asks about ScreenGui layout, scaling, safe areas, UI animation, controller or mobile input, accessibility or quality-of-life settings."
---

# UI, UX and Figma

Make the interface look designed rather than default, and work on a small phone first.

This is one of the focused skills in the `roblox-dev` plugin. It loads a small set of instructions and points at the guides for this topic only. For planning or building a whole game, use the `roblox-game-design` skill.

## How to work

Follow this loop every time. It exists so the user gets a fixed game, not a lecture.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP's `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`), and any numbers the user gave. If there is no access yet, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** Give a short ranked list (impact × confidence ÷ effort), the option you recommend, and one bolder alternative. Pitch it at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

## What to read

| When | Open |
|---|---|
| Design system, tokens, Figma MCP workflow, motion spec, nine screen recipes, polish checklist | `${CLAUDE_PLUGIN_ROOT}/references/ui-design-figma.md` |
| Implementation: scaling, safe areas, input mapping, console and VR, UI architecture and performance, symptom table | `${CLAUDE_PLUGIN_ROOT}/references/ui-input-crossplatform.md` |
| Colour-blind safety, text size, reduced motion, settings menu, quality-of-life features | `${CLAUDE_PLUGIN_ROOT}/references/accessibility-and-player-qol.md` |
| UI sounds and button feedback | `${CLAUDE_PLUGIN_ROOT}/references/audio-sfx-music.md` and `${CLAUDE_PLUGIN_ROOT}/references/vfx-and-juice.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are practice from other developers, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Design at the small-phone frame first and scale up; never shrink a desktop layout.
- Structure and text are native instances; artwork is exported images (9-slice). No baked text, nothing over 1024 px.
- No colour, font, size or timing outside the theme module.
- Never hard-code the top-bar height or the jump-button position: read the insets.
- Pass lines: text at least 12 px drawn, taps at least 44 px, 8 px gaps, and no signal carried by colour alone.
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
