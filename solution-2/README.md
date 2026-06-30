# Solution 2 - API Docs

This folder documents the API exposed by PERKS Solution 2 (S2), the backend service for manual and semi-automatic procedural knowledge authoring and refinement.

S2 supports:
- Collection and refinement of procedures through JSON-based intermediate representations
- RDF lifting and validation against PKO-compatible schemas
- Asynchronous extraction and FAQ generation workflows
- Integration with PKMS storage and downstream semantic services

## OpenAPI Source

The canonical API contract is defined in `openapi.yaml` (OpenAPI 3.0.3).

## Authentication

All endpoints require a Bearer JWT (`Authorization: Bearer <token>`) issued by Keycloak.

Security scheme:
- Type: `http`
- Scheme: `bearer`
- Bearer format: `JWT`

## Common Path Parameters

- `asset_type`: asset category (for example `procedure`, `document`, `model`, `loto`, `rbac`)
- `asset_id`: unique asset identifier
- `job_id`: asynchronous workflow job identifier

## API Endpoints

### Assets

- `GET /store/processed/{asset_type}/{asset_id}`
  - Retrieves processed/enriched asset content or a URL to it
  - Query params: `presigned_url` (bool), `signed_url` (bool)
  - Returns JSON URL payload or binary content
  - Responses: `200`, `400`, `403`, `404`

### RDF

- `POST /lifting/{asset_type}`
  - Validates and lifts provided JSON payload to RDF
  - Query param: `enrich` (bool)
  - `Accept` header controls serialization (`text/turtle`, `application/ld+json`, `application/rdf+xml`)
  - Responses: `200`, `400`, `500`

- `GET /lifting/{asset_type}/{asset_id}`
  - Loads a stored asset and performs RDF lifting
  - Query param: `enrich` (bool)
  - `Accept` header controls serialization
  - Responses: `200`, `403`, `404`, `500`

- `POST /validate/{asset_type}`
  - Validates JSON data against the schema for the selected asset type
  - Responses: `200`, `400`, `403`

### Extraction Workflow

- `POST /extract`
  - Starts asynchronous extraction for an asset
  - Request body: `{ "type": "...", "id": "..." }`
  - Returns local `job_id` and external extraction metadata
  - Responses: `202`, `400`, `403`

- `GET /extract/{job_id}/status`
  - Retrieves extraction status (`queued`, `running`, `finished`, `failed`, `canceled`, `unknown`)
  - Responses: `200`, `403`, `404`

- `POST /extract/{job_id}/cancel`
  - Requests extraction cancellation
  - Responses: `200`, `403`, `404`

- `GET /extract/{job_id}/trace`
  - Retrieves extraction execution trace/events
  - Responses: `200`, `403`, `404`

### FAQ Generation Workflow

- `POST /faq/generate`
  - Starts asynchronous FAQ generation
  - Request body fields include `useCase`, `documentType`, `references`, `resourceType`
  - Responses: `202`, `400`, `403`

- `GET /faq/{job_id}/status`
  - Retrieves FAQ generation status
  - Responses: `200`, `403`, `404`

- `POST /faq/{job_id}/cancel`
  - Requests FAQ generation cancellation
  - Responses: `200`, `403`, `404`

- `GET /faq/{job_id}/trace`
  - Retrieves FAQ generation trace/events
  - Responses: `200`, `403`, `404`

### Approval

- `POST /approve`
  - Submits an existing asset/procedure for approval
  - Request body: `{ "type": "...", "id": "..." }`
  - Responses: `200`, `400`, `403`

## Shared Response Models

- `Error`: standard error payload (`error`, `message`, `status_code`, optional `requiredRoles`, `details`)
- `UrlResponse`: URL payload for processed assets (`url`, optional `signed_url`)
- `ExtractionJobStatus` and `FaqJobStatus`: asynchronous state tracking with timestamps and last error
- `ExtractionJobTrace` and `FaqJobTrace`: event-level execution trace payloads

## Notes

- Access control failures return `403` and may include `requiredRoles`.
- `signed_url` and `presigned_url` retrieval options are mutually exclusive for processed asset retrieval.
- S2 integrates with S1 (extraction) and S6B (FAQ generation) as external asynchronous services.
