WITH CTE_discount_level_table AS (
    SELECT
        f.discount_rate,
        d.discount_rate_level,
        f.order_key,
        f.revenue,
        f.profit,
        f.total_items AS n_items,
        COUNT(order_key) OVER () AS total_orders,
        SUM(revenue) OVER () AS total_revenue,
        SUM(profit) OVER () AS total_profit,
        SUM(total_items) OVER () AS total_items
    FROM orders.fact_orders AS f
    LEFT JOIN orders.dim_discount_rate_level AS d
        ON f.discount_rate_level_key = d.discount_rate_level_key
)

SELECT
    discount_rate_level,
    orders,
    revenue,
    profit,
    n_items AS total_items,
    CAST(CAST(n_items AS FLOAT) / orders AS DECIMAL(10, 2)) AS total_items_per_order,
    CAST(CAST(orders AS FLOAT) / total_orders * 100 AS DECIMAL(10, 2)) AS order_share,
    CAST(revenue / total_revenue * 100 AS DECIMAL(10, 2)) AS revenue_share,
    CAST(profit / total_profit * 100 AS DECIMAL(10, 2)) AS profit_share,
    CAST(CAST(n_items AS FLOAT) / total_items AS DECIMAL(10, 2)) AS total_items_share,
    AOV,
    profit_margin
FROM (
    SELECT
        discount_rate_level,
        COUNT(order_key) AS orders,
        (SELECT DISTINCT total_orders FROM CTE_discount_level_table) AS total_orders,
        SUM(revenue) AS revenue,
        (SELECT DISTINCT total_revenue FROM CTE_discount_level_table) AS total_revenue,
        SUM(profit) AS profit,
        (SELECT DISTINCT total_profit FROM CTE_discount_level_table) AS total_profit,
        SUM(n_items) AS n_items,
        (SELECT DISTINCT total_items FROM CTE_discount_level_table) AS total_items,
        CAST(SUM(revenue) / COUNT(order_key) AS DECIMAL(10, 2)) AS AOV,
        CAST(SUM(profit) / SUM(revenue) * 100 AS DECIMAL(10, 2)) AS profit_margin
    FROM CTE_discount_level_table
    GROUP BY discount_rate_level
) t
ORDER BY discount_rate_level