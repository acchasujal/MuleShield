# Lifecycle Alignment Report

Date: 2026-06-02
Phase: 1 - Lifecycle Alignment Implementation

## Objective

Introduce the `UNDER_REVIEW` lifecycle stage and align lifecycle output with fusion-aware transaction escalation without overriding the existing profile-driven stages.

## Implemented Rule

Applied rule:

- If current lifecycle is `LEGITIMATE`
- And fusion severity is `MEDIUM`, `HIGH`, or `CRITICAL`
- And transaction risk is greater than `0`

Then:

- `LEGITIMATE` -> `UNDER_REVIEW`

Preserved existing profile-driven stages:

- `NEWLY_RECRUITED`
- `ACTIVE_MULE`
- `BEING_FLUSHED`
- `DORMANT`

Explicitly not implemented:

- No direct promotion of `MEDIUM` accounts to `ACTIVE_MULE`

## Files Modified

- `backend/risk_scoring.py`
- `backend/app.py`
- `backend/routers/ml_predict.py`
- `backend/routers/i4c_webhook.py`
- `frontend/utils/constants.py`
- `frontend/components/account_inspector.py`
- `frontend/components/graph_view.py`
- `frontend/components/lifecycle_view.py`

## Backend Changes

### Central Alignment Helper

Added `align_lifecycle_stage()` to `backend/risk_scoring.py`.

Behavior:

- Returns `UNDER_REVIEW` only for transaction-elevated `MEDIUM+` cases currently labeled `LEGITIMATE`
- Leaves all existing profile-driven stages unchanged

### `/analyze`

Updated `backend/app.py` so the analyzed account lifecycle is aligned after:

- fusion score calculation
- severity assignment
- transaction risk calculation

This is the key path that changes `ACC05200000000009` in the round-trip scenario.

### `/predict/single`

Updated `backend/routers/ml_predict.py` to call the same helper with `txn_score = 0.0`.

Effect:

- Baseline single-account behavior is unchanged
- Shared logic remains centralized and consistent

### `/predict/batch`

Updated batch prediction to call the same helper with `txn_score = 0.0`.

Effect:

- Baseline batch behavior is unchanged

### `/ingest-i4c`

Updated the I4C route to use the same helper with `txn_score = 0.0`.

Effect:

- No behavior change in current I4C scoring
- Keeps lifecycle alignment logic centralized

## Frontend Changes

Added display support for `UNDER_REVIEW`:

- lifecycle color mapping
- graph color mapping
- lifecycle timeline explanation

Also updated the account inspector fusion breakdown text to match the current 40/40/20 scoring formula and the current `MEDIUM+` STR trigger threshold.

## Validation Status

Runtime validation was partially blocked in this turn because further shell execution became unavailable after the session hit its escalation approval limit.

Because of that, the post-change outcomes below are code-path validated by implementation inspection, not re-executed end-to-end in this turn.

## Required Outcome Matrix

### A. `ACC05200000000009` baseline

Expected outcome:

- `LOW`
- `LEGITIMATE`
- `STR = False`

Code-path result after implementation:

- Unchanged

Why:

- `/predict/single` passes `transaction_risk = 0.0`
- Alignment rule does not activate

### B. `ACC05200000000009` round-trip scenario

Expected outcome:

- `MEDIUM`
- `UNDER_REVIEW`
- `STR = True`

Code-path result after implementation:

- Aligned to expected

Why:

- `/analyze` computes `transaction_risk = 100.0`
- Severity remains `MEDIUM`
- Current stage is `LEGITIMATE`
- Alignment helper upgrades lifecycle to `UNDER_REVIEW`
- Existing `MEDIUM+` STR trigger remains active

### C. `ACC05200000009002` baseline

Expected outcome:

- `HIGH`
- `ACTIVE_MULE`

Code-path result after implementation:

- Unchanged and aligned to expected

Why:

- Current stage is already profile-driven `ACTIVE_MULE`
- Alignment helper does not override it

### D. `ACC05200000009002` round-trip scenario

Expected outcome:

- `CRITICAL`
- `ACTIVE_MULE`

Code-path result after implementation:

- Unchanged and aligned to expected

Why:

- Current stage is already `ACTIVE_MULE`
- Alignment helper only upgrades `LEGITIMATE`

## Risk Assessment

Low implementation risk:

- Alignment is centralized in one helper
- Existing profile-driven stages are preserved
- No scoring thresholds changed
- No STR thresholds changed

Primary residual risk:

- Runtime validation should be rerun once shell execution is available again, to confirm there are no integration mistakes outside the inspected code paths

## Rollback Plan

If the lifecycle alignment needs to be reverted:

- Remove `align_lifecycle_stage()` usage from the backend routes
- Remove the helper from `backend/risk_scoring.py`
- Remove `UNDER_REVIEW` display mappings from the frontend

## Stop Point

Implementation is complete.

Await approval before beginning Phase 2 - database recovery.
