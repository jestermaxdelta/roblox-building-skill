# Economy and progression design

How to model, tune and repair a game economy. Open it when you design currencies, XP curves, upgrade prices, rebirths or luck for a new game, or when a live game shows inflation, a progression wall, a dupe or a rebalance backlash (jump to "Level-up"). Distilled from knowledge-base sections 1.5, 1.6 and 3.5 and extended on 2026-11-10. Every number is a starting point to validate in playtests, not a law. Tags: `[official]` Roblox docs, `[community]` forum/press practice (heuristic), `[VS]` version-sensitive (check https://create.roblox.com/docs), `[house]` house estimate.

## Design the economy before you build it

1. **Name every currency and resource, then limit them.** The Creator Analytics economy dashboard shows up to 5 currencies and the event limits allow 10 resource types. Fewer currencies are easier to balance and to read.
2. **For each currency, write down who earns it, how (faucets), and what it is spent on (sinks).** Track every source and sink in a sheet. If a currency has no sink, it will inflate; if it has no faucet besides purchase, it is a hard currency and must be priced as one.
3. **Keep sources minus sinks close to zero over a player's week.** The sink ratio (total spent divided by total earned) should sit within about 5% of 1.0 for soft currency. That ratio is a heuristic from the Roblox balance guide, not a documented rule.
4. **Pick the first ten levels or upgrades for speed.** Early purchases should take 3–10 seconds each, so the player learns the loop while the numbers are still small.
5. **Decide the long-term engine** (rebirth, prestige, collection completion or seasons) before launch. Retrofitting one changes every number.

Warning signs of inflation: prices in player trades rise while nothing changed, the top 1% hold most of the wealth (Gini climbs), new players cannot afford starter items at market price, and the sink ratio drifts below 0.9. Fixes, in order of preference: add desirable sinks (cosmetics, upgrades, consumables), add a new currency for the event instead of inflating the old one, then and only then reduce faucets.

## Hard currency or direct Robux prices?

Default `[house]`: price boosts, passes and packs directly in Robux and keep one soft currency. Add a hard currency (gems) only when one of the "for" rows is a real need.

| | For a hard currency | Against |
|---|---|---|
| Player trust | Free players can earn premium items slowly | Hides the real price; leftover balances cause complaints |
| Policy | — | Anything random bought with a Robux-bought currency is a paid random item, even when the currency can also be earned `[official]`; odds, PolicyService and trading gates then apply to every gem sink |
| Operations | Monthly subscription drops and season-pass rewards have a unit to pay in `[official]` | One more of the 5 dashboard currencies to balance; a new currency is a new scam and dupe target `[community]` |
| Pricing | Bundles and sub-1 R$ granularity | Roblox's subscription guide starts from "how much play earns the equivalent of 1 Robux"; keep that rate legible. A DevForum reply recommends rescaling so 1 gem ≈ 1 R$ rather than an odd rate `[community]` |

If you add one: fixed public exchange rate, no random sink for restricted players, never tradeable, and log every source and sink with `AnalyticsService:LogEconomyEvent` (transaction type `IAP` for purchases).

## Progression curves

Model requirement per level as a function of **time**, not of XP. Decide how many minutes level L should take, multiply by XP earned per minute at that level, and you get the requirement:

```
req(L) = t(L) × xpPerMin(L)
```

Curve shapes and when to use them:

| Shape | Formula | Feel | Use |
|---|---|---|---|
| Linear | `base + k × L` | Steady, predictable | Short games, tutorials, battle-pass tiers |
| Polynomial | `base × L^p` (p 1.5–2.5) | Gradual slowdown | RPG levels, most simulators |
| Exponential | `base × g^L` | Fast wall | Incrementals with rebirth or exponent notation |

A geometric cost curve for upgrades uses growth factor `g`:

```
cost(owned) = floor(baseCost × g^owned)         g = 1.07–1.15 for common upgrades, 1.5–3 for rare ones
cost from a to b owned = baseCost × g^a × (g^(b−a) − 1) / (g − 1)
doubling interval (levels until price doubles) = log 2 / log g   (≈ 5 at g = 1.15, ≈ 10 at g = 1.07, ≈ 2 at g = 1.5)
```

Buy-max buttons walk prices forward and stop when the next price exceeds the balance; precompute with the closed form above, do not loop on the client.

## Rebirth and prestige math

Rebirth resets soft progress for a permanent multiplier. Three common shapes:

| Model | Multiplier after k rebirths | Cost of rebirth k | Wait ratio (time to next rebirth / previous) |
|---|---|---|---|
| Additive | `1 + k × p` | `R0 × r^k` | `r × (1 + k p) / (1 + (k + 1) p)` |
| Multiplicative | `q^k` | `R0 × r^k` | `r / q` (constant) |

Worked numbers from the knowledge base: with r = 3 and p = 0.5, rebirth 8 takes about 137 days of play, which is too slow; with r = 1.8 it takes about 3 days 20 hours. With r = 3 and q = 2.4 the wait ratio is a constant ×1.25, which keeps each rebirth about 20–50% longer than the last. Aim for a wait ratio of ×1.2–1.5 between successive rebirths.

Rebirths run on the server only. The client sends intent ("Rebirth"); the server checks the balance, resets and applies the multiplier in one synchronous step.

Rebirth as practised in the 2026 stat-lane hits (owner's scan, `references/market-scan-2026-11.md`) `[community]` `[VS]`: multipliers step ×2 / ×3 / ×4 with level caps (22 / 34 / 48); the collection, passes and Robux purchases survive the reset; stage gates grow about ×4; eggs cost ×40–250 the previous egg; a new World unlocks at the first rebirth; 8–10 gates per World. Rebirth is also a sale moment: the post-reset grind is where a 2× boost is worth most.

Conflict: the knowledge base puts the first rebirth at 15–25 minutes (inside session one); one community glossary says 30–60 minutes and "meaningful rewards across 20–50 rebirths". Keep 15–25 minutes: the median Roblox session is 6.6 minutes and 19–24 minutes is already a top band (market scan), so a 60-minute first rebirth is seen by few players.

## Paid multipliers and the curve

Paid boosts shift the curve; they do not bend it. Model the payer before you price anything.

```
stack M = pass × timed boost × VIP × friend × group          e.g. 2 × 2 × 1.2 × 1.2 × 1.1 ≈ 6.3
extra levels bought by M on a geometric line = log M / log g  (2× → 5 levels at g = 1.15, 10 at g = 1.07; 4× → 10 and 20)
time to any goal for the payer = free time / M                (rebirth wait ratio r / q is unchanged)
content runway for the payer = hours of new content / M       (10 h weekly update ÷ 6.3 ≈ 1.6 h)
```

- Geometric prices absorb multipliers; flat-priced content (zone unlocks, event shops, fixed packs) does not. Price every flat item from top-decile income, not the median.
- Cap the stack `[house]`: permanent paid multipliers ≤ 4× in total, everything including timed boosts ≤ 8×. Same-type boosts extend time, never multiply. Without a cap each new pass shortens the life of every future update.
- Conflict: the +1 / Evolution format sells one-time ×8 / ×15 / ×30 / ×99 training pads (market scan), far above this cap. It works there because gates grow about ×4 per stage, so a ×99 pad is worth log 99 / log 4 ≈ 3.3 stages. Follow the format norm in stage-gated lane games and add stages weekly; apply the cap everywhere content is not geometric.
- Free-to-payer gap `[house]`: a free player reaches any milestone in at most 3–4× the payer's time. Beyond that the game reads as pay-to-win and ratings pay for it.
- Timed boosts gain value as income grows; fixed-amount currency packs lose it. Size packs in minutes of the buyer's current income ("30 min of your income: 9,330 Cash" at 311 per minute), compute the amount on the server and show the exact number before purchase `[house]`. Rewarded-video rewards should likewise "be scaled so that they remain valuable to users as they advance through the game" `[official]`.
- Rewarded video is a faucet: the reward must "not inflate currency or unbalance the game's economy" `[official]`. Cap ad income at about 10–15% of a day's earnings `[house]`.
- No paid multiplier applies to anything ranked or competitive (house rule 3).

## Offline income

```
offline = floor(min(secondsAway, maxHours × 3600) × ratePerSecond × efficiency)
```

Use efficiency 0.25–0.5 and a cap of 8–12 hours. Say what the cap is in the UI, and never claim "earning while away" beyond the honest cap. A 2× offline earnings product or rewarded-video doubler is a good non-invasive sale on return.

## Large numbers

Past about 1e15 double precision loses integer precision. Store a mantissa and exponent pair, or a custom big-number type, once your top balances approach that range. Round before you format with K/M/B/T suffixes so 999,999 does not show as "1000K".

## Random rewards, luck and pity

- Show every outcome and its numeric odds before purchase, summing to exactly 100%. Roll from the same weight list you display. (See monetization-and-policy.md for the paid-random-items rules and the PolicyService gate.)
- **Luck boosts are probability modifiers.** Example: 2× Luck multiplies weights of non-common tiers by 2: Common 90 / Rare 18 / Legendary 2 → 81.82% / 16.36% / 1.82% after normalising. Show the boosted odds live while the boost is active.
- **Server Luck** applies to everyone in the server; announce the activator and the end time to all players and show the boosted odds to all.
- **Pity**: guarantee the top tier by a fixed count (for example at 100 rolls). With a 1% rate, 63.4% of players already have it by roll 100, so pity protects the unlucky tail without changing the average. Disclose pity rules.
- **Direct sale at expected value** is the fallback when paid random items are restricted: a 10 R$ roll with a 5% chance at the item implies a 200 R$ direct price.

## Event currency example (why events need their own currency)

A fishing game sells fish: Catfish 70% at 10 G, Trout 20% at 20 G, Salmon 10% at 30 G, expected value 14 G per cast. (The Roblox doc has a typo saying "Salmon 30% = 3 G"; the corrected 10% is used here.) Adding a 0.1% Golden Salmon worth 1,000 G, taken from Catfish's share, lifts EV to 14.99 G (+7.1%). If the event triples participation, daily income rises to about 44,970 G (+221%) and the main currency inflates. The fix is a unique event currency with its own sinks that expire with the event.

## Pricing soft currency against Robux

Use the player's earning rate to anchor pack prices. Example from the knowledge base: a player earns about 311 G per minute, so 100 R$ (about $1) buys roughly 10,000 G. A ladder with mild bulk bonuses:

| Price (R$) | Currency | Bonus |
|---|---|---|
| 49 | 4,900 | — |
| 99 | 10,000 | — |
| 399 | 42,000 | +5% |
| 999 | 110,000 | +10% |
| 2,499 | 287,000 | +15% |

A 2× Cash boost for 10 minutes is worth about 3,110 G of extra earnings (about 31 R$), so price it at 1–1.5× that value: 29–49 R$. Permanent 2× Money passes sit around 399 R$ in the market `[VS]`.

## Server-authoritative rules for economies

- Clients send intent only (`RequestBuy("ItemId")`), never prices, amounts or outcomes.
- No yield between checking a balance and spending it. If a DataStore call is needed, take a per-player lock first.
- Rebirths, rewards, multipliers and boost expiry are computed on the server; clients display attributes.
- Rate-limit economy remotes with a token bucket (see networking-and-security.md).
- Repair bad data on load (negative balances, NaN, missing fields) rather than trusting it.
- Check `PolicyService` `IsPaidItemTradingAllowed` before enabling trades of paid items.

## Social balance and trading

- Asymmetric factions or classes: target win rates between 45% and 55% with a spread under 10 points, at least two counters per option and at least three viable strategies.
- Trade UI rules: two-sided confirmation, no changes after acceptance, a 3–5 second delay before the final confirm, a value display, a trade history, and a cooldown for new accounts. Gate trading on account age, `Player:IsVerified` or `DeviceTrustLevel` where supported `[VS]`.
- Price levels: `MarketplaceService:GetUsersPriceLevelsAsync` returns a level 1–1000 per user. Allow gifts from a higher level to a lower level, and trades only between equal levels, so regional pricing cannot be arbitraged.

## Trading, gifting and duplication risk

A dupe turns a scarce item into inflation overnight. Grow a Garden disabled pet gifting in July 2025 after a lag-based duplication exploit; press coverage quotes the developers saying they "had to completely rewrite our data backend" before re-enabling it `[community]`. Design for it before the first trade ships.

| Dupe vector | Guard |
|---|---|
| Yield between "check both inventories" and "swap" | One synchronous swap on the server, no yields inside it |
| Player leaves or server dies mid-trade | Swap in memory, then save both profiles immediately; if either save fails, mark both for review |
| Stale data in two servers | Session-locked profiles (data-and-purchases.md); trade only when both profiles are loaded in the same server |
| Offline gift applied twice | Deliver through a message keyed by a unique gift id; applying is idempotent |
| Remote spam racing two trades | Per-player trade lock and token-bucket rate limit |
| Item with no identity | Give every tradeable item a GUID at mint (`HttpService:GenerateGUID(false)`); keep a mint ledger (count minted per item type) |

Operations: a `trading_enabled` and a `gifting_enabled` Configs kill switch; an append-only trade log; an alert when one GUID appears in two inventories or when owned count exceeds minted count; quarantine flagged items (unusable, visible) instead of deleting them, so honest recipients can appeal; new-account cooldown and a per-day value cap. Pausing the feature for a week costs less than a crashed item market.

## Live rebalancing without angering players

1. Measure first: sources and sinks from `LogEconomyEvent`, median and top-decile wallet by cohort, days-to-afford the next key item.
2. Prefer, in order: a new desirable sink → a new tier priced for today's inflated income → event currency → slower growth of future faucets → a cut to an existing faucet (last resort).
3. Never reduce something bought with Robux. Roblox's own guidance when a pass is replaced: existing holders "should continue to receive the benefit they paid for" `[official]`. Grandfather owners or let them choose compensation.
4. Buff the weak option rather than nerf the strong one where the maths allows; players read a nerf as a loss.
5. Ship through Configs to an Experiments cohort, one lever at a time (Roblox's balance guide recommends Experiments for price tests and Configs for live tuning `[official]`), and watch seven days: sink ratio, D1/D7, like ratio, pack and boost sales.
6. Announce before it ships, with the reason and the numbers. The Roblox backlashes that reached the press were changes that arrived without notice or that players read as taking earned value away (Welcome to Bloxburg's job-pay change; the 2026 cross-game pass sales shutdown, which a creator petition says came "without any warning") `[community]`.
7. Compensate on login when anyone loses value: currency, a timed boost or a cosmetic.
8. Roll back or wipe only for exploits, only on affected accounts, and say so publicly.

## Level-up: economy symptoms → likely cause → fix

The knowledge base (`## 3.5`, "Inflation and deflation") has the basic signal table; these are the live-game cases it does not cover.

| Symptom | Likely cause | Fix |
|---|---|---|
| Veterans clear a weekly update in one session | Paid and rebirth multipliers outran flat-priced content | Price new content geometrically from top-decile income; cap the multiplier stack; add a prestige sink |
| Funnel drop at one specific upgrade or gate | Local wall: g too high early, or a gate jump far above ×4 | Flatten that step; first ten purchases 3–10 s each |
| Rebirth-count histogram piles up at k | Additive multiplier flattening while cost grows by r | Move to a multiplicative model or lower r until the wait ratio is ×1.2–1.5 |
| Currency-pack sales decay week over week | Inflation made fixed packs worthless | Packs sized in minutes of current income; add sinks |
| Sink ratio under 0.9; wallets pile up | Nothing left worth buying | Aspirational cosmetics, upgrade tiers, consumables |
| Sink ratio above 1.1; sessions shorten | Starved faucets | Quest and offline income up; cheaper early upgrades |
| Top 1% wallet share and trade prices climb fast | Uncapped faucet, exploit or dupe | Server caps, anomaly review, GUID audit |
| Owned count of an item exceeds minted count; leaderboard jumps overnight | Dupe | Kill switch, quarantine by GUID, patch, announce |
| Main-currency pack sales drop after an event | The event paid out main currency | Event currency with sinks that expire |
| Free players call the game pay-to-win | Free-to-payer time gap above 3–4×, or paid power in a ranked mode | Cap the stack; move paid value to convenience and cosmetics |
| Anger after a balance patch | No notice, or paid value reduced | Protocol above: announce, grandfather, compensate |
| Boost sales fall as players progress | Boost value shown as "2×" while prices grew faster than income | Show the gain in currency at the player's rate; lower late-game g |

## Review gate

- [ ] Every currency has a documented faucet list and sink list.
- [ ] Sink ratio modelled at 0.95–1.05 for week one.
- [ ] First ten upgrades take 3–10 seconds each; first rebirth within the first or second session.
- [ ] Rebirth wait ratio ×1.2–1.5.
- [ ] Offline income capped and stated.
- [ ] Odds shown equal odds rolled; pity disclosed; luck boosts disclosed live.
- [ ] All economy mutations server-side, rate-limited and logged with `AnalyticsService:LogEconomyEvent`.
- [ ] Event rewards use event currency.
- [ ] Payer modelled at the full multiplier stack: stack within the cap, content runway and free-to-payer gap written down.
- [ ] Hard currency justified or absent; if present, every random sink is gated and disclosed.
- [ ] Tradeable items carry GUIDs; trade and gift kill switches exist; the swap has no yields.
- [ ] Live game: baseline sink ratio, wallet medians and pack sales recorded before any rebalance; the change is announced, grandfathered and compensated.

For the grep-able original, search `references/knowledge-base.md` for `## 1.5`, `## 1.6` and `## 3.5`.

## Sources

Accessed 2026-11-10. "(read)" = opened in the `Roblox/creator-docs` mirror (commit of 2026-11-07); "(search summary)" = seen only through web search result text.

- https://github.com/Roblox/creator-docs `content/en-us/production/game-design/balance-virtual-economies.md`, `subscription-design.md`, `season-pass-design.md`; `production/analytics/economy-events.md`; `production/monetization/paid-random-items.md`, `regional-pricing.md`, `subscriptions.md`; `production/promotion/rewarded-video-ads.md` (read)
- `references/market-scan-2026-11.md` and `references/knowledge-base.md` §1.5, §1.6, §3.5 (read)
- https://devforum.roblox.com/t/should-i-charge-more-robux-for-a-smaller-amount-of-gems-or-simply-lower-the-value-of-them/518565, https://devforum.roblox.com/t/paid-random-item-policy-question/3107756, https://devforum.roblox.com/t/premium-tokens-what-they-are-and-how-would-they-work/560411 (search summary)
- https://devforum.roblox.com/t/preventing-duping-methods-in-trading/2688896, https://www.creation.dev/blog/roblox-trading-system-design (search summary)
- Grow a Garden gifting shutdown: https://www.sportskeeda.com/roblox-news/why-pet-gifting-disabled-grow-garden, https://gamertweak.com/pet-gifting-disabled-in-grow-a-garden/ (search summary)
- Backlash cases: https://www.404media.co/roblox-community-protests-communism-update, https://www.change.org/p/bring-back-cross-game-sales-of-gamepasses-on-roblox-e1da39b1-809d-42a3-a03a-997af08075d6 (search summary)
- https://www.creation.dev/glossary/rebirth (search summary; the 30–60 minute and 20–50 rebirth figures)
- No evidence found: a DevForum or Reddit thread with measured rebirth tuning data from a current top simulator; reddit.com was not reachable and surfaced in no search.
