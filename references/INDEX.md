# Index: which file to open

One row per job. Find the row, open that file, and read only the section you need (guides over 300 lines start with a contents line). Paths are relative to the skill's root folder. A real problem often spans two or three rows. Every guide, library file, template and script is listed once.

## Start here

| Job | Open |
|---|---|
| An existing game needs to get better (audit, review, "why is it not growing/retaining/earning"): intake, ten-dimension scorecard, triage tree, Studio MCP runbook, safe-change protocol | `references/audit-existing-game.md` (report template under "Templates and scripts") |
| Building a new game from an idea: the twelve phases and their gates | `references/workflow-phases.md` |
| Standing rules and never-do lines for a topic, each block naming its owner guide | `references/decision-rules.md` |
| Who am I helping and how deep to go; a beginner's first game; realistic scope | `references/learning-paths.md` |
| A term or acronym (CCU, RFY, FTUE, DevEx, PTR, rebirth) | `references/glossary.md` |
| Every ship gate in one place (Gate A audit, Gates 0–5, weekly review, growth gate); the house-rule scan is in Gate 4 | `references/checklists.md` |

## Design

| Job | Open |
|---|---|
| What to build, what is winning or saturated, the 14 shared patterns, cozy-management and +1 format norms, the 13 thumbnail and title rules, the 250-play gate, launch timing, gap ranking (snapshot 2026-11-07) | `references/market-scan-2026-11.md` (raw report: `references/market-research-v2-raw.md`, grep only) |
| Choosing or shaping a genre | `references/genre-playbooks.md` (index), then one file in `references/genres/`: `tycoon-and-cozy-management`, `simulator-incremental`, `pet-collection-hatching`, `plus-one-evolution`, `rng-rolling`, `steal-and-defend`, `obby-tower`, `horror-coop-escape`, `rpg-dungeon`, `fighting-battlegrounds`, `tower-defense`, `shooter-pvp`, `survival-crafting`, `social-roleplay`, `fashion-dress-up`, `social-deduction`, `party-minigames`, `physics-sandbox`, `racing-driving`, `fishing`, `sports` (`.md`) |
| How successful games work; doing a teardown; trend or evergreen | `references/case-studies-teardowns.md` |
| Design theory on paper: the target feeling (MDA), fun, nested loops and the paper loop rubric, motivation, ethics for a young audience, flow and difficulty, first-session theory and goal clarity, light narrative | `references/design-foundations.md` |
| Core loop of a built or live game: loop spec, 0–10 scorecard, finding the broken stage in Creator Analytics, tuning with Configs and Experiments, juice by build cost | `references/core-loop-tuning.md` |
| Tutorials and the first session: first-minute script, teaching patterns, guidance devices, server step state, onboarding funnel, per-genre tutorials, rubric, repair procedure | `references/tutorial-and-onboarding.md` |
| Currencies, XP curves, costs, rebirth, offline income, luck and pity math, trading markets, economy simulation | `references/economy-and-progression.md` |
| Quests, daily rewards, events, season pass, LiveOps calendar, notifications, social rewards (group, like, favourite, friend), shipping updates behind flags | `references/liveops-quests-retention.md` |
| Process, one-pager, GDD, milestones, scope triage, playtesting, postmortems | `references/process-and-playtesting.md` |

## Look and feel

| Job | Open |
|---|---|
| Art direction: choosing a look that differs from the genre default (named directions for tycoon, simulator, obby, horror, roleplay), the style bible, the tells of a generic or AI-made game and the fix for each, keeping several artists consistent, art review rubric, six-week plan for a live game | `references/art-direction-and-quality-bar.md` |
| UI look: visual hierarchy (three reads), grid, colour, type and icon systems, native-first construction recipes for buttons, panels and cards, generic-UI tells, critique rubric, redesign procedure, Figma and Figma MCP hand-off, theme module | `references/ui-design-figma.md` |
| Screen-by-screen build recipes with phone sizes: HUD layouts by genre, shop, inventory, settings, codes, daily rewards, rebirth, notifications, loading | `references/ui-screen-recipes.md` |
| UI motion: motion tokens, button feedback, reward sequences, tween or spring, reduced-motion replacements | `references/ui-motion-and-feedback.md` |
| UI engine rules: containers, insets and sizing, UI architecture and performance, text filtering, thumb zones and pass lines, input mapping, gamepad focus, console, VR, audit scan | `references/ui-input-crossplatform.md` |
| Accessibility and comfort: colour, text size, motion and flashes, the comfort resolver and settings schema (§10), captions, remapping, assists, quality-of-life catalogue | `references/accessibility-and-player-qol.md` |
| VFX principles: shape, value, timing, particles, beams, trails, effect meshes, hit-stop and camera shake numbers (§7), client-only replication, pooling, budgets and quality scaling, flash safety | `references/vfx-and-juice.md` |
| 22 effect build recipes, layer by layer (slash, impact, projectile, explosion, aura, heal, reward burst and more) | `references/vfx-recipes.md` |
| Game feel: feedback tiers, input budget and buffer windows, gameplay camera and shake module, level metrics and soft-locks, NPC AI, procgen, save design | `references/game-craft.md` |
| Cutscenes: when one earns its place, length budgets, shot design, camera paths, client-only architecture, skip and subtitles, timeline runner, trailer capture | `references/cutscenes-and-cinematics.md` |
| Audio: the two audio systems, licensing and upload limits, SFX design, mixing numbers, spatial audio, music, UI sound sets, memory, starter sound lists | `references/audio-sfx-music.md` |
| Maps: planning from the core loop, avatar metrics, spawn and lobby, wayfinding, layout by genre, blockout and kits, streaming-aware layout, collision, procedural levels, heatmaps | `references/level-design-worldbuilding.md` |
| Lighting: how it works after unified lighting, key, fill and rim, atmosphere, post-processing ranges, local-light budgets, per-zone transitions, low-end fallbacks, presets by genre | `references/lighting-and-atmosphere.md` |
| Modelling well in Blender: silhouette, bevels, colour, budgets, recipes, a first kit | `references/blender-modeling-craft.md` |
| Blender → GLB → Roblox: naming, export, collision, textures, packages, import traps | `references/art-pipeline-blender.md` |
| Rigs, animation craft, markers, NPC animation at scale, animation bugs | `references/animation-and-rigs.md` |
| Icons, thumbnails, gameplay video and page text: composition recipes, the 150/64/32 test, Blender renders, generated-look tells, policy lines, test plan, rubric | `references/icons-thumbnails-and-store-page.md` |

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
| Remotes, RemoteGuard, threat modelling, server authority mode, exploit defence, movement checks, bans, backdoor scans, secrets | `references/networking-and-security.md` |
| DataStore limits, ProfileStore, dupe classes, the two-profile trade commit protocol, migrations, rollback and dupe runbooks, idempotent receipts, passes, teleports, MemoryStore | `references/data-and-purchases.md` |
| Frame budgets, MicroProfiler, memory, streaming, collision cost, mobile crashes, loading | `references/performance.md` |
| "It's broken": method, error decoder, symptom → cause → confirm → fix, races, live-only bugs, memory leaks, test strategy (Lune, Jest Roblox) | `references/debugging-and-testing.md` |

## Money, growth and people

| Job | Open |
|---|---|
| Products, passes, subscriptions, boosts, offers, price ladders, elasticity tests, refunds, policy, DevEx | `references/monetization-and-policy.md` |
| KPIs, the one benchmark table, analytics events, Configs, Experiments and sample sizes, Recommended For You signals, thumbnail testing, search, age tiers, matchmaking | `references/analytics-and-discovery.md` |
| Readiness gate before traffic, Ads Manager, TikTok and YouTube Shorts, creators, group and Discord, announcements, codes, localisation, rescuing a weak launch | `references/growth-and-marketing.md` |
| Child safety, maturity labels, chat rules, moderation, bans and appeals, crisis playbooks | `references/community-moderation-safety.md` |
| Teams, hiring, revenue splits, DevEx, IP and licensing, selling a game (facts with dates, not legal advice) | `references/team-business-legal.md` |
| Other agent skills, MCP servers and Luau libraries worth combining with this one, and how to vet them | `references/ai-toolchain-skills.md` |
| Background only: the original knowledge base (646 KB archive, not re-verified; where it differs from a guide, the guide is right). Grep a heading (`grep -n "^## 4.7"`), then read that range only. Sections: 1.x design, 2.x craft and patterns, 3.x platform, economy, monetization, analytics, 4.x engineering, security, data, 5.x performance, art, UI, launch | `references/knowledge-base.md` |

## Templates and scripts

| File | Use |
|---|---|
| `templates/game-audit-report.md` | Level-up mode: full report, and the compact variant for a first pass without access |
| `templates/game-one-pager.md` | Phase 2 |
| `templates/lean-gdd.md` | Phase 4 |
| `templates/economy-balance-sheet.md` | Phase 3, and economy tuning on a live game |
| `templates/monetization-product-plan.md` | Phase 8 |
| `templates/analytics-event-plan.md` | Phase 9 |
| `templates/playtest-plan.md` | Phases 5–12, weekly |
| `templates/launch-checklist.md` | Phase 11 |
| `scripts/blender/` (`export_kit.py`, `check_asset.py`, `silhouette_sheet.py`, `modeling_helpers.py`) | Headless Blender export and checks; see `scripts/README.md` |
| `scripts/images/tile_test.py` | See an icon and thumbnails the way the Home grid shows them |
| `scripts/studio/house_rule_scan.luau` | Read-only scan of a place for house-rule debt (edit mode only) |
