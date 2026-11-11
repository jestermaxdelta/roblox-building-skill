# Icons, thumbnails and the store page

How to make the icon, the 16:9 thumbnails, the gameplay video and the page text so they earn plays honestly and look designed, not generated. This file owns the craft; `analytics-and-discovery.md` owns the ranking signals, the experiment maths and what clickbait costs; `market-scan-2026-11.md` holds the owner's thumbnail rules 1–13, cited here as "rule N". Viewed examples are in `visual-library/icons-and-thumbnails.md`.

## Start here by level

| Level | Do first | Ignore for now |
|---|---|---|
| Beginner | 1. Read §1 and §2. 2. Shoot three 16:9 captures of the real first minute in Studio (§8 route A) with one recipe each from §3. 3. Make the icon from §5 and run the tile test. 4. Upload, activate all three, leave them 7 days | Blender renders, video, localised icons, confidence intervals |
| Intermediate | A five-slot set with five different promises (§3), a Blender hero render with an outline (§7), a brand system shared by icon and thumbnails (§6), a 20–30 s gameplay video (§9), the rubric before every upload (§15), a refresh per update (§14) | Per-language icons until one market passes 15% of plays |
| Expert | A PhotoStudio place with saved cameras, a linked-library render file that re-renders every hero after an art change, test rounds with a kept control and written hypotheses (§13), per-locale icons, Open Cloud upload, an archive of every tile with its metric window | Nothing; re-read the `[VS]` specs each quarter |

Modes: for a new game go §2 → §8 → §13 round 1 before launch. For a live game start at the Level-up table, keep the current winning thumbnail active, and change one family of things per update.

Terms: **tile** the image a player sees on Home; **qPTR** qualified play-through rate, plays that last ÷ impressions; **RFY** Recommended For You; **key / fill / rim** the main light, the shadow-softening light and the edge light behind the subject; **focal length** the Blender camera's zoom (long = narrow view, flatter faces); **wordmark** the game name drawn as a logo; **plate** a background image a character is composited onto.

Related: `lighting-and-atmosphere.md` (in-game key, fill, rim and presets) · `ui-design-figma.md` (logo, tokens, Figma export) · `blender-modeling-craft.md` (silhouette test) · `growth-and-marketing.md` §3–4 (ad creatives, short-form clips, capture rules) · `accessibility-and-player-qol.md` (contrast).

Contents: 1 Three images, three jobs · 2 The promise · 3 Composition recipes · 4 Colour and value on the Home grid · 5 Icon craft and the 150/64/32 test · 6 Text, numbers and the brand system · 7 Character renders in Blender · 8 Procedure: a thumbnail set from Studio and Blender · 9 Gameplay video · 10 Title and description · 11 Low-effort and generated tells · 12 Clickbait and policy lines · 13 Test plan · 14 Refreshes · 15 Critique rubric · Level-up table · Review gate · Sources.

## 1. Three images, three jobs `[official][VS]`

| Asset | Job | Where it shows | Spec |
|---|---|---|---|
| Icon (1:1) | Recognition: "that game again". One shape and one colour pair the player learns | Continue, Favorites, Search, Charts | Square, 512×512 or larger; shown down to 150×150; one icon per locale; auto-generated on first publish (replace it) |
| Thumbnails (16:9) | The promise: "this is what you do in the first minute". One promise per image | Home RFY tile (slot 1, or the personalised pick), the detail-page gallery, Sponsored tiles | 1920×1080; `.jpg .gif .png .tga .bmp`; other ratios are stretched, not cropped; up to 10 images or videos on the page; 2–5 active on Home, each under 3 MB; alt text per image |
| Gameplay video | Proof: "it really looks and moves like this" | First item on the detail page; autoplays inside the RFY tile | 3 uploads a month and rejections count; not shown on Xbox, PlayStation or VR; docs state no length or file-size limit |
| Title, description | Search match and the second line of the promise | Under every tile, the detail page, search | §10 |

- A custom thumbnail is required for any Home impression since 19 Oct 2026; the auto-generated image does not count. Staff wording: upload up to five "to showcase different gameplay elements".
- Home and the detail page hold separate lists. Order the detail page for a player who already clicked: video, then the image that confirms the tile, then depth (world, collection, friends).
- What covers the art: player count and rating sit under or over the bottom edge of a tile `[official]`; the mobile detail-page carousel lays a dark gradient over roughly the lower quarter (bug thread with staff reply, Oct 2026 `[community]`); the platform rounds tile corners (visible in every staff mock-up).
- Phone layout in staff mock-ups: two tiles per row; desktop four or more. The title under a tile is cut at about 23 characters in the staff's own capture. `[house]` viewed.
- Sponsored campaigns take up to 10 creatives at 16:9, split evenly. The "AI generate" button there is off-limits (house rule; `growth-and-marketing.md` §3).

## 2. The promise: show the first minute

Roblox optimises thumbnails for qualified plays, not clicks, so a tile that over-promises loses twice: bounce rises and personalisation stops showing it `[official]`. Rule 1 (show the first minute) is therefore the brief for every image.

Write the promise before opening any tool: `In the first minute you <verb> <thing> and see <result>`. One sentence per thumbnail slot; five slots, five sentences. If a sentence needs "eventually", it belongs on the detail page, not on Home.

| In the image | Keep out |
|---|---|
| Characters, props and places built for the game, posed and lit by hand | Anything not in the game; a late-game base presented as the start |
| Camera angles a player never gets (free camera, low angle, long lens) | A different art style from the game (painted, photoreal, anime) |
| The game's own effects frozen at their best frame; real UI when it is the payoff | Invented UI, rarity banners, odds or numbers no player has reached |
| Mild grade, vignette, depth of field, an outline on the hero | Paint-over that changes shapes, adds detail or adds light the engine cannot make |

`[lihfolk]` table, tightened by house rule 1: because every visible asset is authored in Blender, a render of the same source meshes is the game's art by construction. The check is one side-by-side with a raw in-game screenshot: a player must call them the same game.

## 3. Composition recipes

Pick one recipe per slot. All were seen on live tiles on 2026-11-11 (library groups B–G).

| Recipe | Layout | Promise it carries | Seen on |
|---|---|---|---|
| Hero and prize | Avatar at one third, the thing you get at the other, eye-line or arrow between them | "You get this" | Steal An Egg, Sell a Million Sushi |
| Before → after split | Hard vertical or diagonal cut; same pose both sides; small number left, big number right | The climb (rule 4) | +1 Venom Evolution "+1 / +7M", Run A Farm "$0 / $1,000,000" |
| Three-panel ladder | Three equal columns, a word or price on top, one object each, arrows between | The loop or the upgrade path | Run A Farm "HENS → EGGS → CASH!", Net a Fish "$6 / $67 / $∞" |
| Scale contrast | Tiny avatar, one huge subject cropped by the frame; ratio 1:4 or more `[lihfolk]` | Spectacle | Fisch (whale), Creatures of Sonaria |
| Threat and unaware subject | Small lit victim in front, large threat behind, one warm light | Tension without gore | 99 Nights in the Forest (campfire) |
| First-person hands | Two hands and the tool at the bottom, the target in the centre | "You do this" | 13 Days to Escape, Hypershot, My Small Business |
| Flat silhouette | One or two figures in a single flat colour on a quiet ground | Brand over detail | RIVALS (red figures) |
| Product pattern | The collectable repeated edge to edge, one break in the pattern | Abundance | Sell a Million Sushi (slot 1) |
| Framed series | A fixed frame or sign; only the scene inside changes | Variety under one brand | Brookhaven (door frame), Berry Avenue (street sign) |

Rules that hold across recipes:

- **One focal subject**, 30–45% of the frame on a thumbnail and 60–80% on an icon; at most three readable elements for mood-led genres and five for number-led ones (rule 2) `[lihfolk]`.
- **Placement**: the face or key point on a third, upper half; dead centre only for symmetrical boss shots. The subject looks or moves into the frame, toward the second element `[lihfolk]`.
- **Diagonal action**: tilt the line from weapon to target, rod to fish or avatar to prize 15–30° off horizontal; level horizons are for calm genres. Blade Ball, Fish It and Volleyball Legends are built on one diagonal each `[house]` viewed.
- **Depth in three layers**: a dark or blurred foreground edge, the lit subject, a simpler and lower-contrast background. If the background is as sharp and saturated as the hero, blur it or drop its contrast.
- **Faces**: a face reads only when it is about 8–10% of frame height or more `[lihfolk]`; choose shock, fear, joy or effort, never the default smile (rule 7). Evidence is mixed outside Roblox: one analysis of about 300,000 YouTube videos found faces perform about the same as no face on average and vary by niche (search summary). Treat "add a face" as a hypothesis for §13, not a law.
- **Safe area**: nothing essential in the bottom 20% or within 5% of a corner. An established brand can break this (DOORS puts its wordmark in the bottom fifth of one slot); a new game cannot.
- **Five slots, five promises** (rule 8): ladder, odds, versus, rare item, gag for a simulator; place, activity, friends, home, event for roleplay. Staff: near-identical thumbnails give personalisation nothing to tell apart `[official]`.

## 4. Colour and value on the Home grid

Medians from 62 icons and 171 thumbnails of Top Playing Now games, fetched 2026-11-11 and measured at 64×64 (`[house]`, small samples; saturation is mean HSV S, luminance is 0–1):

| Genre (thumbnails) | Saturation | Luminance | Reading |
|---|---|---|---|
| Simulator, +1, steal (42) | 0.54 | 0.57 | Bright sky blue or grass green behind a warm subject |
| Cozy management (22) | 0.43 | 0.55 | Lighter and softer; pink, cream, wood |
| Roleplay (18) | 0.34 | 0.62 | Brightest and least saturated: daylight renders, pastel |
| Fishing (9) | 0.52 | 0.48 | Blue field, one hot creature |
| Combat, sports (33) | 0.52 | 0.39 | Darker field, saturated effects |
| Tower defence (10) | 0.48 | 0.32 | Dark with neon accents |
| Horror (28) | 0.59 | 0.19 | Very dark with one saturated hue: red, green or violet |

- **Value first.** Convert to greyscale: the subject must sit 30–40 lightness points (of 100) from its surroundings `[lihfolk]`. Saturation cannot rescue a subject that shares its background's value.
- **Subject owns the most saturated colour**; background calmer; a complementary pair (orange on blue, magenta on green, gold on violet).
- **Speak the genre's values, change one thing** (rule 6). In the sample grid the tiles that stood out broke exactly one norm: a white manga-panel tile among dark combat tiles (Jujutsu Shenanigans), flat red on white (RIVALS), flat red and black (Pressure) `[house]` viewed.
- **Light and dark themes.** Roblox Home is near-black in dark theme and near-white in light theme. 25 of 171 thumbnails and 8 of 62 icons had an outer ring below 0.15 luminance: on dark theme their edge disappears and the tile reads as a smaller floating shape. Only 2 thumbnails had a ring above 0.80. So: keep the outer 5% between about 0.2 and 0.8 luminance, or use a lighter rim shape; a horror tile needs one lit shape that touches or nears an edge.
- **Dark tiles band.** Large near-black gradients blotch after recompression; lift blacks to about 5% and add a little grain `[lihfolk]`. Players also view at low screen brightness: keep the hero above mid-grey.
- **A row test beats theory**: paste the candidate among 12–20 current tiles of its genre at 256 px wide on both backgrounds and see where the eye lands.

## 5. Icon craft and the 150/64/32 test

What survived when the 62 chart icons were reduced (`[house]` viewed):

| Size | What still read | What was gone |
|---|---|---|
| 150 px | Everything designed for it | Thin lines, small secondary characters |
| 64 px | One subject; wordmarks of one or two heavy words (BROOKHAVEN, ADOPT ME!, DOORS, "+1") | Sentence text, numbers with commas ("$997,151,167/s"), fine illustration |
| 32 px | About 17 of 62: a single shape or face on a flat field (Murder Mystery 2 knife, 99 Nights eyes, RIVALS figure, Sell a Million Sushi, Throw Food For Animals) | Every word on every icon; every busy anime illustration (noise) |

- **The survivors share three things**: three or fewer value masses, a subject filling 60% or more, a flat or two-tone ground.
- **Text**: 35 of 62 icons had none, 22 carried the game's wordmark, 5 carried a hook ("+1", "GROW OFFLINE"). A wordmark is brand, and only worth its space once players know the name. A new game spends the icon on the subject.
- **One subject, cropped for tension**: let it break the frame; face or focal point upper-middle; nothing vital in the corners (rounded on every surface viewed).
- **No rounded corners, drop shadow or badge baked in**: the platform masks the tile. Google Play's icon spec forbids ranking and deal text or graphics on icons and applies its own corners and shadow (Android developer docs, read); a baked "UPDATE!" ribbon also goes stale the day after.
- **Colour identity**: pick the hue pair once and keep it through every refresh; change the prop, not the palette (§14).
- **Icon and thumbnails share anchors**: same hero, same two colours, same wordmark shape, so the Home tile and the Continue icon read as one game.

Tile test (executed 2026-11-11, Python 3 with Pillow). Icon at 150, 64 and 32 px on both themes; each thumbnail at 320×180, 160×90, greyscale, blurred and with the bottom 20% hidden:

Run `scripts/images/tile_test.py icon.png thumb1.png [thumb2.png ...]` (shipped with this skill; needs Pillow). It writes `tile_test.png`, one contact sheet to judge.

Pass marks: at 32 px a stranger names the subject; at 64 px they name the genre; in greyscale the subject separates; with the bottom hidden nothing is lost; in the blur the focal shape is still the first thing seen. Then look once on a real small phone.

## 6. Text, numbers and the brand system

| Use text when | Skip it when |
|---|---|
| The number is the dream: income per second, size, a multiplier (rule 3) | The image already says it |
| A real in-game label is the payoff (the game's own rarity banner, at large scale) | It would read "NEW", "UPDATE", "FREE", "OP" |
| Two or three words name an unusual verb ("CUT A ROCK!", "PACK ORDERS") | It would sit in the bottom 20% |

- Size `[lihfolk]`: cap height 8–10% of image height (about 90–110 px at 1080p), two to four words, heavy weight, outline or shadow 6–10 px in the image's darkest value. Text under about 40 px at 1080p is unreadable on a 150 px tile (vault).
- A number must be reachable and in the game's own unit (rule 3, rule 11). Abbreviate: "$93.5M/s" survives a phone tile; "$13,957,801,357" does not.
- Text is not translated. Automatic image translation (beta, 9 Nov 2026) covers in-game images only, "not icons and thumbnails" `[official][VS]`; the 2024 icon-translation experiment drew developer complaints about wrong translations `[community]`. Keep one text-free thumbnail active for every market, and upload per-locale icons only where a market earns it.
- Set type in Figma on its own layer over the exported render, with the same display font as the in-game UI (`ui-design-figma.md` tokens). Never set type in Blender `[lihfolk]`.
- **Brand system**: fix three things across the set and let the scene vary. Seen working: a fixed frame (Brookhaven), a fixed sign (Berry Avenue), a wordmark locked to one corner (Adopt Me) or always in a corner (Driving Empire, Dandy's World), one recurring flat-colour character (RIVALS). Build it once as a Figma component; each new thumbnail is a new render dropped under the same layers.
- Established games lead with a logo and mood because the name is the hook; new format games lead with colour, a number and the climb because the mechanic is the hook (vault).

## 7. Character renders in Blender

Use Blender when the tile needs a clean alpha edge, true depth of field, an outline, or the same hero at icon and thumbnail framing. Otherwise capture in Studio (§8 route A).

**Scene.** A separate `store_render.blend` that links (File > Link) the game's own collections: hero rig, the prop, one set piece. Linked data re-renders after any art change. Add the avatar stand-in: an R15 rig wearing an outfit the team owns (`animation-and-rigs.md` for the rig). The avatar is the player's, not a shipped asset; everything else in frame is the game's source (house rule 1). No downloaded models, HDRI-lit photoreal sets or generated backdrops.

**Pose** `[community][lihfolk]`:

- One line of action from foot to head, tilted toward the target. Limbs clear of the torso so the silhouette shows the action; check it as a flat black shape (`blender-modeling-craft.md` four-view test).
- Leave no limb untouched: even a standing figure bends knees and elbows. No intersecting parts; shoulders and hips stay attached.
- Exaggerate about 20% past what looks right at full size; it reads right at tile size.
- Look at the prize or the threat in action shots; at the camera only in icon portraits.
- Take the pose from the game's real animation at its extreme frame when one exists, so the tile shows a move the player will make.

**Camera.** Roblox's `FieldOfView` is vertical; Blender's focal length assumes a 36 mm sensor width. Equivalents at 16:9 (`[house]`, trigonometry):

| Roblox vertical FOV | Blender focal length | Use |
|---|---|---|
| 70° (default) | 14.5 mm | Never for a hero: wide-angle stretch |
| 40° | 28 mm | Scale shots with a huge subject |
| 30° | 38 mm | Two characters and a prop |
| 23° | 50 mm | Standard hero |
| 14° | 85 mm | Icon portrait; flattest face, simplest background |

Place the camera at chest height or lower for power, higher for cute. Depth of field: focus object on the face, f/2.8–f/4 so the background becomes a colour field.

**Three-point light.** World colour black or the scene's shadow hue; no HDRI.

| Light | Position | Power relative to key | Colour |
|---|---|---|---|
| Key (area, large) | 30–45° to the camera side, above eye level | 1 | Warm white or the scene's key colour |
| Fill (area, larger) | Opposite side, at eye level | 0.25–0.5 | The shadow hue (cool if the key is warm) |
| Rim (area or spot) | Behind and above, aimed at the camera-side edge | 1.5–2 | Complement of the background |

A large area light behind the figure "cranked up" is the single most repeated tip in the forum tutorials; two emission planes hidden from the camera on a black world are the minimal version `[community]`. Keep materials as in the game: matte clothing, no added metallic sheen (a common "GFX look" that forum critics call out and that breaks the match with the game) `[community]`.

**Engine and colour** `[lihfolk][VS]`. EEVEE for stylised art (Cycles drifts toward realism). Compare Standard and AgX view transforms against a Studio screenshot of the same asset and keep the closer one; AgX greys saturated toy colours. Film > Transparent. Render 3840×2160 and downscale, or 2048×2048 for the icon.

**Outline.** Three options, in order of cost:

1. Sticker outline in the compositor: Alpha → Dilate/Erode (Distance, +8 to +12 px at 4K) → fill white or the darkest scene colour → Alpha Over beneath the render. This is the sticker edge seen on many simulator tiles.
2. Inverted hull in 3D: Solidify modifier with flipped normals and a backface-culled dark emission material. Holds up when the outline must follow inner overlaps.
3. A rim light alone, for realistic or horror styles where a graphic line would not match the game.

**Composite** in Figma: background plate (a Studio capture, blurred 4–8 px and darkened 10–20%), contact shadow, the character render, glow only where the game has glow, text and logo last. A 10–20% vignette. Export JPG quality 90 for 3D scenes (usually under 1 MB), PNG for flat art; stay under 3 MB.

## 8. Procedure: a thumbnail set from a Studio scene and Blender

Route A is Studio only and is the default. Route B adds a Blender hero. Both end at the same checks.

1. **Write five promises** (§2) and pick a recipe for each (§3). Sketch each as three grey boxes on a 16:9 card. Run the 160×90 squint on the sketch before building anything.
2. **Open the PhotoStudio place** `[lihfolk]`: a private copy of the game with the 3–5 best sets, posable rigs, lighting presets copied from the live place, a `CaptureMode` attribute that hides every ScreenGui (`growth-and-marketing.md` §4), and a safe-area overlay (bottom 20%, corners).
3. **Stage.** Place the avatar and the hero prop on a set. Freeze a real animation at its extreme frame (Play, then `track.TimePosition = t; track:AdjustSpeed(0)`), or key one pose in the Animation Editor. Freeze effects at their peak frame.
4. **Light with the game's own tools** (`lighting-and-atmosphere.md` §2): sun as key at three-quarters, one local light behind as rim, background brighter or darker than the hero. Golden-hour clock times separate subjects best. Use no effect at a strength the live game never reaches.
5. **Camera.** Free camera: Left Shift + P in a playtest; scroll changes field of view; Z and C roll; hold Shift for slow moves `[official]`. Zoom to 20–40° FOV for heroes (table in §7). For repeatable shots set `CameraType = Scriptable` and store each CFrame and FOV in a module so the shot can be redone after an update.
6. **Capture.** Studio Settings > Rendering: Editor Quality 21, Mesh Detail Level 00; in a client test, Graphics Mode manual at maximum `[community]` (2024 tutorial). Window at 16:9, 1920×1080 or larger; wait two seconds for streaming and level of detail. Shoot three distances and two expressions per setup: that is the next test round.
7. **Honesty pass.** Recapture one frame at mid graphics quality on a phone. If the tile and that frame look like different games, tone the tile down.
8. **Route B: render the hero** (§7) with transparent film, matching the plate's camera FOV, key direction and key colour. Mismatched light direction is the first thing that makes a composite look pasted.
9. **Composite and type** in Figma on the brand component (§6). Export.
10. **Icon.** Reframe the same hero at 85 mm on a flat or two-tone ground; do not crop a thumbnail.
11. **Test sheet** (§5 script), then the rubric (§15). Fix the lowest criterion and re-export.
12. **Upload.** Thumbnails under Configurations > Places > the place > Thumbnails: Home Page tab (activate 2–5) and Experience Detail Page tab (order, alt text). Icon under the start place > Icon. Every image passes moderation before it shows `[official]`.
13. **Archive**: the layered source, the camera CFrame, the render file and a dated name (`2026-11-11_ladder_v2.jpg`), plus the metric window once it has run.

Budget: route A is about half a day for five images once the PhotoStudio place exists; route B adds about a day for the first hero and an hour for each later one `[house]` estimate.

## 9. Gameplay video `[official][VS]`

- An approved video plays inside the RFY tile: fully rolled out by the staff post of 31 Aug 2026 (the vault dates the start to 29 Jul). Two cited games gained 30% and 41% more RFY plays and 31% and 39% more RFY playtime while a video was present (test window 7–26 June 2026; Roblox calls the lifts directional).
- Allowed: real, current footage of the core loop; varied camera angles; minor brightness and contrast; curated non-linear clips; in-game UI text; the game's logo; Roblox-catalogue music without lyrics.
- Rejected: cinematic trailers and dramatised gameplay; graphics better than a player gets; real-life footage; voice-over, narration, voice chat or lyrics; promotional or subjective text ("50% off", "Free UGC!").
- Structure for a tile that autoplays muted and small: the core verb inside the first 3 seconds, no logo card first, 3–5 shots of real play, 20–30 s total as a loop `[lihfolk]`. One of the cited teams chose clips that showed the pacing change from stealth to action, which a still could not.
- The HUD stays on if it helps reading the loop; the Superstar Baseball example keeps it on. Hide other players' names (`growth-and-marketing.md` §4 capture rules).
- Spend the three monthly uploads last: cut the clip, show it off-platform or to testers, then upload. Capture settings and clip structure for social video are in `growth-and-marketing.md` §4.
- A video is also the strongest answer to distrust of polished stills: developers in the staff thread asked for more videos precisely because many front-page thumbnails no longer look like the game `[community]`.

## 10. Title and description (brief)

Search, renames, keyword rules and the 160-character hook are in `analytics-and-discovery.md` §Thumbnails and metadata and §Search. Craft points that belong with the images:

- **The name must survive the cut.** Of 98 Top Playing Now titles on 2026-11-11, 43% opened with a bracket tag, 66% carried an emoji, the median length was 22.5 characters and 36% ran past 23, the point where the staff's phone tile cuts the title `[house]`. A tag such as `[WEEK 3 🎃 x BUTCHER]` leaves almost no name. Keep a leading tag to 6 characters or fewer, or put it after the name; this refines rule 9.
- **Title says the verb, tile shows the verb.** "Cut a Rock" under a tile of a rock being cut needs no further text; a clever title under an atmospheric tile needs a subtitle in the art.
- **First description line = the tile's promise in words**, second line = this update. The player who clicked should read the same promise three times: tile, title, first line.
- **Stale tags cost trust**: 14 of 98 chart titles still carried Halloween marks on 11 November `[house]`. Put tag changes on the update checklist (rule 9).
- Never a boost, reward or code in title, tile or first line (house rule; rule 12 allows only a live, real event tag).

## 11. Low-effort and generated tells, and the fix for each

Why it matters: forum sentiment toward generated tiles is hostile (in the Oct 2026 staff thread several of the most-liked developer replies asked whether generated tiles would be excluded and called them slop; artists now label showcases "NO AI") `[community]`; Roblox's roadmap lists takedowns for games that imitate another game's title or thumbnail (late 2026) `[official][VS]`; and several tiles in the 2026-11-11 sample share one generated look, so a designed tile is now the difference cue. Chart position does not prove the art earned it, and the house rule stands regardless: nothing generated ships.

| Tell | Why it reads as cheap or generated | Fix |
|---|---|---|
| Airbrushed plastic sheen on every surface, uniform soft glow | No material decisions; the same finish on rock, cloth and skin | Game materials as built; one glossy element at most |
| Detail everywhere: every scale, gem and plank rendered equally | No hierarchy; nothing was chosen | Detail on the hero only; blur and flatten the rest |
| A photoreal or painterly object beside a blocky avatar | Style mismatch with the game itself | Render the game's own mesh (§7) |
| "Roblox-like" characters with wrong proportions, fingers or merged accessories | Not the platform avatar | A real R15 rig |
| The avatar differs between the five thumbnails | Each image made separately | One rig, one outfit, one render file |
| Garbled signage, melted small props, text that is almost a word | Classic generation artefact | Type set in Figma; props are modelled |
| Warm rim, teal fill, bokeh street behind, in every image | A default look, not this game's light | Key colour and direction taken from the game's own zone lighting |
| Default idle pose, arms at sides, default smile | Nobody posed it | §7 pose rules; an extreme frame of a real animation |
| Flat noon light, no shadow side | Default Studio lighting | Three-quarter key, rim, darker background |
| Stretched image | Not captured at 16:9 | Capture and export at 16:9 only |
| Collage of six features, UI screenshot with chat and names | No promise chosen; privacy problem | One promise per slot; `CaptureMode` on |
| Dark, low-contrast scene "for mood" | Unreadable at tile size; the commonest forum critique of horror tiles | One lit shape; lift the subject above mid-grey |
| Arrow, red circle, "!!" on everything | YouTube habit without a reason | One arrow only when it carries the before → after |
| Stock font with a default stroke | No brand | The game's display font, fixed outline token |

What transfers from other stores and what does not:

| Transfers | Does not transfer |
|---|---|
| App-icon rules: one subject, full-bleed art, no badges, test at small size (Apple and Google guidance) | App screenshots with captions and device frames |
| YouTube's lesson that the winner is judged on watch time, not clicks (its Test & Compare picks by watch-time share), which matches qPTR | Reaction faces of a real creator, red circles, a teaser that hides the subject: on Roblox the tile must show the game |
| Mobile A/B lesson: brighter and simpler usually wins, seasonal icons sometimes win (vendor cases report about +9% for a Halloween icon) | Trusting any published uplift figure: they are vendor case studies (search summaries) |

## 12. Clickbait and policy lines `[official]`

Consequences for ranking are in `analytics-and-discovery.md` §What clickbait costs. Lines for the artwork itself:

| Never in an icon, thumbnail or video | Source |
|---|---|
| Content, UI, odds or numbers the game does not contain | Discovery docs (mismatched metadata); video policy |
| Another game's characters, logo, layout or name styling | Community Standards: "confusingly similar to that of other creators"; discovery docs (non-unique) |
| Robux, prices, "free", giveaways, codes, like or favourite requests | Discovery docs (leading with giveaways); house rule |
| Links, handles, QR codes | Community Standards: external links only through Social Links |
| Blood, gore or fear beyond the game's maturity label | Moderation: a forum case shows a helmet with light blood rejected as too violent `[community]` |
| Real people, real-world brands, licensed characters without a licence | Community Standards (IP, personal information) |
| Voice, lyrics, real-life footage, enhanced graphics, promotional text in video | Video policy; rejections use the monthly quota |
| A boost or scarcity claim that is not live for every viewer | House rule 3 |

The Community Standards say nothing about generated art as such (page searched 2026-11-11); the misleading-metadata, uniqueness and IP rules apply to it like any other image, and the house rule is stricter than the platform.

## 13. Test plan

Method, interval formula, verdict table and the bandit's behaviour are in `analytics-and-discovery.md` §Thumbnail and icon testing; sample-size formula in its §Test design. Store-page specifics:

| Round | What to vary (one family at a time) | Keep fixed |
|---|---|---|
| 1 Promise | Five different promises, one recipe each | Brand layer, hero, style |
| 2 Composition | The winning promise as close-up, scale shot and split | Promise, text |
| 3 Text | No text, a number, a two-word verb | Image |
| 4 Emotion and colour | Expression; background hue against the genre's norm | Layout |

- **Always keep the current winner in the new set.** Since 1 July 2025 a new test that includes the existing winner leaves most traffic on it while the newcomers are measured (21% fewer impressions on non-winners in Roblox's test) `[official]`.
- **Do not restart inside 7 days**; staff call this the first rule. Start with an update, then leave the set alone `[official]`.
- **Sample size.** Roblox's own illustrative table shows qPTR of 1.4–2.1%. At a 1.8% baseline, telling a +30% relative lift from noise needs about 10,000 impressions per thumbnail, and +15% needs about 39,000 (`n ≈ 16(1 − p) ÷ (p × L²)`, same approximation as the owner file). Two thumbnails at 2.1% and 2.0% on 9,000 impressions each are a tie. Under about 1,000 DAU, test only round 1.
- **Reading it**: judge on qPTR and average playtime per qualified play together; a "loser" that wins one age segment stays active. A dip right after a traffic surge is normal `[official]`.
- **Fatigue is real**: one developer reported a tile falling from about 2% to 0.6% over time while the trend it rode faded `[community]`. Plan a new round each update instead of hunting for a permanent winner.
- **The icon has no A/B tool.** Change it only with an update, one element at a time (prop, expression or ground, never all three), and compare the same weekdays before and after on Search and Continue traffic. A sponsored campaign's even split across up to 10 creatives is the quick way to compare thumbnail ideas, not icons.
- **Before any impressions**: the stranger test. Show the tile for one second and ask "what do you do in this game?". Five strangers are enough to kill a bad idea.

## 14. Refreshes: updates and seasons

| Pattern seen on live games | Change | Keep |
|---|---|---|
| One-prop swap (Jujutsu Shenanigans hat, Jailbreak leaf) | A seasonal prop on the icon's subject | Silhouette, palette, crop |
| Logo variant (Blox Fruits pumpkin "O") | One glyph of the wordmark | Everything else |
| Scene swap in a fixed frame (Brookhaven, Berry Avenue, Theme Park Tycoon 2 with an update caption) | The inside scene | Frame, sign, logo position |
| Full art swap with a locked wordmark (Adopt Me) | Hero and colours for the new content | Wordmark, its corner, the style |

- Each major update: two or three new thumbnails that show the new content beside the standing winner; staff say fresh thumbnails with new gameplay signal an active game `[official]`. The detail-page list gets the update image in slot 2, after the video.
- Seasonal art goes up with the event and comes down with it; keep the off-season files ready so the revert is one upload. Switching back to an older icon or thumbnail does not hurt discovery `[official]` (discovery FAQ).
- An Experience Event gets its own thumbnail; a unique one lifts engagement with the event `[official]`.
- Recognition budget: returning players find the game by the icon. Change at most one of silhouette, palette and wordmark per refresh.
- After every art pass in the game, re-render the heroes from the linked file (§7) so the store never shows last season's model.

## 15. Critique rubric

Inputs: the full-size image, the tile-test sheet (§5), two or three raw in-game screenshots of what it shows, the icon, and the promise sentence. Shape adapted from `[lihfolk]`, criteria reconciled with rules 1–13.

Gates, pass or fail; a fail means do not upload:

- **Truthful**: every character, item, place, number and UI element exists in the game in the game's own style; judged against the raw screenshots.
- **Policy-safe**: §12 table.
- **Made, not generated**: every pixel traces to the game's Blender sources, a Studio capture or hand-designed Figma layers.

Ten criteria, each 0, 0.5 or 1:

1. One clear focal subject at the right size (30–45% thumbnail, 60–80% icon).
2. Reads at 320×180; the subject still reads at 160×90.
3. Subject separates in greyscale.
4. Genre obvious in one second; one deliberate break from the genre's norm.
5. A face with the right emotion, or an action in progress.
6. Text discipline: none, or a few large outlined words or one reachable number.
7. Nothing essential in the bottom 20% or the corners; edge ring not lost on either theme.
8. Shares hero, palette or wordmark with the icon and the set.
9. Stands out in a row of 12–20 competitor tiles.
10. No tell from §11.

8.5+ upload as a challenger · 7–8 fix the lowest criterion · 5–6.5 re-shoot (camera distance, light, subject) · under 5 new concept. For an icon replace criterion 2 with "subject named at 32 px, genre at 64 px".

Conflict: LihFolk's rubric allows three elements and no arrows or stickers; the vault's feed coding found giant numbers, before → after climbs and arrows common on current simulator hits and allows five elements. Use the vault limit for number-led genres (simulator, +1, tycoon), the stricter one for horror, roleplay and RPG, and let personalisation data decide.

Critique order when reviewing someone else's work: promise, focal point, value, colour, pose, text, finish. Name what, where and the fix ("hero and wall are both mid-grey: darken the wall 20%"); "make it pop" is not feedback.

## Level-up: store-page symptoms → likely cause → fix

Dashboard-side causes (eligibility, measurement changes, seasonality) are in `analytics-and-discovery.md` §Level-up; check those first.

| Symptom | Likely cause on the page | Fix |
|---|---|---|
| qPTR well under the genre's benchmark, retention fine | Tile does not say what you do ("cool scene" art); one thumbnail only | Rewrite the promise; five recipes; stranger test |
| qPTR up after new art, bounce up too | Render or promise beyond the first minute | Honesty pass (§8 step 7); retire or tone down |
| Feedback says "looks AI" or "looks like every other game" | Tells from §11; cloned format art | Rebuild from the game's meshes; change one genre norm (§4) |
| Good on desktop, weak on phones | Small text, small subject, dark edges | Tile test at 160×90; enlarge the hero; drop the text |
| Players cannot find the game again in Continue | Icon changed too much, or is a scene | One-element refresh rule; single subject |
| Winner changes every few days | Restarting tests; too few impressions | 7-day rule; sample sizes in §13 |
| A strong tile decays over weeks | Fatigue or a fading trend | New round with each update, winner kept in the set |
| Low plays from non-English markets | Text-led tiles and icon untranslated | A text-free thumbnail; per-locale icon for the top market |
| Image rejected by moderation | Blood, weapon aimed at the viewer, a real brand, a face too realistic for the label | Remove the element; match the maturity label; do not re-upload the same file |
| Video rejected | Voice, lyrics, added text claims, enhanced graphics | Recut to the §9 list; rejections count against 3 a month |
| Name cut off under the tile | Long leading tag or emoji string | Tag of 6 characters or fewer, or after the name |
| Search finds a lookalike first | Title and art too close to a format leader | Unique name and brand system; first unique metadata wins `[official]` |
| Store art out of date after an art pass | Hand-made one-off composites | Linked render file and PhotoStudio cameras |

## Review gate

- [ ] Each active thumbnail has a written first-minute promise, and the five promises differ.
- [ ] Every image passed the three gates in §15 and scored 8.5+; the tile-test sheet is saved beside the source.
- [ ] Icon: subject named at 32 px, genre at 64 px, readable on dark and light; no baked corners, shadow or badge.
- [ ] Thumbnails: 1920×1080, under 3 MB, nothing essential in the bottom 20%, subject separates in greyscale.
- [ ] Icon and thumbnails share hero, palette and wordmark; type uses the in-game display font.
- [ ] Blender renders use only the game's linked sources and an owned avatar; a side-by-side with a raw screenshot reads as the same game.
- [ ] No generated imagery anywhere, including ad creatives; no tell from §11.
- [ ] Video (if any): real footage, core verb in the first 3 s, no voice, lyrics, claims or enhancement.
- [ ] Title keeps the name inside the first 23 characters; first description line repeats the tile's promise; no stale seasonal tag.
- [ ] 2–5 thumbnails active including the current winner; no restart inside 7 days; variants judged on qPTR with playtime.
- [ ] At least one text-free thumbnail active; alt text set on the detail page.
- [ ] Source files, camera CFrames and metric windows archived; `[VS]` specs re-checked at create.roblox.com/docs.

## Sources

Accessed 2026-11-11. Images marked (viewed) were downloaded and looked at; entries with links are in `visual-library/icons-and-thumbnails.md`.

- Creator docs (CC BY 4.0), GitHub mirror `Roblox/creator-docs`: `production/publishing/thumbnails.md`, `experience-icons.md`, `cloud/guides/experience-icons-and-thumbnails.md`, `workspace/camera/free-camera.md`, `discovery.md`, `discovery-faq.md`, `production/promotion/ads-manager.md`, `experience-events.md` (read); example images on the icon and thumbnail pages (viewed).
- Roblox Community Standards, https://about.roblox.com/community-standards (read; searched for misleading-metadata, off-platform and AI wording).
- Staff posts on DevForum (read): /t/3257233 thumbnail personalisation launch · /t/3471689 five tips · /t/3793665 personalisation keeps the winner · /t/2875237 16:9 tiles on Home (mock-ups viewed) · /t/4945086 custom thumbnail required (and developer replies on AI art) · /t/4842601 gameplay videos on Home (two example captures viewed) · /t/4068103 video previews · /t/4984692 image translation beta · /t/3105942 icon and thumbnail translation experiment · /t/4880208 Creator Roadmap Fall 2026.
- Community threads on DevForum (read; images viewed where listed in the library): /t/1264771 soft GFX lighting · /t/1249194 GFX advertisement in Blender · /t/2723897 capturing screenshots and video in Studio · /t/662756 and /t/890782 beginner GFX guides · /t/991540 GFX course · /t/1774810 icon colour research · /t/4858140, /t/4158217, /t/3231984, /t/3797919, /t/3876094, /t/3187495, /t/4882870, /t/4960366, /t/4820075 critique and feedback threads · /t/4927362 mobile carousel covering the image · /t/4346638 reactions to a generated-art tool · /t/3274267 icon A/B request · /t/156111 and /t/3134162 artist portfolios.
- Live sample: icons (512 px) and the first three thumbnails (768×432) of 62 Top Playing Now games, and the 98 chart titles, fetched from Roblox's public `explore-api`, `games` and `thumbnails` endpoints on 2026-11-11 (viewed; measurements by script in the session, not shipped).
- The owner's vault: `references/market-scan-2026-11.md` rules 1–13 and feed statistics (read).
- LihFolk Vault V2 (CC BY 4.0, https://github.com/lihfolk-cy/v2-vault): `61 Thumbnails and CTR/` (Composition for High CTR; Making Thumbnails in Studio and Blender; Specs, Rules and Upload; Genre Patterns; Review Checklist and Scoring Rubric), `27 Marketing and Growth/` (Game Icon Design - Readable at Small Sizes; Game Trailers and Clean Footage), `45 Procedural Blender Assets/Dramatic Showcase Renders in Eevee.md` (read). Adapted in our own words.
- Google Play icon design specifications, https://developer.android.com/distribute/google-play/resources/icon-design-specifications (read).
- Search summaries only (hosts not reachable from this session): Search Engine Journal on faces in YouTube thumbnails (300K-video dataset); YouTube Test & Compare selecting by watch-time share; SplitMetrics MyTona Halloween icon case (+9.3%, +9.1%); Asodesk Towerlands icon test; Apple Human Interface Guidelines on app icons (page body did not load); an r/roblox thread and a change.org petition against AI thumbnails.
- Blender 5.3 manual, https://docs.blender.org/manual/en/latest/ : Cameras (lens unit, sensor fit, depth of field), Dilate/Erode node, Glare node, Solidify modifier (read, for option names in §7).
- Not verified: the Blender steps in §7 were not executed (Blender is not installed in the research environment; option names checked against the 5.3 manual, `[VS]`); theme background colours in the tile test are approximations; the half-day and one-day budgets are estimates.
