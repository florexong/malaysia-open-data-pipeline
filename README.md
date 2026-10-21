# Malaysia Open Data Pipeline and Q&A Assistant

[![CI](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/florexong/malaysia-open-data-pipeline/actions/workflows/ci.yml)

A free-tool data engineering portfolio project: ingest public Malaysian open data, model it in a warehouse with tested dbt models, and answer plain-English questions over it with a read-only text-to-SQL assistant.

Status: **phase 1, Python ingestion of OpenDOSM core CPI.** See [PROGRESS.md](PROGRESS.md) and [PLAN.md](PLAN.md).

## What works today
- `ingestion/opendosm.py` pulls a dataset from the official OpenDOSM API into `data/raw/<dataset>/<date>.parquet`, with timeout, retry and backoff for the API's 4 requests/minute limit.
- Offline unit tests (HTTP mocked) and GitHub Actions CI running ruff and pytest.

Data: Department of Statistics Malaysia, CC BY 4.0. Details in [docs/data_sources.md](docs/data_sources.md).

## How to run
```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use .venv/bin/activate on Linux/macOS
pip install -e ".[dev]"
python -m ingestion.opendosm cpi_core
pytest
```

## Planned stack (all free)
Python, DuckDB + Parquet, dbt Core, one free-tier cloud warehouse, Ollama or a free LLM API tier, Streamlit, GitHub Actions.
