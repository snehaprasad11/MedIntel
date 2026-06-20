import mysql.connector
import pandas as pd
import os

# ---------------------------
# 1. CONNECT TO MYSQL
# ---------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",   # change this
    database="medintel"
)

# ---------------------------
# 2. ALL KPI QUERIES
# ---------------------------
queries = {
    # KPI 1: Department Load
    "department_load": """
        SELECT 
            department_id,
            COUNT(appointment_id) AS total_appointments
        FROM appointments_features
        GROUP BY department_id
        ORDER BY total_appointments DESC;
    """,

    # KPI 2: Doctor Load
    "doctor_load": """
        SELECT 
            doctor_id,
            COUNT(appointment_id) AS total_appointments
        FROM appointments_features
        GROUP BY doctor_id
        ORDER BY total_appointments DESC;
    """,

    # KPI 3: Hourly Traffic
    "hourly_traffic": """
        SELECT 
            arrival_hour,
            COUNT(appointment_id) AS total_appointments
        FROM appointments_features
        GROUP BY arrival_hour
        ORDER BY total_appointments DESC;
    """,

    # KPI 4: Weekend vs Weekday
    "weekend_vs_weekday": """
        SELECT 
            CASE 
                WHEN is_weekend = 1 THEN 'Weekend'
                ELSE 'Weekday'
            END AS day_type,
            COUNT(appointment_id) AS total_appointments
        FROM appointments_features
        GROUP BY day_type;
    """,

    # KPI 5: Wait Time Trend
    "wait_time_trend": """
        SELECT 
            date,
            AVG(wait_time_minutes) AS avg_wait_time
        FROM appointments_features
        GROUP BY date
        ORDER BY date;
    """
}

# ---------------------------
# 3. OUTPUT FOLDER
# ---------------------------
output_dir = "analytics/output"
os.makedirs(output_dir, exist_ok=True)

# ---------------------------
# 4. EXECUTE + EXPORT
# ---------------------------
for name, query in queries.items():
    df = pd.read_sql(query, conn)
    file_path = f"{output_dir}/{name}.csv"
    df.to_csv(file_path, index=False)
    print(f"Exported: {file_path}")

# ---------------------------
# 5. CLOSE CONNECTION
# ---------------------------
conn.close()

print("\nAll KPIs executed successfully!")