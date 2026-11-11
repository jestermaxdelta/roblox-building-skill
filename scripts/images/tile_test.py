"""Tile test: see an icon and thumbnails the way the Roblox Home grid shows them.

Usage:
    python3 tile_test.py icon.png thumb1.png [thumb2.png ...]

Writes tile_test.png in the current folder: the icon at 150, 64 and 32 px on dark
and light backgrounds, then each thumbnail at 320x180, 160x90, greyscale, blurred
and with the bottom 20% hidden. Needs Pillow (pip install pillow). Reads the files
you pass and writes one PNG; no network access.

Pass marks are in references/icons-thumbnails-and-store-page.md, section 5.
Run on 2026-11-11 with Python 3 and Pillow.
"""
import sys
from PIL import Image, ImageFilter, ImageOps
icon = Image.open(sys.argv[1]).convert("RGB")
thumbs = [Image.open(p).convert("RGB") for p in sys.argv[2:]]
DARK, LIGHT, PAD = (17, 18, 20), (242, 244, 245), 12   # approximate theme backgrounds
rows = []
for bg in (DARK, LIGHT):
    row = Image.new("RGB", (150 + 64 + 32 + PAD * 4, 150 + PAD * 2), bg); x = PAD
    for px in (150, 64, 32):
        row.paste(icon.resize((px, px), Image.LANCZOS), (x, PAD)); x += px + PAD
    rows.append(row)
for t in thumbs:
    big, small = t.resize((320, 180), Image.LANCZOS), t.resize((160, 90), Image.LANCZOS)
    grey = ImageOps.grayscale(big).convert("RGB")
    blur = big.filter(ImageFilter.GaussianBlur(3))
    cover = big.copy(); cover.paste((0, 0, 0), (0, 144, 320, 180))
    row = Image.new("RGB", (320 * 4 + 160 + PAD * 6, 180 + PAD * 2), DARK); x = PAD
    for im in (big, small, grey, blur, cover):
        row.paste(im, (x, PAD)); x += im.width + PAD
    rows.append(row)
sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), DARK); y = 0
for r in rows:
    sheet.paste(r, (0, y)); y += r.height
sheet.save("tile_test.png")
print("wrote tile_test.png")
