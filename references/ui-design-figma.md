# UI design in Figma, implementation in Roblox

How to design a Roblox HUD, shop, inventory and reward flow in Figma (through the Figma MCP), bring it into Studio as native instances plus a small set of images, and make it look authored instead of generic. Open it when designing UI for a new game, re-skinning a live one, or when a UI audit says "looks default". Engine rules (insets, input, gamepad, accessibility) live in `ui-input-crossplatform.md`; this file is the design and hand-off layer. Tags: `[official]` Roblox docs, `[community]` forum/GitHub practice, `[VS]` version-sensitive, `[house]` house estimates.

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
| Type scale (phone frame px) | Display 28–32, Title 22–24, HUD number 18–20, Body 16, Caption 14 (floor) `[house]` | One display family + one body family. Roblox-native: `FredokaOne`, `LuckiestGuy`, `Bangers` (display); `BuilderSans*`, `Gotham*`, `Nunito` (body) `[official]` |
| Spacing | 4 / 8 / 12 / 16 / 24 | 8 px grid; gaps ≥ 8 px between touch targets |
| Radius | S 6, M 10, L 16, Pill | One radius family per game |
| Stroke | Thin 2, Regular 3, Text 2–3; one near-black outline colour | Outline text that sits on the 3D world or on texture `[official]` |
| Depth | Darker duplicate under the face, offset 4–6 px (button lip), 8–10 px (cards) `[community]` | Press state sinks the face into the lip |
| Motion | Press 0.08–0.1 s, hover/focus 0.12 s, panel open 0.2–0.25 s, count-up 0.35–0.8 s | All go to 0 or fade when `GuiService.ReducedMotionEnabled` `[official]` |

- Fonts `[VS]`: only `Enum.Font` families and Creator Store font families (`FontFace`) render as text. No evidence was found in the docs for arbitrary font upload. Pick the Roblox family first, then find its Figma equivalent, not the reverse.
- Contrast: 4.5:1 body, 3:1 large text and icons (see `ui-input-crossplatform.md`). Test over a gameplay screenshot, not over a grey canvas.
- Young audience: icons before words, loud titles, big numerals with suffixes (`12.5K`, `3.4M`), one obvious next action per screen. `[community]` No rigorous evidence for exact sizes for ages 8–12 was found; playtest with real kids.

## Frames and scale

| Figma frame | Size | Purpose |
|---|---|---|
| `Phone-S` (design here first) | 800×360 `[house]` | Smallest landscape phone; the layout must work here before anything else |
| `Phone-Notch` | 844×390 | Tall-aspect check; community import skills use it as the phone reference `[community]` |
| `Tablet` | 1024×768 | 4:3; thumb reach differs: a button 40% from the top is reachable on a phone, not on a tablet `[official]` |
| `Desktop/TV` | 1920×1080 | Same components; panels get `UISizeConstraint` max so 75% width does not become huge on a TV `[official]` |

- `[house][VS]` Do not assume a phone's viewport equals its physical pixel resolution. Print `workspace.CurrentCamera.ViewportSize` on the real target phone and add that frame.
- Every frame carries three locked overlay layers: thumbstick zone (bottom-left), jump zone (bottom-right), top bar strip. The top bar is reported as 58 px tall on large screens, 48 on phones, absent on console `[community][VS]`: never hard-code it; use `ScreenInsets`/`GuiService.TopbarInset`.
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
| Toast | height 36–44 | 0.11 H | Top-centre under the objective; ≤ 2 visible, 2–3 s, queue the rest; coloured by rarity; never a modal |
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
| `RaRdq/FigmaRobloxForge` | 1 · 2026-11 · MIT | Rasterises every non-text layer to PNG → `.rbxmx`; pixel-accurate but many uploads and more texture memory |
| `astrorehan/figlo` | 1 · 2026-10 · MIT | Figma plugin + local relay + Studio plugin; alpha |
| `cameronpcampbell/supercorner` | 16 · 2026-07 · MIT | Figma-style squircle corners as generated 9-slice images |
| `lopi-py/figblox`, `EgoMoose/figma-to-roblox-ui` | 15 · 2023-12 · MIT; 9 · 2024-09 · archived | Stale: do not start here |

DevForum also lists FigBloxUI, RoImport, UILint, Bloxporter (paid), MonkeyPTR and GuiForge; one 2025 thread reports converter output with elements "separating weirdly" `[community]`. Low star counts everywhere: treat converters as accelerators and audit their output.

## Theme module (unexecuted sketch)

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Theme.luau. Generated from Figma variables; edit in Figma, then regenerate.
local GuiService = game:GetService("GuiService")
local TweenService = game:GetService("TweenService")

local Theme = {
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
	Stroke = table.freeze({ Thin = 2, Regular = 3 }),
	Motion = table.freeze({ Press = 0.09, Hover = 0.12, Panel = 0.22, CountUp = 0.35 }),
}

-- Every UI tween goes through here so Reduce Motion is honoured in one place.
function Theme.tween(target: Instance, seconds: number, goal: { [string]: any }): Tween
	local t = if GuiService.ReducedMotionEnabled then 0 else seconds
	local tween = TweenService:Create(target, TweenInfo.new(t, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), goal)
	tween:Play()
	return tween
end

-- Press feedback on a child UIScale: sink on press, spring back on release. Button anchor must be (0.5, 0.5).
function Theme.bindPress(button: GuiButton, scale: UIScale)
	button.AutoButtonColor = false
	button.MouseButton1Down:Connect(function() Theme.tween(scale, Theme.Motion.Press, { Scale = 0.94 }) end)
	local function release() Theme.tween(scale, Theme.Motion.Hover, { Scale = 1 }) end
	button.MouseButton1Up:Connect(release)
	button.MouseLeave:Connect(release)
end

return table.freeze(Theme)
```

Rarity colours are starting points from a community teardown (approximate) `[community]`; replace all values with your own palette.

## Frameworks and tooling

| Option | GitHub (2026-11-10) | Use when |
|---|---|---|
| Plain instances + Theme + small controllers | n/a | **Default.** Figma-built screens stay visible in Explorer, editable by the Studio MCP and the Style Editor; state is a handful of attributes and signals |
| `StyleSheet` tokens, `StyleQuery`, transitions | engine; styling fully released, StyleQuery May 2026, transitions July 2026 `[community][VS]` | Re-skinning Studio-authored screens; responsive swaps by `@ViewportDisplaySizeSmall` / `@PreferredInputTouch` `[official]` |
| Vide (`centau/vide`) | 355★, pushed 2026-10, MIT | Many dynamic lists and derived state; small reactive core |
| React (`Roblox/react-luau`, read-only mirror; `jsdotlua/react-lua`) | 589★ pushed 2026-10; 582★ pushed 2025-05 | The team already thinks in React; large UI codebase |
| Fusion (`dphfox/Fusion`) | 813★, pushed 2026-02, MIT | Existing Fusion codebases |
| Roact (`Roblox/roact`) | archived 2023-12 | Never for new work |
| Storybook: `flipbook-labs/flipbook` (MIT, 2026-11), `PepeElToro41/ui-labs` (GPL-3.0, 2026-10), `Kampfkarren/hoarcekat` (2025-11) | 124★ / 202★ / 148★ | Any code-built component library: preview states without playtesting |
| Motion: `TweenService`; `fraktality/spr` (2024-07), `littensy/ripple` (2026-07); `Reselim/Flipper` (2021-11, stale) | 146★ / 137★ / 144★ | Tweens for state changes; springs when animations must retarget mid-flight |

**Conflict:** `ui-input-crossplatform.md` named Fusion 0.4 as the "bold" option. By repository activity on 2026-11-10 Vide and react-luau are the actively maintained choices and Fusion is quieter. The default does not change: plain instances. Pick a framework only when more than about five screens share live state or lists exceed a few hundred rows. Recheck activity before adopting any library `[VS]`.

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
- [ ] Polish checklist passed; `ui-input-crossplatform.md` review gate passed.

## Sources

Accessed 2026-11-10.

- `Roblox/creator-docs` (read): `ui/9-slice.md`, `ui/appearance-modifiers.md`, `ui/position-and-size.md`, `ui/labels.md`, `ui/rich-text.md`, `ui/styling/index.md`, `ui/styling/editor.md`, `projects/cross-platform.md`, `production/publishing/accessibility.md`, `performance-optimization/improve.md`, `art/modeling/texture-specifications.md`, `cloud/guides/usage-assets.md`, `studio/mcp.md`, `studio/mcp-open-cloud.md`, `studio/device-simulator.md`, `tutorials/curriculums/user-interface-design/*.md`, `tutorials/use-case-tutorials/ui/create-hud-meters.md`, class and enum reference for `UIStroke`, `UICorner`, `UIShadow`, `UIGradient`, `CanvasGroup`, `ImageLabel`, `GuiService`, `Font`, `GradientType`, `StrokeSizingMode`: https://github.com/Roblox/creator-docs
- https://github.com/xtrair/figma-to-roblox-ui (read: README, SKILL.md)
- https://github.com/grim-technologies-arch/ui-figma-roblox (read: README, SKILL.md, examples/stud-shop/README.md, ATTRIBUTION.md)
- https://github.com/MarkRuiz00/RbxUiStudio (read: README, juegos/README.md, juegos/pet-simulator-99.md, estilos/simulator.md, roblox-ui/images.md, checklist.md)
- https://github.com/NoTwistedHere/Figma-to-Roblox, https://github.com/RaRdq/FigmaRobloxForge, https://github.com/astrorehan/figlo, https://github.com/MiaGobble/Figma-Import-Assistant, https://github.com/cameronpcampbell/supercorner (read: READMEs)
- GitHub search API metadata (read) for the repositories in both tables, including https://github.com/centau/vide, https://github.com/Roblox/react-luau, https://github.com/jsdotlua/react-lua, https://github.com/dphfox/Fusion, https://github.com/Roblox/roact, https://github.com/flipbook-labs/flipbook, https://github.com/PepeElToro41/ui-labs, https://github.com/Kampfkarren/hoarcekat, https://github.com/fraktality/spr, https://github.com/littensy/ripple, https://github.com/Reselim/Flipper
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
