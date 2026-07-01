import requests
import config

TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
RECOVERY_URL = "https://api.prod.whoop.com/developer/v1/recovery/"


class WhoopClient:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self._client_id = client_id
        self._client_secret = client_secret
        resp = requests.post(TOKEN_URL, data={
            "client_id": client_id, "client_secret": client_secret,
            "refresh_token": refresh_token, "grant_type": "refresh_token",
        })
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]

    def get_recovery(self, after_date: str, before_date: str) -> list[dict]:
        try:
            resp = requests.get(
                RECOVERY_URL,
                headers={"Authorization": f"Bearer {self._access_token}"},
                params={"start": after_date, "end": before_date, "limit": 25},
            )
            resp.raise_for_status()
            return [self._parse(r) for r in resp.json().get("records", [])]
        except Exception:
            return []

    def _parse(self, record: dict) -> dict:
        date = record["created_at"][:10]
        score = record.get("score", {})
        sleep_ms = record.get("sleep", {}).get("total_in_bed_time_milli", 0)
        return {
            "date": date,
            "recovery_score": int(score.get("recovery_score", 0)),
            "hrv_ms": float(score.get("hrv_rmssd_milli", 0)),
            "resting_hr": int(score.get("resting_heart_rate", 0)),
            "sleep_hours": round(sleep_ms / 3_600_000, 1),
        }


def build_client() -> WhoopClient:
    return WhoopClient(config.WHOOP_CLIENT_ID, config.WHOOP_CLIENT_SECRET, config.WHOOP_REFRESH_TOKEN)
