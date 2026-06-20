# Data Warehouse Design

## Fact Table

### fact_patient_visits

visit_id

patient_id

doctor_id

department_id

date_id

wait_time

length_of_stay

visit_cost

---

## Dimension Tables

### dim_patient

Patient demographics.

### dim_doctor

Doctor information.

### dim_department

Department information.

### dim_date

Calendar information.

---

## Design Choice

A star schema is used because it simplifies analytical queries and improves reporting performance.
