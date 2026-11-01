---
name: everyinfra-cli
description: Fetch public data from 100+ platforms (TikTok, Amazon, Instagram, Xiaohongshu, Google Maps and more), run web searches, solve CAPTCHAs and call an OpenAI-compatible AI API with the `everyinfra` command-line tool and one EveryInfra API key. Use it when a task needs platform data, search results or a CAPTCHA solution and a terminal is available.
---

# EveryInfra CLI

`everyinfra` is a thin command-line client for the EveryInfra API: platform data, web search, CAPTCHA
solving and the AI API, all paid from one wallet with one key.

Install: `pipx install everyinfra` (or `uv tool install everyinfra`, or `pip install everyinfra`).
Check the setup with `everyinfra doctor`.

## CLI or MCP

- Use the CLI when you have a shell: output goes to files and pipes, and large results do not fill your context.
- Use the MCP server (`https://api.everyinfra.com/mcp`) in chat apps without a terminal.
  `everyinfra mcp-config --client claude|cursor|codex|vscode` prints the config.

## The key

In Claude the plugin's API key setting reaches only the MCP server, so ask the user how they
want to supply the key for CLI calls, for example by running `everyinfra login` themselves;
never read it from a file or an environment variable.
Never print the key, put it in a file you share, or include it in a support ticket.
The catalog, `describe`, `captcha types`, `whats-new` and `--dry-run` work without a key.

## Standard flow

1. Find the capability (free): `everyinfra catalog --find "tiktok comments"`.
   Search tools: `everyinfra catalog --line search`. CAPTCHA types: `everyinfra captcha types`.
2. Read its contract (free): `everyinfra describe tiktok/comments`. It lists the parameters, allowed values,
   returned fields, the price and how paging works.
3. Preview the call (free): `everyinfra data tiktok comments -p url=... --limit 50 --dry-run`.
   It prints the exact request and the estimated cost. Nothing is sent.
4. Try a small real call: `--limit 5`. Check the result before you spend more.
5. Run the batch with a budget: `--max-cost-usd 2 --output result.json`. The CLI does not send a call whose
   estimate is over the budget.

Ask the user before a batch that costs more than they expect. Every paid command prints the charge and the
balance on stderr. `everyinfra account` shows the balance; `everyinfra billing` shows the spend.

## Parameters

- `-p key=value` is converted to the type in the catalog (integer, boolean, array and so on).
- `-p key:=JSON` passes raw JSON: `-p urls:='["https://a","https://b"]'`.
- Repeat `-p` for an array: `-p urls=https://a -p urls=https://b`. Arrays of targets are charged per target.
- Slow capabilities or large limits: add `--async --wait`, or `--async` and later `everyinfra job JOB_ID --wait`.
- Paged capabilities: `--pages 3` follows `next_page_token`. Each page is a separate paid call.

## Output

- Data goes to stdout and messages go to stderr.
- Output is JSON when piped or with `--json`. Use `--jsonl` for one result per line and `--fields a,b` for
  only some fields.
- For large results use `--output FILE`. Then stdout gets only a short summary.

## Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | OK | |
| 2 | Bad request (400, 422) | Fix the parameters. The error JSON on stderr has `param`, `did_you_mean` and `allowed`. |
| 3 | Auth or permission (401, 403) | Fix the key, or ask the user to top up (`ai_topup_required`) or enable a key permission. |
| 4 | Balance too low (402) | Ask the user to top up. Do not retry. |
| 5 | Rate limited (429) | Wait `retry_after` seconds from the error JSON, then retry. |
| 6 | Temporary failure (503) | Retry later. Failed calls are not charged. |
| 7 | Outcome unknown | Do not retry. The call may have run and been charged. Check it with `everyinfra requests --id REQUEST_ID` or `everyinfra job JOB_ID`. |
| 1 | Other | Read the error JSON. |

## Errors and support

Each error on stderr has the API's shape: `{"error": {"code", "message", "request_id", ...}}`. Keep the
`request_id`. When the error says the problem is on EveryInfra's side, draft a ticket with
`everyinfra support draft --subject ... --description ... --request-id ...`, show it to the user, and open
it with `everyinfra support open ... --yes` only after they agree.

## AI API

Accounts that have topped up can use the AI API at no charge: `everyinfra ai chat "..."` for one reply,
`everyinfra ai map --input rows.jsonl --instruction "..." --output out.jsonl` to label, translate or extract
fields row by row. `ai map` waits on rate limits and keeps the input order. Add `--resume` to continue a run.

Guide for agents: https://everyinfra.com/llms.txt
