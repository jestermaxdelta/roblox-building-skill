# Economy and balance sheet spec: <Title>

Build this as a spreadsheet (or a Luau config module with the same columns) before implementing the economy. Formulas and ranges come from references/economy-and-progression.md. Every number here becomes a Configs key with a code default.

Level: beginners fill Sheets 1–3 and 5 and stop. Intermediate adds 2b, 3b, 4, 6–11. Expert adds 12–15 and runs the simulation in CI.

## Sheet 0: Mode and baseline (live games)

Mode: <new game / level-up>. For a live game fill this from `LogEconomyEvent` data and the Creator Hub economy dashboard before changing a number; it is the "before" for every rebalance.

| Measure | Now | Target | After change (7 d) |
|---|---|---|---|
| Sink ratio (spent ÷ earned), soft currency | | 0.95–1.05 | |
| Median wallet / top-decile wallet (payers and non-payers) | | | |
| Minutes to afford the next key item at median income | | | |
| Rebirth-count histogram: where players pile up | | | |
| Currency-pack and boost sales per 1,000 DAU | | | |
| Symptom row matched in "Level-up: economy symptoms" | | | |

## Sheet 1: Currencies

| Currency | Type (soft / hard / event / premium) | Earned by (faucets) | Spent on (sinks) | Tradeable? | Shown on HUD? | Analytics resource name |
|---|---|---|---|---|---|---|
| Cash | soft | deliveries, quests, offline | upgrades, cosmetics | no | yes | Cash |
| Gems | hard (mainly Robux) | packs, rewarded video, rare drops | boosts, skips | no | yes | Gems |
| Event tokens | event | event activities | event shop | no | during event | EventTokens |

Limit: at most 5 currencies on the Economy dashboard; 10 resource types in analytics; a currency Robux can buy makes every random sink it pays for a paid random item.

For each currency: its one job <>; what it buys that nothing else buys <>; what happens when players stop caring <>. Premium currency only: anchor (1 unit ≈ <> R$); price and pack unit <50>; `Paid` and `Free` buckets with spend order <free first / paid first>; target free share <under 50%>; conversions allowed (one way only) <>.

## Sheet 2: Faucets per hour (by player stage)

| Stage | Minutes played | Main loop income per min | Quest income per hour | Offline income per hour (capped) | Rewarded video per day | Total per hour |
|---|---|---|---|---|---|---|
| New (0–30 min) | | | | | | |
| Early (day 1–3) | | | | | | |
| Mid (week 1–2) | | | | | | |
| Late (post-rebirth) | | | | | | |

## Sheet 2b: Time to afford per zone (the income model every price reads)

Target bands: small upgrade 1–3 min; meaningful upgrade 5–15 min; gate 15–45 min; rebirth 1–3 sessions.

| Zone k | Income per min I_k | Income growth g | Gate price P_k | Price growth p | p ÷ g (aim 1.0–1.15) | T_k = P_k ÷ I_k (min) | Observed p50 / p90 (live) | Gate conversion within 3 days (live) |
|---|---|---|---|---|---|---|---|---|
| 0 | | — | | — | — | | | |
| 1 | | | | | | | | |
| … | | | | | | | | |

Quest and event rewards are written as a share of the next gate price: <>%.

## Sheet 3: Sinks and price curves

| Upgrade line | Base cost | Growth g | Doubling interval (log 2 / log g) | Max level | Cost 0→max | Time to max at stage income |
|---|---|---|---|---|---|---|
| Capacity | | 1.15 | ≈ 5 levels | | | |
| Speed | | 1.12 | | | | |
| Zone unlock | | n/a (fixed) | | | | |

Rules: first ten purchases take 3–10 s each; `cost(n) = floor(base × g^n)`; cost a→b `= base × g^a × (g^(b−a) − 1) / (g − 1)`.

## Sheet 3b: Upgrade tracks (cost and benefit together)

| Track | Benefit per level (additive / multiplicative) | Benefit in one unit (% income) | g | Payback at L = 0 / 5 / 10 (min) | Natural cap L* at 60-min tolerance | Greedy-path level after one session | Rounded to 2 s.f. + monotonic? |
|---|---|---|---|---|---|---|---|

`L* = ln(paybackMax × gainPerLevel ÷ baseCost) ÷ ln g` for additive tracks. A multiplicative track needs g well above its per-level multiplier. If the greedy path leaves a track at level 2 while another reaches 40, reprice it.

## Sheet 4: Sink ratio by week

| Week | Total earned (model) | Total spent (model) | Sink ratio | Target 0.95–1.05 | Action if off |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 4 | | | | | |

## Sheet 5: Progression curve

| Level | Target minutes | XP per minute at level | Requirement = minutes × XP/min | Cumulative hours |
|---|---|---|---|---|
| 1 | | | | |
| 10 | | | | |
| 25 | | | | |
| 50 | | | | |

## Sheet 6: Rebirth

- Model: <additive `1 + k·p` / multiplicative `q^k`>.
- Cost `R0 × r^k` with R0 = <>, r = <>.
- Multiplier parameter p or q = <>.
- Wait ratio between rebirths (target ×1.2–1.5): <computed>.
- Time to rebirth 1, 3, 5, 8: <>.
- What resets, what persists (cosmetics, passes, entitlements persist).

## Sheet 7: Offline income

- `floor(min(away, maxHours × 3600) × rate × efficiency)`; efficiency <0.25–0.5>, cap <8–12 h>; UI copy stating the cap.

## Sheet 8: Random rewards (if any)

| Pool | Outcome | Weight | Odds (%) | Odds with 2× Luck (%) | Pity at | Direct-sale price at EV (for restricted players) |
|---|---|---|---|---|---|---|
| Egg A | Common | 90 | 81.82 after boost | | | |
| Egg A | Rare | 18 | | | | |
| Egg A | Legendary | 2 | | | 100 | |

Odds shown must equal odds rolled and sum to 100%.

Pity and supply: rule <flat / ramp from roll N / hard cap K>; expected rolls per top-tier hit <Σ S(k)>; effective rate <1 ÷ E>; share of players reaching the hard cap <>; featured-item rule and carry-over <>; duplicate protection <none / top tier only>. Copies of each top-tier item per day = rolls per day × odds × average luck = <>; luck cap <>; copy sink (fusion, crafting) <>.

## Sheet 9: Robux anchors

- Earning rate used for pricing: <> soft currency per minute.
- 100 R$ ≈ <> soft currency.
- Pack ladder: 49 / 99 / 399 (+5%) / 999 (+10%) / 2,499 (+15%).
- 2× Cash 10 min value = 10 × rate ≈ <> → price 29–49 R$.

## Sheet 10: Event currency

| Event | Dates | Faucets | Sinks (expire with event) | Expected participation lift | Inflation check on main currency |
|---|---|---|---|---|---|

## Sheet 11: Paid multiplier budget

| Multiplier | Source (pass / timed / VIP / friend / group / pad) | Value | Stacks how |
|---|---|---|---|
| | | | multiplies / extends time |

- Full stack M = <product of the column>; permanent paid part ≤ 4×, everything ≤ 8× (stage-gated +1 lane games follow the format norm instead; state which).
- Extra levels M buys on each line = log M / log g: <>.
- Free vs full-stack time to: first rebirth <> / <>; zone 3 <> / <>; end of launch content <> / <>. Gap ≤ 3–4×.
- Payer runway of one weekly update = hours of content ÷ M = <>.
- Currency packs sized in minutes of current income: <> min per rung; rewarded-video income ≤ 10–15% of a day's earnings.

## Sheet 12: Trade and gift risk register (if items move between players)

| Item class | Tradeable? | GUID at mint | Minted count tracked | Paid origin (needs `IsPaidItemTradingAllowed` + price levels) | Daily value cap |
|---|---|---|---|---|---|

- Kill switches: `trading_enabled`, `gifting_enabled` (Configs). Trade log location: <>. Dupe alert: one GUID in two inventories, or owned > minted.
- Swap is one synchronous server step with no yield between check and swap; same-server trades only; persistence follows the two-profile commit protocol in references/data-and-purchases.md ("swap, then save both" leaves a dupe window on a crash).

## Sheet 13: Rebalance log (live games)

| Date | Lever (one) | Old → new | Cohort / Configs key | Announced on | Grandfathered or compensated | 7-day result |
|---|---|---|---|---|---|---|

Order of preference: new sink → new tier priced for current income → event currency → slower future faucet growth → faucet cut. Nothing bought with Robux is reduced.

## Sheet 14: Simulation spec

| Archetype | Share | Sessions per day | Mean minutes | Income multiplier |
|---|---|---|---|---|
| Casual | 0.55 | 0.8 | 12 | 1 |
| Regular | 0.30 | 1.5 | 25 | 1 |
| Grinder | 0.12 | 2.5 | 55 | 1 |
| Payer | 0.03 | 2.0 | 35 | <full stack M> |

Replace with measured clusters after launch. Spending policy: <gate → upgrade if payback ≤ 60 min → rolls from <>% of income>. Churn: base <>% a day, +<>% when the next goal is more than 60 min away. Runs: 30 days, 5 seeds, baseline and change on the same seeds.

| Day-30 output | Baseline | After change | Golden-number tolerance in CI |
|---|---|---|---|
| Stuck share | | | ±10% |
| Sink ÷ faucet | | | ±10% |
| Top-item supply | | | ±20% |
| Median zone by archetype | | | |
| Share of coins held by finishers | | | |
| Days for a grinder to finish launch content (vs update cadence) | | | |

## Sheet 15: Telemetry and alerts

- One wallet module logs every economy event after commit. Custom fields: progress band, config version, experiment variant. SKU and transaction-type names are frozen here: <list>.

| Metric (per progress band) | Source | Healthy range | Alert |
|---|---|---|---|
| Hours of income held, p50 / p90 | balance ÷ income per hour at save | Mid-game under 1–2 h | Rising week over week |
| Net flow by transaction type, per DAU | `LogEconomyEvent` | | A sink halves; robust z above 3 |
| Free premium granted per DAU | wallet | | Robust z above 3; page above 5 |
| New copies of each top-tier item per DAU | mint ledger | rolls × odds × luck | Robust z above 3; page above 5 |
| Top 0.1% share of each currency | own aggregate | | Doubles day over day |
| Payer progress gap at equal playtime | own aggregate | Within the declared gap | Above the gap |

Robust z = (today − median of the same weekday over 4+ weeks) ÷ (1.4826 × MAD).

## Validation plan

- [ ] Simulate week 1 and week 4 for a casual (20 min/day) and a heavy (90 min/day) player; both must have a visible next purchase at all times.
- [ ] Sink ratio 0.95–1.05 in week 1.
- [ ] No upgrade line maxes before the next zone unlocks.
- [ ] Every number is a Configs key; defaults match this sheet.
- [ ] Economy events logged for every faucet and sink with the SKU.
- [ ] Full-stack payer simulated: stack within the cap, runway and free-to-payer gap recorded in Sheet 11.
- [ ] Hard currency absent or justified; every random sink bought with it is disclosed and PolicyService-gated.
- [ ] Live game: Sheet 0 filled before the change and Sheet 13 after it.
- [ ] p ÷ g between 1.0 and about 1.15 for every zone step; every system's prices derived from Sheet 2b.
- [ ] Each rebalance in Sheet 13 has a numeric hypothesis, a simulated comparison and a one-week read.

Credit: Sheets 2b, 3b, 14 and 15 adapt ideas and starting values from LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault); see references/economy-and-progression.md §Sources.
