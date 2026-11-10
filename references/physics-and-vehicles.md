# Physics and vehicles

What this is: how Roblox simulates and replicates physics, and how to build characters, platforms, ragdolls, projectiles and vehicles on top of it without flinging, jitter or exploits. Open it when a design includes anything unanchored, or when a live game has physics bugs, laggy vehicles or movement cheats (jump to "Level-up"). Collision fidelity per asset type, sleep thresholds and query rules are in performance.md; the threat model, server authority mode and the suspicion ladder are in networking-and-security.md; this file does not repeat them. Snippets are unexecuted sketches. Tags: `[official]`, `[community]`, `[VS]` version-sensitive, `[house]`, `[lihfolk]` adapted from LihFolk Vault V2.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | Anchor everything that should not move. Learn the two questions (section 1). Give every moving thing one mover and one owner. Use `VehicleSeat` and hand the car to the driver. Never put damage or rewards on `Touched` | Raycast suspension, flight models, ControllerManager, server authority |
| Intermediate | Constraint movers with force limits; explicit ownership policy per object class; projectiles as swept casts; springs computed from frequency and damping ratio; one server teleport helper with movement exemptions | Custom character controllers, rewind |
| Expert | Raycast chassis with a load-sensitive tyre model; float-point boats; aerodynamic flight with a derived stall speed; per-vehicle validators; streaming for fast vehicles; server authority mode and the Character Controller Library; fixed versus adaptive stepping measured in the MicroProfiler | — |

## Contents

1 Solver basics and the two questions · 2 Assemblies and mass · 3 Network ownership · 4 Constraints, not body movers · 5 Collision groups and collider cost · 6 Character controllers · 7 Moving platforms · 8 Ragdolls · 9 Projectiles · 10 Vehicles (cars, boats, aircraft) · 11 Movement anti-cheat · 12 Physics performance · Level-up · Review gate · Sources

## 1. Solver basics and the two questions

- The engine simulates every unanchored assembly at 240 Hz by default, about 4 "worldsteps" per 60 fps frame `[official]`. Scripts see results in `RunService.PreSimulation` (write control inputs and forces here), `PostSimulation` and `Heartbeat` (read results).
- Units `[official]`: 1 stud is 0.28 m; default `Workspace.Gravity` is 196.2 studs/s², while Earth gravity converted to studs would be 35 studs/s². Roblox gravity is therefore about 5.6 times stronger per stud than reality. Every realistic spring, buoyancy or flight constant feels stiff and nervous until it is retuned for this (sections 10.2, 10.5).
- The solver is iterative. It is good at stacks, hinges and springs with sane mass ratios, and bad at small, fast, spinning colliders, very light parts jointed between heavy ones, and unlimited forces. `[VS]` `Workspace.NextGenerationPhysicsSolver` exists as a rollout-state property described as experimental `[official]`; no evidence found on its effects, so leave it on Default.
- **The two questions** that answer almost every physics bug `[lihfolk]`: (1) What is the assembly: which parts move together, which is the root, what is the total mass, is anything anchored? (2) Which machine runs its physics (the server, a single client, or none because it is asleep or anchored), and can that owner switch during play? Settle both with Studio's visualisation before reading code: Visualization Options > Network owners and Awake parts; Studio Settings > Physics > Are Assemblies Shown, Are Timesteps Shown.

## 2. Assemblies and mass

- An *assembly* is every part joined rigidly (`WeldConstraint`, `Weld`, `Motor6D`, `RigidConstraint`). It has one velocity, one mass, one owner. Constraints with freedom (hinge, spring, rope) connect **separate** assemblies into a *mechanism*. A *mover* is a constraint that applies force or torque to reach a target; *kinematic* means moved by script with no forces (anchored and animated by `CFrame`).
- Root part order `[official]`: anchored first, then non-`Massless`, then higher `RootPriority`, then size (with multipliers for seats and character roots). Set `RootPriority` when code must find a stable root.
- `Massless` only takes effect when the part is welded to a non-massless part, and never on the root. Use it on every visual mesh so body panels, accessories and held weapons do not move the centre of mass.
- Choose mass; do not inherit it. Put the mass in one low, simple root collider with `CustomPhysicalProperties` density, and read `AssemblyMass` and `AssemblyCenterOfMass` (draw a marker there while tuning). Friction combines the two touching surfaces by `FrictionWeight`, so a tyre with friction 1.5–2 and a high weight still slides on an ice material.
- Characters sitting in seats join the assembly: a heavy avatar on a light kart changes its handling. Make vehicles heavy enough that passengers are a small share, or recompute springs on `Occupant` change.
- Any time an assembly changes shape (weld added or removed, anchor toggled, joints broken on death), re-check its root and re-assert its owner `[lihfolk]`.

## 3. Network ownership

The network owner is the one machine (the server or a single client) that simulates an unanchored assembly; every other machine sees replicated, interpolated positions. Rules `[official]`:

| Fact | Consequence |
|---|---|
| The server always owns anchored parts; ownership cannot be set on them | `SetNetworkOwner` on an anchored part errors: guard with `CanSetNetworkOwnership()` |
| Unanchored assemblies default to automatic ownership: a nearby client with capacity is likely to take them | Responsive, but that client can fake their physics, and two nearby players cause hand-offs |
| Setting ownership on one assembly of an unanchored mechanism sets it for every assembly in the mechanism | Set it once, on the root |
| Anchoring then unanchoring a lone assembly loses its ownership setting and returns it to automatic | Call `SetNetworkOwner` again straight after unanchoring |
| `SetNetworkOwner(nil)` gives the server ownership; the docs advise using it conservatively because interactions can look jittery to clients | Use it for gameplay-critical and exploitable objects, not for everything |
| Roblox cannot verify physics computed by an owning client, and `Touched` follows ownership: a client can fire it for parts it owns | Never trust position, velocity or `Touched` of client-owned parts for outcomes |
| `ApplyImpulse` from a client does nothing on a server-owned part | Apply forces on the machine that simulates the assembly |

There is no "owner changed" event; poll `GetNetworkOwner()` on tagged parts in a test session to catch flips `[lihfolk]`.

Ownership policy by object class `[house]`:

| Object | Owner | Why |
|---|---|---|
| Player character | That player's client (always, outside server authority mode) | Engine rule; validate movement instead (section 11) |
| Driven vehicle | The driver, set on `Occupant` change; never a passenger | Otherwise whoever sat first owns it and the driver's input lags by several network cycles `[official]` |
| Parked vehicle | Server (`SetNetworkOwner(nil)`) or anchored | Automatic ownership lets the nearest client grab and throw it `[lihfolk]` |
| NPCs and enemies that matter to gameplay | Server | Automatic ownership makes them slide differently per client and lets a client steer them |
| Shared gameplay props (ball, crate, payload) | Server, with capped velocity; or validate outcomes | Removes ownership ping-pong and flings; costs some responsiveness at high ping |
| Elevators, platforms, doors | Server | Riders otherwise see it through an extra replication hop |
| Cosmetic debris, corpses, pets | No replication at all: simulate or animate per client | Zero server and network cost |

Server authority mode `[VS]` replaces this model for competitive physics games: the server simulates, clients predict whole assemblies and roll back (networking-and-security.md). `[VS]` Physics replication itself changed in 2026: `Workspace.ImprovedPhysicsReplication` is a rollout-state property `[official]`; DevForum posts report a rollout that was rolled back in May 2026, a follow-up thread updated through July 2026, and bug reports of relative-motion desync with it enabled `[community]`. If riders or trains began to jitter after an engine update, test with the property set to Disabled before rewriting anything.

## 4. Constraints, not body movers

Legacy `Body*` movers are deprecated `[official]`; they still run in old models, and audit sketch F in engineering-architecture.md finds them.

| Legacy | Replacement | Notes |
|---|---|---|
| `BodyVelocity` | `LinearVelocity` | `VelocityConstraintMode` Line, Plane or Vector. A dash wants Plane mode with Y free, or the character floats off ledges |
| `BodyPosition` | `AlignPosition` | One- or two-attachment mode; `RigidityEnabled = true` ignores `MaxForce`, `MaxVelocity` and `Responsiveness` |
| `BodyGyro` | `AlignOrientation` | `PrimaryAxisLookAt`, `PrimaryAxisParallel` modes for turrets and self-righting |
| `BodyAngularVelocity` | `AngularVelocity` | |
| `BodyForce`, `BodyThrust` | `VectorForce` | `RelativeTo`, `ApplyAtCenterOfMass` |
| `RocketPropulsion` | `LineForce` + `AlignOrientation` | |

- **Force limits are the most important setting.** An unlimited mover wins every fight: it pushes through thin walls, launches whatever it touches and jitters against other movers. Start at `MaxForce = AssemblyMass × desired acceleration`; about `mass × 2000` reaches a dash speed within a frame or two without punching through geometry `[lihfolk]`.
- A mover whose `Attachment0` is missing or outside the world silently does nothing: check that first when "the dash does nothing".
- Create movers on the machine that owns the assembly, give each a lifetime, and destroy it on every exit path including death.
- **One mover per object.** Choose one: anchored and moved by `CFrame` (kinematic), or unanchored and moved by constraints. A script that sets `CFrame` on an unanchored part every frame fights the solver, worse when the server writes and a client owns.
- Mechanical constraints: `HingeConstraint` (actuator None, Motor or Servo), `PrismaticConstraint` (slider), `CylindricalConstraint` (slide plus spin), `BallSocketConstraint` (cone and twist limits), `SpringConstraint`, `TorsionSpringConstraint`, `RopeConstraint`, `RodConstraint`, `PlaneConstraint`, `UniversalConstraint`, `NoCollisionConstraint`. A hinge's two attachments must share an axis direction or it rotates about the wrong one `[official]`; turn on Constraint Details and check every arrow.
- Stability heuristics `[community]`: keep jointed parts within about one order of magnitude of each other in mass (a near-zero-mass hub between a chassis and a wheel vibrates); never zero damping on a spring; move constraint targets smoothly; enable limits rather than relying on collisions between jointed neighbours.

## 5. Collision groups and collider cost

- Register groups once at server start with `workspace:RegisterCollisionGroup` and `workspace:CollisionGroupSetCollidable`; assign with `BasePart.CollisionGroup`. The engine supports 32 groups `[official]`. Typical set: `Players`, `NPCs`, `Vehicles`, `Wheels`, `Ragdoll`, `Debris`, `Projectiles`. Use `NoCollisionConstraint` for single pairs (wheel to chassis, neighbouring ragdoll limbs).
- `Workspace.TouchesUseCollisionGroups` makes non-colliding groups also ignore `Touched` `[official]`.
- Collider cost rises Box → Hull → Default → Precise, with `Tunable` between `[VS]`; the table per asset type is in performance.md. Physics-specific rules: moving bodies get the simplest collider that plays right (one rounded hull for a car body, a ball or cylinder for a wheel); a mesh tyre with Hull fidelity is a faceted polygon that ticks over flat ground at speed `[lihfolk]`; concave or Precise colliders on fast movers are where tunnelling and snagging start.
- House rules: every visible vehicle, wheel, platform and prop is a Blender mesh. Its collider may be a separate invisible `_COL` mesh or an invisible primitive (the only place primitives are allowed), welded, with the visual set `Massless`, `CanCollide = false`, `CanTouch = false`. Collision groups never switch off player-versus-world collision for a visible object.

## 6. Character controllers

**Default Humanoid.** A state machine that also applies forces: it drives toward `WalkSpeed` along `MoveDirection`, holds `HipHeight`, and manages limb collision. Defaults: `WalkSpeed` 16 studs/s, `JumpHeight` 7.2 studs; time to apex is `sqrt(2h / g)`, about 0.27 s at default gravity.

- States `[official]`: FallingDown, Ragdoll, GettingUp, Jumping, Swimming, Freefall, Flying, Landed, Running, RunningNoPhysics, StrafingNoPhysics, Climbing, Seated, PlatformStanding, Dead, Physics. Disable the ones the game never uses (`Climbing` without ladders, `Swimming` without water, `FallingDown` and `Ragdoll` so small fast parts cannot trip characters). `SetStateEnabled` does not replicate: call it on the server **and** on the owning client. `ChangeState` only works on the machine that owns the character.
- A mover on a Humanoid shares the root with the Humanoid's own forces. Three ways to stop the fight `[lihfolk]`: feed `Humanoid:Move(direction)` the same direction for a short dash; switch to `Physics` or `Freefall` on the owner for launches, grabs and ragdolls, restoring the state on **every** exit path and capping how long anything may hold control; or disable the state machine entirely (below). A character in `Running` is pressed to the ground, so a knock-up needs the state change first.
- NPCs: server-owned; prefer an `AnimationController` rig moved by `AlignPosition` and `AlignOrientation` (or by `CFrame` when anchored) over a full Humanoid once counts pass a few dozen (gameplay-systems-cookbook.md, section 13).

**ControllerManager** `[VS]`. With `Humanoid.EvaluateStateMachine = false` the Humanoid applies no forces, runs no floor or ladder sensing, changes no collision and no state; state events still fire if you set states yourself, which is what keeps the Animate script working `[official]`. A `ControllerManager` (with `RootPart`, `BaseMoveSpeed`, `MovingDirection`, `FacingDirection`, `UpDirection`, `GroundSensor`, `ClimbSensor`) then drives a `GroundController`, `AirController`, `ClimbController` or `SwimController` chosen through `ActiveController`, using `ControllerPartSensor`s. An `ActiveController` that cannot activate (a GroundController with no floor) stays set and is retried each frame, so switch to the AirController in the air yourself. Use it when the Humanoid's movement model is the problem (wall-running, planet gravity through `UpDirection`, custom slopes), not when one move needs a push.

**Character Controller Library** `[VS]`. `AvatarAbilities` rebuilds character movement as Luau "abilities" with start and run conditions, conflict rules and lifecycle callbacks that run on both the predicting client and the authoritative server. Conflict: a DevForum post titled "[Full Release] The Future of Character Movement: Character Controller Library" and the April 2026 weekly recap call it released `[community: search summaries]`, while the docs page still carries a beta notice and an enable step `[official]`. It is opt-in through Avatar Settings > Movement `[official]`. Treat it as adoptable for new projects built on server authority; prototype before migrating a live game.

**Avatar Joint Upgrade** `[VS]`. `AnimationConstraint` is now the default joint for R15 player rigs when `StarterPlayer.AvatarJointUpgrade` is enabled (the default for new experiences) `[official]`. What breaks in older code: `FindFirstChildOfClass("Motor6D")` and `IsA("Motor6D")` find nothing (check for `AnimationConstraint` first, then fall back); `C0`, `C1`, `Part0`, `Part1` are read-only aliases; procedural motion multiplies into `Transform` during `PreSimulation` instead of writing `C0`; never edit `RigAttachment.CFrame`.

## 7. Moving platforms

A character is simulated by its own client and moved by friction against whatever it stands on. What it stands on decides everything `[lihfolk]`:

| Platform | What the rider feels | Verdict |
|---|---|---|
| Anchored, moved by `CFrame`, `PivotTo` or a tween | A floor that teleports with zero velocity: the rider stays put while it slides away; down moves drop them | Wrong for anything players stand on |
| Unanchored, constraint-driven, server-owned | A real moving surface, replicated slightly late | Right for lifts, slow trams, obby blocks |
| Unanchored, owned by another player's client | Two replication hops | Jitter at speed: seat the riders |
| Anchored, with `AssemblyLinearVelocity` set to its motion | Conveyor behaviour: friction drags riders along | Works for slow, mostly linear paths; rotation still slips `[community]` |

- Lift recipe: unanchored car on a `PrismaticConstraint` in Servo mode with a speed cap, `ServoMaxForce` sized to mass × gravity with headroom for a full load, `SetNetworkOwner(nil)`, downward acceleration well below gravity (ramp the speed), walls on fast lifts.
- Exact-path platforms: each client applies the platform's frame-to-frame `CFrame` delta to its own root in `PreSimulation` while standing on a tagged platform (relative carry). It needs no physics agreement and also works for ship decks.
- Speed decides: under about 30 studs/s riders can walk; above that, seat them and allow walking only when stopped. Test with the network simulator at 150 ms, not in solo play.
- Never weld a player to a platform: one assembly has one owner, so either the player loses their character or a client owns the platform. Seats are the weld the engine manages.
- Movement validators must measure speed relative to the floor (section 11).

## 8. Ragdolls

- **With the Avatar Joint Upgrade** `[VS]`: R15 characters already carry `BallSocketConstraint`s beside their `AnimationConstraint`s. Go limp by disabling the animation joints or setting `IsKinematic = false` and lowering `MaxTorque`; partial strength gives stagger and "arm strength" effects `[official]`. `StarterPlayer.CharacterBreakJointsOnDeath` only takes effect with the upgrade enabled.
- **Legacy `Motor6D` rigs:** per joint, add a `BallSocketConstraint` (hinge for knees and elbows), set `Motor6D.Enabled = false`, and set `Humanoid.BreakJointsOnDeath = false` and `RequiresNeck = false` first. Starting limits `[lihfolk]`: neck cone 30–40°, shoulder 70–90°, hip 50–70°, knee and elbow hinges 0–135°, ankle and wrist 20–45°; a little `MaxFrictionTorque` stops limbs swinging forever. Build cone attachments along the child bone in the rest pose.
- Limbs need `CanCollide = true` while limp (the Humanoid normally manages limb collision) and must not collide with their neighbours: `NoCollisionConstraint` per joint or a `Ragdoll` group that ignores itself. Set the root part non-colliding so it does not prop the body up.
- Ownership: a player's ragdoll state change must run on their client (`ChangeState(Physics)` needs ownership). Keep the same network owner through the ragdoll; an ownership change pauses the body for a moment, which is the "knockback plus ragdoll looks laggy" report `[community]`. Pin NPC ragdolls to the server or give them to nobody (below).
- Corpses: on each client, clone the visible parts into a local ragdoll and hide the original. Zero network cost; bodies differ between players, which rarely matters `[lihfolk]`.
- Recovery: blend back by re-enabling joints, then `GettingUp`; cap ragdoll time and exempt the player from movement checks while limp.

## 9. Projectiles

| | Physical part | Simulated point (maths + cast) |
|---|---|---|
| Hit detection | Contact or `Touched` | Cast from last position to new position every step |
| Fast and thin targets | Tunnels: at 600 studs/s a bullet moves 10 studs per 60 fps frame | Cannot miss |
| Network | A replicated assembly with an owner | One small message; every client draws its own visual |
| Bounce and roll | Free | You write it |
| Use for | Grenades that roll down stairs, physics toys, debris | Bullets, arrows, spells, anything fast |

- Motion is closed form: `p(t) = p0 + v0·t + ½·a·t²`. Any machine can compute the position at any time from `(origin, velocity, gravity, startTime)`, so late receivers fast-forward and the server can check a claim. Step by time since launch, never by accumulated frame deltas. Gravity is per weapon, not `Workspace.Gravity`.
- Cast choice: `Raycast` for thin shots; `Spherecast` or `Blockcast` with the projectile's radius for anything fat. Shapecasts do not report what they start inside (do one `GetPartBoundsInRadius` check on the first step) and are limited to 512 studs of shape size and 1,024 studs of travel per call `[official]`.
- Fire from the eye, draw from the muzzle: cast head-to-muzzle first so a muzzle poked through a wall hits that wall. Build `RaycastParams` once per shooter; reassign `FilterDescendantsInstances` rather than mutating it. Cap range by distance **and** by time.
- Network model: shooter predicts and shows effects at once; sends origin, direction, server timestamp and weapon id (never the hit); the server validates and decides damage; other clients get an unreliable, distance-filtered, batched broadcast (one message per 50 ms of fire, a seed for shotgun pellets).
- Who decides the hit: slow projectiles (rockets, arrows) are simulated on the server against current positions, because targets can see and dodge them; fast bullets are client-claimed and server-checked, optionally against a rewound position history capped at about 250 ms (gameplay-systems-cookbook.md, section 12).
- Server checks, cheapest first: weapon owned and equipped; fire rate with a small burst allowance; ammo on the server's count; origin within a few studs of the server's character position; direction finite and unit length; line of sight origin to hit; claimed hit position consistent with the closed-form path at the claimed time.
- Libraries `[community]`: FastCast's author no longer maintains it; FastCast2 (parallel, typed) is an active community fork; SecureCast's thread is marked archived. Read one before writing your own, and vendor a pinned copy from the author's repository, never a Toolbox model.
- Visuals are pooled, anchored, non-colliding Blender meshes or beams (architecture-patterns-luau.md, Object Pool).

## 10. Vehicles

### 10.1 Pick the chassis

| Option | Strengths | Weaknesses | Use when |
|---|---|---|---|
| No physics (anchored model on a path) | Cannot fail | No interaction | Rides, cutscenes, hundreds of traffic cars (simulate as points on splines; spawn a physical car only when a player is involved) |
| Constraint car (hinge motors, springs, servo steering) | Wheels really touch the world; crashes, towing, lost wheels come free | Unstable at high speed; wheels tunnel and catch seams; tuned per car | The fun is the body meeting the world: off-road, derby, sandbox |
| Raycast car (one rigid body, a force per corner) | Stable at any speed, cheap, predictable | You write the tyre model; wheels never collide | Racing, karts, anything above about 120–150 studs/s, or dozens of cars on phones |
| Legacy `VehicleSeat` hinge drive (`MaxSpeed`, `Torque`, `TurnSpeed`) | Zero code | Only detects motors rigidly connected to the seat; fixed feel `[official]` | Never in a shipped game |
| Community kit (A-Chassis family) | Drivetrain, gauges and sounds on day one | Its remotes, input assumptions and update cadence become yours | Only after an audit: every remote it creates, `require(id)` and `loadstring`, deprecated body movers, keyboard-only input, per-frame cost with 20 cars, streaming and deferred-signal safety. More than two failures: write the raycast car `[lihfolk]` |

`VehicleSeat` is still the right seat for every option: it fills `ThrottleFloat` and `SteerFloat` (−1 to 1) from keyboard, gamepad and the touch thumbstick, and exposes `Occupant`; the integer `Throttle` and `Steer` are deprecated and no longer replicate `[official]`. House rules: body, wheels and interior are Blender meshes; code comes from a pinned repository copy that has been read, never a Toolbox model; one input layer feeds every chassis type (ui-input-crossplatform.md).

### 10.2 Springs: compute, do not guess

Treat a `SpringConstraint` (or a raycast spring) as a spring-damper. Choose the sprung mass per corner `m` (about `AssemblyMass / 4`), a natural frequency `f` (road car 1–1.5 Hz, sporty 1.5–2.5, kart or arcade 2.5–4) and a damping ratio `ζ` (0.2 floaty, 0.4–0.6 controlled, 1.0 dead) `[lihfolk]`:

```lua
--!strict
-- unexecuted sketch: suspension numbers from design intent; re-run whenever mass or gravity changes
local function tuneSpring(spring: SpringConstraint, cornerMass: number, hz: number, zeta: number, restLength: number)
	local omega = 2 * math.pi * hz
	local stiffness = cornerMass * omega * omega
	local sag = cornerMass * workspace.Gravity / stiffness -- how far the car settles under its own weight
	spring.Stiffness = stiffness
	spring.Damping = 2 * zeta * math.sqrt(stiffness * cornerMass)
	spring.FreeLength = restLength + sag
	spring.LimitsEnabled = true
	spring.MinLength = restLength * 0.5 -- bump stop
	spring.MaxLength = restLength + sag
end
```

Worked example: mass 400, so `m` = 100; `f` = 1.8 Hz; `ζ` = 0.45 → stiffness 12,790, damping 1,018, sag 1.53 studs. The sag is large because of Roblox gravity: a realistic frequency sinks much further than a real car, so games raise frequency, lower gravity, or accept a kart-like ride; whichever you pick, recompute every spring after changing gravity. If landings hit `MinLength`, the impulse goes straight into the chassis: raise frequency or the bump stop before adding damping.

### 10.3 Constraint car

- Layout per wheel: chassis → invisible hub on a vertical `PrismaticConstraint` with the `SpringConstraint` → wheel on a `HingeConstraint` (Motor). Steered wheels add a knuckle on a Servo hinge about the vertical axis. Hubs and knuckles are small, non-colliding and light but not near-zero mass.
- Build one corner, then mirror it. Mirrored axles flip motor direction: store a per-wheel `Sign` attribute rather than relying on attachment orientation.
- Drive: `AngularVelocity = targetSpeed / wheelRadius` (radians per second); start `MotorMaxTorque` so that torque ÷ wheel radius is about 1–2 times the weight carried by that wheel. Unlimited torque means wheelies and launches.
- Steering: servo torque high enough to beat tyre grip; reduce maximum angle with speed or the car snap-spins at full lock on a straight.
- Stability is the centre of mass: massless panels, mass in a low root, a wide track, optional low-torque `AlignOrientation` to resist flips, a `VectorForce` downforce scaled by speed squared, and a "flip back" action with a cooldown.
- Write inputs in `PreSimulation` on the driver's client; the server zeroes motors when the seat empties, because the client that set them may be gone.

### 10.4 Raycast car

One rigid chassis with a rounded, near-frictionless root collider; four mount attachments; one `VectorForce` per corner (`RelativeTo = World`, `ApplyAtCenterOfMass = false`) so pitch and roll emerge on their own. Wheel meshes are visuals placed at `mount − up × (hitDistance − radius)` and spun by forward speed ÷ radius.

```lua
--!strict
-- unexecuted sketch: one corner per physics step, on the client that owns the car (bind to PreSimulation)
local function stepCorner(root: BasePart, mount: Attachment, force: VectorForce, cfg: Corner, throttle: number)
	local origin, up = mount.WorldPosition, root.CFrame.UpVector
	local hit = workspace:Raycast(origin, -up * (cfg.rest + cfg.radius), cfg.params) -- params exclude this car
	if not hit then force.Force = Vector3.zero; return end
	local compression = cfg.rest - (hit.Distance - cfg.radius)
	local velocity = root:GetVelocityAtPosition(origin)
	local load = math.max(0, cfg.stiffness * compression - cfg.damping * velocity:Dot(up)) -- a spring cannot pull the car down
	local right, forward = mount.WorldCFrame.RightVector, mount.WorldCFrame.LookVector
	local grip = cfg.mu * load -- friction limit grows with load: an unloaded wheel has no grip
	local lateral = math.clamp(-velocity:Dot(right) * cfg.cornering, -grip, grip)
	local drive = if cfg.driven then math.clamp(throttle * cfg.engine, -grip, grip) else 0
	force.Force = up * load + right * lateral + forward * drive
end
```

Without the `math.max` cars stick to ceilings over crests. For drifting, lower `mu` on the rear corners while the handbrake is held. Use a `Spherecast` instead of a ray for smoother kerbs. Tune spring numbers with 10.2.

### 10.5 Ownership, seats, streaming

```lua
--!strict
-- unexecuted sketch (server): the driver owns the car; a parked car belongs to the server
local function bindSeat(car: Model, seat: VehicleSeat, motors: { HingeConstraint })
	local function park()
		for _, motor in motors do motor.AngularVelocity = 0 end
		if seat:CanSetNetworkOwnership() then seat:SetNetworkOwner(nil) end
		Validator.untrack(car)
	end
	seat:GetPropertyChangedSignal("Occupant"):Connect(function()
		local humanoid = seat.Occupant
		local driver = if humanoid then Players:GetPlayerFromCharacter(humanoid.Parent :: Model) else nil
		if driver and Garage.mayDrive(driver, car) then
			seat:SetNetworkOwner(driver) -- applies to the whole mechanism
			Validator.track(car, driver)
		else
			if humanoid then humanoid.Sit = false end -- not allowed to drive this car
			park()
		end
	end)
	park()
end
```

- The docs sample hands the car back with `SetNetworkOwnershipAuto()`; parking on the server instead removes "grab and throw a parked car" at the cost of server simulation while the car is still moving (parked cars sleep) `[lihfolk]`. With hundreds of cars, anchor parked ones and re-assert ownership after unanchoring.
- Multi-seat: passengers never own; gunners send aim intents; loose parts riding on the car go to the same owner `[official]`.
- Streaming: set `ModelStreamingMode = Atomic` on every vehicle so clients never index a half-arrived car; make the driver's own car `PersistentPerPlayer` with `Model:AddPersistentPlayer`. A client-owned car falls through road it has not streamed: raise `StreamingMinRadius` for driving games, keep a coarse persistent road collider, or call the server-only `Player:AddReplicationFocus` on a part ahead of a fast car and remove it on exit `[lihfolk]`. `[VS]` Frustum streaming (`Player.FrustumStreaming`, server-set; `Automatic` turns on for a narrow field of view, a far camera, or high velocity while looking along the direction of travel) streams what the camera sees beyond the normal radius; it is additive, costs client memory and has a short activation delay in Automatic mode `[official]`.
- Spawner: per-player vehicle cap, despawn on leave and after idle time, spawn only onto a clear shapecast, cooldown on the server clock.

### 10.6 Boats

- Float-point model: 4–8 attachments along the waterline; each step, per point: water height `h` (a constant or a shared wave function that server and clients both evaluate), depth `d = h − y`; no force when `d ≤ 0`; otherwise upward force `k × min(d, maxDepth) − c × verticalVelocity`, clamped at zero. One `VectorForce` per point.
- Calibration: with `N` points and a chosen draft, `k = m × g / (N × draft)`, so the hull rests at the draft. Bob frequency is `sqrt(g / draft) / 2π`: 2.2 Hz at a 1-stud draft (a cork), 1.1 Hz at 4 studs. Slow it with a deeper draft, a constant upward force cancelling part of the weight, and a damping ratio of 0.5–0.7 `[lihfolk]`.
- Boats slide like pucks without a keel: sideways drag 10–20 times forward drag feels like a boat, about 5:1 like a jet ski.
- Riders on deck use the relative carry from section 7, or seats at speed.
- Conflict: LihFolk also documents engine buoyancy in Terrain water (parts float by density; `BuoyancySensor`). House rule 1 means the water surface is a Blender mesh with a shader or animated texture, so use the float-point model against your own height function; the rendered and physical surfaces must share that function or boats appear to hover.

### 10.7 Aircraft

| Tier | How | Use for |
|---|---|---|
| Arcade | `LinearVelocity` holds speed along the nose; `AlignOrientation` turns the nose toward input. Add bank into turns, speed traded against pitch, and auto-level | Mounts, jetpacks, flying cars, casual dogfights |
| Simple aerodynamic | Compute lift, drag and thrust each step; apply at wing and tail attachments | Flight-focused games |
| Engine fluid forces `[VS]` | `Workspace.FluidForces = Experimental` (Studio-only setting) with `BasePart.EnableFluidForces`; the docs warn behaviour may change | Build-your-own-plane sandboxes only |

Aerodynamic tier in four numbers: pick cruise speed and a cruise angle of attack (about 4°); set the lift constant `K = m × g / (v_cruise² × CL(α_cruise))`; stall speed follows as `sqrt(m × g / (K × CL_max))`. Fold air density and wing area into `K`; SI constants do not transfer to studs. Stability comes from a tail force behind the centre of mass, or a torque turning the nose toward the velocity scaled by dynamic pressure, plus angular damping. Most players need auto-coordination, stall warning and mouse or stick aim `[lihfolk]`. A lift vector pointing down is the commonest bug: draw it.

## 11. Anti-cheat for movement

First try to make movement cheating worthless `[lihfolk]`: sequential server-validated checkpoints with minimum segment times, server zone gating, server distance checks on every interaction, laps and finishes recorded by the server from gate crossings. A fly hacker who gains only a view needs no detector. Build detection where position itself is the prize (racing, leaderboard obbies, PvP, carrying a stolen item), or adopt server authority mode.

- Sample each character on the server every 0.2–0.5 s, staggered, using real elapsed time; skip a sample when the server itself hitched.
- Honest causes that look like cheating: latency bursts, knockback, moving platforms, vehicles, falling, respawns and server teleports, ragdolls, flings by others. Each needs an exemption or a budget, and every server-caused move must go through one helper that grants it. Grep for `PivotTo`, `.CFrame =` and `MoveTo` on characters: a missed call site is the most common false positive `[lihfolk]`.
- Speed: horizontal displacement minus the floor's velocity against expected speed × dt × 1.5 plus slack; accumulate in a leaky bucket. Teleport: a single step far beyond that, handled at once. Fly: airborne and **not descending** for longer than a jump allows (0.27 s to apex at defaults, so 1.5 s is far outside), grounded by a server raycast, not `Humanoid.FloorMaterial`. Noclip: a ray between samples at mid-torso height against static world geometry, counting only penetrations over about 1 stud.
- Vehicles: per driven car, check horizontal speed against `MaxSpeed` plus margin, height above ground, map bounds and angular velocity (crash rolls are a few radians per second, flings are dozens); three consecutive bad samples at 4 Hz revoke ownership and restore the last good `CFrame`. A measured `MaxSpeed`, not a guessed one, or the fastest honest drivers get reset on the best straight.
- Response: rubber-band and revoke first, add to the suspicion score, never kick on one sample (networking-and-security.md).

```lua
--!strict
-- unexecuted sketch (server): one helper for every server-caused move, and a sampler that respects it
local graceUntil: { [Player]: number } = {}
function Movement.allow(player: Player, seconds: number) -- call before knockback, dashes, launch pads
	graceUntil[player] = math.max(graceUntil[player] or 0, os.clock() + seconds)
end
function Movement.teleport(player: Player, target: CFrame)
	local character = player.Character
	if character then Movement.allow(player, 1.5); character:PivotTo(target) end
end
local function sample(player: Player, s: State, now: number) -- every 0.25 s per player, staggered
	local root, humanoid = rootOf(player), humanoidOf(player)
	if not root or not humanoid then return end
	local dt, position = now - s.t, root.Position
	local exempt = now < (graceUntil[player] or 0) or humanoid.SeatPart ~= nil or dt > 0.75
	if not exempt then
		local floor = workspace:Raycast(position, Vector3.new(0, -(humanoid.HipHeight + 4), 0), WORLD_ONLY)
		local carrier = if floor then (floor.Instance :: BasePart).AssemblyLinearVelocity else Vector3.zero
		local step = ((position - s.position - carrier * dt) * Vector3.new(1, 0, 1)).Magnitude
		local speed = expectedSpeed(player) -- the server's own formula, never a property a client can write
		local allowed = speed * dt * 1.5 + 2 + speed * player:GetNetworkPing()
		s.bucket = math.max(0, s.bucket + (if step > allowed then 1 else -0.25))
		if step > allowed * 3 + 10 or s.bucket >= 4 then -- single-step teleport, or sustained speed
			s.bucket = 0
			Suspicion.add(player, "movement")
			Movement.teleport(player, s.good)
		elseif floor then
			s.good = root.CFrame
		end
	end
	s.position, s.t = position, now
end
```

## 12. Physics performance

- Budget: client physics at most 2–3 ms per frame `[house]` (performance.md). Read `workspace:GetRealPhysicsFPS()`, `GetPhysicsThrottling()` and `GetNumAwakeParts()` in a debug overlay; in the MicroProfiler look under `physicsStepped` → `worldStep`, and treat `stepWorldThrottled` as a sign of too many unanchored assemblies.
- Sleeping is the main saver: an assembly at rest costs nothing. Anything that writes a physics property, an occupied `VehicleSeat` or a moving neighbour keeps things awake (thresholds in performance.md). A tiny constant force may never wake a sleeping part: nudge its velocity when starting one.
- Adaptive timestepping `[VS]`: `Workspace.PhysicsSteppingMethod = Adaptive` (Studio property, not scriptable) assigns assemblies to 240, 120 or 60 Hz islands and can improve physics performance by up to 2.5 times; connected assemblies of different rates run at the highest. Use Fixed for racing, destruction and complex mechanisms, or when most parts sit in the 240 Hz island anyway `[official]`. Decide per game: measure island counts in `LDLPGSSolver::solve` with your vehicles moving.
- Throttling `[official]`: when the engine cannot keep up in real time it updates physics less often and parts appear to move slower; `GetPhysicsThrottling()` returns the percentage of real time being simulated (100 is healthy), and objects associated with Humanoids are exempt. A value under 100 on phones means fewer or simpler moving assemblies, not a faster script. Each driven client-owned vehicle is also a replication stream to every other client: budget it as bandwidth `[lihfolk]`.
- Caps `[house]`: vehicles per player 1–2 and per server sized by a 20-car test on the target phone; physical debris and dropped items capped and expiring; nothing physical for pets, conveyor drops, coins or corpses.
- Lower `FallenPartsDestroyHeight` to just under the map and respawn vehicles that fall.
- Server authority mode adds server CPU (the server simulates every character) and client CPU (resimulation): profile both before adopting.

## Level-up: symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Object flung at spawn or teleport | Spawned overlapping another collider | Shapecast or `GetPartsInPart` before placing; spawn above ground; brief no-collide |
| Fling when a constraint turns on | Unlimited force and a target far away | Force and velocity limits; move targets smoothly |
| Jointed part vibrates, then explodes | Mass mismatch across a joint; zero damping | `Massless` visuals; hubs with real mass; computed damping |
| Players flung when one player touches them | Exploiter replicating extreme velocity on an owned assembly | Server-own shared props; sanity loop resetting non-finite or over-speed assemblies; movement checks |
| Shared crate or ball stutters or snaps back | Ownership ping-pong between two nearby clients | `SetNetworkOwner(nil)` and capped velocity |
| Unanchored part jitters while scripted | Script sets `CFrame` every frame against the solver | One mover: anchor and animate, or constraints on the owner |
| NPC smooth on the server, steppy on clients | Low server heartbeat; too many moving server-owned assemblies | Fix server frame time; animate cosmetics per client |
| NPCs slide differently for each player | NPC on automatic ownership | Server ownership |
| Driver input lags | A passenger sat first and owns the car | Ownership to the driver on `Occupant` change |
| Car snaps back periodically | Ownership flips, or a server script writes its `CFrame` | Explicit owner; move the car only through the teleport helper |
| Car ticks and shakes at speed | Mesh tyre with Hull collision | Cylinder or ball collider, mesh as massless visual |
| Car rolls in every corner | High centre of mass, narrow track | Massless panels, low ballast, wider track, mild self-righting |
| Car bounces forever or rides on bump stops | Guessed spring numbers; gravity changed after tuning | Section 10.2 |
| Car spins on the spot under throttle | Mirrored motors with the same sign | Per-wheel sign |
| Car falls through the road at speed | Client-owned car outran streaming | Atomic and per-player persistent car, larger minimum radius, persistent road collider |
| Riders slide off lifts and trains | Anchored platform moved by `CFrame` | Constraint-driven unanchored platform, relative carry, or seats |
| Riders jitter since an engine update | Physics replication rollout `[VS]` | Test with `ImprovedPhysicsReplication` Disabled; report it |
| Character stuck floating or limp after an ability | State or mover not restored on an exit path | Restore on every path; cap hold time; destroy movers on death |
| Dash does nothing, or stalls from standstill | Missing `Attachment0`; Humanoid fighting the mover | Assert the attachment; `Move(direction)` alongside or a state change |
| Code cannot find `Motor6D` on new characters | Avatar Joint Upgrade `[VS]` | Look for `AnimationConstraint` first |
| Bullets pass through thin walls | Physical projectile parts | Swept casts from last to new position |
| Honest players rubber-banded | A server move without an exemption; platform or vehicle speed counted as walking | One teleport helper; floor-relative speed; seat exemption |
| Physics time climbs with player count | Per-player physical objects (pets, drops, debris) | Client-side visuals; caps; sleep audit with Awake parts |

## Review gate

- [ ] Every unanchored object class has a written owner (driver, server, nobody) and one mover.
- [ ] No `Body*` movers; every constraint mover has a force limit, an attachment check and a cleanup path.
- [ ] No outcome depends on `Touched`, position or velocity of a client-owned assembly without a server check.
- [ ] Vehicles: chassis type chosen for a stated reason; springs computed; visuals massless Blender meshes on simple colliders; driver owns, parked cars are server-owned or anchored; `Atomic` streaming; validator with strikes and server-granted allowances.
- [ ] Platforms players stand on are physically driven and server-owned, or riders are seated or carried.
- [ ] Projectiles that are fast or thin are swept casts with closed-form motion; the server decides damage.
- [ ] Character code works with `AnimationConstraint` rigs; states and movers are restored on every exit path; `SetStateEnabled` is applied on both sides.
- [ ] Every server-caused character move goes through one helper that grants a movement exemption.
- [ ] Stepping method chosen from a MicroProfiler measurement; awake-part count checked at idle; per-player physical object caps in place.
- [ ] `[VS]` items (server authority, Character Controller Library, joint upgrade, replication rollout, fluid forces) re-checked at create.roblox.com/docs before adoption.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/physics/{network-ownership,adaptive-timestepping,mover-constraints,assemblies,units,sleep-system}.md`, `workspace/collisions.md`, `characters/character-controller-library/index.md`, `projects/server-authority/index.md`, `reference/engine/classes/{Workspace,WorldRoot,BasePart,VehicleSeat,Humanoid,ControllerManager,AnimationConstraint,Motor6D,StarterPlayer,HingeConstraint,SpringConstraint,CylindricalConstraint,PhysicsService,Player,Model}.yaml`, `reference/engine/enums/{HumanoidStateType,ModelStreamingMode}.yaml`, `workspace/streaming/frustum.md` (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `25 Physics and Vehicles/` (Cars with Constraints - Suspension Steering and Drive; Choosing a Car Chassis; Boats Buoyancy and Water; Aircraft and Flight Models; Projectiles and Ballistics; Standing on Moving Vehicles and Platforms; Vehicle Ownership and Anti-Exploit; Vehicles and StreamingEnabled); `09 Gameplay Systems/Mover Constraints and Physics Controllers.md`; `23 Debugging Deep Dives/Debugging Physics and Network Ownership.md`; `22 Anti-Exploit and Security/Detecting Movement Exploits - Speed Fly Noclip Teleport.md`; `08 Animation/04 Procedural/Ragdolls and Physics-Based Animation.md` (read)
- Physics replication, 2026 (search summary): https://devforum.roblox.com/t/upcoming-improvements-to-physics-replication/4675512, https://devforum.roblox.com/t/heads-up-upcoming-rollout-of-improved-physics-replication/4618365, https://devforum.roblox.com/t/relative-physics-desync-with-improvedphysicsreplication-enabled/4767277
- Character controllers and joints (search summary): https://devforum.roblox.com/t/full-release-the-future-of-character-movement-character-controller-library/4565267, https://devforum.roblox.com/t/studio-beta-avatarabilities-library-for-a-luau-based-character-controller/4403904, https://devforum.roblox.com/t/weekly-recap-april-6-10-2026/4568634, https://devforum.roblox.com/t/avatar-joint-upgrade-for-physically-simulated-character-movement-is-now-live/4298561
- Vehicles (search summary): https://devforum.roblox.com/t/raycast-suspension-wheel-module-an-alternative-to-standard-physics-based-wheels/2170837, https://devforum.roblox.com/t/trying-to-create-ray-cast-suspension-editable-open-stable-and-optimized/3494597, https://devforum.roblox.com/t/a-vehicle-chassis-with-the-pacejka-friction-circle-raycast-suspension-gearbox/2400821
- Projectiles (search summary): https://devforum.roblox.com/t/securecast-server-authoritative-projectiles-with-lag-compensation-multi-threading-and-more/2546164, https://devforum.roblox.com/t/fastcast2-an-improved-version-of-fastcast-with-parallel-scripting-more-extensions-and-statically-typed-a-powerful-modern-projectile-library/4093890, https://devforum.roblox.com/t/alternatives-to-fastcast/2630169
- Ragdolls, platforms, movement checks (search summary): https://devforum.roblox.com/t/ragdoll-goes-through-ground-due-to-networkownership-changing/1119672, https://devforum.roblox.com/t/knockback-ragdoll-is-lagging/3441781, https://devforum.roblox.com/t/player-falling-off-moving-platform/2525985, https://devforum.roblox.com/t/preventing-anti-exploit-false-positives/280892, https://devforum.roblox.com/t/making-a-good-speed-hack-detector/2026856
- GitHub repository search (read: listing metadata only): `lisphm/A-Chassis` (MPL-2.0, last push 2026-10), `weenachuangkud/FastCast2` (last push 2026-11)
- Not reachable: devforum.roblox.com and create.roblox.com directly (search summaries and the docs mirror only); per-repository GitHub API. No evidence found: an official description of what `NextGenerationPhysicsSolver` changes; measurements of server authority prediction on high-speed constraint vehicles; an official number for vehicles per server.
