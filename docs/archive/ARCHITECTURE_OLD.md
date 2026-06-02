# ARCHITECTURE.md
_Load for backend, ML, and integration tasks. ~700 tokens._

---

## CURRENT ARCHITECTURE (FundTrace AI — pre-transformation)

```
frontend/          React + Tailwind + Cytoscape.js
backend/
  app.py           FastAPI main, existing routers
  risk_scoring.py  Manual multi-signal risk score (no ML)
  graph_service.py Neo4j Cypher queries
  str_generator.py goAML XML generation (Claude API)
  blockchain.py    SHA-256 + OpenTimestamps
docker-compose.yml FastAPI + Neo4j + PostgreSQL + Redis
```

**Gap:** No ML pipeline. No `/predict` endpoints. Risk score is rule-based only. Dataset (F1…F3924 format) not consumed anywhere.

---

## DESIRED ARCHITECTURE (MuleShield AI — target state)

```
backend/
  app.py                    ← add ml_predict router + lifespan model load
  routers/
    ml_predict.py           ← NEW: /predict/single, /predict/batch
    graph.py                ← existing
    str_generator.py        ← existing, now auto-triggered by score ≥ 80
  ml_artifacts/             ← NEW directory
    final_model.pkl         ← XGBoost pipeline (XGB + SMOTE + imputer)
    imputer_full.pkl        ← SimpleImputer fitted on training data
    final_metadata.json     ← 122 selected feature names + thresholds
    cat_mappings.json       ← LabelEncoder mappings for 8 categorical cols
    feature_importances.csv ← sorted feature name → importance score
  risk_scoring.py           ← MODIFIED: add calculate_composite_risk()
  ml_service.py             ← NEW: load artifacts, run inference, build signals

frontend/src/
  pages/
    BatchAnalysis.jsx       ← NEW: drag-drop CSV upload + RiskTable
    AccountDetail.jsx       ← MODIFIED: add SignalCard + lifecycle badge
    ModelMetrics.jsx        ← NEW: PR-AUC curve, confusion matrix
  components/
    SignalCard.jsx          ← NEW: per-account signal explanation
    RiskTable.jsx           ← NEW: sortable/filterable risk scores table
    AlertFunnel.jsx         ← NEW: animated 9082 → N count widget
    LifecycleBadge.jsx      ← NEW: 4-stage mule status indicator
```

---

## SERVICES & PORTS

| Service | Port | Purpose |
|---|---|---|
| FastAPI | 8000 | All API endpoints |
| Neo4j | 7474 (HTTP), 7687 (Bolt) | Graph database |
| PostgreSQL | 5432 | Case management, audit log |
| Redis | 6379 | Velocity sliding windows, demo cache |

---

## API ENDPOINTS (complete list including new)

### Existing (keep)
- `GET /health` — system status
- `POST /graph/trace` — fund flow tracing
- `POST /str/generate` — manual STR generation
- `POST /nlq` — natural language query to Cypher
- `GET /cases` — case management list

### New (T2, T3, T7)
- `POST /predict/single` — single account prediction
  - Input: `{ account_id: str, features: dict }` (F1…F3924 key-value)
  - Output: `RiskResponse` (see schema below)
- `POST /predict/batch` — CSV upload batch prediction
  - Input: multipart `file` (BOI DataSet.csv format, F1…F3924 columns)
  - Output: `{ summary: {...}, accounts: [RiskResponse] }`
- `POST /ingest-i4c` — MHA I4C alert ingestion
  - Input: I4C JSON payload (account_no, complaint_id, amount)
  - Output: cross-referenced `RiskResponse`

### RiskResponse Schema
```json
{
  "account_id": "string",
  "risk_score": 0-100,
  "tier": "CRITICAL|HIGH|MEDIUM|LOW",
  "ml_score": 0.0-1.0,
  "graph_score": 0.0-1.0,
  "mule_stage": "NEWLY_RECRUITED|ACTIVE_MULE|BEING_FLUSHED|DORMANT|null",
  "signals": [
    { "signal": "Regulatory flag active", "severity": "CRITICAL", "value": 1 }
  ],
  "shap_values": { "F670": 0.23, "F886": 0.18, ... },
  "str_recommended": true,
  "str_pre_filled": { ... }
}
```

---

## DATA FLOW (prediction path)

```
BOI CSV upload
    ↓
/predict/batch (FastAPI)
    ↓
ml_service.py:
  1. Load rows as DataFrame
  2. Apply cat_mappings (LabelEncoder)
  3. Impute nulls (imputer_full.pkl)
  4. Select 122 features (final_metadata.json)
  5. XGBoost.predict_proba() → ml_score
  6. SHAP TreeExplainer → top-5 signals
    ↓
risk_scoring.py:
  7. calculate_composite_risk(ml_score, graph_score=ml_score if Neo4j down)
  8. Assign tier (>80 CRITICAL, 60-79 HIGH, 40-59 MEDIUM, <40 LOW)
  9. classify_mule_stage(features, risk_score)
    ↓
Response assembled → if tier==CRITICAL: auto-trigger STR draft
```

---

## RISK SCORING ARCHITECTURE

```python
# backend/risk_scoring.py — SINGLE SOURCE OF TRUTH
def calculate_composite_risk(ml_score: float, graph_score: float) -> float:
    return round((ml_score * 0.70 + graph_score * 0.30) * 100, 1)

# Tier assignment
def assign_tier(score: float) -> str:
    if score >= 80: return "CRITICAL"
    if score >= 60: return "HIGH"
    if score >= 40: return "MEDIUM"
    return "LOW"
```

**Rule:** Only this function computes the final score. T7 calls it. Never inline risk math elsewhere.

---

## MULE LIFECYCLE STAGE LOGIC

```python
# backend/ml_service.py — rule-based, no additional training
def classify_mule_stage(features: dict, risk_score: float) -> str:
    age = features.get('F3889', '')
    f3912 = features.get('F3912', 0)  # NOTE: not in model, used for staging only
    f670  = features.get('F670', 0)
    f115  = features.get('F115', 0)
    f2082 = features.get('F2082', 1)

    if age in ['L7D', 'L90D'] and risk_score >= 60:
        return "NEWLY_RECRUITED"
    if f3912 == 1 and f670 > 0.15:
        return "ACTIVE_MULE"
    if f115 > 0.7 and f2082 == 0:
        return "BEING_FLUSHED"
    if age == 'G365D' and 40 <= risk_score < 60:
        return "DORMANT"
    return None
```

---

## GRAPH INTELLIGENCE ARCHITECTURE

- Neo4j stores account nodes and transaction edges
- On `/predict/single`: query Neo4j for account's 3-hop neighbors
- Compute graph_score from: betweenness centrality + cycle count + hop distance to known fraud nodes
- If Neo4j unavailable: `graph_score = ml_score` (silent fallback, log warning)
- ML-flagged accounts (score ≥ 60) get red node color in Cytoscape.js graph

---

## AUTO-STR TRIGGER (T7)

```python
# In /predict/single and /predict/batch
if risk_response.tier == "CRITICAL":
    str_draft = str_generator.build_draft(
        account_id=risk_response.account_id,
        risk_score=risk_response.risk_score,
        signals=risk_response.signals[:3],  # top 3 only
        pmla_section="12",
    )
    risk_response.str_pre_filled = str_draft
    risk_response.str_recommended = True
```

---

## FAILURE RECOVERY RULES

| Failure | Recovery |
|---|---|
| Model fails to load | Serve pre-computed `demo_results.json` (build Day 4) |
| Neo4j down | graph_score = ml_score, log warning, continue |
| CSV upload slow | Show progress bar + "Analysing 9,082 accounts..." spinner |
| Unknown category value | LabelEncoder fallback → encode as 0, don't crash |
| React build breaks | PropTypes validation on all new components |
