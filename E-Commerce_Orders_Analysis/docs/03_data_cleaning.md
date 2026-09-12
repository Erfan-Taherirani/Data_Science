# Data Cleaning Documentation

**Dataset:** E-Commerce Orders  
**Source:** `data/raw/orders.csv`  
**Cleaning Date:** 2026-09-08  
**Notebook Reference:** `notebooks/data_cleaning.ipynb`  
**Audit Reference:** `docs/data_quality_audit.md`  
**Functions Module:** `src/eda.py`

---

## 1. Cleaning Pipeline Overview

| Step | Operation | Function | Rows Affected | Status |
|------|-----------|----------|---------------|--------|
| 1 | Load raw data & drop `product_categories` | — | 50,125 → 50,125 | ✅ |
| 2 | Remove exact duplicate rows | `drop_duplicates()` | 125 removed | ✅ |
| 3 | Verify `order_id` uniqueness | — | 0 duplicates | ✅ |
| 4 | Convert date columns to `datetime64` | `fix_data_types()` | 50,000 | ✅ |
| 5 | Normalize text: lowercase, strip, categorize | `fix_data_types()` | 50,000 | ✅ |
| 6 | Fix country semantic duplicate (USA → United States) | `fix_data_types()` | 823 | ✅ |
| 7 | Impute `customer_region` from `customer_country` | `fix_customer_country()` | 752 | ✅ |
| 8 | Fix negative `shipping_cost` (sign error) | `fix_negative_shipping_costs()` | 123 | ✅ |
| 9 | Identify ambiguous vs. unambiguous missing values | Custom logic | 12 dual-missing | ✅ |
| 10 | Impute unambiguous `discount_amount` via formula | `fix_missing_discounts()` | 623 | ✅ |
| 11 | Impute unambiguous `shipping_cost` via formula | `fix_missing_shipping_costs()` | 588 | ✅ |
| 12 | Validate financial formula integrity | Custom check | 50,000 | ✅ |

**Final Dataset:** 50,000 rows × 26 columns (excluding `product_categories`)

---

## 2. Data Type Conversions

| Column | Before | After | Method |
|--------|--------|-------|--------|
| `order_date` | str | datetime64[us] | `pd.to_datetime(format="mixed")` |
| `ship_date` | str | datetime64[us] | `pd.to_datetime(format="mixed")` |
| `delivery_date` | str | datetime64[us] | `pd.to_datetime(format="mixed")` |
| `customer_segment` | str | category | `.str.lower().astype("category")` |
| `customer_country` | str | category | `.replace({"USA": "United States"}).str.lower().astype("category")` |
| `customer_city` | str | category | `.str.lower().astype("category")` + `add_categories(['unknown'])` |
| `customer_region` | str | category | `.str.lower().astype("category")` |
| `order_status` | str | category | `.str.lower().astype("category")` |
| `shipping_method` | str | category | `.str.lower().astype("category")` |
| `delivery_status` | str | category | `.str.lower().astype("category")` |
| `payment_method` | str | category | `.str.lower().astype("category")` |
| `payment_status` | str | category | `.str.lower().astype("category")` |
| `sales_channel` | str | category | `.str.lower().astype("category")` |
| `customer_acquisition_channel` | str | category | `.str.lower().astype("category")` |
| `campaign` | str | category | `.str.lower().astype("category")` |
| `customer_name` | str | str | `.str.strip().str.lower()` |

---

## 3. Missing Value Treatment

### 3.1 Imputed via Business Logic (Deterministic)

| Column | Missing Before | Missing After | Method |
|--------|----------------|---------------|--------|
| `customer_region` | 752 (1.5%) | 0 | Mapped from `customer_country`: US/Canada → North America, UK/Germany → Europe, Australia → Oceania |
| `discount_amount` | 1,004 (2.0%) | 12 (0.03%) | Formula: `discount = subtotal + shipping_cost + tax_amount - total_order_value`; values < 0.01 → 0 |
| `shipping_cost` | 602 (1.2%) | 12 (0.03%) | Formula: `shipping = total_order_value - subtotal - tax_amount + discount_amount`; values < 0.01 → 0 |

### 3.2 Remaining Missing (Accepted as Structural)

| Column | Missing Count | Missing % | Reason |
|--------|---------------|-----------|--------|
| `ship_date` | 8,526 | 17.0% | Cancelled/Processing orders never ship |
| `delivery_date` | 13,401 | 26.8% | Includes all missing ship_date + Shipped-not-delivered |
| `customer_city` | 1,000 | 2.0% | Random; imputable but not critical |
| `delivery_status` | 500 | 1.0% | Predictable from order_status/ship_date |
| `payment_method` | 400 | 0.8% | Case variants + random missing |
| `campaign` | 41,469 | 82.9% | Expected: campaigns are time-limited |

---

## 4. Data Quality Fixes

### 4.1 Duplicate Removal
- **Exact row duplicates:** 125 removed via `drop_duplicates(keep="first", ignore_index=True)`
- **Business key duplicates (`order_id`):** 0 remaining after deduplication

### 4.2 Negative Shipping Costs
- **Count:** 123 rows with `shipping_cost < 0`
- **Root cause:** Data entry sign error
- **Fix:** `df.loc[negative_indices, 'shipping_cost'] *= -1`
- **Validation:** All `shipping_cost >= 0` post-fix

### 4.3 Country Standardization
- **Issue:** "USA" (823 rows) vs "United States" semantic duplicate
- **Fix:** `replace({"USA": "United States"})` + lowercase
- **Result:** 5 countries: united states, canada, united kingdom, germany, australia

---

## 5. Financial Formula Validation

The core business rule validated post-cleaning:

```
total_order_value = subtotal + shipping_cost + tax_amount - discount_amount
```

| Validation Rule | Result |
|-----------------|--------|
| Formula holds for all rows | ✅ 100% match (within floating-point tolerance) |
| `shipping_cost >= 0` | ✅ 100% true |
| `discount_amount >= 0` | ✅ 100% true |
| `discount_amount <= total_order_value` | ✅ 100% true |
| `total_items > 0` | ✅ 100% true |
| `unique_products > 0` | ✅ 100% true |
| `profit <= total_order_value` | ✅ 100% true |
| `order_id` unique | ✅ 50,000 distinct |

---

## 6. Function Reference (`src/eda.py`)

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `fix_data_types(df)` | Convert dates, normalize text, categorize | DataFrame | Status string |
| `fix_customer_country(df)` | Impute region from country mapping | DataFrame | Status string |
| `fix_negative_shipping_costs(df)` | Absolute value for negative shipping | DataFrame | Status string |
| `fix_missing_discounts(df, indices)` | Compute discount via formula | DataFrame, Index | Status string |
| `fix_missing_shipping_costs(df, indices)` | Compute shipping via formula | DataFrame, Index | Status string |

---

## 7. Ambiguous Samples Handling

| Scenario | Count | Resolution |
|----------|-------|------------|
| Both `discount_amount` & `shipping_cost` missing | 12 | Excluded from formula imputation; require ML imputation (future work) |
| Only `discount_amount` missing | 623 | Imputed via formula |
| Only `shipping_cost` missing | 588 | Imputed via formula (after discount fix) |

---

## 8. Output

**Cleaned dataset saved to:** `data/processed/orders_cleaned.csv`  
**Schema:** 49,988 rows × 26 columns  
**Memory:** ~5.9 MB (down from 10.3 MB via categorical encoding)

---

## 9. Reproducibility

```python
import pandas as pd
from src.eda import (
    fix_data_types, fix_customer_country, fix_negative_shipping_costs,
    fix_missing_discounts, fix_missing_shipping_costs
)

df = pd.read_csv("data/raw/orders.csv").drop(columns="product_categories")
df = df.drop_duplicates(keep="first", ignore_index=True)

fix_data_types(df)
fix_customer_country(df)
fix_negative_shipping_costs(df)

# Identify unambiguous samples
ambiguous = df[df['discount_amount'].isnull()]['shipping_cost'][
    df[df['discount_amount'].isnull()]['shipping_cost'].isnull()
].index
unambiguous = [i for i in df.index if i not in ambiguous]

fix_missing_discounts(df, df.loc[unambiguous, 'discount_amount'][
    df.loc[unambiguous, 'discount_amount'].isnull()].index)

fix_missing_shipping_costs(df, [
    i for i in df.loc[df['shipping_cost'].isnull(), 'shipping_cost'].index
    if i not in ambiguous
])

# Validate
assert len(df) == 50000
assert df['order_id'].nunique() == 50000
assert (df['shipping_cost'] >= 0).all()
assert (df['discount_amount'] >= 0).all()
```

---

*Documentation generated from `notebooks/data_cleaning.ipynb` and `src/eda.py`*