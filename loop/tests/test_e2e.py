"""End-to-end test in mock mode (no network, no API key).

Run from loop/:  python -m unittest discover -s tests -v
"""
from __future__ import annotations

import email
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

from prospect_loop import config, pipeline, sources, store  # noqa: E402


class LoopTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        config.DB_PATH = Path(self.tmp.name) / "leads.db"
        config.OUT_DIR = Path(self.tmp.name) / "out"
        self.conn = store.connect()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def by_domain(self, domain):
        return next(l for l in store.all_leads(self.conn) if l["domain"] == domain)

    def test_ingest_dedupes_and_excludes(self):
        stats = pipeline.ingest(self.conn)
        self.assertEqual(stats["excluded"], 1)  # Higgsfield
        domains = [l["domain"] for l in store.all_leads(self.conn)]
        self.assertNotIn("higgsfield.ai", domains)
        self.assertEqual(len(domains), len(set(domains)))
        again = pipeline.ingest(self.conn)  # idempotent
        self.assertEqual(again["added"], 0)

    def test_full_loop(self):
        pipeline.ingest(self.conn)
        pipeline.qualify_all(self.conn)
        flam = self.by_domain("flamapp.ai")
        self.assertEqual(flam["status"], "qualified")
        self.assertGreaterEqual(flam["score"], config.QUALIFY_THRESHOLD)
        self.assertTrue(flam["poolday_prompts"]["command"].startswith("/prospect-video https://flamapp.ai"))
        self.assertLessEqual(len(flam["poolday_prompts"]["command"].splitlines()), 3)
        self.assertEqual(self.by_domain("arcee.ai")["status"], "disqualified")  # no buyer

        # human gate: regenerate once, then approve
        with self.assertRaises(ValueError):
            pipeline.submit_video(self.conn, flam["id"], "not a link")
        pipeline.submit_video(self.conn, flam["id"], "https://poolday.ai/v/flam-v1")
        lead = pipeline.regenerate(self.conn, flam["id"], "hard cut at 0:04, hold logo 2 frames longer")
        self.assertEqual(lead["status"], "qualified")
        self.assertEqual(lead["video_version"], 2)
        self.assertIn("hard cut at 0:04", lead["poolday_prompts"]["revision"])
        pipeline.submit_video(self.conn, flam["id"], "https://poolday.ai/v/flam-v2")
        lead = pipeline.approve(self.conn, flam["id"])
        self.assertEqual(lead["status"], "approved")
        body = lead["email"]["body"]
        for must in ("Karthik", "$40M", "[VIDEO THUMBNAIL]", "https://poolday.ai/v/flam-v2"):
            self.assertIn(must, body)
        self.assertEqual(body.count("?"), 1)  # one-question CTA

        pipeline.save_email(self.conn, flam["id"], "Edited subject", body)

        # reject path
        wispr = self.by_domain("wisprflow.ai")
        pipeline.submit_video(self.conn, wispr["id"], "https://poolday.ai/v/wispr-v1")
        pipeline.reject(self.conn, wispr["id"], "UI looks off-brand")

        res = pipeline.export(self.conn)
        self.assertEqual(res["count"], 1)
        msg = email.message_from_bytes(Path(res["eml"][0]).read_bytes())
        self.assertEqual(msg["Subject"], "Edited subject")
        self.assertTrue(Path(res["csv"]).exists())
        self.assertEqual(self.by_domain("flamapp.ai")["status"], "exported")
        actions = [e["action"] for e in store.events(self.conn, flam["id"])]
        self.assertEqual(actions[-1], "exported")
        self.assertIn("regenerate", actions)

    def test_claude_code_mode_roundtrip(self):
        pipeline.ingest(self.conn)
        path = Path(self.tmp.name) / "tasks.json"
        out = pipeline.llm_export(self.conn, path)
        self.assertGreater(out["tasks"], 0)
        data = json.loads(path.read_text())
        t = next(t for t in data["tasks"] if t["company"] == "Flam")
        t["result"] = {"rubric": {"b2b": 20, "freshness": 20, "buyer": 20, "visual_product": 18,
                                  "video_need": 18}, "score": 96, "justification": "test",
                       "video_angle": "your Series B announcement film", "launch_hook": "the round",
                       "audience": "CMO"}
        path.write_text(json.dumps(data))
        self.assertEqual(pipeline.llm_import(self.conn, path)["imported"], 1)
        flam = self.by_domain("flamapp.ai")
        self.assertEqual((flam["status"], flam["qualified_by"], flam["score"]), ("qualified", "claude-code", 96))

    def test_funding_news_stub_parses_rss(self):
        rss = """<rss><channel>
          <item><title>Example Corp raises $30M Series B to build widgets</title>
                <link>https://www.example.com/blog/series-b</link>
                <pubDate>Mon, 21 Sep 2026 10:00:00 GMT</pubDate></item>
          <item><title>Other Co raises $12M Series A</title><link>https://other.example</link></item>
        </channel></rss>"""
        items = list(sources.FundingNewsSource(feeds=[]).parse(rss))
        self.assertEqual(len(items), 1)
        self.assertEqual((items[0]["company"], items[0]["domain"]), ("Example Corp", "example.com"))

    def test_dashboard_http(self):
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
            self.assertIn(b"Prospect loop", urllib.request.urlopen(base + "/").read())
            call("/api/run", {})
            flam = next(l for l in call("/api/leads") if l["domain"] == "flamapp.ai")
            call(f"/api/leads/{flam['id']}/video", {"url": "https://poolday.ai/v/x"})
            lead = call(f"/api/leads/{flam['id']}/approve", {"note": ""})
            self.assertEqual(lead["status"], "approved")
            self.assertEqual(call("/api/export", {})["count"], 1)
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
