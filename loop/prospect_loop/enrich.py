"""Enrichment + deterministic pre-score (works with no LLM at all).

Enrichment here is local and offline: parse dates, pick the best buyer contact,
read the segment/geo flags already in the CSV. `fetch_site_meta` optionally pulls
the homepage <title>/description (used with `--fetch-sites`).
"""
from __future__ import annotations

import html
import re
import urllib.request
from datetime import date, datetime
from email.utils import parsedate_to_datetime

from . import config

# Title keyword -> buyer strength (higher = closer to the person who buys video).
BUYER_TIERS = [
    (3, ("creative director", "cmo", "chief marketing", "vp of product marketing", "vp marketing",
         "vice president marketing", "vp, marketing", "head of marketing", "head of design",
         "product marketing")),
    (2, ("growth", "demand", "content", "communications", "brand", "marketing manager",
         "revenue marketing", "field marketing")),
    (1, ("marketing", "sales")),
]

VIDEO_FIT_STRONG = ("video", "visual", "content", "creative", "design", "mixed-reality", "3d",
                    "presentation", "storytelling", "image", "interactive", " ar ")
VIDEO_FIT_WEAK = ("accounting", "procurement", "compliance", "tax", "erp", "banking",
                  "grc", "leave-management", "portfolio-management", "document-automation")


def parse_round_date(raw: str) -> date | None:
    raw = (raw or "").strip()
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    try:  # RSS pubDate
        return parsedate_to_datetime(raw).date()
    except (TypeError, ValueError):
        return None


def buyer_tier(title: str) -> int:
    t = (title or "").lower()
    for tier, keys in BUYER_TIERS:
        if any(k in t for k in keys):
            return tier
    return 0


def first_name(full: str) -> str:
    """'Carolyn [last masked]' -> 'Carolyn'; 'Lukas Le***t' -> 'Lukas'."""
    return (full or "").split(" ")[0].strip() or "there"


def enrich(raw: dict) -> dict:
    lead = dict(raw)
    d = parse_round_date(raw.get("round_date_raw", ""))
    lead["round_date"] = d.isoformat() if d else None
    lead["days_since_round"] = (config.today() - d).days if d else None
    lead["url"] = f"https://{raw['domain']}"
    contacts = sorted(raw.get("contacts") or [], key=lambda c: -buyer_tier(c["title"]))
    for c in contacts:
        c["first_name"] = first_name(c["name"])
        c["buyer_tier"] = buyer_tier(c["title"])
    lead["contacts"] = contacts
    lead["primary_contact"] = contacts[0] if contacts else None
    notes = (raw.get("confidence_notes") or "").upper()
    lead["flags"] = [f for f in ("SEGMENT FLAG", "GEO FLAG", "PROSUMER") if f in notes
                     or f in (raw.get("what_they_do") or "").upper()]
    return lead


def prescore(lead: dict) -> tuple[int, dict]:
    """Deterministic 0-100 score: freshness 40 + buyer 25 + B2B 15 + video fit 20."""
    days = lead.get("days_since_round")
    if days is None:
        fresh = 0
    elif days <= 14:
        fresh = 40
    elif days <= 30:
        fresh = 34
    elif days <= 60:
        fresh = 28
    elif days <= 90:
        fresh = 22
    elif days <= 180:
        fresh = 12
    elif days <= 365:
        fresh = 5
    else:
        fresh = 0

    tier = (lead.get("primary_contact") or {}).get("buyer_tier", -1)
    buyer = {3: 25, 2: 18, 1: 12, 0: 8}.get(tier, 0)
    if len(lead.get("contacts") or []) >= 2 and buyer:
        buyer = min(25, buyer + 3)

    flags = lead.get("flags") or []
    b2b = 7 if ("SEGMENT FLAG" in flags or "PROSUMER" in flags) else 15

    text = f" {(lead.get('what_they_do') or '').lower()} "
    if any(k in text for k in VIDEO_FIT_STRONG):
        fit = 18
    elif any(k in text for k in VIDEO_FIT_WEAK):
        fit = 6
    else:
        fit = 11

    parts = {"freshness": fresh, "buyer": buyer, "b2b": b2b, "video_fit": fit}
    return sum(parts.values()), parts


def fetch_site_meta(url: str, timeout: float = 8.0) -> dict:
    """Best-effort homepage title + meta description. Never raises."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prospect-loop/0.1"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            page = resp.read(300_000).decode("utf-8", "replace")
    except Exception as exc:
        return {"site_error": str(exc)[:120]}
    title = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', page, re.I)
    return {
        "site_title": html.unescape(title.group(1).strip())[:200] if title else "",
        "site_description": html.unescape(desc.group(1).strip())[:400] if desc else "",
    }
