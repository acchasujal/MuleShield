# MuleShield AI Data Directory 📊

This directory manages the datasets and analysis outputs utilized by the MuleShield AI system.

## BOI Dataset Setup

The Bank of India (BOI) transaction dataset (**`DataSet.csv`**) is required for model training and full inference pipelines. 

Due to **file size limits (116 MB+) and data distribution constraints**, this dataset is **intentionally excluded** from the GitHub repository.

### Setup Instructions

To run local training or full inference:
1. Obtain the BOI transaction dataset.
2. Create the target subdirectory: `data/boi/` (if it does not already exist).
3. Place the dataset file exactly at:
   ```path
   data/boi/DataSet.csv
   ```

---

## Excluded Legacy and Output Files

To maintain a lightweight and professional repository footprint, the following files are excluded from remote version control (but remain preserved locally on development hosts):
- **FundTrace Data Matrices:** `data/*.csv` (synthetic user profiles, legacy transaction files, and scenario CSVs).
- **Inference Fallback Reports:** `data/fallback_*.json` (mock analysis files used during service offline fallbacks).
- **Archive Outputs:** `data/archive/fundtrace_outputs/` (historical suspicious transaction logs).
- **Legacy Components:** `data/legacy/` (older dataset schemas and scenarios).
