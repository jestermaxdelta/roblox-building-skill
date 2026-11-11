---
name: performance
description: "Make a Roblox game run well. Use when the user says \"my game is laggy\", \"low FPS\", \"it crashes on mobile / phones\", \"it stutters\", \"long loading\", \"high ping\", \"server lag\", \"memory is too high\", \"optimize my game\", or asks about MicroProfiler, streaming, draw calls or part counts."
argument-hint: "[where it lags or crashes]"
---

# Performance and optimization

Measure, find the biggest cost, fix that, measure again. Target a 3 GB Android phone.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

## Fast routes

Pick the row that matches the task and read only those sections, in that order, instead of whole guides. Guides are in `${CLAUDE_PLUGIN_ROOT}/references/`; `game-audit-report.md`, `monetization-product-plan.md`, `economy-balance-sheet.md`, `launch-checklist.md` and `analytics-event-plan.md` are in `${CLAUDE_PLUGIN_ROOT}/templates/`. §N is the section numbered N; any other § name is the opening words of the heading. Lines is the reading cost. For anything else, use the table under "What to read".

| Task | Read exactly | Lines |
|---|---|---|
| Low FPS | performance.md §Measured investigation by problem class, §Profiling workflow, §Frame budgets and device targets, §Rendering, §Luau performance idioms, §Physics and collision, §Review gate | 197 |
| Phone crashes, memory | performance.md §Mobile crashes and memory, §Measured investigation by problem class, §Frame budgets and device targets, §Streaming, §Review gate; debugging-and-testing.md §Memory-leak hunting; art-pipeline-blender.md §Texturing strategy | 210 |
| Server lag, high ping | performance.md §Measured investigation by problem class, §Frame budgets and device targets, §Physics and collision, §Parallel Luau, §VFX, §Profiling workflow, §Review gate; networking-and-security.md §Designing the network surface | 188 |
| Slow join | performance.md §Loading and join, §Streaming, §Measured investigation by problem class, §Profiling workflow, §Review gate | 119 |
| Performance audit (live) | performance.md §Level-up audit, §Profiling workflow, §Measured investigation by problem class, §Frame budgets and device targets, §Rendering, §Review gate | 251 |
| Draw calls, triangles, textures | art-pipeline-blender.md §Level-up, §Platform limits and behaviours, §Mesh specifications, §Texturing strategy, §Collision authoring, §Modular kits, §Review gate; performance.md §Rendering, §Physics and collision | 162 |

## What to read

| When | Open |
|---|---|
| Budgets, MicroProfiler, investigation procedures A–E, streaming, rendering, physics, memory, crashes, audit scans | `${CLAUDE_PLUGIN_ROOT}/references/performance.md` |
| Scripted measurement and leak hunting | `${CLAUDE_PLUGIN_ROOT}/references/debugging-and-testing.md` |
| Art-side cost: triangles, textures, draw calls, collision fidelity | `${CLAUDE_PLUGIN_ROOT}/references/art-pipeline-blender.md` |
| Effect budgets and quality scaling (§11); audio voice limits and memory (§6, §10) | `${CLAUDE_PLUGIN_ROOT}/references/vfx-and-juice.md` and `${CLAUDE_PLUGIN_ROOT}/references/audio-sfx-music.md` |
| UI cost | `${CLAUDE_PLUGIN_ROOT}/references/ui-input-crossplatform.md` |
| Bandwidth and replication cost | `${CLAUDE_PLUGIN_ROOT}/references/networking-and-security.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Order of work on a live game: dashboards, then one real low-end phone, then read-only scans, then fixes.
- Never optimise without a capture: name the top cost from the MicroProfiler or the memory view first.
- House budgets: under 1,000 draw calls and 1 M triangles in the worst view, 30 FPS or better on low-end Android, 60 Hz server heartbeat.
- Streaming on, interactive models Atomic, `RequestStreamAroundAsync` before teleports; static geometry anchored; cheap collision (`Box`, `Hull` or a `_COL` proxy).
- Graphics tiers follow the player's own preset and measured frame time; never read `UserGameSettings.SavedQualityLevel`.
- Crowds are server data with pooled client models. Effects and UI updates are event-driven, not per-frame polls.
- Measure at the optimisation level the live game runs before reaching for `--!native`, `buffer` or Actors.
- Re-measure after each fix and report before and after.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the cost is a system built the wrong way: use the `systems` skill.
- If the crash is really a script error: use the `debug` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
