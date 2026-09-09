SELECT
    RANK() OVER (ORDER BY payment_method, payment_status) AS payment_key,
    *
FROM (
    SELECT DISTINCT
        payment_method,
        payment_status
    FROM stg_transformed_orders
) t