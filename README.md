# EveryInfra MCP Server & Agent Plugin — TikTok, Instagram, Amazon, Xiaohongshu & SERP Data API

[![Validate public plugin package](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Plugin version](https://img.shields.io/badge/plugin-v0.4.0-287A73.svg)](CHANGELOG.md)
[![EveryInfra MCP connector on Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra/badges/score.svg)](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra)

**One API key and one MCP endpoint for public web data: 414 data capabilities across 90 platforms, 17 web search tools, CAPTCHA solving for 52 types and an OpenAI-compatible AI API that is free after a top-up. Pay per use from $0.56 per 1,000 data calls; failed or empty calls are not charged.** Works with Claude Code, Cursor, Codex and any MCP client.

**一个 Key、一个 MCP 地址，拿到小红书、抖音、淘宝、京东、1688、B站、微博、公众号和 TikTok、Instagram、Amazon 的公开数据；失败和空结果不扣费。** 中文介绍：[万有引擎 EveryInfra](https://everyinfra.com/mcp-server?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=zh)。

| Social & video | E-commerce | Search & more |
| --- | --- | --- |
| [TikTok](https://everyinfra.com/en/tiktok-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=tiktok) · [Instagram](https://everyinfra.com/en/instagram-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=instagram) · [YouTube](https://everyinfra.com/en/youtube-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=youtube) · [X / Twitter](https://everyinfra.com/en/twitter-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=twitter) · [Reddit](https://everyinfra.com/en/reddit-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=reddit) · [LinkedIn](https://everyinfra.com/en/linkedin-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=linkedin) | [Amazon](https://everyinfra.com/en/amazon-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=amazon) · [Taobao 淘宝](https://everyinfra.com/en/taobao-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=taobao) · [JD 京东](https://everyinfra.com/en/jd-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=jd) | [Google SERP & web search](https://everyinfra.com/en/products/search?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=search) · [CAPTCHA solving](https://everyinfra.com/en/captcha?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=captcha) · [OpenAI-compatible AI API](https://everyinfra.com/en/products/ai?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=ai) |
| [Xiaohongshu / RedNote 小红书](https://everyinfra.com/en/xiaohongshu-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=xiaohongshu) · [Douyin 抖音](https://everyinfra.com/en/douyin-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=douyin) · [Bilibili B站](https://everyinfra.com/en/bilibili-api?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=bilibili) | | [All platforms →](https://everyinfra.com/en/market?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=market) |

**Listed on:** [Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra) · [Smithery](https://smithery.ai/servers/everyinfra/api) · [Cursor Directory](https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data) · [ModelScope 魔搭 MCP 广场](https://www.modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra) · official MCP Registry (`io.github.xiaoxihexiaoyu/everyinfra`)

### Connect in one minute

Get an API key at [everyinfra.com](https://everyinfra.com/en/docs?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=connect_get_key#quickstart), then add the remote MCP server:

```bash
# Claude Code
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp \
  --header "Authorization: Bearer $EVERYINFRA_API_KEY"
```

```json
// Cursor: ~/.cursor/mcp.json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": { "Authorization": "Bearer ${EVERYINFRA_API_KEY}" }
    }
  }
}
```

Tools are named `everyinfra_*`. Ask your agent things like *"Get the latest 20 TikTok videos for #skincare as a table"* or *"小红书搜「露营装备」，导出前 50 条笔记的点赞和评论数"*. Full plugin install for Claude Code, Codex, Cursor and other hosts is in [Quick start](#quick-start).

---

> This repository packages the EveryInfra agent plugin (10 skills) and the remote MCP connection metadata. Product pages: [MCP server](https://everyinfra.com/en/mcp-server?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=mcp_server) · [Pricing](https://everyinfra.com/en/pricing?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=pricing) · [Docs](https://everyinfra.com/en/docs?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=docs).

Install one package to give an AI agent reusable EveryInfra workflows **and** the metadata needed
to connect to EveryInfra's remote MCP server. The repository supports Codex, Claude Code, Cursor,
GitHub Copilot-compatible clients, Qoder CLI, CodeBuddy Code, Kimi Code, and hosts that implement
Agent Plugins 1.0.

This is a plugin repository, not a copy of the EveryInfra backend. It contains:

- 10 discoverable skills: one router, seven product skills, and two outcome workflows;
- remote MCP connection metadata for `https://api.everyinfra.com/mcp`;
- host-specific plugin manifests for Codex, Claude Code, Cursor, Qoder, CodeBuddy, and Kimi;
- self-hosted marketplace manifests for Codex, Claude Code, Cursor, GitHub Copilot, Qoder, and
  CodeBuddy;
- package sources for markets that take uploads (MiniMax, Qoder/QoderWork, ClawHub) under
  `host-packages/`;
- presentation assets and safety boundaries for paid calls, credentials, billing, and external side
  effects.

No API key, customer data, credential, or private gateway source code belongs in this repository.

> **Update (2026-10-09):** the two data cleanup tools have been retired. To clean, classify,
> extract or summarize the data you collect, use the [AI API](https://everyinfra.com/en/products/ai?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=ai_update):
> OpenAI-compatible `POST /api/v1/chat/completions`, also available as the MCP tool
> `everyinfra_chat`. It is free for accounts that have topped up, with per-minute limits that follow
> cumulative top-ups. From version 0.3.0 the skills in this package route that work to the AI API.

## MCP or plugin?

| If you need... | Choose | What you get |
| --- | --- | --- |
| Live tools only | MCP | A direct connection to the remote server and its current tool schemas. |
| Reusable routing and task workflows | Plugin | Skills plus host discovery metadata; the package can also declare an MCP connection. |
| Application or CI integration | REST or SDK | Programmatic access that does not depend on an agent host. |
| Catalog discovery and updates | Marketplace | A pointer to the plugin package; a marketplace does not execute tools. |

MCP and plugins are different layers. MCP is the runtime protocol for live tools, resources,
prompts, and server instructions. A plugin is an installable package that can bundle skills, MCP
connection metadata, hooks, UI assets, and host-specific discovery metadata. Either layer can be
used without the other.

### Why a host may show only Skills

Many hosts surface the installed package through its components rather than as one callable
"plugin." Seeing `everyinfra`, `everysearch`, or the other child skills in an agent's skill list is
expected; the plugin remains the installation and update unit. Check the host's plugin list for the
package and its MCP list for the live server connection. A visible skill does not, by itself, prove
that the MCP connection is authenticated or that an official marketplace has listed the package.

See [MCP, plugin, app, and marketplace boundaries](docs/architecture.md) for the full model.

## What agents can use it for

The package is designed to be discovered from either the product name or the requested outcome.
Example requests include:

- "Find current sources for this claim and cross-check them."
- "Discover the right public-data capability, then export a bounded CSV."
- "Search public profiles, posts, comments, listings, or reviews as structured data."
- "Run this text task through EveryAI."
- "Clean and label these collected comments with the AI API, and return JSON."
- "Solve this captcha for a target I am authorized to automate."
- "Inspect available phone-number, transactional-email, or proxy options before I approve an
  order or send."

AI discovery terms include: **EveryInfra, EveryData, EverySearch, EveryAI, EverySolve,
EveryNumber, EveryMail, EveryProxy, MCP, web search, cited research, structured public data,
social data, ecommerce data, bulk export, captcha, phone verification, transactional email, and
proxy API**.

For an AI agent:

1. Use the `everyinfra` router when the user names EveryInfra, needs more than one product, or has
   not chosen a product.
2. Use a product skill directly when the requested outcome is unambiguous.
3. Discover live MCP capabilities and schemas before inventing parameters or estimating cost.
4. Treat purchases, sends, rentals, captcha solves, and credential delivery as explicit external
   actions. A read or draft request is not authorization to execute them.
5. Keep EveryNumber, EveryMail, and EveryProxy on their documented REST paths until live MCP
   discovery proves otherwise.

## Capability matrix

| Product or workflow | Package entry | Runtime path | Typical outcome |
| --- | --- | --- | --- |
| EveryInfra | `everyinfra` | Router | Choose the correct product and execution boundary. |
| EveryData | `everydata` | MCP | Discover and retrieve structured public-platform data. |
| EverySearch | `everysearch` | MCP | Search, read, crawl, and cross-check current public sources. |
| EveryAI | `everyai` | MCP | Run OpenAI-compatible text generation through EveryInfra. |
| EverySolve | `everysolve` | MCP | Handle an authorized captcha or anti-bot challenge. |
| EveryNumber | `everynumber` | REST guidance | Inspect or operate authorized number activation and rental flows. |
| EveryMail | `everymail` | REST guidance | Inspect, draft, schedule, or send transactional email with authorization. |
| EveryProxy | `everyproxy` | REST guidance | Inspect packages, order, and retrieve credentials with authorization. |
| Cross-check research | `everyinfra-crosscheck-research` | MCP workflow | Produce an evidence-backed answer from distinct retrieval paths. |
| Bulk data export | `everyinfra-bulk-data-export` | MCP workflow | Export bounded, deduplicated CSV or JSON with cost controls. |

The live capability catalog and tool schemas are authoritative. The package must not invent an MCP
tool name, current price, availability state, or billing result.

### AI API route

Use the MCP tool `everyinfra_chat`, or REST `POST https://api.everyinfra.com/api/v1/chat/completions`
with any OpenAI SDK (`base_url` = `https://api.everyinfra.com/api/v1`, same API key). It is free for
accounts that have topped up; per-minute limits follow cumulative top-ups (50 under $100, 500 from
$100, 5,000 from $500, all keys combined). It is meant for organizing the data you collect with
EveryInfra.

## Status: what exists today

| Layer | Repository state | What is not implied |
| --- | --- | --- |
| Remote MCP | Production advertises 25 tools at `https://api.everyinfra.com/mcp`: capability list, data call and job status, AI chat, CAPTCHA types and solve, web search, plus account, usage, billing, API key, settings, webhook and ticket tools. | Discovery is not proof that an account is authenticated or has the balance or top-up a call requires. |
| Plugin package | Portable and host-specific manifests, skills, MCP metadata, and assets are present. | Presence is not a clean-host installation test. |
| Repository validator | Cross-host JSON, path, skill, MCP, and credential-safety checks are available. | Repository validation is not marketplace approval. |
| Self-hosted catalogs | Six marketplace manifests (Codex, Claude Code, Cursor, GitHub Copilot, Qoder, CodeBuddy) and a Kimi Code root manifest are present in this repository. | A catalog file is not an official listing. |
| Market upload packages | MiniMax (CN and US), Qoder/QoderWork skills and expert kit, and ClawHub skills are built from `host-packages/` and pass `scripts/build_host_packages.py check`. | Not submitted to or approved by any of these markets. |
| OpenAI registered app | No `.app.json` or host-issued app ID is included. | Direct MCP metadata is not a registered ChatGPT connector. |
| Directories | Listed on Glama, Smithery, Cursor Directory, ModelScope and the official MCP Registry (links at the top). | A directory listing is not an official Codex, Claude or Cursor marketplace approval. |
| WorkBuddy connectors | Connector packages for the WorkBuddy open platform are prepared under `workbuddy/` and pass `scripts/build_workbuddy.py check`. | Not submitted to or approved by WorkBuddy. |

Release claims should distinguish **prepared**, **validated**, **installed**, **submitted**, and
**listed**. Do not collapse them into one status.

## Quick start

### Get an API key

1. Sign up at [everyinfra.com](https://everyinfra.com/en/docs?utm_source=github_readme&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=get_key#quickstart) and create a key in the console.
2. Connect any MCP client to `https://api.everyinfra.com/mcp` with `Authorization: Bearer <API key>`. Listing tools needs no key.

An EveryInfra API key is required for paid operations. Public capability discovery may be available
without one. Keep the key in the installing host's secret or environment configuration—never in a
manifest, prompt, committed file, or URL query string.

```bash
export EVERYINFRA_API_KEY="ei_..."
```

### SDK release attachments for `v0.2.0`

The `v0.2.0` GitHub Release distributes the official Python and Node clients as release attachments.
These URLs are the supported direct-install path for this version; they do not claim that an npm or
PyPI package with the same name has been published.

Python 3.9 or newer:

```bash
python -m pip install \
  https://github.com/everyinfra/everyinfra-agent-plugins/releases/download/v0.2.0/everyinfra-0.2.0-py3-none-any.whl
```

Node.js:

```bash
npm install \
  https://github.com/everyinfra/everyinfra-agent-plugins/releases/download/v0.2.0/everyinfra-0.2.0.tgz
```

### Codex

From a local clone:

```bash
codex plugin marketplace add <path-to-this-repository>
codex plugin add everyinfra@everyinfra
```

Then add an authenticated MCP connection for paid calls:

```bash
codex mcp add everyinfra \
  --url https://api.everyinfra.com/mcp \
  --bearer-token-env-var EVERYINFRA_API_KEY
```

The explicit MCP entry is separate because a distributable plugin must not contain a real bearer
token. Restart with a new task after installing so Codex can discover the new skills and tools.

After the Git repository is publicly reachable, the local path can be replaced with its repository
source:

```bash
codex plugin marketplace add everyinfra/everyinfra-agent-plugins
```

This command is an installation path, not evidence that the repository is listed in an official
Codex marketplace.

### Claude Code

```bash
claude plugin marketplace add <path-to-this-repository>
claude plugin install everyinfra@everyinfra
```

Configure the sensitive `api_token` value through Claude Code's plugin configuration flow. Avoid
putting a real token on a shell command line because shell history can retain it. A public GitHub
repository source can replace the local path after that source is reachable.

### Cursor

For local development, copy or symlink `plugins/everyinfra` to
`~/.cursor/plugins/local/everyinfra`, reload Cursor, and set `EVERYINFRA_API_KEY` through Cursor's
plugin configuration. A team can import the repository through its own marketplace process after
the Git source is reachable. The presence of `.cursor-plugin/marketplace.json` does not claim an
official Cursor listing.

Users who only need tools can add the EveryInfra MCP endpoint through Cursor's normal MCP
configuration without installing the skills package.

### GitHub Copilot and Agent Plugins 1.0 clients

The GitHub catalog is at `.github/plugin/marketplace.json`; the portable package starts at
`plugins/everyinfra/plugin.json`. Use the marketplace or local-plugin flow supported by your client.
Host support and secret injection differ, so confirm that the client reads `EVERYINFRA_API_KEY`
before making a paid call. The portable `mcp.json` deliberately contains no authorization header.

These files are compatibility metadata in this repository; they do not claim a GitHub marketplace
submission or a completed install test on every compatible client.

### Qoder CLI

```bash
qoder plugins marketplace add everyinfra/everyinfra-agent-plugins
qoder plugins install everyinfra
```

The catalog is `.qoder-plugin/marketplace.json`; the package manifest is
`plugins/everyinfra/.qoder-plugin/plugin.json`. Qoder loads the skills and the bundled `.mcp.json`,
which reads the key from `EVERYINFRA_API_KEY`. A local clone also works:
`qoder plugins install ./plugins/everyinfra`.

### CodeBuddy Code

```text
/plugin marketplace add everyinfra/everyinfra-agent-plugins
/plugin install everyinfra@everyinfra
```

The catalog is `.codebuddy-plugin/marketplace.json`; the package manifest is
`plugins/everyinfra/.codebuddy-plugin/plugin.json`. CodeBuddy asks for the sensitive `api_token`
value when the plugin is enabled and sends it as the `Authorization: Bearer` header.

### Kimi Code

```text
/plugins install https://github.com/everyinfra/everyinfra-agent-plugins/tree/main
```

The root manifest `.kimi-plugin/plugin.json` loads the ten skills from `plugins/everyinfra/skills/`
and declares the remote MCP server at `https://api-cn.everyinfra.com/mcp` (same server and keys as
`api.everyinfra.com`, reachable from mainland China). The manifest carries no key, so listing tools
works out of the box; for paid calls, add the same server with an `Authorization: Bearer` header in
Kimi Code's MCP configuration. Use the `/tree/main` form: a bare repository URL installs the latest
GitHub Release, which predates this manifest.

### Markets that take uploads

MiniMax, Qoder/QoderWork and ClawHub want their own packages. Their manifests and listing metadata
live in `host-packages/`; the skill bodies always come from `plugins/everyinfra/skills/`.

```bash
python3 scripts/build_host_packages.py check   # validate sources and a temporary build
python3 scripts/build_host_packages.py build   # write packages and ZIPs to dist/host-packages/
```

The build does not upload or submit anything. See `host-packages/README.md` for what each market
receives.

## Repository layout

```text
.agents/plugins/marketplace.json              Codex self-hosted marketplace
.claude-plugin/marketplace.json               Claude Code self-hosted marketplace
.cursor-plugin/marketplace.json               Cursor self-hosted marketplace
.github/plugin/marketplace.json               GitHub Copilot-compatible catalog
.qoder-plugin/marketplace.json                Qoder CLI self-hosted marketplace
.codebuddy-plugin/marketplace.json            CodeBuddy Code self-hosted marketplace
.kimi-plugin/plugin.json                      Kimi Code root manifest (install from the repository URL)
plugins/everyinfra/plugin.json                Agent Plugins 1.0 package manifest
plugins/everyinfra/.codex-plugin/plugin.json  Codex package manifest
plugins/everyinfra/.claude-plugin/plugin.json Claude Code package manifest
plugins/everyinfra/.cursor-plugin/plugin.json Cursor package manifest
plugins/everyinfra/.qoder-plugin/plugin.json  Qoder CLI package manifest
plugins/everyinfra/.codebuddy-plugin/plugin.json CodeBuddy Code package manifest
plugins/everyinfra/mcp*.json                   Portable and host-specific MCP metadata
plugins/everyinfra/skills/                     Router, product, and outcome skills
plugins/everyinfra/assets/                     Plugin icon and light/dark logos
workbuddy/                                     WorkBuddy connector packages (MCP + Skill)
host-packages/                                 MiniMax, Qoder/QoderWork and ClawHub package sources
llms-install.md                                Install steps for agents that set up MCP servers
```

## Validate and contribute

Run the dependency-free repository checks:

```bash
python3 scripts/validate.py
python3 scripts/build_workbuddy.py check
python3 scripts/build_host_packages.py check
```

Run host validators that are available in your environment and report unavailable validators as
skipped, not passed. For example:

```bash
claude plugin validate plugins/everyinfra --strict
```

Read [installation details](docs/installation.md), [troubleshooting](docs/troubleshooting.md),
[permissions and billing](docs/permissions.md), and the [REST-only boundary](docs/rest-only.md)
before using paid or state-changing operations.
Contributions are welcome through [CONTRIBUTING.md](CONTRIBUTING.md); include the affected host,
manifest or skill, evidence for changed API behavior, and the validation command you ran.
