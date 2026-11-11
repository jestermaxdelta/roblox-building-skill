# Lean game design document: <Title>

Write this after the one-pager is approved and before the vertical slice. Keep each part short and specific; link to the economy sheet, product plan and analytics plan rather than repeating them. Structure follows the nine-part lean GDD in references/process-and-playtesting.md.

## 1. Overview

- Pitch, fantasy, pillars (copy from the one-pager; update if they changed).
- Target audience, age tier, content-maturity label, platforms, server size.
- Success metrics at soft launch: D1 <x%>, D7 <x%>, bounce under 60 s <x%>, median session <n> min, ARPDAU <>.

## 2. Core gameplay

- Verbs the player has (list each with the input on keyboard, gamepad and touch).
- Core loop diagram (micro → meso → session → meta) with the timing of each.
- Difficulty and flow: sawtooth pacing plan, hint ladder (what the game does at 10 s, 30 s, 60 s of no progress), failure handling.
- Feel targets: response times, juice tiers per action (see references/game-craft.md §1; effects in references/vfx-and-juice.md, sound in references/audio-sfx-music.md).

## 3. Systems

For each system: purpose, inputs, outputs, rules, numbers, server/client split, which reference it follows.

| System | Purpose | Server-authoritative state | Client responsibilities | Reference |
|---|---|---|---|---|
| Progression | | | | economy-and-progression.md |
| Economy | | | | economy-and-progression.md |
| Inventory / collection | | | | data-and-purchases.md |
| Quests / missions | | | | liveops-quests-retention.md |
| Social / trading | | | | liveops-quests-retention.md |
| Combat / interaction | | | | networking-and-security.md |
| Rebirth / meta | | | | economy-and-progression.md |

## 4. Content

- World: zones or stages, unlock order, the modular kit each needs.
- Asset list by class (clutter, small prop, medium prop, building module, hero, NPC, vehicle) with triangle budgets.
- NPCs and AI behaviour (models from references/game-craft.md §5).
- Audio plan: soundbed, spot ambiences, music tracks, SFX count.
- Look and feel: link to the style bible (references/art-direction-and-quality-bar.md §6); UI screens to build (references/ui-screen-recipes.md) and the effects the loop needs (references/vfx-recipes.md), each with its rubric pass mark.

## 5. First-time user experience

- Beat script for the first 10 minutes in the format of references/tutorial-and-onboarding.md §2 (control ≤ 10 s, first verb ≤ 15 s, first reward ≤ 30 s, first upgrade ≤ 2 min).
- Teaching pattern and guidance device per step (its §3 and §5), hint delay as a Config key; skip, resume and returning-player behaviour (its §8).
- Onboarding funnel steps to log (1 Spawned … 7 Session2Start).
- No offers during onboarding; any intro scene follows references/cutscenes-and-cinematics.md §15.

## 6. Economy and monetization

- Link: templates/economy-balance-sheet.md (filled).
- Link: templates/monetization-product-plan.md (filled).
- Policy notes: paid random items present <yes/no>; disclosure UI; PolicyService gates.

## 7. LiveOps plan

- Weekly update day. First four weekly updates by name.
- First event: dates, theme, KPI, event currency, sinks.
- Season pass plan (tiers, XP per day, length) if used.
- Notification and invite usage.

## 8. Technical plan

- Project layout (Rojo tree), framework choice (plain modules + loader recommended), libraries pinned (ProfileStore, RbxUtil Signal/Trove/Component).
- Remotes list: name, direction, payload type, validation rules, rate limit.
- Data schema (template table) with `SchemaVersion`, and the migration policy.
- Products and passes table with ids (filled after creation in Creator Hub; prices read at runtime).
- Streaming settings, collision policy per asset class, lighting preset.
- Performance budgets adopted (from references/performance.md).
- CI pipeline and test plan.

## 9. Production

- Milestones and dates (prototype, vertical slice, alpha, soft launch, launch window).
- Team and roles (even if one person).
- Scope cuts already made and the "if behind schedule, cut next" list.
- Playtest schedule (templates/playtest-plan.md).
- Launch checklist owner (templates/launch-checklist.md).
- Risks and mitigations (top five).
