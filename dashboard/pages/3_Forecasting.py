import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📈 Forecasting")

BASE_DIR = Path(__file__).resolve().parents[2]
forecast = pd.read_csv(BASE_DIR / "data/features/prophet_forecast.csv")

st.line_chart(forecast["yhat"])

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)