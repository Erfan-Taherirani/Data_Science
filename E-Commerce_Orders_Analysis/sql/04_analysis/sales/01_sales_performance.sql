-- How is the overall sales performance evolving?
SELECT
    SUM(revenue) AS total_revenue,
    COUNT(order_key) AS total_orders,
    SUM(total_items) AS total_items_sold,
    ROUND((SUM(revenue) / COUNT(order_key)), 2) AS AOV,
    ROUND(SUM(revenue) / SUM(total_items), 2) AS revenue_per_item,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit) / SUM(revenue) * 100, 2) AS profit_margin,
    ROUND(SUM(profit) / SUM(revenue), 3) AS profit_contribution_per_1_dollar_revenue
FROM orders.fact_orders

-- SELECT
--     order_key,
--     revenue,
--     total_items,
--     profit,
--     profit_margin
-- FROM orders.fact_ordersS