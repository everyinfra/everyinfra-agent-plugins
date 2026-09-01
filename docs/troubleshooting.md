# Troubleshooting

Diagnose the package, MCP connection, authentication, and product runtime as separate layers.

## Skills are visible but tools are missing

The plugin package loaded, but the MCP connection did not. Confirm the host has an `everyinfra`
server whose origin is exactly `https://api.everyinfra.com/mcp`, then reload or start a new agent
session. Do not reinstall the skills repeatedly to repair a missing MCP connection.

## Discovery works but a paid call is unauthorized

Public discovery and paid authorization are separate. Confirm the host is reading the intended
secret reference:

- Codex: the native MCP entry should name `EVERYINFRA_API_KEY` as its bearer-token environment
  variable;
- Claude Code: configure the sensitive `api_token` plugin value;
- Cursor: configure `EVERYINFRA_API_KEY` in plugin settings;
- other clients: follow the client's secret-injection mechanism instead of writing a token into
  `mcp.json`.

Do not paste a real key into an issue, prompt, screenshot, shell history, or committed file.

## A product skill exists but no MCP tool appears

EveryNumber, EveryMail, and EveryProxy are currently REST guidance. Their skill presence does not
create MCP tools. Use the documented REST path or wait until live MCP discovery exposes a real tool
and the package publishes a matching parity-tested update.

## A catalog entry exists but the operation is unavailable

Catalog membership describes a contract, not guaranteed live inventory. Read the current
availability or operation response. Do not retry paid calls indefinitely and do not treat HTTP 200
or a skill name as proof of availability.

## The host shows an old description or skill set

Confirm which marketplace and package path the host installed, reinstall from that source, then
start a new task or reload the host. Plugin source updates, MCP configuration updates, and
marketplace catalog updates may have different refresh cycles.

## Reporting a reproducible problem

Include the host and version, plugin version, installation source, affected skill or MCP tool,
sanitized error category, and the smallest reproduction steps. Remove API keys, request payloads
containing private data, customer identifiers, verification codes, proxy credentials, and provider
details before sharing logs.
