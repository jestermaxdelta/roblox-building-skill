# Community, moderation and safety

How to keep a Roblox game's players safe and its community healthy: child safety and age-appropriate design, the maturity label, chat and text rules, in-game reporting and moderation tools, ban policy, staff and admin tools, exploiters and leaks, community spaces, feedback pipelines, backlash, creators, a crisis playbook and privacy. Open it before adding any feature where one player can reach another (chat, trading, building, voice, parties), when setting up a group, Discord or moderator team, and when something goes wrong in a live game. Platform rules here changed several times in 2025–2026; every `[VS]` item must be re-checked at create.roblox.com/docs. The privacy section touches law: **this is not legal advice**; read the current Roblox Terms of Use and Community Standards and ask a qualified professional about privacy law, contracts with moderators and anything involving minors. Tags: `[official]` Roblox docs, `[community]` forum, press or vendor practice, `[VS]` version-sensitive, `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0).

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Answer the Maturity & Compliance Questionnaire truthfully for the most extreme content. (2) Use default `TextChatService` chat untouched. (3) Filter every player-written string and limit public text edits to one per minute per player. (4) Never ask players for personal information or send them off-platform. (5) Publish short game rules; ban only with evidence | Custom chat UI, voice routing, moderator teams, Discord |
| Intermediate | Rule-report flow with fixed categories and server-attached evidence; case ids, a ban ladder and an appeal route; server-checked staff powers with an action log; weekly look at Safety and Feedback dashboards; group roles on least privilege; RTBF deletion templates; an incident runbook with kill switches | Voice access lists, statistical alt handling |
| Expert | Migration to platform-integrated chat before May 2027; chat-compatible lobby grouping; appeal overturn rate and report-rate benchmarks tracked per release; per-crisis drills; measured Discord value; audited data inventory including external services | — |

## Contents

1. First duty: child safety · 2. Age framework in 2026 · 3. Maturity label and the design choices that move it · 4. Chat and text rules · 5. Voice · 6. Reports and in-game moderation · 7. Ban policy · 8. Staff, admin tools and their abuse · 9. Exploiters and leaks · 10. Community spaces · 11. Moderators · 12. Feedback and bug reports · 13. Drama and update backlash · 14. Creators · 15. Crisis playbook · 16. Privacy and data · 17. Level-up table · 18. Conflicts · Review gate · Sources

## 1. First duty: child safety

A large share of Roblox players are children, so every social feature is designed for the worst user of it first. Who acts on what `[official][lihfolk]`:

| Problem | Who acts | The developer's job |
|---|---|---|
| Grooming or any risk to a child, sexual content, threats of violence, self-harm | Roblox's own report flow | Keep that report one tap away, take the reported player out of the server, and **do not run your own investigation** |
| Harassment, hate, bullying in chat or voice | Roblox, plus you inside your game | Game-level mute or kick; tell the victim to report and block |
| Scams for Robux or accounts | Roblox | No free text in trades; "we never ask for your password or items" messaging |
| Breaking your game's rules (griefing, exploiting, teaming) | You | Your report flow, enforcement and appeals. Roblox does not mediate these unless your rules or enforcement themselves break the Community Standards `[official]` |
| Unsafe things your game displays (unfiltered text, offensive builds) | You; Roblox may take the game down | Filter and design so it cannot happen |

Never build:

- Any way for players to converse outside `TextChatService` (§4), or any private channel between strangers that the platform would not allow.
- A feature whose purpose is to move a conversation off-platform: "type your Discord", free-text trade notes, links, handles or invite codes in game text. Moving a child to a less moderated space is the common pattern in grooming cases `[lihfolk]`.
- Requests for real names, ages, photos, schools, locations, emails or phone numbers, in game or in any community space.
- Primarily private spaces (bedrooms, bathrooms, closets) in a game open to under-18s; add bounding-box limits on beds and similar props `[official]`.
- A moderator process where a child reports abuse to your volunteer and the volunteer handles it privately. A volunteer's whole reply is three things: thanks, a pointer to Roblox's Report button for that player, and a statement that the player is being removed from the server now `[lihfolk]`.
- Anything that infers a player's age (from voice eligibility, `PolicyService` flags, typing style) or pressures players to verify their age.

## 2. Age framework in 2026 `[VS]`

| Fact | Detail |
|---|---|
| Account tiers `[official]` | Roblox Kids (5–8): Minimal or Mild games that pass evaluation; chat off by default. Roblox Select (9–15): up to Moderate; chat off until age-checked, then introduced gradually. Roblox (age-checked 16+): everything except Restricted |
| Age checks for chat | Required worldwide since January 2026 (facial age estimation, or ID). Six groups: under 9, 9–12, 13–15, 16–17, 18–20, 21+; by default a player chats with their own group and the groups directly above and below `[community: Roblox newsroom via search]` |
| Effect on games | Roblox told developers to expect a drop in chat usage and said it "may impact gameplay if chat is a core part of your experience" `[community: DevForum announcement via search]`. No published figure for the size of the drop was found |
| What code can know | `TextChatService:CanUserChatAsync`, `CanUsersChatAsync`, `CanUsersDirectChatAsync` and `GetChatGroupsAsync(players)` (matching group id = can chat) `[official]`. Never an age |
| Reaching under-16s `[official]` | Owner in good standing, verified (facial estimation under 18, government ID at 18+), 2-step verification, a Minimal/Mild/Moderate label, and either a Plus or Premium subscription held 2+ months or a one-time refundable per-game fee. Then evaluation: a trial with age-checked 16+ users, a safety review, and 250 unique plays by highly engaged age-checked users within 60 days. Expedited review: 50,000 R$ refundable fee |
| Parents `[official]` | Linked parents can approve specific games ("Approved Experience", not for Restricted), see friends, screen time and spending, and set who a child may collaborate with in Studio |
| Team side | Team Create with other people requires an age check and, by default, compatible age groups (see `team-business-legal.md`) |

Design consequences `[house]`: assume many players in any server cannot see each other's chat. Core loops must work without chat: pings, emotes, ready checks, Quick Words. For chat-dependent lobbies, group players with `GetChatGroupsAsync` instead of guessing. Discovery consequences of the 16+ trial are in `growth-and-marketing.md`.

## 3. Maturity label and the design choices that move it `[official][VS]`

Labels: Minimal and Mild (Kids, Select, 16+), Moderate (Select and 16+), Content May Vary (age-checked 16+ only; what you get if you answer only the first question), Restricted (ID-verified 18+; unplayable in Korea, Saudi Arabia and Türkiye; can never be lowered). A game with no maturity information is unplayable for everyone. Answer for the most extreme content a player can meet, and re-submit whenever an update changes an answer; repeated wrong answers put the game and account at risk. Resubmitting pauses ad eligibility (`monetization-and-policy.md`).

| Design choice | Effect on audience |
|---|---|
| Violence implied only (heard, off-screen) | Already meets the Mild criterion |
| Consequence of violence shown unrealistically vs realistically, even once | Unrealistic → Mild; any realistic moment → Moderate or stronger. Frequency counts: one area with repeated violence makes the whole game "Repeated" |
| Blood: unrealistic and light vs realistic or heavy | The second pushes toward Moderate or Restricted |
| Scary elements: mild vs moderate (visible organs, open wounds, bleeding eyes) | Horror art direction decides the label; stylise to stay in Mild |
| Primary activity is talking or hanging out ("vibe" games, sad rooms) | Social hangout: age-checked 16+ only, regardless of other answers. Roleplay with roles and props central to play is not a hangout; a title or description that sells "hangout" can make it one |
| Hangout with private spaces (bedroom, bathroom stall, small tent) | ID-verified 18+ |
| Freehand drawing, spray paint, pixel canvases, even temporary or per-round, visible to others | Free-form user creation: 16+. Building with pre-made 3D assets or anything moderated before display does **not** count |
| Primary theme is a current polarising social, political or religious issue | 16+, and not recommended or discoverable unless age-verified |
| Romantic themes (even a quick kiss, or in the title), strong language, strong violence, heavy realistic blood | ID-verified 18+ |
| Any depiction, reference or use of alcohol, including characters drinking at a bar | ID-verified 18+. A fantasy tavern serving ale moves the whole game; serve something else |
| Gambling | Playable gambling, including simulated, is not allowed at all. A casino that players cannot bet in must still be declared |
| Paid random items, paid item trading | Must be declared; gate with `PolicyService` (`monetization-and-policy.md`) |
| Players share media, endless feeds, autoplay; generative-AI interaction (cross-session memory or "main purpose" = extended) | Declared in their own questionnaire sections |
| Nightclub, bar or dance-club setting as the main place | Restrict to 18+ `[official]` (safety guide) |

Parents can bypass most content limits for their child but not the 16+ limit on hangouts and free-form creation. Decide the target audience at concept time: a drawing minigame or a "chill hangout" lobby can remove the whole under-16 audience from an otherwise Mild game.

## 4. Chat and text rules `[official][VS]`

**Definition.** Chat is any feature that lets players hold a back-and-forth conversation in under 60 seconds. It must go through `TextChatService`, which applies privacy settings, age-based limits, filtering and abuse reporting. A game that lets players converse any other way can be taken down; appeals after a fix typically take one to two weeks.

| Text surface | Rule |
|---|---|
| Chat window, bubbles, team and direct messages, custom chat UIs, radios, phones, admin tools that let players or admins message each other | `TextChatService` only |
| Direct or private channels | Check `CanUsersDirectChatAsync`, mark the channel with `TextChannel:SetDirectChatRequester()` |
| Player-editable text others can see (signs, pet names, plates, bulletin boards, comments) | Filter with `TextService`, **and** rate-limit to at most one submission per minute per player. Comments may not have replies: replies are a conversation |
| Preset phrases, chat wheels | Quick Words (Creator Hub ⟩ Configure ⟩ Chat): up to three custom categories of three to ten phrases, written in English, auto-translated, reviewed before going live. Required for player-usable presets by May 2027 |
| Developer-set text (menus, status lines, one-way announcements, moderation logs) | No filtering needed if players cannot alter or reply. Admin commands that let players reply, or admins chat with each other, count as chat |

**Platform-integrated chat.** Opt-in now through `TextChatService.PlatformIntegratedChat = Enabled` (Studio only); required for all games from May 2027. The vault and press report automatic opt-in with an opt-out from February 2027 `[lihfolk][community]`. When enabled:

- Roblox renders all chat, in the default window or in a `TextChannelWindow` whose `Target` is a `TextChannel`. Drawing messages in a custom UI is no longer possible.
- `TextChatMessage.Text` and `.Translation` return `""` with a warning; `PrefixText` is unsupported; `TextChannel:SendAsync` presets move to Quick Words; `OnIncomingMessage` and `Player.Chatted` no longer yield text. Chat-triggered commands must be `TextChatCommand`s. No API returns message content.
- Moderators with the group permission can view chat read-only (§11).

What to do today `[house]`, following `[lihfolk]`:

- Build nothing new that reads message text: chat logs, "say the word" events, keyword triggers, custom profanity counters.
- Move admin and gameplay commands to `TextChatCommand`; treat `unfilteredText` as input to parse, never to store or broadcast.
- Keep chat-tag data in attributes with rendering in one small client module that can be deleted when native role badges ship. If a pass sells a chat tag, word it "where supported" and include a non-chat perk, so nobody pays for something that silently stops.
- Each callback (`OnIncomingMessage`, `OnBubbleAdded`, `ShouldDeliverCallback`) is a single slot owned by one module and must not yield.
- Delivery rules may only narrow (proximity, team, dead-cannot-talk-to-living) through the server-side `TextChannel.ShouldDeliverCallback`; game mutes use `TextSource.CanSend = false`.
- Test the game with the setting enabled before the deadline.

**Filtering edge cases** `[lihfolk]`: filter the final displayed string (filtering "free" and "robux" separately then joining defeats the filter); do not offer several adjacent short fields that work as one message; letter-block building spells anything, so restrict letter pieces in public areas; on a filter error show nothing; leaderboards and overhead names are display surfaces too; never put player text into a system message unfiltered. The filter sketch is in `ui-input-crossplatform.md`; add the limiter:

```lua
--!strict
-- Unexecuted sketch (server): one public text edit per player per minute, checked before filtering.
local COOLDOWN = 60
local lastEdit: { [number]: number } = {} -- keyed by UserId; not cleared on leave, so a rejoin does not reset it

local function mayEditPublicText(player: Player): (boolean, number)
	local now = os.clock()
	local last = lastEdit[player.UserId]
	if last ~= nil and now - last < COOLDOWN then
		return false, math.ceil(COOLDOWN - (now - last)) -- seconds left, for a clear error message
	end
	lastEdit[player.UserId] = now
	return true, 0
end
```

## 5. Voice `[official][VS]`

- Available to age-verified 13+ users in supported countries (ID verification elsewhere); on by default for eligible users in new places; **only in places with a maximum of 100 players**. Disable per place with `VoiceChatService.EnableDefaultVoice = false`.
- Roblox decides who can speak and hear. Routing through the Audio API (`UseAudioApi`, each player's `AudioDeviceInput`, `SetUserIdAccessList` for team voice) may only restrict; refresh lists on every join, leave and team change `[lihfolk]`.
- You cannot record or log voice. Evidence for a voice complaint is timestamps, who was nearby and other reports: enough for a kick, rarely a ban; serious cases go to the platform report.
- Should the game have voice `[lihfolk]`? Co-op horror or heist: proximity, yes. Competitive teams: team-only, optional. Simulators, tycoons, games for Kids and Select: no value and extra moderation exposure. Never required, never rewarded ("speak to earn" produces mic spam), no map-wide radio for everyone, no lockable voice booths in an under-18 game, no home-made "mute for everyone" button.
- Fairness check: compare win rate by share of the team with voice active; if the gap is large, strengthen pings and Quick Words.

## 6. Reports and in-game moderation

**Safety dashboard** (Creator Hub ⟩ Safety ⟩ Overview) `[official]`: abuse-report submitters per 1,000 playtime hours (shown at 1,000+ daily playtime hours), reports per category, filter by channel (Avatar, Chat, Voice, Experience, Audio), and an automatic insight above the 90th-percentile benchmark. Watch the trend rather than the absolute level: when reports jump in the same week a feature ships, suspect that feature. "Romance or sexual" rising is the docs' own cue to review avatar editors and chat. Below the threshold, count your own reports.

**Rule-report flow** `[lihfolk]`:

- Label it "Report rule-breaking in this game" and point to the Roblox report for safety issues. Pair it with Block, mute and "change server": a report does nothing for the next five minutes, blocking does.
- **No free-text box**: it collects personal data and becomes a harassment tool. Fixed categories only.
- The client sends target and category; the **server attaches the context** (positions, recent damage events, trade ids, build id, place version).
- Rate-limit per reporter and cap per target per server. Treat a report as a signal, never a verdict: weigh it by how many different reporters on how many different servers agree, then check what the server itself recorded.
- Store user ids only, in your own store with access control; delete after a fixed window (30–90 days `[lihfolk]`). Never post reports with names to a Discord webhook.

```lua
--!strict
-- Unexecuted sketch (server). ReportStore and Evidence are your own modules (not shown).
local Players = game:GetService("Players")
local CATEGORIES: { [string]: boolean } = { Griefing = true, Exploiting = true, Teaming = true, TradeScam = true, OffensiveBuild = true, Other = true }
local COOLDOWN, MAX_PER_TARGET = 60, 5
local lastReport: { [number]: number } = {}
local perTarget: { [number]: number } = {}

local function onReport(reporter: Player, targetUserId: unknown, category: unknown)
	if typeof(targetUserId) ~= "number" or typeof(category) ~= "string" or not CATEGORIES[category] then return end
	local target = Players:GetPlayerByUserId(targetUserId)
	if target == nil or target == reporter then return end
	local now = os.clock()
	if now - (lastReport[reporter.UserId] or -math.huge) < COOLDOWN then return end
	if (perTarget[targetUserId] or 0) >= MAX_PER_TARGET then return end
	lastReport[reporter.UserId] = now
	perTarget[targetUserId] = (perTarget[targetUserId] or 0) + 1
	ReportStore.enqueue({ -- ids and server facts only: no names, no chat, no free text
		reporter = reporter.UserId, target = targetUserId, category = category,
		jobId = game.JobId, placeVersion = game.PlaceVersion, at = os.time(),
		context = Evidence.snapshot(reporter, target),
	})
end
```

**Player-made content** `[official][lihfolk]`: filters do not understand shapes. Options in rising cost: preset pieces only on public surfaces; "hide this build" per viewer plus report; builds visible to the builder and friends until reviewed; a trusted-builder privilege (playtime, no reports, `Player:IsVerified()`); human review for anything featured. `IsVerified` is an identity signal (phone or ID), not an age check; the docs suggest it for ranked play and trading integrity.

**Action ladder** (mildest action that stops the harm): hide for the reporter → game mute (`TextSource.CanSend`) → restrict a privilege (no building, no trading) via a profile flag → kick → timed ban → permanent ban → economy correction through the ledger. Taking away the tool (chat, building) while leaving the player in the server often ends the problem; a kick tends to bring the same person back on a second account `[lihfolk]`.

When not to build this: a small obby with no UGC, trading or social hub needs default chat, filtered names, owner-only kick and ban, and a weekly look at the dashboard.

## 7. Ban policy

API fields and the detection ladder are in `networking-and-security.md` §Detection (`Players:BanAsync`, `UnbanAsync`, `GetBanHistoryAsync`, alt propagation, device block). Policy on top:

- **Official guidelines** `[official]`: rules must not contradict the Community Standards (no rule may exclude people for who they are); rules must be stated somewhere all players can read; enforce them fairly, not arbitrarily; players appeal to the creator, and Roblox steps in only if the rules or their enforcement break the Standards.
- **Ban message** `[official]`: filtered, up to 400 characters, may say where to appeal in general terms ("Visit the Discord in my group/game page"); no usernames, handles or direct links.
- **Evidence before action** `[lihfolk]`: a case record with a short case id, user id, account age, each signal with rule version, value and threshold, server `JobId`, place version, ping, device type, economy deltas from the ledger, action, actor and reviewer notes. Put the case id in the display reason and a summary in `PrivateReason`. Keep the reason neutral ("Removed for unfair play. Case K7Q2"): naming the detector teaches exploiters which check fired.
- **Ladder:** first confirmed offence temporary, repeat or severe permanent; statistical cases never propagate to alts (`ExcludeAltAccounts = true`), because shared devices and households can be linked `[lihfolk][VS]`.
- **Appeals:** a published route (group page, support form or ticket); reviewed by someone other than the person who acted; read the evidence before the story; check whether the rule version that fired has since been fixed, and the ping, device and place version context; record the decision; unban with the **same scope** the ban used (`ApplyToUniverse` must match) `[lihfolk]`. Track overturn rate per rule: a rule that is often overturned is a bug.
- **Wrong bans:** restore lost time-limited items and streaks, say so plainly, and fix the rule.
- **Alts:** there is no public API to query alt status (`networking-and-security.md`). Design so a fresh account gains little: gate trading, ranked play and gifting behind playtime, `IsVerified` or device-trust routing.
- Bans do not apply in Studio; test in a private production place `[lihfolk]`. The Creator Hub Bans page and Open Cloud user restrictions let staff act without joining a server `[official][VS]`.
- Evidence is personal data: retention window (the vault suggests 180 days after the last action), restricted access, included in erasure handling (§16).

## 8. Staff, admin tools and their abuse

- **Server-checked rank on every privileged remote**; the panel UI is cosmetic. Never gate powers on a client check, a hidden button, a username or a secret command alias.
- `GroupService:GetRolesInGroupAsync(userId, groupId)` returns `IsMember` and a `Roles` array ordered highest first; **only public roles are included**, the role `Id` is the stable identifier and `Rank` is kept for compatibility only `[official][VS]`. Staff roles used for in-game powers must therefore be public roles, matched by `Id`. Wrap the call in `pcall`; the older `GetRankInGroup` family is superseded.
- Membership is effectively cached for the session `[lihfolk]` (widely observed, not documented): keep a **deny list in live config** (`ConfigService`) so a removed moderator loses powers everywhere within the config refresh, not at next join.
- **Smallest power set:** helpers answer questions; moderators kick, game-mute, restrict and read rule reports; bans and data edits belong to senior staff; a two-person rule for permanent bans and data changes on bigger teams.
- **Log every action** (actor id, target id, action, reason code, `JobId`, time) and review weekly. Remove first and investigate second when players report one name repeatedly: a moderator abusing power destroys trust faster than any exploiter `[lihfolk]`.
- **Admin command suites** (third-party admin systems) arrive as modules that `require` by asset id and often include private-message, announce-as-player and "fun" commands. Under house rule 1 and the backdoor guidance in `networking-and-security.md`, read every line or write the six commands you need as `TextChatCommand`s. Disable any command that lets staff message players privately or players reply: it is chat outside `TextChatService` (§4).
- **Prefer panels to typed commands** for anything with consequences: a typo kicks the wrong player, a list does not `[lihfolk]`.
- **Live "admin" events** (`liveops-quests-retention.md`): scripted and bounded. Grant event items through the same idempotent, logged path as any reward; cap what an admin can spawn; record every grant; never let event powers touch the trading economy unlogged. An admin handing rare items to friends is a dupe with a name on it.
- Private-server owner panels (`accessibility-and-player-qol.md` §11) affect only that server and never grant economy value.

## 9. Exploiters and leaks

Exploiters: technical defence is in `networking-and-security.md`. Community side:

- Do not argue with or name exploiters in public channels; announce outcomes in aggregate ("1,240 accounts actioned for duplication").
- A bug shown in a creator video or spread on social media: patch first; do not punish players retroactively for casual use, only for deliberate large-scale abuse `[lihfolk]`.
- Give honest reporters a route (a private ticket or form) and thank them. One top game publicly offered a $10,000 bounty for finding a duplication bug on its test server before a trading feature shipped `[community: press, search summary]`: paying for dupes found before launch is cheaper than cleaning an economy after.
- Decide dupe consequences from the ledger: remove the duplicated value from the accounts that hold it; avoid broad rollbacks that punish everyone (§15).

Leaks (unreleased content getting out):

- Causes: testers, contractors, shared test places, public asset ids, Place Copying left on, data-mined names in a live build.
- Prevention `[house]`: unreleased work lives in a separate private universe; testers hold a Playtest-only role there; contractors work in a sandbox experience (`team-business-legal.md`); ship update assets in the update build, not weeks early; use codenames for unreleased items in live builds; check Place Copying is off `[official]`; staff discussion in a separate private space.
- Do not run a "leaks" channel for a young audience: it breeds rumours and "I have early access, DM me" scams `[lihfolk]`. Planned teasers do the job honestly.
- When it leaks: do not threaten or dox; remove the leaker's access; rotate secrets they could see; if assets were copied to another game, use the Rights Manager or a copyright notice (`team-business-legal.md`); consider releasing an official teaser so players see the real thing.

## 10. Community spaces

`growth-and-marketing.md` §6 covers the marketing use of the group and Discord. Safety and operations:

- **Roblox group (Community)** first: it is on-platform, reaches every age tier and owns the game. Wall and forum posts, name and logo fall under the Community Standards, and **owners are accountable**: Roblox expects reasonable effort against harmful behaviour, repeated failure can restrict group ownership, and an owner whose group is permanently removed cannot own a new group for 90 days `[official]`.
- **Social links** `[official][VS]`: up to three, on the game details page, only if the owner (or one collaborator in a group) is age-verified 16+, visible only to age-verified 16+ users; never inside the game. If every verified 16+ collaborator leaves a group, its links are deleted after 90 days.
- **Discord** reaches only older, verified players, so codes, patch notes and news must also exist on-platform or most players never see them.

| Situation | Recommendation `[lihfolk]` |
|---|---|
| Solo developer with daily players in the low hundreds | Skip the server or keep it announcement-only; rely on the group plus in-game notes |
| Trading, competitive or large fan base | A server with real moderation by adults |
| Audience mostly Kids and Select | Probably none: most players cannot or should not join |
| Team with testers and contractors | A separate private staff server |

Discord operating rules `[lihfolk]`:

- Discord's terms set a minimum age of 13 (higher in some countries). Discord announced "teen-by-default" settings for all accounts on 9 February 2026, then on 24 February delayed the global age-assurance rollout to the second half of 2026 `[community: Discord press release via search][VS]`. Do not build anything that pushes players to verify there.
- **Staff never DM players.** All staff-to-player contact is in public channels or tickets every staff member can read. No "staff interviews" in private.
- Structure: staff-only news channels (announcements, patch notes, codes) mirrored on-platform; forum channels for suggestions and bugs with status tags; slow mode; one or two voice channels that close when no moderator is on; a mod log.
- Security: verification level with verified email and minimum account age; rules screening; AutoMod on scam phrases ("free robux", "beta tester"), mass mentions and unknown links; explicit-content filter; 2FA required for moderators; permissions by role; no Administrator permission except the owner; few bots, each with minimum permissions.
- Pin: **"We will never ask for your password, cookie, items or Robux. Staff never DM first."** Scam shapes to expect: fake staff, giveaway links, "beta test my game" links that steal session cookies, middleman trades, account selling, impersonation servers.
- Account-linking bots: only ones that use Roblox's official sign-in or a profile-code method; never passwords or cookies.
- Keep Discord and in-game enforcement separate unless a published rule links them.
- Never post player data from the game to Discord; errors and telemetry go to a staff-only channel through the secrets store (`networking-and-security.md`).
- Measure its worth: share-link joins from posts, D7 of that cohort, bug reports that led to fixes, bans and tickets per 1,000 members. If it is mostly codes and scams, shrink it to announcement-only.

In-game guilds and clans: member lists and names are player text (filter, rate-limit); guild chat is a `TextChannel` with eligibility checks; **do not build cross-server guild chat** (it needs a custom transport, which is custom chat) `[lihfolk]`.

## 11. Moderators

- **Who:** enforcement powers for trusted adults. The group permission "Moderate experiences" (read-only view of all in-game chat, ban management across all group games) requires the member to be **18+** `[official]`; treat it as the most sensitive permission in the group. Younger volunteers can be helpers: answer questions, flag issues.
- **How many** `[lihfolk]` (rule of thumb): about one trusted adult per peak hour per 1,000 concurrent players in a social game; far fewer in a combat simulator where abuse is mostly exploiting and handled by automation.
- **Recruit** from long-standing, calm community members; a short application through a form, never a private interview; a trial period with helper powers; 2-step verification before any powers.
- **One-page conduct policy**, accepted before access `[lihfolk]`: do not moderate friends or rivals; no private or off-platform messaging with players; never ask for personal information; never promise outcomes; safety issues go to Roblox (and to Discord Trust and Safety on Discord); do not discuss cases in public; record every action with a reason code.
- **Guidelines by offence:** a table of rule → first, second, third response, so two moderators give the same answer. Publish the player-facing half.
- **Care:** rotate, cap shifts, a private space to decompress, never make moderation the condition for a reward that matters. Volunteers burn out after drama.
- **Offboarding:** remove group roles and per-game permissions, add to the live-config deny list, remove Discord roles, rotate anything they could see (`team-business-legal.md`).
- Paying or contracting moderators, and any agreement with a minor, needs a parent or guardian and professional advice.

## 12. Feedback and bug reports

| Channel | What it gives | Notes |
|---|---|---|
| Creator Hub ⟩ Audience ⟩ Feedback `[official][VS]` | Upvote/downvote trend, comments from players who rated on the details page, AI insight reports | Votes logged from 1 Feb 2025, comments from 17 Mar 2025; updates daily. A downvote spike dated to an update is the fastest backlash signal |
| `SocialService:PromptFeedbackSubmissionAsync` `[official][VS]` | In-game rating and comment prompt feeding the same dashboard; once per player per day; yields | Call from a button in settings or the pause menu, or after a positive moment; never as a join popup. The Player Support ticket flow is alpha for select games |
| In-game bug button `[house]` | Category (stuck, lost item, purchase, crash, other) plus automatic context: place version, `JobId`, device class, position, last error ids | Same rules as reports: no free text unless filtered and rate-limited, ids only, capped per player |
| Discord forum or group posts | Long-form reports, clips | Template: device, what you did, what happened, what you expected, time. Never ask for account details `[lihfolk]` |
| Analytics | Funnel drops, error rate | Often the only sign of a logic bug that throws no error |
| Creators and testers | Early warning before release | Private channel; a tester role in a test universe |

Pipeline `[house]`: one inbox → triage twice a week → label (bug severity as in §15, suggestion, balance, question) → owner → status visible to players (Planned, Fixed, Won't do with a reason) → close the loop in the patch notes ("fixed pets vanishing after teleport; thanks to the reports"). A monthly "what we changed because you asked" post is the cheapest retention work in this file. Player reports found a real odds bug in the vault's reference game (a drop designed for roughly 1-in-3 odds came out at roughly 1 in 370, and nothing errored) `[lihfolk]`: treat "luck feels off" as a bug report, and for paid random items as a compliance issue.

## 13. Drama and update backlash

Before the update:

- Changes players can measure (drop rates, damage, prices, limits) are always in the notes. A silent drop-rate change gets data-mined and framed as deception, and makes the disclosed odds wrong `[lihfolk]`.
- For a nerf: numbers, one honest sentence of reason, what affected players get, what you will watch next. Compensation scales with investment: if players paid Robux for the nerfed thing, compensation is close to mandatory `[lihfolk]`.
- Removals are announced before they happen, with what replaces them; anything purchased keeps working or converts.
- Ship risky changes behind a config flag to a share of servers first (`audit-existing-game.md` safe-change protocol).

When backlash lands:

1. Separate signal from volume: downvote ratio and D1 of the update cohort against the previous week, not the loudest thread.
2. Acknowledge within hours, in game and in the group, without arguing: what you heard, what you are checking, when you will say more.
3. Decide once: revert, adjust or hold with a reason. Reverting is normal: Dress To Impress reversed an accessory update after feedback, saying it agreed with the feedback, and Grow a Garden's team apologised and promised changes after an event misfired `[community: press, search summaries]`.
4. Compensate with something earnable in the free economy (a boost, a cosmetic), once per player, recorded in the save.
5. Never punish criticism. Moderate harassment, slurs and threats, not negative opinions. Staff do not argue in public or from personal accounts.

Community drama (accusations against staff, fights between creators, raids): take the conversation out of public channels, state facts once, remove powers during any investigation of staff, report threats and doxxing to the platform, and do not use the game's channels to litigate personal disputes.

## 14. Creators

Outreach, deals and measurement are in `growth-and-marketing.md` §5. Safety and operations additions `[lihfolk]`:

- Many creators are minors: contact through a business address a parent can see, never private DMs; agreements with a minor need a parent or guardian.
- Do not ask creators to funnel young viewers off-platform. Paid promotion is disclosed.
- A creator who promises traffic through bots, alt accounts or manipulated teleports puts **your** Creator Rewards and account at risk `[official]`.
- Never grant creators admin powers or rigged outcomes; offer a private server, early build access and a creator code.
- Before a known video: freeze risky changes for 48 hours, confirm kill switches, add moderators for the premiere, load-test join and data paths. The vault's rule of thumb is a 10–50× concurrency spike within an hour.
- When a creator's content misrepresents the game (wrong odds, fake rewards), request a correction in private first, then state the facts on your channels. If a creator-themed item's namesake has a scandal: pause sales and communicate.
- Judge a collaboration by the cohort's D7 against baseline, not the peak.

## 15. Crisis playbook

Order of work: **contain → communicate → diagnose → recover → post-mortem**. Teams lose most when they hunt the bug while it keeps doing damage `[lihfolk]`.

| Severity | Definition | Response |
|---|---|---|
| SEV1 | Lasting harm to players or money, spreading: data loss, charged-not-granted purchases, duplication, offensive content visible to players | Contain within minutes, even by turning features or servers off. Anything touching saves or Robux starts here |
| SEV2 | Core loop broken for many, no lasting harm | Contained inside an hour; fixed or rolled back the same day |
| SEV3 | Degraded for some | Next update; workaround message |
| SEV4 | Cosmetic | Backlog |

Containment tools, fastest first `[lihfolk][official]`: config kill switch for the feature (a published config reaches servers in roughly 15 s to 1 min `[official]`, but only if the code refreshes its `ConfigSnapshot` on `UpdateAvailable`; a snapshot read once at startup never changes) → disable the affected purchase prompts → saves to read-only → republish the previous version → restart outdated servers → restart all. Kill switches must exist **before** the incident, default to off for new risky features, keep the last known value on a read failure, and have a tested "off" path (open trades cancel and return items).

| Crisis | First hour | Recovery | Say to players |
|---|---|---|---|
| **Data loss or corruption** | Read-only saves; note the start time; check the Roblox status page before blaming your code | DataStore versions: versioned backups expire 30 days after a newer write overwrites them and the latest never expires `[official][VS]`; the vault adds that a backup is cut on the first write per key per UTC hour `[lihfolk]`. Inspect before restoring; never write under a live session lock (`data-and-purchases.md`). Restore, compensate, or both | "Saves are paused while we fix a problem. Progress before 14:00 UTC is safe." |
| **Purchases charged, not granted** | Flag off the prompts | A handler that errored (did not return `PurchaseGranted`) is retried by Roblox once fixed; one that returned granted needs manual grants from your purchase log | "Purchases are paused. Nothing you bought is lost; it will arrive automatically." |
| **Dupe or economy exploit** | Flag off trading and the affected faucet; snapshot ledgers | Close the validation hole first; remove duplicated value from holding accounts; freeze suspicious trades; avoid global rollbacks; action accounts by the ladder (§7) | "We have paused trading to fix a bug. Nothing you own is at risk. Trading returns when this notice disappears." |
| **Exploit wave** (fly, kill-all, server crash) | Raise server-side checks, enable stricter config thresholds, restart affected servers | Patch the remote or validation gap; ban by evidence, not by reports alone | "We are removing cheaters and have tightened checks. Report with the in-game button." |
| **Offensive content incident** (unfiltered text, offensive build or image visible, bypassed asset) | Hide or disable the surface with a flag; remove the content; restrict the uploader's privilege | Fix the filter or review gap; check the Safety dashboard; update the questionnaire if a feature changed; if Roblox moderated the game, fix first, then appeal through Safety ⟩ Issues & appeals describing the change `[official]` | "We removed content that broke our rules and turned the feature off while we fix it." |
| **Compromised staff or owner account** | From another account with rights, remove its roles; rotate API keys and secrets; check versions, prices, payouts | Restore from known-good versions; Roblox Support for owner recovery | Tell the team and community through channels the attacker does not control |
| **Raid or harassment wave** | Extra moderators, slow mode, temporary server-size or join restrictions | Report to Roblox; talk to any creator involved | Short rules reminder; where to report |

Communication rules `[lihfolk]`: acknowledge before you know the cause; say what is safe and what players should not do; update every 30–60 minutes during SEV1 even if only "still working"; a config-driven in-game banner under about 120 characters; the closing message states the cause, the fix and the compensation; name Roblox as the cause only when its status page says so, and never point at players.

Compensation: generous, quick, uniform, once per player, recorded in the save, with an expiry, and not farmable.

Post-mortem within a few days of every SEV1 and SEV2: timeline, root cause, why it reached players, and actions sorted into **prevent, detect, mitigate**, each with an owner and a date. Blameless means about systems: a post-mortem that ends with "be more careful" has failed `[lihfolk]`. Practise once per quarter on the test place: the first drill always finds a missing permission or an untested kill switch.

## 16. Privacy and data

Not legal advice. Roblox passes erasure requests to creators and holds them responsible for completing them `[official]`; which privacy laws (GDPR, CCPA, LGPD, PIPA, COPPA and others) apply to a given developer is a question for a professional.

**Collect less** `[lihfolk][house]`:

- Store user ids, never usernames or display names. Store gameplay state, not conversations: never log chat, and under platform-integrated chat you cannot.
- No real-world personal data at all: no names, ages, emails, photos, locations, social handles. Do not build forms that ask for them, including in support or appeal flows (use ids and case numbers).
- Histories about other people are personal data too ("last 1,000 opponents", trade logs with counterpart ids, gift records, reports, ban evidence): keep them short-lived and capped.
- Every external service that receives a user id (analytics, a Discord bot, a web database) joins your deletion duty. Send nothing you cannot delete.
- Aggregates without ids ("12,000 swords crafted") are not personal data.
- Viewing DataStores is a privacy-relevant group permission; grant it like one.

**Right to be forgotten (RTBF)** `[official][VS]`: when a user has Roblox delete their account, Roblox messages the creator daily with the requests needing action and the affected games, whatever automation exists. Three mechanisms:

1. **Deletion templates** (Creator Hub ⟩ Configurations ⟩ Data stores manager ⟩ RTBF Deletion, or the Open Cloud Configs API key `user_data_templates`): up to 100 patterns with the case-sensitive token `{UserId}` in the key or scope, for standard and ordered stores; Roblox deletes matches itself.
2. **Webhook** with the Right to Erasure Request trigger for data templates cannot reach (ids inside values, shared keys, external systems). Set a secret and verify the signature; the vault reports five delivery retries before a notification is dropped `[lihfolk]`.
3. **The daily message** as the backstop you still read.

Design keys so templates work: `User_{UserId}` in a fixed store; one long-lived leaderboard store rather than a new store per week; no variable parts in key names; old `_vN` stores either templated or deleted. `RemoveAsync` leaves versions that expire later, so erasure is not instant `[lihfolk][VS]`. Test templates on a test account in a test universe.

Retention defaults `[house]`: rule reports 30–90 days; ban evidence 180 days after the last action; purchase logs as long as support needs them, keyed by user id so templates reach them; analytics through Roblox's own services, which need no export.

## 17. Level-up: symptoms → likely cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| Safety dashboard insight (above the 90th percentile) on Chat | A waiting area or loss screen with nothing to do; cross-team chat in PvP | Shorter waits, activities in lobbies, team-only delivery, Quick Words |
| Avatar-channel report spike after an editor shipped | Outfit or body editor abused | Preset options, bounding limits, restrict or roll back the editor |
| Game moderated for chat | Text conversation possible outside `TextChatService`; editable text without the one-minute limit | Remove or rate-limit, then appeal describing the change |
| Game suddenly unplayable or audience collapsed | Missing or changed maturity label; a new drawing, hangout or private-space feature | Complete the questionnaire; remove or gate the feature; re-submit |
| "Players never answer in chat" | Age groups cannot see each other; many unchecked accounts | `CanUsersChatAsync`, `GetChatGroupsAsync` lobbies; non-chat coordination |
| Chat tags, commands or quick-chat wheel stopped working | `PlatformIntegratedChat` enabled or two modules sharing a callback slot | Native features (`TextChatCommand`, Quick Words, `TextChannelWindow`); one owner per callback |
| Honest players banned; appeals overturn often | Single-signal bans; alt propagation on statistical cases; no rule versioning | Case records, ladder, `ExcludeAltAccounts`, track overturn rate |
| Players accuse a moderator of abuse | Broad powers, no logs, friends moderating friends | Action log, weekly review, smallest power set, conduct policy |
| Ex-staff still has powers | Session-cached rank; roles never removed | Live-config deny list; offboarding checklist |
| Discord full of scams, moderation load rising faster than members | Open posting, teen moderators, no AutoMod | §10 security settings, adult moderators, or announcement-only |
| Update content known before release | Tester or contractor access to the live universe; assets shipped early | Separate universes, codenames, sandbox experiences |
| Downvote spike after an update | Silent nerf, removed feature, monetisation change | §13 playbook; notes with numbers; compensation |
| Same bug reported for weeks | No triage owner; reports only on Discord | One inbox, twice-weekly triage, status tags, in-game bug button |
| Incident dragged on for hours | No kill switch, one person with publish rights, silence | Runbook, flags, two people able to act, banner template |
| RTBF messages piling up | No templates; ids inside values; forgotten leaderboards and old stores | Templates for every store; webhook for the rest; key redesign |

## 18. Conflicts

- **Discord age rules.** LihFolk says Discord's teen-by-default settings launched globally in early 2026. Discord's own press release, as summarised in search on 2026-11-10, shows the announcement (9 Feb 2026) and a later note delaying global age assurance to the second half of 2026. Trust the press release and re-check before relying on either.
- **In-game links.** Older community practice gated Discord links behind `PolicyService`; current docs prohibit in-game social links outright (also recorded in `growth-and-marketing.md`). Follow the docs.
- **Honeypots and instant action.** `networking-and-security.md` allows a session kick on a honeypot hit while bans need several signals; this file's ladder agrees. LihFolk's "permanent ban on honeypot plus economy damage" is compatible because it requires two signal types.
- **Platform-integrated chat dates.** The docs give May 2027 as the requirement; the February 2027 default-on date comes from the announcement as reported by the vault and press, and the vault notes the announcement itself mentions March in one table. Plan for February.
- **Moderator staffing ratio** is a LihFolk rule of thumb with no published benchmark; size from your own report volume.

## Review gate

- [ ] No feature lets players converse outside `TextChatService`; every public editable text is filtered and limited to one edit per minute per player; no replies on comment boards.
- [ ] No in-game link, handle, invite code or request for personal data; no reward for joining off-platform spaces.
- [ ] Questionnaire answered for the most extreme content and re-submitted after the last feature change; hangout, private-space and free-form creation effects were decided on purpose.
- [ ] The core loop was played with chat and voice unavailable and still works.
- [ ] Game tested with `PlatformIntegratedChat` enabled; no code depends on message text; paid chat cosmetics have a non-chat equivalent.
- [ ] Voice is off, or justified, capped at 100 players, routing only restricts, never required or rewarded.
- [ ] Rule reports: fixed categories, server-attached context, rate limits, ids only, fixed retention. The platform report is easy to find.
- [ ] Rules are published; bans carry a case id and evidence; appeals have a route and a second reviewer; statistical bans exclude alts.
- [ ] Staff powers are server-checked against public role ids, logged, minimal, and revocable through a live deny list; "Moderate experiences" only for vetted adults.
- [ ] Group roles on least privilege; Place Copying off; unreleased work in a separate universe.
- [ ] Discord (if any): adult moderation, no staff DMs, security settings on, news mirrored on-platform, no player data posted.
- [ ] Feedback dashboard and Safety dashboard reviewed weekly and after each release; a triage owner exists.
- [ ] Incident runbook: severity table, kill switches tested, read-only saves, rollback steps, banner template, two people able to act; one drill done.
- [ ] RTBF templates cover every store; webhook or manual process for the rest; data inventory lists external services; no chat or real-world personal data stored.

## Sources

Accessed 2026-11-10.

- `Roblox/creator-docs` at commit of 2026-11-07, https://github.com/Roblox/creator-docs (read): `safety.md`; `chat/guidelines.md`; `chat/platform-integrated-chat.md`; `chat/quick-words.md`; `chat/voice-chat.md`; `chat/examples/rate-limit-public-text-inputs.md`; `production/bans.md`; `players/index.md` (ban and message guidelines); `production/promotion/content-maturity.md`; `production/publishing/kids-and-select.md`; `production/publishing/RTBF-and-creators.md`; `cloud-services/data-stores/right-to-be-forgotten.md`; `production/promotion/social-media-links.md`; `projects/groups.md`; `projects/group-guidelines.md`; `projects/collaboration.md`; `production/analytics/feedback.md`; `production/configs.md`; `cloud-services/data-stores/versioning-listing-and-caching.md`; `projects/update-games.md`; engine reference for `TextChatService`, `TextChannel`, `TextSource`, `TextChannelWindow`, `VoiceChatService`, `GroupService:GetRolesInGroupAsync`, `SocialService:PromptFeedbackSubmissionAsync`, `Player:IsVerified`
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `26 Community and Moderation/` (Player Reports and In-Game Moderation; Voice Chat and Safety Features; Discord Servers for Roblox Games; Text Chat Customization with TextChatService; Groups Roles and Permissions for Studios; Working with Content Creators), `49 Roblox Platform Features/` (Policy and Age Rules 2026; Regional Compliance - Paid Random Items and Country Rules), `22 Anti-Exploit and Security/Logging Bans and Appeals.md`, `13 Production and Case Studies/` (Live Incident Response and Post-Mortems; Disaster Recovery for a Roblox Game), `38 Live Ops Deep Dive/Patch Notes and Player Communication.md`, `04 Data and Persistence/Player Privacy and Data Deletion.md`, `11 Monetization Publishing and Live Ops/Refunds Chargebacks and Purchase Support.md` (read)
- https://devforum.roblox.com/t/age-checks-to-access-chat-studio-team-create-and-links-on-roblox/4079702, https://about.roblox.com/newsroom/2026/01/roblox-age-checks-required-to-chat (search summary: age groups, default adjacency, expected chat drop, `CanUserChatAsync`)
- https://create.roblox.com/docs/chat/platform-integrated-chat.md, https://www.gamebusiness.jp/article/2026/10/23/28425.html (search summary; the doc itself was read in the mirror)
- https://discord.com/press-releases/discord-launches-teen-by-default-settings-globally and coverage on pocketgamer.biz, medianama.com (search summary: 9 Feb 2026 announcement, 24 Feb delay note)
- https://www.pockettactics.com/roblox/blade-ball-10k-reward and levelup.com coverage (search summary: bounty for a duplication bug before a trading launch)
- https://www.gameleap.com/articles/dress-to-impress-reverse-the-accessory-update-is-it-free, https://gameranx.com/updates/id/544164/article/roblox-grow-a-garden-team-apologies-to-players-and-promises-better-future-with-updates/ (search summary: reverted update; apology)
- https://devforum.roblox.com/t/traders-on-roblox-are-reportedly-abusing-rollbacks/4820634 (search summary; platform trade rollbacks, context only)
- `references/networking-and-security.md`, `references/growth-and-marketing.md`, `references/monetization-and-policy.md`, `references/liveops-quests-retention.md` (read, for consistency)
- Not reachable: reddit.com, devforum.roblox.com, create.roblox.com, about.roblox.com and help-centre pages (blocked or outside the allowed network); Roblox Community Standards and Terms of Use text were not read directly, only as cited by the docs mirror. No published data on post-age-check chat volume, moderator staffing benchmarks or dupe-incident statistics was found.
