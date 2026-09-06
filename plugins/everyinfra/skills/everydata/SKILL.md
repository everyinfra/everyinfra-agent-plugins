---
name: everydata
description: Discover and call EveryData structured-data capabilities across social, commerce, travel, jobs, finance, reviews, and other public platforms. Use when the user needs platform profiles, posts, comments, search results, listings, reviews, or other structured public data.
---

# EveryData

Use the MCP tools `everyinfra_list_capabilities` and `everyinfra_call_api`.

1. Call `everyinfra_list_capabilities` first. Pass `platform` when the platform is already known.
2. Select the exact `platform` and `action` from the returned catalog. Read required parameters,
   optional parameters, `max_limit` and current price. Use availability only when the catalog
   actually returns it; catalog membership alone is not proof that live inventory exists.
3. Put only catalog-declared parameters under `params`. Do not pass upstream or provider-specific
   fields, and do not guess an action name.
4. Call `everyinfra_call_api`. Request the largest useful result within `max_limit` when that avoids
   needless repeated charges.
5. Treat empty, partial and failed results according to the response fields. Report the returned
   `billing` block rather than estimating cost from a stale document.

EveryData returns a normalized and redacted customer contract. Do not promise raw provider output,
provider identity, private data, or fields not present in the live capability catalog.

If the user wants model-assisted cleanup after collection, keep the result bound to its server-issued
source reference and call MCP `tools/list` first. Use source-bound cleanup only when the live server
advertises it; otherwise report it unavailable instead of sending detached data through general
chat. Preserve the source version and submit idempotency key. Field discovery exposes bounded paths
and types without example values; refresh recovery must find the original task before any new
submit. Read [the cleanup reference](../everyinfra/references/data-cleanup.md) for the prepared
15-operation boundary.
