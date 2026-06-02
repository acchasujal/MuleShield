"""
MuleShield AI — SHAP Explainability Engine
Wraps shap.TreeExplainer to generate per-prediction feature attributions.
No scoring logic. No model loading (receives explainer from predictor).
"""

import logging
import shap
import pandas as pd

logger = logging.getLogger("muleshield.ml.shap")


class SHAPEngine:
    """Computes SHAP feature attributions using a pre-fitted TreeExplainer.

    Accepts the explainer and feature importances from MLPredictor so that
    no duplicate explainer initialization is performed.
    """

    def __init__(
        self,
        explainer: shap.TreeExplainer,
        feature_names: list[str],
        feature_importances: dict,
    ) -> None:
        self.explainer          = explainer
        self.feature_names      = feature_names
        self.feature_importances = feature_importances

    def generate_shap_signals(self, processed_df: pd.DataFrame) -> dict:
        """Compute dynamic SHAP attributions for a single processed row.

        Handles XGBoost output shape variants:
          - list format: shap_vals[1][0]   (class 1 values from list of arrays)
          - 3D format:   shap_vals[0][1]   (class 1 slice from (N, 2, F) array)
          - 2D default:  shap_vals[0]      (flat array)

        Args:
            processed_df: Pre-processed 1-row DataFrame from MLPredictor.

        Returns:
            Dict of {feature_name: shap_value} for top-5 attributions by abs impact.
        """
        try:
            shap_vals = self.explainer.shap_values(processed_df)

            if isinstance(shap_vals, list):
                vals = shap_vals[1][0]
            elif len(shap_vals.shape) == 3:
                vals = shap_vals[0][1]
            else:
                vals = shap_vals[0]

            attributions = dict(zip(self.feature_names, vals))
            sorted_attrs = sorted(attributions.items(), key=lambda x: abs(x[1]), reverse=True)
            top_5 = sorted_attrs[:5]
            return {feature: float(val) for feature, val in top_5}

        except Exception as exc:
            logger.error(f"Failed to generate SHAP signals: {exc}")
            # Fallback to static importances on SHAP failure
            return dict(
                sorted(self.feature_importances.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
            )

    def get_static_top5(self) -> dict:
        """Return top-5 features by static importance (for batch speed optimisation).

        Avoids per-row SHAP computation over large batches.

        Returns:
            Dict of {feature_name: importance_value} for top-5 features.
        """
        return dict(
            sorted(self.feature_importances.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        )
