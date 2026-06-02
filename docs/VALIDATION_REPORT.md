# MuleShield AI — Validation and Hardening Report

This report consolidates all verification proofs, database recovery logs, modularization validations, and reliability audit results for the MuleShield AI platform.

---

## 1. Database Recovery & Infrastructure Setup (Phase 2)

Both Neo4j and PostgreSQL database services were successfully recovered, moving the platform from fallback-only operation to a fully dual-database operational mode.

### 1.1 Root Cause & Solution Matrix
* **Neo4j Recovery:** Re-orchestrated the Neo4j 5.15 Community Edition container via Docker Compose. Restored Bolt protocol access on port `7687` and UI access on port `7474`. Installed `neo4j` Python driver in the virtual environment.
* **PostgreSQL Recovery:** Restored PostgreSQL 16 Alpine container via Docker Compose on port `5432`. Installed the asyncpg Python driver in the virtual environment.
* **Timezone Schema Alignment:** Fixed a timezone-aware database mismatch inside [database.py](file:///d:/Projects/FundTrace-AI/backend/database.py). The ORM schema uses `TIMESTAMP WITHOUT TIME ZONE` (naive), but Python was supplying timezone-aware UTC times. Standardized to naive UTC:
  * Modified `CaseAudit.timestamp` column default to `datetime.utcnow()`.
  * Standardized `log_case_audit` to write naive UTC via `datetime.utcnow()`.

### 1.2 Docker Orchestration Specification (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    container_name: fundtrace-postgres
    environment:
      POSTGRES_DB: muleshield
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d muleshield"]
      interval: 10s
      timeout: 5s
      retries: 5

  neo4j:
    image: neo4j:5.15-community
    container_name: fundtrace-neo4j
    environment:
      NEO4J_AUTH: neo4j/password
    ports:
      - "7687:7687"
      - "7474:7474"
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p password 'RETURN 1'"]
      interval: 15s
      timeout: 10s
      retries: 5

volumes:
  postgres-data:
  neo4j-data:
  neo4j-logs:
```

---

## 2. Graph Intelligence & Runtime Proofs

Neo4j GDS normalized degree centrality is successfully wired into the Fusion v5 risk scoring engine. When the database is online, graph scores directly contribute to composite risk.

### 2.1 Degree Centrality Calculation
Degree centrality is normalized by the active network size:
$$\text{Raw Centrality} = \frac{\text{Degree}}{N - 1}$$
Where $N$ is the total count of `Account` nodes, and $\text{Degree}$ is the sum of incoming and outgoing transacted edges.
* **Scaling & Clamping:** The raw centrality is scaled by a factor of `5.0` for visual contrast and clamped to a range of `[0.0, 1.0]`:
  $$\text{Scaled Centrality} = \min\left(1.0, \text{Raw Centrality} \times 5.0\right)$$

### 2.2 End-to-End Runtime Proof Metrics
A verification test run recorded the following baseline-to-ingested state delta for account `ACC05299999999999`:

| Metric | Before Ingestion (Empty Graph) | After Ingestion (Batch Seed) | Delta / Outcome |
| :--- | :--- | :--- | :--- |
| **Node Count** | 0 | 51 | +51 nodes |
| **Relationship Count** | 0 | 50 | +50 relationships |
| **ML Score** | 0.6500 | 0.6500 | 0.0000 (No change) |
| **Transaction Score** | 0.0000 | 0.0000 | 0.0000 (No change) |
| **Graph Score** | 0.0000 | 1.0000 | **+1.0000** |
| **Composite Risk Score**| 26.0 (0.65 * 40) | 46.0 (26.0 + 1.0 * 20) | **+20.0 points** (Matches 20% weight) |

---

## 3. Score Fusion & Lifecycle Alignment Validation

### 3.1 Severity Cohort Studies
Baseline validation runs checked decision integrity across bimodal cohorts (9,001 `LOW` risk nodes, 81 `HIGH` risk nodes):

* **Cohort A (Legitimate Profile):** Account `ACC05200000000009` baseline
  * ML Score: `0.000015` | Transaction Risk: `0.0` | Graph Score: `0.0`
  * Resolved: `0.1` composite score, `LOW` severity, `LEGITIMATE` lifecycle, `STR = False`.
* **Cohort B (Known Mule Profile):** Account `ACC05200000009002` baseline
  * ML Score: `0.000013` | Transaction Risk: `0.0` | Graph Score: `0.0` (profile-driven rules escalate)
  * Resolved: `60.0` composite score, `HIGH` severity, `ACTIVE_MULE` lifecycle, `STR = True`.
* **Cohort C (Legitimate Profile with Round-Trip Ingest):** Account `ACC05200000000009`
  * ML Score: `0.000015` | Transaction Risk: `100.0` (UPI velocity + loops) | Graph Score: `0.0`
  * Resolved: `40.0` composite score, `MEDIUM` severity, `UNDER_REVIEW` lifecycle, `STR = True`.

### 3.2 Aligned Lifecycle Decision Logic
The lifecycle decision engine resolves conflicting profile-only and transaction-based states:
* If current lifecycle is `LEGITIMATE`, and fusion severity resolves to `MEDIUM` or higher, and active transaction points are greater than `0`, the account's state is upgraded to `UNDER_REVIEW`.
* All existing profile-driven stages (`NEWLY_RECRUITED`, `ACTIVE_MULE`, `BEING_FLUSHED`, `DORMANT`) are preserved and never overridden downwards by transaction scoring.

---

## 4. Backend & ML Modularization Valdiations

The legacy codebase was refactored from a monolithic `backend/app.py` and `backend/ml_service.py` layout to a modular, decoupled package architecture.

### 4.1 Modular Layout
* [backend/app.py](file:///d:/Projects/FundTrace-AI/backend/app.py): Stripped of router logic. Handles startup and teardown lifecycles.
* [backend/routers/](file:///d:/Projects/FundTrace-AI/backend/routers/): Houses independent HTTP routers (`health.py`, `analyze.py`, `ai_chat.py`, `ml_predict.py`, `i4c_webhook.py`).
* [backend/ml/](file:///d:/Projects/FundTrace-AI/backend/ml/): Decoupled ML packages:
  * `predictor.py` (XGBoost inference pipeline)
  * `shap_engine.py` (SHAP TreeExplainer attributions)
  * `feature_lookup.py` (Sequential line seek on DataSet.csv)
  * `lifecycle_engine.py` (Timeline rules)
  * `score_fusion.py` (Scoring weights and alignment helper)

### 4.2 Performance Comparison
Modular separation minimized startup imports and resolved database driver overhead, reducing execution latency:

| Dimension | Monolithic Layout | Modular Refactored Layout | Delta |
| :--- | :--- | :--- | :--- |
| **MLService Startup** | 273.3 ms | 143.6 ms | **-47.4%** |
| **Single Predict (inc. SHAP)** | 89.7 ms | 59.5 ms | **-33.7%** |
| **Batch Predict (20 rows)** | 138.4 ms | 119.3 ms | **-13.8%** |

### 4.3 Regression & Prediction Drift Analysis
All outputs compared field-by-field between pre-refactor baseline snapshots (`ml_baseline_snapshot.json`) and post-refactor executions:

| Target Value | Baseline | Post-Refactor | Drift | Status |
| :--- | :--- | :--- | :--- | :--- |
| `single.ml_score` | `3.564574581105262e-05` | `3.564574581105262e-05` | `0.0` | ✅ Identical |
| `single.shap_keys` | `['F3898', 'F2230', 'F3908']` | `['F3898', 'F2230', 'F3908']` | `None` | ✅ Identical |
| `single.shap_vals` | `[-7.309, -7.107, -1.445]` | `[-7.309, -7.107, -1.445]` | `0.0` | ✅ Identical |
| `batch[0].ml_score` | `0.000079` | `0.000079` | `0.0` | ✅ Identical |
| `acc9.ml_score` | `0.000015` | `0.000015` | `0.0` | ✅ Identical |
| `acc9002.ml_score` | `0.000013` | `0.000013` | `0.0` | ✅ Identical |

---

## 5. Stability & Hardening Audits

### 5.1 Warning Resolutions
1. **DataFrame Fragmentation:** Resolved standard pandas fragmentation warnings inside `predictor.py` during column alignment. Instead of inserting missing dataset columns one-by-one in a loop, columns are accumulated in a dictionary and merged all-at-once via a single `pd.concat` call.
2. **Deprecation Warnings:** Replaced deprecated `datetime.utcnow()` instances across all backend modules with timezone-naive UTC conversions where database schemas required it, or timezone-aware `datetime.now(timezone.utc)` for application logic.
3. **Streamlit Layout Deprecations:** Updated Streamlit components. Replaced the deprecated `use_container_width` keyword argument in chart rendering and container blocks with modern properties to prevent crashes on post-2025 library versions.

### 5.2 Crash Mitigation
1. **PyVis Exception Guarding:** Addressed potential tracebacks in [graph_view.py](file:///d:/Projects/FundTrace-AI/frontend/components/graph_view.py) when constructing NetworkX and PyVis network visuals. Added checking to ensure nodes exist before invoking `net.add_edge()`, preventing `AssertionError` crashes.
2. **Temporary File Leakage:** Fixed disk leak inside PyVis rendering. Wrapped temporary HTML generation in a try-finally block. The temporary HTML file is read, and `os.unlink()` is immediately executed in the `finally` block to prevent accumulating temp files on disk.
3. **Database Resource Leaks:** Fixed `ResourceWarning: unclosed BoltDriver` inside `graph_service.py` and unit tests. Guaranteed driver socket closure inside `verify_connectivity()` and routing exception blocks.
