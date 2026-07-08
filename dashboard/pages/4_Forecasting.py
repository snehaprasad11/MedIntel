import streamlit as st
import pandas as pd
from pathlib import Path
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_snapshot_history

apply_theme("light")
require_mode_selected()

st.title("📈 Forecasting")
st.caption("What does demand look like next, based on historical patterns?")
st.divider()

MIN_HISTORY_DAYS = 14

if is_demo_mode():
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

else:
    hospital = get_current_hospital()
    engine = get_engine()
    history = get_snapshot_history(engine, hospital["id"])

    days_of_history = history["submitted_at"].dt.date.nunique() if not history.empty else 0

    if days_of_history < MIN_HISTORY_DAYS:
        st.info(
            f"Forecasting needs a real trend to learn from — you have **{days_of_history} of {MIN_HISTORY_DAYS}** "
            "minimum days of submissions. Keep submitting updates (once a day is enough) and this page "
            "will unlock automatically once there's enough history."
        )
        st.progress(min(days_of_history / MIN_HISTORY_DAYS, 1.0))
        st.stop()

    st.subheader("Bed Occupancy Forecast")
    st.caption("Projects your total occupied-bed trend forward, based on your submission history so far.")

    if st.button("Generate Forecast", type="primary"):
        with st.spinner("Fitting a forecast model to your submission history..."):
            from prophet import Prophet

            daily = history.groupby(history["submitted_at"].dt.date)["occupied_beds"].sum().reset_index()
            daily.columns = ["ds", "y"]

            model = Prophet()
            model.fit(daily)

            future = model.make_future_dataframe(periods=7)
            forecast = model.predict(future)

        st.line_chart(forecast.set_index("ds")[["yhat"]])
        st.caption("Shaded/projected values beyond your last submission date are the 7-day-ahead forecast.")
