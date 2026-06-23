def summarize_kpis(metrics):
    summary = []

    for metric, value in metrics.items():
        if value > 0:
            summary.append(f"{metric} increased by {value}%")
        elif value < 0:
            summary.append(f"{metric} decreased by {abs(value)}%")
        else:
            summary.append(f"{metric} remained stable")

    return summary


if __name__ == "__main__":

    metrics = {
        "wait_time": 18,
        "patient_arrivals": 15,
        "doctor_availability": -10,
        "lab_delay": 5
    }

    results = summarize_kpis(metrics)

    print("\nKPI SUMMARY")

    for item in results:
        print("-", item)