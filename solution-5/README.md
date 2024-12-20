# Solution 5 - API Docs

The following APIs are exposed by S5 via the `pkms-services` component: 
- Add or update of a procedure (body in RDF format). Turtle expected by default.
  ```
  POST /api/procedure/<procedure-id>?format=FORMAT
  ```
- Delete a procedure
  ```
  DELETE /api/procedure/<procedure-id>
  ```
- Get procedure
  ```
  GET /api/procedure/<procedure-id>
  ```

The API specification of the `pkms-grlc` component is provided by the file `pkms-grlc.json` as an OpenAPI specification.
