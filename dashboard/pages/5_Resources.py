import streamlit as st
from dashboard.core.data_loader import load_all_data

appointments, beds, forecast = load_all_data()

st.title("🏥 Resource Utilization")

beds["utilization"] = (beds["occupied_beds"] / beds["total_beds"]) * 100

st.subheader("Bed Utilization by Department")

st.bar_chart(beds.set_index("department_id")["utilization"])

st.subheader("Raw Data")
st.dataframe(beds)

