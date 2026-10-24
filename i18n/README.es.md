<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-light.svg">
    <img alt="EveryInfra: datos web públicos para agentes de IA. 413 capacidades de datos en 90 plataformas, 17 herramientas de búsqueda web y 52 tipos de CAPTCHA en un solo endpoint MCP." src="../assets/hero-light.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://cursor.com/en/install-mcp?name=everyinfra&config=eyJ1cmwiOiJodHRwczovL2FwaS5ldmVyeWluZnJhLmNvbS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgPEFQSSBLZXk%2BIn19"><img src="https://img.shields.io/badge/Install_in_Cursor-2F363D?style=for-the-badge&logo=cursor&logoColor=white" alt="Instalar en Cursor"></a>
  <a href="https://vscode.dev/redirect/mcp/install?name=everyinfra&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.everyinfra.com%2Fmcp%22%2C%22headers%22%3A%7B%22Authorization%22%3A%22Bearer%20%3CAPI%20Key%3E%22%7D%7D"><img src="https://img.shields.io/badge/Install_in_VS_Code-0065A9?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="Instalar en VS Code"></a>
  <a href="#claude-code"><img src="https://img.shields.io/badge/Claude_Code-un_comando-B4532A?style=for-the-badge&logo=claude&logoColor=white" alt="Añadir a Claude Code"></a>
  <a href="#codex"><img src="https://img.shields.io/badge/Codex-un_comando-2F363D?style=for-the-badge" alt="Añadir a Codex"></a>
</p>

<p align="center">
  <a href="https://github.com/everyinfra/everyinfra-agent-plugins/stargazers"><img src="https://img.shields.io/github/stars/everyinfra/everyinfra-agent-plugins?style=social" alt="GitHub stars"></a>
  &nbsp;<b>Danos una estrella en GitHub y obtén $1 de crédito.</b> Marca este repositorio con una estrella y reclama el crédito en la consola: va a tu saldo de bonificación y es válido durante 24 horas.
  <a href="https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=star_line_es#quickstart">Cómo reclamarlo →</a>
</p>

# Servidor MCP y plugin para agentes de EveryInfra

**Una clave API y un endpoint MCP para datos web públicos: 413 capacidades de datos en 90 plataformas, 17 herramientas de búsqueda web y resolución de CAPTCHA para 52 tipos. Pagas por llamada, desde $0.56 por cada 1.000 llamadas; las llamadas fallidas o vacías no se cobran.** Funciona con Claude Code, Cursor, Codex, VS Code y cualquier cliente MCP.

[![Validate](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/everyinfra/everyinfra-agent-plugins/actions/workflows/validate.yml)
[![Plugin version](https://img.shields.io/badge/plugin-v0.4.0-0A7F73)](../CHANGELOG.md)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-0A7F73)](../LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-0A7F73)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.xiaoxihexiaoyu/everyinfra)
[![Discord](https://img.shields.io/badge/Discord-join-5865F2?logo=discord&logoColor=white)](https://discord.gg/9f6KmfekZC)

[English](../README.md) · [简体中文](README.zh-CN.md) · **Español**

## Sin EveryInfra

- ❌ Tu agente no puede leer TikTok, Instagram ni Amazon: los inicios de sesión, los límites de uso y los bloqueos lo frenan.
- ❌ Escribes y mantienes un scraper para cada plataforma, y lo arreglas cada vez que cambia la página.
- ❌ Pagas por ejecuciones que no devuelven nada.

## Con EveryInfra

Tu agente encuentra la capacidad adecuada, revisa los parámetros obligatorios y devuelve datos estructurados. Copia un prompt:

```txt
Trae los 20 videos más recientes de TikTok con #skincare en una tabla con vistas, likes y comentarios.
```

```txt
Busca los 30 primeros resultados de Amazon para "silla ergonómica" y compara precio, valoración y número de reseñas.
```

```txt
Lista las 50 reseñas más recientes de Google Maps de un restaurante, con puntuación, fecha y texto.
```

## Plataformas

<p align="center">
  <a href="https://everyinfra.com/es/tiktok-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_tiktok_es"><img src="../assets/platforms/tiktok.svg" height="28" alt="TikTok"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/instagram-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_instagram_es"><img src="../assets/platforms/instagram.svg" height="28" alt="Instagram"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/youtube-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_youtube_es"><img src="../assets/platforms/youtube.svg" height="28" alt="YouTube"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/twitter-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_twitter_es"><img src="../assets/platforms/x.svg" height="28" alt="X / Twitter"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/reddit-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_reddit_es"><img src="../assets/platforms/reddit.svg" height="28" alt="Reddit"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/facebook-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_facebook_es"><img src="../assets/platforms/facebook.svg" height="28" alt="Facebook"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/threads-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_threads_es"><img src="../assets/platforms/threads.svg" height="28" alt="Threads"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/pinterest-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_pinterest_es"><img src="../assets/platforms/pinterest.svg" height="28" alt="Pinterest"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/xiaohongshu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_xiaohongshu_es"><img src="../assets/platforms/xiaohongshu.svg" height="28" alt="Xiaohongshu / RedNote"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/bilibili-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_bilibili_es"><img src="../assets/platforms/bilibili.svg" height="28" alt="Bilibili"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/weibo-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_weibo_es"><img src="../assets/platforms/sinaweibo.svg" height="28" alt="Weibo"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/zhihu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_zhihu_es"><img src="../assets/platforms/zhihu.svg" height="28" alt="Zhihu"></a>
  <br><br>
  <a href="https://everyinfra.com/es/taobao-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_taobao_es"><img src="../assets/platforms/taobao.svg" height="28" alt="Taobao"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/aliexpress-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_aliexpress_es"><img src="../assets/platforms/aliexpress.svg" height="28" alt="AliExpress"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/shopee-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_shopee_es"><img src="../assets/platforms/shopee.svg" height="28" alt="Shopee"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/etsy-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_etsy_es"><img src="../assets/platforms/etsy.svg" height="28" alt="Etsy"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/ebay-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_ebay_es"><img src="../assets/platforms/ebay.svg" height="28" alt="eBay"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/google-maps-reviews-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_google_maps_reviews_es"><img src="../assets/platforms/googlemaps.svg" height="28" alt="Google Maps reviews"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/spotify-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_spotify_es"><img src="../assets/platforms/spotify.svg" height="28" alt="Spotify"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/twitch-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_twitch_es"><img src="../assets/platforms/twitch.svg" height="28" alt="Twitch"></a>&nbsp;&nbsp;
  <a href="https://everyinfra.com/es/bluesky-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=logo_bluesky_es"><img src="../assets/platforms/bluesky.svg" height="28" alt="Bluesky"></a>
</p>

<p align="center">
  <a href="https://everyinfra.com/es/amazon-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_amazon_es">Amazon</a> ·
  <a href="https://everyinfra.com/es/linkedin-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_linkedin_es">LinkedIn</a> ·
  <a href="https://everyinfra.com/es/douyin-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_douyin_es">Douyin</a> ·
  <a href="https://everyinfra.com/es/jd-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_jd_es">JD.com</a> ·
  <a href="https://everyinfra.com/es/walmart-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_walmart_es">Walmart</a> ·
  <a href="https://everyinfra.com/es/temu-api?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=text_temu_es">Temu</a> ·
  <a href="https://everyinfra.com/es/market?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=all_platforms_es"><b>Las 90 plataformas →</b></a>
</p>

## Empieza en tres pasos

**1. Consigue una clave API** en [everyinfra.com](https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=quickstart_key_es#quickstart). Para listar herramientas no hace falta clave; las llamadas de pago sí la necesitan.

**2. Conecta tu herramienta.**

<a id="claude-code"></a>**Claude Code**

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp \
  --header "Authorization: Bearer <API Key>"
```

<a id="cursor"></a>**Cursor**: pulsa **Install in Cursor** arriba y luego sustituye `<API Key>` en Cursor Settings → MCP.

<a id="codex"></a>**Codex**

```bash
export EVERYINFRA_API_KEY="<API Key>"
codex mcp add everyinfra --url https://api.everyinfra.com/mcp \
  --bearer-token-env-var EVERYINFRA_API_KEY
```

**VS Code**: pulsa **Install in VS Code** arriba (abre un enlace `vscode:mcp/install`) y luego sustituye `<API Key>`.

**3. Pídeselo a tu agente.** Las herramientas se llaman `everyinfra_*`. Prueba uno de los prompts de arriba.

## ¿MCP, plugin o REST?

| Quieres | Usa | Obtienes |
| --- | --- | --- |
| Herramientas en vivo dentro de un agente | MCP remoto | `https://api.everyinfra.com/mcp`, esquemas de herramientas actuales |
| Flujos de trabajo reutilizables | Este plugin | 10 skills (1 router, 7 productos, 2 flujos) y metadatos MCP |
| Una aplicación o un job de CI | REST / SDK | [Documentación de la API](https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=path_rest_es), clientes de Python y Node |

La instalación del plugin en cada host (Codex, Claude Code, Cursor, GitHub Copilot, Qoder, CodeBuddy y Kimi Code), la estructura del repositorio y los comandos de validación están en la versión en inglés: [Plugin install by host](../README.md#plugin-install-by-host).

## Comunidad

[Discord](https://discord.gg/9f6KmfekZC) · [Telegram: Everyinfra bot](https://t.me/everyinfra_bot) · [Issues](https://github.com/everyinfra/everyinfra-agent-plugins/issues) · [Precios](https://everyinfra.com/es/pricing?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=community_pricing_es)

Disponible en [Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra) · [Smithery](https://smithery.ai/servers/everyinfra/api) · [Cursor Directory](https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data) · [ModelScope MCP](https://www.modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra) · el registro oficial de MCP (`io.github.xiaoxihexiaoyu/everyinfra`).

<sub>Cifras del catálogo en vivo del 2026-10-24. El catálogo en vivo y los esquemas de las herramientas MCP son la referencia. Iconos de plataformas: [Simple Icons](https://simpleicons.org) (CC0); los nombres y logotipos pertenecen a sus titulares.</sub>
