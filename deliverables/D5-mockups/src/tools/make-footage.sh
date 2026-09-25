#!/usr/bin/env bash
# Turn a reference clip into a deterministic image sequence for a style preview tile.
# Usage: tools/make-footage.sh <name> <input.mp4> [start_s] [duration_s]
#   name: kinetic | apple | storytelling   (the tile picks it up from assets/footage/<name>/)
set -euo pipefail
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
N=$1; IN=$2; SS=${3:-0}; T=${4:-12}; D="$(dirname "$0")/../assets/footage/$N"
rm -rf "$D"; mkdir -p "$D"
"$FF" -v error -ss "$SS" -t "$T" -i "$IN" -vf "fps=15,scale=640:-2:flags=lanczos" -q:v 4 "$D/f%04d.jpg"
n=$(ls "$D" | grep -c jpg); echo "{\"fps\":15,\"frames\":$n}" > "$D/manifest.json"; echo "$N: $n frames"
