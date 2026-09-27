{% snapshot customer_snapshot %}
{{
    config(
      target_schema='SNAPSHOTS',
      unique_key='customer_key',
      strategy='check',
      check_cols=['customer_name', 'email', 'phone', 'country_code', 'surviving_source']
    )
}}
select * from {{ ref('dim_customer') }}
{% endsnapshot %}
