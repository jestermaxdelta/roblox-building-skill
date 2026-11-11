# Cutscene timeline runner: the full client module

What this is: the companion to `cutscenes-and-cinematics.md` §14, split out so that guide stays readable. One client module plays data-driven cutscenes: several shots and cuts, timed cues, a camera that travels by distance along a Catmull-Rom curve with a ramp–hold–ramp speed profile, an aim on its own curve, and one restore function for every exit. The rules it implements live in the guide (§5 paths and easing, §7 architecture and exit paths, §8 skip, §13 data format); this file holds only the code and how to check it. Tags as in the guide: `[official]` Roblox creator docs (mirror read 2026-11-11), `[community]` other developers' practice, `[house]` a starting number to test.

## Start here by level

| Level | Do | Ignore for now |
|---|---|---|
| Beginner | Use the first-cutscene script in `cutscenes-and-cinematics.md` §14 instead of this module | This file |
| Intermediate | Copy the module as is. Write each scene as a timeline (guide §13), call `play` from one client controller, show Skip when `handle.canSkip()` is true and call `handle.stop("skipped")` | Seeking, anchors, pause |
| Expert | Add the parts left out on purpose (below) one at a time and re-run every exit test after each | Nothing |

## The module

```lua
--!strict
-- Unexecuted sketch. Client ModuleScript required from StarterPlayerScripts, never from the character or a
-- ResetOnSpawn gui: the restore must outlive the character. Camera only; cues go to the game's own systems.
-- One exit: every way out calls finish(), which runs each restore in reverse order. step() never yields.
local GuiService = game:GetService("GuiService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

export type Key = { pos: Vector3, look: Vector3, fov: number }
-- easeIn, easeOut: seconds of speed ramp at the start and end of the shot (defaults 0.4 and 0.6: the settle is longer)
export type Shot = { t: number, length: number, keys: { Key }, easeIn: number?, easeOut: number? } -- a new shot is a cut
export type Cue = { t: number, id: string, state: boolean? } -- state cues also fire on skip
export type Timeline = { length: number, skipAfter: number, shots: { Shot }, cues: { Cue } }
export type Handle = { stop: (reason: string) -> (), canSkip: () -> boolean }
type Track = { pos: { Vector3 }, look: { Vector3 }, fov: { number }, ds: { number }, total: number }

local BIND, STEPS = "CutsceneRunner", 32 -- STEPS: length-table samples per key-to-key segment
local player = Players.LocalPlayer
-- Resolved once at require time (this yields), so play() never yields between taking the camera and arming the exits.
local controls = (require :: any)(player:WaitForChild("PlayerScripts"):WaitForChild("PlayerModule")):GetControls()
local active: Handle? = nil

local function curve(pts: { Vector3 }, x: number): Vector3 -- Catmull-Rom through pts; x runs from 0 (first key) to #pts - 1
	local n = #pts
	if n == 1 then return pts[1] end
	local i = math.min(math.floor(x) + 1, n - 1)
	local a, b, c, d, u = pts[math.max(i - 1, 1)], pts[i], pts[i + 1], pts[math.min(i + 2, n)], x - (i - 1)
	return (b * 2 + (c - a) * u + (a * 2 - b * 5 + c * 4 - d) * u * u + (b * 3 - a - c * 3 + d) * u * u * u) * 0.5
end

local function build(shot: Shot): Track -- the length table: distance travelled after each sample along the path
	assert(#shot.keys > 0, "a shot needs at least one key")
	local tr: Track = { pos = {}, look = {}, fov = {}, ds = { 0 }, total = 0 }
	for i, key in shot.keys do tr.pos[i], tr.look[i], tr.fov[i] = key.pos, key.look, key.fov end
	for k = 1, (#shot.keys - 1) * STEPS do
		tr.total += (curve(tr.pos, k / STEPS) - curve(tr.pos, (k - 1) / STEPS)).Magnitude
		table.insert(tr.ds, tr.total)
	end
	return tr
end

local function paramAt(tr: Track, share: number): number -- key parameter after covering `share` (0 to 1) of the path
	if tr.total < 1e-3 then return share * (#tr.pos - 1) end -- the camera does not travel: turn the aim by time
	local d, lo, hi = share * tr.total, 1, #tr.ds
	while hi - lo > 1 do -- binary search for the two samples either side of distance d
		local mid = (lo + hi) // 2
		if tr.ds[mid] < d then lo = mid else hi = mid end
	end
	return (lo - 1 + (d - tr.ds[lo]) / math.max(tr.ds[hi] - tr.ds[lo], 1e-6)) / STEPS
end

-- Ramp–hold–ramp: speed rises over a seconds, holds, falls over b seconds. Returns the share of the path covered.
local function covered(t: number, len: number, a: number, b: number): number
	if len <= 0 then return 1 end
	t, a, b = math.clamp(t, 0, len), math.min(a, len * 0.45), math.min(b, len * 0.45)
	local top = 1 / (len - (a + b) / 2) -- peak speed, in shares of the path per second
	if t < a then return top * t * t / (2 * a) end
	if t > len - b then return 1 - top * (len - t) ^ 2 / (2 * b) end
	return top * (t - a / 2)
end

local function play(tl: Timeline, onCue: (id: string, skipped: boolean) -> ()): Handle
	if active then active.stop("replaced") end -- the old scene restores fully before this one reads the camera
	local camera = workspace.CurrentCamera :: Camera
	local undo: { () -> () } = {}
	local tracks: { Track } = {}
	local clock, cueIndex, shotIndex, finished = 0, 1, 1, false
	local reduced = GuiService.ReducedMotionEnabled -- ask the game's comfort module instead if it has one
	local handle: Handle

	local function finish(reason: string)
		if finished then return end
		finished = true
		RunService:UnbindFromRenderStep(BIND) -- no error if nothing is bound
		for i = #undo, 1, -1 do pcall(undo[i]) end -- restore first; one failing restore cannot block the rest
		if active == handle then active = nil end -- before the cues, in case one of them starts the next scene
		for i = cueIndex, #tl.cues do -- the world must end in the same state on every path
			if tl.cues[i].state then task.spawn(onCue, tl.cues[i].id, true) end -- spawned: a cue may yield or throw
		end
		-- log `reason` (finished, skipped, died, respawn, teleport, replaced, error, watchdog) as an analytics event
	end

	local function step(dt: number)
		clock += math.min(dt, 0.1) -- voiced scenes: read the clock from the audio's TimePosition instead
		while not finished and cueIndex <= #tl.cues and tl.cues[cueIndex].t <= clock do
			cueIndex += 1
			task.spawn(onCue, tl.cues[cueIndex - 1].id, false)
		end
		if finished then return end -- a cue stopped the scene: never write the camera after the restore
		while shotIndex < #tl.shots and tl.shots[shotIndex + 1].t <= clock do shotIndex += 1 end
		local shot, tr = tl.shots[shotIndex], tracks[shotIndex]
		local share = if reduced then 1 else covered(clock - shot.t, shot.length, shot.easeIn or 0.4, shot.easeOut or 0.6)
		local x = paramAt(tr, share)
		local i = math.min(math.floor(x) + 1, #tr.fov)
		local j = math.min(i + 1, #tr.fov)
		local look = curve(tr.look, x) -- the aim has its own curve and reaches each key's look point with the camera
		camera.CFrame = CFrame.lookAt(curve(tr.pos, x), look)
		camera.Focus = CFrame.new(look)
		camera.FieldOfView = tr.fov[i] + (tr.fov[j] - tr.fov[i]) * (x - (i - 1))
		if clock >= tl.length then finish("finished") end
	end

	local function setup()
		for i, shot in tl.shots do tracks[i] = build(shot) end -- bad shot data fails here, before anything is taken
		local prevType, prevFov = camera.CameraType, camera.FieldOfView
		camera.CameraType = Enum.CameraType.Scriptable
		table.insert(undo, function()
			camera.CameraType = prevType
			camera.FieldOfView = prevFov -- through the FOV owner module if the game has one
			local character = player.Character
			local humanoid = character and character:FindFirstChildOfClass("Humanoid")
			if humanoid then camera.CameraSubject = humanoid end
		end)
		controls:Disable()
		table.insert(undo, function() controls:Enable() end)
		for _, flag in { "HudHidden", "LightingLocked" } do -- attributes set by a client stay local; controllers read them
			player:SetAttribute(flag, true)
			table.insert(undo, function() player:SetAttribute(flag, nil) end)
		end
		local character = player.Character
		local humanoid = character and character:FindFirstChildOfClass("Humanoid")
		local connections: { RBXScriptConnection } = {
			player.CharacterRemoving:Connect(function() finish("respawn") end),
			player.OnTeleport:Connect(function(state: Enum.TeleportState)
				if state == Enum.TeleportState.Started then finish("teleport") end
			end),
		}
		if humanoid then table.insert(connections, humanoid.Died:Connect(function() finish("died") end)) end
		table.insert(undo, function()
			for _, connection in connections do connection:Disconnect() end
		end)
		task.delay(tl.length + 2, finish, "watchdog") -- render steps can stall; this timer does not
		RunService:BindToRenderStep(BIND, Enum.RenderPriority.Camera.Value + 1, function(dt: number)
			local ok, err = pcall(step, dt)
			if not ok then warn("cutscene step failed:", err); finish("error") end
		end)
	end

	handle = {
		stop = finish, -- the skip button calls handle.stop("skipped") when canSkip() is true
		canSkip = function() return not finished and clock >= tl.skipAfter end,
	}
	active = handle
	if not pcall(setup) then finish("error") end -- a failure half-way through setup still restores what was taken
	return handle
end

return { play = play }
```

## How it moves the camera

- **By distance, not by key.** `build` samples each shot's curve 32 times per key-to-key segment into a length table before the camera is taken; `paramAt` finds the curve parameter for a distance by binary search and interpolates inside one sample step. Equal time steps then give equal distances, wherever the keys sit (guide §5; sheet 14, lower left).
- **One speed profile per shot.** `covered` is a trapezoid: speed rises for `easeIn` seconds (default 0.4), holds, and falls for `easeOut` (default 0.6, the settle longer than the start `[house]`); each ramp is capped at 45% of the shot. Peak speed is `1 ÷ (length − (easeIn + easeOut) ÷ 2)` path-lengths per second. Set both to 0 for a constant-speed move inside a longer sequence.
- **The aim has its own curve.** `look` runs through the keys' look points at the same parameter as the position, so every key's framing is hit exactly and roll never appears. A shot whose keys share one position is a pan: the aim then moves by time.
- **FOV** runs linearly key to key; keep the change inside a shot to 15° or less (guide §5).
- **Reduced motion** holds each shot at its last key and cuts between shots (guide §8).

**Hand check** (computed with a port of `curve`, `build`, `paramAt` and `covered`): three keys at (0, 4, 0), (30, 4, 0) and (40, 4, 10), a 4 s shot, default ramps. The curve is 44.7 studs (30.1 + 14.6). Speed rises to 12.8 studs/s by 0.4 s, holds within 2% through the middle key (passed at 2.56 s) until 3.4 s, falls to zero, and the camera lands exactly on the last key at 4.0 s. The previous sketch, which stepped the spline parameter with one Sine ease over the shot, ran 17.8 studs/s at 1 s and 7.1 at 3 s on the same keys: the lurch at the middle key that guide §5 forbids.

## Exits, and what is left out

What reaches `finish`: scene end, skip, death, character removal, teleport start, a second `play`, an error in setup (bad shot data included: `build` runs before anything is taken) or in the camera step, and the watchdog. An error inside a cue is isolated by `task.spawn` and the scene carries on. When the local player leaves the game the client is gone, so there is nothing to restore; other players leaving cannot break a scene because actors are local clones (guide §6). Nothing in `step` yields; every connection is disconnected by the undo list.

Left out on purpose: the readiness gate (guide §12), the anchor transform (multiply each key by the anchor's CFrame when building), pause, seeking for synced scenes (start `clock` at `now − start` and fire only `state` cues before it), fades, letterbox and shake (add shake last, through the comfort gate in `vfx-and-juice.md` §7).

## Review gate

- [ ] Every exit tested by hand: reset the character mid-scene, call `play` twice, call `play` from a state cue, stop the scene from inside a cue, give a shot no keys, teleport mid-scene, let the watchdog fire. After each, camera type, subject and FOV, controls, HUD and lighting flags are back.
- [ ] A three-key shot moves at one steady speed between its ramps (watch the middle key; print distance per frame if unsure), and the camera ends exactly on the last key.
- [ ] With Reduce Motion on, each shot holds its last framing.
- [ ] Nothing in `step` waits or creates instances; the bound name is unbound on every exit.

## Sources

- Roblox creator docs (read in the `Roblox/creator-docs` mirror, 2026-11-11): `RunService` (`BindToRenderStep` runs during `PreRender` and only on the client; `UnbindFromRenderStep` does nothing when the name is not bound), `RenderPriority` (`Camera` = 200), `Camera` (`Focus`, `FieldOfView`, `CameraType`), `GuiService.ReducedMotionEnabled`, `Player` (`OnTeleport`, `CharacterRemoving`), `Humanoid.Died`, `TweenService:GetValue` (clamps alpha; errors on the Bezier and Spring styles) `[official]`.
- `PlayerModule:GetControls()` with `Enable` and `Disable` belongs to Roblox's default player scripts, not the API reference; it is the long-standing community route to turn movement off `[community]`.
- Path maths: Catmull-Rom as in the guide's library row 28 (CRSplineModules); arc-length tables and trapezoidal speed profiles are standard animation practice. The hand check was computed, not run in Roblox.
