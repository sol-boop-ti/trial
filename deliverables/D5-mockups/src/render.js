// Renders every screen to PNG (1x and 2x). Usage:
//   cd deliverables && python3 -m http.server 8765 &
//   NODE_PATH=/opt/node22/lib/node_modules node D5-mockups/src/render.js [name-filter]
const { chromium } = require("playwright");
const path = require("path");
const BASE = "http://127.0.0.1:8765/D5-mockups/src/";
const OUT = path.join(__dirname, "..");
const SHOTS = [
  { name: "01-landing", url: "01-landing.html", w: 1440, h: 900 },
  { name: "01-landing-mobile", url: "01-landing.html", w: 390, h: 844, mobile: true },
  { name: "01b-landing-product-ad", url: "01-landing.html?tab=ad&img=1&v=lumenbottle.com", w: 1440, h: 900 },
  { name: "02-style", url: "02-style.html", w: 1440, h: 900 },
  { name: "02b-style-podcast", url: "02b-style-podcast.html", w: 1440, h: 900 },
  { name: "03-generating", url: "03-generating.html", w: 1440, h: 900 },
  { name: "04-result", url: "04-result.html", w: 1440, h: 900 },
];
(async () => {
  const filter = process.argv[2];
  const browser = await chromium.launch();
  for (const s of SHOTS) {
    if (filter && !s.name.includes(filter)) continue;
    for (const scale of [1, 2]) {
      const ctx = await browser.newContext({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: scale, isMobile: !!s.mobile, hasTouch: !!s.mobile });
      const page = await ctx.newPage();
      await page.goto(BASE + s.url + (s.url.includes("?") ? "&" : "?") + "still=1");
      await page.waitForSelector("body[data-ready]", { state: "attached" });
      await page.waitForTimeout(400);
      // Freeze ambient loops at a pleasant point so stills are deterministic.
      await page.evaluate(() => document.getAnimations().forEach(a => { a.pause(); a.currentTime = 1800; }));
      await page.screenshot({ path: path.join(OUT, `${s.name}${scale === 2 ? "@2x" : ""}.png`) });
      await ctx.close();
    }
    console.log("rendered", s.name);
  }
  await browser.close();
})();
