# Business Questions

In this phase, we should have defined the business questions that we want to answer. The goal is to have a clear understanding of the business objectives and the questions that we want to answer.

### Sales Performance

1. **How is overall sales performance evolving?**
    - Total revenue
    - Total orders
    - Total items sold
    - Average Order Value (AOV)
    - Revenue per item
    - Profit
    - Profit margin

This should be the **sales-performance baseline**.

2. **Which customer segments generate the most revenue and profit?**

    compare:
    - Revenue
    - Orders
    - AOV
    - Profit
    - Profit margin

3. **Which sales channels perform best?**

    compare:
    - Revenue
    - Orders
    - AOV
    - Profit
    - Profit margin
    - Order Share

    This can answer something like:

    **Is the company's marketplace channel generating high sales but lower profitability than direct sales?**

    That's a very realistic e-commerce question.

4. **How does discounting affect revenue and profitability?**

    You can analyze:
    - Discount Rate
    - Revenue
    - Profit
    - Profit Margin
    - Orders

    across discount levels.
    ```
    0%
    1 - 10%
    10 - 20%
    20 - 30%
    30%+
    ```
    The question becomes:

    **Are higher discounts actually generating enough additional sales to justify their impact on profitability?**

    That's a much more sophisticated business question.

5. **Which orders/products generate high revenue but low profit?**

    You have enough information to identify:

    ```
    High revenue + low profit
    High revenue + high profit
    Low revenue + high profit
    Low revenue + low profit
    ```

    This is useful for **identifying potentially problematic sales patterns**.

6. **What is the relationship between order size and profitability?**

    You have:

    ```
    total_items
    unique_products
    subtotal
    shipping_cost
    profit
    ```

    You can investigate:

    **Do larger orders generate disproportionately higher profit?**

    This could reveal **economies of scale or expensive shipping behavior**.

### Customer Analysis

Think:

`Acquisition` → `Value` → `Behavior` → `Retention`

Your dataset doesn't have a customer registration date or explicit retention field, so we shouldn't pretend we can perform a complete CRM/retention analysis.

1. **Which customer segments generate the most customer value?**

    Analyze by:
    
    ```
    customer_segment
    ```
    - Revenue
    - Profit
    - Orders
    - AOV
    - Revenue/customer
    - Profit/customer

2. **Who are the highest-value customers?**

    Identify customers based on:

    - Total revenue
    - Total profit
    - Number of orders
    - Average order value

    This lets you distinguish:

        high-spending customers

    from:

        high-frequency customers

    and:

        high-profit customers

    Those aren't necessarily the same people.

3. **How concentrated is revenue among customers?**

    This is a very good large-e-commerce question.

    For example:

    - What percentage of revenue comes from the top 1%, 5%, 10%, and 20% of customers?

    This can reveal customer concentration risk.

    You can potentially investigate a Pareto-style relationship:

    ```
    Top 10% customers → X% revenue
    Top 20% customers → Y% revenue
    ```

4. **Which customer acquisition channels produce the most valuable customers?**

    You have:

        customer_acquisition_channel

    So compare acquisition channels by:

    - Customers acquired
    - Orders
    - Revenue
    - Revenue/customer
    - Profit
    - Profit/customer
    - AOV

    This is significantly more useful than simply asking:

    "Which channel has the most customers?"

5. **Which campaigns attract the highest-value customers?**

    You have:

        campaign

    Analyze:

    - Number of customers
    - Orders
    - Revenue
    - AOV
    - Profit

    by campaign.

    A particularly useful comparison:

    **Customer volume vs. customer value**

    A campaign might acquire many customers but generate relatively little revenue per customer.

6. **What proportion of customers are repeat purchasers?**

    Because you have:

        customer_id
        order_id

    you can count orders per customer.

    For example:

        1 order → one-time customer
        2+ orders → repeat customer

    Then calculate:

    - **Repeat customer rate = repeat customers / total customers**

    This is a useful e-commerce KPI.

    > **Important:** this is a behavioral definition based on the available dataset; it isn't the same as formal cohort retention.

### Time Analysis

Think:

**Trend** → **Growth** → **Seasonality** → **Operational performance**

1. **How does revenue and profit change over time?**

    Analyze:

    - Revenue
    - Profit
    - Orders
    - AOV
    - Profit margin

    by:

    ```
    day
    week
    month
    quarter
    year
    ```

    depending on your dataset's time range.

2. **What are the company's growth trends?**

    Calculate:

    - **MoM growth**

    ```
    (Current Month Revenue - Previous Month Revenue)
    /
    Previous Month Revenue
    ```

    and, if enough historical data exists:

    - **YoY growth**

    ```
    (Current Year Revenue - Previous Year Revenue)
    /
    Previous Year Revenue
    ```

    This is much more useful to management than raw monthly revenue.

3. **Is there evidence of seasonality?**

    Compare performance by:

    - Month
    - Quarter
    - Day of week

    For example:

        Are certain months consistently stronger?

    or:

        Are weekends materially different from weekdays?

    **Don't claim "seasonality" from a very short dataset**. You need enough historical coverage to support that conclusion.

4. **When does the company receive its highest-value orders?**

    Analyze AOV and order volume by:

    - Month
    - Week
    - Day of week

    This separates:

        high order volume

    from:

        high-value purchasing periods

5. **How does operational performance change over time?**

    You have:

    ```
    order_date
    ship_date
    delivery_date
    delivery_status
    ```

    So you can calculate:

    - Order → Ship duration
    - Order → Delivery duration
    - Ship → Delivery duration

    Then investigate:

    **Is delivery performance improving or deteriorating over time?**

    This connects sales analytics with operations, which is valuable in e-commerce.

## Geography

1. **Which countries generate the most revenue and profit?**

    Compare:

    - Revenue
    - Orders
    - Customers
    - AOV
    - Profit
    - Profit margin

2. **Which regions have the highest customer value?**

    Analyze:

        - customer_region

    using:

    - Revenue/customer
    - Profit/customer
    - AOV
    - Orders/customer

    This is better than simply ranking regions by revenue.

3. **Which geographic markets have strong sales but weak profitability?**

    This is one of my favorite questions for your dataset.

    For example:

    ```
    Region A
    Revenue: $5M
    Profit margin: 4%

    Region B
    Revenue: $3M
    Profit margin: 18%
    ```

    A simple revenue ranking would say:

    Region A is better.

    A profitability analysis says:

    Region B may actually be economically more attractive.

4. **Are shipping costs disproportionately high in certain markets?**

    You have:

    ```
    shipping_cost
    customer_country
    customer_region
    ```

    So investigate:

    - Which geographic markets have the highest shipping cost per order and shipping cost as a percentage of order value?

    This can uncover operational inefficiencies.

5. Which cities are the most important markets?

    Rank cities by:

    - Revenue
    - Orders
    - Customers
    - Profit

    But don't stop there.

    Also consider:

    - Revenue per customer

    and:

    - Profit per customer.

    Otherwise large cities will naturally dominate simply because they have more customers.
