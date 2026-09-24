// Renders every page to PNG (full page + above-the-fold, 1440 wide) and builds the
// before/after comparison images with numbered callouts.
// Run from deliverables/D7-pages:
//   NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node src/render.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const R = path.join(ROOT, 'renders');
const CMP = path.join(ROOT, 'compare');
fs.mkdirSync(R, { recursive: true }); fs.mkdirSync(CMP, { recursive: true });

const LEGEND = {
  home: ['"Watch a 2-min build" for visitors not ready to call', 'Video feed regrouped: 4 use-case rows, uniform tiles, one caption each', 'A demo CTA right after the proof grid', '"Superintelligence" defined in one line', 'Customers and investors split', 'What happens in the 15 minutes'],
  b2b: ['H1 says who it is for and the job', '"Paste your URL" free launch video (D5), tagged "Free · limited"', 'Real B2B customer logos in the first screen', 'Input-to-output use cases, launch video first', '"Human-made" claim backed by named videos', 'Onboarding and 95% autonomy as facts', 'Closing line says what happens on the call'],
  pricing: ['Credits translated into videos per month', '"Your first month at $600 · no lock-in"', 'Customer logos under the plans', 'Short comparison vs agency, freelancer, in-house', 'One-line procurement note', 'Four-question FAQ'],
};
const TITLE = { home: 'poolday.ai — Home', b2b: 'poolday.ai/solutions/b2b-startups', pricing: 'poolday.ai/pricing' };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await ctx.route(/^https?:\/\//, r => r.abort()); // offline: fonts are local, poolday.ai is never fetched
  const page = await ctx.newPage();
  async function shot(name, query, outBase) {
    await page.goto('file://' + path.join(ROOT, 'pages', name + '.html') + (query || ''));
    await page.waitForSelector('body[data-ready="1"]');
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(R, outBase + '.png'), fullPage: true });
    await page.screenshot({ path: path.join(R, outBase + '-fold.png'), clip: { x: 0, y: 0, width: 1440, height: 900 } });
  }
  for (const p of ['home', 'b2b', 'pricing']) {
    await shot(p + '-before', '', p + '-before');
    await shot(p + '-after', '', p + '-after');
    await shot(p + '-after', '?annotate', p + '-after-annotated');
  }
  // Comparison sheets
  for (const p of Object.keys(LEGEND)) {
    for (const mode of ['full', 'fold']) {
      const suf = mode === 'fold' ? '-fold' : '';
      const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;src:url('file://${ROOT}/src/fonts/inter-latin.woff2');font-weight:100 900}
body{margin:0;background:#0a0a0a;color:#f5f5f5;font-family:Inter,sans-serif;padding:48px}
h1{margin:0 0 6px;font-size:34px;font-weight:500;letter-spacing:-.02em}.sub{color:#939393;font-size:16px;margin-bottom:32px}
.row{display:grid;grid-template-columns:720px 720px 420px;gap:28px;align-items:start}
.col h2{margin:0 0 12px;font-size:15px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#939393}.col.after h2{color:#f5f5f5}
.col img{width:720px;display:block;border-radius:10px}
.leg{position:sticky;top:0}.leg h2{margin:0 0 16px;font-size:15px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#939393}
.it{display:flex;gap:14px;align-items:flex-start;margin-bottom:16px;font-size:19px;line-height:1.35}
.n{flex:none;width:32px;height:32px;border-radius:50%;background:#06b6d4;color:#000;font-weight:700;font-size:16px;line-height:32px;text-align:center}
.note{margin-top:28px;font-size:14px;line-height:1.5;color:#939393}</style></head><body>
<h1>${TITLE[p]}: before and after${mode === 'fold' ? ' (above the fold)' : ''}</h1><div class="sub">1440px wide, shown at 50%. Before = reconstruction from reported copy and the brand-kit audit. Goal: more demos booked.</div>
<div class="row"><div class="col"><h2>Before · reconstruction</h2><img src="file://${R}/${p}-before${suf}.png"></div>
<div class="col after"><h2>After · proposed</h2><img src="file://${R}/${p}-after-annotated${suf}.png"></div>
<div class="leg"><h2>Changes (page order)</h2>${LEGEND[p].map((t, i) => `<div class="it"><span class="n">${i + 1}</span><span>${t}</span></div>`).join('')}<p class="note">Detail, copy and A/B tests: D7-page-review.md.</p></div></div></body></html>`;
      const f = path.join(CMP, `.${p}${suf}.html`);
      fs.writeFileSync(f, html);
      const cp = await ctx.newPage();
      await cp.setViewportSize({ width: 2040, height: 300 });
      await cp.goto('file://' + f); await cp.waitForLoadState('load'); await cp.evaluate(() => document.fonts.ready);
      await cp.screenshot({ path: path.join(CMP, `${p}-compare${suf}.png`), fullPage: true });
      await cp.close(); fs.unlinkSync(f);
    }
  }
  await browser.close();
  console.log('rendered');
})();
