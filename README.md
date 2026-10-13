# Snowflake + dbt Customer 360

A governed **Customer 360 / MDM data product** combining Snowflake/dbt transformations with explainable entity resolution, field-level survivorship, stewardship exceptions and API delivery.

## Architecture

```text
CRM ─┐
     ├─> Snowflake RAW -> dbt staging -> identity candidates
ERP ─┘                                     |
                                            +-> deterministic/fuzzy evidence
                                            +-> conflict detection
                                            +-> stewardship queue
                                            |
                                            v
                                   field-level survivorship
                                            |
                                            v
                                      DIM_CUSTOMER
                                            |
                                  BI / APIs / governed AI
```

## Implemented engineering depth

- source-specific staging and normalization
- dbt source declarations, tests, snapshots and golden customer mart
- explainable cross-system entity-resolution engine
- exact-email / exact-phone and name-similarity evidence
- explicit auto-match, review and reject decisions
- protection against merging records with conflicting strong identifiers
- transitive entity clustering
- field-level survivorship rather than whole-record winner-takes-all
- field provenance showing which source supplied each surviving attribute
- stewardship exception queue for ambiguous candidates
- YAML MDM policy defining thresholds and source priority
- automated Python tests for matching, conflict, survivorship and clustering
- CI validation for entity-resolution behavior
- FastAPI data-product boundary and Docker packaging

## MDM policy

`config/mdm_policy.yml` makes the matching and survivorship policy explicit instead of hiding it in application code. Ambiguous matches can be routed to stewardship rather than silently merged.

The public data and rules are synthetic and contain no employer/customer data.

## Run entity-resolution tests

```bash
python -m pip install pytest
pytest -q tests_python
```

For the dbt/Snowflake portion, configure `profiles.yml` and run `dbt build` / `dbt snapshot`.

**Technologies:** Snowflake · dbt · SQL · Python · MDM · entity resolution · survivorship · stewardship · data quality · FastAPI · Docker · CI/CD
