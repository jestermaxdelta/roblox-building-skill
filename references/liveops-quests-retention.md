# LiveOps, quests, retention and social design

Distilled from knowledge-base sections 1.7, 1.8, 3.3 and 3.4, plus a 2026-11-10 research pass on retention systems, notifications and LiveOps practice. Use it when planning onboarding, quests, season passes, events, update cadence and social features, and when a live game's D7, D30 or play days sit below benchmark. Loop-level diagnosis (first session, session time, D1) is in core-loop-tuning.md. Tags: `[official]` Roblox docs, `[community]` forum, press or third-party practice, `[VS]` version-sensitive, `[house]` house estimate.

## Onboarding (first session)

Three goals: teach the loop, make it fun fast, make the player want to return.

Blueprint:

1. Spawn directly into the loop. No lobby, no wall of text.
2. First reward in under 30 seconds; first upgrade within 1–2 minutes.
3. One verb at a time. Introduce the second mechanic only after the first has paid off.
4. Contextual, show-once tutorials. Visual guidance (arrows, glowing targets, signs) is modelled in Blender, not drawn with primitive Parts. If a hint is timed, fire it at about 11 seconds, because most players who will act have done so by 10 seconds.
5. Log every step with `AnalyticsService:LogOnboardingFunnelStepEvent(player, step, stepName)` and watch the funnel for the step with the largest drop.
6. A visible goal ladder (next upgrade, next zone) is on screen from the first minute.
7. Ask for notification opt-in only at a warranted moment (after a win, before a timed event), never on join.
8. No offers, starter packs or purchase prompts during onboarding (house rule).

## Social rewards (group join, like, favourite, friend join)

Every 2025–26 hit rewards them (Steal An Egg gives 10K free Speed for like + favourite + group join; Climb For Animals Eggs the same). They are part of the house default set. The creator docs do not cover in-game rewards for them; what the docs do penalise is *metadata* that leads with giveaways, Robux or "like for rewards" and thumbnails that do not match the game `[VS]`. Build them like this:

- **Bonus, never a gate.** The reward is a one-time boost or cosmetic (a 10–15 min 2× boost, a starter cash bump, a badge, a skin), never progress, a zone, a product or a core feature. A player who never joins loses nothing they need.
- **Timing.** Show the "Join our group" card after the first win and after the 600 s grace, as one of the rate-limited cards from the offer gate (it counts toward the ≤ 3 cards per session). A permanent small "Rewards" button in the HUD lets the player claim later.
- **Group join is the only one Roblox can verify.** Check it on the server with `Player:IsInGroup(groupId)`; the result is cached per session, so after the player joins the group offer a "Check again" button that calls `GroupService:GetGroupsAsync(player.UserId)` (not cached, rate-limited; `pcall` it and retry once). Grant once, save the flag in the profile.
- **Likes and favourites cannot be verified** (no API returns them). Treat the "I liked it" claim as honour-based: grant a small reward once per account via the same claim flow, and accept that it is a thank-you, not a verified action. Never block anything on it.
- **Friend join and invites** are verified: `Player:GetJoinData().ReferredByPlayerId` for invites, friend presence for co-play. Pay the friend bonus (10–20%) to both players while they are in the same server; never require invites to progress.
- **Copy.** The card says what the reward is and that it is optional. No countdown, no "limited", no fake scarcity. Nothing about it in the title, thumbnail or description.
- **Instrument it.** Funnel: RewardsOpened → GroupPromptShown → GroupVerified → Claimed. If GroupVerified is below about 15% of shown, the reward is too small or shown too early.

## Retention benchmarks `[VS]`

Use Creator Analytics' similar-game benchmark first, then these published figures:

| Source | D1 | D7 | D30 | Notes |
|---|---|---|---|---|
| gstack (classic mobile) | 40% | 15% | 5% | Not Roblox-specific; aspirational |
| GameAnalytics 2025, Roblox median | 4.3% (sessions under 3 min) to 11.5% (sessions 19–24 min) | 1.6% median, 8.5% at P98 | — | Session length predicts retention |
| RoWatcher, July 2026 | Obby 25–35; tycoon 20–28; shooter 22–30; roleplay 15–22 | — | — | Genre D1 ranges for games with traffic |
| Creator Analytics | 50th–90th percentile shown per genre (docs example D1 12.11–18.73%; a DevForum announcement example shows 12.4–24.1%) | — | — | Needs 100+ DAU; illustrative, each game gets its own range |
| GameAnalytics 2026, 500+ titles above 1M MAU (Aug 2025–Jul 2026) | Median 10.3%; P25 8.4%; P75–P90 12.9–15.9%; P99 22.2% | Median 1.6%; P25 1.0%; P99 9.1% | Median 0.5%; top 1% 4.7% | `[community]`, read through search summaries; large titles only |

The sources disagree because they measure different populations. Treat them as ranges, and compare yourself to your own genre benchmark in Creator Analytics. Conflict: the RoWatcher genre ranges (20–35% D1) and the common "20% is good, 40% is excellent" rule sit far above the GameAnalytics medians; the 2026 report attributes such figures to small samples of already-promoted games. Do not set targets from them.

Reading the retention pages `[official]` `[VS]`:

- Break D1, D7 and D30 down by **Source** (added October 2025). Judge design changes on the Home Recommendations cohort; ad and external-link cohorts retain differently, and a dip after a large influx is normal.
- The cohort table shows daily cohorts over their first 10 days and weekly cohorts over 10 weeks, with 7-day playtime, 7-day payer conversion and 7- and 30-day revenue per user. Use it to compare players who first joined during an event or update with those before it.
- Recommended For You reads signals in stages: first session (play-through rate, bounce), then D1, D2–7 (play days out of 6), D8–28. A strong D8–28 with a weak D1 is very unlikely, so fix in that order.

Diagnosis rules: low D1 means core loop, onboarding or performance; session time at benchmark with low D1 means there is no stated reason to return; low D7 means a progression wall or empty mid-game; low D30 means no endgame or social reason to stay. Fix retention before adding monetization. The metric-by-metric table with experiments is in core-loop-tuning.md §5.

## Retention toolkit (no punishment anywhere)

Order of work: the loop first, then these. `[community]` Developers who post results say reward layers amplify a working loop and do not rescue a weak one: a game with 4-minute sessions reported no change from adding daily rewards, and a DevForum reply argues that "most of the D1 retention is solely based on your core loop", with daily rewards as secondary amplifiers. No published before/after data was found for indexes, rebirth pacing, season passes or notification opt-in; those rows rest on market pattern and house reasoning.

| System | Done right | Evidence | Limits `[VS]` |
|---|---|---|---|
| Daily reward | Cumulative calendar counting days played; never resets. One-tap claim inside the HUD, not a join pop-up. The reward feeds the player's current goal (a boost, upgrade material), with marquee items on day 7 and day 28 anyone can reach. If a streak exists, grant free freezes and drop a few tiers on a miss, never to zero | `[community]` Opinion on streaks is split; one unsourced Reddit case claims about 3× D7; the "30–50% D7 lift" figures on script-seller pages have no source | The Engagement Rewards package's `Daily` type is a login streak; handle a missed day yourself. No guilt or "streak ends soon" notifications |
| Playtime reward | A ladder at about 5, 10, 20 and 40 minutes that accumulates per day, not per session, so leaving loses nothing. Stop at 60 min. Pay on active play | `[community]` Holds players in a session; does not by itself bring them back | Playtime beyond 60 min per user per day adds nothing to ranking `[official]`. `Player.Idled` (client-only) fires about 2 min after input stops, then every 30 s; Roblox disconnects after 20 min idle `[official]` |
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
| Codes | A dated code in each update log; a milestone ladder (likes, visits) that rewards the community for pushing a counter. Rewards are boosts or cosmetics | `[community]` One press piece: a milestone code buys about a weekend of extra players and a like-ratio bump, not a revival | Nothing about codes, likes or giveaways in the title, thumbnail or description: "leading with giveaways" reduces exposure `[official]` |

Saturdays and December are the peak weeks for Recommended For You traffic; schedule big updates for them.

## Notifications done right `[official]` `[VS]`

- **Who can receive:** opted-in users aged 13+. The game needs 100+ visits and must not be under moderation.
- **Asking:** `ExperienceNotificationService:CanPromptOptInAsync()` in a `pcall`, then `PromptOptIn()`, from a LocalScript. The prompt text is fixed. It does not appear for under-13s, for users already opted in, or within 30 days of the last prompt, so spend it at a moment that warrants a later message: the player has just started something that finishes while they are away ("your egg hatches in 2 hours"). Never on join.
- **Throttle:** one notification per user per day from a game, on top of the user's own daily total across games. Delivery is not guaranteed, and reach rises or falls with how much users engage with your notifications.
- **Content:** personalised to in-game activity and immediately actionable. Docs' good examples: "Your gold goose egg has hatched!", "You're 2 races away from completing the weekly challenge!". Docs' banned or bad examples: generic advertising ("A new line of race cars just dropped"), purely informational messages, disguised ads, false time pressure, bait-and-switch free items, and links that open a pre-loaded purchase.
- **Never** make opting in a condition of playing or progressing.
- **Routing and measurement:** launch data (read with `Player:GetJoinData()`) takes the player to the thing the message was about; an analytics category per message type lets the dashboard compare them. A notification that mentions another user is delivered only if the two are friends.
- **Sending:** server-side through the Open Cloud package (`createUserNotification(userId, { payload = { messageId, type = "MOMENT", parameters, joinExperience = { launchData }, analyticsData = { category } } })`) or the Open Cloud API, using a notification string created in the Creator Dashboard.

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

## Season pass worked plan

- Length about one month, then a one-week rest. 10 tiers. The premium track is a superset of the free track.
- 28-day season, 600 XP per active day, 16 active days expected = 9,600 XP.
- Tier thresholds: 500, 650, 750, 850, 950, 1,000, 1,050, 1,150, 1,250, 1,400 (cumulative 9,550), so a typical active player finishes with a small margin.
- Feature packages `[VS]`: Missions, Season Passes (beta; `SeasonPasses.addProgressToSeason()`), Engagement Rewards (`rewardClaimedHandlerFunction()`), Bundles (never prompt a StarterBundle on `PlayerAdded`; use the offer gate after the first win).

## Update and event cadence

- Content updates should take under 3 weeks of effort each. Weekly is ideal, monthly is the minimum. Expansions take months; plan them separately.
- Roblox retention guidance: a small update every 2–4 weeks, a big one every 2–3 months.
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

## Social design

- Intentional co-play (friends joining together, parties, shared plots) counts toward the co-play discovery signal; random matchmaking does not.
- Friend bonus of about +10% income or XP when playing with a friend is a cheap, honest co-play incentive.
- Server sizes: 6–12 for co-op gameplay, 20–30 for hubs and hangouts. Set from playtest data.
- Waiting time for a match or round under 30 seconds; show something to do while waiting.
- Griefing controls: build-zone ownership, personal plots, report buttons, cooldowns on destructive actions.
- Social friction audit: for every social feature, list how a stranger could ruin it and what stops them.
- Filter all user-visible text with `TextService:FilterStringAsync`.
- Server Luck or server-wide gifts show a thank-you banner naming the buyer (a social reward that costs nothing).
- Social service APIs: `SocialService:CanSendGameInviteAsync` → `PromptGameInvite(player, ExperienceInviteOptions)` with `LaunchData` up to 200 characters read through `GetJoinData()`; referrals through `ReferredByPlayerId`; `ExperienceNotificationService:CanPromptOptInAsync()` / `PromptOptIn()` with a 30-day re-prompt lockout; notifications need 100+ visits, one per user per day, 13+ opted-in users `[VS]`.

## Checklist

- [ ] First reward under 30 seconds, first upgrade under 2 minutes, onboarding funnel logged.
- [ ] Goal ladder visible from minute one.
- [ ] Daily, weekly and seasonal content with real end dates.
- [ ] Event currency per event; one KPI per event.
- [ ] Weekly update day chosen and announced.
- [ ] Notification opt-in prompt only at warranted moments.
- [ ] Co-play incentives (friend bonus, party join) in place.
- [ ] All user text filtered.
- [ ] Social rewards are bonuses only, shown after the first win, group join verified server-side, nothing about them in the title, thumbnail or description.

Grep `references/knowledge-base.md` for `## 1.7`, `## 1.8`, `## 3.3` and `## 3.4` for the source text.
