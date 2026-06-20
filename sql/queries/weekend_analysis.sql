SELECT
    is_weekend,
    COUNT(*) AS total_appointments,
    AVG(wait_time_minutes) AS avg_wait_time
FROM appointments_features
GROUP BY is_weekend;