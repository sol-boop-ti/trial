---
description: Run the prospect loop with Claude Code doing the LLM steps (no API key needed)
argument-hint: "[--fetch-sites]"
---

You are running the Poolday prospect loop in `loop/`. The Python pipeline does the
deterministic work (sourcing, dedupe, pre-score, Poolday prompts, storage, export). You do
the two LLM steps yourself instead of an API call: **qualification** and **email drafting**.

Work from the `loop/` directory. Set `LLM_MODE=mock` for every command so nothing tries to
call the API.

1. **Find + enrich leads.**
   `LLM_MODE=mock python3 -m prospect_loop ingest $ARGUMENTS`
   Report the ingest stats (fetched / excluded / duplicates / added).

2. **Export the pending LLM tasks.**
   `LLM_MODE=mock python3 -m prospect_loop llm-export`
   This writes `loop/work/llm_tasks.json`. Each task has `system` (the rubric or the email
   guide), `prompt` (the lead's facts), `schema` (the JSON shape) and `result: null`.

3. **Do the LLM work.** Read the file. For every task, follow its `system` text exactly and
   write the answer into `result` as a JSON object that matches `schema`:
   - `qualify` tasks: score each rubric criterion 0-20, `score` = their sum, a 2-3 sentence
     `justification` citing the facts, a short intent-level `video_angle` (it goes straight into
     the Poolday prompt, so keep it under ~10 words), `launch_hook`, `audience` (a role).
   - `email` tasks: `subject` + `body` following the email guide (60-110 words, `[VIDEO THUMBNAIL]`
     line, the video link, one yes/no question, first name only).
   Use only the facts in the task. Do not invent launches, customers or metrics. Never name AI
   models in any output. Save the file.

4. **Import the answers.**
   `LLM_MODE=mock python3 -m prospect_loop llm-import`
   Then `LLM_MODE=mock python3 -m prospect_loop list --status qualified`.

5. **Hand over to the human.** Show a short table of the qualified leads (score, company, one-line
   angle) and the `/prospect-video` prompt of the top lead
   (`python3 -m prospect_loop show <id>` → `poolday_prompts.command`). Then tell the user:
   `cd loop && make serve` → open http://127.0.0.1:8765 → copy the prompt into Poolday, paste the
   video link back, approve / reject / regenerate. After they approve leads, running
   `/process-leads` again redrafts those emails (step 3, `email` tasks) with your own writing
   instead of the mock template. Finally, "Export approved drafts" writes `.eml` files and a CSV.

Do not send any email, do not edit `METHODS.md`, `RUNBOOK.md` or `PLAN.md`, and do not commit.
