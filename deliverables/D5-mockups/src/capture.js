// Deterministic capture (seek per frame) and encoding.
//   cd deliverables && python3 -m http.server 8765 &
//   NODE_PATH=/opt/node22/lib/node_modules node D5-mockups/src/capture.js [walkthrough|glass|kinetic|founder ...]
// Outputs: walkthrough.mp4 + walkthrough.gif (1440x900 app, ~33s) and loop-<style>.mp4 (1920x1080, one seamless loop).
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs"), path = require("path");
const FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2";
const FPS = 30, OUT = path.join(__dirname, ".."), TMP = process.env.FRAMES || "/tmp/pd-frames";
const B = "http://127.0.0.1:8765/D5-mockups/src/";
const JOBS = {
  walkthrough: { url: B + "app.html?capture", w: 1440, h: 900, dsf: 1 },
  glass: { url: B + "previews/glass.html?capture", w: 1280, h: 720, dsf: 1.5, out: "loop-glass-keynote.mp4" },
  kinetic: { url: B + "previews/kinetic.html?capture", w: 1280, h: 720, dsf: 1.5, out: "loop-kinetic-hype.mp4" },
  founder: { url: B + "previews/founder.html?capture", w: 1280, h: 720, dsf: 1.5, out: "loop-founder-film.mp4" },
};
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(JOBS);
  const b = await chromium.launch();
  for (const n of names) {
    const J = JOBS[n], dir = path.join(TMP, n); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const p = await b.newPage({ viewport: { width: J.w, height: J.h }, deviceScaleFactor: J.dsf });
    p.on("pageerror", e => console.log("ERR", e.message));
    await p.goto(J.url); await p.waitForSelector("body[data-ready]", { state: "attached", timeout: 30000 }); await p.waitForTimeout(300);
    const dur = await p.evaluate(() => window.DUR || window.LOOP);
    const N = Math.round(dur * FPS);
    for (let i = 0; i < N; i++) { await p.evaluate(t => window.seek(t), i / FPS); await p.screenshot({ path: path.join(dir, `f${String(i).padStart(4, "0")}.png`) }); }
    await p.close();
    const inp = ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(dir, "f%04d.png")];
    if (n === "walkthrough") {
      execFileSync(FF, [...inp, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", path.join(OUT, "walkthrough.mp4")]);
      execFileSync(FF, [...inp, "-vf", "fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle", path.join(OUT, "walkthrough.gif")]);
    } else {
      execFileSync(FF, [...inp, "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", path.join(OUT, J.out)]);
    }
    console.log("done", n, N, "frames");
  }
  await b.close();
})();
