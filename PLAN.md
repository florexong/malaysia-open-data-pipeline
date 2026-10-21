# Plan: Malaysia Open Data Pipeline and Q&A Assistant

Goal: one finished, public GitHub project that proves hands-on cloud and an AI layer on top of a modern ELT pipeline, to close the gaps in my CV for Data/AI Engineer roles (hybrid KL/PJ or remote).

Budget: about 200 hours. At 10 h/week that is about 20 weeks; at 14 h/week about 14 weeks. Review after week 4 and cut scope instead of extending the deadline.

Rule: never trade job applications for this project. Apply to at least 5 roles a week regardless of progress.

## Phases

| # | Phase | Hours | Done when |
|---|-------|-------|-----------|
| 1 | Setup + Python ingestion | 10 | Repo, tests, CI green; OpenDOSM `cpi_core` lands in raw Parquet (done 2026-10-20) |
| 2 | Ingestion | 10 | 3 datasets total; scheduled run via GitHub Actions cron (no Airflow, see decisions) (done 2026-10-21) |
| 3 | Warehouse | 35 | DuckDB with raw / clean / mart layers; dbt models with tests and generated docs (done 2026-10-21) |
| 4 | Cloud | 40 | Marts loaded to one free-tier cloud warehouse, built hands-on (not design only); documented cost guard |
| 5 | AI layer | 70 | Read-only text-to-SQL assistant + RAG over dataset docs; 30-50 question test set with accuracy score |
| 6 | Polish | 35 | Data-quality checks, architecture diagram, README, demo, short write-up |

## CV and LinkedIn checkpoints
- After the repo is public with CI green: add the repo link to CV and LinkedIn (a working pipeline beats a perfect repo nobody sees).
- After phase 4: add "cloud warehouse" to the skills line, only if it is true.
- After phase 5: add the AI bullet with the measured accuracy number.

## Decisions made
- 2026-10-20: Drop Airflow. My work already shows Python and orchestration (dlt, dbt, Dagster) on client projects; the real CV gaps are hands-on cloud and AI. The freed hours go to phases 4 and 5. On the CV, name Dagster as the orchestration skill; do not claim Airflow.
- 2026-10-20: Data source is the OpenDOSM API (CC BY 4.0, 4 requests/minute). First dataset `cpi_core`.
- 2026-10-21: Datasets frozen at three: `cpi_core`, `lfs_month` (DOSM) and `fuelprice` (MoF, Data Catalogue API). Chosen for different grains (monthly by division, monthly national, weekly with two series types) to give the text-to-SQL assistant varied questions. Raw Parquet is a 30-day Actions artifact until phase 4.
- 2026-10-21: dbt models are tables, not views (relative Parquet paths would break views queried from outside `dbt/`). Custom generic tests instead of the dbt_utils package to avoid a dependency. Phases 2 and 3 used far fewer hours than budgeted; the spare goes to phases 4 and 5, not to more datasets.

## Decisions to make early
- Cloud: choose by counting which cloud appears most in 30 target job ads (Azure vs GCP vs AWS). Use only the free tier and set a budget alert.
- LLM: start with a local model through Ollama; fall back to a free API tier if the machine is too slow.

## Risks
- Scope creep: no new datasets after phase 3.
- Time: if behind at week 4, shrink phase 6 polish first; keep cloud (minimal but real) and the AI layer, since those are the CV gaps.
- Cost: never enter a payment method for a free tier without a budget alert.
