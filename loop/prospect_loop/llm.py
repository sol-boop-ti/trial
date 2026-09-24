"""LLM steps: qualification and email drafting.

Three ways to run them:
  * api   - Anthropic Python SDK (ANTHROPIC_API_KEY set, or LLM_MODE=api)
  * mock  - deterministic, offline, plausible output (default without a key)
  * Claude Code - `python -m prospect_loop llm-export` writes the same prompts
    and schemas to a JSON file, Claude Code fills in the answers, and
    `llm-import` validates and stores them (see .claude/commands/process-leads.md)
"""
from __future__ import annotations

import json
import re

from . import config

# --------------------------------------------------------------------------- rubric

ICP_RUBRIC = """You qualify B2B leads for Poolday, an AI video production agent that makes
launch films, product teasers and ads. We send each qualified lead a free,
personalized ~20s video made for them, then a short email.

Score each criterion 0-20 (total 0-100):
1. b2b           - sells to businesses (20); mixed prosumer+business (10); consumer (0).
2. freshness     - latest round recency: <=14 days 20, <=30 17, <=60 14, <=90 11, <=180 6, older 0-3.
                   A fresh round means budget, hiring and a launch/announcement to amplify.
3. buyer         - a named marketing/creative decision-maker we can send the video to
                   (CMO, VP/Head of Marketing, Product Marketing, Creative Director, Head of Design: 16-20;
                   growth/demand/content: 10-15; none: 0).
4. visual_product- the product/UI/experience makes rich video material (UI, 3D, visual output: high;
                   pure backend/finance ops: low).
5. video_need    - would their marketing team plausibly buy video now (upcoming launch, new product line,
                   announcement, design-led brand)?

Rules: use only the facts given; do not invent customers, metrics or launches. If a fact is
missing, score conservatively and say so. `justification` is 2-3 short sentences citing the
facts that drove the score. `video_angle` is one line describing the video to make for them
(framed around their moment, e.g. "your Series B announcement film" or "what your meetings launch
could look like"). `launch_hook` is the short noun phrase for their moment (e.g. "the move into
meetings"). `audience` is who the video is for (role, not a name)."""

QUALIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "rubric": {
            "type": "object",
            "properties": {k: {"type": "integer"} for k in
                           ("b2b", "freshness", "buyer", "visual_product", "video_need")},
            "required": ["b2b", "freshness", "buyer", "visual_product", "video_need"],
            "additionalProperties": False,
        },
        "score": {"type": "integer"},
        "justification": {"type": "string"},
        "video_angle": {"type": "string"},
        "launch_hook": {"type": "string"},
        "audience": {"type": "string"},
    },
    "required": ["rubric", "score", "justification", "video_angle", "launch_hook", "audience"],
    "additionalProperties": False,
}

EMAIL_GUIDE = """You write short cold emails from someone at Poolday (an AI video production
agent) to a marketing/creative leader at a company that just raised. We already made them a
free ~20s video. Constraints:
- 60-110 words in the body, plain text, no bullet points, no emojis, no hype words.
- Personalize with: their round (amount + stage), their moment/launch hook, the contact's role.
- Include the literal line `[VIDEO THUMBNAIL]` on its own line, then the video link on the next.
- Exactly one call to action, phrased as a single yes/no question.
- Greeting uses the first name only. Sign off with the sender name given.
- Never invent facts, customers, metrics or quotes. Never mention which AI models were used.
- Subject: under 8 words, specific to them, no clickbait."""

EMAIL_SCHEMA = {
    "type": "object",
    "properties": {"subject": {"type": "string"}, "body": {"type": "string"}},
    "required": ["subject", "body"],
    "additionalProperties": False,
}


def lead_facts(lead: dict) -> dict:
    """The only facts the model sees (no invented enrichment)."""
    return {
        "company": lead["company"],
        "url": lead.get("url"),
        "what_they_do": lead.get("what_they_do"),
        "round": lead.get("round"),
        "round_amount_musd": lead.get("round_amount_m"),
        "round_date": lead.get("round_date"),
        "days_since_round": lead.get("days_since_round"),
        "total_funding_musd": lead.get("total_funding_m"),
        "notes": lead.get("confidence_notes"),
        "contacts": [{"first_name": c.get("first_name"), "title": c.get("title")}
                     for c in lead.get("contacts") or []],
        "site_title": lead.get("site_title"),
        "site_description": lead.get("site_description"),
    }


def qualify_prompt(lead: dict) -> str:
    return ("Qualify this lead against the rubric. Return JSON only.\n\n"
            + json.dumps(lead_facts(lead), indent=2))


def email_prompt(lead: dict, note: str = "") -> str:
    q = lead.get("qualification") or {}
    c = lead.get("primary_contact") or {}
    ctx = {
        **lead_facts(lead),
        "recipient_first_name": c.get("first_name"),
        "recipient_title": c.get("title"),
        "video_angle": q.get("video_angle"),
        "launch_hook": q.get("launch_hook"),
        "video_link": lead.get("video_url"),
        "sender_name": config.SENDER_NAME,
    }
    extra = f"\n\nReviewer note to apply: {note}" if note else ""
    return "Draft the email. Return JSON only.\n\n" + json.dumps(ctx, indent=2) + extra


# --------------------------------------------------------------------------- validation

def clean_qualification(data: dict) -> dict:
    rubric = {k: max(0, min(20, int(data["rubric"].get(k, 0))))
              for k in ("b2b", "freshness", "buyer", "visual_product", "video_need")}
    return {
        "rubric": rubric,
        "score": max(0, min(100, int(data.get("score") or sum(rubric.values())))),
        "justification": str(data["justification"]).strip(),
        "video_angle": str(data["video_angle"]).strip(),
        "launch_hook": str(data["launch_hook"]).strip(),
        "audience": str(data["audience"]).strip(),
    }


def clean_email(data: dict) -> dict:
    return {"subject": str(data["subject"]).strip(), "body": str(data["body"]).strip()}


# --------------------------------------------------------------------------- API mode

def _call_api(system: str, user: str, schema: dict, max_tokens: int = 4000) -> dict:
    import anthropic  # imported lazily so mock mode needs no dependency

    client = anthropic.Anthropic()
    kwargs = dict(
        model=config.MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"effort": config.EFFORT,
                       "format": {"type": "json_schema", "schema": schema}},
    )
    try:
        if config.MODEL in config.FALLBACK_MODELS:
            # Server-side refusal fallback: a declined request is re-run on the
            # recommended fallback model inside the same call.
            resp = client.beta.messages.create(
                betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
        else:
            resp = client.messages.create(**kwargs)
    except anthropic.AuthenticationError as exc:
        raise RuntimeError("Anthropic API key rejected. Unset it or set LLM_MODE=mock.") from exc
    except anthropic.NotFoundError as exc:
        raise RuntimeError(f"Model '{config.MODEL}' not found. Check CLAUDE_MODEL.") from exc
    except anthropic.RateLimitError as exc:
        raise RuntimeError("Rate limited by the API; retry in a minute.") from exc
    except anthropic.APIStatusError as exc:
        raise RuntimeError(f"API error {exc.status_code}: {exc.message}") from exc
    except anthropic.APIConnectionError as exc:
        raise RuntimeError("Could not reach the Anthropic API.") from exc

    if resp.stop_reason == "refusal":
        raise RuntimeError("The model declined this request.")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("Output truncated (max_tokens).")
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


# --------------------------------------------------------------------------- mock mode

def _mock_angle(lead: dict) -> tuple[str, str]:
    what = (lead.get("what_they_do") or "").strip()
    moving = re.search(r"moving into ([\w\s-]+)", what, re.I)
    days = lead.get("days_since_round")
    if moving:
        topic = moving.group(1).strip()
        return (f"what your {topic} launch could look like: a 20s teaser built from your product UI",
                f"the move into {topic}")
    if days is not None and days <= 21:
        return ("your Series B announcement film: a 20s teaser that turns the round into a launch moment",
                "the Series B announcement")
    short = what.split("(")[0].split(",")[0].strip().rstrip(".") or "your product"
    return (f"a 20s product teaser that makes {short[0].lower() + short[1:]} feel inevitable",
            "the post-raise launch push")


def mock_qualify(lead: dict) -> dict:
    from .enrich import prescore

    total, parts = prescore(lead)
    fit = parts["video_fit"]
    rubric = {
        "b2b": 20 if parts["b2b"] == 15 else 10,
        "freshness": round(parts["freshness"] / 40 * 20),
        "buyer": round(parts["buyer"] / 25 * 20),
        "visual_product": min(20, fit + 1),
        "video_need": min(20, fit + (2 if (lead.get("days_since_round") or 999) <= 60 else -2)),
    }
    score = sum(rubric.values())
    c = lead.get("primary_contact")
    days = lead.get("days_since_round")
    bits = []
    if days is not None:
        bits.append(f"{lead.get('round') or 'Round'} of ${lead.get('round_amount_m')}M {days} days ago"
                    + (" (fresh: launch/hiring push)." if days <= 60 else " (not fresh)."))
    bits.append(f"Buyer: {c['title']}." if c else "No named marketing/creative buyer in the data.")
    if lead.get("flags"):
        bits.append("Flags: " + ", ".join(f.lower() for f in lead["flags"]) + ".")
    angle, hook = _mock_angle(lead)
    return {
        "rubric": rubric,
        "score": score,
        "justification": "[mock] " + " ".join(bits),
        "video_angle": angle,
        "launch_hook": hook,
        "audience": c["title"] if c else "marketing leadership",
    }


def mock_email(lead: dict, note: str = "") -> dict:
    q = lead.get("qualification") or {}
    c = lead.get("primary_contact") or {}
    first = c.get("first_name") or "there"
    role = (c.get("title") or "marketing").split(",")[0]
    amount = lead.get("round_amount_m")
    hook = q.get("launch_hook") or "your next launch"
    body = (
        f"Hi {first},\n\n"
        f"Congrats on the ${amount}M {lead.get('round') or 'round'}. With {hook} coming, "
        f"I figured the {role} seat is about to need a lot of video, fast.\n\n"
        f"So we made one for {lead['company']} with Poolday, from your site alone, no brief:\n\n"
        f"[VIDEO THUMBNAIL]\n{lead.get('video_url') or '<VIDEO LINK>'}\n\n"
        f"Poolday is an AI video production agent: this one took an afternoon, not a quarter.\n\n"
        f"Want the editable version to use for {hook}?\n\n"
        f"{config.SENDER_NAME}"
    )
    if note:
        body += f"\n\n[mock: reviewer note not applied automatically: {note}]"
    return {"subject": f"A launch video for {lead['company']}", "body": body}


# --------------------------------------------------------------------------- public API

def qualify(lead: dict) -> tuple[dict, str]:
    if config.llm_mode() == "api":
        return clean_qualification(_call_api(ICP_RUBRIC, qualify_prompt(lead), QUALIFY_SCHEMA)), "api"
    return clean_qualification(mock_qualify(lead)), "mock"


def draft_email(lead: dict, note: str = "") -> tuple[dict, str]:
    if config.llm_mode() == "api":
        return clean_email(_call_api(EMAIL_GUIDE, email_prompt(lead, note), EMAIL_SCHEMA)), "api"
    return clean_email(mock_email(lead, note)), "mock"
