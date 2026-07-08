import streamlit as st


def is_demo_mode():
    return st.session_state.get("mode") == "demo"


def get_current_hospital():
    return st.session_state.get("hospital")


def require_mode_selected():
    """Every page (other than the landing page) needs either demo mode
    or a logged-in hospital before it can render anything."""
    if not is_demo_mode() and get_current_hospital() is None:
        st.warning("Please go to the home page and choose **View Demo** or **log in** first.")
        st.stop()


def logout():
    st.session_state.pop("hospital", None)
    st.session_state.pop("mode", None)
