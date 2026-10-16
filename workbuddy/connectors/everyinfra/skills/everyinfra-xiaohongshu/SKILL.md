---
name: everyinfra-xiaohongshu
display_name: 小红书数据（EveryInfra）
display_name_en: EveryInfra Xiaohongshu (RedNote) Data
description: 用 EveryInfra 查询小红书公开数据：关键词搜索笔记、笔记详情、评论与回复、用户搜索、用户主页与作品、话题、热榜。用户提到小红书、RedNote、红书、笔记、种草等需求时使用。
description_zh: 查询小红书公开数据：关键词搜索笔记、笔记详情、评论与回复、用户搜索、用户主页与作品、话题、热榜。
description_en: Query public Xiaohongshu (RedNote) data, including note search, note details, comments and replies, user search, profiles and posts, topics and trending.
version: 1.0.0
author: EveryInfra
---

# 小红书数据

平台标识 `xiaohongshu`。调用前先用 `everyinfra_list_capabilities` 传 `{"platform": "xiaohongshu"}`，取当前的参数、允许值、单次条数、单价和返回字段；能力是否可用以目录和调用返回为准。然后用 `everyinfra_call_api` 调用。

## 常用能力

| action | 用途 | 必填参数 | 可选参数 | 返回条数 |
| --- | --- | --- | --- | --- |
| `search` | 关键词搜索 | `keyword` | `content_type`, `date_range`, `page_token`, `sort` | 每页 20 条，可翻页 |
| `profile` | 主页或对象详情 | `user_id` | 无 | 单条 |
| `user_posts` | 用户内容 | `user_id` | `page_token` | 每页 20 条，可翻页 |
| `note` | 笔记详情 | `url` | 无 | 单条 |
| `video` | 视频详情 | `url` | 无 | 单条 |
| `comments` | 评论 | `url` | `page_token`, `sort` | 每页 15 条，可翻页 |
| `comments_batch` | 多链接评论批量采集 | `urls` | `sort` | 每页 15 条，可翻页 |
| `sub_comments` | 评论回复 | `url`, `comment_id` | `page_token` | 每页 10 条，可翻页 |
| `search_users` | 用户搜索 | `keyword` | `follower_range`, `page_token`, `user_type` | 每页 20 条，可翻页 |
| `hashtag` | 话题内容 | `topic_id` | `page_token`, `sort` | 每页最多 20 条，可翻页 |
| `trending` | 热榜 | 无 | 无 | limit 最多 30 |

## 调用示例

用户：「搜索小红书上关于露营装备的笔记，按点赞排序，整理标题、点赞数和链接」

```json
{"platform": "xiaohongshu", "action": "search", "params": {"keyword": "露营装备", "sort": "most_liked"}}
```

## 注意

- search、user_posts 返回的正文可能是截断的摘要，要全文就用笔记链接调 note。
- video_url 是带签名的播放地址，会过期；需要留存时请及时下载。
- 按页返回的能力每次固定一页；要更多就把返回里的 `next_page_token` 作为 `page_token` 再调一次，每页算一次调用。
- 结果在 `results`；`billing` 写明这次是否扣费和实扣美元金额，报告费用以它为准。
- 需要多次付费调用（翻多页、多个链接或关键词）时，先按目录单价估算次数和费用告诉用户，得到同意再执行。
- 在 WorkBuddy 里保持同步模式，不要传 `mode=async`；超时就减小 `limit` 或拆分任务。
- `unauthorized` 或 `invalid_key`：请用户在 WorkBuddy 连接器设置里重新填写 EveryInfra API Key。`quota_exhausted`：提示用户到 everyinfra.com 充值。参数错误：按错误信息里的支持参数和拼写建议改正。`unavailable`：稍后再试，这次不扣费。`rate_limited`：稍等再试。
- 只用于公开数据的正当分析，遵守平台规则和个人信息保护相关法律；导出时只保留任务需要的字段。
