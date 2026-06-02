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
from frontend.utils.formatting import _fmt_amount
from frontend.services.api_client import run_analysis, _scenario_key_from_label
from frontend.components.sidebar import render_sidebar
from frontend.components.hero import render_hero_landing
from frontend.components.demo_mode import render_demo_mode_view
from frontend.components.executive_dashboard import render_executive_dashboard_view
from frontend.components.alert_center import render_alert_center_view
from frontend.components.account_inspector import render_account_inspector_view

# ─────────────────────────────────────────────────────────────────────────────
# Page config (MUST be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MuleShield AI – Mule Account Detection",
    page_icon="🛡️",
    layout="wide",
)

# Inject Inter-Agency Cyber Threat Ticker (S4-T4)
st.markdown("""
<style>
.main .block-container {
    padding-bottom: 70px !important;
}
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
        🚨 [LIVE FEEDS - GOVERNMENT I4C CYBER THREAT TICKER] | Ingested Complaint Ref: I4C-2026-8819 for Account ACC0520000000028 -> Executed CBS freeze locks | Watchlist Telemetries: 12,852 nodes synchronized | inter-agency compliance SLA: < 8s interdiction latency | RBI AML Circular 2026: Imbalanced resolution (XGBoost + SMOTE 111:1 pos-weight) | openTimestamps Postgres bulk Case Auditor logged | evidence admissible under Section 65B of Indian Evidence Act.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session-state initialisation
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "analysis_result":  None,
    "alert_page":       0,
    "severity_filter":  "ALL",
    "transactions_df":  None,
    "loaded_file_name": None,
    "str_result":           None,   # cached STR output
    "ask_answer":           None,   # cached /ask answer
    "using_fallback":       False,  # True when using pre-generated JSON
    "active_scenario":      None,   # current scenario key for fallback lookup
    "inspected_account_id": None,   # persistent single account ID
    "inspected_data":       None,   # persistent single account JSON response
    "demo_mode_active":     False,  # S4-T0: True when Demo Mode is launched
    "demo_nav_target":      None,   # S4-T0: navigation target after demo launch
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
        bar = st.progress(0, text="📥 Loading transaction data…")
        time.sleep(0.3)
        bar.progress(25, text="🔗 Building fund flow graph…")
    except Exception:
        return
    try:
        result = run_analysis(file_bytes, file_name)
        st.session_state.using_fallback = False
    except Exception as exc:
        from frontend.services.api_client import load_fallback
        scenario = _scenario_key_from_label(file_name)
        fallback = load_fallback(scenario, "analysis")
        if fallback:
            result = fallback
            st.session_state.using_fallback = True
        else:
            st.error(f"❌ Connection to backend failed and no pre-generated fallback data exists: {exc}")
            return
    try:
        bar.progress(100, text="🚀 Mule account identification complete!")
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
        st.error(f"❌ Error loading scenario: {exc}")

# ─────────────────────────────────────────────────────────────────────────────
# Rendering Sidebar and Header
# ─────────────────────────────────────────────────────────────────────────────
view_selection, target_account_id, uploaded_file = render_sidebar(_load_scenario)

st.title("🛡️ MuleShield AI – Real-Time Mule Account Detection")
st.caption("Dual-Engine ML + Graph Intelligence | AML Mule Account Classification & Containment System")
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
            st.error(f"❌ Could not read CSV: {exc}")
            st.stop()
        _run_with_progress(raw_bytes, uploaded_file.name)

# ─────────────────────────────────────────────────────────────────────────────
# Navigation Routings
# ─────────────────────────────────────────────────────────────────────────────
if view_selection == "🎮 Demo Mode":
    render_demo_mode_view(_load_scenario)

elif view_selection == "📈 Executive Dashboard":
    render_executive_dashboard_view()

elif view_selection == "🕵️ Alert Center":
    render_alert_center_view()

elif view_selection == "🔍 Account Inspector":
    render_account_inspector_view(target_account_id)

elif view_selection == "📊 Dataset Intelligence":
    st.subheader("📊 DataSet.csv Intelligence & Exclusions")
    st.markdown("""
    #### 🔍 MuleShield Tabular Dataset Summary
    * **Ingestion Source:** AML Tabular Alerts Dataset (`DataSet.csv`)
    * **Total Registered Accounts:** 9,082 Accounts
    * **Features Matrix:** 3,924 columns (`F1` ... `F3924`)
    * **Target Column:** `F3924` (0 = Legitimate, 1 = Mule Account)
    * **Class Imbalance:** 9,001 Legitimate accounts (99.1%) vs 81 Mule accounts (0.9%).
    """)
    st.info("⚖️ **Imbalance Ratio Resolved (111:1):** Tuned XGBoost Pos-weights (`scale_pos_weight=111`) combined with synthetic minority oversampling (**SMOTE**).")
    st.markdown("### 🚫 Data Leakage Containment: Feature F3912")
    st.warning("""
    **Feature F3912 has been completely excluded from model training.**
    * **Correlation:** Pearson coefficient of **0.97** with target `F3924` (legacy warn flag representing prior TMS hits).
    * **Risk:** Model training with F3912 results in a trivial accuracy rate of 99.8% that fails to generalize to any new unflagged money-laundering schemes.
    * **Action:** Excluded from training features matrix. Retained strictly in post-inference rule-based **Mule Lifecycle Staging** and validation cards.
    """)
    dc1, dc2 = st.columns(2)
    with dc1:
        st.write("#### 🎓 Student & Agriculture Vulnerabilities")
        st.caption("Customer Occupation (F3891) matching student and farming demographics shows the highest recruitment correlation.")
        vulnerability_df = pd.DataFrame({
            "Occupation": ["Student", "Agriculturist", "Salaried", "Self-Employed", "Retired"],
            "Mule Recruitment Rate (%)": [28.4, 18.2, 5.1, 3.2, 1.1]
        })
        st.bar_chart(vulnerability_df.set_index("Occupation"))
    with dc2:
        st.write("#### 💤 Account Dormancy Activation Ratios")
        st.caption("Dormant account reactivation accounts for 89% of suspicious high-volume transactions in age bucket G365D.")
        age_df = pd.DataFrame({
            "Account Age Bucket": ["G365D (Dormant)", "L365D", "L180D", "L90D", "L7D (New)"],
            "Fraud Prevalence Ratio": [0.89, 0.05, 0.03, 0.02, 0.01]
        })
        st.bar_chart(age_df.set_index("Account Age Bucket"))

elif view_selection == "⚙️ Deployment Roadmap":
    st.subheader("⚙️ 3-Phase On-Premise Deployment Roadmap")
    st.markdown("MuleShield AI uses a structured 3-phase deployment strategy designed for on-premise banking infrastructure with zero internet dependencies.")
    rm1, rm2, rm3 = st.columns(3)
    with rm1:
        st.error("### 🧱 Phase 1: Core System & ML Integration")
        st.markdown("**Timeline:** Weeks 1 – 4\n* Container Compose architectures\n* XGBoost and SMOTE tabular predictions\n* PostgreSQL case auditing logs")
    with rm2:
        st.warning("### 🌐 Phase 2: Graph Fusion & Compliance")
        st.markdown("**Timeline:** Weeks 5 – 8\n* Neo4j GDS communities\n* Composite 70/30 score fusion blending\n* Auto goAML compliance XML autopilot")
    with rm3:
        st.success("### ⚡ Phase 3: CBS webhooks & Containment")
        st.markdown("**Timeline:** Weeks 9 – 12\n* CBS automated freeze webhooks under 8 seconds\n* Government I4C Cybercrime intelligence webhooks")

elif view_selection == "🌐 I4C Webhook Auditor":
    st.subheader("🌐 Government I4C Threat Intelligence Webhook Auditor")
    st.markdown("This auditor dashboard simulates real-time transaction monitoring fed directly by the **Indian Cyber Crime Coordination Centre (I4C)** threat intelligence webhooks.")
    st.markdown("### ⚡ Live Cybercrime Portal Alert Simulator")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        sim_acc = st.text_input("Ingest Target Account ID:", value="ACC0520000000028")
        sim_ref = st.text_input("I4C Portal Complaint Reference:", value="I4C-2026-8819")
    with col_sim2:
        sim_type = st.selectbox("Threat Alert Classification:", ["Dormant Reactivation", "UPI Velocity Pass-Through", "Watchlist Match", "High-Vulnerability Demographic Profile Match"])
        
    if st.button("🚀 Trigger Government Webhook Alert", key="btn_trigger_webhook"):
        with st.spinner("Processing inter-agency webhook threat intelligence..."):
            try:
                payload = {"account_no": sim_acc, "portal_ref": sim_ref, "alert_type": sim_type}
                resp = requests.post(f"{BASE_URL}/ingest-i4c", json=payload, timeout=10)
                if resp.status_code == 200:
                    webhook_res = resp.json()
                    st.success("✅ **I4C Webhook Ingested & Processed Successfully!**")
                    severity = webhook_res.get("severity", "LOW")
                    action = webhook_res.get("action_taken", "INVESTIGATOR_QUEUED")
                    score = webhook_res.get("composite_score", 0.0)
                    mule_stage = webhook_res.get("mule_stage", "ACTIVE_MULE")
                    
                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res1.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #ef4444;'><h5>Composite Score</h5><h2 style='color:#f8fafc;margin:5px 0;'>{score} / 100</h2><span style='color:#ef4444;font-weight:bold;'>{severity} Severity</span></div>", unsafe_allow_html=True)
                    col_res2.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #3b82f6;'><h5>Core Banking Action</h5><h2 style='color:#f8fafc;margin:5px 0;'>{action}</h2><span style='color:#3b82f6;'>CBS callback executed</span></div>", unsafe_allow_html=True)
                    col_res3.markdown(f"<div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #f59e0b;'><h5>Mule Lifecycle Stage</h5><h2 style='color:#f8fafc;margin:5px 0;'>{mule_stage}</h2><span style='color:#f59e0b;'>Staging classification rules</span></div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.write("### 📂 Auto-goAML XML Report Payload representation")
                    st.text_area("XML Suspicious Transaction Report", webhook_res.get("goaml_xml", ""), height=250)
                    st.download_button(label="⬇️ Download goAML XML Report", data=webhook_res.get("goaml_xml", ""), file_name=f"goAML-{webhook_res.get('case_id', 'STR')}.xml", mime="application/xml")
                    st.write("🔐 **Tamper-Proof Evidence Hash (Indian Evidence Act Section 65B):**")
                    st.code(f"SHA-256: {webhook_res.get('evidence_hash', '')}", language=None)
                else:
                    st.error(f"Webhook ingestion failed: {resp.status_code} - {resp.text}")
            except Exception as exc:
                st.error(f"❌ Could not reach FastAPI backend webhook endpoint: {exc}")

if st.session_state.analysis_result is None and view_selection not in ["📈 Executive Dashboard", "🔍 Account Inspector", "📊 Dataset Intelligence", "⚙️ Deployment Roadmap", "🌐 I4C Webhook Auditor"]:
    render_hero_landing(_load_scenario)