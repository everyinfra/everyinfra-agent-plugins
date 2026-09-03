# Releasing EveryInfra agent plugins

A release is not public merely because its source is ready. Use the following terms precisely:

- **Prepared**: the intended source, manifests, documentation, and changelog entry are present, but
  the release has not completed validation.
- **Validated**: repository validation, public-asset checks, and deterministic archive verification
  pass for the exact release source.
- **Installed**: that validated source or archive has been installed and smoke-tested in a named
  host. Installation in one host does not prove installation in another.
- **Submitted**: an authorized person has sent the release to a repository, release service, or
  marketplace for review. Submission is not approval or public availability.
- **Listed**: the release is visibly discoverable and installable from the named public catalog.

Never use a later status until there is direct evidence for it. Record status per host and per
marketplace rather than assigning one status to every distribution channel.

## Version alignment

Before validation, choose one SemVer value and align every version-bearing file:

- `plugins/everyinfra/plugin.json`
- `plugins/everyinfra/.codex-plugin/plugin.json`
- `plugins/everyinfra/.claude-plugin/plugin.json`
- `plugins/everyinfra/.cursor-plugin/plugin.json`
- the EveryInfra entries in `.claude-plugin/marketplace.json` and
  `.github/plugin/marketplace.json`
- the matching release heading in `CHANGELOG.md`

The Codex and Cursor marketplace catalogs currently do not carry their own version field. Do not
invent one only to make the files look symmetrical. The builder refuses mismatched manifests or
versioned marketplace entries and names the archive
`dist/everyinfra-agent-plugins-<version>.zip`.

## Official MCP Registry

`server.json` at the repository root describes the remote server for the
[official MCP Registry](https://registry.modelcontextprotocol.io/). It declares
`https://api.everyinfra.com/mcp` over Streamable HTTP and one required secret header
(`Authorization: Bearer <api key>`); there is no package to publish first, because the
registry hosts metadata only and this server is remote.

The name is `io.github.everyinfra/everyinfra`. That namespace is reachable **only** by
someone authenticated as the `everyinfra` GitHub organization, so no DNS TXT record and no
custom-domain proof is needed. Domain-based auth would be required only if the name moved to
a reverse-DNS form such as `com.everyinfra/*`.

Validate without publishing at any time:

```bash
mcp-publisher validate
```

Publishing is a two-step flow and the first step is interactive, so it is done by a person:

```bash
mcp-publisher login github     # device-code flow in a browser
mcp-publisher publish
curl "https://registry.modelcontextprotocol.io/v0/servers?limit=100" | grep everyinfra
```

Keep `version` in `server.json` aligned with the plugin version. The registry does not
currently allow arbitrary un-publishing of a version, so treat a publish as permanent and
stabilise the namespace, version and file before running it.

⚠ Registry inclusion proves namespace ownership and metadata shape. It is not a security
review, and it does not mean any host has installed or approved the server.

## Local validation first

Run the checks from the repository root before any commit, tag, upload, or marketplace submission:

```bash
python3 scripts/validate.py
python3 scripts/build_release.py --check-source
python3 scripts/build_release.py
```

`build_release.py` uses only the Python standard library. It validates JSON, the repository's GitHub
YAML structure, SVG XML and safety boundaries, and local Markdown links. It then creates a
deterministic ZIP with one versioned top-level directory, verifies every member against the source,
and writes the result under the gitignored `dist/` directory. Source symlinks are materialized as
regular files so the archive remains usable on hosts that do not preserve symlinks.

To recheck an existing artifact against the current tree, run:

```bash
python3 scripts/build_release.py --verify dist/everyinfra-agent-plugins-<version>.zip
```

GitHub Actions repeats the repository checks, parses GitHub YAML, builds the archive twice, compares
its checksums, and uploads the validated ZIP as a short-lived workflow artifact. A green workflow is
evidence for **validated**, not **installed**, **submitted**, or **listed**.

## Installation smoke test

Install the exact validated source or archive in each host claimed by the release. Confirm that the
host discovers the EveryInfra plugin and its shared skills, that MCP configuration requests the
documented credential rather than embedding one, and that an allowed no-side-effect operation can be
routed. Keep host-specific evidence separate; do not infer marketplace availability from a local
installation.

## External publication

Commit, push, tags, GitHub releases, marketplace submissions, account creation, and permission
changes are external actions and require explicit user authorization. After authorization:

1. Confirm the reviewed source still matches the validated archive and record its SHA-256 checksum.
2. Create the approved commit and version tag without including `dist/`.
3. Attach the already validated ZIP to the approved release destination.
4. Mark each destination **submitted** only after its final submission succeeds.
5. Independently verify the public catalog entry and a clean installation before marking it
   **listed**.

If any source file changes after validation, rebuild and revalidate. Do not reuse validation evidence
from a different tree, archive, version, or host.
