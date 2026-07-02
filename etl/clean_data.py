import pandas as pd
import numpy as np
from pathlib import Path

def clean_patients():
    df = pd.read_csv("data/synthetic/patients.csv")

    # Remove duplicates
    df = df.drop_duplicates(subset=["patient_id"])

    # Age validation
    df = df[(df["age"] >= 0) & (df["age"] <= 120)]

    # Handle missing values (if any)
    df["name"] = df["name"].fillna("Unknown")
    df["city"] = df["city"].fillna("Unknown")

    df.to_csv("data/clean/patients.csv", index=False)
    print("Patients cleaned")

def clean_beds():
    df = pd.read_csv("data/synthetic/beds.csv")

    df = df.drop_duplicates()

    df = df[
        (df["total_beds"] > 0)
    ]

    df = df[
        (df["occupied_beds"] >= 0)
        &
        (df["occupied_beds"] <= df["total_beds"])
        &
        (df["occupied_icu_beds"] >= 0)
        &
        (df["occupied_icu_beds"] <= df["icu_beds"])
    ]

    df.to_csv("data/clean/beds.csv",
        index=False)

    print("Beds cleaned")

def clean_staff():

    df = pd.read_csv("data/synthetic/staff.csv")

    df = df.drop_duplicates()

    df = df[
        (df["doctors_scheduled"] > 0)
        &
        (df["nurses_scheduled"] > 0)
        &
        (df["support_staff_scheduled"] > 0)
    ]

    df = df[
        (df["doctors_present"] <= df["doctors_scheduled"])
        &
        (df["nurses_present"] <= df["nurses_scheduled"])
        &
        (
            df["support_staff_present"]
            <=
            df["support_staff_scheduled"]
        )
    ]

    df.to_csv(
        "data/clean/staff.csv",
        index=False
    )

    print("Staff cleaned")

def clean_equipment():

    df = pd.read_csv("data/synthetic/equipment.csv")

    df = df.drop_duplicates()

    df = df[
        (df["total_units"] > 0)
    ]

    df = df[
        (df["units_in_use"] >= 0)
        &
        (df["units_in_use"] <= df["total_units"])
    ]

    df.to_csv(
        "data/clean/equipment.csv",
        index=False
    )

    print("Equipment cleaned")

def clean_doctors():
    df = pd.read_csv("data/synthetic/doctors.csv")

    df = df.drop_duplicates(subset=["doctor_id"])

    df["doctor_name"] = df["doctor_name"].fillna("Unknown")
    df["specialty"] = df["specialty"].fillna("General Medicine")

    df.to_csv("data/clean/doctors.csv", index=False)
    print("Doctors cleaned")

def clean_departments():
    df = pd.read_csv("data/synthetic/departments.csv")

    df = df.drop_duplicates(subset=["department_id"])

    df["department_name"] = df["department_name"].fillna("Unknown")

    df.to_csv("data/clean/departments.csv", index=False)
    print("Departments cleaned")

def clean_appointments():
    df = pd.read_csv("data/synthetic/appointments.csv")

    # Remove duplicates
    df = df.drop_duplicates(subset=["appointment_id"])

    # Remove invalid foreign keys
    df = df[
        (df["patient_id"] > 0) &
        (df["doctor_id"] > 0) &
        (df["department_id"] > 0)
    ]

    # Convert datetime columns
    df["arrival_time"] = pd.to_datetime(df["arrival_time"])
    df["consultation_time"] = pd.to_datetime(df["consultation_time"])

    # Remove invalid time logic
    df = df[df["consultation_time"] >= df["arrival_time"]]

    # Add derived cleaning flag (useful later)
    df["is_valid"] = 1

    df.to_csv("data/clean/appointments.csv", index=False)
    print("Appointments cleaned")

def main():
    Path("data/clean").mkdir(parents=True, exist_ok=True)

    clean_patients()
    clean_doctors()
    clean_departments()
    clean_appointments()
    clean_beds()
    clean_staff()
    clean_equipment()

    print("All datasets cleaned successfully")


if __name__ == "__main__":
    main()
