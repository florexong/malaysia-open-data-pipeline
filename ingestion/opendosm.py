"""Pull a dataset from the OpenDOSM API (data.gov.my) into raw Parquet.

API docs: https://developer.data.gov.my/static-api/opendosm
Rate limit: 4 requests per minute, so one request per dataset and back off on 429.
"""

from __future__ import annotations

import argparse
import logging
import time
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.data.gov.my/opendosm"
RETRY_STATUSES = {429, 500, 502, 503, 504}

log = logging.getLogger(__name__)


def fetch_dataset(
    dataset_id: str,
    session: requests.Session | None = None,
    max_attempts: int = 3,
    backoff_seconds: float = 20.0,
    timeout: float = 30.0,
) -> list[dict]:
    """Return all records of an OpenDOSM dataset, retrying on rate limits and server errors."""
    http = session or requests.Session()
    for attempt in range(1, max_attempts + 1):
        response = http.get(BASE_URL, params={"id": dataset_id}, timeout=timeout)
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_id", help="OpenDOSM dataset id, e.g. cpi_core")
    parser.add_argument("--out-dir", default="data/raw")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    records = fetch_dataset(args.dataset_id)
    path = to_parquet(records, args.dataset_id, args.out_dir)
    log.info("Wrote %s rows to %s", len(records), path)


if __name__ == "__main__":
    main()
