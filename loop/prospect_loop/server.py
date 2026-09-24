"""Local review dashboard (stdlib only). http://127.0.0.1:8765"""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import config, pipeline, store

PAGE = Path(__file__).with_name("dashboard.html")
ROUTE = re.compile(r"^/api/leads/(\d+)/(video|approve|reject|regenerate|email|redraft)$")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter console
        pass

    def _send(self, code: int, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def do_GET(self):
        conn = store.connect()
        try:
            if self.path in ("/", "/index.html"):
                return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
            if self.path == "/api/meta":
                return self._send(200, {"mode": config.llm_mode(), "model": config.MODEL,
                                        "threshold": config.QUALIFY_THRESHOLD,
                                        "out_dir": str(config.OUT_DIR)})
            if self.path == "/api/leads":
                return self._send(200, store.all_leads(conn))
            m = re.match(r"^/api/leads/(\d+)$", self.path)
            if m:
                lead = store.get(conn, int(m.group(1)))
                lead["events"] = store.events(conn, lead["id"])
                return self._send(200, lead)
            self._send(404, {"error": "not found"})
        except KeyError as exc:
            self._send(404, {"error": str(exc.args[0])})
        finally:
            conn.close()

    def do_POST(self):
        conn = store.connect()
        try:
            body = self._body()
            if self.path == "/api/run":
                ing = pipeline.ingest(conn)
                q = pipeline.qualify_all(conn)
                return self._send(200, {"ingest": ing, "qualify": q})
            if self.path == "/api/export":
                return self._send(200, pipeline.export(conn))
            m = ROUTE.match(self.path)
            if not m:
                return self._send(404, {"error": "not found"})
            lid, action = int(m.group(1)), m.group(2)
            note = (body.get("note") or "").strip()
            if action == "video":
                lead = pipeline.submit_video(conn, lid, body.get("url", ""))
            elif action == "approve":
                lead = pipeline.approve(conn, lid, note)
            elif action == "reject":
                lead = pipeline.reject(conn, lid, note)
            elif action == "regenerate":
                lead = pipeline.regenerate(conn, lid, note)
            elif action == "email":
                lead = pipeline.save_email(conn, lid, body.get("subject", ""), body.get("body", ""))
            else:
                lead = pipeline.redraft_email(conn, lid, note)
            lead["events"] = store.events(conn, lid)
            self._send(200, lead)
        except (ValueError, KeyError) as exc:
            self._send(400, {"error": str(exc).strip("'\"")})
        except RuntimeError as exc:  # LLM/API failures
            self._send(502, {"error": str(exc)})
        finally:
            conn.close()


def serve(port: int = 8765) -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Dashboard: http://127.0.0.1:{port}  (llm mode: {config.llm_mode()}, db: {config.DB_PATH})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
