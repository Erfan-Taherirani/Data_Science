-- create a fact table
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[fact_orders]') AND type in (N'U'))
DROP TABLE [orders].[fact_orders]
GO
CREATE TABLE orders.fact_orders (
    order_key INT,
    customer_key INT,
    date_key INT,
    geo_key INT,
    channel_key INT,
    payment_key INT,
    discount_rate_level_key INT,
    flag_key INT,
    campaign_key INT,
    total_items INT,
    unique_products INT,
    subtotal DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    discount_rate DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    revenue DECIMAL(10,2),
    profit DECIMAL(10,2),
    profit_margin DECIMAL(10,2),
    days_to_ship INT,
    days_to_deliver INT,
    ship_to_delivery_days INT,
    order_date DATE,
    ship_date DATE,
    delivery_date DATE,
    CONSTRAINT PK_fact_orders PRIMARY KEY (order_key)
);

-- CTEs to create dimension tables for joining
WITH CTE_dim_customers AS (
    SELECT
        RANK() OVER (ORDER BY customer_id) AS customer_key,
        customer_id,
        customer_name,
        customer_segment
    FROM (
        SELECT DISTINCT
            customer_id,
            customer_name,
            customer_segment
        FROM stg_transformed_orders
    ) t
),
CTE_dim_dates AS (
    SELECT
        RANK() OVER (ORDER BY order_date) AS date_key,
        *
    FROM (
        SELECT DISTINCT
            order_date,
            month_name,
            day_name,
            year,
            month,
            week,
            week_day,
            day
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
        RANK() OVER (ORDER BY shipping_method, delivery_status) AS flag_key,
        *
    FROM (
        SELECT DISTINCT
            shipping_method,
            delivery_status
        FROM stg_transformed_orders
    ) t
),
CTE_dim_discount_rate_level AS (
    SELECT
        CASE
            WHEN discount_rate_level = '0' THEN 1
            WHEN discount_rate_level = '1-10%' THEN 2
            WHEN discount_rate_level = '10-20%' THEN 3
            WHEN discount_rate_level = '20-30%' THEN 4
            WHEN discount_rate_level = '30%+' THEN 5
        END AS discount_rate_level_key,
        discount_rate_level
    FROM stg_transformed_orders
    GROUP BY discount_rate_level
),
CTE_dim_geo AS (
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
CTE_dim_campaign AS (
    SELECT
        RANK() OVER (ORDER BY campaign) AS campaign_key,
        campaign
    FROM (
        SELECT DISTINCT
            campaign
        FROM stg_transformed_orders
    ) t
)

-- insert data into the fact table
INSERT INTO orders.fact_orders
SELECT
    t.order_key,
    ctedc.customer_key,
    ctedd.date_key,
    ctedg.geo_key,
    ctedch.channel_key,
    ctedp.payment_key,
    ctedr.discount_rate_level_key,
    ctedf.flag_key,
    ctedca.campaign_key,
    t.total_items,
    t.unique_products,
    t.subtotal,
    t.discount_amount,
    t.discount_rate,
    t.shipping_cost,
    t.tax_amount,
    t.revenue,
    t.profit,
    t.profit_margin,
    t.days_to_ship,
    t.days_to_deliver,
    t.ship_to_delivery_days,
    t.order_date,
    t.ship_date,
    t.delivery_date
FROM stg_transformed_orders AS t
LEFT JOIN CTE_dim_customers AS ctedc
ON t.customer_id = ctedc.customer_id
LEFT JOIN CTE_dim_dates AS ctedd
    ON t.order_date = ctedd.order_date
LEFT JOIN CTE_dim_channel AS ctedch
    ON t.sales_channel = ctedch.sales_channel
        AND t.customer_acquisition_channel = ctedch.customer_acquisition_channel
LEFT JOIN CTE_dim_payment AS ctedp
    ON t.payment_method = ctedp.payment_method
        AND t.payment_status = ctedp.payment_status
LEFT JOIN CTE_dim_discount_rate_level AS ctedr
    ON t.discount_rate_level = ctedr.discount_rate_level
LEFT JOIN CTE_dim_flag AS ctedf
    ON t.shipping_method = ctedf.shipping_method
        AND t.delivery_status = ctedf.delivery_status
LEFT JOIN CTE_dim_geo AS ctedg
    ON t.customer_country = ctedg.customer_country
        AND t.customer_city = ctedg.customer_city
        AND t.customer_region = ctedg.customer_region
LEFT JOIN CTE_dim_campaign AS ctedca
   ON t.campaign = ctedca.campaign
ORDER BY order_key;

SELECT * FROM orders.fact_orders
