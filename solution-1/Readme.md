
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

The file can either by provided via upload or via the key under which it is stored in SeaweedFS.
- **Endpoint:** `/api/procedure/extract`
- **Method:** `POST`
- **Input Parameters:**
  - `useCase` (form data) ('Fagor','Beko')
  - `template` (form data) ('Yate Factory' for Beko use case, 'Commission' and 'Manuals' for Fagor use case)
  - `documentType` (form data) ('application/pdf','application/zip')
  - `file` (file upload, omit if swid is used)
  - `swid` (SeaweedFS id, omit if file is used)
  - `document_id` (form data, optional)

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
- **Endpoint:** `/api/download/media/<filename>`
- **Method:** `GET`
- **Description:** Download an image file from the server.
- **Response:** Image file stream.
