# Engineering architecture, Luau standards and tooling

What this is: the client-server model, project architecture, Luau standards, toolchain, testing, CI and Studio MCP working rules. Open it when setting up a project or choosing tools, or jump to "Level-up audit" to assess and untangle an existing codebase. Distilled from knowledge-base sections 4.1, 4.2, 4.3 and 4.10; tool versions and MCP tools re-checked on 2026-11-10 (GitHub repos, `Roblox/creator-docs`). Snippets are unexecuted sketches to adapt. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`.

Contents: Start here by level · Client-server model essentials · Project architecture · Luau standards · Toolchain · Testing · CI/CD with Open Cloud · Runbook: shipping an update to a live game · AI agents and the Studio MCP · Level-up audit · Review gate · Sources

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | (1) Server code in ServerScriptService, shared code in ReplicatedStorage, loading screen in ReplicatedFirst. (2) One server entry Script and one client entry; everything else is ModuleScripts. (3) `--!strict`, `task.wait` not `wait`, `pcall` around every `...Async` call. (4) Handle players who joined before your `PlayerAdded` connection. (5) Use Studio plus Script Sync and git before learning Rojo | Frameworks, ECS, CI, Parallel Luau |
| Intermediate | Init/Start loader; behaviour by CollectionService tags; a Trove per lifetime; pinned toolchain with lint, format and type checks in CI; a test universe; the update runbook | Custom networking codegen, ECS |
| Expert | Expand-then-contract releases across mixed server versions; versioned cross-place messages; in-engine Jest suites through Luau Execution; headless audit scripts; MCP-driven playtests; jecs where entity counts demand it | Nothing: read it all |

Terms: a *service* is a server module that owns one system; a *controller* is its client counterpart. *Replication* is the engine copying instances and properties from server to clients. A *sourcemap* is the file that tells external tools where each script sits in the DataModel. *Version skew* is old and new servers running at the same time after a publish.

Related: studio-workflow.md (Studio setup, Script Sync or Rojo, publishing from Studio); luau-mastery.md (language); architecture-patterns-luau.md (patterns); debugging-and-testing.md (tests and live debugging).

## Client-server model essentials

- One authoritative server, many clients. Only server state is real; everything on a client is a replica, a prediction or decoration.
- Server-to-client replication is automatic for replicated containers. Client-to-server replication does not happen except through network ownership (physics of owned assemblies, including the player's own character, and animations on their own character).
- Replication order is not guaranteed across different kinds of change (a property change and a RemoteEvent fired in the same frame may arrive in either order).
- With `StreamingEnabled`, distant parts may not exist on the client. Use `WaitForChild` with a timeout, CollectionService signals or model streaming modes; never index deep Workspace paths directly.

Containers:

| Container | Replicates | Put here |
|---|---|---|
| `ReplicatedFirst` | Yes, first | Loading screen script and UI only |
| `ReplicatedStorage` | Yes | Shared modules, remotes, config, templates, the single client entry `Script` (`RunContext = Client`) |
| `ServerScriptService` | Never | Single server entry and all server modules |
| `ServerStorage` | Never | Server-only assets and maps |
| `Workspace` | Streamed | World geometry; behaviour by tags, not scripts inside models |
| `StarterPlayerScripts` / `StarterCharacterScripts` / `StarterGui` | Copied per player | LocalScripts only; a `RunContext = Client` Script here runs twice |

Client load order: ReplicatedFirst runs; the DataModel replicates and `game.Loaded` fires; PlayerScripts and `RunContext = Client` scripts run; the character spawns.

`[VS]` Rojo's `emitLegacyScripts` defaults to `true`, which turns `*.client.luau` into a `LocalScript`. A client entry in `ReplicatedStorage` needs `"emitLegacyScripts": false` in `default.project.json`.

Network ownership: anchored parts are server-owned; unanchored assemblies default to automatic ownership near a player. `BasePart:SetNetworkOwner(player)` pins ownership (give vehicles to the driver on `VehicleSeat.Occupant` change). The owner's physics cannot be verified, so see networking-and-security.md.

`[VS]` Server authority mode (`Workspace.AuthorityMode = Server`, `RunService:BindToSimulation`, `SetPredictionMode`) reached full release in 2026. Use it for competitive physics games (racing, sports, shooters); keep client ownership plus server validation elsewhere. Requirements and trade-offs: networking-and-security.md.

## Project architecture

One server entry `Script` and one client entry `Script`; everything else is ModuleScripts ("services" on the server, "controllers" on the client) run through an Init/Start lifecycle:

1. Require every module (top-level code builds tables only; no yields, no cross-module calls).
2. `Init()` on each: own state, own remotes, own signals. No calls into other services, no yielding.
3. `Start()` on each in its own `task.spawn`, so one yielding service cannot block the rest. Cross-service calls are safe from here.
4. Connect `Players.PlayerAdded` last, and loop `Players:GetPlayers()` to catch early joiners.

Rules: no require cycles (resolve lazily in `Init`); shared modules never require server modules; services expose functions, not mutable tables; no server logic in replicated modules.

More rules that prevent slow-burning problems `[lihfolk]`:

- State versus moments: anything that stays true (health, round phase, a door being open) replicates as an attribute or property so late joiners and re-streamed instances see it; remotes carry moments (a request, a hit effect). Per-player private state uses an owner-only channel (networking-and-security.md).
- Defer client modules that the first playable frame does not need (shop catalogue, settings panels); requiring everything at client start is a common cause of slow phone joins.
- Find children through dedicated folders or tags, never by a name that map content could reuse.
- Test switches (test profile keys, simulated failures, debug panels) are read only when `RunService:IsStudio()` is true or the user is on a server allowlist, and the boot log prints every switch that is on. Tester commands follow the admin rules in networking-and-security.md.
- Keep backups, archives and import sources out of the place file; split a script by responsibility long before it becomes unmanageable (place-size numbers in performance.md).

Typed loader sketch (server; mirror it on the client with `Controllers/`):

```lua
--!strict
local Players = game:GetService("Players")
type Service = { Init: ((self: any) -> ())?, Start: ((self: any) -> ())?, PlayerAdded: ((self: any, player: Player) -> ())? }
local services: { [string]: Service }, order: { string } = {}, {}
for _, child in script.Parent:WaitForChild("Services"):GetChildren() do
	if child:IsA("ModuleScript") then services[child.Name] = require(child) :: any; table.insert(order, child.Name) end
end
table.sort(order) -- prefix names ("10_Data") for explicit ordering
for _, name in order do
	local s = services[name]
	if s.Init then local ok, err = xpcall(s.Init, debug.traceback, s); if not ok then error(`[Boot] {name}.Init failed: {err}`, 0) end end
end
for _, name in order do
	local s = services[name]
	if s.Start then task.spawn(function() local ok, err = xpcall(s.Start, debug.traceback, s); if not ok then warn(`[Boot] {name}.Start failed: {err}`) end end) end
end
local function onPlayerAdded(player: Player)
	for _, name in order do local s = services[name]; if s.PlayerAdded then task.spawn(s.PlayerAdded, s, player) end end
end
Players.PlayerAdded:Connect(onPlayerAdded)
for _, player in Players:GetPlayers() do task.spawn(onPlayerAdded, player) end
```

Behaviour on instances: tag with CollectionService and bind one component per tag (RbxUtil `Component`, or 40 lines of `GetTagged` plus added/removed signals with a Trove per instance). Imported Blender models get tags such as `Door`, and their helper attachments get their own tags, so code never depends on names.

Framework choice:

| Option | Status | Verdict |
|---|---|---|
| Plain modules + typed loader + RbxUtil Signal/Trove/Component + ProfileStore + a typed remote guard | Recommended baseline | Full type inference, no magic, easiest for AI agents |
| Knit | Archived July 2024, unmaintained | Do not start new projects on it. Existing games keep working; migrate one service at a time (`KnitInit`/`KnitStart` become `Init`/`Start`, `GetService` becomes `require`, the `Client` table becomes explicit remote registrations) and keep remote names stable so mixed-version servers still talk `[lihfolk]` |
| Flamework (roblox-ts) | Not re-checked here `[lihfolk]` | Only if the team has already chosen TypeScript; that choice is bigger than the framework |
| jecs ECS (0.11 at reading `[VS]`) | Active | Bold option for thousands of similar entities (TD waves, bullet hell, swarms); steeper onboarding |
| Template stacks (MonzterDev) | Pins older libraries | Reference only |

Recommended Rojo layout:

```text
my-game/
├─ rokit.toml  wally.toml  wally.lock  default.project.json  selene.toml  stylua.toml  .luaurc
├─ .github/workflows/ci.yml
├─ assets/blender/ (.blend sources)  assets/export/ (GLB)  assets/asset-ids.json (generated)
├─ tools/blender_exec.py (Blender Lab MCP bridge)  tools/export_glb.py  tools/upload-assets.luau (Lune, Open Cloud)
├─ src/first/        -> ReplicatedFirst (Loading.client.luau)
├─ src/shared/       -> ReplicatedStorage.Shared (Config/, Net/Remotes.luau, Types.luau, Util/)
├─ src/client/       -> ReplicatedStorage.Client (Main.client.luau, Controllers/, Components/)
├─ src/server/       -> ServerScriptService.Server (Main.server.luau, Services/, Components/, Net/RemoteGuard.luau)
├─ src/storage/      -> ServerStorage
├─ Packages/ (wally shared)  ServerPackages/ (wally server)
└─ tests/
```

Declare remotes in the project file (or create them on the server at boot) so they exist before any script runs. Never let the client create remotes. Set `Workspace.SignalBehavior = Deferred`.

## Luau standards

- `--!strict` on every new file. `--!nocheck` only for vendored code. `[VS]` The new type solver is generally released (use it for new code; `Workspace.UseNewLuauTypeSolver` selects it per place); fixes still land, so prefer simple type shapes. Detail in luau-mastery.md.
- Types: `export type`, generics, unions, `T?`, `typeof(setmetatable({} :: Fields, Class))` for classes, `unknown` for untrusted input (forces refinement), singleton string types for enums.
- Naming: PascalCase for services, modules, types and instances; camelCase for locals and functions; SCREAMING_SNAKE_CASE constants; `_private`; `is/has/can` booleans; **`Async` suffix on every yielding function**.
- Errors: `pcall` every yielding call to a web service (DataStores, MemoryStores, MessagingService, MarketplaceService, TeleportAsync, HttpService). `xpcall(fn, debug.traceback)` when you need a trace. `assert` for programmer errors only. Never swallow errors silently; `warn` with context. Retries use exponential backoff with jitter.
- Scheduling: `task.wait`, `task.spawn`, `task.defer`, `task.delay`, `task.cancel`. Never `wait`, `spawn`, `delay`. Per-frame work on `RunService.Heartbeat` (server), `PreRender` (client camera and visuals), `PreSimulation`/`PostSimulation` (physics-adjacent).
- Deferred events `[VS]`: set `SignalBehavior = Deferred` now. Pitfalls: fire-then-read returns stale state; disconnect does not cancel already-queued invocations (use `:Once()`); `Destroying` handlers run after the instance is destroyed; re-entrancy capped at 10.
- Cleanup: every object with a lifetime owns a Trove (RbxUtil `Trove`; Maid and Janitor are older equivalents). Per-player tables are cleared on `PlayerRemoving`. Use RbxUtil `Signal` instead of `BindableEvent` for module-to-module events (BindableEvent deep-copies tables and strips metatables).
- Promises (evaera) are useful for fan-out with timeouts, cancellation and retries; otherwise plain yielding code with `Async` naming is clearer.
- Performance: `--!native` or `@native` only on measured hot server (or Android client) code `[VS]`; `buffer` for compact binary data; cache services and functions in locals; avoid closures and tables per frame in hot loops. The 2025 runtime added `vector`, `math.lerp`, `math.map`, `math.isnan`, `math.isinf`, `math.isfinite`, `buffer.readbits`, `buffer.writebits`.

## Toolchain `[VS]`

Latest tags and dates read from the GitHub repos on 2026-11-10. Pin exact versions; upgrade one tool at a time.

| Tool | Latest (tag date) | Role and notes |
|---|---|---|
| Rokit | 1.2.0 (2025-09) | Pins every CLI in `rokit.toml` (supersedes Aftman and Foreman) |
| Rojo | 7.7.1 (2026-10) | Filesystem ↔ Studio sync; `rojo build`, `serve`, `sourcemap`. 7.7 adds `rojo syncback` (pull an existing place into project files, with `syncbackRules`) and a WebSocket sync transport `[community: release notes via search]`; upgrade the CLI and the Studio plugin together. Never `rojo upload --cookie` in CI |
| Studio Script Sync | Built in | Scripts and folders only; 10,000 scripts per synced root, 128 roots; works with Team Create; no sourcemap. It ignores attributes and tags on scripts (data loss if you rely on them) `[official]`. Conflict: `scripting/sync.md` treats it as a standard feature, `ai/coding-harness.md` still says to enable it under Beta Features |
| Wally | 0.3.2 (2023-06) stable; 0.4.0-alpha.1 (2026-10) | Packages; commit `wally.lock`; CI runs `wally install` then `git diff --exit-code wally.lock`. Stay on the stable line |
| Selene | 0.32.0 (2026-10) | Lint, `std = "roblox"` |
| StyLua | 2.6.0 (2026-10) | Format, `stylua --check src` |
| luau-lsp | 1.70.1 (2026-09) | `luau-lsp analyze` with a fresh `sourcemap.json`; with its companion Studio plugin it is also the editor language server Roblox recommends for Script Sync `[official]` |
| Lune | 0.11.1 (2026-10) | Standalone Luau runtime for build scripts (asset upload, codegen, unit tests). Pre-1.0: minor versions break APIs |
| Jest Roblox | `roblox/jest` 3.20.0 on Wally; repo active 2026-11 | Port of Jest 27; runs in Studio and through Open Cloud Luau Execution `[official README]`. Default for new in-engine tests |
| TestEZ | 0.4.2; last commit 2023-01 | Legacy. Keep existing suites; write new ones in Jest Roblox (its docs include a TestEZ migration guide). `jsdotlua/jest-lua` (last commit 2024-12) is a stale community mirror |
| rbxcloud | 0.17.0; last commit 2025-03 | Open Cloud CLI; fine for simple publish and messaging calls |
| Mantle | 0.11.18 (2025-03) | README: no longer maintained. Do not adopt; use Open Cloud calls from Lune or CI |
| Zap, Blink | Zap 0.6.29 (2026-06); Blink active (2026-09) | Generated networking, see networking-and-security.md |

```toml
# rokit.toml (versions verified 2026-11-10; the docs' own example still shows rojo 7.6.1 and lune 0.10.4)
[tools]
rojo = "rojo-rbx/rojo@7.7.1"
wally = "upliftgames/wally@0.3.2"
lune = "lune-org/lune@0.11.1"
selene = "kampfkarren/selene@0.32.0"
stylua = "johnnymorganz/stylua@2.6.0"
luau-lsp = "johnnymorganz/luau-lsp@1.70.1"
```

Rojo when the filesystem is the source of truth (git, CI, AI agents, non-script instances in version control); Script Sync when Studio is and you only want an external editor and git for code `[official]`. Never run both on the same scripts.

## Testing

- Pure logic (economy maths, damage formulas, migrations, validators) lives in Instance-free modules tested under Lune.
- In-engine tests use Jest Roblox (TestEZ only where a suite already exists) and run in a test place via the Studio CLI (`RobloxStudioBeta.exe --task RunScript --placeId <id> --universeId <id> --runScriptFile tests.luau --outputFile out.log --quitAfterExecution`) or Open Cloud Luau Execution.
- Data code runs against `ProfileStore.Mock`.
- Multi-client tests: `StudioTestService` (`ExecuteMultiplayerTestAsync`, `AddPlayers`) and `UserInputService:CreateVirtualInput()`.
- Leak audit: respawn 20 times and rejoin repeatedly; memory and connection counts return to baseline.
- What to test, cheapest first `[lihfolk, adapted]`: pure logic and migrations against fixture saves (data-and-purchases.md); remote handlers with the fuzz corpus and race test (networking-and-security.md); time-based features (daily rewards, boosts, cooldowns) through an injectable clock instead of `os.time()` calls scattered in code; streaming bugs by forcing stream-out (`StreamingTargetRadius = 64`); long sessions with a soak loop (performance.md, procedure B). Harness design and worked examples: debugging-and-testing.md.

## CI/CD with Open Cloud `[VS]`

Luau Execution API: `POST /cloud/v2/universes/{universeId}/places/{placeId}/luau-execution-session-tasks` with `{ "script": "...", "timeout": "300s" }`; poll until `COMPLETE` or `FAILED`. Limits: 4 MB script, 5 minutes, 4 MB return JSON, 450 KB logs, 100 MiB binary input valid 15 minutes. No physics, no auto-run scripts, DataModel changes not persisted; DataStores work.

Place publishing: `PATCH https://apis.roblox.com/assets/v1/assets/{placeId}` with `request={"assetId":<placeId>,"assetType":"Place","published":true}` and `fileContent` (`.rbxl` as `application/octet-stream`); poll `GET /assets/v1/operations/{id}`. Key needs assets Read and Write.

Pipeline: on every PR run `rokit install`, `wally install` + lock diff, `selene src`, `stylua --check src`, `rojo sourcemap`, `luau-lsp analyze`, Lune unit tests. On merge: `rojo build -o game.rbxl`, publish to a test place in a separate test universe, run in-engine tests. On release tag: publish to production with a manual approval, using Migrate To Latest Update for non-backwards-compatible data migrations. Keys live in CI secrets, scoped to one universe and minimum permissions, created on a dedicated automation account with an IP allowlist and an expiry (networking-and-security.md).

Collaboration: place files do not merge; code merges in git; one place-file owner at a time; Git LFS with locking for binaries; only CI publishes production.

## Runbook: shipping an update to a live game

Publishing does not move players: old and new servers run side by side until old ones empty or you restart them `[official]`. Rules 1–5 adapted from `[lihfolk]`.

1. **Every saved record carries a schema version**, and old code never writes data newer than it understands (the guard in data-and-purchases.md).
2. **Expand, then contract.** Release N reads old and new shapes and still writes what old servers need. Release N+1, after every server has restarted, removes the old shape. The same applies to remote payloads: keep remote names stable and accept the previous payload for one release.
3. **Cross-place messages are versioned contracts.** Teleport data, MemoryStore tickets and MessagingService payloads carry a `v` field; receivers accept the current and previous version.
4. **Features ship dark** behind a Configs flag and are switched on after the restart completes.
5. **Multi-place order:** publish the receiving place (match, dungeon) first and restart its outdated servers with a short delay (5–10 minutes); then publish the sender (lobby) with a longer bleed-off (15–30 minutes); then flip the flag; drop the old version next release.
6. **Restart** from Creator Hub (or Open Cloud): "Restart only servers with outdated versions", plus "Delay server restart" of 1–60 minutes. Roblox stops matchmaking into those servers (invites and teleports can still enter), waits, then teleports each old server's players together to a new one `[official]`.
7. **Drain** when `game.ServerRestartScheduled(restartTime, source, attributes)` fires `[official]`: warn players with a countdown, save everyone once early, refuse new trades, stop enqueuing matchmaking tickets, and start no round that cannot finish before `restartTime`. `source` is `DeveloperUpdate` for your restarts and `RobloxMaintenance` (with empty attributes) for Roblox's, so the handler needs a default policy.
8. **Watch** error report, load-failure counters and the performance dashboard for an hour; compare session length and next-day return of players moved by the update with a normal day `[lihfolk]`.
9. **Emergency.** A bad update with no data impact: revert in Version History, publish, restart outdated servers with a 1–5 minute delay. If the bad build wrote data, rolling code back does not roll data back: fix forward, or ship the rollback build with a reader that tolerates the new fields (incident runbook in data-and-purchases.md).

```lua
--!strict
-- Unexecuted sketch: one drain switch that other services read before starting long activities.
local Drain = { restartAt = nil :: DateTime? }
function Drain.canStart(durationSeconds: number): boolean
	local restartAt = Drain.restartAt
	return restartAt == nil or DateTime.now().UnixTimestamp + durationSeconds < restartAt.UnixTimestamp
end
game.ServerRestartScheduled:Connect(function(restartTime: DateTime, _source: Enum.CloseReason, _attributes: { [string]: any })
	Drain.restartAt = restartTime
	workspace:SetAttribute("RestartAtUnix", restartTime.UnixTimestamp) -- clients show the countdown
end)
return Drain
```

A single-place game with no schema change and no long activities can simply publish and restart outdated servers with a 10–15 minute delay.

## AI agents and the Studio MCP `[VS]`

Studio has a built-in MCP server `[official]`: Assistant > … > Manage MCP Servers > "Enable Studio as MCP server"; stdio transport; quick connect for Claude Code, Claude Desktop, Cursor, VS Code, Codex CLI, Gemini CLI and Antigravity. Commands: Windows `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`, macOS `/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`. If tools do not appear, restart Studio and the client and check the config JSON (the port-13469 conflict note in the earlier version of this file is not in the current docs). The older open-source `Roblox/studio-rust-mcp-server` is no longer developed (its README points to the built-in server). Every call takes a `studio_id` from `list_roblox_studios`.

| Group | Tools (docs, 2026-11) |
|---|---|
| Scripts | `script_read` (whole or line range), `multi_edit` (several edits in one call; creates the script if the path is missing), `script_search` (fuzzy name, 10 results), `script_grep` (50 matches at most) |
| DataModel | `search_game_tree`, `inspect_instance`, `execute_luau` (`datamodel_type` Edit, Client or Server) |
| Playtest | `get_studio_state`, `start_stop_play`, `get_console_output`, `screen_capture` (optional camera position), `character_navigation`, `user_keyboard_input`, `user_mouse_input` |
| Delegation and docs | `subagent` (`explore`, `playtest`), `http_get` (allow-listed Roblox docs), `skill` |
| Assets | `upload_image`, `store_image`, `insert_asset`, `search_asset`, `generate_mesh`, `generate_material`, `generate_procedural_model`, `wait_job_finished` |
| Open Cloud | `open_cloud_invoke`: calls Open Cloud with no API key, limited to the scopes the user enabled for this game (levels Safe, Balanced, Full access; each game starts at Balanced) |

Working rules:

1. Connect, then orient: `list_roblox_studios`, confirm the target place, `get_studio_state`, and find out who owns the files (Rojo, Script Sync or Studio).
2. Explore before editing: `search_game_tree`, `inspect_instance`, `script_search`, `script_grep`. `script_grep` stops at 50 matches, so for a whole-game scan use an `execute_luau` sketch (the audit sections of this skill). Fix every copy, not the first one found.
3. Edit source in Edit mode. Play-mode changes are discarded; `execute_luau` runtime changes do not persist in scripts. If Rojo owns the files, edit the files.
4. A write is not done until a read shows it, and a gameplay change is not done until a play session shows it: `script_read`, then `start_stop_play`, drive the character with `character_navigation` and the input tools, and check `get_console_output` and a `screen_capture`.
5. Modify what exists; never add parallel copies; preserve the hierarchy.
6. `execute_luau` freezes Studio until it yields; batch about 1,000 items per `task.wait()`. `require` in Edit context gives fresh module state. Never publish, save or delete unasked. Stop after the same error repeats twice.
7. House rules override convenient tools: never ship visible 3D content from `generate_procedural_model`, `generate_mesh`, `insert_asset` or `search_asset`. Visible assets come from the Blender pipeline (art-pipeline-blender.md); `open_cloud_invoke` with `asset:read` and `asset:write` and an approved upload folder is the sanctioned way to upload those exports. The generators are acceptable only for throwaway experiments that never reach the shipped place.
8. Verify APIs with `http_get`, `https://create.roblox.com/docs/llms.txt` or the `.md` page versions; do not guess.
9. Permissions are per person and per game. Ask the user to enable a scope; never work around a refusal. "Save & load data" makes `execute_luau` hit live DataStores, and publishing, monetisation, ban and secret scopes act on the live game: use a test universe.

OpenGameEval (Roblox's agent benchmark) ties failures to under-exploration and to fixing one copy when several exist; best core Pass@1 was about 50% at time of reading.

## Level-up audit: how to check an existing game

1. **Find the owner of the source.** Git repo with `default.project.json` (Rojo), Script Sync icons in the Explorer, or Studio only. Never point `rojo serve` at a Studio-owned live place: pull it into files first (`rojo syncback`) or start with Script Sync.
2. **Inventory** with sketch F: scripts per container and class, identical copies, `--!strict` share, largest scripts, legacy API counts. Sketches A–F of this skill (performance, security, data, code) also run headless: `--task RunScript --runScriptFile audit.luau --outputFile out.log --quitAfterExecution` executes at command-bar permission level `[official]`.
3. **Runtime health.** Play in Studio and read the Output; Creator Hub > Monitoring > Error report for the top live errors by count; F9 server log on a live server.
4. **Read the entry points.** Count auto-running Scripts and LocalScripts and write down the real boot order.
5. **Triage in ROI order** `[house]`: errors that hit every player; security and data findings (the other audits); leaks in per-player and per-character code; identical scripts copied into models (one tagged component instead); removed or deprecated APIs on hot paths; source control and lint in CI; types on touched files only.
6. **Refactor a live game by strangling, not rewriting.** New features go through the loader; old scripts move when they are touched, one system per release; remote names and data keys stay stable; risky switches sit behind a Configs flag; test in a separate universe; ship with Migrate To Latest Update.

Sketch F, code inventory (unexecuted sketch; read-only; command bar or Studio MCP `execute_luau`, Edit; ignore hits in services you do not own):

```lua
--!strict
local ScriptEditorService = game:GetService("ScriptEditorService")
local LEGACY = {
	{ "wait(", "[^%.%w_]wait%(" }, { "spawn(", "[^%.%w_]spawn%(" }, { "delay(", "[^%.%w_]delay%(" },
	{ "BodyMover", "Body[VGPFAT]%a+" }, { "Humanoid:LoadAnimation", "[Hh]umanoid:LoadAnimation" },
	{ "FindPartOnRay", "FindPartOnRay" }, { "InvokeClient", "InvokeClient" }, { "while true do", "while%s+true%s+do" },
}
local byPlace: { [string]: number }, legacy: { [string]: number }, copies: { [string]: number } = {}, {}, {}
local sizes: { { path: string, lines: number } } = {}
local total, strict = 0, 0
for _, service in game:GetChildren() do
	local ok, descendants = pcall(function() return service:GetDescendants() end)
	if not ok then continue end
	for _, d in descendants do
		if not d:IsA("LuaSourceContainer") then continue end
		local okSource, source = pcall(function() return ScriptEditorService:GetEditorSource(d) end)
		if not okSource then continue end
		total += 1
		local key = `{service.Name}/{d.ClassName}`
		byPlace[key] = (byPlace[key] or 0) + 1
		if string.find(source, "^%-%-!strict") then strict += 1 end
		if #source > 200 then copies[source] = (copies[source] or 0) + 1 end
		table.insert(sizes, { path = d:GetFullName(), lines = select(2, string.gsub(source, "\n", "")) + 1 })
		for _, item in LEGACY do
			local n = select(2, string.gsub("\n" .. source, item[2], ""))
			if n > 0 then legacy[item[1]] = (legacy[item[1]] or 0) + n end
		end
		if total % 200 == 0 then task.wait() end
	end
end
table.sort(sizes, function(a, b) return a.lines > b.lines end)
for i = 1, math.min(10, #sizes) do print(sizes[i].lines, sizes[i].path) end
local duplicated = 0
for _, n in copies do if n > 1 then duplicated += n end end
print("scripts", total, "strict", strict, "identical copies", duplicated)
print(byPlace, legacy) -- Workspace/Script above zero means scripts inside models
```

| Symptom | Likely cause | Fix |
|---|---|---|
| A fix is applied but the bug persists | The same script is copied into many models | Sketch F "identical copies"; one CollectionService component per tag |
| Works in Studio, errors live ("attempt to index nil", infinite yield) | Streaming and load-order races; client indexes Workspace paths directly | `WaitForChild` with timeout or tags; loop existing players and characters |
| Start-up errors that come and go | Many auto-running Scripts racing each other | One entry point per side and the Init/Start loader |
| Memory grows with every respawn or rejoin | Connections and per-player tables never cleaned | Trove per character and per player; leak audit |
| New nil errors after `SignalBehavior = Deferred` | Code reads state in the same frame it fires an event | Fix per the deferred-events pitfalls above |
| Studio edits vanish | Rojo is serving and the filesystem wins | Decide the owner; `rojo syncback` or edit the files |
| Scripts lose attributes or tags after syncing | Script Sync ignores them | Keep config in ModuleScripts; do not sync those scripts |
| Collaborators overwrite each other | Several people syncing or live-editing the same scripts | Git with reviews; Team Create Drafts mode; one place-file owner |
| CI is green and the game is broken | Lint only, nothing runs in engine | Jest Roblox smoke test through Luau Execution; MCP `playtest` subagent locally |
| An agent "fixed" it and nothing changed | Edited the Play-mode copy, one copy of several, or a file Rojo overwrote | Working rules 3–5 |
| `--!strict` floods the file with errors | Legacy untyped code | Strict on new and touched files; `--!nonstrict` elsewhere until rewritten |

## Review gate (architecture, Luau, tooling)

- [ ] One server entry, one client entry; no Scripts inside models; behaviour by tags.
- [ ] No require cycles; no yields at module top level or in `Init`.
- [ ] `PlayerAdded` and `CharacterAdded` handlers also cover existing players and characters.
- [ ] Every per-player table cleared on `PlayerRemoving`; every connection owned by a Trove.
- [ ] No `RunContext = Client` Script in a Starter container; `emitLegacyScripts` matches the layout.
- [ ] `--!strict`; untrusted input typed `unknown`; no `wait`/`spawn`/`delay`/`tick`/`Humanoid:LoadAnimation`/BodyMovers/`FindPartOnRay`.
- [ ] Every web-service call `pcall`ed with a failure branch.
- [ ] Code works under `SignalBehavior = Deferred`.
- [ ] Toolchain pinned to verified versions; `wally.lock` committed; selene, StyLua and luau-lsp gate every PR; only CI publishes production.
- [ ] One owner of the source (Rojo or Script Sync or Studio), written down; no unmaintained tools adopted (Mantle, Knit, TestEZ for new suites).
- [ ] Existing game: sketch F run; identical script copies and scripts inside Workspace models listed with an owner and a release to remove them.
- [ ] MCP client permissions at Balanced or lower; high-risk scopes off outside the task that needs them.
- [ ] Update runbook followed: versioned saves and cross-place messages, expand-then-contract, "outdated only" restart with bleed-off, `ServerRestartScheduled` drain handler present.
- [ ] No test switch is readable in production; the boot log lists active switches.

Grep `references/knowledge-base.md` for `## 4.1`, `## 4.2`, `## 4.3` and `## 4.10`.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/studio/{mcp,mcp-open-cloud,cli}.md`, `scripting/sync.md`, `ai/coding-harness.md`, `projects/{external-tools,collaboration,server-authority/index}.md`, `production/analytics/error-report.md` (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/41 Multiplayer Services/Server Shutdowns Soft Updates and Migration.md`, `03 Architecture and Networking/{Project Structure and Bootstrapping, Server Lifecycle and Shutdown, Frameworks - Knit Matter and Others, Interest Management and Per-Player Replication}.md`, `04 Data and Persistence/Data Loss Prevention and Recovery.md`, note titles in `12 Performance Testing and Debugging/` (read)
- `Roblox/creator-docs` `projects/update-games.md`, `reference/engine/classes/DataModel.yaml` (`ServerRestartScheduled`) (read)
- Tags and last commits (read via git): https://github.com/rojo-rbx/rojo, https://github.com/rojo-rbx/rokit, https://github.com/UpliftGames/wally, https://github.com/Kampfkarren/selene, https://github.com/JohnnyMorganz/StyLua, https://github.com/JohnnyMorganz/luau-lsp, https://github.com/lune-org/lune, https://github.com/Roblox/jest-roblox, https://github.com/jsdotlua/jest-lua, https://github.com/Roblox/testez, https://github.com/Sleitnick/rbxcloud, https://github.com/blake-mealey/mantle, https://github.com/Sleitnick/Knit, https://github.com/red-blox/zap, https://github.com/1Axen/blink, https://github.com/Ukendio/jecs
- READMEs (read): https://github.com/Roblox/studio-rust-mcp-server, https://github.com/Roblox/jest-roblox, https://github.com/blake-mealey/mantle
- Rojo 7.7 release notes, seen through https://newreleases.io/project/github/rojo-rbx/rojo/release/v7.7.0-rc.1 and a release mirror (search summary)
- https://devforum.roblox.com/t/studio-script-sync-now-in-beta/4065468, https://devforum.roblox.com/t/studio-mcp-server-updates-and-external-llm-support-for-assistant/4415631 (search summary)
- Not reachable: the GitHub REST API for these repos (blocked in this session), so release notes were not read first-hand; versions come from `git ls-remote --tags` and tag commit dates.
