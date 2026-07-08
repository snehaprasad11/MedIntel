import streamlit as st
import pandas as pd

from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_latest_snapshots
from ai_insights.analytics_engine import calculate_metrics
from ai_insights.openai_insights import generate_llm_insight

apply_theme("light")
require_mode_selected()

st.title("🤖 AI Insights")
st.caption("A plain-English summary plus an automatic recommendation, generated from the same metrics as the other pages — not a separate data source.")
st.divider()

if is_demo_mode():
    appointments, beds, forecast = load_all_data()
    metrics = calculate_metrics(appointments, beds)

else:
    hospital = get_current_hospital()
    engine = get_engine()
    latest = get_latest_snapshots(engine, hospital["id"])

    if latest.empty:
        st.info("No data submitted yet. Go to **Submit Update** to enter your first department snapshot.")
        st.stop()

    metrics = {
        "total_appointments": latest["department_name"].nunique(),
        "avg_wait_time": round(latest["avg_wait_time_minutes"].mean(), 2),
        "avg_bed_occupancy": round((latest["occupied_beds"] / latest["total_beds"] * 100).mean(), 2),
        "avg_icu_occupancy": round((latest["occupied_icu_beds"] / latest["total_icu_beds"] * 100).mean(), 2),
    }

result = generate_llm_insight(metrics)

if isinstance(result, dict):
    executive = result.get("executive_summary", "No summary generated")
    recommendation = result.get("recommendation", "No recommendation generated")
else:
    executive = str(result)
    recommendation = "Recommendation unavailable"

col1, col2 = st.columns(2)

with col1:
    st.subheader("Executive Summary")
    st.success(executive)

with col2:
    st.subheader("Recommendation")
    st.warning(recommendation)
