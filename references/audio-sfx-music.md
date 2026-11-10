# Audio: API, licensing, SFX design, mixing, spatial sound, music, memory

What this is: the build-level reference for sound on Roblox: which audio system to use and how to wire it, what audio may legally be used or uploaded, how to design, time, vary and mix sound effects, spatial audio, adaptive music, UI sound sets, loudness, memory and preload on phones, and volume settings. Open it when adding sound to a new game or when a live game sounds repetitive, late, muddy, silent or too loud. It extends `game-craft.md` §4 (bus tree, loudness targets, ducking numbers) and the audio line of `performance.md`; neither is repeated. Visual timing is in `vfx-and-juice.md`.

Tags: `[official]` Roblox docs (mirror commit ccc2b01), `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; numbers from one production game are starting points), `[VS]` version-sensitive (the audio API, limits and licence terms change often), `[house]` house estimate. Terms: *SFX* = sound effect; *one-shot* = a short sound played once; *bed* = a quiet loop under everything; *bus* = a group of sounds sharing one volume control; *ducking* = lowering one bus while another plays; *onset* = time from file start to first audible energy; *peak* = time to the loudest transient; *stinger* = a short musical hit on an event; *voice* = one sound playing right now.

## Contents

Start here by level · 1. The two audio systems · 2. Wiring the audio graph · 3. Licensing: what you may use and upload · 4. Upload limits and moderation · 5. SFX design: layers, variation, timing · 6. Mixing: buses, loudness, ducking, voice limits · 7. Spatial audio and rolloff · 8. Music: playlists, adaptive layers, stingers · 9. UI sound sets · 10. Memory, preload and mobile · 11. Volume settings and accessibility · 12. Level-up table · Review gate · Sources

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Use only Creator Store audio published by Roblox, or sound you made yourself. (2) Play every feedback sound on the client. (3) Give each core verb and each UI action a sound, pitch-varied ±5%. (4) Four buses with sliders: Music, SFX, Ambience, UI. (5) Set min and max distance on every 3D sound; never leave the defaults | Adaptive music, acoustic simulation, sidechain compressors |
| Intermediate | Layer sounds (transient, body, tail). Three or more takes per frequent sound, drawn from a shuffle bag. Trim every file so the transient starts within 10 ms. Level every file to one loudness target before upload. Cap voices and add per-cue cooldowns. Two-deck music crossfades. Keep an asset manifest with licence and uploader | Sample-accurate scheduling, custom attenuation curves |
| Expert | Schedule sounds so the peak lands on the hit frame. One listener per 3D category wired to its own bus. Stems started on mixer time; bar-quantised transitions. Sidechain ducking. Measure loudness in-engine. Load audio per area and verify the Sounds memory label on a phone | — |

## 1. The two audio systems `[VS]`

Roblox has two systems. The docs now say `Sound`, `SoundGroup` and `SoundEffect` "are now discouraged in favor of the more robust functionality of audio objects" `[official]`; the audio graph left beta according to a DevForum announcement `[community]`.

| | Legacy | Audio graph |
|---|---|---|
| Source | `Sound` (`SoundId`, `Volume` 0–10 default 0.5, `PlaybackSpeed`, `Looped`) | `AudioPlayer` (`Asset`, `Volume` 0–10, `PlaybackSpeed` 0–20, `Looping`, `PlaybackRegion`, `LoopRegion`, `AutoLoad`, `IsReady`) |
| 2D or 3D | 3D when parented to a `BasePart` or `Attachment`, 2D anywhere else | 2D: wire the player to an `AudioDeviceOutput`. 3D: wire it to an `AudioEmitter` in the world; an `AudioListener` hears it and is wired to the output |
| Buses | `SoundGroup` (assign `Sound.SoundGroup`); nestable; `Volume` multiplier 0–10 | `AudioFader` (`Volume` 0–10); any object can feed any other through a `Wire` |
| Effects | `EqualizerSoundEffect`, `ReverbSoundEffect`, `CompressorSoundEffect` (has `SideChain`) and others, parented to a Sound or SoundGroup | `AudioEqualizer`, `AudioFilter`, `AudioCompressor` (extra `Sidechain` pin), `AudioLimiter`, `AudioReverb`, `AudioEcho`, `AudioChorus`, `AudioFlanger`, `AudioDistortion`, `AudioPitchShifter`, `AudioTremolo`, `AudioGate`; wired in line, order matters, each has `Bypass` |
| Rolloff | `RollOffMinDistance`, `RollOffMaxDistance`, `RollOffMode` | `DistanceAttenuationMode` presets with `DistanceAttenuationBounds`, or a custom curve from `SetDistanceAttenuation`; `SetAngleAttenuation` for directional sources |
| Scheduling | Frame-quantised (`task.delay`) | `Play(atTime)` and `Stop(atTime)` against `SoundService:GetMixerTime()`, sample-accurate; `Cancel(actionId)` revokes |
| Analysis | `PlaybackLoudness` | `AudioAnalyzer` (`PeakLevel`, `RmsLevel`, spectrum), `AudioPlayer:GetWaveformAsync` |
| Other | `SoundService:PlayLocalSound`, `VolumetricAudio` on parts, Doppler | Voice input (`AudioDeviceInput`), `AudioTextToSpeech`, `AudioSpeechToText`, acoustic simulation (§7) |

Which to use:

| Situation | Choice |
|---|---|
| New game | Audio graph for everything. It is the documented path and the only one with real routing, scheduling and acoustic simulation |
| Live game on `Sound` and `SoundGroup` that works | Keep it. Migrate one bus at a time when you need per-category 3D buses, beat-accurate music, custom curves or occlusion |
| Both in one game during migration | Allowed, but they are separate mixes: wire each settings slider to the `SoundGroup` and to the matching `AudioFader`, and re-test ducking. A toggle left wired to the old system is a classic "music slider does nothing" bug `[lihfolk]` |

Facts that bite:
- Clicking an audio asset in the Toolbox inserts a legacy `Sound`; copy the asset id into an `AudioPlayer` instead `[official]`.
- An `AudioPlayer` alone is silent: nothing is heard until a wire reaches an `AudioDeviceOutput` `[official]` `[community]`.
- `AudioPlayer.Ended` does not fire for looping players or when stopped early; `IsReady` can turn false again under extreme memory pressure `[official]`.
- `AudioPlayer:Play()` and `:Stop()` called on the server replicate to clients; `AudioDeviceOutput.Player` restricts who hears a server-side graph `[official]`. Build feedback graphs on the client anyway.
- `SoundService.RespectFilteringEnabled` is true by default, so a `Sound` played from a LocalScript is heard only by that client `[official]`.
- `SoundService.CharacterSoundsUseNewApi` switches the default footstep and jump sounds to graph instances `[official]`; check it before replacing character sounds.
- `GetMixerTime()` starts at an arbitrary value and differs between machines: use it to schedule locally, never to synchronise players `[official]`. For shared timing send `Workspace:GetServerTimeNow()` and convert on each client.

## 2. Wiring the audio graph

Two canonical graphs `[official]`: 2D is `AudioPlayer → Wire → AudioDeviceOutput`; 3D is `AudioPlayer → Wire → AudioEmitter` (parented to a part or attachment) plus `AudioListener → Wire → AudioDeviceOutput`. A `Wire` has `SourceInstance` and `TargetInstance` (pins default to `Output` and `Input`); many wires into one input mix, one output can feed many wires; `Wire.Connected` is false when a pin name is wrong or the wire would form a cycle `[lihfolk]`.

Listener: `SoundService.DefaultListenerLocation` is `Default` (a camera listener only in experiences with voice chat), `Camera`, `Character` or `None`. With `Camera` or `Character` the engine also creates the `AudioDeviceOutput` and wires it `[official]`. For real buses choose `None` and build the graph yourself: one listener per 3D category, separated by `AudioInteractionGroup` (an emitter is heard only by listeners in the same group), each wired to its category fader `[lihfolk]`.

```lua
--!strict
-- Unexecuted sketch. Client module. Requires SoundService.DefaultListenerLocation = None.
-- Category faders → Master → Limiter → device, plus one camera listener per 3D category.
local SoundService = game:GetService("SoundService")
local Mix = {}
local faders: { [string]: AudioFader } = {}

local function wire(source: Instance, target: Instance, pin: string?)
	local w = Instance.new("Wire")
	w.SourceInstance, w.TargetInstance = source, target
	if pin then w.TargetName = pin end -- "Sidechain" on an AudioCompressor
	w.Parent = target
end

local output = Instance.new("AudioDeviceOutput")
local limiter = Instance.new("AudioLimiter")
limiter.MaxLevel = -1 -- dB: safety ceiling on the whole mix
local master = Instance.new("AudioFader")
output.Parent, limiter.Parent, master.Parent = SoundService, SoundService, SoundService
wire(limiter, output)
wire(master, limiter)
faders.Master = master
for _, name in { "SFX", "UI", "Music", "Ambience" } do
	local fader = Instance.new("AudioFader")
	fader.Name = name
	fader.Parent = SoundService
	wire(fader, master)
	faders[name] = fader
end
for _, name in { "SFX", "Ambience" } do -- world sounds reach their own bus
	local listener = Instance.new("AudioListener")
	listener.AudioInteractionGroup = name
	listener.Parent = workspace.CurrentCamera -- re-parent if CurrentCamera is replaced
	wire(listener, faders[name])
end

function Mix.bus(name: string): AudioFader
	return faders[name]
end
function Mix.setVolume(name: string, slider: number) -- slider 0..1 from the settings menu
	faders[name].Volume = math.clamp(slider, 0, 1) ^ 2 -- squared: loudness is logarithmic
end
return Mix
```

- 2D sound: parent an `AudioPlayer` anywhere and wire it to `Mix.bus("UI")` or `"Music"`.
- 3D one-shot: an `AudioPlayer` and an `AudioEmitter` (same `AudioInteractionGroup` as its listener) parented to the part or attachment, one wire between them; pool the pairs for frequent sounds.
- Sidechain ducking: put an `AudioCompressor` between the Music fader and Master, and wire the SFX (or voice) fader into its `Sidechain` pin.
- One effect can serve many sources: a single `AudioReverb` per room, fed by every sound in that room `[lihfolk]`. `AudioAnalyzer` levels are zero on the server; poll them on the client `[lihfolk]`.

## 3. Licensing: what you may use and upload

Audio is the asset type most likely to be removed after launch, and a removed sound fails silently. Not legal advice.

| Source | Risk | Rule |
|---|---|---|
| Creator Store audio published by Roblox and its partners (more than 100,000 professionally produced SFX and music tracks, free to use `[official]`) | Lowest inside Roblox | First choice. Filter by creator. The licence covers use in Roblox experiences; a trailer on another platform is a separate question: check the track's terms or use music you own `[lihfolk]` |
| Sound you recorded, synthesised or composed | Low | Keep project files and dated exports as proof |
| Commissioned music or SFX | Low with a contract | Written grant: perpetual, worldwide, the game and its sequels, Roblox plus trailers, ads and streams; exclusivity stated; composer does not register the track with content-ID systems or whitelists you; stems, loop points and stingers delivered `[lihfolk]` |
| Licensed third-party libraries (free or paid professional packs) | Medium | Read the licence for "video games" and for redistribution. Upload as private assets under the game's owner and never tick distribution on the Creator Store: that hands the raw sound to every creator, which library licences forbid `[lihfolk]`. LihFolk lists specific vendors with licence notes dated 2026-10-29; not verified here |
| Community uploads on the Creator Store | Medium | Roblox allows it, but the rights chain cannot be checked; prefer verified creators |
| AI-generated audio | Medium | Same platform rules as any upload; your rights depend on the generator's terms on the day you generated `[lihfolk]` |
| Commercial songs you do not own | High | Never upload. The risk is to the uploading account, not only the game |

- Roblox-licensed music has usage terms. A developer post quoting them says: no streaming service or music library inside an experience, no charging players to hear a specific track, and at most 250 distinct licensed tracks in one experience at a time `[community]` `[VS]`. Read the current Licensed Music terms before building a radio.
- Player-entered audio ids (boombox, radio) are the highest-risk feature: the game becomes a player for any infringing or abusive upload. Offer a curated list of tracks you may use; if ids must be allowed, restrict to a reviewed whitelist with per-player mute, a volume cap and an "all radios off" setting. Never sell free id entry `[lihfolk]`.
- Group-owned game: upload audio to the group or grant the experience permission. A personal upload in a group game works in Studio and is silent live `[lihfolk]`.
- Since the 2022 audio privacy change, audio over 6 seconds became private and new uploads are private by default `[community]`; old third-party ids in inherited scripts are usually silent. Replace them.
- Manifest: one row per asset id with source, licence, uploader, date, measured loudness, onset and peak. Run a periodic load check on music ids with a fallback track per context, because a takedown produces silence, not an error `[lihfolk]`.
- Streamer mode: a setting that swaps music for tracks you own outright keeps content-ID claims off the creators who promote the game `[lihfolk]`.

## 4. Upload limits and moderation `[VS]`

| Rule | Value | Source |
|---|---|---|
| Format | One track; `.mp3`, `.ogg`, `.wav` or `.flac` | `[official]` |
| Size and length | Under 20 MB and under 7 minutes | `[official]` |
| Sample rate and channels | At most 48 kHz; mono, stereo, 3.0 or 5.1 | `[official]` |
| Rights | You must hold the legal rights; Community Rules and Terms of Use apply | `[official]` |
| Quota, Studio and Creator Dashboard | 2,000 free uploads per 30 days if ID-verified, 100 if not | `[official]` audio page |
| Quota, Open Cloud | 100 per month if ID-verified, 10 if not | `[official]` Open Cloud page. Conflict between two official pages: plan pipelines around the stricter number |
| Processing | Studio transcodes on import and rejects corrupt or invalid files; uploads then wait in a moderation queue and are visible only to you | `[official]` |
| Privacy | Imported audio is private; you grant use to specific people and experiences | `[official]` |
| Classification | Each upload is classified as a sound effect or a song. Songs can appear on the game details page if they pass moderation and copyright checks, meet duration and play thresholds, have a meaningful title, and the uploader is ID-verified and has accepted the Audio Terms | `[official]` |

- Freshly uploaded assets can fail to load or preload for 20–60 seconds `[lihfolk]`; never judge or ship an id uploaded seconds ago.
- No official loudness normalisation of uploads was found; forum threads describe inconsistent levels `[community]`. Level files yourself (§6).

## 5. SFX design: layers, variation, timing

**Layering.** A single recording is seldom enough for an action. Build it from layers that each do one job and sit in different frequency ranges, so none hides another `[lihfolk]`:

| Layer | Job | Sword example | Length |
|---|---|---|---|
| Transient (attack) | The instant | Slash crack, contact thud | 5–60 ms |
| Body | Weight and character | Metallic or air swish | 100–300 ms |
| Tail | Size and space | Lower, quieter whoosh | Trim at −60 dB; melee 0.6 s total, explosions 2 s |
| Sweetener (optional) | Identity | Element sting: ice crackle, zap | Short |

Bigger actions earn more layers, not more volume. Short tails, or combos smear. Attack shapes meaning: a sharp transient reads as impact, a 30–60 ms swell reads as motion; never trim a whoosh to its loudest sample `[lihfolk]`.

**Variation** against the "machine-gun effect":

| Technique | Detail |
|---|---|
| Shuffle bag | 3 or more takes for anything frequent (4–6 for footsteps); draw without replacement; never the same take twice in a row `[lihfolk]` |
| Pitch | ±3–6% per play (`PlaybackSpeed` 0.94–1.06, about one semitone); less on tonal sounds |
| Volume | ±1–2 dB (a multiplier of about 0.8–1.0) |
| Layer recombination | 3 transients × 3 bodies × 3 tails = 27 combinations from 9 files `[lihfolk]` |
| Choke | A new play stops the previous one of the same layer on rapid repeats `[lihfolk]` |
| Combo climb | Each combo step one semitone higher (×1.059), capped at 4–5 steps `[lihfolk]` |

Do not randomise learned symbols: crit, kill confirm, rare-drop chime, a character's signature. `PlaybackSpeed` changes pitch and length together; for big creatures pick a lower take or use `AudioPitchShifter` rather than slowing a roar `[lihfolk]`.

**Timing.** Sound that leads the picture is noticed about three times sooner than sound that lags (broadcast thresholds are roughly 45 ms early and 125 ms late, ITU-R BT.1359). In a game the player caused the event, so tighten it `[lihfolk]`:

| Sound relative to the visual hit | Reads as |
|---|---|
| 20 ms or more early | Wrong; the sound seems to cause the hit |
| 0–30 ms late | Fused: the target |
| 30–80 ms late | Acceptable for heavy or distant events, soft for snappy hits |
| 80–150 ms late | Mushy; reported as input lag |
| Over 150 ms late | Two separate events |

Where the delay hides `[lihfolk]`: the file (many effects have 20–80 ms of lead-in before the transient, entirely under your control); first-use loading (an unloaded sound is late exactly once, on the player's first hit); output latency (Bluetooth earbuds commonly add 100–300 ms, which you cannot fix).

- Measure onset and peak once per file and store them in the manifest.
- Scheduled sounds (a hit on a known animation marker, footsteps): start at `beat − peak` so the transient lands on the frame.
- Reactive sounds (server-confirmed kill, pickup): trim so onset is under 5–10 ms, or set `TimePosition` to the onset before `Play()`.
- When in doubt err late, never early. Hit-stop: the impact plays at the start of the freeze and is never paused.
- Predict only the neutral contact on the attacker's client. Crit, block, kill, loot and "you were hit" wait for the server; a false hurt sound is worse than a late one `[lihfolk]`.
- A sound scheduled at input for a move that is then cancelled still plays unless it carries a cancellation token `[lihfolk]`.

```lua
--!strict
-- Unexecuted sketch. Client module. One preloaded AudioPlayer per take; shuffle bag; jitter; cooldown; choke on repeat.
local Mix = require(script.Parent.Mix)
export type Cue = { takes: { string }, volume: number, onset: number?, cooldown: number?, fixedPitch: boolean? }
type State = { players: { AudioPlayer }, bag: { number }, last: number, lastIndex: number }
local states: { [Cue]: State } = {}
local rng = Random.new()
local Sfx = {}

function Sfx.register(cue: Cue, busName: string) -- call when the owner loads (equip, spawn), not on first use
	local players = {}
	for i, asset in cue.takes do
		local player = Instance.new("AudioPlayer")
		player.Asset = asset -- AutoLoad is on by default: loading starts now
		player.Parent = Mix.bus(busName)
		local w = Instance.new("Wire")
		w.SourceInstance, w.TargetInstance, w.Parent = player, Mix.bus(busName), player
		players[i] = player
	end
	states[cue] = { players = players, bag = {}, last = 0, lastIndex = 0 }
end

function Sfx.play(cue: Cue)
	local state = states[cue]
	local now = os.clock()
	if not state or now - state.last < (cue.cooldown or 0.03) then return end -- 30 ms stops twenty identical hits in one frame
	state.last = now
	if #state.bag == 0 then
		for i = 1, #state.players do state.bag[i] = i end
		rng:Shuffle(state.bag)
		if #state.bag > 1 and state.bag[#state.bag] == state.lastIndex then -- no repeat across refills
			state.bag[1], state.bag[#state.bag] = state.bag[#state.bag], state.bag[1]
		end
	end
	local index = table.remove(state.bag) :: number
	state.lastIndex = index
	local player = state.players[index]
	player:Stop() -- choke the same take
	player.PlaybackSpeed = if cue.fixedPitch then 1 else rng:NextNumber(0.95, 1.05)
	player.Volume = cue.volume * rng:NextNumber(0.85, 1)
	player.TimePosition = cue.onset or 0 -- skip the lead-in
	player:Play()
end
return Sfx
```

**Sound as information** `[lihfolk]`: use sound for off-screen events (enemy noticed you, hazard incoming, rare thing nearby, action failed), keep the same danger sounding the same, rate-limit cues (an aggro alert at most once a second), give every information sound a visual twin, and remove sounds that fire for the wrong reason (footsteps triggering weapon accents, weapons humming under a full-screen menu). Review each sound four ways: muted, eyes closed, at 0.25× speed, and after 50 repeats.

## 6. Mixing: buses, loudness, ducking, voice limits

Bus tree, slider curve, loudness targets (−18 LUFS mobile, true peak at most −1 dBTP) and sidechain numbers are in `game-craft.md` §4. Additions:

**Loudness consistency.**
- Normalise every source file to one target before upload, so the per-cue `volume` value is the whole mix and swapping a take never changes the balance. One-shots: −18 LUFS momentary maximum (integrated loudness is unreliable on files under about half a second) with a −1 dBTP true-peak limit `[lihfolk]`.
- Level one-shots by peak and beds by RMS: peaks matter for short sounds, average energy for long ones `[lihfolk]`.
- Shape of a mix `[lihfolk]`: your own actions loudest, enemies below, other players' actions about 0.7×, UI far below combat, music and ambience a bed. After levelling, the loudest sound in the game is something the player caused and wanted.
- Measure in-engine with `AudioPlayer:GetWaveformAsync` or an `AudioAnalyzer` (`RmsLevel`, `PeakLevel`) when files cannot be re-exported `[official]`.
- Editing pipeline per file `[lihfolk]`: trim the head to just before the transient; 1–2 ms fade in and 10–50 ms fade out; high-pass below 30–40 Hz; mono for every 3D sound; normalise; export OGG at the native rate; measure peak time; upload under the game's owner; add the manifest row. Free tools (Audacity, a LUFS meter) are enough.
- Reject at source: clipped peaks, baked room reverb on positional sounds, a single take for a frequent sound, mismatched takes in one bag `[lihfolk]`.

**Ducking.** Lower Music and Ambience 3–6 dB under heavy hits and stingers, and 6–12 dB under dialogue, with a 250–500 ms release `[lihfolk]`. Three ways: a sidechain compressor on the bus (`CompressorSoundEffect.SideChain` in the legacy system `[official]`, the `Sidechain` pin in the graph); a scripted tween of the bus volume, which is easier to tune; or both. Conflict: the LihFolk SFX skill says legacy sounds cannot sidechain; the docs show a legacy ducking mix tree, so the docs win.

**Voice limits** `[lihfolk]`. Stacked copies of one file phase, clip and cost CPU (`Sound/stepInstances` in `performance.md`).

| Control | Starting value |
|---|---|
| Global live one-shots | 16 on touch, 24 on desktop |
| Per-cue cooldown | 30 ms minimum; 1 s for alerts; 8 s for boss intros |
| Per-cue instances | 2–4; own swings up to 7, all swings 28 |
| Crowd caps | Per enemy family, so 12 enemies do not play 12 identical growls |
| Steal order | Lowest priority, then farthest or quietest; never the player's own hit or hurt |
| Distance gate | Do not start a sound nobody can hear |

**Relevance rules** are part of the mix: write down what must stay silent (idle animations, menus open, cutscenes) and remove a bed that masks a gameplay cue rather than turning it down `[lihfolk]`.

## 7. Spatial audio and rolloff

Defaults are wrong for games: a legacy `Sound` rolls off from 10 to 10,000 studs, so every explosion is faintly audible map-wide and every footstep joins a murmur `[lihfolk]`. With `Inverse` and `Linear` modes a low maximum cuts off abruptly; `InverseTapered` tapers to zero `[official]`.

| Category | Min (full volume inside) | Max (silent beyond) |
|---|---|---|
| Footsteps | 4–6 | 40–60 |
| Melee swings and hits | 6–10 | 80–120 |
| Abilities, spells | 10–15 | 150–250 |
| Explosions, boss roars | 20–40 | 300–600 |
| Ambient spots (waterfall, machine) | Size of the source | 60–120 |

Starting values `[lihfolk]`; in the graph set the same numbers through `DistanceAttenuationBounds` with the `InverseTapered` preset, or draw a custom curve (flat, shoulder, fast drop, zero; up to 400 points) `[official]`.

- **Listener position.** The listener is the camera, often 15–25 studs behind a third-person character, so the player's own footsteps sound distant. Play the local player's own sounds in 2D (or with a large minimum) and other players' at their root `[lihfolk]`.
- **Directional sources**: `SetAngleAttenuation` makes a megaphone or a roar louder in front `[official]`. `AudioEmitter:GetAudibilityFor(listener)` returns 0–1 and can drive gameplay ("can the monster hear you?") `[official]`.
- **Acoustic simulation** `[VS]`: `SoundService.AcousticSimulationEnabled` plus `AcousticSimulationEnabled` on each emitter and listener gives occlusion, diffraction and reverberation `[official]`. DevForum announcements describe a beta followed by a full release, graph API only, with quality reduced or disabled on low-end devices `[community]`. Consequences: never make gameplay depend on occlusion (some players would hear through walls); use it for stealth and horror, test busy arenas for mud and CPU, and keep a non-simulated mix that still works.
- **Large sources**: legacy `SoundService.VolumetricAudio` lets a `Sound` on a big part surround the listener inside it (rain zones, crowds) `[official]`; in the graph use a 2D bed that crossfades by zone.
- **Streaming**: sounds parented to streamed-out parts stop (`performance.md`). Put critical ambience on always-present containers or play it 2D from the client.
- **Doppler** on fast legacy sounds can sound silly; lower `SoundService.DopplerScale` `[official]`.
- **Stereo files** for 2D only (UI, music, beds, own-character sweeteners); positional sources are mono `[lihfolk]`.

## 8. Music: playlists, adaptive layers, stingers

Music is client-side: each player hears their own mix, driven by state the server replicates (zone, combat, boss phase). Server-played music makes one player's boss fight everyone's soundtrack `[lihfolk]`.

**Baseline every game should have** `[lihfolk]`:
- Two decks: start the next track 4 s before the current one ends (watch `TimeLength − TimePosition`; `Ended` is too late) with an equal-power (sine) crossfade.
- A 2–3 s fade-in on join; the first sound of the game is never a full-volume downbeat.
- A playlist of several tracks with 30–90 s of silence between them; one 2-minute loop for a 30-minute session is a common complaint.
- Context switches (shop, boss, cutscene) resolved by a priority stack: cutscene > boss > shop > zone > default. Fade 1 s out and in; pause the background and resume where it was rather than restarting it (`Stop()` then `Play()` resumes from `TimePosition` `[official]`).
- Hysteresis on zone borders (a minimum time in a state, or separate enter and exit thresholds) so music does not flip.
- Ambience beds per zone, switched by the same zone lookup as lighting, 2.5 s crossfade, levelled by RMS under everything; indoors muffle the outdoor bed and add a room reverb instead of cutting to silence.

**Adaptive structures** (intermediate to expert):

| Structure | How | Notes |
|---|---|---|
| Vertical layering (stems) | One piece split into synchronised stems; intensity fades stems in and out over 0.5–1.5 s | Start all stems with `Play(atTime)` at `GetMixerTime() + 0.1`; sequential `Play()` calls drift `[official]` `[lihfolk]`. Smooth the intensity value over a few seconds; up at 0.6 and down at 0.4 (`game-craft.md`) |
| Horizontal resequencing | Segments switched at bar or phrase boundaries | Next boundary = `start + ceil((now − start) / barLength) × barLength` on mixer time, with `barLength = 240 / BPM` in 4/4; schedule `Play(atTime)` and `Stop(atTime)`; `Cancel` if the state flips back |
| Stingers | Short musical hits: level up, rare drop, boss appears, victory | Louder than the bed, duck the music for their length, quantise to the next beat only when the pulse is strong (a late stinger is worse than an off-beat one). Route them through the Music bus or muted players still hear jingles `[lihfolk]` |

Adaptive music is expensive to compose and costs memory (four stems across five states is twenty long assets). A small game gets most of the value from context switching, stingers and good silence `[lihfolk]`. Loops must be cut on a bar line with matched tails; a click at the loop point is the file. `LoopRegion` loops a section after an intro `[official]`.

## 9. UI sound sets

One family: same timbre, very short (under about 150 ms `[house]`), pitched up for positive and down for negative, levelled far below combat `[lihfolk]`.

| Event | Sound |
|---|---|
| Hover | Soft tick; none on touch devices; throttled so dragging across 40 buttons is not 40 ticks |
| Press | Pop click |
| Panel open, close | Short rise, short fall or air whoosh |
| Confirm, claim | Bright note; a rising run for big rewards |
| Purchase | A distinct "paid" cue, used nowhere else |
| Error, locked, cannot afford | Short low note, never harsh |
| Tab or page switch | Soft tick |
| Counter count-up | A tick that rises in pitch, capped at about 15 per second `[house]` |

Rarity ladder for rewards: each tier adds a layer (brighter sound, a riser before the reveal, a music sting at the top) rather than volume, and the riser peaks on the reveal frame `[lihfolk]`. Play UI sound on the client only; never fire a remote to play a click.

## 10. Memory, preload and mobile

- Audio files are a surprising memory cost when all are loaded at once `[official]`. Read the Sounds label in F9 > Memory on a 3 GB phone before and after a session.
- Keep `ReplicatedStorage` lean: audio that is not needed at join belongs in `ServerStorage` and is sent to the client when needed `[official]`. Simpler: create players for an area's sounds when the player enters it, and destroy them on exit.
- Preload only what the first minute needs: the first music track, the UI set, the core verb's sounds. A huge `PreloadAsync` list adds straight to join time (`performance.md`).
- Preload on approach, not on use: weapon sounds on equip, the boss track at the boss door `[lihfolk]`. `AudioPlayer.AutoLoad = false` defers loading until first play when memory matters more than first-play latency `[official]`.
- Forum reports: `PreloadAsync` on a sound that never began loading can report failure, and an unused sound may be unloaded again `[community]`. Trust `IsLoaded` or `IsReady`, not the preload callback.
- Many instances sharing one asset id cost little beyond the first `[community]`; unique long files are the real cost. Stems: keep only the current and next state's stems loaded `[lihfolk]`.
- File hygiene: mono for 3D, tails trimmed, OGG, no sample rate above 48 kHz.
- House budget `[house]`: at join, at most 1 music track, 1 bed and about 30 short one-shots loaded; at most 3 looping 3D sources audible at once on the low tier.

Mobile constraints:
- Phone speakers reproduce little bass: a sound that only works on headphones does not work. Check that combat cues stay audible over the loudest music state on a phone speaker `[lihfolk]`.
- Many phone players play muted or with their own music: every information sound needs a visual twin, and haptics can carry impact (`game-craft.md`).
- Wireless latency cannot be fixed; removing lead-in from files is what you control. An optional "audio lead" setting (0–250 ms) shifts scheduled sounds earlier for wireless users `[lihfolk]`.
- Lower voice caps (16), no acoustic simulation dependence, and reverb only where it is heard.

## 11. Volume settings and accessibility

- Sliders: Master, Music, SFX, Ambience (may share Music), UI; Voice if used. Square the 0–1 value before applying. Persist with player data and apply before the first sound plays.
- Every sound belongs to a bus. A `Sound` with no `SoundGroup`, or a player wired straight to the output, ignores the sliders `[lihfolk]`.
- Defaults: music low (it sits well under gameplay cues), fade in on join, nothing at full scale. The Roblox client's own volume (`UserGameSettings.MasterVolume`, 0–1 `[official]`) sits above yours; do not fight it.
- Nothing important may depend on a bus the player can mute: every warning has a visual twin, and information-bearing sounds that change what the player does get a caption or icon `[lihfolk]`.
- Test with music off, SFX at 10% and UI muted, on phone speakers, in a full server, after 20 minutes `[lihfolk]`.
- Comfort: a limiter at −1 dB on the master; no sudden loud sounds after silence; no piercing high-pitched loops; a mute for other players' radios; a streamer-mode music option.
- Mute or duck gameplay loops under full-screen menus and during cutscenes.

## 12. Level-up: symptom → cause → fix

| Symptom | Likely cause | Fix |
|---|---|---|
| A sound is silent live but plays in Studio | Uploaded to a personal account for a group game; no permission for the experience; removed asset | Upload under the owner or grant permission; manifest and load check |
| Old ids from inherited scripts are silent | 2022 privacy change; third-party audio | Replace with owned or Roblox-published audio |
| New-API sound is silent | No wire to an `AudioDeviceOutput`; no listener (`DefaultListenerLocation` Default or None); interaction groups differ; wrong pin name | Check `Wire.Connected`; create and wire a listener; match groups |
| Hits feel late or floaty with good assets | Lead-in in the file; sound started on the beat instead of beat minus peak; first-use loading | Trim onset; schedule by peak; preload on equip |
| First hit of a session is silent or late | Sound not loaded | Register and load when the owner loads |
| Machine-gun repetition | One take, no variation | Shuffle bag of 3 or more, pitch and volume jitter, layer recombination |
| Metallic phasing in group fights | The same file stacked | Voice caps, per-cue cooldown, choke |
| Distant fights audible everywhere; constant murmur in hubs | Default 10 to 10,000 stud rolloff; no crowd caps | Per-category distances; crowd caps; distance gate |
| Sound cuts off abruptly at range | Inverse or Linear with a low maximum | `InverseTapered` or a custom curve |
| Own footsteps sound far away | Listener at a third-person camera | Play own sounds 2D |
| UI clicks louder than hits; levels jump between sounds | No loudness target | Normalise files; level by category |
| Music slider does nothing, or jingles ignore it | Sounds outside a bus; settings wired to an old system; stingers on the SFX bus | Every source on a bus; rewire; stingers on Music |
| Music unbearable after 20 minutes | One short loop at a high level | Playlist, silences, lower level |
| Hard cut between tracks; music flips at zone borders | Single player swapping assets; no hysteresis | Two decks; minimum time in state |
| Stems drift apart | Started one by one | `Play(atTime)` on mixer time |
| Everyone hears one player's boss music | Music played on the server | Client music driven by replicated state |
| Sounds memory high, or sounds fail to load on phones | Everything loaded at join; unique long files | Load per area; fewer stems; mono, trimmed files |
| Players miss danger | Audio-only cue, muted phones | Visual twin; caption or icon |
| Game went quiet after an update or a takedown | Asset moderated or claimed | Load-check job with fallbacks; replace from manifest |

## Review gate

- [ ] Audio system chosen deliberately; if both exist, every slider drives both and ducking was re-tested.
- [ ] Every asset id has a manifest row: source, licence, uploader, date, loudness, onset, peak. No commercial music; no free-entry audio ids.
- [ ] Uploads owned by the experience's owner; music ids load-checked with fallbacks; quotas planned around the stricter official number.
- [ ] Each core verb and UI action has a sound; frequent sounds have 3 or more takes, pitch and volume variation, and a cooldown.
- [ ] Files trimmed, mono for 3D, normalised to one target; transient within 10 ms; scheduled sounds start at beat minus peak.
- [ ] Buses for Music, SFX, Ambience and UI with persisted squared sliders; limiter on the master; ducking under dialogue and big moments.
- [ ] Voice caps, crowd caps, steal order and distance gates set; no default rolloff on any 3D sound; own-character sounds 2D.
- [ ] Music is client-side with two-deck crossfades, fade-in on join, silences and a context priority stack; stems start on mixer time.
- [ ] Audio loaded per area; Sounds memory checked on a 3 GB phone; first-minute preload list is short.
- [ ] Every information sound has a visual twin; gameplay never depends on acoustic simulation; mix tested on a phone speaker in a full server.

## Sources

Accessed 2026-11-10. "(read)" = opened; "(search summary)" = seen only through web search result text.

- Roblox/creator-docs at commit ccc2b01 (read): `content/en-us/audio/index.md`, `audio/assets.md`, `audio/objects.md`, `audio/effects.md`, `sound/objects.md`, `sound/groups.md`, `projects/assets/privacy.md`, `cloud/guides/usage-assets.md`, `performance-optimization/improve.md`; `reference/engine/classes/` `AudioPlayer.yaml`, `AudioEmitter.yaml`, `AudioListener.yaml`, `AudioDeviceOutput.yaml`, `AudioFader.yaml`, `AudioCompressor.yaml`, `AudioLimiter.yaml`, `Sound.yaml`, `SoundGroup.yaml`, `CompressorSoundEffect.yaml`, `SoundService.yaml`, `UserGameSettings.yaml`, `ContentProvider.yaml`. https://github.com/Roblox/creator-docs
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault, commit 43ba05d) (read): `07 Lighting VFX and Audio/` The Audio API - Players Emitters Wires and Effects; Music Licensing and Audio Upload Rules for 2026; Sound Design for Games; Spatial Audio and Mixing; Music and Adaptive Audio; `47 Game Feel and Juice/` Feedback Timing - Sound Visual and Haptic Sync; Reward Moments and Celebrations; `skills/lihfolk-sfx/SKILL.md`. Its vendor licence table was not verified.
- https://devforum.roblox.com/t/roblox-audio-api-exits-beta-enhanced-sound-controls-now-available/3153454 and https://devforum.roblox.com/t/new-audio-api-beta-elevate-sound-and-voice-in-your-experiences/2848873 (search summary; audio graph status and beta-era pitfalls)
- https://devforum.roblox.com/t/beta-acoustic-simulation/3634265 and https://devforum.roblox.com/t/full-release-acoustic-simulation-emit-audio-with-presence/4307121 (search summary; acoustic simulation status and low-end behaviour; dates not confirmed)
- https://devforum.roblox.com/t/action-needed-upcoming-changes-to-asset-privacy-for-audio/1701697 and https://devforum.roblox.com/t/update-changes-to-asset-privacy-for-audio/1715717 (search summary; 2022 audio privacy change)
- https://devforum.roblox.com/t/amplify-your-experiences-with-new-music/3164792, https://devforum.roblox.com/t/beta-introducing-the-music-top-100-chart-on-roblox/3301659 and https://en.help.roblox.com/hc/articles/360000927163 (search summary; licensed music partners and quoted terms)
- https://devforum.roblox.com/t/efficient-ways-to-handle-sounds-at-runtime/3307856, https://devforum.roblox.com/t/why-does-contentproviderpreloadasync-return-failure-on-sounds/4075555, https://devforum.roblox.com/t/memory-and-sound-instances-asset-id-question/2940244 (search summary; audio memory and preload behaviour)
- https://devforum.roblox.com/t/what-options-workflows-are-there-for-balancing-audio/705722 (search summary; no documented loudness normalisation)
- No evidence found: an official loudness target or normalisation step for uploads; a dated official statement that the legacy `Sound` classes will be removed (the docs say "discouraged"); whether legacy `Sound`s take part in acoustic simulation today.
