# Malaysia Open Data Pipeline and Q&A Assistant

[![CI](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml)
[![Pipeline](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/pipeline.yml/badge.svg)](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/pipeline.yml)

A free-tool data engineering portfolio project: ingest public Malaysian open data, model it in a warehouse with tested dbt models, and answer plain-English questions over it with a read-only text-to-SQL assistant.

Status: **phase 3: DuckDB warehouse with dbt models and tests over three official datasets.** See [PROGRESS.md](PROGRESS.md) and [PLAN.md](PLAN.md).

```
data.gov.my APIs ──> ingestion/datagovmy.py ──> data/raw/*.parquet ──> dbt (DuckDB) ──> staging ──> marts
 (OpenDOSM, Data       retry, rate limit,          one file per          sources read       typed,     facts + monthly
  Catalogue)           column checks               ingestion day         Parquet in place   latest     economy mart
```

## What works today
- **Ingestion:** `ingestion/datagovmy.py` pulls datasets from the official data.gov.my APIs (OpenDOSM and Data Catalogue) into `data/raw/<dataset>/<date>.parquet`, with timeout, retry and backoff for the 4 requests/minute limit, and fails if a source drops a column the project depends on.
- **Datasets:** core CPI and monthly labour force (DOSM), weekly retail fuel prices (Ministry of Finance).
- **Warehouse:** a dbt Core project on DuckDB (`dbt/`) with three layers: raw Parquet read in place as dbt sources, `staging` (typed, latest snapshot only), and `marts`. Plus a seed of CPI division names from the DOSM MCOICOP lookup. 40 data tests (not null, unique keys, relationships, accepted values, value ranges, two custom generic tests) and source freshness checks.
- **Marts:**
  - `fct_cpi_core_monthly`: core CPI by division and month, with month-on-month and year-on-year change
  - `fct_labour_force_monthly`: labour force and rates, year-on-year change, census basis flag
  - `fct_fuel_price_weekly`: fuel prices per announcement, validity range and change
  - `mart_monthly_economy`: one row per month joining all three; fuel prices are day-weighted monthly averages
- **Automation:** GitHub Actions CI (ruff, pytest with HTTP mocked, `dbt parse`) on every push. The Pipeline workflow ingests, runs `dbt build` and generates dbt docs weekly and on code changes, keeping the warehouse and docs as build artifacts.

Data: DOSM and Ministry of Finance via data.gov.my, CC BY 4.0. Details in [docs/data_sources.md](docs/data_sources.md).

## How to run
```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use .venv/bin/activate on Linux/macOS
pip install -e ".[dev,dbt]"
python -m ingestion.datagovmy --all     # or name datasets: cpi_core lfs_month fuelprice
pytest
cd dbt
dbt build                 # seeds, models and tests into ../data/warehouse.duckdb
dbt docs generate && dbt docs serve
```

## Planned stack (all free)
Python, DuckDB + Parquet, dbt Core, one free-tier cloud warehouse, Ollama or a free LLM API tier, Streamlit, GitHub Actions.
