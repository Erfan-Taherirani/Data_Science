# E-Commerce Orders Data Warehouse Build Guide

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  orders_        │────▶│  stg_orders          │────▶│  stg_transformed_   │
│  cleaned.csv    │     │  (raw load)          │     │  orders (enriched)  │
└─────────────────┘     └──────────────────────┘     └──────────┬──────────┘
                                                                 │
                                    ┌────────────────────────────┼────────────────────────────┐
                                    ▼                            ▼                            ▼
                         ┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
                         │  DIMENSION TABLES │          │   FACT TABLE     │          │  DIMENSION TABLES │
                         │  (8 tables)       │          │  fact_orders     │          │  (8 tables)       │
                         └──────────────────┘          └──────────────────┘          └──────────────────┘
```

---

## Layer 1: Staging (`sql/01_staging/`)

### `01_stg_table_structure.sql`
Creates `stg_orders` with 26 columns matching CSV schema exactly.

| Category | Columns |
|----------|---------|
| Identifiers | order_id, customer_id |
| Dates | order_date, ship_date, delivery_date |
| Customer | name, segment, country, city, region |
| Order | status, total_items, unique_products |
| Financials | subtotal, discount_amount, shipping_cost, tax_amount, total_order_value, profit |
| Fulfillment | shipping_method, delivery_status |
| Payment | payment_method, payment_status |
| Marketing | sales_channel, customer_acquisition_channel, campaign |

### `02_stg_orders.sql`
```sql
INSERT INTO stg_orders SELECT * FROM orders_cleaned;
```
No transformation — pure landing zone.

---

## Layer 2: Transformations (`sql/02_transformations/transformations_orders.sql`)

Single statement with 3 CTEs → `stg_transformed_orders` (39 cols).

### CTE Flow
```
stg_orders
    │
    ▼
CTE_table_with_primary_key
    │  • order_key = RANK() OVER (ORDER BY order_id)
    │  • discount_rate = discount_amount / total_order_value * 100
    │  • profit_margin = profit / total_order_value * 100
    │  • revenue = total_order_value
    ▼
CTE_date_extractions (self-contained, joins on order_key)
    │  • year, month, day, week, week_day
    │  • month_name, day_name
    │  • days_to_ship = DATEDIFF(order_date, ship_date)
    │  • days_to_deliver = DATEDIFF(order_date, delivery_date)
    │  • ship_to_delivery_days = DATEDIFF(ship_date, delivery_date)
    ▼
CTE_discount_rate_level (self-contained, joins on order_key)
    │  • CASE discount_rate INTO 7 buckets: 0, 0-5%, 5-10%, 10-15%, 15-20%, 20-30%, 30%+
    ▼
stg_transformed_orders (final wide table)
```

---

## Layer 3: Data Model — Star Schema (`sql/03_data_model/`)

### Fact Table: `orders.fact_orders`

| Key | Type | Ref |
|-----|------|-----|
| order_key | INT PK | — |
| customer_key | INT FK | dim_customers |
| date_key | INT FK | dim_dates |
| geo_key | INT FK | dim_geo |
| channel_key | INT FK | dim_channel |
| payment_key | INT FK | dim_payment |
| discount_rate_level_key | INT FK | dim_discount_rate_level |
| flag_key | INT FK | dim_flag |
| campaign_key | INT FK | dim_campaign |

**Measures (14):** total_items, unique_products, subtotal, discount_amount, discount_rate, shipping_cost, tax_amount, revenue, profit, profit_margin, days_to_ship, days_to_deliver, ship_to_delivery_days

**Retained dates:** order_date, ship_date, delivery_date (for drill-through)

### Dimension Tables

| # | Table | Natural Key | Surrogate Key Logic |
|---|-------|-------------|---------------------|
| 1 | dim_customers | customer_id | RANK(customer_id) |
| 2 | dim_dates | order_date | RANK(order_date) |
| 3 | dim_geo | country+city+region | DENSE_RANK(country,city,region) |
| 4 | dim_channel | sales_channel+acquisition | RANK(sales,acquisition) |
| 5 | dim_payment | payment_method+status | RANK(method,status) |
| 6 | dim_flag | shipping_method+status | RANK(method,status) |
| 7 | dim_discount_rate_level | discount_rate_level | Hard-coded CASE 1–7 |
| 8 | dim_campaign | campaign | RANK(campaign) |

All dimensions use:
```sql
INSERT INTO dim_X
SELECT <key_gen>, * FROM (SELECT DISTINCT <attrs> FROM stg_transformed_orders) t;
```

### Fact Population
```sql
INSERT INTO fact_orders
SELECT t.order_key,
       dc.customer_key, dd.date_key, dg.geo_key, dch.channel_key,
       dp.payment_key, dr.discount_rate_level_key, df.flag_key, dca.campaign_key,
       t.<measures...>, t.order_date, t.ship_date, t.delivery_date
FROM stg_transformed_orders t
LEFT JOIN dim_customers dc ON t.customer_id = dc.customer_id
LEFT JOIN dim_dates dd ON t.order_date = dd.order_date
LEFT JOIN dim_geo dg ON t.customer_country = dg.customer_country ...
... (all 8 joins)
ORDER BY order_key;
```

---

## Run Sequence

| Step | Script | Output |
|------|--------|--------|
| 1 | `01_stg_table_structure.sql` | `stg_orders` table |
| 2 | `02_stg_orders.sql` | Raw data loaded |
| 3 | `transformations_orders.sql` | `stg_transformed_orders` |
| 4 | `dim_customers.sql` | `orders.dim_customers` |
| 5 | `dim_dates.sql` | `orders.dim_dates` |
| 6 | `dim_geo.sql` | `orders.dim_geo` |
| 7 | `dim_channel.sql` | `orders.dim_channel` |
| 8 | `dim_payment.sql` | `orders.dim_payment` |
| 9 | `dim_flag.sql` | `orders.dim_flag` |
| 10 | `dim_discount_rate_level.sql` | `orders.dim_discount_rate_level` |
| 11 | `dim_campaign.sql` | `orders.dim_campaign` |
| 12 | `fact_orders.sql` | `orders.fact_orders` |

Steps 4–11 can run in parallel.

---

## Data Quality & Conventions

| Aspect | Implementation |
|--------|----------------|
| Surrogate keys | INT, RANK()/DENSE_RANK(), deterministic |
| Money | DECIMAL(10,2) — no floating-point drift |
| Dates | DATE type; parts precomputed in dim_dates |
| NULLs | delivery_date nullable → lead times NULL when missing |
| Idempotency | `IF EXISTS DROP TABLE` before CREATE |
| Discount buckets | Fixed 7-level taxonomy, stable keys via CASE |
| Grain | Fact = 1 row per order (order_key) |

---

## Query Examples

**Revenue by month & segment:**
```sql
SELECT d.year, d.month_name, c.customer_segment, SUM(f.revenue) AS revenue
FROM fact_orders f
JOIN dim_dates d ON f.date_key = d.date_key
JOIN dim_customers c ON f.customer_key = c.customer_key
GROUP BY d.year, d.month_name, c.customer_segment;
```

**Avg days to deliver by geo:**
```sql
SELECT g.customer_country, g.customer_region, AVG(f.days_to_deliver) AS avg_days
FROM fact_orders f
JOIN dim_geo g ON f.geo_key = g.geo_key
WHERE f.days_to_deliver IS NOT NULL
GROUP BY g.customer_country, g.customer_region;
```

**Discount effectiveness:**
```sql
SELECT drl.discount_rate_level,
       COUNT(*) AS orders,
       AVG(f.profit_margin) AS avg_margin,
       SUM(f.revenue) AS total_revenue
FROM fact_orders f
JOIN dim_discount_rate_level drl ON f.discount_rate_level_key = drl.discount_rate_level_key
GROUP BY drl.discount_rate_level
ORDER BY drl.discount_rate_level_key;
```