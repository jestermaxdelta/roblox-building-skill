# Party and minigame-collection playbook

Covers round-based collections of short minigames, elimination game shows and hazard-survival rounds. Open it when "a different one-rule game every two minutes" is the product, when building a round framework that makes each new minigame cheap, or when auditing a live party game for dead time, repeats and bugs that appear after thirty rounds. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | A round manager with five phases; 4–5 minigames that share one contract; hard time limits; pay everyone each round; something to do while waiting | Map voting, levels, cosmetics shop, team games, 15+ minigames |
| Intermediate | Per-round cleanup (a Trove) and `pcall`-wrapped rounds; weighted pick that avoids recent repeats and respects player count; spectator activities; 10–15 minigames; streaming-safe map loads | Automated bot tests, ghosts |
| Expert | Automated round tests for every minigame; win rate tracked by spend tier; per-minigame exploit checks; a host character and escalation finale; live rotation of minigames by telemetry | — |

Terms: *minigame contract* = the interface every minigame module implements so the round manager can run any of them; *Trove* = a cleanup object (RbxUtil `Trove`; Janitor and Maid are older equivalents) that records everything a round creates and destroys it all at the end.

## Snapshot

- Market position: a long-standing category with spikes tied to outside trends. A show-themed elimination game fell from 151K tracked CCU (Oct 2025) to 14K as the show faded (vault, 2026-11-07). Roblox's dashboard lists Party & casual › Minigame as its own subgenre, and its design docs use a hazard-survival round game as a genre example `[official]`.
- Why it works `[lihfolk]`: variety (the next round is different), a low skill floor (one rule, one sentence), cheap losses (two minutes, then a fresh start) and social chaos that produces clips.
- Why it fails `[lihfolk]`: dead time, too few minigames (repeats inside 15 minutes), unclear rules and empty servers (most minigames need four or more players).
- Audience: the youngest and broadest; friend groups; very phone-heavy. Sessions 15–40 min.

## Core loop with timings

| Phase | Target `[lihfolk]` | Notes |
|---|---|---|
| Intermission | 10–20 s | Vote, buy, breathe |
| Map or game vote | Inside intermission | Three options; ties random |
| Rule card | 3–5 s | One sentence and one icon while players load in |
| Round | 60–180 s | Hard time limit, always |
| Results | 5–8 s | Winners, rewards, one highlight |

- A full cycle is 2–4 min. A lost round costs little; the next is different.
- Eliminated players need something to do: switch spectate target, predict the winner for a small reward, act as "ghosts" who drop harmless obstacles `[lihfolk]`.
- With too few players, let one player play something (solo course, practice, bots). Show a first arrival only "Waiting for 2 more players", with nothing to do, and that player leaves `[lihfolk]`.

## First 5 minutes

Genre beats only. Script format, teaching patterns, guidance devices and funnel steps: `tutorial-and-onboarding.md` §2, §3, §5 and §9; this genre's row is in its §10. No offer or social card in this window (offer gate).

1. 0:00 join mid-cycle into a lobby with a toy (a small obby, a ball) and a visible countdown under 60 s.
2. 0:45 first rule card; first round starts with everyone.
3. 2:30 results: participation coins even for last place.
4. 3:00 second, different minigame.
5. 5:00 a level-up or first cosmetic unlock; the vote shows three games not yet played.

## Progression and economy shape

- Every round pays every player: a base amount for taking part, extra by placement, and a winner's bonus, so someone who never comes first still moves forward `[lihfolk]`.
- Round XP feeding a level track is the long goal of a session; what players earn and buy is mostly cosmetic: trails, win effects, victory poses, emotes, titles. Win effects on the results screen are seen by the whole server.
- Daily and weekly challenges ("win three team games") steer players toward minigames they skip.
- A good minigame `[lihfolk]`: one rule; visible state (who is winning); comebacks possible; ends on time or early with a clear winner; declares its player range; fair on phones (no precise jumps or small buttons unless that is the point).
- Portfolio: survival or elimination, race, collection, team, reaction, hidden-role, creative-and-vote, asymmetric. Launch with at least 10–15 so a 20-minute session rarely repeats `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: VIP (coin multiplier, lobby area), gift passes, private servers (friend groups and parties), currency packs, Starter Pack as a cosmetic bundle, 2× Cash or EXP boosts.
- Add: trails, win effects, victory poses, emotes, titles; a limited, transparent "choose the next minigame" product (annoying if bought every round) `[lihfolk]`.
- Delete: Luck, Revive in competitive rounds, Auto-Collect, extra storage.
- House rule 3: no in-round power-ups for Robux (shields, speed) in competitive minigames. Extra vote weight for VIP, if any, stays modest so free players still win votes `[lihfolk]`; the stricter house reading is to sell no vote weight at all.
- Measure win rate by spend tier: if payers win much more, rounds are pay-to-win `[lihfolk]`.
- Rewarded video: post-round payout boost or a second chance in non-competitive survival rounds (survival playbook `[official]`: opt-in 13%+, frequency 2.5+).

## Retention and social hooks

- New minigames on a fixed weekly or fortnightly day; rotate the pool by telemetry (drop the least-finished games).
- A host character or theme ties random games together; escalation toward a special final round `[lihfolk]`.
- Clip moments: a dramatic final two, slow-motion finishes, silly physics.
- Private servers and party join. A win streak is a score that ends on a loss: keep the best streak as a permanent record, attach no reward multiplier to it, and offer a saver only under the Conflict note in `survival-crafting.md` §Monetisation (ad or earned token, never Robux).

## UI patterns

Genre specifics only. Zone layout for this archetype and the shop, inventory, settings and reward-screen recipes: `ui-screen-recipes.md` (HUD layouts by genre). Effects to build first, from `vfx-recipes.md`: coin or reward burst, explosion, shockwave.

- A phase banner with a countdown driven by server time; a rule card with one icon.
- Scores or elimination counts above heads; a shrinking-zone indicator where relevant.
- Results: podium, payout, one highlight; a three-card vote.
- Spectator bar: next and previous target, predict button.
- Works without chat: quick-chat buttons and votes for hidden-role minigames.

## Systems to build, in order

Closest sections of `references/gameplay-systems-cookbook.md`: §10 Rounds, match state machine and intermission, §11 Teams, matchmaking, queues and reserved servers, §20 Checkpoints and obby stages, §13 NPC and enemy spawning and AI, §3 Shop. Its "Build order by genre" table gives a second opinion.

1. Round manager (phases, timers, end conditions that count remaining players).
2. Minigame contract and loader; per-round Trove.
3. Map loading from `ServerStorage` with streaming requests; spawn points; kill planes.
4. Player round state: in round, eliminated, spectating, AFK.
5. Spectating and spectator activities.
6. Rewards, XP and levels; player data.
7. Voting and weighted selection.
8. Cosmetics and shop.
9. Bot-driven automated round tests.

## Technical hot spots

- **Make adding a minigame cheap** `[lihfolk]`: every minigame is one module implementing the same contract (name, player range, duration, `start`, `cleanup`, result) plus one map. The round manager owns selection, map load, spawning, the rule card, the time limit, cleanup, rewards and the return to lobby.

```lua
--!strict
-- Unexecuted sketch: the contract each minigame module returns.
export type RoundResult = { winners: { Player }, scores: { [Player]: number } }
export type Minigame = {
	name: string,
	rule: string, -- one sentence for the rule card
	minPlayers: number,
	maxPlayers: number,
	duration: number, -- hard limit in seconds
	start: (players: { Player }, map: Model, trove: any) -> (),
	finish: () -> RoundResult,
}
```

- **Cleanup discipline**: connections, parts, tools and timers from round 3 must not exist in round 31. Register everything with a per-round Trove and destroy the map. Wrap `start` in `pcall` or `xpcall` so one broken minigame ends its round instead of freezing the loop `[lihfolk]`.
- **Map loads**: clone small maps from `ServerStorage`, destroy after. With streaming on, call `Player:RequestStreamAroundAsync` before teleporting or players spawn into nothing. Large maps loaded every two minutes cause hitches and replication bursts.
- **Phase sync**: the server owns the phase; replicate phase name and end time; clients count down from `Workspace:GetServerTimeNow()`.
- **Leavers**: end conditions recount remaining players every tick so a round never hangs on someone who left.
- **Exploits**: per-minigame server checks (position plausibility, checkpoint order); server-owned physics objects and collision groups in physics games.
- **Testing**: many minigames and little coverage means a rare one stays broken for weeks; run every minigame with bots in Studio as an automated test `[lihfolk]`.
- Maps and props are Blender kits reused across minigames; every piece has real collision.

## The one-new-verb angle

- A host with a personality, or a frame that changes how rounds connect (a board, a tournament ladder, a draft).
- One physics toy shared by all minigames.
- Do not anchor the concept to a current show: it fades with it (vault).

## Common failure modes

- Dead time anywhere: lobby, elimination, minimum-player waits.
- Fewer than ten minigames; repeats within one session.
- Rules that need a paragraph.
- Leaked connections that award points rounds later; memory that grows all day.
- Rounds that never end after a leaver.
- Precise platforming on phones.
- Paid in-round power-ups.
- One broken minigame freezing the server loop.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | No player waits more than 20 s with nothing to do | Lobby toy, spectator actions, solo mode |
| 2 | Cycle time is 2–4 min; rounds have hard limits | Add limits; trim intermission |
| 3 | 10–15+ minigames; selection avoids recent repeats and fits player count | Add games; weighted pick |
| 4 | Each rule fits one sentence and one icon | Rewrite or cut the minigame |
| 5 | Everyone is paid every round | Add participation rewards |
| 6 | Memory and connection counts are flat after 50 rounds | Add a Trove; hunt leaks |
| 7 | A minigame error ends only its round | Wrap in `pcall`; log and skip |
| 8 | Rounds end correctly when players leave | Recount each tick |
| 9 | Map load causes no hitch; players never spawn into unstreamed space | Smaller maps; stream requests |
| 10 | Win rate does not rise with spend | Remove paid power; rebalance |
| 11 | Every minigame is fair on touch | Retune or flag as PC-heavy and weight down |
| 12 | Each minigame has a server-side exploit check | Add plausibility checks |
| 13 | Bot tests run every minigame before release | Build the test harness |

## Review gate

- [ ] Round manager and minigame contract exist before the third minigame is written.
- [ ] Dead time is designed out of every phase.
- [ ] Cleanup, error isolation and leaver handling are tested over many rounds.
- [ ] Portfolio covers several types and player counts.
- [ ] Revenue is cosmetic; no in-round paid power.
- [ ] Maps and props are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-research-v2-raw.md` §Trend lifecycle (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Party and Minigame Collections.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/experience-genres.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/survival.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
