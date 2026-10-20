# Data sources

## OpenDOSM API (Department of Statistics Malaysia, via data.gov.my)
- Endpoint: `https://api.data.gov.my/opendosm?id=<dataset_id>` (no API key)
- Docs: https://developer.data.gov.my/static-api/opendosm
- Rate limit: 4 requests per minute per API; over the limit returns HTTP 429.
  The ingester makes one request per dataset and backs off on 429 / 5xx.
- Licence: Creative Commons Attribution 4.0 (CC BY 4.0). Attribution: Department of Statistics Malaysia (DOSM).

## Datasets in use

| Dataset id | Description | Frequency | Grain | Checked |
|------------|-------------|-----------|-------|---------|
| `cpi_core` | Core consumer price index (base 2010 = 100) | Monthly | month x division (`01`-`13`, `overall`) | 2026-10-20: 1,470 rows, 2018-01 to 2026-09 |

Catalogue page: https://open.dosm.gov.my/data-catalogue/cpi_core
