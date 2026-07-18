# frontend/components/sidebar.py

import streamlit as st
from frontend.utils.demo_registry import DEMO_CRITICAL_ACCOUNT

def render_sidebar() -> tuple[str, str, object]:
    """Renders the professional sidebar navigation panel. Returns (view_selection, target_account_id, uploaded_file)."""
    with st.sidebar:
        # Platform identity
        st.markdown("""
        <div style='padding:12px 4px 8px 4px;'>
            <div style='font-size:17px;font-weight:700;color:#f8fafc;letter-spacing:-0.2px;'>MuleShield</div>
            <div style='font-size:11px;color:#64748b;margin-top:2px;text-transform:uppercase;letter-spacing:0.06em;'>AML Command Center</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1e293b;margin:4px 0 12px 0;'/>", unsafe_allow_html=True)

        # Workflow-based navigation
        view_selection = st.radio(
            "Navigation",
            [
                "Overview",
                "Investigate",
                "Reports",
            ],
            index=0,
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:#1e293b;margin:12px 0;'/>", unsafe_allow_html=True)

        uploaded_file = None
        target_account_id = st.session_state.get("inspected_account_id", DEMO_CRITICAL_ACCOUNT)

    return view_selection, target_account_id, uploaded_file
