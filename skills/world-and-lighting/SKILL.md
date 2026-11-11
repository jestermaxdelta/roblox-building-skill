---
name: world-and-lighting
description: "Give a Roblox game a distinct, cohesive look and fix its maps and lighting. Use when the user says \"my game looks generic / cheap / like AI slop / like every other game\", \"the style doesn't fit together\", \"my map feels empty / cluttered / confusing\", \"players get lost\", \"the lighting looks flat / ugly\", \"make it look better\", \"build a map / lobby / obby / arena / town\", or asks about art style, a style guide, atmosphere or post-processing."
argument-hint: "[the map, area or mood]"
---

# Art direction, maps, level design and lighting

Make a world that looks like one game made on purpose, guides players, and runs on phones.

## How to work

Follow this loop every time.

1. **Look first.** Read what exists before judging: the relevant scripts and instances (Rojo tree, or the Studio MCP: `list_roblox_studios` and `get_studio_state` first, then `script_grep`, `search_game_tree`, `inspect_instance`, `screen_capture`) and any numbers the user gave. Without access, give a short first pass from what they said and ask for at most three things that would change the answer.
2. **Diagnose.** Match what you see against the "Level-up: symptom → cause → fix" table in the reference for this topic. Name the cause in one sentence, with the evidence.
3. **Recommend.** A short ranked list (impact × confidence ÷ effort), the option you recommend and one bolder alternative, pitched at the developer's level: three explained actions for a beginner, the full list with measurements for an expert.
4. **Implement.** Do not stop at advice. Make the top changes in the same turn when you can reach the code or Studio. Pause and ask only before something hard to undo or outward-facing: publishing, changing save data or its schema, creating or repricing products, spending Robux or money, deleting the user's work, or a design choice that is truly the owner's taste.
5. **Verify and report.** Check the work against the reference's review gate, playtest through the Studio MCP when it is connected, then say what changed, what was not verified, and which number will show whether it worked.

On a live game, change it safely: note the baseline number, put the change behind a Config flag where possible, never break saves, change one variable at a time.

**Start from references, not from memory.** Before designing anything here, open the library rows listed below, pick three to five references that fit this game's genre and tone, and look at them: bundled sheets open with the Read tool; for a linked image, download it to a temporary folder and Read it, or work from its "Look at it for" note if it cannot be fetched. Write down what to take from each (layout, hierarchy, palette, timing, shape) before building, borrow principles from several sources and never reproduce one. Work built from defaults is what makes a game look generic.

## What to read

| When | Open |
|---|---|
| Art direction: the tells of a generic or AI-made game per discipline and the fix for each, the style bible, reference boards, review rubric, ordered passes to raise a live game | `${CLAUDE_PLUGIN_ROOT}/references/art-direction-and-quality-bar.md` |
| Layout by genre, scale and metrics, spawn and lobby, wayfinding, kits, procedural levels, diagnosis tables | `${CLAUDE_PLUGIN_ROOT}/references/level-design-worldbuilding.md` |
| Lighting, atmosphere, post-processing ranges, presets by genre, low-end fallbacks | `${CLAUDE_PLUGIN_ROOT}/references/lighting-and-atmosphere.md` |
| Kit pieces: modelling them and getting them into Roblox | `${CLAUDE_PLUGIN_ROOT}/references/blender-modeling-craft.md` and `${CLAUDE_PLUGIN_ROOT}/references/art-pipeline-blender.md` |
| Streaming and draw-call cost of the layout | `${CLAUDE_PLUGIN_ROOT}/references/performance.md` |
| Reference images: environments, maps and lobbies | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/environments-and-maps.md` |
| Reference images: lighting and mood | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/lighting-and-mood.md` |
| Bundled sheets: lighting diagram, spawn view and avatar metrics, style-bible one-pager (16–18) | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- Decide the look before building: a one-page style bible with measurable rules (palette and value range, shape language, bevel rule, material list, lighting key) that every asset is checked against.
- Cohesion beats detail. A small kit used consistently reads as designed; mixed sources, even detail everywhere and default materials read as generic.
- Plan the map from the core loop: decide what each space must teach and how long it should take before placing anything.
- The first frame after spawn shows the objective, a landmark and something moving.
- No dressing until the blockout passes a walk test on a phone. Blockouts use a Blender blockout kit, never primitive Parts that ship.
- Terrain only with the owner's approval for that game.
- Lighting belongs to the client, one writer per property. Shadows vanish at low quality levels, so contrast must also come from colour and baked shading; the low-detail mode follows the player's own toggle, never `SavedQualityLevel`.
- Review with the squint, phone-size, greyscale and one-screenshot tests before calling it done.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the models themselves look amateur: use the `models-and-animation` skill.
- If the map is too heavy for phones: use the `performance` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
