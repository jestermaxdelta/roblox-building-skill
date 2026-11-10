# Game craft: feel, level design, camera, audio, AI, procgen, saves, physics

Distilled from knowledge-base sections 2.0 to 2.2, 2.4, 2.6 to 2.10, plus a 2026-11-10 research pass on game feel. Open it when building or auditing the feel of a verb, a level, the camera, audio, NPCs, generators or saves. UI design and input live in ui-input-crossplatform.md; the cost-ordered juice checklist and the loop scorecard live in core-loop-tuning.md. Deep dives on effects and sound are in vfx-and-juice.md and audio-sfx-music.md; this file keeps the rules a designer needs to tune feel. Tags: `[official]` Roblox docs, `[community]` forum or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; "reference project" = one anonymised production combat game; other figures are rules of thumb), `[VS]` version-sensitive, `[house]` house estimate. Four platform facts shape everything here: the server is authoritative and the client untrusted (rules on the server, juice on the client); the engine owns the game loop (hook `RunService` events); every device shares one server (design for a small landscape phone); players arrive mid-session from discovery (teach the verb in 30–60 s with no reading).

Art-direction guard against "AI slop" (from the asset pipeline source): describe the style along named axes (shape language, silhouette, value, colour, edge, material, light, detail density, camera, motion), approve one hero asset before producing families, and judge every asset at three distances (close, gameplay, far).

## Start here by level

Terms: **juice** = the small responses (flash, sound, shake, number) that make an action feel acknowledged. **Hit-stop** = a brief freeze of the attacker's animation on impact. **Trauma** = a 0–1 value that drives camera shake and decays over time. **Input buffer** = remembering a press for a fraction of a second so an early press still counts. **Coyote time** = allowing a jump shortly after leaving a ledge.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Every verb answers on the frame of the press with a visual, a sound and a number (§1). Use the default camera (§3). Spawn facing the first objective and keep jumps at or under the safe gap (§2). Give every UI action a sound (§4) | Custom cameras, hit-stop, behaviour trees, generators |
| Intermediate | Tier feedback by event size; add jump buffer and coyote time (§1.2); trauma-based shake with a slider; the reward sequence; pooled effects and a low-effects tier; a beat table per level; audio buses and ducking | Per-move stop budgets, FOV-scaled shake, sound onset trimming |
| Expert | One strength value driving stop, trauma and kick; flurry budgets; clock-timed flashes; cancel windows; onset and peak per combat sound; a frame-time governor with hysteresis; multi-target scaling; server tolerance for client forgiveness | — |

## 1. Game feel and juice

What the evidence says. `[official]` "Anytime a player takes an action in a game, it's imperative to provide clear feedback"; without it players wonder whether the action did anything or whether the game is bugged. The docs' examples are plain: a hit-reaction animation, button hover and press states, a "cha-ching" on purchase, a progress bar filling as quest objectives complete. `[community]` No measured Roblox data was found linking shake, particles or hit-stop to retention; polish threads list "juice" as a step without numbers, and general game-feel writing warns that effects should echo the core action and that shake and squash suit only some moments. So: make every verb, reward and goal legible first (tiers 0–1 of core-loop-tuning.md §8), add spectacle only where the event is big, and measure it behind a Config key rather than assuming.

A polished "hit" is a cluster of 5–8 small responses inside about 100 ms: target flash, hit-stop, camera shake, particle burst, sound, squash/scale pop, damage number, sometimes rumble. Everything returns to rest.

| Tier | Example | Particles | Extras | Hit-stop and shake |
|---|---|---|---|---|
| Small | coin pickup, footstep, light hit | 0–4 | sound, small pop | none |
| Medium | normal hit, door, level-up tick | 6–12 | 1–3 frame flash | from the hit's strength value: vfx-and-juice.md §7 |
| Large | kill, boss hit, explosion, rare drop | 20–40 | flash, brief zoom, big number | from the hit's strength value: vfx-and-juice.md §7 |

Hit-stop durations and trauma per hit are owned by vfx-and-juice.md §7 (one strength value per hit; light hits get no stop and no shake). Shake module behaviour: trauma 0–1 decaying 1.0–1.5/s, shake = trauma², driven by smooth noise (never per-frame random), max roll 0.05–0.12 rad and about 0.3–0.8 studs offset at third-person distance. Hit-stop timed on a real-time clock; only the newest hit-stop restores speed. Pop: scale 1.3 on one axis and 0.7 on the other, tween back over about 0.18 s with Back Out. Flash 1–3 frames. Damage numbers rise, fade, drift sideways.

Advanced tuning `[lihfolk]` (full treatment in vfx-and-juice.md):

- **Think in frames.** One frame is 33–40 ms on a hot phone, 17 ms at 60 fps, 4–8 ms on a fast PC. A stop shorter than two phone frames (about 66 ms) is seen only some of the time on weak devices: give stops that matter at least 66 ms and treat shorter ones as seasoning. Time a white flash on the real clock (about 33–50 ms, and at least one rendered frame): a count of rendered frames that reads at 30 fps is invisible at 240 fps (ruling in vfx-and-juice.md §7).
- **One strength value per hit** (for example 0.3 light to 1.3 ultimate) from which stop, trauma and directional kick are all derived, so weapons are tuned in data and never drift apart.
- **Budgets for fast weapons:** at most about 140 ms of hit-stop in any rolling 0.6 s, stop time under 15% of a move's length, visible shake under 10% of combat time. Rapid-fire weapons get per-shot recoil and save stops for kills.
- **Multi-target hits:** one stop per swing; strength is the maximum across targets, not the sum; trauma grows with the logarithm of the count (`× (1 + 0.35 × log2(n))`).
- **Shake is a fraction of the screen, and depends on FOV, not resolution.** One degree of rotation moves the image about 1.25% of screen height at FOV 70 and about 2.4% at FOV 40, so scale rotational shake by `tan(FOV / 2) / tan(35°)` when zoomed. At 30 fps keep the noise frequency under about 0.4 × the frame rate or shake aliases into jitter.
- **Where not to use them:** no hit-stop on the victim (it arrives late over the network and reads as lag) or on other players' attacks; no shake on a purchase button; nothing but a small kick under reduced motion.
- **Sound never leads the picture.** Sound 0–30 ms after the visual fuses with it; 80–150 ms late reads as input lag; 20 ms early feels wrong. Many effect files carry 30–80 ms of lead-in: trim reactive sounds to an onset under about 5 ms, start scheduled sounds early by their peak time, preload combat sounds so the first hit of a session is not silent, and pool about four voices per cue (audio-sfx-music.md).
- **Reward reveals are a time budget.** Common results take 0.3–0.5 s, rare 1–1.5 s, the top one or two tiers 5–6 s; each tier adds a layer instead of only getting louder, and whole channels (world dimming, hidden HUD, server-wide banner) are reserved for the top. Keep total reveal time under about 10% of an hour of play; give auto modes a compact reveal and a skip after first view. The server decides the result before any animation; reels show only reachable items; tells derive from the real result (house rule).
- **Scale with the device, with hysteresis:** drop an effects tier when average frame time exceeds 1.15× the target for 2 s, raise one after 10 s under 0.8×, ignore single spikes, never rise above the player's setting (performance.md).

The numbers (medium 50 ms and trauma 0.12 up to ultimate 89 ms and 0.60, and the ceiling allowed for isolated big moments) live in vfx-and-juice.md §7, with the `Conflict:` note on the older, larger knowledge-base values.

Easing: Back Out for pops, Quad/Cubic Out for settling, Cubic In for wind-ups, Sine InOut for camera and menus, Linear only for real-time progress bars.

Juice checklist per core verb (hit, jump, collect, buy, level up, die): same-frame visual at the point of action; a varied sound; camera reaction scaled to tier; UI reaction (counter pops and counts up, never snaps); anticipation and follow-through; everything returns to rest; effects pooled; accessibility (shake slider default 60–80%, reduce-flashing at most 3 flashes/s, reduce-motion option).

Anti-patterns: shaking the character instead of the camera; per-frame random shake; effects that outlive their cause; maximum juice on every event; juice that hides telegraphs.

Roblox mapping: `TweenService` with `Enum.EasingStyle.Back`; camera shake as an additive offset on `workspace.CurrentCamera.CFrame` removed before and re-added after the default camera step (`BindToRenderStep` at `Enum.RenderPriority.Camera.Value - 1` and `+ 1`), or `Humanoid.CameraOffset` for position-only; `ParticleEmitter` with `Enabled = false` and `emitter:Emit(count)`; `Trail` and `Beam`; `Highlight` (keep one per target and toggle `Enabled`; the client limit is 255 per current docs, previously 31 `[VS]`); `UIScale` tweens; hit-stop via `track:AdjustSpeed(0)` on the client only. Never fire one RemoteEvent per particle: send one event per gameplay fact ("hit at X, tier medium") and let the client build the cluster. Cap emitter counts on weak devices.

Reward sequence (the most repeated feedback in any progression game) `[house]`: the pickup pops and plays a pitch-varied sound in the same frame → an icon flies to its counter in 0.3–0.5 s → the counter counts up and pops → the goal bar advances with a tween → at 100% the bar chimes and the next goal appears within 1 s. Rarer rewards get a longer hold, a distinct sound and colour, never a longer wait before control returns.

Platform rules for effects:

- Client only. A server-side `TweenService` tween replicates the property to every client every frame, which is jittery and costs bandwidth `[official]`. Send one remote per gameplay fact; the client builds the cluster.
- Hit-stop changes animation speed on the client. It never pauses the server simulation or other players.
- In shared servers a player's own effects play in full; other players' effects are reduced and culled by distance, or big moments become unreadable and the frame rate falls.
- Budget on the 3 GB Android phone: pooled emitters, per-tier particle caps, a low-effects setting chosen automatically from frame time (performance.md).
- Haptics: `HapticEffect` gives waveform feedback on supported phones and gamepads `[official]` `[VS]`; use it for large-tier events only, with a setting to turn it off.

```lua
--!strict
-- Unexecuted sketch. Client module. Tier 0 reward feedback: counter pops and counts up, sound pitch varies.
local TweenService = game:GetService("TweenService")

local POP = TweenInfo.new(0.18, Enum.EasingStyle.Back, Enum.EasingDirection.Out)
local COUNT = TweenInfo.new(0.4, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
local rng = Random.new()

local function rewardPop(label: TextLabel, scale: UIScale, sound: AudioPlayer, from: number, to: number) -- AudioPlayer wired to the SFX fader
	scale.Scale = 1.3
	TweenService:Create(scale, POP, { Scale = 1 }):Play()
	sound.PlaybackSpeed = rng:NextNumber(0.94, 1.06) -- about one semitone either way
	sound:Play()

	local counter = Instance.new("NumberValue")
	counter.Value = from
	counter.Changed:Connect(function(value: number)
		label.Text = string.format("%d", math.floor(value + 0.5))
	end)
	local tween = TweenService:Create(counter, COUNT, { Value = to })
	tween.Completed:Once(function()
		counter:Destroy()
	end)
	tween:Play()
end
return rewardPop
```

Level-up: feel symptoms → likely cause → fix.

| Symptom | Likely cause | Fix |
|---|---|---|
| "Feels cheap" or "dead" in feedback; the verb is dull with reward UI hidden | No same-frame response; silent UI | Tier 0 on verb and reward: sound, pop, number |
| Players miss drops or leave rewards unclaimed | Reward feedback is off-screen or identical to routine events | Fly-to-counter, rarity-scaled sound and colour, goal-bar chime |
| Frame rate dips on phones at big moments | Unpooled emitters, uncapped particles or highlights | Pool, cap by device tier, low-effects setting |
| Effects stutter or arrive late | Server-driven tweens, one remote per effect | Client tweens; one remote per gameplay fact |
| Motion or nausea complaints | Per-frame random shake, no slider, large FOV swings | Trauma² with noise, slider default 60–80%, reduce-motion option |
| Combat feels floaty | Feedback waits for the server; no anticipation or hit-stop | Predicted local feedback under 80 ms, 0.04–0.06 s hit-stop, wind-up frames |
| Everything is loud all the time | Maximum juice on every event | Scale by tier; let things return to rest |
| Big moments unreadable in full servers | Everyone's effects at full strength | Own effects full, others' reduced and distance-culled |

### 1.2 Input responsiveness: budget, buffering, cancel windows, coyote time `[lihfolk]`

Most "this feels bad" reports are about input, not effects: a jump that did not fire at a ledge, an early attack that was swallowed, a button that reacts on finger-up.

| What the player perceives | Target |
|---|---|
| Something reacts to the press (pose shift, button state, sound) | Within 1–2 frames of the input being read (under about 35 ms at 60 fps) |
| The action is clearly under way | Within about 100 ms |
| The outcome (hit, damage, reward) | When the design says; hundreds of ms is fine if the first two are met |

First-frame rule: every press shows something on the frame it is read, even when the action must wait. A move on cooldown plays a small "denied" tick; a server-validated action starts its anticipation at once and the result follows the reply. The worst offender is `InvokeServer` in an input handler before any animation: at 150 ms round trip that is 150 ms of nothing. Local presentation first, server confirmation second (networking-and-security.md).

| Action | Buffer window | Note |
|---|---|---|
| Jump before landing | 0.10–0.15 s | Longer feels like a jump nobody pressed |
| Light attack in a combo | 0.15–0.30 s | Players mash; too short drops combos, too long fires after they stopped |
| Dodge or roll, ability | 0.10–0.20 s | Must feel immediate |
| Interact, menu toggles | None, or 0.1 s | A late interaction on the wrong target is worse than a missed press |

Buffer rules: record on press, never on release (a release trails the press by 50–150 ms); a buffered press fires once, then is gone; when several are waiting, defensive actions outrank offensive ones; the latest direction wins; death, stun, menus and cutscenes clear the buffer; hit-stop must not eat the window (pause its ageing during a stop, or make it longer than the longest stop).

Cancel windows: a light attack is roughly 20–30% wind-up, 10–20% active frames and 50–70% recovery. Recovery is where feel lives: allow the next combo hit at the link point and a dodge shortly after the active frames (a 0.1–0.15 s lock), with a 0.05–0.1 s animation fade so the cancel does not pop.

Coyote time on the default Humanoid (0.08–0.15 s): once the Humanoid is in `Freefall`, setting `Humanoid.Jump` does nothing, so the forgiving jump is forced with `Humanoid:ChangeState(Enum.HumanoidStateType.Jumping)` (community practice, not a documented guarantee: test it on your rig `[VS]`). Do not grant it after a jump, a knockback or launch, a dash, or while stunned. Brief `Freefall` on stairs is covered for free. Server-side movement checks need a tolerance for it, or your own forgiveness is flagged as an exploit.

```lua
--!strict
-- Unexecuted sketch. LocalScript under StarterCharacterScripts. Coyote time plus jump buffering on the default Humanoid.
local UserInputService = game:GetService("UserInputService")

local COYOTE, BUFFER = 0.1, 0.12
local character = script.Parent :: Model
local humanoid = character:WaitForChild("Humanoid") :: Humanoid
local leftGroundAt, pressedAt, jumped = -math.huge, -math.huge, false

local function blocked(): boolean
	return humanoid.Health <= 0 or character:GetAttribute("Launched") == true or character:GetAttribute("Stunned") == true
end

humanoid.StateChanged:Connect(function(_old: Enum.HumanoidStateType, new: Enum.HumanoidStateType)
	if new == Enum.HumanoidStateType.Jumping then
		jumped = true
	elseif new == Enum.HumanoidStateType.Freefall then
		if not jumped then
			leftGroundAt = os.clock() -- walked off a ledge: the coyote window opens
		end
	elseif new == Enum.HumanoidStateType.Landed or new == Enum.HumanoidStateType.Running then
		jumped = false
		leftGroundAt = -math.huge
		if os.clock() - pressedAt <= BUFFER and not blocked() then
			pressedAt = -math.huge
			task.defer(function() -- after the state change has finished
				humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
			end)
		end
	end
end)

UserInputService.JumpRequest:Connect(function()
	local now = os.clock()
	if humanoid:GetState() ~= Enum.HumanoidStateType.Freefall then
		return -- grounded: the default controls already jump
	end
	if not jumped and now - leftGroundAt <= COYOTE and not blocked() then
		jumped = true
		humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
	else
		pressedAt = now -- remember the press for the landing (test a held jump key: the default controls also re-jump)
	end
end)
```

```lua
--!strict
-- Unexecuted sketch. LocalScript module. Trauma-based camera shake that never accumulates.
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

Roblox defaults `[VS]`: `WalkSpeed` 16 studs/s, `JumpPower` 50, `JumpHeight` 7.2 studs, `MaxSlopeAngle` 89°, `workspace.Gravity` 196.2. Which jump property applies depends on `UseJumpPower`; check StarterPlayer in your place. Derived: JumpPower 50 gives about 6.37 studs height, 0.51 s air time, 8.2 studs running jump, safe gap 5.7, hard gap 7.8; JumpHeight 7.2 gives 8.7 / 6.1 / 8.2. R15 is about 5 studs tall (pathfinding `AgentHeight` 5, `AgentRadius` 2). Gameplay doors at least 5 wide and 7.5–8 tall, 6+ wide where two players pass (level-design-worldbuilding.md); multiplayer corridors 8+ wide; a comfortable ledge is about 80% of jump height (about 5 studs). Thumbsticks can move slower than `WalkSpeed`; design for keyboard, test on a stick. Disable jumping with `Humanoid:SetStateEnabled(Enum.HumanoidStateType.Jumping, false)`, not power 0. Keep metrics in one `LevelMetrics` module so designers and generators share them.

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

Roblox `[VS]`: the audio graph is the default for new games: `AudioPlayer` → `Wire` → `AudioFader`/`AudioEqualizer`/`AudioCompressor` (Input and Sidechain pins)/`AudioReverb`/`AudioLimiter` → `AudioDeviceOutput`, or `AudioEmitter`/`AudioListener` for 3D. `Sound` and `SoundGroup` (with `CompressorSoundEffect.SideChain`, `SoundService:PlayLocalSound`) are legacy: keep them in a live game that works, and migrate one bus at a time. The two systems are separate mixes. API detail, bus wiring and the migration table are in audio-sfx-music.md. Use `RollOffMinDistance`/`RollOffMaxDistance` with `InverseTapered`. Audio asset permissions can make a sound play silently `[VS]`. Clone per play only for low-rate sounds; pool high-rate ones.

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

## Review gate

- [ ] Every core verb, reward and goal has a same-frame visual, a varied sound and a UI reaction (juice tiers 0–1) before any tier 2–3 work.
- [ ] Effects are tiered by event size, return to rest, and never hide a telegraph.
- [ ] All effects run on the client from one remote per gameplay fact; no server-side tweens on visible objects.
- [ ] Shake slider, reduce-flashing and reduce-motion options exist if shake, flashes or FOV changes are used.
- [ ] Every press shows a response on the frame it is read; nothing waits for the server before local feedback; jump buffer and coyote time in any game with platforming; attack buffers consume once and clear on stun or death.
- [ ] Stops that matter are at least 66 ms; fast weapons respect the stop budget; no stop or shake on light hits, victims or other players' attacks; sound never plays before its visual.
- [ ] Effects pooled and capped; frame rate checked on a 3 GB Android phone during the largest event.
- [ ] Movement metrics derived and stored in one module; critical gaps at or below the safe gap; soft-lock check passes.
- [ ] Spawn faces the first objective; next objective visible from every checkpoint.
- [ ] Camera smoothing is frame-rate independent; drag-heavy UI is off the right side on phones.
- [ ] Audio buses, loudness targets and polyphony caps set; rarer rewards sound better.
- [ ] NPC decisions ticked at 5–15 Hz with repath limits; generators seeded, validated and built from Blender modules.
- [ ] Saves versioned, validated on load, never trusted from the client.

## Sources

Accessed 2026-11-10. "(read)" = opened in the `Roblox/creator-docs` mirror at commit ccc2b01; "(search summary)" = seen only through web search result text. Sections 2–8 come from `references/knowledge-base.md` sections 2.0–2.2, 2.4 and 2.6–2.10 (grep `## 2.1`, `## 2.2`, `## 2.4`, `## 2.6` to `## 2.10`), which list their own sources.

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/onboarding-techniques.md (read; feedback section)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/ui-ux-design.md (read; feedback section)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/performance-optimization/improve.md (read; server-side TweenService replication)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/HapticEffect.yaml (read)
- https://devforum.roblox.com/t/real-game-feel-and-execution-on-roblox/4199862 (search summary; a question with no answers shown)
- https://devforum.roblox.com/t/how-to-polish-game/3244775 (search summary)
- https://gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design- (search summary; general, not Roblox-specific)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/47 Game Feel and Juice/Input Responsiveness Buffering and Coyote Time.md`, `…/Hit-Stop and Screen Shake Tuning by Numbers.md`, `…/Feedback Timing - Sound Visual and Haptic Sync.md`, `…/Reward Moments and Celebrations.md`, `…/Juice on a Budget - Mobile and Low-End.md` (read). Ideas and figures adapted and rewritten; the code is our own.
