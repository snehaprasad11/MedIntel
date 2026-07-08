import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from dashboard.core.theme import apply_theme
from dashboard.core.db import get_engine, create_hospital, verify_login
from dashboard.core.auth import is_demo_mode, get_current_hospital, logout

st.set_page_config(
    page_title="MedIntel Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme("light")

st.title("🏥 MedIntel Dashboard")
st.caption("A hospital operations command center — live bed/ICU/staff tracking, department analytics, and demand forecasting.")
st.divider()

hospital = get_current_hospital()

if is_demo_mode():
    st.success("You're viewing **demo data** — six years of simulated hospital activity. No login needed; select a page from the sidebar.")
    if st.button("Log out of demo"):
        logout()
        st.rerun()

elif hospital:
    st.success(f"Logged in as **{hospital['name']}**. Select a page from the sidebar — data entry and dashboards are scoped to your hospital only.")
    if st.button("Log out"):
        logout()
        st.rerun()

else:
    st.write("Choose how you'd like to use MedIntel:")

    demo_tab, login_tab, signup_tab = st.tabs(["👀 View Demo", "🔐 Log In", "🆕 Sign Up"])

    with demo_tab:
        st.write("Explore the dashboard with realistic simulated data — no account needed.")
        if st.button("View Demo", type="primary"):
            st.session_state["mode"] = "demo"
            st.rerun()

    with login_tab:
        st.write("For hospitals that have already signed up.")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", type="primary")

        if submitted:
            engine = get_engine()
            user = verify_login(engine, email, password)
            if user:
                st.session_state["hospital"] = user
                st.session_state["mode"] = "live"
                st.rerun()
            else:
                st.error("Incorrect email or password.")

    with signup_tab:
        st.write("Register your hospital to start submitting live bed/ICU/staff data.")
        with st.form("signup_form"):
            name = st.text_input("Hospital name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Sign Up", type="primary")

        if submitted:
            if not name.strip() or not email.strip():
                st.error("Hospital name and email are required.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters.")
            elif password != confirm_password:
                st.error("Passwords don't match.")
            else:
                engine = get_engine()
                ok, message = create_hospital(engine, name.strip(), email.strip(), password)
                if ok:
                    st.success(f"{message} You can now log in from the **Log In** tab.")
                else:
                    st.error(message)
