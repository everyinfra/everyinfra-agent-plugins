# Installing the EveryInfra MCP server

These steps are for an AI agent (for example Cline) that sets up MCP servers for its user.

EveryInfra is a remote MCP server. Nothing needs to be cloned, built or run locally.

## 1. Get an API key

Ask the user for an EveryInfra API key. New keys start with `ei_`. A user without a key creates one
in the console after signing up:
https://everyinfra.com/en/docs?utm_source=cline&utm_medium=directory&utm_campaign=listing_2026q4&utm_content=get_key#quickstart

Listing the tools works without a key. Data, search, AI and CAPTCHA calls need it. Never write the
key into a repository, a prompt or a URL.

## 2. Add the server

- Name: `everyinfra`
- Transport: Streamable HTTP
- URL: `https://api.everyinfra.com/mcp`
- Header: `Authorization: Bearer <API key>`

For clients that read a JSON MCP configuration (Cline uses `cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "everyinfra": {
      "type": "streamableHttp",
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${EVERYINFRA_API_KEY}"
      }
    }
  }
}
```

Replace `${EVERYINFRA_API_KEY}` with the user's key if the client does not expand environment
variables. Users in mainland China can use `https://api-cn.everyinfra.com/mcp` instead; it is the
same server and accepts the same keys.

## 3. Verify

1. Reload the MCP servers and list the tools. Expect names that start with `everyinfra_`, including
   `everyinfra_list_capabilities`, `everyinfra_call_api` and `everyinfra_search`.
2. Call `everyinfra_list_capabilities` with `{"platform": "tiktok"}`. It returns the TikTok actions
   with their parameters and prices.
3. Before any paid call, tell the user the expected cost from that catalog. Pricing starts at $0.56
   per 1,000 data calls; failed or empty calls are not charged.

## Optional: skills

The repository also ships ten skills that teach an agent when and how to use these tools. They are
in `plugins/everyinfra/skills/`; see the README for host-specific install commands.
