# Game craft: feel, level design, camera, audio, AI, procgen, saves, physics

Distilled from knowledge-base sections 2.0 to 2.2, 2.4, 2.6 to 2.10. UI design and input live in ui-input-crossplatform.md. Four platform facts shape everything here: the server is authoritative and the client untrusted (rules on the server, juice on the client); the engine owns the game loop (hook `RunService` events); every device shares one server (design for a small landscape phone); players arrive mid-session from discovery (teach the verb in 30–60 s with no reading).

Art-direction guard against "AI slop" (from the asset pipeline source): describe the style along named axes (shape language, silhouette, value, colour, edge, material, light, detail density, camera, motion), approve one hero asset before producing families, and judge every asset at three distances (close, gameplay, far).

## 1. Game feel and juice

A polished "hit" is a cluster of 5–8 small responses inside about 100 ms: target flash, hit-stop, camera shake, particle burst, sound, squash/scale pop, damage number, sometimes rumble. Everything returns to rest.

| Tier | Example | Trauma added | Hit-stop | Particles | Extras |
|---|---|---|---|---|---|
| Small | coin pickup, footstep, light hit | 0.10–0.20 | none | 0–4 | sound, small pop |
| Medium | normal hit, door, level-up tick | 0.30–0.50 | 0.04–0.06 s | 6–12 | 1–3 frame flash |
| Large | kill, boss hit, explosion, rare drop | 0.70–1.00 | 0.10–0.15 s | 20–40 | flash, brief zoom, big number |

Values: trauma 0–1 decaying 1.0–1.5/s, shake = trauma², driven by smooth noise (never per-frame random), max roll 0.05–0.12 rad and about 0.3–0.8 studs offset at third-person distance. Hit-stop timed on a real-time clock; only the newest hit-stop restores speed. Pop: scale 1.3 on one axis and 0.7 on the other, tween back over about 0.18 s with Back Out. Flash 1–3 frames. Damage numbers rise, fade, drift sideways.

Easing: Back Out for pops, Quad/Cubic Out for settling, Cubic In for wind-ups, Sine InOut for camera and menus, Linear only for real-time progress bars.

Juice checklist per core verb (hit, jump, collect, buy, level up, die): same-frame visual at the point of action; a varied sound; camera reaction scaled to tier; UI reaction (counter pops and counts up, never snaps); anticipation and follow-through; everything returns to rest; effects pooled; accessibility (shake slider default 60–80%, reduce-flashing at most 3 flashes/s, reduce-motion option).

Anti-patterns: shaking the character instead of the camera; per-frame random shake; effects that outlive their cause; maximum juice on every event; juice that hides telegraphs.

Roblox mapping: `TweenService` with `Enum.EasingStyle.Back`; camera shake as an additive offset on `workspace.CurrentCamera.CFrame` removed before and re-added after the default camera step (`BindToRenderStep` at `Enum.RenderPriority.Camera.Value - 1` and `+ 1`), or `Humanoid.CameraOffset` for position-only; `ParticleEmitter` with `Enabled = false` and `emitter:Emit(count)`; `Trail` and `Beam`; `Highlight` (keep one per target and toggle `Enabled`; the client limit is 255 per current docs, previously 31 `[VS]`); `UIScale` tweens; hit-stop via `track:AdjustSpeed(0)` on the client only. Never fire one RemoteEvent per particle: send one event per gameplay fact ("hit at X, tier medium") and let the client build the cluster. Cap emitter counts on weak devices.

```lua
-- LocalScript. Trauma-based camera shake that never accumulates.
local RunService = game:GetService("RunService")
local camera = workspace.CurrentCamera
local Shake = {}
local trauma, DECAY, FREQ, userScale = 0, 1.2, 15, 0.7
local MAX_ROLL, MAX_PITCH_YAW, MAX_OFFSET = math.rad(4), math.rad(2), 0.5
local applied = CFrame.identity

function Shake.add(amount: number) trauma = math.min(1, trauma + amount) end

RunService:BindToRenderStep("ShakeUndo", Enum.RenderPriority.Camera.Value - 1, function()
	camera.CFrame = camera.CFrame * applied:Inverse()
	applied = CFrame.identity
end)
RunService:BindToRenderStep("ShakeApply", Enum.RenderPriority.Camera.Value + 1, function(dt)
	if trauma <= 0 then return end
	trauma = math.max(0, trauma - DECAY * dt)
	local s, t = trauma * trauma * userScale, os.clock() * FREQ
	applied = CFrame.new(MAX_OFFSET * s * math.noise(t, 13.6), MAX_OFFSET * s * math.noise(t, 21.4), 0)
		* CFrame.Angles(MAX_PITCH_YAW * s * math.noise(t, 0.31), MAX_PITCH_YAW * s * math.noise(t, 4.73), MAX_ROLL * s * math.noise(t, 9.17))
	camera.CFrame = camera.CFrame * applied
end)
return Shake
```

## 2. Level design

Derive movement metrics first: `MAX_JUMP_HEIGHT = v²/(2g)`, `AIR_TIME = 2v/g`, `MAX_JUMP_DISTANCE = run_speed × AIR_TIME`, `SAFE_GAP = 0.7 × MAX_JUMP_DISTANCE` (critical path), `HARD_GAP = 0.95 ×` (optional/expert). Confirm with a measured gap ladder on every device type.

Roblox defaults `[VS]`: `WalkSpeed` 16 studs/s, `JumpPower` 50, `JumpHeight` 7.2 studs, `MaxSlopeAngle` 89°, `workspace.Gravity` 196.2. Which jump property applies depends on `UseJumpPower`; check StarterPlayer in your place. Derived: JumpPower 50 gives about 6.37 studs height, 0.51 s air time, 8.2 studs running jump, safe gap 5.7, hard gap 7.8; JumpHeight 7.2 gives 8.7 / 6.1 / 8.2. R15 is about 5 studs tall (pathfinding `AgentHeight` 5, `AgentRadius` 2). Doors at least 7 tall and 4–5 wide; multiplayer corridors 8+ wide; a comfortable ledge is about 80% of jump height (about 5 studs). Thumbsticks can move slower than `WalkSpeed`; design for keyboard, test on a stick. Disable jumping with `Humanoid:SetStateEnabled(Enum.HumanoidStateType.Jumping, false)`, not power 0. Keep metrics in one `LevelMetrics` module so designers and generators share them.

Workflow: blockout, test, iterate, then dress. Under the house rules the blockout is a disposable planning artefact (Blender blockout kit, or primitives in an unpublished place or a `_Blockout` folder deleted before release); the dressed level is entirely Blender models.

Paths: critical (minimum route), golden (intended best-feeling route past the views and teaching moments), branches (secrets, shortcuts). Pacing follows a sawtooth with a rest before every climax; plan with a beat table (segment, beat type, intensity 1–5, what it teaches or tests). Teaching loop per mechanic: introduce safely → develop → twist (combine or recontextualise) → test without help.

Gating: lock and key, ability gate, one-way drop (always telegraphed), soft gate. Run a soft-lock check: grow the reachable set from spawn with held keys and abilities until nothing changes; the goal must be in the final set. Automate it for generated levels.

Guidance without walls: light and contrast, leading lines, far landmarks, breadcrumbs, framed vistas, one consistent colour for interactable/climbable. Hubs: compact (every activity within about 10 s of walking), each spoke visible from the centre and marked by a Blender landmark, shops visible but off the main line.

Blockout review: next objective visible from every checkpoint; critical gaps at or below `SAFE_GAP`; one-way drops telegraphed; a rest before every intensity-5 beat; a landmark visible from every major area; soft-lock check passes; reads on a phone; flow measured with real testers.

Obbies: checkpoints every 30–60 s of expected play (more often early), each obstacle type introduced alone then combined; track completion and deaths per stage, and treat a quit-heavy stage as a design bug. Spawns: an invisible `SpawnLocation` inside a Blender pad that carries the visible collision, facing the first objective, never in a traffic lane, with spawn protection where combat exists. Kill zones: a Blender lava or spike model with real collision plus an invisible non-colliding trigger for `Touched`.

## 3. Camera

Smoothing must be frame-rate independent: `alpha = 1 - exp(-rate * dt)`, `pos = lerp(pos, target, alpha)`, rate 5–12/s. Deadzone for small movement; look-ahead eased over 0.2–0.4 s; clamp the view, not the centre; platformers follow vertical lazily. Orbit cameras clamp pitch to about −80° to +45°; spring arm by raycasting from target to desired position; update after the target moves; shake is applied last; reset smoothing on teleport or respawn. FOV changes over about 10–15° need a reduce-motion option.

Roblox: the default `PlayerModule` camera already gives orbit, zoom, popper collision and shift-lock; change it only when the genre needs it. Properties `[VS]`: `Camera.FieldOfView` 70, `CameraMinZoomDistance` 0.5 / `CameraMaxZoomDistance` 128, `StarterPlayer.CameraMode`, `EnableMouseLockOption`, `Humanoid.CameraOffset`. Custom cameras set `CameraType = Scriptable` and drive `Camera.CFrame` in `BindToRenderStep` at `Enum.RenderPriority.Camera.Value`. Mobile players rotate the camera by dragging the right side of the screen, so keep drag-heavy UI off it.

## 4. Audio

Bus tree: Master → Music, SFX, Ambience, UI, Voice. Sliders control buses; square a linear 0–1 slider before applying (loudness is logarithmic). Loudness targets: true peak at most −1 dBTP; about −24 LUFS ±2 for console/PC; about −18 LUFS for mobile. Ducking: sidechain compressor on Music keyed from Voice (threshold about −30 dB, ratio 4–8:1, attack ≤10 ms, release 300–500 ms) or a simple −12 dB tween over 0.25 s. Variation: pitch ±1 semitone, volume ±2 dB, 3–5 variants never repeated back to back, polyphony capped (for example 4 simultaneous coin pickups, steal the oldest). Adaptive music: vertical layers fading over 0.5–1.5 s, horizontal switches at bar boundaries, intensity with hysteresis (up at 0.6, down at 0.4), beat read from the audio clock. Every UI action and gameplay verb gets a sound; rewards sound better as they get rarer.

Roblox: legacy `Sound` → `SoundGroup` (with `CompressorSoundEffect.SideChain`); 3D when parented to a part, 2D in `SoundService`; `SoundService:PlayLocalSound`. Newer audio graph `[VS]`: `AudioPlayer` → `Wire` → `AudioFader`/`AudioEqualizer`/`AudioCompressor` (Input and Sidechain pins)/`AudioReverb`/`AudioLimiter` → `AudioDeviceOutput` or `AudioEmitter`/`AudioListener`. Do not mix the two systems without checking current routing docs. Use `RollOffMinDistance`/`RollOffMaxDistance` with `InverseTapered`. Audio asset permissions can make a sound play silently `[VS]`. Clone per play only for low-rate sounds; pool high-rate ones.

## 5. Game AI

Fun AI beats smart AI: telegraph attacks, react with a 0.2–0.5 s delay, miss sometimes, take turns, show state. Three layers kept separate: decide (FSM, behaviour tree, utility), path (A*, navmesh, flow field), steer.

| Model | Use when |
|---|---|
| FSM | 2–5 clear states; explodes past 6–8 |
| Behaviour tree | Many behaviours with clear priorities (Sequence = AND, Selector = OR, decorators, blackboard) |
| Utility | Graded choices; multiply considerations, add about 0.05 hysteresis to the current action, pick among the top with softmax for variety |
| Hybrid | BT for structure, utility inside a selector |

Cost control: tick decisions at 5–15 Hz, time-slice agents into buckets, LOD by distance, push perception results onto the blackboard as events. Pathfinding: repath on a timer (0.5–1 s) or when blocked, never every frame; stuck timeout about 2 s; flow fields when many agents share one goal.

Roblox: `PathfindingService:CreatePath({AgentRadius = 2, AgentHeight = 5, AgentCanJump = true, AgentCanClimb = false, WaypointSpacing = 4, Costs = {...}})`; `Costs` maps materials or `PathfindingModifier` labels to multipliers (`math.huge` forbids). Listen to `Path.Blocked` and repath only when the blocked index is at or after the next waypoint. `Humanoid:MoveTo` fires `MoveToFinished` with `reached = false` after 8 s (treat as stuck). Call `rootPart:SetNetworkOwner(nil)` on server NPCs. Each `Humanoid` is expensive on the server; beyond a few dozen use `AnimationController` models moved by CFrame along precomputed waypoints, or simulate positions as data and let clients render pooled models. NPC models are Blender characters with simple collision hulls. Run each `ComputeAsync` in its own `task.spawn` with a repathing flag so one slow path does not stall the bucket.

## 6. Procedural generation

Rules: one seeded generator passed everywhere (`Random.new(seed)`, never `math.random` in generation); generate into data, validate, then build; flood-fill connectivity from start to exit; cap placement attempts with a fallback; seeds are version-fragile, so save generated results for saved worlds and ship your own PRNG for shareable seeds `[VS]`. Terrain from fBm (lacunarity 2, gain 0.5), power-curve redistribution, separate elevation and moisture seeds for biomes, island mask, Poisson-disc prop scatter. Dungeons: rooms and corridors with an MST plus extra loop edges, BSP, drunkard's walk, cellular automata (4-5 rule, double-buffered), Wave Function Collapse. Loot: weighted tables, shuffle bags or pity timers, scale by depth.

Roblox: `math.noise(x, y, z)` has no seed, so offset one coordinate by a seed-derived non-integer; it returns 0 at integer lattice points, so use non-integer frequencies. Generated levels assemble a kit of Blender modules snapped by `Attachment` sockets; primitive Parts are never generated. Roblox Terrain (`FillBlock`, `WriteVoxels`) is the engine's own system, not Parts, but under house rule 2 it still needs the owner's per-game approval; the default is Blender ground meshes. Generate on the server, or generate the same seed on every client for cosmetic-only scatter. Luck and Server Luck boosts apply as a documented multiplier on rare weights with the real odds shown; never change odds secretly.

## 7. Save systems (design level; DataStore detail in data-and-purchases.md)

Save data, not objects. Version every save and keep one migration function per step forever. Validate types and ranges on load; fall back to backup or defaults with a flag rather than wiping. Write atomically. Autosave at safe boundaries (purchase, checkpoint, leave), throttled. Store authoritative state and recompute derived state. Separate run state from profile state in roguelikes. Never trust the client's copy. A purchase receipt must be saved before `ProcessReceipt` returns `PurchaseGranted`.

## 8. Physics and performance (brief; detail in performance.md)

Fast objects tunnel: cap speed so `speed / step_rate` is below wall thickness. Mass does not change fall speed; tune "heavy" with gravity, drag and animation. Keep interacting mass ratios within about 1:10. Clamp `dt` spikes. Roblox: anchor everything static; set `CanTouch` and `CanQuery` false on decoration; cheapest `CollisionFidelity` that still feels solid (`Box` or `Hull` for most props, `PreciseConvexDecomposition` only where the shape truly matters); deliberate network ownership (server owns NPCs and shared objects); `StreamingEnabled` for large maps; reuse mesh IDs; `workspace:BulkMoveTo`; batch remote state at 10–20 Hz.
