CREATE TABLE stg_orders (
    [order_id]                     NVARCHAR (50) NOT NULL,
    [customer_id]                  NVARCHAR (50) NOT NULL,
    [order_date]                   DATE          NULL,
    [ship_date]                    DATE          NULL,
    [delivery_date]                DATE          NULL,

    [customer_name]                NVARCHAR (50) NULL,
    [customer_segment]             NVARCHAR (50) NULL,
    [customer_country]             NVARCHAR (50) NULL,
    [customer_city]                NVARCHAR (50) NULL,
    [customer_region]              NVARCHAR (50) NULL,

    [order_status]                 NVARCHAR (50) NULL,
    [total_items]                  TINYINT       NULL,
    [unique_products]              TINYINT       NULL,
    
    [subtotal]                     FLOAT (53)    NULL,
    [discount_amount]              FLOAT (53)    NULL,
    [shipping_cost]                FLOAT (53)    NULL,
    [tax_amount]                   FLOAT (53)    NULL,
    [total_order_value]            FLOAT (53)    NULL,
    [profit]                       FLOAT (53)    NULL,

    [shipping_method]              NVARCHAR (50) NULL,
    [delivery_status]              NVARCHAR (50) NULL,
    [payment_method]               NVARCHAR (50) NULL,
    [payment_status]               NVARCHAR (50) NULL,
    
    [sales_channel]                NVARCHAR (50) NULL,
    [customer_acquisition_channel] NVARCHAR (50) NULL,
    [campaign]                     NVARCHAR (50) NULL
)