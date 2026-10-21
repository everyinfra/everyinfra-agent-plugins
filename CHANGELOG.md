# Changelog

All notable changes to this project are documented here. Versions follow Semantic Versioning.

## [Unreleased]

## [0.4.0] - 2026-10-22

- Rework the README first screen: keyword title, badges, a platform table, "Listed on" directories and a one-minute setup for Claude Code and Cursor; replace the outdated "No submission or listing" status row.
- Cursor manifest: platform-led description and the repository logo.

- Add WorkBuddy connector packages under `workbuddy/`: the main `everyinfra` connector (capability
  discovery, data calls and web search, with four workflow skills and twelve platform skills) and six
  optional single-platform connectors. Users connect with their own API key through WorkBuddy's token
  form; AI chat and CAPTCHA tools are hidden in this package. Prepared and validated, not submitted.
- Add `scripts/build_workbuddy.py` to render, check and package the WorkBuddy connectors, and run its
  check in CI.
- Add host manifests so more agent hosts install from this repository: Qoder CLI
  (`plugins/everyinfra/.qoder-plugin/plugin.json`, `.qoder-plugin/marketplace.json`), CodeBuddy Code
  (`plugins/everyinfra/.codebuddy-plugin/plugin.json`, `.codebuddy-plugin/marketplace.json`) and
  Kimi Code (root `.kimi-plugin/plugin.json`).
- Add `host-packages/` and `scripts/build_host_packages.py` for markets that take uploads: MiniMax
  (CN and US ZIPs), Qoder/QoderWork skills and the "EveryInfra Data Researcher" expert kit, and
  ClawHub skills with a publish script. Skill bodies come from the shared skills; CI runs the check.
  Prepared and validated, not submitted.
- Add `llms-install.md` and `plugins/everyinfra/LICENSE`; the plugin README now states what the
  plugin sends and where.
- Tag outbound links with their source: README links use `utm_source=github_readme`, the Registry
  `websiteUrl` uses `utm_source=mcp_registry`, WorkBuddy key links use `utm_source=workbuddy` with
  one `utm_content` per connector. `server.json` is 1.1.1 for the next Registry publish.
- Update the README to the current catalog: 90 platforms, 414 data capabilities, 17 web search
  tools, 52 CAPTCHA types, from $0.56 per 1,000 data calls, and the 25 tools the MCP server
  advertises.

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
