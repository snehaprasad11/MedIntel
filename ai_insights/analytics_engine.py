import pandas as pd


def calculate_metrics(appointments, beds):

    metrics = {}

    metrics["total_appointments"] = len(appointments)

    metrics["avg_wait_time"] = round(
        appointments["wait_time_minutes"].mean(),
        2
    )

    metrics["avg_bed_occupancy"] = round(
        beds["occupied_beds"].mean(),
        2
    )

    metrics["avg_icu_occupancy"] = round(
        beds["occupied_icu_beds"].mean(),
        2
    )

    return metrics 
