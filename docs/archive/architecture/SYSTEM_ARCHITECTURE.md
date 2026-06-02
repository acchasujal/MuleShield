# SYSTEM_ARCHITECTURE.md
_Systems design blueprint and service-level architecture diagrams. ~700 tokens._

---

## 🏗️ SYSTEM ARCHITECTURE OVERVIEW

MuleShield AI uses a microservices infrastructure orchestrated via Docker Compose. The system is designed to run completely on-premise on Bank of India servers with zero external internet dependencies, meeting strict PSB security guidelines.

```
                  ┌───────────────────────────────┐
                  │      Client Web Browser       │
                  └───────────────┬───────────────┘
                                  │ HTTPS
                                  ▼
                  ┌───────────────────────────────┐
                  │    React Frontend Container   │
                  │         (Nginx Port 80)       │
                  └───────────────┬───────────────┘
                                  │ API Calls (JSON / CSV Upload)
                                  ▼
                  ┌───────────────────────────────┐
                  │    FastAPI Backend Container  │
                  │          (Port 8000)          │
                  └──────┬────────┬────────┬──────┘
                         │        │        │
            ┌────────────┘        │        └────────────┐
            ▼ Bolt                ▼ SQL                 ▼ Redis Protocol
┌───────────────────────┐ ┌───────────────┐ ┌───────────────────────┐
│     Neo4j Graph DB    │ │ PostgreSQL DB │ │    Redis Cache Engine │
│      (Port 7687)      │ │  (Port 5432)  │ │      (Port 6379)      │
└───────────────────────┘ └───────────────┘ └───────────────────────┘
```

---

## 🔌 CONTAINER SERVICES & PORTS

The system is defined by 5 primary Docker containers:

| Container / Service | Image Base | Internal Port | External Port | Operational Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **muleshield-ui** | Node Alpine + Nginx | 80 | **80** (HTTP) | Serves compiled React web UI, visualizations, and static assets. |
| **muleshield-api** | Python 3.11 Slim | 8000 | **8000** | Runs FastAPI application, loads ML models, orchestrates database connections, processes STR drafts. |
| **muleshield-graph** | Neo4j Community | 7474, 7687 | **7474** (HTTP), **7687** (Bolt) | Stores accounts as nodes and transactions as edges. Computes network graphs. |
| **muleshield-store** | PostgreSQL 15 | 5432 | **5432** | Stores user logins, case audit histories, and generated STR XMLs. |
| **muleshield-cache** | Redis Alpine | 6379 | **6379** | Sliding-window velocity cache and fast transaction rate tracking. |

---

## 🔄 END-TO-END DATA FLOW (Prediction Ingestion Path)

```
[ BOI DataSet.csv Upload ]
            │
            ▼ (POST /predict/batch)
┌────────────────────────────────────────────────────────┐
│ muleshield-api Orchestrator                            │
│                                                        │
│ 1. Pandas parses CSV buffer safely                     │
│ 2. Loads Model artifacts (lifespan)                    │
│ 3. Applies cat_mappings.json to categorical fields     │
│ 4. Imputes remaining null values using imputer_full.pkl│
│ 5. Truncates input matrix to 122 selected features     │
│ 6. Executes XGBoost.predict_proba() -> Tabular Score   │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ├────────────────────────────┐
                           ▼ Parallel Execution         ▼ Parallel Execution
             ┌───────────────────────────┐ ┌───────────────────────────┐
             │ Neo4j Graph Bolt Query    │ │ SHAP Tree Explainer       │
             │                           │ │                           │
             │ - Pulls 3-hop subgraph    │ │ - Calculates SHAP weights │
             │ - Centrality & Hub metrics│ │ - Maps to top-5 human     │
             │ - Reverts to ML if down   │ │   readable signals        │
             └─────────────┬─────────────┘ └────────────┬──────────────┘
                           │                            │
                           └─────────────┬──────────────┘
                                         ▼
                           ┌────────────────────────────┐
                           │ Score Fusion Layer         │
                           │                            │
                           │ Calculate Composite score: │
                           │ 0.7*ML + 0.3*Graph         │
                           └─────────────┬──────────────┘
                                         │
                                         ▼
                           ┌────────────────────────────┐
                           │ Compliance Decision Engine │
                           │                            │
                           │ - Assigns Risk Tier        │
                           │ - Classifies Lifecycle     │
                           │ - If CRITICAL (score >=80) │
                           │   auto-triggers goAML STR  │
                           └─────────────┬──────────────┘
                                         │
                                         ▼
                           [ Comprehensive JSON Response ]
```

---

## 🛡️ SYSTEM FAULT-TOLERANCE & FAILURE RECOVERY

To ensure robust operation under challenging hackathon or deployment conditions, the system implements 5 non-negotiable recovery pathways:

### 1. Database Outage (Neo4j Offline)
*   **Symptom:** Bolt connection failure or socket timeout to `muleshield-graph` on port 7687.
*   **Recovery Action:** Capture the error, log a warning, and set `graph_score = ml_score`. The score fusion calculates `composite_score = ml_score * 1.0` dynamically. Display a warning icon on the frontend: "Standalone ML Classification Mode Active."

### 2. Model Ingest Outage (Pickle Corruption)
*   **Symptom:** Pickle version mismatch or memory error loading `final_model.pkl` on lifespan boot.
*   **Recovery Action:** Load pre-computed analysis matrix `demo_results.json` directly into Redis. The frontend falls back to demo mode seamlessly with zero service crash.

### 3. Unknown Categorical Data (Out-of-Vocabulary Category)
*   **Symptom:** Encountering a value (e.g. occupation F3891 = "influencer") not seen during model fitting.
*   **Recovery Action:** Replace with `0` (the default category code mapping in `cat_mappings.json`) and proceed with inference. Do not crash.

### 4. Large Dataset Performance
*   **Symptom:** API processing 9,082 rows experiences slow traversal timeouts on graph checks.
*   **Recovery Action:** Disable synchronous SHAP explainer runs on batch requests. Batch calls return pre-computed feature importances, while individual SHAP trees run strictly on single-entity requests.
