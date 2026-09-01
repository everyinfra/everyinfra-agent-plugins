# Permissions, billing, and side effects

EveryInfra uses one account and wallet across product lines, while API keys can still be restricted
by product scope. Installing this plugin does not create an account, grant money, or change a key's
scope.

## Read and discovery operations

Capability catalogs, availability checks, schemas, usage reads, and order-status reads should be
used before paid operations. A read request must not be converted into a purchase, send, rental,
solve, or credential-delivery action.

## Paid operations

Pricing comes from the live catalog; actual charge evidence comes from a returned `billing` block
when the operation exposes one. Do not rely on a price copied into a skill, README, or model memory,
and do not claim an actual charge when an MCP tool omits the billing envelope. Request the largest
useful result within live limits when that avoids unnecessary repeated charges.

## External and sensitive actions

The user must authorize the actual scope of:

- captcha solving against an authorized target;
- phone-number activation or non-refundable rental;
- email dispatch and recipient list;
- proxy package purchase and one-time credential delivery;
- webhook, domain, credential, or account mutations.

Keep verification codes, proxy passwords, email bodies, API keys, cookies and provider credentials
out of normal chat output, command logs, source files and Git history.
