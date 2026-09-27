# Expected output

With the supplied synthetic CRM and ERP data, ACME and Nordic Parts each occur in both source systems. Their normalized email addresses allow the records to resolve to one identity. CRM wins the example survivorship ranking, while the ERP-only industrial customer remains a separate golden record.

Expected golden customer count: **4**.

The purpose is to make the matching and survivorship behavior easy to inspect during a code review or interview.
