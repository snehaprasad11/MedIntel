import streamlit as st
import pandas as pd
from pathlib import Path
from dashboard.core.theme import apply_theme

apply_theme("light")

st.title("📈 Forecasting")
st.caption("What does demand look like next, based on patterns in historical appointment volume (Prophet forecast model)?")
st.divider()

BASE_DIR = Path(__file__).resolve().parents[2]
forecast_path = BASE_DIR / "data/features/prophet_forecast.csv"

if not forecast_path.exists():
    st.error(
        "Missing generated data file: data/features/prophet_forecast.csv. "
        "Run `python etl/run_pipeline.py` from the project root."
    )
    st.stop()

forecast = pd.read_csv(forecast_path)

st.subheader("Predicted Demand (yhat)")
st.caption("The model's projected appointment volume over the forecast horizon.")
st.line_chart(forecast["yhat"])
