# Contributing

Contributions that improve portability, safety, documentation, or task routing are welcome.

## Before changing a skill

1. Confirm the behavior against the live public capability catalog or API documentation.
2. Keep provider identities, private upstream fields and backend implementation details out of the
   public contract.
3. Never invent an MCP tool name. EveryNumber, EveryMail and EveryProxy remain REST-only until the
   remote MCP server actually advertises them.
4. Make paid calls and external side effects explicit. Discovery and status reads must not silently
   become purchases, sends, rentals, deliveries, or credential mutations.
5. Do not add API keys, example secrets, customer data, cookies, tokens, private endpoints, or
   copied backend source.

## Manifest changes

Keep these version values aligned for a release:

- `plugins/everyinfra/plugin.json`
- `plugins/everyinfra/.codex-plugin/plugin.json`
- `plugins/everyinfra/.claude-plugin/plugin.json`
- `plugins/everyinfra/.cursor-plugin/plugin.json`
- marketplace entries that carry an explicit `version` field

The portable Agent Plugins manifest has a closed schema. This package is a portable core plus
host-specific wrappers; client-specific metadata must remain in host manifests or under a
reverse-domain `extensions` namespace.

## Validation

Run JSON parsing, skill frontmatter checks, secret scans, and the host validators available on your
machine. At minimum:

```bash
python3 scripts/validate.py
claude plugin validate plugins/everyinfra --strict
```

Report skipped validators rather than treating an absent CLI as a pass.
