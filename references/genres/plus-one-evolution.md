# +1 per second and Evolution playbook

Covers "+1 ___ Every Second", "+1 ___ Evolution" and stat-lane games: a stat grows while you train, a lane of stage gates tests it, Wins buy eggs and better training, and rebirth multiplies everything. Open it for the owner's snowball project, any stat-lane concept, or a live +1 game stuck in the under-2K tail. Format norms are the vault's 2026-11-07 snapshot, taken mostly from fan guides, so treat exact values as approximate `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One training pad, one lane with 8 gates at about ×4, Wins, one egg with 4–5 pets, a server-side 1 Hz stat tick, teleport buttons, save stat-independent progress (Wins, pets) | Rebirth, multiple Worlds, Robux pads, quests, friend boosts, seasonal skins |
| Intermediate | Rebirth with caps; 3 Worlds; pad tiers; free-rewards timer; stat shown on the body with clamped scale; server-validated gates; mantissa/exponent numbers | Cash-out-or-push tension, idle pad |
| Expert | A twist where the stat changes how the run plays; weekly World runway with Experience Events; 30+ product ladder scaled by World; telemetry per gate; rating held above 85% before ads | — |

Terms: *Wins* = the soft currency paid by lane gates; *World* = a themed lane with its own gates and egg; *rebirth* = reset the stat for a permanent multiplier.

## Snapshot

- Market position (vault, 2026-11-07): **healthy middle tier**. +1 Venom Evolution 46K CCU, +1 Spider Arm 30K, Bug Evolution 29K, +1 Anime Eyes 17K, +1 Power Fruit Evolution 14K, +1 Gun Forge 8.1K; most of the first 40 "evolution" results are under 1K.
- +1 obbies are **cooling**: +1 Speed Keyboard Escape 33K from a 4.04M peak, down 61% from August to September 2026, with dozens of "+1 ___ Escape" clones.
- "+1 ___ For Eggs" without a journey fails: +1 Strength 1.5K, +1 Wings 606, +1 Muscle 339, +1 Speed 27 (vault).
- The owner's gap: snowball Size plus eggs on a Stage lane; nearest rival is an ad-driven game at a 66% rating with almost no players.
- Audience: young, idle-tolerant, phone-first. Sessions: Venom 14.0 min, Gun Forge 33.8 min (longest found); aim for 19+. Larger shared lobbies suit the format (players watch each other's stat).
- Lifecycle: format hits peak at 0.5–4M and lose 90%+ within 1–4 months; a clone after the parent's peak settles at 4–32K (vault). Ship into a seasonal window.
- LihFolk's teardown of the +1 obby leader `[lihfolk]`: its twist is that more speed makes the course harder to control, so progress raises power and difficulty together and the game stays a skill test. It read the hook as the shortest on the platform (you get stronger even while failing) with a concrete, sensory theme (a keyboard you can hear).

## Core loop with timings

| Step | What happens | Format norm (vault) |
|---|---|---|
| Train | Stand on a pad or pile; the stat rises +X per second × pets × boosts | The stat only grows on a training spot (owner's decision) |
| Run | Enter the lane; pass every gate your stat beats | Gates ×4 apart: 40, 375, 1.5K, 6.2K, 26.2K, 62.5K, 200K |
| Earn | Each gate pays Wins; deeper gates pay more | Wins are the soft currency |
| Spend | Eggs (pets multiply training), better pads, World teleports | Eggs ×40–250 apart, starting at 100 Wins |
| Advance | Clear the World's last gate → next World | 8–10 gates per World; 3 Worlds at launch, add one a week toward 12 |
| Rebirth | Stat resets; pets, Robux pads and passes stay | ×2 / ×3 / ×4 with level caps 22 / 34 / 48 |

- Pace `[house]`: first gate inside 30 s, first egg inside 2–3 min, World 2 inside session 1, first rebirth at 20–40 min.
- A train-run cycle should take 1–3 min early so there is always a reason to leave the pad; long silent idling is where sessions die.

## First 5 minutes

1. 0:00 spawn beside the free +1 pad; the stat counter is the largest thing on screen and on the character.
2. 0:20 enough for gate 1: an arrow points down the lane; the gate breaks with a hit-stop and a Wins pop.
3. 1:00 back to the pad (teleport button); 2:00 gate 3 and the first egg.
4. 3:00 first pet equipped; the per-second rate visibly changes.
5. 5:00 the first Wins pad tier bought; World 2 gate visible with its requirement.
- The first minute must deliver what the thumbnail shows (the climb), since tiles rank by qualified plays.

## Progression and economy shape

- Two currencies only: the stat (resets) and Wins (persist within a rebirth, or always; decide early). Adding Cash is an open question in the owner's design; the vault recommends Wins only.
- Gates: about ×4 per stage; the last gate of a World is the wall that sells the next egg or pad.
- Pads: free +1 → Wins tiers → rebirth-gated 2× / 3× pads → one idle pad (vault: Gold Treadmill 69 R$).
- Pets: 4–5 per egg, top pet 0.1%, additive +0.1 to +5, 3–4 slots. Details in `pet-collection-hatching.md`.
- Rebirth: ×2 / ×3 / ×4 steps with a rising cap; requirement is either a stat threshold or clearing the final gate (open question). Keep the wait ratio ×1.2–1.5.
- Optional tension without bosses: cash out or push on at each gate, where a failed push forfeits unbanked Wins (+1 Superhero Evolution). Under the house rules make the stake only the current run's unbanked Wins, never saved progress.
- Boosts: group +10%, friend +20% (vault). Bonuses only, never gates.

## Monetisation set that fits

- Format ladder (vault): one-time training pads ×8 / ×15 / ×30 / ×99 at 79 / 199 / 499 / 1,299 R$; 2× Wins 90–99 R$; stat packs +25K / +100K / +500K / +1M at 10 / 41 / 86 / 167 R$; idle pad about 69 R$; one 79 R$ egg per World; 30+ cheap repeatable products (Venom 36, Gun Forge 123).
- Keep from the default set: Starter Pack, 2× boosts (as 2× Stat and 2× Wins), Luck and Server Luck (eggs exist: odds shown, `PolicyService` gate), Auto-Hatch, extra pet slots, VIP, gift passes, private servers.
- Delete: 2× EXP, Revive, Auto-Collect (nothing to collect), currency packs in Cash unless Cash exists (sell stat packs instead).
- Fixed stat packs lose value as numbers grow: scale pack size with the player's World or price packs as "N minutes of training" `[house]`.
- House rule 3: the ×99 pad is strong pay-for-speed. Acceptable only while the lane is non-competitive. If the game adds PvP (power-level fighting variants exist), paid multipliers must not apply inside it.
- Rewarded video: use the incremental playbook `[official]` (velocity boost, auto-train preview); benchmark opt-in 13%+, frequency 2.8.

## Retention and social hooks

- Free-rewards timer, quests and a new World weekly on a fixed day (vault norms); reward steps at about 5 / 15 / 30 min of play `[house]`.
- Offline training on the idle pad with a stated cap.
- Friend boost +20% and visible stat on the character: players are each other's goal board.
- Seasonal skin of the lane and a title tag refreshed every update (`[🎄 UPD]`), removed when the season ends.

## UI patterns

- One giant stat counter in the game's own unit (SIZE, °F, POWER) with a per-second line under it; Wins top right.
- Lane gates show their requirement in the world at readable size; a progress bar to the next gate on the HUD.
- Bottom-row buttons seen across the format: Pets, Shop, Rebirth, Worlds, Free Rewards, Quests. Keep five or fewer visible on a phone; the rest behind one menu.
- Teleport-to-pad and teleport-to-lane buttons remove dead walking.

## Systems to build, in order

System names refer to `references/gameplay-systems-cookbook.md`.

1. Stat tick service (pad occupancy, multipliers, 1 Hz) and counter HUD.
2. Lane gates with server validation and Wins payout.
3. Player data: Wins, pets, pads, Worlds, rebirths.
4. Teleports (pad, lane, Worlds).
5. Eggs and pets (see `pet-collection-hatching.md`).
6. Pad tiers and shop.
7. Rebirth.
8. Worlds and their gates.
9. Free-rewards timer, quests, boosts (group, friend).
10. Product ladder; offline or idle pad; weekly World pipeline.

## Technical hot spots

- **Stat tick**: accumulate on the server at 1 Hz from pad occupancy; replicate the value at 1–2 Hz (attribute or a single state remote) and let the client interpolate the counter. Never fire a remote per +1.
- **Pad occupancy** is server-checked by position, not by a client "I am on the pad" message; several players share a pad without collision fights (use collision groups for players on pads).
- **Gates**: server validates stat ≥ requirement and that the player is at the gate (teleport exploits pay Wins otherwise); gate break VFX is client-only.
- **Body-as-stat** (size, arm, eyes): scale a Blender prop or accessory, not the Humanoid, and clamp its visual scale logarithmically so a 1e9 stat does not fill the server or break the camera; keep the collision proxy bounded.
- **+1 Speed or Jump variants**: `WalkSpeed`/`JumpPower` are set by the server but movement is client-owned; add server speed sanity checks or adopt the server authority model `[official]` `[VS]`.
- **Numbers**: stat reaches 1e15 fast; store mantissa/exponent; format with suffixes.
- **AFK**: idling is the format, so do not kick idlers; do exclude idle time from quest and free-reward timers that should require presence, and design the 20-minute Roblox idle disconnect into the offline cap `[VS]`.
- **Lobby size**: each player's pets render on clients with a cap (see the pet playbook).
- When high speed is legitimate, movement checks compare against the player's server-known stat, not a global cap; very fast characters tunnel through thin parts, so use thick collision and server-side gate validation `[lihfolk]`.
- 20-plus players with trails and auras: budget particles per player and offer a hide-others toggle `[lihfolk]`.

## The one-new-verb angle

- The run is the verb: roll, bike, climb, ski, dig. A visible trip down the lane beats a number on a menu (vault patterns 2 and 3).
- Put the stat on the body or the vehicle so progress reads in a thumbnail: "1" snowball → planet-sized "1,000,000,000".
- Cut everything else at launch (bosses, carrying, weather, mutations); they return as weekly updates.
- Let the stat change the run, not only unlock it: speed that is harder to steer, size that changes what you can smash or fit through. Each World should add a movement rule (ice, bounce, moving gates), not a bigger number `[lihfolk]`.

## Common failure modes

- Stat-only game with no lane or journey; nothing to watch.
- Cloning a parent after its peak, or keeping a seasonal tag weeks after the season.
- First gate or first egg too far; players leave before the first Wins.
- Fixed stat packs and pads that become worthless (or mandatory) after the first rebirth.
- Running ads below an 85% rating (vault thumbnail rule 13).
- Remote-per-tick networking; server stalls with 30 players.
- Paid multipliers leaking into a PvP zone.
- The client reports its own stat; every cosmetic is expensive with no ladder from tiny to premium; the same lane with a bigger number each update (sessions shrink) `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | First gate inside 30 s, first egg inside 3 min | Lower gate 1 and egg 1; raise the free pad |
| 2 | Gates step about ×4; no gap takes over 5 min in World 1 | Re-space gates; add a Wins pad tier |
| 3 | The run is a visible trip | Build the lane; move rewards from menus into gates |
| 4 | Stat shows on the character | Add a scaled Blender prop with clamped scale |
| 5 | Session median ≥ 14 min, aim 19+ | Add free-rewards timers, quests, a second World earlier |
| 6 | Stat is server-ticked at 1 Hz; no per-tick remotes | Rewrite the tick; interpolate on the client |
| 7 | Gates and pads are validated by server position | Add server checks |
| 8 | Egg odds shown; policy gate present | See the pet playbook |
| 9 | 30+ repeatable products, several under 50 R$ | Add stat packs, 2× Wins, timed boosts |
| 10 | Packs scale with World | Tie pack size to World or to minutes of training |
| 11 | Rebirth keeps pets and paid pads, and is reachable in 20–40 min | Retune the first requirement |
| 12 | New World every week on a fixed day | Plan a 12-World runway; log each as an Experience Event |
| 13 | Rating ≥ 85% before any ad spend | Fix the first 3 minutes first |
| 14 | Each World adds a movement rule or obstacle idea | Redesign the next World around one new rule |
| 15 | Movement checks use the server-known stat | Replace global caps |

## Review gate

- [ ] Train, run, spend, advance and rebirth each fit one sentence, and the run is physical.
- [ ] Gate, egg and rebirth numbers follow the format ratios and are modelled against minutes.
- [ ] Stat and Wins are server-owned, ticked at 1 Hz, validated at gates.
- [ ] Product ladder is dev-product-led; paid multipliers never reach PvP; egg odds disclosed.
- [ ] Launch date sits in a seasonal window with a weekly World runway.
- [ ] Pads, gates, lane props and pets are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Genre deep dives, §Our games (read; 2026-11-07 snapshot; underlying mechanics from fan guides and Rotrends).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/incremental-sim.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/paid-random-items.md (read)
- Web search for developer write-ups of the +1 format (2026-11-10): no developer analysis found, only code-list and guide pages; no new claims taken from them.
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `59 Viral and Trend Game Teardowns/Teardown - +1 Speed Keyboard Escape.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
