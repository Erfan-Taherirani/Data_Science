SELECT
    DENSE_RANK() OVER (ORDER BY 
        customer_country, customer_city, customer_region) AS geo_key,
    *
FROM (
SELECT DISTINCT
    customer_country,
    customer_city,
    customer_region
FROM stg_transformed_orders
) t