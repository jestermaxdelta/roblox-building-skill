# Monetization product plan: <Title>

House rule: push microtransactions heavily, but never invasively. Non-invasive is the most important rule. Start from the default set and delete what does not fit the game; do not add power purchases in competitive modes. Rules, limits and code live in references/monetization-and-policy.md and references/data-and-purchases.md.

## Mode and baseline

Mode: <new game / level-up of a live game>. Genre row used from the "Price ladder and product mix by genre" table: <>.

Live game only: fill from Creator Hub ⟩ Monetization ⟩ Overview (last 28 days) before changing anything. New game: write targets instead.

| Metric | Now / target | After change (28 d) |
|---|---|---|
| Payer conversion (paying users ÷ DAU) | | |
| ARPPU | | |
| ARPDAU | | |
| Revenue split: developer products / passes / subscriptions / ads (%) | | |
| Share of payers with 2+ purchase days | | |
| Top 5 products by revenue | | |
| Rewarded video: opt-in %, views per viewer per day | | |
| Like ratio and D1 (guardrails) | | |
| Symptom row matched in "Level-up: monetisation symptoms" | | |

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

## Ladder check

Every rung filled, at least one repeatable product on the first two rungs, nothing that sells stat power in a competitive mode.

| Rung | Price (R$) | Products on this rung | Repeatable? |
|---|---|---|---|
| Entry | under 100 | | |
| Core | 100–399 | | |
| Premium | 400–999 | | |
| Top | 1,000+ | | |

Bundles: ×1 / ×3 / ×10 at <> / <> / <> (bulk saving stated on the card, at most about 15%). "Best value" tag on: <one product; its unit price is the lowest>.

## Offer timing map

One row per loop moment this game actually has. Popup rows spend the offer-gate budget; inline rows sit on a screen the player already opened. Delete rows that do not apply.

| Loop moment | Server signal | Offer (row #) | Surface (popup / inline / HUD / world) | Free alternative | Cap |
|---|---|---|---|---|---|
| First win or first rebirth, 10+ min played | | 7 | Popup | Earn contents in play | Once per account; 1 prompt a day |
| Second failed attempt to afford the same upgrade | | 1 or 13 | Inline on the upgrade card | Rewarded video | |
| Storage full, second time | | 9 | Inline | Sell items | |
| 20th manual collect | | 8 | Popup | Manual collect | Once per session |
| Run or round ends (win / loss) | | 1 / 14 | Inline on results | Rewarded video | |
| Return after 4+ h away | | offline doubler | Inline on welcome-back panel | Rewarded video | 1 a day |
| Timed boost under 60 s left | | same boost | HUD pill pulse | Rewarded video 5 min | Once per boost |
| Rebirth completed | | 2 or 4 | Popup | Free 5-min boost | |
| Pass just bought | | complementary pass | Inline in shop | — | Once |
| Event start / weekly update | | limited bundle, ends <date> | Featured tab + one toast | Event currency | Real end time, no restart |
| <game-specific moment> | | | | | |

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

Eligibility: 2,000+ monthly visitors, publisher 13+, ID-verified, 2FA, public game with no free-form user creation. Rewards never random, never Robux, never a gate, and never large enough to inflate the economy. Each placement is reachable within one or two taps of its trigger and shows the reward before the player commits. "Exclude your most likely purchasers": <on only if the same reward is sold / off>.

## Platform setup

- [ ] Managed Pricing on for every pass and product; dynamic price check run with a test account (no hard-coded price text found).
- [ ] Roblox Shop: global Shop button enabled; developer products Listed with icons and categories; receipt handler works for purchases that start outside the game UI.
- [ ] Price labels read `PriceInRobux`; a struck-through base price appears only from `UserBasePriceInRobux` (Plus) or a real dated sale.
- [ ] One Roblox Plus line in the shop footer (`PromptRobloxSubscriptionPurchase`), no popup.
- [ ] Subscription (if any) gated on `IsEligibleToPurchaseSubscription`; benefits identical on every platform; a one-time VIP pass remains as the alternative.
- [ ] Private-server price decided once (changing it cancels active subscriptions).

## Policy checklist for this plan

- [ ] Paid random items present? <yes/no>. If yes: odds UI, 100% sum, live boosted odds, pity disclosed, `ArePaidRandomItemsRestricted` fallback (free path / direct sale at EV / hide).
- [ ] No fake discounts, restarting countdowns or false scarcity in any copy.
- [ ] No offers during onboarding, loading or combat.
- [ ] No stat advantage sold in competitive modes.
- [ ] Gift flow checks price levels; trades check `IsPaidItemTradingAllowed`.
- [ ] Every paid shortcut lists a free alternative above.
- [ ] Receipt handler is idempotent (dedupe by PurchaseId in saved data).
- [ ] Shop and offer funnels logged.
- [ ] Every limited-time offer has one real end time in Configs; reruns are at least 30 days later under a new name.
- [ ] No purchase pads on the path, no buy button in the jump thumb zone, no prompt on join.
- [ ] Each row of "Anti-patterns and the reason each is banned" checked against the shop, HUD and copy: <reviewer, date>.

## Rollout

- Lower-risk launch set: rows 1–4, 7–10, 12–13 plus two rewarded-video placements.
- Bold additions after D1/D7 meet benchmark: VIP subscription, premium season pass, Server Luck events.
- Second-purchase value pack (199–399 R$) added only after the starter pack converts.

| Experiment (one lever each) | Variants | Primary metric | Guardrail | Stop rule |
|---|---|---|---|---|
| Boost price | 29 vs 49 R$ | ARPDAU | Conversion | 14 days or significance |
| Starter-pack trigger | First win vs first rebirth | Payer conversion | D1, like ratio | |
| Starter-pack price | 49 vs 99 R$ | Revenue per new user | Conversion | |
| Grace period | 10 vs 20 min | D1 | ARPDAU | |
| Boost timer | Real time vs play time | Boost repeat purchases | Complaints | |

Games above about 60,000 transactions a month: let Managed Pricing run the price tests and keep Experiments for timing and surfaces.
