SELECT
    department_id,
    COUNT(*) AS appointments,
    RANK() OVER(
        ORDER BY COUNT(*) DESC
    ) AS rank_num
FROM appointments_features
GROUP BY department_id;