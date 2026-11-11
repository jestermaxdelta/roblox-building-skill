# Core loop tuning: spec, scorecard, diagnosis, experiments, juice

A method for writing a core loop from scratch and for finding and fixing the broken part of a live game's loop. Open it when writing the loop section of a GDD, before a playtest, and whenever D1, session time or first-play bounce sits below the Creator Analytics benchmark. Paper-design theory (MDA, nested loops, FTUE phases) is in design-foundations.md; the first-minute script, tutorial build, guidance devices and onboarding-funnel repair are in tutorial-and-onboarding.md; the event API and dashboards are in analytics-and-discovery.md; this file is the working procedure for the loop itself.

Tags: `[official]` Roblox docs or staff posts; `[community]` forum, Reddit, blog or third-party report (heuristic, often one developer's numbers); `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production RNG combat game, its other figures are rules of thumb dated October 2026); `[VS]` version-sensitive, re-check at create.roblox.com/docs; `[house]` house estimate.

## Start here by level

Terms: a **core loop** is the set of actions a player repeats to make progress in one session. **FTUE** (first-time user experience) is everything from pressing Play to understanding that loop. A **funnel** is an ordered list of steps with the share of players reaching each. **D1 / D7 / D30** are the shares of new players who return 1, 7 and 30 days after their first visit.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Write the loop sentence (§1) and the first-minute script (tutorial-and-onboarding.md §2); build the guided first loop from that guide's §4 and §8. Time five fresh players with a stopwatch and fill in scorecard checks 1, 2, 4 and 5 (§4). Add juice tier 0 (§8) | Experiments, benchmarks, anything in §7. You do not have the traffic yet |
| Intermediate | Log the onboarding funnel plus skip and hint events; read the charts in the order of §5 every week; fix the earliest weak step; move every tunable number into Configs; run the full scorecard after each change to the first 10 minutes | Three-variant experiments and custom metrics, until daily users pass about 1,000 |
| Expert | One-key experiments with custom metrics and guardrails (§7); cohort reads by acquisition source; versioned funnels when steps change; wall analysis from progression distribution; `fx_tier` and reward-size tests; the update-curve read in §5 | — |

## Contents

0 Evidence · 1 Loop spec, sentence test, session arc · 2 First-10-minutes script (pointer) · 3 Building the tutorial (pointer) · 4 Scorecard · 5 Finding the broken stage in Creator Analytics · 6 Symptom table · 7 Tuning with Configs and Experiments · 8 Juice by cost

## 0. What the evidence supports (read before quoting a number)

- `[official]` D1 is moved by three things: core loop, first-time experience, performance. D7 by the progression system. D30 by endgame content and social systems. Fun should arrive "in 5 minutes or less". Average session time and D1 are the first two metrics to fix, before acquisition.
- `[official]` `[VS]` Recommended For You reads the first session first (play-through rate, first-play bounce at under 60 s and at 61–180 s), then D1 signals, then D2–7, then D8–28. Playtime counts up to 60 minutes per user per game per day. Benchmarks in Creator Analytics are a comparison aid, not a ranking input.
- `[community]` Developers who post their numbers mostly report that tutorials, daily rewards and playtime rewards amplify a working loop and do not rescue a weak one. Before/after figures exist only as single self-reported cases (quoted in §6 with that label).
- No measured Roblox evidence was found linking juice (shake, particles, hit-stop) to retention. The docs call action feedback "imperative" because players otherwise assume the game is broken. Treat juice as part of making the first reward legible, and order it by cost (§8).
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
| Micro | 10–30 s | First rep within 30 s of gaining control; 2+ reps before 60 s; local feedback under 80 ms | Rep length falls or stakes rise with upgrades | Seconds to `FirstAction`, `FirstReward` |
| Meso | 5–15 min | First upgrade by 2 min; first goal done at 5–10 min | One goal completes every 5–10 min for the first 30 min, then every 10–20 | `GoalDone` custom event, value = minutes since the previous one |
| Macro (session) | 15–25 min | First closure at 15–25 min; median first session at least 10 min | Core players end sessions at a stop point, not a wall | First-session curve; session time |
| Meta | Days to weeks | End of session 1 names what is new tomorrow | Something new on each return day of D1–D7; a content beat every 1–2 weeks | Play days D1, D2–7 (out of 6), D8–28 |

Rules: the verb is one word and is performed in 3D by the character, not in a menu (market-scan pattern 3). Every loop level names what the player sees change. A loop with no entry in "100th-rep difference" has a shelf life of minutes. Every number in the spec is a Config key with a code default (§7).

Loop sentence test `[lihfolk]`. Write the loop as one sentence of verbs joined by "so that" ("collect boxes, sell them, buy a faster cart so that you reach the richer aisle and collect more"). It passes when: every verb is something the hands do (collect, swing, place; not "progress" or "grind"); every output is an input to something (currency that buys nothing ends the loop the moment the player notices); something visibly grows on screen; the sentence can be completed once inside the first minute. A feature list ("pets, trading, rebirths, codes") is not a loop.

Build order, and what must be true before the next step `[lihfolk]` `[house]`:

1. **Verb alone.** It is satisfying with no reward attached: first visible response within 1–2 frames, three kinds of feedback (visual, sound, number), three or more variants of sound or animation.
2. **One unit.** The verb produces one primary unit (cash per sale, studs climbed). Secondary units drop from the same verb at a slower rate.
3. **Sinks.** List every place the unit goes. A sink that raises power closes the loop; a cosmetic sink only extends it.
4. **The spend changes the verb.** Every 5–10 minutes of play buys at least one change the player can see. A +3% stat nobody perceives does not close a loop.
5. **Walls with two ways round.** A wall (gate price, boss, power requirement) shapes the meso loop. Each one needs a visible counter (the number required), a cheap retry, and at least two ways past: repeat the verb, switch to a secondary loop, or reset for a multiplier. Reference project: an 82% funnel loss at a boss that could not be passed by grinding or by doing something else; the fixes were open arenas that reset 20 s after the player walks away, a recommended-power number on each stage sign, a next-goal tracker, and rebirth offered at the wall.
6. **Long loop visible from minute 2.** The locked rebirth button, the rarity ladder, the next realm's portal or a leaderboard is in view before the player can use it.

Secondary loops (crafting, fishing, an index) exist to give a different verb when the main one stalls. Each must feed the core (potions raise luck for rolls) or players skip it. Two to four is typical for a hit `[lihfolk]`.

Session arc `[lihfolk]`. A loop says what players do; the arc says how one visit feels. Design each row, and add the exit hook to the spec:

| Phase | Typical length | Give the player | Fails when |
|---|---|---|---|
| Arrival | 0–30 s | Fast join, spawn facing the action, no pop-up stack | Loading over 10 s; three panels on join |
| Re-orientation | 30 s–2 min | "Here is where you were": the goal line, offline earnings, today's calendar day | Returning player cannot tell what changed |
| Warm-up | 2–5 min | A guaranteed easy win: a quest left almost done, a free gift | First action of the session is a wall |
| Main push | 5–30 min | The meso loop: next gate, tier, boss | No milestone inside any 10-minute window |
| Peak | Any time | One memorable moment: rare pull, boss kill, rebirth burst | Session has no high point |
| Exit hook | Last 2 min | Something unfinished that resolves next visit: a timer, a quest at 2/3, a brew | Hook punishes absence (house rule: it never does) |

Interrupted phone sessions are normal: save progress counters continuously, checkpoint anything longer than a few minutes, land a rejoin near where the player left, and respawn in seconds `[lihfolk]`.

## 2. First-10-minutes script

Moved: the beat-by-beat script template, its funnel steps and fail conditions are in tutorial-and-onboarding.md §2. Targets this file still relies on `[house]`: control within 10 s of joining on a 3 GB Android phone, first verb by 15 s, first reward by 30 s, first upgrade by 2 min, first meso goal at 5–10 min, and no purchase prompt before the first win and minute 10. Extra beats are logged as `FtueBeat` (sketch in §7).

## 3. Building the tutorial

Moved: teaching patterns, step data, guidance devices, the server step machine (save, skip, resume, returning players), copy rules, the per-genre table, the five-version case study, the critique rubric and the repair procedure are in tutorial-and-onboarding.md §3–14. One rule stays here because the loop depends on it: the tutorial is the first run of the real loop, on the real systems, and it ends on a real goal that has a successor.

## 4. Loop scorecard (0–10, observable)

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

Reading: 0–4 the micro loop is not fun; rebuild the verb before tuning anything (no reward schedule rescues it). 5–7 tune with §6 and §7. 8–10 send traffic and move to retention systems (liveops-quests-retention.md). Re-score after every change to the first 10 minutes.

## 5. Locating the broken loop in Creator Analytics

Read in this order; stop at the first chart that is clearly bad. Fixing a later stage while an earlier one leaks wastes the work.

1. **Monitoring → Performance** (100+ DAU for charts) `[official]`: client crash rate, unexpected out-of-memory exits, frame rate and memory percentage, broken down by platform and by **Place Version**. A regression here explains any retention drop that follows an update.
2. **Engagement → New User First Session Retention** `[official]`: share of new users still playing at each minute, current period against the previous one. Note the minute of the steepest drop. Reading `[house]`: before 1 min is arrival; 1–3 min is first payoff; 4–8 min is a missing meso goal; a late cliff is a wall or a session cap.
3. **Funnels → Onboarding** `[official]`: the step with the largest loss relative to its neighbours is the work item. Log win and lose outcomes separately. Skipped steps auto-complete and repeated steps count once, so log steps in a fixed order.
4. **Engagement → Average session time**, filtered by platform and, where offered, memory group `[VS]`. A phone figure far below PC is controls, UI or performance, not the loop.
5. **Retention → D1, D7, D30 with Breakdown = Source** `[official]` (announced October 2025): compare Home Recommendations cohorts only. A fall in overall D1 during an ad or external-link spike is traffic mix, not a design regression.
6. **Retention → cohort table** `[official]`: daily cohorts over their first 10 days, weekly over 10 weeks, each with 7-day playtime, 7-day payer conversion and 7- and 30-day revenue per user. Compare the cohort that first played after a change with the one before it.
7. **Progression distribution** `[official]`: count players per level or stage (grant a marker on advance). A pile-up at one level is the D7 wall.
8. **Acquisition → Home Recommendations**: when impressions fall, check play-through rate, first-play bounce, play days and playtime in the D1, D2–7 and D8–28 windows first, then co-play, qualified sessions and spend.

Instrumenting and reading the onboarding funnel step by step (plumbing checks, the cause table, hint and skip rates) is in tutorial-and-onboarding.md §9, and the repair procedure in its §14. Rule that orders everything here: fix from the earliest weak step forward, one change per release, compared by first-play-date cohort.

`AnalyticsService:LogProgressionEvent` and its Start / Complete / Fail variants exist, but the reference says they do not yet appear in any Roblox-provided chart `[official]` `[VS]`. Until they do, log level attempts as a custom event (name `LevelAttempt`, CustomField01 = level, CustomField02 = result) so walls can be read in Explore.

Reading the curve around an update `[lihfolk]` (daily users from about a week before to two weeks after):

| Pattern | Meaning | Next step |
|---|---|---|
| Big spike, old baseline within a week | Content was consumed fast and left no lasting goal | Add a goal that keeps giving: a collection, a tier, a system |
| Small spike, baseline rises | New systems or goals are working | Repeat the shape |
| Spike, then a baseline below the old one | Something broke or annoyed existing players (nerf, reset, bug) | Error report, economy dashboard, feedback; consider rollback |
| No spike | Nobody knew, or the update was invisible | Event with Notify Me, announcement, a visible change on the game page |

Above 1,000 DAU the weekly AI analytics report flags outlier segments (for example retention falling only on iOS) `[official]` `[VS]`. Alerts on session time, crash rate and concurrent users can post to a Discord webhook `[official]`.

Benchmarks. Use the similar-games range in Creator Analytics first (shown as 50th–90th percentile, 100+ DAU needed).

| Metric | Figures | Tag |
|---|---|---|
| D1 similar-games range | Docs example 12.11–18.73%; DevForum announcement example 12.4–24.1%. Both illustrative; every game gets its own range | `[official]` |
| D1 / D7 / D30, large titles | Median 10.3% / 1.6% / 0.5%. D1 P25 8.4%, P75–P90 12.9–15.9%, P99 22.2%. D7 P25 1.0%, P99 9.1%. D30 top 1% 4.7%. GameAnalytics 2026 report: 500+ titles with 1M+ MAU, Aug 2025–Jul 2026 | `[community]` third-party, read through search summaries |
| Session | Median 9.8 min and 1.56 sessions per player per day (secondary write-up of the same 2026 report). GameAnalytics 2025: half of tracked games under 6 min, P95 near 30 min; games with 0–6 min sessions sit below 10% D1 | `[community]` |
| Folk targets (D1 20% "good", 40% "excellent") | The 2026 report says these circulating figures come from small samples of already-promoted games | `[community]` |

Conflict: design-foundations.md and market-scan-2026-11.md quote the GameAnalytics 2025 figures (median session 6.6 min, P90 about 26 min; D1 4.3% for sessions under 3 min, 11.5% for 19–24 min). The 2026 report samples only titles above 1M MAU, so its medians are higher. Both stand; neither is a target. The target is the game's own P50, then P90, in Creator Analytics.

## 6. Level-up: metric symptom → likely loop cause → experiment → expected movement

"Reported" figures are single self-reported cases from forum or Reddit posts seen through search summaries. They show direction, not a guarantee.

| Symptom | Likely loop cause | Experiment (one variable) | Expected movement |
|---|---|---|---|
| Under-60 s bounce high; first-session curve loses 30%+ in minute 1 | Arrival: slow join, crash on low-memory phones, a menu or play button, spawn far from the verb, tile promises something else | Check Performance (crash rate, out-of-memory exits) by device type first. Then: spawn at the verb with one prompt and no menu, against the current flow | Under-60 s bounce falls within days; D1 follows. Reported: 45% → 18% leaving in the first 30 s after the spawn got one clear first action. Instance streaming cut join times by at least 20% according to a Roblox DevForum streaming thread `[VS]` |
| 61–180 s bounce high, under-60 s fine | Verb found, no payoff: first reward late or weak, first upgrade too expensive, tutorial text in the way | `loop_first_upgrade_cost` or `ftue_start_coins` at two values; or the tutorial at 3 steps against 5 | `FirstUpgrade` conversion up, then 61–180 s bounce down. Reported tutorial cases, in both directions, are in tutorial-and-onboarding.md §0 and §15 |
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
| Large loss at one progression step; players pile up there | A wall with one way past and no visible requirement `[lihfolk]` | Show the required number; make retries free; add a second route (quest, secondary loop, rebirth) | Pile-up level empties over a week; D2–7 play days up |
| Currency balances climb while spend events stay flat | Nothing worth buying; sinks do not change the verb `[lihfolk]` | Add a sink the player can see working; price it in minutes of income | Sink ratio toward 1; session time up |
| Players race through, then leave ("too fast") | Content is consumed before the long loop opens `[lihfolk]` | Smaller early rewards (not harder enemies), or open the long loop earlier. Reference project: new profiles roll only the lowest rarity for their first 60–240 s; effect not measured | Later first-wall arrival; watch D1 as the guardrail |

Tutorial-specific symptoms (hint rate, skip rate, a drop at the first purchase, forced or teleported tutorials, players who finish the tutorial and stall) are in tutorial-and-onboarding.md §15.

## 7. Tuning procedure with Configs and Experiments

One variable at a time. A change that cannot be expressed as one Config key is a redesign, not tuning; ship it as an update and compare cohorts.

1. **Baseline.** Two weeks of data with no change to the system under test. Record the benchmark set in use.
2. **Locate** with §5. Pick the earliest broken stage.
3. **Write the hypothesis** before touching anything: "Because <evidence>, changing <key> from A to B will raise <goal metric>; guardrails <metrics> must not fall."
4. **One key, code default = control.** Stage the Config and test it in Studio with `ConfigService:SetTestingValue` `[VS]`.
5. **Check the minimum detectable effect** on the experiment creation screen. If it is implausibly large (the docs give "more than 100%" as hopeless, and say games under about 1,000 DAU struggle), use the small-game protocol below.
6. **Enrol at the point of use.** `GetConfigForPlayerAsync` then `GetValue` enrols the player for that key; calling it on join enrols players who never reach the system and dilutes the result `[official]`. With audience targeting, eligibility is re-evaluated every session, so persist the assigned value in the profile when a flow spans sessions.
7. **Add up to three custom metrics** built from events already logging: per-user funnel conversion at the target step, participation % on a custom event, average net currency delta `[official]` `[VS]`. Metrics cannot change after the start.
8. **First 24 hours: harm only.** Playtime, payer conversion and ARPU refresh every 5 minutes; thresholds are −10%, −20% and −20%, judged only once 10,000 players are enrolled across variant and control. A sample-ratio-mismatch banner means stop and restart `[official]` `[VS]`.
9. **Run the full term** (14–60 days; up to two variants and a control). The key is locked. Do not ship content that touches the same system; do not overlap experiments that could interact.
10. **Decide.** Goal metric's confidence interval excludes 0, and no guardrail is significantly down. A custom metric that moves while the topline stays flat is information: the change worked mechanically but has not moved retention.
11. **Roll out** through Make decision, record hypothesis, values, result and decision in the postmortem log (process-and-playtesting.md §7 weekly experiment SOP and §9), pick the next variable. A win that came from misleading UI or pressure is a kill regardless of uplift.

Changes that are not experiments (a new feature, a risky system) go out by staged rollout instead: dark, team allowlist, 1–5%, 25–50%, 100%, with abort criteria written first. The plan table and its small-game limits are in liveops-quests-retention.md §Shipping an update. If you assign variants yourself instead of using Experiments, key the assignment to the user id, which keeps a player in one group from session to session, and attach the variant as a custom field to every onboarding event `[lihfolk]`.

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

## 8. Juice checklist, ordered by cost

Work down the list for the core verb first, then the reward, then the goal. Stop when the next tier costs more than the next row of §6. All of it runs on the client: a server-side tween replicates the property to every client every frame and looks jittery `[official]`; send one remote per gameplay fact and build the effect locally (vfx-and-juice.md §7 has the hit-stop and shake values, game-craft.md §1 the shake module).

| Tier | Cost | Items |
|---|---|---|
| 0 | Minutes each, no new assets | Sound on every verb and every UI action, pitch varied ±1 semitone. Button press scale and release. Counters count up and pop, never snap. Number popup at the point of action. Goal bar fills with a tween and chimes on completion |
| 1 | About an hour each, reused assets | `ParticleEmitter:Emit(n)` burst on reward. Reward icon flies to its counter. Flash or `Highlight` toggle on the target. Rarity-scaled sound and colour. Haptic pulse on phones and gamepads (`HapticEffect` `[VS]`) |
| 2 | Half a day each | Trauma-based camera shake with a user slider. Short FOV punch. Client-only hit-stop (animation speed, never the server simulation). Trails and beams on fast objects |
| 3 | Days, Blender work | Anticipation and follow-through animation on the verb. Bespoke VFX meshes. A 2–3 s skippable celebration for rebirth or a rare drop. Layered adaptive music |

Rules: juice scales with the size of the event (game-craft.md tier table) and never hides a telegraph. Budget for the 3 GB Android phone: pooled emitters, capped counts, a low-effects setting. Shake slider, reduce-flashing and reduce-motion options ship with tier 2. Test with the reward UI hidden (does the verb still feel good?) and with sound off (is the reward still legible?). To measure it, put the tier behind a key (`fx_tier`) and read session time and `FirstUpgrade` conversion; expect a small effect and treat a flat result as a reason to stop at tier 1.

## Review gate

- [ ] Loop spec filled in, every number mapped to a Config key with a code default.
- [ ] Loop sentence passes all four checks; every wall has a visible requirement, a cheap retry and two ways past; the session arc has an exit hook that punishes nothing.
- [ ] First-minute script and tutorial pass the review gate in tutorial-and-onboarding.md; funnel steps and `FtueBeat` events live in a published test place; release dates annotated.
- [ ] Scorecard run with five fresh testers or live data; score recorded; anything under 5 sent back to the verb.
- [ ] For a live game: §5 read in order and the earliest broken stage named, with the chart that shows it.
- [ ] One written hypothesis, one key, guardrails named; minimum detectable effect checked or the small-game protocol chosen.
- [ ] No purchase prompt inside the script; notification opt-in only at a warranted moment; no absence punishment in the return hook.
- [ ] Juice tiers 0 and 1 complete for verb, reward and goal; accessibility options present if tier 2 is used; effects budgeted for the low-end phone.
- [ ] Every quoted benchmark carries its tag and date; the target is the game's own Creator Analytics range.

## Sources

Accessed 2026-11-10. "(read)" = content opened in the `Roblox/creator-docs` mirror at commit ccc2b01 (2026-11-07); "(search summary)" = seen only through web search result text.

- Roblox/creator-docs (read), https://github.com/Roblox/creator-docs/tree/main/content/en-us/ : `production/analytics/retention.md`; `production/analytics/engagement.md`; `production/analytics/index.md`; `production/analytics/funnel-events.md`; `production/analytics/performance.md`; `production/analytics/alerts.md`; `production/analytics/insights.md`; `production/analytics/analytics-dashboard.md`; `production/experiments.md`; `production/configs.md`; `production/game-design/core-loops.md`; `production/game-design/onboarding.md`; `production/game-design/onboarding-techniques.md`; `production/game-design/ui-ux-design.md`; `discovery.md` and discovery-faq.md; `performance-optimization/improve.md`; `reference/engine/classes/HapticEffect.yaml`; `reference/engine/classes/AnalyticsService.yaml` (read; progression events)
- https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157 (search summary)
- https://devforum.roblox.com/t/analytics-track-new-user-retention-by-daily-and-weekly-cohort/3817030 (search summary)
- https://devforum.roblox.com/t/analytics-new-user-first-session-retention-new-and-returning-users/2890832 (search summary)
- https://devforum.roblox.com/t/whats-next-for-streaming-we-need-your-feedback/2218024 and https://devforum.roblox.com/t/updates-to-streaming-enabled/2391960 (search summary; the "join times at least 20% lower" figure was attributed to a Roblox streaming thread, exact thread not confirmed)
- https://www.gameanalytics.com/reports/2026-roblox-report and https://www.gameanalytics.com/reports/2025-roblox-report (search summary)
- https://gamedevreports.substack.com/p/gameanalytics-key-roblox-and-roblox (search summary)
- https://blog.rrqworld.com/roblox-game-retention/ (search summary; session and sessions-per-day figures)
- https://reddit.sentinel-team.org/subreddits/robloxgamedev/snapshots/2026-04-03T05%3A12%3A52.21453Z and https://reddit.sentinel-team.org/posts/1sakqj4/snapshots/2026-04-03T05%3A12%3A52.21453Z (search summaries of r/robloxgamedev posts via a third-party mirror, not opened; the 45% → 18% case)
- https://devforum.roblox.com/t/improving-onboarding-for-our-zombie-shooter/3323657 (read 2026-11-11; the tutorial case is told in tutorial-and-onboarding.md §0)
- https://devforum.roblox.com/t/low-engagement-on-new-game/3778071 (search summary; daily rewards did not help)
- https://devforum.roblox.com/t/how-effective-are-playtime-reward/3652644 (search summary)
- https://devforum.roblox.com/t/suggestions-on-how-to-improve-d1-retention/4369566 (search summary)
- https://devforum.roblox.com/t/my-day-1-retention-is-awful-23-losing-half-my-players-in-under-2-minutes-what-am-i-doing-wrong-with-onboarding/4186434 (search summary)
- https://beebom.com/admin-abuse-might-save-dying-roblox-games-but-hurts-them-in-the-long-run (search summary)
- https://dubit.io/blog/how-we-build-hit-roblox-games (search summary)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/10 Game Design and Genres/Core Loops and Session Design.md`, `…/First-Time User Experience and Onboarding.md`, `LihFolk Vault V2/11 Monetization Publishing and Live Ops/Measuring Onboarding - Funnels, Drop-off and A-B Tests.md`, `LihFolk Vault V2/27 Marketing and Growth/Update Cadence and Hype Cycles.md` (read). Ideas adapted and rewritten; no code or text copied.
