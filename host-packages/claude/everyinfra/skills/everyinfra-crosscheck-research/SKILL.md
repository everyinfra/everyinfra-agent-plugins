---
name: everyinfra-crosscheck-research
description: Verify a current factual claim or produce a cited research answer through EverySearch crosscheck. Use when the user needs mechanism-distinct retrieval, source comparison, freshness checks, or an evidence-backed conclusion rather than a simple result list.
---

# EveryInfra cross-check research

Use the `everyinfra_search` MCP tool with the live `crosscheck` schema. This skill owns the research
outcome; `everysearch` remains the product-level reference.

1. Turn the request into one concrete claim or decision question. Preserve any date, jurisdiction,
   product version, or site scope that determines whether a source is relevant.
2. Use `crosscheck` so retrieval mechanisms remain independent. Do not silently replace a failed
   mechanism with duplicate keyword searches and call that corroboration.
3. Inspect the original URLs, source dates, and—when news is involved—the date the event happened.
   Prefer primary sources for technical, policy, product, and organizational claims.
4. Separate agreement, contradiction, and missing evidence. A missing or empty path is uncertainty,
   not proof that the claim is false.
5. State the conclusion at the strength the evidence supports and cite the original sources, not a
   search-result wrapper.
6. Report billing only when the tool result exposes billing evidence. Do not infer a charge from a
   catalog price or HTTP success.

Keep the query and result limits proportional to the decision. If the live MCP schema does not
offer `crosscheck`, report that limitation and use the narrowest available EverySearch mechanism
without describing it as an equivalent cross-check.
