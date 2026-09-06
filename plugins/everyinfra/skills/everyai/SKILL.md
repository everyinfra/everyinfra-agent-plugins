---
name: everyai
description: Use EveryInfra's OpenAI-compatible text completion through the everyinfra_chat MCP tool. Use for summarization, translation, classification, extraction, rewriting, and multi-turn text generation when the user asks to run the work through EveryInfra.
---

# EveryAI

Use the MCP tool `everyinfra_chat`.

1. Build an OpenAI-style `messages` array with only the context required for the task.
2. Use a model value only when it appears in the live MCP schema; otherwise keep the server default.
3. Do not send secrets, credentials, private source documents or personal data unless the user has
   explicitly placed that data and this processing in scope.
4. Validate the returned content against the requested format. A fluent answer is not evidence that
   a factual claim is current; use EverySearch when current verification is required.
5. Report billing only when the response actually contains billing evidence. The current MCP chat
   tool returns generated content but may omit the REST billing envelope; in that case state that
   the charge was not observable from this MCP result instead of inventing an amount or status.

For direct OpenAI-compatible SDK use, the REST base is `https://api.everyinfra.com/api/v1`; the
plugin should still prefer MCP when its tool is available.

## Source-bound EveryData cleanup

First distinguish ordinary user-supplied text from post-processing of an EveryData result.

- Ordinary text may use `everyinfra_chat` only while it remains in live discovery and the requested
  processing is authorized.
- For an EveryData result, call MCP `tools/list` first. If the server does not advertise source-bound
  cleanup, report it unavailable and do not send the result through general chat as a substitute.
- If cleanup is live, read the current schemas, then inspect entitlement, source/version, inferred
  fields and fixed recipes before preview. Activation and submission are separate explicit actions.
- Preserve the original submit idempotency key. After interruption or an unknown response, list
  tasks or find the original task with that same key before any new submit; 404 is not proof that
  the earlier request was never accepted.
- Inspect job, unit and result state before export. Partial export, cancellation and result deletion
  remain separate user choices.

The prepared schema has 15 operations and a bounded qualifying-account policy, but these are not
runtime claims. For the operation inventory, limits and discovery boundary, read
[the cleanup reference](../everyinfra/references/data-cleanup.md) when this route is requested.
