# Design foundations: fun, motivation, difficulty, FTUE, narrative

Distilled from knowledge-base sections 1.1 to 1.4 and 1.9. Use this while writing the one-pager, pillars, loops and FTUE script, and when reviewing a design. Benchmarks are starting estimates, not laws; `[VS]` marks facts that depend on the Roblox version, market or policy as of 2026-11-08.

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

Core-loop rubric, 0–2 per row, pass at 7/10:

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

On Roblox: show the player's own actions locally first (client prediction), then verify on the server; keep local input-to-feedback under 80 ms regardless of ping. Obbies: checkpoints every 30–90 s of play, a new obstacle type per stage group, each new obstacle followed by an easy repetition. A paid "skip stage" is allowed only on a stage that already offers a free skip route after N failures, and never on a stage made harder to sell skips. Proper collision (house rule 2) prevents "fell through the ledge" deaths that read as unfair.

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

On Roblox: sessions under 60 s and 61–180 s count against you in discovery `[VS]`, so core fun inside 60 s and first reward before 180 s. Games with sessions under 3 min show median D1 of 4.3%; 19–24 min sessions show 11.5% `[VS]`. The thumbnail must promise the first minute; clickbait that doesn't retain is penalised since June 2026 `[VS]`. Mobile-first and text-light: can the loop be completed with icons only? Spawn into a playable area while the rest streams in. No purchase prompt before the first meso goal or 10 minutes, whichever is later. Instrument every FTUE beat as a funnel step and review weekly `[VS]`.

## 8. Light narrative and readable worlds

Player promise = fantasy identity + core action + key conflict + perceivable feedback. It must hold across the pitch (title, thumbnail, description), the first 10 minutes and long-term play. A break between pitch and first 10 minutes causes bounces; between first 10 minutes and long-term causes churn. Theme is not differentiation; worldbuilding is not gameplay.

Environmental storytelling, per area: What happened here? Who lives here? Where is this? Tell it through visuals, audio, animation and UI consistently. The world reacts to big events (weather, banners, NPC chatter, prices).

Lynch's city image for hubs: landmarks, paths, nodes, districts, edges. Audits: skyline (1 global and 2 local landmarks visible, silhouettes distinct in black and white, the brightest/most animated thing is where you want the player to go), squint test (blur a screenshot; paths and interactables still read), no-UI run (a new player finds a named place from directions alone). Put a "weenie" landmark in view from spawn.

On Roblox: players skip text, so the world tells the story. Build a Blender story-prop kit per zone with one palette and shape language; every prop is solid. Meme and real-world IP themes spread fast and age fast `[VS]`; an original coherent world lasts longer. Use diegetic UI where cheap: a Blender-modelled leaderboard, update board or index pedestal.
