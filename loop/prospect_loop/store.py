"""SQLite state: one row per lead (JSON blob) + an append-only event log (audit trail
of every human decision)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain TEXT UNIQUE NOT NULL,
  status TEXT NOT NULL,
  score INTEGER,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id INTEGER NOT NULL,
  ts TEXT NOT NULL,
  action TEXT NOT NULL,
  note TEXT
);
CREATE TABLE IF NOT EXISTS api_calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id INTEGER,
  ts TEXT NOT NULL,
  service TEXT NOT NULL,
  op TEXT NOT NULL,
  method TEXT,
  path TEXT,
  http_status INTEGER,
  ms INTEGER,
  request TEXT,
  response TEXT
);
"""

# Lifecycle: new -> qualified (awaiting video) -> in_review -> approved -> exported
#            new -> disqualified;  in_review -> rejected;  in_review -> qualified (regenerate)
STATUSES = ["new", "qualified", "in_review", "approved", "exported", "rejected", "disqualified"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(path: Path | None = None) -> sqlite3.Connection:
    path = Path(path or config.DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)  # the dashboard poller writes from another thread
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _row(r: sqlite3.Row) -> dict:
    d = json.loads(r["data"])
    d.update(id=r["id"], domain=r["domain"], status=r["status"], score=r["score"],
             updated_at=r["updated_at"])
    return d


def upsert_new(conn, lead: dict) -> bool:
    """Insert a lead if its domain is unknown. Never overwrites human state."""
    cur = conn.execute(
        "INSERT OR IGNORE INTO leads(domain, status, score, data, updated_at) VALUES(?,?,?,?,?)",
        (lead["domain"], "new", None, json.dumps(lead), now()))
    if cur.rowcount:
        log(conn, cur.lastrowid, "ingested", lead.get("source"))
    conn.commit()
    return bool(cur.rowcount)


def get(conn, lead_id: int) -> dict:
    r = conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
    if not r:
        raise KeyError(f"lead {lead_id} not found")
    return _row(r)


def get_by_domain(conn, domain: str) -> dict | None:
    r = conn.execute("SELECT * FROM leads WHERE domain=?", (domain,)).fetchone()
    return _row(r) if r else None


def all_leads(conn, status: str | None = None) -> list[dict]:
    q = "SELECT * FROM leads" + (" WHERE status=?" if status else "") + \
        " ORDER BY COALESCE(score,-1) DESC, id"
    return [_row(r) for r in conn.execute(q, (status,) if status else ())]


def save(conn, lead: dict) -> None:
    data = {k: v for k, v in lead.items()
            if k not in ("id", "domain", "status", "score", "updated_at", "events")}
    conn.execute("UPDATE leads SET status=?, score=?, data=?, updated_at=? WHERE id=?",
                 (lead["status"], lead.get("score"), json.dumps(data), now(), lead["id"]))
    conn.commit()


def log(conn, lead_id: int, action: str, note: str | None = None) -> None:
    conn.execute("INSERT INTO events(lead_id, ts, action, note) VALUES(?,?,?,?)",
                 (lead_id, now(), action, note))
    conn.commit()


def events(conn, lead_id: int) -> list[dict]:
    return [dict(r) for r in conn.execute(
        "SELECT ts, action, note FROM events WHERE lead_id=? ORDER BY id", (lead_id,))]


def log_api(conn, lead_id: int | None, service: str, rec: dict) -> None:
    """One row per external API call (Poolday): op, method, path, status, latency, bodies.
    Auth headers are never passed in here."""
    conn.execute("INSERT INTO api_calls(lead_id, ts, service, op, method, path, http_status, ms, "
                 "request, response) VALUES(?,?,?,?,?,?,?,?,?,?)",
                 (lead_id, now(), service, rec.get("op"), rec.get("method"), rec.get("path"),
                  rec.get("http_status"), rec.get("ms"), rec.get("request"), rec.get("response")))
    conn.commit()


def api_calls(conn, lead_id: int | None = None, limit: int = 200) -> list[dict]:
    q = "SELECT * FROM api_calls" + (" WHERE lead_id=?" if lead_id is not None else "") + \
        " ORDER BY id DESC LIMIT ?"
    args = (lead_id, limit) if lead_id is not None else (limit,)
    return [dict(r) for r in conn.execute(q, args)][::-1]
