import streamlit as st

@st.cache_data
def get_department_load(df):
    return df.groupby("department_id").size()

@st.cache_data
def get_doctor_load(df):
    return df.groupby("doctor_id").size()

@st.cache_data
def get_doctor_performance(df):
    return df.groupby("doctor_id").agg({
        "wait_time_minutes": "mean",
        "appointment_id": "count"
    }).rename(columns={"appointment_id": "total_patients"})