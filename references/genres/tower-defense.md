# Tower defence playbook

Covers wave-based tower defence: classic path TD, anime unit TD with summons and traits, and co-op lobby-to-match structures. Open it when placing and upgrading units against waves is the core action, when designing a summon economy that passes policy, or when auditing a live TD for enemy-count lag and bandwidth. Market numbers are the vault's 2026-11-07 snapshot `[VS]`.

## Snapshot

- Market position (vault, 2026-11-07): **rising, led by anime TD**. Anime Adventures 99K CCU, Cameraman Tower Defense 46K. Anime incrementals and tower defence form an active wave. Theme hybrids are small so far: Garden TD 6.8K, Brainrot TD 932.
- Gap (vault): steal × tower defence ("raid other players' bases for towers, then defend with them") scored 27/35 with an 8–12 week MVP; a partial gap.
- Money: one anime TD was reported as the platform's top earner within 10 days of release `[community]`. The summon-and-trait layer is the revenue engine and the compliance risk.
- Audience: older and grind-tolerant; co-op groups; long sessions made of several matches. Macro tools for leading TD games are widespread on GitHub, a sign of how much repetition players will automate.
- Official UI reference: Tower Defense Simulator separates Daily Tower Skins from Daily Crates in its shop `[official]`.

## Core loop with timings

| Phase | What happens | Target `[house]` |
|---|---|---|
| Lobby | Pick a loadout of 4–6 units, a map and a difficulty; party up | Under 60 s from lobby to match start |
| Prepare | Place and upgrade with starting cash | First tower placed within 15 s |
| Wave | Enemies walk the path; towers fire; leaks cost lives | Wave 20–45 s early, longer later |
| Earn | Kill bounty plus end-of-wave income; bonus for calling the next wave early | A meaningful purchase every wave |
| Result | Win or lose → XP, currency, drops → back to lobby | Match 8–20 min; shorter for story stage 1 |
| Meta | Summon or unlock units, level them, roll traits, harder maps | One new unit or upgrade per 2–3 matches early |

- Telegraph the next wave (icons and counts). Enemy variety (fast, armoured, flying, swarm, boss) is what forces tower variety.
- Solo play needs 2× and 3× speed controls; waiting is the genre's dead time.

## First 5 minutes

1. 0:00 skip the lobby for a first-time player: drop straight into a short tutorial map with three starter units.
2. 0:15 first placement on a highlighted spot; 0:30 first kill.
3. 1:30 first upgrade with a visible range and damage change.
4. 3:00 a new enemy type that the first tower handles badly, and the unit that answers it.
5. 5:00 victory screen with a free summon or guaranteed unit, then the lobby.
- The first free summon must return something useful; show its odds panel so the system is understood before any currency is at stake.

## Progression and economy shape

- In-match economy: enemy HP grows 1.1–1.2× per wave while income grows roughly linearly; wave rewards must scale with the next tower tier's cost. Selling refunds about 70%. Leaks cost lives and forfeit bounty.
- Tower value = DPS × time in range. Targeting modes: first, last, closest, strongest, weakest. Balance on cost efficiency per role (single-target, splash, slow, support, economy).
- Meta economy: units by rarity; unit levels; traits or enchants; evolution materials from specific maps; story → challenge → raid → endless.
- Summons (fan-guide figures for one leading anime TD `[community]`): 50 gems for one summon and 500 for ten; top traits at 0.1–0.5% per reroll; a hard pity of 1,500 rerolls on a 0.1% trait; large free reroll grants at anniversaries. Treat as the shape of the market, not targets.
- House defaults: banner pity within reach of a committed free player in one banner period; pity counters visible; earned gems from every mode; duplicate units convert to upgrade material.
- Sinks: unit levels, trait rerolls, evolutions, cosmetics, extra loadout slots.

## Monetisation set that fits

- Keep from the default set: 2× Cash as a timed in-match or reward boost, 2× EXP (unit and account XP), Starter Pack with a fixed disclosed unit, currency packs (gems), extra slots (unit storage, loadouts, team presets), VIP, gift passes, private servers, Luck 2× and Server Luck on summons.
- Add: 2× and 3× game speed for solo (convenience), tower skins, auto-skip waves, a season pass with real fixed end dates, unique towers as passes only if balanced against free ones.
- Delete: Revive (replace with a capped "continue from wave N" in PvE), Auto-Collect.
- Policy `[official]` `[VS]`: summons, crates and trait rerolls bought with Robux or with currency purchasable with Robux are paid random items. Show every outcome and numeric odds before purchase, update odds live under luck boosts, gate with `PolicyService` (`ArePaidRandomItemsRestricted`, and `IsPaidItemTradingAllowed` if units trade). Fallback for restricted players: direct purchase at expected value or earn-only banners.
- House rule 3: banners rotate on real dates and do not restart; no "last chance" unit that returns next week; no paid unit power in PvP or leaderboard modes.
- Offers only between waves or on the result screen, never mid-wave.

## Retention and social hooks

- Co-op is intentional co-play: party queue, private servers, shared victories, carry bonuses for helping a lower-level friend.
- Rotating challenges and banners on fixed timers; weekly unit or map on a fixed day.
- Endless-mode and speedrun leaderboards with a paid-power-free rule set.
- Unit index and trait collection; trading only with the dupe protections in `pet-collection-hatching.md`.

## UI patterns

- Hotbar of loadout units with cost; tap unit then tap ground to place; range ring preview; upgrade panel on select with the stat delta and sell value.
- Wave bar: number, timer, next-wave preview, skip or call-early button, speed toggle.
- Summon screen: banner art, a labelled Odds button, pity counter, single and ten-pull, skip animation.
- Mobile: placement uses a confirm step to avoid mis-taps; camera pan and zoom gestures do not conflict with placement.

## Technical hot spots

- **Enemies are data, not characters.** DevForum consensus `[community]`: do not give enemies Humanoids. Simulate each enemy on the server as path distance, HP and speed; replicate compact state; render pooled Blender models on clients, interpolating along the waypoint path with `AnimationController` rigs.
- **Bandwidth is the second wall.** Do not replicate per-enemy CFrames every frame. Send spawn events (id, type, spawn time, path) and corrections on speed changes; clients derive position from time. Batch damage and death events per tick in a buffer.
- **Targeting**: plain distance checks on the data list, or a spatial grid along the path; precompute which path segments fall inside each tower's range at placement. Run tower logic on one shared server loop at a fixed tick (10–20 Hz) `[house]`.
- **Movement accuracy**: carry leftover distance past waypoints; humanoid `MoveTo` drifts on sharp turns `[community]`.
- **Placement validation on the server**: unit owned and in loadout, cash, placement zone, spacing, cap per player. In maze TD run a BFS before accepting a placement so the path is never blocked.
- **Match servers**: lobby place teleports parties to reserved servers; pass loadout and party in teleport data and re-validate against saved inventory on arrival.
- **Summon integrity**: rolls and pity on the server from the same table the odds panel shows; session-locked profiles; rate-limit multi-pulls.
- **Automation**: macros replay inputs; rate limits and server-side match pacing matter more than detection. Decide whether AFK farming is allowed and design rewards around the answer.
- **VFX**: hundreds of projectiles; pool tracers and impact effects, cap by distance and by count per frame.

## The one-new-verb angle

- Change where towers come from: steal them from other bases (the vault's partial gap), grow them, merge them.
- Change the defender's role: a player character who fights on the lane beside the towers.
- A new theme on the same summon wall lands in the under-1K tail (Brainrot TD 932).

## Common failure modes

- Humanoid enemies; server frame time collapses past a few hundred.
- Per-frame enemy replication; clients on mobile data rubber-band.
- Income outpacing HP growth (trivial late waves) or the reverse (unwinnable without one unit).
- A single dominant unit behind a paid banner.
- Undisclosed or inaccurate odds; missing policy gate on indirect purchases.
- Long unskippable lobbies and no speed control in solo.
- Offers mid-wave.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First-time players skip the lobby into a tutorial map | Add a first-join teleport and three starter units |
| 2 | Enemies have no Humanoids; clients render them | Move to data simulation plus pooled client models |
| 3 | Receive bandwidth stays flat as enemy count rises | Replicate spawn and correction events, not transforms |
| 4 | Tower logic runs in one fixed-tick loop | Merge per-tower loops; precompute path coverage |
| 5 | Placement is server-validated | Add ownership, cash, zone and spacing checks |
| 6 | Each wave offers a meaningful purchase | Refit bounty and income to tower costs |
| 7 | Every enemy type has at least two unit answers, one free | Add or rebalance units |
| 8 | Odds panel, live boosted odds and pity counter exist | Build from the server table |
| 9 | Policy flags are enforced with a fallback path | Add gate and direct-sale or earn-only option |
| 10 | Solo has 2× / 3× speed | Add speed control |
| 11 | Party queue and private servers work end to end | Fix teleport data and re-validation |
| 12 | Banners have real end dates and do not restart | Publish dates; remove resets |
| 13 | Leaderboard modes exclude paid power | Add a normalised rule set |
| 14 | Holds frame rate on a 3 GB phone at peak wave | Pool and cap VFX; reduce distant enemy detail |

## Review gate

- [ ] Wave HP, income and tower cost curves are modelled together.
- [ ] Enemy simulation is data on the server; clients render and interpolate.
- [ ] Network design sends events, not per-frame transforms.
- [ ] Summon economy has disclosed odds, visible pity and a restricted-player fallback.
- [ ] Offers sit between waves or on results; no paid power in competitive modes.
- [ ] Towers, enemies, maps and projectiles are Blender models; maps have real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Gap analysis (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://devforum.roblox.com/t/an-in-depth-guide-to-a-tower-defense-game-part-1/3019857 (search summary)
- https://devforum.roblox.com/t/tower-defense-enemy-system/2667346 (search summary)
- https://devforum.roblox.com/t/how-can-i-create-a-tower-defense-entity-system-that-is-optimized/2128775 (search summary)
- https://devforum.roblox.com/t/how-do-i-lower-my-recv-td-game-enemy-system/2772669 (search summary)
- https://devforum.roblox.com/t/humanoidenemy-optimisation/4804990 (search summary)
- https://github.com/0jewell/td-kit (read README; 4 stars, MIT; pathway, traveller and range-intersection utilities; reference only)
- https://beebom.com/anime-vanguards-surpasses-blox-fruits-top-earning-roblox-game/amp/ (search summary)
- https://deltiasgaming.com/?p=349658 and https://progameguides.com/roblox/anime-vanguards-traits-tier-list-all-traits-ranked/ (search summary; fan guides for summon cost, trait rates and pity)
- GitHub search "roblox tower defense" (2026-11-10): top results are macro and automation tools for existing games (not used).
