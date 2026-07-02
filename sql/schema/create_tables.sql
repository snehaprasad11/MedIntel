-- =========================
-- 1. CREATE & SELECT DB
-- =========================
DROP DATABASE IF EXISTS medintel;
CREATE DATABASE medintel;
USE medintel;

-- =========================
-- 2. CORE DIMENSION TABLES
-- =========================
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    city VARCHAR(100)
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(255),
    specialty VARCHAR(100),
    department_id INT
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

-- =========================
-- 3. FACT TABLES
-- =========================
CREATE TABLE appointments_features (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    department_id INT,
    appointment_date DATE,
    arrival_time DATETIME,
    consultation_time DATETIME,
    is_valid INT,
    wait_time_minutes FLOAT,
    arrival_hour INT,
    day_of_week VARCHAR(20),
    is_weekend INT,
    doctor_appointments INT,
    department_appointments INT,
    date DATE,
    daily_appointments INT
);

CREATE TABLE beds (
    date DATE,
    department_id INT,
    total_beds INT,
    occupied_beds INT,
    icu_beds INT,
    occupied_icu_beds INT,
    PRIMARY KEY (date, department_id)
);

CREATE TABLE staff (
    date DATE,
    department_id INT,
    doctors_scheduled INT,
    doctors_present INT,
    nurses_scheduled INT,
    nurses_present INT,
    support_staff_scheduled INT,
    support_staff_present INT,
    PRIMARY KEY (date, department_id)
);

CREATE TABLE equipment (
    date DATE,
    department_id INT,
    equipment_type VARCHAR(50),
    total_units INT,
    units_in_use INT,
    utilization_pct FLOAT,
    PRIMARY KEY (date, department_id, equipment_type)
);

-- =========================
-- 4. FOREIGN KEYS
-- =========================
ALTER TABLE doctors
ADD FOREIGN KEY (department_id)
REFERENCES departments(department_id);

ALTER TABLE appointments_features
ADD FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
ADD FOREIGN KEY (department_id) REFERENCES departments(department_id);

CREATE OR REPLACE VIEW v_bed_utilization AS
SELECT
    department_id,
    date,
    total_beds,
    occupied_beds,
    ROUND(occupied_beds / NULLIF(total_beds,0) * 100, 2) AS bed_occupancy_pct,
    icu_beds,
    occupied_icu_beds,
    ROUND(occupied_icu_beds / NULLIF(icu_beds,0) * 100, 2) AS icu_occupancy_pct
FROM beds;

CREATE OR REPLACE VIEW v_staff_efficiency AS
SELECT
    department_id,
    date,
    doctors_scheduled,
    doctors_present,
    ROUND(doctors_present / NULLIF(doctors_scheduled,0) * 100, 2) AS doctor_attendance_pct,
    nurses_scheduled,
    nurses_present,
    ROUND(nurses_present / NULLIF(nurses_scheduled,0) * 100, 2) AS nurse_attendance_pct
FROM staff;

CREATE OR REPLACE VIEW v_equipment_usage AS
SELECT
    department_id,
    date,
    equipment_type,
    total_units,
    units_in_use,
    utilization_pct
FROM equipment;

CREATE OR REPLACE VIEW v_appointment_kpis AS
SELECT
    appointment_id,
    department_id,
    wait_time_minutes,
    arrival_hour,
    day_of_week,
    is_weekend
FROM appointments_features;

CREATE OR REPLACE VIEW vw_doctor_performance AS
SELECT
    doctor_id,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY doctor_id;

CREATE OR REPLACE VIEW vw_department_summary AS
SELECT
    department_id,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY department_id;

CREATE OR REPLACE VIEW vw_daily_operations AS
SELECT
    appointment_date,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY appointment_date;

CREATE OR REPLACE VIEW v_department_health_score AS
SELECT
    b.department_id,
    b.date,
    ROUND(b.occupied_beds / NULLIF(b.total_beds,0) * 100, 2) AS bed_occupancy_pct,
    ROUND(s.doctors_present / NULLIF(s.doctors_scheduled,0) * 100, 2) AS doctor_attendance_pct,
    ROUND(s.nurses_present / NULLIF(s.nurses_scheduled,0) * 100, 2) AS nurse_attendance_pct,
    e.utilization_pct,
    COALESCE(a.avg_wait_time, 0) AS avg_wait_time
FROM beds b
JOIN staff s
    ON b.department_id = s.department_id
   AND b.date = s.date
JOIN equipment e
    ON b.department_id = e.department_id
   AND b.date = e.date
LEFT JOIN (
    SELECT department_id, date, AVG(wait_time_minutes) AS avg_wait_time
    FROM appointments_features
    GROUP BY department_id, date
) a
ON a.department_id = b.department_id
AND a.date = b.date;
