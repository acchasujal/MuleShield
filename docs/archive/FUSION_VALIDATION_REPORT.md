# Fusion Validation Report

Date: 2026-06-02
Phase: 1 - Dataset-Wide Fusion Validation
Scope: Audit and validation only. No lifecycle logic changes were implemented in this phase.

## Objective

Validate current Fusion v5 behavior against the prior score fusion model and assess whether score, severity, lifecycle, and STR decisions remain coherent across representative cohorts.

## Validation Inputs

Primary dataset:

- `data/boi/DataSet.csv`

Scenario dataset:

- `data/scenario_roundtrip.csv`

Comparison baseline:

- Previous composite formula: `((ml_score * 0.70) + (graph_score * 0.30)) * 100`
- Current Fusion v5 formula: `0.40 * profile + 0.40 * transaction + 0.20 * graph`

Assumptions used in current environment:

- Neo4j offline, so graph score falls back to ML score in baseline validation
- PostgreSQL offline, so audit writes are not part of validation success criteria

## Validation Results

### Dataset-Wide Severity Comparison

Previous scoring distribution:

- `LOW`: `9001`
- `MEDIUM`: `0`
- `HIGH`: `0`
- `CRITICAL`: `81`

Current Fusion v5 distribution:

- `LOW`: `9001`
- `MEDIUM`: `0`
- `HIGH`: `81`
- `CRITICAL`: `0`

Interpretation:

- Fusion v5 reduces the top-end severity of the 81 known high-risk accounts from `CRITICAL` to `HIGH`
- No low-risk account was incorrectly promoted into `MEDIUM+` in baseline dataset scoring
- The dataset remains bimodal in the current offline baseline: `9001 LOW`, `81 HIGH`

### Dataset-Wide Lifecycle Distribution

Current lifecycle distribution:

- `LEGITIMATE`: `9001`
- `ACTIVE_MULE`: `81`

Interpretation:

- Baseline lifecycle output aligns with baseline severity output across the dataset
- No baseline contradiction was found between `LOW` severity and non-legitimate lifecycle
- No baseline contradiction was found between `HIGH` severity and `LEGITIMATE` lifecycle

### Score Bound Validation

Observed score bounds:

- Previous formula minimum: `0.0`
- Previous formula maximum: `100.0`
- Fusion v5 minimum: `0.1`
- Fusion v5 maximum: `60.0`

Validation outcome:

- No score exceeded `100`
- No score fell below `0`
- Fusion v5 bounds are valid

### Classification Change Count

Accounts with changed severity label:

- `81`

Change pattern:

- All 81 changed accounts moved from previous `CRITICAL` to current `HIGH`
- No baseline `LOW` account changed into `MEDIUM+`

## Cohort Validation

Validation criteria for each cohort:

1. Risk score
2. Severity
3. Lifecycle stage
4. STR decision

### Cohort A - Legitimate Account Baseline

Account:

- `ACC05200000000009`

Observed output:

- Risk score: `0.1`
- Severity: `LOW`
- Lifecycle stage: `LEGITIMATE`
- STR decision: `False`

Result:

- Pass

### Cohort B - Known Mule Account Baseline

Account:

- `ACC05200000009002`

Observed output:

- Risk score: `60.0`
- Severity: `HIGH`
- Lifecycle stage: `ACTIVE_MULE`
- STR decision: `True`

Result:

- Pass

### Cohort C - Legitimate Account With Round-Trip Scenario

Account:

- `ACC05200000000009`

Observed output:

- Risk score: `40.0`
- Severity: `MEDIUM`
- Lifecycle stage: `LEGITIMATE`
- STR decision: `True`
- Transaction risk: `100.0`
- Triggering reasons: `cycle`, `layering`, `ml_anomaly`

Result:

- Partial fail

Reason:

- Risk score and severity increase appropriately
- STR decision increases appropriately
- Lifecycle stage does not increase appropriately and remains `LEGITIMATE`

### Cohort D - Known Mule Account With Round-Trip Scenario

Account:

- `ACC05200000009002`

Observed output:

- Risk score: `92.0`
- Severity: `CRITICAL`
- Lifecycle stage: `ACTIVE_MULE`
- STR decision: `True`
- Transaction risk: `80.0`
- Triggering reasons: `cycle`, `layering`

Result:

- Pass

## Focus Investigation: `ACC05200000000009`

Baseline behavior:

- Endpoint: `/predict/single`
- Risk score: `0.1`
- Severity: `LOW`
- Lifecycle: `LEGITIMATE`
- STR: `False`

Round-trip behavior:

- Endpoint: `/analyze`
- Risk score: `40.0`
- Severity: `MEDIUM`
- Lifecycle: `LEGITIMATE`
- STR: `True`

Conclusion:

- Fusion v5 is functioning correctly for risk escalation
- STR generation is functioning correctly for transaction-elevated severity
- Lifecycle staging is not aligned with transaction-elevated severity

## Contradiction Audit

Dataset baseline contradictions found:

- `0`

Scenario contradiction found:

- `ACC05200000000009` is the clearest live contradiction

Contradiction pattern:

- `MEDIUM` severity
- STR generated
- Lifecycle still `LEGITIMATE`

## Phase 1 Decision

### Fusion Score Validation

Status:

- Pass

Why:

- Bounds are valid
- Cohort risk escalation works
- Scenario-based transaction intelligence now affects the composite score

### Severity Validation

Status:

- Pass

Why:

- Severity tracks fusion score correctly
- Expected `MEDIUM` and `CRITICAL` cohort behavior appears under scenario pressure

### STR Validation

Status:

- Pass

Why:

- STR generation activates consistently for `MEDIUM+`

### Lifecycle Validation

Status:

- Partial fail

Why:

- Lifecycle remains profile-only and can contradict fusion-driven severity

## Recommended Lifecycle Alignment Changes

No lifecycle code changes were made in this phase.

Recommended changes before implementation:

- Keep Fusion v5 scoring as-is
- Keep current severity thresholds as-is
- Keep current STR threshold of `MEDIUM+` as-is
- Align lifecycle so a transaction-elevated `MEDIUM+` account no longer remains `LEGITIMATE`

Recommended policy:

- If current lifecycle is `LEGITIMATE`
- And fusion severity is `MEDIUM+`
- And transaction risk is greater than `0`

Then uplift lifecycle from `LEGITIMATE`

Recommended target stage:

- `UNDER_REVIEW` for `MEDIUM` cases driven by active transaction evidence
- `ACTIVE_MULE` for `HIGH` and `CRITICAL` cases unless a more specific lifecycle rule applies

Specific recommendation for `ACC05200000000009`:

- Current: `40.0 / MEDIUM / LEGITIMATE / STR=True`
- Recommended aligned behavior: `40.0 / MEDIUM / UNDER_REVIEW / STR=True`

## Files Modified In Phase 1

- `FUSION_VALIDATION_REPORT.md`
- `LIFECYCLE_DECISION_MATRIX.md`

## Validation Outcome

Phase 1 completed as an audit-only pass.

- Audit completed
- Dataset-wide validation completed
- Cohort-based validation completed
- Lifecycle decision matrix created
- No lifecycle logic changed

Stop point:

- Await approval before implementing any lifecycle alignment changes.
