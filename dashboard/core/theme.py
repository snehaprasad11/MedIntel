import streamlit as st


def get_theme(mode="light"):

    if mode == "dark":
        return {
            "bg": "#1a1815",
            "text": "#e8e3d8",
            "card": "#242019",
            "sidebar": "#151310",
            "accent": "#c9302c"
        }

    return {
        "bg": "#f4f0e6",
        "text": "#1a1a1a",
        "card": "#faf8f2",
        "sidebar": "#ede8d9",
        "accent": "#8b0000"
    }


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
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
        <style>
        @keyframes paperShift {{
            0%   {{ background-position: 0% 0%; }}
            50%  {{ background-position: 100% 100%; }}
            100% {{ background-position: 0% 0%; }}
        }}
        .stApp {{
            background: linear-gradient(120deg, {theme['bg']} 0%, {theme['card']} 40%, {theme['bg']} 70%, {theme['card']} 100%);
            background-size: 400% 400%;
            animation: paperShift 25s ease infinite;
        }}
        .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div {{
            font-family: 'Lora', Georgia, serif;
            color: {theme['text']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {theme['sidebar']};
            border-right: 3px double {theme['text']};
        }}
        [data-testid="stSidebar"] * {{
            color: {theme['text']};
            font-family: 'Lora', Georgia, serif;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1200px;
        }}
        h1, h2, h3 {{
            font-family: 'Playfair Display', Georgia, serif !important;
            color: {theme['text']};
        }}
        h1 {{
            font-weight: 900;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-top: 4px double {theme['text']};
            border-bottom: 4px double {theme['text']};
            padding: 0.6rem 0;
            margin-bottom: 0.5rem !important;
        }}
        h2, h3 {{
            font-weight: 700;
            border-bottom: 1px solid {theme['text']};
            padding-bottom: 0.2rem;
        }}
        [data-testid="stCaptionContainer"] {{
            font-style: italic;
            text-align: center;
        }}
        [data-testid="stMetric"] {{
            background-color: {theme['card']};
            border: 1px solid {theme['text']};
            border-radius: 0;
            padding: 1.2rem 1rem;
            box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.15);
        }}
        [data-testid="stMetricLabel"] {{
            font-family: 'Playfair Display', Georgia, serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {theme['text']};
        }}
        [data-testid="stMetricValue"] {{
            font-family: 'Playfair Display', Georgia, serif;
            color: {theme['accent']};
        }}
        div[data-testid="column"] {{
            padding: 0 0.6rem;
        }}
        hr {{
            margin: 2rem 0;
            border: none;
            border-top: 3px double {theme['text']};
        }}
        .stButton button, .stFormSubmitButton button {{
            font-family: 'Playfair Display', Georgia, serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-radius: 0;
            border: 2px solid {theme['text']};
            background-color: {theme['accent']};
            color: {theme['card']};
        }}
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            border: 1px solid {theme['text']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    return theme
