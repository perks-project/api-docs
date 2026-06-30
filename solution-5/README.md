# Solution 5 - API Docs

This folder documents the API exposed by PERKS Solution 5 (S5), the Procedural Knowledge Management System (PKMS) backbone service.

S5 provides:
- Asset lifecycle APIs for storage, retrieval, update, deletion, and version inspection
- Policy-restricted access request and review workflows
- Attachment upload/download/deletion with optional signed URL access
- SPARQL data-product query access through a grlc proxy endpoint
- Runtime health and permissions-configuration endpoints

## API Specification Files

S5 uses one local API specification and one external GRLC specification source:

- `openapi.yaml` (OpenAPI 3.0.3)
  - This is the public S5 service contract.
  - It defines S5 endpoints for health, assets, versions, attachments, policies, access requests, configuration, and the RDF proxy endpoint `GET /pkms-api/{api_endpoint}`.
  - It also defines S5 authentication/authorization behavior (Bearer JWT and signed URL support).

- `perks-grlc` repository: <https://github.com/perks-project/perks-grlc>
  - This repository contains the grlc query specifications that define data-product query endpoints (for example `/procedures`, `/steps-of-procedure`, `/next-step`, and others).
  - It is the source for the SPARQL-backed query API surface that S5 forwards to through the RDF proxy.

In short:
- `openapi.yaml` = S5 gateway and governance contract
- `perks-grlc` repository = underlying query catalog source used by the gateway

### How They Work Together

`GET /pkms-api/{api_endpoint}` in `openapi.yaml` is a controlled proxy to the endpoint set defined in the `perks-grlc` repository.

Example mappings:
- `GET /pkms-api/procedures` -> forwards to the grlc `procedures` query endpoint
- `GET /pkms-api/steps-of-procedure` -> forwards to the grlc `steps-of-procedure` query endpoint

Before forwarding, S5 performs authentication and authorization checks, then passes query parameters through to the grlc layer.

### GRLC Methods (Summary by Tag)

The latest `perks-grlc` specifications expose query endpoints with explicit tags.
All GRLC methods are `GET` endpoints and are exposed through S5 via
`GET /pkms-api/{api_endpoint}`.

- `Procedure` (12 methods)
  - Core procedure knowledge queries (for example authors, targets, status, steps, expected duration, adoption, keyword filtering)
  - Examples: `GET /procedures-adopted-by`, `GET /procedure-target`, `GET /steps-of-procedure`

- `Versioning` (9 methods)
  - Asset version-chain and current-version queries
  - Examples: `GET /get-all-versions`, `GET /get-current-version`, `GET /analyze-version-position`

- `Access Control` (10 methods)
  - ODRL permission checks, policy retrieval, and access-request inspection
  - Examples: `GET /check-access-read`, `GET /get-policy`, `GET /get-access-requests-pending`

- `Reference Data` (10 methods)
  - Controlled vocabularies and catalog data for domain entities
  - Examples: `GET /machine-type`, `GET /tool`, `GET /energy`

- `Procedure Execution` (3 methods)
  - Queries over executed procedures and steps
  - Examples: `GET /execution-steps`, `GET /step-executedby-agent`, `GET /step-execution-start-end`

- `Assets` (2 methods)
  - Asset existence and classification helpers
  - Examples: `GET /check-asset-exists`, `GET /classify-asset`

- `Status` (1 method)
  - Status-transition history across versions
  - Example: `GET /get-status-changes`

Note: some endpoints are intentionally cross-tagged (for example `GET /get-current-versions-with-access` appears in both `Versioning` and `Access Control`, and `GET /get-status-changes` appears in both `Versioning` and `Status`).

## Server

- Local development server: `http://localhost:5000`

## Authentication

All endpoints except `/health` require authentication.

Supported mechanisms:
- Bearer JWT (`Authorization: Bearer <token>`) from Keycloak
- Signed URL (`?sig=...`) for URL-based authenticated access

Security schemes:
- `BearerAuth`: HTTP bearer token (JWT)
- `SignedURL`: API key in query parameter `sig`

## Common Path Parameters

- `asset_type`: asset category (for example `procedure`, `document`, `model`, `loto`, `rbac`)
- `asset_id`: unique asset identifier
- `attachment_id`: unique attachment identifier
- `request_id`: unique access request identifier
- `username`: target user for policy revocation
- `api_endpoint`: grlc endpoint path to proxy

## API Endpoints

### Health

- `GET /health`
  - Returns health information for service dependencies
  - No authentication required
  - Responses: `200`, `503`

### Assets

- `GET /store/{asset_type}`
  - Lists current versions of assets by type
  - Query params: `prefix`, `pattern`
  - Responses: `200`, `403`

- `GET /store/{asset_type}/list`
  - Lists assets with optional field/value filtering
  - Query params: `prefix`, `pattern`, `field`, `value`
  - Responses: `200`, `403`

- `GET /store/{asset_type}/{asset_id}`
  - Retrieves content directly or returns URL payload
  - Query params: `presigned_url`, `signed_url`
  - Responses: `200`, `400`, `403`, `404`

- `POST /store/{asset_type}/{asset_id}`
  - Creates or updates an asset
  - Supports `multipart/form-data`, `application/json`, and `application/octet-stream`
  - Optional headers: `x-solution-id`, `x-parent-id`
  - Responses: `200`, `201`, `400`, `403`

- `DELETE /store/{asset_type}/{asset_id}`
  - Deletes an asset
  - Responses: `200`, `403`, `404`

- `POST /store/{asset_type}/{asset_id}/update`
  - Updates one field using query parameters `field` and `value`
  - Optional headers: `x-solution-id`, `x-user-id`
  - Responses: `200`, `403`, `404`

### Asset Versions

- `GET /store/versions/{asset_type}/{asset_id}`
  - Returns metadata for all versions of an asset
  - Responses: `200`, `403`, `500`

### Attachments

- `POST /attachment/{asset_type}/{asset_id}/{attachment_id}`
  - Uploads an attachment file
  - Query param: `signed_url`
  - Responses: `200`, `400`, `403`

- `GET /attachment/{asset_type}/{asset_id}/{attachment_id}`
  - Downloads an attachment or returns URL payload
  - Query params: `presigned_url`, `signed_url`, `inline`
  - Responses: `200`, `400`, `403`, `404`

- `DELETE /attachment/{asset_type}/{asset_id}/{attachment_id}`
  - Deletes an attachment
  - Responses: `200`, `403`, `404`

### Policies

- `DELETE /store/{asset_type}/{asset_id}/policy/permission/{username}`
  - Revokes a specific user permission on a policy-restricted asset
  - Responses: `200`, `400`, `403`

### Access Requests

- `POST /store/{asset_type}/{asset_id}/access-request`
  - Creates an access request
  - Request body includes `action` and `motivation`
  - Responses: `201`, `400`, `403`

- `GET /store/{asset_type}/{asset_id}/access-request`
  - Lists access requests (optionally filtered by `status`)
  - Responses: `200`, `400`, `403`

- `POST /store/{asset_type}/{asset_id}/access-request/{request_id}/review`
  - Reviews an access request (`accept` or `reject`)
  - Responses: `200`, `400`, `403`

### RDF

- `GET /pkms-api/{api_endpoint}`
  - Proxies requests to the configured grlc API
  - `api_endpoint` values correspond to endpoint names defined in the `perks-grlc` repository
  - Forwards query parameters to SPARQL-backed endpoints after S5 auth checks
  - Responses: `200`, `403`, `500`

### Config

- `GET /api/config/permissions`
  - Returns the full runtime permissions configuration
  - Responses: `200`

## Shared Response Models

- `Error`: standard error payload (`error`, `message`, `status_code`, optional `requiredRoles`, `details`)
- `HealthStatus`: service health aggregate (`status`, `services`)
- `UrlResponse`: URL payload for asset/attachment retrieval (`url`, optional `signed_url`)
- `AssetListResponse`: list wrapper for returned assets
- `AccessRequestCreate` and `AccessRequestReview`: payload models for access workflow

## Notes

- Access-control failures return `403` and may include `requiredRoles`.
- For retrieval endpoints, `presigned_url` and `signed_url` are mutually exclusive.
- Signed URL authentication (`sig`) is supported in addition to bearer-token authentication.
