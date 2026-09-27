# Snowflake + dbt Customer 360

Portfolio/reference implementation of a governed Customer 360 pipeline using Snowflake and dbt.

## Business problem

Customer records arrive from CRM and ERP with different identifiers, formats and quality. The pipeline standardizes source data, resolves deterministic cross-system identities and publishes an analytics-ready golden customer model.

## Architecture

```text
CRM ─┐
     ├─> Snowflake RAW -> dbt staging -> identity resolution -> survivorship -> DIM_CUSTOMER
ERP ─┘                                                       |
                                                              +-> snapshot/history
```

See [docs/architecture.md](docs/architecture.md) for layer responsibilities and production extensions.

## Engineering highlights

- Snowflake database/schema bootstrap
- dbt source declarations and model tests
- CRM and ERP staging models
- Email, phone and country standardization
- Deterministic identity resolution
- Explicit source-priority survivorship
- Golden customer dimensional model
- Singular dbt business-rule test
- dbt snapshot for customer history
- Reusable normalization macro
- Environment-variable based profile example
- Synthetic sample data and documented expected result

## Repository structure

```text
.
├── dbt_project.yml
├── profiles.yml.example
├── snowflake/setup.sql
├── seeds/
├── macros/
├── models/
│   ├── sources.yml
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── snapshots/
├── tests/
└── docs/
```

## Running the project

1. Create the Snowflake database/schemas using `snowflake/setup.sql`.
2. Load the supplied synthetic CSV records into `CUSTOMER360.RAW.CRM_CUSTOMERS` and `CUSTOMER360.RAW.ERP_CUSTOMERS`. The files under `seeds/` are intentionally included as transparent sample source data; the models themselves read the RAW source tables.
3. Copy `profiles.yml.example` to your dbt profiles directory and provide the Snowflake environment variables.
4. Run:

```bash
dbt debug
dbt build
dbt snapshot
```

See [docs/expected-output.md](docs/expected-output.md) for the expected golden-record behavior.

## Production evolution

A real enterprise implementation would normally add fuzzy/probabilistic matching where required, reference-data validation, SCD2 strategy aligned to business history requirements, stewardship/exception workflows, source freshness SLAs, observability, role-based access and auditable manual overrides.

This public project uses generic synthetic structures and contains no employer or customer data.
