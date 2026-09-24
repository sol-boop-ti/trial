"""Pipeline steps and human-gate actions. Shared by the CLI and the dashboard."""
from __future__ import annotations

import csv
import json
import re
import threading
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path

from . import config, enrich, llm, poolday, poolday_api, sources, store

# Serializes read-modify-write of a lead between dashboard requests and the Poolday poller.
LOCK = threading.RLock()


# --------------------------------------------------------------------------- 1. find + enrich

def ingest(conn, source_names=("csv",), fetch_sites: bool = False) -> dict:
    raws, stats = sources.collect(source_names)
    added = 0
    for raw in raws:
        lead = enrich.enrich(raw)
        if fetch_sites:
            lead.update(enrich.fetch_site_meta(lead["url"]))
        added += store.upsert_new(conn, lead)
    stats.update(unique=len(raws), added=added, already_known=len(raws) - added)
    return stats


# --------------------------------------------------------------------------- 2. qualify + 3. prompt

def _apply_qualification(conn, lead: dict, q: dict, mode: str) -> None:
    lead["qualification"] = q
    lead["qualified_by"] = mode
    lead["score"] = q["score"]
    if q["score"] >= config.QUALIFY_THRESHOLD:
        lead["status"] = "qualified"
        lead["poolday_prompts"] = poolday.build(lead)
        lead["video_version"] = 1
    else:
        lead["status"] = "disqualified"
    store.save(conn, lead)
    usage = llm.usage_note() if mode == "api" else ""
    store.log(conn, lead["id"], f"qualified:{mode}",
              f"score {q['score']} -> {lead['status']}" + (f" ({usage})" if usage else ""))


def qualify_all(conn, rescore: bool = False, limit: int | None = None,
                domains: list[str] | None = None) -> dict:
    """Pre-score, then LLM-score what passes the gate. `limit` caps the number of LLM
    calls (highest pre-score first) and `domains` restricts the run: both keep a real-API
    test run cheap."""
    todo = store.all_leads(conn, "new")
    if rescore:
        todo += store.all_leads(conn, "disqualified")
    if domains:
        todo = [l for l in todo if l["domain"] in set(domains)]
    todo.sort(key=lambda l: -enrich.prescore(l)[0])
    llm_calls = 0
    stats = {"scored": 0, "qualified": 0, "disqualified": 0, "prescore_cut": 0, "errors": 0}
    for lead in todo:
        pre, parts = enrich.prescore(lead)
        lead["prescore"], lead["prescore_parts"] = pre, parts
        if pre < config.PRESCORE_GATE:
            lead.update(status="disqualified", score=pre)
            store.save(conn, lead)
            store.log(conn, lead["id"], "prescore_cut", f"prescore {pre} < {config.PRESCORE_GATE}")
            stats["prescore_cut"] += 1
            continue
        if limit is not None and llm_calls >= limit:
            stats.setdefault("skipped_limit", 0)
            stats["skipped_limit"] += 1
            continue
        llm_calls += 1
        try:
            q, mode = llm.qualify(lead)
        except Exception as exc:
            store.save(conn, lead)
            store.log(conn, lead["id"], "error", f"qualify failed: {exc}")
            stats["errors"] += 1
            continue
        _apply_qualification(conn, lead, q, mode)
        stats["scored"] += 1
        stats[lead["status"]] += 1
    return stats


# --------------------------------------------------------------------------- 4. human gate

URL_RE = re.compile(r"^https?://\S+$")


def submit_video(conn, lead_id: int, url: str, source: str = "human") -> dict:
    url = url.strip()
    if not URL_RE.match(url):
        raise ValueError("Paste a full http(s) link to the Poolday video.")
    lead = store.get(conn, lead_id)
    if lead["status"] not in ("qualified", "in_review"):
        raise ValueError(f"Lead is '{lead['status']}', not awaiting a video.")
    lead["video_url"] = url
    lead.setdefault("video_history", []).append({"version": lead.get("video_version", 1), "url": url})
    lead["status"] = "in_review"
    store.save(conn, lead)
    store.log(conn, lead_id, "video_submitted", f"v{lead.get('video_version', 1)} {url} (from {source})")
    return lead


def approve(conn, lead_id: int, note: str = "") -> dict:
    lead = store.get(conn, lead_id)
    if lead["status"] != "in_review":
        raise ValueError("Only a lead with a submitted video can be approved.")
    lead["status"] = "approved"
    store.log(conn, lead_id, "approved", note or None)
    return redraft_email(conn, lead, note)


def reject(conn, lead_id: int, note: str = "") -> dict:
    lead = store.get(conn, lead_id)
    lead["status"] = "rejected"
    lead["reject_note"] = note
    store.save(conn, lead)
    store.log(conn, lead_id, "rejected", note or None)
    return lead


def regenerate(conn, lead_id: int, note: str) -> dict:
    """Video not good enough: produce a revision prompt and wait for a new link."""
    if not note.strip():
        raise ValueError("Say what to change (mechanisms, not adjectives: 'hard cut at 0:04').")
    lead = store.get(conn, lead_id)
    if lead["status"] != "in_review":
        raise ValueError("Only a lead with a submitted video can be regenerated.")
    lead["video_version"] = lead.get("video_version", 1) + 1
    lead["poolday_prompts"]["revision"] = poolday.revision_prompt(note)
    lead["video_url"] = None
    lead["status"] = "qualified"
    store.save(conn, lead)
    store.log(conn, lead_id, "regenerate", note)
    pd = lead.get("poolday") or {}
    if pd.get("production_id"):
        # API mode: the revision goes to the SAME Poolday conversation automatically.
        pd["pending_revision"] = True
        store.save(conn, lead)
        lead = _send_revision(conn, lead)
    return lead


# --------------------------------------------------------------------------- 4b. Poolday API

def poolday_client(conn, lead_id: int | None = None) -> poolday_api.PooldayClient:
    """The configured client, with every HTTP call recorded in the api_calls table."""
    client = poolday_api.get_client()
    client.on_call = lambda rec: store.log_api(conn, lead_id, f"poolday:{client.name}", rec)
    return client


def _record(conn, lead: dict, prod: poolday_api.Production, event: str | None = None,
            note: str | None = None) -> dict:
    """Store the production state on the lead; log status changes as events."""
    pd = lead.setdefault("poolday", {})
    before = pd.get("status")
    pd.update(production_id=prod.id or pd.get("production_id"), status=prod.status,
              raw_status=prod.raw_status, question=prod.question, question_id=prod.question_id,
              error=prod.error, updated_at=store.now())
    for k in ("video_url", "preview_url", "thumbnail_url"):
        if getattr(prod, k):
            pd[k] = getattr(prod, k)
    store.save(conn, lead)
    if event:
        store.log(conn, lead["id"], event, note)
    if prod.status != before:
        detail = {"needs_input": prod.question, "failed": prod.error}.get(prod.status)
        store.log(conn, lead["id"], f"poolday:{prod.status}",
                  f"{prod.id} ({prod.raw_status})" + (f": {detail}" if detail else ""))
    return lead


def _api_prompt(lead: dict, which: str) -> tuple[str, list[str]]:
    """The prompt text the API sends, and the files to attach."""
    prompts = lead["poolday_prompts"]
    if which == "fallback":
        # Via the API the skill file is an attachment, so the "[drop ...]" line goes.
        text = "\n".join(l for l in prompts["fallback"].splitlines() if not l.startswith("[drop"))
        skill = Path(config.POOLDAY_SKILL_FILE)
        return text, [str(skill)] if skill.exists() else []
    return prompts["command"], []


def send_to_poolday(conn, lead_id: int, which: str | None = None) -> dict:
    """Submit the generated prompt through the API (new conversation), or, when a
    revision is pending, send it to the existing conversation."""
    with LOCK:
        lead = store.get(conn, lead_id)
        if lead["status"] != "qualified":
            raise ValueError(f"Lead is '{lead['status']}', not awaiting a video.")
        client = poolday_client(conn, lead_id)
        if not client.automatic:
            raise ValueError("No Poolday API configured (POOLDAY_API=manual): copy the prompt "
                             "into Poolday and paste the video link back.")
        pd = lead.get("poolday") or {}
        if pd.get("production_id") and pd.get("pending_revision"):
            return _send_revision(conn, lead, client)
        if pd.get("production_id") and pd.get("status") in poolday_api.ACTIVE:
            raise ValueError(f"Already in production ({pd['production_id']}, {pd['status']}).")
        which = which or config.POOLDAY_PROMPT
        text, files = _api_prompt(lead, which)
        settings = {"title": f"{lead['company']} prospect video v{lead.get('video_version', 1)}"}
        if config.POOLDAY_MODE:
            settings["mode"] = config.POOLDAY_MODE
        if config.POOLDAY_TIER:
            settings["tier"] = config.POOLDAY_TIER
        ref = config.REFERENCE_VIDEO if URL_RE.match(config.REFERENCE_VIDEO) else None
        prod = client.start_production(text, attachments=files, reference_url=ref, settings=settings)
        lead["poolday"] = {"prompt_kind": which, "sent_prompt": text, "attachments": files,
                           "started_at": store.now(), "client": client.name}
        return _record(conn, lead, prod, "poolday:sent",
                       f"{prod.id} via {client.name} API ({which} prompt"
                       + (f", {len(files)} file(s)" if files else "") + ")")


def _send_revision(conn, lead: dict, client=None) -> dict:
    pd = lead["poolday"]
    text = lead["poolday_prompts"]["revision"]
    try:
        client = client or poolday_client(conn, lead["id"])
        prod = client.send_message(pd["production_id"], text)
    except poolday_api.PooldayError as exc:
        pd["error"] = f"revision not sent: {exc}"
        store.save(conn, lead)
        store.log(conn, lead["id"], "poolday:error", pd["error"])
        return lead
    pd["pending_revision"] = False
    pd.pop("video_url", None)
    return _record(conn, lead, prod, "poolday:revision_sent",
                   f"{pd['production_id']} v{lead.get('video_version')}: {text.splitlines()[0]}")


def answer_poolday(conn, lead_id: int, answer: str) -> dict:
    """The human answers the question Poolday's agent asked mid-run."""
    if not answer.strip():
        raise ValueError("Write an answer for the Poolday agent.")
    with LOCK:
        lead = store.get(conn, lead_id)
        pd = lead.get("poolday") or {}
        if pd.get("status") != "needs_input":
            raise ValueError("Poolday is not waiting for an answer on this lead.")
        client = poolday_client(conn, lead_id)
        prod = client.answer_question(pd["production_id"], answer.strip(), pd.get("question_id"))
        if prod.status == "needs_input" and prod.question == pd.get("question"):
            prod.status, prod.question = "running", None  # answered; next poll tells the truth
        return _record(conn, lead, prod, "poolday:answered", answer.strip())


def poll_poolday(conn, lead_id: int | None = None) -> dict:
    """One polling pass over every lead with a production in flight. A finished video
    goes to the human validation gate (in_review), never further."""
    stats = {"polled": 0, "changed": 0, "to_review": 0, "errors": 0}
    leads = [store.get(conn, lead_id)] if lead_id else store.all_leads(conn, "qualified")
    for lead in leads:
        pd = lead.get("poolday") or {}
        if lead["status"] != "qualified" or not pd.get("production_id") \
                or pd.get("status") not in poolday_api.ACTIVE:
            continue
        client = poolday_client(conn, lead["id"])
        try:
            prod = client.get_status(pd["production_id"])        # network call outside the lock
            if prod.status == "done" and not prod.video_url:
                prod = client.get_result(pd["production_id"])
        except poolday_api.PooldayRateLimited:
            stats["errors"] += 1
            break
        except poolday_api.PooldayError as exc:
            stats["errors"] += 1
            with LOCK:
                fresh = store.get(conn, lead["id"])
                fresh.setdefault("poolday", {})["error"] = str(exc)
                store.save(conn, fresh)
            continue
        stats["polled"] += 1
        with LOCK:
            fresh = store.get(conn, lead["id"])
            fpd = fresh.get("poolday") or {}
            if fresh["status"] != "qualified" or fpd.get("production_id") != pd["production_id"]:
                continue  # a human acted in the meantime
            if prod.status == fpd.get("status") and prod.question == fpd.get("question"):
                continue
            stats["changed"] += 1
            _record(conn, fresh, prod)
            if prod.status == "done":
                if prod.video_url and URL_RE.match(prod.video_url):
                    submit_video(conn, fresh["id"], prod.video_url, source="Poolday API")
                    stats["to_review"] += 1
                else:
                    store.log(conn, fresh["id"], "poolday:error", "done but no video URL in the result")
    return stats


class Poller(threading.Thread):
    """Background poller for the dashboard: one pass every POOLDAY_POLL_S seconds."""

    def __init__(self, interval: float | None = None):
        super().__init__(daemon=True, name="poolday-poller")
        self.interval = interval or config.POOLDAY_POLL_S
        self.stop = threading.Event()
        self.last: dict = {}

    def run(self):
        while not self.stop.wait(self.interval):
            try:
                conn = store.connect()
                try:
                    self.last = {**poll_poolday(conn), "at": store.now()}
                finally:
                    conn.close()
            except Exception as exc:  # keep polling; surface the error in /api/meta
                self.last = {"error": str(exc), "at": store.now()}


# --------------------------------------------------------------------------- 5. email

def redraft_email(conn, lead: dict | int, note: str = "") -> dict:
    if isinstance(lead, int):
        lead = store.get(conn, lead)
    email, mode = llm.draft_email(lead, note)
    lead["email"] = {**email, "drafted_by": mode, "edited": False}
    store.save(conn, lead)
    store.log(conn, lead["id"], f"email_drafted:{mode}", note or None)
    return lead


def save_email(conn, lead_id: int, subject: str, body: str) -> dict:
    lead = store.get(conn, lead_id)
    if lead["status"] not in ("approved", "exported"):
        raise ValueError("Approve the video before editing the email.")
    lead["email"] = {**(lead.get("email") or {}), "subject": subject, "body": body, "edited": True}
    store.save(conn, lead)
    store.log(conn, lead_id, "email_edited")
    return lead


# --------------------------------------------------------------------------- 6. export

def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def export(conn, out_dir: Path | None = None, include_exported: bool = False) -> dict:
    out = Path(out_dir or config.OUT_DIR)
    (out / "emails").mkdir(parents=True, exist_ok=True)
    leads = store.all_leads(conn, "approved")
    if include_exported:
        leads += store.all_leads(conn, "exported")
    rows, files = [], []
    for lead in leads:
        c = lead.get("primary_contact") or {}
        e = lead["email"]
        msg = EmailMessage()
        msg["From"] = f"{config.SENDER_NAME} <{config.SENDER_EMAIL}>"
        # The CSV has no email addresses: the sender fills "To" in their client.
        msg["To"] = ""
        msg["Subject"] = e["subject"]
        msg["Date"] = formatdate(localtime=True)
        msg["X-Unsent"] = "1"  # opens as an editable draft in Outlook/Apple Mail
        msg["X-Prospect"] = f"{lead['company']} | {c.get('name', '')} | {c.get('title', '')} | {c.get('linkedin', '')}"
        msg.set_content(e["body"])
        path = out / "emails" / f"{_slug(lead['company'])}.eml"
        path.write_bytes(bytes(msg))
        files.append(str(path))
        rows.append({
            "company": lead["company"], "domain": lead["domain"], "score": lead.get("score"),
            "contact": c.get("name", ""), "title": c.get("title", ""), "linkedin": c.get("linkedin", ""),
            "video_url": lead.get("video_url", ""), "subject": e["subject"], "body": e["body"],
            "eml_file": str(path),
        })
        if lead["status"] != "exported":
            lead["status"] = "exported"
            store.save(conn, lead)
            store.log(conn, lead["id"], "exported", str(path))
    csv_path = out / "email_drafts.csv"
    if rows:
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return {"count": len(rows), "csv": str(csv_path) if rows else None, "eml": files}


def export_gmail_drafts(conn) -> None:
    """STUB. Next step: create Gmail drafts instead of .eml files.

    Plan: google-api-python-client + OAuth installed-app flow (scope
    `https://www.googleapis.com/auth/gmail.compose`), then for each approved lead
    `users().drafts().create(userId="me", body={"message": {"raw": base64url(bytes(msg))}})`
    reusing the EmailMessage built in `export`. Not implemented on purpose: it needs the
    hiring manager's Google OAuth client, and the .eml export already opens as a draft.
    """
    raise NotImplementedError(export_gmail_drafts.__doc__)


# --------------------------------------------------------------------------- Claude Code mode

def llm_export(conn, path: Path) -> dict:
    """Write pending LLM tasks (prompts + schemas) for Claude Code to answer."""
    tasks = []
    for lead in store.all_leads(conn, "new"):
        pre, parts = enrich.prescore(lead)
        if pre < config.PRESCORE_GATE:  # same cheap cut as qualify_all
            lead.update(status="disqualified", score=pre, prescore=pre, prescore_parts=parts)
            store.save(conn, lead)
            store.log(conn, lead["id"], "prescore_cut", f"prescore {pre} < {config.PRESCORE_GATE}")
            continue
        tasks.append({"lead_id": lead["id"], "company": lead["company"], "task": "qualify",
                      "system": llm.ICP_RUBRIC, "prompt": llm.qualify_prompt(lead),
                      "schema": llm.QUALIFY_SCHEMA, "result": None})
    for lead in store.all_leads(conn, "approved"):
        if (lead.get("email") or {}).get("drafted_by") == "mock":
            tasks.append({"lead_id": lead["id"], "company": lead["company"], "task": "email",
                          "system": llm.EMAIL_GUIDE, "prompt": llm.email_prompt(lead),
                          "schema": llm.EMAIL_SCHEMA, "result": None})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"instructions": "Fill each task's `result` with JSON matching "
                                "`schema`, following `system`. Then run llm-import.",
                                "tasks": tasks}, indent=2))
    return {"tasks": len(tasks), "file": str(path)}


def llm_import(conn, path: Path) -> dict:
    data = json.loads(Path(path).read_text())
    done = skipped = 0
    for t in data["tasks"]:
        if not t.get("result"):
            skipped += 1
            continue
        lead = store.get(conn, t["lead_id"])
        if t["task"] == "qualify":
            pre, parts = enrich.prescore(lead)
            lead["prescore"], lead["prescore_parts"] = pre, parts
            _apply_qualification(conn, lead, llm.clean_qualification(t["result"]), "claude-code")
        elif t["task"] == "email":
            lead["email"] = {**llm.clean_email(t["result"]), "drafted_by": "claude-code", "edited": False}
            store.save(conn, lead)
            store.log(conn, lead["id"], "email_drafted:claude-code")
        done += 1
    return {"imported": done, "skipped": skipped}
