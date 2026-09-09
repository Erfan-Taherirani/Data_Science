SELECT
    MIN(discount_rate) AS min_discount_rate,
    MAX(discount_rate) AS max_discount_rate,
    AVG(discount_rate) AS avg_discount_rate,
    SUM(discount_rate) AS sum_discount_rate,
    COUNT(discount_rate) AS count_discount_rate,
    COUNT(DISTINCT discount_rate) AS count_distinct_discount_rate
FROM (
    SELECT
        DENSE_RANK() OVER (ORDER BY customer_id) AS customer_key,
        RANK() OVER (ORDER BY order_id) AS order_key,
        order_date,
        ship_date,
        delivery_date,
        --common date extractions
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        DAY(order_date) AS day,
        DATENAME(MONTH, order_date) AS month_name,
        DATENAME(WEEKDAY, order_date) AS day_name,
        DATENAME(WEEK, order_date) AS week_day,

        -- date diffs
        DATEDIFF(DAY, order_date, ship_date) AS days_to_ship,
        DATEDIFF(DAY, order_date, delivery_date) AS days_to_deliver,
        DATEDIFF(DAY, ship_date, delivery_date) AS ship_to_delivery_days,

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
        -- CASE
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) = 0 THEN "0"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 0 THEN "0 - 5%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 5 THEN "5 - 10%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 10 THEN "10 - 15%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 15 THEN "15 - 20%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 20 THEN "20 - 25%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 25 THEN "25 - 30%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 30 THEN "30 - 35%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 35 THEN "35 - 40%"
        --     WHEN ROUND(discount_amount / total_order_value * 100, 2) > 40 THEN "40 - 45%"
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
) t