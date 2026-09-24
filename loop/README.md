# Prospect loop (D3)

Find leads → enrich → qualify → generate the Poolday prompt → **human** makes the video in
Poolday and pastes the link back → **human validation gate** (approve / reject / regenerate
with a note) → personalized email draft → export `.eml` + CSV. The hiring manager sends the
emails himself.

```
[Sources: CSV (primary) + funding-news stub] ──dedupe by domain, drop Higgsfield──▶
[Enrich: round date → days since, best buyer contact, segment/geo flags]
  ──▶ [Pre-score 0-100, deterministic]   (below 45: cut, no LLM call)
  ──▶ [LLM qualify 0-100 on the ICP rubric + justification + video angle]   (keep ≥ 70)
  ──▶ [Poolday prompt: /prospect-video command + fallback kickoff]
  ──▶ HUMAN pastes it into Poolday, pastes the video link back    (no public Poolday API)
  ──▶ HUMAN GATE: approve · reject · regenerate with note (→ revision prompt, v2, v3…)
  ──▶ [LLM email draft, editable]  ──▶  [Export: .eml drafts + CSV]  ──▶ sent by hand
```

## Setup

Python 3.9+. Mock mode and the dashboard use only the standard library.

```bash
cd loop
make demo          # whole loop end to end in the terminal, mock mode, ~1 second
make test          # 5 end-to-end tests, mock mode
make seed serve    # fresh DB with qualified leads + dashboard on http://127.0.0.1:8765
```

API mode (real qualification and email writing):

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
make seed serve
```

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
| `REFERENCE_VIDEO` | `<REFERENCE VIDEO LINK>` | goes into the Poolday prompts |
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
product, video need. The call returns a 2-3 sentence justification, a short video angle, the
launch hook for the email, and the audience. The rubric text is `ICP_RUBRIC` in `llm.py`.

**Poolday prompt** (`poolday.py`). Intent-level only, because Poolday's agent decides the edit.
- `/prospect-video <url> ref: <reference>` + one line of angle and audience (once the command is
  saved in Poolday after prospect video #1).
- Fallback kickoff until then: drop the Reference Teaser skill file, reference link, brand URL,
  "what I love in the reference", objective + audience, "you have creative freedom".
- Regenerate turns the reviewer's note into a revision prompt for the **same** Poolday
  conversation, and the lead waits for the v2 link.

**Human gate** (`server.py` + `dashboard.html`, stdlib `http.server`). State lives in SQLite
(`work/leads.db`), with an event log of every decision (who did what, when, which note).
Lifecycle: `new → qualified (awaiting video) → in_review → approved → exported`, plus
`rejected`, `disqualified`, and `in_review → qualified` on regenerate.

**Email** (`llm.py`): 60-110 words. It covers the round, their launch hook, and the contact's
role, then a `[VIDEO THUMBNAIL]` line, the video link, and one yes/no question. The draft
stays editable in the dashboard.

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
```

## 2-minute demo script (screen recording)

Before recording, run `make seed serve`, open http://127.0.0.1:8765, and have one real Poolday
video link ready (for example the finished Flam prospect video).

| Time | Show | Say |
|---|---|---|
| 0:00 | The diagram at the top of this README | "Leads in, a validated personalized video email out. One human checkpoint, where it matters." |
| 0:10 | Dashboard, **Disqualified** tab: click Arcee AI, then a pre-score cut | "37 companies from the Series B list, Higgsfield excluded, deduped by domain. Cheap deterministic pre-score first, then the LLM scores the rest against the ICP rubric. Arcee raised 8 days ago but there's no named buyer, so it's out." |
| 0:30 | **Awaiting video** tab: click Flam | "Flam: $40M Series B 10 days ago, CMO and Creative Director named. Here are the rubric, the justification and the angle: 'your Series B announcement film'." |
| 0:45 | Click **Copy** on the `/prospect-video` prompt, switch to Poolday, paste | "Poolday has no public API yet, so the loop writes a 2-line intent-level prompt using the command we saved after the first video. Poolday's agent does the creative work." |
| 1:00 | Paste the video link and click **Send to review** | "Human pastes the link back." |
| 1:05 | Type "hard cut at 0:04, hold logo 2 frames longer" and click **Regenerate** | "The gate: if it's not good enough, I direct with mechanisms. That becomes a revision prompt for the same conversation, and the lead goes back to v2." |
| 1:20 | Paste the v2 link, click **Approve + draft email** | "Approve, and it drafts the email: the round, their moment, the contact's role, the video, one question." |
| 1:35 | Edit one word in the email, **Save**, then **Export approved drafts**, and open `out/emails/flam.eml` | "Editable, then exported as ready-to-send drafts plus a CSV. The hiring manager sends them." |
| 1:50 | History panel | "Every decision is logged. Next steps: the Poolday API or a browser agent for the paste step, and Gmail drafts." |

## Files

```
loop/
  prospect_loop/
    config.py      env config, model id, thresholds, exclusions
    sources.py     LeadSource, CsvSource, FundingNewsSource (stub), dedupe
    enrich.py      enrichment + deterministic pre-score (+ optional site fetch)
    llm.py         ICP rubric, email guide, schemas; API / mock implementations
    poolday.py     /prospect-video, fallback kickoff, revision prompts
    pipeline.py    steps + human-gate actions + export + Claude Code task files
    store.py       SQLite state + event log
    server.py      dashboard HTTP server (stdlib)
    dashboard.html single-page review UI
    __main__.py    CLI
  tests/test_e2e.py
  scripts/demo.sh
  Makefile  requirements.txt
../.claude/commands/process-leads.md   Claude Code mode
```

## Known limitations

- The Poolday step is manual (no public API). The paste-back link is only checked for being a URL.
- The CSV has no email addresses, so `To:` is blank in exports. Finding addresses is a manual step.
- Enrichment is mostly what the CSV already holds. `--fetch-sites` adds the homepage title and
  description on a best-effort basis. There's no live funding feed until a domain resolver is
  plugged into `FundingNewsSource`.
- Mock mode has fixed wording, and it doesn't apply the reviewer's note to a redraft (it only
  shows the note).
- The dashboard is local and single-user, with no auth. Keep it on 127.0.0.1.
