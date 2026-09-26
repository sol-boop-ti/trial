import tempfile, unittest
from email import message_from_bytes as _mfb, policy
message_from_bytes = lambda b: _mfb(b, policy=policy.default)
from email.message import EmailMessage
from pathlib import Path

from prospect_loop import pipeline

BODY = "Hi Carolyn,\n\nWe made one for Wispr Flow:\n\n[VIDEO THUMBNAIL]\nhttps://example.com/v.mp4\n\nWant the editable version?"


class EmailThumbTest(unittest.TestCase):
    def test_html_part_links_an_inline_preview(self):
        with tempfile.TemporaryDirectory() as d:
            gif = Path(d) / "t.gif"; gif.write_bytes(b"GIF89a fake")
            msg = EmailMessage(); msg["Subject"] = "x"
            pipeline.build_email_body(msg, BODY, "https://example.com/v.mp4", gif)
            m = message_from_bytes(bytes(msg))
            plain = m.get_body(("plain",)).get_content()
            html = m.get_body(("html",)).get_content()
            self.assertIn("Watch the video: https://example.com/v.mp4", plain)
            self.assertNotIn("[VIDEO THUMBNAIL]", plain + html)
            self.assertIn('<a href="https://example.com/v.mp4"><img src="cid:video-thumb"', html)
            imgs = [p for p in m.walk() if p.get_content_type() == "image/gif"]
            self.assertEqual(len(imgs), 1)
            self.assertEqual(imgs[0]["Content-ID"], "<video-thumb>")

    def test_no_ffmpeg_or_no_video_falls_back_to_a_link(self):
        msg = EmailMessage(); msg["Subject"] = "x"
        pipeline.build_email_body(msg, BODY, "https://example.com/v.mp4", None)
        html = message_from_bytes(bytes(msg)).get_body(("html",)).get_content()
        self.assertIn('<a href="https://example.com/v.mp4">▶ Watch the video</a>', html)
        self.assertIsNone(pipeline.make_thumbnail("", Path("/tmp/none.gif")))


if __name__ == "__main__":
    unittest.main()
