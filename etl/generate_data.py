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