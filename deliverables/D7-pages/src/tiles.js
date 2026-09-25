// Cuts the unchanged customer-video tiles out of the live screenshots (../real/) into ../tiles/*.png,
// upscaled 3x with high-quality smoothing, so the AFTER pages show the same real frames as the BEFORE.
// Run from deliverables/D7-pages:  NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node src/tiles.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const OUTD = path.join(ROOT, 'tiles');
fs.mkdirSync(OUTD, { recursive: true });
const H = 'poolday-home-fullpage-live.webp', B = 'poolday-b2b-startups-fullpage-live.webp';
// name: [file, x, y, w, h] in source pixels (media area only, inset past the rounded corners)
const CROPS = {
  'h-marblism': [H, 95, 279, 260, 172], 'h-posthog-ai': [H, 364, 279, 126, 70], 'h-clickup': [H, 634, 279, 124, 70],
  'h-poolday-founder': [H, 364, 383, 126, 68], 'h-oreo': [H, 634, 383, 124, 68], 'h-lovable': [H, 499, 383, 125, 171],
  'h-verde': [H, 95, 486, 125, 69], 'h-smart': [H, 230, 486, 125, 274], 'h-dust': [H, 634, 486, 124, 69],
  'h-braavo': [H, 95, 588, 125, 69], 'h-comm': [H, 364, 589, 126, 184], 'h-woman': [H, 499, 588, 125, 170],
  'h-fullenrich': [H, 634, 588, 124, 69], 'h-posthog-pv': [H, 95, 691, 125, 68], 'h-vybe': [H, 634, 691, 124, 68],
  'h-podcast-man': [H, 95, 806, 125, 60],
  'b-cal': [B, 100, 208, 295, 165], 'b-posthog': [B, 100, 407, 295, 165], 
  'b-aicreator': [B, 404, 208, 203, 366], 'b-plausible': [B, 614, 208, 178, 100], 'b-feature': [B, 614, 341, 178, 100],
  'b-testimonial': [B, 614, 473, 178, 99],
};
const MADE = ['posthog-pv', 'fullenrich', 'stars', 'dust', 'braavo', 'vybe', 'adikteev', 'adjust', 'jev', 'upflow', 'poolday-founder', 'clickup', 'posthog-ai', 'verde', 'marblism', 'oreo'];
MADE.forEach((n, i) => { CROPS['m-' + n] = [B, [100, 275, 451, 627][i % 4], [1247, 1374, 1501, 1628][Math.floor(i / 4)], 165, 92]; });

(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage();
  const tmp = path.join(OUTD, '.cut.html');
  fs.writeFileSync(tmp, `<body><img id=h src="file://${ROOT}/real/${H}"><img id=b src="file://${ROOT}/real/${B}"><canvas id=c></canvas></body>`);
  await p.goto('file://' + tmp); await p.waitForFunction(() => [...document.images].every(i => i.complete));
  for (const [name, [file, x, y, w, h]] of Object.entries(CROPS)) {
    const data = await p.evaluate(([id, x, y, w, h]) => {
      const c = document.getElementById('c'); c.width = w * 3; c.height = h * 3;
      const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      g.drawImage(document.getElementById(id), x, y, w, h, 0, 0, w * 3, h * 3);
      return c.toDataURL('image/png');
    }, [file === H ? 'h' : 'b', x, y, w, h]);
    fs.writeFileSync(path.join(OUTD, name + '.png'), Buffer.from(data.split(',')[1], 'base64'));
  }
  fs.unlinkSync(tmp); await b.close();
  console.log('cut', Object.keys(CROPS).length, 'tiles');
})();
