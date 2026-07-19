# MuleShield AI — System Architecture Specification

## 1. High-Level Blueprint

MuleShield AI uses a dual-engine architecture combining profile-based XGBoost inference with transactional graph analytics to score fraud risk.

```
 Incoming transactions ➔ Ingestion & Slicing
                             ├── Profile Features ➔ XGBoost + SHAP Attributions (ML Engine)
                             └── Graph Relations  ➔ Neo4j GDS Centrality (Graph Engine)
                                                       │
                                                       ▼
                                            Score Fusion (40/40/20)
                                                       │
                                                       ▼
                                            Mule Lifecycle Staging
                                                       │
                                                       ▼
                                           Compliance Handoff (goAML)
```

### Component Topology
- **FastAPI Gateway (`backend/app.py`):** Exposes integration API endpoints for banks and threat intel networks.
- **ML Engine (`backend/ml/predictor.py`):** Runs pre-trained XGBoost classifiers on 122 profile variables.
- **SHAP Engine (`backend/ml/shap_engine.py`):** Generates local explanation weights mapping features to plain English.
- **Graph Service (`backend/graph_service.py`):** Tracks transaction flows, circular routes, and sinks in Neo4j.
- **Audit Database (`backend/database.py`):** Commits permanent audit logs and cryptographic hashes to PostgreSQL.
- **goAML XML Autopilot (`backend/xml_generator.py`):** Automatically builds regulatory compliance filings.

---

## 2. Database Schema Mappings

### PostgreSQL ORM (`case_audits` Table)
Keeps an immutable trace of alerts, composite scores, decisions, and evidence checksums.

| Field | Type | Purpose |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key, Auto-incrementing. |
| `case_id` | `String(50)` | STR case reference number. |
| `account_id` | `String(50)` | Target account ID. |
| `event_type` | `String(50)` | Triggering process (`RISK_FUSION` / `I4C_PORTAL`). |
| `timestamp` | `DateTime(UTC)` | UTC event timestamp. |
| `ml_score` | `Float` | XGBoost model output score. |
| `graph_score` | `Float` | Neo4j degree centrality value. |
| `composite_score`| `Float` | Consolidated fusion risk score. |
| `severity` | `String(20)` | Threat level: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `mule_stage` | `String(30)` | Lifecycle stage name. |
| `evidence_hash` | `String(64)` | SHA-256 evidence package checksum. |
| `action_taken` | `String(100)` | Action executed: `AUTO_FREEZE` / `INVESTIGATOR_QUEUED`. |

### Neo4j Graph Model
Represents transaction connections:
- **Nodes:** `(:Account {id: String})`
- **Relationships:** `(:Account)-[:TRANSACTED {amount: Float, timestamp: String, channel: String}]->(:Account)`

---

## 3. Core API Endpoint Contracts

### `POST /analyze`
Accepts a bulk CSV of transaction events, scores them, and generates alert profiles.
- **Response Shape (200 OK):**
```json
{
  "alerts": [
    {
      "account": "ACC05200000000028",
      "risk_score": 86.0,
      "severity": "CRITICAL",
      "reasons": ["Dormant reactivation", "Velocity spike"],
      "explanation": "A dormant salary account reactivated...",
      "mule_stage": "BEING_FLUSHED",
      "ml_score": 78.0,
      "graph_score": 65.0,
      "shap_signals": {"F3889": 0.82, "F3908": 0.74},
      "goaml_xml": "<goAMLReport>...</goAMLReport>",
      "case_id": "STR-20260719-0028",
      "evidence_hash": "e3b0c442..."
    }
  ]
}
```

---

## 4. Score Fusion Equation

$$\text{Composite Risk} = (\text{Profile Risk} \times 0.40) + (\text{Transaction Risk} \times 0.40) + (\text{Graph Risk} \times 0.20)$$

- **Profile Risk (40%):** Standard XGBoost positive class probability.
- **Graph Risk (20%):** Neo4j GDS normalized degree centrality score.
- **Transaction Risk (40%):** Points compiled from heuristic rules (circular cycles, velocity bounds, dormant activity).
