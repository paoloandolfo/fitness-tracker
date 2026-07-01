import streamlit as st
from sheets_client import build_client
from screens import today, plan, progress, performance, history

st.set_page_config(page_title="Marathon Tracker", page_icon="🏃", layout="wide")


@st.cache_data(ttl=300)
def load_data():
    sc = build_client()
    return {
        "activities": sc.read_all("activities"),
        "recovery": sc.read_all("recovery"),
        "plan": sc.read_all("training_plan"),
        "metadata": sc.read_all("metadata"),
    }


data = load_data()

st.sidebar.title("🏃 Marathon Tracker")
st.sidebar.caption("Amsterdam · Oct 18, 2026")
screen = st.sidebar.radio("", ["Today", "Training Plan", "Progress", "Performance", "History"])

if screen == "Today":
    today.render(data["activities"], data["recovery"], data["plan"], data["metadata"])
elif screen == "Training Plan":
    plan.render(data["plan"], data["activities"])
elif screen == "Progress":
    progress.render(data["activities"], data["plan"])
elif screen == "Performance":
    performance.render(data["activities"], data["metadata"])
elif screen == "History":
    history.render(data["activities"])
