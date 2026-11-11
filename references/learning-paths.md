# Learning paths: detect the developer's level, adapt, and route

How Claude works out whether it is helping a beginner, an intermediate or an expert Roblox developer, how the answer changes for each, and the path each one follows: a first hour to first shipped game on-ramp, a ladder from "working" to "good", and the tracks for scaling a live game. Open it at the start of any session where the developer's level is unknown, whenever an answer lands too basic or too advanced, when someone asks "where do I start" or "what should I learn next", and when sizing a project to a time budget. Terms are defined in `references/glossary.md`; Studio mechanics in `references/studio-workflow.md`. Tags: `[official]` creator docs, `[community]` forum, Reddit and blog practice, `[lihfolk]` adapted from LihFolk Vault V2, `[house]`, `[VS]` version-sensitive.

## Start here by level

| Reader | Read | Skip |
|---|---|---|
| Beginner (never shipped a game) | Section 3: first hour, first day, first week, the tiny project, the first kit, "Make it your game", the ten mistakes; the under-16 box if it applies | Sections 4 and 5 until the first game is public |
| Intermediate (a game works, it is not yet good) | Section 4 ladder, top to bottom; section 8 to size the next milestone | The beginner path, except the ten mistakes as a self-check |
| Expert (live game, team or revenue) | Section 5 tracks; section 7 for team shape; section 6 as an index | Everything else |
| Claude | Sections 1 and 2 before the first answer, then the reader's section | — |

## Contents

1. Detect the level · 2. Adapt the answer · 3. Beginner path · 4. Intermediate ladder · 5. Expert tracks · 6. Which reference do I open · 7. Solo, small team, studio · 8. Scope by time budget · 9. Level-up table

## 1. Detect the level

Read the evidence before asking. Level is per domain: rate code, art, design, production and platform knowledge separately. A senior Unity engineer is an expert programmer and a Roblox platform beginner; a builder with 200 hours in Blender may never have written a RemoteEvent.

| Signal | Beginner | Intermediate | Expert |
|---|---|---|---|
| How they ask | "How do I make a game", "it doesn't work", "where do I put this script" | "Is this the right way", "how do I stop exploiters", "why is retention low" | Narrow and comparative: "ProfileStore session steal vs MemoryStore lock for cross-place trades" |
| Vocabulary | "Code", "free models", no client/server distinction | Knows RemoteEvent, DataStore, ModuleScript; hazy on numbers and limits | Uses CCU, D1/D7, ARPDAU, PTR, sink ratio, heartbeat, names libraries and versions |
| Evidence they bring | A screenshot, one pasted script, no Output text | A place or repo, a described bug, some analytics | Profiler captures, dashboards, an experiment result, a diff |
| Code shape | One Script per Part, `wait()` and `while true do`, `LocalPlayer` in a server Script, a remote that carries the amount to grant | ModuleScripts, hand-rolled DataStore with `pcall`, partial validation, mixed old and new APIs | `--!strict`, single entry points, tagged components, ProfileStore, tests |
| Project files | A place only, or one `.rbxl` | Place plus some notes; maybe git | `default.project.json`, `rokit.toml`, `wally.toml`, CI workflows, docs folder |
| Place contents | Toolbox models, primitive Parts, scripts inside models, pixel-offset UI | Organised folders, some packages, a shop | Dev and live universes, Configs, several places, an asset manifest |
| Goal | Finish something; learn | Make the game hold players and earn | Scale, de-risk, delegate |

With Studio MCP or repo access, measure instead of guessing (read-only; sketch F in engineering-architecture.md gives these counts): number of scripts and how many sit inside Workspace models; share of scripts with `--!strict`; hits for `wait(`, `spawn(`, `LoadAnimation`, `SetAsync`; RemoteEvents versus server handlers that validate; whether a `ProcessReceipt` exists and deduplicates.

Rules `[house]`:

- Unknown level: answer at intermediate depth with terms defined in a clause, and add one calibrating question that also moves the work forward ("Is the code in Rojo files, or edited only in Studio?"). Never open with "what is your skill level?".
- Re-rate on every message. One expert-shaped question after three beginner ones usually means a pasted tutorial, not a new level.
- Never label the person ("since you are a beginner"). Adjust silently.
- Do not assume an adult with a budget. Creators can be children (the Team Create docs define age bands from under 9 upwards `[official]`): plain words, the free route first, no assumption of money for ads, plugins or contractors.
- When the stated level and the evidence disagree, trust the evidence for safety decisions and the person for tone.

## 2. Adapt the answer

| Dimension | Beginner | Intermediate | Expert |
|---|---|---|---|
| Tone | Encouraging, concrete, no jargon without a definition | Direct; name the failure each rule prevents | Terse; conclusions first |
| Scope of one answer | One concept, one next step, one thing to check | The system and its neighbours | The decision, the trade-offs, the edge cases |
| Explanation | What it does, where it goes, what you will see in Output | Why this pattern and what breaks without it | Only what is non-obvious; numbers, limits, `[VS]` flags |
| Code | A whole script, the exact container it lives in, how to test it with `F5` | Modules and diffs against their structure | Sketches, interfaces, invariants; they write the rest |
| Tooling | Studio-native: Script Editor, Save with Notes, Device Simulator. No Rojo, Wally or CI unless asked | Script Sync plus git, then Rojo; Selene and StyLua; a dev universe | Full toolchain, CI-only publishing, experiments, headless tests |
| Studio MCP | Claude makes the edit with `multi_edit`, shows it, and has the user press Play and read Output back | Claude audits read-only, proposes, edits behind a named save | Claude runs measured audits and batch fix-ups; the user reviews diffs and numbers |
| Design process | Half of `templates/game-one-pager.md`; no GDD | One-pager, economy sheet, event plan | All templates, experiment plans, audit report |
| Choices | Make the choice, say why in one line | Recommend one, mention the bolder option | Lower-risk and bold options with costs; state which you would pick |
| Numbers | Two or three that matter (first reward under 30 s; test on a phone) | Budgets and gates from the references | Benchmarks with source and date; ask for theirs |
| Pushback | On scope and on unsafe shortcuts only | On architecture debt and missing measurement | On weak evidence and unfalsifiable plans |

What never changes with level `[house]`: the server decides currency, damage, inventory and purchases; published saves use session-locked storage inside `pcall`; receipts are idempotent; policy rules apply; the three house rules apply; no deprecated APIs. Simplify the explanation, never the safety. For a beginner that means handing over the safe pattern as a ready module with three lines of explanation, not teaching the unsafe short version first.

Worked example, "how do I save the player's coins?":

- Beginner: "Saving goes wrong in ways that lose progress, so use the ProfileStore module instead of writing it by hand. Put this ModuleScript in ServerScriptService, this 25-line Script next to it, press `F5`, collect coins, stop, play again: the number should still be there. Saving in Studio only works after you switch on Studio API access in a test game." One next step: test by rejoining.
- Intermediate: the DataService shape in data-and-purchases.md: template, schema version, migrations before `Reconcile`, what happens when the load fails, the shutdown test, and why their `SetAsync` in `PlayerRemoving` loses data on server close.
- Expert: "ProfileStore; cost is one write per profile per auto-save interval. Risks at your scale: write budget under mass rejoin after a restart, 4 MB key ceiling on inventories, cross-place handoff. Measure `GetRequestBudgetForRequestType` during a restart drill. Bold option: split cold data into a second key."

With AI assistance generally `[community]`: the DevForum and Reddit threads found in this pass both say a developer must know enough Luau to catch the assistant's mistakes (two threads: a heuristic, not a survey). So for beginners Claude always states how to verify (what to press, what Output should print) and asks for the result, and never reports a change as working when it was only written.

## 3. Beginner path

Promise: a small, public, saved, phone-tested game in about four weeks of evenings. The route follows Roblox's own "Create your first game" tutorial (a 3D platformer where coins buy jump power `[official]`) with the house rules added.

### Before the first hour

Install Studio (free; Windows or macOS; 3 GB RAM minimum, 8 GB recommended `[official]`) and do the four "First hour" steps in studio-workflow.md section 1 (not the full settings table). The age check can wait until you want to release or to work with someone else: public release and Team Create with other people both require it `[official]` `[VS]`.

No Blender yet? Install it now (free, blender.org) and leave it closed for the first hour: the first hour is Studio only. In the first Blender session, on day one, learn three things and nothing else:

1. Moving around: middle mouse to orbit, `Shift` + middle mouse to pan, wheel to zoom, numpad `1` / `3` / `7` for front, side and top views.
2. Editing a cube: `Tab` into Edit Mode; `G`, `S`, `R` to move, scale and rotate; `E` to extrude a face; `Ctrl R` to add a loop cut.
3. Finishing a shape: add a Bevel modifier, then Object > Apply > All Transforms (`Ctrl A`).

Those three are enough to make the crate in `references/blender-modeling-craft.md`, "First kit walkthrough (beginner)".

### If you are under 16 (or under 13)

Plenty of Roblox developers started at your age, and nothing below stops you from building, testing and sharing a game. It only changes who can see it at first, and it means a parent or guardian should be part of anything involving money or other people. All of this is `[official]` from the creator docs as mirrored on 2026-11-07 and `[VS]`: rules in this area changed several times in 2026, so check the current page with a parent before relying on it.

| Question | What the docs say |
|---|---|
| Can I use Studio and make a game? | Yes. Studio itself has no age check; building, testing and saving are open to everyone |
| Can I publish? | Saving and publishing to your own account keeps the game private to you. Releasing it to other people requires you, the creator, to complete an age check (facial age estimation or ID; government-ID verification is 13+ only). The docs read here state no minimum age for releasing a game, and do not say whether a creator under 13 needs a parent's consent for the age check: ask a parent and check the help centre |
| Who can play it before a public release? | Up to 10 early testers (File > Invite early testers). By your age: 9–12 may invite ages 9–15; 13–15 may invite ages 9–17; trusted friends of any age can also be invited (under-9 testers need a parent's approval). Studio asks you to complete the age check when you send the first invite. The docs list no early-tester option for creators under 9. This is the easiest way to get classmates into a first game |
| Who can play after a basic public release? | Players who are age-checked 16 or older, and your trusted friends. So your own friends under 16 will not find the game publicly yet unless they are trusted friends or early testers. That is normal for every new game, not a penalty for your age |
| How does a game reach players under 16? | Verification of your account (facial age estimation is the route for creators under 18), 2-step verification, the full maturity questionnaire, and either a Roblox Plus or Premium subscription held for 2 months or a one-time refundable fee of 1,000 Robux; then the game must collect 250 unique plays from "highly engaged", age-checked 16+ players within 60 days. A first learning game does not need this. Do not pay the fee or buy a subscription for it without a parent deciding with you |
| Can I work with a friend in Team Create? | Both of you need an age check. By default you can share a session only with compatible ages: under 9 with under 13; 9–12 with under 16; 13–15 with ages 9–17. Someone outside your band must be a trusted friend, or a linked parent must allow it in parental controls. Trusted-friend requests from under-13 accounts need a parent's approval |
| Can I earn money? | Cashing out through DevEx requires being at least 13 and having 30,000 earned Robux, plus tax forms and your legal name. Treat money as a later, parent-involved step (`references/team-business-legal.md`) |

How Claude handles this `[house]`: never ask a young developer to spend Robux or real money, never suggest working with strangers found online, keep contact with collaborators in channels a parent can see (`references/community-moderation-safety.md`), and say plainly when the docs do not answer a question instead of guessing.

### First hour: something moves because of your code

1. New place from the Baseplate template. Fly the camera (`W A S D`, right mouse to look, `F` to focus). Find Explorer, Properties and Output.
2. Insert a Script into ServerScriptService that prints, then one that changes a Part's colour every second with `task.wait(1)`.
3. Play (`F5`), stop (`Shift F5`), and flip the Client/Server toggle to see that there are two worlds.
4. File > Save to Roblox, so the place lives in the cloud.

This place is practice: primitive Parts are fine here because it is never published `[house]`.

### First day: the four ideas everything else stands on

| Idea | Do | You have it when |
|---|---|---|
| Luau basics | Variables, functions, tables, `if`, `for`, events with `:Connect`. The official coding fundamentals pages are enough | You can read a 30-line script aloud and say what each line does |
| Client and server | A LocalScript in StarterPlayerScripts fires one RemoteEvent; a Script in ServerScriptService answers. The client asks, the server decides | You can say which machine runs each script and why a coin count must live on the server |
| The art pipeline in miniature | Make the crate from the first kit walkthrough in blender-modeling-craft.md, export it, import it with the 3D Importer, set its collision | A mesh you made is in the place and you can stand on it |
| Saving your work | Save to Roblox with Notes (`Ctrl Alt S`) before anything risky; never edit during a playtest | You have restored one old version on purpose, once |

### First week: the tiny project, "Coin Dash" (about 10 hours)

One verb (run and jump to collect), one progression axis (coins buy jump height or speed), one goal (reach the top platform). Write the top half of `templates/game-one-pager.md` first: pitch, fantasy, the loop in one sentence, what the first 60 seconds look like.

| Piece | Smallest correct version | Reference |
|---|---|---|
| World | One arena, about 100 × 100 studs, built only from the first kit below; SpawnLocation hidden under a kit piece | blender-modeling-craft.md |
| Coins | Models tagged `Coin`, one server script (sketch below), respawn after 5 s | performance.md (spatial queries, later) |
| Upgrades | Two pads. The client sends "buy jump"; the server checks the price, subtracts, raises `Humanoid.JumpHeight` | networking-and-security.md |
| Saving | ProfileStore with coins and upgrade levels. Copy the module from its official repository into a ModuleScript and read it; do not insert it from the Toolbox | data-and-purchases.md |
| HUD | Coin counter and two buttons, sized with Scale not Offset, checked in the Device Simulator on an entry-level phone | ui-input-crossplatform.md |
| Feel | A sound and a small pop when a coin is collected. It changes how fun the loop reads | game-craft.md §1 (feedback tiers), audio-sfx-music.md |

```lua
--!strict
-- unexecuted sketch. Script in ServerScriptService. Each coin is a Model tagged "Coin" holding
-- the Blender mesh ("Mesh") and an invisible anchored Part "Trigger" (CanCollide off, CanTouch on).
-- Touched is acceptable only for a first coin worth 1 with the server distance check below; anything
-- valuable (damage, real rewards) uses a server spatial query, never Touched (decision-rules.md).
local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")

local COIN_VALUE = 1
local RESPAWN_SECONDS = 5
local MAX_REACH = 12 -- studs: ignore touches claimed from far away

local function connectCoin(trigger: BasePart, mesh: BasePart)
	local available = true
	trigger.Touched:Connect(function(hit: BasePart)
		if not available then
			return
		end
		local character = hit:FindFirstAncestorOfClass("Model")
		local player = character and Players:GetPlayerFromCharacter(character)
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if player and root and root:IsA("BasePart") and (root.Position - trigger.Position).Magnitude <= MAX_REACH then
			available = false
			mesh.Transparency = 1
			mesh.CanCollide = false
			local coins = player:GetAttribute("Coins")
			player:SetAttribute("Coins", (if typeof(coins) == "number" then coins else 0) + COIN_VALUE)
			task.delay(RESPAWN_SECONDS, function()
				mesh.Transparency = 0
				mesh.CanCollide = true
				available = true
			end)
		end
	end)
end

local function setUpCoin(coin: Instance)
	local trigger = coin:FindFirstChild("Trigger")
	local mesh = coin:FindFirstChild("Mesh")
	if trigger and trigger:IsA("BasePart") and mesh and mesh:IsA("BasePart") then
		connectCoin(trigger, mesh)
	end
end

for _, coin in CollectionService:GetTagged("Coin") do
	setUpCoin(coin)
end
CollectionService:GetInstanceAddedSignal("Coin"):Connect(setUpCoin)
```

What the sketch teaches: one script for all coins (tags, not a script per coin), the server grants, a distance check, `task.delay` instead of `wait`. In the real project the attribute is replaced by the saved profile value. The trigger is larger than the mesh, so the coin is collected before it is touched and nobody walks through a visible object; while hidden it does not collide.

End-of-week gate: five people who are not you play for ten minutes (three is the floor `[lihfolk]`); use File > Invite early testers, up to 10 friends `[official]`. If nobody wants a second go, change the loop now: it is the cheapest change the project will ever get.

### The first kit (how a beginner meets house rules 1 and 2)

The full step-by-step lives in `references/blender-modeling-craft.md`, "First kit walkthrough (beginner)": follow it there, not from memory. In one paragraph: set the Blender scene to Unit System None so 1 unit is 1 stud, and keep two box "avatars" (5 and 6.5 studs tall) in the file for scale. Pick six colours and use nothing else. Build four props that look like one family: a crate, a barrel, a lamp post and a fence section. Each one is a simple shape with one narrow bevel (0.08 studs, the same on every piece), smooth shading, bottom faces deleted, origin at the bottom centre (or the snapping end for the fence), and a `Fidelity` property of `Box` or `Hull` that becomes its collision. Check each as a small black silhouette before adding detail, export with the kit script, import with the preset in art-pipeline-blender.md, then walk into every piece and jump on it in a playtest. Nothing visible may be walk-through, and static pieces are anchored.

Coin Dash needs three more pieces made the same way, with the same bevel and palette: a floor tile (8 × 8 studs), a platform (4 × 4) and the coin. Duplicate placed copies with `Ctrl D` instead of importing a piece twice. If the export script is not set up yet, Blender's File > Export > glTF 2.0 (selected objects, modifiers applied) is an acceptable stand-in for a first import `[house]`; move to the script before the kit grows.

Budget for it `[house]`: assume 30 to 60 minutes per simple piece until you have timed your first three, then re-plan. The art volume, not the code, is what sinks a first project under the Blender rule.

A creature (a pet, a dragon, an enemy) is the same skill with stricter limits for a first game:

- **Shape language first.** Friendly reads as round: a big head, a small bottom-heavy body, no neck, large eyes set low. A dragon is that plus three signature shapes: two horns, two small wings, a tail with a spike. Design it to read from behind and above, because that is where the camera sees a pet (blender-modeling-craft.md, "Cute pet").
- **A few boxes and wedges, in Blender.** Body, head, snout, two wings, tail, four stubby legs: about ten bevelled shapes joined into one mesh with one material from the palette. No sculpting, no textures.
- **No rig and no animation at first.** The pet is one rigid mesh. It looks alive from motion you code: it follows, bobs up and down on a sine wave, and turns to face where it is going.
- **Follow on the client.** The server only records which pet a player has equipped. Each player's device moves the pet models itself, anchored and without physics, in one loop for all pets (gameplay-systems-cookbook.md §4). Do not build pets as server-side physics objects: they jitter and cost every player.
- **Variants, not new models.** Four or five dragons are one base mesh with a different palette entry and one changed outline feature each (bigger horns, a crest, wider wings), so rarer ones are recognisable by shape.
- **Later:** flapping wings, a walk cycle or a skinned body are the next step, in `references/animation-and-rigs.md`.

### Make it your game

Coin Dash is scaffolding. Almost nobody wants to make a coin platformer: they want a pet simulator, a tycoon, an obby, a horror game. Once the coin loop works, turn it into the game the developer came for.

The market gate does not apply here. Phase 1 of `workflow-phases.md` (one new verb, market position, saturation) is for games built to grow and earn. A first game is built to be finished. Claude never tells a beginner their idea is saturated, has been done, or will not get players; it helps them find the smallest version of exactly that idea. Market advice is given only when the developer asks how to get players or says income is the goal.

Method:

1. Open the matching file in `references/genres/`. Read only the Beginner row of "Start here by level": "Do first" is the scope, "Leave for later" is the postpone list. Do not read the monetisation or live-game sections yet.
2. Map what already exists: the coin becomes the genre's resource, the upgrade pad becomes its first thing to spend on, the arena becomes its first area. Nothing built in week 1 is thrown away.
3. Take "Systems to build, in order" from the same file. The first three to five items, up to wherever the Beginner row stops, are weeks 2 and 3: one system per sitting, each ending in a playtest. Their how-to is in gameplay-systems-cookbook.md.
4. Count the art before promising anything: pieces × 30–60 minutes.
5. Week 4 stays the same: test with people, release, fix the top three problems.

Worked example: "a pet simulator with dragons" (`genres/pet-collection-hatching.md`).

| Question | Answer |
|---|---|
| Smallest honest version | One small island. Walk around collecting gems. Spend gems at one egg. The egg hatches one of four or five dragons, chosen on the server from a weight table, with the odds shown on the egg from that same table. Your best dragon follows you and multiplies the gems you collect. Everything saves. That is a real pet simulator loop: collect, hatch, get stronger, collect faster |
| From Coin Dash | Coins → gems (same script, new mesh). Upgrade pads → the egg stand. Jump upgrade → the dragon's gem multiplier |
| Week 2 systems (genre list 1–3) | The roll table module on the server; the egg stand and hatch flow with a reveal the player can skip; a pet inventory (stacked counts) with an "equip best" button, saved in the profile |
| Week 3 systems (genre list 4–5) | Dragons following on every client; the odds panel. The `PolicyService` gate in item 5 matters only once an egg can be bought with Robux, which this version does not have |
| Art to make | The six kit pieces (four props, floor tile, platform), a gem, an egg, an egg stand, one dragon base mesh and four variants of it: 14 pieces, so roughly 7 to 14 hours `[house]`. It is the largest item in the plan; start it in week 1 |
| Postpone (the genre file's "Leave for later") | Eggs bought with Robux, luck boosts, mutations and merge machines, trading, multi-hatch, seasonal eggs; also a second island, rebirth, an index, and animated or rigged dragons |
| Done when | A friend can join, hatch a dragon within the first two minutes, come back the next day and still have it |

### First shipped game: weeks 2 to 4

| Week | Goal | Must be true at the end |
|---|---|---|
| 2 | The genre's first systems work, and nothing earned can be lost or duplicated | Systems 1–3 from "Make it your game" are playable; the save survives leave-and-rejoin and a server shutdown; every remote checks type, range and rate on the server |
| 3 | It looks like a game and lasts 30 to 60 minutes | The remaining beginner systems; one style, one lighting preset; icon and three thumbnails drafted on day one of the week, not launch night `[lihfolk]` (Studio-only route: icons-thumbnails-and-store-page.md §8 route A); maturity questionnaire done; played on a real phone |
| 4 | Other people play it | Early testers first, then a public release. A new game is shown to players who are age-checked 16 or older and to your trusted friends: that describes the audience, not you, and it is the same for a creator of any age `[official]` `[VS]`. Reaching younger players is a later, optional step with its own requirements (the under-16 box above; analytics-and-discovery.md). Fix the top three problems and nothing else; write a one-page postmortem |

Shipped means: released; a save verified by rejoining; played on a phone; five people who are not you have played. Never cut: data safety, server validation, the phone layout, the maturity questionnaire `[lihfolk]`.

Optional stretch, only after people come back for a second session: one game pass or developer product. A first learning game does not need to sell anything, and the house rule about pushing microtransactions is for games built to earn. If the developer wants to learn purchases: one `ProcessReceipt` with `PurchaseId` deduplication (data-and-purchases.md), the offer rules in monetization-and-policy.md, and testing with Studio's test purchases, which the prompt itself labels as not charged `[lihfolk]` `[community]`. Claude never tells a minor to spend Robux or real money to test; confirming a real purchase in the live game is something an adult developer does, or a parent does with them.

### Ignore for now

Rojo, Wally and CI; frameworks and ECS; Parallel Luau; MemoryStore, MessagingService and multi-place universes; trading and gifting; custom character controllers and rigs; PBR texture sets; experiments, season passes and event calendars; ads and creator deals; subscriptions. None of them makes a first loop fun, and each has a reference when its turn comes.

### The ten mistakes that cost beginners the most

| # | Mistake | Why it costs | Do instead |
|---|---|---|---|
| 1 | Starting with the dream game (open-world RPG, battlegrounds, big simulator) `[community]` | Months of work, nothing playable; one DevForum postmortem describes two years for about 13K visits | The tiny project, then a 4-week game. A list with "etc." in it is an Ocean (process-and-playtesting.md) |
| 2 | Tutorial collecting and pasting code that is not understood `[community]` | Nothing transfers; the first bug is a wall | One resource per task; type it; change one thing and predict the result before pressing Play |
| 3 | Trusting the client: a remote like "GiveCoins(100)" | The first exploiter sets their own currency | The client sends intent; the server computes and checks (networking-and-security.md) |
| 4 | Scripts in the wrong place: a LocalScript in Workspace does nothing and prints no error; server logic in ReplicatedStorage is readable by every player `[community]` `[official]` | Hours lost to "no error but nothing happens" | Server code in ServerScriptService, client code in StarterPlayerScripts, shared modules in ReplicatedStorage |
| 5 | Hand-rolled saving: `SetAsync` on leave, no `pcall`, tested only in Studio | Silent data loss on server shutdown; wiped saves after one failed load | ProfileStore; test by rejoining and by shutting the server down |
| 6 | Free models and unvetted plugins `[official]` `[community]` | Backdoors, obfuscated scripts, a generic look. The docs themselves tell you to inspect scripts in assets you did not create | House rule: nothing from the Toolbox ships. Read every plugin's permissions |
| 7 | Testing only alone on a PC | The game is mostly played on phones, with other people | Device Simulator and a real phone; Server & Clients with two clients (studio-workflow.md) |
| 8 | Old APIs from old tutorials and from AI output: `wait`, `spawn`, `LoadAnimation` on the Humanoid, BodyMovers | Subtle bugs; habits to unlearn | The never-do list in `decision-rules.md`; check the docs page |
| 9 | No safety net: editing during a playtest, no named saves, backup copies stored inside the place | Lost tuning, lost days, a bloated place | Named save before risky work; copy values out before Stop; backups on disk |
| 10 | Selling, advertising or polishing before the loop is fun | Paying for players who leave in a minute; passes nobody wants | Strangers first, then retention, then money. No offers in the first 10 minutes, ever |

## 4. Intermediate ladder: from a working game to a good one

Climb in order. Each rung protects the ones above it: sending players, or money, into a game that loses saves wastes both. For a game that is already live, score it with audit-existing-game.md first and start at the lowest failing rung.

| Rung | Done when | Open |
|---|---|---|
| 1. Safety net | Dev universe separate from live; named saves; code in git through Script Sync or Rojo; rollback rehearsed | studio-workflow.md |
| 2. Architecture | One server entry and one client entry; logic in modules; behaviour by tags; no scripts inside models; `--!strict` on new code | engineering-architecture.md, architecture-patterns-luau.md, `luau-mastery.md` |
| 3. Data safety | ProfileStore, schema version, tested migration; a failed load never saves; shutdown and rejoin tests pass | data-and-purchases.md |
| 4. Security | Written list of remotes; each one validated and rate-limited on the server; nothing secret in client-visible containers | networking-and-security.md |
| 5. First session and core loop | First reward under 30 s, first upgrade under 2 min; tutorial rubric 16 of 20; loop scorecard at 7 of 10 or better; five strangers observed | `tutorial-and-onboarding.md`, core-loop-tuning.md §4, design-foundations.md §7 |
| 6. Mobile and performance | 30 FPS or better on a 3 GB Android phone in the worst view; budgets table filled from MicroProfiler captures | performance.md |
| 7. UI and controls | Touch, gamepad and keyboard all complete; safe areas respected; nothing reads as default UI (UI rubric 8 of 10 per screen) | ui-input-crossplatform.md, ui-design-figma.md, `ui-screen-recipes.md`, `accessibility-and-player-qol.md` |
| 8. Analytics | Onboarding funnel and economy events firing from the server; one weekly review habit | analytics-and-discovery.md, `templates/analytics-event-plan.md` |
| 9. Economy | Balance sheet with numbers; sink ratio 0.95–1.05 modelled; costs are geometric and time-first | economy-and-progression.md, `templates/economy-balance-sheet.md` |
| 10. Monetisation | Default product set trimmed to fit; offer gate in code; receipts tested live; policy gate passed | monetization-and-policy.md, checklists.md Gate 3 |
| 11. Polish | A written style bible and no engine defaults left; juice tiers on the core verb; UI motion on tokens; mix, music and lighting preset; animation where the verb needs it | `art-direction-and-quality-bar.md`, game-craft.md, `vfx-and-juice.md`, `vfx-recipes.md`, `ui-motion-and-feedback.md`, `audio-sfx-music.md`, `animation-and-rigs.md`, `lighting-and-atmosphere.md` |
| 12. Retention and LiveOps | A reason to return tomorrow that is not a punishment; a weekly update day; a four-week plan | liveops-quests-retention.md |
| 13. Discovery and launch | Icon and thumbnails pass the store-page rubric and are tested; metadata honest; launch checklist signed; growth only after the readiness gate | `icons-thumbnails-and-store-page.md`, analytics-and-discovery.md, growth-and-marketing.md, market-scan-2026-11.md |

The usual intermediate plateau `[community]`: forum threads asking "I know the basics, what next" get the same answers: modules and structure, a data library, source control, then tooling. That is rungs 1 to 3. The step people skip is rung 5: most stalled games have adequate code and an untested first five minutes.

## 5. Expert tracks: scaling a live game

Pick by the constraint the numbers show, not by interest.

| Track | Techniques | Measure | Open |
|---|---|---|---|
| LiveOps cadence | Fixed update day; content shipped dark behind Configs; event calendar; update notes in game | Returning-player lift per update; D7 and D30 by cohort | liveops-quests-retention.md |
| Experiments | Configs plus Experiments; one variable; pre-registered success metric; early-harm watch; before/after cohorts when DAU is too low to split | Effect with interval, not a screenshot | analytics-and-discovery.md, core-loop-tuning.md §7 |
| Performance at scale | Per place-version client and server dashboards; device-class memory; streaming and SLIM tuning; captures from real low-end phones | Crash rate, P10 FPS, server heartbeat, join time | performance.md |
| Team and pipeline | Dev, staging and live universes; CI-only production publishes; ownership map; decision rights; release owner; incident runbook with kill switches | Lead time per change; rollbacks per month | engineering-architecture.md, studio-workflow.md, `team-business-legal.md` |
| Economy management | Faucet and sink telemetry; inflation index; announced rebalances with compensation; dupe and trade audits | Sink ratio, currency per DAU, price of anchor items | economy-and-progression.md |
| Multi-place universes | Hub plus world places; teleport data treated as untrusted; reserved servers; MemoryStore queues; cross-server messaging limits | Teleport failure rate; profile handoff errors | data-and-purchases.md |
| Security operations | Threat model per feature; server authority mode evaluation; honeypots; ban and alt policy; third-party code audit | Exploit reports per week; false-ban rate | networking-and-security.md |
| Growth | Ads Manager with cost-per-play caps; creators; localisation; thumbnail experiments | Qualified play-through, cost per retained player | growth-and-marketing.md, analytics-and-discovery.md |
| Community and safety | Moderation staffing; reporting flows; group and Discord operations | Response time; repeat-offender rate | `community-moderation-safety.md` |
| Business | Group ownership, payouts, contracts, DevEx, IP and licensing | Revenue per productive hour | `team-business-legal.md`, monetization-and-policy.md |
| Comparative study | Tear down a top game in the genre with a fixed template | Three borrowed patterns, one avoided mistake | `case-studies-teardowns.md`, `references/genres/` |

How Claude works with an expert: ask for the number before the opinion; give the lower-risk and the bold option with costs; flag every `[VS]` fact; propose the experiment that would settle a disagreement; keep it short.

## 6. Which reference do I open

The file map is `references/INDEX.md` (one row per job, every guide, template and visual-library file); standing rules are in `references/decision-rules.md` and the twelve build phases in `references/workflow-phases.md`. The rows below only translate the questions developers actually ask into that map. Paths are under `references/` unless they start with `templates/`.

| Question as asked | Open |
|---|---|
| What does this word mean? | glossary.md |
| What should I build? What is trending or saturated? | market-scan-2026-11.md, genre-playbooks.md, then `genres/<genre>.md` |
| Is my idea fun? How do I write it down? | design-foundations.md, process-and-playtesting.md, `templates/game-one-pager.md` |
| My game exists. What do I fix first? | audit-existing-game.md, `templates/game-audit-report.md` |
| Players leave in the first minutes | tutorial-and-onboarding.md (§14 repairs a live funnel), design-foundations.md §7 |
| Players play once and do not come back | core-loop-tuning.md §5–6, liveops-quests-retention.md |
| It looks generic, cheap or "AI-made" | art-direction-and-quality-bar.md, then the matching file in `visual-library/` |
| My UI looks like a default template | ui-design-figma.md, ui-screen-recipes.md (one screen at a time), ui-motion-and-feedback.md |
| My effects look weak; how do I build a slash, an explosion, a hatch reveal? | vfx-and-juice.md (principles), vfx-recipes.md (the build) |
| I want an intro, a boss entrance or a trailer | cutscenes-and-cinematics.md |
| Nobody clicks my game | icons-thumbnails-and-store-page.md, analytics-and-discovery.md |
| How do I build system X (inventory, quests, pets, rounds, shops)? | gameplay-systems-cookbook.md, the genre file |
| Something is broken and I cannot find why | debugging-and-testing.md, studio-workflow.md §2 |
| Which AI tools, skills and MCP servers are safe to add? | ai-toolchain-skills.md |
| Am I ready to ship? | checklists.md, `templates/launch-checklist.md` |
| Anything else (code, data, security, performance, art pipeline, audio, money, team) | The matching row of `INDEX.md` |

## 7. Solo, small team, studio

| Topic | Solo | Small team (2–6) | Studio (7+) |
|---|---|---|---|
| Ownership | Personal account is workable; move to a group before revenue matters | Group-owned from day one; least-privilege roles; two people able to publish and roll back | Group with role tiers; automation account for CI keys |
| Code | Studio-native, then Script Sync plus git | Rojo plus git with reviews; one integrator merges and releases | Rojo, CI gates, CODEOWNERS, release branches |
| Environments | One dev universe plus live | Dev and live; sandbox places for experiments | Dev, staging, live; CI is the only publisher to live |
| Art | One kit, one palette, timed pieces | A named art owner and a one-page style bible | Kit owners, package pipeline, acceptance checklist per asset |
| Decisions | Write them down anyway, with the reason | A decision-rights table: who decides, who is asked, who is told; anyone on the incident list may pull a kill switch `[lihfolk]` | Design owner per pillar; weekly planning; written briefs |
| Playtests | Five strangers per milestone | Weekly internal Team Test plus strangers | Scheduled external tests and experiments |
| Capacity `[lihfolk]` | Hours × 0.6–0.7 focus; 0.4–0.5 for evening hobby hours | Hours × 0.5–0.6 | With a live game, 0.3–0.5: LiveOps eats the rest |
| Typical failure | Spending every week in the favourite role | Everyone builds content; saves, security and analytics wait until launch week | Finished work queues behind one approver |
| AI agents | One Claude session with the Studio MCP | One agent in Studio, others on git branches | The multi-agent protocol in studio-workflow.md §10 |

Solo rotation that prevents the favourite-role trap `[lihfolk]`: give every working day one role in advance (say Monday and Tuesday for systems, Wednesday and Thursday for content, Friday for testing and community).

## 8. Scope by time budget

Capacity first: productive hours = available hours × focus factor (section 7). Add 30–50% to the sum of feature estimates for integration and testing `[lihfolk]`. Conflict: process-and-playtesting.md says to multiply gut estimates by about 3; the capacity method lands between ×2 and ×4. Use the capacity method when hours are known and ×3 when they are not; never apply both to the same number.

| Budget | Productive hours (solo) | What fits | What does not |
|---|---|---|---|
| Weekend | 10–16 | One verb, one arena from the first kit, one upgrade axis, a save, friends-only release. A mechanic slice whose only question is "is the verb fun?" | Monetisation beyond one pass, more than one zone, any custom rig |
| 4 weeks | 60–100 | One loop, one progression axis, one reason to return; a 20–40 piece kit; at most three products; 30–60 minutes of content; funnel analytics; public release. Plan in process-and-playtesting.md §6 | Trading, a second mode, quests and daily systems (first update instead), hand-built large maps, vehicles |
| 3 months | 250–300 (a part-time team of three is in the same range `[lihfolk]`) | The default product set; 2–4 hours of content plus a rebirth or meta layer; quests; one event; localisation; soft launch two to three weeks before the push; weekly update day rehearsed before launch | Open-world roleplay, battle royale, anything whose content list cannot be counted |

Rules:

- Count the content before building it: zones × (kit pieces + enemies + props) is a number, and the Blender rule makes it the binding one `[lihfolk]` `[house]`.
- Build one unit completely (a vertical slice), time it, multiply. Any other estimate is a guess `[lihfolk]`.
- Write the cut list on day 0, in order: second mode; trading and gifting; animations beyond the core verb; extra leaderboards; daily systems and codes; products beyond three `[lihfolk]`.
- Cut layers before features: fewer pets at launch, not no pets.
- A task that overruns by 2× stops for a decision: cut, simplify or move after launch `[lihfolk]`.

## 9. Level-up: symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| "I have watched dozens of tutorials and cannot build anything" | Passive learning | Section 3 tiny project; one resource per task; predict before pressing Play |
| Six months in, nothing playable | Ocean scope; no gates | Section 8; scope gate in process-and-playtesting.md; ship the smallest loop |
| "It works but I am afraid to touch it" | No safety net, no structure | Ladder rungs 1 and 2 |
| Answers from Claude feel too basic or too dense | Level misread | Re-rate with section 1; the user can simply say which domain they are strong in |
| AI-written code breaks or uses old APIs | Unverified output | State the verification step; check the docs; never-do list |
| Good code, players leave in two minutes | Rung 5 skipped | tutorial-and-onboarding.md §14, then core-loop-tuning.md §5 |
| Launched, got 200 visits, called it a flop `[community]` | No traffic plan and too little time; first-session quality unknown | analytics-and-discovery.md for the 250-play gate; fix the first session before buying traffic |
| Strong developer from another engine writes client-trusting code | Platform gap, not skill gap | Client-server model in engineering-architecture.md; data and replication rules |
| Team members overwrite each other | No ownership, shared place | studio-workflow.md §5 |
| Expert asks for a rewrite of a live game | Rebuild instinct | audit-existing-game.md: three fixes usually beat a rebuild |

## Review gate

- [ ] Level rated per domain from evidence, and re-rated when new evidence arrived; the person was never labelled.
- [ ] The answer matched the level in scope, tooling and depth, and no safety rule was simplified away.
- [ ] Beginner: one next step, the exact container for each script, and a way to verify were given; nothing from the "ignore for now" list was introduced unasked.
- [ ] Beginner project: every visible object comes from the Blender kit and collides; practice places with Parts are not published.
- [ ] First learning game: re-skinned to the genre the developer wanted using that genre file's Beginner row; the market gate was not applied and the idea was never called saturated; no purchase was required.
- [ ] Developer under 16: the audience and Team Create rules were explained from the docs with `[VS]`, gaps in the docs were named, a parent was brought in for anything involving money, and nobody was told to spend Robux.
- [ ] Intermediate: the lowest failing rung was addressed before higher ones.
- [ ] Expert: numbers were requested or cited with date; lower-risk and bold options were both stated.
- [ ] Scope was checked against productive hours, with a written cut list.
- [ ] Every routed reference exists (check against `references/INDEX.md`).

## Sources

Accessed 2026-11-10; the under-16 box, early-tester and Team Create age bands, DevEx minimums and Studio requirements were re-read on 2026-11-11 (creator-docs commit 7cbffff of 2026-11-10) and still match.

- Roblox/creator-docs, commit ccc2b01 (2026-11-07), `content/en-us/`: `tutorials/index.md` and the `tutorials/curriculums/` and `tutorials/first-experience/` listings, `studio/setup.md`, `includes/studio/system-reqs.md`, `production/publishing/{publish-games-and-places,kids-and-select,account-verification}.md`, `production/monetization/developer-exchange.md`, `projects/collaboration.md`, `projects/place-files.md`, `projects/assets/packages.md`, `ai/coding-harness.md`, `assistant/guide.md` (read) — https://github.com/Roblox/creator-docs
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `00 Start Here.md`, `ROUTER.md`, `13 Production and Case Studies/{Ship a Game in 30 Days - Week-by-Week Plan for a Solo Dev, Planning and Scoping a Roblox Game, Scoping and Roles for Small Teams, Team Roles and Workflows}.md`, `15 AI Tools/{Prompting and Verifying AI Output, AI Pitfalls - Stale APIs and Luau}.md`, `52 Core Concepts/Core Concepts Start Here.md` (read)
- https://devforum.roblox.com/t/5-mistakes-that-i-made-when-learning-game-development/3646350 (search summary)
- https://dev.to/aprincessplays/top-mistakes-to-avoid-when-making-your-first-roblox-game-m61 (search summary)
- https://devforum.roblox.com/t/i-worked-on-a-project-for-2-years-it-failed/3919166 and https://devforum.roblox.com/t/i-released-my-new-game-but-it-was-a-flop-why/4089941 (search summary)
- https://devforum.roblox.com/t/localscripts-placed-in-the-workspace-do-not-work/3060795 (search summary)
- https://devforum.roblox.com/t/tutorial-common-scripting-mistakes-in-roblox-studio-and-how-to-fix-them/3994024 (search summary)
- https://devforum.roblox.com/t/roblox-scripting-roadmap-learning-resource-list/808430 and https://devforum.roblox.com/t/i-know-the-basics-of-scripting-what-do-i-do-now/3046503 (search summary: the intermediate plateau)
- https://devforum.roblox.com/t/beginning-your-first-real-game-a-beginners-guide/939308 (search summary)
- https://devforum.roblox.com/t/studio-mcp-server-updates-and-external-llm-support-for-assistant/4415631 and a r/robloxgamedev thread seen through a mirror, "tips for using AI to code your Roblox game" (search summary: learn enough Luau to correct the assistant)
- https://devforum.roblox.com/t/how-to-remove-backdoors-from-your-game/511548 (search summary)
- No evidence found: a measured benchmark for how long a first Roblox game takes, or a 2026 community consensus on the best learning course. Time figures here are `[house]` or `[lihfolk]` rules of thumb.
