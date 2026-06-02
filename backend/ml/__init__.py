"""
MuleShield AI — ML Package
Modular ML components for inference, explainability, feature lookup,
lifecycle staging, and score fusion.
"""

from .predictor import MLPredictor
from .shap_engine import SHAPEngine
from .feature_lookup import lookup_account_features
from .lifecycle_engine import classify_mule_stage
from .score_fusion import (
    calculate_composite_risk,
    calculate_transaction_score,
    assign_tier,
    align_lifecycle_stage,
    SIGNAL_WEIGHTS,
    PROFILE_WEIGHT,
    TRANSACTION_WEIGHT,
    GRAPH_WEIGHT,
)
from .schemas import SinglePrediction, BatchPredictionRow

__all__ = [
    "MLPredictor",
    "SHAPEngine",
    "lookup_account_features",
    "classify_mule_stage",
    "calculate_composite_risk",
    "calculate_transaction_score",
    "assign_tier",
    "align_lifecycle_stage",
    "SIGNAL_WEIGHTS",
    "PROFILE_WEIGHT",
    "TRANSACTION_WEIGHT",
    "GRAPH_WEIGHT",
    "SinglePrediction",
    "BatchPredictionRow",
]
