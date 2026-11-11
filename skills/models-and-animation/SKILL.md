---
name: models-and-animation
description: "Create, fix and import 3D models and animation for Roblox using Blender. Use when the user says \"my models look bad / amateur / like free models\", \"the style doesn't match\", \"make a prop / building / vehicle / pet / character in Blender\", \"export to Roblox\", \"the mesh imports wrong / wrong size / no collision\", \"rig this\", or \"the animation is broken / doesn't play / looks stiff\"."
argument-hint: "[the asset or animation]"
---

# Blender models, import pipeline, rigs and animation

Produce a cohesive, non-generic look from Blender and get it into Roblox correctly, with collision.

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

Pick the row that matches the task and read only those sections, in that order, instead of whole guides. Guides are in `${CLAUDE_PLUGIN_ROOT}/references/` (`AD` = `art-direction-and-quality-bar.md`, `LA` = `lighting-and-atmosphere.md`, `LD` = `level-design-worldbuilding.md`, `BM` = `blender-modeling-craft.md`, `AP` = `art-pipeline-blender.md`, `AR` = `animation-and-rigs.md`); library files (`env` = `environments-and-maps.md`, `light` = `lighting-and-mood.md`, `models` = `models-props-characters.md`) are in `${CLAUDE_PLUGIN_ROOT}/references/visual-library/`; sheets are `${CLAUDE_PLUGIN_ROOT}/assets/reference/NN-*.png`. §N is the section numbered N; any other name is the opening words of a heading. For anything else, use the table under "What to read".

| Task | Read exactly | Look at |
|---|---|---|
| Model one prop to the bar | BM The numbers through Recipes, Concept, Rubric · AP Acceptance | models #1–3, #8, #16, #17, #25 |
| Build a first kit | BM The numbers, Edges, Recipes, Rubric, First kit walkthrough · LD §8–§9 · AP Naming, Modular kits, Acceptance | Sheet 17 · env #7, #11, #29, #44, #55 |
| Export to Roblox, or an import went wrong (size, pivot, collision) | AP Pipeline overview, Units, Mesh specifications, Naming, Collision authoring, Upload routes, Import traps, Level-up, Review gate · `scripts/README.md` | none needed |
| Keep several artists consistent | AD §6, §8 · BM Edges, Colour, Rubric · AP Texturing, Naming, Acceptance | Sheet 18 · models #1, #8, #10–11 |
| Make an attack, hit reaction or walk feel good | AR §4, §5, §6, Review gate | Sheet 21 · `animation.md`, the section for that move type |
| Animation is stiff, broken or not replicating | AR §12 first, then the section it points to (§5 playback, §7 replication, §3 pipeline), Review gate | Sheet 21 |
| Rig and animate from Blender | AR §1, §2, §3, Review gate · AP Upload routes | `animation.md` tool rows |

## What to read

| When | Open |
|---|---|
| Modelling craft: silhouette, bevels, colour, budgets, recipes, per-asset rubric, a first kit | `${CLAUDE_PLUGIN_ROOT}/references/blender-modeling-craft.md` |
| Blender → GLB → Roblox: naming, export, collision authoring, textures, packages, import traps, symptom table | `${CLAUDE_PLUGIN_ROOT}/references/art-pipeline-blender.md` |
| Rigs, animation craft with frame counts, markers, replication, NPC animation at scale, stiff-animation tells, bug table | `${CLAUDE_PLUGIN_ROOT}/references/animation-and-rigs.md` |
| What makes assets read as generic, and the style bible they must follow | `${CLAUDE_PLUGIN_ROOT}/references/art-direction-and-quality-bar.md` |
| Shipped export and check scripts | `${CLAUDE_PLUGIN_ROOT}/scripts/README.md` |
| Blender and Studio MCP servers and how to vet them | `${CLAUDE_PLUGIN_ROOT}/references/ai-toolchain-skills.md` |
| Reference images: props, buildings, vehicles, creatures, characters | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/models-props-characters.md` |
| Animation breakdowns and tutorials | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/animation.md` |
| Bundled sheets: style-bible one-pager, attack frame data (18, 21) | `${CLAUDE_PLUGIN_ROOT}/references/visual-library/reference-sheets.md` |

## Reading the references

- Open only the rows you need. Files over 300 lines have a contents line: read the section, not the file. Anything not listed here: `${CLAUDE_PLUGIN_ROOT}/references/INDEX.md`.
- Tags: `[official]` Roblox docs; `[VS]` version-sensitive, re-check at https://create.roblox.com/docs (or the `Roblox/creator-docs` mirror) before relying on it; `[community]` and `[lihfolk]` are other developers' practice, to test rather than trust; `[house]` is a house estimate. `Conflict:` notes record real disagreements; the house rules win, then official docs, then numbers measured on the user's own game.
- Luau in the references is unexecuted: adapt it, keep `--!strict`, test it.
- Unsure how deep to go for this person: `${CLAUDE_PLUGIN_ROOT}/references/learning-paths.md` §1–2. A term they may not know: `${CLAUDE_PLUGIN_ROOT}/references/glossary.md`.

## Rules for this topic

- 1 Blender unit is 1 stud. Check scale against the avatar before detailing.
- Readability at phone size beats detail: test the silhouette small.
- One primary texturing method per game, and one style bible everything is checked against.
- No asset ships without an explicit collision plan: a `_COL` proxy or a chosen `CollisionFidelity`.
- Reference kit pieces by package, never by hard-coded MeshId.
- Never ship temporary animation ids (`RegisterKeyframeSequence`, `RegisterAnimationClip`); publish clips under the game's owner or grant the experience permission. Load each track once and set `Priority` before `Play`.
- Drive Blender through a Blender MCP bridge, export GLB in a separate headless `blender -b` process, and upload through the Studio MCP's `open_cloud_invoke`, the official Roblox Blender add-on or the 3D Importer.

## House rules (the owner's; they override generic advice)

1. **Blender for every model.** Every visible 3D asset is authored in Blender. No primitive-Part builds, marketplace models or generated meshes ship.
2. **Everything in the world is solid.** Players and NPCs cannot walk through world objects. Held tools, pets that follow a player and short-lived effect meshes do not collide.
3. **Monetisation is pushed heavily but never invasively.** Offers are small, dismissible, well-timed and rate-limited. No fake discounts, restarting countdowns or false scarcity, and no power sold in competitive modes.

In a game that already breaks these, list each violation as a finding with a plan ranked by how visible it is; do not refuse to help or demand a rebuild. A first learning game does not need monetisation. Full text and resolutions: `${CLAUDE_PLUGIN_ROOT}/SKILL.md`, section "House rules".

## When it is really a different problem

- If the placement, layout or overall look is the problem, not the assets: use the `world-and-lighting` skill.
- If it is a cutscene or camera move: use the `cinematics` skill.
- If the scene is too heavy: use the `performance` skill.
- If it needs the whole picture (new game, genre choice, full plan): use the `roblox-game-design` skill.
