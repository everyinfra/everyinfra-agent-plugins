---
name: everyinfra
description: Route a task to the correct EveryInfra product and use its MCP or REST contract safely. Use when the user mentions EveryInfra generally, wants to combine multiple EveryInfra products, or is unsure whether a task belongs to EveryData, EverySearch, EveryAI, EverySolve, EveryNumber, EveryMail, or EveryProxy.
---

# EveryInfra router

Use the remote `everyinfra` MCP server for capability discovery and the four MCP-enabled product
lines. Use `https://api.everyinfra.com` only for a REST-only product. Never copy the API key into a
prompt, file, command output, log, URL query string, or response; read it from `EVERYINFRA_API_KEY`.

## Route by outcome

- Structured public platform data: EveryData.
- Current web, semantic, academic, forum, page or site retrieval: EverySearch.
- Text completion, extraction, classification, translation or summarization: EveryAI.
- Captcha or anti-bot challenge solving on a target the user is authorized to access: EverySolve.
- Activation or rental phone number: EveryNumber.
- Transactional email: EveryMail.
- Traffic-billed proxy credentials: EveryProxy.

Do not infer a tool from an old document. MCP tool discovery and the free REST catalogs are the
runtime truth. If the requested product is unavailable, report that state instead of silently
substituting a different mechanism.

## Common workflow

1. Identify the requested outcome and whether it has external side effects or a charge.
2. Use a free discovery tool or catalog before the first paid call.
3. Validate required parameters, limits, solution shape, availability and current price.
4. Invoke the paid operation only when the user's request authorizes that operation.
5. Read returned `billing`, `quota`, status and error fields when present; never infer success,
   availability, or a charge from HTTP 200 or catalog membership alone. If a tool omits billing,
   report that the charge is not observable from that response.
6. Report the useful result, the actual charge state and any remaining external action separately.

EveryInfra uses one account, API key and wallet across product lines, but product-specific scopes
may still deny a call. A scope error is not a reason to broaden or replace the key automatically.
