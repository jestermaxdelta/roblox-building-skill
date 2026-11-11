# Index: which file to open

One row per job. Find the row, open that file, and read only the section you need (files over 300 lines start with a contents line). Paths are relative to the skill's root folder. A real problem often spans two or three rows.

## Start here

| Job | Open |
|---|---|
| An existing game needs to get better (audit, review, "why is it not growing/retaining/earning") | `references/audit-existing-game.md`, report in `templates/game-audit-report.md` |
| Building a new game from an idea: the twelve phases and their gates | `references/workflow-phases.md` |
| Standing rules and never-do list for a topic | `references/decision-rules.md` |
| Who am I helping and how deep to go; a beginner's first game; realistic scope | `references/learning-paths.md` |
| A term or acronym (CCU, RFY, FTUE, DevEx, PTR, rebirth) | `references/glossary.md` |
| Every gate and checklist in one place, including the house-rule scan | `references/checklists.md` |

## Design

| Job | Open |
|---|---|
| What to build, what is winning or saturated, the 14 shared patterns, the 250-play gate, launch timing | `references/market-scan-2026-11.md` (raw report: `references/market-research-v2-raw.md`, grep only) |
| Choosing or shaping a genre | `references/genre-playbooks.md` (index), then one file in `references/genres/`: `tycoon-and-cozy-management`, `simulator-incremental`, `pet-collection-hatching`, `plus-one-evolution`, `rng-rolling`, `steal-and-defend`, `obby-tower`, `horror-coop-escape`, `rpg-dungeon`, `fighting-battlegrounds`, `tower-defense`, `shooter-pvp`, `survival-crafting`, `social-roleplay`, `fashion-dress-up`, `social-deduction`, `party-minigames`, `physics-sandbox`, `racing-driving`, `fishing`, `sports` (`.md`) |
| How successful games work; doing a teardown; trend or evergreen | `references/case-studies-teardowns.md` |
| Fun, motivation, flow, difficulty, progression and retention theory, rubrics | `references/design-foundations.md` |
| Designing, scoring, diagnosing and tuning the core loop; reading the funnel; experiments | `references/core-loop-tuning.md` |
| Tutorials, the first minute, guidance arrows and highlights, onboarding funnels | `references/tutorial-and-onboarding.md` |
| Currencies, XP curves, costs, rebirth, offline income, luck and pity math, trading markets, economy simulation | `references/economy-and-progression.md` |
| Quests, daily rewards, events, season pass, LiveOps calendar, notifications | `references/liveops-quests-retention.md` |
| Process, one-pager, GDD, milestones, scope triage, playtesting, postmortems | `references/process-and-playtesting.md` |

## Look and feel

| Job | Open |
|---|---|
| Art direction, style bible, the tells of a generic or AI-made game and how to fix each, art review rubric | `references/art-direction-and-quality-bar.md` |
| UI design system, visual hierarchy, colour and type, panels and buttons that look designed, Figma workflow, critique rubric | `references/ui-design-figma.md` |
| Screen-by-screen build recipes: HUD, shop, inventory, settings, codes, daily rewards, rebirth, notifications, loading | `references/ui-screen-recipes.md` |
| UI animation, button feedback, reward sequences, motion tokens | `references/ui-motion-and-feedback.md` |
| UI implementation: scaling, safe areas, thumb zones, input mapping, gamepad focus, console, VR, UI performance | `references/ui-input-crossplatform.md` |
| Accessibility, settings menu, quality-of-life features | `references/accessibility-and-player-qol.md` |
| VFX principles: shape, value, timing, particles, beams, trails, hit-stop, camera shake, budgets | `references/vfx-and-juice.md` |
| Effect-by-effect build recipes (slash, impact, projectile, explosion, aura, heal, reward burst and more) | `references/vfx-recipes.md` |
| Game feel, camera, input responsiveness, AI, procgen, save design | `references/game-craft.md` |
| Cutscenes, camera paths, shot design, skip and subtitles, trailers | `references/cutscenes-and-cinematics.md` |
| Sound effects, music, mixing, the audio API, audio licensing | `references/audio-sfx-music.md` |
| Maps, lobbies, wayfinding, layout by genre, kits, procedural levels | `references/level-design-worldbuilding.md` |
| Lighting, atmosphere, post-processing, presets by genre | `references/lighting-and-atmosphere.md` |
| Modelling well in Blender: silhouette, bevels, colour, budgets, recipes, a first kit | `references/blender-modeling-craft.md` |
| Blender → GLB → Roblox: naming, export, collision, textures, packages, import traps | `references/art-pipeline-blender.md` |
| Rigs, animation craft, markers, NPC animation at scale, animation bugs | `references/animation-and-rigs.md` |
| Icons, thumbnails, video thumbnails, the game page | `references/icons-thumbnails-and-store-page.md` |

## Visual references (things to look at before building)

Curated, quality-gated references with a note on what to study in each. Rows marked `viewed` were looked at by the curator. Third-party images are for study, never for copying.

| Aspect | Open |
|---|---|
| Bundled original reference sheets (annotated diagrams shipped with the skill: HUD anatomy, shop, buttons, colour, VFX timing, camera shots, lighting, level metrics and more) | `references/visual-library/reference-sheets.md`, images in `assets/reference/` |
| HUDs by genre and platform | `references/visual-library/ui-hud.md` |
| Shop, inventory, menus, settings, rewards, loading and other screens | `references/visual-library/ui-screens.md` |
| Buttons, icons, type, colour, panels, UI motion, kits and tools | `references/visual-library/ui-components-and-style.md` |
| VFX showcases and breakdowns | `references/visual-library/vfx.md` |
| VFX tutorials, courses, tools and texture sources | `references/visual-library/vfx-learning.md` |
| Cutscenes, camera work and trailers | `references/visual-library/cutscenes-and-cameras.md` |
| Tutorials and onboarding in shipped games | `references/visual-library/tutorials-and-onboarding.md` |
| Environments, maps and lobbies | `references/visual-library/environments-and-maps.md` |
| Props, buildings, vehicles, creatures and characters | `references/visual-library/models-props-characters.md` |
| Lighting and mood studies | `references/visual-library/lighting-and-mood.md` |
| Animation breakdowns and tutorials | `references/visual-library/animation.md` |
| Sound references, libraries with their licences, tools | `references/visual-library/audio-and-sound.md` |
| Icons and thumbnails of hit games, GFX tutorials | `references/visual-library/icons-and-thumbnails.md` |

How to use them: pick three to five references that fit the game's genre and tone, look at them (open a bundled sheet with the Read tool; for a linked image, download it to a temporary folder and Read it; if it cannot be fetched, work from the "Look at it for" note), and write down what to take from each (layout, hierarchy, palette, timing, shape) before building. Borrow principles from several sources; never reproduce one.

## Code and systems

| Job | Open |
|---|---|
| Learning or sharpening Luau, from first script to types, parallelism and performance idioms; game math | `references/luau-mastery.md` |
| Building a gameplay system: wallet, inventory, shop, pets and eggs, quests, rounds, combat, NPCs, plots and placement, trading, leaderboards and more | `references/gameplay-systems-cookbook.md` |
| Physics, network ownership, constraints, ragdolls, projectiles, vehicles | `references/physics-and-vehicles.md` |
| Containers, loader, Rojo layout, Luau standards, toolchain, CI/CD, live-update runbook | `references/engineering-architecture.md` |
| Game Programming Patterns in Luau (state, command, observer, component, object pool, ECS choice) | `references/architecture-patterns-luau.md` |
| Studio setup, test modes, Team Create, publishing, Script Sync or Rojo, working safely through the Studio MCP | `references/studio-workflow.md` |
| Remotes, RemoteGuard, threat modelling, exploit defence, bans, backdoor scans, secrets | `references/networking-and-security.md` |
| DataStore limits, ProfileStore, receipts, dupes, the trade commit protocol, migrations, rollback, teleports, MemoryStore | `references/data-and-purchases.md` |
| Frame budgets, MicroProfiler, memory, streaming, collision cost, mobile crashes, loading | `references/performance.md` |
| "It's broken": symptom → cause → fix, live-only bugs, memory leaks, tests | `references/debugging-and-testing.md` |

## Money, growth and people

| Job | Open |
|---|---|
| Products, passes, subscriptions, boosts, offers, price ladders, elasticity tests, refunds, policy, DevEx | `references/monetization-and-policy.md` |
| KPIs, benchmarks, analytics events, Configs, Experiments, Recommended For You, age tiers | `references/analytics-and-discovery.md` |
| Ads, TikTok and YouTube Shorts, creators, community building, launch and update marketing | `references/growth-and-marketing.md` |
| Child safety, maturity labels, chat rules, moderation, bans and appeals, crisis playbooks | `references/community-moderation-safety.md` |
| Teams, hiring, revenue splits, DevEx, IP and licensing, selling a game (facts with dates, not legal advice) | `references/team-business-legal.md` |
| Other agent skills, MCP servers and Luau libraries worth combining with this one, and how to vet them | `references/ai-toolchain-skills.md` |
| Original knowledge base, 646 KB: grep a heading (`grep -n "^## 4.7" references/knowledge-base.md`), then read that range only. Sections: 1.x design, 2.x craft and patterns, 3.x platform, economy, monetization, analytics, 4.x engineering, security, data, 5.x performance, art, UI, launch | `references/knowledge-base.md` |

## Templates and scripts

| File | Use |
|---|---|
| `templates/game-audit-report.md` | Level-up mode |
| `templates/game-one-pager.md` | Phase 2 |
| `templates/lean-gdd.md` | Phase 4 |
| `templates/economy-balance-sheet.md` | Phase 3, and economy tuning on a live game |
| `templates/monetization-product-plan.md` | Phase 8 |
| `templates/analytics-event-plan.md` | Phase 9 |
| `templates/playtest-plan.md` | Phases 5–12, weekly |
| `templates/launch-checklist.md` | Phase 11 |
| `scripts/blender/` (`export_kit.py`, `check_asset.py`, `silhouette_sheet.py`, `modeling_helpers.py`) | Headless Blender export and checks; see `scripts/README.md` |
| `scripts/images/tile_test.py` | See an icon and thumbnails the way the Home grid shows them |
