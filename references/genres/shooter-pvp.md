# Shooter and PvP duels playbook

Covers first- and third-person shooters, round-based duels (1v1 to 5v5), arena and team modes. Open it when aiming and shooting is the core action, when choosing a netcode model for hit registration, or when auditing a live shooter for cheating, time-to-kill balance and cosmetic revenue. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | Start from the official FPS System or Laser Tag template; two weapons as data rows; one small map; team deathmatch; client raycast with server checks on rate, ammo, range and line of sight; spawn with a default loadout | Ranked, attachments, battle pass, killcams, projectile weapons, more than three maps |
| Intermediate | A weapon sheet with TTK per range band; learnable recoil; hit markers and damage direction; position history with capped rewind; aim assist and touch layout; bots for empty queues | Custom matchmaking, statistics-based cheat review |
| Expert | Server authority mode or a custom predicted controller; statistical aimbot detection with review; skill-based matchmaking; mixed-input fairness (touch versus mouse); seasonal ranked | — |

Terms: *TTK* = time to kill; *STK* = shots to kill; *hitscan* = an instant ray rather than a travelling projectile; *ADS* = aiming down sights; *breakpoint* = a damage value at which STK changes.

## Snapshot

- Market position (vault, 2026-11-07): **one durable leader, thin middle**. RIVALS 217K CCU (#7 on the platform): 1v1–5v5 duels, first to 5 rounds, ranked and contracts, money from cosmetics and keys. Duels were a main cluster on the owner's first feed (MVSD 10K). The vault lists RIVALS among durable games: skill play, real depth, weekly updates.
- Roblox's own genre table calls action "less popular on Roblox than elsewhere" (example: Arsenal) `[official]`; the audience exists but concentrates in a few polished games.
- One tracker reports D1 22–30% for shooters with traffic `[community]`.
- Audience: older, competitive, PC-heavy but increasingly mobile and console; sessions are chains of short matches.
- Platform shift `[official]` `[VS]`: Roblox now ships a server authority model (`Workspace.AuthorityMode`), documented for "FPS, racing, sports, and combat", with client prediction and rollback. A 2026 DevForum announcement is titled "Full Release" while its summary still calls the feature an opt-in beta available to all experiences; check the current release status before committing.
- Official starting points `[official]`: the Laser Tag template (blaster system with damage, ammo capacity, recoil and spread attributes; a round system; an arena), the FPS System template, and the Weapons Kit (projectile-based, over-the-shoulder; Limited Use License).

## Core loop with timings

| Step | What happens | Target |
|---|---|---|
| Queue | Pick mode and loadout | Match found in under 30 s; show something to do while waiting |
| Round | Engage → shoot → reposition → win or lose the round | Round 30–90 s in duels `[house]` |
| Between rounds | Swap weapon, see the score | Under 10 s `[house]` |
| Match | First to N rounds (RIVALS: first to 5) | Match 3–8 min `[house]` |
| Results | XP, currency, contract progress, rematch | Rematch one tap |

- Gunplay knobs (house defaults): hitscan or projectile per weapon; damage falloff (full to 20 m, floor 0.4× by 60 m); headshots 1.5–2×; recoil as a decaying offset; spread with a square-root distribution; `TTK = (ceil(hp / damage) - 1) / fire_rate`.
- Decisions happen in the breaks (death screen, lobby, results), so that is where UI and offers live.
- Time scales `[lihfolk]`: an engagement lasts 1–5 s, a life 20 s–2 min, an objective match 8–12 min with a 15–30 s scoreboard and map vote between matches. Keep players in the same server between matches and rebalance teams.
- Time to first shot under 30 s from joining: spawn first with a default loadout and customise between lives `[lihfolk]`.
- TTK sets identity `[lihfolk]`: fast (0.2–0.4 s for a rifle up close) rewards first-shot aim and positioning; slow (0.8–1.5 s) rewards tracking and makes fights reversible, which is kinder to touch and controller players.

## First 5 minutes

1. 0:00 into a bot or low-stakes warm-up within 20 s of joining; default loadout, no menus.
2. 0:30 first elimination against a bot or dummy; hit markers and sound confirm.
3. 1:30 first real duel against a similarly new player.
4. 3:30 first match result with XP and one unlock.
5. 5:00 loadout screen introduced with the new unlock highlighted; ranked stays locked until a few matches are played.
- New players must not meet veterans in match 1. Bots or new-account pools protect the bounce window.

## Progression and economy shape

- Power is flat. Weapons are sidegrades with distinct roles; unlocks widen choice.
- Account level and per-weapon mastery unlock cosmetics; contracts (daily and weekly tasks) pay currency or keys.
- Ranked ladder with seasons; cosmetic rewards by rank; soft reset between seasons.
- Currencies: soft (matches, contracts) for weapons and basic skins; premium for cosmetic cases or direct skins. Skin cases bought with Robux or Robux-bought keys are paid random items: full odds, `PolicyService` gate, trading gated by `IsPaidItemTradingAllowed` `[official]`.
- Sinks: skins, charms, kill effects, emotes, finishers, season pass tiers.
- Balance by TTK bands per range; publish patch notes on the fixed update day.
- Weapon balance sheet `[lihfolk]`: one row per weapon (damage by zone, fire rate, magazine, reload, falloff start and end, minimum damage, hip and aimed spread, recoil class, move speed, ADS time). Compute STK and TTK per range band and plot them. Each class owns a band (SMG close, rifle mid, sniper long); a weapon that is best in every band is broken; flag anything 20–30% better than its class median.
- Breakpoints `[lihfolk]`: 34 damage against 100 HP kills in 3 shots, 33 damage in 4, a one-third TTK change from one point of damage. The first shot lands at time zero: 4 STK at 10 shots a second is 0.3 s, not 0.4 s. Real TTK divides by accuracy; add ADS time for scoped weapons.
- Recoil should be learnable (fixed or semi-fixed patterns reward practice; pure random feels unfair). Spread is small when aimed and grows with movement and sustained fire; derive it from a seed the server can reproduce `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic), gift passes, private servers (scrims, friends, creators), Starter Pack as a cosmetic bundle, currency packs for the cosmetic currency, 2× EXP as a timed boost.
- Add: skins, cosmetic packs, characters, a battle pass with real fixed end dates, direct-purchase skin bundles beside any case.
- Delete: 2× Cash permanents that buy weapons faster than play allows, Luck on anything that affects combat, Auto-Collect, extra storage, Revive.
- House rule 3: no purchasable stat advantage in competitive modes. No paid weapons with better numbers, no paid attachments, no paid armour.
- Rewarded video `[official]`: Pre-Match Boost (2× XP, credits or keys for the next match; never damage, health or aim), Armoury Currency Reward (a small free-currency option beside paid bundles), Weapon Trial for one match (Rivals), Post-Match Payout Boost. Never interrupt a fight. Benchmark opt-in 10%+, frequency 3+.
- Offers only in lobby, loadout and results screens.

## Retention and social hooks

- Ranked seasons, contracts, weekly weapon or map on a fixed day.
- Party queue, private servers, 1v1 challenge links: intentional co-play.
- Killcams and end-of-match highlights are the shareable clip.
- No punishment for losing beyond rank points; no loss of items.

## UI patterns

- HUD: crosshair, ammo, health, round score, minimal kill feed. Hit markers and damage direction indicators are mandatory feedback.
- Settings: FOV, per-scope sensitivity, aim assist options, crosshair editor, controller dead zones, colour-blind enemy outline.
- Mobile: fire on the right thumb with optional auto-fire on target, large jump and crouch, gyro aim if offered; controller: aim assist with slowdown, not snap.
- Loadout and shop never open during a live round.
- Third person `[lihfolk]`: raycast from the camera to find the aim point, then fire from the muzzle to that point, so players hit what the crosshair shows; offer a shoulder swap.
- Readable art over realism: clean silhouettes, team-coloured outlines, low visual noise behind enemies. Sightline length matches the weapon roster (no 400-stud lanes without long-range weapons) `[lihfolk]`.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §12 Combat, §10 Rounds, match state machine and intermission, §11 Teams, matchmaking, queues and reserved servers, §14 Tools and abilities, §9 Leaderboards. Its "Build order by genre" table gives a second opinion.

1. Weapon data table and weapon controller (fire, reload, recoil, spread).
2. Server hit validation (rate, ammo, origin, range, line of sight).
3. Health, damage, death and respawn with a default loadout.
4. Teams, round and match flow, scoreboard, map vote.
5. Feedback: hit markers, damage direction, kill feed.
6. Position history and lag compensation.
7. Loadouts and unlocks; player data.
8. Bots and join-in-progress.
9. Cosmetics, contracts, battle pass.
10. Ranked rating, matchmaking and cheat statistics.

## Technical hot spots

- **Hit registration model** is the first decision.
  - *Client-detected, server-validated* (the community's common choice `[community]`): the client raycasts immediately for feel and sends origin, direction, target and timestamp. The server checks fire rate, ammo, muzzle origin against its own character position, range, line of sight with its own raycast, and plausibility against recent target positions. The client never reports damage.
  - *Server authority model* `[official]` `[VS]`: movement and shots simulated on the server with client prediction and rollback; requires the Input Action System, fixed simulation, next-generation replication and streaming; core logic in `RunService:BindToSimulation`. Removes fly, speed and teleport cheats by construction. A developer reports fast predicted projectiles jittering under rollback `[community]`; test projectile weapons early.
- **Lag compensation**: keep a short ring buffer of player positions on the server and rewind to the shot time within a cap; community threads note tick-rate limits make exact rewind hard on Roblox `[community]`. Clamp reported ping; cap rewind (house default 300–500 ms).
- **What validation cannot stop**: aimbots and ESP use legitimate data. Mitigate with server-side statistics (headshot rate, snap angles, reaction times), replication limits where possible, and report review.
- **Open references**: Chickynoid (server-authoritative character controller with rollback and lag-compensated hit detection; MIT; invasive, replaces Humanoid movement; last pushed 2024) and SecureCast (server-authoritative projectiles; MIT; archived) show the architecture; neither is a drop-in.
- **Performance**: tracers and impacts are pooled meshes or `Beam`s; viewmodels render only for the local player; third-person weapon models are low-poly Blender LODs; raycast validation can run in Parallel Luau.
- **Maps**: every visible mesh is solid, so cover is honest: what looks like cover blocks rays, and collision meshes match the Blender visual closely enough that shots do not hit invisible edges.
- **Matchmaking**: lobby place plus reserved match servers; skill buckets stored in a memory store; backfill rules for leavers.
- **Cadence checks** `[lihfolk]`: shots per second never exceed the weapon's fire rate plus a small tolerance; ammo and reload time are tracked on the server.
- **Headshots** need their own tighter check (rewind the head position, or accept the body hit and decide the multiplier strictly); generous headshot tolerance is the easiest thing for silent-aim to exploit `[lihfolk]`.
- **Statistics** `[lihfolk]`: headshot ratio, time from target visible to first hit, angular snap speed. Flag outliers for review; never auto-ban on one stat.
- **Killcams** need recorded positions of every player for the last few seconds; budget memory before promising them `[lihfolk]`.
- Touch against mouse is the genre's hardest fairness problem: aim slow-down near targets, optional auto-fire when the crosshair rests on an enemy, and input-based matchmaking where population allows `[lihfolk]`.

## The one-new-verb angle

- One movement or weapon verb that changes duels: a grapple, a deployable wall, a time-limited swap of positions.
- Or a mode frame: asymmetric objectives, a physics ball (physics sports are rising in the vault), co-op PvE waves with the same gunplay.
- Do not enter with "a generic FPS"; the genre's middle tier is thin because polish costs are high.

## Common failure modes

- Trusting client hit or damage reports; cheaters within days.
- Server-only raycasts with no compensation; shots feel wrong above 80–100 ms.
- New players matched against veterans; first-match bounce.
- Paid weapons or attachments with better stats.
- TTK so short that mobile and controller players cannot react, or so long that fights are indecisive.
- No aim assist or sensitivity options; mobile and console churn.
- Maps with invisible collision snag points.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | New player gets an elimination inside the first minute | Add a bot warm-up and new-account pools |
| 2 | Queue to match under 30 s at normal population | Add bots, merge queues, show a warm-up range |
| 3 | Server validates rate, ammo, origin, range, line of sight | Build the validation layer; remove damage from payloads |
| 4 | Shots feel right at 120 ms | Client-side detection with rewind tolerance, or adopt server authority |
| 5 | Rewind and ping are capped | Add caps and logging |
| 6 | Statistical cheat flags and a review queue exist | Log headshot rate, snap angles; build review tools |
| 7 | TTK table per weapon and range is documented | Compute from the formula; rebalance outliers |
| 8 | Nothing sold changes combat numbers | Convert to cosmetics; refund-equivalent grants |
| 9 | Any case or key shows odds and respects policy flags | Add odds panel, gate and a direct-purchase option |
| 10 | Mobile and controller have aim assist and full settings | Add assist and settings |
| 11 | Offers appear only in lobby and results | Remove in-round prompts |
| 12 | Ranked, contracts and a weekly drop exist | Add progression loops |
| 13 | Frame rate holds on a 3 GB phone in a full firefight | Pool effects; LOD weapons; cull distant VFX |
| 14 | TTK plotted per weapon per range band; each class owns a band | Build the sheet; fix weapons that win everywhere |
| 15 | First shot within 30 s of joining | Default loadout; customise between lives |

## Review gate

- [ ] Hit registration model chosen and tested on live servers at high ping.
- [ ] All combat state is server-side; payloads carry intent only.
- [ ] TTK, falloff and recoil are specified per weapon.
- [ ] Newcomer protection, queue time and input options are covered on all platforms.
- [ ] Revenue is cosmetic; paid randomness is disclosed and gated.
- [ ] Weapons, maps and characters are Blender models; collision matches visuals.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md and `techniques.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/templates.md (read; Laser Tag and FPS System templates)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/weapons-kit.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/shooter.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/game-design/design-for-roblox.md (read; genre table)
- https://about.roblox.com/newsroom/2026/07/creating-responsive-cheat-resistant-games-roblox-server-authority (search summary)
- https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 (search summary)
- https://devforum.roblox.com/t/server-authority-instance-stitching-for-fast-projectile-has-werid-rollbacks/4738369 (search summary)
- https://devforum.roblox.com/t/server-side-hit-detection/1295976 (search summary)
- https://devforum.roblox.com/t/server-sided-hit-detection-with-lag-compensation/3322386 (search summary)
- https://github.com/easy-games/chickynoid (read README; 266 stars, MIT, last pushed 2024-05)
- https://github.com/1Axen/Secure-Cast (read README; 30 stars, MIT, archived)
- https://github.com/weenachuangkud/FastCast2 (search listing; 30 stars, licence unclear; not used)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Shooters FPS and TPS.md`, `10 Game Design and Genres/Time-to-Kill Math and a Weapon Balance Sheet.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
