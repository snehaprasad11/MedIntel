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
st.caption("The model's projected appointment volume, including the 30 genuine future days beyond the historical data.")
st.line_chart(forecast["yhat"])

st.divider()

comparison_path = BASE_DIR / "data/features/model_comparison.csv"

st.subheader("Model Comparison")
st.caption("Four forecasting approaches, evaluated on the same held-out slice of historical data — lower MAE is better. This is why Prophet was chosen over the alternatives (or wasn't — see for yourself).")

if comparison_path.exists():
    comparison = pd.read_csv(comparison_path)
    st.dataframe(comparison, use_container_width=True, hide_index=True)
else:
    st.info(
        "No comparison data yet. Run `python -m ml_models.model_comparison` "
        "from the project root to generate it."
    )
