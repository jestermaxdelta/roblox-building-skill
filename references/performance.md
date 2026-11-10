# Performance: budgets, profiling, rendering, streaming, physics, VFX, loading

What this is: frame and memory budgets, the profiling workflow, engine-feature status and the fix for each cost centre. Open it when setting budgets for a new game, or jump to "Level-up audit" when a live game lags, crashes or loads slowly. Distilled from knowledge-base sections 5.1–5.6, 5.9, 5.12 and 4.9; platform facts re-checked against `Roblox/creator-docs` on 2026-11-10. Design for a 3 GB Android phone first. Tags: `[official]` docs, `[community]` forum practice, `[VS]` version-sensitive (device statistics change yearly; several engine features are new), `[house]` house estimate.

## Frame budgets and device targets

Measure milliseconds per frame, not FPS; consistency beats the average.

| Target | Budget | Use |
|---|---|---|
| 30 FPS | 33.33 ms | Floor for the lowest-end phones; never drop below |
| 60 FPS | 16.67 ms | Default target and the server heartbeat cap |
| 72 FPS | 13.9 ms | Standalone VR (Quest 2) |
| 120 / 240 FPS | 8.33 / 4.17 ms | High-refresh desktops |

Device reality `[VS]`: Android is about 65% of players; about 60% of Android devices have 2–4 GB RAM; more than half score 10k–20k on Passmark. Test on an Infinix Smart 9, Moto G05, Oppo A18 or Fire HD 10 (2023) for the low end and a Galaxy S22 Ultra for the high end. Run a 10–15 minute thermal session; the Device Emulator gets screen size right but not memory or performance.

| Budget | Value | Source |
|---|---|---|
| Draw calls in view | < 1,000 | Doc baseline example |
| Triangles in view | < 1,000,000 | Doc baseline example |
| Triangles per mesh | ≤ 20,000 (import limit, not a target) | Doc |
| Long-running script work | about 5 ms per frame, then yield | Doc |
| Server memory | < 50% of (6.25 GiB + 100 MiB × peak players); the dashboard chart hides the total, so also stay < 3 GB | Doc |
| Client memory, whole app | < 1.3 GB so 2 GB phones survive | `[community]` Roblox staff article |
| Stricter working budget | 500 draw calls and 500k triangles in view | `[community]` same article |
| Client crash rate | investigate above 2–3% | Doc |
| Particles | ≤ 400/s per emitter (100/s on mobile); lifetime ≤ 20 s | Doc |
| Simultaneous `Highlight`s | ≤ 255 (extras silently ignored) | Doc |
| Textures | most ≤ 512², minor ≤ 256², hero ≤ 1024² | Doc |
| Client Luau per frame | ≤ 3–4 ms | House |
| Client physics per frame | ≤ 2–3 ms | House |
| Render CPU (Prepare + Perform) | ≤ 6 ms on mid mobile | House |
| Unique textures in view | ≤ 40–60 at ≤ 512² | House |
| Shadow-casting lights in view | ≤ 2–4 | House |
| Join to playable, low-end Android | ≤ 10–15 s | House |
| Per-frame remotes | ≤ 10–20 Hz, deltas | House |

Server heartbeat below about 50 Hz is an incident (house threshold). Server memory does not shrink when players leave; log `DataModel.ServerLowMemoryWarning`.

Frame order for scripts: PreRender (camera only), PreAnimation, PreSimulation (set forces and `Motor6D.Transform`), physics, PostSimulation/Heartbeat (read final positions). `WaitingHybridScriptJob` resumes `task.wait` callers about 30 times a second with a budget; exceed it and waits run late.

Memory labels (F9 > Memory > PlaceMemory `[official]`): GraphicsTexture and GraphicsTextureCharacter (pixel count and unique count are all that matter; PNG compression and alpha removal do not help), GraphicsMeshParts (the importer does not de-duplicate meshes), PhysicsParts and PhysicsCollision (collision data is stored even with `CanCollide = false`), Sounds, LuaHeap, Instances, Signals, Animation, HttpCache. PlaceScriptMemory breaks script memory down per script and custom tag. UntrackedMemory and CoreMemory are not yours to fix.

## Profiling workflow

| Tool | Shortcut | Use |
|---|---|---|
| Developer Console | F9 | Memory per label, errors, network, server MicroProfiler recording |
| MicroProfiler | Ctrl+Alt+F6 (client), Ctrl+F6 (Studio) | Per-frame timing; Ctrl+P pauses; dumps open in a browser with flame graphs and diffs |
| Performance Stats | Ctrl+Alt+F7 | CPU, GPU, memory, network overlay |
| Debug stats | Shift+F1–F5 | Shift+F2 Render (draw calls, triangles); Shift+F3 streaming panels |
| Network Simulation | Alt+S in Studio | Latency and packet loss |
| Scene Analysis | Window > Performance Summary | Script memory, unparented instances, triangle categories, audio and animation memory |
| Luau heap snapshots, Script Profiler | Developer Console | Snapshot diffs for leaks (unique references, unparented instances); per-function CPU |
| Performance Dashboard | Creator Hub > Monitoring > Performance | Client: frame rate, crash rate and count, unexpected out-of-memory exits, memory and memory-% by OS, CPU time. Server: CPU time, frame rate, memory, memory by server age, cores used per server |
| Crashes | Creator Hub > Monitoring > Crashes | Server crashes by reason (out-of-memory vs platform); out-of-memory snapshots open as a treemap of the DataModel at crash time; CSV export |
| Print Join Size Breakdown | Studio setting | Largest instances replicated at join |

Mobile profiling: enable the MicroProfiler in the app settings and open `http://<phone-ip>:1338` from a computer on the same network. Red bars are GPU waits over 2.5 ms (fill rate, overdraw, transparency). Label hot code with `debug.profilebegin("Enemies.UpdateTargets")` / `debug.profileend()`.

Tag table: `physicsStepped`/`worldStep` → anchor, lower fidelity; `stepContacts` → simpler collision shapes; `stepWorldThrottled` → fewer unanchored assemblies; `stepHumanoid`/`stepAnimation` → disable unused states, AnimationController NPCs, client animation; `updateInvalidatedFastClusters` above about 4 ms → stop changing avatar parts every frame, add a Humanoid to models with moving skinned meshes; `ShadowMapSystem`/`LightGridCPU` → fewer shadowed lights, `CastShadow = false`; `UpdateView`/`RenderView` → fewer draw calls; `Pass3dAdorn` → fewer BillboardGuis; `fillGuiVertices` → avoid UIGradient and UICorner on changing text; `Dispatch StreamJob` → lower `StreamingTargetRadius`; `Sound/stepInstances` → fewer sounds; `ProcessPackets` → fewer and smaller remotes, no server tweens; `WaitingHybridScriptJob` → fewer `task.wait` loops. The renderer treats Transparency ≤ 0.01 as opaque. Parts cast shadows regardless of transparency, so every invisible helper needs `CastShadow = false`.

## Luau performance idioms

1. Event-driven before polling. 2. Chunk long work into about 5 ms slices with `task.wait()`. 3. Disconnect everything; destroy player and character instances on leave (`Workspace.PlayerCharacterDestroyBehavior` `[VS]` or `task.defer(player.Destroy, player)` on `PlayerRemoving`). 4. Parallel Luau for large independent computations, measured.

Language-level: build tables with one shape (literal with all fields); `__index` pointing at a table, not a function; never `getfenv`, `setfenv`, `loadstring` (they deoptimize the whole script); fastcalls (`math.floor`, `string.byte(s)`, `bit32.*`, `vector.*`, `buffer.*`); generalized iteration; `table.create(n)` for known sizes; no temporary tables or capturing closures in hot loops; pool short-lived tables; keep hot helpers `local function` for inlining.

`--!native` / `@native` `[VS]`: server scripts and Android clients only; helps math-, table- and buffer-heavy code; costs startup compile time and memory with a size limit (64K instructions per block, 1M per module); annotate parameter types; breakpoints disable it; check with `debug.dumpcodesize()`.

Anti-patterns: per-frame work that could run on change or at 5–10 Hz; creating `RaycastParams` or `OverlapParams` per call; server-side tweens of world objects; repeated `LoadAnimation` (use `Animator:GetTrackByAnimationId()`); `RequestQueueSize` as a loading gate.

## Rendering

Instancing: two MeshParts share a draw call only when they share the same MeshId and identical SurfaceAppearance (or matching TextureContent, or matching material). Upload each kit piece once and reuse its id; re-importing a scene creates duplicate ids (40 lamp posts become 40 draw calls). Audit:

```lua
local seen = {}
for _, d in workspace:GetDescendants() do
	if d:IsA("MeshPart") then seen[d.Name] = seen[d.Name] or {}; seen[d.Name][d.MeshId] = true end
end
for name, ids in seen do
	local n = 0; for _ in ids do n += 1 end
	if n > 1 then warn(name, "has", n, "different MeshIds — duplicate uploads?") end
end
```

Share SurfaceAppearances across kit pieces; tint with `SurfaceAppearance.Color` (measure whether tint variants still instance in your build). Merge only static, unique clusters, after layout is final. Decals, Textures and particles batch poorly.

Transparency: use 0 or 1; values between sort and overdraw (the classic mobile red bar). Avoid Glass and many partial Decals. Foliage uses cutout alpha (`AlphaMode = Transparency` with part Transparency 0).

Shadows and lights: shadows are off below graphics level 4, so gameplay must read without them. `CastShadow = false` on small props, distant geometry, fast movers, VFX hosts and every invisible helper. `Light.Shadows = false` by default; small `Range` and `Angle`; a PointLight in an Attachment is the cheap bulb. Under Realistic lighting, interiors need walls at least 1 stud thick (the tutorial uses 2.5-stud blockers) or light leaks.

LOD `[VS]`: `MeshPart.RenderFidelity` Automatic (full under 250 studs, medium 250–500, lowest beyond), Performance for foliage and clutter, Precise for hero close-ups only. SLIM (`Model.LevelOfDetail = SLIM`, `Workspace.EnableSLIMAvatars`) builds cloud-generated composite LODs for static models (needs streaming, a cloud-saved place and Team Create; keep extents around 64 studs; separate co-planar faces by 0.01 studs). Legacy `StreamingMesh` should be converted to SLIM.

Other costs: skinned meshes in a model without a Humanoid rebuild FastClusters every move; Highlights cost about 1 ms GPU on mobile for the first one, toggle `Enabled` rather than create and destroy; many SurfaceGuis and BillboardGuis are expensive, especially in VR; built-in materials and MaterialVariants share engine textures.

## Streaming

Recommended `Workspace` settings: `StreamingEnabled = true`; `ModelStreamingBehavior = Improved`; `StreamingIntegrityMode = PauseOutsideLoadedArea`; `StreamingMinRadius = 64`; `StreamingTargetRadius = 1024` by default, lower for memory (it must exceed MinRadius); `StreamOutBehavior = Opportunistic`; `EnableSLIMAvatars = Enabled` `[VS]`; `PredictiveStreamingMode` opt-in `[VS]`; `Player.FrustumStreaming` left at Default (off) unless the game has scopes, racing or a free camera, then Automatic `[VS]`.

Behaviour: only Workspace descendants stream (ReplicatedStorage replicates in full at join, so do not park maps there); streamed-out instances are parented to `nil`, not destroyed; unanchored assemblies stream whole, anchored geometry per part; extra `ReplicationFocus` costs about as much as another player; debug view is Shift+F3 then Shift+1 to the fourth panel.

Model streaming modes: Default/Nonatomic for large static scenery; **Atomic** for interactive props (doors, shops, vehicles) so the whole model arrives together; Persistent rarely (global landmarks only); PersistentPerPlayer for a player's own plot. Flatten container hierarchies.

Code rules: never index Workspace content directly from a LocalScript (`WaitForChild(name, 10)` with a nil check, or tags with added/removed signals, which also handle re-streaming); spatial queries on the client see only loaded content, so keep gameplay checks on the server or in attributes on always-present containers; sounds, BillboardGuis, prompts and Touched handlers stop when their part streams out; call `player:RequestStreamAroundAsync(position)` before teleports; the loading screen never waits on a spatial instance; use `GuiService:SetGameplayPausedNotificationEnabled(false)` and `player.GameplayPaused` for a branded pause overlay; test with `StreamingTargetRadius = 64`.

## Engine features and status, late 2026 `[VS]`

Checked against the docs mirror on 2026-11-10. Re-check before relying on any row.

| Feature | Status | What it means for you |
|---|---|---|
| Occlusion culling | On by default `[official]`. It tunes itself down when it costs more than it saves, and a wall made of many small parts is not an occluder `[community: staff replies]` | Large contiguous shells (one wall mesh, terrain, building exteriors) hide what is behind them. It saves draw calls, not Luau: scripts for hidden objects still run, so gate them by distance or tag |
| Texture streaming | Automatic `[official]`: baseline quality first, then raised by free memory, distance and screen size. Covers MeshPart, SurfaceAppearance, Texture, Decal, MaterialVariant, Beam, ParticleEmitter | Texture budgets still apply: UI images are not covered, and unique pixel count is still the memory cost |
| Unified lighting | `Lighting.Technology` is deprecated; use `LightingStyle` (Soft or Realistic) plus `PrioritizeLightingQuality` `[official]`. Old mapping `[community: announcement]`: Future → Realistic + on; ShadowMap → Soft + on; Voxel → Soft + off | Mobile-first default is Soft. `PrioritizeLightingQuality = false` keeps view distance and drops shading first as quality scales down. Ship Realistic only if a low-end capture still holds 30 FPS |
| SLIM model and avatar LOD | Documented (see LOD above); needs streaming, a cloud-saved place and Team Create | First LOD lever for static kit models and crowds |
| Frustum streaming | `Player.FrustumStreaming`: Default (= Disabled), Disabled, Automatic, Enabled. Adds to the streaming radius, never replaces it; costs memory | Only for scopes, racing and free cameras |
| Native code generation | Server scripts and Android clients only `[official]` | Unchanged: measured hot maths only |
| Server authority | Full release in 2026 (see networking-and-security.md) | The server simulates everything and clients roll back and resimulate: profile server CPU and low-end client CPU before adopting |
| Extended Services for Compute | Paid: more than doubles per-player server CPU; first 100K playtime hours per month free, then $0.001 per playtime hour, billed while enabled `[official]` | Last resort after optimising. Roblox says most games see no benefit |
| `CollisionFidelity.Tunable` | `MeshPart.CollisionPrecision` slider: up is more precise and more expensive, down is coarser and cheaper `[official]` | Use instead of Precise where a Hull is too coarse |
| "Cores used per server" chart | Low core use with high server CPU time flags a Parallel Luau candidate `[official]` | Measure before adding Actors |

## Physics and collision

- Anchor all static geometry; for a welded mechanism anchor only the root. Anchoring saves physics CPU, not GPU.
- Sleep thresholds: linear 0.33 studs/s, rotational 0.42, acceleration 0.24 studs/s² blocks sleep; neighbours above 0.48 / 0.59 wake; 16.9 studs/s² acceleration wakes. Any physics property write wakes an assembly, so never write physics properties on idle props every frame. Debug with Visualization Options > Awake parts.
- `Workspace.PhysicsSteppingMethod = Adaptive` gives up to 2.5× speedup (240/120/60 Hz islands); use Fixed only for racing, destruction or complex mechanisms.
- Lower `FallenPartsDestroyHeight` to the map.
- Collision fidelity order, cheapest first: Box, Hull, Default, PreciseConvexDecomposition; `Tunable` with `CollisionPrecision` is newer `[VS]`. Collision data is stored even with `CanCollide = false`, so non-colliding meshes still get Box.

| Asset | Fidelity | Flags |
|---|---|---|
| Small props | Box | CanCollide on if bumpable; CanQuery off unless a hit target |
| Medium props (crates, benches, lamps) | Hull | CanCollide on |
| Walls, floors, cliffs | Box per module or a `_COL` mesh | CanCollide and CanQuery on |
| Doorways, arches, stairs | Precise sparingly, or convex pieces, or `_COL` proxy (3 boxes for a doorway, a ramp for stairs) | Find Precise parts with Explorer filter `CollisionFidelity=PreciseConvexDecomposition` |
| Foliage, cables, decals-on-mesh | Box | CanCollide, CanTouch, CanQuery off; tag `NonSolid`; trunks stay solid |
| Ragdolls and debris | Box or Hull | NoCollisionConstraint between limbs |
| Vehicles | Simplified hull mesh | Collision group "Vehicles"; visual mesh CanCollide off |

Making everything solid (house rule 2): (1) Box or Hull on the visual mesh with CanCollide on; (2) a Blender `_COL` proxy (`Transparency = 1`, `CanCollide = true`, `CanQuery = true`, `CanTouch = false`, `CastShadow = false`, `CollisionFidelity = Hull`) with the visual mesh set to `CanCollide = false`, `CanTouch = false`, `CollisionFidelity = Box`; (3) invisible primitive hull Parts for large simple volumes, same flags, never visible. Walk every asset type before shipping.

`CanTouch` off on almost everything except deliberate triggers. Trigger volume: `Transparency = 1`, `CanCollide = false`, `CanTouch = true` or `CanQuery = true`, `CastShadow = false`, `Anchored = true`; set `OverlapParams.RespectCanCollide` deliberately.

Collision groups: register once at server start with `Workspace:RegisterCollisionGroup` and `CollisionGroupSetCollidable` (old PhysicsService methods are deprecated). Use them for player-player, debris and cosmetic cases only; never exclude a visible object from player collision.

`Touched` fires only from physical movement, needs a debounce and is spoofable by the owning client; use spatial queries for gameplay (`Raycast`, `GetPartBoundsInBox`, `GetPartBoundsInRadius`, `GetPartsInPart`, `Blockcast`/`Spherecast`/`Shapecast` for fast projectiles). Reuse params, cap `MaxParts`, dedupe hits by model, and validate on the server. `BindToCollisionSummaries` is newer `[VS]`.

Network ownership: hand vehicles to the driver on `Occupant` change and back with `SetNetworkOwnershipAuto()`; `SetNetworkOwner(nil)` sparingly. Debug colours: green your client owns, red buffer zone, white/grey server or another client, black nobody. Server authority mode (`AuthorityMode = Server`) reached full release in 2026 `[VS]`; see networking-and-security.md before adopting it.

Humanoids: disable unused `HumanoidStateType`s with `SetStateEnabled`; AnimationController for static NPCs; play NPC animations on the client; spawn NPCs near players and pool them; animate via `Motor6D.Transform` in PreSimulation.

## Parallel Luau

Scripts run in parallel only under an `Actor`; scripts in one Actor run serially, so use more Actors than cores (for example 64 on 4 cores). `task.desynchronize()` or `ConnectParallel` enters the parallel phase; `task.synchronize()` returns before DataModel writes. Raycasts and spatial queries are read-parallel safe; most writes are not. `require` is not allowed in the parallel phase. Communicate with `Actor:SendMessage` / `BindToMessageParallel` and `SharedTable`. Good fits: bulk hit validation, procedural generation, pathfinding batches, large ECS updates. Anti-patterns: many serial/parallel switches per frame, one Actor per projectile.

## VFX, animation and audio budgets

- Particles: rate ≤ 400/s per emitter (100/s mobile), lifetime ≤ 20 s, flipbooks deactivate on low memory and cap at 30 fps, `LightEmission = 1` is additive, runtime property changes are costly (use `Emit(n)` bursts and `Enabled`). House budget: 6–10 ambient emitters in view at Rate ≤ 20, bursts of 5–30, one shared 512² or 1024² VFX atlas. Particles, beams and trails are 2D effects, not "visible objects"; 3D VFX meshes are still Blender models; VFX hosts are invisible helpers or `_Att` attachments.
- Replicate effects as one small event; each client builds the effect from pooled templates and culls beyond about 200 studs. Never create VFX or tween world objects on the server. Reduce effects when `GuiService.ReducedMotionEnabled` is true.
- Animation priorities, high to low: Action4, Action3, Action2, Action, Movement, Idle, Core. Animators must be created on the server; animations on a player's own character replicate from the client; NPC animations replicate only when played on the server, so ambient NPCs animate locally per client and only synchronised moments (boss attacks) play on the server. `LoadAnimation` always creates a new track; cache tracks. Remove unused KeyframeSequences before shipping. Blender animation goes through FBX (one track per file, Add Leaf Bones off, bones scale 1 rotation 0, root at origin, ≤ 4 influences per vertex).
- Audio `[VS]`: legacy `Sound` plus the newer `AudioPlayer`/`AudioEmitter`/`AudioListener`/`AudioDeviceOutput` with Wires and inline effects; prefer the new API for 3D and mixing. Import limits: mp3/ogg/wav/flac, under 20 MB and 7 minutes, ≤ 48 kHz. Upload quota conflict: the audio page says 2,000 per 30 days verified (100 unverified); the Open Cloud page says 100 verified (10 unverified); plan around the stricter numbers. Mix: one 2D soundbed plus 3D spot ambiences; layered loops of different lengths; cap concurrent one-shots (about 16) and pool; play UI sounds on the client; sounds on streamed-out parts stop; expose Music, SFX and Ambience sliders.

## Loading and join

Join order: ReplicatedFirst runs; the rest replicates (only the spawn area with streaming; ReplicatedStorage in full); the avatar loads; `game.Loaded` fires. Keep ReplicatedFirst and ReplicatedStorage lean; defer shop catalogue builds, analytics warm-up and decorative NPC spawns until the player is in control.

Custom loading screen: a ReplicatedFirst LocalScript parents a ScreenGui with `IgnoreGuiInset = true` to PlayerGui, calls `ReplicatedFirst:RemoveDefaultLoadingScreen()`, preloads only its own art, shows a Skip button after a few seconds, waits for `game:IsLoaded()` or skip, then fades out. Do not copy the docs' forced `task.wait(5)`. Never wait on a spatial instance or use `RequestQueueSize` as a progress bar. No offers or starter packs on the loading screen (house rule).

Preloading myths:

| Myth | Reality |
|---|---|
| "Preload everything to stop pop-in" | `ContentProvider:PreloadAsync(workspace)` adds straight to join time `[official]`. Preload only loading-screen art, key menu icons and spawn-area hero assets, behind a Skip button |
| "`RequestQueueSize == 0` means ready" | It fluctuates and is unreliable `[official]` |
| "Smaller PNG files use less memory" | Images are transcoded; only pixel count matters `[official]` |
| "The ReplicatedFirst timer is my load time" | It starts after ReplicatedFirst arrives and stops at `game.Loaded`; it misses connection and avatar load. Use a stopwatch from the Play tap: three runs on low-end Android over mobile data `[official]` |

A join that is slow for the size of the game usually means bulk in ReplicatedStorage, or an obfuscated free-model script that generates thousands of instances `[official]`. "Client API Calls in First 60s After Join" (top games only `[VS]`) should be dominated by asset delivery.

Hardware test matrix: one 2–4 GB Android phone, one mid-range phone, a tablet, a desktop, and a gamepad; measure join time, frame time and memory; run a 10–15 minute thermal session; check touch targets, text size, mid-session input switching and audio.

## Mobile crashes and memory

- Roblox cannot use all of a device's RAM; the OS and background apps take their share `[official]`. No official per-device megabyte limit was found. Working target: whole-app client memory under 1.3 GB for 2 GB phones `[community: staff article]`.
- Out-of-memory is one of the most common crash causes on low-end devices `[official: staff analytics post]`. The OS low-memory killer ending the app counts as a crash; low FPS does not (Android reclassification PSA dated November 4, year inferred as 2025 from thread order `[community]`), so compare crash rates only inside one period.
- Read three charts together: client crash rate (dashed line = noisy, use crash count), unexpected out-of-memory exits, and client memory usage percentage (an Android line near 100% means most Android devices are at risk) `[official]`.
- Reality check `[community]`: developers report cutting memory to about 1.2 GB and raising FPS with no visible drop in Android crash rate (one reported a steady 10–15%). Judge a fix by out-of-memory exits and memory-% for the 2–4 GB class, and decide deliberately whether sub-2 GB devices are supported.
- Usual causes, most common first `[house, from the docs' problem lists]`: unique texture pixels; streaming off or too many Persistent models; the same mesh or image uploaded under several ids; all audio loaded at once; instances cloned and never destroyed; leaked connections and per-player tables; huge `PreloadAsync` lists; streaming-in bursts after a teleport `[community bug report]`.
- Server side: an out-of-memory snapshot from a server that died minutes after start means a start-up spike; one from an old server means a leak. Filter by place version to find the update that introduced it `[official]`.

## Level-up audit: how to check an existing game

Order matters: live data, then one device, then static scans, then fixes by return on effort.

1. **Live data (10 min).** Performance and Crashes dashboards: note the worst OS and the worst metric (crash rate, memory-%, client FPS, server FPS, memory by server age). No dashboard access: start at step 2.
2. **Reproduce on a 2–4 GB Android phone.** Stopwatch the join. Walk to the busiest scene. Record F9 Memory (PlaceMemory labels), Shift+F2 draw calls and triangles, Shift+F5 FPS, and a 2-minute MicroProfiler dump. Keep playing 10–15 minutes for thermal drop.
3. **Classify** with the tag table above: memory, client CPU, GPU (red bars), server CPU, network or load time. Fix the worst class only.
4. **Static scan** in Studio Edit mode with sketches A and B (command bar, or Studio MCP `execute_luau` with `datamodel_type = Edit`). Both are read-only.
5. **Fix in ROI order** `[house]`: (1) streaming on, radius tuned, Persistent audit; (2) texture sizes and duplicate uploads; (3) anchor static parts, Box or Hull collision, `CanTouch` and `CastShadow` off on clutter; (4) partial transparency, particle rates, shadowed lights; (5) shared MeshIds and SurfaceAppearances; (6) per-frame loops to events, server tweens to clients, remote rates; (7) ReplicatedStorage diet and preload list; (8) leaks (respawn 20 times, memory returns to baseline); (9) SLIM, then Parallel Luau or `--!native` for measured hot spots.
6. **Re-measure** the same route on the same device. Ship one class of fix at a time and watch the dashboards for 48 hours `[house]`.

Sketch A, world census (unexecuted sketch):

```lua
--!strict
-- Read-only. Yields so execute_luau does not freeze Studio.
local counts: { [string]: number } = {}
local function bump(key: string) counts[key] = (counts[key] or 0) + 1 end
local seen = 0
for _, d in workspace:GetDescendants() do
	seen += 1
	if seen % 2000 == 0 then task.wait() end
	if d:IsA("BasePart") then
		if not d.Anchored then bump("unanchored") end -- welded mechanisms are fine; loose props are not
		if d.CanTouch then bump("canTouch") end
		if d.CastShadow and d.Size.Magnitude < 4 then bump("smallShadowCasters") end
		if d.Transparency > 0.01 and d.Transparency < 0.99 then bump("semiTransparent") end
		if d:IsA("MeshPart") then
			if d.CollisionFidelity == Enum.CollisionFidelity.PreciseConvexDecomposition then bump("preciseCollision") end
			if d.RenderFidelity == Enum.RenderFidelity.Precise then bump("preciseRender") end
		end
	elseif d:IsA("Light") then if d.Shadows then bump("shadowLights") end
	elseif d:IsA("ParticleEmitter") then if d.Rate > 100 then bump("emittersOver100") end
	elseif d:IsA("Model") then if d.ModelStreamingMode == Enum.ModelStreamingMode.Persistent then bump("persistentModels") end
	elseif d:IsA("LuaSourceContainer") then bump("scriptsInWorkspace")
	elseif d:IsA("Highlight") or d:IsA("BillboardGui") or d:IsA("SurfaceGui") or d:IsA("Sound") then bump(d.ClassName)
	end
end
local top: { { name: string, n: number } } = {}
for _, child in workspace:GetChildren() do table.insert(top, { name = child.Name, n = #child:GetDescendants() }) end
table.sort(top, function(a, b) return a.n > b.n end)
for i = 1, math.min(10, #top) do print(top[i].n, top[i].name) end
print("total", seen, counts)
print("ReplicatedStorage", #game:GetService("ReplicatedStorage"):GetDescendants(), "ReplicatedFirst", #game:GetService("ReplicatedFirst"):GetDescendants())
print("streaming", workspace.StreamingEnabled, workspace.StreamingMinRadius, workspace.StreamingTargetRadius)
```

Sketch B, texture inventory and oversized images (unexecuted sketch; `EditableImage` loading works only for images the creator owns and is memory-budgeted `[VS]`):

```lua
--!strict
local AssetService = game:GetService("AssetService")
local PROPS: { [string]: { string } } = {
	SurfaceAppearance = { "ColorMap", "NormalMap", "RoughnessMap", "MetalnessMap" }, MeshPart = { "TextureID" },
	Decal = { "Texture" }, Texture = { "Texture" }, ParticleEmitter = { "Texture" }, ImageLabel = { "Image" }, ImageButton = { "Image" },
}
local uses: { [string]: number } = {}
for _, root in { workspace, game:GetService("ReplicatedStorage"), game:GetService("StarterGui") } :: { Instance } do
	for _, d in root:GetDescendants() do
		for _, prop in PROPS[d.ClassName] or {} do
			local id = (d :: any)[prop]
			if type(id) == "string" and id ~= "" then uses[id] = (uses[id] or 0) + 1 end
		end
	end
end
local ids: { string } = {}
for id in uses do table.insert(ids, id) end
print(#ids, "unique texture ids") -- budget: 40–60 in view
for i = 1, math.min(#ids, 40) do -- measure in batches; rerun with an offset for the rest
	local ok, image = pcall(function() return AssetService:CreateEditableImageAsync(Content.fromUri(ids[i])) end)
	if ok and image then
		if image.Size.X > 512 or image.Size.Y > 512 then warn("over 512:", ids[i], image.Size, "uses", uses[ids[i]]) end
		image:Destroy()
	end
	task.wait()
end
```

The duplicate-MeshId sketch is under Rendering. For Precise collision, the Explorer filter `CollisionFidelity=PreciseConvexDecomposition` selects the parts directly.

| Symptom | Likely cause | Fix |
|---|---|---|
| Android crash rate high, memory-% near 100 | GraphicsTexture from many unique or large textures; streaming off | Sketch B; 512² default, trim sheets and atlases; streaming on, lower `StreamingTargetRadius` |
| Crashes rise after an update | Memory regression: new assets in ReplicatedStorage, duplicate uploads | Compare F9 labels before and after; filter the dashboards by place version; revert or dedupe |
| FPS falls after 10 minutes | Thermal throttling from sustained GPU or CPU load | Cut overdraw, shadowed lights and per-frame Luau; cap particle rates |
| Red MicroProfiler bars on phones | Fill rate: partial transparency, large particles, Glass | Transparency 0 or 1, cutout foliage, smaller and fewer particles |
| Draw calls over 1,000 | Duplicate MeshIds, unique SurfaceAppearances, many Decals | Duplicate-MeshId sketch; share appearances; SLIM for static models |
| `stepContacts` or `worldStep` high | Unanchored clutter, Precise collision, `CanTouch` everywhere | Sketch A; anchor, Box or Hull, `CanTouch` off |
| Server FPS below 60 with few players | Server tweens, per-frame loops over all players or NPCs, Humanoid NPCs | Move visuals to clients; event-driven code; AnimationController NPCs; Parallel Luau when "cores used" is low |
| Server memory climbs with server age | Leaked connections or per-player tables; instances never destroyed | Out-of-memory snapshot treemap; Luau heap snapshot diff; Trove per lifetime |
| Join over 15 s on phones | Heavy ReplicatedStorage or ReplicatedFirst, streaming off, long preload list | Print Join Size Breakdown; move maps to ServerStorage; preload only what the first screen shows |
| Pop-in or falling through the floor after teleport | No `RequestStreamAroundAsync`; interactive models not Atomic | Request the area first; Atomic on doors, shops and vehicles |
| Data ping far above network ping | Replication queue backlog: too many remotes or moving assemblies | Batch remotes to 10–20 Hz; anchor; under about 50 KB/s and 40–60 moving assemblies `[community: staff article]` |

## Performance review gate

- [ ] Low-end Android holds ≥ 30 FPS in the busiest scene; mid-range about 60; no spikes over about 50 ms in a 2-minute capture.
- [ ] Server heartbeat about 60 Hz with a full server; memory flat over a 1-hour soak and under 50% of the limit.
- [ ] Draw calls < 1,000 and triangles < 1 M in the worst view; Scene Analysis has no surprise categories.
- [ ] Hot loops labelled with `debug.profilebegin`; `--!native` only where measured.
- [ ] Streaming on with the settings above; works at `StreamingTargetRadius = 64`; interactive models Atomic; `RequestStreamAroundAsync` before teleports.
- [ ] All static geometry anchored; every visible object collides; no unapproved Precise fidelity; collision groups registered once.
- [ ] No server tweens or server-created VFX; particle rates within mobile caps; concurrent sounds capped.
- [ ] Join-to-playable ≤ 10–15 s on low-end Android; loading screen has Skip and no forced minimum.
- [ ] Performance Dashboard alerts for crash rate, heartbeat and memory; re-profile after every content update.
- [ ] `LightingStyle` and `PrioritizeLightingQuality` chosen deliberately and captured on the low-end phone; nothing relies on the deprecated `Technology` property.
- [ ] Live game: audit steps 1–6 run, with before and after numbers for the worst metric recorded in the audit report.

Grep `references/knowledge-base.md` for `## 5.1` through `## 5.6`, `## 5.9`, `## 5.12` and `## 4.9`.

## Sources

Accessed 2026-11-10. `Roblox/creator-docs` at commit ccc2b01 (2026-11-07).

- https://github.com/Roblox/creator-docs: `content/en-us/performance-optimization/{identify,improve,design,test-on-hardware}.md`, `production/analytics/{performance,crashes}.md`, `studio/optimization/memory-usage.md`, `workspace/streaming/{slim,frustum}.md`, `parts/{textures-decals,meshes}.md`, `luau/native-code-gen.md`, `cloud-services/extended-services.md`, `reference/engine/classes/{Lighting,AssetService,EditableImage}.yaml` (read)
- https://devforum.roblox.com/t/real-world-building-and-scripting-optimization-for-roblox/3127146 (search summary; staff article: 1.3 GB, 500 draws / 500k triangles, 50 KB/s)
- https://devforum.roblox.com/t/analytics-optimize-low-end-android-crash-rates-server-memory-and-cpu-performance/3145364 (search summary)
- https://devforum.roblox.com/t/psa-mobile-client-crash-reclassification-in-creator-hub/4053071 (search summary)
- https://devforum.roblox.com/t/android-crash-rates/3227626 (search summary; crash rate unchanged after optimisation)
- https://devforum.roblox.com/t/streaming-enabled-can-run-over-memory-management-to-crash-client/3305729 (search summary)
- https://devforum.roblox.com/t/occlusion-culling-now-live-in-roblox-client/3300953 and https://devforum.roblox.com/t/studio-beta-introducing-occlusion-culling/3250604 (search summary)
- https://devforum.roblox.com/t/let-there-be-unified-light-unified-lighting-is-fully-live/3401512 (search summary)
- https://devforum.roblox.com/t/analytics-diagnose-server-crashes-with-server-memory-snapshots/4525675 (search summary)
- No evidence found: an official per-device client memory crash limit; a controlled community before/after study of join time or mobile FPS.
