# Security policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability, leaked credential, customer data exposure, billing
bypass, or provider credential disclosure. Use GitHub's private vulnerability reporting for this
repository when it is available. If it is unavailable, use the support channel published on
`https://everyinfra.com` and include only the minimum reproduction data.

Never include a production API key, session cookie, access token, received verification code,
proxy password, email body, or customer record in a report. Replace secrets with redacted markers
and provide request identifiers only when the support channel authorizes them.

## Supported versions

Security fixes are applied to the latest released version. This repository contains client
instructions and connection metadata; the remote EveryInfra service has its own deployment and
incident lifecycle.

## Trust model

Installing the plugin authorizes an agent host to load its skills and connect to the declared
remote MCP endpoint. It does not grant an API key, broaden key scopes, approve a paid call, or
authorize an external side effect. Review plugin changes before updating, especially changes to
MCP URLs, headers, skill instructions, permissions, and billing language.
