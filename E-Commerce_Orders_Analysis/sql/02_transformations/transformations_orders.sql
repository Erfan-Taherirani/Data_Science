WITH CTE_table_with_primary_key AS (
    SELECT
        DENSE_RANK() OVER (ORDER BY customer_id) AS customer_key,
        RANK() OVER (ORDER BY order_id) AS order_key,
        order_date,
        ship_date,
        delivery_date,

        customer_name,
        customer_segment,
        customer_country,
        customer_city,
        customer_region,

        order_status,
        total_items,
        unique_products,

        subtotal,
        discount_amount,
        ROUND(discount_amount / total_order_value * 100, 2) AS discount_rate,
        shipping_cost,
        tax_amount,
        total_order_value AS revenue,
        profit,
        ROUND(profit / total_order_value * 100, 2) AS profit_margin,

        shipping_method,
        delivery_status,
        payment_method,
        payment_status,

        sales_channel,
        customer_acquisition_channel,
        campaign
    FROM stg_orders
),
CTE_date_extractions AS (
    SELECT
        order_key,
        --common date extractions
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        DAY(order_date) AS day,
        DATEPART(WEEK, order_date) AS week,
        DATEPART(WEEKDAY, order_date) AS week_day,
        DATENAME(MONTH, order_date) AS month_name,
        DATENAME(WEEKDAY, order_date) AS day_name,

        -- date diffs
        DATEDIFF(DAY, order_date, ship_date) AS days_to_ship,
        DATEDIFF(DAY, order_date, delivery_date) AS days_to_deliver,
        DATEDIFF(DAY, ship_date, delivery_date) AS ship_to_delivery_days
    FROM CTE_table_with_primary_key
),
CTE_discount_rate_level AS (
    SELECT
        order_key,
        discount_rate,
    CASE
        WHEN ROUND(discount_amount / revenue * 100, 2) = 0 THEN '0'
        WHEN ROUND(discount_amount / revenue * 100, 2) > 0 THEN '1-5%'
        WHEN ROUND(discount_amount / revenue * 100, 2) > 5 THEN '5-10%'
        WHEN ROUND(discount_amount / revenue * 100, 2) > 10 THEN '10-15%'
        WHEN ROUND(discount_amount / revenue * 100, 2) > 15 THEN '15-20%'
        WHEN ROUND(discount_amount / revenue * 100, 2) > 20 THEN '20-30%'
        ELSE '30%+'
    END AS discount_rate_level
    FROM CTE_table_with_primary_key
)

-- Create a transformation table

SELECT
    ctet.order_key,
    ctet.customer_key,
    ctet.order_date,
    ctet.ship_date,
    ctet.delivery_date,
    -- common date extractions
    cted.year,
    cted.month,
    cted.week,
    cted.week_day,
    cted.day,
    cted.month_name,
    cted.day_name,
    -- date diffs
    cted.days_to_ship,
    cted.days_to_deliver,
    cted.ship_to_delivery_days,

    ctet.customer_name,
    ctet.customer_segment,
    ctet.customer_country,
    ctet.customer_city,
    ctet.customer_region,

    ctet.order_status,
    ctet.total_items,
    ctet.unique_products,

    ctet.subtotal,
    ctet.discount_amount,
    ctet.discount_rate,
    ctedr.discount_rate_level,
    ctet.shipping_cost,
    ctet.tax_amount,
    ctet.revenue,
    ctet.profit,
    ctet.profit_margin,

    ctet.shipping_method,
    ctet.delivery_status,
    ctet.payment_method,
    ctet.payment_status,

    ctet.sales_channel,
    ctet.customer_acquisition_channel,
    ctet.campaign
INTO stg_transformed_orders
FROM CTE_table_with_primary_key AS ctet
LEFT JOIN CTE_date_extractions AS cted
    ON ctet.order_key = cted.order_key
LEFT JOIN CTE_discount_rate_level AS ctedr
    ON ctet.order_key = ctedr.order_key