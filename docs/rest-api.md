# Customer 360 REST API

The API turns the governed dbt mart into a reusable data product for applications and AI consumers.

## Endpoints

- `GET /health` — service health
- `GET /api/v1/customers/{customer_key}` — golden customer
- `GET /api/v1/customers?email=...` — governed customer search
- `GET /api/v1/customers/{customer_key}/quality` — record-level quality summary

FastAPI generates OpenAPI documentation automatically. Snowflake credentials are read from environment variables rather than committed to Git.

## Why an API layer?

The REST interface provides a stable contract above physical warehouse tables. Consumers do not need Snowflake credentials or knowledge of the underlying dbt model structure. In production this layer can add OAuth/OIDC, authorization scopes, rate limiting, caching, observability and richer provenance.
