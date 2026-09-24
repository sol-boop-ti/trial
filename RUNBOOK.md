# RUNBOOK: exactly what to do, step by step

Each step says **WHO** does it, **WHERE**, **DO** (the exact action), **EXPECT** (what should happen), and **REPORT** (the one line to send Claude Code, which logs it in `METHODS.md`).
Legend: 🧑 you · 🎬 Poolday · 🤖 Claude Code (this session) · 💬 Claude chat

> **Reporting habit:** after each step, send me one line, e.g. `done B1 — 12 min, Align asked 4 questions, picked direction 2`. I write it into METHODS.md so you never have to document it yourself.

---

## PHASE 0: Everything done BEFORE opening Poolday (status board)

| # | Who | Task | Needs Poolday? | Status |
|---|---|---|---|---|
| 0.1 | 🧑 | Warm up IG account (A2): 10–15 min/day, no posts yet | no | 🟡 in progress |
| 0.2 | 🧑 | Pick 2 reference videos (any SaaS/motion-design video you love that fits the brand) + 2–3 "what I love" lines each (A3) | no | ⬜ |
| 0.3 | 🧑 | Page reviews: paste `deliverables/PROMPT-A-page-review.md` into Claude chat (it can browse poolday.ai; this session can't), bring the output back here | no | ⬜ |
| 0.4 | 🧑 | Video review: pick PostHog or Upflow, screenshot frames with timestamps (or a screen recording), run `deliverables/PROMPT-B-video-review.md` in Claude chat | no | ⬜ |
| 0.5 | 🧑 | (optional) Anthropic API key: only needed for the loop to run on its own; without it, it runs in mock mode or via a Claude Code command | no | ⬜ |
| 0.6 | 🧑 | Find the Pletor UGC farm screenshot, keep it for the appendix | no | ⬜ |
| 0.7 | 🧑 | UGC: your own Pletor/Casey AI format (shock face + iPhone product demo), made in Poolday the intended way. Send me the Pletor image/video prompts + models so we adapt them to Poolday | no | ⬜ |
| 0.8 | 🤖 | Build the agent loop (D3), runs on the CSV first → `loop/` | no | ✅ done, tests pass (mock mode) |
| 0.9 | 🤖 | Write the growth idea in full (D5) → `deliverables/D5-growth-idea.md` | no | ✅ done (review it) |
| 0.10 | 🤖 | Draft 3 LinkedIn use-case angles + post copy (D1) → `deliverables/D1-linkedin.md` | no | ✅ done (pick an angle) |
| 0.11 | 🤖 | Review kit for Claude chat (D6/D7) → `deliverables/D6-D7-review-kit.md`; polish the final reviews once 0.3/0.4 come back | no | ✅ kit ready, waiting on your chat outputs |
| 0.12 | 🤖 | Final Poolday prompts with your reference links, once 0.2 arrives | no | ⬜ |
| 0.14 | 🧑 | Get the Poolday API docs (dashboard/settings, or ask the Poolday team on Slack) and paste them here | no | ⬜ |
| 0.15 | 🧑 | **(now important)** Allow `poolday.ai` in this cloud environment's network settings so I can read the docs and screenshot the pages to rebuild them (home, b2b-startups, pricing) | no | ⬜ |
| 0.16 | 🧑 | Send the full Claude chat review (main part, not only the addenda) | no | ⬜ |
| 0.17 | 🧑 | Send the reference videos (ImagineArt one, the Skuve one, others) + say which company each is for | no | 🟡 1 received |
| 0.13 | 🤖 | Deliverable doc skeleton → `deliverables/DELIVERABLE.md` | no | ✅ skeleton done, fills as we go |

When 0.2 and 0.12 are done, open Poolday and run A1 → Phase B in one sitting (≈45 min), then Phases D–F.

---

## PHASE A: Setup (≈45 min, today, now)

### A1 🧑 Sign up for Poolday
- **DO:** open your personal invite link and create the account. Check that the $2,000 credits are showing.
- **DO:** turn on **notifications** (browser and email). Runs take about 1h, and notifications tell you when a run is done or has a question.
- **REPORT:** `done A1 — credits visible: $___`

### A2 🧑 Create the Instagram account (do it now: it needs time to warm up)
- **DO:** create a new IG account (use a new email). Add a profile photo, a name, and a bio with one line about what Poolday does plus the link. Switch it to a **Creator** account (this unlocks view stats).
- **DO:** spend 10 min warming it up: follow about 20 accounts in the AI and marketing niche, and like and comment on a few posts. **Don't post yet.**
- **EXPECT:** new accounts can post only **~1–2 times per day** before reach drops or the account gets flagged. This goes in the deliverable.
- **REPORT:** `done A2 — handle @___`
- **STATUS:** 🟡 warm-up started

### A3 🧑 Pick 2 reference videos (your taste = the biggest quality lever)
The skill copies the **cuts, rhythm and look** of the reference, so this choice matters more than any prompt.
- **DO:** on YouTube, search for things like "Linear launch video", "Raycast launch", "Arc browser launch", "Vercel Ship keynote opener", "Apple product intro". Pick videos that are 30–60s with dense cuts.
- **For Wispr Flow:** pick one with **kinetic typography + UI** (text flying and wiping across interfaces). That fits "speak → text appears everywhere".
- **For Flam:** pick one with **camera moves through 3D space and physical-world shots**. That fits mixed reality.
- **DO:** for each, write 2–3 specific things you love, named as mechanisms: *"hard cuts on the kick drum"*, *"oversized type wiping across the UI"*, *"one continuous camera push at the end"*. Not "it's premium".
- **CHECK:** it must be a **YouTube, TikTok, IG or X link** that plays publicly. Google Drive and Dropbox links don't work.
- **REPORT:** `done A3 — WF ref: <link> (likes: …) / Flam ref: <link> (likes: …)`. I'll write the final prompts with your links in them.

---

## PHASE B: Launch 5 Poolday conversations in parallel (≈30 min, right after A3)

For **every** conversation: new conversation → set mode to **Align** (bottom right, instead of Clarify) → set the **tier** listed below → name the conversation as listed.

### B1 🎬 Conversation "WF – skill" (tier: **Max**)
- **DO:** drop the file `poolday/ref-replicate-skill.md` into the chat, then paste the Wispr Flow prompt from `poolday/kickoff-prompts.md` with your reference link and your "what I love" lines filled in.
- **EXPECT:** Align asks you questions **one at a time**. Answer briefly. When it has no more questions, type **`start building`**.
- **REPORT:** `done B1 — started HH:MM, questions it asked: …`

### B2 🎬 Conversation "Flam – skill" (tier: **Max**)
- Same as B1 with the Flam prompt and the Flam reference.

### B3 🎬 Conversation "WF – threejs" (tier: **Max**): the A/B test
- **DO:** paste only this, with no skill:
  `Build a video for Wispr Flow (https://wisprflow.ai) in threejs. Make the most impressive video possible. Rich visual detail, seamless continuity from start to finish. 16:9, ~20 seconds.`
- **WHY:** we compare it with B1 and keep the winner. This comparison is a "method" point in the deliverable.

### B4 🎬 Conversation "UGC – actors" (tier: **Light** for the photos)
- **DO:** your Pletor method. Start with *"First generate 30 actor photos… let me choose"*.

### B5 🎬 Conversation "LinkedIn – concepts" (tier: **Standard**)
- **DO:** paste:
  `I need a LinkedIn video (4:5, under 45 seconds) that makes B2B marketers and founders excited about Poolday and makes them want to book a demo. Before building anything, give me 5 distinct concept directions, each with: the use case shown, the hook for the first 2 seconds, and the story arc in 3 beats. Wait for my choice.`
- **EXPECT:** 5 concepts. **Don't pick yet.** Paste them to me and we'll pick together, weighing which one generates *qualified* leads.

**At the end of Phase B, 5 runs are going. Log each start time. Render time and credits spent per run are data for the deliverable.**

---

## PHASE C: While Poolday runs (the next ~1–2h)

### C1 🤖 Say "build the loop" → I build the agent loop (D3) in this repo
You don't need to do anything technical here. I'll ask if I need an API key (Anthropic API key for qualifying leads and drafting emails).

### C2 🧑 Collect material for the reviews (D6 + D7). poolday.ai is blocked from my session, so I need you to be my eyes
- **DO:** take **full-page screenshots** of https://poolday.ai and https://poolday.ai/solutions/b2b-startups on **desktop and mobile**. In Chrome: DevTools → Cmd+Shift+P → "Capture full size screenshot". For mobile, toggle device mode first.
- **DO:** copy-paste the **visible text** of both pages into a file, or drop the HTML (right-click → Save page as).
- **DO:** watch the video you want to review (PostHog **or** Upflow; pick the one with more flaws, since that makes a better review). Take a screenshot every time something happens, with its timestamp.
- **DO:** drop all of it here (or in Claude chat). I'll write the reviews and log the method.

### C3 🧑 Answer Poolday when notified
Poolday may ask questions mid-run. Answer quickly, because an unanswered question stops the run.

---

## PHASE D: The skill's approval gate (B1, B2), about 30–60 min after "start building"
The skill stops **once**, with 3 sections. This is your only chance to fix things before the expensive render.

| Section | What to check | How to answer |
|---|---|---|
| **Script / swap table** | Is the story right for this company? Is the claim true? Are the figures sourced? | Approve, or edit a line: *"Row 3: replace 'X' with 'Y'"* |
| **Look** (keyframes next to reference frames + 3s render) | Does it feel like the same film as the reference? Is the logo, colour and UI right? | Name the mechanism: *"keyframe 4: the UI is too small, fill 70% of the frame"* |
| **Routing** (Remotion vs. Seedance) | Is anything physical (people, places) on Seedance and UI/text on Remotion? | Usually approve |

- **DO:** take a screenshot of the gate (good evidence for the deliverable), then confirm.
- **REPORT:** `done D — B1 gate: approved / edited …`

---

## PHASE E: Iterate on first cuts (the guide says ~7 prompts for the first video)
For every finished video:
1. Watch it **once as a viewer** (does it hook you? would you finish it?) and **once as a director** (pause at each cut).
2. Write feedback **as mechanisms with timestamps**. Template:
   ```
   Strong: <what to keep>.
   Changes:
   1. 0:0X — <cut/hold/easing/text/sync> → <exact change>
   2. ...
   ```
3. For small fixes, use **point & select** (click the element on the canvas, then describe the change) or the **live editor**. That needs no full re-render.
4. **REPORT** each round: `B1 round 2 — feedback: …, render took X min`. I log prompts per video, which is the "7 → 4 → 2" learning curve.

Compare **B1 vs. B3** (skill vs. threejs). Send me which one wins and why.

---

## PHASE F: Lock the winning flow
When the first prospect video is final:
- **DO** (in that conversation): `Save this whole flow as a skill and create a /prospect-video command that takes a company URL and a reference video link.`
- **DO:** download the MP4s. Upload them to your Drive and send me the links (videos are too big for the repo).
- **REPORT:** `done F — /prospect-video saved`. The agent loop will use this command, and we'll test it on a 3rd company (Convex) to show it takes about 2 prompts.

---

## Later phases (explicit steps get added here as we reach them)
- **G:** UGC production + posting schedule (1–2 posts/day, and log views at +24h)
- **H:** LinkedIn video final + post copy (I draft, you pick)
- **I:** agent loop end-to-end demo on 3 leads + screen recording
- **J:** reviews written (D6, D7) + growth idea final
- **K:** assemble the deliverable doc (+ **Pletor UGC farm screenshot** in the appendix)

---

## Credit budget (tentative: adjust after we see the first run's cost)
| Bucket | $ |
|---|---|
| Prospect videos (B1–B3 + iterations) | 700 |
| LinkedIn video | 300 |
| UGC (4–19 videos) | 500 |
| Agent-loop test videos | 300 |
| Reserve | 200 |

---

## POOLDAY SESSION 1 (live): setup + 5 parallel conversations
Observed in the app: sidebar Assets / Capabilities / Automations / Apps; composer with `+` (attach), `Auto`, `@`, `</>`, a tier selector (shows **Core**) and a mode selector (shows **Clarify** → switch to **Align**). The account shows "…team · Ent…" (Enterprise? The brand kit says Enterprise includes **API access**).

| # | Conversation | Tier | Mode | Goal |
|---|---|---|---|---|
| S0 | none | none | none | Enable notifications. Find the credit balance + API keys (account menu bottom-left, Capabilities) → screenshot to Claude Code |
| S1 | "Setup: skills" | lowest | Align | Save motion-craft + ref-teaser as skills |
| S2 | "Brand kit: Wispr Flow" | high | Align | brand:wisprflow |
| S3 | "Brand kit: Flam" | high | Align | brand:flam + what Flam actually does today |
| S4 | "UGC: actors" | lowest | Align | 30 actor photos → pick |
| S5 | "Brand kit: Poolday" | mid | Align | brand:poolday (for LinkedIn/growth videos; compare with the Claude-made kit) |
Then: prospect videos inside S2/S3 once the kits are done (the v2 kickoff in `poolday/kickoff-prompts.md`).
