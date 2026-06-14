"""
MuleShield AI — Model Evaluation on Validation Split
Performs a stratified 80/20 split on DataSet.csv, processes categorical columns,
imputes features, oversamples the training split with SMOTE, trains the XGBClassifier,
and evaluates model performance (ROC-AUC, PR-AUC, F1-Score, Precision, Recall) on the validation split.
"""

import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
)

def evaluate_pipeline():
    print("[1/6] Initializing evaluation pipeline...")
    csv_path = "data/boi/DataSet.csv"
    metadata_path = "backend/ml_artifacts/final_metadata.json"
    cat_path = "backend/ml_artifacts/cat_mappings.json"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"DataSet.csv not found at: {csv_path}. Please place it there first.")

    print(f"Reading dataset from {csv_path} (this might take a few moments for 116MB)...")
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
        cols = [c for c in df.columns if c.startswith("F")]
        target_col = cols[-1]
    y = df[target_col].copy()

    # 2. Exclude Feature F3912 (prevent data leakage)
    leakage_col = "F3912"
    features_to_drop = [target_col]
    if leakage_col in df.columns:
        features_to_drop.append(leakage_col)
        print("Feature F3912 successfully excluded from features list to prevent data leakage.")

    X_raw = df.drop(columns=features_to_drop, errors="ignore")

    # 3. Categorical Mappings Definition
    categorical_cols = ["F2230", "F3886", "F3888", "F3889", "F3890", "F3891", "F3892", "F3893"]
    categorical_cols = [col for col in categorical_cols if col in X_raw.columns]
    print(f"Categorical features identified: {categorical_cols}")

    if os.path.exists(cat_path):
        with open(cat_path, "r", encoding="utf-8") as f:
            cat_mappings = json.load(f)
        print("Loaded categorical mappings from cat_mappings.json")
    else:
        cat_mappings = {}
        for col in categorical_cols:
            cat_series = X_raw[col].fillna("Unknown").astype(str)
            unique_cats = sorted(cat_series.unique())
            mapping = {val: idx + 1 for idx, val in enumerate(unique_cats)}
            cat_mappings[col] = mapping

    for col in categorical_cols:
        mapping = cat_mappings.get(col, {})
        cat_series = X_raw[col].fillna("Unknown").astype(str)
        X_raw[col] = cat_series.map(mapping).fillna(0).astype(int)

    # 4. Feature Selection: Use the 122 feature names defined in final_metadata.json
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            selected_features = json.load(f)
        print(f"Loaded {len(selected_features)} features list from final_metadata.json")
    else:
        print("final_metadata.json not found! Recreating feature selection logic...")
        null_rates = X_raw.isnull().mean()
        valid_cols = null_rates[null_rates <= 0.80].index.tolist()
        X_valid = X_raw[valid_cols].copy()
        
        # Pearson correlation
        correlations = {}
        for col in X_valid.columns:
            feature_series = X_valid[col]
            if feature_series.dtype != 'object':
                median_val = feature_series.median()
                if pd.isnull(median_val):
                    median_val = 0
                feature_series = feature_series.fillna(median_val)
            corr = feature_series.corr(y)
            correlations[col] = abs(corr) if not pd.isnull(corr) else 0
            
        sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
        analyst_highlights = ["F115", "F321", "F527", "F531", "F670", "F1692", "F2082", "F2122", 
                              "F2582", "F2678", "F2737", "F2956", "F3043", "F3836", "F3887", "F3889", 
                              "F3891", "F3894"]
        analyst_highlights = [col for col in analyst_highlights if col in X_raw.columns]
        
        selected_features_set = set(analyst_highlights)
        for feature, corr_val in sorted_features:
            if len(selected_features_set) >= 122:
                break
            selected_features_set.add(feature)
        selected_features = sorted(list(selected_features_set))
        print(f"Selected exactly {len(selected_features)} features.")

    X_selected = X_raw[selected_features].copy()

    # 5. Stratified Train/Validation Split (80/20)
    print("\n[2/6] Performing 80/20 stratified train/validation split...")
    X_train, X_val, y_train, y_val = train_test_split(
        X_selected, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training split: {X_train.shape[0]} rows, Validation split: {X_val.shape[0]} rows")
    print(f"Training target distribution: {dict(y_train.value_counts())}")
    print(f"Validation target distribution: {dict(y_val.value_counts())}")

    # 6. Imputation
    print("\n[3/6] Fitting SimpleImputer on the training features split...")
    imputer = SimpleImputer(strategy="median")
    X_train_imp = imputer.fit_transform(X_train)
    X_val_imp = imputer.transform(X_val)

    # 7. Class Imbalance correction via SMOTE
    print(f"\n[4/6] Applying SMOTE on training split (Legit: {sum(y_train==0)} vs Mule: {sum(y_train==1)})...")
    smote = SMOTE(k_neighbors=5, random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train_imp, y_train)
    print(f"Resampled training set: {X_train_res.shape[0]} rows (balanced legit/mule classes)")

    # 8. Model Training
    print("\n[5/6] Training XGBoost Classifier...")
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
    model.fit(X_train_res, y_train_res)

    # 9. Model Evaluation on Validation Split
    print("\n[6/6] Evaluating model on validation split...")
    y_pred_proba = model.predict_proba(X_val_imp)[:, 1]
    y_pred = model.predict(X_val_imp)

    # Metric calculations
    roc_auc = roc_auc_score(y_val, y_pred_proba)
    pr_auc = average_precision_score(y_val, y_pred_proba)
    f1 = f1_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)

    print("\n" + "=" * 50)
    print("           MODEL PERFORMANCE METRICS")
    print("=" * 50)
    print(f"ROC-AUC score:                   {roc_auc:.6f}")
    print(f"PR-AUC (Average Precision) score: {pr_auc:.6f}")
    print(f"F1-Score:                        {f1:.6f}")
    print(f"Precision:                       {precision:.6f}")
    print(f"Recall:                          {recall:.6f}")
    print("=" * 50)

    print("\nDetailed Classification Report:")
    print(classification_report(y_val, y_pred, target_names=["Legitimate", "Mule"]))

if __name__ == "__main__":
    evaluate_pipeline()
