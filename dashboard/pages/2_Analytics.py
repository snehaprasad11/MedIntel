import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme

apply_theme("light")

appointments, beds, forecast = load_all_data()

st.title("📊 Analytics Dashboard")
st.caption("Where is the load actually coming from — which departments and which doctors are carrying the most volume?")
st.divider()

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
