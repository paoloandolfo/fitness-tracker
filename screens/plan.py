# fitness-tracker/screens/plan.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta


def _current_week(plan_sessions: list[dict]) -> int:
    today = date.today().isoformat()
    for s in plan_sessions:
        if s["date"] >= today:
            return int(s["week"])
    return 15


def render(plan_sessions, activities):
    st.title("📅 Training Plan")

    completed_dates = {a["date"] for a in activities}
    max_week = max((int(s["week"]) for s in plan_sessions), default=15)
    default_week = _current_week(plan_sessions)

    week_num = st.slider("Week", 1, max_week, default_week)
    week_sessions = [s for s in plan_sessions if int(s["week"]) == week_num]

    if week_sessions:
        phase = week_sessions[0]["phase"]
        dates = [s["date"] for s in week_sessions]
        st.caption(f"**Phase: {phase}** · {dates[0]} → {dates[-1]}")
        st.divider()

        for s in week_sessions:
            d = date.fromisoformat(s["date"])
            d_str = s["date"]
            is_done = d_str in completed_dates
            is_today = d_str == date.today().isoformat()
            is_future = d > date.today()

            status = "✅" if is_done else ("📍 Today" if is_today else ("⬜" if is_future else "❌ Missed"))
            dist = f"{s['target_distance_km']}km" if s["target_distance_km"] else ""
            dur = f"{int(s['target_duration_min'])}min" if s["target_duration_min"] else ""
            detail = " · ".join(filter(None, [dist, dur, s["zone"]]))

            with st.expander(f"{status}  **{s['day']}** — {s['session_type']}  {detail}"):
                st.caption(s["notes"])
                if is_done:
                    actual = next((a for a in activities if a["date"] == d_str), None)
                    if actual:
                        st.markdown(f"Actual: {actual['distance_km']}km in {actual['duration_min']:.0f}min"
                                    + (f" @ {actual['avg_pace_min_km']} min/km" if actual.get("avg_pace_min_km") else ""))
    else:
        st.info("No sessions found for this week.")
