"""A local fake Poolday API for tests and demos. NOT Poolday's real API.

It invents its own paths (/fake/v0/...), field names and status strings on purpose,
so the generic HttpPooldayClient is exercised through a mapping exactly as it will be
with the real docs: nested response fields, status strings that need mapping, a
different auth header, multipart upload.

Simulated run (Align mode): in_queue -> working -> waiting_for_user (one question, like
the Reference Teaser skill's single gate) -> [answer] -> working -> completed (video URL).
A follow-up message on a completed run is a revision: working -> completed with v2, v3...
A prompt containing "[fail]" ends in `error`. Build mode skips the question.

Timing: each phase lasts FAKE_POOLDAY_STEP_S seconds (default 2). With 0, every
status poll advances exactly one phase (deterministic, used by the tests).

Run standalone:  python -m prospect_loop fake-poolday --port 8766
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FAKE_KEY = "fake-poolday-key"

# The same structure as poolday_api.example.toml, filled for the fake server.
FAKE_MAPPING = {
    "api": {"base_url": "http://127.0.0.1:8766", "timeout_s": 10},
    "auth": {"header": "X-Fake-Key", "scheme": "", "key_env": "FAKE_POOLDAY_KEY"},
    "endpoints": {
        "start": "POST /fake/v0/productions",
        "message": "POST /fake/v0/productions/{id}/messages",
        "answer": "POST /fake/v0/productions/{id}/answers",
        "status": "GET /fake/v0/productions/{id}",
        "result": "GET /fake/v0/productions/{id}/result",
        "upload": "POST /fake/v0/files",
        "credits": "GET /fake/v0/credits",
    },
    "request": {
        "prompt": "input.text", "mode": "settings.mode", "tier": "settings.tier",
        "aspect_ratio": "settings.aspect_ratio", "title": "title",
        "reference_url": "input.reference_url", "attachments": "input.file_ids",
        "message_text": "text", "answer_text": "text", "question_id": "question_id",
        "upload_file": "file",
    },
    "request_extra": {"kind": "video"},
    "defaults": {"mode": "align", "tier": "standard", "aspect_ratio": "16:9"},
    "response": {
        "id": "production.id", "status": "production.state",
        "question": "pending_question.text", "question_id": "pending_question.id",
        "video_url": "output.video_url", "preview_url": "output.preview_url",
        "thumbnail_url": "output.thumbnail_url", "error": "failure.reason",
        "upload_id": "file.id",
        "credits_remaining": "balance.remaining", "credits_used": "balance.used",
    },
    "status_map": {
        "queued": ["in_queue"], "running": ["working"], "needs_input": ["waiting_for_user"],
        "done": ["completed"], "failed": ["error"],
    },
}

TIER_COST = {"micro": 5, "light": 15, "standard": 40, "max": 120, "ultra": 200}
QUESTION = ("Script and 3 keyframes are ready next to the reference frames, plus a 3s test "
            "render. Routing: Remotion for the UI rows, Seedance for the camera move. Go ahead "
            "with the 20s 16:9 cut as drafted, or change anything first?")


class _State:
    def __init__(self):
        self.lock = threading.Lock()
        self.prods: dict[str, dict] = {}
        self.files: dict[str, dict] = {}
        self.credits = 2000
        self.used = 0


def _step_s() -> float:
    return float(os.environ.get("FAKE_POOLDAY_STEP_S", "2"))


def _advance(p: dict) -> None:
    """Move through queued phases (time-based, or one per poll when step is 0)."""
    step = _step_s()
    while p["queue"] and p["state"] != "waiting_for_user":
        if step > 0 and time.time() - p["since"] < step:
            return
        p["state"] = p["queue"].pop(0)
        p["since"] = time.time()
        if p["state"] == "waiting_for_user":
            p["question"] = {"id": "q_" + uuid.uuid4().hex[:6], "text": QUESTION}
        if p["state"] == "completed":
            p["output"] = {"video_url": f"{p['base']}/fake/v0/watch/{p['id']}/v{p['version']}",
                           "preview_url": f"{p['base']}/fake/v0/watch/{p['id']}/v{p['version']}?preview=1",
                           "thumbnail_url": f"{p['base']}/fake/v0/watch/{p['id']}/v{p['version']}.jpg"}
        if step == 0:
            return


def _view(p: dict) -> dict:
    return {"production": {"id": p["id"], "state": p["state"], "version": p["version"],
                           "mode": p["mode"], "tier": p["tier"]},
            "pending_question": p.get("question") if p["state"] == "waiting_for_user" else None,
            "output": p.get("output") if p["state"] == "completed" else None,
            "failure": {"reason": "render failed (simulated)"} if p["state"] == "error" else None,
            "messages": len(p["messages"])}


def make_handler(state: _State):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _send(self, code, body, ctype="application/json"):
            data = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _authed(self) -> bool:
            if self.headers.get("X-Fake-Key") != FAKE_KEY:
                self._send(401, {"error": "bad key"})
                return False
            return True

        def _json(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n) or b"{}") if n else {}

        def _base(self) -> str:
            return f"http://{self.headers.get('Host')}"

        def do_GET(self):
            m = re.match(r"^/fake/v0/watch/([\w-]+)/v(\d+)(\.jpg)?", self.path)
            if m:  # public "video page", so the link in the gate is clickable
                with state.lock:
                    p = state.prods.get(m.group(1))
                if not p:
                    return self._send(404, b"no such video", "text/plain")
                html = (f"<!doctype html><meta charset=utf-8><title>Fake Poolday video</title>"
                        f"<body style='font:16px system-ui;padding:40px;max-width:720px'>"
                        f"<h1>Fake Poolday video · v{m.group(2)}</h1><p>Simulated output of the "
                        f"local fake API. Production <code>{p['id']}</code>.</p><h3>Prompt</h3>"
                        f"<pre style='white-space:pre-wrap'>{_esc(p['prompt'])}</pre>"
                        + "".join(f"<h3>Message {i + 1}</h3><pre style='white-space:pre-wrap'>{_esc(t)}</pre>"
                                  for i, t in enumerate(p["messages"])))
                return self._send(200, html.encode(), "text/html; charset=utf-8")
            if not self._authed():
                return
            if self.path == "/fake/v0/credits":
                with state.lock:
                    return self._send(200, {"balance": {"remaining": state.credits, "used": state.used}})
            m = re.match(r"^/fake/v0/productions/([\w-]+)(/result)?$", self.path)
            if not m:
                return self._send(404, {"error": "not found"})
            with state.lock:
                p = state.prods.get(m.group(1))
                if not p:
                    return self._send(404, {"error": "no such production"})
                if not m.group(2):
                    _advance(p)
                elif p["state"] != "completed":
                    return self._send(409, {"error": "not completed yet", "state": p["state"]})
                return self._send(200, _view(p))

        def do_POST(self):
            if not self._authed():
                return
            if self.path == "/fake/v0/files":
                n = int(self.headers.get("Content-Length") or 0)
                blob = self.rfile.read(n)
                fid = "file_" + uuid.uuid4().hex[:8]
                with state.lock:
                    state.files[fid] = {"bytes": len(blob)}
                return self._send(200, {"file": {"id": fid, "bytes": len(blob)}})
            body = self._json()
            if self.path == "/fake/v0/productions":
                text = (body.get("input") or {}).get("text")
                if not text:
                    return self._send(400, {"error": "input.text is required"})
                settings = body.get("settings") or {}
                mode, tier = settings.get("mode", "align"), settings.get("tier", "standard")
                queue = ["in_queue", "working"]
                queue += ["error"] if "[fail]" in text else (
                    ["waiting_for_user"] if mode == "align" else ["working", "completed"])
                pid = "prod_" + uuid.uuid4().hex[:10]
                p = {"id": pid, "prompt": text, "mode": mode, "tier": tier, "state": "in_queue",
                     "queue": queue[1:], "since": time.time(), "version": 1, "messages": [],
                     "base": self._base(), "files": (body.get("input") or {}).get("file_ids") or []}
                with state.lock:
                    state.prods[pid] = p
                    cost = TIER_COST.get(tier, 40)
                    state.credits -= cost
                    state.used += cost
                    return self._send(201, _view(p))
            m = re.match(r"^/fake/v0/productions/([\w-]+)/(messages|answers)$", self.path)
            if not m:
                return self._send(404, {"error": "not found"})
            text = (body.get("text") or "").strip()
            if not text:
                return self._send(400, {"error": "text is required"})
            with state.lock:
                p = state.prods.get(m.group(1))
                if not p:
                    return self._send(404, {"error": "no such production"})
                p["messages"].append(text)
                if p["state"] == "waiting_for_user":          # an answer
                    p["question"] = None
                    p["state"], p["queue"] = "working", ["completed"]
                elif p["state"] == "completed":               # a revision -> next version
                    p["version"] += 1
                    p["state"], p["queue"] = "working", ["completed"]
                    state.credits -= 10
                    state.used += 10
                elif m.group(2) == "answers":
                    return self._send(409, {"error": "no pending question"})
                p["since"] = time.time()
                return self._send(200, _view(p))
    return Handler


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def start_server(port: int = 0, host: str = "127.0.0.1") -> tuple[ThreadingHTTPServer, str]:
    httpd = ThreadingHTTPServer((host, port), make_handler(_State()))
    threading.Thread(target=httpd.serve_forever, daemon=True, name="fake-poolday").start()
    return httpd, f"http://{host}:{httpd.server_address[1]}"


_SINGLETON: dict = {}
_SINGLETON_LOCK = threading.Lock()


def _alive(url: str) -> bool:
    try:
        urllib.request.urlopen(url + "/fake/v0/credits", timeout=1)
    except urllib.error.HTTPError as e:  # 401 without the key: it is up
        return e.code == 401
    except OSError:
        return False
    return True


def ensure_server() -> str:
    """URL of a running fake server: POOLDAY_FAKE_URL if it answers, else one in this process."""
    env = os.environ.get("POOLDAY_FAKE_URL")
    if env and _alive(env.rstrip("/")):
        return env.rstrip("/")
    with _SINGLETON_LOCK:
        if "url" not in _SINGLETON:
            _SINGLETON["httpd"], _SINGLETON["url"] = start_server()
        return _SINGLETON["url"]


def serve_forever(port: int = 8766) -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(_State()))
    print(f"Fake Poolday API on http://127.0.0.1:{port} (step {_step_s()}s). "
          f"Use POOLDAY_API=fake POOLDAY_FAKE_URL=http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
