# AGENT_LOADING_STRATEGY.md
_Use this to determine which context files to load for each task type. Minimize token usage._

---

## LOADING RULES

**Always load:** `AGENT_RULES.md` (identity + architecture invariants)  
**Load by task type:** See table below  
**Never load by default:** `REFERENCE_DOCS.md` (load only for PPT, demo, Q&A tasks)

---

## TASK-TYPE LOADING MAP

### ML / Data Science Task
_(T1, T6, T8, T12, T13 — feature engineering, model training, metrics)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - DATASET_INTELLIGENCE.md (~700 tokens)
  - ARCHITECTURE.md         (~700 tokens) — for RiskResponse schema

SKIP:
  - MASTER_CONTEXT.md (redundant for pure ML work)
  - REFERENCE_DOCS.md
  - CURRENT_SPRINT.md (unless coordinating with others)

TOTAL: ~1,900 tokens of context
```

**Example prompt prefix:**
```
You are building the ML pipeline for MuleShield AI (BOI PS-2 hackathon).
[paste AGENT_RULES.md]
[paste DATASET_INTELLIGENCE.md]
Task: [specific task description]
```

---

### FastAPI Backend Task
_(T2, T3, T7 — endpoints, score fusion, STR trigger)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - ARCHITECTURE.md         (~700 tokens)
  - MASTER_CONTEXT.md       (~600 tokens) — for success criteria context

SKIP:
  - DATASET_INTELLIGENCE.md (paste only the RiskResponse schema if needed)
  - REFERENCE_DOCS.md

TOTAL: ~1,800 tokens of context
```

**Example prompt prefix:**
```
You are building FastAPI endpoints for MuleShield AI.
[paste AGENT_RULES.md]
[paste ARCHITECTURE.md]
Current file: [paste the actual file being modified]
Task: [specific task]
```

---

### Neo4j / Graph Task
_(Graph schema updates, Cypher queries, ML-graph integration)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - ARCHITECTURE.md         (~700 tokens) — Graph Intelligence section

SKIP:
  - DATASET_INTELLIGENCE.md
  - MASTER_CONTEXT.md
  - REFERENCE_DOCS.md

TOTAL: ~1,200 tokens of context
```

**Note for Neo4j tasks:** Also paste the existing `graph_service.py` as direct context. The graph schema (node labels, relationship types) is not in context docs — it lives in the code.

---

### React Frontend Task
_(T4, T5, T9, T10, T11 — components, pages, UI)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - ARCHITECTURE.md         (~700 tokens) — API endpoints + RiskResponse schema

ALSO PASTE:
  - One existing React component as style reference (critical for design consistency)
  - Relevant API endpoint response JSON (so agent knows exact data shape)

SKIP:
  - DATASET_INTELLIGENCE.md
  - MASTER_CONTEXT.md
  - REFERENCE_DOCS.md

TOTAL: ~1,200 tokens + reference component
```

**Critical:** Always include a reference component. Without it, agents default to generic Tailwind patterns that won't match your design system.

---

### Integration / Full-Stack Task
_(T14, T15 — demo scenario, end-to-end testing)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - MASTER_CONTEXT.md       (~600 tokens)
  - ARCHITECTURE.md         (~700 tokens)
  - CURRENT_SPRINT.md       (~300 tokens)

SKIP:
  - DATASET_INTELLIGENCE.md
  - REFERENCE_DOCS.md

TOTAL: ~2,100 tokens of context
```

---

### Bug Fix
_(Any layer — debugging a specific broken behavior)_

```
LOAD:
  - AGENT_RULES.md          (~500 tokens)
  - Relevant section of ARCHITECTURE.md only (paste just the relevant section)

ALSO PASTE:
  - The broken file(s) directly
  - The error message / stack trace
  - Expected vs actual behavior

SKIP:
  - Everything else

TOTAL: ~500 tokens + broken code
```

---

### PPT / Demo / Strategy Task
_(Slide updates, demo script prep, Q&A practice)_

```
LOAD:
  - MASTER_CONTEXT.md       (~600 tokens)
  - REFERENCE_DOCS.md       (~1,500 tokens) — PPT blueprint, demo scripts, Q&A

SKIP:
  - AGENT_RULES.md
  - ARCHITECTURE.md
  - DATASET_INTELLIGENCE.md

TOTAL: ~2,100 tokens of context
```

---

## TOKEN BUDGET REFERENCE

| File | Est. Tokens |
|---|---|
| MASTER_CONTEXT.md | ~600 |
| ARCHITECTURE.md | ~700 |
| DATASET_INTELLIGENCE.md | ~700 |
| CURRENT_SPRINT.md | ~300 |
| TASK_QUEUE.md | ~600 |
| AGENT_RULES.md | ~500 |
| REFERENCE_DOCS.md | ~1,500 |
| **All files total** | **~4,900** |
| **Original HTML files** | **~50,000+** |
| **Reduction** | **~90%** |

---

## MULTI-AGENT SESSION RULES

When running multiple agents in parallel (e.g., Vikram on T2, Sujal on T4 simultaneously):

1. **Before starting:** Both agents load `AGENT_RULES.md` + their task-specific files
2. **Before T4 starts:** Vikram must commit T2's `RiskResponse` schema to `ARCHITECTURE.md` so Sujal's agent knows the exact JSON shape
3. **After T3:** Update `CURRENT_SPRINT.md` to mark T3 complete and unblock T7
4. **Feature list changes:** If Vikram changes `final_metadata.json`, post a note — Sujal's frontend agent must reload `ARCHITECTURE.md`

---

## LOADING CHECKLIST FOR NEW SESSION

Before pasting context to any agent, check:
- [ ] Is the task type identified? (ML / Backend / Frontend / Graph / Integration / PPT)
- [ ] Have I loaded only the relevant files per this strategy?
- [ ] Have I pasted the actual current file being modified (not just context docs)?
- [ ] Have I included the specific error or task description (not vague)?
- [ ] For frontend tasks: have I included a style reference component?
