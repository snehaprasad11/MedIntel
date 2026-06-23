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