# Physics sandbox and ragdoll playbook

Covers physics toys and playgrounds: grab-and-fling sandboxes, ragdoll engines, launch and destruction toys, and their progression hybrids. Open it when one physical verb applied to props and other players is the whole game, when deciding who simulates what, or when auditing a live sandbox for fling abuse, part-count lag and a low approval rating. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One verb (grab, launch or ragdoll) that works on props within 5 s of spawning; server-checked distance; clamped velocities; a per-player prop cap | Grabbing other players, houses, progression, saves |
| Intermediate | Grabbing players with an escape mechanic; safe zones and a no-grab toggle; ragdoll and recovery; auto-cleanup; built-in mini-games (targets, distance boards) | Progression layer, cross-server boards |
| Expert | A progression hybrid (launch distance pays, upgrades, rebirth); server authority mode for shared physics; fling-exploit telemetry; physics budgets held at 25 players | — |

Terms: *network ownership* = which machine simulates an unanchored assembly; *fling* = an extreme velocity imparted by physics abuse; *ragdoll* = a character driven by physics joints instead of animation.

## Snapshot

- Market position (vault, 2026-11-07): **a forming wave with a gap in progression**. Fling Things and People 45K CCU; Ragdoll Physics 28K, Ragdoll Reality 25K, Ragdoll Research 24K, Ragdoll Sandbox 22K; five new ragdoll games entered the top 100 in October 2026. All are sandbox-only. Every progression hybrid is under about 2K (Broken Bones IV 2K, +1 Launch to Break Bones 5).
- The vault's shelved concept: a ragdoll launch incremental (power grows per second, launch your ragdoll, distance pays) scored 30/35 with a 2–4 week MVP and a 1–4 month expected lifespan.
- LihFolk's teardown of the grab-and-fling leader `[lihfolk]` `[VS]`: 25-player servers, about 80% positive (lower than calmer games: being grabbed against your will is both the comedy and the friction), dashboard genre Simulation › Physics Sim, a one-sentence store description.
- Why it lasts `[lihfolk]`: a toy, not a task (nothing to finish and leave); players are the content; clip-ready physics.
- Roblox's own reference game for co-op physics on server authority is Boneheads `[official]`.
- Audience: young, friend groups, clip-driven.

## Core loop with timings

| Step | What happens | Target |
|---|---|---|
| Arrive | Spawn among props and players | First grab or launch inside 5 s |
| Use the verb | Lift on a visible line, release to throw; or launch; or ragdoll | Response under 100 ms on the acting client |
| Be acted on | Someone grabs you; you learn escape by needing it `[lihfolk]` | Escape in 1–3 s `[house]` |
| Invent | Tag, launch contests, towers to knock down | Emergent; minutes |
| Retreat | House or safe zone | Any time |

- Within a minute a new player has flung, been flung and laughed `[lihfolk]`.
- Progression hybrid loop (vault gap): power per second → launch → distance pays → upgrades → rebirth. See `plus-one-evolution.md` and `simulator-incremental.md` for the economy.

## First 5 minutes

1. 0:00 spawn beside small throwable props; the verb is on the primary button.
2. 0:05 first throw with a trail and impact sound.
3. 0:30 first interaction with another player; a one-line hint shows the escape input.
4. 2:00 a signposted toy: target range, launch ramp, tower of crates.
5. 5:00 first coins spent on a toy; the safe zone or house is discovered.

## Progression and economy shape

- Pure sandbox: coins for toys and house items; per-player toy limits; houses that save. Light by design.
- Hybrid: the measured result of the verb (distance, damage, height) is the stat that pays. Keep the physical action as the source of income, not a menu.
- The physics stats that matter between players are reach and escape `[lihfolk]`; treat them as PvP stats (see monetisation).
- Sinks: toys, house items, cosmetics for the grab line, ragdoll effects.
- Built-in mini-games with boards (longest throw, highest launch) give goals to players who want them.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic), gift passes, private servers (friend chaos), Starter Pack of toys, 2× Cash if coins exist, extra slots (toys, house saves).
- Good products raise limits that cost server resources the game budgets anyway: toy cap, house saves, house time `[lihfolk]`. Observed prices in the leader `[lihfolk]` `[VS]`: limit and coin passes 100–400 R$, a cosmetic line pass 95.
- Add: line colours, trails, ragdoll effects, toy packs.
- Delete: Luck, Revive, Auto-Collect, 2× EXP.
- **Conflict (market vs house rule 3):** the leader sells farther reach (460 R$) and faster escape (240 R$), which affect player-versus-player interaction `[lihfolk]`. Do not sell reach, grab strength or escape speed; make them earnable or flat.
- In a launch hybrid, paid multipliers are acceptable only on solo distance, never on shared leaderboards without a separate clean board.

## Retention and social hooks

- Emergent play needs props that combine: ramps, cannons, balloons, glue.
- Houses give a calm personal space inside the chaos `[lihfolk]`.
- Friends turn the toy into a party game; private servers matter.
- Small regular updates (one new toy a week) add return reasons to an already strong toy.

## UI patterns

- Almost none: a crosshair or reticle, a visible grab line (`Beam`), an escape prompt, a toy menu.
- Consent controls in settings and in the world: a no-grab toggle inside safe zones, short immunity after being thrown `[lihfolk]`.
- Distance or score pop-ups on mini-game boards.

## Systems to build, in order

System names refer to `references/gameplay-systems-cookbook.md`; constraints and ownership are in `references/physics-and-vehicles.md`.

1. Grab beam: raycast target, attachment, constraint, visible line.
2. Throw and velocity clamp.
3. Prop spawner with per-player caps and auto-cleanup.
4. Ragdoll toggle and recovery.
5. Grabbing players with server validation; escape mechanic.
6. Safe zones and consent toggle.
7. Coins, toy shop and player data.
8. Houses with compact saves.
9. Mini-game boards; then the progression layer.

## Technical hot spots

- **Who simulates what.** Grabbing a prop: give the grabber network ownership for responsiveness, validate distance and rate on the server, return ownership on release. Grabbing a player means moving a character you do not own: use temporary ownership or server-applied forces, with server distance and rate checks either way `[lihfolk]`.
- **Clamp velocities on the server.** Fling exploits are a platform-wide problem; clamp linear and angular velocity, reset anything that leaves the map `[lihfolk]`.
- **Part budget**: 25 players × unlimited props stalls physics. Per-player prop caps, cleanup of abandoned items, sleeping assemblies, simple collision shapes.
- **Server authority model** `[official]` `[VS]`: Roblox's Boneheads reference keeps physics, collisions and shared mechanisms consistent for every player while clients predict input; evaluate it for new sandboxes.
- **Ragdolls** sell the comedy: constraint-based joints, a recovery timer, no Humanoid state fights; keep ragdoll counts bounded.
- **Houses**: saved as `{id, position, rotation}` lists with caps.
- **Exploit surface**: grabs from across the map (server range checks), spawn spam (rate limits), flinging through client-owned assemblies (ownership discipline, clamps).
- Props and toys are Blender models with simple, deliberate collision; a readable silhouette matters more than detail.

## The one-new-verb angle

- Add a goal to the toy: distance pays (the vault's open gap), build-and-destroy rounds, co-op puzzles with thrown objects.
- Change the verb: magnetise, inflate, stretch, glue.
- A sixth plain ragdoll playground joins five at 21–28K with nothing to tell them apart.

## Common failure modes

- Unclamped velocities; players flung into the void repeatedly.
- No prop limits; server physics lag.
- Grabs validated only on the client.
- No escape, safe zone or consent control; frustrated quits and a falling rating.
- Selling reach or escape.
- A progression layer that replaces the physical verb with menus.
- No updates; the toy never gains new combinations.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Verb usable within 5 s of spawn | Put props at spawn; bind the primary button |
| 2 | Server validates grab distance and rate | Add checks |
| 3 | Linear and angular velocity clamped; out-of-map reset | Add clamps and a reset volume |
| 4 | Per-player prop cap and abandoned-item cleanup | Add budgets |
| 5 | Server physics time holds with a full server | Simplify collision; reduce caps |
| 6 | Escape mechanic, safe zone and no-grab toggle exist | Add all three |
| 7 | Short immunity after being thrown | Add 2–3 s |
| 8 | Rating trend is stable | Review grief reports; strengthen consent controls |
| 9 | No pass changes reach, strength or escape | Convert to cosmetics or limits |
| 10 | At least three built-in mini-games with boards | Add targets, ramps, towers |
| 11 | A goal layer exists for players who want one | Add distance-pays progression |
| 12 | One new toy per week | Keep a toy backlog |

## Review gate

- [ ] The verb is fun in five seconds on a phone.
- [ ] Ownership, validation and velocity clamps are specified for props and for players.
- [ ] Consent and escape are designed, not added after complaints.
- [ ] Physics budgets hold at full population.
- [ ] No player-versus-player physics stat is sold.
- [ ] Props, toys and houses are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives, §Gap analysis (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `59 Viral and Trend Game Teardowns/Teardown - Fling Things and People.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/boneheads/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
