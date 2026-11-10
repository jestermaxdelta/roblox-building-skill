# Analytics, discovery and the Roblox platform

Distilled from knowledge-base sections 3.1, 3.9, 3.10 and 3.11, re-checked against the creator docs on 2026-11-10. Use it to plan the analytics event schema, read Creator Analytics, set up experiments and Configs, and design for Recommended For You, search, thumbnails and matchmaking. In level-up mode it is the reference for reading a live game's numbers: `references/audit-existing-game.md` holds the triage order and benchmark table, `references/growth-and-marketing.md` holds ads, creators and community. Most platform numbers here are version-sensitive `[VS]`; re-check https://create.roblox.com/docs and the owner's vault (`Roblox Research/2026-11 Market Scan/`, snapshot 2026-11-07) before quoting them.

## Platform facts that shape design `[VS]`

- Mobile is the majority; Android is about 65% of players, most on 2–4 GB phones (see performance.md).
- 13+ players outnumber under-13 players. 64% of DAU were age-checked in Q3 2026. Q3 2026 DAU was about 138 million (−9% year on year). The concurrent-user record was 47.4 million on 23 August 2025 (one source says 47.3).
- Home is over 90% of traffic, about 10.5 billion impressions a day. Discovery, not search, decides who sees you.
- Players sort into "tourists" (try, bounce) and "locals" (return daily). Fun must land within 5 minutes or the tourist is gone.
- Appointment timers you pay to skip are downvoted; players accept honest waits with free alternatives.
- Wave lifecycle: hits peak in 7–8 weeks, plateau for 2–5 months, then fall 90–99% within 6–12 months.
- Age tiers and reach: Kids (5–8) see Minimal and Mild content; Select (9–15) adds Moderate; 16+ sees everything except Restricted. To reach under-16 audiences a creator must be ID-verified with 2FA, complete the questionnaire, hold Plus/Premium for 2 months or pay a 1,000 R$ refundable fee, run a trial to 16+, and reach 250 engaged age-checked plays within 60 days (evaluated hourly); 50,000 R$ buys an expedited review. The docs disagree on the refund timing (90 days vs 25 engaged players kept for 60 days).

## Analytics: what to measure

Creator Analytics dashboards need more than 10 DAU and 10 play hours over 7 days. Benchmarks, Performance charts, alerts and insights need 100+ DAU; AI analytics reports 1,000+ DAU; feedback reports 20+ comments `[official][VS]`.

Benchmarks `[official]`: the comparison set is games with similar players, else the same genre, else all experiences, drawn only from games with 100+ DAU, refreshed daily, and it changes as the game grows (the chart is annotated when it switches). Shown as the P50–P90 range (P10–P50 where lower is better) for all retention KPIs, average session time, conversion rate, ARPPU, ARPDAU and play-through rate. Overall KPIs (DAU, revenue, playtime) compare against Top 200 / 500 / 1000 tiers of the top 1,000 games by 30-day playtime. Benchmarks never affect ranking. The doc's D1 example range (12.11–18.73%) is an illustration, not a platform figure.

| KPI | Meaning | Why it matters |
|---|---|---|
| PTR (play-through rate) | Impressions that become plays | Top Recommended For You signal |
| Bounce | Sessions under 60 s, and 61–180 s | Negative signal; onboarding and performance |
| Play days D1 / D2–7 / D8–28 | Days a user returns in each window | Core ranking signals since June 2026 |
| Playtime | Capped at 60 min per user per day | Beyond the cap adds nothing to ranking |
| Co-play days | Days a user played with friends | Important signal |
| Qualified sessions, spend days, Robux per user | Engagement and monetization | Important signals |
| ARPDAU = conversion × ARPPU | Revenue per daily user | Diagnosis |
| LTV ≈ ARPDAU × Σ retention | Lifetime value | Sets the max you can pay per install |

Diagnosis: high ARPPU but low ARPDAU means few payers, so add a starter pack after the first win. Low D1 is core loop, onboarding or performance. Low D7 is a progression wall. Low D30 is endgame or social. Fix retention before monetization. The full ordered triage is in audit-existing-game.md §4.

Reading traps `[official]`:

- Retention charts are keyed to the first-play date. "D7" means the player returned on the 8th day; the newest D7 and D30 cohorts are empty until the days pass. Use the daily (10 days) and weekly (10 weeks) cohort tables to judge an update or campaign.
- A retention dip after a traffic influx is normal; so is a PTR dip while impressions rise.
- The New User First Session Retention chart (share still playing after X minutes, this period vs last) is the fastest onboarding alarm: a drop at minute 5 after an update points at a new step, an error or a performance regression.
- Engagement, retention and PTR differ by acquisition source. Compare like with like in Acquisition → new users funnel (users with plays, conversion rate, D7, 7-day playtime, 30-day payer conversion, 30-day revenue per user), by source or by share link.

Other dashboards worth a weekly look `[official][VS]`:

| Dashboard | What it answers |
|---|---|
| Acquisition → Home Recommendations | Impressions, plays and every ranking signal by window (D1, D2–7, D8–28) with benchmarks; start here when impressions move |
| Monitoring → Performance | Client FPS, crash rate, out-of-memory exits, memory %, CPU time; server frame rate, CPU, memory by age; break down by platform and by **Place Version** to catch a regression from the last publish |
| Configurations → Alerts | Up to 20 alerts per experience on any performance or data-store metric, fixed threshold or period-over-period, delivered to a webhook |
| Audience → Feedback | Up/down vote trend and player comments (from 2025); a downvote spike dates a bad update |
| Thumbnails → Home Page tab | Impressions, qualified plays, average playtime and qualified PTR per active thumbnail |

Open Cloud `[official][VS]`: the Analytics Query API (`/analytics-query-api/v1/universes/{id}/metrics`) returns the same metrics with breakdowns and filters, and the experimental Benchmarks API (`/analytics-benchmark/v1/universes/{id}/benchmarks`) returns the P10/P50/P90 benchmark series; both use the `universe.analytics:read` scope, which the Studio MCP exposes through `open_cloud_invoke`. Standard metrics go back 4 years, performance metrics 28 days. Metric names are listed in audit-existing-game.md §1.

## Event API and limits `[VS]`

All events are server-side, only in published games, and logged after the action succeeds:

- `AnalyticsService:LogOnboardingFunnelStepEvent(player, step, stepName)`
- `AnalyticsService:LogFunnelStepEvent(player, funnelName, funnelSessionId, step, stepName)`
- `AnalyticsService:LogEconomyEvent(player, flowType, currency, amount, endingBalance, transactionType, itemSKU?, customFields?)`
- `AnalyticsService:LogCustomEvent(player, name, value?, customFields?)`
- `AnalyticsService:LogJourneyEvent(...)`

Limits: 120 + 20 × CCU events per minute; 10 funnels with 100 steps each; 10 resource types; 20 transaction types; 100 SKUs; 100 custom event names; 3 custom fields per event (`Enum.AnalyticsCustomFieldKeys.CustomField01.Name`); 8,000 unique field-value combinations; 90-day roll-off. Transaction types: IAP, TimedReward and Onboarding are sources; Shop and Gameplay can be either; ContextualPurchase is a sink. Prefer one event name with fields over many names.

Standard schema (see templates/analytics-event-plan.md):

- Onboarding funnel: 1 Spawned, 2 FirstAction, 3 FirstReward, 4 FirstUpgrade, 5 FirstWin, 6 SawGoals, 7 Session2Start.
- Shop funnel (GUID per open): Opened, ViewedItem, PromptShown, Purchased.
- Offer funnel: Shown, Viewed, Prompted, Purchased, with CustomField01 = trigger.
- Rewarded video funnel: Offered, Started, Completed, Rewarded.
- Economy: every earn and spend of each currency with the item SKU.
- Custom: RoundEnded (value = duration), Rebirth (value = count), ServerLowMemoryWarning.

## Experiments and Configs `[VS]`

- Experiments run 14–60 days with 2 variants plus control, a percent rollout and a metric set (D1, D7, playtime, ARPU, ARPPU, payer conversion, session time). Early-harm detection refreshes playtime, payer conversion and ARPU every 5 minutes in the first 24 hours. Roblox recommends a simple 50/50 on a large rollout; watch the minimum detectable effect. Under 1,000 DAU the statistical power is weak. A result is significant when the confidence interval excludes 0.
- High-value experiments: offer grace 10 vs 20 minutes; offers per session 2 vs 3; starter-pack trigger; 29 vs 49 R$ for the 10-minute boost; rewarded-video placement; hint delay 5 vs 10 s; starting currency.
- Configs: `ConfigService:GetConfigAsync()` or `GetConfigForPlayerAsync(player)` returns a snapshot with `GetValue(key)`; connect `UpdateAvailable` and call `Refresh()`. Limits: 1,000 configs, 100,000 JSON characters. `SetTestingValue` for Studio. Make every tunable (prices, timers, offer gate numbers, drop rates) a config key with a safe code default. A new value is staged first (visible only in Studio sessions), then "Publish now" reaches players in about 15 s–1 min, or "Publish over 15 min" rolls it out gradually; History → Restore re-stages the previous value `[official]`. (Correction: an earlier version of this file said "about 5 minutes"; clients may still take a few minutes to reflect a publish.) Configs and experiments can target by country, tenure and spender tier.
- Matchmaking experiments: one at a time, 3 variants, 100% rollout.

## Recommended For You `[VS]`

The system retrieves candidates and then ranks them per user. Ranking counts only organic Recommended For You users, and it uses per-user averages, not totals.

- Most important signals: PTR, bounce, play days, playtime (capped).
- Important: co-play days, qualified sessions, spend days, Robux per user.
- 2026 changes: 9 March deep PTR; 26 March "Not interested" button; 15 June 28-day window with split D1 / D2–7 / D8–28 signals and a qualified-PTR split; 12 October measurement pipeline change, so PTR before and after is not comparable. Signals lag about 24 hours; impression changes take days.
- Exposure reducers: giveaways and incentivised engagement, mismatched metadata, near-duplicate clones, policy violations. Paid ads do not hurt organic ranking.
- The genre setting is changeable once every three months and is not a ranking input.

Thumbnails and metadata:

- Custom 16:9 thumbnails at 1920×1080 under 3 MB are required for Home. Up to 10 thumbnails; keep 2–5 active so personalization can pick (average +8.5%, up to +50%). Video thumbnails: 3 uploads per month, authentic gameplay only, not shown on console or VR.
- Icon 512×512; check readability at 150 px. Shift+P gives a free camera for captures.
- Market rules: show the first minute of play, one focal point, at most 5 elements, a big number, a visible climb in one frame, readable at 150 px, genre colour coding, a face, fill all 5 slots. Title pattern is a status tag plus a verb phrase (for example `[UPD 🔫] Realistic Ragdoll Playground 🩸`). Copy the format, not the art.
- Description hook in the first 160 characters.

Growth plan. Lower-risk: launch in a seasonal window, fill thumbnails and metadata, run a weekly update day, measure PTR and bounce daily. Bold: pay 50,000 R$ for an expedited under-16 review, launch with an influencer plus an admin event, and buy Ads Manager traffic with `max cost per play ≈ ARPU 30d + rewarded-video earnings per user + Audience Expansion share`. Attribution windows are 30 days (click) and 7 days (view).

## Scaling, safety and matchmaking `[VS]`

- Platforms: PlayStation, Xbox, Android, iOS, PC, Mac, Meta Quest. Automatic translation covers text and chat when the player enables it; set supported languages in Localization. Icon-led UI travels better than text. Holidays are not universal; pick event themes that travel.
- Safety: filter all user text; monitor user creation; for under-18 audiences avoid private-space settings and add bounding-box limits on beds; `Players:BanAsync` detects alt accounts; gate high-trust features on `Player:IsVerified` or account age. The safety dashboard needs 1,000+ daily hours.
- Matchmaking: server score = Σ(signal score 0–1 × weight). Built-in signals: Estimated Player Latency, Has Friends, Is Voice Chat Enabled, Player Age, Player Device Type, Player Language, Player Play History, Server Occupancy, Player Text Chat Group. Custom signals come from data-store attributes (skill rating, level band). Social games weight Friends and Occupancy highest; competitive games add a skill signal and Latency; keep Player Age and Text Chat Group on for mixed audiences. Lower-risk: raise only Friends and Occupancy. Bold: a custom skill or veteran-mix signal under a matchmaking experiment, watching D1 daily.

## Launch checklist (discovery and analytics)

- [ ] Five custom thumbnails, icon tested at 150 px, title with status tag, description hook under 160 characters, genre set.
- [ ] Onboarding funnel, shop funnel, offer funnel and economy events live in a published test place first.
- [ ] Configs for every tunable; Experiments planned for the two riskiest numbers.
- [ ] Bounce under 60 s measured on a low-end phone before launch.
- [ ] Content-maturity questionnaire answered; age-tier plan chosen (16+ first, then under-16 after 250 engaged plays).
- [ ] Launch date inside a seasonal window, ideally a Saturday; weekly update day announced.
- [ ] Share links, invite prompt and referral banner wired.

Grep `references/knowledge-base.md` for `## 3.1`, `## 3.9`, `## 3.10` and `## 3.11`.
