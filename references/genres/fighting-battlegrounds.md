# Fighting, battlegrounds and anime gacha playbook

Covers open-arena battlegrounds brawlers, anime ability fighters and the spin-or-reroll ("gacha") ability layer that many of them carry. Open it when melee or ability PvP is the core action, when deciding where hit detection runs, or when auditing a live fighter for ping complaints, exploit load or pay-to-win drift. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One character with a 4-hit basic chain, block, dash and two abilities; a server state machine; server-validated hits with a range margin; respawn in 2–5 s with a 2 s shield; a training dummy | More characters, ultimates, ranked, gacha, ragdoll physics, matchmaking |
| Intermediate | Character data modules; combo rules (hitstun decay, combo time cap, breaker); input buffer of 150–200 ms (`references/game-craft.md` §1.2); position history and capped rewind; VFX pooling; touch layout with soft targeting | Awakening modes, bounties |
| Expert | Lag compensation tuned on live servers; custom matchmaking signals; per-character mastery; win-rate and pick-rate telemetry for balance; server authority mode; cheat statistics | — |

Terms: *M1* = the basic attack chain; *hitstun* = time a victim cannot act after being hit; *i-frames* = invulnerability frames; *guard break* = a block being broken by enough hits or a heavy attack; *rewind* (lag compensation) = checking a hit against where the target was when the attacker pressed.

## Snapshot

- Market position (vault, 2026-11-07): **durable upper-middle tier**. Jujutsu Shenanigans 89K CCU, The Strongest Battlegrounds 73K; adjacent anime action Attack on Titan Revolution 50K. Battlegrounds was one of the main clusters on the owner's first feed. Durable games share skill play, real depth and weekly updates (vault lifecycle model).
- Anime remains the strongest licence-free aesthetic for the format; anime incrementals and tower defence are the rising anime wave (vault). Blue Lock Rivals is Roblox's own rewarded-video example for the sports-anime hybrid `[official]`.
- Money (vault pattern): PvP and skill games sell cosmetics, not power. Third-party earnings lists put gacha-driven anime games among top earners and note rising scrutiny of gacha for a young audience `[community]`.
- Audience: older, competitive, clip-driven (combos and ultimates are the marketing). Sessions are open-ended: drop in, fight, leave.
- Rating: violence level sets the maturity label; unrealistic, bloodless hits keep the game at Mild `[official]` `[VS]`.

## Core loop with timings

| Step | What happens | Target `[house]` |
|---|---|---|
| Spawn | Pick a character (free roster) and drop into the arena | In a fight within 30 s of joining |
| Engage | M1 chain, block, dash, 3–4 abilities on cooldowns | M1 startup 0.15–0.25 s; chain of 4–5 hits; dash cooldown 2–4 s |
| Convert | Combo into a finisher; build the ultimate bar | Ultimate available every 60–120 s of fighting |
| Resolve | Kill or die → kill feed, streak counter | Respawn in under 5 s |
| Repeat | Swap character freely; chase a streak or a 1v1 | No lobby between lives |

- Depth comes from interactions, not stat growth: block beats M1, grab beats block, dash beats grab, counter windows, combo extenders, environmental hits.
- Round-based modes (1v1 ranked, 2v2) sit beside the open arena for players who want a result.
- Genre grammar players already know `[lihfolk]`: a 4-hit basic chain whose last hit knocks back or ragdolls, with short end lag; block that reduces damage heavily and breaks after N hits or a heavy attack; four abilities per character on 5–25 s cooldowns (a combo starter, a mobility move, a counter, a finisher); an ultimate charged by dealing and taking damage that transforms the move set for 30–60 s. Deviate deliberately, not by accident.
- Time scales `[lihfolk]`: an exchange lasts 1–5 s, a fight 10–60 s. Open battlegrounds have no rounds; respawn time (2–5 s) is the main pacing knob. Arena modes use best of three or five with 60–99 s round timers.
- Server size `[lihfolk]`: 10–20 players in one arena. Below 8 fights are hard to find; above about 25 third-party chaos ruins duels and physics cost climbs.

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; this genre's row is in its §10. No offer or social card in this window (offer gate).

1. 0:00 spawn with a default character in a low-traffic corner; a training dummy within reach.
2. 0:20 M1 chain lands on the dummy with hit-stop, shake (toggleable) and sound.
3. 1:00 first ability and the block prompt, taught by doing.
4. 2:00 first player fight; new-player spawn protection of a few seconds.
5. 5:00 first kill or assist credited; character select reopened with one more free character highlighted.
- Newcomers farmed on spawn leave inside the bounce window: add spawn protection and, at scale, soft matchmaking of new accounts into gentler servers.

## Progression and economy shape

- Horizontal progression: characters are sidegrades. Unlock by play time, kills or mastery levels; power stays flat.
- Per-character mastery (cosmetic titles, auras, alternate finishers) gives a long tail without touching balance.
- Kill streaks and a server leaderboard are the session goal; ranked ladders with seasons are the long goal.
- Currencies: one soft currency from fights (cosmetics, emotes) and optionally a premium one. No stat shop.
- Gacha layer (anime fighters): styles, clans or traits rolled by spins. In a PvP game random power is the most contested design choice. Under house rule 3: spins that affect combat must be earnable in play only; anything bought with Robux or Robux-bought currency is cosmetic. Any Robux-linked roll is a paid random item with full odds and the `PolicyService` gate `[official]`.
- Balance cadence: patch notes on the fixed update day; rotate a free-trial character weekly.
- Combo rules that prevent infinites, the genre's most common design bug `[lihfolk]`: hitstun decays per hit or total combo time is capped (about 3–4 s); ragdoll ends the combo and getting up grants 0.5–1 s of invulnerability; a combo breaker on a long cooldown or meter cost works during hitstun; one wall bounce and one ground bounce per combo. Write combos as data and test with two clients at real latency.
- Protect newcomers with matchmaking, spawn protection and a bounty on high-streak players (so the server gangs up on the leader, not the newcomer). Do not scale damage down on low-health victims; skilled players feel cheated `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic), gift passes, private servers (a core sale here: friend duels, training, creators), Starter Pack as a cosmetic bundle, currency packs for the cosmetic currency.
- Add: skins, auras, kill effects, emotes, finishers, name tags, a season pass with a real fixed end date, emote wheel slots.
- Delete: 2× Cash permanents and stat boosts, Luck / Server Luck on combat rolls, Auto-Collect, extra storage, Revive.
- **Conflict (market vs house rule 3):** early-access character passes and paid spins for combat abilities are common in the genre `[community]`. A paid character is acceptable only as a balanced sidegrade that becomes free on a stated date; paid rolls for combat power are not acceptable here.
- 2× progress boosts are fine when they speed mastery or cosmetic currency and never change combat numbers.
- Rewarded video `[official]` (shooter and sports playbooks): pre-match boost to XP or currency, never damage, health or aim; post-match payout boost; a one-match cosmetic or character trial. Boosts last one match or session. Never interrupt a fight. Shooter benchmark opt-in 10%+, frequency 3+.

## Retention and social hooks

- New character or rework on a fixed cadence is the update that brings players back; show the next one as a silhouette.
- Private servers and 1v1 challenge prompts create intentional co-play.
- Ranked seasons with cosmetic rewards; no rank decay that punishes absence beyond a soft reset.
- Clip moments: ultimates with a short cinematic that other players can still interrupt or see.

## UI patterns

Genre specifics only. Zone layout for this archetype and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre). Effects to build first, from `vfx-recipes.md`: hit spark, melee slash, heavy impact, dash, shield, aura.

- HUD: health, ultimate bar, 4 ability buttons with cooldown sweeps, block and dash, kill feed, streak counter. Nothing else during a fight.
- Mobile: abilities in the right-thumb arc, M1 as the largest button, auto-face or soft lock toward the nearest target, optional auto-block off by default.
- Character select: full-screen only outside combat; one tap to respawn as the same character.
- Settings: screen shake, flash intensity, camera FOV, ping display.
- A fighter with four abilities, an ultimate, block, dash and attack is eight touch buttons: make them large, rest the basic attack under the right thumb, and soft-target abilities toward the nearest enemy in front `[lihfolk]`.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §12 Combat, §14 Tools and abilities, §10 Rounds, match state machine and intermission, §11 Teams, matchmaking, queues and reserved servers, §2 Inventory and equip. Its "Build order by genre" table gives a second opinion.

1. Fighter state machine on the server (idle, attacking, blocking, stunned, ragdolled, dashing).
2. Input layer with buffering for keyboard, touch and gamepad.
3. Hitbox service (spatial queries per active frame) and server hit validation.
4. Damage, stun and status module.
5. Character and move-set registry as data.
6. Respawn, spawn protection and multiple spawn points.
7. Training area with dummy and combo counter.
8. Ultimate meter.
9. Position history and lag compensation.
10. Cosmetics, mastery, streaks and bounties; then ranked rounds.

## Technical hot spots

- **Where the hitbox runs is the central trade-off.** DevForum practice is split `[community]`: client-side hitboxes with server plausibility checks feel responsive and are the commonly reported choice for battlegrounds games; server-side hitboxes are safest but feel delayed above about 100 ms ping. One thread's claim that a leading battlegrounds game uses client hitboxes with a ping-based server check is unverified.
- **House default**: the attacker's client detects the hit and sends attacker state, target and timestamp; the server checks cooldown, attack state, range from its own positions with a ping-scaled tolerance, line of sight and per-target debounce, then applies damage and status. The client never sends damage.
- **Ping compensation** `[community]`: offset target position by velocity × ping, or keep a short server position history and rewind; clamp `Player:GetNetworkPing()` to a maximum so a faked high ping buys no reach. Ping is near zero in Studio, so test on live servers.
- **Server authority model** `[official]` `[VS]`: `Workspace.AuthorityMode = Server` with prediction and rollback is documented for combat games; fully released for all games on 9 July 2026; it needs next-generation replication, the Input Action System, deferred signals, fixed simulation and streaming, and core logic inside `RunService:BindToSimulation`. Evaluate it for new projects; retrofitting a live fighter is a rewrite.
- **Hit detection shape**: spatial queries (`GetPartBoundsInBox`, shapecasts) per active frame, not `Touched`. The open ShapecastHitbox library is the stated successor to RaycastHitbox (last pushed 2025-08).
- **State machine on the server**: stun, block, i-frames, combo counter and cooldowns are server state replicated as attributes; animations and VFX play on clients from a single small event and are pooled.
- **Exploit surface**: reach and kill-aura (range and rate checks), cooldown skipping (server timers), speed and fling (movement sanity or server authority), animation-cancel packets (validate state transitions), teleport-behind (rewind limit).
- **Ragdoll and knockback**: apply impulses on the owner of the character and confirm on the server; cap velocity to stop fling abuse.
- **Performance**: 20+ players each emitting VFX; cull effects by distance, cap particles, and keep the ultimate cinematic client-side.
- **Lag compensation numbers** `[lihfolk]`: for every player, buffer 1 s of root positions at a 20–30 Hz sample rate; rewind by the attacker's ping with a cap (about 250 ms). Past the cap give no extra compensation: rewinding further hits defenders long after they dodged, which feels worse than an occasional whiff. Show the attack on the attacker's client in under 100 ms.
- **Server validation list** `[lihfolk]`: attacker alive and not stunned; move off cooldown by the server clock; target within range plus a latency margin; no more targets hit than the move allows; state transition legal.
- **Input buffer** of 0.15–0.20 s, never above 0.30 s, makes combos feel responsive (`references/game-craft.md` §1.2 owns the windows).
- **Ragdoll cost** `[lihfolk]`: ten simultaneous ragdolls in a 20-player server is normal; keep them 1–2 s, simplify constraints and end them early on low-end devices.
- **Matchmaking** `[lihfolk]` `[VS]`: Roblox lets creators weight matchmaking signals and add custom signals from their own data; use it to group similar skill. Verify the current configuration options in the docs.

## The one-new-verb angle

- One system-level verb: destructible arena, tag-team swaps, a shared physics object, terrain that players reshape.
- Or a new source of characters with the same clarity as anime archetypes, built in Blender with distinct silhouettes.
- Hybrid lead from the vault: physics sports are rising (Practical Basketball +523% on an update); combat verbs on a ball or goal change the win condition.

## Common failure modes

- Server-only hitboxes with no compensation: "I hit him" complaints, then churn.
- Client-trusted damage: kill-aura within a week of traction.
- Paid power (characters stronger at launch, paid combat spins): pay-to-win reviews and a broken house rule.
- Spawn-killing of newcomers; no protection, no gentle servers.
- Infinite combos or stun-locks with no escape option.
- VFX overload that hides the fight and tanks phones.
- A roster too large to keep balanced, with no patch cadence.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | New player is fighting (dummy or player) within 30 s | Move character select behind a default; add a dummy at spawn |
| 2 | Spawn protection exists | Add 3–5 s of invulnerability that ends on first attack |
| 3 | Hits register for a 150 ms player without feeling late | Move detection to the attacker's client with server checks |
| 4 | Server validates range, rate, state and line of sight | Add the validation layer; remove damage from payloads |
| 5 | Ping used for tolerance is clamped | Clamp and log outliers |
| 6 | Every combo has an escape (burst, tech, scaling) | Add damage scaling and a breaker on cooldown |
| 7 | No Robux purchase changes combat numbers | Convert to cosmetics; make paid characters sidegrades with a free date |
| 8 | Any paid roll shows odds and respects policy flags | Add odds panel and gate, or make rolls earn-only |
| 9 | Private servers and 1v1 challenges work | Add both |
| 10 | Frame rate holds on a 3 GB phone in a 10-player brawl | Cull and pool VFX; cap particles |
| 11 | Shake and flash toggles exist | Add settings |
| 12 | Patch notes ship on a fixed day with a character cadence | Commit to a schedule |
| 13 | Ranked or streak goals exist beyond free-for-all | Add a ladder with cosmetic rewards |
| 14 | Combo time is capped or hitstun decays; get-up invulnerability exists | Add both rules; retest every combo |
| 15 | Position history at 20–30 Hz with rewind capped near 250 ms | Add the buffer and the cap |
| 16 | Server size is 10–20 for open arenas | Resize servers |

## Review gate

- [ ] The interaction triangle (attack, block, grab or equivalent) is written down and every option has a counter.
- [ ] Hit detection location, validation rules and ping policy are decided and tested on live servers.
- [ ] Combat state lives on the server; clients own only presentation and their own input.
- [ ] Nothing sold changes combat outcomes; paid randomness is cosmetic and disclosed.
- [ ] Newcomer protection and private servers exist.
- [ ] Characters, weapons and arena pieces are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md and `techniques.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/shooter.md and `sports.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://devforum.roblox.com/t/better-way-to-do-hitbox-validation/3520770 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/how-do-combat-games-achieve-no-lag/3371389 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/how-to-get-network-latency-for-server-compensation-logic/3501679 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/ways-to-fix-server-hitbox-delay/3820669 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/client-sided-hitbox-or-server-sided-hitbox-for-this-combat/2910826 (opened 2026-11-11: thread and topic confirmed, details not re-read)
- https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 (read 2026-11-11; staff announcement, 9 Jul 2026)
- https://github.com/TeamSwordphin/ShapecastHitbox (read README and licence; 22 stars, MIT)
- https://github.com/Swordphin/raycastHitboxRbxl (search listing; 69 stars, MIT; predecessor)
- https://rowatcher.com/news/the-10-highest-earning-roblox-games-in-2026-and-what-they-mean-for-the-platform (search summary; third-party estimates)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Battlegrounds and Arena Fighters.md`, `43 Genre Systems End to End/Arena Rounds with Teams and Spectating End to End.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
