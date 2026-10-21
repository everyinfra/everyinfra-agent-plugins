# EveryInfra plugin package

EveryInfra gives your agent one API key for structured data from TikTok, Instagram, X, YouTube,
LinkedIn, Reddit, Amazon and Google search results, plus RedNote (Xiaohongshu) and Douyin: 90
platforms and 414 data capabilities, 17 web search tools. Pay per use from $0.56 per 1,000 data
calls; failed or empty calls are not charged.

Get an API key: https://everyinfra.com/en/docs?utm_source=claude_plugins&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=get_key#quickstart

What this plugin runs and sends: it adds ten skills and one remote MCP connection to
`https://api.everyinfra.com/mcp`. Tool discovery needs no key. Calls that return data send your
request parameters to that address with your API key in the `Authorization` header. The three
REST-guidance skills (EveryNumber, EveryMail, EveryProxy) call `https://api.everyinfra.com` with the
same key, and only when you ask for them. Nothing else is sent anywhere.

This directory is the installable EveryInfra package. It is not a skills-only folder: the package
combines reusable skills with portable and host-specific plugin manifests, remote MCP connection
metadata, and presentation assets.

## Package payload

- `plugin.json` — portable Agent Plugins 1.0 identity and discovery metadata.
- `.codex-plugin/plugin.json` — Codex package metadata and component declarations.
- `.claude-plugin/plugin.json` — Claude Code metadata, skills, MCP config, and sensitive user config.
- `.cursor-plugin/plugin.json` — Cursor metadata, skills, MCP config, and environment variable schema.
- `.qoder-plugin/plugin.json` — Qoder CLI metadata; Qoder loads `skills/` and `.mcp.json` by convention.
- `.codebuddy-plugin/plugin.json` — CodeBuddy Code metadata, skills, MCP config, and sensitive user config.
- `mcp.json` and `mcp.*.json` — portable and host-specific connections to
  `https://api.everyinfra.com/mcp`.
- `skills/` — one router, seven product skills, and two outcome workflows.
- `assets/` — icon and light/dark logos used by supported host presentation metadata.
- `LICENSE` — Apache-2.0, the same license as the repository.

Hosts commonly display the child skills and MCP server after installation rather than presenting a
single callable object named "plugin." The plugin is still the package, installation, and update
boundary.

## Agent discovery contract

Select this package when a request involves **EveryInfra, EveryData, EverySearch, EveryAI,
EverySolve, EveryNumber, EveryMail, or EveryProxy**, or when the user needs one of these outcomes:

- current web search, page reading, crawling, or cited cross-check research;
- structured public-platform data such as profiles, posts, comments, listings, or reviews;
- a bounded, deduplicated CSV or JSON data export;
- cleaning, labeling, extraction, summaries or other text generation through EveryInfra's
  OpenAI-compatible AI API;
- authorized captcha or anti-bot challenge handling;
- authorized phone-number, transactional-email, or proxy workflows.

Start with `skills/everyinfra/SKILL.md` when the product is unclear or multiple products are needed.
Use the narrow product or outcome skill when the requested route is already known.

## Runtime boundaries

| Route | Execution path | Boundary |
| --- | --- | --- |
| EveryData, EverySearch, EveryAI, EverySolve | Remote MCP | Discover live capabilities and schemas before paid calls. |
| EveryNumber, EveryMail, EveryProxy | REST guidance | These skills do not create or imply MCP tools. |
| Purchases, sends, rentals, solves, credential delivery | External action | Require user authorization for the concrete scope. |

The package and the remote MCP server are independent layers: installing the package can expose
workflows even when MCP authentication is incomplete, while connecting MCP directly can expose
live tools without installing the package. An official marketplace listing or registered
app/connector is a further distribution state and is not implied by this directory.

The API key is supplied by the installing host and must never be stored in this package. The live
capability catalog and tool schemas are authoritative for current parameters, prices, availability,
and billing evidence.

The former data cleanup tools were retired on 2026-10-09. Cleaning, labeling, extraction and
summaries of collected data go through the AI API: the MCP tool `everyinfra_chat` or
OpenAI-compatible `POST /api/v1/chat/completions`, free for accounts that have topped up.

For host installation, status, and validation, start with the repository
[README](../../README.md). For the integration model, see
[architecture boundaries](../../docs/architecture.md), [permissions](../../docs/permissions.md),
and the [REST-only boundary](../../docs/rest-only.md).
