with lfs as (
    select * from {{ ref('stg_lfs_month') }}
)

select
    cur.month,
    cur.labour_force_thousand,
    cur.employed_thousand,
    cur.unemployed_thousand,
    cur.outside_labour_force_thousand,
    cur.unemployment_rate_pct,
    cur.participation_rate_pct,
    cur.employment_population_ratio_pct,
    round(cur.unemployment_rate_pct - prev_year.unemployment_rate_pct, 2) as unemployment_rate_yoy_pp_change,
    -- DOSM reweighted the survey to the 2020 Census from 2025, so the series has a break there.
    case when cur.month >= date '2025-01-01' then 'census_2020' else 'census_2010' end as population_basis
from lfs as cur
left join lfs as prev_year
    on prev_year.month = cast(cur.month - interval 12 month as date)
