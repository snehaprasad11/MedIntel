import streamlit as st
from dashboard.core.data_loader import load_all_data

appointments, beds, forecast = load_all_data()

st.title("📊 Analytics Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Department Load")
    st.bar_chart(appointments.groupby("department_id").size())

with col2:
    st.subheader("Doctor Workload")
    st.bar_chart(appointments.groupby("doctor_id").size())

st.line_chart(appointments["wait_time_minutes"])