"""Poolday API integration: one interface, three implementations.

    PooldayClient          the operations the loop needs (abstract)
    HttpPooldayClient      real HTTP; every URL, header, path and field name comes from a
                           mapping file (poolday_api.toml) that is filled from Poolday's API docs
    ManualPooldayClient    the copy/paste flow (no API): the human is the transport
    FakePooldayClient      HttpPooldayClient pointed at the local fake server in
                           poolday_fake.py (async runs, a question mid-run, a video URL)
    WebhookPooldayClient   POSTs each lead to an inbound webhook that Poolday's agent
                           created; Poolday calls us back (POST /api/poolday/callback)
                           with the outputs. No polling. See README "Poolday via webhook".

Nothing here encodes a real Poolday endpoint. Until the docs arrive, the mapping file is
a template of placeholders (see poolday_api.example.toml and POOLDAY_API.md).

Status vocabulary used by the rest of the loop (Poolday's own strings are mapped onto it):
    queued · running · needs_input · done · failed
"""
from __future__ import annotations

import hmac
import json
import mimetypes
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from . import config

STATUSES = ("queued", "running", "needs_input", "done", "failed")
ACTIVE = ("queued", "running", "needs_input")
ENDPOINT_OPS = ("start", "message", "answer", "status", "result", "upload", "credits")
REQUIRED_OPS = ("start", "message", "status")  # the rest are optional


class PooldayError(RuntimeError):
    """An API call failed (HTTP error, bad response, network)."""


class PooldayNotConfigured(PooldayError):
    """The mapping still has placeholders, or the key is missing."""


class PooldayRateLimited(PooldayError):
    def __init__(self, msg: str, retry_after: float | None = None):
        super().__init__(msg)
        self.retry_after = retry_after


class ManualStep(PooldayError):
    """Raised by ManualPooldayClient: a human has to do this in the Poolday app."""


@dataclass
class Production:
    """One Poolday conversation/job as the loop sees it."""
    id: str | None
    status: str = "queued"                 # one of STATUSES
    raw_status: str | None = None          # Poolday's own status string, for the log
    question: str | None = None            # what the agent is asking (needs_input)
    question_id: str | None = None
    video_url: str | None = None
    preview_url: str | None = None
    thumbnail_url: str | None = None
    error: str | None = None
    raw: dict = field(default_factory=dict, repr=False)

    def summary(self) -> dict:
        d = asdict(self)
        d.pop("raw")
        return {k: v for k, v in d.items() if v is not None}


# --------------------------------------------------------------------------- interface

class PooldayClient(ABC):
    name = "abstract"
    automatic = True      # False: calls must be done by a human in the app
    pollable = True       # False: status only arrives by callback (webhook mode)

    def __init__(self):
        # Set by the caller to receive one record per HTTP call (pipeline writes it to
        # the api_calls table). Never receives the auth header.
        self.on_call: Callable[[dict], None] | None = None

    @abstractmethod
    def start_production(self, prompt: str, attachments: list[str] | None = None,
                         reference_url: str | None = None,
                         settings: dict | None = None, context: dict | None = None) -> Production:
        """New conversation: prompt text + optional files/reference link + mode/tier.
        `context` carries lead details (lead_id, company, token...) for clients that
        send structured payloads (webhook); the HTTP client ignores it."""

    @abstractmethod
    def send_message(self, production_id: str, text: str, context: dict | None = None) -> Production:
        """Follow-up in the SAME conversation (revision after 'regenerate with note')."""

    @abstractmethod
    def get_status(self, production_id: str) -> Production:
        """Poll: status, plus the agent's question when it needs input."""

    def get_result(self, production_id: str) -> Production:
        """Final video URL / preview / thumbnail. Defaults to the status call."""
        return self.get_status(production_id)

    def answer_question(self, production_id: str, answer: str,
                        question_id: str | None = None, context: dict | None = None) -> Production:
        """Reply to the agent's question. Defaults to a plain follow-up message."""
        return self.send_message(production_id, answer, context=context)

    def credits(self) -> dict | None:
        """Remaining credits/usage if the API exposes it, else None."""
        return None

    def describe(self) -> dict:
        return {"client": self.name, "automatic": self.automatic}


class ManualPooldayClient(PooldayClient):
    """No API: the loop shows the prompt, a human pastes it into Poolday and the link back."""
    name = "manual"
    automatic = False

    def _manual(self, what: str):
        raise ManualStep(f"No Poolday API configured: {what} by hand in the Poolday app.")

    def start_production(self, prompt, attachments=None, reference_url=None, settings=None, context=None):
        self._manual("paste the prompt")

    def send_message(self, production_id, text, context=None):
        self._manual("paste the revision into the same conversation")

    def get_status(self, production_id):
        self._manual("check the conversation")


# --------------------------------------------------------------------------- mapping

EXAMPLE_MAPPING = config.LOOP_DIR / "poolday_api.example.toml"


def load_mapping(path: str | Path | None = None) -> dict:
    """Read the mapping (.toml or .json). No network, no secrets in the file."""
    path = Path(path or config.POOLDAY_API_CONFIG)
    if not path.exists():
        raise PooldayNotConfigured(
            f"{path} not found. Copy {EXAMPLE_MAPPING.name} to {path.name} and fill it from "
            "the Poolday API docs (see loop/POOLDAY_API.md).")
    if path.suffix == ".json":
        return json.loads(path.read_text())
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:  # pragma: no cover
        try:
            import tomli as tomllib  # type: ignore
        except ModuleNotFoundError:
            raise PooldayNotConfigured("Reading TOML needs Python 3.11+ (or `pip install tomli`); "
                                       "or write the mapping as .json.") from None
    return tomllib.loads(path.read_text())


def placeholders(mapping: dict, prefix: str = "") -> list[str]:
    """Every value still containing TODO (the docs have not been applied there yet)."""
    out = []
    for k, v in mapping.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out += placeholders(v, key + ".")
        elif isinstance(v, list):
            out += [key for x in v if isinstance(x, str) and "TODO" in x][:1]
        elif isinstance(v, str) and "TODO" in v:
            out.append(key)
    return out


def dig(data, path: str):
    """Read a dotted path ('output.video.url', 'items.0.id', 'versions.-1.url') from JSON."""
    if not path:
        return None
    cur = data
    for part in path.split("."):
        if isinstance(cur, list) and part.lstrip("-").isdigit() and -len(cur) <= int(part) < len(cur):
            cur = cur[int(part)]  # "-1" = the last item (e.g. the latest version)
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def put(body: dict, path: str, value) -> None:
    """Write a dotted path into a request body ('settings.mode' -> {'settings': {'mode': ..}})."""
    if not path or value is None:
        return
    parts = path.split(".")
    cur = body
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def _truncate(obj, n: int = 600) -> str | None:
    if obj is None:
        return None
    s = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + f"… (+{len(s) - n} chars)"


# --------------------------------------------------------------------------- HTTP client

class HttpPooldayClient(PooldayClient):
    """Generic REST client. Knows nothing about Poolday until the mapping tells it."""
    name = "http"

    def __init__(self, mapping: dict | None = None, api_key: str | None = None,
                 base_url: str | None = None):
        super().__init__()
        self.m = mapping if mapping is not None else load_mapping()
        todo = placeholders(self.m)
        if todo:
            raise PooldayNotConfigured(
                "Poolday API mapping still has placeholders (fill from the API docs): "
                + ", ".join(todo))
        api = self.m.get("api", {})
        self.base_url = (base_url or os.environ.get("POOLDAY_BASE_URL") or api.get("base_url", "")).rstrip("/")
        self.timeout = float(api.get("timeout_s", 30))
        auth = self.m.get("auth", {})
        self.auth_header = auth.get("header", "Authorization")
        self.auth_scheme = auth.get("scheme", "Bearer")
        key_env = auth.get("key_env", "POOLDAY_API_KEY")
        self.api_key = api_key if api_key is not None else os.environ.get(key_env, "")
        if not self.base_url:
            raise PooldayNotConfigured("api.base_url is empty.")
        if not self.api_key:
            raise PooldayNotConfigured(f"Set {key_env} (the Poolday API key) in the environment.")
        self.ep = self.m.get("endpoints", {})
        missing = [op for op in REQUIRED_OPS if not self.ep.get(op)]
        if missing:
            raise PooldayNotConfigured("Missing endpoints: " + ", ".join(missing))
        self.req = self.m.get("request", {})
        self.res = self.m.get("response", {})
        self.defaults = self.m.get("defaults", {})
        self.status_map = {raw.lower(): ours for ours, raws in self.m.get("status_map", {}).items()
                           for raw in raws}

    def describe(self) -> dict:
        return {"client": self.name, "automatic": True, "base_url": self.base_url,
                "mode": self.defaults.get("mode"), "tier": self.defaults.get("tier")}

    # -- plumbing

    def _endpoint(self, op: str, pid: str | None = None) -> tuple[str, str]:
        spec = self.ep.get(op) or ""
        if not spec:
            raise PooldayNotConfigured(f"No endpoint mapped for '{op}'.")
        method, _, path = spec.strip().partition(" ")
        if pid is not None:
            path = path.replace("{id}", urllib.parse.quote(str(pid), safe=""))
        return method.upper(), path

    def _headers(self, content_type: str | None = "application/json") -> dict:
        value = f"{self.auth_scheme} {self.api_key}".strip() if self.auth_scheme else self.api_key
        h = {self.auth_header: value, "Accept": "application/json"}
        h.update(self.m.get("headers", {}))
        if content_type:
            h["Content-Type"] = content_type
        return h

    def _call(self, op: str, pid: str | None = None, body: dict | None = None,
              raw: bytes | None = None, content_type: str | None = None,
              log_body=None) -> dict:
        method, path = self._endpoint(op, pid)
        url = self.base_url + path
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        ctype = content_type or ("application/json" if body is not None else None)
        req = urllib.request.Request(url, data=data, method=method, headers=self._headers(ctype))
        t0 = time.monotonic()
        code, text, err = None, "", None
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                code, text = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code, text = e.code, e.read().decode("utf-8", "replace")
            err = e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            err = e
        ms = int((time.monotonic() - t0) * 1000)
        if self.on_call:
            self.on_call({"op": op, "method": method, "path": path, "http_status": code, "ms": ms,
                          "request": _truncate(log_body if log_body is not None else body),
                          "response": _truncate(text or (str(err) if err else None))})
        if code is None:
            raise PooldayError(f"{op}: could not reach {self.base_url} ({err})")
        if code == 429:
            ra = err.headers.get("Retry-After") if isinstance(err, urllib.error.HTTPError) else None
            raise PooldayRateLimited(f"{op}: rate limited (HTTP 429)",
                                     float(ra) if ra and ra.replace(".", "").isdigit() else None)
        if code in (401, 403):
            raise PooldayError(f"{op}: HTTP {code}, the Poolday API key was rejected")
        if code >= 400:
            raise PooldayError(f"{op}: HTTP {code}: {text[:300]}")
        try:
            return json.loads(text) if text.strip() else {}
        except json.JSONDecodeError as exc:
            raise PooldayError(f"{op}: response is not JSON: {text[:200]}") from exc

    def _production(self, data: dict, pid: str | None = None) -> Production:
        r = self.res
        raw_status = dig(data, r.get("status", ""))
        status = self.status_map.get(str(raw_status).lower(), "running") if raw_status is not None else "running"
        p = Production(
            id=str(dig(data, r.get("id", "")) or pid or "") or None,
            status=status, raw_status=None if raw_status is None else str(raw_status),
            question=dig(data, r.get("question", "")),
            question_id=dig(data, r.get("question_id", "")),
            video_url=dig(data, r.get("video_url", "")),
            preview_url=dig(data, r.get("preview_url", "")),
            thumbnail_url=dig(data, r.get("thumbnail_url", "")),
            error=dig(data, r.get("error", "")),
            raw=data)
        if p.question and p.status not in ("done", "failed"):
            p.status = "needs_input"  # a pending question wins over a generic "running"
        return p

    def _upload(self, path: str) -> str:
        """Multipart upload of one file; returns the file id the start call references."""
        p = Path(path)
        boundary = uuid.uuid4().hex
        fieldname = self.req.get("upload_file", "file")
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        payload = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{fieldname}\"; "
                   f"filename=\"{p.name}\"\r\nContent-Type: {ctype}\r\n\r\n").encode() \
            + p.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        data = self._call("upload", raw=payload, content_type=f"multipart/form-data; boundary={boundary}",
                          log_body={"file": p.name, "bytes": p.stat().st_size})
        fid = dig(data, self.res.get("upload_id", "id"))
        if not fid:
            raise PooldayError(f"upload: no file id at '{self.res.get('upload_id', 'id')}' in the response")
        return str(fid)

    # -- operations

    def start_production(self, prompt, attachments=None, reference_url=None, settings=None, context=None):
        settings = {**self.defaults, **(settings or {})}
        body: dict = dict(self.m.get("request_extra", {}))
        put(body, self.req.get("prompt", "prompt"), prompt)
        put(body, self.req.get("mode", ""), settings.get("mode"))
        put(body, self.req.get("tier", ""), settings.get("tier"))
        put(body, self.req.get("aspect_ratio", ""), settings.get("aspect_ratio"))
        put(body, self.req.get("title", ""), settings.get("title"))
        if reference_url:
            if self.req.get("reference_url"):
                put(body, self.req["reference_url"], reference_url)
            elif reference_url not in prompt:  # no dedicated field: Poolday reads links in the text
                put(body, self.req.get("prompt", "prompt"), f"{prompt}\nReference: {reference_url}")
        if attachments:
            if not self.ep.get("upload") or not self.req.get("attachments"):
                raise PooldayNotConfigured("Attachments need endpoints.upload and request.attachments.")
            put(body, self.req["attachments"], [self._upload(a) for a in attachments])
        log_body = dict(body)
        return self._production(self._call("start", body=body, log_body=log_body))

    def send_message(self, production_id, text, context=None):
        body: dict = {}
        put(body, self.req.get("message_text", "message"), text)
        data = self._call("message", production_id, body=body)
        return self._production(data, production_id)

    def answer_question(self, production_id, answer, question_id=None, context=None):
        if not self.ep.get("answer"):
            return self.send_message(production_id, answer)
        body: dict = {}
        put(body, self.req.get("answer_text", "answer"), answer)
        put(body, self.req.get("question_id", ""), question_id)
        return self._production(self._call("answer", production_id, body=body), production_id)

    def get_status(self, production_id):
        return self._production(self._call("status", production_id), production_id)

    def get_result(self, production_id):
        if not self.ep.get("result"):
            return self.get_status(production_id)
        return self._production(self._call("result", production_id), production_id)

    def credits(self):
        if not self.ep.get("credits"):
            return None
        data = self._call("credits")
        return {"remaining": dig(data, self.res.get("credits_remaining", "")),
                "used": dig(data, self.res.get("credits_used", ""))}


class FakePooldayClient(HttpPooldayClient):
    """The real HTTP client, driven by the fake server's mapping (see poolday_fake.py)."""
    name = "fake"

    def __init__(self, base_url: str | None = None):
        from . import poolday_fake
        url = base_url or poolday_fake.ensure_server()
        super().__init__(poolday_fake.FAKE_MAPPING, api_key=poolday_fake.FAKE_KEY, base_url=url)

    def describe(self) -> dict:
        return {**super().describe(), "client": "fake"}


# --------------------------------------------------------------------------- webhook client
#
# Poolday's agent creates an inbound webhook that triggers a saved prompt, and calls a URL
# of ours back with the outputs when the conversation is done. We don't know the exact
# payload shapes Poolday will use, so: our outbound payload is plain, documented JSON (the
# agent is told to accept it), and the callback parser looks for each value under a list
# of candidate keys that can be extended without code changes (env or the [webhook]
# section of poolday_api.toml).

CALLBACK_PATH = "/api/poolday/callback"

# Candidate dotted paths per value, tried in order. "*" expands every item of a list; a
# list item that is an asset dict gives its url/video_url/src, unless its type says image.
# Each path is tried on the payload root, then inside each ENVELOPE (data, payload, ...).
DEFAULT_CALLBACK_KEYS: dict[str, list[str]] = {
    "lead_id": ["lead_id", "leadId", "lead.id", "lead"],
    "token": ["token", "callback_token", "lead_token"],
    "status": ["status", "state", "result.status", "event"],
    "video_url": ["video_url", "videoUrl", "video.url", "video", "result.video", "result.video_url",
                  "result.url", "output.video_url", "output.url", "outputs.*", "assets.*", "videos.*",
                  "files.*", "download_url", "share_url", "url"],
    "thumbnail_url": ["thumbnail_url", "thumbnailUrl", "thumbnail", "poster_url", "result.thumbnail"],
    "conversation_url": ["conversation_url", "conversationUrl", "conversation.url", "chat_url",
                         "thread_url", "run_url"],
    "question": ["question", "question.text", "pending_question", "needs_input.question",
                 "input_request", "message_to_user"],
    "message": ["message", "text", "summary"],     # used as the question when status = needs_input
    "error": ["error", "error.message", "error_message", "failure", "reason"],
    "production_id": ["conversation_id", "conversationId", "run_id", "job_id", "production_id", "id"],
    "version": ["version", "video_version"],
}
DEFAULT_ENVELOPES = ["data", "payload", "body", "result", "output", "event.data", "metadata",
                     "inputs", "input"]
# Poolday status strings -> ours. Exact (case-insensitive) match first, then the
# substring heuristics in `map_status`. Extend in [webhook.status_map].
DEFAULT_WEBHOOK_STATUS_MAP = {
    "done": ["done", "completed", "complete", "success", "succeeded", "finished", "ready"],
    "failed": ["failed", "failure", "error", "errored", "cancelled", "canceled"],
    "needs_input": ["needs_input", "waiting_for_user", "question", "input_required", "awaiting_input"],
    "queued": ["queued", "pending", "received", "accepted"],
    "running": ["running", "in_progress", "processing", "started", "working"],
}
SENSITIVE_KEYS = re.compile(r"secret|token|password|passwd|api[_-]?key|authorization|signature|cookie",
                            re.I)
VIDEO_EXT = re.compile(r"\.(mp4|mov|webm|m4v|m3u8)(\?|#|$)", re.I)
IMAGE_EXT = re.compile(r"\.(png|jpe?g|gif|webp|svg|avif)(\?|#|$)", re.I)
URL_ONLY = re.compile(r"^https?://\S+$")


def _json_env(name: str) -> dict:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return {}
    try:
        val = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PooldayNotConfigured(f"{name} is not valid JSON: {exc}") from None
    return val if isinstance(val, dict) else {}


def webhook_settings() -> dict:
    """Webhook config: environment first, then the optional [webhook] section of the
    mapping file, then defaults. Secrets come from the environment only."""
    section: dict = {}
    try:
        if Path(config.POOLDAY_API_CONFIG).exists():
            section = load_mapping(config.POOLDAY_API_CONFIG).get("webhook", {}) or {}
    except (PooldayError, ValueError, OSError):
        section = {}
    env = os.environ.get
    keys = {k: list(v) for k, v in DEFAULT_CALLBACK_KEYS.items()}
    for src in (section.get("keys") or {}, _json_env("POOLDAY_CALLBACK_KEYS")):
        for k, v in src.items():  # configured paths are tried BEFORE the defaults
            v = [v] if isinstance(v, str) else list(v)
            keys[k] = v + [x for x in keys.get(k, []) if x not in v]
    status_map = {k: list(v) for k, v in DEFAULT_WEBHOOK_STATUS_MAP.items()}
    for k, v in (section.get("status_map") or {}).items():
        status_map.setdefault(k, [])
        status_map[k] = list(v) + status_map[k]
    public = (env("PUBLIC_BASE_URL") or section.get("public_base_url") or "").strip().rstrip("/")
    secret = env("POOLDAY_WEBHOOK_SECRET", "")
    return {
        "url": (env("POOLDAY_WEBHOOK_URL") or section.get("url") or "").strip(),
        "secret": secret,
        # Optional separate secret for the callback; defaults to the same shared secret.
        "callback_secret": env("POOLDAY_CALLBACK_SECRET", "") or secret,
        "secret_header": env("POOLDAY_WEBHOOK_SECRET_HEADER") or section.get("secret_header")
        or "X-Webhook-Secret",
        "secret_field": env("POOLDAY_WEBHOOK_SECRET_FIELD") or section.get("secret_field") or "secret",
        "public_base_url": public,
        "callback_url": public + CALLBACK_PATH if public else "",
        "timeout_s": float(env("POOLDAY_WEBHOOK_TIMEOUT_S") or section.get("timeout_s") or 30),
        "extra": {**(section.get("extra") or {}), **_json_env("POOLDAY_WEBHOOK_EXTRA")},
        "keys": keys,
        "envelopes": list(section.get("envelopes") or DEFAULT_ENVELOPES),
        "status_map": status_map,
    }


def dig_all(data, path: str) -> list:
    """Like `dig`, but '*' expands every item of a list: 'outputs.*.url' -> all urls."""
    if not path:
        return []
    cur = [data]
    for part in path.split("."):
        nxt = []
        for c in cur:
            if part == "*" and isinstance(c, list):
                nxt += c
            elif part == "*" and isinstance(c, dict):
                nxt += list(c.values())
            else:
                v = dig(c, part)
                if v is not None:
                    nxt.append(v)
        cur = nxt
    return [c for c in cur if c is not None and c != ""]


def _scopes(payload: dict, envelopes: list[str]) -> list:
    out = [payload]
    for e in envelopes:
        v = dig(payload, e)
        if isinstance(v, dict) and v is not payload:
            out.append(v)
    return out


def _first(payload, paths, envelopes, want=(str, int, float)):
    for scope in _scopes(payload, envelopes):
        for p in paths:
            for v in dig_all(scope, p):
                if isinstance(v, want) and not isinstance(v, bool) and str(v).strip():
                    return v
    return None


def _urls_from(value) -> list[str]:
    """URL strings from a value: a string, an asset dict (skipping images), or a list."""
    if isinstance(value, str):
        return [value.strip()] if URL_ONLY.match(value.strip()) else []
    if isinstance(value, list):
        return [u for v in value for u in _urls_from(v)]
    if isinstance(value, dict):
        kind = str(value.get("type") or value.get("kind") or value.get("mime_type")
                   or value.get("content_type") or "").lower()
        if any(w in kind for w in ("image", "thumbnail", "audio", "poster")):
            return []
        for k in ("video_url", "url", "src", "href", "download_url", "share_url"):
            if isinstance(value.get(k), str):
                return _urls_from(value[k])
    return []


def _deep_video_urls(value) -> list[str]:
    """Last resort: every string anywhere in the payload that is a video-file URL."""
    if isinstance(value, str):
        return [value] if URL_ONLY.match(value) and VIDEO_EXT.search(value) else []
    if isinstance(value, dict):
        return [u for v in value.values() for u in _deep_video_urls(v)]
    if isinstance(value, list):
        return [u for v in value for u in _deep_video_urls(v)]
    return []


def map_status(raw, status_map: dict) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip().lower()
    for ours, raws in status_map.items():
        if s in (r.lower() for r in raws):
            return ours
    for ours, words in (("failed", ("fail", "error", "cancel")),
                        ("needs_input", ("input", "question", "waiting", "clarif")),
                        ("done", ("complet", "done", "success", "finish", "ready")),
                        ("queued", ("queue", "pending", "received")),
                        ("running", ("run", "progress", "process", "start", "working"))):
        if any(w in s for w in words):
            return ours
    return None


def parse_callback(payload, settings: dict | None = None) -> dict:
    """Pull what the loop needs out of whatever JSON Poolday posts back."""
    st = settings or webhook_settings()
    keys, env = st["keys"], st["envelopes"]
    if not isinstance(payload, dict):
        payload = {"items": payload} if isinstance(payload, list) else {"text": str(payload)}
    # A nested JSON document sent as a string ({"payload": "{...}"}) is unpacked.
    for k in list(env) + ["text"]:
        v = payload.get(k) if "." not in k else None
        if isinstance(v, str) and v.strip()[:1] in "{[":
            try:
                payload = {**payload, k: json.loads(v)}
            except json.JSONDecodeError:
                pass
    raw_lead = _first(payload, keys["lead_id"], env)
    lead_id = None
    if raw_lead is not None:
        m = re.search(r"\d+", str(raw_lead))
        lead_id = int(m.group()) if m else None
    raw_status = _first(payload, keys["status"], env, want=(str,))
    status = map_status(raw_status, st["status_map"])
    conversation_url = _first(payload, keys["conversation_url"], env, want=(str,))
    candidates: list[str] = []
    for scope in _scopes(payload, env):
        for p in keys["video_url"]:
            for v in dig_all(scope, p):
                candidates += _urls_from(v)
    candidates += _deep_video_urls(payload)
    seen, videos = set(), []
    for u in candidates:
        if u not in seen and u != conversation_url and not IMAGE_EXT.search(u):
            seen.add(u)
            videos.append(u)
    videos.sort(key=lambda u: 0 if VIDEO_EXT.search(u) else 1)  # stable: order kept otherwise
    question = _first(payload, keys["question"], env, want=(str,))
    if not question and status == "needs_input":
        question = _first(payload, keys["message"], env, want=(str,))
    error = _first(payload, keys["error"], env, want=(str,))
    version = _first(payload, keys["version"], env)
    try:
        version = int(re.search(r"\d+", str(version)).group()) if version is not None else None
    except AttributeError:
        version = None
    if status is None:
        status = "done" if videos else "needs_input" if question else "failed" if error else None
    elif question and not videos and status in ("queued", "running"):
        status = "needs_input"  # a pending question wins over a generic "running"
    if status == "needs_input" and not question:
        question = "(Poolday asked for input without a question text: open the conversation)"
    return {
        "lead_id": lead_id,
        "token": _first(payload, keys["token"], env, want=(str,)),
        "status": status, "raw_status": None if raw_status is None else str(raw_status),
        "video_url": videos[0] if videos else None, "video_urls": videos,
        "thumbnail_url": _first(payload, keys["thumbnail_url"], env, want=(str,)),
        "conversation_url": conversation_url,
        "question": question, "error": error, "version": version,
        "remote_id": _first(payload, keys["production_id"], env),
        "secret": _first(payload, [st["secret_field"]], env, want=(str,)),
    }


def redact(obj, secrets: list[str] | tuple = ()):
    """Copy of obj with sensitive keys and any known secret value replaced."""
    secrets = [s for s in secrets if s and len(s) >= 4]

    def scrub_str(s: str) -> str:
        for sec in secrets:
            s = s.replace(sec, "[redacted]")
        return s
    if isinstance(obj, dict):
        return {k: "[redacted]" if SENSITIVE_KEYS.search(str(k)) and v not in (None, "")
                else redact(v, secrets) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v, secrets) for v in obj]
    if isinstance(obj, str):
        return scrub_str(obj)
    return obj


def mask_url(url: str) -> str:
    """Scheme + host + path with long (likely secret) path segments masked; no query."""
    u = urllib.parse.urlsplit(url)
    segs = [s if len(s) < 12 else "…" + s[-4:] for s in u.path.split("/")]
    return f"{u.scheme}://{u.netloc}{'/'.join(segs)}" + ("?[query redacted]" if u.query else "")


def secrets_equal(a: str | None, b: str | None) -> bool:
    return bool(a) and bool(b) and hmac.compare_digest(str(a).encode(), str(b).encode())


class WebhookPooldayClient(PooldayClient):
    """POSTs a lead to Poolday's inbound webhook (created by the Poolday agent, triggering a
    saved prompt). Status comes back ONLY through our callback endpoint, so it is not
    pollable. Nothing about Poolday's side is assumed beyond "accepts a JSON POST"."""
    name = "webhook"
    pollable = False

    def __init__(self, settings: dict | None = None):
        super().__init__()
        self.s = settings or webhook_settings()
        missing = [n for n, v in (("POOLDAY_WEBHOOK_URL", self.s["url"]),
                                  ("POOLDAY_WEBHOOK_SECRET", self.s["secret"]),
                                  ("PUBLIC_BASE_URL", self.s["public_base_url"])) if not v]
        if missing:
            raise PooldayNotConfigured("Webhook mode needs " + ", ".join(missing)
                                       + " (see README: Poolday via webhook).")
        if not URL_ONLY.match(self.s["url"]):
            raise PooldayNotConfigured("POOLDAY_WEBHOOK_URL must be a full http(s) URL.")
        self.callback_url = self.s["callback_url"]

    def describe(self) -> dict:
        return {"client": self.name, "automatic": True, "pollable": False,
                "webhook": mask_url(self.s["url"]), "callback_url": self.callback_url,
                "secret_header": self.s["secret_header"]}

    def _post(self, op: str, body: dict) -> dict:
        body = {**self.s["extra"], **body}
        data = json.dumps(body).encode()
        headers = {"Content-Type": "application/json", "Accept": "application/json",
                   self.s["secret_header"]: self.s["secret"]}
        req = urllib.request.Request(self.s["url"], data=data, method="POST", headers=headers)
        t0 = time.monotonic()
        code, text, err = None, "", None
        try:
            with urllib.request.urlopen(req, timeout=self.s["timeout_s"]) as r:
                code, text = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code, text, err = e.code, e.read().decode("utf-8", "replace"), e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            err = e
        ms = int((time.monotonic() - t0) * 1000)
        secrets = [self.s["secret"], self.s["callback_secret"], body.get("token") or ""]
        if self.on_call:
            self.on_call({"op": op, "method": "POST", "path": mask_url(self.s["url"]),
                          "http_status": code, "ms": ms,
                          "request": _truncate(redact(body, secrets), 2000),
                          "response": _truncate(redact(text or (str(err) if err else ""), secrets))})
        if code is None:
            raise PooldayError(f"{op}: could not reach the Poolday webhook ({err})")
        if code == 429:
            raise PooldayRateLimited(f"{op}: rate limited (HTTP 429)")
        if code in (401, 403):
            raise PooldayError(f"{op}: HTTP {code}, the Poolday webhook rejected our secret "
                               f"(header {self.s['secret_header']})")
        if code >= 400:
            raise PooldayError(f"{op}: HTTP {code}: {redact(text, secrets)[:300]}")
        try:
            return json.loads(text) if text.strip() else {}
        except json.JSONDecodeError:
            return {"text": text}  # a plain "ok" is fine: the outputs come by callback

    def _production(self, resp, ctx: dict, status: str, raw_status: str) -> Production:
        parsed = parse_callback(resp, self.s) if isinstance(resp, dict) else {}
        pid = parsed.get("remote_id") or f"wh-{ctx.get('lead_id')}-{str(ctx.get('token', ''))[:6]}"
        return Production(id=str(pid), status=status, raw_status=raw_status, raw=resp or {})

    def _base(self, ctx: dict, kind: str) -> dict:
        if not ctx.get("lead_id") or not ctx.get("token"):
            raise PooldayError("webhook: the lead id and token are required (pipeline bug)")
        return {"kind": kind, "lead_id": ctx["lead_id"], "token": ctx["token"],
                "version": ctx.get("version"), "callback_url": self.callback_url}

    def start_production(self, prompt, attachments=None, reference_url=None, settings=None, context=None):
        ctx = context or {}
        body = self._base(ctx, "start")
        body.update({k: ctx.get(k) for k in ("company", "website", "brand_kit_name", "angle",
                                             "contact_name", "contact_role") if ctx.get(k)})
        body["reference_url"] = reference_url
        body["prompt"] = prompt
        if settings:
            body.update({k: settings[k] for k in ("mode", "tier", "title") if settings.get(k)})
        # Files are not sent: the Poolday agent uses the skills saved in the workspace.
        return self._production(self._post("start", body), ctx, "queued", "sent")

    def send_message(self, production_id, text, context=None):
        ctx = context or {}
        body = self._base(ctx, "revision")
        body.update(production_id=production_id, note=ctx.get("note") or text, message=text)
        return self._production(self._post("message", body), ctx, "running", "revision sent")

    def answer_question(self, production_id, answer, question_id=None, context=None):
        ctx = context or {}
        body = self._base(ctx, "answer")
        body.update(production_id=production_id, answer=answer, note=answer,
                    question=ctx.get("question"), question_id=question_id)
        return self._production(self._post("answer", body), ctx, "running", "answer sent")

    def get_status(self, production_id):
        raise PooldayError("webhook mode: status arrives by callback, nothing to poll")


# --------------------------------------------------------------------------- factory

def get_client() -> PooldayClient:
    """POOLDAY_API=manual|fake|http|webhook (auto: see config.poolday_mode)."""
    mode = config.poolday_mode()
    if mode == "webhook":
        return WebhookPooldayClient()
    if mode == "fake":
        return FakePooldayClient(os.environ.get("POOLDAY_FAKE_URL") or None)
    if mode == "http":
        return HttpPooldayClient()
    return ManualPooldayClient()


def status_line() -> dict:
    """For the dashboard header: which client, configured or not, and why not."""
    try:
        c = get_client()
        return {**c.describe(), "ok": True}
    except PooldayError as exc:
        return {"client": config.poolday_mode(), "automatic": False, "ok": False, "error": str(exc)}
