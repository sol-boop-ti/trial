# D6 bonus: the two videos, remade

The review (`../D6-video-review.md`) says what's wrong. These two remakes show the fix. Both are built in code (HTML/CSS timeline → frame-exact capture with 3-sub-frame motion blur → H.264), 1920×1080, 30 fps. Brand kits and sources: `BRAND-KITS.md`.

| | Original | Remake |
|---|---|---|
| Upflow | 23.3s, scenes 1–2s too long, the product never appears, the proof is micro-text | **15.4s** · `upflow-remake.mp4` · `upflow-compare.mp4` |
| PostHog | 24.4s, 3D clay renders (off-brand), the old logo, a slide-style end card | **19.4s** · `posthog-remake.mp4` · `posthog-compare.mp4` |

## Upflow: every fix from the review, applied
| Time | Shot | Fixes |
|---|---|---|
| 0.0–1.4 | The question is already half-typed and finishes at ~26 characters/s | No empty first second; the hook reads in ~1s |
| 1.4–3.7 | The swarm grows outward in 6 languages (a golden-angle spiral), the camera pulls back, then a whip | Same idea, 2s shorter, denser |
| 3.7–4.6 | "Something simple." as **one** card, the words masked up | 3s and 2 cards → 0.9s and 1 card |
| 4.6–10.3 | **The payoff:** the Upflow app. The same question typed in search → Acme Corp → invoice #2041 → the activity timeline (reminder sent automatically → portal opened → paid) → the chip flips from "Due in 3 days" to **"Paid · 3 days early"**; slow push-in | The missing beat: the product answers the opening question |
| 10.3–12.3 | **−79%** counts up, "invoices 31+ days overdue · WorkMotion, with Upflow" | The best line in the video, promoted from footer micro-text to a hero card |
| 12.3–15.4 | The wordmark rises, **the period drops in last**, the divider draws, the tagline and upflow.io; a slow drift | Logo in ≤0.8s and alive, not typed over 4s |

## PostHog: same story, in PostHog's own medium
| Time | Shot | Brand rule it follows |
|---|---|---|
| 0.0–2.45 | "Launch day." A `# launch` chat window ("is it live yet?", "where is the launch?") + the **hourglass hog**, slowly tipping | PostHog OS windows; a real hog, puppet-style entrance |
| 2.45–4.35 | A big 3D "Ship it" button (hard shadow, a real press), the cursor clicks, the **rocket hog** launches, a small camera shake | "Pressing down" button feel from the brand's interaction rules |
| 4.35–5.85 | **IT'S LIVE.** in Squeak (uppercase, with the **megaphone hog**) + flat brand-color confetti | Squeak only uppercase and only next to hog art |
| 5.85–8.9 | "Then the questions start." Sticky notes slap in ("Where do people drop off?", "Which dashboard is right??", "Another tool??") + the **panic hog**; everything gets swept away | The original's "so many tools" beat, in 2D |
| 8.9–15.2 | "Every answer, in one place." One PostHog window whose nav highlight glides through 3 products: **Product analytics** (the line draws, a "Launch" annotation, 12,408 users labeled directly on the line), **Session replay** (Hogflix pricing page, **rage click ×47** on Upgrade), **Feature flags** (the fix rolls out 10% → 100%). One hog per beat (chart, director, experiment) | "Show, don't tell"; synthetic data that tells a story (their handbook's own 47-clicks example); charts labeled directly, annotated at the launch |
| 15.2–19.4 | The **official 2026 logo**, the logomark doing the app's own jump (head first), the wordmark, "One platform for people who build things.", posthog.com in link red; a second small jump, then still | Never the old logo; approved motion only; ends on a still frame |

## Rebuild
```bash
bash fetch-assets.sh                                  # brand assets → src/_assets (git-ignored)
cd src && python3 -m http.server 8777 &
NODE_PATH=/opt/node22/lib/node_modules node capture.js upflow posthog
open http://127.0.0.1:8777/upflow.html                # live preview loop
```

## Honest limits
- **No music or sound design.** Both would be added in the edit, cut on the beats above.
- **The Upflow UI is a reconstruction.** Swap in real product screens for a public version.
- **PostHog's hedgehogs are licensed art.** This is a private spec piece; don't post it without PostHog's OK.
