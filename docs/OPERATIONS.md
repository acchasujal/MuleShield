# MuleShield AI — Operations and Workspace Specification

This document provides a comprehensive operational guide for the MuleShield AI platform. It consolidates all multi-agent workspace safety rules, coding standards, dataset profiles, regulatory compliance details, and deployment guidelines.

---

## 1. Multi-Agent Workspace Rules & Anti-Collision Framework

To coordinate tasks without merge conflicts or configuration drift, all cooperative agents must strictly adhere to the following ownership and locking rules:

### 1.1 File Ownership & Modification Rights

#### Tier 1: Exclusively Owned (Read-Only to Secondary Agents)
Only the designated owner role can modify these documents. All other roles are restricted to read-only access:
* `context/AGENT_RULES.md` — Owner: **Architecture Lead**
* `context/MASTER_CONTEXT.md` — Owner: **Architecture Lead**
* `architecture/DECISIONS.md` — Owner: **Architecture Lead** (ADRs are append-only)
* `architecture/SYSTEM_ARCHITECTURE.md` — Owner: **Architecture Lead**
* `context/PROJECT_STATE.md` — Owner: **Project Manager**
* `sprints/*` and `tasks/*` — Owner: **Project Manager** (sprint logs and backlog tracking)

#### Tier 2: Role-Owned with Shared Access (Requires Explicit Coordination)
These files have a primary owner but related roles can modify them under coordination (e.g. backend and frontend leads aligning on API contracts or database schema changes):
* `architecture/API_CONTRACTS.md` — Owner: **Backend Lead** (Coordination required before endpoint changes)
* `architecture/DATABASE_SCHEMA.md` — Owner: **Backend Lead** (Coordination required before SQL schema changes)
* `architecture/RISK_ENGINE.md` — Owner: **Data Science Lead** (Coordination required before modifying fusion weights)
* `architecture/ML_PIPELINE.md` — Owner: **Data Science Lead** (Coordination required before model configuration changes)
* `backend/app.py` & `frontend/app.py` — Owned by respective leads.

#### Tier 3: Collaborative Files (Open Writes, Atomic Updates Only)
These files can be modified by any agent to update feature details, regulatory checklists, or logs, following atomic unit guidelines:
* `context/DATASET_INTELLIGENCE.md` — Per-feature block atomic updates.
* `context/REFERENCE_DOCS.md` — Per-regulatory section updates.
* `docs/archive/*` — Append-only historical files.

### 1.2 Atomic Modifications & Versioning Rules
* **Atomic commits:** Each modification must resolve exactly one logical task (e.g., adding a specific helper function or updating a single risk weight). Do not bundle unrelated changes.
* **Locking logic:** Before writing to a Tier 1 or Tier 2 file, inspect the `last_modified` timestamp. If another agent has committed a change in the past 5 minutes, wait to avoid conflict errors.
* **Semantic versioning:** Increment documentation version numbers in the metadata header on every write.
* **Rollback plan:** Tag stable commits. If a change triggers unit test failures or breaks backward compatibility, immediately execute a tag revert (`git checkout snapshot/tag`).

---

## 2. Technical Coding Standards & Identity Invariants

### 2.1 Identity Invariants
* **Product Branding:** Always refer to the platform as **MuleShield AI**. Never use "FundTrace AI" or "FundTrace" in code, configurations, logs, or user interfaces.
* **Organizational Branding:** The target institution is the **Bank of India** (or **BOI**). Never refer to "Union Bank", "Union Bank of India", or "UBI".
* **Problem Domain:** The target domain is **mule account detection and network classification**. Avoid generic "fraud detection" terms in strings and variables.
* **User Terminology:** User-facing tables, badge cards, and labels must use **"mule account"** or **"flagged entity"** (never "suspicious account" or "fraud account" unless quoting regulatory laws).

### 2.2 Backend & ML Boundaries
* **Scoring Centralization:** The composite risk score must be calculated *exclusively* via `calculate_composite_risk` inside `backend/risk_scoring.py` (which forwards to `backend/ml/score_fusion.py`). Do not inline risk calculations in routes or components.
* **Startup ML Loading:** Model binaries and SimpleImputer artifacts must be loaded *only once* during the FastAPI server `lifespan` startup hook. Never reload model pickles per request.
* **Feature Index Integrity:** Feature lists are locked to the 122 validated variables defined in `final_metadata.json`. Never add or omit columns dynamically.
* **Categorical Fallbacks:** Mappings must be retrieved from `cat_mappings.json`. If an unknown category is encountered at inference runtime, map it to `0` to prevent crashes.

---

## 3. Dataset Fact Sheet & Feature Engineering

### 3.1 Dataset Profile (`DataSet.csv`)
* **Total Dimension:** 9,082 records, 3,924 columns (`F1` to `F3924`).
* **Target Label:** `F3924` (0 = Legitimate profile, 1 = Suspicious Mule profile).
* **Positive Class Distribution:** 81 accounts (0.9% positive class rate).
* **Negative Class Distribution:** 9,001 accounts (99.1% negative class rate).
* **Imbalance Ratio:** 111.1 : 1.
* **Missing Value Rate:** 27.6% mean rate across columns.
* **Cleaned Input Feature Size:** **122 features** (after variance and domain-expert filtering).

### 3.2 Prior TMS Flag Data Leakage Prevention (`F3912`)
* **The Hazard:** Feature **F3912** has a **0.97 Pearson correlation** with the target variable `F3924` (with 79 out of 81 mule profiles having `F3912=1`, and only 3 out of 9,001 legitimate profiles having `F3912=1`). This feature represents a legacy transaction monitoring warning.
* **Exclusion Rule:** **F3912 must be completely excluded from training datasets.** Models trained with `F3912` present achieve 99%+ accuracy but fail to generalize to new, unflagged mule accounts.
* **Post-Inference Use:** `F3912` is reserved strictly for post-inference Mule Lifecycle Staging logic (e.g. classifying active stages) and UI display comparison.

### 3.3 Target SHAP Interpretability Dictionary
Tabular predictions on `/predict/single` must translate complex features into plain descriptions using SHAP attributions:

| Feature ID | Feature Condition | Translated Human-Readable Risk Signal |
| :--- | :--- | :--- |
| **F670** | `F670 = 1` | "Prior regulatory watch-list flag active on account" |
| **F886** | `F886 >= 0.15` | "Unusual rapid channel-switching behavior detected" |
| **F3908** | `F3908 >= 0.70` | "High velocity in/out ratio (funds passing through rapidly)" |
| **F115** | `F115 >= 0.65` | "Elevated transaction ratio relative to customer history" |
| **F2082** | `F2082 = 0` | "Complete absence of standard retail banking behavior" |
| **F3889** | `F3889 == 'G365D'` | "Account is established dormant profile activated for laundering" |
| **F3891** | `F3891 == 'student'`| "High-vulnerability demographic profile matched (student mule)" |

---

## 4. Regulatory References & Auditing Procedures

MuleShield AI implements compliance anchoring to support regulatory audits:

### 4.1 goAML XML STR Declarations
When an account score fuses into a `CRITICAL` severity tier (composite score $\ge 80.0$), the backend automatically compiles an XML report compliant with FIU-IND (Financial Intelligence Unit - India) goAML schemas.
* **Details exported:** Account holder details, fused severity metrics, SHAP feature signals, and transactional lists.

### 4.2 Tamper-Proof Evidence Signatures
Every batch ingestion or automated STR execution yields a SHA-256 evidence signature (calculated over all ingested transactions and alerts).
* **Legal Anchoring:** This hash is saved to the PostgreSQL audit log `CaseAudit` database under timezone-naive UTC timestamps. This serves as digital evidence under Section 65B of the Indian Evidence Act.

---

## 5. Deployment & Integration Checklist

### 5.1 On-Premise Air-Gapped Security
To satisfy Public Sector Bank security protocols, MuleShield AI supports complete air-gapped on-premise execution with zero internet dependencies.
* **Local Database Instances:** PostgreSQL and Neo4j operate within a local Docker Compose network.
* **Offline ML Pipeline:** XGBoost inference operates locally using pre-loaded pickle files.
* **Fallback LLM Engine:** If primary cloud NVIDIA NIM endpoints are blocked, the platform fails back to Gemini or uses a local Ollama Llama 3 8B model.

### 5.2 Fresh Verification Checklist
Run these commands in order after deployment changes to verify platform stability:

```bash
# 1. Run local port diagnostics and model validation checks
python health_check.py

# 2. Run the unified unittest suite (with warning exceptions active)
venv\Scripts\python.exe -W error -m unittest discover -s tests
```
If both checks succeed, the platform is verified as stable.
