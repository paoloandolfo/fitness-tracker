# fitness-tracker/tests/test_training_plan.py
from training_plan import generate_plan, get_session_for_date, get_week_targets


def test_plan_has_105_sessions():
    plan = generate_plan(target_finish_seconds=13500)  # 3h45m
    assert len(plan) == 105  # 15 weeks × 7 days


def test_marathon_date_is_race():
    plan = generate_plan(target_finish_seconds=13500)
    race_day = [s for s in plan if s["date"] == "2026-10-18"]
    assert len(race_day) == 1
    assert race_day[0]["session_type"] == "Amsterdam Marathon"


def test_week_1_sunday_long_run_is_base():
    plan = generate_plan(target_finish_seconds=13500)
    sunday_w1 = get_session_for_date(plan, "2026-07-05")  # first Sunday
    assert sunday_w1 is not None
    assert sunday_w1["phase"] == "Base"
    assert sunday_w1["target_distance_km"] <= 22


def test_peak_long_run_is_above_30km():
    plan = generate_plan(target_finish_seconds=13500)
    # Week 9 Sunday = Aug 30
    peak_sunday = get_session_for_date(plan, "2026-08-30")
    assert peak_sunday is not None
    assert peak_sunday["target_distance_km"] >= 30


def test_get_week_targets_returns_dict():
    plan = generate_plan(target_finish_seconds=13500)
    targets = get_week_targets(plan, 1)
    assert "run_km" in targets
    assert "bike_hours" in targets
    assert "swim_km" in targets
    assert targets["run_km"] > 0
