---
name: monetization
description: "Design, fix and implement monetization and the in-game economy of a Roblox game. Use when the user says \"my monetization is bad\", \"my game isn't making money\", \"nobody buys anything\", \"what should I sell\", \"set prices\", \"add game passes / dev products / a shop / a starter pack / boosts\", \"the economy is inflated\", \"balance my upgrade costs or rebirths\", or asks about Robux, DevEx or purchase policy."
argument-hint: "[your game and what it sells now]"
---

# Monetization and economy

Recommend what to sell and what to charge, then build it: products, shop, offer timing and safe purchase code. Heavy on things to buy, never annoying, always within Roblox's rules.

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
| Product set, price ladders by genre, offer timing, shop, elasticity tests, refunds, policy, DevEx | `${CLAUDE_PLUGIN_ROOT}/references/monetization-and-policy.md` |
| Currencies, cost curves, rebirth, luck and pity math, sinks, inflation, trading, simulation | `${CLAUDE_PLUGIN_ROOT}/references/economy-and-progression.md` |
| ProcessReceipt, passes, gifting: purchase code that never double-charges or loses a purchase | `${CLAUDE_PLUGIN_ROOT}/references/data-and-purchases.md` |
| Shop screen recipe and reward feedback | `${CLAUDE_PLUGIN_ROOT}/references/ui-screen-recipes.md` and `${CLAUDE_PLUGIN_ROOT}/references/ui-motion-and-feedback.md` |
| Plan to fill in | `${CLAUDE_PLUGIN_ROOT}/templates/monetization-product-plan.md` and `${CLAUDE_PLUGIN_ROOT}/templates/economy-balance-sheet.md` |
| What fits this genre and what to delete from the default set | `${CLAUDE_PLUGIN_ROOT}/references/genre-playbooks.md` then one file in `${CLAUDE_PLUGIN_ROOT}/references/genres/` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Fix retention before pricing: spend follows session length. If D1 is far below the genre's benchmark, say so and fix that first.
- Start from the default set (timed 2× boosts, starter pack, convenience passes, gift versions, Luck only where the game has luck) and delete what does not fit.
- Every ladder has a rung under 100 R$ and at least one repeatable product. Prices are read at runtime with `GetProductInfoAsync`, never hard-coded.
- Offer gate: no offers in the first 10 minutes or before the first win; at most 3 a session; two dismissals mean 24 hours of silence; at most 25% of the screen, with an X.
- Popups only after a win. An offer that answers friction sits inline where the friction is.
- Paid random items need full numeric odds summing to 100% and the `PolicyService` gate. Never grant from a client signal; save the grant before returning `PurchaseGranted`; deduplicate by `PurchaseId`.
- Never reduce or revalue something bought with Robux. Personal paid boosts count play time; server-wide boosts run in real time and show their end.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If purchases are not granting or items duplicate: use the `security-data` skill.
- If players leave before they could ever buy: use the `retention` skill.
- If the shop looks cheap or breaks on phones: use the `ui` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
