"""Runtime configuration. Everything is overridable through environment variables."""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

LOOP_DIR = Path(__file__).resolve().parent.parent          # .../loop
REPO_DIR = LOOP_DIR.parent                                  # .../trial

CSV_PATH = Path(os.environ.get("LEADS_CSV", REPO_DIR / "data" / "series-b-bay-area.csv"))
DB_PATH = Path(os.environ.get("LOOP_DB", LOOP_DIR / "work" / "leads.db"))
OUT_DIR = Path(os.environ.get("LOOP_OUT", LOOP_DIR / "out"))

# Model id lives here (and only here). Override with CLAUDE_MODEL.
DEFAULT_MODEL = "claude-opus-5"
MODEL = os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL)
EFFORT = os.environ.get("CLAUDE_EFFORT", "medium")  # low | medium | high

# Models that accept the server-side refusal fallback (`fallbacks="default"`).
FALLBACK_MODELS = {"claude-opus-5", "claude-fable-5-1"}

QUALIFY_THRESHOLD = int(os.environ.get("QUALIFY_THRESHOLD", "70"))
PRESCORE_GATE = int(os.environ.get("PRESCORE_GATE", "45"))  # below this, skip the LLM call

EXCLUDE_DOMAINS = {"higgsfield.ai"}  # per the brief

SENDER_NAME = os.environ.get("SENDER_NAME", "[Your name]")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "you@example.com")
REFERENCE_VIDEO = os.environ.get("REFERENCE_VIDEO", "<REFERENCE VIDEO LINK>")


def today() -> date:
    """`LOOP_TODAY=2026-09-24` pins the date so freshness scores are reproducible."""
    raw = os.environ.get("LOOP_TODAY")
    return date.fromisoformat(raw) if raw else date.today()


def llm_mode() -> str:
    """api | mock. `LLM_MODE` wins; otherwise api when a key is present."""
    mode = os.environ.get("LLM_MODE", "").strip().lower()
    if mode in {"api", "mock"}:
        return mode
    return "api" if os.environ.get("ANTHROPIC_API_KEY") else "mock"
