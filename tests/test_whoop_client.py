import pytest
from unittest.mock import patch, MagicMock
from whoop_client import WhoopClient


def _mock_token_response():
    mock = MagicMock()
    mock.json.return_value = {"access_token": "tok", "refresh_token": "ref"}
    mock.raise_for_status = MagicMock()
    return mock


def _mock_recovery_response():
    mock = MagicMock()
    mock.json.return_value = {"records": [{
        "created_at": "2026-06-15T08:00:00Z",
        "score": {"recovery_score": 72, "hrv_rmssd_milli": 58.3, "resting_heart_rate": 52},
        "sleep": {"total_in_bed_time_milli": 27000000}
    }]}
    mock.raise_for_status = MagicMock()
    return mock


def test_get_recovery_returns_list():
    with patch("whoop_client.requests.post", return_value=_mock_token_response()), \
         patch("whoop_client.requests.get", return_value=_mock_recovery_response()):
        client = WhoopClient("id", "secret", "refresh")
        records = client.get_recovery("2026-06-01", "2026-06-30")

    assert len(records) == 1
    assert records[0]["recovery_score"] == 72
    assert records[0]["hrv_ms"] == 58.3
    assert records[0]["resting_hr"] == 52
    assert records[0]["sleep_hours"] == pytest.approx(7.5, rel=0.01)


def test_get_recovery_returns_empty_on_api_error():
    error_mock = MagicMock()
    error_mock.raise_for_status.side_effect = Exception("API error")

    with patch("whoop_client.requests.post", return_value=_mock_token_response()), \
         patch("whoop_client.requests.get", return_value=error_mock):
        client = WhoopClient("id", "secret", "refresh")
        records = client.get_recovery("2026-06-01", "2026-06-30")

    assert records == []
