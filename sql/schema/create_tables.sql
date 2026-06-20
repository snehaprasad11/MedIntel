CREATE TABLE dim_patient (
    patient_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    city VARCHAR(100)
);

CREATE TABLE dim_doctor (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(100),
    specialty VARCHAR(100)
);

CREATE TABLE dim_department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    visit_date DATE
);

CREATE TABLE fact_patient_visits (
    visit_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    department_id INT,
    date_id INT,
    wait_time INT,
    length_of_stay INT,
    visit_cost DECIMAL(10,2)
);