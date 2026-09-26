# D8 (bonus): Poolday's Instagram

## 0. The static story ad (`poolday-static-ad.png`, 1080×1920; `@2x` for print)
One 9:16 image, split screen, almost no copy:
- **Top (42%, greyed): "AI Slop".** A slides app: WordArt "LUMEN 2.0!!!", clip-art, bullet points, a stretched logo.
- **Bottom (58%): the Poolday mark + "Made with Poolday".**
  - A paused frame (0:07 / 0:15) of a professional motion-design video: the Apple-style "phone tunnel" from the user's motion reference, rebuilt for the demo brand **Lumen** (Lumen app screens on every phone, "Plan. Ship. **Grow.**", grain, a motion trail on two phones).
  - Under it, 📎 **"Inspiration attached · Lumen brand kit"**: a 16:9 one-page brand guide (like the user's reference). It has a stacked outline/filled wordmark hero, logo variants, a colour palette with names and hex (Moss, Ember, Sky, Night, Sand), and typography (Bricolage + Inter) with a button. It reads "From lumen.com".
- Poolday's side stays on its brand: black, Inter, the scan-dot halftone. The colour comes only from the customer's video. Lumen is fictional, so there are no rights issues.

## 1. Animated version (`poolday-ad.mp4`, 9:16, 14.4s, with sound)
**The original** (`original-ig-ad-screenshot.png`): a static card, "No AI slop. Just your videos, edited well. Poolday learns your brand and edits every video to it." The idea is right, but:
- nothing happens in the first 3 seconds;
- it tells instead of shows;
- it's set in **monospace + cyan**, which is *off* Poolday's own brand (Inter 400 on black; the brand kit says cyan is for browser chrome only, never text).

**The remake shows the promise instead of stating it:**

| Time | Beat | Why it hooks |
|---|---|---|
| 0–1.6s | Frame 1: "Most AI video tools:" over a garish, misspelled AI ad ("LUMNE", "The futrue of work is hear!!") → a red **AI SLOP** stamp slams at 0.6s | Everyone recognizes slop; it's funny, and it lands in <1s |
| 1.6–2.5s | The card **flips** to the same ad edited well, on brand: "Poolday: your brand, edited well." | A before/after inside one object |
| 2.5–6.7s | "It learns your brand before it edits anything." A URL is typed → the **brand kit** assembles on the beat (logo, colors, type, voice, product UI, each ticked) | Shows the mechanism, not a claim |
| 6.7–10.2s | "Then every video is edited to it." A wall of 12 formats (launch reel, demo, quote, stat, UGC ad, end card…), same logo bug and caption style everywhere; the counter climbs to "12 videos · 1 brand" | Volume + consistency, the real value |
| 10.2–14.4s | **Poolday's own end card** (charcoal, kinetic tagline, slot-machine roll "fast. → on brand. → everywhere. → **well.**", iris-gradient rule that collapses to a centre dash), then the mark + poolday.ai | 100% on their brand kit |

"Lumen" is a fictional demo brand, so there are no third-party rights issues. Built in code with the same engine as the D6 remakes (`../D6-video-review/remake/src/poolday-ad.html`), synthesized soundtrack, real motion blur.

## 2. Fix the profile picture
In the circle crop the logo reads "Poolday.a": the wordmark is cut. **Use the mark alone, centered, with ~25% padding**, and keep "Poolday" in the name field. Proposal: `profile-picture-proposal.png`. The mark was vectorized from a screenshot, so export the real one from Poolday's design files for production.

## 3. Feed the account: short motion use-case videos (one a day)
Each is a 6–10s motion piece made in Poolday, titled with the brand kit's own recipe formula, `<input> to <output>`:
1. **Your URL to a launch film**: paste a site, and the brand kit + launch video appear.
2. **One podcast to 10 clips**: a long waveform splits into 10 captioned vertical clips.
3. **A screen recording to a product demo**: raw Loom on the left, polished demo on the right.
4. **Your logo to a brand kit in 30s**: colors, fonts and UI extracted on the beat.
5. **A viral ad to your ad**: before/after remake of a trending video on your brand.
6. **One video to 5 formats**: 16:9 → 9:16 → 1:1 → captions → end card.
7. **English to 6 languages**: one founder video, voice localized.
8. **One prompt to a UGC farm**: the creators wall filling up.
9. **A lead to a prospect video**: the D3 loop in 8 seconds.
10. **A changelog to a release video**: every Friday, automatically.
11. **Photos + voice to a founder story**.
12. **A webinar to 3 teasers**.

Rules: hook in frame 1, no blur/fade openers (see the pacing finding in D6), on brand (black, Inter, videos carry the colour), and each post ends on the same end card.
