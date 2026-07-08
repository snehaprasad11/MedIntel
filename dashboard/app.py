import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from dashboard.core.theme import apply_theme

st.set_page_config(
    page_title="MedIntel Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme("light")

st.title("🏥 MedIntel Dashboard")
st.caption("A simulated hospital operations command center — six pages, each answering a different operational question, all built from the same underlying appointments/beds/forecast data.")
st.write("Select a page from the sidebar to get started 👈")

st.divider()

st.markdown("""
- **Executive** — the 30-second overview: today's headline numbers.
- **Analytics** — where is the load actually coming from (which departments, which doctors)?
- **Forecasting** — what does demand look like next, based on historical patterns?
- **Doctor** — who's overloaded and who has spare capacity?
- **Resources** — are we running out of physical beds?
- **AI** — a plain-English summary plus an automatic recommendation, generated from the same metrics.
""")
