import streamlit as st


def get_theme(mode="light"):

    if mode == "dark":
        return {
            "bg": "#0B1220",
            "text": "#E5E7EB",
            "card": "#111827",
            "sidebar": "#0F172A",
            "accent": "#60A5FA"
        }

    return {
        "bg": "#F8FAFC",
        "text": "#0F172A",
        "card": "#FFFFFF",
        "sidebar": "#FFFFFF",
        "accent": "#2563EB"
    }


def apply_theme(mode="light"):
    """Inject the theme as CSS. Call this at the top of every page -
    Streamlit runs each page as its own script, so a style block
    injected on one page is not guaranteed to persist when navigating
    to another."""

    theme = get_theme(mode)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {theme['bg']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {theme['sidebar']};
            border-right: 1px solid #E2E8F0;
        }}
        [data-testid="stSidebar"] * {{
            color: {theme['text']};
        }}
        .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1200px;
        }}
        h1, h2, h3 {{
            color: {theme['text']};
        }}
        [data-testid="stMetric"] {{
            background-color: {theme['card']};
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.2rem 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
        }}
        [data-testid="stMetricLabel"] {{
            color: #64748B;
        }}
        [data-testid="stMetricValue"] {{
            color: {theme['accent']};
        }}
        div[data-testid="column"] {{
            padding: 0 0.6rem;
        }}
        hr {{
            margin: 2rem 0;
            border-color: #E2E8F0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return theme
