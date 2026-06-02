# ML_ARCHITECTURE_BASELINE.md — Phase 4A Audit

> **Snapshot Date:** 2026-06-02  
> **Purpose:** Complete baseline audit of the ML layer before Phase 4 structural refactoring. No code has been changed at this point.

---

## 1. Current ML File Structure

```
backend/
├── app.py                    ← FastAPI entry point; registers routers, runs lifespan
├── ml_service.py             ← Monolithic ML class (loading, inference, SHAP, lifecycle)
├── risk_scoring.py           ← Fusion v5 formula, tier assignment, lifecycle alignment
├── utils.py                  ← lookup_account_features(), _validate_dataframe()
├── routers/
│   ├── ml_predict.py         ← /predict/single, /predict/batch endpoints
│   ├── analyze.py            ← /analyze endpoint (graph-based fraud detection pipeline)
│   └── i4c_webhook.py        ← /ingest-i4c endpoint
└── ml_artifacts/
    ├── final_model.pkl        ← Fitted XGBoost binary classifier (404 KB)
    ├── imputer_full.pkl       ← Fitted SimpleImputer (2 KB)
    ├── final_metadata.json    ← Feature names list (122 selected features)
    ├── cat_mappings.json      ← Categorical feature encoding maps (103 KB)
    └── feature_importances.csv ← Pre-computed static feature importances
```

---

## 2. Model Loading Flow

```
MLService.__init__(artifacts_dir="backend/ml_artifacts")
    └── load_artifacts()
            ├── Checks existence of 4 artifact paths (exits early if any missing)
            ├── open(final_metadata.json) → self.feature_names: list[str]  [122 features]
            ├── open(cat_mappings.json)   → self.cat_mappings: dict[str, dict]
            ├── pickle.load(imputer_full.pkl) → self.imputer: SimpleImputer
            ├── pickle.load(final_model.pkl)  → self.model: XGBClassifier
            ├── shap.TreeExplainer(self.model) → self.explainer
            └── pd.read_csv(feature_importances.csv) → self.feature_importances: dict
                     (fallback: self.model.feature_importances_)
```

**State stored on `MLService` instance:**
| Attribute | Type | Description |
|---|---|---|
| `model` | XGBClassifier | Trained classifier |
| `imputer` | SimpleImputer | Pre-fit imputer for missing features |
| `feature_names` | list[str] | 122 selected feature column names |
| `cat_mappings` | dict | String→int encoding maps per column |
| `feature_importances` | dict | Pre-computed or model-derived importances |
| `explainer` | shap.TreeExplainer | Fitted SHAP explainer (single predictions) |
| `is_loaded` | bool | True if all artifacts loaded successfully |

---

## 3. Prediction Flow

### 3a. `predict_single(raw_features: dict) → dict`
```
raw_features (dict)
    ↓
pd.DataFrame([raw_features])               ← 1-row DF
    ↓
preprocess_features(df)
    ├── drop F3912, F3924  (leakage columns)
    ├── encode_categorical(df)             ← cat string→int via cat_mappings
    ├── align to self.feature_names        ← adds missing columns as NaN
    └── imputer.transform()                ← fills remaining NaN
    ↓
model.predict_proba(df_processed)[0][1]   ← fraud positive probability
    ↓
classify_mule_stage(raw_features, prob*100)
    ↓
generate_shap_signals(df_processed)
    ↓
return {"ml_score": float, "mule_stage": str, "shap_signals": dict}
```

### 3b. `predict_batch(df_raw: pd.DataFrame) → list[dict]`
```
df_raw (full DataSet.csv batch)
    ↓
preprocess_features(df_raw)               ← same pipeline as single
    ↓
model.predict_proba(df_processed)[:, 1]  ← all row probabilities at once
    ↓
for each row:
    classify_mule_stage(raw_row, prob*100)
    static top-5 feature_importances (NOT per-row SHAP — speed optimisation)
    ↓
return list[dict]  [index, ml_score, mule_stage, shap_signals]
```

---

## 4. SHAP Flow

### Single Prediction (Dynamic SHAP)
```
generate_shap_signals(processed_df)
    ↓
self.explainer.shap_values(processed_df)   ← shap.TreeExplainer
    ↓
Handle output shape variants:
    list        → shap_vals[1][0]    (class 1 from list format)
    shape (N,3) → shap_vals[0][1]   (class 1 from 3D array)
    default     → shap_vals[0]
    ↓
dict(zip(feature_names, vals))
    ↓
sorted by abs(val) desc → top 5
    ↓
return {feature: float(val), ...}   (5 entries)
```

### Batch Prediction (Static Importances — Speed)
```
self.feature_importances
    ↓
sorted by abs(importance) desc → top 5
    ↓
return top_5_static dict   (shared for ALL rows in batch)
```

---

## 5. Feature Lookup Flow

```
utils.lookup_account_features(account_id: str) → dict
    ↓
Parse account index from "ACC052" prefix
    e.g. "ACC05200000000028" → suffix "00000000028" → idx=28
    ↓
Open data/boi/DataSet.csv
    → readline() header
    → seek to idx-th data row (sequential line skipping)
    → parse CSV line manually (comma split, type inference)
    ↓
Return features dict  OR  fallback_features (if CSV missing / parse error)

Fallback features (hardcoded):
    F670: 1.0, F886: 0.45, F3908: 0.85, F115: 0.90, F2082: 0.0, F3889: "G365D"
```

---

## 6. Lifecycle Staging Flow

```
MLService.classify_mule_stage(raw_features: dict, risk_score: float) → str
    ↓
Extract: age_bucket (F3889), prior_flag (F3912), regulatory (F670),
         trans_ratio (F115), absent_bank (F2082)
    ↓
Stage Rules (evaluated in order, first match wins):
    1. F3889 in ["L7D","L90D"] AND risk_score ≥ 60.0 → "NEWLY_RECRUITED"
    2. F3912 == 1.0 AND F670 > 0.15               → "ACTIVE_MULE"
    3. F115 > 0.70 AND F2082 == 0.0               → "BEING_FLUSHED"
    4. F3889 == "G365D" AND 40.0 ≤ risk_score < 60.0 → "DORMANT"
    5. risk_score ≥ 60.0                           → "ACTIVE_MULE"
    6. default                                     → "LEGITIMATE"
    ↓
risk_scoring.align_lifecycle_stage(stage, severity, txn_score)
    ↓
    If stage=="LEGITIMATE" AND severity in {MEDIUM,HIGH,CRITICAL} AND txn>0 → "UNDER_REVIEW"
    Otherwise → unchanged stage
```

---

## 7. Fusion Scoring Flow

```
risk_scoring.calculate_composite_risk(ml_score, graph_score, txn_score)
    ↓
PROFILE_WEIGHT    = 0.40
TRANSACTION_WEIGHT= 0.40
GRAPH_WEIGHT      = 0.20
    ↓
ml_val    = (ml_score or 0.0) * 100.0
graph_val = (ml_score if graph_score is None else graph_score or 0.0) * 100.0
    ↓
fused = (ml_val * 0.40) + (txn_score * 0.40) + (graph_val * 0.20)
clamped = clamp(fused, 0.0, 100.0)
rounded = round(clamped, 1)
    ↓
return 0.1 if (clamped>0 and rounded==0) else rounded

risk_scoring.assign_tier(score)
    score ≥ 80.0 → CRITICAL
    score ≥ 60.0 → HIGH
    score ≥ 40.0 → MEDIUM
    else         → LOW
```

---

## 8. Dependency Graph (Pre-Refactor)

```
backend/app.py
    └── imports: MLService, Neo4jService, database.init_db
    └── routers:
          ├── routers/health.py          → ai_service.py (nvidia_client, gemini_client)
          ├── routers/analyze.py         → utils.py, explain.py, fraud_detection.py,
          │                                graph_builder.py, risk_scoring.py, xml_generator.py
          ├── routers/ai_chat.py         → ai_service.py
          ├── routers/ml_predict.py      → ml_service.MLService, risk_scoring, xml_generator, database
          └── routers/i4c_webhook.py     → ml_service.MLService, risk_scoring, xml_generator, database

backend/ml_service.py
    ├── pandas, numpy, pickle, json, os
    ├── shap
    └── (reads from): backend/ml_artifacts/

backend/risk_scoring.py
    └── (no external imports — pure python math)

backend/utils.py
    ├── pandas
    ├── fastapi (HTTPException)
    └── (reads from): data/boi/DataSet.csv
```

---

## 9. Baseline Performance Metrics

| Metric | Value |
|---|---|
| MLService startup (load_artifacts) | 273.3 ms |
| Single prediction latency (incl. SHAP) | 89.7 ms |
| Batch prediction latency (20 rows) | 138.4 ms |

## 10. Baseline Prediction Outputs

| Test | ml_score | mule_stage | shap_keys (top-5) |
|---|---|---|---|
| feat row 28 (single) | 3.56e-05 | LEGITIMATE | F3898, F2230, F3908, F1216, F886 |
| feat row 9 (acc9) | 1.5e-05 | LEGITIMATE | — |
| feat row 9002 (acc9002) | 1.3e-05 | ACTIVE_MULE | — |
| batch row 0 | 7.9e-05 | LEGITIMATE | F3898, F1428, F996, F3914, F1320 |
| fusion (0.85ml, 0.70gr) | — | 48.0 → MEDIUM | — |
| lifecycle align (LEGITIMATE, MEDIUM, txn=20) | — | UNDER_REVIEW | — |
