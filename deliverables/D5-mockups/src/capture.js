// Captures the walkthrough deterministically (seek per frame) and encodes GIF + MP4.
//   NODE_PATH=/opt/node22/lib/node_modules node D5-mockups/src/capture.js
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs"), path = require("path"), os = require("os");
const FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2";
const FPS = 30, DUR = 15, OUT = path.join(__dirname, "..");
const DIR = process.env.FRAMES || fs.mkdtempSync(path.join(os.tmpdir(), "pd-frames-"));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  p.on("pageerror", e => console.log("ERR", e.message));
  await p.goto("http://127.0.0.1:8765/D5-mockups/src/walkthrough.html?capture");
  await p.waitForSelector("body[data-ready]", { state: "attached" }); await p.waitForTimeout(500);
  const only = process.env.ONLY ? process.env.ONLY.split(",").map(Number) : null;
  for (let i = 0; i < FPS * DUR; i++) {
    const t = i / FPS; if (only && !only.includes(i)) continue;
    await p.evaluate(t => window.seek(t), t);
    await p.screenshot({ path: path.join(DIR, `f${String(i).padStart(4, "0")}.png`) });
  }
  await b.close();
  if (only) { console.log(DIR); return; }
  const inp = ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(DIR, "f%04d.png")];
  execFileSync(FF, [...inp, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", path.join(OUT, "walkthrough.mp4")]);
  execFileSync(FF, [...inp, "-vf", "fps=20,scale=1080:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle", path.join(OUT, "walkthrough.gif")]);
  console.log("frames in", DIR);
})();
