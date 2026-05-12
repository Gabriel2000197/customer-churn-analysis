# Bank Telemarketing Campaign — Business Intelligence Report

---

## Executive Summary

This report presents the findings of a full analytical review of a retail bank's 
telemarketing campaign data (dataset: 41,172 client contacts from this Portuguese bank [2008–2013]).
The goal was to understand what drives a client 
to subscribe to a term deposit, and to build a tool that helps the bank 
identify, before making the call, which clients are most likely to convert.

The analysis uncovered different categories of insight: e.g. who to call, when to call, 
and how many times to call. Acting on these findings could significantly 
improve campaign ROI without increasing the contact volume.

A predictive model was then developed and validated, achieving a ROC-AUC of 0.82 
and correctly identifying 71% of actual subscribers, while maintaining 
an 83% accuracy rate on non-subscribers. This represents a strong result given the highly imbalanced nature of the dataset, where positive subscription cases account for only a really small portion of the observations.

---

## 1. The Business Problem

The bank runs outbound telemarketing campaigns to sell term deposits. 
The core challenge here is efficiency — the campaign contacted over 41,000 clients, 
but only 11.3% subscribed. The remaining 88.7% were contacted (at a cost)
with no return.

![Subscribers vs Non-Subscribers](outputs/graphs/target_distribution.png)

Every unsuccessful contact represents agent time, operational cost, and customer fatigue without generating revenue, improving efficiency therefore becomes more valuable than simply increasing outreach volume.

The questions this analysis set out to answer:

- Which clients are most likely to subscribe?
- Are there optimal times to run the campaign?
- What role does the broader economic environment play?
- How many contact attempts are worth making before moving on?

---

## 2. Key Findings

### 2.1 The Right Client Profile

Not all client segments respond equally to the campaign. 
The data reveals a clear hierarchy of conversion rates by profession:

| Segment | Conversion Rate |
|---------|----------------|
| Students | 31.4% |
| Retired | 25.3% |
| Unemployed | 14.2% |
| Admin | 12.9% |
| Blue-collar | 6.9% |
Source: '04_sql_analysis.ipynb'

Students and retired clients convert at roughly three times the rate 
of blue-collar workers (lowest conversion rate), yet the campaign directed the majority of its 
contacts toward admin and blue-collar segments simply because they are 
the largest groups (it can be observed in the EDA notebook - job distribution). This is a volume bias, not a performance strategy.

The opportunity: reallocating even 20% of blue-collar contacts toward 
retired and student profiles would meaningfully improve overall conversion 
without increasing campaign costs.

### 2.2 Previous Contact History Matters

Clients who had subscribed in a previous campaign converted at dramatically 
higher rates than those being contacted for the first time. 
This is the single most actionable segmentation variable available to the bank, a list of previously successful clients is a high-value asset that appears to be underutilized here.

Clients with no prior campaign history (86% of the dataset) represent 
a much harder conversion challenge and should be approached with 
more selective targeting criteria.

### 2.3 Stop Calling After 3-4 Attempts

The data is strightforward. Conversion rate drops consistently 
with each additional contact attempt:

| Contact Attempts | Conversion Rate |
|-----------------|----------------|
| 1 | 13.0% |
| 2 | 11.5% |
| 3 | 10.8% |
| 4 | 9.4% |
| 6+ | ~7% and declining |
Source: '04_sql_analysis.ipynb'

Beyond 3-4 attempts, the probability of conversion plateaus and the 
cost-per-acquisition rises sharply. Resources spent on repeated follow-up 
with resistant clients would generate significantly more value if redirected 
toward fresh, untried leads.

### 2.4 Economic Context Is the Strongest Driver

The most striking finding in the entire dataset is the relationship between 
interest rates and subscription behavior. When the Euribor rate was low 
(below 2%), nearly 1 in 4 clients subscribed (24.5%). 
When rates were high (above 2%), fewer than 1 in 20 subscribed (4.8%), 
a fivefold difference.

| Economic Period | Conversion Rate |
|-------------------|----------|
| Low-rate euribor3m | 24.5% |
| High-rate euribor3m | 4.8% |
Source: '04_sql_analysis.ipynb'

This finding has profound implications for campaign planning. 
The bank's campaign results are heavily influenced by macroeconomic conditions 
that are outside its control. However, the timing of high-intensity outreach 
can be aligned with favorable rate environments to maximize returns.
In practical terms, the economic environment acts almost like a “conversion multiplier", even the best-performing segments (retired clients, students) collapse during high-rate periods, while moderate targeting strategies perform significantly better during low-rate periods.
The campaign's most important strategic lever may not be who to call, 
but when to run the campaign at full intensity.


### 2.5 Seasonal Patterns

The campaign showed notably higher conversion rates in certain months, 
particularly in periods that coincided with lower Euribor levels. 
March, September, October and December showed stronger performance, 
while May, despite being the highest-volume month, showed relatively 
modest conversion rates. Volume and effectiveness do not always move together.

![Subscription Trend By Month](outputs\graphs\subscription_trend_month.png)

---

## 3. Predictive Model

A machine learning model was developed to predict, before a call is made, 
whether a client is likely to subscribe. Several predictive approaches were evaluated before selecting the final model used for lead prioritization.

### Model Performance

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.82 |
| Recall (subscribers) | 71% |
| Precision (subscribers) | 35% |
Source: '05_Modeling.ipynb'

The model correctly identifies 71% of actual subscribers before the call is made. 
The classification threshold was deliberately set lower than standard (0.424 vs 0.5) 
to prioritize recall (the number of the actual subscribers correctly captured).
From a business perspective in a campaign context, the cost of missing a genuine 
subscriber outweighs the cost of an unnecessary call. For this reason this strategy was implemented in order to minimize missed potential subscribers.


### What Drives the Model

![Most Important Variables](outputs\graphs\feature_importance.png)

The five variables with the highest influence on the model's predictions are:

1. Number of employees (macroeconomic indicator)
2. Consumer confidence index (macroeconomic indicator)
3. Employment variation rate (macroeconomic indicator)
4. Previously contacted (binary — was the client contacted before?)
5. Previous campaign success (did they subscribe last time?)

The dominance of macroeconomic indicators at the top of this list 
reinforces the finding from the EDA, the economic environment is 
the most powerful contextual factor in predicting subscription behavior. 
The bank has limited control over these variables, but can use them 
as signals for campaign timing.

---

## 4. Business Recommendations

One consistent pattern throughout the analysis is that persistence alone does not create conversions. Relevance, timing, and customer context appear to matter far more
than simply increasing contact frequency.
Four recommendations are presented in order of expected impact:

**1. Time campaigns to economic conditions**
Concentrate high-volume outreach during low Euribor periods. 
During high-rate environments, maintain only relationship-preserving contact 
with the highest-value segments. This single change could improve 
overall campaign conversion by several percentage points.

**2. Prioritize previously successful clients**
Build and maintain a dedicated list of clients who subscribed in past campaigns. 
These clients represent the highest-probability leads available and appear 
significantly underutilized in the current campaign strategy.

**3. Reallocate contacts from high-volume to high-efficiency segments**
Reduce outreach to blue-collar and services segments - large in volume but 
below-average in conversion. Redirect a portion of these contacts toward 
retired and student profiles, which convert at 2-3x the rate despite 
being contacted far less frequently.

**4. Follow-up limit**
Any client who has not responded positively after 4 calls is unlikely to convert.
Introduce a contact fatigue policy by limiting follow-up attempts to a maximum of 4. Beyond this point, additional outreach generates sharply diminishing returns while increasing operational cost and customer irritation risk.
This limit frees up agent time and budget for higher-probability leads.

---

## 5. Limitations

Several limitations should be considered when acting on these findings:

- The dataset covers 2008–2013, a period that includes the global financial crisis. 
  Some patterns, particularly around economic sensitivity, may not fully 
  generalize to current conditions.
- The model achieves 71% recall on subscribers but 35% precision, it is intentionally optimized to capture 
  as  many potential subscribers as possible, even at the cost of recommending some lower-probability leads (35% precision). In a telemarketing context, this trade-off is acceptable because the business cost of missing an interested customer is considered higher than the cost of an additional call attempt.
  The model is a prioritization tool, not a guarantee.
- Causal relationships cannot be established from observational data alone. 
  The patterns identified here, particularly those related to call duration, should be interpreted as associations rather than direct cause-effect relationship.

---

## 6. Next Steps

**1.** Use the predictive model as a lead scoring tool integrated into
the campaign workflow
**2.** Run an A/B test comparing model-prioritized outreach against 
  the current contact strategy to validate ROI improvement
**3.** Refresh the model annually as new campaign data becomes available
**4.** Monitor macroeconomic indicators (Euribor, employment rate) 
  as leading signals for campaign timing decisions

---

*This report was produced as part of a full end-to-end data analysis project 
covering data cleaning, exploratory analysis, SQL-based business intelligence, 
and predictive modeling. All findings are based on: Moro, S., Rita, P., & Cortez, P. (2014). UCI Machine Learning Repository, using bank-additional-full datatset variant.*