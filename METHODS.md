# Methods Log: how everything was made

A record of every process in this project: what was done, with which tool, how decisions were made, and what we learned. It feeds the "How I worked" section of the final deliverable.
**Rule:** every finished step gets an entry here. Write it in the same session the step happens (Claude Code keeps this file up to date; see `CLAUDE.md`).

Entry format: **What · Tools · Inputs · Process · Decision & why · Output · Time / credits · Lessons**

---

## M1. Project planning
- **What:** broke the 7-deliverable assignment into a 48h plan.
- **Tools:** Claude Code (this repo), the Poolday agent guide (pasted in by the user; poolday.ai is blocked from the cloud session).
- **Process:**
  1. Split the brief into deliverables D1–D7.
  2. Read the agent guide and extracted the facts that constrain planning: a run takes about 1h or more, the first video takes about 7 prompts, variants stay in one conversation, skills and commands cut later videos to 1–2 prompts, there's no public API, and Poolday doesn't post to social.
  3. Designed "two lanes, zero idle time": Poolday renders in 5+ parallel conversations while the human does creative work and Claude Code builds.
  4. Put the long-running jobs (brand kits, prospect videos) at hour 0 because they need the most iterations.
- **Decision & why:** parallelize across *different videos*, not across variants of the same video, because the guide says variants clone faster inside one conversation.
- **Output:** `PLAN.md` (v1, then v2 after the guide).
- **Lessons:** the plan changed materially once we had the guide (brand kits first, and the skill/command reuse became the backbone of the agent loop). Read the tool's docs before planning.

## M2. Prospect company selection (D2)
- **What:** picked 2 companies from the Series B list (Higgsfield excluded).
- **Tools:** Claude Code (Python over the CSV), judgment.
- **Inputs:** `data/series-b-bay-area.csv` (38 companies + Higgsfield).
- **Process:**
  1. Defined 4 scoring criteria: **(a) freshness of round** (fresh money → launch and hiring push → needs video now), **(b) a named marketing or creative buyer in the CSV** (someone to send it to), **(c) a visual product** (good material for the video), **(d) fit with video as a need**.
  2. Filtered to rounds in the last 90 days with a script (reproducible):
     `python3` → parse "Round date", compute days before 2026-09-24, keep ≤90, print contact titles.
  3. That gave a shortlist of 9. Removed companies with no contacts (Arcee, Standard Metrics) or an unverified HQ or weaker segment (Delightree, Flex).
  4. Compared the rest on (c) and (d).
- **Decision & why:**
  - **Flam:** freshest round with contacts (10 days ago, $40M). The CMO and Creative Director are listed, and the company is video-native.
  - **Wispr Flow:** biggest fresh round ($280M, 38 days ago), design-led marketing contacts, and an upcoming "meetings" launch that gives the email its hook.
  - **Backup: Convex**, because it's open source, so the skill can use its real UI components.
- **Output:** `research/company-picks.md`.
- **Pitch line:** "Companies that raised in the last ~5 weeks where the list names a marketing or creative decision-maker: fresh money plus an upcoming launch means they need video now, and there's someone to send it to."

## M3. Poolday prompt strategy for prospect videos (D2)
- **What:** decided how to brief Poolday.
- **Tools:** Claude Code (analysis of `poolday/ref-replicate-skill.md`), the agent guide.
- **Process:**
  1. Read the skill. It takes a reference video link and a brand URL, writes the brand kit, story, storyboard and routing by itself, and asks the human once, at a single gate.
  2. Key insight: the reference's look beats the brand's, so **choosing the reference video is the biggest creative lever**. That choice is the human's job.
  3. Kept the kickoff prompt short (the brief's tip: don't paste long Claude prompts, let the agent drive). The prompt includes only the reference, the brand, what we like about the reference (a guide recommendation), the objective and audience, and creative freedom.
  4. Set up an A/B test: the skill-based prompt vs. the brief's "build in threejs, most impressive video possible" prompt, in separate conversations. Keep the winner.
- **Output:** `poolday/kickoff-prompts.md`.

---

<!-- Next entries: M4 reference video choice, M5 Poolday runs (per conversation: tier, prompts count, render times, credits), M6 agent loop build, ... -->

## M4. Instagram account warm-up (D4)
- **What:** created a new IG account and started warming it up before posting any AI UGC.
- **Tools:** Instagram (manual).
- **Process:** new account → normal human activity (follow niche accounts, likes, comments) with **no posts** until the UGC videos are ready.
- **Decision & why:** new accounts that post straight away get throttled or flagged, and they can realistically post only ~1–2 times per day. Starting the warm-up before production means the account is ready by the time the videos are.
- **Status:** in progress (started before any Poolday work).

## M5. Parallel preparation before touching Poolday
- **What:** everything that doesn't need Poolday was prepared first, so Poolday time is spent only on directing renders.
- **Tools:** Claude Code with 5 sub-agents running in parallel (agent loop build, growth idea, LinkedIn angles, UGC scripts, review kit + deliverable skeleton).
- **Inputs:** shared context files written first so every agent works from the same facts: `BRIEF.md` (assignment + user notes), `poolday/agent-guide-notes.md` (condensed agent guide), `PLAN.md`, `research/company-picks.md`.
- **Decisions & why:**
  - **Page and video reviews run in Claude chat** (it can browse the web) instead of this cloud session, which can't reach poolday.ai. We prepared paste-ready review prompts with an explicit framework, so the output is structured and repeatable.
  - **The agent loop works without an API key** (mock mode + a Claude Code command), with the API as an option for running unattended. It can be demoed without any credentials.
  - Each agent writes only its own output file and hands back a methods note, to avoid conflicting edits.

## M6. Growth idea write-up (D5)
- **What:** turned the user's "paste your URL → watch your launch video" idea into a decision-ready proposal.
- **Tools:** Claude Code sub-agent (no web access). Inputs: `BRIEF.md`, `PLAN.md` §4, `poolday/agent-guide-notes.md`.
- **Process:** mapped each part of the idea to a Poolday capability confirmed in the agent guide (brand kit from a URL, screenshot rebuild, saved templates/commands, cloning, Light/Max tiers, pulling video from links, no public API). Then wrote 9 sections: pitch, UX, how it runs on Poolday, X distribution, lead routing, budget, metrics, risks, why now.
- **Decisions & why:**
  - **Email gate before the render:** it turns the ~1h run time into lead capture.
  - **Lead scoring before spending credits:** qualified B2B leads get Standard/Max renders and a personal follow-up; others get Light and self-serve. This lowers cost per booked demo.
  - **Demo offer = "your real launch video + 3 variants in 15 min":** it continues from the video they already received.
  - **Pilot with a human operator before any API work:** it tests demand without needing engineering from Poolday.
  - **Strict X reply rules:** max 3 replies a day, never accuse anyone of faking, skip human artists. This protects the brand.
  - **$3k pilot → up to $15k:** scale if the pilot gets ≥10 booked demos at ≤$300 each with ≥25% qualified leads. Kill if it gets <5 demos, <15% qualified, or >20% of renders fail QA.
  - Estimated numbers are marked **[A]**. Budget caps are in dollars because Poolday's credit cost per render is unknown; it gets measured on pilot day 2.
- **Output:** `deliverables/D5-growth-idea.md` (~2,300 words).

## M7. LinkedIn post prep (D1)
- **What:** use-case angles, post copy, comment-to-lead process, Poolday brief and metrics for the hiring manager's LinkedIn post.
- **Tools:** Claude Code sub-agent. Inputs: `BRIEF.md`, `PLAN.md`, `poolday/agent-guide-notes.md`, `poolday/kickoff-prompts.md`, `research/company-picks.md`.
- **Process:**
  1. Drafted 3 candidate angles and ranked them on four tests: does the CTA filter leads, do we need another company's permission, does it tie into D2/D3/D5, can it be honest about the ~1h run time.
  2. Wrote 2 post variants for each of the top 2 angles.
  3. Mapped comments onto the D3 loop.
  4. Kept the Poolday brief to intent only (107 words, checked with `wc -w`).
  5. Wrote metrics with check-ins at 24h, 72h and 14 days.
- **Decisions & why:**
  - **#1 "One URL in, brand kit + launch video out":** a comment with a URL is already a lead you can look up, the audience is broad, and it tests the growth idea live.
  - **Default example is poolday.ai:** no other company's brand is shown without permission. Angle #2 (a prospect's video) waits for that prospect's OK.
  - **Viral remakes go to X, not LinkedIn:** they bring low-quality leads and carry IP risk on an exec's account.
  - **CTA "comment VIDEO + your URL, I'll pick [10]":** the cap creates scarcity and limits credit spend.
  - **Link in the first comment:** links in the post body cut reach.
  - **Proof points left as placeholders:** they get filled with measured numbers, never invented ones.
- **Lessons:** the CTA itself is the lead filter.

## M8. AI UGC prep (D4)
- **What:** 4 angles, 15 hooks, 8 scripts (22–29s), a ranked posting plan for the first 5 posts, a measurement and iteration loop, the Poolday production flow, and compliance rules.
- **Tools:** Claude Code sub-agent. Inputs: `BRIEF.md`, `PLAN.md`, `RUNBOOK.md`, `poolday/agent-guide-notes.md`.
- **Process:**
  1. Pulled the constraints: 1–2 posts/day on a new account, ~$500 UGC credit budget, the guide's validation steps.
  2. Mapped the audiences (marketers, founders, agencies, social managers) to 4 angles: POV pain, "this is AI" reveal, founder/agency confession, steal-my-workflow.
  3. Wrote 8 scripts at ~2.5 spoken words per second so they land in 15–30s.
  4. Ranked the first 5 posts so every angle and both CTAs ("link in bio" and "comment VIDEO") get tested within 48h.
- **Decisions & why:**
  - **Only product claims documented in the agent guide:** nothing about Poolday is invented.
  - **The "this is AI" reveal goes first:** disclosure becomes the hook, which is the safest option for a new account and a strong pattern interrupt.
  - **POV/skit characters, never fake testimonials:** keeps it honest.
  - **IG "AI info" label on every post, plus "AI-generated with Poolday" in captions and bio:** clear disclosure.
  - **Iterate by swapping the hook on the same body:** the base is reused in one Poolday conversation, which is the cheapest way to iterate.
- **Poolday flow:** Align → brand kit → 30 actor photos, pick 3 → 5 voices each, pick 1 → pilot one script (~5–7 prompts) → save as `/ugc-reel` → batch the rest as variants in one conversation → polish in the live editor.
- **Lessons:** record Poolday screens during the D1/D2 runs. They double as B-roll for the UGC videos.

## M9. Review kit (D6/D7) + deliverable skeleton
- **What:** paste-ready prompts for Claude chat to run the page reviews (D7) and the video review (D6), plus the skeleton of the final deliverable doc.
- **Tools:** Claude Code sub-agent. The reviews themselves run in Claude chat (it can browse), because poolday.ai is blocked from the cloud session.
- **Process:**
  1. Turned the review criteria into fixed frameworks: 10 criteria for the pages (5-second test, value prop, segment fit, social proof, demo CTA friction, objections, instant-value entry point, video content, speed/mobile, experiments) and 11 for the video (hook 0–3s, arc, pacing, mobile legibility, sound-off, sync, proof, CTA, length…).
  2. Specified strict output formats:
     - **Pages:** an ICE-scored table (problem → change → why it books more demos → A/B test), before/after mockups of the top 3 changes, and 2 hero variants per page.
     - **Video:** timestamped fixes written as mechanisms, the top 3 changes, a rewrite of the first 5s, and an intent-level Poolday prompt to build the improved intro as proof.
  3. Built the deliverable skeleton from the plan outline, filling in what's already known and marking the rest `[PLACEHOLDER]`.
- **Decisions & why:**
  - **"Don't guess" rule, with the user's screenshots and frames as the source of truth:** it avoids made-up findings when a fetch misses JS-rendered content or the video can't be played.
  - **Every recommendation comes with an A/B test:** changes are judged against demos booked, not taste.
  - **"Instant value" criterion in the page review:** it ties D7 to the D5 growth idea.
- **Lessons:** when the environment can't see the subject, make the reviewer cite visible evidence (a quoted element or a timestamp).
