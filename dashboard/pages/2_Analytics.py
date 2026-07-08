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
    st.caption("Appointment count by department.")
    st.bar_chart(appointments.groupby("department_id").size())

with col2:
    st.subheader("Doctor Workload")
    st.caption("Appointment count by doctor.")
    st.bar_chart(appointments.groupby("doctor_id").size())

st.divider()

st.subheader("Wait Time Trend")
st.caption("Wait time in minutes across all recorded appointments, in order.")
st.line_chart(appointments["wait_time_minutes"])
