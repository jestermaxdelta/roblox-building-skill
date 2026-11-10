# Case studies and teardowns (what the hits did, what killed the rest, how to take any game apart)

Eighteen teardowns of successful Roblox games, the patterns they share counted across the set, the well-known collapses, and a stopwatch method for tearing down any game: a competitor, or your own. Open it at concept time to borrow mechanisms instead of themes, and on a live game to find the gap between your first ten minutes, store and cadence and the games your players compare you with. Every number carries a source and date; other creators' revenue, retention and click-through are not published by Roblox and are never guessed here.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | Run the stopwatch protocol (§1.3) on 3 games in your genre and on your own game; fill the template (§1.6); read the 2 teardowns closest to your idea; apply the copy / change / avoid filter (§1.5) | Revenue estimates, tracker peaks, the pattern counts |
| Intermediate | Build the comparison table (§6 step 3); map economy and price ladder (§1.4); log competitors weekly for 8 weeks (§1.7); check your plan against §3 and §4 | Chasing a trend you cannot ship inside its window (§5) |
| Expert | Use badge ratios as a rough funnel, pass-list history as a pricing log and update stamps as a cadence model (§1.2); decide trend vs durable with §5; run §6 as a quarterly review with experiments | Single-source claims: anything marked unverified is a lead, not a fact |

## Contents

0. How to read the numbers · 1. Teardown method and template · 2. Eighteen teardowns · 3. Cross-game patterns, ranked · 4. Failure studies · 5. Trend-chasing vs evergreen · 6. Level-up: use a teardown to fix your own game · Review gate · Sources

## 0. How to read the numbers

- **CCU** = concurrent users (players online at one moment). All "now" figures are single snapshots `[VS]`: **LF-27** and **LF-29** = LihFolk's reads of Roblox's public game, votes and game-pass endpoints on 2026-10-27 (US afternoon) and 2026-10-29 08:06 UTC (off-peak; Halloween platform event running) `[lihfolk]`; **V-7** = the owner's vault snapshot, 2026-11-07 09:40–11:00 UTC (see `market-scan-2026-11.md`). CCU swings 2–3× by hour, so two snapshots of one game differ without anything having changed.
- **Peaks** come from third-party trackers (Rolimons, RoMonitor, RoStats, RoWatcher, RoTrends) or press. A tracker's "all-time peak" covers only the period it has been recording `[lihfolk]`. Where sources disagree, both are given.
- **Prices** are public game-pass lists on the stated date `[VS]`. Developer products (repeatable purchases) are not listed publicly; those prices are guide-reported and marked.
- **Limits of the evidence.** The LihFolk notes were written from store pages, APIs, press and guides; nobody played the games for them. Loop timings below are therefore press- or guide-reported unless marked otherwise. Before acting on a teardown, replay the first ten minutes yourself with §1.3: stores, tutorials and prices change every update.
- **Conflict (peaks):** +1 Speed Keyboard Escape 4.04M (V-7, 19 Sep 2026) vs 7.26M (Rolimons, 18 Jul 2026, via LihFolk) vs 5.62M and about 6.2M (other tracker posts); Fisch 510K tracked (V-7) vs 1.3M (RoTrends, undated) and "1M on 4 Oct 2025" (fan wiki); Dress to Impress 651K (NYT, Aug 2024; V-7) vs about 1.7M (trackers, Dec 2024, unconfirmed by press); 99 Nights 11.2–14.2M; Animal Hospital about 564K (V-7) vs 736,948 (Rolimons via GosuGamers) vs 1.3M (RoWatcher, 10 Jul 2026). Keep the vault figure as the house number and quote the range when it matters; none of these changes a design decision.

## 1. Teardown method

A teardown is a timed, written play-through of someone's game that ends in decisions. It answers four questions: how fast does the fun arrive, what keeps the loop turning, what is sold and when, and what brings the player back tomorrow.

### 1.1 Choose the set

Study 5–8 games in three tiers `[lihfolk]`: 1–2 **leaders** (what players expect, the polish bar, price norms), 2–4 **peers** of your size and age, ideally launched in the last few months (what is achievable now; the tier most teams skip), 1–2 **adjacent** games that use a mechanic you are considering. For your own game, run the identical protocol on it, on the same phone, the same day.

### 1.2 What you can see from outside

| Source | Gives you | Trust |
|---|---|---|
| Store page | Title tags, description (often the tutorial), thumbnails, icon, genre, server size, created and updated dates, events | `[official]` data, snapshot only |
| Public pass list | Every game pass and price, including off-sale ones; the shape of the price ladder | `[VS]`; no sales data; developer products are missing |
| Badges | How many players earned each: tutorial badge vs zone-3 badge is a rough funnel (biased: late-added badges count only later players) | `[lihfolk]` `[community]` |
| Creator Hub watchlist | Up to nine games; for games you do not own: like ratio, CCU, updated date, title, owner. Benchmark scorecards for your own game need 100+ DAU and are not a ranking signal | `[official]` `[VS]` |
| Third-party trackers | CCU history, spike days, update days, session and revenue *estimates* | `[community]`; sampled, undocumented methods; never enter credentials |
| Your own play-through | Timings, pop-ups, developer-product prices, UI, feel | The only first-hand source; use a fresh account so progress and personalisation do not distort it |

Never exploit, decompile or use third-party tools to read another game: it breaks Roblox's terms and the method does not need it `[lihfolk]`.

### 1.3 Stopwatch protocol

Start the stopwatch when you tap Play. Use a 3 GB Android phone first, PC second. Write during the session, not after: memory smooths out the friction you are measuring.

| Checkpoint | Record | Why it matters |
|---|---|---|
| **First 60 s** | Seconds to a controllable character; first thing on screen (world, menu, tutorial, pop-up); seconds to first core action; seconds to first reward; what another player's presence taught you; anything you had to read | First-play bounce is a top Recommended For You signal `[official]` `[VS]`; 14 of the 18 games below put the verb inside the first two minutes |
| **First 10 min** | Loop length (seconds per cycle); what differs on cycle 10 vs cycle 1; first upgrade decision; first visible long goal; pop-up count in the first 3 min; minute and content of the first purchase prompt; first "wall" (where progress slows) and how it resolves: grind, social, purchase or skill | The loop and its first escalation live here (`core-loop-tuning.md` §2) |
| **First session** | Session length before you ran out of things to want; currencies seen; every sink and source; every timer; shop tabs and all prices; paid random items and whether odds show before purchase; social touchpoints; the best and the worst moment | Economy, monetisation and social maps |
| **Day 2** | What was waiting (offline income, restock, daily, streak, event); whether you remembered the goal; seconds from join to resuming; what changed on the store page; any notification received | Return hooks; D1 is decided by what you left unfinished and what is waiting |

Then press Shift+F5 (debug stats) or switch on Performance Stats in the client settings for memory and ping `[official]` `[VS]`.

### 1.4 The seven maps

| Map | Write down | Red flags worth noting |
|---|---|---|
| Loop | One sentence "You ___ to get ___ so you can ___"; micro loop (seconds), session loop (minutes), meta loop (days) with a time on each | A menu where a visible journey should be; no change by cycle 10 |
| Economy | Each currency; sources (per minute at minute 5, 30, 120); sinks; gates and their prices; multipliers and how they stack; rebirth terms; trading | One currency doing everything; gates growing faster than income with no new verb |
| Monetisation | Every pass and product with price; class of each (time, capacity, cosmetic, access, power, luck, influence over others); cheapest and dearest item; when and where prompts appear; odds disclosure | Power over other players; luck at the top of the ladder; a prompt before the first win |
| Retention hooks | Timers, restocks, offline income, dailies, quests, seasons, events, collections, unfinished goals; which need a long session and which need a short return | Streak-loss threats; anything that punishes absence |
| Social hooks | Server size; what other players can see of you; co-op roles, trading, voting, theft; friend and private-server bonuses; what works with chat off | Interaction that only harms; nothing to do together |
| UI inventory | HUD elements at spawn (count them); taps from spawn to the core action; shop depth; smallest text; thumb reach; what sits on the top and bottom edges; notification style | A HUD more crowded at spawn than the genre leaders'; modal stacks on join (`ui-input-crossplatform.md`) |
| Technical | Seconds to control on phone; memory and ping; pop-in (streaming); separate lobby and run places; rubber-banding on steals, hits or vehicles; obvious automation by other players; frame drops in a full server | Long first load; client-trusted stats; unbounded player-spawned objects |

### 1.5 Copy / change / avoid filter

| Bucket | Rule | Examples from §2 |
|---|---|---|
| **Copy** the mechanism | Structures nobody owns: a shared visible clock, a price-ladder shape, a first-minute order, a fixed update day | Shared restock, lock timer, "anywhere" passes, per-zone checklist |
| **Change** the expression | Verb, theme, characters, names, UI layout and all art are yours: one new verb, every asset authored in Blender with real collision `[house]`. Near-identical metadata or place files are deprioritised `[official]`; copied UI and art are what the Steal a Brainrot owners sued over (Bloomberg via The Star, 2026-03-25) | Steal a Brainrot → Steal An Egg changed the verb order and theme |
| **Avoid** what breaks house rules or drew the criticism | Power over other players for Robux, paid luck as the top of the store, hidden spend tiers, pay-to-continue at the moment of death without a free path, resets of earned progress, retired-pass scarcity used as pressure | Paid steals, admin-command passes, luck ladders |

### 1.6 Fill-in template

```
TEARDOWN  Game: ________  Tier: leader / peer / adjacent / OWN   Date+hour (UTC): ______
Device: ________  Account: fresh Y/N   Update tag in title/description: ________
Public data: created ____  updated ____  server size __  like ratio __%  CCU now ____ (source ____)
             tracker peak ____ on ____ (source ____)   passes on sale __  cheapest __ R$  dearest __ R$

FIRST 60 S    control at __ s | first screen: world/menu/tutorial/pop-up | first action at __ s
              first reward at __ s | text I had to read: ____ | what other players taught me: ____
FIRST 10 MIN  loop sentence: "You ____ to get ____ so you can ____."   cycle = __ s
              cycle 10 differs from cycle 1 by: ____ | first upgrade at __ min | long goal visible Y/N: ____
              pop-ups in first 3 min: __ (list) | first purchase prompt at __ min: ____ for __ R$
              first wall at __ min, resolved by grind/social/purchase/skill
FIRST SESSION length __ min | currencies: ____ | sources: ____ | sinks: ____ | timers: ____
              rebirth/prestige terms: ____ | trading Y/N, gated by ____
DAY 2         waiting for me: ____ | seconds to resume: __ | store page changes: ____ | notification Y/N

MONETISATION  item | price R$ | class (time/capacity/cosmetic/access/power/luck/influence) | where offered
              ...
              paid random items Y/N; numeric odds before purchase Y/N; rewarded ad placements: ____
SOCIAL        visible to others: ____ | reasons to play together: ____ | harmful interactions: ____
UI            HUD elements at spawn: __ | taps to core action: __ | smallest text OK on phone Y/N
TECHNICAL     memory __ MB | ping __ ms | pop-in Y/N | lobby+run places Y/N | automation seen Y/N
FEEL          best moment: ____   worst moment: ____   bugs/friction: ____

COPY (mechanism): ____     CHANGE (verb, theme, art): ____     AVOID (and why): ____
DECISIONS (max 5, each with the metric it should move): ____
```

### 1.7 Tracking over time

One teardown is a photograph; an 8-week log is a model of how the game is run `[lihfolk]`. Fifteen minutes a week across all tracked games: CCU trend, update shipped (weekday), event, new or retired passes, title tag, thumbnail change. A thumbnail that survives for months is probably winning its personalisation pool; a pass that vanishes was either retired on purpose or failed. Use the log to pick an update day that does not collide with the genre leader's.

## 2. Teardowns

Fields: **Is** (what and how big) · **Loop** (with timings) · **First minute** · **Money** (economy shape and observed prices in Robux, R$) · **Keeps** (retention and social) · **Cadence** · **Spread** · **Risks** · **Lessons**. Unless marked otherwise, facts are `[lihfolk]` (its notes cite press, trackers and guides) cross-checked against V-7.

### 2.1 Grow a Garden (idle farming; the spike-and-collapse reference)
- **Is:** plant, wait, harvest, sell on your own visible plot. Built in a few days by a 16-year-old; Splitting Point partnered at about 500 CCU and 10–20K daily users, then it reached about 100K CCU in two weeks and 1M in a month (GamesBeat interview, 2025-09-07, search summary). Peak 22.3M on 23 Aug 2025 (press citing RoMonitor); 13.6K (LF-27), 19–28K (V-7).
- **Loop:** seconds to minutes: check the shared seed shop (restock about every 5 min, guide-reported), plant, harvest, sell. Hours: rare stock, multi-harvest crops, pets. Days: mutated crops (guides: Gold ×20, Rainbow ×50) and weekly event goals.
- **First minute:** you spawn beside your own empty plot holding enough currency for the first seed; the shop is a few steps away; a sprout appears on the click; fast crops ripen in 1–2 min. The whole loop shows in 2–3 min with no tutorial screen.
- **Money:** deterministic base loop with random server-wide weather multipliers on top. Spend is almost all consumable; reported prices 2025–26: season pass 749, level skip 49, cosmetic crate 199 / 575 / 1,699 for 1 / 3 / 10, paid crop steal 37 (guides and press; unverified against the store). The public pass list held one off-sale pass (LF-27).
- **Keeps:** offline growth (the icon text is the promise), the restock as a server-wide moment, weather, live admin events, plots everyone can walk up to.
- **Cadence:** weekly Saturday updates with named themes; two event teams from July 2025.
- **Spread:** a verb from real life, nothing to learn, rare-mutation clips, the 23 Aug 2025 crossover "admin war" with Steal a Brainrot.
- **Risks:** players called weekly events repetitive by Aug 2025 and the studio acknowledged it; paid stealing drew press criticism; rare pets were resold for real money; under the waiting loop there was little else.
- **Lessons:** (1) make leaving an investment: stamp server time on every growing thing and cap the payout; (2) a shared, visible restock turns a shop into an event; (3) put randomness on top of a dependable loop, never in place of it; (4) a loop built on waiting needs goals that survive a month without new content; (5) never sell an action that takes from another player.

### 2.2 Steal a Brainrot (idle tycoon with theft)
- **Is:** buy units from a shared conveyor, earn per second in your base, steal from the other 7 players. Created 16 May 2025; peak 25.4–25.8M in Oct 2025 (sources differ); 244K (LF-27), 103K (V-7); 74.2B visits; about 85% approval. Estimated $64M of player spending from launch to March 2026 (RoMonitor via Bloomberg via The Star; an estimate of spend, not developer income).
- **Loop:** watch the conveyor, buy the best affordable unit, collect, re-lock the base (about 60 s, +10 s per rebirth, guide-reported); decide whether to leave it exposed to raid someone richer; rebirth resets cash and most units for a multiplier, more slots and a longer lock. A guide puts the first price-tier jump about 8 min in.
- **First minute:** price tags float over every unit on the conveyor, so the economy teaches itself; other players demonstrate stealing by doing it to you.
- **Money:** passes on LF-27: Admin Commands 7,999, VIP 375, 2x Money 299 (older guides list lower prices; the ladder was raised). Gear, lucky blocks and skips are developer products.
- **Keeps:** loss creates attention, and a steal-back is always possible; rare units appear to the whole server at once; scheduled "admin abuse" events; a countdown on the icon itself; concerts and crossovers (12.8M CCU at a January 2026 concert).
- **Cadence:** a named update roughly weekly (Update 44 by early 2026).
- **Spread:** the verb is the title; clip-ready drama; a meme the audience already knew; the lead developer built the community through Discord, video and live events.
- **Risks:** Polygon called the best items cash-only; power over other players is sold; automation scripts for collecting and stealing; a character was pulled from Sept to Nov 2025 in a licensing dispute; hundreds of clones and at least four lawsuits by the owners; each event peak decays faster than the last (RoWatcher).
- **Lessons:** (1) put the verb in the title and show income as a rate; (2) express risk as a timer anyone can read; (3) let rebirth add safety and slots, not only multipliers; (4) validate every steal on the server: distance, lock state, carry state, cooldown; (5) the theft that makes the clips also makes the 85% rating: protect newcomers and sell no weapon aimed at players.

### 2.3 Steal An Egg (the 2026 remix of the steal loop)
- **Is:** train speed, outrun an egg's guardian, hatch a pet that earns, guard your pen. Created 25 Jul 2026; 7-player servers; peak 14.31M on 19 Sep 2026 (RoStats; V-7 ties it to a crossover); 950K (LF-29), 1.14M (V-7); 91.6% approval.
- **Loop:** treadmill raises speed; speed gates biomes; grabbing an egg wakes its guardian; carry it over the safe line; it grows at your pen (10 s to 25 min); the pet pays per second and adds speed. Nests reset every 5 min and events run every 30 min (V-7). Average session about 16 min (Adellion, unverified).
- **First minute:** the treadmill beside spawn makes a number climb at once; the first biome needs almost no speed, so the first grab and chase happen inside a minute, with nothing to read.
- **Money:** public passes X2 Money 399 and X2 Growth Speed 467 (LF-29): self-only multipliers. Products are not visible from outside.
- **Keeps:** two stats: speed is personal and only goes up, money sits in a shared world and can be taken, so a robbed player never feels reset to zero; biome gates as the visible next goal; size and mutation variants keep duplicates worth having.
- **Cadence:** weekly numbered Saturday updates, crossovers and a concert (V-7).
- **Spread:** a known loop plus one physical skill moment; eggs and pets need no meme literacy; launched a year after the brainrot peak, when players loyal to the loop wanted a fresh version.
- **Risks:** disappeared from the platform for a few hours on 24–25 Aug 2026 and returned without its scrolling video panel (allthings.how; no Roblox statement found); five more egg titles sat in the top 100 within three months; guide-level odds tables disagree.
- **Lessons:** (1) remix by changing the order and feel of the verb, not the theme; (2) pair a stat that cannot be lost with one that can; (3) an environmental guardian teaches risk before any player does; (4) seven players keeps theft possible without a crowd; (5) do not bolt on a feature that can get the whole game pulled.

### 2.4 Pet Simulator 99 (collection incremental run as a weekly machine)
- **Is:** break, collect, hatch, equip, unlock the next area. Launched 1 Dec 2023 by BIG Games as a sequel that carried pets forward; 79.9K (LF-27), 46–48K (V-7); peak 481K (RoTrends, undated); about 95% approval; 10-player servers.
- **Loop:** coins fly in the first ten seconds; first egg in 1–2 min; first coin-priced gate soon after; the newest area always pays most. Nine rebirths at areas 25, 50, 75, 99, 125, 150, 175, 199, 219, each +75% pet strength and no longer resetting progress (guide, Oct 2026). Sessions reported at 111 min (Adellion, unverified).
- **First minute:** starter pets swarm whatever you tap; quest arrows and two rank goals are always on screen.
- **Money:** 13 passes, 175–3,250 (LF-27): Auto Farm 175, Lucky 275, Auto Tap 350, +15 Pets 375, VIP 400, +15 Eggs 625, Ultra Lucky 800, Magic Eggs 1,200, Double Stars 2,400, Huge Hunter 3,250. Five of thirteen sell luck and the top of the ladder is luck on the rarest pet; prices rose over time. Per-world coins plus one global currency (diamonds).
- **Keeps:** rank goals as the daily driver; Huge pets as the chase; a Trading Plaza unlocked only after the first rebirth, so day-one accounts cannot be scammed; a "Potato Mode" for weak phones.
- **Cadence:** Saturdays 5 PM GMT, weekly, numbered (Update 73 on 14 Mar 2026); limited-time events about every two weeks whose pets do not return (RoWatcher, search summary).
- **Spread:** franchise audience, weekly video topics for creators, physical toys with codes.
- **Risks:** paid luck is the most policy-exposed store shape for a young audience (RoWatcher calls it the platform's most aggressive); the predecessor's NFT sales were refunded in Feb 2023; off-platform sale of rare pets; the predecessor needed duped currency reverted and accounts banned (BIG Games post, search summary).
- **Lessons:** (1) rebirth as an unlock, not a loss; (2) one currency per world resets pacing without taking anything away; (3) gate trading behind progress; (4) a fixed weekly slot is a product in itself; (5) do not copy a luck-led store: under house rules luck is at most a disclosed, timed boost, never the top of the ladder.

### 2.5 Blox Fruits (action RPG grind with a power-item chase)
- **Is:** quest, fight, level, sail to the next island; 42 fruits (power sets) from common to mythical. Created 16 Jan 2019 as "Blox Piece", renamed under copyright pressure; 65.1B visits; 92.3% approval; 12-player servers; peak about 2.77–2.78M on 31 Dec 2024 after the Dragon rework; 127K (LF-27), 325K (V-7).
- **Loop:** take an island quest sized to your level, kill N enemies or a boss, spend stat points across five stats, repeat until the next island; level cap 3,000 across three seas (second sea at level 700). The dealer's stock rotates every 4 h on a fixed UTC grid, and a second dealer every 2 h (fan trackers; unconfirmed by the studio).
- **First minute:** choose Pirates or Marines, talk to the quest giver beside spawn, win fights within the first couple of minutes; stat points from level 1 mean a build decision before you understand the game.
- **Money:** six passes (LF-27): Fast Boats 350, 2x Boss Drops 350, 2x Money 450, 2x Mastery 450, Dark Blade 1,200, Fruit Notifier 2,700. Main revenue is fruits sold as products, guide-reported from 50 up to 5,000 for a permanent Dragon. Paid fruits are chosen, not random.
- **Keeps:** one global stock on a clock makes "it is in stock" news that travels through Discord and video within minutes; world spawns and boss respawns; mastery as a second ladder; crews, bounty PvP, trading since 2022.
- **Cadence:** few, large, numbered updates with long teasers; a tracker showed about −40% over 30 days between updates, and a rival shipping weekly is cited as part of the slowdown (RoWatcher, search summary); teasers without firm dates draw criticism. A Fourth Sea is reported for December 2026 (V-7).
- **Spread:** borrowed anime fantasy, tier-list and stock-alert creators, record-setting update days.
- **Risks:** a rework converted paid Dragon fruits into tokens and angered owners; raw power sold in a game with PvP; IP borrowing forced the rename; trading around 5,000 R$ items attracts scams.
- **Lessons:** (1) an identity choice in the first ten seconds costs almost nothing; (2) levels are the floor, a rare swappable power set is the dream; (3) one global timed stock builds a check-in habit with no login streak; (4) write down what "permanent" means before selling it, and let owners keep the old version through a rework; (5) fill the gap between big updates with small dated events.

### 2.6 Brookhaven RP (social sandbox; a stage, not a game)
- **Is:** a town with free houses, cars and outfits for pretend play. Created 21 Apr 2020 by a two-person team; sold to Voldex (announced 4 Feb 2025, about 60B visits then); 88.9B visits; 30-player servers; all-time peak 1,296,208 on 19 Dec 2025 (Rolimons), under the new owner and without one large new mechanic; 334K (LF-27), 438K (V-7).
- **Loop:** no scored loop: join friends, claim a house, pick a role and outfit, spawn a car, improvise a scene in a purpose-built building, switch.
- **First minute:** no gate at all. One menu holds houses, vehicles and avatar; a free house and car are yours within a minute or two. The first reward is ownership, not currency.
- **Money:** 18 passes on sale, 35–749 (LF-27): Vehicle Upgrade 35, On Demand Fire 40, Horse Upgrade 85, Penthouse 180, Music Unlocked 199, Premium 320, Land Unlocked 375, Estates 599, House Pets 599, VIP 749. Five passes cost 199 or less; everything sold expands expression or control, nothing sells power. Private servers are sold with a long list of admin powers. A guide reports an event radar for 9 R$ or one rewarded ad.
- **Keeps:** friends, weekly novelty, private servers as a tool for running a community, event hunts that hide collectibles across the existing map (60 pieces, 23 Oct–6 Nov 2026, guide-reported).
- **Cadence:** weekly, typically Fridays, with seasonal events on top.
- **Spread:** roleplay stories are a natural video format; players join friends in progress.
- **Risks:** the most crowded category on Roblox, so a smaller town loses on every measure; unbounded props and vehicles are a performance and abuse load; free-form hangouts carry rating and safety obligations (`genre-playbooks.md`, social hangout); placeholder passes left public look careless.
- **Lessons:** (1) in a stage game any gate between player and props is friction with no payoff; (2) buildings are scene prompts: each one implies a role; (3) sell scale and control, with several entry points under 200 R$; (4) a mature social game can set records on cadence and polish alone; (5) reuse the map for events instead of building a new area.

### 2.7 Adopt Me! (pet care, collection and trading)
- **Is:** raise pets through care tasks, fuse duplicates, trade. Created July 2017 as family roleplay; pets added mid-2019 made it a giant; peak 1.92M in April 2021 (studio press release; one tracker dates a 1.9M figure to April 2026, unverified); 207K (LF-27), 167K (V-7); 35-player servers; about 40 staff in 2021.
- **Loop:** a need icon appears, walk to the matching place, get paid and age the pet; six growth stages; four full-grown copies make a Neon, four Neons a Mega Neon (16 copies). Trading sits across everything.
- **First minute:** pick Parent or Baby; collect a Starter Egg that can only hatch a dog or a cat; the first need is always hunger and the sandwich is handed to you. A scripted first success and a safe first roll: randomness arrives only after the player owns something.
- **Money:** only 6 of 24 passes on sale (LF-27): 1.25x Candy Multiplier 50 (event-long), Premium Plots 285, +1 Pet Pen Slot 295, VIP 480, Cozy Home Lure 765, Millionaire Pack 795. Robux-only pets and eggs are products. Shape: a cheap event pass for the first purchase, 285–480 for permanent convenience and status, 765–795 for bundles.
- **Keeps:** fusion gives every duplicate a purpose; event-only and retired pets; one event currency with weekly drops inside each event; trade licences, trade history and unfair-trade warnings since Nov 2020; daily task board (guide-reported).
- **Cadence:** a rolling event calendar; major updates have roughly tripled CCU (V-7).
- **Spread:** adding one strong meta system (collect, fuse, trade) to an existing social sandbox was worth more than a new game.
- **Risks:** rare pets sold for real money, trust-trade scams, a widely reported A$8,000 child bill (2020); the economy is the product, so a duplication exploit would be fatal; event surges strain servers and data.
- **Lessons:** (1) script the first success and make the first roll impossible to regret; (2) fusion ladders (4 into 1) turn duplicates into goals and reuse art; (3) a 50 R$ event-long multiplier is an honest first purchase; (4) ship anti-scam UI with trading or do not ship trading; (5) do not use retired passes as a pressure lever: real end dates only.

### 2.8 DOORS (co-op horror roguelite)
- **Is:** open 100 doors, learn each entity's rule, survive. Released 10 Aug 2022; press names two developers; 7.96B visits; about 93% approval; 45K during a platform Halloween event (LF-27); tracker peak about 273K (window-limited). Best Use of Audio, 2026 Innovation Awards (Roblox newsroom, search summary).
- **Loop:** lobby, elevator with friends or strangers, pre-run shop (soft currency buys a flashlight, lockpick or vitamins), run. Fixed set pieces anchor each run: chases near doors 35 and 75, a stealth room at 50 and 100; rooms, items and spawns vary between them. Death returns you to the lobby with currency.
- **First minute:** a walk-in elevator is the party system; cheap scares in the first rooms; a lethal entity within minutes that telegraphs with flickering lights and has one answer (hide). Death is the tutorial: a friendly guide explains what killed you.
- **Money:** three passes (LF-27): event pass 99, cosmetic bundle 299, Admin Panel 499. Revives are Robux-only (30 R$, V-7; one free for new players and for joining the group); currency packs and boosts are products. No paid power, luck or gacha.
- **Keeps:** you improve, the character does not, so newcomers and veterans can share a run; achievements, difficulty modifiers, floors; a feature that lets a streamer's audience interfere with the run.
- **Cadence:** slow and big: Floor 2 arrived two years after launch (30 Aug 2024) and was coolly received by part of the audience (Roonby); mid-size updates and platform events between.
- **Spread:** screams on video; a wordmark readable at 50 pixels; entity fan culture and merchandise.
- **Risks:** a two-year gap works only on a base replayable hundreds of times; long teasers raise expectations; pay-to-continue at the moment of death needs a free path and a cooldown; a shop tier that appears only after heavy spending is reported by a community wiki (do not build one).
- **Lessons:** (1) teach by failing, then explain; (2) fixed anchors inside random runs give every run a story; (3) one tell and one answer per threat; (4) a tiny store survives parents and press; (5) sell before or after the run, never during a chase, and give revives away generously.

### 2.9 Dress to Impress (round-based social judging)
- **Is:** theme, timed dressing, runway, peer vote, podium. Released 11 Nov 2023 by a teenage-led team; 11.25B visits; 13-player servers; 651K+ after a pop-album collaboration (Aug 2024, NYT), about 1.7M in Dec 2024 (trackers only); 97.7K (LF-27), 66.8K (V-7).
- **Loop:** the theme is announced in the lobby; dressing ran 360 s in Oct 2024 (Game Rant); each player walks the runway while the rest rate 1–5 stars; the top three take the podium and everyone is paid stars (rank) and cash. A new player has been through the full loop, judged by real people, in about 7 min. A Freeplay mode has no timer or votes.
- **First minute:** you join a server mid-cycle; a theme and a countdown remove the blank page; many items are free.
- **Money:** 14 passes (LF-27): Increased Item Limit 129, Run Faster 149, eight clothing sets at 279–449, Custom Makeup 349, x2 Money 399, VIP 799. No random items, no stats. Sets are a style edge in a judged game; Run Faster is the one pass that changes the competition.
- **Keeps:** a rank ladder built from peer votes; limited-time code items; a story told through seasonal quests that players theorise about between updates; duo mode; collaborations.
- **Cadence:** event-led (a 40-tier Halloween pass in 2026, guide-reported); collaborations in 2024 and 2025.
- **Spread:** a pose became a TikTok meme; streamers; press around the collaboration.
- **Risks:** a three-hour code item crashed the game when everyone redeemed at once (Dec 2024); peer voting invites friend-boosting and revenge votes; a single round format fell to about a sixth of peak or less despite later collaborations; a 2025 celebrity live event was criticised as less personal than promised.
- **Lessons:** (1) a constraint plus a timer is the best onboarding for a creative game; (2) pay everyone, celebrate three; (3) let players be each other's content and judges, with vote weighting and rate limits from day one; (4) sell sets, not stats; (5) spread any timed drop over a window and load-test the redeem path.

### 2.10 Bee Swarm Simulator (the long-lived solo simulator)
- **Is:** gather pollen with a growing swarm, convert to honey, buy bees and gear. Created 21 Mar 2018 by one developer; 4.63B visits; 95.6% approval; 6-player servers; 30.3K (LF-29), 32.5K (V-7); winter-event peaks of 147–265K (tracker articles, unverified).
- **Loop:** claim a hive, swing a tool in a field, fill the backpack, walk home, convert, spend; a bear's quest points at the next purchase. Sessions of 25–31 min are reported for long-lived simulators including this one (Adellion, unverified).
- **First minute:** the first bee hatches as you claim the hive; pollen numbers pop on the first swing; the bag fills fast enough to force the first trip home.
- **Money:** four multiplier passes (x2 pollen, x2 convert speed, x2 ticket chance, one special bee) with no price returned on LF-29; premium currency and items as products.
- **Keeps:** fields gated by bee count, so the collection is also the map key; years of quest lines give a returning player an obvious next step; a slow, visible, permanent hive; secrets the community documents; a yearly winter event (the 2025 one ran from December into March 2026).
- **Cadence:** slow and careful; pace is the community's most consistent complaint, and the latest winter event's quests were criticised as grindy (RoWatcher, search summary).
- **Spread:** a specific warm fantasy instead of "collect coins"; one consistent voice.
- **Risks:** long droughts between rituals; a paid drop-chance pass is a probability modifier and needs numeric disclosure `[VS]`.
- **Lessons:** (1) let the collection double as the key to new places; (2) quest lines are cheap retention for lapsed players; (3) one annual ritual can carry an evergreen; (4) depth at the top is what "lasting" means; (5) a solo developer's game still holds about 30K CCU eight years on, at the price of slow updates.

### 2.11 Tower Defense Simulator and Anime Vanguards (two store shapes for tower defence)
- **Is:** co-op wave defence from a lobby. TDS: created 5 Jun 2019, 5.05B visits, 94% approval, 9.6K (LF-29), 50-player lobby with matches in separate servers. Anime Vanguards: released 8 Sep 2024, peak 340,167 in launch week (Rolimons), 96.7% approval on 2.7M votes, average session 48.2 min (Rolimons), 13.6K at check with an 84.5K 30-day peak (LF-29).
- **Loop:** form a party in the lobby, teleport to a match, place and upgrade units as cash flows, beat waves and a boss, earn currency and materials, upgrade or summon, push a harder mode.
- **First minute:** AV gives a guided first summon and an easy first stage that teaches place, upgrade and sell. TDS's group-join reward is +$100 starting cash: it helps the first match rather than adding permanent power.
- **Money:** TDS (LF-29): Sandbox Plus+ 7,999, Hacker 2,249, Engineer 1,690, Mercenary Base 1,350, limited-time towers 499–799, VIP 375, Custom Music 85, emotes 55, plus crates and a battle pass; many retired towers remain on the list off sale. AV: Shiny Hunter 1,299, Cosmetic Recolor 799, Display All Units 599, VIP 299, Extra Unit Storage 149; summons are paid random items when bought with Robux or Robux-bought currency.
- **Keeps:** mode ladders (story, challenges, raids, infinite) reuse units and maps; episodic content gives the title a reason to change (TDS's title read "[🌙 NIGHT 3]"); long matches are filled with planning.
- **Cadence:** TDS episodic; AV large numbered updates every few months with events and code drops between.
- **Spread:** anime rosters, tier-list creators, co-op carries.
- **Risks:** paid towers that beat free ones make free players passengers; limited-time towers lean on urgency with a young audience; idle farming with parked towers; many enemies and effects in late waves (`genres/tower-defense.md`).
- **Lessons:** (1) spend effort on information design: range shapes on placement, costs and enemy health always visible; (2) one unit you love and one win in the first minute; (3) new rule sets multiply content faster than new maps; (4) a premium sandbox mode is a high-price item that touches nobody else; (5) keep paid units side-grades and show odds on every paid roll.

### 2.12 Blade Ball (one-input skill PvP)
- **Is:** a homing ball picks a target, the target parries, the ball speeds up; last player standing wins. Created 17 Jun 2023 by two developers; peak 511,924 on 19 Nov 2023; 11K (LF-29); 93.5% approval; average session about 13 min (Rolimons); 16-player servers.
- **Loop:** rounds of a few minutes; knock-outs pay coins; coins buy abilities and cosmetic swords and effects.
- **First minute:** you often join mid-round and spectate, which teaches the whole game; the first round uses one button, and the difficulty curve is simply the ball's speed.
- **Money:** passes VIP 240, Double Coins 240, Instant Spin 120, Trading Sign 112 (LF-29). In Oct 2023 a knock-out paid 7 coins and the first ability cost about 300, so 80+ games; about 90% of revenue was reported to come from purchases and premium case rolls (Naavik, unverified).
- **Keeps:** short sessions that fit spare minutes; weekly updates in the launch period; a Discord above 500K members (Oct 2023).
- **Cadence:** weekly at launch; seasonal events now hold a 30-day peak near 27K.
- **Spread:** two finalists trading parries at rising speed is a natural clip; it grew from about 15K to over 100K CCU in three days in Sept 2023, largely through TikTok, with about $1,500 of early ads (Naavik, unverified).
- **Risks:** a slow free earn rate beside purchasable abilities is spending pressure inside PvP; case rolls fall under paid-random-item rules; variable server placement hurt a timing game early; about 98% below peak.
- **Lessons:** (1) one input with rising tempo is the purest onboarding; (2) losses must feel like the player's own mistake: readable tells, timestamped inputs with a capped rewind; (3) effects everyone sees sell cosmetics; (4) in PvP, sell looks, and make abilities earnable at a fair rate with a free rotation; (5) a skill toy without a meta falls as fast as it rose.

### 2.13 Fisch and Fish It (fishing: the original and the simplifier)
- **Is:** cast, play a minigame, catch, sell, upgrade the rod, sail on. Fisch: solo-built, released 5 Oct 2024; 5.07B visits; 57.9K (LF-27), 78.9K (V-7); peaks in the conflict note above. Fish It: created 21 Oct 2024; peak 2,716,766 on 7 Dec 2025 (Rolimons); 58.6K (LF-29), 63.3K (V-7); 82.8% approval.
- **Loop:** Fisch: the starter rod is free with zero stats; the next rods cost 300, 750 and 2,000 cash (guide); the reel minigame is the skill layer and size and mutation rolls the luck layer; weather, time of day and season decide which fish bite; each island has a finite bestiary (16 species on the first, guide-reported). Fish It: click to charge, click quickly; auto-equip, quest arrows, islands close together, "1 in X" odds on every fish, AFK auto-fish (sessions about 30 min, unverified).
- **First minute:** Fisch prints its controls in the store description, so players arrive knowing the verb; first catch in under a minute in both.
- **Money:** Fisch (LF-27): Emote Pack 99, Bobber Pack 99, Supporter 169, Enchant Anywhere 239, Double XP 239, Spawn Boat Anywhere 299, Appraisers Luck 299, Sell Anywhere 399, Appraise Anywhere 499: mostly "anywhere" passes that remove a walk. Fish It (LF-29): Small Luck 50, Extra Luck 245, Advanced Luck 545, More Mutations 295, Sell Anywhere 315, VIP 445, Hyper Pack 999: a luck ladder, plus a gacha and battle pass.
- **Keeps:** a per-zone checklist gives the first session an end; world state as a schedule ("it only bites at night in the rain"); crews and group events (Fish It, 2026).
- **Cadence:** weekly, usually Saturday (guides).
- **Spread:** Fisch proved the genre; Fish It removed friction, displayed odds as spectacle and out-peaked it (2.72M in Dec 2025), climbing during Fisch's weak period. Fishing is up 55% year on year (V-7).
- **Risks:** Fisch's Second Sea (29 Mar 2025) required a high level (200 per Destructoid, 250 per Sportskeeda and PCGamesN), introduced a new currency so everyone restarted, weakened old rods and raised the level cap; players left "by the thousands", an in-game poll drew almost 50,000 voters and a fan wiki says the area was removed on 31 Aug 2025; trading was switched off after that update with no official reason (Sportskeeda); ownership moved to an operator and back within a year (fan wiki). Fish It's luck passes are probability modifiers `[VS]`.
- **Lessons:** (1) put a small skill on top of a luck roll; (2) "anywhere" passes save the buyer a minute and make nobody stronger; (3) never ship an expansion that resets earned progress: let old gear and currency count; (4) poll before you build, not on whether to delete; (5) being first is no moat: a follower that removes friction can take the genre.

### 2.14 Dead Rails (co-op journey survival)
- **Is:** ride a train south through a zombie-infested 1899 desert with friends. Place created 1 Jan 2025 by a studio with many earlier horror games; 6.63B visits; about 93% approval; 16-player servers; 13.4K (LF-29), about 29K (V-7); V-7 calls it "roguelike variety, now niche".
- **Loop:** the train is home, transport and progress bar at once; fuel and supplies force stops; every stop is a group risk decision under a day and night clock (guide-reported); runs can be lost or finished.
- **First minute:** a one-paragraph premise: one goal, one vehicle, one enemy, one instruction (bring friends).
- **Money:** four passes (LF-29): Tommy Gun 175, Mauser C96 148, Sawed-Off Shotgun 148, +5 Storage 95.
- **Keeps:** roles emerge without a class menu (driver, scavenger, defender); distance travelled is the score.
- **Cadence:** not verified; a tracker page showed −38% over 30 days (RoWatcher, undated).
- **Spread:** a large YouTuber's video passed 2M views soon after launch and the recommendation system amplified it; a GameAnalytics essay reads this as distribution mattering more than quality once a threshold is crossed, plus novelty layered on familiar play (search summary). The premise fits one thumbnail and a five-second clip.
- **Risks:** paid weapons shift difficulty for free players in mixed groups; players standing and fighting on a moving platform is a hard physics problem (`physics-and-vehicles.md`); long routes with empty stretches; without a persistent meta the audience drifted.
- **Lessons:** (1) make the base itself the progress display; (2) force stops with a resource and a clock so the group has to decide; (3) a premise that fits one thumbnail is distribution; (4) runs need a meta layer (classes, unlocks) to outlast the wave; (5) give every paid weapon a free path.

### 2.15 99 Nights in the Forest (co-op survival; the most durable 2025 hit)
- **Is:** survive nights around a campfire, rescue four children, reach night 99. Began as a week-long jam in March 2025 and launched after about three months, built by three co-creators plus an artist and an animator in New Zealand (DevForum Creator Spotlight, 2025-10-31); peak about 14.2M (date unconfirmed; V-7 gives 11.2–14.2M); about 250K mid-2026; 158K (LF-27), 221K (V-7); about 90% approval. Best Survival Game, 2026 Innovation Awards.
- **Loop:** by day, chop, loot, craft and explore; by night, return to the fire and defend (cultists from about day 3); feed resources into the fire for a wider safe radius and into the bench for better recipes; rescues need keys from special enemies and fire levels gate them. Meta: diamonds from chests, badges and a repeatable stronghold buy classes from a rotating daily shop (guide, July 2025: 10 to 500 diamonds).
- **First minute:** an axe, a small sack and an obvious task (wood for the fire); the first night falls within the first few minutes; the monster flinches from a flashlight beam. The environment is the tutorial.
- **Money:** one pass on sale, Decorator 199 (LF-27); earlier class passes are off sale; diamonds are sold for Robux and also drop in play. In co-op, bought power helps your own team.
- **Keeps:** every run is a story with an ending; classes make groups want a mix of roles; the fire is a visible, growing progress object.
- **Cadence:** weekly updates, each preceded by a 45-minute "update party" where the developers play with the community and find bugs; three-part seasonal events with their own currency and class.
- **Spread:** a mascot readable at icon size; a scary but funny tone for a broad audience; a film deal and a cross-platform collaboration followed.
- **Risks:** long runs on unstable phones need reconnect or checkpoints; tone against the rating; hundreds of clones carrying the name; content "into the thousands" needs strict mesh and instance budgets.
- **Lessons:** (1) put the first scare inside five minutes and make the safe zone visibly grow; (2) one monster, one tell, one counter; (3) sell roles through a currency that can also be earned; (4) build systems first, then pour content on top weekly; (5) of the 2025 mega-hits, the one built on co-op depth kept the highest floor (above 1% of peak against about 0.1% for Grow a Garden).

### 2.16 Restaurant Tycoon 3 and My Small Business (hands-on tycoon and cozy management)
- **Is:** run a business with your own character, then automate it. Restaurant Tycoon 3: a paid-access beta from 2025 by Ultraw Games, six years after its predecessor; tracker peak 67.4K (RoTrends); 8.0K (V-7). My Small Business: 20.0K with a 44.8–46K peak; 15.2 min sessions (V-7).
- **Loop:** do the job by hand (design, print, pack and ship, or cook and serve), earn within a minute, hire workers, expand the room, idle income. RT3 sends you into the map for ingredients (farmers' market, supermarket, butcher). My Small Business runs offline income and 6–8 player servers with a plot each (V-7).
- **First minute:** hands on a task in a small 3D space; menu-led managers stay under 1K CCU however deep they are (V-7).
- **Money:** cheap repeatable products carry the format: My Small Business has 39; two rivals have no passes at all (V-7). RT3 sells convenience passes such as auto-collect and precision building, none required to progress (search summary).
- **Keeps:** RT3's stated pillars are activity, creativity and depth; staff, merge tiers and an index stand in for pets; a friend boost.
- **Cadence:** RT3 ships updates sometimes several times a week from player feedback, and its team posts at least two short-form videos a week (Creator Spotlight, search summary).
- **Spread:** a sequel audience; price-flip thumbnails; a relatable job.
- **Risks:** decorating raises favourites but shortens sessions (7.9 min in a decorating-led rival, V-7); driving is hard for young players; near-duplicate risk against the format leader (`genres/tycoon-and-cozy-management.md`).
- **Lessons:** (1) the player does the work before a worker does; (2) creativity (layout, menu) gives a tycoon expression as well as numbers; (3) the hiring ladder is this genre's pet collection; (4) repeatable products fit an audience that returns daily; (5) two short videos a week is part of the job.

### 2.17 Tower of Hell (round-based obby)
- **Is:** climb a randomly assembled tower with no checkpoints before the round timer ends. Created 18 Jun 2018; 29.3B visits; 20-player servers; 29.8K (LF-29), 36.3K (V-7); 73.6% approval, the lowest in this file.
- **Loop:** climb, fall, restart from the bottom; a new tower each round from a hand-built section library; coins for progress and finishes; shop gear helps for the current round only.
- **First minute:** the first section is clearable on the first try; then you fall and learn the rule by experience; a visible round timer promises that a bad tower is never permanent.
- **Money:** on sale (LF-29): Haunted Bundle 480, Double Coins 195, Halloween Coils Bundle 90; seasonal bundles rotate. Private-server owners can skip rounds, set tower size and lock the shop.
- **Keeps:** procedural variety from hand-made parts; short rounds reset frustration; mastery as status; faster climbers above you as the tutorial.
- **Cadence:** small, safe drops: a new section or a seasonal bundle (updated 10 Oct 2026).
- **Spread:** "no checkpoints" is a dare, and falling from the top is the most relatable obby clip.
- **Risks:** difficulty divides the audience (see the rating); gear that helps climbing is a soft advantage in a skill game.
- **Lessons:** (1) difficulty can be the brand if rounds are short; (2) hand-made pieces assembled at random give freshness without generated-level quality problems; (3) offer a shop-locked mode for purists; (4) a low rating does not stop visits, but it costs in a system that weighs retention: choose it deliberately; (5) pick an update unit you can ship in a day.

### 2.18 +1 Speed Keyboard Escape (the +1 format with a skill twist)
- **Is:** every step adds speed; more speed makes the keyboard-themed course harder to control. Created 18 Jan 2026; 22-player servers; 96.7% approval on 10M votes; peak in the conflict note above; 25.0K (LF-29), 33.3K (V-7); average playtime about 9 min (Rolimons via The Bloxline). Best Party & Casual Game, 2026 Innovation Awards.
- **Loop:** walk and gain speed, attempt the course, fall, notice you are already faster, finish for Wins, unlock themed worlds; treadmills and equipped trails and auras multiply the gain.
- **First minute:** the counter ticks with a key-click sound from the first step; the course is in view from spawn; failing is itself progress.
- **Money:** 64 passes (LF-29): treadmills 79 to 1,199, trails and auras 19 to 2,999, Wins Multiplier x2 95, More Equipped Items 299, Premium Trade Booth 159, Unlock Soundpacks 85. Almost all fixed-price cosmetics or self-only multipliers; no random items on the list.
- **Keeps:** a personal stat that only rises; world themes that change the title suffix; a full server of trails as social proof; purely comparative competition with nothing harmful.
- **Cadence:** a themed world per major update; a concert during the July 2026 surge (figures unverified).
- **Spread:** the shortest promise on the platform ("always getting stronger"), one sensory theme, launched in the lull after the brainrot wave.
- **Risks:** CCU fell 61.5% from August to September 2026 and the genre is "crowded and fading" (V-7); dozens of near-identical variants; client-reported speed and thin collision at high speed are the standard exploits (`genres/plus-one-evolution.md`).
- **Lessons:** (1) let the stat feed back into difficulty so the number never trivialises the game; (2) a 19-to-2,999 cosmetic ladder gives every budget a purchase without random items; (3) add a movement rule per world, not a bigger number; (4) short sessions suit a system that credits at most 60 minutes per player per day `[official]`; (5) a format game needs its next verb before the clones finish copying the last one.

## 3. Cross-game patterns, ranked

Count = teardowns above (of 18) where the cited evidence shows the pattern. Absence means "not evidenced", not "absent". Codes: GaG, SaB, SAE, PS99, BF, BH, AM, DO, DTI, BSS, TD, BB, FI, DR, 99N, CM (§2.16), ToH, +1.

| # | Pattern | Count | Games | Use it as |
|---|---|---|---|---|
| 1 | The core verb is performed in the first two minutes with no tutorial screen | 14 | GaG SaB SAE PS99 BF BH AM DO BSS BB FI 99N ToH +1 | A gate: no screen before the first action |
| 2 | Other players are the show: visible plots, status, demonstrations, judges | 12 | GaG SaB SAE PS99 BH AM DTI BSS BB CM ToH +1 | Server size and sight lines are design choices |
| 3 | The visible store sells time, capacity, cosmetics or control, not power over others | 11 | SAE BH AM DO DTI BSS FI(Fisch) 99N CM ToH +1 | The default store shape under house rule 3 |
| 4 | All-time peak to current level is a fall of 85% or more | 10 | GaG SaB SAE BF AM DTI BB FI 99N +1 | Budget for the floor, never the peak |
| 5 | A collection with rarity tiers is also the multiplier or the key | 10 | GaG SaB SAE PS99 BF AM BSS TD FI +1 | Make every duplicate useful (fusion, mutation, map key) |
| 6 | A fixed weekly (or faster) update slot | 9 | GaG SaB SAE PS99 BH BB FI 99N CM | Pick a weekday you can keep; biweekly kept beats weekly missed |
| 7 | A shared clock everyone can see (restock, stock, round, weather, day and night) | 9 | GaG SaB SAE BF DTI FI DR 99N ToH | Derive it from server time so all servers agree |
| 8 | The record came on a scheduled event, crossover, big update or holiday | 8 | GaG SaB SAE BF BH AM DTI BSS | Treat event days as launches: flags, load tests |
| 9 | Originated with a team of five or fewer (SaB's figure is an unverified analyst post) | 7 | GaG SaB BH BSS BB FI 99N | Scope is not the barrier; operations after breakout are |
| 10 | Sessions end in an arc (run, round or match) | 7 | DO DTI TD BB DR 99N ToH | Gives a reason to restart and a clip |
| 11 | Loss or danger with a visible counter | 7 | SaB SAE DO BB DR 99N ToH | Timer, tell, safe line or short round for every loss |
| 12 | Tradable rares brought real-money resale, scams, dupes or a trading shut-off | 4 | GaG PS99 AM FI | Gate trading by progress; ship it last |
| 13 | Monetisation drew press or analyst criticism | 4 | GaG SaB PS99 BB | All four sold power over others, paid luck or paid PvP abilities |
| 14 | Lobby place plus separate run or match places | 3 | DO TD 99N | Party in the lobby, sell before the run |
| 15 | Offline progress as the stated promise | 2 | GaG CM | Strong for idle and management, not universal |
| 16 | Forced change over IP | 2 | SaB BF | Original names and characters from day one |

Reading: patterns 1–3 are close to table stakes; 4 is the honest shape of success; 13 lines up with the stores house rule 3 already forbids. The vault's 14-pattern list (`market-scan-2026-11.md`) was coded from current trend hits; this count spans evergreens too, which is why offline income ranks low here and high there. Approval loosely follows tension `[lihfolk]`: 73.6% for Tower of Hell, 79.2% for a 100-player elimination game, 83.1% for a hazard-run brainrot game and about 85% for SaB, against 95–97% for BSS, PS99, +1 and Anime Vanguards. Fish It (82.8%) is a calm game that breaks the rule, so treat it as a tendency; none of it stopped visits.

## 4. Failure studies

| Case | What happened (source, date) | Cause class | Early signal | Prevention |
|---|---|---|---|---|
| Theme-only clone waves | 21 brainrot spin-offs at a median 8.4K CCU; of 40 "Steal a" results 7 above 10K; standalone RNG games fall under 3K fast; dozens of "+1 … Escape" variants (V-7) | Clone fatigue | Parent's 30-day peak under about 10% of all-time; your pitch needs the parent's name | A new verb, own art and place file; see §5 |
| Plants vs Brainrots | 8.65M peak on 11 Oct 2025 (Rolimons) to 2.5K (LF-29) | Loop loyalty, not title loyalty | Each event peak lower than the last | A mechanic per major update; plan the floor |
| Kick a Lucky Block; Animal Hospital | 1.7M (23 May 2026) to 13K in about five months (V-7); Animal Hospital peaked at 0.56–1.3M (sources conflict), won Best New Game and three more awards on 12 Sep 2026 (Roblox newsroom, search summary) and sits at 18–21.5K (V-7; RoWatcher) | Single gimmick | Session length shrinking; the second week of play repeats the first | A meta loop before launch; a second verb by week 4 |
| The Forge | About 1.05M (Dec 2025) to 3.2K (Oct 2026) (Adellion via LihFolk); one blog says updates stopped and communication went quiet (Roonby, 2026-07; single weak source) | Update drought | No update stamp for weeks; silent community channels | A cadence you can keep; say when the next update is |
| Fisch, Second Sea | See §2.13: level gate, new currency, weaker old gear, higher cap, then polls and removal | Progress reset | Design doc contains "new currency" and "old items rebalanced" together | Old progress counts; staged rollout; concept poll first |
| Blox Fruits and DOORS gaps | About −40% in 30 days between updates; Floor 2 after two years, coolly received | Long silent gaps, over-teasing | Teasers without dates | Small dated events between large updates; announce what you can date |
| Grow a Garden | Event fatigue by Aug 2025; paid crop steals; more than 99.8% below peak | Treadmill without depth; pay-to-interfere | "Repetitive" in feedback; refund and parent complaints | Systems before content; nothing bought can take from a player |
| Steal a Brainrot | Character pulled Sept–Nov 2025 (licensing); automation scripts; 85% approval | Borrowed IP; client trust; paid power over others | A meme creator or agent surfaces; scripted steals | Own characters; server-validated steals; no paid weapons |
| Steal An Egg | Offline for a few hours on 24–25 Aug 2026; a video-feed panel was gone on return (allthings.how; no official statement) | Risky feature | A feature outside the tested content rules | Review anything that streams or embeds external media |
| Toilet-themed tower defence | The category leader was reported taken down after a copyright complaint from the source series' creator (guide sites; cause and date unconfirmed) | Whole game built on someone else's IP | The title contains another property's name | Format yes, names and characters no |
| Dress to Impress | Three-hour code item crashed the game (Dec 2024); live event criticised (2025) | Load spike on a timed drop; over-promise | A single redeem window for the whole audience | Stagger, queue, load-test; describe events exactly |
| Pet Simulator X | NFT purchases refunded (Feb 2023); duped currency reverted and accounts banned (BIG Games post) | Real-money adjacency; dupes | Items gaining cash value off-platform | Session-locked atomic trades (`data-and-purchases.md`); no cash-value features |

Dupe incidents: this pass found no verified 2025–26 case of a top game's economy collapsing from duplication. Search results are dominated by scam "dupe script" pages, which are themselves a threat to your players. The risk is still real wherever items trade (pattern 12).

Level-up: symptoms → likely cause → fix

| Symptom on your live game | Likely failure class | First fix |
|---|---|---|
| CCU halves within 3–4 weeks of each update | Content treadmill without depth | One system with long goals (collection, fusion, roles) before more content |
| Rating sliding under 85% | Loss without counterplay, or pay-to-interfere | Lock timers, grace periods, remove paid harm |
| Spike on update day, then a crash and data errors | No load plan | Flags, staged rollout, queue the hot remote (`engineering-architecture.md`) |
| Veterans quit after an expansion | Progress reset | Restore the value of old gear; convert, never delete |
| Impressions fall while metrics hold | Near-duplicate metadata | Unique title, thumbnails and place file (`analytics-and-discovery.md`) |

## 5. Trend-chasing vs evergreen

The vault's lifecycle model (inference, V-7): a mega-hit peaks 7–8 weeks after launch, holds 2–5 months on weekly updates, then falls 90–99% to a 50–300K floor; a format hit peaks at 0.5–4M and loses 90%+ in 1–4 months; a clone that ships during the parent's rise can pass 1M (Break and Steal an Egg: launched about 6 weeks in, 1.31M peak, 129K now); a clone after the peak settles at 4–32K; a remix with a new action reaches 0.4–5M; durable games are co-op or skill-based with real depth.

**Conflict:** the vault puts the clone window at 2–8 weeks into the parent's rise; LihFolk derives 2–6 weeks. Both are inferences from the same public curves and nobody has measured it. Use "inside the first two months of a visible rise, earlier is better", and do not treat either number as a deadline you can plan to the day.

| Question | Trend remix | Durable or evergreen |
|---|---|---|
| What you are betting on | An audience already loyal to a loop | A fantasy and depth that outlast a wave |
| Build time under house rules | Weeks, only with your own format kit (below) | Months |
| Typical session (trackers, unverified) | 9–16 min | 25–48 min |
| Expected life | Weeks to a few months; a floor of 1–10% of peak if you keep updating | Years, with event swings of 2–5× |
| What decides it | Timing, one new verb, first minute, weekly events | Meta loop, co-op or skill depth, cadence kept for 6+ months |
| Main risks | Missed window; near-duplicate deprioritisation; lawsuits over copied UI and art; clone below you within weeks | Slow start; cadence burnout; one bad expansion |
| Evidence in §2 | SAE, +1, Fish It (out-peaked the original) | 99N, BF, BH, BSS, Fisch, Anime Vanguards |

Honest risks of a fast clone:

- **You are probably late.** By the time a trend is obvious on the charts, the leader has months of content. Followers that were not first or second peaked one to two orders of magnitude lower `[lihfolk]`.
- **The platform filters copies.** Games whose metadata and place files closely resemble existing games are no longer prioritised for recommendations `[official]`; Roblox's own advice is to add your own spin.
- **Copying expression is the legal risk.** Mechanics are generally free to use; UI layout, art and names are what the Steal a Brainrot owners sued over (at least four suits since Nov 2025, Bloomberg via The Star). Not legal advice.
- **New games reach older players first.** The 250-play gate before Kids and Select audiences `[VS]` (`market-scan-2026-11.md`) puts weeks between a launch and the core 9–15 trend audience.
- **House rules make a 7-day clone impossible.** **Conflict:** LihFolk's trend-game skill plans a 7-day build from reusable templates and its own asset pack. Under house rule 1 every visible asset is authored in Blender with real collision, so that plan does not apply here. `[house]` The compliant version is a **format kit** built before any trend: your own server-authoritative codebase (plots, income per second, rarity tables, rebirth, timers, receipts) and your own Blender kit (plot, pads, pedestals, UI frames, VFX). A remix is then a new verb, a new theme mesh set and tuning, not a new game.
- **Spikes with short sessions fade fastest.** Approval of 90%+ with 25–30 min sessions predicted longevity better than spike size (Adellion via LihFolk, `[community]`).

Decision rules:

1. Chase a trend only if all four hold: the parent is still rising and under about 8 weeks old; you can state one new verb in a sentence and show it in the thumbnail; your format kit makes a playable build possible in about 2 weeks `[house]`; you have a plan for the first 250 engaged 16+ plays.
2. If the parent has peaked, do not reskin. Either remix the loop with a new verb for the same audience (Escape Tsunami about 5M; Steal An Egg 14.3M a year after the original) or go durable.
3. Choose durable when the team can keep a cadence for six months and the idea has co-op roles, skill, or a collection deep enough to survive a month without content.
4. Whichever you choose, write the floor plan now: what the game is at 5% of its peak, and whether that still pays for weekly updates.
5. Never use another property's characters or name, a competitor's UI layout, or a title built from a competitor's name.

## 6. Level-up: use a teardown to fix your own game

1. **Pick the comparison set** (§1.1): the games your players would otherwise be in. Check Creator Analytics → Acquisition → Home Recommendations for the similar experiences Roblox groups you with `[official]` `[VS]`, and add up to nine to a watchlist.
2. **Run the same protocol on all of them and on your own game** (§1.3), on the same phone, with fresh accounts, in one sitting per game.
3. **Build the gap table.** Rows: seconds to control; seconds to first action; seconds to first reward; pop-ups in the first 3 min; minute of first purchase prompt; loop length; minute of first wall; cheapest item; number of items under 200 R$; update weekday; days since last update. Columns: each competitor, then yours. The first-minute gap is usually larger and cheaper to close than any content gap `[lihfolk]`.
4. **Sort every gap into one of five bins:** table stakes you lack; first-minute fixes; store and price shape; cadence and timing; a gap nobody fills (your positioning). Discard anything that fails §1.5.
5. **Write at most five changes**, each as: change → metric it should move → size of the move you expect → how you will measure it. Route them: loop changes to `core-loop-tuning.md` §5–6, store changes to `monetization-and-policy.md`, cadence to `liveops-quests-retention.md`, everything through the safe-change protocol in `audit-existing-game.md` §7.
6. **Ship behind a config or experiment**, one change per metric, never on the leader's update day.
7. **Re-run the stopwatch on your own game two weeks later** and update the table. Repeat quarterly; the leaders will have moved.

| Symptom in your game | Study these teardowns | Look at |
|---|---|---|
| High first-play bounce, low D1 | §2.1, §2.3, §2.12, §2.18 | Seconds to first action and reward; what the spawn point shows |
| Sessions under 10 min | §2.15, §2.11, §2.10 | Run arcs, mode ladders, quest lines |
| D7 collapses | §2.5, §2.13, §2.4 | Shared stock clocks, world state, rank goals |
| Store ignored | §2.6, §2.18, §2.13 | Entry items under 200 R$, cosmetic ladders, "anywhere" convenience |
| Rating under 85% | §2.2 vs §2.3, §2.17 | Where loss has no counter; what is sold against players |
| Spike then crash on updates | §2.5 vs §2.6 | Big-and-rare vs small-and-weekly |
| Nobody plays together | §2.8, §2.9, §2.15 | Walk-in parties, peer judging, complementary roles |
| Trading scams, inflation | §2.7, §2.4 | Trade gating, warnings, fusion sinks |

## Review gate

- [ ] Every number in the teardown has a source, a date and an hour or "snapshot" label; conflicts are stated, not averaged.
- [ ] The first ten minutes were played first-hand on a phone with a fresh account and a stopwatch; nothing was exploited or decompiled.
- [ ] All seven maps are filled; developer-product prices were recorded in-game, not assumed.
- [ ] Copy / change / avoid is written, and nothing in "copy" is a name, character, UI layout or asset.
- [ ] Nothing adopted sells power over other players, paid luck as the top of the store, hidden spend tiers or progress resets.
- [ ] A trend decision passes all four tests in §5 rule 1, with one new verb and Blender-authored art; otherwise the plan is a remix or a durable game.
- [ ] The floor plan exists (the game at 5% of peak).
- [ ] The output is at most five changes, each tied to a metric and shipped behind a config or experiment.
- [ ] The same protocol is scheduled again after the change and each quarter.

## Sources

Accessed 2026-11-10. Direct fetching of news, tracker and forum sites was blocked in this session; those entries are WebSearch summaries only.

- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `32 Case Studies of Top Roblox Games/` (Start Here; Case Study - Grow a Garden, Steal a Brainrot, Pet Simulator 99, Blox Fruits, Brookhaven RP, Adopt Me, Doors, Dress to Impress, Fisch, 99 Nights in the Forest, Dead Rails, Tower Defense Simulator); `59 Viral and Trend Game Teardowns/` (Start Here; Viral Game Anatomy - Hooks, Loops and Timing; Teardown - Steal An Egg, +1 Speed Keyboard Escape, Bee Swarm Simulator, Tower of Hell, Sol's RNG, Fish It, Plants vs Brainrots, Escape Tsunami for Brainrots, Ink Game); `60 High-Craft Game Teardowns/` (Start Here; What Craft Looks Like on Roblox; Teardown - Blade Ball, Anime Vanguards); `27 Marketing and Growth/Competitor Analysis Method.md`; `skills/roblox-trend-game/SKILL.md` and `references/trend-games-research.md` (read)
- Owner's vault: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/index.md (read; watchlist of nine games, public stats shown, 100+ DAU benchmarks)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md (read; first-play bounce, 60-minute playtime cap, non-unique games, "add your own spin")
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/performance-optimization/identify.md (read; Shift+F5, Performance Stats)
- https://gamesbeat.com/janzen-madsen-interview/ (search summary; Grow a Garden origin and growth)
- https://www.thestar.com.my/tech/tech-news/2026/03/25/robloxs-hit-game-steal-a-brainrot-battles-its-many-imitators (search summary; Bloomberg story: lawsuits, $64M spend estimate)
- https://www.pcgamer.com/games/a-brainrot-themed-roblox-game-is-taking-a-brainrot-themed-fortnite-game-to-court-for-being-a-copy/ (search summary)
- https://allthings.how/steal-an-egg-roblox-ban-why-it-happened-and-how-it-returned/ (search summary; 24–25 Aug 2026 removal)
- https://devforum.roblox.com/t/creator-spotlight-the-story-behind-99-nights-in-the-forest/4036940 (search summary)
- https://devforum.roblox.com/t/creator-spotlight-how-ultraw%E2%80%99s-love-for-food-became-a-trending-tycoon/3840933 (search summary; Restaurant Tycoon 3 pillars, cadence, video output)
- https://rotrends.com/game/7094518649/Restaurant-Tycoon-3 (search summary; tracker peak)
- https://about.roblox.com/newsroom/2026/09/2026-roblox-innovation-awards and https://www.pockettactics.com/roblox/innovation-awards-2026 (search summary; 2026 winners)
- https://www.netinfluencer.com/roblox-crowns-animal-hospital-sweep-at-2026-innovation-awards/ and https://rowatcher.com/games/10148749921/animal-hospital-anomaly (search summary; awards, peak and decline)
- https://destructoid.com/roblox-fisch-second-sea-removed, https://www.sportskeeda.com/roblox-news/why-trading-disabled-fisch-possible-reasons-explored, https://progameguides.com/roblox/cursed-seas-or-cursed-update-the-future-of-fisch-second-sea/ (search summaries; Second Sea backlash, polls, trading disabled)
- https://www.gameanalytics.com/blog/dead-rails-and-the-hit-makers-formula and https://rowatcher.com/games/7018190066/dead-rails/dying (search summaries)
- https://rowatcher.com/news/pet-simulator-99-inside-roblox-s-most-aggressive-monetization-machine and https://www.biggames.io/post/pet-simulator-x-hellish-update (search summaries)
- https://rowatcher.com/games/994732206/blox-fruits/dying and https://rowatcher.com/news/blox-fruits-vs-sailor-piece-which-anime-rpg-is-actually-growing-faster-in-2026 (search summaries; −40% over 30 days, update cycle)
- https://rowatcher.com/news/bee-swarm-simulator-how-one-developer-built-a-roblox-empire-that-won-t-quit (search summary)
- https://rowatcher.com/news/sol-s-rng-and-the-luck-based-game-craze-why-players-keep-rolling (search summary; RNG clones fade within months)
- https://roonby.com/2026/07/10/9-roblox-games-that-are-big-and-flop-downfalls-of-the-most-popular-games/ (search summary; The Forge, single weak source)
- https://gamertweak.com/what-happened-toilet-tower-defense and https://www.game.guide/why-was-toilet-tower-defense-deleted-on-roblox (search summaries; reported takedown, unconfirmed)
- https://app.mergerlinks.com/transactions/2025-02-04-brookhaven (search summary; acquisition)
- No evidence found: a verified 2025–26 dupe-driven economy collapse in a top game; an official explanation for the Steal An Egg removal; session agendas or post-mortem talks from RDC 2026; developer-authored post-mortems for Doors, Dead Rails, Blade Ball or Dress to Impress.
