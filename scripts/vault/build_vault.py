#!/usr/bin/env python3
"""Build an Obsidian-style, agent-searchable vault from the roblox-building-skill repo.

Usage: python scripts/vault/build_vault.py <repo_dir> <out_dir>
Writes <out_dir>/Roblox Game Dev Playbook/ (deleting and rewriting only that folder)
and prints a link-check report. Point <out_dir> at an Obsidian vault to install it.
The other files in this folder (AGENTS.md, CLAUDE.md, Start Here.md, search_vault.py)
are copied into the playbook.
"""
import datetime, json, re, shutil, sys, unicodedata
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
ROOT = OUT / "Roblox Game Dev Playbook"
BUILT = datetime.date.today().isoformat()

FOLDERS = {
    "start": "00 Start Here",
    "process": "01 Workflow and Process",
    "design": "02 Game Design",
    "genres": "03 Genres",
    "market": "04 Market Research",
    "ui": "05 UI and UX",
    "vfx": "06 VFX, Audio and Game Feel",
    "art": "07 Art Direction, World and Lighting",
    "models": "08 Models and Animation (Blender)",
    "cine": "09 Cutscenes and Cameras",
    "eng": "10 Luau, Systems and Engineering",
    "sec": "11 Security, Data and Purchases",
    "money": "12 Monetization and Economy",
    "ret": "13 Retention, Onboarding and LiveOps",
    "growth": "14 Growth, Analytics and Launch",
    "biz": "15 Team, Business and Community",
    "lib": "16 Visual Library",
    "sheets": "17 Reference Sheets",
    "skills": "18 Skills",
    "tpl": "19 Templates",
    "scripts": "20 Scripts and Tools",
    "kb": "90 Archive - Knowledge Base",
    "meta": "99 Meta",
}
FOLDER_ABOUT = {
    "start": "Entry points: agent tutorial, task router, house rules, vault map, glossary.",
    "process": "How work is run: the twelve phases, decision rules, playtesting, Studio workflow, audits, ship gates, AI tooling.",
    "design": "Game design fundamentals: fun, motivation, core loops, game feel, camera, AI, accessibility, teardowns of hit games.",
    "genres": "One playbook per Roblox genre (loops, numbers, monetization, pitfalls) plus cross-genre rules.",
    "market": "Market research: what is winning or saturated on Roblox, gaps, launch timing (Nov 2026 snapshot).",
    "ui": "UI/UX: visual design and Figma hand-off, screen recipes, motion, input and cross-platform.",
    "vfx": "VFX, juice and audio: principles, 22 layered effect recipes, SFX and music.",
    "art": "Art direction and quality bar, level design and worldbuilding, lighting and atmosphere.",
    "models": "Blender modelling craft, Blender to Roblox pipeline, rigs and animation.",
    "cine": "Cutscenes, camera work, trailers, plus a full cutscene runner module.",
    "eng": "Luau, architecture, gameplay systems cookbook, physics, debugging, performance.",
    "sec": "Networking, anti-exploit, DataStores, purchases (ProcessReceipt), teleports.",
    "money": "Monetization catalog and policy, economy and progression math.",
    "ret": "Retention, LiveOps, quests, tutorials and the first-time user experience.",
    "growth": "Discovery, analytics, marketing, icons, thumbnails and store page.",
    "biz": "Team, business, legal, community, moderation and safety.",
    "lib": "Curated, checked example libraries (linked images, videos, breakdowns) per discipline. Study, never copy.",
    "sheets": "22 original reference-sheet diagrams (PNG) with their HTML sources and a gallery note.",
    "skills": "The 14 agent skills: when each triggers, how it works, which notes it reads.",
    "tpl": "Fill-in templates: one-pager, lean GDD, economy sheet, monetization plan, analytics plan, playtest plan, launch checklist, audit report.",
    "scripts": "Shipped tools: Blender helpers and exporter, house-rule scanner for Studio, image tile test.",
    "kb": "Archive: the original 90,000-word knowledge base split by section. Background only; the guides win where they differ.",
    "meta": "Index files, search script, path map, credits, the build script.",
}

# src | folder key | note name | tags
TABLE = """
references/INDEX.md|start|Task Router|type/index
references/glossary.md|start|Glossary|type/reference topic/glossary
references/workflow-phases.md|process|Workflow Phases - Idea to Live|type/guide topic/process
references/decision-rules.md|process|Decision Rules and Never-Do List|type/guide topic/process topic/rules
references/process-and-playtesting.md|process|Process and Playtesting|type/guide topic/process topic/playtesting
references/studio-workflow.md|process|Studio Workflow|type/guide topic/process topic/studio
references/learning-paths.md|process|Learning Paths|type/guide topic/process topic/beginner
references/audit-existing-game.md|process|Audit an Existing Game|type/guide topic/process topic/audit
references/checklists.md|process|Checklists and Ship Gates|type/guide topic/process topic/checklist
references/ai-toolchain-skills.md|process|AI Toolchain - Skills, MCP Servers and Tools|type/guide topic/ai-tools
references/design-foundations.md|design|Design Foundations|type/guide topic/design
references/core-loop-tuning.md|design|Core Loop Tuning|type/guide topic/design topic/core-loop
references/game-craft.md|design|Game Craft - Input, Camera, AI, Procgen, Saves|type/guide topic/design topic/game-feel topic/camera
references/case-studies-teardowns.md|design|Case Studies and Teardowns|type/research topic/design topic/case-study
references/accessibility-and-player-qol.md|design|Accessibility and Player QoL|type/guide topic/accessibility topic/ui
references/genre-playbooks.md|genres|Genre Playbooks - Index|type/guide topic/genre
references/genres/fashion-dress-up.md|genres|Genre - Fashion and Dress-Up|type/genre topic/genre
references/genres/fighting-battlegrounds.md|genres|Genre - Fighting and Battlegrounds|type/genre topic/genre
references/genres/fishing.md|genres|Genre - Fishing|type/genre topic/genre
references/genres/horror-coop-escape.md|genres|Genre - Horror and Co-op Escape|type/genre topic/genre
references/genres/obby-tower.md|genres|Genre - Obby and Tower|type/genre topic/genre
references/genres/party-minigames.md|genres|Genre - Party and Minigames|type/genre topic/genre
references/genres/pet-collection-hatching.md|genres|Genre - Pet Collection and Hatching|type/genre topic/genre
references/genres/physics-sandbox.md|genres|Genre - Physics Sandbox|type/genre topic/genre
references/genres/plus-one-evolution.md|genres|Genre - Plus One and Evolution|type/genre topic/genre
references/genres/racing-driving.md|genres|Genre - Racing and Driving|type/genre topic/genre
references/genres/rng-rolling.md|genres|Genre - RNG and Aura Rolling|type/genre topic/genre
references/genres/rpg-dungeon.md|genres|Genre - RPG, Dungeon and Roguelite|type/genre topic/genre
references/genres/shooter-pvp.md|genres|Genre - Shooter and PvP|type/genre topic/genre
references/genres/simulator-incremental.md|genres|Genre - Simulator and Incremental|type/genre topic/genre
references/genres/social-deduction.md|genres|Genre - Social Deduction|type/genre topic/genre
references/genres/social-roleplay.md|genres|Genre - Social Roleplay|type/genre topic/genre
references/genres/sports.md|genres|Genre - Sports|type/genre topic/genre
references/genres/steal-and-defend.md|genres|Genre - Steal and Defend|type/genre topic/genre
references/genres/survival-crafting.md|genres|Genre - Survival and Crafting|type/genre topic/genre
references/genres/tower-defense.md|genres|Genre - Tower Defense|type/genre topic/genre
references/genres/tycoon-and-cozy-management.md|genres|Genre - Tycoon and Cozy Management|type/genre topic/genre
references/market-scan-2026-11.md|market|Market Scan - Nov 2026|type/research topic/market
references/market-research-v2-raw.md|market|Market Research v2 - Nov 2026 (Raw)|type/research topic/market
references/ui-design-figma.md|ui|UI Design and Figma Hand-off|type/guide topic/ui topic/figma
references/ui-screen-recipes.md|ui|UI Screen Recipes|type/guide topic/ui
references/ui-motion-and-feedback.md|ui|UI Motion and Feedback|type/guide topic/ui topic/game-feel
references/ui-input-crossplatform.md|ui|UI Input and Cross-Platform|type/guide topic/ui topic/input topic/mobile
references/vfx-and-juice.md|vfx|VFX and Juice|type/guide topic/vfx topic/game-feel
references/vfx-recipes.md|vfx|VFX Recipes|type/guide topic/vfx
references/audio-sfx-music.md|vfx|Audio - SFX, Music and Mixing|type/guide topic/audio
references/art-direction-and-quality-bar.md|art|Art Direction and the Quality Bar|type/guide topic/art
references/level-design-worldbuilding.md|art|Level Design and Worldbuilding|type/guide topic/level-design
references/lighting-and-atmosphere.md|art|Lighting and Atmosphere|type/guide topic/lighting
references/art-pipeline-blender.md|models|Blender to Roblox Art Pipeline|type/guide topic/blender topic/art
references/blender-modeling-craft.md|models|Blender Modelling Craft|type/guide topic/blender
references/animation-and-rigs.md|models|Animation and Rigs|type/guide topic/animation topic/blender
references/cutscenes-and-cinematics.md|cine|Cutscenes and Cinematics|type/guide topic/cinematics topic/camera
references/cutscenes-and-cinematics-runner.md|cine|Cutscene Timeline Runner (Code)|type/code topic/cinematics topic/luau
references/luau-mastery.md|eng|Luau Mastery|type/guide topic/luau
references/architecture-patterns-luau.md|eng|Game Programming Patterns in Luau|type/guide topic/luau topic/architecture
references/engineering-architecture.md|eng|Engineering Architecture and Luau Standards|type/guide topic/architecture topic/luau
references/gameplay-systems-cookbook.md|eng|Gameplay Systems Cookbook|type/guide topic/systems topic/luau
references/physics-and-vehicles.md|eng|Physics and Vehicles|type/guide topic/physics
references/debugging-and-testing.md|eng|Debugging and Testing|type/guide topic/debugging
references/performance.md|eng|Performance and Optimization|type/guide topic/performance topic/mobile
references/networking-and-security.md|sec|Networking and Security|type/guide topic/security topic/networking
references/data-and-purchases.md|sec|Data, Purchases and Teleports|type/guide topic/data topic/purchases
references/monetization-and-policy.md|money|Monetization and Policy|type/guide topic/monetization topic/policy
references/economy-and-progression.md|money|Economy and Progression|type/guide topic/economy topic/progression
references/liveops-quests-retention.md|ret|LiveOps, Quests and Retention|type/guide topic/retention topic/liveops
references/tutorial-and-onboarding.md|ret|Tutorials and Onboarding|type/guide topic/onboarding topic/retention
references/growth-and-marketing.md|growth|Growth and Marketing|type/guide topic/growth
references/analytics-and-discovery.md|growth|Analytics and Discovery|type/guide topic/analytics topic/discovery
references/icons-thumbnails-and-store-page.md|growth|Icons, Thumbnails and Store Page|type/guide topic/store-page topic/art
references/team-business-legal.md|biz|Team, Business and Legal|type/guide topic/business topic/legal
references/community-moderation-safety.md|biz|Community, Moderation and Safety|type/guide topic/community topic/safety
references/visual-library/animation.md|lib|Library - Animation|type/visual-library topic/animation
references/visual-library/audio-and-sound.md|lib|Library - Audio and Sound|type/visual-library topic/audio
references/visual-library/cutscenes-and-cameras.md|lib|Library - Cutscenes and Cameras|type/visual-library topic/cinematics
references/visual-library/environments-and-maps.md|lib|Library - Environments and Maps|type/visual-library topic/level-design
references/visual-library/icons-and-thumbnails.md|lib|Library - Icons and Thumbnails|type/visual-library topic/store-page
references/visual-library/lighting-and-mood.md|lib|Library - Lighting and Mood|type/visual-library topic/lighting
references/visual-library/models-props-characters.md|lib|Library - Models, Props and Characters|type/visual-library topic/art topic/blender
references/visual-library/reference-sheets.md|lib|Library - Reference Sheets|type/visual-library type/reference-sheet
references/visual-library/tutorials-and-onboarding.md|lib|Library - Tutorials and Onboarding|type/visual-library topic/onboarding
references/visual-library/ui-components-and-style.md|lib|Library - UI Components and Style|type/visual-library topic/ui
references/visual-library/ui-hud.md|lib|Library - UI HUD|type/visual-library topic/ui
references/visual-library/ui-screens.md|lib|Library - UI Screens|type/visual-library topic/ui
references/visual-library/vfx-learning.md|lib|Library - VFX Learning|type/visual-library topic/vfx
references/visual-library/vfx.md|lib|Library - VFX|type/visual-library topic/vfx
SKILL.md|skills|Skill - Main (roblox-game-design)|type/skill topic/process
skills/cinematics/SKILL.md|skills|Skill - Cinematics|type/skill topic/cinematics
skills/debug/SKILL.md|skills|Skill - Debug|type/skill topic/debugging
skills/growth/SKILL.md|skills|Skill - Growth|type/skill topic/growth
skills/level-up/SKILL.md|skills|Skill - Level Up|type/skill topic/audit
skills/models-and-animation/SKILL.md|skills|Skill - Models and Animation|type/skill topic/blender topic/animation
skills/monetization/SKILL.md|skills|Skill - Monetization|type/skill topic/monetization topic/economy
skills/performance/SKILL.md|skills|Skill - Performance|type/skill topic/performance
skills/retention/SKILL.md|skills|Skill - Retention|type/skill topic/retention topic/core-loop
skills/security-data/SKILL.md|skills|Skill - Security and Data|type/skill topic/security topic/data
skills/systems/SKILL.md|skills|Skill - Systems|type/skill topic/systems topic/luau
skills/ui/SKILL.md|skills|Skill - UI|type/skill topic/ui
skills/vfx-and-audio/SKILL.md|skills|Skill - VFX and Audio|type/skill topic/vfx topic/audio
skills/world-and-lighting/SKILL.md|skills|Skill - World and Lighting|type/skill topic/art topic/lighting topic/level-design
templates/analytics-event-plan.md|tpl|Template - Analytics Event Plan|type/template topic/analytics
templates/economy-balance-sheet.md|tpl|Template - Economy Balance Sheet|type/template topic/economy
templates/game-audit-report.md|tpl|Template - Game Audit Report|type/template topic/audit
templates/game-one-pager.md|tpl|Template - Game One-Pager|type/template topic/design
templates/launch-checklist.md|tpl|Template - Launch Checklist|type/template topic/growth
templates/lean-gdd.md|tpl|Template - Lean GDD|type/template topic/design
templates/monetization-product-plan.md|tpl|Template - Monetization Product Plan|type/template topic/monetization
templates/playtest-plan.md|tpl|Template - Playtest Plan|type/template topic/playtesting
scripts/README.md|scripts|Scripts and Tools - Overview|type/meta topic/tools
assets/reference/ATTRIBUTION.md|sheets|Reference Sheets - Attribution|type/meta type/reference-sheet
CREDITS.md|meta|Sources and Credits|type/meta
README.md|meta|About the Skill (Repo README)|type/meta
"""

SAFE_HEADING = re.compile(r"^[\w\s.,()'&+\-\u2013\u2014]+$")
FENCE = re.compile(r"^\s*(```|~~~)")


def fold(s):
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r'[\\/:*?"<>|#^\[\]`]', "", s)
    return re.sub(r"\s+", " ", s).strip(" .")


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = {}
            for line in text[4:end].splitlines():
                m = re.match(r"^([\w-]+):\s*(.*)$", line)
                if m:
                    v = m.group(2).strip()
                    if v.startswith('"') and v.endswith('"'):
                        try:
                            v = json.loads(v)
                        except Exception:
                            v = v[1:-1]
                    fm[m.group(1)] = v
            return fm, text[end + 5:]
    return {}, text


def headings_of(body):
    out, fence = [], False
    for line in body.splitlines():
        if FENCE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2)))
    return out


def plain(s):
    s = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\\?\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"[`*_]", "", s).strip()


def summary_of(body):
    fence = False
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b or FENCE.match(b) or b.startswith("> [!"):
            continue
        if b.startswith(("#", "|", "<", "---", "![")):
            # a heading block may carry text on the following lines
            lines = [l for l in b.splitlines() if not l.startswith(("#", "|"))]
            if not lines or lines[0].startswith(("|", "<", "---")):
                continue
            b = "\n".join(lines)
        b = plain(" ".join(l.strip().lstrip("-> ").strip() for l in b.splitlines()))
        if len(b) < 40:
            continue
        sents = re.split(r"(?<=[.!?])\s+", b)
        out = ""
        for s in sents:
            if len(out) + len(s) > 330 and out:
                break
            out = (out + " " + s).strip()
        return out[:400]
    return ""


# ---------------------------------------------------------------- registry
notes = {}      # name -> dict
by_src = {}     # repo-relative src -> name


def add_note(name, folder_key, tags, body, src=None, extra=None, subdir=None, convert=True):
    assert name not in notes, name
    folder = FOLDERS[folder_key] + (("/" + subdir) if subdir else "")
    notes[name] = dict(name=name, folder=folder, folder_key=folder_key, tags=tags, body=body,
                       src=src, extra=extra or {}, convert=convert)
    if src:
        by_src[src] = name


for row in TABLE.strip().splitlines():
    src, fk, name, tags = row.split("|")
    text = (REPO / src).read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    extra = {}
    if fm:
        extra = {"skill_name": fm.get("name", ""), "description": fm.get("description", ""),
                 "argument_hint": fm.get("argument-hint", "")}
    add_note(name, fk, tags.split(), body, src=src, extra=extra)

# ---- knowledge base: split by H1 part and H2 section (fence-aware)
kb_text = (REPO / "references/knowledge-base.md").read_text(encoding="utf-8")
kb_lines = kb_text.splitlines()
parts, cur_part, cur_sec, fence = [], None, None, False
preamble = []
part_names = {"0": "Part 0 - Overview"}
cur_part = "0"
sections = []  # (part_folder, h2_text, lines)
part_intro = {}
for line in kb_lines:
    if FENCE.match(line):
        fence = not fence
    if not fence and line.startswith("# ") and not line.startswith("# Roblox Game Design Knowledge Base"):
        m = re.match(r"^# (\d+)\.\s*(.*)$", line)
        if m:
            cur_part = m.group(1)
            part_names[cur_part] = {
                "1": "Part 1 - Design Foundations, Psychology and Process",
                "2": "Part 2 - Game Craft, Genres and Architecture Patterns",
                "3": "Part 3 - Roblox Design, Monetization, LiveOps and Discovery",
                "4": "Part 4 - Engineering, Networking, Security and Data",
                "5": "Part 5 - Performance, World, Art Pipeline, UI and Cross-Platform",
            }.get(m.group(1)) or fold(f"Part {m.group(1)} - {m.group(2)}")[:70]
            part_intro[cur_part] = [line]
            cur_sec = None
            continue
    if not fence and line.startswith("## "):
        cur_sec = [cur_part, line[3:].strip(), part_intro.pop(cur_part, []) + ([""] if cur_part in part_intro else []) + [line]]
        sections.append(cur_sec)
        continue
    if cur_sec is None:
        if cur_part in part_intro:
            part_intro[cur_part].append(line)
        else:
            preamble.append(line)
    else:
        cur_sec[2].append(line)

kb_index_name = "Knowledge Base Archive - Index"
kb_sec_by_num = {}
kb_entries = []
ARCHIVE_NOTE = ("> [!warning] Archive\n> Original source text from the knowledge base. Where it differs from a guide "
                "in folders 01-15, the guide is right. Check anything you take from here.\n")
for i, (pk, h2, lines) in enumerate(sections, 1):
    nm = fold(f"KB {i:02d} - {h2}")[:90].rstrip(" -,")
    num = re.match(r"^(\d+\.\d+)\b", h2)
    if num:
        kb_sec_by_num[num.group(1)] = nm
    body = "\n".join(lines).strip() + "\n"
    add_note(nm, "kb", ["type/archive", "topic/knowledge-base"], ARCHIVE_NOTE + "\n" + body,
             extra={"kb_part": part_names[pk], "kb_h2": h2}, subdir=part_names[pk])
    notes[nm]["src"] = f"references/knowledge-base.md#{h2}"
    kb_entries.append((part_names[pk], nm, h2))

idx_body = "\n".join(preamble).strip() + "\n\n## Sections\n\n"
last = None
for pk, nm, h2 in kb_entries:
    if pk != last:
        idx_body += f"\n### {pk}\n\n"
        last = pk
    idx_body += f"- [[{nm}]]\n"
add_note(kb_index_name, "kb", ["type/archive", "type/index", "topic/knowledge-base"], idx_body,
         src="references/knowledge-base.md")

# ---------------------------------------------------------------- lookup tables
lookup = {}
basename_count = {}
for src in by_src:
    b = src.split("/")[-1]
    basename_count[b] = basename_count.get(b, 0) + 1
for src, nm in by_src.items():
    lookup[src] = nm
    if src.startswith("references/"):
        lookup[src[len("references/"):]] = nm
    b = src.split("/")[-1]
    if basename_count[b] == 1:
        lookup[b] = nm
lookup["SKILL.md"] = by_src["SKILL.md"]
lookup["INDEX.md"] = by_src["references/INDEX.md"]
lookup["README.md"] = by_src["README.md"]
lookup["knowledge-base.md"] = kb_index_name

images = sorted(p.name for p in (REPO / "assets/reference").glob("*.png"))
img_lookup = {}
for im in images:
    img_lookup[im] = im
    img_lookup["assets/reference/" + im] = im

note_headings = {}
for nm, n in notes.items():
    note_headings[nm] = headings_of(n["body"])


def section_target(nm, sec):
    """Heading text in note nm for section number or name sec, if linkable."""
    for _, h in note_headings.get(nm, []):
        if re.match(rf"^{re.escape(sec)}(\.|\s)", h) or h == sec:
            return h if SAFE_HEADING.match(h) else None
    return None


def norm_token(tok):
    t = tok.strip()
    t = re.sub(r"^\$\{CLAUDE_PLUGIN_ROOT\}/", "", t)
    t = re.sub(r"^(\./|\.\./)+", "", t)
    return t.split("#")[0]


img_uses = {im: set() for im in images}
links_out = {nm: set() for nm in notes}
unresolved = {}


def link_for(target_nm, rest, current):
    """Return (wikilink, consumed_chars_from_rest)."""
    links_out[current].add(target_nm)
    # knowledge base section number
    if target_nm == kb_index_name:
        m = re.match(r"^\s?§\s?(\d+\.\d+)", rest)
        if m and m.group(1) in kb_sec_by_num:
            t = kb_sec_by_num[m.group(1)]
            links_out[current].add(t)
            return f"[[{t}]]", m.end()
        return f"[[{target_nm}]]", 0
    m = re.match(r"^\s?§\s?(\d+(?:\.\d+)*)(?![\d\u2013-]|\.\d)", rest)
    if m:
        h = section_target(target_nm, m.group(1))
        if h:
            return f"[[{target_nm}#{h}]]", m.end()
        return f"[[{target_nm}]]", 0
    m = re.match(r"^\s?§\s?([A-Z][^,;:)\]|.]*)", rest)
    if m:
        cand = m.group(1).rstrip()
        best = None
        for _, h in note_headings.get(target_nm, []):
            if cand.startswith(h) and (best is None or len(h) > len(best)) and SAFE_HEADING.match(h):
                after = cand[len(h):len(h) + 1]
                if not after or not after.isalnum():
                    best = h
        if best:
            pre = rest[: m.start(1)]
            return f"[[{target_nm}#{best}]]", len(pre) + len(best)
    return f"[[{target_nm}]]", 0


TICK = re.compile(r"`([^`\n]+)`")
BARE = re.compile(r"(?<![\w/`\[])((?:\$\{CLAUDE_PLUGIN_ROOT\}/)?(?:references|templates|skills)/[\w./-]*?\.md)")


def expand_prefixes(line, prefixes):
    if not prefixes:
        return line

    def rep(m):
        tok = m.group(1)
        for p, url in prefixes:
            if p == "t" and re.match(r"^t/\d+", tok):
                return f"[{tok}]({url.replace('<id>', tok[2:])})"
            if tok.startswith(p + "/"):
                full = url.rstrip("/") + tok[len(p):]
                full = full.split(" ")[0]
                return f"[{tok}]({full})"
        return m.group(0)
    return TICK.sub(rep, line)


def convert_body(nm, body):
    prefixes = []
    if notes[nm]["folder_key"] == "lib":
        for m in re.finditer(r"`([A-Za-z]+|t/<id>)` = `(https?://[^`]+)`", body):
            p = "t" if m.group(1) == "t/<id>" else m.group(1)
            prefixes.append((p, m.group(2)))
    out, fence = [], False
    for line in body.splitlines():
        if FENCE.match(line):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue
        if prefixes and not re.search(r"` = `https?://", line):
            line = expand_prefixes(line, prefixes)
        res, pos = [], 0
        for m in TICK.finditer(line):
            if m.start() < pos:
                continue
            tok = norm_token(m.group(1))
            target = lookup.get(tok)
            if target is None and tok.endswith(".md") and "/" in tok and lookup.get(tok.split("/")[-1]) and basename_count.get(tok.split("/")[-1]) == 1 and tok.split("/")[0] in ("references", "visual-library", "genres", "templates"):
                target = lookup.get(tok.split("/")[-1])
            img = img_lookup.get(tok) or img_lookup.get(tok.split("/")[-1]) if tok.endswith(".png") and "*" not in tok else None
            if target:
                link, used = link_for(target, line[m.end():], nm)
                res.append(line[pos:m.start()] + link)
                pos = m.end() + used
            elif img and img in img_uses:
                img_uses[img].add(nm)
                res.append(line[pos:m.start()] + f"[[{img}]]")
                pos = m.end()
            else:
                if tok.endswith(".md") and not tok.startswith(("http", "LihFolk", "32 Case")):
                    unresolved[tok] = unresolved.get(tok, 0) + 1
        res.append(line[pos:])
        line = "".join(res)
        # bare (un-ticked) repo paths outside existing links and inline code
        segs = re.split(r"(`[^`\n]*`|\[\[[^\]]*\]\]|\]\([^)]*\))", line)
        for i in range(0, len(segs), 2):
            def bare(m):
                tok = norm_token(m.group(1))
                t = lookup.get(tok)
                if t:
                    links_out[nm].add(t)
                    return f"[[{t}]]"
                unresolved[tok] = unresolved.get(tok, 0) + 1
                return m.group(0)
            segs[i] = BARE.sub(bare, segs[i])
        out.append("".join(segs))
    return "\n".join(out) + ("\n" if not body.endswith("\n") else "")


for nm, n in notes.items():
    if n["convert"]:
        n["body"] = convert_body(nm, n["body"])
        links_out[nm].discard(nm)

# ---------------------------------------------------------------- generated notes


def esc_cell(s):
    return s.replace("|", "\\|").replace("\n", " ")


def summary_for(nm):
    n = notes[nm]
    if n["extra"].get("description"):
        d = n["extra"]["description"]
        return d.split(" Use when")[0].strip() if " Use when" in d else d[:300]
    return summary_of(n["body"])


# Skills overview + per-skill "at a glance" callout
skill_names = [nm for nm in notes if nm.startswith("Skill - ")]
for nm in skill_names:
    n = notes[nm]
    desc = n["extra"].get("description", "")
    reads = sorted(t for t in links_out[nm] if not t.startswith(("Skill - ", "KB ")))
    glance = ["> [!abstract] At a glance",
              f"> **Skill id:** `{n['extra'].get('skill_name','')}`" + (f" · **Argument:** `{n['extra']['argument_hint']}`" if n['extra'].get('argument_hint') else ""),
              f"> **Use when:** {desc}",
              "> **How to use it:** follow \"How to work\" (or \"Pick the mode first\" in the main skill), then the \"Fast routes\" row for the task. Read only the listed sections.",
              "> **Notes it reads:** " + ", ".join(f"[[{t}]]" for t in reads),
              ""]
    body = n["body"]
    m = re.search(r"^# .*$", body, re.M)
    if m:
        body = body[: m.end()] + "\n\n" + "\n".join(glance) + body[m.end():]
    else:
        body = "\n".join(glance) + "\n" + body
    n["body"] = body

sk_rows = ["| Skill | What it does | Use when the user says | Key notes |", "|---|---|---|---|"]
for nm in sorted(skill_names, key=lambda x: (not x.startswith("Skill - Main"), x)):
    d = notes[nm]["extra"].get("description", "")
    what = d.split(" Use when")[0] if " Use when" in d else d.split(". ")[0]
    when = d.split(" Use when", 1)[1].split(". ")[0] if " Use when" in d else ""
    when = re.sub(r"^ the user says ", "", when).strip()
    key = sorted(t for t in links_out[nm] if not t.startswith(("Skill - ", "KB ", "Library - ", "Template - ")))[:6]
    sk_rows.append(f"| [[{nm}]] | {esc_cell(what)} | {esc_cell(when)} | " + ", ".join(f"[[{k}]]" for k in key).replace("|", "\\|") + " |")
skills_overview = f"""# Skills Overview

The agent skills that power this playbook, turned into notes you can read and follow. Each skill note starts with an "At a glance" box: when to use it, how to run it and which notes it reads.

**How an agent uses a skill from this vault**
1. Match the request to a row below (trigger phrases are in each skill's "Use when").
2. Open the skill note and follow its "How to work" loop: look first, diagnose against the guide's symptom → cause → fix table, recommend, implement, verify.
3. Use its "Fast routes" table: read exactly the sections listed, not whole guides.
4. Check the work against the review gate of the guide used, and against [[House Rules]].

If nothing matches, use [[Skill - Main (roblox-game-design)]] or the [[Task Router]].

{chr(10).join(sk_rows)}
"""
add_note("Skills Overview", "skills", ["type/index", "type/skill"], skills_overview, convert=False)

# House rules (verbatim section of SKILL.md)
skill_md = (REPO / "SKILL.md").read_text(encoding="utf-8")
hr = re.search(r"^## House rules.*?(?=^## )", skill_md, re.S | re.M).group(0).rstrip()
add_note("House Rules", "start", ["type/rules", "topic/rules"],
         "# House Rules\n\nCopied verbatim from the main skill ([[Skill - Main (roblox-game-design)]]). "
         "These override all generic advice anywhere in this vault.\n\n" + hr + "\n", convert=False)

# Gallery of reference sheets
gal = ["# Reference Sheets Gallery", "",
       "The 22 original reference sheets drawn for the skill. Each sheet prints the guide and section its numbers come from. "
       "Descriptions and the 30 linked official-docs images are in [[Library - Reference Sheets]]; licensing in [[Reference Sheets - Attribution]]. "
       "HTML sources are in `src/` (rebuild with `node src/render.js`).", ""]
for im in images:
    title = fold(im[:-4].replace("-", " ")).capitalize()
    title = re.sub(r"^(\d+) ", r"\1 - ", title)
    used = sorted(img_uses[im])
    gal += [f"## {title}", "", f"![[{im}]]", "",
            "Used by: " + (", ".join(f"[[{u}]]" for u in used) if used else "—"), ""]
add_note("Reference Sheets Gallery", "sheets", ["type/reference-sheet", "type/index"], "\n".join(gal), convert=False)

# Agent tutorial generated from the workflow phase table
wp = notes[by_src["references/workflow-phases.md"]]["body"]
phase_skill = {
    "1": ["Skill - Main (roblox-game-design)"], "2": ["Skill - Main (roblox-game-design)", "Skill - World and Lighting"],
    "3": ["Skill - Retention", "Skill - Monetization"], "4": ["Skill - Systems", "Skill - Security and Data"],
    "5": ["Skill - Systems", "Skill - Security and Data", "Skill - Models and Animation"],
    "6": ["Skill - UI", "Skill - VFX and Audio", "Skill - World and Lighting", "Skill - Cinematics"],
    "7": ["Skill - Models and Animation", "Skill - World and Lighting"], "8": ["Skill - Monetization"],
    "9": ["Skill - Growth", "Skill - Retention"], "10": ["Skill - Performance"], "11": ["Skill - Growth"],
    "12": ["Skill - Retention", "Skill - Level Up"],
}
steps = []
for line in wp.splitlines():
    m = re.match(r"^\|\s*(\d+)\.\s*([^|]+)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$", line.replace("\\|", "¦"))
    if m:
        num, ttl, outp, opn, gate = (x.strip().replace("¦", "|") for x in m.groups())
        steps.append(f"### Step {num}. {ttl}\n\n- **Make:** {outp}\n- **Read:** {opn}\n- **Gate (must pass before the next step):** {gate}\n"
                     f"- **Skill to load:** " + ", ".join(f"[[{s}]]" for s in phase_skill.get(num, [])) + "\n")
tutorial = f"""# How to Build a Great Roblox Game (Agent Tutorial)

The route through this vault from an empty idea to a live, growing game. Follow it in order. Every step says what to make, which notes to read, which skill to load and the gate that must pass before moving on. The source of the steps is [[Workflow Phases - Idea to Live]].

## 0. Before anything else

1. Read [[House Rules]]. They override every other note.
2. Pick the mode (from [[Skill - Main (roblox-game-design)]]):
   - **New game** → the twelve steps below. A beginner's *first* game starts at [[Learning Paths]] instead: the goal is to finish something small.
   - **An existing game should get better** → [[Audit an Existing Game]] with [[Skill - Level Up]]; write the result in [[Template - Game Audit Report]].
   - **One system, bug or question** → the matching row in [[Task Router]] or a skill in [[Skills Overview]].
3. Pitch the depth to the developer's level: [[Learning Paths]].
4. Unknown word? [[Glossary]].

Design before build: before gameplay code exists, the fantasy, three pillars, the loops, the first-minute script, an economy model with numbers and an art direction exist and have passed their rubrics.

## The twelve steps

{chr(10).join(steps)}
For a small request (one system, one bug, one tweak), jump to the matching step but still check that step's gate before calling it done.

## Make it look designed, not generic

- Start from references, not memory: pick three to five rows from the [[16 Visual Library]] notes for the genre and tone, look at them, and write down what to take from each (layout, hierarchy, palette, timing, shape). Borrow principles from several; never reproduce one.
- Use the diagrams in [[Reference Sheets Gallery]] for sizes, spacing, timing and layout rules.
- Hold every screen, effect and model to [[Art Direction and the Quality Bar]].

## Before you call anything done

- The review gate at the end of the guide you used.
- The ship gates in [[Checklists and Ship Gates]] and the never-do list in [[Decision Rules and Never-Do List]].
- Platform facts (APIs, fees, policies) change: check them at https://create.roblox.com/docs before relying on them.

## Learn from what already works

- Genre numbers and loops: [[Genre Playbooks - Index]] and the 21 notes in folder 03.
- What hits did and what killed the rest: [[Case Studies and Teardowns]].
- What to build now: [[Market Scan - Nov 2026]] and [[Market Research v2 - Nov 2026 (Raw)]].
- Deep background (archive): [[Knowledge Base Archive - Index]].
"""
tutorial = tutorial.replace("[[16 Visual Library]]", "Visual Library (folder 16, e.g. [[Library - UI HUD]], [[Library - VFX]])")
add_note("How to Build a Great Roblox Game", "start", ["type/tutorial", "type/index", "topic/process"], tutorial, convert=False)

_sh_fm, _sh_body = split_frontmatter((Path(__file__).resolve().parent / "Start Here.md").read_text(encoding="utf-8"))
add_note("Start Here", "start", ["type/index"], _sh_body, convert=False)

# ---------------------------------------------------------------- write notes
if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True)


def yq(s):
    return json.dumps(s, ensure_ascii=False)


index_entries = []
for nm, n in notes.items():
    summ = summary_for(nm)
    n["summary"] = summ
    aliases = []
    if n["src"] and "#" not in n["src"]:
        aliases += [n["src"], Path(n["src"]).stem if Path(n["src"]).name != "SKILL.md" else (n["extra"].get("skill_name") or "")]
    h1 = next((h for lvl, h in headings_of(n["body"]) if lvl == 1), "")
    if n["extra"].get("kb_h2"):
        h1 = n["extra"]["kb_h2"]
        num = re.match(r"^(\d+\.\d+)\b", h1)
        if num:
            aliases.append(f"knowledge-base.md §{num.group(1)}")
    if h1 and h1 != nm:
        aliases.append(plain(h1))
    aliases = [a for a in dict.fromkeys(aliases) if a]
    fm = ["---", f"title: {yq(nm)}", f"aliases: {yq(aliases)}", f"tags: {yq(n['tags'])}",
          f"folder: {yq(n['folder'])}", f"summary: {yq(summ)}"]
    if n["src"]:
        fm.append(f"source: {yq(n['src'])}")
    if n["extra"].get("kb_part"):
        fm.append(f"kb_part: {yq(n['extra']['kb_part'])}")
    fm.append(f"built: {BUILT}")
    fm.append("---\n")
    path = ROOT / n["folder"] / f"{nm}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(fm) + "\n" + n["body"].lstrip("\n"), encoding="utf-8")
    n["path"] = path.relative_to(ROOT).as_posix()

# assets
img_dir = ROOT / FOLDERS["sheets"] / "images"
img_dir.mkdir(parents=True, exist_ok=True)
for im in images:
    shutil.copy2(REPO / "assets/reference" / im, img_dir / im)
shutil.copytree(REPO / "assets/reference/src", ROOT / FOLDERS["sheets"] / "src")
for sub in ("blender", "studio", "images"):
    shutil.copytree(REPO / "scripts" / sub, ROOT / FOLDERS["scripts"] / sub)

# ---------------------------------------------------------------- vault map, path map, index json
vm = ["# Vault Map", "", "Every note in the playbook, by folder, with one line on what it is for. "
      "Agents: the same data is in `99 Meta/vault-index.json` (with headings, tags and links) and searchable with `99 Meta/search_vault.py`.", ""]
for fk, folder in FOLDERS.items():
    members = sorted((nm for nm, n in notes.items() if n["folder_key"] == fk and nm != "Vault Map"),
                     key=lambda x: notes[x]["folder"] + "/" + x)
    vm += [f"## {folder}", "", FOLDER_ABOUT[fk], ""]
    if fk == "kb":
        vm += [f"- [[{kb_index_name}]]: {len(kb_entries)} archive sections in {len(part_names)} parts.", ""]
        continue
    vm += ["| Note | What it is for |", "|---|---|"]
    for nm in members:
        vm.append(f"| [[{nm}]] | {esc_cell(notes[nm]['summary'][:220])} |")
    if fk == "sheets":
        vm.append(f"| `images/` | {len(images)} PNG sheets, embedded in [[Reference Sheets Gallery]] |")
    if fk == "scripts":
        vm.append("| `blender/`, `studio/`, `images/` | The script files themselves |")
    vm.append("")
tags_all = sorted({t for n in notes.values() for t in n["tags"]})
vm += ["## Tags", "", "Search by tag in Obsidian (`tag:#topic/ui`) or grep the front matter (`topic/ui`).", "",
       ", ".join(f"`{t}`" for t in tags_all), ""]
vm_path = ROOT / FOLDERS["start"] / "Vault Map.md"
vm_fm = ["---", 'title: "Vault Map"', 'aliases: ["MOC", "Map of Content", "index"]', 'tags: ["type/index"]',
         f'folder: "{FOLDERS["start"]}"', 'summary: "Every note in the playbook by folder, with what each is for."', f"built: {BUILT}", "---", ""]
vm_path.write_text("\n".join(vm_fm + vm), encoding="utf-8")

pm = ["# Path Map", "", "Notes often mention paths from the original skill repository (for example `references/ui-design-figma.md`, "
      "`${CLAUDE_PLUGIN_ROOT}/references/...`, `assets/reference/NN-*.png`, `scripts/blender/...`). This table maps each one to its note in this vault.", "",
      "| Repo path | Vault note |", "|---|---|"]
for src, nm in sorted(by_src.items()):
    pm.append(f"| `{src}` | [[{nm}]] |")
pm += ["| `assets/reference/*.png` | `17 Reference Sheets/images/` (see [[Reference Sheets Gallery]]) |",
       "| `assets/reference/src/` | `17 Reference Sheets/src/` |",
       "| `scripts/blender/`, `scripts/studio/`, `scripts/images/` | `20 Scripts and Tools/blender/`, `.../studio/`, `.../images/` |",
       "| `references/knowledge-base.md` §N.N | the note `KB xx - N.N ...` in `90 Archive - Knowledge Base/` |", ""]
(ROOT / FOLDERS["meta"] / "Path Map.md").write_text(
    "---\ntitle: \"Path Map\"\ntags: [\"type/meta\", \"type/index\"]\nsummary: \"Original repo paths mapped to vault notes.\"\n"
    f"built: {BUILT}\n---\n\n" + "\n".join(pm), encoding="utf-8")

index = {"vault": "Roblox Game Dev Playbook", "built": BUILT,
         "how_to_search": "Match the query against title, aliases, tags, summary and headings; open 'path' (relative to the playbook folder) and read only the heading you need.",
         "folders": {FOLDERS[k]: FOLDER_ABOUT[k] for k in FOLDERS}, "notes": [], "images": []}
for nm, n in sorted(notes.items(), key=lambda kv: kv[1]["path"]):
    text = (ROOT / n["path"]).read_text(encoding="utf-8")
    index["notes"].append({
        "title": nm, "path": n["path"], "folder": n["folder"], "tags": n["tags"],
        "aliases": json.loads(re.search(r"^aliases: (.*)$", text, re.M).group(1)) if re.search(r"^aliases: ", text, re.M) else [],
        "summary": n["summary"], "triggers": n["extra"].get("description", ""), "source": n["src"] or "",
        "headings": [h for lvl, h in headings_of(n["body"]) if lvl in (2, 3)][:80],
        "links_to": sorted(links_out.get(nm, [])), "lines": text.count("\n") + 1})
for p in ("Vault Map", "Path Map"):
    pass
index["notes"].append({"title": "Vault Map", "path": f"{FOLDERS['start']}/Vault Map.md", "folder": FOLDERS["start"],
                       "tags": ["type/index"], "aliases": ["MOC"], "summary": "Every note by folder with what it is for.",
                       "source": "", "headings": [], "links_to": [], "lines": len(vm)})
index["notes"].append({"title": "Path Map", "path": f"{FOLDERS['meta']}/Path Map.md", "folder": FOLDERS["meta"],
                       "tags": ["type/meta"], "aliases": [], "summary": "Original repo paths mapped to vault notes.",
                       "source": "", "headings": [], "links_to": [], "lines": len(pm)})
index["notes"].append({"title": "AGENTS", "path": "AGENTS.md", "folder": "", "tags": ["type/index", "type/meta"],
                       "aliases": ["Agent guide", "How to search this vault"],
                       "summary": "How an AI agent finds, reads and applies the notes in this playbook. Read first.",
                       "source": "", "headings": ["1. Find the right note (in this order)", "2. Read efficiently",
                       "3. Rules that apply to every task", "4. Folders", "5. Tags", "6. Keeping it current"],
                       "links_to": [], "lines": 80})
for im in images:
    index["images"].append({"file": f"{FOLDERS['sheets']}/images/{im}", "title": fold(im[:-4].replace('-', ' ')),
                            "used_by": sorted(img_uses[im]), "source_html": f"{FOLDERS['sheets']}/src/{im[:-4]}.html"})
(ROOT / FOLDERS["meta"] / "vault-index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")

shutil.copy2(Path(__file__).resolve(), ROOT / FOLDERS["meta"] / "build_vault.py")
for extra in ("search_vault.py", "AGENTS.md", "CLAUDE.md"):
    p = Path(__file__).resolve().parent / extra
    if p.exists():
        dest = ROOT / (FOLDERS["meta"] if extra.endswith(".py") else (FOLDERS["start"] if extra == "Start Here.md" else ""))
        shutil.copy2(p, dest / extra)

# ---------------------------------------------------------------- link check
all_md = {p.stem: p for p in ROOT.rglob("*.md")}
all_files = {p.name for p in ROOT.rglob("*") if p.is_file()}
heads_cache = {}
bad = []
for p in ROOT.rglob("*.md"):
    fence = False
    for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        for m in re.finditer(r"!?\[\[([^\]]+)\]\]", re.sub(r"`[^`]*`", "", line)):
            tgt = re.split(r"\\?\|", m.group(1))[0]
            name, _, head = tgt.partition("#")
            if name in all_files:
                continue
            if name not in all_md:
                bad.append((p.relative_to(ROOT).as_posix(), ln, m.group(0)))
                continue
            if head:
                if name not in heads_cache:
                    heads_cache[name] = {h for _, h in headings_of(all_md[name].read_text(encoding="utf-8"))}
                if head not in heads_cache[name]:
                    bad.append((p.relative_to(ROOT).as_posix(), ln, m.group(0)))

n_links = sum(len(re.findall(r"\[\[", p.read_text(encoding="utf-8"))) for p in ROOT.rglob("*.md"))
print(f"notes: {len(list(ROOT.rglob('*.md')))}  images: {len(images)}  wikilinks: {n_links}  broken: {len(bad)}")
for b in bad[:30]:
    print("BROKEN", *b)
print("unresolved .md tokens (left as text):", sorted(unresolved.items(), key=lambda kv: -kv[1])[:25])
print("images never referenced:", [i for i, u in img_uses.items() if not u])
