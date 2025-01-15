# Solution 2 - API Docs

The following APIs are exposed by S2: 
- Acceptance of updates (JSON format) for draft procedures
  ```
  POST /api/procedure/<procedure-id>
  ```
- Acceptance of status updates for draft procedures
  ```
  POST /api/procedure/<procedure-id>/update?field=status&value=STATUS_VALUE
  ```

  Status Values accepted are: Draft, Approved
