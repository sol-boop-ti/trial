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
