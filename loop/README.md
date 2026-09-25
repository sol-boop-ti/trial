# Prospect loop (D3)

Find leads → enrich → qualify → generate the Poolday prompt → **Poolday makes the video**
(through a Poolday webhook that calls us back with the video, the current recommended path;
or the older Poolday API client; or by copy/paste when neither is configured) → **human validation gate** (approve / reject / regenerate with a note,
which goes back to the same Poolday conversation) → personalized email draft → export `.eml`
+ CSV. The hiring manager sends the emails himself.

```
[Sources: CSV (primary) + funding-news stub] ──dedupe by domain, drop Higgsfield──▶
[Enrich: round date → days since, best buyer contact, segment/geo flags]
  ──▶ [Pre-score 0-100, deterministic]   (below 45: cut, no LLM call)
  ──▶ [LLM qualify 0-100 on the ICP rubric + justification + video angle]   (keep ≥ 70)
  ──▶ [Poolday prompt: /prospect-video command + fallback kickoff]
  ──▶ [Poolday webhook: POST the lead → Poolday's agent runs the flow → callback with the video URL
        or a question for the human]   (or the Poolday API + poller; or HUMAN copy/paste)
  ──▶ HUMAN GATE: approve · reject · regenerate with note (→ revision in the SAME conversation, v2, v3…)
  ──▶ [LLM email draft, editable]  ──▶  [Export: .eml drafts + CSV]  ──▶ sent by hand
```

## Setup

Python 3.9+. Mock mode and the dashboard use only the standard library.

```bash
cd loop
make demo          # whole loop end to end in the terminal, mock mode, ~1 second
make demo-api      # same, driving the local FAKE Poolday API: send, question, answer, revision (~15 s)
make test          # 37 tests (loop end to end, Poolday API client, webhook + callback against a fake receiver), no network
make seed serve    # fresh DB with qualified leads + dashboard on http://127.0.0.1:8765
make seed serve-fake   # same dashboard, "Send to Poolday" wired to the fake Poolday API
```

API mode (real qualification and email writing):

```bash
pip install -r requirements.txt
set -a; . ~/secrets/anthropic.env; set +a      # ANTHROPIC_API_KEY=... (never commit it; *.env is gitignored)
make seed serve
```

On a small budget, test on a few leads with a cheaper model id and a modest output cap first:

```bash
LLM_MODE=api CLAUDE_MODEL=<cheaper model id> LLM_MAX_TOKENS=1200 \
  python -m prospect_loop qualify --domain flamapp.ai --domain wisprflow.ai --limit 3
```

Every API call's token counts go in the lead's event log (`qualified:api … (in 1178 / out 147 tokens)`).

## Poolday via webhook (current recommended path)

Poolday says its public API is being deprecated. Instead, the Poolday agent creates an
**inbound webhook** that triggers a saved prompt, and when the conversation is done it
**POSTs the outputs to a URL of ours**. The loop does both halves:

```
Send to Poolday ──POST JSON (lead + prompt + callback_url + token)──▶ Poolday's inbound webhook
                                                                          │ agent runs the prospect-teaser flow
Review gate ◀── POST /api/poolday/callback (lead_id, token, status, video_url, conversation_url)
```

- `POOLDAY_API=webhook` selects `WebhookPooldayClient`. There is no polling: a lead's Poolday
  status changes only when Poolday calls back (or when you click **Mark done** and paste the link).
- **Our outbound payload** (JSON, header `X-Webhook-Secret: <secret>`): `kind` (`start`, `revision`
  or `answer`), `lead_id`, `token`, `version`, `company`, `website`, `brand_kit_name` (if known),
  `angle`, `contact_name`, `contact_role`, `reference_url`, `prompt` (the generated prompt text),
  `callback_url`. Follow-ups add `note` / `message` (regenerate) or `answer` / `question`.
- **The callback** `POST /api/poolday/callback` checks the shared secret (header, `Authorization:
  Bearer`, a `secret` body field, or `?secret=`), then the per-lead token (401 on a bad secret,
  403 on a bad token). It reads the payload flexibly: `lead_id` or just the `token`; `status`;
  the video under `video_url`, `url`, `outputs[].url`, `result.video`, `assets[]`… (image
  assets are skipped, `.mp4`/`.mov`/`.webm` links preferred); `conversation_url`; a `question`.
  Those values are also looked for inside `data`, `payload`, `body`, `result`… envelopes. A video
  moves the lead to **Review** and stops there (never auto-approved, never emailed). A question
  shows up on the lead like the API's needs-input flow, and your answer is POSTed back.
  A callback for an older `version` than the lead's current one is ignored.
- **Every callback is logged raw**, with secrets and tokens redacted, in the `api_calls` table
  (dashboard "Poolday API calls" panel, `python -m prospect_loop api-log`), rejected ones included.
- **Only the callback is public.** Through the tunnel (a non-local `Host` or forwarding headers)
  every other route returns 404: the dashboard and its buttons stay on your Mac.
- If Poolday's callback uses other key names, add them without code changes:
  `POOLDAY_CALLBACK_KEYS='{"video_url": ["deliverable.link"]}'`, or `[webhook.keys]` in
  `poolday_api.toml` (see `poolday_api.example.toml`). Static fields Poolday wants in every request:
  `POOLDAY_WEBHOOK_EXTRA='{"source": "prospect-loop"}'`.

### Set it up on your Mac (about 15 minutes)

1. **Tunnel.** In terminal 1, leave this running. It prints `https://<random>.trycloudflare.com`,
   which is free and needs no account. The URL changes every time you restart it.
   ```bash
   brew install cloudflared
   cloudflared tunnel --url http://localhost:8765
   ```
2. **Env file.** In terminal 2, create an env file outside the repo (`*.env` is gitignored anyway):
   ```bash
   mkdir -p ~/secrets
   cat > ~/secrets/poolday-webhook.env <<EOF
   POOLDAY_API=webhook
   PUBLIC_BASE_URL=https://<random>.trycloudflare.com
   POOLDAY_WEBHOOK_SECRET=$(openssl rand -hex 24)
   POOLDAY_WEBHOOK_SECRET_HEADER=X-Webhook-Secret
   REFERENCE_VIDEO=https://<your reference video link>
   POOLDAY_WEBHOOK_URL=
   EOF
   set -a; . ~/secrets/poolday-webhook.env; set +a
   cd <repo>/loop && python3 -m prospect_loop callback-url     # the URL to give Poolday
   echo "$POOLDAY_WEBHOOK_SECRET"                               # the secret to give Poolday
   ```
3. **Poolday conversation.** Open a new Poolday conversation, paste the message below with the
   callback URL and the secret filled in, and send it. Poolday's agent replies with the webhook URL.
4. **Webhook URL.** Put that URL in `POOLDAY_WEBHOOK_URL=` in the env file. If the agent says it
   uses another header name or its own secret, update `POOLDAY_WEBHOOK_SECRET_HEADER` /
   `POOLDAY_WEBHOOK_SECRET` to match.
5. **Dashboard.** Reload the env and start the dashboard. It must run with the same env as the CLI.
   ```bash
   set -a; . ~/secrets/poolday-webhook.env; set +a
   make seed serve        # first time (fresh DB); afterwards just `make serve`
   ```
   The dashboard is at http://127.0.0.1:8765, and **Send to Poolday** now posts to the webhook.

If the tunnel restarts, it gets a new URL. Update `PUBLIC_BASE_URL` and restart `make serve`.
Each request carries its own `callback_url`, so new leads use the new URL. A lead already in
flight still points at the old URL: use **Mark done** for it.

### The message to paste into Poolday

Replace `<CALLBACK_URL>` (from `callback-url`) and `<SECRET>` (from the env file) first.

```text
I want to trigger my prospect-teaser flow from my own app through a webhook, and get the result posted back to me. Please set this up.

1. Create an inbound webhook endpoint that triggers a saved prompt for this flow. Only accept requests whose header X-Webhook-Secret equals <SECRET>. Reply with the webhook URL.

2. Each request is a JSON POST with these fields. Accept all of them and ignore any you don't need:
   kind ("start", "revision" or "answer"), lead_id, token, version, company, website, brand_kit_name (may be missing), angle, contact_name, contact_role, reference_url, prompt, callback_url. Follow-ups also have note and message (revision), or answer and question (answer).

3. On kind "start": run the prospect-teaser flow for the website, with my ref-teaser skill and my motion-craft skill. Use the brand kit named brand_kit_name if it exists; otherwise build the brand kit from the website first. The reference video is reference_url. The angle is angle. The video is for contact_name (contact_role) at company. prompt holds the same brief as one text. 16:9.

4. On kind "revision": apply the note to the video you made for the same lead_id (in the same conversation if you can), then re-render. On kind "answer": it is my answer to your question for that lead_id, so continue.

5. When the video is done, POST JSON to the callback_url from the request (it is <CALLBACK_URL>), with the header X-Webhook-Secret: <SECRET> and this body:
   {"lead_id": <as received>, "token": "<as received>", "version": <as received>, "status": "completed", "video_url": "<shareable link to the final video>", "conversation_url": "<link to this conversation>"}
   Echo lead_id, token and version exactly as you received them.

6. If you need a decision from me before building, POST to the same callback_url with "status": "needs_input" and "question": "<your question>", then wait for an "answer" request. If the run fails, POST "status": "failed" and "error": "<why>".

7. If your webhook feature uses a different header name or generates its own secret, tell me the header name and value, and send that same header on the callback.
```

### Test it in 5 steps

1. **Offline.** `make test` runs everything against a local fake receiver that plays Poolday:
   send, callback, Review, bad secret, flexible payloads, question and answer, regenerate.
2. **Tunnel.** Check the tunnel. The first call should say `"ok": true`, the second is 401 (no
   secret), and the third is 404 (the dashboard is not public).
   ```bash
   curl -s $PUBLIC_BASE_URL/api/poolday/callback
   curl -s -X POST -H 'Content-Type: application/json' -d '{}' $PUBLIC_BASE_URL/api/poolday/callback
   curl -s -o /dev/null -w '%{http_code}
' $PUBLIC_BASE_URL/api/leads
   ```
3. **One lead to Poolday.** Run this with `make serve` running in another terminal with the same
   env. It prints Poolday's HTTP status and reply. Check that the run started in the Poolday
   conversation.
   ```bash
   python3 -m prospect_loop webhook-test --domain flamapp.ai [--brand-kit "Flam"]
   ```
4. **Rehearse the callback through the tunnel** (no credits):
   ```bash
   python3 -m prospect_loop simulate-callback --lead <id> --question "test: ignore" --base $PUBLIC_BASE_URL
   ```
   The question appears on the lead in the dashboard, and `python3 -m prospect_loop api-log <id>`
   shows a `callback … -> 200`.
5. **The real callback.** When Poolday posts back (runs take about an hour), the lead moves to
   **Review** with the video link. Click **Regenerate with note**. Poolday receives
   `kind: "revision"`, and v2 lands in Review. Then **Approve + draft email** as usual. If the
   lead doesn't move, open "Poolday API calls" on the lead: the raw callback is there (redacted).
   Add its key paths with `POOLDAY_CALLBACK_KEYS`, or use **Mark done**.

Locally, without the tunnel: `python3 -m prospect_loop simulate-callback --lead <id> --video https://example.com/v.mp4`
posts to http://127.0.0.1:8765. With `--direct` it runs in-process.

## Three ways to run the LLM steps

| Mode | When | How |
|---|---|---|
| **API** | `ANTHROPIC_API_KEY` is set (or `LLM_MODE=api`) | Anthropic Python SDK, JSON-schema structured output, server-side refusal fallback. Model from `CLAUDE_MODEL` (default in `prospect_loop/config.py`). |
| **Mock** | No key (or `LLM_MODE=mock`) | Deterministic, plausible output derived from the pre-score; justifications are prefixed `[mock]`. Lets you demo the whole flow offline. |
| **Claude Code** | No key, but you work inside Claude Code | Run `/process-leads` (`.claude/commands/process-leads.md`). The pipeline writes the pending prompts and schemas to `work/llm_tasks.json` (`make claude-tasks`), Claude Code answers them in the file, and `make claude-import` validates and stores the answers. Same rubric, same schema as API mode. |

## Configuration (environment variables)

| Variable | Default | Purpose |
|---|---|---|
| `LLM_MODE` | auto | `api` or `mock` (auto = api if a key is set) |
| `CLAUDE_MODEL` | see `config.py` | model id for API mode |
| `CLAUDE_EFFORT` | `medium` | `low` / `medium` / `high` |
| `QUALIFY_THRESHOLD` | `70` | keep leads scoring at least this |
| `PRESCORE_GATE` | `45` | below this pre-score, skip the LLM call |
| `LOOP_TODAY` | today | pin the date (`2026-09-24`) for reproducible freshness |
| `LLM_MAX_TOKENS` | `4000` | output cap per LLM call |
| `REFERENCE_VIDEO` | `<REFERENCE VIDEO LINK>` | goes into the Poolday prompts (the real API refuses to send while it's unset) |
| `POOLDAY_API` | auto | `webhook` (recommended: Poolday inbound webhook + our callback), `manual` (copy/paste), `fake` (local fake API), `http` (API via `poolday_api.toml`, being deprecated by Poolday). Auto = `webhook` when `POOLDAY_WEBHOOK_URL` is set, else `http` when that file and `POOLDAY_API_KEY` exist |
| `POOLDAY_WEBHOOK_URL` | – | Poolday's inbound webhook URL (the agent gives it to you) |
| `POOLDAY_WEBHOOK_SECRET` | – | shared secret, sent to Poolday and required on callbacks (env only). `POOLDAY_CALLBACK_SECRET` sets a different one for callbacks |
| `POOLDAY_WEBHOOK_SECRET_HEADER` | `X-Webhook-Secret` | header carrying the secret, both directions (`POOLDAY_WEBHOOK_SECRET_FIELD`, default `secret`, is the body-field alternative) |
| `PUBLIC_BASE_URL` | – | our public URL (the tunnel); the callback is `<PUBLIC_BASE_URL>/api/poolday/callback` |
| `POOLDAY_CALLBACK_KEYS`, `POOLDAY_WEBHOOK_EXTRA` | – | JSON: extra key paths to read in callbacks; static fields added to every outbound payload |
| `POOLDAY_WEBHOOK_TIMEOUT_S` | `30` | timeout of the POST to Poolday |
| `POOLDAY_API_KEY` | – | Poolday API key (env only) |
| `POOLDAY_API_CONFIG` | `poolday_api.toml` | the endpoint/field mapping filled from the docs ([POOLDAY_API.md](POOLDAY_API.md)) |
| `POOLDAY_PROMPT` | `command` | what "Send" submits: `command` (`/prospect-video`) or `fallback` (kickoff + skill file attached) |
| `POOLDAY_MODE`, `POOLDAY_TIER` | mapping defaults (`align`, `standard`) | override mode / tier per run |
| `POOLDAY_POLL_S` | `5` | dashboard background poller interval (use 30-60 for real runs) |
| `POOLDAY_FAKE_URL`, `FAKE_POOLDAY_STEP_S` | in-process, `2` | fake API location and seconds per simulated phase |
| `SENDER_NAME`, `SENDER_EMAIL` | placeholders | email signature and `From:` |
| `LEADS_CSV`, `LOOP_DB`, `LOOP_OUT` | `../data/…csv`, `work/leads.db`, `out/` | paths |
| `FUNDING_FEEDS` | empty | comma-separated RSS URLs for the funding-news source |

## How each step works

**Sources** (`sources.py`). `CsvSource` reads `data/series-b-bay-area.csv`. `FundingNewsSource`
is a working stub: it parses RSS items like "X raises $40M Series B" but needs a domain resolver
(search API or an LLM with web search) before it can feed real leads, because dedupe is by
domain. To add a source: subclass `LeadSource`, implement `fetch()`, add it to `SOURCES`, run
`python -m prospect_loop ingest --source csv --source <name>`. Re-ingesting never overwrites
a lead that is already in review.

**Pre-score** (`enrich.py`, no LLM): freshness 40 (≤14 days = 40 … >1 year = 0) + named buyer 25
(CMO / creative / product marketing > growth / demand > other) + B2B 15 (halved on the CSV's
segment flag) + video fit 20 (keywords in "what they do").

**Qualification** (`llm.py`): five criteria, 0-20 each: B2B, freshness, named buyer, visual
product, video need. The call returns a 2-3 sentence justification, a short video angle (10
words max, since it goes verbatim into the Poolday prompt), the launch hook for the email, and
the audience. The rubric text is `ICP_RUBRIC` in `llm.py`. Three things are enforced in code, not
left to the model: freshness points come from the rubric's day bands, the total is the sum of
the five criteria, and a lead with **no named buyer is knocked out** whatever its score (there
is nobody to send the video to).

**Poolday prompt** (`poolday.py`). Intent-level only, because Poolday's agent decides the edit.
- `/prospect-video <url> ref: <reference>` + one line of angle and audience (once the command is
  saved in Poolday after prospect video #1).
- Fallback kickoff until then: drop the Reference Teaser skill file, reference link, brand URL,
  "what I love in the reference", objective + audience, "you have creative freedom".
- Regenerate turns the reviewer's note into a revision prompt for the **same** Poolday
  conversation, and the lead waits for the v2 link.

**Poolday API** (`poolday_api.py`, [POOLDAY_API.md](POOLDAY_API.md)). One `PooldayClient` interface
(start a production, send a follow-up, poll status, answer the agent's question, fetch the
result, credits) with four implementations: `WebhookPooldayClient` (the recommended path, see
"Poolday via webhook" above: POSTs to Poolday's inbound webhook, status arrives by callback, no
poller), `HttpPooldayClient` (every URL, header, path and field comes from `poolday_api.toml`,
still a template; Poolday is deprecating its public API), `FakePooldayClient` (the same HTTP
client against the local fake server in `poolday_fake.py`), and `ManualPooldayClient`
(copy/paste). With the API client configured:
- **Send to Poolday** submits the prompt (Align mode, Standard tier by default).
- A background poller in the dashboard server updates the status every `POOLDAY_POLL_S` seconds.
- When the agent asks a question, it shows up on the lead for the human to answer.
- The finished video link lands in the **Review** gate automatically, and stops there.
- **Regenerate with note** posts the revision to the same conversation.
- Every HTTP call goes to the `api_calls` table (shown per lead in the dashboard, and in
  `prospect_loop api-log`). Status changes go to the event log.

**Human gate** (`server.py` + `dashboard.html`, stdlib `http.server`). State lives in SQLite
(`work/leads.db`), with an event log of every decision (who did what, when, which note).
Lifecycle: `new → qualified (awaiting video) → in_review → approved → exported`, plus
`rejected`, `disqualified`, and `in_review → qualified` on regenerate.

**Email** (`llm.py`): 60-110 words. It covers the round, their launch hook, and the contact's
role, names Poolday once, then a `[VIDEO THUMBNAIL]` line, the video link, and one yes/no
question. The guide's hard rules are checked in code (`email_checks`: word count, greeting,
thumbnail line followed by the link, exactly one question mark, round amount, Poolday named,
sign-off, no AI model/vendor names, subject length). In API mode a failing draft gets one repair
call with the list of broken rules, and anything still failing is shown to the reviewer. The
draft stays editable in the dashboard (edits are re-checked).

**Export** (`pipeline.export`): `out/emails/<company>.eml` (opens as an unsent draft; `To:` is
blank because the CSV has no addresses) and `out/email_drafts.csv`. Gmail drafts:
`export_gmail_drafts()` is a documented stub (OAuth + `gmail.compose`, not implemented).

## CLI

```bash
python -m prospect_loop run                       # ingest + qualify
python -m prospect_loop list [--status in_review]
python -m prospect_loop show 17                   # full JSON + event log
python -m prospect_loop video 17 https://…        # paste back the Poolday link
python -m prospect_loop approve|reject|regenerate 17 --note "hard cut at 0:04"
python -m prospect_loop export
python -m prospect_loop qualify --limit 3 --domain flamapp.ai   # cap LLM calls on a small budget

# Poolday API (POOLDAY_API=fake|http)
python -m prospect_loop poolday-status             # which client, TODOs left in the mapping, credits
python -m prospect_loop send 17 [--prompt fallback] # start the production (or send a pending revision)
python -m prospect_loop poll --watch               # poll until nothing is running
python -m prospect_loop answer 17 "Go ahead"       # answer the agent's question
python -m prospect_loop api-log [17]               # every Poolday HTTP call
python -m prospect_loop fake-poolday --port 8766   # the local fake Poolday API

# Poolday webhook (POOLDAY_API=webhook)
python -m prospect_loop callback-url               # the URL to give Poolday
python -m prospect_loop webhook-test --domain flamapp.ai [--brand-kit NAME] [--force]   # send one lead
python -m prospect_loop simulate-callback --lead 17 --video https://… [--base URL | --direct]   # play Poolday
python -m prospect_loop simulate-callback --lead 17 --question "15s or 20s?"
```

## 2-minute demo script (screen recording)

Before recording, run `make seed serve`, open http://127.0.0.1:8765, and have one real Poolday
video link ready (for example the finished Flam prospect video).

| Time | Show | Say |
|---|---|---|
| 0:00 | The diagram at the top of this README | "Leads in, a validated personalized video email out. One human checkpoint, where it matters." |
| 0:10 | Dashboard, **Disqualified** tab: click Arcee AI, then a pre-score cut | "37 companies from the Series B list, Higgsfield excluded, deduped by domain. Cheap deterministic pre-score first, then the LLM scores the rest against the ICP rubric. Arcee raised 8 days ago but there's no named buyer, so it's out." |
| 0:30 | **Awaiting video** tab: click Flam | "Flam: $40M Series B 10 days ago, CMO and Creative Director named. Here are the rubric, the justification and the angle: 'your Series B announcement film'." |
| 0:45 | Click **Copy** on the `/prospect-video` prompt, switch to Poolday, paste | "In copy/paste mode the loop writes a 2-line intent-level prompt using the command we saved after the first video. Poolday's agent does the creative work." |
| 1:00 | Paste the video link and click **Send to review** | "Human pastes the link back." |
| 1:05 | Type "hard cut at 0:04, hold logo 2 frames longer" and click **Regenerate** | "The gate: if it's not good enough, I direct with mechanisms. That becomes a revision prompt for the same conversation, and the lead goes back to v2." |
| 1:20 | Paste the v2 link, click **Approve + draft email** | "Approve, and it drafts the email: the round, their moment, the contact's role, the video, one question." |
| 1:35 | Edit one word in the email, **Save**, then **Export approved drafts**, and open `out/emails/flam.eml` | "Editable, then exported as ready-to-send drafts plus a CSV. The hiring manager sends them." |
| 1:50 | History panel | "Every decision is logged. Next steps: the Poolday API or a browser agent for the paste step, and Gmail drafts." |

**API variant** (`make seed serve-fake` now; `POOLDAY_API=http make seed serve` once the mapping is
filled). Replace 0:45-1:20 with:

| Time | Show | Say |
|---|---|---|
| 0:45 | Click **Send to Poolday** on Flam; the status chip goes queued → running | "The loop submits the prompt to Poolday through the API and polls it in the background." |
| 0:55 | The agent's question appears; type "Go ahead" and click **Answer** | "Align mode: Poolday's agent asks one question at its gate, and the human answers from here." |
| 1:05 | The lead moves to **Review** by itself, with the video link | "The finished video lands in the validation gate. It never goes further without a human." |
| 1:10 | Regenerate with a note; the chip goes back to running, then v2 lands in Review | "The note goes to the same Poolday conversation as a revision." |
| 1:20 | Open **Poolday API calls** under the lead | "Every API call is logged: that's the audit trail for the method write-up." |

## Files

```
loop/
  prospect_loop/
    config.py      env config, model id, thresholds, exclusions
    sources.py     LeadSource, CsvSource, FundingNewsSource (stub), dedupe
    enrich.py      enrichment + deterministic pre-score (+ optional site fetch)
    llm.py         ICP rubric, email guide, schemas; API / mock implementations
    poolday.py     /prospect-video, fallback kickoff, revision prompts
    poolday_api.py PooldayClient interface; webhook, HTTP (mapping-driven), fake, manual clients;
                   callback parsing (parse_callback) and redaction
    poolday_fake.py local fake Poolday API server (tests + demos; NOT Poolday's real API)
    pipeline.py    steps + human-gate actions + export + Claude Code task files
    store.py       SQLite state + event log
    server.py      dashboard HTTP server (stdlib)
    dashboard.html single-page review UI
    __main__.py    CLI
  tests/test_e2e.py  tests/test_poolday_api.py  tests/test_webhook.py (fake Poolday receiver)
  scripts/demo.sh    scripts/demo_poolday_api.sh
  poolday_api.example.toml   the mapping template: FILL FROM POOLDAY API DOCS
  POOLDAY_API.md             what we need from the docs, and how to fill the mapping
  Makefile  requirements.txt
../.claude/commands/process-leads.md   Claude Code mode
```

## Known limitations

- Webhook mode is built against a local fake receiver; the payload shapes Poolday's agent will
  actually send are unknown until the first real run, which is why the callback parser is
  permissive and configurable. Check the first real callback in the API log. The quick tunnel URL
  changes on every restart (a named Cloudflare tunnel fixes that, but needs an account and a domain).
- The Poolday API mapping (`http` mode, being deprecated per Poolday) is still a template: it runs
  only against the local fake server. The paste-back link is only checked for being a URL.
- The CSV has no email addresses, so `To:` is blank in exports. Finding addresses is a manual step.
- Enrichment is mostly what the CSV already holds. `--fetch-sites` adds the homepage title and
  description on a best-effort basis. There's no live funding feed until a domain resolver is
  plugged into `FundingNewsSource`.
- Mock mode has fixed wording, and it doesn't apply the reviewer's note to a redraft (it only
  shows the note).
- The dashboard is local and single-user, with no auth. Keep it on 127.0.0.1. Through a tunnel,
  only `/api/poolday/callback` answers (secret + per-lead token); everything else is 404.
