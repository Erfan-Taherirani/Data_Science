-- create date dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_dates]') AND type in (N'U'))
DROP TABLE [orders].[dim_dates]
GO
CREATE TABLE orders.dim_dates (
    date_key INT,
    order_date DATE,
    month_name VARCHAR(50),
    day_name VARCHAR(50),
    year INT,
    month INT,
    week INT,
    week_day INT,
    day INT,
    CONSTRAINT PK_dim_dates PRIMARY KEY (date_key)
);

-- insert data into the date dimension table
INSERT INTO orders.dim_dates
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
) t;

SELECT * FROM orders.dim_dates
