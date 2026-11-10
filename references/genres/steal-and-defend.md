# Steal-and-defend (base raid) playbook

Covers "Steal a ___" games: each player owns a base that earns per second from collected items, and every other player can walk in and carry one off. Open it when theft between players is the core action, or when auditing a live steal game for exploit load, complaints and the house-rule conflicts this genre carries. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | Bases with slots and per-second income; one shared source of items (conveyor or nests) from a server weight table; a base lock on a server timestamp; server-validated steal (distance, lock, carry, cooldown); newcomer shield; session-locked saves | Rebirth, mutations, fusion, events, trading, guardians, biomes |
| Intermediate | Rarity ladder with 1–3 mutation multipliers from one config; rebirth that adds slots and lock time; restock or spawn timers shown on the HUD; steal-back route and per-victim cooldown; speed and teleport sanity on carriers | Cross-server events, crossovers |
| Expert | Event framework with scheduled server-wide spectacles; alt and transfer-pattern detection; income-gap theft limits; mobile budget for full pens; weekly numbered updates; original characters and UI reviewed for legal distance from leaders | — |

Terms: *base lock* = a timed shield during which nothing can be stolen; *carry state* = the server's record that a player is holding a stolen item; *mutation* = a multiplier variant of an item (Gold, Rainbow); *admin event* = a scheduled live spectacle run by the developers.

## Snapshot

- Market position (vault, 2026-11-07): **peaked, saturated, still the largest genre**. Steal An Egg 1.14M CCU (#1; peak 14.31M on 19 Sep 2026), Break and Steal an Egg 129K (a clone shipped about 6 weeks into the parent's rise; peak 1.31M), Steal a Brainrot 103K (peak 25.4–25.8M in Oct 2025, now event-driven). About 1.55M CCU across the genre, but of 40 "Steal a" results only 7 exceed 10K.
- Lifecycle (vault): mega-hits peak 7–8 weeks after launch, plateau 2–5 months on weekly updates and events, then fall 90–99%. Theme-only brainrot clones settle at 4–15K (median 8.4K across 21 games); a remix with a new mechanic (Escape Tsunami For Brainrots, about 5M peak) beats straight clones.
- Legal and policy heat: "hundreds" of Steal a Brainrot clones and at least 4 lawsuits; Steal An Egg was briefly pulled in Aug 2026 over an in-game video feed (vault). Near-identical titles, visuals or place files are penalised in discovery.
- Audience: broad and young; drama between players is the content. Large shared lobbies. Sessions are driven by "just catch the next spawn" timers.
- Partial gap (vault): steal × tower defence (Garden TD 6.8K, Brainrot TD 932).
- Session and longevity signals `[lihfolk]`: trend hits in this family average 15–16 min sessions against 25–31 min for longer-lived sims; games that held their rank combined about 90%+ approval with 25–30 min sessions, and spikes with 15-minute sessions faded fastest.
- "Is the trend dead?" heuristics `[lihfolk]`: the original's 30-day peak is under about 10% of its all-time peak and each new entrant peaks lower; the meme source has been declared over; clones with no twist cannot clear a few thousand CCU. Even then the loop often survives as a stable genre, as the egg re-skin a year later showed.
- Conflict (server size): the vault's pattern 14 gives steal games larger shared lobbies; LihFolk measured the current leader at 7-player servers, which keeps every pen within one screen of travel and fits a phone budget. Trust the measurement for egg-pen formats; larger lobbies suit conveyor-and-plaza formats.

## Core loop with timings

| Step | Steal a Brainrot (vault) | Steal An Egg (vault) |
|---|---|---|
| Acquire | Buy from a shared conveyor | Grab an egg past a guardian; bigger eggs slow you |
| Earn | Item pays $/s at your base | Egg grows at your pen for 10 s–25 min, hatches a pet paying $/s and Speed |
| Raid | Walk into another base, carry a rarer item home | Same, plus Speed gates the next biome |
| Defend | Base lock on a timer, traps and gear | Pen defences |
| Reset | Rebirth for a multiplier and a longer base lock | New biome |
| Timers | Legendary about every 5 min, Mythic every 15 | Nests reset every 5 min, events every 30 min, numbered weekly updates |

- Fan guides describe a 30 s base lock on joining a server, with lock duration growing per rebirth `[community]`.
- Pace `[house]`: first owned item inside 30 s, first income tick inside 45 s, first successful steal inside 5 min, first time being stolen from only after the newcomer shield ends.
- What the leaders do well `[lihfolk]`: a shared, visible shop that moves (scarcity is public and shopping is a race); income per second as the headline number; a base lock with a visible countdown that everyone understands ("safe for 60 seconds"); a rebirth that adds safety (longer lock, more slots), not only multipliers; scheduled spectacle on all servers at once.

## First 5 minutes

1. 0:00 spawn inside your own base with the lock active and its timer visible.
2. 0:20 first cheap item bought or grabbed; it starts paying immediately.
3. 1:30 second and third items; the rare-spawn countdown on the HUD gives a reason to stay.
4. 3:00 a guided first raid on an unlocked base; carrying slows you and shows a route home.
5. 5:00 newcomer shield ends with a clear warning; the lock button and its cooldown are explained once.
- A new player who is robbed empty in minute 2 bounces; the bounce window (first 1–3 min) is the top discovery signal.

## Progression and economy shape

- Income per second → rarer items → rebirth multiplier. The collection is the multiplier; mutation tiers (vault: Silver 1.2× / Gold 2.5× / Rainbow 3.5×) and fusion reuse meshes.
- Index of every item ever owned; an entry survives theft, so loss never erases collection progress.
- Theft is a transfer, not a sink. Add real sinks: rebirth costs, base upgrades, fusion, slots.
- Loss limits (house rule: no retention through punishment) `[house]`: newcomer shield for the first 10–15 min of lifetime play; items cannot be stolen while their owner is offline (the base leaves with the player); per-victim cooldown so one base is not emptied in a streak; a stolen item keeps paying the victim a reduced rate until the thief banks it, or can be reclaimed if the thief is tagged in transit.
- Speed, carry weight and lock duration are the PvP stats. Earn them in play.
- Newcomer grace can be a time window or theft limits based on the income gap between thief and victim, so a first theft is a lesson, not a loss `[lihfolk]`.
- Give every biome a single movement idea (darkness, jump pads, ice); speed upgrades then open new ways to play as well as new items `[lihfolk]`.
- No wagers or coin flips of items between players: Roblox prohibits simulated and real gambling `[lihfolk]` `[VS]`.

## Monetisation set that fits

- Keep from the default set: 2× Cash 10/30 min, permanent 2× Cash (vault: X2 Money 399 R$ in Steal An Egg), 2× growth or hatch speed (vault: 467 R$), Starter Pack, extra item slots, Auto-Collect, Luck / Server Luck where spawns or eggs are random (odds shown, `PolicyService` gate), VIP, gift passes, private servers.
- Add: base skins and themes, carry and steal VFX, alert sounds, index cosmetics, rebirth skip in PvE terms.
- Delete or rework: Revive (no death loop); anything that sells raid or defence power.
- **Conflict (market vs house rule 3):** leaders sell Robux gear and buyable admin powers (vault), and player guides list paid steal-speed and lifetime double-money passes `[community]`. Selling steal speed, stuns, lock length or trap damage is stat power in a competitive mode and is not allowed here. Sell income, convenience and cosmetics; keep every raid and defence stat earnable only.
- Social-action boosts (like, favourite, group) are bonuses only: vault example 10K free Speed. Keep them out of the title, thumbnail and description.
- Offers never fire on being robbed. Positive triggers only: after a successful steal banked, a rebirth, a new index entry.
- LihFolk reaches the same conclusion as house rule 3: selling theft tools or power over other players draws "pay to win" reviews and press criticism; sell self-only boosts and cosmetics `[lihfolk]`.
- Converting an existing power pass: removing purchased functionality without proper notice is listed under fraud in Roblox's standards `[lihfolk]` `[VS]`. Announce the change and replace the benefit with equal non-combat value.

## Retention and social hooks

- Timers everywhere: rare spawn every 5 and 15 min, server event every 30 min, weekly numbered update on a fixed day (Steal An Egg ships Saturdays).
- Live events are the biggest lever in this genre: admin events, concerts and crossovers set the platform records (47.3–47.4M CCU; Steal An Egg 713K → 1.09M on a concert) (vault). Schedule them as Experience Events with real end times.
- Friends: shared defence, co-raid bonuses, private servers for friend groups (intentional co-play counts for discovery).
- Offline: income accrues to a stated cap; the base is safe while you are away `[house]`.

## UI patterns

- HUD: cash, income per second, lock button with remaining time, rare-spawn countdown, "being raided" alert that is informative, not alarming (no siren loop, no screen shake).
- Carry state: clear icon over the carrier, slow-down shown, a line to the home base on mobile.
- Base board in the world: owner name, lock time, top item (drives envy and target choice).
- Steal log: who took what, with a path to steal it back.
- Conflict (raid alert): LihFolk's juice list for the format includes a steal alarm and siren; this skill keeps the alert calm and informative for a young audience (no siren loop, no shake). A short distinct sound is fine; a repeating alarm is not.
- A friendly "Chances" tab on every egg or crate, built from the table that rolls, builds trust with parents and passes review `[lihfolk]`.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §19 Stealing and base defence, §16 Plots, tycoon ownership and placement, §1 Currency and wallet, §4 Pets, eggs and hatching with odds, §5 Upgrades and rebirth, §24 Server-wide events and boosts, §17 Trading. Its "Build order by genre" table gives a second opinion.

1. Base assignment, slots and per-second income tick.
2. Item config (rarities, mutations, prices) and the shared spawn source (conveyor, nests) with server weights.
3. Player data with session locking, autosave and close handling.
4. Base lock with server timestamps.
5. Steal, carry and bank state machine with validation.
6. Newcomer shield, per-victim cooldown, steal log.
7. Rebirth.
8. Index, fusion and mutations.
9. Timers and event framework (rare spawns, server events, admin commands).
10. Shop with policy-gated luck; then trading and cross-server events.

## Technical hot spots

- **Authoritative carry state.** The server owns who carries what. A steal is a server-timed hold (start, required seconds, distance and line-of-sight checks at start and end), never a client "I stole it" event.
- **Movement exploits are the genre's main load**: teleport-to-base, speed and fling. Results for this genre are full of script-hub "auto lock" and "instant steal" pages. Options: server-side speed and teleport sanity on carriers (rubber-band, drop the item on violation), or build on the server authority model (`Workspace.AuthorityMode = Server`, prediction and rollback) `[official]` `[VS]`.
- **Lock timers**: store the lock end as a server timestamp and replicate the timestamp; clients render the countdown from `Workspace:GetServerTimeNow()`. Lock toggles are rate-limited and validated on the server.
- **Ownership transfer** debits one profile and credits another in one server step, both session-locked, with a transfer id logged. A carrier who leaves or is kicked drops the item back to the owner.
- **Server hopping and alts**: detect repeated transfers between the same two accounts and cap per-pair transfers per hour; treat private servers as the easiest place to feed an alt and apply the same caps there `[house]`.
- **Physics griefing**: disable player-player collision inside bases or use collision groups; no pushable unanchored props near pedestals.
- **Scale**: 20–30 player lobbies with dozens of items per base; items are anchored Blender meshes rendered once, income is a number, not an instance per tick.
- **Shared restock or spawn clock**: derive stock from server time with a deterministic seed (or broadcast it) so every server shows the same items at the same moment; that turns a restock into a shared event `[lihfolk]`.
- **Pens on phones**: many animated items per base; cap visible ones, use shared animations and client-side idle motion `[lihfolk]`.
- **Guardian or chaser NPCs**: the server decides caught-or-not; clients smooth the visuals. Make the chase readable with a safe-line effect, a wind-up sound and a distance meter `[lihfolk]`.
- **Free models and kits**: "complete steal-game kits" circulate; backdoors arrive through free models more than any other route (check for obfuscated code and `require` calls on asset ids) `[lihfolk]`. House rule 1 already forbids shipping them.

## The one-new-verb angle

- "Steal" is taken. Change the acquisition or the escape: steal then outrun a wave (Escape Tsunami), steal and ride it, break it first, steal a tower and defend with it.
- Add a visible journey between bases (terrain, guardian, biome), not a flat ring of plots.
- Do not ship a theme swap: the vault marks "Steal a ___ × any new theme" as saturated.

## Common failure modes

- Clone shipped after the parent's peak; settles at 4–32K or in the under-1K tail.
- Newcomers robbed before their first income; first-minute bounce.
- Client-trusted steal or lock events; exploiters empty servers.
- Paid raid power: rating drops, "pay to win" reviews, and it breaks house rule 3.
- Alarmist raid alerts and loss spirals that make children quit upset; complaints and bad press follow theft formats (vault pattern 10).
- Copied art, names or UI layout from the leaders: lawsuit and near-duplicate exposure.
- An in-game media feed or UGC surface that moderation cannot cover.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Newcomer shield covers the first 10–15 min of lifetime play | Add it with a visible end warning |
| 2 | First income inside 45 s; first steal inside 5 min | Cheapen the first item; guide one raid |
| 3 | Steal is a server-timed hold with distance checks | Rewrite the steal remote as intent only |
| 4 | Carriers are speed- and teleport-checked, or the place runs server authority | Add sanity checks; drop item on violation |
| 5 | Lock end is a replicated server timestamp | Replace client countdowns |
| 6 | Transfers are atomic, logged, session-locked | Single server step with a transfer id |
| 7 | Leaving while carrying returns the item | Handle `PlayerRemoving` and kicks |
| 8 | No Robux product changes steal speed, stun, lock or trap strength | Convert to cosmetics or income; grandfather owners with a refund-equivalent grant |
| 9 | Per-victim cooldown and offline safety exist | Add both; state them in the UI |
| 10 | Index entries survive theft | Separate "owned ever" from "held now" |
| 11 | Rare spawns at 5/15 min and events at 30 min | Add the timers and HUD countdown |
| 12 | Weekly numbered update on a fixed day | Commit to a day; log Experience Events |
| 13 | Raid alert is calm and informative | Remove sirens, shake and red flashes |
| 14 | Title, art, UI and place file are distinct from the leaders | Restyle; rename; rebuild copied layouts |
| 15 | Approval near 90% and median session trending toward 25 min | Fix theft frustration first; add depth before events |
| 16 | Stock and spawn timers are identical across servers | Derive from server time with a shared seed |

## Review gate

- [ ] The concept adds a new acquisition or escape verb; it is not a theme swap.
- [ ] Shield, offline safety, per-victim cooldown and index persistence are designed.
- [ ] Steal, lock, carry and transfer are server-authoritative with exploit checks or server authority mode.
- [ ] No raid or defence power is sold; offers never trigger on loss.
- [ ] Events, timers and a weekly update day are scheduled.
- [ ] Nothing copies a leader's art, names or interface.
- [ ] Bases, items, locks and traps are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives, §Shared DNA, §Trend lifecycle (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/boneheads/index.md (read; official co-op reference game with stealing built on server authority)
- https://en.wikipedia.org/wiki/Steal_a_Brainrot (search summary)
- https://www.thestar.com.my/tech/tech-news/2026/03/25/robloxs-hit-game-steal-a-brainrot-battles-its-many-imitators (search summary)
- https://allthings.how/steal-a-brainrot-roblox-efficient-stealing-events-and-rebirths (search summary; player guide: 30 s join lock, paid passes)
- https://www.pcgamer.com/games/sim/one-of-robloxs-biggest-experiences-right-now-is-a-bizarre-italian-brainrot-character-stealing-simulator-and-lord-help-me-i-now-understand-why-its-so-popular (search summary)
- Web search for DevForum threads on building base-lock or steal systems (2026-11-10): no evidence found; results were player guides and exploit-script pages (not opened).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-trend-game/SKILL.md` and `references/trend-games-research.md` §1.2, §2, §3.2–3.3, §7, §8; `59 Viral and Trend Game Teardowns/Teardown - Steal An Egg.md`; `32 Case Studies of Top Roblox Games/Case Study - Steal a Brainrot.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
