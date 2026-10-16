---
name: everyinfra-douyin
display_name: 抖音数据（EveryInfra）
display_name_en: EveryInfra Douyin Data
description: 用 EveryInfra 查询抖音公开数据：视频搜索、视频详情与文稿、评论、用户主页与作品、热榜、达人搜索与分析、商品搜索。用户提到抖音、短视频、达人、星图、带货、热榜等需求时使用。
description_zh: 查询抖音公开数据：视频搜索、视频详情与文稿、评论、用户主页与作品、热榜、达人搜索与分析、商品搜索。
description_en: Query public Douyin data, including video search, video details and transcripts, comments, profiles and posts, trending, creator search and analytics, product search.
version: 1.0.0
author: EveryInfra
---

# 抖音数据

平台标识 `douyin`。调用前先用 `everyinfra_list_capabilities` 传 `{"platform": "douyin"}`，取当前的参数、允许值、单次条数、单价和返回字段；能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。

## 常用能力

| action | 用途 | 必填参数 | 可选参数 | 返回条数 |
| --- | --- | --- | --- | --- |
| `search` | 关键词搜索 | `keyword` | `publish_time`, `sort` | limit 最多 50 |
| `profile` | 主页或对象详情 | `user_id` | 无 | 单条 |
| `user_posts` | 用户内容 | `user_id` | `page_token`, `since` | limit 最多 100 |
| `video` | 视频详情 | `url` | 无 | 单条 |
| `comments` | 评论 | `url` | `page_token` | limit 最多 150 |
| `trending` | 热榜 | 无 | `boards` | limit 最多 60 |
| `transcript` | 视频文稿 | `url` | 无 | 单条 |
| `creator_search` | 达人搜索 | `keyword` | `follower_range`, `user_type` | limit 最多 20 |
| `creator_audience` | 达人粉丝画像 | `user_id` | `dimension` | 单条 |
| `creator_trend` | 达人涨粉趋势 | `user_id` | 无 | 单条 |
| `creator_benchmark` | 达人同类对标 | `user_id` | 无 | 单条 |
| `xingtu_creator_search` | 星图达人搜索 | `keyword` | 无 | limit 最多 20 |
| `xingtu_creator_analytics` | 星图达人分析 | `douyin_id` | 无 | 单条 |
| `xingtu_rate_card` | 星图达人报价 | `douyin_id` | 无 | 单条 |
| `xingtu_creator_rankings` | 星图达人榜单 | `industry`, `ranking_type`, `time_window` | 无 | limit 最多 5 |
| `product_search` | 商品搜索 | `keyword` | 无 | limit 最多 5 |
| `product_detail` | 商品详情 | `product_id` | 无 | 单条 |
| `live_product_search` | 直播商品搜索 | `keyword` | 无 | limit 最多 3 |

## 调用示例

用户：「看看抖音今天的热榜前 30」

```json
{"platform": "douyin", "action": "search", "params": {"keyword": "咖啡探店", "limit": 20}}
```

## 注意

- 按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
- 结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。
- 需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。
- 在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。
- `unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。
- 只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。
