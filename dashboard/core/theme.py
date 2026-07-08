import streamlit as st


def get_theme(mode="light"):

    if mode == "dark":
        return {
            "bg": "#1f2b29",
            "text": "#eafaf6",
            "card": "#2a3a37",
            "sidebar": "#18211f",
            "accent": "#7ec8e3"
        }

    return {
        "bg": "#cfe9e5",
        "text": "#1a1a1a",
        "card": "#ffffff",
        "sidebar": "#bfe0da",
        "accent": "#7ec8e3"
    }


DOODLE_SVG = """
<svg style="position: fixed; top: 70px; right: 40px; width: 90px; opacity: 0.5; z-index: 0; pointer-events: none;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 70 L70 20 M55 15 L70 20 L65 35" stroke="black" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M10 70 L20 55 M10 70 L28 66" stroke="black" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
<svg style="position: fixed; bottom: 40px; left: 30px; width: 70px; opacity: 0.5; z-index: 0; pointer-events: none;" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 50 Q 30 20, 50 50 T 90 50" stroke="black" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>
"""


def apply_theme(mode="light"):
    """Inject the theme as CSS. Call this at the top of every page -
    Streamlit runs each page as its own script, so a style block
    injected on one page is not guaranteed to persist when navigating
    to another."""

    theme = get_theme(mode)

    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&display=swap" rel="stylesheet">
        <style>
        .stApp {{
            background-color: {theme['bg']};
            background-image: radial-gradient(circle, rgba(0,0,0,0.12) 1.5px, transparent 1.5px);
            background-size: 22px 22px;
        }}
        .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div {{
            font-family: 'Baloo 2', 'Comic Sans MS', sans-serif;
            color: {theme['text']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {theme['sidebar']};
            border-right: 3px solid {theme['text']};
        }}
        [data-testid="stSidebar"] * {{
            color: {theme['text']};
            font-family: 'Baloo 2', 'Comic Sans MS', sans-serif;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1200px;
            position: relative;
            z-index: 1;
        }}
        h1, h2, h3 {{
            font-family: 'Baloo 2', 'Comic Sans MS', sans-serif !important;
            font-weight: 800;
            color: {theme['text']};
        }}
        h1 {{
            text-align: center;
            font-size: 3rem !important;
        }}
        [data-testid="stMetric"] {{
            background-color: {theme['card']};
            border: 3px solid {theme['text']};
            border-radius: 20px;
            padding: 1.2rem 1rem;
            box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.25);
        }}
        [data-testid="stMetricLabel"] {{
            font-weight: 700;
            color: {theme['text']};
        }}
        [data-testid="stMetricValue"] {{
            color: {theme['accent']};
            font-weight: 800;
        }}
        div[data-testid="column"] {{
            padding: 0 0.6rem;
        }}
        hr {{
            margin: 2rem 0;
            border: none;
            border-top: 3px dashed {theme['text']};
        }}
        .stButton button, .stFormSubmitButton button {{
            font-family: 'Baloo 2', 'Comic Sans MS', sans-serif;
            font-weight: 700;
            border-radius: 50px !important;
            border: 3px solid {theme['text']} !important;
            background-color: #ffd93d !important;
            color: {theme['text']} !important;
            box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.25);
        }}
        .stButton button:hover, .stFormSubmitButton button:hover {{
            background-color: #b5e550 !important;
            transform: translateY(-2px);
        }}
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            border: 3px solid {theme['text']};
            border-radius: 14px;
            overflow: hidden;
        }}
        [data-testid="stAlert"] {{
            border: 3px solid {theme['text']};
            border-radius: 16px;
        }}
        </style>
        {DOODLE_SVG}
        """,
        unsafe_allow_html=True,
    )

    return theme
