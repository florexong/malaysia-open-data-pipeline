"""Pull datasets from the data.gov.my open APIs (OpenDOSM and Data Catalogue) into raw Parquet.

API docs: https://developer.data.gov.my/static-api/opendosm
Rate limit: 4 requests per minute per API, so one request per dataset and back off on 429.
"""

from __future__ import annotations

import argparse
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import requests

API_URLS = {
    "opendosm": "https://api.data.gov.my/opendosm/",
    "data-catalogue": "https://api.data.gov.my/data-catalogue/",
}
RETRY_STATUSES = {429, 500, 502, 503, 504}

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Dataset:
    id: str
    api: str
    required_columns: tuple[str, ...]


DATASETS = {
    d.id: d
    for d in [
        Dataset("cpi_core", "opendosm", ("date", "division", "index")),
        Dataset("lfs_month", "opendosm", ("date", "lf", "lf_employed", "lf_unemployed", "u_rate")),
        Dataset("fuelprice", "data-catalogue", ("date", "series_type", "ron95", "ron97", "diesel")),
    ]
}


def fetch_dataset(
    dataset_id: str,
    api: str = "opendosm",
    session: requests.Session | None = None,
    max_attempts: int = 3,
    backoff_seconds: float = 20.0,
    timeout: float = 30.0,
) -> list[dict]:
    """Return all records of a dataset, retrying on rate limits and server errors."""
    http = session or requests.Session()
    url = API_URLS[api]
    for attempt in range(1, max_attempts + 1):
        response = http.get(url, params={"id": dataset_id}, timeout=timeout)
        if response.status_code in RETRY_STATUSES and attempt < max_attempts:
            wait = backoff_seconds * 2 ** (attempt - 1)
            log.warning(
                "HTTP %s for %s, retry %s in %ss", response.status_code, dataset_id, attempt, wait
            )
            time.sleep(wait)
            continue
        response.raise_for_status()
        records = response.json()
        if not isinstance(records, list):
            raise ValueError(
                f"Expected a list of records for {dataset_id}, got {type(records).__name__}"
            )
        return records
    raise RuntimeError("unreachable")


def check_columns(records: list[dict], dataset: Dataset) -> None:
    """Fail loudly if the source schema lost a column we depend on."""
    seen = set().union(*(r.keys() for r in records)) if records else set()
    missing = [c for c in dataset.required_columns if c not in seen]
    if missing:
        raise ValueError(f"{dataset.id} is missing required columns: {missing}")


def to_parquet(records: list[dict], dataset_id: str, out_dir: Path | str = "data/raw") -> Path:
    """Write records to data/raw/<dataset_id>/<YYYY-MM-DD>.parquet with an ingestion timestamp."""
    if not records:
        raise ValueError(f"No records returned for {dataset_id}")
    ingested_at = datetime.now(UTC)
    df = pd.DataFrame.from_records(records)
    df["_ingested_at"] = ingested_at
    path = Path(out_dir) / dataset_id / f"{ingested_at:%Y-%m-%d}.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    return path


def ingest(dataset: Dataset, out_dir: Path | str = "data/raw") -> Path:
    records = fetch_dataset(dataset.id, api=dataset.api)
    check_columns(records, dataset)
    path = to_parquet(records, dataset.id, out_dir)
    log.info("Wrote %s rows to %s", len(records), path)
    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_ids", nargs="*", help=f"one or more of {sorted(DATASETS)}")
    parser.add_argument("--all", action="store_true", help="ingest every registered dataset")
    parser.add_argument("--out-dir", default="data/raw")
    args = parser.parse_args(argv)
    if args.all == bool(args.dataset_ids):
        parser.error("give dataset ids or --all, not both or neither")
    unknown = [d for d in args.dataset_ids if d not in DATASETS]
    if unknown:
        parser.error(f"unknown dataset(s) {unknown}; known: {sorted(DATASETS)}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    for dataset_id in sorted(DATASETS) if args.all else args.dataset_ids:
        ingest(DATASETS[dataset_id], args.out_dir)


if __name__ == "__main__":
    main()
