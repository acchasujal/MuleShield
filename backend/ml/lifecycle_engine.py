"""
MuleShield AI — Lifecycle Staging Engine
Determines mule account lifecycle stage from raw features and risk score.
No ML inference. No score computation.
"""

import logging

logger = logging.getLogger("muleshield.ml.lifecycle")


def classify_mule_stage(raw_features: dict, risk_score: float) -> str:
    """Classify mule lifecycle stage using feature-driven rule engine.

    Rules are evaluated in priority order — first match wins.

    Stage rules:
        1. NEWLY_RECRUITED — Account age L7D/L90D with high risk (≥60)
        2. ACTIVE_MULE     — Prior alert flag (F3912=1) + regulatory hit (F670>0.15)
        3. BEING_FLUSHED   — High transaction ratio (F115>0.70) + no consumer banking (F2082=0)
        4. DORMANT         — Account age G365D with moderate risk (40–60)
        5. ACTIVE_MULE     — Catchall for any score ≥ 60
        6. LEGITIMATE      — Default (score < 60, no rule matched)

    Args:
        raw_features: Raw feature dict (pre-preprocessing, with string categoricals).
        risk_score:   ML probability × 100 (0–100 scale).

    Returns:
        Lifecycle stage string: one of NEWLY_RECRUITED, ACTIVE_MULE, BEING_FLUSHED,
        DORMANT, LEGITIMATE, or UNKNOWN (on error).
    """
    try:
        age_bucket = raw_features.get("F3889", "")
        # Prior alerting warning flag (F3912) used strictly in post-inference staging
        prior_flag  = float(raw_features.get("F3912", 0) or 0)
        regulatory  = float(raw_features.get("F670", 0) or 0)
        trans_ratio = float(raw_features.get("F115", 0) or 0)
        absent_bank = float(raw_features.get("F2082", 1) or 1)

        # Stage 1: Newly Recruited Account
        # Young account age (L7D or L90D) showing immediate high risk
        if age_bucket in ["L7D", "L90D"] or age_bucket in [1, 2]:
            if risk_score >= 60.0:
                return "NEWLY_RECRUITED"

        # Stage 2: Active Mule Account
        # Account has active legacy alert (F3912) and regulatory watch list hits
        if prior_flag == 1.0 and regulatory > 0.15:
            return "ACTIVE_MULE"

        # Stage 3: Being Flushed (Proceeds Dispersal)
        # High frequency transaction ratio coupled with complete lack of normal banking (F2082 == 0)
        if trans_ratio > 0.70 and absent_bank == 0.0:
            return "BEING_FLUSHED"

        # Stage 4: Dormant Account Reactivated
        # Account age is greater than 365 Days (G365D), moderate risk
        if age_bucket == "G365D" or age_bucket == 4:
            if 40.0 <= risk_score < 60.0:
                return "DORMANT"

        return "ACTIVE_MULE" if risk_score >= 60.0 else "LEGITIMATE"

    except Exception as exc:
        logger.error(f"Error classifying mule stage: {exc}")
        return "UNKNOWN"
