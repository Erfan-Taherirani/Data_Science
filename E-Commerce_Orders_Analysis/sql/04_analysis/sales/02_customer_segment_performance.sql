WITH CTE_sales_performance AS (
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
),
CTE_customer_segments AS (
    -- Which customer segments generate the most revenue and profit?
    SELECT
        c.customer_segment,
        ROUND(SUM(f.revenue), 2) AS revenue,
        COUNT(f.order_key) AS orders,
        CAST(CAST(COUNT(f.order_key) AS DECIMAL) / (
            SELECT total_orders FROM CTE_sales_performance
        ) * 100 AS DECIMAL(10, 1)) AS orders_percentage,
        CAST(SUM(f.revenue) / COUNT(f.order_key) AS DECIMAL(10, 2)) AS AOV,
        SUM(f.profit) AS profit,
        CAST(SUM(f.profit) / SUM(f.revenue) AS DECIMAL(10, 3)) AS profit_margin
    FROM orders.fact_orders AS f
    LEFT JOIN orders.dim_customers AS c
        ON f.customer_key = c.customer_key
    GROUP BY c.customer_segment
)

SELECT
    RANK() OVER (ORDER BY revenue DESC) AS rank,
    *
FROM CTE_customer_segments
ORDER BY revenue DESC
