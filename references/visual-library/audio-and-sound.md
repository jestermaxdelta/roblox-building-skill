# Audio and sound reference library

What this is: 47 checked references for game sound on Roblox: the audio graph and platform rules, sound-design and mix breakdowns, tutorials, sound sources with the licence that was read on the source's own page, and free tools. The rules these references support live in `references/audio-sfx-music.md`.

How to use this file:
- Start with section 4 before downloading anything: a sound enters the game only when its row (or its own licence page, read by you on the day) says you may use it in a commercial game. Record source, licence and date in the asset manifest.
- Evidence: `viewed` = the diagram or screenshot was looked at; `read` = the page or thread was read; `oembed` = the video exists with that title and creator, it was not watched, and the note comes from its title or the page that led to it; `search` = seen only in search results, not opened. "Licence not verified" means the licence page could not be read from here: read it yourself before use.
- These are references to study, not assets to copy. Nothing here is legal advice; licences change, so the page on the day you download is what counts. Accessed 2026-11-11.

Image host prefixes: `DOCS` = `https://prod.docsiteassets.roblox.com/assets/audio`, `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads`.

## 1. Roblox audio platform: API, rules, catalogue

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Audio objects](https://create.roblox.com/docs/audio/objects), Roblox docs | tutorial | `DOCS/audio-objects/3D-Audio-Diagram.png`: two separate chains, player → wire → emitter and listener → wire → output; forget the second and 3D sound is silent. `DOCS/audio-objects/DistanceAttenuation.png`: a custom curve at 1.0, 0.5 at 50 studs, 0 at 70 | read; viewed (2) |
| 2 | [Audio effects](https://create.roblox.com/docs/audio/effects), Roblox docs | tutorial | `DOCS/effects/AudioEffect-Layered.png`: three players wired into one effect, then a second effect, then the output: one reverb or compressor serves many sources | read; viewed |
| 3 | [Sound groups](https://create.roblox.com/docs/sound/groups) (legacy system), Roblox docs | tutorial | `DOCS/sound-groups/Mix-Tree.png`: a mix tree ordered by importance (High: GUI notifications, weapons; Medium: player and enemy foley; Low: 3D and 2D ambience) with compressors ducking lower tiers. The idea carries to `AudioFader` buses | read; viewed |
| 4 | [Audio assets](https://create.roblox.com/docs/audio/assets), Roblox docs | tutorial | The limits (mp3/ogg/wav/flac, under 20 MB and 7 minutes, at most 48 kHz), quotas, transcode-on-import, and the song-or-sound-effect classification | read |
| 5 | [Roblox Audio API Exits Beta](https://devforum.roblox.com/t/3153454), Roblox, 2024-09-10 | tutorial | What shipped with the release: `AudioPlayer.Volume`, `AudioFilter` (one band, selectable shape), `AudioAnalyzer.SpectrumEnabled`, the attenuation curve editor | read |
| 6 | [Acoustic Simulation full release](https://devforum.roblox.com/t/4307121), Roblox, 2026 (out of beta 2026-09-22) | tutorial | Occlusion, diffraction and reverb for audio-graph sounds only. Controls: `BasePart.AudioCanCollide`, `PhysicalProperties.AcousticAbsorption`, density. Accuracy drops or switches off with rendering quality | read |
| 7 | [Text-to-Speech API full release](https://devforum.roblox.com/t/3986607) (2025-10), [automatic translation](https://devforum.roblox.com/t/4922029) (2026-10), [asset creation in Luau](https://devforum.roblox.com/t/4950480) (2026-10), Roblox | tutorial | Limits to design around: 300 characters per request, `1 + 6 × concurrent users` requests per minute per experience; `AutoLocalize` on by default; pre-generate fixed lines as assets | read |
| 8 | [Launching Music on the Game Details Page and New Songs from Too Lost](https://devforum.roblox.com/t/4760221), Roblox, 2026-07 | tutorial | Your own uploaded songs can show on the game page with a 15-second preview if titled meaningfully and the uploader is ID-verified; Too Lost catalogue added to the Creator Store | read |
| 9 | [Amplify Your Experiences with New Music](https://devforum.roblox.com/t/3164792), Roblox, 2024–2025 | tutorial | DistroKid catalogue; "Known Limitations": the track must be acquired into the inventory of the user who inserts it, and groups cannot acquire Creator Store audio (2024 text) | read |
| 10 | [Would this be considered a "streaming service"?](https://devforum.roblox.com/t/2531183) (2023) and [Music on Roblox TOS Rule](https://devforum.roblox.com/t/3305661) (2024), DevForum | tutorial | The Terms of Use wording quoted by developers: no streaming service or music library built from Licensed Music, at most 250 distinct licensed tracks in one experience at a time. Replies read it as "a game with music, yes; a music player, no" | read |
| 11 | [How to find good music in Roblox's audio library, using the APM Music Website](https://devforum.roblox.com/t/2149632), jackjenningsdev, 2023 | tutorial | Search by mood, genre and instrument on APM's own site, then find the same track in the Creator Store; Roblox holds only some APM libraries | read |
| 12 | [Asset Versioning Is Coming to Meshes, Images, Audio, and Video](https://devforum.roblox.com/t/4977769), Roblox, 2026-11 | tutorial | From 2027-02-17 an audio asset keeps its id across versions and `rbxassetid://id&version=n` pins one: a re-mix no longer means new ids everywhere | read |
| 13 | [Roblox's New Audio API: A Somewhat Deep Dive](https://devforum.roblox.com/t/3156011), rbx_ind1g0, 2024 | tutorial | Wiring diagrams `DF/optimized/5X/3/3/0/9/33097ab737f75326642f07dbbf150be6f40ecd91_2_690x333.png` and `DF/optimized/5X/1/3/2/e/132e4fb9984ec33948956e1af4229e78dcb0f675_2_690x307.png`, plus a list of valid source → target wire pairs | read; viewed (3) |
| 14 | [AudioEngine](https://devforum.roblox.com/t/4807450), Not_Lowest, 2026 | repo | An open-source runtime where gameplay reports states and parameters and rules decide the mix (stems, ducking, voice limits). Read its design before writing your own; licence not verified, small user base | read |

## 2. Sound design and mix breakdowns (outside Roblox)

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 15 | [Overwatch: The Elusive Goal: Play by Sound](https://www.youtube.com/watch?v=zF_jcrTCMsA), Scott Lawlor and Tomas Neumann, GDC 2016 ([summary](https://www.gamedeveloper.com/audio/video-how-i-overwatch-i-was-designed-so-people-could-play-by-sound-)) | video | An importance system that re-mixes by threat, and cues that carry information (a rising pitch tells how many charges remain), per the coverage that led here | oembed |
| 16 | [The Sound and Music of Hyper Light Drifter](https://www.youtube.com/watch?v=k1b9xKRC74E), GDC talk | video | A small team's sound and score for an action game with no dialogue | oembed |
| 17 | [The 'TUNIC' Audio Talk](https://www.youtube.com/watch?v=sCIK78OHrIY), GDC talk | video | Audio for a stylised, isometric adventure: a useful scale match for Roblox scenes | oembed |
| 18 | [Signal Processing For Sound Design](https://www.youtube.com/watch?v=jVac5IFXpFo), GDC talk | video | What EQ, compression, pitch and time effects do to a sound, for people who design by ear | oembed |
| 19 | [How To Make Sounds For Video Games](https://www.youtube.com/watch?v=aucpH8LYvnE), Marshall McGee (Waveform) | video | A working designer's start-to-finish method for building a game sound from layers | oembed |
| 20 | [Designing An Explosion Sound With Only An iPhone Mic](https://www.youtube.com/watch?v=DWIrBcM_Bxo), Marshall McGee | video | Proof that a phone recording plus layering and processing is enough: the route for making your own with no budget | oembed |
| 21 | [How To Design Sounds For Horror Games](https://www.youtube.com/watch?v=TFLWaTG0NTM), Marshall McGee | video | Horror palette: quiet beds, dynamics and unease instead of constant loud stingers | oembed |
| 22 | [How To Design Sounds For Truly Chaotic Games](https://www.youtube.com/watch?v=PyojbrQ1Mfw), Marshall McGee | video | Keeping a mix readable when many sounds fire at once: the simulator and tower-defence problem | oembed |
| 23 | [How To Create Beautiful Ambient Sounds For A Game](https://www.youtube.com/watch?v=5fJZmO7NdMI), Marshall McGee | video | Building an ambience bed from loops and occasional one-shots | oembed |
| 24 | [Strike a Balance with Sound Effects](https://www.youtube.com/watch?v=qKjD5qbLUeI), Masahiro Sakurai on Creating Games | video | A director's rule set for relative levels between effect types | oembed |
| 25 | [Listen in Various Environments](https://www.youtube.com/watch?v=WUy4lTUhj80), Masahiro Sakurai on Creating Games | video | Checking a mix on different speakers and headphones before shipping: for Roblox, the phone speaker first | oembed |
| 26 | [Game Music and Ambient Sounds](https://www.youtube.com/watch?v=t_tRnBj9tqc), Masahiro Sakurai on Creating Games | video | When a scene wants music and when it wants ambience alone | oembed |
| 27 | [Adaptive Soundtracks in Games](https://www.youtube.com/watch?v=b0gvM4q2hdI), Game Maker's Toolkit | video | Examples of layered and re-sequenced music reacting to play | oembed |
| 28 | [Different Loudness Ranges for Console and Mobile Games](https://designingsound.org/2013/02/20/different-loudness-ranges-for-console-and-mobile-games), Bernard Rodrigue (Audiokinetic), 2013 | breakdown | Mobile games are played in noise and on small speakers that distort: mix them with a narrower loudness range so quiet content is still heard; a range over 20 LU is probably excessive anywhere | read |
| 29 | [Approaching UI Audio from a UI Design Perspective, parts 1 and 2](https://www.audiokinetic.com/en/blog/approaching-ui-audio-ui-design-perspective-1), Audiokinetic blog | breakdown | Treating a UI sound set as a design system (not opened: host did not resolve from here) | search |
| 30 | [How to Make Good Soundtracks and Use Music Effectively in Games](https://devforum.roblox.com/t/1741250), 6oi, 2022 | tutorial | A Roblox composer on timbre choice (the same melody on the wrong instrument does not read as a boss theme), register spacing between melody and chords, and cutting reverb tails so loops close. Its "MP3 and OGG only" note is out of date | read |
| 31 | [Guide to Making Better Horror Experiences](https://devforum.roblox.com/t/2212571), TEARAPARTJAMES, 2023 | tutorial | Audio section: a list of subtle sources to build a horror bed from (floor creaks, light hum, pipes, insects, heartbeat, breathing, wind) | read |

## 3. First-party tutorials for beginners

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 32 | [In-game sounds](https://create.roblox.com/docs/tutorials/use-case-tutorials/audio/in-game-sounds), Roblox docs | tutorial | Positional sound with distance and roll-off, then feedback sounds on a collectable: the first two things a new game needs | read (headings) |
| 33 | [Audacity manual: Loudness Normalization](https://manual.audacityteam.org/man/loudness_normalization.html) | tutorial | Two modes: perceived loudness (default −23 LUFS) and RMS (default −20 dB); keep "normalize stereo channels independently" off | read |
| 34 | [FFmpeg `loudnorm` filter](https://ffmpeg.org/ffmpeg-filters.html) | tutorial | EBU R128 normalisation from the command line: targets `I` (default −24), `LRA` (default 7) and `TP`; two-pass mode for files | read |

## 4. Sound sources and what their licences say

| # | Source | Type | Licence as read on the source's page, and what to do | Evidence |
|---|---|---|---|---|
| 35 | [Roblox Creator Store audio](https://create.roblox.com/store/audio) (Roblox, APM, Monstercat, DistroKid, Too Lost and other partners) | gallery | Free to use in Roblox experiences per the docs ("more than 100,000 professionally-produced sound effects and music tracks"). Licensed Music carries the limits in row 10. Use outside Roblox (a trailer on another platform) is not covered by anything read here | read |
| 36 | [Kenney audio packs](https://kenney.nl/assets/category:Audio) (Interface Sounds, UI Audio, Impact Sounds, RPG Audio, Casino Audio, Digital Audio, Sci-fi Sounds, Music Jingles, Voiceover packs) | gallery | CC0 (public domain): commercial use allowed, no attribution required (support page and the Interface Sounds asset page). Widely used, so re-pitch and layer to avoid the stock sound | read |
| 37 | [Sonniss GameAudioGDC bundles](https://sonniss.com/gameaudiogdc) ([licence](https://sonniss.com/gdc-bundle-license/)) | gallery | Royalty-free, commercial use, no attribution. You may not distribute the sounds as sound effects in any form, modified or not, and may not use them to train AI. Upload as private assets only | read (licence page; bundle page blocked) |
| 38 | [ZapSplat](https://www.zapsplat.com/license-type/standard-license/) | gallery | Free accounts: MP3 only, download limits, **credit to "ZapSplat" required** wherever reasonably possible. Premium: no attribution, and sounds downloaded while subscribed stay licensed. Games allowed; no redistribution outside the project | read |
| 39 | [99Sounds](https://99sounds.org/license/) | gallery | Royalty-free for personal and commercial projects; credit not required; no selling or redistributing the files on their own | read |
| 40 | [OpenGameArt](https://opengameart.org/content/faq) (audio section) | gallery | Per asset: CC0, CC BY, CC BY-SA, GPL and others. Commercial use is allowed if you follow that asset's licence; credit in the form the author asks. Avoid share-alike and GPL audio in a closed Roblox game unless you have checked what they require | read (FAQ) |
| 41 | [Incompetech](https://incompetech.com/music/royalty-free/licenses/) (Kevin MacLeod music) | gallery | Free under Creative Commons with **credit required** (paste the generated credit line); a paid standard licence removes the credit. Heard in thousands of videos: recognisable | read |
| 42 | [itch.io free sound-effect assets](https://itch.io/game-assets/free/tag-sound-effects) | gallery | Per pack: each page states its own licence, and some state none. No stated licence means no permission | read (listing) |
| 43 | [Freesound](https://freesound.org/) | gallery | Licence not verified here (site refused the request). Reported as per-file CC0, CC BY or CC BY-NC: check every file, credit CC BY files, and never use a NonCommercial file in a monetised game | search |
| 44 | [Pixabay sound effects](https://pixabay.com/sound-effects/) and [Mixkit](https://mixkit.co/free-sound-effects/) | gallery | Licence not verified (Pixabay refused the request; Mixkit shows its terms in a script-only dialog). Read the licence page yourself before use | search |
| 45 | [BBC Sound Effects](https://sound-effects.bbcrewind.co.uk/) | gallery | Not for a monetised game: reported as the RemArc licence (personal, educational and research use), with commercial licensing sold separately. Licence page not readable from here | search |

## 5. Tools for making and checking sound

| # | Tool | Type | Use it for | Evidence |
|---|---|---|---|---|
| 46 | [Audacity](https://www.audacityteam.org/) (free, open source); alternatives [ocenaudio](https://www.ocenaudio.com/), [REAPER](https://www.reaper.fm/) (60-day full evaluation, discounted licence under USD 20,000 yearly revenue), [Sonic Visualiser](https://www.sonicvisualiser.org/) (free, open-source spectrogram and analysis), [Youlean Loudness Meter](https://youlean.co/youlean-loudness-meter/) (free LUFS and true-peak meter plugin) | tool | Record, trim, fade, filter, normalise, export, and measure. The guide's §6 procedure uses only Audacity | read (home pages) |
| 47 | [jsfxr](https://sfxr.me/) (browser port of sfxr), [Bfxr](https://www.bfxr.net/) (open source), [ChipTone](https://sfbgames.itch.io/chiptone) (output stated as CC0, free for commercial use), [BeepBox](https://www.beepbox.co/) (songs belong to their authors) | tool | Synthesise retro blips, coins, jumps and short tunes that are yours. jsfxr and Bfxr output terms were not found on their pages: a sound you design from parameters is your own work, but keep a note of the settings | read (home pages) |

Learning hubs (home pages read): [Game Audio Learning](https://www.gameaudiolearning.com/) (a roadmap for newcomers) and [A Sound Effect](https://www.asoundeffect.com/) (interviews and guides; a sound-effects shop, so its libraries are paid and licensed per product).

Not recommended, with reasons: generating shipped music or effects with AI tools (two DevForum threads promote one, September 2026): rights depend on the generator's terms on the day and the house standard is authored sound; the "local file in the Studio content folder" trick ([thread](https://devforum.roblox.com/t/738185), 2020) is unsupported, breaks on Studio updates and solved an upload fee that no longer exists.

## Sources and licences

- Roblox documentation and diagrams: Roblox/creator-docs, CC BY 4.0. DevForum posts belong to their authors; announcements belong to Roblox.
- Licence rows quote or paraphrase the source's own page as fetched on 2026-11-11: kenney.nl/support, sonniss.com/gdc-bundle-license, zapsplat.com standard licence, 99sounds.org/license, opengameart.org FAQ, incompetech.com licences, sfbgames.itch.io/chiptone, beepbox.co.
- Could not be read from here: freesound.org (403), pixabay.com (403), en.help.roblox.com (403, so the Licensed Music terms are known only through developer quotes), sonniss.com bundle page (challenge page), bbcrewind licensing page and mixkit licence (script-rendered), audiokinetic.com (host not resolved), fmod.com docs (script-rendered).
- Videos were verified through YouTube oEmbed (title and channel) and not watched; years are given only where the talk's event year was confirmed by its coverage.
- Loudness: the home-console figure of about −24 LKFS (Sony guidance, later echoed by industry groups) was seen in search results only; no enforced mobile loudness standard was found.
- Images actually viewed for this file: 7 (4 Roblox docs diagrams, 3 community wiring diagrams).
