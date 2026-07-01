# fitness-tracker/screens/progress.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from training_plan import WEEKLY_RUN_KM, _get_phase


def render(activities, plan_sessions):
    st.title("📈 Progress")

    df_act = pd.DataFrame(activities)
    if df_act.empty:
        st.info("No activity data yet.")
        return

    df_act["date"] = pd.to_datetime(df_act["date"])
    df_act["week"] = df_act["date"].dt.isocalendar().week

    # Weekly run volume chart
    st.subheader("Weekly Run Volume")
    runs = df_act[df_act["type"] == "Run"].copy()
    weekly_run = runs.groupby(runs["date"].dt.to_period("W"))["distance_km"].sum().reset_index()
    weekly_run["date"] = weekly_run["date"].dt.start_time

    plan_weeks = sorted(set(int(s["week"]) for s in plan_sessions))
    plan_dates = []
    plan_targets = []
    for w in plan_weeks:
        week_sessions = [s for s in plan_sessions if int(s["week"]) == w]
        if week_sessions:
            plan_dates.append(date.fromisoformat(week_sessions[0]["date"]))
            plan_targets.append(WEEKLY_RUN_KM.get(_get_phase(w), 0))

    fig1 = go.Figure()
    fig1.add_bar(x=weekly_run["date"], y=weekly_run["distance_km"], name="Actual", marker_color="#1f77b4")
    fig1.add_scatter(x=plan_dates, y=plan_targets, name="Target", mode="lines+markers",
                     line=dict(color="orange", dash="dash"))
    fig1.update_layout(height=300, margin=dict(t=10, b=10), legend=dict(orientation="h"))
    st.plotly_chart(fig1, use_container_width=True)

    # Long run progression
    st.subheader("Long Run Progression (Sundays)")
    sundays = df_act[(df_act["type"] == "Run") & (df_act["date"].dt.dayofweek == 6)]
    plan_sundays = [s for s in plan_sessions if s["day"] == "Sunday" and s["session_type"] != "Rest"]

    fig2 = go.Figure()
    if not sundays.empty:
        fig2.add_bar(x=sundays["date"], y=sundays["distance_km"], name="Actual", marker_color="#2ca02c")
    if plan_sundays:
        fig2.add_scatter(
            x=[date.fromisoformat(s["date"]) for s in plan_sundays],
            y=[s["target_distance_km"] or 0 for s in plan_sundays],
            name="Plan", mode="lines+markers", line=dict(color="orange", dash="dash")
        )
    fig2.update_layout(height=300, margin=dict(t=10, b=10), legend=dict(orientation="h"))
    st.plotly_chart(fig2, use_container_width=True)

    # Recovery trend
    st.subheader("30-Day Recovery Trend")
    # (rendered in performance screen instead — cross-link)
    st.caption("See Performance screen for recovery + VO2Max trends.")
