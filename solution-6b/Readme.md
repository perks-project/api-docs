
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

The file can either by provided via upload or via the key under which it is stored in SeaweedFS.
- **Endpoint:** `/api/faq/generate`
- **Method:** `POST`
- **Input Parameters:**
  - `useCase` (form data) ('Fagor','Siemens_EN', 'Siemens_DE')
  - `documentType` (form data) ('application/pdf')
  - `file` (file upload, omit if swid is used)
  - `swid` (SeaweedFS id, omit if file is used)
  - `document_id` (form data, optional)

- **Description:** Uploads a document for processing based on the specified use case.
- **Response:** JSON containing generation information and links for downloading extra files in addition to the same procedure using 'intermediate_download_url'.
  ```json
  {
    "message": "File uploaded successfully!",
    "generation_id": "UUID",
    "document_id": "Document ID if provided",
    "original_document_download_url": "URL to download the original document",
    "trace_download_url": "URL to download the trace file",
    "faq_download_url": "URL to download question-answer-pairs file",
  }
  ```

Please note that generation of question-answer-pairs runs asynchronously. The faq_download_url can be used to poll S6B until results are available. Results are also uploaded to SeaweeFS and can be retrieved from there when available using `qa/{generation_id}/faq` or just `qa/faq_seaweed_id` (latest results only).

## Get Trace Information
- **Endpoint:** `/api/faq/<generation_id>/trace`
- **Method:** `GET`
- **Description:** Retrieves the trace information for a given generation process.
- **Response:** JSON containing trace information.


## Media download
- **Endpoint:** `/api/download/media/<filename>`
- **Method:** `GET`
- **Description:** Download an image file from the server.
- **Response:** Image file stream.
