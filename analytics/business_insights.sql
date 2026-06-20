SELECT 
    department_id,
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY department_id
ORDER BY total_appointments DESC;

SELECT 
    doctor_id,
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY doctor_id
ORDER BY total_appointments DESC;

SELECT 
    arrival_hour,
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY arrival_hour
ORDER BY total_appointments DESC;

SELECT 
    CASE 
        WHEN is_weekend = 1 THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(appointment_id) AS total_appointments
FROM appointments_features
GROUP BY day_type;

SELECT 
    date,
    AVG(wait_time_minutes) AS avg_wait_time
FROM appointments_features
GROUP BY date
ORDER BY date;