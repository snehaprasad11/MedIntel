import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_latest_snapshots, get_snapshot_history

apply_theme("light")
require_mode_selected()

st.title("📊 Analytics Dashboard")
st.caption("Where is the load actually coming from — which departments and which doctors are carrying the most volume?")
st.divider()

if is_demo_mode():
    appointments, beds, forecast = load_all_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Department Load")
        st.caption("Top 15 departments by appointment count (of 50 total).")
        dept_load = appointments.groupby("department_id").size().sort_values(ascending=False).head(15)
        st.bar_chart(dept_load)

    with col2:
        st.subheader("Doctor Workload")
        st.caption("Top 15 busiest doctors by appointment count (of 500 total).")
        doctor_load = appointments.groupby("doctor_id").size().sort_values(ascending=False).head(15)
        st.bar_chart(doctor_load)

    st.divider()

    st.subheader("Wait Time Trend")
    st.caption("Average wait time per day, across the full date range — not every individual appointment (100,000 of them), which was both slow to render and too noisy to read as a trend.")
    daily_wait_time = appointments.groupby("date")["wait_time_minutes"].mean().sort_index()
    st.line_chart(daily_wait_time)

else:
    hospital = get_current_hospital()
    engine = get_engine()
    latest = get_latest_snapshots(engine, hospital["id"])
    history = get_snapshot_history(engine, hospital["id"])

    if latest.empty:
        st.info("No data submitted yet. Go to **Submit Update** to enter your first department snapshot.")
        st.stop()

    latest["bed_occupancy_pct"] = (latest["occupied_beds"] / latest["total_beds"] * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bed Occupancy by Department")
        st.caption("Latest submitted occupancy %, by department.")
        st.bar_chart(latest.set_index("department_name")["bed_occupancy_pct"])

    with col2:
        st.subheader("Wait Time by Department")
        st.caption("Latest submitted average wait time (minutes), by department.")
        st.bar_chart(latest.set_index("department_name")["avg_wait_time_minutes"])

    st.divider()

    st.subheader("Wait Time Trend")
    if len(history["submitted_at"].unique()) < 2:
        st.info("Only one submission so far — a trend needs at least two, over time, to show anything.")
    else:
        st.caption("Average wait time across all departments, per submission over time.")
        trend = history.groupby("submitted_at")["avg_wait_time_minutes"].mean().sort_index()
        st.line_chart(trend)
