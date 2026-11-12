"""Behavioral tests for the offline handoff CLI; no model or network calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "jdot_handoff.py"
PAGE = "https://chatgpt.com/space/page_example"
SESSION_ID = "12345678-1234-4678-9234-567812345678"

spec = importlib.util.spec_from_file_location("jdot_handoff", CLI)
handoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handoff)


class PrepareTests(unittest.TestCase):
    def test_existing_three_argument_call_generates_uuid4(self):
        text = handoff.prepare("cloud", "Hello", PAGE)
        session_id = text.split("Session ID: ", 1)[1].splitlines()[0]
        self.assertEqual(UUID(session_id).version, 4)
        self.assertEqual(str(UUID(session_id)), session_id)

    def test_api_reuses_session_id(self):
        first = handoff.prepare("cloud", "Hello", PAGE, session_id=SESSION_ID)
        retry = handoff.prepare("cloud", "Hello", PAGE, session_id=SESSION_ID)
        self.assertEqual(first, retry)
        self.assertIn(f"Session ID: {SESSION_ID}\n", retry)

    def test_api_rejects_invalid_session_ids(self):
        for session_id in ["", "not-a-uuid", 123, False, [], {}, UUID(SESSION_ID)]:
            with self.subTest(session_id=session_id):
                with self.assertRaisesRegex(ValueError, "session_id must be a UUID string"):
                    handoff.prepare("cloud", "Hello", PAGE, session_id=session_id)


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

    def session_id(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        lines = [line for line in result.stdout.splitlines()
                 if line.startswith("Session ID: ")]
        self.assertEqual(len(lines), 1)
        return lines[0].removeprefix("Session ID: ")

    def test_prepare_generates_distinct_uuid4_for_new_sessions_in_all_modes(self):
        path = self.request("Hello")
        session_ids = []
        for mode, label in [("on-device", "On-Device"), ("cloud", "Cloud"),
                            ("cloud-pro", "Cloud Pro")]:
            with self.subTest(mode=mode):
                for _ in range(2):
                    result = self.cli("prepare", "--mode", mode, "--request-file",
                                      str(path), "--page-url", PAGE)
                    session_id = self.session_id(result)
                    self.assertEqual(UUID(session_id).version, 4)
                    self.assertEqual(str(UUID(session_id)), session_id)
                    self.assertIn(f"Requested Shortcuts mode: {label}\n", result.stdout)
                    self.assertIn("This text has not been sent.", result.stdout)
                    session_ids.append(session_id)
        self.assertEqual(len(set(session_ids)), len(session_ids))

    def test_prepare_retry_keeps_generated_id_and_summary_identity(self):
        path = self.request("Hello")
        args = ("prepare", "--mode", "cloud", "--request-file", str(path),
                "--page-url", PAGE)
        first = self.cli(*args)
        session_id = self.session_id(first)
        retry = self.cli(*args, "--session-id", session_id)
        self.assertEqual(self.session_id(retry), session_id)
        self.assertEqual(first.stdout, retry.stdout)
        path.write_text("Clarified request", encoding="utf-8")
        regenerated = self.cli(*args, "--session-id", session_id)
        self.assertEqual(self.session_id(regenerated), session_id)
        self.assertIn("Clarified request", regenerated.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), "Clarified request")
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()), ["request.txt"])
        checked = self.cli("check-summary", str(self.summary(session_id=session_id)))
        self.assertEqual(checked.returncode, 0, checked.stderr)
        receipt = json.loads(checked.stdout)
        self.assertEqual(receipt["session_id"], session_id)
        self.assertFalse(receipt["saved"])

    def test_prepare_normalizes_existing_uuid_spellings_in_all_modes(self):
        canonical = "abcdef12-3456-5678-9234-56789abcdef0"
        for mode in ["on-device", "cloud", "cloud-pro"]:
            for session_id in [canonical, canonical.upper(), canonical.replace("-", ""),
                               "{" + canonical + "}", "urn:uuid:" + canonical]:
                with self.subTest(mode=mode, session_id=session_id):
                    result = self.cli("prepare", "--mode", mode, "--request-file",
                                      str(self.request("Hello")), "--page-url", PAGE,
                                      "--session-id", session_id)
                    self.assertEqual(self.session_id(result), canonical)

    def test_prepare_rejects_malformed_session_ids_without_output_or_writes(self):
        path = self.request("Hello")
        for session_id in ["", "not-a-uuid", "1234", SESSION_ID[:-1],
                           SESSION_ID + "0", "g" + SESSION_ID[1:],
                           " " + SESSION_ID, SESSION_ID + "\n", SESSION_ID + "\t"]:
            with self.subTest(session_id=session_id):
                result = self.cli("prepare", "--mode", "cloud", "--request-file",
                                  str(path), "--page-url", PAGE,
                                  "--session-id", session_id)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error: session_id must be a UUID string", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(path.read_text(encoding="utf-8"), "Hello")
                self.assertEqual(sorted(p.name for p in self.folder.iterdir()),
                                 ["request.txt"])

    def test_prepare_session_id_option_requires_a_value(self):
        result = self.cli("prepare", "--mode", "cloud", "--request-file",
                          str(self.request("Hello")), "--page-url", PAGE, "--session-id")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("expected one argument", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_prepare_help_exposes_session_id(self):
        result = self.cli("prepare", "--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--session-id", result.stdout)
        self.assertIn("UUID", result.stdout)

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
