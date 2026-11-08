# Monetization and policy

Distilled from knowledge-base sections 3.6, 3.7 and 3.8 (plus 1.6.5). The house rule is "push microtransactions heavily, but never invasively". Non-invasive is the most important rule. Items marked `[VS]` change often; check https://create.roblox.com/docs before quoting them.

## Catalogue of monetization surfaces

| Surface | Rules and limits `[VS]` | Use for |
|---|---|---|
| Game pass | One-time, non-transferable. 5-day payout hold. Owned forever; check on the server. | Permanent perks: 2× Cash, Auto-Collect, VIP, extra slots |
| Developer product | Repeatable, 1–1,000,000,000 R$. Grant only inside the receipt callback. | Boosts, currency packs, revives, skips, Gift versions of passes |
| Robux subscription | At least 49 R$ per month, single tier per subscription, price change at most every 60 days, 50 subscriptions per game. | VIP monthly |
| Local-currency subscription | $2.99–$14.99 tiers; creator receives 70% in month one then 100%; 30-day hold; unavailable in some countries. | VIP monthly on supported platforms |
| Paid access | 25–1,000 R$, or $9.99 / $29.99 / $49.99 in local currency with a 50 / 60 / 70% share. Not on Xbox for Robux; local currency on desktop and web only. | Premium games only; not for discovery-driven titles |
| Private servers | Free or priced | Groups of friends |
| Plus incentives | 100 R$ cap per subscriber per month; up to 250 R$ a month for three months | Bonus Robux for Plus members |
| Robux transfers | Game receives 10% | Player-to-player gifting |
| Avatar items | 40% affiliate share on items sold in-experience | Shop surfaces |
| Rewarded video | 3–10 R$ equivalent reward; needs 2,000+ monthly visitors, 13+ audience, ID verification and 2FA | Free alternative to paid boosts |
| Creator Rewards | Daily Engagement (5 R$ per qualifying day), Active Spender ($9.99+ in 60 days), Audience Expansion (35% of a new user's first $100); needs 100+ DAU, ID verification; 60-day hold | Passive income you influence through retention |

Other facts `[VS]`: the creator share on Robux sales is 70%. Cross-game sales of passes have been disabled since 30 May 2026. The DevEx rate is $0.0038 per Robux (from 5 September 2025; legacy $0.0035), and $0.0054 for US 18+ sales from 8 June 2026, which requires R15-only avatars. Per 100 R$ sold you keep 70 R$, worth about $0.266 (or $0.378 at the 18+ rate). Managed (regional) pricing scales prices to 30–100% of base. Price optimization needs roughly 60,000 transactions in 30 days to be meaningful.

Never hard-code prices in UI. Read `PriceInRobux` through `MarketplaceService:GetProductInfoAsync(id, Enum.InfoType.Product or GamePass)` (`GetProductInfo` is deprecated) and cache it per session only. `RankProductsAsync` is rate-limited; call it once at join. `RecommendTopProductsAsync` returns up to 50 products.

## The house default product set

| Product | Type | Price (R$) | Notes |
|---|---|---|---|
| 2× Cash, 10 min | Dev product | 29–49 | Real-time expiry; buying again extends |
| 2× Cash, 30 min | Dev product | 79–99 | |
| 2× EXP, 10 / 30 min | Dev product | 29–49 / 79–99 | Only if the game has XP |
| 2× Speed (delivery, gather, click), 10 min | Dev product | 25–39 | |
| Luck 2×, 15 min | Dev product | 49–79 | Only with luck mechanics; paid random item rules apply |
| Server Luck | Dev product | 149–249 | Announced to all, with activator and end time |
| Starter Pack | Dev product | 49–99 | One per account (saved flag); after first win only |
| Auto-Collect | Game pass | 199–299 | Convenience |
| Extra storage / slots | Game pass | 129–199 | |
| Permanent 2× Cash | Game pass | 399 | |
| VIP | Game pass or subscription | 799 one-time, or 499 R$ per month / $4.99 | Cosmetic plus convenience, never power in PvP |
| Gift versions of passes | Dev product | Same price as the pass | Grants an entitlement in the recipient's data |
| Currency packs | Dev product | 49 / 99 / 399 / 999 / 2,499 | Bulk bonus up to +15% |
| Revive / second chance | Dev product | 15–30 | Roguelike, horror; never during a chase |
| Private server | Server | 0–100 | |

Market prices are a 2026-11-07 snapshot `[VS]`. Luck and Server Luck exist only in games with random rewards; in those games they are paid random items and need odds disclosure plus the PolicyService gate.

Boost rules: stacking the same boost extends duration (cap it, for example at 6 hours) and never multiplies; different boost types multiply with each other; state whether the timer is real time or play time; show a HUD timer pill with the honest remaining time.

Recommendation. Lower-risk: ship the default set above plus two or three rewarded-video placements, all surfaced through the shop and contextual, dismissible offers. Bold: add a VIP subscription, a premium season pass and Server Luck events, but only after D1 and D7 retention meet your genre's benchmark; monetizing a leaky funnel burns the audience Recommended For You sends you.

## Offer and shop playbook (house rule: never invasive)

Shop design: integrated into the world (a Blender-modelled shop counter with a prompt), contextual (offer the thing the player is looking at), and inviting. Use neutral calls to action such as "View Item", "See Price" or "Open Shop", not "BUY NOW".

Offer gate rules (implement as Configs so you can tune them live):

- Grace period: no offers until the player has at least 10 minutes of lifetime play **and** has had a first win.
- Positive triggers only: after a delivery, a level-up, a round win, a rebirth. Never on death, failure, loading or join.
- Size: at most 25% of the screen, in a safe-area corner outside thumb zones, with an X, never stacked.
- Frequency: at least 8 minutes between offers, at most 3 per session, at most 1 starter-pack prompt per day, and suppress an offer for 24 hours after two dismissals.
- No sound stings, no shaking buttons, no countdowns that restart, honest copy.
- Passive surfaces (shop button, shop shelves, HUD boost pill) are unlimited.
- Always show a free alternative next to a paid one (rewarded video, wait, or earn in play).

Gate sketch (server-side; read the numbers from `ConfigService`):

```lua
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

Boosts module sketch (state is `{ [boostId]: unixExpiry }` in the profile):

```lua
local MAX_STACK_SECONDS = 6 * 60 * 60
function Boosts.add(state, boostId: string, seconds: number)
	local now = os.time()
	local current = state[boostId]
	local base = if current ~= nil and current > now then current else now
	state[boostId] = math.min(base + seconds, now + MAX_STACK_SECONDS)
end
function Boosts.remaining(state, boostId: string): number
	local e = state[boostId]
	return if e ~= nil then math.max(0, e - os.time()) else 0
end
function Boosts.multiplier(state, boostId: string): number
	return if Boosts.remaining(state, boostId) > 0 then 2 else 1
end
```

## Rewarded video

- Opt-in, 6–30 seconds, rewards a fixed developer product worth 3–10 R$; never a gate, never random, pause gameplay damage while it plays.
- Eligibility: 2,000+ monthly visitors, 13+ rating, ID verification and 2FA `[VS]`.
- API: `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)`, `AdService:CreateAdRewardFromDevProductId`, `AdService:ShowRewardedVideoAdAsync`, `AdService:RegisterAdOpportunityAsync`.
- Targets from Roblox playbooks: opt-in 10–20%+, 2–4+ views per viewer per day, 0.5+ impressions per DAU.
- Good placements by genre are in genre-playbooks.md.

## Gift passes

Game passes cannot be transferred, so a gift is a developer product that writes an entitlement into the recipient's profile. Flow: the buyer picks a recipient; the server checks `canGift` (not self, recipient does not own it, not already gifted, buyer's price level is at least the recipient's via `GetUsersPriceLevelsAsync`, fail closed on errors); store `PendingGiftTarget` in the buyer's profile; prompt the product; in the receipt handler set `Entitlements[passId] = true` on the recipient's profile if it is loaded, or deliver through `ProfileStore MessageAsync`, keyed by the `PurchaseId` so repeats are harmless. Every perk check is `ownsPass or data.Entitlements[pass]`. Code is in data-and-purchases.md.

## Policy: what is banned and what must be disclosed `[VS]`

- Discounts must be genuine. No false scarcity, no countdowns that restart, no "only 3 left" that is not true.
- **Paid random items** include anything bought with Robux or with currency bought with Robux whose outcome is random, including crates, eggs, summons, probability modifiers (Luck, pity, rate-up) and indirect purchases.
  - Show every possible outcome with numeric odds before the purchase. An "Info" or "Details" button opening a popup is acceptable; a bare (i) icon is not.
  - Odds sum to exactly 100%, update when outcomes retire, and reflect live boosts.
  - When `PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted` is true, offer a free path, a fixed-order unlock, direct sale at expected value, or hide the feature; never sell the random item.
  - `IsPaidItemTradingAllowed` gates trading of paid items. Rewarded-video rewards cannot be random.
- Content maturity labels: Minimal and Mild are available to Kids and Select audiences; Moderate to Select and 16+; Content May Vary to 16+; Restricted (18+) is unplayable in Korea, Saudi Arabia and Türkiye. Free-form social hangouts are 16+; private spaces (bedrooms, bathrooms) 18+. Playable gambling is banned. Resubmitting the questionnaire pauses ad eligibility.
- Thumbnails and video: no spoken audio, no real footage, no ad text in video thumbnails.
- Notifications: no dark patterns, never gate gameplay on opting in.
- Filter all user text with `TextService:FilterStringAsync`.
- Incentivised likes, favourites and group joins are a common market pattern but are not covered by the docs; treat them as a policy risk and never gate progress on them.

Policy module sketch (cache per player, 3 retries, fail closed):

```lua
local function canBuyRandomItems(info): boolean return info.ArePaidRandomItemsRestricted == false end
local function canTradePaidItems(info): boolean return info.IsPaidItemTradingAllowed == true end
local function canSeeAds(info): boolean return info.AreAdsAllowed == true end
```

## Compliance ship gate

- [ ] Every paid random item shows full numeric odds (summing to 100%) before purchase, including boosted odds.
- [ ] `PolicyService` gates random items, paid-item trading and ads; failures fail closed.
- [ ] No fake discounts, restarting countdowns or false scarcity anywhere.
- [ ] No offers in the first 10 minutes, on loading, or before the first win; rate limits in place.
- [ ] Prices are read from `GetProductInfoAsync`; nothing is hard-coded.
- [ ] Grants happen only in the receipt handler or pass ownership checks, never from UI signals.
- [ ] Rewarded-video rewards are fixed, opt-in and never a gate.
- [ ] Content maturity questionnaire answered truthfully; features that raise the rating (free-form creation, private spaces) are deliberate.
- [ ] All user-generated text filtered on the server.
- [ ] Gift and trade flows check price levels.
- [ ] A free alternative exists next to every paid shortcut.

For the full source text, grep `references/knowledge-base.md` for `## 3.6`, `## 3.7` and `## 3.8`.
