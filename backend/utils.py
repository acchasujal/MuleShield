"""
MuleShield AI — Backend Utilities
General-purpose helpers for DataFrames and account feature retrieval.
lookup_account_features delegates to backend/ml/feature_lookup for clean separation.
"""

import logging
import pandas as pd
from fastapi import HTTPException

from backend.ml.feature_lookup import lookup_account_features  # noqa: F401 — re-export

logger = logging.getLogger("muleshield.utils")

REQUIRED_COLUMNS = {"from_account", "to_account", "amount", "timestamp"}


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate columns, types, and non-emptiness. Raises HTTPException on failure."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(400, detail=f"Missing required columns: {sorted(missing)}")
    if df.empty:
        raise HTTPException(400, detail="Uploaded file contains no data rows.")
    try:
        df["amount"] = df["amount"].astype(float)
    except (ValueError, TypeError) as exc:
        raise HTTPException(400, detail=f"'amount' must be numeric: {exc}")
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except Exception as exc:
        raise HTTPException(400, detail=f"'timestamp' must be parseable dates: {exc}")
    return df
