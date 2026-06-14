# frontend/services/api_client.py

import json
import logging
from pathlib import Path
import pandas as pd
import requests
import streamlit as st
from frontend.utils.constants import BASE_URL, BACKEND_URL

logger = logging.getLogger("frontend.services.api_client")

def _scenario_key_from_label(label: str) -> str:
    """Map a CSV filename or scenario label to the fallback key."""
    label_lower = label.lower()
    if "dormant" in label_lower:
        return "dormant_reactivation"
    if "student" in label_lower:
        return "student_recruitment"
    if "agri" in label_lower or "subsidy" in label_lower:
        return "agri_diversion"
    return "dormant_reactivation"  # safe default

def load_fallback(scenario_name: str, data_type: str):
    """
    Load pre-generated fallback JSON for a scenario.
    data_type: 'analysis', 'str', or 'qa'
    Returns parsed JSON or None if file doesn't exist.
    """
    path = Path(f"data/fallback_{scenario_name}_{data_type}.json")
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning(f"Failed to load fallback {path}: {exc}")
    return None

@st.cache_data(show_spinner=False)
def run_analysis(file_bytes: bytes, file_name: str) -> dict:
    """POST CSV bytes to the FastAPI backend. Cached by (bytes, name)."""
    is_ml = "dataset" in file_name.lower() or "dataset" in file_name
    url = f"{BASE_URL}/predict/batch" if is_ml else BACKEND_URL
    files = {"file": (file_name, file_bytes, "text/csv")}
    resp = requests.post(url, files=files, timeout=120)
    resp.raise_for_status()
    return resp.json()

def _serialise_txn_list(df: pd.DataFrame, limit: int) -> list:
    """Convert top `limit` rows to JSON-safe dicts with vectorised timestamp conversion."""
    subset = df.head(limit).copy()
    if "timestamp" in subset.columns:
        subset["timestamp"] = subset["timestamp"].astype(str)
    return subset.to_dict(orient="records")
