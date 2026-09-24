"""CLI:  python -m prospect_loop <command>   (run from the loop/ directory)"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import config, pipeline, store


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
    s = sub.add_parser("qualify", help="pre-score + LLM score, generate Poolday prompts")
    s.add_argument("--rescore", action="store_true", help="also re-run disqualified leads")
    sub.add_parser("run", help="ingest + qualify")
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

    conn = store.connect()
    if a.cmd in ("ingest", "run"):
        print("ingest:", pipeline.ingest(conn, getattr(a, "source", None) or ["csv"],
                                         getattr(a, "fetch_sites", False)))
    if a.cmd in ("qualify", "run"):
        print(f"qualify (llm mode: {config.llm_mode()}):",
              pipeline.qualify_all(conn, getattr(a, "rescore", False)))
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
        print("Paste into the same Poolday conversation:\n" + lead["poolday_prompts"]["revision"])
    elif a.cmd == "export":
        print(json.dumps(pipeline.export(conn, include_exported=a.all), indent=2))
    elif a.cmd == "llm-export":
        print(pipeline.llm_export(conn, Path(a.file)))
    elif a.cmd == "llm-import":
        print(pipeline.llm_import(conn, Path(a.file)))


if __name__ == "__main__":
    main()
