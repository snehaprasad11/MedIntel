import pandas as pd
from pathlib import Path

# =============================
# PROJECT ROOT
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================
# LOAD DATA
# =============================
appointments = pd.read_csv(BASE_DIR / "data" / "features" / "appointments_features.csv")
beds = pd.read_csv(BASE_DIR / "data" / "clean" / "beds.csv")
departments = pd.read_csv(BASE_DIR / "data" / "clean" / "departments.csv")

# =============================
# DATE FIX
# =============================
appointments["date"] = pd.to_datetime(appointments["date"])
beds["date"] = pd.to_datetime(beds["date"])

# =============================
# PATIENT ARRIVALS
# =============================
patient_arrivals = appointments.groupby("date", as_index=False).agg({
    "appointment_id": "count"
})
patient_arrivals.rename(columns={"appointment_id": "patient_arrivals"}, inplace=True)

# =============================
# BED DEMAND
# =============================
bed_demand = beds.groupby("date", as_index=False).agg({
    "occupied_beds": "mean"
})
bed_demand.rename(columns={"occupied_beds": "bed_demand"}, inplace=True)

# =============================
# ICU OCCUPANCY
# =============================
icu_occupancy = beds.groupby("date", as_index=False).agg({
    "occupied_icu_beds": "mean"
})
icu_occupancy.rename(columns={"occupied_icu_beds": "icu_occupancy"}, inplace=True)

# =============================
# DEPARTMENT LOAD
# =============================
dept_load = appointments.groupby("date", as_index=False).agg({
    "department_id": "count"
})
dept_load.rename(columns={"department_id": "dept_load"}, inplace=True)

# =============================
# MERGE ALL TABLES
# =============================
df = patient_arrivals \
    .merge(bed_demand, on="date", how="outer") \
    .merge(icu_occupancy, on="date", how="outer") \
    .merge(dept_load, on="date", how="outer")

# =============================
# SORT + CLEAN
# =============================
df = df.sort_values("date")

# fill missing values
df = df.fillna(0)

# =============================
# SAVE OUTPUT
# =============================
output_path = BASE_DIR / "data" / "features" / "forecast_dataset.csv"
df.to_csv(output_path, index=False)

print("✅ Forecast dataset created at:", output_path)
print(df.head())