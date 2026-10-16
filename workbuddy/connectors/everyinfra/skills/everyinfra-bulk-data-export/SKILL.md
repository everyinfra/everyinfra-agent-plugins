---
name: everyinfra-bulk-data-export
display_name: EveryInfra 批量数据导出
display_name_en: EveryInfra Bulk Data Export
description: 通过 EveryInfra 批量取得某个平台的公开数据并导出为 CSV 或 JSON，包含能力确认、费用预估、翻页、去重和文件校验。用户要很多条记录、所有页、一个数据集，或要求导出成表格、CSV、JSON 文件时使用。
description_zh: 批量取数并导出 CSV/JSON：先估算次数和费用，再翻页、去重并校验文件。
description_en: Export a bounded dataset to CSV or JSON through EveryInfra with cost estimates, pagination, deduplication and file checks.
version: 1.0.0
author: EveryInfra
---

# EveryInfra 批量数据导出

使用 `everyinfra_list_capabilities` 和 `everyinfra_call_api`。这是会多次付费调用的流程，不是「一直取到没有为止」的许可。

## 调用之前

1. 确认目标条数、需要的字段、输出格式，以及时间或费用上限。
2. 用 `everyinfra_list_capabilities` 确认准确的 platform/action，读必填参数、翻页方式、`page_size` 或 `max_limit` 和当前单价。不要猜接口名或翻页参数名。
3. 按目标条数和单次条数估算最多要调用几次、大约花多少钱，告诉用户并得到同意后再开始；用户已经明确批准过同样范围的花费时可以直接执行。

## 取数与停止

- 每次在上限内取尽量多的条数。
- 只使用能力返回或声明的翻页字段：把 `next_page_token` 作为下一次的 `page_token`。
- 出现以下情况立即停止：返回表明没有下一页、达到目标条数或调用次数、预算用完、翻页不再前进。
- 只对临时性失败（`unavailable`、`timeout`、`rate_limited`）做少量重试；鉴权、参数、余额错误不要重试。
- 用返回里稳定的 ID 去重；没有 ID 时说明用了哪些字段组合作为去重键，不要悄悄丢掉看起来相似的记录。
- 在 WorkBuddy 里保持同步模式，不要用 `mode=async`；单次超时就减小 `limit`。

## 交付与校验

- JSON 保留所选字段和原始类型。
- CSV 使用稳定的表头，只展开导出需要的字段；展开会丢失含义的嵌套内容保留在 JSON 里。
- 校验文件存在、非空、能解析，且去重键没有重复。
- 向用户报告：目标条数和实际条数、调用次数、去掉的重复数、提前停止的原因、文件位置，以及各次返回 `billing` 实扣金额的合计。返回里没有 `billing` 时，说明实际扣费无法从返回中确认，不要用目录单价代替。
- 导出含个人信息的字段（昵称、主页、评论）时只保留任务需要的部分。
