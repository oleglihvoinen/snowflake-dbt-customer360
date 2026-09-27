# Architecture

```text
CRM source -----+
                |
                +--> Snowflake RAW --> dbt staging --+
                |                                    |
ERP source -----+                                    v
                                            standardized identities
                                                     |
                                                     v
                                             identity resolution
                                                     |
                                              survivorship rules
                                                     |
                              +----------------------+------------------+
                              |                                         |
                              v                                         v
                        DIM_CUSTOMER                              dbt snapshot
                              |                                         |
                        BI / semantic / AI                    customer history
```

## Layer responsibilities

**RAW** preserves source-shaped data. **Staging** standardizes types and values without hiding source identity. **Intermediate** contains cross-source identity and survivorship logic. **Marts** expose governed consumer-facing entities. **Snapshots** retain change history.

The public implementation deliberately uses deterministic email/phone identity rules. A production MDM solution may add reference-data validation, fuzzy/probabilistic matching, stewardship queues and auditable overrides.
