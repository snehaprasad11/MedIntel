# Database Design

The canonical MySQL schema is:

```text
sql/schema/create_tables.sql
```

This file reflects the schema used by the ETL loader and analytics SQL. Earlier star-schema naming such as `dim_patient` and `fact_patient_visits` is not the active project schema.

## Core Tables

- `patients`
- `doctors`
- `departments`
- `appointments_features`
- `beds`
- `staff`
- `equipment`

## Relationships

- `departments.department_id` -> `doctors.department_id`
- `patients.patient_id` -> `appointments_features.patient_id`
- `doctors.doctor_id` -> `appointments_features.doctor_id`
- `departments.department_id` -> `appointments_features.department_id`

The resource tables (`beds`, `staff`, and `equipment`) are keyed by date and department so operational capacity can be analyzed by day.

## Main Feature Table

`appointments_features` is the central analytics table. Important fields:

- `wait_time_minutes`
- `arrival_hour`
- `day_of_week`
- `is_weekend`
- `doctor_appointments`
- `department_appointments`
- `daily_appointments`

This table supports department load, doctor workload, daily operations, hourly traffic, wait-time trends, and forecasting inputs.

## Operational Resource Tables

`beds` captures total and occupied bed counts by department and date.

`staff` captures scheduled and present doctor, nurse, and support staff counts.

`equipment` captures total units, units in use, and utilization percentage by equipment type.

## Analytical Views

The schema creates these views:

- `v_bed_utilization`
- `v_staff_efficiency`
- `v_equipment_usage`
- `v_appointment_kpis`
- `vw_doctor_performance`
- `vw_department_summary`
- `vw_daily_operations`
- `v_department_health_score`

These views support the dashboard, SQL analytics layer, and Power BI reporting.

## Reset Behavior

`create_tables.sql` starts with:

```sql
DROP DATABASE IF EXISTS medintel;
CREATE DATABASE medintel;
USE medintel;
```

Run it only when a fresh database rebuild is intended.
