import pandas as pd
import mysql.connector

# =========================
# 1. CONNECTION
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="medintel"
    )

# =========================
# 2. SAFE INSERT
# =========================
def insert_data(df, table_name, conn):
    cursor = conn.cursor()

    df = df.astype(object).where(pd.notnull(df), None)

    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))

    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    cursor.executemany(query, df.values.tolist())

    conn.commit()
    cursor.close()

# =========================
# 3. CLEAR TABLES
# =========================
def clear_tables(conn):
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    cursor.execute("TRUNCATE TABLE appointments_features")
    cursor.execute("TRUNCATE TABLE doctors")
    cursor.execute("TRUNCATE TABLE departments")
    cursor.execute("TRUNCATE TABLE patients")
    cursor.execute("TRUNCATE TABLE beds")
    cursor.execute("TRUNCATE TABLE staff")
    cursor.execute("TRUNCATE TABLE equipment")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    conn.commit()
    cursor.close()

    print("Old data cleared")

# =========================
# 4. MAIN PIPELINE
# =========================
def main():

    conn = get_connection()
    clear_tables(conn)

    # -------------------------
    # LOAD CSVs
    # -------------------------
    patients = pd.read_csv("data/clean/patients.csv")
    doctors = pd.read_csv("data/clean/doctors.csv")
    departments = pd.read_csv("data/clean/departments.csv")
    appointments = pd.read_csv("data/features/appointments_features.csv")

    beds = pd.read_csv("data/clean/beds.csv")
    staff = pd.read_csv("data/clean/staff.csv")
    equipment = pd.read_csv("data/clean/equipment.csv")

    # -------------------------
    # TYPE CLEANING (IMPORTANT)
    # -------------------------
    patients["patient_id"] = patients["patient_id"].astype(int)

    doctors["doctor_id"] = doctors["doctor_id"].astype(int)
    doctors["department_id"] = doctors["department_id"].astype(int)

    departments["department_id"] = departments["department_id"].astype(int)

    beds["department_id"] = beds["department_id"].astype(int)
    staff["department_id"] = staff["department_id"].astype(int)
    equipment["department_id"] = equipment["department_id"].astype(int)

    # -------------------------
    # FIX FK ISSUE (CRITICAL)
    # -------------------------
    doctors = doctors[
        doctors["department_id"].isin(departments["department_id"])
    ]

    # -------------------------
    # DATE FIXES
    # -------------------------
    appointments["appointment_date"] = pd.to_datetime(
        appointments["appointment_date"]
    ).dt.date

    appointments["arrival_time"] = pd.to_datetime(appointments["arrival_time"])
    appointments["consultation_time"] = pd.to_datetime(appointments["consultation_time"])
    appointments["date"] = pd.to_datetime(appointments["date"]).dt.date

    # -------------------------
    # INSERT IN CORRECT ORDER
    # -------------------------
    insert_data(departments, "departments", conn)
    print("Departments loaded")

    insert_data(patients, "patients", conn)
    print("Patients loaded")

    insert_data(doctors, "doctors", conn)
    print("Doctors loaded")

    insert_data(beds, "beds", conn)
    print("Beds loaded")

    insert_data(staff, "staff", conn)
    print("Staff loaded")

    insert_data(equipment, "equipment", conn)
    print("Equipment loaded")

    insert_data(appointments, "appointments_features", conn)
    print("Appointments loaded")

    conn.close()
    print("✅ ALL DATA LOADED SUCCESSFULLY")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()