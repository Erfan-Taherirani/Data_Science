# Data Card — Telecom Customer Churn Dataset

## 1. Dataset Summary

| Item                             | Description                                                     |
| -------------------------------- | --------------------------------------------------------------- |
| **Dataset name**                 | Telecom Churn Dataset                                           |
| **Source**                       | Kaggle — Baligh Mnassri                                         |
| **Source URL**                   | https://www.kaggle.com/datasets/mnassrib/telecom-churn-datasets |
| **Original dataset description** | Cleaned Orange Telecom Customer Churn Dataset                   |
| **Rows**                         | 3,333 customers                                                 |
| **Columns**                      | 20                                                              |
| **Predictors**                   | 19                                                              |
| **Target**                       | `Churn`                                                         |
| **Task**                         | Binary classification                                           |
| **Missing values**               | None reported                                                   |
| **Dataset purpose**              | Learning / ML portfolio                                         |
| **Temporal structure**           | Static customer-level snapshot; no timestamp                    |
| **Granularity**                  | One row per customer                                            |
| **Primary use case**             | Customer churn analysis and prediction                          |

Kaggle's associated documentation states that each row represents a customer and that `Churn` is the target variable.

---

## 2. Intended Use

### Intended uses

This dataset is appropriate for:

* Exploratory analysis of customer churn patterns
* Binary classification modeling
* Feature engineering practice
* Model comparison and evaluation
* Imbalanced-class classification practice
* Model interpretability and feature importance analysis
* Building a portfolio-level end-to-end ML project

### Out-of-scope uses

This dataset should **not** be treated as evidence for:

* Current telecom-market behavior
* Real-world churn rates of a specific telecom operator
* Causal conclusions about why customers churn
* Production deployment without additional validation
* Temporal churn forecasting without a documented prediction horizon

---

## 3. Target Variable

The target is:

**`Churn`**

It indicates whether the customer churned.

| Class                   |     Count |    Share |
| ----------------------- | --------: | -------: |
| `False` — did not churn |     2,850 |   85.51% |
| `True` — churned        |       483 |   14.49% |
| **Total**               | **3,333** | **100%** |

### Class balance

The dataset is **imbalanced**, with approximately **5.9 non-churned customers for every churned customer**.

Therefore, accuracy should not be used as the sole evaluation metric.

Recommended metrics:

* Precision
* Recall
* F1-score
* ROC-AUC
* **PR-AUC**
* Confusion matrix

For a churn-retention use case, threshold selection should ultimately consider the relative business cost of false positives and false negatives.

---

## 4. Feature Groups

### Customer / Account

| Feature          | Type        | Description                           |
| ---------------- | ----------- | ------------------------------------- |
| `State`          | Categorical | US state associated with the customer |
| `Account length` | Numeric     | Length of the customer's account      |
| `Area code`      | Categorical | Customer's telephone area code        |

### Service Subscriptions

| Feature                 | Type               | Description                                            |
| ----------------------- | ------------------ | ------------------------------------------------------ |
| `International plan`    | Binary categorical | Whether the customer has an international calling plan |
| `Voice mail plan`       | Binary categorical | Whether the customer has a voicemail plan              |
| `Number vmail messages` | Numeric            | Number of voicemail messages                           |

### Daytime Usage

| Feature             | Type    | Description                          |
| ------------------- | ------- | ------------------------------------ |
| `Total day minutes` | Numeric | Total daytime call minutes           |
| `Total day calls`   | Numeric | Number of daytime calls              |
| `Total day charge`  | Numeric | Charge associated with daytime usage |

### Evening Usage

| Feature             | Type    | Description                          |
| ------------------- | ------- | ------------------------------------ |
| `Total eve minutes` | Numeric | Total evening call minutes           |
| `Total eve calls`   | Numeric | Number of evening calls              |
| `Total eve charge`  | Numeric | Charge associated with evening usage |

### Night Usage

| Feature               | Type    | Description                            |
| --------------------- | ------- | -------------------------------------- |
| `Total night minutes` | Numeric | Total nighttime call minutes           |
| `Total night calls`   | Numeric | Number of nighttime calls              |
| `Total night charge`  | Numeric | Charge associated with nighttime usage |

### International Usage

| Feature              | Type    | Description                                |
| -------------------- | ------- | ------------------------------------------ |
| `Total intl minutes` | Numeric | Total international call minutes           |
| `Total intl calls`   | Numeric | Number of international calls              |
| `Total intl charge`  | Numeric | Charge associated with international usage |

### Customer Service

| Feature                  | Type    | Description                              |
| ------------------------ | ------- | ---------------------------------------- |
| `Customer service calls` | Numeric | Number of calls made to customer service |

---

## 5. Data Types

The documented schema contains:

* **15 numeric predictors**
* **4 categorical predictors**
* **1 binary target**

`Area code` is represented numerically in the dataset but should generally be treated as a **categorical feature**, not as a continuous numerical variable.

Similarly, `State` is categorical rather than numerical.

The Kaggle documentation identifies the original variable types, including integer/double numeric variables and string variables.

---

## 6. Data Quality

### Reported quality

* Missing values: **None**
* Dataset size: **3,333 rows**
* Target distribution: **Imbalanced**
* Data format: Tabular
* Dataset description: **Cleaned Orange Telecom Customer Churn Dataset**

### Additional checks recommended before modeling

Even with no missing values, a proper ML data-quality audit should verify:

1. Duplicate customer records
2. Duplicate rows
3. Invalid categorical values
4. Impossible numerical values
5. Outliers
6. Cardinality of categorical variables
7. Relationships between derived variables
8. Target leakage
9. Feature-target relationships
10. Train/test distribution differences

The supplied sample alone is not sufficient to establish dataset-wide duplicate counts, exact cardinalities, or numerical ranges.

---

## 7. Important Feature Relationships

Several variables are structurally related.

For example:

* `Total day minutes` ↔ `Total day charge`
* `Total eve minutes` ↔ `Total eve charge`
* `Total night minutes` ↔ `Total night charge`
* `Total intl minutes` ↔ `Total intl charge`

Charges are closely related to usage minutes, so these variables are expected to exhibit strong correlation.

This should be explicitly investigated during EDA.

### Modeling implication

This is not necessarily a problem for tree-based models, but it can affect:

* Linear-model coefficients
* Multicollinearity
* Feature importance interpretation
* Model simplicity

For linear/logistic models, correlation and multicollinearity diagnostics are therefore particularly relevant.

---

## 8. Temporal Scope

The dataset does **not contain an explicit timestamp or longitudinal observation period**.

Therefore:

* A temporal train/test split cannot be constructed from the available data.
* Customer behavior cannot be analyzed as a time series.
* Concept drift cannot be measured directly.
* A documented "predict churn within the next X days/months" prediction horizon cannot be established from the supplied metadata alone.

Consequently, this dataset is better treated as a **static supervised-learning dataset** rather than a realistic longitudinal churn system.

---

## 9. Potential Leakage / Causal Considerations

The dataset should be treated as a **predictive classification dataset**, not a causal dataset.

A correlation between a feature and `Churn` does not establish that the feature causes churn.

Particular attention should be paid to whether all predictor variables would genuinely be available **before the churn decision/prediction point** in a real deployment scenario.

Because the dataset lacks an explicit timestamp and prediction horizon, this cannot be fully established from the dataset alone.

---

## 10. Geographic Features

`State` and `Area code` contain geographic information.

These variables may capture genuine regional differences, but they can also act as proxies for geographic or operational factors that are not explicitly represented in the dataset.

For portfolio modeling, their inclusion should therefore be tested rather than assumed to be useful.

A useful experiment is:

> **Model A:** exclude geographic features
> **Model B:** include geographic features

Then compare their validation performance and interpretability without relying solely on accuracy.

---

## 11. Class-Imbalance Strategy

With only **14.49% churned customers**, random splitting should use **stratification** so that class proportions remain approximately consistent across train/validation/test sets.

Recommended workflow:

```text
Raw Data
   ↓
Data Quality Checks
   ↓
Train/Test Split
   ↓
Stratified Sampling
   ↓
Preprocessing
   ↓
Baseline Model
   ↓
Model Comparison
   ↓
Threshold Evaluation
   ↓
Final Model
```

Potential approaches include:

* Class weights
* Threshold tuning
* Resampling methods such as SMOTE, when justified
* Cost-sensitive learning

Resampling should be performed **only on the training data** to avoid data leakage.

---

## 12. Recommended ML Evaluation

A strong evaluation setup should report:

| Metric               | Purpose                                               |
| -------------------- | ----------------------------------------------------- |
| **Precision**        | How many predicted churners actually churned          |
| **Recall**           | How many actual churners were identified              |
| **F1-score**         | Balance between precision and recall                  |
| **ROC-AUC**          | Ranking/discrimination across thresholds              |
| **PR-AUC**           | Particularly informative for the minority churn class |
| **Confusion Matrix** | Direct view of classification errors                  |

Accuracy can be reported as a supplementary metric, but it should not be the primary metric because of the class imbalance.

---

## 13. Known Limitations

### Dataset limitations

1. **Static dataset**
   No temporal information is available.

2. **Limited sample size**
   3,333 customers is useful for learning but relatively small for representing a large telecom population.

3. **Class imbalance**
   Only 14.49% of customers are labeled as churned.

4. **Limited customer context**
   The dataset primarily contains usage, service, account, and support variables.

5. **No explicit prediction horizon**
   The available metadata does not define when churn is measured relative to the predictors.

6. **No longitudinal customer history**
   Changes in customer behavior over time cannot be modeled.

7. **Potential feature redundancy**
   Several charge variables are strongly related to corresponding usage variables.

8. **Historical dataset**
   It should not be interpreted as representative of current telecom customers without external validation.

---

## 14. Privacy & Security Considerations

The supplied schema does not contain obvious direct personal identifiers such as:

* Customer name
* Phone number
* Email address
* Physical address

Nevertheless, the dataset's provenance and licensing conditions should be respected when redistributing the data or derivative artifacts.

For a portfolio project, referencing the original Kaggle source is preferable to redistributing the raw dataset unnecessarily.

---

## 15. Recommended Portfolio ML Workflow

For this dataset, a professional project can follow:

```text
1. Business Understanding
        ↓
2. Data Card / Data Audit
        ↓
3. Exploratory Data Analysis
        ↓
4. Churn vs. Feature Analysis
        ↓
5. Data Leakage Check
        ↓
6. Feature Engineering
        ↓
7. Stratified Train/Test Split
        ↓
8. Preprocessing Pipeline
        ↓
9. Baseline Model
        ↓
10. Model Comparison
        ↓
11. Imbalance Handling
        ↓
12. Hyperparameter Tuning
        ↓
13. Threshold Optimization
        ↓
14. Model Interpretation
        ↓
15. Error Analysis
        ↓
16. Final Model & Documentation
```

---

## 16. Overall Dataset Assessment

This dataset is well suited to a **learning and portfolio binary-classification project** because it provides:

* A clearly defined target
* Mixed numerical and categorical features
* Class imbalance
* Customer behavioral variables
* Service-subscription variables
* Customer-support information
* Opportunities for feature engineering
* Opportunities to demonstrate model interpretation

However, the dataset should be presented as a **historical/static learning dataset**, not as a production-ready representation of contemporary telecom churn.

### Key modeling question

> **Can customer account characteristics, service subscriptions, usage behavior, and customer-service interactions be used to accurately identify customers who are likely to churn?**

That question provides a clean foundation for the subsequent EDA, feature engineering, modeling, and evaluation stages.
