# Economy and progression design

Distilled from knowledge-base sections 1.5, 1.6 and 3.5. Use it when you model an economy, tune an XP curve, price upgrades, design rebirths or luck, or diagnose inflation. Every number below is a starting point to validate in playtests, not a law. Items marked `[VS]` are version-sensitive; check https://create.roblox.com/docs before relying on them.

## Design the economy before you build it

1. **Name every currency and resource, then limit them.** The Creator Analytics economy dashboard shows up to 5 currencies and the event limits allow 10 resource types. Fewer currencies are easier to balance and to read.
2. **For each currency, write down who earns it, how (faucets), and what it is spent on (sinks).** Track every source and sink in a sheet. If a currency has no sink, it will inflate; if it has no faucet besides purchase, it is a hard currency and must be priced as one.
3. **Keep sources minus sinks close to zero over a player's week.** The sink ratio (total spent divided by total earned) should sit within about 5% of 1.0 for soft currency. That ratio is a heuristic from the Roblox balance guide, not a documented rule.
4. **Pick the first ten levels or upgrades for speed.** Early purchases should take 3–10 seconds each, so the player learns the loop while the numbers are still small.
5. **Decide the long-term engine** (rebirth, prestige, collection completion or seasons) before launch. Retrofitting one changes every number.

Warning signs of inflation: prices in player trades rise while nothing changed, the top 1% hold most of the wealth (Gini climbs), new players cannot afford starter items at market price, and the sink ratio drifts below 0.9. Fixes, in order of preference: add desirable sinks (cosmetics, upgrades, consumables), add a new currency for the event instead of inflating the old one, then and only then reduce faucets.

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

## Checklist before shipping an economy

- [ ] Every currency has a documented faucet list and sink list.
- [ ] Sink ratio modelled at 0.95–1.05 for week one.
- [ ] First ten upgrades take 3–10 seconds each; first rebirth within the first or second session.
- [ ] Rebirth wait ratio ×1.2–1.5.
- [ ] Offline income capped and stated.
- [ ] Odds shown equal odds rolled; pity disclosed; luck boosts disclosed live.
- [ ] All economy mutations server-side, rate-limited and logged with `AnalyticsService:LogEconomyEvent`.
- [ ] Event rewards use event currency.

For the grep-able original, search `references/knowledge-base.md` for `## 1.5`, `## 1.6` and `## 3.5`.
