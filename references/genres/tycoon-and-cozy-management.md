# Tycoon and cozy management playbook

Covers plot-based income games: the classic button/dropper tycoon and its 2026 successor, hands-on cozy management (shop, farm, business, warehouse). Open it when the concept is "own a plot, earn per second, expand", or when auditing a live tycoon whose sessions are short or whose players go AFK. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | Auto-assigned plot; a button chain of 20–30 purchases stored as data; server income tick with no physical drops; save purchase ids; one visible next button | Workers, merge tiers, rebirth, offline income, decoration, raids |
| Intermediate | A hands-on job before automation; Hire pads; payback sheet with `wait(k)` plotted; silent rebuild on join; capped offline income; client-only visual drops with pooling | Routes or map toy, co-op plots |
| Expert | Merge tiers and an index; rebirth that keeps the best staff; friend-help bonus; schema migrations for a changing chain; telemetry on the wait curve and per-pad drop-off | — |

Terms: *button chain* = the ordered list of purchasable pads; *payback time* = cost ÷ income added; *dropper* = a machine that produces the items that become cash.

## Snapshot

- Market position (vault, 2026-11-07): cozy management is **rising with a real middle tier**. My Small Business 20.0K CCU (peak 44.8–46K), Sell a Million Sushi 12.9K, LINE UP! Metro Tycoon 11.6K, Run A Farm! 10.2K. Classic and army tycoons hold a similar tier: Command An Army 15.4K, Military Army Tycoon 11.3K, Build a Phone Empire 9.0K, Restaurant Tycoon 3 8.0K (evergreen). Menu, map and spreadsheet managers sit at 284–993 CCU however deep they are (Fleet Empire peaked at 1.8–2K).
- About 25% of the owner's second feed was management/tycoon tiles. Third-party trackers call the idle-tycoon tail "extremely saturated" `[community]`; "Sell a Million ___" copycats sit at 3–116 CCU and most "Run a ___" games under 100 (vault).
- Audience: young and casual, low skill floor, plays in short bursts and returns for offline income.
- Session shape (vault): 15.2 min (My Small Business), 15.6 (Sushi), 20.7 (LINE UP!), 21.3 (Run A Farm!), 26.7 (Sari-Sari Store); decorating-led Pocket Landlord only 7.9 min. Target 19+ min.
- Servers: 6–8 players, one plot each (LINE UP! runs 50). D1 for tycoons with traffic is reported at 20–28% by one tracker; the GameAnalytics median for 19–24 min sessions is 11.5% `[VS]`. Compare against your own Creator Analytics benchmark.

## Core loop with timings

| Step | Classic tycoon | Cozy management | Target |
|---|---|---|---|
| Arrive | Claim a plot | Spawn on your own pre-assigned plot | Plot owned within 10 s `[house]` |
| Earn | Dropper → conveyor → collector | Do the job by hand in a small 3D space (pick, pack, cook, serve) | First cash within 60 s (vault: playable within a minute) |
| Spend | Step on the next button | Upgrade pad, then Hire 1/5/25 pads | First 10 purchases 3–10 s apart |
| Automate | More droppers, upgraders | Staff do your job; you move to the next station | First hire by minute 2–3 `[house]` |
| Expand | Walls, floors, new wing | Bedroom → warehouse; garage → depot → hub | A new room about every 3–5 min in session 1 `[house]` |
| Reset | Rebirth for a multiplier | "Go public"/prestige, keep best staff | First rebirth at 20–40 min of play `[house]` |

- Loop layers: carry and place (seconds) → order or batch complete (30–90 s) → new station or staff tier (minutes) → rebirth (session).
- Timed spikes keep active play worthwhile: a rush window every 15 min at a stated multiplier (the vault's warehouse concept uses 5× pay), restocks, a weekly new city or cargo type.
- Button-chain rules `[lihfolk]`: start with a free or near-free button so the first input is a purchase; alternate income and spectacle; keep 1–3 buttons available at once (one is a corridor, ten is a menu nobody reads on a phone); place the next button beside the thing just built; end each stage with a big reveal (a floor, a roof, a vehicle).

## First 5 minutes

1. 0:00 spawn facing your plot's first station; one Blender-modelled prompt, no text wall.
2. 0:10 first hand-made item; 0:30 first sale with a cash pop and sound.
3. 1:00 first upgrade pad lights up with its price; the next locked pad is always visible.
4. 2:00 first Hire pad; the worker visibly does the job you just did.
5. 3:00 income per second appears on the HUD; 4:00 second station or room; 5:00 a silhouette of the next building tier with its cost.
- No offer cards in this window (offer gate: 10 min of play and a first win). The first number-go-up moment must land before 180 s (vault launch checklist).

## Progression and economy shape

- Drivers `[official]`: efficiency, accumulation, time management. Button order is a pacing graph: draw price against minute-of-play before building; one visible "next purchase" at all times. Every purchased building is a Blender model that appears with a juicy build-in animation.
- Costs: geometric, `g` 1.07–1.15 for common pads, 1.5–3 for building tiers (economy-and-progression.md). Income per pad grows slower than its cost so the wait ratio creeps up toward rebirth.
- Staff are the collection: Hire 1/5/25 pads; merge 3 of a tier into the next (Rookie → Legendary); an index of everything produced or sold (Sushi: 24-fish index). Reuse one Blender worker mesh with material and accessory variants per tier.
- Rebirth: multiplicative `q` with wait ratio ×1.2–1.5; keeps cosmetics, index and passes.
- Offline income: `min(away, cap) × rate × 0.25–0.5`, cap 8–12 h, cap stated in the UI.
- Sinks: staff tiers, building tiers, decoration (cosmetic only), route or truck slots. Friend bonus +10–20% while a friend is in the server or helping on your plot.
- Payback maths `[lihfolk]`: payback = cost ÷ added income. Early income buttons pay back in 10–60 s; payback grows slowly along the chain (about ×1.1–1.3 per income button). Decorations have zero payback, so space them so the wait never exceeds the stage target (about 2 min early, 5–10 min late), and put a spectacle button right after any long wait. In a sheet, compute `wait(k) = max(0, cost(k) − cash) ÷ incomePerSecond` for every row and plot it: spikes are where players leave.
- If players can choose the order they will buy the best payback first: enforce the intended order with prerequisites, or make payback equal across simultaneous choices so the choice is about looks `[lihfolk]`.
- Long loops after the plot is finished `[lihfolk]`: rebirth (keep cosmetics; players dislike losing a decorated base), more stages, upgrade tiers, decoration, a management layer (the vault's winning answer), leaderboards. Raids only as opt-in with shields and losses limited to temporary resources.
- Conflict (offline cap): LihFolk suggests about 2 hours at 50% because long caps devalue playing; this skill's default is 8–12 hours at 25–50% so an overnight return pays. Keep the longer cap for the day-1 return, use the lower efficiency, and state the cap either way.

## Monetisation set that fits

- Keep from the default set: 2× Cash 10/30 min, 2× Speed (work, delivery), Starter Pack, currency packs, Auto-Collect, extra slots, permanent 2× Cash, VIP (+25% offline income is the vault's concept value), gift passes, private servers.
- Add: rush-boost (start a rush window now), Auto-Pack, extra route or truck slots, a 2× offline-earnings claim on return.
- Delete: 2× EXP (no XP), Revive, and Luck / Server Luck unless staff crates exist. Under the no-luck default, staff come from deterministic merge tiers; if you ship crates they are paid random items (odds shown, `PolicyService` gate).
- Mix (vault): cheap repeatable dev products carry the format. My Small Business 39 dev products; LINE UP! and Run A Farm! have no passes at all.
- Price cash packs as "N minutes of your current income" so they stay relevant after rebirth without breaking the curve `[house]`.
- Rewarded video `[official]`: time skip (double offline earnings on return), progressive rewards (payout grows per consecutive view), progression accelerators. Benchmark opt-in 15%+, frequency 3+.
- Never put a Robux-only pad on the main button path; premium pads sit to the side, clearly marked `[house]`.

## Retention and social hooks

- Offline income with an honest cap is the D1 hook; the return card shows what was earned and what the cap was.
- Fixed weekly update day; rush every 15 min; daily restock of a rotating shop; index completion rewards.
- Co-play: help on a friend's plot for a shared bonus, private servers, visit-and-rate. These are intentional co-play and feed the discovery signal; random matchmaking does not.
- No streak-loss mechanics; a cumulative login calendar instead.

## UI patterns

- HUD: cash, income per second, one "next goal" chip. Prices live in the world on the pad (BillboardGui on a Blender pad), not in a menu.
- Number ladder as identity: `$1/s → $9.8M/s`. Management thumbnails are mostly photoreal with no text, so a number-style tile stands out (vault).
- One panel deep at most; any map or route layer is a toy (drag coloured lines), never a table.
- Mobile: carry/place on a single large context button; pads trigger by walking onto them, no precision taps.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §16 Plots, tycoon ownership and placement, §1 Currency and wallet, §3 Shop, §5 Upgrades and rebirth, §13 NPC and enemy spawning and AI, §7 Daily rewards and playtime rewards, §24 Server-wide events and boosts. Its "Build order by genre" table gives a second opinion.

1. Plot assignment, ownership and release.
2. Button chain as data; purchase pads with server validation.
3. Server income tick and cash HUD.
4. Player data: purchase ids, cash; silent rebuild on join.
5. Client visual drops or hands-on job stations (carry, place, serve).
6. Hire pads and client-rendered workers.
7. Offline income and return card.
8. Shop: boosts, passes, gifting.
9. Merge tiers and index.
10. Rebirth; then friend-help, events (rush windows), decoration.

## Technical hot spots

- **Droppers are the classic performance trap.** Community reports of tycoons becoming unplayable on low-end devices trace to unanchored drop parts `[community]`. Compute income as numbers on a 1 Hz server tick; render conveyor items on each client from pooled Blender meshes moved by CFrame; cap visible items per plot; late-game droppers credit the bank directly.
- **Workers**: no Humanoids. Server stores counts and tiers; clients animate pooled rigs with `AnimationController` along fixed paths. Other players' plots show a reduced crowd.
- **Plot save**: persist purchase IDs (set or bitfield), staff counts per tier and decoration as `{id, cell, rot}`; never serialise instances. Rebuild on join in slices (about 5 ms per frame) to avoid a hitch. One key holds 4,194,304 characters `[official]` `[VS]`.
- **Plot lifecycle**: assign on join, release and clean on `PlayerRemoving`; plot models streamed as units (`Atomic`; `PersistentPerPlayer` for the owner's own plot, see performance.md) `[VS]` so neighbours do not pop in piecewise.
- **Exploit surface**: every pad purchase checks plot ownership, prerequisite, price and distance on the server; "collect" remotes carry no amount; merge consumes three and grants one in a single server step; decoration placement is clamped to the plot grid; offline income uses server `os.time()`, never a client clock.
- **Numbers**: move to mantissa/exponent before balances approach 1e15.
- Scale of the dropper trap `[lihfolk]`: 8 plots × 15 droppers × one drop a second, each living 8 s, is about 960 live physics parts; the data version is one loop over the plots and two attribute updates per player per second. Cap visual drops at about 40 per nearby plot (15 on low-end phones), pooled, and none for far plots.
- If the game's identity really is physical (ore sorting, contraptions), cap active parts per plot and keep money independent of physics outcomes so a lag spike never costs the player cash `[lihfolk]`.
- Rebuild silently: a returning player with 150 purchases sees them all at once; animate only new purchases. When the chain changes after launch, migrate old ids in a versioned load step `[lihfolk]`.
- Players do not keep the same physical plot across servers: rebuild owned ids into any free plot. Auto-assignment avoids every plot being held by idle players `[lihfolk]`.

## The one-new-verb angle

- The job is the verb. Pick one hands-on action that is fun at 30 seconds and still readable at scale: pack neatly, flip a car, draw a route, bid on a locker.
- Give the plot a visible journey (garage → mega-centre) rather than a longer menu. LINE UP! is the one map-based hit because drawing routes plays like a toy (vault).
- Unclaimed pairings in the vault: hands-on warehouse fulfilment plus drawn routes (best hybrids under 2.3K CCU).

## Common failure modes

- Menu or spreadsheet management: deep, liked (Fleet Empire 88.5–89% likes) and still under 1K CCU.
- Nothing to do while waiting, so players AFK and sessions end at the first long price.
- Decoration as the main loop: favourites up, session length down.
- Required driving: hard for young players; keep it optional.
- Near-duplicate of My Small Business or Sell a Million Sushi (theme, art, place file): exposure penalty. Format clones get about two weeks of attention (vault).
- Robux pads in the main path; plots that fail to save; income outrunning prices after the first rebirth.
- Ten buttons visible at once; payback rising sharply mid-chain; a rebuild animation for every owned button on join `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First cash within 60 s, first purchase within 90 s | Cut the intro; pre-assign the plot; put the first station at spawn |
| 2 | Player does something with their hands in minute 1 | Add a manual job in front of the first dropper or station |
| 3 | A next purchase is always visible and under 2× current cash at the median | Re-plot the price curve; insert bridge pads |
| 4 | Median session ≥ 15 min, aim 19+ | Add rush windows, a second station type, merge tiers |
| 5 | Hire/automation arrives by minute 3 | Move the first Hire pad earlier and make its effect visible |
| 6 | Offline income exists, is capped and stated | Add the return card with an honest cap; sell the 2× claim there |
| 7 | Server MicroProfiler shows no physics spike with 6–8 full plots | Replace physical drops with data plus client visuals |
| 8 | Workers and customers use no Humanoids | Swap to client-rendered pooled rigs |
| 9 | Purchases save and reload identically after a rejoin | Save IDs, not instances; test with a full plot |
| 10 | Dev products outnumber passes; three or more cost under 50 R$ | Add repeatable boosts, cash packs, rush boost |
| 11 | No Robux-only pad blocks the path | Move premium pads to a side wing |
| 12 | A collection exists (merge tiers, index) | Add staff tiers on reused meshes and an index panel |
| 13 | Friend bonus and plot visits work | Add +10–20% co-play bonus and a help action |
| 14 | Title and art differ from the nearest hit | Rename away from "Sell a Million"/"Run a"; restyle |
| 15 | `wait(k)` plotted for the whole chain with no spike above the stage target | Insert bridge or spectacle buttons; smooth payback growth |
| 16 | 1–3 buttons available at any moment | Add prerequisites; hide the rest |

## Review gate

- [ ] The core job is hands-on in 3D; any map layer plays like a toy.
- [ ] Price graph drawn against minutes; first rebirth lands inside session 1 or 2.
- [ ] Income is server-computed; no physical drop parts; no Humanoid workers.
- [ ] Plot save is ID-based and tested full; plot releases cleanly on leave.
- [ ] Product set is dev-product-led; no paid pad on the main path; any crate shows odds and respects `PolicyService`.
- [ ] Offline cap stated; no streak-loss mechanics.
- [ ] Every pad, station, worker and building is a Blender model with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/tycoon.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/plant-reference-project.md (read; official plant-and-sell reference project covering persistence, FTUE, networking)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud-services/data-stores/error-codes-and-limits.md (read)
- https://devforum.roblox.com/t/unable-to-progress-tycoon-incremental-due-to-immense-physics-lag-on-low-end-devices/3587271 (search summary)
- https://devforum.roblox.com/t/tycoon-optimization-and-architecture/4574342 (search summary)
- https://devforum.roblox.com/t/best-practice-for-efficient-tycoon-droppers-and-moving-parts/339303 (search summary)
- https://devforum.roblox.com/t/tycoon-saving-compression/3840092 (search summary)
- https://rolearn.dev/insights/genre-saturation-opportunity (search summary; third-party)
- https://github.com/evilbocchi/eternal-empire (read README; 17 stars, CC BY-NC 4.0, roblox-ts tycoon; reference only, non-commercial licence)
- https://github.com/B-Ricey763/Roblox-Studio-Tycoon (search listing; 34 stars, no licence, 2022 tutorial code; reference only)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Tycoons.md`, `43 Genre Systems End to End/Tycoon Plots and Droppers End to End.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
