# MuleShield AI — System Architecture Specification

This document consolidates all architectural blueprints, database schemas, API contracts, risk scoring equations, machine learning pipelines, and lifecycle decision matrices for the MuleShield AI platform.

---

## 1. High-Level System Blueprint
MuleShield AI is designed around a dual-engine detection architecture combining static client features (Tabular Machine Learning) with dynamic transaction behaviors (Topological Graph Analytics).

```
 Incoming transactions ➔ Ingestion & Slicing
                            ├── Tabular features ➔ XGBoost + SHAP Attributions (ML Engine)
                            └── Graph relations  ➔ Neo4j GDS Centrality + NetworkX (Graph Engine)
                                                      │
                                                      ▼
                                           Score Fusion (70/30)
                                                      │
                                                      ▼
                                          Mule Lifecycle Timeline
                                                      │
                                                      ▼
                                         Compliance Autopilot (goAML)
```

### Component Topology
* **FastAPI Gateway Server (`backend/app.py`):** Acts as the entrypoint for client integrations, exposing REST routers.
* **ML Inference Client (`backend/ml/predictor.py`):** Stateful executor that loads final XGBoost binary classifiers and transforms transaction parameters.
* **SHAP Explainer Client (`backend/ml/shap_engine.py`):** Extends TreeExplainer model mappings to provide human-readable explainability logs.
* **Graph Database Controller (`backend/graph_service.py`):** Establishes Bolt connection drivers to Neo4j database to calculate normal degree centralities.
* **Audit Logger Controller (`backend/database.py`):** Serializes case audits and evidence cryptographic signatures into a local/remote PostgreSQL database.
* **Suspicious Autopilot Auto-STR (`backend/xml_generator.py`):** Constructs XML compliance documents conformant to international regulatory standards.
* **Streamlit Web UI (`frontend/app.py`):** Admin dashboard console presenting executive fraud visual analytics.

---

## 2. Database Schema Mappings

### PostgreSQL ORM schema (`case_audits` table)
Used for keeping trace of all system alerts, composite score fusion details, and tamper-proof evidence signatures (Indian Evidence Act Section 65B compliance).

| Field | ORM Type | SQL Constraints | Purpose |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | `Primary Key, Serial` | Auto-incrementing identifier. |
| `case_id` | `String(50)` | `NOT NULL, Indexed` | Case reference STR identifier. |
| `account_id` | `String(50)` | `NOT NULL, Indexed` | Bank Account ID under lookup. |
| `event_type` | `String(50)` | `NOT NULL` | Trigger type: `RISK_FUSION` or `I4C_PORTAL_WEBHOOK`. |
| `timestamp` | `DateTime(timezone=True)`| `NOT NULL` | Timezone-aware UTC event timestamp. |
| `ml_score` | `Float` | `NOT NULL` | Standalone machine learning probability. |
| `graph_score` | `Float` | `NOT NULL` | Standalone GDS degree centrality. |
| `composite_score` | `Float` | `NOT NULL` | Fused composite risk score in points. |
| `severity` | `String(20)` | `NOT NULL` | Threat tier: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `mule_stage` | `String(30)` | `NOT NULL` | Timeline stage classification. |
| `evidence_hash` | `String(64)` | `Nullable` | SHA-256 hash representation of the goAML XML report. |
| `action_taken` | `String(100)` | `NOT NULL` | Enforcement action: `AUTO_FREEZE` or `INVESTIGATOR_QUEUED`. |

### Neo4j Graph Model
Represents transaction connections for topological lookups:
* **Nodes:** `(:Account {id: String})`
* **Relationships:** `(:Account)-[:TRANSACTED {amount: Float, timestamp: String, channel: String}]->(:Account)`
* **Schema Constraints:**
  * Unique node key constraint on `Account.id`.
  * Index on relationship `TRANSACTED.timestamp` for sliding context traversals.

---

## 3. API Routing Contracts

### Ingestion endpoint: `POST /analyze`
Uploads a transaction CSV block, executes independent graph-based cycle and layering searches concurrently via ThreadPoolExecutor worker pools, fuses predictions, logs database audits, and returns alerts.
* **Payload:** `multipart/form-data` containing `file: UploadFile`
* **Response Schema (200 OK):**
```json
{
  "alerts": [
    {
      "account": "ACC05200000009002",
      "risk_score": 92.0,
      "severity": "HIGH",
      "reasons": ["F670", "F886"],
      "explanation": "Prior watch-list flag active (+45 pts) | UPI velocity (+23 pts)",
      "evidence": [
        {
          "from_account": "ACC05200000009002",
          "to_account": "ACC05299999999999",
          "amount": 75000.0,
          "timestamp": "2026-06-02 10:00:00",
          "channel": "UPI"
        }
      ],
      "mule_stage": "ACTIVE_MULE",
      "ml_score": 90.0,
      "graph_score": 85.0,
      "profile_risk": 90.0,
      "transaction_risk": 68.0,
      "graph_risk": 85.0,
      "shap_signals": {"F670": 0.45, "F886": 0.23},
      "goaml_xml": "<report>...</report>",
      "case_id": "STR-20260602-1234",
      "evidence_hash": "e3b0c442..."
    }
  ],
  "signals": {
    "cycle": ["ACC05200000009002"],
    "layering": ["ACC05200000009002"],
    "structuring": [],
    "velocity": [],
    "anomaly": [],
    "dormant": [],
    "ml_anomaly": []
  },
  "fraud_paths": ["ACC05200000009002 ➔ ACC05200000009002"],
  "evidence_hash": "a4f9b8c0...",
  "hash_generated_at": "2026-06-02T10:00:00Z"
}
```

### Ingestion endpoint: `POST /predict/single`
Lookup coordinates features of a single account profile.
* **Request JSON:** `{"features": {"F670": 1.0, "F886": 0.45, ...}}`
* **Response JSON (200 OK):**
```json
{
  "account": "ACC0520000000028",
  "ml_score": 0.01,
  "graph_score": 0.01,
  "composite_score": 0.5,
  "severity": "LOW",
  "mule_stage": "LEGITIMATE",
  "shap_signals": {"F670": 0.0, "F886": 0.01},
  "goaml_xml": null,
  "case_id": null,
  "profile_risk": 0.01,
  "transaction_risk": 0.0,
  "graph_risk": 0.01
}
```

### Ingestion endpoint: `POST /ingest-i4c`
Simulates government threat intelligence webhook ingestion.
* **Request JSON:** `{"account_no": "ACC0520000000028", "portal_ref": "I4C-2026-8819", "alert_type": "Dormant Reactivation"}`
* **Response JSON (200 OK):** Returns composite scores, action executed (`AUTO_FREEZE` / `INVESTIGATOR_QUEUED`), and compiled goAML compliance XML file.

---

## 4. Machine Learning & Preprocessing Pipeline
Stand-alone inference leverages a pre-trained **XGBoost Classifier** model.

### Features Preprocessing (122 features):
1. **Leakage containment:** Drops F3912 (prior audit warnings flag) and F3924 (target labels) to prevent leakage during inference.
2. **Categorical encodings:** Maps string categories to integer encodings dynamically according to a pre-defined metadata schema (`cat_mappings.json`).
3. **Missing columns alignment:** Inspects columns against `final_metadata.json`, generating missing features all-at-once with `np.nan` values using `pd.concat` to prevent DataFrame fragmentation.
4. **SimpleImputer transform:** Imputes missing features using a pre-fit `SimpleImputer` pipeline.
5. **SHAP attribution:** Generates feature contribution vectors using SHAP TreeExplainer attributions to return explanations.

---

## 5. Composite Risk Fusion Engine

### The Score Fusion Equation (Fusion v5)
The platform combines standalone Machine Learning probabilities, Network Centralities, and Live Transaction heuristic rules:

$$\text{Composite Risk} = (\text{Profile Risk} \times 0.40) + (\text{Transaction Risk} \times 0.40) + (\text{Graph Risk} \times 0.20)$$

Where:
* **Profile Risk ($\text{Profile Risk}$):** Standard XGBoost positive probability percentage (ranges between `0.0` and `100.0`).
* **Graph Risk ($\text{Graph Risk}$):** Scaled Neo4j Bolt GDS normalized degree centrality, or standalone ML score if databases are offline.
* **Transaction Risk ($\text{Transaction Risk}$):** Point-based accumulation derived from 7 heuristic transaction analyzers (ranges between `0.0` and `100.0`):
  * Active cycle detection: 40 points
  * Layering loops: 30 points
  * Structuring thresholds: 20 points
  * High Velocity passes: 20 points
  * Anomaly volume: 15 points
  * Dormant reactivation: 15 points
  * Machine learning isolation forest anomalies: 10 points

### Severity Classification Mapping (Tiers)
* **CRITICAL:** Score $\ge 80.0$ (Action: `AUTO_FREEZE` webhook triggers, goAML STR file compiled)
* **HIGH:** $60.0 \le$ Score $< 80.0$ (Action: `INVESTIGATOR_QUEUED`, goAML STR file compiled)
* **MEDIUM:** $40.0 \le$ Score $< 60.0$ (Action: `INVESTIGATOR_QUEUED`, goAML STR file compiled)
* **LOW:** Score $< 40.0$ (Action: `INVESTIGATOR_QUEUED`, no STR generation)

---

## 6. Mule Staging Decision Matrix
Mule stages align composite scores, Standalone XGBoost outputs, and live transaction indicators to assign the account's operational state:

| Base ML Stage | Fusion Severity | Transaction Risk (Points) | Resolved Stage | Recommended Action |
| :--- | :--- | :--- | :--- | :--- |
| Any | `CRITICAL` | Any | **BEING_FLUSHED** | Freeze all debit transactions instantly. |
| Any | `HIGH` | Any | **ACTIVE_MULE** | Lock digital channels (UPI/Internet banking). |
| Any | `MEDIUM` | Any | **NEWLY_RECRUITED**| Queue case for priority human investigator audit. |
| `DORMANT` | `LOW` / `MEDIUM` | $\ge 15.0$ | **ACTIVATION** | Suspend digital transactions pending verification. |
| `DORMANT` | `LOW` | $< 15.0$ | **DORMANT** | Retain in sleep monitoring status. |
| `LEGITIMATE` | `LOW` | $< 15.0$ | **LEGITIMATE** | Retain in standard monitoring status. |
