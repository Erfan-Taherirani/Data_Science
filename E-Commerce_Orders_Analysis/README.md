# E-Commerce Orders Analysis

End-to-end analytics project transforming raw e-commerce transaction data into actionable business insights. Covers the full data lifecycle: profiling, cleaning, star-schema modeling, SQL-based analysis, and Power BI dashboarding.

> **Status:** Work in progress — data pipeline, star schema, and four analyses (baseline, segments, channels, discounts) complete; first Power BI report page live. Customer/time/geography analysis and remaining dashboard pages ongoing.

---

## Project Overview

| Aspect | Details |
|--------|---------|
| **Domain** | E-commerce sales & profitability |
| **Dataset** | 50,125 raw orders (27 columns) → **49,093 clean orders** after dedup & cleaning; 4 raw tables (orders, order_items, customers, products) |
| **Period** | Order dates spanning 2024–2026 |
| **Key Metrics** | Revenue $5.76M • Orders 49,093 • Profit $1.64M • Margin 28.45% |
| **Segments** | Consumer (60.8%), Corporate (24%), Small Business (15.2%) |

---

## Repository Structure

```
E-Commerce_Orders_Analysis/
├── data/
│   ├── raw/                 # Original CSV files (orders, order_items, customers, products)
│   ├── cleaned/             # orders_cleaned.csv — post-cleaning export
│   └── processed/           # Star-schema exports (fact_orders + 8 dims) & analysis result CSVs
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_audit.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_eda.ipynb               # placeholder — EDA not started
│   └── visualizations/
│       └── sales_analysis.ipynb   # Charts for completed analyses
├── sql/
│   ├── 01_staging/          # stg_orders structure + raw load
│   ├── 02_transformations/  # stg_transformed_orders (surrogate keys, date parts, discount bands)
│   ├── 03_data_model/       # fact_orders + 8 dimension tables
│   ├── 04_analysis/
│   │   └── sales/           # Baseline, customer segments, channels, discount queries
│   │                        # (customers/, geography/, time/ placeholders — planned)
│   └── 05_validation/       # (planned) reconciliation checks
├── docs/
│   ├── workflow.md          # 14-phase methodology
│   ├── data_dictionary.md
│   ├── 01_business_questions.md
│   ├── 02_data_quality_audit.md
│   ├── 03_data_cleaning.md
│   ├── 04_data_model.md
│   └── 05_sales_analysis.md
├── powerbi/                 # .pbip project (semantic model + report)
├── src/eda.py               # Reusable cleaning & validation functions
├── utils/                   # Data quality audit helpers
├── figures/                 # Exported charts (segments, channels)
└── test.md                  # Discount impact analysis write-up (to be moved into docs/)
```

---

## Completed Work

| Phase | Deliverable |
|-------|-------------|
| **Data Understanding** | Business objectives, data dictionary, grain definition (one row = one order) |
| **Data Quality Audit** | 50,125 rows profiled; 125 duplicates; issues identified: date columns typed as strings, negative shipping costs, USA/United States duplication, payment_method case inconsistency, systematic missingness |
| **Data Cleaning** | Dedup → 50,000; datetime conversion; text/categorical normalization; formula-based imputation of 623 discounts & 588 shipping costs; 123 negative shipping costs fixed; city gaps filled with "unknown"; dropped 907 rows (12 ambiguous dual-missing + null delivery_status/payment_method) → **49,093 orders** |
| **Star Schema Modeling** | 1 fact (`fact_orders`) + **8 dimensions** (customers, dates, geo, channel, payment, discount band, flag, campaign) |
| **Sales Baseline Analysis** | Revenue $5.76M, AOV $117.23, margin 28.45% ([docs/05](docs/05_sales_analysis.md)) |
| **Customer Segment Analysis** | Consumer drives ~61% of revenue & profit; all segments share ~$117 AOV & ~28.5% margin |
| **Sales Channel Analysis** | Website + Mobile App ≈ 80% of volume; Social Media has the highest AOV & margin but only ~5% share |
| **Discount Impact Analysis** | Margin falls monotonically from 32.9% (0%) to 13.6% (30%+) with no AOV or basket-size lift ([write-up](test.md), [SQL](sql/04_analysis/sales/04_discount_analysis.sql)) |
| **Power BI Model** | Semantic model (fact + 8 dims; DAX measures: AOV, Revenue per Item, Profit Margin) + first report page `sales_performance` |

---

## Key Findings (to date)

- **Consumer segment drives 61% of revenue & profit** — volume-led, not margin-led
- **All three segments have nearly identical AOV (~$117) and margin (~28.5%)** — growth levers are acquisition/retention, not pricing
- **Website and Mobile App generate ~80% of orders, revenue, and profit**; Social Media shows the highest AOV ($120.51) and margin (~29%) but only ~5% of volume — a growth candidate, pending CAC/LTV analysis
- **Discounting erodes margin without lifting order value** — non-discounted orders are 55% of volume but 69% of profit (32.9% margin); 30%+ discounted orders return just 2.4% of profit at 13.6% margin
- **Data quality remediation recovered 1,211 missing financial values** (discounts & shipping) via formula validation and fixed 123 negative shipping costs

---

## Known Issues

- **`fact_orders.discount_rate_level_key` mapping is unreliable** — 13,637 NULLs and 8,279 rows with out-of-range keys (6–7) that don't join `dim_discount_rate_level` (keys 1–5). The discount analysis therefore derives bands directly from `discount_rate`; the fact-table key mapping should be regenerated before dim-based joins are trusted.
- **12 ambiguous orders** (both `discount_amount` and `shipping_cost` missing) were dropped; ML imputation is planned.
- **`ship_date`/`delivery_date` missingness is structural** — Cancelled/Processing orders never ship; in-transit orders have no delivery date yet.
- **`campaign` is 82.9% missing by design** — campaigns are time-boxed; kept for campaign-specific analysis only.

---

## Tech Stack

- **Python:** pandas, numpy, matplotlib, seaborn (pinned in `requirements.txt`); scikit-learn planned for ML imputation
- **SQL:** SQL Server (T-SQL) — staging, transformations, star-schema DDL/DML, analytical queries
- **Power BI:** `.pbip` project (TMDL semantic model, DAX measures, report)
- **Documentation:** Markdown + Mermaid diagrams

---

## Getting Started

```bash
# Clone
git clone https://github.com/<your-username>/E-Commerce_Orders_Analysis.git
cd E-Commerce_Orders_Analysis

# Install dependencies
pip install -r requirements.txt

# Run notebooks in order
jupyter lab notebooks/
```

**Pipeline order:**
1. Notebooks `01 → 03` (Python profiling & cleaning) → `data/cleaned/orders_cleaned.csv`
2. Load the cleaned CSV into SQL Server, then run `sql/` in numbered order: `01_staging` → `02_transformations` → `03_data_model` (dimensions can run in parallel, then `fact_orders.sql`) → `04_analysis`
3. Open `powerbi/e-commerce_orders_analysis.pbip` for the semantic model & report

> **Data:** Raw CSVs in `data/raw/`. Star-schema exports in `data/processed/`.

---

## Roadmap / Future Work

- [x] **Discount impact analysis** — margin elasticity by discount band ✅
- [ ] **Fix `discount_rate_level_key` mapping** in the fact table (NULLs + out-of-range keys)
- [ ] **Customer analysis** — value, concentration (Pareto), acquisition-channel ROI, repeat-purchase rate
- [ ] **Time-series trends** — MoM/YoY growth, seasonality, delivery-performance over time
- [ ] **Geographic analysis** — country/region/city value and shipping-cost audit
- [ ] **EDA notebook** — fill in `04_eda.ipynb`
- [ ] **ML imputation** — ambiguous discount/shipping rows, `delivery_status`, `payment_method`
- [ ] **Power BI dashboards** — Executive, Customer, Product, Operations pages
- [ ] **Automated validation pipeline** — `05_validation` queries, Great Expectations / dbt tests
- [ ] **dbt project** — modular, tested, documented transformations

---

## Methodology

This project follows a structured 14-phase workflow (see [`docs/workflow.md`](docs/workflow.md)) emphasizing:
1. **Understand before cleaning** — business questions first
2. **Audit before transforming** — documented quality issues with root causes
3. **Formula-first imputation** — ML only where deterministic logic fails
4. **Star schema in SQL** — reproducible, version-controlled modeling
5. **Analysis tied to decisions** — every query maps to a business action

---

## Contact

**Author:** Erfan Taherirani — Junior Data Analyst

**LinkedIn:** [LinkedIn](https://www.linkedin.com/in/erfan-taherirani)

**Email:** e.taherirani81@gmail.com

---

*This project demonstrates production-grade analytical engineering: rigorous data quality, dimensional modeling, SQL-first transformations, and stakeholder-ready visualizations.*
