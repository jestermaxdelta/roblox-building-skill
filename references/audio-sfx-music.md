# Audio: API, licensing, SFX design, mixing, spatial sound, music, memory

What this is: the build-level reference for sound on Roblox: which audio system to use and how to wire it, what audio may legally be used or uploaded, how to design, time, vary and mix sound effects, spatial audio, adaptive music, UI sound sets, loudness, memory and preload on phones, and volume settings. Open it when adding sound to a new game or when a live game sounds repetitive, late, muddy, silent or too loud. It owns every audio number in the skill (`game-craft.md` §4 only points here) and extends the audio line of `performance.md` without repeating it. Visual timing is in `vfx-and-juice.md`. Sound sources with the licence read at source, breakdowns and tools: `references/visual-library/audio-and-sound.md`.

Tags: `[official]` Roblox docs (mirror commit ccc2b01, re-checked at 7cbffff on 2026-11-11) and Roblox staff announcements, `[community]` forum practice, `[lihfolk]` adapted from LihFolk Vault V2 (CC BY 4.0; numbers from one production game are starting points), `[VS]` version-sensitive (the audio API, limits and licence terms change often), `[house]` house estimate. Terms: *SFX* = sound effect; *one-shot* = a short sound played once; *bed* = a quiet loop under everything; *bus* = a group of sounds sharing one volume control; *ducking* = lowering one bus while another plays; *onset* = time from file start to first audible energy; *peak* = time to the loudest transient; *stinger* = a short musical hit on an event; *voice* = one sound playing right now.

## Contents

Start here by level · 1. The two audio systems · 2. Wiring the audio graph · 3. Licensing: what you may use and upload · 4. Upload limits and moderation · 5. SFX design: layers, variation, timing · 6. Mixing: buses, loudness, ducking, voice limits · 7. Spatial audio and rolloff · 8. Music: playlists, adaptive layers, stingers · 9. UI sound sets · 10. Memory, preload and mobile · 11. Volume settings and accessibility · 12. Level-up table · 13. Starter sound lists by genre · 14. Making your own sounds · 15. Generic-sound tells · 16. Critique rubric · Review gate · Sources

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | (1) Use only Creator Store audio published by Roblox, or sound you made yourself. (2) Play every feedback sound on the client. (3) Give each core verb and each UI action a sound, pitch-varied ±5%. (4) Four buses with sliders: Music, SFX, Ambience, UI. (5) Set min and max distance on every 3D sound; never leave the defaults. (6) Build the first six sounds of your genre's list (§13) and the UI set (§9) | Adaptive music, acoustic simulation, sidechain compressors |
| Intermediate | Layer sounds (transient, body, tail). Three or more takes per frequent sound, drawn from a shuffle bag. Trim every file so the transient starts within 10 ms. Level every file to one loudness target before upload. Cap voices and add per-cue cooldowns. Two-deck music crossfades. Keep an asset manifest with licence and uploader. Record and edit your ten most frequent sounds yourself (§14); clear the tells table (§15) | Sample-accurate scheduling, custom attenuation curves |
| Expert | Schedule sounds so the peak lands on the hit frame. One listener per 3D category wired to its own bus. Stems started on mixer time; bar-quantised transitions. Sidechain ducking. Measure loudness in-engine. Load audio per area and verify the Sounds memory label on a phone. Score the game with the rubric (§16) each release | — |

## 1. The two audio systems `[VS]`

Roblox has two systems. The docs now say `Sound`, `SoundGroup` and `SoundEffect` "are now discouraged in favor of the more robust functionality of audio objects" `[official]`; the audio graph left beta on 10 September 2024 `[official]`.

| | Legacy | Audio graph |
|---|---|---|
| Source | `Sound` (`SoundId`, `Volume` 0–10 default 0.5, `PlaybackSpeed`, `Looped`) | `AudioPlayer` (`Asset`, `Volume` 0–10, `PlaybackSpeed` 0–20, `Looping`, `PlaybackRegion`, `LoopRegion`, `AutoLoad`, `IsReady`) |
| 2D or 3D | 3D when parented to a `BasePart` or `Attachment`, 2D anywhere else | 2D: wire the player to an `AudioDeviceOutput`. 3D: wire it to an `AudioEmitter` in the world; an `AudioListener` hears it and is wired to the output |
| Buses | `SoundGroup` (assign `Sound.SoundGroup`); nestable; `Volume` multiplier 0–10 | `AudioFader` (`Volume` 0–10); any object can feed any other through a `Wire` |
| Effects | `EqualizerSoundEffect`, `ReverbSoundEffect`, `CompressorSoundEffect` (has `SideChain`) and others, parented to a Sound or SoundGroup | `AudioEqualizer`, `AudioFilter`, `AudioCompressor` (extra `Sidechain` pin), `AudioLimiter`, `AudioReverb`, `AudioEcho`, `AudioChorus`, `AudioFlanger`, `AudioDistortion`, `AudioPitchShifter`, `AudioTremolo`, `AudioGate`; wired in line, order matters, each has `Bypass` |
| Rolloff | `RollOffMinDistance`, `RollOffMaxDistance`, `RollOffMode` | `DistanceAttenuationMode` presets with `DistanceAttenuationBounds`, or a custom curve from `SetDistanceAttenuation`; `SetAngleAttenuation` for directional sources |
| Scheduling | Frame-quantised (`task.delay`) | `Play(atTime)` and `Stop(atTime)` against `SoundService:GetMixerTime()`, sample-accurate; `Cancel(actionId)` revokes |
| Analysis | `PlaybackLoudness` | `AudioAnalyzer` (`PeakLevel`, `RmsLevel`, spectrum), `AudioPlayer:GetWaveformAsync` |
| Other | `SoundService:PlayLocalSound`, `VolumetricAudio` on parts, Doppler | Voice input (`AudioDeviceInput`), `AudioTextToSpeech`, `AudioSpeechToText`, `AudioRecorder`, `AudioChannelSplitter`/`AudioChannelMixer`, acoustic simulation (§7) |

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
- Text-to-speech `[official][VS]`: `AudioTextToSpeech` takes at most 300 characters per request, and an experience may send `1 + 6 × concurrent users` requests per minute. `AutoLocalize` is on by default and re-voices the text in each player's language (11 languages), so switch it off for names and puns. Pre-generate fixed lines as assets (`AssetService:CreateAssetAsync`, Studio beta, October 2026) to avoid the rate limit; generated assets count against the audio upload quota and are not auto-translated. House use `[house]`: accessibility read-aloud, dynamic text and placeholders; signature character voices are recorded by a person with a signed release.
- `GetMixerTime()` starts at an arbitrary value and differs between machines: use it to schedule locally, never to synchronise players `[official]`. For shared timing send `Workspace:GetServerTimeNow()` and convert on each client.

## 2. Wiring the audio graph

Two canonical graphs `[official]`: 2D is `AudioPlayer → Wire → AudioDeviceOutput`; 3D is `AudioPlayer → Wire → AudioEmitter` (parented to a part or attachment) plus `AudioListener → Wire → AudioDeviceOutput`. A `Wire` has `SourceInstance` and `TargetInstance` (pins default to `Output` and `Input`); many wires into one input mix, one output can feed many wires `[lihfolk]`; `Wire.Connected` is false when an instance is missing, a pin name is wrong or the wire would form a cycle `[official]`.

Listener: `SoundService.DefaultListenerLocation` is `Default` (a camera listener only in experiences with voice chat), `Camera`, `Character` or `None`. With `Camera` or `Character` the engine also creates the `AudioDeviceOutput` and wires it `[official]`. For real buses choose `None` and build the graph yourself: one listener per 3D category, separated by `AudioInteractionGroup` (listeners hear only the emitters that share their group), each wired to its category fader `[lihfolk]`.

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
- One effect can serve many sources: a single `AudioReverb` per room, fed by every sound in that room `[lihfolk]`. Audio processing is off on the server, so `AudioAnalyzer` reads zero there: poll it on the client `[official]`.

## 3. Licensing: what you may use and upload

Audio is the asset type most likely to be removed after launch, and a removed sound fails silently. Not legal advice.

| Source | Risk | Rule |
|---|---|---|
| Creator Store audio published by Roblox and its partners ("Licensed Music", which includes sound effects): more than 100,000 professionally produced SFX and music tracks, free to use `[official]`; partners named in announcements include APM, Monstercat and Pro Sound Effects (2022), DistroKid (2024) and Too Lost (2026) `[official][VS]` | Lowest inside Roblox | First choice. Filter by creator. The Terms of Use (§7.1, read 2026-11-11) license it only for synchronising into a game "solely on the Services", only while Roblox offers the track, revocable at any time; no attribution required `[official][VS]`. A trailer on YouTube or TikTok is outside that licence: score it with music you own or licensed for it. A track is acquired into the inventory of the user who inserts it; in 2024 groups could not acquire Creator Store audio, so test a group game live `[official][VS]` |
| Sound you recorded, synthesised or composed | Low | Keep project files and dated exports as proof |
| Commissioned music or SFX | Low with a contract | Written grant: perpetual, worldwide, the game and its sequels, Roblox plus trailers, ads and streams; exclusivity stated; composer does not register the track with content-ID systems or whitelists you; stems, loop points and stingers delivered `[lihfolk]` |
| Licensed third-party libraries (free or paid professional packs) | Medium | Read the licence for "video games" and for redistribution. Upload as private assets under the game's owner and never tick distribution on the Creator Store: that hands the raw sound to every creator, which library licences forbid `[lihfolk]`. Licences read at source are in the library file, §4 |
| Community uploads on the Creator Store | Medium | Roblox allows it, but the rights chain cannot be checked; prefer verified creators |
| AI-generated audio | Medium | Ideation only: shipped sound is recorded, synthesised, commissioned or licensed `[house]`. Platform rules are those of any upload, and your rights depend on the generator's terms on the day you generated `[lihfolk]` |
| Commercial songs you do not own | High | Never upload. The risk is to the uploading account, not only the game |

- **Tonight, with no sounds of your own**: Toolbox → Creator Store → Audio, search the action ("sword impact", "whoosh", "ui click"), open Advanced Filter and filter creators by username `Roblox` (the docs list creator, verification and asset-type filters) `[official]`; right-click → Copy Asset ID → paste into an `AudioPlayer`, never the inserted `Sound`. These files cannot be trimmed: skip their lead-in with `TimePosition` set to the onset you hear in Studio (or `PlaybackRegion`), and add a manifest row. Kenney's Impact Sounds, RPG Audio and Interface Sounds (CC0, library §4) are the alternative, uploaded privately under the owner. Replace first the core verb's impact transient, the sound heard most.
- Licensed Music limits in the Terms of Use (§7.1.1–7.1.6, read 2026-11-11) `[official][VS]`: at most 250 distinct licensed tracks in one game at any one time; no streaming service or music library built from it; no charging users to listen to a specific track; no way for anyone to export, extract or download it; when Roblox revokes a track you must remove it at once. A game that plays music is fine, a music player is not `[community]`.
- Third-party licences as read on each source's own page on 2026-11-11 (wording and links in `visual-library/audio-and-sound.md` §4): Kenney audio is CC0; the Sonniss GDC bundle licence (v2.0) is royalty-free with no attribution but forbids supplying the sounds as sounds and AI training; ZapSplat's free tier requires a credit to "ZapSplat"; 99Sounds does not require credit; Incompetech's free licence requires credit; OpenGameArt and itch.io are per asset. **Licence not verified** (page refused or script-rendered): Freesound, Pixabay, Mixkit, BBC Sound Effects. Ship nothing from those four until you have read the licence on the file's own page.
- Your own songs can appear on the game details page with a 15-second preview once they pass the checks in §4; eligible partner tracks show in the in-experience "What's Playing" panel `[official][VS]`.
- Player-entered audio ids (boombox, radio) are the highest-risk feature: the game becomes a player for any infringing or abusive upload. Offer a curated list of tracks you may use; if ids must be allowed, restrict to a reviewed whitelist with per-player mute, a volume cap and an "all radios off" setting. Never sell free id entry `[lihfolk]`.
- Group-owned game: upload audio to the group or grant the experience permission. A personal upload in a group game works in Studio and is silent live `[lihfolk]`.
- On 22 March 2022 every existing audio asset longer than 6 seconds became private and all new uploads became private by default `[official]`; old third-party ids in inherited scripts are usually silent. Replace them.
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
| Versioning | From 17 February 2027 (earliest target date) an audio asset can publish new versions under one id; `rbxassetid://id&version=n` pins one, an unpinned id loads a frozen version, and `AssetService:GetLatestVersionUriAsync()` returns the newest (announced November 2026) | `[official][VS]` |
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
- When in doubt err late, never early. Hit-stop: fire the impact sound as the freeze begins and never pause it.
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
	local players: { AudioPlayer } = {}
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

This section owns the mix numbers for the whole skill. Bus tree: Master → Music, SFX, Ambience, UI (Voice if used), wired in §2; sliders are squared (§11).

**Loudness consistency.**
- Normalise every source file to one target before upload, so the per-cue `volume` value is the whole mix and swapping a take never changes the balance. One-shots: −18 LUFS momentary maximum (integrated loudness is unreliable on files under about half a second) with a −1 dBTP true-peak limit `[lihfolk]`.
- Set one-shot levels by peak and bed levels by RMS: a short sound is judged by its peak, a long one by its average energy `[lihfolk]`.
- Shape of a mix `[lihfolk]`: your own actions loudest, enemies below, other players' actions about 0.7×, UI far below combat, music and ambience a bed. After levelling, the loudest sound in the game is something the player caused and wanted.
- Measure in-engine with `AudioPlayer:GetWaveformAsync` or an `AudioAnalyzer` (`RmsLevel`, `PeakLevel`) when files cannot be re-exported `[official]`.
- Per-file editing (trim, fades, high-pass, mono, normalise, export, measure, manifest) is the numbered procedure in §14.
- Phones: no enforced mobile loudness standard was found. What is documented is that mobile mixes need a narrower loudness range than console mixes, because quiet content is lost in transit noise and small speakers distort `[community: Audiokinetic via Designing Sound]`. Compress the gap between your quietest bed and loudest hit before raising the overall level.
- Reject at source: clipped peaks, baked room reverb on positional sounds, a single take for a frequent sound, mismatched takes in one bag `[lihfolk]`.

**Ducking.** Lower Music and Ambience 3–6 dB under heavy hits and stingers with a 250–500 ms release `[lihfolk]`, and 6–12 dB under dialogue `[house]`. Three ways: a sidechain compressor on the bus (`CompressorSoundEffect.SideChain` in the legacy system `[official]`, the `Sidechain` pin in the graph); a scripted tween of the bus volume, which is easier to tune; or both. `AudioCompressor` starting values from one combat game `[lihfolk]`: `Threshold = -30`, `Ratio = 4`, `Attack = 0.01`, `Release = 0.35`; documented ranges are −60 to 0 dB, 1 to 50, 0.0001 to 0.5 s and 0.01 to 5 s `[official]`. Conflict: the LihFolk SFX skill says legacy sounds cannot sidechain; the docs show a legacy ducking mix tree, so the docs win.

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

Defaults are wrong for games: a legacy `Sound` rolls off from 10 to 10,000 studs `[lihfolk]`, and an `AudioEmitter` defaults to an inverse-square curve with preset bounds of 4 to 10,000 `[official]`, so every explosion is faintly audible map-wide and every footstep joins a murmur. `Inverse` follows min ÷ distance and does not taper toward the maximum, so a low maximum ends in an audible cut; `Linear`, `LinearSquare` and `InverseTapered` fade to zero at the maximum `[official]`.

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
- **Acoustic simulation** `[official][VS]`: `SoundService.AcousticSimulationEnabled` (off by default) gives audio-graph emitters occlusion, diffraction and reverberation (client beta January 2026, out of beta 22 September 2026; legacy `Sound` support is promised, not shipped). Per-object switches: `AcousticSimulationEnabled` on each emitter and listener (on by default), `BasePart.AudioCanCollide` (on by default except in the default character), `PhysicalProperties.AcousticAbsorption` (how little a material reflects) and density (how much it muffles). Default character sounds join in only with `CharacterSoundsUseNewApi`. Accuracy follows the rendering quality level and may drop or switch off to hold frame rate. Consequences: never make gameplay depend on occlusion (some players would hear through walls); use it for stealth and horror, test busy arenas for mud and CPU, and keep a non-simulated mix that still works.
- **Large sources**: legacy `SoundService.VolumetricAudio` makes a `Sound` fill the inside of its parent, but only when the parent is a `Part`, not a MeshPart or Attachment `[official]`, so it never applies to Blender-authored geometry. Use a 2D bed that crossfades by zone (rain, crowds) in either system.
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
| Vertical layering (stems) | One piece split into synchronised stems; intensity fades stems in and out over 0.5–1.5 s | Start all stems with `Play(atTime)` at `GetMixerTime() + 0.1`; sequential `Play()` calls drift `[official]` `[lihfolk]`. Smooth the intensity value over a few seconds and give it separate up and down thresholds so the music does not flicker `[lihfolk]` |
| Horizontal resequencing | Segments switched at bar or phrase boundaries | Next boundary = `start + ceil((now − start) / barLength) × barLength` on mixer time, with `barLength = 240 / BPM` in 4/4; schedule `Play(atTime)` and `Stop(atTime)`; `Cancel` if the state flips back |
| Stingers | Short musical hits: level up, rare drop, boss appears, victory | Louder than the bed, duck the music for their length, quantise to the next beat only when the pulse is strong (a late stinger is worse than an off-beat one). Route them through the Music bus or muted players still hear jingles `[lihfolk]` |

Adaptive music is expensive to compose and costs memory (four stems across five states is twenty long assets). A small game gets most of the value from context switching, stingers and good silence `[lihfolk]`. Loops must be cut on a bar line with matched tails; a click at the loop point is the file. `LoopRegion` loops a section after an intro `[official]`.

## 9. UI sound sets

Spec for one set (`[house]` unless tagged):

| Property | Value |
|---|---|
| Size | 10–14 sounds, all made from one palette (one synth patch, or one object recorded several ways) so they read as a family `[lihfolk]` |
| Length | Ticks and presses 30–150 ms; open, close, confirm up to 300 ms; purchase and reward up to 600 ms. No reverb tails |
| Pitch language | Positive rises or steps up, negative falls and is softer, neutral stays flat. Pairs (open/close, toggle on/off) are the same sound up and down |
| Spectrum | Energy between about 500 Hz and 5 kHz: a phone speaker plays little below 300 Hz, and loud content around 3 kHz tires the ear |
| Level | Files peak-normalised alike, then mixed well below the core verb's sound; the loudest UI sound is the purchase or reward |
| Routing | 2D, on the UI bus, client only: never a remote to play a click |
| Build order | Design the confirm first, then derive the rest by pitching, shortening and filtering it |

| Event | Sound |
|---|---|
| Hover | Soft tick; none on touch devices; throttled so dragging across 40 buttons is not 40 ticks |
| Press | Pop click |
| Panel open, close | Short rise, short fall or air whoosh |
| Tab, page, toggle, slider step | Soft tick; toggles as an up and down pair |
| Confirm, claim | Bright note; a rising run for big rewards |
| Purchase | A distinct "paid" cue, used nowhere else |
| Error, locked, cannot afford | Short low note, never harsh |
| Notification, toast | Two-note motif, quieter than confirm, at most one per second |
| Counter count-up | A tick that rises in pitch, capped at about 15 per second |

Rarity ladder for rewards: each tier adds a layer (brighter sound, a riser before the reveal, a music sting at the top) rather than volume, and the riser peaks on the reveal frame `[lihfolk]`.

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
- Phone speakers reproduce little bass: a sound that only works on headphones does not work. On a phone speaker, confirm that combat cues still cut through the loudest music state `[lihfolk]`.
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
| Metallic phasing in group fights | The same file stacked | Voice caps, per-cue cooldown, choke |
| Distant fights audible everywhere; constant murmur in hubs | Default 10 to 10,000 stud rolloff; no crowd caps | Per-category distances; crowd caps; distance gate |
| Sound cuts off abruptly at range | `Inverse` mode with a low maximum | `InverseTapered` or a custom curve |
| The player's own footsteps seem distant | The listener sits at a third-person camera | Play the player's own sounds in 2D |
| UI clicks louder than hits; levels jump between sounds | No loudness target | Normalise files; level by category |
| Music slider does nothing, or jingles ignore it | Sounds outside a bus; settings wired to an old system; stingers on the SFX bus | Every source on a bus; rewire; stingers on Music |
| Music unbearable after 20 minutes | One short loop at a high level | Playlist, silences, lower level |
| Hard cut between tracks; music flips at zone borders | Single player swapping assets; no hysteresis | Two decks; minimum time in state |
| Stems drift apart | Started one by one | `Play(atTime)` on mixer time |
| Everyone hears one player's boss music | Music played on the server | Client music driven by replicated state |
| Sounds memory high, or sounds fail to load on phones | Everything loaded at join; unique long files | Load per area; fewer stems; mono, trimmed files |
| Players miss danger | Audio-only cue, muted phones | Visual twin; caption or icon |
| Game went quiet after an update or a takedown | Asset moderated or claimed | Load-check job with fallbacks; replace from manifest |

## 13. Starter sound lists by genre

Build in this order and stop when the budget runs out: a game with the first six of its list sounds finished; a game missing the first two feels broken `[house]`. Every list assumes the UI set of §9.

| Genre | In priority order | Trap |
|---|---|---|
| Simulator, incremental | 1 the core verb (hit, mine, collect): 4–6 takes, pitch climbing with the combo. 2 Currency gain tick and count-up. 3 Sell or cash-in (the "cha-ching" the docs use as their example of feedback `[official]`). 4 UI set. 5 Egg or crate open: riser, reveal, rarity ladder. 6 Level-up and rebirth stinger. 7 Upgrade bought, zone unlocked. 8 Pet or helper chirps on a cooldown. 9 Playlist of 2–3 tracks with silences. 10 One ambience bed per zone | The collect sound plays thousands of times a session: make it the shortest, softest and most varied sound in the game, and cap its voices |
| Obby, platformer | 1 Jump and land. 2 Checkpoint reached: bright and unique. 3 Fail and respawn: under 0.5 s, soft, never mocking. 4 Hazard loops (lava, saw, laser) positional with tight rolloff, because they are information. 5 Timing ticks on timed and moving platforms. 6 Collectable. 7 Stage-complete stinger. 8 UI set. 9 Upbeat playlist at a low level. 10 Footsteps by material | The fail sound is heard two hundred times: test it after 50 repeats (§5) |
| Horror | 1 Ambience bed per area (room tone, never digital silence). 2 Footsteps by surface, the player's and others'. 3 The threat's signature at three ranges: distant, near, chase, always the same so it can be learned. 4 Doors, switches, pickups. 5 Heartbeat or breath driven by proximity or stamina. 6 Subtle one-shots on random 20–90 s timers: creaks, pipes, light hum, insects, wind `[community]`. 7 Chase music layer. 8 Stingers, rationed to the few moments that earn them. 9 Sparse, diegetic UI sounds. 10 Caught or death | Constant loud stingers stop frightening and breach the comfort rules of §11; most phone players are muted, so every scare needs a visual twin |

## 14. Making your own sounds: record, edit, export

Free tools are enough: Audacity, or any editor in `visual-library/audio-and-sound.md` §5. Values are `[house]` starting points unless tagged.

1. **Record.** Quiet, soft-furnished room; phone or USB microphone 10–30 cm from the source; 48 kHz, mono; peaks between −12 and −6 dBFS and never at 0. Record 5–10 takes of each sound and 10 s of room tone.
2. **Trim.** Zoom in and cut so the sound begins within 5–10 ms of the file start; end the file where the tail sinks into the noise (about −60 dB).
3. **Fade.** 1–2 ms in (removes the click), 10–50 ms out.
4. **Clean.** High-pass at 30–40 Hz (80–100 Hz for small UI sounds). Light noise reduction with the room tone as the profile, 12 dB at most: more sounds watery.
5. **Level.** One-shots: Normalize to a −1 dB peak, then match by ear against one reference sound of the same category. Loops, beds and music: Loudness Normalization, perceived loudness, −18 LUFS (Audacity's default is −23) `[official: Audacity manual]`. Turn on Show Clipping and fix anything it marks.
6. **Loops.** Cut at zero crossings, crossfade the join, and export WAV, FLAC or OGG: an MP3 encoder pads the file with silence, which leaves a gap at the loop point.
7. **Export.** Mono for anything positional; stereo only for music, beds and UI. Upload the best master that fits (WAV 16-bit or FLAC under 20 MB), because Studio transcodes on import `[official]` and a pre-compressed file is compressed twice; otherwise OGG at quality 6–8. At most 48 kHz `[official]`. Name files `category_object_action_01`.
8. **Batch** (intermediate, unexecuted): `ffmpeg -i in.wav -af "highpass=f=40,loudnorm=I=-18:TP=-1:LRA=7" -ar 48000 -ac 1 out.ogg` for beds and music `[official: FFmpeg loudnorm]`; keep peak normalisation for one-shots under half a second (§6).
9. **Upload** under the game's owner, wait for moderation, measure onset and peak, add the manifest row (§3).

No microphone: synthesise blips, coins and jumps in ChipTone (output stated as CC0) or jsfxr (its page lists unrestricted commercial use), then layer and filter them into the palette (§5). A recording of a real object nearly always sounds less stock than a preset.

## 15. Generic-sound tells and fixes

Timing, level, rolloff and music-fatigue symptoms are in §12; these are the ones that make a game sound like every other, or broken.

| Tell | Cause | Fix |
|---|---|---|
| Stock character sounds: the default footstep, jump, fall and death on every avatar | Roblox's default character sound script left as shipped | Fork the default `RbxCharacterSounds` script, or swap the sound instances under the `HumanoidRootPart` from a character script; check `SoundService.CharacterSoundsUseNewApi` first (§1). An August 2026 bug report says a fork can be overridden: verify in a live server `[community][VS]` |
| The same click, coin and level-up jingle heard in a hundred games | First page of Toolbox search, or the most-downloaded free pack used raw | Search deeper or by partner library; re-pitch, layer and filter stock into your palette (§5); make the ten most frequent sounds yourself (§14) |
| Crackle or distortion at busy moments | Files normalised to 0 dBFS, `Volume` above 1, stacked voices summing past full scale | −1 dB file peaks, per-cue volume at or under 1, voice caps, limiter on the master (§2, §6) |
| The same sample over and over | One take, no variation | Shuffle bag of 3 or more takes, pitch and volume jitter, layer recombination (§5) |
| Sounds from different worlds: a dry click, a cavernous chime, an 8-bit coin in an orchestral game | Packs mixed without a palette | One palette statement (era, material, wet or dry); one shared reverb or none; replace the odd ones out |
| Click or gap each time a loop repeats | Loop cut off a zero crossing, or an MP3 loop | §14 step 6; `LoopRegion` for an intro plus loop |
| Hiss, hum or a chopped tail | Raw recording, no fades, reverb tail trimmed short | §14 steps 2–4 |
| Meme and nostalgia sounds re-uploaded from elsewhere | Assumed to be free because they are everywhere | They are someone's property: use only what §3 allows |
| Silent menus and a silent world between events | No UI set, no bed | §9 set; one bed per zone (§8) |

## 16. Critique rubric

Score each line 0, 1 or 2 on a phone speaker, then on earbuds. Ship at 14 of 18 or more, with no zero and a 2 on Rights `[house]`.

| Check | 2 means |
|---|---|
| Coverage | Every core verb, reward and UI action answers with a sound on the frame it happens |
| Identity | One palette; nothing recognisable as stock; the game could be named from ten seconds of audio |
| Variation | No frequent sound repeats identically twice in a row; still pleasant after 50 repeats |
| Timing | Impacts fuse with the picture (0–30 ms late); nothing leads; first use is not late |
| Mix | The loudest thing is the player's own action; UI under combat; music a bed; no clipping; readable on a phone speaker in a full server |
| Space | Every 3D sound has deliberate distances; own-character sounds are 2D; no map-wide murmur |
| Music | Fades in on join, changes with context, leaves silences, ducks under dialogue and big moments |
| Information and access | Each warning sound has a visual twin; sliders for every bus persist; comfort limits met |
| Rights and hygiene | Every id has a manifest row with a licence you read; uploads owned by the game's owner; files trimmed, levelled, mono where positional |

## Review gate

- [ ] Audio system chosen deliberately; if both exist, every slider drives both and ducking was re-tested.
- [ ] Every asset id has a manifest row: source, licence, uploader, date, loudness, onset, peak. No commercial music; no free-entry audio ids; no third-party sound whose licence page was not read.
- [ ] Uploads owned by the experience's owner; music ids load-checked with fallbacks; quotas planned around the stricter official number.
- [ ] Each core verb and UI action has a sound; the first six of the genre's starter list (§13) and the UI set (§9) exist; frequent sounds have 3 or more takes, pitch and volume variation, and a cooldown.
- [ ] No row of the tells table (§15) applies; the rubric (§16) scores 14 of 18 or more with no zero and a 2 on Rights.
- [ ] Files trimmed, mono for 3D, normalised to one target; transient within 10 ms; scheduled sounds start at beat minus peak.
- [ ] Buses for Music, SFX, Ambience and UI with persisted squared sliders; limiter on the master; ducking under dialogue and big moments.
- [ ] Voice caps, crowd caps, steal order and distance gates set; no default rolloff on any 3D sound; own-character sounds 2D.
- [ ] Music is client-side with two-deck crossfades, fade-in on join, silences and a context priority stack; stems start on mixer time.
- [ ] Audio loaded per area; Sounds memory checked on a 3 GB phone; first-minute preload list is short.
- [ ] Every information sound has a visual twin; gameplay never depends on acoustic simulation; mix tested on a phone speaker in a full server.

## Sources

Accessed 2026-11-10; docs mirror (commit 7cbffff), DevForum, the Terms of Use and licence pages re-read at source 2026-11-11. "(read)" = opened and read. Per-reference evidence, licence wording and the diagrams that were viewed: `visual-library/audio-and-sound.md`.

- Roblox/creator-docs at commit 7cbffff (read): `content/en-us/audio/index.md`, `audio/assets.md`, `audio/objects.md`, `audio/effects.md`, `sound/objects.md`, `sound/groups.md`, `projects/assets/privacy.md`, `cloud/guides/usage-assets.md`, `performance-optimization/improve.md`; `reference/engine/classes/` `AudioPlayer.yaml`, `AudioEmitter.yaml`, `AudioListener.yaml`, `AudioDeviceOutput.yaml`, `AudioFader.yaml`, `AudioCompressor.yaml`, `AudioLimiter.yaml`, `Sound.yaml`, `SoundGroup.yaml`, `CompressorSoundEffect.yaml`, `SoundService.yaml`, `UserGameSettings.yaml`, `ContentProvider.yaml`, `Wire.yaml`, `AudioAnalyzer.yaml`, `AudioTextToSpeech.yaml`; `reference/engine/enums/` `RollOffMode.yaml`, `DistanceAttenuationMode.yaml`, `ListenerLocation.yaml`. https://github.com/Roblox/creator-docs
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault, commit 43ba05d) (read): `07 Lighting VFX and Audio/` The Audio API - Players Emitters Wires and Effects; Music Licensing and Audio Upload Rules for 2026; Sound Design for Games; Spatial Audio and Mixing; Music and Adaptive Audio; Combat Sound Design and Feedback (sidechain values); `47 Game Feel and Juice/` Feedback Timing - Sound Visual and Haptic Sync; Reward Moments and Celebrations; `skills/lihfolk-sfx/SKILL.md`. Its vendor licence table was not verified.
- Roblox announcements on DevForum (read): Audio API exits beta https://devforum.roblox.com/t/3153454; Acoustic Simulation full release https://devforum.roblox.com/t/4307121; Text-to-Speech full release https://devforum.roblox.com/t/3986607, automatic translation https://devforum.roblox.com/t/4922029, asset creation https://devforum.roblox.com/t/4950480; music on the game details page and Too Lost https://devforum.roblox.com/t/4760221; DistroKid catalogue and What's Playing https://devforum.roblox.com/t/3164792; asset versioning https://devforum.roblox.com/t/4977769; audio API beta https://devforum.roblox.com/t/2848873; acoustic simulation Studio beta https://devforum.roblox.com/t/3634265; 2022 audio privacy change https://devforum.roblox.com/t/1701697 and https://devforum.roblox.com/t/1715717.
- Roblox Terms of Use, section 7 "Music on Roblox" (read through the help-centre API, article 115004647846, last edited 2026-11-01; the HTML page itself returns 403) https://en.help.roblox.com/hc/en-us/articles/115004647846
- Community threads (read): how developers read the Licensed Music terms https://devforum.roblox.com/t/2531183 and https://devforum.roblox.com/t/3305661; APM search method https://devforum.roblox.com/t/2149632; audio API wiring deep dive https://devforum.roblox.com/t/3156011; soundtrack craft https://devforum.roblox.com/t/1741250; horror audio list https://devforum.roblox.com/t/2212571.
- External (read): Designing Sound, "Different Loudness Ranges for Console and Mobile Games" https://designingsound.org/2013/02/20/different-loudness-ranges-for-console-and-mobile-games; Audacity manual, Loudness Normalization https://manual.audacityteam.org/man/loudness_normalization.html; FFmpeg filters, `loudnorm` https://ffmpeg.org/ffmpeg-filters.html. Licence pages: see the library file. Not readable from here: freesound.org and pixabay.com (403), mixkit.co and the BBC archive (licence text script-rendered).
- https://devforum.roblox.com/t/efficient-ways-to-handle-sounds-at-runtime/3307856, https://devforum.roblox.com/t/why-does-contentproviderpreloadasync-return-failure-on-sounds/4075555, https://devforum.roblox.com/t/memory-and-sound-instances-asset-id-question/2940244 (read; audio memory and preload behaviour, one or two posters each)
- https://devforum.roblox.com/t/what-options-workflows-are-there-for-balancing-audio/705722 (read; no documented loudness normalisation)
- No evidence found: an official loudness target or normalisation step for uploads; an enforced loudness standard for mobile games; a dated official statement that the legacy `Sound` classes will be removed (the docs say "discouraged"). UI-set numbers in §9, the genre lists in §13, the recording values in §14 and the rubric threshold are `[house]` estimates.
