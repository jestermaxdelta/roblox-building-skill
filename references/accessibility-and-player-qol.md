# Accessibility and player quality of life

What makes a Roblox game comfortable to play for people with different eyes, ears, hands, devices and patience: accessibility systems (colour, text, motion, flashes, captions, remapping, assists, cognitive load, localisation) and the quality-of-life (QoL) features players praise, each with implementation notes. Open it when designing the settings menu and comfort systems of a new game, or when a live game gets "unplayable on phone", "makes me dizzy", "sold my best pet by accident" or "nothing happens when I click" feedback. Engine-side UI and input rules (insets, sizing, `PreferredTextSize`, the Input Action System, jump buffer code) live in `ui-input-crossplatform.md` and are not repeated here. Tags: `[official]` Roblox docs, `[community]` forum or press practice, `[VS]` version-sensitive, `[house]` house estimate, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; its design numbers are rules of thumb, not measurements).

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Music and SFX sliders with every sound in a `SoundGroup`. (2) Never colour alone: add an icon, word or shape to every colour signal. (3) Body text ≥ 16 px on a phone, fixed `TextSize`, no `TextScaled` for content. (4) Every rejected action says why and what to do next. (5) A lock on valuable items and a confirm on anything irreversible | Remapping UI, touch layout editor, palette modes, server lists |
| Intermediate | One settings schema shared by client and server, saving overrides only; one comfort resolver (shake, screen effects, flashes, hit-stop; §10) that follows `ReducedMotionEnabled`; hold/toggle on every sustained action; graphics preset with a real VFX density scale; captions for sounds that change what a player does; AFK, rejoin and join-friend handled deliberately | Per-assist leaderboards, Oklab palette audit in CI |
| Expert | Numeric palette audit under simulated protan/deutan/tritan vision; flash gate shared by all players' effects; assists as server-authoritative per-player dials with fair leaderboards; automated text-fit audit at `Largest` × max UI scale × longest language; measured assist adoption and quit rate per obstacle | — |

## Contents

1. Principles · 2. Who owns which setting · 3. Colour and contrast · 4. Text size and UI scale · 5. Motion, camera comfort and flashes · 6. Sound: captions, cues, mixing, haptics · 7. Controls: remapping, hold/toggle, one-handed, aim assist · 8. Difficulty, assists and cognitive load · 9. Screen readers, localisation and RTL · 10. Settings architecture · 11. QoL catalogue · 12. QoL audit ranked by cost · 13. Level-up table · 14. Conflicts · Review gate · Sources

## 1. Principles

- **The default game must pass.** Most players never open settings `[lihfolk]`; a toggle is not permission for a bad default.
- **Read platform settings, never replace them.** Roblox owns graphics quality, sensitivity, invert, shift lock, text size, reduce motion, background transparency and the block list. Duplicating one creates two sliders that multiply `[lihfolk]`.
- **Save overrides, not copies.** Store only values the player changed, so a later change to a default or to the platform's Reduce Motion still reaches everyone who never touched it `[lihfolk]`.
- **Presentation is client-side; anything that changes outcomes is server-side.** Captions, palettes and shake are local. Damage reduction, timing windows, auto-collect and item locks are validated and stored by the server.
- **Name options by what they do** ("Wider dodge window"), never by who they are for ("Easy mode", "Kids mode") `[lihfolk]`.
- **Accessibility is also the phone in sunlight and the muted bus ride.** Roblox's own guidance: over 26% of people have a disability and over 5% some colour blindness `[official]`. On a 3 GB Android phone with the sound off, every player is temporarily low-vision and hard of hearing `[house]`.
- Why it pays: these features remove quit reasons in the first session (see `audit-existing-game.md` triage) and cost little once the settings schema exists.

## 2. Who owns which setting `[VS]`

| Setting | Owner | What the game does |
|---|---|---|
| Graphics quality (Automatic or 1–10) | Roblox | Cannot be set by script, and do not read it: staff ask developers to "avoid modulating visual effects by reading `UserGameSettings.SavedQualityLevel`" and plan to deprecate the API (DevForum, 2026-11-05) `[official][VS]`. Add game-only levers driven by the player's own preset and measured frame time (§11 performance mode) |
| Mouse and gamepad sensitivity, invert Y | Roblox (`UserGameSettings.MouseSensitivity`, `GamepadCameraSensitivity`, `GetCameraYInvertValue()`) | Custom cameras multiply by them; never add a second base slider `[lihfolk]` |
| Shift lock, camera mode | Roblox, gated by `StarterPlayer.EnableMouseLockOption` | Allow it or explain why not |
| Text size | Roblox: `GuiService.PreferredTextSize` (`Medium`, `Large`, `Larger`, `Largest`) `[official]` | Layouts that grow; no `TextScaled` content |
| Reduce motion, background transparency | Roblox: `GuiService.ReducedMotionEnabled`, `PreferredTransparency` `[official]` | Follow them, listen for changes, allow a game override |
| Block list, chat mute, report | Roblox | Honour blocks in every custom social system; open `StarterGui:SetCore("PromptBlockPlayer", player)` instead of a custom block button `[official]` |
| Colour-blind filter | Nobody. Roblox staff: games "can and should implement their own colorblind-friendly options"; full-screen colour filters are "not a great solution, and so we don't intend to support them" (DevForum staff reply, 2023-11-29) `[official]` | Redundant cues plus palette modes (§3) |
| FOV, shake, flashes, captions, volume groups, UI scale, keybinds, touch layout, assists | The game | This file |
| Screen reader for in-game UI | Not documented by Roblox as of this pass `[VS]` | §9 |

## 3. Colour and contrast

Rules:

- Every information-carrying colour has a second channel: lightness, shape, icon, text, pattern, position, size or motion. Lightness is the channel every player keeps, including the rare player with no colour vision `[lihfolk]`.
- Colour-blind players mostly fail on signals that are **small** (a 6 px pip, a 1 px outline), **far apart**, **pastel** or **brief** (a 0.2 s flash), not on large saturated patches `[lihfolk]`. Rescue a signal you cannot recolour by making it bigger or longer-lived.
- Risky pairs: red/green, red/brown, green/brown, green/orange, blue/purple, blue/green, yellow/light pink, any two pastels `[lihfolk]`.
- Two teams: blue versus orange, **with a clear lightness gap** and an emblem. A common blue/orange pair measures as the same grey, so the hue alone is not enough `[lihfolk]`. More than two teams: one emblem per team.
- Rarity ladders: rarity name on every card, a pip count or frame shape per tier, lightness rising monotonically with tier.
- Heal versus damage: sign (+/−), direction of motion, weight. Crits are bigger, not just yellower.
- Telegraphs on the 3D floor must read in greyscale: a bright thick edge ring, a hatch or chevron pattern in the decal texture, one shape per attack type, and a fill that grows as the attack charges `[lihfolk]`. The telegraph mesh and its texture are Blender-authored like any other asset (house rule 1).
- Contrast (WCAG 2.x 1.4.3 and 1.4.11): 4.5:1 for text, 3:1 for large text (about 24 px, or 19 px bold) and for icons and control outlines. Compute it, never judge by eye: linearise each sRGB channel (`c ≤ 0.04045 → c ÷ 12.92`, else `((c + 0.055) ÷ 1.055)^2.4`), `L = 0.2126 R + 0.7152 G + 0.0722 B`, ratio = `(L_light + 0.05) ÷ (L_dark + 0.05)`. Mid-tone accents fail with white more often than they look: on the theme's mid-green `Primary` `#35B25D`, white is 2.7:1 (fails both thresholds) while its dark `OnAccent` `#1A1F2B` is 6.0:1; white reaches 5.4:1 only on the dark shade `#1F7A3D`; on the brighter green `#34C759` white is 2.2:1. Check every text-on-accent pair in the theme module (`ui-design-figma.md` tokens) this way.

Measure the palette instead of eyeballing it `[lihfolk]`: convert each token to linear RGB, apply a protan, deutan and tritan simulation matrix (Machado et al. 2009), convert to Oklab, and compare the Euclidean distance of every pair that appears together on a real screen.

| Situation | Minimum Oklab distance under every simulation `[lihfolk]` (rule of thumb) |
|---|---|
| Big patches side by side | 0.08 |
| Signals that are small or apart: outlines, markers, pips | 0.15 |
| Critical reads (safe vs harmful floor, ally vs enemy) | 0.20 plus a channel other than colour |
| Lightness-only check (survives greyscale) | ΔL ≥ 0.15 |

Tests, cheapest first:

1. **Greyscale pass.** Add a `ColorCorrectionEffect` with `Saturation = -1` under `Lighting` in a test session; anything unreadable relies on hue. It affects the 3D view only, so desaturate UI screenshots in an image editor `[lihfolk]`.
2. Simulator pass on screenshots of each strongly graded zone (sunset lighting shifts every token).
3. Numeric audit over the token table in CI.
4. Smallest on-screen size, edge of screen, real phone, outdoors.

Palette modes: UI and VFX reference semantic tokens (`team.enemy`, `state.danger`, `rarity.epic`), a mode swaps the palette, and the binder re-applies on change. Modes change colour only: lightness order, shapes, icons and meaning stay fixed, so nobody relearns the game `[lihfolk]`. Never ship a "filter" built from `ColorCorrectionEffect`: tint and saturation cannot move red-green information to another axis `[lihfolk]`. Do not try to detect colour blindness; default to the standard palette and show a live preview in settings.

## 4. Text size and UI scale

Engine behaviour is in `ui-input-crossplatform.md` §Text. What to add:

- **Measure rendered size**, after every scale, with `TextBounds`, not authored `TextSize`. Hard audit floor: nothing under 12 px rendered on a phone `[lihfolk]`; house targets stay higher (HUD numbers ≥ 18, body 16, captions 14).
- **Three scales multiply** `[lihfolk]`: the player's Roblox text size (text only, ignored by `TextScaled`, clamped by `UITextSizeConstraint`), your device `UIScale`, and your UI-size slider. Test the corner: `Largest` × maximum slider × longest language.
- **UI-size slider:** 0.8–1.3, default 1.0, one `UIScale` per ScreenGui root driven by one controller, **clamped so a reference panel still fits the viewport**, with the effective value shown ("130% (limited to 118% on this screen)"). Without the clamp the slider can push the close button off-screen `[lihfolk]`. Fix the device base scale before adding the slider.
- **Layouts grow:** vertical `UIListLayout` + `AutomaticSize = Y` + `TextWrapped`, inside a `ScrollingFrame` with `AutomaticCanvasSize`. Height is never authored for text.
- **Fixed slots** (toolbar buttons, HUD counters): one or two words, icon carries the meaning, generous `MaxTextSize`. Never truncate prices, counts or names that differ at the end.
- Paragraphs: `LineHeight` 1.15–1.3, 40–60 characters per line on phones, left-aligned, no all-caps sentences, no long italics `[lihfolk]`.
- Stroke on small text: about 8–12% of rendered size and at most 2 px under 16 px text, or it fills the letter counters; use a plate for paragraphs and let the plate follow `PreferredTransparency` `[lihfolk]`.
- World text: clamp billboard text to a minimum rendered height and fade by `MaxDistance`; when the player gets close to a door, show its requirement in screen space rather than leaving it on a `SurfaceGui` alone.
- Automated audit: walk visible `TextLabel`/`TextButton`s and flag `TextFits == false` and small `TextBounds`. Run at `Medium` and `Largest`, minimum and maximum slider, longest language (extend the scan in `ui-input-crossplatform.md`).

## 5. Motion, camera comfort and flashes

Why players feel sick `[lihfolk]`: the eyes report motion the inner ear does not. Worst offenders, in order: camera roll, rotation the player did not cause, narrow FOV on a large close screen, abrupt acceleration, low or uneven frame rate, large areas moving at once. Photosensitivity is a separate safety issue with a published threshold.

| Effect | Comfortable default `[lihfolk]` | Under reduced motion |
|---|---|---|
| Hit and explosion shake | Light hits: none. Heavier hits: a decaying envelope that ends at exactly 0 within about 0.4 s, at most 2° of pitch and yaw and 0.5 studs of offset at full strength, scaled by the player's shake slider. **Roll is always 0 in gameplay**: it is the strongest nausea trigger. Per-hit values are owned by `vfx-and-juice.md` §7 | Off (all rotation and offset); keep at most a 0.25× directional kick, or replace with a reticle hit marker or edge vignette pulse |
| Head bob | None by default; first person only | Off |
| Landing dip | 0.15 s downward offset | 30% or off |
| Knockback | Camera follows the character, no added spin | Same |
| FOV kick (sprint, dash) | Through one FOV owner; total change capped (the vault's reference game used 12°) | Halved, not removed: it carries information |
| Scope zoom | Instant or under 0.15 s; slow zooms are worse | Same |
| Cutscene camera | Constant speed between eased ends, cuts over whip pans, no roll while moving, always skippable. Limits, skip and repeat rules: `cutscenes-and-cinematics.md` §5 and §8 | Hold each shot at its final framing; cuts and fades only |
| Screen wobble ("dizzy", "drunk") | Avoid | Off |
| Vehicle camera | Follow yaw; optional damped pitch | Horizon-locked: never inherit roll |

Implementation:

- One **comfort module** answers "how much motion?" for every system (keys, defaults and the resolver sketch are in §10; other guides point there). Effective reduced motion = the game override (`follow`, `on`, `off`) resolved against `GuiService.ReducedMotionEnabled`; fire a signal on change so long-running loops stop mid-session. Reading the setting only at effect start is the most common bug `[lihfolk]`.
- Apply the shake scale once, at the point where all camera offsets get added up; scaling inside each effect lets a new effect forget it `[lihfolk]`. The slider runs 0–100% and defaults to 100%, so the per-hit values in `vfx-and-juice.md` §7 must already be comfortable at the default (§1: the default game must pass).
- FOV slider 60–100, default 70 (`Camera.FieldOfView` clamps 1–120 `[official]`). One owner writes the property; sprint, zoom and ultimates add named offsets to the player's base. Symptom of a missing owner: FOV resets after the first sprint.
- Flashes are a **separate toggle** from reduced motion: some players want one and not the other (also requested on the DevForum `[community]`).
- **Flash gate.** WCAG 2.3.1: nothing flashes more than three times in any one-second period (unless the flash is below the general and red flash thresholds). Roblox does not enforce it. Flashes come from many systems and many players at once, so route every large-area brightness change (impact frames, lightning, rarity strobes, other players' ultimates) through one limiter, and never use saturated red full-screen flashes `[lihfolk]`.

```lua
--!strict
-- Unexecuted sketch (client): every large-area flash asks this gate first.
local MAX_PER_SECOND = 2 -- stays under the three-per-second guideline
local stamps: { number } = {}

local function tryFlash(flashesEnabled: boolean): boolean
	if not flashesEnabled then return false end
	local now = os.clock()
	while stamps[1] ~= nil and now - stamps[1] > 1 do
		table.remove(stamps, 1)
	end
	if #stamps >= MAX_PER_SECOND then return false end -- caller falls back to a soft vignette
	table.insert(stamps, now)
	return true
end
```

Hit-stop is client presentation only (slow the animation tracks on clients that see the hit); never pause server simulation. Damage numbers: setting `all` / `mine` / `off`, merge hits on one target within about 0.15 s, cap about 12 on screen, pooled labels `[lihfolk]`. Juice itself is in `vfx-and-juice.md`.

## 6. Sound: captions, cues, mixing, haptics

Roblox has no built-in captions for in-game audio `[lihfolk][VS]`; `[official]` guidance is to pair sound events with visual cues and give separate volume controls.

- **Two caption kinds:** subtitles (speech, with speaker name) and sound captions ("[Boss roars, behind]"). Caption a sound only if a hearing player would act differently because of it: off-screen threats, wind-ups, state changes heard but not seen, music that signals something. Do not caption ambience or UI clicks.
- **Muted-play test:** play a full session with sound off and list every time you were surprised or killed by something you would have heard. Each item needs a caption or a visual.

| Caption rule `[lihfolk]` (subtitling practice, rule of thumb) | Value |
|---|---|
| Lines visible | 2, at most 3 |
| Characters per line | About 40 on phones, 60 on desktop |
| Display time | `clamp(0.06 × characters + 0.5, 1.5, 7)` seconds, or the audio length if longer (slow on purpose: many readers are young) |
| Position | Bottom centre, above the thumb zones and hotbar |
| Background | Plate with adjustable opacity, following `PreferredTransparency` |
| Repeats | Merge by key: "[Gunfire, left] ×10" |
| Priority | Threat captions outrank ambient ones |
| Default | Subtitles on; sound captions opt-in, offered in the first session |

- Build captions on the client from events the server already sends; put an optional `caption` key on each sound definition so the play helper calls the caption queue. Never put player-written text in a caption without filtering.
- **Directional indicator:** an arc on a ring around screen centre, angle from `atan2(rel.X, -rel.Z)` in camera space, plus an up/down chevron for other floors. In competitive modes it must reveal no more than the audio would at that distance and occlusion, or it becomes a wallhack everyone turns on `[lihfolk]`.
- **Mixing:** at most five groups (Music, SFX, Speech, UI, Ambient); defaults around 0.6 music and 0.8 SFX `[lihfolk]`; a mute-music toggle; duck music under speech; a one-tap "speech clarity" preset (music 30%, ambient 40%, speech 100%). Dialogue routed into the Music group is the classic bug. No engine mono-downmix switch was found `[VS]`, so direction must also be visual. Mixing craft is in `audio-sfx-music.md`.
- **Haptics:** `HapticEffect` presets (`UIClick`, `GameplayCollision`, `GameplayExplosion`) reinforce timing `[official][VS]`; give them their own on/off, and test on a real controller and phone.
- **Music-carried information** (rhythm, "the music changes when the monster is near") needs a visual equivalent: a beat marker or tension meter; `AudioAnalyzer` levels can drive it on the client `[VS]`.
- **Voice is never required** (`community-moderation-safety.md` §5): most players in a server cannot use it.
- Text to speech: `AudioTextToSpeech` exists `[official][VS]`; limits and filtering rules were not verified in this pass, so prototype before promising it.

## 7. Controls: remapping, hold/toggle, one-handed, aim assist

Baseline (from `ui-input-crossplatform.md`): every action has keyboard, gamepad and touch bindings. On top of that:

- **Every sustained action (charge, block, crouch, aim, sprint) offers hold or toggle.** Implement it as a wrapper around the input, and force toggles off on death, stun, menu open and `UserInputService.WindowFocusReleased`, or the player respawns still sprinting `[lihfolk]`.
- **Hold-to-repeat** for repeated presses (click, mine, roll) at a fixed rate such as 5 per second: in clickers and simulators it is the most important motor feature `[lihfolk]`. It still passes the same server rate limits. Hold-to-repeat is free; fully unattended auto-play can be a pass (§11 auto-collect).
- **No mashing, no long holds without an alternative, no two-button chords without a single-key option, a dedicated key for any double-tap.** An assist setting may widen the combo buffer to the 0.30 s cap (default 0.15–0.20 s; `game-craft.md` §1.2 owns the windows). Conflict: `[lihfolk]` suggests 300–400 ms; above 0.30 s inputs start firing that the player no longer intends.
- **Remapping model** `[lihfolk]`: stable action ids; two keyboard slots and one gamepad slot per action; defaults in code and only differences saved (a new action then reaches everyone); a conservative reserved list (Escape, the key that opens your settings); on conflict **swap** rather than error; capture ignores reserved keys and Escape cancels; gameplay input is sunk while capturing; a reset per action and for all.
- **Labels:** `UserInputService:GetStringForKeyCode()` for every key hint. `KeyCode`s are positional, so `KeyCode.Q` is the "A" key on AZERTY `[official]`; raw `KeyCode.Name` shows French players the wrong letter.
- **Saving:** the client sends the whole table when the remap screen closes; the server sanitises it against the action list like any remote payload.
- With the Input Action System, rebinding changes `InputBinding.KeyCode`; runtime writability of each property from a LocalScript was not confirmed by the vault authors `[lihfolk][VS]`. Test it, and keep `ContextActionService` rebinding as the fallback.
- **One-handed presets** `[lihfolk]`: left hand (WASD plus Q E R F Z X C, Shift, Space, 1–5), right hand (arrows or IJKL plus numpad), mouse only (click-to-move plus a radial menu). The camera is the hard part: offer a follow camera, keyboard turn, or lock-on. On gamepad avoid `ButtonL3`/`ButtonR3` for frequent actions.
- **Touch layout editor** (large cost, large payoff in mobile combat): own your buttons (not auto-generated ones), store each as scale position inside the safe-area container plus a size multiplier 0.75–1.5 and opacity 0.3–1, per device bucket; block overlap with the stick zone; keep ≥ 44 px targets; offer reset and a left-handed mirror (`x → 1 − x`); re-run the overlap check after loading on a different aspect ratio `[lihfolk]`.

Aim assist scales by **active input** (`UserInputService.PreferredInput`), not device `[lihfolk]`:

| Input | Friction (slowdown on target) | Magnetism | Bullet bend cone |
|---|---|---|---|
| Keyboard and mouse | Off | Off | Off |
| Gamepad | Medium | Low | Off or tiny |
| Touch | Medium | Medium | A few degrees |

Rules: line of sight is mandatory; select targets at about 20 Hz among tagged targets near screen centre; outgoing hit volumes are generous and incoming hurtboxes accurate; the server validates range, sight and rate with bounded tolerance whatever the client's assist did (`networking-and-security.md`). In ranked modes either give assist to everyone as a setting or separate queues.

## 8. Difficulty, assists and cognitive load

Difficulty is several dials, not one `[lihfolk]`. "Easy / Normal / Hard" may exist as presets that set them.

| Assist | Range (example) | Kind in a shared server |
|---|---|---|
| Damage taken | 50–100% | Personal: per-player value applied in the one damage function |
| Timing windows (parry, dodge, QTE) | 100–200% | Personal: server widens its accepted window |
| Hints, waypoints, objective reminders | On/off, frequency | Personal |
| Checkpoint frequency, fall protection | More checkpoints; ledge reset instead of death | Personal |
| Aim assist, lock-on, damage dealt, stage skip | — | Personal but affects fairness: flag any score earned with it |
| Game speed, enemy count, boss health | — | World-level: only in a solo or party instance (reserved server), by a stated party rule |

- Assists are **server-authoritative**: the client requests, the server clamps to the schema, stores and applies. A client-trusted multiplier is god mode. Lock changes during combat so nobody toggles damage reduction to survive one hit `[lihfolk]`.
- **Leaderboards:** ranked PvP requires default values for fairness-affecting assists; PvE boards mark assisted entries. Record the flag when the score is earned, not when the board is read `[lihfolk]`.
- Never make the best rewards depend on assist-free play, never hide assists behind progression, never sell the way past a barrier you built (house rule 3; an obby skip product needs a free path such as "skip after N failures").
- **Adaptive help offers, never imposes:** after 3 failures at one obstacle show a small dismissible "Want a hint?" or "Skip?"; after about 90 s without progress pulse the objective; after days away show a "Last time…" recap `[lihfolk]`. Silent dynamic difficulty is visible in multiplayer and feels like cheating when noticed; if used, keep it small and personal.
- **Cognitive load:** working memory holds about four chunks. Count what the screen asks of a new player each minute for the first ten; more than four at once is a warning `[lihfolk]`.

| Load source | Fix |
|---|---|
| Several trackers, a timer and a popup at once | One active objective on the HUD, the rest in a log |
| Cooldowns held in memory | Sweep plus seconds on the button |
| Rules to memorise | Hint at the moment of choice |
| One verb on two keys; close button that moves | One key per verb; fixed positions |
| Offers or choices that expire while reading | No timers on choices that matter (also house rule 3) |
| "+12.5% LCK" | Words first: "+12.5% luck: rarer drops" |
| Popups in combat | Queue until calm (§11 notifications) |
| Systems all shown at join | Progressive disclosure: reveal a system when the player can use it |

- **Focus mode / simple HUD:** hides event banners, social buttons and secondary currencies; never hides health, the objective or danger warnings.
- **A world that cannot pause** needs rest: safe zones, an untargetable AFK state in safe areas, personal timers that pause in menus, checkpoint saves so a disconnect in PvE loses little.
- Measure: deaths, retries and quits per stage; assist adoption and session length after adoption; hint requests per puzzle. Send assist state as an analytics dimension, never as a monetisation segment (`analytics-and-discovery.md`).

## 9. Screen readers, localisation and RTL

- **Screen readers:** no documentation of screen-reader support for in-experience UI was found in `Roblox/creator-docs` (searched 2026-11-11) `[VS]`. Treat blind-accessible play as something the platform does not provide: do not claim it. What a game can do: full gamepad and keyboard navigation with a visible focus ring, distinct audio cues per menu and state, haptics, and optional spoken prompts.
- **Keyboard navigation:** Roblox ships a toggle for the keyboard-navigation shortcut next to Reduce Motion and Background Transparency (staff announcement, 2023-11-29) `[official]`; the selection rules in `ui-input-crossplatform.md` §Gamepad make it work.
- **Localisation:** capture and translation mechanics are in `growth-and-marketing.md` §9 and `ui-input-crossplatform.md` §Text. Accessibility adds: German, French and Portuguese run 20–35% longer and some short labels double `[lihfolk]`, so test the longest language at `Largest`; write short, verb-first sentences with digits (also the best reading level for a young audience); keep text out of images; `AutoLocalize = false` on player names.
- **RTL:** Arabic is in Roblox's automatic translation list `[official]`. `TextLabel`, `TextButton` and `TextBox` have `TextDirection` (`Auto` default, which renders right-to-left scripts right-to-left; `LeftToRight` and `RightToLeft` force it) `[official][VS]`. Layouts do not mirror themselves: reversing a horizontal `UIListLayout` means reversing `LayoutOrder` `[official]`. House approach: keep the HUD layout fixed (thumb zones do not change with language), set `TextXAlignment` per locale on paragraph text, test numbers and mixed Latin/Arabic strings, and never build sentences by concatenating fragments.

## 10. Settings architecture

One schema module in `ReplicatedStorage` lists every key with type, range and default. The client builds controls from it; the server sanitises with it; the profile stores only overrides `[lihfolk]`.

```lua
--!strict
-- Unexecuted sketch: shared schema; sanitize() runs on the client before applying and on the server before saving.
export type Spec =
	{ kind: "number", min: number, max: number, default: number }
	| { kind: "bool", default: boolean }
	| { kind: "choice", options: { string }, default: string }

local Schema: { [string]: Spec } = {
	musicVolume = { kind = "number", min = 0, max = 1, default = 0.6 },
	fov = { kind = "number", min = 60, max = 100, default = 70 },
	uiScale = { kind = "number", min = 0.8, max = 1.3, default = 1 },
	-- Comfort keys: this block is the single owner; vfx-and-juice.md, game-craft.md and cutscenes-and-cinematics.md read it.
	shakeScale = { kind = "number", min = 0, max = 1, default = 1 }, -- 100%: the per-hit values are tuned so the default is comfortable
	screenEffects = { kind = "number", min = 0, max = 1, default = 1 }, -- tint, blur and vignette strength; 0 removes them
	flashes = { kind = "bool", default = true }, -- impact frames and full-screen flashes; on still passes the flash gate
	hitStop = { kind = "bool", default = true },
	damageNumbers = { kind = "choice", options = { "all", "mine", "off" }, default = "all" },
	reducedMotion = { kind = "choice", options = { "follow", "on", "off" }, default = "follow" }, -- follow = GuiService.ReducedMotionEnabled
	sprintMode = { kind = "choice", options = { "hold", "toggle", "always" }, default = "hold" },
}

local function sanitize(raw: unknown): { [string]: any }
	local overrides: { [string]: any } = {}
	if typeof(raw) ~= "table" then return overrides end
	for key, spec in Schema do
		local v = (raw :: any)[key]
		if spec.kind == "number" and typeof(v) == "number" and v == v then -- v == v rejects NaN
			local clamped = math.clamp(v, spec.min, spec.max)
			if clamped ~= spec.default then overrides[key] = clamped end
		elseif spec.kind == "bool" and typeof(v) == "boolean" and v ~= spec.default then
			overrides[key] = v
		elseif spec.kind == "choice" and typeof(v) == "string" and table.find(spec.options, v) ~= nil and v ~= spec.default then
			overrides[key] = v
		end
	end
	return overrides -- unknown keys are dropped; defaults are never stored
end
```

Comfort resolver: the one function every camera, VFX and cutscene system asks, so no effect reads settings by itself. Its outputs are the reduced-motion column of the §5 table.

```lua
--!strict
-- Unexecuted sketch (client). `settings` = schema defaults merged with the player's overrides.
local GuiService = game:GetService("GuiService")
export type Comfort = {
	reduced: boolean, shake: number, kick: number, fovScale: number,
	screenEffects: number, flashes: boolean, hitStop: boolean,
}

local function resolve(settings: { [string]: any }): Comfort
	local reduced: boolean
	if settings.reducedMotion == "follow" then
		reduced = GuiService.ReducedMotionEnabled
	else
		reduced = settings.reducedMotion == "on"
	end
	return {
		reduced = reduced, -- cutscenes hold final framings and cut; UI snaps or fades; head bob, landing dip and drift are off
		shake = if reduced then 0 else settings.shakeScale, -- multiplies the summed shake offset once; roll is never produced
		kick = if reduced then 0.25 else 1, -- directional kick: the confirmation that survives
		fovScale = if reduced then 0.5 else 1, -- FOV offsets are halved, not removed: they carry information
		screenEffects = settings.screenEffects, -- under `reduced`, draw only steady vignettes, no pulses
		flashes = settings.flashes and not reduced, -- false: steady edge vignette plus a directional indicator instead
		hitStop = settings.hitStop and not reduced, -- false: keep the sound and the spark
	}
end
-- Recompute on every settings change and on GuiService:GetPropertyChangedSignal("ReducedMotionEnabled"),
-- then fire one Changed signal so running loops (shake, drift, looping tweens) stop mid-session.
```

- Apply instantly on the client; debounce and send once when the menu closes; ride the profile's normal autosave. Never write a DataStore per slider tick.
- Fetch settings **before** revealing the HUD (a `RemoteFunction` the client invokes avoids the race where the server fires before the listener exists), or the UI flashes default size then jumps `[lihfolk]`.
- **Device buckets:** audio, comfort and palette follow the account; graphics preset and touch layout are stored per bucket (`touch`, `desktop`, `gamepad`) chosen from `UserInputService.PreferredInput` (`Touch`, `KeyboardAndMouse`, `Gamepad`) when the session starts, or a phone inherits the PC's High preset `[lihfolk]`.
- Reset per section; "reset all" confirms; each control marks its default. Settings are reachable from the first second, including during the tutorial, with a gamepad, at maximum UI scale and `Largest` text.
- Menu contents, in the order players look for them: **Audio** (Music, SFX, UI or Speech sliders; mute music) · **Graphics** (Auto / Low / Medium / High, VFX density, hide other players' effects) · **Camera** (FOV, shake 0–100%) · **Comfort** (reduced motion follow/on/off, screen-effects intensity, flashes, hit-stop, damage numbers) · **Interface** (UI size, compact or focus HUD, palette, captions, tooltips, ping display) · **Controls** (hold/toggle, auto-sprint, keybinds, touch layout) · **Social** (ignore trades, duels or invites; hide others' pets) · **Assists**.

## 11. QoL catalogue

Each row: what players get, how to build it, the trap. Server validation and fairness notes are `[house]` unless tagged.

| Feature | Implementation notes | Trap |
|---|---|---|
| Sprint, auto-run | Setting `hold` / `toggle` / `always`; "always" is the best touch default when walking has no purpose `[lihfolk]`. Server picks speed from its own state | Sprint remote that accepts a speed value |
| Auto-collect, collect radius | Server-side magnet by distance; the free baseline must already be painless (generous radius, walk-over pickup). The paid pass adds convenience (wider radius, collect while away), never makes manual collection worse after launch | A pickup made tedious so the pass sells: the "timer that exists to be paid away" pattern in `monetization-and-policy.md` |
| Skip and speed | Cutscenes show Skip at 2 s on any scene over 3 s (`cutscenes-and-cinematics.md` §8 owns the rule); hatch and reward animations: full on first view, tap to skip afterwards; a "fast animations" toggle; skipping grants exactly what watching grants, on the server, idempotently keyed by source id. Tutorial skip applies every step's grants `[lihfolk]` | Skip hidden behind a timer; skippers left without the starter item |
| Loading | Closes on a real ready signal with a hard timeout (the vault uses 20 s) and an honest skip; no fake progress bars; at most one modal in the first minute `[lihfolk]`. See `performance.md` for join time | Bar stuck at 99% |
| Bulk actions | Buy max, open ×N, sell all commons, claim all. Server executes with a per-request cap (for example 200 items); preview grouped by rarity; default ceiling at uncommon; locked and equipped items always excluded `[lihfolk]` | Client sends the item list as authority |
| Inventory sort, filter, search | Client-side on the replicated copy. Comparator needs a unique tiebreak (or items jump and `table.sort` can error); plain-text `string.find(s, q, 1, true)`; debounce search 0.15 s; keep scroll position after sort or sell; stack identical items as counts `[lihfolk]`. Virtualise long lists (`ui-input-crossplatform.md`) | Scroll resets to top after every sale |
| Lock / favourite | Server flag checked in **every** destructive path (sell, trade, fuse, delete); auto-lock above a rarity threshold (setting to disable); equipped behaves as locked; lock icon in every list `[lihfolk]` | UI-only lock that a second menu forgets |
| Confirmation and undo | Friction by damage `[lihfolk]`: trivial → none; cheap → undo toast (server keeps the last sale a few seconds; refuse undo if the proceeds were spent; commit the sale immediately so a crash means no undo, never a dupe); valuable or bulk → dialog with numbers and the most valuable item shown; irreversible (rebirth, delete slot) → summary plus hold 1.5 s, default focus on Cancel, confirm button not where the trigger was. No custom confirm before a Robux prompt: the platform prompt is the confirm | Confirms on everything train click-through; "sell, buy, undo" dupes |
| AFK handling | `Player.Idled` fires on the client after about 2 min idle then every 30 s; Roblox disconnects at 20 min `[official]`. Keep a server-side activity model (accepted remotes, movement, purchases) for reward eligibility. Any earlier idle kick warns 3 min ahead with a sticky toast and a friendly message; never idle-kick private or reserved servers; never fake input to dodge the disconnect `[lihfolk]`. AFK pay policy stays as in `liveops-quests-retention.md`: prefer none; otherwise the same capped rate offline | Movement-only detection kicks players reading a menu |
| Rejoin / reconnect | Button: save, release the profile, then `TeleportAsync` with `TeleportOptions.ServerInstanceId = game.JobId`; fall back to a new server if full; the profile loader retries a held session lock (`data-and-purchases.md`). Handle `TeleportInitFailed` with a visible retry | Rejoin lands on "data locked" |
| Server hop, server list | No engine API lists public servers: each server registers itself in a MemoryStore sorted map with a 15–30 s refresh and short TTL; skip when `game.PrivateServerId ~= ""`; servers cache and relay the list. Show players, friends here, build version, event state. Ping to another server cannot be measured: show the current `Player:GetNetworkPing()` and, at most, the average ping of players in that server `[lihfolk]`. Hop cooldown 10–30 s | Invented per-server ping; private servers leaked in the list |
| Join friend | `Player:GetFriendsOnlineAsync()` cached 30–60 s, filtered to this game; server resolves and teleports; say why when it fails (full, private match). Parties: one `TeleportAsync` call for the whole group with `TeleportOptions.ReservedServerId` set to a fresh `HttpService:GenerateGUID(false)` (`ReservedServerAccessCode` and `ShouldReserveServer` are deprecated) `[official][VS]`. Invite button via `SocialService:PromptGameInvite` where useful, never as a popup | Friends teleported one by one and split; trusting teleport data for loadout |
| Private servers | Detect with `game.PrivateServerId` / `PrivateServerOwnerId`; owner panel (kick from this server, toggle events, reset map); a "Private server" badge; state whether rewards match public servers. Pricing rules are in `monetization-and-policy.md` | Public event and idle-kick rules forced on owners |
| Spectate | For round-based and permadeath modes: `Camera.CameraSubject` on a living player's Humanoid, next/previous buttons, target's name and health; with streaming, the server sets the spectator's `Player.ReplicationFocus` to the target `[VS]`. Spectators do not chat to the living in competitive modes (delivery rule in `community-moderation-safety.md` §4) | Dead players watching a wall for three minutes |
| Respawn | Delay by genre `[lihfolk]`: obby and simulator 0–1 s; casual combat 2–4 s; team shooter 4–8 s. `Players.RespawnTime` defaults to 5 s `[official]`. "Respawn now" after a minimum; death recap; no shop or ad popup on death (house rule 3). Spawn protection as a server flag with an end time that ends on the first attack; a `ForceField` is ignored by code that sets `Health` directly | Protected players attacking freely |
| Performance mode | Presets map levers the engine does not know `[lihfolk]`: VFX density 0.35 / 0.7 / 1.0 through one emit helper, decorative shadows, post effects (keep colour correction), ambient animation, other players' trails. Never hide gameplay telegraphs on Low. The default preset comes from the device bucket (§10: touch → Medium, others → High `[house]`), never from Roblox's quality level (§2). The preset is a ceiling: under it a frame-time governor may lower VFX density by itself (`vfx-and-juice.md` §11). Changing the preset is only ever offered: a watchdog (median far above 33 ms for 30 s) **offers** Low once. `performance.md` owns budgets | A "render distance" slider when streaming radius is place-wide |
| UI scale, compact HUD, hide HUD | §4 slider. Compact is a layout variant with fewer elements (3–4 icons plus a drawer), not a smaller scale; auto-suggest under about 500 px viewport height `[lihfolk]`. Hide-HUD keeps critical warnings and a faded restore button on touch | Mobile player stuck with no HUD |
| FOV slider | §5 | — |
| Mute and ignore | Music mute; per-player emote and sound mute (client); ignore trades, duels and invites (server rejects silently, never "you were blocked"); hide others' pets and effects (also a performance win). The block list comes from `StarterGui:GetCore("GetBlockedUserIds")` with retry until registered `[official][lihfolk]` | Blocked player still able to send trades |
| Clear errors | Remotes return typed results the client maps to text: "Need 120 more coins", "Inventory full (200/200). Sell or lock items", "Dash ready in 1.4 s". Log raw errors, never show them `[lihfolk]` | Silent rejection (reads as lag or a bug) |
| Notifications | One notifier with channels `[lihfolk]`: critical (1, sticky, never muted), personal (3 visible, 3–4 s), social (2), server-wide (1, throttled by rarity), minor (merged into a counter). Queue capped around 8; drop stale; merge by key. No action buttons in a toast that disappears: use an inbox | Rare-drop shouts flooding big servers |
| Data-safety reassurance | Save indicator driven by **server** save results: saving → saved (2 s) → retrying (amber) → not saving (sticky; freeze premium spending) `[lihfolk]`. Purchases show processing → granted receipt → "delayed, will arrive automatically, even if you rejoin" after about 15 s, which is true because unacknowledged receipts are re-sent `[official]`; no upsell on the receipt | A client timer that blinks "Saved" during an outage |
| Ping display | Off / when high (above about 250 ms) / always; rolling average | Lag blamed on players when the server is overloaded |
| Tooltips | Hover 0.4 s on mouse, `SelectionGained` on gamepad, long-press or an (i) on touch; clamp to the viewport `[lihfolk]` | Hover-only help invisible on phones |
| What's new | Once per version, skipped for brand-new players, never blocking; the canonical patch notes (`community-moderation-safety.md` §13) | Shown on every join |
| Anti-frustration | Coyote time and jump buffer (`ui-input-crossplatform.md`); generous checkpoints; hints after repeated failure (§8); bad-luck protection on free random rewards (on paid random items pity changes the odds that must be disclosed); nothing lost on disconnect; cooldowns predicted locally and gated on the server | Punishing a player for the game's own lag |

## 12. QoL audit ranked by cost

Run on four devices (small phone, tablet, PC, gamepad) with a fresh account and a veteran save, record the session, and repeat the social items with a second account `[lihfolk]`. Fix order: anything that loses progress or money → the first 60 seconds → controls on the majority platform → the rest. Effort assumes an existing profile-based save.

**Small (under half a day each)**

- [ ] Music and SFX sliders; mute music; every sound in a group.
- [ ] Every menu sets a selection on open; gamepad B and an on-screen close button close it (Escape belongs to the Roblox menu, so never rely on it).
- [ ] Every rejected action shows a reason and next step.
- [ ] Shake 0–100% at the sum point; flashes toggle plus the flash gate.
- [ ] Loading screen closes on a ready signal with a timeout; one modal at most in the first minute.
- [ ] Hold/toggle for sprint and aim, cleared on death and menus.
- [ ] Rejoin button; friendly idle warning.
- [ ] Cooldown sweep and seconds on ability buttons.
- [ ] Sort tiebreak and kept scroll position; plain-text search.
- [ ] Greyscale pass on the main screens and telegraphs.

**Medium (one to three days each)**

- [ ] Settings schema, server sanitising, overrides saved, device buckets.
- [ ] Graphics presets with real VFX density; telegraphs exempt.
- [ ] Item lock enforced in every destructive path; tiered confirms; undo for cheap sells.
- [ ] Purchase processing, receipt and delayed states; server-driven save indicator.
- [ ] Skippable tutorial with server-side grants; replayable tips.
- [ ] UI-size slider with fit clamp; compact HUD.
- [ ] Notification queue with channels, caps and merge.
- [ ] Captions for threat and state sounds; muted-play test passed.
- [ ] Respawn-now, death recap, spawn protection.
- [ ] Text-fit audit at `Largest` and the longest language.

**Large (a week or more)**

- [ ] Full rebinding with presets, glyphs and one-handed layouts.
- [ ] Touch layout editor.
- [ ] Friends panel, party teleports, server list.
- [ ] Palette modes over semantic tokens with a numeric audit.
- [ ] Assist dials with fair leaderboards.

Re-rank for the audience: phone-heavy games move presets, compact HUD and the touch editor up; combat moves cooldowns, buffering, assist and spawn protection up; simulators move locks, bulk actions, AFK rules and notification caps up `[lihfolk]`. Ship small items as they land and announce each batch; QoL shipped silently is not noticed.

## 13. Level-up: symptoms → likely cause → fix

| Symptom (reviews, feedback dashboard, analytics) | Likely cause | Fix |
|---|---|---|
| "Can't tell teams / rarities apart" | Hue-only signals; small pips; equal lightness | Second channel, lightness gap, greyscale pass |
| "Makes me dizzy / headache" | Camera roll in shake or dashes, head bob, stacked FOV writers, flashes from many players | §5 table (roll 0); one FOV owner; flash gate; follow `ReducedMotionEnabled` |
| Mobile sessions far shorter than desktop | Text under 14 px rendered; hold-only sprint; no assist on touch; High VFX on a 3 GB phone | §4 audit; hold/toggle and "always" sprint; aim friction; preset offer from the watchdog |
| Deaths cluster at one obstacle, then quits | Timing window or checkpoint spacing; hazard heard but not seen | Checkpoint; hint offer after 3 failures; visual cue |
| "Sold / fused my best item by accident" | No lock, bulk action includes rares, confirm under the same thumb | Locks, rarity ceiling, tiered confirm, undo |
| "Paid and got nothing" tickets | No processing state; delayed receipt shown as failure | Purchase states; idempotent receipt handler (`data-and-purchases.md`) |
| "Game ignores my clicks" | Silent server rejection; no pressed state | Typed results mapped to messages; local feedback under 100 ms |
| Settings reset every join, or the phone gets PC graphics | Client-only storage; no device bucket | Profile overrides; buckets |
| Players stuck sprinting or aiming after respawn | Toggle state not cleared | Force-off on death, menu, focus loss |
| Friends cannot play together | Teleports one by one; full-server joins fail silently | Group teleport; failure reasons; private-server guidance |
| Idle-kick complaints | Movement-only detection; no warning; private servers included | Server activity model; warning; exemptions |
| Toasts arrive late or bury "inventory full" | Unbounded single queue | Channels, cap, sticky critical |
| Wrong key shown in prompts for some countries | `KeyCode.Name` labels | `GetStringForKeyCode` |
| Low assist adoption but high quit rate at hard content | Assists hidden, shamefully named or locked behind progression | Surface in settings and in the fail-streak offer; rename |
| Downvote spike after a "polish" update | A platform setting was replaced or a default changed for everyone | Read platform settings; overrides-only saves; announce changes |

## 14. Conflicts

- **Text floor.** LihFolk measures 14 px body and a 12 px hard floor on phones `[lihfolk]`; this skill's house targets are HUD ≥ 18, body 16, captions 14 (`ui-input-crossplatform.md`), in line with the XAG figures quoted there. Trust the house targets for design; use 12 px rendered only as the audit's fail line.
- **UI scale range.** XAG-style guidance says text scalable to 200%; LihFolk caps a whole-UI slider at 1.3 because layouts overflow phones. Both hold: text grows through `PreferredTextSize` in growing layouts, while the whole-UI multiplier stays 0.8–1.3 with a fit clamp.
- **AFK income.** LihFolk allows AFK zones with lower, capped income; `liveops-quests-retention.md` says prefer none and pay the same capped rate offline. The house position stands (no pay-to-idle servers); LihFolk's server-side activity model and warning rules are adopted.
- **Colour-blind filter.** Some community posts ask for a platform filter; Roblox staff said it will not ship one. Build redundancy and palette modes.
- **Shake roll.** LihFolk's camera module clamps roll at 4° and rolls on a dash, while its comfort note says no gameplay roll; the comfort note wins here and in `vfx-and-juice.md` §7: roll is 0 in gameplay. A static tilted cutscene frame is a composition choice, not shake (`cutscenes-and-cinematics.md` §5).
- **Reading Roblox's quality level.** LihFolk and earlier versions of this skill mapped `SavedQualityLevel` to effect presets. Roblox staff asked developers to stop on 2026-11-05 and plan to deprecate the API; presets now start from the device bucket and the player's own choice.
- **Auto features.** LihFolk treats auto-click as accessibility; many games sell auto passes. Resolution: hold-to-repeat is always free; unattended automation may be a pass, and the free loop must not be degraded to sell it.

## Review gate

- [ ] Greyscale and muted-play passes done on the first ten minutes and the hardest fight; every failure has a second channel.
- [ ] No colour-only signal; team, rarity, heal/damage and telegraphs each have shape, text or pattern.
- [ ] Rendered text meets the house floors on the small phone; text-fit audit clean at `Largest` × maximum UI size × longest language.
- [ ] `ReducedMotionEnabled`, `PreferredTextSize` and `PreferredTransparency` followed and re-read on change; no platform setting duplicated; nothing reads `SavedQualityLevel`.
- [ ] Every text-on-colour pair in the theme passes the computed WCAG ratio (4.5:1, or 3:1 for large text and icons).
- [ ] Camera never rolls in gameplay (grep the shake and dash modules for a non-zero third `CFrame.Angles` argument); one FOV owner; shake scaled at the sum point; flash gate holds ≤ 2 large flashes per second with several players' effects.
- [ ] Sustained actions have hold/toggle; no mash, long-hold or chord without an alternative; key labels from `GetStringForKeyCode`.
- [ ] Settings: one schema, server-sanitised, overrides only, device buckets, reachable in the first second with every input.
- [ ] Shake, screen effects, flashes, hit-stop and cutscene motion all read the §10 comfort resolver (no system reads the settings or `ReducedMotionEnabled` itself); with reduced motion on, a hit still shows a marker or vignette and no camera rotation.
- [ ] Assists are server-side, locked in combat, flagged on leaderboards, never sold and never a condition for the best rewards.
- [ ] Locks enforced on the server in every destructive path; tiered confirmations; no extra confirm before Robux prompts.
- [ ] Save indicator and purchase states reflect server results; every rejection has a message.
- [ ] AFK, rejoin, join-friend, private-server and respawn behaviours decided, tested with two accounts, and failure reasons shown.
- [ ] Nothing in this file is implemented with primitive Parts or marketplace models; telegraphs and world markers are Blender meshes with collision where solid.
- [ ] Live game: the symptom table was checked against the Feedback dashboard and funnel data before choosing fixes, and each batch was announced.

## Sources

Accessed 2026-11-11 unless dated. "(read)" = opened and read; "(search summary)" = seen only through web search result text on 2026-11-10 and not re-opened.

- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `42 Accessibility and Inclusive Design/` (Accessibility Start Here; Colour-Blind Safe Design; Readable Text and UI Scale; Motion Sensitivity and Camera Comfort; Captions and Audio Accessibility; Input Remapping and One-Handed Play; Difficulty Options and Cognitive Load), `58 Player QoL and Game Tweaks/` (Top 25 QoL Wins by Effort; QoL Audit Checklist; Settings Menu Essentials and Persistence; AFK Detection Idle Kicks and AFK Reward Rules; Server Hop Rejoin and Server Lists with Ping; Joining Friends Parties and Private Servers; Confirmation and Undo Patterns; Inventory QoL; Feedback - Autosave Indicator Ping Display and Error Toasts; Graphics and Performance Toggles; Block and Mute Respecting Platform Rules; Purchase Receipts and Purchase History in UI; Quick Respawn and Spawn Protection; Notification Queues and Limits; Comfort Toggles; Camera Settings; Aim Assist and Generous Hitboxes; Hold vs Toggle; Skippable Tutorials; UI Scale HUD Hide and Compact Mode; Loading Screen Skip; Mobile Button Layout Editor; Colourblind Palettes Text Size and Tooltips) (read)
- `Roblox/creator-docs` (commit of 2026-11-10), https://github.com/Roblox/creator-docs (read): `production/publishing/accessibility.md`; `production/localization/automatic-translations.md`; `ui/list-flex-layouts.md`; engine reference for `GuiService` (`PreferredTextSize`, `PreferredTransparency`, `ReducedMotionEnabled`), `UserInputService.PreferredInput`, `UserGameSettings`, `Camera.FieldOfView`, `Player.Idled`, `Players.RespawnTime`, `Player:GetFriendsOnlineAsync`, `Player:GetNetworkPing`, `TeleportOptions`, `SocialService`, `StarterGui` core calls, `TextLabel.TextDirection`, `HapticEffectType`, `AudioTextToSpeech`
- Staff DevForum posts (read): Introducing Accessibility Settings, 2023-11-29, https://devforum.roblox.com/t/2723187 (the settings; staff reply 39 on colour-blind filters) · Increasing the Minimum Draw Distance to 500 Studs and Other Auto-Quality Level Improvements, 2026-11-05, https://devforum.roblox.com/t/4977292 (`SavedQualityLevel` planned for deprecation)
- https://devforum.roblox.com/t/feedback-on-accessibility-guidelines/3819039, https://devforum.roblox.com/t/accessibility-text-to-speech-in-engine-captioning/1006734, https://devforum.roblox.com/t/making-accessible-games-for-the-disability-aware-era-a-not-fully-comprehensive-guide-by-an-actual-disabled-developer/1375919 (search summary)
- WCAG 2.x: contrast formula and thresholds (1.4.3, 1.4.11) and the three-flash criterion (2.3.1) are stated from the standard as known, with the worked ratios computed on 2026-11-11; the W3C pages and Machado, Oliveira and Fernandes 2009 were not opened
- `references/ui-input-crossplatform.md`, `references/liveops-quests-retention.md`, `references/monetization-and-policy.md`, `references/vfx-and-juice.md`, `references/cutscenes-and-cinematics.md` (read, for consistency)
- Not read: reddit.com (not reachable). Several "Roblox accessibility settings" pages on pages.dev mirror domains were ignored as SEO spam (they describe a colour-blind toggle that official sources do not).
