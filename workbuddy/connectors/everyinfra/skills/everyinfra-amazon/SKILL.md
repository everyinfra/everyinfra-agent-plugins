---
name: everyinfra-amazon
display_name: 亚马逊数据（EveryInfra）
display_name_en: EveryInfra Amazon Data
description: 用 EveryInfra 查询亚马逊公开数据：商品搜索、商品详情、评价、畅销榜、卖家搜索。用户提到亚马逊、Amazon、跨境电商、BSR、畅销榜等需求时使用。
description_zh: 查询亚马逊公开数据：商品搜索、商品详情、评价、畅销榜、卖家搜索。
description_en: Query public Amazon data, including product search, product details, reviews, bestsellers and seller search.
version: 1.0.0
author: EveryInfra
---

# 亚马逊数据

平台标识 `amazon`。调用前先用 `everyinfra_list_capabilities` 传 `{"platform": "amazon"}`，取当前的参数、允许值、单次条数、单价和返回字段；能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。

## 常用能力

| action | 用途 | 必填参数 | 可选参数 | 返回条数 |
| --- | --- | --- | --- | --- |
| `search` | 关键词搜索 | `keyword` | `domain`, `lang` | limit 最多 50 |
| `profile` | 主页或对象详情 | `url` | `lang` | 单条 |
| `reviews` | 评价 | `url` | `domain` | 列表 |
| `bestsellers` | 畅销榜 | `keyword` | `lang` | limit 最多 100 |
| `sellers` | 卖家搜索 | `keyword` | `lang` | limit 最多 50 |

## 调用示例

用户：「看看亚马逊上 standing desk 的畅销榜前 50」

```json
{"platform": "amazon", "action": "bestsellers", "params": {"keyword": "standing desk", "limit": 50}}
```

## 注意

- 按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
- 结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。
- 需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。
- 在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。
- `unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。
- 只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。
