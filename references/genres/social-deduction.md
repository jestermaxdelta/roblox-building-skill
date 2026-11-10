# Social deduction and hidden-role rounds playbook

Covers murder-mystery rounds (murderer, sheriff, innocents), impostor-style discussion games and other hidden-role formats. Open it when secret roles and short rounds are the game, when deciding how role information is kept from exploiters, or when auditing a live deduction game for role leaks, teaming and a cosmetic trading economy. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026). For killer-versus-survivors horror see `horror-coop-escape.md`.

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One small looping map; three roles; rounds of 2–4 min; roles sent privately with `FireClient`; a grace period; an end screen that reveals everything | Trading, crates, multiple modes, discussion and voting, ranked |
| Intermediate | Role tools granted so they do not leak; dead and living chat separated; map rotation with voting; AFK removal from the role pool; party-aware role assignment; cosmetic knife and gun skins | Cross-server trading hubs |
| Expert | Duplication-proof tradable inventory with logs and cooldowns; statistical teaming detection; seasonal bundles with real retirement; disclosed role weights; exploit telemetry on role-reading scripts | — |

Terms: *hidden information* = state some clients must not be able to read; *teaming* = players sharing roles out of band to rig rounds; *grace period* = seconds at round start with no eliminations.

## Snapshot

- Market position (vault, 2026-11-07): **evergreen**. Murder Mystery 2 242K CCU (#5 on the platform), one of the 2014–2020 evergreens; it went from 192K to 473K in October 2026 with a 2.24M spike. Evergreens swing 2–5× on events.
- Money (vault): knife trading, where old seasonal items gain value, plus a battle pass and crates.
- Show-tied round games fade with the show: Ink Game fell from 151K tracked (Oct 2025) to 14K (vault).
- Two families `[lihfolk]`: *action deduction* (murder mystery; 2–4 min rounds; killer eliminates everyone or is shot by a gun holder; works without chat) and *discussion deduction* (impostor style; 5–15 min; meetings and votes; needs chat or voice). Most of the audience is on phones and many have limited chat, so action deduction fits better.
- Chat is off by default for Roblox Kids and for self-declared Select accounts `[official]` `[VS]`: a discussion game for under-16s needs non-chat tools (accuse buttons, vote UI, quick phrases).
- Dashboard genre: Survival › 1 vs All `[VS]`. Violence level sets the maturity label; keep eliminations bloodless for Mild.

## Core loop with timings

| Phase `[lihfolk]` | Length | Notes |
|---|---|---|
| Intermission | 10–20 s | Cosmetics, map vote, role-chance display |
| Role reveal | 3–5 s | Private to each player, one-line goal |
| Grace | A few seconds | No eliminations while players spread out |
| Play | 2–4 min (action) or 5–15 min (discussion) | Survive, hunt, deduce |
| Resolution | 5–10 s | Reveal every role, who eliminated whom |
| Rewards | A few seconds | Then back to intermission |

- Role rotation is the reason to stay "one more round": each role plays differently, and the rare role is the jackpot.
- A hero mechanic gives the weakest role agency: when the sheriff falls, the gun drops for an innocent to pick up `[lihfolk]`.
- Revealing everything at the end is how players learn the game.

## First 5 minutes

1. 0:00 join mid-round as a spectator with a clear timer to the next round (under 60 s typical) and a lobby toy to play with.
2. 0:45 first role reveal: innocent by default for a first round `[house]`, with a one-line goal.
3. 1:00 first round: survive, hear the cues, see a body marker.
4. 3:30 end screen explains what happened; first coins.
5. 5:00 second round; the role-chance display shows the odds rising for the roles not yet played.
- The whole loop should be explainable in three lines `[lihfolk]`.

## Progression and economy shape

- Power is flat; every knife and gun behaves the same. Cosmetics must never change hitboxes or reach `[lihfolk]`.
- Progress is cosmetic identity: weapon skins, effects, emotes, levels and a collection with history. Seasonal items retired on schedule gain value honestly.
- Soft currency from rounds: modest for surviving innocents, kill-based for the murderer, with a bonus for the hero shot. Keep the incentive to team small `[lihfolk]`.
- Role weights: a pity-style rising chance for roles not yet played; show the real weight. If a paid boost changes role chance, the displayed chance must match the server weight.
- Trading is the long-term economy and the largest risk; add it only on a duplication-proof inventory.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic), gift passes, private servers (friend groups and creators), Starter Pack as a cosmetic bundle, currency packs, 2× currency or EXP as timed boosts.
- Add: knife and gun skins, elimination effects, emotes, a battle pass with real end dates, seasonal bundles retired on schedule, direct-purchase skins beside any crate.
- Delete: Revive, Auto-Collect, extra storage unless inventories cap, permanent 2× Cash if it buys role power.
- Crates bought with Robux or Robux-bought currency are paid random items: odds shown, `PolicyService` gate, and trading of paid items gated by `IsPaidItemTradingAllowed` `[official]` `[VS]`.
- **Conflict (market vs house rule 3):** paid "murderer chance" exists in the genre, and asymmetric horror leaders sell killer-chance packs (vault). Role chance is an advantage in a competitive round; do not sell it. Do not sell radar, longer throws or faster reloads either `[lihfolk]`.
- No constant "last chance" pressure on bundles; a retirement date is stated once and kept.

## Retention and social hooks

- Short rounds, role rotation and map voting.
- Seasonal events and bundles; the evergreen's October spike shows the size of the lever.
- Friends: private servers and party join; but see anti-teaming below.
- Collection status visible in every round (the weapon in hand is the showcase).

## UI patterns

- Role reveal card with a single goal line; role-chance display in the lobby.
- Readability without chat `[lihfolk]`: body-discovery sound and marker, directional footsteps and throw sounds, a visible gun pickup, accuse and vote buttons with quick phrases in discussion variants.
- End screen: all roles, a kill timeline, the hero moment.
- Spectator camera after elimination that does not reveal the killer before the end (or accept that leak as part of the design, deliberately).
- Maps must stay readable on a phone at low graphics; darkness is not difficulty.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §10 Rounds, match state machine and intermission, §14 Tools and abilities, §17 Trading, §22 Chat commands and admin tools, §2 Inventory and equip. Its "Build order by genre" table gives a second opinion.

1. Round loop: intermission, role assignment, grace, play, resolution, rewards.
2. Role service with private replication.
3. Role tools (knife, gun) with server hit validation; dropped-gun pickup.
4. Spectating and dead-player state.
5. Map rotation and voting.
6. Player data and cosmetic inventory.
7. AFK detection and role-pool removal.
8. Shop and battle pass.
9. Trading with confirmations, cooldowns and logs.

## Technical hot spots

- **Information control is the core system** `[lihfolk]`. Roles must never replicate to clients that should not know them: not in `Team`, not in attributes on characters, not in `leaderstats`, not in values under `Workspace`, not in tool names visible to others. Send each player only their own role with `RemoteEvent:FireClient`.
- **Tools leak roles**: a tool in a `Backpack` or character is replicated. Give the knife and gun only at the moment of use, or give every player an identical-looking placeholder; verify with a second client that nothing distinguishes the murderer before the first attack.
- **Effects leak roles**: role-specific sounds, animations and particles at round start must play only on the role holder's client.
- **Server `Random`** with no client-visible seed for assignment.
- **Dead and living chat** are separate `TextChatService` channels; spectators cannot message the living.
- **Anti-teaming** `[lihfolk]`: spread spawns; where parties are detectable (joined by follow or invite), avoid giving murderer and sheriff to the same party; a sheriff who shoots an innocent loses the gun and is penalised; AFK players leave the role pool.
- **Hit validation**: knife reach, throw speed and gun line of sight are checked on the server; see `fighting-battlegrounds.md` and `shooter-pvp.md`.
- **Trading**: atomic, logged, session-locked transfers; confirmations, value warnings and cooldowns limit scams (`pet-collection-hatching.md`).
- **Round state** lives in one server module; late joiners become spectators with no role data sent.

## The one-new-verb angle

- Change what the hidden role does: sabotage a shared job, infect, swap bodies, hunt with a non-lethal tag.
- Change how innocents win: finish a task set, escape, identify by behaviour rather than by gun.
- Do not tie the concept to a current show; it fades with it (vault).

## Common failure modes

- Roles readable by exploit scripts through teams, attributes or tools.
- Instant eliminations at spawn; no grace period.
- Dead players telling the living who the killer is.
- A discussion game shipped to an audience that mostly cannot chat.
- Friends teaming every round with no counter-design.
- Cosmetics that alter reach or hitboxes.
- Trading added before the inventory is duplication-proof; one dupe collapses values.
- Engagement-bait text and endless "last chance" bundles.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | A second test client cannot determine any role before it is revealed by play | Audit teams, attributes, tools, values, effects |
| 2 | Roles sent only by per-player remote | Remove shared replication |
| 3 | Grace period exists | Add 5–10 s with eliminations disabled |
| 4 | Rounds last 2–4 min; intermission 10–20 s | Retune timers and map size |
| 5 | End screen reveals all roles and the kill timeline | Build the reveal |
| 6 | Dead chat is separate | Add channels |
| 7 | Hero mechanic exists (dropped gun or equivalent) | Add it with a visible pickup |
| 8 | AFK players are removed from the role pool | Add idle checks |
| 9 | Party-aware assignment and spawn spreading | Add both where parties are detectable |
| 10 | Role-chance display equals server weights; role chance is not sold | Fix display; convert the product |
| 11 | Cosmetics never change gameplay | Normalise hitboxes and reach |
| 12 | Crates show odds; trading gated by policy flags and protected from dupes | Add odds, gates and atomic trades |
| 13 | Game works with chat disabled | Add cues, markers and quick phrases |
| 14 | Map rotation of three or more with voting | Add maps and a vote |

## Review gate

- [ ] Family chosen (action or discussion) for the real chat situation of the audience.
- [ ] A written list of every place role data exists, each proven private.
- [ ] Round flow, grace, reveal and hero mechanic are in the design.
- [ ] Anti-teaming and AFK rules are defined.
- [ ] Revenue is cosmetic; role chance and gameplay advantages are not sold; crates and trading meet policy.
- [ ] Maps, weapons and props are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Shared DNA, §Trend lifecycle (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Social Deduction and Murder Mystery.md`, `32 Case Studies of Top Roblox Games/Case Study - Murder Mystery 2.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/kids-and-select.md (read; chat defaults)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/experience-genres.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
