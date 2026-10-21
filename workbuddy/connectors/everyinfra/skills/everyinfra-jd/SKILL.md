---
name: everyinfra-jd
display_name: 京东数据（EveryInfra）
display_name_en: EveryInfra JD.com Data
description: 用 EveryInfra 查询京东公开数据：商品搜索、商品详情、全部 SKU 与价格、商品介绍详情图。用户提到京东、JD、商品、SKU、价格等需求时使用。
description_zh: 查询京东公开数据：商品搜索、商品详情、全部 SKU 与价格、商品介绍详情图。
description_en: Query public JD.com data, including product search, product details, all SKUs and prices, and product description images.
version: 1.0.0
author: EveryInfra
---

# 京东数据

平台标识 `jd`。调用前先用 `everyinfra_list_capabilities` 传 `{"platform": "jd"}`，取当前的参数、允许值、单次条数、单价和返回字段；能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。

## 常用能力

| action | 用途 | 必填参数 | 可选参数 | 返回条数 |
| --- | --- | --- | --- | --- |
| `search` | 关键词搜索 | `keyword` | 无 | limit 最多 5 |
| `product_detail` | 商品详情 | `item_id` | 无 | 单条 |
| `skus` | 全部 SKU 与价格 | `item_id` | 无 | limit 最多 100 |
| `description_images` | 商品介绍详情图 | `item_id` | 无 | 列表 |

## 调用示例

用户：「搜索京东上的机械键盘，列出价格和店铺」

```json
{"platform": "jd", "action": "search", "params": {"keyword": "机械键盘"}}
```

## 注意

- 按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
- 结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。
- 需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。
- 在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。
- `unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。
- 只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。
