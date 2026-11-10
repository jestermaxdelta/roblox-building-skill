# Animation and rigs: Blender to Roblox

What this is: the rigging and animation reference for a game whose models all come from Blender (house rule 1): rig choice, Blender rig rules, the clip pipeline, timing charts, playback, markers, replication, NPC scale, procedural layers, bugs and budgets. Open it before the first rig is built, when a clip looks or replicates wrong, or when auditing a live game's `stepAnimation` cost. It extends `references/art-pipeline-blender.md` (static meshes, export scripts, upload) and does not repeat it.

Tags: `[official]` Roblox docs, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (measured in one live action game, October 2026, not Roblox-documented), `[house]` house estimate, `[VS]` version-sensitive: re-check at create.roblox.com/docs.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Keep players on their R15 avatar and the default `Animate` script; swap clip ids only. 2. Author one clip in Blender on a downloaded R15 rig, export FBX, import in the Clip Editor, publish under the creator that owns the game. 3. Load each clip once with `Animator:LoadAnimation`, set `Priority` before `Play`. 4. Put a `Hit` or `Step` marker in the clip and hang sound and particles on it. 5. Move doors and chests with a client-side tween | Skinned custom rigs, IK, custom locomotion controllers, clip thinning, retargeting |
| Intermediate | One written priority convention; upper-body layering; marker times exported to a data table the server reads; clips preloaded on equip; playback rate matched to ground speed; frame charts (section 4) for every attack; NPCs animated per client from attributes | Lua keyframe players, physical joints, graph editor |
| Expert | Animation LOD that never skips time or events; shared skeleton families and retargeting; procedural layers in `PreSimulation` guarded by `EvaluationThrottled`; `AnimationConstraint` physical simulation; server-authority animation rules; key thinning and instance budgets; the interpolation caveats in section 3 | Nothing: measure with the MicroProfiler |

Terms: a **rig** is parts or mesh vertices joined by animatable joints. A **clip** is one animation asset. A **track** (`AnimationTrack`) is one clip loaded on one `Animator`. A **pose** is one joint's offset from its rest position at one keyframe.

## Contents

1 Rig types · 2 Blender rig requirements · 3 Blender to Roblox clip pipeline · 4 Craft: 12 principles and frame charts · 5 Playback: priorities, blending, weights, speed · 6 Markers · 7 Replication and ownership · 8 NPC animation at scale · 9 Procedural animation · 10 Tools and weapons, cutscenes, props, UI-in-world · 11 Performance budgets · 12 Level-up table · 13 Conflicts and open questions · Review gate · Sources

## 1. Rig types and when to use each

Three joint classes are animated by the engine `[official]`:

| Joint | Moves | Notes |
|---|---|---|
| `Motor6D` | A rigid part relative to its parent part: `Part0.CFrame * C0 * Transform = Part1.CFrame * C1` | The Animator writes `Transform` each frame. Animate through `Transform`, never by editing `C0`/`C1` per frame |
| `AnimationConstraint` | Same, through two Attachments; can also run force-limited (`IsKinematic = false`) for ragdolls and arm strength | Replaces Motor6D in R15 player characters when `StarterPlayer.AvatarJointUpgrade` is on (default for new experiences) `[VS]`. `IsA("Motor6D")` is false; `C0`, `C1`, `Part0`, `Part1` are read-only aliases |
| `Bone` | Vertices of a skinned MeshPart; a Bone is also an Attachment | `Bone.WorldCFrame` is the rest pose; read `TransformedWorldCFrame` for the animated position |

Clips bind by name: a pose named `RightUpperArm` drives the joint whose child part (or Bone) has that name. Keys for names the rig lacks are ignored without a warning `[lihfolk]`, which is why one clip set can drive a family of rigs and why a renamed part silently stops moving.

| Rig | What it is | Use for | Avoid when |
|---|---|---|---|
| R15 (standard) | 15 MeshParts, fixed names, `Root > HumanoidRootNode > LowerTorso > UpperTorso > Head / arms / legs` `[official]` | Player avatars; humanoid NPCs that should reuse avatar clips, emotes, accessories and layered clothing | You need a non-human silhouette |
| R15 (advanced) | Same plus up to 37 optional joints (spine, clavicles, fingers, toes) `[official][VS]` | Hero NPCs and avatars needing hands and shoulders | Crowd NPCs on a 3 GB phone |
| R6 | 6 parts, legacy | Only when the game's identity is R6. `Workspace.AvatarUnificationMode` (the R6-to-R15 adapter) is marked deprecated with "R6 avatars always load as R6 rigs" `[official][VS]` | New games: no layered clothing, no dynamic heads, no IK-ready limbs, a separate clip library |
| Custom part rig | Separate Blender meshes joined by Motor6Ds | Hard-surface creatures, robots, weapons, doors, vehicles' moving parts. Default for anything rigid `[lihfolk]` | Organic bending is the point |
| Skinned (bone) rig | One mesh, armature, weights | Organic creatures, tails, wings, cloth, faces | Limbs must collide or be raycast (see below) |
| Hybrid | Skinned body, rigid props on `RigidConstraint` to a socket Bone `[official: RigidConstraint accepts Bones]` | Most finished characters | n/a |

Decision rules:

- Controller: `Humanoid` plus `Animator` only when the character needs Humanoid movement, states, accessories or `MoveTo`. Otherwise `AnimationController` plus `Animator`; static NPCs "have no need for the Humanoid class" `[official: performance docs]`. Exception: a moving model of skinned MeshParts without a Humanoid rebuilds FastClusters on every move, and embedding a Humanoid is the documented workaround `[official]`.
- Part or skin: part rigs are debuggable in Studio, every piece can collide and take attachments, and a mesh swap needs no re-weighting. Skinned rigs look continuous but only the single MeshPart collides, in its rest shape `[official: bones "don't change the physical shape"]`.
- House rule 2 (everything solid) on rigs: give every character one invisible root collider and, where gameplay needs limb hits, small `_COL` hitbox parts on `RigidConstraint`s to bones or welded to rig parts; set the visual limbs `CanCollide = false`. Never rely on the skinned mesh's own collision for an animated limb.
- Custom humanoid proportions that should play any R15 clip: import with Rig Type Custom, then use Adaptive Animation (`HumanoidRigDescription`, T-pose tool); `Workspace.Retargeting` (`AnimatorRetargetingMode`) controls whether clips adapt to body proportions `[official][VS]`.
- Player avatars are the one visible model not authored by you. Everything attached to them (weapons, armour, pets) still comes from Blender.
- Faces `[official][VS]`: avatar heads animate through `FaceControls` (FACS poses, at least 17 base poses for Marketplace bodies). For custom NPCs a few jaw, brow and eye bones inside the 4-influence limit are cheaper than a full FACS head.

## 2. Blender rig requirements

Scene: 1 Blender unit = 1 stud, character faces −Y, feet on Z = 0, final in-game height (as in `art-pipeline-blender.md`); scene frame rate 30 fps (the Clip Editor's grid `[lihfolk]`; clips store seconds).

| Rule | Value | Tag |
|---|---|---|
| Bone and armature transforms | Frozen: scale 1,1,1 and rotation 0,0,0 | `[official]` |
| Root | Exactly one root bone at 0,0,0, with no vertex weights | `[official]` |
| Influences | At most 4 bones per vertex; weights normalised; no unweighted vertices | `[official]` limit, rest `[lihfolk]` |
| Triangles | ≤ 20,000 per mesh; avatar bodies 10,742 across 15 parts | `[official][VS]` |
| R15 names | Exactly the hierarchy in section 1; LowerTorso and Root at 0,0,0; rest pose I, A or T | `[official]` |
| Mesh naming | A mesh object named exactly like a bone becomes a Motor6D-driven part on import; name skinned meshes `<Part>_Geo` or `SK_<Name>` unless you want that | `[community][lihfolk]` |
| Bone names | ASCII, unique, stable, no `.001`; code and clips find joints by name | `[house]` |
| Roll | One rule for the whole rig (local X to the character's right), never hand-rolled per limb | `[lihfolk]` |
| Root motion | Key travel and lift on the first child of the root (`LowerTorso`, `Hips`). The top-level pose of a keyframe is not applied | `[lihfolk]` measured |
| Deform bones | Crowd NPC ≤ 25, regular enemy ≤ 40, boss ≤ 60 | `[house]`, upper two from `[lihfolk]` |
| Control rig | IK targets, poles and Rigify controls are non-deform and never exported. Roblox receives baked deform-bone keys only | `[lihfolk]` |
| Rest pose | Frozen before the first clip; clips are offsets from rest, so editing rest later breaks every clip | `[lihfolk]` |

Weight painting that survives import `[lihfolk]`: pose a range-of-motion action (every joint to its extremes) and paint while scrubbing it; Auto Normalize on; then Clean (threshold about 0.01), Limit Total 4, Normalize All; three edge loops across every bending joint; twist and cap helper bones are baked to keys on export because Roblox evaluates no constraints; never skin a weapon to the hand (separate part on a socket bone).

```python
# unexecuted sketch: select the armature, run in Blender before export.
import bpy
arm, problems = bpy.context.object, []
if any(abs(s - 1) > 1e-4 for s in arm.scale) or any(abs(r) > 1e-4 for r in arm.rotation_euler): problems.append("armature has unapplied scale or rotation")
roots = [b for b in arm.data.bones if b.parent is None]
if len(roots) != 1 or roots[0].head_local.length > 1e-4: problems.append("need exactly one root bone at the origin")
for b in arm.data.bones:
    if "." in b.name: problems.append(f"bone '{b.name}': no dots or .001 suffixes")
for mesh in (o for o in arm.children if o.type == "MESH"):
    names = {g.index: g.name for g in mesh.vertex_groups}
    for v in mesh.data.vertices:
        w = [names[g.group] for g in v.groups if g.weight > 1e-4 and names[g.group] in arm.data.bones]
        if not w: problems.append(f"{mesh.name}: vertex {v.index} unweighted"); break
        if len(w) > 4: problems.append(f"{mesh.name}: vertex {v.index} has {len(w)} influences"); break
        if roots and roots[0].name in w: problems.append(f"{mesh.name}: weights on the root bone"); break
print("\n".join(problems) or "RIG OK")
```

Export settings (pin the Blender version; option names drift):

| Setting | FBX | GLB |
|---|---|---|
| When | Roblox's documented rig and clip path; avatar bodies, heads, emotes `[official]` | Part rigs and creatures with several Actions; no unit dance `[lihfolk]`, verify per Studio version `[VS]` |
| Scale (fix a 100× error here, never by scaling the import in Studio: parts scale but clip translations keep the old units `[lihfolk]`) | Apply Scalings = FBX Unit Scale, every other scale 1.0 `[official]` | None needed; importer Scale Unit = Stud `[official]` |
| Axes | Forward = Z Forward, Up = Y Up; importer World Forward = Front, World Up = Top `[official]` | +Y Up on |
| Leaf bones | Add Leaf Bones off `[official]` | Not applicable |
| Deform only | Only Deform Bones on | Export Deformation Bones Only on |
| Baking | Bake Animation on for clips, off for static meshes `[official]`; Simplify 0; Key All Bones on `[lihfolk]` | Always Sample Animations on, step 1; Optimize Animation Size off `[lihfolk]` |
| Clips per file | One animation track per export `[official]` | Animation mode Actions; Reset Pose Bones Between Actions on `[lihfolk]` |
| Textures | Path Mode Copy with Embed Textures `[official]` | Packed |
| Before export | Clear the active Action and reset the pose, or the rest pose becomes a frame of that clip `[lihfolk]` | Same |

## 3. Blender to Roblox clip pipeline

1. **Rig in Blender.** For player clips download a standard R15 rig from the avatar resources page (or export a dummy from Studio); for NPCs and props Blender is the source of truth.
2. **Author.** One Action per clip, named as the game references it (`Idle`, `Walk`, `Attack1`), fake user on. Mark gameplay beats with Action pose markers. Check key poses from the gameplay camera angle, not the side view.
3. **Bake and export** with the table above. For a layered (partial) clip export only the bones it owns: sampled glTF keys every bone, and a still key at high priority pins the whole body `[lihfolk]`.
4. **Import.** Clip Editor (Avatar tab) > ⋯ > Import > From File on the matching rig in Studio `[official]`; the 2026 clip importer shares the 3D Importer path and adds glTF plus rig scale, rest pose and track selection options `[community][VS]`. Or import model and clips together with the 3D Importer (Rig Type R15 / Custom / No Rig).
5. **Finish in the Clip Editor.** Set looping and priority, add event markers (Blender markers do not arrive), rename the final keyframe `End` only for clips that replace default character animations `[official]`.
6. **Publish** to Roblox with Creator = the user or group that owns the game `[official]`. Automation: the Open Cloud Assets API accepts asset type Animation as `.rbxm`/`.rbxmx` (`model/x-rbxm`) `[official][VS]`.
7. **Record** id, length, loop flag, ground speed and marker times in one generated module (`Shared/Config/Animations.luau`). Never hand-type ids in scripts.
8. **Verify** with a calibration clip (right arm +90° forward, torso +30° yaw left) once per export route `[lihfolk]`, then in a published test place with two clients. Studio alone proves nothing: temporary ids from `AnimationClipProvider:RegisterAnimationClip` and `KeyframeSequenceProvider:RegisterKeyframeSequence` "cannot be used outside of Studio" `[official]`.
9. **Strip.** Delete saved `KeyframeSequence`/`CurveAnimation` sources and importer saves from the shipped place; a published clip costs no instances.

Community practice `[community]`: forum threads describe the Studio editor and Moon Animator as the lower-friction routes, and report that the long-running Blender rig exporter/animation importer add-on does not support skinned meshes and has broken after Studio updates. The route above uses only Blender's own exporters and Studio's importer, so it has no third-party plugin to break.

Ownership `[official][VS]`: animations are not covered by the Asset Privacy default switch; a clip loads only for its owner's experiences or where the owner granted the collaborator and the experience permission on the asset's Permissions page. Game grants cannot be revoked. A clip uploaded to a personal account will not play in a group game until shared or re-uploaded.

| | `KeyframeSequence` | `CurveAnimation` |
|---|---|---|
| Data | Keyframes of poses, quaternion rotation, easing per pose | One curve per channel, tangents, Euler or quaternion rotation |
| Needed for | Default from the dope sheet | Curve Editor work, FACS face channels, Marketplace emotes (under 10 s) `[official][VS]` |
| Trap | Legacy `Cubic` easing is reversed at runtime: use `CubicV2` `[official]` | Opening the Curve Editor converts quaternions to Euler irreversibly unless Default Rotation Type = Quaternions; motion can change near gimbal lock `[official]` |

Data hygiene (matters most when clips are generated, thinned or played by custom code) `[lihfolk]`:

- **Euler wrap.** Blending Euler channels numerically from 170° to −170° spins 340° the wrong way. Blend as CFrames (`CFrame:Lerp`) or use the wrapped delta `(b - a + π) % 2π − π`.
- **Joint holes.** A joint missing from one key snaps to rest for that key in naive players, and in the engine an unkeyed joint lets lower-priority tracks or rest show through. Key every bone the clip owns on every key pose; fill holes at load.
- **Big turns.** Keep each key-to-key rotation under about 120° and never exactly 180° (direction becomes arbitrary); add a breakdown key on the far side of the arc.
- **Easing placement.** A pose's easing shapes the segment leaving it. Cubic ease-in on a short, large arc puts about 70% of the motion into the last two of six frames: add a mid key instead.
- **Dense baked clips** use Linear easing; thin per joint only with a tolerance (0.5–0.75° body joints) and re-check contacts.

## 4. Animation craft: the 12 principles and frame charts

Game rule first: the player's own action must show motion on the input frame; readability for other players comes from the pose, not from delay. Anticipation is spent on enemies (so players can react) and saved on the player (so input feels instant) `[lihfolk][house]`.

| Principle | In a short game loop |
|---|---|
| Squash and stretch | Rigid rigs cannot deform: compress the spine and knees into the hit, extend at contact; scale-pop props for 2–3 frames |
| Anticipation | Player light attack 2–5 f; enemy telegraph ≥ 0.45 s; hide wind-up N+1 inside follow-through N in combos |
| Staging | Weapon and limbs outside the body silhouette from the gameplay camera; one idea per pose |
| Straight ahead / pose to pose | Block key poses with Constant interpolation, then add breakdowns; straight-ahead only for cloth and tails |
| Follow-through and overlap | Hips lead chest by about 1 f, chest leads arm by about 2 f; head and off arm trail 1–2 f |
| Slow in / slow out | Ease out of the wind-up, arrive at contact at speed, decelerate after contact, hold |
| Arcs | A breakdown key keeps the blade on the arc; sparse keys cut the corner through the body |
| Secondary action | Breathing 1–3° on a 3–5 s cycle; spring bones for tails and ears; random phase per NPC so crowds do not pulse |
| Timing | Light vs heavy is frame count, not playback speed: author heavy creatures slow, never play below 1× |
| Exaggeration | Chunky avatars at phone distance need about 1.5× the pose you think |
| Solid drawing | Balance: centre of mass over the support foot; no twinning (mirror-identical arms) |
| Appeal | Distinct idle silhouette per character class; readable at 64 px tall |

Frame counts (30 fps; double for 60 fps authoring; clips store seconds, so playback is frame-rate independent):

| Clip | 30 fps | Seconds | Rules |
|---|---|---|---|
| Idle loop | 90–150 f | 3–5 | No dead hold over 9 f; end pose near every attack's start pose `[lihfolk]` |
| Walk (R15) | 12 f per step, 24 f cycle | 0.8 | Contact, down, passing, up with uneven spacing. Author at its real speed, about 5–6 studs/s: a walk cannot fill 16 studs/s without sliding `[lihfolk]` |
| Run (R15, 16 studs/s) | 8 f per step, 16 f cycle | 0.53 | Planted foot travels back `WalkSpeed / 30` studs per frame (0.533 at 16); lean the chest, pelvis pitch ≤ 8° `[lihfolk]` |
| Sprint (about 26 studs/s) | 6 f per step | 0.2 per step | Separate clip with a longer stride; do not over-speed the run `[lihfolk]` |
| Jump | Launch pose within 1–2 f; airborne 15–16 f; land absorb 3 f, hold 2 f, recover about 8–13 f | 0.51–0.54 in the air | The Humanoid leaves the ground on the input frame, so a crouch anticipation needs a delayed jump you script yourself. Air time derives from defaults (JumpPower 50 or JumpHeight 7.2, gravity 196.2) `[house]`. Split into Jump, Fall loop, Land; let movement cancel Land |
| Light attack | React 1 f, wind-up 2–5, strike 1–3, contact hold 2–3, follow-through 3–5, recovery 4–8 | Hit at 0.20–0.27, total 0.6–0.8 | Recovery cancellable from about 70% with a 0.1–0.2 s input buffer; PvP moves meant to be reacted to need ≥ 8 f startup (reaction time about 0.25 s) `[lihfolk]` |
| Heavy attack | Wind-up 6–16 (with a held coil), strike 2–4, contact 3–4, recovery 10–25 | Hit at 0.5–0.7, total 1.3–1.8 | Longer startup is acceptable because the player chose it `[lihfolk]` |
| Enemy attack | Telegraph ≥ 14 f, boss ≥ 15 f | ≥ 0.45 / 0.5 | `(Hit − Tele) / speed` checked for every attack in every phase `[lihfolk]` |
| Hit reaction | Snap to the flinch pose in 1–2 f, total 6–10 f | 0.2–0.33 | Directional variants (front, left, right, heavy); skip the flinch while a stun or knock-up owns the body `[lihfolk]` |
| Hit-stop (runtime, never baked) | None on light hits; medium to ultimate about 2–3 f | 0.05–0.09 | On confirmed hits only, on the attacker's client, never on the victim; values owned by `vfx-and-juice.md` §7 |

Locomotion without foot slide: store each gait's authored ground speed, play at `rate = horizontalSpeed / groundSpeed`, clamp to roughly 0.5–1.7, and switch gait when the clamp is hit; swap gaits at the same phase so legs do not scissor; fade gait-to-gait 0.15 s, into Jump and Land 0.08 s, into idle variants 0.4 s `[lihfolk]`. One-shot clips should end within a small angle of the pose that takes over: a finished one-shot holds its last pose and fades over about 0.3 s `[lihfolk]`.

## 5. Playback: priorities, blending, weights, speed

Rules `[official]` unless tagged:

- Priority order, high to low: Action4, Action3, Action2, Action, Movement, Idle, Core. Evaluation is **per joint**, from high to low priority, until the summed track weight for that joint reaches 1; tracks at the same priority blend in proportion to their weights (normalised when the sum exceeds 1).
- So an attack that keys only the upper body leaves the legs to the walk (the basis of upper-body layering), and two loops at the same priority average into a pose that matches neither.
- `Play(fadeTime = 0.1, weight = 1, speed = 1)`, `Stop(fadeTime = 0.1)`, `AdjustWeight(weight, fadeTime)`, `AdjustSpeed(speed)`: negative speed plays backwards, 0 pauses.
- `Length` is 0 until the asset loads; anything computed from it on the first frame is wrong. `TimePosition` can be set only while playing: `Play` first. `Looped` changes apply after the current loop. After `Stop`, `AdjustWeight` does nothing until `Play`.
- `Play` on a playing track restarts it at time 0 `[lihfolk]`: check `IsPlaying` or play only on state change.
- `Stopped` fires when playback ends, while the fade-out may still move the rig; `Ended` fires when the track no longer affects anything. Gameplay on `Stopped`, cleanup on `Ended`.
- `LoadAnimation` creates a new track on every call and requires the Animator under Workspace (a `WorldModel` for ViewportFrame rigs `[community]`). Load once and cache, or look up with `GetTrackByAnimationId`. Per-swing loading hits the engine's 256-tracks-per-Animator warning, after which new tracks do not play `[community]`. `Humanoid:LoadAnimation` and `AnimationController:LoadAnimation` are deprecated.
- A partial top layer with nothing below it blends toward the rest pose (a half T-pose) `[lihfolk]`: keep a full-weight base layer.

House priority convention (write yours down; the clash bugs come from having none):

| Layer | Priority | Fade in |
|---|---|---|
| Default `Animate` idle and gaits | Core / Idle / Movement (as authored by Roblox) | n/a |
| Custom locomotion | Movement | 0.15 |
| Carry or hold pose (weapon arm only) | Action | 0.2 |
| Equip, emote, interaction | Action2 | 0.1 |
| Attacks and abilities | Action3 | 0.05 |
| Hit reactions, stuns, cinematics | Action4 | 0.05 |

The default `Animate` script plays a tool-hold clip (`toolnone`) that sticks the right arm out whenever a `Tool` is equipped; replace its id or fade it out if your weapons hold differently `[lihfolk]`. Set replacement ids after `CharacterAppearanceLoaded` and stop the playing tracks so the new ids load `[official]`.

```lua
--!strict
-- unexecuted sketch (client): load once per Animator, preload, priority before Play, markers wired once.
local ContentProvider = game:GetService("ContentProvider")
export type ClipDef = { id: string, priority: Enum.AnimationPriority, fade: number }
export type ClipSet = { [string]: AnimationTrack }
local function loadSet(animator: Animator, defs: { [string]: ClipDef }, onMarker: (clip: string, marker: string) -> ()): ClipSet
	local set: ClipSet, assets: { Instance } = {}, {}
	for name, def in defs do
		local anim = Instance.new("Animation")
		anim.Name, anim.AnimationId = name, def.id
		local track = animator:LoadAnimation(anim) -- Animator must be a descendant of Workspace
		track.Priority = def.priority
		for _, marker in { "Hit", "TrailOn", "TrailOff", "Step" } do -- cosmetic sync only; damage is server-timed
			track:GetMarkerReachedSignal(marker):Connect(function() onMarker(name, marker) end)
		end
		set[name] = track
		table.insert(assets, anim)
	end
	task.spawn(ContentProvider.PreloadAsync, ContentProvider, assets) -- removes the first-use delay
	return set
end
```

Under server authority (`Workspace.AuthorityMode = Server`) the cache rule inverts `[official][VS]`: rollback can replace tracks, so store ids and query `Animator:GetTrackByAnimationId()` or `GetPlayingAnimationTracks()` each time, inside functions bound with `RunService:BindToSimulation` (see `networking-and-security.md`).

The Animation Graph Editor `[official][VS]` publishes blend trees and state machines as one asset; load it like a clip and drive it with `AnimationTrack:SetParameter("speed", v)`. It can replace hand-written gait blending; treat it as new and test it on the 3 GB phone before adopting.

## 6. Markers: syncing VFX, SFX and hitboxes

- Author markers in the Clip Editor's event track (name plus optional string parameter); listen with `track:GetMarkerReachedSignal(name)`, which passes the parameter `[official]`. `KeyframeReached` is the legacy mechanism.
- Vocabulary `[lihfolk]`: `Hit`, `Hit2`…; `TrailOn`/`TrailOff`; `Step`; `Tele` (enemy telegraph); `Cast`/`Release`; `CancelOpen`; camera beats `Open`/`Impact`. Keep names identical across clips; one typo is one silent weapon.
- A marker fires on the first animation step whose time span contains it, so up to one frame late, later on throttled rigs; several markers passed in one step all fire in order; setting `TimePosition` skips markers; markers do not fire until the asset has loaded `[lihfolk]`.
- Markers fire on each machine that plays or receives the track, on that machine's clock. A marker on a player's client is a claim, never proof (`networking-and-security.md`).
- **Server hit timing comes from data.** A build step copies marker times into the generated animation table; the server schedules the hit at `markerTime / speed` on its own clock, minus a small lead (0.06 s in the source project) so damage lands as the blade visibly connects, and validates range and cooldown. The server never needs to load the clip `[lihfolk]`. Regenerate the table whenever a clip is retimed.
- Client uses of markers: enable a `Trail` only between `TrailOn` and `TrailOff` (call `Trail:Clear()` first), play the impact sound with its peak on `Hit`, footsteps on `Step` keyed by `Humanoid.FloorMaterial`, camera kick on `Impact`. Skip cosmetic marker work for distant rigs.
- Hitboxes: open the query window between two marker times, cast with `workspace:GetPartBoundsInBox` or blade-sweep raycasts from attachments, client-predicted for feel and server-confirmed for damage. Do not parent hitboxes to client-animated NPC limbs and expect the server to see them (section 7).
- Speed changes move markers in real time; hit-stop delays every later marker by its duration. Duplicate firing appears when a full-body clip and its upper-body copy both play: listen on one `[lihfolk]`.

## 7. Replication and ownership

All replication of playing tracks goes through the `Animator` `[official]`:

| Rig | Played from | Who sees it |
|---|---|---|
| Your own character (Animator created by the server) | Your client | Everyone |
| Your own character | Server | Everyone, but it fights the owner's own tracks `[lihfolk]`: play from the owning client |
| Another player's character | Your client | Only you |
| NPC or prop (not in a player character) | Server | Everyone |
| NPC or prop | A client | Only that client |
| Any rig whose Animator was created on a client | Anywhere | Only that client |

- Replicated: which clip, play and stop with fades, weight, speed. Not replicated: `Transform` on any joint, anything written procedurally, IK targets set locally, marker events as such. Each client evaluates the clip itself, so remote viewers see it one latency later `[official][lihfolk]`.
- Procedural layers (head look, aim, IK) must run on every client from a replicated input (attribute or `UnreliableRemoteEvent`); do not write `C0` from the server `[official: AnimationConstraint migration notes]`.
- Network ownership does not widen the rule in practice: community reports say client-played tracks on a client-owned NPC do not replicate; only player characters replicate from the client `[community]`. The docs' `LoadAnimation` text mentions `SetNetworkOwner`; treat it as unreliable and test (section 13).
- Three architectures: **owner plays** (player characters; relay only the VFX id through a rate-limited remote, never per-frame CFrames); **server plays** (a handful of NPCs whose limbs must be right on the server; costs server CPU and bandwidth per track change); **server writes state, clients animate** (everything at scale; section 8).
- Synchronised world motion (a gate, a boss door): replicate one attribute with a server start time and let every client run the same deterministic tween.

## 8. NPC animation at scale

Cost model `[official]`: server-played NPC animation is simulated on the server and replicated ("unnecessary overhead"); the mitigation is to play NPC animations on the client, use `AnimationController` instead of `Humanoid` where possible, disable unused Humanoid states, pool NPC models, and spawn only near players. MicroProfiler labels: `stepAnimation`, `stepHumanoid`, `updateInvalidatedFastClusters` (over 4 ms means avatar or skinned-mesh churn).

State protocol `[lihfolk]`: the server AI writes `Anim` (clip name), `AnimSpeed`, then `AnimT` (server time of the start, written last) as attributes on the NPC model; clients react to `AnimT`. Hit reactions, layers and death fades get their own attributes. Damage timing comes from the generated marker table, so the server loads no clips and its hit tests are data-driven (distance, arc, time), not limb positions. Bind the client function below on a `CollectionService` tag-added signal and unbind on removal so streaming works.

```lua
--!strict
-- unexecuted sketch (client): play NPC clips locally from server-written attributes; late joiners land mid-clip.
local function bindNpc(model: Model, clips: { [string]: Animation })
	local controller = model:FindFirstChildOfClass("AnimationController")
	if not controller then return end
	local animator = controller:FindFirstChildOfClass("Animator") or Instance.new("Animator")
	animator.Parent = controller -- client-side play on a non-character rig never replicates: intended here
	local tracks: { [string]: AnimationTrack } = {}
	local current: AnimationTrack? = nil
	local function apply()
		local name = model:GetAttribute("Anim")
		local t0 = model:GetAttribute("AnimT")
		if typeof(name) ~= "string" or typeof(t0) ~= "number" or not clips[name] then return end
		local speedAttr = model:GetAttribute("AnimSpeed")
		local speed = if typeof(speedAttr) == "number" then speedAttr else 1
		local track = tracks[name] or animator:LoadAnimation(clips[name])
		tracks[name] = track
		if current and current ~= track then current:Stop(0.15) end
		current = track
		track:Play(0.15, 1, speed)
		local offset = (workspace:GetServerTimeNow() - t0) * speed
		if track.Length > 0 then -- Length is 0 until the asset loads
			track.TimePosition = if track.Looped then offset % track.Length else math.min(offset, track.Length)
		end
	end
	model:GetAttributeChangedSignal("AnimT"):Connect(apply)
	apply()
end
```

Engine throttling `[official][VS]`: `Workspace.ClientAnimatorThrottling` (Default / Disabled / Enabled) lets the client reduce evaluation of remotely simulated models by visibility, frame rate and animation count; `Animator.PreferLodEnabled` (default true) opts a rig in; `Animator.EvaluationThrottled` is true on a frame that reused the previous pose. Set `PreferLodEnabled = false` only on a boss or a cutscene actor.

Your own LOD (for anything you update in Luau: procedural layers, attribute-driven rigs, ambient props) `[lihfolk]`:

| Tier | Example range from camera | Update |
|---|---|---|
| Near, and always the local character, current target and bosses | ≤ 60 studs | Every frame, all layers |
| Mid | ≤ 150 | Every 2nd frame; drop IK and springs |
| Far | ≤ 300 | Every 4th frame; base clip only |
| Beyond or off-screen | > 300 | Time and gameplay events only, no pose writes |

The rule that prevents the worst bugs: **LOD may skip writing poses; it never skips time or events.** Accumulate skipped `dt`, re-tier on a staggered schedule (every 15 frames with a random phase per rig) with hysteresis, and tier by on-screen size (`radius / distance`) rather than raw distance when rig sizes vary.

Other levers: one shared skeleton per enemy family so 12–13 clips serve every member `[lihfolk]`; random idle phase; ambient shopkeepers sleep beyond about 280 studs `[lihfolk]`; no `Highlight` per NPC (limit 255, see `performance.md`); disable `CastShadow` on small rig parts.

## 9. Procedural animation

Frame order `[official]`: `PreRender` → `PreAnimation` (change tracks, weights, speeds here) → the Animator writes every keyed joint's `Transform` → `PreSimulation` (compose procedural offsets here) → transforms are applied in a batch before physics → `PostSimulation` / `Heartbeat` (read results). A `Transform` written in `PreRender` or `Heartbeat` is overwritten by the next animation step.

```lua
--!strict
-- unexecuted sketch (runs on every viewer's client): head look layered over whatever clip is playing.
local RunService = game:GetService("RunService")
local function findJoint(character: Model, childName: string): Instance?
	for _, d in character:GetDescendants() do
		if (d:IsA("AnimationConstraint") or d:IsA("Motor6D")) and (d :: any).Part1 and (d :: any).Part1.Name == childName then
			return d -- Part1 is a read-only alias on AnimationConstraint
		end
	end
	return nil
end
local function bindHeadLook(character: Model, animator: Animator, getYawPitch: () -> (number, number)): RBXScriptConnection?
	local neck = findJoint(character, "Head") :: any
	if not neck then return nil end
	local yaw, pitch = 0, 0
	return RunService.PreSimulation:Connect(function(dt: number)
		local targetYaw, targetPitch = getYawPitch() -- radians from a replicated attribute, clamped ±70° / ±40°
		local alpha = 1 - math.exp(-12 * dt) -- frame-rate independent smoothing
		yaw += (targetYaw - yaw) * alpha
		pitch += (targetPitch - pitch) * alpha
		if animator.EvaluationThrottled then return end -- stale pose this frame: an offset would compound
		neck.Transform = CFrame.fromEulerAnglesYXZ(pitch, yaw, 0) * neck.Transform
	end)
end
```

Multiplying onto `Transform` is safe only on joints a playing clip rewrites every frame; on an unkeyed joint keep your own base and assign `base * offset`, or the joint winds up `[lihfolk]`. Use `fromEulerAnglesYXZ`, not `CFrame.Angles`, to avoid head roll. Run all layers from one ordered dispatcher (look-at, then IK, then springs).

**IKControl** `[official]`: child of the `Humanoid` or `AnimationController` that has an Animator; required `Type` (Transform, Position, Rotation, LookAt), `ChainRoot`, `EndEffector`, `Target`. It overrides the clip on the chain between root and effector. `Weight` 0–1 blends, but weight 0 does not disable it: set `Enabled = false`. `SmoothTime` defaults to 0.05 s (critically damped), `Pole` steers the elbow or knee, higher `Priority` solves later. Never set `ChainRoot` to the character's root. `GetChainCount() > 0` confirms a valid chain. Fade `Weight` instead of toggling `Enabled` to avoid pops. An IKControl created in a LocalScript does not replicate `[community]`: create it on every client from replicated state.

| Technique | Recipe | Cost and limits |
|---|---|---|
| Look-at | `IKControl` LookAt on the head with `ChainRoot = UpperTorso`, or the `Transform` layer above; lose interest when the target passes behind, with hysteresis | Cheap; run for near rigs only |
| Hand on prop | `IKControl` Transform, `EndEffector = LeftHand`, `Target` = a `Grip_Att` attachment authored in Blender, `SmoothTime = 0` for contact | One clip serves every weapon |
| Foot planting | Per foot: weight by animated foot height (fade out as the clip lifts the foot 0.15–0.6 studs), raycast down from above the sole excluding the character, move an `IKControl` Position target to the hit, tilt up to 25–35°, lower the pelvis by the lowest foot's deficit with smoothing; off in the air `[lihfolk][community]` | Two raycasts per rig per frame: local character and nearest few only; never on the server |
| Springs | Tails, ears, trinkets, weapon sway: critically damped spring per joint; clamp `dt` (≤ 1/30) or use the exact solution so a lag spike cannot explode it; guard NaN `[lihfolk]` | Small CPU per joint; first layer to drop in LOD |
| Smoothing | `1 - exp(-k * dt)`, never a constant lerp per frame (frame-rate dependent) | Free |
| Ragdoll / physical joints | AnimationConstraint `IsKinematic = false` with `MaxForce`/`MaxTorque`, or BallSocket limits; `Humanoid.RequiresNeck = false` and `BreakJointsOnDeath = false` first `[official][lihfolk]` | Owner simulates; see `physics-and-vehicles.md` |

Known issue `[community][VS]`: with `UseFixedSimulation` (required for server authority) a forum bug report says `Transform` writes are ignored while a track plays; the poster's workaround is writing in `PreAnimation`. Test procedural layers under that setting before relying on them.

## 10. Tools and weapons, cutscenes, props, UI-in-world

**Tools and weapons.** Author the weapon in Blender with a `Grip_Att` empty; hold it with a Motor6D (hand to handle) rather than the default tool weld when clips must move it; held weapon parts are `Massless` with `CanCollide`/`CanTouch` off so they cannot shove the wielder, and gameplay uses an invisible hitbox proxy `[lihfolk]` (house rule 2: see section 13). Put the hold tilt in `C0` once and never change it per state; exactly one controller writes the grip joint; lock procedural sway on the grip from attack accept to recovery end, or the blade twists inside the hand `[lihfolk]`. Moving weapon pieces (bow limbs, a flail) are a small part rig with their own clips on the same Animator, named so poses bind. Preload a kit's clips on equip (first use can otherwise start seconds late). Scale movement speed to 0.55–0.9 during swings to stop sliding `[lihfolk]`. First-person arms are a local-only viewmodel under the camera, bound after camera priority, with every part non-colliding and non-queryable (same house-rule note).

**Cutscenes.** Client-local, skippable after about 2 s, never freezing other players. Actors are local clones (client Animator, no replication) with `PreferLodEnabled = false`. Blender cameras do not import: animate a `Cam` bone or part in the actor rig, export it with the clip, and in a `BindToRenderStep` callback after `Enum.RenderPriority.Camera` copy its CFrame to a `Scriptable` camera `[community]`; drive FOV from marker parameters. The system is the restore path `[lihfolk]`: lock input and other controllers, hide and remember every ScreenGui, shoot, then restore camera type, FOV, HUD and control on **every** exit, including death, respawn, script error and a watchdog timeout. Offer a reduced-motion variant (`GuiService.ReducedMotionEnabled`).

**Non-character props.**

| Motion | Tool |
|---|---|
| One-shot (door, chest lid, lever) | `TweenService` on the client, tweening `CFrame` (never `Position` on welded models); server sets state and time |
| Endless (spin, bob, sway) | One client loop computing a formula of time, `workspace:BulkMoveTo` for many parts, 30 Hz, range-gated |
| Authored mechanical motion (crane, trap, creature-like prop) | Blender part rig with Motor6Ds, `AnimationController`, published clip |
| Platforms players ride | Physics constraints or matching velocity; characters ride velocity, not teleported CFrames (`physics-and-vehicles.md`) |

Solid props that animate (house rule 2): the server owns collision truth. It moves or toggles the invisible `_COL` proxy at the state change; clients animate only the visual mesh. A door tweened on clients with its collision still closed on the server is a bug in both directions. Parts moved by a client-only Animator stay at rest on the server, so server raycasts see the rest pose.

**UI-in-world** (BillboardGui, SurfaceGui on Blender signage): tween `UIScale` from a centred `AnchorPoint` for pops, `CanvasGroup.GroupTransparency` for fades, pooled BillboardGuis for damage numbers, `MaxDistance` set, loops stopped while hidden or off-screen. See `ui-input-crossplatform.md` and `vfx-and-juice.md`.

## 11. Performance budgets

| Budget | Value | Tag |
|---|---|---|
| Triangles per NPC | 4,000–10,000 (`art-pipeline-blender.md`); crowd NPC at the low end | `[house]` |
| Deform bones | 25 crowd / 40 enemy / 60 boss | `[house][lihfolk]` |
| Tracks loaded per Animator | Hard stop 256; house ≤ 40 | `[community]` / `[house]` |
| Tracks playing per rig | ≤ 4 layers; stop unused layers rather than parking them at weight 0 | `[house][lihfolk]` |
| Key density after thinning | About 15–30 keys/s for body clips, 5–8 keys/s for weapon hinges | `[lihfolk]` |
| Clip sources in the shipped place | 0 `KeyframeSequence` instances; a 2 s clip keyed on every joint at 20 fps is about 640 instances and every client downloads ReplicatedStorage | `[lihfolk]`; removal advised `[official]` |
| Fully animated rigs in view, 3 GB phone | Start at 15 near plus LOD tiers; tune from `stepAnimation` in the MicroProfiler | `[house]` |
| Foot IK, springs, look-at | Local character plus at most 5 nearest rigs; every equipped kit's clips preloaded (no first-use delay) | `[house]` |
| `updateInvalidatedFastClusters` | Under 4 ms | `[official]` |

## 12. Level-up: symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Works in Studio, nothing plays live for anyone | Temporary registered id, or clip owned by another creator | Publish under the game's owner or grant the experience permission; grep for `RegisterKeyframeSequence` / `RegisterAnimationClip` |
| I see my NPC's animation, others do not | Played from a client, or the Animator was created on a client | Play on the server, or drive every client from attributes (section 8) |
| Server-played character clip jitters for its owner | Owner's client also plays tracks | Play character clips from the owning client |
| Late joiner sees T-posed or restarting NPCs | State sent as a one-off event | Attributes plus server start time; seek by `GetServerTimeNow() - AnimT` |
| Attack plays, legs keep running | Attack clip does not key the legs (per-joint priority) | Intended for upper-body moves; key the legs for full-body ones |
| Pose is a mush of two clips | Same priority, weights averaged | Distinct priorities, or crossfade so weights sum to 1 |
| Walk overrides the attack | Attack published at Core/Idle/Movement, or priority set after `Play` | Set `track.Priority` before `Play`; follow the convention table |
| Right arm sticks out when holding a Tool | Default `Animate` tool-hold clip | Replace its id or fade it out |
| First use seconds late | Asset fetched on first play | `ContentProvider:PreloadAsync` on equip; load tracks early |
| Clip frozen at frame 0 | `Play` called every frame, or speed computed from `Length == 0` | Play on state change only; wait for `Length > 0` |
| Animations stop playing after long sessions | 256-track limit from `LoadAnimation` per use | Cache tracks; `Destroy` tracks you will not reuse |
| Limb spins the long way or flips | Key-to-key turn over about 120°, exact 180°, or Euler wrap in generated data | Breakdown key; blend as CFrames |
| One-key hitch to the rest pose; easing feels backwards | Joint hole (joint missing from a key); legacy `Cubic` or easing set on the arriving key | Key all owned bones on key poses; `CubicV2`, easing on the key that starts the segment |
| Character does not travel or lift, or plays turned 180° after a GLB import | Motion or the importer's axis correction sits on the unapplied top-level root pose `[lihfolk]` | Key the root's first child; calibration clip once per export route |
| Root motion snaps back at clip end | Roblox has no engine root motion: the clip moved the body, not the `HumanoidRootPart` `[community]` | Animate in place and move the root in code from a travel curve, between `MoveStart`/`MoveEnd` markers |
| Shoulders crumple or vertices spike to the origin in Roblox, fine in Blender | More than 4 influences, unnormalised or missing weights | Limit Total 4, Normalize All, run the rig validator, re-export |
| Feet slide | Playback rate not matched to ground speed, or a walk clip at run speed | `rate = speed / groundSpeed`; author a gait for the common speed |
| Feet hover or sink on scaled characters | Clip translations do not follow Humanoid body scale; `Model:ScaleTo` multiplies them `[lihfolk]` | Author translations for the scale method in use; test at real size; check `Workspace.Retargeting` |
| Procedural offset does nothing | Written in `PreRender`/`Heartbeat`, or joints looked up as Motor6D on an upgraded avatar | Write in `PreSimulation`; accept `AnimationConstraint` |
| Procedural joint slowly spins away | Compounding on a throttled or unkeyed joint | Check `EvaluationThrottled`; assign from your own base |
| IKControl does nothing / still acts at weight 0 | Missing required property or wrong parent; weight 0 is not off | Check `GetChainCount()`; `Enabled = false` |
| Swipes pass through players on a skinned boss | MeshPart collides in its rest shape | Hitbox parts on bones or data-driven hits |
| Far enemies hit without swinging, or never finish attacks | LOD skipped time and events | Advance time and gameplay events always; skip only pose writes |
| Blade twists in the hand during swings | Two writers on the grip joint | One grip controller; lock sway during attacks |
| HUD missing or camera stuck after a cutscene | No restore on an error or death path | Restore on every exit plus a watchdog |
| Long joins, `stepAnimation` fine | Hundreds of thousands of Pose instances replicated | Publish clips, delete sources and importer saves |
| Server heartbeat drops with many NPCs | Server-side animation and full Humanoids | Client animation, `AnimationController`, fewer Humanoid states, pooling |

Debug order for anything else: print the track's id and `Length`; dump `Animator:GetPlayingAnimationTracks()` (name, priority, weight, speed) at the moment of the bug; solo the clip; try it on a known-good rig; compare owner, second client and server.

## 13. Conflicts and open questions

- House rule 2 and held items: a colliding held weapon or first-person viewmodel destabilises its own wielder, so this file treats items welded or jointed to a character as covered by the character's collider plus a hitbox proxy, and requires the normal `_COL` proxy the moment the item is dropped or placed in the world. SKILL.md states this resolution explicitly (held tools, weapons and viewmodels do not collide; skinned meshes need a `_COL` proxy).
- Conflict: `performance.md` and knowledge-base 5.9 say Blender animation goes through FBX, one track per file, matching the modeling specification `[official]`. LihFolk measured GLB exports with every Action importing as separate clips, and a 2026 Clip Editor importer beta reportedly added glTF and track selection `[community]`. Trust the docs as the default route; treat multi-clip GLB as valid only after a test import on the pinned Studio version.
- Conflict: "create the Animator on the server" (Animator reference) versus "create the Animator on the client" (performance docs). Both hold: a server-created Animator is required for replication; a client-created one is the documented way to keep NPC animation local.
- Conflict: "cache tracks" (Animator reference, community 256 limit) versus "do not cache tracks" (server authority techniques). Cache everywhere except inside server-authority simulation code.
- Conflict: LihFolk's interpolation model (rotation-vector blending between unevenly spaced keys, 0.3 s end fade, unapplied top-level pose) is measured, not documented. Adopted only as authoring guards (turn limits, end poses near idle, root motion on the first child).
- Open `[VS]`: Avatar Joint Upgrade phase timing (a forum post lists the breaking default for H2 2026); whether client-played tracks on client-owned non-character models replicate; marker timing on throttled remote rigs; the 256-track limit (engine warning text, not in the reference).

## Review gate

- [ ] Every rig, weapon and animated prop came from Blender; the only non-authored visible model is the player avatar.
- [ ] Rig validator passes: one root at origin with no weights, ≤ 4 influences, no unweighted vertices, frozen transforms, stable names, bone budget met.
- [ ] Every animated solid has server-side collision truth: root collider, `_COL` hitboxes on bones where needed, proxies moved by the server for doors and platforms.
- [ ] Every clip is published under the game's owner (or permission granted); no temporary ids; no clip sources or importer saves in the shipped place.
- [ ] One generated animation table holds ids, lengths, ground speeds and marker times; the server times hits from it.
- [ ] A written priority convention exists; `Priority` is set before `Play`; tracks are loaded once and preloaded on equip.
- [ ] Player actions move on the input frame; enemy telegraphs ≥ 0.45 s; hit-stop is runtime and client-side; cutscenes restore camera, HUD and input on every exit path and honour reduced motion.
- [ ] NPC animation runs on clients from attributes with server start times; a late-join test passes.
- [ ] Procedural layers write in `PreSimulation`, accept `AnimationConstraint`, check `EvaluationThrottled`, and run on every viewer.
- [ ] LOD skips pose writes only; far and off-screen rigs still advance time and gameplay events.
- [ ] Tested in a published place with two clients and on a 3 GB Android phone; `stepAnimation` and `updateInvalidatedFastClusters` within budget.

## Sources

Accessed 2026-11-10.

- Roblox/creator-docs (https://github.com/Roblox/creator-docs), `content/en-us/` (read): `animation/index.md`, `animation/using.md`, `animation/editor.md`, `animation/events.md`, `animation/curve-editor.md`, `animation/inverse-kinematics.md`, `animation/graph-editor.md`, `animation/capture.md`; `characters/index.md`, `characters/adaptive-animation.md`; `art/modeling/rigging.md`, `art/modeling/specifications.md`, `art/modeling/export-requirements.md`, `art/blender.md`, `art/characters/export-avatar-animations-from-maya.md`; `avatar/character-bodies/specifications.md`, `avatar/emotes/import.md`, `avatar/emotes/specifications.md`, `avatar/resources.md`; `studio/importer.md`; `performance-optimization/improve.md`; `projects/assets/privacy.md`; `projects/server-authority/index.md`, `projects/server-authority/techniques.md`; `cloud/guides/usage-assets.md`; `reference/engine/classes/` Animator, AnimationTrack, AnimationController, AnimationConstraint, Motor6D, Bone, IKControl, KeyframeSequence, CurveAnimation, AnimationClipProvider, KeyframeSequenceProvider, Humanoid, RunService, StarterPlayer, Workspace, RigidConstraint; `reference/engine/enums/` AnimationPriority, PoseEasingStyle, IKControlType, ClientAnimatorThrottlingMode, AnimatorRetargetingMode, AvatarUnificationMode, RestPose.
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `08 Animation/07 Gotchas/{Engine Gotchas, Troubleshooting Table, Animation LOD, Performance and Memory}`, `08 Animation/02 Rigging and Importing/{Animation Data from Blender to Roblox, Exporting FBX vs GLB, Rigging in Blender, Weight Painting and Skinning for Roblox}`, `08 Animation/01 Fundamentals/{Replication and Ownership, Markers and Events, Bones and Skinned Meshes, Frame Order and RunService Timing}`, `08 Animation/03 Authoring/{Locomotion and Melee Reference Numbers, Combat Animation Craft, Timing Spacing and Frame Charts, Principles of Animation for Games, Idle Breathing and Secondary Motion}`, `08 Animation/04 Procedural/{IKControl Reference, Foot Placement and Ground IK, Tween and CFrame Animation of Objects}`, `08 Animation/05 Systems/{Locomotion Systems, Enemy and NPC Animation, Cameras and Cutscenes, UI and GUI Animation}`, `56 Field Notes/{Animation Data Hygiene - Euler Wrap Joint Holes and Easing, Held Weapons on Motor6D - Locking the Grip During Attacks}`, `62 Engine Reference Cards/Animator - Engine Reference Card` (read); TL;DR blocks of the remaining `08 Animation` notes (read).
- DevForum threads (search summary; direct fetch blocked): https://devforum.roblox.com/t/avatar-joint-upgrade-for-physically-simulated-character-movement-is-now-live/4298561, https://devforum.roblox.com/t/studio-beta-avatar-joint-upgrade-enabling-physically-simulated-characters/3266099; https://devforum.roblox.com/t/r6-to-r15-adapter-beta-enable-r15-tech-in-r6-experiences/2557840; https://devforum.roblox.com/t/studio-beta-animation-clip-editor-improved-importing-and-gltf-support/4260501; https://devforum.roblox.com/t/blender-rig-exporteranimation-importer/34729; https://devforum.roblox.com/t/animation-on-non-character-with-network-ownership-not-replicating/1838969, https://devforum.roblox.com/t/animator-not-replicating/1265879; https://devforum.roblox.com/t/how-do-i-fix-animationtrack-limit-of-256-tracks-for-one-animator-exceeded-new-animations-will-not-be-played/3064455; https://devforum.roblox.com/t/setting-the-priority-to-action-isnt-stopping-my-animation-from-blending/3067476; https://devforum.roblox.com/t/how-can-i-let-the-server-know-to-enable-and-disable-hitboxes-from-an-animation-safely/3843585, https://devforum.roblox.com/t/better-way-to-do-hitbox-validation/3520770; https://devforum.roblox.com/t/help-with-root-motion-animating-the-humanoidrootpart/1556616; https://devforum.roblox.com/t/procedural-foot-planting-with-ikcontrols/2190661, https://devforum.roblox.com/t/inverse-kinematics-control-instance-for-animation-is-now-in-beta/1999010; https://devforum.roblox.com/t/motor6danimation-constraint-transform-property-unable-to-be-changed-server-authority/4846108; https://devforum.roblox.com/t/skinned-meshparts-are-live/831011, https://devforum.roblox.com/t/fully-custom-mesh-deform-character-setup-skinned-meshes/1193941; https://devforum.roblox.com/t/blender-roblox-camera-cutscene/2847027, https://devforum.roblox.com/t/blender-to-roblox-camera-cutscene-addon/3648766; https://devforum.roblox.com/t/sharing-animation-assets-with-connections-and-groups/3892540; https://devforum.roblox.com/t/how-do-i-handle-animations-for-a-large-number-of-npcs/142944, https://devforum.roblox.com/t/game-with-skinned-meshes-has-poor-performance-on-mobile-renderfidelity-doing-nothing/2649641
- https://nilo.io/articles/export-blender-animation-roblox-studio (search summary; third-party vendor article reporting the August 2026 clip importer options, unconfirmed)
