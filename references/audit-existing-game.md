# Level-up mode: auditing and improving an existing game

Method for pointing the skill at a game that already exists (prototype, soft-launched, live, plateaued or declining) and producing a ranked, evidence-based improvement plan, then executing it without breaking saves or the live audience. Open it whenever the user says "improve", "audit", "optimise", "why is my game not growing" or hands over a place file, a Rojo repo or analytics screenshots. Output goes into `templates/game-audit-report.md`; `references/checklists.md` Gate A is the short form.

## Operating rules

- Evidence before opinion. Every finding cites a number, a screenshot, a script path and line, or a timed observation. "Needs polish" is not a finding.
- Read-only first. No edit, publish, config change or DataStore call until the report is accepted.
- Fix in funnel order (reach → stability → first session → D1 → D7 → D30 → monetisation → paid growth). A fix lower in the funnel is wasted while a higher step leaks. Roblox's own guidance: if retention is low, fix core gameplay first; improve monetisation once retention is strong `[official]`.
- House rules are findings, not preferences: visible primitives, marketplace or generated assets, walk-through meshes and invasive offers are P0 regardless of metrics.
- One variable per dimension per week, measured against a recorded baseline.

## 1. Intake

Ask (skip what the repo or dashboard already answers):

| # | Question | Why |
|---|---|---|
| 1 | Universe ID, place IDs, genre, age guideline, public since when? | Scope; Kids/Select gate status |
| 2 | Goal for the next 6 weeks: CCU, retention, revenue, or reach under-16s? | Picks the target metric |
| 3 | DAU, CCU peak, visits, rating %, favourites today and 30 days ago? | Trend, sample size |
| 4 | What changed in the last 30 days (updates, thumbnails, title, ads, prices)? | Separates self-inflicted from platform causes |
| 5 | Who owns the source: Rojo repo, Script Sync, or Studio only? Is CI publishing? | Decides how fixes are applied |
| 6 | Data layer: ProfileStore, DataStore2, raw DataStore? Schema version? Any data-loss reports? | Migration risk |
| 7 | Team size, hours per week, art source (Blender, Toolbox, generated)? | Effort scale; house-rule debt |
| 8 | Fixed update day? Last update date? Community size (group, Discord)? | LiveOps and growth baseline |

Collect:

- Creator Hub screenshots or exports, 28–90 days: Overview (benchmark scorecards), Acquisition (sources, PTR, new-user funnel, **Home Recommendations** signals), Retention (D1/D7/D30 and cohort table), Engagement (session time, first-session retention curve), Monetisation (conversion, ARPPU, ARPDAU, top products), Economy, Funnels, Performance (client and server, by platform and by **Place Version**), Error report, Feedback (rating trend and comments), Thumbnail performance table.
- The game page: title, description, icon, all thumbnails and video, events, social links, group.
- Access: Studio open on the place with the MCP server on, or the `.rbxl` / Rojo repo. A separate test universe for anything that writes.

Data unlock thresholds `[official][VS]`: dashboards need > 10 DAU and 10 play hours for 7 days; benchmarks, Performance charts, alerts and insights need 100+ DAU; AI analytics reports 1,000+ DAU; feedback reports 20+ comments; safety dashboard 1,000+ daily hours.

Pulling numbers without screenshots `[official][VS]`: Open Cloud **Analytics Query API** (`POST https://apis.roblox.com/analytics-query-api/v1/universes/{universeId}/metrics`, body `metric`, `granularity`, `startTime`, `endTime`, optional `breakdown`, `filter`) and the experimental **Benchmarks API** (`POST https://apis.roblox.com/analytics-benchmark/v1/universes/{universeId}/benchmarks`, percentiles 10/50/90, types genre / similarity / top experiences). Scope `universe.analytics:read`; through the Studio MCP it sits in the "Look at your game" permission group and is called with `open_cloud_invoke`. Standard metrics keep up to 4 years, performance metrics 28 days. Useful metric names: `ForwardD1Retention`, `ForwardD7Retention`, `ForwardD30Retention`, `AverageSessionLengthMinutes`, `AveragePlayTimeMinutesPerDAU`, `DailyActiveUsers`, `PayingUsersCVR`, `AverageRevenuePerPayingUser`, `AverageRevenuePerUser`, `RFYPlayThroughRate`, `RFYDuration0To60`, `RFYDuration61To180`, `RFYD2To7PlayDays`, `RFYD8To28PlayDays`, `ClientCrashRate15m`, `OomUnexpectedExits`, `ClientFpsAvg`, `ClientMemoryUsagePercentageAvg`, `ServerFrameRateAvg`, `ThumbnailQualifiedPTR`, `FunnelStepChurnRate`.

## 2. Benchmarks to score against (snapshot 2026-11-10) `[VS]`

Rule: the game's own Creator Analytics benchmark (similar players → genre → all; shown as P50–P90, or P10–P50 where lower is better) beats every published number. Public figures are a fallback for games under 100 DAU.

| Metric | Reference value | Source and grade |
|---|---|---|
| D1 / D7 / D30 median | 10.3% / 1.6% / 0.5%; top 1%: 22.2% / 9.1% / 4.7% | GameAnalytics 2025 Roblox report via third-party summary `[community]` (search summary) |
| D1 by average session | 4.3% (0–3 min), 7.9% (7–12), 10.2% (13–18), 11.5% (19–24); top 2% 32.3%; D7 top 2% 8.5% | Same report, via the vault (market-scan-2026-11.md) |
| D1 dashboard example | P50–P90 = 12.11–18.73% | Creator docs example, not a platform benchmark `[official]` |
| Genre D1 | Obby 25–35, tycoon 20–28, shooter 22–30, roleplay 15–22 | RoWatcher, unsourced `[community]`; treat as optimistic |
| Session length | Median 6.6 min; hits in the vault sample 14–27 min; house target 19+ min | Vault; `[house]` target |
| Daily playtime | Median 16.8 min, top 10% 64.9 min; RFY counts at most 60 min per user per day | Vault; `[official]` cap |
| PTR, first-play bounce | No public number. Use the dashboard benchmark; never compare across 12 Oct 2026 | `[official]`; no evidence found for a public value |
| Payer conversion, ARPPU, ARPDAU | No reliable public Roblox benchmark found. Dashboard benchmarks exist for all three | `[official]` (benchmark exists); no evidence found otherwise |
| Like ratio | Ad-running games median 79%, others 92%; house floor 85% before any paid traffic | Vault sample `[community]` |
| Client crash rate | Investigate above 2–3%; Roblox's own alert example fires at 5% for 5 minutes | Vault "Doc" value; `[official]` alerts page |
| Client memory | Memory-usage-percentage line near 100% on a platform means out-of-memory exits | `[official]` |
| Server | Frame rate 60; CPU time < 16 ms; memory < 50% of the server total, or under 3 GB as a rule of thumb | `[official]` |
| Thumbnail personalisation | +8.5% qualified PTR on average, up to +50% | `[official]` |

Conflict: the vault's GameAnalytics D1 figures are cut by session length (11.5% at 19–24 min) while the third-party summary quotes one overall median (10.3%). They are different cuts of the same report, not a contradiction; use the session-length cut when the game's session time is known.

## 3. Scorecard: 10 dimensions, 0–5

Scale: 0 absent or broken · 1 present but fails its gate · 2 works with major gaps, or metric below benchmark median · 3 gate passed, metric near median · 4 above median, minor gaps · 5 top decile (P90, or P10 where lower is better) and the gate passes in full.
Caps: no live numbers → the dimension scores at most 3. Any house-rule, policy, data-loss or client-trust hit → at most 1 for that dimension.

| # | Dimension | Observe | 1 looks like | 3 looks like | 5 looks like |
|---|---|---|---|---|---|
| 1 | First session (FTUE) | Join-to-playable seconds on a 3 GB phone; seconds to first reward and first upgrade; bounce < 60 s and 61–180 s; first-session retention curve; onboarding funnel | Lobby, menu or text wall before play; first reward > 2 min; prompt or offer in the first minutes; no funnel events | Playable < 15 s after join, first reward < 60 s, one funnel step loses > 40% `[house]`, bounce near median | First reward < 30 s, first upgrade < 2 min, goal ladder on screen, no funnel step loses > 25% `[house]`, bounce in the best decile |
| 2 | Core loop | Loop rubric (design-foundations.md); seconds per loop; the one verb; session time; do strangers start a second loop unprompted | A number ticks on a menu; no decision; loop does not close; session < 5 min | Loop closes in 10–30 s with a visible goal and next purchase; rubric 7/10; session near median | Rubric 9+; session ≥ P90 or 19+ min; D1 playtime ≥ P90; clip-worthy moment every session |
| 3 | Progression and economy | Balance sheet; sink ratio; first ten prices; level distribution (where players stall); D7; wallet balance trend | No sinks or runaway inflation; > 50% of actives parked at one level `[house]`; D7 far below median | Curve modelled, sink ratio 0.95–1.05, rebirth ratio ×1.2–1.5, D7 near median | Economy events logged per currency, balance stable, D7 ≥ P90, 4+ weeks of content ahead of the top 10% |
| 4 | Retention and LiveOps | Days since last update; fixed update day; events; return reasons; D30, D8–28 play days; co-play days | No update in 30+ days; no reason to return; punishing streaks | Monthly updates, capped offline income or timers, dated events | Weekly day kept 4 weeks running, Experience Events used, D8–28 play days ≥ P90, friend bonus and invites live |
| 5 | Monetisation | Product list; offer timing log; conversion, ARPPU, ARPDAU vs benchmark; odds UI; receipt path | Offer in first 10 min, fake discount, missing odds, or client-granted purchase (cap 1); or nothing to buy | House default set live, offer gate compliant, receipts idempotent, conversion near median | Conversion and ARPPU ≥ P90, cheap repeatables drive spend days, offer funnel logged, free alternative beside every paid shortcut |
| 6 | UI/UX | Phone-size screenshots; HUD element count; touch target size; safe insets; text size; gamepad pass | Desktop-only layout; overlaps CoreGui; > 8 persistent HUD elements `[house]`; stock unstyled UI | Usable on phone landscape, insets respected, one visual style | Phone, tablet, desktop and gamepad tested; preferences honoured; distinct identity; every action ≤ 2 taps |
| 7 | Art, cohesion, house rules | House-rule scan output; share of visible parts that are Blender MeshParts; walk-through test; style bible; lighting | Scan lists visible primitives, marketplace or generated assets, or meshes without collision (cap 1) | Scan clean; mixed texel density or default lighting | Scan clean, one style bible, shared trim sheets, lighting preset, any camera angle is thumbnail-ready |
| 8 | Performance | FPS by device class; crash rate; out-of-memory exits; memory %; join time; server frame rate; draw calls and triangles | Crash rate > 3%, < 30 FPS on low-end Android, or server below 60 under load | ≥ 30 FPS low-end, crash rate under 2–3%, server memory within guideline | Gate 4 passes in full, alerts set, flat over a 1-hour soak, no regression by place version |
| 9 | Security and data | Remote list and handlers; `ProcessReceipt`; session locking; `require(<number>)` and `loadstring` hits; data-loss reports | Client-trusted values, grants from client signals, no session lock, unknown asset-id requires (cap 1) | Server-authoritative, most remotes guarded, ProfileStore, receipts idempotent | Gate 2 passes in full, CI-only publish, DataStore quota alerts, migration tested on real profile copies |
| 10 | Discovery and growth | PTR vs benchmark; active thumbnails; title and description; exposure banner; like ratio; acquisition mix; share links; community | Default thumbnail, exposure banner, giveaway lead, mismatched metadata, or like ratio < 70% `[house]` | 2–5 honest custom thumbnails, PTR near median, like ratio ≥ 85% | PTR ≥ P90 with bounce no worse, 3–5 distinct hooks plus video, events, share link per channel, localisation on |

Report the ten scores, the evidence line for each, and the total out of 50. The total is for tracking re-audits; the triage tree, not the total, picks what to fix.

## 4. Triage tree: what to fix first

Walk top to bottom; stop at the first row that is true and make it the sprint goal. Rows T0–T2 pre-empt everything.

| Step | If the numbers say | Likely cause | First fix | Open |
|---|---|---|---|---|
| T0 | Data loss, ungranted purchases, dupes, a policy violation, or a moderation or reduced-exposure banner | Blocker | Fix before any other work; file the "Discovery Content Quality" support ticket if the banner is wrong | data-and-purchases.md, networking-and-security.md, monetization-and-policy.md |
| T1 | Home Recommendations impressions near zero | Not eligible: default thumbnail, "Exclude from recommendations" on, not public, questionnaire missing, or still in the 16+ trial (250 engaged age-checked plays not reached) | Clear the eligibility item; bring 16+ players first | analytics-and-discovery.md, growth-and-marketing.md |
| T2 | Crash rate above 2–3%, out-of-memory exits rising, low-end FPS < 30, or a regression on the newest place version | Performance; it depresses every metric below | Performance sprint; compare by platform and place version | performance.md |
| T3 | Bounce < 60 s high | Slow join, crash, or the tile promises something the first minute does not show | Join-time and thumbnail-honesty fix | performance.md §loading, analytics-and-discovery.md §thumbnails |
| T3b | Bounce 61–180 s high, or the first-session curve has a cliff at one minute mark | FTUE: no reward, confusion, wall of UI | Fix the funnel step with the largest drop | liveops-quests-retention.md §onboarding, core-loop-tuning.md |
| T4 | D1 below benchmark median | Core loop, FTUE or performance `[official]` | Loop and first-10-minutes pass; not new content | core-loop-tuning.md, design-foundations.md, genres/<genre>.md |
| T4b | D1 fine, session time or D1 playtime low | No mid-session goal or depth | Goal ladder, meso loop, co-play | economy-and-progression.md, game-craft.md |
| T5 | D1 fine, D7 or D2–7 play days low | Progression wall or empty mid-game `[official]` | Find the stall level; re-curve | economy-and-progression.md |
| T5b | D7 fine, D30 or D8–28 play days low | No endgame, social system or update cadence `[official]` | Weekly day, events, collections, trading or guilds | liveops-quests-retention.md |
| T6 | Retention at or above median, PTR below median | Icon, thumbnails, title | 3–5 distinct honest thumbnails, video, title pass | analytics-and-discovery.md, market-scan-2026-11.md |
| T7 | Retention fine, conversion low | First purchase too hard or too expensive | Starter pack after first win, cheap repeatables | monetization-and-policy.md |
| T7b | Conversion fine, ARPPU or spend days low | Shallow price ladder, nothing to rebuy | Ladder depth, consumables, season pass | monetization-and-policy.md, economy-and-progression.md |
| T8 | Everything at or above median, DAU flat | Reach | Events, creators, ads, localisation | growth-and-marketing.md |

Notes for reading the numbers:

- T6 is cheap (hours) and may run in parallel with any step, provided the tile shows the real first minute. A PTR gain that raises bounce is a net loss: Recommended For You scores post-click behaviour, and Roblox widened the window to 28 days in June 2026 to stop rewarding attention-grabbing tiles `[official]`.
- A retention dip after a traffic spike is normal, and PTR dips while impressions rise `[official]`. Impressions also move with seasonality (Saturday peak), algorithm changes and competitors `[official]`; check those before blaming the last update.
- "D7" in the dashboard is the 8th day after first play `[official]`. D7 and D30 for the latest cohorts are empty until the days have passed.
- Benchmarks do not affect ranking and the benchmark set changes as the game grows `[official]`.
- Under about 300 new users per reading `[house]`, treat step rates as directional only.
- `[community]` DevForum threads on stalled games repeat three things: add funnel events before changing anything, onboarding fixes moved session time, and inflated first-session rewards can raise D1 without moving D7. Anecdotes, not data.

No numbers yet (under 10 DAU, or no dashboard access):

1. Score from the MCP runbook and a five-stranger playtest (`templates/playtest-plan.md`); every metric-backed dimension caps at 3.
2. Ship instrumentation first: onboarding funnel, shop and offer funnels, economy events (`templates/analytics-event-plan.md`).
3. Get about 300 first sessions `[house]`: 16+ community, share links per channel, friends. A small capped Plays campaign is an acceptable measurement purchase (ad-acquired users never enter Recommended For You ranking `[official]`), but not while the visible like ratio is under 85%.
4. Until dashboard benchmarks unlock at 100 DAU, compare against the §2 fallback rows and say so in the report.

## 5. Studio MCP audit runbook (read-only first) `[VS]`

Phase A, edit mode, nothing written:

1. `list_roblox_studios` → pick the `studio_id`; `get_studio_state` (must be Edit, not playing). Confirm with the user that this is a copy or that no one else is mid-edit.
2. MCP Permissions: "Look at your game" on; "Save & load data", "Edit your game", "Money & monetization" and "Publish & manage assets" off for the audit.
3. `open_cloud_invoke` GET `/cloud/v2/universes/{id}` and the analytics queries in §1 (optional; skip when screenshots were supplied).
4. `search_game_tree` at depth 2 on Workspace, ReplicatedStorage, ReplicatedFirst, ServerScriptService, ServerStorage, StarterGui, StarterPlayer, Lighting, SoundService. Note structure, naming, where scripts live.
5. `inspect_instance` on Workspace (streaming settings, signal behaviour), Lighting, StarterGui screens (insets, reset-on-spawn), StarterPlayer.
6. `execute_luau` (Edit) census below; then the house-rule scan in checklists.md Gate 4.
7. `script_grep`, one pattern per call (50-match cap): `wait(`, `spawn(`, `delay(`, `tick()`, `LoadAnimation`, `BodyVelocity`, `FindPartOnRay`, `InvokeClient`, `loadstring`, `getfenv`, `require(` (then read the hits for numeric asset ids: a backdoor risk), `OnServerEvent`, `OnServerInvoke`, `ProcessReceipt`, `PromptProductPurchaseFinished`, `SetAsync`, `UpdateAsync`, `BindToClose`, `UserOwnsGamePassAsync`, `PolicyService`, `FilterStringAsync`, `AnalyticsService`, `ConfigService`, `HttpService`.
8. `script_read` in this order: the receipt handler, data load and save, the five largest remote handlers, the offer or shop controller, the tutorial or onboarding script, the main client entry.

Phase B, play mode (changes are discarded on stop):

9. `start_stop_play`; time join-to-playable; `get_console_output` for errors and warnings in the first 60 s.
10. Walk the FTUE with `character_navigation`, `user_mouse_input`, `user_keyboard_input` (or the `playtest` subagent). `screen_capture` at 0 s, 30 s, 2 min, 5 min, in the shop, and at the first offer. Log seconds to first reward, first upgrade, first prompt of any kind.
11. Repeat one pass with device emulation set to a small phone (the MCP `skill` tool documents device simulation); capture the HUD and the shop.
12. `execute_luau` (Server, then Client) to read `Stats` memory and instance counts after 5 minutes; compare with minute 0 for leaks.
13. `start_stop_play` to stop; `get_studio_state` to confirm Edit; confirm nothing was saved or published.

Never during an audit: `multi_edit`, publishing, DataStore or MemoryStore calls, `generate_*`, `insert_asset`, `search_asset`. The same rules as engineering-architecture.md §AI agents apply.

```lua
--!strict
-- Unexecuted sketch. Run with execute_luau, datamodel_type = "Edit". Read-only census.
local roots: { Instance } = {
	workspace,
	game:GetService("ReplicatedStorage"),
	game:GetService("ReplicatedFirst"),
	game:GetService("ServerScriptService"),
	game:GetService("ServerStorage"),
	game:GetService("StarterGui"),
	game:GetService("StarterPlayer"),
}
local counts: { [string]: number } = {}
local meshIds: { [string]: boolean } = {}
local function bump(key: string)
	counts[key] = (counts[key] or 0) + 1
end

local seen = 0
for _, root in roots do
	for _, d in root:GetDescendants() do
		seen += 1
		if seen % 2000 == 0 then
			task.wait() -- keep Studio responsive
		end
		bump("class:" .. d.ClassName)
		if d:IsA("LuaSourceContainer") then
			bump("scripts@" .. root.Name)
		elseif d:IsA("BasePart") and not d:IsA("Terrain") then
			if not d.Anchored then
				bump("flag:unanchored")
			end
			if d:IsA("MeshPart") then
				meshIds[d.MeshId] = true
			elseif d.Transparency < 1 then
				bump("flag:visiblePrimitive") -- house rule 1
			end
		end
	end
end

local unique = 0
for _ in meshIds do
	unique += 1
end
local lines = { `instances={seen} uniqueMeshIds={unique}` }
for key, n in counts do
	if n >= 25 or string.sub(key, 1, 5) == "flag:" or string.sub(key, 1, 8) == "scripts@" then
		table.insert(lines, `{key}={n}`)
	end
end
table.sort(lines)
print(table.concat(lines, "\n"))
```

Read the output for: scripts under Workspace (behaviour inside models), remote count (each one needs a guard), `flag:visiblePrimitive`, unanchored count, MeshPart count versus unique MeshIds (instancing), ScreenGui and ImageLabel counts (UI weight), ParticleEmitter and PointLight counts.

## 6. Prioritisation

`Priority = Impact × Confidence ÷ Effort` `[house]`

| Factor | Scale |
|---|---|
| Impact | 5 moves a "most important" Recommended For You signal (PTR, bounce, play days, playtime) or removes a blocker; 4 moves D1 or D7; 3 moves conversion, ARPPU or co-play; 2 moves a secondary metric; 1 cosmetic |
| Confidence | 1.0 measured in this game (funnel drop, profiler capture, repro); 0.7 seen in a stranger playtest or matches an official diagnosis rule; 0.4 genre norm or community heuristic; 0.2 hunch |
| Effort | Dev-days including art, test and rollout; minimum 0.5 |

Tie-breaks: higher in the funnel wins; reversible (a Config flag) beats irreversible; anything that touches the save schema counts double effort. T0 blockers and house-rule violations skip the queue.

Quick-wins sprint or rebuild `[house]`:

| Choose | When |
|---|---|
| Quick-wins sprint (2 weeks, then re-measure) | Core loop ≥ 3, strangers replay unprompted or D1 ≥ half the benchmark median, and most top-10 actions cost ≤ 2 days |
| Rebuild the loop inside the same universe | Core loop ≤ 2, or two sprints on FTUE and loop did not move D1; or security/data ≤ 1 so every fix costs 3× ; or more than half the visible world fails house rule 1 |
| Park or kill | After one FTUE sprint and one loop sprint, five strangers still do not replay and "would you start this today?" is no |

A rebuild keeps the universe, the DataStore key pattern, purchases, badges, favourites and the group. Recommended For You uses a moving window and re-tests daily, so a weak past is not a permanent penalty `[official]`. Players keep everything they paid for.

## 7. Safe-change protocol for live games

1. **Baseline.** Record 14 days (minimum 7) of the target metric, the live place version number, and a Configs export. Never compare PTR across 12 Oct 2026.
2. **Back up.** Add a Version History note to the live version; keep a local `.rbxl` and a git tag. Restoring a version creates a new version and does not publish it; publish and restart servers to make it live `[official]`.
3. **Stage.** Build and test in a separate test universe. No production DataStore access from Studio or the MCP.
4. **Flag.** Ship new behaviour dark behind a Configs key whose code default is the old behaviour. Configs stage first, then "Publish now" (about 15 s–1 min) or "Publish over 15 min"; History → Restore reverts `[official][VS]`.
5. **Experiment or stage the rollout.** With enough DAU, run an Experiment: 50/50, 14–60 days, percent rollout; early-harm metrics (playtime, payer conversion, ARPU) refresh every 5 minutes for the first 24 hours `[official]`. Under about 1,000 DAU, do before/after on daily cohorts and change one thing per week.
6. **Data.** Additive schema changes only; bump the schema version; migrate before `Reconcile`; never change the key pattern; never wipe. After a publish, old and new servers run side by side until restart `[official]`, so the new schema must be readable by old code, or restart outdated servers at once. Test the migration on copies of real profiles (oldest, largest, richest) in the test universe. DataStore keeps prior versions for 30 days after an overwrite `[official]`: that is the recovery window.
7. **Economy and purchases.** Never remove or weaken something a player paid for. Grandfather owners, compensate when a paid item changes, announce nerfs before they land.
8. **Release.** Publish from CI in the audience's off-peak hours. Creator Hub → Configurations → Server management → Restart Servers with "Restart only servers with outdated versions" and a 5–10 minute delay (1–60 allowed); listen to `DataModel.ServerRestartScheduled` to show a countdown and save `[official][VS]`.
9. **Watch for 2 hours.** Performance dashboard broken down by Place Version; alerts on client crash rate, out-of-memory exits and server frame rate sent to a webhook (20 alerts per experience) `[official]`; console errors; purchase success.
10. **Rollback triggers written before shipping.** For example crash rate +2 points, early-harm flag red, purchase failures. Roll back by flipping the Config first, then restoring the version, publishing and restarting.
11. **Announce.** Update announcement (60 characters, at most one per 3 days) `[official]`, an Experience Event for anything dated, an in-game changelog panel, a group post. Details in growth-and-marketing.md.
12. **Metadata is a change too.** Swap thumbnails with an update, keep 2–5 active for 7+ days, do not rename the game often (it breaks search for the old name `[official]`), genre changes once per 3 months.
13. **Wait before judging.** PTR and bounce 24–72 h; D1 two days; D7 eight days; impressions lag signals by days.

## 8. Routing: finding → reference

| Finding | Open |
|---|---|
| Slow or confusing first minutes | `references/liveops-quests-retention.md` §onboarding, `references/design-foundations.md` §7, `references/core-loop-tuning.md` |
| Loop is dull, no decision, short sessions | `references/core-loop-tuning.md`, `references/game-craft.md`, `references/genres/<genre>.md`, `references/genre-playbooks.md` |
| Wall, inflation, dead currency | `references/economy-and-progression.md`, `templates/economy-balance-sheet.md` |
| No reason to return, no cadence | `references/liveops-quests-retention.md` |
| Low conversion, invasive or non-compliant offers | `references/monetization-and-policy.md`, `templates/monetization-product-plan.md` |
| Cluttered HUD, weak mobile layout, stock UI | `references/ui-design-figma.md`, `references/ui-input-crossplatform.md` |
| Primitives, marketplace assets, mixed style, no collision | `references/art-pipeline-blender.md`, checklists.md house-rule scan |
| FPS, memory, crashes, join time | `references/performance.md` |
| Client trust, unguarded remotes, backdoors | `references/networking-and-security.md` |
| Data loss, unsafe receipts, migration | `references/data-and-purchases.md` |
| Spaghetti scripts, no toolchain | `references/engineering-architecture.md`, `references/architecture-patterns-luau.md`, `references/ai-toolchain-skills.md` |
| Low PTR, weak tile or title, no events | `references/analytics-and-discovery.md`, `references/market-scan-2026-11.md` |
| Good metrics, no reach | `references/growth-and-marketing.md` |
| Missing events, no funnels | `references/analytics-and-discovery.md`, `templates/analytics-event-plan.md` |

## Review gate

- [ ] Intake answered; baseline window and place version recorded.
- [ ] All ten dimensions scored with an evidence line each; caps applied (no numbers → 3; house-rule or trust hit → 1).
- [ ] Benchmarks named with source and date; own dashboard benchmark used where it exists.
- [ ] Triage step stated (T0–T8) with the numbers that selected it.
- [ ] Every action has Impact, Confidence, Effort, a metric and an owner; top 10 ranked.
- [ ] Quick-wins, rebuild or park decision stated with the rule that triggered it.
- [ ] Safe-change plan: backup, flag, rollout, data check, rollback triggers, announcement.
- [ ] The audit itself wrote nothing: no edits, publishes or DataStore calls.
- [ ] `[VS]` facts re-checked at create.roblox.com/docs or flagged as unchecked.

## Sources

Accessed 2026-11-10. Roblox creator docs read from the `Roblox/creator-docs` GitHub mirror (commit dated 2026-11-07).

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery-faq.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/retention.md, engagement.md, monetization.md, acquisition.md, performance.md, alerts.md, analytics-dashboard.md, insights.md, feedback.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud/guides/analytics/index.md, metrics.md, benchmarks.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/studio/mcp.md, mcp-open-cloud.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/update-games.md, version-history.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/configs.md, experiments.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud-services/data-stores/versioning-listing-and-caching.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/publish-games-and-places.md, kids-and-select.md, thumbnails.md (read)
- https://gamedevreports.substack.com/p/gameanalytics-key-roblox-and-roblox (search summary; GameAnalytics medians)
- https://www.gameanalytics.com/reports/2025-roblox-report (search summary)
- https://about.roblox.com/newsroom/2026/06/optimizing-discovery-great-games-reach-millions-players-roblox (search summary)
- https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575 (search summary)
- https://devforum.roblox.com/t/struggling-to-increase-ccu-for-new-game/3353917, /t/poor-stats-for-my-new-game-across-the-board/3413365, /t/help-with-improving-player-session-time/3554677, /t/looking-for-advice-on-improving-retention-for-a-wave-based-zombie-shooter/3307981 (search summaries)
- https://devforum.roblox.com/t/introducing-migrate-to-latest-update/535590, /t/improvements-to-updating-experiences/2600703 (search summaries)
- https://rowatcher.com/news/d1-vs-d7-why-fixing-the-wrong-retention-metric-kills-games (search summary; opinion)
- Vault: `references/market-scan-2026-11.md`, `references/knowledge-base.md` §3.9, §3.10, §5.1 (read)
