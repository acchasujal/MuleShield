"""
MuleShield AI — Score Fusion Engine (Fusion v5)
Computes composite risk scores from ML, graph, and transaction signals.
No model loading. No ML inference.
"""

# ---------------------------------------------------------------------------
# Fusion v5 Weights — frozen, never modify without architecture board approval
# ---------------------------------------------------------------------------
PROFILE_WEIGHT     = 0.40
TRANSACTION_WEIGHT = 0.40
GRAPH_WEIGHT       = 0.20

# ---------------------------------------------------------------------------
# Signal weights for transaction-based scoring
# ---------------------------------------------------------------------------
SIGNAL_WEIGHTS = {
    "cycle":       50,
    "layering":    30,
    "structuring": 20,
    "velocity":    25,
    "anomaly":     35,
    "dormant":     20,
    "ml_anomaly":  40,
}


def calculate_transaction_score(reasons: list[str]) -> float:
    """Calculate a normalized 0–100 transaction score from matched signal names.

    Args:
        reasons: List of matched signal names (e.g. ["cycle", "velocity"]).

    Returns:
        Clamped transaction score in [0, 100].
    """
    score = 0.0
    for r in reasons:
        score += SIGNAL_WEIGHTS.get(r, 0.0)
    return min(score, 100.0)


def calculate_composite_risk(
    ml_score: float,
    graph_score: float | None,
    txn_score: float = 0.0,
) -> float:
    """Fuse tabular ML score, graph centrality score, and transaction score (Fusion v5).

    Formula:
        composite = clamp(
            (ml_score_pct  × 0.40)
          + (txn_score     × 0.40)
          + (graph_pct     × 0.20),
            0, 100
        )

    If graph_score is None, ml_score is used as the graph component fallback.

    Args:
        ml_score:    Raw XGBoost probability [0.0, 1.0].
        graph_score: Normalized Neo4j centrality [0.0, 1.0] or None.
        txn_score:   Pre-computed transaction signal score [0, 100].

    Returns:
        Rounded composite risk score [0.0, 100.0].
    """
    ml_val    = (ml_score or 0.0) * 100.0
    graph_val = (ml_score if graph_score is None else (graph_score or 0.0)) * 100.0

    fused   = (ml_val * PROFILE_WEIGHT) + (txn_score * TRANSACTION_WEIGHT) + (graph_val * GRAPH_WEIGHT)
    clamped = min(max(fused, 0.0), 100.0)
    rounded = round(clamped, 1)
    return 0.1 if clamped > 0.0 and rounded == 0.0 else rounded


def assign_tier(score: float) -> str:
    """Assign risk severity tier from composite score.

    Tiers:
        score ≥ 80.0      → CRITICAL
        score in [60, 80) → HIGH
        score in [40, 60) → MEDIUM
        score < 40        → LOW

    Args:
        score: Composite risk score [0, 100].

    Returns:
        Severity tier string.
    """
    if score >= 80.0:
        return "CRITICAL"
    if score >= 60.0:
        return "HIGH"
    if score >= 40.0:
        return "MEDIUM"
    return "LOW"


def align_lifecycle_stage(current_stage: str, severity: str, transaction_risk: float) -> str:
    """Apply fusion-aware lifecycle alignment without overriding profile-driven stages.

    If the ML profile produced LEGITIMATE but the fusion score is elevated and
    there is transaction evidence, escalate to UNDER_REVIEW.

    Args:
        current_stage:    Stage from lifecycle_engine.classify_mule_stage().
        severity:         Tier from assign_tier().
        transaction_risk: Transaction signal score (0–100).

    Returns:
        Final lifecycle stage string.
    """
    stage = (current_stage or "LEGITIMATE").upper().replace(" ", "_")
    sev   = (severity or "LOW").upper()
    txn   = transaction_risk or 0.0

    if stage == "LEGITIMATE" and sev in {"MEDIUM", "HIGH", "CRITICAL"} and txn > 0.0:
        return "UNDER_REVIEW"
    return stage
