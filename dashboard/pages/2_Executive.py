import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_latest_snapshots

apply_theme("light")
require_mode_selected()

st.title("🏥 Executive Overview")
st.caption("The 30-second read: today's headline numbers across the whole hospital, at a glance.")
st.divider()

if is_demo_mode():
    appointments, beds, forecast = load_all_data()

    total_appointments = len(appointments)
    avg_wait_time = appointments["wait_time_minutes"].mean()
    avg_beds = beds["occupied_beds"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Appointments", total_appointments)
    col2.metric("Avg Wait Time (min)", round(avg_wait_time, 2))
    col3.metric("Avg Beds Occupied", round(avg_beds, 2))

    st.divider()
    st.subheader("Recent Appointments")
    st.caption("A sample of the underlying appointment records these headline numbers are computed from.")
    st.dataframe(appointments.head(), use_container_width=True)

else:
    hospital = get_current_hospital()
    engine = get_engine()
    latest = get_latest_snapshots(engine, hospital["id"])

    if latest.empty:
        st.info("No data submitted yet. Go to **Submit Update** to enter your first department snapshot.")
        st.stop()

    latest["bed_occupancy_pct"] = latest["occupied_beds"] / latest["total_beds"] * 100
    latest["icu_occupancy_pct"] = latest["occupied_icu_beds"] / latest["total_icu_beds"] * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Departments Reporting", latest["department_name"].nunique())
    col2.metric("Avg Wait Time (min)", round(latest["avg_wait_time_minutes"].mean(), 1))
    col3.metric("Avg Bed Occupancy", f"{latest['bed_occupancy_pct'].mean():.1f}%")

    st.divider()
    st.subheader("Latest Snapshot by Department")
    st.caption("Most recent submission per department.")
    st.dataframe(
        latest[["department_name", "occupied_beds", "total_beds", "occupied_icu_beds",
                "total_icu_beds", "avg_wait_time_minutes", "submitted_at"]],
        use_container_width=True,
        hide_index=True,
    )
