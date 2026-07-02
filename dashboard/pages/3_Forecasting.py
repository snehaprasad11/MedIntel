import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📈 Forecasting")

BASE_DIR = Path(__file__).resolve().parents[2]
forecast_path = BASE_DIR / "data/features/prophet_forecast.csv"

if not forecast_path.exists():
    st.error(
        "Missing generated data file: data/features/prophet_forecast.csv. "
        "Run `python etl/run_pipeline.py` from the project root."
    )
    st.stop()

forecast = pd.read_csv(forecast_path)

st.line_chart(forecast["yhat"])

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)
