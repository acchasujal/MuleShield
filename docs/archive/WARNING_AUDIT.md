# WARNING AUDIT — MuleShield AI

This document audits all compilation, import, startup, and runtime warnings detected within the MuleShield AI application.

## 1. Syntax & Compilation Warnings
- **Status**: **Clean**
- **Details**: Re-compiled all Python source files in the `backend/` and `frontend/` folders using `compileall` under warnings-as-errors mode. No syntax warnings or syntax errors were detected.

---

## 2. Deprecation Warnings
### Streamlit `use_container_width` Deprecation
- **Warning**: `Please replace use_container_width with width. use_container_width will be removed after 2025-12-31. For use_container_width=True, use width='stretch'.`
- **Location**: Multiple visual components in the frontend:
  - [charts.py](file:///d:/Projects/FundTrace-AI/frontend/components/charts.py) (Lines 24, 43, 63, 80)
  - [alert_center.py](file:///d:/Projects/FundTrace-AI/frontend/components/alert_center.py) (Lines 128, 213)
  - [account_inspector.py](file:///d:/Projects/FundTrace-AI/frontend/components/account_inspector.py) (Line 187)
  - [demo_mode.py](file:///d:/Projects/FundTrace-AI/frontend/components/demo_mode.py) (Line 169)
- **Impact**: Will crash on Streamlit versions released after 2025-12-31.

### Banned `datetime.utcnow()` Usage
- **Warning**: `DeprecationWarning: datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware datetime.now(timezone.utc) instead.`
- **Location**:
  - [ml_predict.py](file:///d:/Projects/FundTrace-AI/backend/routers/ml_predict.py) (Lines 136, 344)
  - [i4c_webhook.py](file:///d:/Projects/FundTrace-AI/backend/routers/i4c_webhook.py) (Lines 88, 100, 123)
- **Impact**: Deprecated standard API call. Triggers failures in hackathon/compliance word audits.

---

## 3. Runtime & Resource Warnings
### DataFrame Fragmentation
- **Warning**: `PerformanceWarning: DataFrame is highly fragmented. This is usually the result of calling frame.insert many times, which has poor performance. Consider joining all columns at once using pd.concat(axis=1) instead.`
- **Location**: [predictor.py](file:///d:/Projects/FundTrace-AI/backend/ml/predictor.py) (Line 140) inside `_preprocess_features`.
- **Impact**: Heavy performance overhead during batch predictions due to incremental DataFrame insertion of 100+ columns one-by-one in a loop.

### Unclosed Neo4j BoltDriver Resource
- **Warning**: `ResourceWarning: unclosed BoltDriver: <neo4j._sync.driver.BoltDriver object at 0x...>`
- **Location**:
  - `run_tests.py` (instantiates `Neo4jService` but never closes it).
  - [graph_service.py](file:///d:/Projects/FundTrace-AI/backend/graph_service.py) (fails to close driver inside exception block when `verify_connectivity()` fails).
  - [graph_view.py](file:///d:/Projects/FundTrace-AI/frontend/components/graph_view.py) (exceptions during queries bypass `driver.close()`).
- **Impact**: Socket descriptor leaks, resource exhaustion under continuous usage.
