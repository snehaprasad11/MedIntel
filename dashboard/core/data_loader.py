import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[2]

@st.cache_data
def load_all_data():
    required_files = {
        "appointments": BASE_DIR / "data/features/appointments_features.csv",
        "beds": BASE_DIR / "data/clean/beds.csv",
        "forecast": BASE_DIR / "data/features/prophet_forecast.csv",
    }

    missing_files = [
        str(path.relative_to(BASE_DIR))
        for path in required_files.values()
        if not path.exists()
    ]

    if missing_files:
        st.error(
            "Missing generated data files: "
            + ", ".join(missing_files)
            + ". Run `python etl/run_pipeline.py` from the project root."
        )
        st.stop()

    appointments = pd.read_csv(required_files["appointments"])
    beds = pd.read_csv(required_files["beds"])
    forecast = pd.read_csv(required_files["forecast"])

    appointments["wait_time_minutes"] = appointments["wait_time_minutes"].fillna(0)

    beds["utilization"] = (beds["occupied_beds"] / beds["total_beds"]) * 100

    return appointments, beds, forecast
