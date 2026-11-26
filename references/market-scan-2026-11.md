# Market scan, November 2026 (what to build and how to get seen)

Two snapshots. **7 Nov 2026** `[VS]`: the owner's research, i.e. the Nov 2026 bundle (`roblox-market-research-2026-11.zip`, byte-identical to the vault's `_raw/` folder) and the v2 report "Roblox Market Research v2 — Nov 2026 (Detailed)" (Claude Doc, https://claude.ai/artifact/WkBA2wVEVauiMCHgy1CSKA), taken Saturday 7 Nov at 09:40–11:00 UTC; a converted copy of the report is in `references/market-research-v2-raw.md` for grep, and the full note set is in the vault at `C:/Users/Nebula PC/Documents/Delta Vault/Roblox Research/2026-11 Market Scan/` (`_MOC.md`, then `_AGENTS.md`). **26 Nov 2026**: a refresh from Roblox's public chart, games and search APIs pulled Thursday 26 Nov (US Thanksgiving) at 10:02–10:20 UTC and again at 11:00 UTC, plus Rolimons peak counters, Roblox's Q3 2026 shareholder letter, YouTube search and press (Sources); these pulls are summarised here. Both main pulls are pre-US hours, but a Thursday is not a Saturday: in October 2026 a weekday averaged about 0.67× a weekend day (Bloxodes), so a game at 0.67× its 7 Nov number has held and one under about 0.35× has really fallen. CCU swings 2–3× by hour, and event days run 3–45× the off-peak. `fact` = sourced or measured, `inference` = our reading.

## Start here by level

| Level | Do this | Ignore for now |
|---|---|---|
| Beginner | Read "The shape of the market", "Waves since 7 Nov" and the 14 shared patterns; pick a format that is rising or open, not saturated, or start from the Idea bank; name your one new action. Follow thumbnail rules 1–5 | Gap scores, feed statistics, the 100-play gate detail |
| Intermediate | Check your design against all 14 patterns and the format norms for your genre (then open the matching file in `genres/`); fill all thumbnail slots (rules 6–13); plan the 16+ first launch and a Saturday or seasonal date | — |
| Expert | Read the discovery facts as ranking signals to instrument (analytics-and-discovery.md); time a format entry against the parent's wave (2–8 weeks into its rise); judge a game by its 24 h and 7-day peaks at a fixed UTC hour, never by one snapshot | — |

Related: genre-playbooks.md and `genres/` turn these norms into build plans; case-studies-teardowns.md explains why the hits work; analytics-and-discovery.md and growth-and-marketing.md own discovery mechanics and launch marketing; monetization-and-policy.md owns prices; liveops-quests-retention.md owns seasonal events and updates.

## The shape of the market

- **Who leads (Thu 26 Nov, 10:04 UTC):** Steal An Egg 706K (24 h peak 847K, 7-day event peak 6.9M, October average 1.28M), then 11 games at 66–213K: Blox Fruits, Brookhaven, Throw Food For Animals 168K, 99 Nights, Adopt Me, RIVALS, Anime Crusaders X 105K (anniversary update), Pet Simulator 99, Anime Adventures, Fish It, MM2. The top 100 by CCU held 3.86M. On 7 Nov about 18 games sat at 60–440K. An hour later (11:00 UTC) the top 100 held 4.05M (+5%: Adopt Me +16%, Brookhaven +13%, Blox Fruits −13%). US afternoons reorder the top: on 18 Nov at 21:37 UTC GGRecon read Steal An Egg 454K, Brookhaven 291K, Adopt Me 286K and Throw Food For Animals 185K, so Steal An Egg peaks outside US hours and Brookhaven and Adopt Me inside them. `fact`
- **Churn is the norm:** 30 of the top 100 were created in October or November, 12 of them in November; GGRecon counted 30 of 99 on 18 Nov. Roblox says about 40% of the weekly Recommended For You top 100 by impressions were created in the previous three months `[official]`. A format hit now holds the chart for 1–3 weeks: Steal A Balut 99K peak (about 19 Nov) → 6.8K, Cat Battles 100K (24 Oct) → 1.3K, My Small Business 44.9K (about 5 Nov) → 1.0K. Across 38 mid-tier games named on 7 Nov the median kept 0.27× of its CCU by 26 Nov, against 0.63× for pre-2026 games (`case-studies-teardowns.md` §4). `fact`
- **The spine is unchanged:** a stat or income per second → multipliers from a collection (pets, staff, fruits, plants) → rebirth, plus **one new action or a visible journey**. The 26 Nov breakouts add one: **distance = luck**, where how far you throw, cast or shoot sets the zone and the rarity (Throw Food For Animals, Throw a Seed, Shoot Arrows For Animals). Remixes with a new action still beat reskins; a number ticking up on a menu is not fun to watch, a visible trip is. `inference`
- **Waves:** a mega-hit peaks 7–10 weeks after launch (Steal An Egg 14.31M 8 weeks after creation; Throw Food For Animals 2.45M after 9 weeks, on an event day), plateaus on weekly updates and events, then falls 90–99% to a floor. Single-gimmick hits lose 90%+ within 1–4 months; +1 and egg-journey hits fell 84–95% from their peaks within 2–6 weeks (24 h peak against all-time peak). A clone wins only if it ships 2–8 weeks into the parent's rise: Throw a Seed was created 7 weeks into Throw Food For Animals' rise and peaked at 172.9K 15 days later. `fact` for the numbers, `inference` for the rule.
- **Rising:** throw-for-distance collecting, ragdoll and crash physics, physics sports, co-op journey survival, cleaning jobs, ape-chase horror, job sims with a hands-on craft verb. **Fading:** the +1/evolution middle tier, "___ For Eggs" journeys, "Steal a ___" (3 of 40 search results above 10K, down from 7), liminal horror, theme-only brainrot, the 7 Nov cozy-management leaders. **Open:** Christmas and snow, warehouse and delivery, ragdoll progression. Detail in the next section.
- **The platform shrank and aged:** Q3 2026 daily users 138M, down 9% year on year (the first annual fall), hours down 15%; over-18s are the fastest-growing cohort (29% of age-checked daily users, 37% in the US) and in the US spend 50%+ more than under-18s; Q4 bookings are guided down 10–15%, assuming a seasonal fall in daily users from Q3 `[official]`. `inference`: design for 13+ and co-op as well as for kids; a trend audience is smaller than in 2025.
- **Seasons:** the December peak is 20 Dec–4 Jan: over 22 established games last winter it ran at a median 1.57× mid-November CCU while 1–19 Dec sat at 0.95×, and Halloween events lifted daily peaks a median 2.05× on each game's event weekend (`references/liveops-quests-retention.md` §Holiday season 2026–27 calendar, measured 26 Nov; the 7 Nov report's 1.8–2.5× players and 2.5–3.5× revenue were not confirmed). Roblox says a significant share of Q4 bookings arrives in the last week of December `[official]`. Launch on a Saturday or a holiday.

## Waves since 7 Nov (26 Nov 2026)

"Now" is Thu 26 Nov 10:04 UTC; peaks are Rolimons counters read about 10:30 UTC; clone counts are the first 40 Roblox search results for the format's words, as on 7 Nov. `fact` unless marked.

| Format | Parent and leaders (created; now; peak) | Clones on 26 Nov | Status |
|---|---|---|---|
| Throw, cast or shoot for distance, collect animals | Throw Food For Animals (18 Sep) 168K, all-time peak 2.45M about 22 Nov; Throw a Seed (7 Nov) 35.5K, peak 172.9K; Shoot Arrows For Animals! (5 Nov) 29.4K, peak 68.8K on 25 Nov; Fish For Sea Animals (31 Oct) 29.1K; Fish for Secret Animals! (2 Nov) 16.5K; Cast For Fish! (10 Nov) 14.1K; Throw a Friend for Monsters (3 Nov) 10.0K | "for animals": 6 above 10K, 13 at 1–10K; "throw": 5 above 10K, 10 of 40 created since 7 Nov | Rising and crowding. The parent is 10 weeks old, so the 2–8 week clone window has closed; a new entry needs its own verb and setting. Build plan: `genres/throw-for-distance.md` |
| Ragdoll and crash physics | Hyper Realistic Ragdoll (29 Oct) 54.5K, peak 201K about 19 Nov, 1 player per server, 19.4 min; BloxNG crash physics (13 Oct) 21.0K, peak 61.2K; Realistic Ragdoll MMA 11.0K; Mechs vs Kaiju's Ragdoll 10.8K | "ragdoll physics": 4 above 10K, 17 at 1–10K, 36 of 40 created since 1 Oct | Rising; sandboxes crowded. Progression hybrids are thin: Defeat Ragdolls for Powers! (6.0K) is the best. Blood labels narrow the audience; one YouTuber reports removals (unconfirmed) |
| Physics sports | Ragdoll Soccer (13 Oct) 18.5K, peak 87.6K, 9.6 min; Volley Bomb (1 Nov) 9.2K; Slap Volleyball! 7.8K; Practical Basketball 16.6K (Top Earning #8) | Turbo Soccer 5.2K (peak 38.4K) | Rising: Sports & Racing weekly average 249K → 313K from August to October (Bloxodes); sessions short |
| Co-op journey survival ("N miles / days / nights") | 99 Nights (2025) 152K; 100 Miles Down the River (12 Oct) 23.8K, peak 91.4K, 18.6 min, 20 per server; 100 Days at Sea 14.6K; Stay the Night 11.9K; 13 Days to Escape 8.8K | "days": 2 above 10K; "nights": 99 Nights and Stay the Night above 10K, the rest under 3K | Rising: one leader per fresh setting |
| Cleaning and ASMR jobs | Clean The Ballpit! (31 Oct) 16.7K, peak 46.9K, a new map every 2–4 days; Clean The Bugs 6.4K; Clean Everything 4.5K | "clean": 1 above 10K, 34 of 40 under 1K | Short waves: Sweep The Moon 53K in the week of 2 Nov (RoWatcher) → 4.3K |
| Ape and monkey chase horror | Lethal Ape Experience 18.1K (peak 31.8K); Fatal Baboons 10.1K; Fatal Apes 9.9K; untitled monkey game (17 Nov, arms-only movement) 9.5K | "monkey": 4 of 40 created since 7 Nov | Forming; YouTube-led (next sections) |
| Job sims with a hands-on craft verb | Warnetopia: Internet Cafe (5 Nov) 12.4K; Barber Empire (31 Oct) 11.5K; Build a Bakery 9.8K; My Cookie Factory 8.0K; Run a Christmas Tree Lot (4 Nov) peak 37.6K | "run a": none above 10K | Each theme leads for 2–4 weeks, then the next takes over |
| Cozy management, the 7 Nov leaders | My Small Business 20.3K → 1.0K; Sell a Million Sushi 12.9K → 4.0K; Run A Farm! 10.2K → 3.0K; LINE UP! 11.7K → 6.9K | "sell a million": 33 of 40 created since 1 Oct; the best "Sell a Million" title has 4.0K | Leaders faded; the format lives on through new themes |
| +1 / Evolution | +1 Venom Evolution 46K → 8.5K (peak 102K about 12 Nov); +1 Spider Arm 30K → 2.1K; Bug Evolution 29K → 2.0K; Ant Evolution (28 Oct, grow a body in a 3D world) 12.9K, peak 65.9K | "+1": 1 above 10K (Keyboard Escape), 16 at 1–10K | Cooling; the fresh form is a body you grow and steer |
| "___ For Eggs" journeys | Bike For Egg! 38K → 6.6K; Climb For Animals Eggs 26.8K → 9.5K; Ride An Egg 15K → 1.4K | "for eggs": the 3 above 10K are steal and throw games | Fading |
| Steal a ___ | Steal An Egg 1.14M → 706K; Break and Steal an Egg 129K → 58K; Steal a Brainrot 103K → 24K (7-day event peak 722K) | 3 of 40 above 10K (7 on 7 Nov) | Saturated and contracting; the leaders live on weekly events |
| Liminal and anomaly horror | DONT SPLASH 80.5K → 12.2K (peak 167K about 5 Nov, 7.5 min sessions); Animal Hospital 8.9K | "anomaly": none above 10K, 10 at 1–10K | Fading; long tail |
| Brainrot as a theme | Steal a Brainrot only | "brainrot": median 211 CCU | Dead as a theme (`inference`) |
| Christmas and snow | No leader | "christmas": best 2.4K; "snowball": all 40 under 100 CCU, 12 created since 7 Nov; sled, snow-globe and gift-wrapping games: best under 1K | Open; winter updates usually start in early December |

## Holiday season so far (26 Nov 2026)

- **Thanksgiving:** 12 of the top 100 carry a Thanksgiving tag (318K CCU, 8% of the top-100 total): Pet Simulator 99 [TURKEY], Fisch [FISCHGIVING], Evade, Dress To Impress [SALE], Cameraman TD, Practical Basketball, Hypershot, BedWars and others. 7 still carry Halloween tags (211K) 26 days after Halloween (rule 9); none carries a winter tag yet. `fact`
- **Roblox's own event:** The Great Build (Roblox Presents, 25–30 Nov: a free gratitude block every hour, stacked into one shared tower) had 44.9K CCU on day 2, #2 on Top Trending and #1 on Up-and-Coming; YouTube guides to its 10 prizes reached 85–129K views within 15 h. No platform-wide December event is announced; there are leak videos only. `fact`
- **Event weeks dwarf the off-peak:** 7-day peaks were 99 Nights 1.40M, Adopt Me 801K, Dandy's World 789K (around its 1.0 update; Top Trending #1, Top Earning #2), Steal a Brainrot 722K and +1 Speed Keyboard Escape 636K, against 14–156K on Thursday morning. `fact`
- **Christmas has no leader:** the seasonal breakout so far is Run a Christmas Tree Lot (37.6K peak about 22 Nov). `inference`: a winter game out by about 12 Dec meets an empty shelf; a Christmas-only theme dies on 26 Dec, so pick a winter theme that runs into February. Event and update planning: `references/liveops-quests-retention.md`.

## Off-platform signals (26 Nov 2026)

YouTube search with the "this week" filter on 26 Nov, views at read time (`fact`, search). TikTok and X could not be measured from this environment, so those lines are third-party or `inference`.

| Format | Evidence | Reading |
|---|---|---|
| Ragdoll physics | Foltyn, "This Roblox Ragdoll Game Is DIABOLICAL..", 2.0M views in 7 days; KTG Gaming 334K; 10+ ragdoll videos above 25K | Rising: the clip format of the month |
| Throw or shoot for animals | "Roblox Throw Food For Baddies" (FoltynPlays) 1.0M in 4 days; RoBros on Throw Food For Animals 385K; "Shoot animals with arrows" 100K in 10 h | Rising; the big channels have moved on to the clones |
| Co-op journey | 100 Miles Down the River: five videos at 115–300K | Rising |
| Ape and gorilla chase | "Gorilla Tag monsters…" (Tyler & Snowi) 1.94M in 5 days; "become every monkey" videos 52–123K; monkey Shorts 1.2–2.2M | Rising, Shorts-led (`inference`) |
| Cleaning | "I Must Clean Up EVERY BALL in Roblox" 688K; a Clean the Moon video 228K | Short spikes |
| Steal a ___ | Daily admin-abuse and owner-command videos at 63–165K | Alive on events, not growing |
| +1 / every second | Best video this week 47K | Cooling |
| Grow a Garden | 3–14K per video; leak videos of a winter pass (rumour) | Fading |
| Brainrot | Italian brainrot's creators called it over in Dec 2025 (RoWatcher, search); a third-party report rates brainrot meme edits as TikTok's highest-engagement Roblox format, favouring ragdoll and chaotic physics (RoLearn, 24 Oct 2026) | Dead as a game theme, alive as an editing style that favours physics games (`inference`) |

## The 14 shared patterns (use as a design checklist)

1. Stat or income per second → multipliers → rebirth.
2. One new action on top of the idle core. The 26 Nov breakouts keep the idle core and change only the launching verb: throw, cast, shoot.
3. A visible journey beats a number on a menu. Its newest form is distance = luck: how far the throw flies sets the zone and the rarity.
4. The collection is the multiplier: 4–5 items per egg or tier, top item about 0.1% (Throw a Seed: 75+ plants across 10 rarities).
5. Merge or fuse tiers (3 into 1, 4 into 1) reuse assets for more rarity levels.
6. Timers everywhere: spawns every 5/15/30 min, restocks, daily shops, weekly boutiques.
7. Offline progress, capped and stated, gives a reason to return tomorrow.
8. Weekly updates on a fixed day; most all-time CCU records land on update or event days. Short-wave formats update faster: Clean The Ballpit! shipped a new map every 2–4 days.
9. Live events are the biggest single lever (admin events, concerts, crossovers). The weekly event peak now runs 3–45× the off-peak: Steal An Egg 6.9M against 706K, Throw Food For Animals 2.45M against 168K, Steal a Brainrot 722K against 24K (26 Nov).
10. Loss aversion through theft drives sessions and defence spending but brings cheating and bad press; the steal format itself is contracting.
11. Loop games sell dev products, not passes: Venom 36 products, Gun Forge 123, My Small Business 39 (7 Nov); Steal An Egg, Throw Food For Animals and Shoot Arrows For Animals list 2 passes each and Break and Steal an Egg none (26 Nov). Sandboxes and job sims without a currency loop sell content passes instead (Hyper Realistic Ragdoll 17, Barber Empire 18, BloxNG 13). Repeat spending feeds the spend-days signal.
12. Playable within a minute, no long tutorial.
13. Free boosts for social actions: like + favourite + group join bonus, friend boost +10–20%, private servers. (House rule: bonuses only, never a gate, never in the title, thumbnail or description; see liveops-quests-retention.md §social rewards.)
14. Small servers: 5–7 for steal, throw and egg-journey loops (Throw Food For Animals 5, Steal An Egg 7); 6–8 with a plot each for management; 12–22 for +1 lobbies; 10–20 for co-op horror and journeys; the top ragdoll sandbox is solo (1 per server).

## Cozy management: format norms (fact, 7 and 26 Nov 2026)

| Game | 7 Nov | 26 Nov (24 h peak) | Session | Key mechanic |
|---|---|---|---|---|
| My Small Business | 20.0K (peak 44.8–46K) | 1.0K (2.7K) | 15.2 min | Design → print → pack → ship; hire workers; bedroom → warehouse; offline income |
| Sell a Million Sushi | 12.9K (peak 15.8K) | 4.0K (5.3K) | 15.6 min | Hire 1/5/25 fishermen, merge 3 into the next tier, 24-fish index, 98.9% likes |
| LINE UP! Metro Tycoon | 11.6K (7-day avg 6.1K) | 6.9K (9.1K) | 20.7 min | Draw rail lines between stations like a toy; 50-player servers |
| Run A Farm! | 10.2K | 3.0K (5.4K) | 21.3 min | Coop → crops → tractors; truck goods to town; hire workers |
| Run a Sari-Sari Store! | 5.2–10.6K (peak 35.8K) | 4.4K (5.9K) | 26.7 min | Shop sim with almost no monetisation |
| Mechanic Legends | 6.9K (peak 12K) | 4.5K | 17.5 min | Buy, repair, flip cars |
| Pocket Landlord | 3.4K | 0.7K | 7.9 min | Decorating: 236K favourites but short sessions |
| Warnetopia: Internet Cafe (5 Nov) | — | 12.4K | — | Run an internet café: buy PCs, fix broken ones, cook orders, hire staff; 6 per server |
| Barber Empire (31 Oct) | — | 11.5K | — | Cut hair strand by strand with real tools, post before/after videos, hire barbers; 68.5% likes |
| Run a Christmas Tree Lot (4 Nov) | — | 2.4K (10.2K; peak 37.6K) | 23.5 min | Stock and sell trees, hire workers, expand the lot; 6 per server |
| Fleet Empire, FLIGHTLANES, Airline Executive, Formula managers | 284–993 each | 34–217 | 22–24 min | Menus, maps, spreadsheets |

Sessions are the vault's 7 Nov values; the Christmas Tree Lot value is Rolimons' average playtime (26 Nov), which reads 19–21 min for the first four rows.

What separates hits from flops (inference):

- **You do the work yourself in a small 3D space.** Every management game above 5K CCU is hands-on with your own character; menu, map and spreadsheet sims stay under 1K however deep they are (Fleet Empire peaked at 1.8–2K). LINE UP! is the only map-based hit and it plays like a toy (drawing coloured lines), not a spreadsheet. The 26 Nov form is a craft verb done with tools: cut hair strand by strand, fix a broken PC.
- **Leaders rotate in 2–4 weeks.** The 7 Nov top three lost 65–95% by 26 Nov while new themes (an internet café, a barber, a Christmas tree lot) took over; LINE UP!, the toy, held best. Plan a pipeline of themes and weekly content, not one theme.
- You earn within a minute, then hire your way from active play to idle income (Hire 1/5/25 pads; merge 3 of a tier into the next; staff take the place of pets).
- Something to collect: merge tiers, an index, rarities.
- Offline income and a friends bonus; 6–8 player servers with one plot per player.
- Money comes from cheap repeatable dev products more than passes; job sims without a currency loop lean on passes (Barber Empire lists 18, from 39 R$).
- Decorating brings favourites but short sessions; driving controls are hard for young players, keep driving optional.
- Management thumbnails are mostly photoreal with no text; the few with a hook use a price flip ("$0.05 → $35,279", "$46.2M SOLD!"). A management game with an incremental-style number ladder stands out.
- Risk: looking too much like the current leader triggers the near-duplicate penalty; a distinct theme, art and place file clears it.

## +1 / Evolution format norms (for the owner's snowball project and any stat-lane game)

- Stage gates grow about ×4 per stage (Dino: 40, 375, 1.5K, 6.2K, 26.2K, 62.5K, 200K); 8–10 gates per World; launch with 3 Worlds and add one a week toward 12.
- Eggs cost ×40–250 the previous egg (Muscle: 100, 25K, 1M, 150M, 7.5B, 125B Wins); 4–5 pets per egg, top pet 0.1%, additive boosts +0.1 to +5, 3–4 starting slots. Paid eggs are paid random items (odds shown).
- Robux ladder seen in the format: one-time training pads ×8 / ×15 / ×30 / ×99 at 79 / 199 / 499 / 1,299 R$; 2× Wins 90–99 R$; size packs at 10 / 41 / 86 / 167 R$; idle pad about 69 R$; 30+ cheap repeatable products.
- Rebirth ×2 / ×3 / ×4 with level caps (22 / 34 / 48), keeps the collection. Group boost +10%, friend boost +20%.
- Sessions: Venom 14.0 min, Gun Forge 33.8 min; aim for 19+ min.
- Status on 26 Nov: the middle tier fell 75–95% from 7 Nov (Venom 46K → 8.5K, Spider Arm 30K → 2.1K, Bug Evolution 29K → 2.0K, Power Fruit 14K → 3.4K). Among 40 "+1" search results only +1 Speed Keyboard Escape is above 10K, and none was created after 7 Nov. Ant Evolution (a body you grow in a 3D world, 65.9K peak) is the fresh form.
- Competition for a snowball-size lane game: still no leader. All 40 "snowball" results are under 100 CCU, but 12 were created since 7 Nov ("+1 Roll a Snowball", "Grow a Snowball", "Roll Snowballs For Animals"), so the name space is filling: the title must be distinct.

## Thumbnail and title playbook v2 (13 rules)

Roblox ranks thumbnails by qualified plays, not clicks, so the first minute must deliver what the tile shows. Home shows 16:9 tiles and uses slot 1 when personalisation is off (+7.2% plays after the switch); with 2–5 thumbnails active on the Home Page tab, personalisation picks one per user (thumbnails docs, read 26 Nov 2026); personalization rotates 2–5 images hourly per age group (+8.5–12% qualified plays, up to +50–56%). Tiles show at about 150 px; text under about 40 px is unreadable; nothing important on the bottom edge.

| # | Rule | Do | Don't |
|---|---|---|---|
| 1 | Show the first minute of gameplay | The progression players actually get | A boss they never meet |
| 2 | One focal point, at most 5 elements | Giant character with one item | A busy map overview |
| 3 | Big number in the game's own unit | "1,000,000,000 SIZE" with a heavy outline | Small "earn money" text |
| 4 | Show the climb in one frame | NOOB → GOD, Day 1 → Day 100, $1/s → $9.8M/s, or one throw arc over rising zone steps to the top prize | Only the end state |
| 5 | Readable at 150 px | 3–4 words, top or middle | Key text on the bottom edge |
| 6 | Colour to genre, or break it on purpose | Saturated for sims; a number-style tile for a management game | Bright art for horror |
| 7 | A face sells the emotion | Shock, crying, screaming (26 Nov 2026: faces on 78% of established games' thumbnails, 49% of new games'; test it, it is not a law) | A blank standing avatar |
| 8 | Fill all 5 personalization slots with different hooks | Ladder, odds, VS, rare item, gag; keep each 7+ days | 5 recolours, or resets every 2 days |
| 9 | Title = short name with the verb; status in Promotional Text, refreshed every update | Name `+1 Snowball Size For Eggs`, Promotional Text "Winter Update"; any tag left in the name 6 characters or fewer | Halloween tags in late November; a seasonal tag with no seasonal art; a long leading tag such as `[WEEK 4 🎃 x BUTCHER]` |
| 10 | Copy the format, not the art | Same formula, your own theme | Cloned art or names; a shared template still carrying another game's labels (26 Nov: five games, one template) |
| 11 | Show your rarest odds only if they are real | "1 in 50,000,000", same odds shown in-game | Odds that don't exist |
| 12 | Put the live boost in Promotional Text (or a tag of 6 characters or fewer) | "2X SIZE", "6H EVENT", rotated with events | A permanent fake "2X"; "SALE!" or prices on the icon |
| 13 | Don't run ads until the rating is 85% or higher | Wait for the rating to settle | Paying to show "66% Rating" (ad median is 79%; non-ad median 92%) |

Rules 9 and 12 changed on 26 Nov 2026: since 3 Nov Roblox's Promotional Text beta takes status, update and event lines (Creator Hub ⟩ game details), and Roblox tests shortened names that drop bracket and emoji tags for some new users (DevForum /t/4973915, beta). Keep the name readable alone; put the live tag in Promotional Text (icons-thumbnails-and-store-page.md §10).

Feed stats (coded from 72 + 177 tiles): [TAG] titles 53–64%, emoji 39–52%, giant number 22–37%, before → after 8–16%, "1 in X" 3–10%, no text at all 27–31%. Established games use a logo and moody art because the name is the hook; new format games use saturated colour, a giant number and a visible climb because the mechanic is the hook. 26 Nov 2026 re-count (60 chart games, 158 thumbnails; 386 titles across Top Playing Now, Top Trending, Up-and-Coming and Top Earning): any bracket tag 48–58% by sort (leading 38–51%), emoji 44–57%, a number on 11% of thumbnails (18% for games created since September, 3% for established games), before → after split 1%, "1 in X" 3%, no text 44%; 17 of 44 leading tags on Top Playing Now were a bare emoji.

## Discovery facts that change design decisions `[VS]`

- Since 15 Jun 2026 Recommended For You rewards: no bounce in the first 1–3 min, return days across 28 days (D1, D2–7, D8–28), long sessions (capped at 60 min per user per day), intentional co-play (joins, invites, private servers; matchmaking does not count), and repeat spending (spend days beat one big purchase). Only organic RFY arrivals count, averaged per user, so small games are not disadvantaged. Signals update within 24 h; impressions lag by days. Saturday is the weekly peak.
- Roblox's Q3 2026 letter (29 Oct): RFY now weights age cohorts, and about 40% of its weekly top 100 by impressions were games created in the previous three months `[official]`. `inference`: a new game can reach the front page within weeks, and so can its clones.
- New since 2026: deep play-through rate (9 Mar), "Not interested" feedback (26 Mar), a 7-day qualified-sessions version (26 Mar), the 12 Oct measurement change (creators report 26–40% PTR drops; do not compare across it).
- Penalties: near-identical visuals, titles or place files (the first to add unique metadata wins); leading with giveaways or Robux; thumbnails that do not match the game; a custom thumbnail is required to appear at all.
- Gameplay video autoplays in RFY since 29 Jul 2026 (up to +39% playtime); real gameplay only. Continue row: the 2 most recent games take the first 2 slots.
- Accounts without an age check get a Kids-equivalent experience (no chat, nothing above Mild). 64% of daily users were age-checked at the end of Q3 2026, 80% in Australia, 75% in the US and UK, and over 80% of 13–17s `[official]`.
- The new-game gate: 100 unique plays (250 until 19 Nov 2026) from highly engaged, age-checked 16+ players within 60 days before Kids (5–8) and Select (9–15) can see the game `[official]`; creator verified with 2FA; all-ages publishing needs Plus/Premium for 2 consecutive months or a refundable fee; expedited review is a refundable 50,000 R$. Plan to bring older players first (Discord, TikTok).
- Standout Games picks 4 per row, mostly small or mid-sized games, on D1/D7, growth, originality, monthly updates and experience events; spending does not count; owners can nominate before launch.
- Benchmarks (GameAnalytics 2025, third-party): median session 6.6 min; sessions of 19–24 min show median D1 11.5% (top 2% 32.3%) and D7 1.6% (top 2% 8.5%). Daily playtime median 16.8 min, top 10% 64.9 min. Use these, not the unsourced 20–35% D1 figures.

## Launch checklist from the v2 report

- [ ] 3–5 distinct thumbnails with personalization on, kept 7+ days, plus a real gameplay video.
- [ ] Unique title, art and place file; no Robux or giveaway lead.
- [ ] Core fun inside 60 s; first number-go-up moment before 180 s. (The report's line. The house target is stricter: first reward under 30 s, first upgrade under 2 min; core-loop-tuning.md.)
- [ ] Average session 19+ min; D1 above 11%, 20–30% as a stretch.
- [ ] Daily return reasons: timers, offline earnings, restocks (no streak-loss anxiety).
- [ ] Core players near the 60 min/day playtime cap.
- [ ] Rewards for friend joins and private servers.
- [ ] Cheap repeatable dev products beside game passes.
- [ ] 100 engaged 16+ plays within 60 days (250 until 19 Nov 2026); monthly-or-faster updates logged as Experience Events; a Standout nomination.
- [ ] Launch on a Saturday or holiday; the December window first.

## Gap ranking (1–5 each, 35 max; the report's 7 Nov scores, re-scored 26 Nov 2026)

Scores: demand (D), competition (C, 5 = empty), buildability (B), money (M), thumbnail (T), timing (Ti), durability (Du). Our judgement on the 26 Nov evidence.

| Rank | Concept | 7 Nov | 26 Nov | MVP | Note |
|---|---|---|---|---|---|
| 1 | Ragdoll launch incremental | 30 | 29 (D5 C4 B4 M4 T5 Ti5 Du2) | 2–4 weeks | The strongest new wave is 4–6 weeks old, so the window stays open to about mid-December; the only progression hybrid above 1K is Defeat Ragdolls for Powers! (6.0K). The bar rose: Hyper Realistic Ragdoll reacts per limb. Stay Mild (no blood) to keep under-13s; 1–4 month life; shelved |
| 2 | Co-op anomaly fishing | 30 | 29 (D4 C5 B3 M4 T5 Ti3 Du5) | 6–8 weeks | Fishing holds (Fish It 68K, Fisch 56K) and co-op journeys rise, but liminal horror faded (DONT SPLASH −85%): frame it as a night-by-night journey. Longest expected life; shelved |
| 3 | +1 Snowball Size For Eggs (the owner's chosen December game) | 31 | 28 (D3 C4 B5 M5 T5 Ti4 Du2) | — | The +1 and egg-journey formats it rides fell 65–95% since 7 Nov, but snowball still has no leader and it is the fastest December build: ship around 10 Dec to clear the 100-play gate before the holiday window. Option: borrow the rising verb, so the Stage-lane roll ends where Size carries you and the landing zone sets the egg's luck |
| 4 | Steal-a-tower TD | 27 | 24 (D4 C4 B2 M5 T4 Ti2 Du3) | 8–12 weeks | TD is durable (Anime Crusaders X 115K peak this week), but steal is contracting (3 of 40 above 10K) |
| 5 | Warehouse: hands-on fulfilment + drawn routes (the owner's next idea) | 24 | 23 (D3 C4 B2 M4 T4 Ti3 Du3) | 8–12 weeks | The 7 Nov competition faded (My Small Business −95%, Sell a Million Sushi −69%), and so did the proof of demand; LINE UP!'s toy map held best. Test the loop at December scope first (Idea bank #12) |

## Idea bank (26 Nov 2026)

Original concepts, not recreations: each takes a rising or open format and adds its own verb and setting. All follow the house rules: every visible object is a solid Blender model with collision (debris, sleds, dogs and shells included), and the default product set (timed 2× Cash, Speed and EXP, a starter pack, gift passes, convenience passes) is sold without blocking play. Only ideas marked "Luck: yes" have a luck mechanic and may sell Luck and Server Luck (full odds, `PolicyService` gate). Scores use the gap rubric above; MVP is a solo-developer estimate (`inference`). Build plans live in the matching `genres/` file (`throw-for-distance.md` for #1 and #6).

1. **Sled Jump For Yetis** — 30 (D5 C4 B5 M5 T5 Ti4 Du2); MVP 2–3 weeks; Luck: yes. *Pitch:* sled off a ski jump; where you land picks the snow creature you befriend. *Loop:* train leg power → jump, steering through boost rings → zone and luck pick the creature → creatures pay $/s at your lodge (offline capped) → better sleds → rebirth. *Verb:* a sled jump with air steering. *Why now:* distance = luck is the biggest new wave (Throw Food For Animals 2.45M peak; Throw a Seed 172.9K within 15 days); no "sled" or "snowball" game is above 1K. *Risk:* 10 "throw" clones since 7 Nov: ship by about 12 Dec, with snow zones rather than Santa so it outlives Christmas. *Thumbnail:* a sled mid-air over coloured distance bands, a glowing yeti on the farthest, "1 in 1,000,000".
2. **Ice Camp** — 30 (D4 C4 B4 M5 T5 Ti4 Du4); MVP 4–6 weeks; Luck: yes. *Pitch:* drill a freezing lake, set tip-ups that fish while you play, and build a heated village as the ice thickens. *Loop:* drill → tip-ups catch on timers → a fish index with sizes and rarities pays → augers, shacks, heaters → thicker ice each week reaches deeper fish; aurora nights spawn mythics. *Verb:* drill (hold-to-drill skill check). *Why now:* fishing is durable (7-day peaks Fisch 338K, Fish It 124K) and cast-for-animals clones reach 14–30K; the best ice-fishing game has 3.8K. *Risk:* a crowded top; it must look distinct (warm-lit shacks on dark ice). *Thumbnail:* a tiny avatar over a hole, a huge shadow under the ice, "1 in 5,000,000".
3. **Shell Swap** — 29 (D4 C5 B4 M4 T5 Ti4 Du3); MVP 3–5 weeks; Luck: yes (shell finds). *Pitch:* a hermit crab grows from a bottle cap to a shipwreck. *Loop:* forage (size per second) → find shells by rarity → swap into a bigger one (3 s exposed to gulls) → tide pool → reef → wreck → a colony with friends; molt to rebirth. *Verb:* swap shells. *Why now:* Ant Evolution peaked at 65.9K with 19.6-min sessions while menu-number +1 games fell 75–95%; no crab game is above 2K. *Risk:* the evolution family is cooling; the swap must feel risky and social. *Thumbnail:* "BOTTLE CAP → SHIPWRECK", a tiny crab beside a giant one wearing a ship.
4. **Paws & Suds** — 29 (D4 C5 B3 M4 T5 Ti4 Du4); MVP 5–7 weeks; Luck: no. *Pitch:* wash, dry, trim and style dogs by hand; each finished pet walks your salon's runway. *Loop:* an order card → wash, brush, trim (layered fur reveals the cut) → stars and tips → tools and decor → hire groomers for idle income → a 30-breed index. *Verb:* trim fur. *Why now:* Barber Empire reached 11.5K in 26 days on strand-by-strand cutting despite 68.5% likes; pet care is evergreen (Adopt Me 7-day peak 801K); no pet salon is above 100. *Risk:* layered fur costs memory on a 3 GB phone and fiddly tools frustrate on touch: forgive the input. *Thumbnail:* a matted poodle → show cut, "5★".
5. **Restore the Park** — 29 (D4 C5 B3 M4 T5 Ti4 Du4); MVP 5–7 weeks; Luck: no. *Pitch:* a co-op crew cleans an abandoned theme park; each restored ride reopens and earns. *Loop:* sweep, scrub, unscrew, repaint a zone → the ride reopens → visitors pay $/s (offline) → the next zone; lost rides to find; a new zone each week. *Verb:* restore (before → after on every object). *Why now:* cleaning jobs trend (Clean The Ballpit! 46.9K peak, a 688K-view video this week) but die within weeks without a tail (Sweep The Moon 53K → 4.3K); "restore" tops out at 1K. *Risk:* content-hungry. *Thumbnail:* split frame, a rusted dark ride beside the same ride lit and running, "DAY 1 → DAY 100".
6. **Tee Off For Dinos** — 29 (D5 C4 B5 M5 T5 Ti3 Du2); MVP 2–3 weeks; Luck: yes. *Pitch:* golf across a prehistoric valley; where the ball lands cracks a dinosaur egg. *Loop:* swing meter → the ball crosses zones → zone and luck set the egg → dinos pay $/s → clubs and balls → rebirth. *Verb:* a timed golf swing (skill on top of distance). *Why now:* the same distance = luck wave; the best golf-for-eggs game has 593. *Risk:* the same lane as #1; build one of the two. *Thumbnail:* a ball streaking over a canyon toward a glowing egg, "1 in 10,000,000".
7. **Ski Jump Legends** — 28 (D4 C5 B4 M3 T5 Ti4 Du3); MVP 3–4 weeks; Luck: no. *Pitch:* ragdoll ski jumping: hold your pose in the air, then stick the landing or cartwheel down the hill. *Loop:* jump → judges score distance and style → sponsor cash → skis and suits → bigger hills (K90 → K240 → a volcano ramp) → a weekly ladder; 8-player heats. *Verb:* hold a flight pose. *Why now:* ragdoll physics and physics sports both rise (Ragdoll Soccer 87.6K peak; a 2.0M-view ragdoll video this week); the best ski-jump game has 610. *Risk:* physics-sport sessions are short (Ragdoll Soccer 9.6 min); the career must carry 15+ minutes. *Thumbnail:* a cartwheeling skier crossing a red "WORLD RECORD 412 m" line.
8. **Hundred-Mile Sled Dogs** — 28 (D4 C5 B2 M4 T5 Ti3 Du5); MVP 6–10 weeks; Luck: no (dog traits shown). *Pitch:* four friends drive a dog sled 100 miles across the Arctic before the long night. *Loop:* mush by day → camp at dusk (fire, feed, repair) → storms and wolves at night → the next outpost → recruit dogs with traits → longer routes. *Verb:* mush (the team's traits change the handling). *Why now:* co-op journeys rise (100 Miles Down the River 91.4K peak, 18.6 min, five 115–300K videos this week) and the dogs are the collection; no sled-dog game has players. *Risk:* misses December; a Blender terrain kit (terrain needs the owner's approval) and dog rigs are the cost. *Thumbnail:* a dog team racing a black storm wall, "MILE 99".
9. **Snow Globe Collector** — 28 (D3 C5 B4 M5 T5 Ti4 Du2); MVP 3–4 weeks; Luck: yes. *Pitch:* shake snow globes to reveal the scene inside and fill a glittering shop. *Loop:* buy a globe → shake until the snow settles on its rarity → shelf sets pay $/s → merge 3 duplicates → weekly drops. *Verb:* shake. *Why now:* pack opening works when the set is the goal (My Little Pony Card Opening, created 7 Nov: 8.1K, 98.4% likes); the best snow-globe game has 201. *Risk:* paid globes are paid random items; thin play; trading needs anti-scam rules. *Thumbnail:* a hand shaking a giant globe with a rainbow dragon inside, "1 in 1,000,000".
10. **Up There: 100 Islands** — 28 (D4 C5 B3 M4 T5 Ti3 Du4); MVP 6–8 weeks; Luck: no. *Pitch:* four friends keep a patched hot-air balloon aloft across 100 sky islands. *Loop:* burn, vent and drop ballast (height picks the wind) → land to loot and repair → storms at night → island 100. *Verb:* trim altitude. *Why now:* co-op journeys rise (as #8) and the sky is unclaimed ("100 Days in the Sky" has 24–38). *Risk:* wind and buoyancy over the network. *Thumbnail:* the balloon between a lightning storm and a floating island, "ISLAND 1 → ISLAND 100". A non-winter journey for January on.
11. **Wrecking Crew** — 27 (D4 C4 B3 M4 T5 Ti4 Du3); MVP 4–6 weeks; Luck: no. *Pitch:* swing a wrecking ball through towers; every falling chunk is cash. *Loop:* demolish → debris pays → heavier balls, longer cranes (merge 3 balls) → house → skyscraper → dam → rebirth. *Verb:* swing the wrecking ball. *Why now:* destruction physics rises (BloxNG 61.2K peak, Top Earning #28 on 13 passes); no demolition game with progression shows above 3.5K in search. *Risk:* debris on a 3 GB phone: pre-fractured Blender chunks, pooled and capped. *Thumbnail:* the ball mid-impact, glass and concrete flying, "$1 → $1,000,000,000".
12. **Gift-Wrap Express** — 27 (D4 C5 B3 M4 T4 Ti4 Du3); MVP 4–6 weeks; Luck: no. *Pitch:* wrap and load presents by hand, then hire elves and draw sleigh routes on a toy map. *Loop:* wrap (fold, tape, bow in three taps) → load the sleigh → draw a route between rooftops → deliveries pay → hire 1/5/25 elves → a bigger workshop. *Verb:* wrap. *Why now:* the owner's warehouse loop at December scope; craft-verb job sims lead cozy management (Warnetopia 12.4K, Barber Empire 11.5K, Run a Christmas Tree Lot 37.6K peak); the best wrapping game has 727. *Risk:* the 26 Dec cliff; keep the depot theme-neutral and reskin in January. *Thumbnail:* an avatar buried in gifts, "1 → 1,000,000 PRESENTS".
13. **Snowfort Siege** — 26 (D4 C5 B2 M5 T4 Ti2 Du4); MVP 8–12 weeks; Luck: only if units are rolled. *Pitch:* build a snow fort with friends, sculpt snowman defenders and throw snowballs yourself at waves of critters. *Loop:* a wave → snow → sculpt and merge snowmen (3 into 1) → you throw too → a boss every 5 waves → new forts. *Verb:* pack and throw (the player is a tower). *Why now:* tower defense is durable (Anime Crusaders X 115K peak this week, Anime Adventures 68K); "snow fort" is empty. *Risk:* TD scope misses December; reskin for January. *Thumbnail:* a giant snowman holding a breach against a horde, "WAVE 100".

## Review gate

- [ ] The concept names its one new action or visible journey, not only a theme.
- [ ] The loop is hands-on in 3D before it is a menu; any map or route layer plays like a toy.
- [ ] Collection, merge tiers, timers, offline income, friend bonus and a fixed weekly update day are in the plan.
- [ ] Product plan leans on cheap repeatable dev products; passes are the convenience layer.
- [ ] Title and art are distinct from the nearest hit; names avoid "Sell a Million" and "Run a".
- [ ] Thumbnail plan follows rules 1–13; no ads until the rating is 85%+.
- [ ] The 16+ first plan for the 100-play gate exists; launch date sits on a Saturday or in a seasonal window.
- [ ] The wave's age is checked: the parent is 2–8 weeks into its rise, judged by 24 h and 7-day peaks at a fixed UTC hour, not one snapshot.
- [ ] A seasonal theme outlives its holiday (winter, not only Christmas).

## Sources

- The owner's research vault, 2026-11-07 snapshot: `Delta Vault/Roblox Research/2026-11 Market Scan/` (bundle `roblox-market-research-2026-11.zip`, identical to the vault's `_raw/` folder), and the v2 report "Roblox Market Research v2 — Nov 2026 (Detailed)" (https://claude.ai/artifact/WkBA2wVEVauiMCHgy1CSKA). The converted report is `references/market-research-v2-raw.md`; the vault-sourced sections of `references/knowledge-base.md` are marked "(Delta Vault: …)".
- Third-party figures quoted through the report (GameAnalytics 2025 benchmarks, creator reports on the 12 Oct 2026 measurement change) were not re-opened for this file; treat them as `[VS]`.
- 26 Nov refresh, all accessed 2026-11-26:
  - Roblox explore API, `https://apis.roblox.com/explore-api/v1/get-sorts` and `.../get-sort-content` (device=all, country=all), pulled 10:02 and 11:00 UTC. It returned 26 game sorts: top-trending (Top Trending), up-and-coming (Up-and-Coming), top-playing-now, top-earning, top-rated, top-revisited, most-popular, fun-with-friends, top-paid-access, more-when-you-subscribe, learning-and-explore, trending-music-experiences and 14 trending-in-<genre> sorts (action, adventure, entertainment, obby-and-platformer, party-and-casual, puzzle, roleplay-and-avatar-sim, rpg, shooter, shopping, simulation, sports-and-racing, strategy, survival), plus filters_v5 and music-top-100 (songs): 931 games in all.
  - Roblox games API `https://games.roblox.com/v1/games?universeIds=…` and `/v1/games/votes` (CCU, visits, favourites, created, updated, genre); game passes `https://apis.roblox.com/game-passes/v1/universes/<id>/game-passes`; search `https://apis.roblox.com/search-api/omni-search` (first 40 results per query).
  - Rolimons game pages, `https://www.rolimons.com/game/<placeId>` (all-time, 30-day, 7-day and 24 h peaks; average playtime), read about 10:30 UTC.
  - Roblox Q3 2026 shareholder letter (29 Oct 2026), SEC 8-K exhibit 99.1, https://www.sec.gov/Archives/edgar/data/1315098/000162828026068235/ex991-q32026earningsshar.htm (read) `[official]`; ir.roblox.com refused the request.
  - Kids and Select threshold of 100 plays: creator docs, https://create.roblox.com/docs/production/publishing/kids-and-select (read from the `Roblox/creator-docs` main branch), and the DevForum post "A Simpler Path to Publish, Plus Invite Early Testers" (12 Oct 2026, edited 19 Nov), https://devforum.roblox.com/t/4930524 (read) `[official]`.
  - The Great Build, https://www.roblox.com/games/98487757108234 (Roblox Presents; description read through the games API).
  - GGRecon, "30 of Roblox's 99 top games didn't exist before October" (19 Nov 2026), https://www.ggrecon.com/articles/roblox-top-games-didnt-exist-before-october/ (read; its own Top Playing Now pull of 18 Nov, 21:37 UTC).
  - Bloxodes, "Roblox in October 2026", https://bloxodes.com/stats/reports/roblox-october-2026 (read; weekday and weekend averages, genre trends; third-party).
  - RoWatcher "Week in Numbers" for 2–8, 9–15 and 16–22 Nov 2026, https://rowatcher.com/news/roblox-week-in-numbers-2026-w45 (and -w46, -w47) (read; third-party lists only, its commentary not used); on brainrot, https://rowatcher.com/news/is-the-brainrot-trend-dying-what-ccu-data-from-three-top-games-reveals (search).
  - YouTube search with the "this week" filter for "roblox", "roblox ragdoll", "roblox for animals", "roblox steal a", "roblox +1 every second", "roblox monkey", "roblox 100 miles down the river", "roblox clean", "roblox grow a garden", "roblox snow" and "roblox christmas game" (search); for example https://www.youtube.com/watch?v=M3vFWpigkD8, https://www.youtube.com/watch?v=rWnrpO3o4t8, https://www.youtube.com/watch?v=Ec7h3v_Ghm4, https://www.youtube.com/watch?v=HOKS5aKoEHM; the removal claim is https://www.youtube.com/watch?v=MXvWIf3mkhM (search; unconfirmed).
  - RoLearn, "Roblox on YouTube & TikTok: Content Trends Report 2026" (24 Oct 2026), https://rolearn.dev/trend-reports/roblox-youtube-tiktok-content-trends-2026 (read; third-party estimates).
