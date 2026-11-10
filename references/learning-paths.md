# Learning paths: detect the developer's level, adapt, and route

How Claude works out whether it is helping a beginner, an intermediate or an expert Roblox developer, how the answer changes for each, and the path each one follows: a first hour to first shipped game on-ramp, a ladder from "working" to "good", and the tracks for scaling a live game. Open it at the start of any session where the developer's level is unknown, whenever an answer lands too basic or too advanced, when someone asks "where do I start" or "what should I learn next", and when sizing a project to a time budget. Terms are defined in `references/glossary.md`; Studio mechanics in `references/studio-workflow.md`. Tags: `[official]` creator docs, `[community]` forum, Reddit and blog practice, `[lihfolk]` adapted from LihFolk Vault V2, `[house]`, `[VS]` version-sensitive.

## Start here by level

| Reader | Read | Skip |
|---|---|---|
| Beginner (never shipped a game) | Section 3: first hour, first day, first week, the tiny project, the Blender starter kit, the ten mistakes | Sections 4 and 5 until the first game is public |
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

Install Studio (free; Windows or macOS; 3 GB RAM minimum, 8 GB recommended `[official]`) and Blender (free). Turn on 2-step verification. Complete the age check when ready to release or to collaborate: public release and Team Create with other people both require it `[official]` `[VS]`. Apply the ten-minute setup in studio-workflow.md section 1.

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
| The art pipeline in miniature | Model one bevelled floor tile in Blender, export `.glb`, import with the 3D Importer, set its collision | A mesh you made is in the place and you can stand on it |
| Saving your work | Save to Roblox with Notes (`Ctrl Alt S`) before anything risky; never edit during a playtest | You have restored one old version on purpose, once |

### First week: the tiny project, "Coin Dash" (about 10 hours)

One verb (run and jump to collect), one progression axis (coins buy jump height or speed), one goal (reach the top platform). Write the top half of `templates/game-one-pager.md` first: pitch, fantasy, the loop in one sentence, what the first 60 seconds look like.

| Piece | Smallest correct version | Reference |
|---|---|---|
| World | One arena, about 100 × 100 studs, built only from the starter kit below; SpawnLocation hidden under a kit pad | art-pipeline-blender.md |
| Coins | Models tagged `Coin`, one server script (sketch below), respawn after 5 s | performance.md (spatial queries, later) |
| Upgrades | Two pads. The client sends "buy jump"; the server checks the price, subtracts, raises `Humanoid.JumpHeight` | networking-and-security.md |
| Saving | ProfileStore with coins and upgrade levels. Copy the module from its official repository into a ModuleScript and read it; do not insert it from the Toolbox | data-and-purchases.md |
| HUD | Coin counter and two buttons, sized with Scale not Offset, checked in the Device Simulator on an entry-level phone | ui-input-crossplatform.md |
| Feel | A sound and a small pop when a coin is collected. It changes how fun the loop reads | game-craft.md |

```lua
--!strict
-- unexecuted sketch. Script in ServerScriptService. Each coin is a Model tagged "Coin" holding
-- the Blender mesh ("Mesh") and an invisible anchored Part "Trigger" (CanCollide off, CanTouch on).
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

### The Blender starter kit (how a beginner meets house rules 1 and 2)

Eight pieces carry the whole first game: floor tile 8×8, wall 8×8, ramp, platform 4×4, coin, upgrade pad, arrow sign, spawn pad.

1. Blender scene units: Unit System None, so 1 Blender unit = 1 stud. A Roblox character is roughly 5 studs tall: size doors and steps against an R15 dummy exported from Studio.
2. Start each piece from a cube sized in studs. Add a Bevel modifier (about 0.1 stud, 2 segments) so edges catch light: this one step separates "authored" from "default cube". Keep each piece under about 500 triangles.
3. One material per piece, flat colours from one small palette you reuse for every piece.
4. Apply all transforms (`Ctrl A` > All Transforms). Put the origin where the piece snaps: a bottom corner for tiles and walls, bottom centre for props.
5. Export: File > Export > glTF 2.0 (`.glb`), selected objects only, modifiers applied.
6. Studio: import with the 3D Importer using the preset in art-pipeline-blender.md (scale unit Studs, Anchored on). Unanchored static meshes fall through the world on Play.
7. Collision: `CollisionFidelity` Box for box-shaped pieces, Hull for the ramp. Walk into every piece in a playtest. Nothing visible may be walk-through.
8. Duplicate placed copies with `Ctrl D`; do not re-import the same piece. When the kit grows past this game, move to packages and the scripted export.

Budget for it `[house]`: assume 30 to 60 minutes per simple piece until you have timed your first three, then re-plan. The art volume, not the code, is what sinks a first project under the Blender rule.

### First shipped game: weeks 2 to 4

| Week | Goal | Must be true at the end |
|---|---|---|
| 2 | Nothing earned can be lost or duplicated | Save survives leave-and-rejoin and a server shutdown; every remote checks type, range and rate on the server; one game pass and one developer product go through a single `ProcessReceipt` with `PurchaseId` deduplication; four onboarding funnel events fire |
| 3 | It looks like a game and lasts 30 to 60 minutes | One style, one lighting preset; icon and three thumbnails drafted on day one of the week, not launch night `[lihfolk]`; maturity questionnaire done; played on a real phone |
| 4 | Public | Early testers first, then release (age-checked 16+ at first; reaching younger players has extra requirements and a 250-engaged-play gate `[VS]`, see analytics-and-discovery.md); fix the top three problems and nothing else; write a one-page postmortem |

Shipped means: public; a save verified by rejoining; one purchase made with real Robux in the live game; played on a phone; five strangers have played. Never cut: data safety, receipt handling, server validation, the phone layout, the maturity questionnaire `[lihfolk]`.

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
| 8 | Old APIs from old tutorials and from AI output: `wait`, `spawn`, `LoadAnimation` on the Humanoid, BodyMovers | Subtle bugs; habits to unlearn | The never-do list in SKILL.md; check the docs page |
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
| 5. First session and core loop | First reward under 30 s, first upgrade under 2 min; loop scorecard at 7 of 10 or better; five strangers observed | design-foundations.md §7, core-loop-tuning.md |
| 6. Mobile and performance | 30 FPS or better on a 3 GB Android phone in the worst view; budgets table filled from MicroProfiler captures | performance.md |
| 7. UI and controls | Touch, gamepad and keyboard all complete; safe areas respected; nothing reads as default UI | ui-input-crossplatform.md, ui-design-figma.md, `accessibility-and-player-qol.md` |
| 8. Analytics | Onboarding funnel and economy events firing from the server; one weekly review habit | analytics-and-discovery.md, `templates/analytics-event-plan.md` |
| 9. Economy | Balance sheet with numbers; sink ratio 0.95–1.05 modelled; costs are geometric and time-first | economy-and-progression.md, `templates/economy-balance-sheet.md` |
| 10. Monetisation | Default product set trimmed to fit; offer gate in code; receipts tested live; policy gate passed | monetization-and-policy.md, checklists.md Gate 3 |
| 11. Polish | Juice tiers on the core verb; mix, music and lighting preset; animation where the verb needs it | game-craft.md, `vfx-and-juice.md`, `audio-sfx-music.md`, `animation-and-rigs.md`, `lighting-and-atmosphere.md` |
| 12. Retention and LiveOps | A reason to return tomorrow that is not a punishment; a weekly update day; a four-week plan | liveops-quests-retention.md |
| 13. Discovery and launch | Thumbnails tested; metadata honest; launch checklist signed; growth only after the readiness gate | analytics-and-discovery.md, growth-and-marketing.md, market-scan-2026-11.md |

The usual intermediate plateau `[community]`: forum threads asking "I know the basics, what next" get the same answers: modules and structure, a data library, source control, then tooling. That is rungs 1 to 3. The step people skip is rung 5: most stalled games have adequate code and an untested first five minutes.

## 5. Expert tracks: scaling a live game

Pick by the constraint the numbers show, not by interest.

| Track | Techniques | Measure | Open |
|---|---|---|---|
| LiveOps cadence | Fixed update day; content shipped dark behind Configs; event calendar; update notes in game | Returning-player lift per update; D7 and D30 by cohort | liveops-quests-retention.md |
| Experiments | Configs plus Experiments; one variable; pre-registered success metric; early-harm watch; before/after cohorts when DAU is too low to split | Effect with interval, not a screenshot | analytics-and-discovery.md, core-loop-tuning.md §6 |
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

All paths are under `references/` unless they start with `templates/`. Files in the wave-2 list may not exist yet in an older copy of the skill: fall back to the neighbour named in brackets.

| Question | Open |
|---|---|
| What does this word mean? | glossary.md |
| What should I build? What is trending or saturated? | market-scan-2026-11.md, genre-playbooks.md |
| How does my genre work, and what breaks in it? | `genres/<genre>.md` |
| Is my idea fun? How do I write it down? | design-foundations.md, process-and-playtesting.md, `templates/game-one-pager.md` |
| My game exists. What do I fix first? | audit-existing-game.md, `templates/game-audit-report.md` |
| Players leave in the first minutes | core-loop-tuning.md, design-foundations.md §7 |
| Players do not come back | liveops-quests-retention.md |
| How do I price upgrades, XP, rebirths, luck? | economy-and-progression.md |
| What do I sell, and what is allowed? | monetization-and-policy.md |
| How do I structure my code? | engineering-architecture.md, architecture-patterns-luau.md |
| A Luau language question (types, tables, metatables, performance idioms) | `luau-mastery.md` [engineering-architecture.md] |
| How do I build system X (inventory, quests, pets, rounds, shops)? | `gameplay-systems-cookbook.md` [architecture-patterns-luau.md, the genre file] |
| Remotes, exploits, bans, secrets | networking-and-security.md |
| Saving, purchases, receipts, teleports, cross-server | data-and-purchases.md |
| It lags, crashes or loads slowly | performance.md |
| Something is broken and I cannot find why | `debugging-and-testing.md` [engineering-architecture.md §Testing, studio-workflow.md §2] |
| Blender, export, import, collision, kits | art-pipeline-blender.md |
| Lighting and mood | `lighting-and-atmosphere.md` [art-pipeline-blender.md §Lighting] |
| Layout of levels and worlds | `level-design-worldbuilding.md` [game-craft.md §2] |
| Characters, rigs, animation | `animation-and-rigs.md` [game-craft.md] |
| Effects and juice; sound and music | `vfx-and-juice.md`, `audio-sfx-music.md` [game-craft.md §1, §4] |
| Vehicles, constraints, physics | `physics-and-vehicles.md` [performance.md §Physics] |
| Designing UI; building UI for every device | ui-design-figma.md; ui-input-crossplatform.md |
| Accessibility, settings, quality-of-life | `accessibility-and-player-qol.md` [ui-input-crossplatform.md] |
| What do I measure? How do I get recommended? | analytics-and-discovery.md |
| How do I get players (ads, video, creators, community)? | growth-and-marketing.md |
| Moderation, community rules, child safety | `community-moderation-safety.md` [monetization-and-policy.md §Policy] |
| Team, contracts, payouts, DevEx, legal | `team-business-legal.md` [monetization-and-policy.md] |
| Studio settings, testing, publishing, Team Create, Rojo migration, backups | studio-workflow.md |
| Which AI tools, skills and MCP servers are safe to add? | ai-toolchain-skills.md |
| How did successful games do it? | `case-studies-teardowns.md` [market-scan-2026-11.md] |
| Am I ready to ship? | checklists.md, `templates/launch-checklist.md` |
| Where do I start learning? | This file |

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

Solo rotation that prevents the favourite-role trap `[lihfolk]`: name the role each day belongs to (for example two days systems, two days content, one day testing and community).

## 8. Scope by time budget

Capacity first: productive hours = available hours × focus factor (section 7). Add 30–50% to the sum of feature estimates for integration and testing `[lihfolk]`. Conflict: process-and-playtesting.md says to multiply gut estimates by about 3; the capacity method lands between ×2 and ×4. Use the capacity method when hours are known and ×3 when they are not; never apply both to the same number.

| Budget | Productive hours (solo) | What fits | What does not |
|---|---|---|---|
| Weekend | 10–16 | One verb, one arena from an 8-piece kit, one upgrade axis, a save, friends-only release. A mechanic slice whose only question is "is the verb fun?" | Monetisation beyond one pass, more than one zone, any custom rig |
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
| Good code, players leave in two minutes | Rung 5 skipped | core-loop-tuning.md |
| Launched, got 200 visits, called it a flop `[community]` | No traffic plan and too little time; first-session quality unknown | analytics-and-discovery.md for the 250-play gate; fix the first session before buying traffic |
| Strong developer from another engine writes client-trusting code | Platform gap, not skill gap | Client-server model in engineering-architecture.md; data and replication rules |
| Team members overwrite each other | No ownership, shared place | studio-workflow.md §5 |
| Expert asks for a rewrite of a live game | Rebuild instinct | audit-existing-game.md: three fixes usually beat a rebuild |

## Review gate

- [ ] Level rated per domain from evidence, and re-rated when new evidence arrived; the person was never labelled.
- [ ] The answer matched the level in scope, tooling and depth, and no safety rule was simplified away.
- [ ] Beginner: one next step, the exact container for each script, and a way to verify were given; nothing from the "ignore for now" list was introduced unasked.
- [ ] Beginner project: every visible object comes from the Blender kit and collides; practice places with Parts are not published.
- [ ] Intermediate: the lowest failing rung was addressed before higher ones.
- [ ] Expert: numbers were requested or cited with date; lower-risk and bold options were both stated.
- [ ] Scope was checked against productive hours, with a written cut list.
- [ ] Every routed reference exists, or the bracketed fallback was used.

## Sources

Accessed 2026-11-10.

- Roblox/creator-docs, commit ccc2b01 (2026-11-07), `content/en-us/`: `tutorials/index.md` and the `tutorials/curriculums/` and `tutorials/first-experience/` listings, `studio/setup.md`, `includes/studio/system-reqs.md`, `production/publishing/publish-games-and-places.md`, `projects/collaboration.md`, `projects/place-files.md`, `projects/assets/packages.md`, `ai/coding-harness.md`, `assistant/guide.md` (read) — https://github.com/Roblox/creator-docs
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
