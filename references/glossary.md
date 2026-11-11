# Glossary: the words a Roblox developer meets

264 terms across the platform, the engine, Luau, networking, data, monetisation, analytics, discovery, the art pipeline, UI and community slang, each in one or two plain lines with the reference to open for more. Open it when a term in another reference, a forum thread or a dashboard is unclear, when explaining something to a beginner (define the term the first time it appears), and in an audit to confirm two people mean the same thing by a word. File names in the last column are under `references/` (the full file map is `references/INDEX.md`). Numbers are `[VS]`: version-sensitive, re-check at create.roblox.com/docs. `[house]` marks house conventions.

Contents: Start here by level · Confusable pairs · A–C · D–F · G–L · M–P · Q–S · T–Z · Level-up: words that flag a problem · Review gate · Sources

## Start here by level

| Level | Use it for |
|---|---|
| Beginner | Learn these 25 first: Experience, Place, Studio, Explorer, Output, Instance, Workspace, Script, LocalScript, ModuleScript, Client, Server, RemoteEvent, ReplicatedStorage, ServerScriptService, Anchored, CanCollide, MeshPart, Stud, DataStore, Game pass, Developer product, Robux, Core loop, Publish ("Studio" is under Roblox Studio; "Publish" is under Confusable pairs). Ignore the rest until a word shows up in front of you |
| Intermediate | The metric words (CCU, DAU, D1/D7/D30, ARPDAU, ARPPU, PTR, payer conversion), the data words (session lock, idempotent, migration, `UpdateAsync`) and the performance words (draw call, frame budget, instance streaming) |
| Expert | A shared vocabulary for briefs and audits, and a list of names that changed recently: LightingStyle, Input Action System, Creator Store, Roblox Plus, Managed Pricing, server authority mode, age tiers |

## Confusable pairs

| Pair | Difference |
|---|---|
| Experience / universe / place | Experience (also "game") is what players see and is one universe (`game.GameId`). A place is one loadable world inside it (`game.PlaceId`). Products, DataStores and badges belong to the universe |
| Save / publish | Save to Roblox stores a new version in the cloud. Publish makes a version the one new servers run. Neither moves players already in old servers |
| Script / LocalScript / ModuleScript | Script runs on the server (or wherever its `RunContext` says). LocalScript runs on one player's device, only in client containers. ModuleScript runs nowhere until something `require`s it |
| ReplicatedStorage / ServerStorage | Both hold things not in the world. Every client can read ReplicatedStorage; no client can see ServerStorage |
| Game pass / developer product / subscription | Pass: bought once, owned forever. Product: bought repeatedly, granted by `ProcessReceipt`. Subscription: renews monthly |
| Anchored / CanCollide | Anchored: physics never moves it. CanCollide: things cannot pass through it. A floor needs both |
| CCU / DAU | CCU: players online at this moment. DAU: distinct players in a day |
| CTR / PTR | CTR: clicks per impression (ads). PTR: plays per impression on Home; qualified PTR counts only plays that last |
| Server authority (principle) / server authority mode | The principle: the server decides outcomes. The mode: an engine feature where the server simulates and clients predict |
| RNG game / gacha / paid random item | RNG game: rolling for rarity is the loop. Gacha: random draws from a pool. Paid random item: any random reward bought with Robux, directly or indirectly; that one carries policy duties |
| Rebirth / prestige | Same idea: reset progress for a permanent multiplier |
| Creator Store / Marketplace | Creator Store: models, plugins, audio for developers. Marketplace: avatar items for players |
| Tween / spring | Tween: fixed duration and easing curve. Spring: follows a moving target, can be interrupted smoothly |
| Touched / spatial query | Touched: event from physical contact, noisy, needs a debounce. Spatial query: you ask what is in a box, sphere or ray at a moment you choose |

## A–C

| Term | Meaning | More |
|---|---|---|
| **250-play gate** | The evaluation a game passes before players under 16 can see it: 250 unique plays by highly engaged, age-checked 16+ players within 60 days, on top of creator verification and a fee or subscription `[VS]` | analytics-and-discovery.md |
| **9-slice** | An image cut into nine regions so the corners keep their shape while the middle stretches (`ScaleType = Slice`); how one small texture makes panels and buttons of any size | ui-design-figma.md |
| **A/B test** | Showing different versions to random groups and comparing a metric. On Roblox: Experiments | analytics-and-discovery.md |
| **Actor** | Container whose scripts may run in parallel with others | performance.md |
| **AFK** | Away from keyboard. Idle players are disconnected after about 20 minutes `[VS]`; AFK rewards must not gate progress | liveops-quests-retention.md |
| **Age check** | Facial age estimation or ID check. Needed for chat, for Team Create with others and for public release `[VS]` | studio-workflow.md |
| **Age tiers** | Roblox Kids (5–8), Roblox Select (9–15), Roblox (16+). Tier plus content label decides who can see a game `[VS]` | analytics-and-discovery.md |
| **Albedo** | The colour texture of a PBR set, with no lighting baked in | art-pipeline-blender.md |
| **AnalyticsService** | API that logs funnel, economy and custom events to Creator Analytics | analytics-and-discovery.md |
| **Anchored** | Property that stops physics moving a part. Static scenery is always anchored | performance.md |
| **Animator / AnimationTrack** | Animator plays animations on a rig; each loaded animation is a track you play, stop and blend | animation-and-rigs.md |
| **ARPDAU** | Average revenue per daily active user | analytics-and-discovery.md |
| **ARPPU** | Average revenue per paying user | analytics-and-discovery.md |
| **Assembly** | Parts joined rigidly into one physics body | physics-and-vehicles.md |
| **Asset id** | The number identifying an uploaded mesh, image, sound or animation (`rbxassetid://…`). Never invent one | art-pipeline-blender.md |
| **Assistant** | Studio's built-in AI helper. Its generators and asset search are off limits for shipped content `[house]` | studio-workflow.md |
| **Atomic** | Model streaming mode: the whole model arrives together or not at all. Use for interactive models | performance.md |
| **Attachment** | A point with orientation on a part, used by constraints, effects and audio | vfx-and-juice.md |
| **Attribute** | A typed custom value stored on an Instance; replicates and fires change events | engineering-architecture.md |
| **Audio API** | The newer audio graph (`AudioPlayer`, `AudioEmitter`, `AudioListener`, wires, effects) next to the classic `Sound` | audio-sfx-music.md |
| **Backdoor** | Hidden code, usually from a free model or plugin, that lets an outsider run commands in your servers | networking-and-security.md |
| **Badge** | A permanent achievement shown on a player's profile | liveops-quests-retention.md |
| **Ban API** | Engine bans by user, with duration and alt-account handling | networking-and-security.md |
| **BasePart** | Parent class of everything physical: Part, MeshPart, and others | performance.md |
| **Beam / Trail** | Beam: a textured ribbon between two attachments. Trail: a ribbon left behind a moving attachment | vfx-and-juice.md |
| **BillboardGui** | UI that floats in the world and faces the camera (name tags, damage numbers) | ui-input-crossplatform.md |
| **BindToClose** | Callback that runs when a server shuts down; about 30 s to finish saving `[VS]` | data-and-purchases.md |
| **Blockout (greybox)** | Rough layout before final art. Here it is built from a Blender blockout kit, never from Parts that ship `[house]` | art-pipeline-blender.md |
| **Boost** | A timed multiplier (2× Cash for 10 minutes), earned or bought | monetization-and-policy.md |
| **Bounce (first-play)** | A new player's first session ending within 60 s, or within 61–180 s. A negative recommendation signal | analytics-and-discovery.md |
| **Brainrot** | Slang for the 2025 meme-character trend and the games built on it (Steal a Brainrot) | market-scan-2026-11.md |
| **Buffer** | Fixed-size block of bytes in Luau; used for compact network and save data | networking-and-security.md |
| **CanCollide / CanQuery / CanTouch** | Whether a part blocks movement / is found by raycasts and spatial queries / fires `Touched` | performance.md |
| **CanvasGroup** | UI container drawn as one image, so it can fade or clip as a unit | ui-input-crossplatform.md |
| **CCU** | Concurrent users: players online right now | analytics-and-discovery.md |
| **CFrame** | Position plus rotation of an object in one value | luau-mastery.md |
| **Character** | The player's avatar model in the world, rebuilt on every respawn | gameplay-systems-cookbook.md |
| **Client** | A player's device and the code running on it. Assume it can be modified | networking-and-security.md |
| **Codes** | Redeemable strings that grant rewards, used for marketing | growth-and-marketing.md |
| **CollectionService** | Service for tags: label Instances, then one script handles every Instance with that label | engineering-architecture.md |
| **Collision group** | A named set of parts with rules for which sets collide | performance.md |
| **CollisionFidelity** | How closely a mesh's physics shape follows its look: Box, Hull, Default, Precise | art-pipeline-blender.md |
| **Command Bar** | Studio input that runs Luau against the open place, with elevated rights | studio-workflow.md |
| **Configs** | Values changed from Creator Hub without republishing (`ConfigService`); the basis of flags and experiments | analytics-and-discovery.md |
| **Content maturity label** | The rating from the maturity questionnaire: Minimal, Mild, Moderate, Restricted, or Content May Vary | analytics-and-discovery.md |
| **Core loop** | The short cycle a player repeats most: act, get rewarded, improve, act again | core-loop-tuning.md |
| **CoreGui** | Roblox's own UI over your game: top bar, menu, chat | ui-input-crossplatform.md |
| **CPP** | Cost per play: ad spend divided by plays bought | growth-and-marketing.md |
| **Creator Hub (Dashboard)** | create.roblox.com: settings, analytics, products, docs | analytics-and-discovery.md |
| **Creator Rewards** | Roblox programme paying creators for daily engagement and for bringing in new or returning users `[VS]` | monetization-and-policy.md |
| **Creator Store** | Roblox's library of models, plugins and audio for developers. Nothing from it ships as visible content `[house]` | studio-workflow.md |
| **CTR** | Click-through rate: clicks divided by impressions | growth-and-marketing.md |
| **Cutscene** | A short scene that takes the camera (and usually the controls) to show something. Always skippable, never before the first action | cutscenes-and-cinematics.md |

## D–F

| Term | Meaning | More |
|---|---|---|
| **D1 / D7 / D30** | Share of new players who return 1, 7 or 30 days after their first day. Benchmarks are in one table only | analytics-and-discovery.md |
| **DataModel** | The tree of everything in a place; `game` in code | engineering-architecture.md |
| **DataStore** | Roblox's persistent key-value storage for player and game data; values up to 4 MB `[VS]` | data-and-purchases.md |
| **DAU / MAU** | Distinct players per day / per month | analytics-and-discovery.md |
| **Debounce** | A guard so an action cannot fire again until a cooldown ends | luau-mastery.md |
| **Deferred events** | Event handlers run a little later in the frame instead of immediately (`SignalBehavior`); the default in new places `[VS]` | luau-mastery.md |
| **Developer Console** | In-game panel (`F9`) with client and server logs, memory and network stats | debugging-and-testing.md |
| **Developer product** | A purchase that can be bought again and again (currency, boosts) | data-and-purchases.md |
| **DevEx** | Developer Exchange: converting earned Robux to money; $0.0038 per Robux at the standard rate `[VS]` | monetization-and-policy.md |
| **Device Simulator** | Studio toolbar that previews phone, tablet, console and headset screens and input | studio-workflow.md |
| **Drafts mode** | Team Create option where script edits stay local until committed | studio-workflow.md |
| **Draw call** | One batch of geometry sent to the GPU. Fewer is faster; house budget under 1,000 in the worst view `[house]` | performance.md |
| **Dupe** | Duplicating items or currency through a bug, usually a save or trade race | economy-and-progression.md |
| **Easing** | The speed curve of a movement (slow start, slow stop). Linear motion reads as mechanical | ui-motion-and-feedback.md |
| **ECS** | Entity component system: data in components, logic in systems. Only for simulation-heavy games | architecture-patterns-luau.md |
| **EditableMesh / EditableImage** | Meshes and images changed by code at runtime; restricted and memory-heavy | performance.md |
| **Egg / hatch** | Collection-game purchase that reveals a random pet. If Robux can buy it, it is a paid random item | genres/pet-collection-hatching.md |
| **Executor** | Third-party program exploiters use to run their own code on the client | networking-and-security.md |
| **Experience** | Roblox's official word for a game | studio-workflow.md |
| **Experiments** | Creator Hub A/B testing built on Configs | analytics-and-discovery.md |
| **Exploit** | Cheating by running modified client code: teleporting, firing remotes with false data | networking-and-security.md |
| **Explorer** | Studio window showing the DataModel tree | studio-workflow.md |
| **Faucet / sink** | Where currency enters the economy / where it leaves | economy-and-progression.md |
| **FilteringEnabled (FE)** | Old switch, now always on: client changes do not replicate to the server. Still used as slang ("FE-safe") | networking-and-security.md |
| **Flipbook** | A grid of frames in one texture (2×2, 4×4 or 8×8), played as an animated particle. Also the name of a UI storybook plugin | vfx-and-juice.md, vfx-recipes.md |
| **FPS** | Frames per second. House floor: 30 on a low-end Android phone `[house]` | performance.md |
| **Frame budget** | Time available per frame: 16.7 ms at 60 FPS, 33.3 ms at 30 | performance.md |
| **Free model** | A Creator Store model made by someone else. Common source of backdoors; banned from shipped content `[house]` | networking-and-security.md |
| **FTUE** | First-time user experience: the first minutes of a new player, including any tutorial | tutorial-and-onboarding.md |
| **Funnel** | Ordered steps (joined, first reward, first upgrade…) with the share of players reaching each | analytics-and-discovery.md |

## G–L

| Term | Meaning | More |
|---|---|---|
| **Gacha** | Random draw from a pool with stated odds | economy-and-progression.md |
| **Game pass** | One-time purchase that grants a permanent perk | data-and-purchases.md |
| **GameId (UniverseId)** | The id of the whole experience; differs between dev and live universes | studio-workflow.md |
| **GDD** | Game design document. The house version is lean (`templates/lean-gdd.md`) | process-and-playtesting.md |
| **GLB / glTF** | The 3D file format the house pipeline exports from Blender | art-pipeline-blender.md |
| **Group** | A Roblox organisation that can own games, hold funds and assign roles | team-business-legal.md |
| **Heartbeat** | `RunService` event fired every frame after physics; also "server heartbeat", the server's frame rate (target 60 Hz) | performance.md |
| **Highlight** | Outline and fill effect on a model; limited in number on screen | vfx-and-juice.md |
| **Hitbox** | The volume used to decide whether an attack lands | gameplay-systems-cookbook.md |
| **Hit-stop** | A few frozen frames on impact that make a hit feel heavy; local to the attacker and target, never a server pause | vfx-and-juice.md |
| **Home** | The Roblox app's front page; most traffic starts here | analytics-and-discovery.md |
| **Honeypot** | A fake remote or value that only a cheater would touch, used as evidence | networking-and-security.md |
| **HttpService** | Server-side web requests and JSON; 500 requests a minute `[VS]` | networking-and-security.md |
| **Humanoid** | The object that makes a model a character: health, walking, jumping, states | gameplay-systems-cookbook.md |
| **HumanoidRootPart** | The invisible central part that positions a character | gameplay-systems-cookbook.md |
| **Idempotent** | Safe to run twice with the same result. Required for purchase grants | data-and-purchases.md |
| **IKControl** | Engine inverse kinematics: makes a limb reach a target | animation-and-rigs.md |
| **Immersive ads** | Ad units placed inside the 3D world that pay the developer | monetization-and-policy.md |
| **Impression** | One showing of your tile or ad to one player | analytics-and-discovery.md |
| **Input Action System** | Newer input model: `InputContext` and `InputAction` Instances mapped to keys, touch and gamepad | ui-input-crossplatform.md |
| **Instance** | Any object in the DataModel | engineering-architecture.md |
| **Instance streaming** | Sending the world to each client in pieces near the player (`StreamingEnabled`). Code must cope with things not being there yet | performance.md |
| **Intent** | What a remote should carry: "I want to buy X", never "give me 100 coins" | networking-and-security.md |
| **Jest Roblox** | Test framework for Luau; the default for new in-engine tests | engineering-architecture.md |
| **Journey** | Analytics for a branching path (pick a class, then a starter): stages with alternative nodes, where a funnel is one straight line `[VS]` | tutorial-and-onboarding.md |
| **Juice** | Feedback that makes an action feel good: sound, flash, shake, particles, squash | game-craft.md §1, vfx-and-juice.md |
| **Key / fill / rim** | The main light, the light that softens its shadows, and the edge light from behind that separates a subject from the background | lighting-and-atmosphere.md |
| **Kit** | A set of modular Blender pieces built on one grid that snap together | art-pipeline-blender.md |
| **Knit** | An older Luau framework. Not used for new projects here `[house]` | engineering-architecture.md |
| **Leaderstats** | A folder named `leaderstats` under a Player whose values show on the default leaderboard. A display, not a save system | gameplay-systems-cookbook.md |
| **Letterbox** | Black bars above and below a cutscene. They tell the player the controls are off, so they never show while the player can act | cutscenes-and-cinematics.md |
| **LightingStyle** | Lighting setting (Soft or Realistic) that replaced `Lighting.Technology` `[VS]` | lighting-and-atmosphere.md |
| **LiveOps** | Running a live game: updates, events, offers, fixes on a cadence | liveops-quests-retention.md |
| **Localization** | Translating text and adapting content per language | growth-and-marketing.md |
| **LocalScript** | Script that runs on a player's device, only in client containers | engineering-architecture.md |
| **LOD** | Level of detail: cheaper versions of distant objects | performance.md |
| **Luau** | Roblox's programming language, derived from Lua 5.1 with types and speed | luau-mastery.md |
| **luau-lsp** | Language server giving editors autocomplete and type errors for Luau | engineering-architecture.md |
| **Luck** | A multiplier on the chance of rare results. If bought, odds must be disclosed and policy-gated | economy-and-progression.md |

## M–P

| Term | Meaning | More |
|---|---|---|
| **Managed Pricing** | Roblox adjusting prices by region and by price tests, within a set range of your base price `[VS]` | monetization-and-policy.md |
| **MarketplaceService** | Service for prompting purchases, checking ownership and reading live prices | data-and-purchases.md |
| **MaterialVariant** | A custom material that replaces or extends a built-in one | art-pipeline-blender.md |
| **MCP** | Model Context Protocol: how AI clients such as Claude use tools like Studio, Blender and Figma | studio-workflow.md |
| **MemoryStore** | Fast, temporary, cross-server storage (queues, sorted maps); data expires | data-and-purchases.md |
| **MeshPart** | A part whose shape is an imported mesh; up to 20,000 triangles each `[VS]` | art-pipeline-blender.md |
| **MessagingService** | Best-effort messages between servers of one experience | data-and-purchases.md |
| **Meta** | (1) The long loop beyond one session. (2) Slang for the currently strongest strategy | design-foundations.md |
| **Mezzanine** | Studio's bar above the toolbar holding the test controls and collaboration buttons | studio-workflow.md |
| **MicroProfiler** | Frame-by-frame timing tool (`Ctrl F6`; some docs pages say `Ctrl Alt F6`) `[VS]` | performance.md |
| **Migration** | Code that upgrades old saved data to a new schema version | data-and-purchases.md |
| **ModuleScript** | A script that returns a value (usually a table of functions) when required. Where shared logic lives | engineering-architecture.md |
| **Motion token** | A named duration and easing (for example "fast: 0.12 s, ease out") used by every UI animation so the whole game moves one way | ui-motion-and-feedback.md |
| **Motor6D** | The animatable joint between two parts of a rig | animation-and-rigs.md |
| **MTX** | Microtransaction: a small in-game purchase | monetization-and-policy.md |
| **Native codegen** | Compiling a hot script to machine code (`--!native`). Only after measuring | performance.md |
| **Network ownership** | Which machine simulates a part's physics: the server or one client | physics-and-vehicles.md |
| **Normal map** | Texture that fakes small surface detail through lighting | art-pipeline-blender.md |
| **NPC** | Non-player character | game-craft.md §5 |
| **Obby** | Obstacle course game | genres/obby-tower.md |
| **Offline income** | Earnings granted for time away; capped and stated `[house]` | economy-and-progression.md |
| **Open Cloud** | Roblox's web APIs: publish places, upload assets, read and write data, run Luau | engineering-architecture.md |
| **OrderedDataStore** | DataStore of integers that can be read in sorted order; used for leaderboards | data-and-purchases.md |
| **Output** | Studio window showing prints, warnings and errors, labelled client or server | studio-workflow.md |
| **Package** | A reusable, versioned asset; copies update from the source | studio-workflow.md |
| **Paid access** | Charging Robux or local currency to enter a game | monetization-and-policy.md |
| **Paid random item** | Any random reward obtainable with Robux, directly or through bought currency. Needs odds disclosure and `PolicyService` gating | monetization-and-policy.md |
| **Parallel Luau** | Running scripts on several threads through Actors | performance.md |
| **ParticleEmitter** | Emits many small textured sprites: smoke, sparks, coins | vfx-and-juice.md |
| **PathfindingService** | Computes walkable routes for NPCs | game-craft.md |
| **Payer conversion** | Share of players who buy anything | analytics-and-discovery.md |
| **PBR** | Physically based rendering: colour, normal, roughness and metalness maps | art-pipeline-blender.md |
| **pcall** | Protected call: runs a function and catches its error. Every DataStore and web call sits in one | luau-mastery.md |
| **Pity** | A guaranteed good result after a set number of unlucky rolls | economy-and-progression.md |
| **Place** | One loadable world inside an experience | studio-workflow.md |
| **Place version** | A numbered save of a place; publishing picks which one new servers run | studio-workflow.md |
| **Play days** | The number of different days a player returns inside a window (day 1, days 2–7, days 8–28). A core recommendation signal | analytics-and-discovery.md |
| **PlayerGui** | Each player's live copy of the UI, cloned from StarterGui | ui-input-crossplatform.md |
| **Plugin** | A Studio extension. Runs with high privileges and can edit every script | studio-workflow.md |
| **PolicyService** | Tells the server what a player may see by region and age (for example whether paid random items are restricted) | monetization-and-policy.md |
| **Primitive Part** | A built-in block, sphere, wedge or cylinder. Allowed only as invisible helpers `[house]` | art-pipeline-blender.md |
| **Private server** | A server only invited players can join, free or paid | monetization-and-policy.md |
| **ProcessReceipt** | The single server callback that grants developer-product purchases | data-and-purchases.md |
| **ProfileStore** | Library that adds session locking and safe saving on top of DataStores; the house default | data-and-purchases.md |
| **ProximityPrompt** | Built-in "hold E to interact" prompt that adapts to touch and gamepad | ui-input-crossplatform.md |
| **PTR / qualified PTR** | Play-through rate: plays per Home impression; with first-play bounce it has been the top recommendation signal since June 2026. Qualified PTR counts only plays that last and is what the thumbnail table reports `[VS]` | analytics-and-discovery.md |
| **PurchaseId** | Unique id of one receipt; save it before granting to avoid double grants | data-and-purchases.md |

## Q–S

| Term | Meaning | More |
|---|---|---|
| **QoL** | Quality of life: small conveniences such as settings, sort, skip, auto-collect | accessibility-and-player-qol.md |
| **Qualified play** | A play that lasts long enough to count as real, which filters accidental taps | analytics-and-discovery.md |
| **Quest** | A stated goal with a reward; daily, weekly or story | liveops-quests-retention.md |
| **R6 / R15** | The two standard avatar rigs: 6 parts or 15 parts | animation-and-rigs.md |
| **Rate limit** | A cap on how often something may happen, per player or per service | networking-and-security.md |
| **Raycast** | Asking what a straight line hits | performance.md |
| **Rebirth** | Resetting progress in exchange for a permanent multiplier | economy-and-progression.md |
| **Reconcile** | ProfileStore step that fills fields missing from an old save using the template. Run migrations first | data-and-purchases.md |
| **RemoteEvent** | One-way message between client and server | networking-and-security.md |
| **RemoteFunction** | Request and reply between client and server. Never invoke the client from the server | networking-and-security.md |
| **RenderFidelity** | How a mesh's detail drops with distance: Automatic, Performance, Precise | performance.md |
| **ReplicatedFirst** | Container delivered to clients before anything else; holds the loading screen | performance.md |
| **ReplicatedStorage** | Container both sides can read. No secrets, no server logic | engineering-architecture.md |
| **Replication** | The engine copying server state to clients (and a little the other way) | engineering-architecture.md |
| **Reserved server** | A private server instance created by code, for matches, dungeons or lobbies | data-and-purchases.md |
| **Retention** | Share of players who come back; see D1 / D7 / D30. Benchmarks: analytics-and-discovery.md | liveops-quests-retention.md |
| **Rewarded video** | An ad a player chooses to watch for a reward. Never random rewards, never a progress gate `[house]` | monetization-and-policy.md |
| **RFY** | Recommended For You: the personalised sort on Home that drives most discovery | analytics-and-discovery.md |
| **Rig** | A model with joints or bones that can be animated | animation-and-rigs.md |
| **RNG** | Random number generator; slang for games whose loop is rolling for rare results | genres/simulator-incremental.md |
| **Roblox Plus** | Roblox subscription whose members get 10% (20% from the third month) off eligible purchases, paid for by Roblox; sits beside the older Premium `[VS]` | monetization-and-policy.md |
| **Roblox Studio** | The free desktop editor (Windows, macOS) for building, scripting, testing and publishing | studio-workflow.md |
| **Robux (R$)** | Roblox's currency. Developers receive a share of each sale and can cash out through DevEx | monetization-and-policy.md |
| **Rojo** | Tool that syncs files on disk into Studio, enabling git, reviews and CI | studio-workflow.md |
| **RunContext** | Property deciding where a Script runs: Server, Client or Legacy | engineering-architecture.md |
| **RunService** | Service exposing per-frame events and "am I server, client or Studio" checks | luau-mastery.md |
| **Safe area** | The part of the screen clear of notches, rounded corners and Roblox's top bar | ui-input-crossplatform.md |
| **ScreenGui** | Container for 2D on-screen UI | ui-input-crossplatform.md |
| **Script** | Code container that runs on the server by default | engineering-architecture.md |
| **Script Sync** | Built-in Studio feature that mirrors scripts to files on disk | studio-workflow.md |
| **Season pass** | A time-limited track of rewards with free and paid lanes | liveops-quests-retention.md |
| **Selene / StyLua** | Luau linter / Luau code formatter | engineering-architecture.md |
| **Server** | The Roblox-hosted machine running the authoritative copy of a game session | engineering-architecture.md |
| **Server authority** | The server decides every outcome that matters; clients only request | networking-and-security.md |
| **Server authority mode** | Engine feature in which the server simulates gameplay and clients predict and correct `[VS]` | networking-and-security.md |
| **ServerScriptService** | Container for server scripts; clients cannot see it | engineering-architecture.md |
| **ServerStorage** | Container for server-only assets; clients cannot see it | engineering-architecture.md |
| **Session lock** | A marker that gives one server ownership of a save, which stops two servers overwriting each other | data-and-purchases.md |
| **Session time** | How long one visit lasts | analytics-and-discovery.md |
| **Shapecast** | Sweeping a box or sphere through space to see what it hits | performance.md |
| **Simulator** | Genre: act, number goes up, upgrade, new zone, rebirth | genres/simulator-incremental.md |
| **Sink ratio** | Currency removed divided by currency created; target 0.95–1.05 `[house]` | economy-and-progression.md |
| **Skinned mesh** | One mesh deformed by bones, instead of rigid parts | animation-and-rigs.md |
| **SLIM** | Cloud-built low-detail stand-ins for distant static models `[VS]` | performance.md |
| **Soft launch** | Public but unpromoted release used to find problems before a push | growth-and-marketing.md |
| **SpawnLocation** | Where characters appear | level-design-worldbuilding.md |
| **Starter pack** | A one-time bundle for new players. Honest price, shown after a first win `[house]` | monetization-and-policy.md |
| **StarterGui** | Container whose UI is copied to each player on spawn | ui-input-crossplatform.md |
| **StarterPlayerScripts** | Container for client scripts that run once per player | engineering-architecture.md |
| **Stickiness** | DAU divided by MAU | analytics-and-discovery.md |
| **Streak** | Consecutive days played. The house daily reward is a cumulative calendar (days played, never resets); a login streak that resets on a miss is rejected `[house]` | liveops-quests-retention.md |
| **Stud** | Roblox's unit of length; 1 stud = 0.28 m. The house pipeline models at 1 Blender unit = 1 stud | art-pipeline-blender.md |
| **Style bible** | One page of measurable art rules for this game: palette, shape language, bevel width, texel density, lighting, UI and effect tie-ins. Written before the first asset | art-direction-and-quality-bar.md |
| **Subscription** | A monthly recurring purchase inside one experience | monetization-and-policy.md |
| **SurfaceAppearance** | The PBR texture set applied to a MeshPart | art-pipeline-blender.md |
| **SurfaceGui** | UI drawn on the face of a part | ui-input-crossplatform.md |

## T–Z

| Term | Meaning | More |
|---|---|---|
| **Tag** | A label on an Instance, read through CollectionService | engineering-architecture.md |
| **task library** | `task.wait`, `task.spawn`, `task.delay`, `task.defer`: the current scheduling functions. `wait`, `spawn` and `delay` are deprecated | luau-mastery.md |
| **Team Create** | Several people editing one place at once | studio-workflow.md |
| **Team Test** | A shared playtest on Roblox servers for collaborators | studio-workflow.md |
| **Telegraph** | A visible warning (ring, flash, wind-up) that shows where and when an attack will land, long enough to react | vfx-and-juice.md, vfx-recipes.md |
| **TeleportService** | Moves players between places and servers. Does not work in Studio playtests | data-and-purchases.md |
| **Terrain** | Roblox's voxel landscape. Needs the owner's approval per game `[house]` | art-pipeline-blender.md |
| **Texel density** | Texture pixels per stud; keep it even across assets (about 50 px per stud `[house]`, fixed in the style bible) | art-pipeline-blender.md, art-direction-and-quality-bar.md |
| **Text filtering** | Mandatory moderation of any player-written text before others see it | ui-input-crossplatform.md |
| **TextChatService** | The current chat system; all chat code goes through it | ui-input-crossplatform.md |
| **Thumbnail / icon** | Thumbnail: the 16:9 image on Home, which promises the first minute. Icon: the square image players learn to recognise. The main levers on play-through rate | icons-thumbnails-and-store-page.md |
| **Tile test** | Shrinking an icon to 150, 64 and 32 px and a thumbnail to 160×90 (also greyscale and blurred) to see what survives on a phone; `scripts/images/tile_test.py` | icons-thumbnails-and-store-page.md |
| **Toolbox** | Studio panel for inserting Creator Store assets and your own inventory | studio-workflow.md |
| **Touched** | Event fired when parts physically touch | performance.md |
| **Trim sheet** | One texture of reusable strips mapped onto many meshes | art-pipeline-blender.md |
| **Tween** | Animating a property from one value to another over a fixed time | ui-motion-and-feedback.md, vfx-and-juice.md |
| **Tycoon** | Genre: own a plot, earn per second, buy the next piece | genres/tycoon-and-cozy-management.md |
| **Type checking (`--!strict`)** | Luau checking types before the code runs. On for all new code `[house]` | luau-mastery.md |
| **UDim2** | UI size and position as scale (fraction of parent) plus offset (pixels) on each axis | ui-input-crossplatform.md |
| **UGC** | User-generated content; on Roblox usually means avatar items sold on the Marketplace | monetization-and-policy.md |
| **UI constraints** | Helper objects such as `UIScale`, `UIAspectRatioConstraint`, `UIListLayout`, `UIStroke`, `UIPadding` | ui-input-crossplatform.md |
| **UnreliableRemoteEvent** | Remote that may drop or reorder messages; for frequent cosmetic updates | networking-and-security.md |
| **UpdateAsync** | DataStore call that reads, lets you change, and writes back safely | data-and-purchases.md |
| **UserId** | A player's permanent numeric id. Key data by it, never by name | data-and-purchases.md |
| **UV** | The 2D coordinates that place a texture on a mesh | art-pipeline-blender.md |
| **Value (art)** | How light or dark a colour is. A scene, icon or effect must read in greyscale before hue is chosen | art-direction-and-quality-bar.md |
| **Version History** | Studio window listing every saved and published version of a place | studio-workflow.md |
| **Vertex colour** | Colour stored on mesh vertices; tints without a texture | art-pipeline-blender.md |
| **Vertical slice** | One small part of the game finished to shipping quality, used to estimate the rest | process-and-playtesting.md |
| **VFX** | Visual effects: particles, beams, trails, flashes | vfx-and-juice.md, vfx-recipes.md |
| **ViewportFrame** | A UI element that renders 3D objects (item previews) | ui-input-crossplatform.md |
| **WaitForChild** | Pauses until a named child exists. Needed on the client; give it a timeout when streaming | engineering-architecture.md |
| **Wally** | Package manager for Luau libraries | engineering-architecture.md |
| **Weld / WeldConstraint** | Joins parts so they move as one assembly | physics-and-vehicles.md |
| **Whale** | A player who spends far more than average | monetization-and-policy.md |
| **Workspace** | The container for everything that exists in the 3D world | engineering-architecture.md |
| **Yield** | When code pauses and lets other code run (`task.wait`, any `…Async` call) | luau-mastery.md |
| **Zap / Blink** | Tools that generate typed, compact networking code from a schema | networking-and-security.md |
| **Zone** | A region of the map that is also a step of progression | level-design-worldbuilding.md |

## Level-up: words that flag a problem in an existing game

| Heard or found | Usually means | Open |
|---|---|---|
| "FE bypass", "they are firing my remotes" | Remotes carry outcomes or lack validation | networking-and-security.md |
| "Free model", "I got it from the Toolbox" | Possible backdoor; house rule 1 violation | networking-and-security.md, art-pipeline-blender.md |
| "Leaderstats saving" | Hand-rolled DataStore code with no session lock | data-and-purchases.md |
| `wait(`, `spawn(`, `LoadAnimation` on a Humanoid, BodyVelocity | Tutorial-era or AI-pasted code | engineering-architecture.md |
| "Dupe" | A save or trade race; purchase grants not idempotent | data-and-purchases.md, economy-and-progression.md |
| "It only happens in the real game" | Studio-only API, asset permissions, latency | studio-workflow.md |
| "CCU is fine but nobody comes back" | A traffic spike hiding weak D1 | core-loop-tuning.md §5, tutorial-and-onboarding.md, liveops-quests-retention.md |
| "It looks AI", "looks like every other game" | Engine defaults, no style bible, generated or borrowed art | art-direction-and-quality-bar.md |
| "Limited time!" on a timer that restarts | False scarcity: policy and house-rule violation | monetization-and-policy.md |

## Review gate

- [ ] Every term used with a beginner was defined the first time it appeared, in words from this file.
- [ ] Any number quoted from a row marked `[VS]` was re-checked in the routed reference or the official docs.
- [ ] Experience, universe and place were not used interchangeably in instructions that involve ids, data or publishing.
- [ ] House-rule terms (primitive Part, free model, Terrain, paid random item, rewarded video, streak) were used with their house limits.
- [ ] Every file named in a "More" column exists (check `references/INDEX.md`).
- [ ] A new term added to another reference was added here in the same pass, in alphabetical order.

## Sources

Accessed 2026-11-10; routing and the facts on PTR, Roblox Plus and the MicroProfiler shortcut re-checked 2026-11-11 (creator-docs commit 7cbffff).

- Definitions follow the existing references in this skill (the file named in each row), which carry their own sources.
- Roblox/creator-docs, commit ccc2b01 (2026-11-07), `content/en-us/`: `studio/{testing-modes,device-simulator,overview,output}.md`, `scripting/sync.md`, `projects/{collaboration,version-history,place-files,update-games}.md`, `projects/assets/packages.md`, `production/publishing/{publish-games-and-places,kids-and-select}.md`, `production/monetization/roblox-plus.md` and the file list of `production/monetization/`, `creator-rewards.md`, `cloud-services/data-stores/index.md` (read) — https://github.com/Roblox/creator-docs
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `Glossary.md` and `52 Core Concepts/Core Concepts Start Here.md` (read), `INDEX_SLIM.md` (section list skimmed). Used as a coverage check for which terms to include; every definition here is rewritten, and about 200 of the 250 terms are not in its glossary.
- Not verified against a primary source in this pass: the 20-minute idle disconnect and the exact scope of Creator Rewards. Both are marked `[VS]`.
