# Changelog

All notable changes to this project are documented here. Versions follow Semantic Versioning.

## [Unreleased]

No unreleased changes.

## [0.3.0] - 2026-10-10

- Retire the data cleanup route: the two cleanup tools were removed from the remote MCP server on
  2026-10-09. Cleaning, labeling, extraction and summaries of collected data now go to the AI API
  (`everyinfra_chat` or `POST /api/v1/chat/completions`), free for accounts that have topped up.
- Remove the cleanup reference and cleanup examples from the README, skills, manifests and
  discovery files.
- Update `server.json` for the official MCP Registry entry `io.github.xiaoxihexiaoyu/everyinfra`
  1.1.0; the API key placeholder now uses the `ei_` prefix.
- Point documentation links to `https://everyinfra.com/en/docs`.
- Detect `ei_` API keys and other secret-like tokens in the validator, and check public text against
  a hashed blocklist.
- Use neutral wording for internal details in contributor, security and support documents.

## [0.2.0] - 2026-09-06

- Add discovery-first routing for the EveryData cleanup tools (retired in 0.3.0).
- Document the live two-tool, 15-operation cleanup contract, including field discovery and original-task recovery.
- Keep ordinary user-supplied text on the existing `everyinfra_chat` compatibility path.
- Add direct GitHub Release installation for the Python and Node 0.2.0 SDK attachments.
- Preserve explicit entitlement activation, stable idempotency keys, bounded quota and no-store boundaries.

## [0.1.0] - 2026-09-02

- Add Agent Plugins 1.0 portable manifest and remote MCP configuration.
- Add Codex, Claude Code, Cursor and GitHub Copilot marketplace metadata.
- Add shared EveryData, EverySearch, EveryAI, EverySolve, EveryNumber, EveryMail and EveryProxy
  skills.
- Document authorization, billing, side effects and REST-only product boundaries.
- Add a dependency-free repository validator and deterministic release builder.
- Clarify the independent MCP, plugin, registered app/connector, and marketplace layers.
- Document a comparable plugin package as a product reference without treating it as a host spec.
- Add cited cross-check research and bounded bulk-data export outcome skills.
- Add GitHub Copilot CLI environment-header authentication and tighten billing/availability claims.
- Add plugin branding assets, AI discovery guidance, troubleshooting, support, issue, and pull-request
  templates for safer public adoption.
