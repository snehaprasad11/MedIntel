import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme

apply_theme("light")

appointments, beds, forecast = load_all_data()

st.title("🏥 Resource Utilization")
st.caption("Are we running out of physical beds — occupancy rate by department.")
st.divider()

beds["utilization"] = (beds["occupied_beds"] / beds["total_beds"]) * 100

st.subheader("Bed Utilization by Department")
st.caption("Occupied beds as a percentage of total beds, per department. Above ~85% is generally considered strained.")
st.bar_chart(beds.set_index("department_id")["utilization"])

st.divider()

st.subheader("Raw Bed Data")
st.dataframe(beds, use_container_width=True)
