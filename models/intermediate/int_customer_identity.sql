with all_customers as (
    select * from {{ ref('stg_crm_customers') }}
    union all
    select * from {{ ref('stg_erp_customers') }}
),
ranked as (
    select *,
        coalesce(email, phone, source_system || ':' || source_customer_id) as identity_key,
        row_number() over (
            partition by coalesce(email, phone, source_system || ':' || source_customer_id)
            order by case source_system when 'CRM' then 1 else 2 end, updated_at desc
        ) as survivorship_rank
    from all_customers
)
select * from ranked
