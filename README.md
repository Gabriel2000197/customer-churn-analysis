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

### 01-Initial Exploration

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
