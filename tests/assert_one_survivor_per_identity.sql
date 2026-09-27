select identity_key
from {{ ref('int_customer_identity') }}
where survivorship_rank = 1
group by identity_key
having count(*) <> 1
