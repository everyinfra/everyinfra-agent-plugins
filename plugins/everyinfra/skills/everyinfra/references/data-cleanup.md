# Source-bound EveryData cleanup

> Production advertises the two source-bound cleanup tools described here alongside the existing
> `everyinfra_chat` compatibility path. Always re-read the remote MCP `tools/list` and current schemas;
> service discovery does not prove that a particular account is eligible, activated or end-to-end tested.

## Route selection

- User-supplied ordinary text may use the discovered `everyinfra_chat` contract when authorized.
- An EveryData result must stay bound to its server-issued source reference/version and use the
  source-bound cleanup route. Do not detach it and call general chat to imitate the benefit.
- If the cleanup tools are absent from `tools/list`, report the route unavailable. Do not generate a
  payload or claim that a package update enabled the server.

## Live 15-operation surface

After live discovery returns the tools, read their current `inputSchema` before calling them.

| Tool | Operations | Boundary |
| --- | --- | --- |
| `everyinfra_data_cleanup_read` | `get_entitlement`, `get_source`, `get_source_fields`, `list_recipes`, `preview`, `list_jobs`, `find_job`, `get_job`, `list_units`, `get_result`, `export` | Read eligibility/policy, source version, inferred fields, recipes, preview and original task/result state. Reads do not activate or submit. |
| `everyinfra_data_cleanup_action` | `activate`, `submit`, `cancel`, `delete_result` | Explicitly begin the included period, submit with a stable idempotency key, request cancellation or delete result content. |

The initial policy is conditional and bounded, not unlimited free Gemini: a qualifying direct
account with at least CNY 500 in verified net settled recharge principal may explicitly activate
one 30-day period, limited to 1,000 successful units per UTC day, 30,000 total, 5 execute attempts
per minute and 5 concurrent units. Only the live entitlement response proves current eligibility,
activation, remaining quota and whether customer charge is zero.

## Discovery, execution and recovery

1. Call `tools/list`; confirm the cleanup tools are present and inspect both schemas.
2. Use `get_entitlement` without activating. Resolve the EveryData `source_ref`, read the server's
   `source_version`, and use `get_source_fields` for bounded path/type inference without example
   values. Field inference is selection help, not proof that a recipe will accept the value.
3. Discover fixed recipes and call `preview`. The source/version and selected fields must remain
   unchanged.
4. `activate` and `submit` are independent user-authorized actions. Persist the submit idempotency
   key and do not put it in URLs, analytics or logs.
5. After refresh, timeout or an unknown response, use `list_jobs` or `find_job` with the original
   key. A 404 does not prove the submit was never accepted; do not automatically switch keys,
   transports or fall back to chat.
6. Read `get_job`, `list_units` and `get_result` before export. Partial export, `cancel` and
   `delete_result` remain explicit choices and must not be inferred from a read request.

This contract accepts only an authorized, unexpired EveryData source and server-declared recipes.
It does not accept arbitrary chat history, custom system prompts, customer-selected models, tools,
external URLs or a free-form output schema.
