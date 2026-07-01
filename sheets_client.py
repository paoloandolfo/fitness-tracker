# fitness-tracker/sheets_client.py
import gspread
from google.oauth2.service_account import Credentials
import config

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


class SheetsClient:
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        gc = gspread.authorize(creds)
        self._spreadsheet = gc.open_by_key(spreadsheet_id)

    def read_all(self, sheet_name: str) -> list[dict]:
        ws = self._spreadsheet.worksheet(sheet_name)
        return ws.get_all_records()

    def append_rows(self, sheet_name: str, rows: list[list]) -> None:
        ws = self._spreadsheet.worksheet(sheet_name)
        ws.append_rows(rows)

    def overwrite(self, sheet_name: str, headers: list[str], rows: list[list]) -> None:
        ws = self._spreadsheet.worksheet(sheet_name)
        ws.clear()
        ws.append_row(headers)
        if rows:
            ws.append_rows(rows)

    def get_value(self, sheet_name: str, key: str) -> str | None:
        ws = self._spreadsheet.worksheet(sheet_name)
        records = ws.get_all_records()
        for row in records:
            if row.get("key") == key:
                return str(row.get("value", ""))
        return None

    def set_value(self, sheet_name: str, key: str, value: str) -> None:
        ws = self._spreadsheet.worksheet(sheet_name)
        records = ws.get_all_records()
        for i, row in enumerate(records, start=2):
            if row.get("key") == key:
                ws.update(f"B{i}", [[value]])
                return
        ws.append_row([key, value])


def build_client() -> SheetsClient:
    return SheetsClient(config.GOOGLE_CREDENTIALS_JSON, config.SPREADSHEET_ID)
