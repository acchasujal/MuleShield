# Lifecycle Decision Matrix

Date: 2026-06-02
Phase: 1 - Dataset-Wide Fusion Validation
Scope: Current implemented decision logic plus recommended alignment changes. No lifecycle logic was modified in this phase.

## Current Decision Sources

Current runtime decisions are split across two separate engines:

- Risk score and severity come from fusion scoring in `backend/risk_scoring.py`
- Lifecycle stage comes from `MLService.classify_mule_stage()` in `backend/ml_service.py`
- STR generation comes from severity checks in `backend/app.py` and `backend/routers/ml_predict.py`

Important implementation fact:

- Lifecycle classification currently uses `risk_score = ml_probability * 100`
- Lifecycle classification does not use fusion score
- Lifecycle classification does not use transaction score
- Lifecycle classification does not use graph score

This is the reason a scenario account can become `MEDIUM` in `/analyze` while still remaining `LEGITIMATE`.

## Score Thresholds

### Transaction Heuristic Weights

- `cycle`: `50`
- `layering`: `30`
- `structuring`: `20`
- `velocity`: `25`
- `anomaly`: `35`
- `dormant`: `20`
- `ml_anomaly`: `40`

Transaction score behavior:

- Sum matched signal weights
- Clamp to `100.0`

### Fusion Weights

- Profile weight: `0.40`
- Transaction weight: `0.40`
- Graph weight: `0.20`

Fusion formula:

- `composite_score = clamp((ml_score_pct * 0.40) + (txn_score * 0.40) + (graph_score_pct * 0.20), 0, 100)`

Low-end display guard:

- If composite score is nonzero but rounds to `0.0`, return `0.1`

## Severity Thresholds

Severity is currently assigned from fusion score:

- `CRITICAL`: `score >= 80.0`
- `HIGH`: `60.0 <= score < 80.0`
- `MEDIUM`: `40.0 <= score < 60.0`
- `LOW`: `score < 40.0`

## Current Lifecycle Transitions

Lifecycle stage is currently assigned from static profile features plus raw ML risk, not fusion risk.

### `NEWLY_RECRUITED`

Assigned when:

- `F3889` is `L7D` or `L90D`, or encoded values `1` or `2`
- Raw ML risk score is `>= 60.0`

### `ACTIVE_MULE`

Assigned when:

- `F3912 == 1.0`
- `F670 > 0.15`

Fallback assignment also sets:

- `ACTIVE_MULE` when raw ML risk score is `>= 60.0`

### `BEING_FLUSHED`

Assigned when:

- `F115 > 0.70`
- `F2082 == 0.0`

### `DORMANT`

Assigned when:

- `F3889 == G365D` or encoded value `4`
- Raw ML risk score is `>= 40.0` and `< 60.0`

### `LEGITIMATE`

Assigned when none of the above rules match and raw ML risk score is `< 60.0`

## STR Trigger Thresholds

Current STR behavior is severity-driven, not lifecycle-driven.

STR generation happens when:

- `severity in ["MEDIUM", "HIGH", "CRITICAL"]`

Action mapping:

- `CRITICAL` -> `AUTO_FREEZE`
- `MEDIUM` or `HIGH` -> `INVESTIGATOR_QUEUED`

Current implication:

- An account can be `LEGITIMATE` and still trigger STR generation if fusion severity is `MEDIUM+`

## Cohort Evaluation Matrix

### A. Legitimate Account Baseline

Account:

- `ACC05200000000009`

Observed result:

- Risk score: `0.1`
- Severity: `LOW`
- Lifecycle stage: `LEGITIMATE`
- STR decision: `False`

Assessment:

- Internally consistent

### B. Known Mule Account Baseline

Account:

- `ACC05200000009002`

Observed result:

- Risk score: `60.0`
- Severity: `HIGH`
- Lifecycle stage: `ACTIVE_MULE`
- STR decision: `True`

Assessment:

- Internally consistent

### C. Legitimate Account in Round-Trip Scenario

Account:

- `ACC05200000000009`

Observed result:

- Risk score: `40.0`
- Severity: `MEDIUM`
- Lifecycle stage: `LEGITIMATE`
- STR decision: `True`
- Transaction signals: `cycle`, `layering`, `ml_anomaly`
- Transaction risk: `100.0`

Assessment:

- Not internally consistent
- Fusion risk and STR behavior both treat the account as suspicious
- Lifecycle still labels the account `LEGITIMATE`

### D. Known Mule Account in Round-Trip Scenario

Account:

- `ACC05200000009002`

Observed result:

- Risk score: `92.0`
- Severity: `CRITICAL`
- Lifecycle stage: `ACTIVE_MULE`
- STR decision: `True`
- Transaction signals: `cycle`, `layering`
- Transaction risk: `80.0`

Assessment:

- Internally consistent

## Decision On The Medium Threshold Question

Question investigated:

- Should lifecycle staging change when risk crosses the `MEDIUM` threshold?

Decision:

- Not for every `MEDIUM` score in isolation
- Yes when `MEDIUM` is reached through active transaction intelligence and the account is still labeled `LEGITIMATE`

Reasoning:

- A pure score threshold alone is too coarse because some `MEDIUM` results may come from profile-only behavior
- The current inconsistency appears specifically when transaction evidence pushes fusion severity to `MEDIUM+`
- In that situation, keeping lifecycle at `LEGITIMATE` conflicts with both the severity and the STR decision

## Recommended Lifecycle Alignment Changes

These are recommendations only. No code changes were made in this phase.

### Recommended Principle

Lifecycle should remain explainable but must not contradict fusion severity when transaction evidence is materially suspicious.

### Recommended Alignment Rule

If all of the following are true:

- Fusion severity is `MEDIUM` or higher
- Transaction risk is greater than `0`
- Current lifecycle stage is `LEGITIMATE`

Then lifecycle should be uplifted away from `LEGITIMATE`.

### Recommended Uplift Behavior

Recommended minimum safe change:

- Introduce a scenario-aware lifecycle stage such as `UNDER_REVIEW`

Recommended stronger change:

- `MEDIUM` with transaction risk `> 0` -> `UNDER_REVIEW`
- `HIGH` or `CRITICAL` with transaction risk `> 0` -> `ACTIVE_MULE`, unless a more specific profile rule maps to `NEWLY_RECRUITED`, `BEING_FLUSHED`, or `DORMANT`

### Why `UNDER_REVIEW` Is Preferred For Medium

- It avoids automatically calling every transaction-elevated account a confirmed mule
- It resolves the contradiction with `LEGITIMATE`
- It stays aligned with current STR generation and investigator workflow

### Specific Recommendation For `ACC05200000000009`

Current state:

- `40.0`
- `MEDIUM`
- `LEGITIMATE`
- STR generated

Recommended aligned state:

- Keep severity at `MEDIUM`
- Keep STR decision as `True`
- Change lifecycle from `LEGITIMATE` to `UNDER_REVIEW`

## Approval Gate

Phase 1 output recommendation:

- Approve lifecycle alignment work only after confirming whether the project wants a new intermediate stage such as `UNDER_REVIEW`, or prefers direct promotion to `ACTIVE_MULE` for transaction-elevated `MEDIUM+` cases.
