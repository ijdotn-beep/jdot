# Tooling provenance

`scripts/validate_plugin.py` and `scripts/package_plugin.py` are copied unchanged from Plugin Autopilot's host-provided helpers. The package's host-workspace-operator Skill was installed with its canonical installer; sandbox-python-executor was copied from the same provided Skill package. They are development and execution guidance, not permission grants.

The compatibility manifest layout was deliberately retained for these helpers. Current OpenAI documentation supports `.codex-plugin/plugin.json` while recommending the newer portable root manifest for new cross-platform packages. This repository uses one manifest source, without mixing the formats.

- [Official plugin packaging guide](https://developers.openai.com/plugins/build/plugins.md)
- [Official Skills guidance](https://learn.chatgpt.com/docs/build-skills.md)
- [Codex Remote mobile workflow](https://developers.openai.com/blog/mastering-codex-remote-for-engineering)
- [Apple Intelligence in Shortcuts](https://support.apple.com/guide/shortcuts/use-apple-intelligence-in-shortcuts-tpg3vrvwmclv/ios)

The supplied signed Shortcut was inspected with a temporary LZFSE decoder outside the repository. The original upload, recovered archive bytes, certificates, and signer material are not distributed. The sanitized audit reports bounded content recovery; no signature or trust chain was verified.
