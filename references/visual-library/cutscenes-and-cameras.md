# Cutscenes and cameras reference library

What this is: 71 checked references for in-game cutscenes, cinematic camera work and trailer capture on Roblox: official tools, camera tutorials, open-source modules with licence and last-commit date, authoring plugins, shipped trailers to study, cinematography basics that transfer to a game camera, and viewed stills of horror and boss-intro framing. The rules these references support live in `references/cutscenes-and-cinematics.md` (shot table in §4, comfort limits in §5, scripts in §14, tells in §17, rubric in §18).

How to use this file:
- Pick the sub-aspect you are working on, open two or three rows, and write down what you will copy as a number or a decision (shot size, FOV, seconds, easing, where the skip sits) before keying anything.
- Evidence: `viewed` = the image was downloaded and looked at (for GIFs, the first frame); `read` = the page, thread or source file was read; `video, not watched; verified to exist (oEmbed)` = YouTube confirmed the title and creator, nobody here watched it, and the note says what to study, not what was seen; `search` = seen only in search results, not opened. Need something to look at now: §9 and §10 hold viewed stills, including frames from two of the §6 videos.
- These are references to study, not assets to copy: every third-party image, clip, plugin and module stays its owner's. Module rows state the licence and last commit read on 2026-11-11, or say "licence not verified". Code modules are not 3D assets, so house rule 1 does not forbid them; any model, rig or prop that ships with one is not for release.

Image host prefix: `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads`. Thread links are `https://devforum.roblox.com/t/<id>`.

## 1. Official tools, docs and 2025–2026 features

Start here: rows 1, 2 and 7.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Customize the camera](https://create.roblox.com/docs/workspace/camera), Roblox docs | tutorial | `CameraType.Scriptable` hands you the camera; `Camera.Focus` must then be set every frame because lighting detail follows it; FOV range 1–120, default 70 | read |
| 2 | [Free camera mode](https://create.roblox.com/docs/workspace/camera/free-camera), Roblox docs, 2026 | tool | Full control table (move, elevation, roll with Z and C, FOV on the wheel) and the config menu; speed and stiffness are separate settings, and low stiffness is the eased look | read |
| 3 | [Enhanced Freecam Capabilities](https://devforum.roblox.com/t/4848482), Roblox staff, 2026-09 | breakdown | Where it works (Studio playtest; live client for owner and editors), the Input Action System opt-in, player lock, UI toggles, custom post menu | read |
| 4 | Freecam showcase frame, same post: `DF/original/5X/c/2/8/0/c280161bab54e7fae5f99b9e3f8ed174c2da3240.gif` | image | Establishing shot done right: small lit house low in frame, storm vortex filling the upper two thirds, one warm window as the focal point against a cold dark value range | viewed |
| 5 | Freecam config frames, same post: `DF/original/5X/c/f/2/7/cf27f44983c2c25ea773b5f8dcc05f1aee7bb59a.gif` (UI visibility), `DF/original/5X/d/1/c/a/d1caa4c13e898bab1edb476d63a538dbf640ce55.gif` (post-processing) | image | First: one-point perspective down a walkway to a statue, symmetry for a "monument" beat, with Screen GUIs and Leaderboard as separate off switches. Second: rim-lit hero prop against a large dim backdrop, and the six effects freecam can layer (depth of field, bloom, blur, colour correction, sun rays, colour grading) | viewed |
| 6 | [Event Sequencer](https://create.roblox.com/docs/resources/modules/event-sequencer), Roblox docs | repo | A seekable scene timeline with `audio`, `animate`, `tween`, `interval`, `schedule` configurations; `SyncToAudio`; a `Skippable` flag that decides whether a missed event still fires on late join; inline mode for existing places | read |
| 7 | [The Mystery of Duvall Drive: EventManager](https://create.roblox.com/docs/resources/the-mystery-of-duvall-drive/foundational-gameplay-systems), Roblox docs | breakdown | A hand-typed keyframe table per event (interpolants, scripts, audio, camera shakes) and the Warmup, InFlight, Cooldown scenes that hide a teleport and proceed on timeout | read |
| 8 | [Roblox presents Twenty One Pilots Concert Experience](https://www.youtube.com/watch?v=0fAhhoXK12o), Roblox, 2021 | video | The event the EventSequencer docs cite as built on that framework: study scene changes timed to music | video, not watched; verified to exist (oEmbed) |
| 9 | [Thumbnails: videos](https://create.roblox.com/docs/production/publishing/thumbnails), Roblox docs | tutorial | The exact allowed and rejected lists for game-page video; "camera work" with cinematic angles is on the allowed side when it shows real gameplay | read |
| 10 | [Gameplay Videos on Home](https://devforum.roblox.com/t/4842601), Roblox staff, 2026-08 | breakdown | Staff wording to keep cinematic trailers out of the gameplay-video slot; two named games and their Recommended For You lifts | read |
| 11 | [Tips for Capturing High Quality Screenshots and Videos in Studio](https://devforum.roblox.com/t/2723897), Roblox staff, 2024; image `https://devforum.roblox.com/secure-uploads/uploads/optimized/5X/a/0/5/b/a05b10eee87d04c32869997ccc1066cf2b02ddef_2_686x500.jpeg` | tutorial | OBS settings (CBR 20,000 kbps or more, MP4, 60 FPS, 4K canvas), device-emulator resolutions, file naming by shot. The image is a low, centred establishing shot inside a tablet outline: check composition at 4:3 before calling a shot done | read, viewed |
| 12 | [CaptureService](https://create.roblox.com/docs/reference/engine/classes/CaptureService), Roblox API reference | tutorial | Player-facing capture: video stops at 30 s and mutes voices; `UICaptureMode` controls UI in screenshots; upload limits per user | read |
| 13 | [Turn screenshots into teleporting paintings](https://devforum.roblox.com/t/4974220), Roblox staff, 2026-11; image `DF/optimized/5X/a/4/6/1/a461a2952e9fc19385a04a0ce695cbb09908c4de_2_668x500.jpeg` | tutorial | A complete client-only script: screenshot, gallery, `EditableImage`, then a short scripted-camera jump through the frame; the image shows a four-step progress strip at the bottom of the screen | read, viewed |
| 14 | [Animation capture](https://create.roblox.com/docs/animation/capture), Roblox docs | tutorial | Face capture from a webcam into keyframes, up to 60 s, beta: the official route to facial animation short of lip-sync | read |

## 2. Camera and cutscene tutorials (Roblox)

Start here: rows 15, 20 and 22.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 15 | [Camera Animations for cutscenes and gameplay!](https://devforum.roblox.com/t/1181691), MemzDev, 2021 (405 likes) | tutorial | Moon Animator camera track exported as a folder of per-frame CFrames; "Reference Part" makes the same camera animation play relative to a HumanoidRootPart for attack cameras | read |
| 16 | [How to Create Camera Cutscenes](https://devforum.roblox.com/t/1629318), BuilderBob25620, 2022 | tutorial | The plain `TweenService` route with camera parts, explained from object space up: the baseline every other row improves on | read |
| 17 | [Blender roblox camera cutscene](https://devforum.roblox.com/t/2847027), IceCreamPickels, 2024 | tutorial | A two-part camera rig (base part plus jointed camera part with an AnimationController) animated in Blender through copy-location and copy-rotation constraints | read |
| 18 | [How to get "AttachToPart" Moon Animator camera frames](https://devforum.roblox.com/t/3113931), JunisL0L, 2024 | tutorial | Why an `AttachToPart` camera plays wrong in game, and the fix: copy the same keys and easing onto the camera's CFrame track before export | read |
| 19 | [How to animate 2 characters like a takedown](https://devforum.roblox.com/t/1625809), MrchipsMa, 2022 (252 likes) | tutorial | Paired animation as two clips played together on two named rigs set a fixed distance apart: the basis of any two-actor scene | read |
| 20 | [How to make synced cutscenes?](https://devforum.roblox.com/t/2668540), support thread, 2023 | tutorial | Accepted answer: animation events read with `GetMarkerReachedSignal` replace guessed `wait` values; easing "None" or "Constant" on a camera key makes a hard cut | read |
| 21 | [How to Animate Cameras Like a Pro! (Moon Animator)](https://www.youtube.com/watch?v=zceidZKAKIs), WhatatoadFilms | video | Hand-keyed camera animation in Moon Animator by a machinima maker: study key spacing and easing choices | video, not watched; verified to exist (oEmbed) |
| 22 | [Guide to Making Better Horror Experiences](https://devforum.roblox.com/t/2212571), TEARAPARTJAMES, 2023 | tutorial | Jumpscare discipline: build expectation, sometimes do nothing, never force the same death scare twice; skippable cutscenes and subtitles listed as basic quality of life | read |

## 3. Open-source modules: cutscene runners, paths, shake

Start here: rows 23, 28 and 30.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 23 | [CutsceneService](https://github.com/Vaschex/CutsceneService), Vaschex; MIT; last commit 2026-04; [thread](https://devforum.roblox.com/t/718571); [setup video](https://www.youtube.com/watch?v=AyFJAU0B5V8) by Venox (video, not watched; verified to exist) | repo | Bezier path through numbered parts driven in `BindToRenderStep` at camera priority + 1; stores previous camera type and CoreGui state and restores them; queues; client-side only | read |
| 24 | [CutsceneManager 2.0](https://github.com/speedetoon/CutsceneManager), rugg3344; MIT; last commit 2026-08; [thread](https://devforum.roblox.com/t/3635714) | repo | Scenes registered by topic and category with an editor object and signals: one way to keep many cutscenes organised as modules | read |
| 25 | [Moon2Cutscene](https://devforum.roblox.com/t/3001411), Hzodx, 2024 (free model; licence not verified) | repo | Plays Moon Animator 2 save files at run time; `waitForObjects` and `canFindObjects` as a readiness check; frame-tagged tasks; built-in subtitle, vignette and fade | read |
| 26 | [CameraService](https://github.com/LugicalDev/CameraService), Lugical; MIT; last commit 2026-06; [thread](https://devforum.roblox.com/t/1988655) | repo | Named camera "views" with smoothness, offset and tilt, and a frame-rate independence release: the gameplay-camera side that a cutscene must hand back to | read |
| 27 | [Camera Manipulation Rig + Effects Module](https://devforum.roblox.com/t/1001900), ellieflopper, 2021 (256 likes); image `DF/original/5X/d/1/c/5/d1c53f7023d56970ac922e271c1cfea796e726d5.jpeg` | repo | A camera rig driven by animation clips instead of tweens, with shake and FOV helpers; the image shows Moon's `AttachToPart` key set to a `CamPart` instance. In the author's [boss cutscene thread](https://devforum.roblox.com/t/1001741) the split is stated: actors on the server, camera effects only for the player in the scene | read, viewed |
| 28 | [CRSplineModules](https://devforum.roblox.com/t/1568205), bhristt, 2021 (125 likes) | repo | Catmull-Rom spline that passes through its control points, with the derivation; the right curve when a camera must hit exact framings | read |
| 29 | [Bhristt's Bezier Curve Module](https://devforum.roblox.com/t/1510751), bhristt, 2021 (203 likes) | repo | N-degree Bezier with a derivative, so an object or camera can face along its path | read |
| 30 | [Camera Replication Focus](https://devforum.roblox.com/t/2653957), mvyasu, 2023 | repo | The streaming hole under a Scriptable camera and one fix: a server-created focus part that the client moves with the camera | read |
| 31 | [RbxCameraShaker (EZ Camera Shake)](https://github.com/Sleitnick/RbxCameraShaker), sleitnick; MIT; last commit 2019; [thread](https://devforum.roblox.com/t/98482) (971 likes) | repo | Shake as a CFrame offset multiplied on after the camera update; presets with fade-in and fade-out; old but the reference design | read |
| 32 | [GG Camera Shake](https://github.com/HysteriaBee/GG-CameraShake), niceshark11; MIT; last commit 2026-07; [thread](https://devforum.roblox.com/t/4731267) | repo | Three algorithms (kick, Perlin, bounce), direction and strength from the source position, and a strength scale for accessibility | read |

## 4. Authoring plugins

Start here: rows 33, 34 and 35.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 33 | [CineCam v3](https://devforum.roblox.com/t/4713811), Nartheos, 2026; images `DF/optimized/5X/b/6/a/5/b6a52809e086a47d82a403df7e41d6143ed04067_2_690x288.jpeg`, `DF/optimized/5X/c/2/c/d/c2cdfa0e95acf2da07f3b0efb822fa28664af4ff_2_364x500.png`, `DF/optimized/5X/2/1/e/a/21eacd6be8bc252d0682e7c7f3cb5179498a4c6c_2_690x420.jpeg` | tool | Per-key controls worth copying into your own data: duration, FOV, easing style and direction, hard cut, track-a-part, shake, event name; numbered path drawn in the viewport; Skip, Bars and Fade toggles; a "Smooth Path" switch | read, viewed |
| 34 | [Cutscene Cinematics](https://devforum.roblox.com/t/4369035), Sindious, 2026; images `DF/optimized/5X/8/9/4/a/894aa230674ea7db7872b1f1088996f8f63325e8_2_690x387.jpeg`, `DF/original/5X/6/5/1/a/651a5d3a9c30dbc50457d5213ac023944fb0a027.jpeg` | tool | The panel opens with easing style Linear selected: a default to change on every key; camera points are stored as a model with attributes | read, viewed |
| 35 | [Smooth Cutscenes](https://devforum.roblox.com/t/1893802), len_ny, 2022; image `DF/optimized/5X/4/7/5/c/475c75c970ab8f953bf7ba6800eb0efe685aa6a8_2_357x500.png` | tool | Timeline at 24 FPS with per-key interpolation (Linear, Bezier, Hermite) and spring settings for speed, damping, force and mass | read, viewed |
| 36 | [Apex Animator](https://devforum.roblox.com/t/4918289), codedtocode, 2026 (free plugin); image `DF/optimized/5X/c/8/2/7/c827caffde59bf043efd22cd2781b1d699bc7285_2_690x247.jpeg` | tool | Dope sheet with separate rows for markers, sounds and movement; the post describes scene and camera rows, screen rows for bars, fades and subtitles, and lip-sync keying (not tested) | read, viewed |

## 5. Dialogue, subtitles and letterbox

Start here: rows 37, 39 and 41.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 37 | [Dialogue Kit V2](https://devforum.roblox.com/t/3106134), artificerrr, 2024 (118 likes); image `DF/optimized/5X/6/e/4/9/6e49ee5a91de660176ce8c8e89bdd5508c693fe7_2_690x388.jpeg` | image | Layout to borrow: speaker name on its own tab above the box, square portrait at the left, text block, full-width Continue bar; the box takes about a third of the height, which is the upper limit on a phone | read, viewed |
| 38 | [MrDialogue](https://github.com/arakoDev/MrDialogue), arakoDev; MIT; last commit 2026-08; [thread](https://devforum.roblox.com/t/4884794); image `DF/original/5X/c/8/b/b/c8bbc422016fb099b431f2ed23f7ce0567c640b9.jpeg` | repo | Dialogue as a graph of line, choice, branch, action and end nodes with conditions evaluated on the server; the screenshot shows a bottom-centre box with a speaker label mid-typewriter | read, viewed |
| 39 | [Chirp](https://github.com/7frostt/chirp), TotallyNotSIMGame; MIT; last commit 2026-10; [thread](https://devforum.roblox.com/t/4909086) | repo | Typewriter built on `MaxVisibleGraphemes` so rich-text tags never show half-open; inline `<pause>`, `<speed>` and `<event>` tags | read |
| 40 | [Simple closed captions system](https://devforum.roblox.com/t/2882829), Roblox_2049, 2024 (73 likes) | repo | Caption with a lifespan and fade, optional per-character blip, inline speed and pause flags | read |
| 41 | [How to do subtitles well](https://www.gamedeveloper.com/audio/how-to-do-subtitles-well-basics-and-good-practices), Ian Hamilton, 2015 | breakdown | Numbers: 37–40 characters a line, two lines, 46 px at 1080p, 2–2.5 s per line and 3–3.5 s for under-13s, a quarter-second gap, outline or plate instead of a lone drop shadow | read |

## 6. Shipped Roblox cinematics and trailers to study

None of these were watched; each row says what to look for. Count shots, time the longest one, and note where the first real gameplay frame appears. Viewed stills, including frames from rows 42 and 44 and the DOORS and Pressure game-page images, are in §9 and §10.

Start here: row 48 (read), then rows 42 and 43.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 42 | [Roblox DOORS - All Cutscenes (2022–2026)](https://www.youtube.com/watch?v=XLdc6U9G6Q4), Plus Roblox (fan compilation); see also [All Seek Chase Scenes](https://www.youtube.com/watch?v=IgK8y-JXzLo), Crano | video | Length of each reveal and how fast control returns; guides describe the Seek reveal as a short scene that runs straight into a chase (search summary) | video, not watched; verified to exist (oEmbed) |
| 43 | [Pressure - Trailer](https://www.youtube.com/watch?v=wJWbfN-zl6o) and [Worth The Wait, Part 1 - Update Trailer](https://www.youtube.com/watch?v=b3Djv2ffx0Y), Urbanshade (developer channel) | video | A horror game's own trailers: how mood shots and gameplay shots alternate | video, not watched; verified to exist (oEmbed) |
| 44 | [Deepwoken Trailer 2024](https://www.youtube.com/watch?v=kkERJc-Qe4o), Deepwoken channel | video | Trailer pacing for a combat RPG: shot lengths and where the title lands | video, not watched; verified to exist (oEmbed) |
| 45 | [RIVALS - Official Trailer](https://www.youtube.com/watch?v=rqjR_IrJPac), Nosniy (developer channel) | video | A shooter trailer from the developer: ratio of gameplay-camera shots to free-camera shots | video, not watched; verified to exist (oEmbed) |
| 46 | [Full Release Update Trailer - Arcane Odyssey](https://www.youtube.com/watch?v=Q_Y86D2bI_Y), Arcane Odyssey Official | video | Establishing shots of a large world, then feature shots | video, not watched; verified to exist (oEmbed) |
| 47 | [TALES OF THE DARK KING, Official Quest Trailer](https://www.youtube.com/watch?v=tOgHJD-Brzk), Dress To Impress | video | Story-led trailer for a dress-up game: how a non-combat game stages characters | video, not watched; verified to exist (oEmbed) |
| 48 | [FOES, paired takedowns](https://devforum.roblox.com/t/4959534), Fel_Kot, 2026 | breakdown | Design notes for a synced finisher with its own camera in PvP: the attacker stays vulnerable during it, and the author asks whether it reads from outside | read |

## 7. Cinematography and game-camera craft

Start here: rows 49, 51 and 54.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 49 | [Shot size cheat sheet](https://s.studiobinder.com/wp-content/uploads/2019/09/Camera-Shots-Chart-of-Camera-Shot-Sizes-Diagram-Infographic-StudioBinder.png), StudioBinder ([article](https://www.studiobinder.com/blog/types-of-camera-shots-sizes-in-film/)) | image | Nested frames on one figure from full shot to extreme close-up: the crop lines (feet, mid-thigh, waist, chest, shoulders, eyes) that the guide's §4 table converts to studs | viewed |
| 50 | [Camera movement storyboard sheet](https://s.studiobinder.com/wp-content/uploads/2020/09/Ultimate-Guide-to-Camera-Movements-Storyboard-Camera-Movement-Examples.png), StudioBinder ([article](https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/)) | image | Static, pan, whip pan, tilt, push in and pull out, each as one silhouette frame with an arrow: the notation to use on your own thumbnails | viewed |
| 51 | [180-degree line break shot list](https://s.studiobinder.com/wp-content/uploads/2020/10/180-Degree-Rule-Crossing-the-Line-25th-Hour-StudioBinder-Shot-List.jpg), StudioBinder ([article](https://www.studiobinder.com/blog/what-is-the-180-degree-rule-film/)) | image | Six shots tagged "MS · HA · Static", "MCU · OTS", "CU · LA": a compact size, angle, move code for shot lists, and a scene that crosses the line on purpose | viewed |
| 52 | [Ultimate Guide to Camera Shots: Every Shot Size Explained](https://www.youtube.com/watch?v=AyML8xuKfoc) and [Ultimate Guide to Camera Movement](https://www.youtube.com/watch?v=IiyBo-qLDeM), StudioBinder | video | Film examples for every size and move named in rows 49–50 | video, not watched; verified to exist (oEmbed) |
| 53 | [Establishing Shots](https://www.youtube.com/watch?v=ACN3dw-ywAU) and [Film Blocking Tutorial](https://www.youtube.com/watch?v=9AGaECt9j4g), StudioBinder | video | How an opening shot sets place and scale; how actor positions carry meaning before any camera move | video, not watched; verified to exist (oEmbed) |
| 54 | [How to Build a Better Cutscene](https://www.gamedeveloper.com/art/how-to-build-a-better-cutscene), Adam Schnitzer (LucasArts, Pixar), 2003 | breakdown | Six failure modes, seven purposes, animatic then layout before animation, effort-saving staging, four ways to hide the pop when leaving gameplay, why cameras need ease-in and ease-out | read |
| 55 | [Better Game Design Through Cutscenes](https://www.gamedeveloper.com/design/better-game-design-through-cutscenes), Hugh Hancock, 2002 | breakdown | When gameplay beats a cutscene, why conversation scenes and info-dumps annoy, cutscene as reward, a two-minute ceiling | read |
| 56 | [50 Game Camera Mistakes](https://www.youtube.com/watch?v=C7307qRmlMI), John Nesky (Journey), GDC 2014 | video | A checklist talk for gameplay cameras: use it to audit the camera you hand back to after a scene | video, not watched; verified to exist (oEmbed) |
| 57 | [Math for Game Programmers: Juicing Your Cameras With Math](https://www.youtube.com/watch?v=tu-Qe66AvtY), Squirrel Eiserloh, GDC 2016 | video | The trauma-based shake model, smoothing and framing maths that `vfx-and-juice.md` §7 builds on | video, not watched; verified to exist (oEmbed) |
| 58 | [Animation Bootcamp: Animating Cameras for Games](https://www.youtube.com/watch?v=hP1Vz70WouE), Simon Unger, GDC 2014 | video | Applying physical camera limits and composition to game and cinematic cameras | video, not watched; verified to exist (oEmbed) |

## 8. Stills, lighting a frame and before/after

Start here: rows 59 and 60 (the only two; more stills in §9 and §10).

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 59 | [Taking high quality screenshots](https://devforum.roblox.com/t/330052), thisfall, 2019 (179 likes); images `DF/optimized/4X/3/7/5/3753d6a9ee2f5bb7aab1c98084bc6d9d8b4e9782_2_690x393.png` (before), `DF/optimized/4X/9/3/b/93ba2372991908e065f8077257db74cf95094070_2_690x387.jpeg` (after) | image | Same bedroom shot inside Studio chrome and with the viewport torn out: a single magenta practical as key, white window as second source, everything else near black; the author sets FOV 50–60 | read, viewed |
| 60 | [Building and Showcase TIPS](https://devforum.roblox.com/t/639045), AerialsAbove, 2020 (155 likes); images `DF/optimized/4X/b/1/8/b18126c5831db86f03a1764283e66540cd45f247_2_517x291.png` (before), `DF/optimized/4X/f/e/2/fe2a27af268c780fa90a17840ca1b872f313173c_2_517x291.png` (after) | image | One diorama before and after a colour-correction pass: the grade lifts saturation and separates the book from the roots; note it is a separate effect that can be removed again | read, viewed |

## 9. Horror stills: reveals, corridors, one light

Every row here was downloaded and looked at on 2026-11-11. Game-page images: fetch `https://thumbnails.roblox.com/v1/games/<universe>/thumbnails?thumbnailIds=<id>&size=768x432&format=Png` and open the `imageUrl` it returns (the CDN link expires, so the id is listed; a developer can retire an image at any time). Video frames: `https://i.ytimg.com/vi/<video>/hq1.jpg` (also `hq2`, `hq3`) are YouTube's automatic stills from early, middle and late in a video, 480×360.

Start here: rows 61, 63 and 65.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 61 | [DOORS](https://www.roblox.com/games/6516141723) game-page image, id 137066221612679 (universe 2440500124), LSPLASH | image | Reveal through a door: door 0013 ajar, black everywhere except the red room behind it, the entity only a one-eyed silhouette against that red. A frame within the frame, one saturated colour, no detail on the threat, and light spilling across the floor in front of the door. The composition for a door-slam intro | viewed |
| 62 | DOORS game-page image, id 82307083747021 (same universe) | image | Depth instead of size: through the open door a cold blue-grey room, and the entity small at the far wall, centred in a second dark doorway. The threat sits at the vanishing point, so the eye crosses the whole room to reach it: the "something at the end of the hallway" shot | viewed |
| 63 | [Apeirophobia](https://www.roblox.com/games/10277607801) game-page image, id 124448879865467 (universe 3761186887), Polaroid Studios; marked "in-game screenshot" | image | One light, one lit object: a single fluorescent tube in a black room, and the only bright shape a pale heap on the floor below it. Everything else sits near black, so the eye has exactly one place to go | viewed |
| 64 | Apeirophobia game-page image, id 13162709087 (same universe); marked "in-game screenshot" | image | Emptiness by repetition: an office floor whose ceiling panels and pillars recede to one vanishing point, with one pool of light on the floor in front. An establishing shot for a liminal level that needs no actor | viewed |
| 65 | [Devlog #1: Making a cinematic horror game](https://devforum.roblox.com/t/2646883), varenst, 2023; menu frame `DF/original/5X/b/9/c/a/b9ca50ffdfe09ef4707acdaa7b2b7483bcc958c8.png` | image | A held establishing shot used as the menu backdrop: a tunnel in one-point perspective, a single strip light just off centre, floor tiles fading to black, menu text small in the empty left third. The same frame works as the first or last shot of an intro | read, viewed |
| 66 | Frame `https://i.ytimg.com/vi/XLdc6U9G6Q4/hq1.jpg` from row 42's DOORS cutscene compilation | image | Floor 2's mine creature filling the far end of a round tunnel, the rails and ribs of the tunnel all converging on its face. The area title and HUD are still on screen: a reveal played without taking the whole screen away | viewed |

## 10. Boss-intro stills: scale, silhouette, the hero in frame

Same fetch routes as §9. Rows 67–69 are promotional renders, not in-engine frames: take the composition, not the polish.

Start here: rows 67, 68 and 70.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 67 | Apeirophobia game-page image, id 101233893707912 (universe 3761186887) | image | Scale by overlap: a giant silhouette with one glowing grin leans over a player silhouette in the foreground, on a red ground. Two silhouettes and one lit feature carry the whole threat, and the player's own shape sets the size | viewed |
| 68 | [Tower Defense Simulator](https://www.roblox.com/games/3260590327) game-page image, id 103980832174490 (universe 1176784616), Paradoxum Games | image | The boss framed by the heroes: boss centred, lit violet, seen from slightly below; two towers cut by the left and right edges of the foreground, darker than the boss. The boss is the brightest, most saturated shape; the foreground pair gives scale and fixes which side of the line the camera is on | viewed |
| 69 | [Pressure](https://www.roblox.com/games/12411473842) game-page image, id 139449456115882 (universe 4367208330), Urbanshade: Hadal Division | image | Scale by one small lit object: a huge creature silhouette against a red glow, and the only detail a small lit shape with two headlight beams at the left. For a cave or underwater boss, let the player's vehicle or lamp be the reference size | viewed |
| 70 | Frame `https://i.ytimg.com/vi/kkERJc-Qe4o/hq2.jpg` from row 44's Deepwoken trailer | image | A lair revealed by silhouette and fog: a symmetrical fortress on a rise, teal haze, two glowing lights high in the frame, no detail below the outline. An arena establishing shot that still reads at phone size | viewed |
| 71 | Frames `https://i.ytimg.com/vi/3dvK5S7aymw/hq1.jpg` and `hq2.jpg` from [The Final Act ALL CUTSCENES](https://www.youtube.com/watch?v=3dvK5S7aymw), PumpkinDrews (fan capture of Tower Defense Simulator's event cutscenes) | image | Story beats on blocky avatars: a close-up whose textured face carries the emotion (gritted teeth), then a four-character reaction shot in warm, low-key light before the threat appears. Close-ups work when the face texture is expressive. The subtitle under the close-up is about 2% of the frame height: unreadable on a phone (guide §8) | viewed |

## Sources and licences

- Roblox Creator Docs text is CC BY 4.0 (`Roblox/creator-docs`); that licence statement names the prose, not the images, so docs images are © Roblox and are linked here for study, not redistributed. Roblox staff posts and their images belong to Roblox.
- DevForum threads and attached images belong to their authors; linked for study only. Like counts are first-post likes read on 2026-11-11.
- Repositories were shallow-cloned to check the `LICENSE` file and last commit: CutsceneService, CutsceneManager, CameraService, RbxCameraShaker, GG-CameraShake, MrDialogue and chirp are MIT. Creator Store plugins and models (CineCam, Cutscene Cinematics, Smooth Cutscenes, Apex Animator, Moon2Cutscene, Dialogue Kit, the spline and Bezier modules, the captions model, Camera Replication Focus) were not installed; their licences are not verified.
- StudioBinder images and articles, Game Developer articles and all YouTube videos belong to their publishers. Videos were verified through YouTube oEmbed only; the frames in rows 66, 70 and 71 are YouTube's automatic stills, viewed, and belong to the uploaders and the games' developers.
- Game-page images (rows 61–64, 67–69) belong to each game's developer; read through the public thumbnails API on 2026-11-11 and linked for study, not redistributed.
- First pass: 45 images viewed, 22 listed. Second pass (2026-11-11, §9–§10): 75 more viewed (9 forum images, 39 game-page images from DOORS, Pressure, The Mimic, Apeirophobia and Tower Defense Simulator, 27 automatic frames from 9 videos), 12 listed. Left out: The Mimic's painted key art, lobby and logo images, HUD-heavy gameplay frames, a primitive-part horror hallway, Blender layout and diagram screenshots, marketplace banner previews, formula screenshots, logos, Studio panels with no lesson, primitive-part demos, a visual-novel frame built on a photograph, dated event posters with undesigned title text, and feedback-thread screenshots too weak to teach framing.
- Links re-checked 2026-11-11 at one request a second: all answered except the studiobinder.com article pages (403 to the checker; the s.studiobinder.com images answered), so those three article links were not re-checked; the seven repositories answered through raw.githubusercontent.com.
- Not reachable or not found: reddit.com; Wikipedia API (rate-limited); developer-written breakdowns of DOORS, Pressure or Deepwoken scenes; an official LSPLASH trailer link that could be verified by oEmbed (fan uploads only were found, so none is listed).
