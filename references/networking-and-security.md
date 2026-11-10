# Networking and security

What this is: the remote design rules, the threat model, the server-side guard, and the anti-cheat, ban, backdoor and credential practices for a Roblox game. Open it when designing a network surface, or jump to "Level-up audit" for a live game that is being exploited or has never been reviewed. Distilled from knowledge-base sections 4.4 and 4.5; platform facts re-checked against `Roblox/creator-docs` on 2026-11-10. Every client-to-server remote in a shipped game goes through the guard in this file. Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

Contents: Start here by level · The three remote types · Designing the network surface · Threat model: what an exploiting client can always do · Exploit landscape · Server authority mode · Threat modelling: procedure and walkthroughs by system · Validation layers · Remote guard and rate limiter · Remote review procedure · Movement and combat checks · Detection, honeypots and consequences · Ownership, access control and third-party code · HttpService and secrets · Backdoors, plugins and team hygiene · Level-up audit · Security review gate · Sources

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | (1) Server code lives in ServerScriptService, never in a replicated container. (2) A remote says what the player wants; the server looks up price, damage and reward. (3) Every handler checks type and range (use `RemoteGuard`). (4) Paid items are granted only in the receipt handler. (5) Run sketch C before publishing | Movement detection, device trust, server authority |
| Intermediate | Threat-model each system before building it; a remote manifest checked at start-up; a busy lock on every handler that moves value; the movement loop with one exemption helper; honeypot plus suspicion score; least-privilege roles and CI keys | Aim statistics, canary rollouts |
| Expert | Lag-compensated reach with a clamped rewind; detectors rolled out shadow → sample review → canary → enforce, with measured precision; fuzz and race harness in CI; server authority for competitive cores; evidence records and an appeals queue | Nothing: read it all |

Terms: a *remote* is a RemoteEvent, UnreliableRemoteEvent or RemoteFunction. A *handler* is the server function connected to it. *Intent* is what the player asks for; *outcome* is what the server decides. A *yield* is any point where a function pauses (`task.wait`, any `...Async` call, `WaitForChild`).

## The three remote types

| | `RemoteEvent` | `UnreliableRemoteEvent` | `RemoteFunction` |
|---|---|---|---|
| Delivery | Guaranteed | Best effort | Guaranteed with response |
| Order | Ordered, including across RemoteEvent instances, per connection and direction | None | Not ordered relative to RemoteEvents |
| Size | Large, keep small | Payloads over 1,000 bytes are dropped | Large |
| Use | All intents and state changes | Replaceable high-frequency data (aim, cosmetic positions) | Client asks server for data via `InvokeServer` |

Rules:

- **Never use `RemoteFunction:InvokeClient`.** A client that never returns yields the server thread forever. Have the client fire a RemoteEvent instead.
- `OnServerInvoke` is assigned once (the last assignment wins silently). Return small tables such as `{ ok = false }` for rejections.
- Ordering is about handler start, not completion. Handlers that yield must tolerate interleaving (per-player busy flag or queue).
- Engine throttle is about 500 requests per second per client per remote type; excess reliable events are delayed, unreliable ones dropped. It protects Roblox, not your game.
- Connect server handlers in `Init`, before clients can fire. Messages with no handler queue and are then discarded.
- The first parameter of every server handler is the `Player` who fired. That is the only trustworthy argument. Ignore any player or userId the client sends.

Serialisation: functions arrive as `nil`; metatables are stripped; mixed tables and `nil` holes misbehave; non-string keys become strings; Instances arrive only if the receiver can see them (`ServerStorage` or streamed-out parts arrive as `nil`); exploiters can send tables shaped like Instances, so check `typeof(x) == "Instance"`; numbers can be NaN or infinite; strings can be megabytes long or invalid UTF-8.

## Designing the network surface

- One remote per intent, named for what the player wants (`RequestPurchase`, `ActivateAbility`), carrying **intent, not outcome**. `SetPosition(cframe)`, `AddCoins(500)` and `DealDamage(target, 50)` are wrong.
- Server-to-client: replicate state through attributes and properties (late joiners see them); use events only for transient things ("play hit effect here").
- The server is a gatekeeper, not a relay. Never forward one client's payload verbatim to others.
- A shared `Net` module defines remote names and payload types; server code connects through the guard; client code calls typed wrappers.
- Private per-player state: attributes on the `Player` or the character replicate to everyone. Send owner-only data with `FireClient` deltas coalesced per tick, or write attributes on a disabled `ScreenGui` (`ResetOnSpawn = false`) inside that player's `PlayerGui`, which only the owner receives `[lihfolk]`. `leaderstats` is public by design.
- Interest filtering: send per-hit effects and entity updates only to players near enough to see them (tiers in performance.md). It is also security: what never reaches a client cannot be read by an exploiter.
- Batch and coalesce high-frequency updates into one packed event per Heartbeat or every N frames. Deltas on reliable remotes only; absolute values on unreliable remotes.
- Attributes as replicated state: `SetAttribute` on the server replicates to clients with the instance. `[VS]` Only the first 64 attributes replicate, names at most 50 characters, string values at most 50 characters. Attributes are public to every client that has the instance; never put private state there.
- Generated networking (Blink or Zap) packs data into `buffer`s and validates structure, not game rules. Worth it for shooters, large simulations and ECS games; a typed wrapper plus the guard is enough for a simulator or obby. Sync handlers must never yield or error; default to `SingleAsync` / `ManyAsync`. Pin versions and commit generated files `[VS]`.
- Test with Server & Clients playtests (up to 8 clients), the Network Simulator (latency, jitter, packet loss) and the Developer Console network stats.

## Threat model: what an exploiting client can always do

Read all replicated code (including disabled scripts); control its character and every part it owns (teleport, fly, noclip, NaN CFrames, fling others); fire `Touched` for owned parts; trigger `ProximityPrompt`s, `ClickDetector`s and `DragDetector`s from any distance (only `Triggered` has a server distance check; `ClickDetector` has none); fire any remote with any arguments at any rate; change its local DataModel; teleport to any place in the universe unless restricted.

It cannot read or change `ServerScriptService` or `ServerStorage`, change server-side properties directly, or call server-only APIs.

For each new feature ask: what happens if this remote is fired 1,000 times per second, with garbage arguments, with another player's objects, from across the map, while dead, during a round transition?

## Exploit landscape, late 2026 `[VS]`

- Hyperion (Byfron) is anti-tamper on the Windows client: it raises the cost of injection and bans in waves; it does not make any client trustworthy `[community]`. Executor sites still advertise working desktop and mobile tools `[community: vendor claims, unverified]`. No official per-platform coverage matrix was found. Roblox's own wording: the built-in anti-cheat "detects exploits after a player joins", and exploits that rely on weak server validation "still work on trusted devices" `[official]`. Plan as if executors exist on every platform.
- The server cannot tell whether a remote came from your LocalScript or an executor `[community]`. Do not try to detect the tool; validate the request.
- Still possible for an exploiting client `[official: security docs]`: fire any remote; decompile every replicated LocalScript, client-context Script and ModuleScript, including disabled and never-required ones; teleport its character and anything it owns; change `WalkSpeed` locally with nothing visible to server-side property reads; play arbitrary animations and manipulate animation state; alter its own collision; replicate NaN or infinite CFrames and extreme velocities to fling other players; suppress or fake `Touched`; teleport itself to any place in the universe (hiding a place's Join button does not block this, and a kick on arrival comes after content has replicated).
- Consequences for tools and animations `[house, follows from the above]`: an equipped tool is part of the client-owned character, so handle position, activation cadence and `Touched` are client-controlled; animation markers and track state are never proof that an attack happened. Time attacks on the server clock and recompute hits from the server's view.
- Duplication and trading exploits are data-layer bugs (rejoin races, rollback after a failed save, non-atomic two-profile writes, double-processed receipts), not network ones. See data-and-purchases.md.

## Server authority mode `[VS]`

Status: Early Access (October 2025), Studio beta (December 2025), client beta (spring 2026), then a DevForum "[Full Release]" post announcing it for all games and a Roblox newsroom post dated July 2026 `[community: search summaries; months inferred from thread order]`. Conflict: `scripting/security/network-ownership.md` in the docs still says "currently in beta", while `projects/server-authority/index.md` has no beta notice. Re-check before committing.

- Enable with `Workspace.AuthorityMode = Server`. It forces `NextGenerationReplication`, `PlayerScriptsUseInputActionSystem`, `SignalBehavior = Deferred`, `UseFixedSimulation` and `StreamingEnabled` `[official]`.
- What it removes: fly, speed, teleport and fling as classes. Clients report inputs only; the server simulates; clients predict and roll back on misprediction.
- What it demands `[official]`: core logic in a shared ModuleScript bound with `RunService:BindToSimulation`; simulation inputs through the Input Action System (InputContexts parented under the Player), still sanity-checked; custom state in attributes (first 64, names and string values ≤ 50 characters); no `Destroy` or reparenting inside the simulation; Tools are not fully supported yet (weld a Model and track "equipped" in an attribute); look tracks up with `Animator:GetTrackByAnimationId()` each frame rather than caching them; effects run outside the simulation and must be reversible.
- What it does not remove: remote validation, economy exploits, backdoors. RemoteEvents are still needed and are not ordered against property and attribute updates.
- Use it for competitive FPS, racing, sports and fighting games. For simulators, tycoons, obbies and social games, client ownership plus the checks below is enough `[house]`. Retrofitting a live game means rewriting the movement and combat core: do it in a separate test universe, never in place.
- Cost: more server CPU. Optimise first; Extended Services for Compute is the paid fallback (see performance.md).

## Threat modelling: procedure and walkthroughs by system

Run this for each system before building it, and for each existing system during an audit (30–60 minutes each). Procedure adapted from `[lihfolk]`; the walkthrough table is `[house]`.

1. **Assets.** List what is worth stealing or breaking in four groups: player value (currency, items, ranks), paid value (products, passes), experience quality (fair matches, server stability), secrets (unreleased content, admin lists). For each, write where the truth lives and which server function may change it.
2. **Trust boundaries**, the points where less-trusted data enters: client → server (remotes, `Touched`, prompts, ClickDetectors, DragDetectors, owned physics, character position); this server → saved data → every future server; HTTP and webhooks; receipts; admin tools; third-party code and plugins.
3. **Questions per boundary** (STRIDE): can someone act as another player or an admin (spoofing), change a value they should not (tampering), deny what happened because nothing was logged (repudiation), learn what they should not (information disclosure), make the server or other players suffer (denial of service), gain a capability they did not earn (elevation)? Add two Roblox questions. Race: what if this request arrives twice in one frame, again after a crash, or from two servers? Physics claim: does this trust anything the owning client simulates?
4. **Write each threat as one sentence in attacker terms**: "A player sends quantity NaN to SellItem; the balance becomes NaN and saves."
5. **Score** Impact, Reach, Ease and Stealth from 1 to 3. Risk = Impact × Reach × (Ease + Stealth), range 2–54. Persistent, wide and quiet threats outrank loud ones: a stealthy dupe scores 3 × 3 × (2 + 3) = 45, a visible fly hack 1 × 2 × (2 + 1) = 6, whatever players complain about most.
6. **Design fix before detector.** Most top threats vanish when the server computes the value. Trivial fixes (a type check, moving a module) are done on the spot, not scored.
7. **Record** one row per threat plus the remote manifest (below). Accepted risks get a reason and a log line. Put audit logs on the high-stealth rows first.

| System | Truth lives in | Worst threats (attacker terms) | Design fix | Signal to log |
|---|---|---|---|---|
| Soft-currency shop | Profile; prices in a server module | Sends a price, or quantity −1, 0.5 or NaN; fires Buy 50 times in one frame | Item id only; server price; integer ≥ 1; deduct before granting with no yield | Spend per minute; rejected arguments |
| Random rolls with luck boosts | Profile (balance, boost expiry); odds on the server | Sends its own luck multiplier; many rolls pass one balance check; datamines odds | Luck read from the profile; deduct-then-roll in one synchronous block; publish the odds (policy requires it for paid random items) | Rolls per minute against the maximum; rarity distribution per account |
| Trading | Both profiles plus a trade record | Edits the offer after the other side confirmed; trades away then rolls its own save back; same item in two trades | Server-owned offer; any edit clears both confirmations and restarts a 3–5 s countdown; one busy lock shared by trade, sell and equip; commit pattern in data-and-purchases.md | Trade ledger with item GUIDs; one GUID in two inventories |
| Melee and ranged combat | Server memory (health, cooldowns) | Claims hits across the map; ignores cooldowns; fires from a fake origin; hits 30 targets per swing | Intent and target only; server-stamped cooldowns; server origin; reach, line of sight, target cap, damage-per-second backstop | Distance ÷ reach of accepted hits; claims per second; reject reasons |
| Position as the prize (obby, race, capture point) | Server checkpoints | Teleports to the finish; flies over gates | Ordered checkpoints with minimum segment times; server zone gating; server authority for ranked modes | Segment times under the floor; rubber-band count |
| Tycoon, plot, placement | Profile plus server plot state | Builds on another player's plot, outside bounds or overlapping; spams placement to lag the server | Owner from the server's plot map; snap, bounds and overlap checked on the server; instance cap per plot | Placement rejects per player |
| Inventory, pets, equip | Profile | Equips an item it does not own or more than the slot cap; equips mid-trade | Look up by item GUID in the sender's own inventory; server slot count; shared busy lock | Equip rejects |
| Leaderboards | Ordered store written from the profile | Every exploit above ends up here; absurd values | Write server-computed stats only, clamped; hold flagged accounts off boards | Gain per interval above the theoretical maximum |
| Daily rewards, codes, referrals | Profile timestamps | Claims on two servers at once; farms codes on alts and funnels by trade | Mark the claim in the session-locked profile before granting; `os.time()`; untradeable or low-value rewards; invitee must reach real activity | Redemptions per code per hour |
| Admin commands | Server registry and allowlist | Rank checked on the client; a failed group lookup grants access; uncapped `give` | Server `can(player, command)`; fail closed; target by UserId; value commands capped, ledgered and off in production `[lihfolk]` | Every command: actor, target, arguments |
| Hidden information (roles, loot tables, stealth) | Server only | Reads replicated attributes and modules (wall-hacks, datamining) | Never replicate what a player must not know; reveal per player at the right time | None: it cannot be detected |
| Player-written text (signs, pet names) | Profile | Unfiltered text shown to others; megabyte strings | Length cap, UTF-8 check, TextService filter, show nothing on failure | Filter failures |

## Validation layers (cheapest first; reject silently)

1. **Rate**: per-player token bucket.
2. **Context and permission**: alive, right round phase, owns the plot, is an admin.
3. **Type and shape**: `type(x)`, `typeof(x)`, argument count, bounded table size and depth.
4. **Value**: NaN passes `type(x) == "number"` and fails every comparison, so check finiteness first (`x == x and x ~= math.huge and x ~= -math.huge`, or `math.isfinite` `[VS]`); then range, integer-ness, allowlist membership; strings: cap length, `utf8.len(s) ~= nil`, allowlists for ids.
5. **Instances**: `typeof(x) == "Instance"`, `IsA`, `IsDescendantOf(expectedFolder)`, ownership attribute, distance from the **server's** view of the character.
6. **Game rules**: cooldown on the server clock, item owned, enough currency, line of sight, plausible timing.

If a handler yields between a check and the effect, take a per-player lock first or re-check after the yield.

Rate limiting: token bucket with capacity for bursts (a button humans press 5 times a second gets capacity 10, refill 5/s); tighter limits plus a busy lock for expensive actions; clear buckets on `PlayerRemoving`; escalate gradually (drop silently, then log, then flag). Never kick on a first violation.

## Remote guard and rate limiter (server-only module)

```lua
--!strict
-- ServerScriptService/Server/Net/RemoteGuard.luau  (never replicate this)
local Players = game:GetService("Players")

type Bucket = { tokens: number, updatedAt: number }
local RateLimiter = {}
RateLimiter.__index = RateLimiter
export type RateLimiter = typeof(setmetatable({} :: { capacity: number, refillPerSecond: number, buckets: { [Player]: Bucket } }, RateLimiter))

function RateLimiter.new(capacity: number, refillPerSecond: number): RateLimiter
	local self = setmetatable({ capacity = capacity, refillPerSecond = refillPerSecond, buckets = {} }, RateLimiter)
	Players.PlayerRemoving:Connect(function(player) self.buckets[player] = nil end)
	return self
end

function RateLimiter.allow(self: RateLimiter, player: Player, cost: number?): boolean
	local now = os.clock()
	local bucket = self.buckets[player]
	if bucket == nil then bucket = { tokens = self.capacity, updatedAt = now }; self.buckets[player] = bucket end
	bucket.tokens = math.min(self.capacity, bucket.tokens + (now - bucket.updatedAt) * self.refillPerSecond)
	bucket.updatedAt = now
	local price = cost or 1
	if bucket.tokens < price then return false end
	bucket.tokens -= price
	return true
end

local Check = {}
function Check.finiteNumber(value: unknown, min: number, max: number): boolean
	if type(value) ~= "number" then return false end
	if value ~= value or value == math.huge or value == -math.huge then return false end -- NaN fails every comparison
	return value >= min and value <= max
end
function Check.integer(value: unknown, min: number, max: number): boolean
	return Check.finiteNumber(value, min, max) and (value :: number) % 1 == 0
end
function Check.string(value: unknown, maxLength: number): boolean
	return type(value) == "string" and #value <= maxLength and utf8.len(value) ~= nil
end
function Check.oneOf(value: unknown, allowed: { [string]: any }): boolean
	return type(value) == "string" and allowed[value] ~= nil
end
function Check.vector3(value: unknown, maxMagnitude: number): boolean
	if typeof(value) ~= "Vector3" then return false end
	local v = value :: Vector3
	return Check.finiteNumber(v.X, -maxMagnitude, maxMagnitude) and Check.finiteNumber(v.Y, -maxMagnitude, maxMagnitude) and Check.finiteNumber(v.Z, -maxMagnitude, maxMagnitude)
end
function Check.instanceIn(value: unknown, className: string, ancestor: Instance): boolean
	return typeof(value) == "Instance" and (value :: Instance):IsA(className) and (value :: Instance):IsDescendantOf(ancestor)
end

export type GuardOptions = { name: string, limiter: RateLimiter, argCount: number, validate: (player: Player, ...unknown) -> boolean }

local VIOLATION_LOG_THRESHOLD = 20
local violations: { [Player]: number } = {}
Players.PlayerRemoving:Connect(function(player) violations[player] = nil end)

local function recordViolation(player: Player, remoteName: string, reason: string)
	local count = (violations[player] or 0) + 1
	violations[player] = count
	if count == VIOLATION_LOG_THRESHOLD then
		warn(`[RemoteGuard] {player.UserId} reached {count} violations (latest: {remoteName}/{reason})`) -- feed detection; do not kick on this alone
	end
end

local RemoteGuard = { RateLimiter = RateLimiter, Check = Check }

function RemoteGuard.connect(remote: RemoteEvent, options: GuardOptions, handler: (player: Player, ...any) -> ()): RBXScriptConnection
	return remote.OnServerEvent:Connect(function(player: Player, ...: unknown)
		if not options.limiter:allow(player) then recordViolation(player, options.name, "rate"); return end
		if select("#", ...) ~= options.argCount then recordViolation(player, options.name, "argCount"); return end
		local ok, valid = pcall(options.validate, player, ...)
		if not ok or valid ~= true then recordViolation(player, options.name, "invalid"); return end
		handler(player, ...)
	end)
end

return RemoteGuard
```

Usage for a soft-currency purchase (price and ownership come from server data only):

```lua
local busy: { [Player]: true } = {}
RemoteGuard.connect(ReplicatedStorage.Remotes.PurchaseItem, {
	name = "PurchaseItem",
	limiter = RemoteGuard.RateLimiter.new(5, 1), -- burst 5, then 1 per second
	argCount = 1,
	validate = function(_player, itemId) return RemoteGuard.Check.oneOf(itemId, Items) end,
}, function(player, itemId: string)
	if busy[player] then return end
	busy[player] = true
	local ok, err = pcall(ShopService.Buy, ShopService, player, itemId)
	busy[player] = nil
	if not ok then warn(`[Shop] {player.UserId} {itemId}: {err}`) end
end)
```

Clear `busy` on `PlayerRemoving` too.

## Remote review procedure

Use it on every new remote and, in an audit, on every existing one. Steps 2 and 5 adapted from `[lihfolk]`.

1. **Inventory.** List every remote with type, direction and handler (sketch D). Compare with the manifest. A remote missing from the manifest, or created anywhere but the one creation module, is a finding.
2. **Read each handler top to bottom and mark each item present or missing:**
   1. Rate limit is the first statement, keyed by `Player` and a fixed action name (never a client string), sized at 1.5–2× the fastest legitimate use.
   2. Argument count, then the type of every argument.
   3. Values: finite, integer where a count is expected, in range; strings capped and valid UTF-8; ids from an allowlist; tables capped in key count and depth before any loop.
   4. Instances: class, expected ancestor, ownership, distance from the server's character position.
   5. Context: alive, right phase, off cooldown by the server clock, not busy.
   6. Lock, then act: no yield between the check and the write it protects. Yields hide in any `...Async` call, `task.wait`, `WaitForChild`, `InvokeClient`, a BindableFunction, and any module you did not write.
   7. The outcome (price, damage, reward, duration, target user) comes from server data, never from the payload.
   8. Relays build a fresh payload on the server and send only to players who need it.
   9. Rejections are silent and counted. No `warn` per request (log flooding), no kick on one violation.
3. **Search** for `InvokeClient`; `FireAllClients(` that forwards handler parameters; a yield between a check and a write; debug, test or admin remotes reachable in production (they need a server allowlist, not only `RunService:IsStudio()`).
4. **Repeat step 2** for `Touched`, `ProximityPrompt.Triggered`, `ClickDetector.MouseClick` and DragDetector handlers. They are client-triggered entry points too.
5. **Abuse-test in Studio only.** Register handlers as plain functions and call them with a test player and this corpus: `nil`, `true`, `0`, `-1`, `0.5`, `2^53 + 1`, `math.huge`, NaN, `""`, a 10,000-character string, invalid UTF-8, `{}`, a mixed table, a table 50 levels deep, a 10,000-entry array, a table shaped like an Instance (`{ Name = "Price", Value = 0 }`), real instances from the wrong place, `Vector3.new(0/0, 0, 0)` and `Vector3.new(1e9, 0, 0)`. Any error is a finding: an error half-way through a handler leaves half-written state. Then the race test below. Gate the harness three ways: it lives outside the published place, its first line returns unless `RunService:IsStudio()`, and no remote starts it. Run it against a mock store.
6. **Report** a table ranked money and items, then combat, then movement, then cosmetics: remote, missing check, the attack in one sentence, the fix.

Remote manifest and race test (unexecuted sketches):

```lua
--!strict
-- ReplicatedStorage/Shared/Net/Manifest.luau. The server creates remotes only from this list.
export type Entry = { direction: "toServer" | "toClient", reliable: boolean, perSecond: number, burst: number, movesValue: boolean, honeypot: boolean? }
local Manifest: { [string]: Entry } = {
	RequestPurchase = { direction = "toServer", reliable = true, perSecond = 1, burst = 5, movesValue = true },
	AimUpdate = { direction = "toServer", reliable = false, perSecond = 20, burst = 30, movesValue = false },
	PlayHitEffect = { direction = "toClient", reliable = true, perSecond = 0, burst = 0, movesValue = false },
	SyncInventoryV2 = { direction = "toServer", reliable = true, perSecond = 0, burst = 0, movesValue = false, honeypot = true },
}
return Manifest
```

```lua
-- Studio-only race test: 20 purchases in one frame must never grant more than the balance pays for.
for _ = 1, 20 do task.spawn(handlers.RequestPurchase, testPlayer, "Sword") end
task.wait()
assert(data.Cash >= 0 and (data.Inventory.Sword or 0) <= startCash // PRICE, "race: more grants than the balance allows")
assert(busy[testPlayer] == nil, "busy flag leaked")
```

At boot the server creates each remote from the manifest, builds its limiter from `perSecond` and `burst`, connects a wrong-direction detector to every `toClient` remote, requires the busy lock on `movesValue` handlers, and in Studio asserts that the remotes folder holds nothing without an entry. A new remote then cannot ship without answering the threat questions.

## Movement and combat checks

Decide first whether movement cheating can be made worthless `[lihfolk]`: ordered checkpoints with minimum segment times, server zone gating, a server distance check on every interaction. If a fly hacker gains only a view, a speed check with rubber-banding is enough. Build the full set only where position is the prize (races, ranked obbies, PvP, hide-and-seek, capture zones), or adopt server authority.

Movement (without server authority mode): a staggered loop per player compares XZ displacement against `WalkSpeed × elapsed × tolerance` (tolerance at least 1.5) and accumulates violations in a leaky bucket. Exempt server teleports, knockback, vehicles and respawns with a "grace until" timestamp. Check sustained airtime for flying and raycast between positions for noclip (this only works because visible models have real collision, which is one more reason for the house rule). Rubber-band to the last valid position before kicking.

| Check | Rule | Starting numbers `[lihfolk, rules of thumb]` | Honest cases to survive |
|---|---|---|---|
| Sampling | Compare server-side root positions at a fixed interval using real elapsed time | Every 0.2–0.5 s; skip a sample when elapsed exceeds 3× the interval (server hitch) | Latency bursts bunch positions: never act on one sample |
| Teleport | One-sample displacement above `maxStep` with no exemption | `maxStep = speed × dt × 1.5 + 8 to 12 studs` | Respawn and every server move: route them all through one helper that sets the exemption (search server code for `PivotTo`, `MoveTo` and character `.CFrame =`) |
| Speed | Leaky bucket on horizontal displacement | Slack scaled by `player:GetNetworkPing()`, clamped to 1 s because the client influences it | Vehicles (`Humanoid.SeatPart` set: validate the vehicle instead); platforms and conveyors (subtract the floor part's `AssemblyLinearVelocity × dt`); knockback |
| Fly | Airborne and not descending for too long | A default jump (gravity 196.2, `JumpHeight` 7.2) rises for about 0.27 s; flag at 1.5 s | Falling (descending is fine); ragdoll; swimming and climbing. Test "grounded" with a server raycast, not `Humanoid.FloorMaterial`, which comes from the client's simulation |
| Noclip | Ray from the previous to the current sample hits static collidable geometry | Count only penetration over 1 stud where the reverse ray also hits; cast at torso height; `RespectCanCollide = true` and the character's collision group | Doors and destructibles (tag and exclude); corners; spawns |

Update "last valid position" only when grounded and plausible, so a rubber-band never returns a player to mid-air. Repeated rubber-bands are themselves a strong signal. Conflict: this file used to say a 1–2 Hz loop; LihFolk samples at 2–5 Hz. Both work with a leaky bucket; use 2–4 Hz where position is the prize, 1–2 Hz elsewhere, and in every case check distance at the moment of each interaction, because a teleport-and-back between samples is invisible.

Combat: the client sends aim direction or target plus a timestamp; the server verifies the cooldown, recomputes the ray from the **server's** character position, and allows a small lag tolerance (community heuristic: about 10–15 extra studs and a 300–500 ms rewind cap). Reject muzzle origins far from the server root. Never apply damage from `Touched` on a client-owned weapon without a server-side distance check and per-target debounce. Parallel Luau fits bulk raycast validation (see performance.md).

Combat tuning `[lihfolk, rules of thumb unless marked]`:

- Cadence belongs to the server: stamp each accepted action with `Workspace:GetServerTimeNow()`, compute the effective cooldown in one server function, and accept at about 0.95× the authored cooldown so jitter never rejects an honest input (measured in their reference project). A server cooldown also makes autoclickers pointless: 30 clicks a second do what holding the button does.
- Reach: start with a generous static tolerance against current server positions (their melee project settled on 17 studs for 1.6×-scale characters after 13 rejected honest hits under real latency). For PvP, rewind the target only, start the interpolation allowance near 0.1 s, and clamp the rewind (0.4 s) so inflated ping buys nothing.
- Line of sight: one ray from attacker torso to target, ignoring blockers within 1.5 studs of the target. Ranged: replace the claimed origin with the server muzzle position and reject claims more than 2–4 studs from it. Cap and dedupe targets per action; keep a rolling damage-per-second backstop against the loadout maximum.
- Tune with data: ship every check log-only, record distance ÷ reach, elapsed time and ping, set tolerances so 99.5–99.9% of trusted players' claims pass, then enforce. Re-check after any change to character scale, weapon reach or move data: most new combat false positives come from your own update.
- Click-rate mechanics: cap the counted rate at about 12–15 per second so fast humans and machines score the same. Timing regularity is a soft signal only (network jitter blurs it and accessibility tools click regularly). For AFK farming prefer diminishing rewards or a presence prompt that pauses rewards, not play.

## Detection, honeypots and consequences

- Heuristics: completion times below a designer floor, gain per minute above the theoretical maximum, inhumanly regular cadence, impossible combinations. Combine into a suspicion score.
- Honeypot remotes that no legitimate client code fires are a high-confidence signal: log it and kick the session `[official]`. Variant: record each remote's intended direction and flag a client that fires a server-to-client remote. Conflict: this file used to say "observe before punishing"; the docs treat a honeypot hit as strong enough for a session kick, while bans still need several signals.
- Why never ban on one signal: it can be lag, a legitimate shortcut or a shared device; an instant ban teaches the exploiter which check fired; and bans spread to suspected alt accounts by default, so a false positive multiplies. Ban only when several different signals push a suspicion score past a high threshold, and never on a client-side detection `[official]`.
- Consequence ladder: silent logging → quiet mitigation (reject, rubber-band, zero rewards) → temporary restrictions → kick → ban. Delay visible consequences so the exploiter cannot tell which check fired.
- `Players:BanAsync` fields: `UserIds`, `Duration` (seconds, −1 permanent), `DisplayReason` (≤ 400 chars, filtered), `PrivateReason` (≤ 1,000 chars), `ExcludeAltAccounts` (alt propagation is on by default), `ApplyDeviceBlock` (24 h), `ApplyToUniverse` (default true). `GetBanHistoryAsync` and `UnbanAsync` for escalation and appeals. Publish your rules. `Players.BanningEnabled` switches the API on. Creator Hub > Moderation > Bans adds, lists and lifts bans with history (group permission required) `[official]`. There is no public API to query alt status `[community: open feature request]`; a 2026 DevForum post announces a new device-blocking capability for the Ban API, details not verified here `[VS]`.
- `[VS]` Device trust: `Player.DeviceTrustLevel` (`Pending`, `Unknown`, `None`, `Standard`, `Full`) and `IntegrityService.EvaluatePlayerDeviceTrust` (one callback per place, about 10 s timeout, after which the player is accepted). Android, Chromebook and Quest report `None`, `Standard` or `Full`; web browsers report `None`; iOS, macOS, Windows, Xbox and PlayStation are "coming soon" and report `Unknown` `[official]`. It describes the device, not the player.
- Device trust rules `[official]`: list the levels you allow (never compare numerically: `Unknown` sorts before `None`); reject only from the callback, never from `PlayerAdded`; read it on the server; check Creator Hub > Safety > Anti-cheat for the share of users, playtime and revenue per level before choosing a policy. Escalate from routing by trust (casual versus ranked places), to gating features such as trading, to rejecting `None` as a last resort.

Enforcement design `[lihfolk]`:

- **Base rates.** With 1% cheaters, a detector that catches 95% of them and wrongly flags 2% of honest players flags 95 cheaters and 198 honest players per 10,000: about 32% precision. Two independent detectors at 2% each wrongly flag an honest player 0.04% of the time. Two speed checks reading the same lag spike are not independent.
- **Score shape.** Weight each rule by reviewed precision; cap each rule's contribution so 200 lag-induced speed flags cannot reach the action threshold; require signals from two categories (movement, combat, economy, remote misuse) for any visible consequence, unless one near-certain signal (honeypot) fired.
- **Rollout.** Every rule has a mode: off, shadow (logged, no effect) or enforce. New and changed rules run in shadow for at least a week; review 20–50 flagged players by hand; enable on a canary (about 10% of servers, by JobId hash or a Configs flag); then enforce. Fall back to shadow automatically when a rule's flag rate jumps (for example 5× its weekly average within an hour): spikes are nearly always your own update.
- **Log with every signal:** ping, device type, place version, rule version, server frame time. Write an evidence record with a short case id before acting; put the case id in `PrivateReason` and in a neutral `DisplayReason` (never "speed hack detected").
- **Ban mechanics** `[VS]`: kicked exploiters rejoin in seconds, so confirmed cases get `BanAsync`. Set `ExcludeAltAccounts = true` unless confidence is high. LihFolk also reports that `UserIds` takes up to 50 ids per call, that an unban lifts only bans of the same scope (universe or place) and that bans do not apply from Studio (test in a private production place); none of the three was re-checked in the docs mirror.
- **Appeals:** look the case up by id, read the evidence before the player's story, check whether the rule version that fired has since been fixed, and check context (high ping, new device type, a buggy place version). Keep evidence for a fixed period and include it in right-to-erasure handling.
- Not adopted: secretly degrading a suspect's experience. LihFolk allows it at high confidence; here the only silent measure is holding flagged accounts off leaderboards (house rule: no punishment patterns on possibly honest players).

## Ownership, access control and third-party code

- Characters are always client-owned; movement validation is the only defence outside server authority mode.
- Gameplay-critical loose objects (a soccer ball): `SetNetworkOwner(nil)` and accept jitter, or validate outcomes on the server.
- Prompts on unanchored parts can be dragged to the exploiter; anchor interactable anchors or parent prompts to an invisible anchored helper.
- Server sanity loops reset assemblies with non-finite positions.
- Gated sub-places: set to "Secure within universe only" so only server `TeleportAsync` can reach them. Keep dev and test places in separate private universes.
- Never ship a module that mixes server and client logic and replicates.
- Libraries come from Wally or Git with pinned versions, never toolbox copies. After any insert, search for `require(<number>)`, `getfenv`, `setfenv`, `loadstring`, obfuscation and whitespace-hidden code. Keep `ServerScriptService.LoadStringEnabled` off. `[VS]` Script Capabilities (`SandboxedInstanceMode`, `Sandboxed`, `Capabilities`) are experimental; never grant `Network`, `DataStore`, `AssetRequire`, `CapabilityControl` or `LoadString` to third-party code.

## HttpService and secrets

- Server-only; needs Allow HTTP Requests. 500 plain HTTP requests per minute per server; Open Cloud calls from the game have a separate 2,500 per minute budget and accept only `x-api-key` and `content-type` headers. HTTPS only.
- Secrets store: up to 500 secrets per game, each up to 1,024 characters, scoped to a domain (never `*`). `HttpService:GetSecret(name)` returns a `Secret` usable in URL or headers with `AddPrefix`/`AddSuffix`, never in the body. Local Secrets for solo Studio testing.
- Never put API keys, webhook URLs or tokens in scripts, attributes, config modules or git. A Discord webhook in a ModuleScript is a public spam endpoint.
- Any player-written text shown to others is filtered on the server with `TextService:FilterStringAsync` and then the matching `Get...Async`; if filtering fails, show nothing.

## Backdoors, plugins and team hygiene

How backdoors arrive: Creator Store models that contain scripts `[official]`; a malicious or compromised plugin that injects scripts into services the Explorer hides and re-inserts them after deletion; a collaborator with edit access `[community]`. Roblox moderates models but does not promise to catch everything `[official]`. Under house rule 1 no marketplace model ships, so any hit below is a finding.

What to look for: `require(<number>)` or a `require` whose argument is built at runtime; `getfenv`, `setfenv`, `loadstring`; `HttpService`, `TeleportService` or `PromptPurchase` calls in code you did not write; obfuscated or unusually complex code, including code pushed off-screen with whitespace `[official]` (in practice: `string.char` chains, byte escapes, one very long line `[house]`); scripts in services the Explorer hides `[community]` or in places no script belongs, such as inside meshes, welds, Lighting or SoundService `[house]`. Legitimate admin systems (Adonis, HD Admin) also `require` by id, so read each hit instead of bulk-deleting `[community]`. Scanner plugins are heuristic pattern matchers and are themselves third-party code with plugin privileges; prefer sketch C.

Clean-up order: remove the suspect plugin first (it re-inserts), then the scripts, then rotate every secret and API key, publish, and restart servers `[community]`.

Team and credential hygiene `[official]`:

- Group roles: keep "edit" separate from "edit and publish"; API-key management, secrets, data-store key and store deletion, ban configuration and payouts are separate permissions, several grantable per game. Give each person the minimum. After any incident read Activity History (Studio Window menu or Creator Hub) and the group audit log.
- Open Cloud keys: a key can reach everything its owner can. Create CI keys on a dedicated automation account that belongs only to the target group with a minimal role; keep Restrict by Experience on; add an IP allowlist (not for keys used from inside a place); set an expiry and own the rotation; store keys in CI secrets. Never put a `.ROBLOSECURITY` cookie in CI: it is a full account session.
- Studio MCP clients can read and modify open places. `open_cloud_invoke` permissions are per game and per person; stay on Balanced and leave Money & monetization, Player consequences, Security & credentials, `universe:write` and `universe-places:write` off except for the task that needs them. "Save & load data" lets `execute_luau` write live DataStores.
- Script Capabilities (above) are still a client beta `[official]`: useful for quarantine tests, not a control to rely on.

Creator account security and takeover recovery `[lihfolk, community-reported]`:

- How accounts fall, most common first: a stolen session cookie (malware posing as a plugin, asset pack, Studio tool or cheat; it can bypass the password and sometimes 2-step verification until the session is revoked); phishing ("Roblox staff", DevEx or copyright notices, commission offers with a "test file"); a malicious plugin acting with your permissions; an over-privileged collaborator whose own account is taken; password reuse.
- Harden: 2-step verification with an authenticator app or security key; a unique password; strong 2FA on the recovery email; an account PIN; a separate owner account that owns the group, rarely logs in and never installs plugins, with your daily account in a high but non-owner role; games owned by a group, not a person; fund permissions for one role only; contractors work in a test universe; a quarterly audit of roles, collaborators and API keys. Open `.rbxm` files from strangers in a scratch place and read every script.
- Recovery, in order: (1) from a clean device change the password, reset 2-step verification and log out of all other sessions (email first if it was hit); (2) if the game is serving malicious content, make it private or shut servers down and restore a known-good version from Version History; (3) remove unknown collaborators, roles and members and rotate every key and secret; (4) run sketch C before republishing; (5) check group funds, product and pass prices; (6) contact Roblox Support through the official form, never a "recovery service"; (7) treat the computer as infected until scanned or reinstalled.

## Level-up audit: how to check an existing game

1. **Contain an active incident first.** Rotate keys and secrets, remove unknown collaborators and plugins, read Activity History and place version history, then fix, publish and restart servers.
2. **Backdoor scan** with sketch C over the whole DataModel. Review every hit by hand.
3. **Remote inventory** with sketch D, then the remote review procedure above on every handler, economy remotes first. Threat-model each system with the walkthrough table.
4. **Play the exploiter in Studio** (Server & Clients test, client command bar): fire each remote with wrong types, NaN, a megabyte string, another player's instances, and 100 times a second; set `WalkSpeed` locally; teleport; trigger prompts from across the map. Do not use real executors for this: a 2026 bug report describes Hyperion banning developers who tested on their own experiences `[community]`.
5. **Fix in this order:** anything that grants currency, items or purchases; then damage and PvP; then movement; then cosmetics.
6. **Configuration:** "Secure within universe only"; `LoadStringEnabled` off; HTTP off unless used; dev and test in a separate universe; roles and keys as above; no secrets in source.
7. **Then add detection:** honeypot, suspicion score, logs to analytics, consequence ladder.

Sketch C, backdoor and secret scan (unexecuted sketch; command bar or Studio MCP `execute_luau` with `datamodel_type = Edit`; read-only):

```lua
--!strict
local ScriptEditorService = game:GetService("ScriptEditorService")
local PATTERNS = {
	{ "require by id", "require%s*%(%s*%d+" }, { "getfenv/setfenv", "[gs]etfenv" }, { "loadstring", "loadstring" },
	{ "HttpService", "HttpService" }, { "string.char", "string%.char" }, { "byte escapes", "\\%d%d%d?\\%d%d" },
	{ "webhook URL", "discord%.com/api/webhooks" }, { "TeleportService", "TeleportService" }, { "PromptPurchase", "PromptPurchase" },
}
local EXPECTED = { "ServerScriptService", "ServerStorage", "ReplicatedStorage", "ReplicatedFirst", "StarterPlayer", "StarterGui", "StarterPack" }
local scanned = 0
for _, service in game:GetChildren() do -- includes services the Explorer hides
	local ok, descendants = pcall(function() return service:GetDescendants() end)
	if not ok then continue end
	for _, d in descendants do
		if not d:IsA("LuaSourceContainer") then continue end
		local okSource, source = pcall(function() return ScriptEditorService:GetEditorSource(d) end)
		if not okSource then continue end
		scanned += 1
		local hits: { string } = {}
		if not table.find(EXPECTED, service.Name) then table.insert(hits, "unexpected location") end -- includes scripts inside Workspace models
		for _, pattern in PATTERNS do
			if string.find(source, pattern[2]) then table.insert(hits, pattern[1]) end
		end
		for line in string.gmatch(source, "[^\n]+") do
			if #line > 500 then table.insert(hits, "line over 500 characters"); break end
		end
		if #hits > 0 then warn(d:GetFullName(), "→", table.concat(hits, ", ")) end
		if scanned % 200 == 0 then task.wait() end
	end
end
print("scanned", scanned, "scripts")
```

Sketch D, remote inventory and unvalidated handlers (unexecuted sketch; a heuristic that only tells you where to read):

```lua
--!strict
local ScriptEditorService = game:GetService("ScriptEditorService")
local function count(source: string, pattern: string): number return (select(2, string.gsub(source, pattern, ""))) end
local remotes, review = 0, 0
for _, root in { game:GetService("ReplicatedStorage"), workspace, game:GetService("StarterGui"), game:GetService("StarterPlayer"), game:GetService("StarterPack") } :: { Instance } do
	for _, d in root:GetDescendants() do
		if d:IsA("BaseRemoteEvent") or d:IsA("RemoteFunction") then
			remotes += 1
			local outcome = string.find(d.Name, "^Set") or string.find(d.Name, "^Add") or string.find(d.Name, "^Give") or string.find(d.Name, "Damage")
			print(d.ClassName, d:GetFullName(), if outcome then "← outcome-style name" else "")
		elseif d:IsA("ProximityPrompt") then
			local host = d.Parent
			if host and host:IsA("BasePart") and not host.Anchored then warn("prompt on an unanchored part:", d:GetFullName()) end
		end
	end
end
for _, d in game:GetService("ServerScriptService"):GetDescendants() do
	if not d:IsA("LuaSourceContainer") then continue end
	local source = ScriptEditorService:GetEditorSource(d)
	local handlers = count(source, "OnServerEvent") + count(source, "OnServerInvoke")
	if handlers == 0 then continue end
	local checks = count(source, "typeof%(") + count(source, "type%(") + count(source, "RemoteGuard")
	if checks < handlers then review += 1; warn(d:GetFullName(), handlers, "handlers,", checks, "type checks") end
	if string.find(source, "InvokeClient") then warn(d:GetFullName(), "uses InvokeClient") end
end
print(remotes, "remotes;", review, "server scripts to read first")
```

| Symptom | Likely cause | Fix |
|---|---|---|
| Players hold impossible currency or items | A remote carries an outcome (amount, price, item id trusted), or a dupe | Intent-only remotes through the guard; server-side prices and ownership; dupes: data-and-purchases.md |
| Strange GUIs or music, "admin" abuse, servers shut down, unknown purchase prompts | Backdoor: `require(id)` from a model or a plugin-injected script | Sketch C; plugin first, then scripts; rotate keys; publish; restart servers |
| Webhook spam or leaked data | Webhook URL or API key in a script | Secrets store with a domain scope; rotate the leaked value |
| Players flung or killed from nowhere | Network-ownership abuse on unanchored props; `Touched`-only damage | Anchor; `SetNetworkOwner(nil)` on gameplay objects; sanity loop for non-finite or over-speed assemblies; server hit checks |
| Speed, fly or teleport wins in an obby or race | Client-owned character with no server check | Movement loop with tolerance; checkpoints validated by order and minimum time; server authority for competitive modes |
| Server lag follows one player | Remote spam or oversized payloads | Token bucket; argument count and size caps before any work |
| Players reach VIP, test or unreleased places | Client-initiated teleport inside the universe | "Secure within universe only"; separate private universe for dev |
| Prompt or click fires from across the map | Server trusts `Triggered` or `MouseClick` | Re-check distance and state on the server |
| Honest players banned | Ban on one signal or on a client-side detection; alt propagation spreads the mistake | Suspicion score, ladder, published rules, appeals, `GetBanHistoryAsync` |
| Mechanics cloned or exploits found fast | Server logic inside replicated ModuleScripts | Split modules; server-only code in ServerScriptService |
| Unknown publishes or settings changes | Over-broad group role, leaked key or cookie | Activity History and audit log; rotate; least privilege; automation account |

## Security review gate

- [ ] Every remote goes through rate limiting plus type, finiteness, range, length, UTF-8, instance and game-rule checks; rejections are silent.
- [ ] No `InvokeClient`; `OnServerInvoke` assigned once.
- [ ] Remotes carry intent; the server never trusts client prices, damage, positions or player ids.
- [ ] Prompts, ClickDetectors and DragDetectors re-validated on the server; interactable anchors anchored.
- [ ] Movement and combat validated with tolerances and teleport exemptions; no `Touched`-only damage.
- [ ] No secrets or server logic in replicated containers.
- [ ] Gated sub-places "Secure within universe only"; dev and test universes separate.
- [ ] Consequences escalate; no instant ban on one signal.
- [ ] Unreliable remotes carry only replaceable data under 1,000 bytes.
- [ ] Backdoor scan run over the whole DataModel; every hit read; no `require(<number>)`, `getfenv` or `loadstring` left.
- [ ] CI keys live on a dedicated automation account, experience-restricted, IP-restricted and expiring; no cookies in CI; group roles are least-privilege.
- [ ] Server authority decision recorded (adopt for competitive physics, otherwise validation loops), with the docs status re-checked.
- [ ] Each system has a threat table (assets, boundaries, scored threats, design fix); every remote has a manifest entry enforced at start-up.
- [ ] Remote review procedure passed on every value-moving handler, including the Studio fuzz corpus and the race test.
- [ ] New detectors start in shadow mode; no visible consequence from one rule; bans carry a case id and an evidence record.
- [ ] Owner account separated, 2-step verification on, roles and keys audited this quarter.

Grep `references/knowledge-base.md` for `## 4.4` and `## 4.5`.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/scripting/security/{security-tactics,client-server-boundary,network-ownership,server-side-detection,third-party-vulnerabilities,access-control,device-trust}.md`, `projects/server-authority/{index,techniques}.md`, `projects/{groups,activity-history}.md`, `production/bans.md`, `cloud/auth/api-keys.md`, `studio/mcp-open-cloud.md`, `scripting/capabilities.md`, `reference/engine/classes/{Players,Workspace,UnreliableRemoteEvent,ScriptEditorService}.yaml` (read)
- Server authority (search summary): https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993, https://devforum.roblox.com/t/studio-beta-build-fair-responsive-games-with-server-authority/4139157, https://devforum.roblox.com/t/early-access-server-authority/3983188, https://devforum.roblox.com/t/client-beta-publish-test-your-server-authoritative-experiences/4606949, https://about.roblox.com/newsroom/2026/07/creating-responsive-cheat-resistant-games-roblox-server-authority
- https://devforum.roblox.com/t/can-you-detect-if-an-event-was-fired-from-an-executor/4064026 (search summary)
- https://devforum.roblox.com/t/hyperion-incorrectly-bans-developers-for-permitted-anticheat-testing-on-edit-enabled-experiences/4527239 (search summary)
- https://devforum.roblox.com/t/ban-api-new-device-blocking-capability/4668265, https://devforum.roblox.com/t/give-us-access-to-the-alt-account-detection-api/4909414 (search summary)
- https://devforum.roblox.com/t/removing-backdoors-101/545574, https://devforum.roblox.com/t/malicious-scripts-inside-cafe-models/3887121, https://devforum.roblox.com/t/backdoor-prevention/3122952, https://devforum.roblox.com/t/clearing-your-game-of-malicious-scripts-plugins/511830, https://devforum.roblox.com/t/shieldscan-anti-backdoor-scanner-for-roblox-studio/4736119 (search summary)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-secure-remotes/SKILL.md`, `skills/roblox-anti-exploit-review/SKILL.md`, `LihFolk Vault V2/22 Anti-Exploit and Security/{Threat Modeling a Roblox Game, Economy Exploits - Dupes Races and Purchase Abuse, Detecting Movement Exploits - Speed Fly Noclip Teleport, Detecting Combat Exploits - Reach Rate and Aim, False Positives Lag and Fair Enforcement, Logging Bans and Appeals, Testing Your Own Remotes - Fuzzing and Abuse Tests, Autoclicker and Macro Detection for Combat Remotes, Admin Commands Done Safely - Permissions and Audit Logs, Creator Account Security and Takeover Recovery}.md`, `03 Architecture and Networking/{Remote Abuse Patterns and Rate Limiting in Practice, Interest Management and Per-Player Replication}.md` (read)
- Executor-vendor pages seen only as search snippets were used solely for the statement that such tools are still advertised; none is linked here.
- No evidence found: an official statement of which platforms Hyperion covers; an official description of how alt-account detection works.
