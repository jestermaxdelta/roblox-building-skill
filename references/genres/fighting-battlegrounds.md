# Fighting, battlegrounds and anime gacha playbook

Covers open-arena battlegrounds brawlers, anime ability fighters and the spin-or-reroll ("gacha") ability layer that many of them carry. Open it when melee or ability PvP is the core action, when deciding where hit detection runs, or when auditing a live fighter for ping complaints, exploit load or pay-to-win drift. Market numbers are the vault's 2026-11-07 snapshot `[VS]`.

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

## First 5 minutes

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

- HUD: health, ultimate bar, 4 ability buttons with cooldown sweeps, block and dash, kill feed, streak counter. Nothing else during a fight.
- Mobile: abilities in the right-thumb arc, M1 as the largest button, auto-face or soft lock toward the nearest target, optional auto-block off by default.
- Character select: full-screen only outside combat; one tap to respawn as the same character.
- Settings: screen shake, flash intensity, camera FOV, ping display.

## Technical hot spots

- **Where the hitbox runs is the central trade-off.** DevForum practice is split `[community]`: client-side hitboxes with server plausibility checks feel responsive and are the commonly reported choice for battlegrounds games; server-side hitboxes are safest but feel delayed above about 100 ms ping. One thread's claim that a leading battlegrounds game uses client hitboxes with a ping-based server check is unverified.
- **House default**: the attacker's client detects the hit and sends attacker state, target and timestamp; the server checks cooldown, attack state, range from its own positions with a ping-scaled tolerance, line of sight and per-target debounce, then applies damage and status. The client never sends damage.
- **Ping compensation** `[community]`: offset target position by velocity × ping, or keep a short server position history and rewind; clamp `Player:GetNetworkPing()` to a maximum so a faked high ping buys no reach. Ping is near zero in Studio, so test on live servers.
- **Server authority model** `[official]` `[VS]`: `Workspace.AuthorityMode = Server` with prediction and rollback is documented for combat games; it needs the Input Action System, fixed simulation and streaming, and core logic inside `RunService:BindToSimulation`. Evaluate it for new projects; retrofitting a live fighter is a rewrite.
- **Hit detection shape**: spatial queries (`GetPartBoundsInBox`, shapecasts) per active frame, not `Touched`. The open ShapecastHitbox library is the maintained successor to RaycastHitbox.
- **State machine on the server**: stun, block, i-frames, combo counter and cooldowns are server state replicated as attributes; animations and VFX play on clients from a single small event and are pooled.
- **Exploit surface**: reach and kill-aura (range and rate checks), cooldown skipping (server timers), speed and fling (movement sanity or server authority), animation-cancel packets (validate state transitions), teleport-behind (rewind limit).
- **Ragdoll and knockback**: apply impulses on the owner of the character and confirm on the server; cap velocity to stop fling abuse.
- **Performance**: 20+ players each emitting VFX; cull effects by distance, cap particles, and keep the ultimate cinematic client-side.

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
- https://devforum.roblox.com/t/better-way-to-do-hitbox-validation/3520770 (search summary)
- https://devforum.roblox.com/t/how-do-combat-games-achieve-no-lag/3371389 (search summary)
- https://devforum.roblox.com/t/how-to-get-network-latency-for-server-compensation-logic/3501679 (search summary)
- https://devforum.roblox.com/t/ways-to-fix-server-hitbox-delay/3820669 (search summary)
- https://devforum.roblox.com/t/client-sided-hitbox-or-server-sided-hitbox-for-this-combat/2910826 (search summary)
- https://devforum.roblox.com/t/full-release-ship-fair-and-competitive-games-with-server-authority/4727993 (search summary)
- https://github.com/TeamSwordphin/ShapecastHitbox (read README and licence; 22 stars, MIT)
- https://github.com/Swordphin/raycastHitboxRbxl (search listing; 69 stars, MIT; predecessor)
- https://rowatcher.com/news/the-10-highest-earning-roblox-games-in-2026-and-what-they-mean-for-the-platform (search summary; third-party estimates)
