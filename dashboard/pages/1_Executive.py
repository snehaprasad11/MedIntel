import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme

apply_theme("light")

appointments, beds, forecast = load_all_data()

st.title("🏥 Executive Overview")
st.caption("The 30-second read: today's headline numbers across the whole hospital, at a glance.")
st.divider()

total_appointments = len(appointments)
avg_wait_time = appointments["wait_time_minutes"].mean()
avg_beds = beds["occupied_beds"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Appointments", total_appointments)
col2.metric("Avg Wait Time (min)", round(avg_wait_time, 2))
col3.metric("Avg Beds Occupied", round(avg_beds, 2))

st.divider()

st.subheader("Recent Appointments")
st.caption("A sample of the underlying appointment records these headline numbers are computed from.")
st.dataframe(appointments.head(), use_container_width=True)
