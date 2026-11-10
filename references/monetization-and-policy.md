# Monetization and policy

What to sell, at what price, when to offer it, and what Roblox policy forbids. Open it when you write a product plan for a new game, or when a live game has a monetisation symptom (jump to "Level-up"). Distilled from knowledge-base sections 3.6–3.8 and 1.6.5, re-verified against `Roblox/creator-docs` and extended with 2025–2026 benchmarks on 2026-11-10. The house rule is "push microtransactions heavily, but never invasively"; non-invasive wins every conflict. Tags: `[official]` Roblox docs, `[community]` forum/press/third-party (heuristic), `[VS]` version-sensitive (re-check https://create.roblox.com/docs), `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; rules of thumb from its reference project unless stated).

## Start here by level

| Level | Do these | Ignore for now |
|---|---|---|
| Beginner | Pick 5–8 rows from the house default set. Read every price with `GetProductInfoAsync`. Grant only in the receipt handler. No offer before the first win and 10 minutes. No paid random items until you can show odds. | Subscriptions, premium currency, ads, experiments |
| Intermediate | A four-rung ladder that passes the value tests. The offer gate and timing map. Managed Pricing and the platform Shop. Two or three rewarded-video placements. Full odds disclosure with the PolicyService gate. A purchase log. | LTV models, webhooks |
| Expert | Payer segments and a repeatable top rung. Elasticity tests with guardrails, cannibalisation and pull-forward checks. Refund webhooks and a clawback policy. Cohort LTV and ad payback. Season-pass arithmetic. | — |

Terms: **conversion** = paying users ÷ daily active users (DAU); **ARPPU** = revenue per paying user; **ARPDAU** = revenue per daily active user; a **rung** is one price band of the ladder; a **paid random item** is anything random reached with Robux, directly or through a currency Robux can buy.

Contents: Catalogue · Benchmarks, segments and unit economics · Default product set · Price ladder by genre and ladder tests · Offer and shop playbook (timing map, honest timers) · Price elasticity and experiments · Rewarded video · Gifts · Refunds and purchase support · Policy · Anti-patterns · Level-up table · Review gate · Sources.

Related: economy-and-progression.md (currency design, sinks, the paid-multiplier cap); gameplay-systems-cookbook.md §3 Shop and §24 Server-wide events and boosts (implementation); data-and-purchases.md (ReceiptService, passes, gifts); ui-design-figma.md (shop screen recipe); liveops-quests-retention.md (season pass missions, social rewards).

## Catalogue of monetization surfaces

| Surface | Rules and limits `[VS]` | Use for |
|---|---|---|
| Game pass | One-time, non-transferable. 5-day payout hold. Owned forever; check on the server. Regional pricing on by default. | Permanent perks: 2× Cash, Auto-Collect, VIP, extra slots |
| Developer product | Repeatable, 1–1,000,000,000 R$. Grant only inside the receipt callback. Roblox's own guide: "Dev Products generally monetize better, as they can be repeatedly purchased" `[official]`. | Boosts, currency packs, revives, skips, Gift versions of passes |
| Robux subscription | At least 49 R$ per month, single tier (no mutually exclusive Bronze/Silver/Gold), price change at most every 60 days and increases need 30 days' notice, 50 subscriptions per game, no refunds, forced regional pricing. Gate on `IsEligibleToPurchaseSubscription`. | VIP monthly |
| Local-currency subscription | $2.99 / $4.99 / $7.99 / $9.99 / $14.99; creator receives 70% in month one then 100%; 30-day hold; web, App Store and Google Play only; unavailable in 12 countries. | VIP monthly on supported platforms |
| Paid access | 25–1,000 R$, or $9.99 / $29.99 / $49.99 in local currency with a 50 / 60 / 70% share. Not available on Xbox; local currency is bought on desktop and web only. Cannot be combined with private servers. | Premium games only; not for discovery-driven titles |
| Private servers | Free or a monthly Robux fee. Changing the price cancels every active subscription. Plus subscribers get paid servers free; you still earn up to 100 R$ per subscriber per month for 60+ minutes of play. | Groups of friends; co-play signal |
| Roblox Plus | Subscribers pay 10% less (20% from month three) on passes, products, subscriptions and paid access; Roblox funds the discount, you still receive 70% of list. `PromptRobloxSubscriptionPurchase` pays 250 R$ a month for three months (750 R$) per new subscriber; 60-day hold. | One quiet "Plus members save 10–20% here" line in the shop footer |
| Robux transfers | Plus subscribers only, 10–500 R$ per transfer via `PromptRobuxTransferAsync`; the game receives 10% (DevEx-eligible), the recipient 90% (not DevEx-eligible). | Player-to-player tipping |
| Roblox Shop | Platform storefront generated for every game: all passes plus "Listed" developer products, personalised ranking, Top Picks, Robux packages. Global Shop button is off by default (Creator Hub ⟩ Monetization ⟩ Shop). `MarketplaceService:OpenShop(player)`. | A second, zero-effort storefront; Listed products can surface outside the game |
| Avatar items | 40% affiliate share on items sold in-experience | Shop surfaces |
| Rewarded video | Reward is a fixed developer product worth 3–10 R$; 2,000+ monthly visitors, publisher 13+, ID verification and 2FA, public game with no free-form user creation | Free alternative to paid boosts |
| Immersive ads | Image, video and portal ad units. An `AdGui` must sit on a block `Part` 8×4.5 to 32×18 studs `[official]`; same eligibility as rewarded video; paid on the 25th of the following month. House rule 1 tension: the Part is the flat screen only, set inside a Blender-modelled billboard frame. | Lobby walls, never in the play path |
| Creator Rewards | Daily Engagement: 5 R$ per Active Spender ($9.99+ platform spend in 60 days) per day, only if your game is one of the first three they play for 10+ minutes. Audience Expansion: 35% of a new or reactivated user's first $100 in 60 days (needs an average of 100+ DAU). 60-day hold. | Income you influence through daily return reasons and 10-minute sessions |

Other facts `[VS]`: the creator share on Robux sales is 70%. Cross-game sales of passes and developer products have been disabled since 30 May 2026. The DevEx rate is $0.0038 per Robux (from 5 September 2025; legacy $0.0035), and $0.0054 for US 18+ sales from 8 June 2026, which requires R15-only avatars. Per 100 R$ sold you keep 70 R$, worth about $0.266 (or $0.378 at the 18+ rate). Managed Pricing (regional pricing plus price optimization) scales prices to 30–100% of base; new games and new items are enrolled by default, and price tests need roughly 60,000 transactions in 30 days and rerun at least every 90 days.

Never hard-code prices in UI: regional cohorts, price-test cohorts and Plus subscribers are all charged a different amount from the list price. Read `PriceInRobux` through `MarketplaceService:GetProductInfoAsync(id, Enum.InfoType.Product or GamePass)` (`GetProductInfo` is deprecated) and cache it per session only. `RankProductsAsync` is throttled to 10 calls a minute; call it once at join. `RecommendTopProductsAsync` returns up to 50 products, and an empty list when the game has had no sale in the past 28 days.

Honest price label (unexecuted sketch; a strike-through appears only when Roblox reports a real discount such as Plus):

```lua
--!strict
local MarketplaceService = game:GetService("MarketplaceService")
local function priceLabel(id: number, infoType: Enum.InfoType): (string, string?)
	local ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, id, infoType)
	if not ok or info.PriceInRobux == nil then return "—", nil end
	local pay: number = info.PriceInRobux
	local base: number = info.UserBasePriceInRobux or pay
	return `{pay} R$`, if base > pay then `{base} R$` else nil -- second value = struck-through base
end
```

## What the numbers say (benchmarks, 2025–2026)

All third-party figures were seen only through search summaries; treat them as orders of magnitude and compare against your own Creator Hub ⟩ Monetization ⟩ Overview (conversion = paying users ÷ DAU; ARPDAU = conversion × ARPPU).

| Metric | Figure | Source and scope |
|---|---|---|
| Players who pay at all | 3.8% over a year (4.2% two years earlier) | GameAnalytics 2026 report, 500+ games with 1M+ MAU, Aug 2025–Jul 2026 `[community]` |
| ARPPU per game | Median $0.70; p25 $0.32, p75 $1.25, p90 $2.33, p95 $4.80 | Same report `[community]` |
| Spend per paying player | Median $0.81; top 10% $8.88, top 5% $20.31, top 1% $86.36 | Same report `[community]` |
| Daily payer conversion, platform-wide | About 1.25% of DAU; daily bookings per user $0.14 | Newzoo, Roblox as a platform in 2025 `[community]` |
| Session length vs spend | Games with median sessions under 6 min: D1 about 6%, ARPPU under $1. Top tier: ARPPU above $6, average transaction $3–4 | GameAnalytics 2025 report, secondary summary `[community]` |
| Price optimization | Median +4% earnings for eligible creators who ran a test; many tests recommended lower prices; one creator reported "over 15%" | Roblox announcements and press `[official]`/`[community]` |
| Regional pricing for passes | Paying users +17% Mexico, +26% Brazil, +52% Philippines in early tests (a later post: +13.8 / +22.4 / +44.8%) | Roblox announcements `[official]` |
| Starter pack | "Roughly 2–10% average revenue gains" (industry benchmark quoted by Roblox) | Roblox starter-pack design guide `[official]`, search summary only |
| Subscriptions | Creators who add them "increase their revenue by 7%" | Roblox announcement, 2024 `[official]` |
| Rewarded video | Expected to be about 3% of creator earnings at first; targets: opt-in 10–20%+, 2–4+ views per viewer per day, 0.5+ impressions per DAU (incremental sims: 13%+ opt-in, 2.8 views) | Roblox DevForum Aug 2025 and playbooks `[official]` |

What follows from them `[house]`: the median payer spends less than one dollar, so the first rung must sit under 100 R$ and there must be something cheap to buy again tomorrow (repeat spend days are also a Recommended For You signal; see market-scan-2026-11.md). The top 1% spend about 100 times the median, so the ladder needs a real top end. Spend follows session length: fix retention before pricing. No published revenue-per-visit benchmark was found; do not quote one.

Payer segments, from minnow to whale (spend figures are the GameAnalytics 2026 percentiles above `[community]`; the design column is `[house]` with `[lihfolk]` where marked):

| Segment | Size and spend | Buys | Design for them |
|---|---|---|---|
| Non-payer | About 96% of players | Nothing | Rewarded video, free alternatives, friend bonuses. They are the population payers play with; never make them worse off to sell a fix |
| Minnow | The median payer: under $1 in a year | One impulse item | Entry rung under 100 R$, starter pack, prices that fit a leftover balance (75, 79, 99) |
| Dolphin | Top 10% of payers: about $9 | Permanent passes, a bundle or two | Core rung, the complementary pass, a season pass, gifts |
| Whale | Top 5% about $20; top 1% about $86 and up | Repeatable value | A top rung that can be bought again (currency, consumables, ×10 packs), never a one-time 4,999 R$ pass that converts a handful once `[lihfolk]`; prestige cosmetics; purchase support that answers. No pressure, no exclusive power |

Players spend from a Robux balance filled earlier by a fixed bundle or a gift card, often a child's finite gift `[lihfolk]`. A price just under a common bundle size fits one top-up; just over forces a second. After a 399 R$ purchase the leftover is what your impulse rung competes for. Check current bundle sizes on the Robux purchase page `[VS]`.

Unit economics `[lihfolk]`. The dashboard shows daily averages; decisions need cohorts. `LTV_d = Robux spent by a join cohort up to day d ÷ cohort size` (store first-seen day and acquisition source; log every receipt's real amount; use cohorts of hundreds). Add expected Creator Rewards. Ad payback at day d = value per new player ÷ (cost per play ÷ share of plays that are new players); above 1.0 the campaign has paid back. Using cost per play as cost per new player is the usual error. Net Robux per sale ≈ 0.70 × list price × regional factor (0.3–1.0): 1,000 sales of a 499 R$ product with 30% of buyers at a 0.6 factor earn about 307,000 R$, not 349,300. Compute revenue from receipt amounts (`CurrencySpent`), never from config prices. See analytics-and-discovery.md and growth-and-marketing.md.

## The house default product set

| Product | Type | Price (R$) | Notes |
|---|---|---|---|
| 2× Cash, 10 min | Dev product | 29–49 | Counts play time, pauses offline; buying again extends |
| 2× Cash, 30 min | Dev product | 79–99 | |
| 2× EXP, 10 / 30 min | Dev product | 29–49 / 79–99 | Only if the game has XP |
| 2× Speed (delivery, gather, click), 10 min | Dev product | 25–39 | |
| Luck 2×, 15 min | Dev product | 49–79 | Only with luck mechanics; paid random item rules apply |
| Server Luck | Dev product | 149–249 | Server-wide, runs in real time; announced to all, with activator and end time |
| Starter Pack | Dev product | 49–99 | One per account (saved flag); popup after first win only; contents listed with their shop value |
| Auto-Collect | Game pass | 199–299 | Convenience |
| Extra storage / slots | Game pass | 129–199 | |
| Permanent 2× Cash | Game pass | 399 | |
| VIP | Game pass or subscription | 799 one-time, or 499 R$ per month / $4.99 | Cosmetic plus convenience, never power in PvP |
| Gift versions of passes | Dev product | Same price as the pass | Grants an entitlement in the recipient's data |
| Currency packs | Dev product | 49 / 99 / 399 / 999 / 2,499 | Bulk bonus up to +15% |
| Revive / second chance | Dev product | 15–30 | Roguelike, horror; never during a chase |
| Private server | Server | 0–100 | |

Market prices are a 2026-11-07 snapshot `[VS]`. Luck and Server Luck exist only in games with random rewards; in those games they are paid random items and need odds disclosure plus the PolicyService gate.

Boost rules: stacking the same boost extends duration (cap it, for example at 6 hours) and never multiplies; different boost types multiply with each other; personal paid boosts count play time and pause offline, server-wide boosts run in real time and show their end time, and the product card says which; show a HUD timer pill with the honest remaining time.

Recommendation. Lower-risk: ship the default set above plus two or three rewarded-video placements, all surfaced through the shop and contextual, dismissible offers. Bold: add a VIP subscription, a premium season pass and Server Luck events, but only after D1 and D7 retention meet your genre's benchmark; monetizing a leaky funnel burns the audience Recommended For You sends you.

## Price ladder and product mix by genre

Every ladder needs four rungs: entry (under 100 R$), core (100–399), premium (400–999) and top (1,000+). Rungs are `[house]`, anchored on the observed prices below. Start from the row, then let Managed Pricing test it.

| Genre | Mix | Entry < 100 | Core 100–399 | Premium 400–999 | Top 1,000+ | Never sell |
|---|---|---|---|---|---|---|
| Simulator, +1, incremental | 30+ cheap repeatable products, 4–6 passes | Stat or cash pack 10–49; 2× 10 min 29–49; idle pad 69; ×8 pad 79; starter pack 49–99 | Auto pass 175–299; slots 129–375; 2× lucky 275; ×15 pad 199 | Permanent 2× 399–450; VIP 400–799; ×30 pad 499 | ×99 pad 1,299; hunter-style pass 2,400–3,250; pack 2,499 | Unbounded paid multipliers (cap the stack; see economy-and-progression.md) |
| Tycoon, cozy management | Product-heavy; passes are convenience | Cash pack 49; restock or timer skip 39–79; 2× cash 10 min | Auto-collect 199–299; extra worker or plot slot; 2× speed pass | Permanent 2× cash 399; VIP 499–799 with offline bonus | Cash pack 2,499; founder bundle | Timers that exist only to be paid away |
| Collection, RNG, gardening | Pack ×1 / ×3 / ×10 ladders, luck boosts, limited packs | Luck 15 min 49–79; restock 39–79; single egg 79 | Pack ×1 at 199; Server Luck 149–249 | Pack ×3 at about 575 | Pack ×10 at about 1,699; limited pack 1,999 | Any random item without odds and the PolicyService gate |
| RPG, anime grinder | Passes first (2× XP, 2× money), then consumables | 2× XP 10 min 29–49; stat or class re-roll 99 | Fast travel 350; storage 129–199 | 2× Money 450; 2× Mastery 450 | Notifier-style utility 2,700 | Best gear or stats usable in PvP |
| Round-based horror, survival | Consumables before the run, revive after it | Revive 15–30; soft-currency pack 49 | Starter kit 99–199 | VIP 400 (extra revives, cosmetics) | Cosmetic bundle 999+ | A revive prompt mid-chase |
| Obby, tower | Tiny impulse products | Skip stage 15–29 (5–20 seen); checkpoint save | Gravity coil, speed coil 99–199 | All-coils VIP 400 | — | Purchase pads on the path |
| Roleplay, social | Passes and cosmetics; subscription suits regulars | Emote or prop pack 49–99 | Premium pass 275; vehicle pack 349–399 | House or estate pass 499–799 | Season or founder bundle | Access to social spaces that raises the maturity rating unplanned |
| Competitive PvP, shooter | Cosmetics, bundles, season pass only | Skin 49–99; key or crate with odds 79 | Bundle 199–399; season premium track | Prestige skin 499–999 | Collector bundle 1,000+ | Stat power of any kind (house rule) |

Observed live prices `[community]` `[VS]` (wikis, guides and the owner's 2026-11-07 scan; fan sources disagree on some, check the game's store page):

| Game | Prices (R$) |
|---|---|
| Pet Simulator 99 | Auto Farm 175, Lucky 275, Auto Tap 350, +15 Pets 375, VIP 400, Ultra Lucky 800, Super Drops 2,400, Huge Hunter 3,250 |
| Blox Fruits | 2× Money 450, 2× Mastery 450, Fast Boats 350, Fruit Notifier 2,700 |
| Brookhaven | Premium 275; vehicle pack 349–399 (sources differ) |
| Doors | VIP 400 |
| Grow a Garden / Grow a Garden 2 | Shop restock 79 / 39; seed packs 199 ×1, 575 ×3, 1,699 ×10 (bulk −4% and −15%); limited pack 1,999 |
| +1 / Evolution format | Pads ×8 / ×15 / ×30 / ×99 at 79 / 199 / 499 / 1,299; 2× Wins 90–99; size packs 10 / 41 / 86 / 167; idle pad 69; Robux egg 79 |
| Obbies (DevForum anecdotes) | Skip stage 5–20; one reply argues 19–49 |

Conflict: the default Starter Pack is 49–99 R$. A DevForum poll thread (older, anecdotal) argues for about 198 R$ with contents under 30% off their combined value, and top-tier games average $3–4 per transaction. Keep 49–99 as the first-purchase rung and add a second, larger value pack at 199–399 for the second purchase; test rather than replace.

### Ladder arithmetic and tests

For a category sold in sizes (packs, boost bundles), compute value per Robux for each rung, `v = amount ÷ price`, and run three tests `[lihfolk]`:

1. **Monotone value.** v rises with size. A rung with worse value than the one below it is a trap; players notice, and it shows as near-zero sales of that rung.
2. **Diminishing extra bonus.** Each step up adds less bonus than the last, or the top rung makes the middle look foolish and you lose mid-tier buyers who would never spend 1,999.
3. **Computed labels.** "+15%" and "Best value" come from the same table the grant uses, asserted at server start. A typed label drifts the first time an amount changes.

- Show bulk bonuses in units ("+500 Cash free") rather than a percentage: regional prices are set per product, so ratios between rungs can differ by region.
- Leave room between rungs (399 beside 449: the cheaper wins unless the extra is obvious). Prices ending in 9 are the platform convention, not a source of value.
- Price a permanent multiplier by lifetime value: the same Robux on a pass must buy something structurally better than a one-hour boost.
- Cannibalisation: a new 299 R$ bundle "earning" 10,000 R$ a week may have taken 9,000 from the 399 R$ pass. Judge total revenue per user, not the product's own line.

Conflict (bulk bonus size): LihFolk's worked gem ladder steps +32% / +43% / +49% `[lihfolk]`; the house ladder caps at +15%, matching the observed ×3 / ×10 seed packs (−4% / −15%). Keep 15–20% for soft-currency and item packs, because a pack is a faucet and a deep bonus accelerates inflation; a premium-currency ladder with real sinks can go deeper. Test it as a content experiment. Its rung bands (under 100, 150–600, 700–1,500, 2,000+) have the same shape as ours; ours stay because they are anchored on observed pass prices.

## Offer and shop playbook (house rule: never invasive)

Shop design `[official]`: integrated into the world (a Blender-modelled shop counter with a prompt), contextual (offer the thing the player is looking at), and inviting. Use neutral calls to action such as "View Item", "See Price" or "Open Shop", not "BUY NOW".

Shop layout that sells without annoying:

- Tabs in this order: Featured (at most 3 cards: starter or value pack, the pass that fits the player's stage, the live event bundle), Boosts, Passes, Currency, Gifts. Mark owned passes "Owned" instead of hiding them, so the player sees what they already have and what is left.
- Every card states the effect in the game's own unit ("+4,200 Cash in 10 min at your current rate"), not only "2×". Starter-pack buyers hesitate when contents are hidden `[community]`: list them with the price each has elsewhere in the shop.
- Anchor honestly: a "Best value" tag is allowed on exactly one pack per ladder and only when its unit price is the lowest; show the arithmetic ("+15% Cash per R$"). A struck-through price is allowed only for a real, ended-on-time discount or a Roblox-reported discount (sketch above).
- Limited-time offers are real: one `endsAt` timestamp in Configs, shown as a date or honest countdown, never extended and never restarted for the same item. Bring an item back as a named rerun at least 30 days later `[house]`.
- Complementary offers `[official]`: after a pass purchase, show the related pass once inside the shop, or sell both as a bundle; do not chain prompts.
- Turn on the platform Shop button, mark products Listed with icons and categories, and keep the receipt handler correct for purchases that start outside your UI.
- Enable Managed Pricing for every pass and product, and run the dynamic price check tool first.
- First-time buyers open on a short "starter shop" (starter pack, one cheap pass, one pack), not the full catalogue: long lists paralyse a first purchase `[lihfolk]`. Card states: BUY, OWNED, ACTIVE mm:ss, UNAVAILABLE.
- Timers that cannot lie `[lihfolk]`: most dishonest countdowns are bugs (computed from the client clock, server start or "since this GUI opened", so they reset on rejoin). Every end time is a server fact: global windows come from the event calendar in Configs; a personal window is written to the profile once, when the offer is first actually shown; the client renders from `endsAt` and `workspace:GetServerTimeNow()` and never starts a countdown itself.
- "Was / now" labels need a reference price that was live for at least 30 days; an item discounted most weeks has the discount as its real price; no discount window under 24 hours `[lihfolk]`. A quantity limit needs an atomic global counter with reservations; if you will not build that, do not claim one.
- Judge a sale on the sale days plus the two following weeks: revenue pulled forward is not revenue gained `[lihfolk]`.

Offer gate rules (implement as Configs so you can tune them live):

- Grace period: no offers until the player has at least 10 minutes of lifetime play **and** has had a first win.
- Positive triggers only: after a delivery, a level-up, a round win, a rebirth. Never on death, failure, loading or join.
- Size: at most 25% of the screen, in a safe-area corner outside thumb zones, with an X, never stacked.
- Frequency: at least 8 minutes between offers, at most 3 per session, at most 1 starter-pack prompt per day, and suppress an offer for 24 hours after two dismissals.
- No sound stings, no shaking buttons, no countdowns that restart, honest copy.
- Passive surfaces (shop button, shop shelves, HUD boost pill, a starter-pack tile inside the shop) are unlimited and may exist from the first minute.
- Always show a free alternative next to a paid one (rewarded video, wait, or earn in play).

Conflict: Roblox's starter-pack guide (search summary) recommends making the pack available as soon as new players spawn, because gating it shrinks the audience, and the glossary defines it as shown "within the first few minutes". House rule 3 overrides the popup timing. Resolution: the pack is visible passively in the shop from minute one; the popup still waits for the gate.

Conflict (popup cadence): LihFolk's reference project allows a new pop-up 8 seconds after the last, caps first-session non-payers at one unprompted offer, and treats near-miss rolls and boss losses as valid moments for small dismissible offers (while calling the near-miss "the most ethically loaded") `[lihfolk]`. The house rule is stricter and wins: 8 minutes, three a session, nothing before the first win, popups on wins only. Loss and near-miss offers exist only as inline buttons. Adopted from it: one server-side engine decides every unprompted offer (the client never does), and it also blocks during roll animations, cutscenes and while any panel is open.

### Offer timing map

One row per loop moment. "Inline" means a button on a screen the player already opened; only "popup" rows spend the offer-gate budget.

| Loop moment (server-known signal) | Offer | Surface | Free alternative |
|---|---|---|---|
| First session before the first win | Nothing pushed | Shop tile only | — |
| First win or first rebirth, 10+ min played | Starter Pack, once per account | Popup (gate) | Earn the contents in about 30 min |
| Second failed attempt to afford the same upgrade | 2× Cash 10 min or the smallest pack that covers the gap | Inline on the upgrade card | Rewarded video; "about N min of play" |
| Storage full for the second time | Slots pass | Inline on the full-storage notice | Sell items |
| 20th manual collect, or 10 min of one repeated action | Auto-Collect pass | Popup (gate) after the action completes | Keep collecting |
| Round or run ends in a win; intermission | Boost for the next round; cosmetic the winner used | Inline on the results screen | — |
| Run ends in a loss | Revive or second chance | Inline on the results screen, never a popup | Rewarded video revive |
| Pre-run lobby or loadout | Consumables for this run | World shop counter | Soft currency |
| Return after 4+ hours away | Double the offline earnings just shown | Inline on the welcome-back panel | Rewarded video doubler (1 a day) |
| Timed boost has under 60 s left | Extend the same boost | HUD pill pulses once | Rewarded video 5 min |
| Rebirth completed | 2× Cash or XP, 30 min (the post-reset grind is its best-value moment) | Popup (gate) | Free 5-min boost granted with the rebirth |
| Third hatch or roll within 2 min | Luck, auto-hatch, ×3 pack | Inline on the hatch UI, odds visible, PolicyService-gated | Free daily luck window |
| Pass just bought | The complementary pass, or the bundle | Inline in the shop, once | — |
| Event start or weekly update day | Limited bundle with a real end time | Featured tab and one toast | Event currency earned in play |
| Day 7+ player with two or more purchases | VIP subscription | Featured card | VIP one-time pass |

Friction and loss rows are inline only. "Positive triggers only" governs popups; a quiet button on a screen the player already sees is a passive surface, and Roblox's rewarded-video playbook names out-of-currency and end-of-run moments as the best opt-in placements `[official]`.

Gate sketch (server-side, unexecuted sketch; read the numbers from `ConfigService`):

```lua
--!strict
-- Defaults: offer_grace_seconds = 600, offer_min_gap_seconds = 480, offer_max_per_session = 3,
-- offer_dismiss_limit = 2, offer_dismiss_cooldown = 86400
function OfferGate.canShow(state, offerId: string): boolean
	local now = os.time()
	if not state.hadFirstWin or state.lifetimeSeconds < num("offer_grace_seconds") then return false end
	if state.inCombat then return false end
	if state.sessionShown >= num("offer_max_per_session") then return false end
	if now - state.lastShownAt < num("offer_min_gap_seconds") then return false end
	local d = state.dismissals[offerId]
	if d and d.count >= num("offer_dismiss_limit") and now - d.at < num("offer_dismiss_cooldown") then return false end
	return true
end
```

The Bundles feature package sample prompts a StarterBundle on `PlayerAdded`. Do not copy that; call `Bundles.promptIfValidAsync(player, "StarterBundle")` from the offer gate after the first win.

Boosts module sketch (unexecuted sketch; personal boosts are `{ [boostId]: remainingPlaySeconds }` in the profile, ticked by the server only while the player is online; a server-wide boost is a server-side `endsAt` in real time):

```lua
--!strict
local MAX_STACK_SECONDS = 6 * 60 * 60
function Boosts.add(state: { [string]: number }, boostId: string, seconds: number)
	state[boostId] = math.min((state[boostId] or 0) + seconds, MAX_STACK_SECONDS)
end
function Boosts.tick(state: { [string]: number }, dt: number) -- once a second per online player
	for boostId, left in state do
		state[boostId] = if left > dt then left - dt else nil
	end
end
function Boosts.remaining(state: { [string]: number }, boostId: string): number
	return state[boostId] or 0
end
function Boosts.multiplier(state: { [string]: number }, boostId: string): number
	return if Boosts.remaining(state, boostId) > 0 then 2 else 1
end
```

## Price elasticity and experiments

Elasticity = % change in units sold ÷ % change in price. Below −1 a price cut raises revenue; between −1 and 0 a rise does. Roblox reports that many price tests recommend lower prices `[official]`, so expect many products to sit on the elastic side.

| Situation | Method |
|---|---|
| 60,000+ transactions in 30 days | Managed Pricing price tests: about three weeks, cohort-split by Roblox, applied only if total revenue rises, then a four-week review with a 2% holdout. Do not hand-tune a product during its test `[official]`. |
| Smaller games | Sequential test `[house]`: change one product's price, hold at least 14 days on each side covering the same weekdays, with no event, update or featuring inside the window. Measure buyers per 1,000 players who saw the card, not sales per day. It is weak evidence: reverse it once to confirm. |
| Any size | Experiments on Configs (14–60 days, a control and up to two variants, a Custom metric set with up to three metrics from economy or funnel events `[official]`) for timing, surface, pack contents and boost duration. Never different Robux prices for the same thing through duplicate products: a fairness and trust risk `[lihfolk]`, and off the table under the house rule. |

Worked example (illustrative `[house]`): 2× Cash moves from 49 to 39 R$ (−20%). Buyers per 1,000 exposed go from 20 to 28 (+40%): elasticity −2, revenue per 1,000 exposed 980 → 1,092 R$ (+11%), keep it. Had buyers gone to 23 (+15%), elasticity is −0.75 and revenue falls to 897 R$ (−8%): revert.

Guards `[lihfolk]`: per-player metrics, never per-day (a few large purchases move a day more than any design change); at least a full week and a few hundred buyers per arm, otherwise treat the result as a hint; guardrails of D1, first-session bounce and like ratio, because an offer that lifts revenue and drops D1 costs distribution; total revenue per user to catch cannibalisation.

## Rewarded video

- Opt-in, 6–30 seconds, rewards a fixed developer product worth 3–10 R$ that is normally sold in the shop; never a gate, never random, never Robux; pause gameplay damage while it plays. The reward must not inflate currency or unbalance the economy `[official]`.
- Eligibility: 2,000+ monthly visitors, publisher 13+, ID verification and 2FA, public game with no free-form user creation, questionnaire approved `[VS]`.
- API: `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)` (call it when the menu opens, not at join), `AdService:CreateAdRewardFromDevProductId`, `AdService:ShowRewardedVideoAdAsync`, `AdService:RegisterAdOpportunityAsync`.
- Placement `[official]`: visible within one or two taps of the triggering moment (end-of-level bonus, low-resource HUD button, welcome-back doubler), reward shown before the player commits, more than one reward type, a cap of at least 2–3 a session. A "Watch Ad" button three menus deep is the documented failure.
- Turn on "Exclude your most likely purchasers" only when the same reward is also sold; leave it off for ad-only rewards `[official]`.
- Good placements by genre are in genre-playbooks.md.

## Gift passes

Game passes cannot be transferred, so a gift is a developer product that writes an entitlement into the recipient's profile. Flow: the buyer picks a recipient; the server checks `canGift` (not self, recipient does not own it, not already gifted, buyer's price level is at least the recipient's via `GetUsersPriceLevelsAsync`, fail closed on errors); store `PendingGiftTarget` in the buyer's profile; prompt the product; in the receipt handler set `Entitlements[passId] = true` on the recipient's profile if it is loaded, or deliver through `ProfileStore MessageAsync`, keyed by the `PurchaseId` so repeats are harmless. Every perk check is `ownsPass or data.Entitlements[pass]`. Code is in data-and-purchases.md. No published evidence was found that gifting raises revenue; treat it as a co-play feature and measure it.

## Refunds, clawbacks and purchase support

| Purchase | Ownership lives in | On a refund through Roblox `[official]` `[VS]` |
|---|---|---|
| Pass, avatar item | Roblox | Revoked automatically (a server that cached ownership keeps the perk until rejoin) |
| Developer product; extras granted alongside a pass | Your save data | Nothing changes in game; removing the benefit is your job |
| Subscription | Roblox | Separate "Subscription Refunded" notification |

- Roblox can post a "Transaction Refunded" webhook (products, passes, private servers, paid access) to an HTTPS endpoint set in Creator Hub. Verify `roblox-signature` (HMAC-SHA256 over `timestamp.body`, Base64, 300-second window). After five failed deliveries Roblox stops sending, so monitor the endpoint `[official]`. The game cannot receive webhooks: the receiver appends a record through Open Cloud to a per-user key that the server reads at join (data-and-purchases.md).
- Keep a purchase log: Roblox stores no per-user product history for you. Record `PurchaseId`, product key, Robux actually spent, the exact grant and the time; the webhook amount is the list price, not what the buyer paid `[lihfolk]`.
- Clawback policy, decided before coding `[lihfolk]`: unspent granted currency is removed (floor at zero); an item still owned and untraded is removed; a consumed boost or revive, and an item already traded on, are written off (the receiver traded in good faith); a one-time-pack flag is cleared.
- Conflict: LihFolk suggests a negative balance repaid from future income when refunded currency was already spent. House position: write it off. Most refunds are a parent reversing a child's purchase, and a debt punishes the child; flag repeat refunders for review instead.
- Support `[lihfolk]`: answer "paid and got nothing" from the log using date, time and product name, never account details. Product keys are permanent; retire a product by taking it off sale and keeping its grant code for pending receipts; announce content changes and let earlier buyers keep what they bought. Enforce one-per-account limits when prompting, not in the receipt handler, and honour a receipt that arrives after an offer expired: refusing a paid receipt charges the player for nothing.

## Policy: what is banned and what must be disclosed `[VS]`

- Discounts must be genuine and fair `[official]`: not genuine if the item is always "on sale" for the same amount; not fair if offered only for a very short time to pressure a purchase. No false scarcity, no countdowns that are inaccurate or restart for the same item.
- Players "must never be misled, confused, or pressured into purchases in ways they did not intend" `[official]`. Avoid pushy or urgent messages when interacting with minors.
- **Paid random items** include anything bought with Robux or with currency bought with Robux whose outcome is random: crates, eggs, wheels, enhancement items with a chance of failing, combination or fusion items, probability modifiers (Luck, pity, rate-up) and indirect purchases (keys, re-roll tokens, spin tickets).
  - Show every possible outcome with numeric odds before the purchase. An "Info" or "Details" button opening a popup is acceptable; a bare (i) icon is not.
  - Odds are percentages summing to exactly 100% (rounded long decimals need a disclaimer), update when a one-per-user outcome is taken, and reflect live boosts.
  - When `PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted` is true, offer a free earnable path, a fixed disclosed order, direct sale at expected value, or hide or block the feature; never sell the random item.
  - `IsPaidItemTradingAllowed` gates trading of paid items. Rewarded-video rewards cannot be random.
  - Random rewards earned without Robux or Robux-bought currency need no odds disclosure, but showing them anyway is the house default.
  - Audit the money paths first `[lihfolk]`: direct (Robux egg), indirect (a currency Robux can buy), modifier (paid luck, pity, drop-rate boosts), a bundle containing any random item, a premium season-pass tier that grants a crate. All are covered.
  - Flatten tier odds into per-outcome odds with the same function the server rolls from; never show a non-zero chance as 0%; for pity disclose the rule and the effective rate (economy-and-progression.md). A modifier card states multiplier, duration, scope and a before/after for the tier players care about `[lihfolk]`.
- Other PolicyService gates: `AreAdsAllowed` (immersive and independent ads; never infer eligibility from age yourself), `IsEligibleToPurchaseSubscription`, `IsEligibleToPurchaseCommerceProduct`.
- Subscriptions `[official]`: same benefits on every platform, benefits honoured for the full term, no extra tasks required after payment (a subscription battle pass is the stated exception), no directing players to buy on another platform. Deleting an active subscription refunds everyone and pays you nothing; take it off sale instead.
- Season pass arithmetic `[lihfolk]`: tune to a target player (say 5 days a week, 25 minutes). XP for the last tier ≈ 80–85% of days × share of days played × XP per play day (30 × 0.71 × 600 ≈ 12,600, so about 10,300). Give premium extra tiers on the same bar rather than only faster XP; premium tiers hold fixed items only; sell premium as one developer product recorded per season id; never re-release a reward sold as exclusive. Fewer than half of target players finishing the free track means the season was too long. Mission design is in liveops-quests-retention.md.
- Advertising `[official]`: disclose ads as ads, no third-party ad servers or SDKs, no bots or misclassified metadata.
- Content maturity labels: Minimal and Mild are available to Kids and Select audiences; Moderate to Select and 16+; Content May Vary to 16+; Restricted (18+) is unplayable in Korea, Saudi Arabia and Türkiye. Free-form social hangouts are 16+; private spaces (bedrooms, bathrooms) 18+. Playable gambling is banned. Resubmitting the questionnaire pauses ad eligibility.
- Thumbnails and video: no spoken audio, no real footage, no ad text in video thumbnails.
- Notifications: no dark patterns, never gate gameplay on opting in.
- Filter all user text with `TextService:FilterStringAsync`.
- Rewards for group joins, likes, favourites and friend joins are in the house default set as bonuses only (one-time boost, cash bump, badge or skin), never as a gate on progress, products or content, and never mentioned in the title, thumbnail or description (leading with giveaways or Robux is the exposure penalty). See liveops-quests-retention.md §social rewards for the verification rules.

Policy module sketch (unexecuted sketch; cache per player, 3 retries, fail closed):

```lua
--!strict
local function canBuyRandomItems(info): boolean return info.ArePaidRandomItemsRestricted == false end
local function canTradePaidItems(info): boolean return info.IsPaidItemTradingAllowed == true end
local function canSeeAds(info): boolean return info.AreAdsAllowed == true end
local function canSubscribe(info): boolean return info.IsEligibleToPurchaseSubscription == true end
```

## Anti-patterns and the reason each is banned

| Anti-pattern | Reason | Do instead |
|---|---|---|
| Item permanently "on sale"; fake struck-through price | Not a genuine discount `[official]` | Real end date, or no discount |
| Countdown that restarts; "deal of the day" shown every login | False urgency `[official]` | One `endsAt`; rerun later under a new name |
| "Only 3 left" on unlimited stock | False scarcity `[official]` | Real server-counted stock or nothing |
| Minutes-long flash sale popups | "Not fair" discount; pressure on minors `[official]` | Sales that last days, shown in the Featured tab |
| "GET IT NOW", "LAST CHANCE" | Language Roblox tells creators to avoid `[official]` | "View Item", "See Price", "Open Shop" |
| Egg, crate or wheel without numeric odds, or behind a bare (i) | Paid random items policy `[official]` | Odds table behind a labelled "Details" button |
| Luck or pity sold without live boosted odds | Probability modifiers are paid random items `[official]` | Show boosted odds while active |
| Random items sold to restricted players | PolicyService gate is mandatory `[official]` | Direct sale at expected value, free path or hide |
| Random or Robux rewarded-video reward; ad during danger | Rewarded-video rules `[official]` | Fixed product; safe zone or paused damage |
| Ad reward that prints currency | Reward must not inflate the economy `[official]` | Time-boxed boost, daily cap |
| Third-party ad SDK or tracking calls | Advertising standards; suspension risk `[official]` | Roblox ad units only |
| Purchase pads on the path; buy button under the jump thumb | Unintended purchases `[official]`; the most-cited player complaint on the DevForum; A is both jump and confirm on a controller `[community]` | Prompts only from a deliberate tap on a shop surface |
| Prompt on join or on the first loading screen | House rule 3; docs say no starter pack on the first load `[official]` | Offer gate after the first win |
| Hard-coded price text | Wrong price for regional, test and Plus cohorts; blocks Managed Pricing `[official]` | `GetProductInfoAsync` at runtime |
| Pass label that over-promises ("VIP" that is mostly decoration) | Buyer's remorse drives dislikes and refund requests `[community]` | State exact effects on the card |
| Stat power sold in competitive modes | House rule 3; players downvote monetisation they disapprove of `[official]` | Cosmetics, convenience, season pass |
| Timers whose only purpose is to be paid away | Roblox: unpopular with its audience `[official]` | Timers as return reasons, with a free path |
| Tasks required after paying for a subscription; mutually exclusive tiers; off-platform purchase links | Subscription guidelines `[official]` | Distinct benefit sets, delivered in full |
| Paid-item trading or gifting without `IsPaidItemTradingAllowed` and price levels | Policy; regional-price arbitrage `[official]` | Gate both, fail closed |
| Granting from a client signal or `PromptProductPurchaseFinished` | Spoofable; double grants | Receipt handler only, idempotent |
| Title or thumbnail that leads with free Robux or giveaways | Exposure penalty (market-scan-2026-11.md) | Lead with the game |
| Changing a private-server price casually; deleting a live subscription | Cancels every active server subscription; full refunds and zero payout `[official]` | Set once; take off sale instead |
| Duplicate products at different prices to test price on players | Fairness and trust risk; Managed Pricing exists for this `[lihfolk]` | Managed Pricing, or a sequential test |
| Selling a currency that expires; wiping paid value in a reset | Destroys what was paid for; refund requests follow `[lihfolk]` | Sell the track, not the tokens; paid value survives every reset |
| Bonus or "% off" label typed by hand | Drifts from the grant and becomes a false claim `[lihfolk]` | Compute from the grant table; assert at server start |
| Re-releasing an item sold as "exclusive" or "never again" | The scarcity claim was untrue `[official]` | Call it "Season 3 reward" and leave the future open |
| Refusing a paid receipt because a limit or timer lapsed | The player is charged for nothing and the receipt sticks `[lihfolk]` | Check limits when prompting; always honour the receipt |
| Comeback discounts as a habit | Teaches players to leave and wait `[lihfolk]` | A welcome-back gift, not a price cut |

## Level-up: monetisation symptoms → likely cause → fix

Read Creator Hub ⟩ Monetization ⟩ Overview for 28 days first. Compare against your own history before any benchmark; a DevForum report notes the built-in ARPDAU benchmark showing a 50th percentile of zero `[community]`.

| Symptom | Likely cause | Fix |
|---|---|---|
| Low payer conversion (under about 1% of DAU; the platform-wide daily figure is about 1.25% `[community]`) | No rung under 100 R$; shop hard to find; offers fire before the player understands value; list prices too high for the regions that play | Add 25–79 R$ products and a starter pack after the first win; enable the Shop button and Listed products; enable Managed Pricing |
| Good conversion, low ARPPU | Only one-time passes; nothing to buy twice; ladder stops at 399 | Add consumables, ×3 / ×10 bundles, 999 and 2,499 rungs, a season pass, seasonal items |
| High ARPPU, low ARPDAU | Revenue rests on a few big spenders `[official]` | Widen the entry rungs; welcome offer for first-time buyers; rewarded video for non-payers |
| Payers buy once and never again | No reason to spend on day 2+ | Timed boosts, restocks, rotating Featured tab, weekly limited bundle; show the complementary pass |
| Starter pack is seen but rarely bought | Contents hidden or not valued; shown before the loop makes sense | List contents and their shop value; move the popup to the first rebirth; A/B the price |
| Timed boosts sell poorly, passes sell well | Boost outlasts the session (median Roblox session 6.6 min) or its value is abstract | Count boost time only while playing; add a 5-min rung; show the gain in the game's unit |
| D1 or rating drops after a monetisation update | Offers too early, too often or too large | Check offer-gate logs; restore grace and caps; cut popups to inline surfaces |
| Dislike, complaint or refund-request spike | Label does not match delivery; accidental prompts; grants failing | Rewrite card copy; remove path pads and thumb-zone buttons; audit receipt errors and idempotency |
| Currency-pack sales decay week over week | Inflation: a pack buys fewer minutes of progress than it used to | Scale packs to the player's stage; add sinks (economy-and-progression.md) |
| Paid eggs sell in some regions and nothing in others | Restricted players see a hidden or dead feature | Direct sale at expected value or a fixed-order track for them |
| Rewarded-video opt-in under 10% | Button buried, reward unclear, one reward type | Move to HUD or results screen; show the reward; add a second reward |
| Price test recommends lower prices | List price above what your audience pays | Accept it; many tests recommend reductions `[official]` |
| Subscription churn after month one | Value was front-loaded | Monthly drop with clear contents; keep the one-time VIP as the alternative |
| Revenue falls after an event | Event paid out main currency | Event currency with expiring sinks |
| One rung of a ladder sells almost nothing | Worse value per Robux than the rung below, or priced too close to it | Monotone-value test; widen the gap `[lihfolk]` |
| New bundle sells, revenue per user is flat | Cannibalisation of an existing product | Judge total revenue per user; differentiate the bundle `[lihfolk]` |
| Sale-day spike, then a two-week dip | Purchases pulled forward | Measure sale plus two weeks against baseline; fewer, event-tied sales `[lihfolk]` |
| Dashboard revenue below list price × units | Regional pricing (your share is of the lower price), not a bug | Compute from receipt amounts `[lihfolk]` |
| "Paid and got nothing" tickets | Receipt not processed (profile not loaded, save failed) or a second `ProcessReceipt` overwrote the first | Purchase-log lookup; fix in data-and-purchases.md |
| Refund notifications went silent | Endpoint failed five deliveries and was marked invalid | Re-save the webhook; add monitoring |

## Review gate

The compliance ship gate. Every box is ticked before products go live and again after any monetisation update.

- [ ] Every paid random item shows full numeric odds (summing to 100%) before purchase, including boosted odds.
- [ ] `PolicyService` gates random items, paid-item trading, ads and subscriptions; failures fail closed.
- [ ] No fake discounts, restarting countdowns or false scarcity anywhere; every limited offer has one real end time.
- [ ] No offers in the first 10 minutes, on loading, or before the first win; rate limits in place; no purchase pads or thumb-zone buy buttons.
- [ ] Prices are read from `GetProductInfoAsync`; nothing is hard-coded; the dynamic price check passes; Managed Pricing is on.
- [ ] Grants happen only in the receipt handler or pass ownership checks, never from UI signals.
- [ ] Rewarded-video rewards are fixed, opt-in, capped and never a gate.
- [ ] The ladder has an entry rung under 100 R$, a repeatable product and a top rung; no stat power in competitive modes.
- [ ] Every offer in the timing map names its trigger, surface and free alternative.
- [ ] Content maturity questionnaire answered truthfully; features that raise the rating (free-form creation, private spaces) are deliberate.
- [ ] All user-generated text filtered on the server.
- [ ] Gift and trade flows check price levels.
- [ ] A free alternative exists next to every paid shortcut.
- [ ] Each sized ladder passes the monotone-value and diminishing-bonus tests; every bonus, discount and timer shown is computed from server data.
- [ ] A purchase log records real Robux spent and the exact grant; a clawback policy is written; limits are enforced at prompt time and every paid receipt is honoured.
- [ ] The top rung is repeatable; no offer, timer or discount targets a failure moment or a specific spender.
- [ ] Live game: 28-day conversion, ARPPU and ARPDAU recorded before the change, with one primary metric and one guardrail (D1 or rating) per experiment.

For the full source text, grep `references/knowledge-base.md` for `## 3.6`, `## 3.7` and `## 3.8`.

## Sources

Accessed 2026-11-10. "(read)" = opened in the `Roblox/creator-docs` mirror (commit of 2026-11-07); "(search summary)" = seen only through web search result text.

- https://github.com/Roblox/creator-docs `content/en-us/production/monetization/`: `index.md`, `passes.md`, `developer-products.md`, `subscriptions.md`, `managed-pricing.md`, `price-optimization.md`, `regional-pricing.md`, `paid-random-items.md`, `roblox-plus.md`, `robux-transfers.md`, `shop.md`, `private-servers.md`, `immersive-ads.md`, `developer-exchange.md`, `18-plus-devex-rate.md` (read)
- Same repo: `content/en-us/creator-rewards.md`, `get-started/monetization.md`, `production/analytics/monetization.md`, `production/game-design/monetization-foundations.md`, `contextual-purchases.md`, `subscription-design.md`, `production/promotion/rewarded-video-ads.md`, `rewarded-video-optimization.md`, `rewarded-video-playbooks/incremental-sim.md`, `comply-with-advertising-standards.md`, `resources/feature-packages/bundles.md`, `reference/engine/classes/PolicyService.yaml`, `MarketplaceService.yaml` (read)
- https://create.roblox.com/docs/production/game-design/starter-pack-design (search summary; not in the mirror)
- https://www.gameanalytics.com/reports/2026-roblox-report and https://www.gameanalytics.com/reports/2025-roblox-report (search summary)
- https://gamedevreports.substack.com/p/gameanalytics-key-roblox-and-roblox and https://gamedevreports.substack.com/p/newzoo-roblox-as-a-platform-in-2025 (search summary)
- https://devforum.roblox.com/t/introducing-regional-pricing-for-passes/3621382, https://devforum.roblox.com/t/managed-pricing-one-system-for-better-pricing-and-earnings-growth/4684738, https://devforum.roblox.com/t/introducing-price-optimization-find-the-best-prices-for-in-experience-items-and-passes/3186081 (search summary)
- https://corp.roblox.com/newsroom/2025/04/roblox-launches-regional-pricing-for-in-experience-items (search summary)
- https://devforum.roblox.com/t/more-creators-can-now-use-rewarded-video-ads/3838678, https://devforum.roblox.com/t/increased-payouts-for-subscriptions-within-experiences/2963619, https://devforum.roblox.com/t/introducing-roblox-plus/4567894 (search summary)
- https://devforum.roblox.com/t/poll-starter-pack-price-points/397653, https://devforum.roblox.com/t/how-can-i-get-people-to-purchase-my-starter-pack/4032577, https://devforum.roblox.com/t/is-it-a-good-strategy-to-constantly-show-the-player-gamepasses/1090505, https://devforum.roblox.com/t/monetization-benchmarks-are-not-accurate/3006968, https://devforum.roblox.com/t/whats-the-best-price-for-a-skip-stage-devproduct/3364893 (search summary)
- https://techraptor.net/gaming/news/roblox-scammers-are-abusing-controller-bindings, https://rowatcher.com/news/the-roblox-free-to-play-illusion-what-players-think-they-bought (search summary)
- Live prices: https://pet-simulator.fandom.com/wiki/Gamepasses_(Pet_Simulator_99), https://blox-fruits.fandom.com/wiki/Shop, https://bloxodes.com/wiki/brookhaven-rp/gamepasses, Grow a Garden guides on beebom.com and deltiasgaming.com (search summary); +1 format from `references/market-scan-2026-11.md`
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/11 Monetization Publishing and Live Ops/` (`Robux Price Points and Offer Design`, `Pricing and Store Design`, `Unit Economics - ARPDAU, Payer Conversion, LTV and Ad Payback`, `Refunds Chargebacks and Purchase Support`, `Paid Random Items and Odds Disclosure in Practice` headings, `Subscriptions and Premium Payouts` headings), `38 Live Ops Deep Dive/Limited-Time Offers - Design and Ethics.md`, `Battle Pass and Season Design.md`, `Skill - Roblox Monetization Compliance.md`, `skills/roblox-monetization-compliance/SKILL.md` (read). Ideas adapted in our words; its offer-engine, ladder and webhook code was not imported.
- Wave-2 verification in the docs mirror: `cloud/webhooks/webhook-notifications.md`, `production/experiments.md`, `production/analytics/event-types.md` (read)
- Not reachable: reddit.com (no r/robloxgamedev or r/roblox thread surfaced in any search), direct fetches of devforum.roblox.com, create.roblox.com, gameanalytics.com and substack.com.
