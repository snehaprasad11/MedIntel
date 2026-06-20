# SQL Analytics - MedIntel
## KPI 1: Total Appointments per Department
### Purpose

Identify hospital departments with the highest patient load.

### Formula

COUNT(appointment_id)

### SQL Query
SELECT 
    department_id, 
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY department_id;

---
## KPI 2: Doctor Utilization (Overloaded Doctors)
### Purpose

Find doctors handling the highest number of appointments (workload distribution).

### Formula

COUNT(appointment_id) per doctor

### SQL Query
SELECT 
    doctor_id, 
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY doctor_id
ORDER BY total_appointments DESC;

---
## KPI 3: Peak Hour Traffic Analysis
### Purpose

Identify the busiest hours in the hospital for staffing optimization.

### Formula

COUNT(appointment_id) grouped by arrival_hour

### SQL Query
SELECT 
    arrival_hour, 
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY arrival_hour
ORDER BY total_appointments DESC;

---
## KPI 4: Weekend vs Weekday Load
### Purpose

Compare patient inflow between weekdays and weekends.

### Formula

COUNT(appointment_id) grouped by is_weekend

### SQL Query
SELECT 
    CASE 
        WHEN is_weekend = 1 THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY day_type;

---
## KPI 5: Average Wait Time Trend
### Purpose

Track hospital efficiency and service delays over time.

### Formula

AVG(wait_time_minutes) per date

### SQL Query
SELECT 
    date,
    AVG(wait_time_minutes) AS avg_wait_time
FROM appointments_features
GROUP BY date
ORDER BY date;