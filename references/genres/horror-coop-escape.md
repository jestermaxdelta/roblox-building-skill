# Horror and co-op escape playbook

Covers co-op run-based horror (rooms, floors, nights), liminal "anomaly" horror, asymmetric killer-versus-survivors rounds and co-op chase games. Open it when fear, tension and escape drive the loop, when choosing a maturity target, or when auditing a live horror game for replay value and mobile lighting cost. For hidden-role rounds without horror see `social-deduction.md`. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One short chapter (10–15 min) for 1–4 players; one monster on a patrol with sight only; a minimum light level; checkpoints so death costs under two minutes; a bright, safe lobby | Procedural rooms, director, multiple entities, revives shop, asymmetric PvP |
| Intermediate | Build–spike–release pacing; monster with sight plus hearing at 5 Hz and throttled repathing; client-only flashlight; spectate on death; party teleport to reserved servers; scare-reduction setting | Seeded variation, modifiers |
| Expert | Tension director that reads party state; seeded room generation with pooling; replication limited to what is perceivable; low-end lighting pass; seasonal content plan for late October | — |

Terms: *tension director* = server logic that decides when threats appear based on how the party is doing; *safe room* = a space where nothing can attack; *reserved server* = a private server instance created for one party's run.

## Snapshot

- Market position (vault, 2026-11-07): **strong after Halloween, liminal sub-wave rising**. Dandy's World 128K CCU, DONT SPLASH 81K (launched 16 Oct 2026, peak 97–167K, poolrooms, tense 10-player servers), Evade 64K, Violence District 57K, Forsaken 42K (launched Dec 2024, 138K+ peak, steady roster updates and lore), Sell Fries! [Anomaly] 40K.
- Seasonality: horror runs about 4× normal on 28–31 Oct; Roblox's The Hollow event (22 Oct–2 Nov 2026) peaked at 507.6K and lifted partner games (Dandy's World +711% on its update).
- Volatility: Animal Hospital (Anomaly) won Best New Game and still fell about 90% (564K → 21.5K). "Anomaly × job sim" is now crowded (vault).
- Open gap (vault): fishing or deep-sea horror; nothing above 2K (It Hears The Water 1.5K, Scary Fishing 37).
- Audience: older than the platform average and friend-group driven; durable hits share co-op or skill play, real depth and weekly updates.
- Maturity decides reach `[official]` `[VS]`: mild fear fits a Mild label, moderate fear needs Moderate. Minimal and Mild games are eligible for Roblox Kids (5–8) and Select (9–15); Moderate is eligible for Select and 16+ but not Kids, so a Moderate label costs the 5–8 audience only. Content May Vary is 16+ and Restricted 18+ age-verified: heavy realistic blood lands there. (Corrected 2026-11-11: an earlier vault note said Moderate also removed Select reach; the content-maturity doc says otherwise.)

## Core loop with timings

| Variant | Loop | Timing |
|---|---|---|
| Co-op run (rooms/floors) | Lobby → pre-run shop → explore → tension → chase or scare → escape → next floor | Run 10–20 min so a discovery player can finish one `[house]` |
| Anomaly / liminal | Do a routine task → notice what changed → respond correctly → next shift | Shift 3–8 min `[house]` |
| Asymmetric | Lobby → 1 killer vs survivors → objectives → escape or die → results | Forsaken: 3–4 min round timer (vault) |
| Co-op chase | Round starts → evade → revive team-mates → survive the timer | Rounds of a few minutes |

- Tension graph: long quiet build-ups, short peaks, a safe room after each peak. Jump scares are rare and earned.
- The AI telegraphs and misses; a director controls pacing so two threats never stack on a struggling party.
- Pacing numbers `[lihfolk]`: a spike (scare, reveal, chase) lasts 5–60 s; a release (safe room, light, music change, a reward, a laugh) lasts 30 s–2 min. Fear wears off fast: scares that arrive a few times a minute turn into a joke within minutes. Silence is a tool; cut ambience before a scare.
- A chapter of 15–30 min fits a session `[lihfolk]`; this skill's 10–20 min run target sits at the short end so a first-time player finishes one.
- Death should cost a group at most a minute or two of progress in chapter games; in round games keep rounds short enough that waiting is tolerable `[lihfolk]`.

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; this genre's row is in its §10. No offer or social card in this window (offer gate).

1. 0:00 lobby with a visible "start" spot for parties; solo queue starts inside 30 s.
2. 0:45 inside the first space; one interaction teaches the core verb (hide, close, check).
3. 2:00 first sign of the threat, with no damage possible yet.
4. 3:30 first real encounter, tuned so nearly everyone survives.
5. 5:00 first safe room or end of shift, with a visible count of how far the run goes.
- Lobby time is the bounce risk: get a new player into the first room in under a minute.
- Any intro follows `cutscenes-and-cinematics.md` (length budgets; first-session intros). Horror's version: mood through the first room itself, not a film before it; one project's 27 s intro inside the first minute was removed even with a 3 s skip `[lihfolk]`.

## Progression and economy shape

- Run state and profile state are strictly separate. Within a run: consumables, keys, light. Across runs: currency, cosmetics, unlockable characters or roles, lore pages, badges for depth reached.
- Replay value comes from variation: seeded room order, rotating entities, modifiers, rare rooms, secrets. A fixed linear scare sequence is played once.
- Asymmetric games progress through a roster (character unlocks, vault) and mastery, not stat growth.
- Meta-currency sinks: pre-run consumables, cosmetics, roster. Keep power creep out of co-op difficulty and out of killer-versus-survivor balance.
- Difficulty modes or modifiers give experts a reason to return without gating newcomers.

## Monetisation set that fits

- Keep from the default set: Revive / second chance at 15–30 R$ (vault: DOORS sells revives at 30 R$ and gives new players one free), Starter Pack, currency packs, VIP (cosmetic), gift passes, private servers (friend groups are the audience).
- Pre-play shop model `[official]`: the DOORS lobby sells only its currency; the elevator pre-run shop sells consumables. Sell before or after the run, never during a chase.
- Add: cosmetic flashlights, skins, emotes, death effects, extra lives in party modes.
- Delete: 2× Cash permanents, Auto-Collect, extra storage, Luck (unless loot rolls exist with odds shown).
- **Conflict (market vs house rule 3):** asymmetric leaders sell points packs (vault: Forsaken 40 R$ for 100 points up to 7,600 R$ for 20K) and packs that raise the chance of playing the killer. Role-chance for money is a paid advantage in a competitive mode; do not sell it. Sell cosmetics and earnable-roster shortcuts that carry no stat edge.
- Revive rules: capped per run, fairly priced, offered on the death screen after the chase ends, with a free alternative (team revive, rewarded video).
- Rewarded video `[official]` (survival playbook): Second Chance, pre-round power-up, daily kit; deterministic consumables only, daily cap. Benchmark opt-in 13%+, frequency 2.5+. The playbook's fourth placement, Streak Saver (Evade uses it), is restricted by the house rules: see the Conflict note in `survival-crafting.md` §Monetisation.
- Paid chapters work only when the free content is substantial `[lihfolk]`; discovery-driven games should keep the first full chapter free.

## Retention and social hooks

- Co-op is the retention engine: party teleport, private servers, proximity play. Design for 2–4 friends first.
- Fixed update cadence with new entities, floors or roster characters; lore drops; seasonal modes with real end dates. Plan the year around 28–31 Oct.
- Shareable moments: deaths and near-misses are clips; keep them readable from the spectator camera.
- Badges for depth and secrets; daily modifiers.

## UI patterns

Genre specifics only. Zone layout for this archetype and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre). Effects to build first, from `vfx-recipes.md`: environmental ambience, fire; light and fog in `lighting-and-atmosphere.md`.

- Minimal HUD; diegetic where possible (battery on the flashlight, stamina on the hand). Nothing that explains the threat in advance.
- Spectate on death with a team view and a calm death recap; purchase options appear here, small and dismissible.
- Settings this genre cannot ship without: reduce flashes, reduce camera shake, captions for the audio cues that carry threat information (`accessibility-and-player-qol.md`).
- Mobile: hide and interact on large context buttons; a sprint toggle rather than hold.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §13 NPC and enemy spawning and AI, §15 Interaction, §10 Rounds, match state machine and intermission, §11 Teams, matchmaking, queues and reserved servers, §21 Party and friends features, §3 Shop. Its "Build order by genre" table gives a second opinion.

1. Lobby, party formation and teleport to a reserved run server.
2. Run state machine (floors or chapters, checkpoints, win and fail).
3. Interaction verbs: hide, door, pickup, light.
4. Monster AI: senses, state machine, pathfinding with repath limits.
5. Death, spectate and revive flow.
6. Audio and lighting states (client-driven).
7. Tension director.
8. Player data: currency, cosmetics, badges.
9. Pre-run shop and post-death offers.
10. Seeded room generation or the round and role system for asymmetric modes.

## Technical hot spots

- **Lighting on phones.** The Future lighting technology is expensive and community reports say many Android devices fall back or struggle `[community]`. Author the look so it survives on lower lighting tiers: baked-in contrast in Blender textures, fog and atmosphere for depth, few shadow-casting lights (a community repro for shadow FPS drops uses 16+ shadowed PointLights), one shadowed flashlight per client and unshadowed lights for other players.
- **Flashlight**: create and aim it on the client; a light parented to the character can visibly lag on low-end devices `[community]`.
- **Audio carries the genre**: positional audio budgets, occlusion faked with volume and filters, heartbeat and breath on the client. Never replicate scare triggers as sounds from the server.
- **Entity AI on the server, presentation on the client.** Pathfinding is budgeted (recompute on a timer, not every frame); chases use simple steering between waypoints. Clients interpolate the model and play animation locally.
- **Hidden information**: anything replicated can be read by exploiters (entity position, hiding spots, the anomaly list). Replicate an entity only when it should be perceivable; keep the round's seed and answers on the server.
- **Procedural runs**: rooms are Blender kit pieces snapped by attachments from a server seed; pool and stream rooms; destroy rooms two behind the party.
- **Parties and runs** live in reserved servers reached by teleport; pass party and seed data through teleport data and validate it on arrival.
- **Asymmetric rounds** need server-side hit validation and anti-speed checks on both roles (see `shooter-pvp.md` and `fighting-battlegrounds.md`).
- **Monster tuning** `[lihfolk]`: chase speed slightly below or equal to player sprint (for example monster 15, sprint 18, walk 12 studs/s) and put the stamina limit on the player, so that decisions (hiding, doors) decide an escape and raw speed does not. A monster faster than sprint sounds scary and feels worst.
- **Senses** `[lihfolk]`: sense at about 5 Hz (8 players × 5 Hz is 40 raycasts a second); mix hearing with sight so stealth is rewarded, rather than always targeting the nearest player, which punishes the bravest. Noise is derived on the server from movement state; a client "I made noise" remote lets exploiters stay silent or lure the monster.
- **Pathfinding** `[lihfolk]` `[VS]`: cap repaths at about two a second; never path every frame. Agent defaults are radius 2, height 5, waypoint spacing 4. Call `SetNetworkOwner(nil)` on the monster so no client simulates it (prevents stutter near players and exploitation). A catch cooldown of about 6 s stops chain kills.
- Test at the lowest graphics quality: atmosphere that reads on a PC often collapses to solid black or even grey on phones `[lihfolk]`.

## The one-new-verb angle

- Pair a calm job with dread: the anomaly formula works when the routine is itself a satisfying verb (fishing by day, cutting loose what is on the line at night: the vault's shelved concept).
- A new setting with a clear rule (poolrooms: do not splash) beats a new monster.
- Co-op roles that force talking (one sees, one acts).

## Common failure modes

- Scripted linear scares with no variation; no reason for a second run.
- Jump-scare spam; fear turns into annoyance and the rating drops.
- Solo-only design on a social platform.
- Darkness as the only technique; unreadable on phone screens in daylight.
- Long lobbies and unskippable intros before the first room.
- A Moderate label chosen by accident (blood or intensity that the design did not need).
- Revive or shop prompts during a chase.
- Launching in November after the Halloween window.
- Monster always chases the nearest player; monster faster than sprint; pathfinding every frame; a client-reported noise remote `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | New player is in the first room within 60 s | Shorten the lobby; auto-start solo |
| 2 | A full run fits 10–20 min | Add an early exit with rewards; shorten floors |
| 3 | Two runs differ (seeded rooms, rotating entities, modifiers) | Add a seed and at least three variable systems |
| 4 | Tension graph has quiet stretches and safe rooms | Remove stacked threats; add a director |
| 5 | Works for 2–4 friends with party teleport and private servers | Add party flow and reserved servers |
| 6 | Maturity label matches intent: Mild keeps Kids (5–8), Moderate keeps Select (9–15) and 16+ | Remove needless intensity; retake the questionnaire |
| 7 | Holds frame rate on a 3 GB phone in the darkest, busiest room | Cut shadowed lights; client-only flashlight |
| 8 | Scene reads on a phone at 50% brightness | Raise ambient floor; use fog and silhouette |
| 9 | Entity state is replicated only when perceivable | Move seeds and answers to the server |
| 10 | Offers appear only pre-run and post-death | Move or delete mid-run prompts |
| 11 | First revive is free; revives are capped per run | Add the grant and the cap |
| 12 | No role-chance or stat power is sold | Convert to cosmetics |
| 13 | Flash and shake toggles exist | Add accessibility settings |
| 14 | A seasonal plan exists for 10 Oct–3 Nov | Schedule content and Experience Events |
| 15 | Monster chase speed ≤ player sprint; senses at about 5 Hz; repath ≤ 2/s; server owns the monster | Retune speeds; throttle senses; set network owner to the server |
| 16 | A scare-reduction setting and a way to leave a chapter exist | Add both |

## Review gate

- [ ] The loop has a rule players can state in one sentence and a verb beyond "walk and get scared".
- [ ] Runs vary by seed; run state and profile state are separate.
- [ ] Lighting, audio and AI budgets are met on the low-end phone.
- [ ] The maturity label is deliberate and its audience cost understood.
- [ ] Shops are pre-run or post-death; revives capped; no power or role-chance sold.
- [ ] Rooms, props, entities and lights' fixtures are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives, §Trend lifecycle (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/content-maturity.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/contextual-purchases.md (read; DOORS lobby and pre-run shop)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/survival.md (read)
- https://devforum.roblox.com/t/guide-to-making-better-horror-experiences/2212571 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/very-poor-performance-with-future-lighting-technology/1439704 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/severe-fps-drops-due-to-aggressive-shadow-recalculations-during-object-movementappearance/3875739 (read 2026-11-11)
- https://devforum.roblox.com/t/pointlight-no-longer-always-follows-humanoidrootpart-in-future-lighting/3620431 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://endsights.com/horror-game-design (search summary; host not reachable for a full read)
- https://github.com/ahmicy/simplepath (search listing; 70 stars, MIT; pathfinding wrapper, reference only)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Horror and Story.md`, `43 Genre Systems End to End/Horror Monster Chase AI End to End.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
