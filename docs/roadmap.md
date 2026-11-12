# Jdot long-term plan

Build a small working memory loop first, then add convenience only after the underlying connection is demonstrated. Pages remains the authoritative memory throughout.

## Stage 1 Memory foundation

Keep the confirmed goal, user decisions, short session summaries, and latest handoff in a private Page. Connected Jdot sessions should read this context before work and save a verified factual summary afterward.

Completion check: save a dated decision, then retrieve it correctly in a fresh Page-connected session. A fresh-agent read has demonstrated saved-memory retrieval during setup; this is separate from a complete device-to-Remote test.

## Stage 2 Adapt the existing Shortcut

Use the inspected two-step **Use Model** workflow as the starting point. Add explicit request capture and a reviewable handoff while keeping **Ask** model selection initially. Use a supported installed Remote-opening action only after confirming it exists on the device.

Completion check: a request reaches the intended Jdot session, that session reads its Page, and the resulting summary is saved and read back. Record every manual transfer step. Do not claim automatic forwarding until it has been tested.

## Stage 3 Verify the three modes

Check the actual On-Device, Cloud, and Cloud Pro choices in Apple Shortcuts. Keep the selected Apple mode distinct from the model used by the remote agent. Document when connectivity is needed for inference, request transfer, and memory storage.

Completion check: test the same small request through each available mode and perform an offline attempt. An unavailable mode should remain unavailable rather than silently selecting a different provider or tier.

## Stage 4 Make memory dependable

Add evidence-backed retry handling, summary deduplication, compact current context, corrections, and forgetting as the workflow matures. Keep confirmed durable facts distinct from temporary session notes and assistant proposals.

Completion checks:

- An interrupted or uncertain save is reconciled before a retry, creating one summary for the session
- A corrected fact replaces stale current context while identifying superseded information
- A forget request covers current context and matching retained summaries, with any tool-imposed history limit reported
- A failed save leaves a clear unsaved summary instead of a false success claim

The offline handoff tool supports `prepare --session-id UUID` to preserve a
session's identity when regenerating its text. The summary validator checks record
shape and length. Neither implements these remote delivery guarantees; uncertain
Page saves still require reconciliation by the connected agent.

## Stage 5 Optional dashboard and maintenance

Consider a private Sites dashboard only after one full request → Remote → Page save → fresh-session retrieval cycle works. A dashboard may expose current projects, recent summaries, pending handoffs, and connection status. Preserve Pages as canonical memory unless the user explicitly chooses a different design.

Scheduled maintenance is a separate future decision with a specific purpose, schedule, and authorized data source. A Page, plugin, or saved plan is not an always-on process. Do not enable background work simply to satisfy an availability label.

## Repository verification

Run the unit tests and plugin validator, build the archive twice, compare the resulting bytes or SHA256 hashes, extract a fresh copy, and validate that copy. Keep the original signed Shortcut, personal memory Page, local configuration, and credentials out of distributable archives.

Package validation, local installation, device execution, GitHub publication, and public Plugin Directory approval are different states. This repository makes no publisher, legal, marketplace approval, or live-connection claims.
