-- MedIntel live database schema
-- Reference copy only - the app creates this automatically on startup
-- (see dashboard/core/db.py). You do not need to run this by hand.

CREATE DATABASE IF NOT EXISTS medintel;

USE medintel;

CREATE TABLE IF NOT EXISTS hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS department_snapshots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    department_name VARCHAR(255) NOT NULL,
    total_beds INT NOT NULL,
    occupied_beds INT NOT NULL,
    total_icu_beds INT NOT NULL,
    occupied_icu_beds INT NOT NULL,
    doctors_scheduled INT NOT NULL,
    doctors_present INT NOT NULL,
    nurses_scheduled INT NOT NULL,
    nurses_present INT NOT NULL,
    avg_wait_time_minutes FLOAT NOT NULL DEFAULT 0,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
    INDEX idx_hospital_submitted (hospital_id, submitted_at)
);
