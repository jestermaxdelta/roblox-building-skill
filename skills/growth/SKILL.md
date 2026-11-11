---
name: growth
description: "Grow a Roblox game's audience. Use when the user says \"nobody plays my game\", \"how do I get players\", \"my game isn't getting impressions\", \"make a thumbnail / icon / title / description\", \"should I run ads\", \"how do I go viral on TikTok\", \"I'm about to launch\", or asks about the Roblox algorithm, Recommended For You, analytics, sponsored ads, creators, Discord or community."
argument-hint: "[your game and your goal]"
---

# Discovery, analytics and growth

Get the right players to the game, and make sure the game deserves them first.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

**Start from references, not from memory.** Before designing anything here, open the library rows listed below, pick three to five references that fit this game's genre and tone, and look at them: bundled sheets open with the Read tool; for a linked image, download it to a temporary folder and Read it, or work from its "Look at it for" note if it cannot be fetched. Write down what to take from each (layout, hierarchy, palette, timing, shape) before building, borrow principles from several sources and never reproduce one. Work built from defaults is what makes a game look generic.

## Fast routes

Pick the row that matches the task and read only those sections, in that order, instead of whole guides. Guides are in `${CLAUDE_PLUGIN_ROOT}/references/`; `game-audit-report.md`, `monetization-product-plan.md`, `economy-balance-sheet.md`, `launch-checklist.md` and `analytics-event-plan.md` are in `${CLAUDE_PLUGIN_ROOT}/templates/`. §N is the section numbered N; any other § name is the opening words of the heading. Lines is the reading cost. For anything else, use the table under "What to read".

| Task | Read exactly | Lines |
|---|---|---|
| Icon, thumbnails, title | icons-thumbnails-and-store-page.md §2, §3, §5, §8, §15, §1, §4, §10, §11, §12, §Review gate; market-scan-2026-11.md §Thumbnail and title playbook v2 | 240 |
| Nobody plays (impressions, PTR) | analytics-and-discovery.md §Level-up, §Recommended For You, §Review gate; audit-existing-game.md §4; growth-and-marketing.md §1, §11; icons-thumbnails-and-store-page.md §Level-up; market-scan-2026-11.md §Discovery facts that change design decisions | 210 |
| Should I run ads? | growth-and-marketing.md §1, §3, §10, §Review gate; checklists.md §Growth gate | 174 |
| About to launch | launch-checklist.md (whole); checklists.md §Gate 5, §Growth gate; growth-and-marketing.md §1, §7; market-scan-2026-11.md §Launch checklist from the v2 report; analytics-and-discovery.md §Launch checklist | 234 |
| TikTok, creators, codes, community | growth-and-marketing.md §4, §5, §6, §8, §10, §Review gate; community-moderation-safety.md §10, §14 | 189 |
| Analytics events | analytics-and-discovery.md §Analytics: what to measure, §Event API and limits, §Experiments and Configs, §Review gate; analytics-event-plan.md (whole) | 218 |

## What to read

| When | Open |
|---|---|
| Icons, thumbnails, video thumbnails, the game page: composition recipes, tile tests, AI-look tells, rubric | `${CLAUDE_PLUGIN_ROOT}/references/icons-thumbnails-and-store-page.md` |
| KPIs, benchmarks, analytics events, Configs, Experiments, Recommended For You, age tiers | `${CLAUDE_PLUGIN_ROOT}/references/analytics-and-discovery.md` |
| Ads, TikTok and YouTube Shorts, creators, community, launch and update marketing, what breaks the rules | `${CLAUDE_PLUGIN_ROOT}/references/growth-and-marketing.md` |
| What is winning or saturated, thumbnail rules, the 250-play gate, launch timing | `${CLAUDE_PLUGIN_ROOT}/references/market-scan-2026-11.md` |
| Community, moderation, child safety, maturity labels | `${CLAUDE_PLUGIN_ROOT}/references/community-moderation-safety.md` |
| Launch gate | `${CLAUDE_PLUGIN_ROOT}/templates/launch-checklist.md` and `${CLAUDE_PLUGIN_ROOT}/references/checklists.md` |
| Event plan to fill in | `${CLAUDE_PLUGIN_ROOT}/templates/analytics-event-plan.md` |
| Reference images: icons and thumbnails of hit games, GFX tutorials | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/icons-and-thumbnails.md` |
| Tile-test script and the icon readability sheet (20) | `${CLAUDE_PLUGIN_ROOT}/scripts/images/tile_test.py` and `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- No paid traffic while bounce or D1 sits below the game's dashboard benchmark median (no dashboard benchmark: D1 above the 11% house target), likes sit under 85% or the crash rate is above 2–3%: ads send players into the funnel you have.
- Icons and thumbnails are designed from real captures or Blender renders, never AI-generated; check each at 150, 64 and 32 px on dark and light before uploading.
- Thumbnails and icons show real gameplay from the first minute. No clickbait: a misleading tile is punished by the bounce it causes.
- Never put "free Robux", giveaways or "like for rewards" in the title, thumbnail or description.
- Social rewards are bonuses only, asked after the first win through the offer gate. Group join (verified on the server) and friend join are the default; like and favourite rewards are a risk to re-check before shipping and leave out if in doubt; no reward for off-platform actions such as joining a Discord.
- No links, invite codes or handles inside the game; social links live on the game's page.
- Design for clips: moments worth recording do more than any ad budget.
- Thumbnail tests vary one family at a time (promise, composition, text, colour), keep the current winner in the set and are not restarted inside 7 days. Read play-through beside first-play bounce and playtime: since 15 June 2026 ranking uses PTR and bounce, not qualified PTR, and PTR is not comparable across 12 October 2026. Change the icon only with an update, one element at a time.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If players arrive but leave: use the `retention` skill.
- If the whole game needs an audit: use the `level-up` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
