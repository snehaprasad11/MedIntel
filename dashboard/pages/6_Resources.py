import streamlit as st
from dashboard.core.data_loader import load_all_data
from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, get_latest_snapshots

apply_theme("light")
require_mode_selected()

st.title("🏥 Resource Utilization")
st.caption("Are we running out of physical beds — occupancy rate by department.")
st.divider()

if is_demo_mode():
    appointments, beds, forecast = load_all_data()

    beds["utilization"] = (beds["occupied_beds"] / beds["total_beds"]) * 100

    st.subheader("Bed Utilization by Department")
    st.caption("Occupied beds as a percentage of total beds, per department. Above ~85% is generally considered strained.")
    st.bar_chart(beds.set_index("department_id")["utilization"])

    st.divider()

    st.subheader("Raw Bed Data")
    st.dataframe(beds, use_container_width=True)

else:
    hospital = get_current_hospital()
    engine = get_engine()
    latest = get_latest_snapshots(engine, hospital["id"])

    if latest.empty:
        st.info("No data submitted yet. Go to **Submit Update** to enter your first department snapshot.")
        st.stop()

    latest["bed_utilization_pct"] = (latest["occupied_beds"] / latest["total_beds"] * 100).round(1)
    latest["icu_utilization_pct"] = (latest["occupied_icu_beds"] / latest["total_icu_beds"] * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("General Bed Utilization")
        st.caption("Above ~85% is generally considered strained.")
        st.bar_chart(latest.set_index("department_name")["bed_utilization_pct"])

    with col2:
        st.subheader("ICU Bed Utilization")
        st.bar_chart(latest.set_index("department_name")["icu_utilization_pct"])

    strained = latest[latest["bed_utilization_pct"] > 85]
    if not strained.empty:
        st.warning(f"{len(strained)} department(s) above 85% bed occupancy: {', '.join(strained['department_name'])}")

    st.divider()

    st.subheader("Latest Submission Detail")
    st.dataframe(
        latest[["department_name", "total_beds", "occupied_beds", "total_icu_beds",
                "occupied_icu_beds", "submitted_at"]],
        use_container_width=True,
        hide_index=True,
    )
