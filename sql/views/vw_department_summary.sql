CREATE VIEW vw_department_summary AS
SELECT
    department_id,
    COUNT(*) AS total_appointments,
    ROUND(AVG(wait_time_minutes),2) AS avg_wait_time
FROM appointments_features
GROUP BY department_id;