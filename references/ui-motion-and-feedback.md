# UI motion and feedback: tokens, button response, reward sequences, springs, reduced motion

How Roblox UI should move and answer the player: a small set of motion tokens, the rules that keep motion from breaking under fast input, what a button does in the first 100 ms, how rewards are staged from a +5 coin to a top-tier reveal, which engine or library to animate with, and what replaces motion when the player turns it down. Open it when adding motion to a screen, staging a reward, or when players call the UI laggy, flat or slow. Visual design is in `ui-design-figma.md`; screens in `ui-screen-recipes.md`; the presenter that opens windows in `ui-input-crossplatform.md` §UI architecture; world effects, hit-stop and camera in `vfx-and-juice.md`; UI sound sets in `audio-sfx-music.md` §9.

Tags: `[official]` Roblox docs and staff announcements, `[community]` DevForum, GitHub and third-party craft writing, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0, rewritten; field values from one production game: starting points, not laws), `[VS]` version-sensitive, `[house]` house rule or estimate.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Copy the Motion module (§8) and use only its tokens. (2) Give every button press, release and a click sound (§4). (3) Counters count up; windows scale in from 0.9 and fade (§2). (4) Honour reduced motion through the module. | Springs, queues, reward ladders |
| Intermediate | State-driven open and close with proportional retarget; stagger and lead-follow; the reward ladder with four beats; fly-to-counter; pending states that mask latency; reduced-motion table | Custom spring solvers |
| Expert | Shared spring loop with zero idle cost; reward queue with priority, merge, safe moments, anti-starvation and compression; reveal time budget per hour; style transitions for Studio-authored states; MicroProfiler check during entrances | Nothing |

## Contents

1 What motion is for · 2 Motion tokens · 3 Rules that hold up under fast input · 4 Button and control feedback · 5 Reward and feedback sequences · 6 Tween, transition or spring · 7 Reduced motion · 8 Motion module · Level-up table · Review gate · Sources

## 1. What motion is for

UI motion has four jobs: orientation (where it came from, where it went), causality (what my input did), hierarchy (what to read first) and state (busy, ready, locked, new). An animation that does none of them is cut `[lihfolk]`. Movement is also the strongest attention tool on the screen, so "moderation is key": too many bright, moving elements overwhelm instead of guiding `[official]`. Feedback is not optional: without it players cannot tell whether an action worked or the game is broken `[official]`; young players expect feedback on every action, in sound, picture and text together, because some cannot read and some play muted `[community]` (Google's kids guidance).

## 2. Motion tokens

Define motion as a handful of tokens; no screen creates its own `TweenInfo`.

| Token | Duration | Easing | Animate | Notes |
|---|---|---|---|---|
| `press` | 0.06–0.10 s | Quad Out | child `UIScale` to 0.92–0.96; face sinks into the lip | Under 0.08 s nothing is visible at 30 fps |
| `release` | 0.16–0.30 s | Back Out | `UIScale` to 1 | |
| `hover` / focus | 0.10–0.12 s | Quad Out | `UIScale` 1.04–1.06 | Gamepad focus looks at least like hover, plus the ring |
| `enter` | 0.18–0.26 s | Back Out (playful) or Quint Out (clean) | `UIScale` from 0.90–0.92 (not from 0) + fade | Full-screen surfaces about 1.3× longer |
| `exit` | 0.10–0.15 s | Quad In or Quint In | scale to 0.90 + fade | 0.55–0.75× the enter time; never Back In |
| `move` | 0.20–0.40 s | Quad or Sine InOut | `Position` | Scale with distance (§3) |
| `emphasis` | 0.25–0.45 s | Back Out | `UIScale` pop 1.2 → 1 | Reward icons, badge arrival, counter on arrival |
| `toggle` / selector | 0.10–0.16 s | Quad Out | knob position, track colour | Keep the colour change under reduced motion |
| `fill` | 0.35 s | Quad Out | bar `Size.X.Scale` | Fast start reads responsive |
| `countUp` | `clamp(0.35 + 0.22 × log10(gain), 0.35, 1.8)` s | Quad Out (Exponential Out for huge jumps) | a number driving text at ≤ 10–30 Hz | +1 → 0.35 s, +1,000 → 1.0 s, +1,000,000 → 1.67 s |
| `idle` (breathe, bob) | 0.6–0.8 s half period | Sine InOut, `Reverses`, `RepeatCount = -1` | transparency, ±3 px, rotation | One per screen; pause when hidden |
| `timer` / cooldown | real duration | Linear | fill | Linear only for things that represent time |
| `shine` | 1.2 s every 3 s | Linear | `UIGradient.Offset` −1 → 1 | One element per screen `[community]` |
| `shake` (error) | 6 steps of 0.04 s: ±8, ±5, ±2 px | none | `Position` offset | Colour flash only under reduced motion |

Durations are `[lihfolk]` field values. Perception bands: under 0.1 s reads as instant, 0.1–0.2 snappy (feedback, exits), 0.2–0.35 visible (entrances), 0.35–0.6 deliberate (big reveals only), above 0.6 the player is waiting. Elastic and Bounce are for a single reward icon, never a panel the player must read. Direction carries meaning: HUD parts slide from their edge, overlays scale from the centre.

**Conflict:** the official accessibility sample tweens a settings panel over 0.75 s, and a Style Editor transition is inserted with a default of 1 s `[official]`. Field reports have players calling 0.3 s opens sluggish and settle at 0.14–0.26 s open, 0.12–0.14 s close `[lihfolk]`. Use the short values for navigation; keep long durations for reward sequences the player is enjoying.

## 3. Rules that hold up under fast input

`[lihfolk]` unless tagged.

- **Distance-scaled moves.** `duration = clamp(0.12 + 0.012 × sqrt(pixels), 0.15, 0.45)`: 40 px → 0.19 s, 200 px → 0.29 s, 600 px → 0.41 s. Measure pixels from `AbsolutePosition`, not scale.
- **Stagger with a cap.** 0.05–0.07 s per item for 2–5 items, 0.03–0.04 s for 6–12, total never above 0.4 s (`step = min(step, 0.4 / (n − 1))`); beyond 12 items stagger the first row only.
- **Lead and follow.** Container first, content 0.04–0.08 s later and shorter so both finish together, primary button last with a small pop. Exits leave together. Overlap steps with `task.delay`; do not chain on `Completed`.
- **State, not events.** Store `wantOpen` and animate toward it from one function. Hide on `Completed` only when `playbackState == Enum.PlaybackState.Completed` and the intent is still "closed". `Tween:Cancel()` leaves the property where it was `[official]`.
- **Proportional retarget.** A close interrupted at 80% needs about 20% of the enter time to reopen: multiply the token time by the remaining fraction, floor about 0.3.
- **Input from the first visible frame.** Never disable buttons until an entrance ends; set the gamepad selection when the entrance starts. Locked input is the usual cause of "the UI feels laggy" with short tweens.
- **Pick the property.** Pop with a child `UIScale` (cheap, scales text and strokes with it); tweening `Size` re-runs sibling layout, re-wraps text and makes `TextScaled` text step. Never tween `Position` of a child owned by a layout: animate an inner face. Fade a panel with `CanvasGroup.GroupTransparency` or per element toward each stored base transparency. Do not tween `UIStroke.Thickness` on text `[official]`.
- **Two scales, two objects.** The root carries device scale, an inner frame carries pop scale; two `UIScale`s on one object fight.
- **Squash honestly.** `UIScale` is uniform; a real squash sets width = 1 / height on the art layer only (never the text), jumps to the extreme pose at once and springs back.

## 4. Button and control feedback

What one press does, in order `[house]` (timings from §2; sound rules in `audio-sfx-music.md` §9):

| Time | Channel | What happens |
|---|---|---|
| 0 ms (input began) | Visual | Face sinks 3–4 px into the lip or scales to 0.94; brightness −8% |
| 0 ms | Sound | One short click from the UI set, pitch-varied a few percent; client-side only |
| 0 ms | Haptic | `HapticEffect` of type `UIClick` on gamepads and phones that support haptics `[official]`; primary actions only |
| on release inside | Visual | `release` back to 1 with a small overshoot; the action fires on `Activated` |
| on release | State | If a server answer is needed: the button enters `pending` at once (spinner or progress in place of the label, `Interactable = false`), then `done` or an inline error with a `shake` |
| on drag off | Visual | Returns without firing |

- The response is local and inside 100 ms; the server result reconciles afterwards. Waiting for the server before any feedback is why buttons "feel dead".
- Hover exists only for mouse; on touch the press state is the only preview, so make it obvious. Gamepad focus replaces hover (`ui-input-crossplatform.md` §Gamepad and console).
- Studio-authored buttons can get hover and press from style rules on `GuiState` (`:Hover`, `:Press`) with transitions, no script `[official][VS]`; anything stateful (pending, retarget) still needs code.
- Controls: a toggle moves its knob and changes a word or icon; a slider's fill follows the finger with no tween; a tab indicator slides (`toggle` token) or springs; a disabled control explains itself on tap instead of staying silent.
- Tutorial pointers: a pulse, wiggle or arrow on exactly the next button, one at a time `[official]`.

## 5. Reward and feedback sequences

Scale the response to the event; return to rest afterwards. The short loop sequence (pickup pops → icon flies → counter counts up → goal bar advances) is in `game-craft.md` §1; this section is the UI build spec.

| Event | Channel | Sequence |
|---|---|---|
| Small gain (`+5`) | Floating number at the point of action | Rise 24–40 px and fade over 0.6–1.2 s; merge same-kind within 0.5 s; counter counts up |
| Currency batch | Fly-to-counter | 5–12 icons leave the source 0.03–0.05 s apart on curved paths (a `Path2D` or a two-segment tween), 0.35–0.5 s each; the counter pops (`emphasis`, 1.15×) on each arrival and counts up to the server's value; one rising tick, capped per second |
| Purchase | Inline on the button, then toast | `pending` → tick + the "paid" sound used nowhere else → the item flies to its home button, which gains a badge. Celebrate what was bought, not the spending `[lihfolk]` |
| Claim (daily, quest) | Card | Card pops, reward icon jumps to the counter, the card settles into `done` with a tick; `Claim all` staggers with the cap from §3 |
| Level up, zone unlock | Centre banner | 2–4 s, queued and gated (`ui-screen-recipes.md` §11); bar fills to 100%, flashes once, resets with the new goal visible within 1 s |
| Rare drop, hatch, roll | Reveal | Four beats below, length by tier |

Tier ladder `[lihfolk]` (rule-of-thumb values; each tier adds a layer rather than only getting longer or louder):

| Tier | Length | Layers added |
|---|---|---|
| Common | 0.3–0.5 s | Card pop, soft sound, count-up |
| Uncommon | 0.6–0.8 s | Rarity colour wash, brighter sound |
| Rare | 1.0–1.5 s | Particle burst, short riser before the reveal |
| Epic | about 2 s | Screen-edge glow, banner, small FOV punch |
| Legendary | 3–4 s | One full-screen colour wash, stronger shake, music sting |
| Top one or two tiers | 5–6 s | World dims, HUD hides, server-wide line |

The four beats, for a 3.5 s Legendary `[lihfolk]`:

| Beat | Time | What happens |
|---|---|---|
| Anticipation | 0.0–1.2 s | Container shakes with growing amplitude, riser climbs, light leaks from the seams. Starts on the tap and masks the server round trip: the reveal waits for the reply |
| Reveal | 1.2–1.5 s | One flash or rarity colour wash, burst, item appears at 1.15× with an instant squash and spring back. The sound peaks on this frame |
| Payoff | 1.5–3.0 s | Name and rarity banner slide in, stats count up, sting peaks, particles drift |
| Settle | 3.0–3.5 s | Effects fade, buttons appear last; the primary one becomes clickable about 0.3 s later |

Rules `[lihfolk]` unless tagged:

- **The server decides before anything animates**; the animation lands on that result. Reels and carousels show only items this player could really have received; escalating tells (blue, purple, gold glow) derive from the real result, never random drama. No engineered near-miss on anything bought with Robux (house rule 3; `genres/rng-rolling.md`).
- **Budget the time.** Reward animations stay under about 10% of play time: 200 opens an hour at 3 s each is 10 minutes of watching. Repeats and auto modes use a compact reveal (a small card over the character); only results at or above a player-chosen tier interrupt.
- **Skippable after the first view**: a tap after about 0.5 s jumps to the payoff, not past it. First-of-a-kind and milestones get the full sequence; repeats the compressed one.
- **Reserve channels.** If only the top tiers dim the world and hide the HUD, the darkening itself becomes the signal.
- **Queue big moments**: priority (rarer first), merge same-kind in a short window ("+3 items", best shown), safe-moment check (not in combat, no cutscene, not dead, no window open), anti-starvation (after about 20 s downgrade to a toast), compression (more than three waiting → each at half length).
- **Do not celebrate** a net loss ("You won 5 coins!" after paying 50), another player's failure in front of them, or a paid result more loudly than an earned one of the same tier.
- **Safety**: at most three full-screen flashes a second, prefer one soft wash; tier readable without sound (colour + label + shape); never a timed decision inside a celebration (`accessibility-and-player-qol.md` §5).

## 6. Tween, transition or spring

The general comparison of `TweenService`, `GetValue`, `SmoothDamp` and hand-rolled springs is in `vfx-and-juice.md` §9. For UI:

| Tool | Use for | Facts |
|---|---|---|
| `TweenService:Create` through the Motion module | Default: presses, entrances, fills, count-ups | Fixed duration; a retarget restarts from the current value (apply the proportional rule) |
| Style transitions (`StyleRule` + transition, tokens of type `TweenInfo`) | Hover, press and theme changes on Studio-authored UI, previewed at edit time | Fully released Jul 2026; run in the engine, cheaper than Luau tweens unless hundreds play at once; per-property transitions cost less than a default-all transition; the inserted default is 1 s: replace it `[official][VS]` |
| `TweenService:SmoothDamp(current, target, velocity, smoothTime, …)` | Followers: tab indicators, bars chasing a value | Critically damped, no overshoot; returns value and velocity; number, Vector2, Vector3, CFrame `[official]` |
| `spr.target(instance, dampingRatio, frequency, props)` | Motion retargeted constantly; playful pops | Damping < 1 overshoots, 1 is critical; README examples use 1 at 1 Hz (slow, no overshoot) and 0.6 at 4 Hz (quick wobble); `spr.stop`, `spr.completed`; animates Color3 in a perceptual space `[community]` |
| Ripple (`createSpring`, `createTween`, `createMotion`) | Value-based motion in code-built UI (React, Vide) | Springs by `tension`/`friction`/`mass` or `frequency`/`dampingRatio`; `onChange` callback; Color3 in Oklab; connects to Heartbeat only while animating when `start = true` `[community]` |
| React Luau bindings | Animating inside React without re-rendering | "A form of signals-based state that doesn't re-render" (README): drive bindings from a spring or tween, never component state at 60 Hz `[community]` |

- Starting points `[house]`: follow motion, damping 1.0 at 4–6 Hz; playful pop, damping 0.5–0.7 at 3–5 Hz.
- Run all Lua springs from one shared connection that disconnects when everything has settled: an idle HUD costs zero Lua per frame `[lihfolk]`. Infinite tweens keep running while a screen is hidden: cancel them on close.
- A constantly animated element re-composes its whole ScreenGui every frame: give it its own small ScreenGui (`ui-input-crossplatform.md` §UI performance).

## 7. Reduced motion is not "no feedback"

`GuiService.ReducedMotionEnabled` reflects the platform setting `[official]`; offer the same switch in the game's settings, because many players never find the platform one `[lihfolk]`. Style rules can branch on it with the `@ReducedMotionEnabledTrue` query selector `[official][VS]`.

| Normal | Reduced |
|---|---|
| Panel scales in | Fade 0.1–0.15 s |
| Press squash, hover lift | Colour or brightness change |
| Staggered cards | All appear together |
| Currency flies to the counter | Counter pulses its colour once and counts up |
| Shake, idle bobbing, rays behind an item | Static |
| Reveal with shake, zoom, particle storm | Tier colour, banner and sound stay; movement goes |

## 8. Motion module (unexecuted sketch)

```lua
--!strict
-- Shared/UI/Motion.luau: the only place a UI TweenInfo is created. Approach adapted from LihFolk's motion notes, rewritten.
local GuiService = game:GetService("GuiService")
local TweenService = game:GetService("TweenService")
export type Token = "press" | "release" | "hover" | "enter" | "exit" | "move" | "emphasis" | "fill"
local Out, In = Enum.EasingDirection.Out, Enum.EasingDirection.In
local TOKENS: { [Token]: TweenInfo } = {
	press = TweenInfo.new(0.08, Enum.EasingStyle.Quad, Out),
	release = TweenInfo.new(0.2, Enum.EasingStyle.Back, Out),
	hover = TweenInfo.new(0.11, Enum.EasingStyle.Quad, Out),
	enter = TweenInfo.new(0.22, Enum.EasingStyle.Back, Out),
	exit = TweenInfo.new(0.13, Enum.EasingStyle.Quad, In),
	move = TweenInfo.new(0.28, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut),
	emphasis = TweenInfo.new(0.3, Enum.EasingStyle.Back, Out),
	fill = TweenInfo.new(0.35, Enum.EasingStyle.Quad, Out),
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
-- Count-up duration scaled by the size of the gain.
function Motion.countUpTime(gain: number): number
	return math.clamp(0.35 + 0.22 * math.log10(math.max(gain, 1)), 0.35, 1.8)
end
return Motion
```

The interruption-safe presenter that uses it is in `ui-input-crossplatform.md` §UI architecture.

## Level-up: motion and feedback symptoms → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| "UI feels laggy" although tweens are short | Input locked until the entrance ends; full enter time after an interrupted close; 0.5–1 s defaults left in | Input from the first frame; proportional retarget; token durations (§2–3) |
| Window opens, then vanishes when reopened quickly | Close tween's `Completed` hides the window without checking state | Hide only on `PlaybackState.Completed` and when the intent is still "closed" |
| Buttons feel dead; taps seem ignored | No pressed state or sound; feedback waits for the server | Local response inside 100 ms, then pending, then reconcile (§4) |
| Every window opens with a different animation | Per-screen `TweenInfo`s | Motion tokens; direction carries meaning |
| Numbers snap; rewards feel like a spreadsheet | No count-up, no arrival pop | `countUp` scaled by gain; fly-to-counter (§5) |
| Collection grind feels slow despite pretty reveals | Reveal time not budgeted per hour | Tier ladder, compact auto mode, skip after first view |
| Big drops do not feel big | Lower tiers already use the strongest channels | Reserve world dimming and HUD hiding for the top |
| Accidental confirms after a reveal | Buttons clickable the moment they appear | Buttons last, primary delayed about 0.3 s |
| Level-up never shows in long fights, or covers the boss | Queue with no maximum wait, or no safe-moment check | Reward queue with anti-starvation and gating (§5) |
| Players say rolls are rigged | Reel shows unreachable items; random tells | Reel from the real pool; tells from the result |
| Idle HUD costs frame time | Perpetual tweens on hidden screens; per-frame Lua springs | Cancel on close; one shared spring loop that disconnects |
| Motion-sensitive players complain | Reduced motion ignored, or treated as "no feedback" | Route everything through the module; mapping in §7 |

## Review gate

- [ ] Every UI tween goes through the Motion module; no screen creates a `TweenInfo`; no transition left at an editor default.
- [ ] Every button: pressed state and click inside 100 ms, pending state where the server answers, disabled state that explains itself.
- [ ] Ten rapid taps on any open/close button end in the last requested state; exits are faster than entrances; no window blocks input while it animates.
- [ ] Counters count up; currency gains have an arrival; nothing loops forever except at most one subtle idle per screen.
- [ ] Reward tiers mapped to lengths and layers; reveal time under about 10% of an hour of play; repeats skippable; buttons appear last.
- [ ] Server decides results before the animation; reels and tells are honest; no near-miss on paid rolls; no celebration of a net loss.
- [ ] Big moments go through one queue with priority, merge, safe-moment and maximum-wait rules; burst-tested.
- [ ] Reduced motion (platform and in-game) swaps movement for fades and keeps the information; flashes within limits.
- [ ] Springs share one connection that disconnects at rest; idle HUD shows no per-frame Lua in the MicroProfiler.

## Sources

Accessed 2026-11-11 unless noted.

- `Roblox/creator-docs` mirror, commit `7cbffff` (read): `production/game-design/ui-ux-design.md` (attention, feedback), `ui/animation.md` (section list and style transitions), `ui/styling/editor.md` (transitions and the inserted default), class reference `TweenService` (`SmoothDamp`), `GuiService`, enums `GuiState`, `HapticEffectType`: https://github.com/Roblox/creator-docs
- Roblox staff announcements (read): styling transitions, full release Jul 2026 https://devforum.roblox.com/t/4646870 · StyleQuery with `ReducedMotionEnabled` https://devforum.roblox.com/t/4566519
- https://github.com/Fraktality/spr (read: README) · https://github.com/littensy/ripple (read: README) · https://github.com/Roblox/react-luau (read: README)
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault) (read): `05 UI and UX/UI Motion Language and Timing.md`; `47 Game Feel and Juice/Reward Moments and Celebrations.md`; `47 Game Feel and Juice/Squash Stretch and Anticipation in UI and Characters.md` (TL;DR and the latency-mask section heading only)
- Google, "Designing engaging apps" (kids; read) https://developers.google.com/building-for-kids/designing-engaging-apps
- Talks verified to exist, not watched (oembed): Martin Jonasson and Petri Purho, "Juice it or lose it" https://www.youtube.com/watch?v=Fy0aCDmgnxg · Jan Willem Nijman, "The art of screenshake" https://www.youtube.com/watch?v=AJdEqssNZ-U
- Related in this repo (read): `game-craft.md` §1, `vfx-and-juice.md` §9 and §12, `audio-sfx-music.md` §9
