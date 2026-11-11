# UI screen recipes: sizes, HUD layouts by genre, shop, inventory, settings, rewards, notifications, loading

Build-level recipes for the screens almost every Roblox game ships: what each contains, the numbers at a small phone, the server rule behind it and the failure modes to test. Open it when a screen is about to be designed or built, or when a live screen misbehaves. The look (hierarchy, tokens, construction, critique) is in `ui-design-figma.md`; motion and reward sequences in `ui-motion-and-feedback.md`; engine rules, zones and the presenter in `ui-input-crossplatform.md`; purchase and data flows in `data-and-purchases.md`. Examples to study before building: `visual-library/ui-hud.md` (HUDs by genre and platform) and the matching section of `visual-library/ui-screens.md` (named in each recipe); bundled sheets 01–04 (`visual-library/reference-sheets.md`).

Tags: `[official]` Roblox docs, `[community]` DevForum, GitHub and third-party craft writing, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0, rewritten; where it clashes with the house rules, the house rules win), `[VS]` version-sensitive, `[house]` house rule or estimate.

**Fast routes** (the full table with sheets and library rows: `ui-design-figma.md` §Fast routes). From this file: redesign one screen → §1, §3 and that screen's section (§5–§12); new HUD → §1, §2, §4; phone layout fix → §1, §4; critique → the Level-up table. Role and size names (`Primary`, Caption 14) are defined in `ui-design-figma.md` §3–4.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Pick the HUD layout for your genre (§2) and place read-1 elements only. (2) Build one window from the shared anatomy (§3). (3) Give every claim and buy button the pending state. (4) Run each recipe's failure tests on a 667×375 emulator. | Virtualised lists, notification kinds as data, slot tables |
| Intermediate | HUD slot table; every recipe the game needs with its server rule; toast queue with merge rules; loading watchdog; state matrices drawn in Figma first | Automated overlap tests |
| Expert | Notifications as data with priority and preemption; virtualised inventory with index-based gamepad selection; automated overlap and tap checks calling the real placement code; per-screen rubric scores tracked per release | Nothing |

## Contents

1 Patterns with sizes · 2 HUD layouts by genre · 3 Shared window anatomy · 4 HUD · 5 Shop · 6 Inventory and collection · 7 Settings · 8 Codes · 9 Daily rewards · 10 Rebirth · 11 Notifications · 12 Loading screen · Level-up table · Review gate · Sources

## 1. Patterns with sizes

px at `Phone-S` (800×360); the scale column is a fraction of screen height (H) or width (W). `[house]` unless tagged; "observed" conventions come from one community teardown of about 20 hit games (screenshot-based, one author) `[community]`. Design every screen and state before building any: HUD, shop, inventory, item detail, reward popup, toast, offer card, quest tracker, settings, confirm dialog, loading screen, custom proximity prompt, world labels, focus ring; plus empty, locked and error states for every list.

| Element | px at Phone-S | Scale | Placement and rule |
|---|---|---|---|
| Currency readout | icon 28–32, number 20; a second currency icon 22, number 16 | 0.08–0.09 H | Top-left under the top bar. Icon + outlined number, no panel `[community]`; counts up, never snaps |
| Menu buttons | 48–56, gap 8 | 0.13–0.155 H | One home edge; 4–6 at most, the rest behind `More`; red count badge only when something is claimable |
| Primary action | 0.8–1.0× the jump button (70 px when the screen's short axis is ≤ 500 px, else 120 px `[official][VS]`) | read at runtime | Placed from the live `JumpButton` once it `IsLoaded` `[official]`; never by screen percentage |
| Touch target floor | 44×44, 48 on the HUD | 0.12 H | 44 is Apple's figure, 48 dp Google's; the docs cite a 9 mm WCAG target `[official]`; Epic's mobile guidance also says 44 `[community]` |
| Objective / timer | height 32–40 | 0.10 H | Top centre; read-only (hardest thumb reach); collapsible if it grows `[community]` |
| Quest tracker | width ≤ 220 | ≤ 0.28 W | Right edge under the top bar; 1–3 lines with `101/500`; folded by default on phones |
| Toast | height 36–44 | 0.11 H | Top centre under the objective; ≤ 2 visible on `Phone-S`; never a modal |
| Window | ≤ 736×308 | ≤ 0.92 W × 0.86 H | Centred; header 44–48; close top-right ≥ 44; opens in ≤ 0.25 s; built inside a fade group 20 px larger on every side (§3) |
| Shop card | Phone: 160×236 in one horizontal row (featured 200×236), next card cut off at the edge; tablet and desktop: a 3–4 column grid | 0.66 H tall on phones | Art 104, name 16, one-line benefit 14, full-width native price button 48 high (price 20); the cut-off card or the top of the next row shows that the list scrolls. Fits `Phone-S`: §5 |
| Inventory cell | 64–72, columns computed from width | 0.18–0.20 H | Rarity = colour + name bar or pips; count bottom-right; undiscovered = silhouette + `??` with `162/284` `[community]` |
| Item detail | n/a | n/a | Side pane on wide screens; a pushed page with Back under about 700 px width |
| Reward popup | item 96–128, window ≤ 0.6 H | n/a | Centre; one Claim button; batch many rewards into one summary (`ui-motion-and-feedback.md` §5) |
| Offer card | ≤ 25% of the screen | n/a | Safe-area corner outside the thumb zones, an X, never stacked; timing and cadence in `monetization-and-policy.md` §Offer and shop playbook |

- Put information in the world when it belongs to an object (price, rate, timer on a `BillboardGui`) `[community]`.
- Print the key on the button on PC (`[E]`); the same action is a round touch button on phones `[community]`. `InputActionLabel` does this from an `InputAction` without code (Studio beta, not yet publishable `[official][VS]`); until release use `UserInputService:GetImageForKeyCode`.
- **Conflict:** the teardown lists strikethrough prices, "% OFF" tags and urgency countdowns as common in hit games. House rule 3 overrides: a timer only for a real state, a discount only against a price really charged, never a countdown that restarts.
- **Conflict:** hit simulators run denser HUDs than the 7-group cap (`ui-design-figma.md` §1), and Epic's mobile guidance says 5–6 active controls `[community]`. Count groups (one menu column = one group) and hide secondary buttons behind `More`. Element count tracks tempo in shipped games: 3 in a calm game, 6–8 in action games, 10 or more groups in desktop simulators, which is where a separate phone arrangement becomes mandatory (`visual-library/ui-hud.md` #25; #21, #7, #23; #5, #10).

## 2. HUD layouts by genre

Read-1 elements and zone layout per archetype `[house]`, built on the zone map in `ui-input-crossplatform.md` §Mobile layout. Element lists per genre are owned by `genres/<genre>.md` (UI section); this table says where things go and what never to do. Top centre is status, bottom corners are thumbs, the centre third stays clear except for short feedback.

| Archetype (genre files) | Read 1 | Layout | Never |
|---|---|---|---|
| Collect and upgrade: simulator, tycoon, pet collection, plus-one, fishing | Loop verb button, capacity or progress bar, main currency with rate | Currency top-left; next-goal chip top centre; menu on the right edge above the jump zone (or one row top-right); verb left of jump; prices and timers in the world | A panel behind numbers; more than one row of boost pills; menu buttons low on the left, inside the stick's touch area |
| Melee and ability combat: battlegrounds, RPG, dungeon | Own health, 3–4 abilities with cooldown sweeps, target or boss health | Health bottom centre or top-left; abilities on an arc around the jump button, largest nearest the thumb; boss bar top centre; kill feed top-right, small | Menus reachable mid-fight in the thumb arc; damage numbers over the crosshair line; more than 4 ability buttons on a phone |
| Shooter | Crosshair, ammo, health, fire button | Crosshair centre (the only centre element); fire and aim in the right thumb zone, placed from jump; ammo beside the fire button; score and timer top centre; hit markers and damage direction around the crosshair | Anything opaque within 15% of the centre; ammo in a boxed panel |
| Obby, tower, platformer | Stage number, timer in timed modes | Stage and progress top centre; skip button appears only after repeated failure; everything else behind one menu button | Any element in the lower-centre landing sight line; persistent side columns |
| Racing, driving | Position, lap, speed | Custom driving controls replace stick and jump: steer left thumb, throttle and brake right thumb; position and lap top-left; speed bottom centre or beside the throttle; minimap top-right | Reusing the on-foot HUD in the car; speed as small text |
| Horror, escape | Nothing persistent; the threat is in the world | Diegetic first (battery on the flashlight); stamina and objective fade in on change and out after 2–3 s; interaction through prompts | Bright saturated UI; a quest list that explains the threat |
| Round-based: party minigames, social deduction, sports | Round timer, objective line, own role or team | Timer and objective top centre; role or team as a colour band plus icon; one context action button; spectate bar after elimination | Showing lobby menus during a round; team by colour alone |
| Tower defense, strategy | Lives, wave, cash, tower hotbar | Wave and lives top centre; cash near the hotbar; tower cards along the bottom centre between the thumb zones; placement mode hides the rest of the HUD | Cards smaller than 56 px; confirm dialogs for each placement |
| Social, roleplay, dress-up | The avatar and other players (the HUD yields) | A short tool row (emotes, phone, catalogue) bottom centre or right edge; chat kept clear top-left; large full-screen editors with tabs | A dense HUD; windows that hide the avatar being edited |
| Survival, crafting | Needs bars, hotbar | Needs as small bars top-left, or bottom centre above the hotbar; hotbar bottom centre; day clock top centre; crafting opens at stations | More than 4 needs bars; inventory as the only way to see health |

- Bottom-centre rows need 12–16 px above the safe edge: young players hit bottom-edge buttons by accident (Smashing Magazine's children's guide `[community]`), and the home indicator lives there.
- Contextual HUD beats a full HUD: swap buttons by state (the docs' ball-possession example `[official]`: the same three thumb positions change verb, `visual-library/ui-hud.md` #8), show ability bars only in combat zones, hide the HUD in placement and photo modes.
- Patterns that hold across the HUD library (`visual-library/ui-hud.md`, "Patterns seen"; numbers are its rows) `[community]`:
  - One home edge of icon + caption buttons survives a phone (#3); two edges, or a left column, meet the thumbstick (#4, #10, #11, #12).
  - A hotbar owns the bottom-centre band between stick and jump: numbered slots with icons, the price under each where it sells (#17, #7, #4). Text-only slots do not read at phone size (#2, #6).
  - Capacity and progress are written as have/need beside the bar (`80/800`, `122/160`), never as a bar alone (#11, #24, #13).
  - Keyboard letters printed on buttons mark a desktop-first HUD: on touch they become icons (#7, #12, #15 against #21, #8).
  - A timer on the HUD states a real remaining time for a real event (#3, #1).
- Pictures per archetype: `visual-library/ui-hud.md` §1 (hit Roblox games judged at phone size), §2 (Roblox HUDs by genre), §3 (shipped games outside Roblox whose layouts transfer).

## 3. Shared window anatomy

Header (icon, loud title, the destination's colour) → categories → scrolling content → optional footer (summary, `Claim all`, timer). On landscape phones the categories are a side rail, because height is the scarce axis (a 44 px tab strip costs 12% of a 360 px screen); a top strip suits portrait and wide screens. The header carries identity plus the one live fact of that screen (restock timer, balance, capacity, season end) and the close button, nothing else; tabs are icon + word, six at most (`visual-library/ui-screens.md` #1, #8, #35, #38; #6, #9, #24). Close top-right, the same component everywhere, also on gamepad B (Escape always opens the Roblox menu and cannot be the close key). One presenter, one open window; the window sits in a transparent `CanvasGroup` 20 px larger on every side, so the fade does not clip the close overhang, outer stroke or shadow (`ui-design-figma.md` §6 Window). A full-screen dim (black at 0.5–0.6 transparency) fades with the window, blocks input behind it and is the tap-outside-to-close target. The primary action is the brightest thing on the screen, one per card at most. On phones an open window hides the HUD. Navigation is at most two levels deep (Epic's mobile guidance `[community]`). `[lihfolk]`

**Claim and buy buttons share one state machine**: available → pending → done, or locked with the reason. Between the tap and the server's answer (50–500 ms, seconds on a bad connection) the button is non-interactable and shows progress, or a second tap sends a second request. The server re-checks everything and records the claim before it pays out. `[lihfolk]`

## 4. HUD

- Agree the zone map first (§2), then the three reads (`ui-design-figma.md` §1). One primary action, visibly the largest element, positioned from its bar or the jump button.
- Stackable elements (boost row, quest tracker, boss bar, toast lane, tutorial banner) are rows in one slot table (edge, order, gap) placed by one layout function. HUDs break by accretion: each hand-placed element looks fine alone and collides at 667×375 mid-fight. `[lihfolk]`
- Show rates beside totals where they drive decisions (`$12.4K/s`). Shown numbers are the true ones: every multiplier included, odds equal to the odds rolled.
- Progressive disclosure: during the tutorial show only the button the current step needs; show later features as locked with their condition ("Unlocks in Zone 4") instead of hiding them; badge only when something useful can be done now. `[lihfolk]`
- Phone: navigation at most 2 columns wide; quest tracker folded by default and at most two rows under about 420 px height; bars and captions enlarged so drawn text stays ≥ 12 px. `[lihfolk]`
- Test: zero overlapping rectangles at every test viewport in every scenario (idle, combat, boss bar, tracker open, tutorial, chat open). A feature reachable only from a hidden HUD element is a broken feature.

## 5. Shop

- Sections with headers: passes, products (currency, boosts), bundles. Card: square art (`ScaleType = Fit`), name, one-line benefit ("2× Cash for 10 min"), native price button. Draw the eye to one card per section with size and extra padding, not with a false label (the docs' bundle example uses exactly that `[official]`).
- Phone layout that fits `Phone-S` (sheet 03) `[house]`: window 736×308, header 48 (title 24), padding 12, so the body is 236 px tall. Category rail 128 wide on the left: tabs 48 tall, gap 8, icon + one word in 14, at most four. Cards in one horizontal `ScrollingFrame` 572 wide: featured 200 + two of 160 + gaps of 8 leave 28 px of the fourth card showing. Card inside 12 px padding: art 104, name 16, benefit 14, price button 48 anchored to the bottom. Four text sizes on the screen: 24, 20, 16, 14.
- The Robux icon is a private-use character the engine draws: `utf8.char(0xE002)`, or `"\u{E002}"` in a script string (Premium is `0xE001`). It is monochrome and takes `TextColor3` or a RichText colour; there is no character for the green shaded logo. The Studio Text field does not parse `\u{...}`: set it from code or paste the character. It is not in the docs: the source is a staff reply in the release notes for version 541 (2022) `[official][VS]`; check it on a device in your chosen font. The `BuilderIcons` font path is undocumented: do not ship on it (`ui-design-figma.md` §5).
- Prices come from `MarketplaceService:GetProductInfoAsync`, never hard-coded; the button only opens the prompt. The grant happens in `ProcessReceipt` (products) or after a server ownership check (passes); the card flips to "Owned" or "Active 12:41" when the server says so, never when the prompt closes.
- Unaffordable soft-currency items: the button takes the disabled look and states the shortfall ("Need 50 coins"); a red price is the docs' own example of a consistent rule `[official]`, usable only where red text measures 4.5:1 on its plate, never on a green fill (`ui-design-figma.md` §3).
- Phone cards about 1.3–1.4× their desktop size with fewer columns `[lihfolk]`. Keep the price stroke thin enough that digit holes stay open; an unreadable price costs sales.
- Say scope precisely ("this server" on a server-wide boost). Live 3D previews (`ViewportFrame`) only in the featured slot or detail pane.
- House rule 3: no countdown that restarts, no strikethrough without a real former price, close button never hidden or delayed. Paid random items show full odds read from the config the server rolls from, behind the PolicyService gate (`monetization-and-policy.md`). Children do not tell promotion from content `[community]` (NN/g): label paid things as paid, with the Robux icon before every Robux price.
- Failure modes: owned state granted from the client; double prompts (no pending state); "Best value" on something that is not.
- Examples: `visual-library/ui-screens.md` §1. What the strong ones share: the price is the button, in a colour reserved for that currency, and a card sold for two currencies shows two buttons (#2, #12, #10); currency packs grow their art with the tier and the top tier gets a larger card, not a louder colour (#10, #9, #5); rotating stock states the real time left (#1, #17, #18); the materials come from the game's world (#1, #4, #7). Several hit shops in that file show struck-through prices and stock counters: its notes flag them, and house rule 3 decides.

## 6. Inventory and collection

- Stack duplicates first: 900 copies of 40 item types are 40 entries. Show the cap (`480 / 500`).
- Under about 100 entries use a plain grid; above about 300, or unbounded, virtualise. A card is 10–20 instances, so 1,000 cards are about 15,000 instances. `[lihfolk]`
- The view is a filtered, sorted array of item keys; cells are windows onto `view[index]`. State (selected, new, equipped) lives in data keyed by item, never on the cell. Connect `Activated` once per cell and read its bound key at click time. `[lihfolk]`
- Search with `string.find(name, query, 1, true)` (plain match: a typed `%` or `[` otherwise throws), debounce 0.15–0.25 s, precomputed lower-case names. End every sort comparator with a unique tiebreaker: `table.sort` is not stable. `[lihfolk]`
- Scroll position: reset on search, filter or sort change; keep on count or state change; for new items show a "1 new" pill instead of jumping.
- Gamepad selection is a data index, not an instance, or recycled cells keep the focus ring on the wrong item.
- Drag and drop `[lihfolk][VS]`: `UIDragDetector` with a custom response style, a ghost on a top-level drag layer (never inside the clipped grid), drop target from `GetGuiObjectsAtPosition`, the move sent as a server-validated intent. Drag detectors support gamepad selection mode (`SelectionModeDragSpeed`, `SelectionModeRotateSpeed` `[official]`); a September 2026 regression that broke it was reverted by staff and confirmed fixed on 2026-11-01 `[community]`. Dragging with a stick is still slow: always offer select-then-place.
- Icons are pre-rendered images; preload the first screen's icons and back each cell with a rarity-tinted plate so late textures do not pop.
- Empty and locked states are designed, and say why and what to do: an empty box with two friendly lines and its actions, an undiscovered entry as a silhouette with `55 / 134 Discovered` under the grid (`visual-library/ui-screens.md` #27, #23). Examples: its §2 (inventories, collections, loadouts) and §3 (trading: both sides named, a status line between them, one Ready button, #32).

## 7. Settings

- Rows: label, optional one-line description, one control. Groups: Audio, Graphics, Controls, Accessibility. Category rail and footer fixed, page scrolls.
- Minimum set: music and SFX volume, effects quality, camera shake, reduced motion (default from the platform setting), hide other players' effects, UI scale, plus what `accessibility-and-player-qol.md` requires.
- Every control ≥ 44 px tall drawn; the whole row is the tap target for toggles. Sliders show the number, follow the finger directly (no tween while dragging) and preview live. Gamepad: left/right steps sliders and segmented choices, shoulder buttons switch category. `[lihfolk]`
- One saving model: auto-save ("Changes save automatically": apply locally at once, send after a few idle seconds or on close) or explicit Apply/Reset. Never mix them, never write a DataStore per slider tick. `[lihfolk]`
- Examples: `visual-library/ui-screens.md` #55 (each toggle an ON / OFF pair, coloured and worded) and #56 (rows mocked with the longest setting name). No settings screen from a current top Roblox game was found in a viewable form.

## 8. Codes

- One instruction line, one labelled text field (about 24 characters), one Redeem button, one inline result line. Errors appear at the field, not in a corner toast.
- Client trims whitespace and shows "Checking…" with the button disabled; the server normalises case, checks validity, expiry and one-use-per-player, and rate-limits attempts (for example 5 a minute). The code list never ships to the client. `[lihfolk]`
- Enter submits (`FocusLost` with `enterPressed`). Distribution policy: `growth-and-marketing.md` §8. Examples: `visual-library/ui-screens.md` #57 (the whole recipe in one panel), #5 (the code field inside the store header).

## 9. Daily rewards

- Seven cards, the last visibly larger. States: claimed (tick, dimmed), today (claim), later (locked). One-tap claim, a badge on the HUD entry while a claim is ready, countdown text updated only while the window is open.
- Reset on a fixed clock (UTC midnight), not 24 hours after the last claim, which drifts later each day `[lihfolk]`.
- **Conflict:** LihFolk treats "does a missed day reset the streak?" as a design choice to state on screen. House rule: it never resets. Use the cumulative calendar from `liveops-quests-retention.md` and no join pop-up.
- Alternative without a calendar: playtime gifts in tiers with one interval banked across a break `[lihfolk]`.
- Examples: `visual-library/ui-screens.md` §4 (#34 today's card largest with a tick once claimed; #43 the seven-day anatomy as a stock template, with a streak rule this skill rejects); quests and passes there follow one anatomy (#35–#39), owned by `liveops-quests-retention.md`.

## 10. Rebirth / prestige

- Current and next tier side by side with their multipliers; a have/need bar with a percentage; one line stating what resets and what stays.
- Two-step confirmation: the first tap turns the button into a `Danger` "Tap to confirm" for about 3 s, or opens a one-line dialog `[lihfolk]`. On gamepad use hold-to-confirm.
- A paid skip, if any, is a separate, clearly priced button (never in competitive modes). Maths: `economy-and-progression.md`. Nearest example: the prestige panel in `visual-library/ui-screens.md` #74 (what was gained, what unlocked, a bar to the next rank); no hit-game rebirth screen was found in a viewable form.

## 11. Notifications

Choose the channel before the look `[lihfolk]`:

| Channel | Lifetime | Use for | Never for |
|---|---|---|---|
| Floating number | 0.6–1.2 s | Result at the point of action (`+5`) | Anything that must be read |
| Toast | 2.5–7 s | Item obtained, quest progress, friend joined | Errors needing action; celebrations |
| Centre banner | 2–4 s, queued | Level up, rare drop, zone unlocked | Routine events |
| Inline status | While true | "Not enough coins" on the buy button, "Full" on the backpack | Unrelated events |
| Modal | Until dismissed | Irreversible choices | Anything a toast can carry |
| Badge / inbox | Persistent | Anything the player must act on later | Real-time feedback |

- The nearer a message is to its cause, the less it needs to be a notification; anything that must be acted on must persist.
- Kinds are data: `{ channel, priority 1–4, merge rule, merge window, minimum time, sound }`. The server sends a kind and parameters, never English text; the client formats, localises and merges. `[lihfolk]`
- Toast queue: 2 visible on `Phone-S`, 3 on larger phones and tablets, 4–5 on PC; at most 8–10 waiting; drop stale ones. Lifetime `clamp(1.6 + 0.3 × words, 2.5, 7)` s, paused while touched. `[lihfolk]`
- Merge rules: `sum` ("+250" five times → "+1,250"), `count` ("Iron Ore ×3"), `replace` ("Quest 4/10"), `none`. Cap lifetime extension so a trickle cannot pin a toast. A full stack lets a higher priority evict the oldest, lowest one. Floating numbers: pool about 12, merge same-kind within about 0.5 s. `[lihfolk]`
- Banners: one centre slot owned by one module, at most 4 waiting, each shortened to about 1.2 s when more than two wait; gated during the tutorial, a cutscene, the death screen or an open window. `[lihfolk]`
- Placement: top centre or top-right, never bottom-right on phones. Sound only for priority 3–4, one shared soft tick otherwise, at most one per 0.5 s.
- Stress test: a debug command that fires every kind 10 times in one frame, then watch for 60 s.
- Examples: `visual-library/ui-screens.md` §7 (reward summaries, level-up and results cards; #75 toast card anatomy and stacking).

## 12. Loading screen

- A `ReplicatedFirst` LocalScript shows its own ScreenGui (`ScreenInsets = None`, high `DisplayOrder`) and calls `RemoveDefaultLoadingScreen()`. Preload only what the first screen needs: loading art, HUD fonts, first-screen icons (`ContentProvider:PreloadAsync`).
- Teardown is one idempotent function; nothing can re-show the screen. A watchdog removes it after a fixed time (15–20 s `[house]`) and logs why. Every wait in the ready check has a timeout and never waits on an instance streaming may not have sent. A watchdog firing on more than about 1% of joins means the ready check waits for the wrong thing. `[lihfolk]`
- Fade out in about 0.3 s. No offers, no purchase prompts (house rule 3). Join pipeline and budgets: `performance.md`. Examples: `visual-library/ui-screens.md` §6 (#48 loading → title → select in one style; #65 a logo that fills by tweening a `UIGradient` offset).

## Level-up: screen symptoms → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| HUD elements overlap on small phones mid-fight | Hand-placed stackable elements | Slot table and one layout function (§4); test at 667×375 in every scenario |
| Double purchases or double claims | No pending state | Shared state machine (§3) |
| Card shows "Owned" but the item is missing | Owned state set from the client when the prompt closes | Flip on the server's answer only (§5) |
| Players lose progress to an accidental rebirth | One-tap irreversible action | Two-step or hold-to-confirm (§10) |
| A wall of identical toasts; toasts arriving a minute late | No merging, unbounded queue | Kinds with merge rules, capped queue, stale drop (§11) |
| Celebration banner over the death screen or tutorial | No popup gate | One centre slot with gating rules (§11) |
| Loading screen never leaves for some players | Ready check without a timeout, or two teardown paths | Idempotent teardown plus watchdog (§12) |
| Inventory stalls or the focus ring lands on the wrong item | Thousands of live cells; selection stored on recycled instances | Virtualise; selection as a data index (§6) |
| Daily reward complaints after a missed day | Streak reset | Cumulative calendar (§9) |

## Review gate

- [ ] HUD layout follows the genre's zone layout; read-1 elements only persistent; slot table for stackable rows; zero overlaps at six viewports in every scenario.
- [ ] Every window uses the shared anatomy and one close component; gamepad B closes it; the HUD is hidden on phones while it is open.
- [ ] Every claim and buy button has available, pending, done and locked states; the server decides and records before paying out.
- [ ] Shop prices fetched, never hard-coded; nothing false, restarting or hidden (house rule 3); odds shown where required.
- [ ] Inventories over a few hundred entries virtualised; comparator has a unique tiebreaker; drag and drop has a non-drag alternative.
- [ ] Notification burst test passed; banners gated; loading watchdog logs under about 1% of joins.
- [ ] Each recipe's listed failure modes were tested on a 667×375 device or emulator.

## Sources

Accessed 2026-11-11 unless noted.

- `Roblox/creator-docs` mirror, commit `7cbffff` (read): `production/game-design/ui-ux-design.md`, `tutorials/curriculums/user-interface-design/choose-an-art-style.md`, `ui/position-and-size.md`, `ui/ui-drag-detectors.md`, class reference `InputActionLabel`, `UIDragDetector`: https://github.com/Roblox/creator-docs
- Roblox `PlayerModule` source, client 0.747, via https://github.com/MaximumADHD/Roblox-Client-Tracker (re-read 2026-11-11: `ControlModule/TouchJump.lua`, `minAxis <= 500` gives the 70 px jump button, otherwise 120 px)
- Roblox staff announcement (read): InputActionLabel Studio beta https://devforum.roblox.com/t/4779420 · Release Notes for 541, staff reply #5 on the Robux (`\u{E002}`) and Premium (`\u{E001}`) characters (read) https://devforum.roblox.com/t/1940089/5; community list of the same characters (read) https://devforum.roblox.com/t/2175425; the Studio Text field ignoring `\u` escapes (read) https://devforum.roblox.com/t/2393765
- Epic, "Designing for Mobile in Fortnite" (read) https://dev.epicgames.com/documentation/fortnite/designing-for-mobile-in-fortnite
- NN/g, "Children's UX: Usability Issues in Designing for Young People" (read) https://www.nngroup.com/articles/childrens-websites-usability-issues/ · Smashing Magazine, "A Practical Guide To Designing For Children" (read) https://www.smashingmagazine.com/2024/02/practical-guide-design-children/
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault) (read): `05 UI and UX/` HUD Design; Menu Archetypes - Shop Settings Codes Rewards; Notification and Toast Systems; Virtualized Lists and Large Inventories; Settings Menu Design for Roblox; Drag-and-Drop Inventories and Sliders with UIDragDetector (TL;DR and patterns); `56 Field Notes/` Centre-Screen Announcements, Streaming Joins and Loading Screen Teardown
- https://github.com/MarkRuiz00/RbxUiStudio (read 2026-11-10: `juegos/README.md`, `juegos/pet-simulator-99.md`, `estilos/simulator.md`): source of the "observed" conventions
- `references/genres/*.md` UI sections (read): element lists per genre
- DevForum bug report (read, with the staff replies of 2026-10-29 and 2026-11-05): UIDragDetector in gamepad selection mode https://devforum.roblox.com/t/4877569
- `visual-library/ui-hud.md` and `visual-library/ui-screens.md` (read): the row numbers cited above
