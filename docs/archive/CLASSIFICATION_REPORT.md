# Knowledge Base Classification & Folder Structure Report

This report analyzes every knowledge base file in the repository, classifies it according to its primary operational purpose, defines the ideal workspace structure, and outlines which files reside in each folder to ensure high-performance multi-agent development.

---

## Phase 1: Classification Analysis

Each file is classified into one of the following operational layers to minimize context overlap, eliminate architectural drift, and control token consumption during agent calls:

| Classification | Core Purpose | Files Covered |
| :--- | :--- | :--- |
| **1. Permanent Context** | Identity, core system state, non-negotiable hackathon requirements. Load at session startup. | - [MASTER_CONTEXT.md](file:///d:/Projects/FundTrace-AI/context/MASTER_CONTEXT.md)<br>- [PROJECT_STATE.md](file:///d:/Projects/FundTrace-AI/context/PROJECT_STATE.md) |
| **2. Architecture Knowledge** | Technical specifications, schemas, interfaces, scoring math, and design logs. Load for implementation. | - [SYSTEM_ARCHITECTURE.md](file:///d:/Projects/FundTrace-AI/architecture/SYSTEM_ARCHITECTURE.md)<br>- [API_CONTRACTS.md](file:///d:/Projects/FundTrace-AI/architecture/API_CONTRACTS.md)<br>- [DATABASE_SCHEMA.md](file:///d:/Projects/FundTrace-AI/architecture/DATABASE_SCHEMA.md)<br>- [RISK_ENGINE.md](file:///d:/Projects/FundTrace-AI/architecture/RISK_ENGINE.md)<br>- [ML_PIPELINE.md](file:///d:/Projects/FundTrace-AI/architecture/ML_PIPELINE.md)<br>- [DECISIONS.md](file:///d:/Projects/FundTrace-AI/architecture/DECISIONS.md) |
| **3. Dataset Knowledge** | Specific tables, mappings, feature selections, demographic indicators. Load for ML logic. | - [DATASET_INTELLIGENCE.md](file:///d:/Projects/FundTrace-AI/context/DATASET_INTELLIGENCE.md) |
| **4. Sprint Knowledge** | Daily scope, targets, active blockers, current focus. Load for standups and execution. | - [CURRENT_SPRINT.md](file:///d:/Projects/FundTrace-AI/sprints/CURRENT_SPRINT.md)<br>- [SPRINT_HISTORY.md](file:///d:/Projects/FundTrace-AI/sprints/SPRINT_HISTORY.md) |
| **5. Task Knowledge** | Prioritized backlog, milestones, verification logs of completed tasks. Load for planning. | - [TASK_QUEUE.md](file:///d:/Projects/FundTrace-AI/tasks/TASK_QUEUE.md)<br>- [COMPLETED_TASKS.md](file:///d:/Projects/FundTrace-AI/tasks/COMPLETED_TASKS.md) |
| **6. Agent Instructions** | Guidelines, prompt templates, loading directories, anti-patterns. Embedded or root load. | - [AGENT_RULES.md](file:///d:/Projects/FundTrace-AI/context/AGENT_RULES.md)<br>- [WORKSPACE_RULES.md](file:///d:/Projects/FundTrace-AI/WORKSPACE_RULES.md)<br>- [AGENT_LOADING_MATRIX.md](file:///d:/Projects/FundTrace-AI/AGENT_LOADING_MATRIX.md) |
| **7. Reference Material** | Slides, scripts, regulatory citations (PMLA, goAML XML), demo scenarios. Low frequency load. | - [REFERENCE_DOCS.md](file:///d:/Projects/FundTrace-AI/docs/reference/REFERENCE_DOCS.md) |
| **8. Archive Material** | Historical analysis, legacy project reports, raw inputs. Archival storage; never load. | - [PROJECT_ANALYSIS.md](file:///d:/Projects/FundTrace-AI/docs/archive/PROJECT_ANALYSIS.md) (moved)<br>- [CHANGELOG.md](file:///d:/Projects/FundTrace-AI/docs/archive/CHANGELOG.md) (moved)<br>- [CONTEXT_OPTIMIZATION_REPORT.md](file:///d:/Projects/FundTrace-AI/docs/archive/CONTEXT_OPTIMIZATION_REPORT.md) (archived) |

---

## Phase 2: Ideal Folder Structure

To prevent context leakage and guarantee that agents read only domain-specific instructions, the repository knowledge base has been restructured as follows:

```
project-root/
│
├── context/                         # Active Core & Permanent Context
│   ├── MASTER_CONTEXT.md            # Project identity, stack, success criteria
│   ├── PROJECT_STATE.md             # Current active states, blockers, integrations
│   ├── AGENT_RULES.md               # Context boundaries and identity invariants
│   └── DATASET_INTELLIGENCE.md      # Authoritative dataset feature reference
│
├── architecture/                    # Technical Blueprints
│   ├── SYSTEM_ARCHITECTURE.md       # Pre vs target architecture, services, failure modes
│   ├── API_CONTRACTS.md             # Endpoint Pydantic specs and payloads
│   ├── DATABASE_SCHEMA.md           # Neo4j graph and PostgreSQL relational schemas
│   ├── RISK_ENGINE.md               # Risk scoring mathematics, mule stages logic
│   ├── ML_PIPELINE.md               # Model training, SMOTE, XGBoost hyperparameters
│   └── DECISIONS.md                 # Architectural Decision Records (ADRs)
│
├── sprints/                         # Sprint & Iteration State
│   ├── CURRENT_SPRINT.md            # Focus checklist and Definition of Done
│   └── SPRINT_HISTORY.md            # Historic sprint releases
│
├── tasks/                           # Work Tracking & Progression
│   ├── TASK_QUEUE.md                # Prioritized backlog of all tasks (P0, P1, P2)
│   └── COMPLETED_TASKS.md           # Log of successfully verified integrations
│
├── prompts/                         # Agent Prompts & Templates
│   └── (Contains specialized templates from raw strategy materials)
│
├── docs/
│   ├── reference/                   # Non-agent reference materials
│   │   └── REFERENCE_DOCS.md        # Slide decks, demo scripts, regulatory citation
│   └── archive/                     # Obsolete or historical documents (Never Loaded)
│       ├── PROJECT_ANALYSIS.md      # Original analysis of the monolithic codebase
│       ├── CLASSIFICATION_REPORT.md # This classification and layout report
│       └── CONTEXT_OPTIMIZATION.md  # Legacy optimization logs
│
├── WORKSPACE_RULES.md               # Multi-agent general conduct principles (root)
├── AGENT_LOADING_MATRIX.md          # Precise task-to-context loading matrix (root)
├── CODEBASE_MAP.md                  # Complete navigation system for files (root)
└── CONTEXT_COMPRESSION_REPORT.md    # Size reduction and reasoning quality analysis (root)
```

### Allocation Rules:
1. **Never load `docs/archive/` files into any agent's context window.** They represent historical states and will result in regression or identity drift ("Union Bank" contamination).
2. **`context/` files are loaded by default at startup** or whenever an execution path begins.
3. **`architecture/` files are highly specialized.** Backend developers load `API_CONTRACTS.md` and `SYSTEM_ARCHITECTURE.md`. Database workers load `DATABASE_SCHEMA.md` and `RISK_ENGINE.md`. ML developers load `ML_PIPELINE.md`.
4. **All files in the root (`WORKSPACE_RULES.md`, `CODEBASE_MAP.md`, etc.)** serve as high-level control anchors to keep all agents coordinated.
