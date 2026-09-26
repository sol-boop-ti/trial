#!/usr/bin/env bash
# Rebuilds remake/src/_assets (git-ignored: third-party brand assets are not redistributed here).
# Needs: git, python3 (Pillow, numpy, potracer), node 22, ffmpeg (imageio_ffmpeg).
set -euo pipefail
cd "$(dirname "$0")/src"; A=_assets; mkdir -p "$A/posthog" "$A/upflow"; T=$(mktemp -d)
# PostHog: official brand package + website repo (for the Squeak webfont)
git clone -q --depth 1 https://github.com/PostHog/brand.git "$T/brand"
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/PostHog/posthog.com.git "$T/site"
(cd "$T/site" && git sparse-checkout set static/fonts)
cp "$T"/brand/assets/fonts/RoundHog*.woff2 "$T/site/static/fonts/squeak-bold-webfont.woff2" "$A/posthog/"
for h in hourglass rocket megaphone panic chart director experiment; do cp "$T/brand/assets/hoggies/vectors/$h.svg" "$A/posthog/"; done
cat > "$T/ex.ts" <<EOF
import { LOGO_BODY, LOGO_VIEW_BOX, LOGOMARK_PARTS } from "$T/brand/src/logo/geometry.ts";
import { writeFileSync } from "fs";
writeFileSync("$PWD/$A/posthog/logo-landscape-gradient.svg", \`<svg xmlns="http://www.w3.org/2000/svg" viewBox="\${LOGO_VIEW_BOX.landscape}">\${LOGO_BODY.landscape.gradient}</svg>\`);
writeFileSync("$PWD/$A/posthog/logomark-parts.json", JSON.stringify(LOGOMARK_PARTS.gradient));
EOF
node --experimental-strip-types "$T/ex.ts"
# Upflow: Figtree (Google Fonts) + the wordmark traced from the original video's end card
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800" > "$T/f.css"
python3 - "$T/f.css" "$A/upflow" <<'PY'
import re, subprocess, sys
css, out = open(sys.argv[1]).read(), sys.argv[2]; faces = ""
for sub, b in re.findall(r'/\* (\S+) \*/\s*@font-face \{(.*?)\}', css, re.S):
    if sub != "latin": continue
    w = re.search(r'font-weight: (\d+)', b).group(1); u = re.search(r'url\((.*?)\)', b).group(1)
    subprocess.run(["curl", "-s", "-o", f"{out}/figtree-{w}.woff2", u]); faces += f"@font-face{{font-family:Figtree;font-weight:{w};src:url(figtree-{w}.woff2)}}\n"
open(f"{out}/fonts.css", "w").write(faces)
PY
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FF" -loglevel error -y -ss 22 -i ../../../../references/review-upflow.mp4 -frames:v 1 "$T/end.png"
python3 - "$T/end.png" "$A/upflow" <<'PY'
import sys, re, numpy as np, potrace
from PIL import Image
im = Image.open(sys.argv[1]).convert("L").crop((125, 455, 555, 615)); S = 6
a = ~(np.array(im.resize((im.width * S, im.height * S), Image.LANCZOS)) > 150)
subs = []
for c in potrace.Bitmap(a).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2):
    d = f"M{c.start_point.x/S:.2f},{c.start_point.y/S:.2f}"
    for s in c.segments:
        d += (f"L{s.c.x/S:.2f},{s.c.y/S:.2f}L{s.end_point.x/S:.2f},{s.end_point.y/S:.2f}" if s.is_corner
              else f"C{s.c1.x/S:.2f},{s.c1.y/S:.2f} {s.c2.x/S:.2f},{s.c2.y/S:.2f} {s.end_point.x/S:.2f},{s.end_point.y/S:.2f}")
    subs.append(d + "Z")
w = ~a; ys = np.where(w.any(1))[0]; xs = np.where(w.any(0))[0]
x0 = lambda p: min(map(float, re.findall(r'-?\d+\.?\d*', p)[0::2]))
open(f"{sys.argv[2]}/wm-vb.txt", "w").write(f"{xs[0]/S-1:.1f} {ys[0]/S-1:.1f} {(xs[-1]-xs[0])/S+2:.1f} {(ys[-1]-ys[0])/S+2:.1f}")
open(f"{sys.argv[2]}/wm-letters.txt", "w").write(" ".join(p for p in subs if x0(p) <= 380))
open(f"{sys.argv[2]}/wm-dot.txt", "w").write(" ".join(p for p in subs if x0(p) > 380))
PY
rm -rf "$T"; echo "assets ready in src/$A"
