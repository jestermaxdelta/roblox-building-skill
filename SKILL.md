---
name: roblox-game-design
description: "The full playbook for making a Roblox game better at any stage: a new idea, a prototype or a live game. Use for planning or building a whole Roblox game, choosing a genre or what to build, design documents, art direction, economy and progression plans, launch, team and business questions, a beginner's first game, and any Roblox, Luau or Roblox Studio task that no more specific Roblox skill covers. Also the fallback for vague requests such as \"help with my Roblox game\". Enforces the house rules: every model from Blender, everything solid, heavy but never invasive monetization."
argument-hint: "[your idea, your game, or what you need]"
---

# Roblox game design and development

This file holds the modes, the house rules and the rules that apply to every task. Everything else is in routed files: open `references/INDEX.md` to find the one for a job. Paths are relative to this skill's folder.

Design before build. Before gameplay code is written, the fantasy, three pillars, the loops, the first-minute script, an economy model with numbers and an art direction exist and have been checked against their rubrics.

## Pick the mode first

| Mode | Use when | Start at | Done when |
|---|---|---|---|
| **A. New game** | An idea, or nothing yet | `references/workflow-phases.md`, phase 1. A beginner's first game starts at `references/learning-paths.md` instead: the goal is to finish something small, so the market gate does not apply and their idea is never "too saturated" | Each phase's gate passes, one at a time |
| **B. Level-up** | A game exists and should get better: "review my game", "why is it not growing / retaining / earning", "optimise it" | `references/audit-existing-game.md` | Scores have evidence, actions are ranked, and the top actions are shipped or handed over with exact steps (`templates/game-audit-report.md`) |
| **C. Single fix** | One system, bug, tweak or question | The trigger table below, or `references/INDEX.md` | The fix passes the review gate of the file used |

Level-up in one paragraph: collect what exists (numbers, place or repo, Studio MCP access, the owner's goal); inspect read-only before judging; score the ten dimensions with evidence; fix in funnel order unless something is on fire (data loss, exploits and crashes, then the first minute, the core loop, retention, monetisation, growth); make live changes safely (baseline number, Config flag, never break saves, one variable at a time); re-measure. A game that breaks the house rules gets each violation listed as a finding with a plan ranked by visibility, on its own track, never a refusal or a forced rebuild.

## Trigger phrases

When a message sounds like the left column, go straight to that focus. As the `roblox-dev` plugin, each row is also a small focused skill that loads only its own instructions: use it when available, and this table when not.

| The user says something like | Focus (plugin skill) | Open first |
|---|---|---|
| "make my game better", "review my game", "why is it not growing" | Level-up audit (`level-up`) | `references/audit-existing-game.md` |
| "players leave after a minute", "nobody comes back", "it's boring", "the tutorial is bad" | Core loop and retention (`retention`) | `references/core-loop-tuning.md`, `references/tutorial-and-onboarding.md`, `references/liveops-quests-retention.md` |
| "my monetization is bad", "it isn't making money", "what should I sell", "set prices" | Monetization and economy (`monetization`) | `references/monetization-and-policy.md`, `references/economy-and-progression.md` |
| "my UI looks bad / generic", "the menu is broken on phone", "make a shop / HUD screen" | UI and UX (`ui`) | `references/ui-design-figma.md`, `references/ui-screen-recipes.md`, `references/ui-input-crossplatform.md` |
| "the VFX is bad", "combat feels flat", "no impact", "the sounds are annoying" | VFX, feel and audio (`vfx-and-audio`) | `references/vfx-and-juice.md`, `references/vfx-recipes.md`, `references/audio-sfx-music.md` |
| "make a cutscene", "intro cinematic", "the camera is robotic", "make a trailer" | Cutscenes and cameras (`cinematics`) | `references/cutscenes-and-cinematics.md` |
| "my game looks generic / like AI slop", "my map feels empty", "the lighting looks flat" | Art direction, maps and lighting (`world-and-lighting`) | `references/art-direction-and-quality-bar.md`, `references/level-design-worldbuilding.md`, `references/lighting-and-atmosphere.md` |
| "my models look bad", "export this to Roblox", "the animation is stiff / broken" | Blender models and animation (`models-and-animation`) | `references/blender-modeling-craft.md`, `references/art-pipeline-blender.md`, `references/animation-and-rigs.md` |
| "make an inventory / pet system / round system / combat / trading" | Gameplay systems and Luau (`systems`) | `references/gameplay-systems-cookbook.md`, `references/luau-mastery.md` |
| "it's broken", "I get this error", "works in Studio but not live" | Debugging (`debug`) | `references/debugging-and-testing.md` |
| "my game is laggy", "it crashes on phones", "low FPS" | Performance (`performance`) | `references/performance.md` |
| "exploiters", "players duped items", "players lost their data", "paid and got nothing" | Security and data (`security-data`) | `references/networking-and-security.md`, `references/data-and-purchases.md` |
| "nobody plays my game", "make a thumbnail / icon", "should I run ads", "I'm launching" | Discovery and growth (`growth`) | `references/icons-thumbnails-and-store-page.md`, `references/analytics-and-discovery.md`, `references/growth-and-marketing.md` |

## How to work

1. **Look first.** Read what exists (scripts, instances, numbers) before judging. Without access, give a short first pass and ask for at most three things that would change the answer.
2. **Diagnose** against the "Level-up: symptom → cause → fix" table in the topic's reference. Name the cause in one sentence, with the evidence.
3. **Recommend** a short ranked list, the option you would pick and one bolder alternative.
4. **Implement** the top items in the same turn. Pause only before something hard to undo or outward-facing: publishing, changing save data, creating or repricing products, spending money, deleting the user's work, or a choice that is the owner's taste.
5. **Verify** against the reference's review gate, then say what changed, what was not verified and which number will show whether it worked.

**Anything visual starts from references, not from memory.** Before designing UI, effects, a map, models, lighting, a cutscene, an icon or a thumbnail: open the matching file in `references/visual-library/` (listed in `references/INDEX.md`), pick three to five references that fit this game's genre and tone, look at them (the bundled sheets in `assets/reference/` open with the Read tool), and note what to take from each. Then check the result against `references/art-direction-and-quality-bar.md`. Work built from defaults is what makes a game look generic.

## Adapt to the developer's level

Judge the level from evidence in the conversation and the project, separately for code, art, design and platform knowledge. Never ask "what level are you" and never label the person.

- **Beginner:** one concept at a time, Studio-native workflow, the three actions that matter most with the reason for each, a scope they can finish. Define terms (`references/glossary.md`).
- **Intermediate:** what turns a working game into a good one. Show the trade-off, recommend one option.
- **Expert:** terse, measured, trade-off-first: numbers, edge cases, experiments, runbooks.

Simplify the explanation, never the safety: a beginner still gets safe saving, server-side checks and compliant purchases, as a ready module with a short explanation. Detail: `references/learning-paths.md`.

## House rules (verbatim, override all generic advice)

- **Blender for every model.** Make every 3D asset in Blender: street lamps, roads, signs, cars, workers, buildings, props, literally everything. No primitive-Part builds and no generic marketplace models. The bar is a very high-quality, cohesive, put-together look that avoids the generic "AI slop" style. Drive Blender through the Blender Lab MCP add-on bridge (see the game's `tools/blender_exec.py`), export GLB in a separate headless `blender -b` process, and upload through Open Cloud.
- **Only Blender models in the game, and everything is solid (strict).** Every visible object in the whole game is a Blender model. No visible primitive Parts and no leftover placeholders ship. Players and NPCs must not be able to walk through solid objects, so every model gets proper collision (a simple collision mesh or a suitable `CollisionFidelity`). Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
- **Push microtransactions heavily, but never invasively.** Non-invasive is the most important rule of all. Starter-pack and offer popups are small, dismissible, never block play, are well-timed (after a win, not in the first minutes), and are rate-limited. Default product set: timed boosts such as 2× EXP, 2× speed (e.g. 2× delivery speed for 10 min), 2× Cash, Luck and Server Luck (only if the game has luck mechanics), a starter pack, Gift versions of passes, and convenience game passes. Stay within Roblox's monetisation rules: no fake discounts, restarting countdowns or false scarcity.

What follows from them:

- No primitive greybox ships: prototype with a Blender blockout kit or in a throwaway place. Nothing from Studio's generative or marketplace tools ships. Terrain needs the owner's approval per game. No AI-generated art ships as final art (UI, icons and thumbnails included); AI tools are for throwaway ideation.
- "Solid" is about the world players move through. Held tools and viewmodels, short-lived effect meshes, pets that follow a player, foliage canopies and hanging cables do not collide; a pet standing in the world as an object does. Skinned meshes need a `_COL` proxy. Particles, Beams, Trails and UI are not models; a mesh used as an effect is still authored in Blender.
- Luck and Server Luck are paid random items: full numeric odds summing to 100%, boosted odds shown live, gated by `PolicyService`.
- "Push heavily" applies to games built to earn. A first learning game needs no monetisation, and a minor is never told to spend real money to test a purchase.
- Without the owner's bridge (`tools/blender_exec.py`), drive Blender through a Blender MCP server or the shipped `scripts/blender/export_kit.py`, and upload through the Studio MCP's `open_cloud_invoke` or the 3D Importer.

## Rules for every task

The complete set, by topic, is in `references/decision-rules.md`: open the block for the topic you are working on. These apply always:

- Mobile first: design UI, controls and budgets for a small 3 GB Android phone, then widen.
- The client is hostile: never trust it for ids, prices, damage, positions, currency or inventory. Remotes carry intent only; the server validates, rate limits and decides.
- Player data: ProfileStore with session locking; a profile that failed to load never saves; never change a live store's key pattern; no yield between a check and its write.
- Purchases: never grant from a client signal; save the grant before returning `PurchaseGranted`; deduplicate by `PurchaseId`; read prices at runtime.
- Offers: no popup before 10 minutes of play and a first win, at least 8 minutes apart, at most 3 a session. Never power sold in competitive modes. Never reduce something bought with Robux.
- Paid random items need disclosed odds and the `PolicyService` gate. Players converse only through `TextChatService`. No links, invite codes, handles or requests for personal data inside the game.
- Retention through content, collection, social play and seasons, never through punishment.
- Social rewards are bonuses, never gates, asked after the first win. Group join and friend join are the default; like and favourite rewards are a risk to re-check before shipping; none for off-platform actions.
- A next goal with its progress and its reward is always on screen. Fix the earliest broken stage first; reward systems amplify a working loop and do not rescue a broken one.
- `--!strict`, modern APIs only (`task.*`; no `wait`, `spawn`, `delay`, BodyMovers). Effects render on clients. Crowds are server data with pooled client models.
- No live change without a baseline number, a Config flag and a rollback trigger. A `ConfigSnapshot` never updates itself: connect `UpdateAvailable` to `Refresh()` or the flag never reaches running servers.
- Never ban on one signal. Treat `require(<number>)`, `getfenv`, `loadstring` and obfuscated strings as findings until explained.
- Never install a third-party skill, plugin or MCP server unread; never paste keys or cookies.
- Legal, tax and IP topics: state the documented fact with its date and point to the current Roblox terms and a professional. Never present it as advice.

## Using the Roblox Studio MCP

A build and test tool, not a content generator.

- Use freely: `list_roblox_studios` first (pass its `studio_id` on every call), then `get_studio_state` before any edit; `script_read`, `script_grep`, `script_search`, `multi_edit`; `inspect_instance`, `search_game_tree`; `execute_luau` for edit-mode scans and batch fixes; `start_stop_play`, `character_navigation`, `user_keyboard_input`, `user_mouse_input`, `get_console_output`, `screen_capture` for playtests; `open_cloud_invoke` for uploads.
- Never for anything that ships: `generate_mesh`, `generate_procedural_model`, `generate_material`, `search_asset`, or any other generator the server offers. `insert_asset` only for the owner's own Blender-authored assets and packages by id.
- On a live game start read-only, edit in edit mode behind a saved version, and keep live Open Cloud scopes to a dev universe until the change is proven. Re-read instances after each `execute_luau` batch.
- Match the project: Rojo-synced files when there is a Rojo tree, `multi_edit` when there is not. Do not convert a workflow unasked.

## Reading the references

- Open only what the task needs. Each guide starts with a "Start here by level" table and ends with a review gate; files over 300 lines have a contents line, so read the section, not the file.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive (API names, limits, prices, policy), re-check at https://create.roblox.com/docs or the `Roblox/creator-docs` mirror before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. Luau in the references is unexecuted: adapt it and test it.
- `Conflict:` notes record real disagreements. Trust in this order: the house rules, current official docs, numbers measured on the user's own game, the market snapshot in `references/market-scan-2026-11.md` (2026-11-07; if the user's CLAUDE.md or memory names a local research vault, prefer its newer numbers), then community practice. `references/knowledge-base.md` is an unverified archive: where it differs from a guide, the guide is right.

## Done means

1. The relevant gate was checked item by item and the result reported: a phase gate or Gate A in `references/checklists.md`, or the review gate of the reference used.
2. `[VS]` facts relied on were re-checked, or the user was told exactly which were not.
3. New Luau is `--!strict` and has a test or a described manual test.
4. Nothing delivered breaks a house rule (scan: `references/checklists.md`, Gate 4); existing violations are listed as findings with a plan.
5. Visual work was built from looked-at references and passed its critique rubric.
6. The user got a recommendation and a bolder alternative wherever a real choice existed, pitched at their level.
