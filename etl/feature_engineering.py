import pandas as pd
import numpy as np
from pathlib import Path

Path("data/features").mkdir(parents=True, exist_ok=True)

def load_data():
    df = pd.read_csv("data/clean/appointments.csv")

    df["arrival_time"] = pd.to_datetime(df["arrival_time"])
    df["consultation_time"] = pd.to_datetime(df["consultation_time"])

    return df

def create_wait_time(df):
    df["wait_time_minutes"] = (
        df["consultation_time"] - df["arrival_time"]
    ).dt.total_seconds() / 60

    return df

def create_time_features(df):
    df["arrival_hour"] = df["arrival_time"].dt.hour
    df["day_of_week"] = df["arrival_time"].dt.day_name()

    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)

    return df

def doctor_load(df):
    doc_load = df.groupby("doctor_id").size().reset_index(name="doctor_appointments")

    df = df.merge(doc_load, on="doctor_id", how="left")

    return df

def department_load(df):
    dept_load = df.groupby("department_id").size().reset_index(name="department_appointments")

    df = df.merge(dept_load, on="department_id", how="left")

    return df

def daily_load(df):
    daily = df.groupby(df["arrival_time"].dt.date).size().reset_index(name="daily_appointments")

    daily.columns = ["date", "daily_appointments"]

    df["date"] = df["arrival_time"].dt.date

    df = df.merge(daily, on="date", how="left")

    return df

def main():

    df = load_data()

    df = create_wait_time(df)
    df = create_time_features(df)
    df = doctor_load(df)
    df = department_load(df)
    df = daily_load(df)

    df.to_csv("data/features/appointments_features.csv", index=False)

    forecast_dataset = (
        df.groupby("date", as_index=False)
        .agg(patient_arrivals=("appointment_id", "count"))
        .sort_values("date")
    )
    forecast_dataset.to_csv("data/features/forecast_dataset.csv", index=False)

    fallback_forecast = forecast_dataset.rename(
        columns={"date": "ds", "patient_arrivals": "yhat"}
    )
    fallback_forecast.to_csv("data/features/prophet_forecast.csv", index=False)

    print("Feature engineering completed successfully")


if __name__ == "__main__":
    main()
