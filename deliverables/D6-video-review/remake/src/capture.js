// Frame-exact capture with real motion blur (3 sub-frames per output frame, averaged).
//   cd deliverables/D6-video-review/remake/src && python3 -m http.server 8777 &
//   NODE_PATH=/opt/node22/lib/node_modules node capture.js upflow posthog
// Output: ../upflow-remake.mp4, ../posthog-remake.mp4 (1920x1080, 30 fps)
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs"), path = require("path");
const FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2";
const FPS = 30, SUB = +(process.env.SUB || 3), TMP = process.env.FRAMES || "/tmp/d6-frames";
const ONLY = process.env.ONLY; // "a-b" seconds, for quick checks
(async () => {
  const names = process.argv.slice(2);
  const b = await chromium.launch();
  for (const n of names) {
    const dir = path.join(TMP, n); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on("pageerror", e => console.log("ERR", e.message));
    await p.goto(`http://127.0.0.1:8777/${n}.html?capture`);
    await p.waitForSelector("body[data-ready]", { state: "attached", timeout: 30000 });
    await p.waitForTimeout(500);
    const dur = await p.evaluate(() => window.DUR);
    let [a, z] = ONLY ? ONLY.split("-").map(Number) : [0, dur];
    const N = Math.round((z - a) * FPS * SUB);
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => window.seek(t), a + i / (FPS * SUB));
      await p.screenshot({ path: path.join(dir, `f${String(i).padStart(5, "0")}.png`) });
    }
    await p.close();
    const out = path.join(__dirname, "..", `${n}-remake${ONLY ? "-part" : ""}.mp4`);
    const blur = SUB > 1 ? `tmix=frames=${SUB},select='not(mod(n+1\\,${SUB}))',` : "";
    execFileSync(FF, ["-y", "-loglevel", "error", "-framerate", String(FPS * SUB), "-i", path.join(dir, "f%05d.png"),
      "-vf", `${blur}setpts=N/${FPS}/TB`, "-r", String(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
      "-preset", "slow", "-movflags", "+faststart", out]);
    console.log("done", n, N, "sub-frames →", out);
  }
  await b.close();
})();
