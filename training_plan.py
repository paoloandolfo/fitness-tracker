# fitness-tracker/training_plan.py
from datetime import date, timedelta

# Plan starts Monday June 29, 2026 (the Monday of the week containing July 1).
# Weeks 1-14 run sequentially. Race Week (week 15) starts Monday Oct 12, 2026
# so that the marathon on Sunday Oct 18 falls exactly in week 15, day 7.
# This gives exactly 14 × 7 + 7 = 105 sessions total.
PLAN_START = date(2026, 6, 29)   # Monday — first training day
MARATHON_DATE = date(2026, 10, 18)

PHASES = [
    (1, 4, "Base"),
    (5, 8, "Build"),
    (9, 11, "Peak"),
    (12, 14, "Taper"),
    (15, 15, "Race Week"),
]

# (phase, day_of_week) -> (session_type, distance_km, duration_min, zone, notes)
SESSION_TEMPLATES = {
    ("Base", "Monday"):    ("Pool swim", None, 45, "Z2", "2km easy"),
    ("Base", "Tuesday"):   ("Short bike", None, 45, "Z2", "45min easy spin"),
    ("Base", "Wednesday"): ("Run intervals", 8.0, None, "Z3-Z4", "Include 4x1km at threshold"),
    ("Base", "Thursday"):  ("Recovery", None, 45, "Z1", "Swim, gym, or rest — your call"),
    ("Base", "Friday"):    ("Easy run", 8.0, None, "Z2", "Conversational pace"),
    ("Base", "Saturday"):  ("Long bike", None, 90, "Z2", "Steady endurance ride"),
    ("Base", "Sunday"):    ("Long run", None, None, "Z2", "Easy pace throughout"),

    ("Build", "Monday"):   ("Pool swim", None, 50, "Z2", "2.5km"),
    ("Build", "Tuesday"):  ("Short bike", None, 60, "Z2", "60min endurance"),
    ("Build", "Wednesday"):("Run intervals", 10.0, None, "Z3-Z4", "6x1km at marathon pace"),
    ("Build", "Thursday"): ("Recovery", None, 50, "Z1-Z2", "Swim or gym"),
    ("Build", "Friday"):   ("Easy run", 10.0, None, "Z2", "Easy, no watch pressure"),
    ("Build", "Saturday"): ("Long bike", None, 120, "Z2", "2hr steady"),
    ("Build", "Sunday"):   ("Long run", None, None, "Z2", "Last 5km at marathon pace"),

    ("Peak", "Monday"):    ("Pool swim", None, 55, "Z2", "3km"),
    ("Peak", "Tuesday"):   ("Short bike", None, 60, "Z2-Z3", "Include 2x10min tempo"),
    ("Peak", "Wednesday"): ("Run intervals", 12.0, None, "Z4", "8x1km at race pace"),
    ("Peak", "Thursday"):  ("Recovery", None, 50, "Z1", "Easy swim — protect the legs"),
    ("Peak", "Friday"):    ("Easy run", 10.0, None, "Z2", "Shake-out, feel good"),
    ("Peak", "Saturday"):  ("Long bike", None, 120, "Z2", "Steady, save legs for Sunday"),
    ("Peak", "Sunday"):    ("Long run", None, None, "Z2", "Race effort last 10km"),

    ("Taper", "Monday"):   ("Pool swim", None, 40, "Z2", "2km easy"),
    ("Taper", "Tuesday"):  ("Short bike", None, 45, "Z1-Z2", "Easy spin, no pressure"),
    ("Taper", "Wednesday"):("Run intervals", 6.0, None, "Z3", "4x1km to stay sharp"),
    ("Taper", "Thursday"): ("Rest", None, None, "Rest", "Full rest or walk only"),
    ("Taper", "Friday"):   ("Easy run", 6.0, None, "Z2", "Light and fresh"),
    ("Taper", "Saturday"): ("Long bike", None, 75, "Z2", "Easy — legs for race"),
    ("Taper", "Sunday"):   ("Long run", None, None, "Z2", "Shorter, confidence run"),

    ("Race Week", "Monday"):   ("Pool swim", None, 30, "Z1", "Light 1.5km"),
    ("Race Week", "Tuesday"):  ("Easy run", 5.0, None, "Z1", "Very easy"),
    ("Race Week", "Wednesday"):("Easy run", 4.0, None, "Z1", "Shake out"),
    ("Race Week", "Thursday"): ("Rest", None, None, "Rest", "Rest completely"),
    ("Race Week", "Friday"):   ("Easy run", 3.0, None, "Z1", "10min jog + strides"),
    ("Race Week", "Saturday"): ("Rest", None, None, "Rest", "Rest, prep kit, sleep early"),
    ("Race Week", "Sunday"):   ("Amsterdam Marathon", 42.2, None, "Race", "Race day!"),
}

LONG_RUN_KM = {
    1: 18, 2: 20, 3: 22, 4: 22,
    5: 24, 6: 26, 7: 28, 8: 28,
    9: 30, 10: 32, 11: 35,
    12: 28, 13: 22, 14: 16,
    15: 42.2,
}

WEEKLY_RUN_KM = {
    "Base": 45, "Build": 60, "Peak": 70, "Taper": 40, "Race Week": 10
}
WEEKLY_BIKE_HOURS = {
    "Base": 2.25, "Build": 3.0, "Peak": 3.0, "Taper": 2.0, "Race Week": 0.5
}
WEEKLY_SWIM_KM = {
    "Base": 2.0, "Build": 2.5, "Peak": 3.0, "Taper": 2.0, "Race Week": 1.5
}


def _get_phase(week: int) -> str:
    for start, end, phase in PHASES:
        if start <= week <= end:
            return phase
    return "Race Week"


def _week_start(week: int) -> date:
    """Return the Monday that starts the given training week.

    Weeks 1-14 are consecutive (each 7 days apart from PLAN_START).
    Week 15 is Race Week: its Monday is fixed to Oct 12, 2026, so that
    Sunday Oct 18 (Amsterdam Marathon) is exactly day 7 of week 15.
    This produces exactly 15 × 7 = 105 sessions in the plan.
    """
    if week == 15:
        return date(2026, 10, 12)
    return PLAN_START + timedelta(weeks=week - 1)


def generate_plan(target_finish_seconds: float) -> list[dict]:
    sessions = []
    for week in range(1, 16):
        phase = _get_phase(week)
        week_start = _week_start(week)
        for i in range(7):
            session_date = week_start + timedelta(days=i)
            day = session_date.strftime("%A")
            template = SESSION_TEMPLATES.get((phase, day))
            if not template:
                continue
            s_type, dist, dur, zone, notes = template
            if day == "Sunday":
                dist = LONG_RUN_KM.get(week, dist)
            sessions.append({
                "date": session_date.isoformat(),
                "week": week,
                "phase": phase,
                "day": day,
                "session_type": s_type,
                "target_distance_km": dist,
                "target_duration_min": dur,
                "zone": zone,
                "notes": notes,
            })
    return sessions


def get_session_for_date(plan: list[dict], date: str) -> dict | None:
    for s in plan:
        if s["date"] == date:
            return s
    return None


def get_week_targets(plan: list[dict], week: int) -> dict:
    phase = _get_phase(week)
    return {
        "week": week,
        "phase": phase,
        "run_km": WEEKLY_RUN_KM.get(phase, 0),
        "bike_hours": WEEKLY_BIKE_HOURS.get(phase, 0),
        "swim_km": WEEKLY_SWIM_KM.get(phase, 0),
    }
