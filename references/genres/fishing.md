# Fishing and catch-collection playbook

Covers fishing games and their close relatives (bug catching, digging, netting): a short skill minigame on top of a luck roll, a bestiary per zone, a gear ladder and travel between waters. Open it when "cast, catch, collect" is the loop, when designing catch odds and luck products that pass policy, or when auditing a live fishing game for AFK abuse and expansion design. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One dock, one free rod already equipped, a two-step cast-and-reel, 10–16 species with a visible checklist, a seller and two rod upgrades | Boats, weather, mutations, trading, battle pass, AFK mode |
| Intermediate | One weighted catch table that feeds both roll and UI; "1 in X" display; per-zone bestiary rewards; world state (time, weather) gating some fish; server sanity checks on reel results | Cross-server rare-catch feed, crews |
| Expert | Live boosted-odds screen; capped AFK fishing; seasonal seas that add without resetting; statistical macro detection; economy telemetry per rod tier | — |

Terms: *bestiary* (index) = the collection log of species caught; *mutation* or *variant* = a random modifier on a catch (size, colour, effect) that multiplies value.

## Snapshot

- Market position (vault, 2026-11-07): **durable, up 55% year on year**. Fisch 79K CCU (510K tracked on a 17 Oct 2026 event), Fish It 63K (2.7M peak), Net a Fish 14K, Deep Fishing 4.3K. A bare "+1 Fishing" had 4 players.
- Two proven shapes `[lihfolk]`: the deeper original (Fisch: hundreds of species, a reel-bar skill minigame, weather, time and seasons; about 91% positive; 20-player servers) and the simplified follower (Fish It: click to charge, click fast to reel, auto-equipped rod, quest arrows, islands close together; about 83% positive; average session about 30 min linked to AFK auto-fish, unverified).
- The follower grew when the leader stumbled `[lihfolk]`: an expansion that required level 200, added a new currency, weakened old rods and raised the level cap told players their progress was worth less; in-game polls later decided its fate.
- Open gap (vault): fishing × anomaly or deep-sea horror; nothing above 2K (It Hears The Water 1.5K). The vault's shelved co-op anomaly-fishing concept scored 30/35 with a 6–8 week MVP and the longest expected life on its list.
- Audience: broad and calm; parallel play where nobody can harm anyone. Dashboard genre: Simulation `[VS]`.

## Core loop with timings

| Step | What happens | Target |
|---|---|---|
| Cast | Hold or click to charge and cast | 1–2 s |
| Wait | Bite timer; optional "shake" action to shorten it | 3–10 s early `[house]` |
| Reel | Skill minigame: keep a bar on a moving target, or click rhythm | 3–8 s; harder fish take longer `[house]` |
| Reveal | Species, size, variant, "1 in X", new-entry stamp | Under 2 s |
| Sell or keep | Seller NPC or sell-anywhere; index fills | Trip under 20 s `[house]` |
| Upgrade | Better rod, bait, boat → new water | First rod upgrade in minutes |

- Skill on top of luck is the genre's core insight `[lihfolk]`: the minigame makes every catch an action; the roll makes every catch a lottery. Skill stops it feeling like a slot machine; luck stops it feeling like work.
- First catch in under a minute; the simplified shape delivers it in seconds `[lihfolk]`.

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; this genre's row is in its §10. No offer or social card in this window (offer gate).

1. 0:00 spawn on a dock with the rod equipped (auto-equip) `[lihfolk]`.
2. 0:15 first cast with a two-line prompt; put the same two lines in the store description `[lihfolk]`.
3. 0:45 first catch: size, a small variant chance, bestiary entry 1 of N.
4. 2:00 an arrow to the seller; first coins buy rod 2.
5. 5:00 three to five species logged, the zone checklist visible with its completion reward, the next island in sight.
- Put a finite checklist on the first island: session one gets an ending and session two gets a goal `[lihfolk]`.

## Progression and economy shape

- Gear ladder: rods (permanent stats: luck, control, speed), bait (consumable modifiers), boats (zone access). Guides for the leader advise upgrading rods before bait because rod stats are permanent `[lihfolk]`.
- Zones: each island or sea has its own bestiary and conditions. Boats gate zones; short travel suits younger players.
- Catch value = species base × size roll × variant multiplier. One weight table per zone; display each species as "1 in X". The denominator on display is what players chase: catching a 1-in-millions fish becomes a story `[lihfolk]`.
- World state as retention `[lihfolk]`: fish tied to weather, time of day and season create "come back at night in the rain" goals with no calendar UI.
- Sinks: rods, bait, boats, enchanting or appraisal rerolls, aquarium or trophy display, zone fees.
- Expansions add, never reset: new seas use existing currency or a convertible one, keep old gear useful and gate by achievable goals. Poll concepts before shipping, not after `[lihfolk]`.
- AFK auto-fishing lowers the skill floor and lengthens sessions, but Recommended For You credits at most 60 minutes per user per day, so AFK time beyond that buys no discovery `[lihfolk]` `[VS]`. Cap AFK yield below active play.

## Monetisation set that fits

- Keep from the default set: 2× Cash, 2× EXP, Starter Pack (a fixed rod or bait bundle), extra storage, VIP, gift passes, private servers, Luck 2× and Server Luck.
- Add "anywhere" convenience: sell anywhere, appraise or enchant anywhere, spawn boat anywhere. They remove a walk, not a challenge `[lihfolk]`. Observed prices `[lihfolk]` `[VS]`: sell-anywhere 315–399 R$, double XP 195–239, cosmetic packs 99, luck passes in three sizes at 50 / 245 / 545.
- Add: bobber and rod skins, emote packs, boats as cosmetics, a season pass with real end dates.
- Delete: Revive, Auto-Collect (unless AFK fishing is the product), permanent power in any fishing tournament mode.
- **Luck is regulated** `[official]` `[VS]`: a paid item that improves odds must state its effect numerically before purchase, and displayed odds must update live while it is active. Rolls bought with Robux or Robux-bought currency (crates, gacha, appraisal rerolls) need full outcome lists as percentages summing to exactly 100% ("1 in X" may sit beside the percentage, not replace it), the `PolicyService` gate, and a trading check. The "1 in X" habit is a strong base: extend the same table into the purchase screen `[lihfolk]`.
- Offer timing: after a new bestiary entry or a rare catch, at the seller, on return. Never mid-reel.

## Retention and social hooks

- Per-zone bestiary completion rewards; rare-catch announcements server-wide make one player's luck everyone's moment `[lihfolk]`.
- Weekly update on a fixed day (the leader's guides report Saturdays) with teaser tags: `[SOON]` days before, `[NOW]` on the day `[lihfolk]`.
- Crews and group fishing events add a reason to play together `[lihfolk]`; friend bonus +10–20%.
- Seasonal waters with secret fish and honest end dates.

## UI patterns

Genre specifics only. Zone layout for this archetype and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre). Effects to build first, from `vfx-recipes.md`: water splash, hatch or open reveal for the catch card, coin or reward burst.

- Reel minigame centred and large; one input on touch. Optional "perfect reel" bonus keeps skill for older players `[lihfolk]`.
- Catch card: species art, size, variant, "1 in X", new-entry stamp, sell or keep.
- Bestiary: silhouettes, habitat and condition hints, per-zone progress bar.
- Odds screen: base odds, active boosts and boosted result side by side `[lihfolk]`.
- Thumbnails: scale contrast (small avatar, enormous creature), in-engine look so the first session matches; news goes in the title tag, not the art `[lihfolk]`.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §4 Pets, eggs and hatching with odds, §2 Inventory and equip, §3 Shop, §6 Quests and achievements, §23 Time and day cycle, §24 Server-wide events and boosts. Its "Build order by genre" table gives a second opinion.

1. Cast and reel minigame (client feel, server validation).
2. Weighted catch table with "1 in X" display.
3. Inventory with stacking and caps; seller.
4. Player data with session locking.
5. Gear shop: rods, bait.
6. Bestiary (index) and zone quests with arrows.
7. Zones and boats.
8. Luck modifiers with live odds.
9. World state: time of day, weather.
10. Rare-catch announcements; then season pass, crews, trading.

## Technical hot spots

- **Rolls on the server**: species, size, variant and luck are rolled server-side when the cast resolves. The client plays the minigame and reports a result that the server sanity-checks (minimum reel time, plausible input rate) `[lihfolk]`.
- **One table feeds roll and UI**: generate the "1 in X" text and the odds panel from the server table; recompute when a boost starts or ends.
- **Macro and AFK abuse**: fishing is the most automatable loop on the platform. Rate-limit casts, vary minigame parameters from a server seed, cap AFK yield and detect inhuman timing regularity.
- **Inventory size**: catches as `{speciesId, size, variant}` records with caps; auto-sell rules; watch the 4,194,304-character key limit `[official]`.
- **Water and boats on 20-player servers**: simple boats (few parts, bobbing animated on the client), fish as small models or UI art `[lihfolk]`. Water surfaces are Blender meshes with collision volumes for "in water" tests.
- **Announcements**: server-wide by remote; cross-server by `MessagingService` with throttling.
- **Trading**, if added, follows the atomic, logged, session-locked rules in `pet-collection-hatching.md`.

## The one-new-verb angle

- Change what is on the line: anomalies by night (vault gap), treasure, salvage, creatures you then raise.
- Change the catching: nets, harpoons, diving, co-op hauling of one huge catch.
- Simplify a deeper leader for younger players, as the 2025 follower did, only while the leader is weak; credit inspirations honestly and copy no art or names.

## Common failure modes

- A slot machine with no skill, or a skill wall with no luck.
- Long walks between dock and seller in the first session.
- An expansion that resets currency, weakens old gear and gates by a high level, all at once.
- Paid luck with no numeric explanation or live odds.
- Unlimited AFK income; the economy inflates and active play feels pointless.
- Stale event thumbnails and title tags after the event.
- Client-rolled catches; exploiters mint the rarest fish.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First catch inside 60 s with the rod pre-equipped | Auto-equip; shorten the first bite timer |
| 2 | The reel has a skill element and a forgiving floor | Add a bar or rhythm with a perfect bonus |
| 3 | Each zone has a finite checklist and a reward | Add per-zone bestiary goals |
| 4 | Odds shown as "1 in X" from the server table | Generate UI from the roll table |
| 5 | Paid luck states its numeric effect and updates odds live | Build the odds screen; add policy gate |
| 6 | Catch rolls and values are server-side; reel results sanity-checked | Move rolls; add timing checks |
| 7 | AFK yield is capped below active play | Add caps and diminishing returns |
| 8 | Some species depend on time, weather or season | Add world-state gates |
| 9 | Convenience passes remove walks, not challenges | Rework passes into "anywhere" perks |
| 10 | New zones keep old gear and currency meaningful | Redesign gates; add conversion |
| 11 | Rare catches are announced; crews or group events exist | Add announcements and a group event |
| 12 | Weekly update day with teaser and launch tags | Commit to a day; rotate tags |
| 13 | Inventory is capped and compact | Add caps, auto-sell, compact records |

## Review gate

- [ ] Skill layer and luck layer are both present and tuned for the target age.
- [ ] One server table drives rolls, "1 in X" text and the odds screen.
- [ ] Luck products, crates and rerolls meet the paid-random-item rules.
- [ ] AFK rules, macro limits and inventory caps are defined.
- [ ] Expansion plan adds without resetting.
- [ ] Rods, boats, docks, fish and water are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives, §Gap analysis (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `32 Case Studies of Top Roblox Games/Case Study - Fisch.md`, `59 Viral and Trend Game Teardowns/Teardown - Fish It.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud-services/data-stores/error-codes-and-limits.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
