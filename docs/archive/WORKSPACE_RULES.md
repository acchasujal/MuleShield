# WORKSPACE_RULES.md - Multi-Agent Safety & Consistency Framework

> **Anti-Collision, Backward-Compatibility, and System Integrity Guidelines for Cooperative AI Agents**  
> Last Updated: May 31, 2026  
> Purpose: Prevent merge conflicts, data corruption, and design drift when multiple agents work concurrently

---

## Overview

When multiple AI agents work simultaneously on different components, collisions and inconsistencies are inevitable without explicit rules. This document defines:

1. **File Ownership & Locking** - Which agent can modify which files
2. **Atomic Operations** - How to safely modify shared files
3. **Backward Compatibility** - How to maintain stability
4. **Conflict Resolution** - What to do when changes collide
5. **Rollback Procedures** - How to recover from mistakes

---

## Part 1: File Ownership & Modification Rights

### Tier 1: Exclusively Owned (Single Agent Writes)

Only the designated owner can modify these files. All other agents read-only.

| File | Owner | Reason | Read-Only Agents |
|------|-------|--------|-----------------|
| `context/AGENT_RULES.md` | Architecture Lead | Core coding standards; must be consistent | All others |
| `context/MASTER_CONTEXT.md` | Architecture Lead | Project mission/identity; rarely changes | All others |
| `architecture/DECISIONS.md` | Architecture Lead | ADRs are append-only historical records | All others |
| `architecture/SYSTEM_ARCHITECTURE.md` | Architecture Lead | System design is authoritative | All others |
| `context/PROJECT_STATE.md` | Project Manager | Current project state; single source of truth | All others |
| `sprints/CURRENT_SPRINT.md` | Project Manager | Sprint definition; managed by PM | All others |
| `sprints/SPRINT_HISTORY.md` | Project Manager | Historical records; append-only | All others |
| `tasks/TASK_QUEUE.md` | Project Manager | Backlog; PM has authority | All others |
| `tasks/COMPLETED_TASKS.md` | Project Manager | Completion records; append-only | All others |

**Rule 1.1: Exclusive Owner Right**
> Only the designated owner can execute WRITE operations (create, modify, delete) on Tier 1 files. All other agents must request changes through official channels (see Conflict Resolution, Part 5).

---

### Tier 2: Role-Owned with Shared Access

These files have a primary owner but can be modified by agents in related roles with explicit coordination.

| File | Primary Owner | Secondary Modifiers | Coordination Required |
|------|---------------|-------------------|---------------------|
| `architecture/API_CONTRACTS.md` | Backend Lead | Frontend Lead | Yes - before API changes |
| `architecture/DATABASE_SCHEMA.md` | Backend Lead | DevOps Lead | Yes - before schema changes |
| `architecture/ML_PIPELINE.md` | Data Science Lead | Backend Lead | Yes - model integration changes |
| `architecture/RISK_ENGINE.md` | Data Science Lead | Backend Lead | Yes - weight/threshold changes |
| `backend/app.py` | Backend Lead | Backend Developers | No - within team |
| `frontend/app.py` | Frontend Lead | Frontend Developers | No - within team |

**Rule 2.1: Explicit Coordination**
> Before modifying a Tier 2 file, the non-owner agent must:
> 1. Post a comment in the issue/PR explaining the change
> 2. Wait for acknowledgment from the primary owner
> 3. Link the change to the corresponding task in TASK_QUEUE.md

**Rule 2.2: Semantic Versioning**
> All Tier 2 file changes must include a version bump:
> ```markdown
> ---
> last_modified: 2026-05-31
> modified_by: Backend Developer
> version: 1.2.0  <!-- Bump if breaking change -->
> ---
> ```

---

### Tier 3: Collaborative Files (Open Writes)

These files can be modified by any agent, but must follow atomic operation rules (Part 2).

| File | Purpose | Atomic Unit |
|------|---------|------------|
| `context/DATASET_INTELLIGENCE.md` | Data features & stats | Per-feature block |
| `context/REFERENCE_DOCS.md` | Regulatory/compliance | Per-section (slides, Q&A, etc.) |
| `docs/reference/REFERENCE_DOCS.md` | External materials | Per-document type |
| `docs/archive/*` | Historical records | Per-file (append-only) |

**Rule 3.1: Atomic Modifications**
> Only modify one logical unit per change. For example, in DATASET_INTELLIGENCE.md:
> - ✅ Update one feature definition
> - ❌ Update 10 features in one write

---

### Tier 4: Task-Specific Files (Temporary Ownership)

Backend/Frontend developers can create and modify files within their module directories, but must respect contracts defined in architecture files.

| Directory | Owner | Rules |
|-----------|-------|-------|
| `/backend/*` | Backend Lead | Files must comply with API_CONTRACTS.md and DATABASE_SCHEMA.md |
| `/frontend/*` | Frontend Lead | Must call only endpoints defined in API_CONTRACTS.md |
| `/tests/*` | QA Lead | Must validate against TASK_QUEUE.md requirements |
| `/data/*` | Data Science Lead | Can add test data; existing data is immutable |

---

## Part 2: Atomic Operations & Consistency

### Atomic Unit Definition

An **atomic unit** is the smallest indivisible change that:
- Maintains file consistency
- Can be reviewed independently
- Doesn't break other components

**Rule 2.1: Single Responsibility Per Commit**
> Each file modification must address exactly one concern:
> ```
> ✅ "Add ML anomaly detector to fraud_detection.py"
> ✅ "Update RISK_ENGINE weights for cycle detection"
> ❌ "Fix bugs, add features, update docs" (too broad)
> ```

**Rule 2.2: File Format Consistency**
> All markdown files must maintain:
- Standard header hierarchy (# → ## → ###)
- Consistent table formatting
- Code blocks with language specification
- Links to related files using format: `[Link Text](path/to/file.md)`

**Rule 2.3: Never Partially Complete Operations**
> If you start modifying a file, finish the modification completely:
> ```
> ❌ Stage 1: Add new API endpoint definition (incomplete)
> ❌ Stage 2: (Awaiting approval from other agent)
> ✅ Complete: API endpoint + tests + documentation
> ```

**Rule 2.4: Batch-Write Strategy**
> For multiple related changes, batch them logically:
> ```
> ✅ Batch 1: API design (API_CONTRACTS.md)
> ✅ Batch 2: Implementation (backend/app.py)
> ✅ Batch 3: Testing (tests/test_api.py)
> ✅ Batch 4: Documentation (docs/API.md)
> ```

---

### Modification Locks

To prevent simultaneous writes to Tier 1 files, use this check-in system:

**Rule 2.5: Pre-Modification Check**
> Before modifying a Tier 1 file:
> 1. Read the current `last_modified` timestamp
> 2. Check if any other agent modified it in the past 5 minutes
> 3. If yes, wait before proceeding
> 4. If no, proceed and update the timestamp immediately

**Example: API_CONTRACTS.md Header**
```markdown
---
last_modified: 2026-05-31T14:32:00Z
modified_by: Backend Developer
modification_lock: None
---
```

---

## Part 3: Backward Compatibility

### API Contracts

**Rule 3.1: Never Break Existing Endpoints**
> - Existing request/response fields are immutable
> - New fields must be optional (nullable)
> - Deprecated fields can be marked but not removed

**Example:**
```python
# ✅ Backward compatible
class AnalyzeRequest(BaseModel):
    file: UploadFile
    advanced_options: Optional[dict] = None  # New optional field

# ❌ Breaking change
class AnalyzeRequest(BaseModel):
    file: UploadFile
    # Removed: filename parameter (breaks existing clients)
```

**Rule 3.2: Version API Changes**
> Changes to request/response must increment the API version:
> ```
> POST /v1/analyze  (current)
> POST /v2/analyze  (breaking changes)
> ```

### Database Schema

**Rule 3.3: Backward Compatible Migrations**
> Database changes must support dual-schema for at least 1 sprint:
> ```sql
> -- ✅ Safe: Add nullable column
> ALTER TABLE transactions ADD COLUMN risk_score FLOAT DEFAULT NULL;
> 
> -- ❌ Unsafe: Drop column
> ALTER TABLE transactions DROP COLUMN old_field;
> 
> -- ✅ Safe with migration: Rename column
> ALTER TABLE transactions ADD COLUMN new_name VARCHAR(255);
> -- Backfill from old_name
> -- Migration: Update application code
> -- Cleanup: Drop old_name
> ```

**Rule 3.4: Schema Versioning**
> All DATABASE_SCHEMA.md changes must include migration scripts:
> ```markdown
> ## Version 2.1.0 (2026-05-31)
> - Added: risk_score column to transactions table
> - Migration: migrations/002_add_risk_score.sql
> - Rollback: migrations/002_rollback.sql
> ```

### Configuration & Constants

**Rule 3.5: Never Hardcode Magic Numbers**
> All thresholds, weights, limits must be in AGENT_RULES.md or config:
> ```python
> # ❌ Bad: Hardcoded weight
> cycle_weight = 50
> 
> # ✅ Good: Load from config
> from config import SIGNAL_WEIGHTS
> cycle_weight = SIGNAL_WEIGHTS['cycle']
> ```

---

## Part 4: Conflict Prevention

### Pre-Emptive Coordination

**Rule 4.1: Announce Work Upfront**
> Before starting work on shared files, post an announcement:
> ```
> [Task #123] Backend Dev starting API redesign
> - Files affected: API_CONTRACTS.md, app.py
> - Estimated duration: 2 hours
> - Blocker: Awaiting approval from Architecture Lead
> - Do not modify these files until completion
> ```

**Rule 4.2: Regular Synchronization**
> Every 4 hours, compare current code state with documented state:
> ```
> If documentation ≠ code:
>   1. Identify discrepancy
>   2. Update documentation immediately
>   3. Log reason in file header comment
> ```

**Rule 4.3: Conflict Detection Script**
> Before pushing changes, run verification:
> ```bash
> # Check for uncommitted changes
> git status
> 
> # Check for timestamp collisions in Tier 1 files
> grep "last_modified" context/*.md | sort
> 
> # Verify no duplicate API endpoints
> grep "POST\|GET\|PUT" architecture/API_CONTRACTS.md | sort
> ```

---

### Simultaneous Modification Scenarios

**Scenario 1: Two agents modify TASK_QUEUE.md simultaneously**

```
Agent A (at 10:00): Adds Task #101
Agent B (at 10:01): Adds Task #102

Problem: If sequential writes fail, one change is lost
Solution: Use line-range locking
- Task #101-#150: Reserved for Backend Dev
- Task #151-#200: Reserved for Frontend Dev
```

**Scenario 2: Backend Dev & Data Scientist both update RISK_ENGINE.md**

```
Backend Dev: Wants to change cycle_weight from 50 → 60
Data Scientist: Wants to change ml_weight from 40 → 45

Solution:
1. Lock file for 15 minutes (first agent wins)
2. Second agent waits & reviews first change
3. Second agent makes change after first completes
4. Both changes logged with reasons
```

**Scenario 3: Frontend & Backend both call new API endpoint**

```
Frontend wants to call: POST /analyze-batch (not yet implemented)
Backend Dev is still implementing it

Solution:
1. Design API_CONTRACTS.md first (coordination)
2. Backend implements endpoint
3. Frontend calls endpoint
4. Never develop in parallel on same component
```

---

## Part 5: Conflict Resolution Process

### When Conflicts Occur

**Rule 5.1: Escalation Path**
```
Level 1: Two agents discuss via comment
  If unresolved after 10 minutes → Level 2
  
Level 2: Architecture Lead as referee
  Reviews both perspectives
  Makes authoritative decision
  Logs decision in architecture/DECISIONS.md
  
Level 3: Project Manager/Team Lead
  Called if Architecture Lead is unavailable
  Makes binding decision
  Documents escalation reason
```

**Rule 5.2: Conflict Log**
> All conflicts must be logged in a new section of PROJECT_STATE.md:
> ```markdown
> ## Active Conflicts
> 
> ### Conflict #1: API_CONTRACTS.md weights
> - Raised by: Data Scientist (May 31 14:00)
> - Issue: Wants ML weight 40 → 45
> - Blocked: Backend Dev testing current 40
> - Resolution: Waiting for Backend test completion
> - Escalated: No (resolved via discussion)
> ```

---

### Rollback Procedures

**Rule 5.3: Always Maintain Rollback Points**
> Before any major change, create a rollback snapshot:
> ```bash
> # Create snapshot before modifying API_CONTRACTS.md
> git commit -m "SNAPSHOT: Before API redesign (issue #123)"
> git tag snapshot/api-redesign-20260531
> ```

**Rule 5.4: Emergency Rollback**
> If a change breaks the system:
> 1. Immediately revert to last working version
> 2. Document what broke and why
> 3. Discuss with Architecture Lead before re-attempting

**Rule 5.5: Post-Conflict Documentation**
> After resolving a conflict, update DECISIONS.md:
> ```markdown
> ## ADR-7: RISK_ENGINE Weight Prioritization
> **Decision:** ML_ANOMALY weight stays at 40
> **Context:** Data Scientist requested increase to 45
> **Rationale:** Backend performance tests show current weight sufficient
> **Resolved by:** Architecture Lead (May 31 14:30)
> **Status:** Accepted
> ```

---

## Part 6: Change Review & Validation

### Mandatory Review Checklist

Before committing any change, complete this checklist:

**For Tier 1 Files (Owner Only):**
```
☐ Change aligns with MASTER_CONTEXT.md mission
☐ Change documented with reason in file header
☐ Timestamp updated to current UTC time
☐ No breaking changes introduced
☐ Backward compatibility verified
☐ Other teams notified if affecting their work
☐ Rollback plan documented
```

**For Tier 2 Files (Coordinated):**
```
☐ Primary owner acknowledged the change
☐ API_CONTRACTS.md or DATABASE_SCHEMA.md updated first
☐ Version number incremented
☐ All related files updated in same batch
☐ Tests written before code changes
☐ Integration tested with dependent modules
☐ Rollback tested
```

**For Tier 3 Files (Collaborative):**
```
☐ Only one logical unit modified
☐ Change atomic and reversible
☐ No partial changes left incomplete
☐ File format consistent with rest of document
☐ No duplicate information elsewhere
☐ Links to related files updated
```

---

## Part 7: Concurrent Agent Rules

### Safe Parallelization

**Rule 7.1: Non-Conflicting Tasks Can Run in Parallel**
```
✅ Parallel: Frontend updates app.py + Backend updates app.py
  (Different functions, no merge conflict)

✅ Parallel: Backend API endpoint + Data Scientist trains ML
  (Independent files, no dependency)

❌ Sequential: Backend API contract + Frontend implementation
  (Frontend depends on completed API contract)
```

**Rule 7.2: Task Dependencies Must Be Explicit**
> In TASK_QUEUE.md, mark dependencies clearly:
> ```markdown
> ### Task #101: Design API contract
> - Status: In Progress (Backend Dev)
> - Blocker: None
> - Blocks: #102, #103, #104
> 
> ### Task #102: Implement API endpoint
> - Status: Blocked
> - Blocker: Task #101
> - Blocked By: #101
> ```

**Rule 7.3: Maximum 3 Concurrent Agents**
> Beyond 3 simultaneous modifications, collision risk becomes too high.
> If more work exists, queue tasks sequentially.

---

## Part 8: Documentation Requirements

### Every File Modification Must Include

**Header Comment (All Files):**
```markdown
---
last_modified: 2026-05-31T14:32:00Z
modified_by: Backend Developer
version: 1.2.0
reason: Added ML anomaly endpoint
issue_link: #123
---
```

**Inline Comments (Code Changes):**
```python
# Added 2026-05-31: ML anomaly detection
# Issue: #123 - Improve fraud signal detection
# Author: Backend Developer
# Validation: Unit tests in test_ml_anomaly.py
def ml_anomaly_detector(df):
    """Detect ML-based anomalies using Isolation Forest."""
    ...
```

**Markdown Change Log (Architecture Files):**
```markdown
## Change Log

### 2026-05-31: Added ML anomaly weight
- **Author:** Data Scientist
- **Issue:** #123
- **Change:** ML_ANOMALY weight 40 → 45
- **Validation:** Tested with 10K transactions, AUC improved 2%
- **Rollback:** Revert weight in Risk Engine if performance degrades
```

---

## Part 9: Emergency Procedures

### System In Critical State

If the system is in an unstable state and multiple fixes are needed:

**Rule 9.1: Emergency Freeze**
> 1. Project Manager declares EMERGENCY FREEZE in PROJECT_STATE.md
> 2. Only Architecture Lead can approve new changes
> 3. All agents pause work except critical fixes
> 4. Freeze lasts until system is stable (min 30 min)

**Rule 9.2: Critical Hotfix Process**
> For critical production bugs:
> 1. Identify the bug's root cause
> 2. Create minimal fix (single atomic change)
> 3. Get Architecture Lead approval (1 minute max wait)
> 4. Apply fix to all affected files immediately
> 5. Write comprehensive test to prevent regression
> 6. Document in COMPLETED_TASKS.md with issue link

---

## Verification Checklist

- [x] All file tiers are defined with clear ownership
- [x] Atomic operation rules are documented
- [x] Backward compatibility requirements are explicit
- [x] Conflict resolution paths are clear
- [x] Rollback procedures are documented
- [x] Concurrent agent guidelines are specific
- [x] No ambiguity in modification rights
- [x] All rules are enforceable by agents
- [x] Emergency procedures are defined

---

## Document History

| Date | Change | Author |
|------|--------|--------|
| 2026-05-31 | Initial WORKSPACE_RULES creation | AI Assistant |
| TBD | First enforcement cycle | Architecture Lead |

