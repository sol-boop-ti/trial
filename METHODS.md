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
- **UGC (D4):** the user's Pletor pipeline is recorded in `poolday/ugc-reference.md` (renamed from `pletor-ugc-reference.md` on 24 Sep) (base character → shock face → image-to-video), with an intent-level Poolday brief that follows the brief's method (30 actor photos → pick → variants). The farm screenshot is kept for the appendix (`deliverables/assets/pletor-ugc-farm.webp`).
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

## M23. Page rebuilds, before/after (D7)
- **What:** before (reconstruction) / after (proposed) of home, /solutions/b2b-startups and /pricing in Poolday's brand kit. Annotated side-by-side comparisons (full page + first screen) and a ranked review with an A/B test per change (primary metric: completed demo bookings per visitor, plus a guardrail).
- **Tools:** static HTML on the kit's `tokens.css` + `components/bundle.css`; the kit's Halftone algorithm redone without React; Node build + render scripts; Playwright + Chromium, fully offline. Rebuild: `cd deliverables/D7-pages && node src/build.js && NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node src/render.js`.
- **Top changes:**
  - **Pricing** (the biggest lever): price per finished video in the lede ("Pay for finished videos, not seats."); the $600 first month named as a pilot band ("Month-to-month, no lock-in."); credits translated into videos per month; a persona line per plan; honest top-up wording; a qualitative comparison vs agency / freelancer / in-house; a security strip; logos; an FAQ.
  - **Home:** price facts under the hero CTA; "Watch a 2-min build" as the one secondary link; a demo CTA right after the video grid; "superintelligence" defined; investors split from customers.
  - **B2B:** H1 "Every feature you ship, on video."; a "Paste your URL" free launch-video field (the D5 growth idea as an entry point); use cases retitled from input to output, with recipe chips.
- **Decisions & why:**
  - Every Poolday fact kept word for word.
  - One secondary action per page.
  - The slogan pattern used twice in total.
  - No invented costs in the comparison.
  - Two made-up metrics that crept into placeholder tiles were caught and removed. Lesson: check placeholder art as strictly as headlines.
- **Unverified:** "~$5–25 per video" on the live site; Enterprise credits = plan price; the credits included in the $600 month; whether security docs exist; the details of every BEFORE layout. Screenshots of the live pages would make the befores exact.

## M24. D7 v2 after user feedback
- **Pricing:** back to the original 2-card table. The best ideas are kept as one-liners: a lede with the price per video, "≈ N videos a month" under each price, a persona caption per plan, and "First month $600 · a pilot, no lock-in". The big pilot band is removed. The comparison, procurement note and FAQ are trimmed and kept below the fold.
- **Home:** the 3 price facts under the hero CTA are removed (noise). "Watch a 2-min build" is kept.
- **B2B:** a tiny cyan "Free · limited" pill on the "Paste your URL" field. It's the only cyan on the page, using the kit's reserved signal colour.
- **Lesson:** pricing gains have to fit inside the original's simplicity. Extra blocks above the cards cost more clarity than they add persuasion.

## M25. Poolday live: API discovered, product feedback, cleanup
- **API confirmed by the agent itself:** there's a public API. Keys, reference docs, a playground and "video ready" webhooks live under **Capabilities → Integrations**. Flow: create a key (org-scoped, server-side only) → send a prompt (the same agent team as in chat) → webhook or poll → download the MP4. Lighter option: an **Automation with an inbound webhook** (POST to a URL → a saved prompt runs → the result appears as a conversation). The agent's advice matches our plan: build the video once in chat, save it, then let every API call run that tested brief (the `/prospect-video` command).
- **Next:** read Integrations → Docs → fill `loop/poolday_api.example.toml` → test in the Playground → run one real lead end to end.
- **Product feedback captured** (`deliverables/PRODUCT-FEEDBACK.md`): the upload modal clips its text; the UI/UX and Align flow are excellent.
- **Cleanup:** the UGC reference file was renamed to `poolday/ugc-reference.md` and no longer names the previous client, since it gets uploaded to Poolday.

## M26. D7 round 3
- **Pricing:** only two additions to the original: "≈ 50–250 finished videos a month" and "Your first month at $600 · no lock-in".
- **Home:** the feed is reorganized into 4 use-case rows (Launch films / Feature videos / Podcast clips / Ads), each with identical 16:10 tiles and one caption per tile (customer + recipe). Three alternatives are documented but not built.
- **B2B:** real customer logos (PostHog, ClickUp, Lovable, Dust, FullEnrich), taken from traceable npm sources (simple-icons CC0, lobehub MIT, Dust's own design-system package, FullEnrich's own n8n node). Marblism falls back to its name in type. Sources are in `deliverables/D7-pages/CREDITS.md`. Poolday should confirm logo permissions before anything goes live.
- **Lesson:** when websites are blocked, the npm packages companies publish themselves are a reliable source of official logos.

## M27. Growth-tool mockups v3 (built directly after the background task was stopped)
- **Changes from the user's review:**
  - Less noise: removed the helper copy on the recording and brand-kit steps, and "Each one is a full brief" / "Previews already use your brand kit" on the style step.
  - Style names: **Apple Motion Style / Kinetic Typo / Storytelling Film**.
  - **Real reference footage in the previews:** Kinetic Typo uses the unedited 0:00–0:14 of the "stretching creativity" video (including the bomb). Apple Motion Style (Langease, YouTube) and Storytelling Film (founder video) have ready slots and fall back to our own loops until the files arrive. YouTube is blocked from this environment (yt-dlp → 403).
  - **New step 5/7, "Last step. Your video is already being made."**: an Align-style card over the blurred style screen with work email (personal domains rejected inline: gmail, yahoo, outlook…), role, and how they heard about Poolday. Why: Poolday is an enterprise product, so free credits go to real companies, and every video becomes a qualified lead. The title keeps people on the page.
  - **Result:** "Copy link" replaced by a prominent **Share** button (share icon) with a menu (Copy link / LinkedIn / X).
  - **Visual language aligned with the Poolday app** (screenshots in `deliverables/design/poolday-app-ui/`): dark panels with large radii, hairline edges, faint dot noise, uppercase micro-labels, a lavender halo on the active card.
- **How:**
  - Footage becomes a deterministic JPEG sequence (`src/tools/make-footage.sh`, 15 fps, 640px), so frame-accurate capture still works.
  - The timeline adds the details step (typed personal email → rejection with a shake → corrected work email → role → source → send), then shifts generation and the result.
  - The share menu opens before the demo CTA is clicked.
- **Outputs:** 15 stills (+@2x) including `04c-details-personal-email-rejected`, `04d-details` and `06b-result-share`; `walkthrough.mp4/.gif`; `loop-kinetic-typo.mp4`; `CREDITS.md`.

## M28. D7 round 4: real live pages replace the reconstructions
- **Input:** the user supplied real screenshots of the live home (full page), the Meet Poolday features, and the pricing page, plus Submagic's pricing as inspiration. Saved in `deliverables/D7-pages/real/`.
- **Verified by the live pages:**
  - "~$5–$25 per finished video" is on the home page's closing CTA card.
  - Enterprise credits equal the plan price.
  - The real pricing layout: a light Business card, a dark Enterprise card, CTA "Book a call to get your agent configured".
  - The real home structure: masonry video grid, "Meet Poolday" with 4 animated features, logo marquee, testimonials, a light-grey CTA card.
- **Feedback applied:**
  - **Home:** remove the post-grid CTA; "Meet Poolday" loses "Not a tool you operate"; add "Book a 15 min demo" right after the features.
  - **Pricing:** rebuilt on the real page, with a Submagic-style framed box ("$1,250 in credits = ≈ 50–250 finished videos").
  - **B2B:** a tasteful "NEW" sticker replaces "Free · limited", and the use cases get animated previews like the home features.
  - **All pages:** legends list only the live changes.
- **Lesson:** reconstructions are a stopgap. As soon as real captures exist, the "before" must be the real page.

## M29. Why the B2B "before" was wrong (and a correction)
- **Cause:** poolday.ai is blocked by this environment's network policy (`connect_rejected`), so Claude Code never saw the live pages. The first BEFOREs were rebuilt from Claude chat's text summary of the copy plus the brand kit's homepage audit. Text can't carry layout: the masonry grids, "See the prompt" pills, the 3×3 use-case cards and the "Made in Poolday" grid were all invisible to us. The images were labelled "reconstruction", but the gap was bigger than that label suggested.
- **Fix:** the user's full-page captures of all three live pages are now the BEFOREs (`deliverables/D7-pages/real/`).
- **Correction:** our D7 critique said "95% need zero edits" was a distortion of "95% autonomy". The live B2B page actually says "Two weeks in, 95% of your videos need zero edits from your team." Claude chat's wording was faithful, and our objection was wrong.
- **Lesson:** for any visual review, get a real capture first (screenshot or saved HTML). Never review or redesign a page you haven't seen.

## M30. D7 round 4 finished: real frames in the AFTERs
- **Approach:** 38 tiles cut from the live screenshots (measured against a pixel-grid overlay, upscaled 3×) fill every unchanged tile in the AFTERs, so the only visual differences are the numbered changes. The B2B layout was corrected to match the live masonry.
- **Outputs:** `compare/{home,pricing,b2b}-compare(-fold).png`, `video/{b2b-after-scroll,b2b-use-cases,home-meet-poolday}.mp4`, and `D7-page-review.md` (with a "Verified by the live screenshots" section).
- **Lesson:** when the BEFORE is a real screenshot, placeholders in the AFTER read as a downgrade. Reuse the real frames wherever nothing changes.

## M31. Poolday session progress (user-reported, with screenshots in `deliverables/assets/poolday-session/`)
- **Done:**
  - S1: skills saved. motion-craft (checklist pointer fixed) and ref-teaser, which now points to `guided-product-launch-video`, skips the missing 21st-dev connector instead of blocking, and accepts link or upload [to align rule 1].
  - S2: brand:wisprflow.
  - S3: brand:flam, specVersion 3, with animatable node cards, stat blocks, format tabs, model cards, 18 imagery assets and motion/sound guidelines. It warns that the perfume-bottle shots are another company's products.
  - S5: the Poolday kit compared with the Claude-made kit and enriched (a comparison report plus a single-file kit).
- **Flam question settled by Poolday's own research:** Flam is an AI-native interactive content format ("the internet beyond videos"). Its own models (Fable, Fantom, Falcon…) generate photoreal 3D/RGBA visuals and talking visual agents from a prompt, playable instantly with no app, with touch, voice and checkout. Formats: Flicks, Airboards (3D/AR), Visual Agents. The product UI has node cards, so the ImagineArt node-and-card reference fits.
- **API conversation:** the use-case question is still pending. Answer: "same video, new data each call".
- **Next:** the prospect videos, using `poolday/prompts/P1-wispr-flow-video.md` and `P2-flam-video.md`.

## M32. Real footage in all three style tiles
- **Workaround for blocked downloads:** YouTube, X, ssstwitter and ytmp3 are refused by this environment's network (organisation policy), and chat uploads of the two MP4s failed. The user uploaded them to the GitHub branch (Add file → Upload files) and Claude Code pulled them with git.
- **Apple Motion Style:** LangEase launch ad 0:06–0:18 (3D phones, progress bar, "Done"). **Storytelling Film:** Alex Whedon founder film 0:00–0:14 (lower third, "World's first fully subquadratic LLM", "12,000,000 tokens"). **Kinetic Typo:** "stretching creativity" 0:00–0:14.
- Converted with `tools/make-footage.sh` into deterministic image sequences. The result page keeps our own Northwind film, since showing another brand's video as "your video" would mislead.
- Stills and the 40s walkthrough re-rendered.

## M33. Poolday API is locked for the trial org
- Capabilities → Integrations shows "Integrations Not Enabled… Contact your administrator." The public API exists, per the agent, but has to be enabled by Poolday for this organisation. The brief itself hints at this ("if you don't know how to activate Poolday via API, write the prompt manually for now").
- **Plan:**
  1. Ask Poolday to enable API integrations for the org (message drafted).
  2. Meanwhile, test the lighter route the agent suggested: an **Automation with an inbound webhook**. The loop POSTs a lead's brief to the webhook URL, and a saved prompt runs it.
  3. The pipeline's Poolday client stays mapping-driven, so enabling the API later is a config fill, not a rewrite.
- Logged as product feedback: the agent offered "Create an API key" on a plan where the feature is locked.

## M34. Poolday webhook mode (the API is being deprecated, per Poolday's CEO)
- **CEO guidance:** use connectors, or have the agent create a webhook endpoint and call back a URL with the outputs. We chose the webhook, which is the closest to the loop's design.
- **Built:**
  - `WebhookPooldayClient` (POOLDAY_API=webhook) POSTs each lead (lead_id, token, version, company, website, brand kit, angle, contact, reference, prompt, callback_url) with a secret header.
  - `POST /api/poolday/callback` verifies the secret and the per-lead token, parses flexible payloads (envelopes, outputs lists, nested JSON, deep scan for video links; extra key paths configurable) and moves the lead to the human Review gate. Questions use the needs_input flow; stale versions and duplicates are ignored.
  - Through the tunnel, only the callback route is reachable. The dashboard, approve and export stay local.
  - CLI: `webhook-test`, `simulate-callback`, `callback-url`.
- **Tests:** 37 pass, including 21 webhook tests against a fake receiver that behaves the way the paste message asks Poolday's agent to.
- **Why a message to Poolday's agent instead of invented endpoints:** our field names are ours, and the agent is asked to accept them and echo lead_id, token and version on the callback. The first real callback's shape is checked in `api-log`, and new keys are added by config.
- **Runs on the user's Mac** (`loop/MAC-SETUP.md`): the cloud session can't reach poolday.ai, and a Cloudflare quick tunnel gives Poolday a public callback address.

## M35. Growth-tool mockups v4: the Poolday app's chrome
- **User request:** match the Poolday app UI (sidebar screenshot) and use the real logo.
- **Logo:** the palm-island mark cut from the user's app screenshot (thresholded to a white mark on transparent, `deliverables/design/poolday-app-ui/poolday-logo-mark.png`), next to the lowercase "poolday" wordmark as in the app. No official SVG is published (per Poolday's own kit comparison), so this is a faithful stand-in.
- **Chrome:** the app's near-black pills with a bright hairline edge (Continue, Generate video, Send me the video), grouped panels like the app's Workspace list (tabs, rail), a faint lavender glow top-left like the app sidebar. "Book a 15 min demo" stays the site's off-white CTA, as the one bright element.
- **Bug caught:** naming the button class "app" collided with the root `.app` container (buttons stretched full width). Renamed to `appbtn`.
- Stills and the walkthrough re-rendered.

## M36. Progress: first UGC reel posted; webhook lives in Automations
- **D4:** the first AI UGC reel is posted on the new IG account. Track views at +1h / +24h / +48h.
- **D3:** Poolday's CEO says the webhook is configured from the **Automations** tab. So the inbound URL, the secret and the saved prompt are set in the UI, not by asking the agent in chat. The loop's webhook client and callback stay the same: only where the URL comes from changes.

## M37. Automations webhook (the real UI) + video progress
- **Automations → New automation:** step 1, choose an Input (Schedule, **Webhook**, or 30+ vendor events such as PostHog, Supabase, Zapier, Airtable…); step 2, write the Prompt. For Webhook, the URL and secret appear after saving. Each run starts a fresh conversation (or one you pick).
- **Design choice:** the automation's prompt tells the agent to skip the ref-teaser approval step and decide itself, because our pipeline's dashboard is the human gate. Otherwise every automated run would stall waiting for someone. It calls our callback with lead_id, token, version and video_url. Prompt: `poolday/prompts/A1-automation-webhook.md`.
- **Videos:** Flam is finished. Wispr Flow v3 is delivered and asks whether to merge 3 new reusable pieces into brand:wisprflow (GmailCompose, VideoPlate, an outdoor living-portrait clip). Merging makes future Wispr teasers cheaper.
- **Skills:** ref-teaser now has an upload fallback when a link is too big to fetch (100 MB or 20 min YouTube cap). Approved with 0 blockers.

## M38. Automation form: concrete settings
- **What:** filled the Poolday Automations webhook form for the pipeline (`poolday/prompts/A1-automation-webhook.md`).
- **Decisions & why:**
  - **HMAC off.** Our pipeline authenticates with a shared secret header (X-Webhook-Secret) and a per-lead token, not an HMAC signature. With HMAC required, Poolday would reject every lead.
  - **No Output.** The prompt itself POSTs the result to callback_url.
  - **New conversation per lead.**
  - **Example event.** A sample lead JSON is pasted so "Insert event field" lists the fields. The prompt starts with a Lead block of inserted fields, so the agent sees the real values.
- **Mac script:** `start-mac.command` no longer asks the agent to build a webhook in chat. It copies the callback secret to the clipboard (to paste over `<SECRET>` in the automation prompt) and asks for the automation's URL. A new tunnel needs no Poolday change, because callback_url travels with each lead.
- **Lessons:** read the platform's auth options before choosing one. A "secure by default" checkbox (HMAC) can silently block a working client.
- **Correction after the user's screenshots:** "Insert event field" only offers `{{event.body}}`, `{{event.files}}`, `{{event.headers}}` and `{{event.query}}`, and "Example event" is a read-only preview. The prompt now inserts `{{event.body}}` (the whole lead JSON) once, instead of 13 per-field inserts. Also caught: the instruction text from the A1 file had been pasted into the prompt, so the prompt must contain only the fenced block.
- **Mac run 1 error:** "Homebrew is missing" although Homebrew was installed. Cause: on Apple Silicon, Homebrew lives in /opt/homebrew/bin, which isn't on the PATH until `brew shellenv` is added to ~/.zprofile (the installer's "Next steps", often skipped). Fix: `start-mac.command` now finds brew in /opt/homebrew or /usr/local, loads it, and adds it to ~/.zprofile once. The "No such file" sed message on the env file is harmless on a first run, because the script creates the file.

## M39. Two new LinkedIn angles: Jev launch demo + AI UGC studio
- **User request:** 2 viral posts about cool uses of Poolday, each built around a 15s sped-up demo made in Poolday: one with Jev, one "set up your AI UGC farm in 1 click".
- **Research:** web search (2026-09-26). Jev = TypeSafe AI's decision model (launched 15 Sep 2026, launch video ~40M views on X, >$10B valuation offers; Bloomberg 25 Sep). Jev appears in Poolday's "made with Poolday" gallery (b2b page). Detail pages were blocked (egress), so figures come from search snippets.
- **Decisions & why:**
  - Real screen recordings, sped up with a clock and a prompt counter, rather than an animated rebuild of the UI: proof holds up better against the "AI slop" button.
  - The Jev claim is gated on Poolday's confirmation, with a fallback copy.
  - "UGC studio" on LinkedIn, "farm" tested on X.
  - Mandatory AI disclosure on every reel.
- **Output:** `deliverables/D1-linkedin.md` §6; prompts `poolday/prompts/L2-jev-launch-demo.md`, `L3-ugc-studio-one-prompt.md` (2 runs each: make it, then cut the 15s demo).
- **Update (user's call):** the Jev angle was dropped. The UGC post was rewritten simple, with the user's best-performing headline format: "Claude Opus 5.5 + Poolday = Infinite UGC farm" (6 variants in D1 §6). The workflow is now Claude writes the scripts → Poolday makes the reels, so the headline is literally true without knowing Poolday's internal model. `L2-jev-launch-demo.md` was removed.
- **Update 2:** everything happens in Poolday (no Claude step). One Poolday prompt now makes the whole 15s video: Poolday animating its own UI building a UGC farm, with creative freedom and 2–3 directions first. The "Claude Opus 5.5 +" headline needs Poolday to confirm it runs Opus 5.5; the fallback is "1 prompt + Poolday = Infinite UGC farm".

## M40. D6 bonus: both review videos remade, on brand
- **User request:** remake the PostHog and Upflow videos to show motion-design skill, 100% on brand, with brand kits researched online.
- **Brand research:**
  - **PostHog:** posthog.com and upflow.io are blocked by egress, but github.com git clones work. `PostHog/posthog.com` (handbook → brand: visual identity, assets, colors) and `PostHog/brand` (official logo geometry, color tokens, RoundHog woff2, 171 hedgehog SVGs, the app's logomark-jump constants) were cloned. Squeak comes from the website repo's static fonts.
  - **Upflow:** the site and brand page are unreachable, so colors were sampled from their video (`#3936DC`, `#191A4C`, `#FAFAF7`). The wordmark was vectorized from the 1080p end card (potracer, 6× supersampled, the period split into its own path). The font was matched by rendering 13 Google fonts against the tagline; Figtree is closest.
- **Tools:** HTML/CSS + a small deterministic timeline engine (`remake/src/lib.js`: easings, springs, a CSS-bezier solver, seeded RNG) → Playwright seek-per-frame capture at 90 fps → ffmpeg `tmix` 3-frame motion blur → 30 fps H.264 CRF 16. `snap.js` makes contact sheets for review.
- **Decisions & why:**
  - **Upflow:** apply every fix from the review table (a hook in 1s, one card, the product payoff, proof as a hero card, a fast logo).
  - **PostHog:** follow its brand book literally: 2D hand-drawn hogs only, puppet-style entrances, the brand's "pressing-down" button, Squeak only uppercase next to hogs, charts labeled directly and annotated, synthetic data that tells a story (the handbook's 47-rage-clicks example), the official 2026 logo with the app's own jump (easing `cubic-bezier(.6,0,.2,.8)`, head first, stagger airtime/15), ending on a still frame.
- **Rights:** PostHog assets are under PolyForm Strict (view-only) and hogs need permission for marketing. The assets are kept out of the repo (`src/_assets` is git-ignored; `fetch-assets.sh` rebuilds it), and the video is labeled a private spec piece.
- **Output:** `deliverables/D6-video-review/remake/` (`upflow-remake.mp4`, `posthog-remake.mp4`, compare videos, `BRAND-KITS.md`, `README.md`).
- **Lessons:** when a brand's site is blocked, its GitHub is often the richest brand source (PostHog ships its whole brand as a package). A brand's own video is a usable color and logo source when nothing else is reachable.
- **v2 (user: "make it incredible and dynamic"):**
  - **Upflow:** rebuilt around Upflow's period as the hero: a caret macro pull-back; a CSS-3D swarm (perspective, dolly and orbit); an implosion into the brand dot; the dot floods the frame; the period of "simple." becomes a hole match-cut; the app swings in from a 38° tilt; the dot travels the payment timeline on the beat and stamps "Paid"; odometer reels; the dot lands as the logo's period.
  - **PostHog:** 24 chat windows popping on the beat; a button drop with squash, then shockwave and a rocket chase-cam; Squeak letters slamming with shake; 40 notes raining with rising tremble; whip-pans inside the app; the logomark landing part by part.
  - **Motion blur fix:** v1's 3-sample tmix left ghost copies on fast moves. Now 5 samples over a 180° shutter, captured by 4 parallel Playwright workers as JPEG (~2 min per video).
  - **Soundtrack:** `sound.py` (numpy, all synthesized: kick, hats, bass with sidechain, pads, whoosh, riser, impact, pops, clicks, keys, ding) from the page's `window.CUES`, normalized with loudnorm to −14 LUFS (the first mix was −9.8).
  - **Before/after:** `compare.sh` puts the original and the remake side by side. The local ffmpeg has no drawtext, so the labels are PIL PNG overlays.

## M41. Growth note: the "AI motion designer" trend
- **User input:** an X screenshot (@tdinh_me, 26 Sep: "paid ~$1,000+ for a video like this a year ago, made it with Opus 5.5 in <30 min", 4k views in 4h; a reply shares the prompt). The user wants this in the final doc: an easy growth lever is to post incredible motion-design videos, because that's the trend and it shows how strong AI motion design is.
- **Decision:** added to `DELIVERABLE.md` §D5 as a quick win. Format: before/after remakes of known brands plus the prompt, 2–3 a week. The D6 remakes are the proof of concept. Guardrails: name the model only if verified; get brand consent before publishing remakes.
- **Output:** `deliverables/DELIVERABLE.md` (D5 "Quick win"), `deliverables/assets/trend-opus-motion-design-tweet.png`.

## M42. Daily posting commitment + "Top 5 use cases" post
- **User input:** they'd post every day on X and LinkedIn about Poolday (it excites them). New idea: "Poolday just launched. Here are my top 5 use cases", with #1 the AI UGC farm (Poolday as a full media agent: incredible things, now easy).
- **Output:**
  - `DELIVERABLE.md`: a new section "My commitment: post about Poolday every day" (rotating formats, cadence, CTA to the lead loop, weekly tracking).
  - `D1-linkedin.md` §7: the listicle post (UGC farm, launch video from a URL, remake any video on brand, prospect videos on autopilot, $1,000 motion design), with a clip plan reusing D2–D6 material and a follow-up series.
- **Guardrail:** "just launched" only if there's a real launch moment.

## M43. Review notes after the remakes + the CEO's caption
- **User's verdicts, added to D6:**
  - Upflow: the original's hook is ~10s, far too long; the remake shows more examples and arguments in less time.
  - PostHog: 2D on-brand is more professional than 3D effects and modelling.
- **CEO post:** the user made the D1 video in Poolday ("Opus 5.5 + Poolday: Infinite UGC farm", 15s, a Poolday UI capture ×40: 50 creators, 50 scripts, a reels wall; the prompt bar's model picker shows "Claude Opus 5.5"). The caption is written in the CEO's voice (`D1-linkedin.md` §8). The model claim is supported by Poolday's own model picker. No real-time or volume claims, since the video is a dramatized ×40 capture. AI-label note in the first comment.

## M44. Cross-cutting finding: Poolday videos are too slow
- **User observation:** all three videos seen (the two review videos + a random post from the CEO's LinkedIn) have scenes that are too slow. The first 3s are wasted (on LinkedIn, just a blur clearing), while people scroll within ~3s.
- **Recorded in:** `DELIVERABLE.md` (top of D6), `PRODUCT-FEEDBACK.md` (high impact), `D6-video-review.md`.
- **Recommendation:** a default "social pacing" preset: meaningful content in frame 1, no blur or fade openers, average shot ≤1.2s, the hook stated by 2s. Evidence: the D6 side-by-side compares.
- The LinkedIn post itself wasn't viewable from this environment; this relies on the user's viewing.

## M45. Mac run 2: port 8765 taken by another server
- **Symptom:** localhost:8765 showed "Error response 404: No permission to list directory". That's Python's plain `http.server`, not our dashboard (ours never lists directories). A stray `python3 -m http.server 8765` was holding the port, so our dashboard couldn't start, and the tunnel would have sent Poolday's callbacks to the wrong server.
- **Fix:** `start-mac.command` now frees port 8765 before starting, waits until `/api/meta` answers (or prints the log and stops), and checks that the tunnel reaches the callback endpoint.
- **Security note:** the Poolday trigger token appeared in a user screenshot. Rotate it in Poolday after the test and update `POOLDAY_WEBHOOK_URL`.

## M46. First live Poolday run through the loop
- **Result:** the pipeline POSTed lead 1 (Wispr Flow) to the Automation webhook → `HTTP 202 {"accepted":1}` → Poolday ran it: it reused the v3 Wispr composition (its ref-teaser rule "a reference decomposed before is loaded, not redone") and rendered 22.4s 16:9 with audio (the video is on S3).
- **Blocker:** the automation's agent has **no outbound network**, so it couldn't POST the callback. It printed the exact callback JSON instead (lead_id, token, version, video_url, conversation_url). The `<SECRET>` placeholder had also not been replaced (irrelevant given no network).
- **Decision:** close the loop with a **human relay** at the validation step: paste Poolday's video link into the lead in the dashboard (field "2 · or paste the Poolday video link"), or run `simulate-callback --lead N --video URL`, which sends the same signed callback. This fits the brief ("if you don't know how to activate Poolday via API, write the prompt manually for now"), and the relay happens at the human gate anyway. Next: check whether the Automation's **Output** can POST (platform-side). Product feedback logged.

## M47. Loop run completed end to end + real email thumbnails
- **The user's run:** pasted Poolday's video URL at the human gate → Review → **Approve + draft email** → the draft appeared (screenshots saved in `deliverables/D3-loop/screenshots/`, excluding any that show the trigger token).
- **Q: how did it know "Carolyn"?** From the dataset: `data/series-b-bay-area.csv` lists "Carolyn [last masked], VP of Product Marketing" for Wispr Flow.
- **Q: how does `[VIDEO THUMBNAIL]` become a real thumbnail?** New in `pipeline.export`: `make_thumbnail()` downloads the video (stdlib urllib; the static ffmpeg segfaults on https in the sandbox) and builds a 3s, 480px, 12fps GIF with a play-button overlay (`assets/play.png`). `build_email_body()` writes plain text plus HTML, where the placeholder becomes `<a href=video><img src=cid:video-thumb></a>`, with the GIF inline (multipart/related). Without ffmpeg it falls back to a "▶ Watch the video" link. `start-mac.command` installs ffmpeg. Tests: 39 pass (2 new). Sample: `deliverables/D3-loop/wispr-flow-email-*`.
- **Output destinations:** connectors only, no webhook (confirmed in the UI), so the paste relay stays.

## M48. D8: Instagram ad remake, profile-picture fix, use-case series
- **Input:** a screenshot of Poolday's sponsored IG story (a static "No AI slop. Just your videos, edited well." card, monospace + cyan). The user noticed the IG logo is badly cropped and wants a series of short use-case motion videos.
- **Build:** `remake/src/poolday-ad.html`, 1080×1920, same engine. `capture.js` now reads `window.SIZE` for vertical formats and takes `OUT` for the output dir. Poolday's brand kit is followed: black ground, Inter 400, the halftone scan-dots (canvas, 4px/8px pitch), a charcoal end card with a slot-machine keyword and the iris rule that collapses to a dash. A fictional demo brand ("Lumen") avoids third-party rights. The Poolday mark was vectorized from the app screenshot (potracer).
- **Output:** `deliverables/D8-instagram/` (poolday-ad.mp4, profile-picture-proposal.png, README with 12 use-case ideas), and `DELIVERABLE.md` D8.
- **Update (user):** the ad must be **static**, a 9:16 split screen: greyed "slop/PowerPoint" attempt on top, the Poolday-made pro frame at the bottom (with the right Poolday logo), clearly built from a brand kit made from a URL. Built as `remake/src/poolday-static-ad.html` → Playwright screenshot at 2× → `D8-instagram/poolday-static-ad.png` (+ @2x). One layout pass fixed an overlap (copy vs CTA, arrow vs kit text).
- **Update 2 (user feedback: "the bottom looks slop"):**
  - Bottom enlarged to 58%; copy cut to two labels ("AI Slop" / "Made with Poolday").
  - The Poolday frame is now a rebuild of the user's Apple-motion reference (a 3D phone tunnel), rebranded to a fuller Lumen identity (Bricolage Grotesque display from Google Fonts + Inter; Moss/Ember/Sky/Night/Sand).
  - The brand kit is a 16:9 one-page brand guide (modelled on the user's "Picante" template screenshot), attached as "Inspiration attached".
- **Update 3 (user feedback on v2):**
  - The slop was "ok tier, not really bad": it's now the generic AI motion-design look (gradient, flare, "WORK SMARTER. GROW FASTER.", glass chart, wrong logo), all in grey. The top shrinks to ≈30% for the old-vs-new effect.
  - The brand kit is now smaller and superposed on the Poolday frame, tagged "built by AI from lumen.com", with a URL bar → arrow so the URL-to-kit mechanic is explicit.
  - Copy changed so the labels don't read "AI SLOP MADE WITH POOLDAY": "Other AI video tools" vs the Poolday logo, headline "Your URL in. Your brand out."
- **Update 4 (user):**
  - The top frame is now the user's "LOCAL AI SLOP" sign image, shown as a paused square video in grey.
  - The top label is bigger and darker (it was unreadable). The **VS** is a 210px medallion on a white seam.
  - The bottom label is the logo + "Made with Poolday".
  - The CTA line is removed.
  - Rights note: the sign is a third-party image; replace it before paid use.

## M49. Poolday time and credits (from the user's screenshots, 26 Sep evening)
- **Credits:** budget 2,000,000 ($2,000, so 1,000 credits = $1). Spent 835,270 (Settings → Usage, 30 days); balance 1,164,730. Top category Agents: 639,531 (77%). Daily: ≈25k (24 Sep), ≈400k (25 Sep, read from the chart), 409,800 (26 Sep, 328 events).
- **Time:** Poolday's agent estimated its own working time per conversation (the sum of timestamp gaps, idle gaps over 10 min excluded): 5h01m across 9 conversations. Heaviest: the D1 UGC-farm film (56m); lightest: the D3 webhook run (4m). Credits per conversation aren't visible to the agent.
- **Derived (labelled as estimates):** ≈2,800 credits per agent-minute on average. A first video with kit, skills and iterations is ≈140k credits (≈$140). The reused-kit webhook run is ≈11k (≈$11), which matches the site's "$5–25 per finished video".
- **Built:** 3 brand kits (Flam, Poolday, Wispr Flow), 2 org skills (motion-craft, ref-teaser), 10 memories, 1 webhook automation.
- **Output:** `DELIVERABLE.md` → "Time and credits" (table mapping conversations to deliverables); screenshots in `deliverables/assets/poolday-final/`. The time-report and usage screenshots weren't saved as files in this session, so their numbers were transcribed.

## M50. Real lead qualification and email, answered in Claude Code (process-leads)
- **Why:** the brief says "find new leads, qualify the lead… draft the email". On the Mac the dashboard ran in mock mode (rules + template), because there's no API key.
- **Process:**
  1. `/process-leads` flow on a separate cloud DB (`LOOP_DB=work/claude-run.db`, `LOOP_TODAY=2026-09-26`): ingest 38 fetched / 1 excluded / 37 added → the pre-score gate cut 10 → 27 qualify tasks.
  2. Each lead scored against the rubric, using only the dataset facts.
  3. Then the Wispr Flow approval was replicated (same S3 video) and its email written. It passes all the email rule checks.
- **Result:**
  - 5 qualified: Flam 99, TwelveLabs 79, Delightree 77, Blacksmith 77, Wispr Flow 76.
  - Close calls under 70: Foxglove 69, Flex/Convex/Vori 67.
  - Convex drops out (the mock had 73: the contact is a marketing manager and the product is a backend). Delightree comes in (HQ to verify: SF vs Denver).
- **Code:**
  - `llm-export --rescore` (re-asks mock-scored leads).
  - Tasks carry `domain`, and `llm-import` matches by domain, so an answer file made on one machine imports into another.
  - Leads already in production (in review, approved, exported, rejected, or with a Poolday run) keep their status, Poolday prompt and video when re-scored.
  - The dashboard header says "answered in Claude Code" once such leads exist.
  - New test; 40 pass.
- **Deviation from the skill:** `process-leads` says "don't commit / don't edit METHODS". Here the answers must reach the user's Mac, so only the answer file is committed (`loop/answers/claude-qualification-2026-09-26.json`, no database), and this entry follows CLAUDE.md.
- **Mac import:** `cd ~/poolday-trial && git pull && cd loop && python3 -m prospect_loop llm-import --file answers/claude-qualification-2026-09-26.json`, then refresh the dashboard. Dry-run on a simulated Mac database: Wispr stays approved with the new email; Convex out, Delightree in.

## M51. D4: first two reels live, early reach
- **Account:** @natecreates99 (professional; 8 followers, 45 following).
  - Reel 1, 26 Sep morning: https://www.instagram.com/reel/DdvmblCsJN1/ ("it did the $5K part from ONE link", laptop with the Poolday UI). At ~+12h: 0 views, 0 likes, average watch 9s.
  - Reel 2, 26 Sep 21:15: https://www.instagram.com/reel/DdwHhNmMUNj/ ("to the tech guy who told me… launch your startup from a URL", face reaction).
- **Read:** "0 views" alongside a 9s average watch means the stats aren't final. A new account's first reel is also throttled.
- **Diagnose before assuming a shadowban:** Profile → ☰ → Account status → whether content can be recommended to non-followers.
- **Changes for the next posts:** Trial reels if available (non-followers first); a face plus text hook in frame 1 (reel 2 has it, reel 1 opens on a laptop); IG library audio; follows slowed to ~10/day plus real niche activity; no delete-and-repost; the "AI info" label on; seed each reel to Story and DMs.
- **Plan:** post 2 more tomorrow (morning, evening) so n = 4 meets 3 < n < 20, a 5th if time allows. Read views at +12/+24h.
- **Output:** `DELIVERABLE.md` D4 table; screenshots in `deliverables/assets/d4/`.

## M52. How the qualification was done and checked (user question)
- **Method:** a code pre-score (freshness 40 / buyer 25 / B2B 15 / video fit 20, gate 45), then the 5×20 rubric answered per lead from dataset facts, with code guards (freshness from dates, sum, knockout without a buyer, threshold 70).
- **Coherence checks** computed on the 27 scored leads:
  - Spearman 0.83 against the pre-score, 0.71 against the mock scorer.
  - 4 of 5 qualified leads shared with the mock.
  - Consistent with the manual D2 picks (Flam, Wispr qualified; Blacksmith qualified; Convex a close call).
  - Only 2 leads differ by ≥10 points from the mock (Flex +15, Consensus −12), both explained.
- **Limits:** one rater, dataset only (no live verification), coarse criteria.
- **Validation plan:** outcomes by score band (5 qualified + 3–5 close calls as a control), re-weighting after 20–30 sends, a blind CEO scoring of 10 leads for agreement between raters, and an optional API second opinion.
- Written into `deliverables/D3-loop/README.md`.
- **Follow-up (user: "what does '4 of 5 are the same' mean?"):**
  - The fallback scorer (the mock: a fixed formula on the same fields, no AI) qualifies Flam 99, TwelveLabs 83, Blacksmith 79, Wispr Flow 73 and Convex 73.
  - The rubric qualifies Flam 99, TwelveLabs 79, Blacksmith 77, Delightree 77 and Wispr Flow 76.
  - Same first four; Delightree replaces Convex. The D3 README bullet now spells this out.
  - Recomputed on the cloud DB (`LOOP_DB=work/claude-run.db`, rebuilt by `ingest`):
    ```
    cd loop && python3 -c "import json;from prospect_loop import llm,store;c=store.connect('work/claude-run.db');a={t['domain']:t['result']['score'] for t in json.load(open('answers/claude-qualification-2026-09-26.json'))['tasks'] if t['task']=='qualify'};print(sorted(((llm.mock_qualify(l)['score'],a[l['domain']],l['company']) for l in store.all_leads(c) if l['domain'] in a),reverse=True)[:6])"
    ```

## M53. Final videos filed (D1, D2) and the 8-reel batch linked (D4)
- **What:** the user uploaded the three final Poolday videos to GitHub (web upload, repo root) and shared the Poolday link and a screenshot of the 8 UGC reels.
- **Tools:** git, ffmpeg (imageio-ffmpeg), PIL, the loop's email rule checks (`llm.clean_email`).
- **Inputs:**
  - Flam teaser: 25.1s, 1920×1080, 30 fps ("final (25 s 16:9)").
  - Wispr Flow teaser: 22.5s, 1920×1080 ("v3 — video plate + Gmail").
  - LinkedIn video: 15.1s, 1536×1920 ("Infinite UGC farm — A · Screen capture ×40 (no end card)").
  - The Poolday conversation "Poolday AI UGC Reels (8x)" (link) and a screenshot of its 8 reels.
- **Process:**
  1. `git mv` to `deliverables/D1-linkedin/infinite-ugc-farm.mp4` and `deliverables/D2-prospect-videos/{flam-series-b-teaser,wispr-flow-meetings-teaser}.mp4` (clean names, same blobs).
  2. Watched each at 1 frame/s (`ffmpeg -vf "fps=1,scale=480:-1,tile=5x5"`) → shot lists. 4-frame previews: `ffmpeg -ss T -i video -frames:v 1` per frame, then a PIL grid with time labels.
  3. Self-review of both prospect videos against my own D6 pacing rule (frame 1, the slowest stretch, the outro length).
  4. Flam email drafted from the loop's email guide and checked with `llm.clean_email`: all rules pass, 71 words.
  5. The 8-reel screenshot saved as `deliverables/assets/d4/poolday-ugc-reels-8x.jpg`. The Pletor screenshot (already in `assets/`) filled the appendix.
  6. Cleanup:
     - `D1-linkedin.md` had a stale duplicate of §5–§6 (the older "Claude writes, Poolday films" version, left by an earlier edit). Removed; §6 now has the UGC guardrails; §8 links the final file and suggests a cover frame.
     - In this file, the D8 ad updates 3 and 4 were moved back under M48 (they had been appended to M50 and M51).
- **Decision & why:**
  - Frame previews go in the docs because Markdown on GitHub doesn't play repo videos inline. The reader sees each video at a glance, then clicks through.
  - The self-review is there because the pacing critique I gave Poolday (D6) should apply to my own videos too.
- **User insight (logged in D4, the Pletor appendix, PRODUCT-FEEDBACK and the daily-post formats):**
  - "The AI creator turns the camera around and films the Poolday demo."
  - For Pletor, only the hook was AI, and the user filmed the demo by hand (iPhone pointed at the Mac). In Poolday, the whole reel comes out of one conversation. The user also found the agent "smart at every step" of the batch.
- **Output:**
  - `DELIVERABLE.md`:
    - D1 filled (video, caption, first comment, lead capture, honesty note, cover frame);
    - D2 (videos, previews, agent time, emails);
    - D4 (Poolday link, screenshot, the 8 hooks, what impressed);
    - TL;DR and key numbers;
    - the Pletor appendix.
  - Also: `D2-prospect-videos/README.md` and PRODUCT-FEEDBACK "What felt great".
- **Time/credits:** no Poolday credits (filing and review only).
- **Lessons:** GitHub web uploads land at the repo root with the original file names, so move them in one commit. A timestamped self-review is cheap and makes the critique of others credible.

## M54. Security housekeeping (user, 26 Sep evening)
- **What:** the user rotated the Poolday automation's webhook secret (the old trigger URL had been visible in a screenshot) and deleted the Anthropic API key pasted in chat earlier.
- **Process:** the scratchpad copy of the key was deleted; a grep over the repo and the scratchpad finds no copy.
- **Mac follow-up:** the loop saves the automation URL in `~/secrets/poolday-webhook.env`. After a rotation, delete the saved line and relaunch. The script then asks for the new URL:
  ```
  sed -i '' '/^POOLDAY_WEBHOOK_URL=/d' ~/secrets/poolday-webhook.env
  cd ~/poolday-trial && bash loop/start-mac.command
  ```
- **Decision & why:** anyone holding a leaked trigger URL can start Poolday runs on the account's credits. Rotation kills the old token. A key pasted in chat should be treated as exposed.

## M55. D4: third reel live; posting rule from the user's experience
- **What:** reel 3 posted on 26 Sep at about 21:40: https://www.instagram.com/reel/DdwK82gsVSt/.
  - Hook #7 of the batch, "when the founder wants a launch video "by Friday"" (the grey-haired creator).
  - Cover caption on the laptop shot: "done before lunch. from one URL".
  - Post caption: "it was so fast im genuinely shocked lol". IG library audio: Total Eclipse of the Heart (applies the M51 advice).
- **Inputs:** two phone screenshots, saved as `deliverables/assets/d4/profile-3-reels.png` (profile: 3 reels in the grid, 8 followers, 45 following; the post counter still read 2) and `reel3-by-friday.png`.
- **User rule:** "from my experience, a new account shouldn't post more than once a day" (read as "shouldn't"; the message said "should", which contradicts its first sentence). The user stopped at 3 on day 1 to avoid a shadowban. The DELIVERABLE posting-limit line now states this rule instead of "1–2 a day".
- **Count:** the brief says 3 < n < 20, so n = 3 is one short. Reel 4 goes up on 27 Sep.
- **Correction to M51:** the grid and the stats page show each reel's cover, which is the laptop shot, not frame 1. Reel 3 opens on a face (the screenshot of it playing), so reel 1 probably does too. Its frame-1 hook is marked "to confirm" (probably #3, the "$5K" one) instead of "opens on a laptop".
- **Output:** DELIVERABLE D4 (table rows 1–4, posting rule, format note); RUNBOOK G.


## M56. Full outside-eye review of every deliverable against the brief (27 Sep)
- **What:** reread every outward document (DELIVERABLE, D1–D8, PRODUCT-FEEDBACK) as a reader who knows nothing of the process, and checked each brief item and tip is answered.
- **Found and fixed:**
  - **Claims that never happened,** written at planning time: a skill-vs-threejs A/B test, a saved `/prospect-video` command with a "7 → 4 → 2" prompt curve, "all conversations in Align mode", Light/Max tiers. "How I worked" was rewritten from METHODS and the Poolday screenshots only (the real curve: ≈50 min and ≈$140 for a first video, 4 min and ≈$11 for a repeat via the webhook). The A/B is now listed as not done.
  - **D3 section was stale** ("no public API, a human pastes the prompt"). It now describes the live webhook run, the real numbers (37 → 10 cut → 27 scored → 5 qualified → 1 video in 4 min → approved → email), and the honest limit on "find new leads" (the RSS news source is built but not run live, and news leads lack a named buyer).
  - **D3 README contradiction:** the walkthrough listed Convex as qualified (the offline formula on the Mac) while the section below listed Delightree (the rubric). Now both are explained.
  - **D5 numbers contradicted each other:** the summary said "$3k pilot, ≤$150 per demo", while the write-up says $15k in 3 stages and ≈$380 per demo at 5%. The summary now follows the write-up.
  - **D5 write-up:**
    - it said credits were priced 1:1 in dollars (wrong: 1,000 credits = $1);
    - the cost table was empty (now measured: ≈$140–155 for a first video, ≈$11 for a repeat);
    - the mockup file names were broken;
    - the automation line was stale.
  - **D6:**
    - "Upflow reaches the product at 4s" corrected to 6s (the remake's shot list);
    - the remakes are now disclosed as built in code, not in Poolday;
    - the Poolday prompts are marked as not run;
    - a [verify] was resolved (github.com/PostHog/brand).
  - **D7:**
    - the brief's two pages now come first and pricing is marked as a bonus;
    - a one-paragraph "why each page loses demos" was added;
    - internal "round 3/4" wording was removed;
    - the comparison sheets were re-rendered with first-person subtitles (`src/render.js`; the renders themselves are unchanged).
  - **DELIVERABLE placeholders filled from existing work:** D3, D6, D7, the TL;DR, and "What I'd do with more time" (D8 row added).
  - **Wording:** "the user" → first person in outward docs. The D1 doc now opens on the final post. D4-ugc-scripts is marked as unused prep. The remake README says 5-sample motion blur (was 3).
- **Links:** every relative link in the deliverable docs resolves. The only exception is the git-ignored PostHog asset folder, which is intended.
- **Left for the user (placeholders):**
  - the submission date;
  - UGC views and reel 4;
  - money spent on other tools;
  - peak parallel Poolday conversations;
  - reel 1's frame-1 hook;
  - the Pletor farm's volume and results.

## M57. The final deliverable page (27 Sep)
- **What:** the version the user sends to the CEO. The user asked for outputs + TL;DR + details, written in the user's voice (simple words, "I worked with Claude Opus 5.5 & Poolday"), with every piece of media visible directly and without lag.
- **Tools:** HTML/CSS (a published claude.ai artifact, private until the user shares it), ffmpeg (imageio-ffmpeg), PIL, Playwright for one look at desktop and phone width.
- **User answers used:**
  - other tools: $200 (Claude Max);
  - up to 5 Poolday conversations at once (Flam, Wispr Flow, AI UGC, motion-craft skill, LinkedIn video) plus Claude;
  - reel 1's hook is the "$5K" one;
  - Pletor: keep it, but no volume or results;
  - only 3 reels posted, because of Instagram's anti-spam shadowban on new accounts that post more than once a day.
- **Process:**
  1. `deliverables/final/build_media.py` rebuilds light media from the originals:
     - 11 videos in H.264 (CRF 26–27, 720p or phone sizes, AAC 96k, +faststart), each with a JPEG poster;
     - 15 images as JPEG, at most 1600–1800px wide.
     - Total 16 MB.
     - The IG profile screenshot is cropped to drop the row of other people's suggested profiles.
  2. `deliverables/final/index.html`:
     - Poolday's own look: black ground, Inter 400, #161616 caption bars under each piece of media, the halftone behind the header, one iris rule. The colour comes from the videos.
     - Structure: Outputs (D1–D8, every video and image), TL;DR (one line per deliverable, 4 numbers, 3 lessons), Details.
     - Videos use `preload="none"` with a poster, so nothing loads until play, and only one plays at a time. Images are lazy-loaded with fixed sizes, and a click opens them full size.
  3. One render at 1440px and 390px: no horizontal scroll. The sticky nav hid section titles, so `scroll-margin-top` was added.
  4. Published as a private artifact, with the media as supporting files.
- **Output:**
  - The page: https://claude.ai/artifact/RWmrnGcJ4unei6jUPUT8GW.
  - The source (`final/index.html`, `final/build_media.py`) is in the repo. The media folder is git-ignored and rebuilt by the script.
  - `DELIVERABLE.md` is updated with the same answers and links to the page.
- **Left:** the reel view counts (marked "[views]" on the page), and sharing the page with the CEO from its Share menu.
