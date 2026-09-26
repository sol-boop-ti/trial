#!/usr/bin/env bash
# Before/after, side by side: the original (left) and the remake (right), synced at 0.
# The shorter clip holds its last frame. Audio: the remake's.
#   bash compare.sh upflow   → ../upflow-compare.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
n=$1; FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
dur() { { "$FF" -i "$1" 2>&1 || true; } | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}'; }
A=../../../references/review-$n.mp4; B=$n-remake.mp4
DA=$(dur "$A"); DB=$(dur "$B"); D=$(python3 -c "print(max($DA,$DB)+0.5)")
LA="BEFORE · original · ${DA%.*}s"; LB="AFTER · remake · $(printf '%.0f' "$DB")s"
python3 - "$LA" "$LB" /tmp/cmp-labels.png <<'PYL'
import sys
from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
for txt, x0, col in ((sys.argv[1], 12, (170, 170, 170)), (sys.argv[2], 964, (255, 255, 255))):
    w = d.textlength(txt, font=f); d.text((x0 + (944 - w) / 2, 236), txt, font=f, fill=col)
im.save(sys.argv[3])
PYL
"$FF" -loglevel error -y -i "$A" -i "$B" -loop 1 -i /tmp/cmp-labels.png -filter_complex "
 color=c=0x111111:s=1920x1080:d=$D[bg];
 [0:v]scale=944:531,setsar=1,tpad=stop_mode=clone:stop_duration=30,trim=duration=$D[a];
 [1:v]scale=944:531,setsar=1,tpad=stop_mode=clone:stop_duration=30,trim=duration=$D[b];
 [bg][a]overlay=12:300[x];[x][b]overlay=964:300[y];[y][2:v]overlay=0:0:shortest=1,fps=30[v];
 [1:a]apad,atrim=duration=$D[au]" -map "[v]" -map "[au]" -t $D -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$n-compare.mp4"
echo "$n-compare.mp4"
