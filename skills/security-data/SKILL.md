---
name: security-data
description: "Secure a Roblox game and keep player data and purchases safe. Use when the user says \"exploiters are ruining my game\", \"can this be exploited\", \"players duped items\", \"players lost their data / progress / coins\", \"data rollback\", \"they paid and got nothing\", \"is my game secure\", or asks about RemoteEvents, anti-cheat, DataStores, ProfileStore, ProcessReceipt, bans or backdoors."
argument-hint: "[what happened or what to check]"
---

# Security, anti-exploit, saving and purchases

Assume the client is hostile and the server can crash at any line. Protect the players' data and money first.

One of the focused skills in the `roblox-dev` plugin: a short set of instructions that points at the guides for this topic only. For planning or building a whole game, use the `roblox-game-design` skill.

## How to work

Follow this loop every time. It exists so the user gets a fixed game, not a lecture.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP's `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

## What to read

| When | Open |
|---|---|
| Remote review procedure, RemoteGuard, threat models per system, movement checks, bans, backdoor scans, audit steps | `${CLAUDE_PLUGIN_ROOT}/references/networking-and-security.md` |
| DataStore limits, ProfileStore, receipts, dupe classes, the trade commit protocol, migration, rollback and dupe-incident runbooks | `${CLAUDE_PLUGIN_ROOT}/references/data-and-purchases.md` |
| How each gameplay system is attacked | `${CLAUDE_PLUGIN_ROOT}/references/gameplay-systems-cookbook.md` |
| Enforcement, appeals and incident communication | `${CLAUDE_PLUGIN_ROOT}/references/community-moderation-safety.md` |
| Purchase policy | `${CLAUDE_PLUGIN_ROOT}/references/monetization-and-policy.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Never trust the client for ids, prices, damage, positions, currency or inventory. Remotes carry intent; the server decides.
- Every remote is validated and rate limited. Never use `RemoteFunction:InvokeClient`. No secrets or server logic in client-visible containers.
- A profile that failed to load never saves. Never change the key pattern of a live store. Snapshot before changing save logic.
- Purchases: never grant from a client signal, save the grant before returning `PurchaseGranted`, deduplicate by `PurchaseId`, one `ProcessReceipt` callback.
- No trading without item GUIDs, the commit protocol, an audit log and a kill switch.
- Any `require(<number>)`, `getfenv`, `loadstring` or obfuscated string is a finding until explained.
- Never ban on one signal or on a client-side detection alone. Removing duped items must not punish good-faith holders.
- In an incident, stop the bleeding first (kill switch), then diagnose.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the cause is an ordinary bug: use the `debug` skill.
- If the economy needs repair after a dupe: use the `monetization` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
