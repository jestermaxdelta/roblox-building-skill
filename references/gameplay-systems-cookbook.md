# Gameplay systems cookbook

What this is: an implementation spec for the 24 gameplay systems Roblox games keep rebuilding, each with its data shape, server/client split, remote intents, validation rules, exploit surface, performance notes and known bugs. Open it when building a system, or when auditing a live one against its "Common bugs" line and the Level-up table at the end. Every design plugs into `DataService` and `ReceiptService` (data-and-purchases.md), `RemoteGuard` (networking-and-security.md) and the Init/Start loader (engineering-architecture.md); design intent (pacing, prices, ethics) lives in economy-and-progression.md, liveops-quests-retention.md and monetization-and-policy.md and is not repeated here. Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`, `[lihfolk]` adapted from LihFolk Vault V2.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | Read section 0. Build wallet → inventory → shop in that order on top of `DataService`. One remote per intent through `RemoteGuard`. Run the seven-step test list in section 0 on every system | Trading, matchmaking, lag compensation, cross-server anything, ECS |
| Intermediate | All-or-nothing grants, stable ids and GUIDs, absolute end times instead of countdown remotes, one odds function for roll and display, exploit table per system, a Configs kill switch per risky feature | Journalled trades, custom queues, rewind |
| Expert | Two-profile commit protocol for trades (17, specified in data-and-purchases.md), MemoryStore queues with a leased matcher (11), rewind-capped hit validation (12), spawn director and flow fields (13), budget maths for ordered stores (9), dupe detection jobs | — |

## Contents

0 Shared contract · 1 Wallet · 2 Inventory and equip · 3 Shop · 4 Pets and eggs · 5 Upgrades and rebirth · 6 Quests and achievements · 7 Daily and playtime rewards · 8 Codes · 9 Leaderboards · 10 Rounds · 11 Teams, queues, reserved servers · 12 Combat · 13 NPCs and hordes · 14 Tools and abilities · 15 Interaction and zones · 16 Plots and placement · 17 Trading · 18 Crafting · 19 Stealing and base defence · 20 Checkpoints · 21 Party and friends · 22 Chat commands and admin · 23 Time and day cycle · 24 Server-wide events and boosts · Build order · Level-up table · Review gate · Sources

## 0. Shared contract (every system below assumes this)

- **Shape:** shared `Config` (display-safe content: ids, names, prices, odds) → server `Service` whose public functions are synchronous and return `(ok, code)` → thin remote handlers (`RemoteGuard.connect`: rate, arg count, type, then the service call) → replicated state → client `Controller` that renders server state and shows the returned code. Assert config at boot (every reward exists, odds sum, every product has a grant) `[lihfolk]`. Terms used below: an *intent* is a remote that says what the player wants, never the outcome; the *profile* is the session-locked saved table from `DataService`; a *mutator* is the synchronous function passed to `DataService:Update`; a *dupe* is an item or balance that exists twice; a *faucet* adds currency to the economy and a *sink* removes it.
- **One of each:** one data writer (`DataService:Update`), one `ProcessReceipt`, one place that creates remotes, one server entry script.
- **Check and write in the same tick.** No `task.wait`, DataStore, HTTP, `MarketplaceService` or `IsInGroupAsync` call between a check and the mutation it guards. Web facts (group, pass, policy, badges) are fetched at join and cached in memory or an attribute; a claim path that yields can interleave with itself `[lihfolk]`.
- **All-or-nothing grants:** `Rewards.canGrant(player, bundle)` then `Rewards.grant`. A free reward into a full bag is refused and nothing is marked claimed; a paid receipt is always granted (overflow mailbox or forced add) because the player already paid `[lihfolk]`.
- **Ids:** content uses stable string ids, never array positions; each unique item gets `HttpService:GenerateGUID(false)` at mint and keeps it for life; saved tables use string keys only.
- **Clocks:** `os.time()` for day indexes and saved expiries; `workspace:GetServerTimeNow()` for replicated end times that clients count down from (round end, stun-until, lock-until); `os.clock()` for cooldowns and rate limits. Never a client clock, never one remote per second.
- **Replication:** public state as attributes on the Player or character (first 64 attributes, names and strings ≤ 50 chars `[VS]`). Private or bulky state (inventory, quest log) as a snapshot plus diffs on a RemoteEvent, or values under the player's own `PlayerGui`, which replicate to that player only. A JSON inventory in a Player attribute is sent to every client on every change; a production game measured this as lag in crowded servers `[lihfolk]`.
- **Result codes:** `Ok, TooFast, NotReady, Invalid, NotOwned, NotEnough, Full, Locked, Restricted, Disabled`. Unknown and not-yet-active look identical to the client (no information leaks).
- **Kill switch:** every risky feature (trading, gifting, codes, events) reads a Configs flag first and returns `Disabled`.
- **Test list** `[lihfolk]`: (1) change state, stop, play: it persists; (2) fresh profile key; (3) simulated load failure kicks and leaves the save untouched; (4) play/stop/play fast: lock path behaves; (5) two clients: nothing leaks between players; (6) fuzz each remote from a Studio-only script (wrong types, NaN, huge strings, extra args, 100/s): nothing is created from nothing; (7) unit-test the pure functions (day maths, odds, costs). Write an exploit table (attack → what stops it → what it does not stop) before calling a system done.

## 1. Currency and wallet

- **Purpose and data:** every balance change in one module. `Currencies: { [id]: number }` in the profile; config per currency `{ cap, paid }`; optional `Ledger` ring (last 50 `{ t, id, delta, reason }`) for support. Mark `paid = true` when Robux can buy the currency directly or indirectly: anything random bought with it is a paid random item `[lihfolk]`.
- **Split and remotes:** no earn remote exists. Gameplay code on the server calls `Wallet.add`; other systems' intents call `Wallet.spend`. Clients read a `Coins` attribute; `leaderstats` is display only.
- **Validate:** amounts are finite non-negative integers under a cap; balance re-read inside the mutator; reason string required. Results are checked too, because a formula that divides can produce NaN from valid inputs.
- **Exploit surface:** any remote carrying an amount; a yield between check and spend; click remotes without a token bucket at human rates; a multiplier accepted from the client; NaN balances (`NaN < cost` is false, so the purchase passes) `[lihfolk]`.
- **Performance:** coalesce attribute pushes to 4–10 Hz in click games; never save per change.
- **Common bugs:** integers stop being exact above 2^53 (≈ 9.007e15): clamp below it or move to mantissa + exponent (economy-and-progression.md); labels rounded up ("1.00M" at 999,999) invite a refused purchase; tradeable premium currency (regional-price arbitrage and real-money trading).

## 2. Inventory and equip

- **Purpose and data:** `Stacks: { [itemId]: count }` for stackables; `Items: { [uid]: { Id, Lvl?, Paid?, Lock? } }` for uniques; `Equipped: { [slot]: uid }`; a storage cap. `Paid` records provenance at grant time (needed for trade policy); `Lock` holds the id of whatever reserved the item (a trade, a craft queue).
- **Split and remotes:** server `canAdd / add / consume / equip`. Every path that removes an item goes through one `consume` that checks `Lock` and `Equipped`. Intents: `Equip(uid)`, `Unequip(slot)`, `Sell(uid | itemId, count)`, `SetLocked(uid)`. What others must see (equipped pets, skin) goes in one small attribute.
- **Validate:** uid is a string ≤ 40 chars and present in the server's table; slot from an allowlist; count an integer in 1..cap; alive and not in a cutscene or trade for equip.
- **Exploit surface:** index-based references (removing one shifts the rest); client-cloned Tools (build Tools from `ServerStorage` on the server at every `CharacterAdded`); selling the same unique twice in one frame (synchronous check-and-remove stops it); every new caller of `add` is a new attack surface.
- **Performance:** cap storage (heavy players hatch thousands; saves and lists grow without bound); virtualise lists past about 200 entries (ui-input-crossplatform.md).
- **Common bugs:** Backpack is wiped on respawn; equipping reparents a Tool from Backpack to the character and breaks cached paths; `Tool.CanBeDropped` left on; deleting unknown item ids at load wipes everyone's copies after a rename (keep the data, skip rendering) `[lihfolk]`; `FindFirstChild` name collisions between an asset and a remote.

## 3. Shop

- **Purpose and data:** soft-currency purchases plus the surfaces that prompt Robux products. Config `{ [key]: { price, currency, grants, limit?, productId?, passId? } }`; saved `Purchases: { [key]: count }` for limits.
- **Split and remotes:** `Buy(key, qty)` for soft currency; `RequestPrompt(key)` so the **server** runs `PromptProductPurchase` after its own checks. Robux grants happen only in `ReceiptService`; pass perks follow data-and-purchases.md.
- **Validate:** key in the server catalogue; qty 1..max; price from server config only; affordability and bag space, then spend and grant with no yield. Limits, "already at max" and policy are checked at prompt time; a paid receipt is never refused for them `[lihfolk]`.
- **Exploit surface:** a "purchase finished" remote; client-sent prices; a restricted player reaching a paid random item through a side pop-up (gate the server prompt path, not the UI).
- **Performance:** fetch prices once per session with `GetProductInfoAsync` and cache; rotating stock comes from `Random.new(dayIndex * 7919 + slot)` so every server agrees without storage.
- **Common bugs:** hard-coded Robux prices (regional pricing shows different numbers); expecting a timed retry after `NotProcessedYet` (redelivery happens on rejoin or the next purchase); a shop timer that restarts on rejoin (banned: derive it from UTC); a product with id 0 prompted.

## 4. Pets, eggs and hatching with odds

- **Purpose and data:** `Pets: { [uid]: { Kind, Lvl?, Paid? } }`, `EquippedPets: { uid }`, `Pity: { [eggId]: n }`, `Index: { [kind]: true }`. Odds tables in shared config so the panel and the roll read one source.
- **Split and remotes:** the server rolls with `Random.new()`. Every client renders every visible player's pets locally (anchored, no physics, one loop). Intents: `Hatch(eggId, count)` or a server-side `ProximityPrompt.Triggered`, `EquipPet(uid)`, `EquipBest()`, `DeletePets({ uid })` (array capped at 100).
- **Validate:** server distance to the egg; count from an allowlist (1, 3, 8 by pass); currency and bag space before rolling; for a paid egg `ArePaidRandomItemsRestricted == false` exactly, fetched at join, failing closed.
- **Odds:** one function computes final weights from base table, luck, pity and already-owned once-items and feeds both the roll and the displayed percentages; luck has one function and one cap; pity counters are saved; odds are shown on every egg, paid or not, which removes the "is this one paid?" grey zone `[lihfolk]`. Treat an odds change as a versioned, announced event.
- **Exploit surface:** choosing or re-rolling the result; equipping by kind name instead of uid; auto-hatch as an idle faucet (same per-roll rate limit as manual); server-hop dupes (session lock).
- **Performance:** follower cost is players × pets × per-pet work: 50 players × 3 pets is 150 models per client per frame. One loop, `workspace:BulkMoveTo`, ground raycasts at a lower rate, far pets at 10 Hz or hidden, one Blender mesh per pet with a far LOD. Never server-side `AlignPosition` pets (one assembly each, ownership churn, jitter) `[lihfolk]` `[community]`.
- **Common bugs:** hand-typed odds labels that drift after a rebalance; pets visible only to their owner (removes the social reason to hatch); a connection per pet; code that waits forever for a streamed-out owner character; an unskippable hatch animation that blocks bulk hatching.

```lua
--!strict
-- unexecuted sketch: one function feeds BOTH the odds panel and the roll
export type Entry = { id: string, weight: number, rare: boolean }
local LUCK_CAP = 8
local function finalWeights(entries: { Entry }, luck: number, pity: number, pityAt: number): ({ number }, number)
	local boost = math.clamp(luck, 1, LUCK_CAP)
	local guaranteed = pityAt > 0 and pity + 1 >= pityAt
	local weights, total = table.create(#entries), 0
	for i, entry in entries do
		local w = if entry.rare then entry.weight * boost elseif guaranteed then 0 else entry.weight
		weights[i] = w; total += w
	end
	return weights, total -- display: weights[i] / total * 100, from this same call
end
local function roll(entries: { Entry }, weights: { number }, total: number, rng: Random): Entry
	local r, last = rng:NextNumber() * total, entries[1]
	for i, w in weights do
		if w > 0 then
			last = entries[i]
			r -= w
			if r < 0 then return last end
		end
	end
	return last -- float edge: the last entry with a non-zero weight
end
```

## 5. Upgrades and rebirth

- **Purpose and data:** `Upgrades: { [id]: level }`, `Rebirths`, `Prestige`. Cost and multiplier formulas live in one shared module so the button shows what the server charges.
- **Split and remotes:** `BuyUpgrade(id, count | "max")`, `Rebirth(count)`. The server derives the multiplier from saved counts; the client never sends it.
- **Validate:** bulk cost in closed form, `cost = base × g^L × (g^n − 1) / (g − 1)`, and `maxN = floor(log(1 + balance × (g − 1) / (base × g^L)) / log g)`, then corrected by an exact check at `maxN ± 1` because of float error `[lihfolk]`. The reset list is explicit, and nothing bought with Robux is on it.
- **Exploit surface:** parallel requests buying several rebirths for one price (no yield between check and reset: the second sees zero); NaN, negative, fractional or string counts; overflow to infinity (clamp every addition).
- **Common bugs:** no immediate save after a rebirth or prestige (the moment a lost save hurts most); formulas typed twice and drifting; an autosave capturing half a reset (do every data change in one synchronous function, then rebuild the world); the exponential wall: with cost growth 1.5 against an additive +0.5 multiplier a 25-rebirth gate takes about 130 hours, and about 3.2 hours at 1.25 `[lihfolk]`. Tune with the wait-ratio rule in economy-and-progression.md and add the second layer before launch, not after.

## 6. Quests and achievements

- **Purpose and data:** `Quests.Completed: { [id]: true }`, `Active: { [chainId]: { Id, Count } }`, daily slots `{ Day, Slots: { { Id, Count, Claimed } } }`, `Achievements: { [id]: tier }`. The current quest is derived (first id in the chain not completed), never stored as an index. Objectives are data: `{ Kind, Target, Amount }`.
- **Split and remotes:** **the client never reports progress.** Server systems that already know the truth call `Quests.report(player, kind, target, n)` (combat kill pipeline, prompt handlers, purchase grants). The only intent is `Claim(id)`. Progress shows through attributes or the private channel.
- **Validate:** claim only when complete and unclaimed; mark, then grant, in one tick. Kill credit comes from server combat code; decide last-hit versus contributor credit once (everyone above 10–20% of max health dealt within a window) and use it for every kill quest.
- **Achievements and badges:** award from the same server path with `BadgeService:AwardBadgeAsync` in `pcall` (50 + 35 × players per minute `[VS]`); the profile is the truth, the badge is a public mirror.
- **Exploit surface:** a progress remote (`QuestProgress:FireServer("Slime", 9999)` is the classic quest exploit `[lihfolk]`); farming one node (per-player, per-node cooldown); shared nodes griefed in starter areas (make collectibles per-player).
- **Performance:** index active objectives by `Kind` so `report` is O(matching quests); coalesce progress pushes.
- **Common bugs:** saved quest index breaks on the first content update; an objective edited in place leaves players at 7 of 5 (new id, or clamp on load); a waypoint aimed at a streamed-out instance (replicate the position); progress reported while the profile is releasing for a teleport; a removed mechanic leaving impossible quests (the feature flag must retire them and swap saved ones) `[lihfolk]`; DoT kills skipping the kill pipeline.

## 7. Daily rewards and playtime rewards

- **Purpose and data:** `Daily: { LastDay, DaysClaimed }`, `Playtime: { Day, Seconds, Claimed: { [tier]: true } }`. Day index `floor((os.time() + OFFSET) / 86400)`; pick the offset so the reset lands in a quiet hour for the main region.
- **Split and remotes:** `ClaimDaily()` and `ClaimPlaytime(tier)`, with no slot or time argument. The server publishes the next reset as a timestamp; players online across the reset get a push, not a stale "claimed" label.
- **Validate:** compare day indexes, never timestamps ("claimed 23 h 59 min ago" bugs); `canGrant` before marking; playtime accumulates per day on the server from session start, paying on active play.
- **Exploit surface:** device clock (never read); asking for a better slot (no arguments); double claim around reset (synchronous: the second call sees `LastDay == today`); rejoining to re-roll a random reward (roll and store when the day starts, not at claim).
- **Common bugs:** rolling 24-hour windows drift later every day until a miss (use a fixed UTC reset) `[lihfolk]`; the window re-opened on every respawn; group or pass bonus fetched inside the claim (yield).
- **Conflict:** LihFolk's worked build resets the streak to day 1 on a missed day and lists a paid streak repair as a variant. House rules forbid retention through punishment: use the cumulative calendar in liveops-quests-retention.md (counts days played, never resets) and sell nothing on a miss.

## 8. Codes

- **Purpose and data:** static list in a server-only module plus an optional live list in one DataStore key refreshed every 5 minutes; per-player `Redeemed: { [code]: true }`; entries `{ reward, expiresAt (UTC), allowedUserIds?, minPlaytime?, globalLimit? }`.
- **Split and remotes:** `Redeem(text)` only. The client never holds the list.
- **Validate:** raw length cap, trim, uppercase, `%w` only, length 3–24; expiry against `os.time()`; one use per player; a per-player `redeeming` guard and a re-check if the path yields.
- **Exploit surface:** reading codes from `ReplicatedStorage`; brute force (token bucket plus a miss lockout by UserId, identical message for unknown and unreleased); alt farms funnelling tradeable code rewards (bind rewards to the account or require playtime); leaked tester codes (check who, not just what).
- **Performance:** a global "first 10,000" limit is a distributed counter: a DataStore key throttles in the first minute after a video, so count in MemoryStore and record in the DataStore; accept slight overshoot `[lihfolk]`.
- **Common bugs:** Studio writes to the live universe's stores, so a test code written from Studio is a real code within 5 minutes; `GetAsync` then `SetAsync` when two people add codes (use `UpdateAsync`); old servers reject a code announced before their refresh (nudge with MessagingService or announce a few minutes late); fixed currency rewards that are worthless or farmable six months on (size as "30 minutes of current income"); expiry shown as a local date (show a countdown). Size every code as if every player redeems it. Campaign design: growth-and-marketing.md.

## 9. Leaderboards (OrderedDataStore, global and per server)

- **Purpose and data:** the profile is the truth; the ordered store is a rebuildable index of integers. Store per board; weekly boards use a new store per week (`Wins_w{floor(os.time() / 604800)}`), never key deletion.
- **Split and remotes:** none client-to-server. The server reads one page per board on a timer and publishes rows through a RemoteEvent or attributes on board models. The "this server" board sorts online profiles every few seconds with no store; a friends board reads friends' saved stats, not the ordered store.
- **Validate:** write with `UpdateAsync`, never lower a monotonic score, floor to integers, skip unchanged values, drop anomalous jumps before they reach the board.
- **Budget** `[VS]`: per server per minute, ordered writes 30 + 5 × players and list pages 5 + 2 × players; page size at most 100 `[official]`. Writing every 120 s when changed plus once on leave uses about 15% of a 20-player server's write budget; stay under half `[lihfolk]`. Every server reads every board, so 500 servers × 2 boards every 2 minutes is 500 list calls a minute against the experience budget: recompute before adding boards. Stagger boards and check `GetRequestBudgetForRequestType` first.
- **Exploit surface:** none of its own; it inherits the economy's integrity. Remove banned users and deletion requests from every board and filter at read time.
- **Performance:** batch names with `UserService:GetUserInfosByUserIdsAsync` and cache; for huge numbers store `floor(log10(value) × 1e6)` and decode for display.
- **Common bugs:** writing on every coin gain; `SetAsync` letting a stale server lower a score; different week formulas in two scripts; Studio sessions writing live boards (separate store name in Studio); prizes granted from a board that is still open (freeze the closed period's store, exclude flagged accounts, then grant through a mailbox).

## 10. Rounds, match state machine and intermission

- **Purpose and data:** one server loop: Waiting → Intermission → Loading → Playing → Results. State lives in memory; only wins and rewards touch the profile. Each minigame is a module with `Start`, `Stop`, `Winners`; maps sit in `ServerStorage`.
- **Split and remotes:** each phase sets two attributes on `ReplicatedStorage`, `RoundState` and `RoundEndsAt = workspace:GetServerTimeNow() + seconds`; clients count down locally, late joiners get the values free, and one replication per phase replaces one remote per second. The loop waits in 0.25 s slices against `os.clock()` so it can end a phase early (one player left alive). Intents: `Vote(mapId)`, `ToggleAfk()`.
- **Validate:** votes against an allowlist while `votingOpen`, tallies published on a 0.5 s tick; eliminations decided on the server only; every transition re-reads the roster at the moment it runs and every waiting state has a timeout.
- **Exploit surface:** a client marking itself alive or finished; flying over hazards (bounds check eliminates, never bans); win farming with an alt (require at least 2 starters and a minimum survived time; consider no rewards in private servers); paying twice when a player leaves on the final tick (a `rewarded` set).
- **Performance:** clone one map per round from `ServerStorage` and destroy it after; call `RequestStreamAroundAsync` before teleporting players in; several arenas in one server means one loop object per arena, not a global loop.
- **Common bugs:** per-round connections never disconnected (a Trove per round); `ResetOnSpawn = true` on the round GUI; a minimum player count that stalls quiet servers forever (lower it after a wait, add bots or a practice mode); undefined late-join state; spawn protection that still lets the protected player deal damage; intermissions over about 30 s on phones `[lihfolk]`.

## 11. Teams, matchmaking, queues and reserved servers

- **Teams:** `Team` instances under `Teams`; `AutoAssignable` evens teams on join only, so rebalance on leave yourself; `TeamColor` must be unique because spawns match by colour; there is no built-in friendly-fire rule, so put it in the damage core `[official]`. Balance by rating or alternating picks from a sorted list; join order stacks teams when friends join together.
- **Do you need a queue?** Roblox's own matchmaking already places players by signals and custom attributes `[official]` (knowledge-base 3.11). Build a queue only for discrete matches with fixed rosters.
- **Data:** a ticket per **party** in a MemoryStore queue or sorted map sharded by mode; ticket state in a hash map (cancel flips state, because items cannot be deleted from the middle of a queue); a match record `{ reservedServerId, roster, mode }` keyed by match id with a short TTL.
- **Split and remotes:** `QueueJoin(mode)`, `QueueCancel()`. One matcher server holds a lease (hash-map `UpdateAsync`, about 15 s); it reads up to 100 tickets `[official]`, validates state, groups, re-adds leftovers **before** removing the batch, writes the match record, then each lobby teleports its own members with `TeleportOptions.ReservedServerId = HttpService:GenerateGUID(false)` (`ReserveServer` and `ReservedServerAccessCode` are deprecated `[VS]`).
- **Validate:** rating read from the server profile; party size against the mode; the match server rejects anyone not on the roster record and never trusts teleport data.
- **Exploit surface:** client-sent rating; the reserved server id leaking to clients (players re-enter finished matches); replaying a finished match for rewards (run record checked at instance start); direct joins to match places (set "Secure within universe only").
- **Performance:** the costs that kill the budget scale with CCU, not with searching players: poll only searching players, publish "N searching" once per cycle from the matcher, read with `waitTimeout = 0`. At 2,000 CCU and 300 searching the pattern costs under 10,000 of 241,000 request units per minute `[lihfolk]`.
- **Common bugs:** every lobby running the matcher (half-matches, double matches); a ticket per member (parties split); no sweeper for states stuck on `matched`; unlimited `TeleportInitFailed` retries; room state keyed by `JobId` instead of `PrivateServerId`; treating `PrivateServerId ~= ""` as "player-owned" without checking `PrivateServerOwnerId`. Limits and teleport rules: data-and-purchases.md.

## 12. Combat (melee, projectiles, validation, lag compensation, status, knockback)

- **Purpose and data:** config per attack `{ damage, reach, minDot, height, hitAt, cooldown, knockback }`; one damage core with ordered "dealt" then "taken" steps; effects as `{ id, source, value, expiresAt, nextTick, stacks }`.
- **Hit model:** choose once.

| Model | Flow | Use for |
|---|---|---|
| Server authoritative | Client sends "I swung"; the server waits until `hitAt` minus clamped one-way latency, then queries its own shape | PvE and casual PvP, with a slightly generous box and a short windup |
| Hybrid | Client runs the same shape for instant feedback and claims targets; the server re-checks rate, existence, reach + tolerance, line of sight, one hit per target per swing | Competitive melee, fast bullets |
| Rewind | As hybrid, checked against a short position history at `now − ping/2 − interpolation`, capped at about 250 ms. Conflict (rewind cap): community threads suggest 300–500 ms `[community]`, LihFolk's melee project clamps at 0.4 s `[lihfolk]`, and the cookbook sketch uses 0.25 s `[house]`. Start at 0.25 s and raise it only when logs show honest claims failing | Shooters; costs memory and complexity |
| Server authority mode `[VS]` | Engine predicts and rolls back | New competitive projects (networking-and-security.md) |

- **Split and remotes:** `Swing(comboIndex)`, `Ability(slot, aimPoint)`, `Guard(held)`, `Dash(direction)`; server to client: reliable damage numbers, unreliable distance-filtered cosmetics. The attacker's client plays its own swing at once; damage numbers wait for the server.
- **Validate:** shape from data queried at hit time (cone = within reach, inside an angle of facing, bounded in Y); dedupe by model per swing (15 parts would otherwise mean 15 hits on R15); re-check alive, weapon and stun after the windup; pace with a token bucket or a "bank" so inputs bunched by a lag spike wait instead of being dropped. Starting tolerance `reach + 4 studs + targetSpeed × 0.2 s`; log claims beyond `reach + 2` to see the real distribution before tightening `[lihfolk]` `[community]`.
- **Damage order:** base → move multiplier → upgrades → conditional traits → **summed** percent buffs → independent multipliers (crit, vulnerability) → clamp; then on the victim: invulnerability → guard or parry → reductions → apply. Sum percent buffs (1 + 0.20 + 0.30 + 0.15 = 1.65) rather than multiplying them, or ten buffs explode. Compare every ability with basic attacks over the same time window `[lihfolk]`.
- **Status effects:** absolute expiry timestamps; modifiers plus one owner that recomputes the stat (`WalkSpeed` has exactly one writer); stacking policy per effect (refresh, extend to a cap, intensity, independent, strongest, per source); one 5–10 Hz loop for all ticks with catch-up capped at 2–3; snapshot DoT damage at application; tag damage kind so reflect cannot trigger reflect; crowd control gets diminishing returns and post-immunity, bosses get scaled or bar-based CC. Store `StunnedUntil` on the **character** in server time: it expires by itself, overlaps merge with `max`, and it cannot survive a respawn `[lihfolk]`.
- **Knockback:** the server decides, the owner applies. Send the vector to the victim's client, which applies the impulse or a short force-limited `LinearVelocity`; the server then validates displacement. Conflict: the `ApplyImpulse` reference says a server call works on parts a client owns through automatic ownership `[official]`; community practice and LihFolk report server impulses on player characters arriving late or not at all. Trust the owner-applies pattern and test your case. NPCs are server-owned, so the server pushes their move goal.
- **Exploit surface:** client damage or target lists trusted as-is; `Touched` on a client-owned weapon; unbounded rewind (hits on players long gone); attacking while dead, stunned or unarmed; kill aura (legit-rate swings after a teleport: needs movement checks); block slow-down and knockback cannot be enforced on a client-owned character outside server authority mode.
- **Performance:** queries only at hit times; ring buffers for history, not `table.remove(samples, 1)`; cosmetic broadcasts filtered to about 300 studs; split the combat code by responsibility before a script nears the 200,000-character source limit `[lihfolk]`.
- **Common bugs:** several damage paths (shields work on swings, not abilities); hit time out of sync with the animation marker (assert `data.hitAt == marker time` in a test); telegraph shape and hit shape differ (one shared shape module); server-played attack animations (the attacker sees them a round trip late).

```lua
--!strict
-- unexecuted sketch: server check of one client-claimed melee hit (hybrid model with capped rewind)
local MAX_REWIND, INTERP_DELAY, TOLERANCE = 0.25, 0.05, 4
type Sample = { t: number, p: Vector3 }
local history: { [Model]: { Sample } } = {} -- ring buffers, 20 Hz, every character root; cleared on removal
local function positionAt(character: Model, t: number): Vector3?
	local samples = history[character]
	if not samples or #samples == 0 then return nil end
	for i = #samples, 2, -1 do
		local a, b = samples[i - 1], samples[i]
		if a.t <= t and t <= b.t then return a.p:Lerp(b.p, (t - a.t) / math.max(b.t - a.t, 1e-3)) end
	end
	return samples[#samples].p
end
local function validateHit(attacker: Player, target: Model, swing: Swing): boolean
	local root = attacker.Character and attacker.Character.PrimaryPart
	local humanoid = target:FindFirstChildOfClass("Humanoid")
	if not root or not humanoid or humanoid.Health <= 0 or swing.hit[target] then return false end
	local rewind = math.clamp(attacker:GetNetworkPing() / 2 + INTERP_DELAY, 0, MAX_REWIND)
	local victim = positionAt(target, workspace:GetServerTimeNow() - rewind)
	if not victim then return false end
	local offset = victim - root.Position
	if offset.Magnitude > swing.reach + TOLERANCE or math.abs(offset.Y) > swing.height then return false end
	if offset.Magnitude > 0.1 and root.CFrame.LookVector:Dot(offset.Unit) < swing.minDot then return false end
	if workspace:Raycast(root.Position, offset, WORLD_ONLY) then return false end -- wall in between
	swing.hit[target] = true
	return true
end
```

## 13. NPC and enemy spawning and AI (pathfinding, state machines, hordes)

- **Purpose and data:** four layers: perception, decision and action on the server, presentation on clients. Enemies are data (`{ health, speed, reach, aggro, leash, attacks, flags }`) driven by one brain; a finite state machine first, weighted attack selection inside Attack, behaviour trees or utility AI only for bosses with many options.
- **Split and remotes:** none from clients. The server sends compact state ("enemy 41 starts Slam at t aimed at P"); clients animate, draw the telegraph and play sound. Gameplay NPC roots are server-owned (`SetNetworkOwner(nil)`), or NPCs near players flip owners and slide differently per client.
- **Pathfinding facts** `[official]`: `AgentRadius` 2 and `AgentHeight` 5 by default; start-to-goal over 3,000 studs fails; computation can fail past 20,000 nodes; `ComputeAsync` can error (use `pcall`). Size agents from the widest collidable part plus 0.5–1 stud, one `Path` per size class. Treat every non-`Success` status as failure and run your own fallback (ranged attack, wait at nearest reachable point, leash home, despawn unseen).
- **Spend fewer paths:** direct movement within about 15–20 studs with a clear shapecast of the agent's radius; a server-wide request queue (for example 20 paths a second) so brains never yield; recompute when the goal moved more than 20% of the remaining distance or every 0.5–1 s; one shared path per pack; a flow field (one breadth-first distance grid) when hundreds share one goal; local steering in open fields `[lihfolk]`.
- **Hordes at scale:** think at 5–10 Hz, staggered, only within about 200 studs of a player; wake and sleep whole areas with hysteresis (for example wake at 160, sleep at 210); global **and** per-area alive caps; pool models. Past a few dozen, drop `Humanoid`: server keeps positions as data (or anchored roots moved by `CFrame`), clients render pooled Blender rigs with `AnimationController` and move them with `BulkMoveTo`. Tower-defence enemies are a distance along a path, not agents. Community reports put the wall for full Humanoid NPCs in the low hundreds even with states disabled `[community]`; measure.
- **Spawn director:** enemy types cost credits (for example fodder 1, ranged 3, tank 8, elite 20); the director earns `base × playerScale × phase × intensity` per second, spends against the alive cap, caps its bank, and cuts the rate for 15–40 s after a peak. Scale earn rate sub-linearly, `1 + k(n − 1)` with k about 0.5–0.7, counting players in the encounter, not the server. Spawn 40–120 studs from the nearest player, out of line of sight, on pre-validated points; a failed spawn refunds credits `[lihfolk]`.
- **Fairness:** at most about 2 attackers per player through attack tokens returned on every exit path (a leaked token makes a pack go passive forever); ring slots at about 0.9 × reach; same-zone and leash rules; a visible alert on aggro; every attack telegraphed with the same shape the server tests, with warnings of at least 0.5 s `[lihfolk]`.
- **Exploit surface:** client-owned NPCs; kill credit from client claims; a dev spawn command left ungated.
- **Common bugs:** `MoveToFinished` awaited forever (per-waypoint timeout); recomputing on any `Blocked` instead of only blocks ahead; velocity-only stuck detection (measure progress over a window); goal at the player's root while they jump (`NoPath`: project to the floor or use the last grounded position); teleporting stuck NPCs in view; a path requested the same frame a wall spawned (wait about 0.5 s).

## 14. Tools and abilities

- **Purpose and data:** ability config `{ id, cooldown, cost, castTime, shape, effects }` with effects as whitelisted ops (architecture-patterns-luau.md, Bytecode); per-player `cooldownUntil[id]` in server memory; loadout in the profile.
- **Split and remotes:** `ActivateAbility(slot, aimPoint)`; `Tool.Activated` carries no aim, so send it yourself. Logic lives in one server service and one client controller, never in scripts inside each Tool. A custom hotbar disables the default backpack UI and equips through a remote.
- **Validate:** slot owned and equipped; cooldown on the server clock with a small grace for latency; resource cost; `aimPoint` finite and within range of the **server's** character position; state checks (alive, not stunned) at request and again after cast time.
- **Exploit surface:** the equipped Tool is part of the client-owned character, so handle position, activation cadence and `Touched` are client-controlled; animation events are never proof of an action. Under server authority mode Tools are not fully supported `[VS]`.
- **Performance:** pooled VFX built per client from one small event (vfx-and-juice.md).
- **Common bugs:** cooldown only on the client; a held weapon welded by the default `RightGrip` cannot be animated (replace with an animatable joint); with the Avatar Joint Upgrade, R15 joints are `AnimationConstraint`s and code looking for `Motor6D` finds nothing `[VS]` (physics-and-vehicles.md); hold-to-attack input that sticks after focus loss.

## 15. Interaction (ProximityPrompt, ClickDetector, zones)

- **Pick the trigger:** `ProximityPrompt` for anything the player chooses to use (it shows the right key hint on every device); `ClickDetector` for dense panels of small buttons (no hint on gamepad); `Touched` only when walking into it is the action; a point-in-volume test for areas.
- **Split and remotes:** prompts fire `Triggered(player)` on the server, so no remote is needed. Zones: the client resolves its own zone for music and lighting; the server resolves zones for safe areas, PvP flags and shop access and mirrors the verdict as an attribute.
- **Validate:** an exploiting client can trigger prompts and click detectors from any distance (networking-and-security.md), so the server re-checks distance (the prompt's `MaxActivationDistance` plus a latency margin, measured to half the object's size), state and a per-player or per-object cooldown.
- **Zones:** invert the question. Ask each player's root "which zone contains me" with a point test in zone space at 2–5 Hz on the server and 5–10 Hz on the client, rather than each zone "who is inside me". Give zones a distinct `Priority` for nesting and grow the current zone by 3–6 studs (hysteresis) so borders do not flicker. Keep zone volumes as data outside Workspace so streaming cannot remove them. Past about 50 zones bucket them in a 2D grid `[lihfolk]`. Per-frame overlap queries are the usual cause of zone-library lag `[community]`.
- **Exploit surface:** a prompt on an unanchored part dragged to the exploiter; a wall as the only gate (enforce by server position checks and send intruders back); client-declared zones.
- **Common bugs:** `TouchEnded` as "left the area" (misses on death and teleport); reward on `Touched` without a debounce (fires once per limb); `RequiresLineOfSight` on a prompt inside a large part (the part blocks its own prompt: host it on an attachment at the handle); default `ButtonX` clashing with an ability; a LocalScript placed under a workspace part (never runs).

## 16. Plots, tycoon ownership and placement

- **Purpose and data:** tycoon: `Tycoon: { Owned: { [buttonId]: true }, Cash, Pending, LastSeen }`; the plot is rebuilt from ids into whichever plot is free. Building: `Placements: { { id, x, y, z, r } }` in **plot-local integer cells** with `r` in quarter turns (0–3) and a format version. About 25–35 characters of JSON per placement, so 400 items is about 12 KB `[lihfolk]`.
- **Split and remotes:** `BuyButton(id)` (a remote, so phone and gamepad players have a UI path; pads use a prompt or a server zone check), `Place(itemId, x, z, rot)`, `Remove(placementId)`. Income is a server tick (`income × dt` once a second), never physical drops; conveyor drops are client-only pooled visuals near the camera.
- **Validate:** ownership of the plot; integers with `v == v`; rotation 0–3; rate and item cap; item owned; bounds, then the occupancy grid, then commit with no yield. Occupancy is the rule; a physics overlap test (box shrunk 0.05–0.1 studs per side) is only for free placement. Walls live on an edge grid, floors and furniture on the cell grid. The server casts its own ground ray; the client's Y is a hint.
- **Exploit surface:** building on other plots; NaN cells passing naive bounds checks; instance bombs (cap per plot and per expensive category); a tower placed at Y = 1000 with range over everything; collecting from another player's collector.
- **Performance:** physical droppers the classic way are about 960 live parts on 8 plots (15 droppers × 1/s × 8 s) `[lihfolk]`; one mesh per placed item; `ModelStreamingMode = Atomic` on placed models; rebuild 20–50 items per `task.wait()`, nearest first, staggered per player; lights on placed items off beyond a distance.
- **Common bugs:** world-space saves (the base lands on someone else's plot next session); assigning a plot on `PlayerAdded` before the profile loads (a failed load strands it); the anchor corner following the cursor (centre the footprint); footprint not swapped on rotation; the ghost hit by its own raycast (`CanQuery = false`); placing on touch release (drag, then confirm); saved placements not revalidated after an update (return failures to the inventory with a message, never delete silently); renaming a button id without a rename map.
- **House rules:** pads, droppers, ghosts and placed items are Blender meshes with real collision; the invisible colliders and zone volumes may be primitives.

```lua
--!strict
-- unexecuted sketch: server side of Place(itemId, x, z, rot); cells are plot-local integers
local function isCell(v: unknown, limit: number): boolean
	return type(v) == "number" and v == v and v % 1 == 0 and v >= 0 and v < limit
end
local function place(player: Player, itemId: unknown, x: unknown, z: unknown, rot: unknown): string
	local plot = Plots.ownedBy(player)
	local def = if type(itemId) == "string" then Catalog[itemId] else nil
	if not plot or not def then return "Invalid" end
	if not (isCell(x, plot.cellsX) and isCell(z, plot.cellsZ) and isCell(rot, 4)) then return "Invalid" end
	local cx, cz, r = x :: number, z :: number, rot :: number
	local w, d = def.w, def.d
	if r % 2 == 1 then w, d = d, w end -- quarter turns swap the footprint
	if cx + w > plot.cellsX or cz + d > plot.cellsZ then return "OutOfBounds" end
	if plot.count >= plot.cap then return "Full" end
	for i = cx, cx + w - 1 do
		for j = cz, cz + d - 1 do
			if plot.occupied[i * 4096 + j] then return "Occupied" end
		end
	end
	if not Inventory.consume(player, itemId :: string, 1) then return "NotOwned" end -- same tick as the checks
	plot:commit(itemId :: string, cx, cz, r) -- marks cells, appends the record, spawns the model
	return "Ok"
end
-- world CFrame = plot.origin * CFrame.new((cx + w / 2) * CELL, 0, (cz + d / 2) * CELL) * CFrame.Angles(0, r * math.pi / 2, 0)
```

## 17. Trading (escrow, two-phase confirm, anti-dupe, audit log, kill switch)

- **Scope ladder** (each step multiplies the bug surface) `[lihfolk]`: no trading, gifting from the shop only → same server, both online, item for item → plus soft currency → asynchronous mailbox with escrow → cross-server marketplace. Premium currency is never tradeable.
- **Data:** a server-owned offer `{ id, a, b, offerA: { uid }, offerB: { uid }, version, state, confirmAt }`; `Lock = tradeId` on every offered item; `PendingTrades: { [id]: { peer, give } }` in each profile; one write-once `Trade_<id>` decision record per trade; `TradeHistory` (last 20) per player.
- **Split and remotes:** small intents only: `Invite(userId)`, `Accept()`, `Add(uid)`, `Remove(uid)`, `Ready(version)`, `Confirm(version)`, `Cancel()`. The client never sends an offer list.
- **Two-phase confirm:** every edit increments `version` and clears both ready flags; `Ready` and `Confirm` carry the version the client saw and are refused on mismatch (kills the last-frame swap scam); both ready starts a 3–5 s countdown with the confirm button disabled; any edit cancels it.
- **Commit:** when both players have confirmed the same version, re-validate from the **profiles**, not the offer, and build the plan (every uid present, locked to this trade, tradable, bags fit). Then run the **two-profile commit protocol in data-and-purchases.md** ("Two-profile commit protocol"): intent saved in both profiles, a write-once decision record, one settle mutation per profile that applies the trade and clears its pending id together, and load-time recovery that writes an abort tombstone before unlocking and stays locked when the record cannot be read. That section is the only specification: it lists the invariant each step protects, the crash outcome after each step, the request cost (5–7 `UpdateAsync` per trade) and what it cannot guarantee. Do not build from this summary, and do not ship without its fault-injection test (server killed between every pair of steps). Items keep their uid across owners.
- **No shortcut is safe for a swap:** "swap in memory and save both at once" duplicates one side whenever a crash, a failed save or a shutdown lands between the two saves, in either order. Use the protocol, or a transaction library such as Lyra (data-and-purchases.md, library status). For a one-way gift, debit the giver and confirm that save before crediting the receiver.
- **Gates, all failing closed:** `IsPaidItemTradingAllowed` for `Paid` items; equal price levels for paid items; unlock requirements that make mules expensive (playtime, level, account age); a per-day cap from young accounts; the `trading_enabled` flag.
- **Exploit surface:** a yield between check and swap; an item consumed elsewhere while offered (one `consume` path checks `Lock`); cross-server "trades" with two leases (make it a mailbox with single-key escrow and call it that); profile released mid-commit (the release path waits for the commit); teleport during a trade (refuse or cancel first).
- **Operations:** append-only audit log covered by deletion handling; nightly uid-collision scan; supply-curve alert (copies of a roll-only item should track rolls × odds); on a dupe, follow "Runbook: dupe incident" in data-and-purchases.md: kill switch first, quarantine (kept, usable, untradeable, flagged) for good-faith holders, removal only from accounts with direct evidence.
- **Common bugs:** a new uid minted on transfer; saving both profiles "soon" through autosave, or "at once" without the protocol; unlocking on an unreadable decision record; unknown policy treated as allowed; a fake fairness meter; the other side's list truncated in the UI.

## 18. Crafting

- **Purpose and data:** recipes `{ id, inputs: { [itemId]: n }, outputs, station?, seconds? }`; a timed craft stores `{ recipeId, readyAt }` as an `os.time()` stamp in the profile, so it survives rejoin.
- **Split and remotes:** `Craft(recipeId, count)`, `Collect(slot)`. Gathering is a server prompt or hit on tagged nodes carrying `Resource`, `Yield` and `MaxHealth` attributes.
- **Validate:** recipe allowlist; count 1..max; station distance; check **all** inputs and output space, then remove all and add, in one tick; node distance includes half the node's size so large nodes are reachable.
- **Exploit surface:** client-decided yield or recipe; ingredients removed one by one around a yield; crafting from across the map; an offered or equipped item used as an input (the `Lock` check in `consume`).
- **Performance:** nodes are depleted through attributes and visibility, not destroyed and re-created; per-player node cooldowns in busy starter areas.
- **Common bugs:** inventory going negative under an autoclicker; a craft timer that restarts on rejoin; the UI showing a recipe the server will refuse (derive "can craft" from the same shared function).

## 19. Stealing and base defence

- **Purpose and data:** per base `{ owner, lockedUntil, slots: { uid } }` in server memory; per player `Carrying: uid?`, newcomer shield end and per-victim cooldowns. Stolen items move between two profiles, so this is a trade without consent: it uses the same two-profile commit protocol as section 17 (data-and-purchases.md).
- **Split and remotes:** `LockBase()`; `StartSteal(slot)` begins a server-timed hold (prompt `HoldDuration` plus a server timer); `Deposit()` happens by server zone check at the home base. `lockedUntil` replicates as a `GetServerTimeNow` timestamp and clients draw the countdown.
- **Validate:** base unlocked on the server clock; distance and line of sight at the start **and** end of the hold; one carried item; carrier speed applied through the single WalkSpeed owner; deposit only inside the home zone; owner offline means the base is not stealable (genres/steal-and-defend.md).
- **Exploit surface:** teleport-to-base and back, speed and fling are the genre's main load: run the carrier checks from physics-and-vehicles.md, drop the item back on violation, and consider server authority mode. A client "I stole it" event; auto-lock macros (rate-limit, cooldown on the server clock).
- **Performance:** the base board (owner, lock time, top item) is three attributes, not a per-frame remote.
- **Common bugs:** the item existing in both profiles after a mid-carry disconnect (move it at deposit, not at pickup; the carried state is memory only); a lock timer kept as a client countdown; newcomer shield stored per session instead of lifetime playtime. House rules: no steal speed, stun or lock length sold for Robux; no offer fired on being robbed.

## 20. Checkpoints and obby stages

- **Purpose and data:** four separate facts: `Current` (where I respawn), `Furthest` (never decreases; gates travel), `Clean` (no skips this run; gates the speedrun board) and `SkipCredits` (bought, not yet used) `[lihfolk]`.
- **Split and remotes:** `TravelToStage(n)`, `UseSkip()`. Progress comes only from server-validated pad contact, never from a "reached stage N" remote. Timing uses the server's `os.clock()` between its own events.
- **Validate:** stage is `Furthest + 1`; the character is alive (a ragdolled body sliding onto a pad must not advance); the server-side position is within a few studs of the pad (about 6); a minimum plausible segment time per stage; travel only to `≤ Furthest`.
- **Exploit surface:** teleporting pad to pad (order plus minimum time makes it worthless, see physics-and-vehicles.md); client timers; a skip product consumed without a saved credit.
- **Performance:** save every N stages (for example 5) with a minimum gap, not on every pad; `RequestStreamAroundAsync` before moving a player to a far stage, and keep checkpoint platforms persistent.
- **Common bugs:** merging `Current` and `Furthest` (going back to help a friend costs 80 stages); a rejoin spawning over an unloaded stage in a fall-die loop; kill parts connected once at startup under streaming (bind by tag); inserting a stage mid-chain without a remap (append, remap by version, or save stable stage ids); reducing the stage count without a remap.

## 21. Party and friends features

- **Purpose and data:** friend-join detection, friend boosts, party teleports, invites. No saved data beyond what rewards grant.
- **Split and remotes:** `InviteFriends()` opens `SocialService:PromptGameInvite` on the client after `CanSendGameInviteAsync`. The server reads `player.FollowUserId`, `Player:IsFriendsWithAsync` and `Player.PartyId` with `SocialService:GetPartyAsync(partyId)` for members across servers `[official]` `[VS]`.
- **Validate:** friendship and party membership are checked on the server at join and cached; friend-boost count is "friends currently in this server", recomputed on join and leave, capped (house cap: counts toward the multiplier stack in economy-and-progression.md).
- **Group teleports:** one `TeleportAsync` moves only players in this server; to gather a spread party, reserve one GUID, store a gather record in MemoryStore, and let each source server teleport its own members. The destination holds an arrival barrier with a deadline rather than starting on the first arrival; `GetJoinData().Members` lists only the same call's group `[lihfolk]`.
- **Exploit surface:** teleport data trusted for party membership; alt accounts farming a friend-join reward (grant once per pair, require playtime from the joiner).
- **Common bugs:** party bigger than the mode's capacity; two members pressing Start at once (a short lock key per party); assuming every member may join every server type (age and privacy settings differ); teleports never tested outside Studio, where they do not run. Design rules for social rewards: liveops-quests-retention.md.

## 22. Chat commands and admin tools

- **Purpose and data:** one server registry of commands, each with a capability; roles are sets of capabilities resolved on the server at join (owner, explicit developer UserIds, group roles). An audit entry for every attempt, allowed or denied.
- **Split and remotes:** front ends only translate: `TextChatCommand.Triggered` (a matched command message is intercepted and not shown to other users `[official]`), an admin panel remote `(name, args)`, console helpers. All call the same registry, so the capability check and the log cannot be skipped.
- **Validate:** fail closed when a group lookup errors (use `GroupService:GetRolesInGroupAsync`; `GetRankInGroupAsync` is deprecated `[VS]`); targets by UserId from the panel, unique-prefix match from chat with ambiguity refused; no peer or superior targets; destructive and economy commands need a two-step token confirmation within 30 s; economy commands are developer-only, capped per call and per day, ledgered, and off in production by default `[lihfolk]`.
- **Exploit surface:** client-side rank checks; a leftover test remote that grants currency (the most common real admin exploit); Creator Store copies of admin systems carrying `require(id)` backdoors (house rule: no Toolbox code; take libraries from the author's repository, pinned and read).
- **Performance:** buffer audit entries and flush every 30–60 s and at shutdown in one write.
- **Common bugs:** dev commands reachable in live servers because the gate was `IsStudio()` in the wrong place; logs lost on shutdown; bans issued by kick loops instead of `Players:BanAsync` (networking-and-security.md); raw chat text stored in logs.

## 23. Time and day cycle

- **Purpose and data:** game time is a pure function of server time: `clock = ((workspace:GetServerTimeNow() + offset) / DAY_SECONDS % 1) × 24`. Nothing is saved; an `offset` attribute lets live-ops move the sun.
- **Split and remotes:** none. Each client sets `Lighting.ClockTime` every frame or two from the shared formula, so all clients agree without messages and the motion is smooth; a server-driven `ClockTime` replicates in visible steps `[community]`. The server evaluates the same formula for gameplay (night spawns, shop hours).
- **Validate:** anything with consequences reads the server's value.
- **Exploit surface:** a client can light its own world however it likes; darkness must never be the only thing hiding gameplay information.
- **Performance:** one priority stack owns Lighting (zones, weather and events push overrides onto it) so two systems never tween the same property; shadow updates at dawn and dusk cost most on phones: lengthen the day or step the sun at low quality (lighting-and-atmosphere.md).
- **Common bugs:** tweening across the 24 → 0 wrap backwards; a per-server clock that makes friends in two servers disagree about "night"; weather decided per client when it affects grip or visibility.

## 24. Server-wide events and boosts

- **Purpose and data:** a boost is `{ kind, multiplier, endsAt, activator }`. Scope decides storage: this server only → server memory plus attributes on `ReplicatedStorage`; every server → one MemoryStore key with a TTL as the truth, plus a MessagingService nudge so servers re-read at once. New servers read the key at start; all servers re-poll every 30–60 s because messaging is best effort `[community]`.
- **Split and remotes:** none from clients. A purchase arrives through `ReceiptService`; an admin start goes through the registry in section 22. Clients read `kind` and `endsAt` attributes and draw the pill and countdown.
- **Validate:** same-kind boosts extend the end time up to a cap and never multiply; the multiplier applies in server reward code only; scheduled events are derived from UTC so every server agrees; a paid server boost is recorded with its `PurchaseId` before it starts.
- **Exploit surface:** MessagingService payloads are untrusted input (validate like a remote; receivers re-read the authoritative key); luck boosts are probability modifiers, so paid ones fall under the paid random item rules (show boosted odds live, gate by policy).
- **Performance:** one key and one message per change; never per-player messages.
- **Common bugs:** a boost that restarts when the buyer rejoins; a server that started after the announcement and never learns of the boost; a countdown reset by a redelivered receipt.
- **Personal boosts:** a personal paid boost is saved as remaining play seconds in the profile, ticked down by the server only while the player is online (it pauses offline) and mirrored to the client as an `endsAt` attribute recomputed at join; the `ReceiptService` sketch in data-and-purchases.md and the Boosts module in monetization-and-policy.md follow this. Server-wide boosts run in real time and show their end time. The product card states which.
- **Conflict:** LihFolk's library stores timed boosts as a real-time `os.time()` expiry, while its own status-effects note argues that anything bought with Robux should pause offline `[lihfolk]`. House ruling: personal paid boosts count play time; server-wide boosts run in real time.

## Build order by genre

Foundation for every genre, in order: DataService → RemoteGuard and Net → Wallet → Inventory → Shop and ReceiptService → analytics events (analytics-and-discovery.md).

| Genre | First playable | Before soft launch | After first retention read |
|---|---|---|---|
| Simulator, incremental, +1 | Core verb earn tick, Upgrades (5) | Rebirth (5), Pets (4), Zones and gates (15), Daily (7) | Quests (6), Leaderboards (9), Boosts (24), Codes (8), Trading (17) only with a team to run it |
| Pet collection, RNG | Hatch with odds (4), Inventory (2) | Index, Luck and pity (4), Daily (7), Quests (6) | Trading (17), Server luck (24), Leaderboards (9) |
| Tycoon, cozy management | Plots and income tick (16) | Rebirth (5), Offline income, Placement (16) | Friends visits (21), Quests (6), Events (24) |
| Obby, tower | Checkpoints (20) | Stage saves and skips (20), Speedrun board (9) | Rounds (10) for tower modes, Daily (7) |
| Round minigames, horror co-op | Round loop (10), Teams (11) | Map voting, Spectate, NPC AI (13) for horror | Queues and reserved servers (11), Party (21) |
| Fighting, battlegrounds, shooter | Combat core (12), Tools (14) | Status effects (12), Rounds (10), Anti-cheat checks | Ranked queue (11), Leaderboards (9), server authority mode |
| RPG, dungeon | Combat (12), NPC AI (13), Inventory (2) | Quests (6), Crafting (18), Spawn director (13) | Party and reserved dungeons (11, 21), Trading (17) |
| Tower defence | Path-distance enemies and placement (13, 16) | Wave data and balance sheet, Lobby → reserved match (11) | Units gacha (4), Leaderboards (9) |
| Steal and defend | Base income (16), Lock and steal (19) | Carrier movement checks, Rebirth (5) | Events (24), Friends defence (21) |
| Roleplay, social | Interaction (15), Tools (14) | Housing placement (16), Day cycle (23), Vehicles (physics-and-vehicles.md) | Party (21), Admin tools (22) |

Admin tools (22) and the kill switches ship before the first public test in every genre.

## Level-up: symptom → cause → fix

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| Impossible balances or items | A remote carries an amount, or a check and its write are separated by a yield | Wallet and Inventory as the only mutators; intents only; synchronous check-and-write (0, 1, 2) |
| "I claimed it and got nothing" | Marked before a grant that failed, or a bag-full partial grant | `canGrant` then mark-and-grant in one tick; refuse free rewards into a full bag (0) |
| Odds on screen differ from results | Labels typed by hand, or luck applied in two places | One weights function for display and roll (4) |
| Dupes after trades or steals | Two saves with a crash between; item consumed while offered | Locks through one `consume`; the two-profile commit protocol and the dupe incident runbook in data-and-purchases.md (17) |
| Quests completed instantly | A progress remote | Server-only `report`; claim as the only intent (6) |
| Leaderboard throttles or shows stale or lowered scores | Write per change; `SetAsync`; too many boards per server | 120 s changed-only writes, `UpdateAsync` monotonic, budget table (9) |
| Servers stuck on "Waiting for players" | No timeout; roster not re-read when someone leaves | Timeouts and re-evaluation on every transition (10) |
| Server slows after hours | Per-round or per-character connections leak; NPC tokens leak | Trove per round; tokens returned on every exit path (10, 13) |
| "My hits don't register" on mobile | Server checks current position with a tight box, or drops bunched inputs | Latency-clamped hit timing, tolerance, bank pacing; log claim distances (12) |
| Players hit "outside the circle" | Telegraph and hit shape come from different data | One shared shape module (12, 13) |
| Slow never wears off, speed restores wrong | Several systems write `WalkSpeed` | Modifiers plus one owner (12) |
| NPCs freeze in groups or lag the server | Path per NPC per tick; brains every frame | Request queue, direct mode, shared paths, 5–10 Hz staggered thinking (13) |
| Bases appear on the wrong plot or lose items after an update | World-space saves; no revalidation on load | Plot-local cells; revalidate and return failures to inventory (16) |
| Crowded servers lag with no hot script | Bulky per-player state in Player attributes; pets simulated on the server | Owner-only channel; client-rendered pets (0, 4) |
| Codes "invalid" for some players | Old servers have not refreshed; case or spaces | 5-minute refresh plus messaging nudge; normalise input (8) |
| Boost vanished or restarted on rejoin | Stored in memory, or as a client countdown | Personal boost saved as remaining play seconds, server-wide boost as a real-time end; attributes from server time (24) |
| Staff abuse or unexplained grants | Client rank checks, no audit, leftover test remote | One registry, capabilities, audit log, flags off in production (22) |

## Review gate

- [ ] Every system has a decisions table, an exploit table and has passed the seven-step test list.
- [ ] No remote carries an amount, price, result, score, progress count, time or another player's id.
- [ ] No yield between any check and the write it guards; web facts are cached at join.
- [ ] Grants are all-or-nothing; paid receipts are never refused for limits or a full bag.
- [ ] Content is referenced by stable ids, unique items by GUID; nothing saved is world-space or index-based.
- [ ] Countdowns replicate as end timestamps; day logic uses UTC day indexes; no client clock anywhere.
- [ ] Odds shown and odds rolled come from one function; paid random items are policy-gated and fail closed.
- [ ] Trading, gifting, codes and events each read a Configs kill switch; trading has version-checked two-phase confirm, item locks, the two-profile commit protocol with its fault-injection test passed, and an audit log.
- [ ] NPC roots are server-owned; AI thinks at 5–10 Hz behind a path budget; alive caps are global and per area.
- [ ] Private or bulky player state does not replicate to other clients.
- [ ] Admin and debug commands sit behind a server capability check and a production-off flag; test remotes are removed.
- [ ] House rules hold: no loss sold back (streak repair, robbed-offer), no stat power for Robux in competitive modes, every visible object is a Blender mesh with collision.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/characters/pathfinding.md`, `players/{teams,leaderboards}.md`, `matchmaking/index.md`, `workspace/collisions.md`, `reference/engine/classes/{ProximityPrompt,ClickDetector,TextChatCommand,BadgeService,OrderedDataStore,MemoryStoreQueue,TeleportOptions,SocialService,Player,Players,GroupService,PolicyService,BasePart,Workspace}.yaml` (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/lihfolk-systems/SKILL.md`, `skills/roblox-system-builder/SKILL.md`; `24 Worked Builds/` (Saved Inventory, Pet Hatching and Following, Melee Combat System, Round-Based Minigame Loop, Global Leaderboards, Codes Redemption System, Daily Rewards System, Rebirth and Prestige System, Quest Chain System, Shop with Game Passes and Developer Products, Weekend Build - Survival Gather, Craft and Place); `09 Gameplay Systems/` (Combat Systems Architecture, Hitboxes and Hit Detection, Status Effects Buffs and Stacking Rules, NPC AI and Behaviour, Pathfinding, Pathfinding Edge Cases and Fallbacks, Spawn Director, Spawning Teams and Rounds, Tools and Inventory Systems, Clickable and Interactive Parts, Zone Detection); `43 Genre Systems End to End/` (Tycoon Plots and Droppers, Tower Defense Waves and Placement, Obby Checkpoints and Stage Saves, Racing Laps and Checkpoints); `41 Multiplayer Services/` (Matchmaking Queues with MemoryStore, Parties and Group Teleports, Reserved and Private Servers in Practice); `04 Data and Persistence/Trading Systems Without Duplication.md`; `06 World Building and Art/Grid Placement and Player Building Systems.md`; `22 Anti-Exploit and Security/Admin Commands Done Safely - Permissions and Audit Logs.md`; `56 Field Notes/Server-Authoritative Freeze and Stun Timestamps.md`; `32 Case Studies of Top Roblox Games/Case Study - Steal a Brainrot.md` (read; its `.luau` files were not copied)
- Combat and lag compensation (search summary): https://devforum.roblox.com/t/am-i-doing-hitbox-replication-right/4773807, https://devforum.roblox.com/t/server-sided-hit-detection-with-lag-compensation/3322386, https://devforum.roblox.com/t/lag-compensation-for-latency-dependant-combat-game/3251761
- Trading and dupes (search summary): https://devforum.roblox.com/t/preventing-duping-methods-in-trading/2688896, https://devforum.roblox.com/t/how-do-i-prevent-duping-in-trading-system/3174956, https://devforum.roblox.com/t/session-locking-explained-datastore/846799
- NPC scale (search summary): https://devforum.roblox.com/t/how-to-optimise-hundreds-of-humanoids/1760085, https://devforum.roblox.com/t/humanoidenemy-optimisation/4804990, https://devforum.roblox.com/t/any-optimalization-tips-managed-about-1500-npcs-mostly-without-lag/284180
- Pets, placement, zones (search summary): https://devforum.roblox.com/t/how-to-make-a-very-optimized-pet-follower/3235258, https://devforum.roblox.com/t/plot-saving-system/2935482, https://devforum.roblox.com/t/creating-a-furniture-placement-system/205509, https://devforum.roblox.com/t/zoneplus-v320-construct-dynamic-zones-and-effectively-determine-players-and-parts-within-their-boundaries/1017701, https://devforum.roblox.com/t/quickzone-v110-60-fps-with-1m-zones-ultra-fast-zoneplus-simplezone-alternative/4369336
- Leaderboards, matchmaking, boosts, day cycle (search summary): https://devforum.roblox.com/t/ordered-datastores/3683582, https://devforum.roblox.com/t/conceptual-implementation-building-a-custom-matchmaking-service-with-memorystore/3652856, https://devforum.roblox.com/t/universescriptservice-that-interact-with-all-servers/3232249, https://devforum.roblox.com/t/synchronize-daynight-cycle-on-client-without-remote-events/2095004, https://devforum.roblox.com/t/how-to-make-a-daynightcycle-with-workspacegetservertimenow/2773629
- Steal genre mechanics (search summary; third-party player guides, timer values disagree): https://driffle.com/blog/how-to-steal-in-steal-a-brainrot/, https://allthings.how/steal-a-brainrot-roblox-efficient-stealing-events-and-rebirths
- GitHub repository search (read: listing metadata only; repository contents not opened): `1ForeverHD/ZonePlus` (MIT, last push 2024-07), `LDGerrits/QuickZone` (MIT, 2026-11), `ahmicy/simplepath` (MIT, 2026-06), `text21/Rewind` (no licence listed, 2026-01)
- Not reachable: devforum.roblox.com, reddit.com and create.roblox.com directly (search summaries only); per-repository GitHub API. No evidence found: a published post-mortem of a trading dupe with the journal protocol measured in production; an official statement on the Humanoid count a server can sustain.
