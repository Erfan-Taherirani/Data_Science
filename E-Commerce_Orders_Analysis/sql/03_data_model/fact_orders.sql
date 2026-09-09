WITH CTE_dim_customers AS (
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
),
CTE_dim_channel AS (
    SELECT
        RANK() OVER (ORDER BY sales_channel, customer_acquisition_channel) AS channel_key,
        *
    FROM (
        SELECT DISTINCT
            sales_channel,
            customer_acquisition_channel
        FROM stg_transformed_orders
    ) t
),
CTE_dim_payment AS (
    SELECT
        RANK() OVER (ORDER BY payment_method, payment_status) AS payment_key,
        *
    FROM (
        SELECT DISTINCT
            payment_method,
            payment_status
        FROM stg_transformed_orders
    ) t
),
CTE_dim_flag AS (
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
)

SELECT
    t.order_key,
    t.customer_key,
    ctedc.geo_key,
    ctedch.channel_key,
    ctedp.payment_key,
    ctedf.flag_key,
    t.total_items,
    t.unique_products,
    t.subtotal,
    t.discount_amount,
    t.discount_rate,
    t.shipping_cost,
    t.tax_amount,
    t.revenue,
    t.profit,
    t.profit_margin
FROM stg_transformed_orders AS t
LEFT JOIN CTE_dim_customers AS ctedc
    ON t.customer_country = ctedc.customer_country
    AND t.customer_city = ctedc.customer_city
    AND t.customer_region = ctedc.customer_region
LEFT JOIN CTE_dim_channel AS ctedch
    ON t.sales_channel = ctedch.sales_channel
    AND t.customer_acquisition_channel = ctedch.customer_acquisition_channel
LEFT JOIN CTE_dim_payment AS ctedp
    ON t.payment_method = ctedp.payment_method
    AND t.payment_status = ctedp.payment_status
LEFT JOIN CTE_dim_flag AS ctedf
    ON t.discount_rate_level = ctedf.discount_rate_level
    AND t.shipping_method = ctedf.shipping_method
    AND t.delivery_status = ctedf.delivery_status
    AND t.campaign = ctedf.campaign
ORDER BY order_key