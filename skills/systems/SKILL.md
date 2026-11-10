---
name: systems
description: "Build and extend Roblox gameplay systems in Luau. Use when the user asks to \"make / add / script\" an inventory, shop, pets or egg hatching, quests, daily rewards, codes, leaderboard, rounds, teams, matchmaking, combat, abilities, NPCs or enemies, tycoon plots, placement, trading, crafting, checkpoints, vehicles or physics, or asks how to structure a Roblox codebase or write better Luau."
---

# Gameplay systems and Luau

Build the system properly the first time: server-authoritative, saved safely, and shaped to fit the rest of the game.

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
| 24 system designs: data shape, server/client split, remotes, validation, exploit surface, build order | `${CLAUDE_PLUGIN_ROOT}/references/gameplay-systems-cookbook.md` |
| Project structure, loader, Rojo layout, toolchain, live-update runbook | `${CLAUDE_PLUGIN_ROOT}/references/engineering-architecture.md` |
| Patterns in Luau: state, command, observer, pooling, ECS choice | `${CLAUDE_PLUGIN_ROOT}/references/architecture-patterns-luau.md` |
| Luau from first script to expert idioms; game math | `${CLAUDE_PLUGIN_ROOT}/references/luau-mastery.md` |
| Physics, network ownership, ragdolls, projectiles, vehicles | `${CLAUDE_PLUGIN_ROOT}/references/physics-and-vehicles.md` |
| Saving and purchases the system touches | `${CLAUDE_PLUGIN_ROOT}/references/data-and-purchases.md` |
| Remotes the system adds | `${CLAUDE_PLUGIN_ROOT}/references/networking-and-security.md` |
| Studio-native workflow, Script Sync or Rojo, the Studio MCP | `${CLAUDE_PLUGIN_ROOT}/references/studio-workflow.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are practice from other developers, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Remotes carry intent only: never amounts, prices, results, progress or time. The server validates and decides.
- No yield between a check and its write: that gap is where dupes live.
- Plain modules with a two-phase Init/Start loader by default; `--!strict` everywhere; untrusted input is `unknown`.
- Player data through ProfileStore with session locking; a failed load never saves.
- Crowds (enemies, pets, workers, droppers) are server data with pooled client-rendered models, never one Humanoid or physical part each.
- Never put damage or rewards on `Touched`; prefer spatial queries.
- Modern APIs only: `task.*`, no `wait`/`spawn`/`delay`, no BodyMovers. One function feeds both the displayed odds and the roll.
- Match the developer's setup: Studio-native for a beginner, Rojo for a team. Do not convert a project's workflow unasked.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If it is built but broken: use the `debug` skill.
- If it is built but exploitable or loses data: use the `security-data` skill.
- If it needs a screen: use the `ui` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
