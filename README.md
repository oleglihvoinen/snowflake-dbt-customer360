# Snowflake + dbt Customer 360

Portfolio/reference implementation of a governed Customer 360 pipeline using Snowflake and dbt.

## Business problem
Customer records arrive from CRM and ERP with different identifiers, formats and quality. The pipeline standardizes source data, applies deterministic identity rules and publishes an analytics-ready golden customer model.

## Architecture
```text
CRM ─┐
     ├─> Snowflake RAW -> dbt staging -> identity resolution -> survivorship -> DIM_CUSTOMER
ERP ─┘
```

## Engineering highlights
- Source definitions and dbt tests
- Email, phone, country and business-key standardization
- Deterministic cross-source identity resolution
- Explicit source-priority survivorship
- Analytics-ready golden customer dimension
- Layered dbt model structure suitable for lineage/documentation

## Structure
```text
models/
├── sources.yml
├── staging/
│   ├── stg_crm_customers.sql
│   └── stg_erp_customers.sql
├── intermediate/
│   └── int_customer_identity.sql
└── marts/
    └── dim_customer.sql
```

Configure a Snowflake target named `customer360` and run `dbt build`.

This public project uses generic/synthetic structures and contains no employer or customer data.
