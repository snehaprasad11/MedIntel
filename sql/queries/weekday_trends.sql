SELECT
    day_of_week,
    COUNT(*) AS appointments
FROM appointments_features
GROUP BY day_of_week;