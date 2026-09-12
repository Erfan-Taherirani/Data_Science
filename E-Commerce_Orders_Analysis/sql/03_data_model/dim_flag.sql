-- create flag dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_flag]') AND type in (N'U'))
DROP TABLE [orders].[dim_flag]
GO
CREATE TABLE orders.dim_flag (
    flag_key INT,
    shipping_method VARCHAR(50),
    delivery_status VARCHAR(50),
    CONSTRAINT PK_dim_flag PRIMARY KEY (flag_key)
);

-- insert data into the flag dimension table
INSERT INTO orders.dim_flag
SELECT
    RANK() OVER (ORDER BY shipping_method, delivery_status) AS flag_key,
    *
FROM (
    SELECT DISTINCT
        shipping_method,
        delivery_status
    FROM stg_transformed_orders
) t;

SELECT * FROM orders.dim_flag
