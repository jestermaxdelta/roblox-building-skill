# Luau mastery: first script to expert idioms

What this is: a Luau language reference in three tiers (beginner, intermediate, expert) plus game-math essentials, a deprecated-to-modern API table and style conventions. Open it when writing or reviewing any script, when a developer asks "how do I do X in Luau", or when modernising an old codebase. Language facts were checked on 2026-11-10 against `Roblox/creator-docs` (commit ccc2b01), `luau-lang/site` (luau.org source), `luau-lang/rfcs` and `luau-lang/luau` (tag 0.746 era). Snippets are unexecuted sketches. Tags: `[official]` Roblox docs or luau.org, `[community]`, `[VS]` version-sensitive, `[house]`, `[lihfolk]` adapted from LihFolk Vault V2.

It extends, and does not repeat: `engineering-architecture.md` (project layout, loader, naming, toolchain), `architecture-patterns-luau.md` (Signal, pool, FSM and other pattern sketches), `performance.md` (profiling, `--!native` limits, Parallel Luau basics), `debugging-and-testing.md` (errors, retries, tests).

## Contents

Start here by level · Beginner: the first week · Intermediate: modules, types, objects, scheduling, idioms · Expert: type system status, compiler and VM, memory, native code, parallelism, limits · Game math essentials · Deprecated → modern · Style conventions · Level-up table · Review gate · Sources

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | Learn where each script kind runs. Write `local` on everything. Use `task.wait`, never `wait`. Reach instances with `game:GetService` and `WaitForChild`. Keep Output open. Read the first-week mistakes table | Metatables, generics, coroutines, optimisation |
| Intermediate | Put all logic in ModuleScripts under `--!strict`. Type the boundaries (`unknown` in, precise types out). Prefer plain modules; use a class only for many instances with a lifetime. Give every connection and thread an owner. Learn `task.spawn` vs `task.defer` | Type functions, `buffer`, native code, Actors |
| Expert | Know what allocates and what the compiler can inline. Benchmark at the live optimisation level on the target device. Use `buffer`, `@native` and Actors only on measured hot paths. Track feature status: the solver, `const`, type functions | Nothing: but measure first |

## Beginner: the first week

**Terms.** An *Instance* is any object in the game tree (Part, Folder, Player, script). The *server* is the one authoritative computer; each *client* is a player's device. To *yield* is to pause a script until something happens. Full model: `engineering-architecture.md`.

Where code runs:

| Script kind | Runs on | Put it in | Use for |
|---|---|---|---|
| `Script` | Server | `ServerScriptService` | Rules, data, anything players must not fake |
| `LocalScript` | One player's client | `StarterPlayerScripts`, `StarterCharacterScripts`, `StarterGui`, `ReplicatedFirst` (it does nothing in `Workspace` or `ReplicatedStorage`) | Input, camera, UI |
| `Script` with `RunContext = Client` | Client | `ReplicatedStorage` (not a Starter container: it would run twice) | A single client entry point |
| `ModuleScript` | Whichever side calls `require` on it | `ReplicatedStorage` (shared), `ServerScriptService` or `ServerStorage` (server only) | All reusable code |

The language in one screen (unexecuted sketch):

```lua
--!strict
local Players = game:GetService("Players") -- always reach services this way
local MAX_COINS = 100 -- a constant by convention; `const MAX_COINS = 100` also exists [VS]
local coins: { [Player]: number } = {} -- dictionary: any key to a value
local greetings = { "Hi", "Hello", "Hey" } -- array: indices start at 1, #greetings == 3

local function addCoins(player: Player, amount: number): number
	local total = math.min((coins[player] or 0) + amount, MAX_COINS) -- `or` supplies a default for nil
	coins[player] = total
	return total
end

local function onPlayerAdded(player: Player)
	local greeting = greetings[math.random(1, #greetings)]
	print(`{greeting}, {player.Name}! You have {addCoins(player, 10)} coins`) -- backtick strings interpolate
end

Players.PlayerAdded:Connect(onPlayerAdded) -- an event calls your function later
for _, player in Players:GetPlayers() do task.spawn(onPlayerAdded, player) end -- players already here
Players.PlayerRemoving:Connect(function(player) coins[player] = nil end) -- assigning nil removes the key
```

Facts that differ from other languages: only `nil` and `false` are falsy (`0` and `""` are truthy); not-equal is `~=`; all numbers are 64-bit floats, exact as integers up to 2^53; `#s` counts bytes; `a // b` is floor division; `x += 1` works but `x++` does not; `continue` exists; `if c then a else b` is also an expression; comparing two tables with `==` compares identity, not contents.

Events: `signal:Connect(fn)` returns a connection (call `:Disconnect()` when done); `signal:Once(fn)` runs one time; `signal:Wait()` yields until the next fire and misses anything fired before it started waiting.

The `task` library `[official]`:

| Call | Does | Typical use |
|---|---|---|
| `task.wait(seconds?)` | Yields; resumes on the first `Heartbeat` after the time; returns the real elapsed time. Never shorter than one frame (about 0.017 s at 60 FPS) | Timers, pacing loops |
| `task.spawn(fn, ...)` | Runs `fn` **now** until it first yields, then your code continues | Start background work |
| `task.defer(fn, ...)` | Runs `fn` after the current code finishes, later this frame | Avoid re-entrancy; batch changes |
| `task.delay(seconds, fn, ...)` | Runs `fn` on the first `Heartbeat` after the delay | One-shot timers |
| `task.cancel(thread)` | Stops a thread from ever resuming | Cancel timers and loops on cleanup |

Instance tree basics: `parent:FindFirstChild("Name")` returns the child or `nil` (check it); `parent:WaitForChild("Name", 10)` yields until it exists or the timeout passes (use it on the client for anything replicated); `parent.Name` errors if the child is missing. Create with `Instance.new("Folder")`, set properties, set `Parent` **last**. Remove with `:Destroy()`, which also disconnects its events. Store small per-instance data in attributes (`SetAttribute`, `GetAttribute`) and mark behaviour with tags (`AddTag`, `CollectionService:GetTagged`). `instance:IsA("BasePart")` tests the class.

First-week mistakes:

| Mistake | What happens | Do instead |
|---|---|---|
| LocalScript placed in `Workspace` or `ServerScriptService` | It never runs | Use the table above |
| Changing coins, health or `leaderstats` from a LocalScript | Only that player sees it; the server never knew | Fire a RemoteEvent with the *request*; the server decides and changes the value |
| A remote like `GiveCoins:FireServer(1000)` | Any exploiter fires it with any number | Send intent ("I clicked the chest"); the server computes the reward (`networking-and-security.md`) |
| `while true do` with no `task.wait()` | Freeze or "Script timeout" | Yield in every loop; prefer events to loops |
| `wait()`, `spawn()`, `delay()` | Deprecated, throttled, imprecise `[official]` | `task.wait`, `task.spawn`, `task.delay` |
| Forgetting `local` | A global: slower, shared by accident, hides typos | `local` always; `--!strict` reports unknown globals |
| Calling a `local function` above the line that defines it | "attempt to call a nil value" on that path only | Define before use, or forward-declare `local f` then assign `f = function` |
| `obj.Method()` instead of `obj:Method()` | `self` is missing; odd errors | `:` to call methods, `.` for plain functions and properties |
| `if count then` to mean "non-zero" | Always true once set, since `0` is truthy | `if count > 0 then` |
| `"Score: " .. score` where `score` is nil | "attempt to concatenate nil" | Interpolate and default: `` `Score: {score or 0}` `` |
| Connecting an event inside another event or loop | Handlers pile up: the action fires 2, 3, 4… times | Connect once; disconnect what you connect |
| `Touched` with no debounce | Fires per body part, many times a second | Mark the object taken first; map the part to a player |
| `PlayerAdded` only | The first player in Studio is skipped | Also loop `Players:GetPlayers()` |
| DataStore or other web calls without `pcall` | One failed request breaks the script | Wrap, and decide what failure does (`data-and-purchases.md`) |
| Tuning values during Play | Changes vanish on Stop | Stop, then edit; or copy values out first |
| `a == b` on computed decimals | `0.1 + 0.2 ~= 0.3` | Compare with a tolerance, or use integers |

## Intermediate

### ModuleScripts

- A module runs once per Luau VM and `require` returns the same value afterwards. Server and each client are separate VMs with separate copies: a "shared" module shares code, never state. Each Actor is another VM.
- Return one table (or function). Top level builds tables and functions only: no yields, no calls into other systems, or every requirer stalls and cycles deadlock.
- No require cycles. Move shared pieces to a third module or resolve lazily inside a function.
- Server-only modules live in server containers; a module in `ReplicatedStorage` is readable by every exploiter.
- Editing a module during a command-bar session has no effect until it is re-required from a fresh clone (the result is cached) `[lihfolk]`.

### Types under `--!strict`

Modes `[official]`: `--!strict` checks everything from inferred and annotated types; `--!nonstrict` checks only what you annotate; `--!nocheck` checks nothing. `Workspace.LuauTypeCheckMode` sets the place default `[VS]`. Types are erased at runtime: an annotation on remote or DataStore input is a claim, not a check.

| Need | Write |
|---|---|
| Optional | `name: string?` |
| One of several | `"idle" \| "run" \| "jump"` (singleton strings as enums) |
| Record | `type Item = { id: string, price: number, tags: { string } }` |
| Map | `{ [Player]: number }` |
| Function | `(player: Player, amount: number) -> boolean` |
| Generic | `function first<T>(list: { T }): T?` |
| Untrusted input | `value: unknown`, then narrow |
| Export | `export type Item = ...`, used as `Module.Item` |
| Type of a value | `typeof(defaults)` |
| Cast after a runtime check | `value :: number` |

Narrowing (the checker follows these): `if x then`, `type(x) == "number"`, `typeof(x) == "Vector3"`, `x:IsA("BasePart")`, `assert(x)`, and comparing a tagged union's `kind` field inline. It does not follow narrowing hidden inside a helper function `[lihfolk]`. `any` switches checking off and spreads; `unknown` forces a check before use.

Tagged union with an exhaustiveness guard and a boundary validator (unexecuted sketch):

```lua
--!strict
type Effect = { kind: "damage", amount: number } | { kind: "heal", amount: number } | { kind: "stun", seconds: number }

local function describe(effect: Effect): string
	if effect.kind == "damage" then return `-{effect.amount} HP`
	elseif effect.kind == "heal" then return `+{effect.amount} HP`
	elseif effect.kind == "stun" then return `stunned {effect.seconds}s`
	else
		local unreachable: never = effect -- add a fourth kind and this line becomes a type error
		return unreachable
	end
end

local function readAmount(value: unknown): number? -- remote arguments arrive as unknown
	if type(value) ~= "number" or not math.isfinite(value) then return nil end -- rejects NaN and infinity
	return math.clamp(value, 0, 1000)
end
```

### Objects: metatables or plain modules

A *metatable* is a table that changes how another table behaves; `__index` makes missing keys fall through to a shared method table, which is how classes are built.

| Situation | Use |
|---|---|
| One of it per server or client (shop, data, combat rules) | Plain module with functions and private locals |
| Many instances with state and a lifetime (enemy, projectile, cooldown, UI card) | Class: `setmetatable` plus `Destroy` |
| Thousands of similar things updated per frame | Arrays of data plus one loop, or an ECS; not one object each |
| Data that only varies by numbers | Frozen config tables, no behaviour |

Typed class (unexecuted sketch; the clock is passed in so tests need no waiting):

```lua
--!strict
local Cooldown = {}
Cooldown.__index = Cooldown
type Fields = { duration: number, readyAt: number }
export type Cooldown = typeof(setmetatable({} :: Fields, Cooldown))

function Cooldown.new(duration: number): Cooldown
	return setmetatable({ duration = duration, readyAt = 0 }, Cooldown) -- one literal with every field
end

function Cooldown.tryUse(self: Cooldown, now: number): boolean
	if now < self.readyAt then return false end
	self.readyAt = now + self.duration
	return true
end

return Cooldown
```

Pitfalls: metatables do not survive RemoteEvents, BindableEvents or DataStores (send plain data and rebuild); `__index` as a function is slower than `__index` as a table; inheritance deeper than one level costs lookups and readers; an object without `Destroy` leaks whatever it connected; inside `__index` or `__newindex` use `rawget`/`rawset` or it recurses.

### Closures

A *closure* is a function that keeps access to the local variables around it (its *upvalues*). It captures the **variable**, not a snapshot: change the variable later and the function sees the change. A `for` loop variable is fresh per iteration, so handlers created in a loop each see their own value; the "every button does the same thing" bug comes from capturing one variable declared **outside** the loop. A closure keeps its upvalues alive, so a connected handler keeps every instance it mentions alive until it is disconnected.

### Coroutines and the scheduler

One thread runs at a time per VM and nothing pre-empts it: code between two yields is atomic, and a loop that never yields freezes everything. Rules:

- `task.spawn(fn, a, b)` instead of `task.spawn(function() fn(a, b) end)`: no closure.
- Errors in spawned threads print to Output but do not reach the spawner. `coroutine.resume` returns `false, err` instead of throwing: ignoring its result hides errors.
- Do not `coroutine.resume` a thread the engine yielded (inside `task.wait`, `WaitForChild`, a web call): it will be resumed twice. Resume only threads you yielded with `coroutine.yield`, using `task.spawn(thread, ...)` `[lihfolk]`.
- Every loop thread has an exit condition or is stored and `task.cancel`led by its owner.
- `coroutine.finally(co, callback)` runs `callback("finished" | "error" | "cancelled", ...)` when the coroutine ends `[official][VS]`: the hook for structured cleanup.
- You cannot yield inside a metamethod, a `table.sort` comparator or a `string.gsub` callback.
- Signals, deferred-event pitfalls and Trove ownership: `engineering-architecture.md`; a Signal sketch: `architecture-patterns-luau.md`.

What cleanup does and does not do:

| Action | Disconnects | Leaves alive |
|---|---|---|
| `instance:Destroy()` | Every connection on it and its descendants; locks `Parent` | Your variables and tables still pointing at it; connections you made on **other** objects |
| `instance.Parent = nil` | Nothing | Everything: fine for pooling, a leak otherwise |
| `connection:Disconnect()` | That handler, including queued deferred calls | The handler's upvalues until the function itself is unreferenced |
| `task.cancel(thread)` | That thread | Whatever it already created |
| `trove:Destroy()` | Everything added to it | Things you forgot to add |

### String and table idioms

| Task | Idiom | Note |
|---|---|---|
| Build text | `` `{name} has {coins} coins` `` | Interpolation; `string.format("%.2f", x)`, `"%03d"`, `"%x"` for formats |
| Join many pieces | `table.concat(parts, ", ")` | `s = s .. x` in a loop copies the whole string each time |
| Split | `string.split(s, ",")` | |
| Match | `string.match(s, "^(%a+)_(%d+)$")` | Lua patterns, not regex: `%d %a %w %s %p`, `-` is lazy, no alternation |
| Count characters | `utf8.len(s)` | `#s` is bytes; player names can be multi-byte |
| Presized array | `table.create(n)` then `t[i] = v` | Fastest when `n` is known `[official]` |
| Append | `table.insert(t, v)` | Fastest when size is unknown `[official]` |
| Remove from the middle, order irrelevant | `t[i] = t[#t]; t[#t] = nil` | `table.remove(t, i)` shifts everything after `i` |
| Queue | `head`/`tail` indices | `table.remove(t, 1)` is O(n) per pop |
| Find | `table.find(t, v)` | Linear; use a set for frequent lookups |
| Set | `seen[key] = true` | Count needs a loop: `#` is for arrays only |
| Copy | `table.clone(t)` | Shallow |
| Lock config | `table.freeze(t)` | Shallow; writes then error |
| Reuse a scratch table | `table.clear(t)` | Keeps its capacity |
| Sort | `table.sort(t, function(a, b) return a.score > b.score end)` | Comparator must return `false` for equal items or it raises "invalid order function"; not stable |
| Iterate | `for key, value in t do` | `ipairs` only when you want to stop at the first `nil` |

Arrays with holes: `#t` is unreliable once a middle element is `nil`. A cleanup list built with `ipairs` over values that may be `nil` silently skips the rest `[lihfolk]`.

Error handling (`pcall`, `xpcall`, result types, retries with backoff) is in `debugging-and-testing.md`.

## Expert

### Language and type-system status `[VS]`

Re-check each row before relying on it; "RFC only" means do not write it yet.

| Feature | Status on 2026-11-10 | Guidance |
|---|---|---|
| New type solver | General release announced on the DevForum, with the beta toggle scheduled for removal on 7 January 2026 `[community: search summary]`. `Workspace.UseNewLuauTypeSolver` (a `RolloutState`, set in Studio, not scriptable) selects it per place `[official]`. Fixes still land in release notes, and Roblox acknowledged slower analysis and higher Studio memory in some cases | Use it for new code. Keep type shapes simple; test surprising errors against the other solver before rewriting code |
| `const` bindings | Documented by Roblox and luau.org: `const X = 1`, `const function f()`; reassignment and `+=` are errors; the binding is immutable, the value is not (`table.freeze` for that); contextual keyword `[official]` | Fine in Studio. In a Rojo project first confirm your StyLua, Selene and luau-lsp versions parse it (not verified here) |
| `type function` and the `types` library | Implemented (RFC); new solver only. Environment: `types`, `math`, `table`, `string`, `bit32`, `utf8`, `buffer` and a few globals; no runtime values, no Roblox APIs `[official: luau.org]` | Library-level types only (`Readonly<T>`, `Pick<T, K>`). Each use re-runs analysis; errors surface at every use site |
| `keyof`, `rawkeyof`, `index`, `rawget`, `setmetatable`/`getmetatable` type functions | Implemented (RFCs) | `keyof<typeof(Config)>` for "one of the config keys" |
| Explicit instantiation `f<<T>>(...)` | Implemented (RFC); documented on luau.org | Useful for `makeList<<number>>()`; confirm in your Studio version |
| `read` / `write` property modifiers | In the luau.org grammar (`{ read name: string }`); new solver | Read-only parameters accept subtypes: fixes "`{Sword}` is not `{Item}`" |
| Default type parameters, singleton types, `never`, `unknown`, typed variadics | Implemented | Everyday tools |
| `@native`, `@deprecated`, `@[deprecated { use = "newApi()", reason = "..." }]` | luau.org attribute reference; attributes are not user-definable | Mark old internal APIs so the linter warns callers |
| `--!optimize 0\|1\|2` | Level 1 is the default in Studio testing, level 2 in live games `[official]` | Leave it alone in game code; use `--!optimize 2` in benchmark scripts |
| `vector` library, `math.lerp`, `math.map`, `math.isnan`/`isinf`/`isfinite`, `math.tau`, `buffer.readbits`/`writebits`, `vector.lerp` | In the Roblox library reference | Use freely |
| `coroutine.finally` | In the Roblox library reference | Structured cleanup for threads |
| `class` syntax, `export` for values, 64-bit `integer` type, cyclic requires | RFC only (no "Implemented" status in `luau-lang/rfcs`) | Do not write; do not promise |
| Bounded generics (`<T: Instance>`), `__gc` finalizers, ephemeron tables | Not in Luau | Take a capability function instead of a bound; clean up explicitly |

Conflict: `engineering-architecture.md` says the new solver "is still rolling out". The DevForum general-release post supersedes that; its practical advice (prefer simple type shapes) still stands because fixes continue.

Type-system behaviour that surprises experts `[lihfolk]`:

- Inference flows from **arguments**, not from where the result goes. `local n: number = first(names)` does not make `T` a number. Annotate the argument, or instantiate explicitly.
- An empty literal gives the checker nothing: `local list = {}` becomes too wide or too narrow later. Write `local list: { Item } = {}`.
- Mutable containers are invariant: a function taking `{ Item }` rejects `{ Sword }` because it could insert a plain `Item`. Make the parameter generic (`<T>(items: { T })`) or read-only.
- One discriminant name everywhere (`kind`), string singletons, compared inline.
- Generic classes: declare `export type RingBuffer<T> = { push: (self: RingBuffer<T>, value: T) -> (), ... }` and cast once in the constructor; `typeof(setmetatable(...))` captures one concrete type.
- Budget cleverness: full generics in shared libraries (signals, pools, codecs, validators); `unknown` plus validators at the network boundary; plain annotations and tagged unions in game systems. If teammates write `:: any` to get past your types, simplify.

### What the compiler and VM do for you `[official: luau.org]`

| Mechanism | Consequence |
|---|---|
| Imports: global chains such as `math.floor` resolve at load | `local floor = math.floor` buys nothing |
| Fastcalls: builtins called directly skip the call frame (`math.*` except `noise` and `random`, `bit32.*`, `type`, `typeof`, `rawget`, `tonumber`, some `string` and `table`) | `string.byte(s, i)` is fast; the method form `s:byte(i)` is not |
| Inline caching on `t.field`, fast method calls on `obj:Method()` | Keep fields directly on the object; do not cache methods in locals; `__index` should be a table |
| Table templates | Build an object in **one literal with every field**; keep one shape per kind of object |
| Specialised iteration | `for k, v in t` equals `pairs`/`ipairs` in speed; `for i = 1, #t` is slightly slower |
| `#t` is cached | Effectively constant time on real arrays |
| Upvalues that are never reassigned are captured by value; closures with only such upvalues may be cached | A reassigned captured variable costs an allocation; a cached closure can share identity, so do not use fresh closures as table keys |
| Inlining and loop unrolling at optimisation level 2 only: `local function`, non-recursive, small; loops with constant bounds | Studio play tests run level 1 and live servers level 2, so Studio timings understate live speed and exclude inlining |
| `getfenv`, `setfenv`, `loadstring` mark the environment impure | Imports, fastcalls and inlining are lost for that script. Never use them |

### Memory model and GC

| Value | Allocates? |
|---|---|
| `nil`, `boolean`, `number`, `Vector3` (the native `vector`) | No: stored inline. Vector maths in a hot loop creates no garbage `[official]` |
| `string` | Yes, unless an identical string already exists; every `..` intermediate is garbage |
| `table`, `buffer` | Yes |
| `function` | Usually (see closure caching) |
| `thread` | Yes, with its own stack; a suspended thread keeps everything on that stack alive |
| `CFrame`, `Color3`, `UDim2`, connections, Instance references | Yes: a userdata wrapper per result. Do the maths in `Vector3` and build the `CFrame` once `[lihfolk]` |

- The collector is incremental (mark, a short atomic step, paged sweep), not generational. Allocation pays for "assists" inside your script, so churn shows up in your own timings `[official]`.
- Heap size is a sawtooth: the troughs are live data, the teeth are garbage. Rising troughs mean a leak; tall fast teeth mean churn.
- No finalizers and no forced collection: `collectgarbage` only supports `"count"`; `gcinfo()` reads the heap in KB. Cleanup is always an explicit call.
- No ephemerons: in a weak-keyed table, a value that references its own key keeps the entry forever. Adding `s` to `__mode` lets a weak table shrink during collection, at the risk of missed keys if it resizes mid-iteration `[official: luau.org]`.
- Capacity is sticky: clearing a table that once held 100,000 entries keeps the memory. Reuse scratch tables with `table.clear`; drop one-off giants by assigning a new table.
- Measure allocation as KB per iteration over thousands of iterations, comparing two versions in one run; a single before-and-after reading can even go negative.

### `buffer`, native code and parallelism

`buffer` is a fixed-size block of bytes with typed little-endian reads and writes (`readu8` … `readf64`, `readstring`, `readbits`, `readvectorf32x3` and matching writes) `[official]`. Use it for compact network payloads, binary save chunks and large numeric grids. An `f32` round-trip loses precision against a Luau number: compare with a tolerance or write `f64`. A buffer sent through a remote arrives as a copy, and one buffer cannot be used from several Actors `[official]`. Unexecuted sketch, 14 bytes for a position and heading:

```lua
--!strict
local TAU = 2 * math.pi
local function packMove(position: Vector3, yaw: number): buffer
	local b = buffer.create(14)
	buffer.writef32(b, 0, position.X)
	buffer.writef32(b, 4, position.Y)
	buffer.writef32(b, 8, position.Z)
	buffer.writeu16(b, 12, math.round((yaw % TAU) / TAU * 65535)) -- heading in 16 bits
	return b
end
```

Native code generation (`--!native`, `@native`): server scripts and Android clients only; identical behaviour, faster numeric code `[official]`. Rules beyond `performance.md`: annotate parameters, above all `Vector3`, or the compiler assumes tables and adds checks; a breakpoint disables native execution for that function; `@native` does not apply to inner functions; calling a typed function with the wrong types forces fallbacks; total native code is capped per game and each script costs start-up time and memory, so never add it "just in case"; `debug.dumpcodesize()` in the Server view shows sizes; the Script Profiler marks `<native>`. Limits: 64K instructions per block, 32K blocks per function, 1M instructions per module. LihFolk describes native code as server-only; the docs now include Android clients.

Parallel Luau beyond the basics in `performance.md`:

- Every Actor is its own VM: a module required by 64 Actors runs 64 times and holds 64 copies of its data; a "global" registry module is per Actor. This is the most common design error `[lihfolk]`.
- Messages are copied; send ids and small parameters. `SharedTable` avoids the copy but each access is synchronised: a staff reply put it near 10× slower than a table `[community]`. Read what you need into locals at the start of a job and write results once at the end.
- `SharedTable.increment` is atomic and much faster than `update`; `SharedTable.update(st, key, fn)` may call `fn` several times under contention, so `fn` must be pure; a plain read-then-write is a race `[official]`.
- Shape every system as read (parallel), compute (parallel), write (serial, one place). If the serial write phase grows, parallelism is a net loss: measure in the MicroProfiler.

### Performance idioms with measured rules

Cost per frame = cost per item × items × times per second ÷ frame rate. Frequency and count dominate: 22 µs per scripted rig × 30 rigs every frame is 0.66 ms; a 1 µs target check over 200 enemies × 20 players every frame is 4 ms, and the same check at 4 Hz is 0.27 ms `[lihfolk: measured in its reference project]`.

| Rule | Why | Source |
|---|---|---|
| Run work on change or at 4–10 Hz, staggered, not per frame | The formula above | `[lihfolk]` |
| One loop over a registry, not one connection or thread per object | A dispatch, a resume and a closure per object per frame | `[official]` docs problem lists |
| No tables, closures, threads or strings created per frame per object | GC assists land in your frame | luau.org |
| `pcall(fn, a, b)` and `task.spawn(fn, a, b)`, never a wrapper closure, in hot paths | One allocation less per call | luau.org |
| Read an Instance property once into a local; mirror attributes into a Lua table on change | Every property access crosses into the engine | `[lihfolk]` rule of thumb: measure |
| Write a property only when the value changed | Writes can trigger replication and physics work | `[lihfolk]` |
| `workspace:BulkMoveTo(parts, cframes, mode)` for many parts | One engine call | `performance.md` |
| Squared distances: `d:Dot(d) < r * r` | No square root, no allocation | `[community]` |
| Slice long jobs by elapsed time (about 5 ms), not by item count | Item cost varies | `performance.md` |
| Benchmark with warm-up, many runs, the median, results consumed, heap delta reported, `--!optimize 2`, and no breakpoints | Each omission is a known way benchmarks lie | `[lihfolk]`, `[official]` |
| Confirm every win in the MicroProfiler on the target device | A 3× win on 0.02 ms is worth nothing | `[house]` |

### Sandboxing and hard limits

| Limit | Detail |
|---|---|
| No `io`; `os` has only `clock`, `date`, `difftime`, `time` | `[official: luau.org]` |
| `loadstring` | Off unless `ServerScriptService.LoadStringEnabled`; never available on clients; cannot load bytecode. Keep it off |
| Security levels and capabilities | Game scripts cannot call plugin or core APIs; the error names a missing capability |
| Globals | Each script has its own; `_G` and `shared` are shared per side: prefer modules |
| No pre-emption | A thread runs until it yields; watchdog details in `debugging-and-testing.md` |
| 200 active locals per function (the main chunk counts), 255 registers, 200 upvalues per closure | Compile errors "Out of local registers…", "Out of registers…", "Out of upvalue registers…" (texts verified in `luau-lang/luau`; values `[lihfolk][VS]`). Fix by splitting into modules, grouping values in a table, or scoping with `do … end` |
| Script `Source` about 200,000 characters `[lihfolk][VS]` | Split generated modules early |
| Integers exact to 2^53 | Above that `x + 1 == x`; idle-game currencies need a mantissa and exponent pair (`economy-and-progression.md`) |

## Game math essentials

**CFrame** (a position plus a rotation; immutable). `LookVector` is the **-Z** axis, `RightVector` +X, `UpVector` +Y.

| Need | Write | Trap |
|---|---|---|
| Face a point | `CFrame.lookAt(from, target)` | Degenerate when the direction is parallel to the up vector: pass another `up` |
| Move in its own space | `cf * CFrame.new(0, 0, -5)` | `A * B` means "B relative to A"; order matters |
| Move in world space | `cf + Vector3.new(0, 5, 0)` | |
| Rotate | `cf * CFrame.Angles(0, math.rad(90), 0)` | Radians. `Angles` applies X, Y, Z; `fromOrientation` uses Y, X, Z like the `Orientation` property |
| World to local | `a:ToObjectSpace(b)`, `a:PointToObjectSpace(p)`, `a:VectorToObjectSpace(v)` | Vectors ignore position |
| Keep a fixed offset | Store `offset = parent.CFrame:ToObjectSpace(child.CFrame)` once; each frame `child.CFrame = parent.CFrame * offset` | The same identity as weld `C0`/`C1` |
| Blend two frames | `a:Lerp(b, t)` | Position linearly, rotation along the shortest arc |
| Move a model | `model:PivotTo(cf)` | Supersedes `SetPrimaryPartCFrame` |

Keep your own scalar yaw and pitch for cameras; reading Euler angles back from a CFrame flips near ±90° pitch.

**Vectors.** `a:Dot(b)` is `|a||b|cos θ`. In front of me: `look:Dot(toTarget) > 0`. Inside a view cone: `look:Dot(toTarget.Unit) > math.cos(math.rad(halfAngle))`. Left or right: the sign of `look:Cross(toTarget).Y` (verify the sign once in your scene). Project onto a direction: `dir * v:Dot(dir)` with `dir` unit length. `.Unit` of a zero vector is NaN, and one NaN in a CFrame makes a part or the camera vanish: guard with `if v.Magnitude > 1e-4`.

**Lerp and smoothing.** `math.lerp(a, b, t)` and `math.map(x, inMin, inMax, outMin, outMax)` do not clamp: clamp `t` unless you want extrapolation (unclamped remaps are the "damage went negative at long range" bug `[lihfolk]`). `current:Lerp(target, 0.1)` per frame depends on frame rate; use `alpha = 1 - math.exp(-speed * dt)`.

**Springs** feel better than tweens for anything the player interrupts. Explicit integration explodes on long frames: a critically damped 4 Hz spring is unstable when one step exceeds about 0.08 s, a bouncy one (damping 0.5) at about 0.04 s, which is a 25 FPS phone `[lihfolk]`. Clamp `dt`, sub-step, reset on non-finite values (unexecuted sketch):

```lua
--!strict
local function stepSpring(pos: number, vel: number, target: number, hz: number, damping: number, dt: number): (number, number)
	local w = 2 * math.pi * hz
	local remaining = math.min(dt, 0.1) -- a hitch is not motion
	while remaining > 1e-6 do
		local h = math.min(remaining, 1 / 120) -- fixed sub-steps keep w * h small
		vel += (-2 * damping * w * vel - w * w * (pos - target)) * h -- velocity first: semi-implicit
		pos += vel * h
		remaining -= h
	end
	if not (math.isfinite(pos) and math.isfinite(vel)) then return target, 0 end
	return pos, vel
end
```

**Easing.** An easing curve is a shape applied to `t`. `TweenService:GetValue(alpha, style, direction)` samples the engine's curves for your own loops (one loop writing 300 CFrames instead of 300 Tweens). Responses to input ease **Out** (fast start); In reads as input lag; two InOut moves chained stop visibly in the middle. `Back` Out overshoots by about 10% of the distance at about 58% of the duration: budget it on long moves and check hinges for clipping `[lihfolk]`. Effects such as shake and FOV kicks are envelopes with an explicit end time that reach exactly zero; sum them, then cap.

**Random.** `Random.new(seed)` per system (loot, spawns, cosmetics) so one system cannot shift another's sequence and bugs replay from a logged seed. `NextInteger(min, max)` is inclusive; `NextNumber()` is 0 to 1; `Shuffle(t)` shuffles in place; `NextUnitVector()` gives a direction `[official]`. Anything of value rolls on the server. Weighted choice (unexecuted sketch):

```lua
--!strict
local function weightedPick<T>(rng: Random, entries: { { item: T, weight: number } }): T
	local total = 0
	for _, entry in entries do total += entry.weight end
	local roll = rng:NextNumber() * total
	for _, entry in entries do
		roll -= entry.weight
		if roll < 0 then return entry.item end
	end
	return entries[#entries].item -- floating-point edge
end
```

Displayed odds must come from the same flattened table the server rolls (`monetization-and-policy.md`); the statistical test is in `debugging-and-testing.md`.

**Noise.** `math.noise(x, y, z)` is Perlin noise, usually within -1 to 1 but sometimes outside: clamp if the range matters `[official]`. It returns 0 at integer coordinates, so scale inputs (`x * 0.05`) and add a per-seed offset. Layer octaves for natural variation: sum `math.noise(x * f, z * f) * a`, doubling `f` and halving `a`, three to five times.

## Deprecated → modern

"Deprecated" rows are marked so in the engine reference at the commit above; "superseded" means the old API still works and the new one is the documented choice. All `[VS]`.

| Old | Modern | Status |
|---|---|---|
| `wait`, `spawn`, `delay` | `task.wait`, `task.spawn` or `task.defer`, `task.delay` | Deprecated |
| `Instance:Remove()`, `:children()`, `:clone()` | `:Destroy()`, `:GetChildren()`, `:Clone()` | Deprecated |
| `Humanoid:LoadAnimation` | `Animator:LoadAnimation`, tracks cached | Deprecated |
| `FindPartOnRay*`, `FindPartsInRegion3*` | `workspace:Raycast`, `Blockcast`/`Spherecast`/`Shapecast`, `GetPartBoundsInBox`/`Radius`, `GetPartsInPart` | Deprecated |
| `BodyVelocity`, `BodyPosition`, `BodyGyro`, `BodyForce` | `LinearVelocity`, `AlignPosition`, `AlignOrientation`, `VectorForce` | Deprecated |
| `PhysicsService:RegisterCollisionGroup`, `CollisionGroupSetCollidable`, `SetPartCollisionGroup` | `workspace:RegisterCollisionGroup`, `workspace:CollisionGroupSetCollidable`, `part.CollisionGroup = "Name"` | Deprecated |
| `TeleportService:Teleport`, `TeleportPartyAsync`, `TeleportToPlaceInstance`, `TeleportToPrivateServer`, `ReserveServer(Async)` | Server-side `TeleportAsync(placeId, players, options)`; reserved servers via `TeleportOptions.ReservedServerId = HttpService:GenerateGUID(false)` | Deprecated |
| `Player:LoadCharacter`, `BadgeService:AwardBadge`, `UserHasBadge`, `Player:IsInGroup`, `MarketplaceService:GetProductInfo`, `PlayerOwnsAsset` | The same name with `Async`, inside `pcall` | Deprecated (the yielding-method rename; LihFolk dates it January 2026) |
| `Player:GetRankInGroup(Async)` | `GroupService:GetRolesInGroupAsync` | Deprecated |
| `Player.MembershipType`, `MarketplaceService:PromptPremiumPurchase` | `Player.HasRobloxSubscription` (prompt: see `monetization-and-policy.md`) | Deprecated |
| `TextFilterResult:GetChatForUserAsync`, legacy `Chat` | `TextChatService`; `GetNonChatStringForBroadcastAsync` / `ForUserAsync` for names and signs | Deprecated |
| `getfenv`, `setfenv` | Modules and explicit parameters | Deprecated; they also de-optimise |
| `Lighting.Technology` | `LightingStyle` plus `PrioritizeLightingQuality` | Deprecated (`performance.md`) |
| `Model:SetPrimaryPartCFrame` | `Model:PivotTo` | Superseded (drift-free) |
| `RunService.RenderStepped`, `Stepped` | `PreRender`, `PreSimulation` (and `PreAnimation`, `PostSimulation`) | Superseded: the old events are not marked deprecated |
| `tick()` | `os.clock()` for durations, `os.time()` for timestamps, `workspace:GetServerTimeNow()` for clocks shared with clients | House standard; `tick` is not marked deprecated at this commit |
| `CFrame.new(position, lookAt)`, `Vector3.new(0, 0, 0)` | `CFrame.lookAt`, `Vector3.zero` / `Vector3.one` | Style |
| `math.random` (one shared generator) | `Random.new(seed)` per system | Style |
| `Instance.new("X", parent)` | Set properties, then `Parent` last | Performance |
| `pairs(t)` / `ipairs(t)` | `for k, v in t` | Style; same speed |
| `BindableEvent` between modules | A Luau Signal or a direct call | Bindables copy tables and drop metatables |
| `RemoteFunction:InvokeClient` | RemoteEvent out, RemoteEvent back, with a timeout | A client can hang the server thread forever |
| `MarketplaceService.ProcessReceipt` assigned in several scripts | One handler, or filtered `BindReceiptHandler` | `data-and-purchases.md` |

Conflict: the knowledge base lists `tick` with the removed APIs. Keep avoiding it, but do not tell a developer it is officially deprecated.

## Style conventions

Naming, the `Async` suffix and tooling are in `engineering-architecture.md`. In addition `[house]`:

- File order: directives (`--!strict`), services, requires, constants, types, private state, private functions, public table, `return`.
- One responsibility per module; split near 300 lines or when the top level approaches the 200-local limit.
- Early returns over nested `if`; guard clauses first.
- String interpolation over `..`; generalized iteration over `pairs`; `if … then … else` expressions for simple choices.
- No magic numbers: named constants or config tables, frozen.
- Functions that yield say so in the name and are never called from `Init` or a metamethod.
- Comments explain why, not what; a `--[[ ]]` block directly above a declaration shows as a hover tooltip in the Script Editor `[official]`.
- `@deprecated` on internal APIs you are retiring `[VS]`; delete them one release later.
- StyLua decides layout; never hand-format.

## Level-up: symptoms → cause → fix

| Symptom in an existing codebase | Likely cause | Fix |
|---|---|---|
| Types are `any` everywhere, autocomplete is useless | `--!nonstrict` default, `require` through dynamic paths, `:: any` casts | `--!strict` on touched files; static require paths; `unknown` plus validators at boundaries |
| Hundreds of new type errors after a Studio update | Solver switch `[VS]` | Check `UseNewLuauTypeSolver`; fix real errors; simplify the worst types |
| A script stops compiling after one more `local` | 200-local limit in the main chunk | Split into modules or group values in tables |
| Hitches every few seconds, nothing obvious | Allocation churn: per-frame tables, closures, strings, CFrame maths | Reuse tables, vector maths, pass functions with arguments |
| `--!native` made nothing faster, or slower | Code dominated by engine calls; untyped parameters; breakpoints set | Remove it; annotate; measure with the Script Profiler |
| Fast in a Studio benchmark, different live | Level 1 vs level 2 optimisation; desktop vs phone | `--!optimize 2` in benchmarks; profile on the device |
| Objects lose their methods after a remote or a save | Metatables are not serialised | Send plain data; rebuild objects on arrival |
| "Shared" module state differs between server and client, or between Actors | One copy per VM | Replicate state through attributes, remotes or `SharedTable` |
| Buttons or handlers all act on the last item | One outer variable captured by every closure | A local per iteration |
| Server threads stuck forever | `InvokeClient`, `:Wait()` on a signal that never fires, `WaitForChild` with no timeout | Events with timeouts; owners that cancel threads |
| A spring or camera goes black after a lag spike | Unclamped `dt`, NaN written to a CFrame | The spring sketch above; guard the write |
| Old tutorials' code everywhere | Deprecated APIs | Sketch F in `engineering-architecture.md` counts them; replace on touch using the table above |

## Review gate

- [ ] `--!strict` on new and touched files; no `:: any` without a runtime check next to it; untrusted input typed `unknown`.
- [ ] No deprecated API from the table; no `getfenv`, `setfenv` or `loadstring`.
- [ ] Module top levels do not yield; no require cycles; no server logic in replicated modules.
- [ ] Classes only where instances have a lifetime, each with `Destroy`; plain modules elsewhere.
- [ ] Every connection, thread and timer has an owner that cleans it; no weak-table cleanup for Instances.
- [ ] No per-frame allocation in hot loops; objects built in one literal; arrays presized where the size is known.
- [ ] `buffer`, `@native` and Actors only with a before-and-after measurement at the live optimisation level on the target device.
- [ ] Springs clamp `dt` and reject non-finite values; remaps clamp; randomness for anything of value is server-side and seeded per system.
- [ ] `[VS]` features (`const`, type functions, explicit instantiation, `coroutine.finally`) confirmed in the current Studio and toolchain before adoption.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07); `luau-lang/site` at c0eb09d (2026-10-20); `luau-lang/rfcs` at 5fcbb5a (2026-10-16); `luau-lang/luau` at 12a6ba7 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/luau/{variables,scope,functions,comments,type-checking,native-code-gen}.md`, `scripting/multithreading.md`, `reference/engine/libraries/{task,coroutine,math,vector,buffer,table,debug}.yaml`, `reference/engine/globals/{LuaGlobals,RobloxGlobals}.yaml`, `reference/engine/datatypes/Random.yaml`, `reference/engine/enums/LuauTypeCheckMode.yaml`, `reference/engine/classes/{Workspace,Player,BadgeService,Humanoid,Model,WorldRoot,TeleportService,TeleportOptions,PhysicsService,Instance,RunService,TextFilterResult}.yaml` (read)
- https://github.com/luau-lang/site: `src/content/docs/guides/{performance,sandbox}.md`, `getting-started/{syntax,compatibility}.md`, `reference/{attributes,grammar,types-library}.md`, `types/{generics,type-functions,object-oriented-programs}.md`, `src/content/news/2025-12-19-luau-recap-runtime-2025.md` (read)
- https://github.com/luau-lang/rfcs: `docs/{const-keyword,explicit-type-parameter-instantiation,user-defined-type-functions,keyof-type-operator,index-type-operator,metatable-type-functions,syntax-attribute-functions-deprecated,function-math-lerp,function-math-map,math-isnan-isfinite-isinf,function-buffer-bits,vector-library,function-vector-lerp,syntax-classes,export-keyword,type-long-integer,support-for-cyclic-requires,function-coroutine-finally,property-readonly}.md` (read; status lines)
- https://github.com/luau-lang/luau: `Compiler/src/Compiler.cpp` (read; register and upvalue limit error texts)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/02 Luau Scripting/{Luau Language Essentials, Task Library Coroutines and Yielding, Events Signals and Connections, Luau Performance Patterns with Benchmarks, Luau Performance and Native Codegen, Parallel Luau and Actors, Math Vectors and CFrames}.md`; `35 Advanced Luau/{Advanced Types - Generics and Type Functions, Luau Garbage Collection and the Memory Model}.md`; `40 Game Math/Interpolation Easing and Curves Math.md`; `56 Field Notes/Springs That Survive Long Frames - dt Clamps and NaN Guards.md`; `SYMPTOMS.md` (read)
- https://devforum.roblox.com/t/general-release-luau%E2%80%99s-new-type-solver/4084991 (search summary; general release, beta toggle removal, known slowness)
- https://create.roblox.com/docs/updates/2026-08-24.md (search summary; solver fixes continuing)
- https://devforum.roblox.com/t/release-notes-for-711/4473831 and https://devforum.roblox.com/t/feedback-on-variables/4590572 (search summary; `const` arrival and early documentation gap)
- https://devforum.roblox.com/t/parallel-luau-version-2-release/2399970 and https://devforum.roblox.com/t/are-frozen-sharedtable-reads-faster-than-standard-sharedtable-reads/4762719 (search summary; SharedTable about 10× slower)
- Not reachable: devforum.roblox.com, create.roblox.com and reddit.com directly; the GitHub REST API (release notes not read first-hand). No evidence found: StyLua, Selene or luau-lsp release notes confirming `const` support; an official statement of the 200,000-character `Source` limit; whether user-defined type functions can be exported across modules.
