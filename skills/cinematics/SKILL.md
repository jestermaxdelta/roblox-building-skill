---
name: cinematics
description: "Create and fix cutscenes, camera sequences and trailers in a Roblox game. Use when the user says \"make a cutscene\", \"add an intro cinematic\", \"boss intro\", \"the camera movement is robotic / janky\", \"camera animation\", \"letterbox\", \"dialogue scene\", \"make a trailer\", or asks about scripted cameras, camera paths, Moon Animator camera work, skippable scenes or cinematic moments."
argument-hint: "[the scene or shot you want]"
---

# Cutscenes, cameras and trailers

Short, directed, skippable scenes that look intentional and never trap the player or freeze anyone else.

One of the focused skills in the `roblox-dev` plugin: a short set of instructions that points at the guides for this topic only. For planning or building a whole game, use the `roblox-game-design` skill.

## How to work

Follow this loop every time. It exists so the user gets a fixed game, not a lecture.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP's `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

**Start from references, not from memory.** Before designing anything here, open the library rows listed below, pick three to five references that fit this game's genre and tone, and look at them: bundled sheets open with the Read tool; for a linked image, download it to a temporary folder and Read it, or work from its "Look at it for" note if it cannot be fetched. Write down what to take from each (layout, hierarchy, palette, timing, shape) before building, borrow principles from several sources and never reproduce one. Work built from defaults is what makes a game look generic.

## What to read

| When | Open |
|---|---|
| When a cutscene earns its place, length budgets, shot design, camera paths and easing, staging, client-only architecture, skip and subtitles, tools, a timeline runner, amateur tells, rubric | `${CLAUDE_PLUGIN_ROOT}/references/cutscenes-and-cinematics.md` |
| Actors, animation playback and markers | `${CLAUDE_PLUGIN_ROOT}/references/animation-and-rigs.md` |
| Scene lighting and post-processing, and restoring them | `${CLAUDE_PLUGIN_ROOT}/references/lighting-and-atmosphere.md` |
| Stingers, ducking and scene audio | `${CLAUDE_PLUGIN_ROOT}/references/audio-sfx-music.md` |
| Motion comfort, reduced motion, subtitles | `${CLAUDE_PLUGIN_ROOT}/references/accessibility-and-player-qol.md` |
| An intro must not cost the first 30 seconds | `${CLAUDE_PLUGIN_ROOT}/references/tutorial-and-onboarding.md` |
| Reference: camera tutorials, modules, strong Roblox cinematics and trailers | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/cutscenes-and-cameras.md` |
| Bundled sheets: shot vocabulary and camera easing (13, 14) | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- A cutscene must earn its place: if the moment can be played, let the player play it. Keep scenes short and skippable after about 2 seconds.
- Client-only: the server changes game state before the scene and never waits on it. Never freeze other players. Late joiners, death and respawn each have a defined path.
- One restore function for every exit path (finish, skip, error, death, leave): camera, controls, HUD, lighting and sound return to what they were.
- No linear robot moves: one spline and one ease per shot, aimed with a look-at curve, constant-velocity paths, cuts instead of whip pans.
- Compose on purpose: choose shot size and field of view for the subject, keep lead room, respect the 180-degree line.
- Subtitles for all speech, paced for children; respect reduced motion; cap letterbox bars at about 10% of the height.
- Preload what the scene needs and stream the area in before cutting to it.
- Actors and props are Blender-authored like everything else; scene actors are local clones.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the animation of the actors is the problem: use the `models-and-animation` skill.
- If it needs effects or sound design: use the `vfx-and-audio` skill.
- If it is the game's tutorial rather than a scene: use the `retention` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
