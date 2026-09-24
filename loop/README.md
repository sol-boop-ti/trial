# Prospect loop (D3)

Find leads → enrich → qualify → generate the Poolday prompt → **Poolday makes the video**
(through the Poolday API: send, poll, answer the agent's question; or by copy/paste when no
API is configured) → **human validation gate** (approve / reject / regenerate with a note,
which goes back to the same Poolday conversation) → personalized email draft → export `.eml`
+ CSV. The hiring manager sends the emails himself.

```
[Sources: CSV (primary) + funding-news stub] ──dedupe by domain, drop Higgsfield──▶
[Enrich: round date → days since, best buyer contact, segment/geo flags]
  ──▶ [Pre-score 0-100, deterministic]   (below 45: cut, no LLM call)
  ──▶ [LLM qualify 0-100 on the ICP rubric + justification + video angle]   (keep ≥ 70)
  ──▶ [Poolday prompt: /prospect-video command + fallback kickoff]
  ──▶ [Poolday API: start conversation → poller → agent's question shown to the human → video URL]
        (or HUMAN copy/paste when POOLDAY_API=manual)
  ──▶ HUMAN GATE: approve · reject · regenerate with note (→ revision in the SAME conversation, v2, v3…)
  ──▶ [LLM email draft, editable]  ──▶  [Export: .eml drafts + CSV]  ──▶ sent by hand
```

## Setup

Python 3.9+. Mock mode and the dashboard use only the standard library.

```bash
cd loop
make demo          # whole loop end to end in the terminal, mock mode, ~1 second
make demo-api      # same, driving the local FAKE Poolday API: send, question, answer, revision (~15 s)
make test          # 16 tests (loop end to end + Poolday client against the fake server), no network
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
| `POOLDAY_API` | auto | `manual` (copy/paste), `fake` (local fake API), `http` (real API via `poolday_api.toml`). Auto = `http` when that file and `POOLDAY_API_KEY` exist |
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
result, credits) with three implementations: `HttpPooldayClient` (every URL, header, path and
field comes from `poolday_api.toml`, which is still a template until we have the docs),
`FakePooldayClient` (the same HTTP client against the local fake server in `poolday_fake.py`),
and `ManualPooldayClient` (copy/paste). With an API configured:
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
    poolday_api.py PooldayClient interface; HTTP (mapping-driven), fake, manual clients
    poolday_fake.py local fake Poolday API server (tests + demos; NOT Poolday's real API)
    pipeline.py    steps + human-gate actions + export + Claude Code task files
    store.py       SQLite state + event log
    server.py      dashboard HTTP server (stdlib)
    dashboard.html single-page review UI
    __main__.py    CLI
  tests/test_e2e.py  tests/test_poolday_api.py
  scripts/demo.sh    scripts/demo_poolday_api.sh
  poolday_api.example.toml   the mapping template: FILL FROM POOLDAY API DOCS
  POOLDAY_API.md             what we need from the docs, and how to fill the mapping
  Makefile  requirements.txt
../.claude/commands/process-leads.md   Claude Code mode
```

## Known limitations

- The Poolday API mapping is a template until we have the docs: today the API path runs only
  against the local fake server, and the real step is copy/paste. The paste-back link is only
  checked for being a URL. There are no webhooks yet: the dashboard polls.
- The CSV has no email addresses, so `To:` is blank in exports. Finding addresses is a manual step.
- Enrichment is mostly what the CSV already holds. `--fetch-sites` adds the homepage title and
  description on a best-effort basis. There's no live funding feed until a domain resolver is
  plugged into `FundingNewsSource`.
- Mock mode has fixed wording, and it doesn't apply the reviewer's note to a redraft (it only
  shows the note).
- The dashboard is local and single-user, with no auth. Keep it on 127.0.0.1.
