CREATE VIEW vw_daily_operations AS
SELECT
    appointment_date,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY appointment_date;