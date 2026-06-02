# RISK_ENGINE.md
_Mathematical specifications for composite risk scores and lifecycle staging. ~600 tokens._

---

## 📐 UNIFIED COMPOSITE RISK SCORE

MuleShield AI fuses tabular behavioral predictions with relational graph data to generate a single composite risk score.

```
       ┌────────────────────────┐
       │   Tabular ML Score     │ ──┐
       │  (XGBoost Probability) │   │
       └────────────────────────┘   │
                                    │ (x 0.70)
                                    ▼
       ┌────────────────────────┐   Σ ──► [ Composite Score (0-100) ]
       │   Graph Score          │   ▲
       │  (Neo4j Connectivity)  │   │
       └────────────────────────┘   │ (x 0.30)
                                    │
                                    │ (Fallback to 1.0 if down)
                                    ┘
```

The scoring engine is defined strictly inside `backend/risk_scoring.py` and implements the formula:

$$\text{Composite Risk} = \text{Round}\left( (\text{ML Score} \times 0.70 + \text{Graph Score} \times 0.30) \times 100, 1 \right)$$

### Parameters:
*   **ML Score ($\text{ml\_score}$):** Floating value $[0.0, 1.0]$ representing predicted probability from the XGBoost pipeline.
*   **Graph Score ($\text{graph\_score}$):** Floating value $[0.0, 1.0]$ representing connectivity score (betweenness centrality + cycle detection + proximity to known fraud nodes).
*   **Outage Fallback Rule:** If the Graph DB container experiences an outage, $\text{graph\_score}$ defaults to $\text{ml\_score}$ so that $\text{Composite Risk} = \text{ml\_score} \times 100$.

---

## 🏷️ RISK SEVERITY TIERS

Composite scores are split into four actionable bands that dictate investigator prioritization:

| Composite Score | Severity Tier | Operational Protocol |
| :--- | :--- | :--- |
| **Score $\geq$ 80.0** | **CRITICAL** | Auto-generate compliance-grade goAML XML, queue case in PostgreSQL, flag lock on CBS, flag node red. |
| **Score $\in$ [60.0, 79.9]** | **HIGH** | Priority review case queue, flag node orange, alert analyst for review. |
| **Score $\in$ [40.0, 59.9]** | **MEDIUM** | Standard review queue, add to watch-list, check velocity patterns on next transaction. |
| **Score < 40.0** | **LOW** | Clear transaction, log record in PostgreSQL ledger, zero active alarm. |

```python
# Authoritative tier logic in backend/risk_scoring.py
def assign_tier(score: float) -> str:
    if score >= 80.0:
        return "CRITICAL"
    if score >= 60.0:
        return "HIGH"
    if score >= 40.0:
        return "MEDIUM"
    return "LOW"
```

---

## 🌀 MULE LIFECYCLE STAGING ALGORITHM

To provide advanced insights to investigators, the system assigns a behavioral stage to flagged accounts. Staging uses rule-based classification based on the 122 metadata dimensions, plus prior-indicator feature **F3912** (which is excluded from training).

```
                      ┌──────────────────────┐
                      │    Classification    │
                      └──────────┬───────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
  [ NEWLY RECRUITED ]      [ ACTIVE MULE ]       [ BEING FLUSHED ]
  - Age: L7D or L90D      - F3912 = 1           - F115 > 0.70
  - Risk >= 60            - Watchlist F670 > 1  - F2082 = 0
```

```python
# Defined inside backend/ml_service.py
def classify_mule_stage(features: dict, risk_score: float) -> str:
    age_bucket = features.get('F3889', '')     # Account age category
    prior_flag = features.get('F3912', 0)     # Leakage feature, used strictly here
    regulatory = features.get('F670', 0)      # watchlist flag
    trans_ratio = features.get('F115', 0)     # transaction ratio
    absent_bank = features.get('F2082', 1)    # normal banking presence indicator

    # Stage 1: Newly Recruited Account
    # Young account age (Less than 7 Days or Less than 90 Days) showing immediate high risk
    if age_bucket in ['L7D', 'L90D'] and risk_score >= 60.0:
        return "NEWLY_RECRUITED"
        
    # Stage 2: Active Mule Account
    # Account has active legacy alert (F3912) and regulatory watch list hits
    if prior_flag == 1 and regulatory > 0.15:
        return "ACTIVE_MULE"
        
    # Stage 3: Being Flushed (Proceeds Dispersal)
    # High frequency transaction ratio coupled with complete lack of normal consumer banking
    if trans_ratio > 0.70 and absent_bank == 0:
        return "BEING_FLUSHED"
        
    # Stage 4: Dormant Account Reactivated
    # Account age is greater than 365 Days, has been inactive, now exhibiting moderate risk
    if age_bucket == 'G365D' and 40.0 <= risk_score < 60.0:
        return "DORMANT"
        
    return None
```
