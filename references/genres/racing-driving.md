# Racing and driving playbook

Covers lap and sprint racing, open-world driving and car collection, drift and stunt parks, and vehicle life games. Open it when a vehicle is the player's main body, when choosing a chassis and a netcode model, or when auditing a live driving game for flings, missed checkpoints, mobile handling and a thin car economy. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One free starter car that feels good on the first corner; one loop road; driver-owned car with server speed checks; a spawn button with one car per player | Tuning menus, traffic AI, licensed looks, ranked racing, aircraft and boats |
| Intermediate | Server-timed checkpoints with plane-crossing tests; garage and saved customisation; chase camera with speed effects; touch and gamepad assists; streaming tested at top speed | Raycast chassis rewrite, performance classes |
| Expert | Raycast or custom chassis tuned per class; ghost replays and clean-lap leaderboards; class-normalised ranked races; server authority mode for competitive modes; statistical cheat review | — |

Terms: *network ownership* = which machine simulates an unanchored assembly; *raycast car* = a single body whose suspension and grip are computed from rays cast down, with no physical wheels; *DNF* = did not finish.

## Snapshot

- Market position (vault, 2026-11-07): **steady middle tier, micro-waves on top**. Driving Empire 33K CCU, Kukirin Life about 29K. The Aug–Sep 2026 scooter and bike launches were a micro-wave (Drive A Kukirin 109K peak, now 6–29K each) and are cooling.
- LihFolk's teardown of the genre leader `[lihfolk]` `[VS]`: 31.8M favourites (players bookmark car games and return), all-time peak 89.6K on 15 Aug 2026, average session about 16.4 min, 22-player servers, dashboard genre Simulation › Vehicle Sim. Its CCU reading (16.7K on 29 Oct) differs from the vault's because CCU swings 2–3× by hour.
- Third-party trackers list driving among categories with search demand and thin competition `[community]`.
- Two families `[lihfolk]`: *racing* (laps, times, positions) and *open-world driving* (cruise, collect, jobs, meets). The open-world model retains better on Roblox: driving is fun alone, cars are a collection, the map is a social space. Pure racing needs full lobbies and scares off newcomers; the common winner is an open world with races as optional activities.
- Audience: slightly older, collection-driven, gamepad share above the platform norm. Driving controls are hard for young players (vault).

## Core loop with timings

| Family | Layer | Length | Content |
|---|---|---|---|
| Racing `[lihfolk]` | Corner | 2–5 s | Brake, turn in, accelerate out |
| | Lap | 30 s–2 min | Learn the track, beat your time |
| | Race | 2–6 min | Positions, overtakes, finish |
| | Meta | Weeks | Cars, upgrades, rank, time boards |
| Open world `[lihfolk]` | Drive | Minutes | Cruise, explore, drift, show off |
| | Activity | 2–10 min | Job, race, delivery, chase, drift challenge |
| | Session | 30–90 min | Earn, buy or upgrade, hang out |
| | Meta | Months | Garage collection, customisation, rare cars |

- Race start: a lobby or in-world start line with a 10–20 s joinable countdown; a DNF timer of about 30 s after the winner so one idle player cannot hold the lobby `[lihfolk]`.
- Rubber-banding (slight help for trailing cars) keeps casual races close; switch it off in ranked and time-trial modes and never make it visible as unfair `[lihfolk]`.

## First 5 minutes

1. 0:00–0:30 driving a free starter car; no garage menu before the first drive `[lihfolk]`.
2. 1:00 first corner taken well: the first minute is a handling test, and players who like the starter car stay `[lihfolk]`.
3. 2:00 first signposted activity (a short race or delivery) with a quick first payout.
4. 4:00 first upgrade or paint change bought; the stat or look change is visible.
5. 5:00 the next car shown in a showroom or driven past by another player.
- Target: first upgrade inside session 1, first new car within one or two sessions `[lihfolk]`.

## Progression and economy shape

- Cars are the collection and the status ladder. Money from driving, races, jobs and events buys cars; customisation (paint, rims, kits) is the expression layer.
- Car data lives in one module: speed, acceleration, handling, price, unlock rule, tuning ranges. Upgrades (engine, tyres, suspension) show visible stat changes.
- Performance classes (cars grouped by rating) let free and paid cars race fairly `[lihfolk]`.
- Limited cars drive returns when their end dates are real. Sinks: upgrades, customisation, garage slots, entry fees for high-stakes events.
- Leaderboards: per-track best lap and best race, clean laps only (a lap with any plausibility flag does not count) `[lihfolk]`.
- Use original car designs. Real brands and liveries need a licence; the genre leader's are partnerships `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: 2× Cash 10/30 min, Starter Pack (a fixed car or kit), currency packs with care, extra slots (garage), VIP, gift passes, private servers (car meets, friend races).
- Add: premium cars with stats inside the range of the best earnable cars, customisation packs, event cars that are also earnable, area or vehicle-class access passes, a radio pass only with licensed audio. Observed pass prices in the genre leader `[lihfolk]` `[VS]`: VIP 500 R$, track pass 450, class passes 199–399, small utility passes 15–125.
- Delete: Luck, Revive, Auto-Collect, 2× EXP unless a level track exists.
- House rule 3: no paid top speed, grip or nitro in ranked or timed modes. Ranked uses normalised classes; premium cars belong to open-world showing off.
- Rewarded video: the sports playbook applies `[official]` (post-race payout boost, a one-race trial of a car; boosts last one race or session; opt-in 15%+, frequency 3+).
- Offers at the garage, the showroom and the results screen; never while driving.

## Retention and social hooks

- Car drops on a fixed cadence, often several per update, with one event car per season `[lihfolk]`.
- Social spaces for meets: parking areas, showrooms, a drag strip. Players are each other's showroom.
- Time-trial ghosts of friends; weekly track or route rotation; cruising with passengers.
- Weekly limited events with honest end dates.

## UI patterns

- Race HUD: position, lap, split delta, speedometer, minimap driven from replicated data (not from car models, which may be streamed out) `[lihfolk]`.
- Chase camera with speed-based field of view, look-back and optional first person; engine pitch by RPM, tyre squeal, collision sounds `[lihfolk]`.
- Touch: steer left/right or a small stick, throttle and brake on the right, auto-accelerate option and steering assist. Gamepad: analogue triggers. Keyboard: digital with smoothing.
- Spawn menu (pick from garage, car appears beside you) for convenience; physical dealerships for showing off; many games use both `[lihfolk]`.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §20 Checkpoints and obby stages, §10 Rounds, match state machine and intermission, §9 Leaderboards, §2 Inventory and equip, §3 Shop. Its "Build order by genre" table gives a second opinion. Vehicle construction is in `references/physics-and-vehicles.md`.

1. Vehicle controller (input for keyboard, touch, gamepad) and one chassis.
2. Vehicle spawner with per-player cap, ownership on sit, despawn on leave and when abandoned.
3. Chase camera and speed effects.
4. Player data: cash, owned cars, customisation.
5. Garage and shop.
6. Checkpoints, laps and server race timing; race lobby and results.
7. Leaderboards per track.
8. Customisation and upgrades.
9. Anti-exploit checks for speed, teleport and flight.
10. Events and limited-car scheduler.

## Technical hot spots

- **Chassis choice** `[lihfolk]`: `VehicleSeat` with hinge wheels (fastest to build, bouncy; casual and roleplay); constraint-based suspension (springs, hinges, cylindrical constraints; most driving games); raycast car (most code, most stable at speed; racing and drift). A wheel catching a seam at 150 studs/s can launch a physics car; a raycast car has no wheels to catch. `VehicleSeat` exposes `ThrottleFloat` and `SteerFloat` `[VS]`.
- **Network ownership**: the driver's client owns the driven car; the server owns idle cars. Set ownership on sit and reset on exit. Community threads report jitter on hand-off, flings on car-to-car contact and laggy passengers `[community]`; keep mass ratios sane, mark decorative parts `Massless`, and use collision groups for cars versus characters and for ghost cars in races.
- **Collision at speed**: thick barriers and simple collision boxes; long road pieces with few seams. Every visible mesh stays solid (house rule 2), so author a simple, thick collision shape per Blender road and barrier piece instead of relying on detailed render-mesh collision.
- **Race timing on the server** `[lihfolk]`: `Touched` gates miss fast cars (150 studs/s is 5 studs per tick at 30 Hz), time imprecisely and ignore direction. Each tick, test the segment from the car's previous to current position against the next gate's plane within its bounds, forwards only; interpolate the crossing time between samples (removes up to 1/tick-rate of error, 33 ms at 30 Hz). Allow two gate crossings per tick for chicanes. Rank positions at about 4 Hz, not every frame.
- **False starts**: anchor the chassis until GO, then un-anchor and hand ownership to the driver; no detection code needed `[lihfolk]`.
- **Speed plausibility resets, it does not ban** `[lihfolk]`: a physics glitch looks like a speed hack. Reset to the last gate and flag the lap; measure the real top speed of the fastest honest car before setting the threshold. A driver-owned car can still cheat slightly under the threshold; only server authority or statistics close that gap.
- **Server authority model** `[official]` `[VS]`: documented for racing; evaluate for ranked modes in new projects.
- **Streaming**: cars outrun streaming. Stream ahead with `Player:RequestStreamAroundAsync`, make vehicle models `Atomic` so they arrive whole, and tune the target radius for top speed.
- **Car count**: about twenty driven cars per server is normal; a hundred idle ones is not. Cap one or two per player and despawn abandoned cars after 60–120 s `[lihfolk]`.
- **User content**: plate text and car names go through `TextService` filtering per viewer; decals only from an approved list.
- **Mobile**: frame drops change handling at speed; test the top car on a 3 GB phone. Car models need LODs and triangle budgets.

## The one-new-verb angle

- Change what driving is for: deliver, chase, drift for score, flip cars for profit (Mechanic Legends, in the vault's management table), carry something fragile.
- Or change the vehicle: the 2026 micro-waves were scooters and bikes; small vehicles are cheap to model and read well on phones.
- A realistic fleet spreadsheet is not a verb (vault: under 1K CCU).

## Common failure modes

- Server-owned driven cars: input lag, players leave in the first corner.
- Detailed mesh collision on roads; cars launch off seams.
- Unlimited spawned cars; server physics collapses.
- Client-reported lap times; boards fill with impossible times.
- Bans on a speed threshold that honest glitches cross.
- Garage or dealership walk before the first drive.
- Real car brands without a licence.
- Touch controls untested at top speed; mobile players cannot hold a lane.
- Paid cars that win ranked races.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Driving within 30 s of joining | Spawn the starter car beside the player |
| 2 | Starter car is pleasant on touch, gamepad and keyboard | Add assists; retune steering curve per device |
| 3 | Ownership set on sit, reset on exit | Add explicit ownership calls and exit handling |
| 4 | No flings at full server load | Collision groups, mass audit, simpler collision |
| 5 | Races timed by server plane-crossing with interpolation | Replace `Touched` gates |
| 6 | Wrong-way and gate-skipping cannot count | Forward-only, in-order gates |
| 7 | DNF timer and anchored countdown exist | Add both |
| 8 | Speed checks reset, thresholds measured | Measure top honest speed; reset and flag |
| 9 | Streaming holds at top speed; cars arrive whole | Stream ahead; `Atomic` vehicles |
| 10 | Per-player spawn cap and idle despawn | Add caps and a 60–120 s timeout |
| 11 | Ranked uses classes; nothing sold wins races | Add performance classes; rebalance premium cars |
| 12 | First upgrade in session 1 | Raise early payouts; cheapen first upgrade |
| 13 | Meet spaces and a car-drop cadence exist | Add a showroom lot; schedule drops |
| 14 | All custom text filtered; decals allow-listed | Audit entry points |

## Review gate

- [ ] Family chosen (racing, open world or both) and the starter-car handling approved on a phone.
- [ ] Chassis type and ownership rules written down; collision authored for speed.
- [ ] Race timing, ordering and leaderboards are server-side with clean-lap rules.
- [ ] Streaming, spawn caps and physics load tested with a full server.
- [ ] Premium cars sit inside the earnable stat range; ranked is class-normalised.
- [ ] Cars, roads, barriers and props are original Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Racing and Driving.md`, `43 Genre Systems End to End/Racing Laps and Checkpoints End to End.md`, `60 High-Craft Game Teardowns/Teardown - Driving Empire.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/templates.md (read; Racing template)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/sports.md (read)
- https://devforum.roblox.com/t/how-to-get-physics-to-chill-out-when-handing-over-network-ownership/2152568 (search summary)
- https://devforum.roblox.com/t/vehiclescars-driven-by-different-players-fling-sometimes-when-colliding/2791026 (search summary)
- https://devforum.roblox.com/t/if-cars-network-owner-is-set-to-driver-it-makes-every-moving-object-laggy-on-passengers-screen/4732327 (search summary)
- https://rowatcher.com/news/roblox-genre-opportunity-map-2026-where-smart-developers-are-building-next (search summary; third-party)
- https://github.com/Astrophsica/Racing-Kit-Roblox (read README; 2 stars, MIT; go-kart kit distributed as a toolbox model; reference only, never ship)
- See also `references/case-studies-teardowns.md` for full game teardowns.
