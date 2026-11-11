---
name: retention
description: "Fix or design the core loop, first-time experience, tutorial, progression pacing and retention of a Roblox game. Use when the user says \"players leave after a minute\", \"nobody comes back\", \"low D1/D7\", \"short sessions\", \"my game is boring\", \"players don't know what to do\", \"the tutorial is bad\", or asks for quests, daily rewards, events, a season pass or an update plan."
argument-hint: "[what players do or where they leave]"
---

# Core loop, first session and retention

Players are leaving too early, or not returning.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

## What to read

| When | Open |
|---|---|
| Loop spec, scorecard, funnel reading, experiments, symptom table | `${CLAUDE_PLUGIN_ROOT}/references/core-loop-tuning.md` |
| Tutorials, the first minute, guidance devices, onboarding funnels and fixes | `${CLAUDE_PLUGIN_ROOT}/references/tutorial-and-onboarding.md` |
| Quests, daily rewards, events, season pass, LiveOps calendar, notifications | `${CLAUDE_PLUGIN_ROOT}/references/liveops-quests-retention.md` |
| Why it is or is not fun: motivation, flow, difficulty, progression theory | `${CLAUDE_PLUGIN_ROOT}/references/design-foundations.md` |
| How the genre's loop should run, with timings | `${CLAUDE_PLUGIN_ROOT}/references/genre-playbooks.md` then one file in `${CLAUDE_PLUGIN_ROOT}/references/genres/` |
| Pacing depends on cost curves | `${CLAUDE_PLUGIN_ROOT}/references/economy-and-progression.md` |
| How shipped games teach and what to study in each | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/tutorials-and-onboarding.md` |
| How hit games handle their first minute | `${CLAUDE_PLUGIN_ROOT}/references/case-studies-teardowns.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Fix the earliest broken stage first: load time and crashes, the first minute, the funnel, session length, D1, D7, D30.
- Control within 10 seconds of joining, first verb by 15, first reward by 30, first upgrade by 2 minutes, one new concept per beat. A timed hint appears after the time most players need plus 1 second (start at 11 s; test 5 s against 10 s).
- A next goal with its progress and its reward is always on screen.
- Reward layers (dailies, quests, passes) amplify a loop that works; they do not rescue one scoring under 5/10. Fix the loop first.
- Retention through content, collection, social play and seasons. Never through punishment: no streaks that reset, no pay-to-idle, no guilt notifications.
- One Config key per experiment. Under about 1,000 DAU, or when the dashboard's minimum detectable effect is larger than the effect expected, compare weekly new-user cohorts instead of running an A/B.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the loop works but feels flat: use the `vfx-and-audio` skill.
- If players leave because of lag or crashes: use the `performance` skill.
- If the leak is a confusing menu or HUD: use the `ui` skill.
- If prices or upgrade costs are the wall: use the `monetization` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
