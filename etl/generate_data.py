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

    beds = []

    current_date = start_date

    while current_date <= end_date:

        for department_id in range(1, 51):

            total_beds = random.randint(50, 150)

            occupied_beds = int(
            total_beds * random.uniform(0.6, 0.95)
        )
            icu_beds = int(total_beds * 0.15)
            occupied_icu_beds = int(
                icu_beds * random.uniform(0.5, 0.95))
            
            beds.append({
            "date": current_date.date(),
            "department_id": department_id,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "icu_beds": icu_beds,
            "occupied_icu_beds": occupied_icu_beds
        })

        current_date += timedelta(days=1)

    beds_df = pd.DataFrame(beds)

    beds_df.to_csv(
    "data/synthetic/beds.csv",
    index=False
    )

    print("Beds generated")

    staff = []

    current_date = start_date

    while current_date <= end_date:

        for department_id in range(1, 51):

            doctors_scheduled = random.randint(5, 20)

            doctors_present = random.randint(
            int(doctors_scheduled * 0.8),
            doctors_scheduled
            )

            nurses_scheduled = random.randint(15, 50)

            nurses_present = random.randint(
            int(nurses_scheduled * 0.8),
            nurses_scheduled
            )

            support_staff_scheduled = random.randint(10, 40)

            support_staff_present = random.randint(
            int(support_staff_scheduled * 0.8),
            support_staff_scheduled
            )

            staff.append({
            "date": current_date.date(),
            "department_id": department_id,
            "doctors_scheduled": doctors_scheduled,
            "doctors_present": doctors_present,
            "nurses_scheduled": nurses_scheduled,
            "nurses_present": nurses_present,
            "support_staff_scheduled": support_staff_scheduled,
            "support_staff_present": support_staff_present
        })

            current_date += timedelta(days=1)

    staff_df = pd.DataFrame(staff)

    staff_df.to_csv(
    "data/synthetic/staff.csv",
    index=False
    )

    print("Staff generated")

    equipment_types = [
    "MRI",
    "CT Scanner",
    "X-Ray",
    "Ventilator",
    "Ultrasound",
    "ECG"
    ]

    equipment = []

    current_date = start_date
    while current_date <= end_date:

        for department_id in range(1, 51):

            for equipment_type in equipment_types:

                total_units = random.randint(1, 10)

                units_in_use = random.randint(
                0,
                total_units
                )

                utilization_pct = round(
                (units_in_use / total_units) * 100,
                2
                )

                equipment.append({
                "date": current_date.date(),
                "department_id": department_id,
                "equipment_type": equipment_type,
                "total_units": total_units,
                "units_in_use": units_in_use,
                "utilization_pct": utilization_pct
                })

        current_date += timedelta(days=1)
    equipment_df = pd.DataFrame(equipment)

    equipment_df.to_csv(
    "data/synthetic/equipment.csv",
    index=False
    )

    print("Equipment generated")
if __name__ == "__main__":
    main()

