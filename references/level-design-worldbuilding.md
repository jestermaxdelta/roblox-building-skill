# Level design and worldbuilding: maps that guide, read and run on a phone

What this is: how to plan, lay out, build, dress, stream and test a Roblox map with a Blender kit, from the core loop down to the polish checklist. Open it before blocking out a map, when a genre needs its layout rules, or when a live map feels empty, cluttered or confusing (jump to §16 and §17). It extends `game-craft.md` §2 and §6 (jump formulas, teaching loop, generator rules), `art-pipeline-blender.md` (kit, collision, export) and `performance.md` (streaming settings, budgets) and does not repeat them; lighting is in `lighting-and-atmosphere.md`. Reference images for towns, hubs, biomes, interiors and obby or arena layouts (strong and weak, with what to study) are in `visual-library/environments-and-maps.md`; what makes a map read as generic and the whole-game art review are in `art-direction-and-quality-bar.md`. House rules hold throughout: every visible object is a Blender model with collision, and Roblox Terrain is used only with the owner's per-game approval. Tags: `[official]` Roblox docs, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (rules of thumb unless marked measured), `[VS]` version-sensitive, `[house]` house estimate.

## Contents

1 Plan from the core loop · 2 Metrics against the R15 avatar · 3 Layout archetypes · 4 Spawn and lobby · 5 Landmarks, sightlines, wayfinding · 6 Composition and density · 7 Layout by genre · 8 Blockout to final with a Blender kit · 9 Modular kit and trim · 10 Set dressing and environmental storytelling · 11 Workspace naming and folders · 12 Streaming-aware layout · 13 Collision, walkability, bounds · 14 Procedural generation · 15 Heatmaps and death maps · 16 Empty / cluttered / confusing · 17 Level-up table · Map polish checklist · Review gate · Sources

Routes: **empty, cluttered or confusing live map** → §16, §17, §5, §6, §4, then the polish checklist (about 120 lines). **New map** → §1, §2 table, §3, §4, §5, §6, §7 (your genre's row), §8 (about 190 lines). **First kit** → §8, §9, §11, then `blender-modeling-craft.md` "First kit walkthrough". Look at sheet 17 and `visual-library/environments-and-maps.md` rows 1–4 and the §G rows of your genre.

## Start here by level

| Level | Do these | Ignore for now |
|---|---|---|
| Beginner | Fill in the map brief (§1). Keep an R15 dummy in every blockout and use the metrics table (§2). Make the spawn face the first objective and one landmark (§4). Blockout, walk it on a phone, only then dress (§8). Run the polish checklist. | Generators, heatmaps, SLIM, pixel maths |
| Intermediate | Focal hierarchy and density gradient (§6). Genre layout numbers (§7). Pass folders and kit reuse (§8, §9, §11). Streaming-aware layout and teleport rules (§12). Collision and bounds sweep (§13). | Golden-hash tests, occluder shells |
| Expert | Angular-size and pixel maths for landmarks (§2, §5). Sight-line leak rays. Socket generators with validation and determinism tests (§14). Position, death and quit maps tagged by map version (§15). Occluder shells and SLIM far landmarks (§12). | Nothing; measure everything |

Terms: *blockout* = the level in plain boxes with no art; *critical path* = the minimum route to the next objective; *landmark* = a shape players orient by; *node* = a place where players stop and decide; *kit* = a small set of modular pieces that snap on one grid; *streaming* = the engine loading only the world near each player.

## 1. Plan the map from the core loop

A map is the loop made physical: it must teach the verbs in order, pace them, and put the spend on the way back to the action. Write one page before any geometry (adapted from the LihFolk world brief `[lihfolk]`):

```
MAP BRIEF: <name>                      Map version: v1 (bump on every layout change)
Loop served: <verb> → <reward> → <spend>; first fun action within __ s of spawn
Must teach, in order: 1 __  2 __  3 __   (one mechanic per space: show → try → test → combine)
Jobs, ranked: 1 new player reaches first action  2 returning player back into play
              3 core spend  4 status  5 social  6 live events
Archetype: hub-and-spoke / linear chain / open / arena / generated rooms; players here: typical __, max __
Metrics: avatar __ studs, WalkSpeed __, jump mode (height/power) __, safe gap __, door __, corridor __
Time budgets: spawn → first station __ s; station → station __ s; zone end to end __ s
Hero landmark: what, where, height (≥ 1.5× anything else), seen from spawn and every gate
Districts and paths: one purpose each; main path width __; marked by (value, light, trim)
Palette and mood: zone hue + one accent no other zone uses; lighting preset name
Not this: 3–5 looks the map must never have    Story moments: 2–3 "what happened here?" groups
Budgets: instances __, lights __ (shadowed __), unique meshes __, draw calls in the worst view __
```

- Rank the jobs. Jobs 1 and 2 set the spawn and the exits; jobs 3–6 fill the ring around them. Building the impressive jobs first and leaving 1–2 to chance is the standard hub failure `[lihfolk]`.
- Players feel time, not studs. At 16 studs/s, 100 studs is 6.25 s and 240 studs is 15 s. Budgets `[lihfolk]`: first station or exit under 15 s from spawn; a veteran out of the hub in under 20 s; station to station under 10 s; an ambient encounter every 150–300 studs (10–20 s). One production game halved a 460-stud walk to its first gate because new players were bored before the first fight `[lihfolk, measured in its reference project]`.
- Compare a new space with one players already like, not with a number: the same project shrank its zones 60% and reverted the same day `[lihfolk]`.
- Give a visible goal, then break the straight line to it so players pass the other draws on the way `[official: Beyond the Dark]`.
- Size the walkable core for the typical head count, not the maximum. A plaza feels occupied with about five players at a 40–70 stud radius `[lihfolk]`. Hub-centred games (trading, social) add nodes, not width.
- Plan pacing with the beat table and sawtooth in `game-craft.md` §2; every intensity-5 beat gets a rest before it.

## 2. Scale and metrics against the R15 avatar `[VS]`

Defaults `[official]`: `CharacterWalkSpeed` 16, `CharacterJumpHeight` 7.2, `CharacterJumpPower` 50, `CharacterMaxSlopeAngle` 89° (so slopes never stop a default character: steepness is a design choice, not an engine limit), gravity 196.2. Which jump value applies depends on `CharacterUseJumpPower`: the reference says it defaults to true (JumpPower 50, apex about 6.4 studs), but place templates differ, so read it in your place. No maximum step-up height is documented. Classic R15 is about 5 studs tall; realistic-proportion bodies reach 6–6.5 `[lihfolk]`. Custom rigs change every number below: write your own table on day one.

| Thing | House number (default avatar) | Why / source |
|---|---|---|
| Gameplay door, clear opening | ≥ 5 wide × 7.5–8 tall; 6+ where two players pass | Pathfinding agent is 4 wide (`AgentRadius` 2); camera needs head room |
| Combat lane, doorway in a shooter | ≥ 10 wide; walls ≥ 10 tall | Official greybox sample: two players abreast, walls not jumpable, camera clear `[official]` |
| Corridor / interior ceiling | 8–12 wide / 10–15 tall (2–3 avatar heights) | Lower ceilings push the default camera (occlusion mode Zoom) into the player's back `[lihfolk]` |
| Storey height | 10–12 floor to floor | `[lihfolk, measured on its house kit]` |
| Stairs | rise ≤ 1, tread ≥ 2 (2–3 typical; 27° at 1:2), width ≥ 6; collision is one ramp `_COL` | The official curriculum's stairs are blocks 1 high on 2.5 treads `[official]`. Ledges up to about 1 stud are walked up without a jump (observed `[lihfolk]`; no step limit is documented), so 1 is the ceiling for any step whose collision is not a ramp. This row is the skill's stair rule; `blender-modeling-craft.md` repeats it |
| Cover | low 2.5–3.5, full 7+; avoid 4–6 | Chest-high blocks aim and camera but cannot be vaulted `[lihfolk]` |
| Counter / window | top at 2.5–3; window 2–3 wide × 3–4 tall, sill at 3–4 | Reads as a window from 40 studs `[lihfolk, measured]` |
| Main path | 12–20 wide; side lanes narrower | LihFolk measured 20–34 with 9-stud characters; scaled to 5-stud avatars `[house]` |
| Spawn area | 12–20 across per simultaneous spawn; nothing overhead below 15 | `[lihfolk]` |
| Queue pad | about 4 studs of diameter per expected player | `[lihfolk]` |
| Prompt spacing | ≥ 2× `MaxActivationDistance` between prompt points (20+ at a 10-stud range) | Stops prompts flickering between stations `[lihfolk]` |
| Flat jump | critical-path gap ≤ 5.7 (JumpPower 50) or 6.1 (JumpHeight 7.2); comfortable ledge 5 | Derivation in `game-craft.md` §2 |
| Hero landmark | ≥ 1.5× the next tallest thing; ≥ 3–5° of view where needed | Height ≥ 0.05–0.09 × viewing distance (computed) |

Jump reach changes with height (computed for JumpHeight 7.2 at 16 studs/s; root travel, add 1–2 studs edge to edge and calibrate on a gap ladder): landing +7 studs → 5.1; +5 → 6.7; level → 8.7; −5 → 10.0; −10 → 11.0. Raising a platform "for looks" is the most common accidental difficulty spike `[lihfolk]`.

```lua
--!strict
-- Unexecuted sketch. Put in the shared LevelMetrics module; designers and generators call the same function.
local StarterPlayer = game:GetService("StarterPlayer")
local EXTRA_REACH = 1.5 -- studs gained from character width; measure on your own gap ladder

local function maxGap(heightDelta: number, runSpeed: number): number? -- nil = cannot be reached at all
	local g = workspace.Gravity
	local v = if StarterPlayer.CharacterUseJumpPower then StarterPlayer.CharacterJumpPower
		else math.sqrt(2 * g * StarterPlayer.CharacterJumpHeight)
	local disc = v * v - 2 * g * heightDelta
	if disc < 0 then return nil end
	return runSpeed * (v + math.sqrt(disc)) / g + EXTRA_REACH
end
return maxGap
```

Screen maths (default `FieldOfView` 70° vertical `[official]`): horizontal view is about 86° on a 4:3 tablet, 102° at 16:9 and 113° on a 19.5:9 phone, so phones see wider (a secret "just off screen" on PC is visible) but everything is physically smaller. On-screen height in pixels = `size × screenHeight / (1.40 × distance)`: a 5-stud avatar at 40 studs is about 64 px on a 720-px-tall phone render; the smallest feature that survives is about `distance / 260` studs, so a 0.1-stud window bar is gone at 40 studs `[lihfolk, computed]`. Angular size = `2·atan(H / 2D)`: 50 studs tall at 500 studs is 5.7°.

- Conflict: door width. LihFolk measured 3.6–4 × 7.5–8 on a house kit `[lihfolk]`; the knowledge base said at least 7 tall and 4–5 wide; the official sample uses 10 `[official]`. Trust: 4 studs is exactly the R15 pathfinding diameter, so use ≥ 5 for any door gameplay passes through and keep 3.6–4 for decorative or single-occupant doors.
- Conflict: the greybox tutorial says walls of 10 stop "Roblox's default jump height of 5 studs"; the StarterPlayer reference says 7.2 (or about 6.4 with JumpPower 50). Trust the reference and your own place: a 6-stud wall is not jump-proof, a 10-stud wall is.
- `CameraMaxZoomDistance` `[VS]`: the docs page states no default; the engine API dump gives a class default of 400 studs (version 0.747, read 2026-11-11), and a place template can carry its own value (128 is often quoted for new places; not verified). Read it in StarterPlayer, set it deliberately (a lower cap also stops players zooming over walls), and test sightlines from the maximum.

## 3. Layout archetypes

| Archetype | Shape | Use for | Strength | Typical failure | Streaming note |
|---|---|---|---|---|---|
| Hub-and-spoke | Compact hub with a station ring; gates or portals to zones | Simulators, pets, RPGs, round games | Every activity near; social centre | Hub too wide or dead; exit hidden behind the centrepiece | Spokes can be far apart: request streaming before each teleport |
| Linear chain | Zones in a row, a gate between each | Progression simulators, obbies, story horror | Pacing and reveals are controlled | Long empty walks, forced backtracking | Only neighbours load; gates hide stream-in |
| Open world | Districts around one global landmark | Roleplay, survival, driving | Freedom, emergent play | Lost or bored players; empty middle | Needs far landmarks (§12) and an encounter every 150–300 studs |
| Arena | Symmetric bowl or three lanes | PvP, rounds | Fairness, fast fights | One dominant perch; spawn camping | Small; occlusion culling helps little in open arenas `[official]` |
| Generated room chain | Socketed rooms assembled per run | Horror, dungeons, towers | Replay value from few assets | Rooms without a valid route or hide spot | Build off-world, parent once (§14) |

- Hub shapes `[lihfolk]`: radial plaza (centrepiece, stations on a ring, exits on the rim), street (one spine, shops either side), courtyard with a wall of gates, vertical tiers for prestige. Store a radial hub as polar coordinates (angle, radius) so the whole thing rescales without re-placing.
- When not to build a hub `[lihfolk]`: single-loop games (spawn straight into play, shop in the UI), servers with very few players, or when a separate hub place would cost a teleport each way.
- Add loops to any tree-shaped layout: put a reward at the end of a dead end and it feels good; leave it empty and players read a designer mistake `[lihfolk]`.

## 4. Spawn and lobby: the first five seconds

The first frame must contain: the first objective or its entrance, one global landmark, and something moving (other players, a pickup, an NPC). Never a wall, never an offer (house rule: no purchase prompts on load).

- Spawn = an invisible `SpawnLocation` inside a Blender pad (see `game-craft.md` §2), rotated to face the objective, on open ground, out of traffic lanes, combat boxes and PvP sightlines, never on a moving piece.
- The centrepiece hides whatever sits directly behind it. If the exit is behind the monument, move the spawn off-axis or raise the gate arch above the monument's silhouette `[lihfolk worked example]`.
- Draw three flows before placing stations `[lihfolk]`: first-time (spawn → first action → exit), return (spawn → exit, passing the core spend station within prompt range, never through a prompt) and loiter (leaderboards, benches, the centrepiece). Loiter nodes sit beside the spawn line, not on it, or new players spawn into a crowd.
- Stations: the prompt sits on the object at chest height (a `Prompt_Att` from Blender), not on a floor disc. `RequiresLineOfSight` hides a prompt when anything but its own parent sits between camera and prompt, and is on by default `[official]`, so a sign, rail or festive arch between camera and prompt makes "the shop not work sometimes": keep an approach cone of about ±30° out to 30 studs clear, or turn line of sight off for that prompt `[lihfolk]`.
- Queue pads: visible from spawn, labelled with what they start and a countdown, a clear walk-off edge, never on the return flow. Detect occupants by polling `GetPartBoundsInBox` above the pad, not with `Touched` (standing characters do not fire it reliably) `[lihfolk]`.
- Returning players: a "continue" portal a few studs from spawn, framed so live content is visible behind it `[lihfolk]`.
- The hub gets the tightest budget in the game: it is the first load on the weakest devices. Profile it with ten players present.
- Event dressing is its own folder with a removal date; it may not move spawns, prompts or bounds. Re-check prompt line of sight and the first frame after adding it `[lihfolk]`.

Respawn is a pipeline, not an instant `[lihfolk]`: death presentation (1–3 s) overlaps `Player:RequestStreamAroundAsync(spot)`; then choose the spot (no other player within about 24 studs, no enemy in aggro range, floor confirmed by a downward raycast, facing a landmark), place, protect, reveal. Engine defaults `[official]`: `Players.RespawnTime` 5 s, `SpawnLocation.Duration` 10 s of ForceField. Choose per genre: obby under 1 s, arena 2–5 s, PvE 3–6 s behind a presentation. Protection ends when the protected player attacks. `Workspace.PredictiveStreamingMode = Enabled` (opt-in; `Default` currently behaves as `Disabled`) pre-fetches possible spawn locations on death `[official, VS]` but cannot know script-chosen spots.

## 5. Landmarks, sightlines and wayfinding

Players read a space in a fixed order `[lihfolk; consistent with level-design practice]`: light and contrast, then motion, then silhouettes against the sky, then openings, then text. Audit every space: what is brightest, what moves, what breaks the skyline, where are the openings? All four must point the same way. A bright decorative lamp in a dead end sends players into the dead end.

| Landmark type | Job | Visible from | Rule |
|---|---|---|---|
| Global | Orient anywhere, including the first frame after respawn | Whole district | One per district, never two; unique silhouette when blacked out |
| Destination | Pull toward the next goal | The previous node or gate | Brightest or most saturated thing in that view |
| Local | Make an area nameable ("the mushroom place") | Inside the area | Listen for player-invented names in playtests |
| Waymarker | Confirm the route at a fork | The junction | A lit lantern on the correct branch |

- Lynch's five elements (paths, edges, districts, nodes, landmarks; `knowledge-base.md` 1.9.3) give the test: after five minutes of play, ask a tester to sketch the map. What they draw works; what they forget did not register `[lihfolk]`.
- Critical path target: about 80% of first-time players find it without UI. If fewer do, fix the space (light, openings, path value), not the HUD `[lihfolk]`. A HUD arrow is the fallback, shown only after a player has been stationary or off-route for a while, never from minute one.
- Thresholds between districts change at least two cues at once (floor and light, or skyline and colour) and are overhead: an arch reads from 50 studs back, a floor change under the avatar is invisible `[lihfolk]`.
- Compression then release: a short canyon or tunnel before a reveal. Keep it under about 5 s of walking with a ceiling of three avatar heights or more; it also hides stream-in of the next area `[lihfolk]`.
- Leading lines (path edges, fences, lamp rows, roof lines) converge on the goal. Breadcrumbs that stop are the strongest "wrong way" signal available.
- One visual language, never broken `[lihfolk]`: one cue per meaning for hazard, interactable, climbable, breakable, locked, collectible and objective. A decorative strip in the hazard colour on a safe walkway costs the whole language. Tag gameplay objects (`Hazard`, `Interactable`) and audit by tag after every art pass.
- Unwanted sightlines: locked zones, unfinished backs, the map edge. Cast rays from a grid of eye points toward a target in the locked zone; any unblocked ray is a leak. Check again from 30–50 studs above the floor (jump pads, knockback) and from maximum zoom `[lihfolk]`. For a progression chain, hide the next zone's floor and enemies but let its landmark show over the wall: that is the pull forward.
- Phones and fog: test every key sightline at the lowest graphics level, at the night preset and at 19.5:9. A landmark that is fine at noon can vanish in a storm preset.

## 6. Composition and density

Order beats detail: layout and primary forms decide whether a map reads; props only finish it `[lihfolk]`.

- Focal hierarchy per view: one hero (tallest, brightest or most saturated), 2–4 primary forms that frame it and never out-shine it, secondary story groups at path edges and nodes, tertiary ground cover with low contrast and no lights.
- Height in steps (low walls, houses, one tower). A skyline of equal heights reads flat; community builders list flat ground and uniform heights among the first tells of an amateur map `[community]`.
- Negative space is a feature: paths, plazas, door fronts, prompt approaches and spawn areas stay clear. Clear ground is what makes dressed edges read.
- Density gradient: dense at edges, walls and corners; sparse in play space; nothing on the path. Clumps with gaps, never an even sprinkle.
- Groups in odd numbers with a hierarchy (one large, two medium, a few small), 5–15% size variation, some asymmetry.
- Made things align (90° steps plus a few degrees, facing their use: chairs to tables, stalls to the path, signs to the approach); grown things vary (random yaw, slight tilt, sunk 0.1–0.3 studs).
- Everything is grounded: nothing hovers, nothing is half inside a wall unless that is the story.
- Saturation is a budget spent on the hero, interactables and rewards, never the ground. One accent hue per zone; pickups use one game-wide colour that no zone uses as decoration.
- Reuse beats variety `[lihfolk]`: 3–5 base meshes per prop type varied by transform; a kit of 50–90 models covered a whole realm in its reference project (617 placements from 87 models, measured); a dressed zone stays around 3k–10k instances.

Tests, in order: (1) player camera at about 10, 50 and spawn distance, in 16:9 and phone aspect; (2) blur the screenshot: hero and path are still the clearest shapes; (3) greyscale (`ColorCorrectionEffect.Saturation = -1`): path and interactables still separate from the ground; (4) hide the detail folder: if the view barely changes, the detail carries nothing, and if it collapses, the primary forms are weak; (5) walk spawn to goal with a stopwatch.

## 7. Layout by genre

Genre design is in `references/genres/<genre>.md` and `genre-playbooks.md`; this is the map side only.

| Genre | Layout | Numbers and rules | Typical failure |
|---|---|---|---|
| Tycoon plots | Plots in a ring or two facing rows around a shared plaza; every plot identical relative to its entrance | Plot count = max players. One forum answer: 6–8 when every plot's NPCs are simulated for everyone, 12–14 when a plot's NPCs render only for players inside it `[community: one thread]`. Space plots for the fully upgraded footprint plus a margin `[community]`. Claim pad visible from spawn, under 15 s away. Decide the final footprint first and reveal Blender kit pieces into it; the owner's plot is `PersistentPerPlayer` (`performance.md`) | Plots that collide when maxed; neighbours hidden so nobody sees progress; each plot a walled flat slab that just ends (`visual-library/environments-and-maps.md` row 63): give it a plinth, a diegetic edge and a backdrop, and let the empty plot show what it becomes (row 66) |
| Simulator zones | Hub ring plus a linear zone chain | One dominant floor colour, one landmark and a themed gate per zone; next zone's landmark visible, its floor hidden; spend stations on the return flow; walk times against §1 budgets | Recolour-only zones; shop off the return path |
| Obby stages | Stage modules snapped `Exit` to `Entry`, each starting and ending on a safe landing ≥ 8×8 | One difficulty dial per new stage (gap margin, landing size, height change, timing window, run-up, camera direction, chain length, penalty, visual noise). At most 5–6 jumps between safe spots: six jumps at 90% each clear 53% of the time. Required timing windows ≥ 0.4 s, first exposure ≥ 1 s. Sideways jumps before depth jumps. Checkpoint before any failure would replay more than about a minute (`genres/obby-tower.md`); blogs quote every 30–90 s or every 3–5 obstacles for easy courses `[community: search summary]`. Breathers are places with a view back, a checkpoint and any shop `[lihfolk]` | Raised platform makes a jump impossible; long chains; server-moved hazards that kill players who dodged on their own screen |
| Horror | Linear or generated room chain; compression, short sightlines | Quiet rooms first, then a long warning, then the threat; one tell and one counter per threat; darkness hides the threat, never the answer; every room validated for a reachable hide spot and a creature route `[lihfolk teardowns]`; safe rooms are the rest beats | Dark for its own sake; a room with no counter in reach |
| PvP arena | Rotational symmetry for free-for-all, mirror for two teams; three primary lanes with cross lanes and combat pockets `[official]` | No position strictly better than its mirror. Elevation "peaks and valleys" control sightlines `[official]`. Spawn alcoves out of every sightline with two exits. Arena radius ≥ largest telegraph radius + boss or objective half-width + 2 × dash; clear height ≥ 30. Plan one meaningful encounter per player every 10–20 s: fewer players means a smaller map `[lihfolk]` | One perch sees everything; spawn sightlines; empty middle becomes a sniper lane `[community]` |
| Objective modes | Three lanes per objective | Each team's fastest route to a neutral objective within about 1 s of the other's (measure it). CTF: two base exits, uncontested return under 45–60 s. King of the hill: zone slightly lower than its approaches. Control points: three, 10–20 s apart. Zone radius 8–12 for small teams, 14–20 for 4v4–8v8 `[lihfolk]` | Hill on high ground; unequal routes |
| Roleplay town | Street or courtyard with a real centre; districts; instanced interiors | Circulation over critical path: nodes (benches, stages, plazas) where people can be seen. Interiors 2–3 avatar heights. Road and pavement widths have no agreed number: test with the game's vehicles `[community]`. Soft boundaries and recovery, not kill planes | No centre; copy-pasted filler buildings `[community]` |

- Dodge test for any telegraphed area attack `[lihfolk, computed]`: escapable radius ≤ speed × (warning − 0.25 s). At 16 studs/s a 1.0 s warning allows 12 studs, 1.5 s allows 20; a dash adds its length. Anything larger is a damage check, deliberate or not.
- Obby hazards: animate from a shared clock (`workspace:GetServerTimeNow()`) on each client so everyone sees the same position without replication, detect the hit on the owning client and sanity-check on the server `[lihfolk]`. Add a blob shadow under the character (a small Blender disc, non-colliding, placed by a downward raycast) wherever landings are small: sun shadows fall at an angle and vanish below graphics level 4.
- Instanced interiors `[lihfolk]`: pooled empty shells in slots above the map, spaced by more than `StreamingTargetRadius` plus the interior size, within a few thousand studs of the origin; server-side `PivotTo` after `RequestStreamAroundAsync`; per-owner furniture loaded on open and cleared on close; close 30–60 s after the last occupant leaves.

## 8. Blockout to final with a Blender kit

| Pass (own folder) | Contents | Gate before the next pass |
|---|---|---|
| `01_Layout` | Blockout: ground, paths, gameplay spaces, spawn, hero stand-in, district masses | Critical path walkable and obvious from spawn with no UI; walk times inside the brief; tested on a phone |
| `02_Primary` | Final kit buildings, cliffs, big trees, the real hero landmark | Silhouette, colour and light reads each identify the zone with small props hidden |
| `03_Composition` | No new assets: move masses from fixed review cameras | One focal point per view; leading lines point at it |
| `04_Medium` | Story groups, stalls, fences, lamps | Each group answers "what happened here?"; paths and prompts still clear |
| `05_Detail` | Seeded scatter, ground cover, seam cover | Hiding the folder changes little; budgets still met |

- Under the house rules the blockout is either a Blender blockout kit (8–12 boxy GLB modules on the kit grid: floor tile, wall, door wall, ramp, stair, pillar, platform, flat function colours from the palette) or primitives in an unpublished place or a `_Blockout` folder that a publish check refuses. No greybox ships.
- Colour blockout by function, not by art: floor, wall, hazard, interactable, enemy area `[lihfolk]`.
- Name blockout pieces `Blockout_<KitPiece>` with the same pivot as the final piece, so one script swaps each for its package by name. Mark where art should go with invisible marker parts carrying attributes (`Replaces`, `IntendedCount`); the art pass consumes markers and a check lists any left `[lihfolk]`.
- Separate layout from visuals: approve a flat sketch, then a minimal 3D structure, before any art, so the two jobs can be done by different people `[community: Mad Studio guidebook]`.
- Every pass is reversible: store old pivots and colours as attributes before a bulk change, and the old hub stays until play-testing approves its replacement (an older place version can supply a copy if needed) `[lihfolk]`.
- Save three review cameras per zone (gate view, landmark view, worst view) in a `_Dev` folder and judge every pass from the same three `[lihfolk]`.
- Order of work after layout: primary forms, composition, medium props, detail, lighting preset, collision and bounds sweep (§13), performance capture on the low-end phone (`performance.md`).

## 9. Modular kit design and trim

Extends "Modular kits, instancing and when to merge" in `art-pipeline-blender.md`.

- Minimum architecture kit: wall (solid, door, window), inner and outer corner, floor, ceiling or roof, stair or ramp, pillar, railing, and trims (plinth, cornice, corner post) that hide seams. A few versatile pieces beat many one-offs `[official: Beyond the Dark]`.
- One grid per project. Seen in the wild: 16 studs for large sci-fi architecture and 5 studs for the shooter greybox `[official]`, 2 studs for houses `[lihfolk]`. Trims and props use a sub-grid of it.
- Walls are at least 1 stud thick (light leaks, see `lighting-and-atmosphere.md`) and the wall shell is a simple, contiguous low-poly piece with the high-poly detail split into separate trim meshes: highly detailed meshes and parts that are small on screen are not used as occluders `[official]`, and staff advise separating interiors from exteriors `[community: staff replies, search summary]`.
- Keep each placed model under about 64 studs across so it streams and LODs as a unit `[official]`.
- Roofs carry houses: at thumbnail size the roof is 40–50% of the side view; overhang eaves 1.4–1.9 studs `[lihfolk, measured]`.
- Reuse matrix across zones `[lihfolk]`: rock and cliff geometry shared with the colour changed per zone (palette swap); one trunk kit with 2–4 canopies per zone; half the props from a shared kit; 6–12 unique props and exactly one hero landmark per zone. Identity comes from the landmark, light and colour, not from unique triangles.
- The same module gives new silhouettes when scaled non-uniformly and tilted: squashed and rounded for safe zones, stretched and tilted 20° for dangerous ones `[lihfolk]`. Instancing depends on MeshId and appearance, so measure draw calls after a pass like this.

## 10. Set dressing and environmental storytelling

- Ask of every area: what happened here, who lives here, where is this (`knowledge-base.md` 1.9.2). Place 2–3 answers per zone on the path or at nodes: ashes gone cold, a single bedroll and a half-written note tell "someone camped here" better than a signpost does `[lihfolk]`.
- Three reader layers `[lihfolk]`: everyone gets mood, names, landmarks and enemy design (zero to one sentence per zone); the curious get one-line item descriptions and a few notes; the obsessed get collectible sets and deliberate gaps. Spend effort in that order.
- Channels before text: zone names, silhouettes, ruins, music, light and colour. Signs are 3–8 words on a SurfaceGui (localisable, never baked into a texture) and name the action, not the key.
- The world reacts: after a big event, change banners, damage and NPC chatter. Secrets stay on the server until earned; never ship a hidden room's contents to every client.
- Scatter `[lihfolk]`: Poisson-disc placement from a seed, never uniform random; keep-outs from a `NoScatter` tag on paths, plazas, door fronts and prompt approaches; clumps at edges and seams; long-tail scale so a few pieces are giants; ground-only raycasts so props do not stack on props; grass and flowers as merged patches authored in Blender, not thousands of single meshes; sway on the client only.
- Foliage canopies and cables may be non-solid (the `NonSolid` exception in `performance.md`); trunks, rocks and every prop a player can bump stay solid.

## 11. Naming and folder structure in Workspace

```
Workspace
  Map/
    Hub/                      one Folder per district or zone; attributes ZoneId, MapVersion
    Zone_01_Meadow/
      01_Layout … 05_Detail/  pass folders (§8); kit pieces are package copies, never fresh imports
      Landmarks/              hero models (SLIM or far stand-in, §12)
      Interactive/            doors, shops, vehicles: one Model each, ModelStreamingMode = Atomic
      Gameplay/               invisible helpers only: Spawns, Checkpoints, Triggers, Bounds, AIFloors
  Runtime/                    everything the server spawns: NPCs, drops, generated rooms, instanced interiors
  _Blockout/  _Dev/           never published: greybox, review cameras, look-dev room, heatmap overlay
```

- Asset names follow `art-pipeline-blender.md` (`KIT_`, `SM_`, `_COL`, `_Att`). Zones are `Zone_<NN>_<Name>`; gameplay helpers are `<Kind>_<Name>` (`Spawn_Hub_A`, `Bounds_North`).
- Code finds things by CollectionService tag and attribute, never by path: `Hazard`, `Interactable`, `Checkpoint` (attribute `Order`), `NoScatter`, `SafeFloor`, `NonSolid`, `LightingZone`. Tags survive re-streaming and re-parenting.
- Flatten containers: a single huge Model of many props defeats streaming and model LOD; decompose it into small models of nearby, related parts `[official]`.
- No scripts inside map models. Maps live in Workspace (only Workspace streams) or ServerStorage, never ReplicatedStorage (`performance.md`).
- Every invisible helper has `CastShadow = false`; every bulk edit records its "before" in attributes.

## 12. Streaming-aware layout

Settings and code rules are in `performance.md` ("Streaming"). Layout consequences:

- The world beyond `StreamingTargetRadius` (default 1024, lower on a memory budget) does not exist on the client. Plan district sizes so the landmarks players steer by are inside it from where they are needed.
- Draw distance is a second, separate limit set by each device's quality level: since 2026-11-05 it is at least 500 studs at the lowest level (it was 200) and rises quickly above that; Roblox says not to design around exact numbers `[official, VS]`. A landmark players must steer by from further than about 500 studs can still be missing on the weakest phones even when it is streamed in: keep steering distances under that, or make the route readable without it. At low quality the engine also skips objects that cover very few pixels `[community: staff reply, 2026-11-10]`, so a small waymarker is not a far landmark.
- Far landmarks, cheapest first: keep them inside the radius; set `Model.LevelOfDetail = SLIM` on a static landmark model so a composite mesh stands in when it is streamed out `[official, VS]`; a separate low-poly stand-in mesh marked `Persistent` (rarely: persistent models never leave memory `[official]`); or paint the shape into the skybox for places players never reach. Legacy `StreamingMesh` imposters are reported to vanish or misplace in several 2025–2026 threads `[community]`: prefer SLIM and test on a published build.
- SLIM works on static models, best under about 64 studs across. A very large map section inside one SLIM model shows offset geometry, because the client falls back to the stand-in whenever the whole model is not loaded; a model nested in a SLIM model does the same when it is removed `[community: staff reply, 2026-09]`. Split big sets into modular models.
- Gates, tunnels and canyon bends are where the next area streams in unseen; `Atmosphere.Density` sets the "edge of interest" inside the radius.
- Teleports, portals, respawn spots and interior doors call `Player:RequestStreamAroundAsync` first and keep the transition effect up while it runs (request at the moment of death, not at respawn) `[lihfolk]`.
- Two places players shuttle between (home base and trading hub): an extra replication focus (`Player:AddReplicationFocus`) keeps both loaded, at about the server cost of one more player per focus `[official]`. Scopes, fast vehicles and free cameras that look past the radius can use `Player.FrustumStreaming` (server-set, opt-in) instead of a larger radius `[official, VS]`.
- Interactive models are Atomic so a door never arrives without its frame; atomicity covers the first arrival only, so handle children added later `[official]`.
- Occlusion culling is on by default on every platform and rewards walls made of large, simple pieces; interiors and city streets gain most, open arenas little. Lights, effects, shadows and avatars are not culled by it `[official]`.
- Coordinates: keep anything players stand on within a few thousand studs of the origin (float jitter beyond) and above `FallenPartsDestroyHeight` `[lihfolk, VS]`.
- Test the whole map at `StreamingTargetRadius = 64` once: every assumption that the world is loaded breaks visibly.

## 13. Collision, walkability and bounds

- Walk test, per asset type and per zone: collision visualisation on; walk and jump on everything; strafe along every wall and trim for snags; stand behind every tall prop and watch the camera; no step over 1 stud and no invisible blocker on the main path. Repeat on a thumbstick.
- Automated checks to run after each pass: jump validation of ordered `Platform` parts against `maxGap` (flag gaps above 90% of reach, and impossible ones) `[lihfolk]`; the soft-lock reachability check in `game-craft.md` §2; sight-line leak rays (§5); a float-and-bury audit that raycasts down from each prop's bounding box and reports gaps or deep overlaps `[lihfolk idea]`; the house-rule scan in `checklists.md`.
- AI floors: detailed visual ground confuses NPC grounding. Put an invisible tagged slab (`SafeFloor`) just under it for NPC ground checks, and keep enemy walk boxes clear of props `[lihfolk]`. Conflict: LihFolk makes decoration inside combat boxes non-colliding; house rule 2 forbids walk-through props, so clear the box instead and dress its rim.
- Pathfinding gaps are clearly passable (comfortably above the agent's 4-stud width) or clearly blocked; a gap barely wider than the agent is the classic stuck point. Large enemies get their own agent parameters.

| Boundary | Use for | Rule |
|---|---|---|
| Diegetic edge (Blender cliff, wall, water, fence) | Everywhere, first choice | Players climb anything with a ledge: test by jumping |
| Invisible wall | Above diegetic edges only | Tall (above jump plus any launcher), a few studs thick, well outside the visual edge; own collision group, excluded from combat raycasts |
| Soft boundary | Open worlds, vehicles | Server-owned 5–10 s countdown, then recovery, not death |
| Recovery plane | Exploration, roleplay, young audiences | Return to the last grounded spot sampled by the server (never client-reported), skipping moving platforms and hazard floors |
| Kill volume | Obbies, sky maps | A short fall below the course; backed by a server height sweep because `Touched` misses fast fallers |

- Fall thresholds are level parameters: store a `MaxDrop` per zone, larger than its biggest legitimate drop. One global 55-stud rule caused false rescues in zones with long drops `[lihfolk, measured]`.
- Wall only the outer outline of a floating hub: an automatic pass that walled every edge (761 walls) stopped players jumping between the hub's own terraces and was rebuilt as 248 outline walls `[lihfolk, measured]`.
- Recover vehicles as whole assemblies; set `FallenPartsDestroyHeight` below the lowest geometry; treat repeated far-out-of-bounds positions as an exploit signal, not an instant ban.
- Combat containment: leash enemies to their walk box; arena seals are visible, raised only when every participant is inside, and lowered on every exit path including errors; edge lips plus a catch volume under arenas `[lihfolk]`.

## 14. Procedural generation with Blender-authored pieces

Rules of seeded, validated, data-first generation are in `game-craft.md` §6. What generators may place: Blender kit rooms, tiles and props. They never create primitive Parts or runtime meshes (an `EditableMesh` ground is a generated mesh and breaks house rule 1), and noise-driven Terrain needs the owner's approval. Without Terrain, noise chooses among pre-authored ground tiles and drives scatter density.

| Method | How | Good for | Weak at |
|---|---|---|---|
| Socket growth | Attach room prefabs at open door sockets until a target count | Hand-made room kits, horror chains, stations | Loops (it grows trees) |
| Grid rooms + graph | Rectangles on a tile grid, minimum spanning tree, then add back 10–20% of the other edges as loops | Roguelike floors | Organic shapes |
| Mission graph first | Generate start, key, lock, boss as a graph, then embed in space | Lock-and-key progression that is correct by construction | More code |
| Wave function collapse | Tiles whose edge sockets must match | Towns, roads, coastlines, dressing | Global structure: fix paths, borders and landmarks as pre-set cells first |
| Poisson scatter + noise mask | Even-but-random points, density from low-frequency noise | Props, foliage, encounters | Anything that must connect |

- Authoring `[lihfolk]`: sockets are `_Att` empties exported from Blender (`Socket_Door_N_Att`) with attributes `Kind` and `Width`; only matching sockets join. Rooms and tiles sit on the kit grid with one pivot convention; rotate in 90° steps only and snap to the grid so float drift cannot open seams. Every obby or tower stage starts and ends on a safe landing, so any stage can follow any other. Test the rotation sign once with an asymmetric tile.
- Overlap tests use a coarse occupancy grid (8- or 16-stud cells), not physics queries on freshly moved geometry. Place required rooms (boss, key, shop) first at a target depth, then fill around them.
- Pacing from graph depth `[lihfolk]`: breadth-first depth from the start room drives difficulty, puts the exit in the deepest room, treasure in dead ends and a rest room near the middle. Track total rooms and critical-path length per floor.
- Validate, then build: reject on too few rooms, any unreachable room, critical path outside its range, a key behind its own lock, a combat room under the arena minimum, or (horror) a room without a reachable hide spot and creature route. Retry with a seed derived from (base seed, attempt) so the accepted result is still reproducible; if average attempts pass 2–3, the parameters are fighting each other.
- Determinism `[lihfolk]`: one `Random` per bounded job, created from a hash and never shared; fork child seeds up front in a fixed order; for anything reachable in any order (chunks) use a stateless integer hash of (seed, x, z, purpose) rather than `seed + x·prime`; never iterate dictionaries or `GetChildren()` when drawing random numbers (sort names first); quantise noise before thresholding. Save `{seed, generatorVersion}`, and for player-owned worlds save the generated result. Loot and reward rolls never derive from a seed the client knows.
- Tests: golden hashes of the description for fixed seeds; generate chunks in two orders and compare; regenerate one after 500 others.
- Build `[lihfolk]`: assemble the whole floor under an unparented Model, then parent once; compute NPC paths after parenting; keep corridors comfortably wider than the agent; parent spawned things under the floor so one `Destroy()` cleans up. Generate at edit time whenever the result does not need to vary per run.

```lua
--!strict
-- Unexecuted sketch. Snap a cloned room so its entry socket meets the previous room's exit socket.
local function attach(room: Model, entry: Attachment, previousExit: Attachment)
	local pivotToEntry = room:GetPivot():ToObjectSpace(entry.WorldCFrame)
	-- sockets face out of their rooms, so turn the entry 180 degrees to face the exit it joins
	room:PivotTo(previousExit.WorldCFrame * CFrame.Angles(0, math.pi, 0) * pivotToEntry:Inverse())
end
return attach
```

## 15. Playtest heatmaps and death maps

`design-foundations.md` says to log every death with its position; this is how. Record on the server, quantise at once, and tag everything with the map version.

| Record | Fields | Answers |
|---|---|---|
| Position sample (every 2 s) | cell, map version, new or veteran | Flow, dead zones, chokepoints |
| Death | victim cell, cause (fall, hazard id, enemy, player), attacker cell | Unfair jumps, unintended perches, spawn camping |
| Quit | cell, session minute | Where frustration ends sessions |
| Checkpoint or objective reached | id, seconds since spawn | Pace and stuck points |

- Cells of 4–16 studs (smaller for obbies). Store counts per cell, never user ids per position. Split first-session players from veterans: they reveal different problems `[lihfolk]`.
- The damage code stamps cause and attacker position when it applies damage; inferring cause after death gives a map of "unknown" `[lihfolk]`.
- Small playtest: print the table at the end. Live game: each server flushes merged counters every 5–10 minutes and in `BindToClose` with `UpdateAsync` (never `SetAsync`, which drops other servers' counts), or sends aggregated cells as custom analytics events (`analytics-and-discovery.md`); sample 10–20% of servers on a popular game `[lihfolk]`. Community heatmap modules and Studio plugins exist `[community]`; treat them as untrusted code and prefer your own 40 lines.
- Draw it back in a test copy only: one flat non-colliding marker per cell in `_Dev`, colour normalised by the 95th percentile, one layer per death cause. Never ship the overlay.
- Change one thing per map version, bump the version, compare.

| Pattern | Likely cause | Fix |
|---|---|---|
| Death cluster at one jump | Gap near the reach limit, unreadable landing, raised platform | Shorten, widen the landing, add a blob shadow, checkpoint before it |
| Deaths just outside spawn with a kill-from cell overlooking it | Spawn sightline | Block the line, add a second exit, move the alcove |
| A kill-from cell runs hot where no player belongs | A perch nobody intended | Remove its cover or block access |
| Cold zone | Players do not know it exists or it pays nothing | Landmark it, reward it or cut it |
| Hot spot that is not an objective | Snag, or a bright decoration pulling players | Fix collision; dim the decoration |
| Hot cells along an edge | The edge looks walkable or promising | Make the boundary diegetic and obvious |
| Quit cluster | Frustration point | Read deaths and timings for the same cells |

```lua
--!strict
-- Unexecuted sketch. Server Script. Counts only; flush or print elsewhere.
local Players = game:GetService("Players")
local CELL, MAP_VERSION = 8, "hub_v3"
local counts: { [string]: number } = {}

local function bump(kind: string, position: Vector3)
	local key = `{MAP_VERSION}/{kind}/{position.X // CELL},{position.Z // CELL}`
	counts[key] = (counts[key] or 0) + 1
end

Players.PlayerAdded:Connect(function(player: Player)
	player.CharacterAdded:Connect(function(character: Model)
		local humanoid = character:WaitForChild("Humanoid") :: Humanoid
		humanoid.Died:Once(function()
			local cause = character:GetAttribute("LastDamageCause") :: string? -- stamped by the damage code
			bump("death_" .. (cause or "unknown"), character:GetPivot().Position)
		end)
	end)
end)

task.spawn(function()
	while true do
		task.wait(2)
		for _, player in Players:GetPlayers() do
			local character = player.Character
			if character then bump("pos", character:GetPivot().Position) end
		end
	end
end)
```

## 16. Diagnosis: the map feels empty, cluttered or confusing

| Feels | What is actually wrong | Check | Fix |
|---|---|---|---|
| Empty | No focal point and flat heights, not too few props | Blur test shows no dominant shape; skyline is level | Add or raise one hero, step the heights, frame it from spawn |
| Empty | Space sized for max players, walks with nothing in view | Walk times over budget; cold cells | Shrink the core, add an encounter or story group every 150–300 studs, or cut the area |
| Empty | Even sprinkle of filler | Props equally spaced, same scale | Delete half, regroup into odd-numbered story groups at edges and nodes |
| Empty | Default lighting, no value structure | Greyscale test is one grey | Pick a preset; darken ground, lift interactables (`lighting-and-atmosphere.md`) |
| Cluttered | Props on paths, door fronts and prompt approaches | Players snag; prompts flicker | Enforce `NoScatter` keep-outs; restore negative space |
| Cluttered | Everything competes: many saturated or glowing things | More than one brightest object per view | Saturation and light only on hero, interactables, rewards |
| Cluttered | Mixed styles and texel densities | Assets from several sources | Re-skin to the palette or trim library (`art-pipeline-blender.md`) |
| Cluttered | Chest-high props in combat space | Camera jumps, blocked aim | Low or full cover only; clear walk boxes |
| Confusing | Spawn faces a wall or the exit hides behind the centrepiece | First-frame screenshot | Rotate or move the spawn; raise the gate |
| Confusing | Brightest thing is decoration | Hot cell at a lamp or sign | Dim it; light the objective |
| Confusing | No or competing global landmarks; all zones look alike | Testers' sketch maps disagree | One global landmark per district; one hue and landmark per zone |
| Confusing | Text-only guidance | "Where do I go?" asked under a sign | Light, motion, an opening, a path; arrow only as fallback |
| Confusing | Landmark streamed out or lost in fog on phones | Missing at distance on a real device | SLIM or stand-in; retune `Atmosphere.Density` |

## 17. Level-up: symptoms in a live game → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| New players leave in the first minute without acting | First action too far or not in the first frame | Spawn facing; first station under 15 s; move the first fight closer |
| Veterans skip the shop | Core spend is off the return flow | Put it on the way out, within prompt range |
| "The shop does not work sometimes" | Decoration blocks prompt line of sight; two prompts in range | Clear the approach cone; space prompt points; one prompt per key |
| Players fall into the void after portals or respawn | Destination not streamed | `RequestStreamAroundAsync` at the start of the transition; Atomic interactives |
| Half-built buildings pop in | Nonatomic interactive models; giant container models | Atomic where scripts need the whole model; decompose containers |
| Obby stage with a quit spike | Chain too long, near-limit upward jump, depth jump too early | Mid-stage checkpoint; run the jump validator; reorder dials |
| "I dodged it and died" | Server-moved hazards with server-side kills | Client clock animation, owner-side hit, server sanity check |
| Spawn camping | Spawns in sightlines; no occupancy check | Alcoves, two exits, pick an unoccupied spot at respawn |
| Enemies stuck on scenery | Props in walk boxes; visual ground as AI floor; tight gaps | Clear boxes, tagged AI floor, gaps clearly passable or blocked |
| Hub stutters on phones at join | Hub heavier than any zone | Hub gets the tightest budget; defer distant dressing |
| Zones feel like recolours | Only hue changes | Change silhouette bias, landmark, light profile and one accent per zone |
| Stale festive props | Event dressing never removed | Folder per event with a removal date |
| Invisible walls feel cheap | Wall at the visual edge or blocking a reachable-looking place | Diegetic edge first; invisible wall well outside it |

## Map polish checklist

- [ ] First frame after spawn and after respawn shows the objective, a landmark and motion.
- [ ] Walk times meet the brief; no step over 1 stud or invisible blocker on the main path.
- [ ] One hero per zone; blur, greyscale, hide-a-pass and phone-aspect tests pass.
- [ ] Paths, door fronts, prompt approaches and spawn areas clear; props grouped, grounded and facing their use.
- [ ] Hazard, interactable and collectible cues each mean one thing everywhere (tag audit).
- [ ] No sight-line leaks into locked or unfinished areas, including from above and from maximum zoom.
- [ ] Every visible object is a Blender model with collision; blockout and dev folders removed.
- [ ] Bounds, catch volumes and per-zone drop thresholds tested by jumping, driving and flinging.
- [ ] Works at `StreamingTargetRadius = 64`; teleports request streaming first; far landmarks still visible on a phone.
- [ ] Budgets met in the worst view on the low-end phone (`performance.md`).

## Review gate

- [ ] Map brief filled in; jobs ranked; map version string exists and is bumped on layout changes.
- [ ] Metrics table written for this game's avatar and jump mode; R15 dummy present in the Blender scene and the blockout.
- [ ] Blockout passed the walk test on a phone before any dressing; passes live in numbered folders.
- [ ] Genre layout rules from §7 checked; PvP routes timed; obby stages validated.
- [ ] Workspace follows the folder and tag conventions; containers flattened; interactives Atomic.
- [ ] Generators (if any) are seeded, validated, versioned and place only Blender kit pieces.
- [ ] Position and death maps reviewed for first-session players after each layout change.
- [ ] No Terrain without the owner's written approval for this game; no primitive or marketplace geometry ships.

## Sources

Accessed 2026-11-10; platform facts re-checked on 2026-11-11 against commit 7cbffff (2026-11-10).

- https://github.com/Roblox/creator-docs (read), under `content/en-us/`: `tutorials/curriculums/environmental-art/{greybox-your-environment,construct-your-world}.md` (stair blocks), `resources/beyond-the-dark/building-architecture.md`, `workspace/streaming/{index,techniques,slim,frustum}.md`, `performance-optimization/design.md`, `workspace/camera/index.md`, `performance-optimization/improve.md`, `reference/engine/classes/{StarterPlayer,Players,Player,SpawnLocation,ProximityPrompt,Humanoid,Model,Workspace}.yaml`
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/lihfolk-worldbuilding/{SKILL.md,references/budgets.md,references/world-brief-template.md}`; `LihFolk Vault V2/06 World Building and Art/{Level Design for Roblox,World Composition and Set Dressing - Designed, Not Scattered,Zone and Biome Art Direction,House Construction Method - Modular Kit Workflow}.md` and the common-mistake tables of `{Foliage Props and Scatter,Level of Detail and Model Streaming}.md`; `33 Level Design/{Level Design Principles - Flow Sightlines and Landmarks,Lobby and Hub Design,Obby and Platforming Level Design,Spawn Points Safe Zones and Respawn Flow,Combat Arena and Encounter Layout,Objective Mode Maps - Capture the Flag, King of the Hill and Control Points,Playtest Heatmaps - Position and Death Maps,Kill Planes, Map Boundaries and Out-of-Bounds Recovery,Teaching Through Level Design,Instanced Interiors - Pooled House and Room Copies for Many Players}.md`; `34 Procedural Generation/{Dungeon and Room Generation,Seeds Determinism and Reproducible Worlds,Wave Function Collapse on Roblox,Infinite and Streamed Worlds}.md`; `36 Narrative and Worldbuilding/Lore Delivery Without Walls of Text.md`; `55 Modelling Nuance and Readability/Modelling to the Roblox Camera and Player Scale.md`; `60 High-Craft Game Teardowns/{What Craft Looks Like on Roblox - Lessons from Top Studios,Teardown - Pressure}.md` (read)
- https://devforum.roblox.com/t/mad-studio-map-layout-design-guidebook/1246963 (read: workflow cycle)
- https://devforum.roblox.com/t/ruskis-tutorial-1-how-to-design-a-map-layout/277853, https://devforum.roblox.com/t/ruski’s-tutorial-3-how-to-design-a-pvp-map/2746055, https://devforum.roblox.com/t/ruskis-tutorial-5-how-to-design-an-open-world-map/3554962 (first two read on 2026-11-11: opening posts; the third is a search summary)
- https://devforum.roblox.com/t/few-questions-from-professional-builders/2891675, https://devforum.roblox.com/t/space-seems-too-empty/1043747, https://devforum.roblox.com/t/how-can-i-make-my-map-look-less-boring-and-empty/2690121 (read: opening posts and most-liked replies); https://devforum.roblox.com/t/showcasing-my-stud-island-map-%E2%80%93-feedback-for-halloween-spooky-update/3968200 (search summary)
- https://devforum.roblox.com/t/how-many-tycoon-plots-should-i-allow/2710675, https://devforum.roblox.com/t/best-way-to-go-about-plot-sizes-without-looking-weird/241843 (read)
- https://devforum.roblox.com/t/open-or-confined-making-a-rp-town-map/306381, https://devforum.roblox.com/t/question-about-road-sizes/490325, https://devforum.roblox.com/t/how-to-build-city-maps-that-arent-repetitive/336205 (read)
- https://devforum.roblox.com/t/occlusion-culling-now-live-in-roblox-client/3300953 (read; official, 2024-12-10, updates to 2025-06-23), https://devforum.roblox.com/t/studio-beta-introducing-occlusion-culling/3250604 (opening post read; the staff replies on interiors are a search summary)
- https://devforum.roblox.com/t/increasing-the-minimum-draw-distance-to-500-studs-and-other-auto-quality-level-improvements/4977292 (read; official, 2026-11-05, staff replies to 2026-11-10)
- https://devforum.roblox.com/t/levelofdetailstreamingmesh-resp-streamingenabled-in-general-unexpected-behaviour-on-studio-and-player/4755979, https://devforum.roblox.com/t/repost-for-pm-streamingenabled-causing-parts-to-become-visually-offset-from-their-bounding-boxactual-position/4844577 (read; staff reply on SLIM in the second)
- https://devforum.roblox.com/t/player-heatmap-module/3961813, https://devforum.roblox.com/t/bulkbrains-heatmap-see-player-movement-as-3d-space/4819968 (read: opening posts)
- Engine API dump, version 0.747 (https://github.com/MaximumADHD/Roblox-Client-Tracker, read 2026-11-11): defaults for `CameraMaxZoomDistance` (400), `CharacterUseJumpPower` (true), `ProximityPrompt.RequiresLineOfSight` (true), `MaxActivationDistance` (10)
- https://www.creation.dev/blog/roblox-obby-design-guide (search summary; third-party blog, checkpoint spacing figures)
- No evidence found: Reddit threads on map design (searches returned DevForum only); an official plots-per-server or road-width figure; a public description of how Doors or Pressure generate rooms; a `CameraMaxZoomDistance` default on the docs page, or any documented step-up height for Humanoids. The jump, pixel and angular-size figures in §2 were recomputed on 2026-11-11 and hold.
