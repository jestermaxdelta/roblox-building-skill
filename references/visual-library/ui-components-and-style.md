# UI reference library: components and style

What this is: 51 checked references for the parts a UI is built from and the look that ties them together: kit sheets and style directions, design tutorials, techniques, Roblox's native styling features, motion, icon sets with their licences, and tools.
The rules these references support live in `references/ui-design-figma.md` (§3 colour, §4 type, §5 icons, §6 construction, §8 tells), `references/ui-motion-and-feedback.md` and `references/ui-input-crossplatform.md`.

How to use this file:
- Before drawing a kit, open three rows from section 1 (include one marked template) and write down what the strong ones share: outline weight, lip, highlight angle, radius, the one motif. Then draw your own five pieces with those numbers fixed.
- Evidence: `viewed` = the image was downloaded and looked at; `read` = the page, thread or licence file was read; `oembed` = the video exists with that title and channel and was not watched; `search` = seen in search results only. `†` after the evidence word = the link is a Fandom `File:` page: it opens in a browser, but Fandom answers HTTP 403 to automated clients (curl, fetch tools), so an agent should download the `WK/…` image path given in the same row instead. Each such file was confirmed to exist through its wiki's `api.php` on 2026-11-11. Row numbers are stable ids that the guides cite: a removed row leaves a gap. Every link and image path was re-requested on 2026-11-11 (GitHub through `git ls-remote`): all answered except kenney.nl (#10), whose page and image return HTTP 403 to clients without a browser user agent and open normally in a browser.
- File types and sizes (checked 2026-11-11): every linked image is a still; no row links a GIF or a video file. Fandom `WK/` paths serve WebP under a .png or .jpg name (the Read tool opens it). Files of 1.5 MB or more carry their size after the path, for example `(PNG 7.3 MB)`; every other file is under 1.5 MB. Each section opens with a "Start here" line naming its strongest rows.
- These are references to study, not assets to copy: every kit, screenshot and icon stays its owner's. Licences are quoted as read on 2026-11-11 and can change; nothing here is legal advice.

Image host prefixes: `DF` = `https://devforum-uploads.s3.dualstack.us-east-2.amazonaws.com/uploads/original`, `WK` = `https://static.wikia.nocookie.net`, `IIG` = `https://interfaceingame.com/wp-content/uploads`. "megathread" = DevForum thread t/311776 "Show off your UI designs" (the link goes to the post).

## 1. Kits, style directions and families

Start here: #1, #2, #3, then template #8 beside them.

Rows marked as template or "before" are here on purpose: compare them with the rows above them.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 1 | [Build & Survive: one kit across five windows](https://devforum.roblox.com/t/311776/87), Preston_Username (BIG Games), 2019, megathread · img `DF/4X/b/9/b/b9ba114f14e13727007c3ce1e10c0ee2db47d20f.png` | image | The inventory from the same set as the shop, coins, settings and dialog mockups in `ui-screens.md`: every window reuses one slanted navy header with halftone dots, one red diamond X, one section tag, one white body, one font pair. Comic-book motif, tilted a few degrees, as the signature. | viewed |
| 2 | [Hand-drawn wood panel and button set](https://devforum.roblox.com/t/311776/142), SturdyStubs, 2019, megathread · img `DF/4X/1/6/1/161075ca6577ff9703adc1d4d0d628cf4889614a.png`, `DF/4X/a/6/a/a6a5721214ab6700bf4c85db2d30fd43b0262b51.png` | image | 9-slice material in practice: a plank frame with a pinned parchment body, and buttons that all share one lip, one highlight band and one outline. Green for every action that proceeds, dark red for No, a round red X; an XP bar with a hex end cap. | viewed |
| 3 | [Glossy "gem" frames (WIP pack)](https://devforum.roblox.com/t/4966865), izzystradlinxx, 2026, feedback thread · img `DF/5X/e/9/7/9/e97917061346b3860e4dfb9e4abe608e1256db6a.jpeg` | image | Hex icon buttons each in a jewel colour, currency pills with a slanted shine, a tilted title tab on the Codes panel, one green Verify. The shine angle and outline weight are identical on every piece, which is what makes it a family. | viewed |
| 4 | [Persona 5-style menu rebuilt in Roblox, beside the original](https://devforum.roblox.com/t/4843768), lollyTR2, 2026 · img `DF/5X/1/4/3/6/1436b1eea47733406462989a5df0f410c79cb905.jpeg`, `DF/5X/6/4/3/3/6433acdb3514e377e2312c4a0ebbb2ac532d298a.jpeg` | image | A hard style direction: cut-paper letters, black, white and red only, everything tilted. A typographic idea carries the screen with no gradient or glow. It is also a caution: this is a famous skin, so take the lesson (one loud idea), not the look. | viewed |
| 5 | [Screen3D: UI with real perspective](https://devforum.roblox.com/t/3273671), yy_qat, 2024, 668 likes; github.com/CatGuyMoment/Screen3D (no licence file found) · img `DF/5X/7/3/8/4/7384eae43581a6d8b5304d2fd2eba637a50f6170.jpeg` | repo | A lobby list skewed in 3D in black and white, in the manner of Phighting. One tilted hero panel can sign a game's look; keep anything the player must read or tap precisely off it. | viewed |
| 6 | [Dress to Impress: icon and panel art in progress](https://dress-to-impress.fandom.com/wiki/File:Valentines_2026_-_UI_Reworks.jpeg), wiki upload 2026 · img `WK/dti-dress-to-impress/images/7/78/Valentines_2026_-_UI_Reworks.jpeg` | image | A capture from a painting app: round medallion icons with a painted subject on the brand pink, and a hand-painted Codes panel. The icons are illustrations in one palette with one light direction: what "designed by hand" looks like on a live hit. | viewed † |
| 7 | [Animal Crossing: New Horizons: NookPhone app grid](https://interfaceingame.com/screenshots/animal-crossing-new-horizons-nookphone/), Nintendo, via interfaceingame.com · img `IIG/animal-crossing-new-horizons/animal-crossing-new-horizons-nookphone.jpg` | image | Nine app icons: one rounded-square plate each, one pastel per app, a simple two-tone glyph, one stroke weight. The selected app's name is printed once above the grid, not under every icon. | viewed |
| 8 | [Epic UI Pack: button matrix](https://devforum.roblox.com/t/2206337), MapleMarvel, 2023, 440 likes (Creator Store plugin) · img `DF/5X/1/f/1/b/1f1bb743caba37910552f0b515694b2350ffb256.jpeg`, `DF/5X/e/a/f/8/eaf86322aedc705cce90e5327aa650a6c9eef76f.jpeg` | gallery | Ten hues × four styles × six sizes of one bevelled button. Useful to see a size ladder and what a stock kit offers; as a look it is the template tell itself: variety by recolour only, with nothing tied to a game. Study it, do not ship it. | viewed |
| 9 | [Cartoon UI pack on one sheet](https://devforum.roblox.com/t/311776/100), Bylocks, 2019, megathread · img `DF/4X/0/d/0/0d000ddecd067902fe86f7782b8ab872d68cd23c.png` | image | A whole kit laid out together: currency pill, bar, titled panels, icon-button set, confirm dialog, chat, dialogue. Good as a checklist of components to draw; the single blue for everything is why it reads as a template. | viewed |
| 10 | [Kenney UI Pack](https://kenney.nl/assets/ui-pack), Kenney; Creative Commons CC0 (stated on the page and the preview image) · img `https://kenney.nl/media/pages/assets/ui-pack/ab9e396e4d-1718203978/preview.png` | tool | Buttons, sliders, checkboxes and panels in five colours, free for commercial use without credit. A grey-box kit for wireframes and tools; a shipped game replaces it with its own family. kenney.nl answers 403 to automated clients: open it in a browser. | viewed |
| 11 | [A designer's own "before": early admin panel and gun shop](https://devforum.roblox.com/t/3077233), unroot, in Roblox's Creator Spotlight, 2024 · img `DF/5X/6/1/1/c/611c02d1bba6915a4db01996bb0e7af1c18b0922.png` | image | Default font, coloured text on translucent blue frames, rows of small same-size buttons. Shown by a now-professional designer as where he started; open it next to his later work in `ui-screens.md` to see what changed (hierarchy, spacing, one accent). | viewed |

## 2. Design fundamentals

Start here: #12, #15, #20.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 12 | [UI Design Starter Guide](https://devforum.roblox.com/t/53461), EmeraldSlash, 2017, 1,112 likes | tutorial | The base course: Scale against Offset, AnchorPoint, ZIndex and DisplayOrder, aspect ratio, text scaling and stroke, black edges on images, 9-slicing, sprite sheets, padding. The screenshots are from 2017; the concepts are unchanged `[VS]`. | read |
| 13 | [UI Design Objects & Tips](https://devforum.roblox.com/t/613948), EmeraldSlash, 2020, 182 likes | tutorial | The follow-up: UICorner, UIGradient, ViewportFrame, each layout, UIScale and the three constraints, then separate advice lists for designers and for scripters. | read |
| 14 | [The Ultimate UI Design Guide](https://devforum.roblox.com/t/1236916), lookLOLtrelakor, 2021, 426 likes | tutorial | Design only: sketch, build in Figma, prototype, import, and hand the developer a spec of what you want. It names Gotham, which now renders as Montserrat `[VS]`. | read |
| 15 | [How to make extremely Clean UI while keeping good UX](https://devforum.roblox.com/t/2438099), bitsplicer, 2023, 108 likes | tutorial | Primary against secondary buttons, with screenshots of pairs that look alike; one constant colour scheme; three ways to fake depth (stroke, duplicated frame, shadow texture). Written before `UIShadow` shipped, so the depth section is now a fallback `[VS]`. | read |
| 16 | [Here's How to Create a Modern Sleek UI Design](https://devforum.roblox.com/t/2528850), rivvvur, 2023, 223 likes | tutorial | A step-by-step dark "modern" panel with a hover script and a section arguing for Offset over Scale. Read it as the recipe behind the dark-dashboard look many games now share, then decide on purpose whether your game wants it. | read |
| 17 | [Professional UI Designer Raising Guides 101, chapter 1](https://devforum.roblox.com/t/476101), 7kayoh, 2020, 232 likes | tutorial | UX before UI, choosing a theme colour, contrast and font cautions, and a list of software and platform guidelines to read. | read |
| 18 | [Don't be so simple-minded at adding borders to your UI](https://devforum.roblox.com/t/1022437), 7kayoh, 2021, 80 likes | tutorial | Why a border made from an enlarged copy of a rounded frame has the wrong corner radius, shown at large scale. Today: `UIStroke`, or outer radius = inner radius + border width. | read |
| 19 | [How to Plan, Design and Build Quality User Interfaces](https://devforum.roblox.com/t/281785), wevetments, 2019, 279 likes | tutorial | Moodboard on Pinterest → concept → one element → symbols (cross, tick) → export → import, in Adobe XD. The tool has aged; the moodboard-first order has not. | read |
| 20 | [Choose an art style (UI design curriculum)](https://create.roblox.com/docs/tutorials/curriculums/user-interface-design/choose-an-art-style), Roblox docs (CC BY 4.0) | tutorial | Sort the UI needs into categories first; limit the colour theme to key information; never rely on colour alone; outline simple icons whose shape language differs from the 3D world while still belonging to it. | read |

## 3. Technique: clipping, borders, shine, icon fonts, type

Start here: #21, #24, #26.

9-slice, export and upload settings are in `ui-design-figma.md` §6 and §13.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 21 | [ClipDescendants with UICorners](https://devforum.roblox.com/t/2492826), Fittergem1000, 2023, 88 likes | tutorial | A `CanvasGroup` with a `UICorner` clips its children to the rounded shape, which `ClipsDescendants` alone does not. Budget CanvasGroups (texture memory) as `ui-input-crossplatform.md` says. | read |
| 22 | [How to make a moving gradient border on a GUI](https://devforum.roblox.com/t/1126520), Awayville, 2021, 143 likes | tutorial | A rotating `UIGradient` on a slightly larger rounded frame behind the content gives an animated border. One per screen at most; with several strokes per object now native, a gradient on a `UIStroke` does the same with one instance `[VS]`. | read |
| 23 | [GUI Shine module](https://devforum.roblox.com/t/4816664), Landinzo, 2026 · img `DF/5X/e/6/7/7/e677c1ba9d218e7d4d77042d2c5bf3b7dc861a82.png` | tool | A diagonal highlight swept across a square, a circle and a rounded tile by tweening a gradient on a temporary child frame; the thread explains the clipping problem on rounded shapes. Shows the "shine" token on three silhouettes. | viewed |
| 24 | [Customize your GUIs with builder icons](https://devforum.roblox.com/t/3968755), 82_O7, 2025, 104 likes · img `DF/5X/1/e/0/6/1e063605addbd1ad031c72334546e599a7dd73f3.jpeg`, `DF/5X/7/f/0/7/7f07e2c0b965adb4edbf1a7d51bd5f0139a0e4cc.png` | tutorial | Roblox's built-in `BuilderIcons` font: about 300 named glyphs (controller and keyboard keys, mouse buttons, social marks, common verbs) typed inside a RichText `<font family>` tag, with filled variants through `<b>`. The asset path is undocumented `[VS]`: wireframes and input hints only. | viewed |
| 25 | [Text+](https://github.com/AlexanderLindholt/TextPlus), AlexanderLindholt, 2025, 937 likes; MIT (LICENSE read) | repo | An open-source text renderer that draws any font file as sprites with per-character control. The route to a display face Roblox does not ship; keep body text native so localisation and the text-size setting still work. | read |
| 26 | [Builder font licence](https://create.roblox.com/docs/resources/builder-font-license), Roblox docs | tool | Builder Sans, Extended and Mono may be used solely to create and publish UGC on Roblox and for digital promotions of that UGC off the platform: fine in the game, its thumbnails and its trailers, not in other products. | read |

## 4. Native styling features: what no longer needs an image

Start here: #27, #28, #31.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 27 | [\[Full Release\] New UI Capabilities: Shadows & Individual Corners!](https://devforum.roblox.com/t/4636263), missmandypanda (Roblox), fully released 23 Jun 2026, 1,963 likes · img `DF/5X/f/6/6/e/f66e25437c5be089152fb0a2be7e091f9ebac9d3.png` | breakdown | `UIShadow` and per-corner `UICorner` radii. The before/after image is a ladder of blur radii from 1 to 128 px after the retune toward CSS: use it to pick a blur by eye instead of by number. | viewed |
| 28 | [\[Full Release\] Upgraded UIShadow Capabilities](https://devforum.roblox.com/t/4934553), missmandypanda (Roblox), fully released 5 Nov 2026 · img `DF/5X/0/b/d/d/0bddce714b334aaeeb4ec1ff002871cf1523342d.png` | breakdown | Text, inset, knockout and gradient shadows. The example strip shows a glowing pill, an inset orb, two text shadows and a knockout ring: pressed states and glows with no PNG. | viewed |
| 29 | [\[Full Release\] Upgraded UI Gradients](https://devforum.roblox.com/t/4846594), missmandypanda (Roblox), fully released 29 Oct 2026 · img `DF/5X/b/2/a/e/b2ae567f3d1abc9e0222f7e9b59eae6208a88b84.jpeg` | breakdown | Radial, conic and elliptical gradients, tile modes and scale. The elliptical example fills a wide frame edge to edge; the post lists banding on darker gradients as a known issue. | viewed |
| 30 | [\[Full Release\] UIStroke Improvements: Scaling, Offsets, and More!](https://devforum.roblox.com/t/3958036), missmandypanda (Roblox), fully released 4 Dec 2025 | breakdown | Stroke thickness that scales with the parent, inner / centre / outer position, offset, ZIndex, and several strokes on one object: the double outline of cartoon kits without stacked frames. | read |
| 31 | [\[Full Release\] UI Styling is officially released!](https://devforum.roblox.com/t/4275082), missmandypanda (Roblox), Jan 2026; follow-ups t/4566519 (StyleQuery, May 2026) and t/4646870 (transitions, Jul 2026) | breakdown | StyleSheets, StyleRules and the Style Editor for one-place re-skins; StyleQuery adds device, input, reduced-motion and text-size queries; transitions add tweens with no script. | read |

## 5. Motion and micro-interactions

Start here: #33, #38, #39.

Tokens and rules: `ui-motion-and-feedback.md`.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 32 | [\[Advanced UI\] Introduction to 2D Animations](https://devforum.roblox.com/t/459849), kenami, 2020, 622 likes | tutorial | Argues that UI animation is part of a game's graphics, using Pet Simulator's lively interface over a deliberately plain map as the case, then gives tween recipes with place files. | read |
| 33 | [spr: spring-driven motion](https://github.com/Fraktality/spr), Fractality, 2020, 364 likes; MIT (LICENSE read) | repo | One call per animation (`spr.target(instance, damping, frequency, properties)`); a spring keeps its velocity when retargeted, which a tween cannot. Use for anything poked repeatedly. | read |
| 34 | [Juice it or lose it - a talk by Martin Jonasson & Petri Purho](https://www.youtube.com/watch?v=Fy0aCDmgnxg), grapefrukt (YouTube) | video | Not watched here; by its title and reputation, a talk on adding "juice" (layered feedback) to a plain game. Listed as the motion guide's reference talk: `ui-motion-and-feedback.md` §Sources. Watch for which single addition changes the feel most. | oembed |
| 35 | [Jan Willem Nijman - Vlambeer - "The art of screenshake"](https://www.youtube.com/watch?v=AJdEqssNZ-U), Dutch Game Garden (YouTube), 2013 | video | Not watched here; a Vlambeer designer's talk on screenshake and feedback, the second reference talk in `ui-motion-and-feedback.md`. Note the order in which effects are added. | oembed |
| 37 | [Hearthstone: How to Create an Immersive User Interface](https://www.youtube.com/watch?v=axkPXCNjOh8), GDC (YouTube); Blizzard talk from GDC 2015 per its GDC Vault listing | video | Not watched here; the UI talk for the game that the Game Developer article in `ui-hud.md` singles out as "tactile and clear". Search summaries describe it as the case for a physical interface over a flat one. | oembed |
| 38 | [Easing Functions Cheat Sheet](https://easings.net/), easings.net | tool | A curve and a motion preview for every standard easing; match each to `Enum.EasingStyle` and direction before writing a token. | read |
| 39 | [NumberSpinnerV2](https://github.com/biotoxin495/NumberSpinnerV2), biotoxin495, 2026; MIT (LICENSE read); thread t/4748302 | repo | Rolling-digit counters for currency and score labels, a modern rewrite of boatbomber's NumberSpinner. | read |
| 40 | [Dynamic ScrollingFrames (plugin)](https://devforum.roblox.com/t/4756150), ui_vns, 2026, 46 likes | tool | Turns an ordinary ScrollingFrame into a curved, diagonal or looping menu using the existing items: carousel and wheel layouts without custom layout code. | read |

## 6. Icon sets, with the licence that was read

Start here: #41, #44, #43.

House position: a shipped game's icons are its own family, drawn in Figma or rendered from its own Blender assets (`ui-design-figma.md` §5). Use these sets to study construction, to test metaphors and to fill wireframes. If one is ever shipped, keep the licence file and any required credit.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 41 | [Lucide](https://lucide.dev/), ISC License (lucide.dev/license and LICENSE read) | tool | A large stroke-icon family on one grid with one stroke weight. Study how every glyph keeps the same corner and line endings. | read |
| 42 | [lucide-roblox](https://github.com/latte-soft/lucide-roblox), Latte Softworks; MIT (LICENSE.md read) | repo | Lucide packaged for Roblox (Wally package `latte-soft/lucide-icons`) with an index of rendered icons and their ids. For tools, plugins and wireframes. | read |
| 43 | [Phosphor Icons](https://phosphoricons.com/), MIT (LICENSE read in phosphor-icons/core) | tool | One family in several weights, including fill and duotone: a reference for drawing the same icon as outline (idle) and filled (active). | read |
| 44 | [Game-icons.net](https://game-icons.net/), "Creative Commons 3.0 BY or CC0 if mentioned", per contributor folder (license.txt read); credit required for the CC BY icons | tool | About 4,180 single-colour game glyphs (weapons, skills, creatures, resources). The fastest way to check a metaphor (does a sword read as strength?) before drawing your own. | read |
| 45 | [Material Symbols and Icons](https://fonts.google.com/icons), Google; Apache License 2.0 (LICENSE read in google/material-design-icons) | tool | Outlined, rounded and sharp versions of one set with adjustable weight and fill: shows how corner style alone changes tone. | read |

## 7. Tools

Start here: #47, #53, #49.

Figma-to-Roblox converters are in `ui-design-figma.md` §13; UI frameworks are in `ui-input-crossplatform.md`.

| # | Reference (linked title, creator, year) | Type | Look at it for | Evidence |
|---|---|---|---|---|
| 47 | [flipbook](https://github.com/flipbook-labs/flipbook), flipbook-labs; MIT-style licence text (LICENSE read) · img `https://raw.githubusercontent.com/flipbook-labs/flipbook/main/docs/static/img/main-screenshot.png` | repo | A storybook inside Studio: component list on the left, live preview, and a Controls panel that toggles props such as `isDisabled`. The way to see every state of a button without playtesting. | viewed |
| 48 | [UI Labs](https://github.com/PepeElToro41/ui-labs), PepeElToro41, 2024, 238 likes; GPL-3.0 (LICENSE read) | repo | Storybook plugin with hot reload for code-built UI (React, Fusion, Vide). GPL covers the plugin, not the UI you preview in it. | read |
| 49 | [OnyxUI](https://github.com/ImAvafe/OnyxUI), Avafe; MIT (LICENSE read) | repo | A themeable component kit for Fusion ("quick, customizable components"). Read how its theme object names colours, spacing and corner radii, then name your own. | read |
| 50 | [Slither (open-source Roblox game)](https://github.com/littensy/slither), littensy; MIT (LICENSE.md read) | repo | A complete casual game whose README states its palette (Catppuccin) and its sources. A working example of a whole game built on one named palette and a code-built UI. | read |
| 51 | [Pixel Perfect (plugin)](https://devforum.roblox.com/t/4927833), RiotDestrudo, 2026, 41 likes; Creator Store | tool | Figma-style editing in the Studio viewport: properties, layers and zoom. For nudging native UI after the Figma hand-off. | read |
| 52 | [ExpressivePrompts](https://github.com/MiaGobble/ExpressivePrompts), Mia Gobble, 2026, 252 likes; MIT (LICENSE read) | repo | A customisable ProximityPrompt UI with animation and sound, configured from one dictionary. A starting point for prompts that match the game's kit. | read |
| 53 | [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/), WebAIM | tool | Type the text and background colours, read the ratio. Check body text at 4.5:1 and large text and icons at 3:1 against a colour sampled from a real gameplay capture. | read |

## Patterns seen across these references

- A kit reads as one family when four numbers never change: outline weight, lip depth, highlight angle, corner radius (#2, #3, #1, #7).
- Each strong kit has one motif that could not be moved to another game unchanged: halftone comic panels, planks and parchment, cut paper, jewel gloss (#1, #2, #4, #3). The template kits have none (#8, #9, #10).
- Colour is assigned by function and kept: green proceeds, red closes or declines, the neutral carries everything else (#2, #1, #3).
- Icons are a plate plus a simple glyph, one colour per destination, drawn or painted as a set; the name is printed once, not repeated under every icon (#7, #6). Open icon sets show the construction grid to imitate (#41, #43, #45).
- Tilt and skew are a signature for headers and hero panels only; bodies stay square to the screen (#1, #3, #5, #4).
- Since 2025–2026 the engine draws shadows, inset shadows, per-corner radii, radial gradients and stacked strokes, so images are left for silhouettes, textures and illustration (#27, #28, #29, #30 against #2, #6).
- Older tutorials still teach the right concepts, but their depth, border and clipping workarounds are now fallbacks (#15, #18, #21, #22).
- Motion references agree on spending effects where the player acts and letting springs handle anything retargeted (#32, #33, #34, #35).
- Professional process starts from references and a named direction, then tokens, then components (#19, #20, #14); a storybook shows every state before a playtest (#47, #48).
- Licences differ in what they ask: ISC, MIT and Apache need the notice kept; CC BY needs visible credit; the Builder font is limited to Roblox use (#41, #43, #45, #44, #26).

## What the weak examples had in common

Drawn from the images rejected while building this file (megathread posts 12, 25, 163, 466, 1657, 2348 and 2698; threads t/210627, t/4859702, t/4941194, t/794068) and from rows #8, #9, #11.

- Variety by recolour: the same bevel and lip in ten hues, or five buttons in five unrelated colours, with no rule for which colour means what.
- No motif from the game's world: the kit could be pasted into any game, which is exactly how players read it.
- One hue for every surface, or a dark translucent panel with a thin bright stroke and a soft shadow on everything (the web-dashboard look in `ui-design-figma.md` §8).
- Default font with a thick outline, or a decorative or alien display face used for text that must be read.
- Neon outline glow on every edge; chrome and metal gradients; a grid texture standing in for design.
- Icons from mixed sources in one grid (emoji-like, flat and rendered side by side).
- Showcases that prove nothing about a game: watermark-covered sheets, GFX renders and platform-chrome redesigns posted as game UI, and kits shown only in their resting state with no pressed, disabled or selected variants.

## Sources and licences

- DevForum threads, megathread posts and Roblox staff announcements (read through the forum's JSON API): text and images belong to their authors or to Roblox; linked for study only.
- Roblox Creator Docs text is CC BY 4.0 (`Roblox/creator-docs`); that licence statement names the prose, not the images, so docs images are © Roblox and are linked here for study, not redistributed. Builder font: its own licence, read at `create.roblox.com/docs/resources/builder-font-license`.
- Licences read from each project's own licence file or page on 2026-11-11: Lucide ISC; lucide-roblox MIT; Phosphor MIT; game-icons.net CC BY 3.0 (CC0 where a contributor says so); Material Symbols Apache-2.0; Kenney UI Pack CC0; spr MIT; Text+ MIT; NumberSpinnerV2 MIT; OnyxUI MIT; Slither MIT; ExpressivePrompts MIT; UI Labs GPL-3.0; flipbook MIT-style text. No licence file was found for Screen3D. Star counts were not recorded (the GitHub API is blocked on this network).
- interfaceingame.com and the Dress to Impress wiki (Fandom, text CC BY-SA): screenshots of commercial games, which stay their publishers'.
- YouTube titles and channels verified through oEmbed; the videos were not watched. Removed in review (2026-11-11): row 36 (an unwatched video described only by its title) and row 46 (Tabler Icons, a second stroke-icon set that added nothing to row 41).
- Not reachable or not opened: figma.com community files (HTTP 403), gameuidatabase.com, artstation.com, behance.net, dribbble.com, reddit.com. No named Roblox UI designer's off-forum portfolio or TikTok could be confirmed through search, so none is listed.
