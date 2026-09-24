"""CLI:  python -m prospect_loop <command>   (run from the loop/ directory)"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import config, pipeline, poolday_api, store


def _print_table(leads):
    print(f"{'id':>3}  {'score':>5}  {'status':<12} company")
    for l in leads:
        print(f"{l['id']:>3}  {l.get('score') if l.get('score') is not None else '-':>5}  "
              f"{l['status']:<12} {l['company']}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="prospect_loop", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ingest", help="find + enrich leads (dedupe by domain)")
    s.add_argument("--source", action="append", choices=["csv", "funding_news"],
                   help="repeatable; default csv")
    s.add_argument("--fetch-sites", action="store_true", help="pull homepage title/description")
    for name, hlp in (("qualify", "pre-score + LLM score, generate Poolday prompts"),
                      ("run", "ingest + qualify")):
        s = sub.add_parser(name, help=hlp)
        s.add_argument("--rescore", action="store_true", help="also re-run disqualified leads")
        s.add_argument("--limit", type=int, help="at most N LLM calls (highest pre-score first)")
        s.add_argument("--domain", action="append", help="only these domains (repeatable)")
    s = sub.add_parser("list", help="show leads")
    s.add_argument("--status", choices=store.STATUSES)
    s = sub.add_parser("show", help="full detail for one lead")
    s.add_argument("id", type=int)
    s = sub.add_parser("video", help="paste back the Poolday video link")
    s.add_argument("id", type=int)
    s.add_argument("url")
    for name in ("approve", "reject", "regenerate"):
        s = sub.add_parser(name, help=f"human gate: {name}")
        s.add_argument("id", type=int)
        s.add_argument("--note", default="")
    s = sub.add_parser("send", help="Poolday API: submit the prompt (or the pending revision)")
    s.add_argument("id", type=int)
    s.add_argument("--prompt", choices=["command", "fallback"], help="default: POOLDAY_PROMPT")
    s = sub.add_parser("answer", help="Poolday API: answer the agent's question")
    s.add_argument("id", type=int)
    s.add_argument("text")
    s = sub.add_parser("poll", help="Poolday API: poll productions in flight")
    s.add_argument("--watch", action="store_true", help="keep polling until nothing is running")
    s.add_argument("--interval", type=float, default=config.POOLDAY_POLL_S)
    s = sub.add_parser("api-log", help="Poolday API calls (all, or one lead)")
    s.add_argument("id", type=int, nargs="?")
    sub.add_parser("poolday-status", help="which Poolday client is active, and credits")
    s = sub.add_parser("fake-poolday", help="run the local fake Poolday API (tests/demos)")
    s.add_argument("--port", type=int, default=8766)
    s = sub.add_parser("export", help="write approved drafts to .eml + CSV")
    s.add_argument("--all", action="store_true", help="re-export already exported leads too")
    s = sub.add_parser("serve", help="start the review dashboard")
    s.add_argument("--port", type=int, default=8765)
    s = sub.add_parser("llm-export", help="Claude Code mode: dump pending LLM tasks")
    s.add_argument("--file", default=str(config.LOOP_DIR / "work" / "llm_tasks.json"))
    s = sub.add_parser("llm-import", help="Claude Code mode: load answered LLM tasks")
    s.add_argument("--file", default=str(config.LOOP_DIR / "work" / "llm_tasks.json"))
    sub.add_parser("reset", help="delete the local database")

    a = p.parse_args(argv)
    if a.cmd == "reset":
        if config.DB_PATH.exists():
            config.DB_PATH.unlink()
        print(f"removed {config.DB_PATH}")
        return
    if a.cmd == "serve":
        from .server import serve
        serve(a.port)
        return
    if a.cmd == "fake-poolday":
        from .poolday_fake import serve_forever
        serve_forever(a.port)
        return

    conn = store.connect()
    if a.cmd in ("ingest", "run"):
        print("ingest:", pipeline.ingest(conn, getattr(a, "source", None) or ["csv"],
                                         getattr(a, "fetch_sites", False)))
    if a.cmd in ("qualify", "run"):
        print(f"qualify (llm mode: {config.llm_mode()}):",
              pipeline.qualify_all(conn, a.rescore, a.limit, a.domain))
        if config.llm_mode() == "api":
            from . import llm
            tin = sum(u["input_tokens"] for u in llm.USAGE)
            tout = sum(u["output_tokens"] for u in llm.USAGE)
            print(f"api usage: {len(llm.USAGE)} calls, {tin} input + {tout} output tokens")
    if a.cmd in ("run", "list", "qualify"):
        _print_table(store.all_leads(conn, getattr(a, "status", None)))
    elif a.cmd == "show":
        lead = store.get(conn, a.id)
        lead["events"] = store.events(conn, a.id)
        print(json.dumps(lead, indent=2))
    elif a.cmd == "video":
        print(pipeline.submit_video(conn, a.id, a.url)["status"])
    elif a.cmd == "approve":
        lead = pipeline.approve(conn, a.id, a.note)
        print(f"Subject: {lead['email']['subject']}\n\n{lead['email']['body']}")
    elif a.cmd == "reject":
        print(pipeline.reject(conn, a.id, a.note)["status"])
    elif a.cmd == "regenerate":
        lead = pipeline.regenerate(conn, a.id, a.note)
        pd = lead.get("poolday") or {}
        if pd.get("production_id") and not pd.get("pending_revision"):
            print(f"Revision sent to the same Poolday conversation ({pd['production_id']}, {pd['status']}):")
        elif pd.get("pending_revision"):
            print(f"Revision NOT sent ({pd.get('error')}). Retry with `send {a.id}`, or paste it by hand:")
        else:
            print("Paste into the same Poolday conversation:")
        print(lead["poolday_prompts"]["revision"])
    elif a.cmd == "send":
        pd = pipeline.send_to_poolday(conn, a.id, a.prompt)["poolday"]
        print(f"sent: {pd['production_id']} ({pd['status']})")
    elif a.cmd == "answer":
        pd = pipeline.answer_poolday(conn, a.id, a.text)["poolday"]
        print(f"answered: {pd['production_id']} ({pd['status']})")
    elif a.cmd == "poll":
        import time
        while True:
            print(pipeline.poll_poolday(conn))
            active = [l for l in store.all_leads(conn, "qualified")
                      if (l.get("poolday") or {}).get("status") in ("queued", "running")]
            waiting = [l["company"] for l in store.all_leads(conn, "qualified")
                       if (l.get("poolday") or {}).get("status") == "needs_input"]
            if waiting:
                print("waiting for your answer:", ", ".join(waiting))
            if not a.watch or not active:
                break
            time.sleep(a.interval)
    elif a.cmd == "api-log":
        for c in store.api_calls(conn, a.id):
            print(f"{c['ts']}  lead {c['lead_id'] or '-':>3}  {c['op']:<8} {c['method']} {c['path']}"
                  f"  -> {c['http_status']} ({c['ms']} ms)")
    elif a.cmd == "poolday-status":
        st = poolday_api.status_line()
        if st.get("ok") and st.get("automatic"):
            try:
                st["credits"] = pipeline.poolday_client(conn).credits()
            except poolday_api.PooldayError as exc:
                st["credits_error"] = str(exc)
        print(json.dumps(st, indent=2))
    elif a.cmd == "export":
        print(json.dumps(pipeline.export(conn, include_exported=a.all), indent=2))
    elif a.cmd == "llm-export":
        print(pipeline.llm_export(conn, Path(a.file)))
    elif a.cmd == "llm-import":
        print(pipeline.llm_import(conn, Path(a.file)))


if __name__ == "__main__":
    main()
