---
name: roblox-game-design
description: "The full playbook for making a Roblox game better at any stage: a new idea, a prototype or a live game. Use for planning or building a whole Roblox game, choosing a genre or what to build, design documents, economy and progression plans, launch, team and business questions, a beginner's first game, and any Roblox, Luau or Roblox Studio task that no more specific Roblox skill covers. Also the fallback for vague requests such as \"help with my Roblox game\". Covers design, genres, core loop, monetization, UI and Figma, Blender art, VFX and audio, Luau systems, security, performance, analytics and growth, and enforces the house rules: every model from Blender, everything solid, heavy but never invasive monetization."
---

# Roblox game design and development

This skill takes a Roblox game to the next level from wherever it is now: an idea, a prototype, or a finished live game. It bundles three entry modes, a phased workflow, decision rules, the owner's non-negotiable house rules, and routed reference files. The references are distilled from a 9,389-line knowledge base (compiled 2026-11-08 from 31 repositories and the owner's research vault) plus a 2026-11-10 research pass over the Roblox Creator Docs, GitHub, the LihFolk Vault V2 (CC BY 4.0, credited in `CREDITS.md`) and developer-forum material found through web search. Code snippets in the references are unexecuted: treat them as starting points to test, not as verified code.

Two meanings of "efficient" apply at once. Efficient games: frame budgets, low-end mobile first, streaming, bandwidth, memory. Efficient development: design before build, vertical slice first, build order, scope cuts, reusable modules, Rojo/Wally/Selene/StyLua/luau-lsp and tests.

"Well thought out" means design before build. Before writing gameplay code, the player fantasy, three pillars, core/session/long-term loops, FTUE script, economy model with numbers, retention and social hooks and a risk list exist and have been reviewed against the rubrics.

## Pick the mode first

Work out which situation the user is in before opening anything else. The modes share the same references but start in different places, and starting in the wrong one wastes the user's time (a GDD for a game that already ships, or a rebuild when three fixes would do).

| Mode | Use when | Start at | Output |
|---|---|---|---|
| **A. New game** | There is an idea or nothing yet | Phase 1 of the workflow below. A beginner's first game starts at `references/learning-paths.md` instead: the goal is to finish something small, so the Phase 1 market gate does not apply and their idea is never "too saturated" | The phase outputs, one gate at a time |
| **B. Level-up** | A game already exists (prototype, soft launch or live) and the goal is "make it better", "why is it not growing/retaining/earning", "review my game", "optimise it" | `references/audit-existing-game.md` | `templates/game-audit-report.md` filled: scores with evidence, a ranked action list, then the top actions executed |
| **C. Single fix** | One system, one bug, one balance tweak, one question | The trigger table below, or the matching row or rows of the routing table (a real problem often spans two or three files) | The fix, checked against the review gate of the file used |

Level-up mode in short (the audit reference has the full method):

1. **Intake.** Ask for what exists: genre, age and platform mix, analytics (retention, session time, funnel, payer conversion, crash rate), the place or Rojo repo, Studio MCP access, and the owner's goal. Missing numbers are fine; say what you assumed.
2. **Inspect before judging, read-only.** Read the code and DataModel, play the first ten minutes through the Studio MCP if it is connected, and open the genre file for the game in `references/genres/`. Change nothing yet.
3. **Score the ten dimensions** (first session, core loop, progression and economy, retention and LiveOps, monetisation, UI/UX, art and house rules, performance, security and data, discovery and growth) with evidence for each score.
4. **Rank by impact × confidence ÷ effort.** Fix in funnel order unless something is on fire: data loss, exploits and crashes first, then first-session bounce, then the core loop, then retention, then monetisation, then growth. Sending more players into a leaky first session wastes them.
5. **Execute the top actions with the safe-change protocol**: back up the place version, put changes behind Configs flags, never break saves, change one variable at a time, and say how the result will be measured.
6. **Re-measure and repeat.** A level-up pass is done when the top actions are shipped or handed over with clear steps, not when the report is written.

House rules in Level-up mode: an existing game often breaks them (primitive Parts, marketplace models, walk-through props, pushy popups). Treat each violation as a finding with a migration plan ranked by how visible it is, rather than blocking every other fix until the whole map is rebuilt.

## Trigger phrases

People describe symptoms, not topics. When a message sounds like the left column, go straight to that focus: open the listed files, diagnose against their "Level-up: symptom → cause → fix" tables, recommend a ranked fix, then implement the top fixes in the same turn (pause only before something hard to undo: publishing, changing save data, creating or repricing products, spending money, deleting the user's work).

When this skill is installed as the `roblox-dev` plugin, each row is also its own small focused skill that loads only its own instructions; use that skill when it is available and this table when it is not.

| The user says something like | Focus (plugin skill) | Open first |
|---|---|---|
| "make my game better", "review my game", "why is it not growing", "what should I fix first" | Level-up audit (`level-up`) | `references/audit-existing-game.md` |
| "players leave after a minute", "nobody comes back", "it's boring", "the tutorial is bad", "low D1" | Core loop and retention (`retention`) | `references/core-loop-tuning.md`, `references/liveops-quests-retention.md` |
| "my monetization is bad", "it isn't making money", "what should I sell", "set prices", "the economy is inflated" | Monetization and economy (`monetization`) | `references/monetization-and-policy.md`, `references/economy-and-progression.md` |
| "my UI looks bad", "the menu is broken on phone", "make a shop / HUD / inventory screen", "turn this Figma into Roblox UI" | UI and UX (`ui`) | `references/ui-design-figma.md`, `references/ui-input-crossplatform.md` |
| "the VFX is bad", "combat feels flat", "no impact", "add juice", "the sounds are annoying" | VFX, feel and audio (`vfx-and-audio`) | `references/vfx-and-juice.md`, `references/audio-sfx-music.md` |
| "my map feels empty", "players get lost", "the lighting looks flat" | Maps and lighting (`world-and-lighting`) | `references/level-design-worldbuilding.md`, `references/lighting-and-atmosphere.md` |
| "my models look bad", "the style doesn't match", "export this to Roblox", "the animation is broken" | Blender models and animation (`models-and-animation`) | `references/blender-modeling-craft.md`, `references/art-pipeline-blender.md`, `references/animation-and-rigs.md` |
| "make an inventory / pet system / round system / combat / trading", "how should I structure this" | Gameplay systems and Luau (`systems`) | `references/gameplay-systems-cookbook.md`, `references/luau-mastery.md` |
| "it's broken", "I get this error", "works in Studio but not live", "infinite yield" | Debugging (`debug`) | `references/debugging-and-testing.md` |
| "my game is laggy", "it crashes on phones", "low FPS", "long loading" | Performance (`performance`) | `references/performance.md` |
| "exploiters", "can this be exploited", "players duped items", "players lost their data", "paid and got nothing" | Security and data (`security-data`) | `references/networking-and-security.md`, `references/data-and-purchases.md` |
| "nobody plays my game", "make a thumbnail", "should I run ads", "I'm about to launch" | Discovery and growth (`growth`) | `references/analytics-and-discovery.md`, `references/growth-and-marketing.md` |

## How to use the references

- Open only the reference files the routing table points at for the current task. Each opens with a "Start here by level" table and ends with a review gate. Files over 300 lines carry a contents line: read the section you need, not the whole file.
- `references/knowledge-base.md` is the full 645,989-byte source. Never read it whole. Grep it by section heading, then read that range only:
  `grep -n "^## 4.7" references/knowledge-base.md` (section start), then `grep -n "^## 4.8"` for the end, then Read with offset/limit. Section map: 1.x design, 2.x game craft and architecture patterns, 3.x platform/economy/monetization/analytics/discovery, 4.x engineering/security/data/purchases, 5.x performance/art/UI/input/launch. `## 3.12` and `## 5.14` list known conflicts.
- Facts marked `[VS]` are version-sensitive (API names, limits, prices, policy, dashboard features). Re-check them at https://create.roblox.com/docs before relying on them. Market numbers date from a 2026-11-07 snapshot.
- For market data (trending genres, what to build, discovery, thumbnails), open `references/market-scan-2026-11.md` first: it distils the maintainer's November 2026 research vault and the v2 report (a converted copy sits in `references/market-research-v2-raw.md` for grep). Those numbers are a 2026-11-07 snapshot and go stale. If the user's CLAUDE.md or memory names a local Roblox research vault, read its index note first and prefer its newer numbers; otherwise the distilled copies are the authority.
- Claims tagged `[community]` come from developer forums, Reddit and videos: treat them as heuristics to test, not guarantees. `[official]` marks Roblox documentation, `[house]` marks house estimates.

## Adapt to the developer's level

The same question deserves a different answer for someone on their first script and someone running a live game with a team. Work out the level from evidence in the conversation and the project (vocabulary, tooling, what already exists), separately for code, art, design and platform knowledge, because people are often expert in one and new in another. Do not ask "what level are you" and do not label the person.

- **Beginner:** one concept at a time, Studio-native workflow before Rojo, the three actions that matter most with the reason for each, a small scope they can finish. Define a term the first time it appears (`references/glossary.md`).
- **Intermediate:** the practices that turn a working game into a good one: architecture, data safety, security, mobile, analytics, polish. Show the trade-off, recommend one option.
- **Expert:** terse, measured, trade-off-first. Skip the basics; bring numbers, edge cases, experiments and runbooks.

Simplify the explanation, never the safety: a beginner still gets session-locked saves, server-side validation and policy-compliant purchases, delivered as a ready module with a short explanation instead of a lecture. `references/learning-paths.md` has the detection signals, the path for each level and realistic scope by time budget.

## House rules (verbatim, override all generic advice)

- **Blender for every model.** Make every 3D asset in Blender: street lamps, roads, signs, cars, workers, buildings, props, literally everything. No primitive-Part builds and no generic marketplace models. The bar is a very high-quality, cohesive, put-together look that avoids the generic "AI slop" style. Drive Blender through the Blender Lab MCP add-on bridge (see the game's `tools/blender_exec.py`), export GLB in a separate headless `blender -b` process, and upload through Open Cloud.
- **Only Blender models in the game, and everything is solid (strict).** Every visible object in the whole game is a Blender model. No visible primitive Parts and no leftover placeholders ship. Players and NPCs must not be able to walk through solid objects, so every model gets proper collision (a simple collision mesh or a suitable `CollisionFidelity`). Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
- **Push microtransactions heavily, but never invasively.** Non-invasive is the most important rule of all. Starter-pack and offer popups are small, dismissible, never block play, are well-timed (after a win, not in the first minutes), and are rate-limited. Default product set: timed boosts such as 2× EXP, 2× speed (e.g. 2× delivery speed for 10 min), 2× Cash, Luck and Server Luck (only if the game has luck mechanics), a starter pack, Gift versions of passes, and convenience game passes. Stay within Roblox's monetisation rules: no fake discounts, restarting countdowns or false scarcity.

Resolutions that follow from the house rules:

- Luck and Server Luck are paid random items: show full numeric odds (summing to 100%, boosted odds live) and gate behind `PolicyService:GetPolicyInfoForPlayerAsync().ArePaidRandomItemsRestricted`.
- No primitive greybox ships. Prototype with a Blender blockout kit (a few bevelled kit pieces exported once) or inside a throwaway place that is never published.
- Do not ship content from Studio's generative or marketplace tools (Assistant mesh generation, procedural models, Toolbox or insert-asset). Blockouts from them may be used only in throwaway places.
- Terrain needs the owner's explicit per-game approval; the default is Blender ground meshes.
- Skinned meshes, SurfaceAppearance and other visual tools are fine when the asset is authored in Blender.
- "Everything is solid" is about the world players and NPCs move through. Tools, weapons and viewmodels held by a character, and transient effect meshes (slashes, projectiles' visuals, impact rings), do not collide: the character's own collider and the server's hitbox cover them. Skinned meshes collide in their rest shape only, so give animated bodies a `_COL` proxy.
- Particles, Beams, Trails and UI are not models: they are allowed. A mesh used as an effect is still authored in Blender.
- Pets and followers that trail a player are client-rendered and do not collide; a pet standing in the world as an object (in a pen, on a pedestal) is solid like anything else.
- "Push microtransactions heavily" applies to games built to earn. A first learning game does not need monetisation, and a minor is never told to spend real money to test a purchase.

## Phased workflow: idea to live

Work the phases in order. Each phase names its outputs, the reference to open and the gate that must pass before the next phase. Do not start a later phase on a system whose earlier gate failed.

| Phase | Outputs | Open | Gate |
|---|---|---|---|
| 1. Concept and genre | Pitch, fantasy, the one new verb, comparables, genre loop, age tier, platform priority | `references/market-scan-2026-11.md`, `references/genre-playbooks.md` then the one matching file in `references/genres/`, `references/case-studies-teardowns.md`, `references/design-foundations.md` §fun | Pitch fits one sentence; genre loop named; the new action or visible journey named; mobile-first confirmed |
| 2. One-pager and pillars | `templates/game-one-pager.md` filled | `references/process-and-playtesting.md`, `references/design-foundations.md` | Core-loop rubric ≥ 7/10; three pillars are decision rules |
| 3. Loops, FTUE and economy model | Loop timings, 5-minute FTUE script, `templates/economy-balance-sheet.md` filled with numbers | `references/core-loop-tuning.md`, `references/economy-and-progression.md`, `references/liveops-quests-retention.md` §onboarding | First reward < 30 s; sink ratio 0.95–1.05 modelled; rebirth wait ratio ×1.2–1.5 |
| 4. Lean GDD and architecture plan | `templates/lean-gdd.md`; remotes list; data schema; products table; streaming and collision policy | `references/engineering-architecture.md`, `references/architecture-patterns-luau.md`, `references/gameplay-systems-cookbook.md`, `references/networking-and-security.md` §surface design | Gate 0 in `references/checklists.md` passes |
| 5. Build order and vertical slice | Rojo project, loader, DataService, RemoteGuard, ReceiptService stubs; one playable loop with blockout kit | `references/engineering-architecture.md`, `references/studio-workflow.md`, `references/data-and-purchases.md`, `references/networking-and-security.md`, `references/debugging-and-testing.md` | Gate 1: five strangers; kill/keep decided (`templates/playtest-plan.md`) |
| 6. Game craft pass | Feel, camera, level layout, VFX, audio, AI, UI design, settings and accessibility | `references/game-craft.md`, `references/level-design-worldbuilding.md`, `references/vfx-and-juice.md`, `references/audio-sfx-music.md`, `references/ui-design-figma.md`, `references/ui-input-crossplatform.md`, `references/accessibility-and-player-qol.md` | Response times and juice tiers met; phone layout tested; greyscale and muted-play passes done |
| 7. Art pipeline | Style bible, kit list, Blender assets → GLB → Open Cloud, post-import fixup, rigs and animation, lighting preset | `references/blender-modeling-craft.md`, `references/art-pipeline-blender.md`, `references/animation-and-rigs.md`, `references/lighting-and-atmosphere.md` | Review gates in those files; house-rule scan OK |
| 8. Monetization | `templates/monetization-product-plan.md`; products created; offer gate; receipts tested | `references/monetization-and-policy.md`, `references/data-and-purchases.md` §purchases | Gate 3 compliance passes |
| 9. Analytics and LiveOps plan | `templates/analytics-event-plan.md`; Configs; Experiments; 4-week update plan; first event | `references/analytics-and-discovery.md`, `references/liveops-quests-retention.md` | Events verified in a test place |
| 10. Performance pass | MicroProfiler captures, budgets table filled, streaming settings, collision audit | `references/performance.md` | Gate 4 on a 2–4 GB Android phone |
| 11. Launch | `templates/launch-checklist.md` signed; thumbnails, metadata, age tier, timing | `references/analytics-and-discovery.md` §discovery, `references/growth-and-marketing.md`, `references/community-moderation-safety.md`, `references/checklists.md` Gate 5 | All gates signed |
| 12. LiveOps | Weekly update day, events, season pass, funnel fixes, safety review | `references/liveops-quests-retention.md`, `references/analytics-and-discovery.md`, `references/growth-and-marketing.md`, `references/audit-existing-game.md` for a periodic level-up pass | Weekly KPI review done |

For a small request (one system, one bug, one balance tweak) skip to the matching row, but still check the gate for that row before declaring done.

## Decision rules

Design

- Mobile first: design the UI, controls and performance budget for a 3 GB Android phone, then widen to PC, console and VR.
- One new verb per game; copy the genre loop, change the verb and the fantasy. A visible journey beats a number on a menu: management and manager games stay hands-on in a small 3D space (menu, map and spreadsheet sims sit under 1K CCU); any map layer must play like a toy.
- Loops are nested: micro 10–30 s, meso 5–15 min, session 15–25 min, meta days to weeks. Every loop needs a visible goal and a next purchase.
- FTUE: first reward under 30 s, first upgrade under 2 min, one verb at a time, hint at about 11 s of no progress, no offers in the first 10 minutes.
- Economy: time-first curves (`req(L) = minutes(L) × xpPerMin(L)`), geometric costs (`floor(base × g^n)`, g 1.07–1.15), first ten purchases 3–10 s each, sink ratio 0.95–1.05, offline income capped and stated.
- Retention through content cadence, collections, social play and seasons; never through punishment, streak loss anxiety or dark patterns.
- Kill or keep after five strangers play the prototype; keep only with evidence.
- Classify a game by its host loop, then open one genre file. In a hybrid, one genre hosts and the other is a layer; the stricter rule wins.
- A next goal with its progress and its reward is always on screen. "What do I do now?" is the most common reason a first session ends.
- Fix the earliest broken stage first: crashes and load time, then the first minute, the funnel, session length, D1, D7, D30. Reward systems (dailies, quests, passes) amplify a loop that already works; they do not rescue one scoring under 5/10.

Engineering

- Plain modules plus a two-phase Init/Start loader is the default framework; jecs or Matter ECS only for simulation-heavy games; no Knit for new projects.
- One server entry, one client entry; no Scripts inside models; behaviour by CollectionService tags; `emitLegacyScripts: false`.
- `--!strict` everywhere; untrusted input is `unknown`; remotes carry intent, never outcome; every remote behind RemoteGuard rate limiting and validation.
- ProfileStore with session locking, schema version and migrations before `Reconcile`; a failed load never saves; purchases idempotent by `PurchaseId` saved before `PurchaseGranted`.
- Toolchain: Rokit pins Rojo, Wally, Selene, StyLua, luau-lsp, Lune; CI publishes via Open Cloud; only CI publishes production.
- Prefer Luau over Parallel Luau until profiling proves a parallel win; prefer spatial queries over `Touched` for gameplay, and never put damage or rewards on `Touched`.
- No yield between a check and its write (that gap is where dupes live); cache web facts such as group rank and pass ownership at join.
- Effects are built on clients: the server sends one validated event, each client renders, the caster predicts. Server hit timing comes from exported marker times; a client animation marker is a claim, not a fact.
- Crowds (enemies, pets, workers, droppers) are server data with pooled client-rendered models, never one Humanoid or physical part each.
- Every unanchored object has one mover and one written network owner.

UI

- Design at the small-phone frame first and scale up; never shrink a desktop layout. Structure and text are native instances, artwork is exported images (9-slice), no baked text, nothing over 1024 px.
- No colour, font, size or timing outside the theme module. Never hard-code the top-bar height or the jump-button position: read the insets.
- Pass lines: text at least 12 px drawn, taps at least 44 px, 8 px gaps, and no signal carried by colour alone.

Art and performance

- 1 Blender unit = 1 stud; kit grid 5/8/16 studs; pivots at the snap point; texel density about 50 px/stud; shared `_SA` trim-sheet library.
- Budgets (house estimates, not official): < 1,000 draw calls, < 1 M triangles in the worst view, ≥ 30 FPS on low-end Android, ≥ 60 Hz server heartbeat, server memory < 50% of the limit.
- Streaming on; interactive models Atomic; code never indexes Workspace without tags or a timeout.
- Collision: static geometry anchored; `Box` for non-colliding visuals, `Hull`/`Default` or a `_COL` proxy mesh for walkable geometry; `PreciseConvexDecomposition` only for approved doorways.

Monetization

- Default product set first; delete what does not fit; never sell stat power in competitive modes; free alternative next to every paid shortcut.
- Offer gate defaults: 600 s grace and a first win; 480 s gap; ≤ 3 per session; ≤ 1 starter pack per day; two dismissals → 24 h silence; ≤ 25% of the screen with an X.
- Prices come from `MarketplaceService:GetProductInfoAsync` at runtime; the plan's price column is only the Creator Hub setup value.
- Every price ladder has a rung under 100 R$ and at least one repeatable product: the median payer spends under a dollar, and repeat spend days are a discovery signal.
- Popups only after a win. An offer that answers friction (out of space, out of energy) sits inline where the friction is, never as a popup.
- Personal paid boosts count play time and pause offline; server-wide boosts run in real time and show their end. State which on the product.
- Never reduce or revalue something a player bought with Robux. Rebalance by adding, not by taking away.
- Fix retention before pricing: spend follows session length.

Live games

- Inspect before changing: dashboards, then one low-end phone, then read-only scans, then fixes.
- No live change without a baseline number, a Config flag and a rollback trigger. Snapshot DataStores before any change to save logic.
- One Config key per experiment. Under about 1,000 DAU there is not enough traffic for a clean A/B: compare weekly cohorts instead.
- No paid traffic while D1 sits below the genre's benchmark median or likes sit under 85%. Ads send players into the funnel you have; they do not fix it.

When a design choice matters, give the user a clear lower-risk option and a bold higher-risk option, state the trade-offs and name the one you recommend.

## Never do

Security

- Never trust the client for ids, prices, damage, positions, currency or inventory; never grant from `PromptProductPurchaseFinished` or any client signal.
- Never use `RemoteFunction:InvokeClient`; never store secrets, API keys or server logic in ReplicatedStorage, StarterPlayer or any client-visible container.
- Never ban on a single heuristic or on a client-side detection alone; never kick for a transient DataStore error.
- Treat any `require(<number>)`, `getfenv`, `loadstring` or obfuscated string in a place as a finding until explained: that is what a backdoor looks like.
- Never run a trading system without item GUIDs, an audit log and a kill switch.

Purchases and data

- Never return `PurchaseGranted` before the grant is saved; never register two `ProcessReceipt` callbacks; never skip `PurchaseId` deduplication.
- Never save a profile that failed to load; never change the key pattern of a live store; never wipe data in a migration without a backup path; never read DataStores in a gameplay hot path.

Policy and monetization

- Never fake discounts, restart countdowns or claim false scarcity; never show offers during onboarding, loading or combat; never stack popups or block play with them.
- Never sell paid random items without full odds disclosure and `PolicyService` gating; never ship unfiltered user text.
- Social rewards (group join, like, favourite, friend join) are wanted in every game, as a bonus only: never gate progress or core content on them, never put "free Robux", giveaways or "like for rewards" in the title, thumbnail or description (that is the exposure penalty), and ask after the first win, not in the first minutes. Group-join and friend-join bonuses are the safe default; before rewarding likes or favourites, re-check the current Roblox Community Standards `[VS]` and leave them out if in doubt. Rules in `references/liveops-quests-retention.md` §social rewards.
- Never run rewarded video with random rewards or as a progress gate.
- Never let players converse outside `TextChatService`; never put links, invite codes, handles or requests for personal data in the game. Social links live on the game's page.
- Never ship a timer, discount or stock count that is not literally true.
- Never present legal, tax or IP guidance as advice: state the documented fact with its date and point to the current Roblox terms and a professional.

Content and tooling

- Never ship a visible primitive Part, placeholder, marketplace model or generated mesh; never leave a walkable mesh without collision; never enable Terrain without the owner's approval for that game.
- Never use deprecated APIs in new code: `wait`, `spawn`, `delay`, `tick`, `Humanoid:LoadAnimation`, BodyMovers, `FindPartOnRay`, `GetProductInfo` without `Async`.
- Never publish production from a local Studio when CI exists; never commit without `wally.lock` and lint passing. Exception: the Open Cloud place publish does not carry some art data (SurfaceAppearance, unions), so art-changing releases publish from Studio and are verified live (`references/studio-workflow.md`).
- Never ship temporary animation ids (`RegisterKeyframeSequence`, `RegisterAnimationClip`): they work in Studio and are dead live. Publish clips under the game's owner.
- Never run Script Sync and Rojo on the same scripts; never point `rojo serve` at a live place another session owns.
- Never install a third-party skill, plugin or MCP server unread; pin a commit, never pipe to a shell, never paste keys or cookies (`references/ai-toolchain-skills.md`).
- Never carry gameplay information by shadows, bloom, post effects or sound alone: low-end devices drop them.

## Using the Roblox Studio MCP

Use the Studio MCP as a build and test tool, not as a content generator.

- Allowed and encouraged: `execute_luau` for edit-mode scans, fixups, batch property edits and the house-rule scan; `script_read`, `script_grep`, `script_search` and `multi_edit` for Luau; `inspect_instance` and `search_game_tree` to audit the DataModel; `start_stop_play`, `get_console_output`, `screen_capture` and `user_*_input` for playtests; `open_cloud_invoke` for asset uploads and publishing; `get_studio_state` before any edit.
- Never use `generate_mesh`, `generate_procedural_model`, `generate_scene`, `generate_texture`, `generate_material` or `search_asset` for anything that ships. Blockouts from them stay in throwaway places only. `insert_asset` is allowed for one thing: inserting the owner's own Blender-authored assets and packages by id.
- On a live game start read-only (`inspect_instance`, `search_game_tree`, `script_grep`, `screen_capture`), make edits in edit mode behind a saved version, and keep live Open Cloud scopes to a dev universe until the change is proven.
- Run scans and fixups in edit mode, never in live servers. Re-read instances after each `execute_luau` batch rather than assuming state.
- Prefer Rojo-synced source files for scripts; use `multi_edit` only when the project has no Rojo tree.

## Routing table

Find the row that matches the task and open that file. Paths are relative to this skill's folder.

**Start here**

| Task | Open |
|---|---|
| An existing game needs to get better (audit, review, "why is it not growing/retaining/earning") | `references/audit-existing-game.md`, report in `templates/game-audit-report.md` |
| Who am I helping and how deep should I go; a beginner's first game; realistic scope | `references/learning-paths.md` |
| A term or acronym (CCU, RFY, FTUE, DevEx, PTR, rebirth) | `references/glossary.md` |
| Every gate and checklist in one place, including the house-rule scan script | `references/checklists.md` |

**Design**

| Task | Open |
|---|---|
| What to build, what is winning or saturated, the 14 shared patterns, thumbnail rules, the 250-play gate, launch timing | `references/market-scan-2026-11.md` (raw report: `references/market-research-v2-raw.md`) |
| Choosing or shaping a genre | `references/genre-playbooks.md` (index), then the one matching file in `references/genres/`: `tycoon-and-cozy-management`, `simulator-incremental`, `pet-collection-hatching`, `plus-one-evolution`, `rng-rolling`, `steal-and-defend`, `obby-tower`, `horror-coop-escape`, `rpg-dungeon`, `fighting-battlegrounds`, `tower-defense`, `shooter-pvp`, `survival-crafting`, `social-roleplay`, `fashion-dress-up`, `social-deduction`, `party-minigames`, `physics-sandbox`, `racing-driving`, `fishing`, `sports` (`.md`) |
| How successful games actually work; doing a teardown of a competitor or your own game; trend or evergreen | `references/case-studies-teardowns.md` |
| Fun, motivation, flow, difficulty, progression and retention theory, rubrics | `references/design-foundations.md` |
| Designing, scoring, diagnosing and tuning the core loop; the first ten minutes; building the tutorial; reading the funnel | `references/core-loop-tuning.md` |
| Currencies, XP curves, costs, rebirth, offline income, luck and pity math, trading markets, economy simulation | `references/economy-and-progression.md` |
| Onboarding, quests, daily rewards, events, season pass, LiveOps calendar, notifications | `references/liveops-quests-retention.md` |
| Process, one-pager, GDD, milestones, scope triage, playtesting, postmortems | `references/process-and-playtesting.md` |

**Feel, world and art**

| Task | Open |
|---|---|
| Game feel, camera, input responsiveness, AI, procgen, save design | `references/game-craft.md` |
| Particles, beams, ability effects, hit-stop, camera shake, the juice ladder | `references/vfx-and-juice.md` |
| Sound effects, music, mixing, the audio API, audio licensing | `references/audio-sfx-music.md` |
| Maps, lobbies, wayfinding, layout by genre, kits, procedural levels, "the map feels empty" | `references/level-design-worldbuilding.md` |
| Lighting, atmosphere, post-processing, presets by genre | `references/lighting-and-atmosphere.md` |
| Modelling well in Blender: silhouette, bevels, colour, budgets, recipes, a first kit | `references/blender-modeling-craft.md` |
| Blender → GLB → Open Cloud, naming, collision authoring, textures, packages, import traps | `references/art-pipeline-blender.md` |
| Rigs, animation, markers, NPC animation at scale, animation bugs | `references/animation-and-rigs.md` |
| UI design system, Figma workflow, motion spec, screen recipes (HUD, shop, inventory, settings and more) | `references/ui-design-figma.md` |
| UI implementation, safe areas, input mapping, mobile, console, VR, UI architecture and performance | `references/ui-input-crossplatform.md` |
| Accessibility, settings menu, quality-of-life features | `references/accessibility-and-player-qol.md` |

**Code and systems**

| Task | Open |
|---|---|
| Learning or sharpening Luau, from first script to types, parallelism and performance idioms; game math | `references/luau-mastery.md` |
| Building a gameplay system: wallet, inventory, shop, pets and eggs, quests, rounds, combat, NPCs, plots and placement, trading, leaderboards and more | `references/gameplay-systems-cookbook.md` |
| Physics, network ownership, constraints, ragdolls, projectiles, vehicles | `references/physics-and-vehicles.md` |
| Containers, loader, Rojo layout, Luau standards, toolchain, CI/CD, live-update runbook | `references/engineering-architecture.md` |
| Game Programming Patterns in Luau (state, command, observer, component, object pool, ECS choice) | `references/architecture-patterns-luau.md` |
| Studio setup, test modes, Team Create, publishing, Script Sync or Rojo, working safely through the Studio MCP | `references/studio-workflow.md` |
| Remotes, RemoteGuard, threat modelling, exploit defence, bans, backdoor scans, secrets | `references/networking-and-security.md` |
| DataStore limits, ProfileStore, receipts, dupes, migrations, rollback, teleports, MemoryStore | `references/data-and-purchases.md` |
| Frame budgets, MicroProfiler, memory, streaming, collision cost, mobile crashes, loading | `references/performance.md` |
| "It's broken": symptom → cause → fix, live-only bugs, memory leaks, tests | `references/debugging-and-testing.md` |

**Money, growth and people**

| Task | Open |
|---|---|
| Products, passes, subscriptions, boosts, offers, price ladders, elasticity tests, refunds, policy, DevEx | `references/monetization-and-policy.md` |
| KPIs, benchmarks, analytics events, Configs, Experiments, Recommended For You, thumbnails, age tiers | `references/analytics-and-discovery.md` |
| Ads, TikTok and YouTube Shorts, creators, community building, launch and update marketing | `references/growth-and-marketing.md` |
| Child safety, maturity labels, chat rules, moderation, bans and appeals, crisis playbooks | `references/community-moderation-safety.md` |
| Teams, hiring, revenue splits, DevEx, IP and licensing, selling a game (facts with dates, not legal advice) | `references/team-business-legal.md` |
| Other agent skills, MCP servers and Luau libraries worth combining with this one, and how to vet them | `references/ai-toolchain-skills.md` |
| Full source text of the original knowledge base; grep by heading, never read whole | `references/knowledge-base.md` |

Templates (copy into the game repo's `docs/` folder and fill in):

| Template | Use at |
|---|---|
| `templates/game-audit-report.md` | Level-up mode |
| `templates/game-one-pager.md` | Phase 2 |
| `templates/lean-gdd.md` | Phase 4 |
| `templates/economy-balance-sheet.md` | Phase 3, and economy tuning on a live game |
| `templates/monetization-product-plan.md` | Phase 8 |
| `templates/analytics-event-plan.md` | Phase 9 |
| `templates/playtest-plan.md` | Phases 5–12, weekly |
| `templates/launch-checklist.md` | Phase 11 |

## When sources disagree

The references record disagreements as `Conflict:` notes instead of hiding them. Trust in this order: the house rules, then current official Roblox documentation, then the owner's vault numbers (for market position), then measured results from the game in front of you, then `[lihfolk]` and `[community]` practice. A number measured on the user's own game beats any benchmark.

## Completion criteria

A task under this skill is done when:

1. The relevant gate has been checked item by item and the result reported: the phase gate in `references/checklists.md` for a build task, Gate A for a level-up pass, or the review gate at the end of the reference used.
2. Any `[VS]` fact relied on has been re-checked against the official docs (https://create.roblox.com/docs, or the `Roblox/creator-docs` mirror on GitHub when that site is unreachable), or the user has been told exactly which facts were not re-checked.
3. New Luau is `--!strict`, passes Selene and StyLua, and has at least one test or a described manual test.
4. No house rule is violated by the work delivered: no visible primitive Parts, world meshes collide, no invasive offers, no generated or marketplace content shipped. In Level-up mode, existing violations are listed as findings with a plan.
5. The user received a clear recommendation plus a bolder alternative wherever a real choice existed, pitched at their level.
6. In Level-up mode: every score has evidence, the action list is ranked, the top actions are shipped or handed over with exact steps, and each change names the metric that will show whether it worked.
