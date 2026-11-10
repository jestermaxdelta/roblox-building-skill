# RNG and aura-rolling playbook

Covers games whose core verb is one button: roll for an item, aura or title with a "1 in N" rarity, keep the rarest, and feed luck, crafting and a collection around it. Open it when rolling is the game or a major layer, when writing roll tables whose shown odds must equal real odds, or when auditing a live RNG game for compliance, inventory flooding and a flat long loop. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026). For egg and pet rolls inside another loop see `pet-collection-hatching.md`.

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One roll button and auto-roll; one server-side weighted table of 15–25 items in 5–6 tiers; a reveal with tier colour; an index; an equip slot that shows the result on the player | Luck stacking, crafting, biomes, trading, paid rolls |
| Intermediate | A table module that reports its true probabilities; progress cap on rollable tier; pity with a visible counter; salvage and fusion for duplicates; inventory filters; server-time world states that shift luck | Cross-server announcements, seasons |
| Expert | Minutes-to-tier modelling per luck level; full paid-random-item compliance with live odds; maximum stacked luck checked against every tier; VFX budgets with "hide others"; macro detection | — |

Terms: *luck* = a modifier that raises the chance of rarer outcomes; *pity* = a guarantee after a number of unlucky rolls; *progress cap* = a limit on the best tier a player can roll, tied to how far they have progressed.

## Snapshot

- Market position (vault, 2026-11-07): **winner-take-most**. Sol's RNG 41K CCU, holding about 40K for 2+ years by adding depth; Anime Dice 30K (up 19 of 19 weekdays in September); then a fast drop under 3K (PlaneRNG 3K, Case Simulator RNG 1.8K, Barber RNG 453). RNG was 18% of the owner's second feed. The vault's reading: RNG works best as a layer inside another loop (a fishing game's "1 in 10M", an incremental's runes).
- The leader `[lihfolk]` `[VS]`: created Dec 2023, 20-player servers, about 91% positive, 400+ auras; it outlasted the early-2024 wave by turning the button into a world (biomes on server time, crafting from duplicates, potions, numbered seasons).
- Why it works `[lihfolk]`: anticipation on every press, big denominators that are stories by themselves, a collection, status worn on the avatar, clips of rare pulls, and one-button input ideal for phones.
- The same mechanics are borrowed from gambling. On a platform full of children that creates duties: honest odds, no paid gambling loops, policy compliance `[lihfolk]`.
- Audience: broad, phone-first, idle-tolerant. Dashboard genre: Simulation › Incremental Simulator or Idle `[VS]`.

## Core loop with timings

| Step | What happens | Timing |
|---|---|---|
| Roll | Press or auto-roll | Reveal about 2.5–3.2 s base; speed upgrades shorten it to a floor `[lihfolk]` |
| Reveal | Reel or animation lands; tier colour, banner, "1 in N" | Higher tiers get longer, louder reveals; low tiers skippable in auto |
| Keep | Equip best; index entry; server broadcast for rare pulls | Instant |
| Convert | Salvage, fuse or craft duplicates | Seconds, in batches |
| Shift luck | Potions, gear, world state (biome), friends | Windows of minutes |
| Advance | New zone or cap raises the rollable tier | Session goal |

- One reference project raised its manual spin from 2.4 s to 3.2 s because rolls felt too fast, with auto-roll at 2.56 s `[lihfolk]`: the reveal is the product, not a delay to minimise.
- Manual roll gets the full-screen reveal; auto-roll shows a small reel over the player's head so the world stays visible `[lihfolk]`.

## First 5 minutes

1. 0:00 the roll button is the largest thing on screen; first roll inside 5 s.
2. 0:10 even a common result plays an animation with its "1 in N" shown large `[lihfolk]`.
3. 1:00 auto-roll unlocks; the numbers start to flow.
4. 2:00 first duplicate: the tutorial teaches salvage-then-upgrade or fuse `[lihfolk]`.
5. 3:00–5:00 a world-state change (biome, weather) sweeps the server and visibly shifts luck; the index shows silhouettes of the next tier with its odds.

## Progression and economy shape

- **Rarity ladder**: 6–9 tiers, one colour per tier used everywhere; stats follow odds within a tier. Rarer must look better: a rule from one project is that every top-tier item is animated `[lihfolk]`.
- **Expected rolls** `[lihfolk]`: at "1 in N", about 63% of players have the item after N rolls; a 99% chance needs about 4.6 N. Convert to minutes with rolls per minute. Example: about 19 manual rolls a minute and a 1-in-2,000 item is about 105 minutes on average, and about 8 hours for the unlucky 1%. Model every tier this way at each luck level.
- **Progress caps**: without a cap a lucky newcomer rolls the best item on day one and the long loop is flat. Cap the rollable tier by zone or level, grant luck from progression (upgrades, rebirths), or unlock tier-specific rolls by progress `[lihfolk]`.
- **Pity** `[lihfolk]`: hard pity (guarantee tier T after K rolls), soft pity (luck rises past a threshold), tokens (each roll earns a token toward a chosen item), duplicate protection. Show the counter ("Epic guaranteed in 137 rolls"); visible pity turns frustration into anticipation.
- **Duplicates are a resource** only if the game says so: index, salvage to materials, forge or upgrade, fusion into stars or the next tier, player-set auto-salvage rules.
- **Luck stack**: define which tiers luck affects and how sources combine; compute the maximum possible stacked luck and check it against every tier so no stack makes the top tier common.
- **World state**: biomes or weather on server time change odds for everyone; a built-in event calendar.

## Monetisation set that fits

- Cleanest first `[lihfolk]`: direct-purchase exclusives that are never rollable (fixed outcome), then speed (fast roll, double roll: more results per press, not better odds), then luck with disclosure.
- Keep from the default set: Luck 2×, Server Luck (benefits everyone; odds update for all), Starter Pack with fixed contents, extra storage, VIP, gift passes, private servers.
- Reference prices from one project `[lihfolk]` `[VS]`: fast-roll pass 299 R$, double-roll pass 599, a small luck pass 75, VIP 399 (includes ×1.1 luck), server luck 99, a paid jackpot roll 499, weekly direct-purchase exclusives 999.
- Delete: Revive, 2× Cash unless a currency economy exists, Auto-Collect.
- **Policy** `[official]` `[VS]`: a roll bought with Robux or Robux-bought currency, and any paid luck, is covered. Show all outcomes with odds as **percentages that sum to exactly 100%** (a "1 in N" label may sit beside the percentage but does not replace it); round long decimals to four or more places past the first non-zero digit with the docs' disclaimer; put overflow in a labelled "Info" or "Details" pop-up; explain paid luck numerically before purchase and update shown odds while it is active; if an outcome can be obtained only once, update the remaining odds for that player. Enforce `ArePaidRandomItemsRestricted` and `IsPaidItemTradingAllowed`.
- Free rolls earned by play need no disclosure; show the odds anyway.
- **Near-miss rule** `[lihfolk]`: a reel that slows past a rare item must draw from the real table and never imply an outcome the player could not have had; never use near-miss presentation on any roll bought with Robux. This matches house rule 3.
- If purchases bypass the progress cap, the disclosure must show the odds the purchased roll really has.

## Retention and social hooks

- World-state rotation ("the rare biome is up, roll now"), numbered seasons with fresh items, a weekly exclusive rotation.
- Server broadcasts and worn auras make one player's luck a server event; 20-player servers suit this `[lihfolk]`.
- Index completion per tier; crafting goals that consume commons so every roll counts.
- Offline or AFK rolling with a stated cap; discovery credits at most 60 minutes of play per user per day `[VS]`.

## UI patterns

- A giant central roll button with an AUTO toggle; standing luck readout ("1.00×") on the HUD `[lihfolk]`.
- Result card: tier colour first, banner, item name, "1 in N"; world burst for rare tiers.
- Inventory for phones: search, filter by tier, hide duplicates, sort by rarest or newest, favourite lock, bulk salvage.
- Odds screen: base percentages, active modifiers, resulting percentages, pity counter.
- Settings: hide other players' auras, reduce flashes.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §4 Pets, eggs and hatching with odds, §2 Inventory and equip, §18 Crafting, §24 Server-wide events and boosts, §5 Upgrades and rebirth. Its "Build order by genre" table gives a second opinion.

1. Roll table module with `roll` and `probabilities` from the same weights.
2. Roll service on the server with rate limiting; auto-roll loop.
3. Reveal presentation (manual and auto variants).
4. Inventory with stacking, filters and caps; index.
5. Equip and display on the avatar.
6. Salvage, fusion and crafting.
7. Luck stack and world-state schedule on server time.
8. Progress cap and zones.
9. Pity counters.
10. Odds screen and policy gate; then broadcasts, seasons, trading.

## Technical hot spots

- **Two implementations, two sets of real odds** `[lihfolk]`. *Normalised weights*: each item has weight 1/N; if the weights do not sum to 1, every real probability is scaled and the labels are wrong. *Rarest-first independent checks*: test the rarest first with chance 1/N, fall through to a default; rare labels are nearly exact, but a common labelled "1 in 2" checked after others lands below 50% and the fallback has no meaningful label. Example with labels 1 in 4, 1 in 2, 1 in 2: weights give 20% / 40% / 40%; rarest-first gives 25% / 37.5% / 37.5%. Compute the shown percentages from the actual algorithm; never hand-type them.

```lua
--!strict
-- Unexecuted sketch: one weight list drives both the roll and the disclosed odds.
export type Entry = { id: string, weight: number }

local function probabilities(entries: { Entry }): { [string]: number }
	local total = 0
	for _, e in entries do total += e.weight end
	local out: { [string]: number } = {}
	for _, e in entries do out[e.id] = e.weight / total end
	return out
end

local function roll(entries: { Entry }, rng: Random): string
	local total = 0
	for _, e in entries do total += e.weight end
	local pick = rng:NextNumber() * total
	for _, e in entries do
		pick -= e.weight
		if pick <= 0 then return e.id end
	end
	return entries[#entries].id
end

return { probabilities = probabilities, roll = roll }
```

- **Luck semantics** `[lihfolk]`: multiply the weights of affected tiers and renormalise; or roll twice and keep the best; or bump the result up a tier with some chance. Each gives different real odds; pick one, document it, and feed it through `probabilities`.
- **Server only**: a `Random` on the server; never accept a result or a seed from the client; rate-limit the roll remote even though the animation paces it. Pity counters are server state saved in the profile.
- **Auto-roll** runs in one server loop with a per-frame budget; the client only animates.
- **VFX budget**: twenty players wearing large auras is a heavy particle load on a 3 GB phone. Offer "hide others' auras", reduce distant auras, cap emitters per aura. Auras are Blender meshes plus particle and beam effects; rarity must read from the silhouette and colour alone.
- **World state from server time** (`Workspace:GetServerTimeNow()` and a deterministic schedule) so every server agrees without messaging.
- **Inventory data**: stacks and counts; unique ids only for tradable items; cap and auto-salvage to stay within key limits.

## The one-new-verb angle

- Give the roll a body: what you roll changes how you move, fight, fish or build (the vault's reading: RNG as a layer).
- Put the roll in the world: a physical machine, a dig, a cast, a thrown die that lands on terrain.
- Standalone "press to roll" entrants meet a winner-take-most field.

## Common failure modes

- Hand-typed "1 in N" labels that differ from the algorithm.
- Luck with undefined semantics; uncapped stacks that trivialise the ladder.
- No progress cap; day-one jackpots flatten the game.
- Paid odds shown only as "1 in N", not as percentages, or not updated under boosts.
- Near-miss effects on paid rolls.
- Inventory flooding with no salvage, fusion or filters.
- Rare items that look ordinary.
- Client-side rolls or seeds.
- A button with no second system; players leave when the first long gap arrives.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Shown odds are generated from the roll code | Add a `probabilities` function; delete typed labels |
| 2 | 100,000 simulated rolls match shown odds within tolerance | Write the test; fix the table |
| 3 | Luck rule is documented and applied in both roll and display | Unify the implementation |
| 4 | Maximum stacked luck leaves the top tier rare | Cap luck or exclude tiers |
| 5 | A progress cap or progression luck exists | Add zone caps |
| 6 | Pity exists with a visible counter | Add hard or soft pity |
| 7 | Minutes-to-tier table exists for the unlucky 1% | Model with 4.6 N; adjust speed, luck, pity |
| 8 | Duplicates convert to something | Add salvage and fusion |
| 9 | Paid rolls and luck show percentages totalling 100%, live under boosts | Build the odds screen |
| 10 | Policy flags enforced with a fallback | Add gate and direct purchase |
| 11 | No near-miss on paid rolls | Remove it |
| 12 | Rolls are server-side and rate-limited | Move and limit |
| 13 | Frame rate holds with 20 auras in view on a 3 GB phone | Hide-others toggle; emitter caps |
| 14 | A second system makes the roll matter | Add crafting, zones or a host loop |

## Review gate

- [ ] The roll has a purpose beyond itself (a host loop, crafting or zones).
- [ ] Table, luck, caps and pity are modelled in minutes for average and unlucky players.
- [ ] Displayed odds are computed, tested and compliant; paid randomness has a restricted-player path.
- [ ] No manipulative presentation on paid rolls.
- [ ] Rolls and counters are server state; VFX fit the phone budget.
- [ ] Items, auras' mesh parts, machines and zones are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - RNG and Collection Games.md`, `59 Viral and Trend Game Teardowns/Teardown - Sol's RNG.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read; percentage format, rounding, one-instance rule, luck disclosure)
- See also `references/economy-and-progression.md` §Random rewards and `references/case-studies-teardowns.md`.
