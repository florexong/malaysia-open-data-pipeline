with latest as (
    select *
    from {{ source('datagovmy', 'fuelprice') }}
    qualify _ingested_at = max(_ingested_at) over ()
)

-- Keep price levels only; week-on-week changes are recomputed in the mart.
select
    cast(date as date) as effective_date,
    cast(ron95 as double) as ron95_rm,
    cast(ron97 as double) as ron97_rm,
    cast(diesel as double) as diesel_peninsular_rm,
    cast(diesel_eastmsia as double) as diesel_east_malaysia_rm,
    cast(ron95_budi95 as double) as ron95_budi95_rm,
    cast(ron95_skps as double) as ron95_skps_rm,
    cast(diesel_budi as double) as diesel_budi_rm,
    cast(diesel_skds as double) as diesel_skds_rm,
    _ingested_at
from latest
where series_type = 'level'
