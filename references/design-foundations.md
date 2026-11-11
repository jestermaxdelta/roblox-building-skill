# Design foundations: fun, motivation, difficulty, FTUE, narrative

Distilled from knowledge-base sections 1.1 to 1.4 and 1.9, plus a 2026-11-10 research pass on spawn and goal clarity. Use this while writing the one-pager, pillars and loops, and when reviewing a design or auditing a live game's first session. The first-minute script, tutorial patterns and onboarding funnel are in tutorial-and-onboarding.md; the working procedure for a built loop (spec format, scorecard, diagnosis table, experiments) is in core-loop-tuning.md. Benchmarks are starting estimates, not laws. Tags: `[official]` Roblox docs, `[community]` forum or third-party practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its "reference project" is one anonymised production game, its timings are rules of thumb), `[VS]` version-sensitive as of 2026-11-10, `[house]` house estimate.

## Start here by level

Terms: **MDA** = mechanics, dynamics, aesthetics (rules, the behaviour they cause, the feeling that results). **FTUE** = first-time user experience, from pressing Play to understanding the loop. **SDT** = self-determination theory (autonomy, competence, relatedness). **Meso / macro / meta loop** = the goal of the next minutes, of one sitting, and of days to weeks.

| Level | Do this | Leave for later |
|---|---|---|
| Beginner | Name one target feeling (§1). Write the loop as verb → feedback → reward (§3). Write the first-minute script (tutorial-and-onboarding.md §2) and check it against the worked example in §7. Put one next-goal line on screen (§7.3). Read the banned list in §5 | Motivation models, DDA, narrative audits |
| Intermediate | Score the paper rubric (§3); fill the SDT matrix (§4); check the difficulty rules and hint ladder (§6); use the genre row in tutorial-and-onboarding.md §10; run the 10-screenshot goal test (§7.3) | Experience Density, Quantic clusters |
| Expert | Pre-mortem the dynamics you will actually get; plot the sawtooth against death heatmaps; segment returning players with `GetPlayerSegmentsAsync` (tutorial-and-onboarding.md §8); test first-reward size and tutorial order as experiments (core-loop-tuning.md §7); audit every reveal and tell against §5 | — |

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

Rules: the loop reads as verb → feedback → reward → repeat and the verb fits in one word. Roblox median session was about 6.6 min with the top 10% near 26 min in GameAnalytics' 2025 report, and 9.8 min (P90 14.7) across titles above 1M MAU in its 2026 report `[community]` `[VS]` (one table with every sample: analytics-and-discovery.md §Benchmarks), so a meso goal completes in 5–10 min and a full macro loop in 15–25 min. Design both a reason to stop and a reason to return. Ask what happens in the 5 seconds after failure (instant retry plus the reason). Uniqueness is a mechanical twist, not a theme ("steal-a game with eggs" is a reskin; "stolen items must be physically carried while ragdolling" is a twist).

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

Owner: tutorial-and-onboarding.md. It holds the beat-by-beat first-minute script with funnel steps and fail conditions (§2), teaching patterns and gates (§3), step design (§4), guidance devices (§5), copy rules (§7), the server step machine with skip, resume and returning players (§8), funnel reading (§9), the first loop per genre (§10), anti-patterns with evidence (§11) and the repair procedure (§14). This section keeps what that guide does not: design-review checks, a worked example, load and spawn (§7.2) and the next-goal HUD (§7.3).

Design-review checks `[house]` (knowledge-base estimates, not measurements): the fantasy reads in the first 5 s, with no login wall, name entry or customisation gate before play; core fun within 3 taps; a taught mechanic is used again within a minute and then combined with the previous one; the tutorial sits inside the fiction; control is never taken away mid-action; over 60% of testers find each key feature by minute 10; 0–1 help requests per tester per 10 min; one strong positive event in the first 10 min; session 2 opens on kept progress and one new thing. Before adding tutorial text, make the goal and the feedback clearer.

Worked first-session example (ragdoll launch incremental), in the beat order of tutorial-and-onboarding.md §2: 0 s spawn on the launch pad facing a landmark ramp, no menu; 3 s one pulsing LAUNCH prompt matching the input device; 6 s first launch with a big distance number and coin burst; 15 s the goal bar appears already 30% full from that launch's coins ("Next launcher: 30/100"); 40 s second and third launches; 60 s the shop button reveals, first choice (power or aim); 90 s a visibly further launch (the aha); 2–3 min first zone boundary; 5 min first free egg with odds shown, index opens; 8–12 min first meso goal, rebirth teased; 15–25 min first rebirth, after which the starter pack may appear once, small and dismissible.

On Roblox: first plays that end inside 60 s or inside 61–180 s are a negative Recommended For You signal `[official]` `[VS]`, so the first reward lands under 30 s and the first upgrade under 2 min. Longer average sessions go with higher D1 (the cut by session length is in analytics-and-discovery.md §Benchmarks). The thumbnail must promise the first minute: metadata that does not match the content is not recommended `[official]`. Mobile-first and text-light: can the loop be completed with icons only? Spawn into a playable area while the rest streams in. No purchase prompt before the first win and minute 10 (house rule).

### 7.1 Tutorial style

Moved to tutorial-and-onboarding.md §3 (eight teaching patterns ranked with evidence; soft gate, HUD reveal, contextual unlock, hard gate) and §8 (returning and lapsed players, `AnalyticsService:GetPlayerSegmentsAsync`). House default: no forced tutorial; a soft-gated, skippable guided first loop, timed hints for players who stall, contextual tips for every secondary system.

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

Worked example of a goal chain `[lihfolk]` (reference project, added because players said they felt "thrown in" after the tutorial): 35 goals generated from the save, not hand-written. The chain opens with entering zone one and killing 5 enemies. Every gate then adds its goals in order (hit the rebirth requirement and rebirth, where that gate demands one; save up its price; open it), every realm adds a boss kill and the step into the realm after it, and the last goal is the final boss. A goal's reward is paid a single time and sized to the player's stage (a gate goal paid 5% of that gate's cost plus a few gems; first kills a small flat amount), shows a progress bar and a trail to its target, and holds the completed bar for 2.5 s before the next goal slides in. For a first session, 3–5 tracked goals are enough ("catch your first fish", "sell for 100 coins", "buy a better rod", "reach the second island"), with any social goal optional. Where the game has quests, seed a real one so a tutorial step completes it: the tutorial then ends on a genuine payout and has taught the quest system.

Tests: take 10 random screenshots across the first 30 minutes (every one shows a goal, its progress and its reward); ask a tester at minute 2 what they are doing and why; log `GoalShown` and `GoalDone` and check that no stretch of the session has no active goal.

Anti-patterns: a quest log that lives only in a menu; five quests at once in session 1; a goal whose reward is hidden; goals stated only in text; moving the goal as the player nears it.

### 7.4 The first five minutes by genre

Moved to tutorial-and-onboarding.md §10 (first loop, pattern, safety and typical failure per genre, and the minute-five checklist); the full loop is in the matching file in `references/genres/`.

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
- [ ] First-minute script and tutorial pass the review gate in tutorial-and-onboarding.md (verb by 15 s, first reward by 30 s, aha by 2 min, first meso goal by 10 min, no purchase prompt inside it, nothing forced).
- [ ] The design-review checks in §7 were run on a build with outside testers, and the counts recorded.
- [ ] Spawn faces the verb with no menu in front of it; control time measured on a 3 GB Android phone.
- [ ] Next-goal line always on screen; 10-screenshot test passed; goal slot never empty; a goal chain or quest takes over when the tutorial ends.
- [ ] The genre row in tutorial-and-onboarding.md §10 is met and its named failure has a counter-measure.
- [ ] Every reveal, tell and decline button checked against the §5 list; the parent test passes.
- [ ] Live game: §7.5 symptoms checked against Creator Analytics before any redesign.

## Sources

Accessed 2026-11-10; DevForum threads re-read on 2026-11-11. "(read)" = opened: docs in the `Roblox/creator-docs` mirror, threads through the DevForum JSON endpoint. Sections 1–6 and 8 come from `references/knowledge-base.md` sections 1.1–1.4 and 1.9 (grep `## 1.1` to `## 1.4`, `## 1.9`), which list their own sources; their thresholds are rules of thumb.

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/core-loops.md, onboarding.md and design-for-roblox.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md (read; first-play bounce windows, mismatched metadata)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/retention.md and engagement.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/players/loading-screens.md (read; the sample's `task.wait(5)`)
- https://devforum.roblox.com/t/does-having-an-in-game-start-menumain-menu-affect-player-retention/2701477 (read; opinions, no measurements)
- https://devforum.roblox.com/t/players-dont-know-how-to-play-my-game/1619037 (read)
- https://devforum.roblox.com/t/my-day-1-retention-is-awful-23-losing-half-my-players-in-under-2-minutes-what-am-i-doing-wrong-with-onboarding/4186434 (read; the "gazillion UI" review)
- Session and retention benchmarks: analytics-and-discovery.md §Benchmarks (GameAnalytics reports, seen through the owner's vault and search summaries)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `LihFolk Vault V2/10 Game Design and Genres/First-Time User Experience and Onboarding.md`, `…/Core Loops and Session Design.md`, `…/Ethical Design and Player Trust.md`, `LihFolk Vault V2/58 Player QoL and Game Tweaks/Loading Screen Skip and First-Session Goals.md`, `LihFolk Vault V2/47 Game Feel and Juice/Reward Moments and Celebrations.md` (read). Ideas adapted and rewritten; nothing copied.
