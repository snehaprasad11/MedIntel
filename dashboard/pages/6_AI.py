import streamlit as st
import pandas as pd

from dashboard.core.data_loader import load_all_data
from ai_insights.analytics_engine import calculate_metrics
from ai_insights.openai_insights import generate_llm_insight


# =========================
# LOAD DATA (CACHED IN CORE)
# =========================
appointments, beds, forecast = load_all_data()

st.title("🤖 AI Insights Engine")

st.info("Generating AI insights...")


# =========================
# METRICS ENGINE
# =========================
metrics = calculate_metrics(appointments, beds)


# =========================
# AI INSIGHTS
# =========================
result = generate_llm_insight(metrics)


# =========================
# SAFETY CHECK (IMPORTANT)
# =========================
if isinstance(result, dict):
    executive = result.get("executive_summary", "No summary generated")
    recommendation = result.get("recommendation", "No recommendation generated")
else:
    executive = str(result)
    recommendation = "Recommendation unavailable"


# =========================
# UI LAYOUT
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Executive Summary")
    st.success(executive)

with col2:
    st.subheader("Recommendations")
    st.warning(recommendation)