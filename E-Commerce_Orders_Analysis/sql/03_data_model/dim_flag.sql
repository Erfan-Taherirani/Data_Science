SELECT
    RANK() OVER (ORDER BY
        discount_rate_level, shipping_method,
        delivery_status, campaign) AS flag_key,
    *
FROM (
    SELECT DISTINCT
        discount_rate_level,
        shipping_method,
        delivery_status,
        campaign
    FROM stg_transformed_orders
) t