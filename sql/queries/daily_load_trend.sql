SELECT
    appointment_date,
    COUNT(*) AS total_appointments
FROM appointments_features
GROUP BY appointment_date
ORDER BY appointment_date;