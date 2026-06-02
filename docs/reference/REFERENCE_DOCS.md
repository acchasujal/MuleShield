# REFERENCE_DOCS.md
_Low-frequency reference materials, slide deck blueprints, demo scripts, and compliance checklists. ~1500 tokens._

---

## 🏛️ BANK OF INDIA PS-2 HACKATHON FOCUS

The public presentation and evaluation panels are composed of three distinct groups:
1.  **BOI Fraud & Audit Officers:** Looking for rapid, reliable detection, minimal false positives, and ease of use in branch networks.
2.  **IIT Hyderabad AI Academics:** Demanding rigorous feature engineering, model explainability (SHAP), data safety, and robust class imbalance handling.
3.  **DFS / IBA Regulatory Overseers:** Focussed on compliance (PMLA Section 12, goAML reporting), blockchain evidence integrity, and cross-channel ingestion.

---

## 🗣️ DEMO PREPARATION SCRIPTS

### The 5-Minute Live Walkthrough
*   **0:00 - 0:30 [The Hook]:** "Imagine a victim reports a cyber-fraud to the government's MHA I4C portal. Within milliseconds, the funds are split and channeled across accounts. Let's see how MuleShield AI blocks this laundering flow."
*   **0:30 - 1:30 [Tabular ML Ingest]:** "We drag and drop the BOI transaction file. The API processes 9,082 records in under 4 seconds. An account is flagged with a composite risk score of 87.2 - CRITICAL."
*   **1:30 - 2:30 [Explainable AI]:** "IIT-H judges will ask: *Why was it flagged?* We show the SHAP attribution card. Feature F670 regulatory flag is active (+28 pts). Feature F886 shows high-velocity channel switching (+22 pts). Feature F3908 shows funds leaving within 40 minutes of entering (+19 pts). We demystify the black box."
*   **2:30 - 3:30 [Graph Network Ring]:** "But individual checks only see single points. We click to open Cytoscape.js. The graph network reveals a coordinated 3-hop mule ring. 4 adjacent nodes are also scoring high risk. tabular models catch 1 account; MuleShield catches the entire network."
*   **3:30 - 4:30 [Staging & goAML STR]:** "We identify the account is in the `ACTIVE_MULE` stage. We click *Generate STR*. The goAML-compliant XML compiles instantly, ready for FIU-IND submission, complete with a local SHA-256 blockchain audit hash."
*   **4:30 - 5:00 [Wrap Up]:** "Zero cloud footprint. Designed for BOI's on-premise hardware. Ready for deployment. Thank you."

### The 90-Second Rapid Pitch
1.  **Ingestion (15s):** "MuleShield AI ingests large transaction logs, processing 9,082 accounts in under 4 seconds using local XGBoost models trained on the BOI dataset."
2.  **Explainability (30s):** "We flag high-risk entities with composite scores. The SHAP dashboard explains the exact reasons (e.g. prior flags + fast money rotation), converting raw features into actionable intelligence."
3.  **Network Traversal (30s):** "Neo4j graph traversals expose multi-hop layering and circular loops, flagging entire cooperative mule networks rather than single accounts."
4.  **Auto-Compliance (15s):** "Critical accounts automatically trigger goAML-compliant XML reports anchored on the blockchain. MuleShield turns hours of manual auditing into seconds of automated security."

---

## 🎯 TOP JUDGING Q&A PREPARATION

### Q1: Why combine Tabular ML with Graph Database intelligence?
*   **Ideal Answer:** Tabular machine learning (XGBoost) excels at identifying point anomalies based on account features and transaction behaviors. However, mule accounts operate in networks (splitting, routing, and layer transfers). These patterns are structural and cooperative. Graph databases allow us to run centrality, hop, and cycle detection queries to identify the coordinated networks that tabular models miss.

### Q2: How did you handle the severe class imbalance in the BOI dataset?
*   **Ideal Answer:** The dataset contains 81 mule accounts out of 9,082 (a 0.9% positive class rate). We handled this by applying SMOTE (Synthetic Minority Over-sampling Technique) on the 122-feature train split, and set the XGBoost hyperparameter `scale_pos_weight = 111` to match the ratio. We measure performance strictly using Precision-Recall Area Under the Curve (PR-AUC) rather than raw accuracy.

### Q3: Why is feature F3912 excluded from your model training?
*   **Ideal Answer:** Feature F3912 has a 0.97 correlation with the target variable, representing prior transaction monitoring system flags. Using it would cause data leakage and a trivial model. We excluded F3912 from model inputs to ensure the model generalizes to new, unflagged accounts. We use F3912 strictly in post-inference *Mule Lifecycle Staging*.

### Q4: How do you guarantee secure data sovereignty on Bank of India servers?
*   **Ideal Answer:** The application is packaged as an on-premise multi-container Docker Compose application. All processing, calculations, and data stores (Neo4j, PostgreSQL, Redis) run locally on BOI's physical hardware. For the compliance report narratives, we use a local Ollama instance running Llama 3 (8B) to generate narratives locally. Zero data leaves BOI's network.

---

## ⚖️ REGULATORY COMPLIANCE REFERENCES

*   **PMLA 2002 (Prevention of Money Laundering Act):**
    *   **Section 12:** Mandates banks maintain a record of all transactions and verify client identities.
    *   **Section 13:** Empowers authorities to impose fines on banking institutions for failure to report suspicious activities.
*   **goAML Web Platform (FIU-IND):**
    *   **Suspicious Transaction Report (STR):** Automated XML export must map to FIU-IND's goAML schema version 3.1, encapsulating account keys, transaction amounts, timestamps, and reason narratives.
*   **FATF (Financial Action Task Force) Recommendation 20:**
    *   Mandates financial institutions promptly report transactions suspected of being linked to money laundering or terrorist financing.
*   **Indian Evidence Act:**
    *   Requires digital forensics evidence to remain unaltered. We address this by generating a SHA-256 hash of the generated STR XML, anchoring it using OpenTimestamps blockchain integration to guarantee court-admissible custody tracking.
