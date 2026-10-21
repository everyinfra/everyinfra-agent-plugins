---
name: everyproxy
description: Use EveryProxy traffic-package REST APIs with the shared EveryInfra key. Use when the user wants to inspect proxy packages, order an authorized rotating or sticky proxy allocation, check provisioning status, or retrieve one-time proxy credentials.
---

# EveryProxy

EveryProxy is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with `Authorization: Bearer $EVERYINFRA_API_KEY`.

1. Read the free `GET /api/v1/proxy/catalog` response. Select a live package by `gb`, `kind`,
   `region` and optional `sticky_minutes`; pricing is by traffic, never by session minutes.
2. `POST /api/v1/proxy/order` is a paid order and may return credentials immediately. The user's
   request must authorize the package and region before ordering.
3. For asynchronous provisioning, inspect `GET /api/v1/proxy/order/{order_id}` without `deliver`.
   Status inspection must not be turned into a purchase.
4. Use `?deliver=1` only when the user intends to accept delivery and the charge. Delivery can expose
   the password exactly once.
5. Move credentials only to the user-approved secret destination. Never print them in normal chat,
   command logs, screenshots, source files or Git history.
6. Report order status and billing separately. If delivery failed and was refunded, create a new
   order only with user authorization.
