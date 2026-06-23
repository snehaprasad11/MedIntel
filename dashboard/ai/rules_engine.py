def generate_alerts(risk_map):

    alerts = []

    for dept, status in risk_map.items():

        if status == "HIGH RISK":
            alerts.append(f"⚠ Department {dept} may overload in 3 days")

    return alerts