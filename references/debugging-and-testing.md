# Debugging and testing: from "it's broken" to the cause

What this is: a symptom-driven debugging reference (method, tools, error decoder, a large symptom table, live-only capture, leak hunting) plus the test strategy, error-handling and logging conventions that stop the same bug returning. Open it when something is broken, when a live game has bugs you cannot reproduce, or before a release. Tool and API facts were re-checked on 2026-11-11 against `Roblox/creator-docs` (commit 7cbffff), the DevForum announcements and the Jest Roblox repository. Snippets are unexecuted sketches. Tags: `[official]` docs, `[community]` forum practice, `[VS]` version-sensitive, `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2.

It extends, and does not repeat: `engineering-architecture.md` (toolchain, CI, Studio MCP rules, sketch F), `performance.md` (MicroProfiler tags, budgets, memory labels), `data-and-purchases.md` (DataStore and receipt code), `networking-and-security.md` (remote guard), `ui-input-crossplatform.md` (UI symptom table), `luau-mastery.md` (language).

## Contents

Start here by level · The method · Tools · Reading errors (decoder) · Symptom table · Races and load order · Live-only bugs (capture kit) · Memory-leak hunting · Error handling and retries · Logging and telemetry · Test strategy · Pre-release regression checklist · Review gate · Sources

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | Keep the Output window open and fix the **first** red line, not the last. Ask "server or client?" before reading code (Client/Server toggle in a play test). Reproduce the bug three times on purpose before changing anything. Use the symptom table below | Profilers, heap snapshots, test frameworks |
| Intermediate | Write the repro with a failure rate ("4 of 10"). Use conditional breakpoints and logpoints instead of print-and-delete. Test with 2+ clients and the Network Simulator. Own every connection with a Trove. Put economy maths, drop tables and migrations under unit tests | Parallel debugging, custom telemetry pipelines |
| Expert | Build the capture kit before the incident: server tag in every log line, state dumps, kill switches, a canary. Diff Luau heap snapshots around a 100× loop. Run soak tests and `StudioTestService` multi-client suites in CI. Treat every fix as unproven until it survives 2× the original failure count under latency | Nothing: but measure before optimising |

Related: `studio-workflow.md` (test modes, the testing ladder, Team Test, working through the Studio MCP); `engineering-architecture.md` (CI and the test stack); `performance.md` (profiling).

## The method: reproduce, isolate, hypothesise, verify

A fix without a reproduction is a guess; a `task.wait(n)` or a silent `pcall` that makes a bug rarer is not an explanation `[lihfolk]`.

1. **Reproduce.** Write it down: start state, steps, expected, actual, and a rate.
   `Start: fresh profile, Studio, 2 clients, "Standard Mobile (4G/LTE)" preset → 1. A equips bow 2. A unequips and re-equips within 1 s 3. B looks at A → Expected: B sees the bow. Actual: nothing, 7 of 10.`
   The rate tells you whether timing is involved and sets the bar for the fix: 0 of 20 is evidence, 0 of 3 is not `[lihfolk]`.
2. **Reach the state fast.** Build once, Studio-gated or allow-listed on the server: a cheat service (set level, grant items, teleport, fire world events), named test profiles (`fresh`, `endgame`, `schema-v3`) on test keys, and seeded randomness (`Random.new(seed)`, one generator per system, seed logged at server start).
3. **Make it frequent.** Each lever that raises the rate is also a clue `[lihfolk]`:

| Lever | How | A higher rate means |
|---|---|---|
| Latency, jitter, loss | Network Simulator preset (see Tools) | Ordering or replication timing |
| Low frame rate | Throwaway client script burning CPU per frame | Per-frame logic assumes a frame length |
| More clients | Server & Clients with 3–8 players | Shared state, contention, ownership |
| Spam the action | Auto-fire loop in a debug script | Missing debounce; two requests in flight |
| Slow storage | Wrap the data layer with `task.wait(2)` in Studio | Load-order assumptions |
| Streaming | Small `StreamingTargetRadius`, `StreamOutBehavior = Opportunistic` on a QA copy | Client assumes an instance exists |
| Join order | Studio Settings > Network > Randomize Join Instance Order: instances arrive in the shuffled order a long-running server produces `[official]` | Client assumes one instance arrives before another |
| Injected jitter | `task.wait(math.random() * 0.5)` before the suspect step, Studio only | You have found the race |

4. **Isolate: which side, then the first wrong value.** Server or client (`RunService:IsServer()` in the path, the Client/Server toggle, F9 Log switch). Then walk back from the visible wrong value to the first place it was wrong: UI shows 0 → is the replicated value 0 → is the server value 0 → was it loaded as 0 or set later. Funnel writes through one setter and put the assertion and `debug.traceback()` there; a changed-signal handler only tells you that it changed, not who wrote it `[lihfolk]`.
5. **Bisect** anything ordered. Scripts: on a **copy** of the place, disable half the systems (`Script.Enabled = false`; group by system so dependents do not hang), about log2(N) runs: 400 scripts is 9 runs. Versions: `git bisect` with Rojo, or restore mid-range Version History builds into a test place. If every old version shows the bug, the cause is stored data, not code `[lihfolk]`. Data: copy the failing profile to a test key and delete half the fields per round. Time: log a value every 30 s and find the first interval where it moved.
6. **Hypothesise in one sentence** ("the player rejoined fast, so the new server loaded the key while the old server's leave-save was still in flight, then wrote its stale copy back"). If you cannot write the sentence, keep isolating.
7. **Fix the cause, then verify** with the original repro under the conditions that made it frequent, at least twice the run count it took to fail. Remove injected delays and debug seeds.
8. **Leave a guard**: a unit test, a boundary assertion, validation on the remote, or a live counter you can watch. Add one line to the bug log (symptom, cause, fix).

Signs a fix is a guess `[lihfolk]`: it adds a wait or a longer timeout; it wraps something in `pcall` and drops the error; it works "most of the time"; nobody can state the sequence of events.

Heisenbugs: a breakpoint changes timing (other machines keep running), a print with `GetFullName()` on many instances changes frame time, a `WaitForChild` in a debug script changes when it resumes. A bug that vanishes under the debugger is a timing bug: switch to logs with `os.clock()` and a sequence counter.

## Tools: what each one answers

| Tool | Open it | Answers | Limits |
|---|---|---|---|
| Output | Window menu or Script tab | First error, stack trace (click to jump), warnings | Filter by context and type; a clean run has zero errors and zero unexpected warnings |
| Script Analysis | Window menu | Type errors, unknown globals, deprecated calls before you run | Lint subset only `[official]` |
| Breakpoints | Click the gutter; right-click for Conditional or Logpoint | Pause on a state (`enemy.Name == "Boss"`), or print without editing the script (logpoint, "Continue Execution" on) | Set the **context** (Client, Server, Edit) or a shared ModuleScript stops on the wrong side; breakpoints disable native execution for that function `[official]` |
| Stepping, Call Stack, Watch | F10 over, F11 into, Shift+F11 out. Pause, then Step Forward in the test toolbar advances physics and animation 1/60 s (scripts keep running) `[official]` | Who called this with the bad value; table contents; one physics frame at a time | Useless for timing bugs and unavailable on live servers |
| Developer Console | F9, `/console` in chat, or Roblox menu > Settings > Developer Console (the route on phones) `[official]` | Live client and server logs, memory, profilers | Server view only for the owner or group members with edit permission `[official]` |
| Console: Log | Client/Server switch | Live server errors that never happen in Studio (throttling, odd remote arguments) | The server command bar runs real code in a production server with a Script's permissions: read-only commands unless you mean it `[official]` |
| Console: Memory, LuauHeap | Tools dropdown | Which category grows; snapshot diffs; who pins an instance | A snapshot can time out a live server with a very large heap; Parallel Luau VM heaps are not included `[official: staff post]` |
| Console: ScriptProfiler | Client or Server; 1 kHz or 10 kHz; 1, 5, 10 min or manual `[official]` | Which function burns CPU (Callgraph or Functions view, ms or %, JSON export); `<native>` marks native functions | Sampling: it misses sleeping threads |
| Console: Network | Summary and Details | **Web calls**: HttpService and service requests such as DataStores, with failures and timings `[official]` | Not replication traffic; for that use the stats overlays in `performance.md` |
| MicroProfiler | Ctrl+F6 in Studio and the desktop client (some doc pages print Ctrl+Alt+F6); phones through the in-game Settings menu and a browser | Which frame phase is slow; `debug.profilebegin` labels | Tag table and mobile capture are in `performance.md` |
| Network Simulator `[VS]` | Test > Device Simulator > Network pill (beta: enable "New Device Simulator" under File > Beta Features). Pick a preset, then press **Apply**: until then it is only staged | Behaviour under latency, jitter and loss per direction. Presets, inbound latency / jitter / loss: Ideal Fiber 8 ms / 0 / 0 (the default, not zero); Wired Broadband 25 / 3 / 0; Home Wi-Fi 30 / 12 / 0.2%; Standard Mobile (4G/LTE) 45 / 20 / 0.4%; Bad Connection (3G) 150 / 70 / 0.5% `[official]` | Added on top of real conditions; ranges 0–1000 ms and 0–0.5% loss; the same values live in Studio Settings > Network and in `NetworkSettings` properties for plugins; set it back to Ideal Fiber after the test |
| Server & Clients | Test dropdown, 1–8 clients (F7) `[official]` | Replication, late join, per-player isolation | Same machine: no real latency unless simulated |
| Error Report | Creator Hub > Monitoring > Error Report | Top live errors by count, with stack, platform, "new errors since version". The same data is readable through the Open Cloud Error Reporting API (`universe.analytics:read`) `[official]` | Tracks 500 unique errors and 500 unique warnings plus the top 100 new per version, reset every 6 hours; 100 ignore or group rules, regex must not start with a wildcard `[official]` |
| Performance and Crashes dashboards, Alerts | Creator Hub > Monitoring; alerts under Configurations > Alerts | Crash rate, out-of-memory exits, memory by server age, server frame rate; a webhook when one crosses a threshold | Need about 100 daily users; details in `performance.md` |
| `LogService` | Script | `MessageOut(message, messageType, context)` for forwarding; `GetLogHistory()` (512 entries by default); structured logging `[official][VS]` | A `MessageOut` handler that prints feeds itself |
| `ScriptContext.Error` | Script | Uncaught errors with stack and script, per side | Errors you `pcall` never reach it, and neither do watchdog timeouts `[official]`: report those yourself |
| `debug.traceback`, `debug.info` | Script | Where am I and who called me; `debug.info(fn, "sl")` gives a callback's source and line | Never parse traceback text; `debug.info` is the stable one |
| Log files | Windows `%LOCALAPPDATA%\Roblox\logs`; Mac `~/Library/Logs/Roblox`; iOS via Console.app or sysdiagnose; Android via Logcat `[official]` | What happened before a client or Studio crash | Ask a tester for these when the app dies without a script error |
| Studio MCP | `get_console_output`, `start_stop_play`, `execute_luau` (`datamodel_type` Edit, Client or Server), `inspect_instance`, `character_navigation`, input tools, `screen_capture` | An agent-driven repro loop (below) | Play-mode edits are discarded; a black screenshot is not evidence `[lihfolk]`; `studio_id` changes on restart |

Agent repro loop through the Studio MCP `[VS]`: (1) `get_studio_state`, confirm Edit mode and the target place; (2) `start_stop_play` to start; (3) drive the repro with `character_navigation` and the input tools, or set state with `execute_luau` on the Server DataModel (test place only); (4) `get_console_output` and read the first error; (5) `execute_luau` once per side to read the suspect value on Server and on Client: that answers "which side"; (6) stop, edit source in Edit mode, read the write back, repeat. For timing bugs run it N times and report the rate. Rules for agents are in `engineering-architecture.md`.

## Reading errors: decoder

The line is `Script.Full.Name:LINE: message`, then the stack, innermost first. The top frame is where it failed; the bug is usually one or two frames down, where the bad value was passed in `[lihfolk]`.

| Message | Means | Check first |
|---|---|---|
| `attempt to index nil with 'X'` | The thing **before** `.X` is nil | Data-driven id that does not exist; a `FindFirstChild` result used unchecked; not replicated or streamed yet (client only); character gone; a function with an early `return` |
| `X is not a valid member of Y "Path"` | Parent exists, child or property does not | Child not replicated yet; renamed; typo; wrong property name for the class |
| `attempt to call a nil value` / `missing method` | Called something that is nil | Typo; `local function` used above its definition; `.` vs `:` mismatch; module returned before defining it |
| `attempt to perform arithmetic (add) on nil and number` | One operand nil | A field missing from old saves: fix at load with defaults and migrations, not at every use |
| `invalid argument #N to 'f' (number expected, got nil)` | Built-in got the wrong type | Count arguments by eye; `Vector3.new(x, y)` with nil z; too few `string.format` args |
| `Unable to cast value to Object` | Wrong type crossed into the engine | An Instance sent over a remote that the receiver cannot see arrives as nil |
| `Infinite yield possible on 'A:WaitForChild("B")'` | Warning after 5 s without a timeout `[official]` | Wrong name; the creator script errored earlier (scroll up); server-only container; streamed out; you waited on the **old** character or GUI |
| `Script timeout: exhausted allowed execution time` | A thread ran too long without yielding | A loop whose exit depends on something that cannot change while it spins; huge one-shot work. The watchdog budget is per resumption and is off (0) unless set `[official]`; Studio has its own timeout setting `[community]`. Yield, do not raise the limit |
| `stack overflow` | Recursion too deep | No base case; `__index` reading a missing `self.x` (use `rawget`); a `Changed` handler writing the same property |
| Maximum event re-entrancy depth | A deferred handler keeps re-firing its own event; limit 10 `[official]` | Compare before writing; do not switch `SignalBehavior` back |
| `Requested module experienced an error while loading` | The module threw on first run | The real error is printed just above; every later `require` repeats this line |
| `The Parent property of X is locked` | Re-parenting a destroyed instance | A stale reference used after a yield or in a deferred callback |
| `attempt to yield across metamethod/C-call boundary` | Yield where it is not allowed | Yielding inside a metamethod, a `table.sort` comparator or a `gsub` callback |
| `... can only be called by the backend server`, `HTTP requests are not enabled`, DataStore 403 in Studio | Wrong side or a setting | Client calling a server API; Game Settings > Security (HTTP, Studio access to API services) |
| `<RequestType>GameServerThrottled` / `ExperienceThrottled` `[VS]` | DataStore per-server or experience budget exceeded `[official]` | See `data-and-purchases.md`; back off with jitter |

When the trace misleads `[lihfolk]`: an error in a `task.spawn` or event-handler thread starts its trace at that function (log context at spawn time); frames before a yield may be gone (log before yielding); `pcall` then `error(err)` points at your re-raise (use `xpcall(fn, debug.traceback)`); `error(msg, 2)` deliberately blames the caller; a table passed to `error` prints as an address unless it has `__tostring`. Under a flood of 300 lines: first error, filter by side, group identical messages (a count of 600 is one nil in a `Heartbeat` handler), ignore `CoreGui`/`CorePackages` noise.

## Symptom → likely causes → confirm → fix

Causes are listed most common first. "Confirm" is the cheapest observation that separates them.

| Symptom | Likely causes | Confirm | Fix |
|---|---|---|---|
| "Infinite yield possible" | Wrong name or path; creator script errored first; server-only container; streamed out; stale parent after respawn | Scroll to the first error; inspect the path on that side with the Client/Server toggle | Fix the path; resolve replicated containers once at start-up; timeout plus nil branch where absence is legal; tags for streamed content |
| Nil index after streaming ("works near spawn", "works the second visit") | Client indexes Workspace directly; `GetTagged` once with no added/removed signals; remote passes an Instance the client does not have | QA copy with `StreamOutBehavior = Opportunistic` and a small target radius; go far, come back, interact again `[lihfolk]` | Tag components with added and removed handlers; `WaitForChild(name, timeout)`; Atomic models for interactables; handle nil Instance arguments |
| Works in Studio, not live | Not published, or Team Create drafts not committed `[community]`; asset owned by another user or group (animation, audio); a setting (HTTP, API access, third-party teleports); latency and streaming races; client doing server-only work; `RunService:IsStudio()` branches; text filtering and real purchases behave differently in Studio | F9 in the live game, server Log first; compare `game.PlaceVersion` with the published version; Server & Clients plus the 4G preset in Studio | Publish and verify the version; re-upload assets under the experience owner; fix the race properly (below) |
| Client/server desync (my screen differs from theirs; late joiners wrong) | State sent as one-off events; client changed a value locally; each side has its own module copy; clocks compared across machines; unreliable remote used for state | Read the same value on both sides (toggle or MCP `execute_luau` per side); join a second client late | Server writes state as attributes or values; moments go through remotes; timers use `workspace:GetServerTimeNow()` and a server-set end time; versioned snapshots with resync `[lihfolk]` |
| Rubber-banding (players or vehicles snap back) | Server-side movement check correcting a legitimate move; network ownership flipping or left on the server; server frame rate low; high ping; server-authority mispredictions | Ownership debug colours and Studio's "Are Owners Shown" `[community]`; server frame rate in F9; repeat on the 3G preset | Set ownership once (driver on sit, server on exit, again after any unanchor: `physics-and-vehicles.md`); widen tolerances and exempt teleports; fix server CPU; see `networking-and-security.md` and `physics-and-vehicles.md` |
| Remote "not firing" | Handler connected late or never (the script errored above it); two remotes with the same name; `FireClient` without the player or `FireServer` on the wrong side; an Instance argument arriving nil; payload over the unreliable size limit dropped; your own rate limiter rejecting silently | Print on both sides at send and receive; first error in Output; count instances with that name | Create remotes in one place before any script runs; connect in `Init`; send ids, not Instances; log rejects with a sampled counter |
| Data not saving | Studio API access off (403); nil load after an error treated as a new player; no session lock (fast rejoin overwrites); save cut off at shutdown (no `BindToClose` or serial saves); unserialisable value (`Vector3`, mixed table, NaN); yield inside an `UpdateAsync` transform; reading the 4-second cache | Uncached read (`UseCache = false`); list the key's versions; F9 Network failures; throttle error names | ProfileStore-style session lock; a failed load never saves; parallel saves in `BindToClose`; plain values only. Code in `data-and-purchases.md` |
| Memory grows per respawn, round or hour | Connection on a long-lived signal from a short-lived object; per-player table written after the player left; threads waiting forever; tracks or UI created per use | Sampler slope by category; respawn 100× and diff heap snapshots (below) | Trove per lifetime; re-check after yields; one loop over a registry; explicit removal |
| Event fires twice (double damage, double purchase UI) | Connected again on every respawn or menu open; object constructed twice with no `Destroy`; under Deferred signals, several invocations queued before the handler could react (and `Destroy()` still runs queued handlers) `[official]`; `Touched` once per body part; a `RunContext = Client` Script in a Starter container; marker in two animation tracks | Log `debug.traceback()` at the connect site; count handler calls per fire | Connect once per lifetime and disconnect in the Trove; `:Once()`; dedupe by character and debounce before the yield |
| Race at join (first player gets nothing, HUD empty on slow phones) | `PlayerAdded` connected after the player arrived; UI built once before data replicated; client fires before the server is ready; receipt replay before the profile loaded | 300 ms inbound latency; injected jitter around the data load; sequence log | Subscribe then iterate with a guard (sketch below); a `DataLoaded` attribute as the readiness signal; `NotProcessedYet` until the profile exists |
| Respawn bugs (UI stuck at 0 health, ability fires twice, perk gone) | Listeners bound to the old Humanoid; `ResetOnSpawn` rebuilding UI; waiting on the old character; game-pass benefits applied once; one system split across StarterCharacterScripts and StarterPlayerScripts | Reset twice quickly, then test; count connections | Rebind on `CharacterAdded`; `if player.Character ~= character then return end` after every yield; `ResetOnSpawn = false` for persistent UI; reapply perks per spawn |
| UI missing on mobile | Offset-sized or off-screen layout; `ScreenInsets` and `ClipToDeviceSafeArea` clipping it; covered by the top bar or touch controls; shown only on a keyboard event; `MouseButton1Click` paths with no `Activated`; unreadable `TextScaled` | Device Simulator with a phone preset and touch; then a real phone | Scale plus constraints, safe-area insets, `Activated`, an on-screen button for every action. Table in `ui-input-crossplatform.md` |
| Paid, nothing granted | Two scripts assign `ProcessReceipt` (last wins); grant in `PromptProductPurchaseFinished`; `PurchaseGranted` returned before the save; profile not loaded and `NotProcessedYet` returned: there is no timed retry, the callback runs again only when the player rejoins or starts another product purchase `[official]` | Server log around the purchase; receipt counter "processed vs granted"; search the code for a second assignment | One idempotent handler keyed by `PurchaseId`; wait for the profile; save, then grant. Code in `data-and-purchases.md` |
| Teleport fails or strands players | `TeleportAsync` not in `pcall`; `TeleportInitFailed` ignored; invalid options (these error but never fire `TeleportInitFailed` `[official: staff reply]`); retried twice by two mechanisms; `GameFull`; tested in Studio | Log `Enum.TeleportResult` and the message; test in a live private server | One retry path: `Flooded` wait 15 s, `Failure` 1 s, cap 3, then tell the player; `RequestStreamAroundAsync` first for in-place moves; reserved servers by `ReservedServerId` `[VS]` |
| "Script timeout" or a freeze with no error | `while` or `repeat` that never yields; unbounded retry loop; work over 100k items in one go | Search for `while true do` and `repeat` without a yield or a cap; bisect systems | Yield per time slice (about 5 ms); cap every retry loop; chunk long jobs |
| Players or parts flung | Overlap at spawn or teleport; heavy non-`Massless` part welded to a character; mover with no force limit; NaN from `.Unit` of a zero vector; two movers on one assembly | Physics visualisation (contacts, owners, awake parts); log velocity and NaN checks at the write | Spawn above ground and test overlap with `GetPartsInPart`; `Massless` on attachments; `ForceLimitsEnabled`; guard non-finite values before writing a CFrame |
| Animation plays for me, not for others | `LoadAnimation` ran before the server-created Animator replicated, creating a local-only Animator `[community]`; NPC clip played in a LocalScript; asset owned by a different user or group than the experience; Studio-only temporary ids | Look for two Animators under the Humanoid; test in a live group game; check the id's owner | Create the Animator on the server and `WaitForChild("Animator")` on the client; play shared NPC moments on the server; re-publish under the owner |
| Animations stop after long play | A new track loaded per use until the track limit `[lihfolk][VS]` | Animation memory category rises with attacks; Scene Analysis > Animation memory names the clips | Cache tracks per Animator |
| HTTP 429, DataStore throttling | HttpService over 500 external requests a minute per server (Open Cloud calls have a separate 2,500) `[official][VS]`; one request per log line or per player; serial calls that could batch; Open Cloud jobs sharing the DataStore budget | F9 Network summary (failed count per type); the throttle code name | Batch per 30–60 s; queue with backoff and jitter; start supported calls concurrently so the engine batches them `[official]`; `SetRateLimitForRequestType` at start-up `[VS]` |
| Fix applied, bug persists | Same script copied into many models; cached `require` in the command bar; Rojo overwrote the Studio edit; edited the Play-mode copy | Sketch F in `engineering-architecture.md`; re-read the source | One tagged component; edit the owner of the source |
| `pcall` returned true but an error printed | The error was in a spawned thread or handler | Trace starts at the spawned function | Return results from the thread; guard per iteration |
| Every button does the same thing | Handlers closed over one shared outer variable | Print the captured value | A local per iteration (see `luau-mastery.md`) |
| Part vanishes or camera goes black | NaN or infinity written to a CFrame (zero-vector `.Unit`, divide by zero, a spring that exploded on a long frame) | Print `value ~= value` at the write | Guard the write, clamp `dt`, sub-step springs |
| Coin awards several times | `Touched` per body part with no debounce | Count awards per touch | Set the taken flag before awarding; map part to player |
| Laggy only on full or old servers | Per-frame work that scales with players; leak; remote flood | Server ScriptProfiler; memory by server age | `performance.md` audit |

## Races and load order

Luau runs one thread at a time per VM, yet races are constant: a race is two pieces of code whose relative order is not fixed. The race surface of a function is its yields: `task.wait`, `WaitForChild`, `require` of a module that yields, every `Async` and web call, `:Wait()`, `InvokeServer`. Three more sources need no yield in your code: script start order (never guaranteed), deferred signals, and replication arriving in batches `[lihfolk]`. When you suspect a race, list the yields between cause and symptom; each is a candidate.

Subscribe, then catch up, with a guard and a post-yield check (unexecuted sketch):

```lua
--!strict
local Players = game:GetService("Players")
local seen: { [Player]: true } = {}

local function onCharacter(player: Player, character: Model)
	local humanoid = character:WaitForChild("Humanoid", 10)
	if not humanoid or player.Character ~= character then return end -- stale after the yield
	-- bind per-life state here; own it with a Trove cleaned on CharacterRemoving
end

local function onPlayer(player: Player)
	if seen[player] then return end -- the connect and the loop can both see one player
	seen[player] = true
	player.CharacterAdded:Connect(function(character) onCharacter(player, character) end)
	if player.Character then task.spawn(onCharacter, player, player.Character) end
end

Players.PlayerAdded:Connect(onPlayer) -- 1. subscribe first
for _, player in Players:GetPlayers() do task.spawn(onPlayer, player) end -- 2. then existing players
Players.PlayerRemoving:Connect(function(player) seen[player] = nil end)
```

The same shape applies to tags (`GetInstanceAddedSignal` then `GetTagged`), children (`ChildAdded` then `GetChildren`) and attributes (subscribe, then read the current value).

Rules:

- Readiness is an explicit flag or signal (`DataLoaded` attribute, a `Ready` signal), never a timer. `task.wait(1)` moves a failure from 30% of players to 3% and makes it harder to find `[lihfolk]`.
- `task.spawn` runs the function now, before your next line; `task.defer` runs after the current resumption, which is not "after everything loaded".
- After any yield, re-check what you captured: the player is still in the game, `player.Character == character`, `instance.Parent ~= nil`.
- Server handlers change state **before** they yield (spend, then refund on failure) or hold a per-player busy flag. Two requests inside the rate limit are enough to dupe.
- `PlayerRemoving` during a load in flight is the most expensive race on the platform: never save a profile that did not finish loading.
- Module top level never yields; one bootstrap defines Init and Start order (`engineering-architecture.md`).

Race tools: a sequence log (`{frame, counter, os.clock(), label}` on both sides of the suspected pair, compared between a good and a bad run), injected jitter, the Network Simulator, a low-end phone, and assertions on invariants ("no profile saves until its load has finished", "one player, at most one character binding").

## Live-only bugs: the capture kit

Ask first: which ingredient does the Studio repro lack `[lihfolk]`? Real latency and loss; 30+ players (budgets, contention); server age (leaks, drifting timers); real devices (memory kills, touch paths); asset permissions; teleports, private and reserved servers; real purchases; streaming at real distances; shutdown during an update. Add that ingredient to the repro before reading code.

Build these before the incident; none can be added during one:

1. **Server tag.** At start: `string.sub(game.JobId, 1, 8)`, `game.PlaceVersion`, start time. Put it in every log event, in a developer overlay, and in the settings menu so a player's screenshot names the server and version `[lihfolk]`.
2. **Join that server.** A gated admin command: `TeleportAsync` with `TeleportOptions.ServerInstanceId = jobId` `[VS]`, then F9 server Log, Memory and ScriptProfiler.
3. **State dumps.** Every system registers `dump(target: Player?): string` (phase, target, last change time, table sizes). Five lines when written with the system; "the boss is stuck" becomes one readable line.
4. **Log level per tag, raised remotely for minutes**, reverting by itself.
5. **Logs off the server.** Old servers are gone when the report arrives. Sink table:

| Sink | Good for | Cost |
|---|---|---|
| Error Report | Uncaught errors and warnings by version | 500 unique messages; dynamic text fragments it |
| AnalyticsService custom events | Funnels and counts: rejects, failures, timings | Aggregates only, nothing raw |
| HttpService to your endpoint | Searchable raw events | One batched request per server per 30–60 s; you secure it; privacy duties; key in Secrets |
| MemoryStore queue | Short cross-server buffer | Quota and expiry |
| DataStore | Almost never | Shares the budget with player data |

6. **Flags.** A kill switch per new system, tested in both states (a `ConfigSnapshot` does not update itself: `gameplay-systems-cookbook.md`); a canary (enable for about 5% of servers by hashing `JobId`) and compare error rates; live bisection by switching new systems off one at a time `[lihfolk]`.
7. **A bug-report button** that attaches the server tag, platform, zone and the last few client log lines; and a stuck-player watchdog that logs the state it found.

Facts: Open Cloud Luau Execution starts a headless server from a place version; it does not attach to a running one `[official]`. Client crash causes (out of memory, thermal) give scripts no event: read them as dashboard rates and correlate with version and platform. Client reports are hints, never facts for gameplay or moderation.

## Memory-leak hunting

1. **Is it a leak?** Growth with time or repetitions under a constant workload that never comes back. Not leaks: server memory not falling when players leave (it never shrinks `[official]`); a Luau heap sawtooth with flat troughs (allocation churn; rising **troughs** are the leak); texture and sound caches that plateau after one round trip; the first 5–10 minutes of warm-up. Need three samples after warm-up `[lihfolk]`.
2. **How urgent?** Express the slope as MB per hour or KB per repetition. A 20-player server has about 8.2 GiB (6.25 GiB + 100 MiB × players `[official]`): 60 MB/h from 1.5 GiB takes about 44 hours to reach the 50% line. The same slope on a 2 GB phone ends a long session, so client leaks usually come first `[lihfolk]`.
3. **Which category?** F9 Memory, or the sampler below.

| Growing | Usual cause |
|---|---|
| `LuaHeap` | Tables or closures held by a module table, upvalue or connection |
| `Signals` | Connections never disconnected (per respawn, per menu open) |
| `Instances` | Created and never destroyed, or destroyed but still referenced |
| `Animation` | Tracks loaded per use |
| `Gui`, `Sounds`, `GraphicsParticles` | Cloned per event and left parented |

4. **Multiply it.** A loop that repeats create-and-remove: respawn (`LoadCharacterAsync` from the server), equip and unequip, open and close every menu, enter and leave a zone, spawn and kill a wave, join and leave with `StudioTestService`. Wait a few idle seconds before the last sample: you cannot force a collection (`collectgarbage` only supports `"count"`) `[official: luau.org]`. Clean code shows under about 1 instance of growth per respawn `[lihfolk]`.
5. **Bisect systems** by a boot flag if the category does not name the owner. Call `debug.setmemorycategory("Combat")` first thing in every thread a system owns and the heap is reported per system `[official]`.
6. **Diff heap snapshots.** Snapshot A after warm-up, run the loop 100×, idle 10 s, snapshot B. Look for counts that grew by about 100 or a multiple; growth of 3 or 7 is noise `[lihfolk]`. Object Tags: `function` +100 is a handler per repetition; `table` +100 is a stored per-use table; `thread` +100 is a loop that never ends. Unparented Instances and Unique References list destroyed-but-referenced instances **with the path that pins them**; read the Graph bottom-up from the object to the module or upvalue that holds it `[official]`. Instances held by a Parallel Luau VM do not appear in Unique References `[official: staff post]`. In Studio, Scene Analysis (Window > Performance Summary) shows unparented instances per script and memory per animation clip: the docs call animation assets one of the most common leak sources `[official]`.
7. **Fix, prove, keep.** "Respawn soak, 200 cycles: +42 instances and +0.18 MB per respawn before; +0.2 and +0.002 after" is the proof. Keep the loop as a regression test.

The leak shapes worth memorising `[lihfolk]`:

| Shape | Why it leaks | Fix |
|---|---|---|
| Per-character code connects to `RunService`, `Players`, `UserInputService` or a global signal | `Destroy()` disconnects only connections on the destroyed instances; the service connection pins the character through its closure | Trove per character, cleaned on `CharacterRemoving` or `Destroying` |
| Per-player entry written after an async load | The player left during the yield, `PlayerRemoving` already ran | `if player.Parent == nil then return end` after every yield, before storing |
| A thread per object in `while true do` | A suspended thread roots its whole stack | `while object.Parent do`, or one loop over a registry; `task.cancel` on removal |
| `Parent = nil` instead of `Destroy()` | Connections stay live | `Destroy()`, unless pooling on purpose |
| Tag handler with no removed handler | Streaming re-adds the instance and setup runs again | Pair every added handler with a removed one |
| Cache keyed by player-controlled strings | Grows with every distinct input; exploitable | Validate length, cap entries, evict |
| Weak table relied on for cleanup | Luau has no ephemerons: a value that references its key keeps the entry forever; weak tables with Instances are not specified | Explicit removal on the end-of-life event; weakness is only a safety net |

`Workspace.PlayerCharacterDestroyBehavior = Enabled` makes the engine destroy old characters and leaving Players `[official]`; it does not help the first row. A slope sampler to leave running in test servers (unexecuted sketch):

```lua
--!strict
local Stats = game:GetService("Stats")
local TAGS = { Enum.DeveloperMemoryTag.LuaHeap, Enum.DeveloperMemoryTag.Signals, Enum.DeveloperMemoryTag.Instances, Enum.DeveloperMemoryTag.Animation, Enum.DeveloperMemoryTag.Gui }
local WINDOW, PERIOD = 20, 30 -- 20 samples, 30 s apart: a 10-minute slope
local history: { [Enum.DeveloperMemoryTag]: { number } } = {}
assert(Stats.MemoryTrackingEnabled, "per-tag memory is unavailable in this session") -- otherwise every read is 0
task.spawn(function()
	while true do
		for _, tag in TAGS do
			local samples = history[tag] or {}
			history[tag] = samples
			table.insert(samples, Stats:GetMemoryUsageMbForTag(tag))
			if #samples > WINDOW then table.remove(samples, 1) end
			if #samples == WINDOW then
				local mbPerHour = (samples[WINDOW] - samples[1]) / ((WINDOW - 1) * PERIOD) * 3600
				print("[Mem]", tag.Name, math.round(mbPerHour), "MB/h") -- live: send as a custom event, not warn
			end
		end
		task.wait(PERIOD)
	end
end)
```

When not to hunt: the slope is tiny against session length (5 MB/h with 20-minute sessions); the growth is a cache with a ceiling (a budget problem, see `performance.md`); crash rate and memory are within budget.

## Error handling and retries

| Rule | Why |
|---|---|
| `pcall` every web-service call (DataStore, MemoryStore, Messaging, Marketplace, Teleport, Http, Badge, Text filtering) and give the failure branch a behaviour | They fail in production as a matter of course |
| `xpcall(fn, debug.traceback)` at system boundaries (one quest handler must not kill the quest loop) | `pcall` loses the stack |
| `pcall(fn, a, b)`, not `pcall(function() return fn(a, b) end)`, in hot paths | No closure per call |
| `assert` and `error` for programmer errors; return `(ok, value)` or a tagged result for expected failures | Callers cannot ignore a result type as easily as a thrown string |
| `error(message, 2)` in library argument checks | Blames the caller's line |
| Never swallow: log with a **stable** message, then degrade | A swallowed error is worse than a crash |
| Long-lived loops catch per iteration | An error in a spawned loop ends it silently |
| Retry only what can succeed later: throttles, timeouts, 5xx. Never retry validation or permission errors | Retrying a 4xx burns budget |
| Retries are capped, exponential and jittered; at most one layer retries | Two layers multiply attempts |
| A failed load never leads to a save; a failed save never returns `PurchaseGranted` | Data loss and lost purchases |
| `LogService:Error` throws a structured error table (`message`, `template`, `context`, `stack`); `Logger:Error` logs and returns `[official][VS]` | Pick deliberately |

Retry helper (unexecuted sketch):

```lua
--!strict
export type Outcome<T> = { ok: true, value: T } | { ok: false, err: string }
local rng = Random.new()

local function retryAsync<T>(label: string, attempts: number, fn: () -> T): Outcome<T>
	local lastErr = "no attempt made"
	for attempt = 1, attempts do
		local ok, result = xpcall(fn, debug.traceback)
		if ok then return { ok = true, value = result :: T } end
		lastErr = tostring(result)
		if attempt < attempts then
			task.wait(math.min(2 ^ (attempt - 1), 16) * (0.5 + rng:NextNumber())) -- 1, 2, 4… s, ±50% jitter
		end
	end
	warn(`[Retry] {label} failed`) -- stable text: ids and counts go in telemetry fields, not the message
	return { ok = false, err = lastErr }
end
```

## Logging and telemetry conventions

- **Stable messages.** With `warn` or `print`, write `"Failed to load profile"` plus fields, never `"Failed to load profile for 12345678"`: the Error Report counts each distinct string against its 500 `[official]`. With the structured methods, put the variable part in the context table: Creator Analytics groups reports by message template, so `LogService:Warn("Failed to load profile for {userId}", { userId = id })` stays one row `[official: announcement 2026-06-04, read]`.
- **Structured logging `[official][VS]`.** `LogService:Info/Warn/Error/Output/Log(message, context)` take `{key}` placeholders and a context table; `LogService:GetLogger("Combat"):GetLogger("Damage")` gives a hierarchical `Logger` (`FullPath` `Combat.Damage`) whose messages bubble to ancestor loggers' `MessageOut`. Entries reach Output, the console and `GetLogHistory` with their context. The docs warn that content may be truncated: never build game logic on log contents. Keep context tables small: cloud features cap them at 1 KB.
- **Tags and levels.** One tag per system; production default `warn`; `info` and `debug` enabled per tag for minutes. A side prefix (`[S]`, `[C]`) when both outputs interleave. Rate-limit any log that can fire per frame.
- **Every event carries** the server tag, place version and, where needed, a `UserId`. Never chat text or other personal content.
- **Ship in batches**: one request per server per 30–60 s, bounded size, sampled where volume is high (1% of remote rejects is enough), with a drop counter so you know when you are blind `[lihfolk]`.
- **Client error reports** are deduplicated on the client, rate-limited per player on the server, type- and length-checked, and versioned.

Counters that catch what errors never will:

| Counter | Catches |
|---|---|
| Receipts processed vs granted | Purchase grant bugs |
| Save failures, retries, "load waited for session lock" | Data loss before players report it |
| Remote rejects per remote (sampled) | Exploit attempts and client bugs |
| Join to playable time (client) | Load regressions |
| Worst server frame per minute | Server performance regressions |
| Table sizes from state dumps (peak per hour) | Leaks |
| Stuck-player watchdog hits | Soft-locks |

Release triage `[lihfolk]`: in the first hour, Error Report filtered to "new errors since" this version, crash rate and out-of-memory exits by platform against the previous version, then your own counters. Roll back or flip the kill switch first, debug second.

## Test strategy

Say which level of proof a change reached; "done" means play-tested for anything that runs at runtime `[lihfolk]`.

| Level | Proves | Does not prove | Tool |
|---|---|---|---|
| Static | Compiles, types, lint | That it does the right thing | `--!strict`, luau-lsp analyze, Selene, StyLua, sketch F |
| Unit | Formulas, tables, state machines, validators, migrations | Engine integration | Lune for Instance-free modules; Jest Roblox in engine |
| Edit-mode dry run | Real code runs on real instances without errors | Timing, replication, physics, input | `execute_luau` in Edit; Studio CLI `RunScript` |
| Solo play test | Runtime behaviour for one player | Multiplayer, latency, late join | Studio Play; MCP `playtest` |
| Multi-client | Replication, join order, isolation | Real devices and networks | Server & Clients; `StudioTestService` |
| Live test | The shipped build on real devices | Rare races at scale | Private server in a test universe |
| Soak | Leaks, drift, server age | Player behaviour | Scripted respawn and churn loops |

Frameworks and status `[VS]` (versions in `engineering-architecture.md`):

| Tool | Status 2026-11 | Use for |
|---|---|---|
| Jest Roblox (`roblox/jest` 3.21) | Active; port of Jest 27.4.7; `describe`/`it`/`expect` must be required from `JestGlobals`; spec files must match `testMatch` in `jest.config.lua` (for example `**/*.spec`); an entry script calls `require(Packages.Jest).runCLI(root, {}, { root }):awaitStatus()` `[official README and docs]` | Default for new in-engine suites; runs in Studio and through Open Cloud Luau Execution |
| TestEZ | Legacy, no recent development | Keep existing suites only |
| Lune | Pre-1.0 standalone Luau runtime | Pure-logic tests on every push (`lune run test`), build scripts |
| `StudioTestService` | Studio only; the `Execute…` calls need plugin security: `ExecutePlayModeAsync`, `ExecuteRunModeAsync`, `ExecuteMultiplayerTestAsync` (1–8 clients, returns the value the server passes to `EndTest`), `AddPlayers`, `GetTestArgs`, `EndTest`, `LeaveTest` `[official]` | Scripted multi-client, staggered join, leave-during-trade tests |
| `VirtualInput` | From `UserInputService:CreateVirtualInput()` (check for `nil`); mouse, key, pointer, text; own UI only (CoreGui throws) `[official]` | Click-through tests of real buttons |
| `StudioDeviceSimulatorService` | Scriptable device, resolution, DPI, orientation `[official]` | Cross-device and rotation regression |
| Open Cloud Luau Execution | Headless, no physics, 5-minute limit | In-engine suites in CI against a place version |
| Coverage | `ScriptContext:EnableCoverage(instance)` and `GetCoverageStats()` (per-line and per-function hits), plugin or Open Cloud security only `[official]` | Finding untested branches in services |

Conflict: LihFolk's notes describe "Jest-Lua" set up with `run-in-roblox` and the `FFlagEnableLoadModule` flag. That matches the `jsdotlua/jest-lua` mirror, which is stale (last commit 2024-12). `Roblox/jest-roblox` documents two public routes, Studio and Open Cloud Luau Execution, and mentions `EnableLoadModule` only for Roblox's internal `roblox-cli` runner.

What to test first, by cost of the bug `[lihfolk]`: economy maths and price tables; drop odds; schema migrations; remote validators; config invariants; purchase granting; pure utilities. Do not automate first: layout and VFX feel, animation timing, physics outcomes, one-line glue.

Patterns:

- **Pure core, thin shell.** Logic takes inputs and returns outputs; services and Instances stay at the edge.
- **Inject the clock and the random source** (`now: number`, `rng: Random`). Every `task.wait` in a test is a slow, flaky test.
- **Fakes over mocks.** A `FakeStore` with `get` and `update` lets you test "two failures then success"; assert on resulting state, and use `jest.fn()` only where the call is the behaviour.
- **Table-driven cases**: one body, a row per bug report.
- **Validators get hostile rows**: `nil`, tables, negatives, `0/0`, `math.huge`, 1.5, a 10,000-character string.
- **Config invariants**: walk every item and collect offending ids into a list; `expect(bad).toEqual({})` prints them.
- **Migration fixtures**: one anonymised save per schema version ever shipped; run the chain and validate.
- **Odds tests**: tolerance of 4 standard deviations, `sqrt(p(1-p)/N)` each, with a seeded generator.

| p | N | 4-sigma tolerance |
|---|---|---|
| 0.33 | 20,000 | 0.013 |
| 0.01 | 100,000 | 0.0013 |
| 0.001 | 1,000,000 | 0.00013 |

A weighted pick that rolled "1 in 370" instead of "1 in 3" shipped in LihFolk's reference project; ten lines like these catch it `[lihfolk]`. Jest Roblox spec, saved as `Loot.spec.luau` (unexecuted sketch; `DevPackages` is where Wally puts dev-dependencies, adjust to your project):

```lua
--!strict
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local JestGlobals = require(ReplicatedStorage.DevPackages.JestGlobals)
local Loot = require(ReplicatedStorage.Shared.Loot)
local describe, it, expect = JestGlobals.describe, JestGlobals.it, JestGlobals.expect

describe("Loot.roll", function()
	it("gives the rare item about 1% of the time", function()
		local rng, hits, rolls = Random.new(42), 0, 100_000
		for _ = 1, rolls do
			if Loot.roll(rng, "StarterCrate") == "RareSword" then hits += 1 end
		end
		expect(math.abs(hits / rolls - 0.01) < 0.0013).toBe(true)
	end)
	it("has complete rows", function()
		local bad: { string } = {}
		for id, row in Loot.Tables do
			if row.weight <= 0 or row.item == nil then table.insert(bad, id) end
		end
		expect(bad).toEqual({})
	end)
end)
```

Multi-client protocol (manual or `ExecuteMultiplayerTestAsync`): two clients plus one late joiner; one client on the 3G preset; one leaves mid-trade and mid-purchase; one resets twice quickly; check that each client sees the other's state and that private state stays private. Streaming QA: a copy with `StreamOutBehavior = Opportunistic` and about a quarter of the live target radius; go far and come back, interact twice, join far away, teleport, die and respawn `[lihfolk]`. Dupe hunt: spam every grant, trade and drop path at 20 clicks a second with a rejoin in the middle.

Make UI testable: stable names (`Buy_Sword`), state exposed as attributes so tests wait on facts rather than timers, one short suite per flow.

## Pre-release regression checklist

- [ ] Output is clean in a solo play test and a 2-client test: zero errors, zero unexpected warnings.
- [ ] Static gate green (types, lint, format); unit suites green; in-engine smoke suite green on the release build.
- [ ] Join, first session, core loop, shop, purchase (test universe), save, leave, rejoin: values persist.
- [ ] Fast rejoin (under 3 s) ten times: no rollback, no dupe.
- [ ] Late joiner sees correct state; reset twice quickly; die during every ability.
- [ ] 4G and 3G presets: no soft-locks; UI never waits forever on the server.
- [ ] Streaming QA route passes; teleports request the area first.
- [ ] Phone, tablet and gamepad pass on the Device Simulator and one real 2–4 GB Android phone.
- [ ] Respawn soak (100×): instance and heap growth per cycle near zero.
- [ ] Server shutdown test: every online profile saved.
- [ ] Kill switches tested in both states; a rollback version noted.
- [ ] Debug remotes gated; injected delays, debug seeds and verbose log levels removed.
- [ ] After publishing: "new errors since version" checked at 1 hour and 24 hours; crash and memory charts compared with the previous version.

## Review gate

- [ ] Every bug fix has a written repro with a rate, a one-sentence cause, and a run count at least twice the original failure count.
- [ ] No fix consists of a wait, a longer timeout or a silent `pcall`.
- [ ] Subscribe-then-iterate with a guard on players, characters, tags and children; state re-checked after every yield.
- [ ] Every connection, thread and per-player entry has an owner that cleans it; respawn soak is flat.
- [ ] Every web-service call is protected and its failure branch does something; retries are capped, jittered and single-layer.
- [ ] Log messages are stable strings; server tag and version on every event; no personal data.
- [ ] Capture kit exists: server tag, state dumps, off-server logs, kill switches, gated admin join.
- [ ] Economy, odds, migrations and validators are under automated tests; the proof level of each change is stated.
- [ ] Release checklist run; first-hour triage owner named.

## Sources

Accessed 2026-11-11. `Roblox/creator-docs` at commit 7cbffff (2026-11-10).

- https://github.com/Roblox/creator-docs: `content/en-us/studio/{debugging,developer-console,testing-modes,network-simulator}.md`, `studio/optimization/{memory-usage,scriptprofiler}.md`, `performance-optimization/{scene-analysis,microprofiler/index}.md`, `production/analytics/{error-report,alerts}.md`, `cloud/guides/error-reporting/index.md`, `scripting/{transparent-batching,events/deferred}.md`, `luau/native-code-gen.md`, `reference/engine/classes/{LogService,Logger,ScriptContext,StudioTestService,VirtualInput,StudioDeviceSimulatorService,NetworkSettings,Workspace,Stats,TeleportService,TeleportOptions,MarketplaceService,HttpService,Instance}.yaml`, `reference/engine/libraries/debug.yaml` (read)
- https://create.roblox.com/docs/cloud/reference/features/luau-execution.md (read)
- https://github.com/luau-lang/site: `src/content/docs/guides/sandbox.md`, `getting-started/compatibility.md` (read; `collectgarbage`, no `__gc`)
- https://github.com/Roblox/jest-roblox at 3.21.0 (2026-11-09): `README.md`, `CHANGELOG.md`, `docs/docs/{GettingStarted,Configuration,UpgradingToJest3}.md` (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-debugging/SKILL.md`; `LihFolk Vault V2/SYMPTOMS.md`; `23 Debugging Deep Dives/{The Debugging Method - Reproduce Isolate Bisect, Debugging Live Servers, Debugging Race Conditions and Yield Order, Reading Luau Errors and Stack Traces}.md`; `12 Performance Testing and Debugging/{Hunting Memory Leaks Step by Step, Debugger Breakpoints and Logging, Developer Console and Stats, Crash and Error Telemetry, Testing Strategies and Frameworks, Automated Testing with TestEZ and Jest-Lua, StreamingEnabled QA - Forcing Stream-Out to Catch Nil Bugs, UI Automation with VirtualInput and StudioTestService}.md`; `35 Advanced Luau/Luau Garbage Collection and the Memory Model.md` (read)
- Staff posts (read): structured logging full release, 2026-06-04, https://devforum.roblox.com/t/4668415 · StudioTestService, 2025-12-04, https://devforum.roblox.com/t/4116257 · Studio testing APIs, 2026-05-28, https://devforum.roblox.com/t/4657854 · Luau VM memory tools and their known issues, 2024-01-25, https://devforum.roblox.com/t/2808362 · staff replies on `TeleportAsync` failure points, 2025-01, https://devforum.roblox.com/t/3373497
- Community threads (read): https://devforum.roblox.com/t/3502516 (developers reporting `NotProcessedYet` receipts not replayed on rejoin; no staff answer) · https://devforum.roblox.com/t/750912 and https://devforum.roblox.com/t/1352119 (animation replication: Animator placement, asset owner) · https://devforum.roblox.com/t/533353 (Studio script-timeout setting) · https://devforum.roblox.com/t/451624 (works in Studio, not in game)
- Not re-read this pass (search summaries from the first draft): https://devforum.roblox.com/t/4861695 (Network Simulator beta; the docs page was read instead), https://devforum.roblox.com/t/90082 (connections leaking instances), https://devforum.roblox.com/t/4504347 (throttle error names; owned by `data-and-purchases.md`), https://github.com/dinoderek/rob (`lune run test` layout).
- No evidence found: an official statement of the script-timeout default on live servers; an official animation track limit figure; a published Studio "Are Owners Shown" reference page.
