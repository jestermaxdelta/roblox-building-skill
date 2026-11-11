# Performance: budgets, profiling, rendering, streaming, physics, VFX, loading

What this is: frame and memory budgets, the profiling workflow, engine-feature status and the fix for each cost centre. Open it when setting budgets for a new game, or jump to "Level-up audit" when a live game lags, crashes or loads slowly. Distilled from knowledge-base sections 5.1–5.6, 5.9, 5.12 and 4.9; platform facts re-checked against `Roblox/creator-docs` (commit 7cbffff) and the DevForum announcements on 2026-11-11. Design for a 3 GB Android phone first. Tags: `[official]` docs, `[community]` forum practice, `[VS]` version-sensitive (device statistics change yearly; several engine features are new), `[house]` house estimate.

Contents: Start here by level · Frame budgets and device targets · Profiling workflow · Luau performance idioms · Rendering · Streaming · Engine features and status · Physics and collision · Parallel Luau · VFX, animation and audio budgets · Loading and join · Mobile crashes and memory · Level-up audit · Measured investigation by problem class (A compute, B memory leak, C network, D place size, E mobile tiers) · Review gate · Sources

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | (1) Keep streaming on. (2) Anchor everything that does not move. (3) Textures 512² or smaller. (4) Use events, not loops that run every frame. (5) Play on a real cheap phone before every publish | Parallel Luau, `--!native`, SLIM, bandwidth budgets |
| Intermediate | Fill the budget table with your own measured numbers; MicroProfiler captures with your own labels; a collision-fidelity pass; effects built on clients; a lean ReplicatedStorage; dashboards checked after each update | Buffer packing, Actors |
| Expert | Leak hunts by slope with heap snapshot diffs; a per-player bandwidth budget with interest tiers; Parallel Luau and native code on measured hot paths; graphics tiers; a regression guard left behind by every fix | Nothing: read it all |

Terms: *frame time* is the milliseconds one frame takes (16.67 ms at 60 FPS). A *draw call* is one batch of geometry sent to the GPU. *Overdraw* is the same pixel painted several times, usually by transparent layers. *Heartbeat* is the server's simulation step, capped at 60 per second. *Data ping* is round-trip time through the replication queue, as opposed to raw network ping.

Related: lighting-and-atmosphere.md (cost of lights, shadows and post effects, low-detail order); vfx-and-juice.md (particle budgets and quality scaling); debugging-and-testing.md (leak hunting, Network Simulator); ui-input-crossplatform.md (UI performance).

## Frame budgets and device targets

Measure milliseconds per frame, not FPS; consistency beats the average.

| Target | Budget | Use |
|---|---|---|
| 30 FPS | 33.33 ms | Floor for the lowest-end phones; never drop below |
| 60 FPS | 16.67 ms | Default target and the server heartbeat cap |
| 72 FPS | 13.9 ms | Standalone VR (Quest 2) |
| 120 / 240 FPS | 8.33 / 4.17 ms | High-refresh desktops |

Device reality `[official][VS]`: Android is about 65% of a typical game's players; of those about 60% have 2–4 GB RAM, 35% have 4–8 GB and 5% more; more than half of all players score 10k–20k on Passmark. Test on an Infinix Smart 9, Moto G05, Oppo A18 or Fire HD 10 (2023) for the low end and a Galaxy S22 Ultra for the high end. Run a 10–15 minute thermal session; the Device Emulator gets screen size right but not memory or performance.

| Budget | Value | Source |
|---|---|---|
| Draw calls in the worst view | < 1,000 | House budget (decision-rules.md). The docs use this figure only as an example of a limit you might find on your baseline device |
| Triangles in the worst view | < 1,000,000 | House budget, same doc example |
| Frame rate | ≥ 30 FPS in the busiest scene on low-end Android; server heartbeat 60 Hz | House budget (decision-rules.md); 60 is the engine's heartbeat cap `[official]` |
| Triangles per mesh | ≤ 20,000 (import limit, not a target) | Doc |
| Long-running script work | about 5 ms per frame, then `task.wait()` | Doc example |
| Server memory | < 50% of (6.25 GiB + 100 MiB × peak players); the dashboard chart hides the total, so also stay < 3 GB | Doc |
| Client memory, whole app | Target < 1.0 GB in the heaviest area; ceiling 1.3 GB so 2 GB phones survive. Neither is an official limit: 1.3 GB is a Roblox engineer's advice, LihFolk says "well under 1 GB" | `[community: staff article, read]`; `[lihfolk]` |
| Stricter working budget | 500 draw calls and 500k triangles in scene, the article's target for 60 FPS on 90% of phones without quality scaling down | `[community: staff article, read]` |
| Client crash rate | investigate above 2–3% | Doc |
| Particles | ≤ 400/s per emitter (100/s on mobile); lifetime ≤ 20 s | Doc |
| Simultaneous `Highlight`s | ≤ 255 (extras silently ignored) | Doc |
| Textures | most ≤ 512², minor ≤ 256² (doc); hero ≤ 1024² (house) | Doc and house |
| Client Luau per frame | ≤ 3–4 ms | House |
| Client physics per frame | ≤ 2–3 ms | House |
| Render CPU (Prepare + Perform) | ≤ 6 ms on mid mobile | House |
| Unique textures in view | ≤ 40–60 at ≤ 512² | House |
| Shadow-casting lights in view | ≤ 2–4 | House |
| Join to playable, low-end Android | ≤ 10–15 s | House |
| Repeating state remotes | ≤ 10–20 Hz, deltas only | House |

Server heartbeat below about 50 Hz is an incident (house threshold). Server memory does not shrink when players leave. Connect `DataModel.ServerLowMemoryWarning` to log and to drop non-essential caches; it can fire repeatedly and does not mean a shutdown is certain `[official]`.

Frame order for scripts: PreRender (camera only), PreAnimation, PreSimulation (set forces and `Motor6D.Transform`), physics, PostSimulation/Heartbeat (read final positions). `WaitingHybridScriptJob` resumes threads waiting in `WaitForChild` or legacy `wait()` about 30 times a second with a time budget; exceed it and they resume late `[official]`. `task.wait` resumes on Heartbeat instead.

Memory labels (F9 > Memory > PlaceMemory `[official]`): GraphicsTexture and GraphicsTextureCharacter (pixel count and unique count are all that matter; PNG compression and alpha removal do not help), GraphicsMeshParts (the importer does not de-duplicate meshes), PhysicsParts (`BaseParts` in `Enum.DeveloperMemoryTag`) and PhysicsCollision (collision data is stored even with `CanCollide = false`), Sounds, LuaHeap, Instances, Signals, Animation, HttpCache. PlaceScriptMemory breaks script memory down per script and custom tag. UntrackedMemory and CoreMemory are not yours to fix.

## Profiling workflow

| Tool | Shortcut | Use |
|---|---|---|
| Developer Console | F9 | Memory per label, errors, network, server MicroProfiler recording |
| MicroProfiler | Ctrl+F6 in Studio and the desktop client (the MicroProfiler page; two other doc pages print Ctrl+Alt+F6, so try both). Phones: see below | Per-frame timing; Ctrl+P pauses; Timers mode lists labels by time and call count; dumps open in a browser with flame graphs and before/after diffs. Server: F9 > MicroProfiler > Server records up to 60 frames after a delay of up to 4 s (edit permission needed) `[official]` |
| Performance Stats | Ctrl+Alt+F7 | CPU, GPU, memory, network overlay |
| Debug stats | Shift+F1–F5 in the client; Ctrl+Shift+F1–F5 in Studio | F2 Render (draw calls, triangles); F3 Network (data ping; Shift+1 cycles panels, the fourth is Streaming); F5 Summary (FPS) |
| Network Simulator `[VS]` | Studio: Test > Device Simulator > Network pill (beta: enable "New Device Simulator" under File > Beta Features) | Latency, jitter and packet loss presets (Home Wi-Fi, 4G, 3G); values and usage in debugging-and-testing.md |
| Scene Analysis | Studio, during a play test: Window > Performance Summary > Scene Analysis | Treemaps of script memory, unparented instances, instance composition, audio and animation memory, triangles and draw calls by pass. Same data from `SceneAnalysisService` (through the Studio MCP) `[official]`. Numbers are your PC's, not a phone's |
| Luau heap snapshots, Script Profiler | Developer Console | Snapshot diffs for leaks (unique references, unparented instances); per-function CPU |
| Performance Dashboard | Creator Hub > Monitoring > Performance | Client: frame rate, crash rate and count, unexpected out-of-memory exits, memory and memory-% by OS, CPU time. Server: CPU time, frame rate, memory, memory by server age, cores used per server. Break any client chart down by Place Version |
| Alerts | Creator Hub > Configurations > Alerts | Up to 20 per game on any dashboard metric (static threshold or change against the previous hour, day or week), delivered to a webhook; needs 100 daily users `[official]` |
| `Stats` service | Script | `SceneDrawcallCount`, `SceneTriangleCount`, `FrameTime` (client), `HeartbeatTime` (server), `DataReceiveKbps`, `InstanceCount`, `GetMemoryUsageMbForTag`: use them for budget assertions and soak logs `[official]` |
| Crashes | Creator Hub > Monitoring > Crashes | Server crashes by reason (out-of-memory vs platform); out-of-memory snapshots open as a treemap of the DataModel at crash time; CSV export |
| Print Join Size Breakdown | Studio setting | Largest instances replicated at join |

Mobile profiling: turn the MicroProfiler on in the in-game Settings menu and open the address it shows (for example `http://<phone-ip>:1338`) from a computer on the same network; it sends the last 30 frames, or add `/90` to the URL for 90. Frame bars: orange means jobs (scripts, physics, animation) took longer than rendering, blue means rendering took longer, red means rendering took longer and the GPU wait passed 2.5 ms (fill rate, overdraw, large textures) `[official]`. Label hot code with `debug.profilebegin("Enemies.UpdateTargets")` / `debug.profileend()`.

Tag table: `physicsStepped`/`worldStep` → anchor, lower fidelity; `stepContacts` → simpler collision shapes; `stepWorldThrottled` → fewer unanchored assemblies; `stepHumanoid`/`stepAnimation` → disable unused states, AnimationController NPCs, client animation; `updateInvalidatedFastClusters` above about 4 ms → stop changing avatar parts every frame, add a Humanoid to models with moving skinned meshes; `ShadowMapSystem`/`LightGridCPU` → fewer shadowed lights, `CastShadow = false`; `UpdateView`/`RenderView` → fewer draw calls; `Pass3dAdorn` → fewer BillboardGuis; `fillGuiVertices` → avoid UIGradient and UICorner on changing text; `Dispatch StreamJob` → lower the streaming radii; `Sound/stepInstances` → fewer sounds; `ProcessPackets` → fewer and smaller remotes, no server tweens; `WaitingHybridScriptJob` → fewer threads parked in `WaitForChild` or legacy `wait()`; `GC` → fewer temporary tables. The renderer treats Transparency ≤ 0.01 as opaque. Parts cast shadows regardless of transparency, so every invisible helper needs `CastShadow = false`.

## Luau performance idioms

1. Event-driven before polling. 2. Chunk long work into about 5 ms slices with `task.wait()`. 3. Disconnect everything; destroy player and character instances on leave (`Workspace.PlayerCharacterDestroyBehavior` `[VS]` or `task.defer(player.Destroy, player)` on `PlayerRemoving`). 4. Parallel Luau for large independent computations, measured.

Language-level: build tables with one shape (literal with all fields); `__index` pointing at a table, not a function; never `getfenv`, `setfenv`, `loadstring` (they deoptimize the whole script); fastcalls (`math.floor`, `string.byte(s)`, `bit32.*`, `vector.*`, `buffer.*`); generalized iteration; `table.create(n)` for known sizes; no temporary tables or capturing closures in hot loops; pool short-lived tables; keep hot helpers `local function` for inlining.

`--!native` / `@native` `[VS]`: server scripts and Android clients only; helps math-, table- and buffer-heavy code; costs startup compile time and memory with a size limit (64K instructions per block, 1M per module); annotate parameter types; breakpoints disable it; check with `debug.dumpcodesize()`.

Anti-patterns: per-frame work that could run on change or at 5–10 Hz; creating `RaycastParams` or `OverlapParams` per call; server-side tweens of world objects; repeated `LoadAnimation` (use `Animator:GetTrackByAnimationId()`); `RequestQueueSize` as a loading gate.

## Rendering

Instancing: two MeshParts share a draw call only when they share the same MeshId and identical SurfaceAppearance (or matching TextureContent, or matching material). Upload each kit piece once and reuse its id; re-importing a scene creates duplicate ids (40 lamp posts become 40 draw calls). Audit:

```lua
-- fragment (unexecuted sketch); run in edit mode
local seen = {}
for _, d in workspace:GetDescendants() do
	if d:IsA("MeshPart") then seen[d.Name] = seen[d.Name] or {}; seen[d.Name][d.MeshId] = true end
end
for name, ids in seen do
	local n = 0; for _ in ids do n += 1 end
	if n > 1 then warn(name, "has", n, "different MeshIds: duplicate uploads?") end
end
```

Share SurfaceAppearances across kit pieces; tint with `SurfaceAppearance.Color` (measure whether tint variants still instance in your build). Merge only static, unique clusters, after layout is final. Decals, Textures and particles batch poorly.

Transparency: use 0 or 1; values between sort and overdraw (the classic mobile red bar). Avoid Glass and many partial Decals. Foliage uses cutout alpha (`AlphaMode = Transparency` with part Transparency 0).

Shadows and lights: shadows are off below graphics level 4, so gameplay must read without them. `CastShadow = false` on small props, distant geometry, fast movers, VFX hosts and every invisible helper. `Light.Shadows = false` by default; small `Range` and `Angle`; a PointLight in an Attachment is the cheap bulb. Under Realistic lighting, interiors need walls at least 1 stud thick (the tutorial uses 2.5-stud blockers) or light leaks.

LOD `[VS]`: `MeshPart.RenderFidelity` Automatic (full under 250 studs, medium 250–500, lowest beyond), Performance for foliage and clutter, Precise for hero close-ups only. SLIM (`Model.LevelOfDetail = SLIM`, `Workspace.EnableSLIMAvatars`) builds cloud-generated composite LODs that stay visible when the model streams out. It needs streaming, a place saved to Roblox and Team Create; it works only for static models with no Humanoid and no runtime changes; keep each model's extents around 64 studs and separate co-planar faces by 0.01 studs; where a platform lacks SLIM the model falls back to no LOD `[official]`. Convert legacy `StreamingMesh` models to SLIM.

Other costs: skinned meshes in a model without a Humanoid rebuild FastClusters every move; Highlights cost about 1 ms GPU on mobile for the first one, toggle `Enabled` rather than create and destroy; many SurfaceGuis and BillboardGuis are expensive, especially in VR; built-in materials and MaterialVariants share engine textures.

## Streaming

Recommended `Workspace` settings: `StreamingEnabled = true`; `ModelStreamingBehavior = Improved`; `StreamingIntegrityMode = PauseOutsideLoadedArea`; `StreamingMinRadius = 64`; `StreamingTargetRadius = 1024` by default, lower for memory (it must exceed MinRadius); `StreamOutBehavior = Opportunistic` (the default, `LowMemory`, unloads only under memory pressure); `EnableSLIMAvatars = Enabled` `[VS]`; `PredictiveStreamingMode` opt-in `[VS]`; `Player.FrustumStreaming` left at Default (off) unless the game has scopes, racing or a free camera, then set to Automatic from a server script `[VS]`. All `Workspace` streaming properties are set in Studio, not by script.

Behaviour: only Workspace descendants stream (ReplicatedStorage replicates in full at join, so do not park maps there); streamed-out instances are parented to `nil`, not destroyed; unanchored assemblies stream whole, anchored geometry per part; extra `ReplicationFocus` costs about as much as another player; debug view is Shift+F3 then Shift+1 to the fourth panel.

Model streaming modes: Default/Nonatomic for large static scenery; **Atomic** for interactive props (doors, shops, vehicles) so the whole model arrives together; Persistent rarely (a few parts client scripts must always find; wait for `Workspace.PersistentLoaded`); PersistentPerPlayer for a player's own plot. Flatten container hierarchies.

Code rules: never index Workspace content directly from a LocalScript (`WaitForChild(name, 10)` with a nil check, or tags with added/removed signals, which also handle re-streaming); spatial queries on the client see only loaded content, so keep gameplay checks on the server or in attributes on always-present containers; sounds, BillboardGuis, prompts and Touched handlers stop when their part streams out; call `player:RequestStreamAroundAsync(position)` before teleports; the loading screen never waits on a spatial instance; use `GuiService:SetGameplayPausedNotificationEnabled(false)` and `player.GameplayPaused` for a branded pause overlay; test with `StreamingTargetRadius = 64`.

## Engine features and status, late 2026 `[VS]`

Checked against the docs mirror on 2026-11-10. Re-check before relying on any row.

| Feature | Status | What it means for you |
|---|---|---|
| Occlusion culling | On for every game and platform, no setting (Windows 2024-12, all platforms 2025-01-27, terrain 2025-06-23) `[official: announcement, read]`. Not culled: avatars, lights, VFX, UI, shadows and shadow casters. Highly detailed meshes and parts that are small on screen do not act as occluders, and the engine may draw a hidden object when checking would cost more | Large simple shells (one wall mesh, terrain, building exteriors) hide what is behind them; a wall of many small parts does not. It saves draw calls, not Luau: scripts for hidden objects still run, so gate them by distance or tag. Staff measured about 33% lower P10 Android frame time in one dense event game; open arenas gain little |
| Texture streaming | Automatic `[official]`: baseline quality first, then raised by free memory, distance and screen size. Covers MeshPart, SurfaceAppearance, Texture, Decal, MaterialVariant, Beam, ParticleEmitter and base materials | Texture budgets still apply: UI images are not covered, and unique pixel count is still the memory cost. The docs prefer separate textures to atlases unless the atlas sits on parts that batch: asking for one sharp tile streams the whole atlas at that size |
| Unified lighting | `Lighting.Technology` is deprecated; use `LightingStyle` (Soft or Realistic) plus `PrioritizeLightingQuality` `[official]`. Old mapping `[official: announcement 2025-01-21, read]`: Future → Realistic + on; ShadowMap → Soft + on; Voxel → Soft + off | Mobile-first default is Soft. `PrioritizeLightingQuality = false` keeps view distance and drops shading first as quality scales down. Ship Realistic only if a low-end capture still holds 30 FPS |
| SLIM model and avatar LOD | Documented (see LOD above); needs streaming, a cloud-saved place and Team Create | First LOD lever for static kit models and crowds |
| Frustum streaming | `Player.FrustumStreaming` (server-set): Default (= Disabled), Disabled, Automatic, Enabled. Adds the camera's view volume to the streaming radius, never replaces it; costs memory and ignores occlusion; the engine switches it off on clients whose draw distance has dropped to the target radius `[official]` | Only for scopes, racing and free cameras |
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

Making everything solid (house rule 2): (1) Box or Hull on the visual mesh with CanCollide on; (2) a Blender `_COL` proxy (`Transparency = 1`, `CanCollide = true`, `CanQuery = true`, `CanTouch = false`, `CastShadow = false`, `CollisionFidelity = Hull`) with the visual mesh set to `CanCollide = false`, `CanTouch = false`, `CollisionFidelity = Box`; (3) invisible primitive hull Parts for large simple volumes, same flags, never visible. Exceptions: held tools, viewmodels and transient effect meshes do not collide; foliage canopies and cables may be `NonSolid`; skinned meshes collide in their rest shape only, so animated bodies get a `_COL` proxy. Walk every asset type before shipping.

`CanTouch` off on almost everything except deliberate triggers. Trigger volume: `Transparency = 1`, `CanCollide = false`, `CanTouch = true` or `CanQuery = true`, `CastShadow = false`, `Anchored = true`; set `OverlapParams.RespectCanCollide` deliberately.

Collision groups: register them in Studio's Collision Groups editor, or once at server start with `workspace:RegisterCollisionGroup` and `workspace:CollisionGroupSetCollidable` (the `PhysicsService` equivalents still work; only `SetPartCollisionGroup` is deprecated: set `part.CollisionGroup`) `[official]`. Use them for player-player, debris and cosmetic cases only; never exclude a visible object from player collision.

`Touched` fires only from physical movement, needs a debounce and is spoofable by the owning client; use spatial queries for gameplay (`Raycast`, `GetPartBoundsInBox`, `GetPartBoundsInRadius`, `GetPartsInPart`, `Blockcast`/`Spherecast`/`Shapecast` for fast projectiles). Reuse params, cap `MaxParts`, dedupe hits by model, and validate on the server. For contact points and impact strength use `BasePart:BindToCollisionSummaries(callback)` `[VS]`.

Network ownership (rules and sketch in physics-and-vehicles.md): give a vehicle to its driver on `Occupant` change and to the server (`SetNetworkOwner(nil)`) or anchor it when parked, because automatic ownership lets the nearest client grab it; anchoring then unanchoring resets ownership, so set it again. Debug colours: green your client owns, red buffer zone, white/grey server or another client, black nobody. Server authority mode (`AuthorityMode = Server`) reached full release in 2026 `[VS]`; see networking-and-security.md before adopting it.

Humanoids: disable unused `HumanoidStateType`s with `SetStateEnabled`; AnimationController for static NPCs; play NPC animations on the client; spawn NPCs near players and pool them; animate via `Motor6D.Transform` in PreSimulation.

## Parallel Luau

Scripts run in parallel only under an `Actor`; scripts in one Actor run serially, so use more Actors than cores (for example 64 on 4 cores). `task.desynchronize()` or `ConnectParallel` enters the parallel phase; `task.synchronize()` returns before DataModel writes. Raycasts and spatial queries are read-parallel safe; most writes are not. `require` is not allowed in the parallel phase. Communicate with `Actor:SendMessage` / `BindToMessageParallel` and `SharedTable`. Good fits: bulk hit validation, procedural generation, pathfinding batches, large ECS updates. Anti-patterns: many serial/parallel switches per frame, one Actor per projectile.

## VFX, animation and audio budgets

Craft and full rules live in vfx-and-juice.md, animation-and-rigs.md and audio-sfx-music.md. The performance facts:

- Particles `[official]`: at most 400/s per emitter (100/s on mobile), lifetime capped at 20 s, flipbooks capped at 30 fps; property writes at runtime are costly, so use `Emit(n)` bursts and `Enabled`. House budget: 6–10 ambient emitters in view at Rate ≤ 20, bursts of 5–30. VFX hosts are invisible helpers or `_Att` attachments; 3D VFX meshes are still Blender models.
- Replicate an effect as one small event; each client builds it from pooled templates and culls beyond about 200 studs. Never create VFX or tween world objects on the server.
- Do not scale effects from `UserGameSettings.SavedQualityLevel`: the docs say it fights the engine's automatic scaling `[official]`, and staff plan to deprecate it (vfx-and-juice.md). Use your own setting plus measured frame time (procedure E).
- Animation: `LoadAnimation` always creates a new track, so cache tracks per Animator; ambient NPCs animate on each client and only synchronised moments play on the server; remove Animation Editor data from rigs before shipping (it replicates on every clone `[official]`). Clips come from Blender as FBX or GLB; the Clip Editor importer (released 2026-03-31) reads every clip in one file `[VS]`. Export settings: animation-and-rigs.md.
- Audio: cap concurrent one-shots (about 16 `[house]`) and pool them; do not load every sound at join; play UI sounds on the client; sounds on streamed-out parts stop. `Sound/stepInstances` in the MicroProfiler is the cost of active sounds.

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

- Roblox cannot use all of a device's RAM; the OS and background apps take their share `[official]`. No official per-device megabyte limit was found. Working target: whole-app client memory under 1.3 GB for 2 GB phones `[community: staff article, read]`.
- Out-of-memory is one of the most common crash causes on low-end devices `[official: staff analytics post]`. A session the OS ends for any reason (the low-memory killer, and on some devices a swipe-to-close) counts as a crash; low FPS does not `[official: staff replies, read]`. Android crash telemetry was reclassified on 4 November 2025 and reported rates fell without any real change, so never compare a rate across that date.
- Read three charts together: client crash rate (dashed line = noisy, use crash count), unexpected out-of-memory exits, and client memory usage percentage (an Android line near 100% means most Android devices are at risk) `[official]`.
- Reality check `[community: one studio's report, October 2024, before the reclassification]`: average Android memory cut to 1.21 GB with no visible drop in a steady 10–15% Android crash rate (iOS about 2%). Judge a fix by out-of-memory exits and memory-% for the 2–4 GB class, and decide deliberately whether sub-2 GB devices are supported.
- Usual causes, most common first `[house, from the docs' problem lists]`: unique texture pixels; streaming off or too many Persistent models; the same mesh or image uploaded under several ids; all audio loaded at once; instances cloned and never destroyed; leaked connections and per-player tables; huge `PreloadAsync` lists; streaming-in bursts after a teleport `[community bug report]`.
- Server side: an out-of-memory snapshot from a server that died minutes after start means a start-up spike; one from an old server means a leak. Filter by place version to find the update that introduced it `[official]`.

## Level-up audit: how to check an existing game

Order matters: live data, then one device, then static scans, then fixes by return on effort.

1. **Live data (10 min).** Performance and Crashes dashboards (charts need at least 100 daily active users; switch "Filter By" from average to the percentile that shows the worst devices: P10 for frame rates, P90 for memory and CPU time): note the worst OS and the worst metric (crash rate, memory-%, client FPS, server FPS, memory by server age). No access or too few users: start at step 2.
2. **Reproduce on a 2–4 GB Android phone.** Stopwatch the join. Walk to the busiest scene. Record F9 Memory (PlaceMemory labels), draw calls and triangles (Shift+F2), FPS (Shift+F5), and MicroProfiler captures from the phone's web view at the worst moments (30–90 frames each). Keep playing 10–15 minutes for thermal drop.
3. **Classify** with the tag table above: memory, client CPU, GPU (red bars), server CPU, network or load time. Fix the worst class only, following the matching procedure (A–E) in the next section.
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

Sketch B, texture inventory and oversized images (unexecuted sketch). `CreateEditableImageAsync` loads only images owned by the game's creator or made in the game, returns `nil` when the editable-memory budget is used up, and an `EditableImage` is at most 1024², so a larger source cannot be told from a 1024² one `[official][VS]`:

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
| Draw calls over 1,000 | Duplicate MeshIds, unique SurfaceAppearances, many Decals, no large occluders | Duplicate-MeshId sketch; share appearances; SLIM for static models; Scene Analysis triangle view to see which pass |
| `stepContacts` or `worldStep` high | Unanchored clutter, Precise collision, `CanTouch` everywhere | Sketch A; anchor, Box or Hull, `CanTouch` off |
| Server FPS below 60 with few players | Server tweens, per-frame loops over all players or NPCs, Humanoid NPCs | Move visuals to clients; event-driven code; AnimationController NPCs; Parallel Luau when "cores used" is low |
| Server memory climbs with server age | Leaked connections or per-player tables; instances never destroyed | Out-of-memory snapshot treemap; Luau heap snapshot diff; Trove per lifetime |
| Join over 15 s on phones | Heavy ReplicatedStorage or ReplicatedFirst, streaming off, long preload list | Print Join Size Breakdown; move maps to ServerStorage; preload only what the first screen shows |
| Pop-in or falling through the floor after teleport | No `RequestStreamAroundAsync`; interactive models not Atomic | Request the area first; Atomic on doors, shops and vehicles |
| Data ping far above network ping | Replication queue backlog: too many remotes or moving assemblies | Procedure C: budget per category, interest tiers, batching; anchor props; the staff article suggests 40–60 moving assemblies as a ceiling `[community]`. The MicroProfiler's network capture shows traffic per frame |

## Measured investigation by problem class

Rules for every investigation `[lihfolk]`: name exactly one problem (compute, memory, load time or network) on one side (client or server); no fix without a measurement that points at it; one change per measurement; never conclude from Studio numbers; leave a guard behind (a profiler label, a budget assertion, a soak loop). Tool-by-tool detail and test harnesses: debugging-and-testing.md.

Record this before touching code and again after each change. Report format: symptom, measurement before, cause, fix, measurement after, guard.

| Metric | How to measure | Before | After |
|---|---|---|---|
| Frame time, typical and worst (ms) | MicroProfiler in the busiest scene on the target phone | | |
| Client memory at the heaviest point (MB) and top three labels | F9 > Memory | | |
| Server heartbeat and script time at a full server | F9 > Server Jobs > Heartbeat > Steps Per Sec, or the dashboard | | |
| Join to playable (s) | Stopwatch, three runs | | |
| Receive rate per player (kbps) and data ping minus network ping | Client: Shift+F3 (data ping) and Performance Stats (network ping); `Stats.DataReceiveKbps`. Server average: F9 > Server Stats | | |

**A. Compute (frame time).**

1. Reproduce with production-like load on the device class your players use. Two Studio clients are not a 30-player server.
2. Capture 30–90 frames (Ctrl+P pauses; on a phone use the web view). For the server use F9 > MicroProfiler > Server (60 frames at most), or the Script Profiler when you already know scripts are the cost.
3. Open Modes > Timers and read total time and call count per label. A label that costs 0.05 ms and runs 2,000 times a frame is invisible in the timeline and at the top of Timers `[lihfolk]`.
4. Name the family (scripts, physics, render, network, UI) and use the tag table above.
5. Wrap suspects in `debug.profilebegin("ConstantName")` and `debug.profileend()`: constant names, balanced, never across a yield.
6. Compare with the budget, change one thing, capture the same route again. Drop the old and new dumps into the web view together for a diff flame graph `[official]`.

Conflict: LihFolk splits a 60 FPS phone frame as rendering 8–10 ms, engine simulation 2–3 ms, your client scripts 2 ms, headroom 2–3 ms, and server scripts under about 5 ms per heartbeat at full player count. The house table above allows client Luau 3–4 ms. Both are estimates; treat 2 ms as the target and 3–4 ms as the ceiling.

**B. Memory leak (hunt by slope, not by snapshot)** `[lihfolk]`.

1. Check it is a leak. Memory rises for the first 5–10 minutes (modules, pools, streamed assets), and server memory never shrinks when players leave. Neither is a leak.
2. Keep the workload fixed, let it warm up, then take three or more samples and express growth as MB per hour or KB per repetition. Time to failure = (ceiling − current) ÷ slope. 60 MB per hour from 1.1 GB kills a 2 GB phone within one long session; the same slope on a 1.5 GiB server takes about 42 hours to reach 4 GiB. Client leaks are usually the urgent ones.
3. Find the label that grows: F9 > Memory, or the sampler below. `debug.setmemorycategory("Name")` in large scripts makes the script-memory view readable.
4. Amplify the leak by repeating the suspect action 100 times in a script (respawning, crossing a zone border, opening and closing a menu, equipping and unequipping).
5. Bisect: disable half the systems, rerun, keep the half where the slope remains.
6. Take Luau heap snapshot A after warm-up, run the loop 100 times, wait 10 s idle, take snapshot B. A count that grew by exactly 100, or a multiple, is the leak; growth of 3 or 7 is noise.
7. Usual holders: a connection per character to a long-lived signal; per-player tables never cleared; a loop spawned per object that never ends; caches keyed by user input with no cap; animation tracks loaded per use; tag handlers with no removal path; menus cloned on every open.
8. Keep the loop as a regression test. Never hide a leak with a periodic "clear everything".

```lua
--!strict
-- Unexecuted sketch: memory slope per label, once a minute. Start it after warm-up on a test server or client.
local Stats = game:GetService("Stats")
local TAGS = { Enum.DeveloperMemoryTag.LuaHeap, Enum.DeveloperMemoryTag.Instances, Enum.DeveloperMemoryTag.Signals,
	Enum.DeveloperMemoryTag.GraphicsTexture, Enum.DeveloperMemoryTag.GraphicsMeshParts, Enum.DeveloperMemoryTag.Sounds, Enum.DeveloperMemoryTag.Gui }
local first: { [Enum.DeveloperMemoryTag]: number } = {}
local startedAt = os.clock()
assert(Stats.MemoryTrackingEnabled, "per-tag memory is unavailable in this session") -- otherwise every read is 0
while true do
	local hours = (os.clock() - startedAt) / 3600
	for _, tag in TAGS do
		local mb = Stats:GetMemoryUsageMbForTag(tag)
		if first[tag] == nil then first[tag] = mb
		else print(tag.Name, string.format("%.1f MB, %+.1f MB/h", mb, (mb - first[tag]) / hours)) end
	end
	task.wait(60)
end
```

**C. Network (bandwidth and data ping).**

1. Symptom: data ping well above network ping, rubber-banding or late hits on phones.
2. Write a per-player budget by category. Example for a 20-player action game `[lihfolk, rule of thumb]`: character movement 8–12 kbps (engine-managed), unanchored props 0–4, combat remotes 6, enemy state 5, UI and economy 1, headroom 6: about 30 kbps server to client.
3. Do the fan-out arithmetic for every broadcast: bytes × rate × recipients. 50 enemies × 20 Hz × about 30 bytes is 30,000 bytes per second, 240 kbps per client, from 1,000 remote calls a second. With interest tiers (15 near at 20 Hz, 20 mid at 5 Hz, the rest on change) and one `buffer` per tick at about 8 bytes per enemy it is 400 updates, 3,200 bytes per second, about 26 kbps from 20 calls `[house arithmetic]`.
4. Interest tiers `[lihfolk]`: near (under 60 studs) 20 Hz with full state; mid (60–160) 5 Hz, position and coarse state; far (160–260) 1 Hz or on change; beyond that nothing. Add hysteresis at tier edges, tie distances to what the camera can show, and interpolate on the client (about 250 ms at 5 Hz).
5. Replaceable streams go on unreliable remotes in batches under about 900 bytes (the limit is 1,000). Animate on clients: a server tween replicates a property update every frame to every client that has the instance.
6. Measure by toggling one system and reading the receive rate; or count calls and approximate bytes per remote name inside the `Net` module to rank the top talkers; check the join payload with Print Join Size Breakdown. Record kbps per player with eight Studio clients in each release note.
7. Stop when data ping matches network ping. A system under about 10 kbps per player rarely repays packing work `[lihfolk]`.

Conflict: the staff article says "aim for under 50 KB/s network receive" per client (about 400 kbps) and 40–60 moving assemblies; LihFolk could find no documentation for the figure, treats it as folklore and budgets about 30 kbps. There is no documented per-client cap: use your own budget and the data-ping gap as the test.

**D. Place size and instance count** `[lihfolk, measured in its reference project]`. Count instances per top-level folder with replicated containers listed separately (sketch A). Keep backups, archives and import sources out of the place: export `.rbxm` files and rely on Version History. At about 1.07 million instances their project had Studio down to about 15 FPS on about 18 GB, with cloud saves timing out; its 600k-instance ReplicatedStorage hurt phone memory as much as join time. Split scripts long before about 200,000 characters (a cap they measured; undocumented `[VS]`). Delete only what is proven unreferenced, never on a name search alone.

**E. Mobile tiers** `[lihfolk]`. Offer an in-game graphics preset (performance, balanced, quality) that switches live. Choose the starting preset from measured frame time in the first seconds of play, and let a frame-time governor lower detail when the phone heats up (sketch in vfx-and-juice.md); do not read `SavedQualityLevel` (see VFX above). Every effect has a low tier, effects on other players are reduced first, ambient effects sleep with distance. Gameplay information (telegraphs, hit areas, timers) is identical on every tier. Each release: a 15-minute fixed route on a real phone (spawn, heaviest area, one full encounter, every major menu, one zone change), recording FPS, peak memory and crashes.

Not adopted from LihFolk: its per-asset content budgets (for example up to 140 beams and 30 emitters for one sword swing, 44 and 10 on low). They are specific to its project and exceed the mobile VFX budget in this file.

## Review gate

- [ ] Low-end Android holds ≥ 30 FPS in the busiest scene; mid-range about 60; no spikes over about 50 ms in a 2-minute capture.
- [ ] Server heartbeat about 60 Hz with a full server; memory flat over a 1-hour soak and under 50% of 6.25 GiB + 100 MiB × peak players.
- [ ] Draw calls < 1,000 and triangles < 1 M in the worst view; Scene Analysis has no surprise categories.
- [ ] Hot loops labelled with `debug.profilebegin`; `--!native` only where measured.
- [ ] Streaming on with the settings above; works at `StreamingTargetRadius = 64`; interactive models Atomic; `RequestStreamAroundAsync` before teleports.
- [ ] All static geometry anchored; every visible object collides; no unapproved Precise fidelity; collision groups registered once.
- [ ] No server tweens or server-created VFX; particle rates within mobile caps; concurrent sounds capped.
- [ ] Join-to-playable ≤ 10–15 s on low-end Android; loading screen has Skip and no forced minimum.
- [ ] Alerts set (Creator Hub > Configurations > Alerts) for client crash rate, server frame rate and server memory; re-profile after every content update.
- [ ] `LightingStyle` and `PrioritizeLightingQuality` chosen deliberately and captured on the low-end phone; nothing relies on the deprecated `Technology` property.
- [ ] Live game: audit steps 1–6 run, with before and after numbers for the worst metric recorded in the audit report.
- [ ] Every fix has a row in the report (symptom, before, cause, fix, after, guard); nothing was changed without a measurement pointing at it.
- [ ] Memory slope measured after warm-up (MB per hour) on client and server; the repetition loop kept as a regression test.
- [ ] Per-player bandwidth recorded for this release; broadcasts are interest-filtered; unreliable batches under 900 bytes.
- [ ] Graphics tiers exist, gameplay information is identical on all of them, and nothing reads `SavedQualityLevel`.

Grep `references/knowledge-base.md` for `## 5.1` through `## 5.6`, `## 5.9`, `## 5.12` and `## 4.9`.

## Sources

Accessed 2026-11-11. `Roblox/creator-docs` at commit 7cbffff (2026-11-10).

- https://github.com/Roblox/creator-docs: `content/en-us/performance-optimization/{identify,improve,design,test-on-hardware,monitor,scene-analysis}.md`, `performance-optimization/microprofiler/{index,modes,tag-table}.md`, `production/analytics/{performance,crashes,alerts}.md`, `studio/optimization/{memory-usage,scriptprofiler}.md`, `studio/network-simulator.md`, `workspace/streaming/{index,techniques,slim,frustum}.md`, `workspace/collisions.md`, `physics/{sleep-system,adaptive-timestepping}.md`, `parts/{textures-decals,meshes}.md`, `art/modeling/specifications.md`, `effects/particle-emitters.md`, `luau/native-code-gen.md`, `scripting/multithreading.md`, `cloud-services/extended-services.md`, `reference/engine/classes/{Workspace,Lighting,Highlight,AssetService,EditableImage,Stats,TriangleMeshPart,PhysicsService}.yaml`, `reference/engine/enums/DeveloperMemoryTag.yaml`, `reference/engine/libraries/debug.yaml` (read)
- https://devforum.roblox.com/t/3127146 (read; Roblox engineer's optimisation article, 2024-08-20: 1.3 GB, 500 draws and 500k triangles, 50 KB/s, 40–60 moving assemblies)
- https://devforum.roblox.com/t/3300953 (read; occlusion culling live, 2024-12-10, with updates to 2025-06-23: platforms, limits, measured gain)
- https://devforum.roblox.com/t/3401512 (read; unified lighting fully live, 2025-01-21: `Technology` mapping)
- https://devforum.roblox.com/t/4053071 (read; Android crash reclassification, 2025-11-07, and staff replies on what counts as a crash)
- https://devforum.roblox.com/t/3227626 (read; one studio's Android crash rates, 2024-10-25)
- https://devforum.roblox.com/t/3145364 (read, first post; low-end Android crash insight, 2024-09-03)
- https://devforum.roblox.com/t/3305729 (read, first post; bug report: streaming-in bursts exhausting memory)
- https://devforum.roblox.com/t/4525675 (read, first post; server memory snapshots, 2026-03-17)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/roblox-performance-audit/SKILL.md`, `LihFolk Vault V2/12 Performance Testing and Debugging/{Hunting Memory Leaks Step by Step, Network Bandwidth Budgets and Measuring Them, Mobile and Low-End Optimization, MicroProfiler Guide}.md`, `03 Architecture and Networking/Interest Management and Per-Player Replication.md` (read)
- Not verified: an official per-device client memory crash limit (none found); the Highlight cost of about 1 ms GPU on mobile and the sleep-related debug colours (carried from the knowledge base); a controlled before/after study of join time or mobile FPS.
