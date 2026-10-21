---
name: everymail
description: Use EveryMail transactional-email REST APIs with the shared EveryInfra key. Use when the user asks to inspect email capabilities or quota, send or schedule a transactional email, submit a batch, cancel a scheduled message, inspect delivery events, or configure an authorized sending domain or webhook.
---

# EveryMail

EveryMail is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with `Authorization: Bearer $EVERYINFRA_API_KEY`.

1. Read `GET /api/v1/email/catalog` and, when authenticated, `GET /api/v1/email/usage`.
2. For a single message, use `POST /api/v1/email/send` with catalog-declared fields. Recipients are
   counted across `to`, `cc` and `bcc`; the API does not accept arbitrary `from`, headers or
   attachments.
3. Use `POST /api/v1/email/batch` for a true batch. Scheduled messages must use the single-send
   endpoint so cancellation and refunds remain unambiguous.
4. Sending email is an external communication. Do not send until the user has authorized the actual
   recipients and content; preparing a draft is not authorization to dispatch it.
5. Do not log message bodies, verification codes or reset links. Report the returned `message_id`,
   status, billing and quota without exposing private content.

Domain verification, webhook mutation and final dispatch are state-changing operations. Keep their
scope exact and do not broaden API-key permissions automatically.
