"""
MuleShield AI — ML Schemas
Typed structures for ML prediction results shared across the ML layer.
"""

from dataclasses import dataclass, field


@dataclass
class SinglePrediction:
    """Result of a single ML inference call."""
    ml_score: float
    mule_stage: str
    shap_signals: dict = field(default_factory=dict)
    error: str | None = None


@dataclass
class BatchPredictionRow:
    """Result of one row in a batch inference call."""
    index: int
    ml_score: float
    mule_stage: str
    shap_signals: dict = field(default_factory=dict)
