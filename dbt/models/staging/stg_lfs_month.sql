with latest as (
    select *
    from {{ source('datagovmy', 'lfs_month') }}
    qualify _ingested_at = max(_ingested_at) over ()
)

select
    cast(date as date) as month,
    cast(lf as double) as labour_force_thousand,
    cast(lf_employed as double) as employed_thousand,
    cast(lf_unemployed as double) as unemployed_thousand,
    cast(lf_outside as double) as outside_labour_force_thousand,
    cast(u_rate as double) as unemployment_rate_pct,
    cast(p_rate as double) as participation_rate_pct,
    cast(ep_ratio as double) as employment_population_ratio_pct,
    _ingested_at
from latest
