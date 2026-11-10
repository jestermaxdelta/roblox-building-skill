# UI, input, cross-platform and accessibility

Engine-side rules for Roblox UI and input: HUD and menu principles, containers and safe areas, sizing, text, mobile/console/VR layout, input mapping and accessibility, plus a symptom table and an audit scan for live games. Open it when building or auditing any screen or control scheme; open `ui-design-figma.md` for visual design, tokens, patterns with sizes and the Figma hand-off. Distilled from knowledge-base sections 2.3, 2.5, 5.10 and 5.11, re-verified against `Roblox/creator-docs` on 2026-11-10. Tags: `[official]` Roblox docs, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0, rewritten), `[VS]` version-sensitive (several UI and input systems are new), `[house]` house estimates.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) One ScreenGui per screen, directly under `StarterGui`, `ResetOnSpawn = false`, default `CoreUISafeInsets`. (2) Scale position + `AnchorPoint`, square things with `UIAspectRatioConstraint`. (3) Buttons use `Activated`; text uses fixed `TextSize`. (4) Keep clear of the thumbstick and jump zones. (5) Run the UI audit scan and test in the phone emulator. | Frameworks, style sheets, virtualised lists, VR |
| Intermediate | One presenter and a written `DisplayOrder` band plan; a sizing strategy with a text floor; every action on keyboard, gamepad and touch; gamepad focus rules; the three accessibility preferences; the measured pass criteria at six viewports | Custom navigation code, declarative libraries |
| Expert | State-driven, interruption-safe windows; zero idle per-frame Lua; MicroProfiler-led budgets; virtualised lists with index-based selection; snapshot-and-delta replication; automated overlap and tap checks that call the real placement code; the conflict notes | Nothing: re-verify every `[VS]` |

Terms: a **ScreenGui** is the container for on-screen UI; **Scale** sizes are fractions of the parent and **Offset** sizes are pixels; a **safe area** is the part of the screen clear of notches and Roblox's own top bar; a **presenter** is the module that opens and closes windows; **virtualising** a list means creating only the visible cells.

## Contents

UI design principles · Containers, insets and sizing · UI architecture (state, mounting, controllers, frameworks) · UI performance · Text, numbers and localisation · Text filtering · Proximity prompts · Input · Mobile layout · Gamepad and console · VR · Accessibility · Level-up symptom table · UI audit scan · Review gate · Sources

## UI design principles

- HUD hierarchy: always visible (health, currency, timer), on change (toasts, count-ups), on demand (inventory, shop, settings). Keep the HUD to 5–7 elements.
- Diegetic UI (a sign, a screen on a Blender-modelled board with a `SurfaceGui`) beats floating panels for immersion; non-diegetic for anything that must be read instantly.
- Menus are a stack (push/pop), so Back always returns to where the player was.
- Feedback states for every control: idle, hover, pressed (100–150 ms), disabled, success, error.
- Readability (XAG): text ≥ 26 px at 1080p on TV, ≥ 18 px on PC, scalable to 200%; contrast 4.5:1 for text and 3:1 for large text and icons; never colour alone (pair rarity colours with labels or icons); touch targets about 9 mm or larger; allow +30% width for localisation.
- Anti-patterns: modals during play, more than 5–7 HUD elements, counters that snap instead of count up, the shop button under the thumb, perpetual decorative motion.
- Event-driven HUD: listen to `player:GetAttributeChangedSignal("Coins")` and tween a NumberValue to count up; update text only when values change and throttle counters to about 10 Hz.
- `BillboardGui` with `MaxDistance` for world labels; pool them.
- A 10-dimension UX review with P0–P3 severities (learnability, efficiency, feedback, error prevention, consistency, readability, accessibility, input parity, performance, monetization honesty) belongs in every milestone review (see process-and-playtesting.md).

Offer surfaces under house rule 3: small cards (≤ 25% of the screen) in a safe-area corner outside thumb zones, dismissible with an X, after positive moments only, never in the first minutes or on the loading screen, rate-limited (≥ 8 min apart, ≤ 3 per session), never stacked, no sound stings; the shop is always one tap away from a HUD button; boost timers show honest remaining time.

## Containers, insets and sizing `[VS]`

- A `ScreenGui` in `StarterGui` clones into `PlayerGui` on first spawn. Set `ResetOnSpawn = false` for HUDs, shops and menus, and keep each ScreenGui a **direct child** of `StarterGui`: one placed inside a Folder is re-cloned on every respawn whatever the property says `[official]`, which closes open windows and leaves controllers holding destroyed instances. One ScreenGui per screen; toggle `ScreenGui.Enabled` (a disabled ScreenGui neither renders nor takes input); layer with `DisplayOrder`.
- `ScreenGui.ScreenInsets`: `CoreUISafeInsets` (default; use for anything interactive), `DeviceSafeInsets` (clears notches, not the top bar), `TopbarSafeInsets` (the strip between the top-bar controls and the right safe edge; flexes with the bar), `None` (full-bleed backgrounds only). Query insets with `GuiService:GetGuiInset()`.
- `IgnoreGuiInset = true` now only switches `CoreUISafeInsets` to `DeviceSafeInsets` `[official]`: it ignores the top bar but still respects the notch, so it is not fullscreen. Set `ScreenInsets` explicitly on every ScreenGui. Set `SafeAreaCompatibility = None` on new guis: the default `FullscreenExtension` stretches anything that looks fullscreen and the docs advise against it for new work `[official]`. `ClipToDeviceSafeArea` (default true) cuts overhangs at the safe edge and is ignored under `None`.
- Two-layer pattern `[lihfolk]`: edge-to-edge art (dimmer, vignette, letterbox, loading cover) in its own `ScreenInsets = None` ScreenGui that no scaler touches; controls in a safe-area ScreenGui one `DisplayOrder` above; open and close them together. Debug aid: a bright translucent full-size frame in each gui shows the area it thinks it owns.
- `GuiService.TopbarInset` is a `Rect` of the free top-bar area and changes at runtime (health bar, `SetCoreGuiEnabled`): listen with `GetPropertyChangedSignal` `[official]`. Reported top-bar heights are 58 px on large screens, 48 px on phones, none on console, and inset reads of 0 on the first frame `[community][VS]`: never hard-code a top-bar height and never read insets once at startup.
- Screen class: `GuiService.ViewportDisplaySize` is `Small` (most phones, tablets, handhelds), `Medium` (laptops, monitors) or `Large` (TVs); listen for changes `[official]`. Do not use `GuiService:IsTenFootInterface()` to detect console `[official]`.
- Sizing rules: scale position plus matching `AnchorPoint` for edge-relative elements (`AnchorPoint (1,0)`, `Position UDim2.new(1,-16,0,16)` for a 16 px top-right margin); scale size plus `UIAspectRatioConstraint` for shape; `UISizeConstraint` for min and max; fixed `TextSize` with `UITextSizeConstraint` rather than `TextScaled` for body text; `AutomaticSize` for content-driven panels (Size becomes the minimum); `ScrollingFrame` with `AutomaticCanvasSize` and `CanvasSize = 0`; `UIScale` on a root frame only as a final global multiplier.
- Gotcha: a `UIAspectRatioConstraint` overrides a layout's sizing.

| Need | Use | Why |
|---|---|---|
| Position against a screen edge | Scale position + matching `AnchorPoint` + small px offset margin | Pixel count and density vary arbitrarily across devices `[official]` |
| Size of buttons, icons, slots | Scale on the short axis + `UIAspectRatioConstraint` (or `SizeConstraint = RelativeYY`) | Scale on both axes stretches shapes on 19.5:9 phones |
| Size of windows | Scale + `UISizeConstraint` max | 75% width is huge on a 4K TV `[official]` |
| Margins, padding, gaps, stroke width | Offset (px) | Small fixed spacing reads the same everywhere; scale padding collapses on phones |
| Whole-HUD multiplier (TV, user "UI size" slider) | One `UIScale` on the root frame | Final multiplier, not the layout system |
| Layout swap by device | `ViewportDisplaySize` breakpoints or `StyleQuery` selectors (`@ViewportDisplaySizeSmall`, `@PreferredInputTouch`) `[official][VS]` | Shrinking a desktop panel never produces a phone layout |

- **Conflict:** community Figma-import skills demand "Scale only, Offset 0" and `AnchorPoint (0.5, 0.5)` everywhere `[community]`. House position: the table above. Offset stays for margins, padding and strokes; anchors follow intent (edge-pinned HUD anchors on its edge; anything that scale-tweens anchors at the centre).
- **Sizing strategies.** A: Scale + constraints + px margins (table above); best for HUD pieces pinned to edges. B `[lihfolk]`: author a window entirely in Offset at one design frame and put one fit `UIScale` on its root, `Scale = clamp(min(viewport.X / design.X, viewport.Y / design.Y), floor, ceiling)`; proportions, strokes and corners stay exact (`UIScale` scales its subtree including `UIStroke` and `UICorner` `[official]`) and Figma pixels map 1:1. The floor is the number that matters: `floor = 12 / smallestAuthoredTextPx`. A 1920×1080 design shrunk to 667×375 has scale 0.347, so 18 px text draws at 6 px; either design at the phone frame (scale ≥ 1 everywhere, cap the ceiling so windows stay under about 70% of a TV) or give that screen a real phone arrangement. Never let one global `UIScale` without a floor be the phone strategy.
- `UIScale` rules `[lihfolk]`: two on one branch multiply, so the device scale goes on the root and a pop/press scale on an inner frame, never two on one object. Hit-testing uses the scaled size: scale a button's visual child, keep the hit area full size, and give small phone buttons an invisible tap pad of at least 44 px (`Selectable = false`).
- How a size resolves (when an object ignores the size you set, walk this list) `[lihfolk]`: `Size` from the parent honouring `SizeConstraint` → a layout's size (flex, grid cell) → `UISizeConstraint` and `UIAspectRatioConstraint` → `AutomaticSize` growth with `Size` as the minimum → every ancestor `UIScale` → `Position` and `AnchorPoint`. Never combine `TextScaled` with `AutomaticSize`, and do not read `AbsoluteSize` in the frame you set `Size`.
- Pixel snapping `[lihfolk]`: offsets snap to whole pixels after scaling, so an odd-sized child cannot be exactly centred in an even parent and a 3 px stroke at scale 0.85 renders soft. Lift descender-heavy captions by 1 px on purpose and record it as an attribute so audits accept it.
- Modifier limits `[official]`: `UICorner` cannot be applied to a `ScrollingFrame`, and it clips input but not descendants (use a `CanvasGroup`, or 9-slice art, for rounded clipping). `ClipsDescendants` does not clip rotated children `[community]`. Do not tween `UIStroke.Thickness` on text (re-renders glyphs every frame). Flex adds a slight layout cost over plain lists; use `UIGridLayout` when cells must align on both axes.
- `CanvasGroup` `[official]`: flattens only when the ScreenGui uses `ZIndexBehavior.Sibling`; consumes extra texture memory capped by the client's quality level and renders **blank** past the cap; keep its size static.
- `UIStroke` `[VS]`: fixed-pixel strokes look thicker on small screens; `StrokeSizingMode = ScaledSize` (Improved UIStrokes beta) scales with the parent's short side. The beta announcement is reported to recommend fewer than 300 UIStrokes on screen for low-end devices; a figure of about 100 UIShadows circulates second-hand `[community]`. Budget both. Whether strokes follow a root `UIScale` has conflicting reports: test on a device.
- New instances `[official][VS]`: `UIDragDetector` (sliders, spinners and draggable panels on every input without code), `Path2D` (2D splines for path animation and curved connectors), radial/elliptical/conical `UIGradient` types (beta), per-corner `UICorner` radii (beta), styling transitions and the Style Editor. Check the beta list before shipping any of them.
- Layouts: `UIListLayout` (with flex and `UIFlexItem`), `UIGridLayout` (compute `CellSize` from `AbsoluteSize`), `UITableLayout` (tabular data only), `UIPageLayout` (carousels), `UIPadding`. Use explicit breakpoints (for example switch a category list from vertical to horizontal under about 700 px width) rather than shrinking desktop panels.
- Styling: `UICorner`, `UIStroke`, `UIGradient`, 9-slice, `UIShadow` (new, partly beta). Sprite sheets via `ImageRectOffset`/`ImageRectSize`. The UI styling system (`StyleSheet`, `StyleRule`, `StyleLink`, `StyleDerive`, `StyleQuery`, tokens like `$Accent`) gives one place to re-skin; define a small token sheet and drive buttons with tag selectors. Status `[VS]`: the styling APIs and Style Editor are fully released for live experiences, `StyleQuery` (media and container queries in one) followed in May 2026 and styling transitions in July 2026 (DevForum announcements, seen through search).
- Motion: `TweenService` on the client for state changes only; 0.1–0.3 s for feedback, ≤ 0.75 s for panel transitions; honour `GuiService.ReducedMotionEnabled` (tween time 0 or fade instead of slide).
- Framework choice, authoring strategy and the presenter: §UI architecture below.
- Performance: hidden screens `Enabled = false`; avoid UIGradient and UICorner on constantly changing text (`fillGuiVertices`); `CanvasGroup` for complex static panels (costs memory; do not nest); icons ≤ 256² in sprite sheets; load menu art lazily; interactive `SurfaceGui`s stay in `StarterGui` with `Adornee` set to the Blender board mesh.
- Long lists `[community]`: a `ScrollingFrame` with about 1,000 or more cells scrolls badly, and mass-parenting buttons into a `UIGridLayout` is reported to freeze. Thresholds, budgets and the virtualising pattern: §UI performance and `ui-design-figma.md` §Inventory. Build a list on first open, not at join `[official]`.
- Image memory follows pixel count, not file size (a 1024² image costs 4× a 512²) `[official]`; export rules are in `ui-design-figma.md`.

## UI architecture: state, mounting, controllers

The shape that survives growth past a handful of screens:

`server truth → replication → one client store → screens (read only) → requests → server`, with one presenter owning open/close, bands, focus and the back action.

- **The server owns the facts.** UI mirrors replicated data (attributes, a profile replica, snapshot-then-delta remotes) and sends requests; it never decides currency, items or ownership. Labels bind to server values, not local guesses.
- **One client store** holds the replicated profile, session state, the device profile (layout family and input kept separate) and preferences (reduced motion, text size). Screens subscribe; they do not talk to each other.
- **One boot script** in `StarterPlayerScripts` requires the controllers. No LocalScripts inside screens.
- **One presenter** opens and closes windows: one window at a time, HUD hidden on phones while a window is open, a stack only for genuine drill-down (shop → item detail). `[lihfolk]`
- **One entry point per transient channel**: notifications, centre banners and floating numbers each go through a module that queues, merges and gates (`ui-design-figma.md` §Notifications).
- **Requests carry a pending state.** Every claim, buy, redeem and save button is non-interactable from tap until the server answers. `[lihfolk]`
- **Find instances by tag or attribute, not by name.** Tutorial pointers, tap pads and controllers that look up `ShopButton` by name break silently when a redesign renames it; use a CollectionService tag or an attribute such as `UiHook = "hud_shop"`. `[lihfolk]`

Authoring strategies:

| Strategy | Good for | Fails when |
|---|---|---|
| Authored in Studio (or generated from Figma), code wires behaviour | Art-heavy windows, HUD | Many near-identical items; layout differs per device |
| Templates authored once, cloned and filled by code | Cards, rows, toasts: most games | Templates drift from what code expects: assert child names at boot |
| Built entirely in code, or a declarative library | Data-driven lists, many states, several UI programmers | Artists must tweak pixels and cannot |

- **Each property has exactly one owner**: the saved instance or the code, never both. The costliest failure LihFolk records is the accidental fourth strategy, a saved copy plus a runtime rebuild: Play looked right while every edit-mode audit read a stale saved copy (137 differing properties before it was re-baked). `[lihfolk]`
- **Mounting.** Build a window on first open, then keep it alive and toggle `ScreenGui.Enabled`; destroy-and-recreate pays the creation spike on every open. Destroy only when memory matters more (leaving a lobby for a match). Idle loops and per-frame connections start on open and stop on close.

`DisplayOrder` band plan `[house]` (write it down once; `ZIndex` never crosses ScreenGuis `[official]`):

| Band | DisplayOrder | Contents |
|---|---|---|
| World overlays | 0–9 | Screen-space damage numbers, markers, crosshair |
| HUD | 10–19 | Currency, menu column, tracker, offer card |
| Windows | 20–49 | Shop, inventory, settings (one open) |
| Toasts and banners | 50–69 | Toast lane, centre banner |
| Confirm dialogs | 70–79 | Rebirth, delete, purchase confirmation |
| Tutorial | 80–89 | Spotlight, pointer: above everything it can point at `[lihfolk]` |
| Loading and transitions | 100+ | Covers everything |

- A higher `DisplayOrder` draws on top but does not block input. A modal needs a full-screen frame with `InputSink = Enum.InputSink.All` under the window; a plain Frame sinks nothing (`InputSink.None`), buttons sink only activation `[official][VS]`. The blocker's own `InputBegan` still fires, which gives tap-outside-to-close.
- Use `GuiButton.Activated` (mouse, touch and gamepad), not `MouseButton1Click`; set `Interactable = false` for disabled and pending buttons; every `UserInputService` gameplay handler returns early on `gameProcessedEvent`. `[lihfolk]`
- New ScreenGuis use `ZIndexBehavior.Sibling` (hierarchy is draw order). In a legacy `Global` gui a new label can sit under its own background; do not flip a large gui's mode in place. `[lihfolk]`

Motion and presenter (unexecuted sketch; token values and rules in `ui-design-figma.md` §Motion spec; approach adapted from LihFolk's motion and ScreenGui notes `[lihfolk]`, rewritten):

```lua
--!strict
-- Shared/UI/Motion.luau: the only place a UI TweenInfo is created.
local GuiService = game:GetService("GuiService")
local TweenService = game:GetService("TweenService")

export type Token = "press" | "release" | "hover" | "enter" | "exit" | "move"
local Out, In = Enum.EasingDirection.Out, Enum.EasingDirection.In
local TOKENS: { [Token]: TweenInfo } = {
	press = TweenInfo.new(0.08, Enum.EasingStyle.Quad, Out),
	release = TweenInfo.new(0.2, Enum.EasingStyle.Back, Out),
	hover = TweenInfo.new(0.11, Enum.EasingStyle.Quad, Out),
	enter = TweenInfo.new(0.22, Enum.EasingStyle.Back, Out),
	exit = TweenInfo.new(0.13, Enum.EasingStyle.Quad, In),
	move = TweenInfo.new(0.28, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut),
}
-- Spatial properties jump to the goal under reduced motion; colour and transparency still fade.
local SPATIAL: { [string]: boolean } = { Position = true, Size = true, Rotation = true, Scale = true, Offset = true }
local Motion = { userReduced = false } -- in-game toggle on top of the platform setting

function Motion.reduced(): boolean
	return Motion.userReduced or GuiService.ReducedMotionEnabled
end

-- fraction (0–1) shortens a retargeted tween. Returns nil when nothing is left to animate.
function Motion.play(target: Instance, token: Token, goal: { [string]: any }, fraction: number?): Tween?
	local base = TOKENS[token]
	local info = TweenInfo.new(base.Time * math.clamp(fraction or 1, 0.3, 1), base.EasingStyle, base.EasingDirection)
	if Motion.reduced() then
		local fades: { [string]: any } = {}
		for property, value in goal do
			if SPATIAL[property] then (target :: any)[property] = value else fades[property] = value end
		end
		if next(fades) == nil then return nil end
		goal, info = fades, TweenInfo.new(math.min(info.Time, 0.15), Enum.EasingStyle.Linear)
	end
	local tween = TweenService:Create(target, info, goal)
	tween:Play()
	return tween
end
return Motion
```

```lua
--!strict
-- Client/UI/Presenter.luau: one window open; state-driven, so rapid toggling ends in the last requested state.
local ContextActionService = game:GetService("ContextActionService")
local GuiService = game:GetService("GuiService")
local UserInputService = game:GetService("UserInputService")
local Motion = require(script.Parent.Motion)

type Window = { gui: ScreenGui, face: CanvasGroup, scale: UIScale, firstFocus: GuiObject?, wantOpen: boolean }
local windows: { [string]: Window } = {}
local current: Window? = nil
local Presenter = {}

local function animate(w: Window)
	if w.wantOpen then
		w.gui.Enabled = true -- input and gamepad focus work from the first visible frame
		if w.firstFocus and UserInputService.PreferredInput == Enum.PreferredInput.Gamepad then
			GuiService.SelectedObject = w.firstFocus
		end
		local remaining = math.clamp((1 - w.scale.Scale) / 0.1, 0, 1) -- proportional retarget
		Motion.play(w.scale, "enter", { Scale = 1 }, remaining)
		Motion.play(w.face, "enter", { GroupTransparency = 0 }, remaining)
	else
		Motion.play(w.scale, "exit", { Scale = 0.9 })
		local fade = Motion.play(w.face, "exit", { GroupTransparency = 1 })
		local function hide()
			if not w.wantOpen then w.gui.Enabled = false end -- still wanted closed?
		end
		if fade then
			fade.Completed:Once(function(state)
				if state == Enum.PlaybackState.Completed then hide() end
			end)
		else
			hide()
		end
	end
end

local function updateBack()
	-- Bound only while a window is open, so gamepad B stays free for gameplay (a dash, a dodge) otherwise.
	if current then
		ContextActionService:BindActionAtPriority("UiBack", function(_, state)
			if state == Enum.UserInputState.End then Presenter.set(nil) end -- close on release: press and release are both sunk
			return Enum.ContextActionResult.Sink
		end, false, Enum.ContextActionPriority.High.Value, Enum.KeyCode.ButtonB)
	else
		ContextActionService:UnbindAction("UiBack")
		GuiService.SelectedObject = nil -- hand the stick back to the character
	end
end

function Presenter.register(name: string, w: Window)
	windows[name] = w
	w.gui.Enabled, w.scale.Scale, w.face.GroupTransparency = false, 0.9, 1
end

-- Presenter.set("Shop") opens it and closes whatever was open; Presenter.set(nil) closes.
function Presenter.set(name: string?)
	local nextWindow = if name then windows[name] else nil
	if current and current ~= nextWindow then
		current.wantOpen = false
		animate(current)
	end
	current = nextWindow
	if nextWindow then
		nextWindow.wantOpen = true
		animate(nextWindow)
	end
	updateBack()
end
return Presenter
```

`face` is the window's root `CanvasGroup` (one per open window is affordable; see UI performance) holding an inner `UIScale` for the pop, separate from any device `UIScale` on the ScreenGui root. Extend with the modal blocker, restore-focus-to-opener and a drill-down stack as needed.

Frameworks and tooling (GitHub activity on 2026-11-10):

| Option | Status | Use when |
|---|---|---|
| Plain instances + Theme + Motion + Presenter | n/a | **Default.** Screens stay visible in Explorer, editable by the Studio MCP and the Style Editor; state is a handful of attributes and signals |
| `StyleSheet` tokens, `StyleQuery`, transitions | Engine; styling fully released, StyleQuery May 2026, transitions July 2026 `[community][VS]` | Re-skinning Studio-authored screens; swaps by `@ViewportDisplaySizeSmall` / `@PreferredInputTouch` `[official]` |
| Vide (`centau/vide`) | 355★, pushed 2026-10, MIT | Many dynamic lists and derived state; small reactive core |
| React (`Roblox/react-luau` read-only mirror; `jsdotlua/react-lua`) | 589★ pushed 2026-10; 582★ pushed 2025-05 | The team already thinks in React; large UI codebase |
| Fusion (`dphfox/Fusion`) | 813★, pushed 2026-02, MIT | Existing Fusion codebases; `Hydrate` binds state onto Studio-authored templates |
| Roact (`Roblox/roact`) | Archived 2023-12 | Never for new work |
| Storybooks: `flipbook-labs/flipbook` (MIT), `PepeElToro41/ui-labs` (GPL-3.0), `Kampfkarren/hoarcekat` | 124★ / 202★ / 148★ | Any code-built component library: preview states without playtesting |
| Springs: `fraktality/spr` (2024-07), `littensy/ripple` (2026-07); `Reselim/Flipper` (2021-11, stale) | 146★ / 137★ / 144★ | Motion that is retargeted mid-flight |

- Declarative libraries pay off with many states, data-driven lists or several UI programmers; a few static windows do not need one. Their cost is learning and tooling, not runtime; the cost of imperative UI is state bugs that grow with every feature. `[lihfolk]`
- Traps in any library `[lihfolk]`: animating through component state (60 re-renders a second: tween instances instead); lists keyed by index (instances are recreated on reorder: key by item id); connections not cleaned up when a screen closes; derived values that loop over the whole inventory on every change; 600 declarative cards are still 600 sets of instances, so virtualise.
- **Conflict:** this file once named Fusion 0.4 as the "bold" option. By repository activity Vide and react-luau are the actively maintained choices and Fusion is quieter. The default does not change. Pick a library only when more than about five screens share live state or lists exceed a few hundred rows, and recheck activity first `[VS]`.

## UI performance

Where UI time goes, and the MicroProfiler label that shows it `[official]`:

| Cost | Trigger | Label | Fix |
|---|---|---|---|
| Layout passes | Children added, removed, resized or reordered under a layout; `Size` tweens; scale-sized BillboardGuis | `UpdateUILayouts/Layout` (shows relayouts, updates, resizes) | Tween a `UIScale` or an inner face instead of `Size`; fixed sizes for billboards; virtualise long lists |
| Z-order rebuild | Parenting or `ZIndex` changes in a large ScreenGui | `UpdateUILayouts/Rebuild Z-order list` | Fewer elements per ScreenGui; do not reparent or change `ZIndex` at runtime |
| Vertex fill | Many visible elements; gradients and corners on text | `Perform/fillGuiVertices` (gui count; `Process GuiEffect`) | Fewer, sparser elements; no `UIGradient`/`UICorner` on changing text |
| World-space UI | Every visible BillboardGui and Humanoid name label | `Prepare/Pass3dAdorn` | `MaxDistance`, pooling, declutter by distance |
| Text shaping | Any text write; `TextScaled` during a size change | inside layout and fill | Write on change only; no `TextScaled` in animated boxes |
| Render-cache invalidation | A ScreenGui's appearance is cached until any descendant changes `[official]` | whole gui re-composed | One spinning icon re-composes its whole ScreenGui every frame: put constantly animated pieces in their own small ScreenGui `[lihfolk]` |
| Texture memory | Large images, one upload per colour, `CanvasGroup`s | Developer Console memory | ≤ 1024 px, sprite sheets, tints, few static CanvasGroups |
| Lua per frame | `RenderStepped` springs, polling loops, timers | script time | Budget below |

Budgets (`[lihfolk]` field values unless tagged; treat as starting points and measure):

| Item | Budget |
|---|---|
| Per-frame Lua with the UI idle | 0 connections. Springs share one connection that exists only while something is unsettled |
| Text updates | On change only; counters ≤ 10 Hz, countdowns about 4 Hz, countdowns in closed windows not at all |
| Decorative loops | Engine tweens (`RepeatCount = -1`) rather than Lua loops, cancelled when the screen closes: infinite tweens keep running while hidden |
| Instances per list card | 10–20. 50 cards: nothing felt; 300: a few frames to open; 1,000 (about 15,000 instances): stalls and visible layout passes; 3,000: unusable on phones |
| Plain layout vs virtualised | Under about 100 entries plain; above about 300, or unbounded, virtualise with `visible + 2 buffer rows` cells positioned by code (no layout object) |
| `CanvasGroup` | 1–2 visible, never nested, static size; text inside can look soft |
| `UIStroke` / `UIShadow` on screen | Under 300 / about 100 `[community][VS]` |
| Floating numbers | Pool of about 12, merged within about 0.5 s |
| `ViewportFrame` | One in a detail pane or featured slot; none per list cell |
| World labels | Created on the client, always `MaxDistance`, anchored to an attachment; custom nametags turn the built-in one off (`Humanoid.DisplayDistanceType = None`); nothing `AlwaysOnTop` for enemies |
| Preload | Only the first screen's fonts and icons (`ContentProvider:PreloadAsync`); everything else on first open |

Getting list data to the client `[lihfolk]`: send a snapshot after the client reports ready (not in `PlayerAdded`, where it can arrive before the listener exists), then small deltas with a sequence number; ignore older deltas and request a fresh snapshot on a gap. Send ids and counts only, since names and icons live in a shared definitions module. Replicating thousands of Value instances is slow and costs memory on both sides. Remote design: `networking-and-security.md`.

Measure, in this order: (1) real low-end phone at its lowest graphics level; (2) MicroProfiler while idle with everything closed (the cost should be near zero); (3) open the busiest window and watch the layout and fill labels during the entrance; (4) fire the notification burst test; (5) scroll the largest list; (6) memory tab before and after opening every window once. Frame budgets and capture workflow: `performance.md`.

## Text, numbers and localisation

- Body text: fixed `TextSize` + `TextWrapped` + `AutomaticSize`. With `GuiService.PreferredTextSize` the engine enlarges such text and auto-sized bounds grow; `TextScaled` text is **not** scaled by the setting, and a `UITextSizeConstraint` clamps it `[official]`.
- `TextScaled` only for short numerals and titles in fixed boxes, always with `UITextSizeConstraint` (min and max). Without a cap, labels of equal size render different text sizes by string length (DevForum reports, thread not individually identified) `[community]`.
- Type floor `[house]`: HUD numbers ≥ 18 px, body 16, captions 14 at phone 1×. Outline (`UIStroke`, Contextual) or plate any text over the 3D world `[official]`. Use stylised fonts sparingly: titles and alerts only `[official]`.
- Big numbers: abbreviate (`12.5K`, `3.4M`), fix the decimals, size every label for the largest value; `TextTruncate` as the last resort and `TextFits` to detect overflow in tests.
- `RichText` for inline colour, weight and stroke. Localisation strips rich-text tags, so re-apply them in translated strings `[official]`. One 2025 thread reports the text-size setting breaking non-`TextScaled` RichText labels `[community][VS]`: test it.
- Escape anything a player typed before placing it in a RichText string (`<`, `>`, `&`), or a name containing `<` breaks the markup; escaping is not filtering (next section). For per-letter colour effects animate a `UIGradient.Offset`, not the string. `[lihfolk]`
- Fonts: set `FontFace` with an explicit family and weight. The `Gotham*` enum values were removed and render Montserrat `[official]`. Outline ratio (≤ 7% of text size for rounded heavy fonts) and number formatting rules are in `ui-design-figma.md` §Design system and tokens.
- Scripted text `[lihfolk]`: translate through `LocalizationService:GetTranslatorForPlayerAsync` (in `pcall`) and `Translator:FormatByKey` with parameters, never by concatenating sentence fragments; re-translate when the player's locale changes; set `AutoLocalize = false` on script-filled labels so the table does not fill with "Gems: 1,240". Pseudo-localise to 140% length as a test.
- Localisation `[official]`: Automatic Text Capture collects strings from GUI objects with `AutoLocalize` enabled; turn `AutoLocalize` off on player names and other text that must not translate. Replace unnecessary text with icons, and design each label for the longest translation (+30% width).

## Text filtering (mandatory)

Any text one player writes that others can see is filtered on the server (unexecuted sketch):

```lua
local TextService = game:GetService("TextService")
SetSignText.OnServerEvent:Connect(function(player, raw: string)
	if typeof(raw) ~= "string" or #raw > 60 then return end
	local ok, result = pcall(TextService.FilterStringAsync, TextService, raw, player.UserId)
	if not ok then return end
	local ok2, filtered = pcall(result.GetNonChatStringForBroadcastAsync, result)
	if ok2 then sign:SetAttribute("Text", filtered) end
end)
```

`GetNonChatStringForBroadcastAsync` for text everyone sees; `GetNonChatStringForUserAsync(userId)` for one recipient. If filtering fails, show nothing.

## Proximity prompts

Properties: `ActionText`, `ObjectText`, `KeyboardKeyCode`, `GamepadKeyCode`, `HoldDuration` (0 = instant), `MaxActivationDistance`, `RequiresLineOfSight` (default true), `Exclusivity`, `ClickablePrompt`, `Style = Custom` with `PromptShown`/`PromptHidden` for your own UI. Events: `PromptTriggered`, `PromptButtonHoldBegan`, `PromptButtonHoldEnded`.

Parent prompts to a Blender-authored `Prompt_Att` attachment (or an invisible anchored anchor part, an allowed helper) inside an **Atomic** model so the prompt survives streaming. Prompts are the mobile-friendly context UI: show "Open" or "Deliver" near the object, not as a permanent button. Always re-validate distance, state and cooldown on the server when `Triggered` fires.

## Input: map actions, not keys

- Detect `UserInputService.PreferredInput` `[VS]` (`Touch`, `KeyboardAndMouse`, `Gamepad`, `MicroGamepad`) and listen to its changed signal to swap hints and touch buttons. `TouchEnabled` is true on touch laptops and `GetLastInputType()` thrashes, so neither is an "is mobile" check.
- Input Action System `[VS]`: `InputContext` (groups of actions with `Priority` and `Sink`), `InputAction` (`Bool`, `Direction1D`, `Direction2D`, `Direction3D`, `ViewportPosition`; events `Pressed`, `Released`, `StateChanged`; `PreferredBinding` for the right key icon), `InputBinding` (keyboard `KeyCode`, gamepad button, touch `UIButton`, composite Up/Down/Left/Right, `MouseDelta`/`TouchDelta` with `Scale`). Set `Workspace.PlayerScriptsUseInputActionSystem` for default scripts. `ContextActionService:BindAction` still works for legacy code. Bind actions only while the owning screen or tool is active.
- Key ownership `[lihfolk]`: Shift is taken by Roblox's shift-lock toggle when `StarterPlayer.EnableMouseLockOption` is on, so sprint on Shift flips the camera lock on every press: move sprint, or disable the option and provide your own lock. Gamepad B as "close window" is bound only while a window is open (Presenter sketch above), or it eats a dash bound to B; disable combat actions while a modal window is open.
- Rule: every action has a keyboard, a gamepad and a touch binding. Exclude reserved keys (Escape, the Roblox menu key, chat) from rebinding.
- Feel: distinguish edge (pressed this frame) from held; radial deadzone about 0.2 with a response curve exponent 1.5–2; input buffer 100–150 ms; coyote time 80–120 ms; prompts switch to the last used device with positional gamepad names.

Jump buffer plus coyote time, unexecuted sketch (client; the Humanoid jump arc itself is fixed):

```lua
local BUFFER, COYOTE = 0.12, 0.10
local lastJumpPress, lastGrounded = -math.huge, -math.huge
ContextActionService:BindActionAtPriority("JumpBuffer", function(_, state)
	if state == Enum.UserInputState.Begin then lastJumpPress = os.clock() end
	return Enum.ContextActionResult.Pass
end, false, Enum.ContextActionPriority.High.Value, Enum.KeyCode.Space, Enum.KeyCode.ButtonA)
humanoid.StateChanged:Connect(function(_, new) if new == Enum.HumanoidStateType.Jumping then lastJumpPress = -math.huge end end)
RunService.Heartbeat:Connect(function()
	local now = os.clock()
	if humanoid.FloorMaterial ~= Enum.Material.Air then lastGrounded = now end
	if now - lastJumpPress <= BUFFER and now - lastGrounded <= COYOTE then
		lastJumpPress = -math.huge
		humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
	end
end)
```

## Mobile layout

- Reserved zones: thumbstick bottom-left, jump button bottom-right. Keep vital information and custom buttons out of both.
- Place frequent actions relative to the jump button (for example 20 px to its left, 0.8× its size, after it exists and `IsLoaded`), not at a fixed screen percentage; a button 40% from the top works on a phone but not a tablet.
- House touch rule: custom buttons at least 0.8× the jump button, ≥ 8 px gaps, HUD text ≥ about 18 px at 1× on a phone; test portrait and landscape if both are allowed.
- Context-based UI: show only what matters now; prompts for object actions.
- Thumb reach `[official]`: most players hold the phone with two thumbs on the stick and the jump button; frequent buttons sit within reach of the bottom corners without entering the reserved zones, read-only status goes top-centre. Reach differs between phone and tablet, hence jump-relative placement.
- Field reports `[community]`: the dynamic thumbstick area covers about 20–25% of the left side; a button beside the stick gets opened by accident (one simulator review: the joystick kept triggering the spin menu); mobile chat, when opened, covers a large part of the screen. Keep the left-edge column above the stick zone and test with chat open.
- The default jump button is reported at about 70 px on small screens, with a larger variant (about 120 px) on big ones `[community][VS]`: read the live `JumpButton` size, never hard-code it.
- Orientation: lock it with `StarterGui.ScreenOrientation` (`LandscapeSensor` for most games) unless a portrait layout was designed; `PlayerGui.CurrentScreenOrientation` reports the live value `[official]`.
- Pass criteria, measured on the drawn result after all scaling `[lihfolk]`: text ≥ 12 px, tap targets ≥ 44 px (48 for HUD buttons), gaps ≥ 8 px, zero overlaps between interactive objects, nothing off-screen. The docs' own floor is "no `MinTextSize` under 9" `[official]`; 12 is stricter on purpose. **Conflict:** this file's design floor is 14 px captions at the phone frame `[house]`; keep 14 as the design target and 12 as the hard fail line.
- Viewports for every pass `[lihfolk]`: 1920×1080, 1366×768, 1024×600, 932×430, 844×390 (also notched, both landscape orientations), 667×375, plus TV at 1080p with `Large` display size and a gamepad. Automated overlap and tap checks must call the game's real placement code; a check with its own copy of the numbers drifts and goes green while players see overlaps.
- What survives on small phones `[lihfolk]`: not shrinking (fails the text floor) and not zoom-and-pan (players disliked dragging windows that compete with scrolling lists), but a second arrangement of the same instances: pages instead of side-by-side panes, horizontal strips for tabs and filters, bigger cards in fewer columns, and store-set-restore of every touched property so switching back restores the desktop layout exactly.
- Test matrix `[VS]`: Device Emulator, or the Device Simulator beta with Flagship, Mid-range and Entry-level phone presets, then the real 3 GB Android phone. The emulator does not show real thumbs.

## Gamepad and console

- Players sit 8–10 feet from a TV: develop for lower resolutions first, keep UI inside TV-safe areas, use relative positions plus `UISizeConstraint`, check `GuiService.ViewportDisplaySize`, and use ScrollingFrames to reduce clutter.
- Every element reachable with four directions plus select and back. Set `GuiService.SelectedObject` when a menu opens, define `NextSelection*` neighbours, trap focus in modals, keep action sequences short.
- Selection tools `[official]`: `SelectionGroup = true` on a container with `SelectionBehaviorUp/Down/Left/Right` (`Escape` default, `Stop` to trap focus in a modal); `SelectionOrder` for the default pick; `Selectable = false` on decorative buttons; `SelectionImageObject` for a themed focus ring; `GuiService.GuiNavigationEnabled` and `AutoSelectGuiEnabled` for manual control. Groups restrict selection; they do not make unreachable buttons reachable `[community]`.
- Test the default directional selection with a real gamepad or the Controller Emulator before writing custom navigation `[official]`. Known rough edges: explicit `NextSelection*` paths across selection groups, and tweened panels confusing selection `[community][VS]`. Close every window on B and return focus to the button that opened it.
- Invisible helpers are the usual culprit `[lihfolk]`: tap pads, hit areas and click-outside catchers are buttons, so the spatial search lands on them and the focus ring seems to vanish. Set `Selectable = false` on every one. A ring drawn inside a `ClipsDescendants` container is cut off: leave a margin. Debug aid: print `GuiService.SelectedObject:GetFullName()` on `GetPropertyChangedSignal("SelectedObject")`.
- Ten-foot rules of thumb `[lihfolk]`: body text 1.25–1.5× its desktop size and nothing under about 20 px at 1080p (the XAG target above is 26 px: aim for 26, fail under 20); keep important UI out of the outer 5% (overscan); every hover tooltip needs a selection-driven equivalent; shoulder buttons switch tabs; map the two or three most-used HUD actions to buttons and leave the rest to selection; never print "Click".
- Disable the chat window on console. Icons via `UserInputService:GetImageForKeyCode()` and `GetStringForKeyCode()`. Haptics with `HapticEffect` (`GameplayCollision`, `UIClick`), sparingly. Add navigation and selection sounds.

## VR

Target 72 FPS on Quest 2; keep Roblox's comfort settings (vignette, stepped rotation, third-person fixed camera); enable streaming; limit raycasts, semi-transparent objects and complex SurfaceGuis; use `InputAction` rather than key-specific code; test on a real headset. Video thumbnails do not show on VR or console.

## Accessibility and preferences

- Why `[official]`: over 26% of people have some disability and over 5% some colour blindness.
- `GuiService.PreferredTransparency` (1 default to 0 opaque): multiply background transparency by it and listen for changes. Official pattern: tag translucent backgrounds (for example `TransparentBack`), store each default and reapply on change.
- `GuiService.PreferredTextSize` (`Medium` default, `Large`, `Larger`, `Largest`): applied by the engine except to `TextScaled` text, so prefer fixed `TextSize` with `AutomaticSize` and `TextWrapped` for body text. Test every screen at `Largest`.
- `GuiService.ReducedMotionEnabled`: reduce UI motion, camera shake and flashes. Either tween time 0, or swap slides for a fade (`CanvasGroup.GroupTransparency`) `[official]`. Route every UI tween through one helper (`Theme.tween` in `ui-design-figma.md`).
- Offer the same switches in the game's own settings (reduced motion, text size or UI scale, screen-effects intensity): many players never find the platform settings `[lihfolk]`. Keep flashes to at most three per second.
- Colour non-reliance (icon or label with every colour state), sound non-reliance (visual cues for audio events), separate Music, SFX and Ambience sliders.
- Adaptive design: input fluidity (every action on every input, hints match the active input), responsive layout (collapse secondary buttons on small screens), dynamic sizing, legibility on the smallest phone and a distant TV.

## Level-up: UI symptoms → cause → fix

For live games. Confirm the symptom on a real small phone and in analytics before changing anything; fix P0 rows first.

| Symptom | Likely cause | Fix |
|---|---|---|
| Buttons hidden under the notch, top bar or home indicator | `IgnoreGuiInset = true` or `ScreenInsets = None` on interactive UI; hard-coded top-bar offset | `CoreUISafeInsets`; react to `TopbarInset` changes |
| Layout fine in Studio, broken on phones (off-screen, overlapping) | Offset sizes and positions authored on a 1080p viewport | Scale + `AnchorPoint` + aspect constraints; redesign at the phone frame, do not shrink |
| Icons and round buttons stretched on wide phones | Scale on both axes, no `UIAspectRatioConstraint` | Constrain every button, icon and image; 9-slice panels |
| Text tiny on phone, huge on TV, or a different size per label | `TextScaled` without `UITextSizeConstraint`; no breakpoints | Fixed type scale; constraint on scaled numerals; `ViewportDisplaySize` breakpoints |
| Text Size setting does nothing, or clips | `TextScaled` body text; fixed-height boxes | Fixed `TextSize` + `AutomaticSize` + `TextWrapped`; test at `Largest` |
| Translated text overflows or shows raw tags | Labels sized for English; rich-text tags stripped by localisation | +30% width, `AutomaticSize`; re-apply tags per language; icons instead of words |
| Accidental shop or spin opens; mis-taps while moving | Buttons in or beside the thumbstick and jump zones; targets under 44 px; gaps under 8 px | Move to the home edge above the stick zone; primary action jump-relative; enlarge targets |
| "Too much on screen" feedback; players miss the main button | More than 5–7 persistent elements; every button equally loud; offer stacking | One home edge, "More" drawer, contextual HUD, world-space labels, one accent; offer rate limit |
| HUD state lost or duplicated after respawn | `ResetOnSpawn = true`, or the ScreenGui sits in a Folder under `StarterGui`; references to a destroyed clone | `ResetOnSpawn = false` on a direct child of `StarterGui`; controllers bind once to `PlayerGui` |
| Window opens, then vanishes when reopened quickly | Close tween's `Completed` hides the window without checking state | Hide only on `PlaybackState.Completed` and when the intent is still "closed"; drive from `wantOpen` |
| "UI feels laggy" although tweens are short | Input locked until the entrance ends; full enter time after an interrupted close | Accept input from the first visible frame; proportional retarget |
| Clicks pass through a popup to the world or to buttons behind | Backdrop is a plain Frame; modality attempted with `DisplayOrder` | Full-screen blocker with `InputSink.All` |
| A new label or icon is invisible | Legacy `ZIndexBehavior.Global`: it draws under its own background | Raise its `ZIndex` there; build new screens as `Sibling` |
| Coloured squares poke out of rounded corners | `ClipsDescendants` clips to the rectangle, not the `UICorner` | Round or inset the child, or one `CanvasGroup` |
| "10" reads as a blob, "Fast" as "Fust" | Text stroke too thick: glyph holes close | Stroke ≤ 7% of text size on rounded heavy fonts; test string at phone size |
| A wall of identical toasts; toasts still arriving a minute later | No merging, unbounded queue | Kinds with merge rules, capped queue, stale drop (`ui-design-figma.md` §Notifications) |
| Celebration banner over the death screen or tutorial | No popup gate | One centre slot with gating rules |
| Loading screen never leaves for some players | Ready check waits without a timeout, or on a streamed-out instance; two teardown paths | Idempotent teardown plus a watchdog that logs the reason |
| Frame drops when a menu opens or a list scrolls | Thousands of cells built at once; `UIGridLayout` mass-parenting; destroy and recreate each open | Virtualise or paginate, pool cells, build on first open |
| Constant UI cost in the MicroProfiler with nothing open | Text set every frame; perpetual tweens; hidden screens still `Enabled`; many BillboardGuis | Update on change (≤ 10 Hz), stop idle tweens, `Enabled = false`, `MaxDistance` and pooling |
| Panels turn blank on low-end phones | `CanvasGroup` texture memory cap exceeded | Fewer, static-size CanvasGroups; native shapes or 9-slice instead |
| UI images blurry, or client memory high | Upscaled small exports; many large uploads; one upload per colour | Export 2× up to 1024 px; sprite sheets; tint a white base with `ImageColor3` |
| Outlines thick on phone, thin on TV | Fixed-pixel `UIStroke` on scale-sized elements | Per-breakpoint thickness or `ScaledSize` strokes once out of beta `[VS]`; verify under `UIScale` |
| Gamepad or console players stuck in a menu | No initial `SelectedObject`; no B to close; focus escapes the modal or stays on a hidden object | Set selection when the entrance starts, `SelectionGroup` with `Stop`, back action on every screen, clear or restore selection on close |
| Gamepad dash or dodge dead outside menus; first A press does nothing | B bound globally to "close"; selection set only after the entrance | Bind B only while a window is open and sink it; select at entrance start |
| Key hints wrong on phone, touch buttons shown on PC | `TouchEnabled` or last-input checks | `PreferredInput` and its changed signal |
| Buttons feel dead; clicks seem ignored | No pressed state or sound; waiting for the server before any feedback | Local press feedback under 100 ms, then reconcile with the server result |
| Purchase prompts or offers annoy players (reviews, chat) | Modal during play, shown in the first minutes, stacked or with sound stings | Offer-surface rules above; `monetization-and-policy.md` |
| UI flashes or is missing for the first seconds | UI waits on full replication; loading screen removed early | Minimal `ReplicatedFirst` loading ScreenGui; enable the HUD when data is ready |

## UI audit scan (edit mode, unexecuted sketch)

Run through the Studio MCP `execute_luau` (Edit datamodel) or the command bar. It only reads and reports; fix by hand.

```lua
--!strict
local StarterGui = game:GetService("StarterGui")
local findings: { string } = {}
local function flag(inst: Instance, msg: string)
	table.insert(findings, `{inst:GetFullName()}: {msg}`)
end

for _, d in StarterGui:GetDescendants() do
	if d:IsA("ScreenGui") then
		if d.ResetOnSpawn then flag(d, "ResetOnSpawn = true") end
		if d.Parent ~= StarterGui then flag(d, "not a direct child of StarterGui: resets on every respawn") end
		if d.SafeAreaCompatibility ~= Enum.SafeAreaCompatibility.None then flag(d, "SafeAreaCompatibility is not None") end
		if d.ScreenInsets == Enum.ScreenInsets.None and d:FindFirstChildWhichIsA("GuiButton", true) then
			flag(d, "interactive UI with ScreenInsets = None")
		end
		if d.ZIndexBehavior ~= Enum.ZIndexBehavior.Sibling then flag(d, "ZIndexBehavior is not Sibling") end
	elseif d:IsA("TextLabel") or d:IsA("TextButton") or d:IsA("TextBox") then
		if d.TextScaled and not d:FindFirstChildOfClass("UITextSizeConstraint") then
			flag(d, "TextScaled without UITextSizeConstraint")
		elseif not d.TextScaled and d.TextSize < 14 then
			flag(d, `TextSize {d.TextSize} below 14`)
		end
		local stroke = d:FindFirstChildOfClass("UIStroke")
		if stroke and stroke.ApplyStrokeMode == Enum.ApplyStrokeMode.Contextual and not d.TextScaled
			and stroke.StrokeSizingMode == Enum.StrokeSizingMode.FixedSize and stroke.Thickness > d.TextSize * 0.12 then
			flag(d, "text stroke above 12% of text size: glyph holes may close")
		end
	end
	if d:IsA("GuiObject") then
		local size = d.Size
		if size.X.Scale == 0 and size.Y.Scale == 0 and (size.X.Offset > 300 or size.Y.Offset > 300) then
			flag(d, "large element sized in pure Offset")
		end
		local isImage = d:IsA("ImageLabel") or d:IsA("ImageButton")
		if isImage and size.X.Scale > 0 and size.Y.Scale > 0 and not d:FindFirstChildOfClass("UIAspectRatioConstraint") then
			flag(d, "scaled image without UIAspectRatioConstraint")
		end
	end
	if d:IsA("CanvasGroup") and d:FindFirstAncestorOfClass("CanvasGroup") then flag(d, "nested CanvasGroup") end
	if d:IsA("GuiButton") and d.Selectable and d.BackgroundTransparency >= 1 and not d:FindFirstChildWhichIsA("GuiObject") then
		flag(d, "invisible button is gamepad-selectable (tap pad or catcher?)")
	end
end
print(`UI audit: {#findings} findings`)
for _, line in findings do print(line) end
```

Extend it with the game's own rules: buttons under 44 px at the phone frame, colours not in the theme, more than 300 `UIStroke`s under one ScreenGui. A fuller audit renders each screen off-screen at desktop and phone sizes and scores it on flags that are pure `AbsolutePosition`/`AbsoluteSize` maths `[lihfolk]`: `pocket` (a fill touching the corners of a rounded ancestor), `stroke2` (stacked outlines), `radius` (nested rounding that does not run parallel), `bleed` (content outside its panel), `uneven` (rows of different height in one list) and `centre` (captions more than a pixel off-centre). Start with `centre`, `uneven` and `pocket`; re-run after every UI change and keep the score at its maximum.

## Review gate

- [ ] Tested in the Device Emulator and on real devices: small phone portrait and landscape, tablet, desktop, 1080p TV with a gamepad.
- [ ] Interactive UI uses `CoreUISafeInsets`; nothing in the mobile reserved zones; custom buttons near the jump button; no hard-coded top-bar height.
- [ ] Every action has keyboard, gamepad and touch bindings; gamepad reaches every element; initial selection set; B closes every window; console chat disabled.
- [ ] Hints follow `PreferredInput`; `PreferredTextSize` (tested at `Largest`), `PreferredTransparency` and `ReducedMotionEnabled` honoured; no body text relies on `TextScaled`.
- [ ] All user-generated text filtered on the server; prompt actions validated on the server.
- [ ] Offer popups small, dismissible, well-timed, rate-limited and honest; shop one tap away.
- [ ] HUD ≤ 7 elements; counters count up; contrast and text sizes meet the thresholds above.
- [ ] One presenter, a written `DisplayOrder` band plan, modal blockers that sink input; every ScreenGui a direct child of `StarterGui` with `ScreenInsets` set explicitly.
- [ ] Measured at the listed viewports: drawn text ≥ 12 px, taps ≥ 44 px, gaps ≥ 8 px, zero overlaps; ten rapid open/close taps end in the last requested state.
- [ ] UI idle costs no per-frame Lua; loops stop when their screen closes; MicroProfiler checked on a low-end phone with the busiest window open.
- [ ] Lists over a few hundred items are virtualised or paginated; no beta-only UI property is required in the live client.
- [ ] UI audit scan returns no unexplained findings; the symptom table was checked against analytics and player feedback for a live game.

## Sources

Accessed 2026-11-10.

- `references/knowledge-base.md` sections `## 2.3`, `## 2.5`, `## 5.10`, `## 5.11` (read; grep those headings for the long form)
- `Roblox/creator-docs` (read): `ui/position-and-size.md`, `includes/ui/screen-insets.md`, `ui/size-modifiers.md`, `ui/list-flex-layouts.md`, `ui/scrolling-frames.md`, `ui/appearance-modifiers.md`, `ui/rich-text.md`, `ui/ui-drag-detectors.md`, `ui/2D-paths.md`, `ui/styling/index.md`, `ui/styling/editor.md`, `projects/cross-platform.md`, `production/publishing/accessibility.md`, `production/localization/automatic-translations.md`, `performance-optimization/improve.md`, `studio/device-simulator.md`, class reference for `GuiService`, `GuiObject`, `GuiBase2d`, `ScreenGui`, `PlayerGui`, `StarterGui`, `CanvasGroup`, `UICorner`, `UIStroke`, `UIShadow`, `TextLabel`: https://github.com/Roblox/creator-docs
- https://devforum.roblox.com/t/full-release-ui-styling-is-officially-released/4275082, https://devforum.roblox.com/t/full-release-stylequery-more-styling-features/4566519, https://devforum.roblox.com/t/full-release-styling-transitions/4646870 (search summary)
- https://devforum.roblox.com/t/studio-beta-uistroke-improvements-scaling-offsets-and-more/3958036, https://gamineai.com/blog/what-roblox-uishadow-beta-changed-for-studio-ui-2026 (search summary)
- https://devforum.roblox.com/t/how-tall-is-the-roblox-top-bar/3248916, https://devforum.roblox.com/t/guiservicegetguiinset-returns-0-0-0-0-for-the-first-frame-of-the-game-with-new-topbar-ui/2973508 (search summary)
- https://devforum.roblox.com/t/mobile-navigation-thumbstick-covers-important-game-uis/205611, https://devforum.roblox.com/t/feedback-on-simulator/2417686, https://devforum.roblox.com/t/thoughts-on-my-simulator-ui/1168190, https://devforum.roblox.com/t/feedback-on-simulator-game/2630240, https://devforum.roblox.com/t/jump-button-and-thumbstick-sized-positioned-wrong-in-mobile-emulator/2861222 (search summary)
- https://devforum.roblox.com/t/virtual-scrolling-list-virtualization/2732175, https://devforum.roblox.com/t/parenting-objects-to-uigridlayouts-causing-extreme-lag-all-of-a-sudden/3607305, https://devforum.roblox.com/t/virtualscroller-infinite-scrollingframes/3990429 (search summary)
- https://devforum.roblox.com/t/introducing-text-scaling-setting-studio-beta/3136967, https://devforum.roblox.com/t/new-preferred-text-size-setting-makes-it-impossible-to-have-text-objects-using-richtext-without-textscaled-enabled-that-arent-affected-by-the-setting/3914959 (search summary)
- https://devforum.roblox.com/t/new-gamepad-ui-selection-apis/1791278, https://devforum.roblox.com/t/introducing-improvements-to-directional-ui-selection-on-gamepad/3864317, https://devforum.roblox.com/t/make-nextselection-properties-dictate-selectiongroup-navigation/3314485 (search summary)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `05 UI and UX/ScreenGui Fundamentals.md`, `Layout - Scale Offset and Constraints.md`, `Responsive UI for Phone Tablet Console and PC.md`, `Safe Areas and Insets.md`, `HUD Design.md`, `UI Motion Language and Timing.md`, `Virtualized Lists and Large Inventories.md`, `Declarative UI - React-Lua and Fusion.md`, `Gamepad and Console UX.md`, `Text Fonts and Rich Text.md`, `Localization.md`, `Accessibility.md`, `UI Design Systems.md`, `World-Space UI - BillboardGui and SurfaceGui.md`, `Nametags and Overhead Bars - Cost and Visibility Rules.md`; `56 Field Notes/` (Shift-Lock Sprint and Gamepad B for Menus, Streaming Joins and Loading Screen Teardown, UIStroke on Text); `skills/roblox-ui-builder/SKILL.md` (read)
- `Roblox/creator-docs` (read, wave 2): `performance-optimization/microprofiler/tag-table.md`, class reference for `LayerCollector`, `TweenService`, `TweenBase`, `UIScale`, `UITextSizeConstraint`, enums `Font`, `InputSink`
- GitHub search API metadata (read) for https://github.com/centau/vide, https://github.com/Roblox/react-luau, https://github.com/jsdotlua/react-lua, https://github.com/dphfox/Fusion, https://github.com/Roblox/roact, https://github.com/flipbook-labs/flipbook, https://github.com/PepeElToro41/ui-labs, https://github.com/Kampfkarren/hoarcekat, https://github.com/fraktality/spr, https://github.com/littensy/ripple, https://github.com/Reselim/Flipper
- https://github.com/xtrair/figma-to-roblox-ui (read: the Scale-only rules cited in the conflict note), https://github.com/grim-technologies-arch/ui-figma-roblox (read: rotated-children clipping note)
- Not reachable directly: reddit.com, devforum.roblox.com, create.roblox.com (blocked); DevForum items above are search-result summaries only.
