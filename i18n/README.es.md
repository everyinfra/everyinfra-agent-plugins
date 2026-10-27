<!-- rq223-banner -->
<p align="center"><img alt="EveryInfra MCP Server & Agent Plugin — Datos públicos de la web, búsqueda y CAPTCHA para agentes de IA, con una sola API key" src="../assets/banner-es.jpg" width="100%"></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/hero-es-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/hero-es-light.svg">
    <img alt="Una araña de líneas recorre una nota de Xiaohongshu, un vídeo de TikTok y un producto de Amazon; cada campo que pisa se escribe como JSON. 414 APIs de datos en 90 plataformas." src="../assets/hero-es-light.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://cursor.com/en/install-mcp?name=everyinfra&config=eyJ1cmwiOiJodHRwczovL2FwaS5ldmVyeWluZnJhLmNvbS9tY3AiLCJoZWFkZXJzIjp7IkF1dGhvcml6YXRpb24iOiJCZWFyZXIgPEFQSSBLZXk%2BIn19"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/deeplink/mcp-install-light.svg"><img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Add EveryInfra MCP server to Cursor" height="28"></picture></a>
  <a href="https://vscode.dev/redirect/mcp/install?name=everyinfra&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.everyinfra.com%2Fmcp%22%2C%22headers%22%3A%7B%22Authorization%22%3A%22Bearer%20%3CAPI%20Key%3E%22%7D%7D"><img src="https://img.shields.io/badge/Instalar_en_VS_Code-0065A9?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="Instalar en VS Code"></a>
  <a href="#claude-code"><img src="https://img.shields.io/badge/Claude_Code-un_comando-B4532A?style=for-the-badge&logo=claude&logoColor=white" alt="Claude Code: un comando"></a>
  <a href="#codex"><img src="https://img.shields.io/badge/Codex-un_comando-2F363D?style=for-the-badge" alt="Codex: un comando"></a>
  <a href="https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra"><img src="https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra/badges/score.svg" alt="EveryInfra MCP connector rated on Glama" height="28"></a>
</p>

<p align="center">
  <a href="https://github.com/everyinfra/everyinfra-agent-plugins/stargazers"><img src="https://img.shields.io/github/stars/everyinfra/everyinfra-agent-plugins?style=social" alt="GitHub stars"></a>
  &nbsp;<b>Dale una estrella al repo y recibe $1 de saldo.</b> <a href="https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=star_line#quickstart">Cómo reclamarlo →</a>
</p>

<p align="center"><a href="../README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>Español</b></p>

# Servidor MCP y plugin para agentes de EveryInfra

Una clave de API y un endpoint MCP para datos públicos de la web: **414 APIs de datos en 90 plataformas**, 17 herramientas de búsqueda web y resolución de CAPTCHA para 52 tipos. Desde $0.56 por 1.000 llamadas; las llamadas fallidas o vacías no se cobran.

<table>
<tr><th width="50%">Sin EveryInfra</th><th width="50%">Con EveryInfra</th></tr>
<tr><td valign="top">

- ❌ Tu agente no puede leer <img src="../assets/icons/tiktok.svg" width="16" height="16" alt=""> TikTok, <img src="../assets/icons/instagram.svg" width="16" height="16" alt=""> Instagram ni <img src="../assets/icons/xiaohongshu.svg" width="16" height="16" alt=""> Xiaohongshu: los inicios de sesión y los bloqueos lo detienen.
- ❌ Un scraper por plataforma, que hay que reescribir cada vez que cambia la página.
- ❌ Pagas por ejecuciones que no devuelven nada.

</td><td valign="top">

- ✅ Tu agente elige la API y valida los parámetros por sí mismo.
- ✅ Todas las plataformas responden con la misma estructura JSON.
- ✅ Las llamadas fallidas o vacías no se cobran.

</td></tr>
</table>

<!-- rq223-listed -->
## Disponible en 7 directorios

Cada tarjeta abre nuestra ficha en ese directorio.

<p align="center">
  <a href="https://modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra"><img src="../assets/launch-cards/modelscope-es.jpg" width="32%" alt="EveryInfra en ModelScope"></a>
  <a href="https://smithery.ai/servers/everyinfra/api"><img src="../assets/launch-cards/smithery-es.jpg" width="32%" alt="EveryInfra en Smithery"></a>
  <a href="https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data"><img src="../assets/launch-cards/cursor-es.jpg" width="32%" alt="EveryInfra en Cursor Directory"></a>
  <a href="https://clawhub.ai/skills/everyinfra"><img src="../assets/launch-cards/clawhub-es.jpg" width="32%" alt="EveryInfra en ClawHub"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=everyinfra"><img src="../assets/launch-cards/mcp-registry-es.jpg" width="32%" alt="EveryInfra en MCP Registry"></a>
  <a href="https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra"><img src="../assets/launch-cards/glama-es.jpg" width="32%" alt="EveryInfra en Glama"></a>
  <a href="https://integrations.sh/everyinfra.com"><img src="../assets/launch-cards/integrations-sh-es.jpg" width="32%" alt="EveryInfra en integrations.sh"></a>
</p>

## 90 plataformas, una sola estructura JSON

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/platform-wall-es-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="../assets/platform-wall-es-light.svg">
    <img alt="Logotipos de 23 de las 90 plataformas con su número de APIs" src="../assets/platform-wall-es-light.svg" width="100%">
  </picture>
</p>

<p align="center"><a href="https://everyinfra.com/es/market?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=all_platforms"><b>Las 90 plataformas y sus APIs →</b></a></p>

## Empieza en tres pasos

**1. Consigue una clave de API** en [everyinfra.com](https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=quickstart#quickstart). Para listar las herramientas no hace falta clave.

**2. Añádelo a tu agente.**

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

**<img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor / <img src="../assets/icons/vscode.svg" width="16" height="16" alt=""> VS Code**: pulsa el botón de instalación de arriba y sustituye `<API Key>`.

**3. Pregunta con tus palabras.** Tu agente llama a `everyinfra_call_api`:

```txt
Busca los 30 primeros resultados de «standing desk» en Amazon y compara precio, valoración y número de reseñas.
```

## ¿MCP, plugin o REST?

| Quieres | Usa | Obtienes |
| --- | --- | --- |
| Herramientas en vivo dentro de un agente | MCP remoto | `https://api.everyinfra.com/mcp`, esquemas de herramientas actuales |
| Flujos de trabajo reutilizables | Este plugin | 10 skills (1 router, 7 productos, 2 flujos) y metadatos MCP |
| Una aplicación o un job de CI | REST / SDK | [Documentación de la API](https://everyinfra.com/es/docs?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=path_rest_es), clientes de Python y Node |

La instalación del plugin en cada host (<img src="../assets/icons/codex.svg" width="16" height="16" alt=""> Codex, <img src="../assets/icons/claude.svg" width="16" height="16" alt=""> Claude Code, <img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor, <img src="../assets/icons/copilot.svg" width="16" height="16" alt=""> GitHub Copilot, <img src="../assets/icons/qoder.svg" width="16" height="16" alt=""> Qoder, <img src="../assets/icons/codebuddy.svg" width="16" height="16" alt=""> CodeBuddy y <img src="../assets/icons/kimi.svg" width="16" height="16" alt=""> Kimi Code), la estructura del repositorio y los comandos de validación están en la versión en inglés: [Plugin install by host](../README.md#plugin-install-by-host).

## Cifras en vivo y actividad

<!-- readme-stats: charts are regenerated daily, do not edit by hand -->

Las insignias leen los catálogos en vivo cada vez que se abre la página. Los dos gráficos se regeneran cada día con esos catálogos y con el historial git de todos los repositorios de EveryInfra, incluido el gateway privado (solo recuentos); cada uno muestra su hora de actualización.

<p><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsocial%2Fcatalog%3Fcompact%3D1&query=%24.platforms.length&label=plataformas&color=0b6e64" alt="plataformas"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsocial%2Fcatalog%3Fcompact%3D1&query=%24.capabilities.length&label=APIs+de+datos&color=0b6e64" alt="APIs de datos"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fsearch%2Ftools&query=%24.tools.length&label=herramientas+de+b%C3%BAsqueda&color=0b6e64" alt="herramientas de búsqueda"> <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.everyinfra.com%2Fapi%2Fv1%2Fcaptcha%2Ftypes&query=%24.types.length&label=tipos+de+CAPTCHA&color=0b6e64" alt="tipos de CAPTCHA"></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme-stats/coverage-es-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/readme-stats/coverage-es-light.svg">
  <img alt="Plataformas y APIs de datos por categoría, leídas del catálogo en vivo" src="../assets/readme-stats/coverage-es-light.svg" width="100%">
</picture>

### Cómo fluye una llamada

```mermaid
flowchart LR
  A["Tu agente"] --> B["MCP o REST"] --> C{"Key y saldo"}
  C -- "ok" --> D["Adaptador de plataforma"] --> E["JSON con campos fijos"]
  C -- "sin key" --> F["401, sin cargo"]
  D -. "fallido o vacío" .-> G["Reembolso por charge_id"]
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/readme-stats/activity-es-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/readme-stats/activity-es-light.svg">
  <img alt="Commits por día en todos los repositorios de EveryInfra y versiones por semana" src="../assets/readme-stats/activity-es-light.svg" width="100%">
</picture>

## Comunidad

[<img src="../assets/icons/discord.svg" width="16" height="16" alt=""> Discord](https://discord.gg/9f6KmfekZC) · [<img src="../assets/icons/telegram.svg" width="16" height="16" alt=""> Telegram: Everyinfra bot](https://t.me/everyinfra_bot) · [Issues](https://github.com/everyinfra/everyinfra-agent-plugins/issues) · [Precios](https://everyinfra.com/es/pricing?utm_source=github&utm_medium=readme&utm_campaign=everyinfra-agent-plugins&utm_content=community_pricing_es)

Disponible en [<img src="../assets/icons/glama.svg" width="16" height="16" alt=""> Glama](https://glama.ai/mcp/connectors/io.github.xiaoxihexiaoyu/everyinfra) · [<img src="../assets/icons/smithery.svg" width="16" height="16" alt=""> Smithery](https://smithery.ai/servers/everyinfra/api) · [<img src="../assets/icons/cursor.svg" width="16" height="16" alt=""> Cursor Directory](https://cursor.directory/plugins/everyinfra-tiktok-instagram-amazon-data) · [<img src="../assets/icons/modelscope.svg" width="16" height="16" alt=""> ModelScope MCP](https://www.modelscope.cn/mcp/servers/xiaoyuaimaomao/EveryInfra) · [<img src="../assets/icons/clawhub.svg" width="16" height="16" alt=""> ClawHub](https://clawhub.ai/skills/everyinfra) · [integrations.sh](https://integrations.sh/everyinfra.com) · el registro oficial de MCP (`io.github.xiaoxihexiaoyu/everyinfra`).

<sub>Cifras del catálogo en vivo del 2026-10-24. El catálogo en vivo y los esquemas de las herramientas MCP son la referencia. Iconos de plataformas: [Simple Icons](https://simpleicons.org) (CC0); los nombres y logotipos pertenecen a sus titulares.</sub>
