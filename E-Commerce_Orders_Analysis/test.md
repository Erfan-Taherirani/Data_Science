# 04. How does discounting affect revenue and profitability?

## Business Question

**Are higher discounts actually generating enough additional sales to justify their impact on profitability?**

## Objective

Measure how revenue, order volume, AOV, and profitability change across discount bands (0%, 1–10%, 10–20%, 20–30%, 30%+) to determine whether discounting drives incremental sales or erodes margin.

## Inputs

Required columns (from `fact_orders` + `dim_discount_rate_level`):

- `discount_rate`
- `discount_rate_level`
- `order_key` (orders)
- `revenue`
- `profit`

Measures produced:

- orders
- order share
- AOV
- revenue / revenue share
- profit / profit share
- profit margin
- items per order

## Key Metrics

| Discount Band | Orders | Order Share |      AOV |   Revenue | Revenue Share |   Profit | Profit Share | Profit Margin | Items per Order |
| ------------- | -----: | ----------: | -------: | --------: | ------------: | -------: | -----------: | ------------: | --------------: |
| **0%**        | 27,177 |      55.36% | **$126.31** |   $3.43M |        59.65% |   $1.13M |       69.05% |   **32.93%** |            3.28 |
| **1–10%**     |  5,554 |      11.31% |   $107.53 | $597.21K |        10.38% | $165.61K |       10.11% |        27.73% |            3.13 |
| **10–20%**    |  8,083 |      16.46% |   $103.36 | $835.43K |        14.52% | $195.80K |       11.96% |        23.44% |            3.20 |
| **20–30%**    |  5,953 |      12.13% |   $101.84 | $606.24K |        10.53% | $106.75K |        6.52% |        17.61% |            3.37 |
| **30%+**      |  2,326 |       4.74% |   $121.88 | $283.49K |         4.93% |  $38.63K |        2.36% |        13.63% |            3.78 |

## Interpretation

* **Profit margin declines monotonically with discount depth** — from 32.93% on non-discounted orders to 13.63% on orders discounted 30%+. Each additional discount tier costs roughly 2–6 points of margin.
* **Deeper discounts do not lift order value.** AOV is highest on non-discounted orders ($126.31) and actually drops in the mid bands ($101.84–$107.53); only the 30%+ band recovers part of the gap ($121.88), likely reflecting large bulk orders that were discounted for volume rather than pulled in by promotion.
* **Basket size increases only marginally with discounting** — items per order rises from 3.28 to 3.78 (+15%) at 30%+, far too small to offset the ~19-point margin erosion.
* **Discounted orders (44.6% of volume) contribute only 31% of profit**, with the 20%+ bands alone destroying margin on 16.9% of all orders while returning just 8.9% of total profit.

## Business Implication

The current discounting strategy appears to be **trading margin for volume without clear incremental return**. Since discounted orders show no meaningful AOV or basket-size lift, the additional sales they generate are unlikely to compensate for the lost profitability. Recommendations:

1. **Audit and cap the 20%+ discount tiers** — they represent only 16.9% of orders yet cost ~21 points of relative margin.
2. **Reserve deeper discounts for inventory-clearance or bulk-price scenarios** rather than blanket promotion.
3. **Test shallower discounts (1–10%)** as the default promotion level, where margin retention (27.73%) stays close to baseline.

## Conclusion

**Discounting reduces profitability at every level without measurably increasing order value or basket size.** Non-discounted orders are both the most common (55.4%) and the most profitable (32.93% margin) — higher discounts are not generating enough incremental sales to justify their cost.

---

## Note on Data Quality

`fact_orders.discount_rate_level_key` contains NULLs (13,637 rows) and out-of-range keys (6, 7 — 8,279 rows) that do not join to `dim_discount_rate_level` (keys 1–5). The figures above therefore derive `discount_rate_level` directly from `discount_rate` using the same banding logic defined in `dim_discount_rate_level.sql`. The fact-table key mapping should be regenerated before relying on dim-based joins for this analysis.

---

SQL results:

| discount_rate_level | orders | order_share | revenue | revenue_share | profit | profit_share | AOV | profit_margin | items_per_order |
| ------------------- | -----: | ----------: | ------: | ------------: | -----: | -----------: | --: | ------------: | --------------: |
| 0                   |  27177 |       55.36 | 3432761.27 |         59.65 | 1130540.98 |        69.05 | 126.31 |         32.93 |            3.28 |
| 1-10%               |   5554 |       11.31 |  597208.37 |         10.38 |  165610.51 |        10.11 | 107.53 |         27.73 |            3.13 |
| 10-20%              |   8083 |       16.46 |  835425.84 |         14.52 |  195796.54 |        11.96 | 103.36 |         23.44 |            3.20 |
| 20-30%              |   5953 |       12.13 |  606237.88 |         10.53 |  106751.26 |         6.52 | 101.84 |         17.61 |            3.37 |
| 30%+                |   2326 |        4.74 |  283489.93 |          4.93 |   38629.93 |         2.36 | 121.88 |         13.63 |            3.78 |
