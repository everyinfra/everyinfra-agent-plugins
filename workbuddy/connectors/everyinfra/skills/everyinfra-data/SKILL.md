---
name: everyinfra-data
display_name: EveryInfra 公开数据查询
display_name_en: EveryInfra Public Data
description: 用 EveryInfra 查询社交、电商、点评、招聘、旅行、金融等平台的公开结构化数据，包括用户主页、内容、评论、搜索结果、商品、店铺和榜单。用户提到 EveryInfra、万有引擎，要求查询、采集或导出某个平台的公开数据，或所需平台没有专属技能时使用。
description_zh: 查询各平台的公开结构化数据：先查能力目录，再按目录参数调用，按次计费。
description_en: Query structured public data from social, commerce, review, jobs, travel and finance platforms through EveryInfra.
version: 1.0.0
author: EveryInfra
---

# EveryInfra 公开数据查询

本连接器向 AI 提供三个工具：

| 工具 | 用途 | 计费 |
| --- | --- | --- |
| `everyinfra_list_capabilities` | 列出平台与数据能力：每项能力的必填/可选参数、允许值、单次条数、单价和返回字段 | 免费 |
| `everyinfra_call_api` | 调用一项数据能力，返回结构化 JSON | 按次计费；失败或空结果不形成最终扣款 |
| `everyinfra_search` | 网页、学术、论坛检索，读网页正文，整站爬取，多来源核实 | 按次计费；用法见 everyinfra-search 技能 |

## 调用步骤

1. 先调 `everyinfra_list_capabilities`。已知平台就传 `platform`（如 `xiaohongshu`、`douyin`、`taobao`、`jd`、`amazon`），只看这个平台。
2. 从返回里选定 `platform` 和 `action`，读清楚必填参数、可选参数及允许值、单次条数（`page_size` 或 `max_limit`）、单价和返回字段。目录里没有的 action 和参数不要猜。
3. 调 `everyinfra_call_api`：

   ```json
   {"platform": "xiaohongshu", "action": "search", "params": {"keyword": "露营装备", "sort": "most_liked"}}
   ```

   | 参数 | 类型 | 必填 | 说明 |
   | --- | --- | --- | --- |
   | `platform` | string | 是 | 平台标识，取自能力目录 |
   | `action` | string | 是 | 能力标识，取自能力目录 |
   | `params` | object | 视能力而定 | 只放目录声明的参数 |
   | `mode` | string | 否 | 保持默认 `sync`，原因见下文 |

   - 按页返回的能力（目录标了 `page_size`，并写明 limit 不生效）每次固定返回一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
   - 其余列表能力可以传 `limit`，最大到 `max_limit`；一次给够比多次小批量更省。
4. 读返回：结果行在 `results`，列表能力另有 `count`；多链接、多目标的调用若有目标没取到，会带 `partial: true` 和 `missed` 列表，要如实告诉用户。`billing` 写明这次是否扣费（`charged`）和实扣美元金额（`amount`）；`quota` 是账户余额。向用户报告费用时用 `billing`，不要拿目录单价估算代替实扣。

## 在 WorkBuddy 里保持同步模式

`mode=async` 的结果需要拿 API Key 调 REST 接口轮询，而连接器不会把 Key 交给对话，所以在 WorkBuddy 里不要用 `async`。同步调用超时，就减小 `limit` 或把任务拆成几次。

## 费用与确认

- 能力目录免费；每项能力的单价在目录里按美元/次列出。
- 一次任务需要多次付费调用（翻多页、批量链接、多个关键词）时，先按目录单价估算调用次数和费用告诉用户，得到同意再开始。
- 用户只要求看看有哪些能力或怎么用时，只查目录，不发起付费调用。

## 错误与恢复

| 返回 | 含义 | 处理 |
| --- | --- | --- |
| `unauthorized` / `invalid_key` | 没有填写 API Key，或 Key 无效 | 请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key（在 everyinfra.com 控制台创建），不要重试 |
| `quota_exhausted` | 账户余额不足 | 提示用户到 everyinfra.com 充值，不要重试 |
| `missing_param` / `invalid_param` / `unknown_capability` | 参数或能力名不对 | 错误信息会列出支持的参数、允许值和拼写建议，按提示改正后再调一次 |
| `rate_limited` | 调用太频繁 | 等一会儿再调 |
| `unavailable` | 暂时无法提供 | 稍后再试；这次不扣费 |
| `timeout` | 同步调用超时 | 减小 `limit` 或拆分任务 |

## 数据与合规

- 只返回平台上公开可见的数据，字段已做规范化处理；不要承诺目录里没有的字段或非公开数据。
- 用于市场调研、内容与舆情分析、竞品和价格监测等正当用途；遵守目标平台规则和个人信息保护相关法律，不用于针对特定个人的跟踪、画像或骚扰。
- 导出含个人信息的数据（昵称、主页、评论）时，只保留任务需要的字段。

## 平台专属技能

小红书、抖音、淘宝、京东、1688、TikTok、快手、哔哩哔哩、微博、知乎、闲鱼、亚马逊各有一份专属技能，列了常用能力和示例。其他平台按本技能的步骤走。
