# Jdot verification

Checked on November 12, 2026, in the managed Linux workspace with Python 3.12.

| Check | Observed result |
| --- | --- |
| Native CLI tests | 8 unittest methods pass, including mode, Page URL, Unicode line boundaries, summary identity, timestamp, length, and clean-error cases |
| Example summary | Valid, 13 words, explicitly reports `saved: false` |
| Example handoff | Prints the request, requested mode, Page URL, and memory guidance without changing source files or sending data |
| Plugin preflight | Skills-only version 0.1.0; 3 Skills; no errors |
| Deterministic plugin packaging | Two builds byte-identical; record the delivered artifact digest alongside its download |
| Clean archive extraction | Extracted package passes the same preflight |
| Guided Skill simulation | A fresh-context baseline omitted the specified bullet count; guided cases cover summary format, uncertain saves, missing Page access, and unverified Remote forwarding |

The generic preflight warns that no explicit public exclusions were supplied. This small private-ready package contains only the listed workflow guidance and no private source material; public submission readiness is not claimed.

The guided cases are agent simulations, not an installed-plugin or device test. Live Apple model availability, Shortcut edits, request forwarding, an actual Remote response path, and background memory capture remain unverified. The original signed Shortcut was not executed or modified. Workflow content was recovered; signature and trust chain were not verified.

The repository is initialized on `main`. The user designated `ijdotn-beep/jdot` for source upload; publication must be checked against its actual branch head. Local verification does not establish a GitHub release, public Plugin Directory submission, or account installation. The GitHub connector can populate the designated existing repository; repository creation and CLI authentication were unavailable in this session.
