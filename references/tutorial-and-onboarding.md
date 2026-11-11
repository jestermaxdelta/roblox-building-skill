# Tutorials and onboarding: first-minute script, teaching patterns, guidance devices, step state, funnels

The owner file for in-game teaching and the first-time user experience (FTUE): how to script the first minutes, which teaching pattern to use, how to build each guidance device cleanly, how to keep step state on the server, how to instrument and read the funnel, and how to repair a live game's onboarding. Open it when writing the first-minute script, building any tutorial or hint, and whenever first-play bounce or D1 is below benchmark. Neighbours: load, spawn and the next-goal HUD spec are in design-foundations.md §7.2–7.3; the loop spec, scorecard, Creator Analytics reading order and experiments are in core-loop-tuning.md; event limits are in analytics-and-discovery.md; viewed reference images, talks and modules are in visual-library/tutorials-and-onboarding.md.

Tags: `[official]` Roblox docs or staff posts; `[community]` forum threads, and outside-Roblox articles, talks and studies (named inline; single-developer numbers are labelled as such); `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production RNG combat game); `[VS]` version-sensitive, re-check at create.roblox.com/docs; `[house]` house rule or estimate.

## Start here by level

| Level | New game | Live game (level-up) | Leave for later |
|---|---|---|---|
| Beginner | Write the script (§2). Use patterns 1 and 5 only (§3): spawn facing the verb, one prompt, one timed hint. Copy rules in §7. Time five fresh players | Time your own first minute on a phone with a fresh account; score the rubric (§13); fix the lowest row | Step machine, funnels, experiments |
| Intermediate | Add the guided first quest only around verbs testers do not find (§3–4); server step state with skip and resume (§8); funnel plus hint and skip events (§9) | Run the repair procedure (§14) on the earliest weak step, one change per release | Journeys, experiments under about 1,000 DAU |
| Expert | Contextual tips for every secondary system; versioned funnels; Journeys for branching starts; hint delay and step count as experiments | Cohort reads by source and platform; lapsed-player recap; rubric review after every update that touches the first 10 minutes | — |

## Contents

0 Evidence · 1 Goals and metrics · 2 First-minute script · 3 Teaching patterns ranked · 4 Step design · 5 Guidance devices · 6 Accessibility and phone rules · 7 Copy for children · 8 Server state, save, skip, replay, returners · 9 Funnel: instrument and read · 10 Tutorial per genre · 11 Anti-patterns with evidence · 12 Case study · 13 Critique rubric · 14 Repair procedure · 15 Level-up symptoms

## 0. What the evidence supports

- `[official]` Onboarding has three goals (teach the essentials, get to the fun quickly, leave players wanting more) and is judged by D1 and those goals. "Lengthy, detailed tutorials are liable to bore users and cause them to bounce"; make any tutorial as visual as possible; stay close to genre norms so less needs explaining. Three named techniques: visual elements, contextual (just-in-time) tutorials, timed hints.
- `[official]` Worked case (Plant sample game): 70.48% of new players never planted the first seed. The fix that worked was an icon above the pots, not a longer tutorial.
- `[community]` The one controlled study found (Andersen et al., CHI 2012; 8 tutorial designs, 3 games, over 45,000 players): tutorials helped only the complex, unconventional game (+29% play time, +75% levels) and did nothing in the two simple ones; in-context instructions beat a manual in the complex game (+40% levels, +16% time); **blocking the player until they obey improved nothing in any game**; in one simple game only 31% of players ever opened a help button, and offering it cut progress 12% and play time 15%.
- `[community]` Nielsen Norman Group's child usability studies (125 children aged 3–12, three rounds) saw children skip lengthy explanations, including on Roblox; the youngest do not read, 6–8s read tentatively, 9–12s scan; children try every option on screen and cannot tell promotions from content.
- `[community]` Roblox developers' own numbers (single cases, self-reported): a forced teleport to a solo tutorial place "caused a massive drop in session time and D1 retention", and moving the teaching into the main game as contextual tips recovered session time; a second developer tried a separate tutorial place and went back for the same reason; a third had 75% tutorial completion and still lost most finishers within five more minutes. Two more single cases from search summaries of Reddit posts: D1 6% → 15% after a 5-step tutorial became 3 (§15), and early exits 45% → 18% after the spawn got one clear first action (core-loop-tuning.md §6).
- Not found: a published Roblox A/B of forced against contextual teaching, or measured effects of a skip button. Reading: shorten, show, and teach in context; more tutorial does not rescue a loop that is not fun (core-loop-tuning.md §4).

## 1. Goals and metrics

Onboarding is finished when the player has run the loop once without help, can say what they are doing and why, has a next goal on screen, and knows one thing that will be different tomorrow.

| Metric | Definition | Read it in | Starting target |
|---|---|---|---|
| Time to control | Join to a movable character on a 3 GB Android phone | Stopwatch; `FtueBeat` event (core-loop-tuning.md §7) | 10 s or less `[house]` |
| Time to first verb, first reward | Seconds from control | `FtueBeat` | 15 s, 30 s `[house]` |
| Step conversion | Players finishing step n ÷ players finishing n−1 | Funnels → Onboarding | 90%+ on early steps `[lihfolk]`; act on any step losing twice its neighbours |
| Completion | Last step ÷ first step | Same chart, Total Conversion | 70%+ `[lihfolk]`; a means, not the goal (see the 75% case above) |
| Hint rate, skip rate | Hint shown or skip pressed ÷ players on that step | Custom events in Explore | No benchmark; compare steps with each other |
| First-play bounce | Sessions under 60 s, and 61–180 s | Home Recommendations | Similar-games range |
| First-session curve | Share of new users still playing each minute | Engagement | Half still playing at 3 min `[community]`; no cliff |
| D1 by source | Next-day return, Home Recommendations cohort | Retention | Your own P50, then P90 |
| Loop statable | "What are you doing and why?" at minute 2 | Playtest | 4 of 5 testers |

Some loss is not yours to fix: one survival game lost 16% of ad-sourced joiners before a single tap on a dimmed screen with one flashing slot `[community]`. Judge a step against its neighbours, against itself last week, and by source.

## 2. First-minute script format

Write the script as beats before building, then build exactly that and time it with a stopwatch on the target phone. One new concept per beat; at most three concepts before minute 2; the script ends on a designed moment of joy `[official]`. Funnel step names match analytics-and-discovery.md; extra beats go out as `FtueBeat` (CustomField01 = beat, value = seconds since spawn).

| Window | Beat | Player does | Game does (words on screen) | Log | Fails when |
|---|---|---|---|---|---|
| Before join | Promise | Taps a tile | Tile shows minute one, not the endgame | (PTR) | Tile and first minute differ `[official]` |
| 0–5 s | Arrive | Nothing | Spawns in a playable area facing the verb target; no menu, play button or cutscene (0 words) | 1 `Spawned` | Control takes over 10 s `[house]` |
| 5–15 s | Call to action | Sees one prompt | One device-matched prompt on the one thing to do; nothing else pulses (≤ 4 words) | — | Two things compete for attention |
| 15–30 s | First rep | Performs the verb | Same-frame feedback, sound, number; first reward | 2 `FirstAction`, 3 `FirstReward` | No reward by 30 s |
| 30–60 s | Repeat | 2–3 more reps | Goal bar appears, already part-filled with real progress (verb + count) | `FtueBeat: GoalBarShown` | Player stops and looks around |
| 60–120 s | First upgrade | Buys or earns it | Visible power change in the world (the aha) | 4 `FirstUpgrade` | Upgrade is a menu stat |
| 2–3 min | First choice | Picks between two real options | Contextual tip only when the system is met | `FtueBeat: FirstChoice` | A fourth concept before minute 2 |
| 3–5 min | Joy moment | Hits a milestone | Designed celebration; first collection entry | `FtueBeat: FirstCollect` | Nothing memorable by minute 5 `[official]` |
| 5–10 min | Meso goal | Completes it | Next three goals (now, session, long-term); the return hook | 5 `FirstWin`, 6 `SawGoals` | No visible next goal; dead time over 5 s |
| 10 min+ and first win | After | Keeps playing | Offers may begin through the offer gate (monetization-and-policy.md); notification opt-in at a warranted moment, 13+ `[VS]` | Offer funnel | Any purchase prompt earlier (house rule) |
| Session 2 | Welcome back | Returns | What changed, one new thing, the next goal | 7 `Session2Start` | Same state, nothing new |

House default: no forced tutorial. A soft-gated, skippable guided first loop of 3–7 steps at most, timed hints for the minority who stall, contextual tips for everything else.

## 3. Teaching patterns, ranked

Use the highest pattern that teaches the thing; move down a row only when a playtest shows the row above failed.

| # | Pattern | How it works | Fits | Cost and risk | Evidence |
|---|---|---|---|---|---|
| 1 | Do-to-learn | The first rep of the real loop is the lesson: spawn faces the target, one prompt, the result explains itself | Every game whose verb is done in the world | Spawn and level layout; nothing to maintain | Fan: do, not read, and once is often enough; Andersen: simple games gain nothing from more `[community]` |
| 2 | Level shape | Introduce the mechanic safely, develop it, add a twist, then test it (the four-step Nintendo structure) | Obbies, platformers, horror, puzzles | Level-design time; cannot teach an economy | Hayashida interview `[community]` |
| 3 | Contextual prompt | A show-once tip fires on a server trigger the first time a system is met or becomes usable | Every secondary system: shop, index, rebirth, trading, crafting | One trigger and one saved flag per system. Players who never meet the system never see it: surface it with a timed hint after two sessions `[official]` | Squishmallows in the docs `[official]`; Andersen `[community]` |
| 4 | Guided first quest | 3–7 server-owned steps, soft-gated, each paying a visible reward, ending on a real goal | Simulators, tycoons, RPGs with a step players do not find alone (salvage, forge, combine) | Step machine, saves, funnel, upkeep on every update | §12 `[lihfolk]`; Plant `[official]` |
| 5 | Timed hint | Arrow, glow or hand appears only after a stall, once, and goes on progress | Any step where a minority stalls | A timer and a cue. Delay = time most players need + 1 s (docs example: 10 s, hint at 11 s); tune 5 s against 10 s `[official]` | Fan's adaptive messaging: tips only for players doing the wrong thing `[community]` |
| 6 | Demonstration | An NPC, ghost, spectating or other players show the action and its result; the player may repeat it without penalty | Timing and physical verbs; players who watch before they act | Animation work. Never blocks input | Graner Ray: "modelling" learners quit explore-only tutorials `[community]` |
| 7 | Safe sandbox | An opt-in practice space where nothing is lost | Novel controls, competitive shooters and fighters | Must be optional, in the same place, enterable with a friend. Forced, solo or by teleport it lost players in two reported cases `[community]` | Adams recommends a separate optional area `[community]` |
| 8 | Gating | Input or features locked until the step is done | Only where one early action can soft-lock or destroy progress | Reads as a cage; experienced players leave | Andersen: no gain from blocking in any game `[community]` |

How much to teach: if testers find the verb within 15 s unaided, ship rows 1 and 5 only. If the economy hides a step, wrap a guided quest around that step, not around the obvious verb. If the controls are new, add rows 6 and 7. Serve both learner types: let the explorer act at once, and give the watcher something to watch and a free repeat.

What a new player may touch before it is taught `[lihfolk]`. **Soft gate** (default): everything works, pointers and rewards follow the script; players wander, so the goal line must always be right. **HUD reveal** (default, with the soft gate): buttons stay hidden until their step and then animate in, later features show a lock and a condition; skips and rejoins must reveal everything already passed. **Contextual unlock**: a feature appears when first needed; optional features go unfound unless a goal points at them. **Hard gate**: only the current step responds; row 8 applies, so keep it for games with 2–3 verbs.

## 4. Step design

Shape: **steps are data, the server owns progress and rewards, the client only draws guidance** `[lihfolk]`.

| Field | Meaning | Rule |
|---|---|---|
| `id` | Permanent name | Never reused. Saves store ids, not positions, so steps can be inserted or removed |
| `objective` | The one line on screen | §7 |
| `signal`, `goal` | Server event that counts, and how many | Sent by the system that knows (currency changed, pet hatched), never a client "I finished". 1 for a new verb, 3–10 for a rhythm step |
| `trigger` | Server condition that starts a contextual step | Backpack full, first time near the trader |
| `isComplete` | Server check for "already done" | Completes the step for players who got there another way (gift, trade, veteran) |
| `guide`, `hintAfter` | `always`, `whenStuck` or `none`; seconds before help | Verbs most players find alone use `whenStuck`; progress resets the timer; guidance stops once the player has done it unaided |
| `reveal` | HUD keys shown when the step starts | The HUD reveal above |
| `reward`, `topUpTo` | What the step pays; a guaranteed balance | Every step pays something visible. Before a purchase step, top the player up to exactly the price: a tester of a digging game finished the mining step and still could not afford the shovel the tutorial pointed at `[community]` |
| `optional` | Never blocks the chain | Social steps always; a friend who joins plays from second one |

Step patterns: **do it once** (`goal = 1`, guide always) for each new verb; **do it a few times** (3–10, pointer to the nearest target only) for rhythm; **try first, help later** (`whenStuck`, 6–10 s); **already done** (`isComplete`); **contextual** (`trigger`); **HUD button** (reveal plus a pulse on the exact button, world pointer off); **affordable purchase** (`topUpTo` on the step before); **server-decided moment** (a short skippable scripted beat).

Anything that can be failed is the main funnel risk. A first fight is against an enemy owned by this player only and weakened (reference project: 0.5× health and 0.3× damage; a tutorial elite at 4× health and 0.4× damage where normal elites were 12× and 1.5×) `[lihfolk]`. A tower-defense first wave cannot be lost; a horror first threat has a long readable warning; a missed jump respawns beside the jump.

## 5. Guidance devices

One pointer and one pulse at a time: with two, players follow neither. Every device is drawn on the client from the replicated step state and removed on step change and on respawn. House rules: a 3D arrow, sign or marker is a Blender mesh placed above head height or beside the route with collision off; beams, highlights, particles and UI are effects, with textures designed in Figma.

| Device | Use when | Build | Limits |
|---|---|---|---|
| World beam, character to target | Target is far or out of view | Client `Beam` between an `Attachment` on the root part and one at the target; `FaceCamera = true`, `TextureMode = Static` with a chevron texture, `TextureSpeed > 0`; re-attach on `CharacterAdded`; switch off within about 10 studs `[official]` | A straight beam passes through walls: route it through hand-placed waypoint attachments indoors. Draw the chevron two-tone (light fill, dark or saturated edge): a white line on snow vanished in one game `[community]` |
| Ground trail (dots, footprints) | Short routes, interiors, hints that should feel found | Decals or pooled emitters along the path; dots that end in a ring at the target | Suggests without ordering (Jailbreak's footprints to the sewer lid `[official]`); too subtle for a mandatory step |
| Marker over the target | Target is visible among look-alikes | Bobbing Blender arrow or a `BillboardGui` icon with `AlwaysOnTop` and a pixel size that stays 44 px or more on a phone | Bob stops under reduced motion |
| Icon over an interactable | Players do not realise the object can be used | Small billboard with the item icon and a down arrow | The cheapest fix; it closed Plant's 70% drop `[official]` |
| `Highlight` | One interactable among look-alikes | One reused instance, move `Adornee`; contrasting `OutlineColor`, `FillTransparency` 0.7 or more; `DepthMode` occluded unless the point is seeing through walls | Up to 255 on a client, disabled ones still count, extras are ignored silently `[official]` `[VS]`. A red fill on red objects read as "tinted, not highlighted" `[community]`. Never rescan `GetDescendants` each frame to place highlights |
| `ProximityPrompt` | "Walk up and press" is the verb | Shows the right key, button or tap by itself; `HoldDuration = 0` for a first interaction; set `MaxActivationDistance` and `RequiresLineOfSight` | A HUD button does the action: use the pulse instead |
| Screen-edge pointer | The target is off-screen or behind the camera | `Camera:WorldToViewportPoint`; when off-screen, clamp to the viewport edge inside a margin and rotate the arrow toward the target (sketch below) | Hide it the moment the target is on screen and let the world marker take over |
| Spotlight on a HUD button | First use of a menu verb | Overlay `ScreenGui` in the tutorial layer (ui-input-crossplatform.md) with `ScreenInsets = CoreUISafeInsets`; a hole that follows the target's `AbsolutePosition` each frame (a transparent frame with a very thick dark `UIStroke`, as the open-source SpotlightUI does); find the target by tag, not name | Dimming alone is not a pointer: add an arrow or hand at the hole. Skip stays visible and tappable. Always clean up, or the screen stays dark |
| Pulse or hand on a button | Lighter nudge at a GUI target | Scale 1 → 1.08 about once a second, or a tapping-hand sprite | Static outline under reduced motion; one on screen |
| Quest tracker line | Always | Spec in design-foundations.md §7.3; shows the verb and the count ("Kill 5 skeletons 4/5") | Never the only cue for a first verb |
| NPC guide | The fiction has a mentor; a system needs two sentences | Portrait or world NPC, 2 lines at most per turn, advance on tap with a visible "tap to continue" | Never locks movement; a tester of one fishing game did not know the dialogue wanted a tap `[community]` |
| World sign with a diagram | A rule needs a picture (Color or Die's three-panel "Hidden / Dead / Dead" wall `[official]`) | Blender board with a designed texture, in the line of sight on the walk to the first verb; pictures plus 1–2 words each | Cannot react to the player |
| Controls legend | Controls are unusual for the genre | Small device-matched list; `InputActionLabel` shows the current binding without code `[VS]` (Studio beta in August 2026; check that it publishes) | Hide after first use; never list WASD |
| One camera nudge | Something behind the player must be noticed, once | 1.5 s or less, control returns at once | Off under reduced motion; never repeated |

```lua
--!strict
-- Unexecuted sketch. Client: one beam to the target; an edge arrow (ImageLabel, art points right, centre anchor, in a ScreenGui with IgnoreGuiInset) while it is off-screen.
local GuiService = game:GetService("GuiService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local MARGIN = 48 -- px kept clear of the screen edge and core UI
local player = Players.LocalPlayer
local camera = workspace.CurrentCamera :: Camera
local edgeArrow = player:WaitForChild("PlayerGui"):WaitForChild("TutorialGui"):WaitForChild("EdgeArrow") :: ImageLabel
local goal = Instance.new("Attachment")
goal.Parent = workspace.Terrain
local beam = Instance.new("Beam")
beam.FaceCamera, beam.TextureMode, beam.TextureLength = true, Enum.TextureMode.Static, 4
beam.Width0, beam.Width1, beam.Enabled = 2, 2, false
beam.Parent = goal
local target: Vector3? = nil
local Guidance = {}

local function source(character: Model?): Attachment?
	local root = if character then character:FindFirstChild("HumanoidRootPart") else nil
	local found = if root then root:FindFirstChild("GuideSource") else nil
	if root and found == nil then
		found = Instance.new("Attachment")
		found.Name = "GuideSource"
		found.Parent = root
	end
	return found :: Attachment?
end

function Guidance.point(position: Vector3?) -- nil clears; call when the hint timer fires and on step change
	target = position
end

RunService.RenderStepped:Connect(function()
	local from = source(player.Character)
	if target == nil or from == nil then
		beam.Enabled, edgeArrow.Visible = false, false
		return
	end
	goal.WorldPosition = target
	beam.Attachment0, beam.Attachment1 = from, goal
	beam.TextureSpeed = if GuiService.ReducedMotionEnabled then 0 else 1
	beam.Enabled = (target - from.WorldPosition).Magnitude > 10
	local point, onScreen = camera:WorldToViewportPoint(target)
	edgeArrow.Visible = not onScreen
	if not onScreen then
		local centre = camera.ViewportSize / 2
		local direction = Vector2.new(point.X, point.Y) - centre
		if point.Z < 0 then
			direction = -direction -- behind the camera the projection is mirrored
		end
		local reach = math.min((centre.X - MARGIN) / math.max(math.abs(direction.X), 0.001), (centre.Y - MARGIN) / math.max(math.abs(direction.Y), 0.001))
		local position = centre + direction * reach
		edgeArrow.Position = UDim2.fromOffset(position.X, position.Y)
		edgeArrow.Rotation = math.deg(math.atan2(direction.Y, direction.X))
	end
end)
return Guidance
```

## 6. Accessibility and phone-size rules

- **Device-true prompts.** Resolve `{TAP}`, `{INTERACT}` tokens on the client from `UserInputService.PreferredInput` and re-render when it changes, because players switch device mid-step; show the remapped key, not the default `[official]` `[lihfolk]`. Touch verbs are their own words ("Drag", "Tap Jump"), not translated keys.
- **Layout.** Objective top-centre with the hint one line below, inside `CoreUISafeInsets`, clear of the left-stick and jump zones and of the middle of the play area. Targets, Skip included, 44 px or more. Check at 667×375 and with `GuiService.PreferredTextSize` at its largest (ui-input-crossplatform.md).
- **Colour plus shape plus words.** A cue is never colour alone. Test each cue on the lightest and the darkest ground in the game.
- **Reduced motion.** When `GuiService.ReducedMotionEnabled` is true: no pulses, static beam texture, no camera nudge, instant HUD reveals `[official]`.
- **Time.** Objectives stay until done; dialogue advances on tap; nothing important is on a timer. Captions for any voiced line.
- **Gamepad and sound.** Set `GuiService.SelectedObject` to the target button when a HUD step starts. Every cue has a sound and no step depends on hearing it. Settings stay reachable during the tutorial (accessibility-and-player-qol.md).

## 7. Copy for children

Assume the youngest reader is 7 and reads slowly; many players read English as a second language; the youngest do not read at all, so the loop must be completable from icons and pointers alone `[official]` `[community: NN/g]`.

| Rule | Number or test | Source |
|---|---|---|
| Words on screen | 8 or fewer at any moment; objective 2–5 | Fan `[community]` |
| Reading level | One- and two-syllable words a 7-year-old reads; no idioms, no lore names in instructions | NN/g: write at each user's grade level `[community]`; `[house]` |
| Form | Verb first, then object, then count: "Sell 3 boxes". Numerals, present tense, one instruction per line | `[house]` |
| Icon plus word | The thing's icon sits beside its name; colour the key word like its target (Creatures of Sonaria prints "water" and "blue" in the trail's blue `[official]`) | Docs: visuals need no translation `[official]` |
| Name the button exactly | Use the label on the button and point at it | Adams: badly described buttons `[community]` |
| Pop-up budget | 3 or fewer text pop-ups in the first 5 minutes; a dialogue turn is 2 lines of 12 words | `[house]` |
| Tone | Celebrate real milestones; no praise for pressing a key; never blame | Adams `[community]` |
| The word "tutorial" | Do not use it; it is the game's first quest | Fan `[community]` |
| Localisation | Tokens stay outside translated strings; leave 30% spare width | accessibility-and-player-qol.md |

Rewrites: "Welcome to Box Tycoon! To begin your journey, head over to the conveyor and start collecting boxes to earn coins." becomes "Collect 5 boxes" with a box icon and a beam. "Open your inventory by clicking the backpack button." becomes an arrow on the button and "Open bag". "When the monster approaches, stand against a wall of your colour or it will see you." becomes a three-picture sign: same colour, hidden; other colour, caught.

## 8. Server state, saving, skip, replay, returning players

What the server machine guarantees `[lihfolk]`:

- Progress and rewards live on the server and in the profile; the client gets one replicated value and every HUD script reads that value.
- Each reward pays once. Skip grants what the remaining steps would have paid and reveals the whole HUD; a replay from Settings pays nothing.
- A failed profile load pauses the tutorial; it never restarts it. Rejoin resumes the same step; finished steps never show again; steps added after launch show only to players who lack them; removed steps map to the nearest current step through a rename table.
- Guidance is cleaned up on step change and respawn; dying mid-step respawns fast and the step still works.
- No automatic pop-up while onboarding runs (daily reward, favourite, group, event, offer). One gate function decides every automatic pop-up: not during onboarding (treat the first 180 s as onboarding if the state is unknown), not over another panel or the death screen, not in combat, at least 8 s after the previous one. Offers also obey the offer gate in monetization-and-policy.md.
- After the last step a successor exists: the next-goal chain (design-foundations.md §7.3).
- Skip is visible from the second step at the latest, never behind a menu, and logs `TutorialSkip` with the step id. Do not log the remaining funnel steps on skip: a later step logged without the earlier ones marks them all complete `[official]` and hides where players skipped.
- Test matrix before shipping any tutorial change: fresh account on a phone-sized viewport, with keyboard, with gamepad; switch device mid-step; rejoin mid-step; skip; die mid-step; a friend joins; each dependency system's kill switch off.

| Player | Detect | Do |
|---|---|---|
| Brand new | No profile | First loop from step 1 |
| Rejoined mid-tutorial | Saved step id | Resume that step with its progress |
| Finished | `done` flag | Nothing. New systems teach themselves through contextual steps |
| Skipped | Skip event, `done` | Same as finished; a "Tips" entry in Settings can replay any step for no reward |
| Fast or genre-veteran | Acts before `hintAfter`; `isComplete` true | No hints ever appear; that is the adaptive path |
| Joined a friend | `Player.FollowUserId ~= 0` | No hard gate; steps run beside co-play and social steps complete themselves |
| Lapsed | Profile last-seen over about 14 days; `AnalyticsService:GetPlayerSegmentsAsync` gives coarse new/active/lapsed/reactivated buckets, `HasData` false when unavailable `[official]` `[VS]` | A recap panel: one line per system added since, the current goal, optional replay. Never the tutorial again. House rule: payer buckets never change difficulty, odds or prices |

```lua
--!strict
-- Unexecuted sketch. Server module: steps as data, progress saved by step id, each step logged once, skip pays the rest.
local AnalyticsService = game:GetService("AnalyticsService")
local HttpService = game:GetService("HttpService")

export type Step = {
	id: string, -- permanent; never reused for a different step
	objective: string, -- 8 words or fewer; {TOKENS} resolve per device on the client
	signal: string, -- sent by the server system that knows it happened
	goal: number,
	hintAfter: number?, -- seconds without progress before the pointer appears
	reveal: { string }?, -- HUD keys shown when this step starts
	topUpTo: number?, -- balance guaranteed before this step, so its purchase is affordable
}
export type Saved = { stepId: string?, progress: number?, done: boolean? }
type State = { index: number, progress: number }

local FIELD1 = Enum.AnalyticsCustomFieldKeys.CustomField01.Name
local STEPS: { Step } = {
	{ id = "collect", objective = "Collect 5 boxes", signal = "Collected", goal = 5 },
	{ id = "sell", objective = "Sell at the green pad", signal = "Sold", goal = 1, hintAfter = 8 },
	{ id = "upgrade", objective = "{TAP} UPGRADE", signal = "Upgraded", goal = 1, reveal = { "UpgradeButton" }, topUpTo = 40 },
}
local RENAMED: { [string]: string } = {} -- removed step id -> nearest current step id
local states: { [Player]: State } = {}
local Tutorial = {}

local function publish(player: Player, state: State)
	local step = STEPS[state.index]
	player:SetAttribute("Tutorial", HttpService:JSONEncode({
		id = if step then step.id else "done",
		objective = if step then step.objective else "",
		progress = state.progress,
		goal = if step then step.goal else 0,
		hintAfter = if step then step.hintAfter else nil,
		reveal = if step then step.reveal else nil,
	}))
end

-- Call only after the profile loaded. On a failed load do not call: a paused tutorial beats a reset one.
function Tutorial.attach(player: Player, saved: Saved?)
	local state: State = { index = 1, progress = 0 }
	if saved and saved.done then
		state.index = #STEPS + 1
	elseif saved and saved.stepId then
		local id = RENAMED[saved.stepId] or saved.stepId
		for index, step in STEPS do
			if step.id == id then
				state.index, state.progress = index, saved.progress or 0
				break
			end
		end
	end
	states[player] = state
	if state.index == 1 then
		AnalyticsService:LogOnboardingFunnelStepEvent(player, 1, "Spawned") -- repeats count once
	end
	publish(player, state)
end

-- Gameplay systems call this; the client never does. Returns the step just completed so the caller pays it and saves.
function Tutorial.signal(player: Player, signal: string, amount: number): Step?
	local state = states[player]
	local step = if state then STEPS[state.index] else nil
	if state == nil or step == nil or step.signal ~= signal then
		return nil
	end
	state.progress = math.min(step.goal, state.progress + amount)
	local finished = state.progress >= step.goal
	if finished then
		state.index += 1
		state.progress = 0
		AnalyticsService:LogOnboardingFunnelStepEvent(player, state.index, step.id)
	end
	publish(player, state)
	return if finished then step else nil
end

-- Returns the steps not yet paid; the caller grants their rewards once, reveals the HUD and saves.
function Tutorial.skip(player: Player): { Step }
	local state = states[player]
	local unpaid: { Step } = {}
	if state == nil or state.index > #STEPS then
		return unpaid
	end
	AnalyticsService:LogCustomEvent(player, "TutorialSkip", 1, { [FIELD1] = STEPS[state.index].id })
	table.move(STEPS, state.index, #STEPS, 1, unpaid)
	state.index, state.progress = #STEPS + 1, 0
	publish(player, state)
	return unpaid
end

function Tutorial.snapshot(player: Player): Saved
	local state = states[player]
	local step = if state then STEPS[state.index] else nil
	return { stepId = if step then step.id else nil, progress = if state then state.progress else 0, done = state ~= nil and step == nil }
end

function Tutorial.detach(player: Player)
	states[player] = nil
end
return Tutorial
```

## 9. Funnel: instrument, then read

Instrument `[official]` unless tagged:

1. List 6–12 steps from the script, each a fact the server can observe. Step 1 is logged on join so the funnel starts there.
2. Log after the step is completed, from the system that knows. The docs' own sample lets the client report steps through a remote with a range check; server facts are cleaner `[house]`.
3. Where a loss is suspected, split the step finer: "opened shop", "picked item", "bought" instead of "bought" `[community]`.
4. Add custom events `TutorialHint` and `TutorialSkip` (CustomField01 = step id) and `FtueBeat` for time-to-beat. Append two survival steps after the last tutorial step ("played 1 more minute", "played 5 more minutes"): in one +1-speed game 75% finished the tutorial, 83% of those stayed one more minute and 43% of those five more, which put the fault after the tutorial, not in it `[community]`.
5. Pass custom fields on funnel steps (variant, starter choice) to break the chart down; three fields, 8,000 value combinations per game.
6. When steps are inserted or reordered, the chart flags the changed step: set the date range from the change date, or log a fresh named funnel (`Tutorial_v3` through `LogFunnelStepEvent`) so cohorts do not mix `[lihfolk]`.
7. A branching start (class, starter pet, tutorial path) is a Journey, not a funnel: `AnalyticsService:LogJourneyEvent(player, journeyName, nodeName)`, up to 10 stages of 10 nodes, shown as a Sankey chart with skipped and churn rates per node (launched November 2026) `[VS]`.
8. Verify in a published test place: Studio sends nothing.

Facts that change the reading: only the first instance of a step counts; a later step logged alone completes the earlier ones; filters such as device apply to the first step only; players are grouped by the day they entered; a player with no funnel events for 180 days counts as new again.

| The funnel shows | Likely cause | Confirm with | Fix |
|---|---|---|---|
| Perfect, or empty | Logging fault | View Events; play in the published place | Fix the plumbing before any design change |
| Largest loss between join and step 2 | Arrival, not the tutorial: join time, spawn facing away, unreadable first objective, wrong audience | Performance by device; split by source; stopwatch | design-foundations.md §7.2; honest tile; in-world cue on the target |
| One step drops, hint rate high | Confusion: goal or target unclear | Watch three fresh players | Rewrite the objective (§7); pointer on the exact target; move the target into view |
| One step drops, skip rate high | Tedium | Time the step | Lower its `goal`, pay more, or cut it |
| One step drops, neither high | Blocked: dependency off, unaffordable price, button off-screen on phones, an edge case (sold the only rod) | Play it on a phone with a fresh account | `topUpTo`; kill-switch test; guard the edge case |
| Menu steps lose far more than world steps | Depth and choice in the UI | Count taps | Open the panel on the right tab, spotlight the one button, fewer options. One survival game lost 34% at "choose the workbench in the craft list" and 2–6% at each world step; a wave shooter with 483,000 funnel entrants kept 86–93% at each of four play steps, then lost 73% at "purchased first weapon", which its developer traced to the number of panels to click through `[community]` |
| A failable step drops | Difficulty | Win and lose logged separately | Make it safe (§4) or move it later |
| Even loss at every step | The loop, not a step | First-session curve | core-loop-tuning.md §4–6 |
| Tutorial finished, D1 still low | No successor goal, or nothing to return to | Session time after the last step | Next-goal chain; return hook |

Fix from the earliest weak step forward: the step after a confusing one inherits its confused players. Segment before concluding (platform, new against returning, source); read medians; annotate every release; one change per release.

## 10. Tutorial per genre

Full loops are in `references/genres/`; first-minute observations of 18 hits are in case-studies-teardowns.md §2. Rows marked `[community]` rest on the funnel threads in Sources; the rest is `[lihfolk]` and `[house]`.

| Genre | First loop to teach by doing | Pattern and device | Make it safe | Leave for contextual tips | Typical failure |
|---|---|---|---|---|---|
| Simulator, incremental | Collect → sell → upgrade, three times; first pet or egg by minute 5 | 1 + 5; guided quest only if selling is not obvious; beam to the sell pad | First upgrade affordable from the first sale | Trading, rebirth, later zones | The sell pad is a long walk; a shop before anything is sold |
| Tycoon, management | Claim plot, first dropper or station, first purchase from income | 1; a pulse on the one affordable button | Something affordable inside 30 s | Rebirth, automation | An empty plot and nothing affordable |
| Steal, escape, grab | The verb in the title; live through one risk event | 1 + 6 (other players demonstrate) | Newcomer grace window or income-gap limit | Rare variants, defences | Robbed by a rich player in minute one |
| Obby, platformer | Move, jump, first checkpoint within about 20 s | 2 (introduce, develop, twist, test) | Respawn beside the jump | Speed routes, skips | A hard jump before checkpoint one |
| Combat, RPG, battlegrounds | First hit, first kill, one ability, one upgrade | 4 with one safe fight; marker over the reserved enemy | Private weakened enemy (§4) | PvP, builds, combos | Full-strength enemies; five abilities at once |
| Shooter, wave defence | Shoot, survive wave one, buy one weapon | 1 + 3 in the main game with other players | Wave one cannot be lost | Crates, attachments, modes | A solo tutorial place; the first purchase buried in panels `[community]` |
| Horror, co-op escape | Mood, then one threat with a long readable tell | 2 + 6; death explains itself in one sentence | The first threat has one clear answer | Lore, rare entities | An unfair first death |
| Social, roleplay | Own something (house, car, outfit) and meet a player | 1; one menu, no gate | Nothing to lose | Jobs, premium items | Any gate before props and friends |
| Tower defense | Place one tower at a marked good spot; win wave one; upgrade before wave three | 4, three steps, range shape shown on placement | Wave one cannot be lost | Synergies, modes | Every stat explained first |
| Survival, crafting | First resource in three hits; first craft; first night with friends | 1 + 5; an icon over the first resource | First night is survivable | Crafting trees | A slow first harvest; the craft menu as step two with the whole HUD visible `[community]` |
| RNG, rolling | Roll, equip, roll again | 1; guided quest around the hidden step (salvage, forge) | Honest odds from roll one | Crafting, potions, index | Teaching the obvious roll and not the hidden economy `[lihfolk]` |
| Round-based (fashion, party, deduction) | One short round with a theme and a timer | 1 + 6 (spectate mid-round); a practice loop in the lobby | A first round nobody is eliminated from early | Voting weight, shops, ranks | A wait or team pick before the first round (one hide-and-hunt game lost 28% there); a blank page with the whole catalogue (one fashion game lost 56% between entering the first dress-up round and reaching the runway) `[community]` |

By minute five in any genre: three loop closures, a number that went up, one real choice, one purchase that changed the verb, a glimpse of the long loop, one designed moment of joy, and the next goal in hand `[lihfolk]`.

## 11. Anti-patterns, with evidence

| Anti-pattern | Evidence | Do instead |
|---|---|---|
| Text wall or dialogue chain before play | Children skipped lengthy explanations on Roblox (NN/g); "players generally don't like to read instructions and skip through text prompts" `[official]`; ten minutes of next-screen text, half forgotten (Adams) | §7; one picture sign; teach by the first rep |
| Unskippable or forced sequence | No gain from blocking in any of three games (Andersen); forum replies to a "players leave during my tutorial" thread: make it optional `[community]` | Soft gate; skip from step 2; adaptive hints |
| Tutorial in a separate place, solo, by teleport | "Massive drop in session time and D1" on one shooter; a second developer reverted `[community]` | Teach in the main place beside other players; sandbox opt-in |
| Cutscene before control | A polished 27 s intro sat inside the bounce window and was disabled `[lihfolk]` | Control first; any scene under 5 s and skippable |
| Tutorial that differs from the real game | A mobile racing teardown: the hand-held start is followed by unexplained progression screens (Luban); "after the tutorial I felt confused on what to do" `[community]` | Real systems, real UI, real numbers; only safety is special; end on a real goal |
| Offers or social prompts during onboarding | Children cannot tell promotions from content (NN/g); "the immediate popup to favorite the game and invite friends is also incredibly annoying" `[community]` | The pop-up gate in §8 (house rule 3) |
| Fake choice | A push-button tutorial with no alternative is the dullest start (Luban) `[community]` | A choice offered in the first 3 minutes changes something visible; if the outcome must be safe, narrow the real options (a starter egg with two possible pets) rather than faking the pick |
| A step that cannot be completed | An unaffordable purchase step `[community]`; a step whose dependency was switched off `[lihfolk]` | `topUpTo`; kill-switch tests |
| Every system and the whole HUD at spawn | "I saw a lot of GUI that made me feel overwhelmed" `[community]`; Fan: spread the teaching out | HUD reveal; contextual steps |
| Guidance nobody can see | White beam on snow; red highlight on red crates; a beam and message box that players walked past `[community]` | Two-tone cues tested on the lightest and darkest ground; move the target into view |
| Losing the tutorial, or being punished in it | "If the player fails at the tutorial, then clearly the tutorial itself has failed" (Adams) | Safe steps; instant retry |
| Patronising praise | Adams; interview study of players' tutorial complaints (Hedges) `[community]` | Reward with the game's own feedback |
| A help menu as the only teaching | In one game 31% opened it and progress fell 12% (Andersen) | In-context cues; a Tips page as a supplement |
| Noise: many pulses, a pointer that never leaves | Players tune out repeated messages (Fan) | One pulse; pointers appear on stall and leave on progress |

## 12. Case study: five versions of one tutorial in two weeks `[lihfolk]`

| Version | Shape | What happened | Change |
|---|---|---|---|
| A | 27 s first-person intro cutscene, then tips | Sat inside the bounce window | Cutscene disabled |
| B | 11 steps: combat, dash, heal, elite, forge; first roll guaranteed Rare | 7-day funnel lost 31% at the fight, 34% at the forge, 82% at the elite. One step could never complete because its system had been switched off | Cut hard |
| C | 3 hub steps, no combat, 16–18 s | Fast, but the non-obvious economy was never taught | Rebuilt around the hidden loop |
| D | 7 steps: roll, equip, roll again, salvage the weaker item, forge, open quests, claim a quest; a real daily quest is seeded so the forge step completes it | Ends on a real payout and teaches quests by paying | Players still felt "thrown in" afterwards |
| E | D plus one short safe combat step and a 35-goal chain read from the save | Direction continues after "complete" | Kept |

Lessons: teach on safe ground first; teach what players will not find alone, not the obvious verb; finish on a real goal; give the tutorial a successor; re-test every step after each update. Open question from the same project: a great first pull reads as generous but shows the top of the early ladder too soon. They moved from Rare-first to Common-first without measuring; test it.

## 13. Tutorial critique rubric

Score 0–2 per row from a screen recording of a fresh account on a phone. Pass at 16 of 20 with no zero in rows 1, 5 or 8.

| # | Criterion | 2 | 1 | 0 |
|---|---|---|---|---|
| 1 | Time to first verb | 15 s or less from control | 30 s or less | Later, or a menu or scene comes first |
| 2 | Words | Never over 8 on screen; nothing to read before the verb | One longer screen | Text wall or dialogue chain |
| 3 | Do, not read | Every step completes by a real action | One "tap to continue" step | Click-through slides |
| 4 | One thing at a time | One pointer, one pulse, at most three concepts by minute 2 | Brief overlap | Full HUD and several pulses at spawn |
| 5 | Guidance can be seen | Every cue reads on light and dark ground at 667×375; colour, shape and word | One weak cue | A cue testers walk past |
| 6 | Adaptive | Hints only after a stall; none for players who act | Fixed delay, short | Hints for everyone, or none |
| 7 | The real game | Same place, real systems, friends can join | Minor differences | Separate solo place, or numbers the real game does not have |
| 8 | Cannot fail or stick | Every step completable; purchases affordable; fights safe | One fragile step | A step that can be lost or cannot complete |
| 9 | Skip, resume, never replay | Skip pays; rejoin resumes; returners untouched | Skip exists, pays nothing | Forced, or replays for returners |
| 10 | Ends on a real goal | Last step is a real payout, a designed joy moment, and the next goal on screen | Goal shown, no payoff | "Tutorial complete" and nothing |

## 14. Procedure: repair a live game's onboarding from its funnel

1. **No funnel yet:** ship instrumentation only (§9) and change nothing else. Wait for 7 days or about 1,000 new players `[house]`.
2. **Baseline:** per-step conversion, completion, hint and skip rates, both bounce windows, the minute of the steepest fall on the first-session curve, D1 by source, all split by platform.
3. **Play it:** fresh account, 3 GB phone, stopwatch, recording. Score §13. Watch three to five fresh players; test 6–8-year-olds in pairs, which NN/g found works best for that age `[community]`.
4. **Pick one step:** the earliest that loses twice its neighbours. If the largest loss is join → step 2, it is arrival; go to design-foundations.md §7.2 first.
5. **Classify** with the §9 table: confusion, tedium, blockage, UI depth, difficulty.
6. **Choose the cheapest fix that could work,** in this order: delete the step; move it later; make the target visible (icon over it, move it into the line of sight); rewrite the words; add a timed hint; rebuild the step. Prefer fixes that are high-impact, cheap and reusable, and ship them ahead of content `[official]`.
7. **One change per release.** New funnel version if steps moved. Annotate the date.
8. **Read by first-play cohort:** the step's conversion should move within days `[official]`; bounce next; D1 last. Under about 1,000 DAU use the small-game protocol in core-loop-tuning.md §7.
9. **With traffic, run it as an experiment:** goal metric is per-user funnel conversion on the last onboarding step; D1 and playtime are guardrails. A funnel that improves while D1 stays flat means the step was fixed and the loop was not `[official]`.
10. **Repeat** until no step loses twice its neighbours. If D1 is still low, the problem is the loop: core-loop-tuning.md §5–6.

## 15. Level-up: symptom → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Under-60 s bounce high, the tutorial barely starts | Arrival, or a tutorial "thrown in the player's face" | Control first; first verb before any panel (core-loop-tuning.md §6, first row) |
| Players stand at spawn for minutes, then leave | No visible first action; text at the start | One prompt, one cue; cut the opening text |
| Completion fine, session short | The tutorial teaches the obvious and ends in a dead end | Successor goal chain; teach the hidden step |
| Completion low, skip rate high | Too long or tedious | Cut to the verbs players do not find alone. Reported: D1 6% → 15% when 5 steps became 3 `[community]` |
| High hint rate on one step | Objective or target unclear `[lihfolk]` | Eight words; pointer on the exact target; step conversion back to 90%+ |
| Drop at the first purchase | Unaffordable, or too many taps | `topUpTo`; open the shop on the item |
| Session time fell after a tutorial was added | Forced, solo or teleported teaching | Fold it into the main game as contextual tips |
| Phone completion far below PC | Cue off-screen, under a thumb, or too small | §6; test at 667×375 |
| Returners leave early in session 2 | The tutorial replayed, or the HUD reset | Saved `done`; reveal from the profile |
| Veterans complain, new players are lost | One path for both | `whenStuck` hints, `isComplete`, skip |
| "I don't know what to do" in feedback after the tutorial | No next goal | design-foundations.md §7.3 |
| A step's conversion fell the day an update shipped | A dependency changed | Run the test matrix; roll back |

## Review gate

- [ ] First-minute script written as beats, built as written, timed on a 3 GB Android phone: verb by 15 s, reward by 30 s, upgrade by 2 min.
- [ ] Highest teaching pattern that works is used; nothing forced, solo or teleported; any sandbox is opt-in.
- [ ] No screen over 8 words; no reading before the first verb; every instruction has an icon or a pointer; device-true prompts.
- [ ] One pointer and one pulse at a time; every cue passes the light-ground and dark-ground check at 667×375 and has a reduced-motion form; 3D guidance objects are Blender meshes and cue textures are designed, not generated.
- [ ] Steps are server-owned data saved by id; each reward pays once; skip pays the rest; rejoin resumes; returners never see it again.
- [ ] Every step is completable: purchases topped up, fights safe, test matrix passed. No automatic pop-up, offer or social prompt during onboarding.
- [ ] Funnel, `TutorialHint`, `TutorialSkip` and `FtueBeat` live in a published test place; funnel versioned when steps moved; release dates annotated.
- [ ] The last step is a real payout, and a next goal is on screen afterwards.
- [ ] Rubric scored at 16 or more with no zero in rows 1, 5, 8. Live game: the earliest weak step is named with its chart, one change shipped, cohorts compared.

## Sources

Accessed 2026-11-11. "(read)" = opened and read; "(viewed)" = image downloaded and looked at; "(oembed)" = video existence and author verified, not watched; "(search summary)" = seen only through search result text. Full annotated list with image links: visual-library/tutorials-and-onboarding.md.

- Roblox/creator-docs at commit ccc2b01 (2026-11-07), https://github.com/Roblox/creator-docs/tree/main/content/en-us/ (read): `production/game-design/onboarding.md`, `onboarding-techniques.md`, `design-for-roblox.md`, `ui-ux-design.md`; `production/analytics/funnel-events.md`, `journey-events.md`; `production/experiments.md`; `production/publishing/accessibility.md`; `resources/plant-reference-project.md`; `education/build-it-play-it-mansion-of-wonder/connect-the-beam.md`, `adding-scripts.md`; `reference/engine/classes/` `AnalyticsService.yaml`, `Highlight.yaml`, `Beam.yaml`, `ProximityPrompt.yaml`, `GuiService.yaml`, `UserInputService.yaml`, `InputActionLabel.yaml`, `Camera.yaml`. Images from the onboarding-techniques, onboarding and funnel pages (viewed, 15).
- Staff posts (read): https://devforum.roblox.com/t/improving-onboarding-through-funnel-events/3064458 (causes of drop-off; Plant and Feline Fishing Fun funnels viewed); https://devforum.roblox.com/t/analytics-understand-complex-player-funnels-with-journeys/4973876 (chart viewed); https://devforum.roblox.com/t/studio-beta-no-code-hotkey-hints-with-inputactionlabel/4779420
- https://devforum.roblox.com/t/improving-onboarding-for-our-zombie-shooter/3323657 and https://devforum.roblox.com/t/low-session-time-specifically-for-phone-and-tablet/3507382 (read; teleport tutorial result; funnel viewed: 73% lost at the first weapon purchase)
- https://devforum.roblox.com/t/the-age-old-question-what-makes-people-leave-this-after-30-seconds/3969002 and https://devforum.roblox.com/t/my-onboarding-analytics-seem-ridiculously-bad/4003426 (read; funnel and screenshots viewed: 16% and 34% losses, white line on snow, separate-place revert)
- https://devforum.roblox.com/t/why-the-players-are-so-confused-in-my-game/3885660 (read; screenshot viewed), https://devforum.roblox.com/t/why-is-my-games-d1-retention-so-low-feedback-needed/4840487 (read; unaffordable step), https://devforum.roblox.com/t/players-leaving-during-tutorial-feedback-needed/3147818 (read), https://devforum.roblox.com/t/need-feedback-mainly-core-loop-ftue-and-retention/4773215 (read; funnel viewed: 75% completion, survival steps), https://devforum.roblox.com/t/looking-for-feedback-50-of-players-leave-within-the-first-minute/4852812 (read; funnel viewed), https://devforum.roblox.com/t/feedback-on-ftue-and-quest-system/485833 (read; image viewed), https://devforum.roblox.com/t/help-with-improving-player-onboarding-and-uuqptr/3554178 (read; funnel viewed)
- https://devforum.roblox.com/t/spotlightui-guided-focus-module/4267581 and https://github.com/Vvshenok/SpotlightUI (read; MIT; mask technique)
- Andersen, O'Rourke, Liu, Snider, Lowdermilk, Truong, Cooper, Popović, "The Impact of Tutorials on Games of Varying Complexity", CHI 2012, https://grail.cs.washington.edu/projects/game-abtesting/chi2012/ (paper read)
- Nielsen and Sherwin, "Children's UX: Usability Issues in Designing for Young People", Nielsen Norman Group, 2019, https://www.nngroup.com/articles/childrens-websites-usability-issues/ (read)
- Curtis, "GDC 2012: 10 tutorial tips from Plants vs. Zombies creator George Fan", https://www.gamedeveloper.com/design/gdc-2012-10-tutorial-tips-from-i-plants-vs-zombies-i-creator-george-fan (read); talk video https://www.youtube.com/watch?v=fbzhHSexzpY (oembed)
- gamedeveloper.com (read): Graner Ray, "Tutorials: Learning To Play", 2010, https://www.gamedeveloper.com/design/tutorials-learning-to-play; Adams, "Eight Ways To Make a Bad Tutorial", 2011, https://www.gamedeveloper.com/design/the-designer-s-notebook-eight-ways-to-make-a-bad-tutorial; Nutt, "The Structure of Fun: Learning from Super Mario 3D Land's Director", 2012, https://www.gamedeveloper.com/design/the-structure-of-fun-learning-from-i-super-mario-3d-land-i-s-director; Luban, "Best practices for a successful FTUE", 2020, and "Mario Kart Tour: Gameplay: 1 - Onboarding: 0", 2019; Hedges, "Video Game Tutorials: How Do They Teach?", 2017 (read in part)
- https://reddit.sentinel-team.org/subreddits/robloxgamedev/snapshots/2026-04-03T05%3A12%3A52.21453Z (search summary of r/robloxgamedev posts via a third-party mirror, not opened; the 6% → 15% case)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/lihfolk-tutorial/SKILL.md` and its `references/ftue-checklist.md`, `references/step-design-patterns.md`; `LihFolk Vault V2/10 Game Design and Genres/First-Time User Experience and Onboarding.md`, `…/Onboarding by Genre - The First Five Minutes.md`; `…/11 Monetization Publishing and Live Ops/Measuring Onboarding - Funnels, Drop-off and A-B Tests.md`; `…/42 Accessibility and Inclusive Design/Onboarding Accessibility and Cross-Device Prompts.md` (read). Ideas adapted and rewritten; no code or text copied.
