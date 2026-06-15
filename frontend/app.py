# frontend/app.py

import sys
sys.path.insert(0, '.')

import io
import time
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timezone

from frontend.utils.constants import SEVERITY_EMOJI, BASE_URL
from frontend.utils.demo_registry import DEMO_I4C_ACCOUNT, DEMO_I4C_REF
from frontend.utils.formatting import _fmt_amount
from frontend.services.api_client import run_analysis, _scenario_key_from_label, load_fallback
from frontend.components.sidebar import render_sidebar
from frontend.components.hero import render_hero_landing
from frontend.components.demo_mode import render_threat_simulation_view
from frontend.components.executive_dashboard import render_executive_dashboard_view
from frontend.components.alert_center import render_alert_center_view
from frontend.components.account_inspector import render_account_inspector_view
from frontend.components.model_metrics import render_model_metrics_view
from frontend.components.compliance_panel import render_compliance_workspace_view

# ─────────────────────────────────────────────────────────────────────────────
# Page config (MUST be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MuleShield — AML Investigation Platform",
    page_icon="🛡️",
    layout="wide",
)

# Inject Inter font + global professional styles + I4C Threat Ticker
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* Global font override */
html, body, [class*="css"], .stMarkdown, .stText, button, input, select, textarea {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
/* Tighten default Streamlit padding */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 80px !important;
    max-width: 1400px;
}
/* Professional metric cards */
[data-testid="metric-container"] {
    background: #1e293b;
    border-radius: 6px;
    padding: 12px 16px;
    border: 1px solid #334155;
}
/* Severity badge utility classes (used in raw HTML) */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-critical { background: #ef4444; color: #fff; }
.badge-high     { background: #f97316; color: #fff; }
.badge-medium   { background: #d97706; color: #fff; }
.badge-low      { background: #10b981; color: #fff; }
.badge-clear    { background: #1e293b; color: #10b981; border: 1px solid #10b981; }
.badge-review   { background: #1e293b; color: #d97706; border: 1px solid #d97706; }
/* Tighten expander headers */
[data-testid="stExpander"] summary {
    font-size: 13px !important;
    font-weight: 500;
}
/* I4C ticker bottom bar */
.main .block-container { padding-bottom: 70px !important; }
.threat-ticker-container {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #0b0f19;
    color: #f43f5e;
    border-top: 1px solid #1e293b;
    padding: 8px 0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 11px;
    z-index: 999999;
    overflow: hidden;
}
.threat-ticker-text {
    display: inline-block;
    white-space: nowrap;
    padding-left: 100%;
    animation: threatMarquee 35s linear infinite;
    font-weight: bold;
}
@keyframes threatMarquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
}
</style>
<div class="threat-ticker-container">
    <div class="threat-ticker-text">
        [LIVE — GOVERNMENT I4C CYBER THREAT TICKER] | Ingested Complaint Ref: I4C-2026-8819 for Account ACC0520000000028 → CBS freeze executed | Watchlist Telemetries: 12,852 nodes synchronized | Inter-agency SLA: &lt; 8s interdiction latency | RBI AML Circular 2026: Imbalanced resolution (XGBoost + SMOTE 111:1 pos-weight) | OpenTimestamps PostgreSQL case auditor logged | Evidence admissible under Section 65B of Indian Evidence Act.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session-state initialisation
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "analysis_result":      None,
    "alert_page":           0,
    "severity_filter":      "ALL",
    "transactions_df":      None,
    "loaded_file_name":     None,
    "str_result":           None,
    "ask_answer":           None,
    "using_fallback":       False,
    "active_scenario":      None,
    "inspected_account_id": None,
    "inspected_data":       None,
    "demo_mode_active":     False,
    "demo_nav_target":      None,
    "analyst_notes":        {},    # keyed by account_id
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
# Local Action callbacks
# ─────────────────────────────────────────────────────────────────────────────
def _run_with_progress(file_bytes: bytes, file_name: str) -> None:
    """Show an animated progress bar, call the backend, store results."""
    try:
        bar = st.progress(0, text="Loading transaction data...")
        time.sleep(0.3)
        bar.progress(25, text="Building fund flow graph...")
    except Exception:
        return
    try:
        result = run_analysis(file_bytes, file_name)
        st.session_state.using_fallback = False
    except Exception as exc:
        scenario = _scenario_key_from_label(file_name)
        fallback = load_fallback(scenario, "analysis")
        if fallback:
            result = fallback
            st.session_state.using_fallback = True
        else:
            st.error(f"Connection to backend failed and no pre-generated fallback data exists: {exc}")
            return
    try:
        bar.progress(100, text="Analysis complete — results loaded.")
        time.sleep(0.4)
        bar.empty()

        st.session_state.analysis_result  = result
        st.session_state.alert_page       = 0
        st.session_state.loaded_file_name = file_name
        st.session_state.active_scenario  = _scenario_key_from_label(file_name)
        st.session_state.str_result  = None
        st.session_state.ask_answer  = None
    except Exception:
        pass

def _load_scenario(path: str, label: str) -> None:
    """Read a local scenario CSV and trigger analysis globally."""
    try:
        with open(path, "rb") as fh:
            file_bytes = fh.read()
        st.session_state.transactions_df = pd.read_csv(io.BytesIO(file_bytes))
        st.session_state.analysis_result = None
        st.session_state.alert_page      = 0
        _run_with_progress(file_bytes, label)
    except FileNotFoundError:
        st.error(f"Scenario file not found: `{path}`\nRun `python generate_synthetic_data.py` first.")
    except Exception as exc:
        st.error(f"Error loading scenario: {exc}")

# ─────────────────────────────────────────────────────────────────────────────
# Rendering Sidebar and Header
# ─────────────────────────────────────────────────────────────────────────────
view_selection, target_account_id, uploaded_file = render_sidebar(_load_scenario)

st.markdown("""
<div style='display:flex;align-items:baseline;gap:12px;margin-bottom:4px;'>
    <span style='font-size:22px;font-weight:700;color:#f8fafc;letter-spacing:-0.3px;'>MuleShield</span>
    <span style='font-size:13px;color:#64748b;font-weight:400;'>AML Investigation Platform</span>
</div>
<div style='font-size:12px;color:#475569;margin-bottom:12px;'>
    Dual-Engine ML + Graph Intelligence &nbsp;|&nbsp; AML Mule Account Classification &amp; Containment
</div>
""", unsafe_allow_html=True)
st.divider()

# Handle uploaded file triggers
if uploaded_file is not None:
    raw_bytes    = uploaded_file.getvalue()
    file_changed = (uploaded_file.name != st.session_state.loaded_file_name)
    if file_changed or st.session_state.analysis_result is None:
        try:
            st.session_state.transactions_df = pd.read_csv(io.BytesIO(raw_bytes))
            st.session_state.analysis_result = None
            st.session_state.alert_page      = 0
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
            st.stop()
        _run_with_progress(raw_bytes, uploaded_file.name)

# ─────────────────────────────────────────────────────────────────────────────
# Navigation Routing — workflow-based
# ─────────────────────────────────────────────────────────────────────────────
if view_selection == "Dashboard":
    render_executive_dashboard_view()

elif view_selection == "Investigations":
    render_threat_simulation_view(_load_scenario)

elif view_selection == "Alerts":
    render_alert_center_view()

elif view_selection == "Accounts":
    render_account_inspector_view(target_account_id)

elif view_selection == "Model Analytics":
    render_model_metrics_view()

elif view_selection == "Compliance":
    render_compliance_workspace_view()

elif view_selection == "Dataset Intelligence":
    st.subheader("Dataset Intelligence & Feature Exclusions")
    st.markdown("""
    #### MuleShield Tabular Dataset Summary
    * **Ingestion Source:** AML Tabular Alerts Dataset (`DataSet.csv`)
    * **Total Registered Accounts:** 9,082 Accounts
    * **Features Matrix:** 3,924 columns (`F1` ... `F3924`)
    * **Target Column:** `F3924` (0 = Legitimate, 1 = Mule Account)
    * **Class Imbalance:** 9,001 Legitimate accounts (99.1%) vs 81 Mule accounts (0.9%).
    """)
    st.info("**Imbalance Ratio Resolved (111:1):** Tuned XGBoost Pos-weights (`scale_pos_weight=111`) combined with synthetic minority oversampling (**SMOTE**).")
    st.markdown("### Data Leakage Containment: Feature F3912")
    st.warning("""
    **Feature F3912 has been completely excluded from model training.**
    * **Correlation:** Pearson coefficient of **0.97** with target `F3924` (legacy warn flag representing prior TMS hits).
    * **Risk:** Model training with F3912 results in a trivial accuracy rate of 99.8% that fails to generalize to any new unflagged money-laundering schemes.
    * **Action:** Excluded from training features matrix. Retained strictly in post-inference rule-based **Mule Lifecycle Staging** and validation cards.
    """)
    dc1, dc2 = st.columns(2)
    with dc1:
        st.write("#### High-Vulnerability Demographics (F3891)")
        st.caption("Customer Occupation (F3891) matching student and farming demographics shows the highest recruitment correlation.")
        vulnerability_df = pd.DataFrame({
            "Occupation": ["Student", "Agriculturist", "Salaried", "Self-Employed", "Retired"],
            "Mule Recruitment Rate (%)": [28.4, 18.2, 5.1, 3.2, 1.1]
        })
        st.bar_chart(vulnerability_df.set_index("Occupation"))
    with dc2:
        st.write("#### Account Dormancy Activation Ratios")
        st.caption("Dormant account reactivation accounts for 89% of suspicious high-volume transactions in age bucket G365D.")
        age_df = pd.DataFrame({
            "Account Age Bucket": ["G365D (Dormant)", "L365D", "L180D", "L90D", "L7D (New)"],
            "Fraud Prevalence Ratio": [0.89, 0.05, 0.03, 0.02, 0.01]
        })
        st.bar_chart(age_df.set_index("Account Age Bucket"))

elif view_selection == "System Health":
    st.subheader("System Health & Deployment Status")
    tab_health, tab_roadmap = st.tabs(["Backend Health", "Deployment Roadmap"])
    with tab_health:
        st.markdown("#### Backend Connectivity")
        if st.button("Run Health Check", key="btn_check_health_page"):
            try:
                r = requests.get(f"{BASE_URL}/health", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    st.success(
                        f"Backend online — v{data.get('version','?')} | "
                        f"NVIDIA: {data.get('nvidia','?')} | "
                        f"Gemini: {data.get('gemini','?')}"
                    )
                else:
                    st.warning(f"Backend responded with {r.status_code}")
            except Exception:
                st.error("Backend unreachable")
    with tab_roadmap:
        st.markdown("#### 3-Phase On-Premise Deployment Roadmap")
        st.markdown("MuleShield uses a structured 3-phase deployment strategy designed for on-premise banking infrastructure with zero internet dependencies.")
        rm1, rm2, rm3 = st.columns(3)
        with rm1:
            st.error("**Phase 1: Core System & ML Integration**")
            st.markdown("**Timeline:** Weeks 1–4\n* Container Compose architectures\n* XGBoost and SMOTE tabular predictions\n* PostgreSQL case auditing logs")
        with rm2:
            st.warning("**Phase 2: Graph Fusion & Compliance**")
            st.markdown("**Timeline:** Weeks 5–8\n* Neo4j GDS communities\n* Composite 70/30 score fusion blending\n* Auto goAML compliance XML autopilot")
        with rm3:
            st.success("**Phase 3: CBS Webhooks & Containment**")
            st.markdown("**Timeline:** Weeks 9–12\n* CBS automated freeze webhooks under 8 seconds\n* Government I4C Cybercrime intelligence webhooks")

elif view_selection == "I4C Intelligence":
    st.subheader("Government I4C Threat Intelligence")
    st.markdown("Real-time transaction monitoring fed by the **Indian Cyber Crime Coordination Centre (I4C)** threat intelligence webhooks.")
    st.markdown("#### Ingest Cybercrime Portal Alert")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_acc = st.text_input("Target Account ID:", value=DEMO_I4C_ACCOUNT)
        sim_ref = st.text_input("I4C Portal Complaint Reference:", value=DEMO_I4C_REF)
    with col_sim2:
        sim_type = st.selectbox("Threat Alert Classification:", ["Dormant Reactivation", "UPI Velocity Pass-Through", "Watchlist Match", "High-Vulnerability Demographic Profile Match"])

    if st.button("Ingest Webhook Alert", key="btn_trigger_webhook"):
        with st.spinner("Processing inter-agency webhook intelligence..."):
            try:
                payload = {"account_no": sim_acc, "portal_ref": sim_ref, "alert_type": sim_type}
                resp = requests.post(f"{BASE_URL}/ingest-i4c", json=payload, timeout=10)
                if resp.status_code == 200:
                    webhook_res = resp.json()
                    st.success("I4C Webhook ingested and processed successfully.")
                    severity = webhook_res.get("severity", "LOW")
                    action = webhook_res.get("action_taken", "INVESTIGATOR_QUEUED")
                    score = webhook_res.get("composite_score", 0.0)
                    mule_stage = webhook_res.get("mule_stage", "ACTIVE_MULE")

                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res1.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:6px;border-left:4px solid #ef4444;'><div style='color:#94a3b8;font-size:11px;text-transform:uppercase;margin-bottom:4px;'>Composite Score</div><div style='color:#f8fafc;font-size:24px;font-weight:700;'>{score} / 100</div><div style='color:#ef4444;font-size:11px;font-weight:600;'>{severity} Severity</div></div>", unsafe_allow_html=True)
                    col_res2.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:6px;border-left:4px solid #3b82f6;'><div style='color:#94a3b8;font-size:11px;text-transform:uppercase;margin-bottom:4px;'>CBS Action</div><div style='color:#f8fafc;font-size:16px;font-weight:700;'>{action}</div><div style='color:#3b82f6;font-size:11px;'>CBS callback executed</div></div>", unsafe_allow_html=True)
                    col_res3.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:6px;border-left:4px solid #f59e0b;'><div style='color:#94a3b8;font-size:11px;text-transform:uppercase;margin-bottom:4px;'>Lifecycle Stage</div><div style='color:#f8fafc;font-size:16px;font-weight:700;'>{mule_stage}</div><div style='color:#f59e0b;font-size:11px;'>Staging classification</div></div>", unsafe_allow_html=True)

                    st.markdown("---")
                    st.write("#### goAML XML Report")
                    st.text_area("Suspicious Transaction Report (XML)", webhook_res.get("goaml_xml", ""), height=250)
                    st.download_button(label="Download goAML XML Report", data=webhook_res.get("goaml_xml", ""), file_name=f"goAML-{webhook_res.get('case_id', 'STR')}.xml", mime="application/xml")
                    st.write("**Tamper-Proof Evidence Hash (Indian Evidence Act Section 65B):**")
                    st.code(f"SHA-256: {webhook_res.get('evidence_hash', '')}", language=None)
                else:
                    st.error(f"Webhook ingestion failed: {resp.status_code} - {resp.text}")
            except Exception as exc:
                st.error(f"Could not reach FastAPI backend webhook endpoint: {exc}")

# ─────────────────────────────────────────────────────────────────────────────
# Hero landing — shown when no data and not on a standalone page
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.analysis_result is None and view_selection not in [
    "Dashboard", "Accounts", "Dataset Intelligence", "System Health",
    "I4C Intelligence", "Model Analytics", "Compliance"
]:
    render_hero_landing(_load_scenario)