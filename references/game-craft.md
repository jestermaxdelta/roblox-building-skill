# Game craft: input feel, game camera, AI, procgen, save design

What this is: the design-level guide to how a verb responds (feedback tiers, input budget, buffering, coyote time), the gameplay camera and its shake module, NPC decision-making and pathfinding, seeded generation, and save design. Open it when a verb feels late or dead, when building a camera, an enemy, a generator or a save format. It also keeps the jump-metric derivation, pacing beat table and soft-lock check that `level-design-worldbuilding.md` points to.

Tags: `[official]` Roblox docs, `[community]` forum or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; "reference project" = one anonymised production combat game; other figures are rules of thumb), `[VS]` version-sensitive, `[house]` house estimate. Platform facts behind every rule here: the server is authoritative and the client untrusted (rules on the server, feedback on the client); every device shares one server (design for a small landscape phone); players arrive mid-session from discovery (teach the verb in 30–60 s with no reading).

| Not in this file | Owner |
|---|---|
| Hit-stop, trauma, kick and FOV numbers; effects; budgets | `vfx-and-juice.md` §6, §7, §11; builds in `vfx-recipes.md` |
| UI pops, count-ups, fly-to-counter, reward reveal length by tier | `ui-motion-and-feedback.md` §2, §5 |
| Sound timing, variation, buses, loudness, ducking, music | `audio-sfx-music.md` |
| Cutscene and scripted cameras, shots, skip | `cutscenes-and-cinematics.md` |
| Teaching the verb, first minute, guidance devices | `tutorial-and-onboarding.md` |
| Map layout, scale table, spawn area, wayfinding, blockout | `level-design-worldbuilding.md` |
| Style bible, hero-asset-first and three-distance rules, art review | `art-direction-and-quality-bar.md` §6, §8 |
| Shake, flash and motion settings; reduced motion | `accessibility-and-player-qol.md` §5, §10 |
| Juice ordered by build cost; loop scorecard | `core-loop-tuning.md` §8 |
| UI layout and input devices | `ui-input-crossplatform.md` |

## Start here by level

Terms: **juice** = the small responses (flash, sound, shake, number) that acknowledge an action. **Hit-stop** = a brief freeze of the attacker's animation on impact. **Trauma** = a 0–1 value that drives camera shake and decays. **Input buffer** = remembering a press briefly so an early press still counts. **Coyote time** = allowing a jump shortly after leaving a ledge. **FSM** = finite-state machine.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Every verb answers on the frame of the press with a visual, a sound and a number (§1). Keep the default camera (§3). Keep critical jumps at or under the safe gap (§2). NPCs: a 3-state FSM and `PathfindingService` (§5) | Custom cameras, hit-stop, behaviour trees, generators |
| Intermediate | Tier feedback by event size (§1); jump buffer and coyote time (§1.2); the shake module with a slider (§1.3); a beat table per level (§2); frame-rate-independent camera smoothing (§3); versioned saves (§7) | Cancel windows, utility AI, shareable seeds |
| Expert | Buffer priorities and cancel windows per move; server tolerance for client forgiveness; time-sliced AI with distance LOD; generators that validate before building; one migration function per save version | — |

## 1. Game feel: tiers, reward sequence, platform rules

Evidence. `[official]` "Anytime a player takes an action in a game, it's imperative to provide clear feedback"; otherwise players wonder whether the action did anything or the game is buggy. The docs' examples are plain: a hit reaction, button hover and press states, a "cha-ching" on purchase. `[community]` No measured Roblox data was found linking shake, particles or hit-stop to retention; general game-feel writing says juice should echo the core action and that shake and squash suit only fast, dynamic games. So: make every verb, reward and goal legible first (tiers 0–1 of `core-loop-tuning.md` §8), add spectacle only where the event is big, and measure it behind a Config key.

A polished hit is a cluster of 5–8 small responses inside about 100 ms (target flash, hit-stop, shake, particle burst, sound, pop, damage number, sometimes rumble) that all return to rest. Scale the cluster to the event:

| Tier | Example | Particles | Extras | Hit-stop and shake |
|---|---|---|---|---|
| Small | coin pickup, footstep, light hit | 0–4 | sound, small pop | none |
| Medium | normal hit, door, level-up tick | 6–12 | 1–3 frame flash | from the hit's strength value: `vfx-and-juice.md` §7 |
| Large | kill, boss hit, explosion, rare drop | 20–40 | flash, brief zoom, big number | from the hit's strength value: `vfx-and-juice.md` §7 |

Checklist per core verb (hit, jump, collect, buy, level up, die): same-frame visual at the point of action; a varied sound; camera reaction scaled to tier; UI reaction (counters count up, never snap); anticipation and follow-through; everything returns to rest; effects pooled; comfort settings exist (`accessibility-and-player-qol.md` §5).

Reward sequence, the most repeated feedback in a progression game `[house]`: the pickup pops and plays a pitch-varied sound in the same frame → an icon flies to its counter → the counter counts up and pops → the goal bar advances with a tween → at 100% the bar chimes and the next goal appears within 1 s. Rarer rewards get a longer hold, a distinct sound and colour, never a longer wait before control returns. Timings, pop scale and reveal length by tier: `ui-motion-and-feedback.md` §5.

Platform rules:

- **Client only.** A server-side `TweenService` tween replicates the property to every client every frame: jittery, and wasted bandwidth `[official]`. Send one remote per gameplay fact ("hit at X, tier medium"); the client builds the cluster. Never one remote per particle.
- **Hit-stop changes animation speed on the attacker's client.** It never pauses the server or other players, and never plays on the victim (it arrives late and reads as lag) `[lihfolk]`.
- **Own effects in full, others' reduced** and culled by distance, or big moments become unreadable in a full server (`vfx-and-juice.md` §11).
- **Sound never leads the picture** (`audio-sfx-music.md` §5).
- **Haptics:** `HapticEffect` gives waveform feedback on supported phones and gamepads `[official]` `[VS]`; large-tier events only, with a setting to turn it off.
- Anti-patterns: shaking the character instead of the camera; per-frame random shake; effects that outlive their cause; maximum juice on every event; juice that hides a telegraph; shake on a purchase button.

| Symptom | Likely cause | Fix |
|---|---|---|
| "Feels cheap" or "dead"; the verb is dull with reward UI hidden | No same-frame response; silent UI | Tier 0 on verb and reward: sound, pop, number |
| Players miss drops or leave rewards unclaimed | Reward feedback off-screen or identical to routine events | Fly-to-counter, rarity-scaled sound and colour, goal-bar chime |
| Effects stutter or arrive late | Server-driven tweens, one remote per effect | Client tweens; one remote per gameplay fact |
| Combat feels floaty | Feedback waits for the server; no anticipation or hit-stop | Local feedback on the input frame (§1.2); hit-stop from `vfx-and-juice.md` §7; wind-up frames (`animation-and-rigs.md`) |
| Everything is loud all the time | Maximum juice on every event | Scale by tier; return to rest |
| Motion or nausea complaints | Per-frame random shake, roll, no slider, large FOV swings | §1.3 module; `accessibility-and-player-qol.md` §5 |

### 1.2 Input responsiveness: budget, buffering, cancel windows, coyote time `[lihfolk]`

Most "this feels bad" reports are about input, not effects: a jump that did not fire at a ledge, an early attack that was swallowed, a button that reacts on finger-up.

| What the player perceives | Target |
|---|---|
| The press gets a reaction (sound, button state, pose shift) | No later than 1–2 frames after the input is read; at 60 fps under about 35 ms |
| The action is clearly under way | Within about 100 ms |
| The outcome (hit, damage, reward) | When the design says; hundreds of ms is fine if the first two are met |

First-frame rule: every press shows something on the frame it is read, even when the action must wait. A move on cooldown plays a small "denied" tick; a server-validated action starts its anticipation at once and the result follows the reply. The worst offender is an input handler that calls `InvokeServer` before any animation: a 150 ms round trip is 150 ms of nothing. Local presentation first, server confirmation second (`networking-and-security.md`).

| Action | Buffer window | Note |
|---|---|---|
| Jump before landing | 0.10–0.15 s | Longer feels like a jump nobody pressed |
| Next attack in a combo | 0.15–0.20 s; never above 0.30 s | One press only. Under 0.10 s drops clicks; above 0.30 s a nervous double-click commits two swings |
| Dodge or roll, ability | 0.10–0.20 s | Must feel immediate |
| Interact, menu toggles | None, or 0.1 s for interact | A late interaction on the wrong target is worse than a missed press |

The combo window is one number, not two: LihFolk's input note gives 0.15–0.30 s and its combo note 0.10–0.20 s with 0.15 s in code; start at 0.15 s and use the top of the range only when buffer ageing is not paused during hit-stop. The `CancelOpen` buffer in `animation-and-rigs.md` and the fighting-genre buffer are this same window.

Buffer rules: record on press, never on release (a release trails the press by 50–150 ms); a buffered press fires once, then is gone; when several are waiting, defensive actions outrank offensive ones; the latest direction wins; death, stun, menus and cutscenes clear the buffer; pause buffer ageing during hit-stop, or make the window longer than the longest stop (89 ms).

Cancel windows: a light attack is roughly 20–30% wind-up, 10–20% active frames and 50–70% recovery. Recovery is where feel lives: allow the next combo hit at the link point and a dodge shortly after the active frames (a 0.1–0.15 s lock), with a 0.05–0.1 s animation fade so the cancel does not pop. A strict server cooldown rejects presses the client buffered to the exact frame: give it a small grace (about 50 ms, `vfx-and-juice.md` §10).

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

-- JumpRequest fires several times per press and repeatedly while held [official]; the flags below make that harmless.
UserInputService.JumpRequest:Connect(function()
	local now = os.clock()
	if humanoid:GetState() ~= Enum.HumanoidStateType.Freefall then
		return -- grounded: the default controls already jump
	end
	if not jumped and now - leftGroundAt <= COYOTE and not blocked() then
		jumped = true
		humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
	else
		pressedAt = now -- remember the press for the landing (a held key re-jumps on landing, as the default controls do)
	end
end)
```

### 1.3 Shake module

Values per hit (how much trauma to add, when, and for whom) are owned by `vfx-and-juice.md` §7. The module's behaviour: trauma 0–1 decays at 1.0–1.5 per second; shake = trauma²; motion comes from smooth noise, never per-frame random; **pitch and yaw only, no roll** (roll is the strongest nausea trigger; `accessibility-and-player-qol.md` §5); the user's shake setting and reduced motion scale the result once, here, where offsets are summed. The offset is removed before the default camera step and re-applied after it, so it never accumulates and never moves the player's aim. `Humanoid.CameraOffset` is the simpler position-only alternative.

```lua
--!strict
-- Unexecuted sketch. Client module. Trauma-based camera shake that never accumulates and never rolls.
local RunService = game:GetService("RunService")
local Shake = { userScale = 1 } -- set from the comfort resolver's `shake` output (accessibility-and-player-qol.md §10), never from the raw setting
local trauma, DECAY, FREQ = 0, 1.2, 12 -- 12 Hz stays under 0.4 x frame rate at 30 FPS (vfx-and-juice.md §7)
local MAX_ANGLE, MAX_OFFSET = math.rad(2), 0.5 -- radians of pitch/yaw and studs at trauma 1
local applied = CFrame.identity

local function noise(t: number, seed: number): number
	return math.clamp(math.noise(t, seed) * 2, -1, 1) -- math.noise stays within about -0.5..0.5
end

function Shake.add(amount: number)
	trauma = math.min(1, trauma + amount)
end

RunService:BindToRenderStep("ShakeUndo", Enum.RenderPriority.Camera.Value - 1, function()
	local camera = workspace.CurrentCamera
	camera.CFrame = camera.CFrame * applied:Inverse()
	applied = CFrame.identity
end)
RunService:BindToRenderStep("ShakeApply", Enum.RenderPriority.Camera.Value + 1, function(dt: number)
	if trauma <= 0 then return end
	trauma = math.max(0, trauma - DECAY * dt)
	local s, t = trauma * trauma * Shake.userScale, os.clock() * FREQ
	applied = CFrame.new(MAX_OFFSET * s * noise(t, 13.6), MAX_OFFSET * s * noise(t, 21.4), 0)
		* CFrame.Angles(MAX_ANGLE * s * noise(t, 0.31), MAX_ANGLE * s * noise(t, 4.73), 0)
	local camera = workspace.CurrentCamera
	camera.CFrame = camera.CFrame * applied
end)
return Shake
```

## 2. Level metrics, pacing and soft-locks

Layout, scale table, spawn area, wayfinding, blockout and dressing are in `level-design-worldbuilding.md`; obby stage rules in `genres/obby-tower.md`. This section keeps the three things those guides point here for.

**Jump metrics.** Derive before blocking out: `MAX_JUMP_HEIGHT = v²/(2g)`, `AIR_TIME = 2v/g`, `MAX_JUMP_DISTANCE = run_speed × AIR_TIME`, `SAFE_GAP = 0.7 × MAX_JUMP_DISTANCE` (critical path), `HARD_GAP = 0.95 ×` (optional or expert). Confirm with a measured gap ladder on every device type.

| Defaults `[official]`: `WalkSpeed` 16, `Workspace.Gravity` 196.2, and | Height | Air time | Running jump | Safe gap | Hard gap |
|---|---|---|---|---|---|
| `JumpPower` 50 (`UseJumpPower = true`, the documented default) | 6.4 | 0.51 s | 8.2 | 5.7 | 7.8 |
| `JumpHeight` 7.2 (`UseJumpPower = false`) | 7.2 | 0.54 s | 8.7 | 6.1 | 8.2 |

Check `StarterPlayer.CharacterUseJumpPower` in your place: it decides which row applies `[VS]`. `MaxSlopeAngle` defaults to 89°. A comfortable ledge is about 80% of jump height (about 5 studs). Thumbsticks can move slower than `WalkSpeed` `[official]`: design for keyboard, test on a stick. Disable jumping with `Humanoid:SetStateEnabled(Enum.HumanoidStateType.Jumping, false)`, not power 0 `[official]`. Keep metrics in one `LevelMetrics` module so designers and generators share them.

**Pacing.** Three paths: critical (minimum route), golden (the intended best-feeling route past the views and teaching moments), branches (secrets, shortcuts). Intensity follows a sawtooth with a rest before every climax; plan it as a beat table (segment, beat type, intensity 1–5, what it teaches or tests). Per mechanic: introduce safely → develop → twist → test without help (`tutorial-and-onboarding.md` §3).

**Gating and the soft-lock check.** Gates: lock and key, ability gate, one-way drop (always telegraphed), soft gate. Check: grow the reachable set from spawn with held keys and abilities until nothing changes; the goal must be in the final set. Automate it for generated levels (§6).

**Spawn and kill-zone pattern** (house rules 1 and 2): an invisible `SpawnLocation` inside a Blender pad that carries the visible collision; a kill zone is a Blender lava or spike model with real collision plus an invisible non-colliding trigger for `Touched`. Placement rules: `level-design-worldbuilding.md` §4.

## 3. Gameplay camera

Scripted and cutscene cameras are in `cutscenes-and-cinematics.md` §5 and §7. For the camera the player plays through:

- **Start from the default.** The `PlayerModule` camera already gives orbit, zoom, occlusion handling and mouse lock; replace it only when the genre needs it. Mobile players rotate by dragging the right side of the screen, so keep drag-heavy UI off it.
- **Properties** `[official]` `[VS]`: `Camera.FieldOfView` defaults to 70 and clamps to 1–120; `StarterPlayer.CameraMinZoomDistance`/`CameraMaxZoomDistance` (the docs state no default: read the value in StarterPlayer and set it deliberately; conflict note in `level-design-worldbuilding.md` §2); `StarterPlayer.CameraMode`; `Humanoid.CameraOffset`. `EnableMouseLockOption` still toggles shift-lock, but the docs say shift-lock APIs are being deprecated in favour of `UserInputService.MouseBehavior`.
- **Custom camera:** set `CameraType = Scriptable` and drive `Camera.CFrame` in `BindToRenderStep` at `Enum.RenderPriority.Camera.Value` (200), after the target has moved.
- **Smoothing is frame-rate independent:** `alpha = 1 - exp(-rate * dt)`, `pos = lerp(pos, target, alpha)`, rate 5–12 per second; or `TweenService:SmoothDamp` (`vfx-and-juice.md` §9). Reset smoothing on teleport and respawn.
- **Framing:** a deadzone for small movement; look-ahead eased over 0.2–0.4 s; clamp the view, not the centre; platformers follow vertical lazily. Orbit cameras clamp pitch to about −80° to +45°; a spring arm raycasts from the target to the desired position.
- **Order each frame:** follow → collision → shake and kicks last (§1.3). One module owns `FieldOfView` (`vfx-and-juice.md` §7); FOV changes over about 10–15° need a reduce-motion path.

## 4. Audio

Owned by `audio-sfx-music.md`: systems and wiring (§1–2), SFX timing and variation (§5), buses, loudness, ducking and voice limits (§6), music (§8), UI sounds (§9), settings (§11). Design rules that belong to feel: every UI action and gameplay verb gets a sound; rewards sound better as they get rarer; a sound 0–30 ms after its picture fuses with it and one that leads it feels wrong.

## 5. Game AI

Fun beats smart: telegraph attacks, react with a 0.2–0.5 s delay, miss sometimes, take turns, show state. Keep three layers separate: decide (FSM, behaviour tree, utility), path (A*, navmesh, flow field), steer.

| Model | Use when |
|---|---|
| FSM | 2–5 clear states; unmanageable past 6–8 |
| Behaviour tree | Many behaviours with clear priorities (Sequence = AND, Selector = OR, decorators, blackboard) |
| Utility | Graded choices: multiply considerations, add about 0.05 hysteresis to the current action, pick among the top with softmax for variety |
| Hybrid | Behaviour tree for structure, utility inside a selector |

Cost control: tick decisions at 5–15 Hz, time-slice agents into buckets, reduce tick rate by distance, push perception results onto the blackboard as events. Repath on a timer (0.5–1 s) or when blocked, never every frame; stuck timeout about 2 s; flow fields when many agents share one goal.

Roblox `[official]`:

- `PathfindingService:CreatePath({ AgentRadius = 2, AgentHeight = 5, AgentCanJump = true, AgentCanClimb = false, WaypointSpacing = 4, Costs = {...} })` (the values shown are the defaults); `Costs` maps materials or `PathfindingModifier` labels to multipliers (`math.huge` forbids).
- `Path:ComputeAsync` yields: run each in its own `task.spawn` behind a repathing flag so one slow path does not stall the bucket.
- `Path.Blocked` also fires for blockages behind the agent: repath only when the blocked index is at or after the next waypoint.
- `Humanoid:MoveTo` times out after 8 s and fires `MoveToFinished` with `reached = false`: treat that as stuck, or re-issue `MoveTo` on long legs.
- Call `rootPart:SetNetworkOwner(nil)` on server NPCs.
- Each `Humanoid` is expensive on the server. Beyond a few dozen, use `AnimationController` models moved by CFrame along precomputed waypoints, or simulate positions as data and let clients render pooled models `[community]`. NPC models are Blender characters with simple collision hulls.

## 6. Procedural generation

Rules: one seeded generator passed everywhere (`Random.new(seed)`, never `math.random` in generation); generate into data, validate, then build; flood-fill connectivity from start to exit plus the §2 soft-lock check; cap placement attempts with a fallback; seeds are version-fragile, so save generated results for saved worlds and ship your own PRNG for shareable seeds `[VS]`.

Methods: terrain from fBm (lacunarity 2, gain 0.5) with power-curve redistribution, separate elevation and moisture seeds for biomes, an island mask, Poisson-disc prop scatter. Dungeons: rooms and corridors with a minimum spanning tree plus extra loop edges, BSP, drunkard's walk, cellular automata (4-5 rule, double-buffered), Wave Function Collapse. Loot: weighted tables, shuffle bags or pity timers, scaled by depth.

Roblox: `math.noise(x, y, z)` has no seed, so offset one coordinate by a seed-derived non-integer; it returns 0 when all inputs are integers and otherwise stays within about −0.5 to 0.5 `[official]`, so use non-integer frequencies and rescale. Generated levels assemble Blender kit modules snapped by `Attachment` sockets (`level-design-worldbuilding.md` §14); primitive Parts are never generated. Roblox Terrain (`FillBlock`, `WriteVoxels`) is the engine's own system, not Parts, but under house rule 2 it needs the owner's per-game approval; the default is Blender ground meshes. Generate on the server, or generate the same seed on every client for cosmetic-only scatter. Luck boosts apply as a documented multiplier on rare weights with the real odds shown; never change odds secretly (`monetization-and-policy.md`).

## 7. Save design (DataStore detail in `data-and-purchases.md`)

- Save data, not objects. Store authoritative state and recompute derived state.
- Version every save; keep one migration function per version step forever.
- Validate types and ranges on load; fall back to a backup or defaults with a flag, never a silent wipe.
- Autosave at safe boundaries (purchase, checkpoint, leave), throttled.
- Separate run state from profile state in roguelikes.
- Never trust the client's copy.
- A purchase is saved before `ProcessReceipt` returns `PurchaseGranted`.

## 8. Physics rules of thumb (detail in `performance.md`, `physics-and-vehicles.md`)

Fast objects tunnel: cap speed so `speed / step_rate` is below wall thickness. Mass does not change fall speed; tune "heavy" with gravity, drag and animation. Keep interacting mass ratios within about 1:10. Clamp `dt` spikes. Anchor everything static; `CanTouch` and `CanQuery` false on decoration; server owns NPCs and shared objects.

## Review gate

- [ ] Every core verb, reward and goal has a same-frame visual, a varied sound and a UI reaction before any shake, hit-stop or FOV work; effects are tiered by event size and none hides a telegraph.
- [ ] All feedback is built on the client from one remote per gameplay fact; no server-side tween on a visible object.
- [ ] No input handler waits for the server before showing a response; a press on cooldown shows a "denied" tick.
- [ ] Buffers: jump 0.10–0.15 s, combo 0.15–0.20 s, one press, recorded on press, cleared on stun, death, menu and cutscene; ageing paused during hit-stop.
- [ ] Coyote time (0.08–0.15 s) and jump buffer exist in any game with platforming; server movement checks tolerate them.
- [ ] Shake comes from the one module in §1.3: no roll, scaled by the player's setting, zero under reduced motion; values match `vfx-and-juice.md` §7.
- [ ] Movement metrics derived for the place's jump mode and stored in one module; critical gaps at or below the safe gap; soft-lock check passes; each level has a beat table.
- [ ] Camera smoothing uses `1 - exp(-rate * dt)` or `SmoothDamp`; smoothing resets on teleport; one owner of `FieldOfView`; drag-heavy UI is off the right side on phones.
- [ ] NPC decisions tick at 5–15 Hz in buckets; repath on a timer or `Path.Blocked` ahead of the agent; server NPCs have network owner `nil`.
- [ ] Generators take one `Random.new(seed)`, validate data before building, and place only Blender modules.
- [ ] Saves are versioned, validated on load, never read from the client; receipts saved before `PurchaseGranted`.

## Sources

Accessed 2026-11-10; re-checked 2026-11-11. "(read)" = opened; docs paths are in the `Roblox/creator-docs` mirror at commit 7cbffff. Sections 2, 3 and 5–8 were distilled from `references/knowledge-base.md` sections 2.0–2.2, 2.4 and 2.7–2.10 (grep `## 2.2`, `## 2.4`, `## 2.7`), which list their own sources; their engine facts were re-checked against the class reference below.

- `content/en-us/production/game-design/onboarding-techniques.md`, `ui-ux-design.md` (read; feedback sections) · `performance-optimization/improve.md` (read; server-side TweenService replication) https://github.com/Roblox/creator-docs
- Class reference (read): `Humanoid` (WalkSpeed, JumpPower, JumpHeight, UseJumpPower, MaxSlopeAngle, CameraOffset, MoveTo, ChangeState), `StarterPlayer`, `Workspace.Gravity`, `Camera.FieldOfView`, `UserInputService.JumpRequest`, `PathfindingService:CreatePath`, `Path`, `HapticEffect`, `TweenService:SmoothDamp`, `Enum.RenderPriority`, `math.noise`; `characters/pathfinding.md` (blocked-path sample).
- https://devforum.roblox.com/t/4199862 (read; a question on game feel with no replies) · https://devforum.roblox.com/t/3244775 (read; "add juice" listed as a polish step, no numbers)
- https://www.gamedeveloper.com/design/squeezing-more-juice-out-of-your-game-design- (read; general, not Roblox-specific: juice should echo the core gameplay)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault) (read): `47 Game Feel and Juice/Input Responsiveness Buffering and Coyote Time.md`, `08 Animation/05 Systems/Combat Combo Systems.md` (the second buffer range), `08 Animation/05 Systems/Camera Shake and Camera FX.md`, `42 Accessibility and Inclusive Design/Motion Sensitivity and Camera Comfort.md`. Ideas and figures adapted and rewritten; the code is our own.
- Not verified: that `ChangeState(Jumping)` works from `Freefall` on every rig (community practice); the AI, procgen and physics rules of thumb are general game-development practice carried over from the knowledge base without a Roblox-specific source.
