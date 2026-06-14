"""
MuleShield-AI — Risk Scoring Engine (backward-compat facade)

All scoring logic now lives in backend/ml/score_fusion.py.
This module re-exports everything unchanged so existing callers
(`from backend.risk_scoring import ...`) continue to work without any
modification.
"""

from backend.ml.score_fusion import (  # noqa: F401 — re-export
    PROFILE_WEIGHT,
    TRANSACTION_WEIGHT,
    GRAPH_WEIGHT,
    SIGNAL_WEIGHTS,
    calculate_transaction_score,
    derive_behavioral_txn_score,
    calculate_composite_risk,
    assign_tier,
    align_lifecycle_stage,
)

# Legacy function kept for /analyze endpoint compatibility
def calculate_risk(account: str, signals: dict) -> tuple:
    """Score an account against all detected fraud signals.

    Args:
        account:  Account ID to evaluate.
        signals:  Dict of {signal_name: set_of_flagged_accounts}.

    Returns:
        (score, severity, reasons) tuple.
    """
    score = 0
    reasons = []

    for signal, accounts in signals.items():
        if account in accounts:
            score += SIGNAL_WEIGHTS.get(signal, 0)
            reasons.append(signal)

    if score >= 70:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity, reasons
