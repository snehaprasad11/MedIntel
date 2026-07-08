import streamlit as st
import pandas as pd
from pathlib import Path
from dashboard.core.theme import apply_theme

apply_theme("light")

st.title("👨‍⚕️ Doctor Intelligence")
st.caption("Who's overloaded and who has spare capacity — average wait time and patient count per doctor.")
st.divider()

BASE_DIR = Path(__file__).resolve().parents[2]
df = pd.read_csv(BASE_DIR / "data/features/appointments_features.csv")

doc_perf = df.groupby("doctor_id").agg({
    "wait_time_minutes": "mean",
    "appointment_id": "count"
}).rename(columns={"appointment_id": "patients"})

st.subheader("Performance by Doctor")
st.caption("Sorted by doctor ID — higher average wait time paired with a high patient count signals an overloaded doctor.")
st.dataframe(doc_perf, use_container_width=True)
