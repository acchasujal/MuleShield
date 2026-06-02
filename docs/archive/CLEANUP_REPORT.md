# Cleanup Report — MuleShield AI

This report documents the repository cleanup process to remove dev-specific scripts, test databases, regression outputs, and compiler caches to optimize package size and portability.

## Safely Removed Files

The following files have been deleted from the repository root:

### Benchmark & Regression Outputs
- `capture_baseline.py` (Non-production float verification benchmarks)
- `regression_after.txt` (Non-production regression performance text logs)
- `db_test_output.txt` (Temporary PostgreSQL diagnostic outputs)
- `proof_output.txt` (Local Centrality execution validation text logs)
- `proof_results.txt` (Local GDS query test results)
- `GRAPH_RUNTIME_PROOF.json` (Local runtime speed diagnostics)
- `RUNTIME_PROOF_DATA.json` (Local runtime speed diagnostics)

### Developer/Local Validation Scripts
- `test_database_recovery.py` (Local DB transaction recovery script)
- `execute_direct_proof.py` (Local Neo4j Centrality calculation verification)
- `execute_runtime_proof.py` (Local Neo4j Centrality calculation verification)
- `proof_exec.py` (Local Neo4j Centrality calculation verification)
- `proof_with_centrality.py` (Local Neo4j Centrality calculation verification)
- `runtime_proof.ps1` (Local PowerShell latency verification benchmarks)
- `runtime_proof.py` (Local Python latency verification benchmarks)
- `simple_graph_validation.py` (Local database socket testing harness)
- `validate_graph_intelligence.py` (Local database socket testing harness)

### Cache and Scratch files
- `query` (Scratch file containing standard database keywords)
- `recovery_test.json` (Temporary verification data payload)

### Redundant Plans & Logs
- `CONSISTENCY_FIX_PLAN.md` (Legacy modularization resolution design template)
- `FAILURE_REPORT.md` (Legacy modularization execution crash traces)
- `FIX_ORDER.md` (Legacy dev sprint tasks tracking)

---

## Retained Critical Assets

All production code and assets have been strictly preserved:
- **Tabular Datasets**: `data/boi/DataSet.csv` remains untouched to support features queries.
- **Demo Scenarios**: `data/scenario_*.csv` and `data/fallback_*.json` remain intact for demo-mode sandbox execution.
- **Trained ML Models**: `backend/ml_artifacts/*` (including final_model.pkl, final_metadata.json, cat_mappings.json, feature_importances.csv, and imputer_full.pkl) are fully preserved.
- **Core Architectures**: All modules under `backend/` and `frontend/` remain fully intact.
