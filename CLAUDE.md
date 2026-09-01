# EveryInfra agent plugin repository

This is the public integration package for EveryInfra. It is intentionally independent from the
private gateway repository.

## Stable boundaries

- Keep MCP, Plugin, registered App/Connector, and Marketplace status distinct.
- Treat live MCP discovery and public catalogs as runtime truth.
- Never add credentials, customer data, provider identities, private upstream fields, or backend
  implementation details.
- Do not describe EveryNumber, EveryMail, or EveryProxy as MCP-enabled until production discovery
  and parity tests prove it.
- Paid calls and external side effects must remain explicit and bounded.

## Change and validation workflow

- Shared skills live only under `plugins/everyinfra/skills/`; host manifests are thin adapters.
- Keep version-bearing manifests and marketplace entries aligned for releases.
- Update `README.md`, `llms.txt`, and `docs/ai-discovery.md` when the public capability boundary
  changes.
- Run `python3 scripts/validate.py` and the available host validators before handoff.
- Do not commit, push, publish, or submit to a marketplace without explicit user authorization.
