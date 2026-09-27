select
    md5(identity_key) as customer_key,
    customer_name,
    email,
    phone,
    country_code,
    source_system as surviving_source,
    updated_at
from {{ ref('int_customer_identity') }}
where survivorship_rank = 1
