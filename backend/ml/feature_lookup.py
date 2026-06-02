"""
MuleShield AI — Feature Lookup Engine
Retrieves account baseline profiles from DataSet.csv using sequential line-seeking.
No prediction logic. No ML inference.
"""

import logging
import os

logger = logging.getLogger("muleshield.ml.feature_lookup")

# Fallback profile used when CSV lookup fails or account is out of range
_FALLBACK_FEATURES = {
    "Unnamed: 0": 999,
    "F670": 1.0,        # Prior regulatory warning
    "F886": 0.45,       # UPI spike
    "F3908": 0.85,      # High velocity passing ratio
    "F115": 0.90,
    "F2082": 0.0,       # Complete absence of consumer behaviour
    "F3889": "G365D",   # Dormant
}

_DATASET_PATH = "data/boi/DataSet.csv"


def lookup_account_features(account_id: str) -> dict:
    """Retrieve account feature profile from DataSet.csv by account ID.

    Uses sequential line-seeking to avoid loading the full 9082-row CSV for
    each single-account lookup. Falls back to hardcoded defaults on any error.

    Args:
        account_id: Account ID string, e.g. "ACC05200000000028".

    Returns:
        Feature dict (compatible with MLPredictor.predict_single input).
    """
    try:
        if not isinstance(account_id, str):
            account_id = str(account_id)
        suffix = account_id.strip()
        if suffix.startswith("ACC052"):
            suffix = suffix[6:]
        try:
            idx = int(suffix)
        except ValueError:
            return _FALLBACK_FEATURES.copy()

        if idx < 1 or idx > 9082:
            return _FALLBACK_FEATURES.copy()

        if not os.path.exists(_DATASET_PATH):
            logger.warning(f"DataSet.csv not found at {_DATASET_PATH}")
            return _FALLBACK_FEATURES.copy()

        with open(_DATASET_PATH, "r", encoding="utf-8") as f:
            header_line = f.readline()
            headers = [h.strip().strip('"').strip("'") for h in header_line.split(",")]

            # Seek directly to the target row (skip idx-1 data lines)
            for _ in range(idx - 1):
                f.readline()

            target_line = f.readline()
            if not target_line:
                return _FALLBACK_FEATURES.copy()

            values = [v.strip().strip('"').strip("'") for v in target_line.split(",")]

            features: dict = {}
            for k, v in zip(headers, values):
                if k == "":
                    k = "Unnamed: 0"
                if v == "" or v.lower() in ("nan", "null", "na"):
                    features[k] = None
                else:
                    try:
                        if "." in v:
                            features[k] = float(v)
                        else:
                            features[k] = int(v)
                    except ValueError:
                        features[k] = v

            if features.get("Unnamed: 0") == idx:
                return features

    except Exception as exc:
        logger.error(f"Error in lookup_account_features({account_id!r}): {exc}")

    return _FALLBACK_FEATURES.copy()
