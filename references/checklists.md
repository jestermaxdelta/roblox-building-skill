# Consolidated checklists and ship gates

Collected from knowledge-base sections 1.12.3 (design review), 3.8 (compliance), 3.10 (launch), 4.11 (engineering anti-patterns) and 5.13 (pre-launch performance and content). Each topic reference file ends with its own detailed gate; this file is the short version to run at each phase. Items marked (HR) enforce a house rule.

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
- [ ] No progress gated on likes, favourites or group joins.
- [ ] Thumbnails and video follow policy (no spoken audio, real footage or ad text in video).

## Gate 4: performance and content (HR)

- [ ] Low-end Android (2–4 GB) ≥ 30 FPS in the busiest scene; mid-range about 60; no spikes over about 50 ms in a 2-minute capture; 10–15 minute thermal test passed.
- [ ] Server heartbeat about 60 Hz with a full server; memory < 50% of (6.25 GiB + 100 MiB × max players) and flat over a 1-hour soak.
- [ ] Draw calls < 1,000, triangles < 1 M in the worst view; duplicate-MeshId audit clean.
- [ ] Streaming on with recommended settings; works at `StreamingTargetRadius = 64`; interactive models Atomic; `RequestStreamAroundAsync` before teleports; no LocalScript indexes Workspace without a timeout or tags.
- [ ] All static geometry anchored; mechanisms anchor only the root; no `PreciseConvexDecomposition` except approved doorways; non-colliding meshes Box; collision groups registered once.
- [ ] **Every visible object is a Blender model and blocks players and NPCs**; the scan below passes; walk-through test passes; Terrain only with explicit owner approval.
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

Tag foliage leaves, VFX ribbons and other deliberately non-solid visuals `NonSolid`.

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
