# Genre playbooks for Roblox

Distilled from knowledge-base sections 2.11 and 3.2. Each entry gives the loop, the tuning knobs, the Roblox mapping and the monetization hooks that fit the house default product set. Every hook obeys house rule 3: small, dismissible, after a win, rate-limited, no fake scarcity. Rewarded-video benchmarks come from Roblox's genre playbooks (opt-in = share of eligible users who watch at least one ad; frequency = ads per viewer per day) `[VS]`. Market prices are a 2026-11-07 snapshot `[VS]`.

## Choosing a genre

- The 2025–26 hits share one spine: income per second → multipliers → rebirth, plus one new verb (steal, grow, kick, throw) `[VS]`. Put originality in the verb.
- Social beats solo on Roblox; single-player games struggle. Younger players prefer exploration, experimentation and socialising over competition; older players (16+) invest more time and money and form communities.
- Waves are short: mega-hits peak in 7–8 weeks, plateau 2–5 months, fall 90–99% within 6–12 months. Clones win only while the parent is rising; remixes beat reskins; near-duplicate clones are penalised `[VS]`.
- Roblox genre settings: set in Creator Dashboard > Publish Settings > Game Details; changeable only once every three months; the selected genre is not a Recommended For You ranking input `[VS]`.
- For current trends and what to build, consult the owner's vault (`Roblox Research/2026-11 Market Scan/_MOC.md`).

Roblox's three-layer loop test: minute-to-minute interaction (exploring) → most repeated action cycle (fighting) → progression engine (upgrades, collections). Each layer must feed the next. Prototype the loop, UI/UX, rules and edge cases before art.

## Simulator and incremental

- Loop: click or collect → sell → upgrade capacity → unlock the next zone → rebirth.
- Knobs: geometric price curve (about 1.15–1.5× per tier), zone gates, rebirth multiplier (see economy-and-progression.md). The enemy is friction between upgrades. Numbers outgrow meaning: use K/M/B suffixes and a new verb per zone.
- Rewarded video: velocity boosts, doubled offline earnings, energy refills, 10 minutes of auto-click that previews a pass. Benchmark opt-in 13%+, frequency 2.8.
- Sells: 2× Cash, 2× speed, auto-collect pass, Luck for eggs/pets (odds shown), extra pet slots, storage, rebirth skips, starter pack. Market: X2 Money 399 R$, X2 Growth Speed 467 R$, rebirth skip 99 R$.

## Tycoon

- Loop: claim a plot → buy droppers → collect → buy the next button → expand. Drivers: efficiency, accumulation, time management.
- Design the button order as a pacing graph with a visible "next purchase" target at all times. Every purchasable building is a Blender model with a juicy build-in animation.
- Rewarded video: time skip (double offline earnings), progressive rewards (payout grows per consecutive view), progression accelerators. Benchmark opt-in 15%+, frequency 3+.
- Sells: 2× Cash, auto-collect, extra plots, cosmetic base themes, VIP area, gift passes.

## Cozy management (shop, farm, business, warehouse)

- Loop: do the job yourself with your own character in a small 3D space (pick, pack, cook, serve, craft) → earn within a minute → hire workers to automate it → expand the space → idle income. Every hit above 5K CCU is hands-on; menu, map and spreadsheet managers stay under 1K however deep they are (Fleet Empire peaked at 1.8–2K). LINE UP! Metro Tycoon is the one map-based hit because drawing routes plays like a toy.
- Format norms (Nov 2026): Hire 1/5/25 pads; merge 3 workers of a tier into the next tier (staff take the place of pets); a collection index; offline income with a cap; friend bonus 10–20%; 6–8 player servers with one plot each; sessions 15–27 min. See `market-scan-2026-11.md` for the comparison table.
- Pitfalls: heavy decorating raises favourites but shortens sessions; driving is hard for young players, keep it optional; "Sell a Million" and "Run a" names are crowded; near-duplicate risk against My Small Business and Sell a Million Sushi, so theme, art and place file must be distinct.
- Thumbnails: most management tiles are photoreal with no text; a price-flip or income ladder ("$1/s → $9.8M/s", "1 box → 1,000,000 boxes", garage → mega-centre) stands out.
- Sells: mostly cheap repeatable dev products (2× income, rush boosts, cash packs, auto-pack, extra slots), then convenience passes (VIP with offline bonus, extra route or truck slots), gift passes. Staff crates are paid random items (odds shown) or, under the no-luck default, deterministic merge tiers instead.

## Obby and platformer

- Loop: attempt → fail → retry → checkpoint → next stage.
- Feel knobs: jump height 3–4 character heights reaching apex in 0.30–0.40 s; fall gravity 1.5–2× rise; coyote time 0.08–0.12 s; jump buffer 0.10–0.15 s; variable jump (early release multiplies upward speed by 0.4–0.5); apex hang; ground acceleration to full speed in 0.05–0.10 s; wall jump at about 0.8× height with 1.25× sideways kick. Derive `g = 2h/t²`, `v0 = 2h/t`. Player hurtboxes slightly smaller than the visual.
- Roblox: the Humanoid jump is a fixed arc; add buffer and coyote time on the client (see ui-input-crossplatform.md); extra fall force via `VectorForce`/`LinearVelocity` on the client, which owns the character. Design gaps from the metrics table in game-craft.md. Checkpoints are invisible `SpawnLocation`s inside Blender pads; kill zones are Blender models with invisible triggers. Save the highest stage.
- Rewarded video: first-spawn buffs, mid-session currency or item trials, post-failure second chance. Benchmark opt-in 15–25% at frequency 3; best in class 30%+ at 4+ (Glide Tower 47% opt-in on "respawn at previous checkpoint").
- Sells: skip-stage product (only after several failures at the same stage, as a small dismissible button, and only where a free skip route exists), checkpoint saves, trails, speed/gravity coils if they do not break the challenge, VIP, gift passes. A stage skip is a fixed disclosed outcome, not a random item.

## Tower defense

- Loop: prepare (place/upgrade) → survive a wave → earn → repeat.
- Balance: enemy HP grows 1.1–1.2× per wave while income grows linearly; measure tower value as DPS × time in range; targeting modes (first, last, closest, strongest, weakest); leaks cost lives and forfeit bounty; selling refunds about 70%; bonus for calling waves early; telegraph the next wave; enemy variety (fast, armoured, flying, swarm, boss) forces tower variety. Wave rewards must scale with the next tower tier's cost.
- Implementation: BFS before allowing a placement in maze TD; carry leftover distance past waypoints. On Roblox do not give enemies Humanoids: simulate them as data (path distance, HP, speed) on the server and render pooled Blender models by CFrame on clients, interpolating. Range checks via `GetPartBoundsInRadius` or a plain distance check on the data list. Validate placement on the server.
- Sells: 2× Cash (timed), 2× game speed for solo, tower skins, unique towers as passes (balanced against free), extra tower slots, starter pack, gift passes. Summons and crates bought with Robux or with Robux-bought currency are paid random items: full odds disclosure plus `PolicyService` gate. Offers only between waves.

## Roguelike and roguelite

- Loop: generated run → fight and loot → die or win → meta-progress → again. Keep run state and profile state strictly apart; every floor passes the connectivity check.
- Roblox: real-time action roguelites fit sessions better than turn-based; rooms from a Blender kit snapped by `Attachment`s; one `Random` per run seeded on the server; party runs share seed and state; runs of 10–20 minutes so a discovery player can finish one.
- Sells: revive tokens (capped per run, fairly priced), cosmetic classes, timed meta-currency boosts, Luck only if loot rolls exist with odds shown. Offer after the run ends, never on death mid-fight. DOORS sells revives at 30 R$ and gives new players one free.

## RPG

- Loop: quest → fight → XP and loot → stronger → harder quests.
- Stats in layers: base → flat → percent → clamp; never store derived stats (Dirty Flag). Damage: ratio formula `attack × K / (K + defense)` with K about 100 degrades smoothly; ±10% variance; 1.5× crit. Quests as state machines (available, active, complete, turned in) fed by an event bus; dialogue as a data graph with string IDs.
- Roblox: stats, XP and loot on the server; display via attributes; `CollectionService` tags for quest givers and enemies; `LocalizationTable`s; `ProximityPrompt` on an invisible anchor.
- Rewarded video ("a micro-transaction paid for with time"): bypass a crafting cooldown, Second Wind revive, 10-minute Luck Potion, 2× EXP. Guardrails: daily cap, deterministic rewards only, account-bound rewards. Benchmark opt-in 15%+, frequency 3+.
- Sells: 2× EXP, inventory/bank expansion, cosmetic armour and mounts, fast travel, season pass, starter pack, gift passes. Never sell the best gear outright where PvP matters.

## Survival and crafting

- Loop: gather → craft → build → survive the night/round → expand. Needs decay at graded rates with soft penalties first; crafting is atomic; tool tiers gate resources; nodes respawn on timers; recipes form a DAG; threat escalates on a day/night cycle; saves are incremental.
- Roblox: tagged Blender resource nodes with real collision; server-authoritative crafting and inventory; grid-snapped building validated with `GetPartBoundsInBox`; `Lighting.ClockTime` for day/night; structures saved as ID + grid position + rotation.
- Rewarded video: Second Chance revive, pre-round power-up, streak saver, daily kit; deterministic consumables with a daily cap. Benchmark opt-in 13%+, frequency 2.5+. Survival was the hottest genre in late Sep–early Oct 2026 `[VS]`.
- Sells: 2× gather speed, extra storage, cosmetic building themes, starter pack. No pay-to-skip raids in PvP.

## Shooter

- Loop: engage → shoot → reposition → win round → rank up. Hitscan vs projectile; falloff (full to 20 m, floor 0.4× by 60 m); headshots 1.5–2×; recoil as a decaying offset; spread with square-root distribution; `TTK = (ceil(hp / damage) - 1) / fire_rate`; FOV and sensitivity options.
- Roblox: client raycasts immediately for feel; server validates fire rate, ammo, range, line of sight with its own raycast, and hit plausibility against recent positions. The client never reports damage. Pooled tracer meshes or `Beam`s.
- Rewarded video: pre-match 2× XP/credits (never damage, health or aim), armoury currency next to paid bundles, weapon trial for one match, post-match payout boost; never interrupt a fight. Benchmark opt-in 10%+, frequency 3+.
- Sells: skins, cosmetic packs, characters, battle pass with real fixed end dates, 2× XP, gift passes. No purchasable stat advantage in competitive modes.

## Sports

- Loop: match → result → progression → rematch. Rewarded video: post-match boost, currency next to bundles, rematch rescue, pre-game edge lasting one match or session only. Best triggers: before a match, after a loss, after a win. Benchmark opt-in 15%+, frequency 3+.

## Puzzle

- Board model is the single source of truth; resolve → gravity → refill → cascade until stable; undo via snapshots including RNG state or reversible commands; detect deadlocks and reshuffle; generated puzzles built backwards from a solved state; lock input while resolving.
- Roblox: client may run a single-player board; the server validates completion by replaying the move list. Pieces are pooled Blender models.
- Sells: hint packs, extra moves (once per failed level, dismissible), cosmetic boards, starter pack.

## Card game

- Every card lives in exactly one zone; atomic transfers; effects as data resolved through a stack or queue; triggers via an event bus; seeded Fisher–Yates shuffle. On Roblox the server owns every deck and hand and never replicates hidden information (anything in `ReplicatedStorage`, attributes or remote payloads is visible to exploiters).
- Sells: card backs, boards, starter deck, gift packs; random packs show odds with honest pity.

## Visual novel and story

- Save anywhere (script position, flags, read lines); typewriter via `TextLabel.MaxVisibleGraphemes` `[VS]`; skip only read text; branch-and-merge structure. Decide early whether multiplayer choices are per-player or votes. Sells: chapter or route passes, outfits, gift passes.

## Social hangout and roleplay

- Loop: customise self and space → act out scenarios → show off and collect. Players are each other's content. Dense but uncrowded spaces, many sit and pose spots, emotes, light minigames, rotating events with real end dates, many interactable Blender props (doors, vehicles, jobs), roles that create interaction.
- Sells: premium roles, vehicles, houses and estates as convenience passes; cosmetics; emotes; room expansions. Brookhaven sells passes at 275–799 R$ (about 5,716 R$ for everything) while most content stays free. Adopt Me offers the Modern Mansion while the player looks at their basic house (a contextual sale).
- Rating risk `[VS]`: free-form social hangouts are rated 16+ and hangouts with private spaces 18+; for under-18 audiences avoid bedroom/bathroom/closet settings and add bounding-box limits on beds. A roleplay game for Kids and Select audiences needs a structured, activity-led design.

## Horror

- Loop: explore → tension → chase or scare → escape → next floor. Audio and lighting carry the genre; long quiet build-ups; AI telegraphs and misses, with a director controlling pacing; jump scares rare; respect flash and shake options.
- Pre-play shop model (DOORS): lobby sells only the currency, the elevator pre-run shop sells consumables. Asymmetric horror sells points packs and killer-chance packs.
- Rating: mild fear at Mild, moderate fear needs Moderate `[VS]`. Horror peaks near 4× normal players on 28–31 Oct; liminal horror is a rising wave `[VS]`.
- Sells: revives (never during a chase), cosmetic flashlights, extra lives in party modes.
