# Steal-and-defend (base raid) playbook

Covers "Steal a ___" games: each player owns a base that earns per second from collected items, and every other player can walk in and carry one off. Open it when theft between players is the core action, or when auditing a live steal game for exploit load, complaints and the house-rule conflicts this genre carries. Market numbers are the vault's 2026-11-07 snapshot `[VS]`.

## Snapshot

- Market position (vault, 2026-11-07): **peaked, saturated, still the largest genre**. Steal An Egg 1.14M CCU (#1; peak 14.31M on 19 Sep 2026), Break and Steal an Egg 129K (a clone shipped about 6 weeks into the parent's rise; peak 1.31M), Steal a Brainrot 103K (peak 25.4–25.8M in Oct 2025, now event-driven). About 1.55M CCU across the genre, but of 40 "Steal a" results only 7 exceed 10K.
- Lifecycle (vault): mega-hits peak 7–8 weeks after launch, plateau 2–5 months on weekly updates and events, then fall 90–99%. Theme-only brainrot clones settle at 4–15K (median 8.4K across 21 games); a remix with a new mechanic (Escape Tsunami For Brainrots, about 5M peak) beats straight clones.
- Legal and policy heat: "hundreds" of Steal a Brainrot clones and at least 4 lawsuits; Steal An Egg was briefly pulled in Aug 2026 over an in-game video feed (vault). Near-identical titles, visuals or place files are penalised in discovery.
- Audience: broad and young; drama between players is the content. Large shared lobbies. Sessions are driven by "just catch the next spawn" timers.
- Partial gap (vault): steal × tower defence (Garden TD 6.8K, Brainrot TD 932).

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

## Monetisation set that fits

- Keep from the default set: 2× Cash 10/30 min, permanent 2× Cash (vault: X2 Money 399 R$ in Steal An Egg), 2× growth or hatch speed (vault: 467 R$), Starter Pack, extra item slots, Auto-Collect, Luck / Server Luck where spawns or eggs are random (odds shown, `PolicyService` gate), VIP, gift passes, private servers.
- Add: base skins and themes, carry and steal VFX, alert sounds, index cosmetics, rebirth skip in PvE terms.
- Delete or rework: Revive (no death loop); anything that sells raid or defence power.
- **Conflict (market vs house rule 3):** leaders sell Robux gear and buyable admin powers (vault), and player guides list paid steal-speed and lifetime double-money passes `[community]`. Selling steal speed, stuns, lock length or trap damage is stat power in a competitive mode and is not allowed here. Sell income, convenience and cosmetics; keep every raid and defence stat earnable only.
- Social-action boosts (like, favourite, group) are bonuses only: vault example 10K free Speed. Keep them out of the title, thumbnail and description.
- Offers never fire on being robbed. Positive triggers only: after a successful steal banked, a rebirth, a new index entry.

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

## Technical hot spots

- **Authoritative carry state.** The server owns who carries what. A steal is a server-timed hold (start, required seconds, distance and line-of-sight checks at start and end), never a client "I stole it" event.
- **Movement exploits are the genre's main load**: teleport-to-base, speed and fling. Results for this genre are full of script-hub "auto lock" and "instant steal" pages. Options: server-side speed and teleport sanity on carriers (rubber-band, drop the item on violation), or build on the server authority model (`Workspace.AuthorityMode = Server`, prediction and rollback) `[official]` `[VS]`.
- **Lock timers**: store the lock end as a server timestamp and replicate the timestamp; clients render the countdown from `Workspace:GetServerTimeNow()`. Lock toggles are rate-limited and validated on the server.
- **Ownership transfer** debits one profile and credits another in one server step, both session-locked, with a transfer id logged. A carrier who leaves or is kicked drops the item back to the owner.
- **Server hopping and alts**: detect repeated transfers between the same two accounts and cap per-pair transfers per hour; treat private servers as the easiest place to feed an alt and apply the same caps there `[house]`.
- **Physics griefing**: disable player-player collision inside bases or use collision groups; no pushable unanchored props near pedestals.
- **Scale**: 20–30 player lobbies with dozens of items per base; items are anchored Blender meshes rendered once, income is a number, not an instance per tick.

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
