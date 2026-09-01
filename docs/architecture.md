# MCP, plugin, app, and marketplace boundaries

EveryInfra uses four related but independent integration layers. Completion at one layer must not
be reported as completion at another.

## 1. MCP is the runtime capability layer

The Model Context Protocol connects an AI client to a server that can expose tools, resources,
prompts, and server-wide instructions. EveryInfra's remote server is
`https://api.everyinfra.com/mcp`.

An MCP server does not need a plugin. Codex, Claude Code, and Cursor can each connect to a remote
MCP server through their native MCP configuration. This is the smallest useful integration when a
user wants live tools but does not need EveryInfra's reusable workflows.

## 2. A plugin is an installable package

A plugin gives the integration a stable package identity and can bundle any supported combination
of skills, MCP connection metadata, agents, commands, rules, hooks, and presentation assets. The
contents vary by host.

A plugin does not have to contain MCP. OpenAI's public `build-web-apps` example is a skills package
without an MCP server. Conversely, an MCP server can be installed directly and have no associated
plugin. Figma and Notion are mainstream app-backed examples: their OpenAI plugin packages combine
skills and metadata with a registered MCP connection.

This repository keeps one portable skill source and adds thin host adapters:

- `plugin.json` and `mcp.json` are the portable Agent Plugins 1.0 core.
- `.codex-plugin/plugin.json` is the OpenAI package manifest.
- `.claude-plugin/plugin.json` is the Claude Code package manifest.
- `.cursor-plugin/plugin.json` is the Cursor-specific package manifest.

The `skills/` directory is therefore content inside the plugin, not a replacement for the plugin.
The installable unit is `plugins/everyinfra`; its manifests give it an identity, its MCP files
connect live tools, its assets make it recognizable in host UI, and its skills teach agents when
and how to use those tools. A host that renders individual skills after installation is showing
plugin components, not proving that only a skills bundle was installed.

Agent Plugins 1.0 is a portable packaging specification supported by Cursor. It is not a promise
that every host will accept every host-specific field or secret-injection mechanism.

## 3. An app or connector is a registered service connection

For OpenAI, `.app.json` maps a plugin package to an MCP connection that was already registered in
ChatGPT developer mode. The `plugin_asdk_app...` identifier and host-managed authentication belong
to this connection layer. `.app.json` is not a substitute for `.mcp.json`, and neither file makes a
plugin officially listed.

Claude also calls remote MCP integrations available through claude.ai “connectors.” Claude Code
can receive those connectors from the account or connect to the same server directly. Cursor can
install a standalone MCP configuration through an MCP deeplink. These are connection and auth
surfaces, not evidence that a full workflow plugin was installed.

EveryInfra has not yet registered an OpenAI app/connector, so this repository intentionally has no
`.app.json`. Registration, OAuth or other host-managed authentication, and connection testing are
required before that file can be added.

## 4. A marketplace is discovery and distribution

A marketplace is a catalog that points to installable packages or MCP connections. Adding a
marketplace does not install every plugin, and having a marketplace manifest does not mean an
official directory approved it.

- OpenAI local and repository marketplaces are authoring, testing, and private/team distribution
  sources. The public ChatGPT/Codex directory is a separate submission.
- Claude Code marketplaces are catalogs of plugins. A plugin may bundle skills, agents, hooks,
  MCP servers, and LSP servers; an MCP server can still be managed independently through `/mcp`.
- Cursor supports portable Agent Plugins and Cursor Plugins. It also supports standalone MCP
  install links, team marketplaces, a reviewed official marketplace, and the community
  `cursor.directory` catalog.

## Mainstream implementation patterns

| Pattern | Examples | EveryInfra path |
| --- | --- | --- |
| Skills-only plugin | OpenAI `build-web-apps` | Possible, but not the current package because live EveryInfra tools matter. |
| App-backed plugin | OpenAI Figma and Notion | Target after EveryInfra registers the remote MCP connection and auth. |
| Plugin-bundled MCP | Claude Code plugins; Cursor Agent Plugins | Current local package shape, with host-specific credential handling. |
| Standalone remote MCP | Native Codex, Claude Code, and Cursor MCP configuration | Available now for the four MCP-enabled product lines. |
| Marketplace listing | OpenAI universal directory, Claude official marketplace, Cursor Marketplace | Not submitted. Self-hosted manifests are preparation only. |

## Comparable project: TikHub

TikHub's public organization contains several different product forms. Only
[`TikHub/tikhub-plugin`](https://github.com/TikHub/tikhub-plugin) is directly comparable to this
repository. Its language SDKs, demo repository, n8n integration, and local MCP distribution are
separate deliverables.

The useful product patterns are:

- present MCP, REST, and SDK as separate ways to reach the same service;
- provide one onboarding/router skill before deep product skills;
- separate integration skills, platform or product skills, and outcome-oriented task skills;
- make endpoint or capability discovery explicit instead of asking the model to guess names;
- estimate cost and enforce hard pagination caps before bulk calls.

EveryInfra already has a router and a runtime capability catalog, so it does not need to copy
TikHub's offline 1,100-endpoint index or its `npx mcp-remote` bridge. The first two outcome skills are
cited cross-check research and bounded bulk structured-data export. They explicitly report when an
MCP result omits billing or availability rather than pretending those envelopes are observable.
This is a product reference, not a schema authority; host manifests continue to follow their
official specifications.

## EveryInfra completion gates

1. **MCP gate:** initialize, discovery, auth failure, paid-call confirmation, and product parity are
   tested independently of any plugin.
2. **Plugin gate:** the package installs in a clean host, exposes the expected skills, connects only
   to documented endpoints, and uninstalls cleanly.
3. **App/connector gate:** the service is registered with the real host-issued ID and its auth flow
   works; no ID is fabricated or copied from another plugin.
4. **Marketplace gate:** submission, review, approval, and public listing are recorded as separate
   states.
5. **Product gate:** EveryNumber, EveryMail, and EveryProxy remain REST-only until the production MCP
   server exposes real tools and parity tests pass.

For the compact machine-readable routing map, see [AI discovery and adoption](ai-discovery.md).

## Primary references

- [OpenAI: package your plugin](https://developers.openai.com/plugins/build/plugins)
- [OpenAI: MCP server concept](https://developers.openai.com/plugins/concepts/mcp-server)
- [OpenAI public plugin examples](https://github.com/openai/plugins/tree/main/plugins)
- [Claude Code: create plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code: connect through MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code: distribute marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cursor: plugins](https://prod.cursor.com/docs/plugins)
- [Cursor: MCP servers](https://docs.cursor.com/en/tools/mcp)
