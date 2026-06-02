# TASK_QUEUE.md
_Authoritative prioritized backlog of all upcoming tasks (P0, P1, P2) for MuleShield AI. ~600 tokens._

---

## 🔥 P0: CRITICAL PATH BACKLOG (Required for Shortlisting)

These tasks represent core ML and integration capabilities. All P0 tasks must be completed before submission.

| Task ID | Task Title | Assigned Owner | Estimated Time | Dependencies | Target Output / Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | Copy ML Artifacts | Vikram | 30 min | None | Write 5 artifact files to `backend/ml_artifacts/`. Verifies via loading script. |
| **T2** | FastAPI ML Endpoints | Vikram/Dhiren | 3 hours | T1 | `/predict/single` and `/predict/batch` live. Batch returns critical count > 0. |
| **T3** | Score Fusion Integration | Dhiren | 2 hours | T2 | `calculate_composite_risk()` in `risk_scoring.py`. Composite handles offline fallbacks. |
| **T4** | Signal Explanation Card | Sujal | 4 hours | T2 | `SignalCard.jsx` linked to Account Details page. Renders SHAP-translated text. |
| **T5** | Batch CSV Ingest UI | Sujal | 3 hours | T2 | Drag-and-drop CSV uploader in `BatchAnalysis.jsx` linking to sortable `RiskTable.jsx`. |
| **T6** | Mule Lifecycle Classifier | Vikram | 4 hours | T2 | Writes `mule_stage` rules inside `ml_service.py` using categorical features. |
| **T7** | Compliance Auto-STR Trigger | Dhiren | 2 hours | T3, T4 | Automatically launches pre-filled STR modal when composite risk score $\geq 80$. |
| **T13** | Dataset Documentation Page | Sujal | 2 hours | None | Navigating to `/dataset` correctly renders structural statistics and feature exclusions. |

---

## ⚡ P1: HIGH-VALUE BACKLOG (Improves Evaluation Rankings)

These tasks enhance explainability, UI presentation quality, and analytical reporting, which are critical for the judges.

| Task ID | Task Title | Assigned Owner | Estimated Time | Dependencies | Target Output / Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T8** | Feature Importance Visuals | Vikram | 3 hours | T2 | Renders dynamic bar charts showing top-20 SHAP values on single predictions. |
| **T9** | Interactive Alert Funnel | Sujal | 2 hours | T5 | Animated dashboard funnel tracking (9,082 total accounts $\rightarrow$ N critical cases). |
| **T10** | Demographics Charts | Sujal | 3 hours | T2 | Renders occupation fraud rates (F3891) and account type splits (F3886). |
| **T11** | Customer Profile Panel | Sujal | 3 hours | T2 | Displays occupation details, account age buckets, and transaction velocity. |
| **T12** | Model Metrics Dashboard | Vikram | 2 hours | T8 | Displays live Precision-Recall (PR-AUC) graphs and classification matrices. |
| **T13.5** | UI Branding Audit | Shriraj | 1 hour | None | Final verification that no "Union Bank" strings remain in UI components. |
| **T13.6** | Slide Insights Ingestion | Sujal | 2 hours | None | Enhances PPT slide decks with BOI dataset insights (89% G365D age patterns). |

---

## 💡 P2: NICE-TO-HAVE BACKLOG (Completed if Time Permits)

These features enhance edge-case reliability, webhook inputs, and mock demo capabilities.

| Task ID | Task Title | Assigned Owner | Estimated Time | Dependencies | Target Output / Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T14** | Live Upload Demonstration | All | 2 hours | T5, T9 | Simulates upload of `DataSet.csv` live, transitioning to critical case and STR. |
| **T15** | Demo Rehearsal & Run | All | 3 hours | All | Simulates end-to-end presentation and timing checks (target under 5 minutes). |
| **T16** | Pre-computed Backup | Vikram | 30 min | T2 | Writes `demo_results.json` containing pre-computed predictions for offline safety. |
| **T17** | Demo Mode UI Button | Sujal | 1 hour | T5 | Adds a "Load Sandbox Results" button to bypass CSV parsing on slow hardware. |
| **T18** | Government I4C Webhook | Dhiren | 1.5 hours | T2 | `/ingest-i4c` endpoint maps webhook payloads to internal risk calculations. |
| **T19** | NLQ Data Interface | Dhiren | 2 hours | T3 | Natural language queries translate to Cypher paths returning search results. |
| **T20** | Regional Fraud Heatmap | Sujal | 2 hours | T10 | Interactive regional heatmap utilizing metropolitan/rural categories (F3890). |

---

## 📈 SEQUENTIAL EXECUTION DEPENDENCY MAP

```
[ Phase 0: Setup ]
  └── T1 (Copy ML Artifacts) & T13 (Dataset Docs) & Branding Audit
        │
        ▼
[ Phase 1: Core Engine ]
  └── T2 (FastAPI ML Endpoints)
        │
        ├───► T3 (Score Fusion) ──► T7 (Auto-STR Trigger)
        │
        ├───► T4 (Signal Card) ───► T11 (Behavior Panel)
        │
        ├───► T5 (CSV Ingest UI) ──► T9 (Alert Funnel UI)
        │
        └───► T6 (Mule Classifier) ─► T10 (Demo Charts)
```
