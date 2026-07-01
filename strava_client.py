# fitness-tracker/strava_client.py
from datetime import datetime
from stravalib import Client
import config

TRACKED_TYPES = {"Run", "Ride", "Swim"}


class StravaClient:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self._client = Client()
        token_response = self._client.refresh_access_token(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )
        self._client.access_token = token_response["access_token"]

    def get_activities(self, after_date: str, before_date: str) -> list[dict]:
        after = datetime.fromisoformat(after_date)
        before = datetime.fromisoformat(before_date)
        raw = self._client.get_activities(after=after, before=before)
        return [self._parse(a) for a in raw if a.type in TRACKED_TYPES]

    def get_athlete_vo2max(self) -> float | None:
        # Strava API does not expose VO2max; populated from wearable data in a later integration
        return None

    def _parse(self, activity) -> dict:
        distance_km = float(activity.distance) / 1000
        duration_min = activity.moving_time.total_seconds() / 60
        pace = (duration_min / distance_km) if distance_km > 0 and activity.type == "Run" else None
        return {
            "date": str(activity.start_date_local.date()),
            "type": activity.type,
            "distance_km": round(distance_km, 2),
            "duration_min": round(duration_min, 1),
            "avg_pace_min_km": round(pace, 2) if pace else None,
            "avg_hr": int(activity.average_heartrate) if activity.average_heartrate else None,
            "vo2max": None,
        }


def build_client() -> StravaClient:
    return StravaClient(config.STRAVA_CLIENT_ID, config.STRAVA_CLIENT_SECRET, config.STRAVA_REFRESH_TOKEN)
