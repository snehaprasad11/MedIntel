import streamlit as st

from dashboard.core.theme import apply_theme
from dashboard.core.auth import require_mode_selected, is_demo_mode, get_current_hospital
from dashboard.core.db import get_engine, submit_snapshot, get_latest_snapshots

apply_theme("light")
require_mode_selected()

st.title("📝 Submit Update")
st.caption("Enter your department's current numbers. Each submission is timestamped and becomes part of your hospital's live history.")
st.divider()

if is_demo_mode():
    st.info("You're in demo mode, which is read-only. Log in as a real hospital (from the home page) to submit live data.")
    st.stop()

hospital = get_current_hospital()
engine = get_engine()

with st.form("submit_update_form"):
    department_name = st.text_input("Department name", placeholder="e.g. Cardiology, Emergency, ICU")

    col1, col2 = st.columns(2)
    with col1:
        total_beds = st.number_input("Total beds", min_value=0, step=1, value=50)
        occupied_beds = st.number_input("Occupied beds", min_value=0, step=1, value=30)
        total_icu_beds = st.number_input("Total ICU beds", min_value=0, step=1, value=10)
        occupied_icu_beds = st.number_input("Occupied ICU beds", min_value=0, step=1, value=5)
    with col2:
        doctors_scheduled = st.number_input("Doctors scheduled", min_value=0, step=1, value=10)
        doctors_present = st.number_input("Doctors present", min_value=0, step=1, value=9)
        nurses_scheduled = st.number_input("Nurses scheduled", min_value=0, step=1, value=25)
        nurses_present = st.number_input("Nurses present", min_value=0, step=1, value=22)

    avg_wait_time_minutes = st.number_input("Average patient wait time today (minutes)", min_value=0.0, step=1.0, value=30.0)

    submitted = st.form_submit_button("Submit Update", type="primary")

if submitted:
    ok, message = submit_snapshot(
        engine, hospital["id"], department_name,
        total_beds, occupied_beds, total_icu_beds, occupied_icu_beds,
        doctors_scheduled, doctors_present, nurses_scheduled, nurses_present,
        avg_wait_time_minutes,
    )
    if ok:
        st.success(message)
    else:
        st.error(message)

st.divider()

st.subheader("Your Departments' Latest Numbers")
latest = get_latest_snapshots(engine, hospital["id"])
if latest.empty:
    st.info("No submissions yet — the form above is your first.")
else:
    st.dataframe(
        latest.drop(columns=["id", "hospital_id"]),
        use_container_width=True,
        hide_index=True,
    )
