"""Poolday prompt generation. Short and intent-level on purpose.

Poolday's agent decides the execution; we only give it the inputs, the objective,
the audience and where it has freedom (see poolday/kickoff-prompts.md). Two forms:

  * command  - the saved `/prospect-video` command (2 lines), once it exists in Poolday
  * fallback - the kickoff prompt used before the command exists (drop the
               Reference Teaser skill file, then paste this)
"""
from __future__ import annotations

from . import config


def _audience(lead: dict) -> str:
    c = lead.get("primary_contact")
    if not c:
        return "their marketing lead"
    return f"{lead['company']}'s {c['title']}"


def command_prompt(lead: dict) -> str:
    q = lead.get("qualification") or {}
    return (
        f"/prospect-video {lead['url']} ref: {config.REFERENCE_VIDEO}\n"
        f"Angle: {q.get('video_angle', 'launch teaser')}. For: {_audience(lead)}."
    )


def fallback_prompt(lead: dict) -> str:
    q = lead.get("qualification") or {}
    return (
        "[drop the Reference Teaser skill file]\n"
        f"Use this skill. Reference: {config.REFERENCE_VIDEO}. Brand: {lead['url']}\n"
        "What I love in the reference: <2-3 specific things: cuts, type treatment, camera move>.\n"
        f"Objective: a teaser I'll send to {_audience(lead)}, framed as \"{q.get('video_angle', 'your launch film')}\". "
        "16:9, sent by email + LinkedIn.\n"
        "Make it the most impressive video possible: rich visual detail, seamless continuity from start to finish.\n"
        "You have creative freedom on everything not fixed by the reference and the brand."
    )


def revision_prompt(note: str) -> str:
    """Paste into the SAME Poolday conversation (variants/revisions stay in one conversation)."""
    return (
        f"Revision: {note.strip()}\n"
        "Keep everything else. Show me the changed shots before re-rendering the full cut."
    )


def build(lead: dict) -> dict:
    return {"command": command_prompt(lead), "fallback": fallback_prompt(lead)}
