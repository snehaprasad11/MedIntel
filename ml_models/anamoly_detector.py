import pandas as pd

def detect_wait_time_anomalies(df):

    threshold = df["wait_time_minutes"].mean() + 2 * df["wait_time_minutes"].std()

    df["anomaly"] = df["wait_time_minutes"] > threshold

    return df