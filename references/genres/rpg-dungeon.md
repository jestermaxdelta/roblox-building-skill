# RPG, dungeon and roguelite playbook

Covers open-world and anime RPGs (quest, fight, loot, level), instanced dungeon crawlers and run-based roguelites. Open it when stats, gear and enemies drive progression, when sizing a content plan a small team can sustain, or when auditing a live RPG for mob performance, inventory bloat or pay-to-win drift. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One zone, three enemy types, one weapon line; server-side damage with a simple formula; XP and levels; a starter drop inside 30 s; one mini-boss with a recommended-power sign; compact inventory save | Classes, skill trees, open world, trading, guilds, procedural dungeons |
| Intermediate | Data-driven mobs rendered on clients; quests as state machines; zone scaling sheet (health, coins, time per zone); open boss arenas that reset; party credit; instanced dungeons in reserved servers | Raids, seasonal content |
| Expert | ECS-style mob simulation with tick budgets; build depth with readable trade-offs and cheap respec; boss phases; economy sinks and trade tax; funnel telemetry at every boss; live balance by pick and clear rates | — |

Terms: *mob* = a non-player enemy; *elite* = a stronger variant with extra drops; *respec* = resetting spent skill points; *instanced dungeon* = a private copy of a dungeon for one party; *gear score* = a single number summarising equipment power.

## Snapshot

- Market position (vault, 2026-11-07): **evergreen at the top, expensive to enter**. Blox Fruits 325K CCU (one of the 2014–2020 evergreens; Fourth Sea due December), Attack on Titan Revolution 50K, King Legacy 40K. Roguelike Dead Rails about 29K from a 79K tracked peak ("roguelike variety, now niche").
- Evergreens swing 2–5× on events and updates (vault lifecycle model). Anime incrementals and tower defence are the rising anime formats; anime RPGs are the incumbents.
- Third-party trackers list "open world action" among categories with search demand and thin competition `[community]`; treat as a lead, not data.
- Audience: older than the platform average (16+ invest more time and money and form communities); long sessions; guilds and trading communities.
- Cost: the most content-hungry genre. Every zone, enemy, weapon and armour set is a Blender asset, so scope is the first design decision.
- Rating: violence and blood levels set the maturity label; decide the target before art starts `[official]` `[VS]`.

## Core loop with timings

| Layer | RPG | Dungeon / roguelite | Timing |
|---|---|---|---|
| Seconds | Attack, dodge, ability | Same | Hit feedback under 100 ms on the client |
| Minutes | Quest: kill or fetch → turn in → XP and loot | Room → fight → loot → next room | Quest 2–5 min early; room 30–90 s `[house]` |
| Session | Level up, new gear, new zone | Run: floors → boss → rewards → meta upgrades | Run 10–20 min so a discovery player can finish one |
| Weeks | Raid, world boss, season | New biome, class, modifier | Weekly or fortnightly drop |

- Roblox's three-layer test `[official]`: exploring (interaction) → fighting (repeated cycle) → upgrades and collections (progression engine). Each layer must feed the next.
- Real-time action fits Roblox sessions better than turn-based.
- Time-to-kill bands at the zone's expected power `[lihfolk]`: a regular enemy takes 2–5 hits (about 3 for a zone-1 regular under a starter weapon); an elite 10–20 s; a mini-boss 20–40 s; a region or world boss 1–3 min. One shipped project used about 25× regular health for mini-bosses and about 150× for world bosses, and aimed for 8–12 min per zone.

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; this genre's row is in its §10. No offer or social card in this window (offer gate).

1. 0:00 spawn with a weapon equipped facing the first enemy; movement and attack prompts only.
2. 0:30 first kill, first loot drop that is visibly better than the starter.
3. 1:30 first quest giver; quest tracker pins one objective.
4. 3:00 level 2–3 with one stat or skill choice.
5. 5:00 first ability unlocked and a mini-boss or dungeon door in sight.
- No class or build screen before the first fight; defer choices until the player has context.
- Tutorial enemies have reduced health and damage and target only their own player; nothing else pulls aggro onto someone mid-tutorial `[lihfolk]`.

## Progression and economy shape

- Levels: model time per level first, then `req(L) = t(L) × xpPerMin(L)`; polynomial `base × L^p` with p 1.5–2.5.
- Stats in layers: base → flat → percent → clamp. Never store derived stats; recompute on change (dirty flag).
- Damage: ratio formula `attack × K / (K + defense)` with K about 100 degrades smoothly; ±10% variance; 1.5× crit.
- Loot: rarity tiers with server-side rolls; bad-luck protection on boss drops; gear score bands per zone so numbers stay readable.
- Random abilities (fruits, races, clans) are the anime-RPG collection layer. Rerolls paid for in Robux, or in a currency bought with Robux, count as paid random items: full odds, live boosted odds, `PolicyService` gate `[official]`.
- Roguelite: keep run state and profile state strictly apart; meta-progression widens options more than it raises power.
- Sinks: repair or upgrade costs, crafting, rerolls, respec, fast travel, cosmetics, bank slots. Trading needs a tax or bind-on-equip to control inflation.
- Quests are state machines (available, active, complete, turned in) fed by an event bus; dialogue is a data graph with string ids.
- Zone scaling from one project's plan `[lihfolk]`: enemy health about +55% per zone and coins per kill about ×1.6 per zone, so players slowly outscale by upgrading. Two regular enemy types plus one mini-boss per zone and one boss per world; introducing an enemy in each zone holds off the treadmill feeling. Variants (+15% size, +30% health, +15% damage, a tint and one trait) and elites (about 1 in 8 spawns later, ×2.5 health, an extra drop roll) stretch each mesh.
- **Bosses are the best moments and the biggest retention risk.** One project's onboarding funnel lost 82% of players at its first boss step `[lihfolk]`. Its fixes: open arenas without locked doors (leave, and after 20 s empty the fight resets), short telegraphed fights, a Recommended Power number on every boss gate, walls that take one upgrade or one better weapon to pass, and bosses that can be refought for drops.
- Build depth comes from choices with readable trade-offs ("+30% damage, −20% health" beats a paragraph); let players respec cheaply, since young players experiment `[lihfolk]`.
- Boss drops: guaranteed materials plus a chance at something rare; a first-clear bonus `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: 2× EXP 10/30 min, 2× Cash (gold), Starter Pack, extra storage (inventory, bank), VIP, gift passes, private servers (very common for grinding with friends), currency packs with care, Revive in dungeons and roguelites (capped per run, offered after the fight).
- Add: cosmetic armour and weapon skins, mounts, fast travel, respec tokens, a season pass with a real fixed end date, extra character slots.
- Luck only where drops roll, with odds shown; Server Luck for world-boss events.
- Delete: Auto-Collect and 2× Speed unless gathering exists.
- House rule 3: never sell the best gear, stat points or ability rerolls that decide PvP. Where PvP exists, normalise paid boosts out of it or keep PvP cosmetic-only.
- Rewarded video `[official]` ("a micro-transaction paid for with time"): bypass a crafting cooldown, Second Wind revive at a checkpoint, 10-minute Luck Potion, 2× EXP. Guardrails: daily cap, deterministic rewards only, account-bound rewards (tradable ad rewards invite alt farming). Benchmark opt-in 15%+, frequency 3+.

## Retention and social hooks

- Party play with shared quest credit and a party XP bonus; guilds; world bosses on a timer (every 30 min `[house]`) that pull the server together.
- Daily and weekly quests as cumulative tracks, no streak loss.
- Fixed-day content drops; the evergreens set records on update days (vault). Communicate a roadmap.
- Trading and a visible gear identity (transmog) are long-term status loops.

## UI patterns

Genre specifics only. Zone layout for this archetype and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre). Effects to build first, from `vfx-recipes.md`: hit spark, melee slash, projectile, AoE telegraph, heal, level-up.

- HUD: health and resource, hotbar with cooldown sweeps, pinned quest, minimal damage numbers (pooled, capped).
- Inventory: grid with rarity frames, compare-on-select, bulk sell, lock toggle. On phones, one-tap equip-best.
- Ability buttons arranged in the right-thumb arc; target assist or soft lock for touch.
- Dialogue: short lines, skip always available, `LocalizationTable` string ids.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §12 Combat, §13 NPC and enemy spawning and AI, §2 Inventory and equip, §6 Quests and achievements, §18 Crafting, §11 Teams, matchmaking, queues and reserved servers, §14 Tools and abilities. Its "Build order by genre" table gives a second opinion.

1. Combat core: attack input, server validation, damage formula, health.
2. Enemy spawners and mob AI (data on the server, visuals on clients).
3. XP, levels and stats (layered, never stored derived).
4. Loot tables, drops and inventory with compact saves.
5. Equipment and upgrades.
6. Quests (state machine) and dialogue (data graph).
7. Zones, gates and fast travel.
8. Bosses with telegraphs, phases and recommended power.
9. Party system and shared credit.
10. Dungeons in reserved servers; then skills, crafting, trading.

## Technical hot spots

- **Mobs are the frame budget.** Do not give every enemy a server-side Humanoid with per-frame logic. One open reference runs about 150 server-driven mobs at roughly 80 KB/s client intake by ticking AI at 8 Hz and movement at 20 Hz on the server, replicating only invisible hitbox CFrames, and rendering and interpolating models on the client at 60 Hz (author's measurements) `[community]`.
- **Combat authority**: client plays the swing instantly; the server validates cooldown, range and line of sight from its own positions and applies damage. The client never reports damage. See `fighting-battlegrounds.md` for hitbox trade-offs.
- **Inventory data**: store items as compact records (`id`, rolls, level); stack materials; cap bag size. Large inventories approach the 4,194,304-character key limit and slow every save `[official]` `[VS]`.
- **Loot and XP on the server**, displayed via attributes or a state remote; drop tables for unreleased content stay in `ServerStorage`.
- **World size**: `StreamingEnabled`, zones as separate places when the map outgrows memory, instanced dungeons in reserved servers with party data passed and re-validated on arrival.
- **Procedural dungeons**: rooms from a Blender kit snapped by `Attachment`s; one server `Random` per run; every floor passes a connectivity check; party members share seed and state.
- **Exploit surface**: kill-aura and teleport farming (validate attacker distance and attack rate), quest-complete remotes (the server tracks objectives itself), item duplication through trade or drop-and-rejoin (session-locked profiles, atomic transfers).
- `CollectionService` tags for quest givers and spawners; `ProximityPrompt` on an invisible anchor inside the Blender model.

## The one-new-verb angle

- One combat or traversal verb that reads in a clip: a grapple, a transformation, a mount that fights.
- Or change the frame: a roguelite on a moving vehicle (Dead Rails), a co-op dungeon built for exactly two friends.
- Avoid competing with evergreens on content volume; win on a tight 10–20 minute run or one deep system.

## Common failure modes

- Scope: a map and class list no small team can finish in Blender; launch slips for a year.
- Empty mid-game: level 15–30 has no new verbs, only bigger numbers; D7 collapses.
- Humanoid armies on the server; server frame time and ping spike at 30 players.
- Client-reported damage or quest completion.
- Selling power where PvP matters; rating and community turn.
- Unbounded inventories and derived stats saved to data.
- Tutorials and build screens before the first fight.
- A boss that blocks progress with a locked arena and no stated power target; the single largest funnel cliff reported for the genre `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First kill inside 30 s, first upgrade inside 90 s | Move the first enemy to spawn; guarantee a starter drop |
| 2 | Every 5 levels adds a verb (ability, enemy behaviour, traversal) | Add abilities or enemy types before more zones |
| 3 | Time-per-level curve is modelled and matches telemetry | Refit the XP table from logged minutes per level |
| 4 | Server frame time holds with a full server in the busiest zone | Move to data-driven mobs with client rendering |
| 5 | Damage, loot, XP and quest progress are server-computed | Remove client authority from remotes |
| 6 | Inventory records are compact and capped | Migrate to id-based records; add stacking |
| 7 | Party play gives shared credit and a bonus | Add party quest credit and XP bonus |
| 8 | A run or session goal fits 10–20 min | Add short dungeons or bounties |
| 9 | Paid boosts are excluded or normalised in PvP | Add PvP normalisation |
| 10 | Any paid reroll shows odds and respects policy flags | Add odds panel and gate |
| 11 | World boss or server event every 30 min | Add a timed event |
| 12 | Trading or drops cannot duplicate items | Atomic, logged transfers; session locking |
| 13 | Update cadence and roadmap are public | Commit to a fixed day |
| 14 | Funnel shows no cliff at the first boss; arena is open and resets | Add recommended power; shorten the fight; unlock the doors |
| 15 | Each zone takes about 8–12 min and adds an enemy type | Retune health and coin scaling per zone |

## Review gate

- [ ] Scope fits the Blender pipeline: asset list counted and scheduled before code.
- [ ] XP, damage and loot formulas are written, modelled and server-side.
- [ ] Mobs are data-driven with client rendering; tick rates stated.
- [ ] Run state and profile state are separate; dungeons use reserved servers.
- [ ] No power sold where PvP exists; random purchases disclose odds.
- [ ] Every enemy, weapon, armour piece and prop is a Blender model with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/rpg.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud-services/data-stores/error-codes-and-limits.md (read)
- https://github.com/ItipatS/RPGJECS (read README; 14 stars, no licence; ECS mob AI and replication demo with tick rates; reference only)
- https://github.com/Ukendio/jecs (search listing; 484 stars, MIT; Luau ECS)
- https://github.com/prooheckcp/RoQuest (read README; 20 stars; quest-system library, licence listed as Apache-2.0 by GitHub and MIT in the README; reference only)
- https://github.com/EgoMooseOldProjects/Dungeon-generator (search listing; 19 stars, MIT, 2016)
- https://devforum.roblox.com/t/script-planning-questions-for-performance/2815331 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/devas-of-creations-npc-replication-idea-smoothness/3151754 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://rowatcher.com/news/roblox-genre-opportunity-map-2026-where-smart-developers-are-building-next (search summary; third-party)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Combat and RPG.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
