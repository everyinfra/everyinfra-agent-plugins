---
name: everyinfra-crosscheck-research
display_name: EveryInfra 多来源核实
display_name_en: EveryInfra Cross-check Research
description: 用 EveryInfra 的 crosscheck 检索核实一个具体事实，或产出带出处的研究结论。用户要求核实、求证、查证某个说法，需要可靠出处，或要比较多个来源是否一致时使用。
description_zh: 用多种互相独立的检索方式核实一个事实，给出一致性判断和原始出处。
description_en: Verify a factual claim with mechanism-distinct retrieval and cite primary sources through EveryInfra crosscheck.
version: 1.0.0
author: EveryInfra
---

# EveryInfra 多来源核实

使用 MCP 工具 `everyinfra_search`，`tool` 设为 `crosscheck`，参数以工具输入说明为准。

1. 把用户的问题收敛成一个具体说法或判断问题，保留决定相关性的日期、地区、产品版本或站点范围。
2. 调用 `crosscheck`，让几条检索方式彼此独立；某一条失败时，不要用重复的关键词搜索顶替，也不要把它算作佐证。
3. 查看原始链接、来源发布日期；涉及新闻时同时看事件本身发生的日期。技术、政策、产品和机构类说法优先采用一手来源。
4. 分开列出一致的、矛盾的和缺失的证据。某条检索为空只代表不确定，不代表说法是假的。
5. 结论的强弱与证据相称，并引用原始来源，不引用搜索结果的包装页。
6. 只有返回里有 `billing` 时才报告费用，不要根据单价或调用成功来推断扣费。

查询范围和返回条数与问题规模相称。如果当前工具说明里没有 `crosscheck`，如实说明，并改用最贴近的检索方式，但不要把它说成等价的多来源核实。
