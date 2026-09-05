SELECT DISTINCT
    *
FROM (
    SELECT
        *,
        COUNT(*) OVER (PARTITION BY order_id) AS duplication_flag
    FROM orders
) t
WHERE duplication_flag > 1
ORDER BY order_id