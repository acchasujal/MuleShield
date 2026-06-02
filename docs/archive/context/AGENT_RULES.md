# AGENT_RULES.md
_Load at the start of every coding session. Non-negotiable, strict system boundaries. ~500 tokens._

---

## 🏷️ IDENTITY INVARIANTS

1.  **Product Name:** Always **MuleShield AI** — never "FundTrace AI" or "FundTrace" in new code, strings, logs, or UI titles.
2.  **Organization:** Always **Bank of India** (or BOI) — never "Union Bank", "Union Bank of India", or "UBI".
3.  **Problem Domain:** Always **mule account detection and network classification** — never "fraud detection" generically.
4.  **UI Terminology:** Use **"mule account"** or **"flagged entity"** in all customer-facing text, tables, and buttons — never "suspicious account", "fraud account", or "scam profile" unless quoting regulatory criteria.

---

## 🏗️ ARCHITECTURAL BOUNDARIES

1.  **Composite Risk scoring:** The composite score must be calculated *exclusively* via `calculate_composite_risk(ml_score, graph_score)` located in `backend/risk_scoring.py`. **Never duplicate or inline this formula** inside routers, service files, or frontend scripts.
2.  **lifespan ML Loading:** Load ML model artifacts *only once* via the FastAPI `lifespan` event handler at application startup (saved in `app.state`). **Never load the pickle files** inside an endpoint, background task, or per-request wrapper.
3.  **Feature Invariance:** The feature lists are locked and immutable after Phase 1. The selected 122 features must match exactly those specified in `final_metadata.json`. Do not dynamically add, remove, or modify columns.
4.  **F3912 Model Ban:** Under no circumstances should feature **F3912** be present in the training datasets or feature lists inside `final_metadata.json`. It is a strict data leakage risk. It is reserved exclusively for post-inference *Mule Lifecycle Staging* in Python and UI rendering.
5.  **Strict Endpoint Contract:** The endpoint `/predict/batch` must take the raw, unaltered `DataSet.csv` containing columns `F1...F3924` and a numeric index. Do not rename the columns on the server.
6.  **Categorical Safety:** Categorical transformations must use the fitted mappings loaded from `cat_mappings.json`. Never fit a new `LabelEncoder` at inference time. If a new category is seen at runtime, default the mapping safely to `0` instead of crashing.

---

## 💻 CODING STANDARDS

### Python (FastAPI & ML Engineering)
*   **Asynchronous Execution:** All API endpoints must be defined using `async def`, and all database accesses (Neo4j Bolt, PostgreSQL, Redis) must be fully `await`ed.
*   **Strict Type-Hinting:** Every single function signature must include complete type hints for inputs and returns.
*   **Pydantic v2 Models:** All API requests and response schemas must be structured via Pydantic v2 models.
*   **Exception Isolation:** Never let ML inference failures crash the server. Catch exceptions cleanly, log them with traceback, and return a safe default: `{ "error": "...", "risk_score": 50.0, "tier": "MEDIUM" }`.
*   **Imports Order:** Group imports alphabetically: Standard libraries $\rightarrow$ Third-party packages $\rightarrow$ Local modules.
*   **Logging Principle:** No `print` statements allowed. Use `logging.getLogger(__name__)` to produce proper formatted logging outputs.

### React (Frontend Engineering)
*   **Modern React:** Functional components only, utilizing modern hooks (`useState`, `useEffect`, `useMemo`).
*   **Validation:** Use `PropTypes` or TypeScript schemas on all components receiving props to catch contract issues early.
*   **Fault Tolerance:** Wrap all components dependent on ML services (such as `SignalCard` or `RiskTable`) in React Error Boundaries to prevent a single API failure from rendering a blank page.
*   **No Mocks in Prod:** Never hardcode risk values or alert structures inside components; always request them via API.
*   **Micro-Animations & Aesthetics:** Implement highly responsive UI states, CSS loading spinners, micro-transitions, and custom CSS glassmorphism.
*   **Environment Configuration:** Fetch all API routes and connection strings from environment variables (`.env`). Never hardcode `localhost:8000` or database ports.

---

## 🔗 INTEGRATION REQUIREMENTS

*   **Concurrency:** Use `asyncio.gather()` to fetch tabular ML scores and graph database metrics in parallel, optimizing response latency.
*   **STR Trigger Threshold:** Automatically trigger goAML XML STR generator only when `tier == "CRITICAL"` (composite score $\geq 80$). Never generate for HIGH, MEDIUM, or LOW profiles.
*   **SHAP Inference Bounds:** Execute full SHAP tree explainers strictly on `/predict/single`. For `/predict/batch`, bypass runtime SHAP calculation (too slow for 9,082 rows) and return top-5 features from the pre-computed `feature_importances.csv`.
*   **Webhooks:** The government MHA I4C alert webhook `/ingest-i4c` must parse the `account_no`, call `/predict/single` internally, and write audit logs to PostgreSQL in a single transactional loop.

---

## 🚫 ANTI-PATTERNS (Never Do These)

*   ❌ **Reporting Accuracy:** Reporting classification accuracy as a valid model success indicator on imbalanced datasets.
*   ❌ **Leakage:** Incorporating F3912 in training datasets.
*   ❌ **Inline Math:** Writing custom risk score math outside of `risk_scoring.py`.
*   ❌ **Hardcoded UI Messages:** Hardcoding feature significance strings in the frontend (use the translation service).
*   ❌ **In-Endpoint Loading:** Initializing ML models inside FastAPI routing endpoints.
*   ❌ **UBI References:** Committing files containing references to "Union Bank", "UBI", or Union Bank schemas.
*   ❌ **Raw fitting:** Fitting encoders, models, or transformers inside the web server container.
