// Tiny deterministic motion engine: every frame is a pure function of t (seconds).
// window.seek(t) renders frame t; the capture script steps t and screenshots.
const E = {
  lin: x => x,
  inCubic: x => x * x * x,
  outCubic: x => 1 - Math.pow(1 - x, 3),
  outQuart: x => 1 - Math.pow(1 - x, 4),
  outQuint: x => 1 - Math.pow(1 - x, 5),
  outExpo: x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  inExpo: x => (x <= 0 ? 0 : Math.pow(2, 10 * x - 10)),
  inOutCubic: x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  inOutQuint: x => (x < 0.5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2),
  outBack: (x, s = 1.6) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
  // damped spring that settles on 1 (overshoot then settle)
  spring: (x, k = 7, f = 13) => (x >= 1 ? 1 : 1 - Math.exp(-k * x) * Math.cos(f * x)),
  bez: (x1, y1, x2, y2) => x => {        // CSS cubic-bezier, solved numerically
    let a = 0, b = 1, m = x;
    for (let i = 0; i < 24; i++) {
      m = (a + b) / 2;
      const X = 3 * x1 * m * (1 - m) ** 2 + 3 * x2 * m * m * (1 - m) + m ** 3;
      if (X < x) a = m; else b = m;
    }
    return 3 * y1 * m * (1 - m) ** 2 + 3 * y2 * m * m * (1 - m) + m ** 3;
  },
};
const P = (t, a, d, e = E.outCubic) => (t <= a ? 0 : t >= a + d ? 1 : e((t - a) / d));
const L = (a, b, k) => a + (b - a) * k;
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const show = (el, v) => { el.style.visibility = v ? "visible" : "hidden"; };
const tf = (el, s) => { el.style.transform = s; };
const op = (el, v) => { el.style.opacity = v; };
// seeded random so every render is identical
function rng(seed) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
// typewriter: returns the substring visible at time t
const typed = (s, t, a, cps) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - a) * cps))));

function boot(dur, render) {
  window.DUR = dur;
  window.seek = t => render(Math.min(t, dur - 1e-4));
  const ready = () => { render(0); document.body.dataset.ready = 1; };
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(ready, 50));
  // live preview: open the page without ?capture to watch it loop
  if (!location.search.includes("capture")) {
    const t0 = performance.now();
    const loop = () => { window.seek(((performance.now() - t0) / 1000) % dur); requestAnimationFrame(loop); };
    setTimeout(() => requestAnimationFrame(loop), 300);
  }
}
