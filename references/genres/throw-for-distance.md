# Throw-for-distance collection playbook

Covers "Throw ___ For Animals", "Throw a ___", "Shoot ___ For ___" and "Cast For ___" games: you train a power stat, throw (or shoot, or cast) something down a runway of zones, and the zone it lands in plus a luck multiplier that grows with distance decide which collectible comes to you; collectibles earn per second on your plot. Open it when the core action is a throw whose distance is the luck, or when auditing a live game in this format. Numbers are this pass's reads on 26 Nov 2026 (10:01–10:17 UTC, a Thursday) from Roblox's endpoints and Rolimons, called **G-26**, against the vault's 2026-11-07 snapshot `[VS]`; loop details come from player guides, not first-hand play.

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One runway with 4–5 zones, a power meter with one timing tap, a server-side distance and roll, 4–5 collectibles per zone, a plot with slots and income per second, one training bar, session-locked saves | Sizes, mutations, Server Luck, eggs, events, weekly zones |
| Intermediate | Luck that rises with distance and shows during the flight; size chain and 3–5 mutations from one config; Index; sell station; bar tiers; offline income with a stated cap; mantissa/exponent numbers | Admin events, cross-server banners |
| Expert | Weekly zone pipeline on a fixed day; Experience Events with real end times; a prestige layer before the zone runway runs out; product ladder of timed boosts with odds and `PolicyService`; telemetry per zone | — |

Terms: *runway* = the course the object flies along, split into zones; *Throw Power* = the trained stat that sets distance; *timing grade* = the PERFECT / GREAT result of the tap that adds power to one throw; *size chain* = repeated size-up rolls that stop at the first failure.

## Snapshot

- Market position (G-26): **a new format, risen in eight weeks, already crowded at the bottom**. Throw Food For Animals 164K CCU (created 18 Sep 2026; 311–324K on 7 Nov; tracker peak 2.45M during its 21–22 Nov Thanksgiving event, Rolimons, unconfirmed by press; 94.1% approval; average playtime 16.2 min; 5-player servers). Followers created 31 Oct–10 Nov: Throw a Seed 35.2K (peak 172.9K about 22 Nov), Shoot Arrows For Animals 29.0K (peak 68.8K, 98.7%), Fish For Sea Animals 29.0K, Fish for Secret Animals 16.5K, Cast For Fish! 14.0K, Throw a Friend for Monsters 10.0K.
- Clone density (G-26 search, 10:11 UTC): 31 of the first 40 results for "throw for animals" are "Throw ___" titles; 7 are above 2K and 23 under 1K. The followers that charted changed the object and kept the loop (seed and garden, bow, fishing line); noun swaps (Throw Food For Dinos, Throw Pets For Animals) have 0–300 players.
- What it is made of: the +1 trained stat (`plus-one-evolution.md`), an RNG reveal with "1 in X" (`rng-rolling.md`), a pet-style collection with sizes and mutations (`pet-collection-hatching.md`) and an idle plot (`tycoon-and-cozy-management.md`). Its one new idea is that the stat becomes a visible distance and the distance is the luck, which is the vault's hybrid rule ("the stat must become a place") borne out.
- Lifecycle (inference): the formats it displaced on the 7 Nov chart (+1 evolutions, egg journeys, cozy management) kept a median 0.27× of their 7 Nov CCU by 26 Nov, against 0.63× for pre-2026 games (`case-studies-teardowns.md` §4). Plan for the same arc: weeks of rise, a short plateau on weekly events, then a fall, unless a second verb or a prestige layer arrives first.
- Audience: young, casual, phone-first, idle-tolerant (training runs itself). Small servers (5) keep everyone's throws and plots within sight.
- Dashboard genre: Simulation › Tycoon (the leader) or Simulation › Incremental Simulator (Throw a Seed) `[VS]`. Full teardown of the leader and its fastest follower: `case-studies-teardowns.md` §2.19.

## Core loop with timings

| Step | What happens | Observed in the leader (guides, Nov 2026) |
|---|---|---|
| Train | Stand in the bar's circle; reps run on their own; XP levels add power | +5 Throw Power per level; a level every 35–45 s around level 270; each bar tier doubles XP per rep; floating ×2 bubbles double one rep |
| Throw | Walk to the line; one tap on a rising meter | PERFECT +19–20, GREAT +17–18 on top of the stat |
| Fly | The camera follows the object across coloured zones; a Luck multiplier climbs on screen | 10 zones at launch, 19 by late Nov; about ×18 over the mountains, ×28 at the deep-water zone; a skippable cut-in for the furthest zone |
| Reveal | A collectible from the landing zone arrives; a counter cycles odds and stops | "1 in X" callouts (LUCKY 1 in 23, SUPER LUCKY 1 in 51); NEW and NEW BEST tags |
| Roll | Mutation, then a size chain | 79.5% no mutation, Rainbow ×20 income; size 20% for the first step, +5% per success, capped at 40%; income ∝ size^1.8 |
| Place or sell | Plot slots; Equip Best; sell the rest | 14 slots mid-game; sale price = 20× income |
| Spend | Better food (rarity), better bar (power), more slots | 50 foods from Common to Sovereign; prices into the 10^50s |
| Weekly | New zone and an admin event | Saturdays 06:00–09:00 PT; a holiday event of about a day |

- Pace `[house]`: first throw inside 15 s, first catch inside 30 s, first income tick inside 45 s, first bar upgrade inside 5 min, a new zone inside the first session.
- A throw cycle (walk, tap, flight, reveal) of about 10–20 s (inferred from guide screenshots; not timed) keeps a decision every few seconds; flights longer than about 8 s need a skip.
- Each lever answers one shortfall and the game should say which: food lands short → train; it lands far but catches are weak → better food (the leader leaves this to guides).

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; the nearest rows in its §10 are simulator and pet. No offer or social card in this window (offer gate).

1. 0:00 spawn on your plot facing the runway; the starter item is equipped; "TAP TO THROW" glows at the line.
2. 0:10 first throw: one tap, a short flight over one or two zones, the luck number ticking.
3. 0:25 the first collectible walks up; its card shows $/s; it is placed in one tap and starts paying.
4. 1:00 throws two and three; the first size or mutation roll gets a celebration.
5. 2:00 the training bar is pointed out: one set, "LEVEL UP +5", and the next throw visibly lands further.
6. 4:00 first item upgrade bought with plot income; the next zone's silhouettes show in the Index.
- The thumbnail promise (the arc, the zones, the rare animal with its $/s) must happen in this window: tiles rank by qualified plays.

## Progression and economy shape

- Three levers, never one: power (distance → zone), item tier (rarity inside a zone), luck (distance multiplier plus boosts). A single lever turns the game into a menu.
- Zones are the map, the luck curve and the content runway at once: 4–8 collectibles per zone (one guide counts about 140 animals across 17 areas), top item about 0.1% (vault pattern 4).
- Income = base × mutation × size^k, with sale price a fixed multiple of income (the leader uses 20×), so every catch converts to progress.
- Plot slots are the capacity sink; Equip Best keeps the plot honest without a spreadsheet.
- Offline income with a stated cap `[house]`; the leader shows an offline-earnings banner on return.
- Numbers explode (the leader's suffixes run past 10^50): store mantissa and exponent from day one.
- No rebirth was described in the guides read on 26 Nov. Plan a prestige layer before the zone runway runs out (inference: the +1 and egg formats that lacked a second layer fell hardest in November).
- No wagers or coin flips of collectibles between players: Roblox prohibits simulated gambling `[lihfolk]` `[VS]`.

## Monetisation set that fits

- What the market sells (G-26, measured): the leader has two passes (x2 Cash 99, x2 Training Power 149) and 53 developer products: Lucky Throws 9–499, Server Luck 2× / 4× / 8× / 16× at 19 / 39 / 79 / 159, timed training 39–179, cash packs 24–199, eggs 60–799, named animals sold outright up to 4,400 and 12,000. Followers add permanent luck passes (Throw a Seed: Double Luck 249, a ×15 Rainbow Seed 799; Throw a Friend for Monsters: x4 LUCK 699, x4 MONSTERS 999) and Auto Throw 149–199.
- Keep from the default set: 2× Cash 10/30 min, 2× Training (as 2× XP), Luck 15 min and Server Luck (paid random items: numeric odds summing to 100% before purchase, boosted odds live, `PolicyService` gate), Starter Pack, extra plot slots, VIP, gift versions, private servers.
- Add: throw trails and impact effects, runway and plot skins, Index cosmetics, a "skip flight" convenience.
- Delete or rework: permanent luck passes and luck multipliers at the top of the ladder; direct sale of the rarest collectibles; stacked ×4 multipliers (cap the stack, `economy-and-progression.md`); Revive (no death).
- **Conflict (market vs this skill's monetisation defaults):** the format's stores put paid luck and 12,000 R$ animals at the top. House rule 3 lists Luck and Server Luck as timed boosts in the default product set, and paid random items need full numeric odds summing to 100%, boosted odds shown live and a `PolicyService` gate (`SKILL.md`). The skill's default `[house]` goes further: luck stays a disclosed, timed boost rather than the top of the store, and the rarest collectibles stay earnable. Price the top of the ladder with cosmetics, slots and convenience instead (monetization-and-policy.md).
- Auto Throw: allowed as convenience only if the timing grade it uses is GREAT, not PERFECT, so skill still pays `[house]`.
- Offers at positive moments only: a NEW BEST catch, a new zone, a bar upgrade; never after a dud roll.
- Rewarded video: rewards are fixed, never random `[official]` `[VS]`: grant training minutes or 2× Cash, not a lucky throw.
- Store-list copying is cheap: a follower mirrored most of the leader's product ladder item for item at prices about 3–5% lower (G-26). Your store is not a moat; your verb and art are.

## Retention and social hooks

- A new zone every week on a fixed day, each with 4–8 new collectibles and one look; events as Experience Events with real end times.
- Server-wide banners for rare rolls ("INSANE LUCK! 1 in 220" in the leader): social proof that rare things are reachable. Rate-limit them.
- Index per zone with silhouettes of what is missing; offline income with a stated cap; daily gifts.
- Five-player servers keep every throw visible; friend boosts are bonuses only, never gates.

## UI patterns

Genre specifics only. Zone layout and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre; the simulator and pet layouts are closest). Effects to build first, from `vfx-recipes.md`: rarity reveal, coin or reward burst, aura for rare items.

- Throw meter: large, centre-bottom, inside thumb reach; the PERFECT band visible; grade text and "+N power" on release.
- Flight view: follow camera with zone names and the live luck multiplier; a skip button on long flights.
- Reveal card: name, size, mutation, $/s, "1 in X", NEW / NEW BEST tags; the full odds table for that zone one tap away ("Chances"), generated from the roll table `[lihfolk]`.
- Plot: floating income tags; Equip Best; a sell ring with an Auto Sell toggle that never sells a mutated or sized-up item without confirmation.
- HUD: cash, income per second, Throw Power, next zone's distance requirement. Index, Shop and Collection buttons stay visible on the runway.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §1 Currency and wallet, §4 Pets, eggs and hatching with odds, §16 Plots, tycoon ownership and placement, §5 Upgrades and rebirth, §7 Daily rewards and playtime rewards, §24 Server-wide events and boosts. For the flight, `physics-and-vehicles.md` §9 Projectiles (here a precomputed arc, not a simulated body).

1. Zone config: distance bands, luck curve, collectible tables per zone, all in one module.
2. Throw service: power + timing grade → distance → zone → rolls, all on the server; returns the arc and the result.
3. Collectibles: species, size chain, mutation, income formula, Index.
4. Plot: slots, placement, income tick, capped offline income, session-locked saves.
5. Training bar: auto-rep XP, levels, bar tiers.
6. Shop: item tiers, bar upgrades, slots; sell station and Equip Best.
7. Timed boosts and Server Luck with odds display and `PolicyService` gate.
8. Server banners, daily gifts, friend boost.
9. Weekly zone pipeline and admin-event framework.
10. Prestige layer before the last planned zone ships.

## Technical hot spots

- **The server owns distance and the roll.** The client sends "throw" and its tap time; the server checks the tap against its own meter phase (meter start as a server timestamp, known period), grades it, computes distance from server-known power, picks the zone and rolls with a server `Random`. Never accept a client distance, zone or catch.
- **Flight is a cutscene, not physics.** Send the precomputed arc (start, apex, landing, duration) and let the client animate a Blender mesh along it; the luck readout is a function of distance along the arc. No unanchored projectile, no network-ownership fights.
- **Rate-limit throws** to one in flight per player, and the training tick to 1 Hz on the server with replication at 1–2 Hz.
- **Odds display from the rolling code**: the "Chances" table and the "1 in X" labels read the same config the server rolls from; boosted odds are recomputed live.
- **Long runways**: 19 zones is a lot of map. Stream distant zones, use low-detail meshes far away and a camera cut for very long throws; budget for a 3 GB Android phone at the furthest zone.
- **Plots full of animated collectibles**: cap visible animations, share rigs and animations, idle motion on the client.
- **Big numbers**: mantissa and exponent with a suffix table that reaches well past 10^50.
- **AFK training**: idling is the format; exclude idle time from rewards that should need presence, and design the 20-minute idle disconnect into the offline cap `[VS]`.
- **Every collectible, runway prop, bar and plot is a Blender model with collision** `[house]`; the thrown object is an effect mesh and does not collide.

## The one-new-verb angle

- The verb is "throw for distance"; the object and the receiver are only theme. Change what the distance does, not the noun: the landing spot grows something you keep (Throw a Seed's garden), the throw is a co-op relay, distance pushes into a scarier zone (the owner's open gap: fishing × anomaly, `fishing.md`), or the object bounces and skips so the path matters, not only the length.
- Keep the spine: trained stat → visible distance → luck → collection → plot income.
- Do not ship "Throw ___ For ___" with a new noun: 23 of the 31 such titles had under 1K players eight weeks in (G-26).

## Common failure modes

- A noun swap of the leader after its peak, with its thumbnail composition and product list.
- Luck that does not depend on distance: the format's whole promise is that further is luckier.
- Flights so long they bore or so short there is no spectacle; no skip.
- Client-reported distance, zone or catch; throws without a rate limit.
- Paid permanent luck and Robux-sold top collectibles; offers after a dud roll.
- No second layer: once the last zone is reached there is nothing to do but wait for Saturday.
- Number inflation without sinks; Auto Sell that destroys a rare catch.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First throw inside 15 s and first income inside 45 s | Equip the starter item at spawn; put the line beside the plot |
| 2 | Distance, zone and rolls are computed on the server | Move the throw to a server service; send intent only |
| 3 | The luck multiplier is visible during the flight and rises with distance | Add the readout; tie luck to distance in the config |
| 4 | The game says which lever is short (power or item) | Add a landing hint ("lands short: train") |
| 5 | Every paid random path shows full percentages before purchase and respects `PolicyService` | Add a "Chances" panel generated from the roll table |
| 6 | No permanent luck pass, and no top collectible sold for Robux | Convert to timed boosts and cosmetics; grant equal value to past buyers |
| 7 | Flights over about 8 s can be skipped | Add a skip; cut long flights |
| 8 | Each zone has 4–8 collectibles and an Index page | Fill thin zones before adding new ones |
| 9 | A new zone ships on a fixed weekday with an Experience Event | Commit to a day and a runway of zones |
| 10 | A prestige or second layer exists before the last planned zone | Design it now; ship it before the content runs out |
| 11 | Auto Sell never sells a mutated or sized-up item silently | Add a filter and a confirmation |
| 12 | Numbers use mantissa and exponent | Migrate the number type behind a flag |
| 13 | Median session is 16+ min and the furthest zone runs on a 3 GB phone | Stream zones; trim the far-zone budget |
| 14 | Title, thumbnail, icon and store list are your own, not the leader's | Restyle; rename; rebuild copied layouts |

## Review gate

- [ ] The throw, the flight, the reveal and the plot each fit one sentence, and the distance is what the player watches.
- [ ] Distance, zone and every roll are server-owned, rate-limited and logged.
- [ ] Zone tables, sizes and mutations live in one config that also drives the odds display.
- [ ] The store sells timed boosts, slots, convenience and cosmetics; luck is a disclosed timed boost, never the top of the ladder; top collectibles are earned.
- [ ] A weekly zone day and a prestige layer are scheduled before launch.
- [ ] The concept changes what the distance does, not only the noun; nothing copies a leader's art, names, thumbnail or interface.
- [ ] Collectibles, runway props, bars and plots are Blender models with real collision.

## Sources

Accessed 2026-11-26 (G-26: 10:01–10:17 UTC; raw pulls in the research scratch folder `data/genres/`).

- Roblox explore sorts, games, game-pass (`apis.roblox.com/game-passes/v1/universes/<id>/game-passes`), developer-product (`apis.roblox.com/developer-products/v2/universes/<id>/developerproducts`, undocumented) and omni-search endpoints (measured); https://www.rolimons.com/game/120219252362013, https://www.rolimons.com/game/129081220403721 and the follower pages (read; peaks, average playtime, rating)
- https://allthings.how/throw-food-for-animals-food-and-zone-guide-prehistoric-forest-to-deep-waters/, https://allthings.how/throw-food-for-animals-mutations-every-chance-and-income-multiplier/, https://allthings.how/throw-food-for-animals-sizes-and-mutations-odds-and-income/, https://allthings.how/throw-food-for-animals-mutation-guide-throw-power-training/ (read; guides dated up to 14 Nov 2026)
- https://bloxodes.com/wiki/throw-food-for-animals and https://bloxodes.com/wiki/throw-a-seed (read; zone counts, event list and times)
- https://www.ggrecon.com/articles/roblox-top-games-didnt-exist-before-october/ (read; 18 Nov chart read: the leader at #5 with 184,865)
- Search summaries (2026-11-26): guide disagreement on zone names and counts (10, 15, 17 or 19 areas over time) and on whether size and mutation stack additively; the AllThingsHow multiplicative formula is used here and is unverified in-game.
- https://create.roblox.com/docs/production/monetization/paid-random-items (rule summary held in `monetization-and-policy.md`; not re-read in this pass)
- See also `references/case-studies-teardowns.md` §2.19 for the full teardown.
