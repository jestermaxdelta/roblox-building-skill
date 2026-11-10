# Networking and security

What this is: the remote design rules, the threat model, the server-side guard, and the anti-cheat, ban, backdoor and credential practices for a Roblox game. Open it when designing a network surface, or jump to "Level-up audit" for a live game that is being exploited or has never been reviewed. Distilled from knowledge-base sections 4.4 and 4.5; platform facts re-checked against `Roblox/creator-docs` on 2026-11-10. Every client-to-server remote in a shipped game goes through the guard in this file. Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

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
- Honeypot remotes that no legitimate client code fires are a high-confidence signal: log it and kick the session `[official]`. Variant: record each remote's intended direction and flag a client that fires a server-to-client remote. Conflict: this file used to say "observe before punishing"; the docs treat a honeypot hit as strong enough for a session kick, while bans still need several signals.
- Why never ban on one signal: it can be lag, a legitimate shortcut or a shared device; an instant ban teaches the exploiter which check fired; and bans spread to suspected alt accounts by default, so a false positive multiplies. Ban only when several different signals push a suspicion score past a high threshold, and never on a client-side detection `[official]`.
- Consequence ladder: silent logging → quiet mitigation (reject, rubber-band, zero rewards) → temporary restrictions → kick → ban. Delay visible consequences so the exploiter cannot tell which check fired.
- `Players:BanAsync` fields: `UserIds`, `Duration` (seconds, −1 permanent), `DisplayReason` (≤ 400 chars, filtered), `PrivateReason` (≤ 1,000 chars), `ExcludeAltAccounts` (alt propagation is on by default), `ApplyDeviceBlock` (24 h), `ApplyToUniverse` (default true). `GetBanHistoryAsync` and `UnbanAsync` for escalation and appeals. Publish your rules. `Players.BanningEnabled` switches the API on. Creator Hub > Moderation > Bans adds, lists and lifts bans with history (group permission required) `[official]`. There is no public API to query alt status `[community: open feature request]`; a 2026 DevForum post announces a new device-blocking capability for the Ban API, details not verified here `[VS]`.
- `[VS]` Device trust: `Player.DeviceTrustLevel` (`Pending`, `Unknown`, `None`, `Standard`, `Full`) and `IntegrityService.EvaluatePlayerDeviceTrust` (one callback per place, about 10 s timeout, after which the player is accepted). Android, Chromebook and Quest report `None`, `Standard` or `Full`; web browsers report `None`; iOS, macOS, Windows, Xbox and PlayStation are "coming soon" and report `Unknown` `[official]`. It describes the device, not the player.
- Device trust rules `[official]`: list the levels you allow (never compare numerically: `Unknown` sorts before `None`); reject only from the callback, never from `PlayerAdded`; read it on the server; check Creator Hub > Safety > Anti-cheat for the share of users, playtime and revenue per level before choosing a policy. Escalate from routing by trust (casual versus ranked places), to gating features such as trading, to rejecting `None` as a last resort.

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

## Level-up audit: how to check an existing game

1. **Contain an active incident first.** Rotate keys and secrets, remove unknown collaborators and plugins, read Activity History and place version history, then fix, publish and restart servers.
2. **Backdoor scan** with sketch C over the whole DataModel. Review every hit by hand.
3. **Remote inventory** with sketch D. For each remote write down: who fires it, what it grants, which checks exist. Flag outcome-style names, missing rate limits, missing type checks, `InvokeClient`.
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

Grep `references/knowledge-base.md` for `## 4.4` and `## 4.5`.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/scripting/security/{security-tactics,client-server-boundary,network-ownership,server-side-detection,third-party-vulnerabilities,access-control,device-trust}.md`, `projects/server-authority/{index,techniques}.md`, `projects/{groups,activity-history}.md`, `production/bans.md`, `cloud/auth/api-keys.md`, `studio/mcp-open-cloud.md`, `scripting/capabilities.md`, `reference/engine/classes/{Players,Workspace,UnreliableRemoteEvent,ScriptEditorService}.yaml` (read)
- https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 (search summary)
- https://devforum.roblox.com/t/studio-beta-build-fair-responsive-games-with-server-authority/4139157, https://devforum.roblox.com/t/early-access-server-authority/3983188, https://devforum.roblox.com/t/client-beta-publish-test-your-server-authoritative-experiences/4606949 (search summary)
- https://about.roblox.com/newsroom/2026/07/creating-responsive-cheat-resistant-games-roblox-server-authority (search summary)
- https://devforum.roblox.com/t/can-you-detect-if-an-event-was-fired-from-an-executor/4064026 (search summary)
- https://devforum.roblox.com/t/hyperion-incorrectly-bans-developers-for-permitted-anticheat-testing-on-edit-enabled-experiences/4527239 (search summary)
- https://devforum.roblox.com/t/ban-api-new-device-blocking-capability/4668265, https://devforum.roblox.com/t/give-us-access-to-the-alt-account-detection-api/4909414 (search summary)
- https://devforum.roblox.com/t/removing-backdoors-101/545574, https://devforum.roblox.com/t/malicious-scripts-inside-cafe-models/3887121, https://devforum.roblox.com/t/backdoor-prevention/3122952, https://devforum.roblox.com/t/clearing-your-game-of-malicious-scripts-plugins/511830, https://devforum.roblox.com/t/shieldscan-anti-backdoor-scanner-for-roblox-studio/4736119 (search summary)
- Executor-vendor pages seen only as search snippets were used solely for the statement that such tools are still advertised; none is linked here.
- No evidence found: an official statement of which platforms Hyperion covers; an official description of how alt-account detection works.
