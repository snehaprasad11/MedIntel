import streamlit as st
import pandas as pd
from pathlib import Path
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_snapshot_history
from ml_models.anamoly_detector import detect_wait_time_anomalies

apply_theme("light")
require_mode_selected()

if is_demo_mode():
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

else:
    st.title("🚩 Department Wait Time Anomalies")
    st.caption("This page tracks doctors individually in demo mode — live submissions are department-level, so this checks each department's submission history for unusually high wait times instead.")
    st.divider()

    hospital = get_current_hospital()
    engine = get_engine()
    history = get_snapshot_history(engine, hospital["id"])

    if history.empty:
        st.info("No data submitted yet. Go to **Submit Update** to enter your first department snapshot.")
        st.stop()

    if len(history) < 5:
        st.info(f"Only {len(history)} submission(s) so far — anomaly detection needs a few more data points to know what 'unusual' looks like for your hospital.")
        st.stop()

    history_renamed = history.rename(columns={"avg_wait_time_minutes": "wait_time_minutes"})
    flagged = detect_wait_time_anomalies(history_renamed)
    anomalies = flagged[flagged["anomaly"]]

    st.subheader("Flagged Submissions")
    st.caption(f"Submissions where the average wait time exceeded your hospital's own mean by more than 2 standard deviations — {len(anomalies)} out of {len(history)} submissions.")

    if len(anomalies) > 0:
        st.dataframe(
            anomalies[["department_name", "avg_wait_time_minutes", "submitted_at"]].sort_values("avg_wait_time_minutes", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No anomalous wait times detected in your submission history.")
