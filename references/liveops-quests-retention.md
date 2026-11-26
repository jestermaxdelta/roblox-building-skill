# LiveOps, quests, retention and social design

Distilled from knowledge-base sections 1.7, 1.8, 3.3 and 3.4, plus research passes on 2026-11-10 (retention systems, notifications, LiveOps practice) and 2026-11-26 (how the top games run updates and events, measured seasonal lifts, the holiday calendar). Use it when planning quests, daily rewards, season passes, events, notifications, update cadence and social features, and when a live game's D7, D30 or play days sit below benchmark. The first session is owned by tutorial-and-onboarding.md; loop-level diagnosis (session time, D1) by core-loop-tuning.md. Tags: `[official]` Roblox docs, `[community]` forum, press or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production game, its other figures are rules of thumb dated October 2026), `[VS]` version-sensitive, `[house]` house estimate.

## Start here by level

Terms: **LiveOps** = everything done to a game after launch (updates, events, offers, communication). A **return hook** is a reason to come back at a specific time, built in on purpose. **Play days** = the number of distinct days a player returns in a window. A **season pass** (battle pass) is a time-limited reward track climbed with season XP. A **kill switch** is a Config boolean that turns a risky system off without a publish.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | The first-session script in tutorial-and-onboarding.md §2 first. Then one cumulative daily calendar, 3 daily quests and capped offline earnings from the toolkit. One fixed update day you can keep. An in-game What's New panel. Real end dates on everything | Season passes, admin events, notifications, staged rollouts |
| Intermediate | The calendar method: measure throughput, plan mostly config and reskin events, one buffer week a month, a one-page brief per event. Notifications at warranted moments. The T-10 to T+7 timeline. Read each update's curve | Per-flag percentage rollouts; seasonal resets |
| Expert | Calendar and patch notes as validated Config data; staged rollout with written abort criteria; season XP budget with 15–20% slack and boundary-purchase rules; notification scheduling when no server is running; lazy season rollover; reviews that feed the next quarter's capacity numbers | — |

Contents: Onboarding (pointer) · Social rewards · Reading retention · Retention toolkit (daily rewards, playtime gifts, offline, AFK) · Notifications · Quests · Season pass · Cadence and seasons · LiveOps calendar (capacity, event types, overlap rules, calendar as data, event brief, timeline, holiday season 2026–27) · Update-day ritual · Shipping an update · Patch notes · Resets · Social design · Level-up table. Related (implementation): gameplay-systems-cookbook.md §6 Quests and achievements, §7 Daily rewards and playtime rewards, §8 Codes, §24 Server-wide events and boosts.

## Fast routes

For a common task, read only these sections, in this order; the last one is the gate to pass. §N is the section numbered N in that file; quoted names are exact headings (trailing `[tags]` omitted).

| Task | Read |
|---|---|
| Nobody returns (D7, D30) | "Level-up: retention symptoms → likely cause → fix", "Reading retention", "Retention toolkit (no punishment anywhere)", "Social design"; `economy-and-progression.md` "Level-up: economy symptoms → likely cause → fix", "Time to afford: price everything from one income model"; this file "Review gate" (about 156 lines) |
| Daily rewards, playtime gifts, quests | "Retention toolkit (no punishment anywhere)", "Quests and missions", "Notifications done right", "Social rewards (group join, like, favourite, friend join)"; `gameplay-systems-cookbook.md` §0, §6, §7; this file "Review gate" (about 149 lines) |
| Events, season pass, update plan | "Update and event cadence", "LiveOps calendar: from capacity to dated events", "Season pass", "Patch notes and player communication", "Resets, seasons and wipes", "Review gate" (about 330 lines; the holiday plan alone is "Holiday season 2026–27 calendar", 27 lines) |

## Onboarding (first session)

Moved to tutorial-and-onboarding.md: first-minute script (§2), teaching patterns (§3), funnel logging and reading (§9). What this file adds for the first session: no automatic pop-up of any retention system (daily reward, group card, event, offer) while onboarding runs, offline earnings start only after it ends, and the notification opt-in prompt waits for a warranted moment (§Notifications).

## Social rewards (group join, like, favourite, friend join)

Every 2025–26 hit rewards them (Steal An Egg gives 10K free Speed for like + favourite + group join; Climb For Animals Eggs the same). The owner's standing rule: social rewards are bonuses only, asked after the first win. Policy position, checked at source 2026-11-11 `[VS]`: no written rule against in-game rewards for likes or favourites was found in the Community Standards or the creator docs, and no staff statement either way; but one creator reported a game placed under review by automated moderation with a note that lists "artificially inflating experience statistics", and suspected a reward for joining an off-platform community server (DevForum t/4776239, August 2026; cause never confirmed). So: **group-join and friend-join bonuses are the safe default; like and favourite rewards are a risk, to re-check before shipping and leave out if in doubt; rewards for off-platform actions (joining a Discord, following a social account) carry their own risk.** What the docs do penalise is *metadata* that implies a monetary reward ("leading with giveaways") or does not match the content `[official]`. Build them like this:

- **Bonus, never a gate.** The reward is a one-time boost or cosmetic (a 10–15 min 2× boost, a starter cash bump, a badge, a skin), never progress, a zone, a product or a core feature. A player who never joins loses nothing they need.
- **Timing.** Show the "Join our group" card after the first win and after the 600 s grace, as one of the rate-limited cards from the offer gate (monetization-and-policy.md, "Offer and shop playbook"; it counts toward the ≤ 3 cards per session). A permanent small "Rewards" button in the HUD lets the player claim later.
- **Group join is the only one Roblox can verify** `[official]` `[VS]`. Let the player join without leaving: a LocalScript calls `GroupService:PromptJoinAsync(groupId)` (native modal; returns an `Enum.GroupMembershipStatus`). Then verify on the server with `Player:IsInGroupAsync(groupId)` in a `pcall` (`IsInGroup` without `Async` is deprecated; role checks use `GroupService:GetRolesInGroupAsync`). The result is cached per peer and the prompt clears only that client's cache, so a server that already answered "no" this session keeps saying no: re-check with `GroupService:GetGroupsAsync(player.UserId)` behind a throttled "Check again" button (`pcall`, one retry). Grant once, save the flag in the profile.
- **Likes and favourites cannot be verified from game code** and are the risky pair (see above). If the owner keeps them: an honour-based "I liked it" claim, a small one-time thank-you through the same claim flow, never a gate, and nothing that tells the player to like in order to receive. If in doubt, ship the group and friend bonuses only.
- **Friend join and invites** are verified: `Player:GetJoinData().ReferredByPlayerId` for invites, friend presence for co-play. Pay the friend bonus (10–20%) to both players while they are in the same server; never require invites to progress.
- **Copy.** The card says what the reward is and that it is optional. No countdown, no "limited", no fake scarcity. Nothing about it in the title, thumbnail or description.
- **Instrument it.** Funnel: RewardsOpened → GroupPromptShown → GroupVerified → Claimed. If GroupVerified is below about 15% of shown, the reward is too small or shown too early.

## Reading retention

Benchmarks: the game's own similar-games range in Creator Analytics first (100+ DAU). Published figures, with samples and trust levels, are in the one table in analytics-and-discovery.md §Benchmarks; this file carries no copy. Do not set targets from genre "D1 20–35%" ranges or the "20% good, 40% excellent" rule: they sit far above every measured median.

Read D1, D7 and D30 by **Source** and judge design changes on the Home Recommendations cohort; use the daily (10 days) and weekly (10 weeks) cohort table to compare players who first joined during an event or update with those before it `[official]`. Chart order and the metric-by-metric table with experiments are in core-loop-tuning.md §5–6. Diagnosis in one line: low D1 is core loop, onboarding or performance; session time at benchmark with low D1 means no stated reason to return; low D7 is a progression wall or empty mid-game; low D30 is no endgame or social reason to stay. Recommended For You reads the windows in order (first session, D1, D2–7, D8–28), so fix in that order, and fix retention before adding monetization.

## Retention toolkit (no punishment anywhere)

Order of work: the loop first, then these. `[community]` Developers who post results say reward layers amplify a working loop and do not rescue a weak one: a game with 4-minute sessions reported no change from adding daily rewards, and a DevForum reply argues that "Most of the D1 retention is solely based on your core loop", with daily rewards as amplifiers. No published before/after data was found for indexes, rebirth pacing, season passes or notification opt-in; those rows rest on market pattern and house reasoning.

| System | Done right | Evidence | Limits `[VS]` |
|---|---|---|---|
| Daily reward | Cumulative calendar counting days played; never resets. One-tap claim inside the HUD, not a join pop-up. The reward feeds the player's current goal (a boost, upgrade material), with marquee items on day 7 and day 28 anyone can reach. A consecutive-day streak that resets or drops tiers on a miss is rejected (house rule: no punishment) | `[community]` Forum opinion on streaks is split and nobody posts measurements; an unverified Reddit-mirror claim of about 3× D7 and the "30–50% D7 lift" figures on script-seller pages have no usable source | The Engagement Rewards package's `Daily` type is a login streak; handle a missed day yourself. No guilt or "streak ends soon" notifications |
| Playtime reward | A ladder at about 5, 10, 20 and 40 minutes that accumulates per day, not per session, so leaving loses nothing. Stop at 60 min. Pay on active play | `[community]` Developer opinion only: holds players in a session; players hooked only on it do not return | Playtime beyond 60 min per user per day adds nothing to ranking `[official]`. `Player.Idled` (client-only) fires about 2 min after input stops, then every 30 s; Roblox disconnects after 20 min idle `[official]` |
| Quests | 3–5 daily across at least three categories; process goals ("deliver 10") beside outcome goals; the quest nearest completion feeds the next-goal line; unclaimed rewards auto-granted | `[official]` quest and season-pass guides | Never require hard currency |
| Collection index | Silhouettes for undiscovered entries; completion % visible; small set bonuses; a diegetic Blender index board | Market pattern (every 2025–26 hit); no measured evidence found | No entry obtainable only through paid random items; odds shown; `PolicyService` gate |
| Rebirth and soft resets | First rebirth at 15–25 min; a preview of what is kept and gained before confirming; collection and cosmetics always kept | `[community]` generic guidance: a first requirement set too high means players never meet the mechanic; resetting too much reads as punishment | None found |
| Season pass | Plan below; free track finishable by a 4-days-a-week player; catch-up week | `[official]` design guide; no public results found | Paid track never sells power in competitive modes (house) |
| Limited events | Real start and end; event currency with its own sinks; items either return later or are honestly final | `[community]` Event-day spikes are large and short; press analysis argues weekly spectacle makes ordinary progress feel disposable | No restarting countdowns or false scarcity (house). Trending Events chart needs a public event started in the last 7 days with 1,000+ RSVPs `[official]` |
| Update cadence | A fixed day and UTC hour players can count on; most top games use Saturday (measured hours in §Update and event cadence) | `[official]` small update every 2–4 weeks, big every 2–3 months. `[community]` Rogueblox's team said a weekly schedule blocked larger features and burned them out before the game closed | Update announcements: 60 characters, at most once every 3 days `[official]` |
| Friend and co-play hooks | Boost for both players while together; shared goals; cheap or free private servers; invite prompt with launch data that drops the friend next to the inviter | `[official]` Intentional co-play days (joins, invites, private servers) are a ranking signal; the design guide warns against pricing private servers out of reach | Never require invites to progress |
| Notifications | See the next section | `[official]` rules; no public opt-in or lift figures found | 13+, opt-in, one per user per day |
| Offline progress | Capped, the cap stated, claimed through a welcome-back panel that also shows one new thing | `[community]` Analyses of Grow a Garden name offline growth as its return trigger | Nothing is lost while away (house) |
| AFK areas | Prefer none. If the genre expects idle earning, pay the same capped rate offline, so closing the app costs nothing | Pay-to-idle lifts session time without return days; see the playtime row | 20-minute idle disconnect `[official]`; no Roblox rule on AFK rewards was found |
| Timers and restocks | Global, predictable timers (spawns every 5–15 min, server events every 30 min), next time shown | `[community]` Grow a Garden's shop restock is reported as a global 5-minute timer that players track | Missing one never costs progress |
| Codes | A dated code in each update log; a milestone ladder on visits or group members that rewards the community for pushing a counter (a likes ladder rewards likes, which is the risky pair above: prefer visits). Rewards are boosts or cosmetics | `[community]` One press piece: a milestone code buys about a weekend of extra players and a like-ratio bump, not a revival | Nothing about codes, likes or giveaways in the title, thumbnail or description: "leading with giveaways" reduces exposure `[official]` |

Saturdays and December are the peak weeks for Recommended For You traffic; schedule big updates for them. In December the peak is 20 Dec to 3 Jan, not the first half of the month (§Update and event cadence).

Which hook serves which window `[lihfolk]`: D1 is a great first session plus one unfinished goal or a timer that resolves tomorrow. D7 is weekly quests, walls with a visible next step, collections and the calendar's day 7. D30 is updates, live events, friends, trading, leaderboards and seasons. Combine three or four hook families (calendar, timer, goal, accumulation, social, content, collection) so that every join has **at least one thing ready**, and never more than one automatic pop-up at a time (the pop-up gate in tutorial-and-onboarding.md §8).

### Building a daily reward that cannot be exploited or resented

| Decision | Options | Choose |
|---|---|---|
| Shape | Strict streak (a miss resets: rejected); streak with grace or a weekly freeze (rejected: still a loss on the second miss); cumulative count; repeating 7-day cycle; 28-day ladder with a weekly highlight `[lihfolk]` | Cumulative, or a 28-day ladder with weekly highlights. Of all the shapes, a strict streak is likeliest to read as punishment when a child misses a day through no fault of their own |
| Day boundary | Fixed UTC midnight (simple, one "resets in" timer; evening reset in the Americas; a 23:50 and 00:10 double claim is possible). Rolling 24 h (claim time drifts later every day). Rolling window: claim any time after 20 h, streak survives to 48 h `[lihfolk]` | UTC day number for the cumulative calendar. Align every daily reset in the game to the same UTC hour |
| Clock | Client or server | Server `os.time()` only |
| Claim order | Pay then mark, or mark then pay | Mark the claim, save at once, then pay; a crash or double click cannot pay twice. Throttle the remote. Session locking must already be in place or two servers can both pay (data-and-purchases.md) |
| Reward size | Fixed, or scaled | Scale soft currency to the player's stage (for example a share of the next gate price) so day 3 matters at hour 1 and hour 100 `[lihfolk]` |
| Day 7 / 28 | More of the same, or a different texture | Something different: a guaranteed higher-rarity roll, a cosmetic. Show the whole week up front; name rewards in plain words ("4 Tempered Iron", not "x4") |
| Where | Join pop-up, or a place | A claimable object or HUD badge. The reference project used a chest model in the hub (make it a Blender prop) |

Conflict: the LihFolk reference project shipped a strict 7-day streak that resets on a miss, and its notification note lists "your daily streak resets in 3 hours" as usable sparingly. Its own ethics note recommends grace days instead. Our rule is firmer: no streak wipes, no streak-warning notifications. Trust ours; the loss-based version trades a short-term pull for resentment in a young audience.

### Playtime gifts, offline earnings and AFK: measured examples

- **Playtime gifts** `[lihfolk]` (reference project): a small gift every 5 minutes of play (9 a day), a medium every 15 (4 a day), a large every 60 (1 a day). Counted in play time, not wall-clock time; the timer banks at most one interval when a gift is ready, so nothing is lost by not claiming; caps reset at UTC midnight; reward pools show their odds and roll the odds shown. The caps stop the screen becoming an overnight income engine, and the largest gift lands on the 60-minute mark where ranking playtime stops counting. Selling a timer skip or an extra gift for Robux turns the gift into a paid random item, and its odds must then be disclosed `[VS]`.
- **Offline earnings** `[lihfolk]` (reference project): 15% of the active rate, capped at 8 hours (12 with VIP), nothing for absences under 5 minutes, and filling only after the tutorial is finished so the first session is about active play. The house default is 25–50% efficiency with an 8–12 h cap (economy-and-progression.md owns the number); treat 15% as the low end. State the cap in the UI and model it in the balance sheet.
- **AFK** `[lihfolk]`: there are real reasons to allow some idle progress (children leave devices running; auto-modes help players with motor difficulties). If you do: idle yields less than active play; idle activities sit in the social hub so idle avatars at least make it look alive; an auto-action keeps the verb visible (a small reel over the head, not a hidden counter); no idle income before onboarding ends; auto-modes never spend paid consumables. This refines, and does not overturn, the "prefer none" row above.

## Notifications done right `[official]` `[VS]`

- **Who can receive:** opted-in users aged 13+. The game needs 100+ visits and must not be under moderation.
- **Asking:** `ExperienceNotificationService:CanPromptOptInAsync()` in a `pcall`, then `PromptOptIn()`, from a LocalScript. The prompt text is fixed. It does not appear for under-13s, for users already opted in, or within 30 days of the last prompt, so spend it at a moment that warrants a later message: the player has just started something that finishes while they are away ("your egg hatches in 2 hours"). Never on join.
- **Throttle:** one notification per user per day from a game, on top of the user's own daily total across games. Delivery is not guaranteed, and reach rises or falls with how much users engage with your notifications.
- **Content:** personalised to in-game activity and immediately actionable. Docs' good examples: "Your gold goose egg has hatched!", "You're 2 races away from completing the weekly challenge!". Docs' banned or bad examples: generic advertising ("A new line of race cars just dropped"), purely informational messages, disguised ads, false time pressure, bait-and-switch free items, and links that open a pre-loaded purchase.
- **Never** make opting in a condition of playing or progressing.
- **Routing and measurement:** launch data (read with `Player:GetJoinData()`) takes the player to the thing the message was about; an analytics category per message type lets the dashboard compare them. A notification that mentions another user is delivered only if the two are friends.
- **Sending:** server-side through the Open Cloud package (`createUserNotification(userId, { payload = { messageId, type = "MOMENT", parameters, joinExperience = { launchData }, analyticsData = { category } } })`) or the Open Cloud API, using a notification string created in the Creator Dashboard.

The channels are not interchangeable `[official]` `[lihfolk]` `[VS]`:

| | Experience notification | Update announcement | Event notification |
|---|---|---|---|
| Content | Your personalised string with parameters, at most 99 characters `[official]` | 60 characters of free text | Generated from the event |
| Audience | Opted-in players aged 13+ | Everyone who enabled notifications for the game `[official]`; LihFolk says this includes under-13s, which the docs do not confirm | Players who tapped Notify Me (or accepted an in-game RSVP prompt) |
| Frequency | 1 per user per day per game, plus the user's cross-game cap | Once every 3 days | When the event starts |
| Sent by | Server code or Open Cloud | You, from the dashboard | Roblox |
| Lands the player | Wherever the launch data says | The start place | The event's place, with `EventId` in the join context |

Under-13 players cannot receive experience notifications at all, so for a young audience the in-game What's New panel and update board carry the load.

The scheduling problem `[lihfolk]`: "your egg hatched" must be sent hours later, possibly when no server holds that player. Options: (1) send from the server where the trigger happens, which only works for social triggers (a friend online beats the record); (2) a shared due-time queue in MemoryStore that any running server polls and sends from, which needs at least one live server and respects MemoryStore's maximum item lifetime `[VS]`; (3) an external scheduler calling the Open Cloud notification API, for games with quiet hours. Whichever is used, keep at most one queued notification per user and let the priority order below decide which survives. Show one line of context before the system prompt ("We can tell you when it hatches") so the fixed-text prompt makes sense.

Priority for the one daily slot `[house]`: (1) something the player set in motion has finished (hatch, harvest, offline cap full); (2) a friend beat or visited them; (3) "N away from" a weekly goal. Never "we miss you", never a streak warning, never an offer. Game-wide news goes through update announcements and Experience Events, not personal notifications.

## Quests and missions

A quest is an objective, a quantity and a reward. Three horizons:

| Horizon | Length | Examples |
|---|---|---|
| Short | One session | Daily missions, "deliver 5 parcels" |
| Mid | Days to a week | Weekly challenges, collection milestones |
| Long | Weeks to a season | Season pass, rebirth tiers, full collection |

Rules: missions are daily, varied, and never reward hard currency; use at least three mission categories so one play style does not finish everything; auto-award unclaimed completed rewards at season end; a final-week double-XP catch-up keeps late joiners engaged.

Badges: 5 free per day, then 100 R$ each; 512×512 icon; award with `BadgeService:AwardBadgeAsync` on the server after a confirmed achievement.

## Season pass

Build one only when the game can carry it `[lihfolk]`. A pass multiplies retention that exists; it creates none.

| Precondition | Why |
|---|---|
| Players already return several days a week | Daily missions only work on players who come back daily |
| New rewards can ship every month without stalling updates | A pass of recycled rewards reads as a cash grab by season 3 |
| The loop has at least three distinct activities | Otherwise every mission is "do the verb 50 times" |
| Sessions are long enough to finish a day's missions (about 15 min) | Otherwise each day ends with lost progress |
| The economy can absorb a monthly burst of currency and items | Pass rewards are a faucet |

Do not build one before launch or in the first month (the retention curve is unknown), under a few hundred daily players, for session games where nobody cares about cosmetics, or when the team already misses update dates: a season is a promise made in public, and it ends on a fixed date.

`[official]` starting values (season-pass design guide, re-read 26 Nov 2026): about one month, at least a week of rest between seasons, automatic enrolment in the free track, daily missions across three or more categories that never need hard currency, premium as a superset, mid-season upgraders receive premium rewards for every tier already reached, claim by button with unclaimed rewards granted at season end, a retired final reward shown as a 3D model in the world (a Blender showcase piece), double XP in the final week. About 10 tiers is a `[house]` starting count; the guide gives none.

What the top games run (26 Nov 2026) `[community]` `[VS]`: passes tied to an event or season, 4–5 weeks long. RIVALS opened Season 4 on 13 Nov 2026 with a fresh pass and a ranked reset. Murder Mystery 2 runs a 30-tier pass on each event's currency: Candy for Halloween 2026 (18 Oct–16 Nov); Snow Tokens for Christmas 2025 at 600 a tier, 16,800 in all, fed by daily quests (14 Dec–19 Jan). Evade's Halloween pass ran on Wisps to 21 Nov; Forsaken's summer pass opened new tiers weekly. To test a pass change, the Experiments Custom metric set reads average currency source, sink and net delta, which is the docs' own season-pass example `[official]` (analytics-and-discovery.md §Experiments and Configs).

XP budget. Tune for a named target player, then leave slack:

`expected XP = season days × share of days played × XP per play day`; set the last tier at **80–85%** of that `[lihfolk]`.

Worked plan: 28 days; target player active 4 days a week = 16 play days; 3 daily missions at 100, 150 and 250 XP plus about 100 XP from play = 600 XP per play day; expected 9,600 XP. Ladder total about 8,100: tiers at 425, 550, 640, 720, 810, 850, 890, 980, 1,060, 1,190 (cumulative 8,115, 84.5%). Tier 1 lands in the first session.

Why the slack: with none, one missed day puts the target player out of reach; players who realise on day 20 that they cannot finish stop playing the pass, and premium buyers who cannot finish feel cheated.

Structure and rewards `[lihfolk]`:

- **Premium on the same XP bar finishes early** (extra missions = faster XP), which is partly paying to progress and leaves premium players idle in week four. Cleaner: one bar, premium bonus missions, and a few premium-only bonus tiers (11–15) that absorb the extra XP. Avoid separate ladders; they are hard to explain to young players.
- **Slots:** tier 1 is an instant claim on both tracks. Early free tiers prove the pass works (currency, a potion, a small cosmetic). Premium tiers are cosmetics with visible flair; no stat power (house rule). The free track has its own smaller capstone. Premium tiers grant fixed items only: one crate or roll makes the whole premium pass a paid random item with odds and `PolicyService` duties `[VS]`.
- **Premium currency refund:** returning part of the price to finishers feels generous; do the arithmetic first, and never when that currency is also the main sink.
- **"Exclusive" is a promise.** If the final reward might ever return, call it "Season 3 reward", not exclusive.
- **Late joiners, cheapest first:** final-week double XP; a small bank of missed daily missions (cap about 3 days); weekly missions completable in two or three sessions. Paid tier skips turn the deadline into the product; house default is not to sell them.
- Conflict (tier skips): five of the top 35 sell them on 26 Nov 2026 (RIVALS 99 R$ a level, up to +70 for 6,999; Forsaken 79 a tier; Dress To Impress 199; Toilet Tower Defense 79–299; 99 Nights 290–400) `[community]`. Keep the default: a skip sells relief from the deadline, and that pressure peaks in the final week on players who are behind. If the owner overrides it: a passive shop item only, never a popup or a final-week promotion, at one price per tier at every size (RIVALS charges 79.9 R$ a level at +10 and 100 at +20).

Selling and edge cases `[lihfolk]` (implementation in data-and-purchases.md):

- Key everything on a season id that is never reused. Record premium ownership per season id in the profile, with the receipt id; one developer product recorded per season is simpler than a new game pass every month.
- **Boundary purchases:** a prompt opened at 23:59:50 and confirmed after the end still charges the player. Decide the rule in advance (hide the buy button for the last 10 minutes, or grant to the ended season and auto-claim everything reached). Every receipt resolves to a grant; never leave one unprocessed because a season ended.
- **Mid-season upgrade:** claimability depends on the tier reached, not on when premium was bought.
- **Double XP for one mission:** key completion by day number and mission id in the profile, so two servers or a teleport cannot both grant it.
- Feature packages `[VS]`: Missions, Season Passes (beta; `SeasonPasses.addProgressToSeason()`), Engagement Rewards (`rewardClaimedHandlerFunction()`), Bundles (never prompt a StarterBundle on `PlayerAdded`; use the offer gate after the first win).

## Update and event cadence

- `[official]` A content-cadence update should take under three weeks of effort; many games ship one every two weeks to a month, and a common rhythm is small updates every 2–4 weeks with bigger ones every 2–3 months (content-updates guide, re-read 26 Nov 2026). Anything that needs a new system is an expansion: plan it separately. Weekly is what the current top games do `[community]`, not a requirement.
- Each event has exactly one KPI and a unique event currency with its own sinks.

What the top games do now `[community]` `[VS]` (Roblox charts and games API pulled 26 Nov 2026 at 10:01–10:08 UTC; Rolimons player history, hourly since mid-October 2026):

- **They publish constantly.** 27 of the top 30 by CCU had published within 3 days, all 30 within 14. The `updated` field moves on every publish, hotfixes included, so read content cadence from the CCU curve or the update log.
- **Most run one fixed weekly live moment, and the curve shows it**: a 1–2 hour spike to 2–6× the level two hours earlier, gone within about three hours.

| Game | Weekly moment (UTC) | Spike, Oct–Nov 2026 |
|---|---|---|
| Steal An Egg | Saturday 15:00–16:00, an admin event just before the weekly update (guides) | 4.7–5.9M at peak, 3–4× the level two hours earlier; 7.3M on Halloween Saturday, 31 Oct |
| Throw Food For Animals | Saturday 14:00 | 0.9–1.4M, 2.5–3.2× |
| 99 Nights in the Forest | Saturday 18:00 | 0.6–0.8M, 2.5–3.1×; moved to Wednesday 25 Nov 19:00 for Thanksgiving (408K) |
| Steal a Brainrot | Saturday 19:00–20:00 and Tuesday 22:00–23:00 (US Tuesday evening) | up to 6.1× |
| Adopt Me!, Fisch, Volleyball Legends | Saturday 16:00–17:00; Volleyball Legends' description promises "weekly Saturdays at 11:30am EST" | 1.8–4.0× |
| Break and Steal an Egg | Sunday 14:00–15:00, plus some Thursdays | 1.9–3.1× |

Big launches use other days: RIVALS Season 4 at 21:00 US Eastern on Friday 13 Nov, Dandy's World 1.0 on Friday 20 Nov (610K at 21:00 UTC, 4.5×). Without any event, established games' weekend peaks run about 1.3× their weekdays. No chart title carried a countdown (0 of 326 on 26 Nov); countdowns live in the Experience Event, the description and in-world boards. Bracket tags are the norm (53 of the top 99): 12 carried a Thanksgiving tag, and 7 still carried a Halloween tag on 26 Nov.

Event mechanics live on 26 Nov 2026 `[community]` (descriptions, passes and developer products read that day): limited items and "limited returns" with the end date written in, an event currency with its own pass (economy-and-progression.md §Event currency), Black Friday sales, a brand collaboration (Brookhaven's LEGO construction event), anniversaries, paid server-wide boosts and "rain" events (prices in monetization-and-policy.md), and code ladders tied to likes or favourites in at least five top-50 descriptions (the risky pair in §Social rewards).

Seasonal effect, measured `[community]` `[VS]`: daily maximum of Rolimons' 00, 06, 12 and 18 UTC samples, median over 22 established top-50 games (launched 2014–2024, none in steep decline), against each game's own 10–23 Nov 2025 median. Six-hourly samples miss one-hour live events, so spikes are understated.

| Season | Window | Measured effect |
|---|---|---|
| Halloween | Event launches 3–31 Oct 2026 | Daily peak 2.05× the 15 Sep–5 Oct median (26 games); horror and event-led 4–8× (Murder Mystery 2 7.8×, 99 Nights 5.3×, Forsaken 4.4×). Peaks came on each game's event-launch weekend (10–25 Oct), not on 28–31 Oct |
| After Halloween | 4–26 Nov 2026 | Late November 0.96× early November; Murder Mystery 2 0.62× once its event closed on 16 Nov |
| Thanksgiving (US) | Wednesday–Sunday | 2025: week 1.10× (IQR 0.99–1.23); the Saturday after 1.40×, ordinary Saturdays 1.16–1.24×. 2026: Wed 25 Nov 1.16× the Wednesday before |
| Early December | 1–19 Dec | 0.95×; weekdays 0.87–0.94×. The quietest stretch of the season |
| Winter break | 20 Dec – 4 Jan | 1.57× (IQR 1.26–1.93). Best day Saturday 20 Dec 2025 (1.66×); 26 Dec–3 Jan 1.46–1.61× every day, weekdays like Saturdays; Christmas Day 1.30×. Games already past their peak: 0.78× |
| January | 5–18 Jan | Weekdays 1.07–1.29×, weekends 1.44–1.61×; games whose winter event kept running held their gain (10–24 Jan: Murder Mystery 2 2.38×, RIVALS 2.08×, Bee Swarm 4.46×) |
| Summer | 10 Jun – 20 Aug | 1.5–2×; launch new games 10–30 Jun (market snapshot 2026-11-07, not re-measured) |
| Back to school | Late Aug – Sep | 0.8–0.9× (same snapshot) |

Conflict: the 7 Nov market snapshot gave Thanksgiving 1.3–1.5×, winter 1.8–2.5× (2.5–3.5× revenue) and horror up to 4× on 28–31 Oct. Measured, Thanksgiving is an ordinary weekend plus 10–15%, 1.8–2.5× is winter's upper quartile (games with a winter event), and Halloween peaks fall on launch weekends. Use the measured values; the revenue multiple could not be checked and is unverified.

Recommendation. Lower-risk: a fixed weekly update day and UTC hour plus one monthly themed event with real dates. Bold: a weekly live moment at a fixed UTC hour, as the top games run it, promoted through Experience Events (1,000 RSVPs puts an event on the Trending chart) `[VS]`; it drives large spikes, needs staff or a scripted Config-timed event, and on its own holds nobody (Level-up table).

## LiveOps calendar: from capacity to dated events

A live game runs on two clocks: what players see on each day, and what the team can build in a week. The calendar is the document that makes them agree. The method below is adapted from the LihFolk live-ops notes `[lihfolk]`; platform limits are `[official]` `[VS]`.

**1. Three documents, not one.** A quarterly roadmap (seasons, major updates, holiday beats; changes monthly). The event calendar (every player-visible beat with UTC start and end; changes weekly; the only one the game servers read). A weekly work plan (tasks, owners, done criteria). Mixing "Halloween event" and "fix the pet dupe" in one sheet does not survive a busy week.

**2. Measure throughput before drawing anything.** Count what shipped in the last four to six weeks in player-visible units: content units (a zone, a boss, an item set of 8–12), event units (a timed event with its own rewards and some new art), system units (trading, a pass). Maintenance (bugs, support, performance) takes 30–40% of a one-to-four-person team once a game is live, more just after a big update. Plan next quarter at the measured rate, not double it.

**3. Spend the reuse budget.**

| Event type | New work | Example | Share of the calendar |
|---|---|---|---|
| Multiplier | Config only | 2× XP weekend, luck boost | Occasional. Every weekend teaches players to wait for it and play less on weekdays; space them and compare weekday play before and after |
| Rotation | Config, maybe an icon | Weekly shop, featured zone | Weekly, automatic |
| Reskin | Art on existing systems | Themed hub, holiday variants of existing meshes | Most themed beats |
| Mechanic event | New rules on existing systems | Boss rush, server-wide collection goal | At most one mechanic or content event a month |
| Content event | A timed zone, boss or mode | A haunted map for two weeks | See above |

**4. Keep one buffer week a month.** Something will break: a platform change, an exploit, a trend worth riding. Slack is what lets a bad week pass without cancelling a promised event.

**5. Fixed beats first.** Holidays for the countries that make up most of your players (check analytics; summer and school terms differ by hemisphere), your own anniversaries and visit milestones. Then layer the repeating rhythm. Repeating beats are what players learn; one-off beats are what they talk about. Conditional configs can give one key a different value by country, language, new or returning, activity status (new, active, lapsed, reactivated) and payer status `[official]` (configs docs, read 26 Nov 2026), so a regional beat or a lapsed-player welcome is a calendar entry, not a code path. Use it for content and timing; prices and offers stay the same for everyone (monetization-and-policy.md).

**6. Write the overlap rules so they can be checked.** At most one headline event live at a time. Multipliers stack with a headline only by design, with a cap on the combined value. No major publish in a headline event's first 48 hours (fix by Config or kill switch). A season end and the next season's start never share a day. Event store offers end when the event ends and never return under another name.

**7. Respect the platform limits.** At most 10 ongoing or upcoming Experience Events, so public events are for beats worth an RSVP, not every rotation. The Off-Platform Featuring programme needs the event submitted at least 7 days before it starts, public and accurate; the best featured events run 7–30 days; selection weighs DAU growth, playtime, retention, monetization, trends and seasonal alignment; do not edit the event after submitting it `[official]` (re-read 26 Nov 2026). Put "submit for featuring" on the calendar as its own dated line. Events and update announcements are being merged into one Creator Hub form; announcements still use the old one for now `[official]` `[VS]`. Trending Events needs 1,000 RSVPs and an event that started within the last 7 days, so publish headline events about a week ahead and collect RSVPs in the game: a LocalScript gets the event id from `SocialService:GetUpcomingExperienceEventsAsync()` and calls `SocialService:PromptRsvpToEventAsync(eventId)` when the player walks up to the countdown board (before the event starts only; never on join) `[official]` `[VS]`. Update announcements: 60 characters, one per 3 days.

**8. Durations and clocks.** Headline events 7–14 days (two weekends reach weekly players as well as daily ones), multipliers 2–3 days, seasons about a month. Long events get a mid-point beat (a second phase, a reward unlocking on day 5) rather than more days. All times are entered in UTC (daylight saving shifts hand-converted local times by an hour twice a year); the start lands in the afternoon or early evening of the largest region and outside its school hours.

**9. The calendar is data the servers read.** One JSON Config key holds every event (`id`, `kind`, `startsAt`, `endsAt`, boosts). "Friday 18:00 UTC" is then one fact, not three (sheet, code constant, update note), and a slipped date needs no publish. Validate on load; a calendar that fails validation is rejected and the previous one keeps running; run the same validator before staging. Ids are permanent because reward claims and analytics key on them. Client countdowns compare the replicated end time with `workspace:GetServerTimeNow()`, never the device clock.

```lua
--!strict
-- Unexecuted sketch. Server module. The event calendar is one JSON Config key; a bad edit is rejected, not run.
local ConfigService = game:GetService("ConfigService")
local HttpService = game:GetService("HttpService")

export type LiveEvent = { id: string, kind: string, startsAt: number, endsAt: number, boosts: { [string]: number }? }
local BOOST_CAP = 3 -- combined multiplier ceiling per stat
local events: { LiveEvent } = {}
local Calendar = {}

local function problemWith(list: { LiveEvent }): string?
	local seen: { [string]: boolean } = {}
	for i, a in list do
		if seen[a.id] then
			return `duplicate id {a.id}`
		elseif a.endsAt <= a.startsAt then
			return `{a.id} ends before it starts`
		end
		seen[a.id] = true
		for j = i + 1, #list do
			local b = list[j]
			if a.kind == "headline" and b.kind == "headline" and a.startsAt < b.endsAt and b.startsAt < a.endsAt then
				return `headline events overlap: {a.id} and {b.id}`
			end
		end
	end
	return nil
end

local function apply(raw: any)
	local ok, decoded = pcall(function()
		return if typeof(raw) == "string" then HttpService:JSONDecode(raw) else raw
	end)
	local source = if ok and typeof(decoded) == "table" then decoded.events else nil
	if typeof(source) ~= "table" then
		warn("[Calendar] unreadable; keeping the previous calendar")
		return
	end
	local list: { LiveEvent } = {}
	for _, e in source do
		if typeof(e) == "table" and typeof(e.id) == "string" and typeof(e.startsAt) == "number" and typeof(e.endsAt) == "number" then
			local kind = if typeof(e.kind) == "string" then e.kind else "rotation"
			local boosts = if typeof(e.boosts) == "table" then e.boosts else nil
			table.insert(list, { id = e.id, kind = kind, startsAt = e.startsAt, endsAt = e.endsAt, boosts = boosts })
		end
	end
	local problem = problemWith(list)
	if problem then
		warn(`[Calendar] rejected ({problem}); keeping the previous calendar`)
		return
	end
	events = list
end

-- Combined boost for a stat from every event live now, capped. Also the test for "is the event running".
function Calendar.boost(stat: string): number
	local now, total = DateTime.now().UnixTimestamp, 1
	for _, e in events do
		local value = if e.boosts then e.boosts[stat] else nil
		if typeof(value) == "number" and value > 0 and now >= e.startsAt and now < e.endsAt then
			total *= value
		end
	end
	return math.min(total, BOOST_CAP)
end

task.spawn(function()
	local ok, snapshot = pcall(function()
		return ConfigService:GetConfigAsync()
	end)
	if not ok then
		return -- no configs: no events, the game still runs on code defaults
	end
	apply(snapshot:GetValue("calendar"))
	snapshot:GetValueChangedSignal("calendar"):Connect(apply)
	snapshot.UpdateAvailable:Connect(function()
		snapshot:Refresh()
	end)
end)
return Calendar
```

**10. One page per headline event.** If a row is empty the event is not ready.

| Field | Example |
|---|---|
| Goal (one KPI) | Lift weekend D2–7 play days among players in zones 3–5 |
| Promise to the player | "Beat the Frost Titan alongside your server to earn a winter aura" |
| Kind and dates (UTC) | Headline, Fri 18:00 to the Sunday after next 18:00 (9 days), mid-point beat on day 5 |
| New assets | One boss reskin, one aura, three icons, a banner, a thumbnail variant (Blender time budgeted) |
| Reused systems | Boss framework, server goal bar, rewards module |
| Config keys and kill switch | `calendar`, `winterBossHp`, `winterDropRate`; `winterEventEnabled` |
| Currency | Event currency with its own shop; nothing paid in the main soft currency |
| Comms | Event page, 60-character update, What's New entry, featuring submission date |
| Success metric and guardrail | Play days up by a stated amount; error rate and refund rate unchanged |
| Returns? | Marked "never returns" or "may return" before launch |
| Owner | One named person |

Teams skip the guardrail line more than any other. If playtime rises but errors double, the event did not succeed.

**11. Timeline for one update or headline event** `[lihfolk]`:

| When | Action |
|---|---|
| T-10 days | Freeze features. Create the event as private and prepare the featuring submission |
| T-7 | Make the event public, with a thumbnail of its own; submit for featuring if eligible |
| T-5 to T-2 | In-world hint: a closed gate, a covered statue, a Blender countdown board showing the real start time |
| T-1 | Publish the build with the content gated behind the start time, so release bugs surface before players arrive |
| T0 | The calendar starts the event; post the update announcement, switch the thumbnail variant on, set the code live |
| T+1 to T+3 | Monitor errors, the economy and the first-session curve; hold major publishes for 48 h |
| T+7 | Review: spike, decay, new baseline (curve patterns in core-loop-tuning.md §5) |

What an update contains, by audience `[lihfolk]`: a new goal above where engaged players are; a reason and a fast route back for lapsed players (a What's New panel, a returning-player catch-up); one first-session fix for new players; something to do together; a visible change on the game page.

When a date will slip: decide by T-3, not on the day; say so plainly with the new date and one sentence of why; change the event's start time before it passes (players who tapped Notify Me are watching); give something small and real on the original date if possible; never leave a countdown running to a date you will miss.

**12. Review loop.** After each headline event and season: did it ship on the date; did it hit the goal and hold the guardrail; what did it cost in person-days against the estimate; what did players say; one change to the next plan. Feed the cost back into step 2. After two or three cycles the estimates stop being guesses.

To step off the content treadmill, let an occasional update be a system rather than a zone (crafting, a ranked mode, a collection book), raise depth instead of width (mastery tiers on existing items, harder versions of existing bosses), and let rotations run on data.

### Holiday season 2026–27 calendar

Written 26 Nov 2026. Lifts are the measured medians in §Update and event cadence; "what top games did" comes from Rolimons player history plus guides and press (search summaries) unless tagged `[official]`. School breaks differ by country and district: check your players' countries in analytics and shift the dates `[VS]`.

Platform events `[official]`: The Hollow (newsroom, 21 Oct 2026) ran 22 Oct–2 Nov: nine horror games, a new monster each day, quests paying free UGC, creator livestreams, a live finale on 31 Oct, early hub access for Plus subscribers. The Great Build (Roblox Presents game page) runs 25–30 Nov: a gratitude tower where every player gets a free block every hour and community milestones unlock free UGC; it had 44K CCU and 8.7M visits about 40 hours after opening. No platform winter event had been announced by 26 Nov (search); the last was Winter Spotlight, 17 Dec 2024–2 Jan 2025. If one is announced, keep your finale off its finale day.

| Date | Beat | Ship or do | What top games did |
|---|---|---|---|
| Tue 24 – Mon 30 Nov | US Thanksgiving (Thu 26), Black Friday (27), Cyber Monday (30). Measured lift about 1.1× | Too late to build: at most a reskin or a 2-day multiplier from Config, and an honest sale of days. Spend the week finishing the winter event | Drops moved midweek (title tags and CCU curves): Fischgiving Tue 24 Nov; Pet Simulator 99's Turkey event, Dress To Impress's sale and 99 Nights' live event Wed 25 Nov (2.6–2.9× the Wednesday before) |
| Wed 2 Dec | Pass free trials go live in the Roblox Shop `[official]` | Choose which passes get trials and check that pass code reads ownership live (monetization-and-policy.md §Offer and shop playbook) | — |
| Sat 5 Dec | Last ordinary weekend | Winter content finished; event currency, shop, calendar entries and the one-page brief done | Adopt Me opened its winter event Fri 5 Dec 2025 (to 5 Jan, weekly additions, an advent calendar 1–25 Dec); Grow a Garden's Christmas part 1, Sat 6 Dec 2025 |
| Wed 9 Dec | T-10 for a Sat 19 Dec start | Feature freeze; create the Experience Event as private; prepare the featuring submission | — |
| Fri 11 – Sat 12 Dec | T-7: last day for Off-Platform Featuring and for the public event, then collect RSVPs in game | Option A, the first wave: launch on Sat 12 Dec and run to about 10 Jan | Murder Mystery 2 (14–15 Dec 2025), RIVALS' winter season, Dandy's World, Dress To Impress, Fisch and Grow a Garden all launched on or near Sat 13 Dec 2025 (daily spikes of 1.5–5.6×) |
| Fri 18 Dec | T-1 | Publish with the content gated by the Config start time | — |
| **Sat 19 Dec** | **Recommended launch**: the matching Saturday was 2025's best day (1.66×) | Headline event starts; the 60-character update announcement; the thumbnail variant on | Pet Simulator 99, Evade, Volleyball Legends and Sol's RNG spiked 1.7–3.2× on Sat 20 Dec 2025; 99 Nights ran weekly Christmas parts (Saturday spikes 13, 20 and 27 Dec) |
| Thu 24 – Fri 25 Dec | Christmas Eve and Day: the biggest one-hour spikes, but only 1.30× for the day | A scripted server event from the calendar (no publish, no staff) and a free gift for everyone who joins that day; the offer gate unchanged | Steal a Brainrot admin events on 24 and 25 Dec 2025 (7.5M on the 25th); Blox Fruits' update on Christmas Day with free fruit every hour; Adopt Me's free pet; Bee Swarm's Beesmas opened 25 Dec |
| Sat 26 Dec – Sun 3 Jan | The plateau: 1.46–1.61× every day | Mid-point beat on Sat 26 Dec (phase two or a new reward) switched on by Config; hotfixes only | 99 Nights' last part 27 Dec 2025; Blox Fruits' free-fruit event to 31 Dec |
| Thu 31 Dec – Fri 1 Jan | New Year | One event at a fixed UTC hour, or a per-region "midnight" from a conditional config by country; never a local-clock countdown | — |
| Mon 4 – Sun 10 Jan | Many schools return; weekdays fall to 1.15–1.3× | Close the earn window around Sun 10 Jan, then a spend-only grace of 3–7 days and conversion (economy-and-progression.md §Event currency) | Adopt Me kept a shop of event items open to 9 Jan 2026 after its event ended on 5 Jan; 99 Nights' candy canes expired on 28 Dec 2025, before the plateau ended |
| Sat 9 – Sun 17 Jan | January weekends still 1.44–1.61× | T+7 review; brief for the next season or event | Murder Mystery 2's Christmas event ran to 19 Jan 2026 |

What held and what only spiked in 2025 `[community]`: Murder Mystery 2 went from about 90K to 217K when its Christmas event opened on 15 Dec and stayed at 235–257K to 10 Jan (own currency, a 30-tier pass, daily quests, five weeks); Bee Swarm went from 130K on 24 Dec to 209K the day after Beesmas opened and was still about 200K on 10 Jan (the event ran into spring); RIVALS opened a season with its Christmas update and held about 2× into January. Games past their peak spiked and kept sliding: Steal a Brainrot hit 7.5M on Christmas Day, holiday median 0.72× mid-November; Grow a Garden's three Saturday Christmas parts each spiked about 5×, holiday median 0.46×, and one admin event was criticised as stingy; 99 Nights peaked at 4.4M on 27 Dec, 0.78× overall. The holiday multiplies a working game for as long as it has something to work toward.

Lead times for a small team `[house]`: the Blender winter kit (hub dressing, 8–12 variant meshes, an aura, icons, a thumbnail variant) 2–3 weeks, so start by 28 Nov for a 19 Dec launch; event currency, shop and Config entries 3–5 days; featuring and the public event at T-7; nothing but hotfixes from 24 Dec to 1 Jan. Do not start a price or economy experiment that would run across 19 Dec–4 Jan: the player mix changes mid-test (experiments run 14–60 days; analytics-and-discovery.md §Experiments and Configs).

Holiday monetization, heavy but never invasive: Gift versions of the passes and of event items (on 26 Nov RIVALS, Fish It, Forsaken, Toilet Tower Defense and Dandy's World all sell gift variants), one event bundle in the Featured tab with a real end date, sales that last days, and the offer gate unchanged (monetization-and-policy.md §Offer and shop playbook). Two top-50 games sell a missed calendar day (Brookhaven "Missed Day" 9 R$, created 16 Nov 2026; Anime Crusaders X "Unlock Yesterday" 37 R$ in its Christmas event): an advent calendar here counts days played, so there is nothing to buy back.

### The update-day ritual as top games run it (and a solo version)

What current hits do `[community]`: one live moment a week at a fixed UTC hour, mostly on Saturday (measured hours in §Update and event cadence). The "admin abuse" form: a developer joins public servers for about an hour before the update and triggers special weather, shop stock, luck or spawns (Grow a Garden's lead developer, press 2025; Steal An Egg's Saturday 15:00 UTC event, guides August–November 2026); it is sometimes skipped when an update is mostly backend work. The August 2025 admin events of Grow a Garden and Steal a Brainrot coincided with the platform's concurrency record. Cautions: the spike is gone within about three hours (measured); an opinion piece argues weekly spectacle makes ordinary play between events feel pointless; Rogueblox's developers said a weekly schedule kept them from building large features and burned the team out; and in the 2025 holidays, spikes without a progression track held nobody (§Holiday season 2026–27 calendar).

Platform tools `[official]` `[VS]`: Experience Events and update announcements (limits in step 7 above and §Notifications; an event can spawn joiners into a chosen place, and `player:GetJoinData().GameJoinContext.EventId` identifies who came for it). Performance alerts with a webhook for the hour after publishing (crash rate, session time, concurrent users; 100+ DAU). Configs can start timed content at a set moment without a publish.

| Ritual step | Top-game version | Solo-dev sustainable version `[house]` |
|---|---|---|
| Cadence | Weekly, fixed day and hour | Fixed day every 2 weeks, alternating a content update with a quality-of-life plus event update; a rest week after each season. Announce a skip rather than miss silently |
| Scope | New systems and maps from a team | At most 3 working days per update: variants of existing Blender meshes, a new tier at the end of progression, one quest set. New systems are expansions on their own schedule |
| Pre-update event | Staff-run admin event | A scripted 10-minute server event started by a Config timestamp in every server at once; earnable drops in event currency; no staff needed (a calendar entry; module above) |
| Countdown | Title tag, socials, in-world timer | A Blender update board reading the same Config timestamp; an Experience Event created several days ahead so Notify Me exists |
| Update log | In-game panel, Discord, video | The same board lists the 3 headline changes; one update announcement |
| Codes | Several per update across channels | One dated code on the board; one milestone ladder for visits or group members |
| After shipping | Analysts on dashboards | Check Performance by place version and the first-session curve the next morning; alerts on crash rate and session time |
| Community | Moderated Discord, creators | The Roblox group plus one Discord channel; one poll per cycle on what to build next |

Rules: every "limited" claim has a real end date; event rewards never use the main soft currency; content for existing players goes at the end of progression so it is not consumed in a day `[official]`; if an update overruns its budget twice running, lengthen the cadence instead of cutting quality.

The scripted pre-update event is one more calendar entry read by the module above; no separate timer code is needed.

## Shipping an update: flags and staged rollout

Separating **deploying** code (publishing) from **releasing** a feature (players getting it) is what makes a publish routine. Flags live in Configs; engineering detail is in engineering-architecture.md and data-and-purchases.md. Design-level rules `[lihfolk]`:

| Flag kind | Purpose | Value when Configs cannot be read | Lifetime |
|---|---|---|---|
| Release | Hide unfinished work; staged rollout | Off | Weeks; deleted after full release |
| Kill switch | Turn a risky system off in an incident | On (the system works) | Permanent |
| Experiment | Choose a variant | Control | Length of the test |
| Permission | Testers, admins | Off | Long-lived |

Defaults decide what happens when Configs fail to load: a release flag defaulting on ships unfinished work at once, and a kill switch defaulting off shuts trading for everyone for the length of the outage. Name flags positively (`tradingEnabled`). The platform publishes a Config to everyone in about 15 s to 1 min `[VS]` or gradually over 15 minutes and targets by attributes `[official]`; a "5% of players" dial is something you build: hash the user id with a per-flag salt into a bucket so membership is sticky and a different slice goes first each time. Evaluate once per session for anything visible; send the client only the booleans it needs.

| Stage | Who | For | Abort if |
|---|---|---|---|
| Dark | Code shipped, flag at 0% | Until ready | New errors from the dormant modules |
| Internal | Team and tester allowlist | 1–3 days | Any bug that touches saved data |
| Canary | 1–5% | 1–2 days including a weekend evening | Errors clearly up; purchase or session numbers outside noise |
| Wide | 25–50% | 2–4 days | A guardrail moves against you |
| Full | 100%, flag kept one more release | A week | Late bugs: back to wide |

Compare the flagged group with the unflagged group in the same hours, not with last week. Under about 1,000 daily players a 2% canary is 20 people: use it to catch catastrophic failures only, and use time (10% for a week) rather than a larger percentage to gather exposure. A flag turns code off; it does not undo data already written in a new shape. Ship code that reads both shapes first, then start writing the new one, and remove the old reader much later.

## Patch notes and player communication

The in-game What's New panel is the canonical patch note; every other channel is a pointer to it `[lihfolk]`. Under-13 players cannot receive personal notifications, and rules on external links in in-game text have tightened in 2026 `[lihfolk]` `[VS]` (check current policy before printing "join our community"), so the in-game notes must be complete on their own.

- **Panel rules:** shown once per version, tracked on the server in the profile (mark as seen before showing, so a disconnect cannot re-show it); skipped for brand-new players, who have nothing to compare; one tap to dismiss, never over onboarding or combat; notes stored as a versioned JSON Config so a typo is fixed without a publish; the last few versions stay readable from a button; translated if the game is localised. The diegetic update board (Blender) shows the headline; the panel holds the detail.
- **Template:** a one-line headline; New (3–6 bullets, each saying where to find it); Changes with numbers ("Ice Sword damage 120 → 105; attack speed unchanged"); Fixes players reported; Known issues; optionally one line on what is next. Readable in under a minute. Short sentences, the game's own names for things, player units ("about 2 seconds faster on phones"), no hype words in place of information. The docs single out "bug fixes" as an unhelpful update message `[official]`.
- **Nerfs:** the change with numbers; the reason in one honest sentence; what affected players receive (compensation scales with investment, and is close to mandatory if the item was bought with Robux); what you will watch next.
- **Removals:** announced before they happen, with what replaces the feature; anything purchased keeps working or is converted.
- **Mistakes:** what happened in one sentence, who was affected, what you are doing by when, what you are giving back. Say what changed in your process, not "this will never happen again".
- **Silent changes:** invisible refactors need no note. Anything a player can measure (damage, drop rates, prices, timers, rewards) does. A silently lowered drop rate will be found and framed as deception; for paid random items it is also a disclosure breach `[VS]`.

## Resets, seasons and wipes

Prefer the least damaging reset that solves a measured problem `[lihfolk]`; balance detail is in economy-and-progression.md.

| Kind | Resets | Trust cost |
|---|---|---|
| Leaderboard season | Ranking stats only (a new `OrderedDataStore` name per season or week; the old board stays readable as a hall of fame) | Very low |
| Ranked soft reset | Rating pulled toward the start value: `new = anchor + (old − anchor) × k`, k between 0.5 and 0.75 | Low |
| Opt-in seasonal save | A separate season character; the main save is untouched | Low |
| Event currency close | Leftover event tokens after the event (economy-and-progression.md §Event currency) | Low with a spend-only grace, warnings and conversion; high when silent |
| Currency reset | Soft currency | Medium to high |
| Progress or full wipe | Levels, zones, items | High; after launch a last resort |

What top games reset now `[community]` (26 Nov 2026): ranked ratings at each season start (RIVALS Season 4, 13 Nov 2026, with a fresh pass) and event currencies at each event's close (Blox Fruits replaced last year's Candy Corn with a new Halloween currency in 2026; Adopt Me kept a shop of event items open for four days after its winter event ended, to 9 Jan 2026).

Non-negotiables: nothing bought with Robux is taken away without equal or better compensation; receipt records are never wiped; settings survive; a reset is announced before, never discovered on login; something permanent (a title, a cosmetic) marks what was lost. Make resets cheap before they are needed by splitting the profile into permanent and seasonal parts from day one, rolling each profile over lazily the next time it loads (idempotent on season id, with a guard that never rolls early), and restarting servers at the boundary when the build changed.

## Social design

Ladder of social interaction `[lihfolk]`, cheapest first: co-presence (a shared hub) → display (titles, rare-pull announcements) → parallel play → cooperation (shared bosses, server goals) → exchange (trading, gifting) → competition → expression and roleplay. Aim for at least three rungs, and design for a server of three before a server of thirty: a feature that needs ten players in a room fails most of the day. Credit every meaningful contributor (damage share or participation), never last hit only. A scheduled server event needs a join window (reference project: a rift open for 45 s, starting when everyone is in or time runs out). PvP is opt-in with normalised damage.

- Intentional co-play (friends joining together, parties, shared plots) counts toward the co-play discovery signal; random matchmaking does not.
- Server sizes: 6–12 for co-op gameplay, 20–30 for hubs and hangouts. Set from playtest data.
- Waiting time for a match or round under 30 seconds; show something to do while waiting.
- Griefing controls: build-zone ownership, personal plots, report buttons, cooldowns on destructive actions; all user-visible text is filtered (community-moderation-safety.md).
- Social friction audit: for every social feature, list how a stranger could ruin it and what stops them.
- Server Luck or server-wide gifts show a thank-you banner naming the buyer (a social reward that costs nothing).
- Social service APIs: `SocialService:CanSendGameInviteAsync` → `PromptGameInvite(player, ExperienceInviteOptions)` with `LaunchData` up to 200 characters read through `GetJoinData()`; referrals through `ReferredByPlayerId` `[official]` `[VS]`. Notification APIs and limits: §Notifications.

## Level-up: retention symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Session time at benchmark, D1 low | Nothing changes while the player is away | Capped offline progress, a timer that completes overnight, a welcome-back panel; opt-in prompt when the timer starts |
| D1 fine, D7 low; players pile up at one level | Progression wall, or content used up by day 3–5 | Tune the curve at the wall through Configs; add a second verb or a quest board with three categories |
| Daily reward claimed, D7 flat | The reward is unrelated to what the player is working on | Make rewards feed the current goal; move effort back to the loop |
| DAU spikes on update day and each trough is lower | Events have replaced progression | Fewer, real events; event currency; make ordinary play pay; put new content at the end of progression |
| CCU 3–6× for an hour at the weekly live event, the week's median still falling | Spectacle without a track: nothing earned in the hour matters next week (Steal a Brainrot: 7.5M on Christmas Day 2025, holiday median 0.72× mid-November) | A multi-week event with its own currency, pass and daily quests (Murder Mystery 2 held 2.4× for five weeks); the live hour becomes its kick-off |
| CCU falls by a third or more the week an event ends | Nothing follows the close (Murder Mystery 2 0.62× after its Halloween event ended, 16 Nov 2026) | Tease the next beat in the last event week; a spend-only grace; a returning-player hook |
| Winter event barely moved the numbers | Launched on or after 24 Dec, after the featuring window and the best day (20 Dec 2025 was 1.66×), or built at Thanksgiving scope | Launch by Sat 19 Dec, submit for featuring by 11 Dec, run to about 10 Jan (§Holiday season 2026–27 calendar) |
| Title still shows last season's tag | No tag change on the update checklist (7 of the top 99 kept a Halloween tag on 26 Nov 2026) | Title, thumbnail variant and event tag change at T0 and at the event's end (icons-thumbnails-and-store-page.md) |
| Update shipped, D7 and D30 unchanged | New content sat at the start of the game or was consumed in a day | Gate it behind existing progression; add a multi-week goal to it |
| Notification opt-in rate low | Asked on join or with no reason | Ask when the player starts something that finishes later |
| Notifications sent, few joins | Generic content; one-per-day slot spent on low-value messages | Personalised and actionable messages; compare analytics categories; apply the priority order (§Notifications) |
| Playtime per user high, play days low | Rewards pay for duration, not for days | Per-day playtime ladder capped at 60 min; daily quests; cumulative calendar |
| Many idle players, session time inflated | The game pays for idling | Offline rate equal to AFK rate, capped; rewards on active play |
| Co-play days near zero | No reason to bring a friend | Two-sided friend boost, shared goal, cheap private servers, invite prompt after a win |
| Quest board finished in minutes by one play style | One mission category | At least three categories; one process goal per day |
| Few players finish the season pass | XP plan assumes daily play | Re-plan for 4 active days a week; final-week double XP |
| Update days slipping, quality falling | Cadence beyond the team | Move to the 2-week solo ritual ("The update-day ritual as top games run it"); cut scope, not polish |
| Events announced, then quietly cancelled | Calendar drawn before throughput was measured; no buffer `[lihfolk]` | Plan from the last six weeks' output; one buffer week a month |
| Weekday play falls while weekends hold | A multiplier every weekend `[lihfolk]` | Space multipliers; rotate event types |
| An event starts an hour off, or needs a publish to move | Local times, or dates hard-coded in scripts | UTC everywhere; calendar in Configs with validation |
| Two events muddy each other's numbers | Overlapping headline events | Overlap rules enforced by the validator |
| "Secret nerf" videos; dislikes after a balance patch | Changes shipped without numbers or reasons | Patch notes with numbers, a reason, and compensation |
| "I bought premium and got nothing" at season end | A receipt arrived after the season closed and was refused | Boundary rule decided in advance; every receipt resolves |
| A feature flag was turned off and saves broke | New data shape written before old code could read it | Read both shapes first; then write; remove later |

## Review gate

- [ ] First session passes the review gate in tutorial-and-onboarding.md; no retention pop-up appears during onboarding.
- [ ] Every toolkit system in use has its "done right" form; no streak wipes, no absence loss, no pay-to-idle.
- [ ] Daily, weekly and seasonal content with real end dates.
- [ ] Event currency per event; one KPI per event.
- [ ] Update day and cadence chosen for the real team size and announced; countdown, update log and code plan exist.
- [ ] Throughput measured; calendar is mostly config, rotation and reskin events with one buffer week a month; overlap rules written; all times UTC.
- [ ] Calendar and patch notes stored as validated Config data; every headline event has a one-page brief with one KPI, a guardrail, a kill switch and a "returns?" decision.
- [ ] Featuring submission and public event dated at least 7 days ahead; T-1 publish with content gated by start time.
- [ ] Seasonal beats sized from the measured lifts, not folklore; a winter event launches by the Saturday before Christmas week and runs to about 10 Jan with a mid-point beat, a spend-only grace and no staffed work from 24 Dec to 1 Jan.
- [ ] What's New panel shows once per version, skips new players, never blocks play; nerfs and removals carry numbers, a reason and compensation.
- [ ] Daily reward is server-timed, mark-then-save-then-pay, throttled, with no streak wipe; playtime gifts capped per day.
- [ ] Season pass only if the preconditions hold; ladder totals 80–85% of the target player's expected XP; boundary-purchase rule written.
- [ ] Release flags default off and kill switches default on; staged rollout plan has abort criteria; data changes follow read-both-then-write.
- [ ] Notification opt-in prompt only at warranted moments, 13+ only; messages personalised and actionable; nothing gated on opting in.
- [ ] Co-play incentives (friend bonus, party join) in place.
- [ ] All user text filtered.
- [ ] Social rewards are bonuses only, shown after the first win, group join verified server-side; like and favourite rewards were re-checked against current policy or left out; no reward for an off-platform action; nothing about rewards, codes or giveaways in the title, thumbnail or description.
- [ ] Live game: retention read by source and by cohort before any system is added; loop-level problems sent to core-loop-tuning.md first.

## Sources

Accessed 2026-11-10; docs and DevForum threads re-checked 2026-11-11. "(read)" = opened (docs in the `Roblox/creator-docs` mirror, threads through the DevForum JSON endpoint); "(search summary)" = seen only through web search result text. Older sections come from `references/knowledge-base.md` sections 1.7, 1.8, 3.3 and 3.4 (grep `## 1.7`, `## 1.8`, `## 3.3`, `## 3.4`), which list their own sources.

Added 2026-11-26 (cadence, seasonal table, holiday calendar, season pass, resets, level-up rows; all accessed that day):

- Roblox APIs (read; raw pulls with UTC times kept in the research scratch folder): explore `get-sort-content` (five chart sorts) and `games.roblox.com/v1/games` (descriptions, `updated`) at 10:01 UTC; `apis.roblox.com/game-passes/v1/universes/<id>/game-passes?passView=Full` and `apis.roblox.com/developer-products/v2/universes/<id>/developerproducts?limit=50` for the top 35 at 10:07–10:15 UTC (the older `games.roblox.com/v1/games/<id>/game-passes` returned 404).
- Rolimons player history, https://www.rolimons.com/game/<placeId> (read 10:05 UTC; six-hourly samples to October 2026, then hourly). Seasonal medians use the 00/06/12/18 UTC samples of 22 established games; a live-event spike is an hourly sample at least 1.8× the one two hours earlier that falls 25% within three hours.
- create.roblox.com/docs (read 26 Nov 2026): `production/promotion/experience-events` (10-event limit, Trending Events rules, update announcements, Off-Platform Featuring eligibility and selection), `production/promotion/experience-notifications` (unchanged), `production/configs` (conditional configs and attributes), `production/experiments` (economy metrics, 14–60 days), `production/game-design/season-pass-design`, `production/game-design/content-updates`.
- DevForum (read): https://devforum.roblox.com/t/4995943 (Introducing Pass Free Trials, 18 Nov 2026), https://devforum.roblox.com/t/4988305 (Experiments custom metrics, 12 Nov 2026), https://devforum.roblox.com/t/4998199 (weekly recap, 20 Nov 2026).
- Roblox newsroom (read): https://corp.roblox.com/newsroom/2026/10/the-hollow-halloween-survival-event; The Great Build page https://www.roblox.com/games/98487757108234/The-Great-Build (description via the games API); Winter Spotlight https://corp.roblox.com/newsroom/2024/12/roblox-winter-spotlight (search summary).
- Event dates and mechanics (search summaries; guide sites disagree on times): Murder Mystery 2 Halloween 2026 https://timesaver.gg/blog/mm2-halloween-event and Christmas 2025 https://noleep.com/en/murder-mystery-2-snow-token-farming-guide-and-christmas-battlepass-rewards-overview; Blox Fruits Hellfire Halloween https://stealthygaming.com/blox-fruits-hellfire-halloween-event-patch-notes/ and Christmas 2025 https://rblxguide.com/games/blox-fruits/updates/update-29-1; 99 Nights Halloween https://rblxguide.com/games/99-nights-in-the-forest/updates/99-nights-trick-or-treat-update-2026 and Christmas 2025 https://www.pcgamer.com/roblox/99-nights-in-the-forest-christmas-update/; Adopt Me Halloween 2026 https://timesaver.gg/blog/adopt-me-halloween-event-2026 and Winter 2025 https://adoptme.fandom.com/wiki/Winter_Event_(2025); RIVALS Season 4 https://nerdschalk.com/rivals-season-4-release-date-changes/ and Season 2 https://roonby.com/2025/12/13/rivals-christmas-update-guide-new-codes-crystals-weapons-and-season-2/; Dandy's World 1.0 https://beebom.com/dandys-world-1-0-release-time-countdown/; Evade Halloween 2026 https://allthings.how/evade-halloween-update-roblox-wisps-and-spellbooks-in-the-event/; Forsaken Summer Games https://allthings.how/forsaken-summer-games-guide-every-reward-and-quest/; Bee Swarm Beesmas 2025 https://rowatcher.com/games/601130232; Grow a Garden Christmas 2025 https://techwiser.com/roblox-grow-a-garden-christmas-part-1-update/ and https://www.iggm.com/news/grow-a-garden-christmas-event-part-2-why-are-players-disappointed-leaving; Steal a Brainrot Christmas 2025 https://roonby.com/2025/12/24/christmas-admin-abuse-in-steal-a-brainrot-when-is-it-what-time/; Steal An Egg admin events https://progameguides.com/roblox/steal-an-egg-admin-abuse/; no 2026 platform winter event announced https://www.ofzenandcomputing.com/what-is-the-next-roblox-event-winter/.

- Roblox/creator-docs (read), https://github.com/Roblox/creator-docs/tree/main/content/en-us/ : production/analytics/retention.md and engagement.md; discovery.md and discovery-faq.md; production/promotion/experience-notifications.md with includes/experience-notifications/{eligibility,guidelines,delivery-system,implementation-create-notification-string}.md; production/promotion/experience-events.md; production/analytics/alerts.md, production/configs.md and production/experiments.md; production/game-design/season-pass-design.md and content-updates.md; production/publishing/badges.md; resources/feature-packages/; reference/engine/classes/GroupService.yaml (`PromptJoinAsync`), SocialService.yaml (`PromptRsvpToEventAsync`), ConfigSnapshot.yaml; production/game-design/design-for-roblox.md; reference/engine/classes/Player.yaml (`Idled`, 20-minute disconnect); production/promotion/experience-events.md (Off-Platform Featuring eligibility)
- DevForum threads (read): https://devforum.roblox.com/t/analytics-view-retention-by-acquisition-source-and-select-your-benchmark-set/4010157, https://devforum.roblox.com/t/analytics-track-new-user-retention-by-daily-and-weekly-cohort/3817030, https://devforum.roblox.com/t/do-daily-rewards-actually-keep-players-retention/3556728, https://devforum.roblox.com/t/low-engagement-on-new-game/3778071, https://devforum.roblox.com/t/how-effective-are-playtime-reward/3652644, https://devforum.roblox.com/t/suggestions-on-how-to-improve-d1-retention/4369566
- https://reddit.sentinel-team.org/posts/1sakqj4/snapshots/2026-04-03T05%3A12%3A52.21453Z (search-result text of an r/robloxgamedev post on a third-party mirror, not opened; the 3× D7 claim is unverified)
- https://devforum.roblox.com/t/4776239 (read 2026-11-11; a creator's report of an automated "scamming" action whose note lists inflating experience statistics; cause unconfirmed)
- https://www.sportskeeda.com/roblox-news/when-admin-abuse-start-grow-garden and https://www.gamepressure.com/newsroom/new-admin-abuse-date-in-grow-a-garden-you-get-to-decide-when-this/z78663 (search summary; admin-event timing)
- https://consolepcgaming.com/roblox-smashes-ccu-record-during-admin-war-between-grow-a-garden-and-steal-a-brainrot (search summary)
- https://beebom.com/admin-abuse-might-save-dying-roblox-games-but-hurts-them-in-the-long-run (read 2026-11-11; opinion piece, 13 Jan 2026)
- https://roonby.com/2025/09/24/why-rogueblox-was-closed-full-explanation-whats-next/ (read 2026-11-11; a blog's summary of the developers' statement)
- https://www.psu.com/news/the-cheap-trick-roblox-devs-use-to-keep-dead-games-alive/ (search summary; milestone codes)
- https://jens.substack.com/p/gamification-of-user-engagement and https://gag.gg/guides/seed-restock-and-values (search summary; offline growth, restock timer)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/38 Live Ops Deep Dive/Event Calendars and Content Planning.md`, `…/Battle Pass and Season Design.md`, `…/Feature Flags and Staged Rollouts.md`, `…/Patch Notes and Player Communication.md`, `…/Economy Resets and Seasonal Wipes.md`, `…/Limited-Time Offers - Design and Ethics.md`, `LihFolk Vault V2/10 Game Design and Genres/Retention and Return Hooks.md`, `…/Core Loops and Session Design.md`, `…/Social Design and Multiplayer Play.md`, `…/Ethical Design and Player Trust.md`, `LihFolk Vault V2/27 Marketing and Growth/Update Cadence and Hype Cycles.md`, `LihFolk Vault V2/49 Roblox Platform Features/Experience Notifications and Return Prompts.md` (read). Ideas adapted and rewritten; code is our own.
