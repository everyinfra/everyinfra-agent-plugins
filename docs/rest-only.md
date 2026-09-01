# REST-only product boundary

The remote MCP server currently exposes EveryData, EverySearch, EveryAI and EverySolve. The skills
for EveryNumber, EveryMail and EveryProxy are public operating guidance for their REST APIs; they do
not add MCP tools and must not imply that MCP can execute those products.

## EveryNumber

Use the public SMS catalog before activation or rental. Activation billing occurs according to the
returned order state; rentals are charged at order time and are non-refundable. Treat received
codes and messages as sensitive credentials.

## EveryMail

Inspect catalog and usage before sending. Drafting is not dispatch authorization. Do not log
message bodies, verification codes, reset links, recipient lists, or domain-verification secrets.

## EveryProxy

Inspect the traffic-package catalog before ordering. Status inspection is not delivery.
Credential delivery may expose a password exactly once and must go only to a user-approved secret
destination.

## Promotion to MCP

A REST-only product may be described as MCP-enabled only after all of the following are true:

1. the production MCP server advertises the tool through live discovery;
2. its input and output schema, billing state, error model, and side-effect semantics are stable;
3. host authentication and scope behavior are tested;
4. this repository's skills, permissions documentation, manifests and validation cases are updated
   in the same release.
