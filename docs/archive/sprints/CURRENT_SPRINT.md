# CURRENT_SPRINT.md
_Active sprint checklist, daily targets, and blocker logs. Refresh daily. ~300 tokens._

---

## 🏃 SPRINT ACTIVE GOAL

**Phase:** Phase 1 (Foundation + Core ML Service Integration)  
**Duration:** Day 1 – Day 2  
**Active Objective:** Transfer pre-trained XGBoost artifacts, build FastAPI batch/single endpoints, integrate score fusion, and render dataset documentation in the UI.

---

## 📋 ACTIVE SPRINT TASK CHECKLIST

### 1. T1: Copy ML Artifacts into Repository
*   **Owner:** Vikram Sindra  
*   **Time Allocation:** 30 minutes  
*   **Target Path:** `backend/ml_artifacts/`
*   **Required Deliverables:** Write the 5 core artifact files (`final_model.pkl`, `imputer_full.pkl`, `final_metadata.json`, `cat_mappings.json`, `feature_importances.csv`).
*   **Validation Check:** Executing `python3 -c "import pickle; pickle.load(open('backend/ml_artifacts/final_model.pkl','rb'))"` outputs zero errors.

### 2. T2: FastAPI ML Inference Service
*   **Owner:** Vikram Sindra & Dhiren Mulwani  
*   **Time Allocation:** 3 hours  
*   **Target Files:**
    *   `[NEW]` `backend/routers/ml_predict.py` (FastAPI router endpoints)
    *   `[NEW]` `backend/ml_service.py` (Inference logic, cat encoder, imputation)
    *   `[MODIFY]` `backend/app.py` (Lifespan load configuration)
*   **Endpoints:** `POST /predict/single` and `POST /predict/batch`.
*   **Validation Check:** `curl -X POST http://localhost:8000/predict/batch -F "file=@DataSet.csv"` returns full JSON response containing critical alerts.

### 3. T3: Wire ML Score into Risk Scoring Engine
*   **Owner:** Dhiren Mulwani  
*   **Time Allocation:** 2 hours  
*   **Target Files:**
    *   `[MODIFY]` `backend/risk_scoring.py` (Composite score calculations)
*   **Required Deliverables:** Wire `calculate_composite_risk(ml_score, graph_score)` using the $70/30$ weighted split.
*   **Validation Check:** Composite score calculation returns a decimal rounded to one place; falls back to 100% ML score if database connection is interrupted.

### 4. T13: Ingest Dataset Documentation Page
*   **Owner:** Sujal Gupta  
*   **Time Allocation:** 2 hours  
*   **Target Files:**
    *   `[NEW]` `frontend/src/pages/DatasetDocs.jsx`
*   **Required Deliverables:** Comprehensive dataset breakdown containing demographics (89% G365D dormant activation, 28% student vulnerabilities), class imbalance details, and details on F3912 exclusion.
*   **Validation Check:** Navigating to `/dataset` correctly renders the documentation card layout.

---

## 🎯 DEFINITION OF DONE (DOD)

*   [ ] All model artifacts load successfully in the Docker container during boot.
*   [ ] `/predict/batch` executes in under 5 seconds on `DataSet.csv`, identifying high-risk accounts.
*   [ ] Risk score calculation is consolidated in `risk_scoring.py` with zero inlining elsewhere.
*   [ ] The front-end renders the dataset details correctly under `/dataset`.
*   [ ] Git commits are cleanly segmented and code compiles without errors.
