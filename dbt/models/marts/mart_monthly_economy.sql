-- One row per month joining the three sources, for cross-dataset questions.
with cpi as (
    select month, cpi_index as core_cpi_index, yoy_pct_change as core_cpi_yoy_pct_change
    from {{ ref('fct_cpi_core_monthly') }}
    where division_code = 'overall'
),

lfs as (
    select month, unemployment_rate_pct, labour_force_thousand, population_basis
    from {{ ref('fct_labour_force_monthly') }}
),

fuel as (
    select * from {{ ref('fct_fuel_price_weekly') }}
),

-- Expand each price to the days it was in effect, up to the end of the last full month.
fuel_days as (
    select
        cast(day.d as date) as day,
        fuel.ron95_rm,
        fuel.ron97_rm,
        fuel.diesel_peninsular_rm
    from fuel
    cross join unnest(generate_series(
        fuel.effective_date,
        least(
            coalesce(fuel.valid_to, current_date),
            cast(date_trunc('month', current_date) - interval 1 day as date)
        ),
        interval 1 day
    )) as day(d)
),

fuel_monthly as (
    select
        cast(date_trunc('month', day) as date) as month,
        round(avg(ron95_rm), 3) as avg_ron95_rm,
        round(avg(ron97_rm), 3) as avg_ron97_rm,
        round(avg(diesel_peninsular_rm), 3) as avg_diesel_peninsular_rm
    from fuel_days
    group by 1
)

select
    coalesce(cpi.month, lfs.month) as month,
    cpi.core_cpi_index,
    cpi.core_cpi_yoy_pct_change,
    lfs.unemployment_rate_pct,
    lfs.labour_force_thousand,
    lfs.population_basis,
    fuel_monthly.avg_ron95_rm,
    fuel_monthly.avg_ron97_rm,
    fuel_monthly.avg_diesel_peninsular_rm
from cpi
full outer join lfs
    on cpi.month = lfs.month
left join fuel_monthly
    on coalesce(cpi.month, lfs.month) = fuel_monthly.month
