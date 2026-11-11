# Attribution for `assets/reference/`

## Original reference sheets (`NN-*.png`, sources in `src/`)

- 22 diagrams designed and drawn for the roblox-dev skill on 2026-11-11. Each is an HTML and inline-SVG page in `src/` rendered to PNG by `src/render.js` (Playwright, 800 CSS px wide at device scale factor 2, then palette-quantised with Pillow when it is installed).
- They contain no third-party artwork, logos, screenshots or textures. Mock game screens, icons, characters and effects are original vector drawings. They are distributed with the skill under the same terms as the rest of the repository.
- Numbers on the sheets come from the skill's own guides (the file and section are printed on each sheet). Guide content tagged `[lihfolk]` is adapted from LihFolk Vault V2 (CC BY 4.0), credited in the repository's `CREDITS.md`.
- Method credits: colour-vision simulation uses the matrices of Machado, Oliveira and Fernandes (2009); lightness values use Björn Ottosson's Oklab; contrast ratios use the WCAG 2 relative-luminance formula. Text is rendered in Inter where installed, falling back to the system sans-serif; no font file is bundled.
- Rebuild: `node assets/reference/src/render.js` (all sheets) or `node assets/reference/src/render.js 07 13` (some). The script prints a warning for any text that overlaps other text, leaves the sheet, is clipped or is drawn too small.

## Official Roblox documentation images: not bundled

Decision: **no image from `Roblox/creator-docs` is copied into this folder.** `references/visual-library/reference-sheets.md` §4 lists 30 of them as external references instead.

Licence evidence, read on 2026-11-11 at commit `7cbffff7aa3409302079631dc1035d53856f841c` (2026-11-10):

1. `LICENSE` at the repository root is the full text of "Creative Commons Attribution 4.0 International Public License" (396 lines). `LICENSE-CODE` is the MIT License, "Copyright (c) 2023 Roblox Corporation".
2. `README.md`, section "Licenses", says exactly: "For prose, this project uses the Creative Commons Attribution 4.0 International Public License. For full license text, see LICENSE." and "Code samples are available under the MIT License. For full license text, see LICENSE-CODE."
3. The launch announcement (DevForum, "Open Sourcing Creator Docs!", 29 August 2023, topic 2569346) says: "The repository uses two open-source licenses: Prose is available under the Creative Commons Attribution 4.0 International License [...] Code samples are available under the MIT License".
4. Images live under `content/en-us/assets/` as Git LFS objects. Neither statement names images, screenshots or media.
5. Several images are screenshots of other studios' experiences (for example `game-design/ui-ux-design/*` and `game-design/onboarding-techniques/*`), which Roblox may show in its docs but cannot be assumed to relicense.

Reading: CC BY 4.0 clearly covers the prose. It does not clearly cover the images, and for third-party game screenshots it very likely does not. The skill therefore links to them and does not redistribute them. If Roblox states that documentation media are CC BY 4.0, the rows in the index already carry the source path needed for attribution; images of third-party games should stay links regardless.

Attribution for the linked images: © Roblox Corporation (and the respective studios for game screenshots), source `https://github.com/Roblox/creator-docs`, path as listed in the index under `content/en-us/assets/`.
