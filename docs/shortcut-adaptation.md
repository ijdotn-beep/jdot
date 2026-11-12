# Adapt the existing Use Model Shortcut

The starting Shortcut contains two **Use Model** steps. Both saved model choices use **Ask**. The first saved prompt is empty; the second references the first response through one unique response identifier. No Remote-opening step, network request, Pages edit, or automation was found.

**Workflow content recovered; signature and trust chain not verified.** The inspection recovered content from an AEA1 profile 0 signed container with one LZVN block. It did not execute the Shortcut or establish what model the user selected during a past run. The [sanitized audit](shortcut-audit.json) records the inspection without distributing the signed upload or signer material.

## Preserve the starting point

Duplicate the Shortcut in Apple Shortcuts before editing so the original remains available for comparison. Use the Shortcuts editor on the intended device. This repository does not re-sign or install a replacement Shortcut.

## Add explicit request capture

1. Add a visible text request step before the first **Use Model** step, using typed or dictated text as appropriate for the device.
2. Connect that captured request to the first prompt so its content is explicit rather than relying on an empty saved prompt.
3. Keep both model choices at **Ask** initially. Confirm the available On-Device, Cloud, and Cloud Pro choices on the device before fixing any model choice.
4. Keep the second step connected to the first response. Review its prompt so it produces a useful concise answer or handoff rather than assuming the existing chaining already provides persistent memory.

The empty saved prompt does not prove that a previous live request was empty. Runtime context and the saved workflow are different evidence.

## Make the handoff visible

1. Show the model response to the user.
2. Prepare a concise handoff containing the user's request, the selected mode, the useful response, and the instruction to load the configured Jdot memory Page.
3. Copy the handoff text for review and submission to the intended Jdot session.
4. Look for the installed ChatGPT or Codex action that opens Remote on that device. Use it only if it is actually available. Do not invent a deep link or internal action identifier.
5. Open the intended Remote host and session, then submit the copied handoff. Keep that submission manual until automatic prompt transfer and the response path have both been demonstrated.

The local formatter can help prepare text:

```sh
python3 scripts/jdot_handoff.py prepare \
  --mode cloud \
  --request-file .jdot/request.txt \
  --page-url "$JDOT_PAGE_URL"
```

This command prints text only. It does not run Shortcuts, send a request, open Remote, or write Pages.

## Save memory through the connected session

Start a Page-connected Jdot session with the handoff. The agent should load the memory Page, complete the requested work, and prepare a dated factual summary of 3–5 bullets totaling no more than 120 whitespace-delimited words.

Use a stable session UUID when checking for an already-saved summary. Validate a JSON summary with `check-summary` when useful, then use the host Pages tools to save it. Confirm the saved content before saying it was remembered. Local validation alone is not a Page save.

## Device acceptance checks

- A typed request visibly reaches the first model step, and the second step receives the first response.
- The available model choices are recorded from the device; an On-Device choice is not silently escalated to a cloud model.
- An offline attempt clearly separates local inference from unavailable Remote or Pages access and preserves an unsaved handoff.
- The Remote-opening action reaches the intended host and session. Opening the app alone is not proof of request transfer.
- A submitted handoff causes the Page-connected session to load the intended memory and save a summary that can be read back.
- Repeating a handoff does not create a duplicate saved summary.

Device execution, model availability, Remote forwarding, and an installed-plugin smoke test remain unverified until these checks are performed on the intended device.
