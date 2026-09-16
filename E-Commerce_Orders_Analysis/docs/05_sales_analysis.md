# 01. Overall Sales Performance — Baseline

## Business Question

**How is the overall sales performance evolving?**

## Objective

Establish the overall sales and profitability baseline across the full dataset to provide a reference point for subsequent time-based and segment-level analysis.

## Key Metrics

| Metric                    |      Result |
| ------------------------- | ----------: |
| Total Revenue             |  **$5.76M** |
| Total Orders              |  **49,093** |
| Total Items Sold          | **161,370** |
| Average Order Value (AOV) | **$117.23** |
| Revenue per Item          |  **$35.66** |
| Total Profit              |  **$1.64M** |
| Profit Margin             |  **28.45%** |

## Interpretation

The business generated **$5.76M in revenue from 49,093 orders**, selling approximately **161K items** during the analyzed period.

The average order generated **$117.23 in revenue**, while each item generated approximately **$35.66 in revenue** on average. With **$1.64M in total profit** and a **28.45% profit margin**, the business retained approximately **$0.28 of profit for every $1.00 of revenue**.

Overall, the results indicate a **strong baseline level of sales activity and profitability**. However, these aggregate figures alone do not show whether sales performance is **improving, declining, or remaining stable over time**.

## Business Implication

This baseline provides the reference point for deeper analysis of **sales trends, customer segments, product performance, and geographic performance**. In particular, the next step should be to examine revenue, order volume, AOV, and profit **over time** to determine the direction and drivers of business performance.

## Conclusion

**The business generated $5.76M in revenue and $1.64M in profit at a 28.45% margin across 49,093 orders.** The overall business is profitable with an average order value of $117.23. However, determining how sales performance is *evolving* requires a time-series analysis rather than aggregate totals alone.


# 02. Which customer segments generate the most revenue and profit?

### Key Finding

The **Consumer segment is the largest revenue and profit contributor**, generating **$3.50M in revenue** and **$996.45K in profit**. It accounts for **60.8% of all orders** and contributes approximately **61.5% of total profit**.

The **Corporate segment** ranks second, generating **$1.38M in revenue** and **$393.25K in profit**, while **Small Business** generates **$871.41K in revenue** and **$247.63K in profit**.

### Segment Performance

| Segment            |  Revenue | Order Share |   Profit | Profit Margin |
| ------------------ | -------: | ----------: | -------: | ------------: |
| **Consumer**       |   $3.50M |       60.8% | $996.45K |         28.5% |
| **Corporate**      |   $1.38M |       24.0% | $393.25K |         28.5% |
| **Small Business** | $871.41K |       15.2% | $247.63K |         28.4% |

### Interpretation

* **Consumer is the dominant segment by scale**, generating more than half of total revenue, orders, and profit.
* **Corporate is the second-largest contributor**, while Small Business contributes the least in absolute revenue and profit.
* The segments have **very similar AOVs (~$117)** and **profit margins (~28.4–28.5%)**. Therefore, the substantial differences in total revenue and profit are primarily associated with **order volume rather than materially different transaction economics**.
* Consumer's strong performance is therefore driven mainly by its much larger customer/order volume rather than higher value per order or a superior profit margin.

<img src="../figures/revenue_and_profit_by_customer_segments.png" width="700">

### Business Implication

The Consumer segment should remain a **primary focus for revenue and profit retention and growth**, given its substantial contribution to overall business performance. At the same time, the relatively similar AOV and profit margins across segments suggest that **increasing order volume within Corporate and Small Business could provide additional growth opportunities without requiring fundamentally different unit economics**.

### Conclusion

**Consumer is the most valuable customer segment in absolute terms**, contributing the largest share of both revenue and profit. However, **no segment demonstrates a meaningful advantage in AOV or profit margin**. The key differentiator between segments is therefore **sales volume**, making order growth and customer acquisition/retention the most relevant areas for further segment-level analysis.

SQL results:

rank | customer_segment | revenue | orders | orders_percentage | AOV | profit | profit_margin
--- | --- | --- | --- | --- | --- | --- | ---
1 | consumer | $3,502,369.34 | 29863 | %60.8 | $117.28 | $996,450.15 | 0.285
2 | corporate | $1,381,734.68 | 14631 | %24.0 | $117.28 | $393,250.00 | 0.285
3 | small_business | $871,410.42 | 15219 | %15.2 | $117.28 | $247,630.00 | 0.284

# 03. Which Sales Channel Performs Best?

### Business Objective

Compare sales channels based on **order volume, revenue contribution, profit contribution, AOV, and profit margin** to understand differences in channel scale and transaction performance.

### Key Metrics

| Sales Channel    | Orders | Order Share |         AOV |  Revenue | Revenue Share |   Profit | Profit Share | Profit Margin |
| ---------------- | -----: | ----------: | ----------: | -------: | ------------: | -------: | -----------: | ------------: |
| **Website**      | 24,458 |      49.82% |     $117.38 |   $2.87M |        49.88% | $817.98K |       49.96% |           28% |
| **Mobile App**   | 14,778 |      30.10% |     $117.36 |   $1.73M |        30.14% | $493.67K |       30.15% |           28% |
| **Marketplace**  |  7,393 |      15.06% |     $115.38 | $853.03K |        14.82% | $240.89K |       14.71% |           28% |
| **Social Media** |  2,464 |       5.02% | **$120.51** | $296.94K |         5.16% |  $84.78K |        5.18% |       **29%** |

### Interpretation

The **Website is the largest sales channel by scale**, generating approximately **50% of total orders, revenue, and profit**. The **Mobile App** is the second-largest channel, contributing around **30%** across the same measures. Together, these two channels account for approximately **80% of the company's orders, revenue, and profit**.

The channels show relatively similar transaction economics. **Social Media has the highest AOV ($120.51)**, while **Marketplace has the lowest ($115.38)**. Social Media also has the highest reported profit margin at approximately **29%**, compared with approximately **28%** for the other channels.

However, Social Media currently represents only **5.02% of orders and 5.16% of revenue**. Therefore, its higher AOV and slightly higher margin have not translated into a large absolute contribution to revenue or profit.

Overall, the results show a clear distinction between **scale and efficiency**: Website and Mobile App drive the majority of business volume, while Social Media shows somewhat stronger transaction-level metrics but at substantially lower volume.

<img src="../figures/sales_channels_by_revenue_and_profit.png" width="700">

### Business Implication

The company should **maintain the Website and Mobile App as the primary sales channels based on their current contribution to revenue and profit**.

Social Media represents a potential **growth opportunity** because it currently combines the highest AOV and profit margin with relatively low order volume. However, the current analysis is not sufficient to conclude that increasing investment in Social Media will produce the highest incremental return.

A further analysis of **customer acquisition cost, conversion rate, customer lifetime value, growth trends, and incremental profit by channel** would be required before making an investment decision.

### Conclusion

**Website currently leads in absolute revenue and profit contribution**, followed by Mobile App. Together, they generate approximately **80% of the company's orders, revenue, and profit**.

**Social Media has the highest AOV and slightly higher profit margin, but its low order volume limits its current contribution.** This makes it a channel worth investigating for growth, while the current data does not yet establish that it should receive greater investment than the other channels.
