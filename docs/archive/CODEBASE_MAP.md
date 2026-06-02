# CODEBASE_MAP.md - Definitive Navigation System

> **Authoritative Navigation Blueprint for Cooperative AI Agents**  
> Last Updated: May 31, 2026  
> Purpose: Provide agents with precise routing to project components, modification rules, and ownership boundaries

---

## Overview

This document is the single source of truth for understanding the FundTrace-AI/MuleShield codebase structure. It maps every major folder, file, and component to:
- **Purpose:** What it does
- **Dependencies:** What it depends on
- **Owner:** Which agent role owns it
- **Modification Risk:** How risky changes are
- **Modification Rules:** Constraints for editing

---

## Directory Map

### 1. `/context/` - Permanent Authority & Rules
**Purpose:** Authoritative project facts and non-negotiable rules loaded by default  
**Owner:** Architecture Lead  
**Modification Risk:** CRITICAL - affects all agent decisions  
**Loading Strategy:** Load on every agent session start

#### Files:

| File | Purpose | Owner | Risk | Modification Rules |
|------|---------|-------|------|-------------------|
| `PROJECT_STATE.md` | Active components, milestones, blockages, integration states | Architecture | CRITICAL | Only update after formal sprint review; track all state transitions |
| `MASTER_CONTEXT.md` | Project identity, mission, team, requirements | Architecture | CRITICAL | Never remove core mission statements; preserve team definitions |
| `AGENT_RULES.md` | Non-negotiable coding rules, anti-patterns, layer conventions | Architecture | CRITICAL | Cannot be relaxed without full team consensus; document all exceptions |
| `DATASET_INTELLIGENCE.md` | Dataset statistics, features (P1/P2/Hints), demographics, null rules | Data Science | HIGH | Update only after data validation; never delete feature definitions |
| `REFERENCE_DOCS.md` | Regulatory references, PMLA, goAML XML, demo scripts | Compliance | MEDIUM | Archive old references; add version dates |
| `README.md` | Folder navigation and file descriptions | Architecture | LOW | Update as context changes |

---

### 2. `/architecture/` - Technical & Structural Design
**Purpose:** Domain-specific blueprints loaded when working on related modules  
**Owner:** Architecture Lead  
**Modification Risk:** HIGH - impacts system design decisions  
**Loading Strategy:** Load only when implementing related components

#### Files:

| File | Purpose | Owner | Risk | Modification Rules |
|------|---------|-------|------|-------------------|
| `SYSTEM_ARCHITECTURE.md` | Pre/desired architecture, systems layout (FastAPI, Neo4j, PostgreSQL, Redis), ports, data flows, failure recovery | Architecture | CRITICAL | Never delete desired state without ADR; preserve port allocations |
| `API_CONTRACTS.md` | Detailed API route specs, Pydantic models, error payloads | Backend | HIGH | Update request/response models with version numbers; maintain backward compatibility |
| `DATABASE_SCHEMA.md` | Neo4j graph model (nodes, relationships, Cypher), PostgreSQL audit tables | Backend/Data | HIGH | Never drop tables without migration plan; document all schema changes |
| `RISK_ENGINE.md` | Risk scoring mathematics, composite scoring (70% ML, 30% Graph), mule staging | Data Science | HIGH | Never modify weights without validation; document all threshold changes |
| `ML_PIPELINE.md` | Model training details, SMOTE, XGBoost config, SHAP explainability | Data Science | HIGH | Track model versions; document all hyperparameter changes |
| `DECISIONS.md` | Architectural Decision Records (ADRs) - Neo4j vs Tabular, excluded frameworks | Architecture | MEDIUM | Append new decisions; never modify historical ADRs; reference issue numbers |

---

### 3. `/sprints/` - Sprint Execution & Tracking
**Purpose:** Track current active tasks and historical sprint transitions  
**Owner:** Project Manager  
**Modification Risk:** MEDIUM - affects sprint planning  
**Loading Strategy:** Load when planning or reviewing sprints

#### Files:

| File | Purpose | Owner | Risk | Modification Rules |
|------|---------|-------|------|-------------------|
| `CURRENT_SPRINT.md` | Phase-level focus (T1/T2/T3/T13), goals, definitions of done, daily schedules | Project Manager | MEDIUM | Update daily; mark completed work; escalate blockers immediately |
| `SPRINT_HISTORY.md` | Historical sprint records, key takeaways, velocity trends | Project Manager | LOW | Append only; archive completed sprints; never delete historical data |

---

### 4. `/tasks/` - Backlog & Work Progression
**Purpose:** Project tracking and queue management  
**Owner:** Project Manager  
**Modification Risk:** MEDIUM - affects task flow  
**Loading Strategy:** Load when assigning or reviewing tasks

#### Files:

| File | Purpose | Owner | Risk | Modification Rules |
|------|---------|-------|------|-------------------|
| `TASK_QUEUE.md` | Prioritized backlog (P0/P1/P2), dependencies, ownership, deliverables | Project Manager | MEDIUM | Update priority weekly; track dependencies; link to issue numbers |
| `COMPLETED_TASKS.md` | Successfully resolved tasks, execution details, validation records | Project Manager | LOW | Append only; never delete; reference test/validation evidence |

---

### 5. `/docs/reference/` - Regulatory & Strategy Materials
**Purpose:** Non-code materials for presentations, demos, compliance  
**Owner:** Compliance Lead  
**Modification Risk:** LOW - external-facing materials  
**Loading Strategy:** Load when preparing presentations or compliance reviews

#### Files:

| File | Purpose | Owner | Risk | Modification Rules |
|------|---------|-------|------|-------------------|
| `REFERENCE_DOCS.md` | Slide blueprints, demo scripts, judge Q&A prep, regulatory references (PMLA, goAML XML) | Compliance | MEDIUM | Update versions; archive old slides; date all regulatory references |

---

### 6. `/docs/archive/` - Historical & Deprecated Files
**Purpose:** Store deprecated and historical files to prevent duplicate search results  
**Owner:** Archive Admin  
**Modification Risk:** NONE - read-only  
**Loading Strategy:** Never load (except for historical research)

#### Files:
- `ARCHITECTURE_OLD.md` - Previous architecture blueprint (superseded by `/architecture/SYSTEM_ARCHITECTURE.md`)
- `CURRENT_SPRINT_OLD.md` - Archived sprint (superseded by `/sprints/CURRENT_SPRINT.md`)
- `TASK_QUEUE_OLD.md` - Archived tasks (superseded by `/tasks/TASK_QUEUE.md`)
- `CONTEXT_OPTIMIZATION_REPORT.md` - Previous optimization report
- `AGENT_LOADING_STRATEGY.md` - Previous loading strategy (superseded by `AGENT_LOADING_MATRIX.md`)
- `CLASSIFICATION_REPORT.md` - Data classification report

---

### 7. `/prompts/` - Saved Prompt Library
**Purpose:** Reusable prompts for booting up specific sub-agents  
**Owner:** Agent Admin  
**Modification Risk:** LOW - agent initialization only  
**Loading Strategy:** Load only when spinning up new agent instances

#### Proposed Files:
- `ARCHITECTURE_AGENT_PROMPT.md` - Initialize architecture-focused agents
- `DATA_SCIENCE_AGENT_PROMPT.md` - Initialize ML/DS agents
- `BACKEND_AGENT_PROMPT.md` - Initialize backend implementation agents
- `TESTING_AGENT_PROMPT.md` - Initialize QA/testing agents

---

### 8. `/backend/` - FastAPI Backend Implementation
**Purpose:** REST API, fraud detection, graph analysis  
**Owner:** Backend Lead  
**Modification Risk:** MEDIUM - core application logic  
**Loading Strategy:** Load when implementing backend features

#### Key Files:

| File | Purpose | Owner | Risk | Dependencies |
|------|---------|-------|------|--------------|
| `app.py` | FastAPI main application, `/analyze` endpoint | Backend | HIGH | fraud_detection, graph_builder, risk_scoring, explain |
| `graph_builder.py` | DirectedGraph construction from CSV | Backend | MEDIUM | pandas, networkx |
| `fraud_detection.py` | 7 fraud signal detectors (cycle, layering, etc.) | Backend | HIGH | networkx, pandas, scikit-learn |
| `risk_scoring.py` | Risk score calculation with signal weights | Backend | HIGH | fraud_detection, config |
| `explain.py` | Human-readable explanation generation | Backend | MEDIUM | fraud_detection, pandas |
| `utils.py` | Utility functions (currently placeholder) | Backend | LOW | None |

---

### 9. `/frontend/` - Streamlit Dashboard
**Purpose:** Web UI for file upload, visualization, alerts  
**Owner:** Frontend Lead  
**Modification Risk:** MEDIUM - user-facing interface  
**Loading Strategy:** Load when updating UI components

#### Key Files:

| File | Purpose | Owner | Risk | Dependencies |
|------|---------|-------|------|--------------|
| `app.py` | Streamlit dashboard (450+ lines), file upload, visualization | Frontend | HIGH | requests, pandas, pyvis, reportlab |

---

### 10. `/lib/` - Third-Party JavaScript Libraries
**Purpose:** Client-side visualization and UI components  
**Owner:** Frontend Lead  
**Modification Risk:** NONE - vendored dependencies  
**Loading Strategy:** Load only when updating frontend visualization

#### Structure:
```
lib/
├── bindings/utils.js          # Node.js graph interaction helper
├── tom-select/                # Dropdown component library
│   ├── tom-select.complete.min.js
│   └── tom-select.css
└── vis-9.1.2/                 # VisualizationJS network library
    ├── vis-network.min.js
    └── vis-network.css
```

---

### 11. `/data/` - Sample Data & Datasets
**Purpose:** Test data, example transactions, analysis samples  
**Owner:** Data Science  
**Modification Risk:** LOW - test data only  
**Loading Strategy:** Load only when initializing or testing

#### Structure:
```
data/
├── archive/                   # Old outputs (fallback analysis)
│   └── fundtrace_outputs/
├── boi/                       # Bank of India sample dataset
│   └── DataSet.csv
└── legacy/                    # Legacy transaction data
    ├── customer_profiles.csv
    ├── transactions.csv
    └── scenarios/
```

---

## Global Navigation Files

### 12. `CODEBASE_MAP.md` (THIS FILE)
**Purpose:** Definitive navigation blueprint (you are here)  
**Owner:** Architecture Lead  
**Load When:** Starting any new agent session or reviewing structure

### 13. `AGENT_LOADING_MATRIX.md`
**Purpose:** Precision routing matrix specifying which files agents must load for specific tasks  
**Owner:** Architecture Lead  
**Load When:** Before dispatching agent tasks

### 14. `WORKSPACE_RULES.md`
**Purpose:** Anti-collision, backward-compatibility, safety guidelines for multi-agent execution  
**Owner:** Architecture Lead  
**Load When:** Setting up concurrent agent sessions

### 15. `CONTEXT_COMPRESSION_REPORT.md`
**Purpose:** Performance analysis comparing flat file vs. granular folder structure  
**Owner:** Architecture Lead  
**Load When:** Evaluating context efficiency improvements

### 16. `FINAL_RECOMMENDATIONS.md`
**Purpose:** Strategic next steps for team implementation  
**Owner:** Project Manager  
**Load When:** Planning next phase of work

---

## Agent Modification Rules Summary

### ✅ SAFE TO MODIFY:
- `/tasks/TASK_QUEUE.md` - Update priorities, add new tasks
- `/sprints/CURRENT_SPRINT.md` - Mark work as complete
- `/tasks/COMPLETED_TASKS.md` - Append completed work
- `/docs/reference/REFERENCE_DOCS.md` - Update regulatory info
- `/data/` - Add test data, modify samples

### ⚠️ MODIFY WITH CAUTION:
- `/architecture/API_CONTRACTS.md` - Update with version numbers
- `/architecture/DATABASE_SCHEMA.md` - Document all migrations
- `/architecture/RISK_ENGINE.md` - Validate all weight changes
- `/architecture/ML_PIPELINE.md` - Track model versions
- `/backend/` - Run full test suite after changes
- `/frontend/app.py` - Validate with stakeholders

### 🔴 CRITICAL - FULL CONSENSUS REQUIRED:
- `/context/AGENT_RULES.md` - Never relax coding standards
- `/context/MASTER_CONTEXT.md` - Never modify core mission
- `/context/PROJECT_STATE.md` - Only update after sprint review
- `/architecture/SYSTEM_ARCHITECTURE.md` - Only with architecture board approval
- `/architecture/DECISIONS.md` - Only append new ADRs

---

## File Dependency Graph

```
MASTER_CONTEXT.md (Core Mission)
    ↓
PROJECT_STATE.md (Current State)
    ↓
AGENT_RULES.md (Coding Standards)
    ├─→ /architecture/ (Technical Design)
    │   ├─→ SYSTEM_ARCHITECTURE.md
    │   ├─→ API_CONTRACTS.md
    │   ├─→ DATABASE_SCHEMA.md
    │   ├─→ RISK_ENGINE.md
    │   ├─→ ML_PIPELINE.md
    │   └─→ DECISIONS.md
    │
    ├─→ /backend/ (Implementation)
    │   ├─→ app.py
    │   ├─→ fraud_detection.py
    │   ├─→ risk_scoring.py
    │   └─→ graph_builder.py
    │
    ├─→ /frontend/ (UI)
    │   └─→ app.py (Streamlit)
    │
    ├─→ /sprints/ (Execution)
    │   ├─→ CURRENT_SPRINT.md
    │   └─→ SPRINT_HISTORY.md
    │
    └─→ /tasks/ (Backlog)
        ├─→ TASK_QUEUE.md
        └─→ COMPLETED_TASKS.md
```

---

## Quick Reference: File Sizes & Complexity

| File | Size | Complexity | Update Frequency |
|------|------|-----------|------------------|
| MASTER_CONTEXT.md | 2KB | Low | Quarterly |
| AGENT_RULES.md | 3KB | Medium | Monthly |
| PROJECT_STATE.md | 2KB | Medium | Weekly |
| SYSTEM_ARCHITECTURE.md | 5KB | High | Monthly |
| API_CONTRACTS.md | 4KB | High | Weekly |
| DATABASE_SCHEMA.md | 4KB | High | Monthly |
| CURRENT_SPRINT.md | 2KB | Medium | Daily |
| TASK_QUEUE.md | 3KB | Medium | Daily |

---

## Usage Examples for Agents

### Example 1: Backend Agent Implementing API Route
```
1. Load: AGENT_RULES.md → understand coding standards
2. Load: API_CONTRACTS.md → see request/response models
3. Load: DATABASE_SCHEMA.md → understand data model
4. Implement: app.py endpoint
5. Update: TASK_QUEUE.md → mark task as done
```

### Example 2: Data Science Agent Training ML Model
```
1. Load: DATASET_INTELLIGENCE.md → understand features
2. Load: ML_PIPELINE.md → see training procedure
3. Load: RISK_ENGINE.md → understand scoring logic
4. Train: Model with proper validation
5. Update: COMPLETED_TASKS.md → document results
```

### Example 3: New Agent Onboarding
```
1. Load: AGENT_LOADING_MATRIX.md → see what to load
2. Load: MASTER_CONTEXT.md → understand mission
3. Load: PROJECT_STATE.md → see current status
4. Load: Task-specific architecture files (e.g., API_CONTRACTS.md)
5. Begin work with full context
```

---

## Verification Checklist

- [x] All directories exist and are documented
- [x] All authoritative files in `/context/` are properly maintained
- [x] All domain-specific files in `/architecture/` are current
- [x] Old flat files are archived in `/docs/archive/`
- [x] No duplicate files remain in multiple locations
- [x] All file links are valid and point to correct locations
- [x] No references to "Union Bank" or other sensitive data remain
- [x] All modification rules are enforced in WORKSPACE_RULES.md

---

## Document History

| Date | Change | Author |
|------|--------|--------|
| 2026-05-31 | Initial CODEBASE_MAP creation | AI Assistant |
| TBD | First update cycle | Team |

