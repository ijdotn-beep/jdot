"""Behavioral tests for the offline handoff CLI; no model or network calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "jdot_handoff.py"
PAGE = "https://chatgpt.com/space/page_example"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *args],
                              capture_output=True, text=True, cwd=self.folder)

    def request(self, text):
        path = self.folder / "request.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def summary(self, **changes):
        data = {"schema_version": 1,
                "session_id": "12345678-1234-5678-1234-567812345678",
                "recorded_at": "2026-11-12T09:00:00Z",
                "bullets": ["Choose the existing Shortcut", "Keep Pages as memory",
                            "Test the device handoff next"]}
        data.update(changes)
        path = self.folder / "summary.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_prepare_preserves_request_and_explicit_mode_without_writing(self):
        text = "Plan tomorrow’s rehearsal\nKeep the camera notes together"
        path = self.request(text)
        result = self.cli("prepare", "--mode", "cloud-pro", "--request-file", str(path),
                          "--page-url", PAGE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(text, result.stdout)
        self.assertIn("Cloud Pro", result.stdout)
        self.assertIn(PAGE, result.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), text)
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()), ["request.txt"])

    def test_prepare_rejects_silent_mode_substitution(self):
        result = self.cli("prepare", "--mode", "automatic", "--request-file",
                          str(self.request("Hello")), "--page-url", PAGE)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)

    def test_prepare_rejects_empty_request(self):
        result = self.cli("prepare", "--mode", "on-device", "--request-file",
                          str(self.request(" \n ")), "--page-url", PAGE)
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", result.stderr)

    def test_prepare_rejects_non_page_or_credentialed_urls(self):
        for url in ["http://chatgpt.com/space/page_example",
                    "https://other.example/space/page_example",
                    "https://user:password@chatgpt.com/space/page_example",
                    "https://chatgpt.com/",
                    "https://chatgpt.com/space/page_example/extra",
                    "https://chatgpt.com/space/page_example\nextra-line",
                    "https://chatgpt.com/space/page_example\t"]:
            with self.subTest(url=url):
                result = self.cli("prepare", "--mode", "cloud", "--request-file",
                                  str(self.request("Hello")), "--page-url", url)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)

    def test_valid_summary_is_validated_but_never_marked_saved(self):
        path = self.summary()
        before = path.read_bytes()
        result = self.cli("check-summary", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertTrue(receipt["valid"])
        self.assertFalse(receipt["saved"])
        self.assertEqual(receipt["word_count"], 13)
        self.assertEqual(path.read_bytes(), before)

    def test_summary_rejects_wrong_identity_version_and_naive_timestamp(self):
        for changes in [{"session_id": "not-a-session"}, {"schema_version": True},
                        {"schema_version": 2}, {"recorded_at": "2026-11-12T09:00:00"},
                        {"recorded_at": "tomorrow"}]:
            with self.subTest(changes=changes):
                result = self.cli("check-summary", str(self.summary(**changes)))
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)

    def test_summary_rejects_missing_long_or_multiline_bullets(self):
        for bullets in [["Only one"], ["a", "b", " "], ["a\nb", "c", "d"],
                        ["one " * 119, "two", "three"], ["a"] * 6,
                        ["a\u0085b", "c", "d"], ["a\u2028b", "c", "d"],
                        ["a\u2029", "c", "d"]]:
            with self.subTest(bullets=bullets):
                result = self.cli("check-summary", str(self.summary(bullets=bullets)))
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)

    def test_malformed_json_returns_clean_error_without_traceback(self):
        path = self.folder / "broken.json"
        path.write_text("not json", encoding="utf-8")
        result = self.cli("check-summary", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
