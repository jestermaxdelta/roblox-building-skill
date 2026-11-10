# Core loop tuning: spec, first 10 minutes, scorecard, diagnosis, experiments, juice

A method for writing a core loop from scratch and for finding and fixing the broken part of a live game's loop. Open it when writing the loop section of a GDD, before a playtest, and whenever D1, session time or first-play bounce sits below the Creator Analytics benchmark. Paper-design theory (MDA, nested loops, FTUE phases) is in design-foundations.md; the event API and dashboards are in analytics-and-discovery.md; this file is the working procedure.

Tags: `[official]` Roblox docs or staff posts; `[community]` forum, Reddit, blog or third-party report (heuristic, often one developer's numbers); `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production RNG combat game, its other figures are rules of thumb dated October 2026); `[VS]` version-sensitive, re-check at create.roblox.com/docs; `[house]` house estimate.

## Start here by level

Terms: a **core loop** is the set of actions a player repeats to make progress in one session. **FTUE** (first-time user experience) is everything from pressing Play to understanding that loop. A **funnel** is an ordered list of steps with the share of players reaching each. **D1 / D7 / D30** are the shares of new players who return 1, 7 and 30 days after their first visit.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Write the loop sentence (§1) and the first-10-minutes table (§2). Build the three-step tutorial from the sketch in §3. Time five fresh players with a stopwatch and fill in scorecard checks 1, 2, 4 and 5 (§4). Add juice tier 0 (§8) | Experiments, benchmarks, anything in §7. You do not have the traffic yet |
| Intermediate | Log the onboarding funnel plus skip and hint events; read the charts in the order of §5 every week; fix the earliest weak step; move every tunable number into Configs; run the full scorecard after each change to the first 10 minutes | Three-variant experiments and custom metrics, until daily users pass about 1,000 |
| Expert | One-key experiments with custom metrics and guardrails (§7); cohort reads by acquisition source; versioned funnels when steps change; wall analysis from progression distribution; `fx_tier` and reward-size tests; the update-curve read in §5 | — |

## Contents

0 Evidence · 1 Loop spec, sentence test, session arc · 2 First-10-minutes script · 3 Building the tutorial · 4 Scorecard · 5 Finding the broken stage in Creator Analytics · 6 Symptom table · 7 Tuning with Configs and Experiments · 8 Juice by cost

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
| Micro | 5–30 s | First rep within 30 s of gaining control; 2+ reps before 60 s; local feedback under 80 ms | Rep length falls or stakes rise with upgrades | Seconds to `FirstAction`, `FirstReward` |
| Meso | 3–10 min | First upgrade by 2 min; first goal done at 5–10 min | One goal completes every 5–10 min for the first 30 min, then every 10–20 | `GoalDone` custom event, value = minutes since the previous one |
| Macro | 10–25 min | First closure at 15–25 min; median first session at least 10 min | Core players end sessions at a stop point, not a wall | First-session curve; session time |
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

## 3. Building the tutorial from the script

The script in §2 is a design. This section turns it into something that survives rejoins, skips, deaths and later edits. The method is adapted from the LihFolk tutorial skill and FTUE notes `[lihfolk]`, restated to our rules; the code is our own sketch. Shape: **steps are data, the server owns progress and rewards, the client only draws guidance.**

Step fields:

| Field | Meaning | Rule |
|---|---|---|
| `id` | Permanent name | Never reused. Saves store ids, not positions, so steps can be inserted or removed later |
| `objective` | The one line on screen | Verb + object, 8 words or fewer, control named for the device in use (`{TAP}`, `{E}`, gamepad glyph), never over the play area |
| `signal`, `goal` | Server event that counts, and how many | Sent by the system that knows it happened (currency changed, pet hatched). Never a client "I finished". 1 for a new verb, 3–10 for a rhythm step |
| `trigger` | Server condition that activates a contextual step | Backpack full, first time near the trader. Every tip outside the first loop uses this |
| `isComplete` | Server check for "already done" | Completes the step for players who got there another way (gift, trade, returning account) |
| `guide`, `hintAfter` | `always`, `whenStuck` or `none`; seconds before help appears | Verbs most players find alone use `whenStuck` with 6–10 s (or the docs' "most players + 1 s"); progress resets the timer; guidance stops once the player has done it unaided |
| `reveal` | HUD keys shown when the step starts | The HUD is hidden until taught, then animates in; locked features show a lock and a price instead of being invisible |
| `reward`, `topUpTo` | What the step pays; a guaranteed balance | Every step pays something visible. If a step asks for a purchase, top the player up to exactly the price so the economy cannot fail the step |
| `optional` | Never blocks the chain | Social steps are always optional; friends can join and play from second one |

Step patterns:

| Pattern | Fields | Use for |
|---|---|---|
| Do it once | `goal = 1`, `guide = always` | Each new verb |
| Do it a few times | `goal = 3..10`, pointer to the nearest target only | Building rhythm; the counter is the reward between hits |
| Try first, help later | `guide = whenStuck`, `hintAfter = 6..10` | Things most players find alone |
| Already done | `isComplete` | Returning or gifted players |
| Contextual | `trigger` + `requires` | Every secondary system, when first met |
| HUD button | `guide = none`, `reveal`, a pulse or hand on the exact button | Menu verbs; the world pointer stays off |
| Social, never a gate | `optional`, completed by the server when a friend is present | Invites, co-play |
| Server-decided moment | Completed by server code | A short skippable scripted beat |
| Affordable purchase | `topUpTo` on the step before | First upgrade, first hatch |

Guidance tools. One pointer at a time; two pointers and the player follows neither.

| Tool | Use when | Avoid when |
|---|---|---|
| `Beam` from the character to the target | Target is off-screen or far | Target is already in view |
| `Highlight` on the target | One interactable among look-alikes | Several targets at once (one per step; the engine caps live highlights `[VS]`) |
| `ProximityPrompt` | The verb is "walk up and press" | The action is a HUD button |
| Pulse or hand on a HUD button | The target is a GUI element | World targets |
| One camera nudge | The player must notice something behind them, once | Repeatedly, or with reduced motion on |
| NPC or ghost demonstration | A physical verb (jump timing, combo) | Text would do; never block input while it plays |
| Level shape: show, try, test | Obbies, horror, platforming | Economy steps the space cannot show |

House rules apply: any arrow, sign or chevron that is a 3D object is a Blender mesh with collision off for decoration-only guides; beams, highlights and particles are effects and are fine. Every cue uses colour plus shape or words, sits inside the safe area, and stops pulsing when `GuiService.ReducedMotionEnabled` is true `[VS]`.

What the server machine must guarantee `[lihfolk]`:

- Progress and rewards live on the server and in the profile; the client receives one replicated state value and draws from it. Every HUD script reads that one value (the HUD reveal), never its own guess.
- Each reward pays once. A skip grants what the remaining steps would have paid; a replay from Settings pays nothing.
- A failed profile load pauses the tutorial. It never restarts it.
- Rejoin resumes the same step. Finished steps never show again. Steps added after launch show only to players who lack them.
- Removed steps map to the nearest current step through a rename table, so nobody is stranded mid-tutorial by an update.
- Funnel logging is server-side, forward-only, and uses a new funnel name (`Tutorial_v3` through `LogFunnelStepEvent`) whenever steps are reordered, so old and new cohorts are not mixed. Skips and hint displays go out as custom events with the step id in a field.
- World guidance is cleaned up on step change and on respawn. Death mid-step respawns fast and the step still works.
- No automatic pop-up of any kind while onboarding runs (daily reward, favourite, group, event, offer). Route every automatic pop-up through one gate function: not during onboarding (treat the first 180 s as onboarding if the state is unknown), not over another panel, reveal or death screen, not in combat, and at least 8 s after the previous one. Purchase offers additionally obey the offer gate in monetization-and-policy.md.

Combat or any step that can be failed is the main funnel risk. If the first minutes need a fight, make it tutorial-safe: the enemy belongs to this player only, and is weakened (reference project: fight-step enemies at 0.5× health and 0.3× damage; the tutorial elite at 4× health and 0.4× damage where normal elites were 12× and 1.5×). A tower-defense first wave cannot be lost; a horror first threat has a long readable warning.

Case study: five versions of one tutorial in two weeks (reference project) `[lihfolk]`.

| Version | Shape | What happened | Change |
|---|---|---|---|
| A | 27 s first-person intro cutscene, then tips | The cutscene sat inside the bounce window | Cutscene disabled |
| B | 11 steps including combat, dash, heal, elite, forge; first roll guaranteed Rare | 7-day funnel lost 31% at the fight step, 34% at the forge step, 82% at the elite step. One step could never complete because the system it depended on had been switched off | Cut hard |
| C | 3 hub steps, no combat, 16–18 s in total | Fast, but the non-obvious part of the economy was never taught | Rebuilt around the hidden loop |
| D | 7 steps: roll, equip, roll again, salvage the weaker item, forge the first, open quests, claim a quest. A real daily quest is seeded first in the list so the forge step completes it | The tutorial finishes a real goal and teaches the quest system by paying out | Players still felt "thrown in" afterwards |
| E | D plus one short combat step ("defeat 3 enemies") and a next-goal chain of 35 goals read from the save | Direction continues after "tutorial complete" | Kept |

Lessons: teach on safe ground first; teach the verbs players will not discover alone, not the obvious one; finish on a real goal; the end of the tutorial needs a successor (design-foundations.md §7.3); check that every step can actually complete after each update. Open trade-off recorded by the same project: a guaranteed great first pull feels generous but shows the top of the early ladder too soon; a modest one leaves room to climb. They switched from Rare-first to Common-first without measuring the effect. Test it.

Starting targets `[lihfolk]` (rules of thumb; replace with your funnel): each early step keeps 90% or more of the players who reached it; 70% or more of starters finish; the whole scripted part is under 3 minutes. Their "first reward under 60 s" is looser than our 30 s; keep 30 s.

Test matrix before shipping any tutorial change: fresh account on a phone-sized viewport, with keyboard, with gamepad; switch input device mid-step; rejoin mid-step; skip; die mid-step; play it with a friend joining; play it with each dependency system's kill switch off.

```lua
--!strict
-- Unexecuted sketch. Server module: tutorial steps as data, progress saved by step id, each step logged once.
local AnalyticsService = game:GetService("AnalyticsService")
local HttpService = game:GetService("HttpService")

export type Step = {
	id: string, -- permanent; never reused for a different step
	objective: string, -- 8 words or fewer; {TOKENS} are resolved per device on the client
	signal: string, -- sent by the server system that knows it happened
	goal: number,
	hintAfter: number?, -- seconds without progress before the pointer appears
	reveal: { string }?, -- HUD keys shown when this step starts
	topUpTo: number?, -- balance guaranteed before this step, so its purchase is affordable
}
export type Saved = { stepId: string?, progress: number?, done: boolean? }
type State = { index: number, progress: number }

local STEPS: { Step } = {
	{ id = "collect", objective = "Collect 5 boxes", signal = "Collected", goal = 5 },
	{ id = "sell", objective = "Sell at the green pad", signal = "Sold", goal = 1, hintAfter = 8 },
	{ id = "upgrade", objective = "{TAP} UPGRADE", signal = "Upgraded", goal = 1, reveal = { "UpgradeButton" }, topUpTo = 40 },
}
local RENAMED: { [string]: string } = {} -- removed step id -> nearest current step id
local states: { [Player]: State } = {}
local Tutorial = {}

local function publish(player: Player, state: State)
	local step = STEPS[state.index]
	player:SetAttribute("Tutorial", HttpService:JSONEncode({
		id = if step then step.id else "done",
		objective = if step then step.objective else "",
		progress = state.progress,
		goal = if step then step.goal else 0,
		hintAfter = if step then step.hintAfter else nil,
		reveal = if step then step.reveal else nil,
	}))
end

-- Call only after the profile loaded. On a failed load do not call: a paused tutorial beats a reset one.
function Tutorial.attach(player: Player, saved: Saved?)
	local state: State = { index = 1, progress = 0 }
	if saved and saved.done then
		state.index = #STEPS + 1
	elseif saved and saved.stepId then
		local id = RENAMED[saved.stepId] or saved.stepId
		for index, step in STEPS do
			if step.id == id then
				state.index, state.progress = index, saved.progress or 0
				break
			end
		end
	end
	states[player] = state
	if state.index == 1 then
		AnalyticsService:LogOnboardingFunnelStepEvent(player, 1, "Joined") -- repeats count once
	end
	publish(player, state)
end

-- Gameplay systems call this; the client never does. Returns the step just completed so the caller pays it and saves.
function Tutorial.signal(player: Player, signal: string, amount: number): Step?
	local state = states[player]
	local step = if state then STEPS[state.index] else nil
	if state == nil or step == nil or step.signal ~= signal then
		return nil
	end
	state.progress = math.min(step.goal, state.progress + amount)
	local finished = state.progress >= step.goal
	if finished then
		state.index += 1
		state.progress = 0
		AnalyticsService:LogOnboardingFunnelStepEvent(player, state.index, step.id)
	end
	publish(player, state)
	return if finished then step else nil
end

function Tutorial.snapshot(player: Player): Saved
	local state = states[player]
	local step = if state then STEPS[state.index] else nil
	return { stepId = if step then step.id else nil, progress = if state then state.progress else 0, done = state ~= nil and step == nil }
end

function Tutorial.detach(player: Player)
	states[player] = nil
end
return Tutorial
```

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

Reading the onboarding funnel properly `[lihfolk]` `[official]`:

1. **Check the plumbing first.** Events come only from published servers (Studio sends nothing), only the first instance of a step counts, and a later step logged without the earlier ones marks them complete. A funnel that looks perfect or empty is usually a logging fault.
2. **Low conversion from `Joined` to step 2** is arrival: join-to-control time, spawn direction, or an unreadable first objective. It is not a tutorial problem.
3. **One step drops sharply.** Read its hint rate (hint shown ÷ players on the step) and skip rate. High hint rate: the objective or target is unclear. High skip rate: the step is tedious. Neither: play it; it may be impossible (a dependency switched off, a drop that never drops, a button off-screen on phones).
4. **A step that can be failed drops.** Make it safe or move it later.
5. **Fix from the earliest weak step forward.** The step after a confusing one inherits its confused players, so the largest drop is not always the one to fix.
6. **Finished the tutorial, D1 still low.** The tutorial ends in a dead end; add the next-goal chain.
7. **Segment before concluding**: platform, new against returning, country. Read medians, not averages.
8. Annotate every release date. One change per release; compare by first-play-date cohort.

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
| Large loss at one progression step; players pile up there | A wall with one way past and no visible requirement `[lihfolk]` | Show the required number; make retries free; add a second route (quest, secondary loop, rebirth) | Pile-up level empties over a week; D2–7 play days up |
| Currency balances climb while spend events stay flat | Nothing worth buying; sinks do not change the verb `[lihfolk]` | Add a sink the player can see working; price it in minutes of income | Sink ratio toward 1; session time up |
| Players race through, then leave ("too fast") | Content is consumed before the long loop opens `[lihfolk]` | Smaller early rewards (not harder enemies), or open the long loop earlier. Reference project: new profiles roll only the lowest rarity for their first 60–240 s; effect not measured | Later first-wall arrival; watch D1 as the guardrail |
| High hint rate on one tutorial step | Objective or target unclear `[lihfolk]` | Rewrite the objective in 8 words; pointer on the exact target | Step conversion to 90%+ |
| Players finish the tutorial, then stall | No successor goal `[lihfolk]` | Next-goal chain that pays once per goal | Session time and D1 up |

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

Changes that are not experiments (a new feature, a risky system) go out by staged rollout instead: dark, team allowlist, 1–5%, 25–50%, 100%, with abort criteria written first. The plan table and its small-game limits are in liveops-quests-retention.md §Shipping an update. If you assign variants yourself instead of using Experiments, assign by user id so the group is stable across sessions, and log the variant in a custom field on every onboarding event `[lihfolk]`.

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

Work down the list for the core verb first, then the reward, then the goal. Stop when the next tier costs more than the next row of §6. All of it runs on the client: a server-side tween replicates the property to every client every frame and looks jittery `[official]`; send one remote per gameplay fact and build the effect locally (game-craft.md §1 has values and the shake module).

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
- [ ] First-10-minutes script written as beats, built, and timed on a 3 GB Android phone; funnel steps and `FtueBeat` events live in a published test place.
- [ ] Tutorial built as server-owned steps saved by id; test matrix passed (phone, keyboard, gamepad, device switch, rejoin, skip, death, friend joins, dependency off); no automatic pop-up during onboarding.
- [ ] Skip and hint events logged; funnel renamed when steps were reordered; release dates annotated.
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
- https://reddit.sentinel-team.org/subreddits/robloxgamedev/snapshots/2026-04-03T05%3A12%3A52.21453Z and https://reddit.sentinel-team.org/posts/1sakqj4/snapshots/2026-04-03T05%3A12%3A52.21453Z (search summaries of r/robloxgamedev posts via a third-party mirror, not opened; the 45% → 18%, 6% → 15% and 7.5 → 9.5 min cases)
- https://devforum.roblox.com/t/improving-onboarding-for-our-zombie-shooter/3323657 (search summary; 6 → 6.5 min)
- https://devforum.roblox.com/t/low-engagement-on-new-game/3778071 (search summary; daily rewards did not help)
- https://devforum.roblox.com/t/how-effective-are-playtime-reward/3652644 (search summary)
- https://devforum.roblox.com/t/suggestions-on-how-to-improve-d1-retention/4369566 (search summary)
- https://devforum.roblox.com/t/my-day-1-retention-is-awful-23-losing-half-my-players-in-under-2-minutes-what-am-i-doing-wrong-with-onboarding/4186434 (search summary)
- https://beebom.com/admin-abuse-might-save-dying-roblox-games-but-hurts-them-in-the-long-run (search summary)
- https://dubit.io/blog/how-we-build-hit-roblox-games (search summary)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/lihfolk-tutorial/SKILL.md`, `skills/lihfolk-tutorial/references/ftue-checklist.md`, `skills/lihfolk-tutorial/references/step-design-patterns.md`, `LihFolk Vault V2/10 Game Design and Genres/Core Loops and Session Design.md`, `…/First-Time User Experience and Onboarding.md`, `…/Onboarding by Genre - The First Five Minutes.md`, `LihFolk Vault V2/11 Monetization Publishing and Live Ops/Measuring Onboarding - Funnels, Drop-off and A-B Tests.md`, `LihFolk Vault V2/27 Marketing and Growth/Update Cadence and Hype Cycles.md` (read). Ideas adapted and rewritten; no code or text copied.
