import streamlit as st
import pandas as pd

from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme
from ai_insights.analytics_engine import calculate_metrics
from ai_insights.openai_insights import generate_llm_insight

apply_theme("light")

appointments, beds, forecast = load_all_data()

st.title("🤖 AI Insights")
st.caption("A plain-English summary plus an automatic recommendation, generated from the same metrics as the other pages — not a separate data source.")
st.divider()

metrics = calculate_metrics(appointments, beds)
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
