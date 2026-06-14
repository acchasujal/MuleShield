# frontend/components/sidebar.py

import requests
import streamlit as st
from frontend.utils.constants import BASE_URL

def render_sidebar(load_scenario_callback) -> tuple[str, str, object]:
    """Renders the professional sidebar navigation panel. Returns (view_selection, target_account_id, uploaded_file)."""
    with st.sidebar:
        # Platform identity
        st.markdown("""
        <div style='padding:12px 4px 8px 4px;'>
            <div style='font-size:17px;font-weight:700;color:#f8fafc;letter-spacing:-0.2px;'>MuleShield</div>
            <div style='font-size:11px;color:#64748b;margin-top:2px;text-transform:uppercase;letter-spacing:0.06em;'>AML Investigation Platform</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1e293b;margin:4px 0 12px 0;'/>", unsafe_allow_html=True)

        # Workflow-based navigation
        view_selection = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Investigations",
                "Alerts",
                "Accounts",
                "Model Analytics",
                "Compliance",
                "I4C Intelligence",
                "Dataset Intelligence",
                "System Health",
            ],
            index=0,
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'/>", unsafe_allow_html=True)

        uploaded_file = None
        target_account_id = "ACC0520000000028"

        if view_selection == "Alerts":
            st.markdown("**Data Input**")
            uploaded_file = st.file_uploader(
                "Upload Transaction CSV",
                type=["csv"],
                help="Upload a transactional log CSV or DataSet.csv features file.",
            )

        elif view_selection == "Accounts":
            st.markdown("**Account Lookup**")
            target_account_id = st.text_input(
                "Account ID",
                value="ACC0520000000028",
                help="Enter Account ID (e.g. ACC0520000000028 to ACC0520000009082).",
            )
            st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'/>", unsafe_allow_html=True)
            st.markdown("**Load Investigation Dataset**")
            if st.button("Round-Trip Layering", key="sb_roundtrip", use_container_width=True):
                load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
            if st.button("Structuring / Smurfing", key="sb_structuring", use_container_width=True):
                load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
            if st.button("Dormant Reactivation", key="sb_dormant", use_container_width=True):
                load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")

        elif view_selection == "Investigations":
            st.markdown("**Threat Simulation Library**")
            st.caption("Pre-loaded transaction intelligence datasets.")
            if st.button("Round-Trip Layering", key="dm_sb_roundtrip", use_container_width=True):
                load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
                st.session_state.demo_mode_active = True
            if st.button("Structuring / Smurfing", key="dm_sb_structuring", use_container_width=True):
                load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
                st.session_state.demo_mode_active = True
            if st.button("Dormant Reactivation", key="dm_sb_dormant", use_container_width=True):
                load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")
                st.session_state.demo_mode_active = True

        # System health check in sidebar (compact)
        st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'/>", unsafe_allow_html=True)
        if st.button("System Health Check", key="btn_check_health"):
            try:
                r = requests.get(f"{BASE_URL}/health", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    st.success(
                        f"Backend online v{data.get('version','?')} | "
                        f"NVIDIA: {data.get('nvidia','?')} | "
                        f"Gemini: {data.get('gemini','?')}"
                    )
                else:
                    st.warning(f"Backend: HTTP {r.status_code}")
            except Exception:
                st.error("Backend unreachable")

    return view_selection, target_account_id, uploaded_file
