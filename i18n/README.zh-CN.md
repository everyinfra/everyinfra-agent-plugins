<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-zh-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-zh-light.svg">
    <img alt="一只线条蜘蛛走过小红书笔记、TikTok 视频和亚马逊商品页，脚落到的字段逐字打成 JSON。90 个平台的 414 个数据接口。" src="../assets/hero-zh-light.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://cursor.com/en/install-mcp?name=everyinfra&config=eyJ1cmwiOiJodHRwczovL2FwaS5ldmVyeWluZnJhLmNvbS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgPEFQSSBLZXk%2BIn19"><img src="https://img.shields.io/badge/在_Cursor_安装-2F363D?style=for-the-badge&logo=cursor&logoColor=white" alt="在 Cursor 安装"></a>
  <a href="https://vscode.dev/redirect/mcp/install?name=everyinfra&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.everyinfra.com%2Fmcp%22%2C%22headers%22%3A%7B%22Authorization%22%3A%22Bearer%20%3CAPI%20Key%3E%22%7D%7D"><img src="https://img.shields.io/badge/在_VS_Code_安装-0065A9?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="在 VS Code 安装"></a>
  <a href="#claude-code"><img src="https://img.shields.io/badge/Claude_Code-一条命令-B4532A?style=for-the-badge&logo=claude&logoColor=white" alt="Claude Code: 一条命令"></a>
  <a href="#codex"><img src="https://img.shields.io/badge/Codex-一条命令-2F363D?style=for-the-badge" alt="Codex: 一条命令"></a>
</p>

<p align="center">
  <a href="https://github.com/everyinfra/everyinfra-agent-plugins/stargazers"><img src="https://img.shields.io/github/stars/everyinfra/everyinfra-agent-plugins?style=social" alt="GitHub stars"></a>
  &nbsp;<b>给本仓库点个 Star，送 $1 额度。</b> <a href="https://everyinfra.com/zh/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=star_line#quickstart">领取方式 →</a>
</p>

<p align="center"><a href="../README.md">English</a> · <b>简体中文</b> · <a href="README.es.md">Español</a></p>

# EveryInfra MCP Server 与 Agent 插件

一个 API Key、一个 MCP 地址，拿到公开网页数据：**90 个平台的 414 个数据接口**，17 个搜索工具，52 种验证码识别。每千次调用 $0.56 起，失败或空结果不收费。

<table>
<tr><th width="50%">没有 EveryInfra</th><th width="50%">用了 EveryInfra</th></tr>
<tr><td valign="top">

- ❌ Agent 读不了 <img src="../assets/icons/tiktok.svg" width="16" height="16" alt=""> TikTok、<img src="../assets/icons/instagram.svg" width="16" height="16" alt=""> Instagram、<img src="../assets/icons/xiaohongshu.svg" width="16" height="16" alt=""> 小红书：登录和拦截把它挡在外面。
- ❌ 每个平台写一套爬虫，页面一改就得重写。
- ❌ 什么都没拿到，也照样付钱。

</td><td valign="top">

- ✅ Agent 自己选接口、自己检查参数。
- ✅ 每个平台都返回同一种 JSON 结构。
- ✅ 失败或空结果不收费。

</td></tr>
</table>

## 90 个平台，一种 JSON 结构

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/platform-wall-zh-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/platform-wall-zh-light.svg">
    <img alt="90 个平台中 23 个的标志和各自的接口数" src="../assets/platform-wall-zh-light.svg" width="100%">
  </picture>
</p>

<p align="center"><a href="https://everyinfra.com/zh/market?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=all_platforms"><b>查看全部 90 个平台和接口 →</b></a></p>

## 三步上手

**1. 拿一个 API Key**：在 [everyinfra.com](https://everyinfra.com/zh/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=quickstart#quickstart) 注册即可。只列出工具不需要 Key。

**2. 接到你的 Agent。**

<a id="claude-code"></a>*<img src="../assets/icons/claude.svg" width="16" height="16" alt=""> Claude Code*

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp \
  --header "Authorization: Bearer <API Key>"
```

<a id="codex"></a>*<img src="../assets/icons/codex.svg" width="16" height="16" alt=""> Codex*

```bash
export EVERYINFRA_API_KEY="<API Key>"
codex mcp add everyinfra --url https://api.everyinfra.com/mcp \
  --bearer-token-env-var EVERYINFRA_API_KEY
```

**<img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor / <img src="../assets/icons/vscode.svg" width="16" height="16" alt=""> VS Code**：点顶部的安装按钮，再把 `<API Key>` 换成你的 Key。

**3. 直接用中文提问。** Agent 会调用 `everyinfra_call_api`：

```txt
小红书搜「露营装备」，导出最近 7 天点赞最高的 50 条笔记的标题、点赞和评论数。
```

## 选 MCP、插件还是 REST？

| 你要 | 用 | 得到 |
| --- | --- | --- |
| 在 Agent 里直接调工具 | 远程 MCP | `https://api.everyinfra.com/mcp`，实时的工具定义 |
| 可复用的工作流 | 本插件 | 10 个 Skill（1 个路由、7 个产品、2 个工作流）和 MCP 元数据 |
| 写进应用或 CI | REST / SDK | [API 文档](https://everyinfra.com/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=path_rest_zh)、Python 和 Node 客户端 |

各宿主（<img src="../assets/icons/codex.svg" width="16" height="16" alt=""> Codex、<img src="../assets/icons/claude.svg" width="16" height="16" alt=""> Claude Code、<img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor、<img src="../assets/icons/copilot.svg" width="16" height="16" alt=""> GitHub Copilot、<img src="../assets/icons/qoder.svg" width="16" height="16" alt=""> Qoder、<img src="../assets/icons/codebuddy.svg" width="16" height="16" alt=""> CodeBuddy、<img src="../assets/icons/kimi.svg" width="16" height="16" alt=""> Kimi Code）的插件安装、仓库结构和校验命令见英文版 [Plugin install by host](../README.md#plugin-install-by-host)。

## 实时数字与活跃度

<!-- readme-stats: charts are regenerated daily, do not edit by hand -->

徽章每次打开页面都现读线上目录。两张图每天重新生成，分别读同一份目录和 EveryInfra 全部仓库（含未公开的网关仓，只统计数量）的 git 记录，图上写着更新时间。

<p><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsocial%2Fcatalog%3Fcompact%3D1&query=%24.platforms.length&label=%E4%B8%AA%E5%B9%B3%E5%8F%B0&color=0b6e64" alt="个平台"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsocial%2Fcatalog%3Fcompact%3D1&query=%24.capabilities.length&label=%E4%B8%AA%E6%95%B0%E6%8D%AE%E6%8E%A5%E5%8F%A3&color=0b6e64" alt="个数据接口"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsearch%2Ftools&query=%24.tools.length&label=%E4%B8%AA%E6%90%9C%E7%B4%A2%E5%B7%A5%E5%85%B7&color=0b6e64" alt="个搜索工具"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fcaptcha%2Ftypes&query=%24.types.length&label=%E7%A7%8D%E9%AA%8C%E8%AF%81%E7%A0%81&color=0b6e64" alt="种验证码"></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme-stats/coverage-zh-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/readme-stats/coverage-zh-light.svg">
  <img alt="按类别统计的平台数和数据接口数，读自线上目录" src="../assets/readme-stats/coverage-zh-light.svg" width="100%">
</picture>

### 一次调用怎么走

```mermaid
flowchart LR
  A["你的智能体"] --> B["MCP 或 REST"] --> C{"核对 Key 和余额"}
  C -- "通过" --> D["平台适配"] --> E["固定字段的 JSON"]
  C -- "没带 Key" --> F["401，不扣费"]
  D -. "失败或空结果" .-> G["按 charge_id 退款"]
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme-stats/activity-zh-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/readme-stats/activity-zh-light.svg">
  <img alt="EveryInfra 全部仓库每天的提交和每周的发版" src="../assets/readme-stats/activity-zh-light.svg" width="100%">
</picture>

## 社区

[<img src="../assets/icons/discord.svg" width="16" height="16" alt=""> Discord](https://discord.gg/9f6KmfekZC) · [<img src="../assets/icons/telegram.svg" width="16" height="16" alt=""> Telegram：Everyinfra bot](https://t.me/everyinfra_bot) · [Issues](https://github.com/everyinfra/everyinfra-agent-plugins/issues) · [价格](https://everyinfra.com/pricing?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=community_pricing_zh)

已上架 [<img src="../assets/icons/glama.svg" width="16" height="16" alt=""> Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra) · [<img src="../assets/icons/smithery.svg" width="16" height="16" alt=""> Smithery](https://smithery.ai/servers/everyinfra/api) · [<img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor Directory](https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data) · [魔搭 MCP 广场](https://www.modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra) · 官方 <img src="../assets/icons/mcp.svg" width="16" height="16" alt=""> MCP Registry（`io.github.xiaoxihexiaoyu/everyinfra`）。

<sub>数字取自 2026-10-24 的线上目录，以线上目录和 MCP 工具定义为准。平台图标来自 [Simple Icons](https://simpleicons.org)（CC0），品牌名称和标志归各自所有者。</sub>
