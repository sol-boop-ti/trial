"""CLI:  python -m prospect_loop <command>   (run from the loop/ directory)"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
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
    s = sub.add_parser("webhook-test", help="Poolday webhook: send one lead to Poolday's inbound webhook")
    s.add_argument("--domain", required=True, help="the lead's domain, e.g. flamapp.ai")
    s.add_argument("--brand-kit", help="name of the lead's brand kit in Poolday, if you made one")
    s.add_argument("--prompt", choices=["command", "fallback"], help="default: POOLDAY_PROMPT")
    s.add_argument("--force", action="store_true", help="re-send even if a run is marked in flight")
    s = sub.add_parser("simulate-callback", help="Poolday webhook: play Poolday calling us back (local test)")
    s.add_argument("--lead", type=int, required=True)
    s.add_argument("--video", help="video URL (moves the lead to Review)")
    s.add_argument("--question", help="a question from the agent instead of a video")
    s.add_argument("--status", help="status string to send (default: completed, or needs_input)")
    s.add_argument("--base", default="http://127.0.0.1:8765", help="where the dashboard runs")
    s.add_argument("--direct", action="store_true", help="skip HTTP, call the handler in-process")
    sub.add_parser("callback-url", help="Poolday webhook: print the callback URL to give Poolday")
    s = sub.add_parser("export", help="write approved drafts to .eml + CSV")
    s.add_argument("--all", action="store_true", help="re-export already exported leads too")
    s = sub.add_parser("serve", help="start the review dashboard")
    s.add_argument("--port", type=int, default=8765)
    s = sub.add_parser("llm-export", help="Claude Code mode: dump pending LLM tasks")
    s.add_argument("--file", default=str(config.LOOP_DIR / "work" / "llm_tasks.json"))
    s.add_argument("--rescore", action="store_true", help="also re-ask leads scored by the offline mock")
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
    if a.cmd == "callback-url":
        st = poolday_api.webhook_settings()
        if not st["callback_url"]:
            sys.exit("PUBLIC_BASE_URL is not set. Start the tunnel (cloudflared tunnel --url "
                     "http://localhost:8765) and export PUBLIC_BASE_URL=https://<it>.trycloudflare.com")
        print(st["callback_url"])
        print(f"secret header: {st['secret_header']} "
              f"({'secret set' if st['callback_secret'] else 'POOLDAY_WEBHOOK_SECRET NOT SET'})",
              file=sys.stderr)
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
    elif a.cmd == "webhook-test":
        os.environ["POOLDAY_API"] = "webhook"
        lead = next((l for l in store.all_leads(conn) if l["domain"] == a.domain), None)
        if lead is None:
            sys.exit(f"No lead {a.domain}. Run `python -m prospect_loop run` first.")
        if lead["status"] != "qualified":
            sys.exit(f"{a.domain} is '{lead['status']}', not awaiting a video.")
        if a.brand_kit:
            lead["brand_kit_name"] = a.brand_kit
            store.save(conn, lead)
        try:
            lead = pipeline.send_to_poolday(conn, lead["id"], a.prompt, force=a.force)
        except (ValueError, poolday_api.PooldayError) as exc:
            sys.exit(f"not sent: {exc}")
        pd = lead["poolday"]
        last = (store.api_calls(conn, lead["id"], limit=1) or [{}])[-1]
        print(f"sent lead {lead['id']} ({lead['company']}) -> Poolday webhook: HTTP {last.get('http_status')}")
        print(f"  production {pd['production_id']} ({pd['status']}), callback {pd.get('callback_url')}")
        print(f"  Poolday's reply: {last.get('response') or '(empty)'}")
        print("The lead moves to Review when Poolday calls back (keep `make serve` and the tunnel running).")
    elif a.cmd == "simulate-callback":
        lead = store.get(conn, a.lead)
        pd = lead.get("poolday") or {}
        st = poolday_api.webhook_settings()
        if not st["callback_secret"]:
            sys.exit("Set POOLDAY_WEBHOOK_SECRET (the same value the dashboard runs with).")
        if not pd.get("callback_token"):
            sys.exit(f"Lead {a.lead} was never sent to Poolday (no token). Use webhook-test first.")
        if not a.video and not a.question:
            sys.exit("Pass --video URL or --question TEXT.")
        payload = {"lead_id": a.lead, "token": pd["callback_token"],
                   "status": a.status or ("completed" if a.video else "needs_input"),
                   "version": lead.get("video_version", 1)}
        if a.video:
            payload["video_url"] = a.video
        if a.question:
            payload["question"] = a.question
        raw = json.dumps(payload).encode()
        headers = {"Content-Type": "application/json", st["secret_header"]: st["callback_secret"]}
        result = None
        if not a.direct:
            req = urllib.request.Request(a.base.rstrip("/") + poolday_api.CALLBACK_PATH, data=raw,
                                         headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    result = (r.status, json.loads(r.read() or b"{}"))
            except urllib.error.HTTPError as e:
                result = (e.code, json.loads(e.read() or b"{}"))
            except OSError:
                print(f"(dashboard not reachable at {a.base}: handling in-process)")
        if result is None:
            result = pipeline.handle_callback(conn, raw, headers, {})
        print(f"HTTP {result[0]}: {json.dumps(result[1])}")
        print(f"lead {a.lead} is now '{store.get(conn, a.lead)['status']}'")
    elif a.cmd == "export":
        print(json.dumps(pipeline.export(conn, include_exported=a.all), indent=2))
    elif a.cmd == "llm-export":
        print(pipeline.llm_export(conn, Path(a.file), a.rescore))
    elif a.cmd == "llm-import":
        print(pipeline.llm_import(conn, Path(a.file)))


if __name__ == "__main__":
    main()
