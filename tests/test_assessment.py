import pytest
from assessment import riegel_project, format_time, assess_fitness


def test_riegel_project_half_to_full():
    # 1:55:00 half → should project ~4h full
    half_seconds = 6900
    result = riegel_project(half_seconds, 21.097, 42.195)
    assert 13500 < result < 15000  # between 3h45 and 4h10


def test_riegel_project_10k_to_full():
    result = riegel_project(2700, 10.0, 42.195)  # 45min 10k
    assert result > 10000  # more than 2h47m


def test_format_time_hours():
    assert format_time(13500) == "3:45:00"


def test_format_time_sub_hour():
    assert format_time(2700) == "0:45:00"


def test_assess_fitness_uses_longest_run():
    activities = [
        {"date": "2026-05-01", "type": "Run", "distance_km": 10.0, "duration_min": 52.0,
         "avg_pace_min_km": 5.2, "avg_hr": 148, "vo2max": None},
        {"date": "2026-05-15", "type": "Run", "distance_km": 21.0, "duration_min": 115.5,
         "avg_pace_min_km": 5.5, "avg_hr": 155, "vo2max": None},
    ]
    result = assess_fitness(activities)
    assert result["current_pace_min_km"] > 0
    assert result["projected_finish_seconds"] > result["current_finish_seconds"]


def test_assess_fitness_empty_returns_defaults():
    result = assess_fitness([])
    assert result["current_pace_min_km"] == 0
    assert result["target_label"] == "Unknown"
