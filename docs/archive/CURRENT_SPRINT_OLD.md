# CURRENT_SPRINT.md
_Load for daily standups and active task context. Refresh each morning. ~300 tokens._

---

## SPRINT: Foundation + Core ML Service
**Phase:** Phase 0 → Phase 1  
**Active Days:** Day 1 – Day 2  
**Sprint Goal:** ML model artifacts integrated into FastAPI. `/predict/batch` returning real scores on DataSet.csv.

---

## ACTIVE TASKS

### T1 — Copy ML Artifacts into Repo `[OWNER: Vikram]`
- **Status:** TODO
- **Time:** 30 min
- **Files:** Create `backend/ml_artifacts/` with 5 files:
  - `final_model.pkl` — XGBoost pipeline
  - `imputer_full.pkl` — SimpleImputer (fitted on train)
  - `final_metadata.json` — 122 feature names + thresholds
  - `cat_mappings.json` — LabelEncoder mappings for 8 categorical cols
  - `feature_importances.csv` — feature name → importance score
- **Validation:** `python3 -c "import pickle; pickle.load(open('final_model.pkl','rb'))"` — no error

### T2 — FastAPI ML Inference Service `[OWNER: Vikram/Dhiren]`
- **Status:** TODO
- **Time:** 3 hours
- **Files affected:**
  - NEW: `backend/routers/ml_predict.py`
  - NEW: `backend/ml_service.py`
  - MODIFIED: `backend/app.py` (add router + lifespan model load)
- **Endpoints to build:** `POST /predict/single` + `POST /predict/batch`
- **Dependencies:** T1 complete
- **Validation:** `curl -X POST http://localhost:8000/predict/batch -F "file=@DataSet.csv"` → returns JSON with `summary.critical > 0`

### T3 — Wire ML Score into Risk Scoring `[OWNER: Dhiren]`
- **Status:** BLOCKED (needs T2)
- **Time:** 2 hours
- **Files affected:** MODIFIED: `backend/risk_scoring.py`
- **Change:** Add `calculate_composite_risk(ml_score, graph_score)` — single source of truth
- **Formula:** `ml_score * 0.70 + graph_score * 0.30`

---

## PARALLEL (can start now, no deps)

### T13 — Dataset Documentation Page `[OWNER: Sujal]`
- **Status:** TODO
- **Time:** 2 hours
- **Files:** NEW: `frontend/src/pages/DatasetDocs.jsx` or static HTML
- **Content:** Dataset size, F3924 target, 18 BOI hint features, fraud rate, methodology, null handling
- **Note:** Required by BOI submission. Must exist before June 15.

---

## DEFINITION OF DONE (this sprint)

- [ ] `final_model.pkl` loads without error in Docker container
- [ ] `POST /predict/batch` processes DataSet.csv → returns `{ summary, accounts[] }`
- [ ] `summary.critical` > 0 (at least one CRITICAL account found)
- [ ] `calculate_composite_risk()` exists in `risk_scoring.py` — no other risk math anywhere
- [ ] Dataset docs page renders at `/dataset`

---

## BLOCKERS / RISKS THIS SPRINT

- **Pickle version:** Pin `scikit-learn==1.5.x` and `xgboost==2.x` in `requirements.txt` before T1
- **SMOTE memory:** Apply SMOTE only on 122 selected features, not full 3924-column matrix
- **F3912 in model:** Double-check `final_metadata.json` does NOT contain F3912 in feature list
