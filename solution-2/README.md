# Solution 2 - API Docs

The following APIs are exposed by S2: 
- Acceptance of updates (JSON format) for procedures
  ```
  POST /store/<asset-type>/<asset-id>
  ```
- Acceptance of status updates for procedures
  ```
  POST /store/<asset-type>/<asset-id>/update?field=status&value=STATUS_VALUE
  ```

Asset Types accepted are: `document`, `loto`, `commissioning-guide`, `commissioning-procedure`, `microgrid`

Status Values accepted are: `Draft`, `Validation`, `Approval`, `Approved`
