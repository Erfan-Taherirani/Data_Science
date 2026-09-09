SELECT
    order_key,
    month_name,
    day_name,
    year,
    month,
    week,
    week_day,
    day,
    days_to_ship,
    days_to_deliver,
    ship_to_delivery_days,
    order_date,
    ship_date,
    delivery_date
FROM stg_transformed_orders
ORDER BY order_key