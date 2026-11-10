# Economy and progression design

How to model, tune and repair a game economy. Open it when you design currencies, XP curves, upgrade prices, rebirths or luck for a new game, or when a live game shows inflation, a progression wall, a dupe or a rebalance backlash (jump to "Level-up"). Distilled from knowledge-base sections 1.5, 1.6 and 3.5 and extended on 2026-11-10. Every number is a starting point to validate in playtests, not a law. Tags: `[official]` Roblox docs, `[community]` forum/press practice (heuristic), `[VS]` version-sensitive (check https://create.roblox.com/docs), `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its numbers are rules of thumb or simulated unless stated).

## Start here by level

| Level | Do these | Ignore for now |
|---|---|---|
| Beginner | One soft currency with a faucet list and a sink list. Write a time-to-afford target for each purchase type. First ten purchases 3–10 s each. Geometric upgrade costs (g 1.07–1.15). Every change to a balance happens on the server. | Hard currency, trading, simulation, pity ramps |
| Intermediate | Derive every price from one income table and check p ÷ g per zone. Payback and the greedy path for each upgrade track. A declared multiplier cap and free-to-payer gap. Event currency with a lifecycle. `LogEconomyEvent` from one wallet with stable SKUs; hours of income held per zone. | Custom telemetry, cross-server markets |
| Expert | Agent-based simulation on the game's own config, run in CI. Cohort telemetry with robust-z alerts. Effective pity rates and item supply per day. Market design for trading (binding, robust prices, taxes, cooldowns). Staged rebalances with a numeric hypothesis. | — |

Terms: a **faucet** creates currency, a **sink** destroys it; **soft** currency is earned in play, **hard** (premium) currency is mainly bought with Robux; **time to afford** is price ÷ income per minute.

Contents: Design first · Time to afford · Hard currency or direct Robux · Progression curves and upgrade tracks · Rebirth · Paid multipliers · Offline income · Large numbers · Random rewards, pity and supply · Event currency · Pricing soft currency · Server rules · Trading and dupes · Measuring a live economy · Simulation · Live rebalancing and resets · Level-up table · Review gate · Sources.

Related: monetization-and-policy.md (what is sold, price ladders, boost rules); gameplay-systems-cookbook.md §1 Currency and wallet, §3 Shop, §5 Upgrades and rebirth (implementation); data-and-purchases.md (saving balances, dupes, receipts); templates/economy-balance-sheet.md (the fill-in sheet).

## Design the economy before you build it

1. **Name every currency and resource, then limit them.** The Creator Analytics economy dashboard shows up to 5 currencies and the event limits allow 10 resource types. Fewer currencies are easier to balance and to read.
2. **For each currency, write down who earns it, how (faucets), and what it is spent on (sinks).** Track every source and sink in a sheet. If a currency has no sink, it will inflate; if it has no faucet besides purchase, it is a hard currency and must be priced as one.
3. **Keep sources minus sinks close to zero over a player's week.** The sink ratio (total spent divided by total earned) should sit within about 5% of 1.0 for soft currency. That ratio is a heuristic from the Roblox balance guide, not a documented rule.
   Conflict: LihFolk's model argues the level is the wrong target in a growing exponential game: balances rise with progress, so the daily sink ÷ faucet ratio sits below 1 (0.29 in its simulated zone game with no endgame sink) and only the trend and the per-zone view carry information `[lihfolk]`. Trust both in their place: 0.95–1.05 is the design target for a settled player's week in the spreadsheet; on live data read the trend within a progress band (see "Measuring a live economy").
4. **Pick the first ten levels or upgrades for speed.** Early purchases should take 3–10 seconds each, so the player learns the loop while the numbers are still small.
5. **Decide the long-term engine** (rebirth, prestige, collection completion or seasons) before launch. Retrofitting one changes every number.

Warning signs of inflation: prices in player trades rise while nothing changed, wealth concentrates inside one progress band (whole-population Gini is high by construction in exponential games), new players cannot afford starter items at market price, and the sink ratio for settled players drifts below 0.9 and keeps falling. Fixes, in order of preference: add desirable sinks (cosmetics, upgrades, consumables), add a new currency for the event instead of inflating the old one, then and only then reduce faucets.

## Time to afford: price everything from one income model

Players feel waiting time, not prices. For every purchase compute `T = price ÷ income per minute at the point the purchase becomes relevant`, and keep T inside a band chosen on purpose `[lihfolk]`:

| Purchase | Target T, active play (rule of thumb) |
|---|---|
| Small upgrade, consumable | 1–3 min (3–10 s for the first ten purchases of the game) |
| Meaningful upgrade (skill node, forge level) | 5–15 min |
| Zone gate, big unlock | 15–45 min |
| Rebirth or prestige | 1–3 sessions (the first one inside session one) |

```
zone k: income I_k = I0 × g^k, gate P_k = P0 × p^k   →   T_k = T0 × (p ÷ g)^k
T0 = 10 min:  p ÷ g = 1.1 → 23.6 min at zone 9;  1.0 → 10 min;  0.9 → 3.9 min (the late game blurs past)
```

- Only the ratio p ÷ g matters. Below 1 is the commonest hidden inflation: no single gate looks wrong, but late zones are skipped. Much above about 1.15 builds walls: in LihFolk's simulation, moving from 1.15 to 1.23 roughly quadrupled the share of stuck players and cost about 5% of DAU within a month `[lihfolk]` (simulated; trust the direction, not the size).
- One model, every system: gates, upgrade boards, forges and quest rewards all read the same income table. A system priced by hand is the one that breaks when income changes (their reference game cut cash income to ×0.55 and found a forge upgrade at 150K that should have cost 12–15K) `[lihfolk]`.
- Carry-over: T assumes arriving with nothing. If old zones can be farmed forever, players arrive holding several gates' worth. Make the newest zone the best place to earn, and pay quests as a share of the next gate's price so they stay relevant.
- An exponential soft currency cannot carry fixed-price content: a 250-coin cosmetic is free two zones later. Put flat-priced goods in a flat currency (premium, event tokens or a separate style currency), or cap multipliers so the flat scale survives.

## Hard currency or direct Robux prices?

Default `[house]`: price boosts, passes and packs directly in Robux and keep one soft currency. Add a hard currency (gems) only when one of the "for" rows is a real need.

| | For a hard currency | Against |
|---|---|---|
| Player trust | Free players can earn premium items slowly | Hides the real price; leftover balances cause complaints |
| Policy | — | Anything random bought with a Robux-bought currency is a paid random item, even when the currency can also be earned `[official]`; odds, PolicyService and trading gates then apply to every gem sink |
| Operations | Monthly subscription drops and season-pass rewards have a unit to pay in `[official]` | One more of the 5 dashboard currencies to balance; a new currency is a new scam and dupe target `[community]` |
| Pricing | Bundles and sub-1 R$ granularity | Roblox's subscription guide starts from "how much play earns the equivalent of 1 Robux"; keep that rate legible. A DevForum reply recommends rescaling so 1 gem ≈ 1 R$ rather than an odd rate `[community]` |

If you add one: fixed public exchange rate, no random sink for restricted players, never tradeable, and log every source and sink with `AnalyticsService:LogEconomyEvent` (transaction type `IAP` for purchases).

One job per currency `[lihfolk]`. A new currency must answer three questions: what does it buy that nothing else buys, where does it come from that nothing else pays, and what happens to it when the player stops caring (if the answer is "it piles up", it is a future inflation problem). A session game rarely needs more than one soft, one premium and one live event currency; crafting materials are inventory items with a count, not currencies. Two counters fit a phone's top bar; three crowd it.

Premium-currency rules that are hard to undo `[lihfolk]`:

- **Anchor.** Fix a value (1 gem ≈ 1 R$) and derive every pack, price and free grant from it. Changing it later reprices the whole shop.
- **No stranded balances.** Make every gem price and every pack size a multiple of one unit. Packs of 100 / 550 / 1,200 against prices of 80 / 400 / 1,000 strand 20–200 gems per purchase; prices of 50 / 250 / 600 let every pack be spent to zero.
- **Paid and free buckets.** Store `GemsPaid` and `GemsFree` separately from day one, with a written spend order. Refund handling, paid-item provenance (trading and paid-random rules) and the free-share metric all need the split; an item bought with a mix counts as paid.
- **Free share** = free gems granted ÷ all gems granted. Above about half, pack sales erode month by month; near zero, free players never learn what gems buy. A 25-gem daily bonus on a pass is about 750 R$ of anchor value per holder per month: decide that on purpose.
- **Sinks before packs.** A premium currency with nothing worth buying is not worth selling.
- **Boosters priced in a fixed gem amount** become the best soft-currency faucet late in the game, because their yield scales with income. Bound the effect or price it against income.
- **Conversions run one way**, from scarcer to commoner (premium → soft, event leftovers → soft). For any loop of conversions multiply the best-case rates; a product above 1 prints money. Floor what the player receives, ceil what they pay, and set a minimum amount, or scripts will convert one unit at a time.
- Premium currency never trades, and currency bought with Robux never expires.

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

### Upgrade tracks: payback, natural caps and the greedy path

Adapted from LihFolk's pricing-curves note `[lihfolk]`; the maths is standard.

- A track is two curves, cost(L) and benefit(L). For income upgrades players respond to **payback** = cost(L) ÷ extra income per minute, and stop buying when payback exceeds the time they expect to stay in the zone (an hour is a workable model).
- Additive bonus with geometric cost has a natural cap: `L* = ln(paybackMax × gainPerLevel ÷ baseCost) ÷ ln g`. With +4 coins per minute per level, cost 150 × 1.15^L and a 60-minute tolerance, L* ≈ 3.4. The real length of the track is L*, not `maxLevel`. Scale track costs with zone income, or each new zone adds ln(income growth) ÷ ln g levels (6.8 at ×2.6 and g = 1.15) and tracks are maxed in seconds.
- A multiplicative per-level bonus (×1.04 per level) has no natural cap: payback grows only by g ÷ 1.04 per level. Keep g well above the per-level multiplier and count the track in the multiplier stack. This is the commonest cause of income exploding after an update.
- Price power tracks (damage, speed) in minutes of income. If kills limit income, +4% damage ≈ +4% income; if half the income is idle, it is worth half and should cost half.
- **Greedy-path test.** Players and guides always buy the best benefit per coin. Simulate one session of greedy buying: if one track ends at level 40 and the rest at 2, the rest are decoration. Fix benefit per coin, not with prerequisites.
- g by use: 1.07–1.10 for dozens of levels per session, 1.12–1.18 for a few per session, 1.2+ only near a cap. A polynomial cost on an uncapped track gets relatively cheaper forever; use it only on short, capped tracks.
- **Rounding.** Round to two significant figures (three when g is under about 1.08), then run a monotonic pass so no level costs the same as or less than the one before. A "nice number" series (1, 1.2, 1.5, 2, 2.5, 3 …) with forced increases turns g = 1.15 into about 1.26, six times the intended price by level 20. Store the rounded prices in config so server, UI and model agree.
- **Buy-max.** Largest affordable n from level L0 with M coins: `n = floor(ln(1 + M(g − 1) ÷ (base × g^L0)) ÷ ln g)`; confirm total(n) ≤ M < total(n + 1) because floats drift by one at the edge (base 100, g 1.15, L0 10, M 50,000 → n = 21, cost about 48,065). With rounded or hand-edited prices use prefix sums and a binary search instead. The client sends "buy max on track X", never a count; the button shows what the server will charge ("Buy max: 21 levels, 48.1K").
- Caps on speed and cooldown tracks come from what the server can validate and streaming can bear; fit the price to the cap, not the reverse.
- Respec: partial refunds of 50–80% are a sink and keep choices meaningful; full refunds on income tracks invite loop-probing.

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

Conflict (which model): LihFolk prefers an additive multiplier with a cost that grows per rebirth (`C(n) = C0 × 1.25^n`) plus a second reward (a slot, an ability, a cosmetic), arguing that a multiplicative multiplier forces cost to grow at the same rate and so becomes cosmetic `[lihfolk]`. The two views meet at the wait ratio. Additive p = 0.5 with r = 1.25 gives ratios of 0.83, 0.94, 1.00, 1.09 and 1.15 at k = 0, 1, 2, 5 and 10: the first rebirths get shorter (a good hook) and later ones settle toward ×1.25. Default to additive with an escalating cost and a non-numeric second reward; use multiplicative only with r ÷ q held inside 1.2–1.5. A constant rebirth cost under any model ends in runs of a few minutes. If a rebirth resets upgrade tracks, price the tracks from the run's income including the multiplier.

## Paid multipliers and the curve

Paid boosts shift the curve; they do not bend it. Model the payer before you price anything.

```
stack M = pass × timed boost × VIP × friend × group          e.g. 2 × 2 × 1.2 × 1.2 × 1.1 ≈ 6.3
extra levels bought by M on a geometric line = log M / log g  (2× → 5 levels at g = 1.15, 10 at g = 1.07; 4× → 10 and 20)
time to any goal for the payer = free time / M                (rebirth wait ratio r / q is unchanged)
content runway for the payer = hours of new content / M       (10 h weekly update ÷ 6.3 ≈ 1.6 h)
```

- Geometric prices absorb multipliers; flat-priced content (zone unlocks, event shops, fixed packs) does not. Price every flat item from top-decile income, not the median.
- Cap the stack `[house]`: permanent paid multipliers ≤ 4× in total, everything including timed boosts ≤ 8×. Same-type boosts extend time, never multiply. Personal paid boosts count play time and pause offline; server-wide boosts run in real time and show their end time (monetization-and-policy.md). Without a cap each new pass shortens the life of every future update.
- Conflict: the +1 / Evolution format sells one-time ×8 / ×15 / ×30 / ×99 training pads (market scan), far above this cap. It works there because gates grow about ×4 per stage, so a ×99 pad is worth log 99 / log 4 ≈ 3.3 stages. Follow the format norm in stage-gated lane games and add stages weekly; apply the cap everywhere content is not geometric.
- Free-to-payer gap `[house]`: a free player reaches any milestone in at most 3–4× the payer's time. Beyond that the game reads as pay-to-win and ratings pay for it.
- Timed boosts gain value as income grows; fixed-amount currency packs lose it. Size packs in minutes of the buyer's current income ("30 min of your income: 9,330 Cash" at 311 per minute), compute the amount on the server and show the exact number before purchase `[house]`. Rewarded-video rewards should likewise "be scaled so that they remain valuable to users as they advance through the game" `[official]`.
- Rewarded video is a faucet: the reward must "not inflate currency or unbalance the game's economy" `[official]`. Cap ad income at about 10–15% of a day's earnings `[house]`.
- No paid multiplier applies to anything ranked or competitive (house rule 3).
- Stacking rule `[lihfolk]`: add bonuses inside a category (all potions, all passes) and multiply across categories. Fully multiplicative stacking explodes with the number of sources (five 1.5× sources = 7.6×). Compute the multiplier in one function, show its breakdown in one tooltip, and generate product descriptions from the same numbers (their reference VIP pass said 1.5× while the code gave 2×).
- Track the **payer progress gap** live: median zone of payers ÷ non-payers at equal playtime. It is the measured form of the declared gap.

## Offline income

```
offline = floor(min(secondsAway, maxHours × 3600) × ratePerSecond × efficiency)
```

Use efficiency 0.25–0.5 and a cap of 8–12 hours. Say what the cap is in the UI, and never claim "earning while away" beyond the honest cap. A 2× offline earnings product or rewarded-video doubler is a good non-invasive sale on return.

Conflict (offline cap): LihFolk suggests about 2 hours at 50% because long caps devalue playing `[lihfolk]`; this skill's default is 8–12 hours at 25–50% so an overnight return pays. Keep the longer cap for the day-1 return, use the lower efficiency, and state the cap either way.

## Large numbers

Past about 1e15 double precision loses integer precision. Store a mantissa and exponent pair, or a custom big-number type, once your top balances approach that range. Round before you format with K/M/B/T suffixes so 999,999 does not show as "1000K".

## Random rewards, luck and pity

- Show every outcome and its numeric odds before purchase, summing to exactly 100%. Roll from the same weight list you display. (See monetization-and-policy.md for the paid-random-items rules and the PolicyService gate.)
- **Luck boosts are probability modifiers.** Example: 2× Luck multiplies weights of non-common tiers by 2: Common 90 / Rare 18 / Legendary 2 → 81.82% / 16.36% / 1.82% after normalising. Show the boosted odds live while the boost is active.
- **Server Luck** applies to everyone in the server; announce the activator and the end time to all players and show the boosted odds to all.
- **Pity**: guarantee the top tier by a fixed count (for example at 100 rolls). With a 1% rate, 63.4% of players already have it by roll 100, so pity protects the unlucky tail without changing the average. Disclose pity rules.
- **Direct sale at expected value** is the fallback when paid random items are restricted: a 10 R$ roll with a 5% chance at the item implies a 200 R$ direct price.
- **Effective rate of a pity ramp** `[lihfolk]`: with chance c(k) on roll k since the last hit and S(k) = Π(1 − c(j)) for j ≤ k, expected rolls per hit E = Σ S(k) for k = 0 … K − 1, and the effective rate is 1 ÷ E. Base 0.6%: no pity 167 rolls (median 116, p90 383); hard pity at 90 gives 69.7 rolls, 1.43%; a ramp of +6 points per roll from 74 with hard pity at 90 gives 62.3 rolls, 1.61%. With hard pity alone about 59% of players reach the guarantee, so most experience "guaranteed at 90", not "0.6%". Disclose the rule and the effective rate; community guides find a hidden ramp within days.
- **Featured 50/50** (lose once, next top-tier hit is guaranteed featured): 1.5 top-tier hits per featured item, about 93 rolls on that ramp and 180 at worst. Say whether the guarantee and the counter carry across events and pools, and never change that mid-event `[lihfolk]`.
- **Duplicate protection**: completing a tier of n equally likely items takes n × H(n) rolls without it (5 items 11.4, 20 items 72, 50 items 225) and exactly n with it. It is a 2–4.5× pacing buff, it starves fusion and trading of duplicates, and in a paid pool it is a probability modifier: per-item odds must reflect the player's own collection `[lihfolk]`.
- **Item supply** `[lihfolk]`: copies per day = rolls per day × p × average luck. 50M rolls a day at 1 in 1,000,000 and 2× average luck mints about 100 copies a day, 3,000 a month. Every luck source multiplies the supply of every rare at once: cap total luck and show the cap, add new top tiers instead of raising luck, and treat a 2× luck weekend as a supply event to model before scheduling.
- **Copy sinks**: fusion at three copies per star consumes 3^5 = 243 base copies for a five-star item (about 2.43M rolls for a 1-in-10,000 item); it scales with supply and gives a reason to keep rolling owned items `[lihfolk]`.
- **Rolls versus progress.** If rolls cost the currency that also buys gates, some players roll their progress away (in LihFolk's first simulation non-payers stalled in zone 0 for a month). Use a separate roll currency, or a roll cost that scales slowly, or nudge toward the gate `[lihfolk]`.
- **Prove display = roll**: in CI, roll each table a million times in every modifier state and compare with the displayed odds (chi-square) `[lihfolk]`. Never display a non-zero chance as 0%.

## Event currency example (why events need their own currency)

A fishing game sells fish: Catfish 70% at 10 G, Trout 20% at 20 G, Salmon 10% at 30 G, expected value 14 G per cast. (The Roblox doc has a typo saying "Salmon 30% = 3 G"; the corrected 10% is used here.) Adding a 0.1% Golden Salmon worth 1,000 G, taken from Catfish's share, lifts EV to 14.99 G (+7.1%). If the event triples participation, daily income rises to about 44,970 G (+221%) and the main currency inflates. The fix is a unique event currency with its own sinks that expire with the event.

Lifecycle `[lihfolk]`: announce → earn window (1–3 weeks) → spend-only grace (3–7 days) → convert or expire → archive (shop removed, ledger kept for support). Key balances by event id (`Event[eventId]`) and convert lazily on the player's next load, so a late returner is not punished and no batch job races live servers; log all of them under one analytics currency with the event id in a custom field. Convert leftovers into soft currency only, at 10–25% of what they bought in the event shop and capped at about one gate at the player's zone. Warn three days and one day before expiry: silent expiry is the top complaint after any event. Never sell an expiring currency; sell the track (a product that unlocks rewards), not the tokens.

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
| Player leaves or server dies mid-trade | "Swap, then save both" is not enough: a crash between the two saves leaves one item in two profiles. Use the two-profile commit protocol in data-and-purchases.md (intent in both profiles, write-once decision record, one settle mutation per profile, recovery that stays locked when unsure) |
| Stale data in two servers | Session-locked profiles (data-and-purchases.md); trade only when both profiles are loaded in the same server |
| Offline gift applied twice, or lost | Debit the giver and confirm that save first, then deliver through a message keyed by a unique gift id; applying is idempotent, and the giver's ledger entry allows a retry |
| Remote spam racing two trades | Per-player trade lock and token-bucket rate limit |
| Item with no identity | Give every tradeable item a GUID at mint (`HttpService:GenerateGUID(false)`); keep a mint ledger (count minted per item type) |

Operations: a `trading_enabled` and a `gifting_enabled` Configs kill switch; an append-only trade log; an alert when one GUID appears in two inventories or when owned count exceeds minted count; quarantine flagged items instead of deleting them (quarantine means kept and usable, but untradeable and flagged until reviewed; removal only from accounts with direct evidence), so good-faith holders lose nothing; new-account cooldown and a per-day value cap. Pausing the feature for a week costs less than a crashed item market. When a dupe is live, follow "Runbook: dupe incident" in data-and-purchases.md step by step.

### Once trading works: designing the market

Once players can trade you no longer set item values; your levers are supply, friction and information `[lihfolk]`.

| Lever | Practice (rules of thumb) |
|---|---|
| Binding | Decide per item class: tradeable (collectibles, cosmetics), bound on use, account-bound (progression power, quest rewards, the very top tier), or tradeable after a cooldown. Tighten binding only for new items; rebinding existing ones confiscates value. |
| Trade cooldown | New, purchased or dupe-sensitive items cannot be traded for 3–7 days. Honest players barely notice; dupes, stolen-account sweeps and real-money sales are delayed long enough for detection to act. |
| Format | Start with same-server barter; add a hub place when players cannot find partners; add a cross-server listing board only with tooling to watch it. A soft-currency market merges the item and coin economies: a big step. |
| Price display | Never the last trade (one alt trade sets it). Median of the last 20–50 trades, at most one per pair of accounts, young accounts excluded, "not enough data" under about 10, and show the trade count. That defeats wash trading. |
| New-player protection | Lopsided-trade warning with a second confirmation when one side is worth under a third of the other; playtime or progress requirement before trading unlocks; receive caps for young accounts. |
| Fees | A trade destroys nothing unless you add a sink: a sales tax on soft-currency markets (above about 10–15% trades move off-market), a flat fee or a consumable trade ticket for barter. Never tax the Robux side. |
| Supply | Every tradeable copy lives forever: 200 copies a day is 18,000 in 90 days. Fusion and crafting that consume copies, new top tiers, published fixed supply for limited items. |
| Thin markets | Per-account holding caps on limited items against cornering; listing caps (5–20) and server rate limits against bots; a short random delay before a listing becomes buyable against snipers. |

- Cross-server boards: MemoryStore is only the index. Escrow the item inside the seller's own profile first, claim a listing with `UpdateAsync` and act on its **return value** (the transform can run more than once), check the price the buyer saw, and settle through a durable decision record plus a mailbox `[lihfolk]`. Implementation belongs with data-and-purchases.md.
- Real-money trading and scams create more support load than exploits. Budget moderation time before launch, keep an in-game trade history as evidence, and do not launch a market for a young audience or before item supply is modelled.
- Do not A/B test the supply or price of tradeable goods or any server-wide multiplier: variants leak into each other's market. Use a staged rollout with a before-and-after comparison.


## Measuring a live economy

Totals hide most problems; the useful numbers are distributions inside a progress band and flows broken down by source `[lihfolk]`.

| Metric | Definition | Catches | Reading |
|---|---|---|---|
| Hours of income held | balance ÷ income per hour, p10 / p50 / p90 per zone or level band | Surplus with nothing to buy; walls | Mid-game median under 1–2 h is healthy; 20+ h late game means no top-end sink |
| Net flow by source | sources − sinks per transaction type per day | A sink that no longer fires; a faucet left running | A sink halving overnight is usually a broken shop or remote |
| Sink ÷ faucet trend | per currency per day | Sinks losing ground | Falling for weeks with unchanged content = inflation |
| Velocity | spent per day ÷ average held | Hoarding, before balances look alarming | Falling while balances rise = saving or a dead shop |
| Observed time to afford | unlock → purchase, p50 and p90 | Drift against the model | A quarter of the model = an unmodelled faucet (code, event, exploit) |
| Gate conversion | share buying the gate within 3 days of unlocking | Walls hidden by survivorship | Falling conversion with flat time to afford is the signature of a wall |
| Concentration | Gini inside one progress band; top 0.1% share | Exploits and dupes | Whole-population Gini is structural in exponential games (0.92 in LihFolk's model) and proves nothing |
| Item supply | new copies of each top-tier item per day, per DAU | Dupes, luck events, table mistakes | Compare against rolls × odds × luck |
| Price index | robust prices of a fixed basket vs a base week | Item inflation in trading games | Falls a week after a luck event |
| Free share of premium | free ÷ all premium granted | Eroding pack sales | Above about half is a warning |

- **Segment first, then aggregate.** A whole-population median moves with who is playing (a featuring brings poor new players, churn removes them); every band can be improving while the total worsens. Group by zone, level or rebirth band, or by join week.
- **Survivorship.** Players who quit at a wall stop producing data, so the ones you still see look fine. Pair every time-to-afford number with its gate-conversion funnel.
- **Logging discipline** `[official]` limits, `[lihfolk]` practice: call `LogEconomyEvent` from one wallet module, after the change is committed, with the ending balance; treat SKU and transaction-type strings like data-store keys (a rename splits history). Limits `[VS]`: 10 resource types tracked, 5 currencies on the dashboard, values grouped as "Other" beyond 20 transaction types and 100 item SKUs, 3 custom fields (8,000 combined values), 120 + 20 × CCU requests per minute. Spend the custom fields on progress band, config version and experiment variant.
- **Alerts.** Compare today with the same weekday over the last four or more weeks using a robust score, `z = (today − median) ÷ (1.4826 × MAD)`, after dividing by DAU. Investigate above 3; page someone above 5 for free premium currency and top-tier item supply. Day-one alerts: premium faucet spike, rare-supply spike, top-0.1% share doubling day over day, a sink falling by half, gate conversion dropping in one zone only `[lihfolk]`.
- **Own aggregates** (only when the dashboard cannot answer: distributions, per-cohort views, item supply): count in memory per server, flush every five minutes to daily keys sharded by a hash of `game.JobId` (16 shards) so no key becomes hot, keep bounded samples rather than censuses, store no user ids, stay under about 5% of the write budget, and never let the flush delay a profile save at shutdown `[lihfolk]`.
- Below a few hundred DAU the distributions are noise: watch individual journeys instead.

Conflict: LihFolk states the built-in experiment metrics exclude economy health (October 2026). The docs mirror of 2026-11-07 describes a Custom metric set with up to three metrics built from economy, funnel or custom events `[official]` `[VS]`. Use it, and still tag economy events with the variant for anything it cannot express.

## Simulate before launch and before every rebalance

A spreadsheet models the average player. An agent-based simulation (many simulated players with different habits) shows who holds the money, which archetype finishes the content in a week, and what a one-number change does to churn `[lihfolk]`. It is a comparison tool: between two runs on the same seeds, the direction and rough size of the gap can be trusted; an absolute number never can.

| Ingredient | Starting values to replace with your own |
|---|---|
| Archetypes (share, sessions per day, mean minutes, income multiplier) | Casual 55% / 0.8 / 12 / 1×; regular 30% / 1.5 / 25 / 1×; grinder 12% / 2.5 / 55 / 1×; payer 3% / 2.0 / 35 / 2× `[lihfolk]`; session lengths drawn from an exponential distribution for a long tail |
| Spending policy | Explicit and greedy: gate first, then an upgrade that pays back within an hour, then rolls from a fixed share of income |
| Churn | A base daily chance plus an extra chance on days the player ends stuck (next goal more than 60 min away) |
| Population | New players every day for 30 days, so day 30 mixes cohorts like a live game |
| Outputs | The same names as live telemetry: hours held, sink ÷ faucet, stuck share, top-item supply, share of coins held by finishers |

What their baseline exposed (simulated): finishers held 99% of all coins (no endgame sink), grinders finished ten zones well inside a month (content runway shorter than a monthly cadence), and casual players sat at a median of zone 1. Two tests: steeper gates (p ÷ g 1.15 → 1.23) quadrupled the stuck share; an endgame roll sink lifted sink ÷ faucet from 0.30 to 0.90 but minted 136% more Mythics. Every sink is also a faucet of something: check what it mints.

Minimal model (unexecuted sketch; session-step, gates only; extend with upgrade tracks, rolls and event currency only when a decision needs them):

```lua
--!strict
type Archetype = { share: number, sessionsPerDay: number, meanMinutes: number, mult: number }
type Config = {
	days: number, joinsPerDay: number, zones: number, incomeBase: number, incomeGrowth: number,
	gateBase: number, gateGrowth: number, baseChurn: number, stuckChurn: number, stuckMinutes: number,
	archetypes: { Archetype },
}
type Agent = { kind: Archetype, zone: number, coins: number, active: boolean }

local function simulate(cfg: Config, seed: number): (number, number) -- active players, stuck share (last day)
	local rng = Random.new(seed)
	local agents: { Agent } = {}
	local active, stuck = 0, 0
	for _ = 1, cfg.days do
		for _ = 1, cfg.joinsPerDay do
			local roll, kind = rng:NextNumber(), cfg.archetypes[#cfg.archetypes]
			for _, a in cfg.archetypes do
				roll -= a.share
				if roll <= 0 then kind = a; break end
			end
			table.insert(agents, { kind = kind, zone = 0, coins = 0, active = true })
		end
		active, stuck = 0, 0
		for _, p in agents do
			if not p.active then continue end
			local sessions = p.kind.sessionsPerDay // 1 + (if rng:NextNumber() < p.kind.sessionsPerDay % 1 then 1 else 0)
			for _ = 1, sessions do
				local minutes = math.max(3, -math.log(1 - rng:NextNumber()) * p.kind.meanMinutes)
				p.coins += cfg.incomeBase * cfg.incomeGrowth ^ p.zone * p.kind.mult * minutes
				while p.zone < cfg.zones - 1 and p.coins >= cfg.gateBase * cfg.gateGrowth ^ p.zone do
					p.coins -= cfg.gateBase * cfg.gateGrowth ^ p.zone
					p.zone += 1
				end
			end
			local income = cfg.incomeBase * cfg.incomeGrowth ^ p.zone * p.kind.mult
			local wait = if p.zone < cfg.zones - 1 then (cfg.gateBase * cfg.gateGrowth ^ p.zone - p.coins) / income else 0
			local isStuck = wait > cfg.stuckMinutes
			if rng:NextNumber() < cfg.baseChurn + (if isStuck then cfg.stuckChurn else 0) then
				p.active = false
			else
				active += 1
				stuck += if isStuck then 1 else 0
			end
		end
	end
	return active, if active > 0 then stuck / active else 0
end
```

Operating rules `[lihfolk]`: compare baseline and change on identical seeds and average five or more; read prices from the game's own config module so a patch cannot leave the model behind; after launch replace archetypes and churn with measured ones and replay a known week (more than about 25% off: fix the model before using it); keep golden day-30 numbers in CI and fail a config change that moves sink ÷ faucet or stuck share by more than 10%, or top-item supply by more than 20%, without an explanation. Do not simulate cosmetic-only economies, prototypes whose structure changes weekly, or decisions you will not act on.

## Live rebalancing without angering players

1. Measure first: sources and sinks from `LogEconomyEvent`, median and top-decile wallet by cohort, days-to-afford the next key item.
2. Prefer, in order: a new desirable sink → a new tier priced for today's inflated income → event currency → slower growth of future faucets → a cut to an existing faucet (last resort).
3. Never reduce something bought with Robux. Roblox's own guidance when a pass is replaced: existing holders "should continue to receive the benefit they paid for" `[official]`. Grandfather owners or let them choose compensation.
4. Buff the weak option rather than nerf the strong one where the maths allows; players read a nerf as a loss.
5. Ship through Configs to an Experiments cohort, one lever at a time (Roblox's balance guide recommends Experiments for price tests and Configs for live tuning `[official]`), and watch seven days: sink ratio, D1/D7, like ratio, pack and boost sales.
6. Announce before it ships, with the reason and the numbers. The Roblox backlashes that reached the press were changes that arrived without notice or that players read as taking earned value away (Welcome to Bloxburg's job-pay change; the 2026 cross-game pass sales shutdown, which a creator petition says came "without any warning") `[community]`.
7. Compensate on login when anyone loses value: currency, a timed boost or a cosmetic.
8. Roll back or wipe only for exploits, only on affected accounts, and say so publicly.
9. State the hypothesis with a number before shipping ("zone 6 gate p50 is 41 min against a 20-min target; −40% should bring it near 25 and lift 3-day gate conversion from 52% to 65%"), check it in the simulation, then judge after a full week: many changes look good on day one (a windfall) and bad by day seven (content finished) `[lihfolk]`.

Reading a change after it ships `[lihfolk]`:

| You see | Likely meaning |
|---|---|
| Target metric moved, churn rose in a later zone | Players now reach the next wall sooner; check that zone |
| Hours held rose in every zone | A faucet grew or a sink weakened more than intended |
| Velocity fell while balances rose | The shop has lost its appeal, or players are saving up for something |
| A week after a luck event the rare price index dropped | Supply shock; decide whether to add a copy sink |
| Metric moved on one platform only | A UI problem on that platform, not the economy |

Fixing an economy that is already inflated, least to most disruptive `[lihfolk]`: a repeatable top-end sink (does not touch existing balances) → higher prices for new content only → slower faucets (announce it) → revaluing balances (reads as confiscation; never touch paid value) → a reset. Fix the model, then re-derive every price from it; patching the one price players complain about leaves the rest on the old model.

Resets and wipes `[lihfolk]`. Good reasons: competitive seasons (new leaderboard store per season, never a cleared one), opt-in seasonal modes, a beta declared provisional, a cleanly reversible exploit. Weak reasons: unmeasured "inflation", a rebalance that could be migrated, a relaunch of a dead game. Rules: nothing bought with Robux is lost without equal or better compensation; receipt records and settings are never wiped; announce 3–4 weeks ahead with a "what stays, what goes" table; stop selling anything resettable a week before and exempt purchases made in the final window; convert rather than erase (soft currency into a permanent cosmetic tier plus a small head start), running the conversion once per profile on load; dry-run the conversion on a sample of real profiles to see who loses most; and greet each player with their own numbers on return, because abstract rules read as loss and personal numbers read as a trade.

## Level-up: economy symptoms → likely cause → fix

The knowledge base (`## 3.5`, "Inflation and deflation") has the basic signal table; these are the live-game cases it does not cover.

| Symptom | Likely cause | Fix |
|---|---|---|
| Veterans clear a weekly update in one session | Paid and rebirth multipliers outran flat-priced content | Price new content geometrically from top-decile income; cap the multiplier stack; add a prestige sink |
| Funnel drop at one specific upgrade or gate | Local wall: g too high early, or a gate jump far above ×4 | Flatten that step; first ten purchases 3–10 s each |
| Rebirth-count histogram piles up at k | Cost growth r outrunning the multiplier at that k | Lower r (or change model) until the wait ratio is ×1.2–1.5; add a non-numeric rebirth reward |
| Currency-pack sales decay week over week | Inflation made fixed packs worthless | Packs sized in minutes of current income; add sinks |
| Sink ratio under 0.9; wallets pile up | Nothing left worth buying | Aspirational cosmetics, upgrade tiers, consumables |
| Sink ratio above 1.1; sessions shorten | Starved faucets | Quest and offline income up; cheaper early upgrades |
| Top 1% wallet share and trade prices climb fast | Uncapped faucet, exploit or dupe | Server caps, anomaly review, GUID audit |
| Owned count of an item exceeds minted count; leaderboard jumps overnight | Dupe | Dupe incident runbook in data-and-purchases.md: kill switch, find duplicated GUIDs, quarantine (kept, usable, untradeable), patch, announce |
| Main-currency pack sales drop after an event | The event paid out main currency | Event currency with sinks that expire |
| Free players call the game pay-to-win | Free-to-payer time gap above 3–4×, or paid power in a ranked mode | Cap the stack; move paid value to convenience and cosmetics |
| Anger after a balance patch | No notice, or paid value reduced | Protocol above: announce, grandfather, compensate |
| Boost sales fall as players progress | Boost value shown as "2×" while prices grew faster than income | Show the gain in currency at the player's rate; lower late-game g |
| Late zones blur past; observed time to afford shrinks with zone | p ÷ g below 1 | Raise gate growth for new content; re-derive from the income table `[lihfolk]` |
| One upgrade track maxed, the others untouched | Benefit per coin far apart on the greedy path | Reprice in one value unit; simulate greedy buying `[lihfolk]` |
| Income explodes after an update | A multiplicative track with g near its own multiplier, or an uncounted stacking source | g well above the multiplier; additive buckets `[lihfolk]` |
| Cosmetics become free mid-game | Fixed prices in an exponential currency | Move them to a flat currency `[lihfolk]` |
| "Inflation" that tracks marketing pushes | Whole-population medians | Segment by progress band `[lihfolk]` |
| Gem-pack sales fall month over month | Free share of premium too high, or no premium sinks | Track free share; add sinks before packs `[lihfolk]` |
| Complaints about leftover gems or vanished event tokens | Pack sizes off the price unit; silent expiry | Common unit; grace period, warnings, conversion `[lihfolk]` |
| Rare prices crash a week after an event | Luck event doubled supply | Model inflow first; add a copy sink `[lihfolk]` |

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
- [ ] Tradeable items carry GUIDs; trade and gift kill switches exist; two-sided swaps use the two-profile commit protocol in data-and-purchases.md.
- [ ] Time-to-afford bands written per purchase type; p ÷ g checked per zone; every system priced from the same income table.
- [ ] Each upgrade track has cost and benefit curves, a known natural cap, monotonic rounded prices and server-side buy-max.
- [ ] Pity rule and effective rate computed and disclosed; item supply per day modelled for every top-tier item; a copy sink exists.
- [ ] Premium currency (if any): anchor fixed, prices and packs on one unit, paid and free buckets, one-way conversions, loop check run.
- [ ] Simulation compares changes on the same seeds and reads the game's config; hours held, gate conversion and item supply are tracked per progress band with alerts.
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
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/48 Economy Design Deep Dive/` (`Simulating an Economy Before Launch`, `Economy Telemetry and Balancing Live`, `Pricing Curves and Upgrade Costs`, `Currency Architecture - Soft Hard and Event Currencies`, `Player-Driven Trading Economies`, `Drop Tables Rarity and Pity Systems`), `11 Monetization Publishing and Live Ops/Economy Inflation Sinks and Faucets Math.md`, `38 Live Ops Deep Dive/Economy Resets and Seasonal Wipes.md` (read). Ideas adapted in our words; its simulated and rule-of-thumb numbers are labelled as such. Not imported: its Python simulator, wallet, telemetry and listing-board code.
- Wave-2 verification in the docs mirror: `production/analytics/event-types.md`, `custom-fields.md`, `production/experiments.md` (read)
- No evidence found: a DevForum or Reddit thread with measured rebirth tuning data from a current top simulator; reddit.com was not reachable and surfaced in no search.
