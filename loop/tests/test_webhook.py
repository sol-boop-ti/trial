"""Webhook mode: the loop POSTs a lead to Poolday's inbound webhook, Poolday calls our
callback with the outputs. A local fake receiver plays Poolday (no network).

The receiver is NOT Poolday: it only does what we ask Poolday's agent to do in the
README message (accept our JSON, check the secret header, POST the result back to the
callback_url with lead_id, token, status, video_url, conversation_url).
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["LLM_MODE"] = "mock"
os.environ["LOOP_TODAY"] = "2026-09-24"

from prospect_loop import config, pipeline, poolday_api, store  # noqa: E402
from prospect_loop.__main__ import main as cli  # noqa: E402
from prospect_loop.server import Handler  # noqa: E402

SECRET = "test-shared-secret-123456"
ENV_KEYS = ("POOLDAY_API", "POOLDAY_WEBHOOK_URL", "POOLDAY_WEBHOOK_SECRET", "POOLDAY_CALLBACK_SECRET",
            "POOLDAY_WEBHOOK_SECRET_HEADER", "PUBLIC_BASE_URL", "POOLDAY_CALLBACK_KEYS",
            "POOLDAY_WEBHOOK_EXTRA", "POOLDAY_API_CONFIG")


class FakePooldayReceiver:
    """Plays the Poolday agent's inbound webhook. On each POST it checks the secret header,
    answers 202, then (unless auto_callback is off) calls the callback_url back.

    `shape(payload, n)` builds the callback body; the default is the flat shape the README
    message asks for. `question_first` makes the first callback a question instead."""

    def __init__(self, secret=SECRET, header="X-Webhook-Secret"):
        self.secret, self.header = secret, header
        self.received: list[dict] = []
        self.callbacks: list[tuple[int, dict]] = []
        self.auto_callback = True
        self.question_first = False
        self.shape = self.flat
        rx = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                body = json.loads(self.rfile.read(n) or b"{}")
                if self.headers.get(rx.header) != rx.secret:
                    return self._send(401, {"error": "bad secret"})
                rx.received.append(body)
                self._send(202, {"accepted": True, "run_id": f"run_{len(rx.received)}"})
                if rx.auto_callback:
                    threading.Thread(target=rx._call_back, args=(body,), daemon=True).start()

            def _send(self, code, obj):
                data = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}/hooks/abcdef0123456789"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    @staticmethod
    def flat(p: dict, n: int) -> dict:
        return {"lead_id": p["lead_id"], "token": p["token"], "status": "completed",
                "video_url": f"https://videos.example/{p['lead_id']}/v{p.get('version')}.mp4",
                "conversation_url": f"https://app.example/c/{p['lead_id']}"}

    def _call_back(self, p: dict):
        time.sleep(0.05)
        n = len(self.received)
        if self.question_first and p["kind"] == "start":
            body = {"lead_id": p["lead_id"], "token": p["token"], "status": "waiting_for_user",
                    "question": "Keep the 20s cut, or go 15s?"}
        else:
            body = self.shape(p, n)
        req = urllib.request.Request(p["callback_url"], data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", self.header: self.secret})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                self.callbacks.append((r.status, json.loads(r.read())))
        except urllib.error.HTTPError as e:
            self.callbacks.append((e.code, json.loads(e.read() or b"{}")))

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class WebhookTestBase(unittest.TestCase):
    header = "X-Webhook-Secret"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.saved = (config.DB_PATH, config.OUT_DIR, config.REFERENCE_VIDEO)
        self.env = {k: os.environ.get(k) for k in ENV_KEYS}
        config.DB_PATH = Path(self.tmp.name) / "leads.db"
        config.OUT_DIR = Path(self.tmp.name) / "out"
        config.REFERENCE_VIDEO = "https://www.youtube.com/watch?v=ref"
        self.saved_cfg = config.POOLDAY_API_CONFIG
        config.POOLDAY_API_CONFIG = Path(self.tmp.name) / "none.toml"  # no mapping file
        # our dashboard (the callback target)
        self.dash = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.dash.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.dash.server_address[1]}"
        self.rx = FakePooldayReceiver(header=self.header)
        for k in ENV_KEYS:
            os.environ.pop(k, None)
        os.environ.update(POOLDAY_API="webhook", POOLDAY_WEBHOOK_URL=self.rx.url,
                          POOLDAY_WEBHOOK_SECRET=SECRET, PUBLIC_BASE_URL=self.base)
        if self.header != "X-Webhook-Secret":
            os.environ["POOLDAY_WEBHOOK_SECRET_HEADER"] = self.header
        self.conn = store.connect()
        pipeline.ingest(self.conn)
        pipeline.qualify_all(self.conn)
        self.flam = next(l for l in store.all_leads(self.conn) if l["domain"] == "flamapp.ai")

    def tearDown(self):
        self.conn.close()
        self.rx.close()
        self.dash.shutdown()
        self.dash.server_close()
        self.tmp.cleanup()
        config.DB_PATH, config.OUT_DIR, config.REFERENCE_VIDEO = self.saved
        config.POOLDAY_API_CONFIG = self.saved_cfg
        for k, v in self.env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def wait(self, until, timeout=5.0):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            lead = store.get(self.conn, self.flam["id"])
            if until(lead):
                return lead
            time.sleep(0.03)
        self.fail("timed out: " + json.dumps(store.get(self.conn, self.flam["id"]).get("poolday")))

    def post_callback(self, body, headers=None, raw=None, path=poolday_api.CALLBACK_PATH):
        h = {"Content-Type": "application/json", **(headers or {})}
        data = raw if raw is not None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, method="POST", headers=h)
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")


class WebhookFlowTest(WebhookTestBase):
    def test_send_callback_review_regenerate_approve(self):
        lid = self.flam["id"]
        self.assertEqual(poolday_api.get_client().name, "webhook")
        lead = pipeline.send_to_poolday(self.conn, lid)
        pd = lead["poolday"]
        self.assertEqual((pd["status"], pd["client"]), ("queued", "webhook"))
        self.assertEqual(pd["callback_url"], self.base + "/api/poolday/callback")

        # what Poolday received: our documented fields, the token, the secret header
        sent = self.rx.received[0]
        for k in ("lead_id", "company", "website", "angle", "contact_name", "contact_role",
                  "reference_url", "prompt", "callback_url", "token"):
            self.assertTrue(sent.get(k), k)
        self.assertEqual((sent["kind"], sent["lead_id"], sent["website"]), ("start", lid, "https://flamapp.ai"))
        self.assertTrue(sent["prompt"].startswith("/prospect-video https://flamapp.ai"))
        self.assertEqual(sent["token"], pd["callback_token"])

        # Poolday calls back -> the lead lands in Review, and stops there
        lead = self.wait(lambda l: l["status"] == "in_review")
        self.assertTrue(lead["video_url"].endswith(f"/{lid}/v1.mp4"))
        self.assertEqual(lead["poolday"]["status"], "done")
        self.assertEqual(lead["poolday"]["conversation_url"], f"https://app.example/c/{lid}")
        self.assertIsNone(lead.get("email"))
        self.assertEqual(self.rx.callbacks[0][0], 200)

        # a v1 callback arriving again is a duplicate, not a state change
        code, resp = self.post_callback(self.rx.flat(sent, 1), {self.header: SECRET})
        self.assertEqual((code, resp.get("ignored")), (200, "duplicate, already in review"))

        # regenerate -> follow-up payload with the same lead_id and the note -> v2 in Review
        lead = pipeline.regenerate(self.conn, lid, "hard cut at 0:04, hold logo 2 frames longer")
        self.assertEqual(lead["poolday"]["status"], "running")
        rev = self.rx.received[1]
        self.assertEqual((rev["kind"], rev["lead_id"], rev["token"], rev["version"]),
                         ("revision", lid, sent["token"], 2))
        self.assertEqual(rev["note"], "hard cut at 0:04, hold logo 2 frames longer")
        lead = self.wait(lambda l: l["status"] == "in_review")
        self.assertTrue(lead["video_url"].endswith("/v2.mp4"))
        self.assertEqual(lead["video_version"], 2)

        # a late v1 callback is ignored as stale... once the lead is waiting again
        pipeline.regenerate(self.conn, lid, "tighter end card")
        self.rx.callbacks.clear()
        code, resp = self.post_callback({**self.rx.flat(sent, 1), "version": 1}, {self.header: SECRET})
        self.assertIn("stale", resp.get("ignored", ""))
        lead = self.wait(lambda l: l["status"] == "in_review")
        self.assertTrue(lead["video_url"].endswith("/v3.mp4"))

        lead = pipeline.approve(self.conn, lid)
        self.assertIn(lead["video_url"], lead["email"]["body"])

        actions = [e["action"] for e in store.events(self.conn, lid)]
        for a in ("poolday:sent", "poolday:callback", "poolday:done", "video_submitted",
                  "regenerate", "poolday:revision_sent", "approved"):
            self.assertIn(a, actions)
        calls = store.api_calls(self.conn, lid)
        ops = [c["op"] for c in calls]
        self.assertEqual(ops[:2], ["start", "callback"])
        self.assertIn("message", ops)
        dump = json.dumps(calls)
        self.assertNotIn(SECRET, dump)            # secrets redacted in the log
        self.assertNotIn(sent["token"], dump)
        self.assertIn("[redacted]", dump)
        self.assertNotIn("abcdef0123456789", dump)  # the webhook URL's secret-looking path is masked

    def test_bad_secret_and_token_rejected(self):
        lid = self.flam["id"]
        self.rx.auto_callback = False
        pipeline.send_to_poolday(self.conn, lid)
        token = store.get(self.conn, lid)["poolday"]["callback_token"]
        good = {"lead_id": lid, "token": token, "status": "completed", "video_url": "https://v.example/x.mp4"}

        self.assertEqual(self.post_callback(good, {self.header: "wrong"})[0], 401)
        self.assertEqual(self.post_callback(good)[0], 401)                        # no secret at all
        self.assertEqual(self.post_callback({**good, "token": "nope"}, {self.header: SECRET})[0], 403)
        self.assertEqual(self.post_callback({**good, "lead_id": 99999}, {self.header: SECRET})[0], 404)
        self.assertEqual(store.get(self.conn, lid)["status"], "qualified")

        rows = store.api_calls(self.conn)
        rejected = [r for r in rows if r["op"] == "callback" and r["http_status"] == 401]
        self.assertEqual(len(rejected), 2)
        self.assertIsNone(rejected[0]["lead_id"])  # unauthenticated: not attached to a lead
        self.assertNotIn(token, json.dumps(rows))
        self.assertIn("[redacted]", rejected[0]["request"])

        # the secret is also accepted as a body field or a Bearer header
        self.assertEqual(self.post_callback({**good, "secret": SECRET})[0], 200)
        self.assertEqual(store.get(self.conn, lid)["status"], "in_review")
        self.assertNotIn(SECRET, json.dumps(store.api_calls(self.conn)))

    def test_receiver_rejects_our_wrong_secret(self):
        os.environ["POOLDAY_WEBHOOK_SECRET"] = "not-the-one"
        with self.assertRaises(poolday_api.PooldayError) as cm:
            pipeline.send_to_poolday(self.conn, self.flam["id"])
        self.assertIn("rejected our secret", str(cm.exception))

    def test_not_configured(self):
        os.environ.pop("PUBLIC_BASE_URL")
        with self.assertRaises(poolday_api.PooldayNotConfigured) as cm:
            poolday_api.get_client()
        self.assertIn("PUBLIC_BASE_URL", str(cm.exception))
        self.assertFalse(poolday_api.status_line()["ok"])

    def test_poll_is_skipped_and_mark_done(self):
        lid = self.flam["id"]
        self.rx.auto_callback = False
        pipeline.send_to_poolday(self.conn, lid)
        self.assertIn("skipped", pipeline.poll_poolday(self.conn))
        with self.assertRaises(ValueError):  # no double submission while waiting for the callback
            pipeline.send_to_poolday(self.conn, lid)
        lead = pipeline.mark_poolday_done(self.conn, lid, "https://v.example/by-hand")
        self.assertEqual((lead["status"], lead["poolday"]["status"]), ("in_review", "done"))
        self.assertIn("poolday:marked_done", [e["action"] for e in store.events(self.conn, lid)])

    def test_dashboard_is_local_only_through_the_tunnel(self):
        tunnel = {"Cf-Connecting-Ip": "203.0.113.9", "Host": "abc.trycloudflare.com"}
        req = urllib.request.Request(self.base + "/api/leads", headers=tunnel)
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(cm.exception.code, 404)
        req = urllib.request.Request(self.base + "/api/run", data=b"{}", method="POST", headers=tunnel)
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(req, timeout=5)
        req = urllib.request.Request(self.base + "/api/poolday/callback", headers=tunnel)
        with urllib.request.urlopen(req, timeout=5) as r:
            self.assertEqual(r.status, 200)
        # the callback itself works through the tunnel
        code, _ = self.post_callback({"lead_id": 1}, {**tunnel, self.header: "bad"})
        self.assertEqual(code, 401)
        meta = json.loads(urllib.request.urlopen(self.base + "/api/meta").read())
        self.assertEqual((meta["poolday"]["client"], meta["poolday"]["pollable"]), ("webhook", False))
        self.assertEqual(meta["poolday"]["callback_url"], self.base + "/api/poolday/callback")

    def test_dashboard_send_and_mark_done_routes(self):
        lid = self.flam["id"]
        self.rx.auto_callback = False

        def call(path, body):
            req = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), method="POST",
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read())
        lead = call(f"/api/leads/{lid}/poolday_send", {"prompt": "command"})
        self.assertEqual(lead["poolday"]["status"], "queued")
        lead = call(f"/api/leads/{lid}/poolday_mark_done", {"url": "https://v.example/m.mp4"})
        self.assertEqual(lead["status"], "in_review")


class WebhookQuestionTest(WebhookTestBase):
    header = "X-Poolday-Hook"  # configurable header name, both directions

    def test_question_then_answer_then_video(self):
        lid = self.flam["id"]
        self.rx.question_first = True
        pipeline.send_to_poolday(self.conn, lid)
        lead = self.wait(lambda l: (l.get("poolday") or {}).get("status") == "needs_input")
        self.assertEqual(lead["poolday"]["question"], "Keep the 20s cut, or go 15s?")
        self.assertEqual(lead["status"], "qualified")
        lead = pipeline.answer_poolday(self.conn, lid, "Go 15s.")
        ans = self.rx.received[1]
        self.assertEqual((ans["kind"], ans["lead_id"], ans["answer"]), ("answer", lid, "Go 15s."))
        self.assertEqual(ans["question"], "Keep the 20s cut, or go 15s?")
        lead = self.wait(lambda l: l["status"] == "in_review")
        self.assertIn("poolday:answered", [e["action"] for e in store.events(self.conn, lid)])

    def test_nested_callback_shape(self):
        """Poolday posts a nested shape: the lead still lands in Review."""
        self.rx.shape = lambda p, n: {"event": "run.completed", "data": {
            "metadata": {"leadId": str(p["lead_id"])}, "callback_token": p["token"],
            "outputs": [{"type": "image", "url": "https://cdn.example/thumb.png"},
                        {"type": "video", "url": "https://cdn.example/final"}],
            "conversation": {"url": "https://app.example/c/9"}}}
        # "data.metadata" is not a default envelope: the lead is found by its token instead
        pipeline.send_to_poolday(self.conn, self.flam["id"])
        lead = self.wait(lambda l: l["status"] == "in_review")
        self.assertEqual(lead["video_url"], "https://cdn.example/final")
        self.assertEqual(lead["poolday"]["conversation_url"], "https://app.example/c/9")


class ParseCallbackTest(unittest.TestCase):
    def setUp(self):
        self.env = {k: os.environ.get(k) for k in ENV_KEYS}
        self.saved_cfg = config.POOLDAY_API_CONFIG
        config.POOLDAY_API_CONFIG = Path("/nonexistent/poolday_api.toml")
        for k in ENV_KEYS:
            os.environ.pop(k, None)

    def tearDown(self):
        config.POOLDAY_API_CONFIG = self.saved_cfg
        for k, v in self.env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def p(self, payload):
        return poolday_api.parse_callback(payload)

    def test_flat(self):
        r = self.p({"lead_id": "7", "token": "t", "status": "completed",
                    "video_url": "https://x.example/v.mp4", "conversation_url": "https://c.example/1"})
        self.assertEqual((r["lead_id"], r["token"], r["status"], r["video_url"], r["conversation_url"]),
                         (7, "t", "done", "https://x.example/v.mp4", "https://c.example/1"))

    def test_outputs_list_skips_images(self):
        r = self.p({"data": {"leadId": 7, "state": "SUCCEEDED", "outputs": [
            {"type": "image", "url": "https://x.example/thumb.png"},
            {"type": "video", "url": "https://x.example/final"}]}})
        self.assertEqual((r["lead_id"], r["status"], r["video_url"]), (7, "done", "https://x.example/final"))

    def test_assets_prefers_video_files_and_infers_done(self):
        r = self.p({"lead": {"id": 7}, "assets": ["https://x.example/poster.jpg", "https://x.example/cut.mp4"]})
        self.assertEqual((r["lead_id"], r["status"], r["video_url"]), (7, "done", "https://x.example/cut.mp4"))

    def test_result_video_and_nested_json_string(self):
        r = self.p({"payload": json.dumps({"lead_id": 3, "result": {"video": "https://x.example/a.mov"}})})
        self.assertEqual((r["lead_id"], r["video_url"]), (3, "https://x.example/a.mov"))

    def test_url_equal_to_conversation_is_not_the_video(self):
        r = self.p({"lead_id": 1, "status": "running", "url": "https://app.example/c/1",
                    "conversation_url": "https://app.example/c/1"})
        self.assertEqual((r["status"], r["video_url"]), ("running", None))

    def test_question(self):
        r = self.p({"lead_id": 7, "event": "run.waiting", "message": "Which logo?"})
        self.assertEqual((r["status"], r["question"]), ("needs_input", "Which logo?"))
        r = self.p({"lead_id": 7, "status": "running", "question": "15s or 20s?"})
        self.assertEqual((r["status"], r["question"]), ("needs_input", "15s or 20s?"))

    def test_failure(self):
        r = self.p({"lead_id": 7, "status": "error", "error": {"message": "render failed"}})
        self.assertEqual((r["status"], r["error"]), ("failed", "render failed"))

    def test_deep_scan_fallback(self):
        r = self.p({"lead_id": 7, "weird": {"nested": [{"thing": "https://x.example/deep/final.webm"}]}})
        self.assertEqual(r["video_url"], "https://x.example/deep/final.webm")

    def test_configurable_keys_env_and_file(self):
        os.environ["POOLDAY_CALLBACK_KEYS"] = json.dumps({"video_url": ["deliverable.link"],
                                                          "lead_id": "ref.lead"})
        r = self.p({"ref": {"lead": "lead-12"}, "deliverable": {"link": "https://x.example/y"}})
        self.assertEqual((r["lead_id"], r["video_url"], r["status"]), (12, "https://x.example/y", "done"))
        os.environ.pop("POOLDAY_CALLBACK_KEYS")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "poolday_api.toml"
            path.write_text('[webhook]\nsecret_header = "X-Hook"\n[webhook.keys]\nvideo_url = ["clip.src"]\n'
                            '[webhook.status_map]\ndone = ["rendered"]\n')
            config.POOLDAY_API_CONFIG = path
            st = poolday_api.webhook_settings()
            self.assertEqual(st["secret_header"], "X-Hook")
            r = poolday_api.parse_callback({"state": "rendered", "clip": {"src": "https://x.example/z"}}, st)
            self.assertEqual((r["status"], r["video_url"]), ("done", "https://x.example/z"))

    def test_redact(self):
        red = poolday_api.redact({"token": "abc", "a": {"api_key": "k"}, "note": "s3cretvalue here"},
                                 ["s3cretvalue"])
        self.assertEqual(red, {"token": "[redacted]", "a": {"api_key": "[redacted]"},
                               "note": "[redacted] here"})

    def test_example_mapping_webhook_section_loads(self):
        m = poolday_api.load_mapping(poolday_api.EXAMPLE_MAPPING)
        self.assertEqual(m["webhook"]["secret_header"], "X-Webhook-Secret")
        self.assertNotIn("webhook", ".".join(poolday_api.placeholders(m)))


class WebhookCliTest(WebhookTestBase):
    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            cli(list(args))
        return out.getvalue()

    def test_callback_url_webhook_test_and_simulate(self):
        self.assertEqual(self.run_cli("callback-url").strip(), self.base + "/api/poolday/callback")
        self.rx.auto_callback = False
        out = self.run_cli("webhook-test", "--domain", "flamapp.ai", "--brand-kit", "Flam kit")
        self.assertIn("HTTP 202", out)
        self.assertEqual(self.rx.received[0]["brand_kit_name"], "Flam kit")
        lid = self.flam["id"]
        # over HTTP to the running dashboard
        out = self.run_cli("simulate-callback", "--lead", str(lid), "--question", "Which logo?",
                           "--base", self.base)
        self.assertIn("HTTP 200", out)
        self.assertEqual(store.get(self.conn, lid)["poolday"]["status"], "needs_input")
        # in-process
        out = self.run_cli("simulate-callback", "--lead", str(lid), "--video", "https://v.example/s.mp4",
                           "--direct")
        self.assertIn("is now 'in_review'", out)


if __name__ == "__main__":
    unittest.main()
