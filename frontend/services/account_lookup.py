# frontend/services/account_lookup.py

import logging
import streamlit as st

logger = logging.getLogger("frontend.services.account_lookup")

@st.cache_data(show_spinner=False)
def lookup_account_by_id(account_id: str) -> dict:
    """Ultra-fast, memory-efficient pure Python lookup of account profile row in DataSet.csv."""
    logger.info(f"[LOOKUP] Entering lookup_account_by_id for: {account_id}")
    try:
        suffix = account_id.strip()
        if suffix.startswith("ACC052"):
            suffix = suffix[6:]
        idx = int(suffix)
        logger.info(f"[LOOKUP] Parsed index: {idx}")
        
        # Read DataSet.csv line-by-line to avoid loading/scanning in Pandas
        with open("data/boi/DataSet.csv", "r", encoding="utf-8") as f:
            header_line = f.readline()
            headers = [h.strip().strip('"').strip("'") for h in header_line.split(",")]
            logger.info(f"[LOOKUP] Headers parsed. Total columns: {len(headers)}")
            
            # Skip idx - 1 lines
            logger.info(f"[LOOKUP] Skipping {idx - 1} lines...")
            for i in range(idx - 1):
                f.readline()
            logger.info("[LOOKUP] Skipping complete.")
                
            target_line = f.readline()
            if not target_line:
                logger.info("[LOOKUP] Target line is empty!")
                return None
                
            values = [v.strip().strip('"').strip("'") for v in target_line.split(",")]
            logger.info(f"[LOOKUP] Row values parsed. Zip coordinates mapping...")
            
            # Zip headers and values
            features = {}
            for k, v in zip(headers, values):
                if k == "":
                    k = "Unnamed: 0"
                if v == "" or v.lower() == "nan" or v.lower() == "null" or v.lower() == "na":
                    features[k] = None
                else:
                    try:
                        if "." in v:
                            features[k] = float(v)
                        else:
                            features[k] = int(v)
                    except ValueError:
                        features[k] = v
            
            logger.info(f"[LOOKUP] Mapping complete. Unnamed: 0 = {features.get('Unnamed: 0')}")
            if features.get("Unnamed: 0") == idx:
                logger.info("[LOOKUP] SUCCESS: Account profile coordinates found!")
                return features
    except Exception as exc:
        logger.error(f"[LOOKUP] Error in pure Python lookup: {exc}", exc_info=True)
    logger.info("[LOOKUP] Exiting lookup - account not found or failed.")
    return None
