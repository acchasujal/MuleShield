# DECISIONS.md
_Architectural Decision Records (ADRs) capturing design tradeoffs and critical rationale. ~600 tokens._

---

## 🏛️ ADR 1: Tabular Machine Learning + Graph DB Score Fusion

### Status
**APPROVED**

### Context
Tabular machine learning models (like XGBoost) are effective at detecting point-in-time anomalous transactions and account features. However, money laundering is structurally cooperative; criminal organizations split, layer, and rotate funds across account nodes. These relational topologies (such as multi-hop laundering chains or round-tripping circular loops) look completely normal on an individual account level, leading to high false-negative rates in pure tabular models.

### Decision
We fuse **XGBoost machine learning** (which captures individual demographic and transaction behavioral anomalies) with **Neo4j graph metrics** (which analyze network relationships, cycles, layering paths, and node centrality).

### Tradeoffs & Implications
*   **Pros:** Dramatically reduces false positives. Catches organized rings instead of just single anomalous accounts.
*   **Cons:** Higher runtime latency due to graph traversals. Rebuilding the graph for every single inference request is slow.
*   **Resolution:** We implement parallel score retrieval using `asyncio.gather()`. If Neo4j is offline or slow, the engine safely falls back to a 100% ML score to ensure service availability.

---

## 🚫 ADR 2: Complete Exclusion of Feature F3912 from ML Training

### Status
**APPROVED**

### Context
Feature **F3912** has a 0.97 correlation with the target variable (`F3924` / mule account flag). During preliminary analysis, it was identified as representing historic warnings or alerts in BOI's legacy transaction monitoring system. Using this feature inside training creates a data leakage risk, resulting in a trivial model with 99%+ accuracy that does not generalize to new, undetected laundering patterns.

### Decision
We **completely exclude F3912** from all training partitions, data preprocessing scaling, and the `final_metadata.json` feature list.

### Tradeoffs & Implications
*   **Pros:** Prevents data leakage. Guarantees the XGBoost model learns actual behavioral patterns rather than relying on prior flags.
*   **Cons:** Lowers raw accuracy metrics on paper.
*   **Resolution:** We explain the exclusion as a positive design choice to the IIT Hyderabad judges, highlighting it as proof of model robustness. F3912 is reserved strictly for post-inference *Mule Lifecycle Staging*.

---

## 🔒 ADR 3: Pure On-Premise Multi-Container Docker Deployment

### Status
**APPROVED**

### Context
Public Sector Banks (PSBs) like Bank of India operate under strict regulatory and data privacy frameworks. Financial data, transaction logs, and customer demographics cannot leave BOI's secure internal network due to RBI guidelines. Cloud-based ML hosting or SaaS-based APIs are non-viable.

### Decision
The entire system is packaged as an **on-premise multi-container Docker Compose application**. All databases (Neo4j, PostgreSQL, Redis) and engines are self-contained.

### Tradeoffs & Implications
*   **Pros:** Fulfills regulatory guidelines. Zero-knowledge footprint outside BOI's hardware. Excellent offline performance.
*   **Cons:** Restricts CPU/GPU scalability to host hardware bounds.
*   **Resolution:** System parameters are optimized for light resources, running XGBoost inference and NetworkX/Neo4j queries locally without external hardware requirements.

---

## 🤖 ADR 4: Local Ollama LLM Fallback for Compliance Reports

### Status
**APPROVED**

### Context
Compliance goAML XML generation requires writing clear, natural-language narrative reports explaining *why* the transaction was flagged. While external APIs (like Claude) produce rich narratives, they are non-viable for sensitive, offline production environments.

### Decision
We use a hybrid LLM model. By default, the system uses a **local, on-premise Ollama instance** running Llama 3 (8B) to generate compliance narratives locally. In development, the system can fallback to the Claude API via environment variables.

### Tradeoffs & Implications
*   **Pros:** Fulfills security guidelines. Zero data leaves BOI's network during automated report generation.
*   **Cons:** Higher local hardware RAM requirement for running the 8B parameter model.
*   **Resolution:** System fallback permits standard template-based narrative generation if local LLM resources are unavailable, preventing bottlenecks.
