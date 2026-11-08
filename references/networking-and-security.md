# Networking and security

Distilled from knowledge-base sections 4.4 and 4.5. Every client-to-server remote in a shipped game goes through the guard in this file. Snippets were checked against the docs but not executed. `[VS]` marks version-sensitive facts.

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
- Batch and coalesce high-frequency updates into one packed event per Heartbeat or every N frames. Deltas on reliable remotes only; absolute values on unreliable remotes.
- Attributes as replicated state: `SetAttribute` on the server replicates to clients with the instance. `[VS]` Only the first 64 attributes replicate, names at most 50 characters, string values at most 50 characters. Attributes are public to every client that has the instance; never put private state there.
- Generated networking (Blink or Zap) packs data into `buffer`s and validates structure, not game rules. Worth it for shooters, large simulations and ECS games; a typed wrapper plus the guard is enough for a simulator or obby. Sync handlers must never yield or error; default to `SingleAsync` / `ManyAsync`. Pin versions and commit generated files `[VS]`.
- Test with Server & Clients playtests (up to 8 clients), the Network Simulator (latency, jitter, packet loss) and the Developer Console network stats.

## Threat model: what an exploiting client can always do

Read all replicated code (including disabled scripts); control its character and every part it owns (teleport, fly, noclip, NaN CFrames, fling others); fire `Touched` for owned parts; trigger `ProximityPrompt`s, `ClickDetector`s and `DragDetector`s from any distance (only `Triggered` has a server distance check; `ClickDetector` has none); fire any remote with any arguments at any rate; change its local DataModel; teleport to any place in the universe unless restricted.

It cannot read or change `ServerScriptService` or `ServerStorage`, change server-side properties directly, or call server-only APIs.

For each new feature ask: what happens if this remote is fired 1,000 times per second, with garbage arguments, with another player's objects, from across the map, while dead, during a round transition?

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

## Movement and combat checks

Movement (without server authority mode): a staggered 1–2 Hz loop per player compares XZ displacement against `WalkSpeed × elapsed × tolerance` (tolerance at least 1.5) and accumulates violations in a leaky bucket. Exempt server teleports, knockback, vehicles and respawns with a "grace until" timestamp. Check sustained airtime for flying and raycast between positions for noclip (this only works because visible models have real collision, which is one more reason for the house rule). Rubber-band to the last valid position before kicking.

Combat: the client sends aim direction or target plus a timestamp; the server verifies the cooldown, recomputes the ray from the **server's** character position, and allows a small lag tolerance (community heuristic: about 10–15 extra studs and a 300–500 ms rewind cap). Reject muzzle origins far from the server root. Never apply damage from `Touched` on a client-owned weapon without a server-side distance check and per-target debounce. Parallel Luau fits bulk raycast validation (see performance.md).

## Detection, honeypots and consequences

- Heuristics: completion times below a designer floor, gain per minute above the theoretical maximum, inhumanly regular cadence, impossible combinations. Combine into a suspicion score.
- Honeypot remotes the real client never fires catch spam scripts; observe before punishing.
- Consequence ladder: silent logging → quiet mitigation (reject, rubber-band, zero rewards) → temporary restrictions → kick → ban. Delay visible consequences so the exploiter cannot tell which check fired.
- `Players:BanAsync` fields: `UserIds`, `Duration` (seconds, −1 permanent), `DisplayReason` (≤ 400 chars, filtered), `PrivateReason` (≤ 1,000 chars), `ExcludeAltAccounts` (alt propagation is on by default), `ApplyDeviceBlock` (24 h), `ApplyToUniverse` (default true). `GetBanHistoryAsync` and `UnbanAsync` for escalation and appeals. Publish your rules.
- `[VS]` `Player.DeviceTrustLevel` (`Pending`, `Unknown`, `None`, `Standard`, `Full`) and `IntegrityService.EvaluatePlayerDeviceTrust` (one callback per place, about 10 s timeout). Attestation exists only on Android, Chromebook and Quest; use it as a per-feature policy input, never a blanket gate.

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

Grep `references/knowledge-base.md` for `## 4.4` and `## 4.5`.
