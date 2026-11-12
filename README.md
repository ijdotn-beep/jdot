# Jdot

[GitHub repository](https://github.com/ijdotn-beep/jdot)

A lightweight personal assistant workflow for **Apple Shortcuts → Codex Remote → Pages memory**.

This repository packages Jdot session guidance, a Shortcut adaptation guide, and offline handoff tools. It starts from an existing two-step **Use Model** Shortcut. Pages remains the authoritative memory, with short factual summaries after connected Jdot sessions.

## Current capabilities

- Prepare a text handoff locally for an On-Device, Cloud, or Cloud Pro request
- Validate the shape and length of a session summary before saving it
- Guide a Page-connected agent through reading memory, working on the request, saving a summary, and checking the save
- Package the Jdot skills for local plugin installation

The handoff tool makes no network requests and does not select or run a model. Remote opening, request transfer, and device model choices still require setup and testing. There is no always-on background engine or automatic cross-app memory sync.

## Start with the existing Shortcut

Inspection recovered a workflow containing two **Use Model** steps. Both defer model selection to **Ask**. The first saved prompt is empty; the second receives the first response. The export contains no Remote launch, network request, Pages update, or automation.

**Workflow content recovered; signature and trust chain not verified.** The original signed export and its signer material are excluded from this repository. See the [sanitized audit](docs/shortcut-audit.json) and [adaptation guide](docs/shortcut-adaptation.md).

The next step is to open that Shortcut in Apple Shortcuts, add explicit request capture, and test the existing model choices before adding a visible Remote handoff.

## Local checks

Use Python 3 with the repository's scripts:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_plugin.py plugins/jdot --json
python3 scripts/package_plugin.py plugins/jdot dist/jdot-plugin.zip --json
```

These commands test local behavior and package structure. They do not verify Apple Shortcuts, a connected Remote host, Pages permissions, or installation in ChatGPT.

## Prepare a handoff

Create a request text file in the ignored `.jdot/` directory and set `JDOT_PAGE_URL` to your own memory Page URL. Keep personal Page URLs and request text outside version control.

```sh
mkdir -p .jdot
python3 scripts/jdot_handoff.py prepare \
  --mode on-device \
  --request-file .jdot/request.txt \
  --page-url "$JDOT_PAGE_URL" > .jdot/handoff.txt
```

Use `cloud` or `cloud-pro` for the other requested modes. The mode labels describe the intended Shortcut choice; the CLI does not route inference. Review the resulting text, copy it to the intended Page-connected Jdot session, and use the installed Remote-opening action if your device offers one.

Reuse the saved handoff when retrying the same session. Each new `prepare` invocation generates a new session ID.

For a summary prepared by the agent:

```sh
python3 scripts/jdot_handoff.py check-summary .jdot/summary.json
```

Passing validation means the summary meets the local schema. It does not mean the summary is true or saved to Pages. The connected agent must make the authorized Page edit and verify the result.

## Install the skills locally

The plugin lives at `plugins/jdot`; the repository marketplace is `.agents/plugins/marketplace.json`. Open this repository with a compatible ChatGPT desktop or Codex client, refresh the local marketplace, and install Jdot through the Plugins Directory. A local installation uses a cached copy, so refresh or reinstall after changes and test in a fresh chat.

The included skills are:

- **jdot-session** — load memory, handle a request, and save a verified factual summary; its setup reference covers adapting the existing Shortcut
- **host-workspace-operator** — use the host's available workspace tools within the requested scope
- **sandbox-python-executor** — use available Python execution for deterministic checks

The package supplies guidance, not permissions or a Pages connection. Enable the Pages plugin and grant the session access to the intended Page. A fresh installed-plugin session has not been tested on the user's device.

## Configuration and memory

Copy the portable example at `config/jdot.example.json` to ignored local configuration at `.jdot/config.json` and replace its placeholders. The CLI uses its explicit flags; the example configuration is a setup reference, not an automatically loaded settings file.

Summary records use `schema_version: 1`, a UUID `session_id`, a timezone-aware ISO 8601 `recorded_at`, and `bullets` containing 3–5 nonempty single-line strings totaling at most 120 whitespace-delimited words. Keep proposals separate from confirmed user facts and use the session ID when checking for duplicate saves.

On-Device inference can be offline while Pages memory is in the cloud. A later Remote handoff or Page save needs connectivity and should stay visible. An offline summary remains unsaved until the authorized cloud save succeeds. No separate OpenAI API backend or API key is required for this repository's workflow.

Read the [architecture](docs/architecture.md), [Shortcut setup steps](docs/shortcut-adaptation.md), and [long-term plan](docs/roadmap.md) for the implementation boundary and device acceptance checks.
