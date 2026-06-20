from faker import Faker
import pandas as pd
import random

fake = Faker()

patients = []

for patient_id in range(1,100001):

    patients.append({
        "patient_id": patient_id,
        "name": fake.name(),
        "age": random.randint(1,90),
        "gender": random.choice(["Male","Female"]),
        "city": fake.city()
    })

patients_df = pd.DataFrame(patients)

patients_df.to_csv(
    "data/synthetic/patients.csv",
    index=False
)

print("Patients generated")

departments = []

for department_id in range(1, 51):

    departments.append({
        "department_id": department_id,
        "department_name": f"Department_{department_id}"
    })

departments_df = pd.DataFrame(departments)

departments_df.to_csv(
    "data/synthetic/departments.csv",
    index=False
)

print("Departments generated")

specialties = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Pediatrics",
    "Emergency",
    "Dermatology",
    "Oncology",
    "Radiology",
    "General Medicine",
    "ENT"
]

doctors = []

for doctor_id in range(1, 501):

    doctors.append({
        "doctor_id": doctor_id,
        "doctor_name": fake.name(),
        "specialty": random.choice(specialties),
        "department_id": random.randint(1, 50)
    })

doctors_df = pd.DataFrame(doctors)

doctors_df.to_csv(
    "data/synthetic/doctors.csv",
    index=False
)

print("Doctors generated")