# fitness-tracker/screens/today.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import config

MARATHON_DATE = date(2026, 10, 18)


def _recovery_status(score: int) -> tuple[str, str, str]:
    if score < config.RECOVERY_RED_THRESHOLD:
        return "🔴", "Low", "Low recovery today. Session stays as planned — consider warming up longer and monitoring effort by feel rather than pace."
    elif score < config.RECOVERY_AMBER_THRESHOLD:
        return "🟡", "Moderate", "Moderate recovery. You can push — keep the first portion easy before ramping up."
    return "🟢", "Good", "Good recovery. Execute as planned."


def render(activities, recovery, plan_sessions, metadata):
    today_str = date.today().isoformat()
    days_to_race = (MARATHON_DATE - date.today()).days

    st.title("🏃 Today")
    st.caption(f"Amsterdam Marathon in **{days_to_race} days** · {MARATHON_DATE.strftime('%B %d, %Y')}")

    # Recovery card
    today_recovery = next((r for r in sorted(recovery, key=lambda x: x["date"], reverse=True)
                           if r["date"] <= today_str), None)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recovery")
        if today_recovery:
            score = int(today_recovery["recovery_score"])
            emoji, label, message = _recovery_status(score)
            st.metric(f"{emoji} {label}", f"{score}%")
            st.caption(f"HRV: {today_recovery['hrv_ms']}ms · RHR: {today_recovery['resting_hr']}bpm · Sleep: {today_recovery['sleep_hours']}h")
            if score < config.RECOVERY_AMBER_THRESHOLD:
                st.warning(message)
            else:
                st.success(message)
        else:
            st.info("No recovery data for today yet.")

    with col2:
        st.subheader("Today's Session")
        today_session = next((s for s in plan_sessions if s["date"] == today_str), None)
        if today_session:
            st.markdown(f"**{today_session['session_type']}**")
            if today_session["target_distance_km"]:
                st.markdown(f"Target: {today_session['target_distance_km']} km")
            if today_session["target_duration_min"]:
                st.markdown(f"Duration: {int(today_session['target_duration_min'])} min")
            st.markdown(f"Zone: {today_session['zone']}")
            st.caption(today_session["notes"])
        else:
            st.info("Rest day or no session planned.")

    # Weekly glance
    st.divider()
    st.subheader("This Week")
    week_start = date.today() - timedelta(days=date.today().weekday())
    days = [week_start + timedelta(days=i) for i in range(7)]
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    completed_dates = {a["date"] for a in activities}
    cols = st.columns(7)
    for col, d, name in zip(cols, days, day_names):
        d_str = d.isoformat()
        session = next((s for s in plan_sessions if s["date"] == d_str), None)
        if d > date.today():
            col.markdown(f"**{name}**\n\n⬜")
        elif d_str in completed_dates:
            col.markdown(f"**{name}**\n\n✅")
        elif session and session["session_type"] != "Rest":
            col.markdown(f"**{name}**\n\n⚠️")
        else:
            col.markdown(f"**{name}**\n\n—")

    # Weekly mileage summary
    week_activities = [a for a in activities if week_start.isoformat() <= a["date"] <= days[-1].isoformat()]
    week_run_km = sum(a["distance_km"] for a in week_activities if a["type"] == "Run")

    st.divider()
    st.subheader("Weekly Mileage")
    target_run_km = 45  # default base; in production read from metadata
    st.progress(min(week_run_km / max(target_run_km, 1), 1.0),
                text=f"Running: {week_run_km:.1f}km / {target_run_km}km target")
