SELECT
    YEAR(appointment_date) AS year,
    MONTH(appointment_date) AS month,
    COUNT(*) AS appointments
FROM appointments_features
GROUP BY year,month;