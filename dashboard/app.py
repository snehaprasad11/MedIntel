import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

st.set_page_config(
    page_title="MedIntel Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏥 MedIntel Dashboard")
st.write("Select a page from sidebar 👈")