CREATE VIEW vw_doctor_performance AS
SELECT
    doctor_id,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY doctor_id;