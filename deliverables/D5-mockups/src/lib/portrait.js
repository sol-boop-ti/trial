// Photo slots with an on-brand fallback.
// Each .portrait holds <img class="photo" src="assets/guest.jpg|founder.jpg">. When that file is missing,
// the slot draws a halftone portrait instead: Poolday's scan-dot texture (4px dots on 8px rows in the kit,
// tighter here for small tiles) masked by a rendered silhouette (assets/person.svg). The brand kit says
// "if there is no video, show the halftone, not a placeholder illustration", so this is the fallback.
(function (g) {
  let silhouette = null;
  function loadSil(src) {
    if (silhouette) return silhouette;
    silhouette = new Promise(res => { const im = new Image(); im.onload = () => res(im); im.onerror = () => res(null); im.src = src; });
    return silhouette;
  }
  g.halftonePortrait = async function (slot, o = {}) {
    const photo = slot.querySelector("img.photo");
    const ok = photo && await new Promise(res => { if (photo.complete) return res(photo.naturalWidth > 0); photo.onload = () => res(true); photo.onerror = () => res(false); });
    if (ok) return;
    if (photo) photo.remove();
    const ph = slot.querySelector("img.ph"); if (ph) ph.remove();
    const im = await loadSil(o.src || "assets/person.svg"); if (!im) return;
    const W = slot.offsetWidth, H = slot.offsetHeight, dpr = Math.max(2, window.devicePixelRatio || 1);
    const cv = document.createElement("canvas"); cv.width = W * dpr; cv.height = H * dpr; cv.style.cssText = "position:absolute;inset:0;width:100%;height:100%";
    slot.appendChild(cv);
    // Rasterise the silhouette, framed like a head-and-shoulders shot.
    const off = document.createElement("canvas"); off.width = W; off.height = H; const oc = off.getContext("2d");
    const sc = (o.scale || 1.0) * Math.max(W / 800, H / 900) * 1.05, dw = 800 * sc, dh = 900 * sc;
    oc.drawImage(im, (W - dw) / 2 + (o.dx || 0) * W, H - dh + (o.dy || 0) * H, dw, dh);
    const px = oc.getImageData(0, 0, W, H).data;
    const ctx = cv.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const step = o.step || 3, row = o.row || 5, col = o.color || [245, 245, 245];
    for (let y = 2; y < H; y += row) for (let x = 0; x < W; x += step) {
      const i = (Math.floor(y) * W + Math.floor(x)) * 4, a = px[i + 3] / 255; if (a < 0.05) continue;
      const lum = (px[i] * 0.3 + px[i + 1] * 0.59 + px[i + 2] * 0.11) / 255;
      // Light from above-left: brighter toward the top of the head and the key side.
      const shade = 0.34 + 0.4 * (1 - y / H) + 0.18 * (1 - x / W) + 1.6 * lum;
      const k = Math.min(1, a * shade);
      ctx.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${(0.25 + 0.6 * k).toFixed(3)})`;
      const hh = 0.8 + 2.2 * k; ctx.fillRect(x, y - hh / 2, 1.2 + 0.6 * k, hh);
    }
  };
})(window);
