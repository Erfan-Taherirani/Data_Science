-- create geo dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_geo]') AND type in (N'U'))
DROP TABLE [orders].[dim_geo]
GO
CREATE TABLE orders.dim_geo (
    geo_key INT,
    customer_country VARCHAR(50),
    customer_city VARCHAR(50),
    customer_region VARCHAR(50),
    CONSTRAINT PK_dim_geo PRIMARY KEY (geo_key)
);

-- insert data into the geo dimension table
INSERT INTO orders.dim_geo
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
) t;

SELECT * FROM orders.dim_geo
