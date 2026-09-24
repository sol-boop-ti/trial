# D5. Growth idea: "Paste your URL, get your launch video"

**The idea.** A one-field page: paste your website, pick a well-known style, get a launch video of your product made by Poolday. We spread it by replying to viral "AI made this in one prompt" posts on X with a real Poolday remake, and every video ends with an offer to book a demo.

*Proposal only. Poolday's credit costs, render times and API aren't known to me. The pilot measures them.*

## 1. User flow

1. Paste your URL.
2. Pick a style card (a looping preview). The card is the whole prompt, like "Hormozi" in Submagic.
3. Enter a work email. That's the only field.
4. Get the video: on the page if renders are fast, by email if they're slow. The design works either way.
5. Share page. Main button: "Turn this into your real launch video (15 min call)". Second: "Edit it yourself".

## 2. Templates

From web search (Sept 2026). View counts not checked: YouTube and X were blocked.

| Style | Why people recognize it | Evidence |
|---|---|---|
| **Apple-style product motion** (incl. Liquid Glass UI) | Best-known "premium" look; asked for by name. | Many 2025–26 YouTube tutorials; paid courses "Master Viral Apple UI Motion Graphics" (Udemy, Skillshare) |
| **Kinetic typography** | Bold words on the beat; fits any launch | Top 2026 trend (Renderforest, GarageFarm, VideoBolt) |
| **3D CGI product ad** (Blender style) | "Floating product, orbit camera" ads; for SaaS the UI is the object | TikTok topic "Blender 3D product ads"; tutorials on "viral CGI product animations" |
| **"One prompt" code motion graphics** | The look of the viral "one prompt" X posts; ties to the replies | "Claude Code + Remotion" tutorials (one reports 15k views); open-source skills on GitHub |
| **Founder / UGC presenter with bold captions** | Submagic/Hormozi caption style; native to TikTok, Reels, paid social | Well known, not verified here |

## 3. Distribution: X replies

**How.** Find viral posts claiming "[model] made this video with one prompt". Give the clip to Poolday as the reference, with a strong brief. Screen-record the run, then reply with a 20–30s cut and the link. Most clips match a template above, so a remake is mostly a clone.

**Where:** recent, high-reach threads about AI video, motion design, SaaS launches or AI tools, preferably ones B2B founders and marketers read. Skip artists showing their own hand-made work.

**Rules:** reply from the official Poolday account. Only post remakes a human judges at least as good as the original. Never accuse anyone of faking. One reply per thread.

**Example replies:**
- *"Tried this one for real in Poolday. Uncut screen recording, reference to final render → [video]. Want one for your product? Paste your URL: [link]"*
- *"Poolday can actually do it. Here's the full run, no hand edits → [video]. Same style is a template here: [link]"*

**Precedent:** Motion/Mosaic replied to big threads with "tag @motion.so to get a video explaining this thread". In August 2026 Motion also announced a URL→launch video skill inside Claude.

## 4. From free video to booked demo

- **Qualified lead:** email domain matches the submitted URL, B2B company of ~10–500 people (via an enrichment tool), founder/marketing/product role.
- **Qualified leads** get a higher tier, a second variant, and a personal email from sales within 24h offering the full launch version on a call.
- **Everyone else** gets the standard video and self-serve path. Free-mail and URLs the submitter doesn't own are deprioritized (famous brands refused).

## 5. How it runs on Poolday, and what's unknown

- **Per request:** "Create a brand kit for [URL]", then clone the saved template with `brand:name` (the guide says a saved /command takes ~2 prompts).
- **Automation (unknown):** no public API is documented. The pilot uses an operator queue; automation only if Poolday exposes an internal endpoint.
- **Render time (unknown):** full productions "can take an hour or more"; Light is for fast, small tasks, so a cloned template may be much faster. Measured on days 1–2.
- **Cost per video (unknown):** measured per template and tier; it sets the daily cap.

## 6. Budget and pilot (up to $15k, released in stages)

| Stage | Budget (est.) | What happens | Trigger for the next stage |
|---|---|---|---|
| **0. Manual pilot** (2 weeks) | ~$2k | Build 5 templates, measure time/cost, videos for ~50 hand-picked ICP companies, 2–3 X remakes/day | ≥5 booked demos, and a known cost per video |
| **1. Public page** (3–4 weeks) | ~$5k | Public page with daily credit cap; automation if possible | Cost per booked demo ≤ Poolday's current cost per demo (to confirm) |
| **2. Scale** | ~$8k | Raise cap, add styles, boost best remakes | Same ratio holds as volume grows |

## 7. Metrics (all targets, to be confirmed with the pilot)

- Page visit → submission: **target ≥20%**
- Share of submissions that qualify: **target ≥30%**
- Qualified video → booked demo: **target ≥5%**
- Cost per booked demo: **target below the current paid channel's cost**
- X remakes: **target ≥1 reply/week that clearly outperforms normal Poolday posts**

## 8. Real risks

1. **Quality varies across arbitrary URLs.** A bad video of someone's own product hurts more than none. *Mitigation:* ship only templates that pass a ~10-site test; human check before sending or posting.
2. **Unknown cost and throughput.** Without an API, volume is capped by operator time; if videos are expensive, only qualified leads get one. *Mitigation:* stage 0 measures both before launch.
3. **Not novel.** Motion already offers URL→launch video. *Mitigation:* compete on output quality (shown publicly in the remakes) and the human demo offer, not the mechanic.
