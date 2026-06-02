"""
MuleShield AI — Machine Learning Inference Service
Public interface facade that delegates to the backend/ml/ modular package.

Backward-compatible: provides same attributes and methods as the original
MLService class so all existing callers require zero changes.
"""

import logging
from backend.ml.predictor import MLPredictor

logger = logging.getLogger("muleshield.ml")


class MLService:
    """Backward-compatible facade over the modular MLPredictor.

    Exposes:
        is_loaded       — bool
        feature_names   — list[str]
        predict_single  — dict
        predict_batch   — list[dict]
    """

    def __init__(self, artifacts_dir: str = "backend/ml_artifacts") -> None:
        self._predictor = MLPredictor(artifacts_dir=artifacts_dir)

    # ------------------------------------------------------------------
    # Compatibility attributes
    # ------------------------------------------------------------------

    @property
    def is_loaded(self) -> bool:
        return self._predictor.is_loaded

    @property
    def feature_names(self) -> list:
        return self._predictor.feature_names

    @property
    def feature_importances(self) -> dict:
        return self._predictor.feature_importances

    # ------------------------------------------------------------------
    # Inference interface (unchanged signatures)
    # ------------------------------------------------------------------

    def predict_single(self, raw_features: dict) -> dict:
        """Execute single-account ML inference. Returns ml_score, mule_stage, shap_signals."""
        return self._predictor.predict_single(raw_features)

    def predict_batch(self, df_raw) -> list[dict]:
        """Execute batch ML inference. Returns list of index/ml_score/mule_stage/shap_signals dicts."""
        return self._predictor.predict_batch(df_raw)

    # ------------------------------------------------------------------
    # Legacy direct method aliases (kept for any direct callers)
    # ------------------------------------------------------------------

    def classify_mule_stage(self, raw_features: dict, risk_score: float) -> str:
        """Legacy alias — delegates to backend.ml.lifecycle_engine."""
        from backend.ml.lifecycle_engine import classify_mule_stage
        return classify_mule_stage(raw_features, risk_score)

    def generate_shap_signals(self, processed_df) -> dict:
        """Legacy alias — delegates to backend.ml.shap_engine via predictor."""
        if self._predictor._shap_engine:
            return self._predictor._shap_engine.generate_shap_signals(processed_df)
        return {}
