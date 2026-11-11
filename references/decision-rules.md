# Decision rules and never-do list

The skill's standing rules by topic: the defaults to apply without being asked, and the lines never to cross. `SKILL.md` carries the house rules and the short list that applies to every task; this file is the complete set. Open the block for the topic you are working on before you start, and check it again before you call the work done. Each rule's reasoning and detail live in the reference that owns the topic (`references/INDEX.md`).

## Decision rules

### Design

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

### Engineering

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

### UI

- Design at the small-phone frame first and scale up; never shrink a desktop layout. Structure and text are native instances, artwork is exported images (9-slice), no baked text, nothing over 1024 px.
- No colour, font, size or timing outside the theme module. Never hard-code the top-bar height or the jump-button position: read the insets.
- Pass lines: text at least 12 px drawn, taps at least 44 px, 8 px gaps, and no signal carried by colour alone.

### Art and performance

- 1 Blender unit = 1 stud; kit grid 5/8/16 studs; pivots at the snap point; texel density about 50 px/stud; shared `_SA` trim-sheet library.
- Budgets (house estimates, not official): < 1,000 draw calls, < 1 M triangles in the worst view, ≥ 30 FPS on low-end Android, ≥ 60 Hz server heartbeat, server memory < 50% of the limit.
- Streaming on; interactive models Atomic; code never indexes Workspace without tags or a timeout.
- Collision: static geometry anchored; `Box` for non-colliding visuals, `Hull`/`Default` or a `_COL` proxy mesh for walkable geometry; `PreciseConvexDecomposition` only for approved doorways.

### Monetization

- Default product set first; delete what does not fit; never sell stat power in competitive modes; free alternative next to every paid shortcut.
- Offer gate defaults: 600 s grace and a first win; 480 s gap; ≤ 3 per session; ≤ 1 starter pack per day; two dismissals → 24 h silence; ≤ 25% of the screen with an X.
- Prices come from `MarketplaceService:GetProductInfoAsync` at runtime; the plan's price column is only the Creator Hub setup value.
- Every price ladder has a rung under 100 R$ and at least one repeatable product: the median payer spends under a dollar, and repeat spend days are a discovery signal.
- Popups only after a win. An offer that answers friction (out of space, out of energy) sits inline where the friction is, never as a popup.
- Personal paid boosts count play time and pause offline; server-wide boosts run in real time and show their end. State which on the product.
- Never reduce or revalue something a player bought with Robux. Rebalance by adding, not by taking away.
- Fix retention before pricing: spend follows session length.

### Live games

- Inspect before changing: dashboards, then one low-end phone, then read-only scans, then fixes.
- No live change without a baseline number, a Config flag and a rollback trigger. Snapshot DataStores before any change to save logic.
- One Config key per experiment. Under about 1,000 DAU there is not enough traffic for a clean A/B: compare weekly cohorts instead.
- No paid traffic while D1 sits below the genre's benchmark median or likes sit under 85%. Ads send players into the funnel you have; they do not fix it.

When a design choice matters, give the user a clear lower-risk option and a bold higher-risk option, state the trade-offs and name the one you recommend.

## Never do

### Security

- Never trust the client for ids, prices, damage, positions, currency or inventory; never grant from `PromptProductPurchaseFinished` or any client signal.
- Never use `RemoteFunction:InvokeClient`; never store secrets, API keys or server logic in ReplicatedStorage, StarterPlayer or any client-visible container.
- Never ban on a single heuristic or on a client-side detection alone; never kick for a transient DataStore error.
- Treat any `require(<number>)`, `getfenv`, `loadstring` or obfuscated string in a place as a finding until explained: that is what a backdoor looks like.
- Never run a trading system without item GUIDs, an audit log and a kill switch.

### Purchases and data

- Never return `PurchaseGranted` before the grant is saved; never register two `ProcessReceipt` callbacks; never skip `PurchaseId` deduplication.
- Never save a profile that failed to load; never change the key pattern of a live store; never wipe data in a migration without a backup path; never read DataStores in a gameplay hot path.

### Policy and monetization

- Never fake discounts, restart countdowns or claim false scarcity; never show offers during onboarding, loading or combat; never stack popups or block play with them.
- Never sell paid random items without full odds disclosure and `PolicyService` gating; never ship unfiltered user text.
- Social rewards (group join, like, favourite, friend join) are wanted in every game, as a bonus only: never gate progress or core content on them, never put "free Robux", giveaways or "like for rewards" in the title, thumbnail or description (that is the exposure penalty), and ask after the first win, not in the first minutes. Group-join and friend-join bonuses are the safe default; before rewarding likes or favourites, re-check the current Roblox Community Standards `[VS]` and leave them out if in doubt. Rules in `references/liveops-quests-retention.md` §social rewards.
- Never run rewarded video with random rewards or as a progress gate.
- Never let players converse outside `TextChatService`; never put links, invite codes, handles or requests for personal data in the game. Social links live on the game's page.
- Never ship a timer, discount or stock count that is not literally true.
- Never present legal, tax or IP guidance as advice: state the documented fact with its date and point to the current Roblox terms and a professional.

### Content and tooling

- Never ship a visible primitive Part, placeholder, marketplace model or generated mesh; never leave a walkable mesh without collision; never enable Terrain without the owner's approval for that game.
- Never use deprecated APIs in new code: `wait`, `spawn`, `delay`, `tick`, `Humanoid:LoadAnimation`, BodyMovers, `FindPartOnRay`, `GetProductInfo` without `Async`.
- Never publish production from a local Studio when CI exists; never commit without `wally.lock` and lint passing. Exception: the Open Cloud place publish does not carry some art data (SurfaceAppearance, unions), so art-changing releases publish from Studio and are verified live (`references/studio-workflow.md`).
- Never ship temporary animation ids (`RegisterKeyframeSequence`, `RegisterAnimationClip`): they work in Studio and are dead live. Publish clips under the game's owner.
- Never run Script Sync and Rojo on the same scripts; never point `rojo serve` at a live place another session owns.
- Never install a third-party skill, plugin or MCP server unread; pin a commit, never pipe to a shell, never paste keys or cookies (`references/ai-toolchain-skills.md`).
- Never carry gameplay information by shadows, bloom, post effects or sound alone: low-end devices drop them.
