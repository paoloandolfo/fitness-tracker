# fitness-tracker/tests/test_sheets_client.py
from unittest.mock import MagicMock, patch
from sheets_client import SheetsClient


def _make_client():
    with patch("sheets_client.gspread.authorize"):
        with patch("sheets_client.Credentials.from_service_account_file"):
            return SheetsClient("credentials.json", "sheet-id")


def test_read_all_returns_list_of_dicts():
    client = _make_client()
    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = [
        {"date": "2026-06-15", "recovery_score": 72}
    ]
    client._spreadsheet.worksheet.return_value = mock_sheet

    result = client.read_all("recovery")

    assert result == [{"date": "2026-06-15", "recovery_score": 72}]


def test_append_rows_calls_worksheet():
    client = _make_client()
    mock_sheet = MagicMock()
    client._spreadsheet.worksheet.return_value = mock_sheet

    client.append_rows("activities", [["2026-06-15", "Run", 10.2]])

    mock_sheet.append_rows.assert_called_once_with([["2026-06-15", "Run", 10.2]])


def test_overwrite_clears_then_writes():
    client = _make_client()
    mock_sheet = MagicMock()
    client._spreadsheet.worksheet.return_value = mock_sheet

    client.overwrite("activities", ["date", "type", "distance_km"], [["2026-06-15", "Run", 10.2]])

    mock_sheet.clear.assert_called_once()
    mock_sheet.append_row.assert_called_once_with(["date", "type", "distance_km"])
    mock_sheet.append_rows.assert_called_once_with([["2026-06-15", "Run", 10.2]])


def test_get_value_returns_matching_key():
    client = _make_client()
    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = [
        {"key": "last_sync", "value": "2026-06-15"},
    ]
    client._spreadsheet.worksheet.return_value = mock_sheet

    result = client.get_value("metadata", "last_sync")

    assert result == "2026-06-15"


def test_get_value_returns_none_when_missing():
    client = _make_client()
    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = []
    client._spreadsheet.worksheet.return_value = mock_sheet

    result = client.get_value("metadata", "nonexistent_key")

    assert result is None
