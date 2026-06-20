SELECT
    arrival_hour,
    COUNT(*) AS appointments
FROM appointments_features
GROUP BY arrival_hour
ORDER BY arrival_hour;