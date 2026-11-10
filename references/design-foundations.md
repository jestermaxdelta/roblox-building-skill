# Design foundations: fun, motivation, difficulty, FTUE, narrative

Distilled from knowledge-base sections 1.1 to 1.4 and 1.9, plus a 2026-11-10 research pass on tutorial style, spawn and goal clarity. Use this while writing the one-pager, pillars, loops and FTUE script, and when reviewing a design or auditing a live game's first session. The working procedure for a built loop (spec format, scorecard, diagnosis table, experiments) is in core-loop-tuning.md. Benchmarks are starting estimates, not laws. Tags: `[official]` Roblox docs, `[community]` forum or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production game, its timings are rules of thumb), `[VS]` version-sensitive as of 2026-11-10, `[house]` house estimate.

## Start here by level

Terms: **MDA** = mechanics, dynamics, aesthetics (rules, the behaviour they cause, the feeling that results). **FTUE** = first-time user experience, from pressing Play to understanding the loop. **SDT** = self-determination theory (autonomy, competence, relatedness). **Meso / macro / meta loop** = the goal of the next minutes, of one sitting, and of days to weeks.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Name one target feeling (§1). Write the loop as verb → feedback → reward (§3). Write the FTUE table in §7 and build the guided first loop (§7.1). Put one next-goal line on screen (§7.3). Read the banned list in §5 | Motivation models, DDA, narrative audits |
| Intermediate | Score the paper rubric (§3); fill the SDT matrix (§4); check the difficulty rules and hint ladder (§6); use the genre row in §7.4; run the 10-screenshot goal test | Experience Density, Quantic clusters |
| Expert | Pre-mortem the dynamics you will actually get; plot the sawtooth against death heatmaps; segment onboarding by `GetPlayerSegmentsAsync`; test first-reward size and tutorial order as experiments (core-loop-tuning.md §7); audit every reveal and tell against §5 | — |

## 1. Design backwards from the feeling (MDA)

Mechanics produce dynamics, which produce aesthetics (feelings). Players experience the reverse, so design the reverse: name the target feeling, choose the dynamics that cause it, then pick mechanics. A design review that does not state its target feelings loses 3 points.

| Aesthetic | Player says | Roblox reference pattern |
|---|---|---|
| Sensation | "That felt great" | Ragdoll physics, launch games, juicy hits |
| Fantasy | "I'm a..." | Roleplay towns, pet owner, anime hero |
| Narrative | "What happens next?" | Story horror chapters, mystery |
| Challenge | "I beat it" | Obbies, tower climbs, boss raids |
| Fellowship | "We did it together" | Co-op survival, friend hangouts |
| Discovery | "I found something" | Secret badges, hidden areas, rare spawns |
| Expression | "Look what I made" | Dress-up, building, house decoration |
| Submission | "I just zone out" | Idle/incremental, fishing, farming |

Rules:
- Pick one primary aesthetic and at most two secondary. Every mechanic serves at least one or goes on the cut list.
- Pre-mortem: imagine the game failed and write the dynamics you *actually* got. ("Win 3 PvP matches a day" became "casuals get stomped and quit"; fix was process goals: "play 3 matches".)
- The primary aesthetic drives the Blender art direction: one palette, one shape language, one texel density.

## 2. Fun is learning (Koster) and the toy test (Schell)

- Every loop needs a learnable pattern with depth. Ask "What's different on the 100th repetition?" If nothing, the loop has a shelf life of minutes.
- Depth means doing it better, not doing more. Rubrics that reward "more content" produce treadmills.
- Toy test: is the micro-loop fun with the reward UI hidden? If launching the ragdoll is not funny on its own, no multiplier saves it.
- Useful Schell lenses: Essential Experience, Surprise, Curiosity, Endogenous Value (do items matter inside the game's own logic?), The Toy, Reward and Punishment.

## 3. Nested loops

| Loop | Duration | Question | Example (ragdoll launch incremental) |
|---|---|---|---|
| Micro (core) | 10–30 s | "What do I do?" | Aim, launch, ragdoll, land, earn distance cash |
| Meso (session goal) | 5–15 min | "What am I working towards?" | Buy a stronger launcher, unlock next zone |
| Macro (session) | One sitting | "Why stop, why come back?" | Hit rebirth threshold, rebirth, see multiplier |
| Meta | Days to weeks | "Who am I here?" | Collection index, rebirth tier, weekly cosmetics |

Rules: the loop reads as verb → feedback → reward → repeat and the verb fits in one word. Roblox median session is about 6.6 min, P90 about 26 min (GameAnalytics 2025 `[VS]`), so a meso goal completes in 5–10 min and a full macro loop in 15–25 min. Design both a reason to stop and a reason to return. Ask what happens in the 5 seconds after failure (instant retry plus the reason). Uniqueness is a mechanical twist, not a theme ("steal-a game with eggs" is a reskin; "stolen items must be physically carried while ragdolling" is a twist).

Conflict: the GameAnalytics 2026 report (500+ titles above 1M MAU, Aug 2025–Jul 2026, seen through search summaries) gives a median session of 9.8 min and median D1 / D7 / D30 of 10.3% / 1.6% / 0.5% `[community]` `[VS]`. Its sample is large titles only, so it reads higher than the 2025 figures above. Both are context; the target is the game's own 50th–90th percentile range in Creator Analytics.

`[official]` Roblox describes the same structure in three parts: minute-to-minute interaction (explore), the most repeated set of actions (fight), and a progression engine (upgrade). If any of the three is missing the loop is not closed.

Core-loop rubric for a paper design, 0–2 per row, pass at 7/10. For a build or a live game use the observable 0–10 scorecard and timing targets in core-loop-tuning.md §1 and §4:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Clarity | Can't state the loop | Stated, feedback unclear | Verb, feedback, reward all obvious |
| Session fit | Fights the platform | Fits with friction | Fits natural sessions |
| Depth | Same on 1st and 100th play | Some mastery | Clear skill/strategy growth |
| Fail state | Punishing or absent | Uninformative | Fast, fair, teaches |
| Uniqueness | Pure clone | Theme twist | Mechanical twist |

The 2025–26 Roblox mega-hits share one spine: income per second → multipliers → rebirth, plus one new verb (steal, grow, kick, throw) `[VS]`. Spend originality on the micro-loop verb, not the economy skeleton.

Experience Density heuristic (diagnostic only): `ED = MD/min × (SF + EB + AR) / CLP` (meaningful decisions per minute, salient feedback, embodiment, atmosphere, cognitive load penalty). Fix order: remove noise, raise feedback quality, tune decision frequency last. Boredom has five causes with different fixes: under-stimulation (add decisions), over-stimulation (cut noise), habituation (vary context), low agency (real choices), low meaning (connect actions to goals). First-hour order: Hook (sell the future) → Loop → Link (early ownership) → Surprise (a peak once the player understands about 80% of the systems).

## 4. Motivation

Self-Determination Theory: autonomy, competence, relatedness, plus novelty as a practical fourth. Retention windows map to needs: FTUE (first 60 s) competence "I can do this"; D1 autonomy "I chose my path"; D7 competence "I'm getting better"; D30 relatedness "my people are here". Recommended For You counts return days at D1, D2–7 and D8–28 `[VS]`; D2–7 rewards varied goals and visible mastery, D8–28 rewards friends, groups and trading.

SDT matrix rule: list every system and tick which needs it serves. A system serving none is cut or redesigned (a bare daily-login calendar is weak; friend combos that hit all four are core).

Quantic Foundry clusters: Action (destruction, excitement), Social (competition, community), Mastery (challenge, strategy), Achievement (completion, power), Immersion (fantasy, story), Creativity (design, discovery). Name the clusters you serve and who you are NOT serving. A design that claims to serve everyone is a red flag.

Intrinsic vs extrinsic: rewards should inform ("you got better"), not control. Never pay players to do something unfun; redesign the task instead (overjustification effect).

Reward schedules: fixed ratio for reliable progress, a light layer of variable ratio for surprise, fixed/variable interval for return reasons. Every variable reward needs a floor: a visible pity counter at 1.5–3× the expected attempts. "30% randomness needed" is unverified opinion. Gambler's-fallacy streak payouts and jackpot patterns are banned.

Cognitive biases, ethical use only:

| Bias | Ethical use | Banned use |
|---|---|---|
| Loss aversion (losses feel about 2× gains) | Protect progress; make losses recoverable | "Your pet dies if you don't log in" |
| Endowed progress (2/10 stamps pre-filled: 34% vs 19% completion) | First goal bar starts partly filled with real tutorial progress | Fake "90% there" bars |
| Goal gradient | Short visible goals, "3 more to go" | Moving the goal as the player nears it |
| Social proof | Server feed: "Ava found a Rainbow Shark!" | Fake purchase toasts, bot players |
| Sunk cost | Show the player's history and collection | Guilt messages |
| Collection drive | Index with silhouettes for undiscovered items | Entries only obtainable through paid random items |

Ludonarrative consonance checks: resources (story says poor, wallet says millions), power, time. Power moment and vulnerable moment more than 20 minutes apart means pacing is too slow.

## 5. Ethics for a young audience (hard rules)

Treat every design as if a 9-year-old plays it with a parent's card `[VS]`. Banned everywhere:
- Fake timers, restarting countdowns, fake red-dot notifications, anxiety timers.
- Offers at the frustration point. A difficulty spike paired with a prompt is ESCALATE: remove the prompt. Never kill the player to sell continues.
- Energy systems that block play; intrusive ads.
- Paying that removes designed pain. Test: "Does paying ENHANCE or REPLACE the fun?"
- Hidden odds. Every paid random item shows odds before purchase; gate with `PolicyService` `[VS]`.
- Absence punishment: crops stop growing, they don't die; pets wait, they don't starve.
- Social shaming: no "poor" tags, spend ranks or exclusion of non-spenders.
- Also banned `[lihfolk]`: confirm-shaming on a decline button (use a neutral "Not now"); a reel that stops one card from the jackpot on anything bought with Robux; suspense "tells" that are randomised instead of derived from the real result (a gold glow must mean the result is gold tier or better); reels that show items the roll could not produce; soft-currency packs at irregular exchange rates that hide the Robux price; auto-modes that spend paid consumables without a fresh opt-in; prompts that urge a player to buy for a friend; a buy button placed where a common button normally sits.
- The parent test `[lihfolk]`: would you explain this feature, as built, to the player's parent without changing a word? If not, it does not ship.

PvP theft (the "Steal a ___" loop) drives sessions and defence purchases but distresses kids and invites cheating `[VS]`. Lower-risk (recommended): thieves take a copy or an income share, 1–3 protected slots, offline protection, a steal-back window, defence products as convenience only. Bold: full theft in opt-in raid servers with a theft-free main mode; higher engagement in that group, split player base, reputational risk.

## 6. Flow, difficulty and fairness

Difficulty follows a sawtooth: rise, dip when a new tool or power arrives, climb above the previous peak. Bad shapes: flat (boring), constant escalation (exhausting), cliff (churn), wrong dip frequency.

| Rule | Threshold | Action |
|---|---|---|
| Spike | A stage more than 2× harder than the previous (fail rate or time) | Smooth, or add a dip before it |
| Death zone | Several spikes within 3 stages | Redesign the section |
| Plateau | 5+ stages flat | Add a mechanic or mastery test |
| Premature spike | Spike before the player has the tool | Move it later |
| Spike plus offer | Monetisation prompt during or after a spike | ESCALATE, remove the prompt |
| Failure cost | Progress lost per failure | 1–5 min fine, 30+ min not |
| Casual tolerance | Consecutive failures before quitting | 1–2 tolerated, 4+ churns |
| Stuck | Time stuck on a main-path puzzle | Never over 15 min |

After 3 failures offer adaptive help, a hint or a skip. Failure should teach and can pay a little consolation currency. Hint ladder: L1 environmental (light the switch, camera nudge), L2 direct after about 5 min (NPC remark), L3 explicit after about 15 min or 5 failures (highlight or skip).

Log every death with position and read the heatmap: clusters at intended tests are fine, clusters on ordinary paths are tuning errors, no deaths anywhere is the boredom zone.

DDA: prefer visible, opt-in assists (mercy shield after N deaths) over hidden manipulation. Never punish experts with hidden difficulty. Never let DDA change monetisation exposure.

Fairness: low skill floor (one verb) and high ceiling (angles, combos, routes). Generous player hitboxes, tight hazard hitboxes. Telegraph danger. No off-screen instant deaths or invisible timers. Favour the player on ties and rounding. Give the last hit point extra value.

Feel thresholds: under 50 ms snappy, 50–80 ms responsive, 80–150 ms sluggish, over 150 ms disconnected. Hit feedback scales with effectiveness.

On Roblox: show the player's own actions locally first (client prediction), then verify on the server; keep local input-to-feedback under 80 ms regardless of ping. Obbies: checkpoints every 30–60 s of expected play (level-design-worldbuilding.md; blogs quote up to 90 s), a new obstacle type per stage group, each new obstacle followed by an easy repetition. A paid "skip stage" is allowed only on a stage that already offers a free skip route after N failures, and never on a stage made harder to sell skips. Proper collision (house rule 2) prevents "fell through the ledge" deaths that read as unfair.

## 7. First-time user experience

| Phase | Window | Must happen | Red flags |
|---|---|---|---|
| Identity | 0–5 s | Player knows the fantasy | Login wall, loading over 5 s, text wall |
| Call to action | 5–15 s | One obvious thing to do | Menus before play, 3+ pulsing buttons |
| First input | 15–30 s | Core verb performed | Cutscene, unskippable dialogue |
| Learning | 30 s–5 min | Aha by about 2 min; cheap first failure; first choice by 3–5 min | 3+ new concepts in 2 min; tutorial over 3 min |
| Commitment | 5–15 min | First meso goal done; stop point and return hook shown | Dead time over 5 s; no visible next goal |
| Session 2+ | Return | Welcome back, progress kept, something new | Absence punishment; offers before the aha |

Benchmarks: first meaningful action under 15 s; aha under 90 s; over 60% find key features by minute 10; 0–1 help requests per 10 min; tutorial completion above 80%; at most 3 tutorial pop-ups in the first 5 min; one strong positive event in the first 10 min; core fun within 3 taps.

Principles: teach by doing in a safe space; progressive disclosure (the shop appears when the player can first afford something); skip genre basics (never explain WASD), explain your twist; put the tutorial in the fiction; re-use a taught mechanic within a minute, then combine it; start the first goal bar partly filled with real progress; before adding tutorial text, make the goal and feedback clearer.

Anti-patterns: text walls, teaching everything up front, taking control mid-action, tutorials that can't be skipped by returners, offers inside the tutorial, name/customisation gates before play, hard failure in the tutorial.

Worked FTUE script (ragdoll launch incremental): 0 s spawn on the launch pad facing a landmark ramp, no menu; 3 s pulsing LAUNCH prompt matching the input device; 6 s first launch with a big distance number and coin burst; 15 s goal bar starts 30% full ("Next launcher: 70% there"); 40 s second and third launches; 60 s shop glows, first choice (power or aim); 90 s visibly further launch (aha); 2–3 min first zone boundary; 5 min first free egg with odds shown, index opens; 8–12 min first meso goal, rebirth teased; 15–25 min first rebirth, after which the starter pack may appear once, small and dismissible.

On Roblox: sessions under 60 s and 61–180 s count against you in discovery `[VS]`, so the first reward lands under 30 s and the first upgrade under 2 min (core-loop-tuning.md §2). Games with sessions under 3 min show median D1 of 4.3%; 19–24 min sessions show 11.5% `[VS]`. The thumbnail must promise the first minute; clickbait that doesn't retain is penalised since June 2026 `[VS]`. Mobile-first and text-light: can the loop be completed with icons only? Spawn into a playable area while the rest streams in. No purchase prompt before the first meso goal or 10 minutes, whichever is later. Instrument every FTUE beat as a funnel step and review weekly `[VS]`. The beat-by-beat script template with funnel steps and fail conditions is in core-loop-tuning.md §2.

### 7.1 Tutorial style: forced, guided or contextual

| Style | Use when | Limits |
|---|---|---|
| Guided first loop: free control, one highlighted target at a time, goal bar already part-filled | Default for every game | Needs the next-goal selector in §7.3 |
| Contextual tip the first time a system is met (shop, index, rebirth, trading) | Every secondary system | Show once; fire on the trigger, not on a timer |
| Timed hint for players who have not acted after most have | Any step where a minority stalls | Delay = time most players need + 1 s (docs example: 11 s); tune 5 s against 10 s with an experiment `[official]` |
| Forced linear tutorial: locked controls, scripted steps | Only where one wrong early action can soft-lock or lose progress | At most 3 steps and 60 s; skippable; never replayed for returners `[house]` |

Evidence: `[official]` docs say use a brief tutorial or contextual tips, avoid long tutorials, end onboarding on a designed moment of joy, and A/B-test steps (their example: a shorter dialogue sequence against a guided arrow). `[community]` single self-reported cases: D1 6% → 15% after a 5-step tutorial became 3; players leaving in the first 30 s fell from 45% to 18% after the spawn area got one clear first action; a counter-case where a more hand-holding tutorial moved session time only from 6 to 6.5 min. No controlled forced-versus-contextual comparison was found. Reading: shortening and clarifying helps; more tutorial does not fix a loop that is not fun.

What a new player may touch before it is taught `[lihfolk]`:

| Gating model | How it works | Good for | Risk |
|---|---|---|---|
| Hard gate | Everything except the current step is disabled | Very small games with two or three verbs | Feels like a cage; experienced players leave |
| Soft gate | Everything works; pointers and rewards follow the script | Most games | Players wander off-script, so the goal line must always be right |
| HUD reveal | Buttons stay hidden until their step, then animate in | Menu-heavy simulators on phones | Skips and mid-tutorial rejoins must reveal everything they passed |
| Contextual unlock | A feature appears when first needed | Large games | Optional features are never found unless a goal points at them |

House default: soft gate plus HUD reveal. The build method (step data, server state machine, patterns, test matrix, a five-version case study with funnel numbers) is in core-loop-tuning.md §3.

Returning players: `AnalyticsService:GetPlayerSegmentsAsync(player)` (server-only) returns coarse buckets such as `UserNewReturningStatus`, `ExperienceActivationStatus` (new, active, lapsed, reactivated), `EngagementLevel` and `UserAcquisitionSource`; `HasData` is false when unavailable `[official]` `[VS]`. Use it with the saved profile to skip the tutorial for returners and show lapsed players a "what's new" recap. House rule: never use the payer buckets to change difficulty, odds or prices.

### 7.2 Load, spawn and the first 60 seconds

- `[official]` "The audience is sensitive to friction and load times"; joining and leaving cost the player nothing, so the first impression decides the session.
- No start menu, play button or cutscene before the verb. `[community]` developers describe menus as friction for casual games; put settings and server choice behind a small HUD button. Round-based games spawn the player into a lobby where the verb already works (practice target, mini-loop) and keep the wait under 30 s.
- The spawn pad faces the first verb target, which is within about 3 s of walking `[house]`. Veterans' builds and effects may be in view as a promise of the future, but nothing they do may cover the first prompt.
- Keep the spawn zone light so control arrives fast on a 3 GB Android phone: instance streaming on, preload only the first-screen UI and spawn-zone assets, load the rest behind play (performance.md). The docs' loading-screen sample holds its screen for a fixed 5 s; do not copy that delay.
- Reference numbers `[lihfolk]` (one production game): loading screen capped at 12 s, skippable after 5 s, new players let in at 8 s whatever had loaded; a polished 27 s intro cutscene disabled because it sat inside the bounce window; the walk from the portal to the first gate cut from about 460 to about 227 studs. Rules of thumb from the same source: control within about 10 s of join, the walk to the first target under 10 s, any cutscene skippable and under 5 s.
- A custom loading screen closes on a ready signal **or** a hard timeout, never on a signal alone; shows real progress or a spinner, never a fake bar; and anything revealed early must tolerate data that has not arrived yet (placeholders) `[lihfolk]`.
- Measure it: seconds from join to `FirstAction` (the `FtueBeat` event in core-loop-tuning.md §7), under-60 s bounce, and the Performance dashboard (crash rate, out-of-memory exits) by device type and place version.

### 7.3 Goal clarity: the "what do I do next" problem

`[official]` Onboarding must teach what to do and why, and surface short, mid and long-term goals "in highly visible places, either in the game-world or the UI"; clear goals are also the first D7 lever. `[community]` Threads from developers with low D1 repeat two causes: players who do not know the objective leave and dislike, and HUD clutter hides the one thing that matters (one reviewer's words: "a gazillion UI").

Next-goal HUD spec `[house]`:

1. One primary goal line is on screen at all times: icon, verb, count, progress bar and reward preview ("Sell 3 more boxes → Conveyor II"). On phones it sits top-centre or under the currency, clear of the right-hand camera-drag area.
2. A selector fills it automatically, in this priority: current tutorial step → an upgrade the player can afford now (the shop button pulses) → the unlock closest to completion → the daily quest closest to completion → the long-term collection. The slot is never empty.
3. A world pointer (a `Beam` from the character, or a Blender arrow above the target) appears only after N seconds without a progress event and disappears on progress. N starts at 11 s in the first minutes and 20–30 s later. A pointer that never goes away stops being read.
4. Three horizons are one tap away: now, this session, long-term (index %, next rebirth, season tier).
5. On completion: celebrate (juice tiers 0–1), then show the next goal within 1 s.
6. One pulsing element at a time; at most 3 goal lines on a phone; nothing in the goal line can require a purchase.
7. When a player out-runs the content, say so: show the next update's real date and point at an evergreen goal (collection, leaderboard, mastery).

Worked example of a goal chain `[lihfolk]` (reference project, added because players said they felt "thrown in" after the tutorial): 35 goals generated from the save, not hand-written. Walk into the first zone; defeat 5 enemies; then for each gate: reach the rebirth requirement and rebirth if the gate needs it, earn the gate price, open it; defeat the realm boss; enter the next realm; and so on to the final boss. Each goal pays once, sized to the player's stage (a gate goal paid 5% of that gate's cost plus a few gems; first kills a small flat amount), shows a progress bar and a trail to its target, and holds the completed bar for 2.5 s before the next goal slides in. For a first session, 3–5 tracked goals are enough ("catch your first fish", "sell for 100 coins", "buy a better rod", "reach the second island"), with any social goal optional. Where the game has quests, seed a real one so a tutorial step completes it: the tutorial then ends on a genuine payout and has taught the quest system.

Tests: take 10 random screenshots across the first 30 minutes (every one shows a goal, its progress and its reward); ask a tester at minute 2 what they are doing and why; log `GoalShown` and `GoalDone` and check that no stretch of the session has no active goal.

Anti-patterns: a quest log that lives only in a menu; five quests at once in session 1; a goal whose reward is hidden; goals stated only in text; moving the goal as the player nears it.

### 7.4 The first five minutes by genre `[lihfolk]`

The principles hold everywhere; the shape does not. Start from the row, then open the genre file in `references/genres/` for the full loop.

| Genre | First 30 s | By 5 min | Teach later | Genre-specific failure |
|---|---|---|---|---|
| Simulator, idle | First collect | Collect, sell, upgrade, first pet or egg; loop closed 3+ times | Rebirth, trading, later zones | A long walk to the first pad; a shop before the first sale |
| Tycoon | Plot claimed, first dropper running | First upgrade bought from income; next purchase visible with its price | Rebirth, automation | An empty plot with nothing affordable |
| Trend (steal, escape, grab) | The verb in the title | First risk event survived or lost with a clear lesson; first stash secured | Defence upgrades, rare variants | Being robbed by a far richer player in minute one: give newcomers a grace window or income-gap limits |
| Obby, platformer | Moving and jumping | Several checkpoints; one new mechanic shown, tried, tested | Skips, speedrun routes | A hard jump before the first checkpoint (first checkpoint within about 20 s) |
| Combat, RPG, battlegrounds | First hit lands | First kill of a weak enemy that belongs to this player; one ability; one upgrade | Combos, builds, PvP | Full-strength enemies; five abilities at once |
| Horror, story | Atmosphere, no threat | First threat met with a long readable warning; first death explained in one sentence | Rare entities, lore | An unfair first death with no lesson |
| Social, roleplay | Owning something (house, car, outfit) | A role picked; first interaction with another player | Jobs, premium items | Any gate before the props and the friends |
| Tower defense | First tower placed at a pointed-out good spot | First waves won; one upgrade before wave 3 | Synergies, modes | Wave 1 can be lost; every stat explained first |
| Survival, co-op | First resource gathered | Shelter or fire; first night survived with friends | Crafting trees | A lonely, dark start with no direction |

By minute five in any genre the player has: closed the loop three or more times, seen a number rise, made one real choice, spent something that changed the verb, seen the long loop (a locked gate with a price, the rebirth button, the rarity ladder), had one designed moment of joy, and been handed the next goal.

Conflict: the LihFolk timeline puts the first verb at 15–30 s and the first big reward at 20–40 s (under 60 s in its checklist), and suggests a favourite prompt 25 s after the tutorial ends. Ours are stricter on purpose: verb by 15 s, first reward by 30 s, and no social or purchase card until the first win and the 600 s grace (house rule). Keep ours; treat theirs as the outer limit.

### 7.5 Level-up: first-session symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Testers cannot state the loop at minute 2 | Verb or reward unclear; too many systems on the HUD | One prompt; progressive disclosure; stronger first-reward feedback |
| Aha arrives after minute 3 | First upgrade costs too much or its effect is a menu stat | Lower the cost or raise starting currency (Config); make the effect visible in the world |
| Players open and close menus repeatedly | Systems shown before they can be used | Hide each button until the player can afford or use it |
| Good first session, weak D1 | No stop point and no stated return hook | Add the macro closure and "what is new tomorrow" (§3) |
| Returners leave early in session 2 | Tutorial replays, or nothing has changed | Skip logic from the profile; welcome-back panel with one new thing |
| Under-60 s bounce high on phones only | Control arrives late, or the first prompt is unreadable on a small screen | §7.2; test on the 3 GB phone |
| "Just another <genre>" feedback | The twist is a theme, not a mechanic | Put the originality in the verb (§3) |

Full metric-by-metric table with experiments: core-loop-tuning.md §6.

## 8. Light narrative and readable worlds

Player promise = fantasy identity + core action + key conflict + perceivable feedback. It must hold across the pitch (title, thumbnail, description), the first 10 minutes and long-term play. A break between pitch and first 10 minutes causes bounces; between first 10 minutes and long-term causes churn. Theme is not differentiation; worldbuilding is not gameplay.

Environmental storytelling, per area: What happened here? Who lives here? Where is this? Tell it through visuals, audio, animation and UI consistently. The world reacts to big events (weather, banners, NPC chatter, prices).

Lynch's city image for hubs: landmarks, paths, nodes, districts, edges. Audits: skyline (1 global and 2 local landmarks visible, silhouettes distinct in black and white, the brightest/most animated thing is where you want the player to go), squint test (blur a screenshot; paths and interactables still read), no-UI run (a new player finds a named place from directions alone). Put a "weenie" landmark in view from spawn.

On Roblox: players skip text, so the world tells the story. Build a Blender story-prop kit per zone with one palette and shape language; every prop is solid. Meme and real-world IP themes spread fast and age fast `[VS]`; an original coherent world lasts longer. Use diegetic UI where cheap: a Blender-modelled leaderboard, update board or index pedestal.

## Review gate

- [ ] Target feelings named: one primary aesthetic, at most two secondary; every mechanic serves one.
- [ ] Loop stated as verb → feedback → reward at all four levels, with a 100th-repetition difference and a reason to stop and to return; paper rubric at 7/10 or better.
- [ ] SDT matrix filled; systems serving no need are cut.
- [ ] No banned pattern from §5 anywhere; every variable reward has a visible floor.
- [ ] Difficulty sawtooth checked for spikes, plateaus and spike-plus-offer; hint ladder present.
- [ ] FTUE written as beats: verb by 15 s, first reward by 30 s, aha by 2 min, first meso goal by 10 min; no purchase prompt inside it.
- [ ] Tutorial is a guided first loop plus contextual tips; any forced part is at most 3 steps, skippable, and never replayed for returners.
- [ ] Spawn faces the verb with no menu in front of it; control time measured on a 3 GB Android phone.
- [ ] Next-goal line always on screen; 10-screenshot test passed; goal slot never empty; a goal chain or quest takes over when the tutorial ends.
- [ ] The genre row in §7.4 is met and its named failure has a counter-measure.
- [ ] Every reveal, tell and decline button checked against the §5 list; the parent test passes.
- [ ] Live game: §7.5 symptoms checked against Creator Analytics before any redesign.

## Sources

Accessed 2026-11-10. "(read)" = opened in the `Roblox/creator-docs` mirror at commit ccc2b01; "(search summary)" = seen only through web search result text. Sections 1–6 and 8 come from `references/knowledge-base.md` sections 1.1–1.4 and 1.9 (grep `## 1.1` to `## 1.4`, `## 1.9`), which list their own sources.

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/core-loops.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/onboarding.md and onboarding-techniques.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/design-for-roblox.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/retention.md and engagement.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/index.md and reference/engine/classes/AnalyticsService.yaml (read; `GetPlayerSegmentsAsync`)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/players/loading-screens.md (read)
- https://www.gameanalytics.com/reports/2026-roblox-report (search summary)
- https://blog.rrqworld.com/roblox-game-retention/ (search summary; 9.8 min session figure)
- https://reddit.sentinel-team.org/subreddits/robloxgamedev/snapshots/2026-04-03T05%3A12%3A52.21453Z (search summary of r/robloxgamedev posts via a third-party mirror; tutorial and spawn cases)
- https://devforum.roblox.com/t/improving-onboarding-for-our-zombie-shooter/3323657 (search summary)
- https://devforum.roblox.com/t/does-having-an-in-game-start-menumain-menu-affect-player-retention/2701477 (search summary)
- https://devforum.roblox.com/t/players-dont-know-how-to-play-my-game/1619037 (search summary)
- https://devforum.roblox.com/t/my-day-1-retention-is-awful-23-losing-half-my-players-in-under-2-minutes-what-am-i-doing-wrong-with-onboarding/4186434 (search summary)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/10 Game Design and Genres/First-Time User Experience and Onboarding.md`, `…/Onboarding by Genre - The First Five Minutes.md`, `…/Core Loops and Session Design.md`, `…/Ethical Design and Player Trust.md`, `LihFolk Vault V2/58 Player QoL and Game Tweaks/Loading Screen Skip and First-Session Goals.md`, `LihFolk Vault V2/47 Game Feel and Juice/Reward Moments and Celebrations.md`, `skills/lihfolk-tutorial/SKILL.md` (read). Ideas adapted and rewritten; nothing copied.
