"""
MuleShield AI — Offline Model Training and Feature Selection
Trains an XGBClassifier on Bank of India (BOI) DataSet.csv and exports ML artifacts.
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

def train_pipeline():
    print("\n[1/7] Initializing training pipeline...")
    csv_path = "data/boi/DataSet.csv"
    artifacts_dir = "backend/ml_artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"DataSet.csv not found at: {csv_path}. Please place it there first.")

    print(f"Reading dataset from {csv_path} (this might take a few moments for 116MB)...")
    # Load dataset
    df = pd.read_csv(csv_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Clean index column if Unnamed is present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    elif "" in df.columns:
        df = df.drop(columns=[""])

    # 1. Target isolation
    target_col = "F3924"
    if target_col not in df.columns:
        # Check if F3924 is in the dataset or if it is named differently
        # Alphanumerically last column is F3924
        cols = [c for c in df.columns if c.startswith("F")]
        target_col = cols[-1]
        print(f"Target column detected as: {target_col}")

    y = df[target_col].copy()
    
    # 2. Exclude Feature F3912 (prevent data leakage)
    leakage_col = "F3912"
    features_to_drop = [target_col]
    if leakage_col in df.columns:
        features_to_drop.append(leakage_col)
        print("Feature F3912 successfully excluded from features list to prevent data leakage.")

    X_raw = df.drop(columns=features_to_drop, errors="ignore")

    # 3. Categorical Mappings Definition
    # Identifies the 8 categorical columns from specifications
    categorical_cols = ["F2230", "F3886", "F3888", "F3889", "F3890", "F3891", "F3892", "F3893"]
    # Filter to only those columns that actually exist in the raw features
    categorical_cols = [col for col in categorical_cols if col in X_raw.columns]
    print(f"Categorical features identified: {categorical_cols}")

    cat_mappings = {}
    for col in categorical_cols:
        # Cast categories as strings, filling NaNs with "Unknown"
        cat_series = X_raw[col].fillna("Unknown").astype(str)
        unique_cats = sorted(cat_series.unique())
        # Map values starting from 1 (0 is reserved as the default fallback placeholder)
        mapping = {val: idx + 1 for idx, val in enumerate(unique_cats)}
        cat_mappings[col] = mapping
        
        # Apply encoding inplace to X_raw
        X_raw[col] = cat_series.map(mapping).astype(int)

    # Save categorical mappings to backend/ml_artifacts/cat_mappings.json
    with open(os.path.join(artifacts_dir, "cat_mappings.json"), "w", encoding="utf-8") as f:
        json.dump(cat_mappings, f, indent=2)
    print("Saved categorical mappings to cat_mappings.json")

    # 4. Feature Selection: Build exactly 122 highly discriminative features
    # Filter out columns with > 80% null values
    null_rates = X_raw.isnull().mean()
    valid_cols = null_rates[null_rates <= 0.80].index.tolist()
    print(f"Columns with <= 80% null rates: {len(valid_cols)} out of {X_raw.shape[1]}")

    X_valid = X_raw[valid_cols].copy()

    # Analyst highlights that MUST be included in the 122 features
    analyst_highlights = [
        "F115", "F321", "F527", "F531", "F670", "F1692", "F2082", "F2122", 
        "F2582", "F2678", "F2737", "F2956", "F3043", "F3836", "F3887", "F3889", 
        "F3891", "F3894"
    ]
    # Ensure they exist in X_valid (if some are dropped by null filter, force include them anyway)
    analyst_highlights = [col for col in analyst_highlights if col in X_raw.columns]
    print(f"Force-including {len(analyst_highlights)} analyst highlighted features.")

    # Calculate correlation with target to choose the remaining features
    # We impute numeric features with median temporarily for correlation calculation
    print("Computing Pearson correlation with target F3924 to select highly discriminative features...")
    correlations = {}
    for col in X_valid.columns:
        feature_series = X_valid[col]
        # Fill numeric missing values with median
        if feature_series.dtype != 'object':
            median_val = feature_series.median()
            if pd.isnull(median_val):
                median_val = 0
            feature_series = feature_series.fillna(median_val)
        
        # Pearson correlation
        corr = feature_series.corr(y)
        correlations[col] = abs(corr) if not pd.isnull(corr) else 0

    # Sort columns by absolute correlation descending
    sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    # Construct feature set starting with the highlighted ones
    selected_features_set = set(analyst_highlights)
    for feature, corr_val in sorted_features:
        if len(selected_features_set) >= 122:
            break
        selected_features_set.add(feature)

    # Sort list alphanumerically for stable deterministic order
    selected_features_list = sorted(list(selected_features_set))
    print(f"Selected exactly {len(selected_features_list)} features for model ingestion.")

    # Save feature names to backend/ml_artifacts/final_metadata.json
    with open(os.path.join(artifacts_dir, "final_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(selected_features_list, f, indent=2)
    print("Saved feature list metadata to final_metadata.json")

    # Extract final features matrix
    X_selected = X_raw[selected_features_list].copy()

    # 5. SimpleImputer Fitting
    print("[5/7] Fitting SimpleImputer on the selected 122 features...")
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X_selected)
    
    # Save the fitted imputer
    with open(os.path.join(artifacts_dir, "imputer_full.pkl"), "wb") as f:
        pickle.dump(imputer, f)
    print("Saved fitted SimpleImputer to imputer_full.pkl")

    # 6. Class Imbalance correction using SMOTE
    print(f"[6/7] Resolving severe class imbalance (Legit: {sum(y==0)} vs Mule: {sum(y==1)})...")
    smote = SMOTE(k_neighbors=5, random_state=42)
    X_res, y_res = smote.fit_resample(X_imputed, y)
    print(f"Resampled dataset size: {X_res.shape[0]} rows (balanced legit/mule classes)")

    # 7. Model Training using XGBClassifier
    print("[7/7] Training XGBoost Classifier...")
    model = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=111,  # matches legit-to-mule class ratio
        eval_metric="aucpr",   # Rank strictly by PR-AUC
        use_label_encoder=False,
        random_state=42
    )
    model.fit(X_res, y_res)

    # Save model artifact
    with open(os.path.join(artifacts_dir, "final_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    print("Saved trained model artifact to final_model.pkl")

    # Save feature importances
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        "feature": selected_features_list,
        "importance": importances
    }).sort_values("importance", ascending=False)
    
    importance_df.to_csv(os.path.join(artifacts_dir, "feature_importances.csv"), index=False)
    print("Saved feature importances to feature_importances.csv")

    print("\nML Model artifacts successfully generated!")
    print(f"Artifact location: {os.path.abspath(artifacts_dir)}")

if __name__ == "__main__":
    train_pipeline()
