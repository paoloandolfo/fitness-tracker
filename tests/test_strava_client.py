# fitness-tracker/tests/test_strava_client.py
import pytest
from unittest.mock import MagicMock, patch
from strava_client import StravaClient


def test_get_activities_returns_list_of_dicts():
    mock_activity = MagicMock()
    mock_activity.start_date_local.date.return_value.__str__ = lambda s: "2026-06-15"
    mock_activity.type = "Run"
    mock_activity.distance = 10200.0
    mock_activity.moving_time.total_seconds.return_value = 3120.0
    mock_activity.average_heartrate = 148
    mock_activity.average_speed = 3.27

    with patch("strava_client.Client") as MockClient:
        instance = MockClient.return_value
        instance.refresh_access_token.return_value = {"access_token": "tok", "refresh_token": "ref"}
        instance.get_activities.return_value = [mock_activity]

        client = StravaClient("id", "secret", "refresh")
        activities = client.get_activities("2026-06-01", "2026-06-30")

    assert len(activities) == 1
    assert activities[0]["type"] == "Run"
    assert activities[0]["distance_km"] == pytest.approx(10.2, rel=0.01)
    assert activities[0]["duration_min"] == pytest.approx(52.0, rel=0.01)


def test_get_activities_filters_non_triathlon_types():
    mock_activity = MagicMock()
    mock_activity.type = "Yoga"
    mock_activity.start_date_local.date.return_value.__str__ = lambda s: "2026-06-15"
    mock_activity.distance = 0

    with patch("strava_client.Client") as MockClient:
        instance = MockClient.return_value
        instance.refresh_access_token.return_value = {"access_token": "tok", "refresh_token": "ref"}
        instance.get_activities.return_value = [mock_activity]
        client = StravaClient("id", "secret", "refresh")
        activities = client.get_activities("2026-06-01", "2026-06-30")

    assert activities == []


def test_pace_calculated_correctly_for_runs():
    mock_activity = MagicMock()
    mock_activity.type = "Run"
    mock_activity.distance = 10000.0
    mock_activity.moving_time.total_seconds.return_value = 3000.0  # 50 min for 10km = 5:00/km
    mock_activity.average_heartrate = 150
    mock_activity.average_speed = 3.33
    mock_activity.start_date_local.date.return_value.__str__ = lambda s: "2026-06-15"

    with patch("strava_client.Client") as MockClient:
        instance = MockClient.return_value
        instance.refresh_access_token.return_value = {"access_token": "tok", "refresh_token": "ref"}
        instance.get_activities.return_value = [mock_activity]
        client = StravaClient("id", "secret", "refresh")
        activities = client.get_activities("2026-06-01", "2026-06-30")

    assert activities[0]["avg_pace_min_km"] == pytest.approx(5.0, rel=0.01)
