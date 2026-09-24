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

## M10. Agent loop (D3)
- **What:** a local pipeline: find leads → enrich → qualify → generate the Poolday prompt → a human pastes it into Poolday and pastes back the video link → human validation gate (approve / reject / regenerate with a note) → draft the email → export (.eml + CSV). The hiring manager sends the emails.
- **Tools:** Claude Code sub-agent (built and tested it). Python 3.11 standard library (SQLite, http.server, email). The Anthropic Python SDK for API mode.
- **Inputs:** `data/series-b-bay-area.csv`, `research/company-picks.md` (scoring criteria), `poolday/kickoff-prompts.md` + `ref-replicate-skill.md` (prompt style), `poolday/agent-guide-notes.md`.
- **Process:**
  1. Pluggable lead sources (the CSV, plus a funding-news stub) → dedupe by domain → drop Higgsfield.
  2. Enrich: days since the round, the best buyer contact ranked by title, segment and geo flags.
  3. Deterministic pre-score out of 100 (freshness 40, buyer 25, B2B 15, video fit 20). It cuts weak leads before any LLM call.
  4. LLM rubric: 5 criteria × 20 points (B2B, freshness, named buyer, visual product, video need), returned as structured JSON with a justification, video angle, launch hook and audience. Keep ≥70.
  5. Generate a 2-line `/prospect-video` prompt plus a fallback kickoff prompt (intent-level).
  6. Dashboard: a copy button for the prompt, a field to paste the video link, approve / reject / regenerate-with-note. Regenerate turns the note into a revision prompt for the same Poolday conversation (v2, v3…).
  7. On approval, an editable email draft → export as .eml + CSV. Every decision is recorded in an event log.
- **Three LLM modes:**
  - **Mock:** offline and deterministic, for demos.
  - **API:** when `ANTHROPIC_API_KEY` is set.
  - **Claude Code:** the `/process-leads` command has Claude Code do the LLM parts, so no key is needed.
- **Verification:** `cd loop && make test` (5 end-to-end tests pass: the full loop, dedupe/exclusion, the Claude Code round trip, the feed stub, the dashboard over HTTP) and `make demo`. API request shape was checked against a local fake endpoint. Result on the CSV (mock scoring): 37 leads → 27 passed the pre-score → 5 kept at ≥70: Flam 99, TwelveLabs 83, Blacksmith 79, Wispr Flow 73, Convex 73. This matches the manual picks in M2.
- **Decisions & why:**
  - **Standard library only:** the demo runs anywhere with nothing to install.
  - **Pre-score before the LLM:** saves calls, and the loop works without an LLM.
  - **Regenerate = a revision in the same Poolday conversation:** follows the agent guide's rule on variants.
  - **Exports are drafts only:** a human sends them.
- **Lessons:**
  - The first rubric scored Wispr Flow at 69 because it missed the "moving into meetings" expansion. Video need now counts product-expansion signals.
  - Email copy must match the timeline: "post-raise launch push", not "announcement coming".
  - Testing against a local fake endpoint caught request-shape bugs without spending anything.
- **Limitations:**
  - The Poolday step is manual (no public API).
  - The CSV has no email addresses, so `To:` is blank.
  - The funding-news source needs a domain resolver.
  - The mock redraft doesn't apply the reviewer's note.
  - Gmail drafts are a stub.
  - The dashboard is local and single-user.
- **Time/credits:** ~1h build, $0 in Poolday credits, $0 API spend.

## M11. Course corrections from the user's review (round 1)
- **Reviews (D6/D7):** extracted the two prompts into standalone files (`deliverables/PROMPT-A-page-review.md`, `PROMPT-B-video-review.md`) so they paste cleanly into Claude chat. The results come back to Claude Code for the final write-up.
- **UGC (D4):** the user runs it with their proven format (shock face + iPhone product demo, from their Casey AI/Pletor work), made in Poolday following the brief's intended steps (options first, Align mode). Our scripts become optional backup.
- **Growth idea (D5):** being rewritten. Shorter and concrete. Render time is treated as unknown until measured, unverified risks are removed, and the templates come from research into what's actually trending (Apple-style motion first).
- **LinkedIn (D1):** being reworked around current-trend viral angles ("we killed AI slop", an AI video slop benchmark, remaking viral fake "one prompt" videos for real).
- **Agent loop (D3):** adding a Poolday API client (the brief implies an API exists). Endpoints are mapped from a config file because the docs aren't available yet. A fake Poolday server is used for tests. Real Anthropic API mode will be tested on a ~$2 budget with a cheaper model on 3–5 leads.
- **Security:** the API key is kept outside the repo (a session-only env file), `.env` files are git-ignored, and a check runs before each commit to make sure no key is in the repo.

## M12. Growth idea rewrite (D5 v2)
- **What:** rewrote D5 to be short (~900 words), concrete, and limited to claims we can back up, following the user's feedback.
- **Tools:** Claude Code sub-agent. 7 web searches (worked); page fetches of YouTube and X were blocked by the network, so view counts weren't checked.
- **Process:** searched for trending motion styles, the viral "one prompt" posts, and competitors. Wrote the doc in the user's structure: idea → flow → templates → X replies → funnel → unknowns → staged budget → targets → risks. Trimmed from 1,203 to 957 words.
- **Decisions & why:**
  - **Render time treated as unknown** (measured in pilot days 1–2). The page shows the video on the page if renders are fast and emails it if they're slow.
  - **Templates picked by recognizability, with evidence from tutorial/course volume and 2026 trend lists:** Apple-style product motion (incl. Liquid Glass), kinetic typography, 3D CGI product ad, "one prompt" code-made motion graphics, founder video with bold captions.
  - **Unverified claims cut:** the spam flag, operator throughput, sub-metric percentages.
  - **Budget in stages:** ~$2k manual pilot → ~$5k public page → ~$8k scale, each stage opened by a trigger.
- **Finding:** search results indicate Motion announced a "paste a URL, get a launch video" capability in Aug 2026, so the mechanic isn't new. The doc treats Motion as both the precedent and the main competitor: Poolday has to win on output quality (proved publicly through the X remakes) and on the human demo offer. *To be verified by opening the source links.*

## M13. LinkedIn rework around current trends (D1 v2)
- **What:** re-ranked the LinkedIn angles around this week's AI trends, per the user's feedback (only the "remake a viral fake video" angle could go viral).
- **Tools:** Claude Code sub-agent. 13 web searches (worked); page fetches of X, TechCrunch and others were blocked, so those claims come from search snippets and should be checked before quoting numbers.
- **Trends found (to verify via the links in the doc):**
  - Major model launches this month.
  - A wave of "made with one prompt" motion videos whose fine print admits hours of agent work.
  - LinkedIn's "Seems like AI slop" button (Jul 30), which cuts reach on flagged posts.
  - The Sora shutdown, and brands pulling AI ads after backlash.
  - Motion shipping URL → launch video inside Claude.
- **Ranking** (virality / lead quality / 48h feasibility):
  1. **The AI Video Slop Test:** the same B2B launch brief run through the leading video models, a "one prompt" setup, and Poolday, shown side by side with fairness rules fixed up front. This merges the user's "we killed AI slop" and "benchmark" ideas.
  2. **"One prompt" receipts:** remake a viral video in Poolday with the creator's OK, and show the real prompt, time and credits.
  3. **"5 tells your launch video is AI slop":** a teardown built from #1's footage.
  4. **URL → video:** demoted from hook to CTA mechanic because of the Motion overlap. It's still the best filter for qualified leads.
- **Decisions & why:**
  - **The comparison is the proof the slop claim needs,** and it attracts people choosing video tools, who are buyers.
  - **Fairness rules and a "rerun it yourself" invitation** protect credibility with an audience ready to hit the slop button.
  - **Creator consent before any remake** avoids a "dunking on creators" look from an exec account.
- **Notes:**
  - #1 needs a small spend outside Poolday for the other models' clips.
  - Commenters have no funding date, so set `PRESCORE_GATE=30` when feeding them into the loop.

## M14. Agent loop v2: Poolday API client + real LLM run (D3)
- **What:** the loop can now drive Poolday through an API. The real LLM mode was tested with a real key on a tiny budget.
- **Tools:** Claude Code sub-agent. Python standard library (urllib, http.server, sqlite, tomllib), the Anthropic Python SDK, a local fake Poolday server, unittest.
- **Process:**
  1. Defined a `PooldayClient` interface from what the loop needs (start a production, follow-up message, poll status, answer the agent's question, fetch the result, credits). No endpoints were guessed.
  2. Put every Poolday-specific detail (base URL, auth, paths, fields, status names) in one mapping file, `loop/poolday_api.example.toml`, marked "FILL FROM POOLDAY API DOCS". The client refuses to run while any TODO is left. `loop/POOLDAY_API.md` lists the questions to answer from the docs.
  3. Built a fake Poolday server with deliberately different conventions, so the mapping code gets exercised: runs go queued → running → a mid-run question → done; follow-ups make v2; failures and credits are simulated.
  4. Wired it into the dashboard:
     - **Send to Poolday** submits the prompt, and a background poller follows the run.
     - The agent's questions appear with an Answer box.
     - A finished video lands in **Review**.
     - **Regenerate with note** posts a revision to the same conversation.
     - Every API call is logged (auth never logged).
     - The human gate is unchanged: nothing is sent without approval.
  5. Real LLM run: 4 leads on the cheaper model, then read the outputs, fixed, and re-ran.
- **Results (real API):**
  - **Scores:** Flam 95, TwelveLabs 76 and Wispr Flow 75 qualified. Arcee AI (62) was knocked out for having no named buyer.
  - **Emails:** all 3 passed the code checks after fixes.
  - **Cost:** ~$0.045 total, ~$0.003 per qualification and ~$0.003–0.006 per email.
- **Bugs found by the real run that mock mode couldn't catch:**
  - The effort parameter is rejected by the cheaper model → now sent per model.
  - A lead with no buyer qualified → now a code-level knock-out.
  - The model misapplied the freshness bands and the totals → freshness is computed in code, and the total = the sum of the criteria.
  - Angles were too long → capped.
  - Emails broke the style guide → the hard rules are checked in code, with one repair call, and anything still failing is shown to the reviewer.
- **Decisions & why:**
  - **A mapping file, not hard-coded endpoints:** filling it takes minutes once the docs arrive, and nothing fake looks real.
  - **Polling first, webhooks later:** it works on localhost.
  - **Prompts with unfilled `<…>` slots are refused before any credits are spent.**
  - **The cheaper model for testing, a stronger model for the real emails:** the wording quality is noticeably better on the stronger model.
- **Verification:** `cd loop && make test` → 16 tests pass. `make demo-api` runs the whole thing in ~15s. The git history was scanned for the key: none.
- **Lessons:** a real run surfaces problems a mock can't. Anything that must be exact belongs in code, not in the prompt.

## M15. Round 2 of user direction
- **Growth idea (D5 v3):**
  - 3 products on arrival: Launch video (styles: Apple, Kinetic, Storytelling), Podcast clips (Hormozi + other famous clip styles), AI product ad.
  - A cost model per product: measured Poolday credits (credits appear to be priced in dollars; verify) plus a bottom-up sanity check from public model API prices.
  - Visual mockups: 4 screens + a GIF walkthrough, built as HTML and rendered with Playwright, in a dark, minimal "superintelligence" design system that will be reused for the page rebuilds.
- **LinkedIn (D1 v3):**
  1. "Same prompt, 4 apps": Higgsfield, Poolday, Kling, Seedance.
  2. "Reply with proof" remakes, inspired by Higgsfield's After Effects plugin replies.
  3. A "your launch video is now free, comment your URL" hook, with an honesty check on any claim that a specific model made the video.
- **UGC (D4):** the user's Pletor pipeline is recorded in `poolday/pletor-ugc-reference.md` (base character → shock face → image-to-video), with an intent-level Poolday brief that follows the brief's method (30 actor photos → pick → variants). The farm screenshot is kept for the appendix (`deliverables/assets/pletor-ugc-farm.webp`).
- **Page review (D7):** critiqued the Claude chat draft (`deliverables/D7-review-draft-claude-chat.md`). Pricing is the most impactful part. Never change factual claims in rewrites, cut the repetitive slogan pattern, and verify the cited numbers.
- **References:** the first reference video received is `references/ref-x-video-1.mp4` (12s, 16:9, beige background; colorful tiles linked by lines → a radial fan of cards → a horizontal carousel of image cards moving in a wave). Frames were extracted with ffmpeg for the analysis.

## M16. Growth idea v3: three products + cost model (D5)
- **What:** D5 v3 with three products (Launch video, Podcast clips, AI product ad), 4 clicks each: pick a product → one input → a style card → work email → video.
- **Styles:**
  - **Launch:** Apple, Kinetic, Storytelling.
  - **Podcast:** Hormozi, Diary of a CEO, MrBeast, Ali Abdaal, Iman Gadzhi. Picked because each has a documented template or how-to; Modern Wisdom was dropped because no documented style was found.
  - **Ads:** 3D hero CGI, faux out-of-home (the most-cited viral CGI ad format of 2026), UGC, Cinematic.
- **Tools:** Claude Code sub-agent. 13 web searches. The claude-api skill for LLM prices. Page fetches (poolday.ai, fal.ai) were blocked, so prices come from search snippets: re-check on fal.ai before quoting.
- **Cost model:**
  - **Formula:** $/delivered video = credits per run × runs per delivered video × $/credit. It gets filled from the user's first Poolday runs, reading credits used in the UI.
  - **Bottom-up [est.]:** launch video 25s ~$3–10; 5 podcast clips ~$5–10; AI product ad 15s ~$12–25 (generative video dominates). All three land inside the reported ~$5–25 per video.
  - **Budget:** blended ~$19 per video (40/30/30 product mix + 30% re-renders) gives ~790 videos for $15k across 3 stages. At 5% video → demo, that's ~$380 per booked demo [est.]. The AI ad is the product to cap.
- **Why this beats Motion:** 3 products instead of 1; podcast clips as a weekly repeat use case; generative ads; a human call offer; quality shown in public through the X remakes. Motion's URL → launch video launch (X post, Aug 2 2026) is confirmed in search results.
- **Finding:** Poolday's Enterprise plan reportedly lists "API access" [verify]. If so, the D3 Poolday client can automate the page.

## M17. LinkedIn v3 (D1)
- **What:** 3 angles, ranked, with full copy for each, a Poolday brief for the top pick (103 words, Align mode, options first), the comment-to-lead process and metrics.
- **Ranking:**
  1. **Same prompt, 4 apps (Higgsfield, Kling, Seedance, Poolday).**
     - The brief: one 15s B2B launch brief, sent word for word to each.
     - Fairness rules: same text and files, 1 attempt + ≤3 revisions, ≤60 min per tool, no edits outside the tool, all four published even if Poolday doesn't win, brief and files public so anyone can rerun it.
     - Takeaway: "a model makes clips, an agent makes the video."
     - Cost outside Poolday: ~$45–65.
  2. **Free launch video, comment your URL:** the first [20] B2B companies get one within 72h. This doubles as the launch of the URL → video tool. A hook naming a specific model is allowed only once Poolday confirms it ran on it; honest alternatives are provided.
  3. **Reply with proof on X:** a playbook (search queries, what to remake, a sped-up screen recording with a real clock, a reply template, consent and credit rules). The best reply becomes a LinkedIn post.
- **Tools:** Claude Code sub-agent, ~7 web searches. Fetches of Higgsfield pages were blocked (snippets only).
- **Decisions & why:**
  - The comparison goes first because it creates the agent-vs-model proof the other posts rely on, and it reaches people choosing tools.
  - The CTA asks for a URL, not just a keyword, which filters leads and avoids the engagement-bait penalty.
  - "Free" is tied to a real, capped offer, so it's true.
- **Unverified:** Higgsfield replying to "AI can't" posts with recordings (only their After Effects "AI Motion Designer" launch, ~Sep 10–13, is confirmed); which model Poolday runs on; tool prices on the day.

## M18. Video review (D6)
- **What:** reviewed both Poolday showcase videos (PostHog GenAI launch, Upflow faster payments).
- **Tools:** ffmpeg (a static build via the `imageio-ffmpeg` pip package, since the system had none): 1 frame/s contact sheets, scene-cut detection (`select='gt(scene,0.25)'`), full-size key frames. Claude Code read the frames. The user's own viewing notes: scenes 1–2s too long, try 1.5×, the PostHog end card looks like PowerPoint, PostHog should be 2D.
- **Process:** mapped each scene to a timestamp → listed the problem → wrote each fix as a mechanism (cut, hold, typing speed, payoff shot). Made a 1.5× quick test of Upflow (`setpts=PTS/1.5`, `atempo=1.5`) to check the pacing hypothesis.
- **Findings:**
  - **Upflow:** a strong idea with slow holds (typing 4s, logo typing 4s). **The product never appears**: the "did Acme pay?" setup is never answered. The best proof (79%) is micro-text.
  - **PostHog:** high production value but off-brand (3D clay vs. PostHog's 2D illustrated identity). The climax "It's live" is tiny. Product proof is ~2s of tiny tabs. The end card is a static web-footer slide.
- **Root causes:**
  - The agent's default pacing is too slow for SaaS UI → propose a "SaaS UI pacing" Poolday skill with numeric rules plus reference videos.
  - The brand kit captured the identity but not the brand's visual medium → feed it the illustration assets and add a "2D only" usage law.
- **Output:** `deliverables/D6-video-review/D6-video-review.md`, `upflow-1.5x-quicktest.mp4`, and 2 remake prompts (intent-level) to produce before/after proof in Poolday.

## M19. Growth-tool mockups + design system (D5 visuals)
- **What:** 4 screens (landing, style, generating, result) + podcast and product-ad variants + mobile, a 15s walkthrough (GIF + MP4), and a reusable dark "superintelligence" design system (`deliverables/design/tokens.css`) for the page rebuilds.
- **Tools:** WebSearch for 2026 AI-launch aesthetics; static HTML/CSS + inline SVG; bundled fonts (Inter, Inter Tight, Geist Mono) so rendering never needs the network; Playwright + the preinstalled Chromium to render; ffmpeg to encode.
- **Process:** tokens → shared components → one HTML page per screen → render → look at each PNG → iterate (stronger horizon arc, kinetic-type spacing, speaker silhouettes, bounding boxes placed on real elements, a chart collision). The walkthrough is a time-driven HTML timeline (cursor path, typing, crossfades, progress) captured frame by frame (450 frames at 30fps), not screen-recorded, so timing is exact and gradients stay clean.
- **Design decisions:**
  - **The signature is a lit "horizon" arc:** a pool surface at dawn.
  - **One accent light (cyan), used only for focus and progress.** Orange, asterisks and purple-pink gradients are avoided, so it can't be mistaken for other AI labs.
  - **Monospace for machine facts:** it makes the agent feel like it's working.
  - **Customer brand colours stay inside the media:** the UI stays neutral next to any brand.
- **Placeholders:** "1,284 videos made today" is illustrative; the podcast style names reference real creators (legal check or rename); the logo is a placeholder; Northwind is fictional.
- **Reproduce:** `cd deliverables && python3 -m http.server 8765 &` then `NODE_PATH=/opt/node22/lib/node_modules node D5-mockups/src/render.js` (and `capture.js` for the walkthrough).

## M20. Reference videos + motion-craft manual
- **Inputs from the user:**
  - ImagineArt video (the easing, the speed, the tiles → radial fan → carousel continuity).
  - Skuve "Product Search" reel (a clean light UI world, numbered product cards, one lime accent).
  - A "stretching creativity to its limits" kinetic serif-type video (brand unknown).
  - `motion-design-for-agents.md`: a motion-design manual distilled in another Claude conversation from analysing many great motion pieces (timing, easing curves, staggers, settles, texture, typography, sound, a per-scene checklist).
- **Decision: a three-input setup for every Poolday video:**
  - **Taste** = the reference video.
  - **Craft** = the manual, saved as a Poolday skill ("motion-craft").
  - **Process** = the ref-teaser skill.
  - Plus a brand kit that captures the brand's visual medium.

  Why: each input fixes a different failure seen in the review. The reference fixes generic style, the manual fixes template-looking motion and slow holds, the skill fixes lost continuity, and the kit fixes off-brand output.
- **Aligned** the D6 pacing rules with the manual. The logo lockup is 2–3s including a ≥0.6s *alive* hold, not a static slide.
- **Files:** `references/README.md`, `poolday/motion-design-for-agents.md`, `poolday/kickoff-prompts.md` (v2 section).

## M21. Reference mapping + growth mockups v2 brief
- **Mapping (decided with the user):**
  - Wispr Flow ← Skuve.
  - Flam ← ImagineArt (motion taste) + ElevenLabs node-canvas videos + "stretching creativity" (collage, serif italic kinetic type, bomb metaphor, colour-dot loader; analysed on a 1 frame/s contact sheet).
  - Open point: the CSV describes Flam as mixed-reality marketing, the user as a node-based creativity tool. Check the live site before the story brief.
- **Mockups v2 (user feedback on v1):**
  - Remove "free, no sign-up".
  - A progress bar that fills on every click.
  - New steps: "Do you have a screen recording?" and "Do you have a brand kit?", each with an "upload" option and a highly clickable "Poolday AI does it for you" option.
  - A longer, more magical generating sequence, including "AI records a walkthrough of your SaaS" (plausible: the Poolday b2b page reportedly lists "The demo records itself" [verify]).
  - Multi-scene animated style previews: Apple liquid-glass UI, kinetic, founder studio film.
  - Punchier style names.
  - Real (CC-licensed) photos in the podcast styles.
  - All brand values isolated in tokens, so Poolday's real kit can be swapped in.
- **Blocker:** Poolday's brand. poolday.ai is denied by the environment's egress policy (`connect_rejected`), so the brand comes from the user: allow the domain, or upload the logo, screenshots and font names, or export the kit from Poolday's own brand-kit feature.

## M22. Poolday brand kit received → re-skin + page rebuilds
- **Input:** `deliverables/design/poolday-brand-kit/`, built by the user in another Claude session from the live site. It contains measured tokens (pure black ground, ink #f5f5f5, off-white cta pill, Inter), the halftone scan-dot signature, components, copy rules (headlines end with a period, one CTA verb "Book a 15 min demo", recipe captions), a copy bank, a homepage UI audit with measurements and a friction list, and a reference screenshot.
- **Decisions:**
  - **Growth mockups:** re-skinned from the invented v1 identity to Poolday's kit. The user's asks are reconciled with the brand rules: the "Poolday AI does it for you" button is the one cta pill in view with a halftone shimmer (no neon glow); the progress bar is a thin ink line; colour lives only inside the media ("the videos are the colour").
  - **D7 page rebuilds started:** before (reconstruction) / after for home, b2b-startups and pricing, in the kit. Annotated side-by-sides plus a ranked change list with an A/B test per change.
  - Rules carried over from the critique: never alter factual claims, limit the slogan pattern, mark unverified numbers.
