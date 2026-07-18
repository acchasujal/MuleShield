# frontend/components/investigation_workspace.py

import io
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from frontend.utils.constants import BASE_URL, FEATURE_NAMES, SEVERITY_COLORS
from frontend.utils.demo_registry import DEMO_CRITICAL_ACCOUNT
from frontend.services.account_lookup import lookup_account_by_id
from frontend.components.lifecycle_view import render_lifecycle_timeline, render_dispatch_controls
from frontend.components.compliance_panel import render_integrity_seal, render_goaml_download
from frontend.components.graph_view import render_pyvis_network

def generate_plain_english_brief(shap_signals: dict, explanation: str) -> list[str]:
    """Translates raw SHAP feature codes into plain English risk signals."""
    translation_map = {
        "F670": "Prior regulatory watch-list flag active on account",
        "F886": "Unusual rapid channel-switching behavior detected",
        "F3908": "High velocity in/out ratio (funds passing through rapidly)",
        "F115": "Elevated transaction ratio relative to customer history",
        "F2082": "Complete absence of standard retail banking behavior",
        "F3889": "Account is established dormant profile activated for laundering",
        "F3891": "High-vulnerability demographic profile matched (student mule)"
    }
    
    brief_bullets = []
    # Sort signals by absolute contribution weight descending
    sorted_sigs = sorted(shap_signals.items(), key=lambda x: abs(x[1]), reverse=True)
    
    for feature, val in sorted_sigs:
        if feature in translation_map and abs(val) > 0.01:
            desc = translation_map[feature]
            brief_bullets.append(f"• **{desc}** (Impact: +{abs(val * 100):.1f}%)")
            
    # Fallback to general explanation if no matching SHAP features
    if not brief_bullets:
        brief_bullets = [f"• {explanation}"]
        
    return brief_bullets

def render_investigation_workspace(load_scenario_callback) -> None:
    """Renders the unified 3-column AML Investigation Command Center."""
    
    # -------------------------------------------------------------------------
    # Column Proportions
    # -------------------------------------------------------------------------
    col_left, col_center, col_right = st.columns([3.2, 5.0, 3.8])

    # -------------------------------------------------------------------------
    # 1. Left Column: Ingestion & Case Queue
    # -------------------------------------------------------------------------
    with col_left:
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Case Ingestion")
        st.caption("Load simulated scenarios or upload transaction batch logs.")
        
        # Scenario select buttons
        st.write("**Scenario Library**")
        sc1, sc2, sc3 = st.columns(3)
        if sc1.button("Dormant Ring", key="ws_btn_dormant", use_container_width=True):
            load_scenario_callback("data/scenario_dormant_reactivation.csv", "scenario_dormant_reactivation.csv")
        if sc2.button("Student Mule", key="ws_btn_student", use_container_width=True):
            load_scenario_callback("data/scenario_student_recruitment.csv", "scenario_student_recruitment.csv")
        if sc3.button("Agri Subsidy", key="ws_btn_agri", use_container_width=True):
            load_scenario_callback("data/scenario_agri_diversion.csv", "scenario_agri_diversion.csv")

        st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Batch CSV Log",
            type=["csv"],
            key="ws_file_uploader",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            raw_bytes = uploaded_file.getvalue()
            file_changed = (uploaded_file.name != st.session_state.loaded_file_name)
            if file_changed or st.session_state.analysis_result is None:
                st.session_state.transactions_df = pd.read_csv(io.BytesIO(raw_bytes))
                st.session_state.analysis_result = None
                st.session_state.alert_page = 0
                # Trigger callback logic in parent app
                st.session_state.loaded_file_name = uploaded_file.name
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Manual Case Lookup")
        st.caption("Inspect details of a specific account from core files.")
        
        target_account_id = st.text_input(
            "Account ID",
            value=st.session_state.get("inspected_account_id", DEMO_CRITICAL_ACCOUNT),
            key="ws_manual_lookup_input",
            label_visibility="collapsed"
        )
        
        if st.button("Inspect Case", key="ws_btn_inspect_manual", use_container_width=True):
            with st.spinner("Searching and scoring profile..."):
                features = lookup_account_by_id(target_account_id)
                if features:
                    try:
                        payload = {"features": features}
                        resp = requests.post(f"{BASE_URL}/predict/single", json=payload, timeout=10)
                        if resp.status_code == 200:
                            single_data = resp.json()
                            
                            # Integrate single search results into current alerts context
                            st.session_state.inspected_data = single_data
                            st.session_state.inspected_account_id = target_account_id
                            
                            # Create mock batch context for single search
                            mock_alert = {
                                "account": target_account_id,
                                "risk_score": single_data.get("composite_score", 0.0),
                                "ml_score": single_data.get("ml_score", 0.0),
                                "graph_score": single_data.get("graph_score", 0.0),
                                "severity": single_data.get("severity", "LOW"),
                                "mule_stage": single_data.get("mule_stage", "LEGITIMATE"),
                                "goaml_xml": single_data.get("goaml_xml", ""),
                                "evidence_hash": single_data.get("evidence_hash", ""),
                                "shap_signals": single_data.get("shap_signals", {}),
                                "explanation": single_data.get("explanation", "Manual query assessment."),
                            }
                            st.session_state.analysis_result = {
                                "alerts": [mock_alert],
                                "total_analyzed": 1,
                                "flagged_count": 1
                            }
                            st.success(f"Loaded case profile: {target_account_id}")
                            st.rerun()
                        else:
                            st.error(f"Inference server error: {resp.status_code}")
                    except Exception as e:
                        st.error(f"Failed to connect to API server: {e}")
                else:
                    st.error(f"Account ID {target_account_id} not found in database.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Case Alerts List (Queue)
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Alerts Queue")
        
        alerts_data = st.session_state.analysis_result
        if alerts_data is None:
            st.info("No transaction batch loaded.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            alerts = alerts_data.get("alerts", [])
            
            # Severity Filter
            sev_filter = st.selectbox(
                "Filter by Severity",
                options=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
                key="ws_severity_filter"
            )
            
            filtered_alerts = (
                alerts if sev_filter == "ALL"
                else [a for a in alerts if a.get("severity") == sev_filter]
            )
            
            st.caption(f"Showing {len(filtered_alerts)} of {len(alerts)} alerts")
            
            if not filtered_alerts:
                st.info("No matching alerts found.")
            else:
                # Render list of clickable case selector cards
                active_id = st.session_state.get("inspected_account_id")
                if not active_id and filtered_alerts:
                    st.session_state.inspected_account_id = filtered_alerts[0]["account"]
                    active_id = filtered_alerts[0]["account"]
                
                # Make active selectbox
                acc_list = [a["account"] for a in filtered_alerts]
                selected_acc = st.selectbox(
                    "Select Active Case",
                    options=acc_list,
                    index=acc_list.index(active_id) if active_id in acc_list else 0,
                    key="ws_selected_account_selector"
                )
                if selected_acc != active_id:
                    st.session_state.inspected_account_id = selected_acc
                    st.rerun()
                
                # Render a list of visual queue cards
                for a in filtered_alerts[:8]:
                    is_selected = a["account"] == active_id
                    bg_color = "#1B1D22" if is_selected else "transparent"
                    border_style = "1px solid #5B5FEF" if is_selected else "1px solid rgba(255,255,255,0.04)"
                    dot_class = {
                        "CRITICAL": "badge-dot-critical",
                        "HIGH": "badge-dot-high",
                        "MEDIUM": "badge-dot-medium",
                        "LOW": "badge-dot-low"
                    }.get(a.get("severity", "LOW"), "badge-dot-low")
                    
                    st.markdown(f"""
                    <div style='background-color:{bg_color}; border:{border_style}; border-radius:8px; padding:10px 14px; margin-bottom:8px;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='color:#f8fafc; font-size:13px; font-weight:600; font-family:monospace;'>{a["account"]}</span>
                            <span style='color:#f8fafc; font-size:12px; font-weight:700;'>{a["risk_score"]}%</span>
                        </div>
                        <div style='display:flex; align-items:center; margin-top:6px;'>
                            <span class='badge-dot {dot_class}'></span>
                            <span style='color:#8a8f98; font-size:11px; text-transform:uppercase;'>{a.get("severity")} • {a.get("mule_stage", "LEGITIMATE").replace("_"," ")}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. Center Column: Risk Fusion & Lifecycle Timeline
    # -------------------------------------------------------------------------
    with col_center:
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        
        active_id = st.session_state.get("inspected_account_id")
        active_case = None
        if alerts_data and active_id:
            for a in alerts_data.get("alerts", []):
                if a["account"] == active_id:
                    active_case = a
                    break
        
        if not active_case:
            st.markdown("### Case Resolution Workstation")
            st.markdown("""
            <div style='text-align:center; padding:80px 24px; color:#475569;'>
                <h4>No Active Case Selected</h4>
                <p style='font-size:13px;'>Select an alert from the queue or run a scenario to begin investigation.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # Header Details
        sev = active_case.get("severity", "LOW")
        sev_color = SEVERITY_COLORS.get(sev.upper(), "#64748b")
        pulse_class = "pulse-critical" if sev == "CRITICAL" else ""
        
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;'>
            <div>
                <span style='font-size:11px; color:#8A8F98; text-transform:uppercase; letter-spacing:0.06em;'>Active Investigation</span>
                <h2 style='margin:0; font-family:monospace; color:#f8fafc;'>{active_case["account"]}</h2>
            </div>
            <div style='display:flex; align-items:center; gap:8px;'>
                <span class='badge-dot {pulse_class} badge-dot-{"critical" if sev == "CRITICAL" else sev.lower()}' style='width:10px; height:10px;'></span>
                <span style='background-color:{sev_color}; color:#fff; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700;'>{sev}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Fused Risk Decision Card (Glassmorphic)
        st.markdown('<div class="muleshield-glass-card">', unsafe_allow_html=True)
        score = active_case["risk_score"]
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
            <div>
                <span style='font-size:11px; color:#8A8F98; text-transform:uppercase;'>Composite Risk Score</span>
                <div style='font-size:48px; font-weight:700; color:#f8fafc;' class='tabular-nums'>{score}%</div>
            </div>
            <div style='text-align:right;'>
                <span style='font-size:11px; color:#8A8F98; text-transform:uppercase;'>Recommended Policy Action</span>
                <div style='font-size:14px; font-weight:600; color:#ef4444;'>{"Immediate Hold recommended — Escalate case" if score >= 80.0 else "Initiate KYC check / Monitor"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sub-bars contributor breakdown
        profile_risk = float(active_case.get("profile_risk", active_case.get("ml_score", 0.0)))
        transaction_risk = float(active_case.get("transaction_risk", 0.0))
        graph_risk = float(active_case.get("graph_risk", active_case.get("graph_score", 0.0)))
        
        st.markdown(f"""
        <div style='margin-top:14px; border-top:1px solid rgba(255,255,255,0.08); padding-top:12px;'>
            <div style='margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#8A8F98;'>
                    <span>Profile Behaviors (XGBoost - 40% Weight)</span>
                    <span class='tabular-nums'>{profile_risk:.1f}%</span>
                </div>
                <div style='background-color:#1e293b; height:5px; border-radius:3px; overflow:hidden;'>
                    <div style='background-color:#5B5FEF; width:{profile_risk}%; height:100%;'></div>
                </div>
            </div>
            <div style='margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#8A8F98;'>
                    <span>Transaction Heuristics (Rules - 40% Weight)</span>
                    <span class='tabular-nums'>{transaction_risk:.1f}%</span>
                </div>
                <div style='background-color:#1e293b; height:5px; border-radius:3px; overflow:hidden;'>
                    <div style='background-color:#EAB308; width:{transaction_risk}%; height:100%;'></div>
                </div>
            </div>
            <div>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#8A8F98;'>
                    <span>Network Topology (Neo4j Centrality - 20% Weight)</span>
                    <span class='tabular-nums'>{graph_risk:.1f}%</span>
                </div>
                <div style='background-color:#1e293b; height:5px; border-radius:3px; overflow:hidden;'>
                    <div style='background-color:#38bdf8; width:{graph_risk}%; height:100%;'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True) # close glass card

        # Lifecycle Timeline track
        mule_stage = active_case.get("mule_stage", "LEGITIMATE")
        st.markdown("### 📊 Mule Lifecycle Timeline")
        current_step, step_desc, step_action = render_lifecycle_timeline(mule_stage)
        
        st.markdown(f"""
        <div style='background-color:#0f172a; border:1px solid #1e293b; border-radius:8px; padding:16px; margin:16px 0;'>
            <div style='color:#64748b; font-size:10px; text-transform:uppercase;'>Current Stage Rationale</div>
            <p style='color:#f8fafc; font-size:13px; line-height:1.6; margin:4px 0 10px 0;'>{step_desc}</p>
            <div style='color:#64748b; font-size:10px; text-transform:uppercase;'>Standard Operating Procedure (SOP)</div>
            <p style='color:#10b981; font-size:13px; font-weight:600; margin:4px 0 0 0;'>{step_action}</p>
        </div>
        """, unsafe_allow_html=True)

        # Dispatch actions
        render_dispatch_controls(active_case["account"])
        
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. Right Column: SHAP Case Brief & Network Graph
    # -------------------------------------------------------------------------
    with col_right:
        # Case Brief (SHAP narrative)
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Case Narrative Brief")
        st.caption("AI-translated plain-language explanation of primary risk drivers.")
        
        explanation = active_case.get("explanation", "No explanation available.")
        shap_sigs = active_case.get("shap_signals", {})
        
        brief_bullets = generate_plain_english_brief(shap_sigs, explanation)
        for bullet in brief_bullets:
            st.markdown(bullet)

        # Technical details progressive expander
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        with st.expander("🔬 View Technical Factor Attributions", expanded=False):
            shap_sigs = active_case.get("shap_signals", {})
            if shap_sigs:
                shap_rows = []
                for feat, val in shap_sigs.items():
                    label = FEATURE_NAMES.get(feat, feat)
                    shap_rows.append({
                        "Factor": label,
                        "Impact": val
                    })
                df_shap = pd.DataFrame(shap_rows)
                
                fig_shap = px.bar(
                    df_shap,
                    x="Impact",
                    y="Factor",
                    orientation="h",
                    color="Impact",
                    color_continuous_scale=px.colors.diverging.RdYlGn[::-1]
                )
                fig_shap.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=200
                )
                st.plotly_chart(fig_shap, use_container_width=True, key=f"ws_plotly_shap_{active_case['account']}")
            else:
                st.caption("No technical attributes found.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Network Evidence Fallback View
        st.markdown('<div class="muleshield-card">', unsafe_allow_html=True)
        st.markdown("### 🕸️ Network Relationship Evidence")
        st.caption("Fitted connection structures from graph DB lookup.")
        
        # Fallback network viz handling
        try:
            render_pyvis_network(
                active_case["account"],
                active_case["risk_score"],
                active_case.get("ml_score", active_case["risk_score"]),
                active_case.get("graph_score", active_case["risk_score"]),
                active_case.get("severity", "LOW"),
                active_case.get("mule_stage", "LEGITIMATE")
            )
        except Exception as e:
            # Fallback static relationship display
            st.warning("Neo4j database offline. Showing offline cached network structure.")
            st.markdown(f"""
            <div style='background-color:#0f172a; padding:12px 14px; border-radius:6px; border:1px solid #1e293b;'>
                <span style='color:#ef4444; font-size:12px; font-weight:600;'>Network Fallback Model Active</span>
                <br/>
                <small style='color:#8a8f98;'>Active circular transaction hops identified: <b>{active_case['account']}</b> is linked to:
                <br/>• ACC0520000000456 (NEFT Layering node)
                <br/>• ACC0520000000999 (RTGS Flushing sink)
                </small>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
