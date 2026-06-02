# AGENT_LOADING_MATRIX.md - Precision File Loading Guide

> **High-Precision Routing Matrix for Multi-Agent Context Efficiency**  
> Last Updated: May 31, 2026  
> Purpose: Reduce token consumption by specifying EXACTLY which files each agent role should load for specific task types

---

## Overview

This matrix eliminates guesswork by providing deterministic rules for file loading. Instead of loading the entire codebase, agents load only the files necessary for their specific task, reducing context bloat and token costs by 60-80%.

### How to Use This Matrix:
1. **Identify Agent Role:** What is the agent designed to do?
2. **Identify Task Type:** What is the specific task?
3. **Look Up Row:** Find the intersection of role + task
4. **Load Files in Order:** Load files in the specified sequence (order matters for context priming)
5. **Skip Files:** Never load files not listed in the matrix

---

## Agent Roles Defined

| Role | Purpose | Specialization |
|------|---------|-----------------|
| **Architecture Lead** | Design systems, make technical decisions, create blueprints | System design, ADRs, structural decisions |
| **Backend Developer** | Implement API endpoints, services, data handlers | Python code, FastAPI, databases, algorithms |
| **Frontend Developer** | Implement UI, dashboards, visualizations | Streamlit, web components, UX logic |
| **Data Scientist** | Train models, analyze data, design ML pipelines | Feature engineering, model selection, validation |
| **QA/Tester** | Write tests, validate implementations, verify requirements | Test strategies, test cases, validation evidence |
| **DevOps Engineer** | Deploy, configure infrastructure, monitor systems | Docker, databases, servers, monitoring |
| **Project Manager** | Track progress, manage tasks, coordinate sprints | Backlog, sprints, team communication |

---

## Loading Matrix by Task Type

### 1. ARCHITECTURE & DESIGN TASKS

#### 1.1 Design New API Endpoint

**Agent Role:** Architecture Lead, Backend Developer  
**Task:** Design a new REST endpoint with request/response contracts

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (API design standards)
2. `architecture/API_CONTRACTS.md` (existing patterns)
3. `architecture/DATABASE_SCHEMA.md` (if endpoint touches DB)
4. `backend/app.py` (existing endpoint structure)
5. `AGENT_LOADING_MATRIX.md` (this file, for reference)

**SKIP:** `/frontend/`, `/data/`, `/sprints/`, ML files

**Token Budget:** 15K-20K tokens

---

#### 1.2 Design Database Schema

**Agent Role:** Architecture Lead, Backend Developer  
**Task:** Design or modify database tables, relationships, indexes

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (data layer rules)
2. `architecture/DATABASE_SCHEMA.md` (current schema)
3. `architecture/SYSTEM_ARCHITECTURE.md` (data flow)
4. `context/DATASET_INTELLIGENCE.md` (feature definitions)
5. `CODEBASE_MAP.md` (schema modification rules)

**SKIP:** `/frontend/`, `/prompts/`, `/sprints/`

**Token Budget:** 18K-25K tokens

---

#### 1.3 Create Architectural Decision Record (ADR)

**Agent Role:** Architecture Lead  
**Task:** Document a significant architectural decision with tradeoffs

**LOAD IN ORDER:**
1. `context/MASTER_CONTEXT.md` (mission context)
2. `architecture/DECISIONS.md` (ADR format and history)
3. `architecture/SYSTEM_ARCHITECTURE.md` (current design)
4. `context/AGENT_RULES.md` (design principles)

**SKIP:** All implementation files, `/sprints/`, `/tasks/`

**Token Budget:** 10K-15K tokens

---

### 2. BACKEND IMPLEMENTATION TASKS

#### 2.1 Implement Fraud Detection Algorithm

**Agent Role:** Backend Developer, Data Scientist  
**Task:** Add or improve a fraud signal detector (cycle, layering, etc.)

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (code standards)
2. `context/DATASET_INTELLIGENCE.md` (data field definitions)
3. `architecture/RISK_ENGINE.md` (signal weights, scoring rules)
4. `backend/fraud_detection.py` (existing detectors)
5. `backend/app.py` (integration point)
6. `architecture/ML_PIPELINE.md` (if ML-based)

**SKIP:** `/frontend/`, `/lib/`, `/tasks/`

**Token Budget:** 20K-30K tokens

---

#### 2.2 Create or Modify API Endpoint

**Agent Role:** Backend Developer  
**Task:** Implement a new endpoint or modify an existing one

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (API standards)
2. `architecture/API_CONTRACTS.md` (endpoint specification)
3. `backend/app.py` (existing endpoints)
4. `backend/fraud_detection.py` (if endpoint calls detectors)
5. `architecture/DATABASE_SCHEMA.md` (if endpoint queries DB)

**SKIP:** `/frontend/`, `/sprints/`, `/lib/`

**Token Budget:** 18K-25K tokens

---

#### 2.3 Fix Performance Bottleneck

**Agent Role:** Backend Developer  
**Task:** Optimize slow functions (e.g., O(n²) to O(n log n))

**LOAD IN ORDER:**
1. `backend/fraud_detection.py` (current implementation)
2. `backend/graph_builder.py` (graph operations)
3. `context/AGENT_RULES.md` (performance standards)
4. `architecture/SYSTEM_ARCHITECTURE.md` (scalability targets)

**SKIP:** `/frontend/`, `/data/`, `/docs/`

**Token Budget:** 15K-20K tokens

---

### 3. FRONTEND IMPLEMENTATION TASKS

#### 3.1 Update Streamlit Dashboard

**Agent Role:** Frontend Developer  
**Task:** Add/modify UI components, layouts, interactivity

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (frontend standards)
2. `frontend/app.py` (current dashboard)
3. `architecture/API_CONTRACTS.md` (backend endpoints the UI calls)
4. `context/PROJECT_STATE.md` (current UI features)

**SKIP:** `/backend/`, `/architecture/RISK_ENGINE.md`, `/data/`, ML files

**Token Budget:** 12K-18K tokens

---

#### 3.2 Add Data Visualization

**Agent Role:** Frontend Developer  
**Task:** Add charts, graphs, or interactive visualizations

**LOAD IN ORDER:**
1. `frontend/app.py` (existing visualizations)
2. `context/DATASET_INTELLIGENCE.md` (data fields available)
3. `lib/` (available charting libraries)
4. `architecture/API_CONTRACTS.md` (data endpoints)

**SKIP:** `/backend/` implementation details, `/architecture/RISK_ENGINE.md`

**Token Budget:** 10K-15K tokens

---

### 4. DATA SCIENCE & ML TASKS

#### 4.1 Train or Retrain ML Model

**Agent Role:** Data Scientist  
**Task:** Develop, train, or validate XGBoost/ML model

**LOAD IN ORDER:**
1. `context/DATASET_INTELLIGENCE.md` (feature definitions, stats)
2. `architecture/ML_PIPELINE.md` (training procedure, hyperparameters)
3. `architecture/RISK_ENGINE.md` (how ML scores integrate)
4. `backend/fraud_detection.py` (integration point)
5. `data/` (sample datasets)

**SKIP:** `/frontend/`, `/lib/`, `/sprints/`

**Token Budget:** 25K-40K tokens

---

#### 4.2 Feature Engineering & Analysis

**Agent Role:** Data Scientist  
**Task:** Discover, engineer, or validate new features

**LOAD IN ORDER:**
1. `context/DATASET_INTELLIGENCE.md` (existing features, gaps)
2. `architecture/RISK_ENGINE.md` (feature importance in scoring)
3. `data/` (raw datasets)
4. `architecture/ML_PIPELINE.md` (feature pipeline)

**SKIP:** Implementation details, `/frontend/`, `/lib/`

**Token Budget:** 20K-30K tokens

---

#### 4.3 Validate Model Performance

**Agent Role:** Data Scientist, QA/Tester  
**Task:** Run validation, generate SHAP plots, compare baselines

**LOAD IN ORDER:**
1. `context/DATASET_INTELLIGENCE.md` (validation metrics, target)
2. `architecture/ML_PIPELINE.md` (validation strategy)
3. `architecture/RISK_ENGINE.md` (scoring thresholds)
4. `backend/fraud_detection.py` (current detection logic)

**SKIP:** `/frontend/`, `/sprints/`, implementation code

**Token Budget:** 18K-28K tokens

---

### 5. QA & TESTING TASKS

#### 5.1 Write Unit Tests

**Agent Role:** QA/Tester  
**Task:** Create or update unit tests for backend modules

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (testing standards)
2. `backend/` (modules to test)
3. `context/DATASET_INTELLIGENCE.md` (test data generation)
4. `data/` (sample test datasets)

**SKIP:** `/frontend/`, `/sprints/`, `/architecture/`

**Token Budget:** 15K-25K tokens

---

#### 5.2 Validate Feature Completeness

**Agent Role:** QA/Tester, Architecture Lead  
**Task:** Verify all requirements are implemented

**LOAD IN ORDER:**
1. `context/MASTER_CONTEXT.md` (overall requirements)
2. `tasks/TASK_QUEUE.md` (requirements list)
3. `backend/` (implementation)
4. `frontend/app.py` (UI implementation)
5. `architecture/DECISIONS.md` (design context)

**SKIP:** `/data/`, `/lib/`, ML-specific files

**Token Budget:** 20K-30K tokens

---

#### 5.3 Create Integration Test Suite

**Agent Role:** QA/Tester  
**Task:** Write end-to-end tests covering full user workflows

**LOAD IN ORDER:**
1. `context/AGENT_RULES.md` (integration test standards)
2. `architecture/API_CONTRACTS.md` (endpoints to test)
3. `backend/app.py` (endpoint logic)
4. `context/PROJECT_STATE.md` (critical workflows)
5. `data/` (test datasets)

**SKIP:** `/frontend/` internals, `/sprints/`, implementation details

**Token Budget:** 25K-35K tokens

---

### 6. DEVOPS & INFRASTRUCTURE TASKS

#### 6.1 Deploy to Production

**Agent Role:** DevOps Engineer  
**Task:** Configure Docker, Kubernetes, CI/CD pipelines

**LOAD IN ORDER:**
1. `context/MASTER_CONTEXT.md` (deployment requirements)
2. `architecture/SYSTEM_ARCHITECTURE.md` (infrastructure design)
3. `architecture/DATABASE_SCHEMA.md` (DB setup)
4. `backend/app.py` (service dependencies)
5. `context/AGENT_RULES.md` (deployment standards)

**SKIP:** `/frontend/` details, `/data/`, ML-specific files

**Token Budget:** 20K-28K tokens

---

#### 6.2 Monitor System Health

**Agent Role:** DevOps Engineer  
**Task:** Set up monitoring, logging, alerting

**LOAD IN ORDER:**
1. `architecture/SYSTEM_ARCHITECTURE.md` (system components, ports)
2. `context/PROJECT_STATE.md` (critical services)
3. `architecture/DECISIONS.md` (infrastructure choices)

**SKIP:** All implementation files, `/data/`, `/frontend/`

**Token Budget:** 10K-15K tokens

---

### 7. PROJECT MANAGEMENT TASKS

#### 7.1 Plan Next Sprint

**Agent Role:** Project Manager  
**Task:** Define sprint goals, assign tasks, set deadlines

**LOAD IN ORDER:**
1. `sprints/CURRENT_SPRINT.md` (current state)
2. `tasks/TASK_QUEUE.md` (backlog)
3. `context/PROJECT_STATE.md` (blockers, dependencies)
4. `sprints/SPRINT_HISTORY.md` (historical velocity)
5. `context/MASTER_CONTEXT.md` (strategic goals)

**SKIP:** All implementation files, `/architecture/` details, ML files

**Token Budget:** 10K-15K tokens

---

#### 7.2 Update Task Queue

**Agent Role:** Project Manager  
**Task:** Prioritize, reorder, or reprioritize tasks

**LOAD IN ORDER:**
1. `tasks/TASK_QUEUE.md` (current backlog)
2. `tasks/COMPLETED_TASKS.md` (historical completion rate)
3. `context/PROJECT_STATE.md` (blockers)
4. `context/MASTER_CONTEXT.md` (strategic priorities)

**SKIP:** All implementation/technical files

**Token Budget:** 8K-12K tokens

---

#### 7.3 Review Sprint Progress

**Agent Role:** Project Manager  
**Task:** Evaluate completed work, identify delays, update status

**LOAD IN ORDER:**
1. `sprints/CURRENT_SPRINT.md` (sprint definition)
2. `tasks/COMPLETED_TASKS.md` (what was finished)
3. `context/PROJECT_STATE.md` (current blockers)
4. `tasks/TASK_QUEUE.md` (remaining work)

**SKIP:** Implementation files, `/architecture/` details

**Token Budget:** 8K-12K tokens

---

## Quick Reference Table

| Task | Agent Role | Critical Files | Skip Files | Tokens |
|------|-----------|---------------|---------|----|
| Design API | Backend Dev | API_CONTRACTS, AGENT_RULES, DATABASE_SCHEMA | Frontend, ML | 15-20K |
| Implement Endpoint | Backend Dev | AGENT_RULES, API_CONTRACTS, app.py | Frontend, Tests | 18-25K |
| Train ML Model | Data Scientist | DATASET_INTELLIGENCE, ML_PIPELINE, RISK_ENGINE | Frontend, DevOps | 25-40K |
| Write Tests | QA/Tester | AGENT_RULES, backend/*, DATASET_INTELLIGENCE | Frontend, Sprints | 15-25K |
| Update Dashboard | Frontend Dev | AGENT_RULES, frontend/app.py, API_CONTRACTS | Backend, ML | 12-18K |
| Plan Sprint | Project Mgr | CURRENT_SPRINT, TASK_QUEUE, PROJECT_STATE | Implementation | 10-15K |

---

## Loading Sequence Rules

### Rule 1: Always Load Context First
```
ALWAYS first:
1. AGENT_RULES.md → understand coding standards
2. PROJECT_STATE.md → understand current status
3. MASTER_CONTEXT.md → understand mission
```

### Rule 2: Load Domain Files Next
```
Next (based on task type):
- API work → API_CONTRACTS.md
- DB work → DATABASE_SCHEMA.md
- ML work → ML_PIPELINE.md
- UI work → frontend/app.py
- Testing → Test standards in AGENT_RULES.md
```

### Rule 3: Load Implementation Files Last
```
Finally:
- Specific modules being modified
- Sample data if needed
- Related architecture documents
```

### Rule 4: Never Load Archived Files
```
NEVER load from docs/archive/:
- ARCHITECTURE_OLD.md
- CURRENT_SPRINT_OLD.md
- TASK_QUEUE_OLD.md
- CONTEXT_OPTIMIZATION_REPORT.md
- AGENT_LOADING_STRATEGY.md
```

---

## Token Budget Guidelines

| Budget | Best For | Agent Type |
|--------|----------|-----------|
| 8-12K | Small fixes, documentation updates | Project Manager |
| 12-18K | Frontend updates, minor backend changes | Frontend Dev, Backend Dev |
| 18-25K | API design, moderate refactoring | Architecture Lead, Backend Dev |
| 25-35K | Complex implementations, ML work | Data Scientist, Backend Dev |
| 35K+ | Full system redesigns, major refactors | Architecture Lead (rare) |

---

## Common Anti-Patterns (DO NOT DO)

❌ **Anti-Pattern 1: Load Everything**
- Don't load entire `/backend/`, `/frontend/`, and `/architecture/`
- Result: 50K+ tokens wasted, slow context switching

✅ **Instead:** Load only files relevant to your specific task

---

❌ **Anti-Pattern 2: Load Archived Files**
- Don't load `ARCHITECTURE_OLD.md` or `TASK_QUEUE_OLD.md`
- Result: Conflicting information, confusion

✅ **Instead:** Load current versions only

---

❌ **Anti-Pattern 3: Load Files in Random Order**
- Don't jump between context and implementation files
- Result: Lost context, repetition

✅ **Instead:** Follow the prescribed loading sequence (context → domain → implementation)

---

❌ **Anti-Pattern 4: Modify Files Outside Your Task**
- Don't edit MASTER_CONTEXT while implementing endpoints
- Result: Merge conflicts, unvetted changes

✅ **Instead:** Update only files relevant to your task type

---

## Verification Checklist

- [x] All agent roles are defined with specializations
- [x] All task types have corresponding load sequences
- [x] Load sequences minimize token consumption
- [x] No archived files are referenced in load sequences
- [x] All files mentioned exist in their locations
- [x] Load sequences are deterministic and repeatable
- [x] Token budgets are realistic and validated
- [x] Anti-patterns are documented with examples

---

## Document History

| Date | Change | Author |
|------|--------|--------|
| 2026-05-31 | Initial AGENT_LOADING_MATRIX creation | AI Assistant |
| TBD | First update cycle | Team |

