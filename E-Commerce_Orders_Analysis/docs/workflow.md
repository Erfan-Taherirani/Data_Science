# Workflow

for this project I will use the following 14 steps workflow:

| **Phase** | **Description** | **Status** |
| --- | --- | --- |
| **1** | Data Understanding | planning |
| **2** | Data Quality Audit (Profile + Diagnose) | Planning |
| **3** | Deduplication (Grain/Keys) | not started |
| **4** | Data Cleaning (Types / Nulls / Rules) | not started |
| **5** | Data Validation (Quality Checks) | not started |
| **6** | Data Modeling (Star Schema / Fact + Dimensions) | not started |
| **7** | SQL Transformations (Analytical Tables) | not started |
| **8** | Business Questions (KPI Definitions) | not started |
| **9** | Exploratory Analysis (Python + SQL) | not started |
| **10** | Power BI Model (Relationships + DAX) | not started |
| **11** | Dashboards (Executive / Product / Customer) | not started |
| **12** | Insights (Findings + Actions) | not started |
| **13** | Final Validation (Reconciliation) | not started |
| **14** | Documentation (README + Data Model) | not started |

## Phase 1: Data Understanding

This phase is about understanding the data and the business questions that we want to answer. I should have documented:

- Business objective
- Business questions
- Dataset/table overview
- Column/data dictionary
- Data types
- Dataset size
- Grain
- Primary keys / business keys
- Relationships
- Categorical vs. numerical fields
- Date/time fields
- Measures vs. dimensions
- Business meaning of important fields
- Potential data-quality risks
- Initial assumptions and constraints

## Phase 2: Data Quality Audit (Profile + Diagnose)

This phase is about understanding the data and the business questions that we want to answer. The Python notebook should answer:

### Structural Quality

- Number of rows
- Number of columns
- Data types
- Memory Usage
- Unique Values

### Missingness

for each column, answer:
- Missing Count
- Missing Percentage

### Duplicates

check:
- full-row duplicates
- business-key duplicates
- unexpected duplicates

### Validity

- quantity <= 0
- price <= 0
- discount < 0
- discount > 100
- negative revenue
- invalid dates
- future dates
- invalid categories
- invalid IDs

### Consistency

- Data Logic Checks
- Check the quality of the string columns

### Referential integrity

make sure the relationships makes sense.

### Deliverable

create a `data_quality_report.md` something like this:
```
Dataset
-------
Rows: 50,000
Columns: 18

Issues detected
---------------
Duplicate rows: 127
Missing customer IDs: 0.4%
Missing product categories: 0.1%
Invalid quantities: 12
Invalid prices: 0
Invalid dates: 3

Business-rule violations
------------------------
Subtotal mismatches: 24
...
```

## Phase 3: Deduplication

- Type 1: drop exact duplicates
- Type 2: drop business key duplicates

## Phase 4: Data Cleaning

### A. Structural Cleaning

- Correct data types
- Standardize column names
- Parse dates
- Remove unnecessary columns
- Normalize categorical values

### B. Missing Value Treatment

### C. Business Rule Validation

### D. Outlier Investigation

Don't blindly drop the detected outliers and analyze them, I could be a valid big purchase or an error. After investigation decide what to do with the outliers.

## Phase 5: Create the Analytical Dataset (in SQL)

```
Raw CSV
   ↓
Python quality investigation
   ↓
Cleaned data
   ↓
SQL staging
   ↓
SQL transformations
   ↓
Analytical model
```

In this phase we have 3 steps and we use SQL to do the transformations, joins, and aggregations and then build and analytical model.
- step 1: **SQL Staging**
- step 2: **SQL Transformations**
- step 3: **Analytical Model**

> **Fact Table:** Contains business events / measurements.

> **Dimension Table:** Contains descriptive context.

## Phase 6: Data Modeling

We use star scheme for this project to model the data.

## Phase 7: Analytical SQL - Business Question Design

Once your model exists, start asking business questions.

**What decisions could an e-commerce management team make using this data?**

### Workflow from business questions to insights:
1. Business Objective
2. Business Question
3. Required KPIs / Metrics
4. Required Columns
5. Define Analytical / Aggregation Grain
6. Write SQL Query
7. Validate Results
8. Interpret Results
9. Select Appropriate Visualization
10. Derive Business Insights / Implications

The suggested sql folder structure is:
```
sql/
│
├── 01_staging/
│
├── 02_transformation/
│
├── 03_data_model/
│
├── 04_analysis/
│   │
│   ├── sales/
│   │   ├── sales_performance.sql
│   │   ├── channel_analysis.sql
│   │   └── discount_analysis.sql
│   │
│   ├── customers/
│   │   ├── customer_value.sql
│   │   ├── customer_concentration.sql
│   │   └── acquisition_analysis.sql
│   │
│   ├── time/
│   │   ├── sales_trends.sql
│   │   ├── growth_analysis.sql
│   │   └── delivery_trends.sql
│   │
│   └── geography/
│       ├── country_analysis.sql
│       ├── region_analysis.sql
│       └── shipping_cost_analysis.sql
│
└── 05_validation/
```

### Power BI Workflow
Power BI workflow is like:

```
Load the cleaned data
   ↓
Build the data model
   ↓
Build the measures
   ↓
Build the relationships
   ↓
Create needed dashboards
```