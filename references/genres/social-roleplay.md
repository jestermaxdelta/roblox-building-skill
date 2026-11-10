# Social roleplay and life-sim playbook

Covers town and life roleplay, role-driven RP (jobs, emergency services, school), fashion and dress-up shows, avatar games and social hangouts. Open it when players are each other's content, when deciding how the maturity questionnaire will classify the game, or when auditing a live RP game for reach, moderation load and monetisation depth. Market numbers are the vault's 2026-11-07 snapshot `[VS]`.

## Snapshot

- Market position (vault, 2026-11-07): **evergreen and dominant at the top**. Brookhaven RP 438K CCU (#2 on the platform; no goals; 115+ houses, 190+ vehicles; updates every Friday), Adopt Me! 167K (pets plus trading inside a life-sim), Dress To Impress 67K (651K peak in Aug 2024; celebrity and IP collaborations), Catalog Avatar Creator 52K.
- Evergreens swing 2–5× on events and updates. New entrants face incumbents with years of content; the openings are a new structured activity (as Dress To Impress did with a timed runway) rather than a bigger town.
- Roblox's own guidance: many players treat the platform as a place to hang out; Brookhaven is "house" for kids; younger players prefer exploration, experimentation and socialising over competition `[official]`.
- One tracker reports D1 15–22% for roleplay games with traffic `[community]`. Sessions are long and unstructured; return is driven by friends and fresh props.
- **Classification decides reach** `[official]` `[VS]`: a game whose primary activity is talking or interacting through chat is a *social hangout*: 16+ only, or age-verified 18+ if it includes private spaces (enclosed spaces designed for one person or a very small number, such as a bathroom stall, bedroom or small tent). A *roleplay* game is exempt only when adopting a role and using in-game items to play it is central. A title or description that references hangouts triggers the hangout classification. Free-form user creation (drawing or writing shown to others) is also 16+; assembling houses or outfits from 3D assets is not. Conflict: a summary of the Aug 2025 safety announcement gives ID-verified 17+ for hangouts with private spaces; the current docs say age-verified 18+. Follow the docs and re-check.
- Chat is off by default for Roblox Kids and for self-declared Select accounts `[official]` `[VS]`; a game for under-16s must work without text chat.

## Core loop with timings

| Variant | Loop | Timing |
|---|---|---|
| Town / life RP | Customise self and space → pick a role or place → act out scenes with others → show off and collect | No fixed cycle; a new toy to try every 1–2 min in session 1 `[house]` |
| Role-driven RP | Choose a job → use its tools → serve or oppose other roles → earn → unlock vehicles and gear | Job task 1–3 min `[house]` |
| Fashion show | Theme announced → dress → runway → player votes → podium | Dress To Impress: 6 min to dress (vault) |
| Avatar / outfit | Browse → try on → save and share → buy | Seconds per try-on |

- Structured activities are the safe design for under-16 reach: rounds, jobs, shows and minigames give the game a primary activity that is not chat.
- Roles should create interaction by design: staff and customers, police and civilians, judges and contestants.
- Space design: dense but uncrowded, many sit and pose spots, light minigames, many interactable Blender props (doors, vehicles, job tools).

## First 5 minutes

1. 0:00 spawn in a busy plaza beside three obvious toys (vehicle spawner, house door, job board).
2. 0:20 first interaction that changes the avatar or its vehicle; no currency needed.
3. 1:00 claim a house or locker with one tap; it is yours for the session and remembers its setup.
4. 2:30 first role or round joined; quick-chat or emote wheel taught by one prompt.
5. 5:00 first shared moment (a show result, a job completed with another player) and a visible premium item seen in use by someone else.
- Most content is free and usable immediately (vault: Brookhaven keeps most content free). Do not gate the first toys behind currency.

## Progression and economy shape

- Two workable shapes: **no progression** (Brookhaven: everything is a toy; revenue from premium toys) or **soft progression** (earn from jobs or shows; spend on cosmetics, furniture, vehicles; ranks unlock roles).
- Status is cosmetic: houses, vehicles, outfits, ranks, rare seasonal items. Retired items gain value honestly when retirement dates are real (Dress To Impress retires items; MM2's old seasonal knives gained trade value).
- Currency sinks: furniture, vehicle customisation, outfit pieces, pet care, plot upgrades. Daily login adds a cumulative track, not a streak that resets.
- Fashion rounds: voting needs anti-collusion (hide voter identity, drop outliers, cap self-vote); rewards are stars toward ranks.
- Trading (pets, items) is a years-long retention engine and a scam surface; see `pet-collection-hatching.md`.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic plus convenience), gift passes (gifting is native to the audience), private servers priced low (Roblox advises against prohibitively expensive private servers) `[official]`, Starter Pack as a cosmetic bundle, currency packs if a soft currency exists.
- Add: premium houses and estates, vehicle packs, role or job passes, emote packs, furniture packs, pose packs, runway effects, seasonal bundles with real end dates. Vault: Brookhaven passes run 275–799 R$, about 5,716 R$ for everything.
- Contextual sale `[official]`: Adopt Me offers the Modern Mansion while the player looks at their basic house. Show premium items in use in the world; sell from the object, not from a pop-up.
- Avatar items sold in-experience pay a 40% affiliate share `[VS]`; a try-on booth is a store.
- Delete: 2× Cash and 2× EXP unless soft progression exists; Luck; Revive; Auto-Collect; anything that sells votes or round wins (house rule 3: fashion shows are competitive).
- Dress To Impress sells items and VIP (vault); VIP wardrobes are cosmetic choice, which is acceptable as long as free players can still win.

## Retention and social hooks

- Fixed weekly update day with new props (Brookhaven Fridays, Dress To Impress Saturday boutique).
- Friends are the retention system: join-friend prompts, shared houses, party vehicles, private servers. Intentional co-play feeds discovery.
- Seasonal events with real end dates; collaborations if available.
- Emotes, poses and photo spots produce shareable images.

## UI patterns

- A radial or bottom-sheet menu for avatar, house, vehicle and roles; one tap to spawn a vehicle; one tap to go home.
- Quick-chat and emote wheels that work with chat disabled; role tags above heads.
- Catalogue grids with large thumbnails, try-on before buy, owned and premium clearly marked.
- Voting UI: stars or sliders with a short timer, results as a podium.
- Report and mute within two taps; house lock and "ban from house" controls for owners.

## Technical hot spots

- **Maturity and private spaces**: design interiors so they are not "private spaces" if the under-18 audience matters: open-plan rooms, no lockable single-occupancy rooms, no bathroom stalls, bounding-box limits on beds. Retake the questionnaire when content changes `[official]`.
- **Text everywhere**: any player-entered text shown to others (house names, signs, pet names, outfit names) goes through `TextService:FilterStringAsync` with the right context. Avoid free-form drawing or writing surfaces unless 16+ is acceptable.
- **Server population**: 20–50 avatars with layered clothing and vehicles is the performance problem. Budget avatar cost, cap accessories rendered at distance, and stream the map.
- **Vehicles**: the driver's client owns the vehicle for responsiveness; community reports describe jitter on ownership hand-off, flings on vehicle-to-vehicle collision and passengers seeing lag `[community]`. Set ownership explicitly on sit and on exit, disable constraints when empty, cap speed on the server, despawn idle vehicles.
- **Houses**: per-player plots or instanced interiors; save furniture as `{id, cell, rot}`; lock and permission checks on the server; streaming keeps other houses out of memory.
- **Avatar editing**: `HumanoidDescription` applied on the server; validate asset ids against an allow-list for in-game items; saved outfits as id lists.
- **Griefing surface**: fling and physics abuse (collision groups, no player-pushable heavy props), seat traps, tool spam, vote collusion, house invasion. Every social feature gets a "how could a stranger ruin this" answer.
- **Exploit surface**: currency grants from job remotes (server tracks task completion), vehicle and item spawn remotes (ownership checks, rate limits), teleport into locked houses (server-side door state).

## The one-new-verb angle

- Give the hangout a structured verb with a result: dress to a theme and be judged, run a shift together, stage a scene and get rated.
- Or a new shared toy system (weather, trains, a town that changes by vote).
- "A bigger Brookhaven" is not a pitch; the evergreens win on volume.

## Common failure modes

- Classified as a social hangout by accident (title wording, chat-first design) and cut off from under-16 players.
- Bedrooms and bathrooms as the main setting; 18+ only.
- A town with nothing to do alone or without chat.
- Paywalls on the first toys; players never see what is fun.
- Vehicles that fling or lag; the most-used system is the least stable.
- Unfiltered custom text; moderation action against the game.
- Vote rings and trolling in show formats with no counter-design.
- No update rhythm against incumbents that ship weekly.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | Questionnaire result matches the intended audience | Remove hangout wording; make role or activity central; retake |
| 2 | No single-occupancy private spaces if under-18 reach matters | Rework interiors; add bed bounding limits |
| 3 | Fun without chat (emotes, quick-chat, roles, toys) | Add wheels and structured activities |
| 4 | Three free toys within 20 s of spawn | Move spawners and doors to the plaza |
| 5 | A structured activity with a result runs every few minutes | Add rounds, shifts or shows |
| 6 | Vehicles stable at full server population | Explicit ownership, speed caps, idle despawn |
| 7 | All player text is filtered | Audit every text entry point |
| 8 | Frame rate holds on a 3 GB phone in the plaza | Avatar LOD and accessory caps; streaming |
| 9 | Premium items are seen in use and sold from the object | Add contextual prompts; remove pop-ups |
| 10 | Gift passes and low-priced private servers exist | Add both |
| 11 | Weekly update on a fixed day | Commit to a day; keep a prop backlog |
| 12 | Report, mute and owner controls within two taps | Add controls |
| 13 | Votes resist collusion; nothing sells wins | Anonymise, trim outliers; remove paid advantage |
| 14 | Friend join and party features are prominent | Add join-friend and invite prompts after a shared moment |

## Review gate

- [ ] The primary activity is stated and is not chat; the classification and audience are deliberate.
- [ ] Interiors, beds and text surfaces are designed against the maturity rules.
- [ ] Most content is free; premium is cosmetic or convenience and shown in use.
- [ ] Vehicles, houses and avatars meet the population budget on the low-end phone.
- [ ] Griefing answers exist for every social feature; moderation tools are present.
- [ ] Houses, vehicles, props and furniture are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Shared DNA, §Trend lifecycle (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/content-maturity.md (read; social hangout, private spaces, free-form user creation)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/kids-and-select.md (read; chat defaults by account type)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/design-for-roblox.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/contextual-purchases.md (read)
- https://devforum.roblox.com/t/strengthening-our-safety-policies-and-tools/3882864 (search summary; the Aug 2025 announcement described private-space hangouts as ID-verified 17+; the current docs say 18+. Conflict noted: follow the docs and re-check)
- https://devforum.roblox.com/t/new-publishing-requirements-evaluation-process-for-games/4573166 (search summary)
- https://devforum.roblox.com/t/how-to-get-physics-to-chill-out-when-handing-over-network-ownership/2152568 (search summary)
- https://devforum.roblox.com/t/if-cars-network-owner-is-set-to-driver-it-makes-every-moving-object-laggy-on-passengers-screen/4732327 (search summary)
- https://devforum.roblox.com/t/vehiclescars-driven-by-different-players-fling-sometimes-when-colliding/2791026 (search summary)
- GitHub search for open roleplay frameworks (2026-11-10): no maintained, licensed reference of note found.
