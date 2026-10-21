#!/usr/bin/env python3
"""Validate the public EveryInfra plugin package without third-party dependencies."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "everyinfra"
EXPECTED_NAME = "everyinfra"
EXPECTED_MCP_URL = "https://api.everyinfra.com/mcp"
EXPECTED_SKILLS = {
    "everyinfra",
    "everyinfra-bulk-data-export",
    "everyinfra-crosscheck-research",
    "everydata",
    "everysearch",
    "everyai",
    "everysolve",
    "everynumber",
    "everymail",
    "everyproxy",
}
JSON_FILES = (
    REPO / ".agents" / "plugins" / "marketplace.json",
    REPO / ".claude-plugin" / "marketplace.json",
    REPO / ".cursor-plugin" / "marketplace.json",
    REPO / ".github" / "plugin" / "marketplace.json",
    REPO / ".qoder-plugin" / "marketplace.json",
    REPO / ".codebuddy-plugin" / "marketplace.json",
    REPO / ".kimi-plugin" / "plugin.json",
    PLUGIN / "plugin.json",
    PLUGIN / ".qoder-plugin" / "plugin.json",
    PLUGIN / ".codebuddy-plugin" / "plugin.json",
    PLUGIN / "mcp.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".cursor-plugin" / "plugin.json",
    PLUGIN / ".mcp.json",
    PLUGIN / "mcp.claude.json",
    PLUGIN / "mcp.cursor.json",
)
TEXT_SUFFIXES = {".json", ".md", ".txt", ".py", ".toml", ".yaml", ".yml"}
REQUIRED_PUBLIC_FILES = (
    REPO / "README.md",
    REPO / "llms.txt",
    REPO / "CLAUDE.md",
    REPO / "docs" / "ai-discovery.md",
    REPO / "docs" / "architecture.md",
    REPO / "docs" / "installation.md",
    REPO / "docs" / "troubleshooting.md",
    REPO / "SUPPORT.md",
    REPO / "llms-install.md",
    PLUGIN / "LICENSE",
    PLUGIN / "assets" / "icon.svg",
    PLUGIN / "assets" / "logo.svg",
    PLUGIN / "assets" / "logo-dark.svg",
)
# Public-text blocklist: SHA-256 digests of lowercase terms that must not appear in public files,
# grouped by term length. Only digests are stored, so the terms themselves stay out of this repository.
BLOCKED_TERM_SHA256 = {
    2: {
        "a9ab292ea9feecdcdfd3d6dfae632d35e27923892feb884ddb36502a9e89a67d",
        "ffdee717a579b55163b17a158aec447545aef28d989f95f47b8b75be9aba07aa",
    },
    4: {
        "a4826fa1e4036d285d76df148a9c9546e59910e1a95da8c4b9997598b4bfbbb6",
        "ee5a80cd15c51ce659df498fde630ca98ac8a6217c47205820d2a1da76ef382b",
    },
    5: {"954f775230679543d69509c294e19c393d50202fce576bcad71ac6add7b819d7"},
    6: {"cbea6fa89a1a56837ec0cdcf534980a4679c118c10ad2d64fe15532bd9e2f132"},
    7: {"51bab7a8adba778797f9123a2c604d12cddbec1dfd7df3891cff9382a104e518"},
    8: {"1581e27de87bffae0bd4d745cd7964e68528d7a83e2e4c259a782d275df6f558"},
    11: {"25904dfbcd8696a81fa6d9d63c751857242455c9d0c3ac90bfb25d5ac6e47789"},
    16: {"f962d695e3503521af2f1e619525cf425b7e4b989b7f5c4b870c968da46ee6a8"},
    20: {"deeeccd8d0c3fc67d116eebd983e7533925456eb8cb098339035ae52e104348d"},
}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {path.relative_to(REPO)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.relative_to(REPO)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(REPO)} must contain a JSON object")
        return {}
    return value


def expect_plugin_manifest(path: Path, errors: list[str]) -> dict[str, Any]:
    manifest = load_json(path, errors)
    if manifest.get("name") != EXPECTED_NAME:
        errors.append(f"{path.relative_to(REPO)} name must be {EXPECTED_NAME!r}")
    if not manifest.get("version"):
        errors.append(f"{path.relative_to(REPO)} must declare a version")
    if not manifest.get("description"):
        errors.append(f"{path.relative_to(REPO)} must declare a description")
    return manifest


def wrapped_server(path: Path, errors: list[str]) -> dict[str, Any]:
    root = load_json(path, errors)
    servers = root.get("mcpServers")
    if not isinstance(servers, dict) or set(servers) != {EXPECTED_NAME}:
        errors.append(f"{path.relative_to(REPO)} must wrap exactly one everyinfra server")
        return {}
    server = servers.get(EXPECTED_NAME)
    if not isinstance(server, dict):
        errors.append(f"{path.relative_to(REPO)} everyinfra server must be an object")
        return {}
    return server


def marketplace_source(path: Path, expected: Any, errors: list[str]) -> None:
    root = load_json(path, errors)
    plugins = root.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{path.relative_to(REPO)} plugins must be an array")
        return
    matches = [item for item in plugins if isinstance(item, dict) and item.get("name") == EXPECTED_NAME]
    if len(matches) != 1:
        errors.append(f"{path.relative_to(REPO)} must contain exactly one everyinfra entry")
        return
    if matches[0].get("source") != expected:
        errors.append(f"{path.relative_to(REPO)} has an unexpected source path")


def skill_frontmatter(path: Path, errors: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        errors.append(f"{path.relative_to(REPO)} has no closed YAML frontmatter")
        return
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    if values.get("name") != path.parent.name:
        errors.append(f"{path.relative_to(REPO)} name must match its directory")
    if not values.get("description"):
        errors.append(f"{path.relative_to(REPO)} must declare a description")


def contains_blocked_term(text: str) -> bool:
    flat = re.sub(r"\s+", " ", text.lower())
    for size, digests in BLOCKED_TERM_SHA256.items():
        for start in range(len(flat) - size + 1):
            if hashlib.sha256(flat[start:start + size].encode()).hexdigest() in digests:
                return True
    return False


def scan_public_text(errors: list[str]) -> None:
    forbidden = {
        "local macOS path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "literal bearer token": re.compile(r"Authorization[^\n]{0,40}Bearer\s+(?!\$\{|<|your-|YOUR_)[A-Za-z0-9_-]{16,}"),
        "EveryInfra API key": re.compile(r"\bei_[A-Za-z0-9_-]{12,}"),
        "secret-like token": re.compile(
            r"\b[a-z]{2,4}_(?=[A-Za-z0-9_-]*[A-Z])(?=[A-Za-z0-9_-]*[0-9])[A-Za-z0-9_-]{24,}"
        ),
    }
    for path in REPO.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in forbidden.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(REPO)} contains a forbidden {label}")
        if contains_blocked_term(text):
            errors.append(f"{path.relative_to(REPO)} contains private or legacy terminology")


def validate_public_discovery(codex: dict[str, Any], errors: list[str]) -> None:
    for path in REQUIRED_PUBLIC_FILES:
        if not path.is_file():
            errors.append(f"missing public discovery file {path.relative_to(REPO)}")

    agents = REPO / "AGENTS.md"
    if not agents.is_symlink() or agents.readlink() != Path("CLAUDE.md"):
        errors.append("AGENTS.md must be a relative symlink to CLAUDE.md")

    interface = codex.get("interface")
    if not isinstance(interface, dict):
        errors.append("Codex manifest must declare interface metadata")
        return
    expected_assets = {
        "composerIcon": "./assets/icon.svg",
        "logo": "./assets/logo.svg",
        "logoDark": "./assets/logo-dark.svg",
    }
    for field, expected in expected_assets.items():
        if interface.get(field) != expected:
            errors.append(f"Codex interface {field} must reference {expected}")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        errors.append("Codex interface must provide one to three default prompts")


def main() -> int:
    errors: list[str] = []
    for path in JSON_FILES:
        load_json(path, errors)

    codex = expect_plugin_manifest(PLUGIN / ".codex-plugin" / "plugin.json", errors)
    claude = expect_plugin_manifest(PLUGIN / ".claude-plugin" / "plugin.json", errors)
    cursor = expect_plugin_manifest(PLUGIN / ".cursor-plugin" / "plugin.json", errors)
    portable = expect_plugin_manifest(PLUGIN / "plugin.json", errors)
    qoder = expect_plugin_manifest(PLUGIN / ".qoder-plugin" / "plugin.json", errors)
    codebuddy = expect_plugin_manifest(PLUGIN / ".codebuddy-plugin" / "plugin.json", errors)
    kimi = expect_plugin_manifest(REPO / ".kimi-plugin" / "plugin.json", errors)
    validate_public_discovery(codex, errors)

    versions = {
        manifest.get("version") for manifest in (codex, claude, cursor, portable, qoder, codebuddy, kimi)
    }
    if len(versions) != 1 or None in versions:
        errors.append(f"plugin versions drifted: {sorted(str(value) for value in versions)}")
    for label, manifest in (("Codex", codex), ("Claude", claude), ("Cursor", cursor), ("CodeBuddy", codebuddy)):
        if manifest.get("skills") != "./skills/":
            errors.append(f"{label} manifest must load ./skills/")
    if codebuddy.get("mcpServers") != "./mcp.claude.json":
        errors.append("CodeBuddy manifest must reuse mcp.claude.json (user_config.api_token)")
    if "api_token" not in (codebuddy.get("userConfig") or {}):
        errors.append("CodeBuddy manifest must declare the sensitive api_token user config")
    # Qoder loads skills/ and .mcp.json by convention; an explicit path would replace them.
    if "skills" in qoder or "mcpServers" in qoder:
        errors.append("Qoder manifest must rely on the skills/ and .mcp.json conventions")
    # Kimi installs the repository root, so its manifest points into the shared plugin directory.
    if kimi.get("skills") != "./plugins/everyinfra/skills/":
        errors.append("Kimi root manifest must load ./plugins/everyinfra/skills/")
    kimi_servers = kimi.get("mcpServers")
    kimi_server = kimi_servers.get(EXPECTED_NAME) if isinstance(kimi_servers, dict) else None
    if not isinstance(kimi_server, dict) or kimi_server.get("url") not in {
        EXPECTED_MCP_URL,
        "https://api-cn.everyinfra.com/mcp",
    }:
        errors.append("Kimi root manifest must declare the everyinfra MCP server")
    elif "headers" in kimi_server:
        errors.append("Kimi root manifest must not embed an authorization header")

    codex_server = wrapped_server(PLUGIN / ".mcp.json", errors)
    if codex_server.get("url") != EXPECTED_MCP_URL:
        errors.append("Codex MCP URL drifted")
    codex_headers = codex_server.get("headers")
    codex_authorization = codex_headers.get("Authorization") if isinstance(codex_headers, dict) else None
    if codex_authorization != "Bearer ${EVERYINFRA_API_KEY}":
        errors.append("shared Codex/Copilot MCP config must reference EVERYINFRA_API_KEY")
    if "bearer_token_env_var" in codex_server:
        errors.append("plugin MCP config must not use the Codex-only bearer_token_env_var field")

    portable_server = wrapped_server(PLUGIN / "mcp.json", errors)
    if portable_server.get("url") != EXPECTED_MCP_URL:
        errors.append("portable MCP URL drifted")
    if "headers" in portable_server:
        errors.append("portable MCP configuration must not embed an authorization header")

    expected_headers = {
        PLUGIN / "mcp.claude.json": "Bearer ${user_config.api_token}",
        PLUGIN / "mcp.cursor.json": "Bearer ${EVERYINFRA_API_KEY}",
    }
    for path, expected in expected_headers.items():
        server = wrapped_server(path, errors)
        if server.get("url") != EXPECTED_MCP_URL:
            errors.append(f"{path.relative_to(REPO)} MCP URL drifted")
        headers = server.get("headers")
        actual = headers.get("Authorization") if isinstance(headers, dict) else None
        if actual != expected:
            errors.append(f"{path.relative_to(REPO)} must use its documented secret reference")

    marketplace_source(
        REPO / ".agents" / "plugins" / "marketplace.json",
        {"source": "local", "path": "./plugins/everyinfra"},
        errors,
    )
    marketplace_source(REPO / ".claude-plugin" / "marketplace.json", "./plugins/everyinfra", errors)
    marketplace_source(REPO / ".cursor-plugin" / "marketplace.json", "plugins/everyinfra", errors)
    marketplace_source(REPO / ".github" / "plugin" / "marketplace.json", "./plugins/everyinfra", errors)
    marketplace_source(REPO / ".qoder-plugin" / "marketplace.json", "./plugins/everyinfra", errors)
    marketplace_source(REPO / ".codebuddy-plugin" / "marketplace.json", "./plugins/everyinfra", errors)

    codex_marketplace = load_json(REPO / ".agents" / "plugins" / "marketplace.json", errors)
    codex_entries = codex_marketplace.get("plugins")
    if isinstance(codex_entries, list) and codex_entries:
        policy = codex_entries[0].get("policy") if isinstance(codex_entries[0], dict) else None
        if not isinstance(policy, dict) or policy.get("authentication") != "ON_USE":
            errors.append("Codex marketplace authentication policy must remain ON_USE")

    version = portable.get("version")
    for path in (
        REPO / ".claude-plugin" / "marketplace.json",
        REPO / ".github" / "plugin" / "marketplace.json",
        REPO / ".codebuddy-plugin" / "marketplace.json",
    ):
        marketplace = load_json(path, errors)
        entries = marketplace.get("plugins")
        matches = [
            item
            for item in entries or []
            if isinstance(item, dict) and item.get("name") == EXPECTED_NAME
        ]
        if matches and matches[0].get("version") != version:
            errors.append(f"{path.relative_to(REPO)} plugin version drifted")

    skill_root = PLUGIN / "skills"
    actual_skills = {path.name for path in skill_root.iterdir() if path.is_dir()}
    if actual_skills != EXPECTED_SKILLS:
        errors.append(f"skill set drifted: expected {sorted(EXPECTED_SKILLS)}, got {sorted(actual_skills)}")
    for name in sorted(actual_skills):
        skill_frontmatter(skill_root / name / "SKILL.md", errors)

    scan_public_text(errors)

    if errors:
        print("EveryInfra plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "EveryInfra plugin validation passed: "
        f"7 manifests, 6 marketplace sources, 4 MCP configs, {len(EXPECTED_SKILLS)} skills"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
