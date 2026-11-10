# Core loop tuning: spec, first 10 minutes, scorecard, diagnosis, experiments, juice

A method for writing a core loop from scratch and for finding and fixing the broken part of a live game's loop. Open it when writing the loop section of a GDD, before a playtest, and whenever D1, session time or first-play bounce sits below the Creator Analytics benchmark. Paper-design theory (MDA, nested loops, FTUE phases) is in design-foundations.md; the event API and dashboards are in analytics-and-discovery.md; this file is the working procedure.

Tags: `[official]` Roblox docs or staff posts; `[community]` forum, Reddit, blog or third-party report (heuristic, often one developer's numbers); `[VS]` version-sensitive, re-check at create.roblox.com/docs; `[house]` house estimate.

## 0. What the evidence supports (read before quoting a number)

- `[official]` D1 is moved by three things: core loop, first-time experience, performance. D7 by the progression system. D30 by endgame content and social systems. Fun should arrive "in 5 minutes or less". Average session time and D1 are the first two metrics to fix, before acquisition.
- `[official]` `[VS]` Recommended For You reads the first session first (play-through rate, first-play bounce at under 60 s and at 61–180 s), then D1 signals, then D2–7, then D8–28. Playtime counts up to 60 minutes per user per game per day. Benchmarks in Creator Analytics are a comparison aid, not a ranking input.
- `[community]` Developers who post their numbers mostly report that tutorials, daily rewards and playtime rewards amplify a working loop and do not rescue a weak one. Before/after figures exist only as single self-reported cases (quoted in §5 with that label).
- No measured Roblox evidence was found linking juice (shake, particles, hit-stop) to retention. The docs call action feedback "imperative" because players otherwise assume the game is broken. Treat juice as part of making the first reward legible, and order it by cost (§7).
- No published before/after data was found for season passes, collection indexes, rebirth pacing or Experience Notifications opt-in rates. Advice on those in this skill is market pattern plus `[house]` reasoning.

## 1. Loop spec format

One page per game. Every blank is filled before any system is built, and re-filled from measured values once the game is live.

```
LOOP SPEC  <game>  v<n>  <date>
Promise   tile/thumbnail shows: ____   the first minute delivers it by: ____
Micro     verb (one word): ____   rep length: __ s
          feedback: visual ____ / sound ____ / number ____   reward: ____
          100th-rep difference: ____   fail -> retry in __ s, and it teaches: ____
Meso      goal: ____   shown on HUD as: ____   length: __ min
          payoff the player SEES in the world (not a menu): ____
Macro     closure (rebirth, zone, round set): ____ at __ min   stop point: ____
          return hook (state that changes while the player is away): ____
Meta      collection: ____   reset layer: ____   social: ____   weekly beat: ____
Tunables  Config keys, one per number below: ____
Events    onboarding funnel steps: ____   custom events: ____
Kill      "If <metric> is below <x> after <n> new users, we change <part>": ____
```

Timing targets per nested loop (`[house]` targets built on the official windows above; tune to the genre benchmark):

| Loop | One cycle | First-session target | Later-session target | Measured by |
|---|---|---|---|---|
| Micro | 5–30 s | First rep within 30 s of gaining control; 2+ reps before 60 s; local feedback under 80 ms | Rep length falls or stakes rise with upgrades | Seconds to `FirstAction`, `FirstReward` |
| Meso | 3–10 min | First upgrade by 2 min; first goal done at 5–10 min | One goal completes every 5–10 min for the first 30 min, then every 10–20 | `GoalDone` custom event, value = minutes since the previous one |
| Macro | 10–25 min | First closure at 15–25 min; median first session at least 10 min | Core players end sessions at a stop point, not a wall | First-session curve; session time |
| Meta | Days to weeks | End of session 1 names what is new tomorrow | Something new on each return day of D1–D7; a content beat every 1–2 weeks | Play days D1, D2–7 (out of 6), D8–28 |

Rules: the verb is one word and is performed in 3D by the character, not in a menu (market-scan pattern 3). Every loop level names what the player sees change. A loop with no entry in "100th-rep difference" has a shelf life of minutes. Every number in the spec is a Config key with a code default (§6).

## 2. First-10-minutes script template

Write it as a table of beats, then build exactly this and time it with a stopwatch on a 3 GB Android phone. The standard funnel step names match analytics-and-discovery.md; extra beats go out as one custom event `FtueBeat` (CustomField01 = beat name, value = seconds since `Spawned`), which gives time-to-beat, something a funnel alone does not.

| Window | Beat | Player does | Game does | Log | Fails when |
|---|---|---|---|---|---|
| Before join | Promise | Taps a tile | Tile shows minute one, not the endgame | (PTR) | Tile and first minute differ: bounce `[official]` |
| 0–5 s | Arrive | Nothing | Spawns in a playable area facing the verb target; rest of the map streams in; no menu, no play button, no cutscene | Step 1 `Spawned` | Control takes over 10 s on the target phone `[house]` |
| 5–15 s | Call to action | Sees one prompt | One device-matched prompt on the one thing to do; nothing else pulses | — | Two or more things compete for attention |
| 15–30 s | First rep | Performs the verb | Same-frame feedback, sound, number; first reward | Steps 2 `FirstAction`, 3 `FirstReward` | No reward by 30 s |
| 30–60 s | Repeat | 2–3 more reps | Goal bar appears already part-filled with the real progress so far | `FtueBeat: GoalBarShown` | Player stops and looks around |
| 60–120 s | First upgrade | Buys or earns it | Visible power change in the world (the aha) | Step 4 `FirstUpgrade` | Upgrade is a menu stat with no visible effect |
| 2–3 min | First choice | Picks between two real options | Contextual tip only when the player meets the system | `FtueBeat: FirstChoice` | A third concept is taught before minute 2 |
| 3–5 min | Joy moment | Hits a milestone | Designed celebration; first collection entry; index opens | `FtueBeat: FirstCollect` | Nothing memorable has happened by minute 5 `[official]` |
| 5–10 min | Meso goal | Completes it | Shows the next three goals (now, this session, long-term); states the return hook | Steps 5 `FirstWin`, 6 `SawGoals` | No visible next goal; dead time over 5 s |
| 10 min+ and first win | After the script | Keeps playing | Offers may begin, through the offer gate only (monetization-and-policy.md); notification opt-in at a warranted moment, 13+ only `[VS]` | Offer funnel | Any purchase prompt earlier (house rule) |
| Session 2 | Welcome back | Returns | What happened while away, one new thing, the next goal | Step 7 `Session2Start` | Lands in the same state with nothing new |

Tutorial style: `[official]` guidance is a brief tutorial or contextual tips, never a long one; teach at the moment the player meets the system; show a timed hint only to players who have not acted after most players have (docs example: most act by 10 s, hint at 11 s). `[community]` reports agree: spawn areas with one clear first action and shorter tutorials are the changes developers credit; no controlled forced-versus-contextual comparison was found. House default: no forced tutorial; a skippable 3-step guided first loop at most.

## 3. Loop scorecard (0–10, observable)

One point per check; half points allowed. Score from a recording of five fresh testers on phones (pre-launch) or from the dashboard (live). The 0–2 × 5 rubric in design-foundations.md §3 judges a paper design; this one judges a build.

| # | Check | How to observe | Point when |
|---|---|---|---|
| 1 | Verb found | Seconds from control to first verb, no reading | Median at most 15 s |
| 2 | Reward lands | Seconds to first reward with visual, sound and number | At most 30 s, all three present |
| 3 | No early exit | Live: first-play bounce in both windows at or better than benchmark. Pre-launch: testers still playing unprompted at 3 min | Live: both windows pass. Pre-launch: 4 of 5 |
| 4 | Loop is statable | Ask at minute 2: "what are you doing and why?" | 4 of 5 answer "I do X to get Y so I can Z" |
| 5 | Next goal on screen | 10 random screenshots across the first 30 min | All 10 show a next goal, its progress and its reward |
| 6 | Meso cadence | Minutes between goal completions | Every gap in the first 30 min is 10 min or less |
| 7 | 100th-rep difference | Hide all reward UI; play the verb for 2 min. List what changed between rep 1 and rep 100 | Still fun as a toy, and one real difference (decision, skill, variance) |
| 8 | Fast recovery | Longest dead time and time from fail to retry in the first 10 min | No dead time over 5 s; retry within 5 s |
| 9 | Stop and return | At the end ask "what will be waiting for you tomorrow?" | 4 of 5 name it; nothing is lost by staying away |
| 10 | Holds past minute 10 | Live: session time and D1 against the 50th-percentile benchmark. Pre-launch: median first session | Live: both at or above P50. Pre-launch: 10 min or more |

Reading: 0–4 the micro loop is not fun; rebuild the verb before tuning anything (no reward schedule rescues it). 5–7 tune with §5 and §6. 8–10 send traffic and move to retention systems (liveops-quests-retention.md). Re-score after every change to the first 10 minutes.

## 4. Locating the broken loop in Creator Analytics

Read in this order; stop at the first chart that is clearly bad. Fixing a later stage while an earlier one leaks wastes the work.

1. **Monitoring → Performance** (100+ DAU for charts) `[official]`: client crash rate, unexpected out-of-memory exits, frame rate and memory percentage, broken down by platform and by **Place Version**. A regression here explains any retention drop that follows an update.
2. **Engagement → New User First Session Retention** `[official]`: share of new users still playing at each minute, current period against the previous one. Note the minute of the steepest drop. Reading `[house]`: before 1 min is arrival; 1–3 min is first payoff; 4–8 min is a missing meso goal; a late cliff is a wall or a session cap.
3. **Funnels → Onboarding** `[official]`: the step with the largest loss relative to its neighbours is the work item. Log win and lose outcomes separately. Skipped steps auto-complete and repeated steps count once, so log steps in a fixed order.
4. **Engagement → Average session time**, filtered by platform and, where offered, memory group `[VS]`. A phone figure far below PC is controls, UI or performance, not the loop.
5. **Retention → D1, D7, D30 with Breakdown = Source** `[official]` (announced October 2025): compare Home Recommendations cohorts only. A fall in overall D1 during an ad or external-link spike is traffic mix, not a design regression.
6. **Retention → cohort table** `[official]`: daily cohorts over their first 10 days, weekly over 10 weeks, each with 7-day playtime, 7-day payer conversion and 7- and 30-day revenue per user. Compare the cohort that first played after a change with the one before it.
7. **Progression distribution** `[official]`: count players per level or stage (grant a marker on advance). A pile-up at one level is the D7 wall.
8. **Acquisition → Home Recommendations**: when impressions fall, check play-through rate, first-play bounce, play days and playtime in the D1, D2–7 and D8–28 windows first, then co-play, qualified sessions and spend.

Above 1,000 DAU the weekly AI analytics report flags outlier segments (for example retention falling only on iOS) `[official]` `[VS]`. Alerts on session time, crash rate and concurrent users can post to a Discord webhook `[official]`.

Benchmarks. Use the similar-games range in Creator Analytics first (shown as 50th–90th percentile, 100+ DAU needed).

| Metric | Figures | Tag |
|---|---|---|
| D1 similar-games range | Docs example 12.11–18.73%; DevForum announcement example 12.4–24.1%. Both illustrative; every game gets its own range | `[official]` |
| D1 / D7 / D30, large titles | Median 10.3% / 1.6% / 0.5%. D1 P25 8.4%, P75–P90 12.9–15.9%, P99 22.2%. D7 P25 1.0%, P99 9.1%. D30 top 1% 4.7%. GameAnalytics 2026 report: 500+ titles with 1M+ MAU, Aug 2025–Jul 2026 | `[community]` third-party, read through search summaries |
| Session | Median 9.8 min and 1.56 sessions per player per day (secondary write-up of the same 2026 report). GameAnalytics 2025: half of tracked games under 6 min, P95 near 30 min; games with 0–6 min sessions sit below 10% D1 | `[community]` |
| Folk targets (D1 20% "good", 40% "excellent") | The 2026 report says these circulating figures come from small samples of already-promoted games | `[community]` |

Conflict: design-foundations.md and market-scan-2026-11.md quote the GameAnalytics 2025 figures (median session 6.6 min, P90 about 26 min; D1 4.3% for sessions under 3 min, 11.5% for 19–24 min). The 2026 report samples only titles above 1M MAU, so its medians are higher. Both stand; neither is a target. The target is the game's own P50, then P90, in Creator Analytics.

## 5. Level-up: metric symptom → likely loop cause → experiment → expected movement

"Reported" figures are single self-reported cases from forum or Reddit posts seen through search summaries. They show direction, not a guarantee.

| Symptom | Likely loop cause | Experiment (one variable) | Expected movement |
|---|---|---|---|
| Under-60 s bounce high; first-session curve loses 30%+ in minute 1 | Arrival: slow join, crash on low-memory phones, a menu or play button, spawn far from the verb, tile promises something else | Check Performance (crash rate, out-of-memory exits) by device type first. Then: spawn at the verb with one prompt and no menu, against the current flow | Under-60 s bounce falls within days; D1 follows. Reported: 45% → 18% leaving in the first 30 s after the spawn got one clear first action. Instance streaming cut join times by at least 20% according to a Roblox DevForum streaming thread `[VS]` |
| 61–180 s bounce high, under-60 s fine | Verb found, no payoff: first reward late or weak, first upgrade too expensive, tutorial text in the way | `loop_first_upgrade_cost` or `ftue_start_coins` at two values; or the tutorial at 3 steps against 5 | `FirstUpgrade` conversion up, then 61–180 s bounce down. Reported: D1 6% → 15% after a 5-step tutorial became 3; session 7.5 → 9.5 min after a tutorial change. Counter-case: a more hand-holding tutorial moved 6 → 6.5 min only |
| One funnel step loses over twice its neighbours | That step is hard to find or not fun | Timed hint at (time most players need + 1 s); move the target into line of sight; `ftue_hint_delay_s` 5 against 10 | Per-user funnel conversion at that step up; D1 only if the step is early |
| Session time 3–6 min; curve cliff at 4–6 min | No meso goal, or the first wall comes too soon | Lower early thresholds (`xp_curve_early`, `cost_growth_early`); add the goal ladder HUD | Survival from minute 5 to 10 up; session time up; D1 with a lag |
| Session time at benchmark, D1 low | A consumable session: nothing changes while away, no stated reason to return | End-of-session return hook: capped offline earnings, tomorrow's calendar day, a timer that completes overnight, opt-in notification | D1 and D1 play days up; session time flat |
| D1 fine, D7 low | Progression wall or content exhausted by day 3–5 | Find the pile-up level; `cost_growth_mid` at two values; add a second verb or a three-category quest board | D2–7 play days up over 2 weeks |
| D7 fine, D30 low | No endgame or social reason | Small content every 2–4 weeks; long collection goals; trading, parties, leaderboards | Weekly cohort table improves over 4–8 weeks; slow to read |
| Playtime per user high, play days low | Marathon sessions with no daily reason; playtime above 60 min a day adds nothing to ranking | Move rewards from duration to days: daily quest board, cumulative calendar | D2–7 play days up; session time may fall, which is acceptable |
| Daily rewards or playtime rewards added, nothing moved | The loop, not the reward layer. Reported: a game with 4-min sessions saw no change from daily rewards; playtime rewards hold players in a session but do not bring them back | Stop adding reward systems; return to rows 1–4 | — |
| Phone session time far below PC | Touch controls, HUD size, frame rate or memory | Phone-only playtest; fix; compare by platform filter | Phone session time converges on PC |
| D1 falls during an ad burst or a viral spike | Cohort mix | None. Read D1 by source | Home Recommendations D1 unchanged |
| Metrics fall the day an update ships | Regression: crash, memory, a new onboarding step, a broken reward | Performance by place version; first-session curve current against previous; roll back or fix | Returns to baseline within 2 cohorts |
| Event-day spike, then a baseline below the old one | Events have replaced progression; players wait for the next giveaway | Event rewards in an event currency; events at most weekly; make ordinary play pay | Between-event DAU stabilises |
| Dislikes and feedback say "I don't know what to do" | No visible next goal | Next-goal HUD (design-foundations.md §7.3); rerun scorecard check 5 | Check 5 passes; session time up |

## 6. Tuning procedure with Configs and Experiments

One variable at a time. A change that cannot be expressed as one Config key is a redesign, not tuning; ship it as an update and compare cohorts.

1. **Baseline.** Two weeks of data with no change to the system under test. Record the benchmark set in use.
2. **Locate** with §4. Pick the earliest broken stage.
3. **Write the hypothesis** before touching anything: "Because <evidence>, changing <key> from A to B will raise <goal metric>; guardrails <metrics> must not fall."
4. **One key, code default = control.** Stage the Config and test it in Studio with `ConfigService:SetTestingValue` `[VS]`.
5. **Check the minimum detectable effect** on the experiment creation screen. If it is implausibly large (the docs give "more than 100%" as hopeless, and say games under about 1,000 DAU struggle), use the small-game protocol below.
6. **Enrol at the point of use.** `GetConfigForPlayerAsync` then `GetValue` enrols the player for that key; calling it on join enrols players who never reach the system and dilutes the result `[official]`. With audience targeting, eligibility is re-evaluated every session, so persist the assigned value in the profile when a flow spans sessions.
7. **Add up to three custom metrics** built from events already logging: per-user funnel conversion at the target step, participation % on a custom event, average net currency delta `[official]` `[VS]`. Metrics cannot change after the start.
8. **First 24 hours: harm only.** Playtime, payer conversion and ARPU refresh every 5 minutes; thresholds are −10%, −20% and −20%, judged only once 10,000 players are enrolled across variant and control. A sample-ratio-mismatch banner means stop and restart `[official]` `[VS]`.
9. **Run the full term** (14–60 days; up to two variants and a control). The key is locked. Do not ship content that touches the same system; do not overlap experiments that could interact.
10. **Decide.** Goal metric's confidence interval excludes 0, and no guardrail is significantly down. A custom metric that moves while the topline stays flat is information: the change worked mechanically but has not moved retention.
11. **Roll out** through Make decision, record hypothesis, values, result and decision in the postmortem log (process-and-playtesting.md §7 weekly experiment SOP and §9), pick the next variable. A win that came from misleading UI or pressure is a kill regardless of uplift.

Order of variables, cheapest and earliest first `[house]`: spawn and first prompt → seconds to first reward → first upgrade cost and starting currency → hint delay → early XP or cost curve → meso goal length → return hook → quest board size → anything monetary (with D1 and D7 as guardrails).

Small-game protocol (under about 1,000 DAU) `[house]`, not causal, so require agreement between signals: change one key; compare the 7 daily new-user cohorts after with the 7 before, same weekdays, Home Recommendations source only, no other update and no change in ad spend inside the window; the leading indicator (step conversion, or survival at the target minute) must move the same way on at least 5 of 7 days; treat relative changes under 10% as noise; if it is ambiguous, revert and try a bolder value rather than a longer wait.

```lua
--!strict
-- Unexecuted sketch. Server module: loop tunables read lazily, FTUE beats logged with time-to-beat.
local AnalyticsService = game:GetService("AnalyticsService")
local ConfigService = game:GetService("ConfigService")
local Players = game:GetService("Players")

local DEFAULTS: { [string]: number } = {
	ftue_hint_delay_s = 11,
	ftue_start_coins = 250,
	loop_first_upgrade_cost = 40,
}
local FIELD1 = Enum.AnalyticsCustomFieldKeys.CustomField01.Name
local snapshots: { [Player]: ConfigSnapshot } = {}
local joinedAt: { [Player]: number } = {}
local Tunables = {}

-- Call where the number is used. The first GetValue for a key is what enrols the player.
function Tunables.get(player: Player, key: string): number
	local snapshot = snapshots[player]
	if snapshot == nil then
		local ok, result = pcall(function()
			return ConfigService:GetConfigForPlayerAsync(player)
		end)
		if not ok then
			return DEFAULTS[key]
		end
		snapshot = result
		snapshots[player] = snapshot
	end
	local value = snapshot:GetValue(key)
	return if typeof(value) == "number" then value else DEFAULTS[key]
end

function Tunables.beat(player: Player, beatName: string)
	local started = joinedAt[player]
	if started then
		AnalyticsService:LogCustomEvent(player, "FtueBeat", os.clock() - started, { [FIELD1] = beatName })
	end
end

Players.PlayerAdded:Connect(function(player)
	joinedAt[player] = os.clock()
end)
Players.PlayerRemoving:Connect(function(player)
	snapshots[player] = nil
	joinedAt[player] = nil
end)
return Tunables
```

## 7. Juice checklist, ordered by cost

Work down the list for the core verb first, then the reward, then the goal. Stop when the next tier costs more than the next row of §5. All of it runs on the client: a server-side tween replicates the property to every client every frame and looks jittery `[official]`; send one remote per gameplay fact and build the effect locally (game-craft.md §1 has values and the shake module).

| Tier | Cost | Items |
|---|---|---|
| 0 | Minutes each, no new assets | Sound on every verb and every UI action, pitch varied ±1 semitone. Button press scale and release. Counters count up and pop, never snap. Number popup at the point of action. Goal bar fills with a tween and chimes on completion |
| 1 | About an hour each, reused assets | `ParticleEmitter:Emit(n)` burst on reward. Reward icon flies to its counter. Flash or `Highlight` toggle on the target. Rarity-scaled sound and colour. Haptic pulse on phones and gamepads (`HapticEffect` `[VS]`) |
| 2 | Half a day each | Trauma-based camera shake with a user slider. Short FOV punch. Client-only hit-stop (animation speed, never the server simulation). Trails and beams on fast objects |
| 3 | Days, Blender work | Anticipation and follow-through animation on the verb. Bespoke VFX meshes. A 2–3 s skippable celebration for rebirth or a rare drop. Layered adaptive music |

Rules: juice scales with the size of the event (game-craft.md tier table) and never hides a telegraph. Budget for the 3 GB Android phone: pooled emitters, capped counts, a low-effects setting. Shake slider, reduce-flashing and reduce-motion options ship with tier 2. Test with the reward UI hidden (does the verb still feel good?) and with sound off (is the reward still legible?). To measure it, put the tier behind a key (`fx_tier`) and read session time and `FirstUpgrade` conversion; expect a small effect and treat a flat result as a reason to stop at tier 1.

## Review gate

- [ ] Loop spec filled in, every number mapped to a Config key with a code default.
- [ ] First-10-minutes script written as beats, built, and timed on a 3 GB Android phone; funnel steps and `FtueBeat` events live in a published test place.
- [ ] Scorecard run with five fresh testers or live data; score recorded; anything under 5 sent back to the verb.
- [ ] For a live game: §4 read in order and the earliest broken stage named, with the chart that shows it.
- [ ] One written hypothesis, one key, guardrails named; minimum detectable effect checked or the small-game protocol chosen.
- [ ] No purchase prompt inside the script; notification opt-in only at a warranted moment; no absence punishment in the return hook.
- [ ] Juice tiers 0 and 1 complete for verb, reward and goal; accessibility options present if tier 2 is used; effects budgeted for the low-end phone.
- [ ] Every quoted benchmark carries its tag and date; the target is the game's own Creator Analytics range.

## Sources

Accessed 2026-11-10. "(read)" = content opened in the `Roblox/creator-docs` mirror at commit ccc2b01 (2026-11-07); "(search summary)" = seen only through web search result text.

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/retention.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/engagement.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/funnel-events.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/performance.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/alerts.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/insights.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/analytics-dashboard.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/experiments.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/configs.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/core-loops.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/onboarding.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/onboarding-techniques.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/ui-ux-design.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md and discovery-faq.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/performance-optimization/improve.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/HapticEffect.yaml (read)
- https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157 (search summary)
- https://devforum.roblox.com/t/analytics-track-new-user-retention-by-daily-and-weekly-cohort/3817030 (search summary)
- https://devforum.roblox.com/t/analytics-new-user-first-session-retention-new-and-returning-users/2890832 (search summary)
- https://devforum.roblox.com/t/whats-next-for-streaming-we-need-your-feedback/2218024 and https://devforum.roblox.com/t/updates-to-streaming-enabled/2391960 (search summary; the "join times at least 20% lower" figure was attributed to a Roblox streaming thread, exact thread not confirmed)
- https://www.gameanalytics.com/reports/2026-roblox-report and https://www.gameanalytics.com/reports/2025-roblox-report (search summary)
- https://gamedevreports.substack.com/p/gameanalytics-key-roblox-and-roblox (search summary)
- https://blog.rrqworld.com/roblox-game-retention/ (search summary; session and sessions-per-day figures)
- https://reddit.sentinel-team.org/subreddits/robloxgamedev/snapshots/2026-04-03T05%3A12%3A52.21453Z and https://reddit.sentinel-team.org/posts/1sakqj4/snapshots/2026-04-03T05%3A12%3A52.21453Z (search summaries of r/robloxgamedev posts via a third-party mirror, not opened; the 45% → 18%, 6% → 15% and 7.5 → 9.5 min cases)
- https://devforum.roblox.com/t/improving-onboarding-for-our-zombie-shooter/3323657 (search summary; 6 → 6.5 min)
- https://devforum.roblox.com/t/low-engagement-on-new-game/3778071 (search summary; daily rewards did not help)
- https://devforum.roblox.com/t/how-effective-are-playtime-reward/3652644 (search summary)
- https://devforum.roblox.com/t/suggestions-on-how-to-improve-d1-retention/4369566 (search summary)
- https://devforum.roblox.com/t/my-day-1-retention-is-awful-23-losing-half-my-players-in-under-2-minutes-what-am-i-doing-wrong-with-onboarding/4186434 (search summary)
- https://beebom.com/admin-abuse-might-save-dying-roblox-games-but-hurts-them-in-the-long-run (search summary)
- https://dubit.io/blog/how-we-build-hit-roblox-games (search summary)
