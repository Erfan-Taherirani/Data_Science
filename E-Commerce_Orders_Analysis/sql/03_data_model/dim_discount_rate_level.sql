-- create discount rate level dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_discount_rate_level]') AND type in (N'U'))
DROP TABLE [orders].[dim_discount_rate_level]
GO
CREATE TABLE orders.dim_discount_rate_level (
    discount_rate_level_key INT,
    discount_rate_level VARCHAR(50),
    CONSTRAINT PK_dim_discount_rate_level PRIMARY KEY (discount_rate_level_key)
);

-- insert data into the discount rate level dimension table
INSERT INTO orders.dim_discount_rate_level
SELECT
    CASE
        WHEN discount_rate_level = '0' THEN 1
        WHEN discount_rate_level = '0-5%' THEN 2
        WHEN discount_rate_level = '5-10%' THEN 3
        WHEN discount_rate_level = '10-15%' THEN 4
        WHEN discount_rate_level = '15-20%' THEN 5
        WHEN discount_rate_level = '20-30%' THEN 6
        WHEN discount_rate_level = '30%+' THEN 7
    END AS discount_rate_level_key,
    discount_rate_level
FROM stg_transformed_orders
GROUP BY discount_rate_level
ORDER BY discount_rate_level_key;

SELECT * FROM orders.dim_discount_rate_level
