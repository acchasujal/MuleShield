# Repository Audit — MuleShield AI

This document audits and classifies all files in the MuleShield AI repository to ensure reproducibility, clean code practices, and open-source readiness.

| File / Folder | Purpose | Classification | Reason |
| :--- | :--- | :--- | :--- |
| `backend/` | Monolithic FastAPI gateway and logic | **KEEP** | Core backend application. |
| `frontend/` | Streamlit interactive UI application | **KEEP** | Core frontend user interface. |
| `data/` | CSV datasets and pre-generated JSON fallbacks | **KEEP** | Necessary data directory for demo and feature lookups. |
| `lib/` | Frontend static JS/CSS library dependencies | **KEEP** | Embedded UI library dependencies. |
| `docs/` | Project documentations | **KEEP** | Helpful onboarding context. |
| `scripts/` | Tooling and setup automation files | **KEEP** | Setup and initialization files. |
| `sprints/` | Development history | **KEEP** | Development sprint tracking. |
| `tasks/` | Development checklists | **KEEP** | Development task records. |
| `docker-compose.yml` | Container specification for Postgres/Neo4j | **KEEP** | Enables portable one-click service startup. |
| `requirements.txt` | Core package dependencies list | **KEEP** | Essential for pip installation. |
| `run_tests.py` | Single prediction and connection test runner | **KEEP** | Primary validation test suite. |
| `run_tests2.py` | Batch prediction and module import test runner | **KEEP** | Secondary validation test suite. |
| `check_audit.py` | Compliance and syntax checks | **KEEP** | Integrity verification script. |
| `generate_synthetic_data.py` | Script to generate synthetic alert datasets | **KEEP** | Essential dev utility to populate scenario CSVs. |
| `README.md` | General landing documentation | **KEEP** | Setup instructions (to be rebuilt). |
| `WORKSPACE_RULES.md` | Workspace instruction rules | **KEEP** | Guidelines for developer workspace. |
| `SYSTEM_INVENTORY.md` | Audit inventory list of MuleShield | **KEEP** | Compliance documentation. |
| `TEST_MATRIX.md` | Audit and coverage test list | **KEEP** | Compliance documentation. |
| `SOURCE_OF_TRUTH_AUDIT.md` | Data lineage source of truth audit | **KEEP** | Compliance documentation. |
| `ML_ARCHITECTURE_BASELINE.md`| Modular ML architecture description baseline | **KEEP** | Compliance documentation. |
| `ML_MODULARIZATION_REPORT.md`| Final modular ML conversion details | **KEEP** | Compliance documentation. |
| `BACKEND_MODULARIZATION_REPORT.md` | Final modular backend conversion details | **KEEP** | Compliance documentation. |
| `LIFECYCLE_DECISION_MATRIX.md` | State transition stage matrix specs | **KEEP** | Compliance documentation. |
| `LIFECYCLE_ALIGNMENT_REPORT.md` | Stage transition rules alignment verification | **KEEP** | Compliance documentation. |
| `GRAPH_INTELLIGENCE_VALIDATION.md` | Neo4j GDS topological proof details | **KEEP** | Compliance documentation. |
| `GRAPH_RUNTIME_PROOF.md` | Centrality calculation runtime speed evidence | **KEEP** | Compliance documentation. |
| `FUSION_VALIDATION_REPORT.md` | Score fusion v5 verification metrics | **KEEP** | Compliance documentation. |
| `DATABASE_RECOVERY_REPORT.md` | PostgreSQL fallback Recovery verification | **KEEP** | Compliance documentation. |
| `DEMO_MODE_ROOT_CAUSE.md` | Analysis of sandbox demo mode bugs | **KEEP** | Compliance documentation. |
| `CONTEXT_COMPRESSION_REPORT.md` | Analysis of context compaction audits | **KEEP** | Compliance documentation. |
| `CHANGELOG.md` | Changelog logs of the project | **KEEP** | Development tracking. |
| `CODEBASE_MAP.md` | Code structure map | **KEEP** | Onboarding documentation. |
| `AGENT_LOADING_MATRIX.md` | compactor logs | **KEEP** | Compliance documentation. |
| `FINAL_RECOMMENDATIONS.md` | compactor logs | **KEEP** | Compliance documentation. |
| `RELEASE_BASELINE.md` | Release version baseline snapshots | **KEEP** | Compliance documentation. |
| `END_TO_END_TEST_MATRIX.md` | End-to-end user path validation matrix | **KEEP** | Compliance documentation. |
| `.gitignore` | Ignored files specification | **KEEP** | Excludes temp files from git index (to be rebuilt). |
| `capture_baseline.py` | Developer benchmark test script | **REMOVE** | Non-production baseline script. |
| `regression_after.txt` | Developer regression benchmarks | **REMOVE** | Non-production text dump. |
| `db_test_output.txt` | Developer PostgreSQL log dump | **REMOVE** | Non-production text dump. |
| `proof_output.txt` | Developer centrality proof dump | **REMOVE** | Non-production text dump. |
| `proof_results.txt` | Developer GDS verification logs | **REMOVE** | Non-production text dump. |
| `recovery_test.json` | Developer test recovery dataset | **REMOVE** | Non-production JSON test payload. |
| `test_database_recovery.py` | Developer postgres recovery script | **REMOVE** | Non-production recovery test. |
| `execute_direct_proof.py` | Developer GDS validation test | **REMOVE** | Non-production validation test. |
| `execute_runtime_proof.py` | Developer GDS validation test | **REMOVE** | Non-production validation test. |
| `proof_exec.py` | Developer GDS validation test | **REMOVE** | Non-production validation test. |
| `proof_with_centrality.py` | Developer GDS validation test | **REMOVE** | Non-production validation test. |
| `runtime_proof.ps1` | Developer runtime speed test | **REMOVE** | Non-production verification script. |
| `runtime_proof.py` | Developer runtime speed test | **REMOVE** | Non-production verification script. |
| `simple_graph_validation.py` | Developer graph connection test | **REMOVE** | Non-production verification script. |
| `validate_graph_intelligence.py` | Developer graph connection test | **REMOVE** | Non-production verification script. |
| `query` | Scratch file | **REMOVE** | Non-production scratch file. |
| `GRAPH_RUNTIME_PROOF.json` | Developer speed benchmarks output | **REMOVE** | Non-production JSON test output. |
| `RUNTIME_PROOF_DATA.json` | Developer speed benchmarks output | **REMOVE** | Non-production JSON test output. |
| `CONSISTENCY_FIX_PLAN.md` | Redundant plan | **REMOVE** | Non-production plan. |
| `FAILURE_REPORT.md` | Redundant failure report | **REMOVE** | Non-production report. |
| `FIX_ORDER.md` | Redundant checklist | **REMOVE** | Non-production checklist. |
| `.env` | Active configuration credentials | **CACHE** | Local active credentials. Excluded from git. |
| `.env.example` | Environmental blueprint template | **KEEP** | Example environment settings (to be created). |
