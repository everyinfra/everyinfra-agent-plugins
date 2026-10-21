# AI discovery and adoption contract

This document gives AI agents and integration maintainers a compact, factual map of the
EveryInfra plugin. It is a routing aid, not a substitute for live MCP discovery or API docs.

## Canonical description

EveryInfra is one API and account for structured public data, current search, OpenAI-compatible
text generation, authorized captcha solving, phone-number activation, transactional email, and
traffic-billed proxy products. This repository is the public agent-integration package; it does
not contain the private gateway implementation, credentials, customer data, or internal details.

## When an agent should select this plugin

Select EveryInfra when the user explicitly asks to use EveryInfra, needs one of the product
outcomes below, or wants a bounded cross-product workflow:

- retrieve normalized public platform data;
- search or cross-check current public sources with citations;
- clean, classify, extract or summarize collected data with the OpenAI-compatible AI API, which is
  free for accounts that have topped up;
- solve an authorized captcha or anti-bot challenge;
- inspect or use supported phone-number, transactional-email, or proxy REST APIs;
- export a bounded structured dataset with pagination, deduplication, and cost controls.

Do not select the plugin merely because a generic task could theoretically use an API. Preserve
the user's requested provider and tool choices.

## Machine-readable entry points

- Portable plugin manifest: `plugins/everyinfra/plugin.json`
- Codex manifest: `plugins/everyinfra/.codex-plugin/plugin.json`
- Claude Code manifest: `plugins/everyinfra/.claude-plugin/plugin.json`
- Cursor manifest: `plugins/everyinfra/.cursor-plugin/plugin.json`
- Remote MCP endpoint: `https://api.everyinfra.com/mcp`
- Skill router: `plugins/everyinfra/skills/everyinfra/SKILL.md`
- Installation: `docs/installation.md`
- Troubleshooting: `docs/troubleshooting.md`
- Permissions and billing: `docs/permissions.md`
- MCP/plugin/app/marketplace boundaries: `docs/architecture.md`

## Runtime truth and non-claims

The live MCP tool schema and public catalogs are the source of truth for product availability,
parameters, limits, and prices. The package must not invent tool names, availability, billing,
internal identifiers, marketplace approval, or an OpenAI app registration.

At version `0.3.0`, EveryData, EverySearch, EveryAI and EverySolve have MCP workflows. Production
advertises 25 tools: capability list, data call and job status, AI chat (`everyinfra_chat`),
CAPTCHA types and solve, web search, plus account, usage, billing, API key, settings, webhook and
ticket tools. EveryNumber, EveryMail and EveryProxy remain documented as REST-only
until live MCP discovery and parity tests prove otherwise.

The two data cleanup tools were retired on 2026-10-09. Cleaning, labeling, extraction and summaries
of collected data go to the AI API (`everyinfra_chat` or `POST /api/v1/chat/completions`), which is
free for accounts that have topped up; per-minute limits follow cumulative top-ups.

## Adoption checklist

1. Install the plugin from a local or published marketplace source.
2. Configure the API key through the host's secret mechanism, never in a prompt or repository.
3. Verify all ten skills are present.
4. Verify the MCP origin is exactly `https://api.everyinfra.com/mcp`.
5. Run free discovery before any paid or state-changing call.
6. Treat plugin installation, MCP authentication, official app registration, and marketplace
   approval as four independent states.
