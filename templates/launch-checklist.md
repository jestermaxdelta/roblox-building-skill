# Launch checklist: <Title>  — target date <YYYY-MM-DD>

Run top to bottom in the final three weeks. Each line has an owner and a date. Detailed gates are in references/checklists.md; this is the sign-off sheet. (HR) = house rule.

Mode: [ ] New launch · [ ] Relaunch or major update of a live game. For a live game run Gate A first (references/audit-existing-game.md), keep the universe and DataStore keys, and treat every line marked (LIVE) as mandatory.

Level: a beginner can sign off with the lines marked (HR), the T-14 playtest and scan lines, the receipt test, the thumbnail lines and the soft-launch block; leave experiments, matchmaking, ads and creator lines blank and say so. Intermediate and expert teams fill every line.

Do not start this checklist while any of these is true: nobody outside the team has finished the first session on a mid-range phone; join time on a phone is unmeasured; no funnel logs join to minute 10; the save system has not survived a forced server shutdown test.

## T-21 days: reach and audience

- [ ] Kids/Select path chosen and started: creator verified with 2FA, questionnaire done, Plus/Premium for 2 months or the 1,000 R$ fee; plan for 250 engaged age-checked 16+ plays inside 60 days (older-audience content, community, or an Engagement-objective campaign with its own budget), or the 50,000 R$ expedited review. Owner: __ Date: __
- [ ] Roblox group live and linked; social links set on the details page (owner age-verified 16+); no URLs, invite codes or handles anywhere in-game.
- [ ] One share link per channel and per creator created; LaunchData perks tested.
- [ ] Clip features in the build: hide-UI creator cam, reveal moments with real odds, readable in-world numbers, private servers.
- [ ] Creator shortlist contacted with a build, a private server and a code; paid deals carry disclosure and a share link.
- [ ] Standout Games nomination submitted if the game is original; launch or update event drafted (Off-Platform Featuring needs 7+ days' notice).
- [ ] (LIVE) Baseline window recorded: PTR, bounce, D1/D7, session time, conversion, crash rate, live place version.

## T-14 days: content and quality freeze

- [ ] Vertical slice to full loop verified; all v1 content in; cut list final. Owner: __ Date: __
- [ ] Five-stranger playtest: fun within 5 minutes; median session ≥ <n> min; no P0/P1 UX issues open.
- [ ] (HR) House-rule scan passes in every place: no visible primitive Parts, every visible world mesh collides (only `NonSolid`-tagged canopies, cables, held tools, viewmodels and effect meshes excepted), invisible helpers have CastShadow off. Walk-through test on every asset class.
- [ ] (HR) Asset manifest complete; duplicate-MeshId audit clean; packages AutoUpdate on; no marketplace or free models.
- [ ] Engineering review gate passed (architecture, security, data, purchases).
- [ ] Performance gate passed on a 2–4 GB Android phone, mid-range phone, tablet, desktop and TV with gamepad; 10–15 minute thermal test; 1-hour server soak.
- [ ] Streaming verified at `StreamingTargetRadius = 64`.

## T-10 days: monetization and compliance

- [ ] Products, passes and (if used) subscriptions created in Creator Hub; ids in the config module; prices displayed via `GetProductInfoAsync`.
- [ ] Receipt handler tested end to end in a published test place, including rejoin after an unacknowledged purchase and two-server replay.
- [ ] Gift flow tested with an offline recipient (MessageAsync delivery).
- [ ] (HR) Offer gate verified: nothing before 10 min and first win; ≥ 8 min gaps; ≤ 3 per session; dismiss suppression; small, dismissible, honest copy.
- [ ] Paid random items: odds UI shows every outcome, sums to 100%, boosted odds live; `PolicyService` fallbacks tested with a restricted test account.
- [ ] No fake discounts, restarting countdowns or false scarcity anywhere in UI or store copy.
- [ ] Rewarded video eligibility confirmed; rewards fixed; placements live.
- [ ] Content-maturity questionnaire submitted truthfully; expected label <Minimal / Mild / Moderate>.
- [ ] All user-generated text filtered on the server.

## T-7 days: discovery and metadata

- [ ] Five custom 16:9 1920×1080 thumbnails (< 3 MB), 2–5 active; icon 512×512 readable at 150 px.
- [ ] Title with status tag and verb phrase; description hook in the first 160 characters; genre set; supported languages set.
- [ ] Gameplay video uploaded: authentic gameplay, no spoken audio, lyrics, real-life footage or ad text (3 uploads per month; rejections count).
- [ ] Thumbnails are distinct hooks, not recolours; each shows something reachable in the first minute; no Robux, giveaway or "free" wording in title, thumbnails or description (HR).
- [ ] Languages enabled (Experience Information and Strings); Automatic Text Capture on; no text baked into UI images.
- [ ] Experience Event created with Notify Me for launch or update day; update announcement drafted (60 characters, specific).
- [ ] Share links per channel; invite prompt and referral banner wired and tested.
- [ ] Age-tier plan: launch at <16+ / Select>; under-16 eligibility steps started (verification, 2FA, questionnaire, Plus/Premium or 1,000 R$ fee).
- [ ] Matchmaking weights set (Friends and Occupancy raised for social games).

## T-5 days: analytics and LiveOps

- [ ] Onboarding, Shop, Offer and RV funnels plus economy and custom events verified in the test place dashboards.
- [ ] Every tunable is a Configs key with a correct default; Experiments for the first two tests drafted.
- [ ] Weekly update day chosen and announced; first four updates planned; first event dated with its own currency.
- [ ] Performance Dashboard alerts: crash rate above 2–3%, out-of-memory exits, server frame rate, memory, sent to a webhook; `ServerLowMemoryWarning` logged.
- [ ] Rollback triggers written (for example crash rate +2 points, purchase failures, early-harm flag); owner on call for the first 2 hours.
- [ ] `DataModel.ServerRestartScheduled` handled: in-game countdown and save before a delayed restart.
- [ ] (LIVE) New behaviour sits behind Configs keys whose defaults are the old behaviour; save schema change is additive, tested on copies of real profiles and readable by servers still on the old version; nothing a player paid for is removed.
- [ ] Safety: `BanAsync` tooling, report handling and appeal path ready; ban rules published.
- [ ] Rollback plan: previous version id recorded; data migrations backwards compatible or Migrate To Latest Update chosen.

## T-7 to T-3 days: soft launch (public, "Exclude from recommendations" on)

- [ ] A few hundred players you control brought in (community, testers' friends, a small Plays campaign with a LaunchData tag). Owner: __ Date: __
- [ ] Zero data loss and no stuck tutorial states across the cohort; console clean.
- [ ] 85%+ of new players reach the first reward within 60 s (fix first if under 70%).
- [ ] Biggest single-step drop in the first 3 minutes is under 15% (fix first if over 25%).
- [ ] Median first session 10+ min (fix first if under 5); D1 direction noted (small samples are noisy).
- [ ] Kill switches exist for trading, new shop items and any currency source; test-only flags guarded by `RunService:IsStudio()`.
- [ ] Server size set for expected launch CCU so players land together; the loop works with one to three players.
- [ ] One fix shipped per leak, cohort re-read; recommendations stay excluded until the bars pass.

## T-1 day

- [ ] CI produced the release build; test universe green; production publish approved manually.
- [ ] Private soak with the team for 1 hour on the production place; console clean.
- [ ] Dev and test places are in separate universes; gated sub-places "Secure within universe only".
- [ ] Secrets only in the Secrets store; no keys in scripts or git.

## Launch day (Saturday, inside a seasonal window if possible)

- [ ] Build published earlier in the week and gated by server time or a Config; go-live (recommendations on, event start, announcement) opens into the weekend. Launch-day changes are bug fixes only.
- [ ] Roles set for the first 12 hours: errors, funnel and player count, community reports (solo: hourly alarms).
- [ ] Publish at <time>; verify join on phone and PC; watch Performance Dashboard (by place version) and console errors for the first 2 hours.
- [ ] (LIVE) Restart only servers with outdated versions, with a 5–10 minute delay; confirm the restore path (restore version → publish → restart).
- [ ] Send the update announcement; start the event; switch the title tag and thumbnail set; post the first clip and the group and community posts with share links.
- [ ] Monitor PTR, bounce and D1 daily for the first week; fix the largest onboarding funnel drop first.
- [ ] Post the first update on the announced weekly day.

## Week 1 after launch

- [ ] Read the launch cohort, not the blended average: daily cohort table, first-session retention curve, Home Recommendations signals; wait 24–72 h for PTR and bounce, 2 days for D1, 8 days for D7.
- [ ] Read the share-link funnel per channel (users with qualified plays, 7-day playtime, D7, 30-day revenue per user); drop the channels that bring players who leave.
- [ ] No paid traffic until the growth gate in references/checklists.md passes (bounce and D1 at or above benchmark median, like ratio ≥ 85%, max cost per play computed). Exception: a capped measurement buy or the Engagement objective for the 250-play gate.
- [ ] Thumbnails left alone for 7+ days; change one variable per release.
- [ ] Day 5–7 branch chosen and written down: healthy (first content drop, consider ads) · leaky start (fix onboarding, buy nothing, add no content) · weak promise (new thumbnail concepts) · no pull (competitor teardown before spending more).
- [ ] Days 7–14: first content aimed at existing players, paired with an event, one new thumbnail, one update announcement.

## Sign-off

| Gate | Owner | Date | Result |
|---|---|---|---|
| Design | | | |
| Engineering | | | |
| Compliance (HR) | | | |
| Performance and content (HR) | | | |
| Discovery and LiveOps | | | |
| Growth and community | | | |
| Live-change safety (LIVE) | | | |
