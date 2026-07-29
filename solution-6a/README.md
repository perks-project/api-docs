# Solution 6a — Procedure Execution API

## Overview

This spec documents all 24 actions of **Solution S6a** (`3f519f2c-518e-44e7-bf94-c834660018be`) plus the MCP transport endpoint.

## Transports

Actions are callable via two transports that share the same action identifiers:

- **Executioner REST** — `POST /api/executioner/actions/{actionId}` with input fields at the top level of the request body. Used by the procedure UI.
- **MCP** — `POST /mcp` (Streamable HTTP, protocol version `2025-06-18`, server "Onlim MCP server" 1.0.0). Of the 24 actions, **8 have category `MCP`** and are flagged `x-mcp-tool: true` in the spec.

## Actions

Each operation is annotated with `x-action-id`, `x-category`, `x-mcp-tool`, `x-branch`, and `x-version-id`.

| Tag | Description |
|-----|-------------|
| **Import** | Add/update a procedure (`ProcedureData` / `ImportProcess` schemas) and delete a procedure (`DeleteProcedureInput` / `DeleteProcedureResponse`, `204 No Content`) |
| **Discovery** | Search procedures by keyword, retrieve full step tree, fetch step detail, generic KG entity fetch |
| **Execution** | Start, record steps, pause/finish/cancel, resume, list executions by status, read room state, expand execution trace, report issues |
| **Config** | Org-wide key/value configuration |
| **Vector documents** | MUS upload and VCT vectorisation for document/vector querying |
| **Legacy chat** | Pre-new-UI chat-era actions kept on the branch; not used by the procedure UI |

## Authentication

All requests require **both** `x-api-key` and `x-organization-id` headers as a joint security requirement.

## Servers

| Environment | Base URL |
|-------------|----------|
| Production | `https://proxy.onlim.com/api/its` |
| Staging | `https://proxy-staging.onlim.com/api/its` |

Action IDs are stable across both environments; what differs per environment is which branch is activated for the calling organisation.
