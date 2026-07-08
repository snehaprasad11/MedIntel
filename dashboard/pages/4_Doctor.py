import streamlit as st
import pandas as pd
from pathlib import Path
from dashboard.core.theme import apply_theme
from ml_models.anamoly_detector import detect_wait_time_anomalies

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

st.divider()

df_flagged = detect_wait_time_anomalies(df)
anomalies = df_flagged[df_flagged["anomaly"]]

st.subheader("Anomalous Wait Times")
st.caption(f"Appointments where the wait time exceeded the mean by more than 2 standard deviations — {len(anomalies):,} out of {len(df):,} appointments ({len(anomalies) / len(df) * 100:.1f}%).")

if len(anomalies) > 0:
    worst = anomalies.sort_values("wait_time_minutes", ascending=False).head(20)
    st.dataframe(
        worst[["appointment_id", "doctor_id", "department_id", "wait_time_minutes"]],
        use_container_width=True,
    )
else:
    st.success("No anomalous wait times detected.")
