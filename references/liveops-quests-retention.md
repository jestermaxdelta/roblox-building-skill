# LiveOps, quests, retention and social design

Distilled from knowledge-base sections 1.7, 1.8, 3.3 and 3.4, plus a 2026-11-10 research pass on retention systems, notifications and LiveOps practice. Use it when planning quests, daily rewards, season passes, events, notifications, update cadence and social features, and when a live game's D7, D30 or play days sit below benchmark. The first session is owned by tutorial-and-onboarding.md; loop-level diagnosis (session time, D1) by core-loop-tuning.md. Tags: `[official]` Roblox docs, `[community]` forum, press or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production game, its other figures are rules of thumb dated October 2026), `[VS]` version-sensitive, `[house]` house estimate.

## Start here by level

Terms: **LiveOps** = everything done to a game after launch (updates, events, offers, communication). A **return hook** is a reason to come back at a specific time, built in on purpose. **Play days** = the number of distinct days a player returns in a window. A **season pass** (battle pass) is a time-limited reward track climbed with season XP. A **kill switch** is a Config boolean that turns a risky system off without a publish.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | The first-session script in tutorial-and-onboarding.md §2 first. Then one cumulative daily calendar, 3 daily quests and capped offline earnings from the toolkit. One fixed update day you can keep. An in-game What's New panel. Real end dates on everything | Season passes, admin events, notifications, staged rollouts |
| Intermediate | The calendar method: measure throughput, plan mostly config and reskin events, one buffer week a month, a one-page brief per event. Notifications at warranted moments. The T-10 to T+7 timeline. Read each update's curve | Per-flag percentage rollouts; seasonal resets |
| Expert | Calendar and patch notes as validated Config data; staged rollout with written abort criteria; season XP budget with 15–20% slack and boundary-purchase rules; notification scheduling when no server is running; lazy season rollover; reviews that feed the next quarter's capacity numbers | — |

Contents: Onboarding (pointer) · Social rewards · Reading retention · Retention toolkit (daily rewards, playtime gifts, offline, AFK) · Notifications · Quests · Season pass · Cadence and seasons · LiveOps calendar (capacity, event types, overlap rules, calendar as data, event brief, timeline) · Update-day ritual · Shipping an update · Patch notes · Resets · Social design · Level-up table. Related (implementation): gameplay-systems-cookbook.md §6 Quests and achievements, §7 Daily rewards and playtime rewards, §8 Codes, §24 Server-wide events and boosts.

## Fast routes

For a common task, read only these sections, in this order; the last one is the gate to pass. §N is the section numbered N in that file; quoted names are exact headings (trailing `[tags]` omitted).

| Task | Read |
|---|---|
| Nobody returns (D7, D30) | "Level-up: retention symptoms → likely cause → fix", "Reading retention", "Retention toolkit (no punishment anywhere)", "Social design"; `economy-and-progression.md` "Level-up: economy symptoms → likely cause → fix", "Time to afford: price everything from one income model"; this file "Review gate" (about 156 lines) |
| Daily rewards, playtime gifts, quests | "Retention toolkit (no punishment anywhere)", "Quests and missions", "Notifications done right", "Social rewards (group join, like, favourite, friend join)"; `gameplay-systems-cookbook.md` §0, §6, §7; this file "Review gate" (about 149 lines) |
| Events, season pass, update plan | "Update and event cadence", "LiveOps calendar: from capacity to dated events", "Season pass", "Patch notes and player communication", "Resets, seasons and wipes", "Review gate" (about 273 lines) |

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
| Update cadence | A fixed day players can count on (Brookhaven Fridays, Dress To Impress and Grow a Garden Saturdays) | `[official]` small update every 2–4 weeks, big every 2–3 months. `[community]` Rogueblox's team said a weekly schedule blocked larger features and burned them out before the game closed | Update announcements: 60 characters, at most once every 3 days `[official]` |
| Friend and co-play hooks | Boost for both players while together; shared goals; cheap or free private servers; invite prompt with launch data that drops the friend next to the inviter | `[official]` Intentional co-play days (joins, invites, private servers) are a ranking signal; the design guide warns against pricing private servers out of reach | Never require invites to progress |
| Notifications | See the next section | `[official]` rules; no public opt-in or lift figures found | 13+, opt-in, one per user per day |
| Offline progress | Capped, the cap stated, claimed through a welcome-back panel that also shows one new thing | `[community]` Analyses of Grow a Garden name offline growth as its return trigger | Nothing is lost while away (house) |
| AFK areas | Prefer none. If the genre expects idle earning, pay the same capped rate offline, so closing the app costs nothing | Pay-to-idle lifts session time without return days; see the playtime row | 20-minute idle disconnect `[official]`; no Roblox rule on AFK rewards was found |
| Timers and restocks | Global, predictable timers (spawns every 5–15 min, server events every 30 min), next time shown | `[community]` Grow a Garden's shop restock is reported as a global 5-minute timer that players track | Missing one never costs progress |
| Codes | A dated code in each update log; a milestone ladder on visits or group members that rewards the community for pushing a counter (a likes ladder rewards likes, which is the risky pair above: prefer visits). Rewards are boosts or cosmetics | `[community]` One press piece: a milestone code buys about a weekend of extra players and a like-ratio bump, not a revival | Nothing about codes, likes or giveaways in the title, thumbnail or description: "leading with giveaways" reduces exposure `[official]` |

Saturdays and December are the peak weeks for Recommended For You traffic; schedule big updates for them.

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

`[official]` starting values (season-pass design guide): about one month, at least a week of rest between seasons, automatic enrolment in the free track, daily missions across three or more categories that never need hard currency, premium as a superset, mid-season upgraders receive premium rewards for every tier already reached, claim by button with unclaimed rewards granted at season end, a retired final reward shown as a 3D model in the world (a Blender showcase piece), double XP in the final week. About 10 tiers is a `[house]` starting count; the guide gives none.

XP budget. Tune for a named target player, then leave slack:

`expected XP = season days × share of days played × XP per play day`; set the last tier at **80–85%** of that `[lihfolk]`.

Worked plan: 28 days; target player active 4 days a week = 16 play days; 3 daily missions at 100, 150 and 250 XP plus about 100 XP from play = 600 XP per play day; expected 9,600 XP. Ladder total about 8,100: tiers at 425, 550, 640, 720, 810, 850, 890, 980, 1,060, 1,190 (cumulative 8,115, 84.5%). Tier 1 lands in the first session.

Conflict: this file's earlier ladder (500 … 1,400, cumulative 9,550) left 0.5% slack, so one missed day put the target player out of reach. The 15–20% slack rule is the better default; the ladder above replaces it. Players who realise on day 20 that they cannot finish stop playing the pass altogether, and premium buyers who cannot finish feel cheated.

Structure and rewards `[lihfolk]`:

- **Premium on the same XP bar finishes early** (extra missions = faster XP), which is partly paying to progress and leaves premium players idle in week four. Cleaner: one bar, premium bonus missions, and a few premium-only bonus tiers (11–15) that absorb the extra XP. Avoid separate ladders; they are hard to explain to young players.
- **Slots:** tier 1 is an instant claim on both tracks. Early free tiers prove the pass works (currency, a potion, a small cosmetic). Premium tiers are cosmetics with visible flair; no stat power (house rule). The free track has its own smaller capstone. Premium tiers grant fixed items only: one crate or roll makes the whole premium pass a paid random item with odds and `PolicyService` duties `[VS]`.
- **Premium currency refund:** returning part of the price to finishers feels generous; do the arithmetic first, and never when that currency is also the main sink.
- **"Exclusive" is a promise.** If the final reward might ever return, call it "Season 3 reward", not exclusive.
- **Late joiners, cheapest first:** final-week double XP; a small bank of missed daily missions (cap about 3 days); weekly missions completable in two or three sessions. Paid tier skips turn the deadline into the product; house default is not to sell them.

Selling and edge cases `[lihfolk]` (implementation in data-and-purchases.md):

- Key everything on a season id that is never reused. Record premium ownership per season id in the profile, with the receipt id; one developer product recorded per season is simpler than a new game pass every month.
- **Boundary purchases:** a prompt opened at 23:59:50 and confirmed after the end still charges the player. Decide the rule in advance (hide the buy button for the last 10 minutes, or grant to the ended season and auto-claim everything reached). Every receipt resolves to a grant; never leave one unprocessed because a season ended.
- **Mid-season upgrade:** claimability depends on the tier reached, not on when premium was bought.
- **Double XP for one mission:** key completion by day number and mission id in the profile, so two servers or a teleport cannot both grant it.
- Feature packages `[VS]`: Missions, Season Passes (beta; `SeasonPasses.addProgressToSeason()`), Engagement Rewards (`rewardClaimedHandlerFunction()`), Bundles (never prompt a StarterBundle on `PlayerAdded`; use the offer gate after the first win).

## Update and event cadence

- `[official]` A content-cadence update should take under three weeks of effort; many games ship one every two weeks to a month, and a common rhythm is small updates every 2–4 weeks with bigger ones every 2–3 months. Anything that needs a new system is an expansion: plan it separately. Weekly is what the current top games do `[community]`, not a requirement.
- Each event has exactly one KPI and a unique event currency with its own sinks.
- Seasonal multipliers (market snapshot 2026-11-07 `[VS]`):

| Season | Window | Effect |
|---|---|---|
| Halloween | 10 Oct – 3 Nov | 2–3× for themed games; horror up to 4× on 28–31 Oct |
| Thanksgiving | Late Nov | 1.3–1.5× |
| Winter | 15 Dec – 5 Jan | 1.8–2.5× CCU, 2.5–3.5× revenue |
| Summer | 10 Jun – 20 Aug | 1.5–2×; launch new games 10–30 Jun |
| Back to school | Late Aug – Sep | 0.8–0.9× |

Recommendation. Lower-risk: a fixed weekly update day plus one monthly themed event with real dates. Bold: an admin-run live event every 2–4 weeks promoted through Experience Events (1,000 RSVPs puts an event on the Trending chart) `[VS]`; it drives spikes but needs reliable staffing and moderation.

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

**5. Fixed beats first.** Holidays for the countries that make up most of your players (check analytics; summer and school terms differ by hemisphere), your own anniversaries and visit milestones. Then layer the repeating rhythm. Repeating beats are what players learn; one-off beats are what they talk about.

**6. Write the overlap rules so they can be checked.** At most one headline event live at a time. Multipliers stack with a headline only by design, with a cap on the combined value. No major publish in a headline event's first 48 hours (fix by Config or kill switch). A season end and the next season's start never share a day. Event store offers end when the event ends and never return under another name.

**7. Respect the platform limits.** At most 10 ongoing or upcoming Experience Events, so public events are for beats worth an RSVP, not every rotation. The Off-Platform Featuring programme needs the event submitted at least 7 days before it starts, public and accurate, and the docs say the best featured events run 7–30 days `[official]`; put "submit for featuring" on the calendar as its own dated line. Trending Events needs 1,000 RSVPs and an event that started within the last 7 days, so publish headline events about a week ahead and collect RSVPs in the game: a LocalScript gets the event id from `SocialService:GetUpcomingExperienceEventsAsync()` and calls `SocialService:PromptRsvpToEventAsync(eventId)` when the player walks up to the countdown board (before the event starts only; never on join) `[official]` `[VS]`. Update announcements: 60 characters, one per 3 days.

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

### The update-day ritual as top games run it (and a solo version)

What current hits do `[community]` (press and fan coverage, 2025–26; times and frequency vary by source): Grow a Garden ships on Saturdays, and its lead developer runs an "admin abuse" session in public servers for roughly the hour before the update goes live (special weather, shop stock, NPC spawns); it is sometimes skipped when an update is mostly backend work. The August 2025 admin events of Grow a Garden and Steal a Brainrot coincided with the platform's concurrency record. Cautions from the same coverage: peaks are not sustained; one opinion piece says games that "barely touched twenty thousand" peaked above one hundred thousand players when an admin event went live, and argues that weekly spectacle makes ordinary play between events feel pointless; Rogueblox's developers said a weekly schedule kept them from building large features and burned the team out.

Platform tools `[official]` `[VS]`: Experience Events (at most 10 ongoing or upcoming; players tap Notify Me and get a stream notification at start, with optional push; the event can spawn joiners into a chosen place; `player:GetJoinData().GameJoinContext.EventId` identifies who came for it). Update announcements (60 characters, once every 3 days, sent to opted-in players; describe what is new, not "bug fixes"). Performance alerts with a webhook for the hour after publishing (crash rate, session time, concurrent users; 100+ DAU). Configs can start timed content at a set moment without a publish.

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
| Currency reset | Soft currency | Medium to high |
| Progress or full wipe | Levels, zones, items | High; after launch a last resort |

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
