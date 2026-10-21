# Progress log

Update this at the end of every working session: what was done, hours spent, what is next.

## Hours
Total spent: 4.5 / 200

## Log
- 2026-10-20: Folder and plan created. Next: phase 1, confirm the data source API and set up the repo.
- 2026-10-20 (1.5 h): Phase 1 done locally. git repo, pyproject, ruff + pytest, CI workflow; `ingestion/opendosm.py` pulls `cpi_core` (1,470 rows, 2018-01 to 2026-09) into Parquet with retry on 429. Licence confirmed CC BY 4.0. Re-planned: Airflow dropped, hours moved to cloud and AI (see PLAN.md decisions). Next: create the public GitHub repo, push, confirm CI green, fix the badge URL in README; then phase 2 (2 more datasets + GitHub Actions cron).
- 2026-10-21 (0.5 h): Published to https://github.com/florexong/malaysia-open-data-pipeline; package renamed to match; first CI run green. Repo link can now go on CV/LinkedIn as "in progress". Next: phase 2, add 2 more OpenDOSM datasets and a GitHub Actions cron run.
- 2026-10-21 (1 h): Phase 2 built; first scheduled run due Thu 2026-10-22 02:00 UTC (check the Actions tab, then mark done). Ingester generalised to `ingestion/datagovmy.py` (dataset registry, two APIs, required-column check, `--all`); added `lfs_month` (200 rows) and `fuelprice` (965 rows), both CC BY 4.0; fixed 301 redirect by using trailing-slash endpoints; weekly `ingest.yml` workflow uploads Parquet as artifact; 15 tests. Next: phase 3, DuckDB + dbt (raw/clean/mart) over the three datasets.
- 2026-10-21 (1.5 h): Phase 3 built. dbt-duckdb project in `dbt/`: Parquet sources with freshness on `_ingested_at`, 3 staging tables (latest snapshot, typed), 4 marts (`fct_cpi_core_monthly`, `fct_labour_force_monthly`, `fct_fuel_price_weekly`, `mart_monthly_economy` with day-weighted fuel averages), MCOICOP division seed from DOSM; 40 data tests incl. two custom generic tests, all passing; dbt docs generate. Workflow `ingest.yml` renamed `pipeline.yml`: ingest + dbt build + docs, artifacts kept 30 days; CI adds `dbt parse`. Sanity checks: Apr 2020 RON95 avg RM1.275 (COVID low), current RON95 RM4.62 / BUDI95 RM1.99. Next: check the first Pipeline run on GitHub is green (marks phases 2 and 3 done); then phase 4, pick the cloud by counting 30 KL/PJ job ads.
- 2026-10-21: First Pipeline run on GitHub green (ingest + dbt build + docs, https://github.com/florexong/malaysia-open-data-pipeline/actions/runs/39628977831); CI green. Phases 2 and 3 marked done. Next: phase 4, count which cloud (Azure / GCP / AWS) appears most in 30 KL/PJ data engineer job ads, then load the marts to that cloud's free tier with a budget alert.
