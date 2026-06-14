# frontend/utils/constants.py

BASE_URL = "http://127.0.0.1:8000"
BACKEND_URL = f"{BASE_URL}/analyze"
STR_URL = f"{BASE_URL}/generate-str"
ASK_URL = f"{BASE_URL}/ask"

# Severity display markers — text-only, no emoji (badges rendered per component)
SEVERITY_EMOJI = {
    "CRITICAL": "CRIT",
    "HIGH":     "HIGH",
    "MEDIUM":   "MED",
    "LOW":      "LOW",
    "LEGITIMATE": "CLEAR",
    "UNDER_REVIEW": "REVIEW",
}

# Severity chip colors for inline HTML badges
SEVERITY_COLORS = {
    "CRITICAL":     "#ef4444",
    "HIGH":         "#f97316",
    "MEDIUM":       "#d97706",
    "LOW":          "#10b981",
    "LEGITIMATE":   "#10b981",
    "UNDER_REVIEW": "#d97706",
}

GRAPH_COLORS = {
    "CRITICAL":     "#ef4444",
    "HIGH":         "#C00000",
    "MEDIUM":       "#B8600A",
    "LOW":          "#10b981",
    "LEGITIMATE":   "#10b981",
    "UNDER_REVIEW": "#eab308",
}

MAX_EDGES = 80
PAGE_SIZE = 5

# Named SHAP Feature Mapping — business-language labels for explainability
FEATURE_NAMES = {
    "F115":  "Transaction Frequency Ratio",
    "F321":  "Debit/Credit Amount Ratio",
    "F527":  "Inward Amount Ratio",
    "F531":  "Outward Amount Ratio",
    "F670":  "Regulatory TMS Flag",
    "F886":  "Payment Channel Switching Rate",
    "F1692": "Activity Count (Suppressed)",
    "F2082": "Normal Banking Activity (Absent)",
    "F2122": "Ratio Feature (Declining)",
    "F2582": "Change Metric (Near-Zero)",
    "F2678": "Extreme Amount Variance",
    "F2737": "Volume Change (Reduced)",
    "F2956": "Transaction Count (Suppressed)",
    "F3043": "Volume Count (Reduced)",
    "F3836": "Balance / Credit Limit Breach",
    "F3887": "Account Age Indicator",
    "F3889": "Dormancy Reactivation (G365D)",
    "F3891": "High-Vulnerability Demographic Profile",
    "F3894": "Account Holder Age",
    "F3908": "High-Velocity Pass-Through",
    "F3912": "Legacy TMS Warn Flag (Post-Inference Only)",
    "F3924": "Target: Mule Classification",
}
