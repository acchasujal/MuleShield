# Dependency Audit — MuleShield AI

This document audits all dependencies registered in `requirements.txt` to verify their usage and eliminate unused third-party overhead.

## Production Dependencies

The following packages are confirmed as **required** and remain in `requirements.txt`:

| Package | Used In | Purpose | Status |
| :--- | :--- | :--- | :--- |
| `fastapi` | `backend/app.py`, `backend/routers/*` | Web API application gateway | **REQUIRED** |
| `uvicorn` | Startup orchestration | ASGI application server | **REQUIRED** |
| `pandas` | Throughout ML and data parsing | DataFrames, feature lookup, structured scenarios | **REQUIRED** |
| `networkx` | `backend/fraud_detection.py`, `backend/graph_builder.py` | Standalone Graph network heuristics (cycles, layering) | **REQUIRED** |
| `streamlit` | `frontend/app.py`, `frontend/components/*` | Developer and landing UI dashboards | **REQUIRED** |
| `scikit-learn` | `backend/fraud_detection.py`, `scripts/train_model.py` | IsolationForest anomaly detection, preprocessing | **REQUIRED** |
| `python-multipart` | `backend/routers/ml_predict.py`, `backend/routers/analyze.py` | Parses uploaded file multipart requests | **REQUIRED** |
| `pyvis` | `frontend/components/graph_view.py` | Generates interactive D3-based HTML networks | **REQUIRED** |
| `reportlab` | `frontend/components/compliance_panel.py` | Compiles suspicous transaction report PDF exports | **REQUIRED** |
| `google-genai` | `backend/ai_service.py` | Client connection to Gemini fallback API | **REQUIRED** |
| `python-dotenv` | Throughout application | Bootstraps credentials from local `.env` | **REQUIRED** |
| `openai` | `backend/ai_service.py` | Connects to NVIDIA NIM Llama endpoints | **REQUIRED** |
| `xgboost` | `backend/ml/predictor.py` | Standalone machine learning classifier | **REQUIRED** |
| `imbalanced-learn`| `scripts/train_model.py` | SMOTE synthetic oversampling algorithms | **REQUIRED** |
| `shap` | `backend/ml/predictor.py`, `backend/ml/shap_engine.py` | TreeExplainer explainable AI calculations | **REQUIRED** |
| `neo4j` | `backend/graph_service.py`, `frontend/components/graph_view.py` | Connection to on-premise Neo4j database | **REQUIRED** |
| `asyncpg` | `backend/database.py` | High-speed async client for PostgreSQL database | **REQUIRED** |
| `sqlalchemy` | `backend/database.py` | Declarative Base and Session database ORM | **REQUIRED** |
| `plotly` | `frontend/components/charts.py`, `frontend/components/alert_center.py` | Renders analytics charts | **REQUIRED** |

---

## Removed Dependencies

The following packages were identified as **unused** and have been purged from `requirements.txt`:

1. **`matplotlib`**:
   - **Reason**: Visual analytics are rendered interactively in Streamlit via Plotly and PyVis. `matplotlib` was never imported in any source files, representing dead dependency baggage.
