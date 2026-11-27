---
title: "AGENTS"
aliases: ["Agent guide", "How to search this vault"]
tags: ["type/index", "type/meta"]
summary: "How an AI agent finds, reads and applies the notes in the Roblox Game Dev Playbook."
---

# Agent guide: Roblox Game Dev Playbook

This folder is a playbook for designing, building, monetizing and growing Roblox games. It holds about 200 notes (Obsidian markdown with YAML front matter) and 22 reference images. Read this file first, then open only what the task needs.

## 1. Find the right note (in this order)

1. **Building or improving a whole game?** Follow `00 Start Here/How to Build a Great Roblox Game.md`, step by step.
2. **One job?** `00 Start Here/Task Router.md` has one row per job and names the note and section to open.
3. **Search:** run `python "99 Meta/search_vault.py" "your words"` from this folder (Python 3, no packages). It ranks notes by title, aliases, tags, headings and summary, adds full-text hits, and prints the path plus the matching headings. Add `-n 20` for more results.
4. **Machine index:** `99 Meta/vault-index.json` lists every note with `path`, `title`, `aliases` (including the original repo path), `tags`, `summary`, `headings`, `links_to`, `lines`, plus every image with the notes that use it.
5. **Grep:** every note starts with front matter (`title`, `aliases`, `tags`, `summary`, `source`). Grep tags such as `topic/ui` or `type/genre`, or grep full text.
6. **Overview:** `00 Start Here/Vault Map.md` lists every note by folder with a one-line purpose.

## 2. Read efficiently

- Guides are long (200 to 500 lines). Read the heading you need, not the whole file: `headings` in the index tells you which exist. Most guides start with a contents line and a "Fast routes" or beginner row.
- Links are Obsidian wikilinks: `[[Note name]]` is the file `Note name.md` somewhere in this folder; `[[Note name#Heading]]` is a heading inside it; `[[01-phone-hud-anatomy.png]]` is an image in `17 Reference Sheets/images/`.
- Notes keep paths from the original skill repo (`references/x.md`, `${CLAUDE_PLUGIN_ROOT}/...`, `scripts/blender/...`, `assets/reference/...`). Translate them with `99 Meta/Path Map.md`.
- Images: open the PNG directly to look at it. The gallery is `17 Reference Sheets/Reference Sheets Gallery.md`.

## 3. Rules that apply to every task

1. `00 Start Here/House Rules.md` overrides everything else.
2. Trust order: guides in folders 01–15 and the skills in 18, then the visual library (16), then the archive (90). The archive is the original source text; where it differs from a guide, the guide is right.
3. Platform facts (APIs, fees, payouts, policies, limits) change. Check them at https://create.roblox.com/docs before relying on them.
4. Visual Library rows link to other people's images and games. Study them for layout, hierarchy, timing and palette ideas; never copy art, logos or palettes. Those images are linked, not bundled.
5. Design before build: before gameplay code, the fantasy, three pillars, loops, the first-minute script, an economy model with numbers and an art direction exist and have passed their rubrics.
6. Done means the review gate of the guide you used passes, plus the matching ship gate in `01 Workflow and Process/Checklists and Ship Gates.md`.

## 4. Folders

| Folder | What is in it |
|---|---|
| `00 Start Here` | Agent tutorial, task router, house rules, vault map, glossary |
| `01 Workflow and Process` | Twelve phases, decision rules, playtesting, Studio workflow, audits, ship gates, AI tooling |
| `02 Game Design` | Fun, motivation, core loops, game feel, camera, AI, accessibility, teardowns |
| `03 Genres` | 22 genre playbooks plus cross-genre rules |
| `04 Market Research` | What is winning or saturated on Roblox, gaps, timing (Nov 2026) |
| `05 UI and UX` | Visual design and Figma, screen recipes, motion, input and cross-platform |
| `06 VFX, Audio and Game Feel` | VFX principles, 22 effect recipes, audio |
| `07 Art Direction, World and Lighting` | Quality bar, level design, lighting |
| `08 Models and Animation (Blender)` | Modelling craft, Blender to Roblox pipeline, rigs and animation |
| `09 Cutscenes and Cameras` | Cutscenes, trailers, a full cutscene runner module |
| `10 Luau, Systems and Engineering` | Luau, architecture, systems cookbook, physics, debugging, performance |
| `11 Security, Data and Purchases` | Networking, anti-exploit, DataStores, receipts, teleports |
| `12 Monetization and Economy` | Product catalog, policy, economy and progression math |
| `13 Retention, Onboarding and LiveOps` | Retention, LiveOps, quests, tutorials, first-time experience |
| `14 Growth, Analytics and Launch` | Discovery, analytics, marketing, icons, thumbnails, store page |
| `15 Team, Business and Community` | Team, business, legal, moderation, safety |
| `16 Visual Library` | Checked example libraries per discipline (linked) |
| `17 Reference Sheets` | 22 original diagrams (PNG), gallery, HTML sources |
| `18 Skills` | The 14 agent skills as notes, plus Skills Overview |
| `19 Templates` | Fill-in documents for each phase |
| `20 Scripts and Tools` | Blender helpers and exporter, Studio house-rule scan, image tile test |
| `21 Private Kits` | Only when the owner built the vault with `--kit`: their own UI kits and downloaded asset packs, kept verbatim. Not in the public repo; check each licence before shipping a file; the guides win where a kit disagrees |
| `90 Archive - Knowledge Base` | The original 90,000-word knowledge base, split by section |
| `99 Meta` | `vault-index.json`, `search_vault.py`, Path Map, credits, a copy of `build_vault.py` |

## 5. Tags

- Type: `type/private-kit` (folder 21), `type/guide`, `type/genre`, `type/skill`, `type/template`, `type/visual-library`, `type/reference-sheet`, `type/research`, `type/archive`, `type/index`, `type/tutorial`, `type/code`, `type/meta`, `type/rules`, `type/reference`.
- Topic: `topic/<name>`, for example `topic/ui`, `topic/vfx`, `topic/audio`, `topic/monetization`, `topic/economy`, `topic/retention`, `topic/onboarding`, `topic/performance`, `topic/security`, `topic/data`, `topic/luau`, `topic/systems`, `topic/blender`, `topic/animation`, `topic/art`, `topic/lighting`, `topic/level-design`, `topic/cinematics`, `topic/growth`, `topic/analytics`, `topic/genre`, `topic/market`. The full list is at the end of the Vault Map.

## 6. Keeping it current

The vault is generated from the `roblox-game-dev-claude-skill` repository (`scripts/vault/`). To rebuild after the repo changes, run `python scripts/vault/build_vault.py <repo folder> <vault folder>` from a clone of the repo. It deletes and rewrites only the `Roblox Game Dev Playbook` folder, so do not hand-edit generated notes; keep your own notes outside it.
