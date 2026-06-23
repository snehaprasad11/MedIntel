import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

@st.cache_data
def load_all_data():

    appointments = pd.read_csv(BASE_DIR / "data/features/appointments_features.csv")
    beds = pd.read_csv(BASE_DIR / "data/clean/beds.csv")
    forecast = pd.read_csv(BASE_DIR / "data/features/prophet_forecast.csv")

    appointments["wait_time_minutes"] = appointments["wait_time_minutes"].fillna(0)

    beds["utilization"] = (beds["occupied_beds"] / beds["total_beds"]) * 100

    return appointments, beds, forecast