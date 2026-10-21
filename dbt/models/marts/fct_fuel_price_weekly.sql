with fuel as (
    select * from {{ ref('stg_fuelprice') }}
)

select
    effective_date,
    cast(lead(effective_date) over (order by effective_date) - interval 1 day as date) as valid_to,
    ron95_rm,
    ron97_rm,
    diesel_peninsular_rm,
    diesel_east_malaysia_rm,
    ron95_budi95_rm,
    ron95_skps_rm,
    diesel_budi_rm,
    diesel_skds_rm,
    round(ron95_rm - lag(ron95_rm) over (order by effective_date), 2) as ron95_change_rm,
    round(ron97_rm - lag(ron97_rm) over (order by effective_date), 2) as ron97_change_rm,
    round(diesel_peninsular_rm - lag(diesel_peninsular_rm) over (order by effective_date), 2)
        as diesel_peninsular_change_rm
from fuel
