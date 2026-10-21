with latest as (
    select *
    from {{ source('datagovmy', 'cpi_core') }}
    qualify _ingested_at = max(_ingested_at) over ()
)

select
    cast(date as date) as month,
    division as division_code,
    cast("index" as double) as cpi_index,
    _ingested_at
from latest
-- Division 02 (alcohol and tobacco) has no core CPI: its prices are government-administered.
where "index" is not null
