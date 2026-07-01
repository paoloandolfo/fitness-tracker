# fitness-tracker/screens/history.py
import streamlit as st
import pandas as pd


def render(activities):
    st.title("📋 History")

    if not activities:
        st.info("No activities yet.")
        return

    df = pd.DataFrame(activities)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False)

    activity_type = st.selectbox("Filter by type", ["All", "Run", "Ride", "Swim"])
    if activity_type != "All":
        df = df[df["type"] == activity_type]

    df_display = df[["date", "type", "distance_km", "duration_min", "avg_pace_min_km", "avg_hr"]].copy()
    df_display.columns = ["Date", "Type", "Distance (km)", "Duration (min)", "Pace (min/km)", "Avg HR"]
    df_display["Date"] = df_display["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(df_display, use_container_width=True, hide_index=True)
    st.caption(f"{len(df_display)} activities shown")
