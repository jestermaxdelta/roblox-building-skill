# Pet collection and hatching playbook

Covers games where the collection is the game: egg hatching, pet or creature collecting, merge and mutation tiers, indexes, trading, and the "___ For Eggs" journey formats. Open it when eggs, pets, units or cards with rarities drive progression, or when auditing a live game's hatch economy, odds compliance or trade safety. For roll-first games see `rng-rolling.md`. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One egg with 4–5 pets on a server-side weight table; an odds panel generated from that table; equip-best; pets rendered on clients; stacked inventory; no Robux eggs and no trading | Luck products, mutations, merge machines, trading, multi-hatch, seasonal eggs |
| Intermediate | Merge or fuse tiers on material variants; index with set rewards; pity; additive boosts with slot caps; a safe first roll (only good outcomes); auto-hatch; `PolicyService` gate before any paid egg | Trading plaza, event currencies |
| Expert | Atomic, logged, session-locked trading with anti-scam UI, cooldowns for new accounts and progress gating; live boosted-odds display; 30-day stacking model; event load planning for 3× players; retired items announced in advance | — |

Terms: *paid random item* = any random reward bought with Robux or with currency Robux can buy; *pity* = a guaranteed result after a number of unlucky rolls; *dupe* = an exploit that duplicates an item; *session lock* = only one server may load a player's data at a time.

## Snapshot

- Market position (vault, 2026-11-07): pets and eggs are **peaked but dominant**, with one rising pocket. Adopt Me! 167K CCU (about $60M a year; CCU roughly triples on updates), Pet Simulator 99 46–48K, Throw Food For Animals 311–324K (casual animal luck/collect, up 388% in 30 days, **rising**).
- Egg journeys are **crowded; only journey games break out**: Bike For Egg! 38K, Climb For Animals Eggs 27K, Ride An Egg 15K, Hike For Eggs 11.5K. Stat-only "+1 ___ For Eggs" sit at 27–1.5K and about ten "Dive for Eggs" at 0–213. Ride A Pet peaked at 1.55M on 3 Oct 2026 and left the top 10 within weeks.
- Pattern (vault #4, #5): the collection is the multiplier, 4–5 items per egg with the top one about 0.1%; merge or fuse tiers (3 into 1, 4 into 1) reuse the same assets for more rarity levels.
- Audience: the youngest on the platform; collectors and traders skew older. Sessions are hatch bursts (minutes) wrapped in a longer earn loop.
- Compliance weight is the highest of any genre: every Robux-linked egg is a paid random item `[official]`.

## Core loop with timings

| Step | What happens | Timing |
|---|---|---|
| Earn | The host loop pays currency (clicks, stages, income/s, a journey) | First egg affordable inside 2 min `[house]` |
| Hatch | Buy egg → reveal → pet with rarity | Reveal 1.5–3 s, skippable; auto-hatch for bulk `[house]` |
| Equip | Best pets multiply the host stat | Equip-best one tap |
| Merge | 3 or 4 of a kind → next tier (Gold, Diamond, Neon, Mega) | A merge available within the first 10 min `[house]` |
| Index | New entry lights up; set rewards | First set completes in session 1 |
| Trade / show | Trade plaza, pets follow or are ridden | After a play-time gate |

- Vault timings: Steal An Egg eggs grow at the pen for 10 s–25 min before hatching; Adopt Me pets are raised through 6 stages, 4 make a Neon and 4 Neons a Mega; Climb For Animals Eggs fuses 3 Gold into a Diamond.
- In +1 formats eggs hatch instantly for Wins (the owner's snowball decision); timers suit journey and steal formats where waiting is the tension.

## First 5 minutes

1. 0:00 the host loop pays immediately; the first egg stands in view with price and an odds button.
2. 1:00–2:00 first hatch; the pet appears beside the player and the stat multiplier visibly jumps.
3. 3:00 second and third hatch; a duplicate teaches merge or "equip best".
4. 4:00 index opens once, showing silhouettes of the egg's remaining pets and their odds.
5. 5:00 the next egg is visible at ×40–250 the price, with a rarer silhouette.
- No Robux egg prompt in this window. The free egg must be good enough to carry the first zone.
- A safe first roll `[lihfolk]`: the starter egg has only good outcomes (two results, both welcome), removing the "I got the bad one" exit. Script the first success so it cannot fail and pays immediately.

## Progression and economy shape

- Egg ladder (vault, +1 format): each egg costs ×40–250 the previous (Muscle: 100, 25K, 1M, 150M, 7.5B, 125B Wins); 4–5 pets per egg; top pet 0.1%; additive boosts +0.1 to +5; 3–4 starting equip slots.
- Mutation multipliers seen (vault): Silver 1.2× / Gold 2.5× / Rainbow 3.5× (Steal An Egg). Build tiers as Blender material and shader variants of one mesh: cheap content inside the Blender-only rule.
- Additive pet boosts keep balance tractable; multiplicative stacking across slots, mutations and luck explodes within weeks. Cap equip slots and state stacking rules.
- Pity protects the unlucky tail: guarantee the top tier by a fixed count and disclose it (at a 1% rate 63.4% already have it by roll 100).
- Sinks: merging consumes duplicates; enchant or reroll consumes currency; index rewards pull players back to old eggs; delete-for-shards recycles commons.
- Trading extends life by years (Adopt Me, MM2) but brings scams and duplication risk; decide before launch, since retrofitting changes every value.
- Rebirth as unlock, not loss `[lihfolk]`: attach features (teleport, auto-hatch, trading access) to rebirths so the milestone opens a door. Per-world currencies plus one global currency give soft resets without loss.
- A care loop is a cheap progress clock for "raise something" games: each need is a small walk and a small reward, and age is the visible bar `[lihfolk]`.
- Event design `[lihfolk]`: one event-only currency, weekly drops inside the event and a small multiplier pass that lasts for that event only (about 50 R$ in the leader). Keep event items cosmetic or collectible; event-only power creates pay-or-miss-out pressure.
- Retire passes and items on purpose and announce it in advance: collectible status without paid random boxes `[lihfolk]`. Removing purchased functionality without proper notice is listed under fraud in Roblox's standards `[lihfolk]` `[VS]`; rebalance paid items with notice and compensation.

## Monetisation set that fits

- Keep from the default set: Luck 2× 15 min, Server Luck (activator and end time announced), extra slots (equip, storage), Auto-Collect, Starter Pack (a fixed, disclosed pet, not a roll), VIP, gift passes, the host loop's 2× boosts.
- Add: Auto-Hatch, multi-hatch (3× / 8×), hatch speed, one Robux egg per world (vault: 79 R$ in +1 Muscle Evolution; 999 R$ premium eggs are cited for Pet Simulator X `[community]`).
- Delete: Revive; 2× EXP unless pets level.
- Rules `[official]` `[VS]`: eggs bought with Robux **or with currency purchasable with Robux** are paid random items. Show every outcome and its odds as percentages that sum to exactly 100% before purchase (a "1 in N" label may accompany but not replace the percentage); a lone "(i)" icon is not enough, label it; if a pet can be obtained only once, update the remaining odds for that player. Luck boosts must be explained numerically and the displayed odds must update live while active. Call `PolicyService:GetPolicyInfoForPlayerAsync`: when `ArePaidRandomItemsRestricted` is true, hide, replace or block the roll; when `IsPaidItemTradingAllowed` is false, block trading of paid items.
- Restricted-player fallback: sell the same pet directly at expected value (10 R$ roll at 5% → 200 R$) or offer earn-only eggs.
- House rule 3: no fake "limited" eggs; a limited egg has a real end date and does not return under a new name.
- Paid luck on rare items is the most sensitive product on the platform for a young audience; keep it modest and never the headline of the store. Launch with three to five passes, not thirteen `[lihfolk]`.
- Anything that lets items take on real-money value off-platform invites scams and account theft; limit what can be traded and never facilitate off-platform sales `[lihfolk]` `[VS]`.

## Retention and social hooks

- Rotating egg or stock on fixed timers (daily, weekly); seasonal pets that retire on a real date gain trade value honestly.
- Index completion rewards per egg and per world; "new" badge on first hatch.
- Trading plaza, pets that follow or can be ridden, friend boost +10–20%.
- Rare-hatch server announcement gives the shareable clip; keep it a toast, not a full-screen takeover.

## UI patterns

- Egg stand: price, "Odds" button with label, E / tap to hatch, auto-hatch toggle. Odds panel lists each pet, rarity and percentage summing to 100%.
- Inventory: grid with rarity frame, equip-best, multi-select delete with a lock toggle on favourites, merge progress "2/3".
- Trade window: both sides visible, a two-step confirm with a 3–5 s lock after any change, value hints, a recent-trades log `[house]`.
- Reveal is skippable and never blocks movement on mobile.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §4 Pets, eggs and hatching with odds, §2 Inventory and equip, §17 Trading, §3 Shop, §24 Server-wide events and boosts. Its "Build order by genre" table gives a second opinion.

1. Roll table module (weights, probabilities, luck) on the server.
2. Egg stands and hatch flow with a skippable reveal.
3. Inventory (stacked records, caps, locks) and equip slots.
4. Client pet followers in one update loop.
5. Odds panel and `PolicyService` gate.
6. Index with set rewards.
7. Merge, fuse and mutation tiers.
8. Pity counters; luck boosts with live odds.
9. Auto-hatch and multi-hatch.
10. Trading (atomic, logged) with anti-scam UI; then events and retired items.

## Technical hot spots

- **Rolls on the server only**, from the same weight table the odds panel renders. Rate-limit hatch requests; multi-hatch is one request with a count the server clamps.
- **Pet followers**: render on clients only. Server stores equipped ids; each client moves pets in one shared update loop (not one per pet) and caps how many of other players' pets it shows (community practice: 3–6 visible per player) `[community]`. `PivotTo` on many models per frame is the measured cost; throttle distant pets.
- **Inventory size**: stack identical pets as `{id, tier, count}`; give unique ids only to tradable or enchanted pets. Watch the 4,194,304-character key limit with large inventories `[official]`.
- **Trades are the duplication surface.** Session-locked profiles (ProfileStore) remove the multi-server dupe; but requesting both saves together is not enough: community threads describe crash-timed dupes when one side saves and the other does not `[community]`. Build trades on the two-profile commit protocol in `references/data-and-purchases.md` (intent, write-once decision record, single settle mutation, recovery on load), give every pet an immutable GUID, and keep a kill switch. If a dupe has already happened, follow "Runbook: dupe incident" in the same file.
- **Leaving mid-trade** cancels; never resolve a trade in `PlayerRemoving`.
- **Scam surface**: no trust trades (both sides must contain what is promised), no off-platform value, text in trade chat filtered. Gate trading behind play time and age-appropriate policy flags.
- **Index and odds data** for unreleased pets stay out of `ReplicatedStorage`.
- **Trading safeguards to build before launch** `[lihfolk]`: gate trading behind progress (for example after the first rebirth) to protect new accounts; a short trade-licence quiz before valuable trades; trade history; unfair-trade warnings; cooldowns for new accounts. The leader added these after the fact. If atomic, session-locked trades are out of reach, ship gifting or no trading.
- **Event load**: updates that triple players can take down servers and the data layer together; test data budgets and joins under event load `[lihfolk]`.
- A low-end mode: one toggle that removes effects and other players' pets `[lihfolk]`.

## The one-new-verb angle

- Change how the egg is obtained, not what is inside: bike, climb, hike, steal, throw food. The journey to the egg is the verb (vault: journey games lead; stat-only versions stall).
- Change what the pet does in the world: ride it, race it, work a job (staff take the place of pets in management games).
- Avoid: a new theme on the same egg wall.

## Common failure modes

- Odds not shown, or shown odds that differ from the roll table: policy strike risk and lost trust.
- Paid currency converted to eggs without the `PolicyService` gate (indirect purchases count).
- Multiplicative stacking that makes the newest egg mandatory within a week.
- Inventory flooding with commons and no bulk delete or merge.
- Trading shipped without session locking; one dupe collapses values.
- Server-side pet models for every player's team: server memory and replication spikes.
- "+1 stat For Eggs" with no visible journey (vault: fails).
- A weekly cadence the team cannot sustain: promise fortnightly and deliver rather than promise weekly and miss `[lihfolk]`.
- Copying the genre at small scale: care, collect, fuse, trade and events are one machine that takes a team `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Every egg has a labelled odds panel that sums to 100% and matches the roll table | Generate the panel from the server table |
| 2 | Boosted odds update live under Luck and Server Luck | Recompute and re-render on boost start and end |
| 3 | `ArePaidRandomItemsRestricted` and `IsPaidItemTradingAllowed` are enforced | Add the gate plus a direct-sale fallback |
| 4 | First hatch inside 2 min | Lower first egg price; pay faster early |
| 5 | Pity exists and is disclosed | Add a fixed-count guarantee |
| 6 | Duplicates have a use | Add merge tiers on material variants |
| 7 | Index exists with set rewards | Add per-egg and per-world indexes |
| 8 | Pets are client-rendered with a visibility cap | Move followers to the client; one update loop |
| 9 | Inventory stacks and bulk-deletes with favourite locks | Rework storage and UI |
| 10 | Trades are atomic, logged and session-locked | Move to a single server transaction with a trade-id log |
| 11 | Trade confirm relocks after changes | Add the 3–5 s relock and two-step confirm |
| 12 | Pet boosts are additive or capped | Convert stacking; cap slots |
| 13 | Limited eggs have real end dates | Remove restarting timers; publish dates |
| 14 | The egg is reached through a journey or action | Add a physical route or verb to obtain eggs |
| 15 | Starter roll has only good outcomes | Replace the first egg's pool |
| 16 | Trading is gated by progress with history, warnings and new-account cooldowns | Add the safeguards or disable trading |

## Review gate

- [ ] Odds, pity and luck effects are disclosed and identical to server data; policy flags enforced.
- [ ] Rolls, merges and trades run on the server in single steps; profiles are session-locked.
- [ ] Followers render on clients with a cap; inventory is stacked.
- [ ] Egg ladder, slots and stacking are modelled for 30 days of play.
- [ ] No fake scarcity; Starter Pack contents are fixed and disclosed.
- [ ] Pets, eggs and stands are Blender models; rarity follows the ladder in `references/blender-modeling-craft.md` (common tiers are palette variants, mid tiers add an accessory or scale, only top tiers get a new mesh) and merge tiers stay material variants; world objects are solid, followers are client-rendered and do not collide.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/content-maturity.md (read; questionnaire item on `ArePaidRandomItemsRestricted`)
- https://devforum.roblox.com/t/should-i-restrict-egg-opening-based-on-arepaidrandomitemsrestricted-policy/3278299 (search summary)
- https://devforum.roblox.com/t/update-on-paid-random-items-restriction-for-uk-users-under-18/3072183 (search summary)
- https://devforum.roblox.com/t/optimize-pet-follow/3166935 (search summary)
- https://devforum.roblox.com/t/my-pet-script-is-so-laggy-and-i-cant-figure-out-why/3495202 (search summary)
- https://devforum.roblox.com/t/preventing-duping-methods-in-trading/2688896 (search summary)
- https://devforum.roblox.com/t/making-a-secure-trading-system-without-external-database/4043236 (search summary)
- https://github.com/MadStudioRoblox/ProfileStore (search listing; 352 stars, Apache-2.0; session locking)
- https://www.metaversemarcom.io/post/inside-the-monetization-playbook-of-roblox-s-biggest-hit (search summary; third-party, Pet Simulator X premium egg price)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `32 Case Studies of Top Roblox Games/Case Study - Adopt Me.md`, `Case Study - Pet Simulator 99.md`, `10 Game Design and Genres/Genre Playbook - Simulators.md` §Pets and eggs, `skills/roblox-trend-game/references/trend-games-research.md` §8 (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
