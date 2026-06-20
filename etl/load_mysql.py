import pandas as pd
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="medintel"
    )

def insert_data(df, table_name, conn):
    cursor = conn.cursor()

    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))

    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = df.values.tolist()

    cursor.executemany(query, data)

    conn.commit()
    cursor.close()
def clear_tables(conn):
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE appointments_features")
    cursor.execute("TRUNCATE TABLE doctors")
    cursor.execute("TRUNCATE TABLE departments")
    cursor.execute("TRUNCATE TABLE patients")

    conn.commit()
    cursor.close()

    print("Old data cleared")
def main():

    conn = get_connection()
    clear_tables(conn)


    # Load datasets
    patients = pd.read_csv("data/clean/patients.csv")
    doctors = pd.read_csv("data/clean/doctors.csv")
    departments = pd.read_csv("data/clean/departments.csv")
    appointments = pd.read_csv("data/features/appointments_features.csv")
    appointments["appointment_date"] = pd.to_datetime(
    appointments["appointment_date"]
).dt.date

    appointments["arrival_time"] = pd.to_datetime(
    appointments["arrival_time"]
)

    appointments["consultation_time"] = pd.to_datetime(
    appointments["consultation_time"]
)

    appointments["date"] = pd.to_datetime(
    appointments["date"]
).dt.date
    appointments = appointments.where(
    pd.notnull(appointments),
    None
)
    
    # Insert into MySQL
    insert_data(patients, "patients", conn)
    print("Patients loaded")

    insert_data(doctors, "doctors", conn)
    print("Doctors loaded")

    insert_data(departments, "departments", conn)
    print("Departments loaded")

    insert_data(appointments, "appointments_features", conn)
    print("Appointments loaded")

    conn.close()

    print("Data loaded into MySQL successfully")


if __name__ == "__main__":
    main()

