# EveryInfra for WorkBuddy

[中文](#中文说明) · [English](#english)

## 中文说明

这里是 EveryInfra 在 WorkBuddy 开放平台上的连接器包（MCP + Skill）。连接器连到 EveryInfra 远程 MCP
服务的中国大陆入口 `https://api-cn.everyinfra.com/mcp`（与 `api.everyinfra.com` 是同一服务、同一套 API Key），用户在 WorkBuddy 的表单里填写自己的 EveryInfra API Key
（`auth_mode: token`，Key 只保存在用户本机），调用按 EveryInfra 账户计费。

**状态：已准备、已本地校验；未提交、未上架。** 目录里的文件不代表 WorkBuddy 已审核或已发布。

### 包含的连接器

| 连接器（source） | 名称 | 开放的工具 | 技能 |
| --- | --- | --- | --- |
| `everyinfra` | 万有引擎 EveryInfra | 能力目录、数据调用、网页检索 | 4 个通用技能 + 12 个平台技能 |
| `everyinfra-xiaohongshu` | EveryInfra 小红书数据 | 能力目录、数据调用 | 小红书 |
| `everyinfra-douyin` | EveryInfra 抖音数据 | 能力目录、数据调用 | 抖音 |
| `everyinfra-taobao` | EveryInfra 淘宝数据 | 能力目录、数据调用 | 淘宝 |
| `everyinfra-jd` | EveryInfra 京东数据 | 能力目录、数据调用 | 京东 |
| `everyinfra-alibaba1688` | EveryInfra 1688数据 | 能力目录、数据调用 | 1688 |
| `everyinfra-tiktok` | EveryInfra TikTok数据 | 能力目录、数据调用 | TikTok |

主连接器 `everyinfra` 覆盖全部平台；六个单平台连接器是可选的市场入口，与主连接器使用同一个 MCP
服务和同一种 API Key。AI 对话与验证码工具在本包里通过 `disabledTools` 关闭，WorkBuddy 用户只看到
数据与检索能力。

平台技能：小红书、抖音、淘宝、京东、1688、TikTok、快手、哔哩哔哩、微博、知乎、闲鱼、亚马逊。
通用技能：公开数据查询、网页检索、多来源核实、批量数据导出。

### 目录与生成

```text
workbuddy/platforms.json                 平台技能的名称、触发词、示例与能力快照（手写 + 快照）
workbuddy/connectors/everyinfra/         主连接器
  connector-meta.json                    手写
  skills/everyinfra-{data,search,crosscheck-research,bulk-data-export}/  手写
  mcp.json, token-schema.json, icon.svg, skills/everyinfra-<平台>/        生成
workbuddy/connectors/everyinfra-<平台>/   单平台连接器，全部生成
```

```bash
python3 scripts/build_workbuddy.py refresh-catalog <catalog.json>  # 用公开能力目录刷新能力快照
python3 scripts/build_workbuddy.py render                          # 写出全部生成文件
python3 scripts/build_workbuddy.py check                           # 生成物是否最新 + WorkBuddy 规则校验
python3 scripts/build_workbuddy.py package                         # 校验后在 dist/workbuddy/ 打 ZIP
```

能力快照来自公开目录 `GET https://api.everyinfra.com/api/v1/social/catalog`，只记录能力名、参数和
返回条数，不记录价格和实时可用性；价格与可用性始终以 `everyinfra_list_capabilities` 返回为准。

`check` 校验的规则来自 WorkBuddy 连接器文档：`source` 为 kebab-case 且与目录同名、名称/说明/中英文示例
齐全（示例 2–5 条，中文说明 20–100 字）、只配置一个 HTTPS 远程 MCP（地址固定为大陆入口）、`${VAR}` 占位与表单字段一一对应且
凭证字段为 password 类型、`minWorkbuddyVersion` 不低于所用字段的最低版本、技能 frontmatter 含
`description`/`description_zh`/`description_en`/`version`/`author` 且是合法 YAML、技能没有引用被关闭的工具、
文件中没有真实凭证。

### 提交前在 WorkBuddy 测试环境核对

1. 用 WorkBuddy 4.24.0 或更高版本导入连接器，填写测试 API Key，确认连接成功、只出现 3 个（单平台为 2 个）工具。
2. 调用一次能力目录（免费）和一次低价数据能力，确认返回、计费字段和错误提示可读。
3. 留存截图：市场卡片、Key 表单、连接成功状态、一次数据查询结果、一次网页检索结果。

## English

This directory holds EveryInfra's connector packages for the WorkBuddy open platform (MCP + Skill).
Each connector points at the mainland China entry of the remote MCP server,
`https://api-cn.everyinfra.com/mcp` (the same server and API keys as `api.everyinfra.com`); the user enters
their own EveryInfra API key in WorkBuddy's form (`auth_mode: token`, stored on the user's device
only), and calls are billed to their EveryInfra account.

**Status: prepared and validated locally; not submitted and not listed.**

- `everyinfra` is the main connector: capability discovery, data calls and web search, with four
  workflow skills and twelve platform skills.
- `everyinfra-<platform>` connectors are optional single-platform entries for Xiaohongshu, Douyin,
  Taobao, JD, 1688 and TikTok, using the same MCP server and API key.
- AI chat and CAPTCHA tools are hidden with `disabledTools` in this package.

Run `python3 scripts/build_workbuddy.py check` before handoff and
`python3 scripts/build_workbuddy.py package` to build the upload ZIPs under `dist/workbuddy/`.
