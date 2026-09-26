// Frame-exact capture, 4 parallel workers, real motion blur (180° shutter: SUBS samples
// spread over the first half of each frame interval, averaged), then the soundtrack is muxed.
//   cd deliverables/D6-video-review/remake/src && python3 -m http.server 8777 &
//   NODE_PATH=/opt/node22/lib/node_modules node capture.js upflow posthog
// Env: SUBS (samples per frame, default 5), WORKERS (default 4), ONLY="a-b" (seconds, preview part)
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs"), path = require("path");
const FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2";
const FPS = 30, SUBS = +(process.env.SUBS || 5), WORKERS = +(process.env.WORKERS || 4), TMP = process.env.FRAMES || "/tmp/d6-frames";
const ONLY = process.env.ONLY, SHUTTER = 0.5;
(async () => {
  const b = await chromium.launch();
  for (const n of process.argv.slice(2)) {
    const dir = path.join(TMP, n); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const open = async () => {
      const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on("pageerror", e => console.log("ERR", e.message));
      await p.goto(`http://127.0.0.1:8777/${n}.html?capture`);
      await p.waitForSelector("body[data-ready]", { state: "attached", timeout: 60000 });
      await p.waitForTimeout(600);
      return p;
    };
    const first = await open();
    const { dur, cues } = await first.evaluate(() => ({ dur: window.DUR, cues: window.CUES || [] }));
    const [a, z] = ONLY ? ONLY.split("-").map(Number) : [0, dur];
    const F = Math.round((z - a) * FPS), jobs = [];
    for (let f = 0; f < F; f++) for (let k = 0; k < SUBS; k++) jobs.push([f * SUBS + k, a + (f + (SUBS > 1 ? k / (SUBS - 1) * SHUTTER : 0)) / FPS]);
    const pages = [first, ...(await Promise.all(Array.from({ length: WORKERS - 1 }, open)))];
    let next = 0, doneN = 0; const t0 = Date.now();
    await Promise.all(pages.map(async p => {
      while (next < jobs.length) {
        const [i, t] = jobs[next++];
        await p.evaluate(t => window.seek(t), t);
        await p.screenshot({ path: path.join(dir, `f${String(i).padStart(6, "0")}.jpg`), type: "jpeg", quality: 94 });
        if (++doneN % 600 === 0) console.log(n, doneN, "/", jobs.length, Math.round((Date.now() - t0) / 1000) + "s");
      }
      await p.close();
    }));
    const base = path.join(__dirname, "..", `${n}-remake${ONLY ? "-part" : ""}`);
    const vf = `${SUBS > 1 ? `tmix=frames=${SUBS},select='not(mod(n+1\\,${SUBS}))',` : ""}setpts=N/${FPS}/TB`;
    execFileSync(FF, ["-y", "-loglevel", "error", "-framerate", String(FPS * SUBS), "-i", path.join(dir, "f%06d.jpg"),
      "-vf", vf, "-r", String(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "15", "-preset", "slow", base + "-silent.mp4"]);
    // soundtrack from the page's cue list
    fs.writeFileSync(base + "-cues.json", JSON.stringify({ dur, cues, start: a, end: z }));
    execFileSync("python3", [path.join(__dirname, "sound.py"), base + "-cues.json", base + ".wav"]);
    execFileSync(FF, ["-y", "-loglevel", "error", "-i", base + "-silent.mp4", "-i", base + ".wav", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
      "-shortest", "-movflags", "+faststart", base + ".mp4"]);
    fs.rmSync(base + "-silent.mp4"); fs.rmSync(base + ".wav"); fs.rmSync(base + "-cues.json");
    console.log("done", n, jobs.length, "samples →", base + ".mp4", Math.round((Date.now() - t0) / 1000) + "s");
  }
  await b.close();
})();
