# frontend/utils/constants.py

BASE_URL = "http://127.0.0.1:8000"
BACKEND_URL = f"{BASE_URL}/analyze"
STR_URL = f"{BASE_URL}/generate-str"
ASK_URL = f"{BASE_URL}/ask"

SEVERITY_EMOJI = {
    "CRITICAL": "[!]",
    "HIGH": "[!]",
    "MEDIUM": "[~]",
    "LOW": "[+]",
    "LEGITIMATE": "[+]",
    "UNDER_REVIEW": "[~]",
}

GRAPH_COLORS = {
    "CRITICAL": "#ef4444",
    "HIGH": "#C00000",
    "MEDIUM": "#B8600A",
    "LOW": "#10b981",
    "LEGITIMATE": "#10b981",
    "UNDER_REVIEW": "#eab308",
}

MAX_EDGES = 80
PAGE_SIZE = 5

# S3-T2 - Named SHAP Feature Mapping
FEATURE_NAMES = {
    "F115": "Transaction Frequency Ratio",
    "F321": "Amount Ratio (Debit/Credit)",
    "F527": "Amount Ratio (Inward)",
    "F531": "Amount Ratio (Outward)",
    "F670": "Regulatory TMS Flag",
    "F886": "Channel Switching Rate",
    "F1692": "Activity Count (Low)",
    "F2082": "Normal Banking Activity (Absent)",
    "F2122": "Ratio Feature (Decline)",
    "F2582": "Change Metric (Near-Zero)",
    "F2678": "Amount Change (Extreme)",
    "F2737": "Change Feature (Low)",
    "F2956": "Count/Volume (Suppressed)",
    "F3043": "Count/Volume (Reduced)",
    "F3836": "Balance/Credit Limit Breach",
    "F3887": "Age Count Feature",
    "F3889": "Dormant Account (G365D Bucket)",
    "F3891": "Student / Agri Demographic Profile",
    "F3894": "Account Holder Age",
    "F3908": "High-Velocity Pass-Through",
    "F3912": "Legacy TMS Warn Flag (Post-Inference Only)",
    "F3924": "Target: Mule Classification",
}
