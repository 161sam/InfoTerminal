# API Versioning

The gateway adds an `X-API-Version: v1` header to responses.
Plugin manifests and the `/plugins/tools` endpoint also report their `apiVersion`.
Clients should use these values to ensure compatibility as new versions roll out.
