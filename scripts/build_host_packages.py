#!/usr/bin/env python3
"""Check and build the EveryInfra packages for skill and plugin markets that take uploads.

Some markets cannot install straight from this repository and want their own package:

- MiniMax: one ZIP per region (CN, US) with ``.minimax-plugin/plugin.json`` at the ZIP root.
- Qoder / QoderWork: one ZIP per skill, plus the "EveryInfra Data Researcher" expert kit.
- ClawHub: one directory per skill with ``metadata.openclaw`` frontmatter, plus ``publish.sh``.
- Claude directory: ``host-packages/claude/everyinfra/``, a copy of the Claude plugin without the
  shared ``.mcp.json`` or other hosts' manifests, so the key comes only from ``user_config``.

Editable sources live in ``host-packages/`` (manifests, MCP files, icon, ``skills.json``). Skill
bodies always come from ``plugins/everyinfra/skills/``; this script only rewrites frontmatter and
appends a short host setup section, so the packaged copies cannot drift from the shared skills.

Commands (standard library only):

  check    validate the sources and build every package into a temporary directory
  build    check, then write the packages and deterministic ZIPs to dist/host-packages/ and
           refresh the committed Claude directory package in host-packages/claude/everyinfra/

Building does not upload or submit anything.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "plugins" / "everyinfra" / "skills"
SOURCE = REPO / "host-packages"
DIST = REPO / "dist" / "host-packages"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

UTM = "utm_medium=directory&utm_campaign=listing_2026q4"
MCP_URL = {"us": "https://api.everyinfra.com/mcp", "cn": "https://api-cn.everyinfra.com/mcp"}

MINIMAX_CATEGORIES = {
    "Office", "Studio", "Design & Sites", "Code", "Business", "Sales", "Productivity",
    "Science & Healthcare", "Education", "Other",
}
MINIMAX_TRANSPORTS = {"stdio", "streamable-http", "sse"}
MINIMAX_PATH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
MINIMAX_NAME_RE = re.compile(r"^[a-z](?:[a-z0-9]|[._-](?=[a-z0-9])){0,79}$")
CLAWHUB_CATEGORIES = {
    "integrations", "automation", "research", "development", "productivity", "communication",
    "creative", "knowledge", "agents", "operations", "security", "finance", "lifestyle", "other",
}
CLAWHUB_RESERVED_TOPICS = {
    "official", "verified", "openclaw", "clawhub", "curated", "community", "featured", "trusted",
}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
# Qoder rejects unfinished placeholders such as TODO or <your-token> in a skill.
PLUGIN = REPO / "plugins" / "everyinfra"
CLAUDE_PACKAGE = SOURCE / "claude" / "everyinfra"
# Copied from plugins/everyinfra; nothing else from that directory goes into the Claude package.
CLAUDE_REPO_BLOB = "https://github.com/everyinfra/everyinfra-agent-plugins/blob/main"
CLAUDE_FILES = (".claude-plugin", "mcp.claude.json", "skills", "README.md", "LICENSE", "assets")
ENV_REFERENCE_RE = re.compile(r"\$\{[A-Z][A-Z0-9_]*\}|\$[A-Z][A-Z0-9_]*\b|EVERYINFRA_API_KEY")
# The shared skills tell other hosts to read EVERYINFRA_API_KEY. Claude passes the sensitive
# user_config key only to the MCP server, so the Claude copies say that instead.
CLAUDE_REST_KEY = (
    "`Authorization: Bearer $EVERYINFRA_API_KEY`.",
    "an `Authorization: Bearer` header. In Claude the plugin's API key setting reaches only the MCP\n"
    "server, so ask the user how they want to supply the key for REST calls; never read it from a file\n"
    "or an environment variable.",
)
CLAUDE_SKILL_TEXT = {
    "everyinfra": (
        "read it from `EVERYINFRA_API_KEY`.",
        "the MCP server receives it from the plugin's\nAPI key setting.",
    ),
    "everymail": CLAUDE_REST_KEY,
    "everynumber": CLAUDE_REST_KEY,
    "everyproxy": CLAUDE_REST_KEY,
}
PLACEHOLDER_RE = re.compile(r"\bTODO\b|<[A-Za-z][A-Za-z0-9 _-]*>")

QODER_SETUP_MCP = """
## Setup in Qoder

1. This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable or from the MCP connection configured in Qoder. If the key is missing, ask the user to configure it. Listing tools works without a key.
2. Add the remote MCP server `everyinfra` at `https://api.everyinfra.com/mcp` (Streamable HTTP) in the MCP settings, with the request header `Authorization` set to `Bearer` followed by the key.
3. Open the MCP tool list once to confirm the `everyinfra_*` tools are present. Treat that live list as the runtime truth.
"""
QODER_SETUP_REST = """
## Setup in Qoder

This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable. If it is missing, ask the user to configure it. This skill calls the REST API at `https://api.everyinfra.com` directly; the catalog endpoint named above works without a key.
"""
# Qoder's market review rejects key sign-up instructions and any paid-call, billing, top-up or
# pricing wording (2026-10-24 rejection of all ten skills and the kit). The Qoder copies rewrite
# those sentences; each original must appear exactly once, so a changed shared skill fails the build
# instead of slipping the old wording through. QODER_BLOCKED_RE in check_tree is the backstop.
QODER_SKILL_TEXT: dict[str, tuple[tuple[str, str], ...]] = {
    "everyinfra": (
        ("- Traffic-billed proxy credentials: EveryProxy.", "- Proxy traffic packages: EveryProxy."),
        ("MCP tool discovery and the free REST catalogs", "MCP tool discovery and the REST catalogs"),
        (
            "1. Identify the requested outcome and whether it has external side effects or a charge.\n"
            "2. Use a free discovery tool or catalog before the first paid call.\n"
            "3. Validate required parameters, limits, solution shape, availability and current price.\n"
            "4. Invoke the paid operation only when the user's request authorizes that operation.\n"
            "5. Read returned `billing`, `quota`, status and error fields when present; never infer success,\n"
            "   availability, or a charge from HTTP 200 or catalog membership alone. If a tool omits billing,\n"
            "   report that the charge is not observable from that response.\n"
            "6. Report the useful result, the actual charge state and any remaining external action separately.",
            "1. Identify the requested outcome and whether it has external side effects.\n"
            "2. Use a discovery tool or catalog before the first operation call.\n"
            "3. Validate required parameters, limits, solution shape and availability.\n"
            "4. Invoke a state-changing operation only when the user's request authorizes that operation.\n"
            "5. Read returned `quota`, status and error fields when present; never infer success or\n"
            "   availability from HTTP 200 or catalog membership alone.\n"
            "6. Report the useful result and any remaining external action separately.",
        ),
        ("one account, API key and wallet across product lines", "one account and API key across product lines"),
        (
            "(`everyinfra_chat`) is free for accounts that have topped up, with per-minute limits that follow\n"
            "cumulative top-ups; an account that has not topped up receives `ai_topup_required`.",
            "(`everyinfra_chat`) handles that text work, within per-minute rate limits set for the account.",
        ),
    ),
    "everydata": (
        ("optional parameters, `max_limit` and current price. Use", "optional parameters and `max_limit`. Use"),
        ("needless repeated charges.", "needless repeated calls."),
        (
            "Report the returned\n   `billing` block rather than estimating cost from a stale document.",
            "Report what the\n   response actually returned rather than relying on a stale document.",
        ),
        ("(`everyinfra_chat`), which is free for\naccounts that have topped up.", "(`everyinfra_chat`)."),
    ),
    "everysearch": (
        ("a current version, price, policy,", "a current version, release, policy,"),
        (
            "- Read the returned `billing` state. Failed or empty calls may be uncharged, but do not infer that\n"
            "  without the response.",
            "- Read the returned status fields; do not infer the outcome of a call without the response.",
        ),
    ),
    "everyinfra-crosscheck-research": (
        (
            "6. Report billing only when the tool result exposes billing evidence. Do not infer a charge from a\n"
            "   catalog price or HTTP success.",
            "6. Report the call outcome only from the returned status fields. Do not infer success from HTTP\n"
            "   status alone.",
        ),
    ),
    "everyinfra-bulk-data-export": (
        ("This is a paid repeated-call workflow,", "This is a repeated-call workflow,"),
        ("any time or cost ceiling.", "any time or call ceiling."),
        ("   `max_limit`, and current catalog price. Do not guess", "   and `max_limit`. Do not guess"),
        ("that exact bounded spend was already", "that exact bounded pull was already"),
        (" the budget is exhausted,", ""),
        ("or insufficient-balance errors", "or account-limit errors"),
        (
            ", output\n  path, and the sum of actual returned billing blocks. If billing is absent, say the actual charge\n"
            "  was not observable instead of substituting the catalog estimate.",
            ", and output\n  path.",
        ),
    ),
    "everyai": (
        ("About 20,000 tokens of input\nper call is reliable", "About 20,000 tokens of input\nper request is reliable"),
        (
            "5. AI API calls are free for accounts that have topped up and do not use the balance. If the\n"
            "   response reports `ai_topup_required`, tell the user that the account needs a top-up instead of\n"
            "   retrying.",
            "5. If the response reports that the account is not enabled for the AI API, tell the user to check\n"
            "   their EveryInfra account instead of retrying.",
        ),
        (
            "Per-minute limits follow cumulative top-ups\n"
            "(50 under $100, 500 from $100, 5,000 from $500, all keys on the account combined); after a",
            "Per-minute rate limits apply per account\n(all keys on the account combined); after a",
        ),
    ),
    "everysolve": (
        (
            "6. Read `billing` and the explicit error status. EverySolve charges on successful delivery and\n"
            "   refunds unsuccessful solves, but the response is the evidence for a particular call.",
            "6. Read the explicit status and error fields; the response is the evidence for a particular call.",
        ),
        ("instead of spending repeated calls on guesses.", "instead of making repeated calls on guesses."),
    ),
    "everymail": (
        ("so cancellation and refunds remain unambiguous.", "so cancellation remains unambiguous."),
        ("status, billing and quota without", "status and quota without"),
    ),
    "everynumber": (
        ("1. `GET /api/v1/sms/catalog` is free. Select", "1. Read `GET /api/v1/sms/catalog`. Select"),
        ("`order_id` and frozen quote. Poll", "`order_id`. Poll"),
        (
            "4. Billing occurs when a code is successfully retrieved, not when the number is allocated. Read the\n"
            "   returned `billing` block.",
            "4. An activation completes when a code is successfully retrieved, not when the number is\n"
            "   allocated. Read the returned status fields.",
        ),
        ("Rentals are charged at order\ntime", "Rentals take effect at order\ntime"),
        ("Because this is non-refundable,", "Because this cannot be undone,"),
    ),
    "everyproxy": (
        ("Read the free `GET /api/v1/proxy/catalog`", "Read the `GET /api/v1/proxy/catalog`"),
        ("pricing is by traffic, never by session minutes.", "packages are sized by traffic, not by session minutes."),
        ("`POST /api/v1/proxy/order` is a paid order and", "`POST /api/v1/proxy/order` creates an order and"),
        ("must not be turned into a purchase.", "must not be turned into a new order."),
        ("accept delivery and the charge.", "accept delivery."),
        (
            "Report order status and billing separately. If delivery failed and was refunded, create a new",
            "Report the order status. If delivery failed, create a new",
        ),
    ),
}
# Words the Qoder review treats as sign-up or paid-call wording. Any hit in a Qoder package fails
# the check. QODER_ALLOWED lists exact phrases that contain a blocked word but say nothing about
# money (none are needed yet; add one with a comment saying why it is safe).
QODER_BLOCKED_WORDS = (
    r"paid", r"pay[ -]?per", r"per[ -]call", r"pricing", r"price", r"billing", r"billed", r"charge",
    r"top[ -]?up", r"topped up", r"refund", r"balance", r"credit", r"\$[0-9]", r"\bfree\b", r"wallet",
    r"\bcost", r"\bspend", r"budget", r"\bquote\b", r"\bbuy\b", r"purchase", r"quickstart", r"sign[ -]?up",
    r"付费", r"计费", r"扣费", r"充值", r"价格", r"退款", r"余额", r"免费", r"赠送", r"购买",
)
QODER_BLOCKED_RE = re.compile("|".join(QODER_BLOCKED_WORDS), re.I)
QODER_KEY_SIGNUP_RE = re.compile(
    r"(?:create|sign[ -]?up|register|get|obtain|claim|领取|领|创建|注册|申请)[^\n]{0,60}api[ -]?key"
    r"|api[ -]?key[^\n]{0,60}(?:create|sign[ -]?up|register|\bget\b|obtain|claim|领取|领|创建|注册|申请)",
    re.I,
)
QODER_ALLOWED: tuple[str, ...] = ()

CLAWHUB_SETUP_MCP = """

## Setup in OpenClaw

1. Create an API key at https://everyinfra.com/en/docs?{utm}&utm_content={slug}#quickstart and export it as `EVERYINFRA_API_KEY`. Capability discovery needs no key; paid calls do.
2. Add the remote MCP server once: `openclaw mcp add everyinfra --url https://api.everyinfra.com/mcp --transport streamable-http`, then set its `Authorization: Bearer` header to the key in Settings -> MCP (keep the key out of config literals). Check it with `openclaw mcp doctor everyinfra --probe`.
3. The live MCP tool list is the runtime truth. EveryInfra failed or empty calls are reported in the response `billing` block; read it instead of assuming.
"""
CLAWHUB_SETUP_REST = """

## Setup in OpenClaw

Create an API key at https://everyinfra.com/en/docs?{utm}&utm_content={slug}#quickstart and export it as `EVERYINFRA_API_KEY`. This skill calls the REST API at `https://api.everyinfra.com` directly; the catalog endpoint named above is free and needs no key.
"""


class BuildError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildError(f"{path.relative_to(REPO)}: {exc}") from exc
    if not isinstance(value, dict):
        raise BuildError(f"{path.relative_to(REPO)} must contain a JSON object")
    return value


def dumps(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def split_skill(slug: str) -> tuple[str, str]:
    text = (SKILLS / slug / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not match:
        raise BuildError(f"shared skill {slug} has no frontmatter")
    description = re.search(r"^description: (.*)$", match.group(1), re.M)
    if not description:
        raise BuildError(f"shared skill {slug} has no description")
    return description.group(1).strip(), match.group(2).rstrip("\n") + "\n"


def quoted(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def regional_skill(slug: str, region: str, meta: dict) -> str:
    description, body = split_skill(slug)
    if slug in meta["region_suffix_skills"]:
        description += " " + meta["region_suffix"][region]
    return f"---\nname: {slug}\ndescription: {quoted(description)}\n---\n" + body


def qoder_skill(slug: str, meta: dict) -> str:
    _, body = split_skill(slug)
    for old, new in QODER_SKILL_TEXT.get(slug, ()):
        if body.count(old) != 1:
            raise BuildError(f"Qoder package: {slug} no longer contains the sentence to rewrite: {old[:60]!r}")
        body = body.replace(old, new)
    entry = meta["skills"][slug]
    setup = QODER_SETUP_MCP if entry["runtime"] == "mcp" else QODER_SETUP_REST
    front = f"---\nname: {slug}\ndescription: {quoted(entry['qoder_description'])}\nversion: 1.0.1\n---\n"
    return front + body + setup.format(utm=f"utm_source=qoder&{UTM}", slug=slug)


def clawhub_skill(slug: str, meta: dict) -> str:
    shared, body = split_skill(slug)
    entry = meta["skills"][slug]
    description = entry["clawhub"]["description"] or shared
    utm = f"utm_source=clawhub&{UTM}"
    front = (
        f"---\nname: {slug}\ndescription: {quoted(description)}\nmetadata:\n  openclaw:\n"
        f"    homepage: https://everyinfra.com/en/docs?{utm}&utm_content={slug}\n"
        "    primaryEnv: EVERYINFRA_API_KEY\n    requires:\n      env:\n        - EVERYINFRA_API_KEY\n---\n"
    )
    setup = CLAWHUB_SETUP_MCP if entry["runtime"] == "mcp" else CLAWHUB_SETUP_REST
    return front + body + setup.format(utm=utm, slug=slug)


def clawhub_publish_script(meta: dict) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "# EveryInfra -> ClawHub. Generated by scripts/build_host_packages.py. Run by a person after",
        "# `clawhub login`:",
        "#   ./publish.sh dry 1     dry run, wave 1",
        "#   ./publish.sh real 1    publish wave 1",
        "#   ./publish.sh real 2    publish wave 2 only after wave 1 is public and clean",
        "# Optional: OWNER_HANDLE=<publisher> ./publish.sh real 1",
        "set -euo pipefail",
        'ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"',
        'MODE="${1:?dry|real}"; WAVE="${2:?1|2}"',
        'OWNER=(); [ -n "${OWNER_HANDLE:-}" ] && OWNER=(--owner "$OWNER_HANDLE")',
        'EXTRA=(); [ "$MODE" = "dry" ] && EXTRA=(--dry-run)',
        'run() { echo ">> $*"; "$@"; }',
    ]
    for wave in (1, 2):
        lines.append(f'if [ "$WAVE" = "{wave}" ]; then')
        for slug, entry in meta["skills"].items():
            listing = entry["clawhub"]
            if listing["wave"] != wave:
                continue
            lines.append(
                f'  run clawhub skill publish "$ROOT/skills/{slug}" --slug {slug} --name "{listing["name"]}" '
                f'--categories {",".join(listing["categories"])} --topics "{",".join(listing["topics"])}" '
                '--changelog "Initial release from EveryInfra." ${OWNER[@]+"${OWNER[@]}"} ${EXTRA[@]+"${EXTRA[@]}"}'
            )
        lines.append("fi")
    return "\n".join(lines) + "\n"


def check_sources(meta: dict, errors: list[str]) -> None:
    shared = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    if set(meta["skills"]) != shared:
        errors.append(f"host-packages/skills.json must list exactly the shared skills {sorted(shared)}")
    if not set(meta["bundle"]) <= shared or not set(meta["region_suffix_skills"]) <= set(meta["bundle"]):
        errors.append("host-packages/skills.json bundle lists an unknown skill")
    for slug, entry in meta["skills"].items():
        if entry.get("runtime") not in {"mcp", "rest"}:
            errors.append(f"{slug}: runtime must be mcp or rest")
        if not entry.get("qoder_description"):
            errors.append(f"{slug}: missing qoder_description")
        listing = entry.get("clawhub", {})
        categories, topics = listing.get("categories", []), listing.get("topics", [])
        if not categories or len(categories) > 3 or not set(categories) <= CLAWHUB_CATEGORIES:
            errors.append(f"{slug}: ClawHub needs one to three known categories")
        if len(topics) > 5 or set(topics) & CLAWHUB_RESERVED_TOPICS:
            errors.append(f"{slug}: ClawHub allows at most five topics and no reserved words")
        if listing.get("wave") not in (1, 2) or not listing.get("name"):
            errors.append(f"{slug}: ClawHub listing needs a name and wave 1 or 2")

    for region in ("cn", "us"):
        root = SOURCE / "minimax" / f"everyinfra-{region}"
        manifest = load_json(root / ".minimax-plugin" / "plugin.json")
        label = f"MiniMax {region}"
        if manifest.get("schemaVersion") != 1 or not MINIMAX_NAME_RE.match(str(manifest.get("name", ""))):
            errors.append(f"{label}: schemaVersion must be 1 and name must follow the MiniMax pattern")
        if not SEMVER_RE.match(str(manifest.get("version", ""))):
            errors.append(f"{label}: version must be semantic")
        if manifest.get("category") not in MINIMAX_CATEGORIES:
            errors.append(f"{label}: unknown category {manifest.get('category')!r}")
        if not 1 <= len(manifest.get("exampleQueries", [])) <= 3:
            errors.append(f"{label}: one to three example queries")
        if manifest.get("icon") != "icon.png" or "hooks" in manifest:
            errors.append(f"{label}: icon must be icon.png and hooks are not accepted")
        expected_skills = [f"skills/{slug}/SKILL.md" for slug in meta["bundle"]]
        if manifest.get("skills") != expected_skills:
            errors.append(f"{label}: skills must be {expected_skills}")
        for reference in manifest.get("mcpServers", []):
            config = load_json(root / reference)
            for name, server in config.get("mcpServers", {}).items():
                if server.get("type") not in MINIMAX_TRANSPORTS:
                    errors.append(f"{label}: {name} uses an unsupported transport")
                if "headers" in server or "env" in server:
                    errors.append(f"{label}: {name} must not carry headers or env (no credentials in the package)")
                if server.get("url") != MCP_URL[region]:
                    errors.append(f"{label}: {name} must point to {MCP_URL[region]}")

    kit = SOURCE / "qoder" / "everyinfra-researcher"
    manifest = load_json(kit / ".qoder-plugin" / "plugin.json")
    if manifest.get("name") != kit.name or not SEMVER_RE.match(str(manifest.get("version", ""))):
        errors.append("Qoder kit: name must match its directory and version must be semantic")
    server = load_json(kit / ".mcp.json").get("mcpServers", {}).get("everyinfra", {})
    if server.get("url") != MCP_URL["us"]:
        errors.append("Qoder kit: MCP URL drifted")


def build_tree(meta: dict, out: Path) -> list[Path]:
    """Write every package under ``out`` and return the package roots to zip."""
    zipped: list[Path] = []
    icon = SOURCE / "minimax" / "icon.png"
    for region in ("cn", "us"):
        source = SOURCE / "minimax" / f"everyinfra-{region}"
        root = out / "minimax" / f"everyinfra-{region}"
        shutil.copytree(source, root)
        shutil.copy2(icon, root / "icon.png")
        for slug in meta["bundle"]:
            target = root / "skills" / slug / "SKILL.md"
            target.parent.mkdir(parents=True)
            target.write_text(regional_skill(slug, region, meta), encoding="utf-8")
        zipped.append(root)

    for slug in meta["skills"]:
        target = out / "qoder" / "skills" / slug / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(qoder_skill(slug, meta), encoding="utf-8")
        zipped.append(target.parent)
    kit = out / "qoder" / "everyinfra-researcher"
    shutil.copytree(SOURCE / "qoder" / "everyinfra-researcher", kit)
    for slug in meta["bundle"]:
        target = kit / "skills" / slug / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(qoder_skill(slug, meta), encoding="utf-8")
    zipped.append(kit)

    for slug in meta["skills"]:
        target = out / "clawhub" / "skills" / slug / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text(clawhub_skill(slug, meta), encoding="utf-8")
    publish = out / "clawhub" / "publish.sh"
    publish.write_text(clawhub_publish_script(meta), encoding="utf-8")
    publish.chmod(0o755)
    return zipped


def build_claude(root: Path) -> None:
    """Copy the Claude plugin without the shared .mcp.json, which reads a machine environment variable."""
    root.mkdir(parents=True)
    for name in CLAUDE_FILES:
        source = PLUGIN / name
        if source.is_dir():
            shutil.copytree(source, root / name, ignore=shutil.ignore_patterns(".DS_Store"))
        else:
            shutil.copy2(source, root / name)
    for slug, (old, new) in CLAUDE_SKILL_TEXT.items():
        skill = root / "skills" / slug / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise BuildError(f"Claude package: {slug} no longer contains the key sentence to rewrite")
        skill.write_text(text.replace(old, new), encoding="utf-8")
    # The package sits one level deeper than plugins/everyinfra, so the README's
    # repo-relative links (../../docs/...) would break; point them at GitHub instead.
    readme = root / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("](../../", f"]({CLAUDE_REPO_BLOB}/"), encoding="utf-8")


def check_claude(root: Path, errors: list[str]) -> None:
    label = "Claude package"
    top = {path.name for path in root.iterdir()}
    if top != set(CLAUDE_FILES):
        errors.append(f"{label}: top level must be exactly {sorted(CLAUDE_FILES)}, found {sorted(top)}")
    manifest = load_json(root / ".claude-plugin" / "plugin.json")
    if manifest.get("mcpServers") != "./mcp.claude.json":
        errors.append(f"{label}: plugin.json must load ./mcp.claude.json")
    token = (manifest.get("userConfig") or {}).get("api_token") or {}
    if token.get("sensitive") is not True:
        errors.append(f"{label}: userConfig.api_token must stay sensitive")
    servers = load_json(root / "mcp.claude.json").get("mcpServers", {})
    authorization = servers.get("everyinfra", {}).get("headers", {}).get("Authorization")
    if authorization != "Bearer ${user_config.api_token}":
        errors.append(f"{label}: mcp.claude.json must read the key from user_config.api_token")
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.name == ".mcp.json" or path.is_symlink():
            errors.append(f"{label}: {relative} is not allowed")
        if path.is_file() and path.suffix in {".json", ".md", ".txt", ".yaml", ".yml", ".sh"}:
            for match in ENV_REFERENCE_RE.findall(path.read_text(encoding="utf-8")):
                errors.append(f"{label}: {relative} reads a machine environment variable ({match})")


def same_tree(left: Path, right: Path) -> bool:
    def files(root: Path) -> dict[str, bytes]:
        if not root.is_dir():
            return {}
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    return files(left) == files(right)


def check_tree(out: Path, meta: dict, errors: list[str]) -> None:
    for skill in sorted(out.rglob("SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---\n", text, re.S)
        name = re.search(r"^name: (.*)$", match.group(1), re.M) if match else None
        relative = skill.relative_to(out)
        if not name or name.group(1).strip() != skill.parent.name or not SKILL_NAME_RE.match(skill.parent.name):
            errors.append(f"{relative}: name must match its directory")
        if "/qoder/" in f"/{relative}" and PLACEHOLDER_RE.search(text):
            errors.append(f"{relative}: Qoder rejects TODO or angle-bracket placeholders")
    for path in sorted((out / "qoder").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in QODER_ALLOWED:
            text = text.replace(phrase, "")
        relative = path.relative_to(out)
        for line_no, line in enumerate(text.splitlines(), 1):
            for regex, reason in ((QODER_BLOCKED_RE, "paid-call or pricing wording"), (QODER_KEY_SIGNUP_RE, "API key sign-up")):
                hit = regex.search(line)
                if hit:
                    errors.append(f"{relative}:{line_no}: Qoder review rejects {reason} ({hit.group(0)!r})")
    for region in ("cn", "us"):
        root = out / "minimax" / f"everyinfra-{region}"
        manifest = json.loads((root / ".minimax-plugin" / "plugin.json").read_text(encoding="utf-8"))
        for reference in [manifest["icon"], *manifest["skills"], *manifest["mcpServers"]]:
            if not (root / reference).is_file():
                errors.append(f"MiniMax {region}: manifest references missing {reference}")
        for path in root.rglob("*"):
            relative = path.relative_to(root).as_posix()
            if not MINIMAX_PATH_RE.match(relative) or path.is_symlink():
                errors.append(f"MiniMax {region}: path {relative!r} is not accepted")
            if path.suffix == ".json" and path.read_bytes().startswith(b"\xef\xbb\xbf"):
                errors.append(f"MiniMax {region}: {relative} has a BOM")
        referenced = {*manifest["skills"], *manifest["mcpServers"]}
        for path in root.rglob("*.mcp.json"):
            if path.relative_to(root).as_posix() not in referenced:
                errors.append(f"MiniMax {region}: {path.name} is not referenced by the manifest")


def write_zip(folder: Path, zip_path: Path, wrap: bool) -> None:
    base = folder.parent if wrap else folder
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(path.relative_to(base).as_posix(), ZIP_TIMESTAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def run(build: bool) -> int:
    meta = load_json(SOURCE / "skills.json")
    errors: list[str] = []
    check_sources(meta, errors)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "host-packages"
        zipped = build_tree(meta, out)
        check_tree(out, meta, errors)
        claude = Path(tmp) / "claude" / "everyinfra"
        build_claude(claude)
        check_claude(claude, errors)
        if not build and not same_tree(claude, CLAUDE_PACKAGE):
            errors.append("host-packages/claude/everyinfra is stale; run: python3 scripts/build_host_packages.py build")
        if errors:
            print("Host package check failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        if not build:
            print(
                "Host package check passed: MiniMax CN and US, "
                f"{len(meta['skills'])} Qoder skills and 1 kit, {len(meta['skills'])} ClawHub skills, "
                "Claude directory package"
            )
            return 0
        zips = out / "zips"
        zips.mkdir()
        for folder in zipped:
            parts = folder.relative_to(out).parts
            # MiniMax wants the manifest at the ZIP root and Qoder's bulk upload wants SKILL.md at
            # the ZIP root; the Qoder kit and ClawHub keep their folder.
            wrap = parts[0] != "minimax" and not (parts[0] == "qoder" and parts[1] == "skills")
            write_zip(folder, zips / f"{parts[0]}-{folder.name}.zip", wrap)
        if DIST.exists():
            shutil.rmtree(DIST)
        shutil.copytree(out, DIST)
        if CLAUDE_PACKAGE.exists():
            shutil.rmtree(CLAUDE_PACKAGE)
        shutil.copytree(claude, CLAUDE_PACKAGE)
    print(f"Built host packages in {DIST.relative_to(REPO)} ({len(zipped)} ZIPs). Nothing was uploaded.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check", "build"))
    args = parser.parse_args()
    try:
        return run(args.command == "build")
    except BuildError as exc:
        print(f"Host package check failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
