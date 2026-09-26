// D7 round 4 renders. BEFORE = the live screenshots in ../real/ (cropped, converted to PNG).
// AFTER = our pages at 1440 wide (animations frozen on a representative frame via ?still).
// Also records the animated sections to MP4 (needs FFMPEG env var pointing to an ffmpeg with libx264).
// Run from deliverables/D7-pages:
//   NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers FFMPEG=/path/to/ffmpeg node src/render.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const ROOT = path.join(__dirname, '..');
const R = path.join(ROOT, 'renders'), CMP = path.join(ROOT, 'compare'), VID = path.join(ROOT, 'video');
for (const d of [R, CMP, VID]) fs.mkdirSync(d, { recursive: true });

// Live screenshots: [file, crop {x,y,w,h} for the full view, fold height in source px]
const LIVE = {
  home: ['poolday-home-fullpage-live.webp', { x: 0, y: 0, w: 854, h: 2000 }, 534],
  b2b: ['poolday-b2b-startups-fullpage-live.webp', { x: 0, y: 0, w: 892, h: 2000 }, 558],
  pricing: ['poolday-pricing-live.webp', { x: 0, y: 210, w: 2000, h: 1091 }, 1091],
};
const LEGEND = {
  home: ['"Watch a 2-min build" next to the hero CTA', 'Masonry feed regrouped: 4 use-case rows, uniform tiles, one caption bar each', '"Meet Poolday." gets a one-line definition', '"Book a 15 min demo" right after Meet Poolday', 'Customers and investors split in the logo wall', 'CTA card says what happens in the 15 minutes'],
  b2b: ['H1 names the job: "Every feature you ship, on video."', '"Paste your URL" free launch video with a NEW sticker (replaces "View examples")', 'Real B2B customer logos in the first screen', 'Use-case cards get animated input-to-output previews'],
  pricing: ['Framed credits box: "$1,250 in credits · ≈ 50–250 finished videos"', '"Your first month at $600 · no lock-in"', 'Customer logos under the plans', 'Short comparison vs agency, freelancer, in-house', 'Four-question FAQ'],
};
const TITLE = { home: 'poolday.ai — Home', b2b: 'poolday.ai/solutions/b2b-startups', pricing: 'poolday.ai/pricing' };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await ctx.route(/^https?:\/\//, r => r.abort());
  const page = await ctx.newPage();

  // 1. BEFORE: live screenshots -> PNG (full + fold)
  for (const [k, [file, c, foldH]] of Object.entries(LIVE)) {
    for (const [suf, h] of [['', c.h], ['-fold', foldH]]) {
      await page.setViewportSize({ width: c.w, height: h });
      const tmp = path.join(R, '.live-crop.html');
      fs.writeFileSync(tmp, `<body style="margin:0;background:#000"><div style="width:${c.w}px;height:${h}px;overflow:hidden;position:relative"><img src="file://${ROOT}/real/${file}" style="position:absolute;left:${-c.x}px;top:${-c.y}px"></div></body>`);
      await page.goto('file://' + tmp);
      await page.waitForFunction(() => document.images[0].complete);
      await page.screenshot({ path: path.join(R, `${k}-before-live${suf}.png`), clip: { x: 0, y: 0, width: c.w, height: h } });
      fs.unlinkSync(tmp);
    }
  }
  await page.setViewportSize({ width: 1440, height: 900 });

  // 2. AFTER renders
  async function shot(name, query, outBase) {
    await page.goto('file://' + path.join(ROOT, 'pages', name + '.html') + query);
    await page.waitForSelector('body[data-ready="1"]'); await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(R, outBase + '.png'), fullPage: true });
    await page.screenshot({ path: path.join(R, outBase + '-fold.png'), clip: { x: 0, y: 0, width: 1440, height: 900 } });
  }
  for (const p of Object.keys(LEGEND)) {
    await shot(p + '-after', '?still', p + '-after');
    await shot(p + '-after', '?still&annotate', p + '-after-annotated');
  }

  // 3. Comparison sheets
  for (const p of Object.keys(LEGEND)) for (const suf of ['', '-fold']) {
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;src:url('file://${ROOT}/src/fonts/inter-latin.woff2');font-weight:100 900}
body{margin:0;background:#0a0a0a;color:#f5f5f5;font-family:Inter,sans-serif;padding:48px}
h1{margin:0 0 6px;font-size:34px;font-weight:500;letter-spacing:-.02em}.sub{color:#939393;font-size:16px;margin-bottom:32px}
.row{display:grid;grid-template-columns:720px 720px 420px;gap:28px;align-items:start}
.col h2,.leg h2{margin:0 0 12px;font-size:15px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#939393}.col.after h2{color:#f5f5f5}
.col img{width:720px;display:block;border-radius:10px}
.it{display:flex;gap:14px;align-items:flex-start;margin-bottom:16px;font-size:19px;line-height:1.35}
.n{flex:none;width:32px;height:32px;border-radius:50%;background:#06b6d4;color:#000;font-weight:700;font-size:16px;line-height:32px;text-align:center}
.note{margin-top:28px;font-size:14px;line-height:1.5;color:#939393}</style></head><body>
<h1>${TITLE[p]}: before and after${suf ? ' (above the fold)' : ''}</h1><div class="sub">Before = the live page (my screenshot). After = my rebuild at 1440px. Both shown at 720px wide. Goal: more demos booked.</div>
<div class="row"><div class="col"><h2>Before · live page, screenshot</h2><img src="file://${R}/${p}-before-live${suf}.png"></div>
<div class="col after"><h2>After · proposed</h2><img src="file://${R}/${p}-after-annotated${suf}.png"></div>
<div class="leg"><h2>Changes (page order)</h2>${LEGEND[p].map((t, i) => `<div class="it"><span class="n">${i + 1}</span><span>${t}</span></div>`).join('')}<p class="note">Everything without a number is the live page, kept. Detail, copy and A/B tests: D7-page-review.md.</p></div></div></body></html>`;
    const f = path.join(CMP, `.${p}${suf}.html`); fs.writeFileSync(f, html);
    const cp = await ctx.newPage(); await cp.setViewportSize({ width: 2040, height: 300 });
    await cp.goto('file://' + f); await cp.waitForLoadState('load'); await cp.evaluate(() => document.fonts.ready);
    await cp.screenshot({ path: path.join(CMP, `${p}-compare${suf}.png`), fullPage: true });
    await cp.close(); fs.unlinkSync(f);
  }
  await browser.close();

  // 4. Animated previews -> MP4 (webm recorded by Playwright, converted with ffmpeg)
  const FF = process.env.FFMPEG;
  if (FF) {
    const clips = [
      ['b2b-after-scroll', 'b2b-after', '.ucgrid', 'scroll'],
      ['b2b-use-cases', 'b2b-after', '.ucgrid', 'hold'],
      ['home-meet-poolday', 'home-after', '.meet', 'hold'],
    ];
    for (const [out, pg, sel, mode] of clips) {
      const vb = await chromium.launch();
      const vctx = await vb.newContext({ viewport: { width: 1440, height: 900 }, recordVideo: { dir: VID, size: { width: 1440, height: 900 } } });
      await vctx.route(/^https?:\/\//, r => r.abort());
      const vp = await vctx.newPage();
      await vp.goto('file://' + path.join(ROOT, 'pages', pg + '.html'));
      await vp.waitForSelector('body[data-ready="1"]');
      const top = await vp.evaluate((s) => document.querySelector(s).getBoundingClientRect().top + scrollY, sel);
      if (mode === 'scroll') {
        for (let y = 0; y <= top + 250; y += 18) { await vp.evaluate((yy) => scrollTo(0, yy), y); await vp.waitForTimeout(33); }
        await vp.waitForTimeout(5500);
      } else {
        await vp.evaluate((yy) => scrollTo(0, yy), top - (sel === '.meet' ? 40 : 80)); await vp.waitForTimeout(10500);
      }
      const webm = await vp.video().path(); await vctx.close(); await vb.close();
      execFileSync(FF, ['-y', '-loglevel', 'error', '-i', webm, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', '-movflags', '+faststart', path.join(VID, out + '.mp4')]);
      fs.unlinkSync(webm);
    }
    console.log('videos done');
  }
  console.log('rendered');
})();
