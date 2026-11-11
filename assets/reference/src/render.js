// Rebuilds every reference sheet: node assets/reference/src/render.js [name-filter ...] [--no-lint]
// Each NN-*.html in this folder is rendered at 800 CSS px, deviceScaleFactor 2, to ../NN-*.png.
// Uses the Playwright that is already installed (no downloads). If Python with Pillow is present the PNGs are
// palette-quantised afterwards to keep each under about 250 KB; without it the larger true-colour files are kept.
const { chromium } = require('playwright');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Runs in the page: reports text that overlaps other text, leaves the sheet, is clipped or is too small.
function lint() {
  const sheet = document.querySelector('.sheet');
  const sr = sheet.getBoundingClientRect();
  const items = [];
  const walker = document.createTreeWalker(sheet, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const label = node.textContent.trim();
    if (!label) continue;
    const pe = node.parentElement;
    if (pe.closest('[data-lint="off"]')) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    let clip = pe;
    while (clip && clip !== sheet && getComputedStyle(clip).overflow === 'visible') clip = clip.parentElement;
    const cr = (clip || sheet).getBoundingClientRect();
    for (const q of range.getClientRects()) {
      if (q.width < 1 || q.height < 1) continue;
      if (q.right <= cr.left || q.left >= cr.right || q.bottom <= cr.top || q.top >= cr.bottom) continue; // fully hidden by a clipping ancestor
      items.push({ label: label.slice(0, 28), node, x0: q.left, y0: q.top, x1: q.right, y1: q.bottom, h: q.height, cr, small: !pe.closest('[data-lint="nosize"]') });
    }
  }
  const out = [];
  for (const a of items) {
    if (a.x0 < sr.left - 0.5 || a.x1 > sr.right + 0.5 || a.y0 < sr.top - 0.5 || a.y1 > sr.bottom + 0.5) out.push(`outside sheet: "${a.label}"`);
    else if (a.x0 < a.cr.left - 1 || a.x1 > a.cr.right + 1 || a.y0 < a.cr.top - 1 || a.y1 > a.cr.bottom + 1) out.push(`clipped: "${a.label}"`);
    if (a.small && a.h < 11.5) out.push(`small text (${a.h.toFixed(1)} px line): "${a.label}"`);
  }
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      const a = items[i], b = items[j];
      if (a.node === b.node) continue;
      const pa = a.h * 0.22, pb = b.h * 0.22; // ignore line-box leading
      if (a.x0 + 0.5 < b.x1 && b.x0 + 0.5 < a.x1 && a.y0 + pa < b.y1 - pb && b.y0 + pb < a.y1 - pa) out.push(`overlap: "${a.label}" x "${b.label}"`);
    }
  }
  return [...new Set(out)];
}

const QUANTISE = `
import sys
from PIL import Image
for p in sys.argv[1:]:
    im = Image.open(p).convert("RGB")
    im.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(p, optimize=True)
`;

(async () => {
  const src = __dirname;
  const out = path.join(src, '..');
  const args = process.argv.slice(2);
  const filters = args.filter(a => !a.startsWith('--'));
  const files = fs.readdirSync(src).filter(f => /^\d\d-.*\.html$/.test(f)).filter(f => !filters.length || filters.some(o => f.includes(o))).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('  page error:', e.message));
  const made = [];
  let bad = 0;
  for (const f of files) {
    await page.goto('file://' + path.join(src, f));
    await page.evaluate(() => document.fonts.ready);
    const problems = args.includes('--no-lint') ? [] : await page.evaluate(lint);
    const target = path.join(out, f.replace('.html', '.png'));
    await (await page.$('.sheet')).screenshot({ path: target });
    made.push(target);
    bad += problems.length;
    console.log(f + (problems.length ? '\n  ' + problems.join('\n  ') : '  ok'));
  }
  await browser.close();
  const q = spawnSync('python3', ['-c', QUANTISE, ...made], { encoding: 'utf8' });
  if (q.status !== 0) console.log('Pillow not available: PNGs left unquantised.', (q.stderr || '').split('\n')[0]);
  for (const p of made) console.log(`${path.basename(p)}  ${(fs.statSync(p).size / 1024).toFixed(0)} KB`);
  if (bad) console.log(`${bad} layout warning(s) above.`);
})();
