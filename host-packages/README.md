# Packages for markets that take uploads

Most hosts install EveryInfra straight from this repository (see the root README). A few markets
want their own package instead. This directory holds the editable sources for those packages;
`scripts/build_host_packages.py` adds the skill bodies from `plugins/everyinfra/skills/` and writes
the finished packages.

```bash
python3 scripts/build_host_packages.py check   # validate sources and a temporary build
python3 scripts/build_host_packages.py build   # write packages and ZIPs to dist/host-packages/
```

Building does not upload or submit anything. A person submits the packages through each market.

| Market | Source here | Built package | What it contains |
| --- | --- | --- | --- |
| MiniMax (CN) | `minimax/everyinfra-cn/` | `zips/minimax-everyinfra-cn.zip` | `.minimax-plugin/plugin.json` at the ZIP root, `icon.png`, `everyinfra.mcp.json` (`api-cn.everyinfra.com`), six skills with Chinese platform hints |
| MiniMax (US) | `minimax/everyinfra-us/` | `zips/minimax-everyinfra-us.zip` | Same layout, English listing, `api.everyinfra.com` |
| Qoder / QoderWork skills | `skills.json` (`qoder_description`) | `zips/qoder-<skill>.zip` | `SKILL.md` at the ZIP root (Qoder bulk upload) with `name`, `description`, `version` frontmatter and a Qoder setup section |
| Qoder / QoderWork expert kit | `qoder/everyinfra-researcher/` | `zips/qoder-everyinfra-researcher.zip` | `.qoder-plugin/plugin.json`, `.mcp.json`, `qoder.md`, `CONNECTORS.md`, `README.md` and six skills |
| ClawHub | `skills.json` (`clawhub`) | `clawhub/skills/<skill>/`, `clawhub/publish.sh` | Skills with `metadata.openclaw` frontmatter (`EVERYINFRA_API_KEY`), publish commands in two waves |
| Claude directory | `plugins/everyinfra/` (copied) | `claude/everyinfra/` (committed; the portal's Plugin path) | `.claude-plugin/plugin.json`, `mcp.claude.json` (`${user_config.api_token}`), skills, README, LICENSE, assets. No `.mcp.json` and no other host's manifest |

## Rules the check enforces

- MiniMax: no credentials anywhere in the package, so the MCP files carry no `headers` or `env`;
  transport is `streamable-http`; ASCII paths only; every `*.mcp.json` and skill is referenced by the
  manifest; category from the MiniMax list; at most three example queries. Paid calls need a key,
  which MiniMax only supports through its own App/Connector integration.
- Qoder: skill names are lowercase with hyphens and match their folder; no `TODO` or angle-bracket
  placeholders in a skill. The review rejects API-key sign-up instructions and any paid-call, billing,
  top-up or pricing wording, so `QODER_SKILL_TEXT` rewrites those sentences in the Qoder copies (the build
  fails if an original sentence disappears) and `check` fails on any word in `QODER_BLOCKED_WORDS` or a
  key sign-up phrase anywhere in a Qoder package.
- Claude directory: the package holds exactly the copied files above; no `.mcp.json`, no `${UPPER_CASE}`
  environment reference anywhere, and the MCP header reads `user_config.api_token`. `check` fails when
  `claude/everyinfra/` is stale; run `build` and commit it with the change.
- ClawHub: one to three categories from the fixed list, at most five topics, no reserved topic words.

## Changing a package

- Skill behavior: edit the shared skill under `plugins/everyinfra/skills/`, then rebuild.
- Listing text, Qoder descriptions or ClawHub categories: edit `skills.json` or the manifests here.
- Raise a package `version` whenever its content changes; MiniMax rejects an update that keeps the
  old version.

Links in the ClawHub packages (and the Qoder kit homepage) carry `utm_source` set to the market (`qoder`, `clawhub`),
`utm_medium=directory` and `utm_campaign=listing_2026q4`. The MiniMax manifest has no URL field.
