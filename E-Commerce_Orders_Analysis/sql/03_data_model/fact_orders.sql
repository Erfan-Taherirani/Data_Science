SELECT
    order_key,
    customer_key,
    total_items,
    unique_products,
    subtotal,
    discount_amount,
    discount_rate,
    shipping_cost,
    tax_amount,
    revenue,
    profit,
    profit_margin,
    order_date,
    ship_date,
    delivery_date,
    days_to_ship,
    days_to_deliver,
    ship_to_delivery_days
FROM stg_transformed_orders

SELECT * FROM stg_transformed_orders