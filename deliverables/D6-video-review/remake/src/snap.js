// Stills at given times → one contact sheet.  node snap.js upflow 0.5 2 3.6 ...
const { chromium } = require("playwright"); const { execFileSync } = require("child_process");
const FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2";
(async () => {
  const [n, ...ts] = process.argv.slice(2); const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); p.on("pageerror", e => console.log("ERR", e.message));
  await p.goto(`http://127.0.0.1:8777/${n}.html?capture`); await p.waitForSelector("body[data-ready]", { state: "attached" }); await p.waitForTimeout(400);
  const files = [];
  for (const t of ts) { await p.evaluate(t => window.seek(t), +t); const f = `/tmp/snap-${n}-${t}.png`; await p.screenshot({ path: f }); files.push(f); }
  await b.close();
  const cols = Math.min(3, files.length), rows = Math.ceil(files.length / cols);
  const inputs = files.flatMap(f => ["-i", f]);
  const lay = files.map((_, i) => `${(i % cols) * 640}_${Math.floor(i / cols) * 360}`).join("|");
  const sc = files.map((_, i) => `[${i}]scale=640:360[v${i}]`).join(";");
  execFileSync(FF, ["-y", "-loglevel", "error", ...inputs, "-filter_complex", `${sc};${files.map((_, i) => `[v${i}]`).join("")}xstack=inputs=${files.length}:layout=${lay}:fill=black`, `/tmp/sheet-${n}.png`]);
  console.log(`/tmp/sheet-${n}.png`);
})();
