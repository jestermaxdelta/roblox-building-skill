# Growth and marketing: getting players in 2025–2026

How a Roblox game gets players beyond what Recommended For You hands it: the readiness gate, on-platform levers, Ads Manager, short-form video, creators, community, announcements, codes, cross-promotion, localisation and the rules that marketing most often breaks. Open it at Phase 11 (launch) and Phase 12 (LiveOps), and in level-up mode when the audit lands on triage step T8 or T1 (`references/audit-existing-game.md`). Evidence for off-platform tactics is thin and mostly anecdotal; those rows are tagged `[community]` and are heuristics.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Pass the readiness gate below before telling anyone. 2. Make one share link per place you post. 3. Create the Roblox group and one Experience Event. 4. Post real clips of the first minute | Ads, creator deals, experiments, localisation beyond auto-translate |
| Intermediate | Soft launch with recommendations excluded, a measurement campaign, a fixed update day with an event each time, clip features in the game, per-channel cohorts in analytics | Scaling ad spend before the value of a player is known |
| Expert | Value-per-player and payback by source, creative testing through campaigns, lapsed-player reactivation, creator programmes with disclosure briefs, the CCU model, search-query tracking | Nothing; re-check `[VS]` facts each quarter |

Terms: **cost per play (CPP)** ad spend ÷ plays; **ROAS** value earned from an ad cohort ÷ spend; **share link** a trackable Roblox link that reports new users per channel; **LaunchData** a short string carried by a link or ad into the game (`Player:GetJoinData()`); **soft launch** public but not yet pushed, used to measure; **cohort** players grouped by first-play date or source.

Contents: 1 Order of operations and soft launch · 2 Channel map · 3 Ads Manager · 4 Short-form video · 5 Creators · 6 Community · 7 Updates, events, launch window · 8 Codes · 9 Cross-promotion, search and localisation · 10 What breaks the rules · 11 Rescuing a weak launch · Level-up table · Review gate · Sources.

## 1. Order of operations

Traffic multiplies whatever the game already does to a new player. Buy or borrow reach only after the readiness gate passes.

| Gate item | Threshold | Why |
|---|---|---|
| Onboarding funnel, economy and offer events live | Required | Otherwise the spend teaches nothing |
| First-play bounce and D1 | At or above the dashboard benchmark median; with no dashboard benchmark, D1 above the 11% house launch target `[house]` (market-scan-2026-11.md; the large-title median is 10.3%, analytics-and-discovery.md §Benchmarks) | Roblox: improve retention and engagement before acquiring `[official]` |
| Like ratio | ≥ 85% | A sponsored tile pays to display the rating (market-scan rule 13); ad-running games sit at a 79% median vs 92% for others (vault sample) |
| Tile matches the first minute | Thumbnail rules 1–13 pass; rubric in `icons-thumbnails-and-store-page.md` §15 scores 8.5+ | Mismatched metadata reduces exposure `[official]` |
| Stability | Crash rate under 2–3%, join ≤ 15 s on low-end Android | A spike magnifies crashes |
| Value of a new player known | 30-day revenue per new user by source, from the Acquisition new-users funnel | Sets the cost-per-play ceiling |
| Kids/Select status known | Trial (16+ only) or eligible | Decides audience and channel |

Do not launch at all while any of these is true `[lihfolk]`: no outsider to the team has played the whole first session on a mid-range phone; nobody knows the join time on a phone; no funnel logs join to minute 10; the save system has not survived a forced server shutdown test. Delay a week instead; the first impression is spent once.

Soft launch `[official]` setting, `[lihfolk]` method: publish publicly with Audience → Advanced → "Exclude from recommendations" on, bring a few hundred players you control (community, testers' friends, a small Plays campaign), and read four things in order: crash-free sessions with zero data loss, the shape of the onboarding funnel, median first-session length, D1 direction. Those players would not count toward ranking anyway, so the rehearsal is free. Rule-of-thumb bars before turning recommendations on `[lihfolk]`:

| Soft-launch cohort metric | Fix before opening | Fine to open |
|---|---|---|
| New players reaching the first reward within 60 s | Under 70% | 85%+ |
| Largest drop at any one step within the first 3 minutes | Over 25% | Under 15% |
| First session, median | Under 5 min | 10+ min |
| D1 | Below the dashboard benchmark, or under 8.4% on the fallback row | Near or above the median |

What counts for ranking `[official]`: Recommended For You ranks only on users who arrived organically through it. Players from ads, search, friends, share links and social media never enter those signals, but any plays help a game get considered. So outside traffic cannot repair weak organic signals, and cannot damage them either.

## 2. Channel map

| Channel | Cost | Best for | Measure with | Notes |
|---|---|---|---|---|
| Recommended For You | Free | Everything; over 90% of traffic starts on Home | Acquisition → Home Recommendations | Earned by signals, see analytics-and-discovery.md |
| Search | Free | Named demand from clips and creators | Acquisition → Search | Keep the name stable; exact-name search arrivals can qualify for Audience Expansion `[official]` |
| Experience Events and update announcements | Free | Returning players, update spikes | Event RSVPs, announcement views | §7 |
| Notifications, invites, referrals | Free | Lapsed and social players | Notification analytics, `ReferredByPlayerId` | liveops-quests-retention.md |
| Share links | Free | Attribution of every off-platform post | New-users funnel by link | One link per channel and per creator |
| Sponsored experiences and search ads | Paid | Seeding data, the 250-play gate, scaling a game that already converts | Ads Manager report + Acquisition | §3 |
| TikTok, YouTube Shorts | Time | Awareness, 13+ and 16+ audiences, search demand | Share link, Search source | §4 |
| Creators | Paid or free | Spikes, trust, long-form walkthroughs | Share link per creator | §5 |
| Roblox group, Discord | Time | Retention of the core, feedback, testers | Group size, returning-user plays | §6 |
| Standout Games, Off-Platform Featuring | Free, curated | Original games with regular events | Curated-sort traffic | Nominate; submit events 7+ days ahead `[official]` |

## 3. Roblox Ads Manager `[VS]`

Formats and mechanics `[official]`:

| Item | Fact |
|---|---|
| Access | 13+ with verified email. Card payment 18+ ($1 verification hold; first-time card users are charged $5 toward the first bill). Ad credits from Robux for 13+: 1-credit minimum, irreversible; Robux earned at the US 18+ DevEx rate are converted first, so convert deliberately. One ad credit cost 263 Robux in September 2025 (staff post; read the conversion preview) `[VS]`. Group-owned games get their own ad account through the group switcher |
| Sponsored experiences | A sponsored tile on Home; the same campaign also runs in search results. The sponsored tile and the organic tile can both show to one user. Since October 2026 sponsored tiles also reach users 13 and under (age-appropriate, labelled, not based on personal data), and gameplay video in sponsored tiles was announced as rolling out (staff post, 2 Oct 2026) `[VS]` |
| Search ads | Up to 10 keywords per ad set, exact keyword match, shown at the top of results or directly after an exact-name match. No audience targeting (all regions, 13+). Second-price auction adjusted for relevance: bid only on keywords the game truly matches. The search-ads page still describes an older keyword flow with an objective named Visits while the Ads Manager page says campaigns appear in search automatically: check the live UI |
| Immersive ads | Billboards (image, or video up to 30 s) and portals placed inside other creators' games; a portal teleports the player in. These are also what a publisher places to earn |
| Objectives | **Plays** (broad, cheapest, early traffic and tests); **Earnings** (still marked "Limited" in the docs; beta from May 2026, opened to "nearly 30,000" eligible games on 2 Oct 2026; eligibility is a monetisation threshold Roblox does not publish; likely spenders, higher cost per play, judged on return on ad spend); **Engagement** (age-checked highly engaged players who count toward the Kids/Select 250-play threshold; smaller audience, higher cost, does not auto-pause at the goal) |
| Audiences | All; New (never played or 180+ days away); Recent (last 30 days; needs 10,000+ recent players); Lapsed (30–180 days; needs 20,000+ lapsed players). Advanced targeting by location, age, gender, genre, device raises cost per play |
| Budget and bidding | Daily or lifetime budget; automated bidding; engaging games receive ad-system discounts; unused credits return when the campaign ends |
| Creatives | Up to 10 thumbnails per campaign, 16:9, split evenly, toggled individually (docs; a May 2026 staff post says 25: check the live UI). An "AI generate" option exists: do not use it (house rule 1 and the accuracy rule; creatives are real captures of the Blender-built game) |
| Timing | Moderation within about 24 h (staff, Oct 2026: review queues now take minutes); first 24 h is a learning phase; reports lag up to 48 h. Staff advice: assess after 7–10 days, and do not pause inside the first 24–48 h because the learning period restarts |
| Fixed after publishing | Goal, audience and budget type cannot be edited; name, budget amount, schedule and creatives can. A wrong audience means a new campaign |
| Invalid traffic | Campaigns are re-checked for fraudulent traffic 14 days after they end and billing is adjusted |
| Attribution | New player: 30 days credited to the ad. Returned after 7–29 days away: 7 days. Returned after 30+ days away: 30 days. Played in the last 7 days: that session only. Read the New, Recent and Resurrected views, not only All Users |
| Launch data | Advanced join options pass LaunchData so the game can tailor onboarding per campaign (tutorial for New, "welcome back" for Lapsed) |
| API | Open Cloud Ads API (`/ads-management/v1`): v1 supports the ENGAGEMENT objective only; budgets are micro-USD strings; creatives are uploaded image assets |
| Effect on organic | None on ranking; an ad-acquired user's later play never becomes a ranking signal, even when they return through Home. That user generally stops seeing the organic tile, so organic impressions can dip during a campaign. That is not a penalty |

Costs (none of these is a guarantee):

| Claim | Value | Source and grade |
|---|---|---|
| Roblox, RDC 2025 recap (10 Sep 2025) | Cost per play "over 71% cheaper"; a player "for less than $0.01" | `[official]` claim, no baseline or spend level given (read) |
| Roblox staff posts, 2025 | 44% and 60% cost-per-play decreases quoted in different posts | `[official]`, the two figures conflict (search summary) |
| Roblox, Ads Manager recap (2 Oct 2026) | Across 21 campaigns in randomised studies: median +14% play sessions and +10% D7-retained users among users shown ads. Of 1,200+ games on the Earnings objective, nearly two in three that reinvested up to 4% of earnings passed 100% return on ad spend (sample: games with 6+ Robux of revenue per user) | `[official]`, Roblox's own studies of selected games (read) |
| Forum-quoted averages by objective | About $0.007–0.011 per play | `[community]`, undated (search summary) |
| Vendor guide | $0.0073 per play, Nov 2025 | `[community]`, vendor source (search summary) |
| Roblox marketing page | Games running ads: +150% impressions, +24% plays, +16% playtime; one top-100 shooter gets up to 10% of plays from sponsored ads after scaling 10 → 25 creatives | `[official]` marketing |
| Developer reports | Mixed: some call it a money drain for small games; one July 2025 bug report shows about 28× fewer impressions per dollar in the redesigned Ads Manager than in the classic one (1.8M for $79 against 119K for $147) | `[community]` anecdotes (read) |

When ads are worth it:

- The readiness gate in §1 passes, and the purpose is one of: (a) a measurement buy of a few hundred first sessions to read the funnel; (b) the Engagement objective to clear the 250-play gate, on its own budget, paused at the goal; (c) scaling when the value of an ad-acquired player exceeds the cost per play; (d) re-engaging Lapsed players for a dated update.
- Not worth it: to fix low organic impressions (ad users do not feed ranking), while the like ratio is under 85%, before funnels exist, or when judged on day 1. Roblox's guidance for the Engagement objective is to give a campaign several days, and to fix onboarding if nothing moves after 3–5 days `[official]`.

Target cost per play `[house]` formula, `[VS]` inputs:

```
value per ad player (USD) = earned Robux per ad-acquired user over 30 days × DevEx rate
                          + rewarded-video earnings per user
                          + expected Audience Expansion share (usually 0 for ad traffic)
max cost per play = value per ad player ÷ target margin (1.5 while learning, 1.2 at scale)
```

- Read "30D revenue per user (cumulative)" for the Sponsored ads row in Acquisition → new users funnel; confirm whether it is before or after the 30% platform fee.
- DevEx is $0.0038 per earned Robux (monetization-and-policy.md). Worked example: 4 earned R$ per ad player → $0.0152 → ceiling about $0.010 at a 1.5 margin. At 1 earned R$ the ceiling is about $0.0025, below every quoted cost per play: do not scale, fix conversion first.
- When paying with ad credits bought with Robux, do the same sum in Robux using the conversion preview.

Plays are not players `[lihfolk]`: Ads Manager counts plays, and one person can produce several. For cohort maths tag ad joins through LaunchData, count unique users and compute revenue per unique user; otherwise the two denominators disagree.

Conflict: quoted costs differ by an order of magnitude. Roblox's posts and forum quotes put a play under $0.01; LihFolk's worked example uses an illustrative $0.10 per play and lands at a 30-day ROAS near 0.08, concluding that paid acquisition rarely pays back on purchases alone for small games. Neither is your number. Run the measurement campaign, read your own CPP and cohort revenue, and expect creative quality (CPP) and monetisation depth (revenue per player) to dominate; with auto-bidding there is no bid lever.

Campaign patterns (structure adapted from `[lihfolk]`):

| Pattern | Setup | Judge by |
|---|---|---|
| Measurement | Plays, New Players, small daily budget for 5–7 days, LaunchData tag per test, ideally while recommendations are excluded | A clean funnel read; not ROAS |
| Creative test | Up to 10 creatives; switch off clear losers after enough impressions. To learn which promise brings players who stay, run one short campaign per concept, because LaunchData cannot tell creatives apart | CPP per creative and the D1 of the cohort it brought; low CPP with poor D1 is over-promising |
| Reactivation | Lapsed Players (needs 20,000+), timed to a real update with an event live that day | Resurrected Users view; your own "returned after 30+ days" segment |
| Eligibility | Engagement objective, its own budget, 3–5 days, paused by hand at the 250-play threshold | Audience Reach progress |

Reading lag `[lihfolk]` (rule of thumb): read CPP after 2–3 days, the ad cohort's D1 after 3–4 days, 7-day revenue per user after 9–10 days. Roblox staff say 7–10 days before judging a campaign, and that a pause in the first 24–48 h restarts learning `[official]`: read early, change late.

```lua
--!strict
-- Unexecuted sketch: classify how a player arrived, from LaunchData set on an ad or share link.
-- Whitelist values so analytics field cardinality stays small and nobody can inject strings.
local HttpService = game:GetService("HttpService")

local ALLOWED: { [string]: boolean } = { ads = true, share = true, event = true, creator = true }

local function acquisitionTag(player: Player): string
	local raw: unknown = player:GetJoinData().LaunchData
	if typeof(raw) ~= "string" or #raw == 0 or #raw > 200 then
		return "organic"
	end
	local ok, decoded = pcall(HttpService.JSONDecode, HttpService, raw)
	if not ok or typeof(decoded) ~= "table" then
		return "organic"
	end
	local src: unknown = (decoded :: { [string]: unknown }).src
	if typeof(src) == "string" and ALLOWED[src] then
		return src
	end
	return "organic"
end
-- Log the tag as a custom field on the onboarding funnel; treat any LaunchData perk as public
-- (links get copied): cosmetic or small, once per account, never tradeable.
```

Operating rules: start with Plays + New Players and 3–5 distinct honest creatives; cap the test budget; switch off the worst creatives only after several days of data (toggle the creative; do not pause the campaign); add creatives rather than budget first; never run a creative the first minute does not deliver; run Lapsed campaigns only in update weeks.

Publisher side (earning, not growth): immersive ad units are Roblox-served surfaces, not Blender assets. If used at all, mount them in a Blender-authored frame with collision, keep them out of the FTUE path, and treat rewarded video under the existing rule (fixed reward, opt-in, never a gate).

## 4. Short-form video: TikTok and YouTube Shorts

Evidence grade: `[community]`. No Roblox or TikTok primary data on Roblox-game marketing was found; sources are developer anecdotes and vendor blogs. One DevForum developer reported about 12 million views on a game hashtag from community clips at no cost; another said a few Brazilian YouTubers were the only thing that grew the game (about 1.7K active players). Roblox's own guidance says only: keep social accounts, post regularly, build a community, partner with creators, and use share links `[official]`.

Why it fits: Roblox states that Roblox and YouTube are the top two platforms for many users and that viewers follow creators into games that look fun to watch `[official]`. Short-form reaches 13+ audiences, which is also where the 250 engaged, age-checked 16+ plays come from.

| Format | Shape | Needs from the game |
|---|---|---|
| The climb | Start state → end state in 10–20 s ("Day 1 → Day 100", "$1/s → $9.8M/s") | A visible journey; a big readable number |
| Rare-drop reaction | The reveal plus the real odds on screen | Honest odds UI; a reveal animation worth watching |
| Fail and physics | Ragdolls, near misses, chain reactions | Physics toys; a replay or death cam |
| Challenge | "Can you beat X in 60 seconds?" over a trending sound | A short timed mode; a shareable result screen |
| Update teaser | One new feature, the date, the weekly day | A fixed update day; a real date |
| Dev log | "I modelled every prop in Blender", before and after | The Blender pipeline itself; appeals to older players |
| Comment reply | Answer one viewer question with gameplay | Nothing extra |

Clip structure `[lihfolk]` (rule of thumb): hook in 0–2 s (the most interesting frame, never a logo or title card) → context in 2–6 s (one line of on-screen text saying what the game is) → payoff by 6–15 s (the reveal, the hit, the transformation) → a last frame that loops or says "Play <exact name> on Roblox". 15–30 s is the safe length; longer needs a second payoff. Platform UI covers the bottom and right edge of vertical video: keep text in the middle 70% of the height and off the right 15%.

It works badly when the fun takes ten minutes to arrive (film the payoff, and make the game deliver it fast) or when the first session leaks: video traffic comes in bursts, and a viral clip gives one chance, which a leaky funnel throws away `[lihfolk]`.

Capture `[lihfolk]`, adapted to the house rules. Recorder settings (bitrate, frame rate, file naming), the 2026 free-camera controls, repeatable camera takes and a trailer shot list are in `cutscenes-and-cinematics.md` §16; still-image quality settings are in `icons-thumbnails-and-store-page.md` §8. What belongs here is the capture place and the rules for footage that leaves Roblox:

- Keep a capture copy of the place with the same lighting as live, a hide-UI toggle (a `CaptureMode` attribute every ScreenGui respects is more reliable than disabling guis from outside), free camera (Left Shift + P `[official]`), and debug grants that are labelled capture-only and never enabled in the live place. Outcomes shown must be reachable at the real odds.
- Record landscape at full resolution with the subject in the centre third, then crop 9:16; resize the window tall only for shots that need native vertical.
- Do not show other players' usernames or display names, and never record voice chat: film with team accounts in a private server. Many players are children.
- Music: Roblox's licensed music may be used on Roblox only (Terms of Use §7.1, read 2026-11-11 `[official][VS]`), so it cannot go in a TikTok, YouTube or other off-platform video. Use music you own or have licensed for social video (`references/audio-sfx-music.md`).
- Answer each platform's "made for kids" question honestly even though it reduces reach; platform minimum ages are commonly 13, so an adult runs the accounts.

Hooks and craft `[community][house]`:

- The payoff frame is in the first 1–3 seconds; overlay text of six words or fewer; real gameplay only.
- Say and show the exact game name; viewers search for it, and exact-name search arrivals of new or reactivated users can pay Audience Expansion `[official]`.
- End on a question or an unfinished climb to earn comments.
- Vertical 9:16, 10–25 s; one idea per clip; cross-post the same file to TikTok, Shorts and Reels.
- Cadence: no Roblox-specific evidence. General marketing guidance clusters around 3–5 posts a week and steady posting over bursts. `[house]` plan: 3 per week per platform, daily in launch and update weeks; expect most clips to do little and a few to carry the results.
- Put the per-channel share link in the profile, not a raw place URL, so the funnel is attributable.
- Never: bought views or bots, "free Robux" or giveaway hooks, footage the game cannot produce.

In-game features that generate clips (build these into the game, they are free marketing):

| Feature | Detail |
|---|---|
| Creator cam / hide-UI toggle | One button hides the HUD and offers; Brookhaven's Creator Cam is Roblox's own example `[official]` |
| Free-cam photo mode | Orbit camera, field-of-view slider, pause for solo sessions |
| Reveal moments | 2–4 s rare-drop or rebirth sequence with a full-screen readable result and the real odds |
| Server-wide callouts | "Player rolled 1 in 50,000" banner; makes other players clip it too |
| Before/after frame | End-of-session card: where you started, where you are now |
| Readable numbers | Giant in-world counters in the game's own unit, legible in a 9:16 crop |
| Short replayable beats | A complete, funny or tense moment inside 15 s |
| Streamer mode | Hide other players' names and chat for creators who record |
| Private servers and a creator code | Lets creators record without crowds; ties to §5 and §8 |

## 5. Creators and influencers

- Find them by search: creators already covering the genre, 1–50K subscribers first. `[community]` reports say small creators are cheaper and still build a following, but hard to find; large ones can cost more than equivalent ad spend.
- Rates: only single-source, unverified estimates were found ($500–5,000 flat per video in one write-up; $2,000–15,000 for YouTube and $500–3,000 for TikTok in another, both from the same vendor). Treat any quote as negotiable and judge it by expected plays × value per player (§3).
- Offer before money: early access to the update build, a private server, a creator code that grants a cosmetic to viewers, creator cam, a ready list of clip moments, a named in-game item.
- Structure paid deals as deliverables plus a share link: one long-form or 3 shorts, exact game name spoken and shown, link in description or profile, a posting window around update day.
- Disclose paid promotion. Roblox's advertising standards require ads to be clearly disclosed, and FTC-style disclosure applies off-platform `[official]` (advertising standards; the former affiliate programme required an FTC disclosure). Anything of value counts (Robux, items, early access). Give every sponsored creator a written brief `[lihfolk]`: say "paid" out loud early and show it on screen (a 2023 US children's-advertising review pressed for wording children understand; hashtags at the end of a description are not enough), use the platform's paid-promotion label, make no unverifiable claims, send no child to an external site or a giveaway that needs personal data, and keep a record of payment and disclosure.
- Avoid middlemen who ask for Robux up front to "get a YouTuber to play"; `[community]` threads flag this as a common scam shape.
- Live "admin" events with creators: the August 2025 cross-game admin event between two top simulators coincided with the platform's 47.4M concurrent record `[community]` (press). The repeatable parts are a dated window, limited drops handed out live, and creators on both sides. Keep it honest: real dates, real stock, no false scarcity; critics note that constant drop events make progression feel disposable.
- Measure each creator with their own share link: users with qualified plays, 7-day playtime, D7, 30-day revenue per user `[official]`.

## 6. Community: Roblox group and Discord

- Roblox group first. Roblox calls groups the best way to connect with and inform a community `[official]`; the group sits on the game details page, events can be featured on its About tab, and membership is the one social action the server can verify (`Player:IsInGroupAsync`). Reward joining as a bonus only, after the first win, per the social-rewards rule in liveops-quests-retention.md.
- Membership APIs `[official][VS]`: `Player:IsInGroup` is superseded by `Player:IsInGroupAsync` (same per-session caching), `Player:GetRankInGroupAsync` by `GroupService:GetRolesInGroupAsync`, and `GroupService:PromptJoinAsync(groupId)` shows a native join prompt on the client and returns the membership status. Check on the server, fail closed, and offer a "check again" path after a join (flow in liveops-quests-retention.md).
- Split the groups once there is staff and revenue `[lihfolk]`: an owning group that holds the games, funds and Team Create permissions, and a separate fan community for players, announcements and perks, so a compromised community moderator cannot touch games or payouts. Keep rank numbers stable and roles few. Detail in `references/community-moderation-safety.md` and `references/team-business-legal.md`.
- Rewarding likes and favourites `[VS]`: no written rule against it was found in the Community Standards or the creator docs (checked 2026-11-11), and no staff statement either way. One creator has reported moderation whose notice listed "artificially inflating experience statistics" (DevForum /t/4776239, Aug 2026: a game with about 200M visits put under review, appeal denied without naming the cause; the creator's own guess was an in-game reward for joining an off-platform server) `[community]`. So rewards for off-platform actions (joining a Discord, following an account) carry their own risk as well as being unverifiable: do not offer them. Group join (verified) and friend join are the safe default.
- Conflict: LihFolk advises against rewarding likes, favourites or social posts at all and prompts for a group join from 90 s in, up to four times a session. This skill keeps the owner's standing rule in SKILL.md: social rewards are bonuses only, asked after the first win; like and favourite thanks are small, honour-based, one-time; and every such card goes through the offer gate (after the first win and the 600 s grace, at most 3 cards a session).
- Discord second, for the 16+ core: code drops, update countdowns, bug reports, suggestion votes, playtest recruiting, creator outreach. Discord's own terms set a minimum age of 13.
- Links `[official][VS]`: up to three social links on the game details page (Facebook, Twitter/X, YouTube, Twitch, Discord, Guilded, Roblox community), only if the owner is age-verified 16+, and visible only to age-verified 16+ users. Social links may not be shared inside the game. Allowed in-game copy: "Join our community server. Links on our game's page." Not allowed: any URL, invite code, handle or email in-game.
- Conflict: older community practice gated in-game Discord links behind `PolicyService` (`AllowedExternalLinkReferences`). The current docs prohibit in-game social links outright; follow the docs.
- Never ask players for personal data, never move minors to private off-platform contact, never run under-13-facing promotion that depends on leaving Roblox.
- Cadence `[house]`: one group post per update, one Discord announcement per update plus a mid-week teaser, a pinned known-issues list, a monthly "what we changed because you asked".

## 7. Update announcements, events and launch timing

| Tool | Limits and use `[official][VS]` |
|---|---|
| Update announcement | 60 characters, at most one every 3 days, sent to players who opted in; be specific ("New Ice Caves world + 3 pets"), never "bug fixes" |
| Experience Events | Dated start and end, up to 5 thumbnails (a unique one lifts engagement), "Notify Me"; the Trending Events sort needs 1,000+ RSVPs and a start inside the last 7 days; feature the event on the group page; log every weekly update as an event |
| Off-Platform Featuring | Time-limited events or significant updates; submit at least 7 days before start |
| Experience notifications | Opted-in 13+ users, one per user per day, personal and actionable |
| Promotional text (beta) | Short secondary line in publish settings; use for the live update, never for giveaways |
| Title tag | `[UPD]`, `[2X EVENT]` rotated with real events (market-scan rule 9 and 12); do not rename the base title, it breaks search for the old name `[official]` |
| Thumbnails | New set with each major update, 2–5 active including the current winner, left alone until the next update `[official]`; refresh patterns and the making-of in `icons-thumbnails-and-store-page.md` §14 and §8 |

Timing (vault, snapshot 2026-11-07): launch or update on or just before Saturday; best windows 15 Dec–5 Jan, 10–30 Jun, Halloween for themed games; avoid late Aug–Sep. A new game needs lead time to clear the 250-play gate before a seasonal window (for example ship around 10 Dec for the holiday peak). Announce the fixed weekly update day and keep it.

Reading an update `[lihfolk]`: the curve is tease (T-7 to T0) → spike (T0 to T+2, usually peaking on the first weekend) → decay (to about T+14) → new baseline. The baseline is the result. Spike and back to the old baseline: content consumed, no lasting goal. Small spike and a higher baseline: a system that keeps giving (a collection, a progression tier). Baseline below the old one: something broke or annoyed existing players. No spike: nobody knew, or the update was invisible. Annotate every update on the charts or a school holiday will be read as a success.

Players consume content far faster than a team builds it, so mix cheap rhythms with expensive ones. A sustainable default for one to four people `[lihfolk]`: weekly rotation from data only (shop, quests); a boost or community-goal event most weekends (a Config change plus an Experience Event); a content update every 2–3 weeks carrying one new goal for existing players and one improvement for new players; a new system every 2–3 months. If every update needs overtime the cadence is too fast. This sits beside, not against, the vault's finding that weekly fixed-day updates mark the hits: the weekly beat can be a rotation or event rather than new assets.

The first two weeks of a launch `[lihfolk]`, compressed: day 0 changes are bug fixes only, with someone on errors, someone on the funnel, someone on community reports; days 1–3 watch the leak, not the player count (one hotfix for crashes and stuck states, one by day 3–5 for the biggest funnel drop); days 5–7 pick a branch: healthy (ship the first content drop, consider ads), leaky start (keep fixing onboarding, buy nothing, add no content), weak promise (new thumbnail concepts, not variants), no pull (competitor teardown before spending more); days 7–14 first content aimed at existing players, paired with an event, one new thumbnail and one update announcement.

Conflict: LihFolk says to publish on a weekday morning, not a Friday night, so the team is awake for the first 12 hours; the vault says to launch on or just before Saturday for the traffic peak. Both hold if "publish" and "go live" are separated: publish the build early in the week with content gated by server time or a Config, then open it (event start, announcement, thumbnails) into the weekend.

Sequence for an update week `[house]`: T-3 teaser clip and Discord post → T-1 Experience Event live with Notify Me → T0 publish off-peak, restart outdated servers, update announcement, title tag, new thumbnails → T+1 creator videos and a second clip → T+3 read PTR, bounce and D1 for the update cohort.

## 8. Codes

`[community]` practice in most simulator and tower-defence hits: time-limited redeem codes released on update day through the description, the group, Discord and creators. Code-list sites and creators republish them for free, and returning players check for codes first. Roblox's experimental description guidance lists "codes" as acceptable additional information in the lower part of a description `[official]`.

Rules:

- Rewards are small boosts or cosmetics that exist anyway in the free economy; never Robux, never anything implying monetary value, never the only route to content.
- Codes go off-platform and, at most, as a plain "Code: NAME" line under additional information at the bottom of the description (Roblox's own template). Keep codes and words such as "FREE" or "giveaway" out of the title, thumbnails and description hook: metadata that leads with giveaways loses exposure `[official]`, and SKILL.md forbids giveaway wording in all three.
- Real expiry dates; no "last chance" countdowns that restart.
- Server-side only: validate, rate-limit, redeem once per account, store the redeemed set in the profile, define codes in Configs so they can be added without a publish.
- Log `CodeRedeemed` with the code as a custom field; it is a free attribution signal per channel when each channel gets its own code.

```lua
--!strict
-- Unexecuted sketch: server-side code redemption. Call from a guarded remote handler.
type CodeDef = { reward: string, amount: number, expiresAt: number } -- expiresAt = Unix seconds
type Profile = { Data: { RedeemedCodes: { [string]: boolean } } }

local function redeemCode(profile: Profile, codes: { [string]: CodeDef }, raw: unknown, now: number): (boolean, string)
	if typeof(raw) ~= "string" or #raw > 24 then
		return false, "Invalid"
	end
	local key = string.upper(raw)
	local def = codes[key]
	if def == nil or now >= def.expiresAt then
		return false, "Expired or unknown"
	end
	if profile.Data.RedeemedCodes[key] then
		return false, "Already redeemed"
	end
	profile.Data.RedeemedCodes[key] = true -- mark first, then grant (grant function not shown)
	return true, def.reward
end
```

## 9. Cross-promotion, search and localisation

Search queries `[lihfolk]` (method; the search facts are in analytics-and-discovery.md): write 15–30 queries a player, friend or parent might type (the genre in plain words, the fantasy, the verb, the setting, "game to play with friends"). Make the first two lines of the description say the top three or four of them in natural sentences: line one is verb + subject + fantasy + social hook, line two is the freshness line that changes each update. Synonyms go in sentences, not lists; never use another game's name. Test by searching each query from a fresh account, record the position, change one thing, re-check after a few days, and judge by search-sourced plays in Acquisition rather than by one query's rank.

Cross-promotion:

- Own portfolio: a Blender-built "more from us" board with a prompt that teleports to a sibling game; teleport arrivals show as their own acquisition source `[official]`. Never interrupt play with it and never show it in the first session.
- Cross-game pass sales have been disabled since 30 May 2026 (monetization-and-policy.md), so cross-promote with teleports, shared events and matching cosmetics, not shared products.
- Collaboration events with a non-competing game of similar size: swap a cosmetic, share an event date, post from both groups.
- Do not clone a partner's title, art or place file: near-duplicates lose exposure `[official]`.

Localisation `[official][VS]`:

- Turn on Automatic Text Capture and "Use Translated Content", then enable languages for both Experience Information (name, description) and Experience Strings and Products. Quotas are per character per language (initial, then monthly).
- Capture misses images with embedded text, default leaderboards and chat, tools, and badge or pass names pulled from the platform. Use icon-led UI and `AutoLocalize`; keep text out of images.
- Search returns a game when the query matches any of its translated titles (staff statement, search summary), and Roblox's own experiment on translated names and descriptions reported higher click-through and plays (search summary).
- Use the Country and Language breakdowns in Creator Analytics to pick languages: translate where players already arrive but retain worse.
- Lock only translations a human reviewed; a locked entry stops receiving safety-related auto-updates.
- Pick event themes that travel; holidays are not universal.

## 10. What breaks the rules

| Do not | Rule |
|---|---|
| Lead the title, thumbnail or description with Robux, giveaways, "free UGC", or "like for rewards" | Reduced exposure for giveaway-led metadata `[official]`; SKILL.md never-do |
| Promise in a tile, video or ad what the first minute does not show | Mismatched metadata is not recommended and ranks lower in search `[official]` |
| Stuff or repeat keywords, or pile on emoji, in name or description | "May result in demotion" `[official]` |
| Put URLs, invite codes, handles or emails in-game, or steer under-13s off-platform | Social links live only on the details page and are 16+ gated `[official]` |
| Gate progress or content on group join, likes, favourites or invites | SKILL.md social-rewards rule: bonus only, after the first win |
| Run giveaways of Robux or items with monetary value, or any chance-based paid entry | Giveaway metadata penalty; paid random item and gambling rules (monetization-and-policy.md) |
| Add narration, lyrics, real-life footage, enhanced graphics or "50% off" text to a video thumbnail | Video policy; rejects count against the 3-per-month quota `[official]` |
| Use bots, alt accounts or incentivised installs to inflate plays or Creator Rewards | Creator Rewards and ad-fraud rules `[official]` |
| Leave paid creator content undisclosed | Advertising standards `[official]` |
| Use AI-generated or non-game art as an ad creative | House rule 1 and the accuracy rule |
| Fake scarcity or restarting countdowns in event and offer marketing | House rule 3 |

## 11. Rescuing a weak launch

Diagnose by funnel stage, not by CCU (stages and order in `references/audit-existing-game.md` §4). Three things are specific to a game that already launched small `[lihfolk]`:

- **Get enough traffic to measure.** A few hundred attributed first sessions before any conclusion; do not tune on ten sessions and do not buy large campaigns into an unmeasured funnel.
- **Fix the empty-server problem.** Thirty players across six servers feels dead. Lower max players for the start place while CCU is low (about 8–12 for social and co-op games, raised later), choose the server-fill setting that fills servers rather than reserving slots (experience settings `[VS]`), make the loop playable with one to three players (bots, solo or two-player mode; "1/8 players" waiting screens are where launches die), merge lobby and mode places into one until CCU supports the split, and make other players visible across servers (a global feed, a shared event, a cross-server leaderboard).
- **Decide: fix, reposition or move on.** Play-through poor but the first session is good on test traffic: reposition (icon, thumbnails, title around the moment players enjoy). Play-through fine, first session poor: rebuild the first session. First session good, nobody returns: add a return reason. Everything mediocre after two or three fix cycles: archive and reuse the systems.

A relaunch is a change of promise plus a change of product, announced honestly: do it when test traffic shows a measurable first-session improvement, into a weekend or school holiday, with an update that fits one line. Never: bought visits or favourites, misleading tiles, changing everything at once, a silent rebrand, or an `[UPDATE]` tag with no update.

## Level-up: symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Ads deliver plays, no retained players | FTUE leak, or the wrong objective and audience | Read the Recent and Resurrected views; fix the funnel; switch to Plays + New |
| Organic impressions dip during a campaign | Ad-acquired users no longer see the organic tile | Expected; judge total new users and cohort value |
| Clip goes viral, D1 falls | Tourists dilute the cohort | Normal; make the clipped moment reachable in the first 5 minutes |
| Stuck in the 16+ trial | Audience is young, few age-checked 16+ players | Engagement-objective campaign, dev-log content, Discord and creator outreach to older players |
| Reduced-exposure banner after a title change | Giveaway or mismatch wording | Remove it, restore accurate metadata, file "Discovery Content Quality" if wrong |
| Creators ignore the game | Nothing clip-worthy, no creator tooling | Build §4 features; send a build, a private server and a code |
| Discord grows, DAU flat | Links are 16+ gated; announcements live off-platform only | Mirror every post to events, update announcements and the group |
| Many players from one country, weak retention there | Untranslated text | Enable that language; fix images with text |
| Update days no longer spike | Announcement too vague or too frequent; no event | One specific 60-character announcement; an Experience Event with Notify Me |
| Update spikes, then the baseline is lower than before | The update broke something or removed value | Error report and economy dashboards by place version; revert or compensate |
| Some players online but every server looks empty | Server size too large for current CCU; too many places | §11 server-fill fixes |
| ROAS looks great in Ads Manager, poor in your own data | Plays counted, not unique players | Tag joins with LaunchData; compute per unique user |
| Thumbnail test "winner" changes weekly | Novelty effect or too few impressions | Run 10–14 days; sample-size rule in analytics-and-discovery.md |

## Review gate

- [ ] Readiness gate (§1) passes with numbers written down, or the spend is labelled a measurement buy with a cap.
- [ ] Value per new player by source is known; max cost per play computed; stop-loss date set.
- [ ] One share link per channel and per creator; Acquisition funnel checked weekly.
- [ ] Every creative, clip and thumbnail is real footage of the Blender-built game and matches the first minute.
- [ ] No giveaway, Robux or "free" wording in title, thumbnails or description lead; codes sit in the description body only.
- [ ] No in-game URLs, invite codes or handles; social links configured on the details page only.
- [ ] Social rewards are bonuses, shown after the first win, group join verified server-side.
- [ ] Update week has an event, a specific announcement, a clip, and a fixed weekly day.
- [ ] Clip features (creator cam, reveal moments, readable numbers) exist before paying any creator.
- [ ] Languages enabled match the Country and Language breakdown.
- [ ] Paid creator content is disclosed, with a written brief ("paid" spoken and on screen).
- [ ] Soft launch run with recommendations excluded; the four bars read before opening.
- [ ] Ad and share-link joins tagged through LaunchData; cohort revenue computed per unique user.
- [ ] Publish and go-live are separate steps; server size fits current CCU.
- [ ] Footage shows no other players' names and uses music licensed for off-platform video.
- [ ] `[VS]` facts (formats, costs, link policy, limits) re-checked at create.roblox.com/docs.

## Sources

Accessed 2026-11-10; Ads Manager, social links, events and discovery facts re-read on 2026-11-11 against the `Roblox/creator-docs` GitHub mirror (commit 7cbffff, 2026-11-10).

- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/ads-manager.md, search-ads.md, advertise.md, advertise-on-roblox.md, comply-with-advertising-standards.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/cloud/guides/advertising.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/monetization/immersive-ads.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/promotion/social-media-links.md, share-links.md, experience-events.md, experience-notifications.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/analytics/acquisition.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/discovery.md, discovery-faq.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/publishing/publish-games-and-places.md, thumbnails.md, descriptions.md, kids-and-select.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/production/localization/automatic-translations.md (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/creator-programs/standout-games.md, creator-affiliate.md (read)
- https://devforum.roblox.com/t/ads-for-creators-rdc-recap-and-what%E2%80%99s-next/3929106 (read)
- https://devforum.roblox.com/t/4909790 Ads Manager RDC recap, 2 Oct 2026; /t/4623762 Ads Manager updates, 7 May 2026 (read)
- https://devforum.roblox.com/t/leveling-up-ads-manager-with-new-features/3587640 (read), /t/roblox-staff-streams-learn-more-about-the-new-ads-manager/3676241 (search summary)
- https://devforum.roblox.com/t/urgent-new-ads-manager-is-delivering-significantly-worse-results-x30-times-worse/3801409 (read)
- https://rowatcher.com/news/roblox-ads-in-2026-the-break-even-math-small-devs-ignore (search summary; third-party)
- https://clipclip.io/guides/get-more-players, https://bloxg.com/guides/roblox-tiktok-marketing (search summaries; vendor content)
- https://rolearn.dev/guidance/roblox-tiktok-content-strategy-viral, https://rolearn.dev/trend-reports/roblox-youtube-tiktok-content-trends-2026 (search summaries; vendor content)
- https://devforum.roblox.com/t/4776239 (read 2026-11-11: creator's report of moderation citing inflated experience statistics)
- https://devforum.roblox.com/t/paying-a-youtuber-or-tiktoker-to-promote-my-game/1045620, /t/how-to-market-your-game/1852434, /t/how-would-i-be-able-to-gain-the-attentionfind-small-social-media-creators-to-boost-my-game/3310038 (search summaries)
- https://devforum.roblox.com/t/level-up-designing-for-youtube-engagement-roundtable-ft-kreekcraft-and-wonder-works-studio/1781335 (search summary; agenda only, takeaways not retrievable)
- https://devforum.roblox.com/t/age-checks-to-access-chat-studio-team-create-and-links-on-roblox/4079702, https://about.roblox.com/newsroom/2025/11/roblox-requires-age-checks-limits-minor-and-adult-chat (search summaries)
- https://www.tubefilter.com/2025/08/25/roblox-grow-garden-steal-brainrot-admin-war-record/amp/, https://www.pcgamer.com/games/sim/roblox-had-more-concurrent-players-than-the-entirety-of-steam-over-the-weekend-as-it-reeled-in-over-45-million-users (search summaries)
- https://beebom.com/admin-abuse-might-save-dying-roblox-games-but-hurts-them-in-the-long-run (search summary; opinion)
- https://devforum.roblox.com/t/introducing-exact-match-search-for-experiences/2425969, /t/upcoming-icon-thumbnail-translation-experiment/3105942 (search summaries)
- Vault: `references/market-scan-2026-11.md`, `references/knowledge-base.md` §3.6, §3.10 (read)
- https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/engine/classes/Player.yaml, GroupService.yaml; content/en-us/creator-rewards.md (read)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `27 Marketing and Growth/` notes "Sponsored Ads and Campaign Math", "Short-Form Video Marketing", "Launch Strategy - The First Two Weeks", "Rescuing a Weak Launch - Empty Servers, Low CCU and Relaunch Tactics", "Update Cadence and Hype Cycles", "Marketing to Kids and Teens - Age Rules and Paid-Promo Disclosure", "Roblox Communities as Your On-Platform Hub", "Experience Description and Search Keywords", "Competitor Analysis Method"; `11 Monetization Publishing and Live Ops/Community Building.md`, `Publishing an Experience.md`; `LihFolk Vault V2/SYMPTOMS.md` (read). Adapted in our own words; platform facts re-checked against creator-docs where marked `[official]`.
