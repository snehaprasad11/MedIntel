def generate_recommendation(metrics):
    """
    Generates operational recommendations
    based on KPI changes.
    """

    wait_time = metrics.get("wait_time_change", 0)
    arrivals = metrics.get("patient_arrivals_change", 0)
    doctors = metrics.get("doctor_availability_change", 0)
    lab = metrics.get("lab_delay_change", 0)

    if wait_time > 10 and doctors < -5:
        recommendation = (
            "Increase physician coverage during peak hours "
            "to reduce patient backlog."
        )

    elif arrivals > 10:
        recommendation = (
            "Scale up front desk and triage capacity "
            "to handle growing patient demand."
        )

    elif lab >= 5:
        recommendation = (
            "Review laboratory workflow and staffing "
            "to reduce turnaround times."
        )

    else:
        recommendation = (
            "System operating within acceptable limits."
        )

    return recommendation


if __name__ == "__main__":

    sample_metrics = {
        "wait_time_change": 18,
        "patient_arrivals_change": 15,
        "doctor_availability_change": -10,
        "lab_delay_change": 5
    }

    result = generate_recommendation(sample_metrics)

    print("\nRECOMMENDATION:")
    print(result)