## Bank marketing campaign analysis

End-to-end data analysis & ML project using a real Portuguese bank telemarketing dataset — from raw data exploration to predictive modeling to to identify which customers will subscribe to a term deposit.

---

## Why this project

Understanding why customers say no is as valuable as knowing who will say yes.
This project started from a simple question: can we identify, before making the call,
which customers are worth contacting?

---

## Dataset

- **Source:** UCI Machine Learning Repository
- **Reference:** Moro et al. (2014), Decision Support Systems  
- **Size:** 41,188 rows, 21 columns (20 + 1 target)
- **Target:** term deposit subscription (yes/no)
- **Class imbalance:** 88.7% no — 11.3% yes

---

## Notebooks - Key findings

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

**Output:** `data/processed/bank_clean.csv`