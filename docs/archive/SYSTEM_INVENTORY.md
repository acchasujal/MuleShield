# MuleShield AI — System Inventory

This document provides a comprehensive, production-grade map of the **MuleShield AI** financial crime intelligence platform. It catalogues the architectural layers, service dependencies, machine learning pipelines, and user interfaces that compose the platform.

---

## 1. Architectural Blueprint

```mermaid
graph TD
    UI[Streamlit Frontend: app.py] -->|HTTP REST / JSON| BE[FastAPI Backend: app.py]
    
    subgraph REST API Routers
        BE --> R1[ml_predict.py: /predict/single]
        BE --> R2[i4c_webhook.py: /ingest-webhook]
        BE --> R3[app.py: /generate-str & /ask]
    end

    subgraph Core Intelligence Services
        R1 --> MLS[MLService: ml_service.py]
        R1 --> GS[GraphService: graph_service.py]
        R1 --> RF[Risk Fusion Engine: risk_scoring.py]
        R2 --> DB[PostgreSQL Auditing: database.py]
        R3 --> LLM[AI NIM / Gemini Clients]
    end

    subgraph Data & Storage Layer
        MLS -->|XGBoost + SHAP| ML_Art[ML Artifacts: .pkl / .json]
        GS -->|Transaction Subgraph| Neo4j[(Neo4j Bolt Database)]
        DB -->|Audit Logging| Postgres[(PostgreSQL Database)]
        MLS -->|Pure Python Lookup| Dataset[data/boi/DataSet.csv]
    end
    
    style UI fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
    style BE fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#fff
    style Core Intelligence Services fill:#0f172a,stroke:#f59e0b,stroke-width:1px,color:#fff
    style Data & Storage Layer fill:#1e293b,stroke:#64748b,stroke-width:1px,color:#fff
```

---

## 2. Component Directory

### 🖥️ Frontend
*   **Implementation:** `frontend/app.py` (Streamlit framework).
*   **Role:** The command terminal for investigators and compliance officers. Implements sleek HSL glassmorphism styles, live alert streams, account-level explainable profiling, dynamic network visualizations, sandbox controls, and regulatory filing logs.
*   **Key Dependencies:** `streamlit`, `plotly`, `pyvis`, `reportlab`, `pandas`.

### ⚙️ Backend
*   **Implementation:** `backend/app.py` (FastAPI).
*   **Role:** Exposes high-performance REST APIs to handle real-time and batch predictions, process government cybersecurity webhook intakes, compile suspect dossiers, and generate legal suspicion declarations.
*   **Key Dependencies:** `fastapi`, `uvicorn`, `pydantic`.

### 🧠 Machine Learning (ML)
*   **Implementation:** `backend/ml_service.py` (Stateless inference service class `MLService`).
*   **Role:** Evaluates risk probability, performs categorical mapping, handles missing data imputation, computes SHAP attributions, and determines mule lifecycle stages.
*   **Loaded Artifacts (`backend/ml_artifacts/`):**
    *   `final_model.pkl`: Pre-trained XGBoost classification model.
    *   `imputer_full.pkl`: Fitted SimpleImputer for handling missing metrics.
    *   `final_metadata.json`: Feature header ordering specification (122 elements).
    *   `cat_mappings.json`: Pre-computed string category indices.
    *   `feature_importances.csv`: Static global importances used as a high-speed fallback.

### 🕸️ Graph Database (Neo4j)
*   **Implementation:** `backend/graph_service.py` (Bolt protocol client class `Neo4jService`).
*   **Role:** Houses the complete transaction ledger graph representation. Traverses directed connections to detect laundering loop closures, calculate account-level degrees, and identify potential suspect clusters.
*   **Offline Mode:** If connection fails on port 7687, gracefully falls back to Standalone ML mode (setting graph risk score to 0.0) without crashing request threads.

### 🐘 Relational Database (PostgreSQL)
*   **Implementation:** `backend/database.py` (SQLAlchemy / Asyncpg pool).
*   **Role:** Records case audit trails and tamper-proof legal hashes (`CaseAudit` model).
*   **Offline Mode:** Uses connection error suppression; if PostgreSQL is offline on port 5432, it reverts to file-based logs and silently allows the main application loop to proceed.

### 🌐 I4C Webhook
*   **Implementation:** `backend/routers/i4c_webhook.py` (`POST /ingest-webhook`).
*   **Role:** Simulates the intake of cyber complaint reports from the Government's **I4C** (Indian Cyber Crime Coordination Centre) portal, auto-indexing accounts for immediate composite audit scoring and frozen debit flags.

### 📄 goAML XML Reporter
*   **Implementation:** `backend/xml_generator.py` (`generate_goaml_xml()`).
*   **Role:** Formats suspect profiles, composite scores, attributions, and transactional flows into an XML file compliant with FIU-IND (Financial Intelligence Unit - India) and goAML schema standards.

### 🔍 SHAP Explainability
*   **Implementation:** `backend/ml_service.py` (`TreeExplainer` integration).
*   **Role:** Generates local feature attribution values per single transaction prediction.
*   **Branding Mapping:** A lookup index (`FEATURE_NAMES` in `frontend/app.py`) translates cryptic column names (e.g. `F670`, `F886`, `F3908`) into plain language descriptions (e.g. "Regulatory TMS Flag", "Channel Switching Rate", "High-Velocity Pass-Through") in the investigator interface.

### 🔗 Graph Intelligence
*   **Implementation:** Combined ML predictions and Neo4j topology queries.
*   **Role:** Analyzes money-laundering loops, shell-routing chains, and high-degree branch activity. Elevates standard tabular scoring by evaluating graph anomalies.

### ⚡ Risk Fusion Engine
*   **Implementation:** `backend/risk_scoring.py` (`calculate_composite_risk()`, `assign_tier()`).
*   **Role:** Blends standard tabular ML scores (70%) and Neo4j graph structural risk (30%) into a unified **Composite Risk Score** [0 - 100]. Tiers risk as CRITICAL (composite $\ge$ 80), HIGH (60-80), MEDIUM (30-60), or LOW (<30).

### 🕵️ Investigator UI
*   **Implementation:** "🔍 Account Inspector" and "🕵️ Alert Center" frontend modules.
*   **Role:** Interactive panel that allows investigators to enter individual account IDs, visualize dynamic 3-hop Pyvis subgraphs, inspect SHAP waterfall contributions, view 4-stage lifecycle meters, and run AI-assisted Q&A case audits.

### 📊 Executive Dashboard
*   **Implementation:** "📈 Executive Dashboard" frontend view.
*   **Role:** Premium dashboard representing overall platform effectiveness. Displays prevented financial losses, governmental webhook ingestion rates, core engine benchmark velocities, channel splits, and demographic vulnerability distributions.

### 🎮 Demo Mode
*   **Implementation:** "🎮 Demo Mode" sandbox hub (`frontend/app.py`).
*   **Role:** Enables instant, zero-configuration interactive tours. Operators can launch three simulated laundering scenarios in a single click:
    1.  **Round-Trip Layering Loop:** An intricate cycle converging on a single high-volume RTGS sink account.
    2.  **UPI Structuring / Smurfing:** Rapid channel switching of sub-threshold (₹49,999) UPI deposits to evade legacy rules.
    3.  **Dormant Account Reactivation:** Sudden surge of high-velocity pass-through transfers inside a previously dormant student profile.
