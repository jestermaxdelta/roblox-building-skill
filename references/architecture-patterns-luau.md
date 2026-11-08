# Game Programming Patterns in Luau

Distilled from knowledge-base section 2.12 (Nystrom's 19 patterns mapped to Roblox). Add a pattern only when the problem it solves is actually present. The Roblox mappings are the compiler's translation (general knowledge); snippets are unexecuted sketches.

| Pattern | Roblox and Luau form | Use when |
|---|---|---|
| Command | Remote intents validated on the server; undo closures; replay lists | Rebindable input, undo in building games, replays, puzzle validation |
| Flyweight | Shared mesh/texture asset IDs, Packages, frozen per-type data tables | Many objects share most of their data |
| Observer | Signal module, engine events, `BindableEvent` (copies its arguments) | Achievements, quests, UI, analytics reacting to gameplay |
| Prototype | `Instance:Clone()` of Blender templates in `ServerStorage`; data delegation | Spawners, variants |
| Singleton | ModuleScript caching per environment; an Init/Start bootstrap | Rarely; use explicit lifecycle instead |
| State | NPC FSM, `HumanoidStateType`, a pushdown screen stack | Clearly separated modes; replaces boolean-flag explosions |
| Double Buffer | Two grids swapped each step | Cellular automata, simultaneous AI decisions |
| Game Loop | `RunService` events plus a fixed-step accumulator | Deterministic simulation (TD waves, lockstep) |
| Update Method | One central `Heartbeat` list with a dead-sweep | Many independent objects needing per-frame behaviour |
| Bytecode | Whitelisted data ops; `loadstring` stays disabled | Designer-authored abilities, card effects |
| Subclass Sandbox | A base module with protected helpers | Many small variations sharing the same engine touches |
| Type Object | Breed data with resolved parent inheritance | Enemies, items, towers, pets that differ in data |
| Component | `CollectionService` tags, or the jecs ECS | Mix-and-match capabilities; thousands of entities for ECS |
| Event Queue | Per-frame drained queue, `SignalBehavior.Deferred` `[VS]`, remotes | Bursty producers, merging duplicates |
| Service Locator | A registry module with null services | Cross-cutting audio, analytics, logging |
| Data Locality | Parallel arrays, an ECS, `buffer`, Actors, only after profiling | Hot loops over thousands of entities |
| Dirty Flag | Cached computed stats | RPG stats, inventory weight, nav graphs after building |
| Object Pool | Reused parts, models, effects, sounds; `BulkMoveTo` | Projectiles, particles, damage numbers, enemies |
| Spatial Partition | `GetPartBoundsInBox`/`Radius` with `OverlapParams`; a grid hash for data | Proximity queries, AI perception |

## Key sketches

Command (server whitelist with undo, cap history at 50, clear on `PlayerRemoving`):

```lua
local Commands = {}
Commands.PlaceProp = {
	validate = function(player: Player, args): boolean
		return typeof(args.propId) == "string" and typeof(args.cell) == "Vector3"
	end,
	execute = function(player: Player, args): () -> ()
		local prop = placeProp(player, args.propId, args.cell)
		return function() prop:Destroy() end -- undo closure
	end,
}
local history: { [Player]: { () -> () } } = {}
remote.OnServerEvent:Connect(function(player, name, args)
	if typeof(name) ~= "string" or typeof(args) ~= "table" then return end
	local command = Commands[name]
	if not command or not command.validate(player, args) then return end
	local list = history[player] or {}
	history[player] = list
	table.insert(list, command.execute(player, args))
	if #list > 50 then table.remove(list, 1) end
end)
```

Observer (Signal whose handlers run in their own threads):

```lua
local Signal = {}
Signal.__index = Signal
function Signal.new() return setmetatable({ _handlers = {} }, Signal) end
function Signal:Connect(handler: (...any) -> ())
	local handlers = self._handlers
	table.insert(handlers, handler)
	return { Disconnect = function()
		local index = table.find(handlers, handler)
		if index then table.remove(handlers, index) end
	end }
end
function Signal:Fire(...)
	for _, handler in table.clone(self._handlers) do task.spawn(handler, ...) end
end
return Signal
```

Singleton alternative: every service module exposes `Init` (internal state, no cross-calls) and `Start` (may call other services); one bootstrap requires all, calls every `Init`, then every `Start`. Each Actor has its own Luau environment and therefore its own module copies.

Game Loop (fixed step inside `Heartbeat`):

```lua
local STEP, accumulator = 1 / 20, 0
RunService.Heartbeat:Connect(function(dt)
	accumulator += math.min(dt, 0.25) -- clamp hitches
	while accumulator >= STEP do
		simulate(STEP)
		accumulator -= STEP
	end
	render(accumulator / STEP)
end)
```

Type Object (breeds with parent inheritance resolved once at load, then frozen):

```lua
local raw = {
	Troll = { health = 25, attack = "The troll hits you!", model = "Troll" },
	TrollArcher = { parent = "Troll", attack = "The troll archer fires an arrow!" },
}
local resolved = {}
local function resolve(name: string)
	if resolved[name] then return resolved[name] end
	local entry = raw[name]
	local result = if entry.parent then table.clone(resolve(entry.parent)) else {}
	for key, value in entry do
		if key ~= "parent" then result[key] = value end
	end
	resolved[name] = table.freeze(result)
	return resolved[name]
end
for name in raw do resolve(name) end
return resolved
```

Component via tags (attach behaviour and cleanup to every tagged instance, including streamed-in ones):

```lua
local CollectionService = game:GetService("CollectionService")
local cleanups: { [Instance]: () -> () } = {}
local function onAdded(instance: Instance)
	if instance:IsA("Model") then cleanups[instance] = attachSpinner(instance) end
end
local function onRemoved(instance: Instance)
	local cleanup = cleanups[instance]
	if cleanup then cleanup(); cleanups[instance] = nil end
end
CollectionService:GetInstanceAddedSignal("Spinner"):Connect(onAdded)
CollectionService:GetInstanceRemovedSignal("Spinner"):Connect(onRemoved)
for _, instance in CollectionService:GetTagged("Spinner") do onAdded(instance) end
```

jecs (v0.11 API in the source; check the current version): `local world = jecs.world()`, `local Position = world:component() :: jecs.Id<Vector3>`, `world:set(e, Position, v)`, `for entity, position, velocity in world:query(Position, Velocity) do ... end`. Its "800,000 entities at 60 fps" is a benchmark claim; measure on your workload. ECS pays off at thousands of entities and is overkill for dozens.

Event Queue (per-frame drain with aggregation; requests made while handling go to the next frame):

```lua
local pending: { [string]: { position: Vector3, count: number } } = {}
local function requestSound(name: string, position: Vector3)
	local request = pending[name]
	if request then request.count += 1 else pending[name] = { position = position, count = 1 } end
end
RunService.Heartbeat:Connect(function()
	local batch = pending
	pending = {}
	for name, request in batch do
		playAt(name, request.position, math.min(1, 0.5 + 0.1 * request.count))
	end
end)
```

Dirty Flag (stats in layers base → flat → percent → clamp; every write path sets the flag):

```lua
function Stats:addModifier(stat: string, flat: number, percent: number)
	table.insert(self.modifiers, { stat = stat, flat = flat, percent = percent })
	self.dirty = true
end
function Stats:get(stat: string): number
	if self.dirty then
		local flat, percent = {}, {}
		for _, m in self.modifiers do
			flat[m.stat] = (flat[m.stat] or 0) + m.flat
			percent[m.stat] = (percent[m.stat] or 0) + m.percent
		end
		for name, value in self.base do
			self.cache[name] = math.max(0, (value + (flat[name] or 0)) * (1 + (percent[name] or 0)))
		end
		self.dirty = false
	end
	return self.cache[stat] or 0
end
```

Object Pool (park by CFrame far away rather than reparenting; reset reused state; pick an overflow policy: skip, steal oldest, or grow):

```lua
local HIDDEN = CFrame.new(0, -10000, 0)
function Pool.new(template: BasePart, size: number, folder: Instance)
	local self = setmetatable({ free = table.create(size), template = template }, Pool)
	for i = 1, size do
		local part = template:Clone()
		part.Anchored, part.CanCollide, part.CFrame, part.Parent = true, false, HIDDEN, folder
		self.free[i] = part
	end
	return self
end
function Pool:get(cframe: CFrame): BasePart?
	local part = table.remove(self.free)
	if not part then return nil end
	part.CFrame = cframe
	part.Transparency = self.template.Transparency
	return part
end
function Pool:release(part: BasePart)
	part.CFrame = HIDDEN
	table.insert(self.free, part)
end
```

Pooled projectiles are non-colliding visuals; the solid-collision rule applies to world objects players can touch, and the server decides every hit.

Spatial Partition: prefer engine queries (`OverlapParams` with `FilterType = Include` on an enemies folder, `workspace:GetPartBoundsInRadius(position, radius, params)`); for data-only entities build a grid hash keyed by `Vector3.new(math.floor(x / CELL), 0, math.floor(z / CELL))` (`Vector3` hashes by value) and scan the 3×3 neighbourhood.

Bytecode alternative: `loadstring` is disabled via `ServerScriptService.LoadStringEnabled` and enabling it for untrusted text is a serious security risk. Use a flat list of whitelisted ops: `{ { "damage", 12 }, { "effect", "Burn" }, { "heal", 3 } }` interpreted by `Ops[instruction[1]](ctx, table.unpack(instruction, 2))`.

Pushdown screen stack: `push(screen)` pauses the top and enters the new one; `pop()` exits the top and resumes the one below, so Back always returns exactly where you were.
