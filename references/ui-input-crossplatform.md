# UI, input, cross-platform and accessibility

Distilled from knowledge-base sections 2.3, 2.5, 5.10 and 5.11. Use it for HUD design, menus, offer surfaces, input mapping, mobile/console/VR layout and accessibility. `[VS]` marks version-sensitive facts (several UI and input systems are new).

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
- `ScreenGui.ScreenInsets`: `CoreUISafeInsets` (default; use for anything interactive), `DeviceSafeInsets`, `TopbarSafeInsets`, `None` (full-bleed backgrounds only). Loading screens use `IgnoreGuiInset = true`. Query insets with `GuiService:GetGuiInset()`.
- Sizing rules: scale position plus matching `AnchorPoint` for edge-relative elements (`AnchorPoint (1,0)`, `Position UDim2.new(1,-16,0,16)` for a 16 px top-right margin); scale size plus `UIAspectRatioConstraint` for shape; `UISizeConstraint` for min and max; fixed `TextSize` with `UITextSizeConstraint` rather than `TextScaled` for body text; `AutomaticSize` for content-driven panels (Size becomes the minimum); `ScrollingFrame` with `AutomaticCanvasSize` and `CanvasSize = 0`; `UIScale` on a root frame only as a final global multiplier.
- Gotcha: a `UIAspectRatioConstraint` overrides a layout's sizing.
- Layouts: `UIListLayout` (with flex and `UIFlexItem`), `UIGridLayout` (compute `CellSize` from `AbsoluteSize`), `UITableLayout` (tabular data only), `UIPageLayout` (carousels), `UIPadding`. Use explicit breakpoints (for example switch a category list from vertical to horizontal under about 700 px width) rather than shrinking desktop panels.
- Styling: `UICorner`, `UIStroke`, `UIGradient`, 9-slice, `UIShadow` (new, partly beta). Sprite sheets via `ImageRectOffset`/`ImageRectSize`. The UI styling system (`StyleSheet`, `StyleRule`, `StyleLink`, `StyleDerive`, `StyleQuery`, tokens like `$Accent`) gives one place to re-skin; define a small token sheet and drive buttons with tag selectors.
- Motion: `TweenService` on the client for state changes only; 0.1–0.3 s for feedback, ≤ 0.75 s for panel transitions; honour `GuiService.ReducedMotionEnabled` (tween time 0 or fade instead of slide).
- Framework: lower-risk is Studio-authored Instances with styling tokens and small controller modules, binding only dynamic regions; bold is Fusion 0.4 with scopes and springs (freeze tables for its skip-update optimisation; `scope:doCleanup()` on close) `[VS]`; React-Luau only if the team comes from React.
- Performance: hidden screens `Enabled = false`; avoid UIGradient and UICorner on constantly changing text (`fillGuiVertices`); `CanvasGroup` for complex static panels (costs memory; do not nest); icons ≤ 256² in sprite sheets; load menu art lazily; interactive `SurfaceGui`s stay in `StarterGui` with `Adornee` set to the Blender board mesh.

## Text filtering (mandatory)

Any text one player writes that others can see is filtered on the server:

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

Jump buffer plus coyote time sketch (client; the Humanoid jump arc itself is fixed):

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

## Gamepad and console

- Players sit 8–10 feet from a TV: develop for lower resolutions first, keep UI inside TV-safe areas, use relative positions plus `UISizeConstraint`, check `GuiService.ViewportDisplaySize`, and use ScrollingFrames to reduce clutter.
- Every element reachable with four directions plus select and back. Set `GuiService.SelectedObject` when a menu opens, define `NextSelection*` neighbours, trap focus in modals, keep action sequences short.
- Disable the chat window on console. Icons via `UserInputService:GetImageForKeyCode()` and `GetStringForKeyCode()`. Haptics with `HapticEffect` (`GameplayCollision`, `UIClick`), sparingly. Add navigation and selection sounds.

## VR

Target 72 FPS on Quest 2; keep Roblox's comfort settings (vignette, stepped rotation, third-person fixed camera); enable streaming; limit raycasts, semi-transparent objects and complex SurfaceGuis; use `InputAction` rather than key-specific code; test on a real headset. Video thumbnails do not show on VR or console.

## Accessibility and preferences

- `GuiService.PreferredTransparency` (1 default to 0 opaque): multiply background transparency by it and listen for changes.
- `GuiService.PreferredTextSize`: applied by the engine except to `TextScaled` text, so prefer fixed `TextSize` with `AutomaticSize` and `TextWrapped` for body text.
- `GuiService.ReducedMotionEnabled`: reduce UI motion, camera shake and flashes.
- Colour non-reliance (icon or label with every colour state), sound non-reliance (visual cues for audio events), separate Music, SFX and Ambience sliders.
- Adaptive design: input fluidity (every action on every input, hints match the active input), responsive layout (collapse secondary buttons on small screens), dynamic sizing, legibility on the smallest phone and a distant TV.

## UI and input review gate

- [ ] Tested in the Device Emulator and on real devices: small phone portrait and landscape, tablet, desktop, 1080p TV with a gamepad.
- [ ] Interactive UI uses `CoreUISafeInsets`; nothing in the mobile reserved zones; custom buttons near the jump button.
- [ ] Every action has keyboard, gamepad and touch bindings; gamepad reaches every element; initial selection set; console chat disabled.
- [ ] Hints follow `PreferredInput`; `PreferredTextSize`, `PreferredTransparency` and `ReducedMotionEnabled` honoured; no body text relies on `TextScaled`.
- [ ] All user-generated text filtered on the server; prompt actions validated on the server.
- [ ] Offer popups small, dismissible, well-timed, rate-limited and honest; shop one tap away.
- [ ] HUD ≤ 7 elements; counters count up; contrast and text sizes meet the thresholds above.

Grep `references/knowledge-base.md` for `## 2.3`, `## 2.5`, `## 5.10` and `## 5.11`.
