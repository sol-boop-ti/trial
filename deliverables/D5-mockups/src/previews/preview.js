// Tiny deterministic preview engine. A preview defines draw(t) for t in [0, loop).
//   ?t=3.2      render one still at 3.2 s
//   ?capture    no rAF loop; the host calls window.seek(t)
// Everything moves from JS on computed curves (lib/motion.js), so frames are reproducible.
(function () {
  const q = new URLSearchParams(location.search);
  const stage = document.querySelector(".stage");
  function fit() { const k = Math.min(innerWidth / 1280, innerHeight / 720); stage.style.transform = `scale(${k})`;
    stage.style.left = (innerWidth - 1280 * k) / 2 + "px"; stage.style.top = (innerHeight - 720 * k) / 2 + "px"; }
  addEventListener("resize", fit); fit();
  // Grain: one seeded noise tile, offset per frame.
  const grain = document.createElement("div"); grain.className = "grainfx"; stage.appendChild(grain);
  const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"), im = x.createImageData(256, 256);
  for (let i = 0; i < 256 * 256; i++) { const v = M.rnd(i * 1.37) * 255; im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = v; im.data[i * 4 + 3] = 255; }
  x.putImageData(im, 0, 0); grain.style.backgroundImage = `url(${c.toDataURL()})`;
  window.Preview = function ({ loop, draw, init }) {
    window.LOOP = loop;
    window.seek = (t) => { t = ((t % loop) + loop) % loop; const f = Math.floor(t * 30);
      grain.style.transform = `translate(${Math.round(M.rnd(f) * 60 - 30)}px, ${Math.round(M.rnd(f + 7) * 60 - 30)}px)`; draw(t); };
    Promise.resolve(init && init()).then(() => document.fonts.ready).then(() => {
      window.seek(q.has("t") ? +q.get("t") : 0); document.body.dataset.ready = 1;
      if (!q.has("capture") && !q.has("t")) { const t0 = performance.now(); const tick = () => { window.seek((performance.now() - t0) / 1000); requestAnimationFrame(tick); }; tick(); }
    });
  };
  // Liquid glass: an SVG displacement map sized to the element, bending the backdrop near the rim.
  window.liquidGlass = function (el, { radius = 40, bezel = 44, scale = 70, mag = 0.12, blur = 0.6, sat = 1.7, bright = 1.06 } = {}) {
    const W = el.offsetWidth, H = el.offsetHeight, id = "lg" + Math.random().toString(36).slice(2, 8);
    const cv = document.createElement("canvas"); cv.width = W; cv.height = H; const cx = cv.getContext("2d"), img = cx.createImageData(W, H);
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const px = i - W / 2, py = j - H / 2, qx = Math.abs(px) - (W / 2 - radius), qy = Math.abs(py) - (H / 2 - radius);
      const ox = Math.max(qx, 0), oy = Math.max(qy, 0), d = Math.min(Math.max(qx, qy), 0) + Math.hypot(ox, oy) - radius; // SDF, <0 inside
      let gx, gy; if (ox > 0 && oy > 0) { const l = Math.hypot(ox, oy); gx = Math.sign(px) * ox / l; gy = Math.sign(py) * oy / l; }
      else if (qx > qy) { gx = Math.sign(px); gy = 0; } else { gx = 0; gy = Math.sign(py); }
      const e = M.clamp(1 + d / bezel), k = Math.pow(e, 2.2); // strongest at the rim, zero in the flat centre
      const mx = (px / (W / 2)) * mag, my = (py / (H / 2)) * mag; // gentle lens magnification toward the centre
      const p = (j * W + i) * 4; img.data[p] = 128 - M.clamp(gx * k + mx, -1, 1) * 127; img.data[p + 1] = 128 - M.clamp(gy * k + my, -1, 1) * 127; img.data[p + 2] = 128; img.data[p + 3] = 255;
    }
    cx.putImageData(img, 0, 0);
    const ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg");
    svg.setAttribute("width", 0); svg.setAttribute("height", 0); svg.style.position = "absolute";
    svg.innerHTML = `<filter id="${id}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feImage href="${cv.toDataURL()}" x="0" y="0" width="${W}" height="${H}" preserveAspectRatio="none" result="m"/>
      <feDisplacementMap in="SourceGraphic" in2="m" scale="${scale}" xChannelSelector="R" yChannelSelector="G"/></filter>`;
    document.body.appendChild(svg);
    el.style.backdropFilter = `url(#${id}) blur(${blur}px) saturate(${sat}) brightness(${bright})`;
  };
})();
// Directional motion blur, weighted by speed (manual section 6): crisp below ~18 px/frame.
(function () {
  const ns = "http://www.w3.org/2000/svg", svg = document.createElementNS(ns, "svg");
  svg.setAttribute("width", 0); svg.setAttribute("height", 0); svg.style.position = "absolute";
  const B = [3, 6, 10, 16, 24]; let h = "";
  B.forEach(b => { h += `<filter id="mbx${b}" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur stdDeviation="${b} 0"/></filter>`;
    h += `<filter id="mby${b}" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="0 ${b}"/></filter>`; });
  svg.innerHTML = h; document.addEventListener("DOMContentLoaded", () => document.body.appendChild(svg));
  // vx, vy in px per frame (stage px). Returns the filter string (so callers can combine).
  window.mblur = function (el, vx, vy = 0) {
    const sp = Math.hypot(vx, vy), w = M.blurW(sp, 16, 40); if (w <= 0) { el.style.filter = ""; return; }
    const amt = w * 24, b = B.reduce((a, c) => Math.abs(c - amt) < Math.abs(a - amt) ? c : a);
    el.style.filter = `url(#mb${Math.abs(vx) >= Math.abs(vy) ? "x" : "y"}${b})`;
  };
})();
