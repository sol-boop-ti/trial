# D6 bonus: the two videos, remade

The review (`../D6-video-review.md`) says what's wrong. These two remakes show the fix. Both are built in code (HTML/CSS timeline → frame-exact capture with 5-sample motion blur → H.264), 1920×1080, 30 fps. Brand kits and sources: `BRAND-KITS.md`.

| | Original | Remake |
|---|---|---|
| Upflow | 23.3s, scenes 1–2s too long, the product never appears, the proof is micro-text | **16.4s** · `upflow-remake.mp4` · `upflow-compare.mp4` |
| PostHog | 24.4s, 3D clay renders (off-brand), the old logo, a slide-style end card | **19.8s** · `posthog-remake.mp4` · `posthog-compare.mp4` |

Version 2 (current) is built to show off: 3D cameras, match cuts on brand elements, a synthesized soundtrack with every hit on its frame, and real 180° motion blur. Version 1 (calmer) is kept in `src/*-v1.html`.

## Upflow: "the dot" (Upflow's period is the hero)
| Time | Shot |
|---|---|
| 0.0–1.5 | Macro on the caret; the camera pulls back as "Did Acme pay invoice #2041 yet?" types (key clicks on every letter) |
| 1.5–3.6 | A 3D dolly back with a slow orbit: 64 questions in 6 languages pop into a deep field around it, the beat kicks in, then doubles |
| 3.6–4.0 | **Implosion:** the whole swarm is sucked into one point, and it becomes Upflow's blue dot |
| 4.0–5.9 | The dot swallows the frame blue → "Something simple." The period of "simple." grows into a hole that reveals the next scene (dot-to-dot match cut) |
| 5.9–10.6 | The Upflow app swings in from a 38° 3D tilt; the question types in search; results cascade; **the brand dot travels the payment journey** (sent → reminder → portal → paid), lighting each step on the beat; it turns green, arcs up and **stamps the chip: "Paid · 3 days early"** (ding + ring); push-in |
| 10.6–12.6 | Whip pan to navy: **−79%** on odometer reels with motion blur; 6 "overdue" bars shrink by 79%; WorkMotion credit |
| 12.6–16.4 | A blue dot drops, squashes, and floods the frame; the wordmark rises; **a white dot falls and lands exactly on Upflow's period**; divider, tagline, upflow.io |

## PostHog: "launch day" in PostHog OS
| Time | Shot | Brand rule it follows |
|---|---|---|
| 0.0–2.55 | Close on one "is it live yet?" DM; the camera pulls back as 24 chat windows pop open on the beat around the **hourglass hog**, which slowly tips; then everything is flung off-screen | PostHog OS windows; real hog, puppet-style |
| 2.55–4.4 | The "Ship it" button drops and squashes; cursor click → shockwave → the **rocket hog** launches; the camera chases it up through speed lines | The brand's "pressing-down" button |
| 4.4–5.9 | **IT'S LIVE.** Squeak letters slam down one per beat with camera shake; the **megaphone hog** blasts sound rings and brand-color confetti | Squeak uppercase, only next to hog art |
| 5.9–9.0 | "Then the questions start." 40 sticky notes rain down faster and faster; the frame trembles; the **panic hog**; then the PostHog window whips in and shoves the pile away | The original's "too many tools" beat, in 2D |
| 9.0–15.3 | "Every answer, in one place." Whip-pans inside one PostHog window: **analytics** (the line draws with a live dot; the "Launch" flag drops; 12,408 counts up), **session replay** (Hogflix pricing, **rage click ×47** with shake and ripples), **feature flags** (the fix rolls out 10% → 100%; toast). One hog per beat | Real product UI, synthetic data that tells a story (the handbook's own 47-clicks example), direct labels, an annotation at the launch |
| 15.3–19.8 | **The official 2026 logomark lands part by part on the beat, head first** (the landing half of the app's own jump); wordmark; tagline; posthog.com in link red; one real logomark jump, then still | The current logo only; approved motion; ends on a still frame |

## Soundtrack
`src/sound.py` synthesizes everything from the page's cue list (`window.CUES`): a 120 bpm bed (kick, hats, bass, sidechain pump, pads), whooshes, risers, impacts, UI pops, clicks, keystrokes and a "paid" ding. Every hit sits on its frame. It's normalized to −14 LUFS. No samples or licensed music are used. A pro music bed would still be swapped in for a public version.

## Rebuild
```bash
bash fetch-assets.sh                                  # brand assets → src/_assets (git-ignored)
cd src && python3 -m http.server 8777 &
NODE_PATH=/opt/node22/lib/node_modules node capture.js upflow posthog
bash compare.sh upflow; bash compare.sh posthog     # before/after side by side
open http://127.0.0.1:8777/upflow.html                # live preview loop
```

## Honest limits
- **The soundtrack is synthesized** (tight to the picture, but not a composer's work).
- **The Upflow UI is a reconstruction.** Swap in real product screens for a public version.
- **PostHog's hedgehogs are licensed art.** This is a private spec piece; don't post it without PostHog's OK.
