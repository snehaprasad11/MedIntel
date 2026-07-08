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

def build_forecast_dataset(appointments_df):
    """Daily aggregates used to train the forecasting models: patient
    arrivals, bed demand, ICU occupancy, and department load. Beds data
    is merged in here so this stays the single source of truth for
    data/features/forecast_dataset.csv (previously duplicated, with a
    thinner version, by ml_models/data_prep.py)."""

    beds = pd.read_csv("data/clean/beds.csv")
    beds["date"] = pd.to_datetime(beds["date"]).dt.date

    patient_arrivals = appointments_df.groupby("date", as_index=False).agg(
        patient_arrivals=("appointment_id", "count")
    )
    bed_demand = beds.groupby("date", as_index=False).agg(bed_demand=("occupied_beds", "mean"))
    icu_occupancy = beds.groupby("date", as_index=False).agg(icu_occupancy=("occupied_icu_beds", "mean"))
    dept_load = appointments_df.groupby("date", as_index=False).agg(dept_load=("department_id", "count"))

    forecast_dataset = (
        patient_arrivals
        .merge(bed_demand, on="date", how="outer")
        .merge(icu_occupancy, on="date", how="outer")
        .merge(dept_load, on="date", how="outer")
        .sort_values("date")
        .fillna(0)
    )

    return forecast_dataset


def main():

    df = load_data()

    df = create_wait_time(df)
    df = create_time_features(df)
    df = doctor_load(df)
    df = department_load(df)
    df = daily_load(df)

    df.to_csv("data/features/appointments_features.csv", index=False)

    forecast_dataset = build_forecast_dataset(df)
    forecast_dataset.to_csv("data/features/forecast_dataset.csv", index=False)

    print("Feature engineering completed successfully")
    print("Note: data/features/prophet_forecast.csv and model_comparison.csv are produced separately by ml_models/")


if __name__ == "__main__":
    main()
