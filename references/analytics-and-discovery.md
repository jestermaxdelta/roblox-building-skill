# Analytics, discovery and the Roblox platform

Distilled from knowledge-base sections 3.1, 3.9, 3.10 and 3.11, re-checked against the creator docs and the staff announcements on 2026-11-11. Use it to plan the analytics event schema, read Creator Analytics, set up experiments and Configs, and design for Recommended For You, search, thumbnails and matchmaking. In level-up mode it is the reference for reading a live game's numbers: this file holds the one benchmark table; `references/audit-existing-game.md` holds the triage order, `references/growth-and-marketing.md` ads, creators and community, `references/icons-thumbnails-and-store-page.md` the craft of the tile, and `references/tutorial-and-onboarding.md` the onboarding funnel. Most platform numbers here are version-sensitive `[VS]`; re-check https://create.roblox.com/docs and the owner's vault (`Roblox Research/2026-11 Market Scan/`, snapshot 2026-11-07) before quoting them.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Upload 2–3 honest custom thumbnails (without one the game gets no Home impressions). 2. Log the seven onboarding funnel steps. 3. Each week read three numbers: first-play bounce, D1, average session time. 4. Put every tunable number in Configs | Experiments, custom dashboards, matchmaking weights, the ranking-signal table beyond its first four rows |
| Intermediate | Read the Home Recommendations signals in priority order; compare with the benchmark P50–P90; keep 3–5 thumbnails as distinct hooks; shop and offer funnels plus economy events; alerts by place version | Sub-point effects you cannot detect at your traffic (see sample sizes below) |
| Expert | Open Cloud analytics pulls, cohort and source splits, the CCU model, pre-registered experiments with minimum detectable effect and guardrails, thumbnail tests with confidence intervals | Nothing; rebaseline after every platform measurement change |

Terms: **impression** a tile shown on Home; **PTR** play-through rate, plays ÷ impressions; **qualified play** a play that lasts (filters accidental taps); **bounce** a first play ending inside 60 s or 61–180 s; **play days** days a user returns in a window; **cohort** users grouped by first-play date; **P50/P90** median and top-decile of the benchmark group; **MDE** minimum detectable effect, the smallest change a test can reliably see.

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

The CCU model `[lihfolk]` (an identity, so it always holds): `average CCU = sessions per day × average session minutes ÷ 1,440`. Sessions per day = new-user sessions (Σ over sources of impressions × play-through rate) + returning-user sessions (Σ over past cohorts of cohort size × retention on that day). Peak CCU is roughly 1.5–2.5× the daily average for a single-region audience (rule of thumb). Put your own dashboard values in a sheet and change one input at a time: in LihFolk's illustrative mid-size example a 50% rise in impressions moved CCU most, then session length, long-tail retention (days 8–30) and sessions per user, with a 20% PTR gain worth about as much as a good retention gain. Impressions cannot be bought organically; they are earned by the other inputs, which is why retention work pays twice.

Weekly review, eight lines `[lihfolk]`: Home impressions (7-day average) · PTR · new users per day by source · bounce (< 60 s, 61–180 s) · D1 and D7 of last week's cohorts · session minutes and sessions per user · average and peak CCU · changes shipped with dates. If CCU moved, the cause sits at the earliest line that also moved. Split every spike three ways: did impressions rise (ranking or ads), did PTR rise (art), or did returning sessions rise (update)?

Other dashboards worth a weekly look `[official][VS]`:

| Dashboard | What it answers |
|---|---|
| Acquisition → Home Recommendations | Impressions, plays and every ranking signal by window (D1, D2–7, D8–28) with benchmarks; start here when impressions move |
| Monitoring → Performance | Client FPS, crash rate, out-of-memory exits, memory %, CPU time; server frame rate, CPU, memory by age; break down by platform and by **Place Version** to catch a regression from the last publish |
| Configurations → Alerts | Up to 20 alerts per experience on any performance or data-store metric, fixed threshold or period-over-period, delivered to a webhook |
| Audience → Feedback | Up/down vote trend and player comments (from 2025); a downvote spike dates a bad update |
| Thumbnails → Home Page tab | Impressions, qualified plays, average playtime and qualified PTR per active thumbnail |

Open Cloud `[official][VS]`: the Analytics Query API (`/analytics-query-api/v1/universes/{id}/metrics`) returns the same metrics with breakdowns and filters, and the experimental Benchmarks API (`/analytics-benchmark/v1/universes/{id}/benchmarks`) returns the P10/P50/P90 benchmark series; both use the `universe.analytics:read` scope, which the Studio MCP exposes through `open_cloud_invoke`. Standard metrics go back 4 years, performance metrics 28 days. Metric names are listed in audit-existing-game.md §1.

## Benchmarks: one table

Snapshot 2026-11-10 `[VS]`. This is the one benchmark table for the skill; other references link here. Order of trust: (1) the game's own Creator Analytics percentile, always, when the owner can read it (100+ DAU); (2) rows marked **Drives triage**; (3) rows marked Cross-check; rows marked **Weak** are listed only so a quoted figure can be recognised and discounted.

| Metric | Value | Sample and source | Use |
|---|---|---|---|
| D1 retention (2026 report) | P25 8.4% · median 10.3% · P75 12.9% · P90 15.9% · P99 22.2% | GameAnalytics 2026 Roblox report: 500+ titles above 1M MAU, Aug 2025–Jul 2026; read through search summaries (figures as recorded in liveops-quests-retention.md) `[community]`. Large titles only, so a small game at the median is doing well | **Drives triage**: under 8.4% below; 8.4–12.9% near median; over 12.9% above. House launch target before paid traffic: above 11% `[house]` (market-scan-2026-11.md) |
| D7 retention (2026 report) | P25 1.0% · median 1.6% · P99 9.1% | Same 2026 report and sample | **Drives triage**: under 1.0% below |
| D30 retention (2026 report) | Median 0.5% · top 1% 4.7% | Same 2026 report and sample | **Drives triage**, coarse: under 0.5% below |
| Session length (2026 report) | Median 9.8 min per game · P99 21.1 min | Same 2026 report and sample (figures as recorded in economy-and-progression.md, search summaries) `[community]` | **Drives triage** for session time (T4b): under 6.6 min is low on either report; 6.6–9.8 min is below the current large-title median; house target 19+ min `[house]` |
| D1 by average session length (2025 report) | 0–3 min 4.3% · 7–12 min 7.9% · 13–18 min 10.2% · 19–24 min 11.5% (top 2% 32.3%; D7 median 1.6%, top 2% 8.5%) · 25+ min 10.8% | GameAnalytics 2025 Roblox report (aggregated titles, Jan 2023–Jul 2025), via the owner's vault. The vault copy has no 4–6 min row; interpolate between 4.3% and 7.9% and say so | Cross-check: is D1 low for the engagement the game already has? |
| Session length (2025 report) | Median 6.6 min · top quarter 14.5 min · top 10% 26.4 min | Same 2025 report, via the vault: all aggregated titles, so it sits lower than the 2026 large-title median | Cross-check only; superseded for triage by the 2026 row |
| Daily playtime per user (2025 report) | Median 16.8 min · top 10% 64.9 min | Same 2025 report, via the vault. Ranking counts at most 60 min per user per day `[official]` | Cross-check |
| Sessions of comparable hits | 14–27 min (vault sample of management and +1 games, one morning, 7 Nov 2026) | market-scan-2026-11.md; about 10 games | Weak: tiny sample, survivors only |
| D1 by genre | Obby 25–35% · tycoon 20–28% · shooter 22–30% · roleplay 15–22% | RoWatcher, July 2026: no sample or method stated; far above the measured medians | **Weak: never triage from it** |
| D1 dashboard example | P50–P90 12.11–18.73% (docs); 12.4–24.1% (a DevForum announcement) | Illustrations of how the dashboard displays a range `[official]`; each game gets its own | **Weak: not a benchmark** |
| D1 / D7 / D30 "40 / 15 / 5" | Mobile-industry rule of thumb | Not Roblox | **Weak: aspirational only** |
| PTR and first-play bounce | No public figure found | Roblox publishes none. The 12 Oct 2026 measurement change raised impression counts more than play counts: Roblox calls the PTR effect "a small decrease" `[official]`, creators in the vault report 26–40% drops `[community]` | Dashboard only; rebaseline after 12 Oct 2026 |
| Payer conversion, ARPPU, ARPDAU | No reliable public Roblox figure found | Dashboard benchmarks exist for all three `[official]` | Dashboard only; under 100 DAU compare with your own last month |
| Like ratio | Ad-running games median 79%; others 92% | Vault coding of Home feed tiles (72 + 177 tiles, 7 Nov 2026) `[community]` | House floor 85% before paid traffic `[house]` |
| Client crash rate | Investigate above 2–3%; Roblox's alert example fires at 5% for 5 minutes | Knowledge-base "Doc" value; alerts page `[official]` | **Drives triage** (T2) |
| Client memory | Memory-usage-percentage near 100% on a platform means out-of-memory exits | Performance dashboard page `[official]` | **Drives triage** (T2) |
| Server health | Frame rate 60; CPU time under 16 ms; memory under 50% of the server total, or under 3 GB | Performance dashboard page `[official]` | **Drives triage** (T2) |
| Thumbnail personalisation lift | +8.5% qualified PTR on average, up to +50% | Roblox's own test figure `[official]` | Expectation, not a target |

How to read one number against it: a D1 of 9% is "near median, lower half" on the triage row. The genre row would call the same game far below and the docs example would call it below P50; both are weak rows and are ignored. The session cut then asks a second question: if that game's average session is 13–18 min (bucket median 10.2%), its D1 is slightly low for its engagement, which points at return reasons rather than the first minute.

Conflict, resolved: the 2025 report (all aggregated titles, Jan 2023–Jul 2025) and the 2026 report (500+ titles above 1M MAU, Aug 2025–Jul 2026) are different samples, not a disagreement; that is why the median session reads 6.6 min in one and 9.8 min in the other. Triage uses the 2026 rows; quote any figure with its report year. The tracker's genre ranges do disagree with both; the 2026 report attributes figures of that size to small samples of already-promoted games, so the measured distributions are trusted.

## Event API and limits `[VS]`

All events are server-side, only in published games, and logged after the action succeeds:

- `AnalyticsService:LogOnboardingFunnelStepEvent(player, step, stepName)`
- `AnalyticsService:LogFunnelStepEvent(player, funnelName, funnelSessionId, step, stepName)`
- `AnalyticsService:LogEconomyEvent(player, flowType, currency, amount, endingBalance, transactionType, itemSKU?, customFields?)`
- `AnalyticsService:LogCustomEvent(player, name, value?, customFields?)`
- `AnalyticsService:LogJourneyEvent(player, journeyName, nodeName, journeySessionId?, customFields?)` for branching paths: 2–10 stages of 1–10 nodes, configured in Creator Hub first (tutorial-and-onboarding.md §9)

Limits `[official]`: 120 + 20 × CCU requests per minute; 10 funnels with 100 steps each; 10 resource types (currencies); 100 custom event names; 3 custom fields per event (`Enum.AnalyticsCustomFieldKeys.CustomField01.Name`). Soft caps, past which values are grouped as "Other": 20 transaction types, 100 item SKUs, 8,000 combined custom-field values. Limits reset daily; an event rolls off the dashboard 90 days after its last data. Transaction types: IAP, TimedReward and Onboarding are sources; Shop and Gameplay can be either; ContextualPurchase is a sink. Prefer one event name with fields over many names.

Standard schema (see templates/analytics-event-plan.md):

- Onboarding funnel: 1 Spawned, 2 FirstAction, 3 FirstReward, 4 FirstUpgrade, 5 FirstWin, 6 SawGoals, 7 Session2Start.
- Shop funnel (GUID per open): Opened, ViewedItem, PromptShown, Purchased.
- Offer funnel: Shown, Viewed, Prompted, Purchased, with CustomField01 = trigger.
- Rewarded video funnel: Offered, Started, Completed, Rewarded.
- Economy: every earn and spend of each currency with the item SKU.
- Custom: RoundEnded (value = duration), Rebirth (value = count), ServerLowMemoryWarning.

## Experiments and Configs `[VS]`

- Experiments `[official]` run 14–60 days with up to 2 variants plus control, a percent rollout and a metric set: the default (D1, D7, playtime, ARPU, ARPPU, payer conversion, session time), a rewarded-video set, or the default plus up to 3 custom metrics built from your own custom, economy and funnel events (for example per-user conversion on the last onboarding step). Nothing can be edited after scheduling. Playtime, payer conversion and ARPU refresh every 5 minutes in the first 24 hours (early harm), but a harm verdict needs 10,000 players enrolled across variant and control. Roblox recommends a simple 50/50 on a large rollout and says games under 1,000 DAU "might struggle to get useful data"; watch the minimum detectable effect. A result is significant when the confidence interval excludes 0.
- High-value experiments: offer grace 10 vs 20 minutes; offers per session 2 vs 3; starter-pack trigger; 29 vs 49 R$ for the 10-minute boost; rewarded-video placement; hint delay 5 vs 10 s; starting currency.
- Configs: `ConfigService:GetConfigAsync()` or `GetConfigForPlayerAsync(player)` returns a snapshot with `GetValue(key)`; connect `UpdateAvailable` and call `Refresh()`. Limits: 1,000 configs, 100,000 JSON characters. `SetTestingValue` for Studio. Make every tunable (prices, timers, offer gate numbers, drop rates) a config key with a safe code default. A new value is staged first (visible only in Studio sessions), then "Publish now" reaches servers in about 15 s to 1 min `[VS]` (clients may take a few minutes to reflect it), or "Publish over 15 min" rolls it out gradually; History → Restore re-stages the previous value `[official]`. Configs and in-game experiments can target by country, language, tenure and payer status.
- Matchmaking experiments: one at a time, 3 variants, 100% rollout.

Test design and sample size `[lihfolk]` (standard A/B approximation; Roblox shows an MDE on the experiment setup screen instead of a formula):

```
n per group ≈ 16 × p × (1 − p) ÷ d²      p = baseline rate, d = absolute difference to detect
(about 95% confidence, 80% power)
```

| Metric and baseline | Difference to detect | Needed per group | At 400 new players a day, two groups |
|---|---|---|---|
| D1 20% | +1 point | about 25,600 | about 128 days (over the 60-day limit: do not run it) |
| D1 20% | +3 points | about 2,850 | about 15 days |
| D1 20% | +5 points | about 1,020 | about 5 days, but run the 14-day minimum |
| Qualified PTR 4% | +25% relative (to 5%) | about 6,100 impressions | — |
| Qualified PTR 4% | +8% relative | about 60,000 impressions | — |

- Small games test bold changes (a different first minute, a new thumbnail promise), not button colours. If the dashboard MDE is larger than the effect you expect, do not start the test.
- Write the plan first: hypothesis, the one Config key, where the player is enrolled (call `GetConfigForPlayerAsync` and `GetValue` only at the moment of exposure), goal metric, guardrail metrics, what "inconclusive" will mean, and a freeze on related changes for the duration.
- Run the full planned duration; stopping on the first significant-looking day inflates false wins, and early leads often fade (novelty). Two full weeks covers the weekday and weekend cycle.
- Payer conversion is less noisy than revenue per user, which a few big spenders dominate.

| Experiment symptom | Cause | Fix |
|---|---|---|
| Groups are not the expected sizes | Enrolment happens after a step the variant changes | Enrol before the difference starts; restart |
| Everything "not significant" | Underpowered; effect below the MDE | Bolder change, larger rollout, longer run, or accept it does not matter |
| Big early win that fades | Novelty or peeking | Judge at the planned end |
| Client shows the variant, server grants the control | Two decision points | Decide once on the server, pass the value to the client by attribute |
| Results odd after a patch | The tested area changed mid-test | Freeze; restart if needed |
| Players richer in one arm after the test | Economy variants persist | Plan how to unify balances before starting |

Rules that still apply inside an experiment: odds disclosed in every variant, no deceptive variant (house rule 3), and prefer testing offer placement or structure over showing two players different prices for the same item.

## Recommended For You `[VS]`

The system retrieves candidates and then ranks them per user. Ranking counts only organic Recommended For You users, and it uses per-user averages, not totals.

How it behaves `[official]`:

- Retrieval needs only "a very low minimum" of plays from any source (ads, search, friends, share links); ranking then tests the game daily on small groups, expands if they stay, and tries other users if they do not (explore and expand). About 100 games reach each user's Home.
- No penalty for a weak start: signals use a moving window, so a fixed onboarding is re-tested. New games do not wait 28 days: PTR and bounce arrive first, then D1, then D2–7, then D8–28.
- Value = long-term retention + long-term monetisation. If retention is low, fix core gameplay first; once retention is strong, monetisation raises impressions. Strong in one still gets impressions; strong in both gets the broad distribution.
- Four things move impressions: your changes, algorithm changes, seasonality (Saturday peak, summer, back to school, holidays) and competitors improving faster than you.
- When impressions drop, read the Home Recommendations signals in order: PTR, bounce, play days and playtime first, across D8–28, D2–7 and D1; only if those are stable look at co-play, qualified sessions, spend days and Robux per user.
- Since 15 June 2026 the algorithm reads a 28-day view instead of 7 days and measures play-through, session quality (bounce) and retention separately, so a tile that wins the click and loses the session no longer helps.
- A user acquired by an ad generally stops seeing the organic tile, so organic impressions can dip during a campaign; that is not a penalty.

- Most important signals: PTR, bounce, play days, playtime (capped).
- Important: co-play days, qualified sessions, spend days, Robux per user.
- 2026 changes `[official]` (staff posts, read): 9 March "deep play-through rate" signal added; late March "Not interested" taps feed the system; 15 June 28-day window with D1 / D2–7 / D8–28 signals, and qualified PTR removed as a ranking signal in favour of PTR plus first-play bounce (thumbnail personalisation still reports qualified PTR); 12 October impressions, clicks and plays moved to a more reliable pipeline, so PTR before and after is not comparable. Signals lag about 24 hours; impression changes take days.
- Exposure reducers: giveaways and incentivised engagement, mismatched metadata, near-duplicate clones, policy violations. Paid ads do not hurt organic ranking.
- The genre setting is changeable once every three months and is not a ranking input.

Thumbnails and metadata:

- Custom 16:9 thumbnails at 1920×1080 under 3 MB are required for Home. Up to 10 thumbnails; keep 2–5 active so personalization can pick (average +8.5%, up to +50%). Gameplay video: 3 uploads per month (rejections count), authentic gameplay only, not shown on console or VR; it autoplays in the Recommended For You tile since 29 July 2026, and YouTube embeds were removed from details pages on 30 September 2026 (icons-thumbnails-and-store-page.md §9).
- Craft (icon, composition, colour, text, Blender renders, video, the upload procedure and the review rubric) is owned by `icons-thumbnails-and-store-page.md`; the owner's thumbnail rules 1–13 are in `market-scan-2026-11.md`. Title pattern in brief: a short status tag plus a verb phrase, with the name inside the first 23 characters.
- Description hook in the first 160 characters. (Roblox labels this guidance experimental, for select creators and aimed at external search engines; the general rule is a first sentence that summarises the game, plus relevant keywords.)
- Name and description rules `[official]`: keep the name consistent (frequent renames break search for the old name); no repeated or irrelevant keywords ("may result in demotion"); one or two well-placed emoji at most. A beta Promotional Text field holds a short secondary line `[VS]`.

Thumbnail and icon testing `[official][VS]`:

- Personalisation is the built-in test: activate 2–5 Home thumbnails and a bandit shows each to random groups, then shifts impressions to the winner per group while still exploring. It optimises **qualified** play-through (plays that last), not clicks. Results appear after a few hours in the Thumbnail Performance table (impressions, qualified plays, average playtime, qualified PTR, winning segment).
- Keep several active instead of crowning one winner; upload a new set with each major update and then leave it until the next. Switching back to an older icon or thumbnail does not hurt discoverability.
- Judge a variant on qualified PTR and average playtime together. A tile that lifts clicks and shortens sessions is a loss.
- Under about 1,000 DAU expect little effect (vault). There is no official icon A/B tool; `[community]` developers have asked for one. Sponsored campaigns accept up to 10 creatives split evenly, which is the practical way to compare hooks quickly (growth-and-marketing.md §3).
- Thumbnails can be managed through Open Cloud; per-thumbnail metrics are in the Analytics Query API.
- Design each round `[lihfolk]`: one control (the current best), two idea challengers (different promises), two single-variable tweaks of the control. Write the hypothesis, the one variable, the metric (qualified PTR) and the guardrail (average playtime per qualified play) before uploading. Run 10–14 days so every weekday and a weekend are covered, and do not start on a big update day. A rough 95% interval per thumbnail is `qPTR ± 1.96 × √(qPTR × (1 − qPTR) ÷ impressions)`; if the challenger's interval overlaps the control's, keep running or test a bolder idea. Report uplift with its impressions ("+18% on 22K vs 31K").
- The bandit gives weaker thumbnails fewer impressions on purpose, and a "loser" overall can be the best match for one user group; removing it can lower the total.

| Qualified PTR | Playtime per qualified play | Bounce and D1 | Verdict |
|---|---|---|---|
| Up | Up or flat | Flat or better | Keep |
| Up | Down | Worse | Over-promise: retire it, or make the first minutes deliver it |
| Flat | Up | Better | Keep in the pool; it attracts the right players |
| Down | Any | Any | Retire unless it wins a segment |

Thumbnail review before upload: the gates (truthful, policy-safe, made not generated), the ten-criterion rubric with its 8.5 upload bar, and the LihFolk-versus-vault conflict on element count now live in `icons-thumbnails-and-store-page.md` §15. Its §13 adds store-page test rounds; since 1 July 2025 a new test that includes the current winner keeps most traffic on it `[official]`.

What clickbait costs:

| Tactic | Consequence |
|---|---|
| Tile or video shows content the first minutes do not contain | Bounce rises (a top negative signal); "mismatched metadata" is not recommended and ranks lower in search `[official]` |
| Title or tile leads with Robux, giveaways or rewards | Not prioritised for recommendations `[official]` |
| Same title and visuals as an existing game | Not prioritised; among lookalikes the first to add unique metadata or a unique place file wins `[official]` |
| Keyword stuffing in name or description | "May result in demotion" `[official]` |
| Misleading video thumbnail (enhanced graphics, narration, ad text) | Rejected and counted against the 3-per-month quota `[official]` |
| Players tap "Not interested" | Negative signal since 26 Mar 2026 (vault) |

A reduced-exposure banner appears on the Creator Dashboard and updates daily; quality is reassessed with every update. If it is wrong, file Support → Discovery Content Quality → Quality Reduced Exposure with the universe ID.

Search `[official]` unless tagged:

- Search historically matched exact queries against titles; it now also understands natural-language queries ("food games") in every supported language. Use accurate genre and subgenre and a first-sentence summary with real keywords.
- Search results also demote mismatched and non-unique games.
- `[community]` (staff replies quoted on DevForum): ranking learns from player behaviour on a query and can take days to adjust; a query also matches translated titles, so enabling languages widens search reach.
- Search ads place a sponsored result at the top or right after an exact-name match (growth-and-marketing.md §3).

Other surfaces: Continue (returning users; not Recommended For You impressions), Friends, Sponsored, Standout Games (curated; nominate), Live Events, Charts (Top Playing Now, Trending, Up-and-Coming, Top Revisited, Trending Events), the details page (events, group, passes), notifications. Social links on the details page are visible only to age-verified 16+ users and may not appear in-game `[official][VS]`.

Growth plan. Lower-risk: launch in a seasonal window, fill thumbnails and metadata, run a weekly update day, measure PTR and bounce daily. Bold: pay 50,000 R$ for an expedited under-16 review, launch with an influencer plus an admin event, and buy Ads Manager traffic with `max cost per play ≈ ARPU 30d + rewarded-video earnings per user + Audience Expansion share`. Ad attribution: 30 days for a first-time player or one returning after 30+ days away, 7 days for one returning after 7–29 days, that session only for a player seen in the last 7 days. The full readiness gate, formats, costs and the cost-per-play worked example are in growth-and-marketing.md.

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

## Level-up: symptoms → likely cause → fix

| Symptom in the dashboards | Likely cause | Fix |
|---|---|---|
| Impressions near zero | Default thumbnail, "Exclude from recommendations" on, 16+ trial not cleared, exposure banner | Clear the eligibility item first |
| Impressions fell, own signals flat | Seasonality, competitor, algorithm change | Compare with last year's week and the benchmark trend; do not thrash the game |
| PTR fell after 12 Oct 2026 | Measurement change | Rebaseline; never compare across the date |
| PTR up, bounce up | Tile over-promises | Show the real first minute; judge on qualified PTR |
| PTR low, retention fine | Weak or single thumbnail, unclear title | 3–5 distinct hooks, gameplay video, title pass |
| Bounce < 60 s high on one platform | Crash, memory or slow join on that platform | Performance dashboard by platform and place version |
| First-session curve drops at one minute mark | That onboarding step | Funnel event per step; fix the earliest step that loses twice its neighbours (tutorial-and-onboarding.md §14) |
| D1 fine, D2–7 play days low | Nothing new on day 2: wall or no daily reason | Progression re-curve, timers, offline income |
| Playtime per user far above 60 min for a few, low for most | Whales carry the average; cap hides it | Design for the median player's first 20 minutes |
| Conversion fine, spend days low | Only one-time purchases | Cheap repeatable dev products |
| Metrics changed after an update, cause unknown | No annotation, several changes at once | One variable per release; Performance by place version; Configs history |
| Dashboard empty | Under 10 DAU for 7 days, or events logged in Studio only | Events record only in published games; seed plays (audit-existing-game.md §4) |

## Review gate

- [ ] KPIs read against the game's own benchmark (type stated), with the baseline window written down.
- [ ] Onboarding, shop and offer funnels plus economy events are live and verified in a published place.
- [ ] Home Recommendations signals read in priority order before any discovery change.
- [ ] 2–5 honest thumbnails active; variants judged on qualified PTR and playtime; no change more often than once per update.
- [ ] Title, description and video match the first minute; no giveaway lead; no keyword stuffing; name unchanged unless necessary.
- [ ] Every tunable is a Configs key; the two riskiest numbers are in an Experiment or a dated before/after test.
- [ ] Alerts exist for crash rate, out-of-memory exits and server frame rate; Performance checked by place version after each publish.
- [ ] No PTR comparison across 12 Oct 2026; signal lag (24 h) and impression lag (days) respected before judging.
- [ ] Any test has a written hypothesis, one variable, a guardrail metric and a sample size the traffic can reach; it ran its full duration.
- [ ] New thumbnails passed the gates and scored 8.5+ on the rubric in `icons-thumbnails-and-store-page.md` §15 before upload.
- [ ] `[VS]` facts re-checked at create.roblox.com/docs.

## Sources

Accessed 2026-11-10 and 2026-11-11. Creator docs read from the `Roblox/creator-docs` GitHub mirror (commit 7cbffff, 2026-11-10); engine signatures from `reference/engine/classes/AnalyticsService.yaml`. Source text for the original sections: grep `references/knowledge-base.md` for `## 3.1`, `## 3.9`, `## 3.10` and `## 3.11`.

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md, discovery-faq.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/analytics-dashboard.md, acquisition.md, retention.md, engagement.md, monetization.md, performance.md, alerts.md, feedback.md, insights.md, event-types.md, custom-events.md, economy-events.md, funnel-events.md, journey-events.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud/guides/analytics/index.md, metrics.md, benchmarks.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/configs.md, experiments.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/thumbnails.md, descriptions.md, publish-games-and-places.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/ads-manager.md, social-media-links.md (read)
- https://about.roblox.com/newsroom/2026/06/optimizing-discovery-great-games-reach-millions-players-roblox (search summary)
- https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575, /t/how-we-are-improving-home-this-year/4502571, /t/improved-discovery-measurement-in-creator-analytics/4930122, /t/4542233 (weekly recap, 27 Mar 2026), /t/4945086 (custom thumbnail required), /t/4879633 (YouTube embeds removed) (read, 2026-11-11)
- https://devforum.roblox.com/t/live-now-personalize-your-thumbnails-to-attract-more-users/3257233, /t/icon-ab-testing/3274267 (search summaries)
- https://devforum.roblox.com/t/thumbnail-personalization-now-remembers-your-existing-winning-thumbnails/3793665 (read, 2026-11-11)
- https://devforum.roblox.com/t/introducing-exact-match-search-for-experiences/2425969, /t/improvements-to-game-search-ranking/673608 (search summaries)
- Vault: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read)
- GameAnalytics 2026 Roblox report percentiles: https://www.gameanalytics.com/reports/2026-roblox-report and https://gamedevreports.substack.com/p/gameanalytics-key-roblox-and-roblox (search summaries; percentile figures as recorded in `references/liveops-quests-retention.md`)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `61 Thumbnails and CTR/` notes "From CTR to CCU - Impressions, Play-Through and the Discovery Loop", "Thumbnail and Icon A-B Testing - Method, Sample Size and Reading Results", "Thumbnail Review Checklist and Scoring Rubric"; `27 Marketing and Growth/A-B Testing and Experiments on Roblox.md`, `Update Cadence and Hype Cycles.md` (read). Adapted in our own words.
