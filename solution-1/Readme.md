
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


## Validated Procedure Notification
- **Endpoint:** `/api/procedure/validate`
- **Method:** `POST`
- **Payload:** JSON containing procedure id and type (e.g. loto), used to create SeaweedFS key `<type>/<id>`
  ```json
  {
    "id": <id>,
    "type": <type>
  }
  ```
- **Description:** Notify S1 that a new validated procedure is available for download from SeaweedFS.
- **Response:** JSON containing HTML response code, 200 for success, 400 for error


## Generating Fagor Custom Procedure from General Procedure and Parameters

The general procedure file and the parameter file can either by provided via upload or via the key under which it is stored in SeaweedFS.
- **Endpoint:** `/api/procedure/instantiate`
- **Method:** `POST`
- **Input Parameters:**
  - `useCase` (form data) (currently, only 'Fagor' is supported)
  - `procedureFile` (file upload of general procedure, omit if procedureSwid is used)
  - `procedureSwid ` (SeaweedFS id of the general procedure, omit if procedureFile is used)
  - `file` (file upload of parameters, omit if swid is used)
  - `swid` (SeaweedFS id of parameters, omit if file is used)

- **Description:** Creates a custom procedure from general procedure and parameters.
- **Response:** JSON containing custom procedure.
