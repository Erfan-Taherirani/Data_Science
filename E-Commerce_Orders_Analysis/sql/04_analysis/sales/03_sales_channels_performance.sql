WITH CTE_sales_channels AS (
    SELECT DISTINCT
        sales_channel
    FROM orders.dim_channel
),
CTE_totals AS (
    SELECT
        COUNT(order_key) AS total_orders,
        SUM(revenue) AS total_revenue,
        SUM(profit) AS total_profit
    FROM orders.fact_orders
)

SELECT
    sales_channel,
    orders,
    CAST(CAST(orders AS FLOAT) / total_orders * 100 AS DECIMAL(10, 2)) AS order_share_percenatage,
    AOV,
    revenue,
    CAST(revenue / total_revenue * 100 AS DECIMAL(10, 2)) AS revenue_share_percenatage,
    profit,
    CAST(profit / total_profit * 100 AS DECIMAL(10, 2)) AS profit_share_percenatage,
    profit_margin
FROM (
    SELECT
        d.sales_channel,
        SUM(f.revenue) AS revenue,
        COUNT(f.order_key) AS orders,
        CAST(SUM(f.revenue) / COUNT(f.order_key) AS DECIMAL(10, 2)) AS AOV,
        SUM(f.profit) AS profit,
        CAST(SUM(f.profit) / SUM(f.revenue) AS DECIMAL(10, 2)) AS profit_margin,
        (SELECT total_orders FROM CTE_totals) AS total_orders,
        (SELECT total_revenue FROM CTE_totals) AS total_revenue,
        (SELECT total_profit FROM CTE_totals) AS total_profit
    FROM orders.fact_orders AS f
    LEFT JOIN orders.dim_channel AS d
        ON f.channel_key = d.channel_key
    GROUP BY sales_channel
) t
ORDER BY revenue DESC