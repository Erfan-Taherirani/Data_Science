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

