# Fashion, dress-up and judged-creation playbook

Covers timed dress-up shows judged by other players, avatar and outfit games, and the wider "create to a theme, show it, get voted on" format (building, drawing, decorating, cooking). Open it when peer voting on something a player made is the core of the round, when designing a fair vote and a cosmetic catalogue, or when auditing a live show game for vote abuse, thin free wardrobes and decline after a peak. Market numbers are the vault's 2026-11-07 snapshot `[VS]`; points tagged `[lihfolk]` are adapted from LihFolk Vault V2 (October 2026). For open-ended town roleplay see `social-roleplay.md`.

## Start here by level

| Level | Do first | Leave for later |
|---|---|---|
| Beginner | One round loop: theme → timed creation → runway → 1–5 star vote → podium; 60–100 free items on racks; a Freeplay room; pay every participant | Ranks, story quests, collaborations, passes, duo mode |
| Intermediate | Vote normalisation and anti-collusion; rank ladder from accumulated stars with item unlocks; saved outfits; pose packs; weekly item drop on a fixed day | Seasonal pass, lore quests |
| Expert | Win-rate tracking for free versus paying players; themed limited drops with real end dates; avatar performance budgets for a full runway; creator and collaboration pipelines; second judged mode | — |

Terms: *judged round* = a round whose winner is decided by other players' ratings; *Freeplay* = a mode with no timer, theme or voting.

## Snapshot

- Market position (vault, 2026-11-07): **established, past its peak, still large**. Dress To Impress 67K CCU (launched Nov 2023; 651K peak in Aug 2024 after a pop-star collaboration); Catalog Avatar Creator 52K. Evergreens in this space swing with collaborations and seasonal drops.
- LihFolk's case study `[lihfolk]` `[VS]`: 13-player servers; dashboard genre Roleplay & avatar sim › Dress Up; trackers report an all-time peak near 1.7M in Dec 2024 (not confirmed by strong sources). Its 2025 collaborations landed during a long decline: collaborations bring press and new audiences but do not by themselves fix a shrinking base.
- Why the format works `[lihfolk]`: the theme is a creative constraint (no blank page), the timer forces a finished result, and distributed judging produces winners and stories every few minutes. The first reward is social: real people voted on your look.
- The same loop fits building, drawing, cooking and decorating. Drawing or writing shown to others is free-form user creation and makes the game 16+ `[official]` `[VS]`; assembling outfits or builds from 3D assets does not.
- Audience: skews female and teen, streamer-driven discovery from outside the platform, phone-first.

## Core loop with timings

| Phase | Length | Notes |
|---|---|---|
| Intermission | 15–30 s `[house]` | Next theme announced |
| Create | About 6 min (vault; press reported 360 s) | Theme and timer stay on screen; shared dressing area with racks and stations |
| Show | 10–15 s per player `[house]` | Runway walk with a chosen pose |
| Vote | During each walk | 1–5 stars from every other player |
| Podium | 10–15 s | Top three on stage |
| Payout | Instant | Every player gets rank progress and soft currency by placement |

- A new player sees the whole loop, is judged by people and is rewarded within about seven minutes `[lihfolk]`.
- Round length sets the session: short rounds let a session be ten minutes or two hours.

## First 5 minutes

1. 0:00 join a server already cycling; if mid-round, land in Freeplay or spectate the runway with a timer to the next round.
2. 0:30 theme appears; arrows to the racks; many items free from the start `[lihfolk]`.
3. 1:00–5:00 dress: equip by walking to racks and tapping; undo and "clear" always visible; a three-item minimum hint so nobody walks out bare.
4. Then the first runway, first stars received, first payout.
- Never put a shop prompt in the first round. The newcomer's question is "can I make something good with free items?" and the answer must be yes.

## Progression and economy shape

- Two currencies `[lihfolk]`: Stars (accumulate into ranks that unlock items; a long goal for a loop with no levels) and Cash (buys clothing and accessories).
- Pay everyone, reward the top three: placement-based payouts keep losers in the game; the podium gives winners their moment `[lihfolk]`.
- Catalogue growth is the content treadmill: weekly items, seasonal sets, retired items with real dates (vault: Saturday boutique, retired items).
- Creative tools as progression: more item slots per outfit, material and pattern options, custom makeup, pose packs.
- Codes and limited items drive returns; keep windows humane (a three-hour code window, as one 2024 update had, excludes most time zones) `[lihfolk]`.
- Light story quests and lore between updates keep the game in conversation `[lihfolk]`.

## Monetisation set that fits

- Keep from the default set: VIP (cosmetic room, tag, extra stations), gift passes (native to this audience), private servers at a low price, Starter Pack as a fixed outfit set, 2× Cash, currency packs.
- Add: named outfit sets as passes (observed band 279–449 R$), creative-tool passes (custom makeup, materials, a higher item limit at 129–349 R$), pose and emote packs, a seasonal pass with a real end date `[lihfolk]` `[VS]`.
- Avatar items sold in-experience pay a 40% affiliate share `[VS]`; an outfit game is also a store.
- Delete: Luck and crates (the leader's pass list has no random boxes `[lihfolk]`), Revive, Auto-Collect, anything that sells votes, placements or rank.
- **Conflict (market vs house rule 3):** the leader sells a "run faster" pass at 149 R$; in a timed round, reaching racks faster is a real competitive edge `[lihfolk]`. Do not sell speed or extra time in judged rounds. Paid outfit sets change looks, not mechanics, and are acceptable only while free players can still win: track the podium rate of non-paying players and widen the free pool if it falls.
- Offers: on the podium screen and in Freeplay next to the item, never during the dressing timer.

## Retention and social hooks

- Voting is the hook: you play for approval and judge back. Duo mode lets two friends compete together `[lihfolk]`.
- Fixed weekly drop day; seasonal passes; an advent-style calendar that is cumulative, not streak-based.
- Poses and outfits become memes and clips; add a photo spot and a clean capture mode.
- Collaborations and creator events are multipliers on a healthy base, not a rescue.

## UI patterns

- Theme and timer pinned at the top for the whole dressing phase.
- Racks in the world with tap-to-equip; a compact outfit panel (worn items, colour and material pickers, undo, clear, save outfit).
- Runway: star buttons large and thumb-reachable, one vote per walk, the voter's own choice hidden from others.
- Podium and results: placement, stars earned, cash earned, rank progress bar.
- Works with chat disabled: poses, emotes and quick reactions carry expression.

## Systems to build, in order

System names refer to `references/gameplay-systems-cookbook.md`.

1. Round loop with phases and a theme list.
2. Outfit system: equip, colour, layer limits, save and load.
3. Item catalogue data and racks.
4. Runway sequencing and poses.
5. Voting with normalisation; results and podium.
6. Player data: stars, cash, owned items, saved outfits.
7. Rank ladder and unlocks.
8. Freeplay mode.
9. Shop, passes and gifting.
10. Weekly drop and code scheduler; then duo mode and quests.

## Technical hot spots

- **Vote integrity** `[house]`: players gain by rating rivals low. Hide who voted what; normalise each voter's ratings (subtract their mean) or trim the top and bottom ratings; ignore voters who give everyone the same score; give a small reward for voting at all; cap self-interest by not showing running scores during the show. Detect rings (the same accounts always rating each other 5) and discount them.
- **Avatar cost**: a runway of 13 avatars each wearing up to 18 layered items is the frame budget. Cap items per outfit, budget triangles and textures per item, and reduce off-stage avatars. Every item is a Blender asset authored to the avatar's cage; test on a 3 GB phone.
- **Outfit application on the server**: clients request item ids; the server validates ownership and slot limits and applies them. Saved outfits are id lists.
- **Coverage and maturity**: enforce a base layer so avatars are never unclothed; review theme lists for romantic or adult framing, which changes the maturity label `[official]` `[VS]`.
- **Text**: outfit names, custom theme suggestions and any typed text pass `TextService` filtering per viewer.
- **Timer fairness**: the dressing timer is server time; late joiners go to Freeplay or spectate rather than entering with seconds left.
- **Exploit surface**: equipping unowned items (server ownership checks), vote spam (one vote per target per round), teleporting on the runway (server-driven walk).

## The one-new-verb angle

- Keep the judged round, change what is made: a room, a float, a dish, a pet's outfit, a build from a kit.
- Change the judge: team votes, a rotating panel, audience plus a rule-based score.
- A plain fashion-show clone meets an incumbent with years of catalogue; pick a different craft or a sharper sub-audience.

## Common failure modes

- A free wardrobe too thin to win with; newcomers lose to paid sets every round and leave.
- Unprotected voting: everyone gives one star, friends trade fives.
- Selling speed, time or votes in a judged round.
- Long dressing timers with nothing to do after finishing early; add a "ready" option.
- Late joiners dropped into a round they cannot finish.
- Collaborations used to mask a retention problem.
- Limited codes with windows so short most players miss them.
- Catalogue growth that stalls; the format lives on new items.

## Level-up checklist for a live game

| # | Check | Fix if failing |
|---|---|---|
| 1 | A new player completes a full round and gets paid within 8 min | Shorten phases; join-in-progress to Freeplay |
| 2 | Free items can produce a podium outfit for every theme | Widen the free pool; test themes with free-only outfits |
| 3 | Non-paying players reach the podium at a healthy rate | Track it; rebalance paid sets as style, not coverage of themes |
| 4 | Votes are anonymised and normalised | Add normalisation and trimming |
| 5 | Flat-voters and vote rings are discounted | Add detection |
| 6 | Everyone is paid by placement | Add participation payouts |
| 7 | Rank ladder with unlocks exists | Add star ranks |
| 8 | Freeplay exists | Add a no-timer room |
| 9 | No pass changes speed, time or scores | Remove or convert it |
| 10 | Runway holds frame rate on a 3 GB phone | Item caps and budgets; off-stage reduction |
| 11 | Outfits are applied and validated on the server | Move equip logic server-side |
| 12 | Weekly drop on a fixed day; limited items have real, humane windows | Schedule drops; widen windows |
| 13 | Works without chat | Add poses, emotes and reactions |
| 14 | Theme list reviewed against the maturity target | Remove or rename risky themes |

## Review gate

- [ ] The round is theme, timed creation, show, vote, podium, payout, and fits in about seven minutes.
- [ ] Free players can win; vote integrity measures are designed.
- [ ] Nothing sold alters the competition; no random boxes are needed.
- [ ] Catalogue pipeline (Blender items per week) is planned for three months.
- [ ] Avatar budgets hold with a full server on stage.
- [ ] Clothing, racks, runway and props are Blender models with real collision.

## Sources

Accessed 2026-11-10.

- Owner's vault distillation: `references/market-scan-2026-11.md`, `references/market-research-v2-raw.md` §Shared DNA, §Trend lifecycle (read; 2026-11-07 snapshot).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `32 Case Studies of Top Roblox Games/Case Study - Dress to Impress.md` (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/content-maturity.md (read; free-form user creation, romantic themes)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/experience-genres.md (read)
- See also `references/case-studies-teardowns.md` for full game teardowns.
