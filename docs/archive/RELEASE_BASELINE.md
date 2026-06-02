# Release Baseline

Date: 2026-06-02
Phase: 0 - Baseline Snapshot
Scope: Read-only audit of the current codebase and runtime behavior before any release-readiness changes.

## Summary

MuleShield AI is currently runnable in standalone mode with local ML artifacts loaded and both AI providers reporting ready. The backend API responds for `/`, `/health`, `/predict/single`, and `/analyze` under local test execution. Neo4j and PostgreSQL are both offline in the present environment and the application falls back to ML-only and offline audit behavior as designed.

## File Structure

Top-level snapshot:

- `backend/`
- `frontend/`
- `data/`
- `architecture/`
- `context/`
- `docs/`
- `scripts/`
- `tasks/`
- `sprints/`
- `prompts/`
- `lib/`
- `run_tests.py`
- `run_tests2.py`
- `requirements.txt`
- `README.md`

Key backend modules:

- `backend/app.py`
- `backend/ml_service.py`
- `backend/risk_scoring.py`
- `backend/graph_service.py`
- `backend/database.py`
- `backend/routers/ml_predict.py`
- `backend/routers/i4c_webhook.py`

Key frontend modules:

- `frontend/app.py`
- `frontend/components/`
- `frontend/services/`
- `frontend/utils/`

Key data assets:

- `data/boi/DataSet.csv`
- `data/scenario_roundtrip.csv`
- `data/scenario_structuring.csv`
- `data/scenario_dormant.csv`
- `data/fallback_*`

## Startup Status

Observed through `fastapi.testclient.TestClient` lifespan startup:

- FastAPI app startup: `WORKING`
- ML service initialization: `WORKING`
- Graph service initialization: `DEGRADED`
- Database initialization: `DEGRADED`
- App shutdown: `WORKING`

Evidence:

- Lifespan boot completed and served requests successfully.
- No startup crash occurred despite database dependencies being unavailable.

## API Status

Observed through local API calls:

- `GET /`: `200 OK`
- `GET /health`: `200 OK`
- `POST /predict/single`: `200 OK`
- `POST /analyze`: `200 OK`

Returned API metadata:

- API title: `MuleShield AI API Gateway`
- Version: `3.0`
- Health status: `ok`
- NVIDIA status: `ready`
- Gemini status: `ready`

## Model Status

Observed from `MLService` and test execution:

- Artifact loading: `WORKING`
- SHAP explainer initialization: `WORKING`
- Single prediction: `WORKING`
- Batch prediction: `WORKING`

Artifacts present:

- `backend/ml_artifacts/final_model.pkl`
- `backend/ml_artifacts/imputer_full.pkl`
- `backend/ml_artifacts/final_metadata.json`
- `backend/ml_artifacts/cat_mappings.json`
- `backend/ml_artifacts/feature_importances.csv`

Validation notes:

- `run_tests.py` confirmed single prediction, SHAP output, and XML generation.
- `run_tests2.py` confirmed batch prediction and module imports.

## Neo4j Status

Current status: `OFFLINE`

Observed connection target:

- `bolt://localhost:7687`

Observed failure:

- Connection refused on both IPv6 and IPv4 localhost.

Current behavior:

- App falls back to standalone ML mode.
- Graph scoring defaults to ML-derived fallback when centrality is unavailable.

## PostgreSQL Status

Current status: `OFFLINE`

Observed connection target:

- `postgresql+asyncpg://postgres:postgres@localhost:5432/muleshield`

Observed failure:

- Remote computer refused the network connection during schema initialization.

Current behavior:

- App falls back to offline log behavior.
- No startup crash occurs when the database is unavailable.

## Current Alerts Distribution

### Dataset Baseline

Source: `data/boi/DataSet.csv`

- Total accounts scored: `9082`
- Total non-low alerts: `81`
- Total low-risk accounts: `9001`

### Round-Trip Scenario Baseline

Source: `data/scenario_roundtrip.csv`

- Total analyzed accounts in graph: `6`
- Total `MEDIUM+` alerts: `1`
- Alert leader: `ACC05200000000009` at `40.0`

## Current Severity Distribution

### Dataset Baseline

- `LOW`: `9001`
- `MEDIUM`: `0`
- `HIGH`: `81`
- `CRITICAL`: `0`

### Round-Trip Scenario

- `LOW`: `5`
- `MEDIUM`: `1`
- `HIGH`: `0`
- `CRITICAL`: `0`

## Current Mule-Stage Distribution

### Dataset Baseline

- `LEGITIMATE`: `9001`
- `ACTIVE_MULE`: `81`

### Round-Trip Scenario

- `LEGITIMATE`: `6`

## Reference Account Check

Account: `ACC05200000000009`

Baseline `/predict/single` result:

- Composite score: `0.1`
- Severity: `LOW`
- Mule stage: `LEGITIMATE`
- Profile risk: `0.08`
- Transaction risk: `0.0`
- Graph risk: `0.08`

Round-trip `/analyze` result:

- Composite score: `40.0`
- Severity: `MEDIUM`
- Mule stage: `LEGITIMATE`

Observation:

- The fusion scoring change is active for `/analyze`.
- Mule-stage logic does not currently promote the round-trip scenario accounts out of `LEGITIMATE`.

## Test Results

### `run_tests.py`

Status: `PASS`

Verified:

- Single prediction + SHAP
- Risk fusion function
- Dataset readability
- goAML XML generation
- Neo4j offline fallback behavior
- PostgreSQL offline fallback behavior

Warnings observed:

- `PerformanceWarning` in `backend/ml_service.py` during repeated DataFrame column insertion

### `run_tests2.py`

Status: `PASS`

Verified:

- Batch prediction
- Fallback JSON presence
- Scenario CSV presence
- Requirements file presence
- Backend module importability

## Baseline Risks Observed

- Neo4j is unavailable, so graph enrichment is not actually online.
- PostgreSQL is unavailable, so audit persistence is not actually online.
- Dataset-wide severity distribution has no `MEDIUM` or `CRITICAL` classifications in baseline scoring.
- Round-trip scenario lifts one account to `MEDIUM`, but mule-stage classification remains `LEGITIMATE`.
- `backend/ml_service.py` emits repeated pandas fragmentation warnings during preprocessing.

## Files Modified In Phase 0

- `RELEASE_BASELINE.md`

## Validation Outcome

Phase 0 completed successfully.

- Audit completed
- Validation scripts executed
- Baseline report created
- No application code changed during this phase

Stop point:

- Await approval before beginning Phase 1 - Dataset-Wide Fusion Validation.
