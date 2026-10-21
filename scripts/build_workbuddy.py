#!/usr/bin/env python3
"""Render, validate and package the EveryInfra WorkBuddy connectors.

WorkBuddy connectors are host adapters: each one is a directory with
``connector-meta.json``, ``mcp.json``, ``token-schema.json``, an icon and
``skills/*/SKILL.md``. Hand-written files (the main connector metadata and its
four workflow skills, plus ``workbuddy/platforms.json``) are the editable
sources. Everything else under ``workbuddy/connectors/`` is rendered by this
script so the shared MCP settings, credential form and platform skills cannot
drift between connectors.

Commands (standard library only):

  render                      write every generated file
  check                       fail if generated files are stale or a connector breaks WorkBuddy rules
  package [--flat] [--offline]
                              check, compare SERVER_TOOLS with the live tools/list, then write
                              deterministic ZIPs to dist/workbuddy/
  refresh-catalog FILE        refresh the platform action snapshot from a saved public catalog JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
WORKBUDDY = REPO / "workbuddy"
CONNECTORS = WORKBUDDY / "connectors"
PLATFORMS_FILE = WORKBUDDY / "platforms.json"
ICON_SOURCE = REPO / "plugins" / "everyinfra" / "assets" / "icon.svg"
DIST = REPO / "dist" / "workbuddy"

MAIN = "everyinfra"
VERSION = "1.0.0"
AUTHOR = "EveryInfra"
# WorkBuddy users are mostly in mainland China, so the connectors use the mainland API entry,
# which serves the same MCP server and accepts the same API keys as api.everyinfra.com.
MCP_URL = "https://api-cn.everyinfra.com/mcp"
TOKEN_KEY = "EVERYINFRA_API_KEY"
# Generous enough for the slowest synchronous call; WorkBuddy's default is 30 s.
MCP_TIMEOUT_MS = 100_000
# Tools the remote server advertises today (tools/list). Names are a customer contract.
SERVER_TOOLS = (
    "everyinfra_list_capabilities",
    "everyinfra_call_api",
    "everyinfra_get_job",
    "everyinfra_chat",
    "everyinfra_list_captcha_types",
    "everyinfra_solve_captcha",
    "everyinfra_search",
    "everyinfra_account",
    "everyinfra_usage",
    "everyinfra_requests",
    "everyinfra_billing",
    "everyinfra_keys",
    "everyinfra_tickets",
    "everyinfra_topup_link",
    "everyinfra_create_ticket",
    "everyinfra_get_ticket",
    "everyinfra_key_create",
    "everyinfra_key_update",
    "everyinfra_key_disable",
    "everyinfra_key_delete",
    "everyinfra_settings_update",
    "everyinfra_webhook_set",
    "everyinfra_webhook_test",
    "everyinfra_ticket_create",
    "everyinfra_ticket_reply",
)
EXPOSED_TOOLS = {
    "main": ("everyinfra_list_capabilities", "everyinfra_call_api", "everyinfra_search"),
    "standalone": ("everyinfra_list_capabilities", "everyinfra_call_api"),
}
# Minimum WorkBuddy client version for each feature this package uses (WorkBuddy connector docs).
FEATURE_MIN_VERSION = {
    "disabledTools": (4, 22, 15),
    "auth_mode:token": (4, 23, 0),
    "name_zh": (4, 24, 0),
    "examples": (4, 24, 0),
}
SOURCE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
PLACEHOLDER_RE = re.compile(r"\$\{([A-Za-z0-9_]+)\}")
TOOL_RE = re.compile(r"\beveryinfra_[a-z_]+\b")
SKILL_REQUIRED = ("description", "description_zh", "description_en", "version", "author")
# Frontmatter values are written as YAML plain scalars, so they must not contain
# sequences a YAML parser would read as structure.
YAML_UNSAFE_RE = re.compile(r": |\s#|^[-?:,\[\]{}#&*!|>'\"%@`]|:$")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

HAND_WRITTEN = {
    f"{MAIN}/connector-meta.json",
    f"{MAIN}/skills/everyinfra-data/SKILL.md",
    f"{MAIN}/skills/everyinfra-search/SKILL.md",
    f"{MAIN}/skills/everyinfra-crosscheck-research/SKILL.md",
    f"{MAIN}/skills/everyinfra-bulk-data-export/SKILL.md",
}


class BuildError(RuntimeError):
    pass


def dumps(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def load_platforms() -> dict:
    data = json.loads(PLATFORMS_FILE.read_text(encoding="utf-8"))
    names = [item["platform"] for item in data["platforms"]]
    if len(names) != len(set(names)):
        raise BuildError("workbuddy/platforms.json lists a platform twice")
    unknown = set(data["standalone"]) - set(names)
    if unknown:
        raise BuildError(f"standalone platforms missing from the platform list: {sorted(unknown)}")
    return data


def mcp_config(kind: str) -> dict:
    disabled = [tool for tool in SERVER_TOOLS if tool not in EXPOSED_TOOLS[kind]]
    return {
        "mcpServers": {
            "everyinfra": {
                "type": "streamableHttp",
                "url": MCP_URL,
                "headers": {"Authorization": "Bearer ${" + TOKEN_KEY + "}"},
                "timeout": MCP_TIMEOUT_MS,
                "disabledTools": disabled,
            }
        }
    }


def token_schema() -> dict:
    return {
        "title": "连接 EveryInfra",
        "title_en": "Connect EveryInfra",
        "description": "填写你的 EveryInfra API Key。Key 只保存在本机，连接时作为请求头发送给 api-cn.everyinfra.com，用于调用和计费。",
        "description_en": "Enter your EveryInfra API key. It is stored on this device only and sent to api-cn.everyinfra.com as a request header for calls and billing.",
        "docUrl": "https://everyinfra.com/docs",
        "docLabel": "如何创建 API Key？",
        "docLabel_en": "How do I create an API key?",
        "fields": [
            {
                "key": TOKEN_KEY,
                "label": "API Key",
                "label_en": "API Key",
                "type": "password",
                "required": True,
                "placeholder": "以 ei_ 开头，在 everyinfra.com 控制台的 API Key 页面创建",
                "placeholder_en": "Starts with ei_; create one on the API Keys page at everyinfra.com",
                "description": "注册 everyinfra.com 后在控制台创建；充值后即可调用付费能力。",
                "description_en": "Sign up at everyinfra.com and create a key in the console; paid capabilities need a funded balance.",
            }
        ],
    }


def capacity_text(action: dict) -> str:
    if not action.get("returns_list"):
        return "单条"
    page_size = action.get("page_size")
    if action.get("limit_ignored") and page_size:
        if action.get("page_size_varies"):
            return f"每页最多 {page_size} 条，可翻页"
        return f"每页 {page_size} 条，可翻页"
    if action.get("max_limit"):
        return f"limit 最多 {action['max_limit']}"
    return "列表"


def frontmatter(values: dict[str, str]) -> str:
    lines = ["---"]
    lines += [f"{key}: {value}" for key, value in values.items()]
    lines.append("---")
    return "\n".join(lines)


def platform_skill(item: dict) -> str:
    platform = item["platform"]
    name_zh, name_en = item["name_zh"], item["name_en"]
    if not item["actions"]:
        raise BuildError(f"{platform} has no action snapshot; run refresh-catalog first")
    rows = [
        "| action | 用途 | 必填参数 | 可选参数 | 返回条数 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for action in item["actions"]:
        required = ", ".join(f"`{name}`" for name in action["required"]) or "无"
        optional = ", ".join(f"`{name}`" for name in action["optional"]) or "无"
        rows.append(
            f"| `{action['action']}` | {action['label']} | {required} | {optional} | {capacity_text(action)} |"
        )
    call = {"platform": platform, **item["example_call"]}
    notes = list(item.get("notes_zh") or [])
    notes += [
        "按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。",
        "结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。",
        "需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。",
        "在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。",
        "`unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。"
        "`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。"
        "`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。",
        "只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。",
    ]
    head = frontmatter({
        "name": f"everyinfra-{platform}",
        "display_name": f"{name_zh}数据（EveryInfra）",
        "display_name_en": f"EveryInfra {name_en} Data",
        "description": f"用 EveryInfra 查询{name_zh}公开数据：{item['scope_zh']}。用户提到{item['triggers_zh']}等需求时使用。",
        "description_zh": f"查询{name_zh}公开数据：{item['scope_zh']}。",
        "description_en": f"Query public {name_en} data, including {item['scope_en']}.",
        "version": VERSION,
        "author": AUTHOR,
    })
    body = [
        head,
        "",
        f"# {name_zh}数据",
        "",
        f"平台标识 `{platform}`。调用前先用 `everyinfra_list_capabilities` 传 "
        f"`{{\"platform\": \"{platform}\"}}`，取当前的参数、允许值、单次条数、单价和返回字段；"
        "能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。",
        "",
        "## 常用能力",
        "",
        *rows,
        "",
        "## 调用示例",
        "",
        f"用户：「{item['examples_zh'][0]}」",
        "",
        "```json",
        json.dumps(call, ensure_ascii=False),
        "```",
        "",
        "## 注意",
        "",
        *[f"- {note}" for note in notes],
        "",
    ]
    return "\n".join(body)


def standalone_meta(item: dict) -> dict:
    platform, name_zh, name_en = item["platform"], item["name_zh"], item["name_en"]
    return {
        "name": f"EveryInfra {name_en}",
        "name_zh": f"EveryInfra {name_zh}数据",
        "name_en": f"EveryInfra {name_en} Data",
        "description": f"Query public {name_en} data with EveryInfra: {item['scope_en']}.",
        "description_zh": f"查询{name_zh}公开数据：{item['scope_zh']}。用 EveryInfra API Key 连接，按次计费。",
        "description_en": f"Query public {name_en} data: {item['scope_en']}. Connect with your EveryInfra API key; pay per call.",
        "source": f"everyinfra-{platform}",
        "type": "mcp",
        "version": VERSION,
        "auth_mode": "token",
        "minWorkbuddyVersion": "4.24.0",
        "examples_zh": item["examples_zh"],
        "examples_en": item["examples_en"],
    }


def generated_files() -> dict[str, bytes]:
    data = load_platforms()
    icon = ICON_SOURCE.read_bytes()
    files: dict[str, bytes] = {
        f"{MAIN}/mcp.json": dumps(mcp_config("main")),
        f"{MAIN}/token-schema.json": dumps(token_schema()),
        f"{MAIN}/icon.svg": icon,
    }
    by_name = {item["platform"]: item for item in data["platforms"]}
    for item in data["platforms"]:
        skill = platform_skill(item).encode("utf-8")
        files[f"{MAIN}/skills/everyinfra-{item['platform']}/SKILL.md"] = skill
    for platform in data["standalone"]:
        item = by_name[platform]
        source = f"everyinfra-{platform}"
        files[f"{source}/connector-meta.json"] = dumps(standalone_meta(item))
        files[f"{source}/mcp.json"] = dumps(mcp_config("standalone"))
        files[f"{source}/token-schema.json"] = dumps(token_schema())
        files[f"{source}/icon.svg"] = icon
        files[f"{source}/skills/everyinfra-{platform}/SKILL.md"] = platform_skill(item).encode("utf-8")
    return files


def render() -> int:
    files = generated_files()
    for relative, data in files.items():
        path = CONNECTORS / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    owned = set(files) | HAND_WRITTEN
    stale = [p for p in CONNECTORS.rglob("*") if p.is_file() and p.relative_to(CONNECTORS).as_posix() not in owned]
    for path in stale:
        if path.name != ".DS_Store":
            raise BuildError(f"unexpected file under workbuddy/connectors: {path.relative_to(REPO)}")
    print(f"Rendered {len(files)} generated WorkBuddy files")
    return 0


def version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def parse_skill(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"{path.relative_to(REPO)} has no closed YAML frontmatter")
        return {}, text
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or key.startswith(" "):
            errors.append(f"{path.relative_to(REPO)} frontmatter line is not a flat key: value pair")
            continue
        values[key.strip()] = value.strip()
        if YAML_UNSAFE_RE.search(value.strip()):
            errors.append(f"{path.relative_to(REPO)} frontmatter {key.strip()} is not a safe YAML plain scalar")
    return values, text[match.end():]


def check_connector(directory: Path, errors: list[str]) -> None:
    label = directory.relative_to(REPO).as_posix()
    meta_path = directory / "connector-meta.json"
    mcp_path = directory / "mcp.json"
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: {exc}")
        return

    for field in ("name", "name_en", "description", "description_zh", "description_en"):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            errors.append(f"{label}: connector-meta.json needs a non-empty {field}")
    zh = meta.get("description_zh", "")
    if isinstance(zh, str) and not 20 <= len(zh) <= 100:
        errors.append(f"{label}: description_zh should be 20-100 characters, got {len(zh)}")
    source = meta.get("source")
    if not isinstance(source, str) or not SOURCE_RE.fullmatch(source) or source != directory.name:
        errors.append(f"{label}: source must be kebab-case and match the directory name")
    if meta.get("type", "mcp") != "mcp":
        errors.append(f"{label}: this package only ships MCP connectors")
    if not SEMVER_RE.fullmatch(str(meta.get("version", ""))):
        errors.append(f"{label}: version must be semantic x.y.z")
    for field in ("examples_zh", "examples_en"):
        examples = meta.get(field)
        if not isinstance(examples, list) or not 2 <= len(examples) <= 5 or not all(
            isinstance(example, str) and example.strip() for example in examples
        ):
            errors.append(f"{label}: {field} needs 2-5 non-empty examples")

    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or len(servers) != 1:
        errors.append(f"{label}: mcp.json must configure exactly one server")
        return
    server = next(iter(servers.values()))
    if server.get("type") != "streamableHttp" or server.get("url") != MCP_URL:
        errors.append(f"{label}: mcp.json must use streamableHttp at {MCP_URL}")
    headers = server.get("headers") or {}
    if headers.get("Authorization") != "Bearer ${" + TOKEN_KEY + "}":
        errors.append(f"{label}: Authorization must reference the token form placeholder")
    disabled = server.get("disabledTools") or []
    unknown = set(disabled) - set(SERVER_TOOLS)
    if unknown:
        errors.append(f"{label}: disabledTools names tools the server does not advertise: {sorted(unknown)}")
    exposed = set(SERVER_TOOLS) - set(disabled)

    features: set[str] = set()
    if disabled:
        features.add("disabledTools")
    if "name_zh" in meta:
        features.add("name_zh")
    if "examples_zh" in meta or "examples_en" in meta:
        features.add("examples")
    auth_mode = meta.get("auth_mode")
    if auth_mode not in (None, "server-side", "gateway", "token"):
        errors.append(f"{label}: unsupported auth_mode {auth_mode!r}")
    placeholders = set(PLACEHOLDER_RE.findall(json.dumps(server)))
    if auth_mode == "token":
        features.add("auth_mode:token")
        schema_path = directory / "token-schema.json"
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: token mode needs a valid token-schema.json ({exc})")
            schema = {}
        fields = schema.get("fields") if isinstance(schema, dict) else None
        if not schema.get("title") or not schema.get("description") or not isinstance(fields, list) or not fields:
            errors.append(f"{label}: token-schema.json needs title, description and at least one field")
            fields = []
        keys = set()
        for field in fields:
            for attr in ("key", "label", "type", "required"):
                if attr not in field:
                    errors.append(f"{label}: token field is missing {attr}")
            if field.get("type") not in ("text", "password"):
                errors.append(f"{label}: token field type must be text or password")
            if re.search(r"KEY|TOKEN|SECRET", str(field.get("key", ""))) and field.get("type") != "password":
                errors.append(f"{label}: credential field {field.get('key')} must use type password")
            for attr, value in field.items():
                if attr.endswith("_en") and not isinstance(value, str):
                    errors.append(f"{label}: localized field {attr} must stay a string")
            keys.add(field.get("key"))
        if placeholders != keys:
            errors.append(f"{label}: mcp.json placeholders {sorted(placeholders)} must equal token fields {sorted(keys)}")

    needed = max((FEATURE_MIN_VERSION[f] for f in features), default=(0, 0, 0))
    declared = meta.get("minWorkbuddyVersion")
    if features and (not isinstance(declared, str) or version_tuple(declared) < needed):
        errors.append(f"{label}: minWorkbuddyVersion must be at least {'.'.join(map(str, needed))}")

    icons = [directory / name for name in ("icon.svg", "icon.png", "icon.jpg") if (directory / name).exists()]
    if len(icons) != 1:
        errors.append(f"{label}: exactly one icon.svg, icon.png or icon.jpg is required")
    elif icons[0].suffix == ".svg":
        try:
            if ET.parse(icons[0]).getroot().tag.rsplit("}", 1)[-1] != "svg":
                errors.append(f"{label}: icon.svg has no svg root element")
        except ET.ParseError as exc:
            errors.append(f"{label}: icon.svg is not valid XML ({exc})")

    skills = sorted((directory / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append(f"{label}: at least one skill is expected")
    for path in skills:
        values, body = parse_skill(path, errors)
        for field in SKILL_REQUIRED:
            if not values.get(field):
                errors.append(f"{path.relative_to(REPO)} must declare {field}")
        if values.get("name") and values["name"] != path.parent.name:
            errors.append(f"{path.relative_to(REPO)} name must match its directory")
        referenced = set(TOOL_RE.findall(body))
        hidden = referenced - exposed
        if hidden:
            errors.append(f"{path.relative_to(REPO)} references tools this connector hides: {sorted(hidden)}")

    for path in directory.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".md"}:
            text = path.read_text(encoding="utf-8")
            if re.search(r"Bearer\s+(?!\$\{)[A-Za-z0-9_-]{8,}", text) or re.search(r"\bei_[A-Za-z0-9_-]{12,}", text):
                errors.append(f"{path.relative_to(REPO)} appears to contain a real credential")


def check_examples(errors: list[str]) -> None:
    for item in load_platforms()["platforms"]:
        call = item["example_call"]
        actions = {action["action"]: action for action in item["actions"]}
        action = actions.get(call["action"])
        if action is None:
            errors.append(f"{item['platform']}: example action {call['action']!r} is not in the snapshot")
            continue
        allowed = set(action["required"]) | set(action["optional"])
        if action.get("max_limit") and not action.get("limit_ignored"):
            allowed.add("limit")
        params = set(call.get("params", {}))
        if params - allowed or set(action["required"]) - params:
            errors.append(f"{item['platform']}: example params {sorted(params)} do not fit {call['action']}")


def check() -> int:
    errors: list[str] = []
    try:
        files = generated_files()
    except (BuildError, KeyError, json.JSONDecodeError) as exc:
        print(f"WorkBuddy check failed: {exc}")
        return 1
    for relative, data in files.items():
        path = CONNECTORS / relative
        if not path.exists() or path.read_bytes() != data:
            errors.append(f"generated file is stale: workbuddy/connectors/{relative} (run render)")
    owned = set(files) | HAND_WRITTEN
    for path in CONNECTORS.rglob("*"):
        if path.is_file() and path.name != ".DS_Store" and path.relative_to(CONNECTORS).as_posix() not in owned:
            errors.append(f"unexpected file: {path.relative_to(REPO)}")
    for relative in HAND_WRITTEN:
        if not (CONNECTORS / relative).is_file():
            errors.append(f"missing hand-written file: workbuddy/connectors/{relative}")
    check_examples(errors)
    connectors = sorted(path for path in CONNECTORS.iterdir() if path.is_dir())
    for directory in connectors:
        check_connector(directory, errors)
    if errors:
        print("WorkBuddy check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    skills = sum(len(list((d / "skills").glob("*/SKILL.md"))) for d in connectors)
    print(f"WorkBuddy check passed: {len(connectors)} connectors, {skills} skills")
    return 0


def live_tools() -> set[str]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode()
    request = urllib.request.Request(MCP_URL, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        # Cloudflare rejects urllib's default User-Agent.
        "User-Agent": "everyinfra-workbuddy-build/1.0",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode("utf-8")
    payload = json.loads(text.split("data:", 1)[1] if text.lstrip().startswith("event:") else text)
    return {tool["name"] for tool in payload["result"]["tools"]}


def package(flat: bool, offline: bool = False) -> int:
    if check():
        return 1
    # disabledTools is a deny list, so a tool the server added after SERVER_TOOLS was written
    # would ship enabled. Refuse to package until SERVER_TOOLS matches the live server.
    if not offline:
        live = live_tools()
        if live != set(SERVER_TOOLS):
            print("WorkBuddy package refused: SERVER_TOOLS differs from the live tools/list")
            print(f"- missing from SERVER_TOOLS: {sorted(live - set(SERVER_TOOLS))}")
            print(f"- no longer served: {sorted(set(SERVER_TOOLS) - live)}")
            return 1
    DIST.mkdir(parents=True, exist_ok=True)
    for directory in sorted(path for path in CONNECTORS.iterdir() if path.is_dir()):
        meta = json.loads((directory / "connector-meta.json").read_text(encoding="utf-8"))
        suffix = "-flat" if flat else ""
        target = DIST / f"{directory.name}-{meta['version']}{suffix}.zip"
        members = sorted(p for p in directory.rglob("*") if p.is_file() and p.name != ".DS_Store")
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in members:
                inner = path.relative_to(directory).as_posix()
                name = inner if flat else f"{directory.name}/{inner}"
                info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        print(f"wrote {target.relative_to(REPO)} ({len(members)} files)")
    return 0


def refresh_catalog(catalog_path: Path) -> int:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    capabilities = catalog.get("capabilities")
    if not isinstance(capabilities, list):
        raise BuildError("catalog JSON must contain a capabilities array")
    data = load_platforms()
    for item in data["platforms"]:
        actions = []
        for cap in capabilities:
            if cap.get("platform") != item["platform"] or cap.get("available") is False:
                continue
            actions.append({
                "action": cap["action"],
                "label": cap.get("action_label") or cap["action"],
                "required": list(cap.get("required_params") or []),
                "optional": list(cap.get("optional_params") or []),
                "returns_list": bool(cap.get("returns_list")),
                "page_size": cap.get("page_size"),
                "page_size_varies": bool(cap.get("page_size_varies")),
                "limit_ignored": bool(cap.get("limit_ignored")),
                "max_limit": cap.get("max_limit"),
            })
        if not actions:
            raise BuildError(f"catalog has no capabilities for {item['platform']}")
        item["actions"] = actions
    PLATFORMS_FILE.write_bytes(dumps(data))
    print(f"Refreshed actions for {len(data['platforms'])} platforms")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("render")
    sub.add_parser("check")
    pack = sub.add_parser("package")
    pack.add_argument("--flat", action="store_true", help="put files at the ZIP root instead of a folder")
    pack.add_argument("--offline", action="store_true", help="skip the live tools/list comparison")
    refresh = sub.add_parser("refresh-catalog")
    refresh.add_argument("catalog", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "render":
            return render()
        if args.command == "check":
            return check()
        if args.command == "package":
            return package(args.flat, args.offline)
        return refresh_catalog(args.catalog)
    except BuildError as exc:
        print(f"error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
