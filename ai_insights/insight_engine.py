import os

# =============================
# SIMPLE AI INSIGHT ENGINE
# =============================

def generate_operational_insights(metrics: dict):
    """
    Converts hospital KPIs into executive-level insights.
    """

    insights = []

    # Extract KPIs
    wait_time = metrics.get("wait_time_change", 0)
    arrivals = metrics.get("patient_arrivals_change", 0)
    doctors = metrics.get("doctor_availability_change", 0)
    lab = metrics.get("lab_delay_change", 0)

    # =============================
    # RULE-BASED ANALYTICS ENGINE
    # =============================

    if wait_time > 10:
        insights.append("Wait time significantly increased, indicating system overload.")

    if arrivals > 10:
        insights.append("Patient arrivals are rising, increasing operational pressure.")

    if doctors < -5:
        insights.append("Doctor availability has dropped, causing staffing imbalance.")

    if lab >=5:
        insights.append("Lab delays are increasing turnaround time.")

    # =============================
    # FINAL RECOMMENDATION ENGINE
    # =============================

    if wait_time > 10 and doctors < -5:
        recommendation = "Increase physician coverage during peak hours to reduce patient backlog."
    elif arrivals > 10:
        recommendation = "Scale up front desk and triage capacity."
    else:
        recommendation = "System operating within acceptable limits."

    return {
        "insights": insights,
        "recommendation": recommendation
    }


# =============================
# SAMPLE RUN
# =============================
if __name__ == "__main__":
    sample_metrics = {
        "wait_time_change": 18,
        "patient_arrivals_change": 15,
        "doctor_availability_change": -10,
        "lab_delay_change": 5
    }

    result = generate_operational_insights(sample_metrics)

    print("\nINSIGHTS:")
    for i in result["insights"]:
        print("-", i)

    print("\nRECOMMENDATION:")
    print(result["recommendation"])