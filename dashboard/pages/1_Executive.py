import streamlit as st
from dashboard.core.data_loader import load_all_data

appointments, beds, forecast = load_all_data()

st.title("🏥 Executive Overview")

total_appointments = len(appointments)
avg_wait_time = appointments["wait_time_minutes"].mean()
avg_beds = beds["occupied_beds"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Appointments", total_appointments)
col2.metric("Avg Wait Time", round(avg_wait_time, 2))
col3.metric("Avg Beds Used", round(avg_beds, 2))

st.dataframe(appointments.head())

