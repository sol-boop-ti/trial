# Poolday Assignment: Execution Plan (v2, updated with the agent guide)

48-hour assignment with 7 deliverables. You win on **parallelization** (never sit idle while Poolday runs), on **directing with mechanisms, not adjectives**, and on **documenting your method** as you go.

---

## 0. What the agent guide changes (key facts)

| Fact from the guide | What it means for us |
|---|---|
| **A run can take an hour or more** (quality over speed). **Light** tier for fast small tasks | This is where "1 hour per run" came from. Keep 5+ conversations going at once and do creative or coding work during runs. Use **Light** for quick iterations and **Max/Ultra** for the showcase videos (LinkedIn, prospects) |
| **First video ≈ 7 prompts, second ≈ 4, third ≈ 1–2** | Budget about 7 prompts × 1h for the first video, so start the hardest videos in the first hours |
| **Brand kit first** (`brand:name`): website import, logos, fonts, screenshots rebuilt into animatable pieces | For each prospect: "Create a brand kit for [company] from [url]" plus product screenshots. This is the biggest quality lever when you don't have their assets |
| **Perfect-prompt structure**: Context/Inputs · Objective · Desired output · Audience · Creative direction · Hard constraints · Validation & choice steps · where it has creative freedom | Use Claude to fill this structure. Poolday decides the editing |
| **Align mode**: one question at a time until "start building" | Always Align (tip from the brief) |
| **Variants: stay in ONE conversation** ("give me 3 variants", base built once, then cloned) | Parallelize across **different videos**, not across variants of the same video |
| **Ask it to parallelize** a video with sections, and it opens the conversations itself | Useful for the 3D prospect videos (cold open / demo / CTA) |
| **Save a flow as a skill or `/command`** → the next video takes 2 prompts | **Key for D3**: after prospect video #1, save a `/prospect-video` command. The agent loop then only needs to generate a 2-line prompt |
| **Pulls YouTube/TikTok/IG links** (≤20 min / 100 MB), but not Drive or Dropbox | References and "remake this viral video" (growth idea) can be passed as links |
| **Point & select + live editor** (sliders, text fields, no re-render) | Polish rounds are fast. Ask for controls ("controls for headline text & music volume") |
| **No public API mentioned; it doesn't post to social** | D3 loop: the "Poolday step" = the agent generates the prompt, a human pastes it into Poolday and pastes the result link back. Say so explicitly; the API is the next step |
| **Options before committing** ("10 actor photos, let me choose… 5 voices…") | Put this in every brief's validation step |

---

## 1. Ground rules

- **Align mode**, correct tier per job, 5+ conversations open at once, notifications ON.
- **Critique with mechanisms**: "hard cut at 0:04, hold logo 2 frames longer, music peak on the tagline", never "make it punchier".
- Claude writes the **brief structure and intent**. Poolday decides the **execution** (don't paste video-editing instructions from Claude blindly).
- **`LOG.md`**: time, conversation, tier, prompt, result, credits, lesson. This becomes your "methods" section.
- Screenshot or record: briefs, option-selection steps, point-and-select edits, final renders, loop dashboard, IG stats.
- Track the credits ($2,000 total). Report spend per deliverable.

### Tool roles
- **Claude (chat):** fills the perfect-prompt template, writes beat sheets and hooks, LinkedIn copy, emails, critiques (paste frames and screenshots), growth-idea write-up.
- **Claude Code:** ranks the CSV, builds the agent loop (this repo), audits the pages (copy extraction, CTA count, Lighthouse), assembles the deliverable doc.
- **Poolday:** brand kits, all videos, skills and commands.

---

## 2. Timeline (48h): two lanes, zero idle time

```
H0–H1   Sign up (invite link). Create IG account. Enable notifications.
        Claude Code: rank CSV → pick 2 companies.
        LAUNCH (parallel, Align mode):
          conv 1: brand kit Company A (url + screenshots)
          conv 2: brand kit Company B
          conv 3: UGC — "generate 30 actor photos, let me choose" (Light)
          conv 4: LinkedIn video — ask for 5 concept directions first
H1–H3   While kits build: write the beat sheets/briefs for A and B with Claude
        (first 2 seconds on their own line). Collect reference videos.
H3–H4   conv 1/2: send the prospect briefs (Max tier, brand:A / brand:B,
        "give me 3 style directions before building")
        conv 3: pick actors → voices → scripts for UGC
H4–H16  Iteration rounds (~7 prompts per first video) on all convs.
        Between runs: build the agent loop with Claude Code.
        Post UGC #1 as soon as one is ready.
H16–H24 After prospect video A is final: "save this flow as a skill +
        /prospect-video command". Test it on video B / a 3rd company (≈2 prompts).
        Page reviews + video review. Growth idea write-up.
H24–H36 Final polish (live editor, point & select). LinkedIn copy.
        Agent loop: end-to-end run on 3 real leads using /prospect-video.
        UGC #2–#3 (1–2 posts/day on a new account).
H36–H46 Assemble deliverable doc. Record 2-min loop demo. IG stats.
H46–H48 Buffer, last UGC post, final stats screenshot.
```

---

## 3. Deliverables: how to do each one

### D1. LinkedIn post + video (use case)
1. Pick a use case. The strongest option, since it ties to D3 and the growth idea: **"I gave Poolday a company URL, it built their brand kit and a launch video"**, or **"personalized prospect videos at scale"**.
2. Poolday conv: ask for **5 concept directions**, pick one, then use the full perfect-prompt brief. 1:1 or 4:5, ≤45s, hook in the first 2s, readable with the sound off. Tier: Max.
3. Claude: write the post. Hook, 3 short lines, lead-capture CTA ("comment VIDEO + your URL and I'll make yours"), link in the first comment.
4. Success criteria: the hook is understood with the sound off, and the CTA qualifies leads (people have to give their URL).

### D2. Two prospect videos
1. Claude Code ranks the CSV: **fresh round** (most recent Series B), visual product, B2B with a marketing team. **Write down why** each company was picked ("raised X weeks ago → launch/hiring push → needs video now").
2. **Brand kit per company** (site URL + product screenshots, which get rebuilt into animatable pieces).
3. Brief using the perfect-prompt template. Attach the skill from the brief and a reference video, and **say what you like about the reference** (pacing, 3D camera moves, type treatment). Add the brief's line: *"build a video for [X] in threejs, make the most impressive video possible. Rich visual detail, seamless continuity from start to finish."*
4. Validation: "3 style directions → I pick → build". Iterate with mechanism-level feedback.
5. **Save as skill + `/prospect-video` command** → prove that video B takes about 2 prompts. This is also a strong story for the deliverable.

### D3. Agent loop (leads → qualify → video → human check → email draft)
Built with Claude Code in this repo:
```
[Sources: CSV + funding news] → [Enrich (site, round date, product)]
 → [Qualify: Claude scores 0–100 on ICP rubric + justification]
 → [Generate Poolday prompt: "/prospect-video brand kit from <url>, company <X>, angle <Y>"]
 → [Human pastes into Poolday → pastes video link back]   (no public API yet)
 → [HUMAN GATE: approve / reject / regenerate-with-note]
 → [Claude drafts personalized email] → [Gmail draft or CSV] → you send
```
- The human gate and the "paste prompt" step can live in a small web dashboard. The demo recording shows one lead going end to end.
- Next step to say in the doc: automate the Poolday step through the API or a browser agent once one is available.

### D4. AI UGC (3 < n < 20)
Your Pletor method applies. Use the guide's validation flow (30 actors → pick → 5 voices → pick → scripts → batch as variants in one conversation). Notes for the doc: **a new IG account can realistically post ~1–2 per day → about 4–5 posts in 48h**. Report views per video and the best hook.

### D5. Growth idea: see section 4.

### D6. Video review (PostHog or Upflow)
Timestamped notes covering the hook (0–3s), clarity of the value prop, pacing, mobile legibility, sound-off viewing, CTA and length. Write it **in the guide's language of mechanisms** (cuts, holds, easing, sync points). Top 3 changes. Bonus: have Poolday remake the first 5s (it can pull the video from the link) as proof.

### D7. Page reviews (home + b2b-startups)
Claude Code extracts the copy, CTAs and Lighthouse scores. Claude reviews: 5-second test above the fold, social proof, demo CTA friction (calendar embed vs. form), and an "instant value" entry point (ties to the growth idea). Output a list prioritized by impact × effort, plus annotated mockups of the top 1–2 changes.

---

## 4. Growth idea: "Paste your URL → watch your launch video"

**Flow (<60s of effort):** paste a URL or describe an idea → pick a style template (*Apple motion design*, *Linear dark UI*, *kinetic type*, *3D three.js*, the styles trending on X) → Poolday builds a brand kit from the URL and renders it using a saved **template/command per style** → preview (watermarked) → HD download or edit = sign up → book a demo.

**Why it's feasible with Poolday today:** the guide confirms brand-kit import from a website, templates and variants cloned from a base, saved commands, and the Light tier for cheaper runs. Each style template = one saved Poolday template, cloned per URL.

**Why it works:** it's the Submagic mechanic (upload → pick "Hormozi" → magic): zero creative effort, instantly shareable, and the watermark spreads it.

**Distribution: "Poolday can actually do it" replies on X.** Motion designers and AI accounts post engagement bait ("Claude / GPT just made this with one prompt", often faked). Poolday **pulls the video from the link** (a supported feature), remakes it with a strong brief on the Max/Ultra tier, and we screen-record it running in Poolday and reply: *"Poolday can actually do it → [recording]. Make yours: [link]"*. Precedent: Motion/Mosaic answered big threads with "tag @motion.so to get a video explaining this thread".

**Constraint to design around:** runs can take about an hour. So the site uses **email delivery** ("we'll send your video when it's ready"), which captures the lead before the value arrives. Pre-built templates on the Light tier keep the time and cost down.

**Budget (up to ~$15k, unlocked in stages):**
| Item | Est. |
|---|---|
| Landing + queue + 4–6 style templates | $2–4k |
| Generation credits (daily cap, email-gated) | $5–8k |
| Operator for X remakes (reply-guy + motion QA) | $2–3k |
| Paid boost on the best remakes | $1–2k |

Start with about $3k. Unlock the rest when cost per booked demo is below target (for example, under $150) after 2 weeks.

**Metrics:** URLs submitted → emails captured → videos watched → signups → demos booked. Also reply impressions on X.
**Risks:** credit abuse (email gate, rate limit, one video per domain), quality variance (ship only templates that work reliably), coming across as spammy (reply only to big, relevant threads, and only with genuinely good remakes).

---

## 5. Deliverable doc: outline
1. **TL;DR**: links, key numbers (views, credits, prompts per video)
2. **Methods**: two lanes/zero idle time, parallel conversations, brand kits, options-before-commit, mechanism critiques, skill/command reuse (prompts per video dropping from 7 to 2, measured), Claude vs. Claude Code vs. Poolday roles
3. D1 LinkedIn · 4. D2 prospects **+ why these companies (fresh round)** · 5. D3 loop (diagram, repo, demo) · 6. D4 UGC **+ IG 1–2 posts/day limit on new accounts** · 7. D5 growth idea · 8. D6 video review · 9. D7 page reviews
10. With more time
11. **Appendix: screenshot of the Pletor UGC farm** ← don't forget

## 6. Checklist
- [ ] Sign up, notifications on, IG account created
- [ ] Rank CSV → 2 companies + rationale
- [ ] Brand kits A & B launched (H0)
- [ ] UGC actors + LinkedIn concepts launched (H0)
- [ ] Prospect briefs sent (H3)
- [ ] `/prospect-video` skill/command saved and tested
- [ ] Agent loop built + demo recorded
- [ ] UGC posted 1–2/day
- [ ] Video review, page reviews, growth idea
- [ ] LinkedIn post copy
- [ ] Deliverable doc + Pletor screenshot
