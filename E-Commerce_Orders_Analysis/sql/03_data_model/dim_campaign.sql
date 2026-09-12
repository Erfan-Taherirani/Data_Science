-- create campaign dimension table
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[orders].[dim_campaign]') AND type in (N'U'))
DROP TABLE [orders].[dim_campaign]
GO
CREATE TABLE orders.dim_campaign (
    campaign_key INT,
    campaign VARCHAR(50),
    CONSTRAINT PK_dim_campaign PRIMARY KEY (campaign_key)
);

-- insert data into the campaign dimension table
INSERT INTO orders.dim_campaign
SELECT
    RANK() OVER (ORDER BY campaign) AS campaign_key,
    campaign
FROM (
    SELECT DISTINCT
        campaign
    FROM stg_transformed_orders
) t;

SELECT * FROM orders.dim_campaign
