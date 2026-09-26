# D5. Growth idea: "Paste a link. Watch the video."

**The idea.** A free page with three products Poolday already makes well: a **launch video** from your URL, **podcast clips** from an episode link, and an **AI product ad** from a URL plus a product photo. One input, one style card, done: the Submagic mechanic (upload → pick "Hormozi" → done), applied to Poolday's best outputs. Every video ends with a booking offer. We spread it on X by remaking viral "AI made this in one prompt" videos for real in Poolday and replying with the run.

*Proposal only: nothing implemented, as the brief asks (the screens are mockups). Costs below mix what I measured during the assignment with estimates, and each estimate is marked [est.].*

## 1. Flow (four clicks, one field each)

1. **Pick a product:** Launch video · Podcast clips · AI product ad.
2. **Give the input:** website URL · YouTube link or upload · URL + product image.
3. **Pick a style:** a looping preview card. The card *is* the prompt.
4. **Work email**, then the video: shown on the page if renders are fast, emailed if slow. The design works either way.
5. **Result page.** Main button: "Get the full version with us (15 min call)". Second: "Edit it yourself in Poolday".

## 2. Products and styles

| Product | Input | Styles (one-line look) |
|---|---|---|
| **Launch video** (20–30s) | Website URL | **Apple Motion Style:** clean product motion, UI floating on soft gradients, slow camera, hard cuts on the beat. **Kinetic Typo:** bold type animated to the beat, one idea per word. **Storytelling Film:** problem → turning point → product, founder voiceover, calmer pacing. |
| **Podcast clips** (5 × 30–60s, 9:16) | YouTube link or upload | **Hormozi:** 1–3 word bold caps, yellow/green keyword pops, punch-in zooms every few seconds. **Diary of a CEO:** 1–3 words, heavy outline, host yellow / guest white, cinematic two-camera cuts. **MrBeast:** comic-style font, blue active word, fast jump cuts, sound effects. **Ali Abdaal:** desaturated grade with one colour pop, handwritten-style captions beside the speaker, calm. **Iman Gadzhi:** fast cuts, minimal "luxury" text overlays, dynamic zooms, dark premium grade. |
| **AI product ad** (15s) | URL + product image | **3D hero CGI:** product floats and turns in a studio void, macro details, light sweeps. **Faux out-of-home:** giant product placed in a real city (the viral FOOH format). **UGC:** an AI creator holds and reviews the product to camera, captions, phone framing. **Cinematic:** the product in a short lifestyle scene, film grade, one line of copy. |

Evidence: Submagic, Kapwing and Choppity sell Hormozi, MrBeast and Ali Abdaal templates by name; how-to guides exist for the Diary of a CEO and Iman Gadzhi looks; FOOH and AI UGC top the 2026 ad trend lists. View counts not checked (X/YouTube blocked) (unverified).

## 3. What the product looks like

Seven screens in Poolday's app style, in `D5-mockups/` (the full path: `walkthrough.mp4`):
1. `01-link.png`: "Paste a link. Watch the video." Pick Launch Video, Podcast Clips or AI Product Ad, then paste the URL (`01b` shows the product-ad input, `01-link-mobile` the phone layout).
2. `02-recording.png`: "Do you have a screen recording of your product?" Upload one (MP4/MOV, up to 2 min), or "No. Poolday AI records it for you".
3. `03-brand-kit.png`: the brand kit pulled from the site (logo, colours, fonts), shown back to the visitor.
4. `04-style.png`: style cards with looping previews (real reference footage). The card *is* the prompt.
5. `04d-details.png`: "Last step. Your video is already being made." Work email, role, source. Personal emails are refused inline (`04c`).
6. `05-generating-*.png`: progress through screen recording → brand kit → storyboard, with the switch to "we'll email it" if the render is slow.
7. `06-result.png`: the video (watermarked 720p download, HD + 3 variants, try another style, share), and the main button, "Book a 15 min demo": "Want this for your real launch? It takes one call." 

## 4. Why this beats Motion

Motion launched "drop a product URL, get a launch video" inside AI assistants on 2 Aug 2026 (their X post) (unverified). So the launch video alone is not new. Our edge:
- **Three products, not one.** Podcast clips are the high-frequency one: a show ships every week, so users come back weekly. Launch videos happen a few times a year.
- **Generative ads.** Motion is a motion-design agent. The product-ad track uses AI video, which it doesn't lead on (unverified).
- **A human behind the video.** Qualified leads get a call offer for the full version. Motion's flow ends at self-serve.
- **Quality shown in public.** The X remakes put the output side by side with the viral clip.

## 5. Distribution: "Poolday can actually do it"

Find viral posts claiming "[tool] made this video with one prompt". Feed the clip to Poolday as the reference with a strong brief, screen-record the run, and reply with a 20–30s cut plus the link. Reply from the official account, one reply per thread, and only when a human judges the remake at least as good. Never accuse anyone of faking. Skip artists showing hand-made work.
> *"Poolday can actually do it. Full run, no hand edits → [video]. Same style is one click here: [link]"*

## 6. Cost model

**(a) Measured during the assignment.** 1,000 credits = $1 (the $2,000 trial = 2,000,000 credits). Poolday's home page says "~$5–$25 per finished video".

| Run | What it included | Agent time | **Cost** |
|---|---|---|---|
| First video for a new brand (Flam, Wispr Flow) | brand kit + custom teaser + iterations | 50–55 min | **≈ $140–155** [est., pro-rata on agent time] |
| The same brand again, through the automation webhook (D3) | saved kit + saved composition, one message | 4 min | **≈ $11** [est.] |

This product sits between the two: a new brand kit per visitor, but a saved style template instead of a custom build. The bottom-up check below puts it at $3–25.

**(b) Bottom-up sanity check (public API prices, Sept 2026).** What the building blocks cost Poolday; its price adds margin.

| Building block | Public price |
|---|---|
| AI video: Veo 3.1 (fal.ai) | $0.20–0.40/s |
| AI video: Seedance 2.0 720p (fal.ai) | $0.24–0.30/s |
| AI video: Kling 3.0 Pro (fal.ai) | $0.224/s silent, $0.336/s with audio |
| Images: Seedream / Nano Banana (fal.ai) | $0.035–0.15 per image |
| Lipsync (fal.ai: VEED, H3) | $0.05–0.08/s |
| Voiceover: ElevenLabs API | $0.05–0.10 per 1k characters |
| Transcription: ElevenLabs Scribe / AssemblyAI | ~$0.22–0.37 per hour of audio |
| Agent LLM: Anthropic API | $2/$10 (mid tier) to $5/$25 (top tier) per M input/output tokens. Cache reads ~0.1× input. |

Assumption for the agent: a templated run uses ~2M input tokens (70% cached) and ~0.1M output tokens, so **$2–6 per run** [est.].

| Product | What it consumes | **Estimate** |
|---|---|---|
| Launch video, 25s | Agent $2–6 · 5 images ~$0.5 · voiceover <$0.05 · optional 10s AI b-roll $2–3.4 · render ~$0.5 | **~$3–10** [est.] |
| Podcast clips, 5 from a 1h episode | Transcript ~$0.3 · agent $3–8 (moment picking + 5 edits) · b-roll images ~$0.6 · 5 renders ~$1 | **~$5–10 total, ~$1–2 per clip** [est.] |
| AI product ad, 15s | AI video 15s × $0.20–0.40 × ~3 takes = $9–18 · seed images ~$0.5 · agent $2–6 · UGC lipsync +$1 | **~$12–25** [est.] |

This lands inside the reported $5–25, so that figure is plausible. Generative video makes the ad the expensive product. A first build (~7 prompts) costs several times a cloned template (~1–2), so every style ships as a saved template.

**(c) Campaign budget ($15k cap).** Planning mix: 40% launch videos, 30% podcast packs, 30% ads. At mid estimates ($10 / $10 / $25) plus 30% re-renders, the blended cost is **~$19 per delivered video** [est.].

| Stage | Budget | Videos at ~$19 [est.] | Range at $8–30 | Trigger to open the next stage |
|---|---|---|---|---|
| **0. Manual pilot** (2 wks) | ~$2k | ~100 | 65–250 | Cost per video measured (table a), ≥5 booked demos |
| **1. Public page** (3–4 wks) | ~$5k | ~260 | 165–625 | Cost per booked demo ≤ Poolday's current paid cost per demo (unverified) |
| **2. Scale** | ~$8k | ~420 | 265–1,000 | Same ratio holds at higher volume |
| **Total** | **$15k** | **~790** | 500–1,900 | |

Credits go only to qualified leads (work email on a matching domain, B2B, ~10–500 people). Everyone else joins a queue or gets the cheapest tier. At 5% video → demo, $19 per video is **~$380 per booked demo** [est.].

## 7. How it runs

- **Per request:** "Create a brand kit for [URL]", then clone the saved style template with `brand:name` (~2 prompts per the agent guide).
- **Automation:** proven in D3. The page POSTs the request to a Poolday Automation webhook, and the agent runs the saved template (the D3 run: 1 message, 4 min). What's missing is the way back: the Automation can't call a URL when the video is done, so the pilot needs Poolday's API or an Output webhook, or an operator who relays the link.
- **Render time:** a full production took 50–55 min; the reused-template run took 4 min. A new visitor needs a new brand kit on top, so the pilot measures it. That number decides on-page vs email delivery.

## 8. Targets (confirm in the pilot)

Visit → submission ≥20% · submissions that qualify ≥30% · qualified video → booked demo ≥5% · cost per demo below the current paid channel · ≥1 X remake a week that clearly beats normal Poolday posts.

## 9. Real risks

1. **Uneven quality on arbitrary inputs.** A bad video of someone's own product is worse than none. *Mitigation:* ship only styles that pass a 10-input test; a human checks every video before it goes out.
2. **AI ad cost.** At ~$12–25 each, ads can eat the budget. *Mitigation:* ads go to qualified leads only, with a daily credit cap per product.
3. **Motion owns "URL → launch video".** *Mitigation:* lead with podcast clips and ads, prove quality publicly with the X remakes, and sell the human call.
