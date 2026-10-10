---
name: everyai
description: Use EveryInfra's OpenAI-compatible AI API through the everyinfra_chat MCP tool. Use for cleaning or labeling collected data, summarization, translation, classification, extraction, rewriting, and multi-turn text generation when the user asks to run the work through EveryInfra.
---

# EveryAI

Use the MCP tool `everyinfra_chat`.

1. Build an OpenAI-style `messages` array with only the context required for the task.
2. Use a model value only when it appears in the live MCP schema; otherwise keep the server default.
3. Do not send secrets, credentials, private source documents or personal data unless the user has
   explicitly placed that data and this processing in scope.
4. Validate the returned content against the requested format. A fluent answer is not evidence that
   a factual claim is current; use EverySearch when current verification is required.
5. AI API calls are free for accounts that have topped up and do not use the balance. If the
   response reports `ai_topup_required`, tell the user that the account needs a top-up instead of
   retrying.

For direct OpenAI-compatible SDK use, the REST base is `https://api.everyinfra.com/api/v1`; the
plugin should still prefer MCP when its tool is available.

## Cleaning collected data

The former data cleanup tools were retired on 2026-10-09. To clean, deduplicate, classify, extract
or summarize records collected with EveryData, pass the relevant fields to `everyinfra_chat`,
describe the output format, and validate the result before using it. About 20,000 tokens of input
per call is reliable; split longer inputs into chunks. Per-minute limits follow cumulative top-ups
(50 under $100, 500 from $100, 5,000 from $500, all keys on the account combined); after a
rate-limit error, wait before retrying.
