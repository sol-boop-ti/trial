"""Poolday API integration: one interface, three implementations.

    PooldayClient          the operations the loop needs (abstract)
    HttpPooldayClient      real HTTP; every URL, header, path and field name comes from a
                           mapping file (poolday_api.toml) that is filled from Poolday's API docs
    ManualPooldayClient    the copy/paste flow (no API): the human is the transport
    FakePooldayClient      HttpPooldayClient pointed at the local fake server in
                           poolday_fake.py (async runs, a question mid-run, a video URL)

Nothing here encodes a real Poolday endpoint. Until the docs arrive, the mapping file is
a template of placeholders (see poolday_api.example.toml and POOLDAY_API.md).

Status vocabulary used by the rest of the loop (Poolday's own strings are mapped onto it):
    queued · running · needs_input · done · failed
"""
from __future__ import annotations

import json
import mimetypes
import os
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

    def __init__(self):
        # Set by the caller to receive one record per HTTP call (pipeline writes it to
        # the api_calls table). Never receives the auth header.
        self.on_call: Callable[[dict], None] | None = None

    @abstractmethod
    def start_production(self, prompt: str, attachments: list[str] | None = None,
                         reference_url: str | None = None,
                         settings: dict | None = None) -> Production:
        """New conversation: prompt text + optional files/reference link + mode/tier."""

    @abstractmethod
    def send_message(self, production_id: str, text: str) -> Production:
        """Follow-up in the SAME conversation (revision after 'regenerate with note')."""

    @abstractmethod
    def get_status(self, production_id: str) -> Production:
        """Poll: status, plus the agent's question when it needs input."""

    def get_result(self, production_id: str) -> Production:
        """Final video URL / preview / thumbnail. Defaults to the status call."""
        return self.get_status(production_id)

    def answer_question(self, production_id: str, answer: str,
                        question_id: str | None = None) -> Production:
        """Reply to the agent's question. Defaults to a plain follow-up message."""
        return self.send_message(production_id, answer)

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

    def start_production(self, prompt, attachments=None, reference_url=None, settings=None):
        self._manual("paste the prompt")

    def send_message(self, production_id, text):
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
    """Read a dotted path ('output.video.url', 'items.0.id') from a JSON response."""
    if not path:
        return None
    cur = data
    for part in path.split("."):
        if isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
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

    def start_production(self, prompt, attachments=None, reference_url=None, settings=None):
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

    def send_message(self, production_id, text):
        body: dict = {}
        put(body, self.req.get("message_text", "message"), text)
        data = self._call("message", production_id, body=body)
        return self._production(data, production_id)

    def answer_question(self, production_id, answer, question_id=None):
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


# --------------------------------------------------------------------------- factory

def get_client() -> PooldayClient:
    """POOLDAY_API=manual|fake|http (auto: http when a filled mapping + key exist)."""
    mode = config.poolday_mode()
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
