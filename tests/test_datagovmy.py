from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from ingestion.datagovmy import (
    API_URLS,
    DATASETS,
    Dataset,
    check_columns,
    fetch_dataset,
    ingest,
    main,
    to_parquet,
)

SAMPLE = [
    {"date": "2020-05-01", "division": "overall", "index": 120.1},
    {"date": "2020-05-01", "division": "04", "index": 126.5},
]


def fake_response(status: int, payload=None) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.json.return_value = payload
    if status >= 400:
        response.raise_for_status.side_effect = requests.HTTPError(f"HTTP {status}")
    return response


def test_fetch_returns_records():
    session = MagicMock()
    session.get.return_value = fake_response(200, SAMPLE)

    assert fetch_dataset("cpi_core", session=session) == SAMPLE
    session.get.assert_called_once_with(
        API_URLS["opendosm"], params={"id": "cpi_core"}, timeout=30.0
    )


def test_fetch_uses_requested_api():
    session = MagicMock()
    session.get.return_value = fake_response(200, SAMPLE)

    fetch_dataset("fuelprice", api="data-catalogue", session=session)
    assert session.get.call_args.args[0] == API_URLS["data-catalogue"]


@patch("ingestion.datagovmy.time.sleep")
def test_fetch_retries_on_rate_limit(sleep):
    session = MagicMock()
    session.get.side_effect = [fake_response(429), fake_response(200, SAMPLE)]

    assert fetch_dataset("cpi_core", session=session, backoff_seconds=1) == SAMPLE
    assert session.get.call_count == 2
    sleep.assert_called_once_with(1)


@patch("ingestion.datagovmy.time.sleep")
def test_fetch_gives_up_after_max_attempts(sleep):
    session = MagicMock()
    session.get.return_value = fake_response(503)

    with pytest.raises(requests.HTTPError):
        fetch_dataset("cpi_core", session=session, max_attempts=3)
    assert session.get.call_count == 3


def test_fetch_rejects_non_list_payload():
    session = MagicMock()
    session.get.return_value = fake_response(200, {"error": "bad id"})

    with pytest.raises(ValueError):
        fetch_dataset("nope", session=session)


def test_check_columns_passes_when_present():
    check_columns(SAMPLE, DATASETS["cpi_core"])


def test_check_columns_names_missing_columns():
    dataset = Dataset("x", "opendosm", ("date", "u_rate"))
    with pytest.raises(ValueError, match="u_rate"):
        check_columns([{"date": "2020-01-01"}], dataset)


def test_registry_apis_are_known():
    assert {d.api for d in DATASETS.values()} <= set(API_URLS)


def test_to_parquet_round_trip(tmp_path):
    path = to_parquet(SAMPLE, "cpi_core", out_dir=tmp_path)

    assert path.parent == tmp_path / "cpi_core"
    df = pd.read_parquet(path)
    assert len(df) == 2
    assert list(df.columns) == ["date", "division", "index", "_ingested_at"]
    assert df["_ingested_at"].notna().all()


def test_to_parquet_rejects_empty(tmp_path):
    with pytest.raises(ValueError):
        to_parquet([], "cpi_core", out_dir=tmp_path)


@patch("ingestion.datagovmy.fetch_dataset", return_value=SAMPLE)
def test_ingest_routes_to_dataset_api(fetch, tmp_path):
    path = ingest(DATASETS["cpi_core"], out_dir=tmp_path)

    fetch.assert_called_once_with("cpi_core", api="opendosm")
    assert path.exists()


@patch("ingestion.datagovmy.ingest")
def test_main_all_ingests_every_dataset(ingest_mock, tmp_path):
    main(["--all", "--out-dir", str(tmp_path)])

    assert sorted(c.args[0].id for c in ingest_mock.call_args_list) == sorted(DATASETS)


@pytest.mark.parametrize("argv", [[], ["--all", "cpi_core"], ["not_a_dataset"]])
def test_main_rejects_bad_arguments(argv):
    with pytest.raises(SystemExit):
        main(argv)
