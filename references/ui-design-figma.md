# UI design in Figma, implementation in Roblox

How to design a Roblox HUD, shop, inventory and reward flow in Figma (through the Figma MCP), bring it into Studio as native instances plus a small set of images, and make it look authored instead of generic. Open it when designing UI for a new game, re-skinning a live one, or when a UI audit says "looks default". Engine rules (insets, input, gamepad, accessibility) live in `ui-input-crossplatform.md`; this file is the design and hand-off layer. Tags: `[official]` Roblox docs, `[community]` forum/GitHub practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0, rewritten), `[VS]` version-sensitive, `[house]` house estimates. The file is style-agnostic: it gives a method for building a game's own design system, not a look to copy.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Read "The one rule of the pipeline". (2) Fill the token table for your game: 6 colour roles, 2 fonts, 1 radius, 1 outline. (3) Design the HUD and one window at the `Phone-S` frame over a real screenshot. (4) Build them from the HUD and Shop recipes with the motion tokens as given. (5) Run the polish checklist. | Frameworks, StyleSheets, springs, converters, virtualised lists |
| Intermediate | Theme and Motion modules with no value outside them; the component state matrix (pressed, disabled, pending, gamepad-focused); every screen recipe your game needs; 9-slice and tinted bases; an asset manifest; the six test viewports; reduced-motion variants | Automating the Figma round trip |
| Expert | Regenerate builders from Figma instead of hand-editing; an automated audit with a score per screen; interruption-safe, distance-scaled motion and springs; notifications as data with merge and preemption; virtualised inventories with index-based gamepad selection; measured budgets in `ui-input-crossplatform.md` §UI performance | Nothing: read the conflict notes and re-verify every `[VS]` |

Terms used below: a **token** is a named design value (a colour role, a size, a duration) stored once and referenced everywhere. **9-slice** stretches an image's edges and centre while keeping its corners fixed. A **presenter** is the one module that opens and closes windows. **Virtualising** a list means creating only the visible cells and recycling them as the player scrolls.

## Contents

The one rule of the pipeline · Design system and tokens · Method: from brief to design system · Frames and scale · Screen inventory · Patterns with sizes · Screen build recipes (HUD, shop, inventory, settings, codes, daily rewards, rebirth, notifications, loading screen) · Motion spec · Figma MCP workflow (px → Roblox, mapping gotchas) · Export and import settings (converters) · Theme module · Generic-UI tells · Polish checklist · Level-up table · Review gate · Sources

## The one rule of the pipeline

**Structure, layout and text are native; artwork is images.** `[community]` Roblox draws rectangles and rounded rectangles with a fill, a gradient, strokes and a drop shadow. Anything else is a PNG.

| Build natively (Frame, TextLabel, layouts, modifiers) | Export from Figma as PNG (ImageLabel/ImageButton) |
|---|---|
| Rect / rounded rect / circle with flat or linear-gradient fill, one border, drop shadow | Non-rectangular shapes: ribbons, shields, stars, speech tails, slanted tabs, boolean shapes |
| Every label, price, counter, description (crisp, scriptable, localisable) | Multi-layer buttons (bevel + lip + sheen + inner shadow), textured panels, illustrations, item/currency/rarity icons, logo |
| Containers, lists, grids, scrolling | Inner shadow, layer/background blur, blend modes (Roblox has none), masks, dashed or stacked strokes |
| Auto layout → `UIListLayout` + `UIPadding` | Stylised title text in a font Roblox lacks (titles only; never body or numbers) |

- Typical button: `ImageButton` (9-sliced body art, no text) → child `TextLabel` (price, native) → child `ImageLabel` (currency icon).
- `UIStroke` follows the box or the glyphs, never an image's alpha: bake icon outlines into the PNG, in white so `ImageColor3` can tint. `[community]`
- `[VS]` Newer modifiers shrink the image list but several are still beta: `UIShadow` (some features beta), per-corner `UICorner` radii (beta flag "New UI Capabilities"), `UIStroke.StrokeSizingMode`/`BorderStrokePosition`/`BorderOffset` (Improved UIStrokes beta), radial/elliptical/conical `UIGradient` (Upgraded UIGradients beta). Each is flagged beta in the class reference `[official]`; beta properties are reported not to render outside Studio `[community]`: check Studio's beta list before relying on one, and keep a 9-slice fallback.

## Design system and tokens

Define tokens once as Figma variables and text styles, mirror them in a Luau theme module (below). No hex value or pixel size appears outside the theme.

| Token group | Contents | Rule |
|---|---|---|
| Colour roles | `Primary` (confirm/buy), `Premium` (Robux), `Danger` (close/destructive), `Info`, `Surface`, `SurfaceAlt`, `Ink`, `InkMuted`, `Outline`, rarity ladder | Limit the colour theme to key information `[official]`; one accent per screen for the primary action; colour means function, not decoration `[community]` |
| Rarity ladder | Common grey → Uncommon green → Rare blue → Epic purple → Legendary gold → Mythic pink/red `[community]` | Players read the ladder before text; always pair with a label or icon (never colour alone) `[official]` |
| Type scale (phone frame px) | Display 28–32, Title 22–24, HUD number 18–20, Body 16, Caption 14 (floor) `[house]` | One display family + one body family. Roblox-native: `FredokaOne`, `LuckiestGuy`, `Bangers` (display); `BuilderSans*`, `Montserrat`, `Nunito` (body) `[official]`. Two families plus weights is enough; each extra family is another download and another set of metrics `[lihfolk]` |
| Spacing | 4 / 8 / 12 / 16 / 24 | 8 px grid; gaps ≥ 8 px between touch targets |
| Radius | S 6, M 10, L 16, Pill | One radius family per game |
| Stroke | Thin 2, Regular 3, Text 2–3; one near-black outline colour | Outline text that sits on the 3D world or on texture `[official]` |
| Depth | Darker duplicate under the face, offset 4–6 px (button lip), 8–10 px (cards) `[community]` | Press state sinks the face into the lip |
| Motion | Named tokens only (`press`, `release`, `enter`, `exit`, `move`, …): full table in Motion spec | Spatial motion becomes a fade or colour change when `GuiService.ReducedMotionEnabled` `[official]` |

- Fonts `[VS]`: only `Enum.Font` families and Creator Store font families (`FontFace`) render as text. No evidence was found in the docs for arbitrary font upload. Pick the Roblox family first, then find its Figma equivalent, not the reverse. The `Gotham*` enum values have been removed and now render Montserrat `[official]`: old kits that say "GothamBlack everywhere" get different metrics, so name the family that really renders (`Font.fromName("Montserrat", Enum.FontWeight.Heavy)`). Fonts outside the client load on first use and can flash a fallback face: preload the HUD's fonts during loading `[lihfolk]`.
- Text outlines `[lihfolk]`: a glyph stroke also grows inward and closes the holes of 0, 6, 8, 9, a and e. Keep `UIStroke.Thickness` at or below about 7% of the rendered text size for rounded heavy fonts (2 px at 28 px text) and about 8–12% for geometric fonts with open counters. Scaling the label up does not help, because `UIScale` scales the stroke too. Test string: `10 20 60 80 88 00 Fast` at the smallest phone size over the real background.
- Numbers `[lihfolk]`: 3 significant figures when abbreviated (`4.62K / 7.40K`), thousands separators below the first tier (`9,840`). Strip trailing zeros only after a decimal point (a real shipped bug showed 160M as "16M"), and re-check the tier after rounding so 999,950 does not print as "1000K". Ticking counters need a fixed-width, right-aligned label or tabular digits, or the layout jitters.
- Contrast: 4.5:1 body, 3:1 large text and icons (see `ui-input-crossplatform.md`). Test over a gameplay screenshot, not over a grey canvas.
- Young audience: icons before words, loud titles, big numerals with suffixes (`12.5K`, `3.4M`), one obvious next action per screen. `[community]` No rigorous evidence for exact sizes for ages 8–12 was found; playtest with real kids.

## Method: from brief to design system

The skill ships no visual style. Each game derives its own; the method is the same every time.

1. **Brief with pictures, not adjectives** `[lihfolk]`. Name one style direction in a phrase (for example "chunky toy", "flat esports", "paper craft", "diegetic minimal"), attach 3–5 reference screenshots, and write what to take (palette logic, shape language, hierarchy) and what to leave (logos, characters, exact art). Never trace or ship reference art.
2. **Tie it to the 3D art bible.** Sample the outline colour, two accents and the surface colour from the Blender style bible (`art-pipeline-blender.md`) so UI and world read as one product.
3. **Turn the direction into tokens** (table above), then into components. Nothing else is allowed to carry a raw value.
4. **Stress-test before committing** `[lihfolk]`. Mock the same five screens in the candidate style: HUD over gameplay, shop, a dense list, a reward moment, settings on `Phone-S`. A style judged on one screen fails on the dense list.
5. **Components own every number** `[lihfolk]`. Screens call builders ("painters") such as `Components.header(panel, title)` or `Components.closeButton(panel)`; a one-off look is an explicit attribute on the screen that every re-skin pass checks, never a silent override.
6. **Make mass edits reversible** `[lihfolk]`. Before a sweep changes a property on hundreds of instances, store the old value in an attribute (`Pre_Font`, `Pre_Color`); `UDim2`, `Color3` and `Font` are valid attribute types `[official]` and outlive Studio's undo history.
7. **Audit with a score** (flags in `ui-input-crossplatform.md` §UI audit scan) and re-run it after every UI change.

Component state matrix: draw and build every state before shipping the component. Most visual bugs are missing states. `[lihfolk]`

| Component | States |
|---|---|
| Button | default, hover, pressed, gamepad-focused, disabled (with reason), pending (request in flight) |
| Claim / buy button | available, pending, done (kept visible, with a tick), locked (with the requirement), premium skip |
| Tab | idle, active, has-badge, gamepad-focused. Active ("this page is open") and focused ("the cursor is here") must look different |
| Card / slot | default, selected, equipped, locked, new |
| Toggle, slider, segmented choice | each value, disabled, focused; toggles move the knob and change a word or icon, not only the colour |
| Progress bar | empty (keep a minimum visible sliver), filling, full, completed |
| Toast | entering, holding, merged (bumped), leaving |

One shared close button: build it once and size it from the header, not per panel `[lihfolk]`. A square about 1.1× the header height (`SizeConstraint = RelativeYY`, `Size = UDim2.fromScale(1.1, 1.1)`), anchored `(1, 1)` at the header's bottom-right, reads as a confident target on phones. Keep `ClipsDescendants` off the header and panel (put it on the inner content frame): a clipped half of a button is neither drawn nor tappable.

## Frames and scale

| Figma frame | Size | Purpose |
|---|---|---|
| `Phone-S` (design here first) | 800×360 `[house]` | Smallest landscape phone; the layout must work here before anything else |
| `Phone-Narrow` | 667×375 | Narrowest common phone; every HUD overlap shows here first `[lihfolk]` |
| `Phone-Notch` | 844×390 (also 932×430) | Tall-aspect check with the notch on either side; community import skills use 844×390 as the phone reference `[community]` |
| `Tablet` | 1024×768 | 4:3; thumb reach differs: a button 40% from the top is reachable on a phone, not on a tablet `[official]` |
| `Desktop/TV` | 1920×1080 | Same components; panels get `UISizeConstraint` max so 75% width does not become huge on a TV `[official]` |

- `[house][VS]` Do not assume a phone's viewport equals its physical pixel resolution. Print `workspace.CurrentCamera.ViewportSize` on the real target phone and add that frame.
- Every frame carries three locked overlay layers: thumbstick zone (bottom-left), jump zone (bottom-right), top bar strip. The top bar is reported as 58 px tall on large screens, 48 on phones, absent on console `[community][VS]`: never hard-code it; use `ScreenInsets`/`GuiService.TopbarInset`.
- Phones report short sides of about 360–430 px in landscape and the smallest tablets about 600 `[lihfolk]`; a workable phone test is touch input with a short side under about 520 px.
- **Conflict:** LihFolk designs at 1920×1080 and adds a separate phone arrangement for every screen that would otherwise draw text under 12 px. This skill designs the phone frame first (house rule: mobile-first) and widens it. Both end in the same place: a real phone layout, not a shrunken desktop one. Their measured thresholds are adopted as pass criteria in `ui-input-crossplatform.md`.
- Size from the short side: on landscape, set element height by scale and lock shape with `UIAspectRatioConstraint` (or `SizeConstraint = RelativeYY`). Offsets are for margins, padding and strokes.

## Screen inventory

Design every row before building any: HUD, shop, inventory/collection, item detail, reward popup, toast/notification, offer card, quest/daily tracker, settings, confirm dialog, loading screen, custom proximity prompt, world labels (`BillboardGui`), gamepad focus ring. For each interactive component draw default, pressed, disabled (with the reason: "Need 50 coins"), selected and gamepad-focused states, plus empty, locked and error states for every list.

## Patterns with sizes

px are at `Phone-S` (800×360); the scale column is the fraction of screen height (H) or width (W). All `[house]` unless tagged; observed conventions come from one community teardown of about 20 hit games (screenshot-based, approximate, one author) `[community]`.

| Element | px at Phone-S | Scale | Placement and rule |
|---|---|---|---|
| Currency readout | icon 28–32, number 18–20 | 0.08–0.09 H | Top-left below the top bar or top of the left column. Icon + outlined number, **no panel behind HUD numbers** `[community]`; count up, never snap |
| Menu buttons | 56×56, gap 8 | 0.155 H | **One home edge** (left column, right column or bottom-centre row) `[community]`; max 4–6, the rest behind "More"; red count badge only when something is claimable |
| Primary action | ≥ 0.8× jump button (≈ 56 where jump is ≈ 70 `[community][VS]`) | read at runtime | Positioned relative to `JumpButton` once it `IsLoaded` `[official]`; never by screen percentage |
| Touch target floor | 44×44 | 0.12 H | Close, tabs, steppers. 44 is the Apple HIG figure, not a Roblox constant `[community]`; XAG asks for about 9 mm |
| Objective / timer | height 32–40 | 0.10 H | Top-centre: "where am I / how long" `[community]`; read-only, hardest thumb reach |
| Quest tracker | width ≤ 220 | ≤ 0.28 W | Right edge, mid-height; 1–3 lines with `101/500` progress; collapsible on phone |
| Toast | height 36–44 | 0.11 H | Top-centre under the objective; ≤ 2 visible on `Phone-S`, lifetime by reading time (2.5–7 s), merge and queue the rest (Notifications recipe); coloured by rarity; never a modal |
| Shop / inventory window | ≤ 736×310 | ≤ 0.92 W × 0.86 H | Centred, dark or neutral body so coloured cards read; header 44–48; **close is red, top-right, ≥ 44** `[community]`; opens in ≤ 0.25 s |
| Shop card | ≈ 220×190, 3 columns | (W − padding) / 3 | Art top, name, native price text, full-width buy button ≥ 44 high; show the top of the next row so scrolling is obvious. Robux buttons green with the Robux glyph; gift button beside passes `[community]` |
| Inventory cell | 64–72, columns computed from width | 0.18–0.20 H | Rarity = colour + name bar or icon; count bottom-right in outlined text; equipped and favourite as icons. Undiscovered = silhouette + `??` with `162/284` progress `[community]` |
| Item detail | n/a | n/a | Side pane on wide screens; a pushed page under about 700 px width (breakpoint, not shrink) |
| Reward popup | item 96–128, window ≤ 0.6 H | n/a | Centre, sunburst behind the item, one Claim button, tap-anywhere dismiss; never traps movement for more than about 1.5 s; batch many rewards into one summary |
| Offer card | ≤ 25% of screen | n/a | Rules in `ui-input-crossplatform.md` (offer surfaces paragraph) and `monetization-and-policy.md` |

- Put information in the world when it belongs to an object (price, rate, timer on a `BillboardGui` above it) so the HUD stays small. `[community]`
- Give each destination one colour and keep it everywhere (Shop red, Rewards green, Quests orange). `[community]`
- Print the key on the button on PC (`[E]`); the same action becomes a round touch button on phones. `[community]`
- **Conflict:** the same teardown lists strikethrough anchor prices, "% OFF" tags and urgency countdowns as common in hit games. House rule 3 overrides: show a timer only for a real state (a restock that happens, an event end date that does not move), a discount only against a price that was really charged, and never reset a countdown.
- **Conflict:** hit simulators run denser HUDs than the 5–7 element cap in `ui-input-crossplatform.md`. Keep the cap on phones by counting groups (one menu column = one element) and hiding secondary buttons behind "More".

## Screen build recipes

Each recipe lists anatomy, numbers, the server rule and the failure modes to test. Sizes are in the patterns table; engine wiring (presenter, bands, blocker) is in `ui-input-crossplatform.md` §UI architecture. Rules adapted from LihFolk's production notes are tagged; where they clash with the house rules, the house rules win.

**Shared window anatomy.** Header (icon, loud title, the window's signature colour) → optional tab strip → scrolling content → optional footer (summary, "Claim all", timer). Close top-right, same component everywhere, also on gamepad B and Escape. One presenter, one open window. A full-screen dim (black at 0.5–0.6 transparency) fades with the window, blocks input behind it and is the tap-outside-to-close target. The primary action is the brightest thing on the screen, one per card at most. On phones an open window hides the HUD. `[lihfolk]`

**Claim and buy buttons share one state machine.** available → pending → done, or locked with the reason. The pending state is the one most games forget: between the tap and the server's answer (typically 50–500 ms, seconds on a bad connection) the button is non-interactable and shows progress, or a second tap sends a second request. The server re-checks everything and records the claim before it pays out. `[lihfolk]`

### HUD

- Agree a zone map before placing anything: status near the top, actions near the bottom, navigation grouped on one edge, the centre third clear except for short feedback.
- One primary action, visibly the largest element, positioned from its bar or the jump button, never from absolute screen offsets.
- Stackable elements (boost row, quest tracker, boss bar, toast lane, tutorial banner) are rows in one slot table (edge, order, gap) placed by one layout function. HUDs break by accretion: each hand-placed element looks fine alone and collides on a 667×375 phone mid-fight. `[lihfolk]`
- Show rates beside totals where they drive decisions (`$12.4K/s`). Shown numbers must be the true ones: every multiplier included, odds equal to the odds rolled.
- Progressive disclosure: during the tutorial show only the button the current step needs; show later features as locked with their condition ("Unlocks in Zone 4") instead of hiding them; badge only when something useful can be done now. `[lihfolk]`
- Phone: navigation at most 2 columns wide; quest tracker folded by default and at most two rows under about 420 px height; bars and captions enlarged so drawn text stays ≥ 12 px. `[lihfolk]`
- Test: zero overlapping rectangles at every test viewport in every scenario (idle, combat, boss bar, tracker open, tutorial). A feature only reachable from a hidden HUD element is a broken feature.

### Shop

- Sections with headers: passes, products (currency, boosts), bundles. Card: square art (`ScaleType = Fit`, never stretched), name, one-line benefit ("2× Cash for 10 min"), native price button.
- Prices come from `MarketplaceService:GetProductInfoAsync`, never hard-coded; the button only opens the prompt. The grant happens in `ProcessReceipt` (products) or after a server ownership check (passes), and the card flips to "Owned" or "Active 12:41" when the server says so, never when the prompt closes. Details in `data-and-purchases.md`.
- Phone cards about 1.3–1.4× their desktop size with fewer columns `[lihfolk]`. Keep the price outline thin enough that digit holes stay open (stroke rule in Design system and tokens); an unreadable price costs sales.
- Say the scope precisely: "this server" on a server-wide boost. Live 3D previews (`ViewportFrame`) only in the featured slot or detail pane, never per card.
- House rule 3: no countdown that restarts, no strikethrough without a real former price, close button never hidden. Paid random items show full odds read from the same config module the server rolls from, behind the PolicyService gate (`monetization-and-policy.md`).
- Failure modes: owned state granted from the client; double purchase prompts (no pending state); "Best value" on something that is not.

### Inventory and collection

- Stack duplicates first: 900 copies of 40 item types are 40 entries. Show an explicit cap (`480 / 500`).
- Under about 100 entries use a plain grid; above about 300, or unbounded, virtualise. A card is 10–20 instances, so 1,000 cards are about 15,000 instances. `[lihfolk]`
- The view is a filtered, sorted array of item keys; cells are windows onto `view[index]`. State (selected, new, equipped) lives in data keyed by item, never on the cell. Connect `Activated` once when a cell is created and read its bound key at click time. `[lihfolk]`
- Search with `string.find(name, query, 1, true)` (plain match: a typed `%` or `[` otherwise throws), debounce 0.15–0.25 s, precompute lower-case names. End every sort comparator with a unique tiebreaker; `table.sort` is not stable, so equal items visibly shuffle. `[lihfolk]`
- Scroll position: reset on search, filter or sort change; keep on count or state change and on new items (show a "1 new" pill instead of jumping).
- Gamepad selection is a data index, not an instance: recycled cells otherwise keep the focus ring on the wrong item. Detail pane beside the grid on wide screens, a pushed page with Back on narrow ones.
- Icons are pre-rendered images; preload the first screen's icons, and back each cell with a rarity-tinted plate so late textures do not pop.

### Settings

- Rows: label, optional one-line description, one control. Groups: Audio, Graphics, Controls, Accessibility. Category rail and footer fixed, page scrolls.
- Minimum set: music and SFX volume, effects quality, camera shake, reduced motion (default from the platform setting), hide other players' effects, UI scale, plus what `ui-input-crossplatform.md` §Accessibility requires.
- Every control ≥ 44 px tall drawn, whatever the track art; the whole row is the tap target for toggles. Sliders show the number; the fill follows the finger directly (no tween while dragging) and previews live. Gamepad: left/right steps sliders and segmented choices, shoulder buttons switch category. `[lihfolk]`
- Pick one saving model: auto-save ("Changes save automatically": apply locally at once, send after a few idle seconds or on close) or explicit Apply/Reset. Never mix them and never write a DataStore per slider tick; settings live in the player profile. `[lihfolk]`

### Codes

- One instruction line, one text field (about 24 characters), one Redeem button, one inline result line. Errors appear at the field, not in a corner toast.
- Client trims whitespace and shows "Checking…" with the button disabled; the server normalises case, checks validity, expiry and one-use-per-player, and rate-limits attempts (for example 5 per minute) so the box is not a brute-force oracle. The code list never ships to the client. `[lihfolk]`
- Enter submits (`FocusLost` with `enterPressed`). Distribution policy is in `growth-and-marketing.md` §8.

### Daily rewards

- Seven cards; the last one visibly larger. States: claimed (tick, dimmed), today (claim), later (locked). One-tap claim, badge on the HUD entry while a claim is ready, countdown text updated only while the window is open.
- Reset on a fixed clock (UTC midnight), not 24 hours after the last claim, which drifts later each day `[lihfolk]`.
- **Conflict:** LihFolk treats "does a missed day reset the streak?" as a design choice to state on screen. House rule: it never resets. Use the cumulative calendar from `liveops-quests-retention.md` (days played, not consecutive days) and no join pop-up.
- Alternative that needs no calendar: playtime gifts in tiers (short, medium, long intervals) with one interval banked across a break `[lihfolk]`.

### Rebirth / prestige

- Current tier and next tier side by side with their multipliers; a progress bar of have/need with a percentage; one line stating what resets and what stays.
- Two-step confirmation: the first tap turns the button into a danger-coloured "Tap to confirm" for about 3 s, or opens a one-line confirm dialog. Players who lose progress by accident do not return. `[lihfolk]`
- A paid skip, if any, is a separate, clearly priced button (never in competitive modes). Maths in `economy-and-progression.md`.

### Notifications

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
- Kinds are data: `{ channel, priority 1–4, merge rule, merge window, minimum time, sound }`. The server sends a kind and parameters (`ItemObtained`, item id, count), never English text; the client formats, localises and merges. `[lihfolk]`
- Toast queue: 2 visible on `Phone-S`, up to 3 on larger phones and tablets, 4–5 on PC; at most 8–10 waiting; drop stale ones. Lifetime `clamp(1.6 + 0.3 × words, 2.5, 7)` s, paused while hovered or touched. `[lihfolk]`
- Merge rules: `sum` ("+250" five times → "+1,250"), `count` ("Iron Ore ×3"), `replace` ("Quest 4/10" in place), `none`. Merge waiting toasts too, and cap lifetime extension so a trickle cannot pin a toast forever. A full stack lets a higher priority evict the oldest, lowest one. Floating numbers: pool about 12, merge same-kind within about 0.5 s. `[lihfolk]`
- Banners: one centre slot owned by one module, at most 4 waiting, each shortened to about 1.2 s when more than two wait. Position with `AnchorPoint (0.5, 0.5)` and scale 0.5 on a full-screen parent, never from a width measured elsewhere. `[lihfolk]`
- Popup gate: no banner during the tutorial, a cutscene, the death screen or an open window; hold it (up to about 20 s) or drop it. `[lihfolk]`
- Placement: top-centre or top-right, never bottom-right on phones. Sound only for priority 3–4, one shared soft tick otherwise, at most one per 0.5 s.
- Stress test: a debug command that fires every kind 10 times in one frame, then watch for 60 s.

### Loading screen

- A `ReplicatedFirst` LocalScript shows its own ScreenGui (`ScreenInsets = None`, high `DisplayOrder`) and calls `RemoveDefaultLoadingScreen()`. Preload only what the first screen needs: the loading art, HUD fonts and first-screen icons through `ContentProvider:PreloadAsync`.
- Teardown is one idempotent function: calling it twice is harmless and nothing can re-show the screen. A watchdog removes the screen after a fixed time (15–20 s `[house]`) and logs why. Every wait in the ready check has a timeout, and nothing waits on an instance that streaming may not have sent. If the watchdog fires on more than about 1% of joins, the ready check waits for the wrong thing. `[lihfolk]`
- Fade out in about 0.3 s. No offers, no purchase prompts (house rule 3). Join pipeline and budgets: `performance.md`.

## Motion spec

UI motion has four jobs: orientation (where it came from, where it went), causality (what my input did), hierarchy (what to read first) and state (busy, ready, locked, new). An animation that does none of them is cut `[lihfolk]`. Define motion as a handful of tokens; no screen creates its own `TweenInfo`.

| Token | Duration | Easing | Animate | Notes |
|---|---|---|---|---|
| `press` | 0.06–0.10 s | Quad Out | child `UIScale` to 0.92–0.96, face sinks into the lip | Under 0.08 s nothing is visible at 30 fps (3–4 frames) |
| `release` | 0.16–0.30 s | Back Out | `UIScale` to 1 | |
| `hover` / gamepad focus | 0.10–0.12 s | Quad Out | `UIScale` 1.04–1.06 | Focus looks at least like hover, plus a ring |
| `enter` | 0.18–0.26 s | Back Out (playful) or Quint Out (clean) | `UIScale` from 0.90–0.92 (not from 0) + fade | `enterLarge` (full-screen surfaces) about 1.3× longer |
| `exit` | 0.10–0.15 s | Quad In or Quint In | scale to 0.90 + fade | 0.55–0.75× the enter time; never Back In (it first moves the wrong way) |
| `move` | 0.20–0.40 s | Quad or Sine InOut | `Position` | Scale with distance (below) |
| `emphasis` | 0.25–0.45 s | Back Out | `UIScale` pop 1.2 → 1 | Reward icons, badge arrival |
| `toggle` / selector slide | 0.10–0.16 s | Quad Out | knob position, track colour | Keep the colour change under reduced motion |
| `fill` (progress) | 0.35 s | Quad Out | bar `Size.X.Scale` | Fast start reads responsive |
| `countUp` | 0.35–0.8 s | Quad Out (Exponential Out for huge jumps) | a NumberValue driving text at ≤ 10 Hz | |
| `idle` (breathe, bob) | 0.6–0.8 s half period | Sine InOut, `Reverses`, `RepeatCount = -1` | transparency, ±3 px, rotation | Pause when the screen is hidden |
| `timer` / cooldown sweep | real duration | Linear | fill | Linear is right only for things that represent time |
| `shine` | 1.2 s every 3 s | Linear | `UIGradient.Offset` −1 → 1 | One element per screen `[community]` |
| `shake` (error) | 6 steps of 0.04 s: ±8, ±5, ±2 px | none | `Position` offset | Colour flash only under reduced motion `[lihfolk]` |

Durations are `[lihfolk]` field values cross-checked with the community numbers already in this file; they agree within a few hundredths. Perception bands: under 0.1 s reads as instant, 0.1–0.2 snappy (feedback, exits), 0.2–0.35 visible (entrances), 0.35–0.6 deliberate (big reveals only), above 0.6 the player is waiting. Elastic and Bounce are for a single reward icon, never a panel the player must read.

**Conflict:** the official accessibility sample tweens a settings panel over 0.75 s, and `ui-input-crossplatform.md` allowed up to 0.75 s for panels. LihFolk reports players calling 0.3 s opens sluggish and settling at 0.14–0.26 s open, 0.12–0.14 s close. Trust the short values for navigation; keep long durations for reward sequences the player is enjoying.

Rules that make motion hold up `[lihfolk]`:

- **Distance-scaled moves.** `duration = clamp(0.12 + 0.012 × sqrt(pixels), 0.15, 0.45)`: 40 px → 0.19 s, 200 px → 0.29 s, 600 px → 0.41 s. Measure pixels from `AbsolutePosition`, not from scale, or the same move is 400 px on a phone and 1,280 px on a monitor.
- **Stagger with a cap.** 0.05–0.07 s per item for 2–5 items, 0.03–0.04 s for 6–12, total never above 0.4 s (`step = min(step, 0.4 / (n − 1))`); beyond 12 items stagger the first row only.
- **Lead and follow.** Container first, content 0.04–0.08 s later and shorter so both finish together, primary button last with a small pop. Exits leave together. Overlap steps (start the next at about 60% of the previous) with `task.delay`; do not chain on `Completed`.
- **State, not events.** Store `wantOpen` and animate toward it from one function. Hide on `Completed` only when `playbackState == Enum.PlaybackState.Completed` and the intent is still "closed"; otherwise a fast reopen ends with the open window vanishing. `Tween:Cancel()` leaves the property where it was `[official]`.
- **Proportional retarget.** A close interrupted at 80% needs about 20% of the enter time to reopen; multiply the token time by the remaining fraction with a floor of about 0.3.
- **Input from the first visible frame.** Never disable buttons until an entrance ends, and set the gamepad selection when the entrance starts. Locked input is the usual cause of "the UI feels laggy" with short tweens.
- **Pick the property.** Pop with a child `UIScale` (cheap, scales text and strokes with it); tweening `Size` re-runs sibling layout, re-wraps text and makes `TextScaled` text step between sizes. Never tween `Position` of a child owned by a layout (nothing happens): animate an inner "face" frame. Fade a whole panel with `CanvasGroup.GroupTransparency` or per-element toward each element's stored base transparency. Do not tween `UIStroke.Thickness` on text `[official]`.
- **Two scales, two objects.** Device scale on the root, pop scale on an inner frame; two `UIScale`s on one object fight.

Springs: use them where motion is retargeted constantly (tab indicators, sliders after release, drag-and-drop, HUD tiles poked often), because a spring keeps its velocity through a retarget. Options: `TweenService:SmoothDamp(current, target, velocity, smoothTime, …)` returns the new value and velocity, is critically damped and never overshoots `[official][VS]`; `spr.target(instance, dampingRatio, frequency, properties)` `[community]`. Starting points `[house]`: follow motion, damping 1.0 at 4–6 Hz; playful pop, damping 0.5–0.7 at 3–5 Hz (spr's README examples use 1/1 and 0.6/4). Run all Lua springs from one shared connection that disconnects when everything has settled, so an idle HUD costs zero Lua per frame `[lihfolk]`.

Reduced motion is not "no feedback" `[official][lihfolk]`:

| Normal | Reduced (`GuiService.ReducedMotionEnabled` or the in-game toggle) |
|---|---|
| Panel scales in | Fade 0.1–0.15 s |
| Press squash, hover lift | Colour or brightness change |
| Staggered cards | All appear together |
| Currency flies to the counter | Counter pulses its colour once |
| Shake, idle bobbing, sunburst | Static |

## Figma MCP workflow

Tool names are from the official Figma MCP connected to this skill's operator `[VS]`. Read tools are rate-limited by plan (reported: 6 calls/month on Starter or View/Collab seats, about 200/day on paid Dev/Full seats `[community][VS]`): batch work, avoid redundant screenshots.

1. **Load the server's skills first.** `/figma-use` before any `use_figma`; `/figma-design-to-code` before `get_design_context`; `/figma-generate-design` for full screens. Fallback: `get_figma_skill` with `skill://figma/<name>/SKILL.md`.
2. **File and session.** `whoami` → plan key → `create_new_file` (editorType `design`) → `create_session` once; pass its `sessionId` to every later call. For an existing file, parse `fileKey` and `node-id` from the URL (`1-2` → `1:2`).
3. **Tokens before pixels.** `use_figma`: create variable collections `Color`, `Space`, `Radius`, `Stroke` and text styles for the type scale. Name them exactly as the theme keys (`Color/Primary`).
4. **Components.** `use_figma`: Button (Primary, Premium, Danger × default/pressed/disabled), Panel, Card, CurrencyReadout, Tab, Badge, Toast, Slot. Frames with auto layout, never Groups. Layer name = Roblox instance name (`BuyButton`). Prefixes: `Img_` rasterise as one PNG, `Btn_` button, `Scroll_` ScrollingFrame, `Txt_` runtime text (placeholder is the longest expected string, +30% for localisation).
5. **Compose at `Phone-S`** over a real gameplay screenshot and the reserved-zone overlays; then place the same components in the other frames. Do not scale a desktop design down.
6. **Review.** `get_screenshot` (raise `maxDimension` above the 1024 default for detail). Run the polish checklist below; fix in Figma, where iteration is cheap.
7. **Extract.** `get_metadata` (tree, x/y/w/h) → `get_design_context` per screen (fills, strokes, radii, effects, auto layout) → `get_variable_defs` (tokens) → `download_assets` per `Img_` node (`defaultFormat` png, `defaultScale` 2–3; URLs expire, download at once). The reference code is React + Tailwind `[community]`: treat it as a spec; never transliterate it.
8. **Theme.** Write tokens to `Theme.luau` (sketch below); optionally mirror them as `StyleSheet` token attributes for Studio-authored screens.
9. **Upload images** (settings below) and record `layer name → rbxassetid` in a manifest committed to the repo.
10. **Build in Studio** (Edit datamodel) with one builder script per screen through the Studio MCP `execute_luau`, or as Rojo-owned code. Order: ScreenGui (`ResetOnSpawn = false`, `ZIndexBehavior = Sibling`, `ScreenInsets = CoreUISafeInsets`) → containers and layouts → native visuals → images → text.
11. **Verify.** Studio MCP `screen_capture` at phone, tablet and desktop in the Device Emulator (`[VS]` the Device Simulator beta adds Flagship / Mid-range / Entry-level phone presets); compare with the Figma screenshot; run the UI audit scan from `ui-input-crossplatform.md`; then test on the real phone.

- Level-up mode (live game): dump the existing ScreenGui tree with `execute_luau`, `screen_capture` each screen, rebuild it as a baseline frame with `use_figma`, redesign beside it, and ship the diff one screen at a time behind a flag.
- Do not use `generate_figma_design` for Roblox: it captures web app pages (per the tool's own description). Design from scratch with `use_figma`.
- Converter plugins (table below) can replace steps 7–10 for a first pass. Always run step 11 on their output.

### px → Roblox

For a node `(x, y, w, h)` inside parent `(pw, ph)`, with coordinates relative to the direct parent (Figma metadata is absolute) and anchor `(ax, ay)` `[community]`:

```
Size      = UDim2.fromScale(w / pw, h / ph)
Position  = UDim2.fromScale((x + w * ax) / pw, (y + h * ay) / ph)
Corner    = UDim.new(math.min(0.5, r / math.min(w, h)), 0)   -- scale is relative to the shortest side [official]
Aspect    = UIAspectRatioConstraint.AspectRatio = w / h      -- on every root panel, button, icon and exported image
Gap / pad = offsets in px for small fixed spacing; scale only when the container itself scales
```

- Anchor by intent: HUD pinned to an edge or corner anchors on that edge; fill bars `(0, 0.5)`; dropdowns and auto-sized lists on the fixed side; centred panels, buttons and anything that scale-tweens `(0.5, 0.5)`.
- Figma opacity 25% = `BackgroundTransparency 0.75` `[official]`. A gradient multiplies the background, so set `BackgroundColor3` white under a `UIGradient`. `[community]`
- **Conflict (text):** community import skills set `TextScaled = true` on all text and forbid Offset. House rule stays: fixed `TextSize` with `AutomaticSize` and `TextWrapped` for body text, because `TextScaled` text ignores the player's `PreferredTextSize` and a `UITextSizeConstraint` clamps it `[official]`. Use `TextScaled` + `UITextSizeConstraint` only for short numerals and titles in fixed boxes.
- **Conflict (UIScale):** one import skill bans `UIScale` because it mis-scaled `ScaledSize` strokes (reported March 2026); other threads report strokes following `UIScale` `[community][VS]`. Keep the root-`UIScale` rule from `ui-input-crossplatform.md`, but do not combine it with `ScaledSize` strokes until checked on a device.

- Alternative mapping: keep every size in Offset exactly as drawn in the frame and put one fit `UIScale` on the screen root (`ui-input-crossplatform.md` §sizing strategies). Pixels then map 1:1 from Figma, which is what generated builders should emit. `[lihfolk]`

### Mapping gotchas

Failure modes when translating Figma data by hand or by converter `[lihfolk]`; compare a Studio capture with the Figma screenshot after each.

| Figma | Roblox | Trap |
|---|---|---|
| Linear gradient handles | `UIGradient.Rotation = atan2(dy, dx)` in degrees, white `BackgroundColor3` | Handles are normalised to the box: convert to pixels first or every diagonal on a non-square box points the wrong way. Roblox spreads stops edge to edge, Figma pins them to the handles: rescale the stops. 2–20 keypoints |
| Stroke align Inside / Center / Outside | `UIStroke.BorderStrokePosition` Inner / Center / Outer `[VS]` | Inside strokes eat into the box, outside strokes add to it; export bounds differ |
| Rotated node | `Rotation` + the node's own size | The bounding box of a rotated node is not its size |
| Mixed corner radii | Per-corner `UICorner` radii (beta) | Fallback: round all corners and cover the square side with a same-colour strip |
| Hug contents | `AutomaticSize` | Mapping Hug to a fixed size makes translated text overflow |
| Clip content on a rounded frame | `ClipsDescendants` clips to the rectangle only | A full-width header strip or fill paints square "pockets" past the rounded corners: round the child too, inset it, or use one `CanvasGroup` `[official]` |
| Drop shadow | One white soft-shadow 9-slice per radius, tinted with `ImageColor3`, or `UIShadow` once out of beta | One shadow per node; bake the rest |
| Image fill mode Fill / Fit / Tile | `ScaleType` Crop / Fit / Tile | Crop the PNG yourself instead of relying on a transform |
| Letter spacing | none | Roblox text has no tracking: design with 0 |
| Component variants | One `State` property: Default, Hover, Pressed, Disabled, Selected (gamepad focus, drawn on purpose) | A mock that shows only the resting state hides half the work |
| Font size 12 | 12 px at the frame's scale | At a 1920×1080 frame shrunk to a small phone it draws at about 4 px: keep ≥ 15 px in 1080p frames, ≥ 14 px in `Phone-S` |

- Exported PNGs keep 2 px of transparent padding for anti-aliasing; a 9-slice source needs only about `2 × inset + 8` px per side. `[lihfolk]`
- Mark guide layers (safe-area overlays, annotations) with a `skip_` prefix so no builder creates them. `[lihfolk]`
- Never hand-edit a generated builder: fix the Figma file or the generator and regenerate, and keep states and motion in a separate controller so regeneration cannot erase them. `[lihfolk]`

## Export and import settings

| Topic | Setting | Tag |
|---|---|---|
| Format | PNG with alpha, cropped to visible bounds (include baked glow or shadow, then size the ImageLabel to the exported bounds) | `[community]` |
| Resolution | Longest side ≤ 1024 px. Export at 2× the largest on-screen size (3× for small icons), never above 1024 | `[community][VS]` 1024×1024 is the documented maximum for texture maps; larger UI images are reported downscaled |
| Upload limits | Open Cloud image upload: `.png .jpeg .bmp .tga`, ≤ 20 MB, smaller than 8000×8000 px | `[official][VS]` |
| Memory | Cost follows pixel count, not file size: 1024² costs 4× a 512²; compressing or dropping alpha saves no memory | `[official]` |
| Text | Hide text layers before export; rebuild as TextLabel. Baked text cannot be localised or resized and is more likely to be moderated | `[community]` |
| Colour variants | Export one white or grey base; tint with `ImageColor3` (multiplies). One slot image serves every rarity | `[community]` |
| 9-slice | Stretchable panels, bars, buttons: export small (128–256 px), `ScaleType = Slice`, `SliceCenter = Rect.new(l, t, w − r, h − b)`, tune `SliceScale` so corners match the mock. Corners never scale; edges scale on one axis | `[official]` |
| Sprite sheets | Many small icons → one ≤ 1024² sheet, `ImageRectOffset`/`ImageRectSize`; 2 px transparent gutter between cells | `[official]` gutter `[house]` |
| Tiling | Stud/noise textures: `ScaleType = Tile` + `TileSize`; never stretch a texture | `[official]` |
| Blend modes | None in Roblox. Convert an Overlay texture to a white-alpha highlight image plus a black-alpha shadow image | `[community]` |
| Fades on images | `UIGradient.Transparency` did not fade a tiled ImageLabel in one verified port: bake the fade | `[community]` single report |
| Pixel art | `ResampleMode = Pixelated` | `[official]` |
| Upload path | Studio MCP `upload_image` (batch, HTTP URLs; one verified port served the export folder on localhost, then stopped the server `[community]`); or Open Cloud Assets through the Studio MCP (`asset:write`, approved upload folder); or Asset Manager bulk import | `[official][VS]` |
| Moderation | Every image is moderated and renders blank until approved; uploads are permanent assets on the owner account or group | `[official]` |

Icon sets and art: draw icons in Figma as one family (same stroke, corner and perspective). Community skills ship art bundles whose own notes say the licence is unclear: use them for reference only, never ship them. Studio MCP `generate_*` and `insert_asset` stay off-limits for shipped content (house rule 1); `upload_image` for your own Figma exports is fine.

### Converters and agent skills (GitHub, checked 2026-11-10)

| Repo | Stars · last push · licence | What it does |
|---|---|---|
| `NoTwistedHere/Figma-to-Roblox` | 32 · 2026-08 · MPL-2.0 | Figma plugin → `.rbxmx`; name-driven (`Button`, `Scroll`, `IMG`); linear gradients only; uploads through an Open Cloud key |
| `MiaGobble/Figma-Import-Assistant` | 18 · 2026-07 · none stated | Studio plugin source that assists manual import |
| `xtrair/figma-to-roblox-ui` | 7 · 2026-09 · MIT | Agent skill: Figma MCP + Studio MCP recipe, px→scale formulas, validator. Scale-only and TextScaled rules conflict with this file (above) |
| `grim-technologies-arch/ui-figma-roblox` | 22 · 2026-10 · MIT (text only) | Agent skill for stud-style UI in Figma with a verified Studio port; bundled art has no clear licence |
| `MarkRuiz00/RbxUiStudio` | 1 · 2026-10 · MIT | Skill + editor + MCP; teardowns of hit-game UI (source of the conventions above) |
| `RaRdq/FigmaRobloxForge`, `astrorehan/figlo` | 1 each · 2026-10/11 · MIT | Rasterise-everything exporter (pixel-accurate, many uploads, more texture memory); plugin + local relay + Studio plugin (alpha) |
| `cameronpcampbell/supercorner` | 16 · 2026-07 · MIT | Figma-style squircle corners as generated 9-slice images |
| `lihfolk-cy/v2-vault` (`skills/lihfolk-figma`) | CC BY 4.0 text | Agent skill with a property-mapping contract and a stdlib-Python converter from Figma REST JSON to a Luau builder (Offset + one fit `UIScale`). Read for method; do not depend on it or on its asset kit |
| `lopi-py/figblox`, `EgoMoose/figma-to-roblox-ui` | 15 · 2023-12 · MIT; 9 · 2024-09 · archived | Stale: do not start here |

DevForum also lists FigBloxUI, RoImport, UILint, Bloxporter (paid), MonkeyPTR and GuiForge; one 2025 thread reports converter output with elements "separating weirdly" `[community]`. Low star counts everywhere: treat converters as accelerators and audit their output.

## Theme module (unexecuted sketch)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Theme.luau. Generated from Figma variables; edit in Figma, then regenerate.
return table.freeze({
	Color = table.freeze({
		Primary = Color3.fromHex("#34C759"), Premium = Color3.fromHex("#FFB020"),
		Danger = Color3.fromHex("#F24848"), Surface = Color3.fromHex("#23262F"),
		Ink = Color3.fromHex("#FFFFFF"), Outline = Color3.fromHex("#14161C"),
	}),
	Rarity = table.freeze({
		Common = Color3.fromHex("#B9C0CC"), Rare = Color3.fromHex("#3BA1FF"),
		Epic = Color3.fromHex("#B04BFF"), Legendary = Color3.fromHex("#FFB020"),
	}),
	Font = table.freeze({
		Display = Font.fromEnum(Enum.Font.FredokaOne),
		Body = Font.fromEnum(Enum.Font.BuilderSansBold),
	}),
	TextSize = table.freeze({ Display = 30, Title = 22, Hud = 20, Body = 16, Caption = 14 }),
	Space = table.freeze({ XS = 4, S = 8, M = 12, L = 16, XL = 24 }),
	Radius = table.freeze({ S = UDim.new(0, 6), M = UDim.new(0, 10), Pill = UDim.new(0.5, 0) }),
	Stroke = table.freeze({ Thin = 2, Regular = 3, TextRatio = 0.07 }),
})
```

Colours and fonts above are placeholders, not a house style; the rarity values are approximate starting points from a community teardown `[community]`. Replace everything with the game's own tokens.

The `Motion` module that owns every `TweenInfo` (tokens, reduced-motion handling, proportional retarget) and the interruption-safe window presenter are sketched in `ui-input-crossplatform.md` §UI architecture.

## Generic-UI tells and fixes

| Tell | Fix |
|---|---|
| Default grey frames, `SourceSans`, square corners, thin 1 px borders | Theme module: one display font, one radius family, 2–3 px near-black outlines |
| Flat buttons with no depth or states | Lip + gradient + sheen (9-slice); pressed sinks; disabled greys and says why |
| Every element equally loud; rainbow gradients on everything | One accent per screen; neutral window bodies; saturation only on actions and rarity |
| Boxes behind every HUD number | Icon + outlined number straight on the world |
| Buttons scattered on all four edges | One home edge; top-centre for status; bottom corners left to the controls |
| Stretched icons and squashed panels on wide phones | `UIAspectRatioConstraint` on every button, icon and image; 9-slice for panels |
| Blurry art | Export 2× at most 1024; no upscaling in Studio; `ImageLabel` near native size `[official]` |
| Text clipped, tiny, or different size per label | Fixed type scale; `UITextSizeConstraint` on scaled numerals; +30% width for localisation |
| Numbers snap; windows pop | Count-up, 0.2 s open, press feedback under 0.1 s |
| Mixed icon styles from several packs | One authored icon family, white base, tinted |
| Copy of a hit game's skin | Copy the layout pattern, not the art, logo or palette `[community]` |
| Coloured "pockets" poking past rounded corners | Round or inset the child, or clip with one `CanvasGroup`; clipping ignores `UICorner` `[official]` |
| Double outlines, mismatched nested radii, rows of uneven height, captions a few pixels off-centre | The audit flags that most often separate "almost" from "finished" `[lihfolk]`; inner radius = outer radius − padding |
| Close buttons that differ per window | One shared close component sized from the header |
| Every window opens with a different animation | Motion tokens; direction carries meaning (HUD parts slide from their edge, overlays scale from centre) `[lihfolk]` |

## Polish checklist

- [ ] Squint test at phone size over real gameplay: the primary action and primary currency are found in under a second.
- [ ] Every button has pressed, disabled and focused states; press feedback under 100 ms with a light click sound.
- [ ] Spacing is on the 8 px grid; visible contents (not bounding boxes) are optically centred.
- [ ] One accent per screen; rarity always carries a label or icon.
- [ ] Text outlined or plated wherever it sits over the world or a texture.
- [ ] Windows: loud title, red close top-right ≥ 44 px, dark or neutral body, Back and gamepad B close it.
- [ ] Counters count up; rewards get one popup, then a toast; nothing loops forever except one subtle idle on the best-value button.
- [ ] Longest localised string and the largest number (`999.9Qa`) fit every label.
- [ ] No image above 1024 px; no baked text; icons from one family; variants are tints.
- [ ] Reduce Motion, Background Transparency and Text Size settings tried once each.
- [ ] Ten rapid taps on any open/close button end in the last requested state; exits are faster than entrances; no window blocks input while it animates.
- [ ] Stroke test string readable at phone size; every claim and buy button has a pending state.

## Level-up: UI look symptoms → cause → fix

| Symptom in a live game | Likely cause | Fix |
|---|---|---|
| "Looks like a free model" feedback, low thumbnail-to-play trust | No design system; default styling | Tokens + Theme; restyle the HUD and shop first, one screen per update |
| Shop conversion low although traffic is fine | Buy buttons small or far from thumb; price baked in art; window slow to open | Full-width buy buttons ≥ 44 px, native price text, open ≤ 0.25 s; see `monetization-and-policy.md` |
| New players miss the main loop button | No visual hierarchy; too many equal buttons | One accent, one home edge, badge only on the next useful action |
| UI art looks soft on desktop, fine on phone | Exported at 1× of the phone frame | Re-export 2–3× (≤ 1024) or rebuild natively |
| Client memory high after a UI update | Dozens of 1024² uploads, full-screen art, a `CanvasGroup` per card | Sprite sheets, tinted bases, 9-slice, native shapes; measure in the Developer Console memory tab |
| Re-skin takes weeks | Colours and sizes hard-coded per instance | Theme module or `StyleSheet` tokens; tag-driven styles |

## Review gate

- [ ] Tokens exist in Figma and in `Theme.luau`; no hard-coded colours, fonts or sizes elsewhere.
- [ ] Designed at `Phone-S` first with reserved-zone overlays; checked on notch phone, tablet and 1080p.
- [ ] Each layer classified native or image; no baked text; images ≤ 1024 px, tinted variants, 9-slice for stretchable art; asset manifest committed.
- [ ] Body text uses fixed `TextSize`; `TextScaled` only with `UITextSizeConstraint` on short numerals and titles.
- [ ] No beta-only UI property is required for the screen to read correctly in the live client.
- [ ] Studio captures match the Figma frames on phone, tablet and desktop; verified on a real 3 GB Android phone.
- [ ] No timer, discount or scarcity element that is not literally true (house rule 3); third-party art not shipped.
- [ ] Every component has its full state matrix; every recipe in use passes its listed failure-mode tests (notification burst, rapid toggle, loading watchdog).
- [ ] All UI tweens go through the Motion module; reduced motion swaps movement for fades.
- [ ] The look is the game's own (brief, references, tokens); nothing copied from a reference kit or another game.
- [ ] Polish checklist passed; `ui-input-crossplatform.md` review gate passed.

## Sources

Accessed 2026-11-10.

- `Roblox/creator-docs` (read): `ui/9-slice.md`, `ui/appearance-modifiers.md`, `ui/position-and-size.md`, `ui/labels.md`, `ui/rich-text.md`, `ui/styling/index.md`, `ui/styling/editor.md`, `projects/cross-platform.md`, `production/publishing/accessibility.md`, `performance-optimization/improve.md`, `art/modeling/texture-specifications.md`, `cloud/guides/usage-assets.md`, `studio/mcp.md`, `studio/mcp-open-cloud.md`, `studio/device-simulator.md`, `tutorials/curriculums/user-interface-design/*.md`, `tutorials/use-case-tutorials/ui/create-hud-meters.md`, class and enum reference for `UIStroke`, `UICorner`, `UIShadow`, `UIGradient`, `CanvasGroup`, `ImageLabel`, `GuiService`, `TweenService`, `TweenBase`, `Font`, `GradientType`, `StrokeSizingMode`: https://github.com/Roblox/creator-docs
- https://github.com/xtrair/figma-to-roblox-ui (read: README, SKILL.md)
- https://github.com/grim-technologies-arch/ui-figma-roblox (read: README, SKILL.md, examples/stud-shop/README.md, ATTRIBUTION.md)
- https://github.com/MarkRuiz00/RbxUiStudio (read: README, juegos/README.md, juegos/pet-simulator-99.md, estilos/simulator.md, roblox-ui/images.md, checklist.md)
- https://github.com/NoTwistedHere/Figma-to-Roblox, https://github.com/RaRdq/FigmaRobloxForge, https://github.com/astrorehan/figlo, https://github.com/MiaGobble/Figma-Import-Assistant, https://github.com/cameronpcampbell/supercorner (read: READMEs)
- GitHub search API metadata (read) for the repositories in the converters table (framework and tooling repositories are listed in `ui-input-crossplatform.md`)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `05 UI and UX/UI Motion Language and Timing.md`, `Menu Archetypes - Shop Settings Codes Rewards.md`, `Notification and Toast Systems.md`, `HUD Design.md`, `Virtualized Lists and Large Inventories.md`, `UI Design Systems.md`, `UI Style Directions - A Visual Vocabulary for Briefs.md`, `Text Fonts and Rich Text.md`, `Settings Menu Design for Roblox - Layout, Controls and Motion.md`, `Figma Property Mapping for Roblox UI.md`, `Figma to Roblox UI - Pipeline and Handoff.md`, `Designing Roblox UI in Figma - Frames, Safe Areas and Tokens.md`, `Responsive UI for Phone Tablet Console and PC.md`; `56 Field Notes/` (Centre-Screen Announcements, Shared Close Buttons and Headers, Streaming Joins and Loading Screen Teardown, UIStroke on Text); `21 LihFolk UI Design System/` (read for method only; its palette, kit and icon style were not adopted); `skills/lihfolk-figma/SKILL.md`, `skills/lihfolk-ui/SKILL.md`, `skills/roblox-ui-builder/SKILL.md` (read)
- https://github.com/Fraktality/spr (read: README)
- Figma MCP tool descriptions as exposed in this session (read): `create_session`, `create_new_file`, `use_figma`, `get_metadata`, `get_design_context`, `get_variable_defs`, `get_screenshot`, `download_assets`, `get_figma_skill`
- https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ (search summary)
- https://devforum.roblox.com/t/full-release-ui-styling-is-officially-released/4275082, https://devforum.roblox.com/t/full-release-stylequery-more-styling-features/4566519, https://devforum.roblox.com/t/full-release-styling-transitions/4646870 (search summary)
- https://devforum.roblox.com/t/studio-beta-uistroke-improvements-scaling-offsets-and-more/3958036, https://devforum.roblox.com/t/weekly-recap-april-20-24-2026/4596790 (search summary)
- https://devforum.roblox.com/t/importing-ui-from-figma-sucks/3381689, https://devforum.roblox.com/t/free-figma-to-roblox-plugin-roimport/4731967, https://devforum.roblox.com/t/plugin-uilint-v2-import-figma-ui-into-roblox-studio/4765869, https://devforum.roblox.com/t/bloxporter-beta-paid-fast-figma-roblox-with-custom-configurations/3501193, https://devforum.roblox.com/t/guiforge-roblox-ui-editorfigma-export/4834077, https://figbloxui.pages.dev/changelog/ (search summary)
- https://devforum.roblox.com/t/why-is-the-max-image-resolution-1024x1024/1679078, https://devforum.roblox.com/t/retaining-high-fidelity-images/3042460 (search summary)
- https://devforum.roblox.com/t/how-tall-is-the-roblox-top-bar/3248916, https://devforum.roblox.com/t/what-are-the-new-topbar-inset-dimensions/3237388 (search summary)
- https://devforum.roblox.com/t/uiscale-scaling-a-text-with-scaled-size-uistroke-bug/4238464, https://devforum.roblox.com/t/introducing-text-scaling-setting-studio-beta/3136967 (search summary)
- https://devforum.roblox.com/t/ui-design-guide/2975811, https://sozai.app/transcript/make-roblox-ui-look-better/ (search summary)
- Not reachable directly: reddit.com, devforum.roblox.com, create.roblox.com, figma.com (blocked); no usable r/robloxgamedev thread surfaced through search.
