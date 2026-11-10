# Consolidated checklists and ship gates

Collected from knowledge-base sections 1.12.3 (design review), 3.8 (compliance), 3.10 (launch), 4.11 (engineering anti-patterns) and 5.13 (pre-launch performance and content). Each topic reference file ends with its own detailed gate; this file is the short version to run at each phase. Items marked (HR) enforce a house rule.

Two entry points. Building from scratch: run Gate 0 → Gate 5 in order. Levelling up an existing game: run Gate A first; it tells you which of Gates 0–5 to re-run and in what order, and every change it produces ships through the live-change items at the end of Gate A.

## Start here by level

| Level | Run | Skip for now |
|---|---|---|
| Beginner | Gate 0 (one-pager and first-five-minutes script), Gate 1, the house-rule scan in Gate 4, the three data items at the top of Gate 2 "Data and purchases", and Gate 3 if anything is sold. For an existing game: Gate A "Before touching anything" plus the top-3 actions | Tooling, CI, experiments, matchmaking, the growth gate |
| Intermediate | Every gate in order; Gate 2 before every release; Gate A every 6 weeks | Nothing in Gates 0–5; treat the growth gate as optional until retention holds |
| Expert | All gates as release criteria in CI or a release checklist, with a named owner per gate; second-opinion review on ship and rebuild calls; deliverable scores logged | Nothing |

A gate item is pass or fail with evidence (a number, a screenshot, a file and line). "Mostly" is a fail.

## Gate A: level-up audit (existing games)

Method, scoring criteria and benchmark table: `references/audit-existing-game.md`. Report: `templates/game-audit-report.md`.

Before touching anything

- [ ] Intake answered: universe and place IDs, 6-week goal and target metric, source owner (Rojo, Script Sync or Studio), data layer and schema version, last 30 days of changes.
- [ ] Baseline recorded: 14 days (minimum 7) of PTR, bounce < 60 s and 61–180 s, D1/D7/D30, session time, conversion, ARPPU, ARPDAU, crash rate, plus the live place version number. No PTR comparison across 12 Oct 2026.
- [ ] Benchmark named for every number: the game's own Creator Analytics benchmark and its type, or the dated fallback when under 100 DAU.
- [ ] Developer level set (beginner, intermediate, expert) and the report shaped to it: a beginner gets blockers plus the top 3 actions explained; an expert gets the full ranked list with measurements.
- [ ] Audit ran read-only: Studio MCP in Edit mode, "Save & load data" and publish permissions off, no `multi_edit`, no DataStore calls, nothing saved or published.

Findings

- [ ] All ten dimensions scored 0–5 with one evidence line each: first session, core loop, progression and economy, retention and LiveOps, monetisation, UI/UX, art and house rules, performance, security and data, discovery and growth.
- [ ] Caps applied: no live numbers → at most 3; (HR) any visible primitive, marketplace or generated asset, walk-through mesh, invasive or non-compliant offer, client-trusted value or data-loss path → at most 1 and listed as a blocker.
- [ ] (HR) House-rule scan run in every place; output pasted into the report.
- [ ] Sub-checks run on a phone and their caps applied: 2a game feel and audio, 6a accessibility and quality of life, 4a community and safety (unfiltered player text or an in-game link is a blocker).
- [ ] Every finding carries an evidence grade (measured, observed, static, inferred); findings from reading alone are labelled "static, not measured"; dismissed findings are listed.
- [ ] Timed first-session log filled: seconds to playable, first reward, first upgrade, first prompt, first Robux offer.
- [ ] Triage step named (T0–T8) with the numbers that selected it; platform causes (seasonality, competitors, algorithm change) ruled in or out.

Plan

- [ ] Every action has Impact × Confidence ÷ Effort, a metric it should move, and the reference it routes to; top 10 ranked; blockers first.
- [ ] Decision stated with its rule: quick-wins sprint, rebuild the loop in the same universe, or park. A rebuild keeps the universe, DataStore keys, purchases and community.
- [ ] A rebuild, park, save-schema migration, live price change or ship decision has a blind second opinion: neutral question, rubric fixed first, same evidence pack, dissent and confidence recorded.
- [ ] 2-week plan has one target metric and one variable per dimension per week; 6-week plan ends with a re-audit.
- [ ] The gates to re-run are listed (for example Gate 3 after any offer change, Gate 4 after any art or performance change, Gate 2 before every release).

Shipping changes to a live game

- [ ] Version History note on the live version; local `.rbxl` and git tag saved; restore path understood (restore → publish → restart servers).
- [ ] Changes built in a separate test universe; no production data touched from Studio.
- [ ] Each behaviour change sits behind a Configs key whose code default is the old behaviour; Experiment (50/50, early-harm watched) or a dated cohort comparison chosen.
- [ ] Save data: additive schema only, version bumped, migration tested on copies of real profiles, readable by servers still on the old version, key pattern unchanged, nothing wiped.
- [ ] (HR) Nothing a player paid for is removed or weakened; compensation planned and announced where a paid item changes.
- [ ] Release at off-peak; restart only outdated servers with a delay; `ServerRestartScheduled` countdown shown.
- [ ] Alerts on crash rate, out-of-memory exits and server frame rate; Performance dashboard watched by place version for 2 hours.
- [ ] Rollback triggers written before release; Config flip first, version restore second.
- [ ] Update announcement (60 characters), Experience Event and in-game changelog posted; thumbnails and title changed only with the update.
- [ ] Risky systems (trading, new shop items, currency sources) have a kill switch; test-only flags are guarded by `RunService:IsStudio()`; errors log `JobId` and place version.
- [ ] Result read after the lag (PTR and bounce 24–72 h, D1 2 days, D7 8 days) and logged as kept or reverted.
- [ ] Each shipped deliverable scored 0–10 (any failed gate caps it at 5.0); nothing under 8.5 is reported as done.

## Gate 0: before any code (design review)

- [ ] One-pager complete: player fantasy, one-sentence pitch, three pillars, core loop, session loop, long-term loop, target audience and age tier, platform priority (mobile first), comparable games, risks.
- [ ] Core loop scores at least 7/10 on the rubric in design-foundations.md (clear goal, fast feedback, meaningful choice, variable reward, visible progress, social hook, repeatability, low friction, fantasy fit, monetization fit).
- [ ] FTUE script written: first reward under 30 s, first upgrade under 2 min, one verb at a time, no offers.
- [ ] Economy sheet modelled with numbers (faucets, sinks, first ten prices, rebirth ratio, pack ladder).
- [ ] Retention and social hooks named for D1, D7 and D30.
- [ ] Monetization plan uses the house default product set; every paid shortcut has a free alternative; Luck items only if luck mechanics exist.
- [ ] Scope fits the milestone plan (vertical slice first); kill criteria written for the prototype.
- [ ] Risk list with the top three risks and a test for each.

## Gate 1: vertical slice

- [ ] The core loop is playable end to end with placeholder-free visuals from the Blender blockout kit or inside a throwaway place (HR: no primitive greybox ships).
- [ ] Five strangers playtested; the Kill/Keep decision is recorded with the evidence.
- [ ] Architecture skeleton exists: single server and client entries, DataService with ProfileStore, RemoteGuard, ReceiptService, analytics stubs.
- [ ] Performance smoke test on one low-end Android phone.

## Gate 2: engineering review (run before every release)

Architecture and Luau

- [ ] One server entry and one client entry; no Scripts inside models; behaviour by tags.
- [ ] No require cycles; no yields at module top level or in `Init`; handlers cover players and characters already present.
- [ ] Every per-player table cleared on `PlayerRemoving`; every connection owned by a Trove.
- [ ] `--!strict`; untrusted input typed `unknown`; no `wait`/`spawn`/`delay`/`tick`/`Humanoid:LoadAnimation`/BodyMovers/`FindPartOnRay`.
- [ ] Every web-service call `pcall`ed with a failure branch; code works under `SignalBehavior = Deferred`.

Networking and security

- [ ] Remotes carry intent; the server never trusts client ids, prices, damage or positions.
- [ ] Every remote passes rate limiting plus type, finiteness, range, length, UTF-8, instance and game-rule checks; rejections silent.
- [ ] No `InvokeClient`; `OnServerInvoke` assigned once; unreliable remotes carry only replaceable data under 1,000 bytes.
- [ ] Prompts and detectors re-validated on the server; interactable anchors anchored.
- [ ] Movement and combat validated with tolerances; no `Touched`-only damage.
- [ ] No secrets or server logic in replicated containers; gated sub-places "Secure within universe only"; dev and test universes separate.
- [ ] Consequences escalate; no instant ban on a single signal.

Data and purchases

- [ ] Session-locked loading; a failed load never saves; migrations before `Reconcile`; newer-schema guard; key pattern unchanged.
- [ ] No DataStore reads during gameplay; staggered autosave; no custom BindToClose on top of ProfileStore.
- [ ] Exactly one `ProcessReceipt` (or filtered handlers); dedupe by `PurchaseId` in saved data; `PurchaseGranted` only after confirmed save.
- [ ] Nothing granted from `PromptProductPurchaseFinished`; pass ownership checked on the server with correct caching.
- [ ] Prices from `GetProductInfoAsync`; gifts gated by price level; boosts extend, never stack.
- [ ] Leaderboard writes throttled; trades mutate both locked profiles synchronously; RTBF templates cover every user-keyed store.

Tooling

- [ ] Toolchain pinned; `wally.lock` committed; selene, StyLua and luau-lsp gate every PR; only CI publishes production.

## Gate 3: compliance and monetization (HR)

- [ ] Every paid random item (crates, eggs, summons, Luck, Server Luck, pity) shows full numeric odds summing to 100% before purchase, boosted odds live; `PolicyService` gates random items, paid-item trading and ads; failures fail closed.
- [ ] No fake discounts, restarting countdowns or false scarcity.
- [ ] No offers in the first 10 minutes, before the first win, on loading, or during combat; ≥ 8 min between offers, ≤ 3 per session, ≤ 1 starter pack per day, 24 h suppression after two dismissals; offers ≤ 25% of the screen with an X, never stacked, no sound stings.
- [ ] Rewarded-video rewards fixed, opt-in, never a gate; eligibility met.
- [ ] A free alternative sits next to every paid shortcut.
- [ ] Content-maturity questionnaire truthful; rating-raising features deliberate; no playable gambling.
- [ ] All user-generated text filtered on the server.
- [ ] Social rewards (group join, like, favourite, friend join) are bonuses only: no progress, product or content gated on them; group join verified server-side; shown after the first win; nothing about them in title, thumbnail or description.
- [ ] Thumbnails and video follow policy (no spoken audio, real footage or ad text in video).

## Gate 4: performance and content (HR)

- [ ] Low-end Android (2–4 GB) ≥ 30 FPS in the busiest scene; mid-range about 60; no spikes over about 50 ms in a 2-minute capture; 10–15 minute thermal test passed.
- [ ] Server heartbeat about 60 Hz with a full server; memory < 50% of (6.25 GiB + 100 MiB × max players) and flat over a 1-hour soak.
- [ ] Draw calls < 1,000, triangles < 1 M in the worst view; duplicate-MeshId audit clean.
- [ ] Streaming on with recommended settings; works at `StreamingTargetRadius = 64`; interactive models Atomic; `RequestStreamAroundAsync` before teleports; no LocalScript indexes Workspace without a timeout or tags.
- [ ] All static geometry anchored; mechanisms anchor only the root; no `PreciseConvexDecomposition` except approved doorways; non-colliding meshes Box; collision groups registered once.
- [ ] **Every visible object is a Blender model, and all world geometry blocks players and NPCs** (only held tools, viewmodels, transient effect meshes, foliage canopies and cables may be non-solid; skinned meshes collide through a `_COL` proxy); the scan below passes; walk-through test passes; Terrain only with explicit owner approval.
- [ ] Triangle and texture budgets met; `_SA` library shared; RenderFidelity Automatic; SLIM on large static models where available.
- [ ] LightingStyle chosen; no interior leaks; CastShadow off on small, moving and invisible parts; scene reads at graphics levels 1–3.
- [ ] Particle rates within mobile caps; VFX client-side and pooled; no server tweens or server VFX; animations loaded once; concurrent sounds capped; volume sliders exist.
- [ ] UI tested on phone (portrait and landscape), tablet, desktop and TV with gamepad; `CoreUISafeInsets`; nothing in reserved zones; every action bound on keyboard, gamepad and touch; `PreferredInput`, `PreferredTextSize`, `PreferredTransparency` and `ReducedMotionEnabled` honoured; console chat disabled.
- [ ] Join-to-playable ≤ 10–15 s on low-end Android; loading screen has Skip, no forced minimum, never waits on spatial instances; no offers on loading.

House-rule scan (edit mode, via Studio MCP `execute_luau` or the command bar; never in live servers):

```lua
local issues = {}
for _, d in workspace:GetDescendants() do
	if d:IsA("BasePart") and d ~= workspace.Terrain then
		local visible = d.Transparency < 1
		if visible and not d:IsA("MeshPart") then
			table.insert(issues, "VISIBLE PRIMITIVE: " .. d:GetFullName())
		end
		if not visible and d.CastShadow then
			table.insert(issues, "INVISIBLE HELPER CASTS SHADOW: " .. d:GetFullName())
		end
		if visible and d:IsA("MeshPart") and not d.CanCollide and not d:HasTag("NonSolid") then
			local model = d:FindFirstAncestorOfClass("Model")
			if not (model and model:FindFirstChild(d.Name .. "_COL", true)) then
				table.insert(issues, "VISIBLE MESH WITHOUT COLLISION: " .. d:GetFullName())
			end
		end
	end
end
print(#issues == 0 and "House-rule scan OK" or table.concat(issues, "\n"))
```

Tag the allowed non-solid visuals `NonSolid`: foliage canopies, cables, held tools, viewmodels and transient effect meshes. Nothing else in the world may carry the tag.

## Gate 5: launch (discovery, analytics, LiveOps)

Product and quality

- [ ] Fun within 5 minutes confirmed by strangers; bounce under 60 s measured on a low-end phone.
- [ ] Gates 2, 3 and 4 passed; soak test done.

Monetization and compliance

- [ ] Default product set live with prices read from the API; offer gate tuned through Configs; receipts verified end to end in a test place.

Discovery and metadata

- [ ] Five custom 16:9 1920×1080 thumbnails under 3 MB (2–5 active), icon readable at 150 px, title with status tag and verb phrase, description hook under 160 characters, genre set, supported languages set.
- [ ] Age-tier plan: launch 16+ (or Select if eligible), then pursue the 250 engaged age-checked plays for under-16 reach; questionnaire complete.
- [ ] Share links, invite prompt (`CanSendGameInviteAsync` → `PromptGameInvite`) and referral banner wired.

Analytics and LiveOps

- [ ] Onboarding, shop, offer and rewarded-video funnels plus economy events live in a published test place first; dashboards checked.
- [ ] Configs for every tunable; first two Experiments planned.
- [ ] Four weeks of updates planned at the weekly cadence; first event dated with its own currency.
- [ ] Performance Dashboard alerts set (crash rate above 2–3%, heartbeat, memory); `ServerLowMemoryWarning` logged.
- [ ] Matchmaking weights chosen (Friends and Occupancy raised for social games).

Timing

- [ ] Launch inside a seasonal window (summer 10–30 June, Halloween, winter) and on or just before a Saturday; weekly update day announced.
- [ ] Rollback plan: previous place version noted; Migrate To Latest Update decision made for any data migration.

## After launch (weekly)

- [ ] Read PTR, bounce, D1/D7/D30, co-play, ARPDAU against last week and against the genre benchmark.
- [ ] Review the onboarding funnel for the biggest drop and fix it first.
- [ ] Re-run the MicroProfiler and Scene Analysis after each content update.
- [ ] Review safety dashboard reports and ban appeals.
- [ ] Ship the weekly update on the announced day.
- [ ] Check the Performance dashboard by place version after each publish; read the Feedback dashboard for a downvote spike.
- [ ] Every 6 weeks, or after two flat weeks, re-run Gate A and rescore.

## Growth gate: before paid or creator-driven traffic

Detail in `references/growth-and-marketing.md`.

- [ ] Bounce and D1 at or above the benchmark median (fallback D1 > 11%); like ratio ≥ 85%; crash rate under 2–3%.
- [ ] Funnels and economy events live; 30-day revenue per new user by source known; max cost per play computed with a stop-loss date.
- [ ] One share link per channel and per creator; creatives are real captures of the game and match the first minute.
- [ ] (HR) No giveaway, Robux or "free" wording in title, thumbnails or description; social rewards stay bonuses after the first win; no restarting countdowns or false scarcity in event marketing.
- [ ] No URLs, invite codes or handles in-game; social links only on the details page; paid creator content disclosed.
- [ ] Engagement-objective spend (for the 250-play gate) has its own budget and is paused at the goal.
- [ ] Soft launch done with "Exclude from recommendations" on: 85%+ of new players reach the first reward within 60 s, no step in the first 3 minutes loses over 15%, median first session 10+ min.
- [ ] Ad and share-link joins tagged through LaunchData; cohort value computed per unique user, not per play.
- [ ] Server size fits current CCU; the loop works with one to three players.

## Sources

This file restates gates defined in the topic references; evidence and source lists live there. Gate A and the growth gate were added on 2026-11-10 from `references/audit-existing-game.md` and `references/growth-and-marketing.md` (creator docs read from the `Roblox/creator-docs` mirror, commit dated 2026-11-07).

- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/quality-score/SKILL.md`, `skills/council-method/SKILL.md`, `commands/audit.md`, `27 Marketing and Growth/Launch Strategy - The First Two Weeks.md`, `Rescuing a Weak Launch - Empty Servers, Low CCU and Relaunch Tactics.md` (read). Source of the evidence-grade, second-opinion, deliverable-score and soft-launch items, rewritten in our own words `[lihfolk]`.
