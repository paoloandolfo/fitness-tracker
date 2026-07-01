# fitness-tracker/config.py
import os
from dotenv import load_dotenv

load_dotenv()
load_env = load_dotenv

MARATHON_DATE = os.getenv("MARATHON_DATE", "2026-10-18")
PLAN_START_DATE = os.getenv("PLAN_START_DATE", "2026-07-01")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN", "")

WHOOP_CLIENT_ID = os.getenv("WHOOP_CLIENT_ID", "")
WHOOP_CLIENT_SECRET = os.getenv("WHOOP_CLIENT_SECRET", "")
WHOOP_REFRESH_TOKEN = os.getenv("WHOOP_REFRESH_TOKEN", "")

GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "credentials.json")

RECOVERY_RED_THRESHOLD = 33
RECOVERY_AMBER_THRESHOLD = 66
