SELECT
    doctor_id,
    COUNT(*) AS appointments
FROM appointments_features
GROUP BY doctor_id
ORDER BY appointments DESC
LIMIT 10;