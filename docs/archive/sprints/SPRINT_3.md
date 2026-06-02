# SPRINT_3.md
_Finals UX Sprint — Close Demo-Critical Gaps Before June 14 Submission._  
_Active Objective: Build every screen required by the 5-Minute Demo Script._

---

## 🏃 SPRINT GOAL

Make every step of the 5-Minute Demo Script work end-to-end on the actual Streamlit frontend.  
Backend, databases, and ML are frozen. This sprint is 100% frontend.

---

## 📋 TASK CHECKLIST

### 🔴 CRITICAL — Demo Blockers (Complete by June 5)

#### S3-T1: Single Account Lookup Panel
- **Owner:** Shriraj Dyaram
- **Time:** 3 hours
- **File:** `frontend/app.py` — new nav entry `🔍 Account Inspector`
- **Deliverable:**
  - Sidebar text input for Account ID (default `ACC0520000000028`)
  - On submit: call `POST /predict/single` with feature row from DataSet.csv
  - Render score card (severity color, composite score, mule_stage badge)
  - Show composite formula: `ml_score * 0.70 + graph_score * 0.30 = X`
- **Validation:** Enter a known CRITICAL account; card renders in < 2 seconds

#### S3-T2: Named SHAP Feature Mapping
- **Owner:** Vikram Sindra + Shriraj Dyaram
- **Time:** 1 hour
- **File:** `frontend/app.py` — add `FEATURE_NAMES` dict near constants
- **Deliverable:**
  ```python
  FEATURE_NAMES = {
      "F670":  "Regulatory TMS Flag",
      "F886":  "Channel Switching Rate",
      "F3908": "High-Velocity Pass-Through",
      "F3889": "Dormant Account (G365D)",
      "F3891": "Student/Agri Demographic Profile",
      "F115":  "Transaction Frequency Ratio",
      "F321":  "Amount Ratio",
      "F3836": "Balance/Limit Breach",
      "F3894": "Account Holder Age",
      "F2082": "Normal Banking Activity (Absent)",
  }
  ```
  Apply in all SHAP render loops: `FEATURE_NAMES.get(code, code)`
- **Validation:** SHAP card shows "Regulatory TMS Flag (+23 pts)" not "F670 (+23 pts)"

#### S3-T3: Neo4j Graph Intelligence Panel
- **Owner:** Dhiren Mulwani + Shriraj Dyaram
- **Time:** 4 hours
- **File:** `frontend/app.py` — new nav entry `🕸️ Graph Intelligence`
- **Deliverable:**
  - Account ID input field
  - Call `GET /graph/neighbors/{account}` (or equivalent backend route)
  - Render pyvis Network from response: risk-color nodes (RED=HIGH, YELLOW=MEDIUM, GREY=LOW)
  - Show banner: "⚠️ 3-Hop Mule Ring Detected — N connected HIGH-risk accounts"
  - Display centrality score per node
- **Validation:** Known CRITICAL account renders graph with ≥ 2 connected red nodes

#### S3-T4: Mule Lifecycle Stage Visual
- **Owner:** Shriraj Dyaram
- **Time:** 2 hours
- **File:** `frontend/app.py` — helper function `render_lifecycle_stage(stage)`
- **Deliverable:**
  - 4-stage HTML pill widget: `🟣 Newly Recruited | 🔴 Active Mule | 🟠 Being Flushed | ⚫ Dormant`
  - Active stage highlighted; inactive stages greyed out
  - One-line description beneath active stage
  - Used in Single Account Lookup + ML alert expanders
- **Validation:** Lifecycle visual renders for each of the 4 possible stage values

---

### 🟠 HIGH — Quick Wins (Complete by June 3)

#### S3-T5: ML Score / Graph Score Split Metric Card
- **Owner:** Shriraj Dyaram
- **Time:** 1 hour
- **File:** `frontend/app.py` — inside ML alert expander
- **Deliverable:** 3-column metric row per alert:
  - `ML Score: X.X` | `Graph Score: Y.Y` | `→ Composite: Z.Z`
- **Validation:** Every expanded alert shows all 3 score components

#### S3-T6: Auto-STR Trigger Banner
- **Owner:** Shriraj Dyaram
- **Time:** 30 minutes
- **File:** `frontend/app.py`
- **Deliverable:** When `composite_score >= 80`: render `st.error("⚡ AUTO-STR TRIGGERED — FIU-IND compliant XML generating in 8 seconds. Account freeze recommended.")`
- **Validation:** CRITICAL alert expander shows red auto-trigger banner

#### S3-T7: 8-Second SLA Detection Metric
- **Owner:** Shriraj Dyaram
- **Time:** 30 minutes
- **File:** `frontend/app.py` — add to metrics row (L501 block)
- **Deliverable:** `st.metric("⚡ Detection Latency", "< 8 sec", delta="vs 4–6 day manual", delta_color="inverse")`
- **Validation:** Metric appears in the summary row after CSV analysis

#### S3-T8: Branding Purge ⚠️ ZERO TOLERANCE
- **Owner:** Sujal Gupta
- **Time:** 30 minutes
- **Files:** `frontend/app.py`, any other frontend files
- **Find & Replace:**
  - `"FundTrace AI"` → `"MuleShield AI"` (ALL occurrences)
  - `"FundTrace"` → `"MuleShield"` (docstrings, captions, error messages)
  - `"Union Bank"` → remove or replace with `Bank of India`
  - `"UBI"` → remove
  - Page title → `"MuleShield AI – Mule Account Detection"`
  - PDF header → `"MuleShield AI – Fraud Intelligence Report"`
- **Validation:** `grep -r "FundTrace\|Union Bank\|UBI" frontend/` returns zero results

---

### 🟡 MEDIUM — Polish (Complete by June 10)

#### S3-T9: Hero Landing Page
- **Owner:** Shriraj Dyaram
- **Time:** 2 hours
- **File:** `frontend/app.py` — replace L1140 `else` block
- **Deliverable:**
  - Product tagline in large text
  - 3 stat cards: "9,082 Accounts Analyzed", "81 Mule Accounts Detected", "< 8 Sec Detection"
  - Descriptive paragraph: What is a mule account? Why MuleShield?
  - `▶ Launch Demo` button (calls `_load_scenario()`)
  - BOI + IITH logos (use emoji substitutes if images unavailable)
- **Validation:** A judge with no context understands the product within 10 seconds

#### S3-T10: One-Click Demo Button
- **Owner:** Shriraj Dyaram
- **Time:** 2 hours
- **File:** `frontend/app.py` — sidebar
- **Deliverable:**
  - Button: `🎯 Full Demo Mode`
  - Action: load `data/DataSet.csv` → run batch inference → auto-select first CRITICAL account → display Account Inspector panel
  - Pre-hardcode a known CRITICAL account ID as fallback
- **Validation:** Demo runs without any manual typing or file upload

#### S3-T11: Real PR-AUC from Metadata
- **Owner:** Vikram Sindra
- **Time:** 1 hour
- **File:** `frontend/app.py` — Model Metrics section
- **Deliverable:** Load `backend/ml_artifacts/final_metadata.json`. If `precision_curve` and `recall_curve` keys exist, render real data. If not, keep mock but add `st.caption("Illustrative — run T11 to link actual model output.")`.
- **Validation:** PR-AUC label reads real number (0.963 or actual trained value)

#### S3-T12: Impact Close Card
- **Owner:** Shriraj Dyaram
- **Time:** 30 minutes
- **File:** `frontend/app.py` — bottom of ML results (after pagination)
- **Deliverable:** Side-by-side card:
  - LEFT: `❌ Without MuleShield | 4–6 days | Funds dispersed | Manual review`
  - RIGHT: `✅ With MuleShield | < 8 seconds | Account frozen | Auto-STR filed`
- **Validation:** Card visible at bottom of ML Alert Center

---

## 🎯 DEFINITION OF DONE

- [ ] A judge can enter any account ID from DataSet.csv and see a scored card in < 2 seconds
- [ ] SHAP shows human-readable feature names (zero raw F-codes visible)
- [ ] Neo4j graph ring renders for CRITICAL accounts showing connected nodes
- [ ] Lifecycle stage shows as a visual 4-stage indicator
- [ ] ML / Graph / Composite scores appear side-by-side in every alert card
- [ ] Composite ≥ 80 shows AUTO-STR red banner
- [ ] 8-second SLA metric is visible in the results header
- [ ] Zero instances of "FundTrace", "Union Bank", "UBI" anywhere in the UI
- [ ] One-click demo button works without file upload or typing
- [ ] Landing page sells the product in 10 seconds

---

## 📅 TIMELINE

| Date | Task | Owner |
|---|---|---|
| June 1 | S3-T8 Branding Purge | Sujal |
| June 1–2 | S3-T2 Named SHAP, S3-T5/T6/T7 Quick Wins | Shriraj + Vikram |
| June 2–3 | S3-T1 Single Account Lookup | Shriraj |
| June 3–5 | S3-T3 Neo4j Graph Panel, S3-T4 Lifecycle Wheel | Dhiren + Shriraj |
| June 6–7 | S3-T9 Hero Landing, S3-T10 Demo Button | Shriraj |
| June 8 | S3-T11 PR-AUC, S3-T12 Impact Card | Vikram + Shriraj |
| June 9–10 | Full demo dry-run — 5-minute walkthrough, fix breaks | All |
| June 11–13 | Edge-case fixes, final polish | All |
| June 14 | **SUBMISSION** | Sujal |
