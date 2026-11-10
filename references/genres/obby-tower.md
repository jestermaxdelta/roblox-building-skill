# Obby and tower playbook

Covers obstacle courses, round-based towers, difficulty-chart obbies and movement-skill platformers. Open it when jumping is the core action, when tuning jump feel and stage difficulty, or when auditing a live obby with low return rates and thin monetisation. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | Default character movement; a calibration course; 30 stages built from 8–10 reusable Blender pieces; a checkpoint per stage; server-validated pad touches; save the furthest stage | Custom jump physics, moving platforms, towers, time trials, shop |
| Intermediate | Sawtooth difficulty with breather stages; deaths-per-stage telemetry; jump buffer and coyote time; client-side moving platforms from server time; streaming; skip and second-chance offers | Server-timed runs, round towers |
| Expert | A movement verb with its own controller; server-timed, plausibility-checked leaderboards or server authority mode; seeded round towers; co-op and race modes; per-stage funnel tuning | — |

Terms: *checkpoint* = the pad a player respawns at; *coyote time* = a short window to jump after leaving a ledge; *jump buffer* = a jump pressed slightly early still fires on landing; *sawtooth* = ramps of rising difficulty separated by easier breather stages.

## Snapshot

- Market position (vault, 2026-11-07): **evergreen leader, cooling wave**. Tower of Hell 36K CCU. +1 Speed Keyboard Escape 33K from a 4.04M peak (down 61% Aug → Sep 2026); obby share of top-10 CCU went from 4.2% to 0% in October. Remixes did better than straight obbies: Escape Tsunami For Brainrots about 5M peak, Swing Obby for Brainrots 87K peak.
- Third-party trackers describe the genre as in gradual decline since mid-2024 `[community]`. It remains the cheapest genre to ship, so the tail is very long.
- Audience: the youngest and broadest; also a skilled niche (tower and difficulty-chart communities).
- Session shape: short attempts, natural stop points at each failure. Obbies should not be judged against simulator day-1 clocks, and Roblox publishes no genre-specific retention benchmark `[community]`. One tracker reports D1 25–35% for obbies with traffic; one developer of a themed obby reported D1 6.36% and D7 0.79% `[community]`. Use your own Creator Analytics benchmark.
- Official starting point: the Platformer template (double jump, dash, roll, long jump, moving and one-way platforms, coin pickups, an example tower) `[official]`.

## Core loop with timings

| Variant | Loop | Timing |
|---|---|---|
| Stage obby | Attempt → fail → respawn at checkpoint → clear → next stage | Stage 10–40 s; respawn under 1 s `[house]` |
| Round tower | Random sections stacked → climb before the timer → new tower | Rounds of a few minutes; no checkpoints `[house]` |
| Difficulty chart | Linear stages ordered by named difficulty tiers | Same as stage obby; late stages minutes each |
| Movement remix | Obby plus one movement verb (swing, glide, dash) or a chaser (tsunami) | First use of the verb inside 15 s |

- Retry is the loop: death to control must feel instant. No death animation, menu or ad between attempts.
- Teach by level design: each new obstacle appears alone and safe, then combined, then under pressure.
- Typical attempt length `[lihfolk]`: early stages 5–15 s, mid 15–40 s, late or hard 30–90 s. Add an internal checkpoint before a failure would make the player replay more than about a minute. Tower sections take 20–60 s each, tagged by difficulty and stacked easy-first.

## First 5 minutes

1. 0:00 control within 2 s of spawn; stage 1 is nearly flat so everyone reaches a checkpoint.
2. 0:30 three checkpoints passed; the stage counter ticks up with a sound.
3. 1:30 the first obstacle that can kill; the checkpoint is directly before it.
4. 3:00 first new obstacle type or the movement verb.
5. 5:00 around stage 15–25 for an average player `[house]`; a visible landmark (world 2 gate, tower top) ahead.
- A skip prompt may appear only after several failures on one stage, as a small dismissible button, and only where a free route exists.

## Progression and economy shape

- Feel knobs (house defaults): jump height 3–4 character heights reaching the apex in 0.30–0.40 s; fall gravity 1.5–2× rise; coyote time 0.08–0.12 s; jump buffer 0.10–0.15 s; variable jump (early release multiplies upward speed by 0.4–0.5); ground acceleration to full speed in 0.05–0.10 s; wall jump about 0.8× height with a 1.25× sideways kick. Derive `g = 2h/t²`, `v0 = 2h/t`. Hurtboxes slightly smaller than the visual.
- Difficulty curve: sawtooth. Each world ramps, then the next world opens easier than the last one ended. Track attempts per stage; a stage that takes the median player over about 8 attempts needs a nearer checkpoint or a wider landing `[house]`.
- Progress currency is the stage number. Add coins only if there is a shop worth saving for (trails, effects, pets as cosmetics).
- Long-term engine: worlds, a rebirth that restarts with a cosmetic rank, time trials with leaderboards, daily or rotating towers.
- Save the highest stage and world on the server.
- Default character numbers to design against `[lihfolk]` `[VS]`: walk speed 16 studs/s, `JumpHeight` 7.2 studs (or `JumpPower` 50 when `UseJumpPower` is on), gravity 196.2 studs/s². By arithmetic that is about 0.27 s to the apex and roughly 8–9 studs of flat travel in the air. Build a calibration course once per project (gaps of 6, 8, 10, 12 studs; ledges of 3, 5, 7) and record what a normal player clears reliably, what needs a run-up and what is impossible; settings, scale and animations all shift the result.
- Three jump bands `[lihfolk]`: comfortably inside the maximum (early stages and anything mobile-friendly), close to the maximum with a clean run-up (mid-game tests), at the edge with precise timing (hard stages only, never in the first 20).
- The feel knobs above describe a custom controller. For a classic obby keep the default character, which players already know, and spend effort on stage design; use custom jump physics when movement itself is the product `[house]`.
- Any change to speed, jump or gravity (boosts, coils, upgrades) changes the meaning of every gap `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: Starter Pack, VIP (cosmetic plus convenience), gift passes, private servers, cosmetic trails and effects.
- Add: skip-stage dev product (community prices: 25 R$ per stage reported; one guide advises 20 R$ or less, another suggests scaling price with difficulty) `[community]`; checkpoint-save in round towers; cosmetic movement gear.
- Delete: 2× Cash and currency packs unless a real shop exists; Luck; Auto-Collect; extra storage.
- Speed or gravity coils only if they do not trivialise stages or leaderboards: keep paid movement out of timed and ranked modes (house rule 3).
- A stage skip is a fixed, disclosed outcome, not a random item `[official]`.
- Rewarded video is strongest here `[official]`: first-spawn buffs, mid-session trials, post-failure second chance. Benchmark opt-in 15–25% at frequency 3; best in class 30%+ at 4+. Examples: Glide Tower 47% opt-in at 2.3 ("respawn at previous checkpoint"); Escape the Carnival of Terror Obby 27% at 3.9 (an item worth one life after failing).
- Developers report low pass sales in plain obbies `[community]`; expect dev products and rewarded video to carry revenue.
- The ethical line `[lihfolk]`: never tune a stage to be unfair so that skips sell. A stage far harder than its neighbours with a skip button beside it is noticed. This is also house rule 3.

## Retention and social hooks

- Reasons to return: new world or tower weekly on a fixed day, rotating daily tower, time-trial ghosts, badges per world.
- Social: race a friend (side-by-side lanes), carry-a-friend co-op stages, spectate on death in round towers, friends' stage numbers over their heads.
- Stage number on a public leaderboard and as an overhead tag is the status loop.
- Never punish quitting mid-stage; progress is the checkpoint.

## UI patterns

- HUD: stage number, world progress bar, a small "Skip?" button that only appears after repeated failure, timer in timed modes.
- Mobile: large jump button in the right thumb zone; camera sensitivity setting; no HUD element above the character's landing line of sight.
- Stage select board in the lobby (teleport to any cleared stage).
- Death feedback under 0.3 s: flash, sound, instant respawn.

## Systems to build, in order

System names refer to `references/gameplay-systems-cookbook.md`.

1. Checkpoints and stage saves (server-validated pad touches, respawn at stage).
2. Kill zones with client feedback and server confirmation.
3. Player data: furthest stage, current stage, best times.
4. Stage teleport and stage-select board (with stream requests).
5. Input feel: jump buffer, coyote time.
6. Moving and timed platforms on server time.
7. Per-stage telemetry (attempts, deaths, time).
8. Skip product and rewarded second chance.
9. Timed runs and leaderboards.
10. Round tower generator or a movement-verb controller.

## Technical hot spots

- **The Humanoid jump is a fixed arc.** Add buffer and coyote time on the client (see ui-input-crossplatform.md); extra fall force via `VectorForce` or `LinearVelocity` on the client, which owns the character. Design gaps from the metrics table in game-craft.md.
- **Checkpoint integrity**: checkpoints are invisible `SpawnLocation`s inside Blender pads. The server accepts a checkpoint only if it is the next in sequence (or within a small window), the player is physically near it, and a minimum plausible time has passed. Otherwise a teleport exploit clears the game in seconds and corrupts leaderboards.
- **Client-owned movement** means speed, fly and noclip are possible. For casual obbies, validate checkpoints and timed-run plausibility. For competitive time trials, either server-replay inputs, or adopt the server authority model (`Workspace.AuthorityMode = Server`) `[official]` `[VS]`.
- **Kill zones**: Blender models with invisible triggers. Detect on the client for instant feedback and confirm on the server; never `Touched` on the server alone for fast movers.
- **Moving platforms**: anchored, moved on each client from a shared server time (`Workspace:GetServerTimeNow()`), so they are identical for everyone and cost no replication. Unanchored physics platforms desync and stutter.
- **Streaming**: long obbies exceed memory on 3 GB phones without `StreamingEnabled`; teleports to a stage must wait for that stage to stream in (`Player:RequestStreamAroundAsync`).
- **Collision**: simple convex or box collision on platforms; every visible mesh is solid, so decoration near the path needs deliberate collision, not accidental snag points.
- **Round towers**: build each tower from a pool of Blender section models chosen by a server seed; the same seed for all players in the round.
- **Most exploited pattern in the genre** `[lihfolk]`: a client remote that says "I reached stage N". Progress comes only from server-validated pad touches, with a distance margin (about 6 studs, roughly 375 ms of walking) and a `Health > 0` filter so a ragdolled body sliding onto the next pad does not advance a dead player.
- Keep two values: `Furthest` (saved, never lowered) and `Current` (changes when the player travels back to replay). Throttle progress saves (about two a minute plus autosave) `[lihfolk]`.
- Timed runs are measured on the server between its own events (`os.clock()`); a client timer can be paused or edited `[lihfolk]`.
- With streaming on, kill zones connected once at start-up miss parts that stream in later; bind them as instances arrive (tags plus `CollectionService` signals) `[lihfolk]`.
- Mobile fairness `[lihfolk]`: avoid early jumps that need camera control and movement at once (turning in mid-air around a pillar); on touch that takes two thumbs plus the jump button.

## The one-new-verb angle

- Add a movement verb (swing, glide, grapple, wall-run) or an external pressure (rising water, tsunami, chaser). The remixes are what charted in 2026 (vault).
- Or change the frame: obby for a reward that lives elsewhere (pets, brainrots), co-op tethered obby, obby as a race.
- A plain rainbow stage obby enters the longest tail on the platform.

## Common failure modes

- First real difficulty before the first checkpoint; mass bounce in minute 1.
- Slow respawn or a prompt on death.
- Stage-skip prompts that interrupt, repeat or appear where no free route exists.
- Difficulty spikes with no data behind them; no per-stage attempt tracking.
- Trusting client checkpoint events.
- Paid coils that break leaderboards.
- Hundreds of unique meshes with no instancing; draw calls sink phones.
- Following the +1 obby wave after it cooled.
- Edge-of-range jumps in the first 20 stages; long stages with no internal checkpoint; stages tuned to sell skips `[lihfolk]`.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | 90%+ of new players reach checkpoint 3 | Flatten stages 1–3; shorten the spawn walk |
| 2 | Respawn to control under 1 s | Remove death animation and prompts |
| 3 | Per-stage attempts tracked as funnel events | Add events; review the top 5 drop stages weekly |
| 4 | No stage over about 8 median attempts without a nearby checkpoint | Add checkpoints or widen landings |
| 5 | Jump buffer and coyote time present | Add both on the client |
| 6 | Checkpoints validated for sequence, distance and time | Move validation to the server |
| 7 | Moving platforms are client-side from server time | Replace physics platforms |
| 8 | Runs on a 3 GB phone with streaming on | Enable streaming; instance repeated meshes |
| 9 | Skip button appears only after repeated failure and is dismissible | Rework the trigger; add 24 h suppression after two dismissals |
| 10 | Rewarded video offers a post-failure second chance | Add the placement; measure opt-in against 15–25% |
| 11 | Something new every week | Schedule a world or rotating tower |
| 12 | A movement verb or pressure distinguishes the game | Prototype one verb on three stages |
| 13 | Timed modes exclude paid movement | Separate ranked rules |
| 14 | Friends can race or co-op | Add side-by-side lanes or tether stages |
| 15 | A calibration course exists and stage gaps sit in the intended band | Build it; re-measure after any movement change |
| 16 | Deaths per stage logged; no stage at 10× its neighbours | Widen, add a checkpoint or move the stage later |

## Review gate

- [ ] Jump metrics are derived from the feel knobs and gaps from the metrics table.
- [ ] Stage order follows teach → combine → pressure; the curve is a sawtooth.
- [ ] Checkpoints, saves and timed runs are server-validated.
- [ ] Skip and revive offers are small, dismissible, post-failure only and have a free alternative.
- [ ] Streaming and instancing hold the 3 GB phone budget.
- [ ] Every platform, hazard and prop is a Blender model with intentional collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Trend lifecycle (read; 2026-11-07 snapshot).
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/obby.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/templates.md (read; Platformer template)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- https://devforum.roblox.com/t/ideas-to-better-monetize-my-obby/1654630 (search summary)
- https://devforum.roblox.com/t/how-to-refine-your-obby-game/862904 (search summary)
- https://devforum.roblox.com/t/obby-game-monetization-being-low/3141998 (search summary)
- https://devforum.roblox.com/t/ideas-to-improve-retention-on-a-themed-obby/1775815 (search summary)
- https://rowatcher.com/news/simulators-and-obbies-need-different-retention-clocks (search summary; host not reachable for a full read)
- https://rolearn.dev/insights/genre-saturation-opportunity (search summary; third-party)
- GitHub search for open obby kits (2026-11-10): no maintained, licensed kit of note found; results were mostly automation or exploit scripts (not used).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Obbies and Platformers.md`, `43 Genre Systems End to End/Obby Checkpoints and Stage Saves End to End.md` (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
