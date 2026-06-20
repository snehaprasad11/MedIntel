SELECT
    department_id,
    COUNT(*) AS appointments
FROM appointments_features
GROUP BY department_id
ORDER BY appointments DESC;