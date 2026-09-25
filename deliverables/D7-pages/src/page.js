// Vanilla port of the brand kit's Halftone component (same algorithm as components/bundle.js),
// plus the numbered annotation overlay shown when the URL has ?annotate.
(function () {
  if (/still/.test(location.search)) document.documentElement.classList.add('still');
  function readColor(name, fb) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    var m = /^#([0-9a-f]{6})$/i.exec(v); if (!m) return fb;
    var n = parseInt(m[1], 16); return [n >> 16 & 255, n >> 8 & 255, n & 255];
  }
  function halftone(cv) {
    var r = cv.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    var w = Math.max(1, Math.round(r.width)), hgt = Math.max(1, Math.round(r.height));
    cv.width = w * dpr; cv.height = hgt * dpr;
    var ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var hi = readColor('--halftone-dot', [45, 45, 50]), lo = readColor('--halftone-dot-dim', [16, 16, 18]);
    var d = cv.dataset;
    var cxp = w * (d.cx ? +d.cx : 0.5), cyp = hgt * (d.cy ? +d.cy : 0.62);
    var rx = d.rx ? +d.rx : Math.min(w * 0.42, 490), ry = d.ry ? +d.ry : rx * 0.66;
    for (var y = 0; y < hgt; y += 8) for (var x = 0; x < w; x += 4) {
      var dx = (x - cxp) / rx, dy = (y - cyp) / ry, k = 1 - Math.sqrt(dx * dx + dy * dy);
      if (k <= 0) continue; k = k * k * (3 - 2 * k);
      ctx.fillStyle = 'rgb(' + Math.round(lo[0] + (hi[0] - lo[0]) * k) + ',' + Math.round(lo[1] + (hi[1] - lo[1]) * k) + ',' + Math.round(lo[2] + (hi[2] - lo[2]) * k) + ')';
      var dh = 1 + 2 * k; ctx.fillRect(x, y - dh / 2, 1.5 + 0.5 * k, dh);
    }
  }
  function annotate() {
    if (!/annotate/.test(location.search)) return;
    var sx = window.scrollX, sy = window.scrollY;
    document.querySelectorAll('[data-callout]').forEach(function (el) {
      var r = el.getBoundingClientRect();
      var box = document.createElement('div'); box.className = 'd7-box';
      box.style.left = (r.left + sx - 8) + 'px'; box.style.top = (r.top + sy - 8) + 'px';
      box.style.width = (r.width + 16) + 'px'; box.style.height = (r.height + 16) + 'px';
      var m = document.createElement('div'); m.className = 'd7-mark'; m.textContent = el.dataset.callout;
      var side = el.dataset.side === 'right';
      m.style.left = (side ? r.right + sx - 10 : r.left + sx - 26) + 'px'; m.style.top = (r.top + sy - 26) + 'px';
      document.body.appendChild(box); document.body.appendChild(m);
    });
  }
  function run() { document.querySelectorAll('canvas.pd-halftone').forEach(halftone); annotate(); document.body.dataset.ready = '1'; }
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(run);
})();
