def generate_recommendation(metrics):
    """
    Generates an operational recommendation from the current
    snapshot metrics (average wait time, bed occupancy, ICU
    occupancy) produced by analytics_engine.calculate_metrics().
    """

    avg_wait_time = metrics.get("avg_wait_time", 0)
    avg_bed_occupancy = metrics.get("avg_bed_occupancy", 0)
    avg_icu_occupancy = metrics.get("avg_icu_occupancy", 0)

    if avg_icu_occupancy > 80:
        recommendation = (
            f"ICU occupancy is averaging {avg_icu_occupancy}% — "
            "review ICU capacity and step-down transfer options before it becomes a bottleneck."
        )

    elif avg_bed_occupancy > 85:
        recommendation = (
            f"General bed occupancy is averaging {avg_bed_occupancy}% — "
            "review discharge planning and consider scaling ward capacity."
        )

    elif avg_wait_time > 45:
        recommendation = (
            f"Average patient wait time is {avg_wait_time} minutes — "
            "increase physician coverage during peak hours and expand triage staffing to reduce backlog."
        )

    else:
        recommendation = (
            f"Average wait time ({avg_wait_time} min) and bed occupancy ({avg_bed_occupancy}%) "
            "are both within acceptable limits — no immediate action needed."
        )

    return recommendation


if __name__ == "__main__":

    sample_metrics = {
        "avg_wait_time": 62.4,
        "avg_bed_occupancy": 77.1,
        "avg_icu_occupancy": 60.0,
    }

    result = generate_recommendation(sample_metrics)

    print("\nRECOMMENDATION:")
    print(result)
