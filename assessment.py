MARATHON_KM = 42.195
PLAN_IMPROVEMENT_FACTOR = 0.96  # 4% improvement from 15-week quality block


def riegel_project(known_time_s: float, known_dist_km: float, target_dist_km: float) -> float:
    return known_time_s * (target_dist_km / known_dist_km) ** 1.06


def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}"


def assess_fitness(activities: list[dict]) -> dict:
    runs = [a for a in activities if a.get("type") == "Run" and a.get("distance_km", 0) > 5]
    if not runs:
        return {
            "current_pace_min_km": 0,
            "current_finish_seconds": 0,
            "projected_finish_seconds": 0,
            "projected_pace_min_km": 0,
            "target_label": "Unknown",
            "projected_label": "Unknown",
        }

    # Use the longest run (by distance) as the baseline
    best = max(runs, key=lambda r: r["distance_km"])
    known_time_s = best["duration_min"] * 60
    known_dist_km = best["distance_km"]

    current_finish_s = riegel_project(known_time_s, known_dist_km, MARATHON_KM)
    projected_finish_s = current_finish_s * PLAN_IMPROVEMENT_FACTOR

    current_pace = current_finish_s / 60 / MARATHON_KM
    projected_pace = projected_finish_s / 60 / MARATHON_KM

    return {
        "current_pace_min_km": round(current_pace, 2),
        "current_finish_seconds": round(current_finish_s),
        "projected_finish_seconds": round(projected_finish_s),
        "projected_pace_min_km": round(projected_pace, 2),
        "target_label": format_time(current_finish_s),
        "projected_label": format_time(projected_finish_s),
    }
