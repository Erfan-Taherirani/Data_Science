SELECT
    RANK() OVER (ORDER BY sales_channel, customer_acquisition_channel) AS channel_key,
    *
FROM (
    SELECT DISTINCT
        sales_channel,
        customer_acquisition_channel
    FROM stg_transformed_orders
) t