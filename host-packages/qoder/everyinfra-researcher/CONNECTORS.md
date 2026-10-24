# Connector dependency

This kit uses one remote MCP server, not an OAuth connector from the marketplace.

| Server | Address | Transport | Auth | Key |
|---|---|---|---|---|
| everyinfra | https://api.everyinfra.com/mcp | Streamable HTTP | `Authorization: Bearer` plus the EveryInfra key | Read from the `EVERYINFRA_API_KEY` environment variable |

Tool discovery works without a key; data, search and AI calls need it. If the key is missing, ask the user to configure it.
