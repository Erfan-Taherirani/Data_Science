WITH CTE_customers AS (
    SELECT DISTINCT
        customer_key,
        customer_name,
        customer_segment
    FROM stg_transformed_orders
)

SELECT *
FROM CTE_customers
ORDER BY customer_key