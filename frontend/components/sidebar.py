# frontend/components/sidebar.py

import requests
import streamlit as st
from frontend.utils.constants import BASE_URL

def render_sidebar(load_scenario_callback) -> tuple[str, str, object]:
    """Renders the comprehensive sidebar panel. Returns (view_selection, target_account_id, uploaded_file)."""
    with st.sidebar:
        st.markdown("## 🛡️ MuleShield AI")
        st.caption("Real-Time Mule Account Detection")
        st.markdown("---")
        
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1e293b,#0f172a);padding:10px 12px;border-radius:8px;border:1px solid #38bdf8;margin-bottom:12px;'>
            <span style='color:#38bdf8;font-weight:bold;font-size:12px;text-transform:uppercase;'>🎮 Demo Mode Active</span><br/>
            <span style='color:#94a3b8;font-size:11px;'>One-click scenarios — no typing needed</span>
        </div>
        """, unsafe_allow_html=True)
        
        view_selection = st.radio(
            "🧭 System Navigation",
            ["🎮 Demo Mode", "📈 Executive Dashboard", "🕵️ Alert Center", "🔍 Account Inspector", "📐 Model Metrics", "📊 Dataset Intelligence", "⚙️ Deployment Roadmap", "🌐 I4C Webhook Auditor"],
            index=0
        )
        
        st.markdown("---")
        
        uploaded_file = None
        target_account_id = "ACC0520000000028"
        
        if view_selection == "🕵️ Alert Center":
            st.header("📂 Data Input")
            uploaded_file = st.file_uploader(
                "Upload Target CSV",
                type=["csv"],
                help="Upload transactional log CSV or DataSet.csv features file.",
            )
        elif view_selection == "🔍 Account Inspector":
            st.header("🔍 Account Lookup")
            target_account_id = st.text_input(
                "Enter Account ID:",
                value="ACC0520000000028",
                help="Enter Account ID (ACC052 + 11-digit zero-padded index, e.g. ACC0520000000028 or ACC0520000009082).",
            )
            st.markdown("---")
            st.subheader("⚡ Quick Demo Scenarios")
            if st.button("🔁 Round-Trip Fraud", key="sb_roundtrip"):
                load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
            if st.button("💰 Structuring / Smurfing", key="sb_structuring"):
                load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
            if st.button("💤 Dormant Reactivation", key="sb_dormant"):
                load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")
        elif view_selection == "🎮 Demo Mode":
            st.markdown("### 🎮 Sandbox Scenarios")
            st.caption("One-click launch. No configuration.")
            if st.button("🔁 Round-Trip Fraud", key="dm_sb_roundtrip", use_container_width=True):
                load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
                st.session_state.demo_mode_active = True
            if st.button("💰 Structuring / Smurfing", key="dm_sb_structuring", use_container_width=True):
                load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
                st.session_state.demo_mode_active = True
            if st.button("💤 Dormant Reactivation", key="dm_sb_dormant", use_container_width=True):
                load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")
                st.session_state.demo_mode_active = True

        st.markdown("---")
        st.write("🔧 **System Health Dashboard**")
        if st.button("🩺 Check Backend Health", key="btn_check_health"):
            try:
                r = requests.get(f"{BASE_URL}/health", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    st.success(
                        f"✅ Backend online v{data.get('version','?')} | "
                        f"NVIDIA: {data.get('nvidia','?')} | "
                        f"Gemini: {data.get('gemini','?')}"
                    )
                else:
                    st.warning(f"Backend responded with {r.status_code}")
            except Exception:
                st.error("❌ Backend unreachable")
                
    return view_selection, target_account_id, uploaded_file
