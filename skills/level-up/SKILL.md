---
name: level-up
description: "Audit and improve an existing Roblox game. Use when the user says \"make my game better\", \"review my game\", \"audit my game\", \"why is my game not growing / dying / losing players / not earning\", \"what should I fix first\", or shares stats (DAU, CCU, D1, D7, session time, conversion) for a Roblox game that already exists, even a prototype."
argument-hint: "[your game and any numbers you have]"
---

# Level up an existing Roblox game

The game already exists. The job is a ranked, evidence-based improvement plan, and then doing the top items. Not a rebuild, and not a design document for a game that already ships.

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
| A few numbers, no access | audit-existing-game.md §Numbers-only first pass, §2, §4, §Review gate; analytics-and-discovery.md §Benchmarks | 112 |
| Inspect read-only | audit-existing-game.md §5, §Operating rules, §House-rule debt track, §7, §Review gate; checklists.md §Gate 4 (scan: `scripts/studio/house_rule_scan.luau`) | 195 |
| Score the ten dimensions | audit-existing-game.md §3, §7, §Review gate; game-audit-report.md §2; tutorial-and-onboarding.md §13; core-loop-tuning.md §4; ui-design-figma.md §9; art-direction-and-quality-bar.md §8; icons-thumbnails-and-store-page.md §15 | 264 |
| Triage, rank, plan | audit-existing-game.md §4, §6, §2, §Review gate; game-audit-report.md §0, §4, §5, §6 | 201 |
| Ship a live fix safely | audit-existing-game.md §9; analytics-and-discovery.md §Experiments and Configs; engineering-architecture.md §Runbook; liveops-quests-retention.md §Shipping an update; checklists.md §Gate A | 157 |
| Genre level-up checklist | genres/<genre>.md §Level-up checklist for a live game, §Common failure modes, §Core loop with timings, §Review gate; genre-playbooks.md §Level-up, §Cross-genre rules, §Routing table | 120–129 |

## What to read

| When | Open |
|---|---|
| Always: the audit method, scorecard, triage tree and safe-change protocol | `${CLAUDE_PLUGIN_ROOT}/references/audit-existing-game.md` |
| The report to fill in (use the compact variant for a first pass) | `${CLAUDE_PLUGIN_ROOT}/templates/game-audit-report.md` |
| The genre's own level-up checklist | `${CLAUDE_PLUGIN_ROOT}/references/genre-playbooks.md` then one file in `${CLAUDE_PLUGIN_ROOT}/references/genres/` |
| Benchmarks and how to read the dashboards | `${CLAUDE_PLUGIN_ROOT}/references/analytics-and-discovery.md` |
| Gate A, and the house-rule scan in Gate 4 | `${CLAUDE_PLUGIN_ROOT}/references/checklists.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Fix in funnel order unless something is on fire: data loss, exploits and crashes first, then the first minute, the core loop, retention, monetisation, then growth. More players into a leaky first session are wasted.
- Every score needs evidence. With no live numbers, say so, score conservatively and state what you assumed.
- Count effort in the owner's real weekly hours.
- Prefer three fixes inside the same universe over a rebuild; ranking history lives with the universe.
- No live change without a baseline number, a Config flag and a rollback trigger.
- The pass is done when the top actions are shipped or handed over with exact steps, not when the report is written.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If players leave early or do not come back: use the `retention` skill.
- If it does not earn: use the `monetization` skill.
- If lag or crashes: use the `performance` skill.
- If exploits, dupes or lost data: use the `security-data` skill.
- If nobody finds the game: use the `growth` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
