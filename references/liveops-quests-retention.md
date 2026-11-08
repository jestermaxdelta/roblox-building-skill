# LiveOps, quests, retention and social design

Distilled from knowledge-base sections 1.7, 1.8, 3.3 and 3.4. Use it when planning onboarding, quests, season passes, events, update cadence and social features. `[VS]` marks version-sensitive facts.

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

Policy note: rewarding likes, favourites or group joins is a market pattern that the docs do not endorse. Treat it as a risk and never gate progress on it.

## Retention benchmarks `[VS]`

Use Creator Analytics' similar-game benchmark first, then these published figures:

| Source | D1 | D7 | D30 | Notes |
|---|---|---|---|---|
| gstack (classic mobile) | 40% | 15% | 5% | Not Roblox-specific; aspirational |
| GameAnalytics 2025, Roblox median | 4.3% (sessions under 3 min) to 11.5% (sessions 19–24 min) | 1.6% median, 8.5% at P98 | — | Session length predicts retention |
| RoWatcher, July 2026 | Obby 25–35; tycoon 20–28; shooter 22–30; roleplay 15–22 | — | — | Genre D1 ranges for games with traffic |
| Creator Analytics | 50th–90th percentile shown per genre (example D1 12.11–18.73%) | — | — | Needs 100+ DAU |

The sources disagree because they measure different populations. Treat them as ranges, and compare yourself to your own genre benchmark in Creator Analytics.

Diagnosis rules: low D1 means onboarding or performance; low D7 means a progression wall or empty mid-game; low D30 means no endgame or social reason to stay. Fix retention before adding monetization.

## Retention toolkit

- Cumulative login calendar (rewards never reset on a missed day) rather than a punishing streak. If you keep streaks, sell or grant streak freezes.
- Soft resets (rebirth, prestige, seasons) that keep cosmetics and meta progress.
- Capped, honest offline income (see economy-and-progression.md).
- Process goals ("deliver 10 parcels") beside outcome goals ("reach level 10").
- Real event dates with real ends. Weekly update day that players can count on (Brookhaven updates on Fridays, Dress To Impress on Saturdays).
- Opt-in notifications for events the player signed up for.
- In-world spawns every 5–15 minutes and server events every 30 minutes give players a reason to stay one more cycle.
- Saturdays and December are the peak weeks for Recommended For You traffic; schedule big updates for them.

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
- [ ] No progress gated on likes, favourites or group joins.

Grep `references/knowledge-base.md` for `## 1.7`, `## 1.8`, `## 3.3` and `## 3.4` for the source text.
