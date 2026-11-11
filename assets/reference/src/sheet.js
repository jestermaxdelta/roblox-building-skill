/* Shared helpers for the reference sheets: page frame, SVG builder, colour maths, easing.
   Loaded by every NN-*.html in this folder. No dependencies. */
const Sheet = (() => {
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  // Adds the standard header and footer around the sheet body.
  function frame({ n, cat, title, sub, supports, sources }) {
    const sheet = document.querySelector('.sheet');
    const hdr = document.createElement('div');
    hdr.className = 'hdr';
    hdr.innerHTML = `<div><div class="kicker">Reference sheet ${n} · ${cat}</div><h1>${title}</h1><div class="sub">${sub}</div></div>
      <div class="supports"><b>Supports</b>${supports.join('<br>')}</div>`;
    sheet.prepend(hdr);
    const ftr = document.createElement('div');
    ftr.className = 'ftr';
    ftr.innerHTML = `<span>roblox-dev skill · original diagram</span><span>Numbers from ${sources}</span>`;
    sheet.append(ftr);
  }
  // Tiny SVG string builder: el('rect',{x:1}) or el('g',{},[children])
  function el(tag, attrs = {}, kids = '') {
    const a = Object.entries(attrs).filter(([, v]) => v !== undefined && v !== null).map(([k, v]) => ` ${k}="${v}"`).join('');
    const body = Array.isArray(kids) ? kids.join('') : kids;
    return `<${tag}${a}>${body}</${tag}>`;
  }
  const txt = (x, y, s, a = {}) => el('text', Object.assign({ x, y, 'font-size': 10.5, fill: '#465062' }, a), esc(s));
  // ---- colour maths (sRGB hex in, numbers out) ----
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const toHex = rgb => '#' + rgb.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('').toUpperCase();
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const unlin = c => 255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055);
  const lum = h => { const [r, g, b] = hex(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const grey = h => { const v = unlin(lum(h)); return toHex([v, v, v]); };
  function oklab(h) {
    const [r, g, b] = hex(h).map(lin);
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s];
  }
  const dOk = (a, b) => { const x = oklab(a), y = oklab(b); return Math.hypot(x[0] - y[0], x[1] - y[1], x[2] - y[2]); };
  // Machado, Oliveira and Fernandes (2009) matrices, severity 1.0, applied in linear RGB.
  const CVD = {
    protan: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    deutan: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.01182, 0.04294, 0.968881]],
    tritan: [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.3039]],
  };
  const sim = (h, kind) => { const v = hex(h).map(lin); return toHex(CVD[kind].map(r => unlin(Math.max(0, Math.min(1, r[0] * v[0] + r[1] * v[1] + r[2] * v[2]))))); };
  // ---- easing (t in 0..1) ----
  const ease = {
    linear: t => t,
    sineInOut: t => 0.5 - 0.5 * Math.cos(Math.PI * t),
    quadOut: t => 1 - (1 - t) * (1 - t),
    quadInOut: t => (t < 0.5 ? 2 * t * t : 1 - 2 * (1 - t) * (1 - t)),
    cubicInOut: t => (t < 0.5 ? 4 * t * t * t : 1 - 4 * Math.pow(1 - t, 3)),
    quintInOut: t => (t < 0.5 ? 16 * Math.pow(t, 5) : 1 - 16 * Math.pow(1 - t, 5)),
    backOut: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  };
  // Polyline path from a function sampled over [0,1].
  function plot(fn, x, y, w, h, n = 80, lo = 0, hi = 1) {
    let d = '';
    for (let i = 0; i <= n; i++) { const t = i / n, v = fn(t); d += (i ? 'L' : 'M') + (x + t * w).toFixed(1) + ' ' + (y + h - ((v - lo) / (hi - lo)) * h).toFixed(1); }
    return d;
  }
  // Flat stylised gameplay backdrop used behind HUD mocks (w x h in px).
  function scene(w, h, o = {}) {
    const hz = h * (o.horizon || 0.46);
    return el('svg', { width: w, height: h, viewBox: `0 0 ${w} ${h}`, style: 'position:absolute;left:0;top:0' }, [
      el('rect', { width: w, height: h, fill: o.sky || '#A9CBDD' }),
      el('path', { d: `M0 ${hz} L${w * 0.12} ${hz - h * 0.12} L${w * 0.27} ${hz - h * 0.03} L${w * 0.4} ${hz - h * 0.16} L${w * 0.55} ${hz - h * 0.05} L${w * 0.72} ${hz - h * 0.14} L${w * 0.88} ${hz - h * 0.04} L${w} ${hz - h * 0.1} L${w} ${hz} Z`, fill: o.hill || '#8FB3A8' }),
      el('rect', { y: hz, width: w, height: h - hz, fill: o.ground || '#6A9777' }),
      o.nopath ? '' : el('path', { d: `M${w * 0.44} ${hz} L${w * 0.56} ${hz} L${w * 0.78} ${h} L${w * 0.22} ${h} Z`, fill: o.path || '#D8CAA6' }),
    ]);
  }
  // Blocky avatar, feet at (x, y), total height hh. Returns SVG group string.
  function avatar(x, y, hh, c = {}) {
    const u = hh / 5, skin = c.skin || '#F2D2A9', top = c.top || '#3E6FB8', leg = c.leg || '#2B3A54', st = c.stroke || '#1A1F2B', sw = c.sw === undefined ? Math.max(1, u * 0.12) : c.sw;
    const r = (rx, ry, rw, rh, f, rr = u * 0.12) => el('rect', { x: (x + rx * u).toFixed(1), y: (y - ry * u).toFixed(1), width: (rw * u).toFixed(1), height: (rh * u).toFixed(1), fill: f, stroke: st, 'stroke-width': sw, rx: rr.toFixed(1) });
    return el('g', {}, [r(-1, 2, 0.95, 2, leg), r(0.05, 2, 0.95, 2, leg), r(-2, 4, 0.95, 2, skin), r(1.05, 4, 0.95, 2, skin), r(-1, 4, 2, 2, top), r(-0.6, 5.2, 1.2, 1.2, skin, u * 0.3)]);
  }

  // Simple item glyphs on a 24 x 24 grid: white fill, dark outline, so they tint and read at small sizes.
  const GLYPH = {
    sword: 'M4 20l2.5-2.5L5 16l2-2 1.5 1.5L18 6l2.5-2.5L21 6l-2.5 2.5L9 18l1.5 1.5-2 2-1.5-1.5L4.5 22z',
    potion: 'M9.5 2h5v2h-1v4.5l4.2 7.6A3.3 3.3 0 0 1 14.8 21H9.2a3.3 3.3 0 0 1-2.9-4.9L10.5 8.5V4h-1z',
    gem: 'M7 4h10l4.5 5.5L12 21 2.5 9.5z',
    shield: 'M12 2.5l8 3v6c0 5-3.4 8.4-8 10-4.6-1.6-8-5-8-10v-6z',
    key: 'M14.5 2.5a6 6 0 1 1-5.3 8.8L3 17.5V21h4v-2h2v-2h2l1.7-1.7a6 6 0 0 1 1.8-12.8zm1.5 4a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
    egg: 'M12 2.5c4 0 7.5 6 7.5 11a7.5 7.5 0 0 1-15 0c0-5 3.5-11 7.5-11z',
    star: 'M12 2l3 6.6 7.2.8-5.4 4.9 1.5 7.1L12 17.8 5.7 21.4l1.5-7.1L1.8 9.4 9 8.6z',
    lock: 'M7 10V7.5a5 5 0 0 1 10 0V10h2v11H5V10zm3 0h4V7.5a2 2 0 0 0-4 0z',
    check: 'M3.5 12.5l3-3 3.5 3.5 7.5-7.5 3 3L10 19z',
    heart: 'M12 21C6 16.5 2.5 13 2.5 8.8A4.8 4.8 0 0 1 12 6.5a4.8 4.8 0 0 1 9.5 2.300C21.5 13 18 16.5 12 21z',
    bolt: 'M13.5 2L5 13.5h5.5L9.5 22 19 10h-5.5z',
    hex: 'M12 2.5l8.200 4.75v9.5L12 21.5l-8.200-4.75v-9.5zM9.5 9.5v5h5v-5z',
  };
  function icon(name, size = 24, fill = '#fff', stroke = '#1A1F2B', sw = 1.6) {
    return el('svg', { width: size, height: size, viewBox: '0 0 24 24', style: 'display:block;flex:none' }, el('path', { d: GLYPH[name], fill, stroke, 'stroke-width': sw, 'stroke-linejoin': 'round', 'fill-rule': 'evenodd' }));
  }
  const RARITY = [['Common', '#6A7382'], ['Uncommon', '#2F9E55'], ['Rare', '#4A98E8'], ['Epic', '#B48BF5'], ['Legendary', '#F0B63A'], ['Mythic', '#FFC0D9']];
  return { RARITY, icon, GLYPH, frame, el, txt, esc, hex, toHex, lum, contrast, grey, oklab, dOk, sim, ease, plot, scene, avatar };
})();
