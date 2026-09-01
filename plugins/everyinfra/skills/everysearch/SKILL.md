---
name: everysearch
description: Use EverySearch for current web, semantic, academic, forum, page-reading, crawling, and cross-check retrieval. Use when a task needs up-to-date sources, multiple retrieval mechanisms, cited factual verification, or content from a specific public URL or site.
---

# EverySearch

Use the MCP tool `everyinfra_search`. Its live input schema is the source of truth for available
`tool` values and parameters.

- Use the narrowest retrieval mechanism that matches the user's question.
- Use `crosscheck` for a concrete claim such as a current version, price, policy, availability, or
  API behavior. It is designed to compare mechanism-distinct retrieval paths.
- Use page-reading or crawl tools for known URLs instead of searching for the same page again.
- Keep query and result limits proportional to the task. Empty or failed results must not be
  presented as proof that nothing exists.
- Cite the original sources returned by the search result when producing factual conclusions.
- Read the returned `billing` state. Failed or empty calls may be uncharged, but do not infer that
  without the response.

Do not silently replace semantic retrieval with keyword retrieval when result meaning matters.
If the requested tool is not in the current MCP schema, state that it is unavailable.
