# Progress log

Update this at the end of every working session: what was done, hours spent, what is next.

## Hours
Total spent: 1.5 / 200

## Log
- 2026-10-20: Folder and plan created. Next: phase 1, confirm the data source API and set up the repo.
- 2026-10-20 (1.5 h): Phase 1 done locally. git repo, pyproject, ruff + pytest, CI workflow; `ingestion/opendosm.py` pulls `cpi_core` (1,470 rows, 2018-01 to 2026-09) into Parquet with retry on 429. Licence confirmed CC BY 4.0. Re-planned: Airflow dropped, hours moved to cloud and AI (see PLAN.md decisions). Next: create the public GitHub repo, push, confirm CI green, fix the badge URL in README; then phase 2 (2 more datasets + GitHub Actions cron).
