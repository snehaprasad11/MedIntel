import streamlit as st
import pandas as pd
from pathlib import Path

st.title("👨‍⚕️ Doctor Intelligence")

BASE_DIR = Path(__file__).resolve().parents[2]
df = pd.read_csv(BASE_DIR / "data/features/appointments_features.csv")

doc_perf = df.groupby("doctor_id").agg({
    "wait_time_minutes": "mean",
    "appointment_id": "count"
}).rename(columns={"appointment_id": "patients"})

st.dataframe(doc_perf)

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)