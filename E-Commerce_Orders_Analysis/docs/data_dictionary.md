# Data Dictionary

In this document, we will have a data dictionary that will help us understand the data and the business questions that we want to answer.

| Table       | Candidate Key           | Unique? | Meaning                          | Expected Grain            |
| ----------- | ----------------------- | ------: | -------------------------------- | ------------------------- |
| Orders      | `order_id`              |     Yes | Identifies an order              | One row per order         |
| Order Items | `order_id + product_id` |     Yes | Identifies product line in order | One row per order-product |
| Customers   | `customer_id`           |     Yes | Identifies customer              | One row per customer      |
| Products    | `product_id`            |     Yes | Identifies product               | One row per product       |

## Orders Table

**Grain:** the granularity of the data is that: each row represents a single order that has been placed by a customer.

### order_date & ship_date & delivery_date

- **Order date** shows the exact date that the order was placed. 

- **Ship date** shows the date when the order was shipped and it's in transit to the customer.

- **Delivery date** shows the date when the order was delivered to the customer.

### Customer Segment

Customer segment shows the customer segment that the order belongs to. The values in this column are:

- Consumer
- Corporate
- Small Business

### Total Items

This column shows the total number of items in the order. Our dataset order has the granularity of one row per order so we just have that how many items are in each order.

### Subtotal

Subtotal shows the total value of the order before taxes, shipping cost, and discounts. All the values are in USD.

### Discount Amount

Discount amount shows that how many dollars the get discount on the total value of the order.

### total_order_value

We can say that total value of the order is the revenue of the order.

$$
    \text{total order value} = \text{subtotal} - \text{discount amount} - \text{shipping cost} + \text{tax amount}
$$

### Profit

Profit shows how many dollars we profit from the order. We can use this columns to

### Campaign

About the campaign we can say that there are many null values cause most of the orders are not part of any campaign.
