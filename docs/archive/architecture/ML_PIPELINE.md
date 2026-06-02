# ML_PIPELINE.md
_Machine learning training lifecycle, feature engineering rules, and explainability pipeline. ~700 tokens._

---

## ⚙️ MACHINE LEARNING PIPELINE FLOW

The pipeline executes in two primary phases: an offline model training flow and a stateless runtime inference service.

```
[ OFFLINE MODEL TRAINING ]
Raw DataSet.csv (9,082 x 3,924)
        │
        ▼
1. Drop columns with >80% null values
2. Exclude Feature F3912 (prevent leakage)
3. Retain 122 highly discriminative features (variance/domain filter)
4. Fit SimpleImputer on training features -> imputer_full.pkl
5. Map categorical variables -> cat_mappings.json
6. Oversample minority class using SMOTE
7. Train XGBClassifier (scale_pos_weight=111) -> final_model.pkl
        │
        ▼
[ STATELESS RUNTIME INFERENCE ]
POST /predict/batch (FastAPI Web Layer)
        │
        ▼
1. Load model artifacts once during server lifespan
2. Apply LabelEncoder mappings from cat_mappings.json
3. Impute missing features using imputer_full.pkl
4. Drop extra columns to retain only the 122 selected features
5. Model predicts probability of mule behavior (XGBoost)
6. Compute top-5 feature attributions using SHAP TreeExplainer
```

---

## 🔍 ARTIFACT FILES SCHEMA

The inference engine in `backend/ml_service.py` is initialized using 5 authoritative files located in `backend/ml_artifacts/`:

1.  **`final_model.pkl`:** Pickled pipeline containing the fitted `XGBClassifier` model.
2.  **`imputer_full.pkl`:** Pickled `SimpleImputer` trained on the training partition median values.
3.  **`final_metadata.json`:** JSON structure containing the exact sorted list of 122 feature names required by the model.
4.  **`cat_mappings.json`:** JSON dictionary of the 8 categorical variables mapped to their integer codes.
5.  **`feature_importances.csv`:** Sorted list of feature names and their corresponding overall importance weights.

---

## 📐 TRAINING & HYPERPARAMETER SPECIFICATIONS

Model training is governed by strict class-balancing controls. The learning parameters are defined as:

*   **Oversampling (SMOTE):**
    ```python
    from imblearn.over_sampling import SMOTE
    # k_neighbors=5, random_state=42. Executed only on the 122-feature train split.
    smote = SMOTE(k_neighbors=5, random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_122, y_train)
    ```
*   **XGBoost Classifier Parameters:**
    ```python
    from xgboost import XGBClassifier
    
    model = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=111,          # Compensates for 111:1 legit-to-mule class imbalance
        eval_metric='aucpr',           # Optimize strictly on Precision-Recall AUC
        use_label_encoder=False,
        random_state=42
    )
    ```

---

## 💡 SHAP EXPLAINABILITY RUNTIME IMPLEMENTATION

To provide transparency, every single transaction alert serves local SHAP explainability.

```python
# Defined inside backend/ml_service.py
import shap
import json
import numpy as np

# explainer initialized once at boot using lifespan model
# explainer = shap.TreeExplainer(app.state.ml_model)

def generate_shap_signals(account_id: str, processed_features_df, model_features_list) -> dict:
    """
    Computes SHAP value attributions for a single account inference.
    Returns the top-5 feature names along with their numerical contributions.
    """
    # 1. Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(processed_features_df)[0]
    
    # 2. Extract attribution weights for target class (1 = Mule)
    # XGBoost outputs log-odds or probabilities depending on output_margin
    attributions = dict(zip(model_features_list, shap_vals))
    
    # 3. Sort by absolute contribution weight
    sorted_attributions = sorted(
        attributions.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    
    # 4. Slice top 5 contributions
    top_5 = sorted_attributions[:5]
    
    return {feature: float(value) for feature, value in top_5}
```
