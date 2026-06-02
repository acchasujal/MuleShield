# DATASET_INTELLIGENCE.md
_Authoritative reference for dataset statistics, features, null handling, and explanation models. ~700 tokens._

---

## 📊 DATASET FACT SHEET

*   **Source File:** `DataSet.csv`
*   **Total Accounts:** 9,082
*   **Total Dimensions:** 3,924 columns (F1...F3924)
*   **Target Label:** **F3924** (0 = Legitimate account, 1 = Suspicious Mule account)
*   **Mule Accounts Count:** 81 (0.9% positive class rate)
*   **Legitimate Accounts Count:** 9,001 (99.1% negative class rate)
*   **Imbalance Ratio:** 111.1 : 1 (legitimate to mule)
*   **Mean Missing Data Rate:** 27.6% across features
*   **Retained Feature Dimensions:** **122 features** (post null-filtering, variance filtering, and domain-matching)

---

## 🚫 DATA LEAKAGE PREVENTION: FEATURE F3912

> [!WARNING]
> Feature **F3912** has a **0.97 Pearson correlation** with feature F3924 (target).
> - 79 out of 81 suspicious mule accounts have F3912 = 1.
> - Only 3 out of 9,001 legitimate accounts have F3912 = 1.
> F3912 represents a prior transaction monitoring system (TMS) flag or historical warning.
> **DO NOT allow F3912 to be used as an input feature for model training.**
> Including F3912 will result in a trivial 99%+ accuracy that will not generalize to new, unflagged mule accounts, which will lead to immediate disqualification by IIT Hyderabad judges.

### Approved Uses of F3912:
1.  **Lifecycle Staging:** Use F3912 strictly in post-inference rule-based staging (e.g., identifying `ACTIVE_MULE`).
2.  **Demo Narrative:** "Our engine cross-checks and correlates predictions with BOI's legacy TMS indicator (F3912), serving as an intelligent, high-precision second opinion."
3.  **Judges Q&A Defense:** "We isolated F3912 as an historical operational flag and removed it from our feature matrix to ensure the model generalizes to new, sophisticated money-laundering patterns."

---

## 🔑 FEATURE ENGINEERING CATEGORIES

### P1 Features (Direct Model Ingestion - High Discrimination)
*   **F670:** watchlist flag (binary). Hits 23.5% of fraud accounts vs 9.0% of legit (2.6× separation).
*   **F3908:** In/Out transaction volume velocity ratio. Mule accounts show extreme ratios near 1.0 (funds entering are immediately sent out).
*   **F886:** Channel switching intensity. Identifies rapid, non-standard switches between ATM, mobile, and RTGS (7.4× separation).
*   **F115:** Transaction frequency ratio. Polynomial feature extraction: `F115_squared = F115 ** 2`.
*   **F255, F253, F258, F256 (Activity Pattern Group):** Flagged accounts show dense activity. Extract `mean(F255, F253, F258, F256) as activity_density`.
*   **F2082:** Absence of normal banking. Evaluates to `0` for ALL suspicious accounts. Must be processed as a negative weight signal.

### P2 Features (Transform & Engineer Before Ingestion)
*   **F2686:** Frequency counter (118× higher in fraud). Must apply logarithmic smoothing: `log1p(F2686)`.
*   **F2578, F2285, F2779, F2481:** Transaction amounts (100× higher in fraud). Impute null values with `0` (amount features median), apply `log1p()`, and generate ratio: `F2578 / F2285`.
*   **F3889:** Categorical account age bucket. Encode ordinally: `G365D` (greater than 365 days) = 4, `L365D` = 3, `L180D` = 2, `L90D` = 1, `L7D` = 0.
*   **F3891:** Categorical occupation. Extract binary feature: `is_vulnerable_demographic` (if student or agriculture worker).

---

## 🔠 MANDATORY CATEGORICAL ENCODING

There are **8 categorical columns** that must be encoded using fitted mappings from `cat_mappings.json` before feeding to the XGBoost inference model:

| Field | Description / Key Values | Target Encoding Strategy |
| :--- | :--- | :--- |
| **F2230** | Anonymous categorical column | LabelEncoder fitted mapping |
| **F3886** | Account Type (e.g., Savings, Current, MSME) | MSME accounts map to lower initial velocity limits |
| **F3888** | Anonymous categorical column | LabelEncoder fitted mapping |
| **F3889** | Account age bucket (`G365D`, `L365D`, `L180D`, `L90D`, `L7D`) | Ordinal numeric encoding (4 down to 0) |
| **F3890** | Region classification (`M`=Metro, `SU`=Semi-Urban, `R`=Rural, `U`=Urban) | LabelEncoder fitted mapping |
| **F3891** | Customer Occupation (`student`, `agriculture`, `salaried`, etc.) | LabelEncoder mapped + vulnerability flag |
| **F3892** | Anonymous categorical column | LabelEncoder fitted mapping |
| **F3893** | Anonymous categorical column | LabelEncoder fitted mapping |

*Rule:* If the inference API encounters an out-of-vocabulary category at runtime, fallback to `0` instead of crashing.

---

## ⚖️ CLASS IMBALANCE CORRECTION

To address the severe 111:1 imbalance in the training partition, the pipeline must employ a dual-correction approach:

1.  **Synthetic Minority Over-sampling Technique (SMOTE):** Apply only to the 122 selected features after dropping irrelevant dimensions, setting `k_neighbors = 5`.
2.  **XGBoost scale_pos_weight:** Set `scale_pos_weight = 111` in `XGBClassifier` to scale gradient updates for the minority class.

```python
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# Oversample training data
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_res, y_train_res = smote.fit_resample(X_train_122, y_train)

# Setup classifier with scale_pos_weight
model = XGBClassifier(
    scale_pos_weight=111,
    eval_metric='aucpr',  # Rank by Precision-Recall AUC
    use_label_encoder=False,
    random_state=42
)
```

---

## 🔍 MODEL INTERPRETATION (SHAP) & EXPLANATION

Every classification prediction on `/predict/single` must supply the top-5 contributing features using the SHAP `TreeExplainer`. The raw feature symbols must be translated to human-readable fraud signals:

| Feature | Raw Criteria | Translated Human-Readable Risk Signal |
| :--- | :--- | :--- |
| **F670** | F670 = 1 | "Prior regulatory watch-list flag active on account" |
| **F886** | F886 $\geq$ 0.15 | "Unusual rapid channel-switching behavior detected" |
| **F3908** | F3908 $\geq$ 0.70 | "High velocity in/out ratio (funds passing through rapidly)" |
| **F115** | F115 $\geq$ 0.65 | "Elevated transaction ratio relative to customer history" |
| **F2082** | F2082 = 0 | "Complete absence of standard retail banking behavior" |
| **F3889** | F3889 in ['G365D'] | "Account is established dormant profile activated for laundering" |
| **F3891** | F3891 in ['student'] | "High-vulnerability demographic profile matched (student mule)" |

---

## 🏛️ BOI HINT FEATURES REFERENCE
The following 18 features were highlighted by Bank of India analysts as highly predictive. Ensure these are treated with high importance and documented on the system interface:
`F115`, `F321`, `F527`, `F531`, `F670`, `F1692`, `F2082`, `F2122`, `F2582`, `F2678`, `F2737`, `F2956`, `F3043`, `F3836`, `F3887`, `F3889`, `F3891`, `F3894`.
