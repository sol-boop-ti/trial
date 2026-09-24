"""Poolday API client + pipeline wiring, against the local fake server (no network).

The fake server runs with FAKE_POOLDAY_STEP_S=0: every status poll advances one phase,
so the sequence is deterministic.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["LLM_MODE"] = "mock"
os.environ["LOOP_TODAY"] = "2026-09-24"
os.environ["FAKE_POOLDAY_STEP_S"] = "0"

from prospect_loop import config, pipeline, poolday_api, poolday_fake, store  # noqa: E402


class FakeServerMixin:
    @classmethod
    def setUpClass(cls):
        cls.httpd, cls.url = poolday_fake.start_server()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()


class ClientTest(FakeServerMixin, unittest.TestCase):
    def client(self):
        c = poolday_api.FakePooldayClient(self.url)
        c.calls = []
        c.on_call = c.calls.append
        return c

    def poll_until(self, c, pid, status, n=10):
        for _ in range(n):
            p = c.get_status(pid)
            if p.status == status:
                return p
        self.fail(f"never reached {status}, last {p.status}")

    def test_async_run_question_answer_revision(self):
        c = self.client()
        before = c.credits()["remaining"]
        p = c.start_production("/prospect-video https://flamapp.ai ref: https://youtu.be/x",
                               settings={"mode": "align", "tier": "standard"})
        self.assertTrue(p.id.startswith("prod_"))
        self.assertEqual((p.status, p.raw_status), ("queued", "in_queue"))
        self.assertEqual(c.get_status(p.id).status, "running")
        q = c.get_status(p.id)
        self.assertEqual(q.status, "needs_input")
        self.assertIn("Go ahead", q.question)
        self.assertTrue(q.question_id)
        a = c.answer_question(p.id, "Go ahead.", q.question_id)
        self.assertEqual(a.status, "running")
        done = self.poll_until(c, p.id, "done")
        self.assertTrue(done.video_url.endswith("/v1"))
        self.assertEqual(c.get_result(p.id).video_url, done.video_url)
        # revision in the same conversation -> v2
        r = c.send_message(p.id, "Revision: hard cut at 0:04")
        self.assertEqual(r.status, "running")
        self.assertTrue(self.poll_until(c, p.id, "done").video_url.endswith("/v2"))
        self.assertLess(c.credits()["remaining"], before)
        # the watch link is a real page
        self.assertIn(b"hard cut at 0:04", urllib.request.urlopen(done.video_url).read())
        # every call was reported, without the key
        ops = [x["op"] for x in c.calls]
        self.assertEqual(ops[:3], ["credits", "start", "status"])
        self.assertIn("answer", ops)
        self.assertIn("message", ops)
        self.assertNotIn(poolday_fake.FAKE_KEY, json.dumps(c.calls))
        start = next(x for x in c.calls if x["op"] == "start")
        self.assertEqual((start["method"], start["path"], start["http_status"]),
                         ("POST", "/fake/v0/productions", 201))
        self.assertIn('"mode": "align"', start["request"])

    def test_build_mode_skips_question_and_upload(self):
        c = self.client()
        skill = Path(config.POOLDAY_SKILL_FILE)
        files = [str(skill)] if skill.exists() else []
        p = c.start_production("Use this skill. Brand: https://wisprflow.ai", attachments=files,
                               settings={"mode": "build"})
        self.assertEqual(self.poll_until(c, p.id, "done").status, "done")
        if files:
            self.assertEqual([x["op"] for x in c.calls][0], "upload")

    def test_failure_and_bad_key(self):
        c = self.client()
        p = c.start_production("[fail] test")
        self.assertEqual(self.poll_until(c, p.id, "failed").error, "render failed (simulated)")
        bad = poolday_api.HttpPooldayClient(poolday_fake.FAKE_MAPPING, api_key="wrong", base_url=self.url)
        with self.assertRaises(poolday_api.PooldayError):
            bad.start_production("x")
        with self.assertRaises(poolday_api.PooldayError):
            c.get_status("prod_missing")


class MappingTest(unittest.TestCase):
    def test_example_mapping_is_all_placeholders(self):
        m = poolday_api.load_mapping(poolday_api.EXAMPLE_MAPPING)
        todo = poolday_api.placeholders(m)
        for key in ("api.base_url", "endpoints.start", "endpoints.message", "endpoints.status",
                    "request.prompt", "response.id", "response.status", "response.video_url"):
            self.assertIn(key, todo)
        with self.assertRaises(poolday_api.PooldayNotConfigured):
            poolday_api.HttpPooldayClient(m, api_key="k")
        # same structure as the filled fake mapping
        self.assertEqual(set(m) - {"headers"}, set(poolday_fake.FAKE_MAPPING))

    def test_dig_put(self):
        body = {}
        poolday_api.put(body, "settings.mode", "align")
        self.assertEqual(body, {"settings": {"mode": "align"}})
        self.assertEqual(poolday_api.dig({"a": [{"b": 1}]}, "a.0.b"), 1)
        self.assertIsNone(poolday_api.dig({"a": 1}, "a.b"))
        self.assertEqual(poolday_api.dig({"v": [{"u": 1}, {"u": 2}]}, "v.-1.u"), 2)

    def test_manual_client(self):
        old = os.environ.get("POOLDAY_API")
        os.environ["POOLDAY_API"] = "manual"
        try:
            c = poolday_api.get_client()
            self.assertFalse(c.automatic)
            with self.assertRaises(poolday_api.ManualStep):
                c.start_production("x")
        finally:
            os.environ.pop("POOLDAY_API") if old is None else os.environ.__setitem__("POOLDAY_API", old)


class PipelineTest(FakeServerMixin, unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.saved = (config.DB_PATH, config.OUT_DIR)
        config.DB_PATH = Path(self.tmp.name) / "leads.db"
        config.OUT_DIR = Path(self.tmp.name) / "out"
        self.env = {k: os.environ.get(k) for k in ("POOLDAY_API", "POOLDAY_FAKE_URL")}
        os.environ.update(POOLDAY_API="fake", POOLDAY_FAKE_URL=self.url)
        self.conn = store.connect()
        pipeline.ingest(self.conn)
        pipeline.qualify_all(self.conn)
        self.flam = next(l for l in store.all_leads(self.conn) if l["domain"] == "flamapp.ai")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()
        config.DB_PATH, config.OUT_DIR = self.saved
        for k, v in self.env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

    def poll(self, until, n=10):
        for _ in range(n):
            pipeline.poll_poolday(self.conn)
            lead = store.get(self.conn, self.flam["id"])
            if until(lead):
                return lead
        self.fail("poll never converged: " + json.dumps(lead.get("poolday")))

    def test_send_question_answer_review_regenerate_approve(self):
        lid = self.flam["id"]
        lead = pipeline.send_to_poolday(self.conn, lid)
        pd = lead["poolday"]
        self.assertEqual(pd["status"], "queued")
        self.assertTrue(pd["sent_prompt"].startswith("/prospect-video https://flamapp.ai"))
        with self.assertRaises(ValueError):  # no double submission while running
            pipeline.send_to_poolday(self.conn, lid)

        lead = self.poll(lambda l: l["poolday"]["status"] == "needs_input")
        self.assertEqual(lead["status"], "qualified")
        self.assertIn("Go ahead", lead["poolday"]["question"])
        lead = pipeline.answer_poolday(self.conn, lid, "Go ahead with the 20s cut.")
        self.assertEqual(lead["poolday"]["status"], "running")

        # finished video lands in the human gate, and stops there
        lead = self.poll(lambda l: l["status"] == "in_review")
        self.assertTrue(lead["video_url"].endswith("/v1"))
        for _ in range(3):
            pipeline.poll_poolday(self.conn)
        self.assertEqual(store.get(self.conn, lid)["status"], "in_review")
        self.assertIsNone(store.get(self.conn, lid).get("email"))

        # regenerate -> follow-up in the SAME conversation -> v2 back in review
        lead = pipeline.regenerate(self.conn, lid, "hard cut at 0:04, hold logo 2 frames longer")
        self.assertEqual(lead["poolday"]["production_id"], pd["production_id"])
        self.assertFalse(lead["poolday"]["pending_revision"])
        self.assertEqual(lead["poolday"]["status"], "running")
        lead = self.poll(lambda l: l["status"] == "in_review")
        self.assertTrue(lead["video_url"].endswith("/v2"))
        self.assertEqual(lead["video_version"], 2)

        lead = pipeline.approve(self.conn, lid)
        self.assertIn(lead["video_url"], lead["email"]["body"])

        actions = [e["action"] for e in store.events(self.conn, lid)]
        for a in ("poolday:sent", "poolday:needs_input", "poolday:answered", "poolday:done",
                  "video_submitted", "regenerate", "poolday:revision_sent", "approved"):
            self.assertIn(a, actions)
        calls = store.api_calls(self.conn, lid)
        self.assertEqual({c["op"] for c in calls} >= {"start", "status", "answer", "message"}, True)
        self.assertTrue(all(c["service"] == "poolday:fake" for c in calls))

    def test_fallback_prompt_attaches_skill_file(self):
        lead = pipeline.send_to_poolday(self.conn, self.flam["id"], "fallback")
        self.assertNotIn("[drop", lead["poolday"]["sent_prompt"])
        if Path(config.POOLDAY_SKILL_FILE).exists():
            ops = [c["op"] for c in store.api_calls(self.conn, self.flam["id"])]
            self.assertEqual(ops[:2], ["upload", "start"])

    def test_http_client_from_mapping_file_refuses_placeholders(self):
        """The generic HTTP path (mapping read from a file, key from env), as with the real API."""
        path = Path(self.tmp.name) / "poolday_api.json"
        path.write_text(json.dumps({**poolday_fake.FAKE_MAPPING,
                                    "api": {"base_url": self.url, "timeout_s": 5}}))
        saved = (config.POOLDAY_API_CONFIG, config.REFERENCE_VIDEO)
        config.POOLDAY_API_CONFIG = path
        os.environ.update(POOLDAY_API="http", FAKE_POOLDAY_KEY=poolday_fake.FAKE_KEY)
        try:
            self.assertEqual(poolday_api.get_client().name, "http")
            with self.assertRaises(ValueError) as cm:  # "<REFERENCE VIDEO LINK>" is unfilled
                pipeline.send_to_poolday(self.conn, self.flam["id"])
            self.assertIn("REFERENCE", str(cm.exception))
            config.REFERENCE_VIDEO = "https://www.youtube.com/watch?v=ref"
            lead = pipeline.send_to_poolday(self.conn, self.flam["id"])
            self.assertIn("ref: https://www.youtube.com/watch?v=ref", lead["poolday"]["sent_prompt"])
            self.assertEqual(lead["poolday"]["client"], "http")
        finally:
            config.POOLDAY_API_CONFIG, config.REFERENCE_VIDEO = saved
            os.environ.pop("FAKE_POOLDAY_KEY", None)

    def test_manual_mode_refuses_send(self):
        os.environ["POOLDAY_API"] = "manual"
        with self.assertRaises(ValueError):
            pipeline.send_to_poolday(self.conn, self.flam["id"])

    def test_dashboard_endpoints(self):
        from http.server import ThreadingHTTPServer
        from prospect_loop.server import Handler

        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"

        def call(path, body=None):
            req = urllib.request.Request(base + path, method="POST" if body is not None else "GET",
                                         data=json.dumps(body).encode() if body is not None else None,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read())
        try:
            meta = call("/api/meta")
            self.assertTrue(meta["poolday"]["automatic"])
            self.assertEqual(meta["poolday"]["credits"]["remaining"] is not None, True)
            lid = self.flam["id"]
            lead = call(f"/api/leads/{lid}/poolday_send", {"prompt": "command"})
            self.assertEqual(lead["poolday"]["status"], "queued")
            self.assertTrue(lead["api_calls"])
            for _ in range(3):
                lead = call(f"/api/leads/{lid}/poolday_poll", {})
            self.assertEqual(lead["poolday"]["status"], "needs_input")
            call(f"/api/leads/{lid}/poolday_answer", {"answer": "Go ahead."})
            for _ in range(3):
                lead = call(f"/api/leads/{lid}/poolday_poll", {})
            self.assertEqual(lead["status"], "in_review")
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
