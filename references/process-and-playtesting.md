# Process: concept, pillars, prototyping, scope, milestones, playtesting, review

Distilled from knowledge-base sections 1.10 to 1.13 and 2.13. Use this during the concept, one-pager, prototype and review phases, and whenever scope needs cutting. Tags: `[VS]` version-sensitive facts as of 2026-11-08 (re-check at create.roblox.com/docs), `[house]` house rule or estimate.

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | Fill the one-pager (§1) and three pillars (§2). Write a prototype brief with KEEP IF and KILL IF before any code (§4). Watch two outsiders play without helping (§7). Cut by the triage order in §5 | Rubric scoring, weekly experiment SOP, A/B tests |
| Intermediate | Lean GDD parts 1–9 (§3); the right slice for the question, not a vertical slice first (§4); milestone exit criteria (§6); five-tester think-aloud sessions with a written hypothesis (§7); the review rubrics (§8); a postmortem after every launch and major update (§9) | Experiments on small traffic |
| Expert | Pre-registered weekly experiments with guardrail metrics and a rollback owner (§7, sample sizes in analytics-and-discovery.md); triangulated telemetry, observation and interviews; one-way-door decision records (§5); cross-checking rubrics against churn points (§8) | — |

Related: templates/game-one-pager.md, templates/lean-gdd.md and templates/playtest-plan.md are the fill-in forms for §1, §3 and §7; tutorial-and-onboarding.md owns the first-minute script (§2) and the tutorial critique rubric (§13); core-loop-tuning.md owns the loop spec, the loop scorecard (§4) and the experiment procedure (§7); audit-existing-game.md is the process for a game that is already live.

## 1. Concept one-pager

Write one page before building anything. Fields and their tests:

| Field | Content | Test |
|---|---|---|
| Fantasy | Who the player is or feels like | Say it in one breath |
| Core loop | Verb → feedback → reward → repeat | Is the core a single strong verb? |
| Twist | What is mechanically new | Would one screenshot look different from competitors? |
| Audience | Primary, secondary, and who it is NOT for | Names a Quantic Foundry cluster |
| Platform and session | Devices; target session length | Fits Roblox sessions (median 6.6 min in GameAnalytics 2025, 9.8 min for large titles in its 2026 report; analytics-and-discovery.md §Benchmarks) |
| Comp set | 3 comparable games, what you take and where you differ | Honest comps |
| Nested loops | 30 s, 5 min, session, meta | A reason to stop and a reason to return |
| Iceberg | Validation evidence from context to external proof | Intuition counts least |
| Next validation step | Smallest probe that could change the decision | |
| Biggest risk | One sentence | |
| Scope | Full vision vs smallest fun version in person-months | Ratio above 10:1 is fantasy |

Intro formula: "(Title) is a (art direction), (niche) (genre) for (platform) about (story), set (setting), featuring (features)." Titles: unique, searchable, about 3–4 words or 17 characters, containing a non-dictionary word; Roblox titles often use status tags plus a verb phrase `[VS]`.

Six forcing questions: Have you *seen* someone enjoy this? Are the comps really comparable? Is 30 seconds of play enjoyable alone? How does the 1st play differ from the 100th? What is the full-vision to smallest-fun ratio? What have real players actually done with it?

## 2. Pillars and concept order

Pick 3 pillars the whole game obeys ("Every launch is funny", "Progress is never lost", "Better with friends"). Each pillar becomes a measurable rule ("competitive balance" becomes "win-rate variance under 5%"). Every review must be able to name one mechanic that contradicts a pillar; the answer is a cut or a pillar change.

Mandatory concept order: seed → verbs → 2–4 design-nucleus options → alignment between actions and goals → assumption ledger → player promise → core loop → scope gate → validation plan. Never write "tune later" instead of a validation plan. Never add a genre-standard system just because the genre usually has one.

## 3. Lean GDD

A living body of knowledge (wiki, board, sheets), not a monolith. Parts:
1. One-pager and pillars.
2. Loops: every system records the loop it serves, the behaviour it changes, its feedback, its validation metric and its deletion condition.
3. Progression and economy sheet (see economy-and-progression.md).
4. FTUE script, beat by beat (format in tutorial-and-onboarding.md §2).
5. Monetisation plan: products, placement moments, rate limits, ethics checks.
6. Art bible: Blender kit list, palette, shape language, texel density, polygon budgets, and a collision plan per model class.
7. Telemetry plan: every metric names the decision it informs.
8. Cut list and idea bin.
9. Tools and versions (Blender version, export settings).

Gamebook layout: write in the order the player experiences it. On Roblox: before (thumbnail, title, icon, video, page), during (the experience), after (notifications, update day, return visit).

## 4. Prototyping

Prototype brief, filled before any code: QUESTION (one, binary if possible), CORE VERB, THROWAWAY? (yes/no), TIMEBOX (30–90 min for a mechanic, or one sitting), KEEP IF, KILL IF.

| Decision | Signal |
|---|---|
| Keep | A fresh player uses the verb on purpose within about 30 s unprompted and plays "one more time" unasked |
| Kill | The verb only feels good after explanation; fun needs systems far beyond scope; you are adding art or levels to avoid admitting the verb is flat |
| Refactor | One variable is clearly off; retune and retest |

A "keep" authorises a rewrite in the real project, never promotion of spike code.

| Slice | Duration | Question |
|---|---|---|
| Mechanic | 3–7 days | Is the verb fun? |
| Onboarding | 1–2 weeks | Do new players get it within 60 s? |
| Progression | 2–3 weeks | Does the curve pull players forward? |
| Combat | 1–3 weeks | Is moment-to-moment conflict good? |
| Economy | 1–2 weeks (spreadsheet) | Does faucet/sink balance hold? |
| Vertical | 4–8 weeks | Is the full experience shippable at quality? |

Jumping straight to a vertical slice is the most common scope mistake. Score a slice 0–2 on validation value, feasibility, signal clarity, dependency risk and scope discipline; 8–10 is strong, 0–3 is not a prototype. Build the slice you are afraid of.

Prototyping under house rule 1 (no primitive builds ship):
- Lower-risk (recommended): build a small Blender blockout kit early (low-poly ramps, pads, walls, props at target proportions, GLB with simple collision). Prototypes use Blender assets from day one and the kit becomes the base for final art. Costs about half a day to a day.
- Bold: greybox with primitives for 1–3 days in a separate private place that is never published, then rebuild in Blender before any outside test. Needs a release gate: zero visible `Part`, `WedgePart` or `CornerWedgePart` outside the invisible-helpers folder.

Jam-style workflow (section 2.13): hours 0–2 pick the verb and the one question; 2–8 core loop playable; 8–16 feel pass and one zone; 16–24 FTUE, cut everything else. Priority: fun > clarity > performance > polish > sustainability.

## 5. Scope and decisions

- Lake or Ocean: a Lake can be finished; an Ocean cannot. A content list containing "etc." is an Ocean.
- Scope gate tiers: MVP, vertical slice, after demo, pitch concept only, cut. Score each feature 1–5 on promise delivery, behaviour change, unknowns reduced, cost, dependencies.
- Suspect by default: open world, real-time multiplayer modes beyond the default, branching story, complex economy, UGC, live ops, high-precision physics, expensive 3D (every asset is Blender-made, so this applies directly).
- Triage under deadline, in order: Does the core loop work without it? (yes: stretch goal.) Can a player tell it's missing? (no: cut.) Under 30 minutes of work? (no: defer.) Default answer is cut.
- Multiply duration estimates by about 3. Make it work, then work well, then elegant.
- One-way vs two-way doors: record the question, default action, reversibility, options, uncertainty, at most 3 probes with the signal each would give, the chosen probe and a stop rule. Spend validation on hard-to-reverse choices (core currency, server model, art direction).
- Ask: "Which one feature would you cut to ship 3 months early?"

## 6. Milestones

| Milestone | Exit criteria |
|---|---|
| First playable | Core loop closes: start → play → fail/win → restart. Playability 6+/12 |
| Vertical slice | One zone at final quality: Blender art, collision, sound, FTUE. Feel 10+/14 |
| Alpha | All systems in, content incomplete, economy simulated |
| Beta | Content complete, tuning, telemetry live, closed test |
| Launch | Release checklist passed (checklists.md) |
| Live | Fixed weekly update day, events calendar, weekly metrics review |

Worked 4-week solo MVP (heuristic; small incrementals are commonly 2–4 weeks `[VS]`):
- Week 0: one-pager, pillars, Blender blockout kit, mechanic slice (2–3 days), keep or kill.
- Week 1: core loop in the real project; Blender hero assets (launcher, pad, first zone); collision pass.
- Week 2: progression and economy sheet in code; rebirth; shop; collection index; monetisation products wired but rate-limited.
- Week 3: FTUE script, funnel telemetry, feel pass, thumbnails and video; closed test with 16+ testers; bug freeze in the last 2 days.
- Week 4: launch to the 16+ audience; gather 250 engaged plays (under-16 users can't see a new game until then `[VS]`); first weekly update on the fixed day.

Game page is the "before" chapter: 3–5 distinct thumbnails left at least 7 days with personalisation on; a real gameplay video (up to +39% RFY playtime reported `[VS]`); unique title and place with your own twist, since near-duplicate clones are penalised `[VS]`. If the audience skews young, plan how to reach 250 engaged age-checked 16+ players within 60 days (older-skewing hooks, Discord, TikTok) `[VS]`.

Solo pitfalls: over-ambition, isolation, not letting others test, perfectionism.

## 7. Playtesting

| Method | Best for | Sample size |
|---|---|---|
| Self-play | Bugs, obvious feel | Never sufficient alone |
| Uncoached outsider | FTUE confusion | 1–2; two minutes beat an hour of self-play |
| Moderated think-aloud | FTUE and UX | 5 finds about 85% of usability issues; 8–10 recommended |
| Unmoderated telemetry | Funnels, balance, churn | Balance 15–30; retention 30–100+ |
| Closed or open beta | Scale, economy, social | Hundreds |
| A/B test | One variable | In-person comparison: at least 20 per variant, 50+ recommended, and it shows only large usability differences. Live metric tests need hundreds to thousands per arm (table in analytics-and-discovery.md); under about 1,000 DAU compare weekly cohorts instead |
| Regression testing | Nothing regresses | Automate |

Running a session: write a hypothesis ("4 of 5 testers can restate the core conflict within 1 minute"); control build, device, instructions, time; the observer does not help unless the tester is stuck more than 2 minutes; log timestamps of confusion, frustration and delight with severity; interview with "What were you trying to do?", "When did you feel most/least in control?", "What would you tell a friend this game is?", laddering "why" three deep. Never ask leading, compound or defensive questions, "would you pay $5?", or use jargon. Reports never use "fun", "engaging" or "balanced" without concrete definition.

Interpreting: triangulate observation, metrics and interviews (one source is a hypothesis, two a pattern, three high confidence). Systemic issue = 60%+ of testers; segment = one persona; else individual variance. Immediate = clarity; progressive = pacing; threshold = cliff. Severity × frequency decides action. Every metric maps to a decision or stops being collected. Video analysis costs 3–5× session length.

Walkthrough personas: Casual Newcomer, Interested Returner, Dedicated, Hardcore Optimiser, Streamer ("would I clip this?"), Lapsed Returner, Genre Critic. Healthy emotion arc: Curious → Confused → Aha → Empowered. Unhealthy: death spiral, no relief valve, content wall, pay-to-win moment, social decay, complexity cliff, plateau.

On Roblox: test in a private place in the same universe with Team Test or a private server; use Studio's local multi-client server for social mechanics. Recruit adult or 16+ testers through age-appropriate channels; never collect personal data from in-game players or move minors off-platform; use `PolicyService` before showing external links `[VS]`. For in-game A/B tests use Experiments with one Config key (core-loop-tuning.md §7); if you assign variants yourself, hash the `UserId` into stable buckets and log the bucket on every event. Discovery responds to signal changes only after a few days `[VS]`; play-through rates changed meaning after the 12 Oct 2026 measurement change, so never compare across that date `[VS]`.

Weekly experiment SOP: Monday freeze the variant, Tuesday ship, Wednesday quality gates, Thursday check, Friday–Sunday collect, next Monday decide (amplify, iterate, observe, roll back, kill). Pre-register primary, secondary and negative metrics, decision date and rollback owner; one variable per variant; segment by new/returning/existing; rollback is a config switch. A win from misleading UI or anxiety timers, or D1 up with complaints up, is a kill regardless of uplift.

## 8. Review rubrics

| Rubric | Scale | Pass |
|---|---|---|
| Core loop | 0–10 (5 dimensions × 0–2) | 7+; −3 if no target feelings stated |
| Motivation | SDT 0–3, player types 0–3, consonance 0–2, emotional arc 0–2 | 7+; must name who it is NOT for |
| Progression | FTUE 0–2, hooks 0–3, difficulty 0–2, churn points 0–3 (top 3 quit points each with mitigation) | 7+ |
| Economy | Currency clarity, faucets/sinks 0–3, monetisation ethics 0–3, spending tiers 0–2 | 7+; −3 if no faucet/sink map |
| Feel | 7 × 0–2 = 14 (responsiveness, clarity, impact, rhythm, payoff, dead time, overload) | 12–14 "alive" |
| Build playability | 6 × 0–2 = 12 (loop closure, 5+ min session viability, onboarding within 60 s, retry under 5 s, retention signal, peak moment) | 10–12 "play-ready"; 0–3 tech demo |
| Prototype slice | 5 × 0–2 = 10 | 8+ |

Review rules: no sycophancy ("needs balancing" is not a finding; state the imbalance, how it fails and the metric). Designer intent is not player experience. Cross-check sections: does the paywall land at a churn point? Does an offer sit next to a spike? Flag "game slop": stock UI, "click to start" splash, unbranded shop grid; the cohesive Blender art bar applies to UI too. After a retro ask "more fun, or just more complete?", keep at most 3 action items, and if team confidence is under 7/10 plan cuts until it is 8+.

Ten design fallacies: sunk cost (would you start this today?), feature creep (serves a pillar?), complexity bias (depth from interactions, not rules), success theatre (metrics that change no decision), platform mismatch, audience mismatch, retention cargo cult (dailies without a loop worth returning to), monetisation–gameplay conflict (money from removing designed pain), scope optimism, uniqueness fallacy (theme ≠ twist).

Roblox-specific failure modes: reskin clone shipped after the parent peaked (waves peak in 7–8 weeks `[VS]`); clickbait thumbnail the first minute doesn't deliver; tutorial or menu wall; offer at the frustration point or in the first minutes; 4+ currencies or no sinks; absence punishment; empty large server; no fixed update day; leftover primitive Parts or walk-through props.

## 9. Postmortem

After every jam, launch and major update: goal and hypothesis with pre-set thresholds; what happened (D1, D2–7 play days, session length, funnel drop-off, spend days vs predictions); 3–5 things that went right with causes; 3–5 that went wrong with root causes; surprises; a decision per system (amplify, iterate, observe, roll back, kill); at most 3 action items with owner and date; one-line reusable lessons.

## 10. Source conflicts resolved (section 1.13)

- Microtransactions: generic sources prefer cosmetic-only; house rule 3 requires boosts and convenience. Resolution: boosts only speed loops that are already fun, no paid PvP power, the paid multiplier stack capped (permanent ≤ 4× in total, ≤ 8× including timed boosts; economy-and-progression.md owns the cap), offers only at delight peaks.
- Prototype art: greybox-with-primitives sources vs house rule 1. Resolution above (blockout kit recommended).
- Scarcity: only genuine, disclosed limits ("until Dec 31"); never fake stock counts.
- Engagement psychology: BlackBook's manipulation toolkit is banned; use only its analytical audits.
- "Each extra click costs 10% conversion" and "30% randomness": unverified; measure your own funnel.
- Retention benchmarks: Creator Analytics similar-game benchmarks first, then the one table in analytics-and-discovery.md §Benchmarks; generic F2P targets (D1 40%) are not Roblox norms.
- Pacing: compress PC/console milestones 5–10× for Roblox.
- Retention mechanics: cumulative calendars (never a login streak that resets), announced timers, no absence punishment (liveops-quests-retention.md).

## Review gate

- [ ] One-pager filled; the pitch fits one sentence; the scope ratio (full vision to smallest fun version) is under 10:1.
- [ ] Three pillars exist as measurable rules, and the last review named what contradicts them.
- [ ] Every prototype had a brief (question, timebox, KEEP IF, KILL IF) and ended in keep, kill or refactor; no spike code was promoted.
- [ ] Nothing built with primitives left the throwaway place: outside tests used the Blender blockout kit (house rule 1).
- [ ] The current milestone's exit criteria are written and met before the next one starts.
- [ ] Playtests had a written hypothesis, an observer who did not help, and at least five outsiders before a keep decision.
- [ ] Every metric collected maps to a decision; experiments were pre-registered with a guardrail and a rollback owner.
- [ ] Review findings state the failure and the metric, not "needs balancing"; at most three action items per retro.
- [ ] A postmortem exists for the last launch or major update.

## Sources

- `references/knowledge-base.md` sections 1.10–1.13 (concept, prototyping, scope, playtesting, source conflicts) and 2.13 (jam workflow); grep `## 1.10` to `## 1.13` and `## 2.13`. Those sections list their own upstream repositories and the owner's vault notes. No web sources were opened for this file: its sample sizes, timeboxes and rubric thresholds are practitioner rules of thumb, not measurements.
- Market facts tagged `[VS]` (250-play gate, wave length, thumbnail and video figures) come from `references/market-scan-2026-11.md`, a 2026-11-07 snapshot.
