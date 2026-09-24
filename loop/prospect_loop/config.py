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

MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "4000"))  # per call; keep modest on a small budget

# Models that accept the server-side refusal fallback (`fallbacks="default"`).
FALLBACK_MODELS = {"claude-opus-5", "claude-fable-5-1"}
# Models that reject `output_config.effort` (400): send no effort for these.
NO_EFFORT_PREFIXES = ("claude-haiku", "claude-sonnet-4-5", "claude-opus-4-1", "claude-3")


def supports_effort(model: str) -> bool:
    return not model.startswith(NO_EFFORT_PREFIXES)

QUALIFY_THRESHOLD = int(os.environ.get("QUALIFY_THRESHOLD", "70"))
PRESCORE_GATE = int(os.environ.get("PRESCORE_GATE", "45"))  # below this, skip the LLM call

EXCLUDE_DOMAINS = {"higgsfield.ai"}  # per the brief

SENDER_NAME = os.environ.get("SENDER_NAME", "[Your name]")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "you@example.com")
REFERENCE_VIDEO = os.environ.get("REFERENCE_VIDEO", "<REFERENCE VIDEO LINK>")

# ---- Poolday API (see POOLDAY_API.md). POOLDAY_API = manual | fake | http (auto: see poolday_mode)
POOLDAY_API_CONFIG = Path(os.environ.get("POOLDAY_API_CONFIG", LOOP_DIR / "poolday_api.toml"))
POOLDAY_PROMPT = os.environ.get("POOLDAY_PROMPT", "command")   # which prompt the API sends: command | fallback
POOLDAY_MODE = os.environ.get("POOLDAY_MODE", "")              # override the mapping's default mode (align | build | clarify)
POOLDAY_TIER = os.environ.get("POOLDAY_TIER", "")              # override the default tier (micro | light | standard | max | ultra)
POOLDAY_SKILL_FILE = os.environ.get("POOLDAY_SKILL_FILE", str(REPO_DIR / "poolday" / "ref-replicate-skill.md"))
POOLDAY_POLL_S = float(os.environ.get("POOLDAY_POLL_S", "5"))  # dashboard background poller interval


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


def poolday_mode() -> str:
    """manual | fake | http. `POOLDAY_API` wins; otherwise http when a mapping file and
    POOLDAY_API_KEY both exist, else manual (copy/paste)."""
    mode = os.environ.get("POOLDAY_API", "").strip().lower()
    if mode in {"manual", "fake", "http"}:
        return mode
    return "http" if POOLDAY_API_CONFIG.exists() and os.environ.get("POOLDAY_API_KEY") else "manual"
