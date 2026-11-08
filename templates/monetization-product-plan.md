# Monetization product plan: <Title>

House rule: push microtransactions heavily, but never invasively. Non-invasive is the most important rule. Start from the default set and delete what does not fit the game; do not add power purchases in competitive modes. Rules, limits and code live in references/monetization-and-policy.md and references/data-and-purchases.md.

## Product set

| # | Product | Type | Price (R$) | Trigger / surface | Grant logic (server) | Free alternative | Analytics SKU | Creator Hub id |
|---|---|---|---|---|---|---|---|---|
| 1 | 2× Cash, 10 min | Dev product | 29–49 | Shop; after-win offer | `Boosts.DoubleCash` expiry +600 s, extend | Rewarded video 5 min | boost_cash_10 | |
| 2 | 2× Cash, 30 min | Dev product | 79–99 | Shop | +1,800 s | | boost_cash_30 | |
| 3 | 2× Speed, 10 min | Dev product | 25–39 | Shop; contextual near the slow thing | | Rewarded video | boost_speed_10 | |
| 4 | 2× EXP, 10 / 30 min | Dev product | 29–49 / 79–99 | Shop | | | boost_exp_10 | |
| 5 | Luck 2×, 15 min | Dev product | 49–79 | Shop (only with luck mechanics) | boosted weights; odds shown live; PolicyService gate | Free daily luck hour | boost_luck_15 | |
| 6 | Server Luck | Dev product | 149–249 | Shop | server attribute with expiry; banner thanks buyer; odds shown to all | | server_luck | |
| 7 | Starter Pack | Dev product | 49–99 | Offer gate after first win; once per account | `Entitlements.StarterPack`, Cash, item | Earned in 30 min of play | starter_pack | |
| 8 | Auto-Collect | Game pass | 199–299 | Shop; contextual after 20 manual collects | attribute `AutoCollect` | Manual collect | pass_autocollect | |
| 9 | Extra storage / slots | Game pass | 129–199 | Shop; when storage is full | | Sell items | pass_storage | |
| 10 | Permanent 2× Cash | Game pass | 399 | Shop | | Timed boost | pass_2x_cash | |
| 11 | VIP | Pass 799 or subscription 499/mo ($4.99) | Shop | cosmetic + convenience, no PvP power | | pass_vip | |
| 12 | Gift <pass> | Dev product | same as pass | Shop gift tab; price-level gated | recipient `Entitlements[pass]`; MessageAsync if offline | | gift_<pass> | |
| 13 | Currency packs | Dev product | 49 / 99 / 399 / 999 / 2,499 | Shop | +5 / +10 / +15% bulk bonus | Play | pack_s/m/l/xl/xxl | |
| 14 | Revive / second chance | Dev product | 15–30 | After run ends, never mid-chase | | Rewarded video revive | revive | |
| 15 | Private server | Server | 0–100 | Roblox UI | | | | |

Prices are read at runtime from `GetProductInfoAsync`; this column is the intended list price for Creator Hub setup. Market prices are a 2026-11-07 snapshot; re-check.

## Offer gate configuration (Configs keys)

| Key | Default | Meaning |
|---|---|---|
| offer_grace_seconds | 600 | No offers before 10 min lifetime play |
| offer_requires_first_win | true | And a first win |
| offer_min_gap_seconds | 480 | At least 8 min between offers |
| offer_max_per_session | 3 | |
| starter_max_per_day | 1 | |
| offer_dismiss_limit | 2 | Dismissals before suppression |
| offer_dismiss_cooldown | 86400 | 24 h suppression |
| offer_max_screen_fraction | 0.25 | Design constraint, not runtime |

Positive triggers only (list them): <delivery complete, level-up, round win, rebirth, zone unlock>. Blocked states: first minutes, loading, combat, death, menus open.

## Rewarded video placements (2–3)

| Placement | Reward (fixed dev product) | Value (3–10 R$) | Daily cap | Where |
|---|---|---|---|---|
| Double offline earnings | | | 1 | Return screen |
| 5 min 2× Cash | | | 3 | Shop, next to the paid boost |
| Second chance | | | 2 | Run end |

Eligibility: 2,000+ monthly visitors, 13+ audience, ID-verified, 2FA. Rewards never random, never a gate.

## Policy checklist for this plan

- [ ] Paid random items present? <yes/no>. If yes: odds UI, 100% sum, live boosted odds, pity disclosed, `ArePaidRandomItemsRestricted` fallback (free path / direct sale at EV / hide).
- [ ] No fake discounts, restarting countdowns or false scarcity in any copy.
- [ ] No offers during onboarding, loading or combat.
- [ ] No stat advantage sold in competitive modes.
- [ ] Gift flow checks price levels; trades check `IsPaidItemTradingAllowed`.
- [ ] Every paid shortcut lists a free alternative above.
- [ ] Receipt handler is idempotent (dedupe by PurchaseId in saved data).
- [ ] Shop and offer funnels logged.

## Rollout

- Lower-risk launch set: rows 1–4, 7–10, 12–13 plus two rewarded-video placements.
- Bold additions after D1/D7 meet benchmark: VIP subscription, premium season pass, Server Luck events.
- Experiments queued: boost price 29 vs 49; grace 10 vs 20 min; starter-pack trigger.
