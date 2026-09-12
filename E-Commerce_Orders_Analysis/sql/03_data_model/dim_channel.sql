-- create channel dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_channel]') AND type in (N'U'))
DROP TABLE [orders].[dim_channel]
GO
CREATE TABLE orders.dim_channel (
    channel_key INT,
    sales_channel VARCHAR(50),
    customer_acquisition_channel VARCHAR(50),
    CONSTRAINT PK_dim_channel PRIMARY KEY (channel_key)
);

-- insert data into the channel dimension table
INSERT INTO orders.dim_channel
SELECT
    RANK() OVER (ORDER BY sales_channel, customer_acquisition_channel) AS channel_key,
    *
FROM (
    SELECT DISTINCT
        sales_channel,
        customer_acquisition_channel
    FROM stg_transformed_orders
) t;

SELECT * FROM orders.dim_channel
