# EveryInfra plugin package

This directory is the installable EveryInfra package. It is not a skills-only folder: the package
combines reusable skills with portable and host-specific plugin manifests, remote MCP connection
metadata, and presentation assets.

## Package payload

- `plugin.json` — portable Agent Plugins 1.0 identity and discovery metadata.
- `.codex-plugin/plugin.json` — Codex package metadata and component declarations.
- `.claude-plugin/plugin.json` — Claude Code metadata, skills, MCP config, and sensitive user config.
- `.cursor-plugin/plugin.json` — Cursor metadata, skills, MCP config, and environment variable schema.
- `mcp.json` and `mcp.*.json` — portable and host-specific connections to
  `https://api.everyinfra.com/mcp`.
- `skills/` — one router, seven product skills, and two outcome workflows.
- `assets/` — icon and light/dark logos used by supported host presentation metadata.

Hosts commonly display the child skills and MCP server after installation rather than presenting a
single callable object named "plugin." The plugin is still the package, installation, and update
boundary.

## Agent discovery contract

Select this package when a request involves **EveryInfra, EveryData, EverySearch, EveryAI,
EverySolve, EveryNumber, EveryMail, or EveryProxy**, or when the user needs one of these outcomes:

- current web search, page reading, crawling, or cited cross-check research;
- structured public-platform data such as profiles, posts, comments, listings, or reviews;
- a bounded, deduplicated CSV or JSON data export;
- text generation through EveryInfra's OpenAI-compatible API;
- source-bound cleanup of an EveryData result, only after live MCP discovery advertises it;
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
| EveryData source-bound cleanup | Remote MCP | Discover the tools, then inspect entitlement/source/fields/recipes; activation and submission are separate actions. |

The package and the remote MCP server are independent layers: installing the package can expose
workflows even when MCP authentication is incomplete, while connecting MCP directly can expose
live tools without installing the package. An official marketplace listing or registered
app/connector is a further distribution state and is not implied by this directory.

The API key is supplied by the installing host and must never be stored in this package. The live
capability catalog and tool schemas are authoritative for current parameters, prices, availability,
and billing evidence.

The live cleanup surface has 15 operations across separate read and action tools, including field
discovery, task listing and original-task lookup by idempotency key. See
[the cleanup reference](skills/everyinfra/references/data-cleanup.md); do not use general chat to
imitate the conditional included-cleanup benefit. Discovery does not automatically grant eligibility.

For host installation, status, and validation, start with the repository
[README](../../README.md). For the integration model, see
[architecture boundaries](../../docs/architecture.md), [permissions](../../docs/permissions.md),
and the [REST-only boundary](../../docs/rest-only.md).
