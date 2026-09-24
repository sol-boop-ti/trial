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
missing, score conservatively and say so. `score` is the sum of the five criteria.
`justification` is 2-3 short sentences (60 words max) citing the facts that drove the score;
do not repeat the per-criterion numbers in it. When `freshness_points` is given, use it as the
freshness score.
`video_angle` is at most 10 words, addressed to them, framed around their moment, with no hype
words: it is pasted verbatim into the video brief (e.g. "your Series B announcement film" or
"what your meetings launch could look like"). `launch_hook` is a short noun phrase for their
moment, at most 6 words (e.g. "the move into meetings"). `audience` is one role, not a name
(e.g. "VP of Product Marketing")."""

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
- Personalize with: their round (amount + stage, e.g. "$40M Series B"), their moment/launch
  hook, and why it matters for the contact's role.
- Say once, plainly, that the video was made with Poolday, an AI video production agent.
- Include the literal line `[VIDEO THUMBNAIL]` on its own line, then the video link on the next.
- Exactly one call to action, phrased as a single yes/no question; no other question marks.
- Greeting uses the first name only. Sign off with the sender name given.
- Never invent facts, customers, metrics or quotes. Never mention which AI models were used.
- Subject: under 8 words, specific to them, no clickbait.

Body shape (blank line between blocks):
Hi <first name>,
<2-3 sentences: the round, their moment, why it matters for their role>
<1 sentence: we made them a ~20s video with Poolday>
[VIDEO THUMBNAIL]
<video link>
<the one yes/no question>
<sender name>"""

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
    facts = lead_facts(lead)
    pts = freshness_points(lead.get("days_since_round"))
    if pts is not None:
        facts["freshness_points"] = pts  # computed from the rubric's bands; use as-is
    return ("Qualify this lead against the rubric. Return JSON only.\n\n"
            + json.dumps(facts, indent=2))


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

def freshness_points(days: int | None) -> int | None:
    """The rubric's freshness scale, applied in code (models misread the bands)."""
    if days is None:
        return None
    for limit, pts in ((14, 20), (30, 17), (60, 14), (90, 11), (180, 6), (365, 3)):
        if days <= limit:
            return pts
    return 0


def clean_qualification(data: dict, lead: dict | None = None) -> dict:
    rubric = {k: max(0, min(20, int(data["rubric"].get(k, 0))))
              for k in ("b2b", "freshness", "buyer", "visual_product", "video_need")}
    fresh = freshness_points((lead or {}).get("days_since_round"))
    if fresh is not None:
        rubric["freshness"] = fresh
    return {
        "rubric": rubric,
        # The total is always the sum of the criteria (a model's own total can drift from it).
        "score": sum(rubric.values()),
        "justification": str(data["justification"]).strip(),
        "video_angle": str(data["video_angle"]).strip(),
        "launch_hook": str(data["launch_hook"]).strip(),
        "audience": str(data["audience"]).strip(),
    }


def clean_email(data: dict, lead: dict | None = None) -> dict:
    body = str(data["body"]).strip().replace("\r\n", "\n")
    # Deterministic layout fix: the thumbnail placeholder and the link each on their own line.
    body = re.sub(r"[ \t]*\[VIDEO THUMBNAIL\][ \t]*", "\n\n[VIDEO THUMBNAIL]\n", body)
    body = re.sub(r"\[VIDEO THUMBNAIL\]\n\s*(https?://\S+)[ \t]*", r"[VIDEO THUMBNAIL]\n\1\n\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    out = {"subject": str(data["subject"]).strip(), "body": body}
    if lead is not None:
        out["checks"] = email_checks(out, lead)
    return out


MODEL_NAMES = re.compile(r"\b(claude|anthropic|gpt|openai|gemini|chatgpt|llm)\b", re.I)


def email_checks(email: dict, lead: dict) -> list[str]:
    """The email guide's hard rules, checked in code. Empty list = passes."""
    body, issues = email["body"], []
    c = lead.get("primary_contact") or {}
    first = c.get("first_name")
    link = lead.get("video_url")
    words = [w for w in body.split() if w != "[VIDEO THUMBNAIL]" and not w.startswith("http")]
    if not 60 <= len(words) <= 110:
        issues.append(f"body is {len(words)} words (60-110)")
    if first and not body.startswith(f"Hi {first}"):
        issues.append(f"greeting should be 'Hi {first},'")
    lines = body.splitlines()
    if "[VIDEO THUMBNAIL]" not in lines:
        issues.append("missing the [VIDEO THUMBNAIL] line")
    elif link and (lines.index("[VIDEO THUMBNAIL]") + 1 >= len(lines)
                   or lines[lines.index("[VIDEO THUMBNAIL]") + 1].strip() != link):
        issues.append("the video link must be on the line after [VIDEO THUMBNAIL]")
    if body.count("?") != 1:
        issues.append(f"{body.count('?')} question marks (exactly one yes/no question)")
    amount = lead.get("round_amount_m")
    if amount and f"${amount}M" not in body.replace(",", ""):
        issues.append(f"round amount ${amount}M not mentioned")
    if "poolday" not in body.lower():
        issues.append("Poolday not named")
    if not body.rstrip().endswith(config.SENDER_NAME):
        issues.append(f"should sign off with '{config.SENDER_NAME}'")
    if MODEL_NAMES.search(body + " " + email["subject"]):
        issues.append("mentions an AI model/vendor")
    if len(email["subject"].split()) >= 8:
        issues.append("subject is 8+ words")
    return issues


# --------------------------------------------------------------------------- API mode

# Token usage of every API call in this process (for spend reporting and the event log).
USAGE: list[dict] = []


def _call_api(system: str, user: str, schema: dict, max_tokens: int | None = None) -> dict:
    import anthropic  # imported lazily so mock mode needs no dependency

    client = anthropic.Anthropic()
    output_config: dict = {"format": {"type": "json_schema", "schema": schema}}
    if config.supports_effort(config.MODEL):
        output_config["effort"] = config.EFFORT
    kwargs = dict(
        model=config.MODEL,
        max_tokens=max_tokens or config.MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config=output_config,
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

    u = resp.usage
    USAGE.append({"model": getattr(resp, "model", config.MODEL),
                  "input_tokens": u.input_tokens, "output_tokens": u.output_tokens})
    if resp.stop_reason == "refusal":
        raise RuntimeError("The model declined this request.")
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"Output truncated at max_tokens={kwargs['max_tokens']} (raise LLM_MAX_TOKENS).")
    text = next((b.text for b in resp.content if b.type == "text"), None)
    if text is None:
        raise RuntimeError(f"No text in the response (stop_reason={resp.stop_reason}).")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Response was not valid JSON: {text[:200]}") from exc


def usage_note() -> str:
    """'in 812 / out 305 tokens' for the last API call (empty outside API mode)."""
    if not USAGE:
        return ""
    u = USAGE[-1]
    return f"in {u['input_tokens']} / out {u['output_tokens']} tokens"


# --------------------------------------------------------------------------- mock mode

def _mock_angle(lead: dict) -> tuple[str, str]:
    """Short, intent-level angle (it goes into the Poolday prompt) + the email hook."""
    what = (lead.get("what_they_do") or "").strip()
    moving = re.search(r"moving into ([\w\s-]+)", what, re.I)
    days = lead.get("days_since_round")
    if moving:
        topic = moving.group(1).strip()
        return f"what your {topic} launch could look like", f"the {topic} launch"
    if days is not None and days <= 21:
        return "your Series B announcement film", "the post-raise launch push"
    return "a 20s launch teaser for your next release", "your next launch"


def mock_qualify(lead: dict) -> dict:
    from .enrich import prescore

    total, parts = prescore(lead)
    fit = parts["video_fit"]
    # An announced expansion ("moving into meetings") means a launch that needs video.
    expansion = 4 if re.search(r"moving into|launch|new product", lead.get("what_they_do") or "", re.I) else 0
    rubric = {
        "b2b": 20 if parts["b2b"] == 15 else 10,
        "freshness": round(parts["freshness"] / 40 * 20),
        "buyer": round(parts["buyer"] / 25 * 20),
        "visual_product": min(20, fit + 1),
        "video_need": min(20, fit + expansion + (2 if (lead.get("days_since_round") or 999) <= 60 else -2)),
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
        f"Congrats on the ${amount}M {lead.get('round') or 'round'}. With {hook} ahead, "
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
        return clean_qualification(_call_api(ICP_RUBRIC, qualify_prompt(lead), QUALIFY_SCHEMA), lead), "api"
    return clean_qualification(mock_qualify(lead), lead), "mock"


def draft_email(lead: dict, note: str = "") -> tuple[dict, str]:
    if config.llm_mode() == "api":
        prompt = email_prompt(lead, note)
        email = clean_email(_call_api(EMAIL_GUIDE, prompt, EMAIL_SCHEMA), lead)
        if email["checks"]:  # one repair pass with the failed rules, then the human sees the rest
            retry = (f"{prompt}\n\nYour previous draft broke these rules: {'; '.join(email['checks'])}."
                     f"\nPrevious draft:\n{email['body']}\n\nRewrite it so every rule holds.")
            email = clean_email(_call_api(EMAIL_GUIDE, retry, EMAIL_SCHEMA), lead)
        return email, "api"
    return clean_email(mock_email(lead, note), lead), "mock"
