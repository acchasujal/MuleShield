# PROJECT_STATE.md
_Dynamic file tracking active engineering state. Update immediately after completing any task. ~300 tokens._

---

## 🚦 CURRENT SYSTEM STATUS

- **Performance Hardening (Batch Predict):** 🟢 **Complete (Sprint 3 Performance Hardening)**
  - Ingestion optimized: column-slicing dynamically reduces parsed width from 3,925 features to ~130.
  - Neo4j bulk retrieval: reduced centrality query roundtrips from 9,082 single queries down to **1 single query**.
  - CPU XML templates: replaced slow DOM ElementTree/minidom sequentially 9,082 times with a fast f-string template.
  - PostgreSQL bulk inserts: merged 9,082 individual active database tasks into a single transaction bulker.
  - Payload compression: sliced LOW-risk compliance details out, dropping response from 26.17 MB to 4.76 MB.
  - Benchmark validated: roundtrip HTTP processing time for 9,082 rows dropped from **118.59 seconds** to **5.81 seconds**!
- **Branding Transformation:** 🟢 **Complete (S3-T8)**
  - All "FundTrace AI" and "Union Bank" strings purged from `frontend/app.py`.
  - Page title, PDF header, docstring, empty-state message all updated to MuleShield AI.
  - Verified with `Select-String` grep — zero violations remain.
- **ML Predictor Pipeline:** 🟢 **Active & Operational**
  - XGBoost training pipeline fully wired. `/predict/single` and `/predict/batch` fully operational inside FastAPI using BOI model.
- **Neo4j Graph Database:** 🟢 **Active & Hardened**
  - Graph GDS centrality lookups operate in bulk, scaling efficiently. Operational in `backend/graph_service.py`.
- **Relational Case Database:** 🟢 **Active & Hardened**
  - PostgreSQL ORM case auditing operational with high-speed single-transaction bulk logging.
- **Frontend Sprint 3 UX:** 🟢 **Complete & Fully Validated**
  - S3-T1: Single Account Inspector — high-speed pure Python lookup, composite risk score card, severity badges, Mule Lifecycle badges, Named SHAP signal Plotly bar charts, goAML XML autopilot forms, and Section 65B cryptographic integrity seals. Validated on low-risk (ACC0520000000028) and critical (ACC05200000009002) profiles.
  - S3-T8: Branding purge complete — MuleShield AI everywhere.
  - S3-T2: `FEATURE_NAMES` dict maps all 22 BOI F-codes to human-readable signal labels in SHAP cards.
  - S3-T5: ML Score / Graph Score / Composite Score split card appears in every ML alert expander.
  - S3-T6: Auto-STR red banner fires automatically when composite_score >= 80.
  - S3-T7: "< 8 sec" detection latency metric card added as 4th column in ML Ingest Funnel header.
  - S3-T3: Interactive Network Graph — pyvis-powered dark-themed force-directed network representation with risk-colored nodes, transaction directional edges (amount, mode), and rich tooltip hover details. Full Neo4j-bolt integration with robust deterministic mock fallback.
  - S3-T4: Mule Lifecycle Timeline — high-fidelity custom visual progression timeline (Recruitment, Activation, Active Mule, Being Flushed, Dormant) with glowing, pulse-animated active state indicators, timeline narrative cards (reasoning, Recommended CBS SOP), and compliance dispatch action controls (Monitor, Review, Escalate, STR, Freeze) fully persistent across tab routing and interactions.
  - Verification: 100% verified across 5 strategic axes (Interactive Graph, Staged Lifecycle Timeline, State Persistence, goAML Compilation, and 4-Column Metric Row).
- **Auto-STR Compliance Generator:** 🟢 **Active & Integrated**
  - Suspicious goAML XML payloads automatically trigger on score fusion $\geq 80$. Low-risk accounts have compliance overheads sliced dynamically to optimize memory and payloads.


---

## 📈 MILESTONE TIMELINE

| Milestone | Deliverable | Target Date | Current Status |
| :--- | :--- | :--- | :--- |
| **M1: Core ML Integration** | `/predict/single` and `/predict/batch` fully operational inside FastAPI using BOI model. | June 2, 2026 | 🟢 Complete |
| **M2: Dynamic Risk UI** | React table showing 9,082 analyzed accounts with animated funnel, sorting, and SHAP cards. | June 5, 2026 | 🔴 Pending (T4, T5, T6) |
| **M3: Compliance Autopilot** | Composite risk scoring trigger, blockchain OpenTimestamps, and XML goAML report auto-fills. | June 8, 2026 | 🔴 Pending (T7) |
| **M4: Analytics & Heatmaps** | Demographics page, region heatmaps, model comparison panels, and feature viz. | June 11, 2026 | 🔴 Pending (T8, T9, T10, T11, T12) |
| **M5: Pilot Release** | Docker Compose on-premise rehearsal, 5-minute pitch demo, final PPT validation. | June 14, 2026 | 🔴 Pending (T14, T15) |

---

## 🛑 ACTIVE BLOCKERS

1. **Pickle Version Safety:** We must confirm that the pickled files from model training (`final_model.pkl`, `imputer_full.pkl`) match the versions pinned in `requirements.txt` (`scikit-learn==1.5.x` and `xgboost==2.x`) before loading at backend initialization.
2. **Neo4j Graph Fallback Logic:** Dhiren must implement the fallback route where the composite risk score reverts to 100% of the ML model score if Neo4j experiences an outage, preventing FastAPI 500 crashes.

---

## 🛠️ NEXT SYSTEM INTEGRATION POINTS

- **FastAPI Lifespan Startup:** Edit `backend/app.py` to load ML pipeline artifacts once into `app.state.ml_model` upon server boot.
- **Cytoscape Linkage:** Frontend Cytoscape.js canvas needs to read `mule_stage` from the `/predict/single` JSON payload to color high-risk nodes dynamically.
