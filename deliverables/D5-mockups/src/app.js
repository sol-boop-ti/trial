// Poolday lead-magnet flow (v2): one page, six steps, one clock.
// Everything visible is a pure function of time + an event list, so the same code runs
//   - live (real clicks append events at "now"),
//   - as a looping scripted demo (?demo), and
//   - frame-accurate for capture (?capture: the host calls window.seek(t)).
// Curves come from lib/motion.js (motion manual): exponential settles, staggered births,
// ink tied to motion, alive holds. No CSS default eases on anything choreographed.
(() => {
const { clamp, lerp, seg, fr, expo, ink, out3, out5, in3, inOut3, spring, rnd } = M;
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const Q = new URLSearchParams(location.search);
const CAPTURE = Q.has("capture"), DEMO = CAPTURE || Q.has("demo");
const SCRIPT = Q.get("script") || "launch";
if (DEMO && !Q.has("nocursor")) document.documentElement.classList.add("demo");

// ---------------------------------------------------------------- steps + labels
const STEP = { "s-link": [1, "Product & link"], "s-rec": [2, "Screen recording"], "s-kit": [3, "Brand kit"], "s-style": [4, "Style"], "s-gen": [5, "Generating"], "s-res": [6, "Your video"], "s-pod": [2, "Clip style"] };

// ---------------------------------------------------------------- event model
let EV = [];                      // {t, type, ...}
const push = (e) => { EV.push(e); EV.sort((a, b) => a.t - b.t); };
const last = (t, type, f) => { let r = null; for (const e of EV) { if (e.t > t) break; if (e.type === type && (!f || f(e))) r = e; } return r; };
const all = (t, type) => EV.filter(e => e.type === type && e.t <= t);
// A click = press feedback + a progress tick + the action.
function click(t, sel, fill, action) {
  push({ t, type: "press", sel });
  if (fill) push({ t: t + 0.03, type: "fill", d: fill });
  if (action) push({ t: t + 0.04, ...action });
}

// ---------------------------------------------------------------- scripted walkthroughs
const GEN = [ // phase, start, end, status label
  ["open", 0, 1.5, "Opening northwind.ai"], ["record", 1.5, 5.3, "AI is recording a walkthrough of your SaaS"],
  ["brand", 5.3, 7.4, "Extracting the brand kit"], ["script", 7.4, 8.8, "Writing the script"], ["voice", 8.8, 10.0, "Recording the voice-over"],
  ["board", 10.0, 12.4, "Storyboarding"], ["render", 12.4, 13.8, "Rendering 1080p"]];
const GEN_DUR = 13.9;
let CURSOR = [], DUR = 33, INIT = {};

function scriptLaunch(product = "launch", url = "northwind.ai") {
  EV = []; INIT = { product: null, url: "" };
  push({ t: 0, type: "go", to: "s-link" });
  click(1.05, `.tab[data-tab=${product}]`, 4, { type: "tab", tab: product });
  click(1.55, "#input", 4, { type: "focus" });
  push({ t: 1.66, type: "type", text: url, per: 0.05 });
  click(3.0, "#go1", 8, { type: "go", to: "s-rec" });
  // S2: glance at upload, then the AI option; hover builds, press, burst.
  click(5.8, "#rec-ai", 14, { type: "choose", q: "rec", v: "ai" });
  push({ t: 6.75, type: "go", to: "s-kit" });
  click(8.55, "#kit-ai", 14, { type: "choose", q: "kit", v: "ai" });
  push({ t: 9.5, type: "go", to: "s-style" });
  click(12.15, '.card[data-i="0"]', 6, { type: "select", i: 0 });
  click(13.2, "#go4", 8, { type: "go", to: "s-gen" });
  push({ t: 13.5, type: "gen" });
  push({ t: 13.5 + GEN_DUR + 0.05, type: "go", to: "s-res" });
  click(30.9, "#book", 0, { type: "book" });
  DUR = 33;
  CURSOR = [[0, [1080, 760]], [0.45, [1080, 760]], [0.98, `.tab[data-tab=${product}]`], [1.2, `.tab[data-tab=${product}]`], [1.5, ["#input", -170, 2]],
    [2.45, ["#input", -150, 4]], [2.9, "#go1"], [3.2, "#go1"], [3.7, ["#rec-up", 40, 30]], [4.35, ["#rec-up", 10, 10]], [4.6, ["#rec-up", 0, 0]],
    [5.15, ["#rec-ai", -40, 60]], [5.45, ["#rec-ai", 30, 70]], [5.78, ["#rec-ai", 36, 72]], [6.3, ["#rec-ai", 44, 80]],
    [7.2, ["#kit-ai", 160, 190]], [7.95, ["#kit-ai", 20, 60]], [8.52, ["#kit-ai", 30, 64]], [9.1, ["#kit-ai", 40, 70]],
    [10.0, [900, 700]], [10.8, ['.card[data-i="0"] .pv', 60, 40]], [11.6, ['.card[data-i="0"] .pv', 80, 34]], [12.12, ['.card[data-i="0"] .pv', 84, 30]],
    [12.5, ['.card[data-i="0"] .pv', 90, 34]], [13.05, "#go4"], [13.4, "#go4"],
    [27.6, [1010, 560]], [28.3, [1010, 560]], [29.6, ["#book", 30, 4]], [30.85, ["#book", 34, 3]], [33, ["#book", 36, 4]]];
  HIDE_CURSOR = [[13.45, 27.75]];
}
function scriptPodcast() {
  EV = []; INIT = { product: "podcast", url: "youtu.be/op-hour-212" };
  push({ t: 0, type: "fill", d: 16, instant: true });
  push({ t: 0, type: "go", to: "s-pod" });
  push({ t: 0, type: "select", i: 0 });
  CURSOR = [[0, [1080, 760]]]; HIDE_CURSOR = [[0, 999]]; DUR = 10;
}
let HIDE_CURSOR = [];

// ---------------------------------------------------------------- derived state
function screenAt(t) { const g = last(t, "go"); const prev = g ? last(g.t - 1e-6, "go") : null; return { cur: g ? g.to : "s-link", te: g ? g.t : 0, prev: prev ? prev.to : null }; }
function productAt(t) { const e = last(t, "tab"); return e ? e.tab : INIT.product; }

// ---------------------------------------------------------------- geometry (resolved once, untransformed)
const R = {};
function rectOf(sel) { if (R[sel]) return R[sel]; const el = typeof sel === "string" ? $(sel) : sel; const r = el.getBoundingClientRect(); return (R[sel] = { x: r.left, y: r.top, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }); }
function pt(p) { if (Array.isArray(p) && typeof p[0] === "number") return { x: p[0], y: p[1] };
  const [sel, dx, dy] = Array.isArray(p) ? p : [p, 0, 0]; const r = rectOf(sel); return { x: r.cx + dx, y: r.cy + dy }; }
function cursorAt(t) {
  const K = CURSOR; if (!K.length) return { x: -99, y: -99 };
  for (let i = 0; i < K.length - 1; i++) { const [t0, a] = K[i], [t1, b] = K[i + 1];
    if (t <= t1) { const k = inOut3(seg(t, t0, t1)), A = pt(a), B = pt(b);
      const arc = Math.sin(k * Math.PI) * Math.min(40, Math.hypot(B.x - A.x, B.y - A.y) * 0.08); // slight human arc
      return { x: lerp(A.x, B.x, k) + arc * 0.4, y: lerp(A.y, B.y, k) - arc }; } }
  return pt(K[K.length - 1][1]);
}

// ---------------------------------------------------------------- hover (virtual cursor or real pointer), smoothed
let POINTER = { x: -99, y: -99 }, lastT = null;
const H = new Map();
function hoverUpdate(t, cur, scr) {
  const dt = lastT == null ? 1 : t - lastT;
  $$("[data-hover]", $("#" + scr)).concat($$("[data-hover]", $(".topbar"))).forEach(el => {
    const r = el.getBoundingClientRect(); const inside = cur.x >= r.left && cur.x <= r.right && cur.y >= r.top && cur.y <= r.bottom;
    const prev = H.get(el) ?? 0, target = inside ? 1 : 0;
    const k = dt < 0 || dt > 0.25 ? 1 : 1 - Math.pow(target > prev ? 0.72 : 0.8, dt * 30); // fast in, softer out
    const h = prev + (target - prev) * k; H.set(el, h); el.style.setProperty("--h", h.toFixed(3));
  });
}
function pressAmt(t, sel) { const e = last(t, "press", e => e.sel === sel); if (!e) return 0; const u = t - e.t;
  return u < 0.05 ? out3(u / 0.05) : u < 0.13 ? 1 : 1 - out3(seg(u, 0.13, 0.3)); }

// ---------------------------------------------------------------- progress bar
function progressAt(t) {
  let p = 0, glow = 0, sheenT = null;
  for (const e of all(t, "fill")) { const tau = fr(t, e.t); p += e.instant ? e.d : e.d * expo(tau, 0.82);
    const u = t - e.t; const g = (u < 0.06 ? u / 0.06 : Math.exp(-(u - 0.06) / 0.5)) * Math.min(1, e.d / 8); glow = Math.max(glow, g); if (!e.instant) sheenT = e.t; }
  const gs = last(t, "gen"); if (gs) { const u = t - gs.t; p += 42 * genP(u);
    for (const [, , b] of GEN) { const v = u - b; if (v >= 0 && v < 1.2) glow = Math.max(glow, (v < 0.06 ? v / 0.06 : Math.exp(-(v - 0.06) / 0.45)) * 0.7); if (v >= 0 && v < 0.6) sheenT = gs.t + b; } }
  return { p: Math.min(100, p), glow, sheenT };
}
function genP(u) { return clamp(u / (GEN_DUR - 0.1)); }
function drawProgress(t, scr) {
  const { p, glow, sheenT } = progressAt(t), W = 232; // track width px (computed below)
  const tw = $("#track").getBoundingClientRect().width || W;
  $("#fill").style.width = p + "%"; $("#head").style.left = p + "%"; $("#bloom").style.left = p + "%";
  $("#head").style.opacity = p > 0.3 ? 1 : 0; $("#track").style.setProperty("--glow", glow.toFixed(3));
  if (sheenT != null) { const u = t - sheenT; const fillW = tw * p / 100; $("#sheen").style.transform = `translateX(${out3(seg(u, 0, 0.6)) * (fillW + 60)}px)`; $("#sheen").style.opacity = 1 - seg(u, 0.45, 0.7); } else $("#sheen").style.opacity = 0;
  const [n, lbl] = STEP[scr]; const tot = scr === "s-pod" ? 4 : 6; $("#progN").innerHTML = `<b>0${n}</b> / 0${tot}`; $("#progL").textContent = lbl;
}

// ---------------------------------------------------------------- screen transitions + entrances
function splitWords() { $$("[data-words]").forEach(h => { h.querySelectorAll("span").forEach(s => { s.innerHTML = s.textContent.split(" ").map(w => `<span class="w">${w}</span>`).join(" "); }); }); }
function drawScreens(t) {
  const { cur, te, prev } = screenAt(t), u = t - te;
  $$(".screen").forEach(s => { const id = s.id;
    if (id === cur) { s.classList.add("on"); const k = out3(seg(u, 0, 0.5));
      s.style.opacity = prev ? k : 1; s.style.transform = prev ? `scale(${1.012 - 0.012 * out5(seg(u, 0, 0.8))})` : ""; s.style.filter = prev && k < 1 ? `blur(${(1 - k) * 6}px)` : "";
    } else if (id === prev && u < 0.5) { s.classList.add("on"); const k = out3(seg(u, 0, 0.45));
      s.style.opacity = 1 - k; s.style.transform = `scale(${1 - 0.02 * k}) translateY(${-10 * k}px)`; s.style.filter = `blur(${k * 6}px)`;
    } else { s.classList.remove("on"); }
  });
  // Entrances of the current screen: words rise on an exponential settle, blocks stagger 3 frames apart.
  const scr = $("#" + cur), base = te + (prev ? 0.12 : 0.05);
  $$(".w", scr).forEach((w, i) => { const tau = fr(t, base + i * 3 / 30); w.style.transform = `translateY(${(1 - expo(tau)) * 30}px)`; w.style.opacity = ink(tau, 0.55); });
  const nw = $$(".w", scr).length;
  $$("[data-in]", scr).forEach(el => { const k = +el.dataset.in; const tau = fr(t, base + (nw ? nw * 2 / 30 : 0) + k * 3 / 30);
    el.style.transform = (el.dataset.baseT || "") + ` translateY(${(1 - expo(tau, 0.8)) * 26}px)`; el.style.opacity = ink(tau, 0.42); });
  return { cur, te };
}

// ---------------------------------------------------------------- S1
const TABS = { launch: { ph: "yourcompany.com", go: "Continue" }, podcast: { ph: "Paste a YouTube or podcast link", go: "Find clips" }, ad: { ph: "yourproduct.com", go: "Continue" } };
function drawLink(t) {
  const prod = productAt(t), te = last(t, "tab");
  $$(".tab", $("#tabs")).forEach(b => b.classList.toggle("on", b.dataset.tab === prod));
  const ind = $("#ind"), tabsR = rectOf("#tabs");
  if (prod) { const prevTab = te ? last(te.t - 1e-6, "tab") : null; const rb = rectOf(`.tab[data-tab=${prod}]`);
    const ra = prevTab ? rectOf(`.tab[data-tab=${prevTab.tab}]`) : rb; const k = te ? expo(fr(t, te.t), 0.74) : 1;
    ind.style.left = (lerp(ra.x, rb.x, k) - tabsR.x - 1) + "px"; ind.style.width = lerp(ra.w, rb.w, k) + "px";
    const pop = te ? spring(fr(t, te.t), 0.5, 0.35) : 1; ind.style.opacity = te && !prevTab ? ink(fr(t, te.t), 0.8) : 1;
    ind.style.transform = te && !prevTab ? `scale(${0.9 + 0.1 * pop})` : "";
    ind.style.setProperty("--flash", te ? Math.exp(-(t - te.t) / 0.35).toFixed(3) : 0);
  } else ind.style.opacity = 0;
  const P = TABS[prod || "launch"]; $("#field").dataset.tab = prod || "launch"; $("#golabel").textContent = P.go;
  const focus = !!last(t, "focus"), ty = last(t, "type");
  let v = INIT.url || ""; let typing = false;
  if (ty) { const n = Math.floor((t - ty.t) / ty.per) + 1; v = ty.text.slice(0, clamp(n, 0, ty.text.length)); typing = n <= ty.text.length; }
  const inp = $("#input"), ph = $("#ph");
  ph.textContent = v || P.ph; ph.className = v ? "typed" : "ph";
  $("#field").classList.toggle("focus", focus); $("#field").classList.toggle("has-fav", !!v && !typing && prod !== "podcast");
  const blink = typing || (Math.floor(t / 0.53) % 2 === 0); $("#caret").style.opacity = focus && blink ? 1 : 0;
  $("#caret").style.order = v ? 2 : 0;
  if (ty && !typing) { const tau = fr(t, ty.t + ty.text.length * ty.per); $(".field .fav").style.transform = `scale(${0.6 + 0.4 * spring(tau, 0.45, 0.3)})`; }
  const btn = $("#go1"); btn.style.setProperty("--p", pressAmt(t, "#go1"));
  $("#imgslot").classList.toggle("filled", !!INIT.img);
  if (INIT.img && !$("#imgslot").dataset.f) { $("#imgslot").dataset.f = 1; $("#imgslot").innerHTML = `<span class="thumb"><svg width="22" height="28" viewBox="0 0 22 28"><defs><linearGradient id="bt" x1="0" x2="1"><stop offset="0" stop-color="#9aa4b4"/><stop offset=".45" stop-color="#eef2f7"/><stop offset="1" stop-color="#6d7686"/></linearGradient></defs><rect x="8" y="1" width="6" height="4" rx="1" fill="#c6f432"/><path d="M7 5h8v3c3 1.2 4 3 4 5.5V25a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V13.5C3 11 4 9.2 7 8z" fill="url(#bt)"/><rect x="5" y="15" width="12" height="6" rx="1" fill="#0e1116" opacity=".85"/></svg></span>lumen.png`; }
  // proof count ticks up slowly (illustrative)
  $("#count").textContent = (1284 + Math.floor(t / 4.2)).toLocaleString("en-US");
}

// ---------------------------------------------------------------- S2/S3: the AI option
const ANG = new Map();
function drawAI(t, el, q, te) {
  const h = H.get(el) ?? 0, p = pressAmt(t, "#" + el.id), ch = last(t, "choose", e => e.q === q);
  const dt = lastT == null ? 0 : clamp(t - lastT, 0, 0.1);
  const a = (ANG.get(el) ?? 200) + dt * (38 + 150 * h + (ch ? 260 * Math.exp(-(t - ch.t) / 0.5) : 0)); ANG.set(el, a);
  el.style.setProperty("--ai-a", (a % 360).toFixed(1) + "deg");
  el.style.setProperty("--p", p.toFixed(3));
  // Shimmer: one sweep every 2.6 s at rest; on hover a quicker sweep starts right away.
  const body = $(".body", el), bw = body.offsetWidth || 520, u = t - te;
  const period = 2.6 - 1.2 * h, ph = ((u + 1.8) % period) / period;
  $(".shim", el).style.left = lerp(-200, bw + 60, inOut3(clamp(ph * 1.6))) + "px";
  const au = $(".aur", el); au.style.left = (260 + Math.sin(t * 0.7) * 60) + "px"; au.style.top = (-60 + Math.cos(t * 0.5) * 30) + "px";
  $(".orb svg", el).style.transform = `rotate(${Math.sin(t * 1.2) * 6 + h * 18}deg) scale(${1 + h * 0.08 + Math.sin(t * 2.4) * 0.02})`;
  // Press flash, then burst + sparks + confirmed state.
  const fl = $(".flash", el); if (ch) { const v = t - ch.t; fl.style.opacity = v < 0.05 ? v / 0.05 : Math.exp(-(v - 0.05) / 0.25); } else fl.style.opacity = p * 0.5;
  const bu = $(".burst", el);
  if (ch) { const v = t - ch.t, k = out3(seg(v, 0, 0.7)); bu.style.opacity = (1 - k) * (v < 0.7 ? 1 : 0); bu.style.transform = `scale(${1 + 0.1 * k}, ${1 + 0.22 * k})`;
    const dn = $(".done", el), cont = [$(".top", el), $("h3", el), $("p", el), $(".steps3, .kitdots", el), $(".cta", el)].filter(Boolean);
    const dk = ink(fr(v, 0.12), 0.35); dn.style.opacity = dk; cont.forEach(c => { c.style.opacity = 1 - dk; c.style.filter = dk > 0.02 && dk < 0.98 ? `blur(${dk * 4}px)` : ""; });
    $(".ok", dn).style.transform = `scale(${0.4 + 0.6 * spring(fr(v, 0.1), 0.42, 0.28)})`;
    sparks(el, v);
  } else { bu.style.opacity = 0; $(".done", el).style.opacity = 0; sparks(el, -1); }
}
function sparks(el, v) {
  if (!el._sp) { el._sp = []; for (let i = 0; i < 14; i++) { const s = document.createElement("i"); s.className = "spark"; el.appendChild(s); el._sp.push(s); } }
  el._sp.forEach((s, i) => { if (v < 0 || v > 0.9) { s.style.opacity = 0; return; }
    const ang = (i / 14) * Math.PI * 2 + rnd(i) * 0.4, dist = (170 + rnd(i + 3) * 120) * expo(fr(v, 0), 0.84), w = el.offsetWidth / 2, hgt = el.offsetHeight / 2;
    s.style.transform = `translate(${Math.cos(ang) * dist * (w / 150)}px, ${Math.sin(ang) * dist * (hgt / 150) * 0.9}px) scale(${1 - v})`; s.style.opacity = (1 - seg(v, 0.35, 0.9)); });
}
function drawAsk(t, scr, te) {
  const q = scr === "s-rec" ? "rec" : "kit", ai = $(`#${q}-ai`), up = $(`#${q}-up`);
  drawAI(t, ai, q, te);
  const ch = last(t, "choose", e => e.q === q); up.style.opacity = ch ? 1 - 0.5 * out3(seg(t, ch.t, ch.t + 0.4)) : "";
  // kit shimmer dots
  if (q === "kit") $$(".kitdots i", ai).forEach((d, i) => d.style.backgroundPosition = `${150 - ((t * 0.8 + i * 0.12) % 1) * 250}% 0`);
}

// ---------------------------------------------------------------- S4: styles (launch)
const PV = []; // iframe windows
function drawStyle(t, te) {
  const sel = last(t, "select");
  $$(".card", $("#grid3")).forEach((c, i) => { const on = sel && sel.i === i; c.classList.toggle("on", on);
    const ck = $(".check", c); if (on) { const tau = fr(t, sel.t); ck.style.opacity = ink(tau, 0.7); ck.style.transform = `scale(${0.5 + 0.5 * spring(tau, 0.45, 0.3)})`; } else ck.style.opacity = 0;
    c.style.transform = `translateY(${(c.style.getPropertyValue("--h") || 0) * -3 - pressAmt(t, `.card[data-i="${i}"]`) * -2}px) ${c.dataset.inT || ""}`; });
  $("#go4").style.setProperty("--p", pressAmt(t, "#go4"));
  seekPreviews(t - te, $$("#grid3 iframe"));
}
function seekPreviews(u, frames) {
  frames.forEach((f, i) => { const w = f.contentWindow; if (!w || !w.seek) return; w.seek(u + 0.0);
    const segs = $(".segs", f.parentElement); if (!segs) return; const L = w.LOOP, sc = w.SCENES || [[0, L]];
    if (!segs.children.length) segs.innerHTML = sc.map(() => "<i><b></b></i>").join("");
    const lt = ((u % L) + L) % L; [...segs.children].forEach((s, k) => { const [a, b] = sc[k]; s.firstChild.style.transform = `scaleX(${clamp((lt - a) / (b - a))})`; }); });
}

// ---------------------------------------------------------------- S4b: podcast clip styles (guest photo slot)
const POD = [
  { k: "hz", name: "Hormozi", tag: "Popular", desc: "Bold caps, colour pops, punch-ins", bg: "radial-gradient(90% 60% at 50% 25%, #3a3632, #141312 70%)", beats: [["MOST", ""], ["FOUNDERS", ""], ["NEVER", "y"], ["SHIP.", "g"]] },
  { k: "doac", name: "Diary of a CEO", desc: "Outlined words, two cameras", bg: "radial-gradient(70% 50% at 80% 30%, #3b0c0a, #0a0606 60%, #050303)", beats: [["WHY", "host"], ["DID IT", "host"], ["TAKE TEN", ""], ["YEARS?", ""]] },
  { k: "mb", name: "MrBeast", desc: "Comic type, blue active word", bg: "linear-gradient(180deg, #1c3f8a, #0b1633)", beats: [["WE", ""], ["SPENT", ""], ["$10,000", "b"], ["ON ONE", ""], ["VIDEO", "b"]] },
  { k: "ali", name: "Ali Abdaal", desc: "Muted grade, handwritten notes", bg: "linear-gradient(180deg, #d8c9b3, #a99479)", beats: [["the 3-step system", ""]] },
  { k: "iman", name: "Iman Gadzhi", desc: "Dark luxury, fast zooms", bg: "radial-gradient(80% 60% at 50% 20%, #26211b, #0a0907 70%)", beats: [["DISCIPLINE", ""], ["IS", ""], ["FREEDOM", "i"]] },
];
function buildPod() {
  $("#grid5").innerHTML = POD.map((s, i) => `<div class="card pod" data-in="${i + 2}">
    <span class="check" style="top:18px;right:18px;width:22px;height:22px"><svg width="11" height="11"><use href="#i-check"/></svg></span>
    <div class="pv pod-${s.k}" style="background:${s.bg}"><div class="portrait" data-slot="guest"><img class="ph" src="assets/person.svg" alt=""><img class="photo" src="assets/guest.jpg" alt="" onerror="this.remove()"></div>
      <div class="cap"></div><div class="segs"><i><b></b></i></div></div>
    <div class="meta3"><div><h3>${s.name}${s.tag ? ` <span class="pop">${s.tag}</span>` : ""}</h3><p>${s.desc}</p></div></div></div>`).join("");
  const st = document.createElement("style"); st.textContent = `
    .pod .cap { font-weight: 900; }
    .pod-hz .cap { top: 58%; font-family: "Montserrat"; font-size: 30px; line-height: 1; text-transform: uppercase; color: #fff; -webkit-text-stroke: 7px #000; paint-order: stroke fill; text-shadow: 0 5px 0 rgba(0,0,0,.9); }
    .pod-hz .y { color: #ffe02e; } .pod-hz .g { color: #3cff6a; }
    .pod-doac .cap { top: 60%; font-family: "Montserrat"; font-size: 26px; line-height: 1.02; text-transform: uppercase; color: #fff; -webkit-text-stroke: 8px #000; paint-order: stroke fill; }
    .pod-doac .host { color: #ffd400; } .pod-doac .bars { position: absolute; left: 0; right: 0; height: 22px; background: #000; z-index: 1; }
    .pod-mb .cap { top: 56%; font-family: "Bangers"; font-weight: 400; font-size: 40px; letter-spacing: .02em; line-height: 1; color: #fff; -webkit-text-stroke: 6px #000; paint-order: stroke fill; text-shadow: 3px 4px 0 #000; }
    .pod-mb .b { color: #33b4ff; }
    .pod-ali .portrait { filter: grayscale(.75) contrast(1.02) brightness(1.05); }
    .pod-ali .cap { top: 30%; left: 14px; right: auto; text-align: left; font-family: "Caveat"; font-weight: 700; font-size: 30px; line-height: .95; color: #1c1a17; }
    .pod-ali .cap mark { background: none; color: #e0402a; }
    .pod-ali .cap svg { display: block; margin: 4px 0 0 30px; }
    .pod-iman .portrait { filter: contrast(1.1) brightness(.85) saturate(.8); }
    .pod-iman .cap { top: 64%; font-family: "Instrument Serif"; font-weight: 400; font-size: 30px; letter-spacing: .18em; color: #efe6d6; text-shadow: 0 2px 20px rgba(0,0,0,.7); }
    .pod-iman .cap i { font-style: italic; letter-spacing: .04em; color: #d9b77a; }
    .pod .pv::after { content: ""; position: absolute; inset: 0; background: radial-gradient(90% 70% at 50% 40%, transparent 55%, rgba(0,0,0,.45)); pointer-events: none; z-index: 1; }`;
  document.head.appendChild(st);
  $(".pod-doac").insertAdjacentHTML("beforeend", `<div class="bars" style="top:0"></div><div class="bars" style="bottom:0"></div>`);
}
function drawPod(t, te) {
  const u = t - te, sel = last(t, "select");
  $$(".card.pod").forEach((c, i) => { const s = POD[i], pv = $(".pv", c), cap = $(".cap", c), por = $(".portrait", c);
    c.classList.toggle("on", !!sel && sel.i === i); $(".check", c).style.opacity = sel && sel.i === i ? 1 : 0;
    const L = 3.2, lu = ((u % L) + L) % L, n = s.beats.length, per = (L - 0.4) / n, bi = Math.min(n - 1, Math.floor(lu / per)), bt = lu - bi * per;
    $(".segs b", c).style.transform = `scaleX(${lu / L})`;
    if (s.k === "hz") { const [w, cl] = s.beats[bi]; cap.innerHTML = `<span class="${cl}">${w}</span>`;
      const tau = fr(bt, 0); cap.style.transform = `scale(${1 + (1 - expo(tau, 0.7)) * 0.35})`; por.style.transform = `scale(${bi % 2 ? 1.14 : 1.0})`; }
    if (s.k === "doac") { const [w, cl] = s.beats[bi]; cap.innerHTML = `<span class="${cl}">${w}</span>`; cap.style.transform = `translateY(${(1 - expo(fr(bt, 0))) * 12}px)`;
      por.style.transform = cl === "host" ? "scaleX(-1) scale(1.12) translateX(-14px)" : "scale(1.0)"; pv.style.filter = cl === "host" ? "hue-rotate(-10deg) brightness(.9)" : ""; }
    if (s.k === "mb") { const [w, cl] = s.beats[bi]; cap.innerHTML = `<span class="${cl}">${w}</span>`; const tau = fr(bt, 0);
      cap.style.transform = `rotate(${(bi % 2 ? 4 : -4) * (1 - expo(tau, 0.75)) - 2}deg) scale(${1 + (1 - expo(tau, 0.68)) * 0.5})`; por.style.transform = `scale(${[1, 1.18, 1.06, 1.24, 1.1][bi]}) translate(${bi % 2 ? 6 : -4}px, ${bi % 2 ? 10 : 0}px)`; }
    if (s.k === "ali") { const k = clamp(lu / 1.4); const txt = "the 3-step"; const nch = Math.floor(k * 18);
      const full = `${txt.slice(0, Math.min(nch, 10))}${nch > 10 ? "<br><mark>" + "system".slice(0, nch - 11) + "</mark>" : ""}`;
      cap.innerHTML = full + `<svg width="70" height="40" viewBox="0 0 70 40"><path d="M4 4 C20 30 40 36 62 30 M52 22 L63 30 L52 37" fill="none" stroke="#1c1a17" stroke-width="3" stroke-linecap="round" stroke-dasharray="120" stroke-dashoffset="${120 - 120 * clamp((lu - 1.3) / 0.5)}"/></svg>`;
      por.style.transform = `scale(${1.02 + lu * 0.01}) translateX(18px)`; }
    if (s.k === "iman") { cap.innerHTML = s.beats.slice(0, bi + 1).map(([w, cl]) => cl === "i" ? `<i>${w.toLowerCase()}</i>` : w).join("<br>");
      const tau = fr(bt, 0); cap.style.opacity = ink(tau, 0.3); por.style.transform = `scale(${1.05 + bi * 0.08 + (1 - expo(tau, 0.85)) * 0.05})`; }
  });
}

// ---------------------------------------------------------------- S5: generating
const LOG = [["open", "Opening northwind.ai in a browser", "Opened northwind.ai"], ["record", "AI is recording a walkthrough", "Walkthrough recorded"],
  ["brand", "Extracting the brand kit", "Brand kit extracted"], ["script", "Writing the script", "Script written"], ["voice", "Recording the voice-over", "Voice-over"],
  ["board", "Storyboarding", "Storyboard"], ["render", "Rendering", "Rendered"]];
const BEATS = [["0:00 · HOOK", "Your forecast is <span class='hd'>stale.</span>"], ["0:04 · TURN", "Northwind sees the next quarter while it's still ahead of you."], ["0:12 · PROOF", "Ledger, CRM and payroll. One live model."]];
function buildGen() {
  $("#log").innerHTML = LOG.map(([k]) => `<li data-k="${k}"><span class="ic"><svg width="11" height="11"><use href="#i-check"/></svg></span><div><div class="row"><span class="lb"></span><span class="dt"></span></div>${k === "brand" ? `<div class="detail"><div class="kit"><span class="lg" data-at="0.4"><svg width="18" height="18"><use href="#i-nw"/></svg></span><span class="sw"><i data-at="1.1" style="background:#0e1116"></i><i data-at="1.2" style="background:#c6f432"></i><i data-at="1.3" style="background:#f4f1ea"></i><i data-at="1.4" style="background:#8a93a3"></i></span><span class="ty" data-at="0.7"><b>Aa</b><span>Manrope · Inter</span></span></div></div>` : ""}</div></li>`).join("");
  for (let i = 0; i < 6; i++) $("#strip").insertAdjacentHTML("beforeend", `<div class="th empty" data-i="${i}"><svg viewBox="0 0 1600 900" style="display:none"><use href="#nwF${i + 1}"/></svg><span class="n">0${i + 1}</span></div>`);
  $("#beats").innerHTML = BEATS.map(([tc, tx]) => `<div class="beat"><span class="tc">${tc}</span><span class="tx" data-full="${tx.replace(/"/g, "&quot;")}"></span></div>`).join("");
  $("#wave").innerHTML = Array.from({ length: 96 }, (_, i) => { const env = 0.25 + 0.75 * Math.abs(Math.sin(i * 0.37) * Math.sin(i * 0.11 + 1)) * (0.6 + 0.4 * rnd(i)); return `<i style="height:${Math.round(10 + env * 120)}px"></i>`; }).join("");
  $("#vlines").innerHTML = "Your forecast is stale. Northwind sees the next quarter while it's still ahead of you.".split(" ").map(w => `<span>${w}</span>`).join(" ");
}
function typeHTML(html, n) { // reveal n visible characters of simple HTML; newest 3 glyphs in the accent colour
  let out = "", c = 0, i = 0; while (i < html.length && c < n) { if (html[i] === "<") { const j = html.indexOf(">", i); out += html.slice(i, j + 1); i = j + 1; continue; }
    const ch = html[i]; out += c >= n - 3 ? `<span style="color:#c6f432">${ch}</span>` : ch; c++; i++; }
  // close an open span
  if ((out.match(/<span class='hd'>/g) || []).length > (out.match(/<\/span>/g) || []).length - (out.match(/<span style/g) || []).length) out += "</span>";
  return out;
}
const plainLen = (h) => h.replace(/<[^>]+>/g, "").length;
function drawGen(t) {
  const gs = last(t, "gen"); const u = gs ? t - gs.t : 0, g = genP(u);
  const ph = GEN.find(([, a, b]) => u >= a && u < b) || GEN[GEN.length - 1]; const pk = ph[0], pu = u - ph[1];
  const done = (k) => { const q = GEN.find(x => x[0] === k); return u >= q[2]; };
  // log
  $$("#log li").forEach((li, i) => { const [k, act, fin] = LOG[i]; const q = GEN[i]; const isA = u >= q[1] && u < q[2], isD = u >= q[2];
    li.classList.toggle("active", isA); li.classList.toggle("done", isD); $(".lb", li).textContent = isD ? fin : act;
    li.querySelector(".ic").style.setProperty("--spin", (t * 360 % 360) + "deg");
    const dt = $(".dt", li); const lu = u - q[1];
    dt.textContent = k === "open" ? (isD ? "14 pages" : isA ? `${Math.floor(clamp(lu / 1.5) * 14)} pages` : "")
      : k === "record" ? (isA ? `REC 00:${String(Math.floor(lu * 6)).padStart(2, "0")}` : isD ? "00:23 · 6 clicks" : "")
      : k === "brand" ? (isA || isD ? "logo · colours · type" : "") : k === "script" ? (isA || isD ? "3 beats · 29s" : "")
      : k === "voice" ? (isA ? `${Math.round(clamp(lu / 1.2) * 29)}s` : isD ? "warm, mid · 29s" : "")
      : k === "board" ? (isA ? `${Math.min(6, Math.floor(lu / 0.4))} / 6 frames` : isD ? "6 frames" : "")
      : k === "render" ? (isA ? `${Math.round(clamp(lu / 1.4) * 100)}%` : isD ? "1080p · 30fps" : "") : "";
    const det = $(".detail", li); if (det) { det.style.display = isA || isD ? "" : "none";
      $$("[data-at]", det).forEach(el => { const tau = fr(lu, +el.dataset.at); el.style.opacity = ink(tau, 0.5); el.style.transform = `scale(${0.6 + 0.4 * spring(tau, 0.45, 0.3)})`; }); }
  });
  $("#stageLb").textContent = pk === "board" ? `Storyboarding frame ${Math.min(6, Math.floor(pu / 0.4) + 1)} of 6` : u >= 13.8 ? "Final check" : ph[3];
  $("#stageLb").style.backgroundPosition = `${100 - ((t / 2.4) % 1) * 150}% 0`;
  $("#pct").textContent = Math.floor(g * 100) + "%"; const s = Math.round((1 - g) * 228); $("#left").textContent = s > 90 ? `about ${Math.round(s / 60)} min left` : s > 5 ? `about ${s}s left` : "almost there";
  // canvas layers
  const inBrowser = ["open", "record", "brand"].includes(pk);
  $("#L-browser").classList.toggle("on", inBrowser); $("#L-script").classList.toggle("on", pk === "script"); $("#L-voice").classList.toggle("on", pk === "voice"); $("#L-board").classList.toggle("on", pk === "board" || pk === "render");
  if (inBrowser) drawBrowser(t, u, pk, pu);
  if (pk === "script") { $$("#beats .tx").forEach((el, i) => { const full = el.dataset.full, n = Math.floor(fr(pu, 0.05 + i * 0.36) * 2.2); el.innerHTML = typeHTML(full, Math.min(n, plainLen(full)) + (n > plainLen(full) + 8 ? 3 : 0));
      el.parentElement.style.opacity = n > 0 ? 1 : 0.0; }); $("#L-script .docpanel").style.transform = `translateY(${-pu * 6}px)`; }
  if (pk === "voice") { const k = clamp(pu / 1.15); const bars = $$("#wave i"); bars.forEach((b, i) => { b.classList.toggle("on", i / bars.length < k); b.style.transform = `scaleY(${i / bars.length < k ? 1 : 0.35})`; });
    const ws = $$("#vlines span"); ws.forEach((w, i) => w.classList.toggle("said", i / ws.length < k)); }
  if (pk === "board" || pk === "render") drawBoard(u);
  // strip
  $$("#strip .th").forEach((th, i) => { const b = 10.0 + i * 0.4; const filled = u >= b + 0.4, isCur = u >= b && u < b + 0.4;
    th.classList.toggle("empty", !filled && !isCur); th.classList.toggle("cur", isCur); const sv = $("svg", th); sv.style.display = filled || isCur ? "" : "none"; sv.style.opacity = isCur ? 0.45 : 1;
    th.style.backgroundPosition = `${150 - ((t / 1.8) % 1) * 250}% 0`; });
}
let BV = null;
function drawBrowser(t, u, pk, pu) {
  const bv = $("#bview"); if (!BV) BV = { w: bv.offsetWidth, h: bv.offsetHeight }; const sc = BV.w / 1200;
  $(".appv svg.dash").style.top = (-56 * sc) + "px"; $("#newline").style.cssText = `position:absolute;left:0;top:${-56 * sc}px;width:100%`;
  const D = (x, y) => ({ x: 18 + x * sc, y: 18 + 40 + y * sc - 56 * sc }); // dash coords -> canvas px
  const S = (x, y) => ({ x: 18 + x, y: 18 + 40 + y });                     // bview px -> canvas px
  // browser entrance + url
  const bt = fr(u, 0); $("#browser").style.transform = `scale(${0.94 + 0.06 * out5(Math.min(1, bt / 18))})`; $("#browser").style.opacity = ink(bt, 0.4);
  let url = "", view = "skel";
  if (u < 1.5) { url = "northwind.ai".slice(0, Math.floor(fr(u, 0.15) / 1.5)); view = u < 1.0 ? (u < 0.6 ? "none" : "skel") : "site"; }
  else if (u < 5.3) { url = u < 1.72 ? "northwind.ai" : "app.northwind.ai/forecast"; view = u < 1.72 ? "site" : u < 1.9 ? "skel" : "app"; }
  else { url = "northwind.ai"; view = u < 5.45 ? "skel" : "site"; }
  $("#urlT").textContent = url;
  const loadK = u < 1.5 ? seg(u, 0.6, 1.05) : u < 5.3 ? seg(u, 1.72, 1.92) : seg(u, 5.3, 5.47);
  $("#load").style.width = (out3(loadK) * 100) + "%"; $("#load").style.opacity = loadK > 0 && loadK < 1 ? 1 : 0;
  $("#skel").style.display = view === "skel" ? "" : "none"; $("#site").style.display = view === "site" ? "" : "none"; $("#appv").style.display = view === "app" ? "" : "none";
  $$("#skel i").forEach(i => i.style.backgroundPosition = `${150 - ((t / 1.2) % 1) * 250}% 0`);
  // REC badge during the walkthrough
  const recOn = u >= 1.75 && u < 5.3; $("#rec").style.opacity = recOn ? ink(fr(u, 1.75), 0.5) : 0;
  $("#recT").textContent = `REC 00:${String(Math.floor(Math.max(0, u - 1.75) * 6)).padStart(2, "0")}`;
  $("#rec i").style.opacity = Math.floor(t * 2) % 2 ? 0.35 : 1;
  // AI cursor path (canvas px) with clicks
  const nav = S(96 + 186, 25); // "Product" link in the site nav (approx)
  const K = [[0.9, S(560, 330)], [1.3, S(200, 26)], [1.5, S(200, 26)], [2.05, D(110, 190)], [2.35, D(400, 196)], [2.7, D(400, 200)], [2.95, D(80, 236)], [3.5, D(80, 238)],
    [3.8, { x: 0, y: 0, slider: 0 }], [4.45, { x: 0, y: 0, slider: 1 }], [4.75, D(900, 470)], [5.1, D(960, 450)], [5.3, D(960, 450)]];
  const pan = $("#panel"); const panK = out5(seg(u, 3.0, 3.4)); pan.style.transform = `translateX(${(1 - panK) * 290}px)`; pan.style.opacity = panK;
  const slK = inOut3(seg(u, 3.85, 4.45)); const slx = 18 + 16 + 18 + (BV.w - 16 - 250) + 18 + slK * 0 ; // placeholder
  const panR = { x: 18 + BV.w - 16 - 250, y: 58 + 16 };
  const sl0 = { x: panR.x + 18 + 214 * 0.4, y: panR.y + 18 + 92 }, sl1 = { x: panR.x + 18 + 214 * 0.8, y: sl0.y };
  const res = (p) => p.slider === 0 ? sl0 : p.slider === 1 ? sl1 : p;
  let c = res(K[0][1]); for (let i = 0; i < K.length - 1; i++) { const [t0, a] = K[i], [t1, b] = K[i + 1]; if (u <= t1) { const k = inOut3(seg(u, t0, t1)); const A = res(a), B = res(b); c = { x: lerp(A.x, B.x, k), y: lerp(A.y, B.y, k) }; break; } c = res(b); }
  const aic = $("#aic"); aic.style.transform = `translate(${c.x - 4}px, ${c.y - 3}px)`; aic.style.opacity = u > 0.9 && u < 5.25 ? ink(fr(u, 0.9), 0.5) * (1 - seg(u, 5.1, 5.25)) : 0;
  const clicks = [1.5, 2.95, 3.85, 5.1]; const ck = clicks.find(x => u >= x && u < x + 0.45); const cl = $("#clk");
  if (ck != null) { const v = (u - ck) / 0.45, p = K.find(k => k[0] >= ck) ; const P = res(p ? p[1] : K[0][1]); cl.style.left = P.x + "px"; cl.style.top = P.y + "px"; cl.style.opacity = 1 - v; cl.style.transform = `scale(${0.5 + out3(v) * 1.3})`; } else cl.style.opacity = 0;
  // app state
  const hl = $("#sidehl"); const hlTo = u < 2.95 ? 190 : 236; const hlFrom = 190; const hk = expo(fr(u, 2.97), 0.75);
  const hy = u < 2.95 ? 190 : lerp(hlFrom, hlTo, hk); const hp = D(16, hy - 18); Object.assign(hl.style, { left: (hp.x - 18) + "px", top: (hp.y - 58) + "px", width: 188 * sc + "px", height: 36 * sc + "px" });
  $("#slf").style.width = lerp(40, 80, slK) + "%"; $("#slk").style.left = lerp(40, 80, slK) + "%";
  $("#hires").textContent = "+" + Math.round(lerp(2, 4, slK)); $("#runway").textContent = Math.round(lerp(31, 27, slK)) + " mo";
  $("#nlp").style.strokeDashoffset = 1 - out3(seg(u, 4.0, 4.9)); $("#newline").style.opacity = u > 3.95 ? 1 : 0;
  // brand-kit extraction overlays on the site
  const site = $("#site"), inBrand = u >= 5.3; $("#scanl").style.display = inBrand ? "" : "none"; $("#scanl").style.top = (20 + ((pu * 260) % 360)) + "px";
  const sr = site.getBoundingClientRect();
  $$(".bbox", site).forEach(b => { const on = inBrand && pu >= +b.dataset.at; b.style.display = on ? "" : "none"; if (!on) return;
    const tgt = $(b.dataset.t, site).getBoundingClientRect(), k = sr.width / site.offsetWidth, pad = 5;
    const L = Math.max(3, (tgt.left - sr.left) / k - pad), T = Math.max(3, (tgt.top - sr.top) / k - pad), W = Math.min(site.offsetWidth - 3 - L, tgt.width / k + pad * 2), Hh = Math.min(site.offsetHeight - 3 - T, tgt.height / k + pad * 2);
    const tau = fr(pu, +b.dataset.at), e = expo(tau, 0.72);
    Object.assign(b.style, { left: (L - (1 - e) * 10) + "px", top: (T - (1 - e) * 10) + "px", width: (W + (1 - e) * 20) + "px", height: (Hh + (1 - e) * 20) + "px", opacity: ink(tau, 0.6) });
    const lb = $("b", b); lb.style.top = T < 24 ? "50%" : "-19px"; lb.style.left = T < 24 ? "calc(100% + 6px)" : "-1.5px"; lb.style.transform = T < 24 ? "translateY(-50%)" : ""; });
}
function drawBoard(u) {
  const B0 = 10.0, BF = 0.4, NF = 6; let cur, next, rev;
  if (u < 12.4) { const f = (u - B0) / BF, i = Math.floor(f); next = Math.min(NF - 1, i); cur = i - 1; rev = f - i; }
  else { cur = 4; next = 4; rev = clamp((u - 12.4) / 1.35); }
  $("#curF").style.display = cur < 0 ? "none" : ""; if (cur >= 0) $("#curF use").setAttribute("href", `#nwF${cur + 1}`);
  $("#nextF use").setAttribute("href", `#nwF${next + 1}`);
  const render = u >= 12.4; $("#curF").style.filter = render ? "grayscale(1) brightness(.5)" : "";
  $("#nextF").style.clipPath = `inset(0 ${(1 - out3(rev)) * 100}% 0 0)`;
  $("#scan").style.left = (out3(rev) * 100) + "%"; $("#scan").style.display = u >= 13.75 ? "none" : "";
  $("#gridov").style.clipPath = `inset(0 0 0 ${out3(rev) * 100}%)`; $("#gridov").style.display = u >= 13.75 ? "none" : "";
  $("#hudA").textContent = render ? "RENDER PASS" : `FRAME 0${next + 1}`; $("#hudB").textContent = u >= 13.75 ? "ENCODING" : render ? `${Math.round(rev * 100)}%` : "COMPOSITING";
  $("#canvas").style.transform = `scale(${1 + (u - 10) * 0.0015})`;
}

// ---------------------------------------------------------------- S6: result
function drawResult(t, te) {
  const u = t - te; seekPreviews(u, [$("#s-res iframe")]);
  const L = 12, lu = ((u % L) + L) % L; $$("#rscrub i").forEach((s, k) => s.firstChild.style.transform = `scaleX(${clamp((lu - k * 3) / 3)})`);
  const secs = Math.floor(lu / 12 * 30); $("#rtime").innerHTML = `0:${String(secs).padStart(2, "0")} <span>/ 0:30</span>`;
  $("#book").style.setProperty("--p", pressAmt(t, "#book"));
}

// ---------------------------------------------------------------- frame
let CUR_T = 0;
function seek(t) {
  CUR_T = t;
  const { cur, te } = drawScreens(t);
  const c = DEMO ? cursorAt(t) : POINTER;
  hoverUpdate(t, c, cur);
  drawProgress(t, cur);
  const prod = productAt(t), url = last(t, "type");
  $("#urlchip").style.opacity = cur === "s-link" ? 0 : 1; $("#urlchipT").textContent = SCRIPT === "podcast" ? "The Operator Hour · Ep. 212" : (url ? url.text : INIT.url || "northwind.ai");
  if (cur === "s-link" || screenAt(t).prev === "s-link") drawLink(t);
  if (cur === "s-rec" || cur === "s-kit") drawAsk(t, cur, te);
  const prev = screenAt(t).prev; if (prev === "s-rec" && t - te < 0.5) drawAsk(t, "s-rec", last(te - 1e-6, "go").t);
  if (prev === "s-kit" && t - te < 0.5) drawAsk(t, "s-kit", last(te - 1e-6, "go").t);
  if (cur === "s-style") drawStyle(t, te);
  if (cur === "s-pod") drawPod(t, te);
  if (cur === "s-gen" || prev === "s-gen") drawGen(t);
  if (cur === "s-res") drawResult(t, te);
  // demo cursor + click ripple
  if (DEMO) { const cu = $("#cursor"); const hid = HIDE_CURSOR.find(([a, b]) => t >= a - 0.15 && t < b + 0.3);
    let op = 1; for (const [a, b] of HIDE_CURSOR) { if (t >= a - 0.15 && t < a) op = 1 - seg(t, a - 0.15, a); else if (t >= a && t < b) op = 0; else if (t >= b && t < b + 0.3) op = seg(t, b, b + 0.3); }
    const pr = EV.filter(e => e.type === "press").some(e => t >= e.t && t < e.t + 0.12);
    cu.style.opacity = op; cu.style.transform = `translate(${c.x - 5}px, ${c.y - 3}px) scale(${pr ? 0.88 : 1})`;
    const rp = $("#ripple"), pe = EV.filter(e => e.type === "press" && t >= e.t && t < e.t + 0.5).pop();
    if (pe && op > 0) { const v = (t - pe.t) / 0.5, p = cursorAt(pe.t); rp.style.left = p.x + "px"; rp.style.top = p.y + "px"; rp.style.opacity = (1 - v) * op; rp.style.transform = `scale(${0.4 + out3(v) * 1.1})`; } else rp.style.opacity = 0; }
  lastT = t;
}

// ---------------------------------------------------------------- live interactions
function liveNow() { return (performance.now() - T0) / 1000; }
let T0 = 0;
function wireLive() {
  addEventListener("pointermove", e => { POINTER = { x: e.clientX, y: e.clientY }; });
  const on = (sel, fn) => $$(sel).forEach(el => el.addEventListener("click", () => fn(el)));
  on("#tabs .tab", el => click(liveNow(), `.tab[data-tab=${el.dataset.tab}]`, 4, { type: "tab", tab: el.dataset.tab }));
  on("#input", () => { const t = liveNow(); click(t, "#input", 4, { type: "focus" }); const p = productAt(t);
    push({ t: t + 0.1, type: "type", text: p === "podcast" ? "youtu.be/op-hour-212" : p === "ad" ? "lumenbottle.com" : "northwind.ai", per: 0.035 }); });
  on("#go1", () => { const t = liveNow(); const p = productAt(t) || "launch"; if (!productAt(t)) push({ t, type: "tab", tab: "launch" }); click(t, "#go1", 8, { type: "go", to: p === "podcast" ? "s-pod" : "s-rec" }); });
  on("#rec-ai, #rec-up", el => { const t = liveNow(); click(t, "#" + el.id, 14, { type: "choose", q: "rec", v: el.id.endsWith("ai") ? "ai" : "up" }); push({ t: t + 0.95, type: "go", to: "s-kit" }); });
  on("#kit-ai, #kit-up", el => { const t = liveNow(); click(t, "#" + el.id, 14, { type: "choose", q: "kit", v: el.id.endsWith("ai") ? "ai" : "up" }); push({ t: t + 0.95, type: "go", to: "s-style" }); });
  on("#grid3 .card", el => click(liveNow(), `.card[data-i="${el.dataset.i}"]`, 6, { type: "select", i: +el.dataset.i }));
  on("#go4", () => { const t = liveNow(); if (!last(t, "select")) push({ t, type: "select", i: 0 }); click(t, "#go4", 8, { type: "go", to: "s-gen" }); push({ t: t + 0.3, type: "gen" }); push({ t: t + 0.3 + GEN_DUR + 0.05, type: "go", to: "s-res" }); });
  on("#book", () => click(liveNow(), "#book", 0, { type: "book" }));
}

// ---------------------------------------------------------------- boot
async function boot() {
  $("#svgdefs").innerHTML = await (await fetch("frames.svg")).text();
  splitWords(); buildPod(); buildGen();
  $$("iframe[data-src]").forEach(f => f.src = f.dataset.src + "?capture");
  await document.fonts.ready;
  await Promise.all($$("iframe").map(f => new Promise(res => { const chk = () => f.contentDocument?.body?.dataset.ready ? res() : setTimeout(chk, 40); chk(); })));
  // ticks on the progress track at step boundaries
  [16, 30, 44, 58].forEach(v => $("#track").insertAdjacentHTML("afterbegin", `<i class="tick" style="left:${v}%"></i>`));
  if (SCRIPT === "podcast") scriptPodcast(); else if (SCRIPT === "ad") { scriptLaunch("ad", "lumenbottle.com"); INIT.img = true; } else scriptLaunch();
  $$(".screen").forEach(s => s.classList.add("on")); document.body.offsetWidth; // layout for geometry
  CURSOR.forEach(([, p]) => pt(p)); ["#tabs", ".tab[data-tab=launch]", ".tab[data-tab=podcast]", ".tab[data-tab=ad]"].forEach(rectOf);
  $$(".screen").forEach(s => s.classList.remove("on"));
  if (!DEMO) { EV = []; INIT = { product: null, url: "" }; push({ t: 0, type: "go", to: "s-link" }); wireLive(); }
  window.seek = seek; window.DUR = DUR; window.GEN_DUR = GEN_DUR;
  seek(Q.has("t") ? +Q.get("t") : 0);
  document.body.dataset.ready = 1;
  if (!CAPTURE && !Q.has("t")) { T0 = performance.now(); const loop = () => { const t = (performance.now() - T0) / 1000; seek(DEMO ? t % DUR : t); requestAnimationFrame(loop); }; loop(); }
}
boot();
})();
