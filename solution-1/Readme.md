
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
- **Endpoint:** `/api/procedure/extract`
- **Method:** `POST`
- **Input Parameters:**
  - `useCase` (form data) ('Fagor','Beko')
  - `template` (form data) ('Yate Factory','Commission')
  - `file` (file upload)
  - `document_id` (form data)
  - `documentType` (form data, optional) ('application/pdf','application/zip')
- **Description:** Uploads a document for processing based on the specified use case and template.
- **Response:** JSON containing procedure information and links for downloading extra files in addition to the same procedure using 'intermediate_download_url'.
  ```json
  {
    "message": "Procedure Extracted successfully!/File uploaded successfully but extraction failed!" , // if file was uploaded but extraction failed
    "extraction_id": "UUID",
    "document_id": "Document ID if provided",
    "original_document_download_url": "URL to download the original document",
    "trace_download_url": "URL to download the trace file",
    "intermediate_download_url": "URL to download intermediate processing file/null",
    "procedure": "JSON containing Procedure Intermediate Representation (IR)/null",
  }
  ```


## Get Trace Information
- **Endpoint:** `/api/procedure/<extraction_id>/trace`
- **Method:** `GET`
- **Description:** Retrieves the trace information for a given extraction process.
- **Response:** JSON containing trace information.


## Media download
- **Endpoint:** `/api/download/imgs/<filename>`
- **Method:** `GET`
- **Description:** Download an image file from the server.
- **Response:** Image file stream.
