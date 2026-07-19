# 10_AI_CONTEXT.md — MuleShield AI: AI Context & Explainability Framework

This document outlines the machine learning explanation models, feature mapping keys, and explainability boundaries implemented in the MuleShield AI financial trust infrastructure.

---

## 1. Mapped Feature Explainer Keys (SHAP to Plain English)

The system translates SHAP feature indicators into human-readable, explainable financial trust intelligence:

- **`F3889`**: Dormant profile reactivated
- **`F3908`**: High-velocity pass-through behavior
- **`F886`**: Unusual payment-channel switching
- **`F115`**: Elevated transaction frequency
- **`F2082`**: Normal retail activity is absent (e.g. no utility bills, zero grocery/dining spends)
- **`F670`**: Prior regulatory watch-list signal
- **`F3891`**: High-vulnerability profile signal

---

## 2. SHAP TreeExplainer Attribution

- **Model Engine**: XGBoost binary classifier trained on 122 variables.
- **Explainability**: Local feature attributions calculated using `shap.TreeExplainer`.
- **UI Presentation**: Mapped values show up under the "Case Brief" panel with interactive focus links that tie signals directly back to their risk contributor dimensions.

---

## 3. Threat Staging Decision Matrix

State progression rules map composite risk scores to active lifecycle phases:

| Fused Severity | Heuristic Conditions | Resolved Stage | Action |
| :--- | :--- | :--- | :--- |
| **CRITICAL** (Score $\ge 80$) | Any | `BEING_FLUSHED` | Debit freeze webhook + goAML STR generation |
| **HIGH** ($60 \le$ Score $< 80$) | Any | `ACTIVE_MULE` | Suspend digital channels (UPI/Net) |
| **MEDIUM** ($40 \le$ Score $< 60$)| Any | `NEWLY_RECRUITED` | Queue case for analyst audit |
| **LOW** (Score $< 40$) | Active rules rule out fraud | `LEGITIMATE` | Log, no escalation |
