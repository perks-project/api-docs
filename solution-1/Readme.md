# API Documentation

## API Check

- **Endpoint:** `/api`
- **Method:** `GET`
- **Description:** Check if the API is working.
- **Response:**
  ```json
  {
    "message": "API is working!"
  }
  ```

## Extract Procedure Intermediate Representation (IR) from a file

The file can either be provided via upload or via the key under which it is stored in SeaweedFS.

- **Endpoint:** `/api/procedure/extract`
- **Method:** `POST`
- **Input Parameters:**
    - `useCase` (form data) ('Fagor', 'Beko')
    - `template` (form data) ('Yate Factory' or 'Other' for Beko use case, 'Commission' and 'Manuals'
      for Fagor use case)
    - `mode` (form data) (for 'Beko' use case only, 'heuristic' for heuristic pipeline, 'llm' for
      llm-based pipeline)
    - `documentType` (form data) ('application/pdf', 'application/xlsx', 'application/zip', 'text/plain', 'text/markdown')
    - `file` (file upload, omit if swid is used)
    - `swid` (SeaweedFS id, omit if file is used)
    - `document_id` (form data, optional)

- **Description:** Uploads a document for procedure extraction based on the specified use case and
  template.
- **Response:** JSON containing extraction_id and links for downloading related files as well as job
  management URLs OR HTTP status 503 if a previous job is still running.
  ```json
  {
    "message": "File uploaded successfully!",
    "extraction_id": "UUID",
    "document_id": "Document ID if provided",
    "original_document_download_url": "URL to download the original document",
    "trace_download_url": "URL to download the trace file when job is finished",
    "intermediate_download_url": "URL to download intermediate processing file when job is finished",
    "job_status_url": "URL to query job status",
    "job_cancel_url": "URL to cancel job"
  }
  ```

Note that procedure extraction runs asynchronously. Use `job_status_url` to get the job's current
status. Use `job_cancel_url` to cancel the job. When job status is `finished` use
`intermediate_download_url` to retrieve procedure from S1. As an alternative, the procedure can also
be retrieved from SeaweedFS using `s1/<extraction_id>/intermediate-json` as key.

## Get Job Status

- **Endpoint:** `/api/procedure/<extraction_id>/status`
- **Method:** `GET`
- **Description:** Retrieves the job status for a given extraction process.
- **Response:** JSON containing job status.
  ```json
  {
    "job": "<extraction_id>",
    "status": "either 'running', 'finished', 'canceled' or 'unknown' if there is no job with given extraction id"
  }
  ```

## Cancel Job

- **Endpoint:** `/api/procedure/<extraction_id>/cancel`
- **Method:** `GET`
- **Description:** Cancels the job for a given extraction process.
- **Response:** JSON containing job status.
  ```json
  {
    "job": "<extraction_id>",
    "status": "either 'canceled' if successful canceled or 'unknown' if there is no job with given extraction id"
  }
  ```

## Get Trace Information

- **Endpoint:** `/api/procedure/<extraction_id>/trace`
- **Method:** `GET`
- **Description:** Retrieves the trace information for a given extraction process.
- **Response:** JSON containing trace information.
  ```json
  {
    "static": "static trace information",
    "dynamic": "dynamic trace information",
    "errors": "list of errors that have occurred during extraction, should be empty"
  }
  ```

## Validated Procedure Notification

- **Endpoint:** `/api/procedure/validate`
- **Method:** `POST`
- **Payload:** JSON containing procedure id and type (e.g. loto), used to create SeaweedFS key
  `<type>/<id>`
  ```json
  {
    "id": "id",
    "type": "type"
  }
  ```
- **Description:** Notify S1 that a new validated procedure is available for download from
  SeaweedFS.
- **Response:** JSON containing HTML response code, 200 for success, 400 for error

## Generating Custom Procedure from General Procedure and Parameters

The general procedure file and the parameter file can either be provided via upload or via the key
under which they are stored in SeaweedFS.

- **Endpoint:** `/api/procedure/instantiate`
- **Method:** `POST`
- **Input Parameters:**
    - `useCase` (form data) (currently, only 'Fagor' is supported)
    - `procedureFile` (form data) (file upload of general procedure, omit if procedureSwid is used)
    - `procedureSwid` (form data) (SeaweedFS id of the general procedure, omit if procedureFile is
      used)
    - `file` (form data) (file upload of parameters, omit if swid is used)
    - `swid` (form data) (SeaweedFS id of parameters, omit if file is used)

- **Description:** Creates a custom procedure from general procedure and parameters.
- **Response:** JSON containing custom procedure.
