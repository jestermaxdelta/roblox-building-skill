# Decision rules and never-do list

The standing rules by topic: the defaults to apply without being asked, and the lines never to cross. Open the block for the topic you are working on before you start, and check it again before you call the work done.

- The three house rules and what follows from them are in `SKILL.md`. They override every line here and are not repeated here.
- Each block names its owner guide, which holds the reasoning, the numbers and the code. Where a rule here and its owner guide differ, the guide is right.
- `[house]` marks a house estimate, not a Roblox figure. `[VS]` marks a platform fact to re-check before relying on it.

## Design

Owners: `references/design-foundations.md`, `references/core-loop-tuning.md`, `references/tutorial-and-onboarding.md`, `references/genre-playbooks.md`, `references/market-scan-2026-11.md`, `references/process-and-playtesting.md`.

- Mobile first: design the UI, controls and performance budget for a 3 GB Android phone, then widen to PC, console and VR.
- One new verb per game: copy the genre loop, change the verb and the fantasy. Management games stay hands-on in a small 3D space; any map layer plays like a toy.
- Classify a game by its host loop (what fills most minutes), then open one genre file. In a hybrid one genre hosts, the other is a layer, and the stricter rule applies.
- Loops are nested: micro 10–30 s, meso 5–15 min, session 15–25 min, meta days to weeks. Every loop has a visible goal and a next purchase.
- First session `[house]`: control within 10 s of joining, first verb by 15 s, first reward by 30 s, first upgrade by 2 min, one new concept per beat.
- A timed hint appears after the time most players need plus 1 s (start at 11 s, test 5 s against 10 s) and goes away on progress.
- A next goal with its progress and its reward is always on screen.
- Fix the earliest broken stage first: crashes and load time, then the first minute, the funnel, session length, D1, D7, D30. Reward systems (dailies, quests, passes) amplify a loop that works; they do not rescue one scoring under 5/10.
- Retention through content cadence, collections, social play and seasons. Never through punishment: no streak that resets, no pay-to-idle, no guilt notification, nothing lost while away.
- Kill or keep after five strangers play the prototype; keep only with evidence.
- Where a design choice matters, give a lower-risk option and a bolder one, the trade-off, and the one you recommend.

## Economy

Owner: `references/economy-and-progression.md`.

- Price from time: `req(L) = minutes(L) × xpPerMin(L)`; costs `floor(base × g^n)` with g 1.07–1.15; the first ten purchases take 3–10 s each.
- Sink ÷ faucet 0.95–1.05 as the design target; rebirth wait ratio ×1.2–1.5 between successive rebirths.
- Offline income is capped and the cap is stated (default 8–12 hours at 25–50%).
- Paid multipliers `[house]`: at most 4× permanent, 8× with timed boosts. The same boost extends its time, never multiplies.
- One function feeds both the displayed odds and the roll.
- Never reduce or revalue something bought with Robux. Rebalance by adding, not by taking away.

## Monetization

Owners: `references/monetization-and-policy.md`, `references/data-and-purchases.md` (receipts).

- Fix retention before pricing: spend follows session length.
- Start from the house default set and delete what does not fit. A free alternative sits next to every paid shortcut. Never sell stat power in competitive modes.
- Offer gate, as Config keys: no popup before 600 s of lifetime play and a first win; 480 s between popups; at most 3 a session; at most 1 starter-pack prompt a day; two dismissals silence that offer for 24 h; at most 25% of the screen, in a safe-area corner, with an X, never stacked.
- Popups fire on positive moments only (a win, a delivery, a level-up, a rebirth), never on death, failure, loading, join or combat. An offer that answers friction sits inline where the friction is.
- Passive surfaces (shop button, shelves, boost pill, a starter-pack tile in the shop) are unlimited from the first minute.
- Every price ladder has a rung under 100 R$ and at least one repeatable product.
- Prices come from `MarketplaceService:GetProductInfoAsync` at runtime; the plan's price column is only the Creator Hub setup value.
- Personal paid boosts count play time and pause offline; server-wide boosts run in real time and show their end. The product card says which.
- Every countdown is a server fact: the client renders from `endsAt` and `workspace:GetServerTimeNow()` and never starts a timer. A personal offer window is written to the profile once and never restarts.
- Paid random items: full numeric odds and the `PolicyService` gate. A restricted player is never sold the random item: sell it directly at expected value, give an earnable path, or hide the feature.
- Rewarded video rewards a fixed product: never random, never Robux, never a gate on progress.
- Social rewards (`references/liveops-quests-retention.md`, "Social rewards") are bonuses, never gates, and go through the offer gate after the first win. Group join (verified on the server) and friend join are the default. Like and favourite rewards are a `[VS]` risk: at most a small one-time honour-based thank-you, re-checked before shipping, left out if in doubt. No reward for off-platform actions. Nothing about rewards, giveaways or "free Robux" in the title, thumbnail or description.

## Purchases and data

Owner: `references/data-and-purchases.md`.

- ProfileStore with session locking, one key per player, a schema version, and migrations that run before `Reconcile` on a copy.
- A failed load kicks with a clear message. It never falls through to default data, and a profile that failed to load never saves.
- Never change the key pattern of a live store; never wipe data in a migration; never read DataStores in a gameplay hot path. Snapshot before any change to save logic.
- One `ProcessReceipt`. Grant and record the `PurchaseId` in one step, return `PurchaseGranted` only after the save is confirmed, and never grant from `PromptProductPurchaseFinished` or any client signal.
- No yield between a check and its write: that gap is where dupes live. Fetch web facts (group, pass, policy) at join and cache them.
- One-way transfers (gift, mail) debit the giver and confirm that save before crediting the receiver.
- Trading needs all of: immutable item GUIDs; the two-profile commit protocol, built from its full text (both profiles session-locked on one server, item locks honoured by every path that consumes or changes an item, currency escrowed); its fault-injection test passed; a ledger; a kill switch.

## Engineering

Owners: `references/engineering-architecture.md`, `references/luau-mastery.md`, `references/gameplay-systems-cookbook.md`, `references/physics-and-vehicles.md`, `references/debugging-and-testing.md`.

- Plain modules with a two-phase Init/Start loader. jecs only for thousands of similar entities. No Knit, Mantle or TestEZ in new work.
- One server entry and one client entry; no Scripts inside models; behaviour by CollectionService tags.
- `--!strict` everywhere; untrusted input is typed `unknown`.
- Modern APIs only: `task.*`, `Animator:LoadAnimation`, constraints, `Raycast`, `...Async` calls. Never the deprecated `wait`, `spawn`, `delay`, `Humanoid:LoadAnimation`, BodyMovers, `FindPartOnRay` or `GetProductInfo`. House standard: `os.clock()`, `os.time()` or `workspace:GetServerTimeNow()` in place of `tick()`.
- Toolchain pinned with Rokit: Rojo, Wally (commit `wally.lock`), Selene, StyLua, luau-lsp, Lune. Tests: Lune for Instance-free logic, Jest Roblox in engine.
- Luau before Parallel Luau, `--!native` or `buffer`: adopt those only after a capture at the live optimisation level shows the hot path.
- Spatial queries for gameplay; never damage or rewards on `Touched`.
- Effects are built on clients: the server sends one validated event, each client renders, the caster predicts. Server hit timing comes from exported marker times; a client animation marker is a claim, not proof.
- Crowds (enemies, pets, workers, droppers) are server data with pooled client-rendered models, never one Humanoid or physical part each.
- Every unanchored object has one mover and one written network owner.
- Server authority (`Workspace.AuthorityMode = Server`, full release July 2026 `[VS]`) for competitive shooters, racing, sports and fighting games; client ownership plus server checks elsewhere. Never retrofit it into a live game in place.
- Never "fix" a bug with a wait, a longer timeout or a silent `pcall`. A fix needs a written repro with its failure rate and a run count at least twice what it took to fail.

## Security

Owner: `references/networking-and-security.md`.

- Never trust the client for ids, prices, damage, positions, currency or inventory. Remotes carry intent, never outcome; every remote sits behind validation and rate limiting.
- Never use `RemoteFunction:InvokeClient`. No secrets, API keys or server logic in ReplicatedStorage, StarterPlayer or any client-visible container.
- Never ban on one signal or on a client-side detection. A honeypot hit justifies a session kick; a ban needs several independent signals.
- Treat `require(<number>)`, `getfenv`, `loadstring` and obfuscated strings as findings until explained.

## UI

Owners: `references/ui-design-figma.md` (look), `references/ui-input-crossplatform.md` (engine), `references/ui-screen-recipes.md`, `references/ui-motion-and-feedback.md`.

- Design at the small-phone frame and widen; never shrink a desktop layout.
- Native first: buttons, panels, cards and bars are built from `UICorner`, `UIStroke`, `UIGradient` and `UIShadow`. Use an image only for texture, a silhouette that is not a rounded rectangle, or a repeated element that would need more than about 10 instances. Stay under 300 strokes and 100 shadows on screen.
- Images carry no text, are at most 1024 px on the longest side, and stretch by 9-slice.
- No colour, font, size, spacing or timing outside the theme module.
- Never hard-code the top-bar height or the jump-button position: read the insets.
- Pass lines, measured on the drawn result: text at least 12 px (design targets: HUD 18, body 16, captions 14), taps at least 44 px (48 on the HUD), gaps at least 8 px, no overlapping targets, at most 7 HUD groups, no signal carried by colour alone.

## Feel, effects, camera and audio

Owners: `references/vfx-and-juice.md` (hit-stop and shake numbers), `references/game-craft.md` (input windows), `references/accessibility-and-player-qol.md` (comfort), `references/cutscenes-and-cinematics.md`, `references/audio-sfx-music.md`, `references/animation-and-rigs.md`.

- Every press shows something on the frame it is read. Combo buffer 0.15–0.20 s, never above 0.30 s.
- Hit-stop is client-only: none on light hits, at least 66 ms where it must be felt, at most 200 ms per stop and 140 ms in any 0.6 s.
- No camera roll in gameplay. Shake is at most 2° of pitch and yaw and ends at exactly 0. One module owns `Camera.FieldOfView`.
- Shake, flashes, hit-stop and cutscene motion all read one comfort resolver that follows `GuiService.ReducedMotionEnabled`; no system reads the settings itself. At most 2 large flashes a second.
- Scale effects from the player's own preset and measured frame time. Never read `UserGameSettings.SavedQualityLevel`.
- Never carry gameplay information by shadows, bloom, post effects or sound alone, and never cull a telegraph to save frames.
- Cutscenes are client-only, have one restore function for every exit path, show Skip at 2 s on any scene over 3 s (`cutscenes-and-cinematics.md` §8), and do not run on first join except the short, skippable intro allowed for horror and story-led games (`tutorial-and-onboarding.md` §2).
- Animation: publish clips under the game's owner; never ship temporary ids (`RegisterKeyframeSequence`, `RegisterAnimationClip`); load each track once; set `Priority` before `Play`.
- Audio: use only sound the owner has the right to use and keep an id manifest. Roblox's licensed Creator Store audio is licensed for use inside Roblox only: a trailer or clip posted elsewhere needs owned or commissioned sound `[VS]`.

## Art and performance

Owners: `references/art-pipeline-blender.md`, `references/art-direction-and-quality-bar.md` (style bible, §6), `references/performance.md`, `references/level-design-worldbuilding.md`.

- 1 Blender unit = 1 stud; one kit grid per game (5, 8 or 16 studs for architecture); pivots at the snap point.
- One style bible, one texturing method and one texel density per game (about 50 px per stud `[house]`, or none for palette-atlas art); shared `_SA` SurfaceAppearances.
- Each kit piece is uploaded once and referenced by package, never by a hand-typed MeshId.
- Budgets `[house]`: under 1,000 draw calls and 1 M triangles in the worst view; at least 30 FPS in the busiest scene on low-end Android; server heartbeat 60 Hz. Server memory under 50% of its limit and under 3 GB (dashboard guidance).
- Streaming on; interactive models Atomic; code never indexes Workspace without tags or a timeout; teleports, portals, respawns and remote cutscene stages call `RequestStreamAroundAsync` first.
- Collision: static geometry anchored; `Box` for small props and non-colliding visuals, `Hull` for medium props, a `_COL` proxy for walls, doorways and stairs; `PreciseConvexDecomposition` only for approved doorways.

## Live games

Owners: `references/audit-existing-game.md` (safe-change protocol, §9), `references/analytics-and-discovery.md` (benchmarks, Configs, Experiments, ranking), `references/engineering-architecture.md` (update runbook), `references/growth-and-marketing.md` (readiness gate).

- Inspect before changing: dashboards, then one low-end phone, then read-only scans, then fixes.
- No live change without a baseline number, a Config flag and a rollback trigger written first. One variable at a time.
- A published Config reaches servers in about 15 s to 1 min, but a `ConfigSnapshot` never updates itself: connect `UpdateAvailable` to `Refresh()`, or the kill switch never reaches running servers.
- Publishing does not move players: use Restart Servers (outdated servers only, with a delay), and ship features dark behind a flag.
- Only CI publishes production when CI exists. Exception: the Open Cloud publish skips `SurfaceAppearance` and unions, so art-changing releases publish from Studio and are verified live.
- One Config key per experiment, run for the planned 14–60 days. Under about 1,000 DAU, or when the dashboard's minimum detectable effect is larger than the effect expected, compare weekly new-user cohorts instead.
- Benchmarks: the game's own Creator Analytics percentile first, then the one benchmark table in `references/analytics-and-discovery.md`. Never triage from genre D1 ranges or mobile-industry rules of thumb.
- Ranking `[VS]`: since 15 June 2026 Recommended For You reads play-through rate, first-play bounce and retention separately over 28 days; qualified play-through no longer ranks (thumbnail personalisation still reports it). Never compare PTR across 12 October 2026.
- No paid traffic while bounce or D1 sits below the dashboard benchmark median (no dashboard benchmark: D1 above 11% `[house]`), likes sit under 85% or the crash rate is above 2–3%.

## Safety, policy and legal

Owners: `references/community-moderation-safety.md`, `references/monetization-and-policy.md` (policy), `references/team-business-legal.md`.

- Players converse only through `TextChatService`; every player-written string is filtered.
- No links, invite codes, handles or requests for personal data inside the game. Social links live on the game's page.
- Legal, tax and IP topics: state the documented fact with its date and point to the current Roblox terms and a professional. Never present it as advice.

## Tooling

Owners: `references/studio-workflow.md`, `references/engineering-architecture.md` (Studio MCP rules), `references/ai-toolchain-skills.md`.

- Never run Script Sync and Rojo on the same scripts. Never point `rojo serve` at a Studio-owned live place: pull it into files first (`rojo syncback`) and set `servePlaceIds` to the dev place.
- Through the Studio MCP on a live game: read-only first, edits in edit mode behind a saved version, never save, publish or delete unasked.
- Never install a third-party skill, plugin or MCP server unread: pin a commit, never pipe to a shell, never paste keys or cookies.
