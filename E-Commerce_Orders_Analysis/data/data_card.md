# Final orders.csv  recommended columns

| Group     | Column                         |
| --------- | ------------------------------ |
| ID        | `order_id`                     |
| ID        | `customer_id`                  |
| Date      | `order_date`                   |
| Date      | `ship_date`                    |
| Date      | `delivery_date`                |
| Customer  | `customer_name`                |
| Customer  | `customer_segment`             |
| Geography | `customer_country`             |
| Geography | `customer_city`                |
| Geography | `customer_region`              |
| Order     | `order_status`                 |
| Order     | `total_items`                  |
| Order     | `unique_products`              |
| Order     | `product_categories`           |
| Finance   | `subtotal`                     |
| Finance   | `discount_amount`              |
| Finance   | `shipping_cost`                |
| Finance   | `tax_amount`                   |
| Finance   | `total_order_value`            |
| Finance   | `profit`                       |
| Shipping  | `shipping_method`              |
| Shipping  | `delivery_status`              |
| Payment   | `payment_method`               |
| Payment   | `payment_status`               |
| Marketing | `sales_channel`                |
| Marketing | `customer_acquisition_channel` |
| Marketing | `campaign`                     |

## E-commerce Orders Dataset

**Domain:** B2C E-commerce

**Unit of observation:** One row = one customer order

**Primary analytical use:** Sales analytics, customer behavior, profitability analysis, forecasting, segmentation, and ML

## Important Feature Groups

| Group     | What it represents                          |
| --------- | ------------------------------------------- |
| Order     | When and what happened with the order       |
| Customer  | Who purchased                               |
| Geography | Where the customer is located               |
| Basket    | Size and diversity of the order             |
| Finance   | Revenue, discount, tax, shipping and profit |
| Shipping  | Fulfillment and delivery                    |
| Payment   | Payment behavior                            |
| Marketing | How the customer was acquired               |

Use the 27-column orders.csv as your primary dataset, and create the three companion datasets only when you need them.

orders.csv tells you what happened in the order.

order_items.csv tells you exactly what products and prices were inside the order.

**What is sutotal:**

Subtotal is the cost of the products in an order before adding shipping and tax, and after accounting for discounts depending on how you define it.

So the financial fields become:

subtotal
discount_amount
shipping_cost
tax_amount
total_order_value
profit

And:

total_order_value = subtotal - discount + shipping + tax
