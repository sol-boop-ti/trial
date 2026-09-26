"""Builds the light, web-ready media for the final page (deliverables/final/index.html).

Videos: H.264, CRF 26-27, AAC 96k, +faststart, scaled for the web. Each gets a JPEG poster.
Images: JPEG, max 1600px wide. Output: deliverables/final/media/ (git-ignored, rebuild any time).
    python3 deliverables/final/build_media.py
"""
import os, subprocess
from PIL import Image
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(D, "final", "media")
os.makedirs(OUT, exist_ok=True)

# name: (source, scale filter, crf, poster time in s)
VIDEOS = {
    "d1-ugc-farm": ("D1-linkedin/infinite-ugc-farm.mp4", "scale=864:1080", 26, 9.5),
    "d2-flam": ("D2-prospect-videos/flam-series-b-teaser.mp4", "scale=1280:720", 26, 17.4),
    "d2-wispr": ("D2-prospect-videos/wispr-flow-meetings-teaser.mp4", "scale=1280:720", 26, 3.5),
    "d5-walkthrough": ("D5-mockups/walkthrough.mp4", "scale=1280:800", 27, 1.0),
    "d6-upflow-remake": ("D6-video-review/remake/upflow-remake.mp4", "scale=1280:720", 26, 8.0),
    "d6-posthog-remake": ("D6-video-review/remake/posthog-remake.mp4", "scale=1280:720", 26, 11.0),
    "d6-upflow-compare": ("D6-video-review/remake/upflow-compare.mp4", "scale=1280:720", 27, 9.0),
    "d6-posthog-compare": ("D6-video-review/remake/posthog-compare.mp4", "scale=1280:720", 27, 12.0),
    "d7-home-meet": ("D7-pages/video/home-meet-poolday.mp4", "scale=1280:800", 27, 4.0),
    "d7-b2b-use-cases": ("D7-pages/video/b2b-use-cases.mp4", "scale=1280:800", 27, 11.0),
    "d8-ad": ("D8-instagram/poolday-ad.mp4", "scale=720:1280", 26, 0.9),
}
# name: (source, max width)
IMAGES = {
    "d3-dashboard": ("D3-loop/screenshots/03-dashboard-leads.jpg", 1600),
    "d3-poolday-done": ("D3-loop/screenshots/06-poolday-video-done.jpg", 1600),
    "d3-human-check": ("D3-loop/screenshots/10-dashboard-human-validation.jpg", 1600),
    "d3-email": ("D3-loop/wispr-flow-email-preview.png", 1400),
    "d4-8-reels": ("assets/d4/poolday-ugc-reels-8x.jpg", 1600),
    "d5-link": ("D5-mockups/01-link.png", 1440),
    "d5-result": ("D5-mockups/06-result.png", 1440),
    "d7-home": ("D7-pages/compare/home-compare-fold.png", 1800),
    "d7-b2b": ("D7-pages/compare/b2b-compare-fold.png", 1800),
    "d7-pricing": ("D7-pages/compare/pricing-compare-fold.png", 1800),
    "d8-static-ad": ("D8-instagram/poolday-static-ad.png", 900),
    "d8-original": ("D8-instagram/original-ig-ad-screenshot.png", 600),
    "d8-profile-pic": ("D8-instagram/profile-picture-proposal.png", 900),
    "appendix-pletor": ("assets/pletor-ugc-farm.webp", 1600),
}


def run(*a):
    subprocess.run([FF, "-y", "-loglevel", "error", *a], check=True)


for name, (src, scale, crf, t) in VIDEOS.items():
    src = os.path.join(D, src)
    run("-i", src, "-vf", scale + ",setsar=1", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", os.path.join(OUT, name + ".mp4"))
    run("-ss", str(t), "-i", src, "-frames:v", "1", "-vf", scale, "-q:v", "4", os.path.join(OUT, name + ".jpg"))

for name, (src, w) in IMAGES.items():
    im = Image.open(os.path.join(D, src)).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".jpg"), quality=82, optimize=True, progressive=True)

# The IG profile screenshot: keep the stats and the reels grid, drop the row of other people's profiles.
src = Image.open(os.path.join(D, "assets/d4/profile-3-reels.png")).convert("RGB")
top, grid = src.crop((0, 0, src.width, 690)), src.crop((0, 1560, src.width, 2310))
prof = Image.new("RGB", (src.width, top.height + grid.height)); prof.paste(top, (0, 0)); prof.paste(grid, (0, top.height))
prof.resize((600, round(prof.height * 600 / src.width)), Image.LANCZOS).save(os.path.join(OUT, "d4-profile.jpg"), quality=82, optimize=True, progressive=True)

for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if f.endswith(".jpg"):
        with Image.open(p) as im:
            print(f"{f:28} {os.path.getsize(p) // 1024:6} KB  {im.width}x{im.height}")
    else:
        print(f"{f:28} {os.path.getsize(p) // 1024:6} KB")
print("total", sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024 // 1024, "MB")
