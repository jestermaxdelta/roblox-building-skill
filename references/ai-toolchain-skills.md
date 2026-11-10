# AI toolchain: skills, MCP servers and open-source tools to combine with this skill

A verified catalogue of agent skills, MCP servers, Blender and Figma bridges and Luau libraries that pair with `roblox-game-design`, with a trust note on each. Open it when setting up a machine or repo for a new game, when an audit finds a missing or risky tool, or before installing anything third-party. Nothing here overrides the house rules: when a tool can generate meshes, import marketplace assets or build with primitive Parts, that feature stays off.

How to read it: every repository below was seen through the GitHub API on 2026-11-10. ★ and "last push" are GitHub's `stargazers_count` and `pushed_at` (a push to any branch, so it can be newer than the last release). "Read" in the trust column means a shallow clone was opened and its README, skill files and script inventory were inspected; "metadata only" means only the API record was seen. Nothing was installed or executed. All of it is `[VS]`: re-check before relying on it. Stars are not an audit (see "Safe use").

Trust tiers: **A** first-party (Roblox, Blender Foundation, Figma, Anthropic). **B** established community project with a licence, readable source and recent activity. **C** small or young project: read every file before use. **D** do not install.

## Recommended combinations

| Need | Lower-risk default | Bold option (after review) | Never |
|---|---|---|---|
| Drive Blender | Blender Lab MCP (official) plus `references/art-pipeline-blender.md` | `bpy-dev/blender-mcp` for headless saved-file tools; one Blender skill pack for technique | AI mesh generators, asset downloaders |
| Drive Studio | Studio's built-in MCP server through `Roblox/roblox-studio-agent-plugin` | `Chrrxs/robloxstudio-mcp` for profiler, memory and multi-client test tooling | Archived servers, executor MCPs, anything shipped as an `.exe` |
| Upload assets | Studio MCP `open_cloud_invoke` (no key) or a scoped Open Cloud key in CI | Official Roblox Blender add-on; Asphalt for images and audio | Cookie-based uploaders |
| UI design | Official Figma MCP server (`references/ui-design-figma.md`) | Framelink for read-only layout context | Write-capable bridges on a file you have not backed up |
| API facts | `https://create.roblox.com/docs/llms.txt`, `.md` doc pages, `Roblox/creator-docs` | A docs MCP or a dated Luau skill as a second opinion | Trusting an undated skill over the docs |
| Code quality | Rokit, Rojo, Selene, StyLua, luau-lsp (`references/engineering-architecture.md`) | A Luau standards skill as a second reviewer | Unpinned tools |

Rule of thumb: one MCP server per application, one skill per responsibility. Overlapping skills fire together and contradict each other.

## Blender MCP servers

| Project | What it does | ★ | Last push | Licence | Combine with this skill | Trust and risk |
|---|---|---|---|---|---|---|
| Blender Lab MCP (`projects.blender.org/lab/blender_mcp`, docs at `blender.org/lab/mcp-server`) | Official add-on plus MCP server: an LLM client runs Python in a live Blender over a local socket, with bundled API docs | n/a (not on GitHub) | 1.0.x in 2026 `[community]` | GPL-3.0-or-later | This is the "Blender Lab MCP bridge" the house pipeline names. Author and validate here; export in a separate headless process | **A**. Needs Blender 5.1+. Executes model-written Python with your user's permissions and no sandbox. Upstream page was unreachable from this session; facts come from a fork's README and NOTICE (read) and search summaries |
| `bpy-dev/blender-mcp` | Modified distribution of Blender Lab MCP: `_for_cli` tools that work on saved `.blend` files in fresh subprocesses, standalone `bpy` backend, runtime API lookup | 97 | 2026-09-12 | GPL-3.0 | Fits the "never export from the live session" rule: headless validation and export through MCP | **C**. Read. Self-described developer preview. Its SECURITY.md is explicit: subprocess isolation is not an OS sandbox; work on copies in a dedicated directory |
| `ahujasid/mcp-for-blender` (formerly `blender-mcp`) | Community server and add-on: `execute_blender_code`, scene inspection, screenshots, Poly Haven / Sketchfab / Poly Pizza import, AI model generation (Meshy, Tripo, Rodin, Hunyuan3D) | 33,819 | 2026-11-04 | MIT | Works as the Python bridge if the official server is unavailable | **B**. Read. Turn off every asset-import and generation tool (house rule 1). Sends an anonymous usage record unless `DISABLE_TELEMETRY=true`. Its quick install pipes a remote script into the shell: use the manual `uvx` path and pin the version. Remote bind has no authentication |

## Blender agent skills and Blender-to-Roblox tools

| Project | What it does | ★ | Last push | Licence | Combine with this skill | Trust and risk |
|---|---|---|---|---|---|---|
| `WildCake/roblox-blender-modelling` | One skill for Blender assets bound for Roblox: texel density in real units, intentional UV stacking, one mesh per rigid transform, publish each prototype once and verify MeshId reuse | 7 | 2026-09-30 | MIT | Closest match to the house pipeline; use as a second checklist for UV quality and export grouping | **C**. Read. 21 files, 4 Python scripts. Few stars, so no social proof; small enough to read fully. Its own comparison is one illustrative pair, not a benchmark |
| `EL4CTEO/blender-skills` | 28 skills for Blender 5.2 LTS: hard-surface modelling, retopology and UVs, trim-sheet texturing, baking, environment kits, game optimisation, export pipelines, asset QA, Geometry Nodes | 920 | 2026-11-07 | MIT | Technique reference for bevels, weighted normals, baking and kit building. The style bible still decides the look | **B/C**. Read. 104 Python scripts plus `install.sh` / `install.ps1`: copy the skill folders by hand and read the scripts you run |
| `arjun988/blender-skills` | 94 specialist skills (lookdev, modelling, pipeline) executed through a Blender MCP | 2,363 | 2026-11-06 | MIT | Broad technique library | **B/C**. Read. The skills are Markdown with no Python or shell scripts, so the risk is bad advice, not code (the repo also holds a few TS/JS files outside the skill folders). Install is a plain folder copy. Load a few, not all 94 |
| `RobLe3/cc-blender-skill` | 30 chain-loaded skills; supports the official Blender Lab MCP first, the community server second | 156 | 2026-10-12 | MIT | Orchestration pattern for multi-step modelling tasks | **C**. Read. 37 scripts. Routes some tasks to the community server's download and generation tools: block those |
| `majidmanzarpour/blender-game-skills` | `blender-image-to-3d`: scripted modelling from concept art through gated phases to a rigged GLB or FBX, each phase checked on renders and measurements | 174 | 2026-09-24 | MIT | Concept-to-asset flow when the owner supplies concept art. Scripted Blender modelling is Blender authoring, so it is within rule 1 | **C**. Read. 9 scripts. Installs through `npx skills`: pin the commit |
| `elithril/blender-kiln` | Claude Code plugin: describe or photograph an object, get a modelled, validated, measured export. States "no marketplace, no AI generation" | 204 | 2026-11-03 | MIT | Validation and measurement ideas | **C**. Read. 102 scripts and an approval hook: review before enabling. Textures come from CC0 scans, which fights a single palette or trim library |
| `dillydog580/animate-roblox-characters` | R6 and R15 character animation in Blender on Studio-derived rigs; exports `.rbxanim` or animation-only FBX with pose and loop audits | 30 | 2026-07-15 | MIT | NPC and emote animation alongside the art pipeline | **C**. Read. 11 scripts |
| `Roblox/roblox-blender-plugin` | Official Blender add-on: OAuth login, uploads selected objects as packages through Open Cloud, re-uploads as new package versions | 258 | 2026-04-20 | MIT | An upload route that keeps package ids stable (art-pipeline "Upload routes") | **A**. Read. Reference implementation; Blender 3.2+ |
| `Cautioned/Blender-Animations-Plugin` | Animation import and export between Blender and Studio (Blender add-on plus Studio plugin over a local port) | 117 | 2026-11-06 | GPL-3.0 | Hand-keyed animation round trip | **C**. README read. Opens a local server on port 31337; run it only while syncing |
| `Gl2imm/RBX_Toolbox` | Blender 4.5+ add-on collecting Roblox dummies, templates and helpers | 102 | 2026-10-08 | GPL-3.0 | Source of an R15 scale dummy | **C**. README read. Do not ship any mesh bundled with it |
| `TylerAtStarboard/Roblox-BlenderBridge` | Live-syncs meshes, textures and armatures to Studio over websockets; bulk upload without an Open Cloud key; versions existing assets | 26 | 2026-10-02 | MIT | Alternative iteration loop | **C**. README read. Depends on a Studio beta API `[VS]` |
| `KhronosGroup/glTF-Blender-IO` | The glTF exporter that ships inside Blender | 1,677 | 2026-11-05 | Apache-2.0 | Source of truth for `export_scene.gltf` options | **A/B**. Metadata only |
| `mrven/Blender-Texel-Density-Checker` | Measures and sets texel density | 463 | 2026-07-06 | GPL-3.0 | Enforce the bible's px-per-stud value | **B**. Metadata only |
| `jackTabsCode/asphalt` | CLI that uploads images, audio, animations and models and generates Luau id tables | 167 | 2026-07-28 | MIT | Icon, UI and audio ids as code. Its README advises the 3D Importer over the web API for models | **B**. README read. Needs an Open Cloud key: scope it and keep it in the environment |

## Figma MCP servers and skills

| Project | What it does | ★ | Last push | Licence | Combine with this skill | Trust and risk |
|---|---|---|---|---|---|---|
| Official Figma MCP server (`figma/mcp-server-guide`) | Remote server: design context, screenshots, variables, write to canvas, FigJam; ships its own skills | 2,170 | 2026-11-09 | none on the guide repo | The default for the Figma-to-Roblox UI workflow in `references/ui-design-figma.md` | **A**. Read. Starter plans and View or Collab seats get about 6 read tool calls a month; Dev and Full seats get per-minute limits. Write-to-canvas is free only during its beta `[VS]` |
| `GLips/Figma-Context-MCP` (Framelink) | Read-only: simplified layout and style data for coding agents | 16,183 | 2026-10-27 | MIT | Feed frame geometry to an agent that builds ScreenGuis | **B**. README read. Needs a Figma access token; its sample config passes the key on the command line, so set `FIGMA_API_KEY` in the environment instead |
| `southleft/figma-console-mcp` | Design-system extraction, variable and token sync, canvas writes through a desktop bridge plugin, parity checks | 3,253 | 2026-10-29 | MIT | Token export for a UI theme module | **B**. README read. Large write surface: duplicate the file first |
| `grab/cursor-talk-to-figma-mcp` | MCP server, Figma plugin and local websocket for reading and modifying a file | 7,096 | 2026-07-26 | MIT | Programmatic layout edits | **B**. README read. Setup pipes a remote script into bash to install Bun: install Bun yourself |
| `figma/community-resources` | Index of open-source plugins, widgets and agent skills | 863 | 2026-07-17 | MIT | Discovery | Read. Its own disclaimer: not endorsed by Figma; do your own security review |
| `xtrair/figma-to-roblox-ui`, `NoTwistedHere/Figma-to-Roblox` | Figma-to-Studio GUI import (a Claude skill and a converter) | 7; 32 | 2026-09-24; 2026-08-11 | MIT; MPL-2.0 | See the comparison in `references/ui-design-figma.md` | **C**. Metadata only |

## Roblox Studio MCP servers

| Project | What it does | ★ | Last push | Licence | Combine with this skill | Trust and risk |
|---|---|---|---|---|---|---|
| Studio built-in MCP server (docs: `studio/mcp.md`) `[official]` | stdio server inside Studio: script read, search and `multi_edit`; tree search and `inspect_instance`; `execute_luau`; play control, console, screenshots, input; `open_cloud_invoke`; a `skill` tool that loads Studio's own skills (`rbx-open-cloud-usage`, `rbx-permissions`, `rbx-import-asset`) | n/a | ships with Studio | n/a | The build-and-test tool this skill assumes. Working rules: SKILL.md and engineering-architecture.md | **A**. Docs warn that clients can read and modify open places. Each game starts at the Balanced Open Cloud level; keep it there or go Custom, never Full access by default. Generation and Creator Store tools exist and stay unused for shipped content |
| `Roblox/roblox-studio-agent-plugin` | Official Claude and ChatGPT/Codex plugin (v0.2.3): configuration and a setup skill that launch Studio's own MCP binary | 32 | 2026-11-10 | MIT | Install route for Claude Code (`/plugin`, search "Roblox Studio") | **A**. Read. Contains no code. Its README says to save or publish a version first because not every agent change can be undone |
| `Chrrxs/robloxstudio-mcp` | Maintained community server and Studio plugin: runtime eval on server and client, solo and multi-client playtests, script and MicroProfiler captures, memory breakdown, scene analysis, screenshots | 363 | 2026-11-09 | MIT | Evidence gathering for `references/performance.md` and `references/audit-existing-game.md` | **B**. README and SECURITY.md read. The documented install is `npx -y @chrrxs/robloxstudio-mcp@latest --auto-install-plugin`: pin an exact version instead and install the Studio plugin by hand. Eval tools run arbitrary Luau, so use a copy of the place and remove the plugin after the audit |
| `hope1026/weppy-roblox-mcp` | Commercial toolkit: MCP server, Studio plugin, dashboard, multi-place work, sync | 75 | 2026-11-06 | custom (has a commercial licence file) | Not needed with the built-in server | **C**. README read. Free and paid tiers; Google Analytics telemetry unless disabled; one-line script installers |
| `n4tivex/mcp-roblox-docs` | Read-only documentation server: API reference, Open Cloud, Luau, DevForum search (`uvx mcp-roblox-docs`) | 16 | 2026-09-15 | none | Second source for API checks | **C**. README read. No licence. Read-only, so low blast radius; pin the PyPI version |
| `Roblox/studio-rust-mcp-server` | Roblox's earlier standalone server | 500 | 2026-04-03 | MIT | Migrate to the built-in server | Archived. README: no longer developed |
| `boshyxd/robloxstudio-mcp` | Earlier community server | 499 | 2026-06-06 | MIT | Migrate to the built-in server or the Chrrxs fork | Archived 2026-06; the author reports losing access to the npm account, so do not run `npx -y robloxstudio-mcp@latest` |
| `Roblox/open-game-eval` | Roblox's benchmark for agents working in Studio | 76 | 2026-10-05 | MIT | Read its failure analysis before designing agent workflows | **A**. Metadata only (cited in engineering-architecture.md) |

Do not install (tier D), as observed on 2026-11-10:
- `Nanoutrolley/roblox-studio-mcp` (283 ★, MIT file present): the README tells the reader to download an archive through an off-GitHub link, run `ProjectFiles.exe` and "inject the script". The repository holds 17 lines of placeholder Python and no MCP server.
- A cluster of repositories with 68–76 ★, no licence, titles ending in "2026" and a push on the day of the search (for example `chandtheblues99-ai/studio-bridge-mcp`: a README, two SVG "Download" buttons and an HTML page, no source).
- "Executor" MCP servers that drive a live Roblox client through an exploit. They break the Roblox Terms of Use and put the account that owns the game at risk.

## Roblox, Luau and game-design agent skills

| Project | What it does | ★ | Last push | Licence | Combine with this skill | Trust and risk |
|---|---|---|---|---|---|---|
| `MSayib/roblox-dev-skill` | Router plus 14 references on Luau, client-server, security, DataStores, UI, performance, monetisation and the Studio MCP; states the Studio and Luau versions it was last verified against | 85 | 2026-11-07 | MIT | Second opinion on API currency | **B/C**. Read. Ships 11 Python and 7 shell or PowerShell scripts (installers, tests, API-dump monitors by path): copy the skill by hand and run none of them unread |
| `andrian-syh/roblox-best-practices-skill` | Luau coding standard: a rule card routing to reference files | 14 | 2026-11-08 | MIT | Already a source for knowledge-base 4.10. Use as a code-review rubric | **C**. Read. Mostly Markdown |
| `EL4CTEO/roblox-skills` | 23 skills; CI type-checks each Luau example and flags deprecated APIs | 96 | 2026-11-03 | MIT | Narrow topic skills (Open Cloud, Studio MCP) | **C**. Read. 3 shell scripts |
| `nonlooped/roblox-suite` | 16 API-selection skills, each linked to the official page it was reviewed against | 29 | 2026-11-05 | MIT | Quick API lookups with sources | **C**. Read. Markdown only |
| `TabooHarmony/roblox-brain` | 29 skills in Core, Gameplay, Design and Tools sets | 178 | 2026-10-15 | MIT | Gameplay recipes (camera, NPCs, input) | **C**. Read. 6 scripts |
| `gamedev-skills/awesome-gamedev-agent-skills` | 77 engine and discipline skills; eight `roblox-*` skills plus level design, game feel, game UI/UX, genre packs | 8,073 | 2026-11-09 | Apache-2.0 | Engine-agnostic design disciplines to cross-check `game-craft.md` | **B**. Directory listing read; skill bodies not reviewed |
| `adnvli/vfxskill` | VFX and animation through the stock Studio MCP, with frame-by-frame self-review | 39 | 2026-10-19 | MIT | VFX polish pass under `performance.md` particle budgets | **C**. Read. 2 scripts; needs Node 18+ |
| `brockmartin/roblox-game-skill` | Single large skill: router plus 16 references across design, Luau, monetisation, security | 425 | 2026-03-04 | none | Comparison reading only | **C**. Read. No licence, and eight months without a push on a platform that ships weekly |
| `SyphoDev-yt/roblox-ai-skills` | 11 skills and sub-agents from idea to playtest, including text-to-3D model and texture generation | 141 | 2026-11-04 | custom file | Conflicts with this skill: its 3D and texture stages generate meshes (rule 1) and its code scaffold uses Knit (archived) | **C**. Read. 155 Python scripts. Its own notice records a Kaggle account ban from the batch stage |
| `izzyfrm/roblox-ai` | Media library: 12,165 images, 5 clips, 2,210 CC0 sound effects sorted as UI, icon and thumbnail references | 191 | 2026-11-05 | none | Visual reference for UI and thumbnail study | **C**. README read. No licence and mixed provenance: reference only, never ship a file from it |
| `fagemx/gstack-game`, `rondorkerin/gamestack` | Engine-agnostic game design and production skill sets | 83; 34 | 2026-05-31; 2026-06-30 | MIT; MIT | Possible cross-check for `process-and-playtesting.md` | **C**. Metadata only |

Ecosystem plumbing: `anthropics/skills` (191,402 ★, pushed 2026-11-06; Anthropic's public skills repository), `agentskills/agentskills` (27,117 ★, Apache-2.0; the Agent Skills specification), `vercel-labs/skills` (38,786 ★, MIT; the `npx skills` installer several repos above use), and the index lists `VoltAgent/awesome-agent-skills` (37,018 ★), `ComposioHQ/awesome-claude-skills` (79,163 ★) and `hesreallyhim/awesome-claude-code` (57,654 ★). An index entry is a pointer, not a review.

## Luau open-source libraries by category

Verdicts live in `references/engineering-architecture.md` (toolchain, frameworks), `references/data-and-purchases.md` (data) and `references/networking-and-security.md` (remotes); this table adds category coverage and GitHub state. Where a verdict there cites a release or default-branch commit, trust it over `pushed_at`.

| Category | Library (★, last push, licence) | Status |
|---|---|---|
| Data | `MadStudioRoblox/ProfileStore` (352, 2025-07-31, Apache-2.0) | House default; quiet because finished |
| Data | `paradoxum-games/lyra` (156, 2026-03-25, MIT); `leifstout/dataService` (88, 2026-02-26, MIT) | Lyra: evaluate for transactions; dataService: metadata only |
| Data | `MadStudioRoblox/ProfileService` (332, 2024-10-13); `buildthomas/MockDataStoreService` (84, 2023-08-15) | Superseded; stale |
| Networking | `1Axen/blink` (192, 2026-11-07, MIT); `red-blox/zap` (190, 2026-06-23, MIT); `ffrostfall/ByteNet` (185, 2025-08-01, MIT) | Blink and Zap active; ByteNet quiet for 15 months |
| Networking | `MadStudioRoblox/Replica` (77, 2025-08-07, Apache-2.0); `Data-Oriented-House/Squash` (66, 2026-01-04, MIT) | State replication; buffer serialisation |
| UI | `dphfox/Fusion` (813, 2026-02-02, MIT); `centau/vide` (355, 2026-10-26, MIT); `jsdotlua/react-lua` (582, 2025-05-23, MIT); `Roblox/react-luau` (589, 2026-10-30, MIT, read-only mirror) | All usable; choose per `ui-input-crossplatform.md`. `Roblox/roact` is archived |
| UI tooling | `PepeElToro41/ui-labs` (202, 2026-10-14, GPL-3.0); `flipbook-labs/flipbook` (124, 2026-11-05, MIT); `SirMallard/Iris` (362, 2026-10-24, MIT); `1ForeverHD/TopbarPlus` (245, 2026-10-20) | Storybooks; immediate-mode debug UI; top-bar icons |
| State | `littensy/charm` (275, 2026-10-01, MIT); `littensy/reflex` (109, 2025-12-21, MIT); `Roblox/rodux` (338, 2026-06-30, Apache-2.0) | Charm active; Reflex and Rodux slow |
| ECS | `Ukendio/jecs` (484, 2026-10-22, MIT); `matter-ecs/matter` (119, 2024-12-31, MIT) | jecs active; Matter stale |
| Testing | `Roblox/jest-roblox` (50, 2026-11-10, MIT); `lune-org/lune` (977, 2026-10-21, MPL-2.0) | Defaults for in-engine and off-engine tests. `Roblox/testez` is archived; `jsdotlua/jest-lua` last pushed 2024-12 |
| Motion | `littensy/ripple` (137, 2026-07-18, MIT); `fraktality/spr` (146, 2024-07-31, MIT); `ffrostfall/crunchyroll` (99, 2025-12-13, MIT) | Ripple active; spr finished and small; crunchyroll is a custom animation solver (metadata only). `Reselim/Flipper` last pushed 2021 |
| Utilities | `Sleitnick/RbxUtil` (474, 2026-08-11, MIT); `howmanysmall/Janitor` (153, 2026-07-28, MIT); `evaera/roblox-lua-promise` (354, 2024-08-06, MIT); `osyrisrblx/t` (335, 2025-03-11, MIT); `evaera/Cmdr` (544, 2026-10-21, MIT); `1ForeverHD/ZonePlus` (101, 2024-07-04, MIT) | RbxUtil (Signal, Trove, Component) is the house baseline. `Sleitnick/Knit` is archived |
| Toolchain | `rojo-rbx/rojo` (1,862, 2026-10-31); `rojo-rbx/rokit` (507, 2026-09-27); `UpliftGames/wally` (511, 2026-10-12); `Kampfkarren/selene` (839, 2026-10-01); `JohnnyMorganz/StyLua` (2,335, 2026-10-30); `JohnnyMorganz/luau-lsp` (563, 2026-11-08); `seaofvoices/darklua` (249, 2026-07-13); `pesde-pkg/pesde` (131, 2026-11-09); `roblox-ts/roblox-ts` (1,331, 2026-10-30) | Active. Pin exact versions in `rokit.toml` |
| Open Cloud | `Sleitnick/rbxcloud` (140, 2025-03-23, MIT); `blake-mealey/mantle` (116, 2026-05-28, MIT) | rbxcloud quiet; Mantle unmaintained per its README (engineering-architecture.md) despite a 2026 push |

Vendor or pin every library; commit `wally.lock`. A library with no push in a year is acceptable only if it is small, finished and you have read it.

## Safe use

Skills are instructions an agent will follow; MCP servers and their plugins are programs with your permissions. Security vendors reported malicious skills and lookalike MCP servers in public registries during 2026 `[community]`, and the tier D list above shows the same pattern in the Roblox niche.

Before installing anything:
1. **Identify the publisher.** First-party tier A when one exists. Check that the repository is the real one (owner name, age, licence, source that matches the description). Stars can be bought.
2. **Read it at a fixed commit.** Clone, record the SHA, read `SKILL.md`, every script, every hook and every `plugin.json` or MCP config. A skill that asks the agent to fetch remote instructions, disable confirmations or read files outside the project is disqualified.
3. **Pin.** Vendor the reviewed folder or reference the commit SHA. Pin npm and PyPI versions exactly; never `@latest`, never `curl … | sh` or `irm … | iex`. Re-review on every update.
4. **Least privilege.** Studio MCP at Balanced or Custom with only the scopes the task needs and one approved upload folder. Blender MCP on copies of `.blend` files in a dedicated directory, bound to localhost only. Third-party Studio plugins only on a copy of the place, removed afterwards.
5. **Keys.** Never paste an API key, OAuth token or `.ROBLOSECURITY` cookie into a chat, a skill file, a prompt or a committed config. Keys live in the OS keychain, environment variables or CI secrets, scoped to one group or universe and one API. Prefer `open_cloud_invoke`, which never exposes a credential to the client. Rotate any key that touched a transcript.
6. **House-rule filter.** Disable or ignore: AI mesh and texture generators (Studio `generate_*`, Meshy, Tripo, Rodin, Hunyuan3D, Hi3DGen), asset downloaders (Poly Haven, Sketchfab, Poly Pizza), Creator Store search and insert, and any skill that builds maps from primitive Parts. Agent-scripted modelling inside Blender is Blender authoring and is allowed.
7. **Back up first.** Publish or save a version of the place and commit the repo before an agent session; duplicate Figma files before write-capable tools.

Read-only triage of a cloned repository (a clean result is not an audit):

```bash
REPO=path/to/clone
git -C "$REPO" log -1 --format='%H %cd' --date=short        # the commit you reviewed
find "$REPO" -type f \( -name '*.sh' -o -name '*.ps1' -o -name '*.bat' -o -name '*.exe' -o -name '*.py' -o -name '*.js' -o -name '*.ts' \) -not -path '*/.git/*'
grep -rnEI 'curl |wget |Invoke-WebRequest|iex |base64 -d|eval\(|child_process|subprocess|os\.system|ROBLOSECURITY|\.ssh|\.env' "$REPO" --exclude-dir=.git
grep -rnEI '"hooks"|PreToolUse|PostToolUse|SessionStart|mcpServers' "$REPO" --exclude-dir=.git
```

## Level-up: toolchain symptoms → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent writes `wait()`, BodyMovers, legacy Chat | No current API grounding; a stale skill | Point it at `llms.txt` and the `.md` doc pages; gate with Selene and luau-lsp; drop skills with no verification date |
| Agent builds from Parts, inserts Creator Store models or generates meshes | A third-party skill or MCP tool that conflicts with rule 1 | Remove the skill or disable the tools; restate the house rules in the project's `CLAUDE.md` |
| Two skills answer the same request differently | Overlapping triggers | One skill per responsibility; house rules win |
| New tools appear, or behaviour changes between sessions | An unpinned `@latest` server or auto-updating plugin | Pin, diff and re-review |
| Studio MCP stops connecting after an update | An archived standalone server is still configured, Studio is out of date, or another app holds port 13469 | Remove the old entry; update Studio; close the other app and restart Studio (official plugin troubleshooting notes) |
| Art changes need manual re-import every time | No upload route chosen | Pick one route from art-pipeline "Upload routes" and script it |
| A key shows up in git history or a transcript | Pasted credential | Revoke and rotate now, then move to secrets |
| Audit has no numbers for memory or frame time | Only edit-mode tools connected | Add profiler and memory capture tooling for the audit, on a copy |

## Review gate

- [ ] Every installed skill, plugin and MCP server is listed in the repo with its source URL, reviewed commit or exact version, and reviewer.
- [ ] Tier A options used wherever they exist; no tier D pattern present; no archived server configured.
- [ ] No `@latest`, no pipe-to-shell installers, no executables downloaded outside a package manager or signed vendor installer.
- [ ] No credential in chat logs, skill files, MCP configs or git history; Open Cloud keys scoped and stored as secrets.
- [ ] Studio MCP Open Cloud level is Balanced or Custom; upload folder approved explicitly; place saved before agent sessions.
- [ ] Generation, download and Creator Store tools are disabled or documented as off-limits for shipped content.
- [ ] Libraries pinned and vendored; none archived; each has a verdict in the engineering or data reference.

## Sources

Accessed 2026-11-10. GitHub metadata came from `GET /search/repositories` (queries by keyword and topic: blender mcp, blender-mcp, blender skill, figma mcp, figma skill, roblox mcp, roblox-mcp, roblox studio mcp, rojo mcp, roblox skill, luau skill, game design skill, claude-skills, agent-skills, roblox blender, figma roblox, plus `repo:` look-ups for each library).

- Read (shallow clone, files opened, nothing executed): https://github.com/Roblox/roblox-studio-agent-plugin, https://github.com/Roblox/roblox-blender-plugin, https://github.com/Roblox/studio-rust-mcp-server, https://github.com/Roblox/creator-docs (`content/en-us/studio/mcp.md`, `studio/mcp-open-cloud.md`), https://github.com/bpy-dev/blender-mcp (README, SECURITY.md, NOTICE.md), https://github.com/ahujasid/mcp-for-blender, https://github.com/WildCake/roblox-blender-modelling, https://github.com/EL4CTEO/blender-skills, https://github.com/arjun988/blender-skills, https://github.com/RobLe3/cc-blender-skill, https://github.com/majidmanzarpour/blender-game-skills, https://github.com/elithril/blender-kiln, https://github.com/dillydog580/animate-roblox-characters, https://github.com/Cautioned/Blender-Animations-Plugin, https://github.com/Gl2imm/RBX_Toolbox, https://github.com/TylerAtStarboard/Roblox-BlenderBridge, https://github.com/jackTabsCode/asphalt, https://github.com/figma/mcp-server-guide, https://github.com/GLips/Figma-Context-MCP, https://github.com/southleft/figma-console-mcp, https://github.com/grab/cursor-talk-to-figma-mcp, https://github.com/figma/community-resources, https://github.com/Chrrxs/robloxstudio-mcp, https://github.com/boshyxd/robloxstudio-mcp, https://github.com/hope1026/weppy-roblox-mcp, https://github.com/n4tivex/mcp-roblox-docs, https://github.com/Nanoutrolley/roblox-studio-mcp, https://github.com/chandtheblues99-ai/studio-bridge-mcp, https://github.com/MSayib/roblox-dev-skill, https://github.com/andrian-syh/roblox-best-practices-skill, https://github.com/EL4CTEO/roblox-skills, https://github.com/nonlooped/roblox-suite, https://github.com/TabooHarmony/roblox-brain, https://github.com/brockmartin/roblox-game-skill, https://github.com/SyphoDev-yt/roblox-ai-skills, https://github.com/adnvli/vfxskill, https://github.com/izzyfrm/roblox-ai, https://github.com/gamedev-skills/awesome-gamedev-agent-skills
- Metadata only (GitHub API record): every other repository named above, at `https://github.com/<owner>/<repo>`.
- https://www.blender.org/lab/mcp-server/ and https://projects.blender.org/lab/blender_mcp (not reachable from this session; version, requirement and safety wording are search summary, corroborated by the fork's README and NOTICE)
- Reports of malicious skills and lookalike MCP servers in 2026: https://obot.ai/blog/mcp-security-agent-skills-supply-chain/, https://oecd.ai/en/incidents/2026-04-29-8e04, https://dev.to/bawbel/skill-files-are-the-new-supply-chain-attack-surface-your-ci-pipeline-does-not-know-that-yet-7i9 (search summary; figures not verified, so none are quoted)
- Not found: an agent skill or MCP server dedicated to Rojo with meaningful adoption (search returned projects with 0–7 ★); a first-party Blender skill pack.
