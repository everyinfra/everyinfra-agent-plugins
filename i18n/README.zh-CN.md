<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img alt="EveryInfra：给 AI Agent 的公开网页数据。90 个平台 413 项数据能力、17 个网页搜索工具、52 种验证码，一个 MCP 地址。" src="../assets/hero-light.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://cursor.com/en/install-mcp?name=everyinfra&config=eyJ1cmwiOiJodHRwczovL2FwaS5ldmVyeWluZnJhLmNvbS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgPEFQSSBLZXk%2BIn19"><img src="https://img.shields.io/badge/Install_in_Cursor-2F363D?style=for-the-badge&logo=cursor&logoColor=white" alt="在 Cursor 中安装"></a>
  <a href="https://vscode.dev/redirect/mcp/install?name=everyinfra&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.everyinfra.com%2Fmcp%22%2C%22headers%22%3A%7B%22Authorization%22%3A%22Bearer%20%3CAPI%20Key%3E%22%7D%7D"><img src="https://img.shields.io/badge/Install_in_VS_Code-0065A9?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="在 VS Code 中安装"></a>
  <a href="#claude-code"><img src="https://img.shields.io/badge/Claude_Code-一条命令-B4532A?style=for-the-badge&logo=claude&logoColor=white" alt="添加到 Claude Code"></a>
  <a href="#codex"><img src="https://img.shields.io/badge/Codex-一条命令-2F363D?style=for-the-badge" alt="添加到 Codex"></a>
</p>

<p align="center">
  <a href="https://github.com/everyinfra/everyinfra-agent-plugins/stargazers"><img src="https://img.shields.io/github/stars/everyinfra/everyinfra-agent-plugins?style=social" alt="GitHub stars"></a>
  &nbsp;<b>在 GitHub 点星领 $1 额度。</b> 给本仓库点星，再到控制台「余额与充值」领取：直接进赠送余额，24 小时内有效。
  <a href="https://everyinfra.com/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=star_line_zh#quickstart">怎么领 →</a>
</p>

# EveryInfra MCP 服务器与 Agent 插件

**一个 Key、一个 MCP 地址，拿到 90 个平台的公开数据：413 项数据能力、17 个网页搜索工具、52 种验证码识别。按次计费，每千次 $0.56 起；失败和空结果不扣费。** 支持 Claude Code、Cursor、Codex、VS Code 和任意 MCP 客户端。

[![Validate](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml)
[![Plugin version](https://img.shields.io/badge/plugin-v0.4.0-0A7F73)](../CHANGELOG.md)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-0A7F73)](../LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-0A7F73)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.xiaoxihexiaoyu/everyinfra)
[![Discord](https://img.shields.io/badge/Discord-join-5865F2?logo=discord&logoColor=white)](https://discord.gg/9f6KmfekZC)

[English](../README.md) · **简体中文** · [Español](README.es.md)

## 没有 EveryInfra 时

- ❌ Agent 读不到小红书、抖音、TikTok：要登录、被限流、请求被拦，它就卡住了。
- ❌ 每个平台各写一套爬虫，页面一改就得修。
- ❌ 跑空了也照样付钱。

## 有了 EveryInfra

Agent 自己找到对口的能力、核对必填参数，返回结构化数据。复制一条试试：

```txt
小红书搜「露营装备」，导出前 50 条笔记的标题、点赞和评论数。
```

```txt
抖音搜「咖啡探店」，列出点赞最高的 20 条视频和作者。
```

```txt
淘宝搜「人体工学椅」，按热度列出前 10 个商品的价格、店铺和销量。
```

## 覆盖的平台

<p align="center">
  <a href="https://everyinfra.com/tiktok-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_tiktok_zh"><img src="../assets/platforms/tiktok.svg" height="28" alt="TikTok"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/instagram-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_instagram_zh"><img src="../assets/platforms/instagram.svg" height="28" alt="Instagram"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/youtube-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_youtube_zh"><img src="../assets/platforms/youtube.svg" height="28" alt="YouTube"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/twitter-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_twitter_zh"><img src="../assets/platforms/x.svg" height="28" alt="X / Twitter"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/reddit-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_reddit_zh"><img src="../assets/platforms/reddit.svg" height="28" alt="Reddit"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/facebook-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_facebook_zh"><img src="../assets/platforms/facebook.svg" height="28" alt="Facebook"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/threads-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_threads_zh"><img src="../assets/platforms/threads.svg" height="28" alt="Threads"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/pinterest-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_pinterest_zh"><img src="../assets/platforms/pinterest.svg" height="28" alt="Pinterest"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/xiaohongshu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_xiaohongshu_zh"><img src="../assets/platforms/xiaohongshu.svg" height="28" alt="Xiaohongshu / RedNote"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/bilibili-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_bilibili_zh"><img src="../assets/platforms/bilibili.svg" height="28" alt="Bilibili"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/weibo-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_weibo_zh"><img src="../assets/platforms/sinaweibo.svg" height="28" alt="Weibo"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/zhihu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_zhihu_zh"><img src="../assets/platforms/zhihu.svg" height="28" alt="Zhihu"></a>
  <br><br>
  <a href="https://everyinfra.com/taobao-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_taobao_zh"><img src="../assets/platforms/taobao.svg" height="28" alt="Taobao"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/aliexpress-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_aliexpress_zh"><img src="../assets/platforms/aliexpress.svg" height="28" alt="AliExpress"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/shopee-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_shopee_zh"><img src="../assets/platforms/shopee.svg" height="28" alt="Shopee"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/etsy-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_etsy_zh"><img src="../assets/platforms/etsy.svg" height="28" alt="Etsy"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/ebay-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_ebay_zh"><img src="../assets/platforms/ebay.svg" height="28" alt="eBay"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/google-maps-reviews-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_google_maps_reviews_zh"><img src="../assets/platforms/googlemaps.svg" height="28" alt="Google Maps reviews"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/spotify-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_spotify_zh"><img src="../assets/platforms/spotify.svg" height="28" alt="Spotify"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/twitch-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_twitch_zh"><img src="../assets/platforms/twitch.svg" height="28" alt="Twitch"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/bluesky-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_bluesky_zh"><img src="../assets/platforms/bluesky.svg" height="28" alt="Bluesky"></a>
</p>

<p align="center">
  <a href="https://everyinfra.com/amazon-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_amazon_zh">Amazon</a> ·
  <a href="https://everyinfra.com/linkedin-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_linkedin_zh">LinkedIn</a> ·
  <a href="https://everyinfra.com/douyin-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_douyin_zh">抖音</a> ·
  <a href="https://everyinfra.com/jd-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_jd_zh">京东</a> ·
  <a href="https://everyinfra.com/walmart-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_walmart_zh">Walmart</a> ·
  <a href="https://everyinfra.com/temu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_temu_zh">Temu</a> ·
  <a href="https://everyinfra.com/market?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=all_platforms_zh"><b>全部 90 个平台 →</b></a>
</p>

## 三步上手

**1. 拿 API Key**：在 [everyinfra.com](https://everyinfra.com/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=quickstart_key_zh#quickstart) 注册并创建。列工具不需要 Key，付费调用需要。

**2. 接入你的工具。**

<a id="claude-code"></a>**Claude Code**

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp \
  --header "Authorization: Bearer <API Key>"
```

<a id="cursor"></a>**Cursor**：点上面的 **Install in Cursor**，再到 Cursor Settings → MCP 把 `<API Key>` 换成你的 Key。

<a id="codex"></a>**Codex**

```bash
export EVERYINFRA_API_KEY="<API Key>"
codex mcp add everyinfra --url https://api.everyinfra.com/mcp \
  --bearer-token-env-var EVERYINFRA_API_KEY
```

**VS Code**：点上面的 **Install in VS Code**（会打开 `vscode:mcp/install` 链接），再把 `<API Key>` 换成你的 Key。

在中国大陆，可以把地址换成 `https://api-cn.everyinfra.com/mcp`：同一个服务，同一个 Key。

**3. 直接问 Agent。** 工具名都以 `everyinfra_` 开头，试试上面的提示词。

## 选 MCP、插件还是 REST？

| 你要 | 用 | 得到 |
| --- | --- | --- |
| 在 Agent 里直接调工具 | 远程 MCP | `https://api.everyinfra.com/mcp`，实时的工具定义 |
| 可复用的工作流 | 本插件 | 10 个 Skill（1 个路由、7 个产品、2 个工作流）和 MCP 元数据 |
| 写进应用或 CI | REST / SDK | [API 文档](https://everyinfra.com/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=path_rest_zh)、Python 和 Node 客户端 |

各宿主（Codex、Claude Code、Cursor、GitHub Copilot、Qoder、CodeBuddy、Kimi Code）的插件安装、仓库结构和校验命令见英文版 [Plugin install by host](../README.md#plugin-install-by-host)。

## 社区

[Discord](https://discord.gg/9f6KmfekZC) · [Telegram：Everyinfra bot](https://t.me/everyinfra_bot) · [Issues](https://github.com/everyinfra/everyinfra-agent-plugins/issues) · [价格](https://everyinfra.com/pricing?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=community_pricing_zh)

已上架 [Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra) · [Smithery](https://smithery.ai/servers/everyinfra/api) · [Cursor Directory](https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data) · [魔搭 MCP 广场](https://www.modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra) · 官方 MCP Registry（`io.github.xiaoxihexiaoyu/everyinfra`）。

<sub>数字取自 2026-10-24 的线上目录，以线上目录和 MCP 工具定义为准。平台图标来自 [Simple Icons](https://simpleicons.org)（CC0），品牌名称和标志归各自所有者。</sub>
