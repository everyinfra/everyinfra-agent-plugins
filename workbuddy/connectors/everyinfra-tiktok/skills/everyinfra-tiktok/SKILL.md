---
name: everyinfra-tiktok
display_name: TikTok数据（EveryInfra）
display_name_en: EveryInfra TikTok Data
description: 用 EveryInfra 查询TikTok公开数据：视频搜索、视频详情与文稿、评论、用户主页与作品、话题、粉丝数、电商商品与带货达人。用户提到TikTok、海外短视频、跨境达人、TikTok Shop等需求时使用。
description_zh: 查询TikTok公开数据：视频搜索、视频详情与文稿、评论、用户主页与作品、话题、粉丝数、电商商品与带货达人。
description_en: Query public TikTok data, including video search, video details and transcripts, comments, profiles and videos, hashtags, follower counts, shop products and creators.
version: 1.0.0
author: EveryInfra
---

# TikTok数据

平台标识 `tiktok`。调用前先用 `everyinfra_list_capabilities` 传 `{"platform": "tiktok"}`，取当前的参数、允许值、单次条数、单价和返回字段；能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。

## 常用能力

| action | 用途 | 必填参数 | 可选参数 | 返回条数 |
| --- | --- | --- | --- | --- |
| `search` | 关键词搜索 | `keyword` | `content_type` | limit 最多 200 |
| `profile` | 主页或对象详情 | `username` | 无 | 单条 |
| `user_videos` | 用户视频 | `username` | `min_likes`, `sort`, `until` | limit 最多 50 |
| `video` | 视频详情 | `url` | 无 | 单条 |
| `comments` | 评论 | `url` | 无 | limit 最多 200 |
| `hashtag` | 话题内容 | `hashtag` | 无 | limit 最多 30 |
| `followers` | 粉丝数量 | `username` | `channel` | 单条 |
| `transcript` | 视频文稿 | `url` | 无 | 单条 |
| `shop_search` | 电商商品搜索 | `keyword` | `country`, `page` | limit 最多 100 |
| `shop_creator` | 带货达人 | `username` | `country` | 单条 |

## 调用示例

用户：「搜索 TikTok 上关于 portable blender 的热门视频」

```json
{"platform": "tiktok", "action": "search", "params": {"keyword": "portable blender", "limit": 30}}
```

## 注意

- 按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
- 结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。
- 需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。
- 在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。
- `unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。
- 只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。
