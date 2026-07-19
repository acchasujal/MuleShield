# MuleShield AI

> **AI-Native Financial Trust Infrastructure**  
> A dual-engine platform that transforms financial behavior into explainable trust intelligence.

---

## What Is MuleShield AI?

MuleShield AI is infrastructure for **trust at scale** in digital finance. It continuously understands financial behavior, detects coordinated abuse, and generates compliance-ready evidence—enabling banks to protect their networks in real time.

Today, it powers **money-mule account detection and containment**. Tomorrow, it becomes the trust layer upon which a nation of 500M digital finance users builds with confidence.

### The Problem We Solve

India's digital payment rails (UPI, NEFT, IMPS) are moving **₹500+ trillion annually**. Fraud rings exploit a critical gap: the **4–72 hour delay** between when a victim files a complaint and when a bank can investigate and freeze an account.

In that window, ₹1,776 crore annually flows through mule accounts—recruited from vulnerable, newly-banked populations—before dispersing beyond recovery.

**MuleShield collapses that window to 4 seconds.**

---

## How It Works

### The Architecture

MuleShield fuses three independent intelligence engines:

```
Transaction Data
       ↓
   ┌───┴───┐
   ↓       ↓
 ML Risk  Graph Risk    Heuristic Risk
(XGBoost) (Neo4j GDS)   (NetworkX)
   ↓       ↓               ↓
   └───┬───┴───────────────┘
       ↓
Composite Risk Score (0–100)
       ↓
  Severity Tier + Explanation
       ↓
  Lifecycle Stage Classification
       ↓
  Evidence Package (goAML XML + SHA-256)
```

Each engine catches what the others miss:

- **ML Engine (40%)**: Detects behavioral anomalies and profile drift (built on XGBoost + SMOTE balancing for severely imbalanced fraud datasets).
- **Graph Engine (20%)**: Identifies topological hubs, cycles, and fan-in/fan-out laundering patterns (Neo4j GDS degree centrality + NetworkX community detection).
- **Transaction Heuristics (40%)**: Flags structuring, velocity spikes, dormant reactivation, and channel anomalies via rule-based scorers.

### The Output

Every flagged account receives:

1. **Composite Risk Score**: 0–100, fused from all three engines.
2. **Plain-English Explanation**: SHAP-driven translation of why the account is risky (e.g., "Prior regulatory flag active" + "Unusual rapid channel-switching").
3. **Lifecycle Stage**: DORMANT | ACTIVATION | NEWLY_RECRUITED | ACTIVE_MULE | BEING_FLUSHED.
4. **Compliance-Ready Report**: goAML XML (FIU-IND format) + SHA-256 hash for Section 65B Evidence Act compliance.

---

## The Platform

MuleShield AI is designed as a **modular, compounding system**, not a single model.

| Component | Purpose | Status |
|---|---|---|
| **Trust Intelligence Engine** | Composite risk fusion (ML + graph + heuristics) | ✅ Prototype |
| **Explainability Layer** | SHAP-based plain-English reasoning | ✅ Prototype |
| **Evidence Engine** | goAML XML generation + tamper-evident hashing | ✅ Prototype |
| **Investigator Workspace** | UI for analyst investigation and case management | ✅ Prototype |
| **Trust APIs** | Programmatic trust-signal access for bank systems | 🔄 Planned |
| **Cross-Bank Intelligence** | Privacy-preserving shared risk signals (federated) | 📅 Vision |
| **Regulator Portal** | Direct integration with FIU-IND portal | 📅 Vision |

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Backend API** | FastAPI, Uvicorn |
| **ML / Explainability** | XGBoost, SHAP TreeExplainer, scikit-learn |
| **Graph Intelligence** | Neo4j (GDS), NetworkX |
| **Database** | PostgreSQL (audit log), Neo4j (transaction graph) |
| **Frontend** | React + TypeScript + Vite + Framer Motion |
| **Infrastructure** | Docker Compose, on-premise/air-gapped capable |
| **Compliance** | goAML XML generation, SHA-256 hashing |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### 1. Start Databases

```bash
docker-compose up -d
```

This spins up PostgreSQL and Neo4j containers. Verify:
```bash
docker-compose ps
```

### 2. Run Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Access Swagger docs at `http://localhost:8000/docs`.

### 3. Run Frontend

```bash
cd frontend-react
npm install
npm run dev
```

Access the Investigator Workspace at `http://localhost:5173`.

---

## API Endpoints (Prototype)

### Analyze Batch
```bash
POST /analyze
Content-Type: multipart/form-data

# Upload a CSV of transactions
# Returns composite risk scores, SHAP explanations, lifecycle stages, goAML XML
```

### Single Account Prediction
```bash
POST /predict/single
Content-Type: application/json

{
  "features": { "F670": 1.0, "F886": 0.45, ... }
}

# Returns: ml_score, graph_score, composite_score, shap_signals, mule_stage
```

### I4C Webhook (Government Alert Ingestion)
```bash
POST /ingest-i4c
Content-Type: application/json

{
  "account_no": "ACC0520000000028",
  "portal_ref": "I4C-2026-8819",
  "alert_type": "Dormant Reactivation"
}

# Returns: composite_score, action_recommended (AUTO_FREEZE | INVESTIGATOR_QUEUED), goAML_xml
```

---

## Documentation

Full documentation is in the `/docs` folder, numbered for clarity:

- **PROJECT_CONTEXT.md** — Vision, problem statement, differentiators
- **ARCHITECTURE.md** — System blueprints, risk fusion formulas, API contracts
- **BUILD_GUIDE.md** — Implementation roadmap and 48-hour sprint plan
- **DESIGN_SYSTEM.md** — Visual language and UI/UX specifications
- **AI_CONTEXT.md** — ML feature mappings, SHAP signals, technical notes
- **PECHACKS_STRATEGY.md** — Hackathon positioning, judge Q&A prep

---

## Prototype Validation

### Dataset Performance
- **Dataset**: 9,082 account profiles (3,924 raw features, 122 validated).
- **Class Distribution**: 81 mule accounts vs. 9,001 legitimate (111:1 imbalance).
- **ML Pipeline**: XGBoost with SMOTE oversampling on training set.
- **Validation Approach**: Stratified cross-validation, leakage detection verified.

### Key Findings
- **F2082 (Zero Normal Banking Behavior)**: Strongest negative predictor — all confirmed mules scored 0.0.
- **F3912 Exclusion**: Correctly identified and excluded from training to prevent data leakage.
- **Established Account Reactivation**: 89% of mule accounts > 365 days old (dormant recruitment pattern).

---

## Deployment

### On-Premise / Air-Gapped
MuleShield is designed for bank-side deployment with zero cloud dependency:

- PostgreSQL and Neo4j run locally in Docker.
- FastAPI backend connects via standard server hardware (8-core/32GB validated).
- Fallback modes: if Neo4j is unavailable, system runs on ML scoring alone.
- No internet required after initial setup; batch ingestion via CSV or webhook.

### Production Roadmap
1. **Phase 1 (Pilot)**: Single bank, 90 days, 3 branches, Docker single-server.
2. **Phase 2 (Scale)**: Bank national rollout with Kafka event streaming.
3. **Phase 3 (Infrastructure)**: Multi-bank federated intelligence with privacy-preserving collaboration.

---

## Contributing

This is a hackathon project. For production use, security audits, regulatory validation, and data governance are required.

---

## License

[To be specified]

---

## Contact

**PEC Hacks 4.0 Submission**  
Team: [Your Team Name]  
Email: [your-email@example.com]

---

## Key References

- **Problem Domain**: Money-mule accounts in UPI-scale digital payments
- **Use Case**: Real-time suspicious-account containment & regulator reporting
- **Impact**: 4-second response vs. 4–72 hour manual investigation
- **Positioning**: AI-native Financial Trust Infrastructure

For judges and stakeholders: **MuleShield AI is the infrastructure layer that makes trust possible at the scale of India's digital financial inclusion.**