# EveryInfra Agent Plugin

Install one package to give an AI agent reusable EveryInfra workflows **and** the metadata needed
to connect to EveryInfra's remote MCP server. The repository supports Codex, Claude Code, Cursor,
GitHub Copilot-compatible clients, and hosts that implement Agent Plugins 1.0.

This is a plugin repository, not a copy of the EveryInfra backend. It contains:

- 10 discoverable skills: one router, seven product skills, and two outcome workflows;
- remote MCP connection metadata for `https://api.everyinfra.com/mcp`;
- host-specific plugin manifests for Codex, Claude Code, and Cursor;
- self-hosted marketplace manifests for Codex, Claude Code, Cursor, and GitHub Copilot;
- presentation assets and safety boundaries for paid calls, credentials, billing, and external side
  effects.

No API key, customer data, upstream provider credential, or private gateway source code belongs in
this repository.

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

## Status: what exists today

| Layer | Repository state | What is not implied |
| --- | --- | --- |
| Remote MCP | The manifests target `https://api.everyinfra.com/mcp` for four MCP-enabled product lines. | A configured URL is not proof that a paid call is authenticated. |
| Plugin package | Portable and host-specific manifests, skills, MCP metadata, and assets are present. | Presence is not a clean-host installation test. |
| Repository validator | Cross-host JSON, path, skill, MCP, and credential-safety checks are available. | Repository validation is not marketplace approval. |
| Self-hosted catalogs | Four marketplace manifests are present in this repository. | A catalog file is not an official listing. |
| OpenAI registered app | No `.app.json` or host-issued app ID is included. | Direct MCP metadata is not a registered ChatGPT connector. |
| Official marketplaces | No submission or listing is claimed here. | Prepared metadata is not submitted, approved, or published metadata. |

Release claims should distinguish **prepared**, **validated**, **installed**, **submitted**, and
**listed**. Do not collapse them into one status.

## Quick start

An EveryInfra API key is required for paid operations. Public capability discovery may be available
without one. Keep the key in the installing host's secret or environment configuration—never in a
manifest, prompt, committed file, or URL query string.

```bash
export EVERYINFRA_API_KEY="your-key"
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

## Repository layout

```text
.agents/plugins/marketplace.json              Codex self-hosted marketplace
.claude-plugin/marketplace.json               Claude Code self-hosted marketplace
.cursor-plugin/marketplace.json               Cursor self-hosted marketplace
.github/plugin/marketplace.json               GitHub Copilot-compatible catalog
plugins/everyinfra/plugin.json                Agent Plugins 1.0 package manifest
plugins/everyinfra/.codex-plugin/plugin.json  Codex package manifest
plugins/everyinfra/.claude-plugin/plugin.json Claude Code package manifest
plugins/everyinfra/.cursor-plugin/plugin.json Cursor package manifest
plugins/everyinfra/mcp*.json                   Portable and host-specific MCP metadata
plugins/everyinfra/skills/                     Router, product, and outcome skills
plugins/everyinfra/assets/                     Plugin icon and light/dark logos
```

## Validate and contribute

Run the dependency-free repository checks:

```bash
python3 scripts/validate.py
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
