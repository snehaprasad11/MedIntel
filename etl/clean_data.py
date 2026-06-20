import pandas as pd
import numpy as np

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
    clean_patients()
    clean_doctors()
    clean_departments()
    clean_appointments()

    print("All datasets cleaned successfully")


if __name__ == "__main__":
    main()

    