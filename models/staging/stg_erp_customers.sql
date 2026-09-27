select
    cast(account_id as varchar) as source_customer_id,
    'ERP' as source_system,
    upper(trim(account_name)) as customer_name,
    lower(trim(contact_email)) as email,
    regexp_replace(contact_phone, '[^0-9+]', '') as phone,
    upper(trim(country)) as country_code,
    modified_at as updated_at
from {{ source('raw', 'erp_customers') }}
where account_id is not null
