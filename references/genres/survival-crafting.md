# Survival and crafting playbook

Covers co-op night-survival games, gather-craft-build survival, and round-based hazard survival. Open it when "prepare, then survive" is the loop, when planning base building and its save format, or when auditing a live survival game for horde performance and mid-game drop-off. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | A run-based design (survive N nights, then reset) for 1–4 players; one resource, one tool tier, five recipes; day/night with a creature at night; needs that slow but never kill; meta unlocks saved, nothing else | Persistent bases, PvP, raids, large worlds, trading, classes |
| Intermediate | Recipe DAG with an obvious next craft; grid-snapped building validated on the server; data-driven hordes; shared camp progress; revives; daily shop | Persistent shared worlds, offline protection |
| Expert | Per-player base blueprints packed into buffers with incremental saves; structural support graph; streaming for thousands of pieces; opt-in PvP with offline protection; weekly biome cadence | — |

Terms: *run-based* = each session is a complete arc that resets; *DAG* = a directed graph with no loops, here of recipes; *support graph* = which building pieces hold up which; *wipe* = a scheduled reset of a shared world.

## Snapshot

- Market position (vault, 2026-11-07): **durable**. 99 Nights in the Forest 221K CCU (launched Mar 2025; 11.2–14.2M peak in 2025; 2.17M tracked on 17 Oct 2026; "the most durable 2025 hit": weekly updates, friend co-op, an older audience), Survive Your Ideas 41K, co-op chase Evade 64K. Survival was the fastest-growing genre in the week of 28 Sep–4 Oct 2026 (+45.4%).
- Durable games share co-op or skill play, real depth and weekly updates (vault lifecycle model); survival fits all three.
- The 99 Nights team is small: three leads for design and art, programming, and building, per a Roblox creator spotlight; they describe building a feature, then scaling it "to the thousands" `[community]`.
- Audience: older than average, plays with friends, long sessions. Roblox's doc example for the genre is round-based hazard survival (Natural Disaster Survival) `[official]`.
- Rating: fear and violence levels set the label; night-horror framing can push to Moderate, which removes Kids and Select reach `[official]` `[VS]`.

## Core loop with timings

| Variant | Loop | Timing |
|---|---|---|
| Co-op night survival | Day: gather, craft, build up camp → night: defend → count the nights → new area | Day/night cycle 4–8 min; a session covers several nights `[house]` |
| Sandbox survival | Gather → craft tools → build base → explore for higher tiers → survive raids or weather | First tool in 60 s, first shelter in 5 min `[house]` |
| Round hazard | Lobby → hazard announced → survive → streak → repeat | Round 2–4 min; wait under 30 s |

- Needs (hunger, warmth, light) decay at graded rates with soft penalties first; death is the last step, not the first.
- Threat escalates on a visible clock; tool tiers gate resources; recipes form a DAG so there is always one obvious next craft.
- Loop lengths `[lihfolk]`: an action takes seconds; a trip 2–10 min (go out, gather, fight, return before night or before needs run out); a day cycle 8–20 min; the base is built over days to weeks.
- Pick two or three pressure systems, not all `[lihfolk]`: needs (force trips but become tedious if drain is fast), day and night (rhythm), other players (highest tension, most toxicity), decay (keeps the world clean but players hate losing builds offline). A casual co-op game for young players can use only day/night and creatures.

## First 5 minutes

1. 0:00 spawn beside a resource and a campfire or bench; one prompt: gather.
2. 0:30 first craft (a tool that visibly speeds gathering).
3. 2:00 first structure or camp upgrade placed with a ghost preview.
4. 3:30 first dusk warning; players regroup at the fire.
5. 5:00 first night survived with a clear "Night 1" stamp and a reward.
- Joining a server mid-night as a new player must be safe: spawn at camp with a short grace period.

## Progression and economy shape

- Tool and station tiers gate biomes; each tier adds a resource and a recipe set. Resource nodes respawn on timers.
- Camp or base level is shared progress in co-op; personal progress is class, recipes known and cosmetics.
- Classes or roles (vault: 99 Nights has a daily class shop with limited stock, a premium currency, and 99 R$ class re-rolls) give horizontal variety. A paid class re-roll is a paid random item: odds shown, `PolicyService` gate `[official]`.
- Crafting is atomic on the server: consume inputs and grant output in one step.
- Sinks: tool durability or upgrades, building materials, consumables (food, fuel), class unlocks, cosmetics.
- Long-term engine: night count records, new biomes weekly, badges, base persistence in sandbox variants.
- Loss: on death drop a recoverable bag or lose only carried consumables; never wipe persistent progress.
- Needs tuning `[lihfolk]`: one trip should use about half of a full bar, so players think about food once per trip, not every minute. Food variety matters (better food fills more or buffs), which gives farming and cooking a purpose.
- Persistence model is the first decision `[lihfolk]`: run-based (20–60 min arcs, meta unlocks only; easiest to ship and safest for retention), a persistent personal world, a persistent shared server world wiped on a schedule (complex and risky), or the common compromise of a base saved per player in a world that resets per server.
- Crafting time: instant for basics, 2–10 s timers for advanced items, never long real-time timers in a session game `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: Revive / second chance (capped per night or run), 2× gather speed, extra storage, Starter Pack (a fixed kit), currency packs, VIP (cosmetic plus convenience), gift passes, private servers (friend groups are the core audience).
- Add: cosmetic building themes, tool and campfire skins, emotes, a daily kit claim, class unlocks at a fixed price.
- Delete: permanent 2× Cash unless a cash economy exists; Auto-Collect; Luck unless loot rolls with odds shown.
- House rule 3: no pay-to-skip raids and no paid weapons or armour in PvP survival. In PvE co-op, paid convenience must not make the team's free players irrelevant.
- Rewarded video `[official]`: Second Chance (revive near the point of death), Pre-Round Power-Up (shield, speed or tool for one round), Streak Saver (keep a survival streak after dying), Daily Survival Kit (one consumable per 24 h). Rules: deterministic rewards, consumables only, daily cap. Benchmark opt-in 13%+, frequency 2.5+. Examples: Evade (Second Chance plus Streak Saver), Natural Disaster Survival (Pre-Round Power-Up).
- Offer timing: at camp, at dawn, on the death screen after the threat has passed. Never mid-attack.

## Retention and social hooks

- Friend co-op is the engine: shared camp, revives, role synergy, private servers. Intentional co-play feeds discovery.
- Daily shop with limited stock and a weekly update on a fixed day (vault norms for the genre leader).
- Records: nights survived per server and per friend group; badges at milestones.
- Streaks are part of the fantasy in round survival; soften them with a streak saver rather than a hard reset.

## UI patterns

- HUD: needs bars, day/night clock, hotbar, a compact objective line. Crafting opens at stations with the craftable items first and missing inputs highlighted.
- Build mode: ghost preview, snap grid, rotate, valid/invalid tint, one-tap confirm on mobile.
- Team panel: teammate health, downed markers with distance, ping wheel that works without chat.
- Inventory: stack counts, quick-transfer to chests, favourite lock.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §18 Crafting, §2 Inventory and equip, §13 NPC and enemy spawning and AI, §16 Plots, tycoon ownership and placement, §23 Time and day cycle, §10 Rounds, match state machine and intermission. Its "Build order by genre" table gives a second opinion.

1. Resource nodes and gathering with tool tiers.
2. Inventory and server-authoritative crafting.
3. Day/night cycle and threat schedule.
4. Creature AI and spawning (data-driven at scale).
5. Needs (hunger, warmth) with soft penalties.
6. Building: grid placement, validation, structure health.
7. Camp or base progression; storage.
8. Death, revive and recovery.
9. Player data: meta unlocks, classes, cosmetics; base blueprint if persistent.
10. Daily shop, records and badges; then PvP rules.

## Technical hot spots

- **Hordes**: enemies as server data with simple steering, rendered and animated on clients; no per-enemy Humanoid at scale; pathfinding recomputed on a timer and shared between enemies heading to the same target.
- **Building**: grid-snapped Blender pieces validated on the server (`GetPartBoundsInBox` overlap, support rules, distance from player, ownership zone). Structures save as `{id, grid position, rotation}`; quantise and pack into a `buffer` or compact string. A developer reports cutting a build from 14.6% to about 0.9% of the key limit by rounding and compressing `[community]`.
- **Storage limits** `[official]` `[VS]`: 4,194,304 characters per key; total storage 500 MB + 1 MB × lifetime users. Voxel-scale worlds and large bases need chunked keys and incremental saves (save changed chunks, not the world).
- **Resource nodes**: tagged Blender models with real collision; state (depleted until T) kept in a table, respawn by timestamp, not one thread per node.
- **Day/night**: `Lighting.ClockTime` driven from server time; clients tween locally. Night lighting must stay readable on a phone (see `horror-coop-escape.md` for light budgets).
- **Inventory and crafting**: server-authoritative; requests carry intent (`recipeId`, `count`), never results; rate-limit crafting and gather hits; validate gather distance and tool tier.
- **World size**: `StreamingEnabled`; per-server camps mean no cross-server state, but persistent bases need load-on-join and unload-on-leave.
- **Exploit surface**: item spawning through crafting remotes, gather-aura, teleport looting, duplication via drop-and-rejoin (session-locked profiles; ground items owned by the server).
- **Base data** `[lihfolk]`: each piece is type, position relative to the base origin, rotation, health, owner and contents. Grid-snap so positions store as small integers; a 2,000-piece base as full-precision JSON approaches key limits, a packed format does not. Document the axis convention in the module: mixed-up axes are a common save bug.
- **Scale** `[lihfolk]`: eight players with 1,500 pieces each is 12,000 models. Anchor everything, use simple meshes, turn off `CanTouch` and `CanQuery` where unused, and stream distant bases.
- **Structural support**: require pieces to connect to a foundation; compute support as a graph walk from foundations when pieces are added or destroyed, and cache it `[lihfolk]`.
- **Raids on player-built shapes**: pathfinding into bases is expensive; many games let creatures attack the nearest wall piece instead `[lihfolk]`.
- **PvP and griefing** `[lihfolk]`: raiding offline bases is the most-complained-about mechanic in the genre. Use opt-in PvP (zones, flags or separate servers), offline protection, build permissions per plot, chest locks and team access.

## The one-new-verb angle

- The genre leader puts the goal in its title (survive 99 nights). Find a verb that sits on top of prepare-and-survive: tame, cook for the camp, move the base (a vehicle camp), survive what players themselves invented.
- Unclaimed pairing in the vault: fishing × anomaly horror (fish by day, deal with what is on the line at night).
- Seasonal lead: Christmas × survival showed only games under 300 CCU on 7 Nov 2026 (vault).

## Common failure modes

- Needs that punish instantly; new players die of hunger before learning to craft.
- A recipe list with no obvious next craft.
- Solo-hostile balance, or co-op where one player's purchase trivialises the night.
- Server-side Humanoid hordes; ping climbs each night until the server stalls.
- Saving bases as instance dumps; hitting key limits and save throttles.
- Losing persistent progress on death.
- Night scenes too dark for phones.
- Too many pressure systems at once; offline raiding; free placement with no grid (hard to validate, overlap exploits) `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First craft inside 60 s; first night survived by nearly all new players | Move resources to spawn; soften night 1 |
| 2 | The next craft is always obvious | Reorder recipes into a DAG; highlight the next goal |
| 3 | Needs decay has soft penalties before death | Add slow, blur or reduced regen stages |
| 4 | Server frame time holds on the worst night with a full server | Data-driven enemies; shared pathing |
| 5 | Build placement is server-validated | Add overlap, support, range and zone checks |
| 6 | Saves are incremental and compact | Chunk keys; pack structures; save deltas |
| 7 | Death never wipes persistent progress | Recoverable bag or consumable-only loss |
| 8 | Works for 2–4 friends with private servers and mid-session join | Add grace spawn at camp; party teleport |
| 9 | Revive offers are post-threat, capped, with a free alternative | Move and cap offers; add team revive |
| 10 | Any class or loot roll for Robux shows odds and respects policy | Add odds panel and gate, or fixed-price unlocks |
| 11 | Night is readable on a 3 GB phone | Raise ambient floor; cut shadowed lights |
| 12 | Daily shop and weekly update exist | Add the rotation and a fixed day |
| 13 | Night records and badges exist | Add server and personal records |
| 14 | Persistence model is deliberate; run-based unless a persistent base is the product | Simplify to runs with meta unlocks, or build the blueprint save properly |
| 15 | One trip uses about half a needs bar | Retune drain |
| 16 | PvP is opt-in with offline protection | Add zones or flags and protection |

## Review gate

- [ ] Prepare and survive phases are both fun alone and better with friends.
- [ ] Recipes, tiers and threat curve are drawn as graphs before building.
- [ ] Crafting, inventory, building and gathering are server-authoritative.
- [ ] Horde and save designs meet the frame and storage budgets.
- [ ] Monetisation is revive, convenience and cosmetics; no paid combat power in PvP.
- [ ] Nodes, tools, structures and enemies are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Shared DNA, §Trend lifecycle (read; 2026-11-07 snapshot); `references/knowledge-base.md` §3.2 (vault note on the survival growth week).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/survival.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud-services/data-stores/error-codes-and-limits.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://devforum.roblox.com/t/creator-spotlight-the-story-behind-99-nights-in-the-forest/4036940 (search summary)
- https://devforum.roblox.com/t/datastores-access-and-storage-updates/3597255 (search summary)
- https://devforum.roblox.com/t/saving-thousands-of-parts-to-datastores/938866 (search summary)
- https://devforum.roblox.com/t/data-store-size-limit-question/4026178 (search summary)
- https://github.com/Zyn-ic/Stoway (read README; 13 stars, MIT; inventory and hotbar system; reference only)
- GitHub search for open survival frameworks (2026-11-10): only small personal projects without licences found.
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Survival and Crafting.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
