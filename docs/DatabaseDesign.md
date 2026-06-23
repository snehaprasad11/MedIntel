# Database Design

## Schema Overview

Core tables:
- patients
- doctors
- departments
- appointments_features
- beds
- equipment
- staff

---

## Key Relationships

- patients → appointments (1:M)
- doctors → appointments (1:M)
- departments → doctors (1:M)
- departments → beds (1:M)

---

## Feature Table: appointments_features

Key engineered fields:
- wait_time_minutes
- arrival_hour
- day_of_week
- is_weekend
- doctor_appointments
- department_appointments

---

## Analytical Views

### vw_daily_operations
Daily hospital KPIs

### vw_department_summary
Department efficiency metrics

### vw_doctor_performance
Doctor workload + performance ranking