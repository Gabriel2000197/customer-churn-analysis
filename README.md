## Bank marketing campaign analysis

End-to-end data analysis & ML project using a real Portuguese bank telemarketing dataset — from raw data exploration to predictive modeling to identify which customers will subscribe to a term deposit.

---

## Why this project

The starting point was a real business problem: a Portuguese bank ran thousands of telemarketing calls
to sell term deposits, but only 1 in 9 clients subscribed.
The question was not just "can we identify, before making the call,
which customers are worth contacting?", but also "why do they subscribe, when they should be contacted, and how to make the campaign actually efficient?".

This project covers a full analysis workflow: raw data exploration, cleaning, SQL-based business intelligence, viusla EDA, and a predictive model. Every step was driven by a business question.

The result is a set of findings (business report) that a campaign manager could act on tomorrow - and
a live app that scores any client before the call is made.

---

## Dataset

- **Source:** UCI Machine Learning Repository
- **Reference:** Moro et al. (2014), Decision Support Systems  
- **Size:** 41,188 rows, 21 columns (20 + 1 target)
- **Target:** term deposit subscription (yes/no)
- **Class imbalance:** 88.7% no — 11.3% yes

---

## Notebooks

### 01 — Initial Exploration
First look at the dataset to understand its structure and quality.

**What I found:**
- No true NaN values
- Missing data is encoded as strings: `unknown` appears in 6 columns, 
  with `default` being the most problematic (8,597 unknown, only 3 "yes")
- Target is heavily imbalanced: 88.7% no vs 11.3% yes
- 12 duplicate rows
- 4 calls with duration = 0 seconds, likely recording errors
- `pdays = 999` and `poutcome = nonexistent` describe the same thing 
  from two different angles, most clients had no prior contact with the bank
- `education` has only 18 "illiterate" cases, not meaningful

### 02 — Data Cleaning
Cleaned the raw dataset from 41,188 to 41,172 rows.

**Decisions made:**

- **Duplicates:** 12 removed
- **Duration = 0:** 4 records removed — no contact was made
- **education:** merged 'illiterate' (18 cases) into 'basic.4y' — too rare to be meaningful
- **default:** collapsed 3 'yes' into 'no' — statistically irrelevant, kept 'unknown' as separate category
- **pdays:** dropped column — most of the values were 999 (a placeholder, not a real number -> a problem for the future models). Created binary column `previously_contacted` to preserve the yes/no information
- **housing & loan:** imputed 990 'unknown' with mode — it's not specified in the dataset documentation that the 'unknown' values are a behavioral signal (no answer), so not a separate category
- **education unknown:** kept as separate category — 1,730 cases can be meaningful enough and are too large to impute without introducing bias
- **job & marital unknown:** imputed with mode — small percentage, low risk
 
**Winsorization:** applying the strategy outlined in the EDA notebook for outliers (`duration` and `campaign` - capping at 99th percentile) to produce the model-ready dataset.

**Output:** `data/processed_data/bank_clean.csv`, `data/processed_data/bank_model.csv`

### 03 — Exploratory Data Analysis
Visual and more in depth exploration of the cleaned dataset to uncover patterns and relationships.

**Coverage:**
- **Numerical and categorical distributions:** histograms for all numerical and categorical variables, outlier identification via boxplots for `duration` and `campaign`
- **Target analysis:** call duration vs subscription outcome, age distribution by outcome, campaign contacts vs outcome (great visual sign for understanding what can be the optimal number of contacts)
- **Correlation matrix:** strong multicollinearity confirmed among economic indicators (r > 0.90)
- **Economic context:** scatter plot revealing two distinct economic clusters (low vs high euribor), boxplot confirming subscribers were predominantly contacted during low-rate periods (one of the strongest pattern in the dataset)
- **Temporal patterns:** monthly subscription rate trend

**Outlier handling strategy (no real application here):**
- `age`: no action — distribution is natural, 10 clients over 90 are plausible
- `duration` and `campaign`: capping at 99th percentile applied in the Data Cleaning notebook to produce the model-ready dataset


### 04 — SQL Analysis
Business intelligence queries on a SQLite database ('bank.db').
Covers customer profiling, campaign effectiveness, economic context quantification, 
segment volume and stability analysis, and a risk-opportunity matrix 
classifying all job segments across conversion rate and volume dimensions.
This notebook extends and replicates the EDA findings.

**Output:** `outputs/database/bank.db` (put in .gitignore)

### 05 — Predictive Modeling

End-to-end model training pipeline to predict term deposit subscription (identify who is worth contacting).

Approach:
- Three models compared (ROC-AUC): Logistic Regression, Random Forest, XGBoost
- Hyperparameter tuning via RandomizedSearchCV on the two best performers
- Threshold optimization (only for selected model after tuning) for a better F1-score and a better recall for class 1 ('yes' - really important in this business context), with a precision constraint of at least 0.35 (avoid an excessive number of false positives).

**Key decisions**:
- **duration excluded** — only available post-call, not useful for pre-call lead prioritization
- **Class imbalance** — handled via scale_pos_weight (XGBoost) and class_weight='balanced' (others)
- **Two threshold optimization strategies compared** — F1 maximization vs Recall maximization
- **Recall-focused threshold selected** — in a campaign context, missing a potential subscriber is more costly than an unnecessary call
**XGBoost tuned** — selected as final model (ROC-AUC: ~0.8194), with a **decision threshold (recall-optimizated) of ~0.424**

**Output**: `outputs/models/final_subscription_model.pkl`, `outputs/models/best_threshold.pkl` `outputs\models\preprocessor.pkl`

---
https://bank-marketing-analysis-gabriel.streamlit.app/