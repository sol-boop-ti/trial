// Renders every still (1x and @2x) from the live app, by seeking its timeline.
//   cd deliverables && python3 -m http.server 8765 &
//   NODE_PATH=/opt/node22/lib/node_modules node D5-mockups/src/render.js [name-filter]
const { chromium } = require("playwright");
const path = require("path");
const BASE = "http://127.0.0.1:8765/D5-mockups/src/app.html?capture&nocursor";
const OUT = path.join(__dirname, "..");
const L0 = 13.45, G = L0 + 5.85, R0 = G + 13.9 + 0.05; // must match scriptLaunch() in app.js
const SHOTS = [
  { name: "01-link", t: 2.6 },
  { name: "01-link-mobile", t: 2.6, w: 390, h: 844, mobile: true },
  { name: "01b-link-product-ad", t: 2.6, script: "ad" },
  { name: "02-recording", t: 5.6 },
  { name: "02b-recording-chosen", t: 6.3 },
  { name: "03-brand-kit", t: 8.35 },
  { name: "04-style", t: 12.9 },
  { name: "04b-style-podcast", t: 1.6, script: "podcast" },
  { name: "04c-details-personal-email-rejected", t: L0 + 2.3 },
  { name: "04d-details", t: L0 + 5.4 },
  { name: "05-generating-recording", t: G + 3.3 },
  { name: "05b-generating-brand-kit", t: G + 6.6 },
  { name: "05c-generating-storyboard", t: G + 11.25 },
  { name: "06-result", t: R0 + 1.2 },
  { name: "06b-result-share", t: R0 + 3.6 },
];
(async () => {
  const filter = process.argv[2];
  const browser = await chromium.launch();
  for (const s of SHOTS) {
    if (filter && !s.name.includes(filter)) continue;
    for (const scale of [1, 2]) {
      const ctx = await browser.newContext({ viewport: { width: s.w || 1440, height: s.h || 900 }, deviceScaleFactor: scale, isMobile: !!s.mobile, hasTouch: !!s.mobile });
      const page = await ctx.newPage();
      await page.goto(BASE + (s.script ? "&script=" + s.script : ""));
      await page.waitForSelector("body[data-ready]", { state: "attached", timeout: 30000 });
      // Play into the moment so smoothed states (hover, trails) are what the walkthrough shows.
      await page.evaluate(async (T) => { for (let t = Math.max(0, T - 1.2); t <= T + 1e-6; t += 1 / 30) window.seek(t); window.seek(T); }, s.t);
      await page.waitForTimeout(150);
      await page.screenshot({ path: path.join(OUT, `${s.name}${scale === 2 ? "@2x" : ""}.png`) });
      await ctx.close();
    }
    console.log("rendered", s.name);
  }
  await browser.close();
})();
