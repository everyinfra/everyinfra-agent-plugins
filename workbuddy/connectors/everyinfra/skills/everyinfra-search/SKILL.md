---
name: everyinfra-search
display_name: EveryInfra 网页检索
display_name_en: EveryInfra Web Search
description: 用 EveryInfra 做最新的网页、新闻、学术、论坛、商品和地点检索，读取指定网页正文，列出或爬取站点页面。用户要查最新信息、找出处、读某个链接、了解某个网站的内容，或需要多种检索方式时使用。
description_zh: 网页、新闻、学术、论坛检索与网页正文读取，返回原始来源链接，按次计费。
description_en: Web, news, academic, forum, shopping and place search plus page reading and site crawling through EveryInfra.
version: 1.0.0
author: EveryInfra
---

# EveryInfra 网页检索

使用 MCP 工具 `everyinfra_search`。它的 `tool` 枚举和参数以工具自带的输入说明为准。

```json
{"tool": "web", "params": {"q": "WorkBuddy 连接器 开放平台", "num": 10}}
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tool` | string | 是 | 检索方式，取自工具说明里的枚举 |
| `params` | object | 视检索方式而定 | 该检索方式的参数 |

## 选哪种检索

- 普通查找用 `web`；新闻用 `news`；论文和专利用 `scholar`；真人讨论用 `forum`；商品比价用 `shopping`；地点和商户用 `places`；图片视频用 `media`。
- 用一句话描述要找的内容、关键词搜不准时用 `semantic`；找与某个网页相似的页面用 `similar`。
- 已知链接直接用 `read` 读正文，不要再搜一遍；先看一个站有哪些页面用 `map`，要成批取正文用 `crawl`。
- 要断言具体事实（版本号、价格、政策、某项服务是否存在）时用 `crosscheck`，见 everyinfra-crosscheck-research 技能。
- `harvest` 可能要几分钟，容易超过同步时限；只在 `crawl` 拿不到时使用，并提前告诉用户可能较慢。

## 使用要求

- 查询条数与任务规模相称，不要为了保险把条数开到最大。
- 引用结论时给出返回结果里的原始来源链接。
- 空结果或失败不能当成「不存在」的证据，只能说明这次没检索到。
- 读返回里的 `billing` 了解是否扣费；失败或空结果通常不扣费，但以返回为准。

## 错误与恢复

- `unauthorized` / `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。
- `quota_exhausted`：余额不足，提示用户到 everyinfra.com 充值。
- 参数错误：错误信息会列出可用参数，按提示改正后再试一次。
- `rate_limited`：稍等再试。
