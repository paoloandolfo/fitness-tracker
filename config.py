import os
import json
import tempfile
from dotenv import load_dotenv

try:
    import streamlit as st
    _secrets = st.secrets
except Exception:
    _secrets = {}

load_dotenv()
load_env = load_dotenv  # callable alias required by downstream modules


def _get(key: str, default: str = "") -> str:
    try:
        val = _secrets.get(key, None)
    except Exception:
        val = None
    if val is None:
        val = os.getenv(key, default)
    return str(val)


def get_credentials_path() -> str:
    try:
        if "gcp_service_account" in _secrets:
            tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
            json.dump(dict(_secrets["gcp_service_account"]), tmp)
            tmp.flush()
            return tmp.name
    except Exception:
        pass
    raw = _get("GOOGLE_CREDENTIALS_JSON")
    if raw and raw.startswith("{"):
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(json.loads(raw), tmp)
        tmp.flush()
        return tmp.name
    return raw or "credentials.json"


MARATHON_DATE = _get("MARATHON_DATE", "2026-10-18")
PLAN_START_DATE = _get("PLAN_START_DATE", "2026-07-01")
SPREADSHEET_ID = _get("SPREADSHEET_ID", "")
STRAVA_CLIENT_ID = _get("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = _get("STRAVA_CLIENT_SECRET", "")
STRAVA_REFRESH_TOKEN = _get("STRAVA_REFRESH_TOKEN", "")
WHOOP_CLIENT_ID = _get("WHOOP_CLIENT_ID", "")
WHOOP_CLIENT_SECRET = _get("WHOOP_CLIENT_SECRET", "")
WHOOP_REFRESH_TOKEN = _get("WHOOP_REFRESH_TOKEN", "")
GOOGLE_CREDENTIALS_JSON = get_credentials_path()
RECOVERY_RED_THRESHOLD = 33
RECOVERY_AMBER_THRESHOLD = 66
