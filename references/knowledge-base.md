# Roblox Game Design Knowledge Base

A large reference on designing and building efficient, well-thought-out Roblox games. It combines generic game design knowledge that transfers to Roblox with official Roblox documentation and the best open-source Roblox engineering libraries.

- **Status: archive.** This is the original source text, compiled before the Roblox docs site and the DevForum could be read directly. The guides in `references/` were later verified at source and corrected; where a guide and this file differ, the guide is right. Use this file only to dig for background, and check anything you take from it.
- **Compiled:** 2026-11-08, from 31 GitHub repositories (shallow clones, text files only), plus the owner's Roblox market-research vault (snapshot 2026-11-07).
- **Size:** about 90,000 words in five sections.
- **Purpose:** source material for the `roblox-game-design` agent skill, and a deep reference for humans and agents.

## How to use this document

- **Starting a new game:** read Section 1 (design foundations) and Section 3 (Roblox design, monetization, discovery). Then pick a genre playbook in Section 2.11 and the genre loops in Section 3.2.
- **Building systems:** read Section 4 (architecture, networking, security, data, purchases) and Section 2.12 (architecture patterns mapped to Luau).
- **Art, world, UI and performance:** read Section 5. Section 5.7 holds the Blender-to-Roblox pipeline that the house rules require.
- **Before launch:** use the checklists in Sections 1.12, 3.10, 4.11 and 5.13.
- **Version-sensitive facts** are flagged inline (`[VS]`, `[version-sensitive]` or `(version-sensitive)`). Re-check them against the live Creator Docs before relying on them. Each section ends with a conflicts register that lists where sources disagree and how this document resolves it.
- **Sources:** every `##` subsection ends with a `Sources:` line. `creator-docs:<path>` points into `Roblox/creator-docs` under `content/en-us/`. `(general knowledge)` marks well-established material that does not come from the repos. `(vault: ...)` marks third-party market observations from the owner's research vault, not Roblox documentation.

## House rules (override all generic advice in this document)

These are the owner's standing rules for every Roblox game.

1. **Blender for every model.** Every 3D asset is made in Blender: street lamps, roads, signs, cars, workers, buildings, props, literally everything. No primitive-Part builds and no generic marketplace models. The bar is a very high-quality, cohesive, put-together look that avoids the generic "AI slop" style. Blender is driven through the Blender Lab MCP add-on bridge (see the game's `tools/blender_exec.py`). GLB is exported in a separate headless `blender -b` process and uploaded through Open Cloud.
2. **Only Blender models in the game, and everything is solid (strict).** Every visible object in the whole game is a Blender model. No visible primitive Parts and no leftover placeholders ship. Players and NPCs must not be able to walk through solid objects, so every model gets proper collision (a simple collision mesh or a suitable `CollisionFidelity`). Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
3. **Push microtransactions heavily, but never invasively.** Non-invasive is the most important rule of all. Starter-pack and offer popups are small, dismissible, never block play, are well-timed (after a win, not in the first minutes), and are rate-limited. Default product set: timed boosts such as 2× EXP, 2× speed (for example 2× delivery speed for 10 minutes), 2× Cash, Luck and Server Luck (only if the game has luck mechanics), a starter pack, Gift versions of passes, and convenience game passes. Stay within Roblox's monetisation rules: no fake discounts, restarting countdowns or false scarcity.

## Cross-section decisions and open questions

The research surfaced these points where sources conflict with each other or with the house rules.

- **Luck and Server Luck are paid random items.** Roblox's policy lists luck boosts, pity systems and rate-up items as "probability modifier items". Any Luck product needs exact boosted odds shown before purchase and updated live, and must be gated with `PolicyService:GetPolicyInfoForPlayerAsync()` (`ArePaidRandomItemsRestricted`). See Sections 3.5 and 3.8.
- **Prototyping without primitives.** Several sources recommend grey-boxing with primitive Parts. Under house rule 1, use a reusable Blender blockout kit, or grey-box in a throwaway place that never ships. See Sections 1.10 and 2.13.
- **Generative Studio tools.** Roblox Studio MCP tools such as `generate_mesh`, `generate_procedural_model` and `insert_asset` (marketplace) break house rules 1 and 2 for shipped content. Do not use them for anything that ships. See Section 4.10.
- **Terrain.** Roblox Terrain is not a Blender model. A strict reading of house rule 2 bans it; the owner decides per game. The default in this document is Blender ground meshes with collision. See Section 5.13.
- **Framework choice.** Knit is archived. The lower-risk default is plain ModuleScripts with a typed loader (services and controllers with Init/Start). The bolder option is an ECS (jecs) with buffer networking (Blink or Zap). See Section 4.2.
- **Early offers in official samples.** Some official starter-pack and bundle samples prompt players early. That breaks house rule 3; delay offers until after a first win and rate-limit them. See Sections 3.7 and 3.12.

## Source index

Stars are GitHub stars at research time (2026-11-08).

### Roblox-specific

| Repository | Stars | Used for |
|---|---|---|
| Roblox/creator-docs | 895 | Official Creator Docs (1,049 pages): game design, monetization, analytics, promotion, publishing, scripting, security, data stores, performance, art, UI, input. Primary source for Sections 3 to 5 |
| luau-lang/site | 18 (language repo 6,065) | Official Luau docs: types, performance guide, native code generation |
| Roblox/roblox-studio-agent-plugin | 30 | Roblox's official AI assistant plugin: how agents should work in Studio |
| Roblox/open-game-eval | 76 | What Roblox evaluates when AI builds games |
| Sleitnick/Knit, Sleitnick/RbxUtil | 630, 473 | Service/controller framework (archived) and utilities: Signal, Trove, Comm, Component |
| MadStudioRoblox/ProfileStore | 351 | Session-locked player data |
| nezuo/lapis | 82 | Alternative DataStore abstraction |
| evaera/roblox-lua-promise | 353 | Promise-based async |
| Ukendio/jecs | 483 | Entity Component System for Luau |
| 1Axen/blink, red-blox/zap | 192, 190 | Buffer-based networking IDL compilers |
| dphfox/Fusion | 811 | Reactive UI |
| MonzterDev/Roblox-Game-Template | 17 | Example project structure |
| andrian-syh/roblox-best-practices-skill | 13 | Roblox/Luau coding standard packaged as an agent skill |
| awesome-roblox/awesome-roblox, elevenpassin/awesome-roblox | 91, 199 | Tooling ecosystem map |
| dungnotnull/tycoon-game-economy-design-agent-skill | 8 | Tycoon and simulator economy design |

### Generic game design and development

| Repository | Stars | Used for |
|---|---|---|
| gamedev-skills/awesome-gamedev-agent-skills | 7,654 | 77 game-dev agent skills: disciplines, genres, workflows, and Roblox-specific skills |
| munificent/game-programming-patterns | 4,570 | Game Programming Patterns book source, mapped to Luau |
| 2DGD-F0TH/2DGD_F0TH | 465 | Community compendium on game design and development |
| Roobyx/awesome-game-design | 708 | Curated game design learning map |
| kkga/gamedesign-playlist | 313 | Curated articles, books and talks |
| DY-2026/GameDesignOS | 452 | Evidence-driven design methodology for AI agents |
| fagemx/gstack-game | 81 | 27 game production skills: concept, design review, playtest, ship |
| momowangOUO/GameDev-BlackBook | 129 | Formula-driven design and monetization audits (analytical parts only) |
| deepnight/gamefeel | 243 | Game feel talk demo |
| Shupianmaka/codex-game-ux-skills | 13 | Game UX skills |
| r-lyeh/gamebook, kosinaz/game-design-document-template-for-beginners | 47, 42 | GDD conventions and templates |
| ellisonleao/magictools, Kavex/GameDev-Resources | 17,720, 7,153 | Resource lists (further reading only) |

### Also used

- The owner's research vault, `Roblox Research/2026-11 Market Scan/` (snapshot 2026-11-07): discovery, Recommended For You, thumbnails, genre and market patterns. Market numbers are a snapshot and go stale.

### Deliberately excluded

- Dozens of recently created, SEO-styled repos ("Best ... 2026", around 70 stars each) that looked like spam or malware lures.
- Exploit, cheat, macro and account-manager repos.
- Engine-specific tooling for Unity, Godot or Unreal with no design content.

## Section map

1. **Game Design Foundations, Psychology and Process:** fun (MDA, Koster, Schell, loops), motivation and ethics, flow and difficulty, FTUE, progression math, economy math, social design, retention, narrative, process from one-pager to live game, playtesting, review rubrics, failure modes.
2. **Game Craft Disciplines, Genre Playbooks and Architecture Patterns:** game feel and juice, level design, UI/UX, camera, input, audio, AI, procedural generation, saves, physics, 14 genre playbooks, all 19 Game Programming Patterns in Luau, prototyping and jams.
3. **Roblox Game Design, Monetization, Analytics, LiveOps and Discovery:** platform realities, genre loops, onboarding, quests and LiveOps, economy math, every monetization product with fees and payouts, the non-invasive monetization playbook, policy, analytics and experiments, discovery and launch, scaling and matchmaking.
4. **Roblox Engineering:** client-server model, project architecture, Luau standards, networking, security with a remote guard and rate limiter, ProfileStore data, idempotent ProcessReceipt and game passes, teleports and cross-server, Parallel Luau, tooling, CI/CD and AI agents, common bugs.
5. **Roblox Performance, World Building, Art Pipeline, UI and Cross-Platform:** frame budgets and profiling, Luau performance, rendering, streaming, physics and collision, the Blender-to-Open-Cloud pipeline, lighting, VFX, animation, audio, UI implementation, cross-platform input and accessibility, loading, pre-launch checklist.

---


---

# 1. Game Design Foundations, Psychology and Process

This section covers general game design theory and turns each idea into practical guidance for Roblox. It spans three files, meant to be read in order:

- `01-design-foundations.md` (this file): how to use the section, the house rules, fun and loops, motivation and psychology, flow and difficulty, and onboarding.
- `01-design-foundations-part2.md`: progression, economy and balance math, social design, retention, and light narrative.
- `01-design-foundations-part3.md`: process from concept to launch, playtesting, review rubrics, failure modes, postmortems, and a list of contradictions between sources and how they are resolved.

## 1.0 How to use this section

**Who it is for.** A designer, or an AI agent acting as one, who is planning, building, reviewing or fixing a Roblox experience. Each topic gives the theory first, then the numbers and decision rules, and ends with an **On Roblox:** block that turns the idea into platform practice.

**Conventions.**

- `[VS]` marks a claim that depends on the version of Roblox, the market or a policy, and could change. Every `[VS]` claim was true as far as the sources show on **2026-11-08**. Check it again before you rely on it.
- Benchmarks are **starting estimates, not laws**. The source repos say so themselves. Calibrate them against your own analytics after launch.
- Each `##` subsection ends with a `Sources:` line. Paths are `owner/repo:path`.
  - `(general knowledge)` marks widely published design knowledge that is not in the source repos, such as named books, studies and formulas.
  - `(Delta Vault: …)` marks the owner's Roblox market-research knowledge base. Its data snapshot is from 2026-11-07.

**House rules.** These apply to every recommendation in this section. Nothing here overrides them.

1. **Blender for every visible asset.** Lamps, roads, signs, vehicles, NPCs, buildings and props are all modelled in Blender, exported as GLB and uploaded through Open Cloud. Primitive-Part builds and generic marketplace models never ship. The look must be cohesive and high quality, not generic "AI slop".
2. **Everything visible is solid.** Every visible model has proper collision, through a simple collision mesh or a suitable `CollisionFidelity`. Players and NPCs never walk through solid objects. Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
3. **Monetise heavily, but never invasively.** Offers are small, dismissible, well timed (after a win, never in the first minutes) and rate-limited. The default product set is:
   - timed 2× boosts (EXP, speed, cash);
   - Luck and Server Luck, but only if the game has luck mechanics;
   - a starter pack;
   - Gift versions of passes;
   - convenience passes.

   Fake discounts, countdowns that restart and false scarcity are banned.

**The one-paragraph version of this whole section.**

- Decide the feeling first (aesthetics), then design the dynamics and mechanics that produce it.
- Make the 10–30 second loop fun with no rewards attached. Then nest a 5–15 minute loop and a multi-day loop around it.
- Get a new player to the fun inside 60 seconds and to a visible "number go up" or first reward before 3 minutes. Roblox discovery penalises sessions that end before 60 seconds or within 61–180 seconds `[VS]`.
- Pace progression by time, not by XP. Keep the economy's faucets and sinks near balance.
- Give players reasons to return across several days and to bring friends. Do it without punishing absence, without obligations and without manipulating children.
- Prototype the one risky question cheaply. Test with real players. Cut scope ruthlessly. Review against written rubrics instead of gut feeling.

Sources: fagemx/gstack-game:ETHOS.md, fagemx/gstack-game:skills/game-review/references/gotchas.md, (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/First-Play Bounce Rate.md, New Game Launch Checklist.md)

---

## 1.1 What makes games fun

### 1.1.1 MDA: design backwards from the feeling

The MDA framework (Hunicke, LeBlanc and Zubek, 2004) splits a game into three layers:

- **Mechanics**: rules, verbs and data.
- **Dynamics**: the behaviour that emerges when players use the mechanics.
- **Aesthetics**: the emotions the player feels.

The designer builds mechanics, then dynamics, then aesthetics. The player experiences them the other way round. So you design backwards: name the target feeling, choose the dynamics that cause it, and only then pick the mechanics. gstack-game deducts 3 points from any design review that does not state its target feelings.

The eight MDA aesthetics, with Roblox reference points:

| Aesthetic | Player says | Roblox reference pattern |
|---|---|---|
| Sensation | "That felt great" | Ragdoll physics, launch games, juicy hits |
| Fantasy | "I'm a…" | Roleplay towns, pet owner, anime hero |
| Narrative | "What happens next?" | Story horror chapters, mystery games |
| Challenge | "I beat it" | Obbies, tower climbs, boss raids |
| Fellowship | "We did it together" | Co-op survival, friend hangouts |
| Discovery | "I found something" | Secret badges, hidden areas, rare spawns |
| Expression | "Look what I made" | Avatar dress-up, building, house decoration |
| Submission | "I just zone out" | Idle and incremental games, fishing, farming |

Rules:

- Pick **one primary aesthetic and at most two secondary ones**. Every mechanic must serve at least one of them. A mechanic that serves none is cut, or must justify itself in the cut list.
- **The pre-mortem MDA test.** Imagine the game has launched and failed. Write down the dynamics and aesthetics you *actually* got, not the ones you intended.
  - BlackBook's worked example: "Win 3 PvP matches a day to level the battle pass." The real dynamics were that players used only the strongest loadout, casual players got stomped and logged off after two losses, and the pass felt like a job.
  - The fix was to make the goal about the process ("play 3 matches" or "deal X damage"), not the result.

### 1.1.2 Koster: fun is learning

Raph Koster's *A Theory of Fun* argues that fun is the feeling of the brain learning a pattern. Boredom arrives when the pattern is fully learned or can't be learned at all. This gives two practical rules:

- **Every loop needs a learnable pattern with depth.** gstack asks: "What's different on the 100th repetition?" If the answer is "nothing", the loop has a shelf life of minutes.
- **Depth means doing it better, not doing more.** A rubric that rewards "more content" over "more mastery" will produce a treadmill.

### 1.1.3 Schell's lenses: questions as tools

Jesse Schell's *The Art of Game Design* gives more than 100 "lenses": short sets of questions to view a design through. The ones most useful on Roblox:

- **Essential Experience.** What experience should the player have, and what is the minimum that delivers it?
- **Surprise.** What will surprise players, and when? This feeds rare spawns and events.
- **Curiosity.** What questions does the game put in the player's mind?
- **Endogenous Value.** Do the items and currencies matter *inside* the game's own logic?
- **The Toy.** Is it fun to play with even with no goal? This is the "30-second loop with zero rewards" test.
- **Reward and Punishment.** Is the reward schedule tuned? Is punishment fair and does it teach?

### 1.1.4 Nested loops

| Loop | Duration | Question it answers | Example (ragdoll launch incremental) |
|---|---|---|---|
| Micro (core) | 10–30 s | "What do I do?" | Aim, launch, ragdoll, land, earn distance cash |
| Meso (session goal) | 5–15 min | "What am I working towards?" | Buy a stronger launcher, unlock the next zone |
| Macro (session) | One sitting | "Why stop, and why come back?" | Hit the rebirth threshold, rebirth, see the new multiplier |
| Meta | Days to weeks | "Who am I in this game?" | Collection index, rebirth tier, weekly event cosmetics |

Rules for loops:

1. **Clarity.** The loop reads as *verb → feedback → reward → repeat*. If a player can't say the verb in one word, the loop isn't clear.
2. **Session fit.** The meso loop fits the platform's real sessions. On Roblox the median per-user session is about 6.6 minutes and the 90th percentile is about 26 minutes (GameAnalytics 2025 `[VS]`). So a meso goal should complete in 5–10 minutes, and a full macro loop in 15–25 minutes.
3. **A reason to STOP and a reason to RETURN.** Both must be designed. With no natural stopping point, players leave frustrated. With no hook, they never return.
4. **Fail state.** Ask what happens in the 5 seconds after a failure. A good answer is an instant retry plus information about why it failed.
5. **Uniqueness.** Finish the sentence "It's the game where you…" with a mechanical twist, not a theme. "It's the steal-a game but with eggs" is a reskin. "It's the steal-a game where stolen items have to be physically carried while ragdolling" is a twist.

gstack's core-loop rubric scores each dimension 0–2 for a total out of 10:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Clarity | Can't state the loop | Loop is stated but feedback is unclear | Verb, feedback and reward are all obvious |
| Session fit | Loop length fights the platform | Fits with friction | Fits natural sessions |
| Depth | Same on the 1st and 100th play | Some mastery | Clear skill or strategy growth |
| Fail state | Punishing or absent | Exists but uninformative | Fast, fair, teaches |
| Uniqueness | Pure clone | Theme twist | Mechanical twist |

Key questions:

- "Is the 30-second loop fun with zero rewards?"
- "What's different on the 100th repetition?"
- "What happens in the 5 seconds after failure?"

### 1.1.5 Experience density and the four-step experience (GameDesignOS)

GameDesignOS offers an **Experience Density** heuristic. It is a diagnostic aid, not science:

> **ED = MD/min × (SF + EB + AR) / CLP**
>
> - MD/min = meaningful decisions per minute
> - SF = salient feedback
> - EB = embodiment (the feel of controlling the character)
> - AR = atmosphere and resonance
> - CLP = cognitive load penalty

How to use ED:

1. **Find the stimulation window.** Is the experience too low, optimal, too high, or uneven?
2. **Remove noise first** (lower CLP).
3. **Raise quality** (SF, EB, AR).
4. **Tune the frequency of decisions** (MD/min) last.

Boredom has five different causes, and each needs a different fix:

- **Under-stimulation**: add decisions.
- **Over-stimulation**: cut noise.
- **Habituation**: vary the context. Use alternative uses, combinations and reframing.
- **Low agency**: give real choices.
- **Low meaning**: connect actions to goals.

The **Hook → Loop → Link → Surprise** method gives a simple order for the first hour:

1. **Hook**: sell the future first. Show the player what they can become.
2. **Loop**: each reward fuels the next round.
3. **Link**: give early ownership and a sketch of the world.
4. **Surprise**: deliver a peak once the player understands about 80% of the systems. Before that it is noise. After that it is too late.

**On Roblox:**

- **The 2025–26 hits share one spine.** The owner's market scan found every recent mega-hit built on *income per second → multipliers → rebirth*, with **one new verb on top** (steal, grow, kick, throw) `[VS]`.
  - Treat this spine as the macro and meta structure.
  - Spend your design originality on the **micro-loop verb**, which is where the fun lives. Don't spend it on the economy skeleton.
- **Pick the primary aesthetic from the audience, then let it drive the visual target.**
  - Sensation games need physics feel and juicy feedback.
  - Expression games need deep customisation.
  - Submission games need calm, readable numbers.
  - Under house rule 1, the aesthetic also drives the Blender art direction: one palette, one shape language and one texel density for every model.
- **Run the "toy test" on the micro-loop with the reward UI hidden.** If launching a ragdoll is not funny on its own, no multiplier will save it.

Sources: fagemx/gstack-game:skills/game-review/references/core-loop.md, fagemx/gstack-game:skills/game-ideation/SKILL.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/ed-framework.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/density-formula.zh-CN.md, DY-2026/GameDesignOS:game-experience-analyzer/references/four-step-experience-method.zh-CN.md, DY-2026/GameDesignOS:game-concept-architect/references/core-loop-expansion.zh-CN.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch1 Tool 3), 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/003_Consolidating_Mechanics.md, (general knowledge: Hunicke/LeBlanc/Zubek MDA 2004; Koster *A Theory of Fun*; Schell *The Art of Game Design*), (Delta Vault: Roblox Research/2026-11 Market Scan/Patterns/Income Per Second to Multiplier to Rebirth.md, One New Verb on the Idle Core.md; Algorithm/Retention Benchmarks.md)

---

## 1.2 Motivation and player psychology

### 1.2.1 Self-Determination Theory (SDT)

Deci and Ryan's SDT says people are intrinsically motivated when three needs are met:

- **Autonomy**: meaningful choice.
- **Competence**: growing mastery.
- **Relatedness**: connection to others.

GameDesignOS adds **novelty** as a practical fourth need: material that is half familiar and half new. gstack ties retention windows to these needs:

| Window | Dominant need | What the player must feel |
|---|---|---|
| FTUE (first 60 s) | Competence | "I can do this" |
| D1 | Autonomy | "I chose my path" |
| D7 | Competence | "I'm getting better" |
| D30 | Relatedness | "My people are here" |

**SDT matrix rule.** List every system and tick the needs it serves. A system that serves no need does not motivate anyone. Cut it or redesign it.

| System | Autonomy | Competence | Relatedness | Novelty | Verdict |
|---|---|---|---|---|---|
| Launcher upgrades | Choice of path ✓ | Distance grows ✓ | — | — | Keep |
| Daily login calendar | — | — | — | Small | Weak. Pair it with a choice of reward |
| Friend launch combos | ✓ | ✓ | ✓ | ✓ | Core. Invest here |
| Generic achievement list | — | Weak | — | — | Cut or make it social |

### 1.2.2 Player taxonomies: Bartle and Quantic Foundry

**Bartle (1996)** sorts players on two axes: acting on or interacting with, and the world or other players. That gives four types:

- **Achievers**: act on the world.
- **Explorers**: interact with the world.
- **Socialisers**: interact with players.
- **Killers**: act on players.

It is a useful vocabulary, but it was derived from MUD players.

**Quantic Foundry's Gamer Motivation Model** comes from survey data on more than a million gamers `[VS]`. It has 12 motivations in 6 clusters:

| Cluster | Motivations | Roblox hooks |
|---|---|---|
| Action | Destruction, Excitement | Ragdoll chaos, explosions, PvP |
| Social | Competition, Community | Leaderboards, groups, hangouts |
| Mastery | Challenge, Strategy | Obbies, build optimisation |
| Achievement | Completion, Power | Collection index, rebirth tiers |
| Immersion | Fantasy, Story | Roleplay, horror chapters |
| Creativity | Design, Discovery | Building, outfits, secrets |

**Rule.** Name the clusters you serve, and **name who you are NOT serving**. gstack treats a design that claims to serve everyone as a red flag. The concept one-pager has an explicit "NOT for" line.

### 1.2.3 Intrinsic and extrinsic motivation

**Intrinsic motivation** is doing something because it is enjoyable. **Extrinsic motivation** is doing it for a reward.

**The overjustification effect.** Big external rewards for an activity people already enjoy can reduce their intrinsic interest once the rewards stop. This was shown with children and drawing (Lepper, Greene and Nisbett, 1973).

Design implications:

- Rewards should **inform** the player ("you got better") rather than **control** them ("do this or lose that").
- Make the micro-loop intrinsically fun. Use extrinsic rewards (cash, XP, items) to give **direction**, not to replace fun.
- **Never pay players to do something unfun.** If a task needs a bribe, redesign the task.

### 1.2.4 Reward schedules

| Schedule | Definition | Game use | Danger |
|---|---|---|---|
| Fixed ratio (FR) | Reward every N actions | "10 launches = chest" | Predictable. Can feel like work |
| Variable ratio (VR) | Reward after a random number of actions | Drops, crits, rare spawns | The most compulsive schedule. This is the slot-machine pattern |
| Fixed interval (FI) | Reward after time T | Daily login, restock timers | FOMO and the "chore" feeling |
| Variable interval (VI) | Reward at random times | Surprise events, meteor showers | Players camp and idle-farm |

Rules:

- Mix the schedules. Use FR for reliable progress, a light layer of VR for surprise, and FI or VI for return reasons.
- **Every variable reward must have a floor.** That means a visible pity counter or a guaranteed minimum. Set pity at **1.5–3× the expected number of attempts** and make it visible. Going past 2× the expected attempts without a payout feels broken.
- BlackBook claims a core action needs "30% randomness" or it feels like work. **Treat that as an unverified opinion**, not a benchmark.
- BlackBook's "how to create greed" row recommends gambler's-fallacy streak payouts and Skinner-box jackpots. **Do not use those techniques**, especially with a young audience (see 1.2.7).

### 1.2.5 Cognitive biases you will meet

| Bias | Finding | Ethical use | Exploitative use (banned) |
|---|---|---|---|
| **Loss aversion** | Losses feel about 2× as strong as equal gains (Kahneman and Tversky; λ is roughly 2–2.25) | Protect hard-won progress. Make losses recoverable | "Your pet will die if you don't log in"; threatening to destroy progress |
| **Endowed progress** | A loyalty card with 2 of 10 stamps already filled was completed more often than a blank 8-stamp card: 34% vs 19% (Nunes and Drèze, 2006) | Start the first goal bar partly filled with real, earned progress from the tutorial | Fake "you're 90% there!" bars |
| **Goal-gradient** | Effort speeds up near a goal (Hull; Kivetz et al. 2006) | Shorter, visible goals; show "3 more to go" | Moving the goal just as the player gets close |
| **Zeigarnik effect** | Unfinished tasks stay in mind. Replications are mixed, so treat it as weak | End sessions with a visible next goal | Pop-ups nagging about "unfinished" tasks |
| **Social proof** | People copy what others do (Cialdini) | Server feed: "Ava found a Rainbow Shark!" | Fake purchase notifications; bot "players" |
| **Sunk cost** | People keep investing to justify past investment | Value players' collections and show their history | "Your level-60 warrior is waiting…" guilt messages |
| **Collection drive** | Completing sets is motivating in itself | Index with silhouettes for undiscovered items | Index entries you can only get through paid random items |

### 1.2.6 Ludonarrative consonance

The mechanics must say the same thing as the fiction. BlackBook gives three checks:

- **Resources.** The story says you're poor, but you carry millions.
- **Power.** The story says you're badly hurt, but you parkour at full health.
- **Time.** The story says the bomb explodes in 5 minutes, but you can fish for 20.

gstack scores consonance 0–2 and asks:

- Where is the **power moment**?
- Where is the **vulnerable moment**?
- How far apart are they? More than 20 minutes apart means the pacing is too slow.

### 1.2.7 Ethics and dark patterns for a young audience

A large share of Roblox users are under 13, and many more are teenagers `[VS]`. Treat every design as if a 9-year-old will play it with a parent's card. The sources agree on the red lines below. They are banned in every game:

- **No fake timers or restarting countdowns.** No red-dot "notifications" that are not real news. No anxiety timers to push purchases. GameDesignOS lists these as kill criteria in experiments, and house rule 3 bans them.
- **No paywall at the frustration point.** Offers appear at **delight** peaks, never when the player is failing.
  - gstack flags a difficulty spike paired with a monetisation prompt as **ESCALATE**.
  - 2DGD says: don't kill the player to sell continues.
- **No energy systems that block play**, and no intrusive ads (2DGD).
- **Paying must enhance the fun, not remove designed pain.** gstack's test is "Does paying ENHANCE or REPLACE the fun?" If you designed the pain so you could sell the cure, the design is broken.
- **No "surprise mechanics" euphemisms.** Every paid random item shows its odds before purchase. Roblox requires this for paid random items, and some regions restrict them. Check `PolicyService` `[VS]`.
- **No absence punishment.** Crops stop growing rather than dying. Pets wait rather than starve. Cozy-game design from BlackBook: "always welcome the player back."
- **No social shaming.** No "poor" tags, no public spend ranks, no exclusion of non-spenders.
- **Do not copy BlackBook's manipulation toolkit.** Its README calls the book "selling anxiety" and "legal addiction". Use it only for its analytical frameworks:
  - Lynch's city image;
  - environmental-storytelling audits;
  - hint grading;
  - social-friction audits.

  Do not use its "engineering addiction" tactics.

**The loss-aversion PvP theft problem.** "Steal a ___" games show that the threat of theft drives session length and defence purchases. They also cause distressed kids, complaints and cheating `[VS]`. Two options:

- **Lower-risk (recommended).**
  - Thieves take a *copy* or a *share of income*, not the item itself.
  - Each player keeps 1–3 protected slots.
  - Bases have offline protection.
  - The victim gets a short steal-back window.
  - Defence products are convenience (a longer lock, an alarm), never the only way to stay safe.
- **Bold.** Full item theft in opt-in "raid" servers only, with clear labelling and a theft-free main mode. Higher engagement in the opted-in group, but it splits the player base and still carries reputational risk.

**On Roblox:**

- **Design for SDT across the retention windows the algorithm measures.** Since June 2026, Recommended For You counts return days at D1, D2–7 and D8–28 `[VS]`.
  - The D2–7 window rewards autonomy and competence: varied goals and visible mastery.
  - The D8–28 window rewards relatedness: friends, groups and trading communities.
- **Make social proof real and positive.** Server-wide toasts for rare finds, and a "Server Luck active, thanks to @name" banner when someone buys Server Luck. Generosity is a social-proof moment that is not invasive.
- **Collection index.** Show silhouettes of undiscovered items and the number found. Make every index entry obtainable through play.
  - Paid luck may speed up the hunt. It must never be the only route.
  - Luck products exist only because this game has luck mechanics, as house rule 3 requires.
- **Use `PolicyService:GetPolicyInfoForPlayerAsync`** to respect regional rules on paid random items and paid trading, and to check which external-link references are allowed for each user `[VS]`.

Sources: fagemx/gstack-game:skills/game-review/references/motivation.md, fagemx/gstack-game:skills/game-review/references/progression.md, fagemx/gstack-game:skills/game-review/references/economy.md, fagemx/gstack-game:skills/balance-review/references/progression.md, fagemx/gstack-game:skills/balance-review/references/difficulty-curve.md, fagemx/gstack-game:skills/game-direction/SKILL.md, fagemx/gstack-game:skills/game-ideation/SKILL.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/flow-sdt-experience-gates.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/lever-playbook.zh-CN.md, momowangOUO/GameDev-BlackBook:README.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch1 Tool 2, Ch2 Hook Audit, Ch5 Ludonarrative Check, Ch11 Stressor Elimination Audit), 2DGD-F0TH/2DGD_F0TH:chapters/008_Marketing_Community/001_Marketing/006_F2P.md, (general knowledge: Deci and Ryan SDT; Bartle 1996; Quantic Foundry Gamer Motivation Model; Lepper, Greene and Nisbett 1973; Kahneman and Tversky prospect theory; Nunes and Drèze 2006; Kivetz et al. 2006; Cialdini), (Delta Vault: Roblox Research/2026-11 Market Scan/Patterns/Loss Aversion Through PvP Theft.md, Collection Index and Trading.md; Algorithm/28-Day Retention Window.md)

---

## 1.3 Flow, difficulty and fairness

### 1.3.1 The flow channel

Csikszentmihalyi's flow is a state of absorbed, focused enjoyment. It happens when challenge roughly matches skill, goals are clear and feedback is immediate. If challenge is far above skill, the player feels anxiety. If it is far below, the player feels boredom. Skill grows as the player plays, so challenge must rise too, but not in a straight line.

**The sawtooth.** The healthiest difficulty curve rises, then dips when a new mechanic or power arrives, then climbs above the previous peak.

```
challenge
  ^            /|        /|
  |       /|  / |   /|  / |
  |  /|  / | /  |  / | /  |     each dip = new tool or power ("I'm strong now")
  | / | /  |/   | /  |/   |     each climb = mastery test
  |/  |/        |/
  +-------------------------------> time
```

Bad curve shapes (gstack):

- **Flat**: boring.
- **Constant escalation**: exhausting.
- **Cliff**: churn.
- **Wrong frequency**: dips too rare or too frequent.

2DGD lists other legitimate shapes: logarithmic, linear waves, and widening intervals. Some games are *meant* not to be about difficulty, such as comedy, relaxation and collectathons.

### 1.3.2 Measurable difficulty rules

| Rule | Threshold | Action |
|---|---|---|
| Spike | A level or stage is more than 2× harder than the previous one (measured by fail rate or time) | Smooth it, or add a dip before it |
| Death zone | Several spikes within 3 consecutive stages | Redesign the section |
| Plateau | 5 or more stages with flat difficulty | Add a new mechanic or a mastery test |
| Premature spike | A spike before the player has the tool to beat it | Move it later |
| Spike plus offer | A monetisation prompt during or after a spike | **ESCALATE. Remove the prompt** |
| Failure cost | Progress lost to one failure | 1–5 min is fine. 30+ min is not |
| Casual failure tolerance | Consecutive failures before quitting | 1–2 is tolerated. 4 or more means churn |
| Stuck on a puzzle | Time stuck on a main-path puzzle | Never more than 15 min (see the hint ladder) |

**Recovery after repeated failure.** After 3 failures, offer adaptive help, a hint or a skip. Failure should **teach** (show why it happened) and can **pay out** a little (consolation currency), so it is never zero value.

**BlackBook's hint ladder**, adapted:

1. **L1, environmental.** Light the key switch. Add floor scratches pointing at the secret door. Nudge the camera.
2. **L2, direct.** After about 5 minutes stuck, an NPC companion talks to themselves: "That switch looks shootable."
3. **L3, explicit.** After about 15 minutes or 5 consecutive failures, highlight the target or offer a skip. This gives the player a face-saving way out: "I just don't want to waste time."

**The difficulty heatmap.** Log every death or failure with its position. Then read the clusters:

- **Clusters at intended tests** (boss rooms) are fine.
- **Clusters on ordinary paths** mean a tuning error or a trap the player couldn't see.
- **No deaths anywhere** means the boredom zone. Add elites, patrols or hazards.

### 1.3.3 Dynamic difficulty adjustment (DDA)

| Technique | Example | Visibility | Risk |
|---|---|---|---|
| Rubber-banding | Kart racers boost players at the back | Often hidden | Experts feel cheated if it is obvious |
| Hidden difficulty rank | The game quietly adjusts enemy aggression based on performance | Hidden | Players may feel manipulated if they find out |
| Mercy assist after deaths | Offer a shield or a checkpoint after N deaths | Visible, opt-in | Low. This is the recommended default |
| AI director | Spawns paced by player stress | Hidden | Complex to tune |
| Matchmaking by skill | Rated queues | Visible | Needs a large population |

Rules:

- Prefer **visible, opt-in assists** over hidden manipulation.
- **Never make the game harder for experts as a punishment** (2DGD).
- **Never let DDA change monetisation exposure.** The game must not get harder so that a boost looks more attractive.

### 1.3.4 Skill floor, skill ceiling, and perceived fairness

- **Skill floor**: how hard it is to do anything meaningful. **Skill ceiling**: how much mastery can still improve results. Roblox's broad audience needs a **low floor** (one verb, instantly understood) and a **high ceiling** (optimal angles, combos, routes).
- **Make it feel fair** (2DGD):
  - Use generous hitboxes for the player and tight ones for hazards.
  - Make a near-miss *feel* like a near-miss.
  - Telegraph danger. Bioshock's first enemy shots deliberately miss.
  - No off-screen instant deaths, no invisible time limits, no taking away control without warning.
  - Outline hazards, or make foreground objects semi-transparent when they block the view.
- **Make the last hit point count.** Many games quietly give the last sliver of health extra value: a hidden buffer or 1–2 seconds of invulnerability. "Barely survived" moments are memorable.
- **"Favour the player 99% of the time."** Tie-breaks, rounding and crit edge cases should go the player's way.

**Feel thresholds** (gstack feel vocabulary):

| Response time | Feel |
|---|---|
| Under 50 ms | Snappy |
| 50–80 ms | Responsive |
| 80–150 ms | Sluggish |
| Over 150 ms | Disconnected |

Hit feedback (flash, shake, sound) should scale with how effective the hit was.

**On Roblox:**

- **Network latency is part of difficulty.**
  - Show the player's own actions locally, straight away (client-side prediction). Let the server check the result afterwards.
  - Keep input-to-feedback under 80 ms locally, whatever the ping.
  - Precision platforming in obbies needs especially forgiving collision.
  - Every Blender model needs proper collision under house rule 2. That also prevents "I fell through that ledge" deaths, which read as unfair.
- **Obbies and tower climbs live or die on the sawtooth.** Put checkpoints every 30–90 seconds of play. Add a new obstacle type every stage group. Follow each new obstacle with an easy "repetition" section, as 2DGD's *repetita juvant* says (re-use a mechanic soon after teaching it).
- **Add an opt-in "skip stage" convenience product only on stages with a high fail rate after the skip has been offered for free.** The free route might be a hint, a skip after N failures, or a skip token from play. Never put a skip offer on a stage you made harder to sell skips.
- **Track a heatmap of where players die or fail.** Send custom analytics events with the position, aggregate them, and review weekly. Check the current `AnalyticsService` event names `[VS]`.

Sources: 2DGD-F0TH/2DGD_F0TH:chapters/007_Refining/001_Balancing/001_Introduction.md, 2DGD-F0TH/2DGD_F0TH:chapters/007_Refining/001_Balancing/002_Difficulty_Curves.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/008_Tips.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/009_Perceived_Fairness.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/003_Consolidating_Mechanics.md, fagemx/gstack-game:skills/balance-review/references/difficulty-curve.md, fagemx/gstack-game:skills/feel-pass/references/feel-vocabulary.md, fagemx/gstack-game:skills/playtest/references/metrics-and-benchmarks.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch6 Difficulty Heatmap, Hint Grading System), (general knowledge: Csikszentmihalyi flow; DDA examples such as rubber-banding and AI directors)

---

## 1.4 Onboarding and the first-time user experience (FTUE)

### 1.4.1 The four time horizons

| Phase | Window | Must happen | Red flags |
|---|---|---|---|
| Identity | 0–5 s | Player knows what the game is (the fantasy) | Login wall, loading over 5 s on a fast connection, text wall |
| Call to action | 5–15 s | One obvious thing to do | Menus before play, more than 3 buttons pulsing |
| First input | 15–30 s | Player performs the core verb | Cutscene, unskippable dialogue |
| Learning | 30 s–5 min | Aha by about 2 min. First failure (cheap). First choice by 3–5 min | More than 3 new concepts in 2 min; tutorial longer than 3 min |
| Commitment | 5–15 min | First meso goal done. Natural stopping point and return hook shown | Dead time over 5 s; no visible next goal |
| Session 2+ | Return | Welcome back, progress kept, something new | "You were away" punishment; monetisation before the aha moment |

Playtest benchmarks (gstack): first meaningful action in under 15 s is healthy; aha in under 90 s; more than 60% of players have found the key features by minute 10; 0–1 help requests per 10 minutes; tutorial completion above 80%. BlackBook adds: no more than 3 tutorial pop-ups in the first 5 minutes, at least one strong positive event in the first 10 minutes, and core fun within 3 clicks or taps.

### 1.4.2 Principles of good onboarding

1. **Teach by doing, in a safe space.** Give a safe area to try the controls, then a real but forgiving challenge (2DGD).
2. **Progressive disclosure.** Introduce one system at a time, only when it is needed. A shop appears when the player first has enough cash to buy something, not before.
3. **Skip genre basics.** Don't explain WASD to a Roblox player. Do explain your twist (2DGD: don't pad the tutorial).
4. **Put the tutorial in the fiction.** The tutorial is a level or a character, not a manual.
5. **Re-use what you just taught.** Use the new mechanic again within a minute, then combine it with an old one (*repetita juvant*).
6. **Endowed progress.** The first goal bar starts partly filled with the progress the tutorial just earned.
7. **Simplify goals and feedback before adding a tutorial.** GameDesignOS's failure table says: if players don't know what to do, first make the goal and the feedback clearer. Adding tutorial text is the last resort.

**Tutorial anti-patterns:**

- A text wall, or unskippable dialogue.
- Teaching every system up front.
- Taking control away mid-action.
- Tutorials that can't be replayed or skipped by returning players.
- Forced purchases or pass offers inside the tutorial.
- Gating play behind a name or customisation screen. Make customisation optional and later, or one tap.
- Hard failure states during the tutorial.

### 1.4.3 Worked FTUE script (ragdoll launch incremental)

| Time | Beat | Design detail |
|---|---|---|
| 0 s | Spawn already on the launch pad, facing a landmark ramp | No menu. Camera framed on the ramp and the distance markers. Blender-modelled pad and ramp with proper collision |
| 3 s | Pulsing **LAUNCH** button (touch) or key prompt (keyboard/gamepad) | Prompt matches the detected input device |
| 6 s | First launch, ragdoll flight, landing | Big readable distance number and coin burst. Satisfying sound |
| 15 s | Cash counter fills a goal bar that starts 30% full ("Next launcher: 70% there") | Endowed progress |
| 40 s | Second and third launches. Bar fills | Repetition. The player learns that aim angle matters |
| 60 s | Shop button appears with a glow. Buy the first upgrade | Progressive disclosure. First choice: power or aim |
| 90 s | Launch goes visibly further | Aha: "upgrades = distance" |
| 2–3 min | First zone boundary crossed. New terrain revealed | Discovery beat. First "number go up" milestone before 180 s |
| 5 min | First pet or companion from a free egg (odds shown) | Collection hook. Index opens with silhouettes |
| 8–12 min | First meso goal: reach zone 2 | Natural stopping point. Tease the rebirth ("Rebirth at 10K: ×1.5 forever") |
| 15–25 min | First rebirth | Macro loop closes inside session 1. Starter-pack offer may appear **after** this win: small, dismissible, once |

**On Roblox:**

- **Bounces are a top negative discovery signal.** Recommended For You counts sessions under 60 s and 61–180 s against a game `[VS]`. So:
  - put the core fun inside 60 s;
  - put the first reward or "number go up" moment before 180 s.
- **Short-session games retain worse.** Games with average sessions under 3 minutes show a median D1 of only 4.3%. Games with 19–24 minute sessions show a median D1 of 11.5% (GameAnalytics 2025 `[VS]`).
- **Make the thumbnail promise the first minute.** A thumbnail that doesn't match the first minute causes bounces. Since June 2026, Roblox explicitly penalises click-winning thumbnails that don't retain players `[VS]`. "Show the first minute of gameplay" is a practical rule.
- **Mobile-first and text-light.** Most Roblox sessions are on phones and tablets `[VS]`. BlackBook's "Alpha generation" test asks: can the core loop be completed using only icons, without reading?
  - Use large touch targets.
  - Show prompts that match the detected input type.
  - Show numbers rather than sentences.
- **Load fast.** Spawn players into a playable area while the rest of the world streams in (`StreamingEnabled`). Keep Blender meshes efficient:
  - LOD-friendly topology;
  - shared texture atlases;
  - simple collision hulls instead of `PreciseConsistentDecomposition` on every prop.

  House rule 1 raises the visual bar, but it must not cost load time.
- **No offers in the first minutes (house rule 3).** A good default is no purchase prompt before the first meso goal or 10 minutes, whichever comes later. Offers are allowed only right after a win.
- **Instrument the FTUE as a funnel.** Use Roblox's onboarding funnel events, one step per beat in the table above. Review where the drop-off is steepest every week `[VS]`.

Sources: fagemx/gstack-game:skills/player-experience/references/walkthrough-phases.md, fagemx/gstack-game:skills/playtest/references/metrics-and-benchmarks.md, fagemx/gstack-game:skills/balance-review/references/progression.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/002_Tutorials.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/003_Consolidating_Mechanics.md, DY-2026/GameDesignOS:game-concept-architect/references/prototype-validation-gate.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/lever-playbook.zh-CN.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch1 Generational UI Audit, Ch2 FTUE Friction Test), (general knowledge: progressive disclosure; Nunes and Drèze endowed progress), (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/First-Play Bounce Rate.md, Retention Benchmarks.md, June 2026 Discovery Overhaul.md; Patterns/Playable Within a Minute.md; Thumbnails/Rule 01 - Show the First Minute of Gameplay.md)

---

## Further reading (Part A: fun, psychology, flow, onboarding)

- Hunicke, LeBlanc and Zubek, *MDA: A Formal Approach to Game Design and Game Research*. The original MDA paper.
- Raph Koster, *A Theory of Fun for Game Design*. Fun as learning.
- Jesse Schell, *The Art of Game Design: A Book of Lenses*. The lenses toolkit.
- Celia Hodent, *The Gamer's Brain*. Cognitive science and game UX.
- Quantic Foundry, *Gamer Motivation Model* reference. The 12 motivations.
- Steve Swink, *Game Feel*. The vocabulary of responsiveness and juice.
- Greg Costikyan, *I Have No Words & I Must Design*. Classic essay on the nature of games.
- Alex Jaffe, *Cursed Problems in Game Design* (GDC talk). Design goals that conflict with each other.

Sources: Roobyx/awesome-game-design:README.md, kkga/gamedesign-playlist:README.md



This file continues Section 1. It covers progression, economy and balance math, social design, retention, and light narrative. The conventions are the same as in Part 1:

- `[VS]` marks claims that depend on the Roblox version, the market or a policy, checked on 2026-11-08.
- Every subsection ends with a `Sources:` line.
- The house rules always apply: Blender-only visible assets, every visible object solid, and heavy but never invasive monetisation.

## 1.5 Progression systems

### 1.5.1 XP curve formulas

Let `req(L)` be the XP needed to go from level L to L+1. Let `cum(L)` be the total XP needed to reach level L, that is, `req(1) + … + req(L−1)`.

| Curve | Formula | Character |
|---|---|---|
| Linear | `req(L) = a·L` | Gentle. Late levels feel the same as early ones |
| Polynomial | `req(L) = a·L^p`, with p usually 1.5–2.5 | The standard RPG feel. Steady slowdown |
| Exponential | `req(L) = a·r^(L−1)`, with r usually 1.05–1.2 | Fast early, then a wall. Needs income that grows exponentially too |
| Doubling (2DGD example) | 5,000, 10,000, 20,000, 40,000 … | Very steep. Only works with matching XP inflation |

Computed values, with a = 100 unless noted:

| Level | Linear: req / cum | Poly p=1.5: req / cum | Poly p=2 (a=50): req / cum | Exp r=1.15: req / cum |
|---|---|---|---|---|
| 1 | 100 / 0 | 100 / 0 | 50 / 0 | 100 / 0 |
| 5 | 500 / 1,000 | 1,118 / 1,702 | 1,250 / 1,500 | 175 / 499 |
| 10 | 1,000 / 4,500 | 3,162 / 11,105 | 5,000 / 14,250 | 352 / 1,679 |
| 20 | 2,000 / 19,000 | 8,944 / 67,135 | 20,000 / 123,500 | 1,423 / 8,821 |
| 30 | 3,000 / 43,500 | 16,432 / 189,030 | 45,000 / 427,750 | 5,758 / 37,717 |
| 50 | 5,000 / 122,500 | 35,355 / 689,515 | 125,000 / 2,021,250 | 94,231 / 627,541 |

**What the curves feel like.** XP income usually grows as players level. Suppose XP per minute is `20·L`. Then minutes per level come out as:

- **Linear**: a flat 5 minutes at every level.
- **Polynomial p=1.5**: 5 minutes at L1, 15.8 at L10, 35 at L50.
- **Polynomial p=2**: 2.5 minutes at L1, 25 at L10, 125 at L50.
- **Exponential**: under 2 minutes in the mid-levels, then 94 minutes at L50. That is a wall.

The exponential curve's late wall is why it is dangerous. A well-known example of the shape: in RuneScape's skill curve, level 92 needs about half the total XP of level 99 (6,517,253 vs 13,034,431).

**Design rule: design the curve from time, not from XP.** Decide how many minutes each level should take, decide the XP income at that level, and multiply:

> `req(L) = t(L) × xpPerMin(L)`

Worked example: `t(L) = 1 + 0.4·L` minutes and `xpPerMin(L) = 50·1.05^L`.

| Level | Minutes for this level | XP/min | req | Cumulative playtime to reach it |
|---|---|---|---|---|
| 1 | 1.4 | 52 | 74 | 0 |
| 5 | 3.0 | 64 | 191 | 8 min |
| 10 | 5.0 | 81 | 407 | 27 min |
| 20 | 9.0 | 133 | 1,194 | 1.6 h |
| 30 | 13.0 | 216 | 2,809 | 3.4 h |
| 50 | 21.0 | 573 | 12,041 | 9.0 h |

Players get 8 level-ups in the first 27 minutes and still have about 9 hours of runway to L50, before rebirth multiplies everything again.

### 1.5.2 Pacing milestones

gstack's PC/console milestones are below. Mobile and Roblox compress them **5–10×**. Flag anything that comes out more than 2× or less than 0.5× the target.

| Milestone | PC/console target | Roblox-compressed target (heuristic) |
|---|---|---|
| First action | < 30 s | < 15 s |
| "I understand" | 2–5 min | 60–90 s |
| First real choice | 5–15 min | 1–3 min |
| Wow moment | 30–60 min | 5–10 min |
| Build identity | 1–3 h | 15–30 min |
| Major unlock | 3–8 h | 30–90 min (often the first rebirth) |
| Mid-game | 10–20 h | 2–4 h |
| Endgame | 20–50 h | 6–15 h |
| Mastery | 50–200 h | 20+ h, plus weekly content |

Other pacing measures:

- **Content runway.** Under 2 hours of meaningful content is a red flag for free-to-play, and under 5 hours for a premium game.
- **Grind ratio**, defined as meaningful actions divided by total actions:

| Grind ratio | Verdict |
|---|---|
| Above 0.5 | Engaging |
| 0.3–0.5 | Acceptable |
| 0.2–0.3 | Grindy |
| Below 0.2 | Treadmill |

Flag any stretch longer than 2 hours with a ratio under 0.3.

**Level-gap XP scaling** (2DGD). To stop players farming weak enemies and to reward taking on strong ones, scale XP by the level gap. The table uses 5,000 XP at an equal level:

| Player level minus enemy level | XP change | Reward |
|---|---|---|
| ≤ −3 | +600% | 35,000 |
| −2 | +300% | 20,000 |
| −1 | +100% | 10,000 |
| 0 | 0% | 5,000 |
| +1 | −50% | 2,500 |
| +2 | −84% | 800 |
| ≥ +3 | Fixed | 1 |

Grind is self-levelling only up to a point. 2DGD's warning example is Super Hydlide's US release, which had to halve XP requirements and double XP gains because the original grind was too heavy. Farming must still pay off, though. If a farmable exploit pays far more than intended play, players will farm and nothing else.

### 1.5.3 Prestige and rebirth

**Rebirth** is a soft reset. The player gives up their current progress for a permanent bonus and replays faster. 2DGD describes tiered resets: lose weapons and levels for +2% attack, or take a deeper reset for +10% XP. Each tier has its own reward and its own harshness.

The usual parameters:

- **Rebirth cost:** `R_k = R_0 · g^k`, with g usually 2–4.
- **Rebirth multiplier, additive:** `M_k = 1 + b·k`, with b usually 0.25–1. This is the safe choice.
- **Rebirth multiplier, compounding:** `(1 + b)^k`. It explodes. Use it only with matching cost growth.
- **Prestige currency from lifetime earnings:** scale it by a square or cube root, for example `P = floor(c · (lifetimeEarnings)^(1/3))`. Roots keep each extra prestige point worth chasing without letting the numbers run away. Cookie Clicker uses a cube root.

Worked example with R_0 = 10,000, g = 3 and b = 0.5:

| Rebirth k | Cost | Multiplier | Cost ÷ multiplier (relative time to next rebirth) |
|---|---|---|---|
| 0 | 10,000 | 1.0× | 10,000 |
| 1 | 30,000 | 1.5× | 20,000 |
| 2 | 90,000 | 2.0× | 45,000 |
| 3 | 270,000 | 2.5× | 108,000 |
| 5 | 2,430,000 | 3.5× | 694,286 |

The time per rebirth roughly doubles to 2.5× with each tier. Rules:

- **Target 1.3–2× growth in time per rebirth.** When one rebirth takes longer than about 2 sessions, add the next layer: super-rebirth, a new world, or a new prestige currency.
- **The first rebirth should land inside session 1**, at about 15–25 minutes, so the macro loop closes before the player first leaves.
- **Every rebirth must show immediately what the player gained.** For example: "Your first launch is now 1.5× further".

### 1.5.4 Horizontal and vertical progression, collection and mastery

- **Vertical progression** means bigger numbers: stats, multipliers, levels. It is easy to build, and it inflates.
- **Horizontal progression** means new options: sidegrades, tools, cosmetics, new verbs. It lasts longer and keeps PvP fair.
  - BlackBook contrasts the "Western" style, where a max-level player can still die to basic enemies if they play badly, with efficiency-first mobile markets.
- **Collection.** Indexes, sets and set bonuses.
  - "Mutations" (Silver, Gold, Rainbow, weather traits) multiply rarity tiers from the same base asset.
  - Under house rule 1 this suits a Blender workflow: one well-made base mesh, plus material and shader variants and Blender-made VFX attachments.
  - Mutation visuals still need cohesion. A palette for each tier, not random hue shifts.
- **Mastery.** Track use of each tool. 2DGD's example: 1,000 spear kills gives +20% spear attack. Tales of Berseria keeps mastered bonuses, or doubles them if you keep the item.
  - Mastery rewards depth: doing it better, not just doing more.
  - It also gives a reason to keep using tools that are no longer the strongest.
- **Unlockable design** (2DGD). An unlock should be one of four kinds:
  - simply good;
  - neutral but with synergy;
  - good with a drawback;
  - bad until combined with something.

  Assume a wiki will document every secret within days.

**On Roblox:**

- Use the **income/s → multiplier → rebirth** spine where it fits (simulators, incrementals, tycoons) `[VS]`. Use the time-first table above to tune it.
- **Make paid progression horizontal in PvP and allowed to be vertical in PvE.** Hit games that sell power keep it to "speed, 2×, skips, revives, VIP", stating that purchases are "not required to progress". PvP games sell cosmetics and characters `[VS]`.
- **Design for return days, not marathon sessions.** Roblox discovery counts playtime only up to **60 minutes a day per user** `[VS]`. A progression that needs 3-hour sessions earns no extra credit. Spread milestones so a 20–40 minute daily session always closes at least one goal.

Sources: 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/008_Tips.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/006_Gameplay_Flow.md, fagemx/gstack-game:skills/balance-review/references/progression.md, fagemx/gstack-game:skills/game-review/references/progression.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch7 Efficiency-Immersion Slider), (general knowledge: XP curve forms; RuneScape XP table; Cookie Clicker cube-root prestige; the time-first pacing method), (Delta Vault: Roblox Research/2026-11 Market Scan/Patterns/Income Per Second to Multiplier to Rebirth.md, Stacked Mutations and Multipliers.md, Money From Speed Multipliers and Convenience.md; Algorithm/New Game Launch Checklist.md)

---

## 1.6 Balance and economy math

### 1.6.1 Sources and sinks

Map every **faucet** (a way currency enters the game) and every **sink** (a way it leaves). gstack deducts 3 points from any economy review that has no faucet/sink map.

```
FAUCETS                              SINKS
launch payouts ──┐               ┌── launcher upgrades (scaling cost)
daily reward ────┤               ├── egg/pet hatching (consumable)
quests/events ───┼──► WALLET ────┼── rebirth (resets wallet, the main sink)
offline income ──┤               ├── cosmetics (permanent, non-power)
trade-in/sell ───┘               └── repairs/fees/crafting (soft sinks)
```

**Faucet/sink ratio**, measured over a day of typical play (gstack):

| Ratio | State |
|---|---|
| Above 1.2 | Inflationary. Prices become trivial, and player markets explode |
| 0.9–1.1 | Healthy |
| Below 0.8 | Deflationary. Players hoard, and nothing feels affordable |

**What inflation does** (2DGD):

- Fixed shop prices become meaningless.
- Player-market prices skyrocket.
- Bartering in items replaces the currency.

Deflation causes hoarding. Minigames and fees work as material sinks.

**Number of currencies:**

| Currencies | Verdict |
|---|---|
| 1 | Clear |
| 2 | Standard (soft + premium) |
| 3 | Manageable |
| 4 or more | Red flag |

Every extra currency needs its own faucet/sink map.

**Wealth inequality.** Gini coefficient targets for player wealth:

| Game type | Gini target |
|---|---|
| PvE | Below 0.3 |
| PvP | 0.3–0.5 |
| Sandbox or trading | 0.4–0.6 |
| Any | Above 0.6 is a flag |

**Day projection.** Simulate a typical non-spending player's stockpile over 90 days. Flag the day it first exceeds **2× the most expensive item**. gstack's broken example:

| Day | Stockpile |
|---|---|
| 1 | 200 |
| 7 | 1,200 |
| 14 | 3,500 |
| 30 | 11,000 |
| 90 | 45,000 |

If nothing costs more than 5,000, this economy is dead by day 14.

**Questions to answer before launch:**

- "What breaks first at 2× earn rate?"
- "Describe a Day-30 non-spender's resource state."
- "Describe a $100 week-1 spender against a Day-30 free player."

### 1.6.2 Cost curves and time-to-reward

The standard incremental cost curve is geometric:

> `cost_n = base · r^n`, with r usually 1.07–1.15 (Cookie Clicker uses 1.15)

If each unit adds a fixed income, the **payback time** (cost divided by added income per second) grows by the same factor r with each purchase. With base 10, r = 1.15 and +1/s per unit:

| Unit n | Cost | Payback |
|---|---|---|
| 0 | 10 | 10 s |
| 10 | 40 | 40 s |
| 25 | 329 | 5.5 min |
| 50 | 10,837 | 3 h |

That 3-hour wall at unit 50 is where a new tier, a multiplier upgrade or a rebirth must take over.

**Time-to-reward rules** (heuristics):

- **Price items in minutes of play, then convert to currency:** `price = targetMinutes × incomePerMin(stage)`.
- **Early game:** something affordable every 30–90 seconds.
- **Mid game:** every 3–5 minutes.
- **Late game:** one major purchase per session, plus small purchases between.
- **Always show a "next affordable" target** with an estimate in minutes. It is a goal-gradient tool.

### 1.6.3 Idle and offline math

- **Offline income** = `incomePerSec × min(timeAway, cap) × offlineRate`.
  - Common heuristics: a cap of 8–12 hours and an offline rate of 25–50%.
  - Example: 100/s × 8 h × 50% = **1.44M**.
- **Rule:** offline earnings should equal roughly one active session's earnings. Then returning feels good, but active play stays better.
- **Never** let offline gains decay or be lost (see 1.8). Add a cap, and show it honestly: "Storage full. Come back to collect."

### 1.6.4 Balance spreadsheet and simulation

**A minimal balance sheet** has one row per level or stage, with these columns:

- stage;
- target minutes;
- income per minute;
- cost of the next upgrade;
- minutes to afford it;
- cumulative minutes;
- multiplier sources (free and paid, shown separately);
- stockpile for a non-spender;
- stockpile for a spender;
- days to reach the stage;
- notes.

**Simulation, from cheapest to most expensive:**

1. **Deterministic day projection.** Spreadsheet rows per day.
2. **Monte Carlo for random drops.** Simulate 10,000 players opening N eggs. Report the 50th, 90th and 99th percentiles of attempts needed.
3. **Agent simulation.** Scripted bots playing a policy. Machinations or Loopy work for visual flow models.

**Pity math.** The chance of at least one success in n attempts is `1 − (1 − p)^n`:

| Drop rate p | Expected attempts | Chance by 1× expected | By 2× | By 3× | Attempts for 99% |
|---|---|---|---|---|---|
| 10% | 10 | 65.1% | 87.8% | 95.8% | 44 |
| 1% | 100 | 63.4% | 86.6% | 95.1% | 459 |
| 0.5% | 200 | 63.3% | 86.5% | 95.1% | 919 |
| 0.1% | 1,000 | 63.2% | 86.5% | 95.0% | 4,603 |

About 37% of players will *not* get the item after the expected number of attempts. Set pity at 1.5–3× the expected attempts, and show the counter.

gstack's gacha warning: an SSR at 0.6% means about 167 expected pulls, and a pity at 300 pulls at $3 each means a worst case of about $500. That is unacceptable for a young audience. On Roblox, paid random items must show their odds `[VS]`.

### 1.6.5 Monetisation math within the house rules

gstack's measures:

| Measure | Fair | Aggressive | Hostile |
|---|---|---|---|
| Progression speed, paying vs free | ≤ 2× | 3–5× | > 5× |
| Share of content behind a paywall | < 10% | 10–30% (standard) | > 30% |
| P2W score (1–10) | 4–5 means convenience | — | Flag above 5 in any PvP context |

Spending tiers: minnows ($0), dolphins ($5–20), whales ($50–200+), and mega-whales, whose extra spending must hit diminishing returns.

**Stacking.** Three +10% boosts multiply to +33.1%, not +30%. Two 2× boosts multiply to 4×.

**Resolving the conflict between the sources and house rule 3.** 2DGD argues for cosmetic-only microtransactions. House rule 3 requires timed boosts (2× EXP, speed, cash) and convenience passes. The resolution:

1. Boosts may only **speed up a loop that is already fun**. They must never remove pain you designed in order to sell the cure.
2. **No paid power in PvP.** Boosts affect PvE progress only.
3. **Keep permanent paid multipliers at ≤ 2× the free rate when combined.**
4. **Timed boosts.** Two options:
   - **Lower-risk (recommended):** paid multipliers stack **additively** within their category. A 2× cash pass plus a 2× timed boost gives 3×, not 4×. Show the total on the HUD.
   - **Bold:** multiplicative stacking for PvE only, capped at a visible total (for example 4×). This earns more per boost but pushes the paid speed into gstack's "aggressive" band. Accept that only with clear in-game messaging and strong free routes.
5. **Luck and Server Luck only where luck mechanics already exist.** Show the luck effect as an exact odds change: "Rare 1% → 2%".
6. **Gift versions of passes.** They create a generosity loop and repeat spend days. On Roblox, game passes cannot be gifted natively. Build gifts as a developer product that grants the pass entitlement to a chosen friend's UserId, saved in a DataStore `[VS]`.

**On Roblox:**

- **Repeat spending over several days is a discovery signal.** "Spend days per user" and Robux per user are discovery signals `[VS]`. Cheap, repeatable developer products (timed boosts) alongside one-off passes beat one big purchase.
- **Log every currency faucet and sink with economy analytics events** (source and sink, with an item category), so the faucet/sink ratio can be read from live data `[VS]`.
- **An illustrative price ladder**, to calibrate with real data `[VS]`:
  - timed boosts as the cheapest tier;
  - the starter pack at a low, one-time "first purchase" price;
  - convenience passes in the middle;
  - the VIP or "everything" pass at the top.

  The starter pack is offered once, after the first rebirth or a similar win. It is never re-offered on a fake timer.
- **Sell "limited" items only if they really are limited, and say exactly how.** "Available until Dec 31" is honest. "Only 3 left!" when that isn't true is false scarcity and is banned. 2DGD's point that "artificially low supply makes it valuable" applies only to genuine, disclosed limits.

Sources: fagemx/gstack-game:skills/game-review/references/economy.md, fagemx/gstack-game:skills/balance-review/references/economy-model.md, fagemx/gstack-game:skills/balance-review/references/monetization.md, fagemx/gstack-game:skills/balance-review/references/gotchas.md, fagemx/gstack-game:skills/balance-review/references/progression.md, fagemx/gstack-game:skills/game-direction/SKILL.md, 2DGD-F0TH/2DGD_F0TH:chapters/007_Refining/001_Balancing/003_Economy.md, 2DGD-F0TH/2DGD_F0TH:chapters/008_Marketing_Community/001_Marketing/006_F2P.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/005_Game_Design_Tips/008_Tips.md, Roobyx/awesome-game-design:README.md (Machinations, Loopy), (general knowledge: geometric cost curves; Cookie Clicker 1.15 cost factor; offline income heuristics; binomial pity math), (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/Spend Days Per User.md, Robux Spent Per User.md; Patterns/Money From Speed Multipliers and Convenience.md)

---

## 1.7 Social and multiplayer design

### 1.7.1 Interaction structures

| Structure | What it produces | Design levers | Pitfalls |
|---|---|---|---|
| Co-op (positive-sum) | Fellowship, relatedness | Shared goals; combo bonuses; complementary roles | Free-riders. Reward contribution, with a floor for everyone present |
| Competition (zero-sum) | Challenge, status | Ranked queues; leaderboards; duels | Stomping new players. Toxic losers |
| Asymmetric roles | Tension, drama, replay variety | One-vs-many ratios (1 murderer : 1 sheriff : N innocents); role rotation | Role balance. Waiting for a preferred role |
| Parallel play | Presence without pressure | Shared space, visible progress, emotes | No real interaction |
| Async social | Low-pressure relatedness | Gifts, visits, likes on builds, notes | Spam and griefing via gifts |

**Asymmetric balance** (Sirlin-style, from gstack):

- **Win rates.** Keep the spread under 10%, with each role between 45% and 55%.
- **Counters.** Every option has at least 2 counters.
- **Strategies.** At least 3 viable strategies.
- **The four structures.** Know whether your system is transitive (better is better), intransitive (rock-paper-scissors), frustra (a counter that shuts you down) or asymmetric.

### 1.7.2 Presence, spectating and events

- **Presence.** Make other players' moments visible: launches flying overhead, rare-find toasts, build showcases. Social proof (1.2.5) turns into *aspiration*: "I want a Rainbow Shark too."
- **Spectating.** In round-based games, dead or waiting time must stay under about 30 seconds, or give players something to do: spectate with predictions, bet free points on the outcome, or play a minigame in the lobby. 2DGD notes that spectating and speedrun tools (timers, splits, personal bests) build community.
- **Small-group and server-wide events.**
  - **Small-group** (2–6 players): raids, co-op puzzles. They create fellowship and need balance for group size.
  - **Server-wide**: boss spawns, meteor showers, "admin abuse" live events, Server Luck. They create shared moments, chat spikes and clips.

  Use both. Server-wide events are the cheapest relatedness generator on Roblox.

### 1.7.3 Trading and griefing

**Trading** can extend a game's life by years. Adopt Me and MM2 are examples `[VS]`. It also brings scams. A minimum trade design:

- two-sided confirmation screens;
- no changes to items after "accept";
- a confirm delay of 3–5 seconds;
- a value or rarity display;
- trade history;
- a cooldown on new accounts.

Respect `PolicyService` rules on paid-item trading per region `[VS]`.

**Griefing controls:**

- PvP is opt-in, by zone or toggle.
- Spawn protection.
- No friendly fire by default.
- Base locks.
- Physics props that can't be used to trap players.
- Rate limits on gifts and emotes.
- Easy block and report.
- Collision that can't be exploited to push players off the map. Proper collision (house rule 2) also prevents clipping exploits.

**BlackBook's social-friction audit:**

- No tasks like "add 3 friends". Ask for one-way gestures instead, such as "wave at 3 players".
- Add async options so players don't have to be online together.
- Make declining free of awkwardness: a busy mode, and silent declines.

**On Roblox:**

- **Intentional co-play counts; matchmaking doesn't.** Joining a friend, invites, and private or reserved servers count towards discovery. Random matchmaking does not `[VS]`. So build:
  - friend-join bonuses that are positive and modest, for example +10% income while playing with a friend;
  - one-tap invites;
  - free private servers where possible;
  - co-op mechanics that work best with friends.

  Never require invites to progress. Check current Roblox policy before rewarding social actions such as invites, likes or favourites. Many 2026 hits reward likes, favourites and group joins, but policy can change `[VS]`.
- **Set server size to the game type.** Smaller servers (6–12) feel full sooner at launch and suit co-op. Hubs and simulators commonly use 20–30. An empty large server kills a social game. Start small and raise it when the CCU supports it.
- **Filter all user text.** Any player-written text (pet names, signs, trade notes) must go through Roblox text filtering before other players see it `[VS]`.
- **Server Luck** is a positive-sum social purchase. One player pays and the whole server benefits. Show a short, dismissible thank-you banner, not a sales pitch.

Sources: fagemx/gstack-game:skills/balance-review/references/character-balance.md, 2DGD-F0TH/2DGD_F0TH:chapters/008_Marketing_Community/002_Keep_Players_Engaged.md, 2DGD-F0TH/2DGD_F0TH:chapters/003_Project_Management/001_Basics/004_Common_Errors.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch12 Social Friction Audit, Ch7 Social Pressure Audit), (general knowledge: Sirlin balance framing; co-op and competition structures; Roblox text-filtering requirement), (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/Intentional Co-Play Days.md; Patterns/Collection Index and Trading.md, Engagement Prompts in the Loop.md, Live Admin Abuse Events.md)

---

## 1.8 Retention systems, with ethics

### 1.8.1 The toolkit

| Mechanic | How it works | Ethical version | Banned version |
|---|---|---|---|
| Daily reward | Reward for logging in each day | **Cumulative calendar** (counts days played, not consecutive days), or a streak with 1–2 free "streak freezes" | Streak resets to zero and wipes accumulated rewards |
| Streaks | Escalating rewards for consecutive days | Soft reset: drop back a few tiers, not to zero | Guilt notifications; paid "streak repair" as the only option |
| Appointment mechanics | Timers: crops, restocks, spawns every 5/15/30 min | Timers that reward *showing up* without punishing *not showing up* | Rewards that rot or expire unless you return on time |
| Offline progress | Earnings while away | Capped, honest, never lost | Offline losses; "your base was raided while you slept" without protection |
| Goals ladder | Daily, weekly and season goals | Process goals ("play 3 rounds"); a mix of short and long | Result-only goals that punish weaker players |
| Live events | Limited-time content | Clear dates; event items that may return later, or are clearly stated not to | Fake "last chance" banners; restarting countdowns |
| Weekly updates | New content on a fixed day | A predictable cadence players can plan around | Content dribbled out to extend obligations |
| Notifications | Reminders outside the game | Opt-in, real news ("your crops are ready", "event starts") | Spammy or guilt-based messages |

**gstack's distinction:** skill gates create mastery, and time gates create obligation. Fixed-interval rewards such as a daily reset create FOMO by their nature. Use them lightly and generously.

### 1.8.2 Retention benchmarks: the sources conflict

| Source | D1 | D7 | D30 | Notes |
|---|---|---|---|---|
| gstack "Good" (generic F2P) | 40%+ | 15%+ | 5%+ | Mobile and F2P industry-style targets |
| GameAnalytics 2025, Roblox game-level medians `[VS]` | 4.3% (sessions < 3 min) to 11.5% (19–24 min) | Median 1.6%, P98 8.5% (19–24 min band) | — | All users, 2025 data |
| RoWatcher, Jul 2026, by Roblox genre `[VS]` | Obby 25–35%; tycoon and incremental 20–28%; shooter 22–30%; RP 15–22% | Tycoon 12–18%; shooter 12–16% | — | No methodology published |

**Resolution:**

- Use **Roblox Creator Analytics' benchmark against similar games** as your primary yardstick. It compares you with 50+ similar games and does not itself affect the algorithm `[VS]`.
- Use GameAnalytics for percentile thinking: a D1 above 11% is above the median, and 20–30% is around the top 2%.
- Treat gstack's figures as general F2P targets, not Roblox norms.

### 1.8.3 Event and cadence design

- **A fixed weekly update day.** All-time CCU records for the 2025–26 hits were set on update days. Brookhaven updates on Fridays. DTI's boutique rotates on Saturdays `[VS]`.
  - Decide the day before launch.
  - Make each update visible in-game with a "What's new" board, Blender-modelled and diegetic rather than a pop-up.
  - Log each update as an Experience Event.
- **Timer cadence.** Rare spawns every 5–15 minutes and events every 30 minutes keep players for "just one more" `[VS]`. Ethically:
  - announce the next spawn time;
  - never punish players who miss it;
  - never make missing it cost progress.
- **Seasonality.** Saturdays and the December holidays have the most Home traffic `[VS]`. Schedule big events and launches to match.

**On Roblox:**

- **Return days count more than marathon sessions.** Recommended For You measures play days at D1, D2–7 (out of 6 possible days) and D8–28, and counts daily playtime only up to 60 minutes `[VS]`. The algorithm itself rewards **several good short sessions over one long one**, which matches healthy design for children. Do not build mechanics that push young players past an hour.
- **Notifications must be opt-in and genuinely useful.** Use Roblox's Experience Notifications. Check the current rate limits and eligibility rules `[VS]`.
- **Never let absence destroy anything.** Use BlackBook's cozy rule: things stop growing, they don't die.

Sources: fagemx/gstack-game:skills/game-review/references/progression.md, fagemx/gstack-game:skills/balance-review/references/progression.md, fagemx/gstack-game:skills/player-experience/references/walkthrough-phases.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/retention-risk-gates.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/flow-sdt-experience-gates.zh-CN.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch11 Stressor Elimination Audit), 2DGD-F0TH/2DGD_F0TH:chapters/008_Marketing_Community/002_Keep_Players_Engaged.md, (general knowledge: streak-freeze and cumulative-calendar patterns), (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/Retention Benchmarks.md, Creator Analytics Benchmarks.md, Play Days Per User.md, 28-Day Retention Window.md, New Game Launch Checklist.md; Patterns/Weekly Updates on a Fixed Day.md, Things Happen on a Timer.md, Offline Progress.md)

---

## 1.9 Light narrative: fantasy, theme and environmental storytelling

### 1.9.1 Fantasy first

The **player fantasy** is who the player gets to *be* or *feel*. gstack's example for Minecraft: "I built this world, it's MINE." GameDesignOS formalises the **player promise** as:

> **promise = fantasy identity + core action + key conflict + perceivable feedback**

That promise has to stay consistent across three layers:

1. the external pitch (title, thumbnail, description);
2. the first 10 minutes;
3. long-term play.

A promise broken between layers 1 and 2 causes bounces. A promise broken between layers 2 and 3 causes churn.

**Hard rules from GameDesignOS:**

- Theme is not differentiation.
- Worldbuilding is not gameplay.
- Never write untestable fantasy documents.

### 1.9.2 Environmental storytelling

**BlackBook's three questions, asked of every room or area:**

1. **What happened here?** Signs of a struggle, a coffee that's still steaming, an open book.
2. **Who lives here?** Posters, books, the rubbish bin. Everything must fit the owner, or the mismatch must be explained.
3. **Where is this?** Architecture, the view, vegetation and notices that place the scene in the world and its current state.

**gstack's four channels.** Tell story through visuals, audio, animation and UI, and keep all four consistent.

**Other techniques:**

- **Item descriptions** carry lore for players who look for it, as in Dark Souls. Characters are more interesting when they are bad at something.
- **Fetch quests need a twist.** The illusion of choice is acceptable if it is used sparingly (2DGD).
- **The world reacts to the player** (BlackBook's reactivity matrix). After a big event:
  - the visuals change: weather, banners, damage;
  - NPC chatter changes;
  - at the highest level, NPC behaviour changes too: prices, new areas open, a celebration.

### 1.9.3 Readable worlds

Kevin Lynch's five elements of a city image, via BlackBook, apply to hubs and maps:

- **Landmarks**: visible from far away.
- **Paths**: where people move.
- **Nodes**: junctions and plazas.
- **Districts**: themed zones.
- **Edges**: boundaries.

Three audits:

- **Skyline audit.** At regular points, can you see 1 global and 2 local landmarks? Are their silhouettes still distinct in black and white? Is the brightest, most saturated, most animated thing in view the place you want the player to go?
- **Squint test.** Blur the screenshot. Are paths and walls still clear? Do interactables stand out?
- **No-UI run.** Turn off the HUD and minimap. Can a new player find "the village at the foot of the hill" from directions alone? When they get lost, do they find something interesting?

A "weenie" is Disney's name for a big, attractive landmark that pulls visitors forward. Put one in view from spawn.

**On Roblox:**

- **Players skip text, so the world tells the story.** Under house rule 1 every prop is Blender-made, so environmental storytelling is part of the art budget, not an afterthought.
  - Build a Blender **"story prop kit"** for each zone: wear and tear, personal items and signage.
  - Give it one palette and one shape language. The art bible prevents generic "AI slop" props.
  - Every story prop is solid (house rule 2). Players will climb on it.
- **Make the title and thumbnail promise the fantasy and the verb**, and make the first minute deliver exactly that. Delivering it consistently is how you avoid the anti-clickbait correction `[VS]`.
- **Meme and real-world IP themes spread fast but age fast** `[VS]`. A coherent original world lasts longer. Pick on purpose: fast wave-riding or a durable world.
- **Use diegetic UI where it is cheap.** A Blender-modelled leaderboard, update board or index pedestal in the hub adds presence and story at once.

Sources: DY-2026/GameDesignOS:game-concept-architect/references/player-promise-framework.zh-CN.md, DY-2026/GameDesignOS:game-concept-architect/SKILL.md, fagemx/gstack-game:skills/game-ideation/SKILL.md, fagemx/gstack-game:skills/game-review/references/design-consistency.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch3 Skyline Audit, Squint Test, No-UI Run; Ch5 Environmental Audit, World Reactivity Matrix), 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/006_Worldbuilding/001_Introduction.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/006_Worldbuilding/004_Quest_Design.md, 2DGD-F0TH/2DGD_F0TH:chapters/004_GameDev_Basics/006_Worldbuilding/005_Story_Design.md, (general knowledge: Lynch *The Image of the City*; the Disney "weenie"), (Delta Vault: Roblox Research/2026-11 Market Scan/Patterns/Real-World and Meme IP.md; Algorithm/Clickbait and Giveaway Penalty.md; _MOC.md executive summary)

---

## Further reading (Part B: progression, economy, social, retention, narrative)

- Ian Schreiber, *Game Balance Concepts* (free course). Cost curves, transitive and intransitive balance.
- Ernest Adams and Joris Dormans, *Game Mechanics: Advanced Game Design*. Internal economies and Machinations diagrams.
- GDKeys and Deconstructor of Fun. Progression and F2P economy teardowns.
- Daniel Cook (Lost Garden), *The Chemistry of Game Design*. Skill atoms and loops.
- Emily Short's blog. Storylets and light narrative structures.
- *The Level Design Book* (free). Readability, landmarks and flow.

Sources: Roobyx/awesome-game-design:README.md, kkga/gamedesign-playlist:README.md



This part covers the design process from first idea to live game, then playtesting, review rubrics, failure modes, postmortems, and a list of points where sources disagree. The conventions match Parts 1 and 2: `[VS]` marks claims that depend on Roblox's version, the market or policy (checked 2026-11-08), and `Sources:` lines close each subsection. The house rules always apply.

## 1.10 Process: from idea to a live game

### 1.10.1 The concept one-pager

Write one page before you build anything. gstack's one-pager has these fields:

| Field | Content | Test |
|---|---|---|
| Fantasy | Who the player *is* or *feels like* | Can you say it in one breath? |
| Core loop | Verb → feedback → reward → repeat | Verb test: is the core a single strong verb? |
| Twist | What is *mechanically* new | Screenshot test: would one frame look different from its competitors? |
| Audience | Primary, secondary, **and who it is NOT for** | Names a Quantic Foundry cluster |
| Platform and session | Devices; target session length | Fits Roblox sessions (see 1.1.4) |
| Comp set | 3 comparable games, with what you take from each and where you differ | Be honest about comps |
| Nested loops | 30 s, 5 min, session, meta | A reason to stop and a reason to return |
| Iceberg | Validation evidence, layered from context to external proof | Intuition counts least for first-timers |
| Next validation step | The smallest probe that could change your decision | — |
| Biggest risk | One sentence | — |
| Scope | Full vision vs the smallest fun version, in person-months | A ratio above 10:1 is fantasy |

Kosinaz's intro formula makes a good first line:

> "(Title) is a (art direction), (niche) (genre) for (platform) about (story), set (setting), featuring (gameplay features)."

Kosinaz also gives title guidance. Titles should be unique, easy to search, around 3–4 words or about 17 characters, and include a non-dictionary word. On Roblox, titles follow the platform's own conventions, such as status tags plus a verb phrase `[VS]`.

gstack's **six forcing questions** for a concept:

1. **Fun reality.** Have you *seen* someone enjoy this, or only imagined it?
2. **Comp honesty.** Are your comparable games really comparable?
3. **The 30-second session test.** Is 30 seconds of play enjoyable on its own?
4. **Repeatability.** How does the 1st play differ from the 100th?
5. **Scope honesty.** What is the ratio of full vision to smallest fun version?
6. **Observation.** What have real players actually done with it?

### 1.10.2 Pillars

Pick **3 design pillars**: short statements the whole game obeys, such as "Every launch is funny", "Progress is never lost" and "Better with friends".

Each pillar must translate into a **measurable rule**. gstack's example is "competitive balance" becoming "win-rate variance under 5%".

For a review, ask: "Name one mechanic that contradicts a pillar." Every review should be able to answer this, and every answer is either a cut or a pillar change.

Use GameDesignOS's ordering for concept work. This order is mandatory:

1. Seed.
2. Verbs.
3. Two to four design-nucleus options.
4. Alignment between actions and goals.
5. **Assumption ledger.**
6. Player promise.
7. Core loop.
8. **Scope gate.**
9. Validation plan.

Never write "tune later" in place of a validation plan. Never add a genre-standard system just because the genre usually has one.

### 1.10.3 A lean GDD

The GDD is a **living body of knowledge**, not a monolith. It can be a wiki, a kanban board or spreadsheets (2DGD). A lean GDD needs these parts:

1. **One-pager and pillars.** The two sections above.
2. **Loops**, each system with these five fields (from GameDesignOS):
   - the loop it serves;
   - the behaviour it changes;
   - its feedback;
   - its validation metric;
   - its **deletion condition**.
3. **Progression and economy sheet.** See 1.5 and 1.6.
4. **FTUE script.** Second-by-second, as in 1.4.3.
5. **Monetisation plan.** Products, placement moments, rate limits and ethics checks, all in line with house rule 3.
6. **Art bible.**
   - Blender kit list, palette, shape language, texel density and polygon budgets (house rule 1).
   - A collision plan for each model class (house rule 2).
7. **Telemetry plan.** Every metric names the decision it informs.
8. **Cut list and idea bin.**
9. **Tools and versions.** For example, the Blender version and the export settings.

**The Gamebook convention** (r-lyeh) is a useful layout. Write the design in the order the player experiences it: *before* the game runs, *during* play, and *after* it ends. Each spread has a player-view "left page" of sketches and screens, and a developer-view "right page" with implementation, tech, art direction, risks and estimates.

On Roblox, the three stages look like this:

- **Before**: thumbnail, title, icon, video, game page.
- **During**: the experience itself.
- **After**: notifications, update day, the return visit.

### 1.10.4 Prototyping

**The prototype brief.** Fill this in before you write any code:

- **QUESTION**: one question, binary if possible.
- **CORE VERB**: the one action being tested.
- **THROWAWAY?**: yes or no.
- **TIMEBOX**: 30–90 minutes for a mechanic, or one sitting.
- **KEEP IF**: the signal that means continue.
- **KILL IF**: the signal that means stop.

**Kill criteria:**

| Decision | Signal |
|---|---|
| Keep | A fresh player uses the verb on purpose within about 30 s, unprompted, and plays "one more time" without being asked |
| Kill | The verb only feels good after you explain it; or making it fun needs systems far beyond scope; or you are adding art or levels to avoid admitting the verb is flat |
| Refactor | One variable is clearly off. Retune and retest |

A "keep" decision authorises a **rewrite** in the real project. It does not mean promoting the spike code.

**Slice types**, with gstack's typical durations:

| Slice | Duration | Question it answers |
|---|---|---|
| Mechanic | 3–7 days | Is the verb fun? |
| Onboarding | 1–2 weeks | Do new players get it within 60 s? |
| Progression | 2–3 weeks | Does the curve pull players forward? |
| Combat | 1–3 weeks | Is the moment-to-moment conflict good? |
| Economy | 1–2 weeks (spreadsheet) | Does the faucet/sink balance hold? |
| Vertical | 4–8 weeks | Is the full experience shippable at quality? |

**Jumping straight to a vertical slice is the most common scope mistake.**

Score slices out of 10, 0–2 on each of five axes: validation value, feasibility, signal clarity, dependency risk and scope discipline. A score of 8–10 is a strong slice. A score of 0–3 is not a prototype. A demo is not a prototype. Define the failure condition, and "build the slice you're afraid of."

**The source repos conflict with house rule 1 here.** gamedev-skills and gstack say "greybox with primitives". House rule 1 says no primitive builds ship. The resolution:

- **Lower-risk (recommended).** Build a tiny **Blender blockout kit** early: low-poly ramps, pads, walls and props in the target proportions, exported as GLB with simple collision. Prototypes then use Blender assets from day one, and the kit becomes the base for final art. This costs about half a day to a day upfront, and it removes all risk of placeholders reaching release.
- **Bold.** Greybox with primitives for 1–3 days in a **separate, private test place** that is never published. Then rebuild in Blender for any test with outside players. This is faster for pure mechanic questions, but there is a real risk of "temporary" Parts surviving. It needs a release gate: zero visible `Part`, `WedgePart` or `CornerWedgePart` outside an `InvisibleHelpers` folder.

### 1.10.5 Scope, cut lists and decisions

- **Lake or Ocean** (gstack). A *Lake* is a scope you can boil, meaning finish completely. An *Ocean* cannot be finished. If your content list contains "etc.", it is an Ocean.
- **The scope gate** (GameDesignOS) has five tiers:
  - MVP;
  - vertical slice;
  - after the demo;
  - pitch concept only;
  - **cut**.

  Score each feature 1–5 on five criteria: how much it delivers the promise, how much it changes behaviour, how much it reduces unknowns, its cost, and its dependencies.
- **Suspect these by default:**
  - open world;
  - real-time multiplayer;
  - branching story;
  - complex economy;
  - UGC;
  - live ops;
  - high-precision physics;
  - expensive 3D.

  On Roblox, multiplayer comes for free, but each feature on this list still needs a reason to exist. Expensive 3D applies to you directly, since every asset is Blender-made.
- **Feature triage under deadline** (gamedev-skills game-jam). Ask three questions in order:
  1. Does the core loop work without it? If yes, it is a stretch goal.
  2. Can a player tell it's missing? If no, cut it.
  3. Is it under 30 minutes of work? If no, defer it.

  When unsure, the default answer is **cut**.
- **Estimates.** Multiply your duration estimates by about 3 (2DGD).
- **Feature creep.** Make it work, then make it work well, then make it elegant. Brainstorm early, not late.
- **One-way and two-way doors** (GameDesignOS decision brief). For each decision, record:
  - the question;
  - the default action;
  - how reversible it is;
  - the options;
  - the uncertainty map;
  - at most 3 information-gathering actions, each with the signal that favours A or B;
  - the chosen probe;
  - a stop rule.

  Spend validation effort on decisions that are hard to reverse, such as the economy's core currency, the server model or the art direction. Move fast on decisions that are easy to undo.
- **Ask:** "Which one feature would you cut to ship 3 months early?"

### 1.10.6 Milestones and solo realities

| Milestone | Exit criteria |
|---|---|
| First playable | Core loop closes: start → play → fail or win → restart. Playability score of 6 or more out of 12 |
| Vertical slice | One zone at final quality: Blender art, collision, sound and FTUE. Feel score of 10 or more out of 14 |
| Alpha | All systems in, content incomplete. Economy simulated |
| Beta | Content complete, tuning, telemetry live, closed test |
| Gold / launch | Release checklist passed (1.12.3) |
| Live | Fixed weekly update day, events calendar, metrics reviewed weekly |

A **worked 4-week solo MVP plan on Roblox** (heuristic; a small incremental game is commonly scoped at 2–4 weeks `[VS]`):

| Week | Work |
|---|---|
| 0 | One-pager, pillars, Blender blockout kit, mechanic slice (2–3 days), kill or keep |
| 1 | Core loop in the real project; Blender hero assets (launcher, pad, first zone); collision pass |
| 2 | Progression and economy sheet in code; rebirth; shop; collection index; monetisation products wired in but rate-limited |
| 3 | FTUE script, funnel telemetry, feel pass, thumbnails and video; closed test with 16+ testers; bug freeze in the last 2 days |
| 4 | Launch to the 16+ audience. Gather 250 engaged plays; under-16 users can't see a new game until it has them `[VS]`. Run the first weekly update on the fixed day |

**Solo pitfalls** (2DGD):

- Losing motivation through over-ambition. Leave out features like complex multiplayer modes.
- Working in isolation.
- Not letting others test. Your own skill is not a universal measure.
- Perfectionism. Order your fixes by effort against improvement.

gstack's ethos gives a priority order: **fun > clarity > performance > polish > sustainability**. "Player time is sacred." Forced waits, unskippable replays, and grind built to sell skip buttons all disrespect the player.

**On Roblox:**

- Treat the **game page as the "before" chapter of the Gamebook**. Prepare 3–5 distinct thumbnails with personalisation on, and leave them for at least 7 days. Upload a real gameplay video (up to +39% Recommended For You playtime has been reported) `[VS]`. Use a unique title and a unique place file with your own twist. Near-duplicate clones are penalised `[VS]`.
- **Respect the 16+ age gate in your plans.** If your audience skews young, you need a way to get 250 engaged, age-checked 16+ players within 60 days. Use older-skewing hooks, Discord or TikTok `[VS]`.

Sources: fagemx/gstack-game:skills/game-ideation/SKILL.md, fagemx/gstack-game:skills/game-review/references/risk.md, fagemx/gstack-game:skills/game-review/references/design-consistency.md, fagemx/gstack-game:skills/prototype-slice-plan/references/slice-types.md, fagemx/gstack-game:skills/prototype-slice-plan/references/scoring.md, fagemx/gstack-game:skills/prototype-slice-plan/references/gotchas.md, fagemx/gstack-game:skills/game-retro/SKILL.md, fagemx/gstack-game:ETHOS.md, DY-2026/GameDesignOS:game-concept-architect/SKILL.md, DY-2026/GameDesignOS:game-concept-architect/references/scope-gate.zh-CN.md, DY-2026/GameDesignOS:game-concept-architect/references/core-loop-expansion.zh-CN.md, DY-2026/GameDesignOS:game-concept-architect/templates/assumption-ledger.md, DY-2026/GameDesignOS:game-concept-architect/templates/feature-priority-matrix.md, DY-2026/GameDesignOS:runtime/workspace-template/06-decisions/decision-brief.template.md, DY-2026/GameDesignOS:docs/workflows/idea-to-validation.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/prototype-fast/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/game-jam/SKILL.md, 2DGD-F0TH/2DGD_F0TH:chapters/003_Project_Management/002_GDD.md, 2DGD-F0TH/2DGD_F0TH:chapters/003_Project_Management/001_Basics/003_General_Tips.md, 2DGD-F0TH/2DGD_F0TH:chapters/003_Project_Management/001_Basics/004_Common_Errors.md, 2DGD-F0TH/2DGD_F0TH:chapters/009_Putting_Yourself_Out_There/003_GameJams.md, r-lyeh/gamebook:README.md, kosinaz/game-design-document-template-for-beginners:docs/Game Design Document.md, (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/New Game Launch Checklist.md, 250-Play 16+ Age Gate.md, Near-Duplicate Clone Penalty.md; Thumbnails/Title Formulas.md; _MOC.md)

---

## 1.11 Playtesting and iteration

### 1.11.1 Methods

| Method | Best for | Sample size (gstack) | Cost |
|---|---|---|---|
| Self-play | Bugs, obvious feel problems | — | Lowest. Never sufficient on its own |
| Uncoached outsider | FTUE confusion | 1–2 | Two minutes reveal more than an hour of self-play |
| Moderated think-aloud | FTUE and UX issues | 5 finds about 85% of usability issues (Nielsen); 8–10 recommended | Medium |
| Unmoderated telemetry | Funnels, balance, churn points | Balance 15–30; retention 30–100 or more | Low per player, high setup |
| Closed or open beta | Scale, economy, social | 100s | Medium |
| A/B test | One variable at a time | At least 20 per variant, 50+ recommended | Needs traffic and discipline |
| Regression testing | Nothing that worked before breaks | — | Automate where possible (2DGD) |

### 1.11.2 Running a session

1. **Write a hypothesis:** "We believe X. We will confirm or refute it by metric Y at threshold Z." For example: "4 of 5 testers can restate the core conflict within 1 minute" or "3 of 5 replay without being asked" (GameDesignOS).
2. **Control the variables:** the build, the device, the instructions, the time.
3. **The observer doesn't help** unless the tester has been stuck for more than 2 minutes. Write down timestamps, confusion, frustration and moments of delight, and grade how severe each one is.
4. **Post-session interview.** Use universal questions such as "What were you trying to do?", "When did you feel most and least in control?" and "What would you tell a friend this game is?". Ladder three levels deep with "why?".
5. **Questions you must not ask:**
   - leading questions;
   - compound questions;
   - questions that defend the design;
   - "would you pay $5?";
   - jargon.
6. **Banned words in reports** (gstack voice rule): "fun", "engaging" and "balanced", unless you define them concretely.

### 1.11.3 Interpreting results

- **Triangulate** observation, metrics and interviews:
  - one source is a hypothesis;
  - two sources are a pattern;
  - three sources give high confidence.
- **How widespread is it?**
  - A **systemic** issue affects 60% or more of testers.
  - A **segment** issue affects one persona.
  - Otherwise it is individual variance.
- **When does it appear?**
  - Immediately: a clarity problem.
  - Progressively: pacing.
  - At a threshold: a cliff.
- **Watch for bias:** confirmation, recency, the designer's own bias, and survivorship. People who quit are missing from your interviews.
- **Severity × frequency decides the action.** Fix anything high on both now. Watch anything low on both.
- **Every metric must map to a decision.** If no value of the number would change what you do, stop collecting it. Analysing video costs 3–5× the session length, so budget for it.
- **Personas for walkthroughs.** Run walkthroughs as each of gstack's seven personas:
  - Casual Newcomer;
  - Interested Returner;
  - Dedicated;
  - Hardcore Optimiser;
  - Streamer ("would I clip this?");
  - Lapsed Returner;
  - Genre Critic.
- **Emotion patterns.** A healthy pattern looks like Curious → Confused → Aha → Empowered. Unhealthy patterns include:
  - a death spiral;
  - no relief valve;
  - a content wall;
  - a pay-to-win moment;
  - social decay;
  - a complexity cliff;
  - a plateau.

### 1.11.4 Live experiments: GameDesignOS's weekly SOP

| Day | Step |
|---|---|
| Monday | Freeze the variant |
| Tuesday | Ship |
| Wednesday | Quality gates |
| Thursday | Check |
| Friday to Sunday | Collect data |
| Next Monday | Decide: **amplify, iterate, observe, roll back or kill** |

Rules for experiments:

- Pre-register the primary, secondary and **negative** metrics, the decision date and the owner of any rollback.
- Change one variable per variant.
- Segment results by new, returning and existing players.
- Make rollback a config switch.
- **Some wins are unacceptable:**
  - D1 rises but complaints rise too;
  - conversion rises through misleading UI or anxiety timers.

  Any dark pattern means **kill**, whatever the uplift.

**On Roblox:**

- **Test in a private place in the same universe**, with Team Test or a private server. Run Studio's local multi-client server to test social mechanics.
- **Protect minors in playtests.** Run moderated sessions with adult or 16+ testers you recruit through age-appropriate channels. Never collect personal data from in-game players, and never move minors into private off-platform contact. Use `PolicyService` before showing any external link reference `[VS]`.
  - Where anonymous in-game telemetry covers the question, prefer it.
  - Testers who appear in recordings must give consent (gstack: consent and NDA).
- **A/B tests in-game.** Hash the `UserId` into buckets, keep a player in the same bucket across sessions, and log the bucket with every analytics event. Thumbnail personalisation and testing are handled separately by Roblox `[VS]`.
- **Remember discovery lag.** Impressions respond to changes in your signals only after a few days `[VS]`. Recorded play-through rates also changed meaning after the 12 Oct 2026 measurement change, so never compare before and after that date `[VS]`.

Sources: fagemx/gstack-game:skills/playtest/SKILL.md, fagemx/gstack-game:skills/playtest/references/analysis-framework.md, fagemx/gstack-game:skills/playtest/references/metrics-and-benchmarks.md, fagemx/gstack-game:skills/playtest/references/gotchas.md, fagemx/gstack-game:skills/player-experience/references/personas.md, fagemx/gstack-game:skills/player-experience/references/emotion-vocabulary.md, DY-2026/GameDesignOS:game-concept-architect/references/prototype-validation-gate.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/weekly-experiment-sop.zh-CN.md, DY-2026/GameDesignOS:game-experience-density-optimizer/references/retention-risk-gates.zh-CN.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/prototype-fast/SKILL.md, 2DGD-F0TH/2DGD_F0TH:chapters/007_Refining/003_Testing.md, (general knowledge: Nielsen's five-user finding), (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/Signal and Impression Lag.md, Oct 12 2026 Measurement Change.md, Thumbnail Personalization.md)

---

## 1.12 Design review rubrics, checklists, failure modes and postmortems

### 1.12.1 Review scorecard

| Rubric | Scale | Pass | Notes |
|---|---|---|---|
| Core loop (1.1.4) | 0–10 | 7 or more | −3 if no target feelings are stated |
| Motivation | SDT 0–3, player types 0–3, consonance 0–2, emotional arc 0–2 (total /10) | 7 or more | Must name who the game is *not* for |
| Progression | FTUE 0–2, hooks 0–3, difficulty 0–2, churn points 0–3 (top 3 quit points, each with a mitigation) | 7 or more | — |
| Economy | Currency clarity, sinks and faucets 0–3, monetisation ethics 0–3, spending tiers 0–2 | 7 or more | −3 if there is no faucet/sink map |
| Feel | 7 dimensions × 0–2 = 14 (responsiveness, clarity, impact, rhythm, payoff, dead time, overload) | 12–14 = "alive" | — |
| Build playability | 6 dimensions × 0–2 = 12 (loop closure, session viability of 5+ min, onboarding within 60 s, failure recovery with a retry under 5 s, retention signal, peak moment) | 10–12 = "play-ready" | 0–3 = tech demo |
| Prototype slice | 5 axes × 0–2 = 10 | 8 or more | — |
| Balance review weights | Sections weighted 25/25/20/20/10 | — | — |

**Review rules** (gstack gotchas):

- **No sycophancy.** Never write just "needs balancing". State the imbalance, how it fails and the metric that shows it.
- **Designer intent is not player experience.**
- **Check sections against each other.** For example, does the paywall land at a churn point instead of a delight peak? Does a monetisation prompt sit next to a difficulty spike?
- **Watch for "game slop"** (generic patterns). If a screen or feature can be described in generic terms, it is slop. That includes stock UI, a "click to start" splash, and an unbranded shop grid. The house-rule art bar (cohesive, Blender-made, not AI-slop) applies to UI too.
- **After a retro**, ask: "Is the game more fun this sprint, or just more complete?" Keep to at most 3 action items. If team confidence is below 7/10, plan cuts until it reaches 8 or more.

### 1.12.2 Failure modes

**The 10 design fallacies** (gstack codex), each with what to check:

| Fallacy | What to check |
|---|---|
| Sunk cost | Would you start this feature today? |
| Feature creep | Does it serve a pillar? |
| Complexity bias | Does depth come from interactions or from adding rules? |
| Success theatre | Metrics that look good but don't change decisions |
| Platform mismatch | Session length and input fit |
| Audience mismatch | Is the stated audience the one actually playing? |
| Retention cargo cult | Copying dailies and streaks without a loop worth returning to |
| Monetisation–gameplay conflict | Does the money come from removing designed pain? |
| Scope optimism | The ×3 rule and the Lake/Ocean test |
| Uniqueness fallacy | Theme ≠ twist |

**Roblox-specific failure modes:**

- **Reskin clone.** Same loop, new theme, shipped after the parent game has peaked. Near-duplicate clones are penalised, and waves peak in 7–8 weeks `[VS]`.
- **A clickbait thumbnail that the first minute doesn't deliver.** This causes bounces and the anti-clickbait correction `[VS]`.
- **A tutorial wall or menu wall** before the first input.
- **A paywall or offer at the frustration point**, or a pop-up in the first minutes. This breaks house rule 3.
- **Four or more currencies**, or an economy with no sinks.
- **Absence punishment** and guilt messaging.
- **An empty large server.** Server size is too big for your CCU.
- **Stale updates.** No fixed update day, so there is no return reason in the D8–28 window `[VS]`.
- **Leftover primitive Parts** or walk-through props. This breaks house rules 1 and 2, and makes the world feel unfinished.

### 1.12.3 Pre-launch checklist (Roblox)

**Design**

- [ ] The micro-loop is fun with the reward UI hidden.
- [ ] The macro loop closes in session 1 (for example, the first rebirth at 15–25 min).
- [ ] Core fun happens inside 60 s, and the first reward or "number go up" moment comes before 180 s.
- [ ] A natural stopping point and a return hook are visible at the end of each session.
- [ ] Faucet/sink ratio is 0.9–1.1. The day-30 non-spender projection is checked. There are 3 or fewer currencies.
- [ ] Difficulty has no spike more than 2× the previous step, and no spike next to an offer.

**Monetisation (house rule 3)**

- [ ] No offers in the first 10 minutes or before the first meso win.
- [ ] Every offer is small, dismissible and rate-limited. A good default is at most 1 per 15 minutes and 3 per session, with silence after the player dismisses one.
- [ ] Timed 2× boosts, the starter pack, gift passes and convenience passes are set up. Luck and Server Luck exist only if the game has luck mechanics.
- [ ] No fake discounts, restarting countdowns or false scarcity. The odds for every paid random item are shown.
- [ ] Paid multipliers combined stay at 2× or less permanently. Stacking rules are shown on the HUD. There is no paid power in PvP.

**Art and collision (house rules 1 and 2)**

- [ ] An audit finds zero visible primitive Parts. Every visible object is a Blender GLB uploaded through Open Cloud. Helper Parts are invisible and kept in a named folder.
- [ ] A walk-through test passes. Players and NPCs can't pass through any solid model. Collision fidelity is chosen for each model class.
- [ ] The art bible's cohesion holds: one palette, one shape language, the same texel density everywhere. The squint test and skyline audit pass.

**Platform**

- [ ] 3–5 thumbnails and a gameplay video are ready. The title is unique, and nothing leads with Robux or a giveaway.
- [ ] FTUE funnel, economy and custom analytics events are live, and each one is mapped to a decision.
- [ ] Text filtering is applied to all player-written text. PolicyService checks are in place for random items, trading and links.
- [ ] A plan exists for the 16+ age gate. The weekly update day is fixed. The first event is scheduled.

### 1.12.4 The postmortem template

Write a postmortem after every jam, launch and major update (2DGD, gstack retro):

1. **Goal and hypothesis.** What you set out to prove, with the metric thresholds you set in advance.
2. **What happened.** Metrics against predictions: D1, D2–7 play days, session length, funnel drop-off, spend days.
3. **What went right.** 3–5 items, each with a cause.
4. **What went wrong.** 3–5 items, each with its root cause, not its symptom.
5. **Surprises.** The things nobody predicted. They are usually the most valuable lessons.
6. **Decisions.** Amplify, iterate, observe, roll back or kill, for each system.
7. **At most 3 action items**, each with an owner and a date.
8. **Lessons for the knowledge base.** One line each, reusable.

Sources: fagemx/gstack-game:skills/game-review/references/core-loop.md, fagemx/gstack-game:skills/game-review/references/motivation.md, fagemx/gstack-game:skills/game-review/references/progression.md, fagemx/gstack-game:skills/game-review/references/economy.md, fagemx/gstack-game:skills/game-review/references/cross-section.md, fagemx/gstack-game:skills/game-review/references/gotchas.md, fagemx/gstack-game:skills/feel-pass/references/scoring.md, fagemx/gstack-game:skills/build-playability-review/references/scoring.md, fagemx/gstack-game:skills/prototype-slice-plan/references/scoring.md, fagemx/gstack-game:skills/balance-review/references/scoring.md, fagemx/gstack-game:skills/game-codex/references/design-fallacies.md, fagemx/gstack-game:skills/plan-design-review/references/game-slop-patterns.md, fagemx/gstack-game:skills/game-retro/SKILL.md, 2DGD-F0TH/2DGD_F0TH:chapters/009_Putting_Yourself_Out_There/003_GameJams.md, 2DGD-F0TH/2DGD_F0TH:chapters/009_Putting_Yourself_Out_There/001_Dissecting_Games.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/game-jam/SKILL.md, (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/New Game Launch Checklist.md, Near-Duplicate Clone Penalty.md, Clickbait and Giveaway Penalty.md; _MOC.md executive summary)

---

## 1.13 Where the sources disagree, and how this section resolves it

| Topic | Source position | Conflict | Resolution used here |
|---|---|---|---|
| Microtransactions | 2DGD: cosmetic only; pay-to-win is hated. gstack: paying to remove designed pain is broken | House rule 3 requires timed 2× boosts and convenience passes | Boosts only speed up loops that are already fun. No paid PvP power. Permanent paid multipliers at 2× or less. Additive stacking recommended. Offers only at delight peaks (1.6.5) |
| Prototype art | gamedev-skills and gstack: greybox with primitives | House rule 1: no primitive builds ship | Recommended: a Blender blockout kit from day one. Bold: primitives only in a private, unpublished place, with a release gate audit (1.10.4) |
| Scarcity | 2DGD: "artificially low supply makes it valuable" | House rule 3: no false scarcity | Only genuine, disclosed limits ("until Dec 31"). Never fake stock counts (1.6.5) |
| Engagement psychology | BlackBook: "engineering addiction", greed via the gambler's fallacy, sunk-cost churn messaging | Ethics for a young audience | Use BlackBook's analytical audits only. Its manipulation tactics are banned (1.2.7) |
| Hook model claims | BlackBook: each extra click costs 10% conversion; core actions need 30% randomness | Unverified and unsourced | Treat as opinion. Measure your own funnel |
| Retention benchmarks | gstack: D1 40%, D7 15%, D30 5% "good" | Roblox medians are far lower (GameAnalytics); RoWatcher is far higher | Use Creator Analytics' similar-game benchmarks first, then GameAnalytics percentiles (1.8.2) |
| Pacing milestones | gstack: PC/console hours | Roblox sessions are short (median about 6.6 min) | Compress 5–10× (1.5.2) |
| Retention mechanics | Industry: daily streaks and FOMO timers | gstack and GameDesignOS: time gates create obligation; anxiety timers are kill criteria | Cumulative calendars, streak freezes, announced timers, no absence punishment (1.8.1) |
| PvP theft (Roblox hits) | Market data: loss-aversion theft drives sessions and spending | Distress for kids, cheating | Recommended: copy or share theft with protected slots. Bold: opt-in raid servers (1.2.7) |

**Gaps.**

- Quantitative studies of Roblox-specific monetisation tolerance are thin.
- The benchmarks here come from third parties or are heuristics. Calibrate them with live data.
- Roblox APIs and policies change often. Re-check every `[VS]` item before relying on it.

Sources: 2DGD-F0TH/2DGD_F0TH:chapters/008_Marketing_Community/001_Marketing/006_F2P.md, 2DGD-F0TH/2DGD_F0TH:chapters/007_Refining/001_Balancing/003_Economy.md, fagemx/gstack-game:skills/game-direction/SKILL.md, fagemx/gstack-game:skills/prototype-slice-plan/references/slice-types.md, fagemx/gstack-game:skills/game-review/references/progression.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/prototype-fast/SKILL.md, momowangOUO/GameDev-BlackBook:README.md, momowangOUO/GameDev-BlackBook:遊戲研發與發行全書 (The Game Dev's Black Book).md (Ch1–2 toolkits), DY-2026/GameDesignOS:game-experience-density-optimizer/references/retention-risk-gates.zh-CN.md, (Delta Vault: Roblox Research/2026-11 Market Scan/Algorithm/Retention Benchmarks.md; Patterns/Loss Aversion Through PvP Theft.md)

---

## Further reading (Part C: process, playtesting, reviews)

- Tynan Sylvester, *Designing Games*. Practical design process from the creator of RimWorld.
- Jonathan Blow, *Indie Prototyping* (talk). Prototype to find the game.
- Liz England, *The Door Problem*. What a designer actually does.
- Mark Rosewater, *Twenty Years, Twenty Lessons Learned* (GDC talk). Design lessons from Magic: The Gathering.
- Postmortem archives on Game Developer, plus data postmortems such as *Slay the Spire: Metrics* and *Among Us: The Data*.
- Game Accessibility Guidelines. An industry checklist to fold into reviews.

Sources: Roobyx/awesome-game-design:README.md, kkga/gamedesign-playlist:README.md



---

# 2. Game Craft Disciplines, Genre Playbooks and Architecture Patterns

This section takes general game craft and translates it to Roblox. The craft covers feel, level design, UI/UX, camera, input, audio, AI, procedural generation, saving, physics and performance. It also includes genre playbooks and the full Game Programming Patterns catalogue. Each topic gives the engine-neutral idea first, then an **On Roblox:** translation with concrete services, numbers and short Luau sketches.

The section is split across three files:

- **This file (2.0–2.6):** feel, level design, UI/UX, camera, input, audio.
- **`02-craft-and-patterns-part2.md` (2.7–2.11):** AI, procedural generation, save systems, physics and performance, genre playbooks.
- **`02-craft-and-patterns-part3.md` (2.12–2.13):** architecture patterns, prototyping workflow, further reading.

Some material comes from the author's own background rather than the source repos. That material is marked `(general knowledge)`. Version-sensitive claims are dated against **2026-11-08**.

## 2.0 How to use this section, and the house rules

The source skills are engine-neutral. Most of their examples are Godot, Unity or plain pseudocode. On Roblox the same ideas hold, but four platform facts change how they apply:

1. **The server is authoritative and the client is untrusted.** Every rule that touches progress, currency, damage or inventory runs on the server. "Juice" (camera shake, particles, UI pops, sounds) runs on the client, because it is cosmetic and latency-sensitive. Most Roblox systems therefore split cleanly into a server rule and a client presentation.
2. **The engine owns the game loop.** You do not write `while true do update() render() end`. You hook into `RunService` events (`Heartbeat`, `PreSimulation`, `PostSimulation`, `PreRender`, `PreAnimation`, `RenderStepped`, `Stepped`) and use the `dt` they pass.
3. **Every device plays the same server.** Phones, tablets, PCs, consoles and VR headsets can share one server. Design every screen, control and text size for the worst-case device. In practice that is usually a small phone held in landscape.
4. **Players arrive mid-session from discovery.** Many players join an existing server, play for minutes, and leave. The first 30–60 seconds must teach the core verb with no reading required (general knowledge).

**House rules.** These are the user's standing rules for Roblox games. Every recommendation in this section is aligned with them.

- **Blender for every visible 3D asset.** No primitive-Part builds and no marketplace models. Assets are exported as GLB in a headless Blender process and uploaded through Open Cloud. Where the generic advice says "greybox with primitives", treat the greybox as a throwaway planning artefact that never ships. You can block out in Blender with simple shapes. You can also block out with Studio Parts in a separate prototype place, or in a clearly named `_Blockout` folder that is deleted before release. Every one of those Parts is then replaced with a Blender model.
- **Everything visible is solid.** Every visible model gets proper collision: a simplified collision proxy, or a suitable `CollisionFidelity` such as `Box` or `Hull` for props and `PreciseConvexDecomposition` only where the shape truly matters. Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
- **Monetize heavily, but never invasively.** This rule wins any conflict. Offers are small, dismissible, well-timed (after a win, not in the first minutes) and rate-limited. The default product set is timed boosts (2× XP, 2× Cash, 2× speed for 10 minutes, and Luck or Server Luck only when the game has luck mechanics), a starter pack, gift versions of passes, and convenience game passes. There are no fake discounts, no restarting countdowns and no false scarcity. The genre playbooks below note natural monetization hooks. Monetization in depth is covered by another section.

The `create-game-assets` skill supports the Blender rule. Its 3D pipeline is DCC (Blender), then normalized transforms and pivots, then simplified collision proxies, then LODs, then GLB export, then validation in the engine. It also recommends describing the visual style along named axes: shape language, silhouette, value, colour, edge, material, light, detail density, camera and motion. Approve one "hero" asset before producing the rest in families. Then evaluate every asset at three distances: close, gameplay distance and far. This is the cheapest guard against the generic "AI slop" look the house rules forbid.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/create-game-assets/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/create-game-assets/references/three-d-pipeline.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/create-game-assets/references/art-direction.md, Roblox/creator-docs:content/en-us/reference/engine/classes/RunService.yaml

## 2.1 Game feel and juice

**The idea.** Game feel is the sum of tiny, fast responses that make an action feel physical. One "hit" in a polished game is not one event. It is a cluster of 5–8 small responses that all fire within about 100 ms:

- a flash on the target,
- a short hit-stop (freeze),
- camera shake,
- a particle burst,
- a sound,
- a squash/scale pop,
- a damage number,
- sometimes controller rumble.

Each response is exaggerated briefly and then returns to rest. Nothing should stay displaced. The deepnight "gamefeel" demo makes the same point by letting you toggle each small feature on and off, so you can see how much each one adds. Its source code is not in the cloned repo, so the specific technique list below comes from the game-feel skill and general knowledge, not from that demo.

**Scale by importance.** Juice is a budget. If every event gets the maximum, nothing feels special and the screen becomes noise. Assign each event a tier:

| Tier | Example | Trauma added | Hit-stop | Particles | Extras |
|---|---|---|---|---|---|
| Small | coin pickup, footstep, light hit | 0.10–0.20 | none | 0–4 | sound only, small pop |
| Medium | normal hit, door open, level-up tick | 0.30–0.50 | 0.04–0.06 s | 6–12 | 1–3 frame flash |
| Large | kill, boss hit, explosion, rare drop | 0.70–1.00 | 0.10–0.15 s | 20–40 | flash, brief zoom, big number |

**Typical values.**

- **Trauma shake.** Keep a `trauma` value between 0 and 1. Events add to it, and it decays at about 1.0–1.5 per second. The actual shake amount is `trauma²`, so small trauma barely moves the camera and large trauma moves it a lot. Drive the offset with smooth noise or summed sine waves, never with a fresh random number every frame, because white noise looks like jitter, not impact. A sensible maximum is roll of 0.05–0.12 radians and a small positional offset. In 2D the skill quotes 8–16 pixels. In 3D that is roughly 0.3–0.8 studs at third-person distance (general knowledge).
- **Hit-stop.** Freeze for 0.04 s on a light hit, up to 0.15 s on a heavy one. Time it with a real-time clock, not game time, otherwise it freezes itself. If hits overlap, only the newest hit-stop is allowed to restore normal speed.
- **Pop.** Scale to about 1.3 on one axis and 0.7 on the other (squash), then tween back to 1 with an EaseOutBack curve over about 0.18 s.
- **Flash.** 1–3 frames of a solid colour or emissive overlay on the target.
- **Damage numbers.** They rise, fade out, and drift a small random amount sideways so stacked hits stay readable.

**Easing cheat sheet.**

| Easing | Use it for |
|---|---|
| Back Out | a "pop" with overshoot |
| Quad or Cubic Out | settling into place |
| Cubic In | anticipation, a wind-up before a release |
| Sine InOut | camera moves and menu transitions |
| Linear | almost never for motion. Use it for progress bars that represent real time. |

**Juice checklist.** Run this for every core verb: hit, jump, collect, buy, level up, die.

1. Is there an immediate (same-frame) visual response at the point of action?
2. Is there a sound, and does it vary (see 2.6)?
3. Does the camera react, scaled to the event tier?
4. Does the UI react? For example, the counter pops and the number counts up instead of snapping.
5. Is there anticipation before big actions (wind-up), and follow-through after them (settle)?
6. Does everything return to rest? Nothing may remain offset, scaled or tinted.
7. Is the effect pooled, so that 30 hits per second do not allocate 30 new emitters?
8. Is there an accessibility path? Provide a camera-shake slider (default 60–80%), a "reduce flashing" option (no more than 3 flashes per second, WCAG 2.3.1), and a "reduce camera motion" option.

**Anti-patterns.**

- Shaking the character's body instead of the camera. This breaks aim and collision. Always shake the camera.
- Random-per-frame shake (jitter).
- Effects that outlive their cause.
- Identical maximum juice on every event.
- Juice that hides information, such as particles covering the enemy's attack telegraph.

**On Roblox:**

| Generic tool | Roblox tool |
|---|---|
| Tweens | `TweenService:Create(instance, TweenInfo.new(time, Enum.EasingStyle.Back, Enum.EasingDirection.Out), goals)` |
| Camera shake | Additive offset on `workspace.CurrentCamera.CFrame`, applied after the default camera updates. Use `Humanoid.CameraOffset` for position-only shake. |
| Particle bursts | `ParticleEmitter` with `Enabled = false`, then call `emitter:Emit(count)` per event |
| Trails and beams | `Trail` for swings, `Beam` between two `Attachment`s for lasers and tethers |
| Outline flash | `Highlight` (client limit is 255 at once per current docs; the older limit was 31, so check before relying on it) |
| UI pop | `UIScale` on the GuiObject, tweened. `UIStroke` thickness or colour pulse for emphasis. |
| Mixing | `SoundGroup`s, or the newer `AudioFader` and `AudioCompressor` graph (see 2.6) |
| Hit-stop | Pause the relevant `AnimationTrack`s with `track:AdjustSpeed(0)` for 0.04–0.15 s on the client. You cannot freeze the server's physics, so hit-stop is a local presentation trick only. |
| Character feedback | Brief `Highlight` or a material or colour flash on the Blender mesh, a knockback impulse applied by the server, a hurt animation |

Run all of this in a LocalScript, triggered by a `RemoteEvent` from the server or by local prediction. The server decides that the hit happened. The client decides how it looks.

The default camera scripts read the camera's current CFrame in some code paths. If you add shake on top every frame and never remove it, the rotation can creep into the player's view direction. The safe pattern is to remove last frame's shake before the default camera runs, and add the new shake after it runs (general knowledge):

```lua
-- LocalScript. Trauma-based camera shake that never accumulates.
local RunService = game:GetService("RunService")
local camera = workspace.CurrentCamera

local Shake = {}
local trauma = 0
local DECAY = 1.2                -- trauma lost per second
local MAX_ROLL = math.rad(4)     -- about 0.07 rad
local MAX_PITCH_YAW = math.rad(2)
local MAX_OFFSET = 0.5           -- studs
local FREQ = 15                  -- noise speed
local userScale = 0.7            -- settings slider, 0 to 1
local applied = CFrame.identity  -- the offset we added last frame

function Shake.add(amount: number)
	trauma = math.min(1, trauma + amount)
end

-- Remove last frame's offset before the default camera updates.
RunService:BindToRenderStep("ShakeUndo", Enum.RenderPriority.Camera.Value - 1, function()
	camera.CFrame = camera.CFrame * applied:Inverse()
	applied = CFrame.identity
end)

-- Add this frame's offset after the default camera updates.
RunService:BindToRenderStep("ShakeApply", Enum.RenderPriority.Camera.Value + 1, function(dt)
	if trauma <= 0 then
		return
	end
	trauma = math.max(0, trauma - DECAY * dt)
	local s = trauma * trauma * userScale
	local t = os.clock() * FREQ
	-- math.noise is smooth. Offsetting each axis keeps them uncorrelated.
	local pitch = MAX_PITCH_YAW * s * math.noise(t, 0.31)
	local yaw = MAX_PITCH_YAW * s * math.noise(t, 4.73)
	local roll = MAX_ROLL * s * math.noise(t, 9.17)
	local ox = MAX_OFFSET * s * math.noise(t, 13.6)
	local oy = MAX_OFFSET * s * math.noise(t, 21.4)
	applied = CFrame.new(ox, oy, 0) * CFrame.Angles(pitch, yaw, roll)
	camera.CFrame = camera.CFrame * applied
end)

return Shake
```

A UI pop and a pooled burst can share one helper:

```lua
local TweenService = game:GetService("TweenService")
local POP = TweenInfo.new(0.18, Enum.EasingStyle.Back, Enum.EasingDirection.Out)

local function pop(gui: GuiObject, peak: number?)
	local scale = gui:FindFirstChildOfClass("UIScale")
	if not scale then
		scale = Instance.new("UIScale")
		scale.Parent = gui
	end
	scale.Scale = peak or 1.25
	TweenService:Create(scale, POP, { Scale = 1 }):Play()
end

local function burst(emitter: ParticleEmitter, tier: "small" | "medium" | "large")
	local counts = { small = 3, medium = 10, large = 30 }
	emitter:Emit(counts[tier]) -- the emitter lives on a reused Attachment and is never cloned per hit
end
```

Hit-stop with a token, so only the newest call restores speed:

```lua
local stopToken = 0
local function hitStop(tracks: { AnimationTrack }, duration: number)
	stopToken += 1
	local myToken = stopToken
	for _, track in tracks do
		track:AdjustSpeed(0)
	end
	task.delay(duration, function()
		if myToken ~= stopToken then
			return -- a newer hit-stop owns the restore
		end
		for _, track in tracks do
			track:AdjustSpeed(1)
		end
	end)
end
```

Roblox-specific pitfalls (general knowledge):

- `Highlight` is cheap to toggle but expensive to create in bulk. Keep one per target and toggle `Enabled`.
- Particle-heavy effects cost the most on low-end phones. Cap emitter counts per tier and lower `Rate` when the device is weak.
- Never fire one `RemoteEvent` per particle. Send one event per gameplay fact ("hit at position X, tier medium") and let the client build the cluster.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-feel/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-feel/references/feedback-recipes.md, deepnight/gamefeel:README.md, Roblox/creator-docs:content/en-us/reference/engine/classes/Highlight.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/RunService.yaml

## 2.2 Level design

**Metrics come first.** Before building any space, derive the character's movement metrics. Every gap, ledge and corridor size depends on them:

- `MAX_JUMP_HEIGHT = v² / (2g)`, where `v` is the jump's starting vertical speed and `g` is gravity.
- `AIR_TIME = 2v / g`.
- `MAX_JUMP_DISTANCE = run_speed × AIR_TIME` (level ground).
- `SAFE_GAP = 0.7 × MAX_JUMP_DISTANCE`. Use it on the critical path and for new players.
- `HARD_GAP = 0.95 × MAX_JUMP_DISTANCE`. Use it only for optional or expert challenges.

The formulas are idealized. Confirm them with a measured "gap ladder": a test strip of gaps and ledges at increasing sizes, which you jump yourself on every device type.

**Workflow: blockout, test, iterate, dress.** Lay out the space in simple volumes, playtest it, change it until the flow works, and only then dress it with final art. Dressing too early wastes art time and hides layout problems. Under the house rules, the blockout is a disposable planning artefact. The dressed level is built entirely from Blender models.

**Paths.**

- The **critical path** is the minimum route to finish.
- The **golden path** is the intended, best-feeling route, which usually passes the best views and teaching moments.
- **Branches** are optional detours that pay off with secrets, shortcuts or rewards.

**Pacing.** Tension should follow a sawtooth: build, peak, release, then build higher. Always place a rest before a climax, so the player arrives at the boss or hard section calm and stocked up. A beat table is the simplest planning tool:

| Room or segment | Beat type | Intensity (1–5) | Teaches or tests |
|---|---|---|---|
| Spawn plaza | rest / orientation | 1 | camera, movement |
| First jumps | introduce | 2 | jump |
| Moving platforms | develop | 3 | timing |
| Collapsing bridge | twist | 4 | jump plus urgency |
| Checkpoint garden | rest | 1 | — |
| Tower climb | test | 5 | everything so far |

**The teaching loop.** Introduce a mechanic in a safe place. Develop it with slightly harder variants. Twist it by combining it with something else or changing the context. Test it with no hand-holding. This four-beat structure mirrors kishotenketsu: introduction, development, twist, conclusion. It works because the twist teaches the player something new about a mechanic they thought they understood.

**Gating.** Gates control order and pacing.

- **Lock and key.** A door needs an item or a switch.
- **Ability gate.** You need double jump to reach the ledge.
- **One-way drop.** Always telegraph it. The player must be able to see that they cannot come back, before they commit.
- **Soft gate.** A tough enemy or long route discourages but does not forbid.

Every gated level needs a soft-lock check. Starting from the spawn, repeatedly grow the reachable set: everything you can reach with the keys and abilities you hold, then add any newly unlocked keys and abilities, until nothing changes. If the goal is not in the final set, the level can soft-lock. Run this check automatically on generated levels (see 2.8).

**Guidance without walls.** A lost player is fixed with guidance, not with invisible walls. The tools:

- light and contrast (the path is brighter),
- leading lines (rails, roads, cables, rows of lamps),
- landmarks visible from far away (a tower, a glowing tree),
- breadcrumbs (coins or pickups along the route),
- framed vistas that show the goal,
- one consistent colour for "interactable" or "climbable" across the whole game.

**Hubs.** A hub-and-spoke layout puts a central safe area with clear exits to each activity. Each spoke should be visible from the hub centre, labelled by a landmark rather than only text, and return the player to the hub when finished.

**Blockout review checklist.**

1. Can a new player see the next objective from every checkpoint?
2. Are all critical-path gaps at or below `SAFE_GAP`?
3. Does every one-way drop have a visible telegraph?
4. Is there a rest beat before every intensity-5 beat?
5. Is there at least one landmark visible from every major area?
6. Does the soft-lock check pass?
7. Does the space read on a phone screen? Small details that matter on PC can vanish on mobile.
8. Did you measure flow with real playtesters, not just the designer?

**On Roblox:**

Roblox character defaults, per the current creator docs:

| Value | Default |
|---|---|
| `Humanoid.WalkSpeed` (`StarterPlayer.CharacterWalkSpeed`) | 16 studs/s |
| `Humanoid.JumpPower` | 50 (range 0–1000) |
| `Humanoid.JumpHeight` | 7.2 studs |
| `Humanoid.MaxSlopeAngle` | 89° |
| `workspace.Gravity` | 196.2 studs/s² |

Which jump property applies depends on `UseJumpPower` (and `StarterPlayer.CharacterUseJumpPower`). The docs list the default as `true`. Newer places and templates may use `JumpHeight` instead, so check StarterPlayer in your place before trusting any table. This is version-sensitive. To stop jumping, use `Humanoid:SetStateEnabled(Enum.HumanoidStateType.Jumping, false)` rather than setting the power to 0. The docs also note that gamepad and touch thumbsticks can move the character slower than `WalkSpeed` when the stick is not fully deflected. Design gaps for full-speed keyboard players, but test them on a stick.

Derived numbers (idealized, measure before trusting):

| Setting | Jump height | Air time | Running jump at WalkSpeed 16 | Safe gap (0.7×) | Hard gap (0.95×) |
|---|---|---|---|---|---|
| JumpPower 50 | ≈ 6.37 studs | ≈ 0.51 s | ≈ 8.2 studs | ≈ 5.7 studs | ≈ 7.8 studs |
| JumpHeight 7.2 | 7.2 studs | ≈ 0.54 s | ≈ 8.7 studs | ≈ 6.1 studs | ≈ 8.2 studs |

Other useful metrics (general knowledge; measure in your place):

- The default R15 character is about 5 studs tall. The pathfinding agent defaults (`AgentHeight` 5, `AgentRadius` 2) match this.
- Doors should be at least 7 studs tall and 4–5 studs wide. Corridors in multiplayer areas should be 8 or more studs wide so groups do not block each other.
- A comfortable climbable ledge is about 80% of the jump height. That is roughly 5 studs with JumpPower 50.

A small helper keeps metrics in one place, so every level designer and generator uses the same numbers:

```lua
-- ModuleScript: LevelMetrics
local Metrics = {}

function Metrics.compute(walkSpeed: number, jumpVelocity: number, gravity: number)
	local airTime = 2 * jumpVelocity / gravity
	local maxDist = walkSpeed * airTime
	return {
		maxHeight = jumpVelocity ^ 2 / (2 * gravity),
		airTime = airTime,
		maxDistance = maxDist,
		safeGap = 0.7 * maxDist,
		hardGap = 0.95 * maxDist,
	}
end

-- JumpPower is the starting vertical speed. For JumpHeight h, the speed is math.sqrt(2 * g * h).
Metrics.default = Metrics.compute(16, 50, workspace.Gravity)

return Metrics
```

**Obby design.** An obby is a pure level-design genre. Apply the sawtooth and the teaching loop per stage group. Place a checkpoint every 30–60 seconds of expected play, and more often early (general knowledge). Introduce each new obstacle type alone, then combine it. Measure stage completion rates and deaths per stage with analytics. A stage where many players quit is a design bug, not a skill check.

**Hub-and-spoke lobbies.** The spawn hub is the first thing a discovery player sees. Keep it compact, so every activity is reachable within about 10 seconds of walking. Mark the portals or spokes with Blender-built landmarks, and keep shops visible but out of the main walking line (general knowledge).

**Spawn design.**

- Spawns are technical helpers, so a `SpawnLocation` may be invisible (`Transparency = 1`, `CanCollide = false`), placed inside or above a Blender-built spawn pad that carries the visible collision.
- Face the spawn toward the first objective.
- Never spawn players inside a path that other players run through.
- Give spawn protection where combat exists.

**Kill zones.** A "kill brick" becomes a Blender lava or spike model with real collision. An invisible, non-colliding trigger part handles the `Touched` logic.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/level-design/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/level-design/references/pacing-and-flow.md, Roblox/creator-docs:content/en-us/reference/engine/classes/Humanoid.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/StarterPlayer.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/Workspace.yaml, Roblox/creator-docs:content/en-us/characters/pathfinding.md

## 2.3 Game UI and UX (design level)

This subsection is about UI design decisions. Roblox UI implementation detail (layouts, constraints, components) belongs to another section.

**HUD hierarchy.** Rank every HUD element by how often the player needs it during play:

1. **Always visible, glanceable:** health, the current objective, the primary currency.
2. **Visible on change:** ammo, cooldowns, pickup notifications. These fade in when they change and fade out after a few seconds.
3. **On demand:** inventory, map, settings, shop. These live behind a button or key.

Put the most important information where the eyes already are, usually near the character or the screen centre. Peripheral corners hold secondary information.

**Diegetic, non-diegetic and spatial UI.**

- **Diegetic UI** exists in the world. An example is a health bar painted on the character's back.
- **Non-diegetic UI** is a screen overlay.
- **Spatial UI** sits in the world but is not part of the fiction, like a floating name tag or a waypoint marker.

Diegetic UI is immersive but can be hard to read. Use it for mood and keep critical information non-diegetic. World-space markers for off-screen targets should clamp to the screen edge and point toward the target.

**Structure.**

- Anchor UI to screen edges and containers, not absolute pixels.
- Pick a reference resolution and a scaling policy.
- Respect the device safe area (notches, rounded corners).
- Every screen needs an initial focus target, so gamepad and keyboard users are never lost.
- Manage menus as a stack: opening a menu pushes it, Back pops it, and Back always works.
- Make the HUD event-driven. It updates when a value changes, rather than polling every frame.

**Feedback states.** Every interactive element needs visible states: normal, hover or focus, pressed, disabled and selected. A press state of 100–150 ms with a light sound is the minimum. A button that does nothing when pressed is a P0 bug, because the player assumes the game is broken. Disabled buttons should explain why they are disabled ("Need 50 coins").

**Readability and accessibility.** Concrete numbers from the Xbox Accessibility Guidelines, as summarised by the source skill:

- **Text size (XAG 101):** at least 26 px at 1080p for TV-distance play and at least 18 px for PC. Text should be scalable to 200%.
- **Contrast (XAG 102):** at least 4.5:1 for body text and 3:1 for large text.
- **Colour:** never encode state by colour alone. Add an icon, shape or label, because about 8% of men have some colour-vision deficiency (general knowledge).
- **Touch targets:** at least about 9 mm physical size, with spacing between them.
- **Localization:** leave about 30% extra width, because German and other languages run longer than English.

**Evaluating usability.** The Shupianmaka game-UX evaluation skill gives a full review framework. It scores ten dimensions from 1 to 5:

1. learnability
2. operability
3. information architecture
4. visual usability
5. feedback
6. error tolerance and recovery
7. efficiency
8. context adaptivity
9. accessibility
10. emotional design

Each finding gets a severity from P0 (blocks the core flow) to P3 (polish), and a confidence: confirmed, suspected or to-confirm. It asks you to:

- Infer the design goal before judging.
- Observe before judging.
- Analyse three player stages separately: new, mid and hardcore.
- Make every recommendation concrete. Write "add a 100–150 ms press state and a light click sound", not "improve feedback".

It grounds its judgements in Nielsen's heuristics, Norman's design principles, Fitts's law (big, close targets are faster), Hick's law (more choices means slower decisions), Miller's limits on working memory, MDA, flow theory and Bartle's player types.

**Anti-patterns.**

- Modal popups during play.
- More than about 5–7 top-level HUD elements.
- Tiny text on mobile.
- Hidden Back buttons.
- Currency counters that snap instead of counting up.
- Notifications that stack forever.
- Shop buttons placed where the thumb lands during play, which causes accidental purchase prompts. The Roblox purchase dialog will still ask for confirmation, but the interruption itself is invasive.

**On Roblox:**

**Core UI zones.** Roblox reserves screen zones for core UI: the top-left Roblox menu and chat, and the top-right player list. Do not put game buttons there. Query `GuiService:GetGuiInset()`, or use `ScreenGui.ScreenInsets` with `Enum.ScreenInsets.CoreUISafeInsets` or `DeviceSafeInsets`, rather than hard-coding offsets. The top bar's size has changed in past redesigns, so hard-coded numbers break (general knowledge, version-sensitive).

**Mobile thumb zones.** On a landscape phone (general knowledge):

- The left thumb owns the bottom-left third (the movement thumbstick).
- The right thumb owns the bottom-right (jump and action buttons).
- The top centre is the hardest to reach. Use it for read-only information such as timers and objectives.
- Put the main action button near the default jump button, with at least about 9 mm of separation so players do not mis-tap.
- Keep shop and menu buttons on the left or right edge at mid-height. They are reachable on purpose, but not under the thumb during play.

**Event-driven HUD.** Drive the HUD from attribute or value change signals, not polling:

```lua
-- LocalScript. The HUD coin counter updates only when the server changes the attribute.
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local player = Players.LocalPlayer
local label = script.Parent :: TextLabel

local counter = Instance.new("NumberValue") -- one reusable value drives the count-up
counter.Value = player:GetAttribute("Coins") or 0
label.Text = tostring(counter.Value)
counter.Changed:Connect(function(v)
	label.Text = tostring(math.floor(v + 0.5))
end)

local COUNT_UP = TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
local active: Tween? = nil

player:GetAttributeChangedSignal("Coins"):Connect(function()
	if active then
		active:Cancel() -- a new change interrupts the old count-up from its current value
	end
	local tween = TweenService:Create(counter, COUNT_UP, { Value = player:GetAttribute("Coins") or 0 })
	active = tween
	tween:Play()
end)
```

**Accessibility settings (version-sensitive).** Roblox exposes some user-level settings, such as reduced motion and preferred text size, through `GuiService` in recent engine versions. Check that the property exists before reading it, and offer your own in-game sliders as well, because not every setting is covered (general knowledge).

**Spatial UI.** Use `BillboardGui` for spatial labels and markers, with a `MaxDistance` so distant markers do not clutter the screen. Use `SurfaceGui` on a Blender model's face for diegetic screens such as a shop sign, a scoreboard or a tycoon display.

**Offer popups.** These follow the house rules:

- Small, in a corner, with an obvious close button.
- Never shown in the first few minutes, and never during active combat or an obby jump.
- Shown after a positive moment (a win or a level-up).
- Rate-limited, for example at most one unsolicited offer per 10–15 minutes and never the same offer twice in a session after it was dismissed (general knowledge; tune with analytics).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-ui-ux/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-ui-ux/references/layout-and-flow.md, Shupianmaka/codex-game-ux-skills:game-interaction-usability-eval/SKILL.md, Shupianmaka/codex-game-ux-skills:game-interaction-usability-eval/references/evaluation-framework.md

## 2.4 Camera design

**Smoothing must be frame-rate independent.** A naive `pos = lerp(pos, target, 0.1)` behaves differently at 30 and 144 fps. Use exponential smoothing instead:

```
alpha = 1 - exp(-rate * dt)
pos = lerp(pos, target, alpha)
```

A `rate` of 5–12 per second covers most follow cameras. Lower values feel floaty and cinematic. Higher values feel tight and responsive.

**Follow and framing.**

- **Deadzone.** The camera ignores small target movement inside a box or circle around the centre. The skill quotes 32–64 px for 2D. A box deadzone suits platformers, where horizontal and vertical movement differ. A radial deadzone suits top-down games.
- **Look-ahead.** Shift the camera toward where the player is moving or aiming. The skill quotes 40–120 px, eased in over 0.2–0.4 s so it does not snap when direction changes.
- **Clamp the view, not the centre.** World bounds should limit the visible rectangle, so the camera never shows outside the level.
- **Platformers.** Lock or slow vertical follow, so the camera does not bounce on every jump. Update the vertical position mainly when the player lands on a new height.

**3D orbit cameras.**

- Clamp pitch to about −80° to +45°, so the player cannot look straight up through the floor. First-person cameras use about ±80° to ±89°.
- Use a spring arm: cast from the target toward the desired camera position and pull the camera in front of any obstacle.
- Update the camera after the target has moved this frame, otherwise it lags by a frame and jitters.
- Shake (2.1) is an additive offset applied last.
- Reset smoothing on teleport or respawn, otherwise the camera sweeps across the map.

**Anti-patterns.**

- Smoothing with a constant lerp factor.
- Shake baked into the follow logic.
- Cameras that clip into walls.
- Forced camera moves during player control.
- Field-of-view changes larger than about 10–15° without a reduce-motion option (general knowledge).

**On Roblox:**

- **Default camera.** The default `PlayerModule` camera already gives orbit, zoom, spring-arm collision ("Popper") and shift-lock. Change it only when the genre needs it. Useful properties (general knowledge; check current defaults):
  - `Camera.FieldOfView` (70 by default)
  - `Player.CameraMinZoomDistance` and `CameraMaxZoomDistance` (0.5 and 128 by default, set from `StarterPlayer`)
  - `StarterPlayer.CameraMode` (`Classic` or `LockFirstPerson`)
  - `StarterPlayer.EnableMouseLockOption` (shift-lock)
  - `Humanoid.CameraOffset` (shoulder offset)
- **Custom cameras.** Set `Camera.CameraType = Enum.CameraType.Scriptable` and drive `Camera.CFrame` from `RunService:BindToRenderStep` at `Enum.RenderPriority.Camera.Value`. Typical uses are a side-scroller, a top-down tycoon view or a cutscene.
- **Spring arm.** Use `workspace:Raycast(origin, direction, params)` from the head toward the desired position, filter out the character, and place the camera slightly in front of the hit point.
- **Mobile.** Players rotate the camera by dragging the right side of the screen. Do not put drag-heavy UI there.

```lua
-- LocalScript. Side-scroller camera with exponential smoothing and lazy vertical follow.
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local camera = workspace.CurrentCamera
camera.CameraType = Enum.CameraType.Scriptable

local RATE_X, RATE_Y = 9, 3 -- tight horizontally, lazy vertically
local DISTANCE = 40
local focus: Vector3? = nil

RunService:BindToRenderStep("SideCam", Enum.RenderPriority.Camera.Value, function(dt)
	local character = Players.LocalPlayer.Character
	local root = character and character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then
		return
	end
	local target = root.Position + root.AssemblyLinearVelocity * Vector3.new(0.15, 0, 0) -- look-ahead
	if focus == nil or (target - focus).Magnitude > 60 then
		focus = target -- reset on teleport or respawn
	end
	local current = focus :: Vector3
	local ax = 1 - math.exp(-RATE_X * dt)
	local ay = 1 - math.exp(-RATE_Y * dt)
	local nextFocus = Vector3.new(
		current.X + (target.X - current.X) * ax,
		current.Y + (target.Y - current.Y) * ay,
		target.Z
	)
	focus = nextFocus
	camera.CFrame = CFrame.lookAt(nextFocus + Vector3.new(0, 4, DISTANCE), nextFocus)
end)
```

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/camera-systems/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/camera-systems/references/follow-and-framing.md, Roblox/creator-docs:content/en-us/reference/engine/classes/RunService.yaml

## 2.5 Input and controls across devices

**Map actions, not keys.** Gameplay code asks "was Jump pressed?", never "was Space pressed?". A mapping layer turns keys, buttons and touches into actions. This one decision makes rebinding, gamepad support, touch support and accessibility possible.

**Edge versus held.** Distinguish "just pressed" (fire once) from "held" (continuous). Most "the button fires twice" bugs come from mixing the two.

**Sticks.** Apply a radial deadzone of about 0.2 and rescale the remaining range to 0–1, so movement starts smoothly at the deadzone edge. Then apply a response curve (an exponent of about 1.5–2 gives fine control near the centre). Keep sensitivity, which is a multiplier, separate from the response curve, which is a shape. Players tune them independently.

**Forgiveness windows.** These are what make controls feel fair:

- **Input buffering:** remember a press for 100–150 ms, so a jump pressed just before landing still happens.
- **Coyote time:** allow a jump for 80–120 ms after walking off a ledge.
- Both are consumed on use. A buffered jump fires once and then clears.

**Rebinding.** Support full remapping with conflict detection (warn when two actions share a key), persist the choice, and offer a reset to defaults.

**Prompts.** Switch on-screen button prompts to the last-used device, and switch as soon as a different device is used. On gamepads, refer to button positions (South, East, West, North) rather than letters, because Xbox and PlayStation layouts differ.

**Touch.** Use a floating-origin virtual stick: the stick centre appears where the thumb first lands. It feeds the same action layer as keyboard and gamepad.

**Accessibility.**

- Full remapping.
- A toggle option for every hold action.
- No required simultaneous chords.
- Adjustable timing windows.
- Axis inversion.
- No input that requires rapid repeated tapping without an alternative.

**On Roblox:**

- **Device detection.** `UserInputService.PreferredInput` reports the player's current preferred input: `KeyboardAndMouse`, `Gamepad`, `Touch` or `MicroGamepad`. Use it to switch prompts and layouts. It is newer than the older `TouchEnabled`/`KeyboardEnabled`/`GamepadEnabled` checks, which describe hardware, not intent. A touchscreen laptop has both.
- **Input Action System (version-sensitive).** The newer Input Action System models the action layer as instances:
  - `InputContext`, with `Enabled`, `Priority` and `Sink`, so a menu context can override gameplay.
  - `InputAction`, with `Pressed`, `Released` and `StateChanged` events and a `Type` such as Bool or Direction2D.
  - `InputBinding`, which maps a `KeyCode`, a `UIButton` for touch, a `PrimaryModifier`, a `ResponseCurve`, a `PressedThreshold` and a `Scale` to an action.

  It is the closest built-in match to "map actions, not keys". Because it is relatively new, check its current status and API in the creator docs before standardizing on it.
- **Stable fallback.** `ContextActionService:BindAction(name, handler, createTouchButton, ...inputs)` binds one action to several inputs and can create a mobile button.
- **Defaults to keep.** The default `PlayerModule` handles movement on all devices, including the dynamic thumbstick on mobile. Leave it alone unless you have a strong reason.

Jump buffering and coyote time on top of the default Humanoid (general knowledge):

```lua
-- LocalScript. Adds a 120 ms jump buffer and 100 ms coyote time to the default character.
local ContextActionService = game:GetService("ContextActionService")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")

local BUFFER, COYOTE = 0.12, 0.10
local lastPressed = -math.huge
local lastGrounded = -math.huge

local function consume()
	lastPressed = -math.huge -- consume the buffer
	lastGrounded = -math.huge -- consume coyote time
end

-- Any jump, including the default one, consumes both windows.
-- Without this, a held buffer would fire a second jump in mid-air.
local function onCharacter(character: Model)
	local humanoid = character:WaitForChild("Humanoid") :: Humanoid
	humanoid.StateChanged:Connect(function(_, new)
		if new == Enum.HumanoidStateType.Jumping then
			consume()
		end
	end)
end
Players.LocalPlayer.CharacterAdded:Connect(onCharacter)
if Players.LocalPlayer.Character then
	onCharacter(Players.LocalPlayer.Character)
end

ContextActionService:BindActionAtPriority("BufferedJump", function(_, state)
	if state == Enum.UserInputState.Begin then
		lastPressed = os.clock()
	end
	return Enum.ContextActionResult.Pass -- let the default jump still run
end, false, Enum.ContextActionPriority.High.Value, Enum.KeyCode.Space, Enum.KeyCode.ButtonA)

RunService.Heartbeat:Connect(function()
	local character = Players.LocalPlayer.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if not humanoid then
		return
	end
	local now = os.clock()
	if humanoid.FloorMaterial ~= Enum.Material.Air then
		lastGrounded = now
	end
	if now - lastPressed <= BUFFER and now - lastGrounded <= COYOTE then
		-- Covers both cases: pressed just before landing, or just after leaving a ledge.
		humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
	end
end)
```

Touch players use the default jump button. Bind the same action through it, or through an `InputBinding` with a `UIButton`, if you need buffering there too.

**Rebinding.** Persist bindings per player, in a settings table saved with the profile, and validate them on load. Roblox reserves some keys and buttons for core UI (for example, Escape and the gamepad menu button), so exclude them from rebinding (general knowledge).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/input-systems/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/input-systems/references/buffering-and-accessibility.md, Roblox/creator-docs:content/en-us/reference/engine/classes/UserInputService.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/InputContext.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/InputAction.yaml, Roblox/creator-docs:content/en-us/reference/engine/classes/InputBinding.yaml

## 2.6 Audio design

**The bus tree.** Route every sound through a bus. A bus is a group with one volume.

```
Master
├── Music
├── SFX
├── Ambience
├── UI
└── Voice
```

Settings sliders control buses, never individual sounds. Work in decibels internally. Human loudness perception is roughly logarithmic, so a linear 0–1 slider should be squared (or mapped through a dB curve) before it is applied. Otherwise the bottom half of the slider seems to do nothing.

**Loudness targets.** These come from Sony's ASWG-R001, as quoted by the source skill:

- True peak at most −1 dBTP.
- Integrated loudness about −24 LUFS ±2 for console and PC.
- About −18 LUFS for mobile, because phone speakers and noisy environments need it louder.

Pick one target, master all music and SFX against it, and keep it.

**Ducking.** Important sounds (dialogue, alerts) temporarily lower less important ones. There are two approaches:

- **Sidechain compression:** a compressor on the Music bus listens to the Voice bus. Typical settings are a threshold of about −30 dB, a ratio of 4–8:1, attack of 10 ms or less, and release of 300–500 ms.
- **Simple volume duck:** tween the Music bus down by about −12 dB over 0.25 s while the important sound plays, then back up.

**SFX variation.** Repetition is the fastest way to make audio feel cheap.

- Randomise pitch by about ±1 semitone and volume by about ±2 dB.
- Use a pool of 3–5 recorded variants per sound, and never play the same variant twice in a row.
- Cap polyphony per sound, for example at most 4 simultaneous coin pickups. Steal the oldest voice when over the cap.

**Adaptive music.**

- **Vertical layering.** Stems such as drums, bass and melody play in sync. Layers fade in or out over 0.5–1.5 s as intensity changes.
- **Horizontal re-sequencing.** Switch between sections, but only at bar boundaries. Use short transition segments and stingers (one-shot musical hits) for events.
- **Smoothed intensity.** Feed the music from a smoothed intensity value with hysteresis, for example go up at 0.6 and come back down at 0.4, so the music does not flicker between states.
- **Beat sync.** Read the beat from the audio playback clock, not from the game clock, which drifts.

**Feedback sounds.**

- Every UI action gets a sound: a light click on press, a positive chime on success, a dull thud on denial.
- Every gameplay verb gets a layered sound: a transient "attack", a body and a tail.
- Rewards should sound better as they get rarer. Escalate pitch on combos and streaks.

**On Roblox:**

- **Legacy API.**
  - `Sound` objects routed to `SoundGroup`s with `Sound.SoundGroup`. Each `SoundGroup` has a `Volume` and can hold effects such as `EqualizerSoundEffect`, `ReverbSoundEffect` and `CompressorSoundEffect`. The compressor has a `SideChain` property for ducking.
  - A `Sound` parented to a part or attachment is 3D. A `Sound` in `SoundService` or a GUI is 2D.
  - `SoundService:PlayLocalSound(sound)` plays UI sounds on the client.
- **Newer audio graph (version-sensitive).** The newer audio API builds explicit graphs:
  - `AudioPlayer` connected by `Wire`s to `AudioFader`, `AudioEqualizer`, `AudioCompressor` (which has `Input` and `Sidechain` pins), `AudioReverb` and `AudioLimiter`.
  - Graphs end at `AudioDeviceOutput`, or at `AudioEmitter` and `AudioListener` for 3D sound.

  This maps one-to-one onto the bus tree and sidechain ducking described above. Check current docs before you mix the two systems in one game, because they are routed differently.
- **3D falloff.** Use `RollOffMinDistance`, `RollOffMaxDistance` and `RollOffMode` (`InverseTapered` is a good default) so distant sounds do not fill the mix (general knowledge).
- **Assets.** Roblox audio assets have privacy and permission rules: uploaded audio must be usable by your experience. Check permissions when a sound plays silently (general knowledge, version-sensitive).

A volume slider, a duck and a varied one-shot:

```lua
-- LocalScript (client-side mixing).
local SoundService = game:GetService("SoundService")
local TweenService = game:GetService("TweenService")
local musicGroup = SoundService:WaitForChild("Music") :: SoundGroup

local userMusic = 0.8 -- slider value 0..1 from settings
local function applyMusicVolume(duckFactor: number)
	local target = (userMusic * userMusic) * duckFactor -- squared slider, then the duck
	TweenService:Create(musicGroup, TweenInfo.new(0.25), { Volume = target }):Play()
end

local DUCK = 10 ^ (-12 / 20) -- -12 dB is about 0.25 linear
local function duckFor(seconds: number)
	applyMusicVolume(DUCK)
	task.delay(seconds, applyMusicVolume, 1)
end

local lastVariant = 0
local function playVaried(variants: { Sound }, parent: Instance)
	local index = math.random(1, #variants)
	if #variants > 1 and index == lastVariant then
		index = index % #variants + 1 -- never repeat the same variant twice in a row
	end
	lastVariant = index
	local sound = variants[index]:Clone()
	sound.PlaybackSpeed = 2 ^ ((math.random() * 2 - 1) / 12) -- +/-1 semitone
	sound.Volume *= 10 ^ ((math.random() * 4 - 2) / 20) -- +/-2 dB
	sound.Parent = parent
	sound:Play()
	sound.Ended:Once(function()
		sound:Destroy()
	end)
end
```

Cloning per play is fine for low-rate sounds. For high-rate sounds such as gunfire, footsteps in crowds or coin showers, keep a small pool per sound, as described in the Object Pool pattern in 2.12.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/audio-design/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/audio-design/references/adaptive-music.md, Roblox/creator-docs:content/en-us/reference/engine/classes/AudioCompressor.yaml



This file continues Section 2 with 2.7–2.11: game AI, procedural generation, save systems, physics and performance, and genre playbooks.

## 2.7 Game AI

**Fun AI beats smart AI.** Game AI exists to create good play, not to win. Good enemy AI:

- telegraphs its attacks,
- reacts with a short, human-like delay (about 0.2–0.5 s),
- misses sometimes,
- takes turns attacking instead of all at once,
- shows its state clearly (an alert icon, a bark, a change of posture).

A perfectly aimed enemy feels like cheating. A readable enemy feels fair.

**Three layers.** Keep these separate:

1. **Decide:** what to do next. This is the FSM, behaviour tree or utility scorer.
2. **Path:** how to get there through the level. This is A*, a navmesh or a flow field.
3. **Steer:** how to move along the path. This covers seek, arrive, avoid and separation.

**Choosing a decision model.**

| Model | Use when | Strength | Weakness |
|---|---|---|---|
| Finite state machine (FSM) | 2–5 clear states (patrol, chase, attack) | simple, debuggable | transitions explode beyond about 6–8 states |
| Behaviour tree (BT) | many behaviours with clear priorities | modular, reusable subtrees | graded choices are awkward |
| Utility AI | graded choices between many options ("how hungry vs how scared?") | smooth, emergent | harder to predict and tune |
| Hybrid | complex agents | BT for structure, utility inside a selector | more moving parts |

**FSM rules.** Each state has `enter`, `update` and `exit`. Each state owns its own outgoing transitions. Use hierarchical states (a "Combat" parent holding Attack and Reposition) when several states share the same exit conditions.

**Behaviour tree rules.**

- Nodes return Success, Failure or Running.
- A **Sequence** runs its children in order until one fails (logical AND).
- A **Selector** runs its children in order until one succeeds (logical OR).
- **Decorators** wrap one child: Inverter, Cooldown, Repeat, TimeLimit.
- Use reactive selectors that re-check higher-priority branches every tick, with proper Reset or abort of the interrupted Running node.
- Store shared facts on a **blackboard**, such as `target`, `lastSeenPosition` and `health`.

**Utility rules.**

- Each consideration maps an input to a 0–1 score through a curve: linear, quadratic, sigmoid or smoothstep.
- Multiply the considerations, and apply a compensation factor so actions with many considerations are not unfairly punished.
- Add a small hysteresis bonus (about 0.05) to the current action to prevent flip-flopping.
- For variety, pick among the top actions with softmax or weighted random instead of always taking the maximum.

**Cost control.**

- Tick decisions at 5–15 Hz, not every frame. The source example ticks a guard at 10 Hz.
- Time-slice: split agents into buckets and update one bucket per frame.
- Use LOD by distance: far agents tick slowly or freeze.
- Push perception results (seen, heard) onto the blackboard as events, instead of raycasting on every tick.

**Pathfinding rules.**

- A* needs an admissible heuristic (Manhattan on 4-way grids, octile on 8-way). Check for the goal when a node is popped from the open set, not when it is pushed.
- Use flow fields when many agents share one goal (tower defense, zombie hordes). Compute the field once and let all agents follow it.
- Repath on a timer (every 0.5–1 s) or when the path is blocked, never every frame.
- Add a stuck timeout: if an agent has not made progress for about 2 s, repath or teleport it to the next waypoint.

**Shooter enemy loop.** Patrol, then alert (with a reaction delay), then attack (in short bursts), then search the last known position, then back to patrol.

**On Roblox:**

- **PathfindingService.** `PathfindingService:CreatePath(params)` takes `AgentRadius` (default 2), `AgentHeight` (5), `AgentCanJump` (true), `AgentCanClimb` (false; when true, it uses `TrussPart`s and labels the waypoint "Climb"), `WaypointSpacing` (4) and a `Costs` table.
  - `Costs` maps materials or `PathfindingModifier` labels (for example "DangerZone") to a cost multiplier. Use `math.huge` to forbid an area.
  - The docs note that `ComputeAsync` avoids jumps where possible.
  - Listen to `Path.Blocked`, and only repath when the blocked index is at or after the next waypoint you are heading to.
- **Moving the Humanoid.** `Humanoid:MoveTo(position)` walks toward a point. `MoveToFinished` fires with `reached = false` after 8 seconds if the target was not reached. Call `MoveTo` again for long walks, and treat the timeout as "stuck".
- **Server ownership.** Set `rootPart:SetNetworkOwner(nil)` on server-controlled NPCs, so a nearby player's client does not take over their physics. That would make them stutter, and it is exploitable (general knowledge).
- **Cost of many NPCs.** Each `Humanoid` is relatively expensive on the server, because it runs its own state machine and physics. Beyond a few dozen active NPCs, consider other approaches (general knowledge):
  - `AnimationController` models moved by CFrame along precomputed waypoints.
  - Server-side simulation of positions as plain data, with clients rendering and interpolating the visible models.
  - Pooling NPC models (2.12).
  - Distance-based tick rates.
- **Models.** NPC models are Blender characters with simple collision hulls, per the house rules.

A server NPC with a small FSM, a shared 10 Hz tick and time slicing:

```lua
-- Script (server). A small FSM per NPC with a shared, time-sliced 10 Hz tick.
local RunService = game:GetService("RunService")
local PathfindingService = game:GetService("PathfindingService")
local Players = game:GetService("Players")

local TICK, BUCKETS, SIGHT = 0.1, 4, 60
local npcs = {} -- array of { model, humanoid, root, state, target }

local function nearestPlayer(root: BasePart): BasePart?
	local best, bestDist = nil, SIGHT
	for _, player in Players:GetPlayers() do
		local char = player.Character
		local hrp = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
		if hrp then
			local d = (hrp.Position - root.Position).Magnitude
			if d < bestDist then
				best, bestDist = hrp, d
			end
		end
	end
	return best
end

local States = {}
States.Patrol = {
	update = function(npc)
		npc.target = nearestPlayer(npc.root)
		if npc.target then
			return "Chase"
		end
		return nil
	end,
}
States.Chase = {
	enter = function(npc)
		npc.path = PathfindingService:CreatePath({ AgentRadius = 2, AgentHeight = 5, Costs = { DangerZone = math.huge } })
		npc.nextRepath = 0
	end,
	update = function(npc)
		local target = npc.target
		if not target or not target.Parent or (target.Position - npc.root.Position).Magnitude > SIGHT * 1.2 then
			return "Patrol" -- the 1.2 factor is hysteresis, so chase does not flicker at the edge
		end
		if os.clock() >= npc.nextRepath then
			npc.nextRepath = os.clock() + 0.75 -- repath on a timer, never every tick
			local ok = pcall(function()
				npc.path:ComputeAsync(npc.root.Position, target.Position)
			end)
			if ok and npc.path.Status == Enum.PathStatus.Success then
				local waypoints = npc.path:GetWaypoints()
				local nextWaypoint = waypoints[2] or waypoints[1]
				if nextWaypoint.Action == Enum.PathWaypointAction.Jump then
					npc.humanoid.Jump = true
				end
				npc.humanoid:MoveTo(nextWaypoint.Position)
			end
		end
		return nil
	end,
}

local function setState(npc, name: string)
	local old = States[npc.state]
	if old and old.exit then
		old.exit(npc)
	end
	npc.state = name
	local new = States[name]
	if new.enter then
		new.enter(npc)
	end
end

local accumulator, bucket = 0, 0
RunService.Heartbeat:Connect(function(dt)
	accumulator += dt
	if accumulator < TICK / BUCKETS then
		return
	end
	accumulator = 0
	bucket = (bucket + 1) % BUCKETS
	for i = bucket + 1, #npcs, BUCKETS do -- each NPC is ticked about every TICK seconds
		local npc = npcs[i]
		local nextState = States[npc.state].update(npc)
		if nextState then
			setState(npc, nextState)
		end
	end
end)
```

`ComputeAsync` yields. In production, run each NPC's repath in its own `task.spawn` with a "repathing" flag, so one slow path does not stall the bucket. The pcall-inline version above keeps the sketch short.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-ai/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-ai/references/behavior-trees.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/game-ai/references/pathfinding.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/ai-behavior-trees-utility-ai/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/ai-behavior-trees-utility-ai/references/utility-ai-system.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/ai-behavior-trees-utility-ai/references/best-practices-and-pitfalls.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/fps-shooter/SKILL.md, Roblox/creator-docs:content/en-us/characters/pathfinding.md, Roblox/creator-docs:content/en-us/reference/engine/classes/Humanoid.yaml

## 2.8 Procedural generation (design level)

**Rules that prevent most procgen bugs.**

1. **One seeded random generator, passed everywhere.** Never call the global random function inside generation code. The same seed must give the same world.
2. **Generate into data first, then build.** Produce a grid or graph of room data, validate it, and only then spawn models.
3. **Validate connectivity.** Flood fill from the start. If the exit or any required room is unreachable, reject the layout or repair it. Use the reachable-set check from 2.2 for keys and gates.
4. **Cap attempts.** Placement loops ("try up to 100 times to place a room") must have a limit and a fallback.
5. **Seeds are version-fragile.** A library or engine update can change what a seed produces. Ship your own small PRNG for anything players share, such as daily seeds or seed codes. For saved worlds, save the generated results rather than only the seed.

**Terrain from noise.**

- Use fractal Brownian motion (fBm): add several octaves of noise, each at double the frequency (lacunarity 2) and half the amplitude (gain 0.5). Then normalize.
- Redistribute with a power curve (`e^k`) to flatten valleys or sharpen peaks.
- Use separate seeds for elevation and moisture, and pick biomes from a table indexed by both.
- Multiply by an island mask (falling off with distance from the centre) for bounded maps.
- Scatter props with Poisson-disc sampling, so nothing overlaps and spacing looks natural.

**Dungeons.**

| Method | Result |
|---|---|
| Rooms and corridors | Random rooms connected by a minimum spanning tree, plus a few extra edges for loops |
| BSP | Recursively split space, then place one room per leaf. Gives tidy, building-like layouts. |
| Drunkard's walk | Organic caves |
| Cellular automata | Caves. Use the 4-5 rule and double-buffer each step. |
| Wave Function Collapse | Tile-based, rule-constrained layouts |

Adding loops matters. A pure tree layout forces backtracking, which feels bad.

**Loot.**

- Use weighted tables.
- Avoid bad streaks with a "bag" (shuffle a deck of outcomes and draw without replacement) or a pity timer (guarantee a rare drop after N misses).
- Scale loot by depth or level.

**On Roblox:**

- **Random generators.** Use `Random.new(seed)` objects (`rng:NextInteger(a, b)`, `rng:NextNumber()`) and pass them into every generator function. Do not use `math.random` in generation code. Whether `Random`'s output is guaranteed stable across engine versions is not documented in the sources used here. For shareable seeds, save the seed plus a generator version, and keep your own PRNG if exact reproduction matters (general knowledge).
- **Noise.** `math.noise(x, y, z)` gives smooth Perlin-style noise but takes no seed. Offset one coordinate by a seed-derived, non-integer value. It returns 0 at integer lattice points, so scale your inputs by non-integer frequencies.
- **Building from data.** Under the house rules, generated levels are assembled from a kit of Blender modules: room pieces, corridor pieces and props. Each module has `Attachment` sockets that snap together. Primitive Parts are never generated. Terrain is the exception, because `Terrain:FillBlock` and `WriteVoxels` are the engine's own terrain, not Parts. Collision for kit pieces comes from their collision hulls.
- **Server versus client.** Generate on the server, or generate the same seed on every client for cosmetic-only scatter, which saves replication bandwidth.

```lua
-- fBm height with a seed offset (math.noise has no seed parameter).
local function fbm(x: number, z: number, seedOffset: number, octaves: number): number
	local amplitude, frequency, sum, norm = 1, 1 / 64, 0, 0
	for _ = 1, octaves do
		sum += amplitude * math.noise(x * frequency, z * frequency, seedOffset)
		norm += amplitude
		amplitude *= 0.5 -- gain
		frequency *= 2 -- lacunarity
	end
	return sum / norm -- roughly -1..1
end

-- Weighted loot with a pity timer.
local function makeLootRoller(rng: Random, table_: { { item: string, weight: number, rare: boolean? } }, pityAfter: number)
	local total = 0
	for _, entry in table_ do
		total += entry.weight
	end
	local misses = 0
	return function(): string
		if misses >= pityAfter then
			for _, entry in table_ do
				if entry.rare then
					misses = 0
					return entry.item
				end
			end
		end
		local roll = rng:NextNumber() * total
		for _, entry in table_ do
			roll -= entry.weight
			if roll <= 0 then
				misses = if entry.rare then 0 else misses + 1
				return entry.item
			end
		end
		return table_[#table_].item
	end
end
```

If a game sells Luck or Server Luck boosts (house rule product set), apply them as a documented multiplier on rare weights, and show the real odds. Never secretly change odds (general knowledge).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/procedural-gen/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/procedural-gen/references/noise.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/procedural-gen/references/dungeon-generation.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/roguelike/references/generation-fov-loot.md

## 2.9 Save systems (design level)

**Rules.**

1. **Save data, not objects.** Serialize plain tables of numbers, strings and booleans. Never serialize live instances or references.
2. **Version every save.** Store a `version` field. Write one migration function per step (v1 to v2, v2 to v3, and so on) and keep them all forever, because a player may return after a year on version 1.
3. **Validate on load.** Check types and ranges. If the data is corrupt, fall back to a backup, or to defaults with a flag, rather than crashing or wiping progress.
4. **Write atomically.** A save is complete or it did not happen. Never leave half-written state.
5. **Autosave on safe boundaries,** such as after a purchase, at a checkpoint or on leave. Throttle it.
6. **Store authoritative state, recompute derived state.** Save the base stats and the equipped item IDs, not the final damage number. Derived values are recomputed on load (see the Dirty Flag pattern in 2.12).
7. **Separate run state from profile state** in roguelikes. A run can be abandoned. The profile (unlocks, meta-currency) must survive.
8. **Never trust the client's copy** in multiplayer.

**On Roblox** (general knowledge; DataStores are covered in depth by another section):

- Save through `DataStoreService` on the server only. Prefer `UpdateAsync` over `SetAsync` for read-modify-write.
- Use session locking, either through a well-known library such as ProfileStore or your own lock field. This stops two servers from overwriting each other when a player rejoins quickly.
- Save on `Players.PlayerRemoving`, and flush in `game:BindToClose`.
- Keys have a size limit (about 4 MB per key) and request budgets. Keep saves compact and throttle autosaves to every few minutes.
- A purchase receipt (`ProcessReceipt`) must be saved before it returns `PurchaseGranted`, so a crash never loses a paid item.

```lua
-- ModuleScript: SaveMigrations. Each step upgrades exactly one version. Never delete old steps.
local CURRENT = 3
local steps = {
	[1] = function(d) -- v1 to v2: rename gold to coins
		d.coins = d.gold or 0
		d.gold = nil
		return d
	end,
	[2] = function(d) -- v2 to v3: add settings with safe defaults
		d.settings = d.settings or { shake = 0.7, music = 0.8 }
		return d
	end,
}

local function migrate(data)
	data.version = data.version or 1
	while data.version < CURRENT do
		data = steps[data.version](data)
		data.version += 1
	end
	if typeof(data.coins) ~= "number" or data.coins < 0 then
		data.coins = 0 -- validate after migrating
	end
	return data
end

return { migrate = migrate, CURRENT = CURRENT }
```

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/save-systems/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/save-systems/references/versioning-and-migration.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/roguelike/SKILL.md

## 2.10 Physics tuning and performance (brief)

Deep Roblox physics and performance specifics belong to another section. These are the generic rules and their short Roblox translation.

**Physics rules.**

- Simulate on a fixed timestep and interpolate rendering between steps.
- Fast objects tunnel through thin walls. Use continuous collision detection, or cap speed so that `speed / step_rate` is less than the wall thickness.
- Mass does not change fall speed. Gravity does. Tune "heavy feeling" with gravity scale, drag and animation, not mass.
- Keep interacting mass ratios within about 1:10. Extreme ratios make joints and stacks unstable.
- Let resting bodies sleep.
- Use a layer/mask matrix so that only things that should collide can collide.
- Clamp `dt` spikes, for example after a hitch, so one huge step does not launch objects.

**Performance rules.**

- **Profile before optimizing.** At 60 fps the frame budget is 16.67 ms. A rough split is scripts 5 ms, physics 3 ms, rendering 4 ms and UI 2 ms, with the rest as headroom.
- **Decide whether you are CPU-bound or GPU-bound first.** Fixing the wrong one does nothing.
- **"Do less."** Lower the update cadence, use spatial partitioning, LOD, caching, amortizing work across frames, and pooling. Avoid allocations in hot loops, because garbage collection spikes look like random hitches.
- **Mobile budgets.** The skill quotes roughly 5k–20k triangles per character, 1024–2048 px textures and a few hundred draw calls. Remember that phones throttle when hot, so a test at minute 1 is not a test at minute 20.

**On Roblox** (general knowledge unless noted):

- **Physics.**
  - Roblox runs physics on its own internal step. Your scripts read results in `PreSimulation`, `PostSimulation` and `Heartbeat` (event names per the RunService docs).
  - Set network ownership deliberately: the server owns NPCs and shared objects, and each player's client owns their own character.
  - Anchor everything that does not move.
  - Turn off `CanTouch` and `CanQuery` on decorative parts and meshes that do not need them.
  - Pick the cheapest `CollisionFidelity` that still feels solid (`Box` or `Hull` for most Blender props), consistent with the house rule that everything visible is solid.
- **Performance.**
  - Use the MicroProfiler and the Developer Console to find hot spots.
  - Use `StreamingEnabled` for large maps.
  - Reuse Blender `MeshPart`s with the same mesh ID, because shared assets are loaded once (see Flyweight in 2.12).
  - Move many parts at once with `workspace:BulkMoveTo`.
  - Throttle `RemoteEvent` traffic, for example by batching state updates at 10–20 Hz instead of firing every frame.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/physics-tuning/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/physics-tuning/references/timestep-and-ccd.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/performance-optimization/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/performance-optimization/references/profiling-and-budgets.md, Roblox/creator-docs:content/en-us/reference/engine/classes/RunService.yaml

## 2.11 Genre playbooks

Each playbook gives the core loop, the key systems and tuning knobs, the common pitfalls, a Roblox mapping and natural monetization hooks. Every monetization hook must follow the house rules: small, dismissible, well-timed and rate-limited offers, with no fake discounts and no false scarcity.

### 2.11.1 Platformer and obby

**Core loop.** Run, jump, reach the checkpoint, repeat with harder obstacles.

**Feel knobs** (2D-tile terms from the source; the ratios transfer):

- Jump height of 3–4 character heights, reaching the apex in 0.30–0.40 s.
- Fall gravity 1.5–2.0× rise gravity, for a snappy arc.
- Coyote time 0.08–0.12 s and jump buffer 0.10–0.15 s.
- Variable jump: on early release, multiply upward speed by 0.4–0.5.
- Apex hang: half gravity near the top of the jump.
- Ground acceleration reaching full speed in 0.05–0.10 s.
- Corner correction of about 4 px, which nudges the player around ledge corners they barely clip.
- Wall jump at about 0.8× normal jump height, with a 1.25× run-speed sideways kick and 0.10–0.15 s of steering lock.
- Derive physics from the design values: `g = 2h / t²` and `v0 = 2h / t`, where `h` is the jump height and `t` is the time to apex.

**Pitfalls.** Floaty symmetric arcs, no coyote time, unfair hitboxes. Keep player hurtboxes slightly smaller than the visual.

**On Roblox.**

- The default Humanoid jump is a fixed arc. Add a jump buffer and coyote time (2.5). For a snappier fall, apply extra downward force while falling with a `VectorForce` or `LinearVelocity` on the character, created and run on the client because the client owns its character (general knowledge).
- Design gaps from the metrics table in 2.2.
- Obby checkpoints are invisible `SpawnLocation`s inside Blender-built checkpoint pads. Kill zones are Blender models with invisible triggers.
- Save the highest stage reached.

**Monetization.** A "skip stage" developer product, offered only after several failures at the same stage, as a small dismissible button. Convenience passes such as a speed coil or double jump, if they do not break the core challenge. Gift versions of passes. Cosmetic trails (general knowledge).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/platformer/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/platformer/references/feel-tuning.md

### 2.11.2 Tower defense

**Core loop.** Prepare (place and upgrade towers), survive a wave, earn money, repeat.

**Balance.**

- Enemy HP grows about 1.1–1.2× per wave, while income grows roughly linearly. This forces smarter placement rather than just more towers.
- Measure tower value as DPS × time in range, not raw DPS. Range and placement matter as much as damage.
- Offer targeting modes: first, last, closest, strongest, weakest.
- Leaks cost lives and forfeit the bounty.
- Selling refunds about 70%.
- Reward calling waves early with a bonus.
- Always telegraph the next wave's composition.
- Use enemy variety to force tower variety: fast, armoured, flying, swarm, boss.

**Implementation.**

- In maze-building TD, run a BFS before allowing a placement, so the player can never fully block the path.
- Waypoint movement must carry the leftover distance past a waypoint into the next segment. Otherwise fast enemies desync.

**On Roblox.**

- Do not give each enemy a Humanoid. Represent enemies on the server as data: path distance, HP and speed. Clients render pooled Blender models positioned by `CFrame` along the path, interpolating from the server's periodic updates. This scales to hundreds of enemies (general knowledge).
- Tower range checks use `workspace:GetPartBoundsInRadius` with `OverlapParams`, or a plain distance check against the data list, which is cheaper.
- Tower placement is validated on the server, against a grid and a path-clearance check.

**Monetization.** 2× Cash boost (timed), 2× game speed for solo play, unique towers as passes (keep them balanced against free towers), starter pack, gift passes. Show offers between waves, never during a wave.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/tower-defense/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/tower-defense/references/balancing.md

### 2.11.3 Roguelike

**Core loop.** Enter a generated run, fight and loot through floors, die or win, unlock meta-progress, start again.

**Systems.**

- The Berlin Interpretation (random generation, permadeath, turn-based, grid-based) defines the classic form. Roguelites keep the run structure and relax the rest.
- Turn order uses an energy scheduler: each actor gains energy by speed, and acts when it reaches the turn cost (100).
- Field of view uses symmetric shadowcasting, so "if I can see you, you can see me" holds.
- Loot scales with depth.
- Run state and profile state are kept strictly apart (2.9).
- Every floor passes the connectivity check (2.8).

**Pitfalls.** Unwinnable seeds, early deaths with no learning, runs that are too long for the session length.

**On Roblox.**

- Real-time action roguelites fit Roblox sessions better than turn-based ones (general knowledge).
- Assemble rooms from a Blender kit snapped by `Attachment`s (2.8).
- Use one `Random` per run, seeded on the server.
- Party runs share a seed and a run state on the server.
- Keep runs to 10–20 minutes so a discovery player can finish one.

**Monetization.** Revive tokens (cap them per run and price them fairly), cosmetic classes, meta-currency boosts (timed). Luck boosts only if loot rolls exist, with shown odds. Offer after a run ends, not on death mid-fight.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/roguelike/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/roguelike/references/generation-fov-loot.md

### 2.11.4 RPG

**Core loop.** Quest, fight, earn XP and loot, get stronger, take harder quests.

**Stats.**

- Compute final stats in modifier layers: base, then flat bonuses, then percentage bonuses, then clamp.
- Never store derived stats. Recompute them when inputs change (Dirty Flag, 2.12).
- XP curves are often quadratic: `xpToNext = base × level²`.

**Damage.**

- Subtractive: `damage = attack − defense`, floored at a minimum. Simple, but it breaks at high defense.
- Ratio: `damage = attack × K / (K + defense)` with K around 100. This degrades smoothly.
- Add ±10% variance and a 1.5× critical multiplier.

**Quests.**

- State machines: available, active, complete, turned in.
- Objectives listen to gameplay events ("enemy killed", "item collected") through an event bus, rather than polling.
- Dialogue is a data graph of nodes, choices, conditions and variable writes, using string IDs for localization.

**On Roblox.**

- All stats, XP and loot live on the server. Replicate display values with attributes.
- Use `CollectionService` tags for quest givers and enemies.
- Dialogue strings go through `LocalizationTable`s (general knowledge).
- Use `ProximityPrompt` on an invisible anchor part as the talk trigger, which is allowed as a technical helper.

**Monetization.** 2× XP boost (timed), inventory or bank expansion (convenience pass), cosmetic mounts, starter pack, gift passes. Never sell the best gear outright in PvP-relevant RPGs (general knowledge).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/rpg/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/rpg/references/stats-combat-quests.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/dialogue-systems/SKILL.md

### 2.11.5 Survival and crafting

**Core loop.** Gather, craft, build, survive the night or the threat, expand.

**Systems.**

- **Needs** decay at graded rates. Thirst falls faster than hunger, and both cause soft penalties before death.
- **Crafting** is atomic. Check the inputs and inventory space, then consume and produce in one step.
- **Tool tiers** gate resources: stone, then iron, then advanced.
- **Resource nodes** respawn on timers.
- **Recipes** form a tech DAG (a directed graph with no cycles), so progress unlocks visibly.
- **Threat** escalates on a day/night cycle.
- **Saves** are incremental, because the world state is large.

**On Roblox.**

- Resource nodes are tagged Blender models with real collision.
- Crafting and inventory are server-authoritative.
- Base-building uses grid snapping with server-side placement validation (overlap check with `GetPartBoundsInBox`).
- Day/night can drive `Lighting.ClockTime`.
- Save placed structures as compact data, such as an ID, a grid position and a rotation, never as instances.

**Monetization.** 2× gather speed (timed), extra storage (convenience), cosmetic building themes, starter pack. No pay-to-skip raids in PvP.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/survival-crafting/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/survival-crafting/references/needs-and-crafting.md

### 2.11.6 Shooter (FPS and TPS)

**Core loop.** Engage, shoot, reposition, win the round, upgrade or rank up.

**Systems.**

- **Hitscan or projectile.** Hitscan is an instant ray. Projectiles have travel time and drop.
- **Damage falloff.** For example, full damage to 20 m, falling to a 0.4 multiplier floor by 60 m.
- **Headshots** do 1.5–2× damage.
- **Recoil** is a learnable pattern, kept as a separate decaying offset rather than permanently moving the aim.
- **Spread** samples a cone with a square-root distribution, so shots fill the cone evenly.
- **Time to kill:** `TTK = (ceil(hp / damage) − 1) / fire_rate`. Tune weapons by TTK, not damage alone.
- **Authority.** The server is authoritative, with lag compensation.
- **Options.** Offer FOV and sensitivity settings.

**On Roblox.**

- The client raycasts immediately for feel: muzzle flash, tracer and predicted hit marker.
- The server validates each claimed shot (general knowledge):
  - fire rate and ammo,
  - distance and range,
  - line of sight with its own `workspace:Raycast`,
  - plausibility of the hit position against the target's recent positions.
- Never let the client report damage directly.
- Use `Beam`s or pooled tracer meshes for bullets.
- Weapons and props are Blender models.

**Monetization.** Weapon skins and cosmetic packs, a battle-pass style progression (with real, fixed end dates, which are not false scarcity), 2× XP boost, gift passes. No purchasable stat advantages in competitive modes (general knowledge).

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/fps-shooter/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/fps-shooter/references/shooting-and-feel.md

### 2.11.7 Puzzle

**Core loop.** Read the board, make a move, watch it resolve, repeat until the goal or failure.

**Systems.**

- The board model is the single source of truth. Visuals only mirror it.
- Resolution loop: resolve matches, apply gravity, refill, then check for cascades until the board is stable.
- Undo uses snapshots (including the RNG state) or reversible commands (2.12).
- Detect deadlocks (no legal moves) and reshuffle.
- Generated puzzles must be solvable. Build them backwards from a solved state, or check parity for sliding puzzles.
- Lock input while the board is resolving.

**On Roblox.**

- For single-player puzzles, the client can run the board for responsiveness. The server validates the completion and any rewards, for example by replaying the move list (the Command pattern).
- Puzzle pieces are Blender models, and they are pooled.

**Monetization.** Hint packs, extra moves (offered once per failed level, dismissible), cosmetic boards, starter pack.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/puzzle/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/puzzle/references/board-and-resolution.md

### 2.11.8 Card game

**Core loop.** Draw, play cards with a limited resource (mana), resolve effects, end the turn.

**Systems.**

- Every card lives in exactly one zone at a time: deck, hand, board or discard. Moves are atomic transfers.
- When the deck is empty, draw reshuffles the discard pile.
- Effects are data operations ("deal 3", "draw 1") resolved through a stack (LIFO, for responses) or a queue (FIFO).
- Triggers ("when a creature dies") subscribe through an event bus.
- Playing a card is atomic: pay, move and resolve, or roll back.
- Shuffle with Fisher–Yates, using a seeded per-deck RNG.
- Balance the mana curve.

**On Roblox.**

- The server owns every deck and hand.
- Never replicate hidden information. Anything in `ReplicatedStorage`, in attributes or in a `RemoteEvent` payload is visible to exploiters. Send each client only its own hand and the public board (general knowledge).

**Monetization.** Cosmetic card backs and boards, a starter deck pack, gift packs. If packs are random, show the odds and keep the pity rules honest.

```lua
-- Seeded Fisher–Yates shuffle (server).
local function shuffle(deck: { any }, rng: Random)
	for i = #deck, 2, -1 do
		local j = rng:NextInteger(1, i)
		deck[i], deck[j] = deck[j], deck[i]
	end
end
```

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/card-game/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/card-game/references/effect-resolution.md

### 2.11.9 Visual novel and story games

**Core loop.** Read, choose, see the consequence, reach one of several endings.

**Systems.**

- Save anywhere. Store the exact script position, all flags and the set of read lines.
- Text appears with a typewriter effect based on the visible character count, not substring slicing.
- Skip only text the player has already read.
- Keep a backlog of past lines.
- Structure the story as branch and merge, which keeps content cost manageable.
- Authoring tools: Ink, Yarn Spinner, or a small data-graph runner. Do not invent a scripting language.

**On Roblox.**

- `TextLabel.MaxVisibleGraphemes` gives a typewriter effect without slicing strings (general knowledge, version-sensitive).
- Story flags are saved on the server.
- In multiplayer, decide early whether choices are per-player or group votes.

**Monetization.** Chapter or route passes, cosmetic outfits, gift passes.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/visual-novel/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/genres/visual-novel/references/script-and-flow.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/dialogue-systems/SKILL.md

### 2.11.10 Roblox-native genres (general knowledge)

These genres are not covered by the source skills. The notes come from general knowledge of the Roblox platform. Check them against the market-research sections of this knowledge base.

- **Simulator.**
  - Loop: click or collect, sell, upgrade capacity, unlock the next zone, rebirth.
  - Key knobs: the exponential price curve (prices grow about 1.15–1.5× per tier), zone gates, and the rebirth multiplier.
  - Pitfall: the numbers outgrow meaning. Use readable suffixes (K, M, B) and new verbs per zone.
  - Monetization fits naturally: 2× Cash, 2× speed, auto-collect pass, Luck boosts for egg or pet hatching (with shown odds), extra pet slots, starter pack.
- **Tycoon.**
  - Loop: claim a plot, buy droppers or machines, collect income, buy the next button, expand.
  - Design the button order as a pacing graph (2.2), with a visible "next purchase" target at all times.
  - Every purchasable building is a Blender model that appears with a juicy build-in animation (2.1).
  - Monetization: 2× Cash, auto-collect, VIP area, gift passes.
- **Social hangout.**
  - Loop: arrive, express yourself, meet people, do light shared activities, return.
  - Keys: dense but uncrowded spaces, many sit and pose spots, emotes, light minigames, and rotating events (with real end dates).
  - Monetization: cosmetics, emotes, house or room expansions.
- **Horror.**
  - Loop: explore, sense the threat, hide or run, escape.
  - Audio and lighting carry the genre (2.6). Use a tension graph with long quiet build-ups.
  - The AI should telegraph and miss (2.7). Use "fun AI" stalking with a director that controls the pacing.
  - Keep jump scares rare. Respect flash and shake accessibility options.
  - Monetization: revives, cosmetic flashlights, extra lives in party modes. Never shown during a chase.
- **Roleplay.**
  - Loop: choose a role, use tools and places to act out stories with others.
  - Keys: many interactable Blender props (doors, vehicles, jobs), clear zones, and roles that create interaction (police and civilians, staff and customers).
  - Monetization: premium roles or vehicles as convenience passes, houses, cosmetics, gift passes.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/genres/README.md (genre coverage only; the content above is general knowledge)



This file finishes Section 2 with 2.12 (every chapter of *Game Programming Patterns*, mapped to Roblox and Luau), 2.13 (prototyping and jam workflow) and a short Further reading list.

## 2.12 Architecture patterns: Game Programming Patterns on Roblox

Robert Nystrom's *Game Programming Patterns* has 19 pattern chapters, in six groups:

- **Design Patterns Revisited:** Command, Flyweight, Observer, Prototype, Singleton, State.
- **Sequencing:** Double Buffer, Game Loop, Update Method.
- **Behavioral:** Bytecode, Subclass Sandbox, Type Object.
- **Decoupling:** Component, Event Queue, Service Locator.
- **Optimization:** Data Locality, Dirty Flag, Object Pool, Spatial Partition.

The book's own warning applies to all of them. Every pattern trades simplicity for flexibility or speed. Add one when the problem it solves is actually present, not in advance.

Each entry below gives a summary, when to use it, the pitfalls, and a Roblox mapping with a short Luau sketch. The Roblox mappings are the author's translation (general knowledge) unless a Roblox doc is cited.

### Command

**Summary.** A command is a method call turned into an object. You can store it, queue it, send it, log it and undo it. The book's uses are configurable input (a button maps to a command object), commands that work on any actor (the same "jump" command drives the player or an AI), and undo/redo (each command knows how to reverse itself).

**When to use.** Rebindable input, AI and player sharing one action vocabulary, undo in building games and editors, replays, and networked intent.

**Pitfalls.** Undo needs commands to capture the state they change. Long undo histories cost memory, so cap them.

**On Roblox.** Command is the natural shape of client-to-server traffic. The client sends a named command with arguments, which is intent. The server validates the command and executes it. Tycoon and building games get undo for free by storing each executed command's reverse. Replays and puzzle validation (2.11.7) replay the command list.

```lua
-- Server. Commands are a whitelist of validated, undoable actions.
local Commands = {}
Commands.PlaceProp = {
	validate = function(player: Player, args): boolean
		return typeof(args.propId) == "string" and typeof(args.cell) == "Vector3"
	end,
	execute = function(player: Player, args): () -> ()
		local prop = placeProp(player, args.propId, args.cell) -- your placement function
		return function()
			prop:Destroy() -- the undo closure captures what it needs
		end
	end,
}

local history: { [Player]: { () -> () } } = {}
remote.OnServerEvent:Connect(function(player, name, args)
	if typeof(name) ~= "string" or typeof(args) ~= "table" then
		return
	end
	local command = Commands[name]
	if not command or not command.validate(player, args) then
		return
	end
	local list = history[player] or {}
	history[player] = list
	table.insert(list, command.execute(player, args))
	if #list > 50 then
		table.remove(list, 1) -- cap the undo history
	end
end)
```

Clear `history[player]` on `PlayerRemoving`, or the table leaks.

### Flyweight

**Summary.** Split an object's data into intrinsic state, which is shared and identical for every copy (a tree's mesh, texture and stats), and extrinsic state, which is unique per instance (position, scale, health). Store the intrinsic state once and reference it. The book's examples are forests (one tree model drawn thousands of times) and terrain tiles (each tile points at a shared terrain type object instead of storing its own properties).

**When to use.** Many objects share most of their data.

**Pitfalls.** Shared data must be treated as read-only. Mutating it changes every instance.

**On Roblox.**

- Blender `MeshPart`s that use the same mesh and texture asset IDs are shared assets. The client downloads and stores the mesh once, however many copies exist (general knowledge).
- Packages keep one source model for many placed copies.
- For gameplay data, keep per-type stats in one ModuleScript table, and store only per-instance values as attributes.

```lua
-- ModuleScript: TreeTypes. Intrinsic, shared, read-only.
return table.freeze({
	Oak = table.freeze({ wood = 5, regrowSeconds = 60, model = "Oak_LOD0" }),
	Pine = table.freeze({ wood = 3, regrowSeconds = 40, model = "Pine_LOD0" }),
})
-- Each placed tree stores only extrinsic state: tree:SetAttribute("Type", "Oak"), plus its own health.
```

### Observer

**Summary.** A subject keeps a list of observers and notifies them when something happens. The book's example is an achievement system that listens to physics events, so the physics code never knows that achievements exist. The book's warnings:

- Notification is synchronous, so a slow observer blocks the subject. "Stay off the UI thread."
- The lapsed listener problem: observers that are never unregistered keep dead objects alive and keep receiving events. Be disciplined about unregistering.
- Observers make the flow hard to follow when you need to reason about both sides together. They work best between unrelated "lumps" of code.

**When to use.** One system needs to react to another without the two depending on each other. Examples: achievements, quests, UI updates, analytics.

**On Roblox.**

- Engine events (`Changed`, `GetAttributeChangedSignal`, `Touched`) are observers.
- For your own events, use a small Signal module. `BindableEvent` also works, but its arguments are copied, so tables lose their metatables and identity (general knowledge).
- Destroying an Instance disconnects its own events. Connections to other objects must be stored and disconnected, often with a "maid" or "trove" cleanup helper.

```lua
-- ModuleScript: Signal. Handlers run in their own threads, so one error cannot break the others.
local Signal = {}
Signal.__index = Signal

function Signal.new()
	return setmetatable({ _handlers = {} }, Signal)
end

function Signal:Connect(handler: (...any) -> ())
	local handlers = self._handlers
	table.insert(handlers, handler)
	return {
		Disconnect = function()
			local index = table.find(handlers, handler)
			if index then
				table.remove(handlers, index)
			end
		end,
	}
end

function Signal:Fire(...)
	for _, handler in table.clone(self._handlers) do -- clone so handlers may disconnect while firing
		task.spawn(handler, ...)
	end
end

return Signal
```

### Prototype

**Summary.** Make new objects by cloning an existing prototype instead of calling a class constructor. The book covers spawners that clone a prototype monster, spawn functions, and, most usefully, prototypes for data modelling. A data entry can name a parent entry and inherit its fields, overriding only what differs. The book uses this to keep data files small.

**When to use.** Spawners, variants of a base object, and data files with many near-duplicate entries.

**Pitfalls.** Deep versus shallow copies. A clone that shares a nested table with its prototype will mutate the prototype.

**On Roblox.** `Instance:Clone()` is the Prototype pattern. Keep templates, which are Blender models with their collision set up, in `ServerStorage` or `ReplicatedStorage`, and clone them. For data, use metatable delegation, or copy the parent's fields down at load time (see Type Object below).

```lua
local ServerStorage = game:GetService("ServerStorage")
local function makeSpawner(template: Model, parent: Instance)
	return function(cframe: CFrame): Model
		local copy = template:Clone()
		copy:PivotTo(cframe)
		copy.Parent = parent
		return copy
	end
end
local spawnGoblin = makeSpawner(ServerStorage.Enemies.Goblin, workspace.Enemies)
```

### Singleton

**Summary.** One instance with global access. The book argues against it in most cases:

- It is a global variable in disguise.
- It hides coupling.
- It complicates concurrency.
- Lazy initialization can happen at a bad moment.

Its alternatives: pass the object to whoever needs it, get it from a base class, get it from an existing object, or use a Service Locator.

**When to use.** Rarely. Use it when there is truly one of something and passing it around would be absurd.

**On Roblox.** A `ModuleScript` is cached after the first `require`, so every module is effectively a singleton per Luau environment: one on the server and one per client. Each Actor has its own environment, so it gets its own copy (general knowledge). The pitfalls are hidden dependencies, circular requires (which error) and unclear start-up order. A common fix is explicit lifecycle methods: every service module exposes `Init` (set up internal state, no cross-calls) and `Start` (may call other services). A single bootstrap script requires all of them, calls every `Init`, and then calls every `Start`.

### State

**Summary.** Behaviour depends on the current state, so put each state's behaviour in its own place instead of tangled flags. The book progresses from an enum with a switch statement, to state objects (shared static instances, or instantiated per object when they hold data), to enter and exit actions. It then covers:

- concurrent machines (two FSMs side by side, such as movement and equipment),
- hierarchical machines (sub-states inherit from a parent state),
- pushdown automata (a stack of states, so you can return to the previous one).

FSMs suit AI, input handling, menus and network protocols. The book notes that game AI has moved toward behaviour trees and planners for complex agents.

**When to use.** An object behaves very differently in a few clearly separated modes.

**Pitfalls.** State explosion. Boolean flags such as `isJumping`, `isDucking` and `isAttacking` multiply into impossible combinations. Replace them with one state variable.

**On Roblox.** For an NPC FSM, see 2.7. `Humanoid` itself is an engine FSM (`HumanoidStateType`). Use a pushdown automaton for the menu or screen stack:

```lua
local stack = {}
local function push(screen)
	local top = stack[#stack]
	if top then
		top:pause() -- hide but keep state
	end
	table.insert(stack, screen)
	screen:enter()
end
local function pop()
	local top = table.remove(stack)
	if top then
		top:exit()
	end
	local below = stack[#stack]
	if below then
		below:resume() -- Back always returns to exactly where you were
	end
end
```

### Double Buffer

**Summary.** Keep two copies of some state. Readers see the current buffer while writers build the next one. Then swap them in a single atomic step. Use it when state is modified incrementally but must be read as a consistent whole in the middle of modification. The book's non-graphics example is "buffered slaps": actors that react to being slapped this frame must all see last frame's slaps, otherwise the result depends on update order. The costs are memory for two buffers, plus the swap itself, which must be atomic.

**When to use.**

- Cellular automata.
- Simultaneous AI decisions.
- Any simulation where update order must not change the result.

**On Roblox.**

```lua
-- Cave cellular automaton, step with a double buffer (the 4-5 rule).
local W, H = 64, 64
local current, nextGrid = table.create(W * H, 0), table.create(W * H, 0)

local function wallNeighbours(grid, x, y): number
	local count = 0
	for dy = -1, 1 do
		for dx = -1, 1 do
			if dx ~= 0 or dy ~= 0 then
				local nx, ny = x + dx, y + dy
				if nx < 1 or ny < 1 or nx > W or ny > H or grid[(ny - 1) * W + nx] == 1 then
					count += 1 -- out of bounds counts as wall
				end
			end
		end
	end
	return count
end

local function step()
	for y = 1, H do
		for x = 1, W do
			local i = (y - 1) * W + x
			local n = wallNeighbours(current, x, y) -- read only the current buffer
			nextGrid[i] = if n >= 5 or (current[i] == 1 and n >= 4) then 1 else 0
		end
	end
	current, nextGrid = nextGrid, current -- the swap
end
```

### Game Loop

**Summary.** The loop processes input, updates the game and renders, decoupling game time from processor speed. The book compares the options. A fixed update step with variable rendering, plus interpolation, is the robust default. A pure variable timestep is discouraged, because it makes physics and networking nondeterministic. On battery devices, clamp the frame rate to save power. On most platforms the engine owns the loop.

**When to use.** You rarely write it yourself. Use a fixed-step accumulator inside the engine's loop when you need deterministic simulation.

**On Roblox.** Roblox owns the loop and exposes it through `RunService` events. Use `Heartbeat` (after physics, on both server and client) for most game logic, `PreSimulation` for things that must happen before physics, and `PreRender` or `BindToRenderStep` on the client for camera and visual work. If the logic must be deterministic, such as a tower-defense wave simulation or a lockstep minigame, run your own fixed step inside `Heartbeat`:

```lua
local RunService = game:GetService("RunService")
local STEP = 1 / 20 -- simulation rate: 20 Hz
local accumulator = 0

RunService.Heartbeat:Connect(function(dt)
	accumulator += math.min(dt, 0.25) -- clamp hitches to avoid a "spiral of death"
	while accumulator >= STEP do
		simulate(STEP) -- your deterministic update
		accumulator -= STEP
	end
	render(accumulator / STEP) -- interpolation factor 0..1 for visuals
end)
```

### Update Method

**Summary.** Each game object has an `update(dt)` method, and the game calls it on every active object once per frame. The book's cautions:

- Objects update one at a time, so order matters. An object may see some neighbours already updated this frame and others not.
- Objects must store whatever state they need to resume next frame.
- Adding or removing objects during the update pass needs care. Cache the count so new objects wait until next frame, and mark removed objects dead, then sweep them after the pass.
- Keep dormant objects out of the active list.
- The update can live on the entity, on its components or on a delegate.

**When to use.** Many independent objects that each need a little behaviour every frame.

**On Roblox.** You can connect `Heartbeat` separately in every object, but one central loop gives you control over order, safe removal and a single place to profile.

```lua
local RunService = game:GetService("RunService")
local active = {}

local function add(object)
	table.insert(active, object)
end

RunService.Heartbeat:Connect(function(dt)
	local count = #active -- objects added during this pass start next frame
	for i = 1, count do
		local object = active[i]
		if not object.dead then
			object:update(dt)
		end
	end
	local keep = 0 -- sweep dead objects after the pass, preserving order
	for i = 1, #active do
		local object = active[i]
		if not object.dead then
			keep += 1
			active[keep] = object
		end
	end
	for i = #active, keep + 1, -1 do
		active[i] = nil
	end
end)
```

### Bytecode

**Summary.** Encode behaviour as data, as instructions for a small virtual machine, so designers or modders can author behaviour safely without touching engine code. The book calls it the most complex pattern in the book. Its warnings:

- Keep the language's scope on a leash, or it becomes a full programming language.
- You will need a front end (an authoring tool or compiler).
- You lose your debugger.

It recommends a stack-based VM for simplicity.

**When to use.** Large amounts of designer-authored or user-authored behaviour that must be sandboxed. The usual examples are spells, card effects and mod content.

**On Roblox.** `loadstring` is disabled by default, through `ServerScriptService.LoadStringEnabled`, and enabling it to run untrusted text is a serious security risk (general knowledge). Use a small data interpreter instead. For most games, a flat list of whitelisted operations is enough. A full stack VM is rarely needed.

```lua
-- Abilities and card effects as data programs over whitelisted operations.
local Ops = {
	damage = function(ctx, amount: number)
		ctx.target:TakeDamage(amount)
	end,
	heal = function(ctx, amount: number)
		ctx.caster.Health = math.min(ctx.caster.MaxHealth, ctx.caster.Health + amount)
	end,
	effect = function(ctx, name: string)
		ctx.playEffect(name, ctx.target)
	end,
}

local function run(program: { { any } }, ctx)
	for _, instruction in program do
		local op = Ops[instruction[1]]
		assert(op, "unknown op " .. tostring(instruction[1]))
		op(ctx, table.unpack(instruction, 2))
	end
end

-- Data, not code: { { "damage", 12 }, { "effect", "Burn" }, { "heal", 3 } }
```

### Subclass Sandbox

**Summary.** A base class provides a set of protected operations. Each subclass implements one sandbox method, such as `activate`, using only those operations. The base class becomes the single place where subclasses touch the engine, which keeps them decoupled from the rest of the code. The risk is the brittle base class problem: the base class grows huge, and every change to it ripples into every subclass.

**When to use.** Many small variations (superpowers, abilities, interactables) that all need the same handful of engine services.

**On Roblox.**

```lua
-- ModuleScript: Ability. A base class with protected helpers.
local Ability = {}
Ability.__index = Ability

function Ability.new(owner: Player)
	return setmetatable({ owner = owner }, Ability)
end
-- Protected operations: the only way subclasses touch the world.
function Ability:playSound(name: string) --[[ play a sound through the shared mixer ]] end
function Ability:spawnEffect(name: string, at: CFrame) --[[ take an effect from the pool ]] end
function Ability:dealDamage(target: Humanoid, amount: number) --[[ validate, then apply ]] end
function Ability:activate()
	error("subclass must implement activate")
end

-- A subclass, in another module.
local Dash = setmetatable({}, { __index = Ability })
Dash.__index = Dash
function Dash.new(owner)
	return setmetatable(Ability.new(owner), Dash)
end
function Dash:activate()
	self:playSound("Whoosh")
	self:spawnEffect("DashTrail", self.owner.Character:GetPivot())
end
```

### Type Object

**Summary.** Instead of a class per kind of monster, make one `Monster` class plus a `Breed` object that holds the kind's data. Breeds become data, so designers can add kinds without code. Breeds can inherit from a parent breed. The book's example is a Troll (health 25, attack "The troll hits you!"), with a Troll Archer and a Troll Wizard that inherit from it and override the attack text. Copying the parent's values down at load time makes lookups fast. The pitfalls:

- You must manage type objects yourself; the language will not track them.
- Per-breed behaviour is harder than data. Pick from a fixed set of functions, or use Bytecode.

**When to use.** Many kinds of things that differ mostly in data: enemies, items, towers, pets.

**On Roblox.**

```lua
-- ModuleScript: Breeds. Data with parent inheritance, resolved once at load.
local raw = {
	Troll = { health = 25, attack = "The troll hits you!", model = "Troll" },
	TrollArcher = { parent = "Troll", attack = "The troll archer fires an arrow!" },
	TrollWizard = { parent = "Troll", attack = "The troll wizard casts a spell on you!" },
}

local resolved = {}
local function resolve(name: string)
	if resolved[name] then
		return resolved[name]
	end
	local entry = raw[name]
	local result = if entry.parent then table.clone(resolve(entry.parent)) else {}
	for key, value in entry do
		if key ~= "parent" then
			result[key] = value -- copy down, overriding the parent's value
		end
	end
	resolved[name] = table.freeze(result)
	return resolved[name]
end

for name in raw do
	resolve(name)
end
return resolved
```

### Component

**Summary.** A single entity spans several domains (physics, rendering, AI, sound). Instead of one giant class, split the entity into components, one per domain. The entity becomes a container. Components communicate by:

- modifying shared state on the container,
- holding direct references to each other,
- sending messages through the container.

Each option trades coupling for convenience.

**When to use.** Entities mix and match capabilities. Your class hierarchy is fighting you, for example a "flying, burning, collectable" object.

**On Roblox.**

- **CollectionService tags** are the lightweight form. Tag a Blender model "Spinner", "Collectable" or "Damaging", and one script per tag attaches behaviour to every tagged instance, including ones that stream in or spawn later.
- **An ECS such as jecs** (Ukendio/jecs, version 0.11.0 in the cloned repo) is the heavy form. It stores components in archetype tables, iterates with fast queries and supports entity relationships. Its README claims 800,000 entities at 60 fps. That is a benchmark claim, so measure it on your own workload. An ECS pays off with thousands of simulated entities, such as TD enemies, projectiles or crowds. It is overkill for a few dozen.

```lua
-- Tag-based component: each tagged instance gets behaviour and cleanup.
local CollectionService = game:GetService("CollectionService")
local cleanups: { [Instance]: () -> () } = {}

local function attachSpinner(model: Model): () -> ()
	local connection = game:GetService("RunService").Heartbeat:Connect(function(dt)
		model:PivotTo(model:GetPivot() * CFrame.Angles(0, dt * 2, 0))
	end)
	return function()
		connection:Disconnect()
	end
end

local function onAdded(instance: Instance)
	if instance:IsA("Model") then
		cleanups[instance] = attachSpinner(instance)
	end
end
local function onRemoved(instance: Instance)
	local cleanup = cleanups[instance]
	if cleanup then
		cleanup()
		cleanups[instance] = nil
	end
end

CollectionService:GetInstanceAddedSignal("Spinner"):Connect(onAdded)
CollectionService:GetInstanceRemovedSignal("Spinner"):Connect(onRemoved)
for _, instance in CollectionService:GetTagged("Spinner") do
	onAdded(instance)
end
```

```lua
-- jecs (API as shown in the repo's how_to examples for v0.11; check the current version).
local jecs = require(path.to.jecs)
local world = jecs.world()
local Position = world:component() :: jecs.Id<Vector3>
local Velocity = world:component() :: jecs.Id<Vector3>

local e = world:entity()
world:set(e, Position, Vector3.zero)
world:set(e, Velocity, Vector3.new(0, 0, 10))

local function movementSystem(dt: number)
	for entity, position, velocity in world:query(Position, Velocity) do
		world:set(entity, Position, position + velocity * dt)
	end
end
```

### Event Queue

**Summary.** Decouple when an event is sent from when it is processed. Senders push events into a queue, and a receiver drains it later. The book's example is an audio system that queues "play sound" requests, so game code never blocks on audio and duplicate requests in one frame can be merged. The warnings:

- A central queue is a global, with all the dangers of one.
- The world may change between sending and processing, so events must carry all the data they need, not references that may be stale.
- Feedback loops happen when handling an event sends new events. Do not send while handling, or defer the new events to the next frame.

A ring buffer gives a fixed-size, allocation-free queue.

**When to use.** Bursty event producers, work that should happen at a controlled time, merging duplicate requests, and cross-thread handoff.

**On Roblox.**

- `RemoteEvent`s are already queued between client and server.
- `workspace.SignalBehavior` can make engine signals deferred, so handlers run later in the frame instead of immediately. Roblox has moved new places toward `Deferred`. Check the current default in your place (general knowledge, version-sensitive).
- For gameplay, drain your own queue once per `Heartbeat` and aggregate duplicates.

```lua
-- Sound request queue with per-frame aggregation (client).
local RunService = game:GetService("RunService")
local pending: { [string]: { position: Vector3, count: number } } = {}

local function requestSound(name: string, position: Vector3)
	local request = pending[name]
	if request then
		request.count += 1 -- merge: 20 coin pickups this frame play one louder sound
	else
		pending[name] = { position = position, count = 1 }
	end
end

RunService.Heartbeat:Connect(function()
	local batch = pending
	pending = {} -- requests made while handling go to next frame, which prevents feedback loops
	for name, request in batch do
		playAt(name, request.position, math.min(1, 0.5 + 0.1 * request.count)) -- your playback function
	end
end)
```

### Service Locator

**Summary.** Provide global access to a service through a locator, without coupling callers to the concrete class that implements it. Use it sparingly, and prefer passing objects explicitly. Two useful tricks from the book:

- **Null service:** register a do-nothing implementation by default, so callers never get nil.
- **Decorated service:** wrap the real service in a logging version for debugging.

**When to use.** Cross-cutting services such as audio, analytics, logging and settings, where passing a reference through every layer would be noise.

**On Roblox.**

```lua
-- ModuleScript: Services. A registry with null defaults.
local Services = {}
local registry = {}

local NullAnalytics = { track = function(_self, _event: string, _data: any) end }
registry.Analytics = NullAnalytics

function Services.provide(name: string, implementation)
	registry[name] = implementation
end
function Services.get(name: string)
	return registry[name] or error("no service registered: " .. name)
end

return Services
-- In tests or Studio play you can provide a logging decorator:
-- Services.provide("Analytics", { track = function(_, e, d) print("[analytics]", e, d) end })
```

### Data Locality

**Summary.** Modern CPUs are much faster than memory, so arrange data in the order you process it. The book's techniques:

- contiguous arrays of components instead of pointers to scattered objects,
- packed arrays that keep active objects together,
- hot/cold splitting, which separates frequently used fields from rarely used ones.

Apply this only when profiling shows cache misses are the problem. It complicates code.

**When to use.** Hot loops over thousands of entities, after profiling.

**On Roblox.** Luau tables are not raw C structs, so the gains are smaller and less predictable than in C++ (general knowledge). The useful versions are:

- parallel arrays (`positions[i]`, `speeds[i]`) instead of arrays of tables for large simulations,
- an archetype ECS such as jecs, which does this for you,
- the `buffer` type for compact binary data such as network packets and saves,
- Parallel Luau Actors for splitting independent work across cores.

Profile with the MicroProfiler before and after any change.

### Dirty Flag

**Summary.** Keep derived data cached and mark it "dirty" when its inputs change. Recompute it only when it is next needed. The book's example is world transforms in a scene graph. The book is specific about when the pattern is worth it:

- the primary data changes more often than the derived data is used,
- and the derived data is expensive to compute, and hard to update incrementally (if incremental updates are easy, keep a running total instead).

Set the flag on every change. Missing one place causes stale-data bugs. Deferring work also has a cost: a big recomputation can land at an awkward moment.

**When to use.** RPG stats computed from many equipment and buff modifiers. Inventory weight. Pathfinding graphs after building changes.

**On Roblox.**

```lua
-- Cached final stats, recomputed only when equipment or buffs change (server).
local Stats = {}
Stats.__index = Stats

function Stats.new(base: { [string]: number })
	return setmetatable({ base = base, modifiers = {}, dirty = true, cache = {} }, Stats)
end

function Stats:addModifier(stat: string, flat: number, percent: number)
	table.insert(self.modifiers, { stat = stat, flat = flat, percent = percent })
	self.dirty = true -- every write path must set the flag
end

function Stats:get(stat: string): number
	if self.dirty then
		local flat, percent = {}, {}
		for _, m in self.modifiers do
			flat[m.stat] = (flat[m.stat] or 0) + m.flat
			percent[m.stat] = (percent[m.stat] or 0) + m.percent
		end
		for name, value in self.base do -- layers: base, then flat, then percent, then clamp (2.11.4)
			self.cache[name] = math.max(0, (value + (flat[name] or 0)) * (1 + (percent[name] or 0)))
		end
		self.dirty = false
	end
	return self.cache[stat] or 0
end
```

### Object Pool

**Summary.** Pre-allocate a fixed set of reusable objects and recycle them, instead of creating and destroying objects constantly. This avoids allocation cost and memory fragmentation. When the pool is empty, choose an overflow policy:

- prevent the creation,
- skip the request,
- kill the oldest or quietest existing object,
- grow the pool.

Reset every reused object fully, because leftover state from its last use is a classic bug. A free list makes finding an available object O(1).

**When to use.** Frequent spawn and despawn: projectiles, particles, damage numbers, enemies, pickups, sounds.

**On Roblox.** Creating and destroying Instances (especially Blender `MeshPart`s and models) has a real cost, both on the server and in replication. Pool them. Parking a pooled object far away, by `CFrame`, is usually cheaper than reparenting it (general knowledge). Use `workspace:BulkMoveTo` to move many pooled parts in one call.

```lua
-- Pool of Blender projectile meshes (client-side visuals).
local HIDDEN = CFrame.new(0, -10000, 0)
local Pool = {}
Pool.__index = Pool

function Pool.new(template: BasePart, size: number, folder: Instance)
	local self = setmetatable({ free = table.create(size), template = template }, Pool)
	for i = 1, size do
		local part = template:Clone()
		part.Anchored = true
		part.CanCollide = false -- visual-only copies; gameplay collision is decided on the server
		part.CFrame = HIDDEN
		part.Parent = folder
		self.free[i] = part
	end
	return self
end

function Pool:get(cframe: CFrame): BasePart?
	local part = table.remove(self.free)
	if not part then
		return nil -- overflow policy: skip. Alternatives: steal the oldest, or grow.
	end
	part.CFrame = cframe
	part.Transparency = self.template.Transparency -- reset reused state
	return part
end

function Pool:release(part: BasePart)
	part.CFrame = HIDDEN
	table.insert(self.free, part)
end
```

These pooled projectiles are short-lived, non-colliding visuals. The solid-collision house rule applies to world objects that players can touch, and the server still decides every hit.

### Spatial Partition

**Summary.** Store objects in a structure organized by position, so "what is near here?" queries avoid checking every object against every other, which is O(n²). The book contrasts:

- flat structures (a fixed grid) with hierarchical ones (quadtree, BSP, k-d tree),
- partitions that do not depend on the objects (a grid) with partitions that adapt to them (a quadtree that splits where objects cluster).

A grid is simple and great when objects are evenly spread.

**When to use.** Proximity queries, collision broad-phase, and AI perception with many entities.

**On Roblox.** The engine already partitions parts. `workspace:GetPartBoundsInBox`, `GetPartBoundsInRadius` and `GetPartsInPart`, with `OverlapParams`, plus `workspace:Raycast` with `RaycastParams`, use its acceleration structures. Use them for part-based queries. For data-only entities, such as TD enemies stored as data or ECS entities, build a simple grid hash.

```lua
-- Engine query: enemies within a tower's range.
local params = OverlapParams.new()
params.FilterType = Enum.RaycastFilterType.Include
params.FilterDescendantsInstances = { workspace.Enemies }
local hits = workspace:GetPartBoundsInRadius(tower:GetPivot().Position, 24, params)

-- Data-only grid hash.
local CELL = 16
local grid: { [Vector3]: { any } } = {}
local function cellOf(position: Vector3): Vector3
	return Vector3.new(math.floor(position.X / CELL), 0, math.floor(position.Z / CELL))
end
local function insert(entity, position: Vector3)
	local key = cellOf(position)
	local bucket = grid[key] or {}
	grid[key] = bucket
	table.insert(bucket, entity)
end
local function nearby(position: Vector3): { any }
	local center, found = cellOf(position), {}
	for dx = -1, 1 do
		for dz = -1, 1 do
			for _, entity in grid[center + Vector3.new(dx, 0, dz)] or {} do
				table.insert(found, entity)
			end
		end
	end
	return found
end
```

`Vector3` values compare and hash by value in Luau, so they work as table keys (general knowledge). Rebuild the grid each tick, or move entities between buckets when their cell changes.

### Quick mapping table

| Pattern | Roblox and Luau form |
|---|---|
| Command | Remote intents validated on the server; undo closures; replay lists |
| Flyweight | Shared mesh and texture asset IDs, Packages, frozen per-type data tables |
| Observer | Signal module, engine events, `BindableEvent` (copies its arguments) |
| Prototype | `Instance:Clone()` of templates; data delegation |
| Singleton | ModuleScript caching per environment; an Init/Start bootstrap |
| State | NPC FSM, `HumanoidStateType`, a pushdown screen stack |
| Double Buffer | Two grids swapped each step |
| Game Loop | `RunService` events plus a fixed-step accumulator |
| Update Method | One central `Heartbeat` list with a dead-sweep |
| Bytecode | Whitelisted data ops. `loadstring` stays disabled. |
| Subclass Sandbox | A base module with protected helper methods |
| Type Object | Breed data with resolved parent inheritance |
| Component | CollectionService tags, or the jecs ECS |
| Event Queue | Per-frame drained queue, `SignalBehavior.Deferred`, remotes |
| Service Locator | A registry module with null services |
| Data Locality | Parallel arrays, an ECS, `buffer`, Actors, only after profiling |
| Dirty Flag | Cached computed stats |
| Object Pool | Reused parts, models, effects and sounds; `BulkMoveTo` |
| Spatial Partition | `GetPartBoundsInBox`/`Radius` with `OverlapParams`; a grid hash for data |

Sources: munificent/game-programming-patterns:book/command.markdown, munificent/game-programming-patterns:book/flyweight.markdown, munificent/game-programming-patterns:book/observer.markdown, munificent/game-programming-patterns:book/prototype.markdown, munificent/game-programming-patterns:book/singleton.markdown, munificent/game-programming-patterns:book/state.markdown, munificent/game-programming-patterns:book/double-buffer.markdown, munificent/game-programming-patterns:book/game-loop.markdown, munificent/game-programming-patterns:book/update-method.markdown, munificent/game-programming-patterns:book/bytecode.markdown, munificent/game-programming-patterns:book/subclass-sandbox.markdown, munificent/game-programming-patterns:book/type-object.markdown, munificent/game-programming-patterns:book/component.markdown, munificent/game-programming-patterns:book/event-queue.markdown, munificent/game-programming-patterns:book/service-locator.markdown, munificent/game-programming-patterns:book/data-locality.markdown, munificent/game-programming-patterns:book/dirty-flag.markdown, munificent/game-programming-patterns:book/object-pool.markdown, munificent/game-programming-patterns:book/spatial-partition.markdown, Ukendio/jecs:README.md, Ukendio/jecs:how_to/001_hello_world.luau, Ukendio/jecs:how_to/020_queries.luau, Roblox/creator-docs:content/en-us/reference/engine/classes/RunService.yaml

## 2.13 Prototyping and game-jam workflow

**Prototype fast.**

1. Each prototype answers one question, such as "is grappling between moving platforms fun?".
2. Decide up front whether the prototype is throwaway or a keeper. Default to throwaway.
3. Timebox it to 30–90 minutes.
4. Use greybox art only.
5. Instrument it: count attempts, deaths and time to first success.
6. Set keep/kill criteria in advance. Keep the idea if a fresh player performs the verb unprompted within about 30 seconds and asks for "one more time".
7. When an idea survives, rewrite it properly rather than promoting prototype code into the game.

**Game jam.**

- Write a one-sentence concept: "You [verb] to [goal] while [constraint]."
- Cut features ruthlessly into must, should and could.
- Reserve the last 20% of the time for shipping: builds, a title screen, sound, bug fixes.

**On Roblox, with the house rules.**

- **Where to prototype.** Prototype in a separate place, or a separate Studio file. Studio Parts are acceptable there as throwaway greybox, because they never ship.
- **Moving into the real game.**
  - Every visible object becomes a Blender model before release: built in Blender, exported as GLB in a headless `blender -b` process, uploaded via Open Cloud.
  - Every one of those models gets collision.
  - The only Parts left are invisible technical helpers: triggers, prompt anchors, spawns and collision hulls.
- **Release check.** Before release, search the place for visible `Part`, `WedgePart` and `TrussPart` instances, and treat any hit as a release blocker (general knowledge).
- **Test early.** Test the prototype on a phone in the first session, not the last. Many Roblox players are on mobile, and controls that feel good on a keyboard often fail on touch.

Sources: gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/prototype-fast/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/workflows/game-jam/SKILL.md, gamedev-skills/awesome-gamedev-agent-skills:skills/disciplines/create-game-assets/references/three-d-pipeline.md

## Further reading

These titles appear in the curated book lists in the source repos.

- **Design:** Jesse Schell, *The Art of Game Design*; Raph Koster, *A Theory of Fun*; Scott Rogers, *Level Up!*; Salen and Zimmerman, *Rules of Play*; Tynan Sylvester, *Designing Games*; Adams and Dormans, *Game Mechanics: Advanced Game Design*; Mihaly Csikszentmihalyi, *Flow*.
- **AI and simulation:** Mat Buckland, *Programming Game AI by Example*; Daniel Shiffman, *The Nature of Code*.
- **Architecture:** Robert Nystrom, *Game Programming Patterns* (free online; it is the basis of 2.12).
- **Talks:** the awesome-gametalks list, linked from the magictools README.

Sources: ellisonleao/magictools:README.md, Kavex/GameDev-Resources:README.md



---

# 3. Roblox Game Design, Monetization, Analytics, LiveOps and Discovery

This section covers how a Roblox game makes players stay, spend and come back, and how Roblox decides who sees it. It is split across three files:

- `03-roblox-design-business.md` (this file): platform realities, core and genre loops, onboarding, quests and LiveOps.
- `03-roblox-design-business-part2.md`: economy math, the full monetization catalog with fees and payouts, contextual purchases and the non-invasive monetization playbook, and policy and compliance.
- `03-roblox-design-business-part3.md`: analytics, experiments and configs; discovery and growth with a launch checklist; scaling, safety and matchmaking; and a register of conflicts and version-sensitive facts.

**Conventions used throughout**

- Today is 2026-11-08. Facts that change often carry a **(version-sensitive)** flag with the date they took effect.
- Creator-docs paths are written as `creator-docs:production/...`. They point into the `Roblox/creator-docs` repository under `content/en-us/`.
- Facts from Delta's market research vault are labelled `(vault: <note path>, snapshot 2026-11-07)`. They are third-party market observations, not Roblox documentation. Treat their numbers as a snapshot.
- When two docs disagree, the newer statement wins, and the conflict is named. Part 3 ends with a full conflict register.
- House rules for this project apply everywhere and override generic advice:
  1. Every visible 3D asset is modeled in Blender. No primitive-Part builds and no marketplace models.
  2. Every visible object has proper collision. Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
  3. Push microtransactions heavily, but never invasively. Non-invasive is the most important rule. Offers are small, dismissible, never block play, are well-timed (after a win, not in the first minutes) and are rate-limited. There are no fake discounts, restarting countdowns or false scarcity.

## 3.1 Platform realities

Roblox is not an app store. It behaves more like YouTube: players hop between many games in one session, and a recommendation feed decides most of what they see. Every design and business decision should start from the facts below.

### Who plays

- **Most users play on mobile.** Design UI for touch first, then add gamepad and keyboard shortcuts. Keep clear of the core UI (chat, player list) and put inventory slots at the bottom of the screen (`creator-docs:production/game-design/design-for-roblox`).
- **More users are 13+ than under 13.** The biggest regions are the US, UK and Canada. Europe and APAC are growing (`creator-docs:production/analytics/roblox-user-base`).
- **Younger players prefer exploration, experimentation and socializing over competition.** The top games mirror childhood play: Brookhaven is "house", Islands is Lego, Jailbreak is cops and robbers. For this audience, fun matters more than visual fidelity.
- **Older players invest more time and money.** They form the core of communities and turn from tourist into regular more often (Phantom Forces, Arsenal, Doors). Do not port a game unchanged from another platform (`creator-docs:production/game-design/design-for-roblox`).
- **Tourists and locals.** Tourists hop between games for variety. Locals are almost all of a game's engaged base, and many locals start as tourists. Tourists buy items with an immediate effect or show-off value. Locals buy long-term items such as a battle pass (`creator-docs:production/monetization/index`).
- **Scale (version-sensitive).** Q3 2026 averaged about 138M daily players, down 9% year on year. This comes from one secondary source. The platform record is 47.4M concurrent users on 23 Aug 2025, driven by a Steal a Brainrot "admin abuse" event (vault: `Market/Platform Context.md`, snapshot 2026-11-07).

### How players find games

- **Home is where most traffic starts.** Roblox said "over 90% of platform traffic begins" on Home, which served 10.5B+ impressions a day (version-sensitive: Roblox statement, Mar 2025) (vault: `Market/Platform Context.md`, snapshot 2026-11-07).
- **The acquisition dashboard agrees.** Home recommendations bring "the vast majority" of players (`creator-docs:production/analytics/acquisition`).
- **A session spans several games.** Growth also comes from word of mouth, Discord, X and YouTube. Players see developers as celebrity peers (`creator-docs:production/analytics/roblox-user-base`).
- **Roblox and YouTube are the top two platforms for many users.** Design so the game is good to stream. Brookhaven has a "Creator Cam" mode that hides the UI (`creator-docs:production/game-design/design-for-roblox`).

### Age gating now shapes the audience (version-sensitive, 2026)

Roblox puts every account into one of three tiers. This is the biggest structural change for new games in 2026.

| Tier | Who | Content ratings allowed | Chat |
|---|---|---|---|
| Roblox Kids | Self-declared or age-checked 5–8 | Minimal, Mild | Off by default; a linked parent can enable it after an age check |
| Roblox Select | Self-declared 9+ until age-checked, or age-checked 9–15 | Minimal, Mild, Moderate | Off for self-declared accounts; brought in gradually after an age check |
| Roblox | Age-checked 16+ | Everything except Restricted (18+) | On by default where available |

(`creator-docs:production/publishing/kids-and-select`)

**To reach players under 16, a new game must pass an evaluation:**

- **Creator account:** verified (facial age estimation under 18, government ID at 18+), with 2-step verification.
- **Rating:** a completed Maturity and Compliance Questionnaire with a Minimal, Mild or Moderate rating.
- **Publishing cost.** Choose one:
  - An active Roblox Plus or Premium subscription for 2 consecutive months.
  - A refundable fee of 1,000 Robux per game (`creator-docs:production/publishing/publish-games-and-places`).
- **Trial phase:** the game is first shown only to age-checked users 16 and older.
- **Threshold:** **250 unique plays from highly engaged, age-checked players within 60 days.** A "highly engaged player" must meet requirements for account tenure, playtime in your game and platform spend. Platform spend means a purchase anywhere on Roblox in the last 60 days. They need not spend in your game. Roblox evaluates this hourly.
- **Expedited review:** a refundable fee of **50,000 Robux** per game skips the engagement threshold for a timed launch. Safety review still applies.
- **Tracking:** watch progress in the **Audience Reach** dashboard.

**Refund conflict.** The docs disagree on when the 1,000 Robux fee comes back.

- `kids-and-select` says it is refunded 90 days after the game becomes eligible, or 90 days after payment if it never becomes eligible.
- `publish-games-and-places` says it is refunded once the game keeps 25 highly engaged players for 60 days without moderation.

Treat both as possible and check the dashboard.

**Other audience facts:**

- Users without an age check get a Kids-equivalent experience: no chat, and no games rated above Mild. This rolled out globally by about June 2026.
- In Q3 2026, 64% of global DAU were age-checked (vault: `Algorithm/Unchecked Account Filtering.md`, snapshot 2026-11-07).
- **Design consequence:** a game that wants the whole audience must earn a Minimal or Mild rating and must hold age-checked 16+ players long enough to clear the 250-play gate. The Ads Manager **Engagement** objective buys this traffic directly; it is optional (`creator-docs:production/promotion/ads-manager`).

### Design rules that fall out of these facts

- **Social beats solo.** Many users treat Roblox as a place to hang out with friends.
  - Players are evergreen content for each other (Brookhaven).
  - Single-player games struggle.
  - Build invites into gameplay: parties, trading, co-op goals.
  - Do not price private servers out of reach (`creator-docs:production/game-design/design-for-roblox`).
- **Avatars are shared identity across the platform.** Change or hide them only for a strong gameplay reason.
- **Visual, consistent icons beat text.** Younger users avoid reading.
- **Get to the fun within 5 minutes or less.** The retention guide uses this as the D1 target (`creator-docs:production/analytics/retention`). Top games are playable within about a minute (vault: `Patterns/Playable Within a Minute.md`, snapshot 2026-11-07).
- **Players punish monetization they dislike** by downvoting. Appointment mechanics and timers you can pay to skip or shorten are unpopular on Roblox (`creator-docs:production/monetization/index`).
- **Waves are short.** Mega-hits ramp to their first multi-million peak in about 7–8 weeks, plateau for 2–5 months, then fall 90–99% within 6–12 months to a 50–300K floor. One-gimmick format hits peak at 0.5–4M and drop 90%+ within 1–4 months. Clones only win while the parent game is still rising, and remixes beat reskins (vault: `Market/Trend Lifecycle Model.md`, snapshot 2026-11-07).

Sources: creator-docs:production/game-design/design-for-roblox, creator-docs:production/analytics/roblox-user-base, creator-docs:production/analytics/acquisition, creator-docs:production/analytics/retention, creator-docs:production/monetization/index, creator-docs:production/publishing/kids-and-select, creator-docs:production/publishing/publish-games-and-places, creator-docs:production/promotion/ads-manager, vault: Roblox Research/2026-11 Market Scan/Market/Platform Context.md, vault: Roblox Research/2026-11 Market Scan/Algorithm/Unchecked Account Filtering.md, vault: Roblox Research/2026-11 Market Scan/Patterns/Playable Within a Minute.md, vault: Roblox Research/2026-11 Market Scan/Market/Trend Lifecycle Model.md

## 3.2 Core loops and genre loops

### The three layers of a core loop

Roblox's design docs describe a core loop in three layers (`creator-docs:production/game-design/core-loops`):

1. **Minute-to-minute interaction.** What the player physically does most of the time. In an action RPG, this is exploring.
2. **The most repeated set of actions.** The cycle the player repeats. In an action RPG, this is fighting.
3. **The progression engine.** What makes the repetition matter: an upgrade tree, levels, skills, collections.

A loop is healthy when each layer feeds the next. Exploration finds fights, fights pay currency and XP, and progression makes the next exploration faster or more interesting.

**Test a loop before building art.** Prototype on paper or in Studio, and explore four areas (`creator-docs:production/game-design/prototyping`):

- The core loop.
- UI and UX.
- Game rules, such as the respawn timer.
- Edge cases.

**House-rule note.** Prototypes may use temporary greybox geometry inside Studio. None of it ships. Every visible object in a release build is a Blender model with proper collision.

### The shared core of 2026 hits

Market observations from the November 2026 snapshot (vault: `Patterns/Income Per Second to Multiplier to Rebirth.md`, `Patterns/One New Verb on the Idle Core.md`, `Patterns/Things Happen on a Timer.md`, `Patterns/Offline Progress.md`, `Patterns/Weekly Updates on a Fixed Day.md`, `Patterns/Stacked Mutations and Multipliers.md`, `Patterns/Collection Index and Trading.md`, `Patterns/Loss Aversion Through PvP Theft.md`, snapshot 2026-11-07):

- **Income per second, then multipliers, then rebirth.** Most hits add one new verb on top: steal, grow, kick, throw.
- **Things happen on a timer.** Examples:
  - Rare spawns every 5 or 15 minutes (Steal a Brainrot).
  - Nest resets every 5 minutes and events every 30 minutes (Steal An Egg).
  - Restocks and weather (Grow a Garden).
  - Daily shops (99 Nights in the Forest).
  - Weekly boutiques (Dress To Impress).

  Players stay to "just catch the next one".
- **Offline progress** gives a reason to return tomorrow.
- **Weekly updates on a fixed day.** All-time concurrent-player records were set on update days. Brookhaven updates on Fridays. Adopt Me triples its players on major updates.
- **Stacked mutations** (Silver, Gold or Rainbow; weather; Neon or Mega) multiply rarity tiers from the same models. For this project, that means Blender material and shader variants of one mesh. This is cheap content that still meets the Blender-only rule.
- **Collection indexes and trading** extend a game's life by years (MM2, Adopt Me) but bring scam risk.
- **Loss aversion through PvP theft** (base locks, thief alerts) drives sessions and Robux spent on defence. The cost is complaints and cheating.

These are market patterns, not Roblox guidance. Read them together with the discovery rules in 3.10: a loop that hooks players but makes them bounce or feel cheated loses impressions.

### Genre loops

Each entry gives the loop, what players pay for, and where rewarded video fits. The rewarded-video benchmarks come from Roblox's genre playbooks.

- **Opt-in rate** is the share of ads-eligible users who watch at least one ad.
- **Frequency** is how many ads each viewer watches per day.

#### Simulator and incremental

- **Loop.** Click or collect, then convert to currency, then buy upgrades, then reach a rebirth, which multiplies income. Bee Swarm Simulator is the doc example: "click an item to max level, then trade it for an upgraded version" (`creator-docs:production/game-design/design-for-roblox`).
- **The enemy is friction**, meaning the time between upgrades. Rewarded video should bridge that friction for non-payers while paid options keep big spenders engaged (`creator-docs:production/promotion/rewarded-video-playbooks/incremental-sim`).
- **Rewarded-video strategies:**
  - Velocity rewards (speed or multiplier boosts).
  - Doubling offline earnings on return.
  - Refilling energy or stamina.
  - Ten minutes of Auto-Click or Auto-Sell, which also previews a premium pass.
- **Rewarded-video benchmark:** opt-in 13%+, frequency 2.8.
- **What sells:** 2× Cash, 2× speed, auto-collect, extra storage, rebirth skips. Market prices: X2 Money 399 R$ and X2 Growth Speed 467 R$ (Steal An Egg); a 99 R$ rebirth skip (Kick a Lucky Block) (vault: `_raw/B-core-mechanics.md`, snapshot 2026-11-07).
- **Economy:** see the cost-curve and rebirth formulas in Part 2, section 3.5.

#### Tycoon

- **Loop.** Droppers produce currency. The player buys more droppers and building pieces, and the base grows (Lumber Tycoon 2) (`creator-docs:production/game-design/design-for-roblox`).
- **What drives it:** efficiency, accumulation and time management.
- **Rewarded-video strategies** (`creator-docs:production/promotion/rewarded-video-playbooks/tycoon`):
  - **Time Skip:** double offline earnings on return.
  - **Progressive Rewards:** a sequence of videos whose payout grows with each consecutive view (Grow a Garden).
  - **Progression Accelerators:** a cash injection or a booster (Mansion Tycoon, Raft Tycoon).
- **Rewarded-video benchmark:** opt-in 15%+, frequency 3+.
- **What sells:** 2× Cash, auto-collect, extra plots, cosmetic base themes, VIP areas.

#### Obby (obstacle course)

- **Loop.** Attempt a stage, fail, retry, reach a checkpoint, unlock the next stage. Tower of Hell is the doc example.
- **Rewarded-video placements** (`creator-docs:production/promotion/rewarded-video-playbooks/obby`):
  - First spawn: timed buffs or an extra daily bonus.
  - Mid-session: free currency or a trial of a high-value item.
  - Post-failure second chance.
- **Rewarded-video benchmark:** genre average opt-in 15–25% with frequency 3; best in class 30%+ with frequency 4+. Examples:
  - Escape the Carnival of Terror Obby (27% opt-in, 3.9 frequency): watch after failing to claim an item good for one life.
  - Glide Tower (47%, 2.3): watch after failing to respawn at the previous checkpoint.
- **What sells:** skip-stage products, checkpoint saves, trails and cosmetics, gravity or speed coils, VIP.
- **Compliance note:** a stage skip is a fixed, disclosed outcome, not a random item.

#### RPG

- **Loop.** Explore, then fight, then loot and XP, then gear and skills, then harder zones.
- **Roblox frames an RPG ad as "a micro-transaction paid for with time"** (`creator-docs:production/promotion/rewarded-video-playbooks/rpg`). Placements:
  - **Convenience:** bypass a crafting cooldown.
  - **Loss aversion:** a "Second Wind" revive at a checkpoint instead of the starting village.
  - **Scarcity:** a Luck Potion that boosts rare drops for 10 minutes.
  - **Grind:** 2× EXP for a set time.
- **Guardrails:**
  - A daily cap.
  - Deterministic rewards only ("Watch to receive [Specific Item]").
  - Account-bound rewards, because tradable ad rewards invite alt-account farming.
- **Rewarded-video benchmark:** opt-in 15%+, frequency 3+.
- **What sells:** 2× EXP, extra inventory, cosmetic armor sets, mounts, fast travel, a season pass.

#### Shooter

- **Loop.** Short, intense rounds. Decisions happen in the breaks: death screen, lobby, results.
- **Rewarded-video strategies** (`creator-docs:production/promotion/rewarded-video-playbooks/shooter`):
  - **Pre-Match Boost:** 2× XP, credits or keys for the next match, never damage, health or aim.
  - **Armory Currency Reward:** a small free-currency option shown next to the paid bundles.
  - **Weapon Trial:** use a premium weapon or skin for one match (Rivals).
  - **Post-Match Payout Boost:** double the round's coins or XP (Hypershot uses the pre-match boost).
  - **Rule:** never interrupt a fight.
- **Rewarded-video benchmark:** opt-in 10%+, frequency 3+.
- **What sells:** cosmetics, skins, characters, battle passes. PvP and skill games sell cosmetics, not power (vault: `Patterns/Money From Speed Multipliers and Convenience.md`, snapshot 2026-11-07).

#### Survival

- **Loop.** Prepare, survive a hazard or round, keep a streak, repeat (Natural Disaster Survival).
- **The core fear is losing everything.** Rewarded video is a safety net at peak tension (`creator-docs:production/promotion/rewarded-video-playbooks/survival`):
  - **Second Chance:** revive near the point of death.
  - **Pre-Round Power-Up:** a shield, speed boost or tool for one round.
  - **Streak Saver:** keep a survival streak after dying.
  - **Daily Survival Kit:** one consumable per 24 hours.
- **Rules:** deterministic rewards only, consumables only, and a daily cap.
- **Examples:** Evade (Second Chance plus Streak Saver), Natural Disaster Survival and Scary Shawarma Kiosk (Pre-Round Power-Up).
- **Rewarded-video benchmark:** opt-in 13%+, frequency 2.5+.
- **Market note:** Survival was the hottest genre in the week of 28 Sep–4 Oct 2026 (+45.4%) (vault: `Market/Platform Context.md`, snapshot 2026-11-07).

#### Sports

- **Loop.** Match, then result, then progression, then rematch. Every loss is motivation.
- **Rewarded-video strategies** (`creator-docs:production/promotion/rewarded-video-playbooks/sports`):
  - Post-Match Earnings Boost.
  - A Currency Reward next to the paid bundles.
  - **Rematch Rescue:** re-enter instantly instead of waiting.
  - **Pre-Game Edge:** a one-session speed, stamina or power boost.
- **Rule:** boosts last one match or one session only. Permanent ones look pay-to-win.
- **Best triggers are emotional moments:** before a match (anticipation), after a loss (frustration) or after a win (reward).
- **Examples:** NFL Universe Football; Blue Lock Rivals (currency reward plus progressive unlock).
- **Rewarded-video benchmark:** opt-in 15%+, frequency 3+.

#### Roleplay and hangout

- **Loop.** Customize a self and space, then act out social scenarios, then show off and collect. Brookhaven is the doc example and is "house" for kids. Players are each other's content.
- **What sells:** premium vehicles, houses and estates. Brookhaven sells passes from 275–799 R$, about 5,716 R$ for everything, while most content stays free (vault: `_raw/B-core-mechanics.md`, snapshot 2026-11-07).
- **Strong contextual sale:** Adopt Me offers the Modern Mansion while the player looks at their basic house (`creator-docs:production/game-design/contextual-purchases`).
- **Rating risk (version-sensitive).** Under `content-maturity`, social hangouts and free-form creation are rated 16+, and hangouts with private spaces are 18+. Parental controls cannot override this.
  - For under-18 audiences, avoid settings mainly in bedrooms, bathrooms or closets, and add bounding-box limits on beds (`creator-docs:safety`).
  - A roleplay game that wants Kids and Select audiences needs a structured, activity-led design, not a free-form hangout.

#### Horror

- **Loop.** Explore, build tension, get chased or scared, escape, and progress to the next floor or night.
- **Co-op roguelite horror** (DOORS) sells revives for 30 R$ and gives new players one free (vault: `_raw/B-core-mechanics.md`, snapshot 2026-11-07).
- **Pre-play shops are a model to copy** (`creator-docs:production/game-design/contextual-purchases`):
  - The DOORS lobby sells only Knobs, its currency.
  - Its elevator Pre-Run Shop sells consumables.
- **Asymmetric horror** (Forsaken) sells points packs from 40 R$ (100 points) to 7,600 R$ (20K points), plus packs that raise the chance of playing the killer.
- **Rating:** fear levels set the maturity rating. Mild fear is allowed at Mild; moderate fear needs Moderate (`creator-docs:production/promotion/content-maturity`).
- **Market:** liminal horror is a rising wave (vault: `_MOC.md`, snapshot 2026-11-07).
- **Season:** horror peaks near 4× normal players on 28–31 Oct (vault: `Market/Seasonal Multipliers.md`, snapshot 2026-11-07).

#### Tower defense

- **Loop.** Place and upgrade towers, survive waves, earn currency, then unlock or summon new towers and harder maps.
- **What sells:** tower skins, crates or summons, and extra tower slots.
- **UI example:** Tower Defense Simulator groups Daily Tower Skins apart from Daily Crates (`creator-docs:production/game-design/ui-ux-design`).
- **Compliance:** summons and crates bought with Robux, or with currency bought with Robux, are paid random items. They need full odds disclosure and a PolicyService gate (Part 2, 3.8).
- **Market:** anime incrementals and tower defense form an active wave (vault: `_MOC.md`, snapshot 2026-11-07).
- **Economy:** wave rewards must scale with the cost of the next tower tier. Use the cost-curve math in 3.5.

### Genre table (doc definitions)

| Genre | Description | Example |
|---|---|---|
| Action | Less popular on Roblox than elsewhere | Arsenal |
| Customization | Dress-up and shopping | Fashion Famous |
| Hide and seek | Hide from a player or NPC | Piggy |
| Obby | Obstacle course | Tower of Hell |
| Roleplaying | Social roleplay | Brookhaven |
| Simulator | Click an item to max level, then trade it for an upgraded version | Bee Swarm Simulator |
| Survival | Survive hazards | Natural Disaster Survival |
| Tycoon | Droppers produce currency; build and unlock more droppers | Lumber Tycoon 2 |

(`creator-docs:production/game-design/design-for-roblox`)

**Genre settings:**

- Set the genre and subgenre in Creator Dashboard > Publish Settings > Game Details.
- You can change the genre only **once every three months**.
- Roblox reviews genres and may change inaccurate ones; you can appeal through Support.
- Changes take a few days to reach the Charts sorts (`creator-docs:production/publishing/experience-genres`).
- Recommended For You learns genre from player behavior. The selected genre is not a ranking input (`creator-docs:discovery-faq`).

Sources: creator-docs:production/game-design/core-loops, creator-docs:production/game-design/prototyping, creator-docs:production/game-design/design-for-roblox, creator-docs:production/game-design/contextual-purchases, creator-docs:production/game-design/ui-ux-design, creator-docs:production/promotion/rewarded-video-playbooks/incremental-sim, creator-docs:production/promotion/rewarded-video-playbooks/tycoon, creator-docs:production/promotion/rewarded-video-playbooks/obby, creator-docs:production/promotion/rewarded-video-playbooks/rpg, creator-docs:production/promotion/rewarded-video-playbooks/shooter, creator-docs:production/promotion/rewarded-video-playbooks/survival, creator-docs:production/promotion/rewarded-video-playbooks/sports, creator-docs:production/promotion/content-maturity, creator-docs:safety, creator-docs:production/publishing/experience-genres, creator-docs:discovery-faq, vault: Roblox Research/2026-11 Market Scan/Patterns/*, vault: Roblox Research/2026-11 Market Scan/_raw/B-core-mechanics.md, vault: Roblox Research/2026-11 Market Scan/Market/Seasonal Multipliers.md

## 3.3 Onboarding (first-time user experience)

Onboarding decides the D1 retention number and the first-session bounce rate, which is one of Recommended For You's most important signals (3.10). Treat it as the highest-leverage system in the game.

### Goals

Roblox defines three onboarding goals (`creator-docs:production/game-design/onboarding`):

1. **Teach the essentials.** Cover the controls, then what the core loop is and why to do it.
2. **Get to the fun fast.**
   - Use an XP curve with low early thresholds, so the first level-ups come in seconds or minutes. Tune it live with Configs.
   - Use social motivators. Experiments can test matchmaking parameters during onboarding.
   - Give starter items and currency. Test starting amounts with Experiments, then roll the winner out globally with Configs.
3. **Leave players wanting more.**
   - Show short, mid and long-term goals: skill trees, season passes, quests, collections.
   - End onboarding with a deliberate moment of joy.

**Success measures:** D1 retention and the share of players who hit each onboarding goal. Fun should arrive in **5 minutes or less** (`creator-docs:production/analytics/retention`, `creator-docs:production/analytics/engagement`).

### Techniques

Roblox lists three techniques (`creator-docs:production/game-design/onboarding-techniques`).

**1. Visual elements.** A bouncing arrow, particles, a glowing trail, or an in-world sign showing the loop. They serve four goals:

- **Clarity.**
  - Color or Die places a sign in the player's line of sight.
  - Hello Kitty Cafe spotlights the target button, dims the rest of the screen, outlines the button in pink and points an arrow at it.
  - Jailbreak uses hints that imply interactivity.
- **Accessibility.** No translation is needed, and visuals suit small screens and young readers.
- **Immersion.** A trail suggests a path without forcing it.
- **Feedback** (Winds of Fortune):
  - VFX flashes on hits.
  - Red damage numbers.
  - A red screen effect at low health.
  - Health bars for the player and the enemy.
  - Coins fly out on a kill.
  - The quest counter updates.

**House-rule note.** In-world signs, arrows and props used for onboarding are visible 3D objects, so they are Blender models. Particles, beams and trails are effects, not models, and are allowed. A guide-arrow mesh modeled in Blender looks far better than a stretched primitive.

**2. Contextual (just-in-time) tutorials.** Teach a system at the moment the player meets it.

- Squishmallows shows the combine tutorial when the player holds two identical items.
- Its marketplace tutorial appears when the player finds the marketplace.
- Benefits: better retention of what was learned, faster onboarding and lower cognitive load.

**3. Timed hints.** Show a hint only to players who have not acted after most players already have.

- In Roblox's plant example, most players press the button within 10 seconds, so the highlight appears at 11 seconds.
- Rules:
  - Show each hint once.
  - Show it only to players who need it.
  - Show it only after most players have finished the step.
- Timed hints can also surface overlooked features, such as the trade button for a player who has not used it in two sessions.
- Experiments can compare a 5-second and a 10-second delay. Configs then apply the winner.

### Onboarding blueprint (decision rules)

1. **Spawn into the loop, not a menu.** No loading-screen offers in the first session, and no starter pack on the first load (`creator-docs:production/game-design/contextual-purchases`).
2. **First reward within 30 seconds.** The first upgrade or level comes within 1–2 minutes.
3. **Teach one verb at a time.** Use contextual tutorials for every secondary system: trading, crafting, rebirth.
4. **Instrument every step** with `LogOnboardingFunnelStepEvent`. Track win and lose outcomes too. The biggest drop between two steps is where to work first (`creator-docs:production/analytics/funnel-events`).
5. **Show a goal ladder before the session ends.** Give one goal for today, one for this week and one long-term, such as a collection index or season-pass tier.
6. **Ask for the notification opt-in at a moment that warrants a future notification.** For example, "Your egg hatches in 2 hours". Never gate gameplay on it (3.10).
7. **No monetization prompts during onboarding.** The first offer comes after the first meaningful win, and never inside the first-session grace period (Part 2, 3.7). This is the house rule.

### Anti-patterns

- **Long, front-loaded tutorials.** Players bounce, and bounces in the first 60 seconds and at 61–180 seconds are ranking signals (`creator-docs:discovery`).
- **Text walls.** Younger players skip reading.
- **Forcing the avatar into a costume** without a gameplay reason.
- **A starter-pack popup in the first minutes.** The monetization glossary defines a starter pack as "an initial offer… a new user sees within the first few minutes after joining". This project's house rule overrides that: starter packs appear only after a win and outside the grace period.
- **Asking for likes, favourites or group joins before the player has had fun.** It is a common market pattern: Steal An Egg gives 10K free Speed for a like, favourite and group join (vault: `Patterns/Engagement Prompts in the Loop.md`, snapshot 2026-11-07). Roblox's docs do not explicitly ban it. Treat it as a risk: never gate progress on it, keep the reward small, and check current Community Standards before shipping.

Sources: creator-docs:production/game-design/onboarding, creator-docs:production/game-design/onboarding-techniques, creator-docs:production/game-design/contextual-purchases, creator-docs:production/game-design/monetization-foundations, creator-docs:production/analytics/retention, creator-docs:production/analytics/engagement, creator-docs:production/analytics/funnel-events, creator-docs:discovery, vault: Roblox Research/2026-11 Market Scan/Patterns/Engagement Prompts in the Loop.md

## 3.4 Quests, missions and LiveOps

### Quest anatomy

A quest has an **objective**, a **quantity** and a **reward**, for example "Catch 10 fish, get 500 Gold". Quests can chain, so finishing one unlocks the next (`creator-docs:production/game-design/introduction-to-quest-design`).

**Goal horizons:**

| Horizon | Length | Example |
|---|---|---|
| Short | One session | Daily quests: last 24 h, modest reward, a reliable soft-currency drip |
| Mid | Days to weeks | Weekly challenges, event quest chains, season-pass missions |
| Long | Months | Achievements (badges), collection indexes, max rebirth |

**What quests are for:**

- **Surface features.** The Squishmallows campsite quest.
- **Teach** through tutorial quests.
- **Add session variety.**
- **Drip resources** at a controlled rate. This is the main economy lever.
- **Drive engagement** with limited-time quests.
- **Drive progression.** Dragon Adventures' season-pass missions lead to an exclusive dragon.
- **Encourage new play.** Jailbreak has an "impossible" badge for hitting a helicopter from a vehicle.
- **Deliver narrative.** In Spellbound, the NPC Moritor wants a cure for baldness and rewards the player with a hat.

### Badges

- **Free creation:** up to 5 badges per game per 24 hours (GMT). Each extra badge costs 100 Robux.
- **Image:** use a 512×512 template. It is cropped to a circle.
- **Awarding:** award on the server with `BadgeService:AwardBadgeAsync`. Check ownership with `UserHasBadgeAsync`, or `GetUserBadgesAsync` for batches.
- **Enabled state:** `GetBadgeInfoAsync` returns `IsEnabled`.

(`creator-docs:production/publishing/badges`)

### Season pass design

Roblox's guide sets these starting values (`creator-docs:production/game-design/season-pass-design`):

- **Length:** about 1 month per season, with at least a 1-week rest between seasons.
- **Tiers:** start with 10.
- **Tier rewards:** consumables, small amounts of currency, temporary buffs (for example a 10% shield) and small cosmetics.
- **Final reward:** a brand-new asset that is retired after the season. Show it as a 3D model in the world. For this project it is a Blender model with its own showcase plinth, also from Blender.
- **Tracks:** free and premium. Premium is a superset of free.
  - Free players can't complete premium missions.
  - A player who upgrades mid-season gets every premium reward for tiers already completed.
- **Claiming:** a manual claim button, with a badge icon for unclaimed rewards. Anything unclaimed is auto-awarded at season end.
- **Missions:**
  - Unlock and reset daily.
  - Vary category and difficulty (easy, medium, hard).
  - Rarely repeat a mission.
  - **Never require hard currency.**
  - Premium players get daily bonus missions that everyone can see but only premium players can complete.
- **Mission categories:** exploration, collection, combat, social, customization, survival. Use at least 3.
- **Surfacing:**
  - Big colorful buttons.
  - A visible timer.
  - Themed HUD art.
  - A first-login message.
  - Notification badges.
  - An in-world prize showcase.
- **Later additions:**
  - Missions for each new feature.
  - Co-op missions.
  - **Catch-up: double XP in the final week.**
  - Weekly hard missions.
- **Comprehension:** enroll players automatically, and keep progress, rewards and time remaining visible.
- **Monetization traits:**
  - Rewards are previewed and tied to the core loop.
  - The split between free and premium is clear.
  - Reward spacing matches the average session time.
  - XP per level is stated clearly (`creator-docs:production/game-design/monetization-foundations`).

**Worked tier-XP plan (illustrative):**

- **Season:** 28 days. Target: an engaged free player active 4 days a week (16 active days) finishes all 10 tiers in about 80% of the season.
- **XP sources:** 3 daily missions at 100, 150 and 250 XP (500 XP per active day), plus about 100 XP per day from play. So 600 XP per active day × 16 days = 9,600 XP.
- **Tier thresholds** rise gently: 500, 650, 750, 850, 950, 1,000, 1,050, 1,150, 1,250, 1,400.
  - Cumulative total: 9,550 XP.
  - The first tier lands on day 1, which gives an early win.
- **Catch-up:** double XP in the final week lets a 3-days-a-week player finish too.
- Use Roblox's tier-balance spreadsheet from the guide to check spacing against your real session data.

**Season pass as a subscription:** a battle pass can be sold as a subscription. A player who subscribes mid-season can claim the premium rewards they already earned (`creator-docs:production/game-design/subscription-design`, `creator-docs:production/monetization/subscriptions`).

### Feature packages

Roblox ships free, open-source feature packages on the Creator Store. They are code and UI, not 3D models, so they do not conflict with the Blender rule. Restyle their UI to match the game (`creator-docs:resources/feature-packages/index`).

- **Missions.** Each mission has a `missionId`, a `categoryId` and tasks. Options:
  - `prerequisites`.
  - Manual unlock.
  - Start and end times in UTC (unfinished missions fail at the end time).
  - Repeatable, with a repeat limit and a delay.
  - `expireSeconds`, plus `expireCountOffline` to count offline time.
  - Timed tasks.
  - Categories can reset on a schedule, which gives daily or weekly boards.
  - (`creator-docs:resources/feature-packages/missions`)
- **Season Passes** (beta). Needs Core and Missions. Tiers have an `upperBoundXP`, plus a free and a premium reward. Call `SeasonPasses.addProgressToSeason()` to add XP (`creator-docs:resources/feature-packages/season-passes`).
- **Engagement Rewards.** Two reward types:
  - `Daily` (login streaks).
  - `Time` (minutes played).

  You must replace `rewardClaimedHandlerFunction()`, which returns a boolean, with your own grant logic (`creator-docs:resources/feature-packages/engagement-rewards`).
- **Bundles.** Sells item collections for Robux or for in-game currency.
  - Use a new developer product per bundle, so sales are tracked separately.
  - **House-rule conflict:** the sample prompts a `StarterBundle` on `PlayerAdded`. Do not ship that. Call `Bundles.promptIfValidAsync(player, "StarterBundle")` from your offer gate after the first win instead (Part 2, 3.7).
  - (`creator-docs:resources/feature-packages/bundles`)

### LiveOps: content cadence

**Two kinds of updates** (`creator-docs:production/game-design/liveops-essentials`, `creator-docs:production/game-design/content-updates`):

- **Cadence content** builds only on existing systems: avatar items, furniture, pets, vehicles, weapons, levels or maps, quests, limited-time events, seasonal content and UGC contests.
  - Simple color variants work well (Adopt Me pet variants).
  - Keep each cadence update under 3 weeks of effort.
  - Many games ship one every 2 weeks to 1 month. The monetization guide calls weekly ideal and monthly the minimum (`creator-docs:production/monetization/index`).
  - The market pattern is a weekly update on a fixed day (vault: `Patterns/Weekly Updates on a Fixed Day.md`, snapshot 2026-11-07).
- **Expansions** add new systems and take months:
  - Social: guilds, groups, trading, parties.
  - Competitive: PvP, leaderboards, tournaments.
  - Collections and achievements.
  - Live events: map overhauls, new roles.

  A new system is an expansion, not cadence, and cannot be sustained weekly.

**Retention guide cadence:** small updates every 2–4 weeks and big ones every 2–3 months to lift D30 (`creator-docs:production/analytics/retention`).

**Quality-of-life updates** cover UI, UX flows, aesthetic refreshes, accessibility and performance. Prioritize bugs by severity, effort and number of players affected.

**Rules for content that lasts:**

- Theme every release. Holidays are not universal, so pick themes that travel.
- Content must not be used up at once:
  - Put new progression content at the end of the progression.
  - Limited-time content should take most players weeks to exhaust.
  - Use season passes.
- Make players earn access to new content (`creator-docs:production/monetization/index`).
- Listen for the reasoning behind player suggestions (Discord), tie every update to the core loop and to analytics, and protect the team's health.

**Blender pipeline note.** Cadence content is mostly new models: pets, vehicles, props and map pieces. Budget Blender time per release. Use material and shader variants of existing meshes (the "mutation" pattern) for cheap cadence that still meets the quality bar.

### LiveOps: events

Events are temporary and complement the core loop. Content updates are permanent (`creator-docs:production/game-design/liveops-planning`).

**Plan:**

1. Pick one target KPI, for example DAU or D7.
2. Define the player actions you want.
3. Design rewards that do not break the economy. Prefer a unique event currency spent only in an event shop (3.5).

**Communicate:**

- **External:** social media, an experience event (3.10) and an update announcement.
- **Internal:** login popups, UI alerts and the lobby.
- **Timing:** announcing in advance maximizes participation. Announcing just before feels spontaneous but risks being missed. Design a memorable start moment.

**Monitor:**

- Data must be timely: hourly and same-day.
- Data must be comparable: the week before versus the week after.
- Success means short and long-term retention rise, and item and currency sales rise both during and after the event.

**Market levers (vault):**

- **Live "admin abuse" events** are the biggest single lever: a scheduled spectacle with exclusive drops. Steal a Brainrot's August 2025 event pushed the platform to its 47.3–47.4M concurrent-user record; sources differ (vault: `Patterns/Live Admin Abuse Events.md`, snapshot 2026-11-07).
- **Seasonal windows** (ROLearn estimates against a trailing 30-day baseline) (vault: `Market/Seasonal Multipliers.md`, snapshot 2026-11-07):

| Window | Dates | CCU lift | Notes |
|---|---|---|---|
| Halloween | 10 Oct–3 Nov | 2–3× | Horror peaks near 4× on 28–31 Oct; launching after 25 Oct misses most of it |
| Thanksgiving | 20–30 Nov | 1.3–1.5× | |
| Winter holiday | 15 Dec–5 Jan | 1.8–2.5× | Revenue lift 2.5–3.5×, the highest of the year; spending concentrates on 24 Dec–2 Jan through Robux gifts; holiday events earn 3–4× pass revenue |
| Summer | 10 Jun–20 Aug | 1.5–2× | Best window to launch a new game is 10–30 Jun |
| Back to school | Late Aug–mid Sep | 0.8–0.9× | The only dip |

Recommended For You traffic also peaks every Saturday (`creator-docs:discovery`).

**Event recommendations:**

- **Lower risk (recommended):** a fixed weekly update day plus one themed event per month. Each event has its own event currency, an event shop, a timed spawn (every 15–30 minutes) and a free event badge. Gift versions of passes are on sale during the winter window.
- **Bolder, higher risk:** a scheduled live admin event every 2–4 weeks, announced with an experience event (needs 1,000 RSVPs for the Trending Events chart). It offers exclusive but genuinely earnable drops and a server-wide Server Luck moment if the game has luck mechanics.
  - Upside: the largest concurrent-player spikes in the market.
  - Downside: it needs live staff and robust servers, and if drops are missed or bugged, players turn on the game publicly.

**Anti-patterns:**

- **Event rewards paid in the main soft currency.** This causes inflation, and Gold purchases fall after the event (3.5).
- **"Limited time" claims that are not true, and countdowns that restart.** Both are banned (Part 2, 3.8).
- **Shipping a new system as weekly cadence.** It burns the team out.
- **A season pass without catch-up mechanics.** Players who fall behind stop trying.

Sources: creator-docs:production/game-design/introduction-to-quest-design, creator-docs:production/publishing/badges, creator-docs:production/game-design/season-pass-design, creator-docs:production/game-design/monetization-foundations, creator-docs:production/game-design/subscription-design, creator-docs:production/monetization/subscriptions, creator-docs:resources/feature-packages/index, creator-docs:resources/feature-packages/missions, creator-docs:resources/feature-packages/season-passes, creator-docs:resources/feature-packages/engagement-rewards, creator-docs:resources/feature-packages/bundles, creator-docs:production/game-design/liveops-essentials, creator-docs:production/game-design/content-updates, creator-docs:production/game-design/liveops-planning, creator-docs:production/monetization/index, creator-docs:production/analytics/retention, creator-docs:discovery, vault: Roblox Research/2026-11 Market Scan/Patterns/Weekly Updates on a Fixed Day.md, vault: Roblox Research/2026-11 Market Scan/Patterns/Live Admin Abuse Events.md, vault: Roblox Research/2026-11 Market Scan/Market/Seasonal Multipliers.md


## 3.5 Virtual economy balance (with worked math)

A Roblox economy usually has one or more **soft currencies** earned in play (Coins, Gold, Gems) and one **hard currency**, Robux, bought with real money. The design goal is that earned currency keeps its value over time. When players can buy currency with Robux, inflation in the soft currency also destroys Robux revenue (`creator-docs:production/game-design/balance-virtual-economies`, `creator-docs:production/game-design/monetization-foundations`).

### What to measure before tuning

Roblox's balancing guide says to track:

- Who buys what.
- Which actions yield currency.
- Currency earned versus currency purchased.
- Whether earned or purchased currency is what gets spent on items.
- Item usage and timing.
- How often each feature is used.

Log every currency change with `AnalyticsService:LogEconomyEvent` (code in Part 3, 3.9). The Economy dashboard then shows sources and sinks by transaction type.

**Health rules from the economy-events guide:**

- Total sources minus total sinks should sit **near 0** over time.
- If the average wallet balance keeps growing, especially for payers, add sinks.
- The dashboard shows up to 5 currencies, while the limits table allows 10 resource types.

(`creator-docs:production/analytics/economy-events`)

A third-party economy skill suggests a working tolerance: keep the sinks-to-sources ratio within about 5% of 1.0 over a long enough horizon (`dungnotnull/tycoon-game-economy-design-agent-skill: SECOND-KNOWLEDGE-BRAIN.md`). This is a heuristic, not a Roblox rule.

### Core formulas

**Sources, sinks and wallets:**

```
NetFlow(day)        = Σ sources(day) − Σ sinks(day)
SinkRatio           = Σ sinks ÷ Σ sources          (target ≈ 1.0 over a week or more)
WalletGrowth(day)   = mean wallet(day) − mean wallet(day−1)   (split payers / non-payers)
DaysToAfford(item)  = price ÷ median daily earnings          (track for the next key item)
EV(roll)            = Σ p_i × value_i                         (expected value of a random source)
```

**Upgrade and rebirth curves** (from `gamedev-skills/awesome-gamedev-agent-skills: roblox-simulator-economy`):

| Quantity | Formula | Notes |
|---|---|---|
| Price of the next level | `floor(baseCost × g^owned)` | Use g = 1.07–1.15 for upgrades bought many times, and 1.5–3 for rare large ones |
| Cost from level a to b | `baseCost × g^a × (g^(b−a) − 1) ÷ (g − 1)` | The floored per-level sum is slightly less |
| Price doubling interval | `log(2) ÷ log(g)` levels | About 5 levels at g = 1.15, 10 at 1.07 and 2 at 1.5 |
| Buy max | Walk the real prices until the next exceeds the balance or `maxLevel` | Safer than the log formula with floored prices |
| Rebirth requirement k | `R0 × r^k` | |
| Additive rebirth multiplier | `1 + k × p` | Grows slowly |
| Wait ratio between rebirths (additive) | `T(k+1) ÷ T(k) = r × (1 + k·p) ÷ (1 + (k+1)·p)` | Starts at r ÷ (1+p) and climbs toward r |
| Multiplicative multiplier | `q^k`, giving a constant wait ratio of r ÷ q | Easy to tune, but every other income source must be designed for exponential growth |
| Offline income | `floor(min(away, maxHours × 3600) × rate × efficiency)` | Away time ≤ 0 or NaN pays 0 |

**Pacing targets** (starting points, from the same skill):

- **Early upgrades take seconds.** The default config's first 10 levels take 3–10 s each.
- **Each rebirth should take only a little longer than the last,** about ×1.2 to ×1.5.
  - With r = 3 and p = 0.5, the ratio runs ×2.00, ×2.25, ×2.40 up to ×2.67, and rebirth 8 takes 137 days at default income. That is far too slow.
  - With r = 1.8, the ratio runs ×1.20 rising to ×1.60, and rebirth 8 takes 3 days 20 hours.
  - Keeping r = 3 with a multiplicative q = 2.4 gives a constant ×1.25.
- **Offline earns less than online.** Use an efficiency of 0.25–0.5 and a cap of 8–12 hours.
- **Precision.** Luau numbers are exact integers only up to 2^53 (about 9e15). Past about 1e15, store a mantissa and exponent pair, or a log10 value.
- **Display.** Round before choosing a suffix, so 999,950 shows "1.0M", not "1000.0K".

### Worked example 1: the fishing event (fixed from the docs)

Roblox's guide uses a game called Feline Fishing Fun with the currency Gold (G) (`creator-docs:production/game-design/balance-virtual-economies`).

**Baseline odds and values:**

| Fish | Chance | Value | EV contribution |
|---|---|---|---|
| Catfish | 70% | 10 G | 7 G |
| Trout | 20% | 20 G | 4 G |
| Salmon | 10% | 30 G | 3 G |
| Total | 100% | | **14 G per cast** |

**Doc typo.** The page writes the Salmon line as "30% = 3G". The arithmetic only works at 10%, which this table uses.

At 1,000 casts per day across the game, the baseline source is **14,000 G per day**.

**The event:** add a Golden Salmon worth 1,000 G at 0.1% for 24 hours.

- **Renormalize the odds.** Adding 0.1% on top makes the total 100.1%, which breaks the paid-random-item disclosure rule (3.8) if casts can be bought or boosted with Robux. Take the 0.1% from Catfish, so Catfish becomes 69.9%.
- **New EV** = 0.699×10 + 0.2×20 + 0.1×30 + 0.001×1000 = 6.99 + 4 + 3 + 1 = **14.99 G per cast**, which is **+7.1%**.
- **The real risk is participation, not EV.** If the event triples activity to 3,000 casts a day, Gold entering the economy goes from 14,000 to 3,000 × 14.99 = **44,970 G per day**, which is **+221%**.

Roblox warns that launching without this estimate creates a Gold surplus: "players stop buying Gold, and revenue falls after the event."

**Fixes, in order of safety:**

1. **A unique event currency** (for example Golden Scales) earned only during the event and spent only in an event shop. Roblox calls this "the safest solution".
2. **Event sinks priced to absorb the surge:**
   - Golden cosmetics in the event shop, such as accessories and rod skins. These are Blender models.
   - A sequential event next month that spends the previous event's currency.
   - Fees on event-only services.
3. **Balanced elevation:** sources and sinks both rise, but stay close together on the dashboard.

### Worked example 2: pricing currency packs against playtime

**Rule from the subscription design guide:** about **$1 USD per 100 Robux**. Work out how much soft currency equals 1 Robux by how much gameplay it takes to earn it. Then compare against your existing 100 Robux pack (`creator-docs:production/game-design/subscription-design`).

**Step 1: measure earnings.** The median engaged player earns 14,000 G in a 45-minute day, about **311 G per minute**.

**Step 2: decide what 100 Robux should buy.** This is a design decision. Here, 100 R$ ≈ 30 minutes of play, so 100 R$ ≈ 9,330 G, rounded to **10,000 G**.

**Step 3: build the ladder.** Bonuses must be **permanent and genuine**. They are a stated bonus on a larger pack, not a "sale" that never ends (3.8).

| Pack | Price | Gold | Bonus vs base rate | G per Robux |
|---|---|---|---|---|
| Pouch | 49 R$ | 4,900 | 0% | 100 |
| Sack | 99 R$ | 10,000 | ~0% | 101 |
| Chest | 399 R$ | 42,000 | +5% | 105 |
| Vault | 999 R$ | 110,000 | +10% | 110 |
| Hoard | 2,499 R$ | 287,000 | +15% | 115 |

**Step 4: check against item prices.** If the key mid-game item costs 50,000 G, it takes about 2.7 days of median play or 499 R$ of packs. If that feels like pay-to-skip a wall, the wall is the problem, not the price.

### Worked example 3: pricing timed boosts consistently

**A 2× Cash boost for 10 minutes** adds about 600 s × income per second. At 311 G per minute (5.2 G/s), it adds about **3,110 G**.

- At the ladder's 100 G per Robux, that is worth about **31 R$** of Gold.
- **Rule:** price the boost at about **1–1.5× its currency-pack equivalent**, because boosts also give speed and fun, not just Gold. That puts 2× Cash for 10 minutes at **29–49 R$**.
- **Market check:** permanent 2× Money passes sell at 399 R$ (Steal An Egg, Dress To Impress) (vault: `_raw/B-core-mechanics.md`, snapshot 2026-11-07).
- **Implication:** a timed boost for a whole week would beat the permanent pass. Cap stacking (code in 3.7) and keep long durations rare.
- **Arbitrage check:** if the boost's currency value is far above its price, players buy boosts instead of packs, and the Gold pack line dies. Recompute whenever income per second changes. A rebirth multiplier also multiplies boost value.

### Worked example 4: Luck, Server Luck and pity

Luck products change the odds of a random outcome. That makes them **probability modifiers**, which are explicitly covered by the paid random items rules when bought with Robux or with currency bought with Robux (`creator-docs:production/monetization/paid-random-items`). The house rule allows Luck and Server Luck **only if the game already has luck mechanics**.

**Base egg weights:** Common 90, Rare 9, Legendary 1 (total 100), so 90% / 9% / 1%.

**2× Luck** doubles the weights of every tier above Common:

| Tier | Weight | Shown odds |
|---|---|---|
| Common | 90 | 90 ÷ 110 = **81.82%** |
| Rare | 18 | 18 ÷ 110 = **16.36%** |
| Legendary | 2 | 2 ÷ 110 = **1.82%** |

The total is 100%. "2× Luck" does not mean 2× Legendary chance: here it is 1.82×. **Display the real numbers.** Roblox requires boosted odds to be shown numerically and kept updated while the boost is active.

**Server Luck** applies a modifier to everyone in the server. It is bought by one player.

- Disclose the new odds to everyone in the server, and show who activated it and its exact end time.
- Players restricted by `ArePaidRandomItemsRestricted` must not be able to buy it (3.8).

**Pity:** guarantee a Legendary after N rolls without one.

- With p = 1% per roll, the chance of hitting at least one Legendary in 100 rolls is 1 − 0.99^100 ≈ **63.4%**. A pity counter at 100 caps the worst case.
- Pity is also a probability modifier. Show the counter and the rule.

**Implementation rule:** build the shown odds and the server roll from the **same weight list**, after applying any boost. Then shown and actual odds cannot drift (`roblox-simulator-economy: references/formulas.md`).

**Price direct sales at expected value** for restricted players. A 10 R$ roll with a 5% chance of an item means selling the item directly for 10 ÷ 0.05 = **200 R$** (`creator-docs:production/monetization/paid-random-items`).

### Inflation and deflation: signals and fixes

| Signal | Likely cause | Fix |
|---|---|---|
| Mean payer wallet rising week over week | Not enough sinks for big spenders | Add aspirational cosmetics and upgrades at the top end; add a prestige or rebirth sink |
| Gold pack sales drop after an event | Event flooded soft currency | Move events to a unique event currency; add an event shop sink |
| Days-to-afford the next key item rising | Prices outran income (g too high) | Lower `costGrowth` to 1.07–1.15 for frequently bought upgrades |
| Rebirth k takes weeks | `requirementGrowth` far above multiplier growth | Lower r, or switch to a multiplicative multiplier |
| A few players earn 10× the median | Exploit or uncapped source | Server-side caps, rate limits, anomaly review |
| Offline payouts of days of income | Client timestamp or no cap | Server `os.time()` only; cap hours; treat a future `lastSeen` as now |

### Server-authoritative economy rules

These come from `roblox-simulator-economy`:

- **A RemoteEvent carries intent only**, such as "buy upgrade Income". Never send an amount or a price from the client.
- **The server looks up the price, checks the balance, spends and grants without yielding in between.** A yield between the check and the spend allows double-spends.
- **Rebirths are decided on the server.** Never accept "I rebirthed" or a balance from the client.
- **Repair save data on load and never error.** Non-numbers, NaN, infinity and negative values become 0, and unknown upgrade IDs are dropped.
- **Rate-limit every remote per player** with a token bucket.
- **Trading:** if paid items can be traded, gate trading with `IsPaidItemTradingAllowed`, and compare regional price levels (3.6).

Sources: creator-docs:production/game-design/balance-virtual-economies, creator-docs:production/game-design/monetization-foundations, creator-docs:production/game-design/subscription-design, creator-docs:production/analytics/economy-events, creator-docs:production/monetization/paid-random-items, gamedev-skills/awesome-gamedev-agent-skills: skills/other-engines/roblox-simulator-economy/SKILL.md and references/formulas.md, dungnotnull/tycoon-game-economy-design-agent-skill: SECOND-KNOWLEDGE-BRAIN.md, vault: Roblox Research/2026-11 Market Scan/_raw/B-core-mechanics.md

## 3.6 The monetization catalog: every product, fee and payout

All earnings are paid as **Earned Robux** unless noted. The standard creator share on a Robux sale is **70%**: Roblox keeps 30%. Roblox Plus discounts are funded by Roblox, so the creator still gets 70 Robux per 100 Robux list price (`creator-docs:production/monetization/roblox-plus`).

### Product catalog

| Product | What it is | Price rules | Creator share | Hold / notes |
|---|---|---|---|---|
| **Game pass** | One-time permanent purchase | Set in Creator Hub; icon up to 512×512 (circle crop) | 70% | About 5 days. Listed passes appear on Home, in search and on the post-Robux-purchase page |
| **Developer product** | Repeatable purchase (consumables, currency, boosts) | 1 Robux to 1 billion Robux | 70% | Must be granted through `ProcessReceipt`; never from `PromptProductPurchaseFinished` |
| **Subscription (Robux)** | Auto-renewing monthly benefit; single tier only | 49 Robux or more; forced regional pricing; price change once per 60 days, increases need 30 days' notice | 70% every month | About 5 days; no refunds |
| **Subscription (local currency)** | Same, paid in local money | $2.99 / $4.99 / $7.99 / $9.99 / $14.99; price can't change (delete and recreate) | 70% first month, then **100%** | 30 days. Seller must be ID- or phone-verified. Web, App Store and Google Play only. Unavailable in Argentina, China, Colombia, India, Indonesia, Japan, Russia, Taiwan, Türkiye, UAE, Ukraine and Vietnam |
| **Paid access (Robux)** | Pay to enter the game | 25–1,000 Robux | 70% | Escrow up to 7 days; no refunds; not on Xbox; no private servers; verified email and account 30+ days old |
| **Paid access (local currency)** | Pay to enter, in local money | $9.99 / $29.99 / $49.99 | 50% / 60% / 70% | Escrow 60+ days; buyer refunds within 48 h; desktop and web only; ID-verified 13+ seller with Tipalti; moderation review |
| **Private servers** | Rentable servers | Free or a monthly Robux fee; not combinable with paid access | 70% | Changing the price cancels all active subscriptions; under-13s may be blocked by settings |
| **Plus private-server incentive** | Plus subscribers get paid private servers free | — | 70% of the server price, capped at 100 R$ per subscriber per month | Subscriber needs 60+ minutes in 30 days and the server in their top 5 |
| **Plus sign-up incentive** | Sign-ups through `PromptRobloxSubscriptionPurchase` | — | 250 R$ per month for 3 months (up to 750 R$) | 60-day hold; trials don't count |
| **Robux transfers** | A Plus subscriber sends Robux to another user in your game | 10–500 Robux | **10%** to the game (recipient gets 90%) | DevEx-eligible; Roblox takes no fee |
| **Avatar items sold in game** | Catalog items via the inspect menu or `AvatarEditorService` | Item creator adds your start place to its sale locations | **40% affiliate commission** to the game owner (item creator 30%, platform 30%) | Item analytics cover up to 400 items |
| **Creator Store** | Plugins and models for other creators | Plugins $4.99+, models $2.99+ | Only taxes and payment fees deducted | 30-day escrow |
| **Commerce products** | Real-world Shopify goods | US buyers 13+ (18+ in Texas) | Merchant terms | Creator 18+, ID, email and 2FA verified; 500 products, 100 on sale |
| **Rewarded video** | Opt-in 6–30 s ad that grants a developer product | Reward worth about 3–10 Robux | Earnings = EPM × impressions ÷ 1,000 | Needs 2,000+ unique monthly visitors |
| **Immersive ads** | Billboard and portal ads in the world | — | Per view, impression or teleport | Paid on the 25th of the following month |
| **Creator Rewards** | Platform payouts for engagement and new users | Automatic | See below | 60-day hold |

Sources for the table:

- `creator-docs:production/monetization/passes`, `developer-products` and `subscriptions`.
- `creator-docs:production/monetization/paid-access-robux`, `paid-access-local-currency` and `private-servers`.
- `creator-docs:production/monetization/roblox-plus` and `robux-transfers`.
- `creator-docs:marketplace/marketplace-fees-and-commissions`.
- `creator-docs:production/monetization/commerce-products`.
- `creator-docs:production/promotion/rewarded-video-ads` and `immersive-ads`.
- `creator-docs:creator-rewards`.

**Cross-game sales (version-sensitive):** since **May 30, 2026**, a game can no longer sell passes or developer products that belong to another game. This is now in effect. Use Robux transfers or move products into the game that sells them (`creator-docs:production/monetization/passes`).

### Subscription limits and earnings

- Up to 50 subscriptions per game. The shortened game name is permanent.
- **Rules:**
  - Give each subscription a clear name with its price and duration.
  - Give the same benefits on every platform.
  - Honor the full term.
  - Never send users to buy on another platform.
  - Never gate paid benefits behind extra tasks. Battle passes are allowed.
- **Deleting an active subscription** refunds subscribers fully and pays you nothing.
- **Worked earnings** (at $0.01 = 1 Robux):
  - A $5 local-currency subscription pays 350 R$ in month one, then 500 R$ a month.
  - A 500 R$ Robux subscription pays 350 R$ every month.
- **Analytics:** new, renewed, resurrected and cancelled subscribers. Webhooks fire on purchase, renewal, cancellation and refund.
- **APIs:**
  - `GetUserSubscriptionStatusAsync` (server only).
  - `PromptSubscriptionPurchase`.
  - `Players.UserSubscriptionStatusChanged`.
  - `GetSubscriptionProductInfoAsync`.
  - `GetUserSubscriptionPaymentHistoryAsync`.

(`creator-docs:production/monetization/subscriptions`)

**Subscription use cases** (`creator-docs:production/game-design/subscription-design`):

- Bundles. If any item is durable, choose the Durable product type.
- Currency packs, using about $1 per 100 Robux.
- Item or variety packs. Limit durables.
- VIP memberships.
- Season passes.

Design subscriptions to be valuable, informative, diverse, consistent, progressive and engaging.

### Creator Rewards (version-sensitive: replaced Engagement-Based Payouts on July 24, 2025)

- **Daily Engagement:** **5 Robux per day** for each **Active Spender** who plays your game 10+ minutes, if yours is among the first 3 games they launch that day.
  - An Active Spender made qualifying purchases (Robux, Premium or UGC subscriptions) of **$9.99+ in the past 60 days** and was not new or reactivated in that time.
- **Audience Expansion:** **35% of a new or reactivated user's first $100** of qualifying purchases anywhere on Roblox in their first 60 days. All of these must be true:
  - They arrive through your share link, a direct link, or a search for your exact game name.
  - It is their first session of the day, and they play 10+ minutes.
  - Your game averages 100+ DAU over the 60 days.
  - You are ID-verified.

  "Reactivated" means lapsed for 60 days.
- **Payment:** 60-day hold, paid as Earned Robux. Paid-access games qualify.
- **Banned:** bots, encouraging alt accounts, impersonation and chargeback fraud.

**Worked example:**

- If 2,000 Active Spenders a day play your game 10+ minutes as one of their first 3 launches, Daily Engagement pays 2,000 × 5 = **10,000 R$ per day**.
- Each fully qualifying Audience Expansion user is worth up to **35 USD-equivalent in Robux** (35% × $100).

**Design consequence:** share links and "search for our exact name" campaigns on YouTube and Discord pay twice, once in players and once in Audience Expansion. Put the share link everywhere off-platform (3.10). (`creator-docs:creator-rewards`)

**Premium:** `PromptPremiumPurchase` still exists.

- Never paywall content behind Premium.
- Give no tactical advantage to Premium members.
- Check `Player.MembershipType == Enum.MembershipType.Premium` and listen to `Players.PlayerMembershipChanged`.

(`creator-docs:production/monetization/engagement-based-payouts`, deprecated page)

### DevEx: converting Earned Robux to cash (version-sensitive)

| Rate | Applies to | Effective |
|---|---|---|
| **$0.0038 per Robux** ($114 per 30,000) | Standard Earned Robux | From Sept 5, 2025 |
| $0.0035 per Robux ($105 per 30,000) | Robux earned before Sept 5, 2025; these cash out first | Legacy |
| **$0.0054 per Robux** | Developer products, passes, subscriptions and private servers bought by **US players age-verified 18+** | From June 8, 2026 |

(`creator-docs:production/monetization/developer-exchange`, `creator-docs:production/monetization/18-plus-devex-rate`)

**Eligibility:** age 13+, at least 30,000 Earned Robux, a verified email, a DevEx portal account and a W-9 or W-8 tax form.

**The 18+ rate has a strict avatar condition.** Player characters must be eligible for 100% of active playtime: R15 (standard or advanced), a custom human form, or a custom non-human form.

- **R15 animations only.** Any R6 option makes the game ineligible. Set Avatar Settings to "R15 Only".
- A custom human form needs 1 head, 2 arms, 2 legs, a torso of 2+ parts and full bipedal motion. Per the FAQ, 15+ parts or joints is enough.
- Blender-made custom rigs must meet this if you want the higher rate.

**Worked payout per 100 R$ of list price sold:**

```
Creator receives      = 100 × 0.70             = 70 Earned Robux
Cash (standard rate)  = 70 × $0.0038           = $0.266
Cash (US 18+ rate)    = 70 × $0.0054           = $0.378
Player paid (approx.) = 100 R$ ≈ $1.00 (doc rule of thumb)
Creator cash share of player spend ≈ 26.6% (standard) or 37.8% (US 18+)
```

### Managed Pricing: price optimization and regional pricing (version-sensitive)

New items are enrolled by default (`creator-docs:production/monetization/managed-pricing`, `price-optimization`, `regional-pricing`).

**Price optimization (price tests):**

- Usually needs about **60,000 transactions in the past 30 days**.
- Tests use the smallest possible cohort, and new prices are applied only if **total revenue rises**.
- Tests run automatically at least every 90 days and take about 3 weeks.
- A 4-week review follows: 98% of users see the new prices and 2% are held out.
- You can't edit prices during a test. Subscriptions are not price-tested.

**Regional pricing:**

- Prices run from **30% to 100%** of the default, based on the player's economic location. That location comes from VPN use, billing history and account history.
- On by default for passes. Developer products need opt-in, dynamic prices and `GetUsersPriceLevelsAsync`.
- Subscriptions and private servers are regionalized automatically.

**Never hard-code prices in UI.** A hard-coded number shows the wrong price to regionally priced players, price-test cohorts and Plus subscribers, who are still charged the correct amount.

- Read prices at runtime with `MarketplaceService:GetProductInfoAsync` (code in 3.7). The receipt still carries the exact Robux paid.
- Test with the dynamic price check tool ("price pinned" or "location pinned", up to 5 test accounts).
- **API note:** guides still show `GetProductInfo`, but the engine reference marks it **Deprecated, superseded by `GetProductInfoAsync`**. Use the Async version.

**Price levels protect trades and gifts.** `GetUsersPriceLevelsAsync(userIds)` returns one `PriceLevelInfo` per user (`{ UserId: number, PriceLevel: number }`), where `PriceLevel` runs 1–1000 and 1000 means full price.

- Call it at join and don't cache it past the session.
- Doc example policy: **allow gifts from a higher level to a lower one; allow trades only at equal levels.** This stops arbitrage where a low-price region buys items and trades them to full-price regions.

### Other monetization surfaces

- **The Roblox Shop.** Roblox runs a personalized Shop with Top Picks, categories, search, and Robux packages that include your items.
  - Passes are always listed. Developer products can be listed or unlisted.
  - Hide the in-game Shop menu entry with `StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.ExperienceShop, false)`. The global Shop button is off by default, and Roblox recommends enabling it.
  - Earnings are the same as for other sales.
  - **External sales** require the product to be Listed and `ProcessReceipt` to be correct. Roblox checks continuously. A flagged product loses only its external eligibility; fix it and click "Mark as fixed".

  (`creator-docs:production/monetization/shop`, `developer-products`)
- **Buy Robux page promotion.** A pass can be given free to buyers of an eligible Robux package.
  - The on-sale price must be over 49 and under 801 Robux.
  - It needs a thumbnail and cannot grant paid random items.
  - Create a unique pass for this purpose.

  (`creator-docs:production/monetization/passes`)
- **Personalized product ranking.**
  - `RankProductsAsync` has a strict rate limit, so call it once at join.
  - `RecommendTopProductsAsync` returns up to 50 items. It needs at least 1 sale in the last 28 days and excludes passes the user owns. Call it inside `task.spawn`.

  (`creator-docs:production/monetization/passes`)

Sources: creator-docs:production/monetization/passes, creator-docs:production/monetization/developer-products, creator-docs:production/monetization/subscriptions, creator-docs:production/game-design/subscription-design, creator-docs:production/monetization/paid-access-robux, creator-docs:production/monetization/paid-access-local-currency, creator-docs:production/monetization/private-servers, creator-docs:production/monetization/roblox-plus, creator-docs:production/monetization/robux-transfers, creator-docs:marketplace/marketplace-fees-and-commissions, creator-docs:production/monetization/commerce-products, creator-docs:production/monetization/shop, creator-docs:production/monetization/managed-pricing, creator-docs:production/monetization/price-optimization, creator-docs:production/monetization/regional-pricing, creator-docs:production/monetization/developer-exchange, creator-docs:production/monetization/18-plus-devex-rate, creator-docs:production/monetization/engagement-based-payouts, creator-docs:creator-rewards, creator-docs:production/promotion/rewarded-video-ads, creator-docs:production/promotion/immersive-ads, creator-docs:reference/engine/classes/MarketplaceService

## 3.7 Contextual purchases and the non-invasive heavy-monetization playbook

### Right item, right time

Roblox's framework is "right item, right time" (`creator-docs:production/game-design/contextual-purchases`):

- **In-play.** Sell at a natural pause.
  - Dress to Impress sells Theme Props during the intermission, like an arcade "continue?" countdown.
  - Leave several seconds for the Robux purchase flow.
  - If gameplay can't pause, don't use in-play offers.
- **Pre-play.**
  - The DOORS lobby sells only Knobs.
  - The elevator Pre-Run Shop sells consumables for the next run.
- **Lobby.** Super Striker League shows offers on 3D objects in the lobby. Make clear whether those are all the items; otherwise link to the main shop.
  - House rule: these displays are Blender models with collision.
- **Complementary.** Bee Swarm sells a Bee Pollen Pass (2× pollen) next to a Honey Speed Pass (2× conversion). Don't overuse this pairing; bundle the items instead.
- **UI surfaces:** badges, event windows and announcements.
  - Loading-screen offers are fine in **later** sessions, but never a starter pack on the first load.
  - Modal offers fit context: Adopt Me offers the Modern Mansion while the player looks at their basic house.
  - **Never layer modals on top of each other.**

### Shop design

The shop must be (`creator-docs:production/game-design/monetization-foundations`):

- **Integrated:** easy to find and consistent with the UI.
- **Contextual:** DOORS explains what Revives do right where it sells them.
- **Inviting:** a mall to linger in, with rotating stock.

Every item needs a clear purpose (the DOORS flashlight) and a truthful description. Item types:

- **Durable** (permanent) or **consumable** (used up).
- **Enhancement** (gameplay) or **expression** (cosmetic).

**UI attention rules** (`creator-docs:production/game-design/ui-ux-design`):

- **Highlight with color, size, space and movement, in moderation.**
  - Jailbreak puts a gold stripe under premium rewards.
  - Dragon Adventures makes its best-value coin bundle bigger, with extra padding.
- **Use conventions.** X closes a dialog, gray means disabled, and a lock means not yet unlocked.
- **Be consistent.** Prices turn red when the player can't afford them.
- **Write neutral calls to action** for minors (`creator-docs:production/monetization/index`):

| Avoid | Use instead |
|---|---|
| "GET IT NOW" | "View Item" |
| "LAST CHANCE, ACT NOW" | "See Price" |
| "BUY BEFORE IT'S GONE!" | "Open Shop" |

### The playbook: heavy but never invasive

This is the project's house rule, turned into numbers. Every number is a **Config default** that you tune with Experiments (3.9). None of them is a Roblox rule.

**Offer rules:**

1. **First-session grace period:** no offer popups in a player's first 10 minutes of lifetime playtime, and none before their first meaningful win (a first rebirth, round win or quest completion).
2. **Trigger only on positive or neutral moments:**
   - After a win.
   - After a level-up.
   - When the player opens the shop.
   - When the player inspects an item they can't afford.
   - Never mid-combat, mid-jump or mid-round.
3. **Small and dismissible:**
   - A corner card or toast covering at most about 25% of the screen on mobile.
   - An always-visible close (X).
   - Never a full-screen block.
   - Never stacked: one offer surface at a time.
4. **Rate limits:**
   - At least 8 minutes between popups.
   - At most 3 popups per session.
   - At most 1 starter-pack popup per day.
   - After 2 dismissals of the same offer, suppress it for 24 hours.
5. **Never invasive:**
   - No offer during onboarding.
   - No sound stings or screen shakes on offers.
   - No modal that steals input.
6. **Honest copy:**
   - State the exact contents, duration and price, read at runtime.
   - "+15% bonus Gold" is fine only if it is permanently true.
   - No countdowns unless there is a real fixed end time that does not restart.
7. **Passive surfaces are unlimited, because they never interrupt:**
   - A shop button with a notification dot.
   - A boost timer pill on the HUD.
   - An in-world 3D shop stand.
   - A season-pass progress bar.
8. **Free alternatives sit next to paid ones.** Put a rewarded-video "Watch for 2× for 5 min" next to the paid "2× Cash 10 min". This raises conversion through familiarity and monetizes non-payers.

### Default product set and price ladder (starting points)

Prices are Robux list prices. Regional pricing and Plus discounts adjust what players actually pay. Always display runtime prices.

| Product | Type | Starting price | Notes |
|---|---|---|---|
| 2× Cash, 10 min | Developer product | 29–49 R$ | Priced against the pack ladder (3.5 example 3) |
| 2× Cash, 30 min | Developer product | 79–99 R$ | About 2.5× the 10-minute price; the volume tier |
| 2× EXP, 10 / 30 min | Developer product | 29–49 / 79–99 R$ | RPG, shooter and season-pass XP |
| 2× Speed, 10 min (e.g. 2× delivery speed) | Developer product | 25–39 R$ | Movement or task speed |
| Luck 2×, 15 min | Developer product | 49–79 R$ | **Only if the game has luck mechanics**; disclose boosted odds |
| Server Luck 2×, 15 min | Developer product | 149–249 R$ | Luck games only; whole-server effect, announced to all |
| Starter Pack (one-time) | Developer product with a saved "bought" flag | 49–99 R$ | Shown after the first win, never in the first 10 minutes; contents worth clearly more than the price |
| Auto-Collect / Auto-Sell | Game pass | 199–299 R$ | Convenience; also trialable through rewarded video |
| Extra storage or slots | Game pass | 129–199 R$ | Market: Item Limit 129 (Dress To Impress) |
| Permanent 2× Cash | Game pass | 399 R$ | Market anchor: 399 (Steal An Egg, Dress To Impress) |
| VIP | Game pass or subscription | 799 R$ pass, or 499 R$ (or $4.99) per month | Market: VIP 799 (Dress To Impress); cosmetic perks plus a chat tag |
| Gift version of each pass | Developer product, one per pass | Same as the pass | Biggest seller in the winter window |
| Currency packs | Developer product | 49 / 99 / 399 / 999 / 2,499 R$ | Ladder in 3.5 example 2 |
| Revive or second chance | Developer product | 15–30 R$ | Market: DOORS revives 30 R$, one free for new players |
| Private server | Monthly | 0–100 R$ | Keep cheap; social is retention |

Market prices are from vault: `_raw/B-core-mechanics.md`, snapshot 2026-11-07.

### Code: ProcessReceipt that never double-grants or loses a purchase

This uses ProfileStore. The pattern comes from its docs: cache `PurchaseId` in profile data, then return `PurchaseGranted` only once the save is confirmed.

- `Profiles` maps each `Player` to an active profile.
- The profile template must include `PurchaseIds = {}`, `Coins = 0` and `Boosts = {}`.
- Grant functions must not yield.

```lua
--!strict
-- ServerScriptService/Receipts.server.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local AnalyticsService = game:GetService("AnalyticsService")

local Profiles = require(script.Parent.Profiles) -- { [Player]: Profile } managed by your ProfileStore loader
local Boosts = require(script.Parent.Boosts)

local PURCHASE_ID_CACHE_SIZE = 100

-- One entry per developer product. Grants must not yield.
local GRANTS: { [number]: (player: Player, profile: any) -> () } = {
	[1111111] = function(player, profile) -- "2x Cash - 10 min"
		Boosts.add(profile.Data.Boosts, "Cash2x", 10 * 60)
	end,
	[2222222] = function(player, profile) -- "Sack of Gold - 10,000"
		profile.Data.Coins += 10000
		AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Source, "Coins",
			10000, profile.Data.Coins, Enum.AnalyticsEconomyTransactionType.IAP.Name, "GoldPack_10000")
	end,
}

local function waitForProfile(player: Player)
	local profile = Profiles[player]
	while profile == nil and player.Parent == Players do
		task.wait(0.25)
		profile = Profiles[player]
	end
	return profile
end

local function isSaved(profile, purchaseId: string): boolean
	local saved = profile.LastSavedData.PurchaseIds
	return saved ~= nil and table.find(saved, purchaseId) ~= nil
end

MarketplaceService.ProcessReceipt = function(receiptInfo)
	local grant = GRANTS[receiptInfo.ProductId]
	local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
	if grant == nil or player == nil then
		return Enum.ProductPurchaseDecision.NotProcessedYet -- retried on next join
	end

	local profile = waitForProfile(player)
	if profile == nil or not profile:IsActive() then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	local ids = profile.Data.PurchaseIds
	if table.find(ids, receiptInfo.PurchaseId) == nil then
		local ok, err = pcall(grant, player, profile)
		if not ok then
			warn("Grant failed", receiptInfo.ProductId, err)
			return Enum.ProductPurchaseDecision.NotProcessedYet
		end
		while #ids >= PURCHASE_ID_CACHE_SIZE do
			table.remove(ids, 1)
		end
		table.insert(ids, receiptInfo.PurchaseId)
	end

	-- Only confirm once the grant is in the DataStore.
	while profile:IsActive() do
		if isSaved(profile, receiptInfo.PurchaseId) then
			return Enum.ProductPurchaseDecision.PurchaseGranted
		end
		local before = profile.LastSavedData
		profile:Save()
		if profile.LastSavedData == before then
			profile.OnAfterSave:Wait()
		end
		if not isSaved(profile, receiptInfo.PurchaseId) and profile:IsActive() then
			task.wait(10)
		end
	end
	return Enum.ProductPurchaseDecision.NotProcessedYet
end
```

**Why it is built this way:**

- **Only one server script may set `ProcessReceipt`.**
- **`receiptInfo` carries the exact Robux paid**, even during price tests.
- **`NotProcessedYet` makes Roblox retry the receipt** on the player's next join. This also covers Shop purchases made outside the game.
- **The `PurchaseId` cache makes retries idempotent.** A retry after a crash finds the ID and does not grant twice.
- **Never grant from `PromptProductPurchaseFinished`.**

(`creator-docs:production/monetization/developer-products`, `MadStudioRoblox/ProfileStore: docs/devproducts/index.md`)

### Code: timed boosts (server clock, capped stacking)

```lua
--!strict
-- ServerScriptService/Boosts.luau (ModuleScript)
-- State is saved in profile.Data.Boosts as { [boostId]: unixExpiry }.
local Boosts = {}

local MAX_STACK_SECONDS = 6 * 60 * 60 -- a boost can never be extended past 6 h from now

function Boosts.add(state: { [string]: number }, boostId: string, seconds: number)
	local now = os.time()
	local current = state[boostId]
	local base = if current ~= nil and current > now then current else now
	state[boostId] = math.min(base + seconds, now + MAX_STACK_SECONDS)
end

function Boosts.remaining(state: { [string]: number }, boostId: string): number
	local expiry = state[boostId]
	return if expiry ~= nil then math.max(0, expiry - os.time()) else 0
end

function Boosts.multiplier(state: { [string]: number }, boostId: string): number
	return if Boosts.remaining(state, boostId) > 0 then 2 else 1
end

return Boosts
```

**Decision rules for boosts:**

- **Stack duration, never multiplier.** Two 2× Cash boosts mean 20 minutes at 2×, not 4×.
- **Different boost types multiply each other.** 2× Cash × 2× from a pass = 4×. Budget for it in the economy (3.5).
- **Real-time or playtime.** The code above counts real time, including offline. If you sell "10 minutes", say "10 minutes (real time)".
  - Bolder alternative: store remaining seconds and count down only while the player is in the game. Players like it more, but it needs a per-tick update and a save on leave.
- **Show a HUD timer pill** for every active boost, with remaining time from `Boosts.remaining`.

### Code: offer gate (rate limits from Configs)

```lua
--!strict
-- ServerScriptService/OfferGate.luau (ModuleScript)
local ConfigService = game:GetService("ConfigService")

local DEFAULTS = {
	offer_grace_seconds = 600,      -- no popups in the first 10 min of lifetime playtime
	offer_min_gap_seconds = 480,    -- at least 8 min between popups
	offer_max_per_session = 3,
	offer_dismiss_limit = 2,        -- after 2 dismissals, suppress that offer for 24 h
	offer_dismiss_cooldown = 86400,
}

local snapshot: ConfigSnapshot? = nil
task.spawn(function()
	local ok, result = pcall(function()
		return ConfigService:GetConfigAsync()
	end)
	if ok then
		snapshot = result
		result.UpdateAvailable:Connect(function()
			pcall(function() result:Refresh() end)
		end)
	end
end)

local function num(key: string): number
	local value = if snapshot then snapshot:GetValue(key) else nil
	return if typeof(value) == "number" then value else DEFAULTS[key]
end

export type OfferState = {
	lifetimeSeconds: number,           -- saved: total playtime
	hadFirstWin: boolean,              -- saved
	dismissals: { [string]: { count: number, at: number } }, -- saved
	sessionShown: number,              -- session only
	lastShownAt: number,               -- session only
	inCombat: boolean,                 -- session only, set by gameplay
}

local OfferGate = {}

function OfferGate.canShow(state: OfferState, offerId: string): boolean
	local now = os.time()
	if not state.hadFirstWin or state.lifetimeSeconds < num("offer_grace_seconds") then return false end
	if state.inCombat then return false end
	if state.sessionShown >= num("offer_max_per_session") then return false end
	if now - state.lastShownAt < num("offer_min_gap_seconds") then return false end
	local d = state.dismissals[offerId]
	if d and d.count >= num("offer_dismiss_limit") and now - d.at < num("offer_dismiss_cooldown") then
		return false
	end
	return true
end

function OfferGate.markShown(state: OfferState)
	state.sessionShown += 1
	state.lastShownAt = os.time()
end

function OfferGate.markDismissed(state: OfferState, offerId: string)
	local d = state.dismissals[offerId] or { count = 0, at = 0 }
	d.count += 1
	d.at = os.time()
	state.dismissals[offerId] = d
end

return OfferGate
```

**How to wire it in:**

- Call `OfferGate.canShow` on the **server** when a trigger fires, such as a win.
- If it returns true, fire a RemoteEvent that shows a small card. The card's "View" button calls `PromptProductPurchase`.
- Log impressions, dismissals and purchases as a shop funnel (3.9) to measure each trigger.
- Configs need the game to be published, so the defaults cover Studio tests.

### Code: showing dynamic prices on the client

```lua
-- StarterPlayerScripts/PriceLabels.client.luau
local MarketplaceService = game:GetService("MarketplaceService")

local cache: { [string]: number } = {}

local function getPrice(id: number, infoType: Enum.InfoType): number?
	local key = infoType.Name .. id
	if cache[key] then return cache[key] end
	local ok, info = pcall(function()
		return MarketplaceService:GetProductInfoAsync(id, infoType)
	end)
	if ok and info and info.PriceInRobux then
		cache[key] = info.PriceInRobux -- this player's price: regional, test or Plus
		return info.PriceInRobux
	end
	return nil
end

local function bindLabel(label: TextLabel, id: number, infoType: Enum.InfoType)
	label.Text = "…"
	task.spawn(function()
		local price = getPrice(id, infoType)
		label.Text = if price then ("%d R$"):format(price) else "View"
	end)
end

-- bindLabel(shop.Cash2x.Price, 1111111, Enum.InfoType.Product)
-- bindLabel(shop.VIP.Price, 3333333, Enum.InfoType.GamePass)
```

**Why the client, and why no cache past the session:** passes and price optimization show prices from the client, so call this on the client (`creator-docs:production/monetization/passes`). Do not cache prices across sessions, because test cohorts and regional levels change.

### Code: pass ownership and grant

```lua
-- ServerScriptService/Passes.server.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local VIP_PASS = 3333333

local function applyVip(player: Player)
	player:SetAttribute("VIP", true) -- gameplay reads this attribute
end

local function ownsPass(userId: number, passId: number): boolean
	local ok, owns = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, userId, passId)
	return ok and owns == true
end

Players.PlayerAdded:Connect(function(player)
	-- Also honour gifted passes saved in the profile (see the gift flow below).
	if ownsPass(player.UserId, VIP_PASS) then
		applyVip(player)
	end
end)

MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
	if purchased and passId == VIP_PASS then
		applyVip(player)
	end
end)
```

Grant pass privileges on the server, both on purchase and on join (`creator-docs:production/monetization/passes`).

### Gift versions of passes

A pass can't be bought for someone else. Sell a **"Gift VIP" developer product** at the same price instead, and save the gift as a flag in the recipient's data.

**Flow:**

1. The sender picks a recipient in the same server.
2. The server checks:
   - The recipient doesn't already own the pass, and hasn't already been gifted it.
   - The price levels allow the gift: `PriceLevel` of the sender ≥ `PriceLevel` of the recipient, per the regional-pricing doc's example policy.
3. The server saves `PendingGiftTarget = recipientId` in the **sender's** profile, then prompts the gift product.
4. In `ProcessReceipt`, the gift grant reads `PendingGiftTarget`.
   - If the recipient is still in the server, set `GiftedPasses[passId] = true` in their profile and announce the gift to both players.
   - If they left, give the sender a **Gift Token** redeemable later. The purchase is never lost, and the grant never yields.

```lua
-- Server-side check before prompting a gift (excerpt)
local function canGift(sender: Player, recipient: Player, passId: number): boolean
	if recipient == sender or ownsPass(recipient.UserId, passId) then return false end
	local rProfile = Profiles[recipient]
	if rProfile == nil or rProfile.Data.GiftedPasses[tostring(passId)] then return false end
	local ok, levels = pcall(function()
		return MarketplaceService:GetUsersPriceLevelsAsync({ sender.UserId, recipient.UserId })
	end)
	if not ok then return false end -- fail closed
	local byUser = {}
	for _, info in levels do
		byUser[info.UserId] = info.PriceLevel
	end
	local s, r = byUser[sender.UserId], byUser[recipient.UserId]
	return s ~= nil and r ~= nil and s >= r -- gifts may flow from higher to lower price levels
end
```

**Return shape caveat.** The engine reference describes the result as a list of `PriceLevelInfo` objects. One summary line calls it a dictionary keyed by user ID strings. Log the raw result once in a test server and adapt the loop if needed.

### Rewarded video in the playbook

Rewarded video is the non-payer half of heavy monetization.

**Hard rules** (`creator-docs:production/promotion/rewarded-video-ads`):

- **Format:** an opt-in, full-screen ad of 6–30 seconds.
- **Reward:** must be a **developer product** that would normally be sold in the game. It must be granted right after the ad, and **cannot be random**. It also cannot be Robux.
- **Trigger:** needs a clear action the player takes first, with a disclosure of the reward, for example "Watch the ad to earn 10 diamonds!".
- **Never forced** as a progress gate. It must not take over the screen or obscure avatar motion outside the ad.
- **Character safety:** pause damage while the ad plays, or show ads only in safe zones.
- **Reward value:** Roblox recommends rewards worth **3–10 Robux**.
- **Eligibility:**
  - A public, unrestricted game with no free-form user creation.
  - An approved maturity questionnaire.
  - **2,000+ unique visitors per month.**
  - A 13+, ID-verified creator with 2FA.

**Implementation:**

- Call `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)` as close as possible to showing the button.
- On the server, call `AdService:CreateAdRewardFromDevProductId` and then `ShowRewardedVideoAdAsync(player, reward[, placementId])`. Grant in `ProcessReceipt` (the receipt handler above covers it).
- Track `RegisterAdOpportunityAsync` per placement.
- **"Exclude likely spenders"** is a toggle. Enable it only if the ad reward can also be bought.

**Earnings math:**

```
Earnings (Robux)   = EPM × impressions ÷ 1000
Impressions / DAU  = opt-in rate (DUV/eDAU) × frequency
Weekly potential   = ads-eligible 7-day visitors × ads per user × EPM ÷ 1000   (dashboard calculator)
```

**Health targets** from the optimization playbook (`creator-docs:production/promotion/rewarded-video-optimization`):

| Metric | Target | Fix if low |
|---|---|---|
| Opt-in rate | 10–20%+ | Show the prompt in context, such as a HUD notice at a moment of need, not buried in menus |
| Frequency | 2–4+ per day | Loosen caps; use consumable, repeatable rewards |
| Impressions per DAU | 0.5+ | Offer several reward options for new and existing players |

**Self-audit:**

- The prompt is visible within the first couple of actions after the trigger.
- There is more than one reward type.
- The cap allows at least 2–3 prompts per session.
- Rewards are consumable.
- Rewarded video sits within or near the core loop.

**Bad placements:**

- A button buried three taps deep.
- A generic "Watch Ad" label with no reward shown.
- The same prompt for every player whether they need it or not.

**De-risk with an Experiment** using the Rewarded Video Earnings metric set (3.9).

### Recommendation

- **Lower risk (recommended):**
  - The default product set above.
  - Passive surfaces everywhere.
  - At most 3 popups per session, behind the offer gate.
  - Rewarded video at 2–3 placements: post-round 2× payout, a free option in the shop, and a revive.
  - A starter pack after the first win.
  - Gift products live all year and featured in the winter window.

  It earns steadily and protects the Recommended For You signals (play days, playtime), which multiply everything else.
- **Bolder, higher risk:**
  - Add a VIP subscription (local currency $4.99 for 100% creator share after month one) and a premium season pass.
  - Add Server Luck moments tied to live events, and Experiment-driven price tests on boosts.
  - Upside: much higher ARPPU from regulars.
  - Downside: complexity, compliance exposure (luck = paid random item rules), and risk of a pay-to-win perception that hurts D7 and D8–28.

  Ship it only after D1 and D7 meet the benchmarks.

Sources: creator-docs:production/game-design/contextual-purchases, creator-docs:production/game-design/monetization-foundations, creator-docs:production/game-design/ui-ux-design, creator-docs:production/monetization/index, creator-docs:production/monetization/developer-products, creator-docs:production/monetization/passes, creator-docs:production/monetization/regional-pricing, creator-docs:production/configs, creator-docs:production/promotion/rewarded-video-ads, creator-docs:production/promotion/rewarded-video-optimization, creator-docs:reference/engine/classes/MarketplaceService, MadStudioRoblox/ProfileStore: docs/devproducts/index.md, vault: Roblox Research/2026-11 Market Scan/_raw/B-core-mechanics.md

## 3.8 Policy and compliance

Breaking these rules risks removal from discovery, loss of ad or monetization eligibility, moderation, or account action. They override any growth tactic.

### Discounts, urgency and language

From the monetization index (`creator-docs:production/monetization/index`):

- **Genuine:** an item must not be permanently "on sale" for the same amount.
- **Fair:** a discount must not be offered for a very short time to pressure buyers.
- **No false scarcity:** no false "almost out of stock" or "limited time" claims.
- **No inaccurate or auto-restarting countdowns.** The "deal of the day" that resets daily is the doc's example.
- **Use neutral calls to action** for minors (table in 3.7).
- **Configs can schedule a real flash sale.** Run it only if the old price really applied before and returns after, with a fixed end time (`creator-docs:production/game-design/balance-virtual-economies`).

### Paid random items (crates, eggs, spins and luck)

The rules cover more than crates (`creator-docs:production/monetization/paid-random-items`):

**What counts:**

- Capsules: wheels, eggs, chests.
- Enhancements with a random duration or success chance.
- Combination items.
- **Probability modifiers: luck boosts, pity systems, better-drop items and rate-up scrolls.**
- Indirect purchases such as keys, re-roll tokens and spin tickets.
- Items bought with currency that can be bought with Robux.

**Disclosure rules:**

- Show **every outcome with numerical odds** before purchase.
- A clickable popup labeled **"Info" or "Details"** is acceptable. An (i) icon alone is not.
- Percentages must **sum to exactly 100%**. Rounding is allowed to 4+ decimal places past the first non-zero digit, with a disclaimer.
- "Odds for each item listed below: X%" is acceptable when all odds are equal.
- **Update the odds** when unique outcomes are no longer obtainable.
- Odds-boosting items must **show the new odds numerically and keep them updated** while active.
- **Free rewards** that cost no Robux and no purchasable currency need no disclosure.

**When `ArePaidRandomItemsRestricted` is true,** apply one treatment:

- Offer a free, earnable path.
- Use a fixed, disclosed order.
- **Sell the outcome directly at its expected value** (10 R$ at 5% becomes 200 R$).
- Hide or remove the item.
- Block it with an error message.
- Teleport the player away.

**When `IsPaidItemTradingAllowed` is false,** block trading of paid items.

**Rewarded-video rewards cannot be random.** The RPG playbook's "Luck Potion" is fine only as a fixed, stated item. Its boosted odds must still be shown if the boost affects outcomes that can also be bought.

### Code: PolicyService gate (fail closed)

```lua
--!strict
-- ServerScriptService/Policy.luau (ModuleScript)
local PolicyService = game:GetService("PolicyService")
local Players = game:GetService("Players")

local cache: { [Player]: any } = {}

local function fetch(player: Player)
	for attempt = 1, 3 do
		local ok, info = pcall(PolicyService.GetPolicyInfoForPlayerAsync, PolicyService, player)
		if ok then
			cache[player] = info
			return info
		end
		task.wait(attempt)
	end
	return nil
end

Players.PlayerAdded:Connect(fetch)
Players.PlayerRemoving:Connect(function(player) cache[player] = nil end)

local Policy = {}

-- Unknown policy means "restricted": never sell random items or allow paid trades on a failed lookup.
function Policy.canBuyRandomItems(player: Player): boolean
	local info = cache[player] or fetch(player)
	return info ~= nil and info.ArePaidRandomItemsRestricted == false
end

function Policy.canTradePaidItems(player: Player): boolean
	local info = cache[player] or fetch(player)
	return info ~= nil and info.IsPaidItemTradingAllowed == true
end

function Policy.canSeeAds(player: Player): boolean
	local info = cache[player] or fetch(player)
	return info ~= nil and info.AreAdsAllowed == true
end

return Policy
```

**Where to call it:**

- Check `Policy.canBuyRandomItems` before **every** prompt of an egg, crate, spin, Luck or Server Luck product. Check it again in the server handler that opens the result.
- For restricted players, swap the button for the direct-sale version, or hide it.
- Check `Policy.canSeeAds` before showing immersive or portal ads (`creator-docs:production/promotion/comply-with-advertising-standards`).

PolicyService is also required for eligibility checks on subscriptions and commerce (`creator-docs:production/monetization/index`).

### Advertising and notification standards

**Ads** (`creator-docs:production/promotion/comply-with-advertising-standards`):

- Disclose ads clearly, without copying Roblox's own disclosure style.
- Use **no third-party ad servers or external ad calls**, even for analytics. Serve only content you uploaded.
- Hide or replace ads when `AreAdsAllowed` is false. If the whole game is an ad, kick ineligible users.
- Integrity: no bots, no misclassified metadata and no obscured disclosures.

**Notifications** (`creator-docs:production/promotion/experience-notifications`). Notifications must not use dark patterns:

- **Disguised ads**, such as "important information about your account" that turns out to be a promo.
- **False time pressure**, such as "buy in the next 10 minutes".
- **Bait-and-switch "free" items.**
- **Links that pre-load a purchase.**

Never gate gameplay on enabling notifications. Notification content follows platform-wide standards and text filtering, whatever the game's rating.

### Content maturity (version-sensitive: content-maturity replaces the older experience-guidelines)

**Access by label** (`creator-docs:production/promotion/content-maturity`):

| Label | Who can play |
|---|---|
| Minimal, Mild | Roblox Kids (5–8) and Select (9–15) |
| Moderate | Select (9–15) and standard (16+) |
| Content May Vary | Age-checked 16+ only |
| Restricted | Age-verified 18+ only |

**What each label allows:**

- **Minimal:** occasional mild violence, light unrealistic blood.
- **Mild:** repeated mild violence, heavy unrealistic blood, mild fear, mild crude humor.
- **Moderate:** moderate violence, light realistic blood, moderate fear, moderate crude humor, and unplayable gambling content.
- **Restricted:** strong violence, heavy realistic blood, romantic themes, alcohol, strong language. Restricted games are unplayable in Korea, Saudi Arabia and Türkiye.

**Theme rules:**

- **Social hangouts and free-form creation are 16+.** Parental controls can't override this.
- Hangouts with private spaces are 18+.
- Romantic themes, private spaces and adult settings are 18+. Alcohol and strong language are 18+.
- Sensitive-issue themes are 16+ and not recommended unless the player is age-verified.
- **Playable gambling, including simulated gambling, is banned.** A luck game must never let players wager currency on random outcomes against each other or the house.

**The questionnaire:**

- A game with no maturity info is restricted for everyone.
- Answering only the first question reaches 16+ in most regions. The full questionnaire is needed for Kids and Select.
- It also covers paid random items, paid trading (with PolicyService), media sharing and AI interaction.
- Answer for the most extreme content, and update it whenever content changes.
- Resubmitting **pauses ad and rewarded-video eligibility** during review, so resubmit only when answers change.

**Conflict.** The older `experience-guidelines` page uses All ages / 9+ / 13+ / 17+ and puts hangouts at 13+. The newer `content-maturity` page wins.

### Other rules to remember

- **Subscriptions:**
  - The same benefits on every platform.
  - Never send users to another platform to buy.
  - Honor the full term.
  - No extra tasks to unlock paid benefits.

  (`creator-docs:production/monetization/subscriptions`)
- **Premium:** no paywalls and no tactical advantage (`creator-docs:production/monetization/engagement-based-payouts`).
- **Creator Rewards:** no bots, no encouraging alt accounts, no impersonation (`creator-docs:creator-rewards`).
- **Discovery metadata:**
  - No promises of Robux or monetary rewards.
  - Metadata must match the game.
  - No near-duplicate copies (3.10).
- **Thumbnail videos:**
  - No spoken audio.
  - No real-life footage.
  - No advertising text such as "50% off" or "Free UGC!".

  (`creator-docs:production/publishing/thumbnails`)
- **Text:** filter all user text with `TextService:FilterStringAsync`, or the game may be removed (`creator-docs:safety`).

### Compliance checklist (ship gate)

- [ ] Every price label is read at runtime. No hard-coded Robux numbers.
- [ ] Developer products are granted only in an idempotent `ProcessReceipt`. Passes are granted on join and on `PromptGamePassPurchaseFinished`.
- [ ] Every random paid outcome, including Luck, Server Luck and pity, shows exact odds that sum to 100% behind an "Info" or "Details" control. Boosted odds update live.
- [ ] PolicyService gates random items, paid trading and ads, and fails closed.
- [ ] There are no countdowns without a real fixed end, no permanent "sales" and no scarcity claims.
- [ ] Calls to action use neutral wording ("View Item", "See Price", "Open Shop").
- [ ] Rewarded-video rewards are fixed developer products, disclosed before the ad, and never block progress.
- [ ] The maturity questionnaire matches the most extreme content in the build.
- [ ] Trades and gifts respect `GetUsersPriceLevelsAsync`. Gifts flow from higher levels to lower ones; trades happen only at equal levels.
- [ ] No starter pack or offer popup appears in the first-session grace period or during onboarding.
- [ ] All user text is filtered.

Sources: creator-docs:production/monetization/index, creator-docs:production/monetization/paid-random-items, creator-docs:production/game-design/balance-virtual-economies, creator-docs:production/promotion/comply-with-advertising-standards, creator-docs:production/promotion/experience-notifications, creator-docs:production/promotion/content-maturity, creator-docs:production/promotion/experience-guidelines, creator-docs:production/promotion/rewarded-video-ads, creator-docs:production/monetization/subscriptions, creator-docs:production/monetization/engagement-based-payouts, creator-docs:creator-rewards, creator-docs:production/publishing/thumbnails, creator-docs:safety, creator-docs:reference/engine/classes/PolicyService


## 3.9 Analytics: KPIs, events, experiments and configs

### Dashboard basics

- **Eligibility.** A game gets the analytics dashboard once it has more than 10 DAU and 10 play hours for 7 straight days.
- **Filters:**
  - **Age group:** <9, 9–12, 13–15 and 18+.
  - **Active payer status,** by in-game percentile: top 15%, intermediate 35%, casual 50%, lapsed, never.
  - **Platform spender:** "Active" means $9.99+ spent anywhere on Roblox in 60 days.
  - **In-game activity:** early, active, lapsed, reactivated.
  - **Engagement:** inactive, low, medium or high, by days played in the last 7.
  - Platform activity, platform, OS and memory group.
- **Explore page:** calculated metrics (for example sources minus sinks), period-over-period comparison and a 7-day moving average.
- **Benchmarks.** Your game is compared with games that have similar players, else the same genre, else all games. Only games with 100+ DAU are used.
  - Benchmarks are shown as a 50th–90th percentile range. The doc's example D1 range is **12.11%–18.73%**.
  - Overall KPIs use the top 1,000 games by 30-day playtime, in Top 200, 500 and 1000 tiers.
  - Benchmarks do not affect ranking (`creator-docs:discovery`).
- **Sales data CSV** refreshes every 48 hours.
- **Insights** need 100+ DAU. AI reports need 1,000+ DAU, and feedback reports need 20+ comments (`creator-docs:production/analytics/insights`).

(`creator-docs:production/analytics/analytics-dashboard`)

### KPI glossary (formulas and what moves them)

| KPI | Formula / definition | What moves it |
|---|---|---|
| DAU / MAU | Unique players per day / month | Discovery, retention |
| CCU | Concurrent players at a moment | Swings 2–3× by hour of day (vault: `_AGENTS.md`, snapshot 2026-11-07) |
| D1 / D7 / D30 retention | Share of a first-play cohort that returns on day 1, 7 or 30 | D1: core loop, onboarding (fun in 5 min or less), performance. D7: progression. D30: endgame, social systems, updates |
| Average session time | Total time ÷ number of sessions | Goals, timers, co-play |
| Playtime per user | Minutes per user per day; Recommended For You caps it at 60 min per user per game per day | Loop depth, offline-return hooks |
| First-session retention curve | Share still playing after X minutes | Onboarding |
| Play-through rate (PTR) | Plays ÷ impressions (Home) | Thumbnail, title, metadata accuracy |
| First-play bounce rate | Share of first plays that end under 60 s, and at 61–180 s | Onboarding speed, thumbnail honesty |
| Play days per user | Days played within D1, D2–7 (out of 6 days) and D8–28 windows | Daily hooks, offline progress, cadence |
| Conversion (payer rate) | Paying users ÷ DAU | Starter pack, first-purchase value, contextual offers |
| ARPPU | Revenue ÷ paying users | Price ladder depth, subscriptions, VIP |
| ARPDAU | Revenue ÷ DAU = conversion × ARPPU | Both of the above, plus ads |
| ARPU (window) | Revenue in window ÷ users in cohort (7-day, 30-day) | Used by Experiments and acquisition |
| LTV (estimate) | ARPDAU × expected active days; expected active days ≈ Σ daily retention over the horizon | Use it to cap cost per play in ads |
| Spend days per user | Days with a purchase | Repeat-purchase consumables, boosts |
| Rewarded-video opt-in | DUV ÷ eligible DAU | Placement in context |
| RV frequency | Ads watched per viewer per day | Repeatable rewards, caps |
| EPM | Ad earnings ÷ impressions × 1,000 | Fill rate, audience |
| Sink ratio | Σ sinks ÷ Σ sources per currency | Economy health (3.5) |
| Abuse reports per 1,000 playtime hours | Safety dashboard; needs 1,000+ daily hours | Moderation, griefing tools |

(`creator-docs:production/analytics/retention`, `engagement`, `monetization`, `creator-docs:discovery`, `creator-docs:production/promotion/rewarded-video-ads`, `creator-docs:safety`)

**Diagnosis rules:**

- **High ARPPU with low ARPDAU** means revenue comes from too few players. Lower the first-purchase barrier with a starter pack after the first win, and offer welcome deals to first-time buyers (`creator-docs:production/analytics/monetization`).
- **D1 below the 50th percentile benchmark:**
  - Work on onboarding and performance before content.
  - Track every onboarding step, including win and lose outcomes.
- **D7 low but D1 fine:** progression stalls. Check how players spread across levels for a "wall".
- **D30 low:** missing endgame and social systems. Ship small updates every 2–4 weeks and big ones every 2–3 months.
- **A retention dip after a big influx of users is normal.** New tourists dilute the cohort (`creator-docs:production/analytics/retention`).
- **Fix retention before monetization.** Recommended For You weighs both, but retention compounds (`creator-docs:discovery-faq`).

### Analytics events API

All logging calls are **server-only** and only record in **published** games. Log an event only after the action succeeds (`creator-docs:production/analytics/event-types`).

| Call | Signature | Use |
|---|---|---|
| Onboarding funnel | `LogOnboardingFunnelStepEvent(player, step, stepName)` | One-time first-session funnel |
| Recurring funnel | `LogFunnelStepEvent(player, funnelName, funnelSessionId, step, stepName)` | Shop visits, upgrades, rounds |
| Economy | `LogEconomyEvent(player, flowType, currency, amount, endingBalance, transactionType, itemSKU?, customFields?)` | Every currency source and sink |
| Custom | `LogCustomEvent(player, name, value?, customFields?)` | Anything else, such as rounds, deaths, trades |
| Journey | `LogJourneyEvent(player, journeyName, nodeName, journeySessionId?)` | Branching paths (configured in Analytics > Journeys or as a `JourneysConfig` Creator Config) |

**Limits:**

- **Rate:** 120 + 20 × CCU requests per minute.
- **Funnels:**
  - 10 funnels with 100 steps each.
  - A user's progress expires after 180 days without events.
  - Repeated steps count once, and skipping a step auto-completes the earlier steps.
  - Only the 10 most recent session IDs per user per funnel are tracked.
- **Economy:**
  - 10 resource types.
  - Transaction types beyond 20 become "Other". Item SKUs beyond 100 become "Other".
  - The amount is always positive; the flow type gives the direction.
- **Custom events:**
  - 100 event names.
  - 3 custom fields per event. Field values beyond 8,000 combinations become "Other".
  - Custom field keys are `Enum.AnalyticsCustomFieldKeys.CustomField01.Name` to `CustomField03.Name`, and values must be strings.
- **Journeys:** 2–10 stages with 1–10 nodes each. Names can be up to 50 characters. An automatic `__entry__` stage is added. Cohorts are followed for 90 days.
- **Retention of data:** data rolls off 90 days after the last event. The View Events tool shows a near-real-time feed.

(`creator-docs:production/analytics/funnel-events`, `economy-events`, `custom-events`, `custom-fields`, `journey-events`, `event-types`)

**Built-in transaction types** (use `Enum.AnalyticsEconomyTransactionType.<X>.Name`):

- **Sources:** IAP, TimedReward, Onboarding.
- **Either direction:** Shop, Gameplay.
- **Sink:** ContextualPurchase.
- Custom types are allowed.

**Funnel session IDs:**

- None for one-time funnels.
- A GUID per shop visit.
- `<playerId>-<itemId>` for item upgrades.
- Validate any client-reported step on the server through a RemoteEvent.

**Instrumentation skill.** The `/rbx-instrument-analytics` skill works with the Studio MCP and can add these calls for you (`creator-docs:production/analytics/event-types`).

### Event schema plan (starting template)

| Event | Call | Steps / fields | Question it answers |
|---|---|---|---|
| Onboarding | Onboarding funnel | 1 Spawned, 2 FirstAction, 3 FirstReward, 4 FirstUpgrade, 5 FirstWin, 6 SawGoals, 7 Session2Start | Where new players drop |
| Shop | Funnel `Shop`, GUID per visit | 1 Opened, 2 ViewedItem, 3 PromptShown, 4 Purchased | Which surface converts |
| Offer card | Funnel `Offer`, GUID per card | 1 Shown, 2 Viewed, 3 Prompted, 4 Purchased; field01 = trigger (`Win`, `LevelUp`, `ShopOpen`) | Which trigger converts without hurting retention |
| Rewarded video | Funnel `RV`, GUID | 1 ButtonShown, 2 Clicked, 3 Completed; field01 = placement | Opt-in by placement (complements AdService metrics) |
| Coins | Economy | Every source and sink; SKU per item; field01 = event or season | Sink ratio, wallet growth |
| Rounds | Custom `RoundEnded`, value = seconds | field01 = map, field02 = result, field03 = mode | Map balance, round length |
| Rebirth | Custom `Rebirth`, value = rebirth count | field01 = minutes since last rebirth, bucketed | Pacing versus the ×1.2–1.5 target |

### Code: logging calls

```lua
-- Server only. Call after the action succeeds.
local AnalyticsService = game:GetService("AnalyticsService")
local HttpService = game:GetService("HttpService")

local F1 = Enum.AnalyticsCustomFieldKeys.CustomField01.Name
local F2 = Enum.AnalyticsCustomFieldKeys.CustomField02.Name

-- Onboarding funnel (one-time, steps start at 1)
local function onboardingStep(player: Player, step: number, name: string)
	AnalyticsService:LogOnboardingFunnelStepEvent(player, step, name)
end

-- Shop funnel (recurring): new GUID per shop visit
local shopSessions: { [Player]: string } = {}
local function shopOpened(player: Player)
	local id = HttpService:GenerateGUID(false)
	shopSessions[player] = id
	AnalyticsService:LogFunnelStepEvent(player, "Shop", id, 1, "Opened")
end
local function shopStep(player: Player, step: number, name: string)
	local id = shopSessions[player]
	if id then
		AnalyticsService:LogFunnelStepEvent(player, "Shop", id, step, name)
	end
end

-- Economy sink after a successful purchase with soft currency
local function logCoinSpend(player: Player, amount: number, newBalance: number, sku: string)
	AnalyticsService:LogEconomyEvent(player, Enum.AnalyticsEconomyFlowType.Sink, "Coins",
		amount, newBalance, Enum.AnalyticsEconomyTransactionType.Shop.Name, sku,
		{ [F1] = "Season-Winter2026" })
end

-- Custom event with fields instead of many event names
local function logRoundEnd(player: Player, seconds: number, map: string, won: boolean)
	AnalyticsService:LogCustomEvent(player, "RoundEnded", seconds,
		{ [F1] = "Map-" .. map, [F2] = if won then "Result-Win" else "Result-Loss" })
end
```

**Naming rule.** Use one event with custom fields, not many event names. For example, log `PlantSeed` with a field set to Cabbage or Turnip, not `PlantCabbage` and `PlantTurnip` (`creator-docs:production/analytics/custom-events`).

### Experiments

**Types:**

- **In-game experiments**, driven by Configs.
- **Matchmaking experiments.** Only one can run at a time. They allow 3 variants and should use a 100% rollout.

**Setup:**

- **Duration:** 14–60 days.
- **Variants:** up to 2 plus a control for in-game experiments.
- **Metric sets:** Default, Rewarded Video Earnings, or Custom (up to 3 custom metrics).
- **Metrics:** D1, D7, playtime, ARPU, ARPPU, payer conversion and session time.
- **Early harm detection:** playtime, conversion and ARPU update every 5 minutes for the first 24 hours.

**Reading results:**

- **Sample size:** games under about 1,000 DAU struggle to reach a useful minimum detectable effect.
- **Significance:** a result is significant when its confidence interval excludes 0. The doc's example is ARPU +2.37%, with an interval of 0.55% to 4.19%.

**Best practices:**

- Write a hypothesis first.
- Run the full duration, because novelty effects fade.
- Change nothing mid-test.
- Weigh trade-offs, for example ARPU up but D7 down.
- Document findings.

**Targeting** copies the config rules and is evaluated per session. The config key locks while the test runs.

(`creator-docs:production/experiments`)

**High-value experiments for this playbook:**

1. Offer grace period: 10 vs 20 minutes. Primary metric D1; guardrail ARPU.
2. Popup cap: 2 vs 3 per session. Primary metric ARPU; guardrails D7 and playtime.
3. Starter-pack trigger: first rebirth vs first round win. Primary metric payer conversion.
4. 2× Cash 10-minute price: 29 vs 49 R$. Primary metric ARPPU; guardrail conversion.
5. Rewarded-video placement: post-round vs shop-only. Use the Rewarded Video Earnings metric set; guardrail playtime.
6. Hint delay: 5 vs 10 seconds. Primary metric onboarding funnel completion (`creator-docs:production/game-design/onboarding-techniques`).
7. Starting currency amount. Primary metric D1, then roll the winner out with Configs (`creator-docs:production/game-design/onboarding`).

### Configs

**Reading values:**

- `ConfigService:GetConfigAsync()` returns global values.
- `ConfigService:GetConfigForPlayerAsync(player)` returns targeted values. Experiments and targeting need this per-player form.
- Both are server-only. Read a value with `snapshot:GetValue(key)`.
- Snapshots do not auto-refresh. Listen to `UpdateAvailable`, then call `Refresh()`. `GetValueChangedSignal(key)` fires on changes to one key.

**Limits:**

- Up to 1,000 active configs.
- Types: string, number, boolean and JSON (up to 100,000 characters).
- Conditions: up to 100 per game and 20 per key.

**Publishing:** changes are staged first, then published either in 15 seconds to 1 minute, or gradually over 15 minutes.

**Target attributes:** country, language, new vs returning, source, first-played date, payer status, activity, engagement, platform spender and platform activity.

**Studio testing:** `SetTestingValue` and `ClearTestingValue` set values for local tests.

(`creator-docs:production/configs`, `creator-docs:reference/engine/classes/ConfigService`, `ConfigSnapshot`)

```lua
-- Server: per-player config (needed for experiments and targeting)
local ConfigService = game:GetService("ConfigService")

local function getPlayerConfig(player: Player)
	local ok, snapshot = pcall(function()
		return ConfigService:GetConfigForPlayerAsync(player)
	end)
	return if ok then snapshot else nil
end

local function readNumber(snapshot, key: string, default: number): number
	if snapshot == nil then return default end
	local value = snapshot:GetValue(key)
	return if typeof(value) == "number" then value else default
end

-- local cfg = getPlayerConfig(player)
-- local startingCoins = readNumber(cfg, "onboarding_starting_coins", 250)
```

**Decision rule.** Every tunable number in this section and in 3.7 should be a config key with a code default:

- XP curve.
- Starting currency.
- Hint delays.
- Offer gate values.
- Boost durations.
- Event drop rates.

Then you can tune live and run experiments without publishing a new build.

Sources: creator-docs:production/analytics/analytics-dashboard, creator-docs:production/analytics/insights, creator-docs:production/analytics/retention, creator-docs:production/analytics/engagement, creator-docs:production/analytics/monetization, creator-docs:production/analytics/funnel-events, creator-docs:production/analytics/economy-events, creator-docs:production/analytics/custom-events, creator-docs:production/analytics/custom-fields, creator-docs:production/analytics/journey-events, creator-docs:production/analytics/event-types, creator-docs:production/experiments, creator-docs:production/configs, creator-docs:production/game-design/onboarding, creator-docs:production/game-design/onboarding-techniques, creator-docs:discovery, creator-docs:discovery-faq, creator-docs:safety, creator-docs:reference/engine/classes/ConfigService, creator-docs:reference/engine/classes/ConfigSnapshot, vault: Roblox Research/2026-11 Market Scan/_AGENTS.md

## 3.10 Discovery and growth

### How Recommended For You works

1. **Retrieval.** Roblox picks candidate games using engagement, retention and monetization.
2. **Personalized ranking.** It ranks the candidates for each user.

Other sources speed up consideration: ads, curation, search, charts, friends, teleports, notifications and social sharing. But **ranking counts only users who arrived organically through Recommended For You** (`creator-docs:discovery`).

**Key signals:**

| Priority | Signal | Notes |
|---|---|---|
| Most important | Play-through rate (PTR) | First session of RFY-acquired users |
| Most important | First-play bounce rate (negative) | Measured for <60 s and 61–180 s |
| Most important | Play days per user | Counted over D1, D2–7 (out of 6 days) and D8–28 |
| Most important | Playtime per user | Capped at 60 min per user per game per day |
| Important | Intentional co-play days | Joining friends, invites, private servers |
| Important | Qualified play sessions | |
| Important | Spend days | |
| Important | Robux spent per user | |

(`creator-docs:discovery`, `creator-docs:discovery-faq`)

**How the signals are used:**

- **Per-user averages, not totals,** so small games are not disadvantaged.
- **Explore and expand phases.** The window moves and games are retested daily, so there is no penalty for a weak start, and old games can regrow.
- **Each window is judged separately, then combined.**
- **New games don't wait 28 days.** Signals arrive in order: PTR and bounce, then D1, then D2–7, then D8–28.
- **Finite or story games are not penalized** for low D8–28. Genre is learned from behavior, not chosen.
- **Value = long-term retention + long-term monetization.**
  - Fix retention first.
  - A game strong in only one area still gets impressions. Strength in both gets broader distribution.
- **Impressions also move for reasons outside your game:**
  - Your own updates.
  - Algorithm changes.
  - Seasonality: weekly peak on Saturday, plus summer, back-to-school and holidays.
  - Competitors improving: "a 50% signal gain can yield minimal impression growth if competitors improve more".
- **A user's Home shows about 100 games.**

**Version-sensitive 2026 changes** (vault: `Algorithm/June 2026 Discovery Overhaul.md`, `Algorithm/Deep Play-Through Rate.md`, `Algorithm/Not Interested Feedback.md`, `Algorithm/Oct 12 2026 Measurement Change.md`, `Algorithm/Signal and Impression Lag.md`, snapshot 2026-11-07):

- **Mar 9, 2026:** a "deep play-through rate" signal rewards plays that last past the first minutes.
- **Mar 26, 2026:** "Not interested" user feedback became a negative signal.
- **Jun 15, 2026:** the retention window grew from 7 to **28 days** (D1, D2–7, D8–28). The old qPTR signal was split into play-through, session-quality and spend signals.
  - Roblox said short-term engagement had been overvalued, which favored attention-grabbing thumbnails. This was an explicit anti-clickbait move.
  - The current creator-docs discovery page matches this structure.
- **Oct 12, 2026:** a more reliable measurement pipeline. Recorded impressions rose and PTR dipped. Roblox says ranking is unaffected. Creators report PTR drops of about 26–40% (third-party).
  - **Do not compare PTR from before and after Oct 12.**
- **Lag:** most signals update within 24 h, and impressions lag signal changes by a few days.

**What reduces exposure:**

- Leading with giveaways ("Robux! Play now!").
- Metadata that doesn't match the game. The doc's example is a "Great Dinosaur Quest" that is really a generic obby.
- **Near-duplicate games** in visuals, titles or place files. The game that first added the unique metadata or place file wins; creation date does not decide it.
- Policy violations.

A daily banner on the dashboard shows the status. Report problems through Support under "Discovery Content Quality" (`creator-docs:discovery`).

**Market reading:** the clone penalty seems narrow, applying to near-identical games only. A distinct theme plus distinct art clears it (vault: `Algorithm/Near-Duplicate Clone Penalty.md`, snapshot 2026-11-07). Blender-made original art is therefore a discovery asset as well as a quality bar.

**Ads and Recommended For You:**

- Ads don't hurt Recommended For You. Ad-acquired users are excluded from its signals permanently.
- A user acquired by an ad generally won't then see the game in Recommended For You, so impressions can dip after a campaign. **That dip is not a penalty** (`creator-docs:discovery-faq`).

### Thumbnails, icon, title and description

**Official specs** (`creator-docs:production/publishing/thumbnails`, `experience-icons`):

- **Custom thumbnail:** **required to get Home recommendation impressions** (`creator-docs:discovery`).
  - Use 16:9 at 1920×1080, under 3 MB, in jpg, gif, png, tga or bmp.
  - Up to 10 images or videos per game.
  - Keep essential elements away from the bottom edge, where the player count may cover them.
- **Thumbnail personalization:**
  - Activate 2–5 Home thumbnails. A bandit shows each to random groups, then favors the winner per group while still exploring.
  - Measured lift: +8.5% qualified play-through on average, up to +50%.
  - Test new thumbnails with each major update, then leave them alone until the next. Keep several active rather than picking one winner.
- **Video thumbnails:**
  - 3 uploads per month; rejected videos count against the quota.
  - The video must be authentic gameplay. Camera work, minor color grading, a logo overlay, curated sequences and Roblox catalog music are fine.
  - **No** spoken audio or lyrics, real-life footage, artificially enhanced graphics, misrepresented gameplay, or advertising text such as "50% off" or "Free UGC!".
  - Not supported on Xbox, PlayStation or VR.
- **Icon:** square, at least 512×512. Check it at 150×150.
- **Free camera:** press Left Shift + P in a solo playtest for cinematic captures. A Blender-built world can also be rendered directly in Blender for key art, but **thumbnails must still match real in-game visuals**.

**Market playbook** (vault: `Thumbnails/` notes, snapshot 2026-11-07). These are inference-grade rules distilled from a 72-tile feed sample:

1. Show the first minute of gameplay.
2. Use one focal point and at most 5 elements.
3. Use a big number if the game has one.
4. Show the climb in one frame (before and after).
5. Make it readable at 150 px. Text under about 40 px is unreadable.
6. Match color to genre.
7. Use a face to sell the emotion.
8. Fill all 5 personalization slots with different hooks.
9. Write the title as a status tag plus a verb phrase, for example `[UPD 🔫] Realistic Ragdoll Playground 🩸`. 64% of feed titles carry an emoji or a bracket tag.
10. Copy the format, not the art.

**Two strategies by game age:** established games use a logo and moody art, because their name is the hook. New format games use saturated color, a giant number and a visible progression, because the mechanic is the hook (vault: `Thumbnails/Two Thumbnail Strategies by Game Age.md`).

**Description.** Roblox's experimental guidance, meant only for select creators, focuses on external SEO (`creator-docs:production/publishing/descriptions`):

- Open with a **hook of up to about 160 characters** that contains the title, the core genre and the most unique feature.
- Then cover recent updates, the main mechanics, and device support, codes and FAQ.
- Example: "X is a fast-paced tower defense game to build up your fortress and fend off hordes of enemies. Can you build the ultimate base and survive all 500 levels?"

Use accurate tags and a gameplay video to reduce bounces (`creator-docs:discovery-faq`).

### Social growth tools

**Invite prompts:**

- Check `SocialService:CanSendGameInviteAsync` (wrapped in pcall), then call `SocialService:PromptGameInvite(player, options)`.
- `ExperienceInviteOptions` fields:
  - `PromptMessage`. It is hidden if it overflows the UI.
  - `InviteUser`, to target one friend.
  - `InviteMessageId`, a Notification string asset that must include `{experienceName}` and may include `{displayName}`.
  - `LaunchData`, up to 200 characters, read with `Player:GetJoinData()`. It can take a few seconds to arrive, so retry.

(`creator-docs:production/promotion/invite-prompts`)

**Friend referrals:**

- `GetJoinData().ReferredByPlayerId` is filled for every invite type.
- Reward both inviter and invitee. Publish a reward banner in Engagement > Referral Rewards; only one banner is live at a time.
- **Anti-abuse:**
  - One-time rewards per invitee.
  - A cooldown per inviter.
  - Monitoring and reward cancellation.
- Eligibility: games live for at least 1 day. Referral links never expire, and invites can go to people who aren't yet Roblox friends.

(`creator-docs:production/promotion/referral-system`)

**Share links:**

- Unlimited experience links per game, each with optional custom `LaunchData` for in-game perks.
- Analytics show new users per off-platform channel.
- Make one link per channel.
- Share-link arrivals can also qualify for Creator Rewards Audience Expansion (3.6).

(`creator-docs:production/promotion/share-links`)

**Experience notifications:**

- **Eligibility:** 100+ visits since launch, not under moderation.
- **Delivery:** only to opted-in users aged 13+, and **1 per user per day** per game. Delivery is not guaranteed; reach grows with engagement.
- **Sending:** use the Open Cloud package from the Creator Store, or the Open Cloud API, with `type = "MOMENT"`, parameters, `launchData` and an analytics category.
- **Opt-in prompt:** `ExperienceNotificationService:CanPromptOptInAsync()` then `PromptOptIn()`. The text is fixed, and the prompt won't show again for 30 days after it was seen.
- **Content:** personalized and actionable. "You're 2 races away from completing the weekly challenge!" is good; generic promos are not.

(`creator-docs:production/promotion/experience-notifications`)

**Experience events:**

- Up to 10 ongoing or upcoming events, each with a thumbnail, category, start and end time, and target place. Players can tap "Notify Me".
- **Trending Events in Experiences** chart: the event started within the last 7 days, has 1,000+ RSVPs and is public.
- **Event attribution:** the event ID is added to the player's `GameJoinContext`.
- **Update announcements:** up to 60 characters, at most once every 3 days.
- **Off-Platform Featuring** (App Store, Google Play, Roblox marketing):
  - Submit at least 7 days before the start.
  - Events of 7–30 days work best.
  - Selection uses DAU growth, playtime, retention and monetization.

(`creator-docs:production/promotion/experience-events`)

```lua
-- Client: ask to invite at a co-op moment, and ask for notifications when something will happen later
local Players = game:GetService("Players")
local SocialService = game:GetService("SocialService")
local HttpService = game:GetService("HttpService")
local ExperienceNotificationService = game:GetService("ExperienceNotificationService")
local player = Players.LocalPlayer

local function promptInvite()
	local ok, canSend = pcall(SocialService.CanSendGameInviteAsync, SocialService, player)
	if ok and canSend then
		local options = Instance.new("ExperienceInviteOptions")
		options.PromptMessage = "Bring a friend into the next round!"
		options.LaunchData = HttpService:JSONEncode({ inviter = player.UserId })
		SocialService:PromptGameInvite(player, options)
	end
end

local function promptNotifications()
	local ok, canPrompt = pcall(ExperienceNotificationService.CanPromptOptInAsync, ExperienceNotificationService)
	if ok and canPrompt then
		ExperienceNotificationService:PromptOptIn()
	end
end
```

### Paid acquisition

**Ads Manager objectives** (`creator-docs:production/promotion/ads-manager`):

- **Plays:** broad distribution, testing, and early traffic that can help a game get considered for Recommended For You.
- **Earnings:** players likely to spend. It has a higher cost per play.
- **Engagement:** age-checked, highly engaged players who count toward the 250-play Kids and Select threshold. Give it a dedicated budget.

**Budgets and payment:**

- Daily or lifetime budgets with auto-bidding.
- Pay by card (18+, with a $1 verification hold) or ad credits converted from Robux. Conversion is irreversible, has a 1-credit minimum and is open to users 13+.
- **Robux earned at the US 18+ rate are converted first.** That is the most valuable Robux, so convert deliberately.
- Auto-reload is optional. Unused credits return when a campaign ends.

**Attribution:**

- A first-time player is credited to the ad for 30 days.
- A player resurrected after 7+ days away is credited for 7 days.
- A recent player is credited only for that session.
- Data can take up to 48 h to appear. The first 24 h are a learning phase.

**Placement:** campaigns show on Home and in search. A sponsored tile and a Recommended For You tile can both show, spaced apart. **Running ads does not affect Recommended For You ranking.**

**Search ads:** up to 10 keywords per ad set. They appear at the top of search results, or right after the exact-name match (`creator-docs:production/promotion/search-ads`).

**Budget rule.** Keep cost per play (CPP) below the expected value of a new player:

```
max CPP  ≈  ARPU_30d(ad-acquired cohort)  +  RV earnings per user  +  any Creator Rewards Audience Expansion share
```

Check the "Recent Users" and "Resurrected Users" reporting views, not only "All Users".

### Growth plan

- **Lower risk (recommended):**
  1. Launch with 3–5 honest Home thumbnails showing real Blender-built gameplay, plus a gameplay video.
  2. Instrument the onboarding funnel from day one.
  3. Fix bounce and D1 before spending on ads.
  4. Run a small Plays campaign to seed signals, plus an Engagement campaign if the game targets under-16s.
  5. Run a fixed weekly update day, monthly events with Notify Me, referral rewards and share links per channel.
- **Bolder, higher risk:**
  - Time the launch into a seasonal window: 10–30 Jun for summer, or before 15 Dec for winter.
  - Pay the 50,000 R$ refundable expedited review so all ages can play on day one.
  - Run a creator or influencer campaign with share links and an "admin abuse" live event in week 2.
  - Upside: wave-scale spikes and Audience Expansion income.
  - Downside: money tied up for 90+ days, and a big influx can expose weak D1, which then trains Recommended For You against the game.

### Launch checklist

**Product and quality**

- [ ] Fun within 5 minutes; first reward within 30 seconds; no long tutorial.
- [ ] Every visible object is a Blender model with collision. No visible primitive Parts, placeholders or marketplace models. Invisible Parts are used only as triggers, prompt anchors, spawns and collision hulls.
- [ ] Mobile-first UI checked on a small phone. Touch targets are large, and nothing overlaps chat or the player list.
- [ ] Performance tested on low-memory devices. The dashboard has a memory-group filter.

**Monetization and compliance**

- [ ] All developer products go through the idempotent `ProcessReceipt`. Passes are granted on join and on purchase.
- [ ] Prices are read at runtime. The dynamic price check tool has been run with pinned test accounts.
- [ ] The offer gate is live: grace period, gaps, caps, dismissal suppression, and no stacking.
- [ ] Odds disclosure and PolicyService gates are in place for any random or luck product.
- [ ] Rewarded video: the button discloses the reward, the reward is a fixed developer product, and damage is paused during ads.
- [ ] The global Shop button is enabled, and products are Listed with icons.

**Discovery and metadata**

- [ ] A custom 16:9 thumbnail is uploaded (required for Home impressions). 2–5 thumbnails are active for personalization, and a gameplay video is approved.
- [ ] A 512×512 icon, readable at 150 px.
- [ ] The title follows the status-tag + verb format. A description hook of up to 160 characters. Accurate genre and subgenre (changeable only every 3 months).
- [ ] The maturity questionnaire is complete, and the rating fits the target audience.
- [ ] Kids and Select path chosen: Plus or Premium for 2+ months, or the 1,000 R$ fee, or the 50,000 R$ expedited review.

**Analytics and LiveOps**

- [ ] Onboarding, shop, offer and rewarded-video funnels are logged. Every currency flow is logged with `LogEconomyEvent`.
- [ ] Configs exist for every tunable value, with code defaults.
- [ ] The first Experiment is queued for week 2 or later. Under 1,000 DAU, expect weak statistical power.
- [ ] Weekly update day chosen. The first event is created as an experience event, with Notify Me enabled.
- [ ] Notifications are eligible (100+ visits). The opt-in prompt is tied to a future moment.
- [ ] Share links per channel, a referral banner, and an invite prompt at co-op moments.

**Timing**

- [ ] Launch before a Saturday, ideally inside a seasonal lift window. Avoid back-to-school (0.8–0.9×).
- [ ] Do not compare PTR across the Oct 12, 2026 measurement change.

Sources: creator-docs:discovery, creator-docs:discovery-faq, creator-docs:production/publishing/thumbnails, creator-docs:production/publishing/experience-icons, creator-docs:production/publishing/descriptions, creator-docs:production/publishing/experience-genres, creator-docs:production/publishing/kids-and-select, creator-docs:production/promotion/invite-prompts, creator-docs:production/promotion/referral-system, creator-docs:production/promotion/share-links, creator-docs:production/promotion/experience-notifications, creator-docs:production/promotion/experience-events, creator-docs:production/promotion/ads-manager, creator-docs:production/promotion/search-ads, creator-docs:creator-rewards, vault: Roblox Research/2026-11 Market Scan/Algorithm/*, vault: Roblox Research/2026-11 Market Scan/Thumbnails/*, vault: Roblox Research/2026-11 Market Scan/Market/Seasonal Multipliers.md

## 3.11 Scaling, safety and matchmaking

### Scaling across platforms and languages

- **Platforms:** PlayStation, Xbox, Android, iOS, PC, Mac and Meta Quest (`creator-docs:scale`).
  - Paid access in Robux is not available on Xbox.
  - Local-currency paid access is desktop and web only.
  - Video thumbnails don't show on consoles or VR.
- **Translation:** Roblox automatically translates game text and chat for players who turn on Automatic Translations in their account settings.
  - Set your supported languages in the Localization settings.
  - Visual, icon-led UI travels better than text (`creator-docs:production/localization/automatic-translations`, `creator-docs:production/game-design/design-for-roblox`).
- **Holidays are not universal.** Pick event themes that work across regions (`creator-docs:production/game-design/content-updates`).
- **Regional pricing** already scales prices to local purchasing power (30–100%). Protect trades and gifts with price levels (3.6).

### Safety

**Rules and tools** (`creator-docs:safety`):

- **Filter all user text** with `TextService:FilterStringAsync`: names, signs, pet names, chat-like UI. Unfiltered text can get the game removed.
- **Safeguard UGC.** Monitor avatar editors and any user creation.
  - Free-form creation pushes the rating to 16+ and makes the game ineligible for rewarded video (3.8, 3.7).
- **For under-18 audiences:**
  - Avoid games set mainly in private spaces such as bedrooms, bathrooms or closets.
  - Add bounding-box limits on beds.
  - Clubs and bars are 18+.
- **Enforcement tools:** `Players:BanAsync` (it can detect alt accounts), `Player:Kick` and `Player:IsVerified`. Gate high-trust features such as trading on verification or account age.
- **The safety dashboard** shows abuse-report submitters per 1,000 playtime hours (it needs 1,000+ daily hours), reports by category, and channels (avatar, chat, voice, experience, audio). An insight appears when the game is above the 90th percentile.
- **Trading safety.** Trading economies extend a game's life but bring scam risk (vault: `Patterns/Collection Index and Trading.md`, snapshot 2026-11-07). Use:
  - Two-step confirm screens.
  - Value displays.
  - Trade logs.
  - `IsPaidItemTradingAllowed` and price-level checks.

### Matchmaking

**How a join is matched:**

1. A player requests to join a place.
2. Matchmaking finds eligible servers, filtering out ones that are full, private, reserved or about to shut down.
3. It scores each server.
4. The player joins the highest-scoring server.

(`creator-docs:matchmaking/index`)

**Score formula** (`creator-docs:matchmaking/scoring`):

```
signal score   ∈ [0, 1]      (attribute transformed: aggregation, comparison, normalization)
weighted       = signal score × weight      (weights ≥ 0; weight 0 = ignored)
server score   = Σ weighted signals         (highest score wins)
```

**Worked example:** a place with 8 slots and an Occupancy weight of 2.

- Server A has 2 players: 2/8 = 0.25, weighted 0.5.
- Server B has 6 players: 6/8 = 0.75, weighted 1.5.
- Add a Friends signal with weight 1 and Server A containing a friend: A = 1×1 + 0.5 = 1.5, which now ties B. Raise the Friends weight and A wins.

**Signals:**

- **Built-in signals:** Estimated Player Latency, Has Friends, Is Voice Chat Enabled, Player Age, Player Device Type, Player Language, Player Play History, Server Occupancy and Player Text Chat Group.
- **Maximum relevant differences:** 25 years for age and 4.6 for play history. Friends acts as a numerical signal with a maximum of 1.
- **Custom signals** need custom attributes read from your data stores, for example a skill rating or a level band. Preview new weights against mock servers before publishing.
- **Analytics** track configuration success.

(`creator-docs:matchmaking/attributes-and-signals`, `customize-matchmaking`, `analytics`)

**Matchmaking experiments:** only one at a time, with 3 variants and a 100% rollout. Test matchmaking parameters during onboarding too (`creator-docs:production/experiments`, `creator-docs:production/game-design/onboarding`).

**Decision rules:**

- **Social games** (roleplay, tycoon, simulator): weight Friends and Occupancy highest. Full servers feel alive, and co-play days are a Recommended For You signal.
- **Competitive games** (shooter, sports): add a custom skill signal and weight Latency. Keep Occupancy moderate so matches start fast.
- **Mixed-age audiences:** keep the Player Age and Text Chat Group signals on, so younger players land with peers and compatible chat settings.
- **Languages:** weight Player Language when the game relies on chat or voice coordination.
- **Server size:** large enough that a server is never empty when friends join, and small enough that the 8,000-combination analytics limits and performance budgets hold. Set it with play-test data, not guesswork.

**Recommendation:**

- **Lower risk:** keep the default weights, and raise only Friends and Occupancy for social density. This is safe and directly helps co-play signals.
- **Bolder:** add a custom "spender-and-veteran mix" or skill signal and A/B it with a matchmaking experiment. It can lift retention and ARPU, but a bad weight can silently strand new players in empty or mismatched servers. Watch D1 daily during the test.

Sources: creator-docs:scale, creator-docs:production/localization/automatic-translations, creator-docs:production/game-design/design-for-roblox, creator-docs:production/game-design/content-updates, creator-docs:safety, creator-docs:matchmaking/index, creator-docs:matchmaking/scoring, creator-docs:matchmaking/attributes-and-signals, creator-docs:matchmaking/customize-matchmaking, creator-docs:matchmaking/analytics, creator-docs:production/experiments, creator-docs:production/game-design/onboarding, vault: Roblox Research/2026-11 Market Scan/Patterns/Collection Index and Trading.md

## 3.12 Conflicts and version-sensitive register

| Topic | Older or conflicting statement | Current or preferred statement | Source |
|---|---|---|---|
| Content ratings | `experience-guidelines`: All ages / 9+ / 13+ / 17+; hangouts 13+ | `content-maturity`: Minimal / Mild / Moderate / Content May Vary / Restricted (18+); hangouts and free-form creation 16+ | creator-docs:production/promotion/experience-guidelines vs content-maturity |
| Subscription price tiers | `subscription-design`: $2.99 / $4.99 / $7.99 / $14.99 | `subscriptions`: adds $9.99 | creator-docs:production/game-design/subscription-design vs production/monetization/subscriptions |
| Fishing EV example | "Salmon 30% = 3G" | Salmon is 10%; EV = 14 G per cast | creator-docs:production/game-design/balance-virtual-economies |
| Starter-pack timing | Glossary: shown "within the first few minutes after joining" | House rule: only after the first win and outside the grace period. The docs also say no starter pack on the first loading screen | creator-docs:production/game-design/monetization-foundations, contextual-purchases |
| Bundles feature package | Sample prompts a StarterBundle on `PlayerAdded` | Prompt from the offer gate after the first win | creator-docs:resources/feature-packages/bundles |
| `GetProductInfo` | Used in monetization guides | Engine reference: deprecated; use `GetProductInfoAsync` | creator-docs:reference/engine/classes/MarketplaceService |
| Publishing-fee refund | `kids-and-select`: refunded 90 days after eligibility (or 90 days after payment) | `publish-games-and-places`: refunded once 25 highly engaged players are kept for 60 days | Both creator-docs:production/publishing |
| Economy dashboard | Shows up to 5 currencies | Limits allow 10 resource types | creator-docs:production/analytics/economy-events vs event-types |
| Payouts | Engagement-Based Payouts | Replaced by Creator Rewards on July 24, 2025 | creator-docs:production/monetization/engagement-based-payouts, creator-docs:creator-rewards |
| DevEx rate | $0.0035 per Robux | $0.0038 from Sept 5, 2025; $0.0054 for US 18+ sales from June 8, 2026 | creator-docs:production/monetization/developer-exchange, 18-plus-devex-rate |
| Cross-game sales | Allowed | Disabled from May 30, 2026 | creator-docs:production/monetization/passes |
| Recommendation window | 7 days; single qPTR signal | 28 days (D1, D2–7, D8–28) with split signals, from Jun 15, 2026 | vault: Algorithm/June 2026 Discovery Overhaul.md; creator-docs:discovery |
| PTR measurement | Pre-Oct 12, 2026 pipeline | New pipeline; PTR is not comparable across the change | vault: Algorithm/Oct 12 2026 Measurement Change.md |
| Luck boosts | Often treated as "just a boost" | Probability modifiers fall under paid random item rules | creator-docs:production/monetization/paid-random-items |
| Flash sales | "Use Configs to trigger flash sales" | Allowed only as genuine, fair discounts with a real end | creator-docs:production/game-design/balance-virtual-economies vs production/monetization/index |
| RPG rewarded-video "Luck Potion" | Listed as a rewarded-video strategy | Rewards must be fixed and non-random. A fixed luck item is fine, but its boosted odds must be disclosed where paid outcomes are affected | creator-docs:production/promotion/rewarded-video-playbooks/rpg vs paid-random-items |
| Immersive and portal ads vs house rules | Ad units need a visible Block Part (8×4.5 to 32×18 studs) with an AdGui; portals need the Creator Store BasePortal package | House rule: build the frame around the ad face in Blender and treat the ad face as a platform requirement, or skip portals | creator-docs:production/promotion/immersive-ads |
| `GetUsersPriceLevelsAsync` return shape | One reference line says a dictionary keyed by user-ID strings | Same page: a list of `PriceLevelInfo` objects; log and verify | creator-docs:reference/engine/classes/MarketplaceService |
| Incentivized likes, favourites and group joins | Common market pattern (vault) | Not explicitly covered in creator-docs; risky; never gate progress on it | vault: Patterns/Engagement Prompts in the Loop.md |

Sources: creator-docs:production/promotion/experience-guidelines, creator-docs:production/promotion/content-maturity, creator-docs:production/game-design/subscription-design, creator-docs:production/monetization/subscriptions, creator-docs:production/game-design/balance-virtual-economies, creator-docs:production/game-design/monetization-foundations, creator-docs:production/game-design/contextual-purchases, creator-docs:resources/feature-packages/bundles, creator-docs:reference/engine/classes/MarketplaceService, creator-docs:production/publishing/kids-and-select, creator-docs:production/publishing/publish-games-and-places, creator-docs:production/analytics/economy-events, creator-docs:production/analytics/event-types, creator-docs:production/monetization/engagement-based-payouts, creator-docs:creator-rewards, creator-docs:production/monetization/developer-exchange, creator-docs:production/monetization/18-plus-devex-rate, creator-docs:production/monetization/passes, creator-docs:production/monetization/paid-random-items, creator-docs:production/monetization/index, creator-docs:production/promotion/rewarded-video-playbooks/rpg, creator-docs:production/promotion/immersive-ads, creator-docs:discovery, vault: Roblox Research/2026-11 Market Scan/Algorithm/June 2026 Discovery Overhaul.md, vault: Roblox Research/2026-11 Market Scan/Algorithm/Oct 12 2026 Measurement Change.md, vault: Roblox Research/2026-11 Market Scan/Patterns/Engagement Prompts in the Loop.md



---

# 4. Roblox Engineering: Architecture, Networking, Security, Data and Tooling

This section is the engineering reference for building Roblox games. It is split into three files, read in order:

- `04-roblox-engineering.md` (this file): 4.1 Client-server model, 4.2 Project architecture, 4.3 Luau standards, 4.4 Networking.
- `04-roblox-engineering-part2.md`: 4.5 Security, 4.6 Data, 4.7 Purchases.
- `04-roblox-engineering-part3.md`: 4.8 Teleports and cross-server systems, 4.9 Multithreading and the scheduler, 4.10 Tooling, testing, CI/CD and AI agents, 4.11 Common bugs and anti-patterns checklist.

**Conventions used here**

- Source citations use `creator-docs:<path>` for files under the official Roblox creator-docs repository (`content/en-us/`), and `<Repo>:<path>` for community repositories (for example `ProfileStore:docs/api.md`).
- **[Version-sensitive]** marks facts that were true in the sources as of 2026-11-08 and are likely to change. Re-check them before relying on them.
- All code is `--!strict` Luau unless stated otherwise. Snippets were checked against the engine reference in creator-docs and the library source code. They are patterns to adapt, not drop-in libraries.

**House rules this section supports.** Every visible 3D asset is modelled in Blender, exported as GLB in a headless Blender process and uploaded through the Open Cloud Assets API (covered in 4.10). Every visible object has proper collision; invisible Parts exist only as technical helpers (triggers, prompt anchors, spawn points, collision hulls). Monetisation is heavy but never invasive (purchase plumbing is in 4.7; offer timing and UX belong to the monetisation section).

---

## 4.1 The client-server model

### 4.1.1 The two data models

Every running game has one authoritative server and many clients. The server copies the place's edit-time DataModel into a runtime DataModel, and each client receives the parts it may see (with streaming, only a subset near the player). Only server state is real. Everything a client holds is a replica, a prediction or local decoration.

Rules that follow from this:

- **Server-to-client replication is automatic** for instances in replicated containers. Property changes, new instances, destroyed instances and attribute changes made by the server reach every client that has the instance.
- **Client-to-server replication does not happen** for ordinary changes. If a LocalScript sets `part.Color`, only that client sees it. The documented exceptions all involve **network ownership** (see 4.1.4). These are the physics of assemblies the client owns, which includes its own character, and the animations played on its own character.
- **Replication order is not guaranteed across different kinds of change.** A property change and a RemoteEvent fired in the same frame may arrive in either order. Changes of the same type (for example two property changes) do arrive in order. Never write client code that assumes "the remote arrived, so the property must already be set".
- **With `StreamingEnabled`, distant parts may not exist on the client.** Use `WaitForChild` with a timeout, `CollectionService` added signals or `Model` streaming controls, never direct indexing into deep `Workspace` paths.

### 4.1.2 Containers: what lives where

| Container | Replicates to client? | Scripts run there? | Put here |
| --- | --- | --- | --- |
| `ReplicatedFirst` | Yes, first and once | Yes (client) | Minimal loading-screen script and its UI only. Its scripts can run before the rest of the game loads, so no `WaitForChild` is needed for its own children. |
| `ReplicatedStorage` | Yes | Only `Script` with `RunContext = Client` (and modules required from elsewhere) | Shared ModuleScripts, remote definitions, shared config, templates cloned at runtime, the single client entry Script. |
| `ServerScriptService` | Never | Yes (server) | The single server entry Script and all server-only modules. |
| `ServerStorage` | Never | No (modules can be required by server scripts) | Server-only assets and maps cloned in on demand, server-only modules if you prefer them out of SSS. |
| `Workspace` | Yes (streamed) | Legacy scripts do, but avoid | World geometry only. Attach behaviour with CollectionService tags, not scripts inside models. |
| `StarterPlayer.StarterPlayerScripts` | Copied into each `Player.PlayerScripts` | Yes (client) | LocalScripts if you must use them (sparingly). |
| `StarterPlayer.StarterCharacterScripts` | Copied into each character | Yes | Per-character scripts that should reset on respawn. |
| `StarterGui` | Copied into each `PlayerGui` | Yes (client) | UI templates. Most modern projects build UI from code or clone from ReplicatedStorage. |

Starter containers **copy** their contents. A `Script` with `RunContext = Client` placed in a Starter container runs once from its original location *and* once from each copy, so it runs twice. Keep `RunContext = Client` scripts in `ReplicatedStorage` and keep `LocalScript`s in the Starter containers.

### 4.1.3 Script types and RunContext

- **`Script`** has a `RunContext` property: `Legacy` (default; runs on the server, and only in legacy-supported locations such as `Workspace` and `ServerScriptService`), `Server` (runs on the server wherever it is placed), or `Client` (runs on every client wherever it is replicated, including `ReplicatedStorage`).
- **`LocalScript`** runs on the client only in specific containers: Starter* copies, `PlayerScripts`, `PlayerGui`, the character, `Backpack` and `ReplicatedFirst`. A LocalScript in `ReplicatedStorage` does nothing.
- **`ModuleScript`** runs once per side (once on the server, once per client) on first `require`, and every later `require` returns the same cached value. Requiring two modules from each other at load time fails with `Requested module was required recursively`.

**Recommended layout (official guidance):** one `Script` with `RunContext = Server` in `ServerScriptService`, one `Script` with `RunContext = Client` in `ReplicatedStorage`, a minimal loader in `ReplicatedFirst` for the loading screen, and everything else as ModuleScripts that expose a start function. The Plant reference project follows this layout.

**Client load order** (useful for knowing when `WaitForChild` is needed):

1. `ReplicatedFirst` replicates and its scripts run.
2. The rest of the DataModel replicates; then `game.Loaded` fires and `game:IsLoaded()` becomes true.
3. `PlayerScripts` LocalScripts and `RunContext = Client` Scripts in `ReplicatedStorage` run.
4. The character spawns and `StarterCharacterScripts` run.

**[Version-sensitive] Rojo versus Studio Script Sync naming.** Studio's built-in Script Sync maps `name.server.luau` to a `Script` with `RunContext = Server` and `name.client.luau` to a `Script` with `RunContext = Client` (`name.local.luau` is a LocalScript, `name.legacy.luau` a Legacy Script). Rojo's `emitLegacyScripts` project option **defaults to `true`**. Under that default, `*.server.luau` becomes a Legacy `Script` and `*.client.luau` becomes a `LocalScript`. A Rojo `Main.client.luau` mapped into `ReplicatedStorage` therefore does not run unless you set `"emitLegacyScripts": false` at the top of `default.project.json`. With the default, client entry scripts must live in `StarterPlayerScripts`. Both layouts are valid; just do not mix the assumptions.

### 4.1.4 Network ownership and physics

Roblox distributes physics. Each unanchored assembly is simulated by one **network owner**, either the server or one client.

- The server always owns **anchored** parts; you cannot change that.
- Unanchored parts default to automatic ownership. The engine hands them to a nearby client based on the character's proximity and the client's hardware capacity. Each player's client owns its own character.
- `BasePart:SetNetworkOwner(player)` (server-only) pins ownership. `SetNetworkOwner(nil)` pins it to the server. `SetNetworkOwnershipAuto()` reverts to automatic. Setting ownership on one assembly of a mechanism with no anchored parts sets it for the whole mechanism.
- Typical fix: give a vehicle to the driver when `VehicleSeat.Occupant` changes. Otherwise a passenger who sat first owns the car and the driver's input lags. Also hand loose parts riding on the vehicle to the same client.
- Server-owning gameplay-critical physics objects prevents client manipulation but can make interaction jittery. Use it deliberately, not everywhere.
- Studio visualises owners: turn on **Network owners** in the viewport visualisation options.

**Security consequence:** Roblox cannot verify physics computed by an owning client. An exploiting client can teleport, fly or noclip anything it owns, including its character. It can also fire `Touched` for parts it owns even when the server never saw a touch. See 4.5.

### 4.1.5 Server authority mode (prediction and rollback)

**[Version-sensitive]** Roblox now documents a **server authority** model. In it the server simulates everything, and clients predict locally with rollback and resimulation:

- Enable it with `Workspace.AuthorityMode = Server`. This is a protected setting you set manually in Studio. It also forces `NextGenerationReplication`, `PlayerScriptsUseInputActionSystem`, `SignalBehavior = Deferred`, `UseFixedSimulation` and `StreamingEnabled`.
- Simulation code is registered with `RunService:BindToSimulation(callback)` from a module shared by server and client. Prediction is controlled with `RunService:SetPredictionMode()` and inspected with `RunService:GetPredictionStatus()`.
- Use `time()`, which is synchronised, inside simulations. `tick()`, `os.time()` and `os.clock()` are not synchronised.
- Route simulation input through the **Input Action System** (`InputContext`, `InputAction`) and keep predicted state in attributes. Do not `Destroy` inside the simulation callback; mark with an attribute and remove after simulation.
- Effects and sounds go in render-step code. Tools are not fully supported yet.
- Design for latency: slower acceleration and delayed effects hide resimulation artefacts. Other players' inputs are not forwarded by default; racing games forward them through attributes.
- Templates exist for Racing, Soccer and Laser Tag.

The pages disagree on maturity. `creator-docs:scripting/security/network-ownership.md` says server authority is "currently in beta and will be released soon", while `creator-docs:projects/server-authority/index.md` presents it as available. Treat it as new and maturing. Use it for competitive physics games (racing, sports, shooters) and keep client ownership plus server validation (4.5) elsewhere.

Sources: creator-docs:projects/client-server.md, creator-docs:projects/data-model.md, creator-docs:scripting/locations.md, creator-docs:includes/engine-comparisons/script-locations.md, creator-docs:scripting/attributes.md, creator-docs:scripting/module.md, creator-docs:scripting/sync.md, creator-docs:physics/network-ownership.md, creator-docs:scripting/security/network-ownership.md, creator-docs:projects/server-authority/index.md, creator-docs:projects/server-authority/techniques.md, creator-docs:resources/boneheads/server-authority.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/external-editors.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/false-positives.md

---

## 4.2 Project architecture

### 4.2.1 The single-entry, module-based layout

Modern Roblox projects use **one server entry Script and one client entry Script**. Each requires ModuleScripts ("services" on the server, "controllers" on the client) and runs a two-phase lifecycle. Compared with dozens of loose scripts racing at start-up, this gives a deterministic start order, one place to catch start-up errors, explicit testable interfaces instead of globals, and no code copied inside models.

### 4.2.2 The Init/Start lifecycle

The convention most frameworks share (it originated in Knit and AeroGameFramework) is:

1. **Require** every service module. Module top-level code only builds tables; it must not yield or touch other services.
2. **Init phase**: call every `Init()`. Each service sets up its own state, creates its remotes and connects to its own signals. `Init` must not call other services' methods (they may not be initialised yet) and should not yield. Knit ran all `KnitInit` methods concurrently and waited for all of them to finish.
3. **Start phase**: call every `Start()`, each in its own thread (`task.spawn`) so one yielding service cannot block the others. Cross-service calls are safe from here on.
4. Only after all `Start` calls are dispatched should the entry script connect `Players.PlayerAdded`. It should also loop over `Players:GetPlayers()` to catch players who joined during start-up.

**Dependency rules**

- Never `require` in a cycle. If A needs B and B needs A, extract the shared part into C, or have one side resolve the other lazily inside `Start`.
- Server modules may require shared modules. Shared modules must never require server modules. Client modules may require shared modules and never server modules, which are not replicated anyway.
- Services expose functions, not mutable tables. Other services read state through getters, so the owner can validate and fire change signals.
- Do not create services after start-up has begun. Knit forbade this outright.
- Never put server logic in a module that also replicates to clients. Decompilation leaks it (see 4.5).

### 4.2.3 A typed loader

```lua
--!strict
-- ServerScriptService/Server/Main.server.luau  (Script, RunContext = Server)
-- Client mirror: ReplicatedStorage/Client/Main.client.luau with Controllers/.
local Players = game:GetService("Players")

type Service = {
	Init: ((self: any) -> ())?,
	Start: ((self: any) -> ())?,
	PlayerAdded: ((self: any, player: Player) -> ())?,
}

local servicesFolder = script.Parent:WaitForChild("Services")
local services: { [string]: Service } = {}
local order: { string } = {}

-- 1. Require every service module (top-level code must not yield).
for _, child in servicesFolder:GetChildren() do
	if child:IsA("ModuleScript") then
		services[child.Name] = require(child) :: any
		table.insert(order, child.Name)
	end
end
table.sort(order) -- deterministic order; prefix names ("10_Data") if you need explicit ordering

-- 2. Init: synchronous, no cross-service calls, no yielding.
for _, name in order do
	local service = services[name]
	if service.Init then
		local ok, err = xpcall(service.Init, debug.traceback, service)
		if not ok then
			error(`[Boot] {name}.Init failed: {err}`, 0) -- fail loudly; a half-booted server is worse
		end
	end
end

-- 3. Start: each in its own thread so a yielding service cannot block others.
for _, name in order do
	local service = services[name]
	if service.Start then
		task.spawn(function()
			local ok, err = xpcall(service.Start, debug.traceback, service)
			if not ok then
				warn(`[Boot] {name}.Start failed: {err}`)
			end
		end)
	end
end

-- 4. Players: connect last, and catch anyone who joined during boot.
local function onPlayerAdded(player: Player)
	for _, name in order do
		local service = services[name]
		if service.PlayerAdded then
			task.spawn(service.PlayerAdded, service, player)
		end
	end
end
Players.PlayerAdded:Connect(onPlayerAdded)
for _, player in Players:GetPlayers() do
	task.spawn(onPlayerAdded, player)
end
```

A service module then looks like this:

```lua
--!strict
-- ServerScriptService/Server/Services/CurrencyService.luau
local CurrencyService = {}

local DataService -- resolved in Init to avoid require cycles at load time

function CurrencyService.Init(self: typeof(CurrencyService))
	DataService = require(script.Parent.DataService)
end

function CurrencyService.Start(self: typeof(CurrencyService))
	-- cross-service calls are safe here
end

function CurrencyService.AddCash(self: typeof(CurrencyService), player: Player, amount: number): boolean
	assert(amount == amount and amount >= 0 and amount < math.huge, "invalid amount")
	return DataService:Update(player, function(data)
		data.Cash += math.floor(amount)
	end)
end

return CurrencyService
```

RbxUtil's `Loader` module packages the same idea. For example, `Loader.SpawnAll(Loader.LoadDescendants(folder, Loader.MatchesName("Service$")), "OnStart")` requires every module whose name ends in `Service` and spawns its `OnStart`. The MonzterDev template uses an even simpler loader. It requires every ModuleScript under `Services` (server) or `Controllers` (client) and `task.spawn`s its `OnStart`, with no Init phase. That is fine for small games but gives no ordering guarantee between services.

### 4.2.4 Behaviour on instances: tags and components

Do not put Scripts inside models. Tag instances with **CollectionService** tags and let one component system bind behaviour:

- RbxUtil `Component` (`Component.new({ Tag = "Door", Ancestors = { workspace }, Extensions = {...} })`) creates one object per tagged instance. Its lifecycle methods are `Construct`, `Start` and `Stop`, plus optional `HeartbeatUpdate`, `SteppedUpdate` and `RenderSteppedUpdate`. Default ancestors are `{workspace, game.Players}`. Extensions (`ShouldConstruct`, `Constructing`, `Started` and so on) let you gate construction, for example "only for the local player's own plot".
- A hand-rolled version is about 40 lines: `GetTagged` plus `GetInstanceAddedSignal`/`GetInstanceRemovedSignal`, with a Trove per instance. Listening to the signals also handles streaming; calling `GetTagged` once at start-up does not.

This fits the Blender house rule: imported GLB models (Models of MeshParts) are tagged (`"Door"`, `"Conveyor"`) rather than given scripts, and invisible helpers inside them (prompt anchors, triggers, collision hulls) get their own tags so code does not depend on names.

### 4.2.5 Framework choice

| Option | What it is | Strengths | Weaknesses | Status |
| --- | --- | --- | --- | --- |
| **Plain modules plus a small loader** (4.2.3) | Your own Init/Start loader, RbxUtil Signal, Trove and Component, a thin typed remote wrapper | Full type inference and autocomplete, no magic, smallest surface for an AI agent to misunderstand, easy to test | You write about 150 lines of glue yourself | Recommended baseline |
| **Knit** | Services and controllers, `Knit.CreateService`, `KnitInit`/`KnitStart`, automatic remotes via the `Client` table, Promise-based start | Familiar to many developers, lots of tutorials | **Archived and unmaintained.** The author's reason: it "cannot fully benefit from types, and thus does not have good intellisense." No runtime type checks on remote data. | Do not start new projects on it. Maintain existing Knit games, and migrate gradually. |
| **jecs ECS** | Archetype-based entity component system with first-class relationships (`world:entity()`, `world:component()`, `world:set()`, `world:query(A, B)`) | Very fast. Claims 800,000 entities iterated at 60 fps, typed API, zero dependencies, hooks and signals, relationship pairs and wildcards | Different mental model; UI and Roblox instance code still need bridging; archetype fragmentation if you over-split components; the author warns against overusing hooks and generalising | Active (`package.json` version 0.11.0 at time of reading) **[Version-sensitive]** |
| **Template stacks** (MonzterDev) | Module loader plus ProfileService, Cmdr, Net, Reflex, React, using Aftman, Wally and Rojo | Fast start | Pins older libraries (ProfileService rather than ProfileStore, Aftman rather than Rokit) | Use as a reference, not a dependency |

**Recommendation.**

- **Lower-risk (recommended for most games and for AI-agent-driven development):** plain ModuleScripts with the typed Init/Start loader above. Add RbxUtil `Signal`, `Trove` and `Component` from Wally, ProfileStore for data, and a small typed remote wrapper with server-side validation (4.4, 4.5). Everything type-checks, every file is readable on its own, and there is no framework to go stale.
- **Bold (higher-risk, higher ceiling):** jecs for simulation state, with Blink or Zap generating the network layer from an IDL file. Choose it when the game simulates hundreds or thousands of similar things per frame: tower defence waves, bullet-hell projectiles, swarms, large tycoons with many machines. You gain performance and bandwidth, but onboarding is steeper, you get more generated code to keep in sync, and fewer people (and AI models) know the idioms well. Do not pick it for a simple obby or social hangout.

### 4.2.6 A complete Rojo project layout

```text
my-game/
├─ rokit.toml                 # pinned toolchain (rojo, wally, lune, selene, stylua, luau-lsp)
├─ wally.toml / wally.lock    # package dependencies (commit the lock file)
├─ default.project.json       # Rojo tree (below)
├─ selene.toml  stylua.toml  .luaurc
├─ .github/workflows/ci.yml   # lint, format check, type check, build, deploy (4.10)
├─ assets/
│  ├─ blender/                # .blend sources: every visible model (house rule)
│  ├─ export/                 # GLB files exported headlessly with `blender -b`
│  └─ asset-ids.json          # generated: asset name -> rbxassetid, committed
├─ tools/
│  ├─ blender_exec.py         # Blender Lab MCP bridge (per game)
│  └─ upload-assets.luau      # Lune script: upload GLBs via Open Cloud, write asset-ids.json
├─ src/
│  ├─ first/                  # -> ReplicatedFirst: Loading.client.luau + loading UI
│  ├─ shared/                 # -> ReplicatedStorage.Shared
│  │  ├─ Config/              # Items.luau, Products.luau (dev product/pass ids), Assets.luau (generated from asset-ids.json)
│  │  ├─ Net/                 # Remotes.luau: names, payload types, client wrappers
│  │  ├─ Types.luau           # exported shared types
│  │  └─ Util/                # pure helpers (no side effects at require time)
│  ├─ client/                 # -> ReplicatedStorage.Client
│  │  ├─ Main.client.luau     # the ONLY client entry (RunContext = Client; needs emitLegacyScripts=false)
│  │  ├─ Controllers/         # UIController, InputController, ShopController ...
│  │  └─ Components/          # client components bound to CollectionService tags
│  ├─ server/                 # -> ServerScriptService.Server
│  │  ├─ Main.server.luau     # the ONLY server entry
│  │  ├─ Services/            # DataService, ShopService, ReceiptService, RoundService ...
│  │  ├─ Components/          # server components bound to tags
│  │  └─ Net/                 # RemoteGuard.luau, RateLimiter.luau (server-only)
│  └─ storage/                # -> ServerStorage: server-only templates
├─ Packages/                  # wally "shared" realm  -> ReplicatedStorage.Packages
├─ ServerPackages/            # wally "server" realm  -> ServerScriptService.ServerPackages
└─ tests/                     # Jest-Lua / TestEZ specs, run in CI via Open Cloud Luau execution
```

```json
{
  "name": "my-game",
  "emitLegacyScripts": false,
  "tree": {
    "$className": "DataModel",
    "ReplicatedFirst": { "$path": "src/first" },
    "ReplicatedStorage": {
      "Shared": { "$path": "src/shared" },
      "Client": { "$path": "src/client" },
      "Packages": { "$path": "Packages" },
      "Remotes": {
        "$className": "Folder",
        "PurchaseItem": { "$className": "RemoteEvent" },
        "Effects": { "$className": "UnreliableRemoteEvent" }
      }
    },
    "ServerScriptService": {
      "Server": { "$path": "src/server" },
      "ServerPackages": { "$path": "ServerPackages" }
    },
    "ServerStorage": { "Storage": { "$path": "src/storage" } },
    "Workspace": { "$properties": { "SignalBehavior": "Deferred" } }
  }
}
```

Notes on this layout:

- `"emitLegacyScripts": false` is required for the `ReplicatedStorage` client entry (4.1.3).
- Remotes are declared in the project file, so they exist before any script runs. The alternative is server creation at boot from a list in `Shared/Net`. Never let the client create remotes.
- Rojo syncs code. The world (terrain, Blender imports, placement) usually lives in the place file, edited in Studio. The `Workspace.SignalBehavior` line only matters when Rojo owns the place file (`rojo build`).
- Wally realms: `shared` packages go to `ReplicatedStorage.Packages`, `server` packages (ProfileStore, Lapis) go to `ServerScriptService.ServerPackages`.

Sources: creator-docs:scripting/locations.md, creator-docs:scripting/module.md, creator-docs:projects/external-tools.md, creator-docs:scripting/sync.md, Knit:ARCHIVAL.md, Knit:README.md, Knit:docs/executionmodel.md, Knit:CHANGELOG.md, RbxUtil:README.md, RbxUtil:modules/loader/init.luau, RbxUtil:modules/component/init.luau, jecs:README.md, jecs:how_to/001_hello_world.luau, jecs:how_to/020_queries.luau, jecs:how_to/999_temperance.luau, MonzterDev/Roblox-Game-Template:README.md, MonzterDev/Roblox-Game-Template:default.project.json, MonzterDev/Roblox-Game-Template:src/shared/ModuleLoader.lua, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/external-editors.md

---

## 4.3 Luau standards

### 4.3.1 Type checking modes

Put a mode comment on the first line of every file:

- `--!strict` asserts all types, inferred or annotated. **Use this for all new code.**
- `--!nonstrict` only checks variables you explicitly annotate; everything else is `any`. This is the Studio default.
- `--!nocheck` disables checking. Use it only for vendored third-party files you will not edit.

Type errors show in Studio's Script Editor and the Script Analysis window. In external editors they show through luau-lsp (4.10). CI should fail the build on type errors.

Type features to use:

- Aliases and exports: `export type PlayerData = {...}`, consumed as `Types.PlayerData`. Generics (`<T>`), unions, intersections and optional `T?`.
- Casts with `value :: Type`, allowed only between related types; `:: any` is an escape hatch to use sparingly.
- **`typeof(expr)` in type position** for metatable classes: `type Class = typeof(setmetatable({} :: Fields, Class))`.
- **`unknown`** for untrusted input such as remote arguments. Unlike `any`, it forces refinement with `type()` or `typeof()`.
- **Singleton types** such as `"Manual" | "External" | "Shutdown"` for string enums.

**[Version-sensitive]** Luau has a new type solver that is still being rolled out. The luau-lang site's own examples include workarounds for new-solver bugs. If a type error appears or disappears when toggling solvers in Studio beta settings or luau-lsp, prefer simpler type shapes over clever ones.

### 4.3.2 Naming and style

| Kind | Convention | Example |
| --- | --- | --- |
| Services, modules, classes, types, Roblox instances | PascalCase | `DataService`, `PlayerData`, `RemoteGuard` |
| Locals, functions, methods on your own objects | camelCase (or PascalCase methods for Roblox-style APIs; pick one per project) | `local remainingTime`, `function getProfile()` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_STACK`, `AUTO_SAVE_PERIOD` |
| Private members | leading underscore | `self._connections` |
| Booleans | `is`/`has`/`can` prefix | `isLoaded`, `hasPass` |
| Async (yielding) functions | `Async` suffix, matching Roblox | `loadProfileAsync()` |

The `Async` suffix matters. ProfileStore and Roblox both use it to mean "this yields". Anyone reading `foo()` should be able to assume it does not yield. A function that yields without the suffix is a latent race condition.

Format with **StyLua** and lint with **Selene** (4.10). Prefer string interpolation (`` `{name} has {count}` ``), `if a then b else c` expressions, generalised iteration (`for k, v in tbl do`), `table.freeze` for config, `+=` and `continue`.

### 4.3.3 Error handling

- Wrap every **yielding call to a Roblox web service** in `pcall`. These include DataStores, MemoryStores, MessagingService, MarketplaceService ownership checks, `TeleportAsync`, `HttpService` and `Players:GetUserIdFromNameAsync`. They fail routinely under load.
- Use `xpcall(fn, debug.traceback, ...)` when you need the stack trace for logs. `pcall` throws the trace away.
- Use `assert(cond, msg)` for programmer errors, never for expected runtime failures like a DataStore timeout. `error(message, 2)` blames the caller.
- **Never silently swallow errors.** At minimum `warn` with context (player, key, product).
- Retries use exponential backoff with jitter and a cap, never a tight loop (4.6).
- **[Version-sensitive]** Per the Luau 2025 runtime recap, `pcall` and `xpcall` are now "stackless" in yieldable contexts, so the C-call depth limit no longer applies there.

### 4.3.4 The task library and deprecated scheduling globals

| Legacy (do not use) | Modern | Behaviour |
| --- | --- | --- |
| `wait(n)` | `task.wait(n)` | Yields and resumes on Heartbeat. `task.wait()` with no argument waits one Heartbeat. Returns the actual elapsed time. |
| `spawn(f)` | `task.defer(f)` or `task.spawn(f)` | `task.spawn` resumes immediately, inside the current frame. `task.defer` resumes at the end of the current resumption cycle. |
| `delay(n, f)` | `task.delay(n, f)` | Resumes on Heartbeat after `n` seconds. Returns a thread you can `task.cancel`. |
| `coroutine.wrap(f)()` for fire-and-forget | `task.spawn(f)` | Errors are reported properly with a stack trace. |
| `while true do wait() end` polling | Events, or `RunService.Heartbeat:Connect`, or `task.wait(interval)` with a real interval | |

The legacy globals throttle under load and resume late; Selene flags them. Per-frame work goes on `RunService.Heartbeat` (server logic), `PreRender` (formerly `RenderStepped`; client camera and visuals) or `PreSimulation`/`PostSimulation` (physics-adjacent).

### 4.3.5 Deferred events

**[Version-sensitive]** `Workspace.SignalBehavior` controls when connected handlers run:

- **`Immediate`** runs the handler synchronously inside the code that fired the event.
- **`Deferred`** queues the handler and runs it at the next resumption point. Resumption points include input processing, PreRender, PreAnimation, PreSimulation, PostSimulation, Heartbeat, task resumption, legacy `wait` resumption and BindToClose.
- **`Default`** currently means `Immediate` but is documented to switch to `Deferred` in future. New templates already use `Deferred`, and server authority mode forces it.

Set `Deferred` explicitly now and write code that works under it. Pitfalls:

- **Fire-then-check code breaks.** Setting a property and immediately reading state that a `Changed` handler would have updated returns the old value. The handler has not run yet.
- **Disconnect is not instant for queued invocations.** If an event fired twice before your handler ran, both invocations are queued. Disconnecting inside the first does not stop the second. Use `:Once()` for one-shot handlers.
- **`Destroy` versus `Disconnect`.** Destroying an instance still runs handlers already queued for it, while disconnecting drops them. The `Destroying` event's handlers run after the instance is already destroyed (parent locked).
- **Re-entrancy is capped at 10**: an event that fires itself through handlers stops after 10 nested deferrals.
- **Auto-disconnect on destroy** happens only for non-deferred events.

### 4.3.6 Signals, cleanup and Troves

Every `:Connect` you make on something that outlives the current object is a memory leak unless you disconnect it. The standard tools:

- **Signal** (RbxUtil `Signal`, Wally `sleitnick/signal@2.0.3` at time of reading): a typed pure-Luau event with `Signal.new<T...>()`, `:Connect`, `:Once`, `:Wait`, `:Fire`, `:FireDeferred`, `:DisconnectAll`, `:Destroy` and `Signal.Wrap(rbxScriptSignal)`. Use it for module-to-module events instead of `BindableEvent`, which deep-copies tables, strips metatables and is slower.
- **Trove** (RbxUtil `Trove`, `sleitnick/trove@1.8.0`; Maid and Janitor are older equivalents): a bag of things to clean up, with `Add(obj, cleanupMethod?)`, `Connect`, `Once`, `Clone`, `Construct`, `BindToRenderStep`, `AddPromise`, `Extend()` (child trove), `AttachToInstance(instance)` (clean on destroy), `Clean()` and `Destroy()`.

The rule: **every object with a lifetime owns a Trove**, whether that is a component, a round, a UI screen or a player session. Everything it connects or creates goes into the Trove, and its `Destroy` calls `trove:Destroy()`.

```lua
--!strict
local Players = game:GetService("Players")
local Trove = require(game:GetService("ReplicatedStorage").Packages.Trove)

local sessions: { [Player]: typeof(Trove.new()) } = {}

Players.PlayerAdded:Connect(function(player)
	local trove = Trove.new()
	sessions[player] = trove
	trove:Connect(player.CharacterAdded, function(character)
		-- per-character work; use a child trove that is cleaned on respawn
	end)
end)

Players.PlayerRemoving:Connect(function(player)
	local trove = sessions[player]
	if trove then
		sessions[player] = nil
		trove:Destroy()
	end
end)
```

Other leak sources: per-player tables keyed by `Player` that are never cleared on `PlayerRemoving`; `Instance.new` objects that are never parented and never destroyed while still referenced; connections to `RunService` events that are never disconnected; and closures captured in long-lived tables.

### 4.3.7 Promises

`evaera/roblox-lua-promise` provides Promise/A+-style async values: `Promise.new`, `Promise.try`, `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`, `Promise.some`, `Promise.each`, `Promise.fold`, `Promise.delay`, `Promise.retry`, `Promise.retryWithDelay`, `Promise.fromEvent` and `Promise.promisify`. Instance methods include `:andThen`, `:catch`, `:finally`, `:tap`, `:timeout`, `:cancel`, `:await`, `:expect` and `:now`.

- Promises are useful for **concurrent fan-out with timeouts** (load five things, fail if any takes over 10 s), **cancellation** (stop loading a UI if the player closes it) and **retry** policies.
- Rejections must be handled. An unhandled rejection emits a warning on the next frame. Do not store pre-rejected promises.
- Lapis and Knit expose Promise APIs. ProfileStore uses plain yielding `Async` methods.
- Elsewhere, plain yielding code with `pcall` and `Async` naming is clearer and fully typed.

### 4.3.8 Performance-oriented Luau

- **Native code generation:** put `--!native` at the top of a script, or `@native` on one function, to compile it to machine code. **[Version-sensitive]** It is supported only for server scripts and for client scripts on Android. It helps numeric, table-heavy and `buffer`-heavy code, not code dominated by Roblox API calls. It costs compile time, memory and a per-game native code size limit, so apply it selectively and measure with the Script Profiler (native functions are marked). Check sizes with `debug.dumpcodesize()` in the server-view Command Bar. Annotate parameter types, especially `Vector3`, so the compiler specialises. Avoid `getfenv`/`setfenv`, which de-optimise. Breakpoints disable native execution.
- **[Version-sensitive] New built-ins (Luau 2025 recap):** the `vector` library with fast-call optimisation and constant folding; `math.lerp`, `math.map`, `math.isnan`, `math.isinf` and `math.isfinite`; and `buffer.readbits`/`buffer.writebits`.
- **`buffer`** is the right type for compact binary data: network payloads, voxel or tile maps, replay data. Blink and Zap build on it.
- Cache service references and frequently used functions in locals at the top of the module. Avoid creating closures or tables per frame in hot loops.

Sources: creator-docs:luau/type-checking.md, creator-docs:luau/native-code-gen.md, creator-docs:scripting/scheduler.md, creator-docs:scripting/events/deferred.md, creator-docs:reference/engine/classes/Workspace.yaml, luau-lang/site:src/content/news/2025-12-19-luau-recap-runtime-2025.md, luau-lang/site:src/content/docs/types/overview.md, RbxUtil:modules/signal/init.luau, RbxUtil:modules/trove/init.luau, RbxUtil:README.md, roblox-lua-promise:README.md, roblox-lua-promise:docs/WhyUsePromises.md, roblox-lua-promise:lib/init.lua, ProfileStore:docs/api.md

---

## 4.4 Networking

### 4.4.1 The three remote types

| | `RemoteEvent` | `UnreliableRemoteEvent` | `RemoteFunction` |
| --- | --- | --- | --- |
| Delivery | Guaranteed | Best effort; may drop | Guaranteed request plus response |
| Order | Ordered, **including across different RemoteEvent instances**, per connection and direction | No guarantee | Not ordered relative to RemoteEvents |
| Size limit | Large, but keep small | **Payloads over 1,000 bytes are dropped** | Large |
| Yields caller | No | No | Yes, until the other side returns |
| Use for | All gameplay intents and state changes | High-frequency, replaceable data: cosmetic effects, aim direction, positions you resend every frame | Client asks server for data (`InvokeServer`) when a reply is needed |

Rules:

- **Never use `RemoteFunction:InvokeClient`.** If the client errors, the error is re-thrown on the server. If the client disconnects, it throws. If the client never returns, which an exploiter can arrange, the server thread **yields forever**. If you need data from a client, have the client fire a RemoteEvent and treat the reply as untrusted input.
- `InvokeServer` is fine for request/response ("give me the shop catalogue"), but the server handler must not yield for long, must validate everything and must return quickly.
- There is one in-flight invocation per calling thread, and RemoteFunction calls are not ordered relative to RemoteEvents. If order matters, use one remote type or add sequence numbers.
- **Ordering is about handler start, not completion.** If a handler yields, later events start before it finishes. Handlers that yield must be written to tolerate interleaving, for example with a per-player busy flag or a queue.
- **Throttle:** roughly **500 requests per second per client**, shared by all remotes of the same type. Excess reliable events are delayed, not dropped. Excess unreliable events are dropped.
- **No handler connected:** messages queue (with count and memory limits) and are then discarded with a "Remote event invocation" error. Connect server handlers during Init, before players can fire. On the client, connect handlers before telling the server you are ready.
- The first parameter of every server handler is **always the `Player`** who fired it. That is the only argument you can trust. The client never needs to send its own identity, and you must ignore any player or userId value it sends.

### 4.4.2 What survives serialisation

Arguments are copied, not referenced. When designing payloads:

- **Functions** arrive as `nil`. **Metatables** are stripped, so class instances arrive as plain tables.
- **Mixed tables** (array part plus string keys) are not supported. Arrays with `nil` holes truncate or misbehave.
- **Non-string table keys** become strings in dictionaries. A `{[123] = true}` dictionary arrives keyed by `"123"`.
- **Instances** arrive as references only if the receiver can see them. An instance the client has not replicated, or one in `ServerStorage`, arrives as `nil`. With streaming, a server-sent part reference can be `nil` on the client.
- **Exploiters can send tables shaped like Instances.** Always check `typeof(x) == "Instance"` and then `x:IsA(...)`, never just `x.Name`.
- Numbers can be `NaN`, `inf` or `-inf`, and strings can be megabytes long or invalid UTF-8. Validation is covered in 4.5.

### 4.4.3 Designing the network surface

- **One remote per intent**, named for what the player wants (`RequestPurchase`, `RequestEquip`, `ActivateAbility`), carrying **intent, not outcome**. `ActivateAbility("Dash")` is good. `SetPosition(cframe)`, `AddCoins(500)` and `DealDamage(target, 50)` are wrong: the server decides outcomes. The Boneheads reference project states this as "clients express intent, not outcome".
- **Server-to-client** traffic is state replication (attributes and properties) plus events for things that are not state: "play hit effect here", "show toast". Prefer attributes for anything a late-joining client also needs to see. Remote events are transient, and a client that joins afterwards never gets them.
- **The server is a gatekeeper, not a relay.** If client A's action should affect client B, as with chat, trades, emotes or effects, the server validates A's request and then decides what B sees. Never forward a client's payload verbatim to other clients.
- **Encapsulate.** A shared `Net` module defines remote names and payload types. Server code connects through a guard (4.5.6). Client code calls typed wrapper functions instead of `remote:FireServer` directly.
- **Batch and coalesce** high-frequency updates. Instead of firing one event per changed tile or enemy, accumulate changes during a frame and send one packed event on `Heartbeat`, or every N frames. RbxUtil `TaskQueue` batches tasks that occur in the same execution step. Deltas save bandwidth on reliable remotes only. On unreliable remotes, send absolute values, because a dropped delta corrupts state.
- **Unreliable for continuous streams:** a turret's aim every frame, cosmetic projectile positions. A dropped packet is harmless because the next one supersedes it. Keep each payload under 1,000 bytes and never use unreliable remotes for anything the player paid for or progressed with.

### 4.4.4 Attributes as replicated state

`Instance:SetAttribute(name, value)` on the server replicates to every client that has the instance, and `GetAttributeChangedSignal(name)` lets clients react. This is often the simplest correct networking: a door's `Open` attribute, a plot's `OwnerUserId`, a round's `TimeLeft`.

- Supported types include primitives and common datatypes (`Vector3`, `CFrame`, `Color3`, `UDim2`, `NumberRange` and so on). Instances and tables are not supported.
- **[Version-sensitive] Replication limits** (from the server authority documentation): an attribute replicates only if it is among the **first 64 attributes** on the instance, its name is **at most 50 characters**, and, for strings, its value is **at most 50 characters**.
- Client-set attributes do not replicate to the server. A client changing `OwnerUserId` locally changes only what that client sees.
- Use replicated attributes rather than remotes for puzzle and mechanism state too. The Boneheads project uses `_activated` attributes so late joiners and streamed-in clients see the right state.

### 4.4.5 Generated networking: Blink and Zap

Both are IDL compilers. You describe events in a small schema language, and a CLI generates server and client Luau modules. These modules:

- pack data into `buffer`s, using a fraction of the bandwidth and harder to read with remote-spy tools;
- **validate all incoming data** against the declared types before your code sees it;
- provide fully typed APIs with autocomplete;
- support `Reliable` and `Unreliable` events (unreliable still capped at 1,000 bytes), functions, and `Polling` iteration.

```text
-- Blink (.blink file)                    -- Zap (.zap file; note the "=")
event ActivateAbility {                   event ActivateAbility = {
    From: Client,                             from: Client,
    Type: Reliable,                           type: Reliable,
    Call: SingleAsync,                        call: SingleAsync,
    Data: (u8, vector)                        data: (Ability: u8, Aim: Vector3)
}                                         }
```

- The `Call` modes are `SingleSync`, `ManySync`, `SingleAsync`, `ManyAsync` and `Polling`. Both projects warn that **sync handlers must never yield or error**. A yield causes "undefined and game-breaking behaviour", and an error in Zap drops the packet. Default to `SingleAsync` or `ManyAsync`.
- **[Version-sensitive] Status:** Zap's main branch is undergoing a rewrite, and `0.6.x` is maintained on a separate branch. Blink is released through GitHub releases and has a Studio plugin. Pin exact versions and commit the generated files, or generate them in CI.
- **Validation is structural only.** Blink and Zap guarantee that a `u8` is a `u8`. They do not check that the ability is unlocked, off cooldown or affordable. Game-rule validation (4.5) is still mandatory.
- **When it is worth it:** many players, high-frequency updates, or bandwidth-sensitive genres such as shooters, large simulations and ECS games. For a typical simulator or obby with a dozen remotes fired at human speed, plain RemoteEvents plus a typed wrapper and a guard are simpler and good enough.

As Knit's archival note says, every networking library wraps the same three remote types, and Luau types are not enforced at runtime. Runtime checks on network input are required whichever library you use.

### 4.4.6 Testing the network

Use **Server & Clients** playtests (up to 8 clients), the **Network Simulator** (latency, jitter, packet loss; essential for unreliable remotes and prediction), and the Developer Console's network stats while firing your heaviest event at its real rate. Scripted multi-client tests with `StudioTestService` are covered in 4.10.2.

Sources: creator-docs:scripting/events/remote.md, creator-docs:reference/engine/classes/RemoteEvent.yaml, creator-docs:reference/engine/classes/UnreliableRemoteEvent.yaml, creator-docs:reference/engine/classes/RemoteFunction.yaml, creator-docs:scripting/security/client-server-boundary.md, creator-docs:scripting/attributes.md, creator-docs:projects/server-authority/index.md, creator-docs:resources/boneheads/server-authority.md, creator-docs:studio/testing-modes.md, creator-docs:reference/engine/classes/StudioTestService.yaml, Blink:README.md, Blink:docs/pages/getting-started/2-introduction.mdx, Blink:docs/pages/language/5-events.mdx, Zap:README.md, Zap:docs/intro/what-is-zap.md, Zap:docs/config/events.md, Knit:ARCHIVAL.md, RbxUtil:README.md



This file continues Section 4 (4.5–4.7). The snippets use the service layout and loader from 4.2.

---

## 4.5 Security

### 4.5.1 The threat model: what an exploiting client can always do

Assume every player runs arbitrary code on their own client. Per the security-tactics page, they can:

- **Read all replicated code.** LocalScripts and every ModuleScript in replicated containers can be decompiled, including disabled scripts. Secrets, loot tables, admin lists and server logic placed there are public.
- **Fully control their character and every part they own.** They can teleport, fly, noclip, change `WalkSpeed` and `JumpPower` locally (undetectable by reading the property on the server), play any animation, and send `NaN` or infinite CFrames and velocities. They can also fling other players through physics contact.
- **Fire `Touched` for any part they own** even when nothing touched, and suppress touches they do not want.
- **Trigger `ProximityPrompt`s, `ClickDetector`s and `DragDetector`s from any distance.** Prompt events can fire even when `Enabled` is false. Only `Triggered` gets a server-side distance check, and `HoldDuration` can be bypassed. `ClickDetector` has no server checks at all. `DragDetector` checks only `Enabled` and `PermissionPolicy`. A `DragDetector` with `RunLocally = true` replicates nothing.
- **Fire any remote, with any arguments, at any rate,** including remotes your UI never fires and argument types your code never sends.
- **Change their local DataModel silently.** UI, local properties and local-only instances are theirs.
- **Teleport themselves to any place in your universe,** unless place access is restricted (4.5.9).

What they **cannot** do: read or change anything in `ServerScriptService` or `ServerStorage`, change server-side properties directly, or call server-only APIs (DataStores, MarketplaceService grants, BanAsync).

For each new feature, the docs suggest asking: *What happens if this remote is fired 1,000+ times per second? With garbage arguments? With another player's objects? From across the map? While dead? During a round transition?*

### 4.5.2 Server authority: intent in, outcome out

The core rule is **"clients express intent, not outcome"**. The client says what the player is trying to do. The server checks whether that is allowed and computes the result.

| Wrong (client decides outcome) | Right (client sends intent) |
| --- | --- |
| `GiveCoins:FireServer(500)` | Server awards coins when it observes the collect condition |
| `DealDamage:FireServer(target, 35)` | `Attack:FireServer(aimDirection)`. The server raycasts from the server-side character position, applies weapon stats and cooldowns, and computes damage |
| `BuyItem:FireServer("Sword", 0)` (price from client) | `BuyItem:FireServer("Sword")`. Price comes from the server's catalogue |
| `CompleteObby:FireServer()` | Server tracks sequential checkpoint touches and a plausible minimum time |
| `SetPetEquipped:FireServer(petInstance)` | `EquipPet:FireServer(petUid)`. Server looks up the uid in **this player's** inventory |

**Defensive design** removes the incentive before validation is needed: do not reward cheaply faked actions (no points for spawn-protected kills), make progress sequential (checkpoint N counts only after N−1), compute hits on the server, and never let one client's request change another client's state without a server decision.

### 4.5.3 Validation layers

Validate in this order, cheapest first. Reject silently: no error message back to the client, which only helps attackers tune their payloads.

1. **Rate.** Is this player within budget for this action (4.5.4)?
2. **Context and permission.** Is the player alive, in the right round phase, not stunned, the owner of this plot, an admin for admin remotes?
3. **Type and shape.** Check `type(x) == "number"` or `"string"`, `typeof(x) == "Vector3"` and so on. Check the argument count. For tables: expected keys only, bounded size and depth, no metatables expected.
4. **Value.**
   - Numbers: `NaN` passes `type(x) == "number"` and **fails every comparison**, so negated range checks (`if x < 0 or x > MAX then reject`) let it through. Check finiteness first: `x == x and x ~= math.huge and x ~= -math.huge`, or `math.isfinite(x)` **[Version-sensitive: Luau 2025]**.
   - Then check ranges, integers (`x == math.floor(x)`), and enum membership against an allowlist.
   - Strings: cap the length before anything else, check `utf8.len(s) ~= nil` (valid UTF-8, also required for DataStore saves), and use allowlists for ids.
5. **Instances.** Check `typeof(x) == "Instance"`, because exploiters can send tables shaped like instances. Then check `x:IsA("BasePart")`, `x:IsDescendantOf(expectedFolder)`, ownership (`x:GetAttribute("OwnerUserId") == player.UserId`) and distance from the **server's** view of the character.
6. **Game rules.** Cooldown elapsed (server clock), item owned, enough currency, target in line of sight, plausible timing.

Only after all of that, perform the action. If a handler yields between a check and the effect (for example a DataStore call), take a per-player lock first, or re-check after the yield.

### 4.5.4 Rate limiting

The engine throttle (about 500 requests/s per client per remote type, 4.4.1) protects Roblox, not your game. Add per-player, per-action limits:

- **Token bucket** (the official sample): `capacity` tokens refilled at a steady rate, allowing bursts but capping the sustained rate. Clear buckets on `PlayerRemoving`.
- Pick limits from real behaviour: a button a human presses 5 times per second gets capacity 10, refill 5/s. Expensive actions (DataStore, raycast-heavy, purchase-adjacent) get tighter limits and a per-player busy lock.
- **Escalate gradually:** drop silently, then log, then flag. Do not kick on the first violation; lag spikes bunch legitimate calls.

### 4.5.5 Movement and combat checks

**Movement** (without server authority mode):

- Run a staggered 1–2 Hz loop per player. Compare XZ displacement against `WalkSpeed × elapsed × tolerance` (tolerance at least 1.5). Accumulate violations in a **leaky bucket** so one spike triggers nothing.
- Exempt server teleports, knockback, vehicles, launch pads and respawns with a "grace until" timestamp whenever the server moves a character.
- Check sustained airtime separately for flying. Raycast between consecutive positions for noclip. The check only works where visible models have real collision, one more reason for the house rule.
- Rubber-band to the last valid position rather than kicking, until violations are sustained.

**Combat:**

- The client sends the aim direction or target and a timestamp. The server verifies the cooldown, recomputes the ray from the **server's** character position, and allows a small lag tolerance. The best-practices skill suggests about 10–15 studs of extra range and a 300–500 ms rewind cap as starting heuristics (a community heuristic, not official).
- Reject a claimed muzzle origin that is far from the server's root part position.
- Never apply damage from `Touched` on a client-owned weapon without a server-side distance check and a per-target debounce.
- Parallel Luau is a good fit for validating many characters' raycasts per frame (4.9).

### 4.5.6 Reusable remote guard and rate limiter

This server-only module combines rate limiting, structural validation and violation counting. Connect every client-to-server remote through it. A rejected call is dropped silently and counted, never echoed.

```lua
--!strict
-- ServerScriptService/Server/Net/RemoteGuard.luau  (server-only; never replicate this)
local Players = game:GetService("Players")

--------------------------------------------------------------------------
-- Token bucket rate limiter (per player)
--------------------------------------------------------------------------
type Bucket = { tokens: number, updatedAt: number }

local RateLimiter = {}
RateLimiter.__index = RateLimiter

export type RateLimiter = typeof(setmetatable(
	{} :: { capacity: number, refillPerSecond: number, buckets: { [Player]: Bucket } },
	RateLimiter
))

function RateLimiter.new(capacity: number, refillPerSecond: number): RateLimiter
	local self = setmetatable({
		capacity = capacity,
		refillPerSecond = refillPerSecond,
		buckets = {},
	}, RateLimiter)
	Players.PlayerRemoving:Connect(function(player)
		self.buckets[player] = nil
	end)
	return self
end

function RateLimiter.allow(self: RateLimiter, player: Player, cost: number?): boolean
	local now = os.clock()
	local bucket = self.buckets[player]
	if bucket == nil then
		bucket = { tokens = self.capacity, updatedAt = now }
		self.buckets[player] = bucket
	end
	bucket.tokens = math.min(self.capacity, bucket.tokens + (now - bucket.updatedAt) * self.refillPerSecond)
	bucket.updatedAt = now
	local price = cost or 1
	if bucket.tokens < price then
		return false
	end
	bucket.tokens -= price
	return true
end

--------------------------------------------------------------------------
-- Validation helpers (all take `unknown`, so callers must refine)
--------------------------------------------------------------------------
local Check = {}

function Check.finiteNumber(value: unknown, min: number, max: number): boolean
	if type(value) ~= "number" then
		return false
	end
	-- NaN fails every comparison, so test finiteness before ranges.
	if value ~= value or value == math.huge or value == -math.huge then
		return false
	end
	return value >= min and value <= max
end

function Check.integer(value: unknown, min: number, max: number): boolean
	return Check.finiteNumber(value, min, max) and (value :: number) % 1 == 0
end

function Check.string(value: unknown, maxLength: number): boolean
	return type(value) == "string" and #value <= maxLength and utf8.len(value) ~= nil
end

function Check.oneOf(value: unknown, allowed: { [string]: any }): boolean
	return type(value) == "string" and allowed[value] ~= nil
end

function Check.vector3(value: unknown, maxMagnitude: number): boolean
	if typeof(value) ~= "Vector3" then
		return false
	end
	local v = value :: Vector3
	return Check.finiteNumber(v.X, -maxMagnitude, maxMagnitude)
		and Check.finiteNumber(v.Y, -maxMagnitude, maxMagnitude)
		and Check.finiteNumber(v.Z, -maxMagnitude, maxMagnitude)
end

function Check.instanceIn(value: unknown, className: string, ancestor: Instance): boolean
	-- typeof (not type) rejects tables that merely look like instances
	return typeof(value) == "Instance"
		and (value :: Instance):IsA(className)
		and (value :: Instance):IsDescendantOf(ancestor)
end

--------------------------------------------------------------------------
-- Guarded connection
--------------------------------------------------------------------------
export type GuardOptions = {
	name: string,
	limiter: RateLimiter,
	argCount: number,
	validate: (player: Player, ...unknown) -> boolean,
}

local VIOLATION_LOG_THRESHOLD = 20
local violations: { [Player]: number } = {}
Players.PlayerRemoving:Connect(function(player)
	violations[player] = nil
end)

local function recordViolation(player: Player, remoteName: string, reason: string)
	local count = (violations[player] or 0) + 1
	violations[player] = count
	if count == VIOLATION_LOG_THRESHOLD then
		-- Feed your server-side detection / review pipeline here (4.5.7). Do not kick on this alone.
		warn(`[RemoteGuard] {player.UserId} reached {count} violations (latest: {remoteName}/{reason})`)
	end
end

local RemoteGuard = { RateLimiter = RateLimiter, Check = Check }

function RemoteGuard.connect(
	remote: RemoteEvent,
	options: GuardOptions,
	handler: (player: Player, ...any) -> ()
): RBXScriptConnection
	return remote.OnServerEvent:Connect(function(player: Player, ...: unknown)
		if not options.limiter:allow(player) then
			recordViolation(player, options.name, "rate")
			return
		end
		if select("#", ...) ~= options.argCount then
			recordViolation(player, options.name, "argCount")
			return
		end
		local ok, valid = pcall(options.validate, player, ...)
		if not ok or valid ~= true then
			recordViolation(player, options.name, "invalid")
			return
		end
		handler(player, ...)
	end)
end

return RemoteGuard
```

Usage, for a shop purchase that spends soft currency:

```lua
--!strict
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RemoteGuard = require(script.Parent.Parent.Net.RemoteGuard)
local Items = require(ReplicatedStorage.Shared.Config.Items) -- { [string]: { Price: number } }

local busy: { [Player]: true } = {}

RemoteGuard.connect(ReplicatedStorage.Remotes.PurchaseItem, {
	name = "PurchaseItem",
	limiter = RemoteGuard.RateLimiter.new(5, 1), -- burst 5, then 1 per second
	argCount = 1,
	validate = function(_player, itemId)
		return RemoteGuard.Check.oneOf(itemId, Items)
	end,
}, function(player, itemId: string)
	if busy[player] then
		return
	end
	busy[player] = true
	-- Price and ownership come from server data only. ShopService.buy must not trust the client.
	local ok, err = pcall(ShopService.Buy, ShopService, player, itemId)
	busy[player] = nil
	if not ok then
		warn(`[Shop] {player.UserId} {itemId}: {err}`)
	end
end)
```

Here `ShopService` is resolved in `Init`, as in 4.2.3. Clear the `busy` entry on `PlayerRemoving` too. For `RemoteFunction`s, use the same pattern with `OnServerInvoke` (one assignment only; the last one wins silently), and return a small result table such as `{ ok = false }` for rejected calls.

### 4.5.7 Server-side detection, honeypots and consequences

Validation stops bad requests. **Detection** finds bad actors who stay just inside the limits.

- **Heuristics:** completion times below a designer-set floor, gain per minute above the theoretical maximum, inhumanly regular cadence, impossible combinations (owning an item never sold). Combine signals into a **suspicion score** rather than acting on any one.
- **Honeypots.** A remote your client never fires (a tempting `GiveAdminCash`) catches remote-spam scripts. The best-practices skill warns against auto-punishing honeypot hits without long observation, because a false positive is a banned paying player.
- **Consequence ladder:** silent logging → quiet mitigation (reject, rubber-band, zero rewards) → temporary restrictions → kick → ban. **Delay visible consequences.** An immediate ban tells the exploiter exactly which check fired.
- **Bans:** `Players:BanAsync(config)` (server-only, gated by `Players.BanningEnabled`). Its fields:
  - `UserIds`
  - `Duration` in seconds (`-1` = permanent)
  - `DisplayReason`, shown to the user, at most 400 characters and text-filtered
  - `PrivateReason`, at most 1,000 characters, never sent to the client
  - `ExcludeAltAccounts`; alt propagation is **on** by default
  - `ApplyDeviceBlock`, which blocks the device for 24 hours
  - `ApplyToUniverse`, default true; a ban in the start place effectively excludes the user from the whole universe

  Use `Players:GetBanHistoryAsync` to escalate durations and `Players:UnbanAsync` for appeals. Publish your rules and give players a way to appeal.
- **[Version-sensitive] Device Trust.** `Player.DeviceTrustLevel` takes the values `Pending`, `Unknown`, `None`, `Standard` and `Full`. Register one `IntegrityService.EvaluatePlayerDeviceTrust` callback per place. It runs after `PlayerAdded`, can return `{ Action = Enum.PlayerDeviceTrustDecision.Reject, Message = ... }`, and times out after about 10 s, after which the player is accepted. At the time of writing, attestation exists only on Android, Chromebook and Quest. Web reports `None`, other platforms `Unknown`, and Studio is always `Pending`. Read it on the server only and treat `Pending` as untrusted. Use it as a per-feature policy input (for example "trading requires Standard or better on platforms that support it"), never as a blanket gate that locks out unsupported platforms.

### 4.5.8 Network ownership exploits

Because owners simulate their own assemblies (4.1.4), ownership is a power you hand out:

- **Characters:** always client-owned. Movement validation (4.5.5) is the only defence outside server authority mode.
- **Unanchored props near players** become client-owned automatically. An exploiter can carry, fling or delete a client-owned crate, a ball or a vehicle someone else is driving. For gameplay-critical physics objects (a soccer ball's position decides the score), either `SetNetworkOwner(nil)` and accept some jitter, or validate outcomes on the server (the goal counts only if the server's ball state crossed the line). Server authority mode is the long-term fix.
- **Prompts and detectors on unanchored parts** can be dragged to the exploiter, which defeats distance checks. Anchor interactable anchors, or parent the prompt to an invisible, anchored helper part. That is allowed under the house rules as a technical helper.
- **`NaN` or huge CFrames and velocities** on owned parts can crash or fling nearby physics. Server-side sanity loops should reset assemblies with non-finite positions.

### 4.5.9 Access control and code exposure

- Clients can teleport to **any** place in your universe unless restricted. In Game Settings, set sub-places that need a gate (VIP areas, matches) to **"Secure within universe only"**, so only server-initiated `TeleportAsync` can get players there. The options are Fully open, Limited to same universe and Secure within universe only. Default-deny restricted places.
- Keep development and test places in **separate private universes**, not as unlisted sub-places of the live game.
- Never ship a module that mixes server and client logic and replicates. Split it, so `ServerScriptService` holds the server half.
- Do not rely on obscure names. Remote names, folder names and "hidden" admin commands are all readable.

### 4.5.10 Third-party code and backdoors

The house rule (only Blender-made models) removes the most common backdoor vector, free models from the Creator Store carrying hidden scripts. It does not remove plugins, packages, or community libraries copied from the toolbox.

- Get libraries from **Wally or Git with pinned versions**, not toolbox copies. Read diffs when you upgrade.
- Search the place for every `Script`, `LocalScript` and `ModuleScript` after any insert. Look for `require(<number>)` (remote module loading), `getfenv` and `setfenv`, `loadstring`, string obfuscation, and code pushed far to the right with whitespace.
- Keep `ServerScriptService.LoadStringEnabled` off.
- **[Version-sensitive] Script Capabilities** (documented as "experimental and available as a client beta"): set `Workspace.SandboxedInstanceMode = Experimental`, then mark untrusted containers `Sandboxed = true` with minimal `Capabilities`. Never grant `Network`, `DataStore`, `AssetRequire`, `CapabilityControl` or `LoadString` to third-party code.

### 4.5.11 HttpService and secrets

- HTTP requests are **server-only** and need **Allow HTTP Requests** enabled. Plain HTTP requests are limited to **500 per minute per server**. Open Cloud calls from inside the game have a separate **2,500 per minute per server** budget and accept only the `x-api-key` and `content-type` headers. HTTPS only. Ports below 1024 are blocked except 80 and 443, port 1194 is blocked, and path parameters may not contain `..`.
- **Secrets store:** up to **500 secrets per game**, each up to **1,024 characters**, scoped to a domain (never use `*`). `HttpService:GetSecret(name)` returns a `Secret` object, which prints as `Secret(name)` and cannot be read back as a string. It supports `AddPrefix` and `AddSuffix` (for `Bearer ` and so on) and can go in the URL or headers, **never the body**. Secrets resolve only on live servers and in collaborative Team Test. For solo Studio testing, add **Local Secrets** in Experience Settings.
- Never put API keys, webhook URLs or tokens in any script, attribute, config module or git repository. A Discord webhook URL in a ModuleScript is a public spam endpoint. In CI (4.10), Open Cloud keys go in the CI secret store, are scoped to one universe and the minimum permissions, and are rotated on any leak.
- **Text filtering:** any player-written text shown to other players must be filtered on the server through `TextService:FilterStringAsync` and then the appropriate `Get...Async` method. If filtering fails, show nothing rather than the raw text.

Sources: creator-docs:scripting/security/security-tactics.md, creator-docs:scripting/security/client-server-boundary.md, creator-docs:scripting/security/defensive-design.md, creator-docs:scripting/security/network-ownership.md, creator-docs:scripting/security/server-side-detection.md, creator-docs:scripting/security/access-control.md, creator-docs:scripting/security/third-party-vulnerabilities.md, creator-docs:scripting/security/device-trust.md, creator-docs:scripting/capabilities.md, creator-docs:physics/network-ownership.md, creator-docs:reference/engine/classes/Players.yaml, creator-docs:cloud-services/http-service.md, creator-docs:cloud-services/secrets.md, creator-docs:resources/boneheads/server-authority.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/security.md, gamedev-skills/awesome-gamedev-agent-skills:skills/other-engines/roblox-networking/SKILL.md

---

## 4.6 Data

### 4.6.1 Choosing a storage service

| Need | Use | Why |
| --- | --- | --- |
| Player progress, inventory, currency, purchase history | **Standard data store** through a session-locking library (ProfileStore or Lapis) | Durable, versioned, one key per player |
| Global leaderboards, "top 100" | **Ordered data store** (integers only), cached and refreshed periodically | Sorted queries |
| Matchmaking queues, live server lists, cross-server locks, trade escrow, short-lived global state | **MemoryStore** (sorted map, queue, hash map) | Fast, expiring (max 45 days), high throughput |
| "Something happened" broadcasts (global announcements, shutdown notices, cross-server chat hints) | **MessagingService** | Best-effort pub/sub, about 1 KB messages |
| Live feature flags and tuning numbers | **Configs** (read-only at runtime; changes deploy over about 5 minutes) | No republish needed |
| API keys and webhook tokens | **Secrets store** (4.5.11) | Never in code |
| Per-server caches and session state | **Luau tables** in a server module | Free and instant, gone on shutdown |

All cloud services are **server-only**. Studio needs **Enable Studio Access to API Services** to use them. Roblox recommends a **separate test game** for Studio sessions so testing never touches live player data. MemoryStore data in Studio is isolated from production automatically.

### 4.6.2 DataStore limits (exact)

**[Version-sensitive]** These are the figures in `creator-docs:cloud-services/data-stores/error-codes-and-limits.md` at time of writing.

- **Sizes:**
  - data store name, key name and scope: 50 characters each
  - value: 4,194,304 characters (4 MB) of serialised JSON per key
  - metadata: key 50 characters, value 250 characters, 300 characters total
- **Experience-level limits, per minute.** These are shared with Open Cloud calls against the same experience.

  | Request type | Standard and ordered (same figures) |
  | --- | --- |
  | Read | 300 + CCU×40 |
  | Write | 300 + CCU×20 |
  | List | 300 + CCU×2 |
  | Remove | 300 + CCU×40 |

  `UpdateAsync` consumes **both** a read and a write.
- **Per-server default limits, per minute.** These can be adjusted with `DataStoreService:SetRateLimitForRequestType` and inspected with `GetRequestBudgetForRequestType`. There is a start-up burst allowance.

  | Request type | Standard | Ordered |
  | --- | --- | --- |
  | Read | 60 + players×40 | 60 + players×40 |
  | Write | 60 + players×40 | 30 + players×5 |
  | List | 5 + players×2 | 5 + players×2 |
  | Remove | 60 + players×40 | 30 + players×5 |

- **Per-key throughput,** over a rolling 60 seconds: reads 25 MB/min, writes 4 MB/min. Each request is rounded up to the next KB.
- **Request queues:** each request type queues up to 30 requests. Beyond that, requests fail immediately with codes 301–306.
- **Storage quota:** 500 MB + 1 MB × lifetime users. It is measured on the **compressed latest version** of each key, so do not pre-compress data yourself. Studio Run mode has separate static limits.

**Key error codes** (log the code; it tells you what to fix):

| Code | Meaning | Action |
| --- | --- | --- |
| 101 / 102 | Key name empty / too long | Fix the key builder |
| 103 / 104 | Value not allowed / can't store (functions, Instances, userdata, cycles, mixed tables, NaN) | Fix serialisation (4.6.3) |
| 105 | Value too large | Split data or trim history |
| 106 / 107 | Ordered `GetSortedAsync` argument errors (page size must be 1–100) | Fix the query |
| 301–306 | Throttled: the queue is full | Back off, reduce frequency, check budgets |
| 401 / 402 | Request during shutdown | Expected in `BindToClose`; save earlier |
| 403 | No Studio API access | Enable it, ideally in a test game |
| 404, 501–505 | Internal errors (502 = request rejected) | Retry with backoff; **verify** before assuming failure |
| 509 | Personal RCC | Not available in personal servers |
| 511–513 | Metadata or user id errors | Fix metadata size or user id list |

**[Version-sensitive]** Newer, more specific throttle names have been added: `StandardReadExperienceThrottled`, `StandardWriteExperienceThrottled`, `StandardListExperienceThrottled`, `StandardRemoveExperienceThrottled`, `GameServerThrottled`, their `Ordered*` equivalents, `KeyThrottled` and `DatastoreThrottled`.

**A failed write may have succeeded.** After a timeout or internal error, confirm with an uncached read before refunding or retrying something non-idempotent. Use `DataStoreGetOptions.UseCache = false`, because `GetAsync` normally serves a 4-second cache.

### 4.6.3 DataStore practices that prevent data loss

- **One key per player** with a static pattern such as `Player_{UserId}`. Use few data stores. Prefer prefixes inside a store to many stores. **Never change the key pattern** of a live game without a migration that reads the old key.
- **[Version-sensitive] Identity:** the engine has added `Player.User` and a `User` datatype, described as "the standard way to identify users in new code". The data store documentation still uses `Player.UserId` for keys, and RTBF templates use a `{UserId}` token. Keep numeric `UserId`-based keys for persistence.
- **Load once, buffer in memory, save periodically.** Never read the DataStore during gameplay.
- **Prefer `UpdateAsync` over `SetAsync`** for anything multiple servers could write. The transform function **must not yield**, may run more than once, and returning `nil` cancels the write. **Metadata and user ids are not preserved automatically.** Pass them again on every write or they are lost.
- **Retries:** exponential backoff with jitter (for example 1 s, 2 s, 4 s, 8 s, each ± random 25 %), capped at 3–5 attempts, and **in order per key**, so an older save never lands after a newer one.
- **Stagger periodic work.** Autosave loops start at a random offset, so servers launched together do not save together.
- **Serialisable data only:**
  - plain tables, either a pure array or all string keys, never mixed;
  - no `nil` holes in arrays;
  - no Instances, `Vector3`, `CFrame` or `Color3` (store components or ids);
  - no `NaN` or `inf`;
  - valid UTF-8 strings (`utf8.len`);
  - no cycles.

  Cap the length of player-supplied strings and the count of player-supplied keys before they ever enter saved data.
- **Versioning:** a version is created from the first write per key per UTC hour. Later writes in the same hour overwrite it. Overwritten versions expire after 30 days. `ListVersionsAsync` and `GetVersionAsync` are your backup and restore tools. Ordered data stores have **no** versioning or metadata.
- **Hot keys:** shard read-heavy shared keys, for example a global config, by hashing `game.JobId` to one of N copies.
- **Tooling:** the Creator Hub Data Stores Manager inspects and edits keys; the Observability dashboard shows throttling and errors; deleted stores keep a 30-day restore buffer. DataStore2 is legacy.
- **Trade and dupe safety:** never move items between two players with two independent saves. Use session-locked profiles on the same server, check `IsActive()` on both, mutate both with no yield, then save both. Cross-server trades use an escrow record with a unique trade id and idempotent completion. Session locking blocks the classic "trade, then leave before save" dupe.

### 4.6.4 Session locking and ProfileStore

**Why session locking matters:** without it, a fast server-hopper loads on server B before server A's final save lands, causing rollback or duplication. Roblox's purchasing guide sample stores a lock GUID with expiry in key metadata via `UpdateAsync` and refreshes it on autosave. ProfileStore and Lapis do this for you.

**ProfileStore** (by MadStudio, successor to ProfileService) is the community default:

- `ProfileStore.New(storeName, template)` creates the store. `store:StartSessionAsync(key, { Cancel = fn })` acquires the session and returns a `Profile`, or `nil` if a session could not be started.
- **Session conflict handling** uses these constants from the source; adjust them with `ProfileStore.SetConstant`:
  - `AUTO_SAVE_PERIOD = 300` seconds
  - `FIRST_LOAD_REPEAT = 5` and `LOAD_REPEAT_PERIOD = 10` seconds between reads while another server holds the session
  - `SESSION_STEAL = 40` seconds before the waiting server takes the session
  - `ASSUME_DEAD = 630` seconds without updates before an active session is treated as belonging to a crashed server
  - `START_SESSION_TIMEOUT = 120` seconds, disabled when you pass a `Cancel` function
- When another server requests the session, the current holder makes a final save and releases. **Never use `{ Steal = true }`** for normal loading; it bypasses the lock and exists for debugging.
- `profile.Data` is saved as long as `profile:IsActive()` is true. **The guarantee does not survive a yield.** Check `IsActive()` and then write immediately. For trades, check both profiles and write both without yielding.
- `profile:EndSession()` performs the final save and releases the lock. Always call it on `PlayerRemoving`. ProfileStore also ends all sessions itself on server shutdown (the `OnLastSave` reason is `"Shutdown"`), so **do not add your own BindToClose save loop** on top of it.
- **Signals:**
  - `OnSave`: fires before each save; last chance to write derived fields.
  - `OnLastSave(reason)`, where reason is `"Manual"`, `"External"` or `"Shutdown"`: use it for logout penalties. It may never fire if the server crashes.
  - `OnSessionEnd`: no more writes after it; kick the player.
  - `OnAfterSave(lastSavedData)`: `profile.LastSavedData` now reflects what is stored, which makes it ideal for purchase confirmation.
- **Module signals:** `ProfileStore.OnError(message, storeName, key)`, `OnOverwrite`, `OnCriticalToggle` and `IsCriticalState`, which is true after excessive DataStore failures; use it to warn players. `DataStoreState` is one of `"NotReady"`, `"NoInternet"`, `"NoAccess"` or `"Access"`.
- **Other API:**
  - `profile:Reconcile()` fills in template fields missing from old profiles.
  - `profile:AddUserId(userId)` associates the user id for GDPR and RTBF.
  - `profile.RobloxMetaData` holds key metadata (300-character total limit).
  - `profile:Save()` triggers an immediate save, costing one `UpdateAsync`; reserve it for purchases.
- **Offline delivery:** `store:MessageAsync(key, message)` delivers a message to a profile whether or not it is loaded, at the cost of two `UpdateAsync` calls. The receiver handles it with `profile:MessageHandler(function(message, processed) ... processed() end)`. Messages persist until `processed()` is called, up to `MAX_MESSAGE_QUEUE = 1000`. This is the right tool for **gifting paid items to offline friends**. For non-critical notifications, MessagingService is cheaper.
- **Read-only access:** `store:GetAsync(key, version?)` loads a profile without a session. Use it for admin tools and support lookups. Edit the result and write it with `profile:SetAsync()` only for support fixes; that ends any active session.
- **`store.Mock`** mirrors the API against a throwaway in-memory store. Use it for unit tests, or in Studio when API access is on but you must not touch live keys.

### 4.6.5 ProfileStore load and release, with schema migration

This module plugs into the loader from 4.2.3 (`Init` and `PlayerAdded` hooks).

```lua
--!strict
-- ServerScriptService/Server/Services/DataService.luau
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ServerScriptService = game:GetService("ServerScriptService")

local ProfileStore = require(ServerScriptService.ServerPackages.ProfileStore)

local SCHEMA_VERSION = 3
local USE_MOCK_IN_STUDIO = true -- or point Studio at a separate test universe (Roblox's recommendation)

export type PlayerData = {
	SchemaVersion: number,
	Cash: number,
	Inventory: { [string]: number }, -- itemId -> count
	Boosts: { [string]: number }, -- boostId -> expiry (os.time, UTC seconds)
	Entitlements: { [string]: boolean }, -- perks granted by gifts/products, not real pass ownership
	PurchaseIds: { string }, -- recent processed receipts (capped, see 4.7)
}

local TEMPLATE: PlayerData = {
	SchemaVersion = SCHEMA_VERSION,
	Cash = 0,
	Inventory = {},
	Boosts = {},
	Entitlements = {},
	PurchaseIds = {},
}

-- MIGRATIONS[n] upgrades saved data from version n to n + 1. Never edit a shipped step.
local MIGRATIONS: { [number]: (data: { [string]: any }) -> () } = {
	[1] = function(data) -- v1 -> v2: "Coins" renamed to "Cash"
		data.Cash = (data.Cash or 0) + (data.Coins or 0)
		data.Coins = nil
	end,
	[2] = function(data) -- v2 -> v3: inventory array of ids -> counts
		local counts: { [string]: number } = {}
		for _, itemId in data.Inventory or {} do
			counts[itemId] = (counts[itemId] or 0) + 1
		end
		data.Inventory = counts
	end,
}

local store = ProfileStore.New("PlayerData", TEMPLATE)
if USE_MOCK_IN_STUDIO and RunService:IsStudio() then
	store = store.Mock :: any
end

type Profile = typeof(store:StartSessionAsync(""))

local profiles: { [Player]: Profile } = {}
local failed: { [Player]: true } = {}

local function migrate(data: { [string]: any }): boolean
	local version = if type(data.SchemaVersion) == "number" then data.SchemaVersion else 1
	if version > SCHEMA_VERSION then
		return false -- written by a newer server build; this server must not touch it
	end
	while version < SCHEMA_VERSION do
		local step = MIGRATIONS[version]
		if step then
			step(data)
		end
		version += 1
	end
	data.SchemaVersion = SCHEMA_VERSION
	return true
end

local DataService = {}

function DataService:Init()
	Players.PlayerRemoving:Connect(function(player)
		failed[player] = nil
		local profile = profiles[player]
		if profile ~= nil then
			profiles[player] = nil
			profile:EndSession() -- final save + releases the session lock
		end
	end)
end

function DataService:PlayerAdded(player: Player)
	local profile = store:StartSessionAsync(`Player_{player.UserId}`, {
		Cancel = function()
			return player.Parent ~= Players -- stop retrying if the player already left
		end,
	})

	if profile == nil then
		failed[player] = true
		player:Kick("We couldn't load your data. Please rejoin in a moment.")
		return
	end

	-- Migrate BEFORE Reconcile: Reconcile would stamp TEMPLATE.SchemaVersion onto old data.
	if not migrate(profile.Data :: any) then
		failed[player] = true
		profile:EndSession() -- data untouched, so the final save is a no-op rewrite
		player:Kick("This server is out of date. Please rejoin to get the latest version.")
		return
	end
	profile:AddUserId(player.UserId) -- GDPR / right-to-erasure association
	profile:Reconcile() -- fill fields added to TEMPLATE since this profile was last saved

	profile.OnSessionEnd:Connect(function()
		profiles[player] = nil
		player:Kick("Your data was loaded on another server. Please rejoin.")
	end)

	if player.Parent ~= Players then
		profile:EndSession() -- left during load; PlayerRemoving already ran
		return
	end

	profiles[player] = profile
	player:SetAttribute("DataLoaded", true) -- clients wait for this before showing currency UI
end

-- Returns the active profile, or nil. Never cache the result across a yield.
function DataService:GetProfile(player: Player): Profile?
	local profile = profiles[player]
	if profile ~= nil and profile:IsActive() then
		return profile
	end
	return nil
end

-- Yields until the profile is ready, the player leaves, loading fails, or the timeout passes.
function DataService:WaitForProfileAsync(player: Player, timeoutSeconds: number): Profile?
	local deadline = os.clock() + timeoutSeconds
	while player.Parent == Players and not failed[player] and os.clock() < deadline do
		local profile = self:GetProfile(player)
		if profile ~= nil then
			return profile
		end
		task.wait(0.1)
	end
	return self:GetProfile(player)
end

-- Synchronous mutation. `mutator` must not yield.
function DataService:Update(player: Player, mutator: (data: PlayerData) -> ()): boolean
	local profile = self:GetProfile(player)
	if profile == nil then
		return false
	end
	mutator(profile.Data :: any)
	return true
end

return DataService
```

Design notes:

- A failed load **kicks**. It never falls through to default data, because default data would then be saved over the real profile. The Roblox purchasing sample does the opposite: it loads defaults but marks the profile errored so it never saves, and blocks purchases. Either way, the rule is the same: **a session that did not load real data must never save.**
- The newer-version guard handles a player who joins a new server, leaves, then lands on an old server still running the previous build. Lapis documents the same hazard. The fixes are this guard, Roblox's **Migrate To Latest Update** shutdown option, or backwards-compatible (additive-only) migrations.
- Client UI should wait for the `DataLoaded` attribute rather than assume data exists at join.

### 4.6.6 Lapis: the Promise-based alternative

Lapis (nezuo) offers:

- session locking
- **validation** before every save (for example with the `t` runtime type checker)
- an explicit **migrations** array that can mark steps `backwardsCompatible = true`
- automatic retries and throttling that never exceed budgets
- save batching (pending `save` and `close` calls merge into one request)
- autosave every 5 minutes
- automatic `BindToClose`
- deep-frozen immutable documents by default

The API is `Lapis.createCollection(name, { defaultData, validate, migrations })`, then `collection:load(key, { userId }):andThen(function(document) ... end)` and `document:close()`. **[Version-sensitive]** The README warns it "has not been battle-tested in a large production game yet". The changelog is at 0.3.4 (February 2025), which passes the document key to migrations.

Choose Lapis if you want enforced validation and immutability and already use Promises. Choose ProfileStore for its larger production track record and its `MessageAsync` offline delivery.

### 4.6.7 Schema evolution rules

1. Store an explicit `SchemaVersion` integer in every profile from day one.
2. **Additive changes** (new field with a default) need only a template change plus `Reconcile`, and they are backwards compatible.
3. **Renames, type changes and removals** need a migration step. They are **not** backwards compatible. Ship them with **Migrate To Latest Update**, or keep both old and new fields for one release.
4. Migrations are pure, deterministic and never edited after shipping. Fix a bad migration with a new one.
5. Test migrations against copies of real saved data, obtained with `ProfileStore:GetAsync` or the Data Stores Manager, before release.
6. Never delete a data store or switch store names to "reset" data. Migrate, or add a season field.

### 4.6.8 Autosave and shutdown

- **Autosave** every 3–5 minutes with a random initial offset. The Roblox sample uses 180 s; ProfileStore uses 300 s; Lapis uses 5 minutes. Save immediately after purchases and other high-value events.
- **`game:BindToClose`** gives about **30 seconds** after shutdown begins. If you run your own save system, save all players **in parallel** (one thread each), skip queued duplicate requests, and do not start new non-essential work. Requests made after shutdown begins fail with 401/402. ProfileStore and Lapis already handle this.
- **Never yield indefinitely in BindToClose**, and remember it also runs in Studio when you stop a playtest, where a 30-second hang is a common annoyance.

### 4.6.9 Ordered data stores and leaderboards

- `DataStoreService:GetOrderedDataStore(name)` stores **integer** values only. Use `GetSortedAsync(ascending, pageSize 1–100, min?, max?)` for pages. `GlobalDataStore:BatchGetAsync` can read many keys at once.
- They have no versioning and no metadata, and their **write budget is lower** (30 + players×5 per server per minute).
- Write a player's leaderboard value **at most every few minutes and on leave**, never on every coin. Read the top page every 1–5 minutes per server and cache it. For "live" global boards, keep a MemoryStore sorted map as the hot copy and periodically flush it to the ordered store.
- The Roblox create-leaderboard tutorial covers the in-experience `leaderstats` folder. `leaderstats` values are **display**, not storage. Never read currency back from them as the source of truth.

### 4.6.10 MemoryStores

**[Version-sensitive] Limits:**

- **Memory quota:** 64 KB + 1.2 KB × users. After user counts drop, an 8-day traceback period applies before the quota lowers.
- **Request units:** 1,000 + 120 × CCU per minute across the experience. `GetRangeAsync` and `ReadAsync` cost one unit per returned item (`ReadAsync` adds one per 2 s of waiting); HashMap `UpdateAsync` costs at least 2; `ListItemsAsync` costs partitions plus items.
- **Per-partition throughput:** about 30,000 units per minute. A hash map key allows about 5,000 write and 15,000 read units per minute. Each structure is capped at 100,000 units per minute.
- **Structure size:** a sorted map or queue holds at most 1,000,000 items and 100 MB.
- **Item size:** values up to 32 KB; keys and sort keys up to 128 characters.
- **Expiration:** at most 3,888,000 s (45 days), which is also the default.
- **Queues:** the default invisibility timeout is 30 s. An item read but not removed reappears, so **processing must be idempotent**.
- **Errors** include `TotalMemoryOverLimit`, `DataUpdateConflict` and `PartitionRequestsOverLimit`.
- **Flushing:** `POST /cloud/v2/universes/{id}/memory-store:flush?scope=LIVE|TEST` flushes everything, for example after a bad deploy.

**Patterns:**

- **Shard** hot sorted maps across N maps (`userId % N`) to spread partitions.
- **Revolving queues:** rotate among several queue names.
- **Global server browser:** each server writes its JobId with a 30–60 s expiry and refreshes it.
- **Cross-server lock or escrow:** use `UpdateAsync` on a hash map key with a unique token and expiry.
- **Matchmaking ticket queue:** see 4.8.

MemoryStores are **not durable**. Anything that must survive goes to a data store.

### 4.6.11 Right to be forgotten (RTBF)

Erasure requests require deleting the user's data. Automate it:

- **Deletion templates.** In Creator Hub, go to Data stores manager and open the **RTBF Deletion** tab, or use the Open Cloud Configs API (config `user_data_templates`, needing `universe:read` and `universe:write`). Up to **100 templates** per game.
- Templates use a case-sensitive `{UserId}` token. Key templates take `data_store_type` (`STANDARD` or `ORDERED`), `data_store_name`, `key_pattern` and an optional `scope_pattern`. Data store templates can delete whole **standard** stores matching a `data_store_pattern`.
- **Eligibility:** the user id must appear in the name, scope or key through a static pattern such as `Player_{UserId}`. Data keyed otherwise (usernames, guild member lists) needs your own webhook handler (`creator-docs:cloud/webhooks/automate-right-to-erasure.md`).
- Call `profile:AddUserId` (ProfileStore) or pass `{ userId }` to Lapis `load` so key metadata lists the owner.
- MemoryStore entries expire within 45 days by design. Sorted-map and hash-map docs still advise removing user-keyed entries on request.

Sources: creator-docs:cloud-services/data-stores-vs-memory-stores.md, creator-docs:cloud-services/data-stores/index.md, creator-docs:cloud-services/data-stores/error-codes-and-limits.md, creator-docs:cloud-services/data-stores/best-practices.md, creator-docs:cloud-services/data-stores/versioning-listing-and-caching.md, creator-docs:cloud-services/data-stores/player-data-purchasing.md, creator-docs:cloud-services/data-stores/right-to-be-forgotten.md, creator-docs:cloud-services/memory-stores/index.md, creator-docs:cloud-services/memory-stores/sorted-map.md, creator-docs:cloud-services/memory-stores/hash-map.md, creator-docs:cloud-services/memory-stores/queue.md, creator-docs:reference/engine/datatypes/User.yaml, creator-docs:reference/engine/classes/Player.yaml, creator-docs:tutorials/use-case-tutorials/data-storage/save-player-data.md, creator-docs:tutorials/use-case-tutorials/data-storage/create-leaderboard.md, creator-docs:scripting/security/client-server-boundary.md, ProfileStore:docs/api.md, ProfileStore:docs/tutorial/index.md, ProfileStore:ProfileStore.luau, Lapis:README.md, Lapis:docs/Migrations.md, Lapis:docs/Example.md, Lapis:CHANGELOG.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/patterns/data.md

---

## 4.7 Purchases

### 4.7.1 Developer products and `ProcessReceipt`: the rules

Developer products (consumables, currency packs, timed boosts, gift purchases) are granted **only** through the receipt callback. Facts from the engine reference:

- **Set `MarketplaceService.ProcessReceipt` exactly once, from one server script.** A second assignment silently replaces the first.
- It is called after a purchase completes, after a successful prompt, and **again when the player joins** for any receipt not yet acknowledged. There is **no time-based retry**: an unacknowledged receipt waits until the player's next join or purchase.
- The callback **can yield**, and there is no timeout. Order between multiple pending receipts is non-deterministic.
- **The same receipt can be processed on two servers at the same time** (for example during a fast server hop). Idempotency must not rely on one server's memory.
- If no callback is set, receipts are acknowledged automatically, meaning the player paid and got nothing.
- Returning `PurchaseGranted` acknowledges the receipt, though the acknowledgement itself can fail to record. Returning `NotProcessedYet` (or erroring) keeps it pending.
- `receiptInfo` fields: `PurchaseId` (unique per purchase, stable across retries), `PlayerId`, `ProductId`, `PlaceIdWherePurchased`, `CurrencySpent`, `CurrencyType`, `ProductPurchaseChannel`.
- **Never grant from `PromptProductPurchaseFinished`.** It is a UI signal, not proof of payment.
- **[Version-sensitive]** Developer products can be sold outside the game. Roblox reviews your `ProcessReceipt` implementation and flags weak ones in Creator Hub under Monetization, then Shop.

**The official handling flow** (Roblox's purchasing guide, which assumes session locking):

1. Wait until the player's data is loaded **on this server** without errors. Stop waiting if the player leaves, so the callback can run again on their next join.
2. If the `PurchaseId` is already recorded **and that record is saved** to the data store, return `PurchaseGranted`. If it is recorded but not yet saved, the outcome depends on the next save.
3. Award the purchase in the in-memory data.
4. Record the `PurchaseId` in the in-memory data.
5. Save. Return `PurchaseGranted` only once the save succeeds; otherwise return `NotProcessedYet`. A later save may still persist it, and step 2 then handles the retry.

Session locking is what makes in-memory checks trustworthy. If the save succeeds, no other server can have read or written the player's data in between.

### 4.7.2 A complete, idempotent ProcessReceipt

This version follows the official flow, using ProfileStore's `LastSavedData` to confirm the save. It is the "cache PurchaseIds and wait for the save" approach from ProfileStore's own developer-product guide.

```lua
--!strict
-- ServerScriptService/Server/Services/ReceiptService.luau
-- The ONLY code in the game that assigns MarketplaceService.ProcessReceipt.
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local DataService -- resolved in Init

local PURCHASE_ID_LIMIT = 100 -- receipts are only re-delivered until granted, so recent ids suffice
local LOAD_TIMEOUT = 30
local SAVE_CONFIRM_TIMEOUT = 25

-- Each grant must be synchronous (no yields) and must validate before mutating,
-- so an error can never leave a half-applied grant.
type Grant = (player: Player, data: any, receipt: { [string]: any }) -> ()

local GRANTS: { [number]: Grant } = {
	[1111111] = function(_player, data) -- "1,000 Cash"
		data.Cash += 1000
	end,
	[2222222] = function(_player, data) -- "2x Cash for 10 minutes": extends rather than stacks
		local now = os.time()
		data.Boosts.DoubleCash = math.max(data.Boosts.DoubleCash or 0, now) + 600
	end,
	[3333333] = function(_player, data) -- "Starter Pack"
		data.Cash += 500
		data.Inventory.StarterSword = (data.Inventory.StarterSword or 0) + 1
		data.Entitlements.StarterPack = true
	end,
}

local function isSaved(profile: any, purchaseId: string): boolean
	local saved = profile.LastSavedData
	local ids = if saved then saved.PurchaseIds else nil
	return ids ~= nil and table.find(ids, purchaseId) ~= nil
end

-- Forces saves until LastSavedData contains the PurchaseId, the session ends, or time runs out.
local function confirmSavedAsync(profile: any, purchaseId: string): boolean
	local deadline = os.clock() + SAVE_CONFIRM_TIMEOUT
	while profile:IsActive() and os.clock() < deadline do
		if isSaved(profile, purchaseId) then
			return true
		end
		local finished = false
		local connection = profile.OnAfterSave:Connect(function()
			finished = true
		end)
		profile:Save()
		local waitUntil = math.min(deadline, os.clock() + 10)
		while not finished and profile:IsActive() and os.clock() < waitUntil do
			task.wait(0.2)
		end
		connection:Disconnect()
	end
	return isSaved(profile, purchaseId)
end

local function processReceipt(receipt: { [string]: any }): Enum.ProductPurchaseDecision
	local purchaseId = receipt.PurchaseId :: string
	local productId = receipt.ProductId :: number

	local player = Players:GetPlayerByUserId(receipt.PlayerId :: number)
	if player == nil then
		return Enum.ProductPurchaseDecision.NotProcessedYet -- re-delivered on next join
	end

	local grant = GRANTS[productId]
	if grant == nil then
		warn(`[Receipt] No grant function for product {productId}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	-- Step 1: wait for session-locked data on this server (gives up if the player leaves).
	local profile = DataService:WaitForProfileAsync(player, LOAD_TIMEOUT)
	if profile == nil then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	-- Steps 2-4 run without yielding, so IsActive() stays valid for the writes.
	local data = profile.Data
	if table.find(data.PurchaseIds, purchaseId) == nil then
		local ok, err = pcall(grant, player, data, receipt) -- Step 3: award in memory
		if not ok then
			warn(`[Receipt] Grant failed for {purchaseId} (product {productId}): {err}`)
			return Enum.ProductPurchaseDecision.NotProcessedYet
		end
		table.insert(data.PurchaseIds, purchaseId) -- Step 4: record as handled
		while #data.PurchaseIds > PURCHASE_ID_LIMIT do
			table.remove(data.PurchaseIds, 1)
		end
	end

	-- Steps 2/5: acknowledge only once the record is in saved data.
	if confirmSavedAsync(profile, purchaseId) then
		return Enum.ProductPurchaseDecision.PurchaseGranted
	end
	return Enum.ProductPurchaseDecision.NotProcessedYet
end

local ReceiptService = {}

function ReceiptService:Init()
	DataService = require(script.Parent.DataService)
	MarketplaceService.ProcessReceipt = function(receipt)
		local ok, result = pcall(processReceipt, receipt)
		if ok then
			return result
		end
		warn(`[Receipt] Unhandled error: {result}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end
end

return ReceiptService
```

Why each piece matters:

- **Dedupe by `PurchaseId` in the player's saved data**, not a server-local table, because a receipt can be retried on another server, or on two at once.
- **Grant before save, but acknowledge after save.** The player gets the item instantly, and Roblox stops retrying only once the record is durable. If the save never confirms, the player keeps the item for this session and the next join's retry finds the id in saved data and returns `PurchaseGranted` without granting again.
- **No yield between the `IsActive` check and the writes**, which is ProfileStore's guarantee window.
- **Unknown product ids return `NotProcessedYet`** rather than granting nothing and acknowledging. Fix the config, and the receipt is processed on the next join.
- **The whole body is `pcall`ed,** because an error is equivalent to `NotProcessedYet`, and logging tells you why.

### 4.7.3 [Version-sensitive] `BindReceiptHandler`, the newer receipt API

`MarketplaceService:BindReceiptHandler(receiptType, handler, filter?)` registers per-type receipt handlers:

- Receipt types are `Enum.ReceiptType.DeveloperProduct`, `RobuxTransferSender` and `RobuxTransferReceiver`.
- Handlers return `Enum.ReceiptDecision.Processed` or `NotProcessedYet`.
- For developer products, pass a `filter` array of product ids to route specific products, or omit it for a catch-all. A bound handler takes precedence, and unmatched developer-product receipts **fall through to `ProcessReceipt`**, so you can adopt it incrementally.
- Duplicate registrations error, and the method returns a connection.
- Receipt info includes `PurchaseId`, `PlayerId`, `PlaceIdWherePurchased`, `ReceiptType`, plus `ProductId`, `CurrencyType` and `CurrencySpent` for products, and `TransferRequestId` for transfers.
- It pairs with the new server-only `MarketplaceService:PromptRobuxTransferAsync`, which sends Robux from one user to another. Both sides get receipts once the transfer settles, wherever they are.

The idempotency rules are identical. Use `processReceipt`'s logic inside the handler and return `Processed` only after the save is confirmed. For new code, binding filtered handlers per product family is cleaner. Keep the `ProcessReceipt` pattern above as the documented baseline until the new API has a longer track record.

### 4.7.4 Game passes

- **Check ownership on the server** with `MarketplaceService:UserOwnsGamePassAsync(userId, passId)`. Results are **cached by the engine**. A pass bought outside the session (on the website) can take minutes to show up, but the first check on the join after a purchase returns true. The call supports **transparent batching**: start checks for all passes concurrently with `task.spawn` at join and the engine batches them.
- **Listen to `PromptGamePassPurchaseFinished` on the server only.** When `purchased` is true, the engine's ownership cache is refreshed, so apply the perk immediately.
- Cache `true` for the session. Re-check a cached `false` after a short TTL, so out-of-game purchases appear. **Never cache a failed check**: treat it as "unknown, not owned for now" and retry.
- Apply character perks (speed, tools) on every `CharacterAdded`, not just at join.

```lua
--!strict
-- ServerScriptService/Server/Services/PassService.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local NEGATIVE_TTL = 60 -- seconds before re-checking a "not owned" answer

type Entry = { owned: boolean, checkedAt: number }
local cache: { [Player]: { [number]: Entry } } = {}

local PassService = {}

function PassService:OwnsAsync(player: Player, passId: number): boolean
	local perPlayer = cache[player]
	if perPlayer == nil then
		perPlayer = {}
		cache[player] = perPlayer
	end
	local entry = perPlayer[passId]
	if entry ~= nil and (entry.owned or os.clock() - entry.checkedAt < NEGATIVE_TTL) then
		return entry.owned
	end
	local ok, result = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, player.UserId, passId)
	if not ok then
		warn(`[Pass] Ownership check failed ({player.UserId}, {passId}): {result}`)
		return if entry ~= nil then entry.owned else false -- fail closed; do not cache failures
	end
	perPlayer[passId] = { owned = result == true, checkedAt = os.clock() }
	return result == true
end

function PassService:Init()
	MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player: Player, passId: number, purchased: boolean)
		if not purchased or player.Parent ~= Players then
			return
		end
		local perPlayer = cache[player] or {}
		cache[player] = perPlayer
		perPlayer[passId] = { owned = true, checkedAt = os.clock() }
		-- apply the perk now (fire a Signal that the relevant services listen to)
	end)
	Players.PlayerRemoving:Connect(function(player)
		cache[player] = nil
	end)
end

return PassService
```

### 4.7.5 Subscriptions, gifts, boosts and pricing

- **Subscriptions:** call `MarketplaceService:GetUserSubscriptionStatusAsync(player, subscriptionId)`. It returns `{ IsSubscribed, IsRenewing }`. Check it on join, and listen to `Players.UserSubscriptionStatusChanged` to grant or revoke benefits mid-session. Fail closed on errors and retry.
- **Gift versions of passes** (house rule default product set). Roblox game passes cannot be transferred, so a "Gift VIP" is a **developer product** that grants an **entitlement in the recipient's data**, for example `Entitlements.VIP = true`. Every perk check is then `ownsPass(VIP) or data.Entitlements.VIP`. The flow:
  1. The buyer picks a recipient. The server validates the id: the recipient is in the server, or is a friend checked server-side. Then the server prompts the product.
  2. Before prompting, store the intended recipient as a pending gift **in the buyer's profile data**, not only in server memory, because receipts carry only the buyer's id and may be re-delivered on a later join or another server. One pending gift per product at a time.
  3. In the grant, deliver the entitlement. If the recipient is online and session-loaded, mutate their profile directly. Otherwise use `store:MessageAsync(recipientKey, { type = "gift", item = "VIP", giftId = purchaseId })`, and handle the message idempotently by `giftId` in `profile:MessageHandler`.
  4. Record the `PurchaseId` on the **buyer's** profile, as in 4.7.2, and clear the pending gift in the same synchronous step.

  `MessageAsync` yields, which breaks the "grant functions are synchronous" rule from 4.7.2. Give gift products a dedicated branch that sends the message first. If `MessageAsync` returns false, return `NotProcessedYet`. Only then record the `PurchaseId` and confirm the save. The recipient's handler dedupes by `giftId`, so a retry that sends the message twice is harmless.

  Gate cross-region gifting and trading with `MarketplaceService:GetUsersPriceLevelsAsync` to prevent regional-price arbitrage.
- **Timed boosts** (2× Cash, 2× EXP, 2× speed for 10 minutes): store an **expiry timestamp** (`os.time()` UTC seconds) in saved data, so the boost runs on real time and survives rejoining. For "10 minutes of play time", store remaining seconds and decrement only while online; state which one in the product description. Buying again **extends** the expiry. Apply the multiplier in server reward code, never on the client. Server-wide boosts ("Server Luck", only with luck mechanics) live server-side with an expiry, announced via attribute.
- **Prices:** never hardcode Robux prices in UI. Read `PriceInRobux` from `MarketplaceService:GetProductInfoAsync(id, Enum.InfoType.Product)` or `GamePass` (transparently batched). Regional (managed) pricing means different players see different prices. `RankProductsAsync` is strictly rate-limited, so call it once at join.
- **Offer timing and honesty** (house rules): prompts come from explicit player action, or from small, dismissible, rate-limited offers after a win, never in the first minutes and never blocking play. No fake discounts, restarting countdowns or false scarcity. Keep a per-player `lastOfferAt` on the server, which decides when an offer may show.

Sources: creator-docs:reference/engine/classes/MarketplaceService.yaml, creator-docs:cloud-services/data-stores/player-data-purchasing.md, creator-docs:production/monetization/developer-products.md, creator-docs:production/monetization/passes.md, creator-docs:production/monetization/regional-pricing.md, creator-docs:scripting/transparent-batching.md, creator-docs:scripting/security/client-server-boundary.md, ProfileStore:docs/devproducts/index.md, ProfileStore:docs/api.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/monetization-policy.md



This file completes Section 4 (4.8–4.11).

---

## 4.8 Teleports, reserved servers and cross-server systems

### 4.8.1 Teleporting

- Use **server-only** `TeleportService:TeleportAsync(placeId, players, teleportOptions?)`, wrapped in `pcall` with retries. Do not use the client-side `Teleport()` for game flows; the server decides where players go.
- **[Version-sensitive] Deprecated:** `ReserveServer` / `ReserveServerAsync`, `TeleportOptions.ShouldReserveServer` and `ReservedServerAccessCode`. The replacements are:
  - **Reserved (private match) server:** `options.ReservedServerId = HttpService:GenerateGUID(false)`. The first teleport with a new id creates the server; later teleports with the same id join it. Store the id to route late joiners and reconnects.
  - **VIP server:** `options.VipServerId = game.PrivateServerId`.
  - **A specific public server** (follow a friend): `options.ServerInstanceId = jobId`.
  - The best-practices skill reports that setting more than one target field errors **[Version-sensitive]**.
- **Detecting a reserved server:** `game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0`. VIP server access is checked per player at connect time.
- **Teleport data is not secure.** `options:SetTeleportData(t)` is client-visible and tamperable. Read it with `player:GetJoinData().TeleportData` as a hint only. Store anything that matters (roster, wager) server-side in a MemoryStore hash map keyed by the reserved server id.
- **Session locks:** ProfileStore handles hops. The destination's `StartSessionAsync` asks the source to release; `PlayerRemoving` → `EndSession` runs normally. Expect a few seconds' load delay on arrival.
- **Custom loading screen:** `TeleportService:SetTeleportGui(gui)` sets it on the source. On arrival, `TeleportService:GetArrivingTeleportGui()` lets you keep it up until data is loaded.
- **Access control:** destination places that must only be reached through your matchmaker should be set to **Secure within universe only** (4.5.9).

```lua
--!strict
-- ServerScriptService/Server/Services/TravelService.luau (official SafeTeleport pattern, typed)
local HttpService = game:GetService("HttpService")
local TeleportService = game:GetService("TeleportService")

local ATTEMPT_LIMIT = 5
local RETRY_DELAY = 1
local FLOOD_DELAY = 15
local MAX_INIT_RETRIES = 3

local initRetries: { [Player]: number } = {}
local TravelService = {}

function TravelService:TeleportAsync(placeId: number, players: { Player }, options: TeleportOptions?): (boolean, any)
	local ok, result
	for attempt = 1, ATTEMPT_LIMIT do
		ok, result = pcall(TeleportService.TeleportAsync, TeleportService, placeId, players, options)
		if ok then
			break
		end
		task.wait(RETRY_DELAY * attempt)
	end
	if not ok then
		warn(`[Travel] TeleportAsync failed after {ATTEMPT_LIMIT} attempts: {result}`)
	end
	return ok, result
end

function TravelService:StartMatchAsync(placeId: number, players: { Player }): string?
	local options = Instance.new("TeleportOptions")
	local matchId = HttpService:GenerateGUID(false)
	options.ReservedServerId = matchId
	options:SetTeleportData({ matchId = matchId }) -- hint only; the roster lives server-side
	local ok = self:TeleportAsync(placeId, players, options)
	return if ok then matchId else nil
end

function TravelService:Init()
	TeleportService.TeleportInitFailed:Connect(function(player, result, message, placeId, options)
		local count = (initRetries[player] or 0) + 1
		initRetries[player] = count
		if count > MAX_INIT_RETRIES then
			warn(`[Travel] Giving up on {player.UserId}: {result.Name} {message}`)
			return
		end
		if result == Enum.TeleportResult.Flooded then
			task.wait(FLOOD_DELAY)
		elseif result == Enum.TeleportResult.Failure then
			task.wait(RETRY_DELAY)
		else
			warn(`[Travel] Not retrying {player.UserId}: {result.Name} {message}`)
			return
		end
		self:TeleportAsync(placeId, { player }, options)
	end)
end

return TravelService
```

### 4.8.2 Matchmaking

- **Roblox's built-in matchmaking** places joining players into public servers. It uses weighted-sum scoring over signals (friends, age, language, latency, occupancy and similar) and lets you add **custom attributes** (numerical or categorical, which can be sourced from data stores) and adjust weights. Use it to shape public servers, for example by skill bracket or language, before building your own.
- **A custom match flow**, for queues and parties:
  1. Lobby servers add tickets to a MemoryStore sorted map or queue, sharded by mode.
  2. One matchmaker, either a server elected via a MemoryStore lock with expiry or every lobby taking turns via `UpdateAsync`, groups tickets.
  3. It writes the match record (`matchId`, roster, mode) to a hash map.
  4. It calls `StartMatchAsync`.
  5. The match server reads its roster by `game.PrivateServerId` and rejects anyone not on it.
- Queue reads hide items for the invisibility timeout (30 s default), so make "remove ticket" idempotent and expire stale tickets.

### 4.8.3 Cross-server messaging

**[Version-sensitive] MessagingService limits:**

| Limit | Value |
| --- | --- |
| Delivery | Best effort, typically 1–2 s |
| Topic names | 1–80 characters |
| Message size | 1 kB |
| Sends per server | 600 + 240 × players per minute |
| Receives per topic | 40 + 80 × servers per minute |
| Receives per game | 400 + 200 × servers per minute |
| Subscriptions per server | 20 + 8 × players |
| Subscribe requests | 240 per minute |

Use it for **hints**: announcements, "refresh your leaderboard cache", or "player X is online in server Y". Receivers re-read authoritative state from data stores or MemoryStores. Never use it for currency, trades or anything that must arrive. ProfileStore `MessageAsync` covers guaranteed per-player delivery. Wrap `SubscribeAsync` and `PublishAsync` in `pcall` with backoff, and validate `message.Data` like a remote payload.

Open Cloud also exposes `PublishUniverseMessage` (publish from outside the game, for example from a live-ops tool) and `RestartUniverseServers`.

Sources: creator-docs:projects/teleport.md, creator-docs:projects/teleport-private-servers.md, creator-docs:reference/engine/classes/TeleportService.yaml, creator-docs:matchmaking/index.md, creator-docs:reference/engine/classes/MessagingService.yaml, creator-docs:cloud-services/memory-stores/queue.md, creator-docs:cloud-services/http-service.md, ProfileStore:docs/api.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/patterns/network.md

---

## 4.9 Multithreading and the scheduler

### 4.9.1 The frame and the scheduler

Luau threads are coroutines on one main thread. The engine resumes them at fixed **resumption points** each frame: input, `PreRender` (formerly `RenderStepped`, client only), `PreAnimation`, `PreSimulation` (formerly `Stepped`), physics, `PostSimulation`, `Heartbeat`, plus deferred-event and `task` resumption. `task.wait` and `task.delay` resume on Heartbeat. Anything that runs long in one resumption, such as a loop over 100,000 items, stalls the whole frame. Split the work with `task.wait()` between batches, or move it to Parallel Luau.

Measure before optimising. The **Script Profiler** shows per-function time, the **MicroProfiler** shows frame timing and labels, and the Luau heap view shows memory.

### 4.9.2 Parallel Luau

- Scripts run in parallel only if they are **descendants of an `Actor`**. Scripts in the same Actor always run serially with each other, so split work across several Actors by logical unit. The docs suggest more Actors than cores, for example 64 on a 4-core machine.
- Enter the parallel phase with `task.desynchronize()`, or connect with `signal:ConnectParallel(fn)`. Return with `task.synchronize()` before writing to the DataModel.
- **Thread safety:** Roblox APIs are marked *Unsafe* (the default; serial only), *Read Parallel* (reads allowed in parallel), *Local Safe* (allowed on the Actor's own descendants) or *Safe*. Raycasts and spatial queries are readable in parallel, while most property writes are not.
- **`require` is not allowed in the parallel phase.** Require everything at the top level first.
- **Communication:** `Actor:SendMessage(topic, ...)` with `BindToMessage` or `BindToMessageParallel`. Use `SharedTable` for shared data across Actors. Ordinary tables are copied per Actor VM.
- **Good fits:** per-character hit and movement validation, procedural generation (noise in parallel, `WriteVoxels` serially), pathfinding pre-computation and large ECS updates.
- **Anti-patterns:** many serial/parallel switches per frame, one Actor per projectile, hundreds of Actors each syncing to write one property, and trivial work whose overhead exceeds the gain.

```lua
--!strict
-- Script (RunContext = Server) inside each of N Actors cloned at boot.
local actor = script:GetActor()
assert(actor, "must run inside an Actor")

local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude

actor:BindToMessageParallel("ValidateShots", function(shots: { { origin: Vector3, direction: Vector3, shooter: Model } })
	local hits: { [number]: RaycastResult? } = {}
	for i, shot in shots do -- parallel phase: read-only queries
		params.FilterDescendantsInstances = { shot.shooter }
		hits[i] = workspace:Raycast(shot.origin, shot.direction, params)
	end
	task.synchronize() -- serial phase: safe to write the DataModel
	-- apply damage for valid hits here (or fire a BindableEvent to the combat service)
end)
```

Sources: creator-docs:scripting/scheduler.md, creator-docs:scripting/multithreading.md, creator-docs:scripting/events/deferred.md, creator-docs:luau/native-code-gen.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/performance.md

---

## 4.10 Tooling, testing, CI/CD and AI agents

### 4.10.1 The toolchain

| Tool | Role | Notes |
| --- | --- | --- |
| **Rokit** | Toolchain manager (`rokit.toml`, `rokit install`) | Supersedes Aftman and Foreman and reads their manifests. Pins every CLI below per project. |
| **Rojo** | Filesystem ↔ Studio sync, `rojo build`, `rojo serve`, `rojo sourcemap` | The docs' example pins 7.6.1. `emitLegacyScripts` defaults to true (4.1.3). Cannot live-sync terrain or some properties. `rojo upload --cookie` uses a browser cookie, so never use it in CI; use Open Cloud. |
| **Studio Script Sync** | Built-in file sync for scripts only | Up to 10,000 scripts per root and 128 roots. Works with Team Create. Attributes and tags on synced scripts are lost. The best-practices skill reports it went GA in 2026 **[Version-sensitive]**. |
| **Argon / Lync / Azul** | Alternative sync tools | Project fields differ from Rojo's. Do not copy configs between tools. |
| **Wally** | Package manager (`wally.toml`, `wally install` → `Packages/`, `ServerPackages/`) | Pins 0.3.2. Commit `wally.lock`. Stable Wally has no `--locked`, so CI runs `wally install` and then `git diff --exit-code wally.lock`. `pesde` is a newer alternative. |
| **Selene** | Linter (`selene.toml` with `std = "roblox"`) | Flags deprecated globals, shadowing and unused variables. Run as `selene src`. |
| **StyLua** | Formatter (`stylua.toml`, `syntax = "Luau"`) | `stylua --check src` in CI. |
| **luau-lsp** | Language server and `luau-lsp analyze` type checking | Needs a fresh `sourcemap.json` (`rojo sourcemap default.project.json --output sourcemap.json`). A stale sourcemap is the usual cause of "does not exist" errors. Its Studio Companion plugin pairs with Script Sync. |
| **Lune** | Standalone Luau runtime with filesystem, network and `roblox` place-file APIs | Replaces Remodel for build scripts (asset upload, place edits, codegen). Scripts have full machine access, so review them like shell scripts. |
| **Jest-Lua / TestEZ** | In-engine test frameworks | TestEZ is the older BDD framework. Jest-Lua is Roblox's newer port of Jest. |
| **rbxcloud, Mantle** | Open Cloud CLI; infrastructure-as-code | RbxUtil's CI uses `rbxcloud experience publish`. |

Also useful: Darklua (source transforms such as string requires to instance paths), Moonwave (docs from `--[=[ ]=]` comments) and roblox-ts (TypeScript to Luau; adopt it for a whole project or not at all).

```toml
# rokit.toml (pin exact versions; the first three are the docs' example)
[tools]
rojo = "rojo-rbx/rojo@7.6.1"
wally = "upliftgames/wally@0.3.2"
lune = "lune-org/lune@0.10.4"
selene = "kampfkarren/selene@<pin>"
stylua = "johnnymorganz/stylua@<pin>"
luau-lsp = "johnnymorganz/luau-lsp@<pin>"
```

**Rojo or Script Sync?** If the filesystem is the source of truth (git, CI, code review, AI agents editing files), use **Rojo**. If Studio is the source of truth and you only want an external editor, use **Script Sync**.

### 4.10.2 Testing

- **Pure logic** (economy maths, damage formulas, schema migrations, validators) lives in modules with no Instance dependencies, so it runs under Lune in milliseconds. Test migrations against fixtures copied from real saved data.
- **In-engine tests** (Jest-Lua or TestEZ) run in a test place, either through the Studio CLI (`RobloxStudioBeta.exe --task RunScript --placeId <id> --universeId <id> --runScriptFile tests.luau --outputFile out.log --quitAfterExecution`) or through **Open Cloud Luau Execution** in CI.
- **Data code** runs against `ProfileStore.Mock` so tests never touch live keys.
- **Scripted multiplayer tests** use `StudioTestService` (Studio-only: `ExecuteMultiplayerTestAsync`, `AddPlayers`, `GetTestArgs`, `EndTest`) and `UserInputService:CreateVirtualInput()` for simulated input.
- **Leak audit:** respawn 20 times and rejoin repeatedly; memory and connection counts must return to baseline.

### 4.10.3 CI/CD with Open Cloud

**Luau Execution API.** Create a task with `POST /cloud/v2/universes/{universeId}/places/{placeId}/luau-execution-session-tasks`, or `.../versions/{versionId}/luau-execution-session-tasks` for an exact version, with a body of `{ "script": "...", "timeout": "300s" }`. Poll the returned `path` until `state` is `COMPLETE` or `FAILED`. The states are `QUEUED`, `PROCESSING`, `CANCELLED`, `COMPLETE` and `FAILED`. `output.results` holds JSON-serialisable return values (Instances become null), and the logs endpoint returns printed output.

Limits:

| Limit | Value |
| --- | --- |
| Script size | 4 MB |
| Default and maximum runtime | 5 minutes |
| Return value | 4 MB of JSON |
| Retained logs | 450 KB |
| Binary input | up to 100 MiB, valid for 15 minutes; the script reads it via `({...})[1].BinaryInput` |

The session has no physics and does not auto-run scripts. DataModel changes are not persisted, but DataStores and other engine cloud APIs work. Errors surface as `SCRIPT_ERROR` and `DEADLINE_EXCEEDED`. The best-practices skill reports a cap of 10 incomplete tasks per place **[Version-sensitive, not confirmed in the docs]**.

**Place publishing.** Send `PATCH https://apis.roblox.com/assets/v1/assets/{placeId}` with form fields `request={"assetId":<placeId>,"assetType":"Place","published":true}` (`published` must be explicitly `true`) and `fileContent` (an `.rbxl` as `application/octet-stream`, or an `.rbxlx` as `application/xml`). It returns an operation to poll at `GET https://apis.roblox.com/assets/v1/operations/{id}`. The result has `revisionId` and `isPublished`. The key needs **assets** Read and Write for that game. It does not update EditableImage, EditableMesh, PartOperation, SurfaceAppearance or BaseWrap; publish those from Studio. Community guides still cite the older `POST /universes/v1/{universeId}/places/{placeId}/versions?versionType=Published`; prefer the Assets API the current docs use.

**A pipeline** (lower-risk; the shape of Roblox's place-ci-cd-demo and RbxUtil's CI):

1. **On every pull request:** `rokit install`; `wally install` then `git diff --exit-code wally.lock`; `selene src`; `stylua --check src`; `rojo sourcemap default.project.json --output sourcemap.json`; `luau-lsp analyze --sourcemap=sourcemap.json src` (pass the Roblox definitions file; check flags for your pinned version); Lune unit tests.
2. **On merge to main:** `rojo build -o game.rbxl`, publish to a **test place in a separate test universe**, run in-engine tests there with Luau Execution, and fail the build on any failed test.
3. **On a release tag:** publish the same artefact to production. Keep a manual approval step, and use **Migrate To Latest Update** when the release contains non-backwards-compatible data migrations.

Open Cloud keys live in CI secrets. Scope each key to one universe and the minimum permissions, and keep production and test keys separate.

### 4.10.4 The Blender → GLB → Open Cloud asset pipeline (house rule)

1. Model in Blender. Drive Blender through the Blender Lab MCP add-on bridge (`tools/blender_exec.py`). Keep real-world scale and clean pivots. For complex meshes, include simple collision geometry as separate low-poly objects.
2. **Export in a separate headless process**, for example `blender -b assets/blender/StreetLamp.blend --python tools/export_glb.py`, where the script calls Blender's glTF exporter with GLB format. Never export from the interactive session that the MCP bridge is driving.
3. **Upload** with `POST https://apis.roblox.com/assets/v1/assets` (multipart). Send header `x-api-key`, a `request` field of `{"assetType":"Model","displayName":...,"description":...,"creationContext":{"creator":{"userId" or "groupId":...}}}`, and `fileContent=@file.glb;type=model/gltf-binary`. The limit is **20 MB per call**. The key needs the **assets** scope with Read and Write; for OAuth the scopes are `asset:read` and `asset:write`.
4. **Poll** `GET /assets/v1/operations/{operationId}` until `done`. Record `assetId` and check `moderationResult`. The model arrives as a **Model of MeshParts uploaded as a package**. Reference it by `rbxassetid://<id>` or `Content.fromAssetId(id)`.
5. **[Version-sensitive] Content updates (PATCH) are supported for `.fbx` only.** Every GLB re-upload creates a **new asset id**, so the pipeline must rewrite `assets/asset-ids.json` and the generated `Shared/Config/Assets.luau`, and placed instances must be swapped. A Lune or Python script owns this mapping. Never hand-edit ids.
6. **Collision (house rule):** after insertion, set each MeshPart's `CollisionFidelity` at edit time:
   - `Box` for crates and signs;
   - `Hull` for convex props;
   - `Default` or `PreciseConvexDecomposition` for walkable or complex shapes.

   Alternatively, set the visual MeshParts to `CanCollide = false` and add invisible, anchored hull parts (`Transparency = 1`, `CanCollide = true`) as technical helpers. Verify with Studio's collision/decomposition geometry visualisation and a walk-through test: nothing visible may be walk-through.
7. **Images** must be under 8000×8000 and cannot be updated in place. **Audio** uploads are capped at 7 minutes, with 100 uploads a month for ID-verified accounts and 10 otherwise.

### 4.10.5 Studio collaboration

- **Team Create:** live scripting is the default (auto-save every 5 minutes, Script History). **Drafts mode** is off by default; drafts are local and must be **committed**, with Merge From Server for conflicts. **Team Test** allows one session at a time.
- **Place files do not merge.** Code merges in git; the place file has one owner at a time. Track binary files with lockable Git LFS, and let **only CI publish** to production.

### 4.10.6 AI agents working with Studio

**[Version-sensitive]** Studio ships a built-in **MCP server**:

- Enable it in the Assistant settings ("Enable Studio as MCP server"). The menu path has moved between versions.
- Transport is stdio. On Windows the command is `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`, run from its own folder. Roblox's official agent plugin (`Roblox/roblox-studio-agent-plugin`, v0.2.2, config only) launches this binary, and its docs note that a port-13469 conflict breaks the connection.
- Every call takes a `studio_id` from `list_roblox_studios`.
- Tools cover script read, search and `multi_edit`; tree search and `inspect_instance`; `execute_luau` (Edit, Server or Client context); play control, console output and screen capture; input simulation; generation; and `open_cloud_invoke`, which has per-game permission levels (Safe, Balanced by default, Full access, Custom) and never sends credentials to the client.

Working rules distilled from Roblox's plugin, the best-practices skill and OpenGameEval:

1. **Connect, then orient.** Call `list_roblox_studios`; if several places are open, confirm the target with the user. Call `get_studio_state`, and find out who owns the files: Rojo, Script Sync or Studio.
2. **Explore before editing.** OpenGameEval ties failures to under-exploration (giving up after two searches) and to fixing one copy when six existed. Enumerate with `search_game_tree` or an `execute_luau` listing.
3. **Edit source, in Edit mode.** Play-mode changes are discarded, and `execute_luau` runtime changes do not persist in scripts. If Rojo owns the files, edit the files, or Rojo overwrites Studio.
4. **A write is not done until a read shows it.** Re-read, then playtest and check `get_console_output`.
5. **Modify what exists; do not add parallel copies.** Preserve the hierarchy, because code and checks depend on paths.
6. **Guardrails.** `execute_luau` freezes Studio until it yields, so batch about 1,000 items per `task.wait()`. `require` in the Edit context gives fresh module state. Never publish, save or delete unasked. Stop after the same error repeats twice.
7. **House rules override convenient tools.** Do not ship visible content from `generate_procedural_model` (primitive Parts), `insert_asset` (Creator Store models) or AI mesh generation. Visible assets come from the Blender pipeline (4.10.4).
8. **Verify APIs; do not guess.** Use `https://create.roblox.com/docs/llms.txt`, the `.md` page versions, or Studio CLI `--api` / `--fullApi` dumps.

**[Version-sensitive] OpenGameEval** (`Roblox/open-game-eval`) benchmarks agents on about 87 core and 30 debug tasks in real Studio sessions. At time of reading, the best core Pass@1 is around 50%. Its checks reward persistent source edits, an intact hierarchy and reuse of existing objects.

Sources: creator-docs:projects/external-tools.md, creator-docs:scripting/sync.md, creator-docs:studio/cli.md, creator-docs:studio/testing-modes.md, creator-docs:studio/mcp.md, creator-docs:studio/mcp-open-cloud.md, creator-docs:projects/collaboration.md, creator-docs:cloud/guides/usage-assets.md, creator-docs:cloud/guides/usage-place-publishing.md, creator-docs:reference/cloud/openapi.json, RbxUtil:.github/workflows/ci.yaml, RbxUtil:ci/RunTests.luau, Roblox/roblox-studio-agent-plugin:README.md, Roblox/roblox-studio-agent-plugin:skills/roblox-get-started/SKILL.md, Roblox/open-game-eval:README.md, Roblox/open-game-eval:LLM_LEADERBOARD.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/external-editors.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/studio-mcp.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/team-workflow.md, gamedev-skills/awesome-gamedev-agent-skills:skills/other-engines/roblox-studio-workflow/SKILL.md, awesome-roblox/awesome-roblox:readme.md, elevenpassin/awesome-roblox:readme.md

---

## 4.11 Common bugs and anti-patterns checklist

Use this as a review gate before shipping.

**Architecture and lifecycle**

- One server entry and one client entry; no Scripts inside models; behaviour bound by tags.
- No circular requires; no yielding at module top level or in `Init`.
- `PlayerAdded` handlers also run for players already in `Players:GetPlayers()`; same for `CharacterAdded` and existing characters.
- Every per-player table is cleared on `PlayerRemoving`. Every connection has an owner (Trove) and a teardown path.
- No `RunContext = Client` Script inside a Starter container (it runs twice). The Rojo `emitLegacyScripts` setting matches where client scripts live.
- Client code waits for streamed Workspace content (`WaitForChild` with a timeout, or tag signals).

**Luau**

- `--!strict` in new files; untrusted input typed `unknown`; casts only after runtime checks.
- No `wait`, `spawn`, `delay`, `tick`, `Humanoid:LoadAnimation`, BodyMovers or `FindPartOnRay`. Use `task.*`, `os.clock`/`time`, `Animator`, constraint movers and `workspace:Raycast`.
- Every web-service call is `pcall`ed, and the failure branch does something.
- Code works under `SignalBehavior = Deferred` (no fire-then-read, `Once` for one-shots).

**Networking**

- Remotes carry intent, not outcomes; the server never trusts client-sent player ids, prices, damage or positions.
- No `InvokeClient`; `OnServerInvoke` is assigned once.
- Unreliable remotes carry only replaceable data under 1,000 bytes, and absolute values rather than deltas.
- No mixed tables, `nil` holes, metatables or non-string dictionary keys in payloads.
- Private state is not in attributes (attributes are public to every client that has the instance).
- Server handlers are connected before clients can fire; handlers that yield tolerate interleaving.

**Security**

- Every remote goes through rate limiting plus type, finiteness (NaN/inf), range, length, UTF-8, instance (`typeof`, `IsDescendantOf`, ownership) and game-rule checks.
- Prompts, ClickDetectors and DragDetectors are re-validated on the server (distance, enabled, cooldown); interactable anchors are anchored.
- Movement and combat are validated server-side with tolerances and teleport exemptions; there is no `Touched`-only damage on client-owned parts.
- No secrets, webhooks or server logic in replicated containers; secrets are only in the Secrets store.
- Sub-places are "Secure within universe only" where gated; dev and test places live in separate universes.
- Consequences escalate (log → mitigate → restrict → ban); no instant ban on a single signal.

**Data**

- Session-locked loading (ProfileStore or Lapis); a failed load never leads to a save; the player is kicked or the profile is marked unsaveable.
- Migrations run before `Reconcile`; there is a newer-schema guard; the key pattern never changes.
- No DataStore reads during gameplay; autosave is staggered; no custom BindToClose on top of a library that already handles shutdown.
- `UpdateAsync` transforms never yield; metadata and user ids are re-passed; failed writes are verified with `UseCache = false`.
- Leaderboard writes are throttled to minutes, not per change; leaderstats are display only.
- Trades mutate both session-locked profiles synchronously after `IsActive()` checks.
- RTBF templates cover every user-keyed store.

**Purchases**

- Exactly one `ProcessReceipt` (or filtered `BindReceiptHandler`s); grants are deduped by `PurchaseId` in saved data; `PurchaseGranted` is returned only after the save is confirmed.
- `NotProcessedYet` when the player is absent, data is not loaded, the product is unknown, or the grant or save fails.
- Nothing is granted from `PromptProductPurchaseFinished`; game pass ownership is checked on the server and cached (true for the session, false with a TTL, failures uncached).
- Prices are read from `GetProductInfoAsync`; gifts are gated by `GetUsersPriceLevelsAsync`; boosts store an expiry and extend rather than stack.
- Offers are small, dismissible, rate-limited and well-timed; no fake discounts, restarting countdowns or false scarcity.

**Assets and world (house rules)**

- Every visible object is a Blender-made model; no visible primitive Parts or placeholders; no Creator Store models.
- Every visible object has proper collision (`CollisionFidelity` or invisible hull helpers); a walk-through test passes.
- Asset ids come from the generated mapping, and the pipeline handles new ids after each GLB re-upload.

**Tooling and agents**

- Toolchain pinned in `rokit.toml`; `wally.lock` committed; selene, StyLua and luau-lsp analysis gate every PR.
- CI publishes test builds to a separate test universe and runs in-engine tests via Luau Execution; only CI publishes production.
- AI agents connect, orient, explore, edit source in Edit mode, read back every write, and never publish or delete unasked.

Sources: creator-docs:scripting/security/security-tactics.md, creator-docs:scripting/events/remote.md, creator-docs:scripting/events/deferred.md, creator-docs:cloud-services/data-stores/best-practices.md, creator-docs:cloud-services/data-stores/player-data-purchasing.md, creator-docs:reference/engine/classes/MarketplaceService.yaml, creator-docs:cloud/guides/usage-assets.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/review-checklist.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/false-positives.md, andrian-syh/roblox-best-practices-skill:roblox-best-practices/references/api-currency.md, gamedev-skills/awesome-gamedev-agent-skills:skills/other-engines/roblox-luau/SKILL.md, Roblox/open-game-eval:README.md



---

# 5. Roblox Performance, World Building, Art Pipeline, UI and Cross-Platform

This section covers how a Roblox game stays fast on a cheap Android phone and still looks finished. It goes from frame budgets and profiling down to Luau idioms. It then covers rendering, streaming and physics, the Blender-to-Roblox art pipeline, lighting, VFX, audio, UI, input, loading, and a pre-launch checklist.

Facts come from the Roblox creator-docs snapshot dated 2026-11-07 and from the Luau language site. They also draw on a few community references. Where a fact is version-sensitive (beta, recently renamed or recently rolled out), it is flagged with **[version-sensitive]**. Re-check those facts against the live docs before relying on them. Today's date for this knowledge base is 2026-11-08.

Three house rules apply throughout. This section is written to fit them.

1. **Every 3D asset is made in Blender.** That covers buildings, props, roads, lamps, vehicles and characters. Nothing is built from primitive Parts or taken from the marketplace.
2. **Every visible object is a Blender model, and every one is solid.** Players and NPCs must not walk through anything visible. Invisible Parts are allowed only as technical helpers: triggers, prompt anchors, spawn points and collision hulls.
3. **Monetization is heavy but never invasive.** This affects UI and loading design (sections 5.10 and 5.12). Offers never block play, and they never appear during loading or the first minutes.

The file is split into three parts. This part covers sections 5.1–5.6: performance model, profiling, Luau, rendering, streaming and physics. `05-roblox-performance-content-part2.md` covers sections 5.7–5.9: the art pipeline, lighting, and VFX, animation and audio. `05-roblox-performance-content-part3.md` covers sections 5.10–5.14: UI, input, loading, the checklist, and a list of contradictions and version notes.

## 5.1 The performance model: frame time, budgets and device targets

### Frame time is the real budget

Roblox performance is measured in **milliseconds per frame**, not in FPS. FPS hides how uneven frames are. A game that averages 60 FPS but hitches to 80 ms every few seconds feels worse than a steady 45 FPS. The docs say plainly that consistency matters more than the average.

| Target FPS | Frame budget | Typical use |
|---|---|---|
| 30 | 33.33 ms | The floor for the lowest-end phones. Treat it as the "must never drop below" line. |
| 60 | 16.67 ms | The default target, and the server heartbeat cap. Design for this on mid-range mobile. |
| 72 | 13.9 ms | Standalone VR (Quest 2). |
| 120 | 8.33 ms | High-refresh desktops and phones. |
| 240 | 4.17 ms | The highest client cap. The client can be uncapped up to 240 FPS on Windows. |

The **server** runs its heartbeat at up to 60 Hz. A falling server heartbeat shows up as rubber-banding, delayed remotes and laggy physics for *everyone*. The client frame rate only hurts one player. Treat a server heartbeat that stays below about 50 Hz as an incident; that threshold is a house recommendation, not a documented number.

### What fills a frame

Every frame, the task scheduler runs a fixed sequence of jobs. Luau can hook in at these RunService events, in frame order:

1. **PreRender.** Runs after input and before rendering. Use it only for things that must react to input before drawing, such as camera motion. For strict ordering use `RunService:BindToRenderStep()`.
2. **PreAnimation.** Runs before animations are stepped.
3. **PreSimulation.** Runs before physics. Set velocities, forces and `Motor6D.Transform` here. If you do it later, Animators overwrite the change on the next frame.
4. **Physics** runs (the `worldStep` and `physicsStepped` scopes).
5. **PostSimulation / Heartbeat.** Runs after physics. Read final positions here. How Heartbeat scripts run depends on `Workspace.SignalBehavior` (deferred versus immediate events).

Rendering then has three phases: Prepare, Perform and Present. Rendering runs on its own thread, and parts of physics and some Luau run on worker threads. The **main thread** is still the usual bottleneck: scripts, animation, Humanoids and most of physics live there. `WaitingHybridScriptJob` resumes yielded threads such as `task.wait` callers. It runs about 30 times a second and has a time budget. If you exceed that budget, resumption is pushed to later frames, and "my `task.wait(0.1)` takes 0.3 s" bugs appear.

### Device reality (snapshot data, flagged as volatile)

The test-on-hardware docs give these 2025–2026 device figures **[version-sensitive]**:

- **Platform share:** Android is about **65 %** of players.
- **Android RAM:** about **60 %** have **2–4 GB**, about 35 % have 4–8 GB, and only about 5 % have more than 8 GB.
- **Performance class:** more than 50 % of devices score **10k–20k on Passmark**, which is low-end by PC standards.
- **Suggested test devices:** Infinix Smart 9, Moto G05, Oppo A18 and Fire HD 10 (2023) for the low end, and Galaxy S22 Ultra for the high end.

**Design rule:** the baseline device is a 3 GB Android phone that heats up and throttles. A thermal test means 10–15 minutes of active play on real hardware, because throttling only appears after several minutes. The Studio Device Emulator gets screen size right but is **not accurate for memory or performance**.

### Budget table

The first group of rows are doc limits. The second group are house recommendations, derived from the doc figures for a game that must hold 60 FPS on mid-range mobile and 30 FPS on the low end.

| Budget item | Value | Origin |
|---|---|---|
| Frame time, mid mobile | ≤ 16.67 ms | Doc default target |
| Frame time, low-end floor | ≤ 33.33 ms | Doc table |
| Draw calls in view | < 1,000 (example baseline-device limit) | Doc (identify.md) |
| Triangles in view | < 1,000,000 (example baseline) | Doc (identify.md) |
| Triangles per mesh (hard import limit) | ≤ 20,000 | Doc (art specs) |
| Long-running script work | ~5 ms per frame, then yield | Doc (design.md) |
| Server memory | < 50 % of (6.25 GiB + 100 MiB × peak players); 30 players gives about 9.18 GiB | Doc (identify.md) |
| Client crash rate | Investigate above 2–3 % | Doc |
| Particle emission | ≤ 400 particles/s per emitter (100/s on mobile); lifetime cap 20 s | Doc (particle-emitters.md) |
| Simultaneous `Highlight`s | ≤ 255 (extras are silently ignored) | Doc (highlighting.md) |
| Texture size | Most ≤ 512², minor ≤ 256², hero ≤ 1024² | Doc (improve.md) |
| VR | 72 FPS on Quest 2 | Doc (vr-guidelines.md) |
| Client Luau per frame | ≤ 3–4 ms total across all scripts | House |
| Physics per frame (client) | ≤ 2–3 ms | House |
| Render CPU (Prepare + Perform) | ≤ 6 ms on mid mobile | House |
| Unique textures in a typical view | ≤ 40–60 at ≤ 512² | House |
| Lights with `Shadows = true` in view | ≤ 2–4 | House (docs say "use fewer") |
| Prop triangles | 50–1,500 small, 1,500–6,000 medium, ≤ 15,000 hero/building module | House |
| Join to playable on low-end Android | ≤ 10–15 s | House |
| Remote traffic | Deltas only; throttle per-frame remotes to ≤ 10–20 Hz | House, from improve.md "throttle remotes" |

### Memory categories you will see

The Developer Console Memory tab and Scene Analysis split memory into labels. The ones that matter most for content are:

- **GraphicsTexture:** texture pixels. A 1024² texture costs four times a 512² one. Images are transcoded on upload, so PNG compression and removing the alpha channel do **not** reduce runtime memory. Only resolution and unique-texture count matter.
- **GraphicsMeshParts:** unique mesh geometry. The Importer does not de-duplicate meshes, so importing a whole scene as one file creates duplicate mesh IDs for identical props.
- **PhysicsParts:** collision geometry. This includes parts with `CanCollide = false`, because their collision data is still stored. Precise fidelity is expensive here.
- **Sounds:** loaded audio.
- **LuaHeap, PlaceScriptMemory, InstanceCount:** watch these for leaks.
- **Animation:** loaded animation clips. Scene Analysis has a separate view for them.

Server memory **does not shrink** when players leave, so leaks accumulate over a long-lived server. `DataModel.ServerLowMemoryWarning` fires when the server is close to its limit; log it to your analytics. If heartbeat stays low even after optimization, Extended Services for Compute is an option.

Sources: creator-docs:performance-optimization/index.md, creator-docs:performance-optimization/design.md, creator-docs:performance-optimization/identify.md, creator-docs:performance-optimization/microprofiler/index.md, creator-docs:performance-optimization/microprofiler/task-scheduler.md, creator-docs:performance-optimization/test-on-hardware.md, creator-docs:performance-optimization/monitor.md, creator-docs:effects/particle-emitters.md, creator-docs:effects/highlighting.md, creator-docs:production/publishing/vr-guidelines.md

## 5.2 Profiling tools and the MicroProfiler workflow

### Keyboard shortcuts and tools

| Tool | Shortcut / location | Use it for |
|---|---|---|
| Developer Console | F9 (client and server tabs) | Memory per label, script errors, network stats, server MicroProfiler recording |
| MicroProfiler | Ctrl+Alt+F6 in the client; Ctrl+F6 in Studio and the desktop client | Per-frame timing of every engine job and your custom labels |
| Performance Stats | Ctrl+Alt+F7 | Live overlay of CPU, GPU, memory and network |
| Debug stats | Shift+F1 to Shift+F5 | Shift+F2 is Render (draw calls, triangles). Shift+F5 is Summary. Shift+F3 has the streaming panels (see 5.5) |
| Network Simulation | Alt+S in Studio | Add latency and packet loss while testing |
| Scene Analysis | Window > Performance Summary in Studio | Script memory, unparented instances, instance composition, audio memory, animation memory, triangle composition |
| Performance Dashboard | Creator Dashboard | Live-game client and server frame time, memory, crash rate and heartbeat by device class |
| Print Join Size Breakdown | Studio setting | Prints the largest instances replicated on join |

Scene Analysis splits triangles into categories: shadows, opaque, transparent, terrain, grass, particles, sky and UI. Use it to see whether the triangle count comes from geometry, or from shadow passes and transparency overdraw. The same data is exposed to AI tools through `SceneAnalysisService` (`GetInstanceCompositionAsync`, `GetScriptMemoryAsync`, `GetUnparentedInstancesAsync`, `GetTriangleCompositionAsync`, `GetAnimationMemoryAsync`, `GetAudioMemoryAsync`) via the Studio MCP **[version-sensitive]**.

### Reading the MicroProfiler

- **Bar colours:** orange bars are jobs (scripts, physics, animation). Blue bars are rendering. **Red** bars are rendering plus a GPU wait over 2.5 ms, which means you are GPU-bound: fill-rate, overdraw or too many pixels of transparency.
- **Threads:** Main, Worker and Render (prepare, perform, present).
- **Pausing:** press Ctrl+P to pause a capture, then zoom into a spike frame.
- **Dumps:** saved dumps go to `%LOCALAPPDATA%\Roblox\logs` and open in a browser. The web viewer has an **X-Ray** memory view, **flame graphs** and **diff flame graphs**. Diff two dumps before and after a change.
- **Server profiling:** in the Developer Console you can record up to 60 frames, with up to a 4 s delay.
- **Mobile profiling:** enable the MicroProfiler in the Roblox settings on the phone. Then open `http://<phone-ip>:1338` from a computer on the same network. Append `/90` (or another number) to capture more frames.
- **Assistant analysis:** the Studio Assistant and the Studio MCP can analyse a paused capture **[version-sensitive]**.

Label your own code so it shows up by name:

```lua
local RunService = game:GetService("RunService")

RunService.PostSimulation:Connect(function(dt)
	debug.profilebegin("Enemies.UpdateTargets")
	updateTargets(dt)
	debug.profileend()
end)
```

### Tags that point at content problems

| MicroProfiler tag | Meaning | Usual fix |
|---|---|---|
| `physicsStepped` / `worldStep` | Physics cost | Anchor static geometry, lower collision fidelity, fewer constraints, check adaptive stepping |
| `stepContacts` | Contact pair cost | Simpler collision shapes; boxes are cheaper than complex meshes |
| `stepWorldThrottled` | Physics overloaded; only real-time assemblies simulate | Reduce unanchored assemblies |
| `stepHumanoid`, `stepAnimation` | Humanoid and animation cost | Disable unused HumanoidStates; use AnimationController NPCs; animate NPCs on the client |
| `updateInvalidatedFastClusters` | Avatar or skinned-mesh cluster rebuilds. Above about 4 ms is a problem | Don't change avatar parts every frame; add a Humanoid to models with moving skinned meshes; split huge models |
| `Prepare` / `Perform` / `computeLightingPerform` / `LightGridCPU` / `ShadowMapSystem` | Lighting and shadow cost | Fewer shadow-casting lights, smaller ranges, `CastShadow = false` on small or moving parts |
| `UpdateView` / `RenderView` | Scene submission cost | Fewer draw calls (instancing, merging), fewer unique materials |
| `Pass3dAdorn` | BillboardGuis and adornments | Fewer world-space BillboardGuis; pool them |
| `fillGuiVertices` | UI geometry rebuilds | Avoid UIGradient and UICorner on text-heavy, constantly changing elements; consider CanvasGroup (costs memory) |
| `Dispatch StreamJob` | Streaming cost | Lower StreamingTargetRadius |
| `Sound/stepInstances` | Many playing sounds | Fewer simultaneous sounds |
| `ProcessPackets`, `Allocate Bandwidth and Run Senders` | Network | Fewer and smaller remotes; send deltas; no server-side tweens |
| `WaitingHybridScriptJob` | Resuming yielded threads | Fewer `task.wait` loops; event-driven code |
| GC entries | Garbage collection | Pool tables; avoid allocations in hot loops |

The tag table also has a transparency rule. The renderer treats transparency ≤ 0.01 as **opaque**, and anything between 0.01 and 1 as **transparent**, which is sorted and overdrawn. Parts cast shadows **regardless of transparency**, so a fully transparent helper part must also have `CastShadow = false`. This matters for house rule 2's invisible collision hulls.

Sources: creator-docs:performance-optimization/identify.md, creator-docs:performance-optimization/microprofiler/index.md, creator-docs:performance-optimization/microprofiler/use-microprofiler.md, creator-docs:performance-optimization/microprofiler/tag-table.md, creator-docs:performance-optimization/scene-analysis.md, creator-docs:performance-optimization/improve.md

## 5.3 Luau performance idioms

Most Roblox frame-time problems are not about raw Luau speed. They come from doing the wrong work too often: per-frame loops that should be events, unbounded raycasts, and creating instances every frame. Fix the algorithm first. Then use the idioms below for genuinely hot code.

### Structural rules (biggest wins)

1. **Event-driven before polling.** Use `GetPropertyChangedSignal`, `CollectionService` tag signals, `Touched` (with caveats, see 5.6) and remotes rather than `while true do task.wait() end` loops.
2. **Chunk long work.** Split it into about 5 ms slices per frame. Spread map generation, inventory rebuilds and bulk DataStore work across frames:

```lua
local BUDGET = 0.005 -- 5 ms
local function processInSlices(items, fn)
	local start = os.clock()
	for i, item in items do
		fn(item)
		if os.clock() - start > BUDGET then
			task.wait()
			start = os.clock()
		end
	end
end
```

3. **Disconnect everything you connect.** Clean up when a screen closes, an NPC despawns or a player leaves. Player and character instances are **not** destroyed automatically. Either set `Workspace.PlayerCharacterDestroyBehavior` **[version-sensitive: newer property]** or clean up manually:

```lua
local Players = game:GetService("Players")
Players.PlayerAdded:Connect(function(player)
	player.CharacterRemoving:Connect(function(character)
		task.defer(character.Destroy, character)
	end)
end)
Players.PlayerRemoving:Connect(function(player)
	task.defer(player.Destroy, player)
end)
```

Also remove per-player entries from your own tables in `PlayerRemoving`.

4. **Parallel Luau** (Actors plus `task.desynchronize`) suits large, independent computations such as pathfinding batches, procedural generation and many raycasts. Moving work into Actors has real overhead, so measure first.

### Language-level idioms (from the Luau performance guide)

- **Constant-key field access is fast** when the table has no metatable and the shape stays the same. Build objects with a table literal containing all fields at once, so every instance gets the same shape:

```lua
-- good: one shape, preallocated
local function newBullet(pos: Vector3, vel: Vector3)
	return { pos = pos, vel = vel, age = 0, alive = true }
end
```

- **Metatables:** point `__index` at a table, not a function. Call methods as `obj:Method()`. Caching methods in locals "is not productive", because the VM already optimizes method calls.
- **Imports:** globals like `math.max` are resolved at load time. `getfenv`, `setfenv` and `loadstring` **deoptimize** the whole script. Never use them.
- **Fastcalls:** builtins like `math.floor`, `string.byte(s)`, `bit32.*`, `vector.*` and `buffer.*` are fastcall-optimized. `string.byte(s)` is faster than `s:byte()`.
- **Iteration:** use generalized iteration (`for k, v in t do`). It is the recommended and fast form. `#t` is effectively O(1).
- **Preallocate:** use `table.create(n)` and indexed fill instead of repeated `table.insert` for known sizes.
- **Avoid temporary tables and closures in hot loops.** A closure with no upvalues, or only module-level immutable upvalues, is cached and free. A closure that captures loop variables allocates every time.
- **Vectors:** the native `vector` type (and `Vector3`) has SIMD-friendly math. The 2025 additions include the `vector` library, `math.map`, `math.lerp`, `math.isnan`, `math.isinf`, `math.isfinite`, `buffer.readbits` and `buffer.writebits`, plus better constant folding **[version-sensitive: 2025 runtime recap]**.
- **GC:** the garbage collector is incremental. Pool short-lived tables in high-frequency systems such as bullets, damage numbers and particles driven by Luau. Weak tables can be made shrinkable with `__mode = "s"`.
- **Inlining:** O2 inlining and loop unrolling apply to **local** functions. Keep hot helpers `local function`.

### Native code generation

Mark a whole script with `--!native` at the top, or mark a single function with the `@native` attribute. Facts **[version-sensitive]**:

- Native execution is supported only for **server scripts and Android clients**. Other clients run the normal interpreter.
- It helps most for math-heavy, table-heavy and `buffer`-heavy code: procedural generation, pathfinding, simulation, compression.
- It **costs compile time at startup and memory**, and there is a total size limit. Limits are 64K instructions per block, 32K blocks per function and 1M instructions per module. Do **not** mark every script native.
- Type annotations matter. Annotate parameters such as `v: Vector3` so the compiler can specialize.
- Breakpoints disable native execution for that script. Check code size with `debug.dumpcodesize()`.

```lua
--!native
--!strict
local function integrate(positions: {Vector3}, velocities: {Vector3}, dt: number)
	for i = 1, #positions do
		positions[i] += velocities[i] * dt
	end
end
```

### Anti-patterns

- Running work every frame in `Heartbeat`, `PreRender` or `PreSimulation` that could run on change or at 5–10 Hz.
- Creating `RaycastParams` or `OverlapParams` every call. Create them once and reuse them.
- Server-side tweens of world objects. These replicate every property step; tween on the client instead (see 5.9).
- `LoadAnimation` called repeatedly for the same animation. It always creates a new track. Use `Animator:GetTrackByAnimationId()`.
- Using `RequestQueueSize` or "wait until everything is loaded" loops as a loading gate (see 5.12).

Sources: luau-lang__site:src/content/docs/guides/performance.md, luau-lang__site:news/2025-12-19 runtime recap, creator-docs:luau/native-code-gen.md, creator-docs:performance-optimization/design.md, creator-docs:performance-optimization/improve.md, creator-docs:reference/engine/classes/Animator.yaml

## 5.4 Rendering: draw calls, instancing, transparency, shadows and LOD

### Instancing is the core rendering idea

Roblox batches identical meshes into one draw call (GPU instancing). Two MeshParts can share a draw call when **all** of these hold:

1. They share the same `MeshContent` (MeshId). The copies must reuse one uploaded mesh asset, not two uploads of identical geometry.
2. If they have a `SurfaceAppearance`, the SurfaceAppearances are identical.
3. With no SurfaceAppearance, their `TextureContent` must match.
4. With neither, their materials must match.

Consequences for a Blender pipeline:

- **Upload each kit piece once and reuse its ID everywhere.** Never re-import a prop for each placement. Re-importing a whole scene in one go creates duplicate IDs: 40 identical lamp posts become 40 meshes and 40 draw calls instead of 1. Packages keep IDs shared (see 5.7). This script audits duplicates:

```lua
local seen = {}
for _, d in workspace:GetDescendants() do
	if d:IsA("MeshPart") then
		local key = d.Name
		seen[key] = seen[key] or {}
		seen[key][d.MeshId] = true
	end
end
for name, ids in seen do
	local n = 0
	for _ in ids do n += 1 end
	if n > 1 then warn(name, "has", n, "different MeshIds — duplicate uploads?") end
end
```

- **Share SurfaceAppearances.** A shared trim-sheet SurfaceAppearance across many kit pieces keeps texture memory low. It does not merge different meshes into one draw call, though, because instancing still needs the same mesh.
- **Tint instead of new textures.** `SurfaceAppearance.Color` is a free multiplier. One near-white texture can produce many colour variants without new texture memory. Check before relying on it that tint variants still instance together in your build; the docs say the SurfaceAppearance must be identical.
- **Merge late, merge static.** The environmental-art curriculum merged a tower from 8 draw calls to 1 by combining meshes that always appear together and never move. Merge only after layout is final, and only for unique, static clusters. Keep repeated pieces separate so they instance.
- Decals, Textures and particles batch poorly. Prefer UV-mapped detail baked into a trim sheet over stacking Decals.

### Transparency

- Use only **0 or 1** wherever possible. Values between 0.01 and 1 are sorted and blended, which causes overdraw. Layered transparent surfaces (glass behind glass, foliage cards behind fog particles) multiply the GPU cost. This is the classic red-bar GPU-bound case on mobile.
- Avoid the `Glass` material and partially transparent Decals in large numbers, especially in VR.
- For foliage, prefer **cutout** alpha. Set SurfaceAppearance `AlphaMode = Transparency` with `MeshPart.Transparency = 0`, which gives a cutout. Smooth blending only starts at a part Transparency of at least 0.02.

### Shadows and lights

- Shadows are disabled below graphics quality level 4. Don't rely on them for gameplay readability.
- Set `CastShadow = false` on small props, distant geometry, fast-moving parts, particles' host parts and **every invisible helper part**. Invisible parts still cast shadows.
- For local lights, turn off `Light.Shadows` unless the shadow matters. Keep `Range` and `Angle` as small as the look allows, and use fewer lights. A PointLight inside an `Attachment` is the cheap way to place a bulb.
- Under the Realistic lighting style, indoor spaces need closed walls at least 1 stud thick, or outdoor light leaks inside. The indoor-lighting tutorial wraps mesh walls with parts at least 2.5 studs thick. For house rule 2, those blockers must be **invisible** (Transparency 1, CastShadow on only if they are meant to block light, CanCollide off unless they double as collision). Better still, author the walls in Blender with real thickness. More in 5.8.

### Level of detail

Roblox does not import hand-made LOD chains. Use these engine systems instead:

| System | What it does | Setting |
|---|---|---|
| `MeshPart.RenderFidelity` | Automatic mesh LOD. Automatic uses highest detail under 250 studs, medium from 250–500, lowest beyond 500. Performance is always reduced. Precise is always full | Use Automatic for most meshes, Performance for foliage and clutter, Precise sparingly (hero close-ups only) |
| **SLIM** **[version-sensitive]** | Cloud-generated composite LOD meshes for whole Models and avatars; combines parts into fewer draw calls | `Model.LevelOfDetail = Enum.ModelLevelOfDetail.SLIM` on static models; `Workspace.EnableSLIMAvatars = Enabled` |
| Legacy `StreamingMesh` | Older imposter LOD for streamed-out models | Convert to SLIM |
| Streaming radius | Content beyond `StreamingTargetRadius` is not on the client at all | See 5.5 |
| Frustum and occlusion culling | Automatic. Room or portal culling (hiding interiors) is manual | Use `ModelStreamingBehavior` or scripted parenting for interiors |

SLIM requirements: StreamingEnabled, a place saved to Roblox (cloud transcoding), and Team Create enabled. It works on static models without a Humanoid. Keep each SLIM model's extent compact; the docs suggest about 64 studs. Separate co-planar overlapping faces by about 0.01 studs to avoid z-fighting in the merged mesh. In the docs' avatar example, SLIM cut far-away avatars from about 2.6 M to about 170k triangles, and near ones from about 670k to about 100k.

### Other renderer costs

- **Skinned meshes** inside a Model with no Humanoid rebuild FastClusters every time they move. Putting a Humanoid (or the right controller setup) in the model avoids it. Very large models with many parts also trigger rebuilds; split them.
- **Highlights:** only 255 can show at once; extras are silently ignored. The first visible Highlight costs up to about 1 ms of GPU time on mobile, and later ones are cheap. Adding or removing a Highlight forces a geometry rebuild, so toggle `Enabled` instead of creating and destroying. Mobile cost grows with screen coverage.
- **SurfaceGuis and BillboardGuis** cost CPU and render time. Many complex SurfaceGuis are specifically called out as costly for VR.
- **Particles:** fill-rate scales with screen pixels covered and with overlapping layers (see 5.9).
- **Built-in materials over custom textures.** Roblox materials and MaterialVariants share engine textures. Custom per-asset textures add memory. Under the Blender-only rule, keep a small shared trim-sheet library (see 5.7) instead of unique textures per asset.

Sources: creator-docs:performance-optimization/improve.md, creator-docs:performance-optimization/design.md, creator-docs:performance-optimization/microprofiler/tag-table.md, creator-docs:parts/meshes.md, creator-docs:workspace/streaming/slim.md, creator-docs:art/modeling/surface-appearance.md, creator-docs:effects/highlighting.md, creator-docs:effects/light-sources.md, creator-docs:tutorials/curriculums/environmental-art/optimize-your-experience.md, creator-docs:tutorials/use-case-tutorials/lighting/enhance-indoor-environments.md

## 5.5 Instance streaming: settings and designing code around it

Streaming is the single most important memory lever. The docs rank it first for asset memory. It is on by default for new places, and `StreamingEnabled` cannot be changed by script at runtime.

### Recommended settings

| Property | Recommended | Notes |
|---|---|---|
| `Workspace.StreamingEnabled` | true | Default for new places |
| `ModelStreamingBehavior` | Improved | Non-atomic models stream more sensibly than Legacy |
| `StreamingIntegrityMode` | PauseOutsideLoadedArea | Pauses the player if they reach unloaded space instead of letting them fall through |
| `StreamingMinRadius` | 64 (default) | Guaranteed-loaded radius around the focus |
| `StreamingTargetRadius` | 1024 (default); lower it for memory | Must be **larger** than MinRadius to leave a buffer. Lowering it is the main memory and `Dispatch StreamJob` fix |
| `StreamOutBehavior` | Opportunistic | Streams out beyond the target radius even without memory pressure |
| `EnableSLIMAvatars` | Enabled **[version-sensitive]** | Cheap distant avatars |
| `PredictiveStreamingMode` | Enabled (opt-in) **[version-sensitive]** | Prefetches the spawn area and returns to recent CFrames |
| `Player.FrustumStreaming` | Automatic, or test Enabled **[version-sensitive]** | Server-side per-player setting: Default, Disabled, Automatic, Enabled. Under Opportunistic stream-out, out-of-view instances linger 1.5 s. Frustum streaming has no occlusion awareness, and its cost adds to normal radius streaming |

### How streaming behaves

- Only **Workspace descendants** stream. ReplicatedStorage content replicates in full at join. Don't park the whole map in ReplicatedStorage; server-only assets belong in ServerStorage.
- Streamed-out instances are parented to `nil`, not destroyed. Your references stay valid, but property reads can be stale.
- Instances created on the client are never streamed out.
- Unanchored **assemblies** stream in whole. Anchored geometry streams **per part**, so a wall made of 10 anchored MeshParts can appear piece by piece. Use model streaming modes to control this.
- `Player.ReplicationFocus`, plus `AddReplicationFocus` and `RemoveReplicationFocus`, add extra streaming centres for cutscene cameras or remote-controlled drones. Each extra focus costs about as much as another player.
- **Debug view:** press Shift+F3, then Shift+1 to cycle to the 4th panel. It shows the streaming regions in red, yellow, blue and green.

### Model streaming modes

| `Model.ModelStreamingMode` | Behaviour | Use for |
|---|---|---|
| Default / Nonatomic | Parts stream individually; the model container may arrive empty | Large static scenery |
| **Atomic** | The whole model and its descendants arrive together. `WaitForChild` the model, then use its children freely | Interactive props: doors, vending machines, shop counters, vehicles |
| Persistent | Always present; `workspace.PersistentLoaded` signals arrival | **Rarely.** Global landmarks only. Every persistent model is join-time memory |
| PersistentPerPlayer | Persistent for players added with `Model:AddPersistentPlayer()` | A player's own plot or base in a tycoon |

Flatten hierarchies. Break up "container" models whose only job is grouping, so streaming can unload pieces independently.

### Designing code around streaming

Nearly every streaming bug is a client script assuming an instance exists. Rules:

1. **Never index straight into Workspace content from a LocalScript.** Use `WaitForChild` with a timeout, or `FindFirstChild` with a nil check:

```lua
local door = workspace:WaitForChild("ShopDoor", 10)
if not door then return end -- streamed out or not yet arrived; handle gracefully
```

2. **Use CollectionService tags plus added and removed signals as the main pattern** for anything interactive:

```lua
local CollectionService = game:GetService("CollectionService")

local function onAdded(inst: Instance)
	if inst:GetAttribute("Spawned") then
		-- already played spawn FX on a previous stream-in; just bind behaviour
	else
		inst:SetAttribute("Spawned", true) -- client-side flag
		playSpawnFX(inst)
	end
	bindInteraction(inst)
end
local function onRemoved(inst: Instance)
	unbindInteraction(inst) -- disconnect, stop sounds, destroy client VFX
end

for _, inst in CollectionService:GetTagged("Interactable") do onAdded(inst) end
CollectionService:GetInstanceAddedSignal("Interactable"):Connect(onAdded)
CollectionService:GetInstanceRemovedSignal("Interactable"):Connect(onRemoved)
```

3. **Spatial queries only see streamed content.** `GetChildren`, raycasts, `GetBoundingBox` and overlap queries on the client see only what is loaded. Store bounds and gameplay metadata in **attributes** on always-present containers, or keep gameplay checks on the server.
4. **Sounds, BillboardGuis, ProximityPrompts, Touched handlers and ClickDetectors stop working when their part streams out.** Put critical prompts in Atomic models near where they are used, and design for prompts that only appear near the player. That is how prompts should behave anyway.
5. **Teleports:** call `player:RequestStreamAroundAsync(position)` on the server before `PivotTo`, so the destination is loaded when the player lands.
6. **The loading screen must never wait on a spatial instance.** It might never stream in. Wait on `game.Loaded` and on non-spatial UI assets (see 5.12).
7. **Custom pause handling:** call `GuiService:SetGameplayPausedNotificationEnabled(false)`, then react to `player.GameplayPaused` with your own branded overlay.
8. **Test with `StreamingTargetRadius = 64`** to force streaming edge cases early. An AI skill named `rbx-convert-to-streaming` exists in the Studio agent tooling **[version-sensitive]**.

Sources: creator-docs:workspace/streaming/index.md, creator-docs:workspace/streaming/techniques.md, creator-docs:workspace/streaming/slim.md, creator-docs:workspace/streaming/frustum.md, creator-docs:performance-optimization/improve.md

## 5.6 Physics: assemblies, collision, queries and network ownership

### Assemblies, anchoring and sleep

- An **assembly** is a set of parts rigidly joined by welds or Motor6Ds. It simulates as one rigid body. Forces, velocity, mass and network ownership all apply per assembly.
- The **root part** is chosen in this order: anchored parts first, then non-Massless parts, then higher `RootPriority`, then size. Seats and VehicleSeats get a size multiplier, followed by HumanoidRootPart and then Torso.
- **Anchor all static world geometry.** Anchored parts are not simulated and are owned by the server. For a welded mechanism, anchor **only the root**. Anchoring every part splits the mechanism into more assemblies. The environmental-art guidance is "anchor everything except doors" (and other intentional mechanisms). Anchoring saves physics CPU. Rendering cost does not change, despite one tutorial's loose claim that it saves GPU.
- **Sleep system:** non-moving assemblies stop simulating. Thresholds:

| Threshold | Value | Direction |
|---|---|---|
| Linear velocity | 0.33 studs/s | Below this, awake can go to sleeping |
| Rotational velocity | 0.42 studs/s | Below this, awake can go to sleeping |
| Linear and rotational acceleration | 0.24 studs/s² | Above this, an assembly cannot fall asleep |
| Neighbor linear velocity | 0.48 studs/s | Above this, sleep-checking goes to awake |
| Neighbor rotational velocity | 0.59 studs/s | Above this, sleep-checking goes to awake |
| Wake linear and rotational acceleration | 16.9 studs/s² | Above this, sleep-checking goes to awake |

  Things that wake an assembly include: a collision with an assembly moving faster than 1 stud/s, any physics property change (Anchored, velocity, CanCollide, CanTouch, CustomPhysicalProperties, Massless, RootPriority), impulses, Workspace gravity, wind or air density changes, constraint creation or property changes, an occupied VehicleSeat, and being inside an Explosion's BlastRadius. **Anti-pattern:** a script that writes a physics property on idle props every frame keeps them all awake. Actuated joints (Motor or Servo hinges, LinearVelocity, AlignPosition with `RigidityEnabled = false`, winch ropes and others) use a stricter sleep threshold, so slow mechanisms keep moving. Debug sleep with Visualization Options > **Awake parts**: red is awake, orange is sleep-checking, and no outline means asleep.

- **Adaptive timestepping** (`Workspace.PhysicsSteppingMethod = Adaptive`) is recommended and gives up to **2.5×** physics speedup. The solver puts assemblies into 240, 120 or 60 Hz islands. It shows as `worldStep - Adaptive` in the profiler. In `LDLPGSSolver::solve` the islands are listed as 1dt (240 Hz), 2dt (120 Hz) and 4dt (60 Hz). Use **Fixed** (240 Hz) only for racing games, destruction simulations or complex mechanisms such as tanks. Also use it when most parts end up at 240 Hz anyway, because mixing islands converts neighbours to 240 Hz with overhead. Visualize with Studio Settings > Physics > **Are Timesteps Shown**.
- Lower `Workspace.FallenPartsDestroyHeight` to an appropriate value for your map, so falling debris is destroyed early.

### CollisionFidelity per asset type

Fidelity order, cheapest first: **Box, Hull, Default, PreciseConvexDecomposition**. A newer **Tunable** option adds a `CollisionPrecision` slider **[version-sensitive]**. Collision geometry is stored in memory (**PhysicsParts**) **even when `CanCollide` is false**. Non-colliding meshes should therefore still be set to Box.

| Asset type | Fidelity | Flags | Notes |
|---|---|---|---|
| Small props (cans, books, bottles) | Box | CanCollide on if the player can bump it; CanQuery off unless it's a hit target | Cheapest; a box is fine for anything under knee height |
| Medium props (crates, benches, lamps, bins) | Hull | CanCollide on | A convex hull wraps the silhouette. Watch for L-shapes and concave props, whose hulls fill the gap |
| Large walls, floors, cliffs | Box per module, or a separate simple collision mesh | CanCollide on, CanQuery on (so raycasts and lasers hit) | Modular walls are naturally boxy; keep modules convex |
| Trims and edges near jump paths | Hull | | Matches the curriculum guidance |
| Doorways, arches, stairs, anything concave the player walks *through* or *on* | PreciseConvexDecomposition sparingly, **or** split into convex pieces, **or** an invisible collision mesh | | Precise only where navigation needs it. Find all precise parts with the Explorer filter `CollisionFidelity=PreciseConvexDecomposition` |
| Foliage, grass cards, hanging cables, decals-on-mesh | Box | CanCollide **off**, CanTouch off, CanQuery off | Leaves are not "solid objects" for house rule 2. Tree **trunks** are solid, so give the trunk its own Hull or Box collision |
| Ragdolls and debris | Box or Hull | NoCollision constraints between limbs | Fewer contact pairs |
| Vehicles | Simplified hull mesh | Collision group "Vehicles" | Visual mesh with CanCollide off |

### Making everything solid under house rule 2

Every visible object must block players and NPCs. There are three ways to achieve that, from cheapest to most accurate.

1. **Fidelity on the visual mesh.** Use Box or Hull on the visual MeshPart with `CanCollide = true`. This is right for most props. It costs nothing extra and needs no extra instances.
2. **A separate Blender collision mesh** (recommended for architecture and complex shapes). Model a low-poly convex proxy in Blender named `<Asset>_COL`. Export it with the asset, and after import set:
   - The `_COL` part to `Transparency = 1`, `CanCollide = true`, `CanQuery = true` (if raycasts should hit it), `CanTouch = false`, `CastShadow = false` and `CollisionFidelity = Hull` (or Default for a multi-piece proxy). Anchor it, or weld it to the visual root.
   - The visual mesh to `CanCollide = false`, `CanTouch = false`, `CollisionFidelity = Box` (to minimize stored collision data), and CanQuery off unless clicks or raycasts target it.

   Roblox has **no `UCX_`-style automatic collision convention**. The `_COL` suffix is a house convention, applied by a post-import script (see 5.7).
3. **Invisible primitive hull Parts.** Box or wedge Parts with `Transparency = 1` are allowed by the house rule *as collision hulls*. Use them for large simple volumes (a building's walls) where a `_COL` mesh would be overkill. Same flags as above. They must never be visible: verify with a pre-launch scan (5.13).

Precision matters for feel. A Box on a lamp post makes players bump into air beside the pole. A Hull on an archway seals the arch. Walk every asset with a character before shipping.

### CanCollide, CanTouch and CanQuery are separate decisions

| Flag | Controls | Turn off when |
|---|---|---|
| `CanCollide` | Physical blocking | Foliage, VFX hosts, visual meshes that have a separate `_COL` proxy, triggers |
| `CanTouch` | Whether `Touched` and `TouchEnded` fire | Almost everything except deliberate trigger volumes. It saves touch processing |
| `CanQuery` | Whether raycasts and overlap queries see the part (only when CanCollide is off) | Decorative meshes that shouldn't block clicks, camera rays or weapons |

**Invisible trigger volume:** `Transparency = 1`, `CanCollide = false`, `CanTouch = true` (if you use Touched) or CanQuery true (if you poll with overlap queries), `CastShadow = false`, `Anchored = true`. If you use spatial queries, also set `OverlapParams.RespectCanCollide` deliberately, because it changes which flag the query honours.

### Collision groups

Register groups **from one script** (or the Collision Groups editor) at server start. The old PhysicsService collision-group methods are deprecated and forward to Workspace.

```lua
local Workspace = game:GetService("Workspace")
Workspace:RegisterCollisionGroup("Players")
Workspace:RegisterCollisionGroup("NPCs")
Workspace:RegisterCollisionGroup("Debris")
Workspace:CollisionGroupSetCollidable("Players", "Players", false) -- no player-player blocking
Workspace:CollisionGroupSetCollidable("Debris", "Players", false)  -- cosmetic debris never blocks
-- assign: part.CollisionGroup = "Debris"
```

The `StudioSelectable` group controls editor selection. `NoCollisionConstraint` handles single part-to-part exceptions such as a ragdoll's limbs. **House-rule caution:** turning off player-versus-world collision for any visible object breaks rule 2. Use groups only for player-player, debris and cosmetic cases.

### Touched versus spatial queries

- `Touched` fires only from **physical movement**, not from CFrame or PivotTo moves. It needs a debounce. It is **spoofable** when the client owns the touching part. Treat it as a hint and validate on the server.
- **Collision summaries** (`BindToCollisionSummaries`) **[version-sensitive]** report per-frame contacts. They exist only on the network owner, and parts with `CanCollide = false` don't produce them.
- **Use spatial queries for gameplay.** Use `Workspace:Raycast` for lines, `GetPartBoundsInBox` or `GetPartBoundsInRadius` for cheap volume checks, `GetPartsInPart` for exact shapes (more expensive), and `Blockcast`, `Spherecast` or `Shapecast` for fast projectiles that would tunnel. Reuse params, cap `MaxParts`, and deduplicate hits by model:

```lua
local params = OverlapParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude
params.FilterDescendantsInstances = { attackerCharacter }
params.MaxParts = 64
local hit = {}
for _, part in workspace:GetPartBoundsInBox(hitboxCFrame, hitboxSize, params) do
	local model = part:FindFirstAncestorOfClass("Model")
	if model and not hit[model] and model:FindFirstChildOfClass("Humanoid") then
		hit[model] = true
		validateAndDamage(model) -- server-side checks: range, cooldown, line of sight
	end
end
```

The server must check the ray origin against the server-known character position. Never accept a client-supplied origin as proof of a hit.

### Network ownership

- Anchored parts are always owned by the server. Unanchored assemblies near a player's character are **automatically** given to that client. That makes them responsive, but the client can then fake their physics.
- Use `part:SetNetworkOwner(player)` for things a player drives, and `SetNetworkOwnershipAuto()` to hand back. Use `SetNetworkOwner(nil)` (server ownership) **sparingly**, for gameplay-critical loose objects, because it costs server CPU and adds latency for players.
- **Vehicles:** give the driver ownership when they sit, and put every loose part of the vehicle under the same owner:

```lua
local seat: VehicleSeat = script.Parent
seat:GetPropertyChangedSignal("Occupant"):Connect(function()
	local humanoid = seat.Occupant
	if humanoid then
		local player = game.Players:GetPlayerFromCharacter(humanoid.Parent)
		if player then seat:SetNetworkOwner(player) end
	else
		seat:SetNetworkOwnershipAuto()
	end
end)
```

- Visualize owners in Studio's ownership debug view. The outline colours mean:
  - **Green:** your client owns and simulates the part.
  - **Red:** a buffer zone. Your client simulates the part, but something else still owns it.
  - **White/grey:** the server or another client owns it.
  - **Black:** nobody owns it, so physics does not apply.
- **[version-sensitive]** When `Workspace.AuthorityMode = Server`, the server owns the simulation, and clients predict parts near their character with rollback (`RunService:SetPredictionMode()`). In this mode, drive predicted forces from `RunService:BindToSimulation()` on both sides. This is a newer model, so check the live docs before adopting it.

### Humanoids and NPCs (physics-adjacent CPU)

- Disable HumanoidStateTypes you don't use (Climbing, Swimming, Ragdoll and so on) with `Humanoid:SetStateEnabled`.
- Use **AnimationController** instead of a Humanoid for static NPCs (shopkeepers, workers). For moving NPCs, use a custom controller plus AnimationController.
- Play NPC animations **on the client**. Spawn NPCs only near players, and **pool** them.
- Animate through `Motor6D.Transform` in PreSimulation, not by writing C0 or C1.
- Attach accessories and held items outside the avatar model when possible, to avoid FastCluster rebuilds.

Sources: creator-docs:physics/assemblies.md, creator-docs:physics/sleep-system.md, creator-docs:physics/adaptive-timestepping.md, creator-docs:physics/network-ownership.md, creator-docs:workspace/collisions.md, creator-docs:parts/meshes.md, creator-docs:performance-optimization/improve.md, creator-docs:tutorials/curriculums/environmental-art/optimize-your-experience.md, gamedev-skills__awesome-gamedev-agent-skills:skills/other-engines/roblox-physics/SKILL.md


## 5.7 The Blender-to-Roblox art pipeline

This is the most important subsection for this knowledge base. House rules 1 and 2 require that every visible object is a Blender model with proper collision. The pipeline below is built for that. It reuses meshes so they instance and share textures so memory stays low. It also gives a cohesive, hand-made look instead of a generic one.

### Pipeline overview

1. **Style bible and kit plan.** Fix the palette, texel density, bevel standard, trim-sheet set and grid before modelling anything (see "Cohesive art style" below).
2. **Author in Blender through the Blender Lab MCP add-on bridge.** The game repo's `tools/blender_exec.py` sends Python to the running Blender. Use the bridge for modelling, validation and scene layout, but not for export.
3. **Validate inside Blender** with a script: triangle counts, applied transforms, one material per mesh, one UV map, naming, `_COL` proxies present.
4. **Export GLB in a separate headless process,** `blender -b <file>.blend --python export_glb.py -- <asset> <out.glb>`. Export is deterministic and repeatable, and it never touches the artist's open session.
5. **Upload through the Open Cloud Assets API** (`POST /assets/v1/assets`, `model/gltf-binary`). Poll the operation, and record the resulting asset ID in a manifest.
6. **Insert into Studio,** through the Studio MCP, the Toolbox or Asset Manager. Run a **post-import fix-up script** that applies anchoring, collision flags, `_COL` handling, CastShadow, RenderFidelity and shared SurfaceAppearances.
7. **Wrap each kit piece or prop as a package** (PackageLink with AutoUpdate on). Place copies of the package, never fresh imports.
8. **QA in Studio** under the final lighting at a low graphics quality level and on a real phone (see 5.13).

### Units, scale and orientation

- **1 stud = 0.28 m**, so 1 m ≈ 3.57 studs. Gravity is 196.2 studs/s², which is about 35 m/s². Roblox gravity is deliberately floaty, so real-world physical scale isn't sacred.
- **Studio treats incoming units as studs.** A 2-unit Blender cube imports as 2 studs with the default importer Scale Unit = Stud. That is the simplest and recommended convention: **1 Blender unit = 1 stud**. In Blender set Scene > Units > Unit System = **None** (or Metric with Unit Scale 1, read as studs) and Rotation = Degrees. glTF export needs no scale settings. FBX needs Apply Scalings = **FBX Unit Scale**.
- If an asset was modelled at real metric scale, import it with Scale Unit = **Meter** so it is multiplied by about 3.57. Don't mix the two conventions inside one project. The `MeshScaleUnit` options are Stud, Meter, CM, MM, Foot and Inch.
- **Scale reference:** keep an R15 dummy (exported from Studio) in a hidden Blender collection. Roblox avatars are chunky, so doors, counters, steps and seats should be checked against the dummy, not against real-world human sizes. Studio's glTF export is **beta** and exports no animation **[version-sensitive]**.
- **Orientation:** export with Blender's +Y Up (glTF default). For FBX use Forward = **Z Forward** and Up = **Y Up**, as the Blender docs specify. In the Studio importer use World Forward = **Front** and World Up = **Top**. Model assets facing −Y in Blender (Blender's "front" view), then confirm once in Studio with a test asset that has an obvious front and lock the convention.
- **Transforms:** apply all transforms (rotation 0, scale 1) before export. For skinned meshes, bones must have scale 1 and rotation 0, the root at the origin, at most **4 influences per vertex**, and no influences on the root bone.

### Pivots and the modular grid

- **Pick one grid per project.** The environmental-art curriculum uses a **5-stud** grid. Every piece is at least 5 studs, and sizes are divisible by the smallest piece. Beyond the Dark used a **16-stud** grid for large sci-fi architecture. City and town games generally suit a 4- or 8-stud sub-grid for props and a 16-stud grid for building modules. Whichever you choose, write it into the style bible.
- **Modular kit pivots:** put the pivot at the **front-lower corner** of walls and floor pieces, so they snap edge-to-edge with Studio's grid snap and rotation in 90° steps.
- **Prop pivots:** put the pivot **where the prop attaches** to the world. That is bottom-centre for floor props (benches, lamps, bins), back-centre for wall props (signs, sconces) and top-centre for hanging props.
- **Importer:** **Use Imported Pivot** (default on) keeps the Blender origin. Set Pivot to Scene Origin (default on) and Insert Using Scene Position (default off) decide placement at insert time. For per-asset GLBs, place the asset's origin at world (0,0,0) in Blender before export, so all three settings agree.
- Moving models in code uses `Model:PivotTo()`, `MoveTo` or `TranslateBy`, and needs a PrimaryPart or WorldPivot. The pivot you author in Blender becomes the pivot every placement script uses.

### Mesh specifications and triangle budgets

Doc limits:

- **At most 20,000 triangles per mesh.** That is an import limit, not a target.
- Meshes should be **watertight**, have volume, contain **no n-gons**, and use quads where possible (the exporter triangulates).
- **One material per mesh.** A Blender object with three material slots becomes three primitives, which become three MeshParts in Studio. That is three draw calls and three collision shapes.
- **One UV set,** in 0–1 space. Overlapping UVs are allowed, for mirrored or stacked islands.
- Consistent normals. The importer has **Invert Negative Faces**, but fix normals in Blender instead. **Make Double Sided** costs extra rendering; use it only for foliage cards.

House triangle budgets for a mobile-first game:

| Asset class | Triangles | Example |
|---|---|---|
| Clutter (hand-sized) | 50–300 | Cans, books, cups |
| Small prop | 200–1,500 | Bins, signs, chairs, fire hydrants |
| Medium prop | 1,500–5,000 | Street lamps, vending machines, benches with detail |
| Vehicle | 5,000–15,000 (split body, wheels and glass into ≤ 4 meshes) | Delivery van |
| Modular building piece | 200–3,000 per piece | Wall 16×12, window frame, cornice |
| Hero landmark | Up to 20,000 per mesh, split into several meshes | Town hall clock tower |
| Character (NPC worker) | 4,000–10,000 | Skinned R15-compatible mesh |
| Collision proxy (`_COL`) | 12–200 | Convex boxes and hulls |

Spend triangles on the **silhouette and edge bevels**, not on flat interiors. The curriculum says props need only as much geometry as the silhouette requires. A 0.05–0.15 stud chamfer on hard-surface edges, with weighted or custom normals, catches light and reads as hand-made. Razor-sharp unbevelled boxes are the biggest single "cheap AI asset" tell.

### UVs, texel density and texture specs

- **Formats:** png, jpg, tga and bmp. Up to 4096² is technically supported, but treat **1024² as the max** for game assets. Both the UV spec and the curriculum say 1024, and memory scales with pixel count (see the contradictions list in 5.14).
- **Texel density, doc guidance:** 256² for a 5×5-stud object, 512² for 10×10 and 1024² for 20×20. That is about **51 px per stud**. A separate PBR guideline says 256² per 2×2×2 units (about 128 px/stud), max 1024². **House rule:** use about 50 px/stud for environment and architecture, and up to about 100 px/stud only for props seen at arm's length. Keep the density consistent across the whole kit; mismatched density is very visible.
- **Default material reference:** Roblox's built-in materials show 1024² across an 8×8-stud part face, and terrain shows 512² across 8×8 studs. Match those if you mix MaterialVariants with your trims.
- **Most textures 512² or less, minor ones 256² or less.** Images are transcoded, so file-size tricks don't save memory.
- **Unwrapping:** use **Follow Active Quads** on trim strips so they line up with the trim sheet's horizontal bands. Keep UVs in 0–1 as specified. If you rely on UV wrap beyond 0–1 for long trims, test it on a sample asset in Studio first. The spec doesn't promise it, so split long trims at seams if in doubt.

### PBR maps and SurfaceAppearance

| Map | Format | Notes |
|---|---|---|
| ColorMap | sRGB RGB(A) | Author **near-white or desaturated** if you will tint with `SurfaceAppearance.Color` |
| NormalMap | **OpenGL tangent space** (+Y up). Flat is (127,127,255) | Blender bakes OpenGL by default. Never use DirectX normals |
| RoughnessMap | 8-bit grayscale | Add about **+0.1** roughness to compensate for Roblox's Fresnel |
| MetalnessMap | 8-bit grayscale | Almost always pure 0 or pure 1 (metalness workflow) |
| Emissive | `EmissiveMaskContent`, `EmissiveStrength`, `EmissiveTint` **[version-sensitive: newer properties]** | Marketplace items must keep strength 0–40. For games, keep emissive subtle so Bloom doesn't blow out |

`SurfaceAppearance.AlphaMode` options:

- **Overlay** (default): the colour map's alpha reveals `MeshPart.Color` underneath. Useful for colour-tinted panels.
- **Transparency:** with `MeshPart.Transparency = 0` it acts as a **cutout**. Smooth blending starts at 0.02 or above.
- **TintMask:** alpha masks where `SurfaceAppearance.Color` applies.
- **Opaque:** **[version-sensitive: beta]**.

Other rules:

- SurfaceAppearance overrides MaterialVariant maps on the same MeshPart.
- SurfaceAppearance only works on meshes with UVs, so it does not work on Parts. That is irrelevant under the Blender-only rule.
- Most SurfaceAppearance properties can't be changed by scripts at runtime. Make variants as separate SurfaceAppearance instances.

**Recommended material architecture.** Do not embed a unique texture set in every GLB. Instead:

1. Bake or paint a **small shared library**. Use 4–8 square **trim sheets** at 1024² for the whole game (for example metal, wood, concrete, painted panels, signage, fabric), plus a few **tileables** for floors, walls and ground.
2. Upload each map once as an image asset. Build one SurfaceAppearance per material and name it with the **`_SA` suffix** (Beyond the Dark convention). Publish the set as a **package** that acts as the project's material library.
3. Import tileables as **MaterialVariants** with Set as Override and **Organic** tiling where repetition shows. They then apply to terrain-like surfaces and stay engine-shared.
4. Each mesh's single Blender material is just a **placeholder name** that matches a library entry, such as `M_Trim_Metal`. The post-import script swaps in the matching `_SA` clone.

The results: one texture memory cost for the whole city, consistent texel density, and consistent colour. Beyond the Dark built **90 % of its architecture** from a handful of trim-sheet sets made from a swappable template. Avoid unique details on trim sheets: a recognisable stain repeated on 200 walls looks worse than plain.

**Vertex colour** is a texture-free way to add variation such as dirt gradients, ambient occlusion and colour blocking (see art/blender.md). The importer can drop it with **Ignore Vertex Colors**, so leave that off if you rely on it.

### Naming and hierarchy

| Convention | Meaning | Origin |
|---|---|---|
| `SM_<Category>_<Name>_<Variant>` | Static mesh, for example `SM_Street_Lamp_A` | House |
| `SK_<Name>` | Skinned mesh | House |
| `KIT_<Set>_<Piece>_<WxH>_<Variant>` | Modular piece, for example `KIT_Shop_Wall_16x12_A` | House |
| `<Asset>_COL` | Invisible collision proxy (see 5.6) | House |
| `<Name>_Att` | Imported as an **Attachment**, for example a light bulb position, VFX socket or prompt anchor | Doc (importer) |
| `_OuterCage` / `_InnerCage` | Layered clothing cages | Doc (importer) |
| `<Name>_SA` | SurfaceAppearance | Beyond the Dark |
| `M_<Library>_<Name>` | Blender material placeholder matching a library SurfaceAppearance | House |

glTF imports as a **nested Model with one MeshPart per primitive**. Name collisions get a **`_Node`** suffix, so keep names unique within a file. Split multi-part assets into named child meshes, for example `Door`, `Frame`, `Handle_Att`. The curriculum recommends this so moving parts can animate and each piece can get the right collision.

**`_Att` empties are the hand-off between art and code.** Put `Prompt_Att` where a ProximityPrompt should sit, `Light_Att` where a PointLight goes, `VFX_Steam_Att` for emitters and `Seat_Att` for seating. Scripts then find attachments by name instead of hard-coding offsets.

### Collision authoring in Blender

This follows the policy in 5.6.

- For each asset, decide in the style bible whether it uses fidelity on the visual mesh (Box or Hull) or a `_COL` proxy.
- `_COL` proxies are convex (or a few convex pieces), have **no material**, are about 12–200 triangles, and sit inside or slightly outside the visual surface. Make walkable surfaces flush, so feet don't float.
- For doorways and arches, build the proxy from 3 boxes (two jambs and a lintel) instead of relying on PreciseConvexDecomposition.
- For stairs, use a single sloped proxy (a ramp) under the visual steps. Characters climb it smoothly, and it costs far less than per-step collision.
- Export the `_COL` objects in the same GLB as the visual mesh, so they arrive in one Model.

### Level of detail

There is no import path for hand-authored LOD chains. Build each asset to its budget and let the engine handle distance (5.4): `RenderFidelity` Automatic, Performance for clutter and foliage, **SLIM** on static models **[version-sensitive]**, and the streaming radius. For huge distant backdrops such as mountains or a skyline that players never reach, model a dedicated low-poly backdrop mesh rather than placing full-detail buildings far away.

### Headless export script

Run this in a **separate process**, never inside the MCP-connected session:

```python
# tools/export_glb.py
# usage: blender -b assets/street_props.blend --python tools/export_glb.py -- SM_Street_Lamp_A build/SM_Street_Lamp_A.glb
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
root_name, out_path = argv[0], argv[1]

bpy.ops.object.select_all(action="DESELECT")
root = bpy.data.objects[root_name]
for obj in [root, *root.children_recursive]:
    obj.hide_set(False)
    obj.select_set(True)
bpy.context.view_layer.objects.active = root

bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format="GLB",
    use_selection=True,       # "Limit to Selected"
    export_apply=True,        # apply modifiers (bevels, weighted normals)
    export_yup=True,          # +Y up
    export_texcoords=True,
    export_normals=True,
    export_materials="EXPORT",
    export_animations=False,
)
```

Exporter parameter names change between Blender releases. Pin the Blender version in the repo and check `bpy.ops.export_scene.gltf` options when upgrading. For FBX (needed for animations and for the FBX-only update endpoint), use Path Mode = **Copy** with **Embed Textures**, Apply Scalings = **FBX Unit Scale**, **Add Leaf Bones off** and **Bake Animation off** for static meshes. FBX holds only **one animation track** per file.

A pre-export validation run through the MCP bridge catches most import problems:

```python
import bpy, bmesh
MAX_TRIS = 20000
problems = []
for obj in bpy.data.objects:
    if obj.type != "MESH":
        continue
    if any(abs(s - 1) > 1e-4 for s in obj.scale):
        problems.append(f"{obj.name}: unapplied scale {tuple(obj.scale)}")
    if len(obj.data.uv_layers) != 1 and not obj.name.endswith("_COL"):
        problems.append(f"{obj.name}: {len(obj.data.uv_layers)} UV maps (need 1)")
    if len([m for m in obj.material_slots if m.material]) > 1:
        problems.append(f"{obj.name}: more than one material")
    bm = bmesh.new(); bm.from_mesh(obj.data)
    tris = sum(len(f.verts) - 2 for f in bm.faces)
    ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
    bm.free()
    if tris > MAX_TRIS: problems.append(f"{obj.name}: {tris} tris > {MAX_TRIS}")
    if ngons: problems.append(f"{obj.name}: {ngons} n-gons")
print("\n".join(problems) or "OK")
```

### Studio 3D Importer settings

Use these when importing by hand rather than through Open Cloud. Save them as an importer **preset**.

| Setting | Default | Recommended | Why |
|---|---|---|---|
| Import Only As Model | On | On | Model container |
| Upload to Roblox | On | On | Creates mesh asset IDs |
| Creator | User | **Group that owns the game** | Asset permissions follow the owner |
| Import as Package | Off | **On** for kit pieces and props | Shared IDs, AutoUpdate |
| Add to Workspace | On | On | Also grants the place permission to the asset |
| Insert Using Scene Position | Off | On for scene layouts; Off for single assets | Keeps the Blender layout |
| Set Pivot to Scene Origin | On | On | Matches the origin-at-zero export |
| Use Imported Pivot | On | On | Keeps the Blender pivot |
| Anchored | Off | **On** for static assets | Physics cost (5.6) |
| Scale Unit | Studs | Studs (1 BU = 1 stud) | |
| World Forward / Up | | Front / Top | |
| Merge Meshes | Off | Off; merge deliberately later | Merging breaks instancing |
| Make Double Sided | Off | Off (foliage only) | Rendering cost |
| Invert Negative Faces | | Off; fix in Blender | |
| Ignore Vertex Colors | | Off if you use vertex colour | |
| Uses Cage | | Only for layered clothing | |

The importer does **not de-duplicate meshes**. Import each kit piece once from its own file, then place package copies.

### Open Cloud upload

The endpoint is `POST https://apis.roblox.com/assets/v1/assets`, a multipart request with an `x-api-key` header. The API key needs the **assets** permission with read and write. For OAuth the scopes are `asset:read` and `asset:write`.

```bash
curl -s -X POST "https://apis.roblox.com/assets/v1/assets" \
  -H "x-api-key: $ROBLOX_API_KEY" \
  -F 'request={"assetType":"Model","displayName":"SM_Street_Lamp_A","description":"Street lamp, kit v3","creationContext":{"creator":{"groupId":"1234567"}}}' \
  -F 'fileContent=@build/SM_Street_Lamp_A.glb;type=model/gltf-binary'
# -> returns an Operation; poll until done:
curl -s -H "x-api-key: $ROBLOX_API_KEY" "https://apis.roblox.com/assets/v1/operations/$OPERATION_ID"
```

Facts and limits:

- **Content types:** `model/gltf-binary` (.glb), `model/gltf+json` (.gltf) and `model/fbx` (.fbx).
- **Size:** at most **20 MB** per file. Images must be under 8000×8000.
- Uploaded models become **packages**.
- **Updating content** (PATCH on an existing asset) is supported **only for .fbx**, and is a **beta** endpoint **[version-sensitive]**. Re-uploading a changed **GLB creates a new asset ID**. Keep a manifest (for example `assets/manifest.json`) mapping asset name to current asset ID, file hash and version. Update placements by editing the asset's **package** and publishing, so every copy updates through PackageLink AutoUpdate.
- Raw mesh uploads only accept content downloaded from Asset Delivery, so upload Models, not bare mesh files.
- **Upload under the same group that owns the game,** or the place may not be allowed to load the assets.
- **Audio** uploads through Open Cloud: up to 7 minutes; the Open Cloud page says 100 uploads a month when ID-verified and 10 when not. This conflicts with the audio page (see 5.9 and 5.14).
- Never commit the API key. Store it in an environment variable or secret store, and scope it to the one group and the assets API.

### Post-import fix-up (Studio side)

Run this through the Studio MCP or the command bar after inserting a model. It enforces house rule 2 and the 5.6 flag policy:

```lua
local function fixup(model: Model)
	for _, d in model:GetDescendants() do
		if d:IsA("MeshPart") then
			d.Anchored = true
			if d.Name:match("_COL$") then
				d.Transparency = 1
				d.CanCollide, d.CanQuery, d.CanTouch = true, true, false
				d.CastShadow = false
				d.CollisionFidelity = Enum.CollisionFidelity.Hull
			elseif model:FindFirstChild(d.Name .. "_COL", true) or model:GetAttribute("HasCOL") then
				d.CanCollide, d.CanTouch = false, false
				d.CollisionFidelity = Enum.CollisionFidelity.Box -- minimise stored collision data
			else
				d.CanCollide, d.CanTouch = true, false
				-- Box for small props, Hull for medium: decided per asset via attribute
				local fid = model:GetAttribute("Fidelity") or "Hull"
				d.CollisionFidelity = Enum.CollisionFidelity[fid]
			end
			if d.Size.Magnitude < 3 then d.CastShadow = false end -- tiny clutter
		end
	end
end
```

`CollisionFidelity` normally can't be changed by a running game script; this script is meant to run at edit time in Studio. Check the setting through the Studio MCP for your build, or set it in the Properties window.

### Modular kits and packages

- **Keep the kit small and versatile.** Beyond the Dark built a whole station from a few versatile pieces and placed more than 1,000 wall-panel package instances. Fewer unique meshes means more instancing and less memory.
- **Each piece is a package with AutoUpdate on.** One fix in Blender, re-export, swap inside the package and publish, and every placement updates. Updating a package keeps its ID instead of creating new ones.
- Use the built-in grid snap at the kit grid size. Rotate in 90° steps. Hide seams with trims (cornices, corner posts, skirting).
- Prefer reusing the same modules with variant SurfaceAppearances (paint colours, signage) over new meshes.

### Cohesive art style (avoiding the generic look)

A cohesive look comes from **constraints applied everywhere**, not from detail. Put these in a one-page style bible and check every asset against it:

1. **Palette:** 8–12 base colours plus 2 accent colours. Apply them via the `SurfaceAppearance.Color` tint, the `MeshPart.Color` overlay or vertex colour. Ban unlisted colours.
2. **Shape language:** decide whether shapes are soft-rounded and chunky (stylized), or crisp with small bevels. Exaggerate proportions slightly relative to the chunky Roblox avatar, with thicker frames and larger handles.
3. **Bevel standard:** one chamfer width per size class, for example 0.05 studs for props and 0.15 for architecture, always with weighted normals.
4. **Texel density and trim set:** one density (about 50 px/stud) and one shared trim library (above).
5. **Material response:** a roughness range per material family (painted metal 0.4–0.6, raw concrete 0.8–0.95 and so on). Metalness is 0 or 1.
6. **Wear and story:** consistent edge wear and grime direction (gravity-driven streaks), not random noise.
7. **Lighting-first review:** judge assets in-engine under the final Lighting and Atmosphere preset (5.8), at a low graphics quality level and on a phone. A model that looks good in Blender's Eevee can look flat under Roblox's Soft lighting style.

**Anti-patterns:** mixed texel densities; noisy procedural textures with no wear logic; saturated rainbow palettes; every object glowing; unbevelled boxes; one-off unique textures per prop; random marketplace-looking proportions; text baked into textures (use SurfaceGui or decals for localizable signage).

Sources: creator-docs:art/blender.md, creator-docs:art/modeling/specifications.md, creator-docs:art/modeling/texture-specifications.md, creator-docs:art/modeling/export-requirements.md, creator-docs:art/modeling/gltf-export.md, creator-docs:art/modeling/surface-appearance.md, creator-docs:studio/importer.md, creator-docs:parts/meshes.md, creator-docs:parts/models.md, creator-docs:physics/units.md, creator-docs:cloud/guides/usage-assets.md, creator-docs:tutorials/curriculums/environmental-art/assemble-an-asset-library.md, creator-docs:tutorials/curriculums/environmental-art/develop-polished-assets.md, creator-docs:tutorials/curriculums/environmental-art/optimize-your-experience.md, creator-docs:resources/beyond-the-dark/building-architecture.md, creator-docs:performance-optimization/improve.md

## 5.8 Lighting, atmosphere and environment presets

### Lighting style replaced "Technology" **[version-sensitive]**

`Lighting.Technology` has been **superseded** by two properties:

- **`Lighting.LightingStyle`**, which states the artistic intent:
  - **Realistic:** the most advanced lighting and shadows.
  - **Soft:** a flat, retro-Roblox look with softer lights and shadows. **Studio starts new places on Soft.**
- **`Lighting.PrioritizeLightingQuality`**, which sets what scales down first on weaker devices:
  - `true` keeps advanced shadows and high-quality shaders close up.
  - `false` keeps view distance.

In the old `Technology` enum, Voxel (a 4×4×4 voxel light grid), ShadowMap and Future remain. Legacy, Compatibility and Unified are deprecated and can't be selected. To recreate the old Compatibility look, use Voxel with a `ColorGradingEffect` set to `TonemapperPreset = Retro`. `LightingStyle` can be set only in the Properties window.

**Decision rule:**

- Use **Realistic** for anything with interiors, local lights, reflective materials or a night mode. That covers most high-quality Blender-art games.
- Use **Soft** for bright, flat, cartoon styles where crisp shadows fight the art.
- Set `PrioritizeLightingQuality = true` for small, dense worlds such as towns, interiors and obbies. Set it to `false` for large open maps where seeing far matters.

### Key Lighting properties

| Property | What it does | Starting point |
|---|---|---|
| `Ambient` | Hue for everything, indoors and out | Dark, slightly tinted, for example (26,34,36) as in the curriculum sample |
| `OutdoorAmbient` | Hue for outdoor areas only | Warm by day, cool blue at night |
| `Brightness` | Sun or moon intensity | 2–3 day, 0.5–1 night (house) |
| `ExposureCompensation` | Camera exposure | 0; adjust ±0.5 for mood |
| `ColorShift_Top` / `ColorShift_Bottom` | Tint of sun-facing and away-facing surfaces | Subtle warm top, cool bottom |
| `EnvironmentDiffuseScale` | Ambient light taken from the skybox | 0.5–1 for natural fill |
| `EnvironmentSpecularScale` | Sky reflections. Near 1, metals look real | 0.7–1 if PBR metals are used |
| `GlobalShadows` | Shadows on or off | On |
| `ShadowSoftness` | 0 is hard, 1 is soft. **Realistic only** | 0.15–0.3 |
| `ClockTime` / `TimeOfDay` | Sun position (same value, number versus string) | Scripted day/night cycle |
| `GeographicLatitude` | Sun path | Tune for long shadows |

Interior light leaking under Realistic: indoor spaces need enclosing geometry at least **1 stud thick**. The tutorial wraps mesh walls in parts at least **2.5 studs** thick. Under the house rules, give Blender walls real thickness (≥ 1 stud). Where an extra blocker is still needed, use invisible helper parts (Transparency 1, CanCollide off unless they are also hulls), and verify they are invisible.

### Atmosphere, sky and post-processing

- **Atmosphere** (child of Lighting):
  - `Density` sets how much the air obscures distant objects. Fog hides streaming pop-in and lets you lower `StreamingTargetRadius`. That is a performance-plus-mood win.
  - `Offset` sets the horizon silhouette versus blend-into-sky. A low offset can make the sky show through terrain, so balance it against Density.
  - `Haze`, `Color`, `Glare` and `Decay`: Glare needs Haze above 0, and Decay needs both Haze and Glare above 0.
- **Sky:** six images form a cube. `Sky.SkyboxOrientation` can rotate it, scripted with `% 360` to avoid precision drift. Rotated skies are not reflected in indoor reflections.
- **Clouds:** a dynamic cloud object for outdoor games. **GlobalWind** drives clouds, grass, particles affected by wind, and fluid forces. Changing `Workspace.GlobalWind` wakes physics assemblies (5.6), so don't animate it every frame in a physics-heavy game.
- **Post-processing:**
  - `BloomEffect`: make emissives glow; keep Intensity low.
  - `BlurEffect`: blur the world behind modal menus. Use it only while the menu is open.
  - `ColorCorrectionEffect`: overall grade.
  - `DepthOfFieldEffect`: shop item focus, photo modes.
  - `SunRaysEffect`.
  - `ColorGradingEffect` with `TonemapperPreset`: **Default** is the post-2019 vivid look; **Retro** is the pre-2019 look **[version-sensitive]**.

  Each effect costs full-screen GPU time. Keep at most 2–3 always on, and toggle DepthOfField and Blur contextually.

### Presets

**Curriculum sample, "Environment Art – Constructing" (exact values from the docs):** Lighting `Ambient` and `OutdoorAmbient` = (26,34,36), `LightingStyle` = Realistic, `ShadowSoftness` = 0.15, `GeographicLatitude` = −18. Atmosphere `Density` = 0.285, `Offset` = 0.65, `Decay` = (254,254,254), `Glare` = 0.3, `Haze` = 2.

**House starting presets.** Tune these in-engine with your palette; they are starting points, not doc values.

| Preset | LightingStyle | ClockTime | Brightness | Ambient / OutdoorAmbient | Atmosphere (Density / Offset / Haze / Glare) | Post |
|---|---|---|---|---|---|---|
| Bright stylized day (simulators, tycoons) | Soft or Realistic | 14 | 2.5 | (70,70,80) / (120,120,130) | 0.25 / 0.25 / 0.5 / 0 | Bloom low, ColorCorrection Saturation +0.1 |
| Golden hour town | Realistic | 17.6 | 2 | (40,35,45) / (110,90,80) | 0.3 / 0.3 / 1.5 / 0.4 | SunRays low, Bloom low |
| Night city (neon) | Realistic | 0 | 0.5 | (15,15,25) / (40,45,70) | 0.35 / 0.2 / 1 / 0 | Bloom for emissive signs; few shadowed lights |
| Overcast / moody | Realistic | 12 | 1.2 | (50,55,60) / (90,95,100) | 0.4 / 0.1 / 2.5 / 0 | ColorCorrection Contrast +0.1 |
| Interior shop | Realistic | any | 1.5 | (30,30,35) / (60,60,70) | 0.2 / 0.5 / 0 / 0 | No blur; SurfaceLights in Blender-modelled fixtures |

**Lighting performance rules:**

- Every shadow-casting local light costs `ShadowMapSystem` and `LightGridCPU` time. Bake mood into textures, emissive and vertex colour where you can.
- Lights go on `_Att` attachments inside the Blender light-fixture models, with `Shadows = false` by default.
- Test on graphics quality level 1–3, where shadows are off. Make sure the scene still reads without shadows.

Sources: creator-docs:environment/lighting.md, creator-docs:environment/atmosphere.md, creator-docs:environment/skybox.md, creator-docs:environment/clouds.md, creator-docs:environment/global-wind.md, creator-docs:environment/post-processing-effects.md, creator-docs:effects/light-sources.md, creator-docs:reference/engine/enums/Technology.yaml, creator-docs:reference/engine/enums/LightingStyle.yaml, creator-docs:tutorials/curriculums/environmental-art/construct-your-world.md, creator-docs:tutorials/use-case-tutorials/lighting/enhance-indoor-environments.md, creator-docs:physics/sleep-system.md

## 5.9 VFX, animation and audio: budgets and replication

### Particle emitters, beams and trails

**Doc limits and costs:**

- **Rate:** one ParticleEmitter can emit up to **400 particles per second**, but only **100 per second on mobile**. Keep Rate as low as the look allows. Make up for it with bigger, better-designed particles.
- **Lifetime** is capped at **20 s**.
- **Fill-rate:** the more screen pixels particles cover, the more GPU they cost. Large, close-up smoke is the worst case.
- **Overdraw:** overlapping transparent particles multiply cost. Few dense layers beat many faint ones.
- **Flipbooks** cost texture memory. Clients **automatically deactivate flipbooks on low memory**, which is likely on older phones. Use few unique flipbooks. `FlipbookFramerate` is capped at **30 fps**. OneShot mode spreads frames across the particle's lifetime.
- **LightEmission** 0 is normal blending and 1 is **additive** (glows, and hides the dark areas of grayscale textures).
- **Changing ParticleEmitter properties at runtime is costly.** Prefer `Emit(n)` bursts and `Enabled` toggles to per-frame property animation.
- **Weather:** a single emitter has limited rate, so rain over an area uses a grid of emitter parts. If distant particles flicker, you've hit the particle limits; reduce Rate, area or Lifetime. Roblox's weather-island sample schedules storms, cloud and wind changes, and roof detection.

**House VFX budget (mobile):**

- Constant ambient effects: at most about 6–10 emitters in view.
- Ambient emitters: Rate ≤ 20 each.
- Bursts: `Emit(5–30)`.
- One shared **VFX texture atlas** of 512² or 1024² holds smoke, spark, ring and glow sprites.
- Beams and Trails for ribbons, lasers, speed lines and delivery-route arrows: they are cheap compared with particles, but still transparent.

**House rules and VFX:** particles, beams and trails are 2D effects, not "visible objects" in the house-rule sense. **3D VFX meshes** (shockwave rings, coin models, debris chunks) are still made in Blender. VFX host parts are invisible helpers: Transparency 1, CanCollide, CanTouch and CanQuery off, CastShadow off. Better still, host VFX on `_Att` attachments in the Blender model.

**Highlights:** at most 255 at a time. The first costs up to about 1 ms of GPU time on mobile. Toggle `Enabled` instead of creating and destroying. Mobile cost scales with screen coverage. They suit "interactable" outlines; use one at a time on the targeted object.

### Replicating effects: do them on the client

The server should send **one small event**. Each client builds the effect locally from pooled templates. Never create VFX instances on the server, and never tween world objects on the server; both replicate every change to every client.

```lua
-- ReplicatedStorage/Net: RemoteEvent "PlayFX"
-- Server: fire a compact message (id + CFrame), optionally only to nearby players
PlayFX:FireAllClients("CoinBurst", rootPart.CFrame)

-- Client
local templates = ReplicatedStorage.FX -- Blender meshes + emitters authored once
PlayFX.OnClientEvent:Connect(function(id: string, cf: CFrame)
	if (cf.Position - camera.CFrame.Position).Magnitude > 200 then return end -- cull far FX
	local fx = acquireFromPool(templates[id]) -- pooled clone
	fx:PivotTo(cf)
	for _, e in fx:GetDescendants() do
		if e:IsA("ParticleEmitter") then e:Emit(e:GetAttribute("Burst") or 10) end
	end
	task.delay(2, releaseToPool, fx)
end)
```

Also skip or reduce effects when `GuiService.ReducedMotionEnabled` is true or the graphics quality level is low.

### Animation

- **Priorities,** from highest to lowest: **Action4, Action3, Action2, Action, Movement, Idle, Core**. Set them in the Animation Editor or on the track. Movement overrides Idle, and Action overrides Movement.
- **Replication rules (Animator):**
  - If an Animator is under a Humanoid or AnimationController **in a player's character**, animations the client starts replicate to the server and other clients.
  - If the Animator is **not in a player character** (an NPC), its animations must be loaded and played **on the server** to replicate.
  - The Animator must be **created on the server**. One created locally won't replicate any tracks.
  - `LoadAnimation()` requires the Animator to be in Workspace.
- **Performance guidance conflicts with naive replication.** The performance docs recommend playing **NPC animations on the client** for cost. Resolve it like this: for ambient NPCs (workers, crowds, shopkeepers), let each client load and play animations locally on its own copy. Visual sync doesn't matter there. Use server-played animations only where every player must see the same timing (boss attacks).
- `LoadAnimation()` **always creates a new AnimationTrack**. Load once and cache, or use `Animator:GetTrackByAnimationId()`.
- Animate procedural motion through `Motor6D.Transform` in **PreSimulation**. Remove unused animation metadata (KeyframeSequences kept in rigs) before shipping; the network docs call this out. Animation Editor saves go to ServerStorage, which does not replicate.
- **Blender to Roblox animation:** FBX is the documented animation route. Use one animation track per FBX, Bake Animation as required for the clip, Add Leaf Bones off, and a rig matching R15 bone names if it targets avatars. Bones need scale 1 and rotation 0, the root at the origin, at most 4 influences per vertex, and no root influence.
- **Moving NPC models with skinned meshes:** include a Humanoid (or the correct controller), or each movement rebuilds FastClusters (5.4). Keep `updateInvalidatedFastClusters` under about 4 ms.
- Graph Editor state machines evaluate transitions by **Priority**; equal priorities pick at random **[version-sensitive: newer animation graph tooling]**.

### Audio

There are two audio systems **[version-sensitive]**:

- **Legacy `Sound` objects** with SoundGroups and SoundEffects (Equalizer, Chorus, Reverb and so on).
- The newer **audio API:** `AudioPlayer` (plays an asset), `AudioEmitter` (a virtual speaker in 3D), `AudioListener` (a virtual microphone), `AudioDeviceOutput` (the player's speakers), `AudioDeviceInput` (a microphone), `AudioTextToSpeech`, `AudioSpeechToText`, and **Wires** connecting them. Effects such as `AudioEqualizer`, `AudioCompressor`, `AudioReverb`, `AudioChorus` and `AudioFader` are wired in-line.

Clicking a Creator Store audio inserts a legacy `Sound`, which lacks the new API's routing. New projects should prefer the audio API for 3D and mixing work.

**Import limits (audio page):** mp3, ogg, wav or flac; a single track; under **20 MB** and **7 minutes**; sample rate ≤ **48 kHz**; mono, stereo, 3.0 or 5.1. Upload quota: **2,000 per 30 days if ID-verified, 100 per 30 days if not**. The Open Cloud asset page gives **100 a month verified and 10 unverified**. Treat the stricter Open Cloud numbers as the limit for automated pipeline uploads until confirmed (5.14).

**Mix design (Beyond the Dark pattern):**

- One **2D soundbed** (omnipresent ambience), plus **3D spot ambiences** parented to objects (fish tank, fans, neon buzz) that pull the ear around the space.
- The station's whole mix was 1 soundbed, 2 dialogue tracks, 3 music tracks, 10 scripted events and **50 3D sounds**, run through a nested SoundGroup bus with sidechain compression. Use that as a realistic scale reference.
- **Layered loops** of different lengths add variety for free. A 6 s and a 5 s loop stay unique for their least common multiple, 30 s.
- Use EQ and Chorus to reshape reused sources: a river recording EQ'd to sound underwater was reused in another room.

**Performance and correctness:**

- Many simultaneous playing sounds cost `Sound/stepInstances` time. Cap concurrent one-shots (for example at most 16 SFX voices) and pool them.
- Sounds parented to streamed-out parts **stop** (5.5). Put critical ambience on always-present containers, or play it as 2D on the client.
- Play UI and feedback sounds **on the client**. Never fire a remote just to play a click.
- Use `RollOffMinDistance`, `RollOffMaxDistance` and `RollOffMode` (Inverse, Linear, InverseTapered, LinearSquare). Very low max distances make sounds cut off abruptly.
- Respect player volume settings. Expose separate Music, SFX and Ambience sliders through SoundGroups or AudioFaders (5.11).
- Preload only the first music track and core UI sounds (5.12).

Sources: creator-docs:effects/particle-emitters.md, creator-docs:effects/beams.md, creator-docs:effects/trails.md, creator-docs:effects/highlighting.md, creator-docs:performance-optimization/improve.md, creator-docs:reference/engine/classes/Animator.yaml, creator-docs:animation/editor.md, creator-docs:animation/graph-editor-state-machine.md, creator-docs:art/modeling/specifications.md, creator-docs:art/modeling/export-requirements.md, creator-docs:audio/index.md, creator-docs:audio/assets.md, creator-docs:audio/effects.md, creator-docs:sound/objects.md, creator-docs:sound/dynamic-effects.md, creator-docs:cloud/guides/usage-assets.md, creator-docs:resources/beyond-the-dark/sound-design.md


## 5.10 UI implementation

### Containers, lifecycle and safe areas

- **Where UI lives:** a `ScreenGui` in `StarterGui` is cloned into each player's `PlayerGui` when their character first spawns. If `Players.CharacterAutoLoads` is off, the clone waits until `LoadCharacterAsync`. All on-screen UI and its code run on the **client**.
- **`ResetOnSpawn`:** this re-clones the ScreenGui on every respawn. Set it to **false** for HUDs, shops and menus that should keep their state. Never keep references to a destroyed clone.
- **Separate screens:** use one ScreenGui per screen (HUD, Shop, Settings, Offer popup). Toggle `ScreenGui.Enabled`, because a disabled ScreenGui doesn't render, take input or update. Layer screens with `DisplayOrder`, giving modals a higher value than the HUD.
- **`ScreenGui.ScreenInsets`** sets the safe area:
  - `CoreUISafeInsets` (default) keeps content clear of the top-bar buttons and device cutouts. **Use it for anything interactive.**
  - `DeviceSafeInsets` avoids notches but not the Roblox top bar.
  - `TopbarSafeInsets` places content in the strip beside the top-bar controls and flexes with it.
  - `None` is only for non-interactive full-bleed backgrounds.
  - Loading screens set `IgnoreGuiInset = true` to cover the whole screen.

### Scale, offset and constraints

`UDim2` has a **scale** part (a fraction of the parent) and an **offset** part (pixels). `AnchorPoint` sets which point of the element `Position` refers to. Decision rules:

| Need | Use |
|---|---|
| Element placed relative to screen edges | Scale position and matching AnchorPoint, for example `AnchorPoint (1,0)` with `Position UDim2.new(1,-16,0,16)` for top-right with a 16 px margin |
| Element that keeps its shape on every screen | Scale size plus a `UIAspectRatioConstraint`. Default ratio 1 suits square icons and avatar thumbnails |
| Element with sensible min and max on extreme screens | `UISizeConstraint` (MinSize and MaxSize in pixels) |
| Text that must stay readable | `TextSize` with `UITextSizeConstraint`, or TextScaled with a constraint. TextScaled ignores the player's PreferredTextSize (5.11) |
| Panel that grows with content | `AutomaticSize` X, Y or XY. `Size` becomes the **minimum** size. Combine with TextWrapped for labels |
| Scrolling list | `ScrollingFrame` with `AutomaticCanvasSize` and `CanvasSize = 0`, not a fixed canvas |
| Uniform global scale (console TV, accessibility) | `UIScale` on a root frame, as a final multiplier, not as the layout system |

**Gotcha:** if an element is controlled by both a layout (such as `UIListLayout`) and a `UIAspectRatioConstraint`, **the constraint wins** and overrides the layout's sizing.

### Layouts

- **`UIListLayout`** handles one-dimensional flow (fill direction, alignment, wrapping, padding). It has **flex** behaviour (equal fill and distribution, item line alignment). Use `UIFlexItem` for per-child grow and shrink, like CSS flexbox.
- **`UIGridLayout`** is for uniform cells such as inventories and shop grids. Compute `CellSize` from `AbsoluteSize` when the column count must change by width.
- **`UITableLayout`** is only for truly tabular data. **`UIPageLayout`** suits carousels and tutorial pages. **`UIPadding`** sets inner margins.
- Use explicit **breakpoints** (narrow versus wide) rather than shrinking a desktop panel until it fits. For example, a category list switches from vertical to horizontal under about 700 px width, and the details panel becomes a separate screen.

### Appearance modifiers and styling

- **`UICorner`** rounds corners. **`UIStroke`** adds a border or text outline, with thickness, colour or gradient, border position or offset, and corner style. **`UIGradient`** handles colour and transparency sequences, type, offset, rotation and tile mode. **9-slice** (`SliceCenter`, edited in the Studio 9-slice editor) stretches panel art without distorting corners.
- **`UIShadow`** **[version-sensitive: new; some features in beta]** gives shape or text shadows with blur, spread, offset, inset and gradient. It follows the parent's `UICorner` and rotation, but doesn't support `Path2D` or textures.
- **Sprite sheets:** pack icons into one image and use `ImageRectOffset` and `ImageRectSize`. That means one texture instead of dozens, which saves memory and load time.
- **UI styling system** **[version-sensitive: new engine feature]**:
  - A `StyleSheet` holds `StyleRule`s with CSS-like `Selector`s: class (`"Frame"`), tag (`".ButtonPrimary"`), name, modifiers (pseudo-instances such as UICorner and UIStroke), `GuiState` selectors (such as Hover), and `@` query selectors driven by `StyleQuery` (screen size, input type, accessibility).
  - **Tokens** are attributes on a token StyleSheet (`$Magenta`, `$SquareM`). **Themes** are StyleSheets that derive tokens via `StyleDerive`.
  - A `StyleLink` binds one StyleSheet to a ScreenGui tree; only one StyleSheet applies per tree.
  - The Style Editor and Properties window mark styled properties.
  - Recommendation: for a new game, define a small token sheet (colours, corner radii, stroke widths, spacing, fonts) and drive buttons via tag selectors. That gives you a consistent visual language and one place to re-skin.

```lua
-- Minimal token + rule setup (abridged from the styling docs)
local tokens = Instance.new("StyleSheet")
tokens:SetAttribute("Accent", Color3.fromHex("FFCC00"))
tokens:SetAttribute("Radius", UDim.new(0, 12))
local link = Instance.new("StyleLink"); link.StyleSheet = tokens; link.Parent = hudScreenGui
local rule = Instance.new("StyleRule"); rule.Selector = ".ButtonPrimary"; rule.Parent = tokens
rule:SetProperties({ BackgroundColor3 = "$Accent", BorderSizePixel = 0 })
```

### Motion and tweening

- Tween UI on the client with `TweenService`. Animate **state changes** such as open and close, focus and confirmation. Avoid perpetual decorative motion.
- Keep tweens short and interruptible: 0.1–0.3 s for UI feedback, at most about 0.75 s for panel transitions.
- Honour **`GuiService.ReducedMotionEnabled`**. Set the tween time to 0, or swap a slide for a fade:

```lua
local GuiService = game:GetService("GuiService")
local TweenService = game:GetService("TweenService")
local t = if GuiService.ReducedMotionEnabled then 0 else 0.2
TweenService:Create(panel, TweenInfo.new(t, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
	{ Position = UDim2.fromScale(0.5, 0.5) }):Play()
```

### Framework choice: plain Instances, Fusion or React-Luau

| Option | What it is | Strengths | Costs |
|---|---|---|---|
| **Plain Instances + small modules** | Author the UI shell as named Instances in StarterGui and wire behaviour with small controller modules | Editable in Studio, visible in Explorer, works with the Style Editor and MCP tools, zero dependency | Manual state syncing; discipline needed to avoid one giant LocalScript |
| **Fusion** (dphfox, 0.4.x in the repo) | Reactive state library: `scope:Value`, `scope:Computed`, `scope:Observer`, `scope:Spring`, `scope:Tween`, `scope:New "Frame" {...}`, `[Children]`, `OnEvent`, `Hydrate` for existing instances | Fine-grained reactivity, so only changed properties update. Built-in springs and tweens. **Scopes** destroy everything together. Can hydrate Studio-authored UI | API changed a lot between versions (0.2 → 0.3 → 0.4 introduced scopes), so check the version **[version-sensitive]**. Needs a Rojo or Wally toolchain |
| **React-Luau** (Roblox's port of React) | Declarative components, hooks, virtual tree reconciliation | Familiar to web developers, large patterns ecosystem, used heavily by Roblox's own UI | More boilerplate, reconciliation overhead, UI exists only in code (less Studio-editable) |

Fusion performance notes from its docs: Fusion **skips updates** when a computed returns a value that isn't meaningfully different. It cannot do that for tables, so **freeze tables** you won't mutate (`table.freeze`) to unlock the optimization. Always put objects in a **scope** and call `scope:doCleanup()` when a screen closes.

**Recommendation:**

- **Lower-risk:** author screens as Studio Instances with the new styling tokens. Drive them with small controller modules, and use **Fusion's `Hydrate`-style or plain property binding only for dynamic regions** (inventory grids, currency counters). This keeps AI-assisted and Studio-MCP editing easy.
- **Bolder:** build the whole UI in Fusion 0.4 with scopes and springs. You get the most polished motion and consistent state at scale, but you depend on a fast-moving library and lose some Studio editability.
- **Pick the lower-risk option** unless the team already knows Fusion.
- Use React-Luau only if the team comes from React.

### UI performance rules

- Hidden screens: set `ScreenGui.Enabled = false`, not just `Visible = false` on children.
- Avoid rebuilding UI every frame. Update text only when the value changes, and throttle counters to at most about 10 Hz.
- `fillGuiVertices` cost: avoid UIGradient and UICorner on text or frames that change constantly. Consider a **CanvasGroup** for complex static panels. It flattens rendering but **costs memory**, so don't nest them or use many.
- World-space UI: every `BillboardGui` adds `Pass3dAdorn` cost. Pool them, use `MaxDistance`, and show them only near the player. Many complex `SurfaceGui`s are expensive, especially in VR.
- Use sprite sheets and ≤ 256² icons. Load menu art lazily rather than at join.
- Diegetic UI (Beyond the Dark's map) is built from `SurfaceGui`s. For interactive SurfaceGuis, keep them in `StarterGui` with `Adornee` set to the world part so button events work. `LightInfluence < 1` enables `Brightness` for a glow. Under the house rules, the board or screen **mesh** is a Blender model, and the SurfaceGui sits on it.

### Text filtering (mandatory for user-generated text)

Any text one player writes that others can see must be filtered **on the server**. That includes pet names, plot or shop names, signs and custom messages. Text from external web sources must be filtered too.

```lua
local TextService = game:GetService("TextService")
SetSignText.OnServerEvent:Connect(function(player, raw: string)
	if typeof(raw) ~= "string" or #raw > 60 then return end
	local ok, result = pcall(TextService.FilterStringAsync, TextService, raw, player.UserId)
	if not ok then return end
	local ok2, filtered = pcall(result.GetNonChatStringForBroadcastAsync, result)
	if ok2 then sign:SetAttribute("Text", filtered) end -- clients render the attribute
end)
```

Use `GetNonChatStringForBroadcastAsync` for text everyone sees, and `GetNonChatStringForUserAsync(userId)` for text shown to one specific user. Always wrap both calls in `pcall`. If filtering fails, show nothing rather than the raw text.

### Proximity prompts

- **Key properties:**
  - `ActionText` and `ObjectText` label the prompt.
  - `KeyboardKeyCode` and `GamepadKeyCode` set the keys.
  - `HoldDuration` sets the hold time; 0 triggers instantly.
  - `MaxActivationDistance` sets the visibility range.
  - `RequiresLineOfSight` (default **true**) needs a clear camera-to-prompt path.
  - `Exclusivity` controls how prompts compete when several are in range.
  - `ClickablePrompt` lets touch and mouse users tap or click the prompt.
  - `Style = Custom` lets you draw your own UI.
- **Events** (on `ProximityPromptService` or the prompt): `PromptTriggered`, `PromptButtonHoldBegan`, `PromptButtonHoldEnded`, `PromptShown` and `PromptHidden`. With custom styles, use `PromptShown` to build your UI.
- **Placement:** parent prompts to a Blender-authored **`Prompt_Att` attachment** inside the interactive model. Attachments and invisible anchor parts are allowed helpers. With streaming, the prompt disappears when its model streams out, so make interactive models **Atomic**.
- Prompts are the mobile-friendly **context-based UI** the docs recommend. Show an "Open" or "Deliver" action only near the object, not as a permanent button.
- **Validate on the server.** `Triggered` tells you who pressed it. Re-check distance, state and cooldown before granting anything.

### Monetization UI under house rule 3

Offer surfaces are small, dismissible cards that never block play:

- They sit in a safe-area corner, **outside** the mobile thumb and reserved zones.
- They appear after a positive moment (a delivery completed, a level-up), **never** in the first minutes or on the loading screen.
- They are rate-limited per session.
- The shop is always one tap away from a HUD button.

Timed boosts (2× Cash, 2× speed) show their remaining time honestly. No fake discounts, no restarting countdowns, no false scarcity.

Sources: creator-docs:ui/on-screen-containers.md, creator-docs:includes/ui/screen-insets.md, creator-docs:ui/position-and-size.md, creator-docs:ui/size-modifiers.md, creator-docs:ui/list-flex-layouts.md, creator-docs:ui/grid-table-layouts.md, creator-docs:ui/appearance-modifiers.md, creator-docs:ui/9-slice.md, creator-docs:ui/styling/index.md, creator-docs:ui/animation.md, creator-docs:ui/text-filtering.md, creator-docs:ui/proximity-prompts.md, creator-docs:performance-optimization/microprofiler/tag-table.md, creator-docs:resources/beyond-the-dark/user-interface.md, creator-docs:tutorials/curriculums/user-interface-design/index.md, dphfox__Fusion:docs/tutorials/best-practices/optimisation.md, dphfox__Fusion:docs/tutorials/fundamentals/scopes.md, gamedev-skills__awesome-gamedev-agent-skills:skills/other-engines/roblox-ui/SKILL.md

## 5.11 Cross-platform input, console, VR and accessibility

### Detect the preferred input, not the device

Use **`UserInputService.PreferredInput`** **[version-sensitive: newer property]**. It reflects built-in inputs plus the player's most recent gamepad or keyboard-and-mouse interaction. Its values include Touch, KeyboardAndMouse, Gamepad and MicroGamepad. Why the old checks fail:

- `TouchEnabled` is **true on touch-screen laptops**, so it is not an "is mobile" check.
- `GetLastInputType()` **thrashes**, for example between MouseMovement and Keyboard, or between Touch and Gamepad. That makes UI flicker between layouts. It can also return confusing values such as TextInput or Focus.

```lua
local UserInputService = game:GetService("UserInputService")
local function apply()
	local p = UserInputService.PreferredInput
	hud.TouchButtons.Visible = (p == Enum.PreferredInput.Touch)
	hud.KeyHints.Visible = (p == Enum.PreferredInput.KeyboardAndMouse)
	hud.GamepadHints.Visible = (p == Enum.PreferredInput.Gamepad)
end
UserInputService:GetPropertyChangedSignal("PreferredInput"):Connect(apply)
apply()
```

### Input Action System (the input abstraction) **[version-sensitive: new system]**

- **`InputContext`:** a group of actions, for example `PlayContext` for character controls and `NavContext` for menus. Enable or disable a context to switch control schemes. `Priority` decides order, and `Sink = true` consumes input so lower contexts don't receive it. That suits modal menus.
- **`InputAction`:** a gameplay verb ("Sprint", "Deliver", "Interact"). Its `Type` is one of:
  - **Bool:** press and release, for jump, shoot and sprint.
  - **Direction1D:** throttle, zoom.
  - **Direction2D:** movement, camera.
  - **Direction3D**.
  - **ViewportPosition**.

  Events are `Pressed` and `Released` (Bool only) and `StateChanged` (all types). `PreferredBinding` returns the binding for the current device, which is useful for showing the right key icon.
- **`InputBinding`:** one per input method on each action:
  - Keyboard uses `KeyCode` (LeftShift); gamepad uses ButtonY.
  - Touch links the binding's **`UIButton`** to an on-screen button.
  - Composite `Up`/`Down`/`Left`/`Right` keys give WASD-style 2D input.
  - `MouseDelta` and `TouchDelta` report pixels, so scale them, for example with `Scale = 0.01`.
- Set `Workspace.PlayerScriptsUseInputActionSystem` to make the default player scripts use the system. `ContextActionService` still works for legacy code. Bind actions only while the screen or tool that owns them is active.
- **Rule:** every action needs a keyboard, a gamepad **and** a touch binding. The VR guidance also says to avoid platform-dependent code and use `InputAction`.

### Mobile-first layout

- **Reserved zones:** the default thumbstick sits bottom-left and the jump button bottom-right. Keep vital information and custom buttons out of both.
- **Thumb zones:** place frequent actions near the jump button. Position them **relative to the jump button**, not at a fixed screen percentage. A button 40 % from the top edge is reachable on a phone but not on a tablet. The docs show placing a custom button 20 px left of `JumpButton`, after waiting for it to load:

```lua
local jump = playerGui:FindFirstChild("JumpButton", true) -- wait until it exists and IsLoaded
local b = Instance.new("ImageButton")
b.AnchorPoint = Vector2.new(1, 1)
b.Size = UDim2.fromOffset(jump.Size.X.Offset * 0.8, jump.Size.Y.Offset * 0.8)
b.Position = jump.Position + UDim2.fromOffset(-20, jump.Size.Y.Offset)
b.Parent = jump.Parent
```

- **Context-based UI:** show only what matters right now, and use proximity prompts for object actions.
- **House touch-target rule:** custom buttons at least as large as 0.8× the jump button, with ≥ 8 px gaps. HUD text at least about 18 px at 1× on a phone. Test portrait and landscape if you allow both.

### Gamepad and console (the "10-foot experience")

- Players sit **8–10 feet** from a TV. Develop for **lower resolutions first**. Use relative positions plus `UISizeConstraint`, check `GuiService.ViewportDisplaySize` (Large means most TVs), and use ScrollingFrames to reduce clutter as UI scales up.
- Keep important UI inside **TV-safe areas**, because some TVs don't display to the screen edge.
- **Navigation:** every element must be reachable with the four directions plus select and back. Roblox provides **directional selection** and a **virtual cursor** out of the box. Custom layouts need bespoke navigation: set an initial `GuiService.SelectedObject` when a menu opens, define `NextSelection*` neighbours, and trap focus inside modals. Keep action sequences short; each controller step is a button press.
- **Disable the chat window on console games.**
- **Button icons:** `UserInputService:GetImageForKeyCode()` returns default Roblox icons, and `GetStringForKeyCode()` maps key codes to the console keyboard layout.
- **Haptics:** use `HapticEffect` instances with types such as `GameplayCollision` and `UIClick`, played with `:Play()`. Use them for dramatic events, attention events and UI notifications such as hitting the end of a list. **Don't overuse vibration.**
- **Audio feedback:** add sounds for navigation and selection on console. Console interactions are otherwise silent.

### VR

- **Target 72 FPS** on standalone headsets (Quest 2). Quest's **Auto Quality Mode** may lower draw distance and lighting to hold frame rate. Frame drops cause discomfort.
- **Comfort settings** are provided by Roblox: vignette during motion, stepped rotation, and a 3rd-person fixed camera. Don't fight them with custom camera scripts.
- **Performance list from the docs:**
  - Enable streaming.
  - Limit raycasts.
  - Prefer `RunService.Heartbeat` over `task.wait` for precise timing.
  - Mobile VR is draw-call sensitive, so place detail only where it matters.
  - Use minimal geometry.
  - Minimize semi-transparent objects (Decals, Glass).
  - Limit complex SurfaceGuis.
  - Use InputAction rather than key-specific code.
  - Test on a real headset.

### Accessibility and player preferences

- **`GuiService.PreferredTransparency`** goes from 1 (default) to 0 (fully opaque). Multiply your background transparency by it, and listen for changes:

```lua
local GuiService = game:GetService("GuiService")
local function applyTransparency()
	for obj, base in panelDefaults do -- {[GuiObject]: number}
		obj.BackgroundTransparency = base * GuiService.PreferredTransparency
	end
end
GuiService:GetPropertyChangedSignal("PreferredTransparency"):Connect(applyTransparency)
applyTransparency()
```

- **`GuiService.PreferredTextSize`** (default Medium; Large and larger are opt-in) is applied by the engine's font pipeline, with some limits:
  - `TextScaled` text is **not** scaled.
  - `UITextSizeConstraint` limits still apply.
  - `AutomaticSize` elements grow to fit.
  - `TextWrapped` text wraps.
  - `TextService:GetTextSize()` and `GetTextBoundsAsync()` respect it.

  **Consequence:** prefer fixed `TextSize` with AutomaticSize and wrapping over TextScaled for body text. TextScaled locks out this accessibility setting.
- **`GuiService.ReducedMotionEnabled`:** reduce or remove UI motion (see 5.10). Also tone down camera shake and screen flashes.
- **Colour contrast and colour non-reliance:** pair colour with icons or text, for example rarity plus a label, or a red state plus an "X". **Sound non-reliance:** show visual cues for audio events. **Volume controls:** separate sliders for music, SFX and ambience.
- **Adaptive design principles:** input fluidity (every action on gamepad, keyboard and touch, with hints matching the active input), responsive layout (collapse secondary buttons into a menu on small screens), dynamic sizing (content-driven sizing that respects text-size preferences), and legibility (readable fonts on the smallest phone and on a distant TV, avoiding thin or decorative fonts). The Interactivity Showcase place demonstrates them.

Sources: creator-docs:input/index.md, creator-docs:input/input-action-system.md, creator-docs:input/mobile.md, creator-docs:input/gamepad.md, creator-docs:ui/position-and-size.md, creator-docs:production/publishing/console-guidelines.md, creator-docs:production/publishing/vr-guidelines.md, creator-docs:production/publishing/accessibility.md, creator-docs:production/publishing/adaptive-design.md, gamedev-skills__awesome-gamedev-agent-skills:skills/other-engines/roblox-ui/SKILL.md

## 5.12 Loading: join flow, loading screens and preloading

### What happens at join

1. **ReplicatedFirst** replicates first. Its LocalScripts run immediately, which is where the loading screen lives.
2. The rest of the data model replicates. With streaming, that is only the area around the spawn point. ReplicatedStorage and everything outside Workspace replicate in full.
3. The avatar loads.

`game.Loaded` and `game:IsLoaded()` report completion of the initial replication. Measure it on real devices with the snippet below (from the docs), placed in a ReplicatedFirst LocalScript:

```lua
local startTime = os.clock()
game.Loaded:Connect(function()
	print(("Loaded in %.2f s, %d instances"):format(os.clock() - startTime, #workspace:GetDescendants()))
end)
```

Use the Studio setting **Print Join Size Breakdown** to find the biggest join-time instances. Free models with obfuscated scripts are a known source of hidden join bloat; the Blender-only rule removes that risk.

### Reducing join time

- Keep **ReplicatedFirst and ReplicatedStorage lean**. Server-only assets go in ServerStorage. Client-needed but rarely used assets can be cloned in on demand.
- Keep streaming on and use **Persistent** models rarely (5.5). Consider `PredictiveStreamingMode` to prefetch the spawn area **[version-sensitive]**.
- **Defer** non-essential startup work, such as building the full shop catalogue, analytics warm-up or decorative NPC spawns, until after the player is in control.
- Fewer unique meshes and textures (5.7) also means faster joins.

### Custom loading screen

Facts from the docs:

- Create or reference a ScreenGui from a **ReplicatedFirst** LocalScript. Parent it to `PlayerGui` with `IgnoreGuiInset = true`.
- Call **`ReplicatedFirst:RemoveDefaultLoadingScreen()`**.
- Wait for `game.Loaded`, then destroy the screen.
- Animate with TweenService.
- Teleport loading screens are configured separately, through TeleportService.

The docs' sample also forces a `task.wait(5)` minimum display time. **Don't copy that.** It contradicts the performance guidance to defer work and offer a **Skip** button. Use at most a short fade.

Rules from the performance guide:

- **Preload only** the loading screen's own images, key menu images and the spawn area. Don't preload the whole Workspace or every asset.
- Don't rely on `ContentProvider.RequestQueueSize` as a progress bar.
- Offer a **Skip Loading** button.
- **Never wait on a spatial instance** in the loading screen. It may never stream in.

```lua
-- ReplicatedFirst/LoadingScreen (LocalScript); LoadingGui is a ScreenGui child of this script
local ReplicatedFirst = game:GetService("ReplicatedFirst")
local ContentProvider = game:GetService("ContentProvider")
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local gui = script:WaitForChild("LoadingGui")
gui.IgnoreGuiInset = true
gui.Parent = Players.LocalPlayer:WaitForChild("PlayerGui")
ReplicatedFirst:RemoveDefaultLoadingScreen()

task.spawn(ContentProvider.PreloadAsync, ContentProvider, { gui }) -- only this screen's own art

local skipped = false
gui.Root.Skip.Activated:Connect(function() skipped = true end)
task.delay(4, function() gui.Root.Skip.Visible = true end) -- appear after a few seconds

while not (game:IsLoaded() or skipped) do task.wait(0.1) end
TweenService:Create(gui.Root, TweenInfo.new(0.3), { GroupTransparency = 1 }):Play() -- Root is a CanvasGroup
task.wait(0.3)
gui:Destroy()
```

**House rule 3 and loading:** no offers, starter-pack popups or purchase prompts on the loading screen or in the first minutes. Branding and a gameplay tip are fine.

### Test on hardware

- Test on at least one 2–4 GB Android phone (the largest player segment), one mid-range phone, a tablet, a desktop, and a gamepad (on a console or a desktop with a controller).
- Measure join time, frame time and memory (MicroProfiler over Wi-Fi, port 1338).
- Run a **10–15 minute thermal play session**.
- Check touch-target reach, text readability, input switching (plug in a controller mid-session) and audio on both speakers and headphones.

Sources: creator-docs:players/loading-screens.md, creator-docs:performance-optimization/identify.md, creator-docs:performance-optimization/improve.md, creator-docs:performance-optimization/test-on-hardware.md, creator-docs:workspace/streaming/techniques.md

## 5.13 Pre-launch checklist

Work through this list before every public release. Items marked **(HR)** enforce a house rule.

### Performance

- [ ] Low-end Android (2–4 GB) holds ≥ 30 FPS (≤ 33.3 ms) in the busiest scene. Mid-range holds about 60 FPS. No spikes over about 50 ms in a 2-minute MicroProfiler capture.
- [ ] Server heartbeat stays at about 60 Hz with a full server. Server memory is < 50 % of (6.25 GiB + 100 MiB × max players). Memory is flat over a 1-hour soak test.
- [ ] Draw calls < 1,000 and triangles < 1 M in the worst view (Shift+F2). Scene Analysis shows no surprise categories (shadows, transparency, UI).
- [ ] No per-frame script work above budget. Custom `debug.profilebegin` labels exist on all hot loops.
- [ ] `--!native` is only on measured hot server or Android code, not on everything.
- [ ] All connections are cleaned up. Player and character instances are destroyed on leave. Per-player tables are cleared.
- [ ] Remotes are throttled and send deltas. There are no server-side tweens and no server-created VFX.

### Streaming

- [ ] Streaming is on with the 5.5 settings. The game works at `StreamingTargetRadius = 64`.
- [ ] Interactive models are Atomic. Persistent models are justified one by one.
- [ ] No LocalScript indexes Workspace content without WaitForChild with a timeout, FindFirstChild or CollectionService.
- [ ] `RequestStreamAroundAsync` runs before every teleport.

### Physics and collision (HR)

- [ ] All static geometry is anchored. Mechanisms anchor only the root.
- [ ] **Every visible object blocks players and NPCs.** Walk-test each asset type, and run the scan below.
- [ ] No `PreciseConvexDecomposition` except approved doorways. Check with the Explorer filter `CollisionFidelity=PreciseConvexDecomposition`.
- [ ] Non-colliding meshes use Box fidelity. CanTouch is off by default. CanQuery is deliberate.
- [ ] Collision groups are registered in one script. No visible object is excluded from player collision.
- [ ] Gameplay hits use server-validated spatial queries, not raw `Touched`.
- [ ] Vehicles and other driven assemblies have deliberate network ownership.

```lua
-- Edit-mode scan for house rules 1–2 (run via Studio MCP / command bar, not in live servers)
local issues = {}
for _, d in workspace:GetDescendants() do
	if d:IsA("BasePart") and d ~= workspace.Terrain then
		local visible = d.Transparency < 1
		if visible and not d:IsA("MeshPart") then
			table.insert(issues, "VISIBLE PRIMITIVE: " .. d:GetFullName())
		end
		if not visible and d.CastShadow then
			table.insert(issues, "INVISIBLE HELPER CASTS SHADOW: " .. d:GetFullName())
		end
		if visible and d:IsA("MeshPart") and not d.CanCollide and not d:HasTag("NonSolid") then
			local model = d:FindFirstAncestorOfClass("Model")
			if not (model and model:FindFirstChild(d.Name .. "_COL", true)) then
				table.insert(issues, "VISIBLE MESH WITHOUT COLLISION: " .. d:GetFullName())
			end
		end
	end
end
print(#issues == 0 and "House-rule scan OK" or table.concat(issues, "\n"))
```

Tag foliage leaves, VFX ribbons and similar non-solid visuals `NonSolid` deliberately. Roblox **Terrain** is not a Blender model. Under a strict reading of house rule 1, ground and water should be Blender meshes, or the exception should be approved explicitly.

### Art pipeline (HR)

- [ ] Every mesh came from the Blender pipeline. The manifest maps every asset name to an asset ID. No marketplace or free models, so no hidden scripts.
- [ ] Each kit piece or prop is uploaded once and placed as a package with AutoUpdate. The duplicate-MeshId audit (5.4) is clean.
- [ ] Triangle budgets (5.7) are met. Nothing is over 20k per mesh. One material and one UV set per mesh.
- [ ] Textures are ≤ 1024², mostly ≤ 512², from the shared trim and tileable library. `_SA` SurfaceAppearances are shared.
- [ ] RenderFidelity is Automatic (Performance for clutter and foliage). SLIM is on for large static models where available.
- [ ] Style bible check: palette, bevels, texel density and roughness ranges are consistent, judged under final lighting at a low quality level.

### Lighting, VFX and audio

- [ ] LightingStyle and PrioritizeLightingQuality are chosen deliberately. No interior light leaks.
- [ ] Shadow-casting local lights are minimal. CastShadow is off on small, moving and invisible parts.
- [ ] The scene reads well at graphics quality levels 1–3, where shadows are off.
- [ ] Particle rates fit mobile caps. Flipbooks are few. VFX are client-side and pooled.
- [ ] Animations are loaded once. NPC animation strategy is chosen (client-local for ambient NPCs).
- [ ] Concurrent sounds are capped. Ambience doesn't rely on streamed-out parts. Volume sliders exist.

### UI and input

- [ ] Tested in the Device Emulator **and** on real devices: small phone portrait and landscape, tablet, desktop, and a 1080p TV with a gamepad.
- [ ] Interactive UI uses `CoreUISafeInsets`. Nothing sits in the mobile reserved zones. Custom buttons are near the jump button.
- [ ] Every action has keyboard, gamepad and touch bindings. Gamepad can reach every element. Initial selection is set. The console chat window is disabled.
- [ ] Hints follow `PreferredInput`. PreferredTextSize, PreferredTransparency and ReducedMotion are honoured. No body text relies on TextScaled.
- [ ] All user-generated text is filtered on the server. Prompt-triggered actions are validated on the server.
- [ ] **(HR)** Offer popups are small, dismissible and well-timed (never in the first minutes or on loading), rate-limited, and honest (no fake discounts or restarting timers).

### Loading

- [ ] Join-to-playable is ≤ 10–15 s on low-end Android. The loading screen has a Skip button, has no forced long minimum, and never waits on spatial instances.
- [ ] ReplicatedFirst and ReplicatedStorage are lean. Preloading covers only the loading screen and key menu art.

### Live monitoring after launch

- [ ] Performance Dashboard alerts set for client crash rate (above 2–3 %), server heartbeat and memory. `ServerLowMemoryWarning` is logged.
- [ ] Re-run the MicroProfiler and Scene Analysis after every content update. Content creep is the usual cause of regressions.

Sources: creator-docs:performance-optimization/index.md, creator-docs:performance-optimization/identify.md, creator-docs:performance-optimization/improve.md, creator-docs:performance-optimization/monitor.md, creator-docs:performance-optimization/test-on-hardware.md, creator-docs:workspace/streaming/techniques.md, creator-docs:workspace/collisions.md, creator-docs:production/publishing/console-guidelines.md, creator-docs:production/publishing/accessibility.md, creator-docs:ui/text-filtering.md

## 5.14 Contradictions, version-sensitive facts and open questions

### Contradictions between sources (newer or stricter value preferred)

| Topic | Source A | Source B | Resolution used here |
|---|---|---|---|
| Max texture size | Texture spec resolution section: up to 4096² supported | UV and PBR sections and the env-art curriculum: max 1024² | Treat **1024² as the practical max**. 4096 is a technical upload limit, not a budget |
| Texel density | 256² per 5×5 studs (about 51 px/stud) | PBR: 256² per 2×2×2 units (about 128 px/stud) | About 50 px/stud for the world, up to about 100 for close props |
| Audio upload quota | audio/assets.md: 2,000 per 30 days verified, 100 unverified | cloud/guides/usage-assets.md: 100 a month verified, 10 unverified | Plan pipeline uploads around the **stricter Open Cloud** numbers until verified live |
| Loading-screen minimum time | loading-screens.md samples force `task.wait(5)` | improve.md: defer work, offer Skip | **No forced minimum**; Skip button after a few seconds |
| NPC animation replication | Animator.yaml: non-character animations must play on the server to replicate | improve.md: play NPC animations on the client for performance | Ambient NPCs animate locally per client; server-played only where timing must match |
| Anchoring and GPU | One tutorial implies anchoring saves GPU | Physics docs: anchoring removes simulation cost (CPU) | Anchoring is a **CPU/physics** win; rendering is unaffected |
| Collision of non-colliding parts | Intuition: CanCollide off means no collision cost | improve.md: collision geometry is still stored | Set **Box** fidelity on non-colliding meshes |

### Version-sensitive features (re-verify against live docs)

- **Lighting:** `LightingStyle` and `PrioritizeLightingQuality` replaced `Lighting.Technology`. Legacy, Compatibility and Unified are deprecated.
- **Streaming:** SLIM (`Model.LevelOfDetail = SLIM`, `EnableSLIMAvatars`) replaces legacy `StreamingMesh`. `PredictiveStreamingMode` and `Player.FrustumStreaming` are new.
- **Collision:** `CollisionFidelity.Tunable` with `CollisionPrecision`, and collision summaries (`BindToCollisionSummaries`).
- **Server authority:** `Workspace.AuthorityMode = Server` with client prediction (`SetPredictionMode`, `BindToSimulation`).
- **Lifecycle:** `Workspace.PlayerCharacterDestroyBehavior`.
- **Assets and art:** `SurfaceAppearance.AlphaMode = Opaque` (beta), the emissive SurfaceAppearance properties, Studio glTF export (beta, no animation), and Open Cloud asset content updates (FBX-only, beta).
- **UI and input:** UI styling (`StyleSheet`, `StyleRule`, `StyleLink`, `StyleDerive`, `StyleQuery`, the Style Editor), `UIShadow` (partly beta), `UserInputService.PreferredInput`, and the Input Action System (`InputContext`, `InputAction`, `InputBinding`, `PlayerScriptsUseInputActionSystem`).
- **Audio:** the new audio API (`AudioPlayer`, `AudioEmitter`, `AudioListener`, Wires) alongside legacy `Sound`.
- **Luau:** native codegen platforms (server and Android only), the 2025 `vector`, `math` and `buffer` additions, and the Scene Analysis service exposed through the Studio MCP.
- **Data:** device statistics (Android share, RAM split, Passmark), which change yearly.

### Gaps worth filling elsewhere

- There is no official per-device draw-call or triangle budget beyond the docs' "example baseline" (under 1,000 draw calls, under 1 M triangles). The house numbers in 5.1 and 5.7 are informed estimates; calibrate them on your own test devices.
- The docs don't say whether `SurfaceAppearance.Color` tint variants still share a draw call. Measure with Shift+F2 before relying on tint-heavy instancing.
- Whether the glTF importer turns Blender PBR material channels into SurfaceAppearance maps reliably isn't documented in depth. The shared `_SA` library approach in 5.7 avoids depending on it.

Sources: creator-docs:art/modeling/texture-specifications.md, creator-docs:audio/assets.md, creator-docs:cloud/guides/usage-assets.md, creator-docs:players/loading-screens.md, creator-docs:performance-optimization/improve.md, creator-docs:reference/engine/classes/Animator.yaml, creator-docs:reference/engine/enums/Technology.yaml, creator-docs:workspace/streaming/slim.md, creator-docs:workspace/streaming/frustum.md, creator-docs:parts/meshes.md, creator-docs:ui/styling/index.md, creator-docs:input/index.md, creator-docs:input/input-action-system.md, creator-docs:luau/native-code-gen.md, creator-docs:performance-optimization/test-on-hardware.md

