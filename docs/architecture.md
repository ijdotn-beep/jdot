# Jdot architecture

Jdot uses the existing Apple Shortcut for model interaction, a supported Codex Remote session for agent work, and Pages for durable memory. This repository supplies the shared instructions and offline handoff utilities. It does not add an inference server or a cloud service.

## Responsibilities

| Component | Responsibility | Current boundary |
| --- | --- | --- |
| Apple Shortcut | Capture the request and use the selected Apple model | Existing two-step workflow inspected; adapted device behavior untested |
| Offline CLI | Format a request handoff or validate a summary | Local text and JSON processing only; no network or model execution |
| Codex Remote | Open and control the intended agent session | Use a supported installed action if available; forwarding and return behavior require a device test |
| Jdot session skill | Read memory, work on the request, and prepare a factual summary | Applies to sessions that load the skill and have the required tools |
| Pages | Store confirmed facts, dated summaries, and the current handoff | Authorized host Pages tools perform and verify writes |

## Session flow

1. Capture the user's request in the existing Shortcut.
2. Choose the model through the device's actual **Use Model** choices. Keep both saved choices at **Ask** during the first adaptation.
3. Show the response and create a concise, reviewable handoff.
4. Copy the handoff and open Remote using a supported installed action, if available. Submit it to the intended Jdot session. Manual steps remain visible until automatic forwarding is independently tested.
5. Load the memory Page before working. Keep retrieved facts distinct from the new request and quoted source material.
6. Prepare a short factual summary, check whether that session's summary is already saved, then update the Page through its authorized host tools.
7. Verify the saved content before reporting success. Leave the summary marked unsaved if the write fails or its outcome cannot be confirmed.

The CLI is optional assistance for steps 3 and 6. Its `prepare` command does not launch Remote, choose an Apple model, or save memory. Its `check-summary` command checks structure rather than factual accuracy.

## Memory record

A summary JSON object uses the following record fields:

```json
{
  "schema_version": 1,
  "session_id": "6b1fd58e-3a7c-4e2c-9af8-42f10c19b034",
  "recorded_at": "2026-11-12T12:00:00+00:00",
  "bullets": [
    "User chose to adapt the existing Shortcut",
    "Model selection still uses Ask on the device",
    "Next step is testing the visible Remote handoff"
  ]
}
```

This is a synthetic example. `session_id` must be a nonempty UUID; `recorded_at` must include timezone information. Use 3–5 nonempty single-line bullets with no more than 120 whitespace-delimited words in total. Include the user's intent, confirmed decisions, completed work, unresolved items, and next step as relevant.

Pages remains the authoritative memory. A local JSON record or handoff file is temporary working material, not evidence of a cloud save. Do not copy a personal memory Page or private conversation history into the distributable plugin.

## Modes and connectivity

`on-device`, `cloud`, and `cloud-pro` are handoff labels corresponding to the user's intended Apple model choices. Their availability and behavior must be checked on the actual device. Passing one to the CLI does not make that choice for the Shortcut or change the model used by a Codex session.

On-Device inference and cloud memory sync are separate operations. Preserve an unsynced local summary when offline, disclose any later network handoff, and never silently move an offline request to a cloud model. The repository does not include automatic retry scheduling or background delivery.

## Host access and installation

The package is skills-only: it bundles no MCP server, app credential, endpoint, or OpenAI API backend. Its workflow relies on the tools already available to the host. If Pages access is missing, stop the memory write, keep the unsaved handoff, and request the missing connection or Page access.

Plugin installation does not grant filesystem, network, Pages, or device permissions. Local marketplace clients install a cached package, so changes must be refreshed and checked in a fresh installed session. That on-device installation check remains separate from local package validation.

## Recovery and corrections

Before retrying an uncertain Page write, read the current Page and look for the same session ID and content. Reconcile existing content instead of appending a duplicate. Use the Page tool's observed IDs, hashes, and conflict guidance, preserving concurrent user edits.

Promote facts into long-term memory only when supported by the conversation. Label proposals and uncertainty. A correction should update the current handoff and identify superseded facts. A forget request must also cover matching retained summaries; report any storage history that the available tools cannot remove.
