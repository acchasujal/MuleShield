"""
MuleShield AI — ML Predictor
Loads trained artifacts and executes XGBoost inference.
Responsibilities: load artifacts, preprocess features, run inference, return probabilities.
No business logic. No lifecycle staging. No fusion scoring.
"""

import json
import logging
import os
import pickle

import numpy as np
import pandas as pd
import shap

from .shap_engine import SHAPEngine
from .lifecycle_engine import classify_mule_stage
from .schemas import SinglePrediction, BatchPredictionRow

logger = logging.getLogger("muleshield.ml.predictor")

_FALLBACK_PREDICTION = SinglePrediction(
    ml_score=0.55,
    mule_stage="DORMANT",
    shap_signals={
        "F670":  0.28,
        "F886":  0.18,
        "F3908": 0.15,
        "F115":  0.12,
        "F2082": -0.10,
    },
)


class MLPredictor:
    """Stateful ML inference engine for MuleShield account classification.

    Loads all artifacts on construction. Provides predict_single and
    predict_batch methods that mirror the original MLService interface
    exactly so that callers require no changes.
    """

    def __init__(self, artifacts_dir: str = "backend/ml_artifacts") -> None:
        self.artifacts_dir   = artifacts_dir
        self.model           = None
        self.imputer         = None
        self.feature_names: list[str] = []
        self.cat_mappings:  dict = {}
        self.feature_importances: dict = {}
        self.explainer       = None
        self._shap_engine: SHAPEngine | None = None
        self.is_loaded       = False

        self._load_artifacts()

    # ------------------------------------------------------------------
    # Artifact loading
    # ------------------------------------------------------------------

    def _load_artifacts(self) -> bool:
        """Load all pre-trained ML artifacts from artifacts_dir."""
        try:
            model_path      = os.path.join(self.artifacts_dir, "final_model.pkl")
            imputer_path    = os.path.join(self.artifacts_dir, "imputer_full.pkl")
            metadata_path   = os.path.join(self.artifacts_dir, "final_metadata.json")
            cat_path        = os.path.join(self.artifacts_dir, "cat_mappings.json")
            importance_path = os.path.join(self.artifacts_dir, "feature_importances.csv")

            for path in [model_path, imputer_path, metadata_path, cat_path]:
                if not os.path.exists(path):
                    logger.warning(f"ML artifact not found: {path}. Reverting to demo/fallback mode.")
                    return False

            with open(metadata_path, "r", encoding="utf-8") as f:
                self.feature_names = json.load(f)

            with open(cat_path, "r", encoding="utf-8") as f:
                self.cat_mappings = json.load(f)

            with open(imputer_path, "rb") as f:
                self.imputer = pickle.load(f)

            with open(model_path, "rb") as f:
                self.model = pickle.load(f)

            # Initialize SHAP TreeExplainer
            self.explainer = shap.TreeExplainer(self.model)

            # Load static feature importances
            if os.path.exists(importance_path):
                imp_df = pd.read_csv(importance_path)
                self.feature_importances = dict(zip(imp_df["feature"], imp_df["importance"]))
            else:
                importances = self.model.feature_importances_
                self.feature_importances = dict(zip(self.feature_names, importances))

            self._shap_engine = SHAPEngine(
                explainer=self.explainer,
                feature_names=self.feature_names,
                feature_importances=self.feature_importances,
            )

            self.is_loaded = True
            logger.info("MuleShield ML inference artifacts loaded successfully.")
            return True

        except Exception as exc:
            logger.error(f"Error loading ML artifacts: {exc}", exc_info=True)
            self.is_loaded = False
            return False

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------

    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map string categorical columns to pre-defined integer codes."""
        df_encoded = df.copy()
        for col, mapping in self.cat_mappings.items():
            if col in df_encoded.columns:
                col_series = df_encoded[col].fillna("Unknown").astype(str)
                df_encoded[col] = col_series.map(mapping).fillna(0).astype(int)
        return df_encoded

    def _preprocess_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply categorical maps, align columns, and impute missing values.

        Pipeline:
            1. Drop leakage features F3912, F3924
            2. Encode categorical columns
            3. Align to 122 selected feature names (add missing as NaN)
            4. Impute remaining NaN with pre-fit SimpleImputer
        """
        df_clean = df.drop(columns=["F3912", "F3924"], errors="ignore").copy()
        df_encoded = self._encode_categorical(df_clean)

        missing_cols = [col for col in self.feature_names if col not in df_encoded.columns]
        if missing_cols:
            df_encoded = pd.concat([df_encoded, pd.DataFrame(np.nan, index=df_encoded.index, columns=missing_cols)], axis=1)

        df_aligned = df_encoded[self.feature_names].copy()
        imputed_arr = self.imputer.transform(df_aligned)
        df_imputed = pd.DataFrame(imputed_arr, columns=self.feature_names, index=df.index)
        return df_imputed

    # ------------------------------------------------------------------
    # Public inference API
    # ------------------------------------------------------------------

    def predict_single(self, raw_features: dict) -> dict:
        """Execute single-account inference with SHAP attribution.

        Returns dict with keys: ml_score, mule_stage, shap_signals.
        On model-not-loaded, returns deterministic fallback values.
        """
        if not self.is_loaded:
            logger.warning("ML Model not loaded. Returning sandbox mock prediction.")
            return {
                "ml_score":    _FALLBACK_PREDICTION.ml_score,
                "mule_stage":  _FALLBACK_PREDICTION.mule_stage,
                "shap_signals": _FALLBACK_PREDICTION.shap_signals,
            }

        try:
            df = pd.DataFrame([raw_features])
            df_processed = self._preprocess_features(df)

            prob = float(self.model.predict_proba(df_processed)[0][1])
            mule_stage   = classify_mule_stage(raw_features, prob * 100.0)
            shap_signals = self._shap_engine.generate_shap_signals(df_processed)

            return {
                "ml_score":    prob,
                "mule_stage":  mule_stage,
                "shap_signals": shap_signals,
            }

        except Exception as exc:
            logger.error(f"Error during single prediction: {exc}", exc_info=True)
            return {
                "error":       str(exc),
                "ml_score":    0.50,
                "mule_stage":  "UNKNOWN",
                "shap_signals": {},
            }

    def predict_batch(self, df_raw: pd.DataFrame) -> list[dict]:
        """High-speed batch inference using static importances (not per-row SHAP).

        Returns list of dicts with keys: index, ml_score, mule_stage, shap_signals.
        """
        if not self.is_loaded:
            logger.warning("ML Model offline. Cannot execute batch inference.")
            return []

        try:
            df_processed = self._preprocess_features(df_raw)
            probs        = self.model.predict_proba(df_processed)[:, 1]
            top_5_static = self._shap_engine.get_static_top5()

            batch_results = []
            for idx, prob in enumerate(probs):
                raw_row   = df_raw.iloc[idx].to_dict()
                prob_val  = float(prob)
                mule_stage = classify_mule_stage(raw_row, prob_val * 100.0)

                batch_results.append({
                    "index":       int(df_raw.index[idx]),
                    "ml_score":    prob_val,
                    "mule_stage":  mule_stage,
                    "shap_signals": top_5_static,
                })
            return batch_results

        except Exception as exc:
            logger.error(f"Error during batch prediction: {exc}", exc_info=True)
            return []
