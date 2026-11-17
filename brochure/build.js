// Builds the Ray2Volt brochure: src/pages/*.html -> one HTML file -> PDF (+ PNG previews).
// Usage: node build.js [--png] [--only=07,08]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = __dirname;
const src = path.join(root, 'src');
const only = (process.argv.slice(2).find(a => a.startsWith('--only=')) || '').replace('--only=', '').split(',').filter(Boolean);
// With --only, build just those pages into a private temp file (safe to run in parallel) and skip the PDF.
const out = only.length ? path.join(root, 'preview', `.tmp-${only.join('-')}.html`) : path.join(root, 'Ray2Volt-Solar-Brochure.html');
const pdf = path.join(root, 'Ray2Volt-Solar-Brochure.pdf');
const prev = path.join(root, 'preview');
const args = process.argv.slice(2);
const wantPng = args.includes('--png');

const b64 = f => fs.readFileSync(f).toString('base64');
const TITLE = 'Solar &amp; Green Energy, Explained';

function assemble(inline) {
  let fonts = fs.readFileSync(path.join(root, 'fonts/fonts.css'), 'utf8');
  fonts = fonts.replace(/url\(([^)]+\.woff2)\)/g, (m, f) =>
    inline ? `url(data:font/woff2;base64,${b64(path.join(root, 'fonts', f))})` : `url(fonts/${f})`);
  const css = fs.readFileSync(path.join(src, 'base.css'), 'utf8');
  const sprite = fs.readFileSync(path.join(src, 'sprite.svg'), 'utf8');
  const logo = `data:image/png;base64,${b64(path.join(root, '..', 'images', 'logo.png'))}`;
  const hero = `data:image/jpeg;base64,${b64(path.join(root, '..', 'images', 'hero-solar.png'))}`;
  const files = fs.readdirSync(path.join(src, 'pages')).filter(f => f.endsWith('.html')).sort().filter(f => !only.length || only.some(o => f.startsWith(o)));
  const pages = files.map(f => {
    let h = fs.readFileSync(path.join(src, 'pages', f), 'utf8');
    return h.replace(/\{\{LOGO\}\}/g, logo)
            .replace(/\{\{HERO\}\}/g, hero)
            .replace(/\{\{PN\}\}/g, f.slice(0, 2))
            .replace(/\{\{FOOT\}\}/g, `Ray2Volt Solar &nbsp;·&nbsp; ${TITLE}`)
            .replace(/<section class="page/, `<section data-file="${f}" class="page`);
  });
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ray2Volt Solar — Solar &amp; Green Energy, Explained</title>
<style>${fonts}\n${css}</style></head><body>\n${sprite}\n${pages.join('\n')}\n</body></html>`;
}

(async () => {
  fs.mkdirSync(prev, { recursive: true });
  fs.writeFileSync(out, assemble(true));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await page.goto('file://' + out);
  await page.evaluate(() => document.fonts.ready);

  // Overflow check: anything spilling out of its page or its page body is reported.
  const problems = await page.evaluate(() => {
    const res = [];
    document.querySelectorAll('.page').forEach(p => {
      const f = p.dataset.file; const pr = p.getBoundingClientRect();
      const pb = p.querySelector('.pb');
      if (pb) {
        const br = pb.getBoundingClientRect();
        let maxB = 0, maxR = 0;
        pb.querySelectorAll('*').forEach(e => { if (e.closest('svg') && e.tagName !== 'svg') return; const r = e.getBoundingClientRect(); if (r.width === 0) return; maxB = Math.max(maxB, r.bottom); maxR = Math.max(maxR, r.right); });
        if (maxB > br.bottom + 1) res.push(`${f}: content overflows page body by ${Math.round(maxB - br.bottom)}px (vertical)`);
        if (maxR > pr.right - 40) res.push(`${f}: content overflows right margin by ${Math.round(maxR - (pr.right - 40))}px`);
        const last = pb.lastElementChild; if (last) { const gap = br.bottom - last.getBoundingClientRect().bottom; if (gap > 60) res.push(`${f}: ${Math.round(gap)}px of empty space at the bottom of the page`); }
      }
      // SVG text spilling outside its viewBox
      p.querySelectorAll('svg').forEach((s, i) => { const sr = s.getBoundingClientRect(); s.querySelectorAll('text').forEach(t => { const r = t.getBoundingClientRect(); if (r.left < sr.left - 1 || r.right > sr.right + 1 || r.top < sr.top - 1 || r.bottom > sr.bottom + 1) res.push(`${f}: svg#${i} text "${t.textContent.trim().slice(0, 30)}" spills outside the svg`); }); });
    });
    return res;
  });
  console.log(problems.length ? 'LAYOUT PROBLEMS:\n' + problems.join('\n') : 'Layout check: OK');

  if (!only.length) { await page.pdf({ path: pdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  console.log('PDF:', pdf, Math.round(fs.statSync(pdf).size / 1024) + ' KB'); }

  if (wantPng) {
    const els = await page.$$('.page');
    for (const el of els) {
      const f = (await el.getAttribute('data-file')).replace('.html', '');
      await el.screenshot({ path: path.join(prev, f + '.png') });
    }
    console.log('Previews written to', prev);
  }
  await browser.close();
})();
