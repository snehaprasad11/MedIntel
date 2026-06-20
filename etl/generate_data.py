from faker import Faker
import pandas as pd
import random 
from datetime import datetime
from datetime import timedelta
def main():
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

    appointments = [] 
    start_date = datetime(2020, 1, 1)

    end_date = datetime(2025, 12, 31)
    for appointment_id in range(1,100001):
        appointment_date = start_date + timedelta(
        days=random.randint(
        0,
        (end_date-start_date).days
        )
    )
        patient_id = random.randint(1,100000)
        doctor_id = random.randint(1,500)
        department_id = random.randint(1,50)
        arrival_hour = random.choices(
        [8,9,10,11,12,13,14,15,16,17],
        weights=[15,15,15,15,10,8,8,6,4,4]
    )[0]
    arrival_minute = random.randint(0,59)
    arrival_time = datetime(
    appointment_date.year,
    appointment_date.month,
    appointment_date.day,
    arrival_hour,
    arrival_minute
)
    wait_minutes = random.randint(5,120)
    consultation_time = (
    arrival_time +
    timedelta(minutes=wait_minutes)
)
    appointments.append({

    "appointment_id": appointment_id,

    "patient_id": patient_id,

    "doctor_id": doctor_id,

    "department_id": department_id,

    "appointment_date": appointment_date.date(),

    "arrival_time": arrival_time,

    "consultation_time": consultation_time
})
    appointments_df = pd.DataFrame(
    appointments
)
    appointments_df.to_csv(
    "data/synthetic/appointments.csv",
    index=False
)
    print("Appointments generated")

if __name__ == "__main__":
    main()

