# Animation and rigs: Blender to Roblox

What this is: the rigging and animation reference for a game whose models all come from Blender (house rule 1): rig choice, Blender rig rules, the clip pipeline, timing charts, playback, markers, replication, NPC scale, procedural layers, bugs and budgets. Open it before the first rig is built, when a clip looks or replicates wrong, or when auditing a live game's `stepAnimation` cost. It extends `references/art-pipeline-blender.md` (static meshes, export scripts, upload) and does not repeat it. Viewed examples, breakdowns, rigs and tools: `references/visual-library/animation.md`.

Tags: `[official]` Roblox docs, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (measured in one live action game, October 2026, not Roblox-documented), `[house]` house estimate, `[VS]` version-sensitive: re-check at create.roblox.com/docs.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Keep players on their R15 avatar and the default `Animate` script; swap clip ids only. 2. Author one clip in Blender on a downloaded R15 rig, export FBX, import in the Clip Editor, publish under the creator that owns the game. 3. Load each clip once with `Animator:LoadAnimation`, set `Priority` before `Play`. 4. Put a `Hit` or `Step` marker in the clip and hang sound and particles on it. 5. Move doors and chests with a client-side tween. 6. Make one attack, one hit reaction and a walk from the section 4 recipes and score them with its rubric | Skinned custom rigs, IK, custom locomotion controllers, clip thinning, retargeting |
| Intermediate | One written priority convention; upper-body layering; marker times exported to a data table the server reads; clips preloaded on equip; playback rate matched to ground speed; frame charts (section 4) for every attack; NPCs animated per client from attributes | Lua keyframe players, physical joints, graph editor |
| Expert | Animation LOD that never skips time or events; shared skeleton families and retargeting; procedural layers in `PreSimulation` guarded by `EvaluationThrottled`; `AnimationConstraint` physical simulation; server-authority animation rules; key thinning and instance budgets; the interpolation caveats in section 3 | Nothing: measure with the MicroProfiler |

Terms: a **rig** is parts or mesh vertices joined by animatable joints. A **clip** is one animation asset. A **track** (`AnimationTrack`) is one clip loaded on one `Animator`. A **pose** is one joint's offset from its rest position at one keyframe. The **Clip Editor** is Studio's Animation Editor (Avatar tab), called the Animation Clip Editor in Roblox announcements.

## Contents

1 Rig types · 2 Blender rig requirements · 3 Blender to Roblox clip pipeline · 4 Craft: rules, recipes (attack, hit reaction, locomotion), posing checks, stiff tells, rubric · 5 Playback: priorities, blending, weights, speed · 6 Markers · 7 Replication and ownership · 8 NPC animation at scale · 9 Procedural animation · 10 Tools and weapons, cutscenes, props · 11 Performance budgets · 12 Level-up table · 13 Conflicts and open questions · Review gate · Sources

## 1. Rig types and when to use each

Three joint classes are animated by the engine `[official]`:

| Joint | Moves | Notes |
|---|---|---|
| `Motor6D` | A rigid part relative to its parent part: `Part0.CFrame * C0 * Transform = Part1.CFrame * C1` | The Animator writes `Transform` each frame. Animate through `Transform`, never by editing `C0`/`C1` per frame |
| `AnimationConstraint` | Same, through two Attachments; can also run force-limited (`IsKinematic = false`) for ragdolls and arm strength | Replaces Motor6D in R15 player characters under `StarterPlayer.AvatarJointUpgrade`: live since January 2026, `Default` means on since Phase 2 (May 2026), and the opt-out is due to be removed (targeted for the end of 2026) `[official][VS]`. `IsA("Motor6D")` is false; `C0`, `C1`, `Part0`, `Part1` are read-only aliases and writing them errors. Never move `RigAttachment.CFrame`: retargeting depends on it |
| `Bone` | Vertices of a skinned MeshPart; a Bone is also an Attachment | `Bone.WorldCFrame` is the rest pose; read `TransformedWorldCFrame` for the animated position |

Clips bind by name: a pose named `RightUpperArm` drives the joint whose child part (or Bone) has that name. Keys for names the rig lacks are ignored without a warning `[lihfolk]`, which is why one clip set can drive a family of rigs and why a renamed part silently stops moving.

| Rig | What it is | Use for | Avoid when |
|---|---|---|---|
| R15 (standard) | 15 MeshParts, fixed names, `Root > HumanoidRootNode > LowerTorso > UpperTorso > Head / arms / legs` `[official]` | Player avatars; humanoid NPCs that should reuse avatar clips, emotes, accessories and layered clothing | You need a non-human silhouette |
| R15 (advanced) | Same plus up to 37 optional joints: 15 per hand, Spine, Chest, two clavicles, HeadBase, `LeftToeBase`/`RightToeBase` (2026 names; Pelvis and Toes were renamed) `[official][VS]` | Hero NPCs and avatars needing hands and shoulders | Crowd NPCs on a 3 GB phone |
| R6 | 6 parts, legacy | Only when the game's identity is R6. `Workspace.AvatarUnificationMode` (the R6-to-R15 adapter) is marked deprecated with "R6 avatars always load as R6 rigs" `[official][VS]` | New games: no layered clothing, no dynamic heads, no IK-ready limbs, a separate clip library |
| Custom part rig | Separate Blender meshes joined by Motor6Ds | Hard-surface creatures, robots, weapons, doors, vehicles' moving parts. Default for anything rigid `[lihfolk]` | Organic bending is the point |
| Skinned (bone) rig | One mesh, armature, weights | Organic creatures, tails, wings, cloth, faces | Limbs must collide or be raycast (see below) |
| Hybrid | Skinned body, rigid props on `RigidConstraint` to a socket Bone `[official: RigidConstraint accepts Bones]` | Most finished characters | n/a |

Decision rules:

- Controller: `Humanoid` plus `Animator` only when the character needs Humanoid movement, states, accessories or `MoveTo`. Otherwise `AnimationController` plus `Animator`; static NPCs "have no need for the Humanoid class" `[official: performance docs]`. Exception: a moving model of skinned MeshParts without a Humanoid rebuilds FastClusters on every move, and embedding a Humanoid is the documented workaround `[official]`.
- Part or skin: part rigs are debuggable in Studio, every piece can collide and take attachments, and a mesh swap needs no re-weighting. Skinned rigs look continuous but only the single MeshPart collides, in its rest shape `[official: bones "don't change the physical shape"]`.
- House rule 2 (everything solid) on rigs: give every character one invisible root collider and, where gameplay needs limb hits, small `_COL` hitbox parts on `RigidConstraint`s to bones or welded to rig parts; set the visual limbs `CanCollide = false`. Never rely on the skinned mesh's own collision for an animated limb.
- Custom humanoid skeletons that should play R15 clips, or whose clips should play on avatars: run the Adaptive Animation tool (Avatar tab) to generate a `HumanoidRigDescription`, plus a `DigitsRigDescription` per hand. Generally available since April 2026; the importer's "Custom Humanoid" rig type was removed in its favour. `Workspace.Retargeting` (`AnimatorRetargetingMode`) controls whether clips adapt to body proportions `[official][VS]`.
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
| When | Roblox's documented rig and clip path; avatar bodies, heads, emotes `[official]` | Part rigs and creatures with several Actions; no unit dance `[lihfolk]`; accepted by the Clip Editor importer since 2026 `[official][VS]` |
| Scale (fix a 100× error here, never by scaling the import in Studio: parts scale but clip translations keep the old units `[lihfolk]`) | Apply Scalings = FBX Unit Scale, every other scale 1.0 `[official]` | None needed; importer Scale Unit = Stud `[official]` |
| Axes | Forward = Z Forward, Up = Y Up; importer World Forward = Front, World Up = Top `[official]` | +Y Up on |
| Leaf bones | Add Leaf Bones off `[official]` | Not applicable |
| Deform only | Only Deform Bones on | Export Deformation Bones Only on |
| Baking | Bake Animation on for clips, off for static meshes `[official]`; Simplify 0; Key All Bones on `[lihfolk]` | Always Sample Animations on, step 1; Optimize Animation Size off `[lihfolk]` |
| Clips per file | One take per file is the documented avatar-asset route; the 2026 importer also reads several clips from one FBX `[official][VS]` | Animation mode Actions; Reset Pose Bones Between Actions on `[lihfolk]`; each Action imports as its own clip `[official][VS]` |
| Textures | Path Mode Copy with Embed Textures `[official]` | Packed |
| Before export | Clear the active Action and reset the pose, or the rest pose becomes a frame of that clip `[lihfolk]` | Same |

## 3. Blender to Roblox clip pipeline

1. **Rig in Blender.** For player clips download a standard R15 rig from the avatar resources page (or export a dummy from Studio); for NPCs and props Blender is the source of truth.
2. **Author.** One Action per clip, named as the game references it (`Idle`, `Walk`, `Attack1`), fake user on. Mark gameplay beats with Action pose markers. Check key poses from the gameplay camera angle, not the side view.
3. **Bake and export** with the table above. For a layered (partial) clip export only the bones it owns: sampled glTF keys every bone, and a still key at high priority pins the whole body `[lihfolk]`.
4. **Import.** Clip Editor (Avatar tab) > ⋯ > Import > From File on the matching rig in Studio `[official]`. The importer released on 31 March 2026 shares the 3D Importer code path, reads FBX and glTF, imports every clip in the file, saves each to `ServerStorage/RBX_ANIMSAVES` under its clip name (Load swaps between them) and asks whether to keep the file's or the rig's rest pose; reimport is not yet supported `[official][VS]`. Or import model and clips together with the 3D Importer (Rig Type R15 / Custom / No Rig).
5. **Finish in the Clip Editor.** Set looping and priority, add event markers (Blender markers do not arrive), rename the final keyframe `End` only for clips that replace default character animations `[official]`. Optimize Keyframes (⋯ menu) thins keys with a preview slider `[official]`.
6. **Publish** to Roblox with Creator = the user or group that owns the game `[official]`. Automation: the Open Cloud Assets API accepts asset type Animation as `.rbxm`/`.rbxmx` (`model/x-rbxm`) `[official][VS]`. Today a new version published to an animation id updates every game that references it. Announced timeline (earliest dates) `[official][VS]`: from December 2026 an id can pin a version (`rbxassetid://id&version=n`); from 31 March 2027 an unpinned animation id keeps loading the version current on that date, so later versions reach a game only through a pinned id or `AssetService:GetLatestVersionUriAsync()`.
7. **Record** id, length, loop flag, ground speed and marker times in one generated module (`Shared/Config/Animations.luau`). Never hand-type ids in scripts.
8. **Verify** with a calibration clip (right arm +90° forward, torso +30° yaw left) once per export route `[lihfolk]`, then in a published test place with two clients. Studio alone proves nothing: temporary ids from `AnimationClipProvider:RegisterAnimationClip` and `KeyframeSequenceProvider:RegisterKeyframeSequence` "cannot be used outside of Studio" `[official]`.
9. **Strip.** Delete saved `KeyframeSequence`/`CurveAnimation` sources (`ServerStorage/RBX_ANIMSAVES`, each rig's `AnimSaves`) from the shipped place; a published clip costs no instances.

Third-party routes `[community]`: the long-running Blender rig exporter/animation importer (Den_S, 2017) targets Blender 2.80–2.93, ships as a pasted script with no licence text and does not support skinned meshes. Its maintained fork (Cautioned's Blender Animations plugin, GPL-3.0 tool, Blender 4.2 or later recommended) adds live sync to Studio, and the popular free R15 and R6 IK rigs export through it. Moon Animator 2 and newer plugins animate inside Studio. The route above needs none of them, so it has no plugin to break; if you adopt one, pin its version. Studio's prompt-to-animation beta (November 2026) is for blocking and timing tests only: shipped clips are authored `[house]`.

Ownership `[official][VS]`: animations are not covered by the Asset Privacy default switch; a clip loads only for its owner's experiences or where the owner granted the collaborator and the experience permission on the asset's Permissions page. Game grants cannot be revoked. Upload a clip to a personal account and a group game cannot play it until it is shared or re-uploaded.

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

## 4. Animation craft: rules, recipes, checks, rubric

Frame numbers are at 30 fps (the editor grid; clips store seconds, so playback is frame-rate independent). Viewed references for every rule are in `visual-library/animation.md`; the 12 principles one by one, with game examples, are its rows 1, 2, 16 and 18.

**Five rules for short game clips.**
- **Input frame.** The player's own action shows motion on the frame of the press. Anticipation is spent on enemies (so players can react) and rationed on the player `[lihfolk][house]`; input budgets are in `game-craft.md` §1.2.
- **Weight lives in the follow-through.** A player attack is fast in, slow out: the settle after contact sells the mass, and a marked cancel frame lets it play in full only when no new input arrives `[community: Cooper, Game Anim]`.
- **Favour the keys.** With few frames, an in-between sits next to a key pose, not halfway. Add frames before or after a key, never between two keys `[community: Skullgirls GDC talk; Dead Cells]`.
- **One frame of overshoot.** Go one frame past the final pose, then come back: impact at no cost in length `[community: Skullgirls GDC talk]`.
- **Motion between poses is an effect.** A rigid rig cannot smear or squash. Carry the strike with a `Trail` between `TrailOn` and `TrailOff` or a Blender slash mesh shown for 2–3 f; "squash" by compressing spine and knees, "stretch" by extending limbs `[community: Dead Cells; Cooper]`.

**Workflow for any clip** `[community: Bavelly spotlight; Skullgirls talk]`. (1) Reference: film yourself or find footage from side and front, step through it, note the frame of every pose change. (2) Block the key poses with Constant interpolation and judge them as a slideshow from the gameplay camera. (3) Break down in halves, then quarters, then eighths, adding the arc and the lead-and-drag. (4) Offset parts: hips lead chest by 1 f, chest leads arm by 2 f, head and off arm trail 1–2 f `[lihfolk]`. (5) Put the rough clip in the game on the real rig at phone distance before polishing. (6) Polish, add markers, score it with the rubric below.

### Recipe: light attack (22 f, 0.73 s)

| Frames | Pose | Rule |
|---|---|---|
| 0 | Idle, or the last pose of the previous attack | Chest or weapon already moves on f1 |
| 1–4 | Anticipation: coil away from the target, weight on the back foot, weapon clear of the body outline | 2–6 f. In combos, hide wind-up N+1 inside follow-through N `[lihfolk]` |
| 5–6 | Strike: hips, then chest, then arm; the weapon covers most of its arc here | 1–3 f; `TrailOn` at 5. Add a breakdown key so the blade stays on the arc |
| 7 | Contact with one frame of overshoot, arm at full extension | `Hit` marker at 0.20–0.27 s |
| 8–9 | Hold the contact pose | 2–3 f; `TrailOff` |
| 10–14 | Follow-through: weapon carries on, body settles, head arrives last | Slow out |
| 15–22 | Recovery to a pose within a small angle of idle | `CancelOpen` marker (next combo hit may start) at about 70% of the clip `[lihfolk]`. The press it accepts is buffered 0.15–0.20 s, never above 0.30 s; that window and the dodge-cancel lock are owned by `game-craft.md` §1.2 |

Variants `[lihfolk]`: **heavy** = wind-up 6–15 f with a held coil, strike 2–4, contact hold 3–4, recovery 10–20 (hit at about 0.4–0.7 s, total about 0.7–1.5 s; the player chose the delay); weight is frame count, so author heavy moves and creatures slow and never play a clip below 1×. **Enemy** = telegraph at least 14 f (0.45 s), boss 15 f (0.5 s), checked as `(Hit − Tele) / speed` for every attack in every phase. PvP moves meant to be reacted to need at least 8 f of startup (reaction time is about 0.25 s). Think in three columns for every move: startup, active, recovery `[community: fighting-game frame data]`. Hit-stop is runtime and never baked (`vfx-and-juice.md` §7).

### Recipe: hit reaction (6–10 f, 0.2–0.33 s)

- f0–1: snap to the flinch extreme with no ease in: chest and head thrown away from the hit by 15–30° `[house]`, hips lagging.
- f2–3: hold, with the head arriving 1–2 f after the chest; f4–9: slow out back toward idle.
- Make four: front, left, right, heavy (heavy adds a step back, 12–16 f). Key the upper body only so legs keep their gait; play at Action4; skip the flinch while a stun or knock-up owns the body `[lihfolk]`.

### Recipe: locomotion set

Build in this order: Idle, Walk, Run, Jump, Fall, Land; add Climb, Swim and Swim Idle when the game uses them (the set Roblox requires for a Marketplace animation pack `[official]`).

| Clip | 30 fps | Rules |
|---|---|---|
| Idle loop | 90–150 f (3–5 s) | Breathing of 1–3°; no dead hold over 9 f; end pose near every attack's start pose; random phase per NPC `[lihfolk]`; a silhouette of its own per character class |
| Walk (R15) | 12 f per step, 24 f cycle | Four poses per step: contact, down, passing, up, unevenly spaced; mirror for the other foot. Author at its real speed, about 5–6 studs/s `[lihfolk]` |
| Run (16 studs/s) | 8 f per step, 16 f cycle | Planted foot travels back `WalkSpeed / 30` studs per frame (0.533 at 16); lean the chest, pelvis pitch at most 8° `[lihfolk]` |
| Sprint (about 26 studs/s) | 6 f per step | A separate clip with a longer stride; do not over-speed the run `[lihfolk]` |
| Jump, Fall, Land | Launch pose in 1–2 f; airborne 15–16 f; land absorb 3 f, hold 2, recover 8–13 | The Humanoid leaves the ground on the input frame, so a crouch needs a scripted delayed jump. Air time follows from JumpHeight 7.2 and gravity 196.2 `[house]`. Let movement cancel Land |

- Torso and head: counter-twist the chest against the hips each step, bob the root, keep the head steadier than the chest. "The torso and head are static" is the most repeated critique in DevForum feedback threads `[community]`.
- No foot slide: store each gait's authored ground speed, play at `rate = horizontalSpeed / groundSpeed` clamped to about 0.5–1.7, switch gait at the clamp and at the same phase so legs do not scissor; fade gait to gait 0.15 s, into Jump and Land 0.08 s, into idle variants 0.4 s `[lihfolk]`. An Animation Graph `Blend1D` with Phase Sync does the same without code (section 5).

### Posing and silhouette checks

- Black-fill test: view each key pose as a flat black shape from the gameplay camera at about 64 px tall (Blender: flat black viewport colour; Studio: a `Highlight` with black fill at 0 transparency). If the action cannot be named, re-pose.
- Weapon, hands and feet outside the torso outline at anticipation and at contact; one idea per pose.
- One line of action from the back foot through the spine to the head, and it reverses between anticipation and contact.
- Centre of mass over the supporting foot; no twinning (mirror-identical arms or legs).
- Push every key pose to about 1.5× what looks right at the desk: chunky avatars at phone distance flatten it `[house]`.
- Pose for the camera the player has: behind and above in third person, so swings that travel across the screen read and thrusts toward the screen do not.

### Stiff-animation tells and fixes

| Tell | Cause | Fix |
|---|---|---|
| Every part starts and stops on the same frame | No overlap | Offset hips, chest, arm, head by 1–2 f each |
| Limbs move, torso and head do not | Only arms and legs keyed | Key LowerTorso and UpperTorso: twist, lean, bob |
| Even, floating motion | Two distant keys and default easing | Favour the keys; fast in, slow out; hold the contact |
| Bouncy wobble at the end | Bounce or Elastic easing, or several overshoots | One overshoot frame, then Quad or Cubic out `[community]` |
| Attack looks weak | No coil, no hold, no overshoot | 2–6 f anticipation, 2–3 f hold, 1 f overshoot, trail on the strike |
| Hand or blade cuts through the body or travels in a straight line | Missing breakdown | A breakdown key on the far side of the arc |
| Pop to idle between actions | Clip ends far from the next start pose; zero fade | End near the pose that takes over (a finished one-shot holds its last pose and fades over about 0.3 s `[lihfolk]`); upper-body layers over locomotion |
| Hitch once per loop | The editor does not interpolate from the last key to the first `[official]` | Copy the first keys to the last frame |
| Statue idle | Dead holds, no breathing | Idle rules above; a spring layer on tails and ears (section 9) |
| Unreadable at phone size | Under-posed; weapon inside the outline | Black-fill test; 1.5× |

### Critique rubric

Score each line 0, 1 or 2 from a recording taken on a phone. Ship at 14 of 18 or more with no zero `[house]`.

| Check | 2 means |
|---|---|
| Readability | Action named from the black-fill silhouette at 64 px on every key pose |
| Timing | Frame counts inside the recipe ranges; contact held; nothing evenly spaced |
| Weight | Anticipation and follow-through sized to the damage; heavy moves authored slow |
| Overlap | Hips, chest, arm and head arrive on different frames; secondary parts trail |
| Arcs | Hands and weapon tip trace clean curves; no pass through the body |
| Transitions | Starts from and returns near idle; no pop into or out of any clip that can follow |
| Contacts and loops | Feet planted with no slide at authored speed; loops with no hitch |
| Game fit | Motion on the input frame; `Hit`, `TrailOn`/`TrailOff`, `CancelOpen` present; enemy telegraph at least 0.45 s |
| Hygiene | Only owned bones keyed; priority set; key density in budget (section 11) |

## 5. Playback: priorities, blending, weights, speed

Rules `[official]` unless tagged:

- Priority order, high to low: Action4, Action3, Action2, Action, Movement, Idle, Core. Where two tracks move the same joint the higher priority shows; tracks at the same priority blend by weight. Measured detail `[lihfolk]`: evaluation is **per joint**, and weight is handed out from the highest priority down until the joint's total reaches 1, so a track at weight 0.5 lets half of the layer below show through.
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

Animation Graphs `[official][VS]` (full release July 2026) publish a blend tree as one asset that loads, plays and replicates like a clip; clips and graphs are interchangeable in code. Drive one with `AnimationTrack:SetParameter("Speed", v)` (parameters replicate; the last write in a frame wins). `Blend1D` and `Blend2D` with Phase Sync replace hand-written gait blending, markers that reach the graph output still fire `GetMarkerReachedSignal`, and Graph > Create Animate script generates the loader for players or NPCs. State machines with Luau-expression transitions (`not Grounded`, `Speed > 5`, a Swing 1 → Swing 2 combo chain) are a Studio beta since October 2026. Test a graph on the 3 GB phone before it replaces a working controller.

## 6. Markers: syncing VFX, SFX and hitboxes

- Author markers in the Clip Editor's event track (name plus optional string parameter); listen with `track:GetMarkerReachedSignal(name)`, which passes the parameter `[official]`. `KeyframeReached` is the legacy mechanism.
- Vocabulary `[lihfolk]`: `Hit`, `Hit2`…; `TrailOn`/`TrailOff`; `Step`; `Tele` (enemy telegraph); `Cast`/`Release`; `CancelOpen`; camera beats `Open`/`Impact`. Keep names identical across clips; one typo is one silent weapon.
- A marker fires on the first animation step whose time span contains it, so up to one frame late, later on throttled rigs; several markers passed in one step all fire in order; setting `TimePosition` skips markers; markers do not fire until the asset has loaded `[lihfolk]`.
- Markers fire on each machine that plays or receives the track, on that machine's clock. A marker on a player's client is a claim, never proof (`networking-and-security.md`).
- **Server hit timing comes from data.** A build step copies marker times into the generated animation table; the server schedules the hit at `markerTime / speed` on its own clock, minus a small lead (0.06 s in the source project) so damage lands as the blade visibly connects, and validates range and cooldown. The server never needs to load the clip `[lihfolk]`. Regenerate the table whenever a clip is retimed.
- Client uses of markers: enable a `Trail` only between `TrailOn` and `TrailOff` (call `Trail:Clear()` first), play the impact sound with its peak on `Hit`, footsteps on `Step` keyed by `Humanoid.FloorMaterial`, camera kick on `Impact`. Skip cosmetic marker work for distant rigs.
- Hitboxes: open the query window between two marker times, cast with `workspace:GetPartBoundsInBox` or blade-sweep raycasts from attachments, client-predicted for feel and server-confirmed for damage. Do not parent hitboxes to client-animated NPC limbs and expect the server to see them (section 7).
- Speed changes move markers in real time; hit-stop delays every later marker by its duration. If a full-body clip plays alongside its upper-body copy, markers fire twice: listen on one only `[lihfolk]`.

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

## 8. NPC animation at scale

Cost model `[official]`: server-played NPC animation is simulated on the server and replicated ("unnecessary overhead"); the mitigation is to play NPC animations on the client, use `AnimationController` instead of `Humanoid` where possible, disable unused Humanoid states, pool NPC models, and spawn only near players. MicroProfiler labels: `stepAnimation`, `stepHumanoid`, `updateInvalidatedFastClusters` (over 4 ms means avatar or skinned-mesh churn).

State protocol `[lihfolk]`: the server AI writes `Anim` (clip name), `AnimSpeed`, then `AnimT` (server time of the start, written last) as attributes on the NPC model; clients react to `AnimT`. Hit reactions, layers and death fades get their own attributes. Damage timing comes from the generated marker table, so the server loads no clips and its hit tests are data-driven (distance, arc, time), not limb positions. Bind the client function below on a `CollectionService` tag-added signal and unbind on removal so streaming works.

```lua
--!strict
-- unexecuted sketch (client): play NPC clips locally from server-written attributes; late joiners land mid-clip.
local function bindNpc(model: Model, clips: { [string]: Animation }): RBXScriptConnection?
	local controller = model:FindFirstChildOfClass("AnimationController")
	if not controller then return nil end
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
		track:Play(0.15, 1, speed) -- TimePosition can be set only while playing
		task.spawn(function() -- Length is 0 until the asset loads: wait, then seek if this is still the clip to show
			while track.Length == 0 and current == track and model.Parent do task.wait() end
			if track.Length == 0 or current ~= track or model:GetAttribute("AnimT") ~= t0 then return end
			local offset = (workspace:GetServerTimeNow() - t0) * speed
			track.TimePosition = if track.Looped then offset % track.Length else math.min(offset, track.Length)
		end)
	end
	local connection = model:GetAttributeChangedSignal("AnimT"):Connect(apply)
	apply()
	return connection -- disconnect it when the tag is removed or the model streams out
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
| Ragdoll / physical joints | AnimationConstraint `IsKinematic = false`: `MaxForce`/`MaxTorque` are hard limits, `AngularStrength`/`LinearStrength` and their `Damping` twins (default 1, mass-independent) set how firmly the joint tracks the clip `[official][VS]`; upgraded avatars already contain BallSocketConstraints. `Humanoid.RequiresNeck = false` and `BreakJointsOnDeath = false` first `[official][lihfolk]` | Owner simulates; see `physics-and-vehicles.md` |

## 10. Tools and weapons, cutscenes, props

**Tools and weapons.** Author the weapon in Blender with a `Grip_Att` empty; hold it with a Motor6D (hand to handle) rather than the default tool weld when clips must move it; held weapon parts are `Massless` with `CanCollide`/`CanTouch` off so they cannot shove the wielder, and gameplay uses an invisible hitbox proxy `[lihfolk]` (house rule 2: see section 13). Put the hold tilt in `C0` once and never change it per state; exactly one controller writes the grip joint; lock procedural sway on the grip from attack accept to recovery end, or the blade twists inside the hand `[lihfolk]`. Moving weapon pieces (bow limbs, a flail) are a small part rig with their own clips on the same Animator, named so poses bind. Preload a kit's clips on equip (first use can otherwise start seconds late). Scale movement speed to 0.55–0.9 during swings to stop sliding `[lihfolk]`. First-person arms are a local-only viewmodel under the camera, bound after camera priority, with every part non-colliding and non-queryable (same house-rule note).

**Cutscenes.** Owned by `cutscenes-and-cinematics.md`: when to use one, shot lists, camera paths, the client-only runner that restores camera, HUD and control on every exit, skip, subtitles, reduced motion and trailers.
Rig-side facts kept here: actors are local clones on a client Animator with `PreferLodEnabled = false`; Blender cameras do not import, so animate a `Cam` bone or part in the actor rig and export it with the clip (playback in that guide's §6).

**Non-character props.**

| Motion | Tool |
|---|---|
| One-shot (door, chest lid, lever) | `TweenService` on the client, tweening `CFrame` (never `Position` on welded models); the server replicates state and start time in one attribute and every client runs the same deterministic tween |
| Endless (spin, bob, sway) | One client loop computing a formula of time, `workspace:BulkMoveTo` for many parts, 30 Hz, range-gated |
| Authored mechanical motion (crane, trap, creature-like prop) | Blender part rig with Motor6Ds, `AnimationController`, published clip |
| Platforms players ride | Physics constraints or matching velocity; characters ride velocity, not teleported CFrames (`physics-and-vehicles.md`) |

Solid props that animate (house rule 2): the server owns collision truth. It moves or toggles the invisible `_COL` proxy at the state change; clients animate only the visual mesh. A door tweened on clients with its collision still closed on the server is a bug in both directions. Parts moved by a client-only Animator stay at rest on the server, so server raycasts see the rest pose.

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
| A limb flips or rotates the long way round | Rotation between two keys exceeds about 120° or is exactly 180°, or generated data has an Euler wrap | Add a breakdown key; blend as CFrames |
| One-key hitch to the rest pose; easing feels backwards | Joint hole (joint missing from a key); legacy `Cubic` or easing set on the arriving key | Key all owned bones on key poses; `CubicV2`, easing on the key that starts the segment |
| Character does not travel or lift, or plays turned 180° after a GLB import | Motion or the importer's axis correction sits on the unapplied top-level root pose `[lihfolk]` | Key the root's first child; calibration clip once per export route |
| Root motion snaps back at clip end | Roblox has no engine root motion: the clip moved the body, not the `HumanoidRootPart` `[community]` | Animate in place and move the root in code from a travel curve, between `MoveStart`/`MoveEnd` markers |
| Shoulders crumple or vertices spike to the origin in Roblox, fine in Blender | More than 4 influences, unnormalised or missing weights | Limit Total 4, Normalize All, run the rig validator, re-export |
| Feet slide | Playback rate not matched to ground speed, or a walk clip at run speed | `rate = speed / groundSpeed`; author a gait for the common speed |
| Feet hover or sink on scaled characters | Clip translations do not follow Humanoid body scale; `Model:ScaleTo` multiplies them `[lihfolk]` | Author translations for the scale method in use; test at real size; check `Workspace.Retargeting` |
| Procedural offset does nothing, or the joint slowly spins away | Written in `PreRender`/`Heartbeat`; joints looked up as Motor6D on an upgraded avatar; compounding on a throttled or unkeyed joint | Write in `PreSimulation`; accept `AnimationConstraint`; check `EvaluationThrottled`; assign from your own base |
| IKControl does nothing / still acts at weight 0 | Missing required property or wrong parent; weight 0 is not off | Check `GetChainCount()`; `Enabled = false` |
| Swipes pass through players on a skinned boss | MeshPart collides in its rest shape | Hitbox parts on bones or data-driven hits |
| Far enemies hit without swinging, or never finish attacks | LOD skipped time and events | Advance time and gameplay events always; skip only pose writes |
| Blade twists in the hand during swings | Two writers on the grip joint | One grip controller; lock sway during attacks |
| Long joins, `stepAnimation` fine | Hundreds of thousands of Pose instances replicated | Publish clips, delete sources and importer saves |
| Server heartbeat drops with many NPCs | Server-side animation and full Humanoids | Client animation, `AnimationController`, fewer Humanoid states, pooling |

Debug order for anything else: print the track's id and `Length`; dump `Animator:GetPlayingAnimationTracks()` (name, priority, weight, speed) at the moment of the bug; solo the clip; try it on a known-good rig; compare owner, second client and server.

## 13. Conflicts and open questions

- House rule 2 and held items: a colliding held weapon or first-person viewmodel destabilises its own wielder, so this file treats items welded or jointed to a character as covered by the character's collider plus a hitbox proxy, and requires the normal `_COL` proxy the moment the item is dropped or placed in the world. SKILL.md states this resolution explicitly (held tools, weapons and viewmodels do not collide; skinned meshes need a `_COL` proxy).
- Resolved 2026: multi-clip FBX and glTF import is official in the Clip Editor importer. `performance.md` and knowledge-base 5.9 still describe one track per FBX, which remains the documented avatar-asset route. Keep the calibration clip per export route: the importer beta shipped a 180° rotation bug, fixed before release `[official]`.
- Conflict: "create the Animator on the server" (Animator reference) versus "create the Animator on the client" (performance docs). Both hold: a server-created Animator is required for replication; a client-created one is the documented way to keep NPC animation local. Likewise "cache tracks" (Animator reference) versus "do not cache" (server authority techniques): cache everywhere except inside server-authority simulation code.
- Conflict: LihFolk's interpolation model (rotation-vector blending between unevenly spaced keys, 0.3 s end fade, unapplied top-level pose) is measured, not documented. Adopted only as authoring guards (turn limits, end poses near idle, root motion on the first child).
- Open `[VS]`: the date the Avatar Joint Upgrade opt-out disappears (announced target: end of 2026); whether client-played tracks on client-owned non-character models replicate; marker timing on throttled remote rigs; a bug report, acknowledged by staff as a known issue (September 2026), that `Transform` writes in `PreSimulation` are ignored while a track plays under `UseFixedSimulation`, which server authority requires (fix promised through a new API: test procedural layers under that setting); the 256-track limit (engine warning text, not in the reference).

## Review gate

- [ ] Every rig, weapon and animated prop came from Blender; the only non-authored visible model is the player avatar.
- [ ] Rig validator passes: one root at origin with no weights, ≤ 4 influences, no unweighted vertices, frozen transforms, stable names, bone budget met.
- [ ] Every animated solid has server-side collision truth: root collider, `_COL` hitboxes on bones where needed, proxies moved by the server for doors and platforms.
- [ ] Every clip is published under the game's owner (or permission granted); no temporary ids; no clip sources or importer saves in the shipped place.
- [ ] One generated animation table holds ids, lengths, ground speeds and marker times; the server times hits from it.
- [ ] A written priority convention exists; `Priority` is set before `Play`; tracks are loaded once and preloaded on equip.
- [ ] Every attack, hit reaction and gait scores 14 of 18 or more on the section 4 rubric with no zero, judged from a phone recording.
- [ ] Player actions move on the input frame; enemy telegraphs ≥ 0.45 s; hit-stop is runtime and client-side; cutscenes restore camera, HUD and input on every exit path and honour reduced motion.
- [ ] NPC animation runs on clients from attributes with server start times; a late-join test passes.
- [ ] Procedural layers write in `PreSimulation`, accept `AnimationConstraint`, check `EvaluationThrottled`, and run on every viewer.
- [ ] LOD skips pose writes only; far and off-screen rigs still advance time and gameplay events.
- [ ] Tested in a published place with two clients and on a 3 GB Android phone; `stepAnimation` and `updateInvalidatedFastClusters` within budget.

## Sources

Accessed 2026-11-10; DevForum, docs commit 7cbffff and external pages read at source 2026-11-11. Short `/t/<id>` links are on devforum.roblox.com. Per-reference evidence and viewed images: `visual-library/animation.md`.

- Roblox/creator-docs (https://github.com/Roblox/creator-docs), `content/en-us/` (read): `animation/index.md`, `animation/using.md`, `animation/editor.md`, `animation/events.md`, `animation/curve-editor.md`, `animation/inverse-kinematics.md`, `animation/graph-editor.md`, `animation/graph-editor-state-machine.md`, `animation/expressions.md`, `animation/capture.md`; `characters/index.md`, `characters/adaptive-animation.md`; `art/modeling/rigging.md`, `art/modeling/specifications.md`, `art/modeling/export-requirements.md`, `art/blender.md`, `art/characters/export-avatar-animations-from-maya.md`; `avatar/character-bodies/specifications.md`, `avatar/emotes/import.md`, `avatar/emotes/specifications.md`, `avatar/resources.md`; `studio/importer.md`; `performance-optimization/improve.md`; `projects/assets/privacy.md`; `projects/server-authority/index.md`, `projects/server-authority/techniques.md`; `cloud/guides/usage-assets.md`; `reference/engine/classes/` Animator, AnimationTrack, AnimationController, AnimationConstraint, Motor6D, Bone, IKControl, KeyframeSequence, CurveAnimation, AnimationClipProvider, KeyframeSequenceProvider, Humanoid, RunService, StarterPlayer, Workspace, RigidConstraint; `reference/engine/enums/` AnimationPriority, PoseEasingStyle, IKControlType, ClientAnimatorThrottlingMode, AnimatorRetargetingMode, AvatarUnificationMode, RestPose.
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `08 Animation/07 Gotchas/{Engine Gotchas, Troubleshooting Table, Animation LOD, Performance and Memory}`, `08 Animation/02 Rigging and Importing/{Animation Data from Blender to Roblox, Exporting FBX vs GLB, Rigging in Blender, Weight Painting and Skinning for Roblox}`, `08 Animation/01 Fundamentals/{Replication and Ownership, Markers and Events, Bones and Skinned Meshes, Frame Order and RunService Timing}`, `08 Animation/03 Authoring/{Locomotion and Melee Reference Numbers, Combat Animation Craft, Timing Spacing and Frame Charts, Principles of Animation for Games, Idle Breathing and Secondary Motion}`, `08 Animation/04 Procedural/{IKControl Reference, Foot Placement and Ground IK, Tween and CFrame Animation of Objects}`, `08 Animation/05 Systems/{Locomotion Systems, Enemy and NPC Animation, Cameras and Cutscenes, UI and GUI Animation}`, `56 Field Notes/{Animation Data Hygiene - Euler Wrap Joint Holes and Easing, Held Weapons on Motor6D - Locking the Grip During Attacks}`, `62 Engine Reference Cards/Animator - Engine Reference Card` (read); TL;DR blocks of the remaining `08 Animation` notes (read).
- DevForum (read, first post or more): Avatar Joint Upgrade live https://devforum.roblox.com/t/4298561; AJU Phase 2 migration https://devforum.roblox.com/t/4656414; Improved AnimationConstraint https://devforum.roblox.com/t/4700211; Clip Editor importer, glTF, multi-clip https://devforum.roblox.com/t/4260501; Animation Graphs full release https://devforum.roblox.com/t/4739840; State machines and expressions beta https://devforum.roblox.com/t/4921939; Adaptive Animation full release https://devforum.roblox.com/t/4605672; Full body animation with fingers https://devforum.roblox.com/t/4618805; Animation Packs on Marketplace https://devforum.roblox.com/t/4861803; Prompt to animation beta https://devforum.roblox.com/t/4977709; Asset versioning https://devforum.roblox.com/t/4977769; Blender rig exporter/animation importer, with post 1628 on the maintained fork https://devforum.roblox.com/t/34729; Jespone's guide to animations https://devforum.roblox.com/t/225752; Creator Spotlight: Bavelly https://devforum.roblox.com/t/3730925; hitbox and animation sync https://devforum.roblox.com/t/4945076; running animation feedback https://devforum.roblox.com/t/315329; sword animation feedback https://devforum.roblox.com/t/588102; low-FPS style https://devforum.roblox.com/t/2800541; Procedural animation https://devforum.roblox.com/t/564782; foot planting with IKControls https://devforum.roblox.com/t/2190661. First post read 2026-11-11 (staff): AJU Studio beta /t/3266099, R6 to R15 adapter /t/2557840, IKControl beta /t/1999010, skinned meshes /t/831011, sharing animation assets /t/3892540; (community, one poster each): client-owned NPC not replicating /t/1838969 and /t/1265879, 256-track warning /t/3064455, priority blending /t/3067476, hitbox validation /t/3843585 and /t/3520770, root motion /t/1556616, `Transform` under fixed simulation /t/4846108 (staff reply), skinned character setup /t/1193941, Blender camera rigs /t/2847027 and /t/3648766, NPC animation at scale /t/142944, skinned-mesh cost on mobile /t/2649641.
- Craft sources (read): Jonathan Cooper, "The 12 principles of animation in video games" (Game Anim excerpt) https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games; Christopher Totten, "12 principles for game animation" https://www.gamedeveloper.com/game-platforms/12-principles-for-game-animation; 80.lv write-up of Mariel Cartwright's Skullgirls GDC talk https://80.lv/articles/tips-on-making-fluid-and-powerful-animations (slides viewed); Thomas Vasseur, Dead Cells art deep dive https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i- (GIFs viewed); Dustloop "Using Frame Data" https://www.dustloop.com/w/Using_Frame_Data; Cautioned/Blender-Animations-Plugin README (GPL-3.0). Degree ranges and the rubric threshold marked `[house]` are house estimates, not sourced.
