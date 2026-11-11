# Data, purchases, teleports and cross-server systems

What this is: player data (ProfileStore), DataStore and MemoryStore limits, idempotent receipts, game passes, gifts, teleports and messaging. Open it when building the data layer, or jump to "Level-up audit" when a live game loses data, dupes items or throttles. Distilled from knowledge-base sections 4.6, 4.7 and 4.8; limits, API signatures and the ProfileStore API re-checked at source on 2026-11-11 (`Roblox/creator-docs`, DevForum staff posts, `ProfileStore.luau`). Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`, `[lihfolk]` adapted from LihFolk Vault V2.

Contents: Start here by level · Choosing a storage service · DataStore limits · Practices that prevent data loss · Duplication: four classes and the commit pattern · ProfileStore essentials · DataService with schema migration · Runbook: shipping a schema migration · Runbook: data incident and rollback · Runbook: dupe incident · Developer products: idempotent ProcessReceipt · Game passes · Subscriptions, gifts, boosts, prices · Teleports, reserved servers and messaging · Level-up audit · Review gate · Sources

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | (1) Use ProfileStore with the DataService below; do not write raw `SetAsync` code. (2) If loading fails, kick; never play on default data that could save. (3) One key per player, `Player_{UserId}`. (4) Grant paid products only in `ProcessReceipt`, with the ReceiptService below. (5) Test in a separate universe or with `store.Mock` | Trading, MemoryStore, cross-server systems |
| Intermediate | Schema version plus migrations with fixture tests; staggered autosave; item GUIDs; snapshot before data releases; RTBF templates; Data Stores dashboard at peak | Marketplaces, custom session locks |
| Expert | Two-profile commits with a decision record; `MinReader` and expand-then-contract releases; bulk restore drills; ownership index for rare items; rate-limit budgets per request type under load | Nothing: read it all |

Terms: a *profile* is one player's saved table. A *session lock* (or lease) marks which server currently owns a profile so two servers cannot write it. A *schema* is the shape of the saved table; a *migration* upgrades an old shape. *Idempotent* means running it twice has the same effect as once. Related: gameplay-systems-cookbook.md (§1 Wallet, §2 Inventory, §3 Shop and §17 Trading are built on the DataService and ReceiptService here); monetization-and-policy.md (product set, boost rules, refunds and clawback policy); economy-and-progression.md (what the saved numbers mean); networking-and-security.md (RemoteGuard); debugging-and-testing.md (migration and receipt tests).

## Choosing a storage service

| Need | Use |
|---|---|
| Player progress, inventory, currency, purchase history | Standard DataStore through a session-locking library (ProfileStore by default; see library status below) |
| Global leaderboards | Ordered DataStore (integers only), cached and refreshed every few minutes |
| Matchmaking queues, server lists, cross-server locks, trade escrow | MemoryStore (sorted map, queue, hash map); expires within 45 days |
| Broadcast hints (announcements, "refresh your cache") | MessagingService (best effort, about 1 KB) |
| Live feature flags and tuning | Configs (read-only at runtime; "Publish now" reaches servers in about 15 s to 1 min, clients can take a few minutes `[official]` `[VS]`) |
| API keys and tokens | Secrets store |

All cloud services are server-only. Studio needs "Enable Studio Access to API Services"; use a separate test universe so Studio never touches live data.

## DataStore limits `[VS]`

- Names, keys and scopes: 50 characters. Value: 4,194,304 characters of JSON per key. Metadata: 300 characters total. Per-key throughput: 25 MB/min reads, 4 MB/min writes, each request rounded up to the next KB.
- Experience-level per-minute limits (shared with Open Cloud): Read 300 + CCU×40; Write 300 + CCU×20; List 300 + CCU×2; Remove 300 + CCU×40. `UpdateAsync` costs one read and one write.
- Per-server defaults per minute: standard Read/Write/Remove 60 + players×40, List 5 + players×2; ordered Read 60 + players×40, Write and Remove 30 + players×5, List 5 + players×2. These are now a creator tool: `DataStoreService:SetRateLimitForRequestType` changes them and `GetRequestBudgetForRequestType` reads what is left. A throttled request waits in a per-type queue of 30; past that it fails. Errors tell you which layer throttled: `…GameServerThrottled` (server limit or full queue), `…ExperienceThrottled`, `KeyThrottled`, `DatastoreThrottled` `[official]`. The server default allows 40 writes per player-minute but the experience budget only 20: a game that spends its server budget on writes is throttled at experience level.
- 2026 changes `[official: DevForum staff posts, read]`: storage limits active from 9 April 2026 and experience-level access limits rolled out 9–23 April; in July the in-game and Open Cloud budgets merged into one per-experience budget and base storage rose from 100 MB to 500 MB. Going over the storage limit does not fail writes: after notices and a 2-week grace period the overage is deducted from the owner's Robux (or billed through Extended Services), and an experience that cannot pay is unpublished. Conflict: the Extended Services pricing table in the docs still shows the older defaults (250, 100 and 10 request baselines; 100 MB). Trust the limits page and your dashboard.
- Above the defaults: Extended Services (paid; owner 18+, ID-verified, supported country). Standard stores per million requests: Get $0.08, Set $0.80, List $0.60, Remove $0.80; storage $0.12 per GB-month; monthly budget from $0.50, throttled when it runs out `[official]`. Reduce requests and storage first.
- Operations tools `[official]`: Monitoring > Data Stores (requests by API and status, quota usage, storage); Configurations > Data stores manager (browse keys, compare and revert versions, mark for deletion with a 30-day restore window, RTBF templates); Open Cloud Snapshot Data Stores (once a day; take one before any update that changes save logic); `GetVersionAtTimeAsync`; the Data Stores Batch Processor CLI for bulk repairs.
- Storage quota: 500 MB + 1 MB × lifetime users, counting the compressed latest version of each key (do not pre-compress; old versions do not count).
- Key error codes: 101/102 key name; 103/104 unserialisable value (functions, Instances, cycles, mixed tables, NaN); 105 too large; 301–306 throttled; 401/402 during shutdown; 403 no Studio access; 404 and 501–505 internal (retry with backoff and verify); 511–513 metadata or user-id errors.
- A failed write may have succeeded `[official]`. Confirm with `DataStoreGetOptions.UseCache = false` before refunding or retrying anything non-idempotent (`GetAsync` serves a 4-second cache).

## Practices that prevent data loss

- One key per player, static pattern `Player_{UserId}`. Never change the key pattern without a migration. Keep numeric `UserId` keys even though `Player.User` exists `[VS]`.
- Load once, buffer in memory, never read during gameplay. Autosave every 3–5 minutes with a random initial offset; save immediately after purchases.
- Prefer `UpdateAsync` for anything several servers could write; the transform must not yield, may run more than once, and returning `nil` cancels. Metadata and user ids must be re-passed on every write.
- Retries: exponential backoff with jitter (1, 2, 4, 8 s ± 25%), 3–5 attempts, in order per key.
- Serialisable data only: pure arrays or all-string-key tables, no `nil` holes, no Instances or `Vector3`/`CFrame`/`Color3`, no NaN or inf, valid UTF-8, no cycles. Cap player-supplied strings and key counts before they enter saved data.
- Versioning: one version per key per UTC hour, overwritten versions kept 30 days; `ListVersionsAsync` and `GetVersionAsync` are your backup and restore.
- Ordered stores have no versioning or metadata; write leaderboard values at most every few minutes and on leave; `leaderstats` is display, never storage.
- `game:BindToClose` gives 30 seconds; ProfileStore already handles shutdown, so do not add your own save loop on top.
- Three load outcomes, kept distinct `[lihfolk]`: loaded; new (the read succeeded and returned nothing); failed (error or lock timeout). Only the first two ever get a save path. A thrown error is never "new player".
- Tell the player when data is unhealthy: set an attribute, show a banner that stays up, and show no purchase prompts while the profile cannot save `[lihfolk]`.
- Count load results (new, loaded, failed, locked) and save results per server and send aggregates to analytics. A rising locked rate means sessions are not being released; a rising validation-failure rate means a bug is producing bad data `[lihfolk]`.
- Auditing a hand-rolled session lock in an existing game `[lihfolk]`: the lock must be read and renewed inside the same `UpdateAsync` that writes the data; every save carries the session's token so a server that lost the lock stops writing; leases under about 30 s are unsafe (clock skew); autosave no longer than a third of the lease (their reference: 90 s lease, renewed every 30 s). Conflict: LihFolk builds its own lease module; this skill keeps ProfileStore for new games because it is the more widely exercised implementation, and uses these numbers only to judge custom code.
- Right to be forgotten: RTBF deletion templates in Creator Hub (up to 100), using the `{UserId}` token; call `profile:AddUserId(userId)` so metadata lists the owner; data keyed otherwise needs a webhook handler.

## Duplication: four classes and the commit pattern

Adapted from `[lihfolk]`. Knowing the class tells you where to look; class 1 is fixed in code, classes 2–4 in architecture.

| Class | Mechanism | Typical trigger | Fix |
|---|---|---|---|
| 1. In-server race | Two requests pass a check before either writes, because the handler yields in between | Double click, two remotes in one frame | Synchronous core: read, validate, write with no yield; busy lock shared across trade, sell, equip |
| 2. Save-boundary split | Two profiles change in memory, only one saves before a crash or leave | Server dies right after a trade | One-way transfer (gift, mail): debit the giver and confirm that save **before** crediting the receiver, so a crash destroys rather than duplicates, and the giver's ledger or outbox entry lets a retry or support restore it. Two-way swap: no save order is safe (whichever side saves first, a crash leaves one item in two profiles), so use the commit protocol below |
| 3. Cross-server overlap | One profile live on two servers | Fast rejoin, teleport, a writer that ignores the lock (admin tool, Studio session, "load anyway" fallback) | Session lock respected by every writer; audit them with sketch E |
| 4. Rollback abuse | The player moves value out, then gets their own save reverted | "Restore my data" support requests; a forced failed save | Restores never bring back items the ledger shows left after the restore point; check item GUIDs |

- **Plan, validate, apply, record.** Express every economic action as a list of changes; validate it against current state; apply it synchronously; append a ledger entry (action, changes, resulting balance, time, `game.JobId`, `game.PlaceVersion`). Keep the last 50–200 entries in the profile for support and repair.
- **Item identity.** Every non-stackable item gets a GUID at creation (`HttpService:GenerateGUID(false)`), used as the inventory key and never regenerated on transfer, with `source` and `acquiredAt`. The same GUID usable in two inventories is proof of a dupe and identifies exactly the copies (the one exception: a copy still locked under a committed trade id is waiting to settle, see the protocol below). For rare items add an ownership index (a key per GUID, updated with `UpdateAsync` on transfer); it costs one write per transfer.
- **Validate on load.** Saved data crosses a trust boundary to every future server: currencies finite, non-negative integers under a cap well below 2^53 (doubles stop being exact there; some "dupes" are rounding); every item id known; rare-item counts plausible for account age. Repair obvious corruption from the ledger, quarantine suspicious items and log. Never wipe. *Quarantine* has one meaning in this skill: the item is kept and stays usable, but is untradeable and flagged with the incident or review id until a person decides; removal is reserved for accounts with direct evidence (dupe runbook below).
- **Refuse broken saves.** Before writing, reject a profile that fails the same invariants, keep the last good version as latest, and alert `[lihfolk]`.

### Two-profile commit protocol (canonical: trades, swaps, steals)

Use it wherever two profiles must change together; every other file links here, so do not build from a shorter summary. Preconditions: both profiles session-locked on this server and `IsActive()`; every item has an immutable GUID; every code path that consumes **or changes** an item refuses one whose `Lock` is set; nothing else moves value into another profile except this protocol or a one-way transfer whose debit save was confirmed first. Currency in a trade is escrowed the same way: moved out of the balance into the pending entry at step 1, paid to the peer from the record at step 3, returned on abort. Trade ids are `<UTC yyyymmdd>-<GUID with the hyphens removed>` (41 characters): the key `Trade_<id>` is then 47 characters, under the 50-character key limit (a hyphenated GUID makes it 51 and every write fails with error 102), and one day's records list by the prefix `Trade_<yyyymmdd>`. The journal idea is adapted from `[lihfolk]` and matches DevForum practice `[community]`; the abort tombstone, the single settle mutation and the recovery rules are this skill's corrections `[house]`.

| Step | Action | Invariant it protects | Crash or failure after this step |
|---|---|---|---|
| 1 Intent | In each profile, one mutation: `PendingTrades[id] = { peer, give = { guid } }` and `Lock = id` on every given item. Save both profiles and confirm both saves (the `LastSavedData` check used by `confirmSavedAsync` in the receipt code below) | Before anything is decided, each profile's **saved** state says "these items are reserved for this trade", so no profile can forget it was in one | Nothing has moved. A profile that loads with the pending id finds no record: recovery writes `aborted`, then unlocks |
| 2 Decide | One `UpdateAsync` on `Trade_<id>`: if the key is empty, write `{ state = "committed", a, b, fromA, fromB, t }` with full item records (without `Lock`); if it already holds anything, return `nil` and use what is there | The record is the only truth and is write-once: exactly one of `committed` or `aborted` ever exists. A slow or hung server cannot commit after a peer aborted, and a peer cannot abort after a commit | The trade is real. Both profiles are unsettled and locked; each rolls forward when it loads |
| 3 Settle | In each profile, one synchronous mutation, idempotent by trade id: if `PendingTrades[id]` is absent, do nothing; otherwise remove the given GUIDs, add the received items whose GUID is not already present (never refused for bag space: the peer has already given theirs up), clear locks, delete `PendingTrades[id]`, append a ledger entry. Save both | "Applied" and "no longer pending" are one saved write, so a saved profile is either pending and unapplied or settled, never applied and still pending. Roll-forward therefore cannot re-add an item that has since moved on | One side settled, the other pending: the unsettled side still holds its old items **locked**, and settles on load. This is the only state in which a GUID sits in two profiles, and the locked copy cannot be used or traded |
| 4 Acknowledge | Best effort, and only **after that side's settle save is confirmed** (same `LastSavedData` check): add `ackA` or `ackB` to the record without changing `state` or the item lists | Tells a cleanup job that both sides settled. An early acknowledgement is a dupe: the record is deleted, the unsaved side reloads still pending, finds an empty key, aborts and unlocks items the peer already received | None for correctness |

Recovery runs on every profile load, before trading unlocks and before any inbound gift or mail message is applied (a returning item must not meet its own locked copy), for each pending id that is not owned by a live commit on this server:

1. Run the step-2 update proposing `{ state = "aborted" }`. An empty key is **filled with the tombstone first**, so a commit that arrives later fails its compare-and-set.
2. The record says `committed`: settle (roll forward; never roll back, because the peer may already have used the items). It says `aborted`: clear the locks and the pending id in one mutation.
3. The call errored, was throttled or timed out: the outcome is unknown. Leave the items locked and the pending id in place, tell the player the trade is being verified, and retry with backoff and on the next load. Never unlock on a guess.

Live-path rules: a failed or unconfirmed intent save goes through recovery step 1 (write `aborted`, then unlock), never straight to unlock; an unknown result from step 2 is retried with the same proposal (the update is idempotent) and otherwise left locked; a record that turns out `aborted` is settled as aborted; a profile that is no longer `IsActive()` is left to its own recovery; at step 3 the commit looks each side's profile up again by `UserId`, because a player who left and rejoined this server mid-commit has a new profile object whose recovery skipped the trade as live (when the commit ends, re-run recovery for any id it skipped); `PlayerRemoving` should wait for an in-flight commit before `EndSession` (the DataService below ends the session at once, which is safe but leaves the items locked until the next load), with a timeout that leaves the pending id in place; shutdown starts no new commits. Log every step with trade id, both user ids, GUIDs, `game.JobId`, `game.PlaceVersion` and the decision state.

```lua
--!strict
-- Unexecuted sketch, never run. Do not ship without the fault-injection test described below.
-- PlayerData is extended with Items: { [guid]: Item }, PendingTrades: { [id]: { peer: number, give: { string } } }, Ledger.
-- DataStoreService, scheduleRetry (backoff, then recoverAsync again) and the live-commit table come from the surrounding module.
local tradeLog = DataStoreService:GetDataStore("TradeLog_v1")
type Decision = { state: "committed" | "aborted", a: number?, b: number?, fromA: { [string]: any }?, fromB: { [string]: any }?, t: number }
-- Write-once compare-and-set. Returns what the record now holds, or nil when the outcome is unknown (stay locked, retry).
local function decideAsync(tradeId: string, proposal: Decision): Decision?
	local stored: Decision? = nil
	local ok = pcall(function()
		tradeLog:UpdateAsync("Trade_" .. tradeId, function(current: Decision?) -- may run more than once; the last run wins
			if current ~= nil then stored = current; return nil end -- already decided: never overwrite
			stored = proposal
			return proposal
		end)
	end)
	return if ok then stored else nil -- an error may hide a write that succeeded: the retry then reads it back
end
-- Step 3. One synchronous mutation per profile; applying and clearing the pending id cannot be saved apart.
local function settle(data: any, tradeId: string, decision: Decision, userId: number)
	local pending = data.PendingTrades[tradeId]
	if pending == nil then return end -- already settled here: a second call changes nothing
	if decision.state == "committed" then
		local isA = userId == decision.a
		for guid in (if isA then decision.fromA else decision.fromB) :: { [string]: any } do data.Items[guid] = nil end
		for guid, item in (if isA then decision.fromB else decision.fromA) :: { [string]: any } do
			if data.Items[guid] == nil then data.Items[guid] = table.clone(item) end
		end
	end
	for _, guid in pending.give do -- aborted: unlock what is still here; committed: nothing left to unlock
		local item = data.Items[guid]
		if item ~= nil and item.Lock == tradeId then item.Lock = nil end
	end
	data.PendingTrades[tradeId] = nil
	table.insert(data.Ledger, { t = os.time(), trade = tradeId, state = decision.state, job = game.JobId })
end
local function recoverAsync(player: Player, profile: any, liveTrades: { [string]: true })
	local ids = {}
	for tradeId in profile.Data.PendingTrades do table.insert(ids, tradeId) end -- snapshot: the loop yields
	for _, tradeId in ids do
		if liveTrades[tradeId] then continue end
		local decision = decideAsync(tradeId, { state = "aborted", t = os.time() }) -- empty key: tombstone written FIRST
		if not profile:IsActive() then return end
		if decision == nil then scheduleRetry(player, tradeId); continue end -- unknown: stay locked
		settle(profile.Data, tradeId, decision, player.UserId)
	end
	profile:Save()
end
```

Cost, stated plainly: 5 `UpdateAsync` calls per trade (two intent saves, one decision, two settle saves), 7 with acknowledgements, each counting one read and one write against the budgets above, plus one read-or-abort per pending id on load. A 20-player server has 860 writes a minute by default and those 20 players add 400 to the experience budget, so 10 trades a minute use 50–70 of either. It is three sequential round trips, so a commit takes seconds: show "completing trade", and let a timeout leave items locked, never unlocked. Records are roughly 0.5–2 KB of cross-player data `[house]`: delete a committed record only when both acknowledgements are present **and** it is older than the 30-day version-restore window (a profile restored to a point before its settle is pending again and must still find the record), and a tombstone only after 30 days (a late reload then just writes a fresh one). RTBF templates match keys by `{UserId}` and cannot find these records, so keep a per-user list of trade ids for erasure, and for a record that is not fully acknowledged blank the requester's id and keep the record: deleting it lets the peer abort a trade that was committed.

What it does not guarantee:

- **Atomicity.** There is a window in which one side has settled and the other is locked. A player who never returns leaves a locked copy at rest (and a committed record that can never be deleted), so dupe scans must ignore copies locked under a committed id.
- **Liveness.** While the trade-log store is unreadable, the items stay locked.
- **Classes 3 and 4.** A writer that ignores the session lock still dupes. Restoring a profile to a version from before a trade resurrects the items it gave away: restore tools must replay that user's committed records after the restore point.
- **Split profiles.** It relies on a profile being one key saved whole; a sharded or multi-key profile breaks step 3.
- **Correctness of this text.** It is a design reviewed on paper, not production-proven code. A transaction library (Lyra's `txAsync`, see library status) is the alternative to evaluate.

Fault-injection test, required before shipping: with `ProfileStore.Mock` and a mock trade-log store, abandon the commit after each of these points: one intent save, both intent saves, the decision write, one settle save, both settle saves, one acknowledgement. Also make the decision write throw after it succeeded; delay step 2 while the peer's profile loads on a second mock server and recovers; rejoin the same server mid-commit; end both sessions mid-commit; run the record cleanup between every pair of steps. After each case load both profiles through recovery and assert: every GUID is unlocked in exactly one profile; no profile has the trade applied and still pending; item counts are conserved; a second recovery pass changes nothing.

## ProfileStore essentials

- `ProfileStore.New(storeName, template)`; `store:StartSessionAsync(key, { Cancel = fn })` returns a `Profile` or `nil` (also `nil` once shutdown has begun), and throws if that key already has a session on this server.
- Constants (adjust with `ProfileStore.SetConstant`): `AUTO_SAVE_PERIOD = 300`, `FIRST_LOAD_REPEAT = 5`, `LOAD_REPEAT_PERIOD = 10`, `SESSION_STEAL = 40`, `ASSUME_DEAD = 630`, `START_SESSION_TIMEOUT = 120` (disabled when a `Cancel` function is passed). Never pass `{ Steal = true }` in normal loading.
- `profile.Data` saves while `profile:IsActive()` is true; the guarantee does not survive a yield. Check, then write immediately.
- `profile:EndSession()` on `PlayerRemoving`: the profile is inactive at once and the final save retries until it succeeds. Signals: `OnSave`, `OnLastSave(reason)` (`"Manual"`, `"External"`, `"Shutdown"`; not fired when another server steals the session), `OnSessionEnd` (kick the player), `OnAfterSave(lastSavedData)`. `profile.LastSavedData` is replaced after every save with what the DataStore now holds, including when this server has lost the session, so "the id is in `LastSavedData`" is proof of durability.
- Module signals: `OnError`, `OnOverwrite`, `OnCriticalToggle`, `IsCriticalState`, `DataStoreState`.
- `profile:Reconcile()` fills missing template fields; `profile:AddUserId()`; `profile:Save()` costs one `UpdateAsync` and only warns on an inactive profile (reserve it for purchases and commits). Every write re-checks session ownership inside its `UpdateAsync`, so a server that lost the lock cannot overwrite the new owner.
- `store:MessageAsync(key, message)` delivers to a profile whether or not it is loaded (two `UpdateAsync` calls); receive with `profile:MessageHandler(function(message, processed) ... processed() end)`. Delivery is at least once (a message is cleared at the save after `processed()`), so handlers dedupe by an id. Use it for gifting paid items to offline friends.
- `store:GetAsync(key)` reads without a session for admin tools; `store.Mock` for tests. With Studio API access off, ProfileStore silently uses an in-memory mock, so a save that "works" in Studio proves nothing about live stores.

Library status at 2026-11-10 `[VS]` (last commit dates read from the repos):

| Library | Evidence | Verdict |
|---|---|---|
| ProfileStore (MadStudioRoblox) | Last commit 2025-07-31; one ModuleScript; author says ProfileService profiles load in it (test `MessageAsync` first) `[community]` | Default. A quiet repo here means finished, not abandoned; vendor a pinned copy |
| ProfileService | Last commit 2024-10; superseded by ProfileStore | Leave it in a healthy live game; migrate when you next rework data |
| Lyra (paradoxum-games) 0.6.0 | Last commit 2026-03; transactions (`txAsync`), auto-sharding past 4 MB, validation, migrations, import of existing data. README: early development, "avoid … where data loss would be catastrophic" | Evaluate when atomic trades or very large saves are core; soak-test first |
| DataStore2 | Last commit 2023-03; the docs call it legacy; Roblox ships a beta migration tool `[official]` | Migrate off |

Read the official player-data sample (session locking, ordered retries, 180 s autosave) before judging any library `[official]`. Lapis (last commit 2025-02; README: not battle-tested) is niche; Suphi's DataStore and DocumentService appear in forum comparisons, no evidence gathered here.

## DataService with schema migration

```lua
--!strict
-- ServerScriptService/Server/Services/DataService.luau (unexecuted sketch)
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ProfileStore = require(game:GetService("ServerScriptService").ServerPackages.ProfileStore)

local SCHEMA_VERSION = 3
export type PlayerData = { SchemaVersion: number, Cash: number, Inventory: { [string]: number }, Boosts: { [string]: number }, Entitlements: { [string]: boolean }, PurchaseIds: { string } }
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
if RunService:IsStudio() then store = store.Mock :: any end -- Studio never touches live data
type Profile = typeof(store:StartSessionAsync(""))
local profiles: { [Player]: Profile } = {}
local function deepCopy(value: any): any
	if type(value) ~= "table" then return value end
	local copy = {}
	for key, child in value do copy[key] = deepCopy(child) end
	return copy
end
-- Returns a migrated COPY, or nil and a reason. The live table stays untouched until every step has succeeded:
-- whatever sits in profile.Data is saved when the session ends, half-migrated or not.
local function migrate(data: { [string]: any }): ({ [string]: any }?, string?)
	local version = if type(data.SchemaVersion) == "number" then data.SchemaVersion else 1
	if version > SCHEMA_VERSION then return nil, "newer" end -- a newer build wrote it; do not touch
	local copy = deepCopy(data)
	for v = version, SCHEMA_VERSION - 1 do
		local step = MIGRATIONS[v]
		if step ~= nil then
			local ok, err = pcall(step, copy)
			if not ok then return nil, `step {v}: {err}` end
		end
	end
	copy.SchemaVersion = SCHEMA_VERSION
	return copy, nil
end

local DataService = {}
function DataService:Init()
	Players.PlayerRemoving:Connect(function(player)
		local profile = profiles[player]
		if profile ~= nil then profiles[player] = nil; profile:EndSession() end
	end)
end
function DataService:PlayerAdded(player: Player)
	local profile = store:StartSessionAsync(`Player_{player.UserId}`, { Cancel = function() return player.Parent ~= Players end })
	if profile == nil then
		player:Kick("We couldn't load your data. Please rejoin in a moment.")
		return
	end
	local migrated, reason = migrate(profile.Data :: any) -- migrate BEFORE Reconcile
	if migrated == nil then
		warn(`[Data] migration refused for {player.UserId}: {reason}`) -- count by reason (migration runbook, step 7)
		profile:EndSession() -- saves the untouched original
		player:Kick(if reason == "newer" then "This server is out of date. Please rejoin to get the latest version."
			else "We couldn't upgrade your data safely, so nothing was changed. Please try again later.")
		return
	end
	profile.Data = migrated :: any
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
	while player.Parent == Players and self:GetProfile(player) == nil and os.clock() < deadline do task.wait(0.1) end
	return self:GetProfile(player) -- a kicked player leaves Players, which ends the wait
end
function DataService:Update(player: Player, mutator: (data: PlayerData) -> ()): boolean -- mutator must not yield
	local profile = self:GetProfile(player)
	if profile == nil then return false end
	mutator(profile.Data :: any)
	return true
end
return DataService
```

A failed load kicks; it never falls through to default data, because defaults would be saved over the real profile. A migration step that throws leaves the saved profile exactly as it was: the steps run on a copy that replaces `profile.Data` only when all of them succeed. Schema rules: additive changes need only a template change plus `Reconcile`; renames and type changes need a migration and ship with a restart of outdated servers; migrations are pure and never edited after shipping; test them against copies of real data.

## Runbook: shipping a schema migration

1. **Write the step** so it is pure (no yields, no service calls: the load path holds the session lock), total (handles every shape old code could have written, including missing tables), and leaves an audit record in the profile when it removes, merges or converts anything `[lihfolk]`.
2. **Never shrink paid value.** Rescale only soft currency; keep paid and earned balances in separate fields from day one. Cancel and refund in-flight escrow (trades, listings) in old units before rescaling `[lihfolk]`.
3. **Fixtures.** Keep a folder of anonymised real profiles from every schema era, plus the messiest long-lived account you have. In CI or the command bar run `migrate` over all of them and assert no error, invariants hold, and `migrate(migrate(x))` equals `migrate(x)`. Record profile size before and after (test method in debugging-and-testing.md).
4. **Plan for version skew.** Old and new servers overlap after every publish. The guard in `migrate` (refuse data newer than this build) stops old code overwriting new fields. For risky changes use expand, then contract: release N reads both shapes and writes both; release N+1, after every server has restarted, drops the old field. Store a `MinReader` number beside `SchemaVersion` if you need to know the oldest build that may safely rewrite a profile `[lihfolk]`.
5. **Snapshot** all data stores through Open Cloud just before publishing (one per day) `[official]`.
6. **Publish.** Multi-place games publish the receiving place first, then the sender, then flip the Configs flag `[lihfolk]`. Creator Hub > Restart Servers with "Restart only servers with outdated versions" and a bleed-off delay of 1–60 minutes; handle `game.ServerRestartScheduled` to warn players, stop starting long activities and save early. Final saves belong there, not squeezed into the 30 s of `BindToClose` `[official]`.
7. **Watch for one hour:** load failures by reason (read failed, refused newer, step error, lock timeout), count of profiles per step, Data Stores dashboard statuses. A step error above zero means hotfix forward; roll back code only if every profile written so far is still readable by the old build.
8. **Follow-ups the lazy migration misses** `[lihfolk]`: leaderboards in old units (start a new board name and backfill on join), cross-player records that embed old item ids, support tools that read raw profiles (they must call the same `migrate`).

## Runbook: data incident and rollback

1. **Confirm** with three sources: player reports (ask for UserId and approximate time), dashboard error or throttle spikes, your own load and save counters.
2. **Stop the bleeding.** If saving is doing harm, publish a hotfix that keeps loading but refuses to save, or revert the place version, then restart outdated servers. Rolling back code does not roll back data: prefer a forward fix when new-schema profiles already exist `[lihfolk]`.
3. **Snapshot now** if none was taken today, so the current state survives the repair.
4. **Find the window and the keys:** players who loaded during the bad window (from analytics), or list keys and read each key's updated time (listing returns key names only, so that costs one read per key against the budget in the dupe runbook, step 4).
5. **Rehearse** the restore on a copy in a test universe with real exported data.
6. **Restore offline players first;** kick online players with a clear message, then restore. Version history gives one restore point per key per UTC hour, kept 30 days after being superseded, so choose a time before the bad release, not just before the report. Ordered stores have no versions: rebuild them from profiles.
7. **Verify** with an uncached read (`UseCache = false`) and by joining as the player.
8. **Compensate and tell players** what happened and what was restored. Apply the class-4 rule: do not restore items the ledger shows were traded away later.
9. **Post-mortem:** which guard was missing, and the test that would have caught it.

Restore one profile with ProfileStore (API read in `docs/api.md`; not executed here): `store:VersionQuery(key, Enum.SortDirection.Descending, nil, beforeUtc):NextAsync()` returns the newest version older than the `DateTime` `beforeUtc`, or `nil`; call `:SetAsync()` on it to write that version as the latest; then check with `store:GetAsync(key)`. `SetAsync` ends any active session, so the player must be offline. Without a library use `DataStore:GetVersionAtTimeAsync(key, timestampMs)` and write the value back inside `UpdateAsync`, returning `nil` when a live session owns the key and passing the key info's user ids and metadata through. One key at a time: Data Stores Manager > Compare versions > Revert (it does not know about session locks, so only for offline players). Many keys: the Open Cloud data store API or the Data Stores Batch Processor, rate-limited because they share the live budget.

## Runbook: dupe incident

Run it in order; keep an incident log with UTC times. Steps not tagged are `[house]`; none of this has been exercised on a live incident here.

1. **Stop the bleeding, keep the game up.** Turn off `trading_enabled`, `gifting_enabled` and any marketplace or mail flag through Configs ("Publish now" reaches servers in about 15 s to 1 min `[official]`; a `ConfigSnapshot` never updates by itself, so the kill switch only works if the server connects `snapshot.UpdateAvailable` to `snapshot:Refresh()` and reads the flag per trade). Decided trades still settle; new intents return `Disabled`. Do not shut servers down: play continues, and shutdowns add recovery work. Take an Open Cloud snapshot now (one per day `[official]`) and note the time as T0.
2. **Find the cause class** with the four-class table above. Ask of three known cases: was there a crash or leave (class 2), a rejoin or teleport (3), a double click or remote spam (1), a support restore (4), or a path that is not trading at all (sell, fuse, mail, drop and pick up, a double-granted receipt)? Read those profiles' ledgers for a GUID that the ledger shows leaving and that is still present; `game.JobId` and `game.PlaceVersion` on the entries tie it to a server and a release. Reproduce in the test universe with fault injection before patching.
3. **Define "duplicated" precisely.** (a) The same GUID usable in more than one inventory; a copy locked under a committed trade id is waiting to settle and does not count. (b) A lineage fork: the trade log shows one GUID leaving the same holder twice, or arriving somewhere with no committed record. (c) Stackables have no GUID: compare owned totals with the mint ledger, and each account's gain rate with the theoretical maximum.
4. **Scan within budget.** Open Cloud scans share the live budget `[official]`: per minute, Read 300 + CCU × 40 and List 300 + CCU × 2 `[VS]`. Spend at most a quarter, and pace the tool yourself (the docs give a leaky-bucket sample; Open Cloud has no built-in limiter). At 5,000 CCU that is about 50,000 reads a minute, so 2 million profiles take about 40 minutes; at 200 CCU it is about 2,000 reads a minute and the same scan takes 16 hours, during which a quarter of the List budget (175 calls a minute) is not the bottleneck but must be counted too. Each key also has a 25 MB per minute read limit, which only matters for repeated reads of one large profile. Narrow first, in this order: accounts named in trade records since the suspect release (list keys with the prefix `Trade_<yyyymmdd>`); accounts whose rare-item counts jumped in analytics; then everyone. Run it offline through the Open Cloud data store API or the Data Stores Batch Processor `[official]`, never from a live game server, and build a `GUID → holders` map.
5. **When a full scan is too expensive, build the index on load.** After the hotfix, each profile load checks its top-tier items against an ownership key per GUID (`UpdateAsync`: claim it if empty; if it names another user, flag both copies and log; skip copies locked under a committed trade id). Cap the checks per load (for example 10): each is one read and one write against budgets that grow by 40 and 20 per player-minute. It converges as players return, which is enough: only active accounts move the economy.
6. **Choose the canonical copy.** Follow each GUID from its mint through committed transfers; the copy at the end of the unbroken chain is canonical (earliest legitimate lineage). A copy still held by an account whose ledger shows it leaving is the duplicate. If both lines were traded on, the line backed by committed records is canonical and the other line's holders are good-faith holders.
7. **Good-faith holders are not punished.** Quarantine their copy (kept, usable, untradeable, flagged with the incident id). Then either convert it to a marked legitimate copy (fresh GUID, `source = "incident-<id>"`, counted in the supply report, tradeable after a cooldown) or compensate at equal value in account-bound form. Convert when the extra supply is small against the item's total; compensate when it would move the price. Never remove anything silently: the player gets a message naming the item and what replaced it.
8. **Sanctions need direct evidence:** the account's own ledger or the server log shows it performing the duplicating sequence, usually repeatedly. Remove the copies and proceeds from those accounts only, use the consequence ladder, and give an appeal path (community-moderation-safety.md, sections 7 and 9). Holding a duplicate is not evidence.
9. **Repair the economy.** Publish internally a supply report per affected item (minted, expected from rolls × odds, owned before and after). Hide or freeze price displays for those items until supply is corrected; add a time-limited sink if duped currency entered circulation; do not roll back the whole economy unless the exploit is cleanly reversible (economy-and-progression.md).
10. **Tell players** within a day: trading is paused, why in one sentence without exploit details, that legitimately obtained items are safe, and when the next update comes. On re-enable, state what was removed, converted and compensated, with counts.
11. **Re-enable in stages:** fix published and outdated servers restarted; the fault-injection test above green; trading back on behind the flag with a 3–7 day trade cooldown on the affected items; watch the GUID-collision alert for a week.
12. **Regression tests to add:** a test that replays the exact sequence found in step 2; the full fault-injection matrix (server killed between every pair of protocol steps); a dupe-hunting script that runs trade, gift, drop, sell and rejoin sequences across two mock servers and asserts that every GUID is usable in one profile and totals are conserved.
13. **Log from now on:** every transfer (trade id, GUIDs, both user ids, step times, decision state, `JobId`, `PlaceVersion`); mints per item type; recovery outcomes as counters (rolled forward, aborted, left locked); a daily supply figure per top-tier item; an alert on any GUID collision.

## Developer products: idempotent ProcessReceipt

Facts `[official]` `[VS]`: set `MarketplaceService.ProcessReceipt` exactly once from one script (a second assignment silently replaces the first; with **no** callback set, receipts are auto-acknowledged and cannot be recovered). It runs for every unresolved receipt when the player completes a purchase or is shown a successful purchase prompt, and when they join any server; there is no time-based retry and no timeout on a yielding callback. The player must be present for it to be called, but a result returned after they left is still recorded. The same receipt can run on two servers at once, so dedupe in saved data, not server memory. Returning `PurchaseGranted` acknowledges, although even that can fail to record, in which case the receipt comes back and the dedupe list must absorb it; `NotProcessedYet` or an error keeps it pending; unresolved purchases are never refunded automatically. Never grant from `PromptProductPurchaseFinished`.

Flow `[official: player data and purchasing guide]`, implemented with the `PurchaseId` cache from the ProfileStore docs (the short sample on the developer-products docs page acknowledges without confirming a save: do not copy it): wait for session-locked data on this server; grant in memory and record the `PurchaseId` in one synchronous step, unless the id is already recorded; return `PurchaseGranted` only once the id is in **saved** data. If the player leaves first, the final session save carries the grant and the id, and the receipt is acknowledged here when that save lands in time, otherwise at the next join without a second grant. The id list is capped at 100: safe, because an unresolved receipt is re-delivered with every later purchase and join, so it cannot wait behind 100 newer ones.

```lua
--!strict
-- ServerScriptService/Server/Services/ReceiptService.luau (the ONLY assigner of ProcessReceipt; unexecuted sketch)
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local DataService -- resolved in Init
local PURCHASE_ID_LIMIT, LOAD_TIMEOUT, SAVE_CONFIRM_TIMEOUT = 100, 30, 25

type Grant = (player: Player, data: any, receipt: { [string]: any }) -> () -- synchronous; cannot fail half-way
local GRANTS: { [number]: Grant } = {
	[1111111] = function(_p, data) data.Cash += 1000 end,
	[2222222] = function(_p, data) -- 2x Cash 10 min: remaining PLAY seconds; extend (cap 6 h), never stack
		data.Boosts.DoubleCash = math.min((data.Boosts.DoubleCash or 0) + 600, 6 * 60 * 60)
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
	while not isSaved(profile, purchaseId) and os.clock() < deadline do
		local finished = false
		local connection = profile.OnAfterSave:Connect(function() finished = true end)
		if profile:IsActive() then profile:Save() end -- an ended session is already writing its final save: just wait for it
		local waitUntil = math.min(deadline, os.clock() + 10)
		while not finished and os.clock() < waitUntil do task.wait(0.2) end
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
	local data = profile.Data -- active profile, and no yields from here until the id is recorded
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

A grant that throws after changing something is granted again on the retry: validate first, then mutate with plain assignments, and send anything that yields (gifts) through its own branch (below).

`[official]` `[VS]` `MarketplaceService:BindReceiptHandler(receiptType, handler, filter?)` is the newer per-type API (`Enum.ReceiptType.DeveloperProduct`, `RobuxTransferSender`, `RobuxTransferReceiver`; the handler returns `Enum.ReceiptDecision.Processed` or `NotProcessedYet`; `filter` is an array of product ids; a second handler for the same type and id throws; unmatched product receipts fall through to `ProcessReceipt`). Same idempotency rules. Keep the pattern above as the baseline.

## Game passes

- Check on the server with `UserOwnsGamePassAsync(userId, passId)`; results are engine-cached and transparently batched, so `task.spawn` all checks at join `[official]`.
- Listen to `PromptGamePassPurchaseFinished` on the server; when `wasPurchased` is true, apply the perk immediately.
- Cache per player and pass `{ owned, checkedAt }`: return a cached `true` for the session; re-check a cached `false` after a TTL (60 s) so website purchases appear (the engine's own cache can lag a purchase made outside the game by several minutes `[official]`); call in `pcall` and never cache a failed check (return the previous answer, or `false`); clear the player's entries on `PlayerRemoving`, and do not write an entry for a player who left during the yield.
- Apply character perks on every `CharacterAdded`. Expose perks through attributes (`player:SetAttribute("VIP", true)`) and also honour `data.Entitlements[pass]` from gifts.

## Subscriptions, gifts, boosts, prices

- Subscriptions: `GetUserSubscriptionStatusAsync(player, subscriptionId)` → `{ IsSubscribed, IsRenewing }`; listen to `Players.UserSubscriptionStatusChanged`; fail closed.
- Gift passes are developer products granting `Entitlements[pass] = true` in the recipient's data. Store the intended recipient as a pending gift in the **buyer's** profile before prompting (receipts carry only the buyer's id and may replay on another server). In the grant, mutate the recipient's loaded profile, or send `store:MessageAsync(recipientKey, { type = "gift", item = "VIP", giftId = purchaseId })` and dedupe by `giftId` in the recipient's handler. Because `MessageAsync` yields, give gift products their own branch that sends first and returns `NotProcessedYet` if it fails, then records the `PurchaseId`. Gate with `GetUsersPriceLevelsAsync` (the docs disagree on its return shape; log and verify `[VS]`).
- Timed boosts: a personal paid boost is saved as remaining play seconds (it pauses offline) and extends on repurchase; a server-wide boost runs in real time and shows its end. Ruling and module sketch: monetization-and-policy.md; cross-server mechanics: gameplay-systems-cookbook.md §24.
- Prices: `GetProductInfoAsync(id, Enum.InfoType.Product or GamePass).PriceInRobux`; regional pricing means players see different prices. `RankProductsAsync` once at join.
- Refunds: a refunded developer product reaches you only as the Open Cloud "Transaction Refunded" webhook `[official]`. Keep a ledger entry per `PurchaseId` naming what it granted, so the clawback can find it (endpoint, signature check and policy: monetization-and-policy.md).

## Teleports, reserved servers and messaging

- Server-only `TeleportService:TeleportAsync(placeId, players, options)` in `pcall` with retries; handle `TeleportInitFailed` (`Flooded` → wait 15 s, other retryable results → wait 1 s; cap the retries: the docs sample uses 5 attempts) `[official]`.
- `[official]` `[VS]` `ReserveServer`/`ReserveServerAsync`, `TeleportToPrivateServer`, `ShouldReserveServer` and `ReservedServerAccessCode` are deprecated. Use `options.ReservedServerId = HttpService:GenerateGUID(false)` (first teleport creates the server, later ones join), `options.VipServerId = game.PrivateServerId`, or `options.ServerInstanceId = jobId`. Setting more than one target field errors.
- Detect a reserved server with `game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0`.
- Teleport data is client-visible and tamperable; read `player:GetJoinData().TeleportData` as a hint only and keep rosters in a MemoryStore hash map keyed by the reserved server id. Match servers reject anyone not on the roster.
- `TeleportService:SetTeleportGui(gui)` and `GetArrivingTeleportGui()` for a custom loading screen. Call `player:RequestStreamAroundAsync(position)` before in-place teleports.
- Custom matchmaking: lobby servers write tickets to a MemoryStore sorted map or queue sharded by mode; one matchmaker (elected via a MemoryStore lock) groups tickets, writes the match record to a hash map, and calls the teleport. Queue reads hide items for 30 s, so ticket removal must be idempotent.
- MemoryStore limits `[official]` `[VS]`: memory 64 KB + 1.2 KB × users (the quota shrinks only 8 days after users leave); 1,000 + 120 × CCU request units per minute for the whole experience (a range or queue read costs one unit per item returned, a hash-map `UpdateAsync` at least two); throttling from roughly 30,000 units per minute on one partition, and a sorted map or a queue is one partition; about 5,000 writes and 15,000 reads per minute on one hash-map key; 1,000,000 items and 100 MB per sorted map or queue; 32 KB values; 128-character keys; 45-day maximum (and default) expiry; queue invisibility timeout 30 s by default. Not durable.
- MessagingService limits `[official]` `[VS]`: 1 kB messages; topic names 1–80 characters; 600 + 240 × players sends per server per minute; receives per minute 40 + 80 × servers per topic and 400 + 200 × servers for the whole game; 20 + 8 × players subscriptions per server; delivery usually within 1–2 s, never guaranteed. Use it for hints only; receivers re-read authoritative state. Validate `message.Data` like a remote payload. Open Cloud `PublishUniverseMessage` and `RestartUniverseServers` exist for live-ops tooling.

## Level-up audit: how to check an existing game

1. **Dashboards.** Monitoring > Data Stores: non-200 statuses, throttles, quota usage per request type, storage against the limit. Error report: queue and throttle warnings at peak hours.
2. **Static scan** with sketch E, then read three paths by hand: load (what happens when it fails?), save (leave, shutdown, autosave), purchase (one handler, idempotent, grant recorded before acknowledging).
3. **Measure a heavy profile** on a test server: `#HttpService:JSONEncode(value)` against 4,194,304; find what grows without a cap (logs, id lists, placed objects).
4. **Rollback drill** in a test universe: follow the incident runbook above on one key. Take an Open Cloud snapshot before every update that changes save logic.
5. **Fix order:** failed load that saves defaults; missing session lock in a game with trading; non-idempotent receipts; `SetAsync` on shared keys and reads during gameplay; leaderboard write rate; versioned migrations; RTBF templates.
6. **Dupe review:** classify each reported dupe with the four-class table; check that every profile writer respects the lock and that value-moving handlers have a synchronous core. For a live dupe follow "Runbook: dupe incident".
7. **Moving a live game to ProfileStore or Lyra** is never a big bang: on first load read the old key, write the new one, mark the profile as migrated, leave the old key untouched for at least 30 days, and rehearse on copies of real data. For DataStore2 use Roblox's beta migration tool `[official]`.

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
| Duplicated items after trades | Two independent saves; no session lock; one side rolled back on purpose | Both profiles locked on one server and the two-profile commit protocol (or a transaction library); escrow across servers; log trade ids; then the dupe incident runbook |
| Robux spent and nothing granted, or granted twice | Grant in `PromptProductPurchaseFinished`; `PurchaseGranted` before the save; second `ProcessReceipt` assignment; no `PurchaseId` dedupe in saved data | The ReceiptService pattern above |
| Throttle errors at peak | Reads or writes during gameplay; leaderboard written on every change; every server polling one key | Buffer in memory; throttle ordered writes; jitter; shard hot read keys |
| Storage near the limit | One data store per player (DataStore2, "Berezaa method"); dead test data; uncapped arrays | Official migration packages; delete test stores; cap lists |
| Saves fail only for veterans | Profile near 4 MB, or over 4 MB per minute of writes on one key | Prune; split into a few deterministic keys; or an auto-sharding library |
| "Loaded on another server" kicks | Stale lock after a crash, or teleports that do not wait for the old session to end | Let the library time the lock out; never `Steal`; end the session before teleporting |

## Review gate (data and purchases)

- [ ] Session-locked loading; a failed load never saves; the player is kicked or the profile marked unsaveable.
- [ ] Migrations run before `Reconcile`, on a copy, with the newer-schema guard; steps are pure and total; fixtures from every schema era pass, including the idempotence check; paid balances never shrink; key pattern unchanged.
- [ ] No DataStore reads during gameplay; autosave staggered; no custom BindToClose on top of ProfileStore.
- [ ] `UpdateAsync` transforms never yield; metadata and user ids re-passed; failed writes verified with `UseCache = false`.
- [ ] Leaderboard writes throttled; `leaderstats` display only.
- [ ] Trades follow the two-profile commit protocol: trade-record keys are at most 50 characters, acknowledgements follow confirmed settle saves, and the fault-injection test has passed.
- [ ] Exactly one `ProcessReceipt` (or filtered handlers); dedupe by `PurchaseId` in saved data; `PurchaseGranted` only after confirmed save; `NotProcessedYet` on absent player, unloaded data, unknown product, failed grant or save; nothing granted from `PromptProductPurchaseFinished`; pass ownership checked on the server and cached correctly.
- [ ] Prices from `GetProductInfoAsync`; gifts gated by price level; boosts extend, never stack; personal boosts count play time, server-wide boosts run in real time.
- [ ] RTBF templates cover every user-keyed store (exact `{UserId}` token; `scope_pattern` "global" for default scopes).
- [ ] Snapshot taken before any update that changes save logic; restore drill done in a test universe; Data Stores dashboard checked at peak; `ServerRestartScheduled` handled; restarts use "outdated only" with a bleed-off delay.
- [ ] Value-moving actions use a synchronous commit with a ledger entry; non-stackable items carry GUIDs; saves and loads validate invariants.

Grep `references/knowledge-base.md` for `## 4.6`, `## 4.7` and `## 4.8`.

## Sources

Accessed 2026-11-11. `Roblox/creator-docs` at commit 7cbffff (2026-11-10); ProfileStore at commit 45c9847 (2025-07-31).

- https://github.com/Roblox/creator-docs (read): `content/en-us/cloud-services/data-stores/{best-practices,error-codes-and-limits,versioning-listing-and-caching,observability,data-stores-manager,right-to-be-forgotten,player-data-purchasing}.md`, `cloud-services/{extended-services,http-service,secrets}.md`, `cloud-services/memory-stores/{index,queue,hash-map,sorted-map}.md`, `production/{configs,monetization/developer-products,monetization/regional-pricing}.md`, `projects/{teleport,update-games}.md`, `cloud/webhooks/webhook-notifications.md`, `reference/engine/classes/{MarketplaceService,TeleportService,TeleportOptions,MessagingService,DataModel}.yaml`
- https://github.com/MadStudioRoblox/ProfileStore (read: `ProfileStore.luau` in full for the save, session and message paths; `docs/api.md`; `docs/devproducts/index.md`). https://github.com/MadStudioRoblox/ProfileService, https://github.com/paradoxum-games/lyra, https://github.com/nezuo/lapis, https://github.com/Kampfkarren/Roblox (DataStore2) (README and last commit as of 2026-11-10; not re-read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-datastore-safety/SKILL.md`, `LihFolk Vault V2/04 Data and Persistence/{Data Loss Prevention and Recovery, Schema Migrations - Worked Case Studies, Trading Systems Without Duplication, Saving Correctly - Autosave and BindToClose}.md`, `22 Anti-Exploit and Security/Economy Exploits - Dupes Races and Purchase Abuse.md`, `41 Multiplayer Services/Server Shutdowns Soft Updates and Migration.md` (read)
- Limits and Extended Services (read, Roblox staff posts): https://devforum.roblox.com/t/datastores-access-and-storage-updates/3597255, https://devforum.roblox.com/t/extended-services-for-data-stores-is-now-available/4504347, https://devforum.roblox.com/t/weekly-recap-july-13-%E2%80%93-17-animation-graphs-go-live-5%C3%97-more-data-store-storage/4743286. Not re-read: https://devforum.roblox.com/t/extended-services-update/4070634
- Libraries, dupes and migration (search summary, not re-read): https://devforum.roblox.com/t/datastores-migration-packages-for-the-berezaa-method-and-datastore2-module-public-beta/3631514, https://devforum.roblox.com/t/session-locking-explained-datastore/846799, https://devforum.roblox.com/t/exploiting-how-to-prevent-exploiters-from-abusing-data-store-rollbacks-and-sanitizing-against-data-store-vulnerabilities/2019989, https://devforum.roblox.com/t/what-is-the-best-datastore-module-to-use-currently/3598021, https://devforum.roblox.com/t/should-i-use-profilestore-or-profileservice/3871636
- Not verified: the two-profile commit protocol and every runbook are paper designs, never executed; no public post-mortem of a large data-loss or dupe incident with numbers was found.
