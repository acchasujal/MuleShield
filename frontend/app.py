# frontend/app.py

import sys
sys.path.insert(0, '.')

import io
import time
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timezone

from frontend.utils.constants import BASE_URL
from frontend.services.api_client import run_analysis, _scenario_key_from_label, load_fallback
from frontend.components.sidebar import render_sidebar
from frontend.components.hero import render_hero_landing
from frontend.components.executive_dashboard import render_executive_dashboard_view
from frontend.components.investigation_workspace import render_investigation_workspace
from frontend.components.compliance_panel import render_compliance_workspace_view

# ─────────────────────────────────────────────────────────────────────────────
# Page config (MUST be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MuleShield — AML Investigation Platform",
    page_icon="🛡️",
    layout="wide",
)

# Inject Inter font + custom design system stylesheet
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
try:
    with open("frontend/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading design system stylesheet: {e}")

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
view_selection, target_account_id, uploaded_file = render_sidebar()

st.markdown("""
<div style='display:flex;align-items:baseline;gap:12px;margin-bottom:4px;'>
    <span style='font-size:22px;font-weight:700;color:#f8fafc;letter-spacing:-0.3px;'>MuleShield</span>
    <span style='font-size:13px;color:#64748b;font-weight:400;'>AML Command Center</span>
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
if view_selection == "Overview":
    render_executive_dashboard_view()

elif view_selection == "Investigate":
    if st.session_state.analysis_result is None:
        render_hero_landing(_load_scenario)
    else:
        render_investigation_workspace(_load_scenario)

elif view_selection == "Reports":
    render_compliance_workspace_view()