# Data, purchases, teleports and cross-server systems

What this is: player data (ProfileStore), DataStore and MemoryStore limits, idempotent receipts, game passes, gifts, teleports and messaging. Open it when building the data layer, or jump to "Level-up audit" when a live game loses data, dupes items or throttles. Distilled from knowledge-base sections 4.6, 4.7 and 4.8; limits and library status re-checked on 2026-11-10 (`Roblox/creator-docs`, library repos). Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

## Choosing a storage service

| Need | Use |
|---|---|
| Player progress, inventory, currency, purchase history | Standard DataStore through a session-locking library (ProfileStore by default; see library status below) |
| Global leaderboards | Ordered DataStore (integers only), cached and refreshed every few minutes |
| Matchmaking queues, server lists, cross-server locks, trade escrow | MemoryStore (sorted map, queue, hash map); expires within 45 days |
| Broadcast hints (announcements, "refresh your cache") | MessagingService (best effort, about 1 KB) |
| Live feature flags and tuning | Configs (read-only at runtime, about 5-minute deploy) |
| API keys and tokens | Secrets store |
| Per-server caches | Luau tables |

All cloud services are server-only. Studio needs "Enable Studio Access to API Services"; use a separate test universe so Studio never touches live data.

## DataStore limits `[VS]`

- Names, keys and scopes: 50 characters. Value: 4,194,304 characters of JSON per key. Metadata: 300 characters total.
- Experience-level per-minute limits (shared with Open Cloud): Read 300 + CCU×40; Write 300 + CCU×20; List 300 + CCU×2; Remove 300 + CCU×40. `UpdateAsync` costs one read and one write.
- Per-server defaults per minute: standard Read/Write/Remove 60 + players×40, List 5 + players×2; ordered Write and Remove 30 + players×5. These are now a creator tool: `DataStoreService:SetRateLimitForRequestType` changes them and `GetRequestBudgetForRequestType` reads what is left. Errors tell you which layer throttled: `…GameServerThrottled`, `…ExperienceThrottled`, `KeyThrottled`, `DatastoreThrottled` `[official]`.
- 2026 changes `[community: DevForum announcements via search]`: storage limits enforced from 9 April 2026 and experience-level access limits rolled out 9–23 April; in July the in-game and Open Cloud budgets merged into one per-experience budget and base storage rose from 100 MB to 500 MB. Conflict: the Extended Services pricing table in the docs still shows the older defaults (250, 100 and 10 request baselines; 100 MB). Trust the limits page and your dashboard.
- Above the defaults: Extended Services (paid; owner 18+, ID-verified, supported country). Standard stores per million requests: Get $0.08, Set $0.80, List $0.60, Remove $0.80; storage $0.12 per GB-month; monthly budget from $0.50, throttled when it runs out `[official]`. Reduce requests and storage first.
- Operations tools `[official]`: Monitoring > Data Stores (requests by API and status, quota usage, storage); Configurations > Data stores manager (browse keys, compare and revert versions, mark for deletion with a 30-day restore window, RTBF templates); Open Cloud Snapshot Data Stores (once a day; take one before any update that changes save logic); `GetVersionAtTimeAsync`; the Data Stores Batch Processor CLI for bulk repairs.
- Per-key throughput: 25 MB/min reads, 4 MB/min writes. Each request type queues up to 30 requests; beyond that errors 301–306.
- Storage quota: 500 MB + 1 MB × lifetime users, measured on compressed data (do not pre-compress).
- Key error codes: 101/102 key name; 103/104 unserialisable value (functions, Instances, cycles, mixed tables, NaN); 105 too large; 301–306 throttled; 401/402 during shutdown; 403 no Studio access; 404 and 501–505 internal (retry with backoff and verify); 511–513 metadata or user-id errors.
- A failed write may have succeeded. Confirm with `DataStoreGetOptions.UseCache = false` before refunding or retrying anything non-idempotent (`GetAsync` serves a 4-second cache).

## Practices that prevent data loss

- One key per player, static pattern `Player_{UserId}`. Never change the key pattern without a migration. Keep numeric `UserId` keys even though `Player.User` exists `[VS]`.
- Load once, buffer in memory, save periodically. Never read during gameplay.
- Prefer `UpdateAsync` for anything several servers could write; the transform must not yield, may run more than once, and returning `nil` cancels. Metadata and user ids must be re-passed on every write.
- Retries: exponential backoff with jitter (1, 2, 4, 8 s ± 25%), 3–5 attempts, in order per key.
- Autosave every 3–5 minutes with a random initial offset. Save immediately after purchases.
- Serialisable data only: pure arrays or all-string-key tables, no `nil` holes, no Instances or `Vector3`/`CFrame`/`Color3`, no NaN or inf, valid UTF-8, no cycles. Cap player-supplied strings and key counts before they enter saved data.
- Versioning: one version per key per UTC hour, overwritten versions kept 30 days; `ListVersionsAsync` and `GetVersionAsync` are your backup and restore.
- Ordered stores have no versioning or metadata; write leaderboard values at most every few minutes and on leave; `leaderstats` is display, never storage.
- Trades: never move items between two players with two independent saves. Both profiles session-locked on the same server, both `IsActive()`, mutate both with no yield, then save both. Cross-server trades use an escrow record with a unique id and idempotent completion.
- `game:BindToClose` gives about 30 seconds; ProfileStore and Lapis already handle shutdown, so do not add your own save loop on top.
- Right to be forgotten: RTBF deletion templates in Creator Hub (up to 100), using the `{UserId}` token; call `profile:AddUserId(userId)` so metadata lists the owner; data keyed otherwise needs a webhook handler.

## ProfileStore essentials

- `ProfileStore.New(storeName, template)`; `store:StartSessionAsync(key, { Cancel = fn })` returns a `Profile` or `nil`.
- Constants (adjust with `ProfileStore.SetConstant`): `AUTO_SAVE_PERIOD = 300`, `FIRST_LOAD_REPEAT = 5`, `LOAD_REPEAT_PERIOD = 10`, `SESSION_STEAL = 40`, `ASSUME_DEAD = 630`, `START_SESSION_TIMEOUT = 120` (disabled when a `Cancel` function is passed). Never pass `{ Steal = true }` in normal loading.
- `profile.Data` saves while `profile:IsActive()` is true; the guarantee does not survive a yield. Check, then write immediately.
- `profile:EndSession()` on `PlayerRemoving`. Signals: `OnSave`, `OnLastSave(reason)` (`"Manual"`, `"External"`, `"Shutdown"`), `OnSessionEnd` (kick the player), `OnAfterSave(lastSavedData)` (`profile.LastSavedData` is now durable; ideal for purchase confirmation).
- Module signals: `OnError`, `OnOverwrite`, `OnCriticalToggle`, `IsCriticalState`, `DataStoreState`.
- `profile:Reconcile()` fills template fields; `profile:AddUserId()`; `profile:Save()` costs one `UpdateAsync` (reserve for purchases).
- `store:MessageAsync(key, message)` delivers to a profile whether or not it is loaded (two `UpdateAsync` calls); receive with `profile:MessageHandler(function(message, processed) ... processed() end)`. Use it for gifting paid items to offline friends.
- `store:GetAsync(key)` reads without a session for admin tools; `store.Mock` for tests and Studio.

Library status at 2026-11-10 `[VS]` (last commit dates read from the repos):

| Library | Evidence | Verdict |
|---|---|---|
| ProfileStore (MadStudioRoblox) | Last commit 2025-07-31; one ModuleScript; author says ProfileService profiles load in it (test `MessageAsync` first) `[community]` | Default. A quiet repo here means finished, not abandoned; vendor a pinned copy |
| ProfileService | Last commit 2024-10; superseded by ProfileStore | Leave it in a healthy live game; migrate when you next rework data |
| Lyra (paradoxum-games) 0.6.0 | Last commit 2026-03; transactions (`txAsync`), auto-sharding past 4 MB, validation, migrations, import of existing data. README: early development, "avoid … where data loss would be catastrophic" | Evaluate when atomic trades or very large saves are core; soak-test first |
| Lapis | Last commit 2025-02; Promise API, validation, migrations; README: not battle-tested | Niche |
| DataStore2 | Last commit 2023-03; the docs call it legacy; Roblox ships a beta migration tool `[official]` | Migrate off |

Read the official player-data sample (session locking, ordered retries, 180 s autosave) before judging any library `[official]`. Suphi's DataStore and DocumentService appear in forum comparisons; no evidence gathered here.

## DataService with schema migration

```lua
--!strict
-- ServerScriptService/Server/Services/DataService.luau
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ProfileStore = require(game:GetService("ServerScriptService").ServerPackages.ProfileStore)

local SCHEMA_VERSION = 3
local USE_MOCK_IN_STUDIO = true

export type PlayerData = {
	SchemaVersion: number, Cash: number,
	Inventory: { [string]: number }, Boosts: { [string]: number },
	Entitlements: { [string]: boolean }, PurchaseIds: { string },
}
local TEMPLATE: PlayerData = { SchemaVersion = SCHEMA_VERSION, Cash = 0, Inventory = {}, Boosts = {}, Entitlements = {}, PurchaseIds = {} }

-- MIGRATIONS[n] upgrades version n to n + 1. Never edit a shipped step.
local MIGRATIONS: { [number]: (data: { [string]: any }) -> () } = {
	[1] = function(data) data.Cash = (data.Cash or 0) + (data.Coins or 0); data.Coins = nil end,
	[2] = function(data)
		local counts: { [string]: number } = {}
		for _, itemId in data.Inventory or {} do counts[itemId] = (counts[itemId] or 0) + 1 end
		data.Inventory = counts
	end,
}

local store = ProfileStore.New("PlayerData", TEMPLATE)
if USE_MOCK_IN_STUDIO and RunService:IsStudio() then store = store.Mock :: any end
type Profile = typeof(store:StartSessionAsync(""))
local profiles: { [Player]: Profile } = {}
local failed: { [Player]: true } = {}

local function migrate(data: { [string]: any }): boolean
	local version = if type(data.SchemaVersion) == "number" then data.SchemaVersion else 1
	if version > SCHEMA_VERSION then return false end -- newer build wrote it; do not touch
	while version < SCHEMA_VERSION do
		local step = MIGRATIONS[version]
		if step then step(data) end
		version += 1
	end
	data.SchemaVersion = SCHEMA_VERSION
	return true
end

local DataService = {}

function DataService:Init()
	Players.PlayerRemoving:Connect(function(player)
		failed[player] = nil
		local profile = profiles[player]
		if profile ~= nil then profiles[player] = nil; profile:EndSession() end
	end)
end

function DataService:PlayerAdded(player: Player)
	local profile = store:StartSessionAsync(`Player_{player.UserId}`, { Cancel = function() return player.Parent ~= Players end })
	if profile == nil then
		failed[player] = true
		player:Kick("We couldn't load your data. Please rejoin in a moment.")
		return
	end
	if not migrate(profile.Data :: any) then -- migrate BEFORE Reconcile
		failed[player] = true
		profile:EndSession()
		player:Kick("This server is out of date. Please rejoin to get the latest version.")
		return
	end
	profile:AddUserId(player.UserId)
	profile:Reconcile()
	profile.OnSessionEnd:Connect(function()
		profiles[player] = nil
		player:Kick("Your data was loaded on another server. Please rejoin.")
	end)
	if player.Parent ~= Players then profile:EndSession(); return end
	profiles[player] = profile
	player:SetAttribute("DataLoaded", true) -- clients wait for this before showing currency UI
end

function DataService:GetProfile(player: Player): Profile?
	local profile = profiles[player]
	return if profile ~= nil and profile:IsActive() then profile else nil
end

function DataService:WaitForProfileAsync(player: Player, timeoutSeconds: number): Profile?
	local deadline = os.clock() + timeoutSeconds
	while player.Parent == Players and not failed[player] and os.clock() < deadline do
		local profile = self:GetProfile(player)
		if profile ~= nil then return profile end
		task.wait(0.1)
	end
	return self:GetProfile(player)
end

function DataService:Update(player: Player, mutator: (data: PlayerData) -> ()): boolean -- mutator must not yield
	local profile = self:GetProfile(player)
	if profile == nil then return false end
	mutator(profile.Data :: any)
	return true
end

return DataService
```

A failed load kicks; it never falls through to default data, because defaults would be saved over the real profile. Schema rules: additive changes need only a template change plus `Reconcile`; renames and type changes need a migration and ship with Migrate To Latest Update; migrations are pure and never edited after shipping; test them against copies of real data.

## Developer products: idempotent ProcessReceipt

Facts `[VS]`: set `MarketplaceService.ProcessReceipt` exactly once from one script (a second assignment silently replaces the first). It runs after purchase and again on every join for unacknowledged receipts; there is no time-based retry. It can yield. The same receipt can be processed on two servers at once, so dedupe in saved data, not server memory. Returning `PurchaseGranted` acknowledges; `NotProcessedYet` or an error keeps it pending. Never grant from `PromptProductPurchaseFinished`. Roblox reviews weak implementations in Creator Hub.

Official flow: wait for session-locked data on this server; if the `PurchaseId` is already in **saved** data return `PurchaseGranted`; grant in memory; record the `PurchaseId`; save; return `PurchaseGranted` only once the save succeeds.

```lua
--!strict
-- ServerScriptService/Server/Services/ReceiptService.luau (the ONLY assigner of ProcessReceipt)
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local DataService -- resolved in Init

local PURCHASE_ID_LIMIT = 100
local LOAD_TIMEOUT = 30
local SAVE_CONFIRM_TIMEOUT = 25

type Grant = (player: Player, data: any, receipt: { [string]: any }) -> () -- synchronous; validate before mutating
local GRANTS: { [number]: Grant } = {
	[1111111] = function(_p, data) data.Cash += 1000 end,
	[2222222] = function(_p, data) -- 2x Cash 10 min: extend, never stack
		data.Boosts.DoubleCash = math.max(data.Boosts.DoubleCash or 0, os.time()) + 600
	end,
	[3333333] = function(_p, data) -- Starter Pack
		data.Cash += 500
		data.Inventory.StarterSword = (data.Inventory.StarterSword or 0) + 1
		data.Entitlements.StarterPack = true
	end,
}

local function isSaved(profile: any, purchaseId: string): boolean
	local saved = profile.LastSavedData
	local ids = if saved then saved.PurchaseIds else nil
	return ids ~= nil and table.find(ids, purchaseId) ~= nil
end

local function confirmSavedAsync(profile: any, purchaseId: string): boolean
	local deadline = os.clock() + SAVE_CONFIRM_TIMEOUT
	while profile:IsActive() and os.clock() < deadline do
		if isSaved(profile, purchaseId) then return true end
		local finished = false
		local connection = profile.OnAfterSave:Connect(function() finished = true end)
		profile:Save()
		local waitUntil = math.min(deadline, os.clock() + 10)
		while not finished and profile:IsActive() and os.clock() < waitUntil do task.wait(0.2) end
		connection:Disconnect()
	end
	return isSaved(profile, purchaseId)
end

local function processReceipt(receipt: { [string]: any }): Enum.ProductPurchaseDecision
	local purchaseId = receipt.PurchaseId :: string
	local productId = receipt.ProductId :: number
	local player = Players:GetPlayerByUserId(receipt.PlayerId :: number)
	if player == nil then return Enum.ProductPurchaseDecision.NotProcessedYet end
	local grant = GRANTS[productId]
	if grant == nil then warn(`[Receipt] No grant for product {productId}`); return Enum.ProductPurchaseDecision.NotProcessedYet end
	local profile = DataService:WaitForProfileAsync(player, LOAD_TIMEOUT)
	if profile == nil then return Enum.ProductPurchaseDecision.NotProcessedYet end
	local data = profile.Data -- no yields from here until the record is written
	if table.find(data.PurchaseIds, purchaseId) == nil then
		local ok, err = pcall(grant, player, data, receipt)
		if not ok then warn(`[Receipt] Grant failed {purchaseId} ({productId}): {err}`); return Enum.ProductPurchaseDecision.NotProcessedYet end
		table.insert(data.PurchaseIds, purchaseId)
		while #data.PurchaseIds > PURCHASE_ID_LIMIT do table.remove(data.PurchaseIds, 1) end
	end
	return if confirmSavedAsync(profile, purchaseId) then Enum.ProductPurchaseDecision.PurchaseGranted else Enum.ProductPurchaseDecision.NotProcessedYet
end

local ReceiptService = {}
function ReceiptService:Init()
	DataService = require(script.Parent.DataService)
	MarketplaceService.ProcessReceipt = function(receipt)
		local ok, result = pcall(processReceipt, receipt)
		if ok then return result end
		warn(`[Receipt] Unhandled error: {result}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end
end
return ReceiptService
```

`[VS]` `MarketplaceService:BindReceiptHandler(receiptType, handler, filter?)` is the newer per-type API (`Enum.ReceiptType.DeveloperProduct`, `RobuxTransferSender`, `RobuxTransferReceiver`; returns `Enum.ReceiptDecision.Processed` or `NotProcessedYet`; unmatched receipts fall through to `ProcessReceipt`). Same idempotency rules. Keep the pattern above as the baseline.

## Game passes

- Check on the server with `UserOwnsGamePassAsync(userId, passId)`; results are engine-cached and transparently batched, so `task.spawn` all checks at join.
- Listen to `PromptGamePassPurchaseFinished` on the server; when `purchased` is true, apply the perk immediately.
- Cache `true` for the session; re-check a cached `false` after a TTL (60 s) so website purchases appear; never cache a failed check.
- Apply character perks on every `CharacterAdded`. Expose perks through attributes (`player:SetAttribute("VIP", true)`) and also honour `data.Entitlements[pass]` from gifts.

```lua
local NEGATIVE_TTL = 60
type Entry = { owned: boolean, checkedAt: number }
local cache: { [Player]: { [number]: Entry } } = {}
function PassService:OwnsAsync(player: Player, passId: number): boolean
	local perPlayer = cache[player] or {}; cache[player] = perPlayer
	local entry = perPlayer[passId]
	if entry ~= nil and (entry.owned or os.clock() - entry.checkedAt < NEGATIVE_TTL) then return entry.owned end
	local ok, result = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, player.UserId, passId)
	if not ok then warn(`[Pass] check failed ({player.UserId}, {passId}): {result}`); return if entry ~= nil then entry.owned else false end
	perPlayer[passId] = { owned = result == true, checkedAt = os.clock() }
	return result == true
end
```

## Subscriptions, gifts, boosts, prices

- Subscriptions: `GetUserSubscriptionStatusAsync(player, subscriptionId)` → `{ IsSubscribed, IsRenewing }`; listen to `Players.UserSubscriptionStatusChanged`; fail closed.
- Gift passes are developer products granting `Entitlements[pass] = true` in the recipient's data. Store the intended recipient as a pending gift in the **buyer's** profile before prompting (receipts carry only the buyer's id and may replay on another server). In the grant, mutate the recipient's loaded profile, or send `store:MessageAsync(recipientKey, { type = "gift", item = "VIP", giftId = purchaseId })` and dedupe by `giftId` in the recipient's handler. Because `MessageAsync` yields, give gift products their own branch that sends first and returns `NotProcessedYet` if it fails, then records the `PurchaseId`. Gate with `GetUsersPriceLevelsAsync` (the docs disagree on its return shape; log and verify `[VS]`).
- Timed boosts store a UTC expiry (`os.time()`), extend on repurchase, and apply in server reward code only. Server-wide boosts live server-side with an expiry announced through an attribute.
- Prices: `GetProductInfoAsync(id, Enum.InfoType.Product or GamePass).PriceInRobux`; regional pricing means players see different prices. `RankProductsAsync` once at join.

## Teleports, reserved servers and messaging

- Server-only `TeleportService:TeleportAsync(placeId, players, options)` in `pcall` with retries; handle `TeleportInitFailed` (`Flooded` → wait 15 s, `Failure` → wait 1 s, cap 3 retries).
- `[VS]` `ReserveServer`, `ShouldReserveServer` and `ReservedServerAccessCode` are deprecated. Use `options.ReservedServerId = HttpService:GenerateGUID(false)` (first teleport creates the server, later ones join), `options.VipServerId = game.PrivateServerId`, or `options.ServerInstanceId = jobId`. Setting more than one target field errors.
- Detect a reserved server with `game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0`.
- Teleport data is client-visible and tamperable; read `player:GetJoinData().TeleportData` as a hint only and keep rosters in a MemoryStore hash map keyed by the reserved server id. Match servers reject anyone not on the roster.
- `TeleportService:SetTeleportGui(gui)` and `GetArrivingTeleportGui()` for a custom loading screen. Call `player:RequestStreamAroundAsync(position)` before in-place teleports.
- Custom matchmaking: lobby servers write tickets to a MemoryStore sorted map or queue sharded by mode; one matchmaker (elected via a MemoryStore lock) groups tickets, writes the match record to a hash map, and calls the teleport. Queue reads hide items for 30 s, so ticket removal must be idempotent.
- MemoryStore limits `[VS]`: quota 64 KB + 1.2 KB × users; 1,000 + 120 × CCU request units per minute; about 30,000 units per partition per minute; 1,000,000 items and 100 MB per structure; 32 KB values; 128-character keys; 45-day max expiry; queue invisibility timeout 30 s. Not durable.
- MessagingService limits `[VS]`: 1 kB messages; 600 + 240 × players sends per server per minute; 40 + 80 × servers receives per topic per minute; 20 + 8 × players subscriptions per server. Use it for hints only; receivers re-read authoritative state. Validate `message.Data` like a remote payload. Open Cloud `PublishUniverseMessage` and `RestartUniverseServers` exist for live-ops tooling.

## Level-up audit: how to check an existing game

1. **Dashboards.** Monitoring > Data Stores: non-200 statuses, throttles, quota usage per request type, storage against the limit. Error report: queue and throttle warnings at peak hours.
2. **Static scan** with sketch E, then read three paths by hand: load (what happens when it fails?), save (leave, shutdown, autosave), purchase (one handler, idempotent, grant recorded before acknowledging).
3. **Measure a heavy profile** on a test server: `#HttpService:JSONEncode(value)` against 4,194,304; find what grows without a cap (logs, id lists, placed objects).
4. **Rollback drill** in a test universe: restore one key with `ListVersionsAsync` + `GetVersionAsync` (or Revert in the Data Stores Manager). Take an Open Cloud snapshot before every update that changes save logic.
5. **Fix order:** failed load that saves defaults; missing session lock in a game with trading; non-idempotent receipts; `SetAsync` on shared keys and reads during gameplay; leaderboard write rate; versioned migrations; RTBF templates.
6. **Moving a live game to ProfileStore or Lyra** is never a big bang: on first load read the old key, write the new one, mark the profile as migrated, leave the old key untouched for at least 30 days, and rehearse on copies of real data. For DataStore2 use Roblox's beta migration tool `[official]`.

Sketch E, data and purchase call sites (unexecuted sketch; read-only; command bar or Studio MCP `execute_luau`, Edit):

```lua
--!strict
local ScriptEditorService = game:GetService("ScriptEditorService")
local CHECKS = {
	{ "SetAsync: lost updates when two servers write", ":SetAsync%(" }, { "GetAsync: load-time only", ":GetAsync%(" },
	{ "ProcessReceipt assignment: exactly one", "ProcessReceipt%s*=" }, { "PromptProductPurchaseFinished: never grant here", "PromptProductPurchaseFinished" },
	{ "GetDataStore", "GetDataStore%(" }, { "GetOrderedDataStore", "GetOrderedDataStore%(" }, { "BindToClose", "BindToClose" },
	{ "DataStore2: legacy", "DataStore2" }, { "ProfileService: superseded", "ProfileService" },
}
local totals: { [string]: number } = {}
for _, root in { game:GetService("ServerScriptService"), game:GetService("ServerStorage"), game:GetService("ReplicatedStorage") } :: { Instance } do
	for _, d in root:GetDescendants() do
		if not d:IsA("LuaSourceContainer") then continue end
		local source = ScriptEditorService:GetEditorSource(d)
		for _, check in CHECKS do
			local n = select(2, string.gsub(source, check[2], ""))
			if n > 0 then totals[check[1]] = (totals[check[1]] or 0) + n; print(n, check[1], d:GetFullName()) end
		end
	end
end
print(totals) -- more than one store name per player, or zero BindToClose with no library, are findings
```

| Symptom | Likely cause | Fix |
|---|---|---|
| Full wipes reported after an outage | Failed load fell back to default data, then autosave wrote it | Kick on failed load; never save an unloaded profile; restore from versions |
| Last minutes lost on leave or shutdown | No final save, or it failed; autosave too rare | Library session end and shutdown handling; autosave every 3–5 min (the official sample uses 180 s) |
| Duplicated items after trades | Two independent saves; no session lock; one side rolled back on purpose | Both profiles locked on one server, mutate with no yield, save both; escrow or a transaction library across servers; log trade ids |
| Robux spent and nothing granted, or granted twice | Grant in `PromptProductPurchaseFinished`; `PurchaseGranted` before the save; second `ProcessReceipt` assignment; no `PurchaseId` dedupe in saved data | The ReceiptService pattern above |
| Throttle errors at peak | Reads or writes during gameplay; leaderboard written on every change; every server polling one key | Buffer in memory; throttle ordered writes; jitter; shard hot read keys |
| Storage near the limit | One data store per player (DataStore2, "Berezaa method"); dead test data; uncapped arrays | Official migration packages; delete test stores; cap lists |
| Saves fail only for veterans | Profile near 4 MB, or over 4 MB per minute of writes on one key | Prune; split into a few deterministic keys; or an auto-sharding library |
| "Loaded on another server" kicks | Stale lock after a crash, or teleports that do not wait for the old session to end | Let the library time the lock out; never `Steal`; end the session before teleporting |

## Review gate (data and purchases)

- [ ] Session-locked loading; a failed load never saves; the player is kicked or the profile marked unsaveable.
- [ ] Migrations run before `Reconcile`; newer-schema guard present; key pattern unchanged.
- [ ] No DataStore reads during gameplay; autosave staggered; no custom BindToClose on top of ProfileStore.
- [ ] `UpdateAsync` transforms never yield; metadata and user ids re-passed; failed writes verified with `UseCache = false`.
- [ ] Leaderboard writes throttled; `leaderstats` display only; trades mutate both locked profiles synchronously.
- [ ] Exactly one `ProcessReceipt` (or filtered handlers); dedupe by `PurchaseId` in saved data; `PurchaseGranted` only after confirmed save; `NotProcessedYet` on absent player, unloaded data, unknown product, failed grant or save.
- [ ] Nothing granted from `PromptProductPurchaseFinished`; pass ownership checked on the server and cached correctly.
- [ ] Prices from `GetProductInfoAsync`; gifts gated by price level; boosts extend, never stack.
- [ ] RTBF templates cover every user-keyed store (exact `{UserId}` token; `scope_pattern` "global" for default scopes).
- [ ] Snapshot taken before any update that changes save logic; restore drill done in a test universe; Data Stores dashboard checked at peak.

Grep `references/knowledge-base.md` for `## 4.6`, `## 4.7` and `## 4.8`.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/cloud-services/data-stores/{best-practices,error-codes-and-limits,versioning-listing-and-caching,observability,data-stores-manager,right-to-be-forgotten,player-data-purchasing}.md`, `cloud-services/extended-services.md`, `cloud-services/memory-stores/index.md` (read)
- https://github.com/MadStudioRoblox/ProfileStore, https://github.com/MadStudioRoblox/ProfileService, https://github.com/paradoxum-games/lyra, https://github.com/nezuo/lapis, https://github.com/Kampfkarren/Roblox (DataStore2) (read: README and last commit)
- Limits and Extended Services (search summary): https://devforum.roblox.com/t/datastores-access-and-storage-updates/3597255, https://devforum.roblox.com/t/extended-services-for-data-stores-is-now-available/4504347, https://devforum.roblox.com/t/extended-services-update/4070634, https://devforum.roblox.com/t/weekly-recap-july-13-%E2%80%93-17-animation-graphs-go-live-5%C3%97-more-data-store-storage/4743286
- Libraries, dupes and migration (search summary): https://devforum.roblox.com/t/datastores-migration-packages-for-the-berezaa-method-and-datastore2-module-public-beta/3631514, https://devforum.roblox.com/t/session-locking-explained-datastore/846799, https://devforum.roblox.com/t/exploiting-how-to-prevent-exploiters-from-abusing-data-store-rollbacks-and-sanitizing-against-data-store-vulnerabilities/2019989, https://devforum.roblox.com/t/what-is-the-best-datastore-module-to-use-currently/3598021, https://devforum.roblox.com/t/should-i-use-profilestore-or-profileservice/3871636
- No evidence found: a public post-mortem of a specific large data-loss or dupe incident with numbers.
