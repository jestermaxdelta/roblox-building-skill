---
name: roblox-game-design
description: "One-shot playbook that takes any Roblox game to the next level, at any stage: a new idea, a prototype, or a fully built live game that needs an audit. Covers concept and genre choice (with per-genre playbooks), core-loop design and tuning, FTUE, economy math, retention and LiveOps, non-invasive monetization (boosts, passes, starter pack, gifts, Luck), UI/UX design with Figma, the Blender-to-Roblox art pipeline, Luau architecture (Rojo, ProfileStore, remotes), security and anti-exploit, performance for low-end mobile, analytics, discovery, growth and launch. Use this skill whenever the user is making, designing, planning, scripting, balancing, monetizing, optimizing, auditing, reviewing, fixing or launching a Roblox game or experience, even if they only say \"my game\" in a Roblox or Luau project; when they ask why a Roblox game is not retaining, earning, growing or running well; when writing Luau systems, DataStores, purchases or UI; when working in Roblox Studio (including through the Studio MCP); or when asking what Roblox game to build. Enforces the house rules: every model from Blender, everything solid, heavy but never invasive monetization."
---

# Roblox game design and development

This skill takes a Roblox game to the next level from wherever it is now: an idea, a prototype, or a finished live game. It bundles three entry modes, a phased workflow, decision rules, the owner's non-negotiable house rules, and routed reference files. The references are distilled from a 9,389-line knowledge base (compiled 2026-11-08 from 31 repositories and the owner's research vault) plus a 2026-11-10 research pass over developer forums, Reddit, GitHub and the Creator Docs. Code snippets in the references are unexecuted: treat them as starting points to test, not as verified code.

Two meanings of "efficient" apply at once. Efficient games: frame budgets, low-end mobile first, streaming, bandwidth, memory. Efficient development: design before build, vertical slice first, build order, scope cuts, reusable modules, Rojo/Wally/Selene/StyLua/luau-lsp and tests.

"Well thought out" means design before build. Before writing gameplay code, the player fantasy, three pillars, core/session/long-term loops, FTUE script, economy model with numbers, retention and social hooks and a risk list exist and have been reviewed against the rubrics.

## Pick the mode first

Work out which situation the user is in before opening anything else. The modes share the same references but start in different places, and starting in the wrong one wastes the user's time (a GDD for a game that already ships, or a rebuild when three fixes would do).

| Mode | Use when | Start at | Output |
|---|---|---|---|
| **A. New game** | There is an idea or nothing yet | Phase 1 of the workflow below | The phase outputs, one gate at a time |
| **B. Level-up** | A game already exists (prototype, soft launch or live) and the goal is "make it better", "why is it not growing/retaining/earning", "review my game", "optimise it" | `references/audit-existing-game.md` | `templates/game-audit-report.md` filled: scores with evidence, a ranked action list, then the top actions executed |
| **C. Single fix** | One system, one bug, one balance tweak, one question | The matching row of the routing table | The fix, checked against that row's gate |

Level-up mode in short (the audit reference has the full method):

1. **Intake.** Ask for what exists: genre, age and platform mix, analytics (retention, session time, funnel, payer conversion, crash rate), the place or Rojo repo, Studio MCP access, and the owner's goal. Missing numbers are fine; say what you assumed.
2. **Inspect before judging, read-only.** Read the code and DataModel, play the first ten minutes through the Studio MCP if it is connected, and open the genre file for the game in `references/genres/`. Change nothing yet.
3. **Score the ten dimensions** (first session, core loop, progression and economy, retention and LiveOps, monetisation, UI/UX, art and house rules, performance, security and data, discovery and growth) with evidence for each score.
4. **Rank by impact × confidence ÷ effort.** Fix in funnel order unless something is on fire: data loss, exploits and crashes first, then first-session bounce, then the core loop, then retention, then monetisation, then growth. Sending more players into a leaky first session wastes them.
5. **Execute the top actions with the safe-change protocol**: back up the place version, put changes behind Configs flags, never break saves, change one variable at a time, and say how the result will be measured.
6. **Re-measure and repeat.** A level-up pass is done when the top actions are shipped or handed over with clear steps, not when the report is written.

House rules in Level-up mode: an existing game often breaks them (primitive Parts, marketplace models, walk-through props, pushy popups). Treat each violation as a finding with a migration plan ranked by how visible it is, rather than blocking every other fix until the whole map is rebuilt.

## How to use the references

- Open only the reference files the routing table points at for the current task. Each is 100–300 lines and ends with a review gate.
- `references/knowledge-base.md` is the full 645,989-byte source. Never read it whole. Grep it by section heading, then read that range only:
  `grep -n "^## 4.7" references/knowledge-base.md` (section start), then `grep -n "^## 4.8"` for the end, then Read with offset/limit. Section map: 1.x design, 2.x game craft and architecture patterns, 3.x platform/economy/monetization/analytics/discovery, 4.x engineering/security/data/purchases, 5.x performance/art/UI/input/launch. `## 3.12` and `## 5.14` list known conflicts.
- Facts marked `[VS]` are version-sensitive (API names, limits, prices, policy, dashboard features). Re-check them at https://create.roblox.com/docs before relying on them. Market numbers date from a 2026-11-07 snapshot.
- For market data (trending genres, what to build, discovery, thumbnails), open `references/market-scan-2026-11.md` first: it distils the owner's Nov 2026 research bundle and the v2 report (a converted copy sits in `references/market-research-v2-raw.md` for grep). For the full note set read the Obsidian vault folder `C:/Users/Nebula PC/Documents/Delta Vault/Roblox Research/2026-11 Market Scan/` — start with `_MOC.md`, then `_AGENTS.md`. Read `Agent Vault Guide.md` and `hot.md` in the vault root first. Those numbers are a 2026-11-07 snapshot. The vault lives on the owner's PC: when it is not reachable (cloud sessions, other machines), the distilled copies in `references/` are the authority and nothing is lost.
- Claims tagged `[community]` come from developer forums, Reddit and videos: treat them as heuristics to test, not guarantees. `[official]` marks Roblox documentation, `[house]` marks house estimates.

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

## Phased workflow: idea to live

Work the phases in order. Each phase names its outputs, the reference to open and the gate that must pass before the next phase. Do not start a later phase on a system whose earlier gate failed.

| Phase | Outputs | Open | Gate |
|---|---|---|---|
| 1. Concept and genre | Pitch, fantasy, the one new verb, comparables, genre loop, age tier, platform priority | `references/market-scan-2026-11.md`, `references/genre-playbooks.md`, `references/design-foundations.md` §fun | Pitch fits one sentence; genre loop named; the new action or visible journey named; mobile-first confirmed |
| 2. One-pager and pillars | `templates/game-one-pager.md` filled | `references/process-and-playtesting.md`, `references/design-foundations.md` | Core-loop rubric ≥ 7/10; three pillars are decision rules |
| 3. Loops, FTUE and economy model | Loop timings, 5-minute FTUE script, `templates/economy-balance-sheet.md` filled with numbers | `references/economy-and-progression.md`, `references/liveops-quests-retention.md` §onboarding | First reward < 30 s; sink ratio 0.95–1.05 modelled; rebirth wait ratio ×1.2–1.5 |
| 4. Lean GDD and architecture plan | `templates/lean-gdd.md`; remotes list; data schema; products table; streaming and collision policy | `references/engineering-architecture.md`, `references/architecture-patterns-luau.md`, `references/networking-and-security.md` §surface design | Gate 0 in `references/checklists.md` passes |
| 5. Build order and vertical slice | Rojo project, loader, DataService, RemoteGuard, ReceiptService stubs; one playable loop with blockout kit | `references/engineering-architecture.md`, `references/data-and-purchases.md`, `references/networking-and-security.md` | Gate 1: five strangers; kill/keep decided (`templates/playtest-plan.md`) |
| 6. Game craft pass | Feel, camera, level kit, audio, AI, UI design | `references/game-craft.md`, `references/ui-input-crossplatform.md` | Response times and juice tiers met; mobile layout tested |
| 7. Art pipeline | Style bible, kit list, Blender assets → GLB → Open Cloud, post-import fixup, lighting preset | `references/art-pipeline-blender.md` | Art review gate; house-rule scan OK |
| 8. Monetization | `templates/monetization-product-plan.md`; products created; offer gate; receipts tested | `references/monetization-and-policy.md`, `references/data-and-purchases.md` §purchases | Gate 3 compliance passes |
| 9. Analytics and LiveOps plan | `templates/analytics-event-plan.md`; Configs; Experiments; 4-week update plan; first event | `references/analytics-and-discovery.md`, `references/liveops-quests-retention.md` | Events verified in a test place |
| 10. Performance pass | MicroProfiler captures, budgets table filled, streaming settings, collision audit | `references/performance.md` | Gate 4 on a 2–4 GB Android phone |
| 11. Launch | `templates/launch-checklist.md` signed; thumbnails, metadata, age tier, timing | `references/analytics-and-discovery.md` §discovery, `references/checklists.md` Gate 5 | All gates signed |
| 12. LiveOps | Weekly update day, events, season pass, funnel fixes, safety review | `references/liveops-quests-retention.md`, `references/analytics-and-discovery.md` | Weekly KPI review done |

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

Engineering

- Plain modules plus a two-phase Init/Start loader is the default framework; jecs or Matter ECS only for simulation-heavy games; no Knit for new projects.
- One server entry, one client entry; no Scripts inside models; behaviour by CollectionService tags; `emitLegacyScripts: false`.
- `--!strict` everywhere; untrusted input is `unknown`; remotes carry intent, never outcome; every remote behind RemoteGuard rate limiting and validation.
- ProfileStore with session locking, schema version and migrations before `Reconcile`; a failed load never saves; purchases idempotent by `PurchaseId` saved before `PurchaseGranted`.
- Toolchain: Rokit pins Rojo, Wally, Selene, StyLua, luau-lsp, Lune; CI publishes via Open Cloud; only CI publishes production.
- Prefer Luau over Parallel Luau until profiling proves a parallel win; prefer spatial queries over `Touched` for gameplay.

Art and performance

- 1 Blender unit = 1 stud; kit grid 5/8/16 studs; pivots at the snap point; texel density about 50 px/stud; shared `_SA` trim-sheet library.
- Budgets (house estimates, not official): < 1,000 draw calls, < 1 M triangles in the worst view, ≥ 30 FPS on low-end Android, ≥ 60 Hz server heartbeat, server memory < 50% of the limit.
- Streaming on; interactive models Atomic; code never indexes Workspace without tags or a timeout.
- Collision: static geometry anchored; `Box` for non-colliding visuals, `Hull`/`Default` or a `_COL` proxy mesh for walkable geometry; `PreciseConvexDecomposition` only for approved doorways.

Monetization

- Default product set first; delete what does not fit; never sell stat power in competitive modes; free alternative next to every paid shortcut.
- Offer gate defaults: 600 s grace and a first win; 480 s gap; ≤ 3 per session; ≤ 1 starter pack per day; two dismissals → 24 h silence; ≤ 25% of the screen with an X.
- Prices come from `MarketplaceService:GetProductInfoAsync` at runtime; the plan's price column is only the Creator Hub setup value.

When a design choice matters, give the user a clear lower-risk option and a bold higher-risk option, state the trade-offs and name the one you recommend.

## Never do

Security

- Never trust the client for ids, prices, damage, positions, currency or inventory; never grant from `PromptProductPurchaseFinished` or any client signal.
- Never use `RemoteFunction:InvokeClient`; never store secrets, API keys or server logic in ReplicatedStorage, StarterPlayer or any client-visible container.
- Never ban on a single heuristic; never kick for a transient DataStore error.

Purchases and data

- Never return `PurchaseGranted` before the grant is saved; never register two `ProcessReceipt` callbacks; never skip `PurchaseId` deduplication.
- Never save a profile that failed to load; never change the key pattern of a live store; never wipe data in a migration without a backup path; never read DataStores in a gameplay hot path.

Policy and monetization

- Never fake discounts, restart countdowns or claim false scarcity; never show offers during onboarding, loading or combat; never stack popups or block play with them.
- Never sell paid random items without full odds disclosure and `PolicyService` gating; never ship unfiltered user text.
- Social rewards (group join, like, favourite, friend join) are wanted in every game, as a bonus only: never gate progress or core content on them, never put "free Robux", giveaways or "like for rewards" in the title, thumbnail or description (that is the exposure penalty), and ask after the first win, not in the first minutes. Rules in `references/liveops-quests-retention.md` §social rewards.
- Never run rewarded video with random rewards or as a progress gate.

Content and tooling

- Never ship a visible primitive Part, placeholder, marketplace model or generated mesh; never leave a walkable mesh without collision; never enable Terrain without the owner's approval for that game.
- Never use deprecated APIs in new code: `wait`, `spawn`, `delay`, `tick`, `Humanoid:LoadAnimation`, BodyMovers, `FindPartOnRay`, `GetProductInfo` without `Async`.
- Never publish production from a local Studio when CI exists; never commit without `wally.lock` and lint passing.

## Using the Roblox Studio MCP

Use the Studio MCP as a build and test tool, not as a content generator.

- Allowed and encouraged: `execute_luau` for edit-mode scans, fixups, batch property edits and the house-rule scan; `script_read`, `script_grep`, `script_search` and `multi_edit` for Luau; `inspect_instance` and `search_game_tree` to audit the DataModel; `start_stop_play`, `get_console_output`, `screen_capture` and `user_*_input` for playtests; `open_cloud_invoke` for asset uploads and publishing; `get_studio_state` before any edit.
- Never use `generate_mesh`, `generate_procedural_model`, `generate_scene`, `generate_texture`, `generate_material`, `insert_asset` or `search_asset` for anything that ships. Blockouts from them stay in throwaway places only.
- Run scans and fixups in edit mode, never in live servers. Re-read instances after each `execute_luau` batch rather than assuming state.
- Prefer Rojo-synced source files for scripts; use `multi_edit` only when the project has no Rojo tree.

## Routing table

| Task | Open |
|---|---|
| Fun, motivation, flow, difficulty, FTUE, progression and retention theory, rubrics | `references/design-foundations.md` |
| Process, one-pager, GDD, milestones, scope triage, playtesting, postmortems | `references/process-and-playtesting.md` |
| Game feel, camera, level design, audio, AI, procgen, save design | `references/game-craft.md` |
| What to build, what is winning or saturated, the 14 shared patterns, cozy-management and +1 format norms, thumbnail rules 1–13, the 250-play gate, launch timing | `references/market-scan-2026-11.md` (raw report: `references/market-research-v2-raw.md`) |
| Choosing or shaping a genre (tycoon, simulator, cozy management, obby, horror, RPG, fighting, racing, social, roleplay, tower defence) | `references/genre-playbooks.md` |
| Game Programming Patterns in Luau (state, command, observer, component, object pool, ECS choice) | `references/architecture-patterns-luau.md` |
| Currencies, XP curves, costs, rebirth, offline income, luck and pity math, packs, trading | `references/economy-and-progression.md` |
| Products, passes, subscriptions, boosts, offers, gifts, rewarded video, policy, DevEx | `references/monetization-and-policy.md` |
| Onboarding, quests, badges, events, season pass, social and notification APIs | `references/liveops-quests-retention.md` |
| KPIs, AnalyticsService events, Configs, Experiments, RFY, thumbnails, age tiers, matchmaking | `references/analytics-and-discovery.md` |
| Containers, loader, Rojo layout, Luau standards, toolchain, CI/CD, Studio MCP working rules | `references/engineering-architecture.md` |
| Remotes, serialisation, RemoteGuard, exploit defence, bans, HttpService, secrets | `references/networking-and-security.md` |
| DataStore limits, ProfileStore, DataService, ReceiptService, passes, teleports, MemoryStore, MessagingService | `references/data-and-purchases.md` |
| Frame budgets, MicroProfiler, Luau idioms, rendering, streaming, physics, collision, VFX/audio budgets, loading | `references/performance.md` |
| Blender → GLB → Open Cloud, naming, collision authoring, textures, kits, packages, lighting presets | `references/art-pipeline-blender.md` |
| UI implementation, styling, text filtering, prompts, input mapping, mobile, console, VR, accessibility | `references/ui-input-crossplatform.md` |
| Every gate and checklist in one place, including the house-rule scan script | `references/checklists.md` |
| Full source text; grep by heading | `references/knowledge-base.md` |

Templates (copy into the game repo's `docs/` folder and fill in):

| Template | Use at |
|---|---|
| `templates/game-one-pager.md` | Phase 2 |
| `templates/lean-gdd.md` | Phase 4 |
| `templates/economy-balance-sheet.md` | Phase 3 |
| `templates/monetization-product-plan.md` | Phase 8 |
| `templates/analytics-event-plan.md` | Phase 9 |
| `templates/playtest-plan.md` | Phases 5–12, weekly |
| `templates/launch-checklist.md` | Phase 11 |

## Completion criteria

A task under this skill is done when:

1. The relevant phase gate in `references/checklists.md` has been checked item by item and the result reported.
2. Any `[VS]` fact relied on has been re-checked against the official docs, or the user has been told it was not.
3. New Luau is `--!strict`, passes Selene and StyLua, and has at least one test or a described manual test.
4. No house rule is violated: no visible primitive Parts, every visible mesh collides, no invasive offers, no generated or marketplace content shipped.
5. The user received a clear recommendation plus a bolder alternative wherever a real choice existed.
