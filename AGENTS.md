# Jdot repository guidance

Jdot keeps durable memory in a user-authorized ChatGPT Page. Start by reading the user-supplied Page or the `memory_page_url` in ignored `.jdot/config.json`; local configuration is not memory itself. If neither is available, ask for the Page. Never imply a missing Page was loaded.

Keep Apple model inference, Codex Remote control, and Pages persistence distinct. `Ask` in an exported workflow means deferred selection. A generated handoff is text for manual transfer, not a dispatch receipt. This repository has no unattended bridge or API-backed inference server.

Use the Jdot session Skill for 3–5 factual summary bullets, at most 120 words, after each connected session. Read current Page state before writes, preserve unrelated content, reuse existing session identity when retrying, and verify the save. Mark unconfirmed ideas as proposals. A local validation result never means a Page was updated.

Preserve uploaded Shortcut bytes. Do not commit personal Page links, original signed exports, signer metadata, certificates, credentials, or raw conversation history. Keep those in ignored `.jdot/` only when needed and authorized. Portable plugin content must work without this repository or personal configuration.

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate_plugin.py plugins/jdot --json` after relevant changes. Package with `python3 scripts/package_plugin.py plugins/jdot dist/jdot-plugin.zip --json`. Do not claim device tests, an installed-plugin smoke test, GitHub publication, or Plugin Directory approval unless observed. Repository creation does not authorize public sharing or submission.
