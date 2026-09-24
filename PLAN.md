# Poolday Assignment: Execution Plan

48-hour assignment with 7 deliverables. You win on **parallelization** (several Poolday conversations rendering while you work on something else) and on **documenting your method** as you go.

> Note: `poolday.ai` is blocked from this cloud session, so I couldn't read the agent guide. **Read https://poolday.ai/agent-guide yourself first (15 min)** and fix anything below that contradicts it, especially API access, credit costs and render times.

---

## 0. Ground rules for the whole project

| Rule | Why |
|---|---|
| Always use **Align** mode in Poolday, not Clarify | Tip from the brief |
| Don't paste Claude-written prompts blindly into Poolday | Poolday's agent knows video editing better than Claude. Use Claude for the *intent* (story, hook, audience) and let Poolday decide the *execution* |
| Run **3–5 Poolday conversations at once** on different variants, then consolidate the best | Parallelization is what the brief asks for |
| Keep a **`LOG.md`**: timestamp, tool, prompt, result, credits spent, what you learned | This becomes your "how I did it / my methods" section |
| Screenshot or screen-record every key moment (prompt, iterations, final render, loop dashboard, IG stats) | Evidence for the deliverable |
| Track credits ($2,000 total) | Report spend per deliverable at the end |

**Measure render time yourself.** Log the start and end of each Poolday run in `LOG.md` during the first hour. Your whole schedule depends on that number. (About "1 hour per run": that wasn't said in this session and isn't a known number. Treat it as unknown until you've timed it.)

### Tool roles
- **Claude (chat):** strategy, copywriting (LinkedIn post, emails), critique of videos and pages, growth-idea write-up. Paste screenshots of pages and video frames for reviews.
- **Claude Code:** builds the lead agent loop (code, repo), scrapes and analyzes the Series B CSV, audits the web pages (HTML fetch, Lighthouse, copy extraction), builds the growth-idea mockup if you want one, and assembles the final deliverable doc.
- **Poolday:** all videos (LinkedIn, 2 prospect videos, UGC). Use the attached skill and reference videos.
- **Instagram/TikTok:** UGC distribution.

---

## 1. Timeline (48h)

```
H0–H2   Setup: sign up (invite link), read agent guide, time 1 test render,
        pick 2 companies, create IG account (start warming it NOW)
H2–H10  PARALLEL:
          Poolday tabs 1–2 → prospect video A (2 variants)
          Poolday tabs 3–4 → prospect video B (2 variants)
          Poolday tab 5    → LinkedIn video (use-case)
          Poolday tab 6    → UGC: generate ~30 actor photos, pick favorites
          You + Claude Code → agent loop build (while renders run)
H10–H14 Review renders, follow-up prompts, consolidate best versions
        Post UGC #1 (IG limits new accounts to ~1–2 posts/day)
H14–H24 Page reviews + video review (Claude + screenshots)
        Growth idea write-up. Agent loop: end-to-end run on 3 real leads
H24–H36 Final versions of all videos. LinkedIn post copy. UGC #2–#3
H36–H46 Assemble deliverable doc, record 2-min loop demo, collect IG stats
H46–H48 Buffer. Final UGC post and stats screenshot
```

---

## 2. Deliverables: how to do each one

### D1. LinkedIn post + video (use case)
**Goal:** qualified leads (B2B marketers and founders), not just likes.
1. Claude: brainstorm 10 use cases, pick the one with the strongest "wait, it did that?" moment. Strong candidates:
   - "I gave Poolday a URL, it made our launch video"
   - "Personalized prospect videos at scale" (ties into D3, so you can show the loop)
   - "Recreated a viral motion-design video with one prompt" (ties into the growth idea)
2. Poolday: 2–3 parallel conversations, each with a different reference video. Keep it under 45s, put the hook in the first 2s, include captions, make it square or 4:5 for LinkedIn feed.
3. Claude: write the post. Hook line, 3 short lines, soft CTA ("comment VIDEO and I'll make one for your company" is a lead-capture mechanic), link in the first comment.
4. **Success criteria:** hook understood with sound off, a clear CTA, and a lead-capture mechanic.

### D2. Two prospect videos (Series B list, not Higgsfield)
1. Claude Code: load the CSV and rank companies by **recency of round** (fresh money means budget and a launch or hiring push coming), a visual product (good video material), and B2B with a marketing team.
2. Pick 2. **In the deliverable, explain why:** e.g. "raised Series B X weeks ago → upcoming launch/hiring announcements → immediate need for video."
3. Gather each company's site, product screenshots, brand colors, recent announcement, and a reference video you like.
4. Poolday: drop the skill in the chat plus the reference video. Also try the prompt from the brief: *"build a video for [X] in threejs, make the most impressive video possible. Rich visual detail, seamless continuity from start to finish."* Run 2 variants per company in parallel and keep the best.
5. These two runs are also your manual prototype for the D3 loop. Note which prompt structure worked best.

### D3. Agent loop (leads → qualify → video → human check → email draft)
Build with Claude Code in this repo. Suggested architecture:
```
[Lead sources] → [Enrich] → [Qualify (Claude API, scored rubric)] → [Brief + Poolday prompt]
   → [Poolday: API if the agent guide documents one, else prompt shown to human to paste]
   → [HUMAN GATE: review video (approve / reject / regenerate with note)]
   → [Claude drafts personalized email] → [Gmail draft / CSV] → you send
```
- **Sources:** the Series B CSV, funding-news RSS or X searches ("raised Series B"), Crunchbase/Harmonic/Apollo if you have access.
- **Qualify:** Claude scores 0–100 on ICP fit (B2B SaaS, 50–500 employees, recent round, active on LinkedIn, launches often), with a written justification. Keep leads scoring 70 or more.
- **Human gate:** a small web dashboard or a Slack message with approve/reject buttons. This matters most for the reviewer, so make it visible in the demo.
- **Email:** short, personalized, video thumbnail plus link, one question as the CTA.
- **Deliverable:** repo, architecture diagram, 2-min screen recording of one lead going end to end, and the next steps to make it fully automated.

### D4. AI UGC (3 < n < 20)
You already have a method (Pletor), so just run it. Things to note for the doc:
- **Create the IG account on day 1** and post lightly to warm it.
- **New accounts can realistically post only ~1–2 times per day**, so in 48h expect about 4–5 posts. Say this explicitly in the deliverable, along with the plan to post the remaining videos over the next days.
- Report views per video, the best hook, and what you'd iterate on.

### D5. Growth idea: "Enter your URL, watch your launch video"
Full write-up is in section 3.

### D6. Video review (PostHog or Upflow)
Watch it 3 times. Screenshot frames at key moments and give them to Claude with this frame: *hook (0–3s), clarity of value prop, pacing, text legibility on mobile, sound-off viewing, CTA, length versus platform.* Write it as **timestamped notes + top 3 changes + one "I'd remake the first 5s like this" proposal** (optionally make that alternative intro in Poolday; it's strong evidence).

### D7. Page reviews (home + b2b-startups) → more demos booked
1. Claude Code: fetch both pages, extract the copy, count CTAs, run Lighthouse (speed and mobile), and list the friction points.
2. Claude: review the above-the-fold section (can you tell in 5s what Poolday is, who it's for, and what to do next?), social proof placement, the demo CTA (calendar embed versus form), and whether there is an "instant value" hook, which connects to the growth idea.
3. Output: a prioritized list (impact × effort). Mock up the top 1–2 changes as annotated screenshots.

---

## 3. Growth idea (detailed draft)

**"Paste your URL → get your launch video."** A single-purpose lead-magnet site. No long page, no long copy.

**User flow (under 60s of effort):**
1. Paste your website URL, or describe your idea.
2. Pick a style template: *Apple motion design*, *Linear-style dark UI*, *Kinetic typography*, *3D product (three.js)*, and similar styles trending on X.
3. Poolday generates the video. The user watches a preview (watermarked or low-res). To download HD or edit, they create an account, which leads to a demo booking.

**Why it works:** the same mechanic as Submagic ("upload, pick the Hormozi template, magic"). There's zero creative effort, the result is instantly shareable, and a watermark on shared videos makes it spread.

**Distribution engine: "actually do it" replies on X:**
- Motion designers and AI accounts regularly post engagement bait like *"Claude/GPT just made this video with one prompt"* (often faked).
- The Poolday team takes the video, has Poolday actually rebuild it (reference video plus a strong model and prompt), screen-records it running in Poolday, and replies: *"Poolday can actually do it: [recording]. Try yours: [link]"*.
- This borrows the reach of viral threads and shows real capability against fake claims.
- Precedent: Mosaic/Motion answered large X threads with "tag @motion.so to get a video explaining this thread."
- Also a "tag @poolday for a video of this thread" bot.

**Budget (up to ~$15k, gated by traction):**
| Item | Est. |
|---|---|
| Site + templates build (1–2 weeks) | $2–4k |
| Generation credits (free videos), capped per day | $5–8k |
| Reply-guy operator / motion editor for X remakes | $2–3k |
| Small paid boost on the best remakes | $1–2k |

Start with about $3k. Unlock the rest when metrics pass the thresholds.

**Metrics:** URL submissions per day → % who sign up → % who book a demo. Also reply-thread impressions and cost per demo booked. **Kill/scale rule:** scale spend if cost per booked demo is below target (for example, under $150) after 2 weeks.

**Risks and mitigation:** generation cost abuse (email gate before HD, rate limits), quality variance (only offer templates that work reliably), and remake replies coming across as spammy (reply only to big and relevant threads, and only when the remake is genuinely good).

---

## 4. Final deliverable doc: outline

1. **TL;DR:** what I shipped, links, key numbers (views, credits spent, time)
2. **How I worked (methods):** parallel Poolday tabs, Claude vs. Claude Code vs. Poolday roles, the LOG, the consolidation process, the timeline actually followed
3. D1 LinkedIn post + video
4. D2 Prospect videos, **plus why these 2 companies (fresh round)**
5. D3 Agent loop: diagram, repo, demo recording
6. D4 UGC: account, videos, views, **note on the IG new-account limit of 1–2 posts/day within 48h**
7. D5 Growth idea
8. D6 Video review
9. D7 Page reviews
10. What I'd do with more time
11. **Appendix: screenshot of the UGC farm made for Pletor** (to show prior experience) ← don't forget

---

## 5. Checklist
- [ ] Read agent guide; sign up via invite link
- [ ] Time one render; log it
- [ ] Create IG account (day 1)
- [ ] Pick 2 companies from CSV + write rationale
- [ ] Launch parallel Poolday tabs (D1, D2×2, UGC actors)
- [ ] Build agent loop in Claude Code
- [ ] Post UGC (1–2/day)
- [ ] Video review, page reviews, growth idea
- [ ] LinkedIn post copy
- [ ] Assemble deliverable doc + Pletor screenshot
