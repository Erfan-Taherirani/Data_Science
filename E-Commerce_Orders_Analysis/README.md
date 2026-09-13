# E-Commerce Orders Analysis

End-to-end analytics project transforming raw e-commerce transaction data into actionable business insights. Covers the full data lifecycle: profiling, cleaning, star-schema modeling, SQL-based analysis, and Power BI dashboarding.

> **Status:** Work in progress — core analysis complete; dashboard and advanced analytics ongoing.

---

## Project Overview

| Aspect | Details |
|--------|---------|
| **Domain** | E-commerce sales & profitability |
| **Dataset** | 50K orders, 27 columns, 4 raw tables (orders, order_items, customers, products) |
| **Period** | Single-year snapshot (2025) |
| **Key Metrics** | Revenue $5.76M • Orders 49,093 • Profit $1.64M • Margin 28.45% |
| **Segments** | Consumer (60.8%), Corporate (24%), Small Business (15.2%) |

---

## Repository Structure

```
E-Commerce_Orders_Analysis/
├── data/
│   ├── raw/                 # Original CSV files
│   ├── cleaned/             # Post-cleaning exports
│   └── processed/           # Star-schema fact/dim tables
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_audit.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_eda.ipynb
│   └── visualizations/
├── sql/
│   ├── 01_staging/          # Staging layer
│   ├── 02_transformations/  # Business logic
│   ├── 03_data_model/       # Fact & dimension tables
│   └── 04_analysis/         # Analytical queries by domain
├── docs/
│   ├── workflow.md          # 14-phase methodology
│   ├── data_dictionary.md
│   ├── 01_business_questions.md
│   ├── 02_data_quality_audit.md
│   ├── 03_data_cleaning.md
│   ├── 04_data_model.md
│   └── 05_sales_analysis.md
├── powerbi/                 # .pbip project (model + report)
├── src/                     # Reusable Python utilities
├── utils/                   # Data quality audit module
└── figures/                 # Exported charts
```

---

## Completed Work

| Phase | Deliverable |
|-------|-------------|
| **Data Understanding** | Business objectives, data dictionary, grain definition |
| **Data Quality Audit** | 50K rows profiled; 125 duplicates; 8 critical issues identified (negative shipping costs, date parsing, country duplication, payment_method inconsistency, systematic missingness) |
| **Data Cleaning** | Deduplication, type conversion, text normalization, formula-based imputation (discount, shipping), ML imputation for dual-missing values |
| **Star Schema Modeling** | 1 fact (`fact_orders`) + 9 dimensions (customers, dates, geo, channel, campaign, payment, discount band, flag, shipping) |
| **Sales Baseline Analysis** | Revenue, orders, AOV, profit, margin by segment/channel/time |
| **Customer Segment Analysis** | Consumer dominates volume; all segments share ~$117 AOV & ~28.5% margin |
| **Power BI Model** | Semantic model with relationships, DAX measures, report pages |

---

## Key Findings (to date)

- **Consumer segment drives 61% of revenue & profit** — volume-led, not margin-led
- **All three segments have nearly identical AOV (~$117) and margin (~28.5%)** — growth levers are acquisition/retention, not pricing
- **28.45% overall profit margin** — healthy baseline; discount impact analysis next
- **Data quality remediation recovered 1,004 discount values & fixed 123 negative shipping costs** via formula validation

---

## Tech Stack

- **Python:** pandas, numpy, scikit-learn (KNN imputation), matplotlib/seaborn
- **SQL:** PostgreSQL-flavored DDL/DML for staging, transformations, star schema
- **Power BI:** Star schema model, DAX measures, executive dashboard
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

> **Data:** Raw CSVs in `data/raw/`. Processed star-schema tables in `data/processed/`.

---

## Roadmap / Future Work

- [ ] **Discount impact analysis** — margin elasticity by discount band
- [ ] **Channel profitability** — marketplace vs. direct economics
- [ ] **Customer concentration (Pareto)** — top 10% revenue share
- [ ] **Acquisition channel ROI** — CAC vs. LTV proxy by channel
- [ ] **Time-series trends** — MoM/YoY growth, seasonality detection
- [ ] **Geographic shipping-cost audit** — high-cost/low-margin regions
- [ ] **Power BI dashboards** — Executive, Customer, Product, Operations
- [ ] **Automated validation pipeline** — Great Expectations / dbt tests
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