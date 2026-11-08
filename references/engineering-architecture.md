# Engineering architecture, Luau standards and tooling

Distilled from knowledge-base sections 4.1, 4.2, 4.3 and 4.10. Use it when setting up a project, choosing a framework, writing Luau, or configuring Rojo, Wally, CI and the Studio MCP. Snippets are patterns to adapt; they were checked against the docs but not executed. `[VS]` marks version-sensitive facts.

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

`[VS]` Server authority mode (`Workspace.AuthorityMode = Server`, `RunService:BindToSimulation`, `SetPredictionMode`) is new and maturing. Use it for competitive physics games (racing, sports, shooters); keep client ownership plus server validation elsewhere.

## Project architecture

One server entry `Script` and one client entry `Script`; everything else is ModuleScripts ("services" on the server, "controllers" on the client) run through an Init/Start lifecycle:

1. Require every module (top-level code builds tables only; no yields, no cross-module calls).
2. `Init()` on each: own state, own remotes, own signals. No calls into other services, no yielding.
3. `Start()` on each in its own `task.spawn`, so one yielding service cannot block the rest. Cross-service calls are safe from here.
4. Connect `Players.PlayerAdded` last, and loop `Players:GetPlayers()` to catch early joiners.

Rules: no require cycles (resolve lazily in `Init`); shared modules never require server modules; services expose functions, not mutable tables; no server logic in replicated modules.

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
| Knit | Archived, unmaintained | Do not start new projects on it |
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

- `--!strict` on every new file. `--!nocheck` only for vendored code. `[VS]` The new type solver is still rolling out; prefer simple type shapes.
- Types: `export type`, generics, unions, `T?`, `typeof(setmetatable({} :: Fields, Class))` for classes, `unknown` for untrusted input (forces refinement), singleton string types for enums.
- Naming: PascalCase for services, modules, types and instances; camelCase for locals and functions; SCREAMING_SNAKE_CASE constants; `_private`; `is/has/can` booleans; **`Async` suffix on every yielding function**.
- Errors: `pcall` every yielding call to a web service (DataStores, MemoryStores, MessagingService, MarketplaceService, TeleportAsync, HttpService). `xpcall(fn, debug.traceback)` when you need a trace. `assert` for programmer errors only. Never swallow errors silently; `warn` with context. Retries use exponential backoff with jitter.
- Scheduling: `task.wait`, `task.spawn`, `task.defer`, `task.delay`, `task.cancel`. Never `wait`, `spawn`, `delay`. Per-frame work on `RunService.Heartbeat` (server), `PreRender` (client camera and visuals), `PreSimulation`/`PostSimulation` (physics-adjacent).
- Deferred events `[VS]`: set `SignalBehavior = Deferred` now. Pitfalls: fire-then-read returns stale state; disconnect does not cancel already-queued invocations (use `:Once()`); `Destroying` handlers run after the instance is destroyed; re-entrancy capped at 10.
- Cleanup: every object with a lifetime owns a Trove (RbxUtil `Trove`; Maid and Janitor are older equivalents). Per-player tables are cleared on `PlayerRemoving`. Use RbxUtil `Signal` instead of `BindableEvent` for module-to-module events (BindableEvent deep-copies tables and strips metatables).
- Promises (evaera) are useful for fan-out with timeouts, cancellation and retries; otherwise plain yielding code with `Async` naming is clearer.
- Performance: `--!native` or `@native` only on measured hot server (or Android client) code `[VS]`; `buffer` for compact binary data; cache services and functions in locals; avoid closures and tables per frame in hot loops. The 2025 runtime added `vector`, `math.lerp`, `math.map`, `math.isnan`, `math.isinf`, `math.isfinite`, `buffer.readbits`, `buffer.writebits`.

## Toolchain `[VS]`

| Tool | Role |
|---|---|
| Rokit | Pins every CLI in `rokit.toml` (supersedes Aftman and Foreman) |
| Rojo | Filesystem ↔ Studio sync; `rojo build`, `rojo serve`, `rojo sourcemap`. Never `rojo upload --cookie` in CI |
| Studio Script Sync | Built-in script-only sync; up to 10,000 scripts per root. Use it when Studio owns the source |
| Wally | Packages; commit `wally.lock`; CI runs `wally install` then `git diff --exit-code wally.lock` |
| Selene | Lint, `std = "roblox"` |
| StyLua | Format, `stylua --check src` |
| luau-lsp | `luau-lsp analyze` with a fresh `sourcemap.json` |
| Lune | Standalone Luau runtime for build scripts (asset upload, codegen, unit tests) |
| Jest-Lua / TestEZ | In-engine tests |
| rbxcloud, Mantle | Open Cloud CLI; infrastructure as code |

```toml
# rokit.toml
[tools]
rojo = "rojo-rbx/rojo@7.6.1"
wally = "upliftgames/wally@0.3.2"
lune = "lune-org/lune@0.10.4"
selene = "kampfkarren/selene@<pin>"
stylua = "johnnymorganz/stylua@<pin>"
luau-lsp = "johnnymorganz/luau-lsp@<pin>"
```

Rojo when the filesystem is the source of truth (git, CI, AI agents); Script Sync when Studio is.

## Testing

- Pure logic (economy maths, damage formulas, migrations, validators) lives in Instance-free modules tested under Lune.
- In-engine tests run in a test place via the Studio CLI (`RobloxStudioBeta.exe --task RunScript --placeId <id> --universeId <id> --runScriptFile tests.luau --outputFile out.log --quitAfterExecution`) or Open Cloud Luau Execution.
- Data code runs against `ProfileStore.Mock`.
- Multi-client tests: `StudioTestService` (`ExecuteMultiplayerTestAsync`, `AddPlayers`) and `UserInputService:CreateVirtualInput()`.
- Leak audit: respawn 20 times and rejoin repeatedly; memory and connection counts return to baseline.

## CI/CD with Open Cloud `[VS]`

Luau Execution API: `POST /cloud/v2/universes/{universeId}/places/{placeId}/luau-execution-session-tasks` with `{ "script": "...", "timeout": "300s" }`; poll until `COMPLETE` or `FAILED`. Limits: 4 MB script, 5 minutes, 4 MB return JSON, 450 KB logs, 100 MiB binary input valid 15 minutes. No physics, no auto-run scripts, DataModel changes not persisted; DataStores work.

Place publishing: `PATCH https://apis.roblox.com/assets/v1/assets/{placeId}` with `request={"assetId":<placeId>,"assetType":"Place","published":true}` and `fileContent` (`.rbxl` as `application/octet-stream`); poll `GET /assets/v1/operations/{id}`. Key needs assets Read and Write.

Pipeline: on every PR run `rokit install`, `wally install` + lock diff, `selene src`, `stylua --check src`, `rojo sourcemap`, `luau-lsp analyze`, Lune unit tests. On merge: `rojo build -o game.rbxl`, publish to a test place in a separate test universe, run in-engine tests. On release tag: publish to production with a manual approval, using Migrate To Latest Update for non-backwards-compatible data migrations. Keys live in CI secrets, scoped to one universe and minimum permissions.

Collaboration: place files do not merge; code merges in git; one place-file owner at a time; Git LFS with locking for binaries; only CI publishes production.

## AI agents and the Studio MCP `[VS]`

Studio ships an MCP server (enable "Enable Studio as MCP server" in Assistant settings; stdio transport; Windows command `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`; a port-13469 conflict breaks the connection). Every call takes a `studio_id` from `list_roblox_studios`.

Working rules:

1. Connect, then orient: `list_roblox_studios`, confirm the target place, `get_studio_state`, and find out who owns the files (Rojo, Script Sync or Studio).
2. Explore before editing: `search_game_tree`, `inspect_instance`, `script_search`, `script_grep`, or an `execute_luau` listing. Fix every copy, not the first one found.
3. Edit source in Edit mode. Play-mode changes are discarded; `execute_luau` runtime changes do not persist in scripts. If Rojo owns the files, edit the files.
4. A write is not done until a read shows it. Re-read with `script_read`, then `start_stop_play` and check `get_console_output`.
5. Modify what exists; never add parallel copies; preserve the hierarchy.
6. `execute_luau` freezes Studio until it yields; batch about 1,000 items per `task.wait()`. `require` in Edit context gives fresh module state. Never publish, save or delete unasked. Stop after the same error repeats twice.
7. House rules override convenient tools: never ship visible content from `generate_procedural_model`, `generate_mesh`, `generate_scene`, `insert_asset` or `search_asset`. Visible assets come from the Blender pipeline (art-pipeline-blender.md). These tools are acceptable only for throwaway experiments that never reach the shipped place.
8. Verify APIs against `https://create.roblox.com/docs/llms.txt` or the `.md` page versions; do not guess.

OpenGameEval (Roblox's agent benchmark) ties failures to under-exploration and to fixing one copy when several exist; best core Pass@1 was about 50% at time of reading.

## Review gate (architecture, Luau, tooling)

- [ ] One server entry, one client entry; no Scripts inside models; behaviour by tags.
- [ ] No require cycles; no yields at module top level or in `Init`.
- [ ] `PlayerAdded` and `CharacterAdded` handlers also cover existing players and characters.
- [ ] Every per-player table cleared on `PlayerRemoving`; every connection owned by a Trove.
- [ ] No `RunContext = Client` Script in a Starter container; `emitLegacyScripts` matches the layout.
- [ ] `--!strict`; untrusted input typed `unknown`; no `wait`/`spawn`/`delay`/`tick`/`Humanoid:LoadAnimation`/BodyMovers/`FindPartOnRay`.
- [ ] Every web-service call `pcall`ed with a failure branch.
- [ ] Code works under `SignalBehavior = Deferred`.
- [ ] Toolchain pinned; `wally.lock` committed; selene, StyLua and luau-lsp gate every PR; only CI publishes production.

Grep `references/knowledge-base.md` for `## 4.1`, `## 4.2`, `## 4.3` and `## 4.10`.
