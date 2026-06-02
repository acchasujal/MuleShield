# CRASH AUDIT — MuleShield AI

This document audits all known and potential runtime crash risks, unhandled exceptions, and resource leakages within the MuleShield AI application.

## 1. PyVis Graph Rendering Failures & AssertionErrors
- **Risk**: `AssertionError` in `pyvis.Network.add_edge`
- **Location**: [graph_view.py](file:///d:/Projects/FundTrace-AI/frontend/components/graph_view.py)
- **Root Cause**:
  1. PyVis throws an `AssertionError` when adding an edge between nodes where one or both nodes are missing from the network.
  2. If the Neo4j database returns records where `from_id` or `to_id` are empty/null, the code adds them to the graph as `None` or skip adding them, causing `AssertionError` when adding the edge.
  3. No validation is done to ensure the edge endpoints exist before calling `net.add_edge`.
- **Impact**: Streamlit page crashes with an uncaught traceback, breaking the Account Inspector graph visualization view.

---

## 2. PyVis Temporary HTML File Leak
- **Risk**: Host disk space exhaustion
- **Location**: [graph_view.py](file:///d:/Projects/FundTrace-AI/frontend/components/graph_view.py)
- **Root Cause**:
  1. The function `render_pyvis_network` creates a temporary file using `tempfile.NamedTemporaryFile(delete=False, suffix=".html")` to write the network HTML.
  2. The file is never deleted after the contents are read and embedded via `components.html`.
- **Impact**: Leaves behind temporary files on disk on every single visualization render, causing eventual disk space exhaustion on active servers.

---

## 3. Uncaught PyVis Rendering Exceptions
- **Risk**: Complete page crash on third-party library failures
- **Location**: [graph_view.py](file:///d:/Projects/FundTrace-AI/frontend/components/graph_view.py)
- **Root Cause**:
  1. The PyVis configuration and HTML generation block runs outside of any try-except block.
  2. If PyVis, NetworkX, or system temp file creation fails for any reason, the exception propagates unchecked.
- **Impact**: Displays raw tracebacks to end users and crashes the active view tab.

---

## 4. Unhandled Database Connection & Startup Failures
- **Risk**: Startup loop crashes
- **Location**: [app.py](file:///d:/Projects/FundTrace-AI/backend/app.py) / [database.py](file:///d:/Projects/FundTrace-AI/backend/database.py)
- **Root Cause**:
  1. Database initializations are executed during application startup. If PostgreSQL is offline, `init_db()` catches the exception and returns `False` gracefully.
  2. If Neo4j is offline, `Neo4jService` catches the connection error and reverts to Standalone ML mode.
- **Status**: **Mitigated**. The fallback mechanisms are implemented, but resource cleanup in error paths (such as closing the Bolt connection pool after a verification failure) requires optimization to prevent subsequent warnings.
