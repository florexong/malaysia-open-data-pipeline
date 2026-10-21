with cpi as (
    select * from {{ ref('stg_cpi_core') }}
)

select
    cur.month,
    cur.division_code,
    div.division_name_en,
    div.division_name_bm,
    cur.cpi_index,
    round(100 * (cur.cpi_index / prev_month.cpi_index - 1), 2) as mom_pct_change,
    round(100 * (cur.cpi_index / prev_year.cpi_index - 1), 2) as yoy_pct_change
from cpi as cur
left join {{ ref('mcoicop_divisions') }} as div
    on cur.division_code = div.division_code
left join cpi as prev_month
    on cur.division_code = prev_month.division_code
    and prev_month.month = cast(cur.month - interval 1 month as date)
left join cpi as prev_year
    on cur.division_code = prev_year.division_code
    and prev_year.month = cast(cur.month - interval 12 month as date)
