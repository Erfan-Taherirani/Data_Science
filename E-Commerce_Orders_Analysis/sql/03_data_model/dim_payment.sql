-- create payment dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_payment]') AND type in (N'U'))
DROP TABLE [orders].[dim_payment]
GO
CREATE TABLE orders.dim_payment (
    payment_key INT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    CONSTRAINT PK_dim_payment PRIMARY KEY (payment_key)
);

-- insert data into the payment dimension table
INSERT INTO orders.dim_payment
SELECT
    RANK() OVER (ORDER BY payment_method, payment_status) AS payment_key,
    *
FROM (
    SELECT DISTINCT
        payment_method,
        payment_status
    FROM stg_transformed_orders
) t;

SELECT * FROM orders.dim_payment
