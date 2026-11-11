# Cutscenes and cinematics: short, skippable, directed moments, and trailers

What this is: how to decide whether a moment deserves a cutscene, plan it as shots, move the camera so it looks directed, stage actors, run it on the client with a guaranteed way out, and capture trailers that Roblox will accept. Open it before taking the camera away from a player for any reason, when a cutscene leaves a camera stuck or a HUD missing, or when planning a trailer. It links instead of repeating: camera maths for gameplay cameras (`game-craft.md` §3), markers, Cam-bone rigs and replication (`animation-and-rigs.md` §6, §7, §10), motion comfort and captions (`accessibility-and-player-qol.md` §5, §6), lighting hand-off and depth of field (`lighting-and-atmosphere.md` §6, §10), music priority and ducking (`audio-sfx-music.md` §6, §8), shake values (`vfx-and-juice.md` §7). Reference images, modules and videos: `visual-library/cutscenes-and-cameras.md`.

Tags: `[official]` Roblox docs (mirror commit 7cbffff, 2026-11-10) or Roblox staff posts, `[community]` DevForum practice, `[lihfolk]` LihFolk Vault V2 as quoted in sibling guides, `[VS]` version-sensitive, `[house]` house estimate: a starting number to test, not a measurement. Film and game-cinematics craft sources are named inline (Schnitzer, Hancock, Hamilton, StudioBinder) and listed in Sources. Terms: a **shot** is one continuous camera take; a **cut** is an instant change of shot; a **cue** is a timed event (sound, VFX, subtitle, state change); the **runner** is the one client module that plays a timeline and restores everything.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Ask the §1 question; most moments stay playable. 2. Copy the first-cutscene script at the start of §14: one shot through two or three marks, a fade, one sound, skip and restore built in. 3. Run every test listed under it; after each, the camera, controls and HUD must be back. 4. Change game state on the server before the cutscene starts, never at its end | The timeline runner, actors, depth of field, synced party cutscenes, trailers |
| Intermediate | Shot list before any keying (§3); shot sizes from the §4 table; the §14 timeline runner (splines travelled by distance, one speed profile per shot); local actor clones with marker cues; subtitles at child reading speed; reduced-motion variant; preload and stream the stage before the trigger | Blender Cam-bone cameras, EventSequencer, dolly zoom |
| Expert | Data-driven timelines that seek, so late and synced viewers join mid-scene; party-synced reveals with a server clock; audio as master clock for voiced scenes; Cam-bone cameras for takedowns and first-person scenes; repeatable capture paths for trailers; funnel events for every exit reason | Nothing: watch skip rate and exit reasons |

## Fast routes

| Task | Read exactly | Look at |
|---|---|---|
| First cutscene for a beginner | ROUTE1 | LOOK1 |
| Boss or reveal intro | ROUTE2 | LOOK2 |
| Fix a robotic camera | ROUTE3 | LOOK3 |
| Dialogue scene with subtitles | ROUTE4 | LOOK4 |
| Trailer capture | ROUTE5 | LOOK5 |

## Contents

1 Earn the cutscene · 2 Length budgets · 3 Storyboard to shot list · 4 Shot vocabulary for avatars · 5 Paths, easing, comfort · 6 Staging actors · 7 Client-only architecture · 8 Skip, pause, subtitles, reduced motion · 9 Dialogue presentation · 10 Lighting and post · 11 Audio · 12 Performance and streaming · 13 Authoring tools and data format · 14 First-cutscene script and timeline runner · 15 First-session intros · 16 Trailers and capture · 17 Amateur tells · 18 Critique rubric · 19 Level-up table · Review gate · Sources

## 1. When a cutscene earns its place

A cutscene is any stretch where the game, not the player, owns the camera or the controls. Default answer: do it in play. Hancock's rule still holds: if a goal can be met with gameplay instead of a cutscene, players prefer that, with two exceptions, pacing and moments where being unable to act is the drama. Schnitzer's list of legitimate purposes: mark the start or end of a level, reward, show a clue the player needs, set mood, carry the story forward.

| The moment | Use | Why |
|---|---|---|
| Player must notice one thing (door opened across the map, new zone) | 1–2 s camera glance with control returned, or a world beacon and no camera at all | Information, not drama; a glance costs 2 s, a beacon costs 0 |
| A threat arrives | Telegraph in play, then a reveal of 3–6 s that hands straight into the fight or chase | DOORS shows eyes on the walls before Seek appears, plays a short reveal, and the chase starts at once (search summary) |
| Reward, hatch, unlock, rank-up | Short reveal over live play or a 2–4 s framed shot | The reward is the point; see skip and speed in `accessibility-and-player-qol.md` §11 |
| NPC talk, shop, quest hand-in | Dialogue UI with the gameplay camera, or a bark bubble | Conversation scenes that seize the camera are the classic annoyance (Hancock) |
| Backstory, lore | Environment, item text, optional readable; never a forced scene | Info-dumps are where cutscenes fail most (Hancock) |
| Ending, chapter break, boss death | A real cutscene | Natural rest point after effort: reward plus pacing |
| Teleport or streaming pause to hide | A covering transition that does a job | Roblox's Duvall Drive demo hides room teleports behind Warmup, InFlight and Cooldown scenes with a timeout `[official]` |
| Competitive or PvP live play | Nothing that takes control for more than about 1.5 s `[house]` | A locked player is a free kill |

Three tests before building `[house]`: (1) say what the player learns or feels in one sentence; (2) say why play cannot deliver it; (3) the scene still works with sound off and at phone size. Failing any one means cut it or make it a glance.

## 2. Length budgets

One production game removed a polished 27 s intro that sat inside the first minute, even with a 3 s skip `[lihfolk]`. Hancock's console-era ceiling was 2 minutes for any scene; for a phone-first audience in short sessions the house ceiling is half that.

| Purpose | Budget `[house]` | Repeat views |
|---|---|---|
| First-join intro | None by default; the one exception (mood-driven genres) and its ceiling are owned by `tutorial-and-onboarding.md` §2 | Never again |
| Glance ("look there") | 1–2 s out and back | Once per event |
| Zone or map reveal | 2–4 s, one shot | First visit only |
| Round intro flyover (shared) | 3–6 s, inside time the round already spends spawning and streaming; skip is personal (§7) | Every round, so keep it under 4 s after the first |
| Ability, takedown or finisher camera | 0.8–2.5 s | Every use: vary the angle or players tire of it |
| Reward or hatch reveal | 2–4 s | 1 s fast version, tap to skip, or off by setting |
| Boss reveal | 4–8 s in 2–3 shots | Second attempt onward: 1.5 s title sting only |
| Death or jumpscare camera | 1.5–3 s | Never the same unskippable scare twice `[community]` |
| Story beat mid-session | 10–25 s; over 30 s, split it with play | Skipped by default, replayable from a menu |
| Chapter ending | 20–45 s, hard cap 60 s | Replayable from a menu |

Skip follows the one rule in §8 for every row. Budget for a whole session: non-interactive time under about 5% of play (30 s in 10 minutes) `[house]`. A shot needs 1.2 s or more on a phone to be read; a typical shot runs 2–4 s; hold the first and last frame 0.3–0.5 s `[house]`.

## 3. Storyboard to shot list

Order of work, cheapest first (Schnitzer's previsualisation order, cut down for a small team): beat line → thumbnails → animatic → layout in engine → animation → lighting, sound, polish. The camera is locked at layout; animation then works to the camera, not the other way round.

1. **Beat line.** One sentence per beat, at most five beats. "Gate cracks. Light spills. Boss steps out. Boss roars at the player. Fight."
2. **Thumbnails.** One stick-figure frame per beat on paper or in Figma: where the subject sits in frame, where it looks, which way it moves.
3. **Animatic.** Thumbnails cut against scratch sound at real length. This is the only cheap moment to find out the scene is too long.
4. **Shot list.** The contract between design, animation and code; one row per shot.
5. **Layout.** Grey-box the shot list in Studio with the §14 runner and static actors. Fix framing and timing here, then animate.

| # | Start (s) | Length | Size | Angle | Move | FOV | Subject and action | Cues | Purpose |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0 | 2.5 | Wide | Low, eye at 2 studs | Slow push-in, 6 studs | 50 | Gate splits, light pours out | `GateOpen` (state), rumble, music duck | Where we are; something is coming |
| 2 | 2.5 | 2.0 | Medium | Low, 15° off axis | Static, slight drift | 40 | Boss steps through, turns head to camera | `Step` markers, dust | Who it is, how big |
| 3 | 4.5 | 2.0 | Close | Eye level | 0.5 s push, then hold | 35 | Roar | Stinger on the cut, shake 0.3, title card | Threat; hand over to the fight |

Rules for the list: every shot has one purpose; size changes by at least two steps between neighbouring shots of the same subject (wide to medium to close, not medium to slightly tighter medium); camera angle changes by 30° or more between shots of the same subject or it reads as a jump cut (the 30-degree rule); nobody walks from A to B on screen unless the walk is the suspense ("shoeleather", Schnitzer). Save animation effort the way film does (Schnitzer): frame out feet on moving characters, show one character at a time, and put actions that are hard to animate off screen with a sound and a reaction shot.

## 4. Shot vocabulary for Roblox avatars

`Camera.FieldOfView` is vertical by default, 1–120°, default 70 `[official]`. Frame height at distance `d` is `2 × d × tan(FOV / 2)`, so distance = frame height ÷ `(2 × tan(FOV / 2))`. A default R15 avatar is about 5 studs tall with a head of about 1.2 studs `[house]`; measure your own rig and scale the table.

| Shot | Shows | Frame height (studs) | Distance at FOV 30 | FOV 40 | FOV 50 | FOV 70 | Use |
|---|---|---|---|---|---|---|---|
| Extreme wide | Avatar under 1/10 of frame | 50+ | n/a | n/a | 54+ | 36+ | Scale, place, loneliness |
| Wide | Avatar about 1/3 of frame | 15 | 28 | 21 | 16 | 11 | Establish who is where |
| Full | Head to feet with air | 6.5 | 12 | 8.9 | 7.0 | 4.6 | Outfit, pet, pose, action |
| Cowboy | Mid-thigh up | 5 | 9.3 | 6.9 | 5.4 | 3.6 | Weapon at the hip, stand-offs |
| Medium | Waist up | 4 | 7.5 | 5.5 | 4.3 | 2.9 | Dialogue, reactions |
| Medium close | Chest up | 3 | 5.6 | 4.1 | 3.2 | 2.1 | A line that matters |
| Close | Head and shoulders | 2 | 3.7 | 2.7 | 2.1 | 1.4 | Emotion, the roar |
| Extreme close | Eyes or a prop | 0.8 | 1.5 | 1.1 | 0.9 | 0.6 | Props and hands only |

- **Lens choice.** FOV 70 is a very wide lens (about 17 mm on a full-frame camera); 50 ≈ 26 mm, 40 ≈ 33 mm, 30 ≈ 45 mm, 20 ≈ 68 mm `[house]` (from `12 ÷ tan(FOV / 2)`). Wide lenses stretch near objects and exaggerate depth; long lenses flatten and isolate. House defaults: establishing 55–70, action 45–60, dialogue and reveals 35–45, close-ups 25–40. Close-ups at FOV 70 put the camera 1.4 studs from a face: distorted, and one step from clipping through it. Community screenshot practice lands in the same place, FOV 50–60 for a "cinematic" look `[community]`.
- **Extreme close-ups of faces expose the model.** Low-polygon heads and missing lip-sync look worst at the tightest size (Schnitzer). Use them for props, hands and eyes on creature rigs built for it.
- **The line (180-degree rule).** Draw a line through two subjects, or along a subject's direction of travel. Keep every camera on one side of it and screen direction stays consistent: the boss always faces left, the player always right. Cross it only with a visible camera move or a neutral shot on the line (StudioBinder).
- **Lead room and headroom.** Leave more space in front of where a subject looks or moves than behind it; keep eyes near the upper third; do not centre everything.
- **Aspect ratios.** Vertical FOV is held constant (`Camera.FieldOfViewMode` defaults to `Vertical` `[official]`), so width changes by device: from `2 × atan(tan(FOV / 2) × aspect)`, FOV 70 gives a horizontal view of about 86° on a 4:3 tablet, 102° on 16:9 and 113° on a 19.5:9 phone (computed). Compose inside the centre 4:3 area and treat the sides as bonus. Check every shot on the Studio device emulator at a small phone and a tablet.
- **Motivated movement.** The camera moves because something moved, was revealed or changed (a push-in as the roar builds, a tilt up to show height). A move with no reason is the "flying 3D camera" look Schnitzer warns about. A still frame is a valid shot.
- **Entering from play.** The player can be anywhere when the scene starts. Hide the pop by making the first shot very different from the gameplay camera (opposite angle, close-up or high wide), by cutting in on a detail whose position you control, or by leading in from neutral scenery and letting the subject enter (Schnitzer).

## 5. Camera paths, easing and comfort

Why scripted cameras look robotic: (a) straight-line interpolation between waypoints, so velocity snaps at every corner; (b) one tween per segment, so the camera stops and starts at every waypoint; (c) rotation interpolated separately from position, so the subject drifts out of frame; (d) linear easing, the default selected in at least one cutscene plugin's panel (viewed) `[community]`.

| Do | How |
|---|---|
| One curve through all keys | Catmull-Rom spline (passes through its points; a Bezier is only shaped by them) `[community]`. A shot with two keys is a line; add a third key to give it an arc |
| Move by distance, not by spline parameter | Equal steps of the parameter bunch where keys are close and stretch where they are far, so the camera lurches at every key. Sample the curve into a length table once per shot and look up the point at each distance (§14 runner; sheet 14) |
| One speed profile per shot, never per waypoint | Ramp up, hold a constant speed, ramp down (a trapezoid), applied to distance along the whole curve. `TweenService:GetValue(alpha, Quad, InOut)` `[official]` is the same ramps with no hold: fine for a single two-key move. No Back, Bounce or Elastic on a camera |
| Aim, do not slerp | Keep a second curve for the look-at point, evaluated at the same key parameter as the position, and build `CFrame.lookAt(position, look)` each frame. Each key's framing is hit exactly, the subject stays framed and roll never creeps in |
| Give the camera weight | Real cameras on dollies ramp up and settle, so ease both ends (Schnitzer). House numbers: ramps of 0.3 s or more at each end, the settle longer than the start |
| Drive it per frame | One function of time evaluated in `BindToRenderStep` at `Enum.RenderPriority.Camera.Value + 1` `[official]`, so it can be sought, paused and skipped. Use time, never frame counts: a `for` loop over 60 exported frames with `task.wait()` runs at half speed on a 30 FPS phone |
| Cut instead of travelling | To get from A to B, cut. A long fly-through between two framings is travel time the viewer did not ask for |
| Set `Camera.Focus` every frame | A Scriptable camera does not update it, and lighting detail follows it `[official]` |

`TweenService` on `Camera.CFrame` is fine for exactly one move between two framings. Past that, chained tweens cannot seek, leave the camera mid-path when cancelled, and split restore logic across callbacks.

**Comfort limits** (extends the cutscene row in `accessibility-and-player-qol.md` §5; numbers `[house]`):

| Quantity | Limit |
|---|---|
| Sustained pan or tilt | Under 30°/s. Where a whip pan is tempting, cut instead |
| Speed changes mid-move | None: constant speed between the eased ends |
| Roll while moving | None. A static tilted frame up to about 10° is fine |
| FOV change inside a shot | 15° at most, over 0.5 s or more; dolly zoom only as a signature moment |
| Simultaneous motion | Two of translate, rotate, zoom; never all three |
| Handheld drift | Under 0.3° and under 0.5 Hz of smooth noise on static shots; off under reduced motion |
| Shake | Through the shared comfort gate and trauma model; values in `vfx-and-juice.md` §7 |
| Near plane | Keep the camera 1.5 studs or more from any surface it passes |

## 6. Staging actors

- **Actors are local.** Clone on the client and animate with a client `Animator`: nothing replicates, nobody else is disturbed (`animation-and-rigs.md` §7, §10). `Clone()` returns nil for an instance whose `Archivable` is false `[official]`, and player characters spawn that way `[community]`: set it true around the call and back afterwards. For another avatar use `Players:CreateHumanoidModelFromDescriptionAsync`, which yields, so build it during preload.
- **Hide what should not be in frame, locally.** Set `LocalTransparencyModifier` on the real character and on strangers standing on the stage, and put them back on exit. Never move or anchor other players for your shot.
- **Server-owned NPCs.** The server puts the boss in an `Intro` state (no attacks, no damage taken) and each client plays the performance on its own copy of the animation. The state has a fixed server duration; no client reports that it is "done".
- **Marks.** Actors start from named `Attachment` marks authored with the set in Blender, not from wherever gameplay left them. Store camera keys relative to an anchor (the arena origin, or the HumanoidRootPart for ability cameras) and multiply at play time, the "reference part" trick from Moon Animator workflows `[community]`.
- **Clip markers are cues.** Sound and VFX hang on `GetMarkerReachedSignal` markers (`animation-and-rigs.md` §6); hand-timed `task.wait` chains drift `[community]`. Use the same cue names in clips and timelines. When the camera lives in the clip (Cam bone), the clip is the clock; otherwise the timeline is.
- **Body-locked cameras** (first person, takedowns). Blender cameras do not import: animate a `Cam` bone or part in the actor rig (`animation-and-rigs.md` §10) and, in the render step after camera priority, copy its world CFrame (`Bone.TransformedWorldCFrame` for a bone) to the Scriptable camera `[community]`. Orient the bone in Blender so its −Z axis is the view direction, and carry FOV as marker parameters `[house]`. The restore rules in §7 apply unchanged.
- **Eyelines.** Actors look at each other or at a point just off the lens; straight into the lens only when addressing the player. Use the procedural head look-at from `animation-and-rigs.md` §9 for a live target.
- **Lip-sync status `[VS]`.** The engine has no automatic lip-sync. `FaceControls` on animatable heads can be keyed, and Studio's Face Capture records up to 60 s from a webcam (beta) `[official]`; the Fall 2026 roadmap lists FACS upgrades and root motion for mid-2027 `[official]`. Third-party animator plugins advertise lip-sync keying `[community]` (not tested). House position: on blocky avatars use body acting, a jaw or head beat per phrase, and subtitles; do not build a scene that depends on mouths.
- **Geometry.** Every prop and set piece in frame is Blender-authored and solid (house rules 1 and 2). Camera path points are data in a module, not parts left in `Workspace`: stray parts become primitive builds, and streaming can remove them. The one allowance is the §14 first-cutscene script: invisible, non-colliding marks in one `Atomic` model that the script checks before it plays.

## 7. The client-only architecture

The cutscene is presentation of a state change that has already happened on the server. The camera exists only on the client (`Workspace.CurrentCamera` `[official]`), so a "server cutscene" is always a broadcast: a server script that fires every client is how one player's trigger ends up hijacking everyone's screen `[community]`.

| The server may | The server may not |
|---|---|
| Decide the moment happened and change state at once: door open, boss in `Intro`, reward granted | Wait for a client to say the cutscene finished before granting, opening or starting anything |
| Tell the affected players which cutscene to play, with an anchor and a start time from `Workspace:GetServerTimeNow()` `[official]` | Move, anchor, freeze or teleport players who are not part of the moment |
| Pre-stream the stage with `Player:RequestStreamAroundAsync` before sending the event `[official]` | Trust "I am in a cutscene" from a client for protection |
| Grant protection it started itself, for a fixed time (scene length + 1 s), in PvE only | Write `Lighting`, HUD or camera properties for the scene (`lighting-and-atmosphere.md` §10) |
| End `Intro` states on its own timer | Run animation, camera or sound for the scene itself |

Cutscene data may sit on every client. A player who forces a scene to play early has only spoiled it for themselves; outcomes stay on the server `[community]`.

| Pattern | Use | Rules |
|---|---|---|
| Personal | Chest, zone reveal, quest beat, ending | Only this client plays it. Others see the player standing still. Skip is personal |
| Party-synced | Co-op boss reveal, round intro | Server sends the start time. Each client seeks to `now − start` and plays from there; more than half gone means jump to the end state. The boss wakes on the server clock, so a personal skip returns your camera but not an early fight. Offer a party vote-skip only if every present member has seen it |
| Server-wide event | Concert, live event, season finale | Roblox's EventSequencer runs scene timelines across servers with seeking and late join `[official]` (§13) |

- **Late joiners and streamed-in players** receive the end state, never a replay. The door is open; the boss is already fighting.
- **Death and respawn.** On `Humanoid.Died` or `CharacterRemoving` the runner exits and the respawn pipeline owns the camera (`level-design-worldbuilding.md`, respawn). Guis with `ResetOnSpawn` are rebuilt on respawn, so a list of "the ScreenGuis I disabled" goes stale: hide the HUD through one gate that every HUD controller reads.
- **Restore list.** Camera type, subject and FOV; controls (`PlayerModule` controls, or an `InputContext` with high `Priority` and `Sink` if the game uses the Input Action System `[official]` `[VS]`); `GuiService.TouchControlsEnabled`; HUD gate; `SetCoreGuiEnabled` changes; mouse behaviour and icon; proximity prompts; lighting lock and scene effects; music stack and duck; hidden characters; local actors and lights; letterbox and subtitle guis; gamepad selection.
- **Exit paths.** Finished, skipped, died, respawned, replaced by another cutscene, error in a step, watchdog timeout, teleport start. All of them call one function. "Camera stuck in the air" after returning to `Custom` and "stuck on the first point" threads are restore paths that were never written `[community]`.
- **Coming back.** The default camera resumes from its own remembered orbit, not from your last frame. Cover the seam: dip to black for 0.2 s, restore, fade in over 0.3 s; or end the last shot behind the character at gameplay distance.
- **VR.** Do not take the camera in VR: tilt and roll against the head cause sickness `[official]` (`Camera.VRTiltAndRollEnabled`). Give VR players the end state and a fade.

## 8. Skip, pause, subtitles and reduced motion

- **Skip: the one rule** `[house]`. Every scene longer than 3 s shows a skip control 2 s after it starts: the 2 s stop a button mashed during play from skipping by accident, and shorter scenes end about when a skip would appear. One exception: from the second view, reward and hatch reveals skip on the first tap (`accessibility-and-player-qol.md` §11). The control sits bottom-right at thumb size on a `ScreenGui` with the default insets (`ScreenInsets = None` is for non-interactive content such as fades and bars `[official]`) and shows on any input. Touch: one tap on the visible button. Keyboard and gamepad: hold for 0.6–0.8 s with a fill ring `[house]`. Skipping jumps to the end state (cues marked `state` still fire) and grants exactly what watching grants.
- **Repeats.** Full on first view; from the second view play the short version or nothing (`accessibility-and-player-qol.md` §11). Store "seen" in the profile the server already saves `[community]`.
- **Pause.** A personal scene may pause when the Roblox menu opens: freeze the clock, `AdjustSpeed(0)` on tracks, pause the audio. Synced scenes never pause; they run on the server clock.
- **Subtitles.** Rules and the display-time formula are in `accessibility-and-player-qol.md` §6. Cutscene additions from Hamilton's subtitle guide: on by default and switchable before the first line plays; two lines at most; one second minimum on screen; about 2–2.5 s per line for adults and 3–3.5 s per line for under-13s (BBC figures he cites), so pace Roblox scenes for children; leave a quarter-second gap between subtitles; split a line rather than reveal the twist early; name the speaker when it is not obvious; outline or plate behind the text, never a drop shadow alone.
- **Letterbox.** Bars say "controls are off", so never show them while the player can act. Height per bar = `max(0, (H − W ÷ 2.39) ÷ 2)`: 12.8% of height on 16:9, about 4.7% on a 19.5:9 phone, 22% on a 4:3 tablet, so cap at 10% `[house]`. Use a `ScreenGui` with `ScreenInsets = None` so bars reach the edges `[official]`; slide in over 0.3 s. Subtitles may sit on the lower bar if they stay at subtitle size.
- **Reduced motion.** Ask the comfort module (`accessibility-and-player-qol.md` §5): hold each shot at its final framing and cut between shots, cross-fade through black for big changes, no shake, no drift, no FOV animation. Read the setting when the scene starts and on change.

## 9. Dialogue presentation

| Element | Rule |
|---|---|
| Box | Bottom centre, at most 30% of screen height on a phone, above the thumb zones; speaker name on a tab; portrait optional (pattern seen in community dialogue kits, viewed) |
| Text | Two lines of about 40 characters per box on phones (`accessibility-and-player-qol.md` §6); split longer speech into more boxes, not smaller type |
| Reveal | Typewriter at 30–45 characters per second `[house]` using `MaxVisibleGraphemes`, which keeps rich text tags intact `[official]`. First tap completes the line, second tap advances |
| Advance | Tap anywhere, Space, E or gamepad A. Auto-advance is a setting; when on, use the caption display-time formula |
| Choices | Two or three, 44 px or taller, in the thumb arc; the server validates the choice and owns the outcome |
| Camera | Shop and quest talk keep the gameplay camera. Story dialogue may use an over-shoulder pair at FOV 40–50 on one side of the line; cut on speaker change only for lines longer than 2 s |
| Barks | One-liners that do not need an answer go in a bubble with `TextChatService:DisplayBubble` (client-side call) `[official]`, never a modal box |
| Text sources | Strings by key in a `LocalizationTable`; leave 30% spare width for translation; no player-written text in dialogue without filtering (`ui-input-crossplatform.md`) |
| Voice | One audio file per line so skip and advance cut cleanly; duck music under it (§11) |

The legacy `Dialog` and `DialogChoice` instances still exist `[official]` but give an unstyled click bubble; build the UI. Open-source runtimes worth reading before writing your own are in the library file.

## 10. Lighting and post-processing for a scene

- Take the lighting lock before touching anything: set the flag the zone controller checks (`LightingLocked` in `lighting-and-atmosphere.md` §10) and release it on exit so the controller blends back over 1–2 s.
- Add, do not edit. Create the scene's own `ColorCorrectionEffect`, `DepthOfFieldEffect` and lights as new local instances and destroy them on exit. Editing the zone grade in place is how a cutscene leaves the world tinted.
- Depth of field: set `FocusDistance` to the camera-to-subject distance every frame; safe ranges are in `lighting-and-atmosphere.md` §6. Low graphics levels drop post effects `[VS]`, so the shot must read without them: separate subject from background with value and a rim light first, blur second.
- One key light for the hero, no shadow casting on phones, budget in `lighting-and-atmosphere.md` §7. Light the face side nearest the camera.
- Fades are a full-screen frame in a top `ScreenGui`, not `Lighting` brightness. Large brightness jumps go through the flash gate (`accessibility-and-player-qol.md` §5).

## 11. Audio

- The cutscene takes the top slot of the music priority stack and gives it back on exit; the gameplay track pauses and resumes rather than restarting (`audio-sfx-music.md` §8).
- Put the stinger on the cut or the reveal frame, not on the scene start. Impacts sync as in `audio-sfx-music.md` §5: 0–30 ms after the picture, never before it. Only a music or ambience change may lead a cut, by 2–4 frames (a J-cut) `[house]`.
- Duck music and ambience 6–12 dB under speech and mute gameplay loops for the scene (`audio-sfx-music.md` §6).
- On skip, fade scene audio over 0.2 s; a hard stop clicks. State cues still restore the music stack.
- Voiced or beat-matched scenes read time from the audio (`TimePosition`), the approach behind `SyncToAudio` in Roblox's EventSequencer `[official]`; otherwise picture drifts from sound after any hitch.

## 12. Performance, streaming and readiness

- **Preload in the background, ahead of the trigger** (on entering the boss corridor, not on pressing the gate): animations, sounds and UI images through `ContentProvider:PreloadAsync`. It does not cover `SurfaceAppearance` or `MaterialVariant` `[official]`. Never turn this into a loading screen: a long or fake one is a reported reason to quit `[community]`.
- **Streaming.** Content streams around the character, not the camera, so a remote camera sees a hole. Cheapest fix: keep the stage inside the minimum streaming radius of the player. Otherwise the server calls `RequestStreamAroundAsync(position, timeOut)` before the event (it yields and gives no guarantee `[official]`), or for a longer remote scene adds a part with `Player:AddReplicationFocus` (server only `[official]`) and removes it afterwards. A community package moves a server-made focus part with a Scriptable camera `[community]`.
- **Readiness gate.** Before the first frame, check that every actor, mark and asset exists, with a 1.5 s limit `[house]`. Not ready means do not play: apply the end state and continue. Duvall Drive proceeds after a timeout the same way `[official]`; a community Moon player exposes `canFindObjects` for the same reason `[community]`.
- **Cost.** The runner is a few vector operations per frame. The real costs are cloned actors, extra lights and depth of field. On a 3 GB Android phone: at most two cloned characters, one scene light without shadows, and depth of field only above the low graphics levels `[house]`. Measure with the MicroProfiler (`performance.md`).
- **Exported per-frame cameras** (Moon Animator writes one CFrame per frame, 60 per second by default `[community]`): index by time and interpolate between neighbours; store as a compact module, not thousands of value instances.

## 13. Authoring tools compared, and a data format

| Approach | Good for | Limits | Status |
|---|---|---|---|
| Hand-written `TweenService` calls | One two-point move | Stop-start at waypoints, no seek, restore code scattered | Always available |
| Path modules: CutsceneService (Bezier through numbered parts, restores camera type and CoreGui) | Fly-throughs, menu backdrops | Points are parts in `Workspace`; a Bezier does not pass through its points; client-only, you trigger it | MIT, last commit 2026-04 `[community]` |
| Editor plugins: CineCam v3, Cutscene Cinematics, Smooth Cutscenes | Placing keys by eye, preview in edit mode, per-key FOV and easing | Export per-key tween scripts; check the default easing; one "Broadcast" export fires every client | 2022–2026, closed plugins `[community]` `[VS]` |
| Moon Animator 2 camera track, or newer animator plugins with scene and camera rows | Hand-keyed action cameras tied to character animation; `AttachToPart` camera on a rig | Paid `[VS]`; exports a CFrame per frame; `AttachToPart` exports need re-keying to CFrame to match in game `[community]` | Widely used `[community]` |
| Blender Cam bone in the actor rig | First-person scenes, takedowns, anything locked to a body | Needs the rig pipeline; FOV travels as marker parameters | House default for body-locked cameras (`animation-and-rigs.md` §10) |
| EventSequencer | Concerts, live events, multi-scene shows synced across servers; seek and late join; inline mode for existing places | Heavy for a 4 s reveal; scenes are folders with client and server schemas | Roblox module `[official]` |
| Data-driven timeline (below) | Everything else: reveals, intros, endings, capture paths | You write the runner once | House default |

Roblox ships no track-based sequencer; its own showcase team typed keyframes into a script-driven `EventManager` (interpolants, scripts, audio, camera shakes per event) and said they would have liked a track UI `[official]`. The house format follows the same idea. Its core is the `Timeline` type of the §14 runner (code in `cutscenes-and-cinematics-runner.md`): `length` and `skipAfter` in seconds; `shots[]` of `{ t, length, keys[], easeIn?, easeOut? }`, where a new entry is a cut and `keys[]` are `{ pos, look, fov }` (one key is a static shot, two a move, three or more a spline; one speed profile per shot); `cues[]` of `{ t, id, state? }` sorted by time, each `id` looked up in one cue table (sound, VFX, subtitle, actor clip, title card), with `state = true` on cues that must also run on skip. Add when the scene needs them: `anchor` (the mark all positions are relative to), `subtitles[]` of `{ t, key, speaker? }` (localisation keys; display time from the caption formula), `actors[]` of `{ name, rig, mark, clip }` (local clones built during preload) and `short` (the repeat-view timeline).

Everything is a function of time, so the same data plays, seeks for late joiners, skips to the end, renders the reduced-motion variant and replays identically for trailer capture.

## 14. First-cutscene script and timeline runner

### First cutscene (beginners start here)

One shot for a first scripted camera: it waits until the marks are there, fades in from black, glides through two or three marks at a steady speed with eased ends, plays one sound, offers Skip at 2 s (§8), and gives back camera, controls and HUD on every exit. Set-up: in `Workspace` make a Model named `IntroCamera` with `ModelStreamingMode` set to `Atomic` (its parts then arrive together `[official]`). Inside it: Parts `Cam1`, `Cam2` and optionally `Cam3` along the path, and `LookAt` where the camera aims, each with Anchored on, CanCollide, CanTouch and CanQuery off and Transparency 1; plus one `Sound` placed directly in the model, not in a part, so it plays at full volume `[official]`. Keep the marks within 64 studs of the spawn (the default `StreamingMinRadius` `[official]`) and 1.5 studs from any surface.

```lua
--!strict
-- FirstCutscene: a LocalScript in StarterPlayerScripts. Unexecuted: play it, then run every test listed below.
local Players, RunService, TweenService = game:GetService("Players"), game:GetService("RunService"), game:GetService("TweenService")
local MOVE, EASE, SKIP_AFTER, SOUND_AT = 4, 0.8, 2, 1.5 -- seconds: travel, speed-up and slow-down, skip (§8), sound
local player = Players.LocalPlayer
if not game:IsLoaded() then game.Loaded:Wait() end
if game:GetService("VRService").VREnabled then return end -- never take the camera in VR (§7)
local character = player.Character or player.CharacterAdded:Wait()
local model = workspace:WaitForChild("IntroCamera", 1.5) -- 1. Ready check (§12): missing after 1.5 s means no scene
local h, target = character:WaitForChild("Humanoid", 1.5), model and model:FindFirstChild("LookAt")
local sound = model and model:FindFirstChildOfClass("Sound")
local marks: { Vector3 } = {}
for _, name in { "Cam1", "Cam2", "Cam3" } do
	local mark = model and model:FindFirstChild(name)
	if mark and mark:IsA("BasePart") then table.insert(marks, mark.Position) end
end
if not (h and h:IsA("Humanoid") and target and target:IsA("BasePart") and #marks >= 2) then return end
local humanoid, lookAt = h :: Humanoid, target :: BasePart
if sound then game:GetService("ContentProvider"):PreloadAsync({ sound }) end
-- 2. One smooth curve through the marks, cut into short straight steps so the camera can move by distance.
local path, dist = { marks[1] }, { 0 }
for i = 1, #marks - 1 do
	local a, b, c, d = marks[math.max(i - 1, 1)], marks[i], marks[i + 1], marks[math.min(i + 2, #marks)]
	for k = 1, 20 do
		local u = k / 20
		local p = (b * 2 + (c - a) * u + (a * 2 - b * 5 + c * 4 - d) * u * u + (b * 3 - a - c * 3 + d) * u * u * u) * 0.5
		table.insert(dist, dist[#dist] + (p - path[#path]).Magnitude)
		table.insert(path, p)
	end
end
local function cameraAt(t: number): Vector3 -- speed ramps up for EASE s, holds steady, ramps down for EASE s
	t = math.clamp(t, 0, MOVE)
	local top = 1 / (MOVE - EASE) -- share of the path covered per second at full speed
	local share = if t < EASE then top * t * t / (2 * EASE) elseif t > MOVE - EASE then 1 - top * (MOVE - t) ^ 2 / (2 * EASE) else top * (t - EASE / 2)
	local goal, i = share * dist[#dist], 2
	while i < #dist and dist[i] < goal do i += 1 end
	return path[i - 1]:Lerp(path[i], math.clamp((goal - dist[i - 1]) / math.max(dist[i] - dist[i - 1], 1e-6), 0, 1))
end
-- 3. A black cover that reaches the screen edges, and a Skip button that stays inside the safe area.
local cover, skip = Instance.new("Frame"), Instance.new("TextButton")
cover.Size, cover.BackgroundColor3, cover.BorderSizePixel = UDim2.fromScale(1, 1), Color3.new(0, 0, 0), 0
skip.AnchorPoint, skip.Position, skip.Size = Vector2.new(1, 1), UDim2.new(1, -16, 1, -16), UDim2.fromOffset(120, 52)
skip.Text, skip.TextSize, skip.Visible = "Skip", 24, false
local guis = { Instance.new("ScreenGui"), Instance.new("ScreenGui") }
guis[1].ScreenInsets, cover.Parent, skip.Parent = Enum.ScreenInsets.None, guis[1], guis[2]
-- 4. One way out: finished, skipped, died, respawned, an error and the safety timer all call finish().
local camera, playerGui = workspace.CurrentCamera, player:WaitForChild("PlayerGui")
local controls = (require :: any)(player:WaitForChild("PlayerScripts"):WaitForChild("PlayerModule")):GetControls()
local oldType, oldFov, clock, played, done = camera.CameraType, camera.FieldOfView, 0, false, false
local hidden: { ScreenGui }, connections: { RBXScriptConnection } = {}, {}
local function finish()
	if done then return end
	done = true
	RunService:UnbindFromRenderStep("FirstCutscene")
	for _, connection in connections do connection:Disconnect() end
	camera.CameraType, camera.FieldOfView, camera.CameraSubject = oldType, oldFov, humanoid
	controls:Enable()
	for _, gui in hidden do gui.Enabled = true end
	skip.Visible, cover.BackgroundTransparency = false, 0 -- black for a moment hides the camera snapping back
	local fade = TweenService:Create(cover, TweenInfo.new(0.3), { BackgroundTransparency = 1 }) -- fade back in (§7)
	fade.Completed:Once(function() for _, gui in guis do gui:Destroy() end end)
	fade:Play()
end
local function step(dt: number) -- runs every frame and never waits
	clock += math.min(dt, 0.1)
	skip.Visible = clock >= SKIP_AFTER
	if sound and not played and clock >= SOUND_AT then played = true; sound:Play() end
	local position = cameraAt(if game:GetService("GuiService").ReducedMotionEnabled then MOVE else clock) -- less motion: hold the end
	camera.CFrame, camera.Focus = CFrame.lookAt(position, lookAt.Position), CFrame.new(lookAt.Position)
	if clock >= MOVE + 0.5 then finish() end -- the last framing holds for 0.5 s
end
local function start()
	camera.CameraType = Enum.CameraType.Scriptable
	controls:Disable()
	for _, gui in playerGui:GetChildren() do -- the game's own HUD; finish() turns it back on
		if gui:IsA("ScreenGui") and gui.Enabled then gui.Enabled = false; table.insert(hidden, gui) end
	end
	for _, gui in guis do gui.Parent = playerGui end
	TweenService:Create(cover, TweenInfo.new(0.6), { BackgroundTransparency = 1 }):Play() -- fade in from black
	connections = { humanoid.Died:Connect(finish), player.CharacterRemoving:Connect(finish), skip.Activated:Connect(finish) }
	task.delay(MOVE + 3, finish) -- safety net: control always comes back
	RunService:BindToRenderStep("FirstCutscene", Enum.RenderPriority.Camera.Value + 1, function(dt: number)
		local ok, err = pcall(step, dt)
		if not ok then warn("FirstCutscene:", err); finish() end
	end)
end
if not pcall(start) then finish() end
```

Test each, and after each check you can walk, the camera follows you and the HUD is back: watch to the end; press Skip as soon as it shows; reset mid-scene (Esc, Reset); delete `Cam2` (the scene must simply not play); a phone in the device emulator (Skip clear of the notch); Reduce Motion on (the camera holds the end framing). It plays on every join, which suits testing; for first join only, the server saves a "seen" flag in the profile it already keeps (§8) and the script skips when it is set. Change the four numbers at the top and where the marks sit; nothing else needs editing.

### Timeline runner

For scenes with several shots, cuts and cues, use the full client module in `cutscenes-and-cinematics-runner.md` (about 150 lines, `--!strict`, unexecuted, with a hand check and the exit tests). It plays a §13 timeline. Before it takes the camera it builds a length table for each shot (32 samples per key-to-key segment), so the camera moves by distance along a Catmull-Rom curve; speed follows one ramp–hold–ramp profile per shot (`easeIn` 0.4 s and `easeOut` 0.6 s by default); the aim follows its own curve through the keys' look points; cues fire by time on spawned threads, and `state` cues also fire on skip. Finished, skipped, died, respawn, teleport, replaced, error and watchdog all go through one `finish` that undoes everything in reverse order. Left out on purpose: the readiness gate (§12), anchor transform, pause, seeking for synced scenes, fades and shake.

## 15. First-session intros that do not cost the first 30 seconds

The first-join rule is owned by `tutorial-and-onboarding.md` §2: no intro by default, and one exception for genres where mood is the product (horror, story-led), with its ceiling and how to measure it. Evidence behind it: the same guide's case study (§12) disabled a 27 s intro `[lihfolk]`, and community post-mortems of weak day-one retention keep pointing at the seconds before control, long loading screens first `[community]`. Ways to arrive with style:

| Technique | Cost to the player | How |
|---|---|---|
| Arrival framing | 0 s | Spawn facing the verb target with the camera already composed: establishing shot and gameplay camera are the same frame |
| Playable pull-in | 0 s | Start the camera wide and ease to gameplay distance over 1.5–2.5 s with controls live from frame one; any input ends the move |
| Title sting over play | 0 s | Logo and three-note sting fade over live gameplay for 1.5 s; no popup rules broken, nothing to dismiss |
| Deferred story beat | Up to 8 s, skippable | After `FirstReward` (30–60 s in), when the player has a reason to care |
| First boss or first chest reveal | 2–6 s | The first cinematic the player sees is a reward they caused |
| Mood intro (horror, story-led only) | Inside the tutorial guide's ceiling | One shot that ends in the player's own framing so control returns without a jump: the §14 first-cutscene script, with a slam, blackout or cut to black hiding the hand-over |

Measure it: log time from `Spawned` to `FirstAction` as an `FtueBeat` (`tutorial-and-onboarding.md` §2, instrumented in its §9) and compare variants in an experiment. Returning players never see an intro. The first-minute script and step funnel are owned by `tutorial-and-onboarding.md`.

## 16. In-engine trailers and marketing capture

Two deliverables with different rules. The **game-page gameplay video** (autoplays in Recommended For You) is owned by `icons-thumbnails-and-store-page.md` §9: policy list, measured lifts, structure. The part that matters here: varied and "cinematic" camera angles are allowed as long as they show real gameplay, and free camera is the tool the docs name, but Roblox staff advise against cinematic trailers and dramatised gameplay in that slot `[official]` `[VS]`. So directed camera work goes into the **off-platform trailer** (YouTube, TikTok, Discord, event pages; channels and hooks in `growth-and-marketing.md` §4), which is still made only from real captures.

**Shot list for a 20–30 s trailer** `[house]`: 8–12 shots of 1.5–3 s. One establishing wide; three or four core-loop shots from the real gameplay camera with HUD; two hero shots (low angle, FOV 30–45, slow push); one multiplayer shot with team accounts; one payoff; end card of 1.5–2 s with the exact game name. Each shot has one idea, and either the subject moves or the camera does. Cut on action: leave a shot while the motion is still going and enter the next with it under way.

**Capture** (still-image route and quality settings are in `icons-thumbnails-and-store-page.md` §8; capture-place rules in `growth-and-marketing.md` §4):

- **Free camera upgrades (2026).** Left Shift + P works in a Studio playtest and, for the owner and editors, in the live client `[official]`. With `Workspace.PlayerScriptsUseInputActionSystem` enabled it adds roll, per-control speed and stiffness, a player lock that tracks a chosen player, Screen GUI and leaderboard toggles, and its own post-processing menu `[official]` `[VS]`. Low stiffness is the built-in ease: set it before recording moving shots. Leave the post menu off for anything going to the game page, where only minor adjustments pass.
- **Video recording.** OBS at constant bitrate of 20,000 kbps or more, MP4, 60 FPS, canvas up to 3840×2160; name files by project, shot type and shot name (Roblox staff tips `[official]`). Record landscape and crop later.
- **Repeatable takes.** Fly hero shots with the §14 runner on saved timelines so the same move can be re-shot after an art change. Hand-flown free camera is for discovery; the keeper is data.
- **`CaptureService` is for players, not trailers.** `StartVideoCaptureAsync` records at most 30 s with voices muted and hands the player a clip to save or share; screenshots can leave out UI `[official]`. Use it for a photo mode or a "save this moment" prompt after a boss kill: opt-in, never a gate, never a reward condition.
- **Trailer music.** Roblox's Creator Store music is licensed for use inside Roblox only (Terms of Use §7.1, `audio-sfx-music.md` §3) `[official]`: score an off-platform trailer with music you own or have licensed for that use.
- **Pre-rendered video inside the game** costs Robux per upload according to a 2026 forum report `[community]` `[VS]`, cannot restyle with the game and does not show the player's own avatar. In-engine scenes are the default.

## 17. The amateur cutscene: tells and fixes

| Tell | Fix |
|---|---|
| Camera glides in straight lines, at linear speed, or pauses at every waypoint | One spline per shot, travelled by distance, with ramps of 0.3 s or more at its two ends only (§5) |
| Camera never stops moving, flies through walls, orbits for no reason | Motivate each move or hold the frame; keep 1.5 studs from geometry; cut instead of travelling |
| Everything at FOV 70 | Pick a lens per shot from §4 |
| Subject dead centre in every shot, looking out of frame | Thirds, lead room, eyes on the upper third |
| Characters flip sides between shots | Stay on one side of the line (§4) |
| Cut between two nearly identical framings | Change size by two steps and angle by 30° |
| Close-up of a blocky face delivering a speech | Medium shot, body acting, subtitles |
| Characters walk the whole distance | Cut the shoeleather: leave frame, cut, arrive |
| Scene starts with a pop from wherever the player stood | Contrasting first shot, cut-in or lead-in (§4) |
| Sound starts late, music cuts dead | Stinger on the cut; fades; priority stack (§11) |
| Unskippable, plays every time, on every server join | Skip per the §8 rule; seen flag; short version |
| Bars, big title text and lens flare on a 3 s reveal | Remove decoration until the shot reads without it |
| Whole server watches one player's trigger | Client-only; server sends state to the affected players (§7) |
| HUD gone, camera stuck or FOV changed afterwards | One runner, one exit, watchdog (§14) |
| Idle actors stand in default pose, mouths shut while "talking" | Author an idle and a gesture per line; avoid mouth-dependent framing (§6) |

## 18. Critique rubric

Score each line 0 (absent), 1 (partly) or 2 (clearly); ship at 16 of 20 or more with no zero in the first four `[house]`.

| # | Criterion | Observable test |
|---|---|---|
| 1 | Earns its place | One-sentence purpose; play could not deliver it |
| 2 | Within budget | Length inside the §2 row; shots of 1.2 s or more |
| 3 | Leaves cleanly | All eight exit paths restore camera, controls, HUD, lighting and audio |
| 4 | Skippable and fair | Skip per the §8 rule; same end state and rewards; repeat views shortened |
| 5 | Reads on a phone, muted | Story clear on a small screen with sound off; subtitles on |
| 6 | Shots are chosen | Size, angle and lens differ with purpose; line respected; lead room |
| 7 | Motion has weight | Eased, splined, motivated; inside the §5 comfort limits; reduced-motion variant |
| 8 | Staging | Actors on marks, eyelines right, nothing unintended in frame |
| 9 | Sound and light serve the frame | Stinger on the reveal; subject separated from background |
| 10 | Disturbs nobody else | No other player frozen, moved, blinded or made to wait |

## 19. Level-up: symptom → cause → fix

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| New players leave before the first input | Intro scene or loading screen in the first 30 s | §15: no intro, or the mood exception inside its ceiling; defer the story beat |
| Skip rate above about 70% on first view `[house]` | Too long, or it plays before the player cares | Halve it; move it after a reward; make it a glance |
| Camera stuck, floating, or wrong FOV after a scene | A missing exit path (death, error, replaced) or two scripts writing the camera | One runner with reverse-order restore and a watchdog; one FOV owner |
| HUD or touch controls missing after respawn | Disabled ScreenGuis were rebuilt; restore held stale references | One HUD gate attribute; restore on `CharacterRemoving` |
| Everyone sees one player's cutscene | Server fires all clients, or a shared trigger part handled without a player check | Fire the affected player only; the client checks it is the one who touched |
| Black holes or missing props in remote shots | Streaming follows the character | Keep the stage near; `RequestStreamAroundAsync`; replication focus; readiness gate (§12) |
| First viewing stutters or actors appear in T-pose | Assets fetched on first play | Background preload before the trigger; build actors during preload |
| Scene runs slow or desynchronised on phones | Frame-indexed playback or `task.wait` chains | Time-based evaluation; marker cues; audio clock for voiced scenes |
| Motion-sickness complaints | Roll, fast pans, FOV swings, per-waypoint stop-start | §5 limits; honour reduced motion |
| World stays tinted or dark afterwards | Scene edited zone lighting in place; two writers | Lighting lock; own effect instances destroyed on exit (§10) |
| Music restarts or doubles after a scene | Scene stopped tracks directly | Priority stack push and pop (§11) |
| Players killed while watching | Client-claimed protection or none | Server-started bounded protection in PvE; no control-taking scenes in PvP |
| Game-page video rejected | A cinematic trailer, narration, lyrics, ad text or enhanced visuals in the gameplay-video slot | Re-cut as plain gameplay (`icons-thumbnails-and-store-page.md` §9); keep the trailer off-platform |

## Review gate

- [ ] Every cutscene has a one-sentence purpose, a §2 budget row, and a reason play could not do the job.
- [ ] Any first-join intro meets the rule in `tutorial-and-onboarding.md` §2; returning players never see one.
- [ ] A shot list exists before keying; neighbouring shots differ by two sizes or 30°; the line is respected.
- [ ] Lens chosen per shot; no face close-ups at FOV 70; composition checked at 4:3 and 19.5:9.
- [ ] Camera paths are splines travelled by distance with one ramp–hold–ramp per shot, time-based, inside the comfort limits, with a reduced-motion variant.
- [ ] One runner owns the camera; finished, skipped, died, respawn, replaced, error, watchdog and teleport all restore camera, controls, HUD, lighting and audio (tested by hand).
- [ ] State changes and rewards happen on the server before the scene; skipping and disconnecting lose nothing; late joiners get the end state.
- [ ] No other player is frozen, moved or shown the scene unless they are part of the moment; protection is server-started and time-boxed.
- [ ] Skip control follows the §8 rule on every device; repeat views shortened; subtitles on by default at child reading pace.
- [ ] Stage preloaded and streamed before the trigger; readiness gate falls through to the end state.
- [ ] Scene lighting and post are separate instances removed on exit; music uses the priority stack.
- [ ] Cinematic trailers stay off-platform and use real captures, team accounts and music owned or licensed for off-platform use (not Creator Store tracks); the game-page video passes `icons-thumbnails-and-store-page.md` §9.

## Sources

Accessed 2026-11-11. "(read)" = opened and read; "(viewed)" = image looked at; "(oembed)" = video existence and author verified, not watched; "(search summary)" = seen only as web search result text.

- Roblox/creator-docs at commit 7cbffff (read): `workspace/camera/index.md`, `workspace/camera/free-camera.md`, `production/publishing/thumbnails.md`, `resources/modules/event-sequencer.md`, `resources/the-mystery-of-duvall-drive/{main-design-requirements,foundational-gameplay-systems}.md`, `animation/capture.md`, `input/input-action-system.md`, `workspace/streaming/{index,techniques}.md`, `ui/animation.md`; reference pages `Camera` (and the `FieldOfViewMode`, `CameraType` enums), `CaptureService`, `VideoCapture`, `Capture`, `ScreenshotHud`, `ContentProvider`, `Player`, `GuiService`, `RunService`, `TweenService`, `TextChatService`, `ScreenGui`, `FaceControls`, `Dialog`, `Instance`, `Players`, `Workspace`, `AnimationTrack`.
- Roblox staff posts (read): https://devforum.roblox.com/t/full-release-enhanced-freecam-capabilities/4848482 (2026-09); https://devforum.roblox.com/t/gameplay-videos-on-home-help-your-games-get-discovered/4842601 (2026-08); https://devforum.roblox.com/t/tips-for-capturing-high-quality-screenshots-and-videos-in-studio/2723897 (2024-02); https://devforum.roblox.com/t/creator-roadmap-2026-fall-update/4880208 (2026-09); https://devforum.roblox.com/t/turn-screenshots-into-teleporting-paintings/4974220 (2026-11).
- DevForum tutorials and resources (read): camera animations with Moon Animator https://devforum.roblox.com/t/camera-animations-for-cutscenes-and-gameplay/1181691; CutsceneService https://devforum.roblox.com/t/cutsceneservice-smooth-cutscenes-using-b%C3%A9zier-curves/718571 and https://github.com/Vaschex/CutsceneService (cloned; MIT); CineCam https://devforum.roblox.com/t/4713811; Cutscene Cinematics https://devforum.roblox.com/t/4369035 (panel viewed); Smooth Cutscenes https://devforum.roblox.com/t/1893802; Moon2Cutscene https://devforum.roblox.com/t/3001411; Catmull-Rom module https://devforum.roblox.com/t/1568205; Moon `AttachToPart` export fix https://devforum.roblox.com/t/3113931; Camera Replication Focus https://devforum.roblox.com/t/2653957; Apex Animator https://devforum.roblox.com/t/4918289; Dialogue Kit V2 https://devforum.roblox.com/t/3106134 (viewed); high-quality screenshots https://devforum.roblox.com/t/taking-high-quality-screenshots/330052; horror guide https://devforum.roblox.com/t/guide-to-making-better-horror-experiences/2212571.
- DevForum support and feedback threads (read): synced cutscenes and marker cues https://devforum.roblox.com/t/how-to-make-synced-cutscenes/2668540; client or server https://devforum.roblox.com/t/should-cutscenes-be-managed-on-the-client/570514 and https://devforum.roblox.com/t/what-is-the-right-way-to-handle-cutscenes/3258546; everyone sees one cutscene https://devforum.roblox.com/t/3651449; camera stuck https://devforum.roblox.com/t/909434 and https://devforum.roblox.com/t/1671591; cutscene organisation https://devforum.roblox.com/t/1770927; retention and loading screens https://devforum.roblox.com/t/4557364; video upload fee https://devforum.roblox.com/t/4912625; Moon Animator pricing https://devforum.roblox.com/t/2181571; character `Archivable` default https://devforum.roblox.com/t/630401 (one reply).
- Adam Schnitzer, "How to Build a Better Cutscene", Game Developer, 2003 https://www.gamedeveloper.com/art/how-to-build-a-better-cutscene (read). Hugh Hancock, "Better Game Design Through Cutscenes", Game Developer, 2002 https://www.gamedeveloper.com/design/better-game-design-through-cutscenes (read). Ian Hamilton, "How to do subtitles well", Game Developer, 2015 https://www.gamedeveloper.com/audio/how-to-do-subtitles-well-basics-and-good-practices (read).
- StudioBinder: shot sizes https://www.studiobinder.com/blog/types-of-camera-shots-sizes-in-film/, the 180-degree rule https://www.studiobinder.com/blog/what-is-the-180-degree-rule-film/, camera movement https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/ (read; cheat-sheet images viewed). The 30-degree rule: Wikipedia summary (read).
- GDC talks (oembed): John Nesky, "50 Game Camera Mistakes" https://www.youtube.com/watch?v=C7307qRmlMI; Squirrel Eiserloh, "Juicing Your Cameras With Math" https://www.youtube.com/watch?v=tu-Qe66AvtY; Simon Unger, "Animating Cameras for Games" https://www.youtube.com/watch?v=hP1Vz70WouE.
- DOORS Seek reveal structure: game-guide articles (search summary); compilation video listed in the library file (oembed).
- Sibling guides for `[lihfolk]` figures: `tutorial-and-onboarding.md` §2 and §11–12, `genres/horror-coop-escape.md`, `accessibility-and-player-qol.md` §5–6. Game-page video policy and lifts: `icons-thumbnails-and-store-page.md` §9.
- Failed or not found: reddit.com not reachable; Wikipedia API rate-limited after two pages; no breakdown by the developers of DOORS, Pressure or Deepwoken of how their scenes are built was found; no official statement of a maximum length or file format for game-page videos in the mirrored docs.
