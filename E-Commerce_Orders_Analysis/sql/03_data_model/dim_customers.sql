-- create customer dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_customers]') AND type in (N'U'))
DROP TABLE [orders].[dim_customers]
GO
CREATE TABLE orders.dim_customers (
    customer_key INT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    customer_segment VARCHAR(50),
    CONSTRAINT PK_dim_customers PRIMARY KEY (customer_key)
);

-- insert data into the customer dimension table
INSERT INTO orders.dim_customers
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
) t;

SELECT * FROM orders.dim_customers
