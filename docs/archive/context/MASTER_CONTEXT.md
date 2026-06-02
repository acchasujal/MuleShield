# MASTER_CONTEXT.md
_Load this file at the start of every agent session. Highly dense, structured reference. ~600 tokens._

---

## 🎯 PROJECT IDENTITY

*   **Product:** **MuleShield AI** (evolved from FundTrace AI)
*   **Tagline:** *Real-time mule account detection, classification, and fraudulent proceeds containment.*
*   **Hackathon Challenge:** Public Sector Banks (PSBs) Cybersecurity, Fraud & AI Hackathon 2026
    *   **Problem Statement (PS-2):** AI/ML Classification of Suspicious Mule Accounts (Bank of India)
*   **Organizers:** Bank of India (BOI), IIT Hyderabad (IITH), Department of Financial Services (DFS - Ministry of Finance), and Indian Banks' Association (IBA).
*   **Submission Deadline:** June 15, 2026 (Submission) · June 30, 2026 (Shortlist announcement) · August 27–28, 2026 (Physical Finale at IIT Hyderabad).
*   **Prizes:** 🥇 1st Place: ₹5,00,000 · 🥈 2nd Place: ₹3,00,000 · 🥉 3rd Place: ₹2,00,000.
*   **Team BRUH (Authoritative Owners):**
    *   **Vikram Sindra:** Machine Learning / Data Science Specialist
    *   **Dhiren Mulwani:** Backend & System Integration Specialist
    *   **Shriraj Dyaram:** Frontend & UI/UX Specialist
    *   **Sujal Gupta:** Product, Compliance, and Presentation Strategy Specialist

---

## 🚀 ONE-SENTENCE MISSION

Identify, score, stage, and contain mule account networks in real-time by fusing tabular **XGBoost machine learning** (trained on 3,924 BOI features) with **Neo4j graph intelligence**, producing automated, blockchain-anchored, FIU-IND compliant Suspicious Transaction Reports (STRs) within 8 seconds of alert ingestion.

---

## 🛠️ AUTHORITATIVE TECH STACK

| Layer | Component | Specifications & Version Boundaries |
| :--- | :--- | :--- |
| **Frontend** | Single Page Application | React (v18.x), Cytoscape.js / D3.js (interactive graphs), Vanilla CSS + custom glassmorphism components |
| **Backend** | API Services | Python 3.11, FastAPI (asynchronous endpoints), Uvicorn ASGI server |
| **Graph DB** | Network Intelligence | Neo4j Community Server (Graph Data Science - GDS library enabled) |
| **Relational DB** | Auditing & Compliance | PostgreSQL (v15+) for case management, incident history, and auditing logs |
| **ML Engine** | Tabular Inference | XGBoost (v2.x), Scikit-Learn (v1.5.x), SHAP (explainer model), Imbalanced-Learn |
| **Cache Engine** | Speed & Security | Redis for sliding-window velocity tracking and transactional alert caching |
| **Compliance LLM** | Narratives | Claude API (via client library) with local **Ollama** on-premise fallback (Llama 3 8B) |
| **Evidence Validation** | Anchoring | Local SHA-256 generation with OpenTimestamps blockchain anchoring |
| **Deployment** | Infrastructure | On-premise multi-container Docker Compose. Zero internet dependency option. |

---

## ⚠️ NON-NEGOTIABLE CRITICAL REQUIREMENTS

1.  **Strict Dataset Ingestion:** The ML engine must run and evaluate directly on the provided BOI `DataSet.csv` (9,082 accounts, 3,924 anonymous features F1...F3924, F3924 as target).
2.  **Data Leakage Prevention:** Feature **F3912** has a 0.97 correlation with the target and represents a legacy fraud flag. It **must be completely excluded** from ML model training. It is reserved solely for post-inference *Mule Lifecycle Staging* and validation.
3.  **Correct Metric Reporting:** Since the dataset has a severe class imbalance (0.9% fraud rate), **never report raw accuracy**. Model success is ranked strictly by **Precision, Recall, F1-Score, and PR-AUC**.
4.  **Class Imbalance Resolution:** You must use **SMOTE** (Oversampling) and tune the `scale_pos_weight` hyperparameter in XGBoost (set to `111` to match the ratio) to balance the class weights.
5.  **Strict Branding Cleanliness:** "Union Bank of India", "Union Bank", or "UBI" **must not appear anywhere** in the code, comments, documentation, presentation slides, or user interface.
6.  **No Strategy/SaaS Fluff:** Zero slides or UI sections regarding SaaS pricing, market size (TAM/SAM/SOM), or revenue share. Replace with a pragmatic **3-Phase PSB Deployment Roadmap**.
7.  **Explainable AI (XAI):** Every single transaction alert must serve SHAP explainability. IIT Hyderabad judges will demand mathematical proof of why an account was flagged.
8.  **Formula Visibility:** The composite risk score formula (`ml_score * 0.70 + graph_score * 0.30`) must be explicitly exposed in the UI.

---

## 🎯 WORKSPACE SUCCESS CRITERIA

- [ ] **Batch Analysis:** `POST /predict/batch` executes in under 5 seconds on `DataSet.csv` and returns $\geq 10$ critical/high-severity accounts.
- [ ] **Signal Visualizer:** UI displays at least 3 distinct human-readable risk signals (SHAP to feature translation) per flagged account.
- [ ] **Lifecycle Stage:** Accounts are classified into specific lifecycle stages (*Newly Recruited*, *Active Mule*, *Being Flushed*, *Dormant*).
- [ ] **STR Ingestion:** Automatic goAML-compliant XML reports generate instantly when composite risk $\geq 80$.
- [ ] **Alert Funnel:** UI animates the alert narrowing funnel (9,082 total accounts analyzed $\rightarrow$ N critical cases).
- [ ] **Model Metrics Page:** Interactive PR-AUC and ROC-AUC curves are rendered dynamically.
- [ ] **Zero Downtime Fallback:** Standalone prediction falls back to 100% ML score if the Neo4j instance is disconnected.
