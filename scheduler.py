# fitness-tracker/scheduler.py
from datetime import date, timedelta

import config
from strava_client import build_client as strava
from whoop_client import build_client as whoop
from sheets_client import build_client as sheets
from training_plan import generate_plan
from assessment import assess_fitness, format_time

ACTIVITY_HEADERS = ["date", "type", "distance_km", "duration_min", "avg_pace_min_km", "avg_hr", "vo2max"]
RECOVERY_HEADERS = ["date", "recovery_score", "hrv_ms", "resting_hr", "sleep_hours"]
PLAN_HEADERS = ["date", "week", "phase", "day", "session_type", "target_distance_km", "target_duration_min", "zone", "notes"]


def run_daily_sync() -> None:
    sc = sheets()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()

    # Pull yesterday's Strava activity
    activities = strava().get_activities(yesterday, today)
    if activities:
        rows = [[a[h] for h in ACTIVITY_HEADERS] for a in activities]
        sc.append_rows("activities", rows)

    # Pull today's Whoop recovery
    recovery = whoop().get_recovery(yesterday, today)
    if recovery:
        rows = [[r[h] for h in RECOVERY_HEADERS] for r in recovery]
        sc.append_rows("recovery", rows)

    print(f"Daily sync complete: {len(activities)} activities, {len(recovery)} recovery records.")


def run_first_time_setup() -> None:
    sc = sheets()
    six_months_ago = (date.today() - timedelta(days=180)).isoformat()
    today = date.today().isoformat()

    print("Pulling 6 months of Strava history...")
    activities = strava().get_activities(six_months_ago, today)
    rows = [[a.get(h) for h in ACTIVITY_HEADERS] for a in activities]
    sc.overwrite("activities", ACTIVITY_HEADERS, rows)

    print("Pulling Whoop recovery history...")
    recovery = whoop().get_recovery(six_months_ago, today)
    rows = [[r.get(h) for h in RECOVERY_HEADERS] for r in recovery]
    sc.overwrite("recovery", RECOVERY_HEADERS, rows)

    print("Assessing fitness and generating training plan...")
    assessment = assess_fitness(activities)
    plan = generate_plan(assessment["projected_finish_seconds"])
    plan_rows = [[s.get(h) for h in PLAN_HEADERS] for s in plan]
    sc.overwrite("training_plan", PLAN_HEADERS, plan_rows)

    sc.set_value("metadata", "current_finish_label", assessment["target_label"])
    sc.set_value("metadata", "projected_finish_label", assessment["projected_label"])
    sc.set_value("metadata", "current_pace_min_km", str(assessment["current_pace_min_km"]))
    sc.set_value("metadata", "projected_pace_min_km", str(assessment["projected_pace_min_km"]))
    sc.set_value("metadata", "current_finish_seconds", str(assessment["current_finish_seconds"]))
    sc.set_value("metadata", "projected_finish_seconds", str(assessment["projected_finish_seconds"]))
    sc.set_value("metadata", "setup_complete", "true")

    print(f"Setup complete. Current projection: {assessment['target_label']} | With plan: {assessment['projected_label']}")


if __name__ == "__main__":
    import sys
    if "--setup" in sys.argv:
        run_first_time_setup()
    else:
        run_daily_sync()
