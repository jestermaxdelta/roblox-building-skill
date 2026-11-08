# Roblox Building Skill

A Claude Code skill that helps you design, build and launch Roblox games, from the first idea to weekly updates.

You don't need special commands. Tell Claude what you want to make, and the skill guides it step by step.

---

## Install (one command)

```bash
git clone https://github.com/jestermaxdelta/roblox-building-skill.git ~/.claude/skills/roblox-game-design
```

Restart Claude Code. That's it.

To update later:

```bash
cd ~/.claude/skills/roblox-game-design && git pull
```

---

## How to use it

Talk to Claude normally about your Roblox game. The skill turns on by itself.

If it doesn't, start your message with `/roblox-game-design`.

---

## Use case examples

### 1. "I have an idea for a new game"

**You say:**

> I want to make a Roblox tycoon where you run a pizza delivery company. Ages 9 to 14, mostly mobile. I'm solo and want a first version in 4 weeks. No luck mechanics.

**Claude does:**

1. Writes a one-page plan: the fantasy, 3 design pillars, and the core loop (cook, deliver, earn, upgrade).
2. Plans the first 5 minutes of play, so players get a reward within 30 seconds.
3. Builds an economy sheet with real numbers: prices, upgrade costs, income per minute.
4. Plans the code structure, the save data and the shop products.
5. Only then starts building, beginning with one small playable loop.

### 2. "I don't know what game to make"

**You say:**

> What Roblox game should I build next? I like simulators.

**Claude does:** checks current market trends, compares a few game ideas, and recommends one safe option and one bold option, with the reasons for each.

### 3. "Help me make money from my game"

**You say:**

> Add monetization to my simulator. It has egg hatching.

**Claude does:** plans boosts (2× Cash, 2× Speed, Luck), a starter pack, gift versions of passes and convenience passes. It times offers so they never interrupt play (none in the first 10 minutes, at most 3 per session), shows the odds on luck items as Roblox requires, and writes purchase code that never charges a player twice or loses a purchase.

### 4. "Fix one thing"

**You say:**

> My players lose their coins sometimes. Here's my DataStore script.

**Claude does:** goes straight to the data-saving guide, finds the bug and fixes it with safe saving (ProfileStore with session locking).

### 5. "My game is laggy on phones"

**You say:**

> My game runs badly on phones. Make it faster.

**Claude does:** works through a performance checklist (draw calls, streaming, collision, scripts) and fixes the biggest problems first.

### 6. "I'm about to launch"

**You say:**

> I'm launching my game this weekend. Am I ready?

**Claude does:** runs the launch checklist (thumbnails, icon, description, age rating, analytics, security, purchases) and tells you what's missing.

---

## What to tell Claude (the more, the better)

| Tell it | Example |
|---|---|
| Your idea | "You run a pizza delivery empire" |
| Genre | Tycoon, simulator, obby, horror, RPG |
| A similar game | "Like Restaurant Tycoon 2" |
| Who plays it | "Ages 9 to 14, mostly on phones" |
| Your time and team | "Solo, 4 weeks" |
| Luck mechanics? | Yes or no (luck boosts only work with yes) |
| Can it use Roblox Terrain? | Yes or no (the default is no) |
| Where you are | New idea, prototype or live game, plus your project folder |

If you leave something out, Claude asks or picks a sensible default and tells you.

---

## Rules the skill always follows

1. **Every 3D model is made in Blender.** No basic Roblox parts and no free marketplace models in the finished game.
2. **Everything is solid.** Players can't walk through walls, props or buildings.
3. **Lots of shop items, but never annoying.** Offers are small, easy to close and never block play. No fake discounts, fake countdowns or fake "limited stock".

---

## What you need

- [Claude Code](https://claude.com/claude-code)
- Roblox Studio with the Studio MCP connected, so Claude can build and playtest
- Blender, plus a Blender bridge script in your game project (`tools/blender_exec.py`)

**Tip:** keep the planning files Claude writes in your game's `docs/` folder. Claude doesn't remember between chats, but it reads those files to pick up where you left off.

---

## What's inside

| Path | What it is |
|---|---|
| `SKILL.md` | The main instructions Claude follows: 12 steps from idea to live game, with a checklist for each |
| `references/` | 16 topic guides: game design, genres, economy math, monetization, security, saving data, performance, Blender pipeline, UI and more |
| `references/knowledge-base.md` | The full 90,000-word research document behind the skill |
| `templates/` | Fill-in documents: one-page plan, design doc, economy sheet, product plan, analytics plan, playtest plan, launch checklist |

The research comes from 31 GitHub repositories, led by Roblox's official Creator Docs, and was compiled in November 2026. Some facts (prices, limits, APIs) change over time, so Claude re-checks those against the live Roblox docs.
