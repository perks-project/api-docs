
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

## Generate Question-Answer-Pairs from a file

The file can either be provided via upload or via the key under which it is stored in SeaweedFS.

- **Endpoint:** `/api/faq/generate`
- **Method:** `POST`
- **Input Parameters:**
    - `useCase` (form data) ('Fagor', 'Siemens_EN', 'Siemens_DE')
    - `documentType` (form data) ('application/pdf')
    - `file` (file upload, omit if swid is used)
    - `swid` (SeaweedFS id, omit if file is used)
    - `document_id` (form data, optional)

- **Description:** Uploads a document for question-answer-pair generation based on the specified use
  case.
- **Response:** JSON containing generation id and links for downloading related files as well as job
  management URLs OR HTTP status 503 if a previous job is still running.
  ```json
  {
    "message": "File uploaded successfully!",
    "generation_id": "UUID",
    "document_id": "Document ID if provided",
    "original_document_download_url": "URL to download the original document",
    "trace_download_url": "URL to download the trace file when job is finished",
    "faq_download_url": "URL to download question-answer-pairs file when job is finished",
    "job_status_url": "URL to query job status",
    "job_cancel_url": "URL to cancel job"
  }
  ```

Note that generation of question-answer-pairs runs asynchronously. Use `job_status_url` to get the
job's current status. Use `job_cancel_url` to cancel the job. When job status is `finished` use
`faq_download_url` to retrieve question-answer-pairs from S6B. As an alternative, the qa-pairs can
also be retrieved from SeaweedFS using `qa/<generation_id>/faq` as key.

## Get Job Status

- **Endpoint:** `/api/faq/<generation_id>/status`
- **Method:** `GET`
- **Description:** Retrieves the job status for a given generation process.
- **Response:** JSON containing job status.
  ```json
  {
    "job": "<generation_id>",
    "status": "either 'running', 'finished', 'canceled' or 'unknown' if there is no job with given generation id"
  }
  ```

## Cancel Job

- **Endpoint:** `/api/faq/<generation_id>/cancel`
- **Method:** `GET`
- **Description:** Cancels the job for a given generation process.
- **Response:** JSON containing job status.
  ```json
  {
    "job": "<generation_id>",
    "status": "either 'canceled' if successful canceled or 'unknown' if there is no job with given generation id"
  }
  ```

## Get Trace Information
- **Endpoint:** `/api/faq/<generation_id>/trace`
- **Method:** `GET`
- **Description:** Retrieves the trace information for a given generation process.
- **Response:** JSON containing trace information.
  ```json
  {
    "static": "static trace information",
    "dynamic": "dynamic trace information",
    "errors": "list of errors that have occurred during generation, should be empty"
  }
  ```
