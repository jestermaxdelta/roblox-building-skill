# Consolidated checklists and ship gates

Each topic reference ends with its own detailed gate; this file is the short version to run at each phase (phases in `references/workflow-phases.md`, standing rules in `references/decision-rules.md`, file map in `references/INDEX.md`). Items marked (HR) enforce a house rule. Quality is scored with the rubric the owning guide defines; this file names the rubric and its pass mark and does not restate criteria.

Two entry points. Building from scratch: run Gate 0 → Gate 5 in order. Levelling up an existing game: run Gate A first; it tells you which of Gates 0–5 to re-run and in what order, and every change it produces ships through the live-change items at the end of Gate A.

## Start here by level

| Level | Run | Skip for now |
|---|---|---|
| Beginner | Gate 0 (one-pager and first-five-minutes script), Gate 1, the house-rule scan in Gate 4, the three data items at the top of Gate 2 "Data and purchases", and Gate 3 if anything is sold. For an existing game: Gate A "Before touching anything" plus the top-3 actions | Tooling, CI, experiments, matchmaking, the growth gate |
| Intermediate | Every gate in order; Gate 2 before every release; Gate A every 6 weeks | Nothing in Gates 0–5; treat the growth gate as optional until retention holds |
| Expert | All gates as release criteria in CI or a release checklist, with a named owner per gate; second-opinion review on ship and rebuild calls; deliverable scores logged | Nothing |

A gate item is pass or fail with evidence (a number, a screenshot, a file and line). "Mostly" is a fail.

## Gate A: level-up audit (existing games)

Method, scoring and routing (finding → guide, §10): `references/audit-existing-game.md`. Benchmark table: `references/analytics-and-discovery.md` §Benchmarks. Report: `templates/game-audit-report.md`.

Before touching anything

- [ ] Intake answered: universe and place IDs, 6-week goal and target metric, source owner (Rojo, Script Sync or Studio), data layer and schema version, last 30 days of changes.
- [ ] Baseline recorded: 14 days (minimum 7) of PTR, bounce < 60 s and 61–180 s, D1/D7/D30, session time, conversion, ARPPU, ARPDAU, crash rate, plus the live place version number. No PTR comparison across 12 Oct 2026.
- [ ] Benchmark named for every number: the game's own Creator Analytics benchmark and its type, or the dated fallback when under 100 DAU.
- [ ] Developer level set (beginner, intermediate, expert) and the report shaped to it: a beginner gets blockers plus the top 3 actions explained; an expert gets the full ranked list with measurements.
- [ ] Audit ran read-only: Studio MCP in Edit mode, "Save & load data" and publish permissions off, no `multi_edit`, no DataStore calls, nothing saved or published.

Findings

- [ ] All ten dimensions scored 0–5 with one evidence line each: first session, core loop, progression and economy, retention and LiveOps, monetisation, UI/UX, art and house rules, performance, security and data, discovery and growth.
- [ ] Five dimensions quote a guide rubric as evidence: first session → tutorial rubric (`tutorial-and-onboarding.md` §13, pass 16/20); core loop → loop scorecard (`core-loop-tuning.md` §4, pass 7/10); UI/UX → UI rubric per screen (`ui-design-figma.md` §9, pass 8/10); art → whole-game art review (`art-direction-and-quality-bar.md` §8, score = lowest discipline); discovery → store-page gates and rubric (`icons-thumbnails-and-store-page.md` §15, pass 8.5/10).
- [ ] Caps applied to scores: no live numbers → at most 3; (HR) any visible primitive, marketplace or generated asset, walk-through mesh, invasive or non-compliant offer, client-trusted value or data-loss path → at most 1 for that dimension. A cap describes the game; it does not set the order of work.
- [ ] Blockers listed separately and fixed first: data loss, ungranted purchases, dupes and client-trusted values, policy violations, (HR) walk-through geometry on the main path, (HR) invasive or non-compliant offers. Nothing else is a blocker.
- [ ] (HR) Every other house-rule violation is a finding on the debt track: listed by surface, ordered by visibility (spawn view, shop, main path, capture spots, the rest), with a fixed 20–30% of weekly hours. It does not hold up other fixes and never triggers a rebuild by itself.
- [ ] (HR) House-rule scan run in every place; output pasted into the report.
- [ ] Sub-checks run on a phone and their caps applied: 2a game feel and audio, 6a accessibility and quality of life, 4a community and safety (unfiltered player text or an in-game link is a blocker).
- [ ] Every finding carries an evidence grade (measured, observed, static, inferred); findings from reading alone are labelled "static, not measured"; dismissed findings are listed.
- [ ] Timed first-session log filled: seconds to playable, first reward, first upgrade, first prompt, first Robux offer.
- [ ] Triage step named (T0–T8) with the numbers that selected it; platform causes (seasonality, competitors, algorithm change) ruled in or out.

Plan

- [ ] Every action has Impact × Confidence ÷ Effort, a metric it should move, and the reference it routes to (audit §10; tutorial, art direction, UI screens, UI motion, VFX recipes, cutscenes, store page and the visual library each have a row); top 10 ranked; blockers first. Effort is in hours and restated in weeks at the owner's weekly budget.
- [ ] With no place access, the numbers-only first pass was sent (triage step, top 3 actions with reasons, at most five asks, under about 400 words) instead of an empty report.
- [ ] Decision stated with its rule: quick-wins sprint (the default), rebuild the loop in the same universe (an option presented with its hours and weeks, chosen only if the loop problem is measured, the estimate fits about eight weeks of the owner's budget and a second opinion agrees), or park. A rebuild keeps the universe, DataStore keys, purchases and community.
- [ ] A rebuild, park, save-schema migration, live price change or ship decision has a blind second opinion: neutral question, rubric fixed first, same evidence pack, dissent and confidence recorded.
- [ ] First sprint plan (two weeks of the owner's hours) has one target metric, one variable per dimension per week and the 20–30% debt-track block; 6-week plan ends with a re-audit.
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
- [ ] FTUE script written in the format of `tutorial-and-onboarding.md` §2: first verb by 15 s, first reward by 30 s, first upgrade by 2 min, one verb at a time, no offers.
- [ ] Art direction decided before any asset: the three-decisions line, palette and bevel width (`art-direction-and-quality-bar.md` §3–6); three to five references chosen from `references/visual-library/` with what to take from each.
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
- [ ] Look-and-feel rubrics passed, each scored by someone other than the maker: art review with no discipline under 6 and no caps (`art-direction-and-quality-bar.md` §7–8, soft-launch tier); UI rubric 8+ on every screen (`ui-design-figma.md` §9; screens built from `ui-screen-recipes.md`); UI motion on tokens with a reduced-motion path (`ui-motion-and-feedback.md` review gate); core-verb and reward effects 16/20 (`vfx-and-juice.md` §16); tutorial 16/20 (`tutorial-and-onboarding.md` §13); any cutscene skippable and 16/20 (`cutscenes-and-cinematics.md` §18).

House-rule scan (edit mode, via Studio MCP `execute_luau` with `datamodel_type = "Edit"`, or the command bar; never in live servers). It groups findings by area with counts, caps its output, and checks who uploaded the most-used meshes:

```lua
--!strict
-- House-rule scan. Unexecuted sketch. Edit mode only and read-only: it changes and saves nothing.
local MarketplaceService = game:GetService("MarketplaceService")

local MAX_ROWS = 25 -- areas printed
local CREATOR_CHECKS = 30 -- most-used MeshIds to look up; 0 skips the lookup
local CHECK_PAUSE = 0.5 -- seconds between lookups; GetProductInfoAsync is rate-limited
local PRIM, NOCOL, SHADOW = 1, 2, 3

local roots: { Instance } = { workspace, game:GetService("ReplicatedStorage"), game:GetService("ServerStorage") }
local areas: { [string]: { number } } = {}
local totals: { number } = { 0, 0, 0 }
local meshUses: { [string]: number } = {}

-- Area = service plus the next two levels, for example "Workspace/Map/Shop".
local function areaOf(inst: Instance): string
	local names: { string } = {}
	local current: Instance? = inst.Parent
	while current ~= nil and current ~= game do
		table.insert(names, 1, current.Name)
		current = current.Parent
	end
	return table.concat(names, "/", 1, math.min(#names, 3))
end

local function bump(inst: Instance, kind: number)
	local key = areaOf(inst)
	local tally = areas[key]
	if tally == nil then
		tally = { 0, 0, 0 }
		areas[key] = tally
	end
	tally[kind] += 1
	totals[kind] += 1
end

local seen = 0
for _, root in roots do
	for _, d in root:GetDescendants() do
		seen += 1
		if seen % 2000 == 0 then
			task.wait() -- keep Studio responsive
		end
		if d:IsA("BasePart") and not d:IsA("Terrain") then
			if d.Transparency >= 1 then
				if d.CastShadow then
					bump(d, SHADOW)
				end
			elseif d:IsA("MeshPart") then
				meshUses[d.MeshId] = (meshUses[d.MeshId] or 0) + 1
				if not d.CanCollide and not d:HasTag("NonSolid") then
					local model = d:FindFirstAncestorOfClass("Model")
					if not (model and model:FindFirstChild(d.Name .. "_COL", true)) then
						bump(d, NOCOL)
					end
				end
			else
				bump(d, PRIM) -- Part, WedgePart, TrussPart, UnionOperation and other non-mesh parts
			end
		end
	end
end

local out: { string } = {
	`Visible primitives {totals[PRIM]} | visible meshes without collision {totals[NOCOL]} | invisible helpers casting shadow {totals[SHADOW]}`,
}
local keys: { string } = {}
for key in areas do
	table.insert(keys, key)
end
table.sort(keys, function(a: string, b: string): boolean
	return areas[a][PRIM] + areas[a][NOCOL] > areas[b][PRIM] + areas[b][NOCOL]
end)
for i = 1, math.min(#keys, MAX_ROWS) do
	local t = areas[keys[i]]
	table.insert(out, `  {keys[i]}: primitives {t[PRIM]}, no collision {t[NOCOL]}, shadow helpers {t[SHADOW]}`)
end
if #keys > MAX_ROWS then
	table.insert(out, `  ... and {#keys - MAX_ROWS} more areas`)
end

local ids: { string } = {}
for id in meshUses do
	table.insert(ids, id)
end
table.sort(ids, function(a: string, b: string): boolean
	return meshUses[a] > meshUses[b]
end)
local foreign, unreadable = 0, 0
local checked = math.min(#ids, CREATOR_CHECKS)
if checked > 0 and game.CreatorId ~= 0 then
	for i = 1, checked do
		local assetId = tonumber(string.match(ids[i], "%d+"))
		local ok: boolean, info: any = false, nil
		if assetId ~= nil then
			ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, assetId, Enum.InfoType.Asset)
		end
		local creator: any = if ok and typeof(info) == "table" then info.Creator else nil
		if typeof(creator) ~= "table" then
			unreadable += 1
		elseif creator.CreatorTargetId ~= game.CreatorId or creator.CreatorType ~= game.CreatorType.Name then
			foreign += 1
			table.insert(out, `  NOT THE OWNER'S UPLOAD: {ids[i]} used {meshUses[ids[i]]} times, uploaded by {creator.Name}`)
		end
		task.wait(CHECK_PAUSE)
	end
	table.insert(out, `Unique MeshIds {#ids}; creator checked on the {checked} most used: {foreign} not uploaded by the game owner, {unreadable} unreadable`)
else
	table.insert(out, `Unique MeshIds {#ids}; creator check skipped (unpublished place, no meshes, or CREATOR_CHECKS = 0)`)
end

local clean = totals[PRIM] == 0 and totals[NOCOL] == 0 and totals[SHADOW] == 0 and foreign == 0 and unreadable == 0
table.insert(out, if clean then "House-rule scan OK" else "House-rule scan: findings above")
print(table.concat(out, "\n"))
```

What the scan can and cannot prove:

- A MeshPart is not proof of a Blender model. The creator lookup catches the common case, a Toolbox mesh still pointing at someone else's upload, by comparing the mesh asset's creator with the game's owner (`game.CreatorId`, `game.CreatorType`) `[VS]`.
- The lookup cannot work, and the scan says so in its output, when the place is unpublished (`CreatorId` is 0), when asset details are not readable for that mesh (private, archived or moderated assets count as "unreadable", which blocks the OK line), or beyond the first `CREATOR_CHECKS` ids (raise it gradually; the call is rate-limited).
- It gives a false alarm for meshes a teammate uploaded from a personal account to a group-owned game (confirm, then re-upload to the group), and a false pass for a Toolbox or generated mesh that the owner downloaded and re-uploaded. No API can tell how a mesh was authored. The asset manifest from the Blender pipeline (`references/art-pipeline-blender.md`) is the only proof of rule 1; "House-rule scan OK" means no primitive, collision or foreign-upload finding, not certified authorship.
- Not covered: SpecialMesh inside a Part (counted as a primitive), textures and decals, assets inserted at runtime by id, and scripts inside Toolbox models (read those in the security pass).
- On a game built from Parts expect large primitive counts per area. In Level-up mode that output is the input to the house-rule debt track (`references/audit-existing-game.md` §6): replace by area, most-seen first.

Tag the allowed non-solid visuals `NonSolid`: foliage canopies, cables, held tools, viewmodels and transient effect meshes. Nothing else in the world may carry the tag.

## Gate 5: launch (discovery, analytics, LiveOps)

Product and quality

- [ ] Fun within 5 minutes confirmed by strangers; bounce under 60 s measured on a low-end phone.
- [ ] Gates 2, 3 and 4 passed; soak test done.

Monetization and compliance

- [ ] Default product set live with prices read from the API; offer gate tuned through Configs; receipts verified end to end in a test place.

Discovery and metadata

- [ ] Five custom 16:9 1920×1080 thumbnails under 3 MB (2–5 active on Home), each with its own first-minute promise, passing the three gates and 8.5+ on the rubric in `icons-thumbnails-and-store-page.md` §15; icon subject named at 32 px and genre at 64 px (tile test, its §5); title keeps the name inside the first 23 characters; first description sentence summarises the game; genre and supported languages set.
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

- [ ] Read PTR, bounce, D1/D7/D30, co-play, ARPDAU against last week and against the game's own dashboard benchmark (fallback rows: `analytics-and-discovery.md` §Benchmarks).
- [ ] Review the onboarding funnel; fix the earliest step that loses twice its neighbours (`tutorial-and-onboarding.md` §14).
- [ ] Re-run the MicroProfiler and Scene Analysis after each content update.
- [ ] Review safety dashboard reports and ban appeals.
- [ ] Ship the weekly update on the announced day.
- [ ] Check the Performance dashboard by place version after each publish; read the Feedback dashboard for a downvote spike.
- [ ] Every 6 weeks, or after two flat weeks, re-run Gate A and rescore.

## Growth gate: before paid or creator-driven traffic

Detail in `references/growth-and-marketing.md`.

- [ ] Bounce and D1 at or above the dashboard benchmark median (no dashboard benchmark: D1 above the 11% house launch target, which sits just over the 10.3% large-title median); like ratio ≥ 85%; crash rate under 2–3%.
- [ ] Funnels and economy events live; 30-day revenue per new user by source known; max cost per play computed with a stop-loss date.
- [ ] One share link per channel and per creator; creatives are real captures of the game and match the first minute.
- [ ] (HR) No giveaway, Robux or "free" wording in title, thumbnails or description; social rewards stay bonuses after the first win; no restarting countdowns or false scarcity in event marketing.
- [ ] No URLs, invite codes or handles in-game; social links only on the details page; paid creator content disclosed.
- [ ] Engagement-objective spend (for the 250-play gate) has its own budget and is paused at the goal.
- [ ] Soft launch done with "Exclude from recommendations" on: 85%+ of new players reach the first reward within 60 s, no step in the first 3 minutes loses over 15%, median first session 10+ min.
- [ ] Ad and share-link joins tagged through LaunchData; cohort value computed per unique user, not per play.
- [ ] Server size fits current CCU; the loop works with one to three players.

## Sources

This file restates gates defined in the topic references; evidence and source lists live there. Gates 0–5 came from knowledge-base sections 1.12.3, 3.8, 3.10, 4.11 and 5.13; Gate A and the growth gate from `references/audit-existing-game.md` and `references/growth-and-marketing.md`. Rubric pointers and platform facts re-checked on 2026-11-11 (creator docs mirror, commit 7cbffff of 2026-11-10; `MarketplaceService:GetProductInfoAsync` signature read in the engine reference).

- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `skills/quality-score/SKILL.md`, `skills/council-method/SKILL.md`, `commands/audit.md`, `27 Marketing and Growth/Launch Strategy - The First Two Weeks.md`, `Rescuing a Weak Launch - Empty Servers, Low CCU and Relaunch Tactics.md` (read). Source of the evidence-grade, second-opinion, deliverable-score and soft-launch items, rewritten in our own words `[lihfolk]`.
