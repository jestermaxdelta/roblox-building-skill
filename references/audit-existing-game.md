# Level-up mode: auditing and improving an existing game

Method for pointing the skill at a game that already exists (prototype, soft-launched, live, plateaued or declining) and producing a ranked, evidence-based improvement plan, then executing it without breaking saves or the live audience. Open it whenever the user says "improve", "audit", "optimise", "why is my game not growing" or hands over a place file, a Rojo repo or analytics screenshots. Output goes into `templates/game-audit-report.md`; `references/checklists.md` Gate A is the short form.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner (first game, Studio-only, no analytics yet) | 1. Time the first five minutes with a stopwatch (runbook step 10; the log table is in the report template). 2. Run the house-rule scan and fix blockers. 3. Add the onboarding funnel events. Then take the **top 3 actions** only | The 50-point total, experiments, percentiles, cost-per-play maths |
| Intermediate (live game, some players, reads the dashboard) | Full scorecard with sub-checks, triage step, top 10 actions, the safe-change protocol on every release | Building custom analytics; multi-variant experiments under 1,000 DAU |
| Expert (team, CI, 1,000+ DAU) | Pull metrics by API, cohort and source splits, the CCU model, experiment design with sample sizes, second-opinion review on every high-stakes call, deliverable scoring | Nothing; but do not skip T0–T2 because the game is "mature" |

Terms used here: **DAU** daily active users; **CCU** concurrent users; **PTR** play-through rate (plays ÷ impressions on Home); **bounce** a first play that ends within 60 s or 61–180 s; **D1/D7/D30** share of new players who return 1, 7 or 30 days after first play; **FTUE** first-time user experience; **ARPDAU** revenue per daily active user; **P50/P90** the median and top-decile values of the benchmark group; **cohort** players grouped by first-play date.

Contents: 1 Intake (and the numbers-only first pass) · 2 Benchmarks · 3 Scorecard and sub-checks · 4 Triage tree · 5 Studio MCP runbook · 6 Prioritisation · 7 Evidence grades and deliverable quality · 8 Second opinion · 9 Safe-change protocol · 10 Routing · Review gate · Sources.

Shortest route. The owner gave a few numbers and no access: read only "Numbers-only first pass" in §1, the four rules in §2 and the triage table in §4 (about 60 lines), then reply. Open §3 and §5–9 once there is a place, a repo or a dashboard to inspect; §10 is a lookup table.

## How the audit adapts to the developer

Rate the owner per domain from evidence in the conversation and the project, never by asking "what level are you" (same rule as SKILL.md; signals in `references/learning-paths.md`). People are often strong in one domain and new in another, so the report mixes columns: an owner who quotes D1 and conversion but works Studio-only with no Rojo gets the intermediate treatment for numbers and the beginner treatment for the change method.

| Domain | Beginner signals | Intermediate signals | Expert signals |
|---|---|---|---|
| Metrics and platform | Talks in visits and likes; has not opened Creator Analytics | Quotes D1, session time, conversion; reads the dashboard | Cohort and source splits, experiments, API pulls |
| Code and tooling | Studio-only, scripts inside models, raw DataStore calls | Modules, ProfileStore or similar, Configs, some funnels | Rojo, CI publish, tests, typed Luau |
| Art | Toolbox models and Parts | Some own meshes, mixed styles | Blender pipeline with kits and a style bible |
| Design and economy | Features listed, no loop timings or price curve | Loop and curve described, balance by feel | Balance sheet, sink ratio, modelled curves |
| Time | Under about 10 h a week, solo | 10–30 h a week or a small team | Full-time team |

The audit work is identical; the report changes. Pick each row of the table below from the matching domain.

| | Beginner | Intermediate | Expert |
|---|---|---|---|
| What they receive | Blockers, then the top 3 actions, each with why it matters, exact steps, and how to tell it worked | Scorecard, triage step, top 10 ranked actions, 2-week and 6-week plan | Everything, plus the full ranked finding list, dismissed findings, measurements, experiment plans and the CCU model |
| Numbers shown | Stopwatch times and one metric (D1 or session time) | Each KPI against P50 and P90 | Cohort tables, source splits, confidence intervals, minimum detectable effect |
| Language | Every term defined once; no acronyms left unexplained | Standard KPI vocabulary | Terse; references by path and section |
| Change method | One change per week, Config flags explained step by step | Safe-change protocol | Experiments, staged rollouts, kill switches, automated alerts |
| Decision support | Auditor recommends; one alternative | Lower-risk and bold options | Second-opinion review (§8) on ship, rebuild, pricing and migration calls |

Never hide a T0 blocker to keep a report short, and always list house-rule debt with its migration track (§6), whatever the level.

## Operating rules

- Evidence before opinion. Every finding cites a number, a screenshot, a script path and line, or a timed observation. "Needs polish" is not a finding.
- Read-only first. No edit, publish, config change or DataStore call until the report is accepted.
- Fix in funnel order (reach → stability → first session → D1 → D7 → D30 → monetisation → paid growth). A fix lower in the funnel is wasted while a higher step leaks. Roblox's own guidance: if retention is low, fix core gameplay first; improve monetisation once retention is strong `[official]`.
- House-rule violations in an existing game are findings with a migration plan ranked by visibility, on their own track with a fixed share of weekly hours (§6). They do not block other fixes. Only two are blockers: walk-through geometry on the main path, and invasive or non-compliant offers. Work delivered during the level-up never adds a new violation.
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

Data unlock thresholds `[official][VS]` (detail in analytics-and-discovery.md §Analytics): dashboards from 10 DAU and 10 play hours for 7 days in a row; benchmarks, Performance charts, alerts and insights from 100 DAU; analytics reports from 1,000 DAU.

Pulling numbers without screenshots `[official][VS]`: Open Cloud **Analytics Query API** (`POST https://apis.roblox.com/analytics-query-api/v1/universes/{universeId}/metrics`, body `metric`, `granularity`, `startTime`, `endTime`, optional `breakdown`, `filter`) and the experimental **Benchmarks API** (`POST https://apis.roblox.com/analytics-benchmark/v1/universes/{universeId}/benchmarks`, percentiles 10/50/90, types genre / similarity / top experiences). Scope `universe.analytics:read`; through the Studio MCP it sits in the "Look at your game" permission group and is called with `open_cloud_invoke`. Standard metrics keep up to 4 years, performance metrics 28 days. Useful metric names: `ForwardD1Retention`, `ForwardD7Retention`, `ForwardD30Retention`, `AverageSessionLengthMinutes`, `AveragePlayTimeMinutesPerDAU`, `DailyActiveUsers`, `PayingUsersCVR`, `AverageRevenuePerPayingUser`, `AverageRevenuePerUser`, `RFYPlayThroughRate`, `RFYDuration0To60`, `RFYDuration61To180`, `RFYD2To7PlayDays`, `RFYD8To28PlayDays`, `ClientCrashRate15m`, `OomUnexpectedExits`, `ClientFpsAvg`, `ClientMemoryUsagePercentageAvg`, `ServerFrameRateAvg`, `ThumbnailQualifiedPTR`, `FunnelStepChurnRate`.

### Numbers-only first pass (no place access yet)

When the owner gives a few numbers and a description but no place file, repo or Studio access, do not open the full template and do not answer with a wall of "no data". Reply once, in under about 400 words, in this shape:

1. **What the numbers say** (2–3 sentences): each number placed against the benchmark rule in §2, with the benchmark named.
2. **Triage step** (T0–T8) and the one sentence of evidence that selects it; say what was assumed for anything missing.
3. **Top 3 actions**, each with the reason, the first concrete step, the effort in hours and in weeks at the owner's weekly budget, and the number that will show it worked. If the description reveals house-rule debt, say it goes on the 20–30% track and name the first surface (spawn view).
4. **At most five asks**, the ones that would change the plan: usually (a) first-play bounce under 60 s and 61–180 s, (b) average session time and the first-session curve at 5 minutes, (c) crash rate on the worst platform, (d) read access to the place or repo, (e) the one thing the owner most wants to move.
5. **What comes next:** the full scored report after access, with its date.

No scorecard, no 50-point total and no day-by-day plan in this reply: scores need inspection, and a 10-hours-a-week owner plans in weeks. Example of the action format: "Add the seven onboarding funnel events (about 3 hours, this week): without them the 9% D1 cannot be traced to a step; done when the funnel chart shows all steps for 200+ new players."

## 2. Benchmarks to score against `[VS]`

The single benchmark table, with the sample and source behind every row and the weak rows marked, is `references/analytics-and-discovery.md` §"Benchmarks: one table". Use it like this:

1. **The dashboard percentile always wins.** If the owner can read Creator Analytics (100+ DAU), score against the game's own P50–P90 (or P10–P50 where lower is better) and name the benchmark type (similar players, genre, all).
2. **No dashboard benchmark:** the row that drives triage for retention is the large-title distribution (D1 P25 8.4%, median 10.3%, P75 12.9%, P90 15.9%; D7 median 1.6%; D30 median 0.5%). D1 under 8.4% is "below" and fires T4. D1 from 8.4% to 12.9% is "near median": T4 does not fire on D1 alone; continue down the tree and keep D1 as a secondary target. D1 above 12.9% is "above".
3. **Cross-check with the session-length row,** never instead of step 2: a D1 below the median for the game's own session bucket means players enjoy a session but have no reason to return (look at T5 causes before the first minutes).
4. **Never triage from** the unsourced genre ranges, the docs' illustrative dashboard example, or mobile-industry rules of thumb. They are listed in the table only so a quoted figure can be recognised and discounted.

Worked reading: a tycoon with D1 9% and no dashboard benchmark is in the "near median" band (lower half), not "far below", whatever a genre tracker says about tycoons at 20–28%. Bounce, session time and crash rate decide the triage step; D1 becomes the secondary target.

## 3. Scorecard: 10 dimensions, 0–5

Scale: 0 absent or broken · 1 present but fails its gate · 2 works with major gaps, or metric below benchmark median · 3 gate passed, metric near median · 4 above median, minor gaps · 5 top decile (P90, or P10 where lower is better) and the gate passes in full.
Caps: no live numbers → the dimension scores at most 3. Any house-rule, policy, data-loss or client-trust hit → at most 1 for that dimension. A cap describes the state of the game; it does not set the order of work (§4 and §6 do).

| # | Dimension | Observe | 1 looks like | 3 looks like | 5 looks like |
|---|---|---|---|---|---|
| 1 | First session (FTUE) | Tutorial rubric from a phone recording of a fresh account (tutorial-and-onboarding.md §13, 0–20); join-to-playable seconds on a 3 GB phone; seconds to first reward and first upgrade; bounce < 60 s and 61–180 s; first-session retention curve; onboarding funnel | Rubric under 10, or a zero in its rows 1, 5 or 8 (menu or scene before the verb, unseen cue, a step that can stick); first reward > 2 min; prompt or offer in the first minutes; no funnel events | Rubric 16+; playable < 15 s after join, first reward < 60 s for 85% of new players, no funnel step in the first 3 minutes loses more than 25%, bounce near median | Rubric 19+; first verb ≤ 15 s, first reward ≤ 30 s, first upgrade < 2 min, goal ladder on screen, no step loses more than 15%, median (not mean) first session 10+ min, bounce in the best decile |
| 2 | Core loop | Loop scorecard from a recording of fresh testers or the dashboard (core-loop-tuning.md §4, 0–10); seconds per loop; the one verb; session time; do strangers start a second loop unprompted | A number ticks on a menu; no decision; loop does not close; session < 5 min | Loop closes in 10–30 s with a visible goal and next purchase; scorecard 7/10; session near median | Scorecard 9+; session ≥ P90 or 19+ min; D1 playtime ≥ P90; clip-worthy moment every session |
| 3 | Progression and economy | Balance sheet; sink ratio; first ten prices; level distribution (where players stall); D7; wallet balance trend | No sinks or runaway inflation; > 50% of actives parked at one level `[house]`; D7 far below median | Curve modelled, sink ratio 0.95–1.05, rebirth ratio ×1.2–1.5, D7 near median | Economy events logged per currency, balance stable, D7 ≥ P90, 4+ weeks of content ahead of the top 10% |
| 4 | Retention and LiveOps | Days since last update; fixed update day; events; return reasons; D30, D8–28 play days; co-play days | No update in 30+ days; no reason to return; punishing streaks | Monthly updates, capped offline income or timers, dated events | Weekly day kept 4 weeks running, Experience Events used, D8–28 play days ≥ P90, friend bonus and invites live |
| 5 | Monetisation | Product list; offer timing log; conversion, ARPPU, ARPDAU vs benchmark; odds UI; receipt path | Offer in first 10 min, fake discount, missing odds, or client-granted purchase (cap 1); or nothing to buy | House default set live, offer gate compliant, receipts idempotent, conversion near median | Conversion and ARPPU ≥ P90, cheap repeatables drive spend days, offer funnel logged, free alternative beside every paid shortcut |
| 6 | UI/UX | UI critique rubric per screen on phone-size screenshots over gameplay (ui-design-figma.md §9, 0–10; tells in its §8); HUD, shop and inventory at least; gamepad pass | Rubric under 6 on the HUD: desktop-only layout, overlaps CoreGui, > 8 persistent HUD elements `[house]`, stock unstyled UI | Rubric 6–7.5 on every core screen: usable on phone landscape, insets respected, one visual style | Rubric 8+ on every screen, scored by someone who did not build it; phone, tablet, desktop and gamepad tested; preferences honoured; every action ≤ 2 taps |
| 7 | Art, cohesion, house rules | House-rule scan output; walk-through test; whole-game art review (art-direction-and-quality-bar.md §8: twelve phone captures, four tests, 0–10 per discipline, game score = lowest discipline); defaults scan (its §2) | Scan lists visible primitives, marketplace or generated assets, or meshes without collision (cap 1); or any discipline at 0–2 | Scan clean; lowest discipline 5–6 (consistent, forgettable); score 2 at 3–4, score 4 at 7 | Scan clean; no discipline under 8; one-screenshot test passed with strangers (the "competitive" tier in its §7) |
| 8 | Performance | FPS by device class; crash rate; out-of-memory exits; memory %; join time; server frame rate; draw calls and triangles | Crash rate > 3%, < 30 FPS on low-end Android, or server below 60 under load | ≥ 30 FPS low-end, crash rate under 2–3%, server memory within guideline | Gate 4 passes in full, alerts set, flat over a 1-hour soak, no regression by place version |
| 9 | Security and data | Remote list and handlers; `ProcessReceipt`; session locking; `require(<number>)` and `loadstring` hits; data-loss reports | Client-trusted values, grants from client signals, no session lock, unknown asset-id requires (cap 1) | Server-authoritative, most remotes guarded, ProfileStore, receipts idempotent | Gate 2 passes in full, CI-only publish, DataStore quota alerts, migration tested on real profile copies |
| 10 | Discovery and growth | PTR vs benchmark; active thumbnails and icon against the store-page gates and rubric (icons-thumbnails-and-store-page.md §15); title and description; exposure banner; like ratio; acquisition mix; share links; community | Default thumbnail, exposure banner, giveaway lead, mismatched metadata, a tile that fails a gate (untruthful, policy, generated), or like ratio < 70% `[house]` | 2–5 custom thumbnails that pass the three gates, PTR near median, like ratio ≥ 85% | PTR ≥ P90 with bounce no worse, 3–5 distinct hooks at 8.5+ on the rubric plus video, events, share link per channel, localisation on |

The rubrics named in rows 1, 2, 6, 7 and 10 are defined in their guides; score with them, quote the rubric number as the evidence line, and do not restate their criteria in the report. Report the ten scores, the evidence line for each, and the total out of 50. The total is for tracking re-audits; the triage tree, not the total, picks what to fix. The 25% and 15% step-loss bars and the 85%-reach-first-reward bar are soft-launch rules of thumb `[lihfolk]`, not Roblox targets.

### Sub-checks (six yes/no items each; they adjust the parent dimension, they are not extra dimensions)

Rule: fewer than 3 passes caps the parent dimension at 2; 3–4 passes caps it at 4; 5–6 leaves it alone. An item marked (blocker) fails straight to T0.

| Sub-check | Parent | Items (pass or fail, on a phone) | Open |
|---|---|---|---|
| 2a Game feel and audio | Core loop | Every core action shows a visible response in the same frame or the next (no waiting on the server for the cosmetic part) · every reward has a sound and a visual, scaled to its size · a missed input is forgiven (buffered press, ledge grace) where the genre needs it · sounds route through SoundGroups with Master, Music and SFX sliders that persist · effects scale down on low graphics levels while gameplay telegraphs stay visible · no stretch over about 10 s in the loop with nothing to do or watch | `references/vfx-and-juice.md` (rubric §16), `references/ui-motion-and-feedback.md`, `references/audio-sfx-music.md` (rubric §16), `references/animation-and-rigs.md`, `references/game-craft.md` §1 |
| 6a Accessibility and quality of life | UI/UX | Settings open from the first second, including during the tutorial · text follows `PreferredTextSize` and stays readable at the largest size · camera shake, flashes and motion can be reduced and follow `ReducedMotionEnabled` · colour is never the only carrier of meaning (rarity, team, danger also use shape, icon or text) · tutorial and loading screen can be skipped and the skip costs nothing · prompts show the correct glyph for touch, keyboard and gamepad, and destructive actions ask once | `references/accessibility-and-player-qol.md`, `references/ui-input-crossplatform.md` |
| 4a Community and safety | Retention and LiveOps | All player-written text is filtered on the server before anyone sees it (blocker) · no URL, invite code, handle or email appears in-game (blocker) · players are told how to use the platform report tool, and any game-rule report flow is rate-limited and category-based · bans use `Players:BanAsync` with escalating consequences and an appeal route, and moderator powers are checked on the server · each social feature has a stated grief control (plot ownership, trade confirmation, mute and block respected) · server size fits current CCU so new players land with others, and the loop works with one to three players | `references/community-moderation-safety.md`, `references/liveops-quests-retention.md` §social design |

## 4. Triage tree: what to fix first

Walk top to bottom; stop at the first row that is true and make it the sprint goal. Rows T0–T2 pre-empt everything.

| Step | If the numbers say | Likely cause | First fix | Open |
|---|---|---|---|---|
| T0 | Data loss, ungranted purchases, dupes, a policy violation, a moderation or reduced-exposure banner, walk-through geometry on the main path, or an invasive or non-compliant offer | Blocker | Fix before any other work; file the "Discovery Content Quality" support ticket if the banner is wrong | data-and-purchases.md, networking-and-security.md, monetization-and-policy.md |
| T1 | Home Recommendations impressions near zero | Not eligible: default thumbnail, "Exclude from recommendations" on, not public, questionnaire missing, or still in the 16+ trial (250 engaged age-checked plays not reached) | Clear the eligibility item; bring 16+ players first | analytics-and-discovery.md, growth-and-marketing.md |
| T2 | Crash rate above 2–3%, out-of-memory exits rising, low-end FPS < 30, or a regression on the newest place version | Performance; it depresses every metric below | Performance sprint; compare by platform and place version | performance.md |
| T3 | Bounce < 60 s high | Slow join, crash, or the tile promises something the first minute does not show | Join-time and thumbnail-honesty fix | performance.md §loading, icons-thumbnails-and-store-page.md §2 (the promise), analytics-and-discovery.md §What clickbait costs |
| T3b | Bounce 61–180 s high, or the first-session curve has a cliff at one minute mark | FTUE: no reward, confusion, wall of UI | Fix the earliest funnel step that loses twice its neighbours | tutorial-and-onboarding.md §14 (repair procedure) and §9 (reading the funnel), design-foundations.md §7.2 |
| T4 | D1 below benchmark median | Core loop, FTUE or performance `[official]` | Loop and first-10-minutes pass; not new content | core-loop-tuning.md §4–6, tutorial-and-onboarding.md §2, genres/<genre>.md |
| T4b | D1 fine, session time or D1 playtime low | No mid-session goal or depth | Goal ladder, meso loop, co-play | economy-and-progression.md, game-craft.md |
| T4c | Social or round-based game, CCU under about 50, players spread over many servers or stuck on "waiting for players" | Empty-server problem: the game is not dead, it only looks dead `[lihfolk]` | Lower max players for the start place (about 8–12 for co-op and social), fill servers fully, make the loop work with 1–3 players or bots, merge mode places into one, show cross-server activity (global feed, shared event) | community-moderation-safety.md, data-and-purchases.md §messaging, growth-and-marketing.md §11 |
| T5 | D1 fine, D7 or D2–7 play days low | Progression wall or empty mid-game `[official]` | Find the stall level; re-curve | economy-and-progression.md |
| T5b | D7 fine, D30 or D8–28 play days low | No endgame, social system or update cadence `[official]` | Weekly day, events, collections, trading or guilds | liveops-quests-retention.md |
| T6 | Retention at or above median, PTR below median | Icon, thumbnails, title | 3–5 distinct honest thumbnails, video, title pass | icons-thumbnails-and-store-page.md (Level-up table, then §3 and §13), analytics-and-discovery.md |
| T7 | Retention fine, conversion low | First purchase too hard or too expensive | Starter pack after first win, cheap repeatables | monetization-and-policy.md |
| T7b | Conversion fine, ARPPU or spend days low | Shallow price ladder, nothing to rebuy | Ladder depth, consumables, season pass | monetization-and-policy.md, economy-and-progression.md |
| T8 | Everything at or above median, DAU flat | Reach | Events, creators, ads, localisation | growth-and-marketing.md |

Notes for reading the numbers:

- T6 is cheap (hours) and may run in parallel with any step, provided the tile shows the real first minute. A PTR gain that raises bounce is a net loss: Recommended For You scores post-click behaviour: since 15 June 2026 it ranks on play-through rate plus first-play bounce (qualified PTR was removed as a ranking signal) over a 28-day window `[official]`.
- A retention dip after a traffic spike is normal, and PTR dips while impressions rise `[official]`. Impressions also move with seasonality (Saturday peak), algorithm changes and competitors `[official]`; check those before blaming the last update.
- "D7" in the dashboard is the 8th day after first play `[official]`. D7 and D30 for the latest cohorts are empty until the days have passed.
- Benchmarks do not affect ranking and the benchmark set changes as the game grows `[official]`.
- Under about 300 new users per reading `[house]`, treat step rates as directional only.
- CCU is an outcome, not a diagnosis. `average CCU = sessions per day × average session minutes ÷ 1,440`, and peak runs roughly 1.5–2.5× the daily average for a one-region audience `[lihfolk]` (rule of thumb). Sessions come from new users (impressions × PTR per source) plus returning users (past cohorts × retention). When CCU moves, find the earliest input that moved: impressions, PTR, bounce, retention, session length, sessions per user.
- Compare like with like: weekday against weekday, holiday against holiday, organic cohort against organic cohort. Use the median first-session length, not the mean.
- Read an update by its new baseline two weeks later, not by its spike: spike then old baseline means content was consumed with no lasting goal; baseline below the old level means the update broke or annoyed something `[lihfolk]`.
- No dashboard benchmark and no numbers from comparable games: run a stopwatch teardown of two leaders and two peers on a fresh account (load to control, first action, first reward, pop-ups in the first 3 minutes, first purchase prompt) and put your own game in the same table. The first-minute gap is usually cheaper to close than any content gap `[lihfolk]`. Template in `references/case-studies-teardowns.md`.
- `[community]` DevForum threads on stalled games repeat three things: add funnel events before changing anything, onboarding fixes moved session time, and inflated first-session rewards can raise D1 without moving D7. Anecdotes, not data.

No numbers yet (under 10 DAU, or no dashboard access):

1. Score from the MCP runbook and a five-stranger playtest (`templates/playtest-plan.md`); every metric-backed dimension caps at 3.
2. Ship instrumentation first: onboarding funnel, shop and offer funnels, economy events (`templates/analytics-event-plan.md`).
3. Get about 300 first sessions (below that, a few points of D1 difference is noise `[lihfolk]`; look only for big leaks): 16+ community, share links per channel, friends. A small capped Plays campaign is an acceptable measurement purchase (ad-acquired users never enter Recommended For You ranking `[official]`), but not while the visible like ratio is under 85%. For a rehearsal, keep the game public with "Exclude from recommendations" on `[official]` so no organic first impressions are spent on an unmeasured first session.
4. Until dashboard benchmarks unlock at 100 DAU, use the fallback rule in §2 and say so in the report.

## 5. Studio MCP audit runbook (read-only first) `[VS]`

Phase A, edit mode, nothing written:

1. `list_roblox_studios` → pick the `studio_id`; `get_studio_state` (must be Edit, not playing). Confirm with the user that this is a copy or that no one else is mid-edit.
2. MCP Permissions (per person, per published game; each game starts at Balanced): choose Safe, keep "Look at your game" on (it carries `universe.analytics:read`) and every other section off for the audit: "Edit your game", "Save & load data", "Publish & manage assets", "Money & monetization", "Player consequences", "Security & credentials".
3. `open_cloud_invoke` GET `/cloud/v2/universes/{id}` and the analytics queries in §1 (optional; skip when screenshots were supplied).
4. `search_game_tree` at depth 2 on Workspace, ReplicatedStorage, ReplicatedFirst, ServerScriptService, ServerStorage, StarterGui, StarterPlayer, Lighting, SoundService. Note structure, naming, where scripts live.
5. `inspect_instance` on Workspace (streaming settings, signal behaviour), Lighting, StarterGui screens (insets, reset-on-spawn), StarterPlayer.
6. `execute_luau` (Edit) census below; then the house-rule scan in checklists.md Gate 4.
7. `script_grep`, one pattern per call (50-match cap): `wait(`, `spawn(`, `delay(`, `tick()`, `LoadAnimation`, `BodyVelocity`, `FindPartOnRay`, `InvokeClient`, `loadstring`, `getfenv`, `require(` (then read the hits for numeric asset ids: a backdoor risk), `OnServerEvent`, `OnServerInvoke`, `ProcessReceipt`, `PromptProductPurchaseFinished`, `SetAsync`, `UpdateAsync`, `BindToClose`, `UserOwnsGamePassAsync`, `PolicyService`, `FilterStringAsync`, `AnalyticsService`, `ConfigService`, `HttpService`.
8. `script_read` in this order: the receipt handler, data load and save, the five largest remote handlers, the offer or shop controller, the tutorial or onboarding script, the main client entry.

Phase B, play mode (changes are discarded on stop):

9. `start_stop_play`; time join-to-playable; `get_console_output` for errors and warnings in the first 60 s.
10. Walk the FTUE with `character_navigation`, `user_mouse_input`, `user_keyboard_input` (or the `playtest` subagent). `screen_capture` at 0 s, 30 s, 2 min, 5 min, in the shop, in the inventory, and at the first offer. Log seconds to first reward, first upgrade, first prompt of any kind. The same captures feed the tutorial rubric, the UI rubric and the art review (the twelve-capture list is in art-direction-and-quality-bar.md §8).
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
| Effort | Hours of the owner's (or team's) real time, including art, test and rollout; minimum 2. Always restate it against the weekly budget from intake: at 10 h a week a 30-hour action is three weeks, not "4 days" |

Tie-breaks: higher in the funnel wins; reversible (a Config flag) beats irreversible; anything that touches the save schema counts double effort. Only T0 blockers skip the queue.

Weekly hours split `[house]`: T0 blockers first until cleared; then about 70–80% on the ranked action list and a fixed 20–30% on the house-rule debt track below. At 10 h a week that is 2–3 hours of asset replacement every week, which is slow but never zero.

### House-rule debt track

Existing violations (primitive Parts, Toolbox or generated models, meshes without collision, pushy offers) are migrated in order of how many players see them, not all at once:

| Order | Surface | Why first |
|---|---|---|
| 0 (blocker, T0) | Walk-through geometry on the main path; invasive or non-compliant offers | Breaks play, trust or policy today |
| 1 | The spawn view: everything on screen in the first 10 seconds | Every new player and every thumbnail capture sees it |
| 2 | The shop, offer surfaces and anything a paid item looks like | Purchases are judged by how the goods look |
| 3 | The main path of the first session and the core-loop station | Where playtime is spent |
| 4 | Thumbnail and video capture locations | Tiles must show the real game, so the real game must look right there |
| 5 | Everything else, by traffic | Periphery last |

Before any kit is replaced, run the cheap whole-game passes in art-direction-and-quality-bar.md §10 (defaults sweep, palette pass, writing pass: hours each); a new kit under default lighting still reads as generic. Rules for the track: replace one kit at a time (the lamp kit, the shop kit) with Blender-authored pieces on the same footprint and with collision, so gameplay and saves are untouched; ship each batch behind the normal safe-change steps; re-run the scan and log the remaining count per area in the report, so the debt visibly falls. Toolbox models that carry scripts are a security finding first (read every script; a `require` of a numeric asset id is T0), an art finding second. Unique, self-made art also removes the near-duplicate discovery risk, so this track is not only cosmetic.

Quick-wins sprint or rebuild `[house]`:

| Choose | When |
|---|---|
| Quick-wins sprint (default; two weeks of the owner's hours, then re-measure) | Core loop ≥ 3, or strangers replay unprompted, or D1 is at or above the "near median" band; and most top-10 actions fit inside one week of the owner's hours each |
| Rebuild the loop inside the same universe (an option to present with its cost, never the automatic answer) | Core loop ≤ 2 with evidence from a stranger playtest, or two measured sprints on the first session and loop did not move the target metric; or security/data ≤ 1 so every fix costs about 3× |
| Park or kill | After one first-session sprint and one loop sprint, five strangers still do not replay and "would you start this today?" is no |

House-rule debt never triggers a rebuild by itself, however much of the map it covers: it goes on the debt track.

Tie-break when both the quick-wins row and the rebuild row are true (a common case: weak loop, but D1 near median): choose quick wins unless all three hold: (1) the loop problem is measured (playtest or funnel), not assumed; (2) the rebuild estimate, in the owner's own hours, fits inside about eight weeks of their budget (80 hours at 10 h a week); (3) a blind second opinion (§8) agrees. If any one fails, run quick wins for two sprints and decide again with the new numbers. When a rebuild is presented, state its hours, its weeks at the owner's pace, what stays live meanwhile, and the lower-cost alternative beside it.

A rebuild keeps the universe, the DataStore key pattern, purchases, badges, favourites and the group. Recommended For You uses a moving window and re-tests daily, so a weak past is not a permanent penalty `[official]`. Players keep everything they paid for.

## 7. Evidence grades and deliverable quality

Grade every finding, so a reader can tell a measurement from a guess (this is the Confidence factor in §6 made explicit):

| Grade | Meaning | Confidence |
|---|---|---|
| Measured | A number from this game: dashboard, funnel, profiler capture, stopwatch | 1.0 |
| Observed | Seen and reproducible in a play pass or stranger playtest; screenshot or clip attached | 0.7 |
| Static | Read in code or the DataModel, not run. Label performance and exploit findings from reading alone "static, not measured" `[lihfolk]` | 0.4–0.7 |
| Inferred | Genre norm, community heuristic or analogy to another game | 0.2–0.4 |

Code findings also carry a severity class `[lihfolk]`, which orders the T0 list: **P0** lost or duplicated data or purchases, client-controlled currency, items or damage, exploitable remotes, paid random items without odds or the policy gate; **P1** freezes, crashes, unprotected DataStore calls, missing shutdown save; **P2** leaks, per-frame waste, connection build-up; **P3** deprecated APIs and style. Keep a **dismissed findings** list (pattern hit, location, one-line reason) so the next audit does not re-litigate them.

Deliverable score, 0–10, for each fix or asset shipped from the plan (adapted from LihFolk's quality-score method; the weights and gates below are ours) `[lihfolk][house]`:

- Hard gates, pass or fail. Any fail caps the score at 5.0: runs with a clean console · no house-rule violation in the work delivered (new or replaced assets are Blender-authored and solid; offers non-invasive) · no policy or data-safety regression · behind a Config flag with a rollback path if it touches a live game · tested on a phone.
- Criteria, each scored 0, 1 or 2 against evidence:

| Criterion | Weight | 0 | 1 | 2 |
|---|---|---|---|---|
| Moves its target metric | 3 | No baseline or no reading | Directional (small sample or playtest only) | Measured against baseline after the lag |
| First-session and mobile impact | 2 | Worse or untested | Neutral | Better, timed |
| Edge cases (rejoin, leave mid-action, double tap, lag) | 2 | Breaks | Some handled | All handled |
| Fit with pillars and the genre loop | 1 | Off-pillar | Neutral | Strengthens the one verb |
| Feedback and polish (sound, visual, copy) | 1 | Silent | Partial | Complete |
| Reversible and documented | 1 | Neither | One | Both |

`score = 10 × Σ(weight × points ÷ 2) ÷ Σ(weight)`, one decimal. Bar: 8.5 to call it done; below that it is a draft and the report says so. Fix the lowest-scoring, highest-weight criterion first, one change per round, at most three rounds, then stop and report what blocks it. Judged criteria (fit, polish) are scored by someone other than the maker, from the evidence only. Log first score, final score and the fix that moved it in the report's re-audit log; after about ten entries the log shows which mistakes to pre-empt.

## 8. Second opinion for high-stakes calls

One reviewer anchors on a first idea and grades their own work kindly. For decisions that are costly to reverse, get a verdict the auditor did not write (method adapted from LihFolk's council skill `[lihfolk]`).

Use it for: ship or hold · quick-wins or rebuild or park · a save-schema migration · a price or economy change on a live game · anything the user asks to be "objective" about. Do not use it for routine fixes.

| Tier | When | Shape |
|---|---|---|
| Quick (default) | Most judgement calls | The auditor writes a verdict privately; one fresh reviewer with a sceptic brief (assume the obvious answer is wrong) gets the question and evidence but not the verdict; compare |
| Standard | Rebuild, migration, live pricing, public launch | Three blind reviewers in parallel with different lenses: player advocate (a 12-year-old on a phone), systems engineer (correctness, security, data, performance), producer or sceptic (scope, cost, risk); the auditor scores the three answers against the rubric |

Procedure:

1. Restate the question neutrally. Remove the owner's preferred answer and loaded wording ("should we finally rebuild?" becomes "compare patching with rebuilding").
2. Fix a 3–5 point rubric before any answer exists (player experience, data and security risk, cost, reversibility, expected metric effect).
3. Build one short evidence pack and give every reviewer the same one: the numbers table, the scorecard, the timed first-session log, screenshots, the relevant code paths. Reviewers inspect the real artefact, not a description of it.
4. Reviewers answer in under about 250 words: verdict, the 2–4 deciding reasons with evidence, confidence.
5. Reconcile: on any disagreement, go with the answer that has evidence behind it. State the verdict, the best argument against it, whether it changed the recommendation, confidence, and what new evidence would flip it.

In Claude Code, reviewers are fresh subagents (or a new session) that receive only the framed question, rubric and evidence pack. Where no second agent is available, hand the same pack to a human reviewer. Limit: reviewers from the same model family share blind spots; playtest data and the official docs outrank any panel.

## 9. Safe-change protocol for live games

1. **Baseline.** Record 14 days (minimum 7) of the target metric, the live place version number, and a Configs export. Never compare PTR across 12 Oct 2026.
2. **Back up.** Add a Version History note to the live version; keep a local `.rbxl` and a git tag. Restoring a version creates a new version and does not publish it; publish and restart servers to make it live `[official]`.
3. **Stage.** Build and test in a separate test universe. No production DataStore access from Studio or the MCP.
4. **Flag.** Ship new behaviour dark behind a Configs key whose code default is the old behaviour. Give risky systems (trading, new shop items, anything that mints currency) their own kill switch so a dupe can be turned off in minutes `[lihfolk]`. Guard test-only flags with `RunService:IsStudio()` so they cannot reach live players. Configs stage first, then "Publish now" (about 15 s–1 min) or "Publish over 15 min"; History → Restore reverts `[official][VS]`.
5. **Experiment or stage the rollout.** With enough DAU, run an Experiment: 50/50, 14–60 days, percent rollout; early-harm metrics (playtime, payer conversion, ARPU) refresh every 5 minutes for the first 24 hours, but a harm verdict needs 10,000 players enrolled across variant and control `[official]`. Under about 1,000 DAU, do before/after on daily cohorts and change one thing per week.
6. **Data.** Additive schema changes only; bump the schema version; migrate before `Reconcile`; never change the key pattern; never wipe. After a publish, old and new servers run side by side until restart `[official]`, so the new schema must be readable by old code, or restart outdated servers at once. Test the migration on copies of real profiles (oldest, largest, richest) in the test universe. DataStore keeps prior versions for 30 days after an overwrite `[official]`: that is the recovery window.
7. **Economy and purchases.** Never remove or weaken something a player paid for. Grandfather owners, compensate when a paid item changes, announce nerfs before they land.
8. **Release.** Separate "publish" from "go live": publish early in the week, gate the new content by server time or a Config, and open it on the announced day `[lihfolk]`. Publish from CI in the audience's off-peak hours. Creator Hub → Configurations → Server management → Restart Servers with "Restart only servers with outdated versions" and a 5–10 minute delay (1–60 allowed); listen to `DataModel.ServerRestartScheduled` to show a countdown and save `[official][VS]`.
9. **Watch for 2 hours.** Log `game.JobId` and `game.PlaceVersion` with every error and report so a live bug can be matched to a server and build. Performance dashboard broken down by Place Version; alerts on client crash rate, out-of-memory exits and server frame rate sent to a webhook (20 alerts per experience) `[official]`; console errors; purchase success.
10. **Rollback triggers written before shipping.** For example crash rate +2 points, early-harm flag red, purchase failures. Roll back by flipping the Config first, then restoring the version, publishing and restarting.
11. **Announce.** Update announcement (60 characters, at most one per 3 days) `[official]`, an Experience Event for anything dated, an in-game changelog panel, a group post. Details in growth-and-marketing.md.
12. **Metadata is a change too.** Swap thumbnails with an update, keep 2–5 active for 7+ days, do not rename the game often (it breaks search for the old name `[official]`), genre changes once per 3 months.
13. **Wait before judging.** PTR and bounce 24–72 h; D1 two days; D7 eight days; impressions lag signals by days.

## 10. Routing: finding → reference

| Finding | Open |
|---|---|
| Not sure which file covers a finding; a standing rule or never-do; the phase a rebuild restarts from | `references/INDEX.md`; `references/decision-rules.md`; `references/workflow-phases.md` |
| Slow or confusing first minutes; tutorial players skip, stall or fail | `references/tutorial-and-onboarding.md` (§14 repair procedure, §13 rubric, §15 symptoms), `references/design-foundations.md` §7, `references/visual-library/tutorials-and-onboarding.md` |
| Loop is dull, no decision, short sessions | `references/core-loop-tuning.md` §4–6, `references/game-craft.md`, `references/genres/<genre>.md`, `references/genre-playbooks.md` |
| Wall, inflation, dead currency | `references/economy-and-progression.md`, `templates/economy-balance-sheet.md` |
| No reason to return, no cadence | `references/liveops-quests-retention.md` |
| Low conversion, invasive or non-compliant offers | `references/monetization-and-policy.md`, `templates/monetization-product-plan.md` |
| Cluttered HUD, weak mobile layout, stock UI | `references/ui-design-figma.md` (§9 rubric, §10 redesign), `references/ui-input-crossplatform.md`, sheets 01–07 and 19 in `references/visual-library/reference-sheets.md` |
| One screen is weak (shop, inventory, settings, codes, daily rewards, rebirth, notifications, loading) | `references/ui-screen-recipes.md` |
| UI pops in, buttons give no feedback, rewards land flat on screen | `references/ui-motion-and-feedback.md` |
| Looks generic, default or "AI-made"; no style bible; disciplines do not match | `references/art-direction-and-quality-bar.md` (§2 tells, §8 review, §10 ordered passes), `references/visual-library/` (index in `references/INDEX.md`) |
| Primitives, marketplace assets, mixed style, no collision | `references/art-pipeline-blender.md`, `references/blender-modeling-craft.md` (modelling quality and budgets), checklists.md house-rule scan |
| FPS, memory, crashes, join time | `references/performance.md` |
| Client trust, unguarded remotes, backdoors | `references/networking-and-security.md` |
| Data loss, unsafe receipts, migration | `references/data-and-purchases.md` |
| Spaghetti scripts, no toolchain | `references/engineering-architecture.md`, `references/architecture-patterns-luau.md`, `references/ai-toolchain-skills.md` |
| Low PTR, weak icon, tile, video or title | `references/icons-thumbnails-and-store-page.md` (craft, rubric §15), `references/visual-library/icons-and-thumbnails.md`, `references/analytics-and-discovery.md` (signals, tests) |
| Good metrics, no reach | `references/growth-and-marketing.md` |
| Missing events, no funnels | `references/analytics-and-discovery.md`, `templates/analytics-event-plan.md` |
| Actions feel flat, rewards land silently, weak hit or reveal moments | `references/vfx-and-juice.md` (principles, rubric §16), `references/vfx-recipes.md` (the effect to rebuild), `references/game-craft.md` §1 |
| Intro or cutscene delays the first verb, cannot be skipped, or looks amateur; trailer capture | `references/cutscenes-and-cinematics.md` (§15 first-session intros, §17 tells, §16 capture) |
| No or harsh audio, no volume control, music fatigue | `references/audio-sfx-music.md` |
| Stiff, sliding or T-posing characters and NPCs | `references/animation-and-rigs.md` |
| A system is missing or home-grown badly (inventory, quests, pets, trading, rounds, codes) | `references/gameplay-systems-cookbook.md` |
| Vehicles, ragdolls or thrown objects jitter, tunnel or desync | `references/physics-and-vehicles.md` |
| Bugs that only happen live, races, memory leaks, no tests | `references/debugging-and-testing.md` |
| Untyped or slow Luau, deprecated idioms, leaks from connections | `references/luau-mastery.md` |
| Players get lost, dead space, no landmarks, spawn far from the fun | `references/level-design-worldbuilding.md` |
| Flat or muddy look on phones, unreadable interiors, default sky | `references/lighting-and-atmosphere.md` |
| Unsure what "good" looks like in the genre; need comparables and a teardown template | `references/case-studies-teardowns.md`, `references/market-scan-2026-11.md` |
| The owner is new and needs an order to learn things in | `references/learning-paths.md`, `references/glossary.md` |
| Slow or risky Studio habits, no version notes, plugin or MCP misuse | `references/studio-workflow.md`, `references/engineering-architecture.md` §AI agents |
| No settings menu, unreadable text, motion or colour problems, missing QoL | `references/accessibility-and-player-qol.md` |
| Griefing, unfiltered text, no report or ban path, empty servers, unmoderated community | `references/community-moderation-safety.md` |
| Revenue splits, contractors, IP, DevEx, tax, group ownership and permissions | `references/team-business-legal.md` |
| Scope creep, no pillars, no playtests, no postmortems; a rebuild or relaunch that needs a plan | `references/process-and-playtesting.md`, `templates/game-one-pager.md`, `templates/lean-gdd.md`, `templates/playtest-plan.md`, `templates/launch-checklist.md` |

## Review gate

- [ ] Intake answered; baseline window and place version recorded.
- [ ] All ten dimensions scored with an evidence line each; caps applied (no numbers → 3; house-rule or trust hit → 1). Dimensions 1, 2, 6, 7 and 10 quote their guide's rubric score.
- [ ] House-rule debt listed by surface with a visibility-ranked migration track and its weekly share of hours; only main-path walk-through geometry and invasive or non-compliant offers treated as blockers.
- [ ] Effort stated in hours and in weeks at the owner's weekly budget; with no access, the numbers-only first pass was sent instead of an empty template.
- [ ] Benchmarks named with source and date; own dashboard benchmark used where it exists.
- [ ] Triage step stated (T0–T8) with the numbers that selected it.
- [ ] Every action has Impact, Confidence, Effort, a metric and an owner; top 10 ranked.
- [ ] Quick-wins, rebuild or park decision stated with the rule that triggered it.
- [ ] Safe-change plan: backup, flag, rollout, data check, rollback triggers, announcement.
- [ ] Developer level set at intake and the report shaped to it; blockers shown at every level.
- [ ] Sub-checks 2a, 4a and 6a run on a phone and their caps applied.
- [ ] Every finding carries an evidence grade; reading-only findings are labelled "static, not measured"; dismissed findings listed.
- [ ] High-stakes decision (ship, rebuild, migration, live pricing) has a blind second opinion with dissent and confidence recorded.
- [ ] Shipped deliverables scored 0–10 with gates; nothing under 8.5 is called done.
- [ ] The audit itself wrote nothing: no edits, publishes or DataStore calls.
- [ ] `[VS]` facts re-checked at create.roblox.com/docs or flagged as unchecked.

## Sources

Accessed 2026-11-10; platform facts re-read on 2026-11-11 against the `Roblox/creator-docs` GitHub mirror (commit 7cbffff, 2026-11-10).

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
- GameAnalytics 2026 Roblox report percentiles (500+ titles above 1M MAU), as recorded in `references/liveops-quests-retention.md` from search summaries of https://www.gameanalytics.com/reports/2026-roblox-report
- https://about.roblox.com/newsroom/2026/06/optimizing-discovery-great-games-reach-millions-players-roblox (search summary)
- https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575 (read: 28-day window, QPTR replaced by PTR and first-play bounce); /t/improved-discovery-measurement-in-creator-analytics/4930122 (read: 12 Oct 2026 measurement change)
- https://devforum.roblox.com/t/struggling-to-increase-ccu-for-new-game/3353917, /t/poor-stats-for-my-new-game-across-the-board/3413365, /t/help-with-improving-player-session-time/3554677, /t/looking-for-advice-on-improving-retention-for-a-wave-based-zombie-shooter/3307981 (search summaries)
- https://devforum.roblox.com/t/introducing-migrate-to-latest-update/535590, /t/improvements-to-updating-experiences/2600703 (search summaries)
- https://rowatcher.com/news/d1-vs-d7-why-fixing-the-wrong-retention-metric-kills-games (search summary; opinion)
- Vault: `references/market-scan-2026-11.md`, `references/knowledge-base.md` §3.9, §3.10, §5.1 (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/quality-score/SKILL.md`, `skills/quality-score/rubrics/system.md`, `skills/council-method/SKILL.md`, `agents/council-member.md`, `agents/council-chair.md`, `commands/audit.md`, `LihFolk Vault V2/SYMPTOMS.md`, `27 Marketing and Growth/Rescuing a Weak Launch - Empty Servers, Low CCU and Relaunch Tactics.md`, `27 Marketing and Growth/Launch Strategy - The First Two Weeks.md`, `27 Marketing and Growth/Competitor Analysis Method.md`, `27 Marketing and Growth/Update Cadence and Hype Cycles.md`, `61 Thumbnails and CTR/From CTR to CCU - Impressions, Play-Through and the Discovery Loop.md`, `58 Player QoL and Game Tweaks/QoL Audit Checklist.md` (read). Ideas adapted in our own words; its checker scripts, hooks and asset pack are not used.
