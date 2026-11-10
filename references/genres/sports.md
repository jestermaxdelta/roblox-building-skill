# Sports and physics-sports playbook

Covers team ball sports (football, volleyball, basketball), ability or anime sports, and individual physics sports (golf, bowling). Open it when a shared ball and short matches are the game, when choosing how the ball is simulated over the network, or when auditing a live sports game for laggy kicks, uneven teams and pay-to-win pressure. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026).

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One small pitch, 3v3, 3–5 min matches; possession model (ball attached to the carrier) with a simple server-decided shot; auto team assignment; one context action button | Ranked, clubs, abilities, fouls, replays, goalkeepers |
| Intermediate | Deterministic ball flight from one launch message; bots that fill and yield slots; practice area as tutorial; pass aim assist; stats and results screen | Elo ranking, community league tools |
| Expert | Ranked with Elo and placement weighting; contested-ball arbitration with grace windows; spectator and referee tools; server authority mode or a custom predicted ball; ability balance | — |

Terms: *possession model* = while a player has the ball it is positioned at their feet or hand rather than simulated; *deterministic flight* = the ball's path is a pure function of launch data and time, so every client can draw it from one message.

## Snapshot

- Market position (vault, 2026-11-07): **solid middle tier; physics sports rising**. Volleyball Legends 38K CCU, Illegal Soccer 36K; Practical Basketball rose 523% on an update. A physics-sports × incremental pairing was judged weak (already covered by a lucky-block kicker).
- Roblox publishes a rewarded-video playbook for the genre and cites NFL Universe Football and Blue Lock Rivals `[official]`.
- Styles `[lihfolk]`: realistic (teamwork, positioning; older fans and leagues), arcade (simplified rules, exaggerated physics; broad and young) and ability sports (powers and character kits; the anime and battlegrounds audience). Arcade and ability styles fit phones and the platform's audience better.
- Audience: competitive but social; community-run leagues on private servers are a major growth source `[lihfolk]`.
- Dashboard genre: Sports & racing › Sports `[VS]`. Use original teams, kits and names; real leagues, clubs and players are protected.

## Core loop with timings

| Layer | Length `[lihfolk]` | Content |
|---|---|---|
| Play | 1–10 s | Receive, move, pass, shoot, tackle |
| Possession | 10–60 s | One team's attack |
| Match | 3–8 min | Score, win |
| Session | 20–60 min | Several matches, casual or ranked |
| Meta | Weeks | Rank, skills, cosmetics, club |

- Adapt real rules `[lihfolk]`: 3v3 to 6v6 so everyone touches the ball; no offside; fouls simplified or automated; an AI keeper or no keeper in casual modes.
- Join and play in seconds: a new arrival is placed on a team or in the next-match queue at once, with a practice area while waiting. Waiting time under 30 s.

## First 5 minutes

1. 0:00 spawn in a practice area beside the pitch with a ball at your feet.
2. 0:20 first shot at a target; charge-to-power taught by doing.
3. 1:00 take over a bot's slot in a live casual match, or kick off a bot match if the server is empty `[lihfolk]`.
4. 3:00 first pass completed with aim assist; first goal or assist credited on the feed.
5. 5:00 results screen: personal stats, a cosmetic unlock, one-tap rematch.
- Everyone already knows "put the ball in the goal"; do not explain it. Teach the two or three deep moves in practice drills.

## Progression and economy shape

- Power is flat in competitive modes: the same base speed for every character. Progress is rank, stats, cosmetics and club standing.
- Depth lives in a few practised moves (curved shots, timed tackles, tricks) rather than stat growth `[lihfolk]`.
- Ability sports: characters or styles are sidegrades; if styles are rolled, see the gacha rules in `fighting-battlegrounds.md` (earn-only rolls for anything that affects play).
- Ranked `[lihfolk]`: Elo-style rating; for teams, expected result from average team ratings, update each player by the team result, weight new players' updates higher, penalise leaving. Open ranked only when casual queues are short.
- Currency from matches buys kits, boots, balls, trails and celebrations. Stats saved per player: goals, assists, passes, saves.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic), gift passes, private servers (leagues, clubs and tournaments run on them), Starter Pack as a cosmetic bundle, currency packs for the cosmetic currency, 2× EXP or currency as a timed boost.
- Add: kits, boots, balls, trails, goal celebrations and emotes (the genre's main spend), a battle pass with cosmetic tracks and per-position challenges, a small club-creation fee that also filters spam `[lihfolk]`.
- Delete: 2× Cash permanents that buy power, Luck on anything that affects play, Revive, Auto-Collect, extra storage.
- Rewarded video `[official]`: post-match earnings boost, a currency reward beside paid bundles, rematch rescue (re-enter without waiting). Best triggers are emotional moments: before a match, after a loss, after a win. Benchmark opt-in 15%+, frequency 3+.
- **Conflict (official playbook vs house rule 3):** Roblox's sports playbook also lists a "pre-game edge" (a one-session speed, stamina or power boost). LihFolk advises against selling stat boosts because they destroy competitive trust, and house rule 3 forbids stat power in competitive modes. Follow the house rule: pre-match boosts apply to XP and currency only, or to non-ranked practice.

## Retention and social hooks

- Short matches and one-tap rematches; daily and weekly challenges per position.
- Clubs and community leagues: support them with private servers, a referee or host panel and match recording `[lihfolk]`.
- Ranked seasons with cosmetic rewards and soft resets.
- Celebrations are social currency; spectating and substitution keep waiting players engaged.

## UI patterns

- HUD: score, timer, stamina, a possession indicator, one context action button (shoots near goal, passes otherwise) plus sprint and tackle; five buttons is already the phone limit `[lihfolk]`.
- Broadcast-style camera for team sports (side-on or behind the team) that keeps ball and goal in view; follow camera for individual sports.
- Pass aim assist toward a teammate in the aimed direction makes team play possible on touch `[lihfolk]`.
- "GOAL" banner and replays only after the server confirms.

## Systems to build, in order

System names refer to `references/gameplay-systems-cookbook.md`.

1. Teams and auto-balancing; round and match flow (kickoff, score, timer, results).
2. Ball system: possession, launch, deterministic flight, server decisions.
3. Rules engine: goals, out of bounds, restarts.
4. Practice area and drills.
5. Bots that fill and yield slots.
6. Stats and player data.
7. Cosmetics: kits, balls, celebrations.
8. Spectating and substitution.
9. Ranked rating and queues.
10. Clubs with filtered names; league tools.

## Technical hot spots

- **The ball problem** `[lihfolk]`: every player wants instant control of one object that each client sees at a different time.

| Approach | Kicker feels | Others see | Risk |
|---|---|---|---|
| Server owns and simulates | Delayed 100–300 ms | Consistent | Sluggish on high ping |
| Ownership moves to the possessor | Instant | Jumps on hand-over | Owner can move the ball anywhere (exploit) |
| Possession model + server-decided flight | Instant dribble | Clean | Less physical feel |
| Server-authoritative ball with client prediction | Instant, then corrected | Smooth | Most code |

- House default: possession model with deterministic flight. Flight is one message (start position, start velocity, server start time); every client renders `positionAt(launch, Workspace:GetServerTimeNow())`, and the server uses the same function for interceptions and goals. Never replicate the ball's CFrame every frame.

```lua
--!strict
-- Unexecuted sketch: shared by server and clients (ModuleScript in ReplicatedStorage).
export type Launch = { origin: Vector3, velocity: Vector3, startTime: number, gravity: number }

local function positionAt(launch: Launch, serverNow: number): Vector3
	local t = math.max(0, serverNow - launch.startTime)
	return launch.origin + launch.velocity * t + Vector3.new(0, -0.5 * launch.gravity * t * t, 0)
end

return positionAt
```

- Walls, posts and bounces: the server raycasts along the predicted path segment by segment and issues each bounce as a new launch. Curve shots add a sideways term to the formula rather than using physics `[lihfolk]`.
- **Contested balls**: decide on the server's timeline with a small capped grace window; show a stumble for the loser so the loss reads as play, not lag `[lihfolk]`.
- **Server authority model** `[official]` `[VS]`: documented for sports; the engine-level route to a predicted ball. Evaluate for new projects.
- **Real physics balls** suit hangouts, chaos arcade games and one-owner sports (golf, bowling: the shooter owns their ball) `[lihfolk]`.
- **Exploit surface**: steal or shoot requests every frame (per-action cooldowns, range checks, rate limits), speed hacks (server speed checks), ball teleport (never client-owned in competitive modes).
- **Characters**: collision groups so players do not push and fling each other; tackles are custom logic.
- **Leavers**: bots fill slots; rating penalty in ranked. Small pitches need no streaming; large ones need a radius that covers the pitch.
- Club names and kit text pass `TextService` filtering per viewer.

## The one-new-verb angle

- Bend one rule hard: "illegal" versions of a sport, abilities on a ball, a moving or hazardous pitch.
- Borrow the ball for another genre's goal: a ball in a battlegrounds arena changes the win condition.
- A sport rarely built on the platform, kept arcade and 3v3.

## Common failure modes

- A plain unanchored ball owned by whoever touched it last: laggy for some, exploitable by all.
- Per-frame ball replication.
- 11-a-side teams and long matches; most players never touch the ball.
- Complex foul rules nobody understands.
- Empty servers with no bots; newcomers wait and leave.
- Selling speed or shot power.
- Ranked opened before casual queues are healthy.
- Real club names, logos or player likenesses.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | A new player touches a ball within 20 s and joins a match within 60 s | Practice ball at spawn; bot slots to take over |
| 2 | Kicks feel instant at 150 ms ping | Move to possession model with deterministic flight |
| 3 | Ball state is server-authoritative; no client ownership in competitive modes | Rework ownership |
| 4 | Ball replication is per launch, not per frame | Replace CFrame streaming with launch messages |
| 5 | Teams are 3v3–6v6 and matches 3–8 min | Shrink teams and timers |
| 6 | Bots fill empty slots and yield to joiners | Add bot players |
| 7 | Steal, tackle and shoot have server cooldowns and range checks | Add validation and rate limits |
| 8 | Players cannot fling each other | Collision groups; custom tackles |
| 9 | Touch has a context action button and pass assist | Rework mobile controls |
| 10 | Nothing sold changes speed, stamina or power in ranked | Convert to cosmetics |
| 11 | Private servers and host tools support leagues | Add host panel and spectate |
| 12 | Ranked exists only with short queues; leavers penalised | Gate ranked on population; add penalties |
| 13 | Celebrations and kits are the visible spend | Add celebration slots and a kit shop |

## Review gate

- [ ] Style chosen (realistic, arcade or ability) and rules adapted to small teams and short matches.
- [ ] Ball model decided, deterministic and server-authoritative; contested-ball rules written.
- [ ] Bots, practice area and instant join cover low-population hours.
- [ ] Revenue is cosmetic; the pre-game power boost is not sold.
- [ ] Original teams, kits and names; all player text filtered.
- [ ] Pitch, goals, balls and kits are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `10 Game Design and Genres/Genre Playbook - Sports.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/rewarded-video-playbooks/sports.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/projects/server-authority/index.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
