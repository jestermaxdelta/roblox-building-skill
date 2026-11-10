# UI, input, cross-platform and accessibility

Engine-side rules for Roblox UI and input: HUD and menu principles, containers and safe areas, sizing, text, mobile/console/VR layout, input mapping and accessibility, plus a symptom table and an audit scan for live games. Open it when building or auditing any screen or control scheme; open `ui-design-figma.md` for visual design, tokens, patterns with sizes and the Figma hand-off. Distilled from knowledge-base sections 2.3, 2.5, 5.10 and 5.11, re-verified against `Roblox/creator-docs` on 2026-11-10. Tags: `[official]` Roblox docs, `[community]` forum practice, `[VS]` version-sensitive (several UI and input systems are new), `[house]` house estimates.

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

- A `ScreenGui` in `StarterGui` clones into `PlayerGui` on first spawn. Set `ResetOnSpawn = false` for HUDs, shops and menus. One ScreenGui per screen; toggle `ScreenGui.Enabled` (a disabled ScreenGui neither renders nor takes input); layer with `DisplayOrder`.
- `ScreenGui.ScreenInsets`: `CoreUISafeInsets` (default; use for anything interactive), `DeviceSafeInsets` (clears notches, not the top bar), `TopbarSafeInsets` (the strip between the top-bar controls and the right safe edge; flexes with the bar), `None` (full-bleed backgrounds only). Loading screens use `IgnoreGuiInset = true`. Query insets with `GuiService:GetGuiInset()`.
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
- Modifier limits `[official]`: `UICorner` cannot be applied to a `ScrollingFrame`, and it clips input but not descendants (use a `CanvasGroup`, or 9-slice art, for rounded clipping). `ClipsDescendants` does not clip rotated children `[community]`. Do not tween `UIStroke.Thickness` on text (re-renders glyphs every frame). Flex adds a slight layout cost over plain lists; use `UIGridLayout` when cells must align on both axes.
- `CanvasGroup` `[official]`: flattens only when the ScreenGui uses `ZIndexBehavior.Sibling`; consumes extra texture memory capped by the client's quality level and renders **blank** past the cap; keep its size static.
- `UIStroke` `[VS]`: fixed-pixel strokes look thicker on small screens; `StrokeSizingMode = ScaledSize` (Improved UIStrokes beta) scales with the parent's short side. The beta announcement is reported to recommend fewer than 300 UIStrokes on screen for low-end devices; a figure of about 100 UIShadows circulates second-hand `[community]`. Budget both.
- New instances `[official][VS]`: `UIDragDetector` (sliders, spinners and draggable panels on every input without code), `Path2D` (2D splines for path animation and curved connectors), radial/elliptical/conical `UIGradient` types (beta), per-corner `UICorner` radii (beta), styling transitions and the Style Editor. Check the beta list before shipping any of them.
- Layouts: `UIListLayout` (with flex and `UIFlexItem`), `UIGridLayout` (compute `CellSize` from `AbsoluteSize`), `UITableLayout` (tabular data only), `UIPageLayout` (carousels), `UIPadding`. Use explicit breakpoints (for example switch a category list from vertical to horizontal under about 700 px width) rather than shrinking desktop panels.
- Styling: `UICorner`, `UIStroke`, `UIGradient`, 9-slice, `UIShadow` (new, partly beta). Sprite sheets via `ImageRectOffset`/`ImageRectSize`. The UI styling system (`StyleSheet`, `StyleRule`, `StyleLink`, `StyleDerive`, `StyleQuery`, tokens like `$Accent`) gives one place to re-skin; define a small token sheet and drive buttons with tag selectors. Status `[VS]`: the styling APIs and Style Editor are fully released for live experiences, `StyleQuery` (media and container queries in one) followed in May 2026 and styling transitions in July 2026 (DevForum announcements, seen through search).
- Motion: `TweenService` on the client for state changes only; 0.1–0.3 s for feedback, ≤ 0.75 s for panel transitions; honour `GuiService.ReducedMotionEnabled` (tween time 0 or fade instead of slide).
- Framework: lower-risk is Studio-authored Instances with styling tokens and small controller modules, binding only dynamic regions; bold is Fusion 0.4 with scopes and springs (freeze tables for its skip-update optimisation; `scope:doCleanup()` on close) `[VS]`; React-Luau only if the team comes from React. **Conflict:** by GitHub activity on 2026-11-10, Vide and react-luau are the actively maintained code-first options and Fusion is quieter; the default (plain instances) is unchanged. Comparison table in `ui-design-figma.md` §Frameworks and tooling.
- Performance: hidden screens `Enabled = false`; avoid UIGradient and UICorner on constantly changing text (`fillGuiVertices`); `CanvasGroup` for complex static panels (costs memory; do not nest); icons ≤ 256² in sprite sheets; load menu art lazily; interactive `SurfaceGui`s stay in `StarterGui` with `Adornee` set to the Blender board mesh.
- Long lists `[community]`: a `ScrollingFrame` with about 1,000 or more cells scrolls badly, and mass-parenting buttons into a `UIGridLayout` is reported to freeze. Above a few hundred items, virtualise (create only visible rows and recycle them on `CanvasPosition` change), pool cells instead of destroy-and-recreate on open, or paginate. Build a list on first open, not at join `[official]`.
- Image memory follows pixel count, not file size (a 1024² image costs 4× a 512²) `[official]`; export rules are in `ui-design-figma.md`.

## Text, numbers and localisation

- Body text: fixed `TextSize` + `TextWrapped` + `AutomaticSize`. With `GuiService.PreferredTextSize` the engine enlarges such text and auto-sized bounds grow; `TextScaled` text is **not** scaled by the setting, and a `UITextSizeConstraint` clamps it `[official]`.
- `TextScaled` only for short numerals and titles in fixed boxes, always with `UITextSizeConstraint` (min and max). Without a cap, labels of equal size render different text sizes by string length (DevForum reports, thread not individually identified) `[community]`.
- Type floor `[house]`: HUD numbers ≥ 18 px, body 16, captions 14 at phone 1×. Outline (`UIStroke`, Contextual) or plate any text over the 3D world `[official]`. Use stylised fonts sparingly: titles and alerts only `[official]`.
- Big numbers: abbreviate (`12.5K`, `3.4M`), fix the decimals, size every label for the largest value; `TextTruncate` as the last resort and `TextFits` to detect overflow in tests.
- `RichText` for inline colour, weight and stroke. Localisation strips rich-text tags, so re-apply them in translated strings `[official]`. One 2025 thread reports the text-size setting breaking non-`TextScaled` RichText labels `[community][VS]`: test it.
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
- Test matrix `[VS]`: Device Emulator, or the Device Simulator beta with Flagship, Mid-range and Entry-level phone presets, then the real 3 GB Android phone. The emulator does not show real thumbs.

## Gamepad and console

- Players sit 8–10 feet from a TV: develop for lower resolutions first, keep UI inside TV-safe areas, use relative positions plus `UISizeConstraint`, check `GuiService.ViewportDisplaySize`, and use ScrollingFrames to reduce clutter.
- Every element reachable with four directions plus select and back. Set `GuiService.SelectedObject` when a menu opens, define `NextSelection*` neighbours, trap focus in modals, keep action sequences short.
- Selection tools `[official]`: `SelectionGroup = true` on a container with `SelectionBehaviorUp/Down/Left/Right` (`Escape` default, `Stop` to trap focus in a modal); `SelectionOrder` for the default pick; `Selectable = false` on decorative buttons; `SelectionImageObject` for a themed focus ring; `GuiService.GuiNavigationEnabled` and `AutoSelectGuiEnabled` for manual control. Groups restrict selection; they do not make unreachable buttons reachable `[community]`.
- Test the default directional selection with a real gamepad or the Controller Emulator before writing custom navigation `[official]`. Known rough edges: explicit `NextSelection*` paths across selection groups, and tweened panels confusing selection `[community][VS]`. Close every window on B and return focus to the button that opened it.
- Disable the chat window on console. Icons via `UserInputService:GetImageForKeyCode()` and `GetStringForKeyCode()`. Haptics with `HapticEffect` (`GameplayCollision`, `UIClick`), sparingly. Add navigation and selection sounds.

## VR

Target 72 FPS on Quest 2; keep Roblox's comfort settings (vignette, stepped rotation, third-person fixed camera); enable streaming; limit raycasts, semi-transparent objects and complex SurfaceGuis; use `InputAction` rather than key-specific code; test on a real headset. Video thumbnails do not show on VR or console.

## Accessibility and preferences

- Why `[official]`: over 26% of people have some disability and over 5% some colour blindness.
- `GuiService.PreferredTransparency` (1 default to 0 opaque): multiply background transparency by it and listen for changes. Official pattern: tag translucent backgrounds (for example `TransparentBack`), store each default and reapply on change.
- `GuiService.PreferredTextSize` (`Medium` default, `Large`, `Larger`, `Largest`): applied by the engine except to `TextScaled` text, so prefer fixed `TextSize` with `AutomaticSize` and `TextWrapped` for body text. Test every screen at `Largest`.
- `GuiService.ReducedMotionEnabled`: reduce UI motion, camera shake and flashes. Either tween time 0, or swap slides for a fade (`CanvasGroup.GroupTransparency`) `[official]`. Route every UI tween through one helper (`Theme.tween` in `ui-design-figma.md`).
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
| HUD state lost or duplicated after respawn | `ResetOnSpawn = true`; references to a destroyed clone | `ResetOnSpawn = false`; controllers bind once to `PlayerGui` |
| Frame drops when a menu opens or a list scrolls | Thousands of cells built at once; `UIGridLayout` mass-parenting; destroy and recreate each open | Virtualise or paginate, pool cells, build on first open |
| Constant UI cost in the MicroProfiler with nothing open | Text set every frame; perpetual tweens; hidden screens still `Enabled`; many BillboardGuis | Update on change (≤ 10 Hz), stop idle tweens, `Enabled = false`, `MaxDistance` and pooling |
| Panels turn blank on low-end phones | `CanvasGroup` texture memory cap exceeded | Fewer, static-size CanvasGroups; native shapes or 9-slice instead |
| UI images blurry, or client memory high | Upscaled small exports; many large uploads; one upload per colour | Export 2× up to 1024 px; sprite sheets; tint a white base with `ImageColor3` |
| Outlines thick on phone, thin on TV | Fixed-pixel `UIStroke` on scale-sized elements | Per-breakpoint thickness or `ScaledSize` strokes once out of beta `[VS]`; verify under `UIScale` |
| Gamepad or console players stuck in a menu | No initial `SelectedObject`; no B to close; focus escapes the modal | Set selection on open, `SelectionGroup` with `Stop`, back action on every screen |
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
end
print(`UI audit: {#findings} findings`)
for _, line in findings do print(line) end
```

Extend it with the game's own rules: buttons under 44 px at the phone frame, colours not in the theme, more than 300 `UIStroke`s under one ScreenGui.

## Review gate

- [ ] Tested in the Device Emulator and on real devices: small phone portrait and landscape, tablet, desktop, 1080p TV with a gamepad.
- [ ] Interactive UI uses `CoreUISafeInsets`; nothing in the mobile reserved zones; custom buttons near the jump button; no hard-coded top-bar height.
- [ ] Every action has keyboard, gamepad and touch bindings; gamepad reaches every element; initial selection set; B closes every window; console chat disabled.
- [ ] Hints follow `PreferredInput`; `PreferredTextSize` (tested at `Largest`), `PreferredTransparency` and `ReducedMotionEnabled` honoured; no body text relies on `TextScaled`.
- [ ] All user-generated text filtered on the server; prompt actions validated on the server.
- [ ] Offer popups small, dismissible, well-timed, rate-limited and honest; shop one tap away.
- [ ] HUD ≤ 7 elements; counters count up; contrast and text sizes meet the thresholds above.
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
- https://github.com/xtrair/figma-to-roblox-ui (read: the Scale-only rules cited in the conflict note), https://github.com/grim-technologies-arch/ui-figma-roblox (read: rotated-children clipping note)
- Not reachable directly: reddit.com, devforum.roblox.com, create.roblox.com (blocked); DevForum items above are search-result summaries only.
