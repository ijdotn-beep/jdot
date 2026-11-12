#!/usr/bin/env python3
"""Prepare a manual Jdot handoff or validate a summary. Never sends or saves data."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
from uuid import UUID, uuid4

MODES = {"on-device": "On-Device", "cloud": "Cloud", "cloud-pro": "Cloud Pro"}
MAX_FILE_BYTES = 128 * 1024


def read_text(path):
    """Read a bounded UTF-8 file without modifying it."""
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("file exceeds 128 KiB")
    return data.decode("utf-8")


def prepare(mode, request, page_url, session_id=None):
    """Format a manual handoff, reusing a UUID string when supplied."""
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in page_url):
        raise ValueError("Page URL must not contain whitespace or control characters")
    url = urlsplit(page_url)
    if (url.scheme != "https" or url.netloc != "chatgpt.com"
            or not re.fullmatch(r"/space/page_[A-Za-z0-9_-]+", url.path)
            or url.query or url.fragment):
        raise ValueError("provide a canonical https://chatgpt.com/space/page_... URL")
    if not request.strip():
        raise ValueError("request must not be empty")
    if session_id is None:
        session_id = str(uuid4())
    else:
        if not isinstance(session_id, str):
            raise ValueError("session_id must be a UUID string")
        try:
            session_id = str(UUID(session_id))
        except ValueError:
            raise ValueError("session_id must be a UUID string") from None
    return (
        "Start a Jdot session\n\n"
        f"Session ID: {session_id}\n"
        f"Memory Page: {page_url}\n"
        f"Requested Shortcuts mode: {MODES[mode]}\n\n"
        "This text has not been sent. The mode above is a requested label, not proof "
        "that a model was selected or that inference occurred.\n\n"
        "Read the Memory Page with the host's authorized Pages tools. Continue from "
        "its confirmed context and address the request below. Do not silently change "
        "the requested mode or claim this handoff selected the Codex model.\n\n"
        "At the end, save 3–5 short factual summary bullets, at most 120 words, "
        "and update the Page handoff. Verify the save before reporting it. If Page "
        "access is unavailable, state that memory was not loaded or saved.\n\n"
        "## Request\n\n" + request + "\n"
    )


def check_summary(data):
    """Validate an offline summary envelope; this is not a persistence receipt."""
    if not isinstance(data, dict):
        raise ValueError("summary must be a JSON object")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    session_id = data.get("session_id")
    if not isinstance(session_id, str):
        raise ValueError("session_id must be a UUID string")
    UUID(session_id)
    recorded_at = data.get("recorded_at")
    if not isinstance(recorded_at, str):
        raise ValueError("recorded_at must be an aware ISO 8601 timestamp")
    timestamp = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("recorded_at must include a timezone")
    bullets = data.get("bullets")
    if not isinstance(bullets, list) or not 3 <= len(bullets) <= 5:
        raise ValueError("summary must contain 3–5 bullets")
    for bullet in bullets:
        if (not isinstance(bullet, str) or not bullet.strip()
                or any(ord(char) < 32 or ord(char) == 127
                       or char in "\u0085\u2028\u2029" for char in bullet)):
            raise ValueError("each bullet must be a nonempty single-line string")
    word_count = sum(len(bullet.split()) for bullet in bullets)
    if word_count > 120:
        raise ValueError("summary exceeds 120 whitespace-delimited words")
    return {"valid": True, "saved": False, "session_id": session_id,
            "word_count": word_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    handoff = commands.add_parser("prepare", help="print text for a manual Remote handoff")
    handoff.add_argument("--mode", choices=MODES, required=True)
    handoff.add_argument("--request-file", required=True)
    handoff.add_argument("--page-url", required=True)
    handoff.add_argument("--session-id", metavar="UUID",
                         help="reuse an existing session UUID when regenerating a handoff; "
                              "omit to create a new session")
    summary = commands.add_parser("check-summary", help="validate JSON without saving it")
    summary.add_argument("path")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(prepare(args.mode, read_text(args.request_file), args.page_url,
                          session_id=args.session_id), end="")
        else:
            print(json.dumps(check_summary(json.loads(read_text(args.path))), sort_keys=True))
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
