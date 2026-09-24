# D5. Growth idea: "Paste your URL, get your launch video"

> **Pitch.** A one-field page: paste your website, pick a trending style, and get a real launch video made by Poolday in your inbox. It spreads through "Poolday can actually do it" replies on X, and every video ends with a 15-minute demo offer.

*Status: proposal only (not implemented, per the brief). Numbers marked **[A]** are assumptions to check in the pilot. I have no access to Poolday's internal pricing, credit costs or customer data.*

---

## 1. Why this books demos, not just signups

Most "free tool" funnels stop at a signup. This one is built so that the **free video is the sales conversation**:

```
X reply / tag  →  landing page  →  URL + style  →  work email (gate)  →  enrichment
   → video arrives by email (~1h+)  →  watch  →  "Want this for your launch? Book 15 min"
                                           ↘ HD / edit → account (self-serve)
```

- **The prospect gets a video of their own product** in their brand, before they've spoken to anyone. That shows the result, which a feature list can't.
- **The ~1h+ render time helps here.** The email is collected up front, before the value arrives, so every submission becomes a lead.
- **Qualification happens before any credits are spent.** B2B leads get the best render and a demo CTA. Everyone else gets a lighter render and the self-serve path (see §5).
- **The demo offer is concrete, not generic.** It's "we'll turn this into your real launch video, plus 3 variants, on a 15-minute call." The call continues something they already hold.

## 2. Product experience

**One screen. No long copy.** Headline: *"Paste your URL. Watch your launch video."* A single input field ("or describe your idea") and a row of style cards, each a looping 3-second preview:

| Style template | What it looks like | Best for |
|---|---|---|
| **Apple-style motion** | White space, product floating in 3D, slow eased camera, big type reveals | Hardware-like or premium SaaS |
| **Linear-style dark UI** | Dark gradient, glowing UI panels assembling, crisp micro-interactions | Dev tools, B2B SaaS |
| **Kinetic typography** | Bold words hitting on the beat, fast cuts, one idea per frame | Launch announcements, fundraises |
| **3D product world (three.js)** | UI screenshots rebuilt as 3D objects, continuous fly-through | "Most impressive" prospect style |
| **"One prompt" X-viral** | The glossy motion-designer style that goes viral as "AI made this in one prompt" | Shareability, the X engine |
| **Founder UGC** | AI presenter in selfie framing, captions, hook in the first 2 seconds | Paid social, TikTok/IG |

**Flow (under 60 seconds of user effort):**
1. Paste URL → pick a style → pick a format (16:9 / 9:16 / 1:1).
2. **Email gate:** "Your video takes about an hour. Where should we send it?" A work email is suggested. Free-mail addresses are accepted but deprioritized (§5).
3. **Instant feedback while waiting:** the brand kit preview (logo, colours, fonts pulled from the URL) appears on screen within minutes. This proves "it understood my brand" and keeps them engaged.
4. **Delivery email:** a watermarked 720p preview on a hosted share page (the watermark reads "Made with Poolday · make yours").
5. **Unlocks:** HD download, removing the watermark, and editing in Poolday's live editor all require an **account**. The share page has **"Want this for your launch? Book 15 min"** as its main button, with a calendar embed (no form), and "Edit it yourself" as the secondary button.

**The Submagic comparison.** Submagic's mechanic is upload → pick "Hormozi" → done. Users get something that already looks like a known creator's style, with zero creative decisions. We copy that exactly: **the style card is the whole prompt.** The difference is that Submagic sells a self-serve subscription tool, while our output is a showcase that opens a sales conversation.

## 3. How it runs on Poolday

| Step | Poolday capability used (from the agent guide) |
|---|---|
| URL → brand | "Create a brand kit for [x]" from a website. App screenshots are rebuilt into animatable pieces, then applied as `brand:name` |
| Style | One **saved template + `/command` per style**, built once on a Max run and then iterated until reliable (first video ≈ 7 prompts, later ones ≈ 1–2) |
| Per request | **Clone the template** with the new brand kit ("another one like X but for [brand]") |
| Tiers | **Light** for free-mail/unqualified previews. **Standard/Max** for qualified B2B leads and X remakes |
| Variants | "3 variants" in one conversation. Reserved as the demo-call hook |

**Hard dependency: an API or internal pipeline.** The agent guide documents no public API, so a self-serve page cannot trigger runs today. Two options:
- **(a) Internal pipeline (recommended for the pilot):** Poolday's team exposes an internal endpoint (submit brand-kit + template-clone job, then poll status and fetch the output URL). This is a small engineering task that needs sign-off from the Poolday team.
- **(b) Human-in-the-loop pilot:** submissions land in a queue and an operator pastes the 2-line `/command` into Poolday. That covers roughly 40–60 videos a day per operator **[A]**. It's enough to validate demand before any engineering.
- Either way we need **job queueing, a per-day credit cap, output QA** (auto-reject blank or broken renders) and **video hosting** for the share pages.

## 4. Distribution engine: "Poolday can actually do it"

**The play.** Motion designers and AI accounts post viral "Claude/GPT made this video with one prompt" clips, and many are faked or heavily hand-edited. We **actually remake the video in Poolday**: pull the reference from the link (Poolday accepts YouTube/TikTok/IG links; for X clips, we download and upload the file), then run a strong brief on Max/Ultra. We **screen-record the run** (prompt → agent working → render) and reply with a 20–30s cut plus the link.

**Precedent.** Motion/Mosaic replied to big X threads with "tag @motion.so to get a video explaining this thread", which turned their product into a public reply bot.

**The "tag @poolday" variant (phase 2).** Anyone can reply "@poolday make this" under a post. A mention watcher (X API) adds it to the queue. It's prioritized by follower count and thread size, gets a Light render and a human QA check, and then Poolday replies with the video plus "make one for your product → link". Limit: 20 per day **[A]**.

**Targeting rules.**
- The thread is about AI video, motion design, SaaS launches or AI tools, **and** it has ≥250k views or ≥1k likes, **and** it's under 12h old **[A]**.
- **Priority:** threads from B2B founders and marketers (the ICP can see them), and "one prompt" claims we can genuinely match.
- **Skip:** politics, harassment threads, individual artists showing their own hand-made work (we remake AI-bait, not artists' craft), and anything we can't match in quality.
- To handle the 1h+ render delay, **pre-build the 6 style templates**. Most viral clips map to one of them, so a remake is a template clone and not a new video. If a reply lands late, quote-post it from the Poolday account instead.

**Tone.** Be helpful and a little cheeky, never a dunk. Show the process, not just a claim. One link at most. No hashtags. Never accuse the original poster of faking.

**Example replies.**
1. *"Couldn't resist trying this one for real. Here's Poolday rebuilding it from the reference, uncut, 1 prompt → [video]. Want it for your product? Paste your URL: [link]"*
2. *"Screen recording of our agent making a version of this, brand kit to final render → [video]. Same style is a 1-click template here: [link]"*
3. *"We tried the 'one prompt' test honestly: 2 prompts, ~1h, no hand edits. Full run → [video]. Try it on your site: [link]"*

**Anti-spam rules.**
- ≤3 remake replies/day. Never the same reply text twice. One reply per thread, never repeated.
- Only post when a human QA pass says the remake is at least as good as the original.
- Reply from the official Poolday account (plus the founder's account, if they opt in). No sockpuppets, no bulk tagging.
- Stop immediately if the original author objects.

## 5. Lead qualification and routing

Scored at the email gate, before any credits are spent:

| Signal | Source | Weight |
|---|---|---|
| Work email; email domain matches the submitted URL | Email + URL compare | High |
| Company size 11–500, funded (Seed–Series C), B2B | Domain enrichment (Clearbit/Apollo-type provider) | High |
| Role: founder, marketing, growth, product marketing | Enrichment / optional 1-click field "your role" | Medium |
| Came from a qualified X thread or a "tag @poolday" request | UTM | Low |
| Free-mail, no company, or the URL is someone else's brand | Rules | Negative |

**Routing:**
- **A (qualified, score ≥70):** Standard/Max render + **3 variants**, a personal email from a human salesperson with the video, and the demo CTA front and centre. Alert in the sales channel within 5 minutes.
- **B (plausible):** Light render, share page with the demo CTA, a 3-email nurture sequence.
- **C (random/consumer):** Light render once there's spare capacity (or a waitlist), self-serve signup CTA, no sales touch.

## 6. Budget (up to $15k, unlocked in stages)

Per-render credit cost is **unknown to me [A]**. The caps below are expressed as spend, and the render counts are derived from the measured cost after day 2.

| Line item | Pilot ($3k) | Scale (+$12k) |
|---|---|---|
| Landing page, queue, email, share pages (built in-house with Claude Code/no-code) | $600 | $1,000 |
| Style templates (6 × Max build + tuning, one-off) | $500 | $500 (new trending styles) |
| Render credits, capped daily | $1,200 | $6,500 |
| X remakes (Max/Ultra) + operator/motion QA | $400 | $2,000 |
| Enrichment + X API access | $200 | $500 |
| Paid boost of the best 2–3 remakes | $100 | $1,500 |

**Abuse prevention:** email verification before render · **one free video per domain** · rate limits per IP and per device · daily global credit cap with a waitlist once it's reached · Light tier by default, higher tiers only for score A · block competitor or famous-brand URLs that aren't the submitter's (no fake ads for brands you don't own) · manual QA before X replies.

## 7. Metrics, targets and pilot

| Metric | Pilot target (2 weeks) **[A]** |
|---|---|
| Landing visits → submissions | ≥25% |
| Submissions/day | 30 by week 2 (capped by credits) |
| Verified email capture (of submissions) | ≥85% |
| Qualified (score A) share | ≥30% |
| Video watched (email → share page) | ≥60% |
| Demo booked (of score A) | ≥8% |
| **Booked demos** | **≥10** |
| **Cost per booked demo** | **≤$300 pilot → ≤$150 at scale** |
| X reply impressions | ≥500k total; ≥1 remake over 100k |

**Decision rule after 2 weeks:**
- **Scale** (unlock the next $6k, then the final $6k after 2 more weeks at target): ≥10 demos **and** cost per booked demo ≤$300 **and** the qualified share ≥25%.
- **Iterate one more week** (no new money): demos are 5–9, or the qualified share is low while watch rate is high. Fix targeting or the CTA.
- **Kill:** <5 booked demos, **or** the qualified share <15% (it's attracting consumers, not buyers), **or** render QA failure >20%.

**2-week pilot plan:**
- **Days 1–3:** build 6 style templates in Poolday and save them as `/commands`. Measure prompts and credits per clone. Ship the landing page and email gate. Choose the pipeline (internal endpoint vs operator queue).
- **Days 4–5:** soft launch to 50 hand-picked ICP founders (fresh Series A/B, from the D3 agent loop). Measure watch rate and demo rate. Fix the weakest template.
- **Days 6–10:** turn on the X engine: 2–3 remake replies per day, and 1 remake + screen recording as a post on the Poolday account. Daily review of the funnel dashboard.
- **Days 11–14:** trial "tag @poolday" at a cap of 10 per day. Boost the best remake. On day 14, apply the scale/kill rule.

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| 1h+ render time kills momentum | Email delivery + instant brand kit preview; pre-built templates; quote-posts for late X replies |
| Uneven quality embarrasses the brand | Only ship templates that pass a 10-URL reliability test; automated and human QA; a "regenerate" button |
| Credit burn from consumers or bots | Email gate, one per domain, Light tier by default, daily cap, scoring before spending |
| No API → the pipeline doesn't scale | Operator queue for the pilot; internal endpoint only if the pilot hits target |
| Backlash for "calling out" creators | Never accuse anyone; remake with credit; skip human artists; stop if asked |
| X account flagged as spam | ≤3 replies/day, unique copy, human QA, official account only |
| IP / trademark (videos of brands) | Users only for domains they own (email domain match for HD); famous-brand blocklist |

## 9. Why now, and why Poolday

- **Why now:** "AI made this in one prompt" videos are one of the biggest engagement formats on X right now, and many are overclaimed. Replying with a real, screen-recorded run stands out in that feed.
- **Why Poolday specifically:** the idea works because of capabilities Poolday already has. It builds a **brand kit from a URL**, rebuilds **screenshots into animatable pieces**, supports **saved templates/commands with cloning** (so each extra video costs about 1–2 prompts), and uses an **agent that runs end to end**, which is exactly what makes a screen recording convincing. A plain text-to-video model can't show a brand-accurate launch video made from just a URL.
- **It compounds with the other deliverables:** the style templates are reused for prospect videos (D2), the qualification rubric is shared with the agent loop (D3), and the home page gets its "instant value" entry point (D7).
