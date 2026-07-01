# fitness-tracker/screens/performance.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from assessment import assess_fitness, riegel_project, format_time, MARATHON_KM, PLAN_IMPROVEMENT_FACTOR


def _pace_label(min_km: float) -> str:
    if min_km == 0:
        return "—"
    mins = int(min_km)
    secs = int((min_km - mins) * 60)
    return f"{mins}:{secs:02d} /km"


def render(activities, metadata):
    st.title("⚡ Performance")

    meta = {row["key"]: row["value"] for row in metadata} if metadata else {}

    current_label = meta.get("current_finish_label", "—")
    projected_label = meta.get("projected_finish_label", "—")
    current_pace = float(meta.get("current_pace_min_km", 0))
    projected_pace = float(meta.get("projected_pace_min_km", 0))

    # Main two-column comparison
    col1, col2 = st.columns(2)
    with col1:
        st.metric("If You Raced Today", current_label,
                  delta=None, help="Based on your longest recent run via Riegel formula")
        st.caption(f"Pace: {_pace_label(current_pace)}")
        st.caption("Based on current fitness & recent long runs")

    with col2:
        st.metric("Race Day Projection", projected_label,
                  delta=None, help="If you commit to the plan through October 18")
        st.caption(f"Pace: {_pace_label(projected_pace)}")
        st.caption("Based on current trajectory continued through Oct 18")

    # Gain summary
    if current_pace > 0 and projected_pace > 0:
        st.divider()
        pace_gain = current_pace - projected_pace
        time_gain = int((float(meta.get("current_finish_seconds", 0) or 0) -
                         float(meta.get("projected_finish_seconds", 0) or 0)))

        st.subheader("Potential Gain from Committing to the Plan")
        g1, g2 = st.columns(2)
        g1.metric("Pace improvement", f"{pace_gain*60:.0f} sec/km faster")
        g2.metric("Time improvement", f"{time_gain//60} min off finish")

    # Pace trajectory chart
    st.divider()
    st.subheader("Pace Trajectory")

    df = pd.DataFrame(activities)
    if not df.empty and "type" in df.columns:
        df = df[df["type"] == "Run"].copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df[df["avg_pace_min_km"].notna() & (df["avg_pace_min_km"] > 0)]
        df = df.sort_values("date")

        fig = go.Figure()
        if not df.empty:
            fig.add_scatter(x=df["date"], y=df["avg_pace_min_km"],
                            mode="markers", name="Run pace", marker=dict(color="#1f77b4", size=6))
            # rolling 4-run average
            df["rolling_pace"] = df["avg_pace_min_km"].rolling(4, min_periods=1).mean()
            fig.add_scatter(x=df["date"], y=df["rolling_pace"],
                            mode="lines", name="4-run average", line=dict(color="orange", width=2))

        if projected_pace > 0:
            fig.add_scatter(
                x=[date(2026, 10, 18)], y=[projected_pace],
                mode="markers", name="Race day target",
                marker=dict(color="green", size=12, symbol="star")
            )

        fig.update_layout(
            height=350,
            yaxis_title="Pace (min/km)",
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h"),
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No run data available yet.")
