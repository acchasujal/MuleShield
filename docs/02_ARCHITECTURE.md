# 02_ARCHITECTURE.md — MuleShield AI: System Architecture Specification

## 1. High-Level Blueprint

MuleShield AI is designed as a modular **AI-Native Financial Trust Infrastructure**. It converts complex transactional metadata and profile features into a unified financial trust graph, feeding real-time decision and compliance layers.

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
                                            Trust Handoff (goAML XML)
```

### Component Topology
- **FastAPI Gateway (`backend/app.py`):** Exposes core integration API endpoints for trust lookups and network alerts.
- **ML Predictor Client (`backend/ml/predictor.py`):** Scores behavioral anomalies across 122 profile variables.
- **SHAP Engine (`backend/ml/shap_engine.py`):** Translates XGBoost decision boundaries into plain-English attributions.
- **Graph Service (`backend/graph_service.py`):** Tracks topology loops, degree centralities, and flow-direction patterns.
- **Audit Database (`backend/database.py`):** Commits permanent audit logs and cryptographic hashes to PostgreSQL.
- **goAML XML Generator (`backend/xml_generator.py`):** Automates regulatory filing report compilations.

---

## 2. Database Schema Mappings

### PostgreSQL ORM (`case_audits` Table)
Keeps an immutable audit log of threat scores, decisions, and evidence checksums.

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
| `mule_stage` | `String(30)` | Resolved lifecycle stage name. |
| `evidence_hash` | `String(64)` | SHA-256 evidence package checksum. |
| `action_taken` | `String(100)` | Action executed: `AUTO_FREEZE` / `INVESTIGATOR_QUEUED`. |

### Neo4j Graph Model
Represents transaction connections:
- **Nodes:** `(:Account {id: String})`
- **Relationships:** `(:Account)-[:TRANSACTED {amount: Float, timestamp: String, channel: String}]->(:Account)`

---

## 3. Core API Endpoint Contracts

### `POST /analyze`
Ingests transaction details, evaluates composite trust scores, and outputs risk signals.
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

- **Profile Risk (40%):** Tabular XGBoost positive class probability.
- **Graph Risk (20%):** Neo4j GDS normalized degree centrality score.
- **Transaction Risk (40%):** Points compiled from heuristic rules (circular cycles, velocity bounds, dormant activity).
