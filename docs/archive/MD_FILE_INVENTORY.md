# Markdown File Inventory — MuleShield AI

This document catalogs every Markdown (`.md`) file in the MuleShield AI repository, along with its size, purpose, current relevance, and consolidation strategy.

## Root Directory Markdown Files

| File | Size (Bytes) | Purpose | Relevance | Action |
| :--- | :--- | :--- | :--- | :--- |
| `AGENT_LOADING_MATRIX.md` | 15,433 | Compactor loading instructions | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `BACKEND_MODULARIZATION_REPORT.md`| 6,817 | Phase 3 Backend Modularization results | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `CHANGELOG.md` | 7,281 | Development history and logs | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `CLEANUP_REPORT.md` | 2,472 | Phase 6A repository cleanup details | Validation | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `CODEBASE_MAP.md` | 15,539 | Context reference structure map | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `CONTEXT_COMPRESSION_REPORT.md` | 13,590 | Compactor details and reports | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `CRASH_AUDIT.md` | 2,826 | Phase 5 crash vulnerabilities audit | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `DATABASE_RECOVERY_REPORT.md` | 11,654 | Postgres transaction recovery details | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `DEMO_MODE_ROOT_CAUSE.md` | 4,378 | Analysis of legacy sandbox demo bugs | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `DEPENDENCY_AUDIT.md` | 2,874 | requirements.txt audit details | Validation | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `END_TO_END_TEST_MATRIX.md` | 6,372 | Coverage test matrices | Validation | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `FINAL_RECOMMENDATIONS.md` | 18,941 | Compactor recommendations | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `FUSION_VALIDATION_REPORT.md` | 6,354 | Validation of risk score fusion algorithms | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `GITHUB_READINESS_REPORT.md` | 2,052 | GitHub checklist readiness verification | Validation | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `GRAPH_INTELLIGENCE_VALIDATION.md`| 22,583 | Neo4j GDS topological validation results | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `GRAPH_RUNTIME_PROOF.md` | 3,887 | Speed and latency benchmarks for GDS | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `LIFECYCLE_ALIGNMENT_REPORT.md` | 4,624 | Mule lifecycle rules mapping alignment | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `LIFECYCLE_DECISION_MATRIX.md` | 6,423 | Staging rules matrix | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `ML_ARCHITECTURE_BASELINE.md` | 8,653 | Baseline model loading descriptions | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `ML_MODULARIZATION_REPORT.md` | 10,323 | Modular ML structure details | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `PROJECT_ANALYSIS.md` | 30,509 | Compactor project reports | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `README.md` | 6,717 | Main project overview and setup | Current | **KEEP** (rebuilt in 6A, keep at root) |
| `RELEASE_BASELINE.md` | 5,882 | Baseline project snapshots | Release | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `RELEASE_PREP_REPORT.md` | 3,794 | Final Phase 6A release report | Release | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `REPOSITORY_AUDIT.md` | 6,533 | Audited list of repo files | Release | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `SOURCE_OF_TRUTH_AUDIT.md` | 8,596 | Standard banking data sources audits | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `SYSTEM_INVENTORY.md` | 7,099 | Inventory details | Release | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `TEST_MATRIX.md` | 8,153 | Test requirements list | Release | **Merge** to `RELEASE_READINESS.md` ➔ **Archive** |
| `WARNING_AUDIT.md` | 2,941 | Warnings and deprecations audit details | Validation | **Merge** to `VALIDATION_REPORT.md` ➔ **Archive** |
| `WORKSPACE_RULES.md` | 17,498 | Guidelines for developer workspace | Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |

---

## Subdirectory Markdown Files

| File | Size (Bytes) | Purpose | Relevance | Action |
| :--- | :--- | :--- | :--- | :--- |
| `architecture/API_CONTRACTS.md` | 4,631 | API paths and JSON contract schemas | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `architecture/DATABASE_SCHEMA.md`| 6,560 | Schema design configurations | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `architecture/DECISIONS.md` | 4,522 | Decision logs for GDS and ML layers | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `architecture/ML_PIPELINE.md` | 4,165 | ML training and dataset parameters | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `architecture/RISK_ENGINE.md` | 5,233 | Math algorithms and composite scoring | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `architecture/SYSTEM_ARCHITECTURE.md`| 8,480| Visual graph topologies | Architecture | **Merge** to `ARCHITECTURE.md` ➔ **Archive** |
| `context/AGENT_RULES.md` | 5,702 | Agent execution parameters | Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |
| `context/DATASET_INTELLIGENCE.md`| 6,838| Data structures and imbalancy resolutions| Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |
| `context/MASTER_CONTEXT.md` | 5,358 | Workspace contexts | Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |
| `context/PROJECT_STATE.md` | 5,438 | Current project checkpoints | Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |
| `context/README.md` | 2,566 | Guide to context directory | Operations | **Archive** |
| `context/REFERENCE_DOCS.md` | 9,279 | Regulatory reference documents | Operations | **Merge** to `OPERATIONS.md` ➔ **Archive** |
| `docs/archive/AGENT_LOADING_STRATEGY.md`| 5,301| Developer compactor strategies | Archive | **Keep in Archive** |
| `docs/archive/ARCHITECTURE_OLD.md`| 6,830 | Outdated system blueprints | Archive | **Keep in Archive** |
| `docs/archive/CLASSIFICATION_REPORT.md`| 6,878| Outdated ML evaluation reports | Archive | **Keep in Archive** |
| `docs/archive/CONTEXT_OPTIMIZATION_REPORT.md`| 5,677| Developer compactor logs | Archive | **Keep in Archive** |
| `docs/archive/CURRENT_SPRINT_OLD.md`| 2,858 | Outdated checklists | Archive | **Keep in Archive** |
| `docs/archive/TASK_QUEUE_OLD.md` | 3,974 | Outdated checklists | Archive | **Keep in Archive** |
| `docs/reference/REFERENCE_DOCS.md`| 6,009 | Legacy manuals | Archive | **Keep in Archive** |
| `prompts/README.md` | 2,566 | Guide to developer prompts directory | Operations | **Archive** |
| `sprints/CURRENT_SPRINT.md` | 2,994 | Active sprint check logs | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `sprints/SPRINT_3.md` | 7,944 | Sprint 3 progress logs | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `sprints/SPRINT_HISTORY.md` | 1,487 | Sprint history summaries | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `tasks/COMPLETED_TASKS.md` | 1,445 | Completed task lists | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
| `tasks/TASK_QUEUE.md` | 4,812 | Pending task lists | Dev History | **Merge** to `DEVELOPMENT_HISTORY.md` ➔ **Archive** |
