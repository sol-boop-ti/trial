# Poolday Growth Assignment: Deliverables

**[PLACEHOLDER: name]** · 48-hour assignment · **[PLACEHOLDER: submission date]**

---

## TL;DR

| # | Deliverable | Link | Key number |
|---|---|---|---|
| D1 | LinkedIn post + video | [PLACEHOLDER: post draft / video link] | [PLACEHOLDER: length, ratio] |
| D2 | Prospect video: Flam | [PLACEHOLDER: video link] | [PLACEHOLDER: prompts, render time] |
| D2 | Prospect video: Wispr Flow | [PLACEHOLDER: video link] | [PLACEHOLDER: prompts, render time] |
| D3 | Agent loop (leads → qualify → video → human gate → email draft) | [PLACEHOLDER: repo link] · [PLACEHOLDER: demo recording] | [PLACEHOLDER: leads processed, emails drafted] |
| D4 | AI UGC on Instagram | [PLACEHOLDER: @handle] | [PLACEHOLDER: n posts, total views] |
| D5 | Growth idea: "Paste your URL, get your launch video" | [D5-growth-idea.md](D5-growth-idea.md) · [PLACEHOLDER: shareable link] | $3k pilot → up to $15k; target ≤$150 per booked demo at scale |
| D6 | Video review ([PLACEHOLDER: PostHog / Upflow]) | [PLACEHOLDER: link] | Top 3 changes + first-5s rewrite |
| D7 | Page reviews (home + b2b-startups) | [PLACEHOLDER: link] | [PLACEHOLDER: n prioritized changes] |

**Key numbers**
- Total UGC views: [PLACEHOLDER] across [PLACEHOLDER] posts (best post: [PLACEHOLDER] views)
- Credits spent: [PLACEHOLDER] of $2,000 (by deliverable: see [Credits](#credits-by-deliverable))
- Prompts per video: [PLACEHOLDER: e.g. 7 → 4 → 2] (first → second → third video)
- Render time per run: [PLACEHOLDER: median / range]
- Parallel Poolday conversations at peak: [PLACEHOLDER]

---

## How I worked

**1. Planned before building, from the tool's own docs.** I read the Poolday agent guide first and let it change the plan. Runs take about an hour, a first video takes about 7 prompts, variants belong in one conversation, and saved skills/commands cut later videos to 1–2 prompts. That moved brand kits and prospect videos to hour 0, and made the saved command the backbone of the agent loop.

**2. Two lanes, zero idle time.** Poolday renders in one lane. I and Claude Code work in the other (briefs, critiques, the agent loop, reviews). Long jobs started first, and every render window was used for other work.

**3. Parallel Poolday conversations.** [PLACEHOLDER: n] conversations at once, one per video (prospect A, prospect B, an A/B test, UGC, LinkedIn), all in Align mode, each on the right tier (Light for quick option rounds, Max for showcase videos). I parallelized across different videos, never across variants of one video: the guide says variants clone faster inside a single conversation.

**4. Brand kits first.** Each prospect video started with a brand kit built from the company's website, the biggest quality lever when you don't have a company's assets. [PLACEHOLDER: what the brand kit got right/wrong]

**5. Options before committing.** Every brief included a validation step: 5 concept directions for LinkedIn, [PLACEHOLDER: n] actor photos → pick → voices → pick for UGC, and the skill's single approval gate (script, look, routing) for prospect videos. Choosing before rendering is cheaper than fixing after. [PLACEHOLDER: screenshot of an option-selection step]

**6. The reference video is the biggest creative lever.** The reference-teaser skill copies the reference's cuts, rhythm and look, so I picked references myself and wrote down what I liked about each as mechanisms ("hard cuts on the kick", "oversized type wiping across the UI"). [PLACEHOLDER: references used]

**7. Mechanism critiques, not adjectives.** Feedback was timestamped and mechanical ("hard cut at 0:04, hold the logo 2 frames longer, music peak on the tagline"), never "make it punchier". [PLACEHOLDER: one real feedback round, before/after]

**8. A/B test on the brief.** Skill-based prompt vs. the brief's one-liner ("build it in threejs, most impressive video possible") in separate conversations. Winner: [PLACEHOLDER: which and why].

**9. Skill/command reuse and the learning curve.** After the first prospect video was final, I saved the flow as a skill and a `/prospect-video` command. Measured prompts per video: **[PLACEHOLDER: 7] → [PLACEHOLDER: 4] → [PLACEHOLDER: 2]**. The agent loop now only has to generate a 2-line call.

**10. Clear roles per tool.**

| Tool | Role |
|---|---|
| **Claude (chat)** | Brief structure and intent, hooks and scripts, LinkedIn and email copy, critiques from frames, page and video reviews (it can browse) |
| **Claude Code** | Ranked the CSV, built the agent loop, kept the plan, runbook and methods log, assembled this doc |
| **Poolday** | Brand kits and every video, plus saved skills and commands. It decides the execution. I didn't paste editing instructions from Claude into it |

**11. Documented as I went.** Every step was logged the same day (what, tools, inputs, process, decision and why, output, time/credits, lessons). That log is the source for this section. [PLACEHOLDER: link to METHODS.md]

---

## D1. LinkedIn post + video

- **Use case shown:** [PLACEHOLDER: chosen concept; recommended: "One URL in, brand kit + launch video out", see [D1-linkedin.md](D1-linkedin.md)]
- **Why this angle:** [PLACEHOLDER: why it produces *qualified* leads]
- **Video:** [PLACEHOLDER: link] · 4:5 · [PLACEHOLDER: length] · hook understood with the sound off
- **Process:** 5 concept directions from Poolday → picked [PLACEHOLDER] → full brief → [PLACEHOLDER: n] prompts, [PLACEHOLDER: credits]
- **Post copy:**
  > [PLACEHOLDER: final post text]
- **Lead-capture CTA:** [PLACEHOLDER: e.g. "Comment VIDEO + your URL and I'll make yours"]. It qualifies leads, because people have to give their company URL. Link in the first comment.

---

## D2. Two prospect videos

### Why these companies: fresh rounds with a named buyer
> I picked companies that raised in the last ~5 weeks and where the list names a marketing or creative decision-maker: fresh money plus an upcoming launch means they need video *now*, and there's someone to send it to.

Scoring on the Series B list (38 companies, Higgsfield excluded): (1) freshness of round, (2) a named marketing/creative buyer, (3) a visual product, (4) fit with video as a need. A filter on rounds in the last 90 days gave 9 companies. I removed those with no contact (Arcee AI, Standard Metrics) or a weaker segment/unverified HQ (Delightree, Flex).

| | Flam | Wispr Flow |
|---|---|---|
| Round | $40M Series B, 10 days before the analysis | $280M Series B, 38 days before |
| Buyer | CMO / Head of Product + Creative Director | VP Product Marketing + Head of Design, Marketing |
| Why | Freshest round with contacts. They sell interactive content to enterprise marketers, so they judge visual quality professionally | Largest fresh round on the list. Design-led brand, and the move into meetings means a launch is coming |
| Angle | "Your Series B announcement film" | "What your meetings launch could look like" |
| Video | [PLACEHOLDER: link] | [PLACEHOLDER: link] |
| Prompts / render time / credits | [PLACEHOLDER] | [PLACEHOLDER] |

Backup: **Convex** ($57M, open source, so the skill can use its real UI components). [PLACEHOLDER: used as the 3rd video to test `/prospect-video`? result]

### How they were made
- Brand kit from the website → reference-teaser skill + a reference video I chose, with what I liked about it written as mechanisms → the skill's approval gate (script, look, routing) → iteration with timestamped mechanism feedback.
- A/B test: skill-based vs. the "threejs, most impressive video possible" prompt. [PLACEHOLDER: result]
- [PLACEHOLDER: screenshot of the approval gate]
- **Outreach drafts:** [PLACEHOLDER: email to each buyer, from the D3 loop]

---

## D3. Agent loop

**Leads → qualify → Poolday video → human validation → email draft**

[PLACEHOLDER: diagram]

```
[Sources: CSV + funding news] → [Enrich: site, round date, product]
 → [Qualify: score 0–100 on an ICP rubric, with justification]
 → [Generate Poolday prompt: "/prospect-video <url> <reference>"]
 → [Human pastes into Poolday → pastes video link back]   (no public API yet)
 → [HUMAN GATE: approve / reject / regenerate with a note]
 → [Draft personalized email] → [draft for the hiring manager to send]
```

- **Repo:** [PLACEHOLDER: repo link]
- **Demo recording (one lead end to end):** [PLACEHOLDER: link]
- **Qualification rubric:** [PLACEHOLDER: criteria and weights]
- **Poolday step:** Poolday has no documented public API, so the loop generates the 2-line `/prospect-video` call and a human pastes it in. The saved command is what makes this step short.
- **Results:** [PLACEHOLDER: n leads in → n qualified → n videos → n approved → n emails drafted]
- **Next step:** automate the Poolday step through an API or a browser agent once one is available, and send the drafts to the hiring manager's inbox.

---

## D4. AI UGC on Instagram

- **Account:** [PLACEHOLDER: @handle] (new account, Creator mode for view stats)
- **Posting limit:** a new IG account can only post about **1–2 times per day** before reach drops or the account gets flagged, so **about 4–5 posts fit in 48 hours**. I warmed the account up with normal activity (follows, likes, comments) and no posts, starting before any video production.
- **Method:** reused my AI UGC method from Pletor (see appendix), inside Poolday: actor photos → pick → voices → pick → scripts → batch as variants in one conversation.

| # | Hook (first 2s) | Posted | Views at +24h | Views at submission |
|---|---|---|---|---|
| 1 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 2 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 4 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| 5 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

- **Total views:** [PLACEHOLDER] · **Best hook:** [PLACEHOLDER] · **Leads/profile clicks:** [PLACEHOLDER]
- [PLACEHOLDER: IG insights screenshot]

---

## D5. Growth idea: "Paste your URL, get your launch video"

**Summary.** A very simple site: paste your website URL, pick a style (Apple-style motion design, Linear-style dark UI, kinetic type, 3D, trending social motion styles), get your launch video. It's the Submagic mechanic (upload → pick a template → done) applied to launch videos. Poolday builds the brand kit from the URL and renders it with a saved template per style. Runs take about an hour, so the video is **emailed**, which captures the lead before the value arrives. Watermarked preview → HD download or edit = sign up → book a demo.

**Distribution: "Poolday can actually do it."** On X, engagement-bait posts claim "an AI model just made this video with one prompt" (often faked). We actually remake the video in Poolday (it pulls the video from the link), screen-record it running, and reply "Poolday can actually do it" + the link. Precedent: Motion/Mosaic replied to big threads with "tag us to get a video explaining this thread".

**Quick win: ride the "AI motion designer" trend.** It's the format of the week on X: "I paid $1,000 for a video like this a year ago. Now I made it with Opus 5.5 in 30 minutes" (e.g. @tdinh_me, 4k views in 4h; replies share the prompt: *"Make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are… visit the pages first to learn about the product, then write the video yourself"*). Screenshot: `assets/trend-opus-motion-design-tweet.png`.
- **The play:** post incredible motion-design videos made with Poolday for well-known brands, 2–3 a week, with the before/after and the prompt, e.g. "We gave Poolday one prompt: make [brand]'s launch video better." Each post shows people how good AI motion design has become, and that Poolday does it without code.
- **Proof it works:** my D6 remakes (PostHog and Upflow, rebuilt 100% on brand, with 3D cameras, brand match cuts and a synced soundtrack) are exactly this format.
- **Honesty rule:** name the model ("Opus 5.5") only if Poolday confirms it runs on it for that video; otherwise "made with Poolday". Only publish another brand's remake with their OK (PostHog's hedgehogs are licensed art), or use our own brand or consenting customers.

**Budget:** a $3k pilot, then up to $12k more unlocked in stages when targets are hit (cost per booked demo ≤$300 in the pilot, ≤$150 at scale).

**Full write-up** (product flow, how it runs on Poolday, distribution, lead routing, budget, metrics, risks): [D5-growth-idea.md](D5-growth-idea.md) · [PLACEHOLDER: shareable link]

---

## D6. Video review: [PLACEHOLDER: PostHog GenAI launch / Upflow faster payments]

- **Method:** framework-based review (hook 0–3s, the question the opening sets up, value prop, story arc, pacing, mobile legibility, sound-off viewing, music/SFX sync, product proof, CTA, length vs platform) from frames with timestamps and a screen recording. Notes are written as mechanisms (cuts, holds, easing, sync points).
- **Timestamped notes:** [PLACEHOLDER: table]
- **Top 3 changes:**
  1. [PLACEHOLDER]
  2. [PLACEHOLDER]
  3. [PLACEHOLDER]
- **First 5 seconds, rewritten:** [PLACEHOLDER: shot list]
- **Proof:** [PLACEHOLDER: improved intro remade in Poolday, before/after, or "not run"]

---

## D7. Page reviews: poolday.ai and /solutions/b2b-startups

- **Goal:** more demos booked.
- **Method:** fixed framework (5-second test, value prop, segment fit, social proof, demo CTA friction, objection handling, "instant value" entry points, on-page video, speed/mobile, analytics) applied to the live pages plus my own desktop and mobile screenshots. Every finding points to a specific element.
- **Biggest reason each page loses demos:** home [PLACEHOLDER] · b2b-startups [PLACEHOLDER]
- **Prioritized changes (ICE):** [PLACEHOLDER: table: problem → change → why it increases demo bookings → A/B test]
- **Top 3 changes, annotated mockups (before/after):** [PLACEHOLDER]
- **Hero rewrites (2 variants per page):** [PLACEHOLDER]
- **Link to D5:** [PLACEHOLDER: where a "paste your URL" entry point would sit on the page and how it hands off to the demo CTA]

---

## My commitment: post about Poolday every day
I'd post every day on X and LinkedIn about Poolday. It genuinely excites me. The content engine is ready:
- **Formats that rotate:**
  - use-case listicles ("Top 5 Poolday use cases");
  - before/after remakes of well-known videos (the "AI motion designer" trend);
  - "Same prompt, 4 apps" comparisons;
  - "Claude Opus 5.5 + Poolday = Infinite UGC farm" style equations;
  - replies with proof under "AI can't do this" threads;
  - build-in-public updates from the prospect loop and the UGC account.
- **Cadence:**
  - X: 1 post and 3–5 proof replies a day.
  - LinkedIn: 1 post a day, founder voice, the best performer from X re-cut.
- **Every post ends in a measurable action** (comment a URL or a number), which feeds the lead loop (D3).
- **Tracked weekly:** posts, views, URL comments, demos booked.

## What I'd do with more time

- [PLACEHOLDER: refine after the 48h]
- Automate the Poolday step of the agent loop (API or browser agent) and run it on a weekly feed of fresh rounds.
- Run the D7 changes as real A/B tests with the demo funnel instrumented end to end (CTA view → click → booking → show-up).
- Pilot the D5 URL-to-video site with 2–3 style templates and a hard daily credit cap.
- Scale UGC past the new-account limit: more warmed accounts and more platforms (TikTok, YouTube Shorts), iterating on the best hook.
- Build a library of saved Poolday commands per use case (launch, funding announcement, feature drop) so each new video takes 1–2 prompts.

---

### Credits by deliverable

| Deliverable | Credits | Prompts | Notes |
|---|---|---|---|
| D1 LinkedIn | [PLACEHOLDER] | [PLACEHOLDER] | |
| D2 Flam | [PLACEHOLDER] | [PLACEHOLDER] | |
| D2 Wispr Flow | [PLACEHOLDER] | [PLACEHOLDER] | |
| D2 A/B test (threejs) | [PLACEHOLDER] | [PLACEHOLDER] | |
| D3 loop test videos | [PLACEHOLDER] | [PLACEHOLDER] | |
| D4 UGC | [PLACEHOLDER] | [PLACEHOLDER] | |
| D6 intro remake | [PLACEHOLDER] | [PLACEHOLDER] | optional |
| **Total** | **[PLACEHOLDER] / $2,000** | | |

---

## Appendix

**Prior experience: the AI UGC farm I built for Pletor**

[PLACEHOLDER: screenshot of the UGC farm built for Pletor]

[PLACEHOLDER: one line of context: what it produced, volume, results]
