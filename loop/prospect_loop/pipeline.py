"""Pipeline steps and human-gate actions. Shared by the CLI and the dashboard."""
from __future__ import annotations

import csv
import json
import re
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path

from . import config, enrich, llm, poolday, sources, store


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
    store.log(conn, lead["id"], f"qualified:{mode}",
              f"score {q['score']} -> {lead['status']}")


def qualify_all(conn, rescore: bool = False) -> dict:
    todo = store.all_leads(conn, "new")
    if rescore:
        todo += store.all_leads(conn, "disqualified")
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


def submit_video(conn, lead_id: int, url: str) -> dict:
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
    store.log(conn, lead_id, "video_submitted", f"v{lead.get('video_version', 1)} {url}")
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
    return lead


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
