# Economy and balance sheet spec: <Title>

Build this as a spreadsheet (or a Luau config module with the same columns) before implementing the economy. Formulas and ranges come from references/economy-and-progression.md. Every number here becomes a Configs key with a code default.

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
| Gems | hard (Robux only) | packs, rewarded video, rare drops | boosts, skips | no | yes | Gems |
| Event tokens | event | event activities | event shop | no | during event | EventTokens |

Limit: at most 5 currencies on the dashboard; 10 resource types in analytics.

## Sheet 2: Faucets per hour (by player stage)

| Stage | Minutes played | Main loop income per min | Quest income per hour | Offline income per hour (capped) | Rewarded video per day | Total per hour |
|---|---|---|---|---|---|---|
| New (0–30 min) | | | | | | |
| Early (day 1–3) | | | | | | |
| Mid (week 1–2) | | | | | | |
| Late (post-rebirth) | | | | | | |

## Sheet 3: Sinks and price curves

| Upgrade line | Base cost | Growth g | Doubling interval (log 2 / log g) | Max level | Cost 0→max | Time to max at stage income |
|---|---|---|---|---|---|---|
| Capacity | | 1.15 | ≈ 5 levels | | | |
| Speed | | 1.12 | | | | |
| Zone unlock | | n/a (fixed) | | | | |

Rules: first ten purchases take 3–10 s each; `cost(n) = floor(base × g^n)`; cost a→b `= base × g^a × (g^(b−a) − 1) / (g − 1)`.

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
- Swap is one synchronous server step; both profiles saved immediately; same-server trades only.

## Sheet 13: Rebalance log (live games)

| Date | Lever (one) | Old → new | Cohort / Configs key | Announced on | Grandfathered or compensated | 7-day result |
|---|---|---|---|---|---|---|

Order of preference: new sink → new tier priced for current income → event currency → slower future faucet growth → faucet cut. Nothing bought with Robux is reduced.

## Validation plan

- [ ] Simulate week 1 and week 4 for a casual (20 min/day) and a heavy (90 min/day) player; both must have a visible next purchase at all times.
- [ ] Sink ratio 0.95–1.05 in week 1.
- [ ] No upgrade line maxes before the next zone unlocks.
- [ ] Every number is a Configs key; defaults match this sheet.
- [ ] Economy events logged for every faucet and sink with the SKU.
- [ ] Full-stack payer simulated: stack within the cap, runway and free-to-payer gap recorded in Sheet 11.
- [ ] Hard currency absent or justified; every random sink bought with it is disclosed and PolicyService-gated.
- [ ] Live game: Sheet 0 filled before the change and Sheet 13 after it.
