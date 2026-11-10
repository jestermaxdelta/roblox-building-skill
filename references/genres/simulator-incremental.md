# Simulator, incremental and clicker playbook

Covers click-or-collect simulators, "X Incremental" upgrade-board games, standalone RNG rollers and collection sims such as fishing. Open it when the loop is "act → number goes up → upgrade → new zone → rebirth", or when auditing a live simulator that bleeds players at the first wall. For stat-per-second lane games use `plus-one-evolution.md`; for the egg and pet layer use `pet-collection-hatching.md`. Market numbers are the vault's 2026-11-07 snapshot `[VS]`.

## Snapshot

- Market position (vault, 2026-11-07): **crowded with a long tail**. "X Incremental": Depth Incremental 19.8K CCU and Noob Incremental 5.5K lead; about 30 of the first 40 results are under 1K. Standalone RNG is **winner-take-most**: Sol's RNG 41K (about 40K held for 2+ years by adding depth), Anime Dice 30K, then a fast drop under 3K. Clicker/collect: Tap Simulator REBORN 36–37K, Bee Swarm Simulator 32K, Cut a Rock 26K. Fishing is **durable, up 55% year on year**: Fisch 79K, Fish It 63K, Net a Fish 14K.
- Simulators overall cooled from 55% to 35% of top-10 CCU between September and October 2026 (vault). A third-party tracker reports 189 new simulator launches in one quarter with average CCU per game down 20% `[community]`.
- The leaders add a visible journey: Depth Incremental digs down a pit ("Day 1 → Day 100, +$23/s → +$23,382,465/s"); menu-only incrementals sit under 2K.
- Audience: young, casual, plays one-handed on a phone; session 14–34 min in comparable games (vault). Server size is flexible: shared lobbies of 12–30 work because players do not compete for space `[house]`.

## Core loop with timings

| Variant | Loop | Timing targets |
|---|---|---|
| Click / collect sim | Act → fill backpack → sell → upgrade tool or capacity → next zone → rebirth | Action feedback under 100 ms; sell trip under 20 s; upgrades 3–10 s apart for the first ten |
| X Incremental | Income ticks automatically → spend on a large upgrade board or tree → boss gate → reset layer 1 → layer 2 | First upgrade within 15 s; a new board node every 20–60 s in session 1 `[house]` |
| RNG | Roll (slot-machine reveal) → keep best → auto-roll in the background → craft or equip luck gear | Roll cycle 1–3 s with skip; rare reveal 3–6 s `[house]` |
| Fishing / collection | Cast → timing minigame → catch with a rarity → sell or index → better rod → new water | One catch every 10–30 s `[house]` |

- First zone unlock inside 3 min and first rebirth at 15–25 min so a discovery player sees the whole loop in one session `[house]`.
- X Incremental format norms (vault): 2+ reset layers, often a boss gate before rebirth, and an RNG side system (titles, runes, fossils). Robux is light in this format.

## First 5 minutes

1. 0:00 spawn next to the first thing to hit or collect; the tool is already equipped.
2. 0:05 first number pop; 0:20 first sale; 0:30 first upgrade purchased.
3. 1:30 backpack or cap fills for the first time: the wall teaches selling and the capacity upgrade.
4. 3:00 first zone gate opens with a new prop set and a new resource colour.
5. 5:00 the rebirth button is visible with its requirement and reward.
- Friction between upgrades is the enemy `[official]`; if any gap in the first 5 minutes exceeds 30 s, insert a cheaper step.

## Progression and economy shape

- Costs: geometric `g` 1.15–1.5 per tier for tools and capacity; zone gates as larger steps. Rebirth: multiplicative, wait ratio ×1.2–1.5 between successive rebirths (economy-and-progression.md).
- Layers must change the verb or the view, not just the suffix: a new zone brings a new resource, enemy or movement, and a new reset layer unlocks a new board.
- Numbers outgrow meaning: K/M/B suffixes, round before formatting, mantissa/exponent storage before 1e15.
- Prestige is a decision, not a reflex: show "rebirth now gives ×A, in 5 min gives ×B" so the timing choice is readable `[community]`.
- RNG works best as a layer inside another loop (vault inference: Net a Fish's "1 in 10M", Noob Incremental's runes), not as the whole game.
- Sinks: tool tiers, capacity, zone unlocks, crafting luck gear, cosmetic auras. Sink ratio near 1.0 across a week.

## Monetisation set that fits

- Keep from the default set: 2× Cash 10/30 min, 2× Speed (click, gather), Auto-Collect / auto-click pass, extra storage, permanent 2× Cash, Starter Pack, currency packs, VIP, gift passes.
- Add: rebirth skip (vault: 99 R$ in Kick a Lucky Block), auto-sell, auto-roll speed, extra equip slots.
- Luck 2× and Server Luck only where rolls exist; then they are paid random items: full odds shown, boosted odds shown live, `PolicyService` gate. Vault prices: X2 Money 399 R$, X2 Growth Speed 467 R$.
- Delete: 2× EXP unless a level track exists; Revive.
- Rewarded video `[official]`: velocity boosts, doubled offline earnings, energy refills, 10 minutes of auto-click that previews the pass. Benchmark opt-in 13%+, frequency 2.8.
- Dev-product-led catalogues win the format (vault: +1 Gun Forge 123 products, Venom 36). Leaderboards must not be buyable outright: separate a "no boosts" board or rank by rebirth count `[house]`.

## Retention and social hooks

- Timers: rare spawn every 5 or 15 min, server event every 30 min, daily shop, weekly update on a fixed day.
- Offline progress with a stated cap; a "claim" card on return.
- Collection index with completion rewards; global and friends leaderboards (`OrderedDataStore`, written every few minutes and on leave).
- Friend boost +10–20%; group bonus; codes on update day.
- A vendor case study credits a 7-day login calendar ending in a rare pet with lifting D1 from 18% to 29%; unverified `[community]`. If used, make it cumulative (a missed day never resets it).

## UI patterns

- HUD: currency, backpack bar, one "next goal" chip, boost pills with honest timers. Thumb-reachable Sell/Teleport button.
- Upgrade board: nodes show cost, effect and the delta ("+25% → +40%"); affordable nodes pulse once, not continuously.
- Roll reveal: skippable, with the odds text on the result card ("1 in 10,000") drawn from the server's table.
- Buy-max uses the closed-form sum; never loop purchases through remotes.

## Technical hot spots

- **Click remotes**: batch on the client (send a count every 0.2–0.5 s), cap credited actions per second on the server, and reject batches that exceed the cap. Server computes value from its own multipliers; the payload never contains an amount.
- **Auto systems** (auto-click, auto-roll, auto-sell) run on the server in one shared loop with a per-frame budget, not one thread per player.
- **Pickups and orbs**: spawn and animate on the client from a server seed; the server validates a collect request by id, position and timing.
- **Rolls**: one `Random` on the server; the displayed odds table and the roll table are the same data; never send the full weighted table of unreleased items to clients.
- **Saves**: unlock sets and counters, not arrays of instances; session-locked profiles; throttle leaderboard writes.
- **Zones**: `StreamingEnabled` with per-zone models; teleport gates check the unlock on the server.
- Mobile: number pops and VFX pooled and capped per frame; a 3 GB phone drops frames from hundreds of simultaneous `BillboardGui`s.

## The one-new-verb angle

- Replace "click" with a physical verb that reads on a thumbnail: dig, cut, throw, kick, reel.
- Turn the stat into a place: depth, height, distance. A visible journey beats a bigger suffix (vault patterns 2 and 3).
- Open pairings in the vault: ragdoll launch × incremental (hybrids under 2K), anomaly × fishing (under 2K).

## Common failure modes

- A reskin of a crowded format with no new action; lands in the under-1K tail.
- First wall before the first rebirth; players leave at minute 6–8.
- Zones that only change colour and multiplier.
- Standalone RNG with no second system; winner-take-most punishes entrants.
- Upgrade trees with shortcuts that skip orders of magnitude and make the intended path pointless `[community]`.
- Trusting the client for click counts or sell values; inflation from exploiters wrecks leaderboards.
- Marketing before retention is fixed (one developer reports buying ads at 6% D1 as wasted spend) `[community]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First upgrade inside 30 s; no gap over 30 s in the first 5 min | Insert cheaper early tiers |
| 2 | First rebirth reachable in 15–25 min | Lower the first requirement; keep later wait ratio ×1.2–1.5 |
| 3 | Each zone adds a verb, resource or view | Rework the two weakest zones before adding new ones |
| 4 | The stat is visible in the world (depth, size, distance) | Add a physical journey for the main stat |
| 5 | Funnel shows no step losing over 40% of players | Find the wall with funnel events; bridge it |
| 6 | Server caps actions per second; payloads carry no amounts | Add batching and a server cap; recompute value server-side |
| 7 | Offline income with stated cap | Add it with a return card |
| 8 | Timers exist at 5/15/30 min | Add rare spawns and a server event |
| 9 | Odds shown before any paid roll; boosted odds live | Build the odds panel from the roll table; add the `PolicyService` gate |
| 10 | Catalogue is dev-product-led with entries under 50 R$ | Add timed boosts, skips and packs |
| 11 | Leaderboards are not purely purchasable | Rank by rebirths or add a clean board |
| 12 | Numbers stay readable past 1e15 | Mantissa/exponent store; suffix formatter |
| 13 | Frame time holds on a 3 GB phone during a multi-pop burst | Pool and cap pops and VFX |

## Review gate

- [ ] The loop names a physical verb and a visible journey, not only a theme.
- [ ] Price and rebirth curves are modelled against minutes; first rebirth inside session 1.
- [ ] All income, rolls and sells are server-computed and rate-limited.
- [ ] RNG, if present, is a layer with disclosed odds, not the whole game.
- [ ] Timers, offline cap, index and a fixed update day are planned.
- [ ] Tools, resources, zones and pickups are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/incremental-sim.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://devforum.roblox.com/t/how-to-increase-retention-engagement-etc-in-a-simulator/3292053 (search summary)
- https://rolearn.dev/insights/genre-saturation-opportunity (search summary; third-party)
- https://rolearn.dev/case-studies/simulator-500-to-50k (search summary; vendor case study)
- https://rowatcher.com/news/the-simulator-blueprint-how-every-hit-game-is-built (search summary; host not reachable for a full read)
- r/incremental_games threads on prestige timing and upgrade-tree shortcuts, seen through search mirrors (search summary)
- https://github.com/LILRINO71/power-punch-simulator (read README; 1 star, MIT; small Rojo clicker with server-side rate limiting; reference only)
- https://github.com/MadStudioRoblox/ProfileStore (search listing; 352 stars, Apache-2.0)
