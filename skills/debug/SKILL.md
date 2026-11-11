---
name: debug
description: "Find and fix bugs in a Roblox game. Use when the user says \"it's broken\", \"this script doesn't work\", \"I get an error\", \"infinite yield\", \"works in Studio but not in the real game\", \"it only happens sometimes\", \"players are stuck / rubber-banding / desynced\", \"memory keeps growing\", or pastes a Roblox error or stack trace."
argument-hint: "[the error or what goes wrong]"
---

# Debugging and testing

Get from "it's broken" to the cause quickly, fix the cause rather than the symptom, and leave a test behind.

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
| Method, tools, the symptom → cause → confirm → fix table, live-only bugs, leak hunting, tests | `${CLAUDE_PLUGIN_ROOT}/references/debugging-and-testing.md` |
| Language pitfalls and the deprecated → modern API table | `${CLAUDE_PLUGIN_ROOT}/references/luau-mastery.md` |
| Physics symptoms: flinging, jitter, ownership | `${CLAUDE_PLUGIN_ROOT}/references/physics-and-vehicles.md` |
| Animation symptoms | `${CLAUDE_PLUGIN_ROOT}/references/animation-and-rigs.md` |
| How the system should have been built | `${CLAUDE_PLUGIN_ROOT}/references/gameplay-systems-cookbook.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Reproduce before fixing: a written repro with its failure rate, then one sentence naming the cause.
- Never "fix" a bug with a wait or a silent `pcall`.
- After every yield, re-check the state you captured: the player may have left, the instance may be gone.
- Subscribe to the event, then iterate what already exists, with a guard against handling an item twice.
- "Works in Studio, dead live" has a short list of causes: not published or drafts not committed, an asset owned by another creator or a temporary id, a game setting (HTTP, API access, third-party teleports), latency and streaming races, `RunService:IsStudio()` branches. Check those first.
- A fix is done when the original repro, under the conditions that made it frequent, survives at least twice the run count it took to fail, and a test or a written manual test is left behind.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the bug is lag or a crash: use the `performance` skill.
- If the bug is lost data, a dupe or an exploit: use the `security-data` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
