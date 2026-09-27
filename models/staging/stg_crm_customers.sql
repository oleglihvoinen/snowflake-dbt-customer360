select
    cast(customer_id as varchar) as source_customer_id,
    'CRM' as source_system,
    upper(trim(customer_name)) as customer_name,
    lower(trim(email)) as email,
    regexp_replace(phone, '[^0-9+]', '') as phone,
    upper(trim(country_code)) as country_code,
    updated_at
from {{ source('raw', 'crm_customers') }}
where customer_id is not null
