from ai_insights.analytics_engine import calculate_metrics
from ai_insights.openai_insights import generate_llm_insight
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="MedIntel",
    page_icon="🏥",
    layout="wide"
)

# ==========================================
# PROJECT ROOT
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# LOAD DATA
# ==========================================

appointments = pd.read_csv(
    BASE_DIR / "data" / "features" / "appointments_features.csv"
)

beds = pd.read_csv(
    BASE_DIR / "data" / "clean" / "beds.csv"
)

forecast = pd.read_csv(
    BASE_DIR / "data" / "features" / "prophet_forecast.csv"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    BASE_DIR / "assets" / "medintel_logo.png",
    width=180
)

st.sidebar.title("MedIntel")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Forecasting",
        "AI Insights"
    ]
)

# ==========================================
# COMMON HEADER
# ==========================================

col1, col2 = st.columns([1, 6])

with col1:
    st.image(
        BASE_DIR / "assets" / "medintel_logo.png",
        width=90
    )

with col2:
    st.title("MedIntel")
    st.caption(
        "AI-Powered Hospital Operations Intelligence"
    )

st.markdown("---")

# ==========================================
# EXECUTIVE OVERVIEW
# ==========================================

if page == "Executive Overview":

    st.header("Executive Overview")

    total_appointments = len(appointments)

    avg_wait_time = round(
        appointments["wait_time_minutes"].mean(),
        2
    )

    avg_bed_occupancy = round(
        beds["occupied_beds"].mean(),
        2
    )

    avg_icu_occupancy = round(
        beds["occupied_icu_beds"].mean(),
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Appointments",
        total_appointments
    )

    c2.metric(
        "Average Wait Time (min)",
        avg_wait_time
    )

    c3.metric(
        "Average Bed Occupancy (%)",
        avg_bed_occupancy
    )

    c4.metric(
        "Average ICU Occupancy (%)",
        avg_icu_occupancy
    )

    st.markdown("---")

    st.subheader("About MedIntel")

    st.write(
        """
        MedIntel is an AI-powered healthcare analytics platform
        designed to improve hospital operations through
        business intelligence, forecasting, and AI-driven insights.

        Key Features:

        • Healthcare KPI Monitoring

        • Operational Analytics

        • Patient Demand Forecasting

        • AI-Powered Recommendations

        • Executive Decision Support
        """
    )

# ==========================================
# FORECASTING
# ==========================================

elif page == "Forecasting":

    st.header("Forecasting")

    st.subheader(
        "Patient Arrival Forecast"
    )

    forecast["ds"] = pd.to_datetime(
        forecast["ds"]
    )

    forecast = forecast.set_index("ds")

    st.line_chart(
        forecast["yhat"]
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Expected Daily Arrivals",
        round(forecast["yhat"].mean(), 2)
    )

    c2.metric(
        "Maximum Forecast",
        round(forecast["yhat"].max(), 2)
    )

    c3.metric(
        "Minimum Forecast",
        round(forecast["yhat"].min(), 2)
    )

    st.markdown("---")

    st.write(
        """
        Prophet forecasting predicts future patient demand
        based on historical appointment patterns.
        This enables hospital administrators to plan
        staffing, resource allocation, and capacity
        requirements more effectively.
        """
    )

# ==========================================
# AI INSIGHTS
# ==========================================

elif page == "AI Insights":

    st.header("AI Insights")

    metrics = calculate_metrics(
        appointments,
        beds
    )

    result = generate_llm_insight(
        metrics
    )

    st.subheader(
        "Executive Summary"
    )

    st.write(
        result["executive_summary"]
    )

    st.markdown("---")

    st.subheader(
        "Recommendation"
    )

    st.write(
        result["recommendation"]
    )