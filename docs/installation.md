# Installation details

Installing the plugin and connecting the MCP server are separate operations. The plugin supplies
an installable identity, host manifests, reusable skills, brand assets, and connection metadata;
the MCP connection supplies live tools. A host may combine both steps in one UI, but validation
still treats them independently. Seeing the ten skills in a host UI is the expected visible result
of installing this plugin, not evidence that the plugin wrapper is missing. See
[architecture and distribution boundaries](architecture.md).

## Requirements

- A supported agent host or another Agent Plugins 1.0 client.
- Network access to `https://api.everyinfra.com`.
- An EveryInfra API key for paid operations. Public capability discovery does not require a key.

## Authentication by host

- **Codex:** the plugin's `.mcp.json` provides public discovery. For paid MCP calls, add the same
  server through Codex's native configuration so the host reads `EVERYINFRA_API_KEY` without
  writing its value to the plugin:

  ```bash
  codex mcp add everyinfra \
    --url https://api.everyinfra.com/mcp \
    --bearer-token-env-var EVERYINFRA_API_KEY
  ```
- **Claude Code:** `mcp.claude.json` reads the sensitive `api_token` declared in the Claude plugin
  manifest.
- **Cursor:** `mcp.cursor.json` reads the configured `EVERYINFRA_API_KEY` variable.
- **Agent Plugins 1.0 portable core:** `mcp.json` contains no authorization header. Version 1.0 does
  not define a portable credential-reference field, so authorization is client-managed.

Restart or reload the host after setting the key if it snapshots the launch environment. Do not put
the key into `plugin.json`, `mcp.json`, a workspace file, a URL query string, or a prompt.

For an official ChatGPT/Codex directory submission, register the remote MCP connection in ChatGPT
developer mode and add the resulting `.app.json` mapping. That is an app/connector registration,
not a replacement for the plugin manifest or MCP server. Do not fabricate or copy another
plugin's `plugin_asdk_app...` identifier.

## Verify the connection

1. Confirm the installed plugin version is `0.2.0` and that all ten skills are visible.
2. Independently confirm the MCP origin is exactly `https://api.everyinfra.com/mcp`.
3. Run a free capability-discovery operation before a paid call.
4. Check that the result includes an explicit capability, availability, or billing state rather
   than inferring success from the HTTP status alone.
5. Disable or uninstall the plugin and confirm that its skills disappear; remove the standalone
   MCP entry separately if one was configured.

If discovery works but a paid call returns an authorization or scope error, fix the client-managed
credential or account scope. Do not copy the key into plugin files and do not broaden it
automatically.
