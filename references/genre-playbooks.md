# Genre playbooks: index and cross-genre rules

Routes a concept or a live game to its deep playbook in `references/genres/`, and holds the rules that apply to every genre and to hybrids. Open it first when choosing or naming a genre, then open the one or two genre files it points to. Market positions are the owner's vault snapshot of 2026-11-07 `[VS]` (see `market-scan-2026-11.md`); rewarded-video benchmarks are Roblox's genre playbooks `[official]` `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Use this index to | Then |
|---|---|---|
| Beginner | Pick one genre from the table whose asset bill you can finish (obby, simulator, tycoon, +1, party minigames are the lightest); read only that file's "Start here by level" row and "Systems to build, in order" | Build the beginner row, nothing else; ship; come back for the intermediate row |
| Intermediate | Classify a working game by its host loop; run that file's level-up checklist; check the cross-genre rules below | Fix the top three failing checks before adding content |
| Expert | Design or audit a hybrid (host plus layer); resolve every "Conflict" note; compare vault status with the pairing table | Model the economy and netcode choices the genre file names, then instrument them |

Terms: *host loop* = the loop that fills most minutes of play; *layer* = a system borrowed from another genre; *CCU* = concurrent users.

## How to pick a genre

1. **Start from the spine, then the verb.** Every 2025–26 mega-hit runs a stat or income per second → multipliers from a collection → rebirth, plus one new action or a visible journey (steal, grow, kick, throw, climb, bike, dig, roll, draw routes). Put originality in the verb, not the theme.
2. **Read the status column below.** Rising or durable with an open pairing beats saturated. A clone wins only if it ships 2–8 weeks into the parent's rise; format clones get about two weeks of attention; remixes with a new action far outperform reskins.
3. **Match the team to the content bill.** Every visible asset is a Blender model. Obby, +1, simulator and tycoon need tens of assets; RPG, roleplay and shooter need hundreds. Count the asset list before committing.
4. **Match the audience and reach.** Younger players prefer exploration, experimentation and socialising over competition; older players (16+) invest more time and money and form communities `[official]`. Social beats solo. Moderate-rated content loses Kids and Select reach; social hangouts are 16+ `[official]` `[VS]`.
5. **Check lifecycle against patience.** Mega-hits peak in 7–8 weeks and fall 90–99% within 6–12 months; single-gimmick format hits lose 90%+ in 1–4 months; durable games (co-op or skill play, real depth, weekly updates) hold for years.
6. **Run the three-layer loop test** `[official]`: minute-to-minute interaction → most repeated action cycle → progression engine. Each layer must feed the next. Prototype loop, UI, rules and edge cases before art.
7. **For a live game, classify by what players do most**, not by the title. If two files fit, the host loop (the one that fills most minutes) leads and the other is a layer; see hybrids below.

Dashboard genre settings `[official]` `[VS]`: set genre and optional subgenre in Creator Dashboard; changeable once every three months; Roblox may correct an inaccurate genre (appeal possible). The selected genre feeds genre charts but is not a Recommended For You ranking input. For current trends and what to build, consult the owner's vault (`Roblox Research/2026-11 Market Scan/_MOC.md`).

## Routing table

| Genre | File | Loop in one line | Vault status (2026-11-07) | Dashboard genre › subgenre |
|---|---|---|---|---|
| Tycoon and cozy management | `genres/tycoon-and-cozy-management.md` | Do the job by hand on your plot → hire → expand → idle income → rebirth | Cozy management rising (10–20K leaders); menu sims under 1K | Simulation › Tycoon |
| Simulator, incremental, clicker | `genres/simulator-incremental.md` | Act → number up → upgrade → zone → rebirth | Crowded long tail; simulators cooling | Simulation › Incremental Simulator / Idle |
| RNG and aura rolling | `genres/rng-rolling.md` | Roll → reveal → keep best → convert duplicates → shift luck → raise cap | Winner-take-most (41K, 30K, then under 3K) | Simulation › Incremental Simulator / Idle |
| Fishing and catch collection | `genres/fishing.md` | Cast → reel minigame → catch with rarity → index → better rod → new water | Durable, up 55% year on year (79K, 63K) | Simulation |
| Pet collection and hatching | `genres/pet-collection-hatching.md` | Earn → hatch (odds shown) → equip → merge → index → trade | Peaked but dominant; casual animal games rising; egg journeys crowded | Roleplay & avatar sim › Pet Care, or the host loop's genre |
| +1 per second and Evolution | `genres/plus-one-evolution.md` | Train a stat → run the stage lane for Wins → eggs and pads → World → rebirth | Healthy middle tier (14–46K); +1 obbies cooling | Simulation › Incremental Simulator |
| Steal-and-defend (base raid) | `genres/steal-and-defend.md` | Acquire → earn per second at base → steal rarer → lock and defend → rebirth | Peaked, saturated, still #1 (1.14M) | No steal subgenre exists; pick by core loop (Simulation › Tycoon or Incremental Simulator) |
| Obby and tower | `genres/obby-tower.md` | Attempt → fail → checkpoint → next stage | Evergreen leader; wave cooling | Obby & platformer › Classic / Tower Obby |
| Horror and co-op escape | `genres/horror-coop-escape.md` | Explore → tension → chase → escape → next floor | Strong; liminal anomaly rising | Survival › Escape / 1 vs All (no horror genre exists) |
| RPG, dungeon, roguelite | `genres/rpg-dungeon.md` | Quest or room → fight → XP and loot → stronger → harder | Evergreen top (Blox Fruits 325K); costly to enter | RPG › Action RPG / Open World & Survival RPG |
| Fighting, battlegrounds, anime gacha | `genres/fighting-battlegrounds.md` | Spawn → combo and abilities → kill or die → respawn | Durable upper-middle (73–89K) | Action › Battlegrounds & Fighting |
| Tower defence | `genres/tower-defense.md` | Loadout → place and upgrade → survive waves → summon and level | Rising, anime-led (46–99K) | Strategy › Tower Defense |
| Social roleplay and life-sim | `genres/social-roleplay.md` | Customise self and space → act out roles → show off and collect | Evergreen, dominant (Brookhaven 438K) | Roleplay & avatar sim › Life |
| Fashion, dress-up, judged creation | `genres/fashion-dress-up.md` | Theme → timed creation → runway → peer vote → podium → payout | Established, past peak, still large (67K) | Roleplay & avatar sim › Dress Up |
| Social deduction and hidden roles | `genres/social-deduction.md` | Role reveal → short round of hunt and survive → full reveal → rewards | Evergreen (MM2 242K) | Survival › 1 vs All |
| Survival and crafting | `genres/survival-crafting.md` | Gather → craft → build → survive the night → expand | Durable (99 Nights 221K) | Survival, or RPG › Open World & Survival RPG |
| Shooter and PvP duels | `genres/shooter-pvp.md` | Queue → rounds of engage, shoot, reposition → result → rank | One durable leader (RIVALS 217K); thin middle | Shooter › Deathmatch Shooter |
| Racing and driving | `genres/racing-driving.md` | Drive → earn → buy or tune a car → races and meets | Steady middle (33K, 29K); scooter micro-wave cooling | Sports & racing › Racing; Simulation › Vehicle Sim |
| Sports and physics sports | `genres/sports.md` | Kick-off → possessions → score → result → rematch | Solid middle (36–38K); physics sports rising | Sports & racing › Sports |
| Party and minigame collections | `genres/party-minigames.md` | Intermission → rule card → 1–3 min minigame → results → next | Long-standing; show-tied spikes fade | Party & casual › Minigame |
| Physics sandbox and ragdoll | `genres/physics-sandbox.md` | Grab or launch → fling → be flung → invent games | Forming wave (21–45K); gap in progression hybrids | Simulation › Physics Sim |

Each genre file uses the same headings: Start here by level · Snapshot · Core loop with timings · First 5 minutes · Progression and economy shape · Monetisation set that fits · Retention and social hooks · UI patterns · Systems to build, in order · Technical hot spots · The one-new-verb angle · Common failure modes · Level-up checklist for a live game · Review gate · Sources.

## Cross-genre rules

Design:
- One new verb per game. A visible journey beats a number on a menu; any map or menu layer must play like a toy.
- Playable within a minute; first number-go-up before 180 s; no tutorial wall. The first 1–3 minutes decide the bounce signal.
- The collection is the multiplier (4–5 items per tier, top about 0.1%); merge tiers reuse one Blender mesh with material variants.
- Timers at 5 / 15 / 30 minutes, capped and stated offline progress, a fixed weekly update day, events with real end dates.
- Sessions of 19+ minutes are the target; a discovery player should complete one full loop (run, rebirth, match set) in the first session.
- Retention never through punishment: no progress wipes, no streak-loss anxiety, loss capped to the current run.
- Longevity signal `[lihfolk]`: games that held their rank combined about 90%+ approval with 25–30 min sessions; spikes with 15-minute sessions faded fastest. Depth and rating predict life better than peak size.
- Bosses, walls and first losses are funnel cliffs in every genre: state the requirement, keep the retry cheap, and make the fix one step away `[lihfolk]`.

Monetisation:
- Dev-product-led catalogues with several items under 50 R$; passes are the convenience layer. Each genre file lists what to add to and delete from the default set in `monetization-and-policy.md`.
- Offers only at positive moments and in breaks (after a win, between waves, on results); never on death, mid-fight or mid-chase.
- No stat power sold in competitive modes. Where the market does it anyway, the genre file marks a "Conflict" and gives the house answer.
- Any roll bought with Robux or with Robux-bought currency is a paid random item: every outcome and numeric odds before purchase, boosted odds shown live, `PolicyService` flags enforced, direct-sale fallback `[official]` `[VS]`. Odds are shown as percentages summing to exactly 100%; a "1 in N" label may accompany but not replace them. Generate the display from the code that rolls: hand-typed labels drift from real odds `[lihfolk]`.
- Before removing or weakening anything a player paid for, give notice and equal value; removal without notice is listed under fraud in Roblox's standards `[lihfolk]` `[VS]`.
- Rewarded-video benchmarks by genre `[official]` `[VS]`: obby opt-in 15–25% at frequency 3 (best 30%+ at 4+); tycoon, RPG and sports 15%+ at 3+; incremental sim 13%+ at 2.8; survival 13%+ at 2.5+; shooter 10%+ at 3+.

Engineering:
- The server computes every number that matters; remotes carry intent, never amounts or damage.
- Crowds (enemies, workers, pets, droppers) are data on the server and pooled Blender models on clients. No Humanoid armies, no physical part spam.
- Save ids and counts, not instances; session-locked profiles; atomic, logged transfers wherever items move between players.
- Movement is client-owned by default. For competitive movement or hit registration, validate on the server or adopt the server authority model (`Workspace.AuthorityMode`) `[official]` `[VS]`.
- Budget for a 3 GB Android phone in the busiest scene of the genre (the plaza, the peak wave, the 10-player brawl).
- Timers and schedules come from server time (`Workspace:GetServerTimeNow()`), replicated as end timestamps, so every client and server agrees.
- Round-based games clean up per round (a janitor) and isolate errors per round; leaks surface after dozens of rounds, not in testing `[lihfolk]`.

## Hybrid genres

Most 2026 hits are hybrids: an idle core plus one borrowed system. Rules:

- **One host, one layer.** The host loop fills most minutes and sets session shape, server size and UI. The layer adds a collection, a risk or a social frame. Two hosts (a full RPG inside a full tycoon) doubles the content bill and confuses the thumbnail.
- **Read both files; the host file leads.** Take Core loop, First 5 minutes and Technical hot spots from the host; take the economy and compliance sections from the layer.
- **Strictest rule wins.** If the layer adds PvP, the no-paid-power rule applies to everything that touches it. If the layer adds rolls, the paid-random-item rules apply to the whole purchase path. If the layer adds fear above Mild, the reach cost applies to the whole game.
- **The stat must become a place.** Hybrids that only add a number (a "+1" on an egg game) fail; hybrids that add a trip or an action (bike, climb, steal, draw) chart (vault).
- **Check the pairing is open** by searching the first 40 results for both parents and counting games above 2K CCU.

| Pairing | Host file (in `genres/`) | Layer file | Vault verdict (2026-11-07) |
|---|---|---|---|
| +1 Stage lane × eggs × snowball theme | plus-one-evolution | pet-collection-hatching | Gap (owner's December game) |
| Hands-on warehouse × drawn routes | tycoon-and-cozy-management | — | Gap, with real competition still rising |
| Fishing × anomaly horror | fishing | horror-coop-escape | Gap; longest expected life |
| Ragdoll launch × incremental | physics-sandbox | plus-one-evolution | Gap; 1–4 month lifespan |
| Steal × tower defence | tower-defense | steal-and-defend | Partial gap |
| +1 stat × eggs with no journey | — | — | Fails |
| Steal a ___ × new theme; X Incremental × any theme; standalone RNG; anomaly × job sim | — | — | Saturated or crowded |

## Formats without a dedicated file

Racing, fishing, sports, RNG, fashion, social deduction, party minigames and physics sandboxes now have their own files (see the routing table). The formats below have less market evidence in the vault; each entry points to the files to combine.

- **Zombie and wave-survival co-op.** A director with a spawn budget releases enemies in a trickle, not all at once; party scaling is sublinear with a global cap on living enemies; downed, revive, bleed-out and spectate replace instant death with long respawns `[lihfolk]`. Use `genres/survival-crafting.md` (hordes, revives) and `genres/tower-defense.md` (wave sheets).
- **Battle royale.** Choose lobby size and match length for the CCU the game really has; a large-lobby requirement at launch population is the classic failure. Lobby and match are separate places with reserved servers and teleport-failure handling; the zone is server-owned with timed damage checks and reachable final circles `[lihfolk]`. Use `genres/shooter-pvp.md`.
- **Open-world city and crime roleplay.** Robberies are multi-step, timed and validated by position on the server; wanted level and alerts are server state, and markers show areas rather than exact positions by default; server size and police cap are live-tunable; avoid huge empty maps at low server sizes `[lihfolk]`. Use `genres/social-roleplay.md`, `genres/racing-driving.md` and `genres/shooter-pvp.md`.
- **Naval and open-sea adventure.** Give players something to stop for every 30–90 s of sailing; use an arcade ship controller on a flat physics plane with waves drawn on the client rather than full buoyancy that throws crew off decks; the helm's client owns the ship with server speed and teleport checks `[lihfolk]`. Use `genres/racing-driving.md` and `genres/rpg-dungeon.md`.
- **Roguelike and roguelite.** Covered in `genres/rpg-dungeon.md`: runs of 10–20 minutes, run state apart from profile state, one server `Random` per run, revives capped and offered after the fight.
- **Puzzle.** The board model is the single source of truth; resolve → gravity → refill → cascade until stable; undo via snapshots including RNG state or reversible commands; detect deadlocks and reshuffle; build generated puzzles backwards from a solved state; lock input while resolving. The client may run a single-player board; the server validates completion by replaying the move list. Pieces are pooled Blender models. Sells: hint packs, extra moves (once per failed level, dismissible), cosmetic boards, starter pack. Escape rooms `[lihfolk]`: three hint tiers per puzzle and every valid solution accepted; answers and puzzle logic only on the server; guesses rate-limited (about 5 per 10 s per player) and distance-checked; interactables highlighted rather than pixel-hunted; group state synchronised for late joiners.
- **Card game.** Every card lives in exactly one zone; atomic transfers; effects as data resolved through a stack or queue; triggers via an event bus; seeded Fisher–Yates shuffle. The server owns every deck and hand and never replicates hidden information (anything in `ReplicatedStorage`, attributes or remote payloads is visible to exploiters). Sells: card backs, boards, starter deck, gift packs; random packs show odds with honest pity.
- **Visual novel and story.** Save anywhere (script position, flags, read lines); typewriter via `TextLabel.MaxVisibleGraphemes` `[VS]`; skip only read text; branch-and-merge structure. Decide early whether multiplayer choices are per-player or votes. Sells: chapter or route passes, outfits, gift passes.

## Level-up: symptoms → likely cause → fix (any genre)

| Symptom in a live game | Likely cause | Fix | Where |
|---|---|---|---|
| High bounce in minutes 1–3 | No action in the first 30 s; lobby, tutorial or veterans in the way | Put the core verb at spawn; protect newcomers | Genre file §First 5 minutes |
| Sessions under 10 min | One loop layer missing; nothing on a timer | Add the next layer and 5/15/30 min timers | Genre file §Core loop |
| D1 fine, D7 collapses | Mid-game wall or no new verb after the first rebirth or zone | Refit curves; add a verb per tier | `economy-and-progression.md` |
| Players call it pay-to-win | Power sold where players compare or compete | Convert to cosmetics and convenience | Genre file §Monetisation |
| Good CCU, low revenue | Pass-only catalogue; no repeatable products; offers at bad moments | Dev-product ladder; positive-moment triggers | `monetization-and-policy.md` |
| Server lag grows with players or waves | Humanoid crowds, physical parts, per-frame replication | Data on the server, pooled visuals on clients | Genre file §Technical hot spots |
| Exploiters ruin leaderboards or fights | Client-trusted amounts, hits or checkpoints | Intent-only remotes; server validation or server authority | `networking-and-security.md` |
| Impressions fall after a clone wave | Near-duplicate title, art or place file | Distinct metadata, art and verb | `market-scan-2026-11.md` |
| Under-16 audience missing | Maturity label or hangout classification | Redesign to Mild and a structured activity; retake the questionnaire | `genres/social-roleplay.md`, `genres/horror-coop-escape.md` |

## Review gate

- [ ] The game is classified by its host loop, and the matching genre file has been read in full.
- [ ] The one new verb or visible journey is named; the pairing was checked against the first 40 search results.
- [ ] For a hybrid: one host, one layer, strictest rule applied.
- [ ] The genre file's level-up checklist was run (live game) or its review gate passed (new game).
- [ ] Asset count fits the Blender pipeline; maturity target and dashboard genre are chosen deliberately.
- [ ] Monetisation deletes what the genre file says to delete; every "Conflict" is resolved in favour of the house rules.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot); `references/knowledge-base.md` §2.11 and §3.2 (read; source of the puzzle, card, visual-novel and sports entries kept here).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/experience-genres.md (read; genre and subgenre list, three-month rule)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/design-for-roblox.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/content-maturity.md (read)
- https://github.com/Roblox/creator-docs/tree/main/content/en-us/production/promotion/rewarded-video-playbooks (read: incremental-sim, tycoon, obby, rpg, shooter, survival, sports)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/templates.md and `resources/boneheads/index.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/` genre playbooks (summaries of Battle Royale, Naval and Open-Sea Adventure, Open-World City and Crime Roleplay, Zombie and Wave Survival Co-op, Puzzle and Escape Rooms; full notes cited in each genre file), `skills/roblox-trend-game/references/trend-games-research.md` (read)
- Full game teardowns: `references/case-studies-teardowns.md`. Systems: `references/gameplay-systems-cookbook.md`.
