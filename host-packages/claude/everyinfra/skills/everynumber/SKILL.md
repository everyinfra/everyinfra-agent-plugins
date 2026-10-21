---
name: everynumber
description: Use EveryNumber activation and rental phone-number REST APIs with the shared EveryInfra key. Use when the user needs an authorized verification number, wants to poll a received code, cancel an unused activation, inspect order history, or rent a number for a supported term.
---

# EveryNumber

EveryNumber is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with an `Authorization: Bearer` header. In Claude the plugin's API key setting reaches only the MCP
server, so ask the user how they want to supply the key for REST calls; never read it from a file
or an environment variable.

## Activation flow

1. `GET /api/v1/sms/catalog` is free. Select the exact `country` and service string from it.
2. `POST /api/v1/sms/number` with `country`, `product` and optional `voice` or `reuse`.
3. Preserve the returned `order_id` and frozen quote. Poll
   `GET /api/v1/sms/code/{order_id}` at a reasonable interval.
4. Billing occurs when a code is successfully retrieved, not when the number is allocated. Read the
   returned `billing` block.
5. If the number is no longer needed before settlement, call
   `POST /api/v1/sms/cancel/{order_id}` so inventory is released.

## Rental flow

Use `GET /api/v1/sms/rental/catalog` before `POST /api/v1/sms/rental`. Rentals are charged at order
time and cannot be cancelled or renewed. Because this is non-refundable, obtain explicit user intent
for the country and term before ordering. Treat received codes and messages as sensitive one-time
credentials and do not store them in logs or project files.
