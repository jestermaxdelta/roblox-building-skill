---
name: vfx-and-audio
description: "Build and fix visual effects, game feel and sound in a Roblox game. Use when the user says \"the VFX is bad\", \"the effects look cheap\", \"combat feels flat / weightless\", \"hits have no impact\", \"add juice\", \"make it feel better / more satisfying\", \"the sounds are annoying / missing / too loud\", or asks for particles, beams, trails, ability effects, hit-stop, camera shake, SFX, music or mixing."
argument-hint: "[the action or effect]"
---

# VFX, game feel and audio

Make actions feel good: readable effects, timing that sells impact, and sound that supports it, within a phone's budget.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

**Start from references, not from memory.** Before designing anything here, open the library rows listed below, pick three to five references that fit this game's genre and tone, and look at them: bundled sheets open with the Read tool; for a linked image, download it to a temporary folder and Read it, or work from its "Look at it for" note if it cannot be fetched. Write down what to take from each (layout, hierarchy, palette, timing, shape) before building, borrow principles from several sources and never reproduce one. Work built from defaults is what makes a game look generic.

## What to read

| When | Open |
|---|---|
| Principles: shape, value, timing, layers, texture authoring, mesh effects, hit-stop, camera, budgets, generic-VFX tells, rubric | `${CLAUDE_PLUGIN_ROOT}/references/vfx-and-juice.md` |
| Build recipes for 21 effects with layers, property values and timings | `${CLAUDE_PLUGIN_ROOT}/references/vfx-recipes.md` |
| SFX design, starter sound lists, UI sound sets, mixing, the audio API, licensing | `${CLAUDE_PLUGIN_ROOT}/references/audio-sfx-music.md` |
| Input responsiveness, camera, reward sequence | `${CLAUDE_PLUGIN_ROOT}/references/game-craft.md` |
| Syncing effects and sound to animation markers | `${CLAUDE_PLUGIN_ROOT}/references/animation-and-rigs.md` |
| Reduced motion and photosensitivity limits | `${CLAUDE_PLUGIN_ROOT}/references/accessibility-and-player-qol.md` |
| Reference images and breakdowns of strong effects | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/vfx.md` |
| Tutorials, tools and texture sources | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/vfx-learning.md` |
| Sound references and libraries with their licences | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/audio-and-sound.md` |
| Bundled sheets: timing chart, layer anatomy, shape and value language (10–12) | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Effects are built on clients: the server sends one validated event, each client renders, the caster predicts. Never build or tween effects on the server.
- Climb the juice ladder from the cheapest rung: sound and a UI response first, then particles, then camera, then hit-stop.
- Timing sells impact: anticipation, a sharp hit, then follow-through. Hit-stop is client-only: none on light hits, at least 66 ms where it must be felt (50 ms is one or two frames at 30 FPS), at most 200 ms per stop and 140 ms in any 0.6 s.
- Scale burst counts yourself from the player's own effects preset and measured frame time, never from `UserGameSettings.SavedQualityLevel`. Never cull telegraphs or the player's own hit feedback to save frames.
- No camera roll in gameplay; shake is at most 2° of pitch and yaw and ends at exactly 0. Shake, flashes and hit-stop read the one comfort resolver (`accessibility-and-player-qol.md` §10), never the settings directly.
- Never carry gameplay information by post effects, shadows or sound alone: low-end devices drop them. Every information sound has a visual twin.
- Particles, beams and trails are not models; a mesh used as an effect is.
- Use only audio the owner has the right to use; keep an id manifest. Roblox's licensed Creator Store audio is licensed for use inside Roblox only: a trailer or clip posted elsewhere needs owned or commissioned sound. Every sound sits on a mix bus.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the action is unclear because the loop is unclear: use the `retention` skill.
- If effects are causing frame drops: use the `performance` skill.
- If the animation itself is the problem: use the `models-and-animation` skill.
- If it is a cutscene or camera sequence: use the `cinematics` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
