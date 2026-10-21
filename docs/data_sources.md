# Data sources

All data comes from the official data.gov.my open APIs. No API key is needed.

| API | Endpoint |
|-----|----------|
| OpenDOSM (Department of Statistics Malaysia) | `https://api.data.gov.my/opendosm/?id=<dataset_id>` |
| Data Catalogue (data.gov.my) | `https://api.data.gov.my/data-catalogue/?id=<dataset_id>` |

- Docs: https://developer.data.gov.my/static-api/opendosm
- The endpoints without a trailing slash answer with a 301 redirect, so the ingester uses the slash form.
- Rate limit: 4 requests per minute per API; over the limit returns HTTP 429.
  The ingester makes one request per dataset and backs off on 429 / 5xx.
- Licence: every dataset below is Creative Commons Attribution 4.0 (CC BY 4.0).

## Datasets in use

| Dataset id | API | Source | Description | Frequency | Grain | Checked 2026-10-21 |
|------------|-----|--------|-------------|-----------|-------|--------------------|
| `cpi_core` | OpenDOSM | DOSM | Core consumer price index (base 2010 = 100) | Monthly | month x division (`01`-`13`, `overall`) | 1,470 rows, 2018-01 to 2026-09 |
| `lfs_month` | OpenDOSM | DOSM, Labour Force Survey | Labour force, employed, unemployed, outside labour force (thousands of persons); unemployment, participation and employment-population rates | Monthly | month | 200 rows, 2010-01 to 2026-08 |
| `fuelprice` | Data Catalogue | Ministry of Finance | Retail fuel prices per litre in RM (RON95, RON97, diesel Peninsular and East Malaysia, subsidised RON95 variants) | Weekly | week x `series_type` (`level` = price, `change_weekly` = week-on-week change) | 965 rows, 2017-03-30 to 2026-10-15 |

Catalogue pages:
- https://open.dosm.gov.my/data-catalogue/cpi_core
- https://open.dosm.gov.my/data-catalogue/lfs_month
- https://data.gov.my/data-catalogue/fuelprice

## Notes for modelling (phase 3)
- `lfs_month`: rates such as `u_rate` are stored as percentages (e.g. `3.5`), not 0-1 ratios. Data before 2025 is weighted to the 2010 Census and from 2025 to the 2020 Census, so expect a break in the series.
- `fuelprice`: each date has two rows, one per `series_type`; filter to `level` for prices. Subsidy columns (`ron95_budi95`, `ron95_skps`, `diesel_budi`, `diesel_skds`) are null before their schemes started.
- `cpi_core`: core CPI is not computed for division `02` (alcoholic beverages and tobacco), whose prices are government-administered.

## Schedule
`.github/workflows/ingest.yml` runs every Thursday 02:00 UTC (after the Wednesday fuel price update) and on demand. It keeps the raw Parquet as a 30-day build artifact until the cloud phase gives it a permanent home. GitHub pauses scheduled workflows after 60 days with no repository activity, and emails the repository owner when a scheduled run fails.
