# Malaysia Open Data Pipeline and Q&A Assistant

[![CI](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml)

A free-tool data engineering portfolio project: ingest public Malaysian open data, model it in a warehouse with tested dbt models, and answer plain-English questions over it with a read-only text-to-SQL assistant.

Status: **phase 2: Python ingestion of three official datasets, with a weekly scheduled run (first run due 2026-10-22).** See [PROGRESS.md](PROGRESS.md) and [PLAN.md](PLAN.md).

## What works today
- `ingestion/datagovmy.py` pulls datasets from the official data.gov.my APIs (OpenDOSM and Data Catalogue) into `data/raw/<dataset>/<date>.parquet`, with timeout, retry and backoff for the 4 requests/minute limit, and fails if a source drops a column the project depends on.
- Datasets: core CPI and monthly labour force (DOSM), weekly retail fuel prices (Ministry of Finance).
- A weekly GitHub Actions run ingests everything and keeps the Parquet as a build artifact.
- Offline unit tests (HTTP mocked) and GitHub Actions CI running ruff and pytest.

Data: DOSM and Ministry of Finance via data.gov.my, CC BY 4.0. Details in [docs/data_sources.md](docs/data_sources.md).

## How to run
```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use .venv/bin/activate on Linux/macOS
pip install -e ".[dev]"
python -m ingestion.datagovmy --all     # or name datasets: cpi_core lfs_month fuelprice
pytest
```

## Planned stack (all free)
Python, DuckDB + Parquet, dbt Core, one free-tier cloud warehouse, Ollama or a free LLM API tier, Streamlit, GitHub Actions.
