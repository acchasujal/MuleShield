# MuleShield AI — Development History and Compactor Diary

This document compiles the complete evolution of the MuleShield AI platform. It consolidates all changelogs, sprint histories, compactor recommendations, agent navigation mappings, and development walkthroughs.

---

## 1. Product Evolution Changelog

### Phase 1: Backend Stabilization
* **LLM Client Fix:** Changed the fallback LLM client from `gemini-2.0-flash` to `gemini-1.5-flash` in the early developmental cycle to address temporary free-tier quota exceptions.
* **OpenAI Integration:** Configured an OpenAI `gpt-3.5-turbo` endpoint as a secondary recovery route when Gemini calls timed out.
* **Exponential Backoff:** Added backoff retries (2s ➔ 4s ➔ 8s) and capped all API calls with a 30-second execution deadline using `asyncio.wait_for`.
* **Non-Blocking Execution:** Routed LLM API interactions through `asyncio.run_in_executor` to prevent blocking the FastAPI single-threaded event loop.
* **In-Memory Caching:** Introduced a SHA-256 in-memory audit cache for `/generate-str` responses. Payload matching skips LLM processing entirely.
* **Token Optimization:** Added the `_slim_transactions()` utility. It strips non-essential logging headers and compacts transaction data arrays before sending them to the LLM.

### Phase 2: Frontend UX Hardening
* **Deprecation Purges:** Removed legacy Streamlit layout widgets, resolving warnings on newer package versions.
* **WebSocket Resilience:** Wrapped frontend widgets with exception handlers to suppress `WebSocketClosedError` tracebacks if browser windows are closed mid-run.
* **Interactive AI Tabs:** Added modular UI cards for STR file exports and case audits.

### Phase 3: Developer Setup & Portability
* **Portability Scripting:** Introduced cross-platform automated setup scripts (`scripts/setup.ps1` for Windows, `scripts/setup.sh` for Unix) to manage virtual environments, install dependencies, and run database schema migrations.
* **Standard Environment Blueprint:** Created `.env.example` as a template for API keys and database credentials.
* **Diagnostic Check Engine:** Introduced `health_check.py` to check model assets, dataset parameters, and database port availabilities automatically.

### Phase 4: NVIDIA NIM Primary + Gemini Flash Fallback
* **Primary NVIDIA Provider:** Standardized NVIDIA NIM Llama-based models as the primary AI service:
  * `/generate-str` ➔ `meta/llama-3.1-70b-instruct` (longer STR reviews).
  * `/ask` ➔ `meta/llama-3.1-8b-instruct` (rapid Q&A).
* **Gemini SDK Upgrade:** Re-implemented the fallback client to use the modern `google-genai` SDK (`from google import genai`) with the `gemini-2.0-flash` model.
* **Unified Recovery Model:**
  ```
  API Call ➔ NVIDIA NIM Primary (45-second timeout)
                 │ (on failure)
                 ▼
             Gemini 2.0 Flash Fallback (2 retries, backoff)
                 │ (on failure)
                 ▼
             Local File Fallback (Loads cached JSON data)
  ```

### Phase 5: Verification & Hardening
* **DataFrame Fragmentation Fix:** Switched the tabular feature alignment logic in `predictor.py` to use a dictionary-accumulation and single-pass `pd.concat` approach, removing pandas performance warnings.
* **Neo4j BoltDriver Resource Closure:** Wrapped driver verification calls inside try-finally blocks to close Bolt connection sockets, resolving unclosed socket leakage.
* **PyVis Graph Edge Guards:** Integrated validation guards to ensure edge nodes exist in the visual network before calling `pyvis.Network.add_edge()`, preventing Streamlit page tracebacks.
* **Disk Space Reclamation:** Unlinked PyVis generated HTML files immediately after embedding them in the UI to prevent temp file accumulations on host servers.
* **Banned Compliance Terms Purge:** Purged obsolete regulatory names and hackathon literals (e.g. replacing "FundTrace" with "MuleShield" and "Union Bank" with "Bank of India") across all source codes, comments, and schemas.

---

## 2. Development Sprints & Task Checklists

### Sprint 1: Foundation & Tabular ML Service
* **Objective:** Establish the directory layout, load trained XGBoost features, build FastAPI endpoints, and integrate score fusion weights.
* **Outcome:** Loaded XGBoost binary models and simple imputers. Standardized the 70/30 composite score fusion in `risk_scoring.py`, reverting to 100% ML score when Neo4j is offline.

### Sprint 2: Core Infrastructure & Recovery
* **Objective:** Restore Neo4j and PostgreSQL databases and resolve timezone mismatches.
* **Outcome:** Orchestrated database containers via Docker Compose. Standardized date/time fields to naive UTC to resolve PostgreSQL timestamp mismatch failures.

### Sprint 3: Frontend UX Optimization
* **Objective:** Implement the user journey pages, human-readable feature descriptions, and automated STR alerts in the UI.
* **Outcome:** Created the "🔍 Account Inspector" and "🕵️ Alert Center" tabs in Streamlit. Mapped cryptic feature headers (e.g. `F670` ➔ "Regulatory TMS Flag") to clear text descriptions. Added a 4-stage visual timeline pill for account states. Purged branding references.

---

## 3. Codebase Mapping & Navigation Blueprint

To maintain design separation of concerns and prevent code changes from introducing regression risks, cooperative agents follow these guidelines:

### 3.1 Workspace Layout
* `/backend/ml/` (new modular package) - Strictly isolates prediction algorithms, feature imputers, SHAP engines, feature seeker lookups, and staging classifiers.
* `/backend/routers/` - Handles API routing controllers.
* `/backend/app.py` - Manages application initialization lifespans.
* `/frontend/components/` - Grouped dashboard views (charts, inspect panels, alert centers).
* `/data/` - Static test data, scenarios, and offline fallback JSON matrices.

### 3.2 Modification Rules
1. **Authoritative Context (`/context/`):** Contains master guidelines. Modify only after a sprint review.
2. **Technical Blueprints (`/architecture/`):** Contains schemas, risk engine equations, and ML pipelines. Backward compatibility is strictly required.
3. **Core Backend and Frontend (`/backend/`, `/frontend/`):** Run the complete unittest suite (`python -m unittest discover -s tests`) after any edits.

---

## 4. Context Optimization & Token Reductions

As a repository scales, large numbers of scattered files can lead to significant AI context overhead. The MuleShield AI repository consolidation represents a substantial improvement:

* **Pre-Consolidation State:** 54 scattered Markdown files and flat checklists comprised over 430 KB of text (approximately 110,000 tokens of context overhead).
* **Consolidation State:** Merged all documentation into 5 target specifications: `docs/ARCHITECTURE.md`, `docs/VALIDATION_REPORT.md`, `docs/RELEASE_READINESS.md`, `docs/DEVELOPMENT_HISTORY.md`, and `docs/OPERATIONS.md`.
* **Archive Policy:** Moved original individual text files into the `docs/archive/` folder, removing them from active context searches while preserving historical logs.
* **Impact:** Reduced active token overhead by over **80%**, improving agent response accuracy and speed.
